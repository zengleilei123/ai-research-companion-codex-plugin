---
name: research-router
description: Route ambiguous AI research requests to the right AI Research Companion skills and decide skill sequence. Use when a user asks a broad natural-language research question, starts a project, proposes an idea, asks for progress, mentions training, asks what to do next, or when multiple skills could apply and Codex needs an explicit routing decision.
---

# Research Router Skill

Use this skill to choose the smallest effective skill sequence. It prevents over-invoking skills and makes natural dialogue map to the right research workflow.

## Role

You are the dispatcher for AI Research Companion. Your job is to decide which skill should run first, which should run next, and which should not run yet.

## Routing Table

| User intent or signal | First skill | Follow-up skill |
| --- | --- | --- |
| New project, missing setup, generic starter | `project-schema` | `project-onboarding` |
| Raw idea, "is this worth doing" | `idea-judge` | `research-mentor`, then `literature-research` if references are missing |
| Need strict taste/feasibility review | `research-mentor` | `literature-research` or `experiment-memory-scout` |
| Related work, novelty, baseline, papers, repos | `literature-research` | `research-mentor` |
| Starting, continuing, or interpreting an experiment | `experiment-memory-scout` | `training-monitor` if a run exists |
| Active training run, GPU, logs, checkpoint, NaN/OOM/loss | `training-monitor` | `progress-review` |
| Status, blockers, "what next", second week | `progress-review` | `experiment-memory-scout` if experiments are involved |
| Weekly summary or track decision | `weekly-review` | `context-companion` |
| What changed, why it changed, modification history, long-context memory loss | `change-memory` | `context-companion` if resuming or handing off |
| Context compression, handoff, switching agents | `change-memory` if edits happened | `context-companion` |
| Missing schema/documentation/memory/reference/observability | `project-schema` | the originally requested skill |

## Decision Rules

1. Prefer one skill first unless evidence clearly requires a sequence.
2. Run `project-schema` before other skills when required files do not exist.
3. Run `literature-research` before execution when reference grounding is missing.
4. Run `experiment-memory-scout` before starting a new experiment.
5. Run `training-monitor` only when there is a run/log/checkpoint/resource signal to inspect.
6. Run `weekly-review` only when the user asks for a week-level review or enough recent evidence exists.
7. Run `change-memory` after meaningful edits, experiment changes, or workflow updates.
8. Run `context-companion` at the end of long sessions or before handoff.

## Output

Return:

- Detected intent
- Selected first skill
- Optional follow-up skills
- Why this route is minimal
- What information is required before execution
- Exactly three recommended next options when the routing itself is the main answer

## Rules

- Do not perform the full work of the selected skill inside this router.
- Do not route to external third-party skills unless they are installed in the project and the user asks for that layer.
- If two skills overlap, pick the one whose output is needed earliest.
