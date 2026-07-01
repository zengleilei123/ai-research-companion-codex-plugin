---
name: status-board
description: Show a real-time or on-demand research project status board with text status bars, JSON, or markdown summaries for project setup, experiments, training observability, references, change memory, context handoff, git state, risks, and next actions. Use when the user asks for a status bar, dashboard, live observability, current project health, realtime monitoring overview, or a single page showing research progress and blockers.
---

# Research Status Board

## Overview

Use this skill to give the human one compact view of research state. It is not a replacement for `training-monitor`, `progress-review`, or `change-memory`; it is the observability front panel that decides what needs attention.

## Role

You are the research operations observer. You summarize status signals without changing experiments, processes, or research notes unless the user asks to write `.research/status.md`.

## Sources

Inspect read-only evidence first:

- `.research/settings.yaml`
- `.research/status.md`
- `.research/context/SESSION_STATE.md`
- `.research/context/NEXT_PROMPT.md`
- `.research/changes/index.md` and recent `.research/changes/*.md`
- `experiments/*/exp.yaml`, `notes.md`, `monitor.md`, and `results.md`
- `knowledge/paper_cards/*.md`
- `references/papers/index.md` and `references/code/index.md`
- training folders such as `logs/`, `runs/`, `outputs/`, `checkpoints/`, `artifacts/`, `wandb/`, and `mlruns/`
- git status and latest commit

Prefer the bundled collector:

```bash
plugins/ai-research-companion/skills/status-board/scripts/collect_status_board.py --repo . --format text
```

For a markdown status file:

```bash
plugins/ai-research-companion/skills/status-board/scripts/collect_status_board.py --repo . --format markdown --write-status .research/status.md
```

For terminal refresh:

```bash
plugins/ai-research-companion/skills/status-board/scripts/collect_status_board.py --repo . --format text --watch --interval 30
```

## Workflow

1. Identify the project root. If no `.research/` layout exists, route to `project-schema`.
2. Collect the status board JSON or text output with the bundled script.
3. Interpret the bars using research judgment:
   - `project_memory`
   - `experiment_memory`
   - `training_observability`
   - `references`
   - `change_memory`
   - `context_handoff`
4. If a bar is low, route to the specific skill:
   - setup gaps -> `project-schema` or `project-onboarding`
   - training gaps or alerts -> `training-monitor`
   - missing history -> `change-memory`
   - missing resume state -> `context-companion`
   - weak evidence/reference grounding -> `literature-research`
5. Return a compact dashboard and exactly three recommended next options.

## Output Contract

Use this shape in conversation:

```text
Research Status Board
Overall             [########--] 80% watch
Project Memory      [#########-] 90% ok
Experiments         [######----] 60% watch
Training Observed   [####------] 40% gap
References          [#######---] 70% ok
Change Memory       [########--] 80% ok
Context Handoff     [#####-----] 50% gap
```

Then list:

- active run or active experiment
- alerts
- stale files
- missing observability
- three next options

## Rules

- Do not claim live training health from stale logs.
- Treat missing logs, checkpoints, references, or context files as explicit gaps.
- Do not start, stop, or modify a training run.
- Do not write `.research/status.md` unless the user asks or the request explicitly needs a saved dashboard.
- Do not store secrets, raw logs, private keys, or full diffs in the status file.
- Use `training-monitor` for detailed run diagnosis; this skill is for the top-level panel.
