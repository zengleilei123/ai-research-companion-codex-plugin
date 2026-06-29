#!/usr/bin/env python3
"""Collect read-only ML training signals and emit JSON.

This script intentionally uses only the Python standard library. It is designed
for agents to run against local experiment folders, log files, checkpoint
directories, and optional GPU probes without modifying the training run.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any


ERROR_PATTERNS = {
    "nan_or_inf": re.compile(r"\b(nan|inf|infinity)\b", re.IGNORECASE),
    "oom": re.compile(r"(out of memory|cuda.*oom|cuda error.*memory)", re.IGNORECASE),
    "killed": re.compile(r"\b(killed|sigkill|terminated)\b", re.IGNORECASE),
    "traceback": re.compile(r"traceback \(most recent call last\)", re.IGNORECASE),
    "dataloader": re.compile(r"(dataloader|data loader|worker.*exited|broken pipe)", re.IGNORECASE),
}

METRIC_PATTERNS = [
    re.compile(
        r"(?P<name>train[_\s-]*loss|loss|val[_\s-]*loss|valid[_\s-]*loss|validation[_\s-]*loss|accuracy|acc|f1|auc|bleu|rouge|map|ndcg)"
        r"\s*[:=]\s*(?P<value>[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?P<name>train[_\s-]*loss|loss|val[_\s-]*loss|valid[_\s-]*loss|validation[_\s-]*loss|accuracy|acc|f1|auc|bleu|rouge|map|ndcg)"
        r"\s+(?P<value>[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)",
        re.IGNORECASE,
    ),
]


def read_tail(path: Path, max_bytes: int) -> str:
    with path.open("rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(max(0, size - max_bytes), os.SEEK_SET)
        return f.read().decode("utf-8", errors="replace")


def normalize_metric_name(name: str) -> str:
    return re.sub(r"[\s-]+", "_", name.lower())


def scan_log(path: Path, max_bytes: int) -> dict[str, Any]:
    try:
        text = read_tail(path, max_bytes)
    except OSError as exc:
        return {"path": str(path), "error": str(exc)}

    metrics: dict[str, float] = {}
    metric_events: list[dict[str, Any]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pattern in METRIC_PATTERNS:
            for match in pattern.finditer(line):
                name = normalize_metric_name(match.group("name"))
                value = float(match.group("value"))
                metrics[name] = value
                metric_events.append({"line_tail_index": line_no, "name": name, "value": value})

    alerts: list[str] = []
    for alert_name, pattern in ERROR_PATTERNS.items():
        if pattern.search(text):
            alerts.append(alert_name)

    stat = path.stat()
    return {
        "path": str(path),
        "size_bytes": stat.st_size,
        "modified_at": stat.st_mtime,
        "age_seconds": max(0, time.time() - stat.st_mtime),
        "latest_metrics": metrics,
        "metric_events_tail": metric_events[-20:],
        "alerts": alerts,
    }


def newest_file(paths: list[Path]) -> dict[str, Any] | None:
    existing = [p for p in paths if p.exists() and p.is_file()]
    if not existing:
        return None
    path = max(existing, key=lambda p: p.stat().st_mtime)
    stat = path.stat()
    return {
        "path": str(path),
        "size_bytes": stat.st_size,
        "modified_at": stat.st_mtime,
        "age_seconds": max(0, time.time() - stat.st_mtime),
    }


def collect_checkpoints(paths: list[Path]) -> dict[str, Any]:
    checkpoint_files: list[Path] = []
    suffixes = {".pt", ".pth", ".ckpt", ".safetensors", ".bin"}
    for path in paths:
        if not path.exists():
            continue
        if path.is_file() and path.suffix.lower() in suffixes:
            checkpoint_files.append(path)
        elif path.is_dir():
            for root, _, files in os.walk(path):
                for file_name in files:
                    candidate = Path(root) / file_name
                    if candidate.suffix.lower() in suffixes:
                        checkpoint_files.append(candidate)
    return {
        "count": len(checkpoint_files),
        "newest": newest_file(checkpoint_files),
    }


def collect_gpu() -> dict[str, Any]:
    try:
        proc = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=index,name,utilization.gpu,memory.used,memory.total",
                "--format=csv,noheader,nounits",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "error": str(exc)}

    if proc.returncode != 0:
        return {"available": False, "error": proc.stderr.strip() or proc.stdout.strip()}

    gpus = []
    for line in proc.stdout.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 5:
            continue
        gpus.append(
            {
                "index": parts[0],
                "name": parts[1],
                "utilization_gpu_percent": to_int(parts[2]),
                "memory_used_mb": to_int(parts[3]),
                "memory_total_mb": to_int(parts[4]),
            }
        )
    return {"available": True, "gpus": gpus}


def to_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def classify(logs: list[dict[str, Any]], checkpoints: dict[str, Any], max_stale_seconds: int) -> tuple[str, list[str]]:
    alerts: list[str] = []
    for log in logs:
        alerts.extend(log.get("alerts", []))
        age = log.get("age_seconds")
        if isinstance(age, (int, float)) and age > max_stale_seconds:
            alerts.append("stale_log")

    newest = checkpoints.get("newest")
    if newest is not None:
        age = newest.get("age_seconds")
        if isinstance(age, (int, float)) and age > max_stale_seconds:
            alerts.append("stale_checkpoint")

    unique_alerts = sorted(set(alerts))
    severe = {"oom", "killed", "traceback", "nan_or_inf"}
    if severe.intersection(unique_alerts):
        return "stop_or_restart", unique_alerts
    if unique_alerts:
        return "watch_closely", unique_alerts
    if not logs and checkpoints.get("count", 0) == 0:
        return "insufficient_signal", ["observability_gap"]
    return "healthy_continue", []


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect read-only training run signals as JSON.")
    parser.add_argument("--run", action="append", default=[], help="Experiment/run directory to inspect.")
    parser.add_argument("--log", action="append", default=[], help="Training log file to scan.")
    parser.add_argument("--checkpoint", action="append", default=[], help="Checkpoint file or directory.")
    parser.add_argument("--max-log-bytes", type=int, default=200_000)
    parser.add_argument("--max-stale-seconds", type=int, default=3600)
    parser.add_argument("--gpu", action="store_true", help="Run read-only nvidia-smi probe if available.")
    args = parser.parse_args()

    run_paths = [Path(p) for p in args.run]
    log_paths = [Path(p) for p in args.log]
    checkpoint_paths = [Path(p) for p in args.checkpoint]

    for run in run_paths:
        for pattern in ("*.log", "*.out", "*.err", "logs/*.log", "logs/*.out", "logs/*.err"):
            log_paths.extend(run.glob(pattern))
        for pattern in ("checkpoints", "checkpoint", "ckpts", "outputs", "artifacts"):
            candidate = run / pattern
            if candidate.exists():
                checkpoint_paths.append(candidate)

    logs = [scan_log(path, args.max_log_bytes) for path in sorted(set(log_paths)) if path.exists()]
    checkpoints = collect_checkpoints(sorted(set(checkpoint_paths)))
    health, alerts = classify(logs, checkpoints, args.max_stale_seconds)

    payload: dict[str, Any] = {
        "generated_at": time.time(),
        "run_paths": [str(p) for p in run_paths],
        "logs": logs,
        "checkpoints": checkpoints,
        "health": health,
        "alerts": alerts,
    }
    if args.gpu:
        payload["gpu"] = collect_gpu()

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
