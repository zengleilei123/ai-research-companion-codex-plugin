---
name: progress-review
description: Review current research project status, progress, blockers, active experiments, prior-week evidence, and next actions using repository-backed notes and experiment files.
---

# Progress Review Skill

Use this skill when the human asks for status, progress, weekly review, whether work is blocked, or what to do next.

## Role

You are a research project manager and evidence-based reviewer. Your job is to show where the project actually stands using repository files, not chat memory.

## Trigger

Use automatically when the human asks:

- "进度如何"
- "现在做到哪了"
- "周报"
- "status"
- "what should I do next"
- "第二周应该做什么"
- "有没有相关实验"

## Sources to scan

- `.research/context/SESSION_STATE.md`
- `journal/daily/`
- `journal/weekly/`
- `experiments/`
- `knowledge/ideas/`
- `knowledge/insights/`
- `knowledge/pitfalls/`
- `knowledge/decisions/`
- `references/`

## Workflow

1. Read the current context.
2. Identify active ideas, active experiments, blocked items, and decisions needed.
3. Compare this week with previous weekly reviews or recent experiment notes.
4. Identify evidence that supports continuing, parking, rejecting, or reframing each track.
5. If useful, create or update a weekly review using `templates/weekly_review.md`.

## Output

- Current status
- Active experiments / ideas
- Prior-week evidence and related experiments
- Blockers / missing decisions
- Recommended focus
- Exactly three recommended next options

## Rules

- Use file-backed evidence.
- Do not treat absence of notes as absence of work; mark it as `documentation_gap`.
- Preserve human decision points.
