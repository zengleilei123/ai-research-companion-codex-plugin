# AI Research Companion

Chinese version: [README.md](README.md)

AI Research Companion is an agent-native research workflow pack for Codex and Claude Code.
It is not a CLI app, server, or standalone product. It is a collection of `SKILL.md`
instructions that an agent can load while you work inside a research project.

Repository: https://github.com/zengleilei123/ai-research-companion-codex-plugin

## What This Is

AI Research Companion turns an AI coding agent into a stricter research partner. It helps you:

- onboard a new research project before coding
- check prior experiments, weekly reviews, papers, and reference code before judging an idea
- evaluate idea taste, engineering feasibility, novelty risk, MVP scope, and failure criteria
- end important conversations with three concrete next-step options
- run literature scouting, code-reference scouting, progress reviews, weekly reviews, and context handoff

This repository is plugin-only. It intentionally excludes private project state, experiments, journals, paper libraries, reference repos, and `.research` files.

## Compatibility

| Tool | Recommended setup | Invocation |
| --- | --- | --- |
| Codex App / Codex CLI | Install as a Codex plugin | Natural language, or `$ai-research-companion:research-mentor` |
| Claude Code | Copy or symlink skills into `.claude/skills/` or `~/.claude/skills/` | Natural language, or `/research-mentor` |
| Other Agent Skills tools | Reuse each `SKILL.md` directly | Tool-specific |

## Install for Codex

Add this repository as a Codex plugin marketplace:

```bash
codex plugin marketplace add https://github.com/zengleilei123/ai-research-companion-codex-plugin.git --sparse .agents/plugins
```

Restart Codex, open Plugins, and install:

```text
AI Research Companion
```

Then open Codex inside your research project and ask naturally:

```text
I have a new research idea. First onboard this project, then judge whether the idea is worth an MVP.
```

Or invoke a bundled skill explicitly:

```text
$ai-research-companion:research-mentor strictly evaluate this idea.
$ai-research-companion:literature-research survey related papers, baselines, and reference implementations.
$ai-research-companion:progress-review review project progress, blockers, and prior-week evidence.
```

## Use with Claude Code

Claude Code can load `SKILL.md` files directly. To install these skills for one project:

```bash
git clone https://github.com/zengleilei123/ai-research-companion-codex-plugin.git .agent-libs/ai-research-companion
mkdir -p .claude/skills
cp -R .agent-libs/ai-research-companion/plugins/ai-research-companion/skills/* .claude/skills/
```

Start Claude Code from the project root:

```bash
claude
```

Ask naturally:

```text
I am starting a new research project. Help me set it up, then identify missing papers, reference code, and prior experiment memory.
```

Or invoke skills explicitly:

```text
/project-onboarding
/research-mentor strictly evaluate this idea.
/literature-research find related papers, baselines, and code.
/weekly-review produce this week's research review.
```

To make the skills available across all projects:

```bash
mkdir -p ~/.claude/skills
cp -R plugins/ai-research-companion/skills/* ~/.claude/skills/
```

## Suggested Workflow

1. Project start: run `project-onboarding` to define the research question, hypothesis, data, baselines, MVP, and success/failure criteria.
2. Idea discussion: let `idea-judge` and `research-mentor` intervene during natural conversation instead of waiting for a command.
3. Survey: use `literature-research` to collect third-party papers, baselines, code, and novelty risks.
4. Before experiments: use `experiment-memory-scout` to inspect old experiments, weekly notes, related failures, and reusable evidence.
5. End of week: run `weekly-review` and classify tracks as continue, park, reject, or reframe.
6. Before context switching: use `context-companion` to preserve state and write the next starting prompt.

## Browser and Internet Access

This repository only provides research workflow skills. Web browsing, Chrome control, paper search, and GitHub access come from the host agent:

- Codex App: enable Codex Browser / Chrome / GitHub plugins as needed. These skills can then ask the agent to use those capabilities.
- Claude Code: use the web search, MCP, browser, or local tools configured in your Claude Code environment.

AI Research Companion decides when and how to research, evaluate, and organize evidence. The actual network or browser capability depends on your Codex or Claude Code setup.

## Included Skills

- `project-onboarding`
- `literature-research`
- `research-mentor`
- `idea-judge`
- `experiment-memory-scout`
- `progress-review`
- `weekly-review`
- `context-companion`

## Repository Contents

```text
.agents/plugins/marketplace.json
plugins/ai-research-companion/.codex-plugin/plugin.json
plugins/ai-research-companion/skills/
```

Do not add private research files such as `.research/`, `experiments/`, `journal/`, `references/`, logs, secrets, generated caches, or local databases to this repository.
