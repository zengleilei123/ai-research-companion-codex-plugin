#!/usr/bin/env python3
"""Collect read-only repository change signals and emit JSON.

This helper is intentionally conservative: it gathers status, diff statistics,
and the latest commit without printing full diffs or modifying the repository.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path
from typing import Any


def run_git(repo: Path, args: list[str], timeout: int = 8) -> dict[str, Any]:
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
        return {
            "cmd": "git " + " ".join(args),
            "returncode": None,
            "stdout": "",
            "stderr": str(exc),
        }

    return {
        "cmd": "git " + " ".join(args),
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect read-only git change signals as JSON.")
    parser.add_argument("--repo", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--include-diff-stat",
        action="store_true",
        help="Include unstaged and staged diff statistics, but not full diffs.",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    payload: dict[str, Any] = {
        "generated_at": time.time(),
        "repo": str(repo),
        "branch": run_git(repo, ["branch", "--show-current"]),
        "head": run_git(repo, ["rev-parse", "HEAD"]),
        "status_short": run_git(repo, ["status", "--short"]),
        "latest_commit": run_git(repo, ["log", "-1", "--oneline"]),
    }

    if args.include_diff_stat:
        payload["diff_stat"] = run_git(repo, ["diff", "--stat"])
        payload["cached_diff_stat"] = run_git(repo, ["diff", "--cached", "--stat"])

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
