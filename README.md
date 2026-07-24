# My Skills

Claude Code 自定义技能插件。

## 技能列表

### [baoyu-design](./skills/baoyu-design)

创建精美的设计产物为自包含 HTML：UI 原型、交互原型、线框图、落地页、仪表盘、App 界面、幻灯片（PPT）以及视觉探索。

- 支持线框图、高保真设计、交互原型、移动端原型、PPT/幻灯片、动画视频等丰富产出形式
- 内置设计系统管理、Figma 导入、设计审查等完整设计工作流
- 可导出为 PDF、PPTX（可编辑版或截图版）、视频（MP4）
- 跨平台兼容 Claude Code / Cursor / Codex Agent
- **第三方技能**，来源：[jimliu/baoyu-design](https://github.com/jimliu/baoyu-design)

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

### [release-skills](./skills/release-skills)

通用发布工作流，支持多语言变更日志，自动检测版本文件和 changelog。

- 支持 Node.js、Python、Rust、Claude Plugin、GitHub Releases、annotated tags
- 自动检测项目类型并选择合适的版本文件与发布策略
- 支持历史发布回填、通用项目发布
- 可自定义：Release URL 模板、版本文件、变更日志路径

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
/baoyu-design
/hallmark
/obsidian-icon-assigner
/opencode-model-optimizer
/playlist-organizer
/release-skills
/storage-analyzer
/update-version
/weekly-report
```

或使用带插件命名空间的完整命令：

```
/my-skills:baoyu-design
/my-skills:hallmark
/my-skills:obsidian-icon-assigner
/my-skills:opencode-model-optimizer
/my-skills:release-skills
/my-skills:update-version
/my-skills:weekly-report
```

或在提示词中指定技能名称：

```
请使用 my-skills:baoyu-design 设计一个登录页面原型
请使用 my-skills:hallmark 设计一个反 AI 模板化的页面
请使用 my-skills:obsidian-icon-assigner 为我的知识库分配图标
请使用 my-skills:opencode-model-optimizer 推荐模型配置方案
请使用 my-skills:release-skills 发布新版本
请使用 my-skills:update-version 更新版本号
请使用 my-skills:weekly-report 生成本周周报
```
