---
name: project-schema
description: Create or validate the standard AI Research Companion project workspace structure and repository-backed research memory files. Use when starting a new project, onboarding an incomplete project, creating .research/settings.yaml, experiment folders, journal files, references indexes, or when other skills report documentation_gap, memory_gap, reference_gap, observability_gap, or missing templates.
---

# Project Schema Skill

Use this skill to create a stable project-local research memory layout. The goal is to remove guesswork for every other skill.

## Role

You are a research workspace bootstrapper and schema auditor. You create only project-local files needed for research memory, evidence tracking, and automation.

## Core Workflow

1. Inspect the repository root and identify whether it already has research state.
2. Read `references/workspace-schema.md` before creating or auditing files.
3. Classify the workspace:
   - `new_workspace`
   - `partial_workspace`
   - `schema_drift`
   - `ready`
4. Create only missing directories and starter files that are safe and generic.
5. Do not overwrite existing research notes, experiment results, references, or decisions.
6. Report exactly what was created, what already existed, and what remains a user decision.

## Minimum Project Layout

Create these directories when missing:

```text
.research/context/
.research/changes/
experiments/
journal/daily/
journal/weekly/
knowledge/ideas/
knowledge/insights/
knowledge/pitfalls/
knowledge/decisions/
knowledge/literature_reviews/
knowledge/paper_cards/
references/papers/
references/code/
```

Create starter files only when absent:

```text
.research/settings.yaml
.research/status.md
.research/context/SESSION_STATE.md
.research/context/NEXT_PROMPT.md
.research/changes/index.md
references/papers/index.md
references/code/index.md
```

## Experiment Folder Contract

When creating a new experiment folder, use:

```text
experiments/<YYYYMMDD_slug>/
  exp.yaml
  notes.md
  monitor.md
  results.md
```

`exp.yaml` must include at least:

- `id`
- `created_at`
- `status`
- `hypothesis`
- `baseline`
- `dataset`
- `metrics`
- `success_criteria`
- `failure_criteria`
- `run_paths`
- `owner_decision`

## Output

Return:

- Workspace classification
- Files/directories created
- Existing useful memory files
- Existing change-memory files
- Missing project decisions
- Risks from missing schema fields
- Exactly three recommended next options

## Rules

- Never place private research state inside this plugin repository.
- Do not overwrite existing user notes.
- Prefer `documentation_gap` over inventing missing information.
- Keep schema generic; project-specific details belong in the user's research project, not this plugin.
