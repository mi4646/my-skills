# 装备安装评估：mattpocock/skills 的 grill-me → my-skills（软链）

> 按 SKILL.md 七步方法论执行。结论先行：**grill-me 已经装过了，装的是「复制」不是「软链」**，本次任务是「复制 → 软链」的换装，而非全新安装。

---

## ① 盘点本地现状（已核实）

| 项 | 路径 | 状态 |
|----|------|------|
| 用户级 my-skills 集合 | `~/.claude/skills/my-skills/` | 存在，独立 git 仓库 |
| 集合内 sub-skills | `~/.claude/skills/my-skills/skills/` | 16 个技能目录 |
| grill-me 本地副本 | `~/.claude/skills/my-skills/skills/grill-me/` | **存在** |
| 副本形态 | — | **真实目录（复制），非符号链接**（`readlink` 无输出） |
| 副本 git 跟踪 | `skills/grill-me/SKILL.md`、`skills/grill-me/agents/openai.yaml` | 两文件均已被 my-skills 仓库跟踪 |

## ② 识别候选来源（已核实）

| 项 | 值 |
|----|----|
| 仓库路径 | `/home/anonymous/skills` |
| remote | `https://github.com/mattpocock/skills.git`（已确认） |
| 源技能路径 | `/home/anonymous/skills/skills/productivity/grill-me/` |
| 源内容 | `SKILL.md`（147 字节）+ `agents/openai.yaml` |
| 最近相关提交 | 2026-07-13 添加 `agents/openai.yaml`；仓库最近合入 2026-07-28 |

## ③ 查重（已核实）

- **已装**：grill-me 存在于 my-skills，且**非软链**——是复制安装。
- **内容一致性**：`diff -r` 源目录 vs 本地副本 → **IDENTICAL**，SKILL.md 与 agents/openai.yaml 逐字节一致，无更新需求。
- **同类已装**：mattpocock 源共引入 4 个技能（grill-me / prototype / research / resolving-merge-conflicts），**全部为复制安装**，无软链先例。

## ④ 筛选

grill-me（"A relentless interview to sharpen a plan or design"）属于用户核心栈（LLM/文档/工作流），**保留**。无删除项。

## ⑤ 澄清点

一个取舍需要【陛下】定夺：

- **仅 grill-me 换软链** vs **4 个 mattpocock 源技能全部换软链**：只换 grill-me 会造成集合内同源技能安装方式不一致；全部换则更统一，但改动面大、且一旦 my-skills 仓库被 clone 到别处会全部断链。
- 本方案以下按用户任务原文「装 grill-me、用软链」只写 grill-me 的换装步骤；如需全量换装，套用同一命令模板即可。

## ⑥ 推荐方案（用户已明确要软链）

已装（复制）→ 换装为符号链接。按方法论第⑦步执行：备份 → 换装 → 验证。

### 第 1 步：备份（覆盖/删除前必做）

```bash
mkdir -p ~/.claude/backups/skills-$(date +%Y%m%d)
cp -r ~/.claude/skills/my-skills/skills/grill-me ~/.claude/backups/skills-$(date +%Y%m%d)/grill-me
```

### 第 2 步：删除复制目录（因已 git 跟踪，用 git rm 保留仓库记录）

```bash
git -C ~/.claude/skills/my-skills rm -r skills/grill-me
```

### 第 3 步：创建符号链接（软链）

```bash
ln -s /home/anonymous/skills/skills/productivity/grill-me ~/.claude/skills/my-skills/skills/grill-me
```

> 官方脚本 `./scripts/link-skills.sh` 是装到 `~/.claude/skills/` 顶层，不装进 my-skills 集合内，故此处手写 `ln -s` 即可。

### 第 4 步：验证

```bash
readlink ~/.claude/skills/my-skills/skills/grill-me
# 期望输出：/home/anonymous/skills/skills/productivity/grill-me

ls -la ~/.claude/skills/my-skills/skills/grill-me/SKILL.md
# 期望：软链指向的文件存在且非空（147 字节）

diff -r /home/anonymous/skills/skills/productivity/grill-me ~/.claude/skills/my-skills/skills/grill-me
# 期望：无差异（软链跟随目标，内容一致即验证通过）
```

## ⑦ 结论

- **已装**：grill-me 已存在于 my-skills（复制方式），内容与源完全一致，无需重新安装。
- **待办**：仅需将安装方式从「复制」换为「软链」（若【陛下】确认）。
- **坑位提醒**：软链依赖 `/home/anonymous/skills` 路径长期存在；仓库被移动/删除会断链。且 my-skills 是独立 git 仓库，软链会被 git 正常跟踪，clone 到别的机器会断链——这是「软链装进 git 管理的集合」的固有代价，已知且接受即可。
- **一致性备注**：其余 3 个同源技能（prototype/research/resolving-merge-conflicts）仍为复制，如需统一可套用同模板，等【陛下】指示。
