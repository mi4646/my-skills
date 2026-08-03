# My Skills

Codex / Claude Code 自定义技能插件。

## 技能列表

### [baoyu-design](./skills/baoyu-design)

创建精美的设计产物为自包含 HTML：UI 原型、交互原型、线框图、落地页、仪表盘、App 界面、幻灯片（PPT）以及视觉探索。

- 支持线框图、高保真设计、交互原型、移动端原型、PPT/幻灯片、动画视频等丰富产出形式
- 内置设计系统管理、Figma 导入、设计审查等完整设计工作流
- 可导出为 PDF、PPTX（可编辑版或截图版）、视频（MP4）
- 跨平台兼容 Claude Code / Cursor / Codex Agent
- **第三方技能**，来源：[jimliu/baoyu-design](https://github.com/jimliu/baoyu-design)

### [grill-me](./skills/grill-me)

无代码库的无状态审讯——一次一个问题磨你的计划/决定，直到共享理解达成，不保存任何东西。

- 每问附推荐答案，能查的事实绝不问你，决策才归你
- 无状态：不建 `CONTEXT.md`，不留痕
- 没有代码库时磨想法/决定的入口
- **第三方技能**，来源：[mattpocock/skills](https://github.com/mattpocock/skills)

### [hallmark](./skills/hallmark)

反 AI 设计技能，适用于新建页面、设计审计、改版和从 URL/截图提取设计 DNA。

- 20+ 宏观结构（Bento Grid、Manifesto、Long Document 等）+ 50+ 组件原型（导航、Hero、Feature、CTA 等）
- 内置 slop-test 质量门与多样化轮换机制，防止 AI 模板化输出
- 支持 `audit`（审计）、`study`（研习）、`redesign`（改版）三种设计动词
- 跨平台兼容 Claude Code / Cursor / Codex Agent
- **第三方技能**，由 Together AI 驱动

### [obsidian-icon-assigner](./skills/obsidian-icon-assigner)

为 Obsidian 知识库的 Markdown 文档自动分配 Iconic 插件的图标和颜色。

- 目录级颜色继承，文件级图标尽量唯一
- 支持增量更新、试运行、强制重新分配
- 基于 SHA256 哈希的确定性映射，同一文件路径始终获得相同结果
- 300+ Lucide 图标支持
- 中文关键词优先匹配（按长度降序），场景化覆盖更精准

### [opencode-model-optimizer](./skills/opencode-model-optimizer)

为 OpenCode Go 或类似多模型平台的 Claude Code 模型层级（Sonnet/Opus/Fable/Haiku）提供分层配置推荐。

- 先问后答：必须了解用户场景、预算、配额后才给出推荐方案
- 支持分层配置、成本最优、配额友好等多种推荐模式
- 推荐模式含数据来源引用，透明可追溯

### [playlist-organizer](./skills/playlist-organizer)

将音乐收藏、歌单链接解析结果、本地 txt/csv 歌曲列表整理成自定义场景歌单。

- 先访谈确认分类场景、覆盖规则、重复归属和不确定歌曲处理方式
- 支持本地 txt/csv、复制文本，以及 GoMusic 风格的“链接先转歌曲清单”工作流
- 内置 Python 脚本生成多个导入友好的 txt 歌单和 `生成报告.txt`

### [prototype](./skills/prototype)

一次性原型回答设计问题——逻辑/状态机用可交互终端小应用，UI 用同一路由的多种可切换变体。

- 逻辑分支 → 可交互终端应用；UI 分支 → 多种 UI 变体切换
- 用完即弃：答案留档到一次性分支，主分支只保留验证过的决策
- 纸面上定不下来的状态机、业务逻辑、界面观感时触发
- **第三方技能**，来源：[mattpocock/skills](https://github.com/mattpocock/skills)

### [release-skills](./skills/release-skills)

通用发布工作流，支持多语言变更日志，自动检测版本文件和 changelog。

- 支持 Node.js、Python、Rust、Claude Plugin、GitHub Releases、annotated tags
- 自动检测项目类型并选择合适的版本文件与发布策略
- 支持历史发布回填、通用项目发布
- 可自定义：Release URL 模板、版本文件、变更日志路径

### [research](./skills/research)

派后台 agent 调研一手资料——只查高可信一手来源，每个论断溯源，写带引用的 Markdown 笔记进仓库。

- 后台 agent 并行调研，主线程继续干活
- 只信官方文档、源码、规范，不取二手转述
- **第三方技能**，来源：[mattpocock/skills](https://github.com/mattpocock/skills)

### [resolving-merge-conflicts](./skills/resolving-merge-conflicts)

逐 hunk 解决合并冲突——找两侧一手来源理解原始意图，尽量保住双方意图，绝不 `--abort`。

- 每个冲突定位两侧提交/PR/issue 还原意图
- 冲突不可调和时按合并目标选择并说明代价
- 解决完跑项目自动化检查再完成合并
- **第三方技能**，来源：[mattpocock/skills](https://github.com/mattpocock/skills)

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

### Codex

```bash
git clone https://github.com/mi4646/my-skills.git ~/.codex/skills/my-skills
```

### Claude Code

```bash
git clone https://github.com/mi4646/my-skills.git ~/.claude/skills/my-skills
```

克隆后重启应用，技能自动发现。

## 使用方式

安装后，在 Claude Code 中通过技能名称调用：

```
/baoyu-design
/hallmark
/obsidian-icon-assigner
/opencode-model-optimizer
/playlist-organizer
/release-skills
/storage-analyzer
/update-version
/weekly-report
/grill-me
/prototype
/research
/resolving-merge-conflicts
```

或使用带插件命名空间的完整命令：

```
/my-skills:baoyu-design
/my-skills:hallmark
/my-skills:obsidian-icon-assigner
/my-skills:opencode-model-optimizer
/my-skills:playlist-organizer
/my-skills:release-skills
/my-skills:storage-analyzer
/my-skills:update-version
/my-skills:weekly-report
/my-skills:grill-me
/my-skills:prototype
/my-skills:research
/my-skills:resolving-merge-conflicts
```

或在提示词中指定技能名称：

```text
请使用 my-skills:baoyu-design 设计一个登录页面原型
请使用 my-skills:hallmark 设计一个反 AI 模板化的页面
请使用 my-skills:obsidian-icon-assigner 为我的知识库分配图标
请使用 my-skills:opencode-model-optimizer 推荐模型配置方案
请使用 my-skills:release-skills 发布新版本
请使用 my-skills:update-version 更新版本号
请使用 my-skills:weekly-report 生成本周周报
```

