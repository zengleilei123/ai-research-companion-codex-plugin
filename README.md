# AI Research Companion for Codex

AI Research Companion is a Codex plugin that provides human-led research workflows:

- project onboarding
- literature and code reference scouting
- strict research mentor review
- idea taste judgment
- experiment memory scouting
- MVP planning support
- progress and weekly review
- context checkpointing

This repository is intentionally plugin-only. It does not include any private research project state, experiments, journals, references, or `.research` files.

## Install from GitHub

After this repository is pushed to GitHub, users can add it as a Codex plugin marketplace:

```bash
codex plugin marketplace add https://github.com/<your-user-or-org>/<repo>.git --sparse .agents/plugins
```

Then restart Codex, open Plugins, and install:

```text
AI Research Companion
```

## Install from a local clone

```bash
git clone https://github.com/<your-user-or-org>/<repo>.git
cd <repo>
codex plugin marketplace add .
```

Then restart Codex and install `AI Research Companion` from the plugin directory.

## Use

After installation, start a new Codex thread and ask naturally:

```text
I have a research idea. Help me judge whether it is worth testing.
```

or invoke one of the bundled skills explicitly:

```text
$research-mentor strictly evaluate this idea.
$literature-research survey related papers, code, and baselines.
$progress-review review current project status and blockers.
```

## Bundled skills

- `project-onboarding`
- `literature-research`
- `research-mentor`
- `idea-judge`
- `experiment-memory-scout`
- `progress-review`
- `weekly-review`
- `context-companion`

## Repository contents

```text
.agents/plugins/marketplace.json
plugins/ai-research-companion/.codex-plugin/plugin.json
plugins/ai-research-companion/skills/
```

Do not add private project files such as `.research/`, `experiments/`, `journal/`, `references/`, or local data to this repository.

