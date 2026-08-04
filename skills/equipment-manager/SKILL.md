---
name: equipment-manager
description: 管理本地已装第三方 Claude skill 与 agent 的盘点、评估、精简、接入时用本技能：想盘点自己装了哪些 skill/agent、各来自哪个仓库？某仓库 git pull 或 clone 后，想评估新增的 skill/agent 值不值得装？想从某仓库装 skill/agent 到 my-skills、~/.claude/skills 或 ~/.claude/agents？想删掉/清理用不上的旧装备、查重去重？本技能先盘点、列清单给选项，你拍板才动手，不擅自改文件。已接入 msitarzewski/agency-agents、wshobson/agents、mattpocock/skills，新仓库可随时接入。注意：本技能只管理『skill/agent 装备本身』，不处理改代码、优化性能、写文档、数据处理等普通开发任务。
version: v1.2.0
---

# 装备管理器（Equipment Manager）

管理从第三方仓库安装的 skill 与 agent，全程用**对话式流程**推进：一次一问、给选项、你拍板、才动手。**方法论一份，各仓库专属情报按仓库归档在 `references/`**——加新仓库只需加一个档案文件，方法论不动。

## 使用时机

- 某仓库 `git pull` 后有新增/变更的 skill 或 agent，需评估是否安装
- 从某仓库安装新 skill/agent
- 精简/删除某仓库已装的装备
- 盘点本地已装的 skill/agent 及其来源

## 支持的仓库

| 档案 | 仓库 | 内容 |
|------|------|------|
| `references/msitarzewski.md` | msitarzewski/agency-agents | agent 按 domain 分目录，install.sh 清单安装 |
| `references/wshobson.md` | wshobson/agents（Marketplace） | plugins 多域结构，符号链接惯例 |
| `references/mattpocock.md` | mattpocock/skills | 按 domain 分目录，link-skills.sh |

## 接入新仓库

当用户说「我新 clone 了 XX 仓库」「想接入 XX 仓库」、或提出一个新的 skill/agent 来源时：

1. **确认来源**：`git -C <仓库路径> remote -v`
2. **摸清结构**：目录结构、命名约定、安装机制（复制 vs 符号链接）
3. **建档案**：在 `references/` 下新建档案文件（按作者或仓库名命名，仿照现有三个档案的格式：基本信息/目录结构/安装机制/坑位/已知实践）
4. **登记**：在上表加一行
5. **更新 description**：把新仓库加入 frontmatter `description` 的「已接入」列表（保持触发精准）

通用内核不动——仓库差异全走档案，加仓库 = 建档案 + 表格一行 + description 补一个名字。

## 对话式流程

装备管理是一场对话，不是一份报告。核心节奏：**一次一问 → 给 2-3 个选项 → 你选 → 确认 → 下一步**。每个岔路口停下来等你拍板，不一口气甩结论。

### 硬闸门
在对话对齐并获得你明确批准之前，**不安装、不删除、不改动任何文件**。对话本身是安全的——只有你说"装/删"之后才动手。

### 阶段一：对齐场景（开场必问）
别一上来就盘点或查仓库。先问一句你要干嘛，给选项：
- **A 盘点**：本地装了什么、各来自哪个仓库
- **B 评估**：某仓库 git pull/clone 后新增了啥，值不值得装
- **C 安装**：从某仓库装某个 skill/agent
- **D 精简**：清理用不上的旧装备

选完再走对应分支；B/C/D 先确认是哪个仓库、意图是什么，再深入。

### 阶段二：澄清（一次一问）
一次只问一个，问到 95% 确定理解需求为止；优先给多选，开放回答也行。涉及删除，先复述你理解的清单让你确认，再继续。

### 阶段三：摸底与查重（结果说人话）
- 盘点本地：`ls ~/.claude/skills/`、`~/.claude/agents/`、`~/.claude/plugins/`，`ls -la` 识别软链来源，区分用户级/项目级
- 识别增量：`git -C <repo> log --diff-filter=A --name-only --since="90 days"`，对照 `references/<仓库>.md` 档案区分新增与早已装，只评估新增
- 查重：先看本地已装，同源项跳过，不重复推荐

**输出必须用大白话**：什么是什么、哪来的。术语要翻译（in-progress=未完工、软链=跟着仓库更新自动传播、ticket=拆出的任务条），不许甩黑话。

### 阶段四：给方案（每个决策点 2-3 个选项）
每个决策点给 2-3 个选项带利弊，**先说我的推荐**，你选：
- **装不装**：值得装 / 待定 / 不装，各给一句理由
- **安装方式**（须你拍板）：软链（仓库更新自动传播，省磁盘，但仓库路径变动会断链）vs 复制（独立稳定，但更新需手动重装）；默认推荐软链，听你的
- **删不删**：给三档清单（保留/待定/删）+ 理由，等你确认

### 阶段五：批准与执行
你说"装/删"之后才动手：
1. 覆盖/删除前先备份：`mkdir -p ~/.claude/backups/<日期>` + `cp`，不用 `mv xxx.bak`
2. 按你选的安装方式执行（软链 `ln -s` / 复制 `cp -r`，官方脚本有软链选项优先用官方参数，具体见对应仓库档案）
3. 验证：文件存在且非空；软链 `readlink` 确认目标存在、目标目录有 `SKILL.md`

### 接入新仓库（同样对话式）
用户说"接入新仓库"时，走阶段一 B/C 分支，确认仓库路径后依次确认：来源（`git remote -v`）→ 结构（目录/命名/安装机制）→ 建档案（`references/` 下按作者或仓库名新建，仿现有三个档案）→ 登记表格 → 更新 frontmatter description。**每一步都先确认再做下一步**，不一口气全做。
