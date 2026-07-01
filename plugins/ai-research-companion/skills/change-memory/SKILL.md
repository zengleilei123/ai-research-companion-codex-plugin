---
name: change-memory
description: Record repository-backed project change history, modification rationale, files changed, commands or tests run, evidence, decisions, risks, and next actions after research project edits, commits, experiment changes, refactors, documentation updates, or before context compression and agent handoff. Use when the user asks what changed, why changes were made, how to avoid losing modification memory, or when prior edits may be forgotten after long context.
---

# Research Change Memory

## Overview

Use this skill to preserve why a project changed, not only what the diff says. The output should help a future agent resume after context compression by reading repository-backed memory rather than relying on chat history.

## Role

You are the change historian for a human-led research project. You summarize edits, rationale, evidence, decisions, and unresolved risks into project-local memory files.

## Sources

Inspect the smallest useful set of sources:

- `git status --short`, `git diff --stat`, `git diff --cached --stat`, and recent commits
- `.research/context/SESSION_STATE.md` and `.research/context/NEXT_PROMPT.md`
- `.research/changes/index.md` and recent `.research/changes/*.md`
- touched experiment files such as `exp.yaml`, `notes.md`, `monitor.md`, and `results.md`
- relevant docs, configs, scripts, tests, logs, or generated artifacts mentioned by the user

Natural language is the primary interface. When deterministic git signals are useful, run the read-only helper:

```bash
plugins/ai-research-companion/skills/change-memory/scripts/collect_change_signals.py --repo . --include-diff-stat
```

## Workflow

1. Identify the project root. If no `.research/` layout exists, route to `project-schema` first.
2. Collect change signals from git and relevant project memory files.
3. Classify the change scope:
   - `research_decision`
   - `experiment_change`
   - `training_monitoring`
   - `literature_or_reference`
   - `code_or_config`
   - `documentation`
   - `workflow_or_skill`
4. Write a concise change entry that explains:
   - objective
   - files changed
   - rationale
   - evidence inspected
   - commands or tests run
   - decisions made
   - risks or unknowns
   - next actions
5. Update `.research/changes/index.md` with the newest entry.
6. Create or append to `.research/changes/YYYY-MM-DD.md` for the detailed session note.
7. If the user is about to compress context or switch agents, also ensure `context-companion` is run after this skill.

## File Contract

Create these files only inside the user's research project, never inside this plugin distribution repository:

```text
.research/changes/
  index.md
  YYYY-MM-DD.md
```

Use this index shape:

```text
# Change Memory Index

| Date | Scope | Summary | Evidence | Next |
| --- | --- | --- | --- | --- |
```

Use this daily entry shape:

```text
# Change Memory - YYYY-MM-DD

## HH:MM - short summary

- Objective:
- Scope:
- Files changed:
- Rationale:
- Evidence:
- Commands/tests:
- Decisions:
- Risks:
- Next actions:
```

## Rules

- Do not store secrets, credentials, private keys, raw dataset samples, or long diffs.
- Do not paste full logs; summarize only the decision-relevant signals and link paths.
- Do not overwrite prior memory. Append or create a new dated entry.
- Distinguish user-authored changes from agent-authored changes when evidence is available.
- Prefer concrete file paths and command names over vague summaries.
- If a change lacks a clear reason, record `rationale_gap` instead of inventing one.
- End with exactly three recommended next options when user action is needed.
