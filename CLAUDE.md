# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Claude Code 自定义技能插件，只含八个自研技能（第三方技能已迁出，各自独立安装，见 README 部署备忘录）。通过 `.claude-plugin/plugin.json` 声明为可安装插件，技能定义在 `skills/<name>/SKILL.md`。

## 技能架构

每个技能是一个 `skills/<name>/` 目录，核心是 `SKILL.md`（YAML frontmatter + Markdown 指令）。部分技能带有 `scripts/` 下的 Python 辅助脚本，均不依赖第三方库。

- **obsidian-icon-assigner**：脚本技能，SKILL.md 指导 Claude 调用 Python 脚本操作 Obsidian Iconic 插件的 `data.json`，基于 SHA256 确定性分配图标和 HSL 颜色
- **opencode-model-optimizer**：纯指令技能，无脚本，Claude 依据 SKILL.md 中的规则为用户推荐 OpenCode Go 或同类平台的模型分层配置方案
- **playlist-organizer**：访谈 + 脚本技能，先确认歌曲来源、分类场景、覆盖/重复规则和输出位置，再调用 `scripts/build_playlists.py` 生成多个导入友好的 txt 歌单和 `生成报告.txt`
- **release-skills**：纯指令技能，无脚本，Claude 依据 SKILL.md 中的规则执行通用发布工作流，支持多语言 changelog
- **update-version**：纯指令技能，无脚本，Claude 依据 SKILL.md 中的规则直接执行 git diff 分析和文件写入
- **weekly-report**：纯指令技能，无脚本，Claude 依据 SKILL.md 中的规则执行 git log 并归纳周报
- **equipment-manager**：纯指令方法论技能，管理多个第三方 skill/agent 仓库的安装/筛选/精简；通用七步流程（盘点→查重→三档筛选→提问→备份安装→验证）+ `references/` 下按作者归档专属情报（msitarzewski / wshobson / mattpocock）；评估时消费 persona 的用户画像
- **persona**：脚本 + 方法论技能，从 Claude Code session 日志自学习用户画像——miner（`scripts/profile_miner.py`）举证 + 置信度/衰减/纠正 + 用户确认；画像分人工层（`profile.md`）与自学习层（`profile.d/<hostname>.md` 技术栈/工作流供评估 + `profile.d/prefs/<hostname>.md` 个人习惯仅备忘，每机一个文件、多机 git pull 零冲突）；供 equipment-manager 评估等场景消费

### evals

每个技能在 `skills/<name>/evals/evals.json` 定义测试用例（prompt + expected_output），用于评估技能质量。目前没有自动化测试运行器。

## 关键约定

- SKILL.md frontmatter 的 `description` 字段决定技能何时被触发，需精确描述触发场景
- 修改任何自研技能时，同步更新该技能 SKILL.md frontmatter 顶部的 `version` 字段（仅本仓库自研技能，第三方技能不动）；版本号递增幅度与改动匹配，酌情处理：小改动递增修订号（v1.0.0 → v1.0.1），功能/结构调整递增次版本（v1.0 → v1.1），破坏性变更递增主版本（v1.x → v2.0）
- 脚本路径使用 `${CLAUDE_PLUGIN_ROOT}` 环境变量，不硬编码路径
- 所有技能面向中文用户，SKILL.md 和输出均为中文
- `update-version` 依赖 `humanizer-zh` 技能优化文本
- 第三方技能（mattpocock 精选、baoyu-design、hallmark、storage-analyzer）已迁出，位于 `~/.claude/skills/` 各独立目录，不在本仓库维护
- 插件名称在 `.claude-plugin/plugin.json` 中定义，安装后技能命名空间为 `my-skills:<skill-name>`
