# 接入方案：新第三方 skill 仓库（~/new-skill-repo）

> 按装备管理器方法论「接入新仓库」流程输出。**本方案只出方案、不执行**——仓库尚未 clone，且硬闸门要求：在对话确认并获得批准前，不建档案、不改 SKILL.md、不装任何东西。下文每一步都标注了"待确认后执行"的动作。

## 仓库性质预判

`~/new-skill-repo` 是 **agents 与 skills 混合**仓库。这与现有三个仓库都不同（msitarzewski 纯 agents、wshobson/mattpocock 以 skills 为主），所以档案里要**分别记录两类装备的目录与安装机制**，不能混为一谈。

---

## 五步接入流程

### 第 1 步：确认来源

仓库 clone 到位后执行（本机当前不存在，此步为待办占位）：

```bash
git -C ~/new-skill-repo remote -v
```

- 记录 remote URL（github/gitlab 等）与默认分支，写入档案「基本信息」。
- 目的：档案里写明来源，日后 git pull 评估增量、查软链指向时能对上号。

### 第 2 步：摸清结构

对 `~/new-skill-repo` 做一次只读摸底，重点四项：

1. **目录结构**：agents 与 skills 各在哪个目录（如 `agents/`、`skills/`，或混合在 `plugins/` 下），按 domain 分目录还是平铺。
2. **命名约定**：agent 是 `<domain>-<name>.md` 单文件，还是 skill 是 `skills/<name>/SKILL.md` 目录式；目录名与装备名是否可能不一致（wshobson 有前车之鉴：本地名 vs 仓库名不一致导致断链）。
3. **安装机制**：有无官方脚本（install.sh / link-skills.sh 之类）；无脚本时看仓库 README 的惯例是**符号链接**还是**复制**。agents 与 skills 的安装目标目录不同——agents 装到 `~/.claude/agents/`，skills 装到 `~/.claude/skills/`（或项目级 `.claude/`），要分别确认。
4. **副产物**：仓库里是否带 `agents/openai.yaml` 之类的面向其他宿主（Codex/OpenAI）的文件，Claude Code 会忽略但改动时要注意同步（mattpocock 档案已记录此坑）。

产出：摸清结果用大白话汇报（不甩黑话），并把结论落进档案。

### 第 3 步：建档案（references/ 下新建）

按作者或仓库名新建 `references/new-skill-repo.md`，**仿照现有三个档案的五段式**：

```markdown
# 仓库档案：<作者>/new-skill-repo

## 基本信息
- **本地路径**：`/home/anonymous/new-skill-repo`
- **git remote**：`<第 1 步确认的 URL>`

## 目录结构
- `agents/`：…（按 domain 分目录 / 平铺，命名约定）
- `skills/`：…（目录式 SKILL.md / 单文件）
- `scripts/`：…（官方安装脚本，如有）

## 安装机制
- agents → `~/.claude/agents/`：官方脚本参数 / 软链 / 复制，命令示例
- skills → `~/.claude/skills/`：同上
- ⚠️ 安装方式（软链/复制）按主流程让用户拍板，不默认

## 坑位与约定
- 本地名 vs 仓库名不一致风险；安装脚本是否覆盖同名文件
- 混合仓库：agents 与 skills 的软链/复制选择需分别确认

## 已知实践（2026-08）
- 待接入后补充：本地已装哪些、安装方式、备份位置
```

> 档案格式与现有三个档案完全同构（基本信息/目录结构/安装机制/坑位/已知实践），方法论一份、仓库差异全走档案。

### 第 4 步：登记表格（SKILL.md「支持的仓库」表加一行）

在 `/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/SKILL.md` 的表格追加一行：

```markdown
| `references/new-skill-repo.md` | new-skill-repo | agents + skills 混合，安装机制待摸清后填写 |
```

### 第 5 步：更新 frontmatter description（补一个名字）

把新仓库名加入 `description` 的「已接入」列表，保持触发精准：

- **改前**：`已接入：msitarzewski/agency-agents、wshobson/agents、mattpocock/skills（新仓库可按流程接入）`
- **改后**：`已接入：msitarzewski/agency-agents、wshobson/agents、mattpocock/skills、new-skill-repo（新仓库可按流程接入）`

只补名字，不改 description 其余措辞。

---

## 边界与硬闸门声明

- **通用方法论不动**：五步流程、对话式节奏、备份/验证规则均为通用内核，不因新仓库而改动；仓库差异全部收敛到 references/ 档案里。
- **不擅自执行**：本方案不含任何实际改动。待仓库 clone 到位、你逐项确认（来源→结构→档案内容→登记→description）后，才按阶段五执行：先 `mkdir -p ~/.claude/backups/<日期>` + `cp` 备份 SKILL.md，再改档案/表格/description，最后验证。
- **混合仓库提醒**：agents 与 skills 的安装目标目录、软链/复制选择需分别拍板；若仓库有官方脚本，优先用官方参数。

## 待你确认的点

1. 仓库 clone 到位后，先跑第 1、2 步摸底汇报；
2. 档案按上面模板建是否 OK；
3. description 改法（只补名字）是否 OK。
