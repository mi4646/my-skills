# 接入新仓库方案：`~/new-skill-repo`（agents + skills 混合）

> 只读方案，未实际执行任何 clone / 安装 / git 变更。
> 仓库结构未知（agents + skills 混合），以下步骤按"先摸清再登记"的顺序展开。

---

## 阶段 0：确认来源与摸清结构（只读侦察）

在动任何登记之前，先把仓库本身看清楚。

### 0.1 确认来源
```bash
git -C ~/new-skill-repo remote -v
git -C ~/new-skill-repo log -1 --format='%h %s (%ci)'
```
- 记录 git remote URL、作者、最近一次更新
- 若 remote 缺失或为私有 fork，先与陛下确认仓库的权威来源

### 0.2 摸清目录结构
```bash
tree ~/new-skill-repo -L 3 -I 'node_modules|.git|__pycache__'
ls ~/new-skill-repo/
```
重点识别：
- **agents 在哪**：顶层 `agents/`？按 domain 分目录？文件命名约定（`<domain>-<name>.md` 还是 `<name>.md`）？
- **skills 在哪**：顶层 `skills/`？每个 skill 是否有 `SKILL.md` frontmatter（`name` / `description`）？
- **是否有 plugins**：`plugins/` 目录或符号链接惯例
- **是否有官方安装脚本**：`scripts/install.sh`、`link-skills.sh`、`Makefile` 等
- **README / CONTRIBUTING**：作者推荐的安装方式

### 0.3 摸清安装机制
- 复制（`cp -r`）还是符号链接（`ln -s`）？
- 安装目标路径：用户级 `~/.claude/agents/`、`~/.claude/skills/`，还是项目级 `.claude/`？
- 是否有官方清单文件（类似 msitarzewski 的 `agents-to-install.example`）？
- 是否有依赖（npm/pip/外部二进制）需要预装？

### 0.4 坑位扫描
- 仓库是否使用符号链接内部互指（cp 会保留链接，可能带来意外行为）
- 是否有同名 agents/skills 与已接入的三个仓库（msitarzewski / wshobson / mattpocock）冲突
- 文件编码 / 换行 / frontmatter 格式是否与 Claude Code 兼容

---

## 阶段 1：建档案（`references/<仓库名>.md`）

在 `/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/references/` 下新建一个档案文件，文件名按仓库作者或仓库名命名（例如 `new-skill-repo.md`，或 `<author>.md` 若作者明确）。

档案模板（仿照现有 `msitarzewski.md` / `wshobson.md` / `mattpocock.md`）：

```markdown
# 仓库档案：<author>/<repo>

## 基本信息
- **本地路径**：`/home/anonymous/new-skill-repo`
- **git remote**：`<url>`
- **作者 / 维护状态**：<活跃 / 归档 / 个人实验>
- **内容类型**：agents + skills 混合

## 目录结构
- <agents 目录布局>
- <skills 目录布局>
- <命名约定>

## 安装机制
- <官方脚本 / 手动 cp / 手动 ln -s>
- <安装目标路径>
- <清单文件格式（如有）>
- ⚠️ 安装方式（软链/复制）按主流程第⑦步让用户拍板

## 坑位与约定
- <与已接入仓库的同名冲突>
- <符号链接互指 / 依赖项 / 格式陷阱>

## 已知实践
- <初次接入日期>
- <已装清单 / 已删清单>
```

---

## 阶段 2：登记到 SKILL.md「支持的仓库」表格

编辑 `/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/SKILL.md`，在「支持的仓库」表格追加一行：

```markdown
| `references/<author>.md` | <author>/<repo> | agents + skills 混合，<安装机制简述> |
```

保持与现有三行格式一致（档案 | 仓库 | 内容）。

---

## 阶段 3：更新 frontmatter `description`

编辑同一份 SKILL.md 的 frontmatter：

```yaml
---
name: equipment-manager
description: 管理第三方 skill/agent 仓库的安装、筛选与精简。已接入：msitarzewski/agency-agents、wshobson/agents、mattpocock/skills、<author>/<repo>（新仓库可按流程接入）。当用户提到某个 skill/agent 仓库的更新、安装、精简、盘点时使用——包括 git pull 后评估新内容、从这些仓库装新装备、删除无用的旧装备、或想接入一个新的第三方仓库。凡涉及"要不要装、装什么、删什么"的 skill/agent 决策都用本技能，不直接动手。各仓库结构/安装机制见 references/ 下档案。
version: v1.1.0   # 可选： bump minor 表示新增支持仓库
---
```

- 仅追加仓库名到「已接入」列表，不重写整段 description
- 触发词保持不变，避免稀释触发精准度

---

## 阶段 4：走通用七步流程（首次安装评估）

档案建好、登记完成后，`~/new-skill-repo` 即视为已接入的第四仓库。首次从中挑选装备时，按 SKILL.md 的通用七步走：

1. **盘点本地现状**：`ls ~/.claude/agents/` `ls ~/.claude/skills/` 及项目级 `.claude/`
2. **识别候选来源**：`git log --diff-filter=A --since="90 days"` 找新增项；对照档案区分新旧
3. **查重**：符号链接 `readlink` 识别来源；复制产物按命名约定识别；跳过已装同类
4. **三档筛选**（基于真实项目栈，不基于"可能用到"）：
   - 保留：匹配 Python 后端 / LLM / API / DB / DevOps / 代码质量 / 文档 / git
   - 待定：边界情况，列倾向交陛下拍板
   - 建议删：PHP/CMS、移动/小程序、区块链、嵌入式、网络、ITIL、合规/渗透等不碰的方向
5. **提问澄清**：一次一问，追问到 95% 理解再出方案
6. **军师出方案**：推荐 + 理由，陛下三选一或修改
7. **备份安装验证**：
   - 覆盖/删除前备份到 `~/.claude/backups/<日期>/`
   - 安装方式（符号链接 vs 复制）由陛下拍板，不默认替选
   - 验证：文件存在、非空；符号链接则 `readlink` 确认目标存在、目标目录有 `SKILL.md` 或 agent frontmatter

---

## 阶段 5：与陛下对齐的关键决策点（需提问）

以下信息方案阶段无法替陛下决定，需按"一次一问"原则逐步澄清：

1. **仓库权威来源**：`~/new-skill-repo` 的 git remote 是什么？作者是谁？（决定档案命名与引用方式）
2. **安装方式偏好**：符号链接（更新自动传播，依赖路径存在）vs 复制（独立稳定，更新需手动重装）？
3. **作用域**：装到用户级 `~/.claude/` 还是项目级 `/var/www/demo/.claude/`？
4. **范围**：agents 全装 / 精选？skills 全装 / 精选？是否包含 plugins？
5. **是否替换现有**：若与已接入仓库有同名装备，是保留现有、替换、还是共存（不同作用域）？

---

## 交付清单（执行时的产物）

| 产物 | 路径 | 说明 |
|------|------|------|
| 仓库档案 | `~/.claude/skills/my-skills/skills/equipment-manager/references/<author>.md` | 新建，按模板 |
| SKILL.md 表格 | `~/.claude/skills/my-skills/skills/equipment-manager/SKILL.md` | 追加一行 |
| SKILL.md description | 同上 frontmatter | 追加仓库名到「已接入」列表 |
| 可选：bump version | 同上 frontmatter | v1.0.0 → v1.1.0 |

---

## 风险与克制

- **不为了装而装**：档案建完不等于要装，装多少按三档筛选 + 陛下拍板
- **方法论不动**：只加档案、加表格一行、加 description 一个名字，通用七步流程原封不动
- **拿不准就问**：仓库结构未知时不预填档案内容，先侦察再落笔
- **删除前必备份**：首次接入若涉及替换现有装备，先备份到 `~/.claude/backups/<日期>/`
