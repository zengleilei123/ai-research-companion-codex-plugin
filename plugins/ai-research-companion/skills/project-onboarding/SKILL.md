---
name: project-onboarding
description: Set up a new or incomplete research project by inspecting project files, asking at most three key setup questions, and updating per-project research settings.
---

# Project Onboarding Skill

Use this skill when entering a new project, when `research_companion.md` is incomplete, or when the human asks how to set up the project.

## Role

You are a project setup companion. Your job is to turn a generic starter into a per-project research workspace without assuming the research direction.

## Trigger

Use automatically when:

- `project_name`, long-term goal, or research questions are blank or generic.
- The user says this is a new project.
- The user asks "how should I set this up?", "what do you need to know?", or similar.
- The agent cannot tell what research area, compute budget, or project boundaries apply.

## Workflow

1. Read `research_companion.md`, `.research/context/SESSION_STATE.md`, `AGENTS.md` or `CLAUDE.md`, and existing `knowledge/`, `experiments/`, `references/`.
2. Summarize what is already known and what is missing.
3. Ask at most three setup questions, prioritizing:
   - research objective / domain
   - current stage and success criteria
   - constraints: compute, time, datasets, codebase, writing target
4. If the human answers, update `research_companion.md` and `.research/context/SESSION_STATE.md`.
5. If the human does not answer but the task can proceed, state temporary assumptions and continue conservatively.

## Output

- Current project understanding
- Missing setup fields
- Up to three questions
- Suggested first research action
- Exactly three recommended next options

## Rules

- Do not make one project setting global for all projects.
- Do not force a full setup wizard before useful work if a small next step is clear.
- Prefer project files as source of truth over chat memory.
