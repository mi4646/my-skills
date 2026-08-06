# 新仓库接入方案：~/new-skill-repo（agents + skills 混合）

## 背景

用户 clone 了一个新仓库 `~/new-skill-repo`，里面是 agents 和 skills 混合的。需要按 equipment-manager 流程接入管理。

## 本地现状（盘点结果）

| 类别 | 数量 | 来源 | 安装方式 |
|------|------|------|----------|
| agents（`~/.claude/agents/`） | 22 个 engineering-* + 3 个 security-* | msitarzewski/agency-agents | 复制 |
| skills（`~/.claude/skills/`） | 19 个符号链接 | wshobson/agents | 符号链接 |
| skills（`~/.claude/skills/`） | gstack 生态 + my-skills 生态 | 各自来源 | 目录/链接混合 |
| skills（项目级 `.claude/skills/`） | 15 个符号链接 | wshobson/agents | 符号链接 |

## 接入步骤

### Step 1：确认来源

```bash
git -C ~/new-skill-repo remote -v
```

记录 git remote URL。如果仓库尚未 clone，先 clone：
```bash
git clone <remote-url> ~/new-skill-repo
```

### Step 2：摸清结构

需要回答以下问题并记录：

```bash
# 顶层目录
ls ~/new-skill-repo/

# agents 和 skills 分别在哪
find ~/new-skill-repo -maxdepth 3 -type d | grep -iE 'agent|skill'

# 文件命名约定
ls ~/new-skill-repo/<agents目录>/ | head -10
ls ~/new-skill-repo/<skills目录>/ | head -10

# 安装脚本
ls ~/new-skill-repo/scripts/ 2>/dev/null
ls ~/new-skill-repo/*.sh 2>/dev/null

# 文件格式（frontmatter 判断宿主兼容性）
head -5 ~/new-skill-repo/<某个agent文件>
head -5 ~/new-skill-repo/<某个skill目录>/SKILL.md
```

关键问题清单：
- [ ] agents 和 skills 分别放在哪些目录？
- [ ] 是按 domain 分目录还是扁平结构？
- [ ] 文件命名约定？（如 `domain-name.md` 还是别的）
- [ ] 有安装脚本吗？（install.sh / link-*.sh / Makefile）
- [ ] 安装是复制还是符号链接？
- [ ] agent/skill 文件格式是 Claude Code 原生（frontmatter `---` 段含 name/description）还是其他宿主格式？

### Step 3：建档案

在 `/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/references/` 下新建档案。

**文件命名**：按仓库作者或仓库名，如 `new-author.md` 或 `new-skill-repo.md`。

**档案模板**（仿现有三档案格式）：

```markdown
# 仓库档案：<owner>/<repo>

## 基本信息
- **本地路径**：`/home/anonymous/new-skill-repo`
- **git remote**：`<remote URL>`

## 目录结构
- agents 目录：<描述 agents 的组织方式和命名约定>
- skills 目录：<描述 skills 的组织方式和命名约定>
- 其他：<scripts/ 等>

## 安装机制
- <官方脚本或惯例>
- <符号链接还是复制，参数说明>
- ⚠️ 安装方式按主流程第⑦步让用户拍板（软链/复制二选一）

## 坑位与约定
- <发现的特殊行为、命名陷阱、格式兼容性问题>
- <如果是混合 agents+skills，说明两者安装路径不同>

## 已知实践（2026-08）
- <首次接入时的盘点结果>
```

### Step 4：查重

新仓库的 agents/skills 逐个对照本地已装内容，跳过重复：

```bash
# agents 查重
ls ~/new-skill-repo/<agents目录>/ | while read f; do
  name=$(basename "$f" .md)
  [ -f ~/.claude/agents/"$name".md ] && echo "DUP agent: $name"
done

# skills 查重
ls ~/new-skill-repo/<skills目录>/ | while read d; do
  [ -d ~/.claude/skills/"$d" ] && echo "DUP skill: $d"
  [ -L ~/.claude/skills/"$d" ] && echo "LINKED skill: $d -> $(readlink ~/.claude/skills/$d)"
done
```

已有的 22 个 engineering-* agents 和 19 个 wshobson skills 是主要查重对象。

### Step 5：登记到 SKILL.md 表格

在 `/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/SKILL.md` 的「支持的仓库」表格加一行：

```markdown
| `references/<新档案名>.md` | <owner>/<repo> | agents + skills 混合，<一句话描述结构特点> |
```

### Step 6：更新 description

在 SKILL.md frontmatter 的 `description` 字段，把新仓库加入「已接入」列表。

当前：
```
已接入：msitarzewski/agency-agents、wshobson/agents、mattpocock/skills
```

改为：
```
已接入：msitarzewski/agency-agents、wshobson/agents、mattpocock/skills、<新仓库名>
```

description 是 skill 路由的触发依据，必须保持精准。

### Step 7：验证

- [ ] `references/<新档案>.md` 存在且内容完整
- [ ] SKILL.md 表格新增一行
- [ ] SKILL.md frontmatter description 已更新
- [ ] 跑一次盘点确认新仓库可被正常引用

## 产出清单

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `references/<新档案名>.md` | 新建 | 仓库档案，含基本信息/目录结构/安装机制/坑位/已知实践 |
| `SKILL.md` 表格 | 加一行 | 登记新仓库到「支持的仓库」表 |
| `SKILL.md` frontmatter | 改 description | 补一个仓库名到「已接入」列表 |

## 不动什么

- 通用方法论（七步流程）不改
- 已有三个档案不动
- 仓库本身不做安装/删除——接入方案只建档案和登记，实际安装走七步流程
