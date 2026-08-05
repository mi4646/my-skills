# My Skills

个人自研技能集合：7 个自研技能 + install.sh 一键安装第三方技能。
第三方装备来源独立、更新互不影响（构成与调用见文末「三方装备」）。

## 速览（30 秒）

| 技能 | 用途 | 触发 |
|------|------|------|
| equipment-manager | 管理第三方安装的 skill/agent：盘点→查重→三档筛选→备份安装→验证 | /my-skills:equipment-manager |
| obsidian-icon-assigner | 为 Obsidian Markdown 分配 Iconic 图标与颜色 | /my-skills:obsidian-icon-assigner |
| opencode-model-optimizer | 推荐 OpenCode Go 模型分层配置 | /my-skills:opencode-model-optimizer |
| playlist-organizer | 音乐收藏整理成场景歌单 | /my-skills:playlist-organizer |
| release-skills | 通用发布工作流，多语言 changelog | /my-skills:release-skills |
| update-version | 依 git diff 自动更新版本号 | /my-skills:update-version |
| weekly-report | 依 git commit 归纳周报 | /my-skills:weekly-report |

## 技能详解

一行速览见上表，以下为完整介绍；完整工作流见各技能目录的 SKILL.md。

### equipment-manager

管理从第三方仓库安装的 skill/agent——对话式流程：盘点 → 查重 → 三档筛选 → 备份安装 → 验证。

触发 `/my-skills:equipment-manager` · 目录 [skills/equipment-manager/](./skills/equipment-manager/)

### obsidian-icon-assigner

为 Obsidian 知识库的 Markdown 文档自动分配 Iconic 插件的图标和颜色。

- 目录级颜色继承，文件级图标尽量唯一
- 基于 SHA256 哈希的确定性映射，同一文件路径始终获得相同结果
- 300+ Lucide 图标，中文关键词优先匹配

触发 `/my-skills:obsidian-icon-assigner` · 目录 [skills/obsidian-icon-assigner/](./skills/obsidian-icon-assigner/)

### opencode-model-optimizer

为 OpenCode Go 等平台的 Claude Code 模型层级提供分层配置推荐。

- 先问后答：了解场景、预算、配额后才给方案
- 支持分层配置、成本最优、配额友好等推荐模式

触发 `/my-skills:opencode-model-optimizer` · 目录 [skills/opencode-model-optimizer/](./skills/opencode-model-optimizer/)

### playlist-organizer

将音乐收藏、歌单链接、本地 txt/csv 整理成自定义场景歌单。

- 先访谈确认分类场景、覆盖规则、重复归属
- 内置 Python 脚本生成导入友好的 txt 歌单和报告

触发 `/my-skills:playlist-organizer` · 目录 [skills/playlist-organizer/](./skills/playlist-organizer/)

### release-skills

通用发布工作流，支持多语言 changelog，自动检测版本文件和发布策略。

触发 `/my-skills:release-skills` · 目录 [skills/release-skills/](./skills/release-skills/)

### update-version

根据 git diff 差异自动更新版本号。

触发 `/my-skills:update-version` · 目录 [skills/update-version/](./skills/update-version/)

### weekly-report

根据 git commit 历史归纳本周/上周工作成果，生成结构化开发周报。

触发 `/my-skills:weekly-report` · 目录 [skills/weekly-report/](./skills/weekly-report/)

## 安装

```bash
git clone https://github.com/mi4646/my-skills.git ~/.claude/skills/my-skills
bash ~/.claude/skills/my-skills/install.sh   # 一键装好第三方技能
```

重启 Claude Code（或 `/reload-plugins`）生效。升级 `bash install.sh --update`（git pull + 强制重新复制）｜清单 `bash install.sh --list`。默认全平台复制安装、不依赖软链（误删 ~/skills 不中断）。

## 三方装备

mattpocock、baoyu-design、hallmark、storage-analyzer 由 install.sh 一键安装，来源独立、更新互不影响。
构成、来源、维护与全部调用命令（`/mattpocock:*`、`/baoyu-design`、`/hallmark`、`/storage-analyzer`）见 [THIRD-PARTY.md](./THIRD-PARTY.md)。
