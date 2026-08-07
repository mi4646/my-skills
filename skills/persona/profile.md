# 用户画像（使用习惯）

供 equipment-manager 评估装备时判断「用不用得上」的权威依据。**稳定个人情报，进 git，随 my-skills 三机部署同步**——新设备跑 install.sh 即自动带上。

## 分层

- **人工层（本文件）**：稳定的结构性事实 + 用户明确表态，手工维护
- **自学习层**：miner 从本机日志挖掘、用户确认的偏好，见 `profile.d/<hostname>.md`——**每机一个文件，miner 只写本机自己的 → 三机各写各的，`git pull` 零冲突**

- **updated**: 2026-08-07
- **证据来源分级**：🧠记忆记录 / 🔍环境扫描实测（`scripts/scan_profile.sh`）/ 🔍日志挖掘（`scripts/profile_miner.py`，写入 profile.d/）/ 🗣用户口述 / ⚠️推断。单一口述不落地，实测与记忆交叉验证后才写死

## 工作流（人工层）

- **skill/agent 装备工程化与评测**：写/改 skill、评测触发机制（benchmark、claude -p 实测）、触发词优化 🧠
- **装备管理与跨仓库评估**：equipment-manager 盘点/评估/精简 🔍（~/.config/equipment-manager/ 台账 + references 三档案在案）
- **多机部署**：my-skills 为部署入口（install.sh 复制模式）+ dotfiles 仓库（mi4646/dotfiles）同步配置 🔍

## 技术栈（人工层 · 环境配置）

- 多语言运行时已装但非活跃：.nvm/.bun/.dotnet 🔍
- **四层模型栈已实锤落地**：qwen3.7-max(旗舰/Opus)+deepseek-v4-pro(主力/Sonnet)+qwen3.7-plus(轻量/Fable)+deepseek-v4-flash(兜底/Haiku) 🔍（~/.claude/settings.json 实测，Fable 槽位 2026-08-07 确认；与 OpenCode 记忆同源）
- *自学习层证据条目（Python 后端 FastAPI+Django、/var/www 业务项目等）见 `profile.d/<hostname>.md`*

## 常用场景（人工层）

- 写 skill / agent 文档（SKILL.md、AGENTS.md、CLAUDE.md）🧠
- 评测 skill 触发机制与质量 🧠
- 装备查重、精简、跨仓库评估 🧠
- 部署脚本与跨机同步（install.sh + dotfiles）🔍

## 明确不用的领域（暂无——2026-08-06 全量清除推断）

无。**负面偏好不推断**，只有用户明确表态「用不上 X」才记录（标记 🗣）。domain-modeling/prototype/wizard 类不再被"明确不用"排除，下次评估以 miner 实证为准。

## 更新方式

- **miner 举证（自学习层）**：评估前跑 `profile_miner.py --evaluate` 产出候选条目，你确认 → 写入 `profile.d/<hostname>.md`（本机文件，不碰本文件）；纠正 → `--correct <关键词>` 降权
- **人工层**：工作流/技术栈结构变化时直接编辑本文件 + 更新 `updated` 时间戳 + commit
- 任何变更 commit 后三机 `git pull`
