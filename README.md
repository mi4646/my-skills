# My Skills

个人自研技能集合。**本仓库只含自研技能**；第三方技能由 `install.sh` 一键安装，来源一目了然、更新互不影响。

## 技能列表（自研 7 个）

### [equipment-manager](./skills/equipment-manager)
管理从第三方仓库安装的 skill/agent——对话式流程：盘点 → 查重 → 三档筛选 → 备份安装 → 验证。

### [obsidian-icon-assigner](./skills/obsidian-icon-assigner)
为 Obsidian 知识库的 Markdown 文档自动分配 Iconic 插件的图标和颜色。

- 目录级颜色继承，文件级图标尽量唯一
- 基于 SHA256 哈希的确定性映射，同一文件路径始终获得相同结果
- 300+ Lucide 图标，中文关键词优先匹配

### [opencode-model-optimizer](./skills/opencode-model-optimizer)
为 OpenCode Go 等平台的 Claude Code 模型层级提供分层配置推荐。

- 先问后答：了解场景、预算、配额后才给方案
- 支持分层配置、成本最优、配额友好等推荐模式

### [playlist-organizer](./skills/playlist-organizer)
将音乐收藏、歌单链接、本地 txt/csv 整理成自定义场景歌单。

- 先访谈确认分类场景、覆盖规则、重复归属
- 内置 Python 脚本生成导入友好的 txt 歌单和报告

### [release-skills](./skills/release-skills)
通用发布工作流，支持多语言 changelog，自动检测版本文件和发布策略。

### [update-version](./skills/update-version)
根据 git diff 差异自动更新版本号。

### [weekly-report](./skills/weekly-report)
根据 git commit 历史归纳本周/上周工作成果，生成结构化开发周报。

---

## 安装

```bash
git clone https://github.com/mi4646/my-skills.git ~/.claude/skills/my-skills
bash ~/.claude/skills/my-skills/install.sh   # 一键装好第三方技能
```

重启 Claude Code（或 `/reload-plugins`）生效。默认全平台复制安装——软链指向 `~/skills/` 源目录，误删该目录会断链，故一律复制，不依赖软链；升级跑 `install.sh --update`（`git pull` + 强制重新复制）。

---

## 三方装备（install.sh 安装）

第三方技能、agents、插件由 `install.sh` 一键安装，来源独立、更新互不影响。实时清单用 `bash install.sh --list` 查看。

### Skills

- **mattpocock** — 插件，mattpocock/skills 精选 10 个技能，命名空间 `mattpocock:`，来源 `github.com/mattpocock/skills`
- **baoyu-design** — 技能 + 内置子技能/agents，前端与设计原型，除主技能外内置 50 余个流程子技能与 3 个只读子代理，来源 `github.com/jimliu/baoyu-design`
- **hallmark** — 纯技能，反 AI 味的网页设计指导，来源 `github.com/nutlope/hallmark`
- **storage-analyzer** — 技能 + Python 脚本，存储空间分析，来源 `github.com/KKKKhazix/khazix-skills`

### Agents

仅 baoyu-design 自带 3 个只读子代理，由主流程内部 spawn，**无全局调用命令**：

- **vision-probe-agent** — 任务前探测当前模型/提供商是否支持图像输入
- **fork-verifier-agent** — 校验刚生成的设计交付物，回报 `done` / `needs_work`
- **design-system-checker** — 只读校验便携设计系统，输出一行健康摘要

### Plugins

仅 mattpocock 是插件（`.claude-plugin/plugin.json` 声明），其余为独立技能目录。

---

## 使用方式

### 自研技能（`my-skills:` 前缀）

```
/my-skills:obsidian-icon-assigner
/my-skills:opencode-model-optimizer
/my-skills:playlist-organizer
/my-skills:release-skills
/my-skills:update-version
/my-skills:weekly-report
/my-skills:equipment-manager
```

### mattpocock 精选（`mattpocock:` 前缀）

```
/mattpocock:obsidian-vault
/mattpocock:edit-article
/mattpocock:git-guardrails-claude-code
/mattpocock:grill-with-docs
/mattpocock:domain-modeling
/mattpocock:handoff
/mattpocock:grill-me
/mattpocock:prototype
/mattpocock:research
/mattpocock:resolving-merge-conflicts
```

### 独立第三方（无前缀）

```
/baoyu-design   /hallmark   /storage-analyzer
```

### 提示词中指定技能

```text
请使用 my-skills:obsidian-icon-assigner 为我的知识库分配图标
请使用 my-skills:opencode-model-optimizer 推荐模型配置方案
请使用 my-skills:release-skills 发布新版本
请使用 my-skills:update-version 更新版本号
请使用 my-skills:weekly-report 生成本周周报
请使用 mattpocock:grill-with-docs 拷问并沉淀这个计划的 ADR
请使用 baoyu-design 设计一个登录页面原型
```
