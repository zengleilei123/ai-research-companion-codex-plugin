#!/usr/bin/env python3
"""Collect a read-only AI Research Companion status board.

The script emits a compact status-bar view, JSON, or markdown. It uses only the
Python standard library and does not modify the project unless --write-status is
provided.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


CHECKPOINT_SUFFIXES = {".pt", ".pth", ".ckpt", ".safetensors", ".bin"}
LOG_SUFFIXES = {".log", ".out", ".err"}
ALERT_PATTERNS = {
    "nan_or_inf": re.compile(r"\b(nan|inf|infinity)\b", re.IGNORECASE),
    "oom": re.compile(r"(out of memory|cuda.*oom|cuda error.*memory)", re.IGNORECASE),
    "traceback": re.compile(r"traceback \(most recent call last\)", re.IGNORECASE),
    "killed": re.compile(r"\b(killed|sigkill|terminated)\b", re.IGNORECASE),
}


def run_git(repo: Path, args: list[str], timeout: int = 5) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "stdout": "", "stderr": str(exc)}
    return {"ok": proc.returncode == 0, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}


def file_info(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "path": str(path)}
    stat = path.stat()
    return {
        "exists": True,
        "path": str(path),
        "size_bytes": stat.st_size,
        "modified_at": stat.st_mtime,
        "age_seconds": max(0, time.time() - stat.st_mtime),
    }


def newest(paths: list[Path]) -> dict[str, Any] | None:
    existing = [p for p in paths if p.exists() and p.is_file()]
    if not existing:
        return None
    return file_info(max(existing, key=lambda p: p.stat().st_mtime))


def count_markdown_rows(path: Path) -> int:
    if not path.exists():
        return 0
    rows = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and "---" not in stripped and not stripped.lower().startswith("| key"):
            rows += 1
    return max(0, rows - 1)


def parse_simple_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw or raw.lstrip().startswith("#") or raw.startswith(" "):
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def iter_files(repo: Path, roots: list[str], suffixes: set[str], max_files: int) -> list[Path]:
    found: list[Path] = []
    for root_name in roots:
        root = repo / root_name
        if not root.exists():
            continue
        if root.is_file() and root.suffix.lower() in suffixes:
            found.append(root)
        elif root.is_dir():
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__", "node_modules"}]
                for filename in filenames:
                    path = Path(dirpath) / filename
                    if path.suffix.lower() in suffixes:
                        found.append(path)
                        if len(found) >= max_files:
                            return found
    return found


def scan_alerts(paths: list[Path], max_bytes: int) -> list[str]:
    alerts: set[str] = set()
    for path in paths:
        try:
            with path.open("rb") as handle:
                handle.seek(0, os.SEEK_END)
                size = handle.tell()
                handle.seek(max(0, size - max_bytes), os.SEEK_SET)
                text = handle.read().decode("utf-8", errors="replace")
        except OSError:
            continue
        for name, pattern in ALERT_PATTERNS.items():
            if pattern.search(text):
                alerts.add(name)
    return sorted(alerts)


def score(label: str, value: int, status: str, signals: list[str]) -> dict[str, Any]:
    return {"label": label, "score": max(0, min(100, value)), "status": status, "signals": signals}


def classify_score(value: int) -> str:
    if value >= 80:
        return "ok"
    if value >= 50:
        return "watch"
    return "gap"


def bar(value: int, width: int = 10) -> str:
    filled = round(max(0, min(100, value)) / 100 * width)
    return "[" + "#" * filled + "-" * (width - filled) + f"] {value:3d}%"


def collect(repo: Path, max_files: int, stale_hours: float) -> dict[str, Any]:
    now = time.time()
    research = repo / ".research"
    settings = research / "settings.yaml"
    status_md = research / "status.md"
    session = research / "context" / "SESSION_STATE.md"
    next_prompt = research / "context" / "NEXT_PROMPT.md"
    changes_index = research / "changes" / "index.md"
    change_entries = sorted((research / "changes").glob("*.md")) if (research / "changes").exists() else []

    experiment_dirs = sorted([p for p in (repo / "experiments").glob("*") if p.is_dir()]) if (repo / "experiments").exists() else []
    experiments = []
    monitor_files: list[Path] = []
    result_files: list[Path] = []
    for exp_dir in experiment_dirs:
        exp_yaml = exp_dir / "exp.yaml"
        exp = parse_simple_yaml(exp_yaml)
        monitor = exp_dir / "monitor.md"
        results = exp_dir / "results.md"
        if monitor.exists():
            monitor_files.append(monitor)
        if results.exists():
            result_files.append(results)
        experiments.append(
            {
                "path": str(exp_dir),
                "id": exp.get("id", exp_dir.name),
                "status": exp.get("status", "unknown"),
                "has_exp_yaml": exp_yaml.exists(),
                "has_monitor": monitor.exists(),
                "has_results": results.exists(),
            }
        )

    log_files = iter_files(repo, ["experiments", "logs", "runs", "outputs"], LOG_SUFFIXES, max_files)
    checkpoint_files = iter_files(repo, ["experiments", "checkpoints", "runs", "outputs", "artifacts"], CHECKPOINT_SUFFIXES, max_files)
    alerts = scan_alerts(log_files[-20:], 200_000)
    newest_log = newest(log_files)
    newest_checkpoint = newest(checkpoint_files)

    papers_index = repo / "references" / "papers" / "index.md"
    code_index = repo / "references" / "code" / "index.md"
    paper_rows = count_markdown_rows(papers_index)
    code_rows = count_markdown_rows(code_index)

    git_status = run_git(repo, ["status", "--short"])
    git_head = run_git(repo, ["log", "-1", "--oneline"])
    dirty_lines = [line for line in git_status.get("stdout", "").splitlines() if line.strip()]

    stale_seconds = stale_hours * 3600
    session_fresh = session.exists() and file_info(session).get("age_seconds", stale_seconds + 1) <= stale_seconds
    next_fresh = next_prompt.exists() and file_info(next_prompt).get("age_seconds", stale_seconds + 1) <= stale_seconds
    change_fresh = bool(change_entries) and file_info(change_entries[-1]).get("age_seconds", stale_seconds + 1) <= stale_seconds
    log_fresh = newest_log is not None and newest_log.get("age_seconds", stale_seconds + 1) <= stale_seconds
    checkpoint_fresh = newest_checkpoint is not None and newest_checkpoint.get("age_seconds", stale_seconds + 1) <= stale_seconds

    project_memory_score = 0
    project_signals = []
    if research.exists():
        project_memory_score += 30
        project_signals.append(".research exists")
    if settings.exists():
        project_memory_score += 25
        project_signals.append("settings exists")
    if session.exists():
        project_memory_score += 20
        project_signals.append("session state exists")
    if next_prompt.exists():
        project_memory_score += 15
        project_signals.append("next prompt exists")
    if status_md.exists():
        project_memory_score += 10
        project_signals.append("status file exists")

    exp_score = 0
    exp_signals = []
    if experiments:
        exp_score += 45
        exp_signals.append(f"{len(experiments)} experiment folders")
    if any(exp["status"] in {"running", "active", "planned"} for exp in experiments):
        exp_score += 25
        exp_signals.append("active/planned experiment found")
    if monitor_files:
        exp_score += 15
        exp_signals.append("monitor notes found")
    if result_files:
        exp_score += 15
        exp_signals.append("result notes found")

    train_score = 0
    train_signals = []
    if log_files:
        train_score += 35
        train_signals.append(f"{len(log_files)} log files")
    if log_fresh:
        train_score += 20
        train_signals.append("fresh log")
    if checkpoint_files:
        train_score += 25
        train_signals.append(f"{len(checkpoint_files)} checkpoints")
    if checkpoint_fresh:
        train_score += 10
        train_signals.append("fresh checkpoint")
    if monitor_files:
        train_score += 10
        train_signals.append("experiment monitor file")
    if alerts:
        train_score = min(train_score, 45)
        train_signals.append("training alerts detected")

    reference_score = 0
    reference_signals = []
    if papers_index.exists():
        reference_score += 30
        reference_signals.append("paper index exists")
    if code_index.exists():
        reference_score += 30
        reference_signals.append("code index exists")
    reference_score += min(20, paper_rows * 5)
    reference_score += min(20, code_rows * 5)
    if paper_rows:
        reference_signals.append(f"{paper_rows} paper rows")
    if code_rows:
        reference_signals.append(f"{code_rows} code rows")

    change_score = 0
    change_signals = []
    if changes_index.exists():
        change_score += 45
        change_signals.append("change index exists")
    if change_entries:
        change_score += 25
        change_signals.append(f"{len(change_entries)} change entries")
    if change_fresh:
        change_score += 20
        change_signals.append("fresh change entry")
    if not dirty_lines:
        change_score += 10
        change_signals.append("git clean")
    elif changes_index.exists():
        change_signals.append(f"{len(dirty_lines)} git changes need recording")

    handoff_score = 0
    handoff_signals = []
    if session.exists():
        handoff_score += 35
        handoff_signals.append("session state exists")
    if next_prompt.exists():
        handoff_score += 35
        handoff_signals.append("next prompt exists")
    if session_fresh:
        handoff_score += 15
        handoff_signals.append("fresh session")
    if next_fresh:
        handoff_score += 15
        handoff_signals.append("fresh next prompt")

    bars = [
        score("Project Memory", project_memory_score, classify_score(project_memory_score), project_signals),
        score("Experiments", exp_score, classify_score(exp_score), exp_signals),
        score("Training Observed", train_score, classify_score(train_score), train_signals),
        score("References", reference_score, classify_score(reference_score), reference_signals),
        score("Change Memory", change_score, classify_score(change_score), change_signals),
        score("Context Handoff", handoff_score, classify_score(handoff_score), handoff_signals),
    ]
    overall = round(sum(item["score"] for item in bars) / len(bars)) if bars else 0

    gaps: list[str] = []
    if not research.exists():
        gaps.append("missing .research workspace")
    if not experiments:
        gaps.append("no experiment folders")
    if not log_files and not checkpoint_files:
        gaps.append("no training logs or checkpoints detected")
    if not papers_index.exists() or not code_index.exists():
        gaps.append("reference indexes missing")
    if dirty_lines and not change_fresh:
        gaps.append("git changes may need change-memory")
    if not session.exists() or not next_prompt.exists():
        gaps.append("context handoff files missing")
    gaps.extend(alerts)

    return {
        "generated_at": now,
        "repo": str(repo),
        "overall": score("Overall", overall, classify_score(overall), []),
        "bars": bars,
        "git": {
            "head": git_head.get("stdout", ""),
            "dirty_count": len(dirty_lines),
            "status_short": dirty_lines[:20],
        },
        "experiments": experiments[:20],
        "training": {
            "log_count": len(log_files),
            "checkpoint_count": len(checkpoint_files),
            "newest_log": newest_log,
            "newest_checkpoint": newest_checkpoint,
            "alerts": alerts,
        },
        "references": {"paper_rows": paper_rows, "code_rows": code_rows},
        "context": {
            "session": file_info(session),
            "next_prompt": file_info(next_prompt),
            "latest_change": file_info(change_entries[-1]) if change_entries else None,
        },
        "gaps": gaps,
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = ["Research Status Board", f"Overall             {bar(payload['overall']['score'])} {payload['overall']['status']}"]
    for item in payload["bars"]:
        lines.append(f"{item['label']:<19} {bar(item['score'])} {item['status']}")
    lines.append("")
    lines.append(f"Git: {payload['git']['head'] or 'unknown'}; dirty={payload['git']['dirty_count']}")
    lines.append(
        "Training: "
        f"logs={payload['training']['log_count']}, "
        f"checkpoints={payload['training']['checkpoint_count']}, "
        f"alerts={','.join(payload['training']['alerts']) or 'none'}"
    )
    lines.append(f"References: papers={payload['references']['paper_rows']}, code={payload['references']['code_rows']}")
    if payload["gaps"]:
        lines.append("Gaps: " + "; ".join(payload["gaps"][:8]))
    else:
        lines.append("Gaps: none detected")
    return "\n".join(lines)


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Research Status Board",
        "",
        f"- Generated at: {time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime(payload['generated_at']))}",
        f"- Repository: `{payload['repo']}`",
        f"- Overall: `{bar(payload['overall']['score'])}` `{payload['overall']['status']}`",
        "",
        "| Area | Bar | Status | Signals |",
        "| --- | --- | --- | --- |",
    ]
    for item in payload["bars"]:
        signals = "; ".join(item["signals"]) if item["signals"] else "none"
        lines.append(f"| {item['label']} | `{bar(item['score'])}` | `{item['status']}` | {signals} |")
    lines.extend(
        [
            "",
            "## Signals",
            "",
            f"- Git: `{payload['git']['head'] or 'unknown'}`; dirty files: `{payload['git']['dirty_count']}`",
            f"- Training logs: `{payload['training']['log_count']}`",
            f"- Checkpoints: `{payload['training']['checkpoint_count']}`",
            f"- Alerts: `{', '.join(payload['training']['alerts']) or 'none'}`",
            f"- Reference rows: papers `{payload['references']['paper_rows']}`, code `{payload['references']['code_rows']}`",
            "",
            "## Gaps",
            "",
        ]
    )
    if payload["gaps"]:
        lines.extend(f"- {gap}" for gap in payload["gaps"])
    else:
        lines.append("- none detected")
    return "\n".join(lines) + "\n"


def render(payload: dict[str, Any], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(payload, indent=2, sort_keys=True)
    if output_format == "markdown":
        return render_markdown(payload)
    return render_text(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect an AI Research Companion status board.")
    parser.add_argument("--repo", default=".", help="Research project root.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write-status", nargs="?", const=".research/status.md", help="Write markdown status to this path.")
    parser.add_argument("--watch", action="store_true", help="Refresh the terminal view until interrupted.")
    parser.add_argument("--interval", type=float, default=30.0, help="Refresh interval in seconds for --watch.")
    parser.add_argument("--max-files", type=int, default=500, help="Maximum log/checkpoint files to scan.")
    parser.add_argument("--stale-hours", type=float, default=24.0, help="Freshness window for status files.")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()

    def emit_once() -> str:
        payload = collect(repo, args.max_files, args.stale_hours)
        output = render(payload, args.format)
        if args.write_status:
            target = Path(args.write_status)
            if not target.is_absolute():
                target = repo / target
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_markdown(payload), encoding="utf-8")
        return output

    if args.watch:
        try:
            while True:
                sys.stdout.write("\033[2J\033[H")
                sys.stdout.write(emit_once())
                sys.stdout.write("\n")
                sys.stdout.flush()
                time.sleep(max(1.0, args.interval))
        except KeyboardInterrupt:
            return 0

    print(emit_once())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
