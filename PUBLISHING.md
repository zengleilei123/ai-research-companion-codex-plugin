# Publishing

Use this checklist to publish the plugin without leaking project-specific state.

## What to include

- `.agents/plugins/marketplace.json`
- `plugins/ai-research-companion/.codex-plugin/plugin.json`
- `plugins/ai-research-companion/skills/**`
- `README.md`
- `PUBLISHING.md`
- `.gitignore`

## What not to include

- `.research/`
- `journal/`
- `experiments/`
- `knowledge/`
- `references/`
- `templates/`
- `bin/`
- personal notes
- local database files
- logs
- secrets
- generated caches

## Create and push the GitHub repo

From this directory:

```bash
git init
git add README.md PUBLISHING.md .gitignore .agents plugins
git commit -m "feat: publish AI Research Companion Codex plugin"
git branch -M main
git remote add origin git@github.com:<your-user-or-org>/<repo>.git
git push -u origin main
```

For HTTPS remotes:

```bash
git remote add origin https://github.com/<your-user-or-org>/<repo>.git
git push -u origin main
```

## User installation command

After publishing:

```bash
codex plugin marketplace add https://github.com/<your-user-or-org>/<repo>.git --sparse .agents/plugins
```

