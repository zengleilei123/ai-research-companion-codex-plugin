# AI Research Companion

AI Research Companion is an agent-native research workflow pack for Codex and Claude Code.
It is not a CLI app, server, or standalone product. It is a collection of `SKILL.md`
instructions that an agent can load while you work inside a research project.

- 中文说明见下方
- English guide below

Repository: https://github.com/zengleilei123/ai-research-companion-codex-plugin

## 中文说明

### 这个项目是什么

AI Research Companion 用来把一个 AI coding agent 变成更严格的科研伙伴。它强调：

- 新项目进入时先做项目设定和研究问题澄清
- 在评价 idea 前先检查已有实验、周报、文献和参考代码
- 用严格导师视角判断 idea taste、工程可行性、科研新颖性和 MVP 边界
- 每次重要对话后给出三个可选下一步
- 支持文献调研、参考代码库检索、进度检查、周报复盘和上下文交接

这个仓库只发布插件和 skills，不包含任何个人研究数据、实验记录、日志、参考论文库或私有 `.research` 文件。

### 适配方式

| 工具 | 推荐接入方式 | 调用方式 |
| --- | --- | --- |
| Codex App / Codex CLI | 安装为 Codex plugin | 自然语言触发，或用 `$ai-research-companion:research-mentor` 这类 skill 名 |
| Claude Code | 复制或链接到 `.claude/skills/` 或 `~/.claude/skills/` | 自然语言触发，或用 `/research-mentor` 这类 slash skill |
| 其他支持 Agent Skills 的工具 | 直接复用每个 `SKILL.md` | 取决于对应工具 |

### 在 Codex 中安装

把这个仓库加入 Codex plugin marketplace：

```bash
codex plugin marketplace add https://github.com/zengleilei123/ai-research-companion-codex-plugin.git --sparse .agents/plugins
```

然后重启 Codex，在 Plugins 中安装：

```text
AI Research Companion
```

安装后，在项目文件夹中打开 Codex，直接自然语言使用：

```text
我有一个新的研究想法，请先做 project onboarding，然后严格判断这个 idea 是否值得做 MVP。
```

也可以显式点名某个 skill：

```text
$ai-research-companion:research-mentor 严格评估这个 idea 的科研 taste、工程可行性和最小验证实验。
$ai-research-companion:literature-research 帮我找相关论文、baseline 和参考代码库。
$ai-research-companion:progress-review 检查当前项目进度、阻塞和上周实验证据。
```

### 在 Claude Code 中使用

Claude Code 可以直接读取 `SKILL.md`。你可以把本仓库的 skills 复制到当前项目：

```bash
git clone https://github.com/zengleilei123/ai-research-companion-codex-plugin.git .agent-libs/ai-research-companion
mkdir -p .claude/skills
cp -R .agent-libs/ai-research-companion/plugins/ai-research-companion/skills/* .claude/skills/
```

然后在项目根目录启动 Claude Code：

```bash
claude
```

自然语言触发：

```text
我准备开始一个新的研究项目。请先做项目设定，并检查是否需要补充论文库、代码库和实验记忆。
```

或显式调用：

```text
/project-onboarding
/research-mentor 严格评估这个 idea。
/literature-research 找相关论文、baseline 和代码实现。
/weekly-review 生成本周研究复盘。
```

如果你想让这些 skills 对所有项目可用，可以复制到个人 skills 目录：

```bash
mkdir -p ~/.claude/skills
cp -R plugins/ai-research-companion/skills/* ~/.claude/skills/
```

### 推荐工作流

1. 新项目启动：先让 agent 运行 `project-onboarding`，明确研究问题、假设、数据、baseline、MVP 和成功/失败标准。
2. idea 对话阶段：自然讨论时让 `idea-judge` 和 `research-mentor` 介入，避免只凭直觉推进。
3. 调研阶段：用 `literature-research` 补第三方论文、baseline、参考代码和 novelty risk。
4. 实验前：用 `experiment-memory-scout` 查已有实验、上周记录、相似失败和可复用证据。
5. 每周结束：用 `weekly-review` 输出 continue / park / reject / reframe 判断。
6. 切换上下文前：用 `context-companion` 保存当前状态和下一轮启动提示。

### 浏览器和互联网能力

这个仓库本身只提供研究工作流 skills。浏览网页、打开 Chrome、搜索论文、访问 GitHub 等能力来自你正在使用的宿主 agent：

- Codex App：安装或启用 Codex 的 Browser / Chrome / GitHub 等插件后，本插件的 skills 可以要求 agent 使用这些能力。
- Claude Code：使用 Claude Code 已配置的 web search、MCP、浏览器或本地工具。

也就是说，AI Research Companion 负责“什么时候该调研、怎么判断、如何组织证据”；具体能不能联网、能不能控制浏览器，取决于你的 Codex 或 Claude Code 环境。

### Bundled Skills

- `project-onboarding`: 新项目设定、研究目标澄清、项目配置
- `literature-research`: 论文、baseline、参考代码和 novelty risk 调研
- `research-mentor`: 严格导师视角，评估科研与工程可行性
- `idea-judge`: 将原始 idea 变成可证伪假设、MVP 和决策
- `experiment-memory-scout`: 实验前查找历史证据和重复风险
- `progress-review`: 检查进度、阻塞、实验状态和下一步
- `weekly-review`: 周报复盘，判断继续、暂停、拒绝或重构
- `context-companion`: 上下文压缩、交接和下一轮启动提示

### 仓库内容

```text
.agents/plugins/marketplace.json
plugins/ai-research-companion/.codex-plugin/plugin.json
plugins/ai-research-companion/skills/
```

不要把这些内容加入本仓库：

```text
.research/
experiments/
journal/
knowledge/
references/
templates/
bin/
logs/
secrets/
local databases
personal research notes
```

## English Guide

### What This Is

AI Research Companion turns an AI coding agent into a stricter research partner. It helps you:

- onboard a new research project before coding
- check prior experiments, weekly reviews, papers, and reference code before judging an idea
- evaluate idea taste, engineering feasibility, novelty risk, MVP scope, and failure criteria
- end important conversations with three concrete next-step options
- run literature scouting, code-reference scouting, progress reviews, weekly reviews, and context handoff

This repository is plugin-only. It intentionally excludes private project state, experiments, journals, paper libraries, reference repos, and `.research` files.

### Compatibility

| Tool | Recommended setup | Invocation |
| --- | --- | --- |
| Codex App / Codex CLI | Install as a Codex plugin | Natural language, or `$ai-research-companion:research-mentor` |
| Claude Code | Copy or symlink skills into `.claude/skills/` or `~/.claude/skills/` | Natural language, or `/research-mentor` |
| Other Agent Skills tools | Reuse each `SKILL.md` directly | Tool-specific |

### Install for Codex

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

### Use with Claude Code

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

### Suggested Workflow

1. Project start: run `project-onboarding` to define the research question, hypothesis, data, baselines, MVP, and success/failure criteria.
2. Idea discussion: let `idea-judge` and `research-mentor` intervene during natural conversation instead of waiting for a command.
3. Survey: use `literature-research` to collect third-party papers, baselines, code, and novelty risks.
4. Before experiments: use `experiment-memory-scout` to inspect old experiments, weekly notes, related failures, and reusable evidence.
5. End of week: run `weekly-review` and classify tracks as continue, park, reject, or reframe.
6. Before context switching: use `context-companion` to preserve state and write the next starting prompt.

### Browser and Internet Access

This repository only provides research workflow skills. Web browsing, Chrome control, paper search, and GitHub access come from the host agent:

- Codex App: enable Codex Browser / Chrome / GitHub plugins as needed. These skills can then ask the agent to use those capabilities.
- Claude Code: use the web search, MCP, browser, or local tools configured in your Claude Code environment.

AI Research Companion decides when and how to research, evaluate, and organize evidence. The actual network or browser capability depends on your Codex or Claude Code setup.

### Included Skills

- `project-onboarding`
- `literature-research`
- `research-mentor`
- `idea-judge`
- `experiment-memory-scout`
- `progress-review`
- `weekly-review`
- `context-companion`

### Repository Contents

```text
.agents/plugins/marketplace.json
plugins/ai-research-companion/.codex-plugin/plugin.json
plugins/ai-research-companion/skills/
```

Do not add private research files such as `.research/`, `experiments/`, `journal/`, `references/`, logs, secrets, generated caches, or local databases to this repository.
