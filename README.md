# My Skills

Claude Code 自定义技能插件。

## 技能列表

### [obsidian-icon-assigner](./skills/obsidian-icon-assigner)

为 Obsidian 知识库的 Markdown 文档自动分配 Iconic 插件的图标和颜色。

- 目录级颜色继承，文件级图标尽量唯一
- 支持增量更新、试运行、强制重新分配
- 基于 SHA256 哈希的确定性映射，同一文件路径始终获得相同结果
- 300+ Lucide 图标支持

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
/obsidian-icon-assigner
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
│   ├── obsidian-icon-assigner/
│   │   ├── SKILL.md
│   │   ├── evals/
│   │   ├── references/
│   │   └── scripts/
│   ├── update-version/
│   │   └── SKILL.md
│   └── weekly-report/
│       ├── SKILL.md
│       └── evals/
└── README.md
```
