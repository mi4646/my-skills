# My Skills

Claude Code 自定义技能插件。

## 技能列表

### [neat-freak](./skills/neat-freak)

会话末对项目文档（CLAUDE.md / README.md / docs/）和 agent 记忆进行洁癖级同步与规范执行审计。

- 三类知识（agent 记忆 / 项目根 CLAUDE.md / docs）分层同步，记忆「毕业」机制防止膨胀
- 审计工作空间规范的执行：命名约定、必备文件、CLAUDE.md 与 AGENTS.md 软链同源、规则文件死引用
- 跨平台兼容 Claude Code / OpenAI Codex / OpenCode / OpenClaw
- 第三方技能，来源：[KKKKhazix/khazix-skills](https://github.com/KKKKhazix/khazix-skills/tree/main/neat-freak)

### [obsidian-icon-assigner](./skills/obsidian-icon-assigner)

为 Obsidian 知识库的 Markdown 文档自动分配 Iconic 插件的图标和颜色。

- 目录级颜色继承，文件级图标尽量唯一
- 支持增量更新、试运行、强制重新分配
- 基于 SHA256 哈希的确定性映射，同一文件路径始终获得相同结果
- 300+ Lucide 图标支持

### [playlist-organizer](./skills/playlist-organizer)

将音乐收藏、歌单链接解析结果、本地 txt/csv 歌曲列表整理成自定义场景歌单。

- 先访谈确认分类场景、覆盖规则、重复归属和不确定歌曲处理方式
- 支持本地 txt/csv、复制文本，以及 GoMusic 风格的“链接先转歌曲清单”工作流
- 内置 Python 脚本生成多个导入友好的 txt 歌单和 `生成报告.txt`

### [storage-analyzer](./skills/storage-analyzer)

只读扫描 macOS / Windows 磁盘占用，生成分级清理建议和交互式 HTML 报告。

- 自动识别系统，扫描常见用户目录、缓存目录、下载目录和开发缓存
- 将占用项分为 🟢可自动清理 / 🟡需人工判断 / 🔴谨慎清理 三级
- 生成可折叠、命令可复制的 HTML 报告；可选本地服务模式提供移到废纸篓/打开目录操作
- 第三方技能，来源：[KKKKhazix/khazix-skills](https://github.com/KKKKhazix/khazix-skills/)

### [update-version](./skills/update-version)

根据 git diff 差异自动更新版本号到 `update_info.txt` 和 `version` 文件。

- 自动根据修改规模判断版本号递增（小改/大修/破坏性变更）
- `update_info.txt` 仅保留最新版本，`version` 文件追加保留完整历史
- 集成 `humanizer-zh` 优化更新描述

### [weekly-report](./skills/weekly-report)

根据 git commit 历史归纳本周/上周的工作成果，生成结构化开发周报。

- 自动确定 commit 区间（支持指定区间、时间范围或默认上周）
- 智能过滤与归纳，合并相关提交为完整工作成果
- 输出 3~6 条精炼周报条目

## 安装

将仓库克隆到 Claude Code 的用户技能目录，启动时自动发现：

```bash
git clone https://github.com/mi4646/my-skills.git ~/.claude/skills/my-skills
```

## 使用方式

安装后，在 Claude Code 中通过技能名称调用：

```
/neat-freak
/obsidian-icon-assigner
/playlist-organizer
/storage-analyzer
/update-version
/weekly-report
```

或使用带插件命名空间的完整命令：

```
/my-skills:obsidian-icon-assigner
/my-skills:update-version
/my-skills:weekly-report
```

或在提示词中指定技能名称：

```
请使用 my-skills:obsidian-icon-assigner 为我的知识库分配图标
请使用 my-skills:update-version 更新版本号
请使用 my-skills:weekly-report 生成本周周报
```

## 项目结构

```
my-skills/
├── .claude-plugin/
│   └── plugin.json           # 插件清单
├── skills/
│   ├── neat-freak/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── obsidian-icon-assigner/
│   │   ├── SKILL.md
│   │   ├── evals/
│   │   ├── references/
│   │   └── scripts/
│   ├── playlist-organizer/
│   │   ├── SKILL.md
│   │   ├── evals/
│   │   └── scripts/
│   ├── storage-analyzer/
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   ├── references/
│   │   └── scripts/
│   ├── update-version/
│   │   └── SKILL.md
│   └── weekly-report/
│       ├── SKILL.md
│       └── evals/
└── README.md
```
