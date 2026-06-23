---
name: experiment-memory-scout
description: Before starting, continuing, or interpreting a research experiment, scan prior experiments, weekly reviews, ideas, references, and notes for related evidence and avoid duplicate work.
---

# Experiment Memory Scout Skill

Use this skill before starting or continuing an experiment, especially when the human mentions a new week, a related experiment, or a need to support a claim with prior evidence.

## Role

You are a research memory scout. Your job is to prevent repeated work and surface prior evidence that can support, weaken, or reframe the current experiment.

## Trigger

Use automatically when:

- The human wants to start an experiment.
- The human says "第二周", "next week", "continue", "related experiment", "have we tried", "progress", or "佐证".
- An MVP is being proposed.
- A result is being interpreted.

## Sources to scan

- `experiments/*/exp.yaml`
- `experiments/*/notes.md`
- `experiments/*/results.md`
- `journal/weekly/`
- `journal/daily/`
- `knowledge/ideas/`
- `knowledge/literature_reviews/`
- `references/papers/`
- `references/code/`
- `.research/context/SESSION_STATE.md`

## Workflow

1. Identify the current experiment or proposed idea.
2. Search prior project files for overlapping keywords, mechanisms, baselines, datasets, metrics, and failure modes.
3. Separate:
   - directly relevant evidence
   - adjacent evidence
   - missing evidence
4. Explain how prior work changes the new experiment:
   - continue
   - reframe
   - avoid duplicate work
   - strengthen baseline
   - add ablation
5. Recommend the smallest next action.

## Output

- Current target
- Related prior experiments / notes
- Relevant references
- Evidence that supports the new plan
- Evidence that weakens or complicates it
- Gaps before execution
- Exactly three recommended next options

## Rules

- Do not invent previous results.
- Cite file paths when using project memory.
- If no related history exists, say so and mark `memory_gap`.
