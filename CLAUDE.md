# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Claude Code 自定义技能插件，包含六个自研技能与三个第三方技能。通过 `.claude-plugin/plugin.json` 声明为可安装插件，技能定义在 `skills/<name>/SKILL.md`。

## 技能架构

每个技能是一个 `skills/<name>/` 目录，核心是 `SKILL.md`（YAML frontmatter + Markdown 指令）。部分技能带有 `scripts/` 下的 Python 辅助脚本，均不依赖第三方库。

- **obsidian-icon-assigner**：脚本技能，SKILL.md 指导 Claude 调用 Python 脚本操作 Obsidian Iconic 插件的 `data.json`，基于 SHA256 确定性分配图标和 HSL 颜色
- **opencode-model-optimizer**：纯指令技能，无脚本，Claude 依据 SKILL.md 中的规则为用户推荐 OpenCode Go 或同类平台的模型分层配置方案
- **playlist-organizer**：访谈 + 脚本技能，先确认歌曲来源、分类场景、覆盖/重复规则和输出位置，再调用 `scripts/build_playlists.py` 生成多个导入友好的 txt 歌单和 `生成报告.txt`
- **release-skills**：纯指令技能，无脚本，Claude 依据 SKILL.md 中的规则执行通用发布工作流，支持多语言 changelog
- **update-version**：纯指令技能，无脚本，Claude 依据 SKILL.md 中的规则直接执行 git diff 分析和文件写入
- **weekly-report**：纯指令技能，无脚本，Claude 依据 SKILL.md 中的规则执行 git log 并归纳周报
- **baoyu-design**：第三方全功能设计技能（来源 [jimliu/baoyu-design](https://github.com/jimliu/baoyu-design)），用 HTML 创建设计原型、交互原型、PPT 等设计产物，含 Figma 导入、设计系统管理等子技能
- **hallmark**：第三方设计技能，反 AI 设计风格，含 40+ 组件原型与 20+ 宏观结构参考，适用于新建页面、审计、改版和从 URL/截图提取设计 DNA
- **storage-analyzer**：第三方脚本技能（来源 [KKKKhazix/khazix-skills](https://github.com/KKKKhazix/khazix-skills/)），只读扫描磁盘占用并生成分级清理 HTML 报告

### evals

`evals/evals.json` 为每个技能定义测试用例（prompt + expected_output），用于评估技能质量。目前没有自动化测试运行器。

## 关键约定

- SKILL.md frontmatter 的 `description` 字段决定技能何时被触发，需精确描述触发场景
- 脚本路径使用 `${CLAUDE_PLUGIN_ROOT}` 环境变量，不硬编码路径
- 所有技能面向中文用户，SKILL.md 和输出均为中文
- `update-version` 依赖 `humanizer-zh` 技能优化文本
- 插件名称在 `.claude-plugin/plugin.json` 中定义，安装后技能命名空间为 `my-skills:<skill-name>`
