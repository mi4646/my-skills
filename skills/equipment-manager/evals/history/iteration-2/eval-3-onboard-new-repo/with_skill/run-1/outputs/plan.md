# 接入新仓库方案：~/new-skill-repo

## 背景

用户 clone 了一个新的第三方仓库到 `~/new-skill-repo`，里面混合包含 agents 和 skills。
需要按 equipment-manager 的「接入新仓库」五步流程完成接入。

---

## 五步接入方案

### Step 1：确认来源

```bash
git -C ~/new-skill-repo remote -v
```

确认 git remote URL，提取作者/仓库名（如 `author/repo-name`），作为档案命名和登记依据。

### Step 2：摸清结构

需要探查以下信息：

```bash
# 顶层目录
ls ~/new-skill-repo/

# 递归查看目录树（深度 3）
find ~/new-skill-repo/ -maxdepth 3 -type d | head -60

# 统计 agents / skills 数量
find ~/new-skill-repo/ -name "*.md" -path "*/agents/*" | wc -l
find ~/new-skill-repo/ -name "SKILL.md" | wc -l

# 检查是否有官方安装脚本
ls ~/new-skill-repo/scripts/ 2>/dev/null
ls ~/new-skill-repo/install.sh 2>/dev/null
```

需要记录的关键信息：
- 目录组织方式（按 domain 分目录？扁平？agents/skills 混在一起还是分开？）
- 命名约定（文件名模式、目录名模式）
- 安装机制（有无官方脚本？复制 vs 符号链接？脚本参数？）
- agents 和 skills 的区分方式（目录隔离？文件后缀？SKILL.md 存在与否？）

### Step 3：建档案

在 `references/` 下新建档案文件。

**文件路径**：`/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/references/<作者名>.md`

命名规则：按 git remote 的作者/组织名命名（如 `references/johndoe.md`），与现有三个档案（mattpocock.md / msitarzewski.md / wshobson.md）保持一致。

**档案模板**（按现有三个档案的格式）：

```markdown
# 仓库档案：<author>/<repo>

## 基本信息
- **本地路径**：`/home/anonymous/new-skill-repo`
- **git remote**：`<从 Step 1 获取的 URL>`

## 目录结构
- <描述顶层目录组织，如：按 domain 分目录 / agents 和 skills 混合在 plugins/ 下>
- <命名约定，如：agent 文件 `<name>.md`，skill 目录含 `SKILL.md`>

## 安装机制（官方）
- <有官方脚本时：脚本路径 + 关键参数>
- <无官方脚本时：惯例为符号链接，给出示例命令>
- ⚠️ 安装方式（软链/复制）按主流程第⑦步让用户选择，不默认

## 坑位与约定
- <该仓库特有的注意事项，如：agents 和 skills 混装时的区分方式、特殊文件格式、命名陷阱等>
- <如无特殊坑位，写「暂无已知坑位」>

## 已知实践（<当前年月>）
- 新接入仓库，尚无历史实践记录
```

### Step 4：登记

在 SKILL.md 的「支持的仓库」表格中追加一行：

**修改文件**：`/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/SKILL.md`

**修改位置**：「支持的仓库」表格末尾

**追加内容**：

```markdown
| `references/<作者名>.md` | <author>/<repo> | <一句话描述内容，如「agents + skills 混合，按 domain 分目录」> |
```

### Step 5：更新 description

**修改文件**：`/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/SKILL.md`

**修改位置**：frontmatter `description` 字段

**当前值**：
```
description: 管理第三方 skill/agent 仓库的安装、筛选与精简。已接入：msitarzewski/agency-agents、wshobson/agents、mattpocock/skills（新仓库可按流程接入）。当用户提到某个 skill/agent 仓库的更新、安装、精简、盘点时使用——包括 git pull 后评估新内容、从这些仓库装新装备、删除无用的旧装备、或想接入一个新的第三方仓库。凡涉及"要不要装、装什么、删什么"的 skill/agent 决策都用本技能，不直接动手。各仓库结构/安装机制见 references/ 下档案。
```

**修改后**（在「已接入」列表中追加新仓库名）：
```
description: 管理第三方 skill/agent 仓库的安装、筛选与精简。已接入：msitarzewski/agency-agents、wshobson/agents、mattpocock/skills、<author>/<repo>（新仓库可按流程接入）。当用户提到某个 skill/agent 仓库的更新、安装、精简、盘点时使用——包括 git pull 后评估新内容、从这些仓库装新装备、删除无用的旧装备、或想接入一个新的第三方仓库。凡涉及"要不要装、装什么、删什么"的 skill/agent 决策都用本技能，不直接动手。各仓库结构/安装机制见 references/ 下档案。
```

---

## 变更清单汇总

| 操作 | 文件路径 | 说明 |
|------|----------|------|
| 新建 | `references/<作者名>.md` | 仓库档案（按模板填写） |
| 修改 | `SKILL.md` 表格 | 追加一行登记 |
| 修改 | `SKILL.md` frontmatter | description 已接入列表追加仓库名 |

共涉及 2 个文件（1 新建 + 1 修改），方法论核心不动。
