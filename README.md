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

## 安装

```bash
git clone https://github.com/mi4646/my-skills.git ~/.claude/skills/my-skills
bash ~/.claude/skills/my-skills/install.sh
```

升级 `bash install.sh --update`（git pull + 强制重新复制）｜清单 `bash install.sh --list`。
重启 Claude Code（或 /reload-plugins）生效。（复制安装不依赖软链，误删 ~/skills 不中断）

## 技能索引

每个技能的完整工作流见其目录的 SKILL.md；一句话用途与触发命令见「速览」总表。
（技能索引区为未来扩展位——截图、示例、更新记录可挂在各 H3 下。）

### equipment-manager → [skills/equipment-manager/](./skills/equipment-manager/)
### obsidian-icon-assigner → [skills/obsidian-icon-assigner/](./skills/obsidian-icon-assigner/)
### opencode-model-optimizer → [skills/opencode-model-optimizer/](./skills/opencode-model-optimizer/)
### playlist-organizer → [skills/playlist-organizer/](./skills/playlist-organizer/)
### release-skills → [skills/release-skills/](./skills/release-skills/)
### update-version → [skills/update-version/](./skills/update-version/)
### weekly-report → [skills/weekly-report/](./skills/weekly-report/)

## 三方装备

mattpocock、baoyu-design、hallmark、storage-analyzer 由 install.sh 一键安装，来源独立、更新互不影响。
构成、来源、维护与全部调用命令（`/mattpocock:*`、`/baoyu-design`、`/hallmark`、`/storage-analyzer`）见 [THIRD-PARTY.md](./THIRD-PARTY.md)。
