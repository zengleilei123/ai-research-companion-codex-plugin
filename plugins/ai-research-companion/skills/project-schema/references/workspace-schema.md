# AI Research Companion Workspace Schema

This schema defines project-local files that other skills can rely on. It is intentionally minimal and should be extended only inside the user's research project.

## Directory Layout

```text
.research/
  settings.yaml
  context/
    SESSION_STATE.md
    NEXT_PROMPT.md
experiments/
  <YYYYMMDD_slug>/
    exp.yaml
    notes.md
    monitor.md
    results.md
journal/
  daily/
  weekly/
knowledge/
  ideas/
  insights/
  pitfalls/
  decisions/
  literature_reviews/
references/
  papers/
    index.md
  code/
    index.md
```

## `.research/settings.yaml`

Recommended keys:

```yaml
project:
  name: ""
  domain: ""
  stage: "new"
  owner: ""

research:
  primary_question: ""
  target_venue_or_product: ""
  success_definition: ""
  failure_definition: ""

constraints:
  compute_budget: ""
  time_budget: ""
  data_access: ""
  reproducibility_requirements: ""

automation:
  training_monitor_interval: ""
  weekly_review_day: ""
  alert_channels: []

external_skills:
  supervisor_skills: false
  research_paper_writing: false
```

## `SESSION_STATE.md`

Use headings:

```text
# Session State

## Current Objective
## Active Idea
## Active Experiment
## Latest Evidence
## Decisions
## Open Questions
## Risks
## Files Changed
## Commands Run
## Next Action
```

## `NEXT_PROMPT.md`

Keep this short and executable:

```text
Continue this research project from repository-backed state.
First read .research/context/SESSION_STATE.md, then inspect the referenced experiment and notes.
The next action is: ...
```

## `exp.yaml`

Recommended structure:

```yaml
id: "20260629_example"
created_at: "2026-06-29"
status: "planned"
hypothesis: ""
baseline: ""
dataset: ""
metrics:
  primary: ""
  secondary: []
success_criteria: ""
failure_criteria: ""
run_paths:
  logs: []
  checkpoints: []
  tensorboard: []
  wandb: []
  mlflow: []
owner_decision:
  current: "undecided"
  updated_at: ""
```

## `monitor.md`

Use this file for short monitoring notes, not raw logs:

```text
# Training Monitor

## Latest Health
## Key Signals
## Alerts
## Decision
## Next Check
```

## Reference Indexes

`references/papers/index.md`:

```text
# Paper Index

| Key | Title | Link | Relevance | Status |
| --- | --- | --- | --- | --- |
```

`references/code/index.md`:

```text
# Code Reference Index

| Key | Repo | Link | Relevance | Status |
| --- | --- | --- | --- | --- |
```
