# 评估：把 mattpocock/skills 的 grill-me 装进 my-skills（软链方式）

评估日期：2026-08-04
评估方法：equipment-manager 技能（阶段三摸底查重 → 阶段四给方案）
执行状态：**只评估未改动**（硬闸门：未获批准前不动任何文件）

## 一、摸底结果（已核实的事实）

### 1. 是否已装：**已装，但装的是副本，不是软链**
- 目标路径 `/home/anonymous/.claude/skills/my-skills/skills/grill-me/` **已存在**，是一个**真实目录（复制方式安装）**，不是符号链接（`readlink` 无输出）。
- 目录内：`SKILL.md`（147 字节，2026-08-03 15:51）、`agents/openai.yaml`（137 字节）。

### 2. 来源仓库核实
- 仓库路径 `/home/anonymous/skills`，remote 为 `https://github.com/mattpocock/skills.git`（与档案 `references/mattpocock.md` 一致）。
- 源技能位于仓库内 `/home/anonymous/skills/skills/productivity/grill-me/`，内容为 `SKILL.md` + `agents/openai.yaml`。

### 3. 内容一致性：**完全一致**
- `diff -r /home/anonymous/skills/skills/productivity/grill-me/ /home/anonymous/.claude/skills/my-skills/skills/grill-me/` 退出码 0，两个文件逐字节相同。
- 结论：**无需重新安装**，已装的副本与仓库源零差异。

### 4. 命名空间
- grill-me 位于 my-skills 插件的 `skills/` 下，暴露为 `my-skills:grill-me`。改造成软链后命名空间不变。

### 5. 官方脚本不适用
- 仓库官方 `scripts/link-skills.sh` 注明是 **dev-only、维护者专用**，且行为是把仓库里**全部** skill 软链到 `~/.claude/skills`（顶层，不是 my-skills 插件目录）。
- 不适合"只装 grill-me 一个到 my-skills 插件里"的诉求 → 走**手动 `ln -s`**。

## 二、查重结论（说人话）

| 项 | 结论 |
|---|---|
| 装没装 | 已经装了 |
| 怎么装的 | 复制（独立副本），不是软链 |
| 内容跟仓库一样吗 | 一样，零差异 |
| 你要的软链 | 没做，现在是副本 |

所以这单的真正动作不是"安装"，而是**把已有副本改造成软链**（副本删除 + 建软链），让仓库 `git pull` 的更新自动传播。

## 三、安装方案（阶段四，给 2-3 个选项）

### 选项 A（推荐）：改造成软链 —— 满足"用软链"的要求
- 利：仓库更新自动传播；省磁盘；符合你的明确要求。
- 弊：若仓库路径变动或仓库被删，软链断裂（可 `readlink` 发现、重链修复）。
- 步骤（**需你批准后才执行**）：

```bash
# 1. 备份现有副本（覆盖前先备份，不用 mv xxx.bak）
mkdir -p ~/.claude/backups/2026-08-04
cp -r /home/anonymous/.claude/skills/my-skills/skills/grill-me ~/.claude/backups/2026-08-04/grill-me-copy

# 2. 移除已装的副本
rm -rf /home/anonymous/.claude/skills/my-skills/skills/grill-me

# 3. 建软链指向仓库源
ln -s /home/anonymous/skills/skills/productivity/grill-me /home/anonymous/.claude/skills/my-skills/skills/grill-me

# 4. 验证：软链目标存在、目录非空、有 SKILL.md
ls -la /home/anonymous/.claude/skills/my-skills/skills/grill-me   # 应显示 -> /home/anonymous/skills/skills/productivity/grill-me
readlink /home/anonymous/.claude/skills/my-skills/skills/grill-me # 应输出源路径
test -f /home/anonymous/.claude/skills/my-skills/skills/grill-me/SKILL.md && echo "软链有效，SKILL.md 存在"
```

### 选项 B：保持副本现状，什么都不做
- 利：零改动、零风险；内容与仓库已完全一致。
- 弊：仓库更新不会自动传播，下次要手动重拷；不是你要的软链。
- 适用：如果你其实不介意安装方式，这个最省事。

### 选项 C：先删掉，再重新软链安装（等价于 A 但多一步）
- 不推荐：与 A 结果相同，且多了"先删后装"的窗口期风险，无额外收益。

## 四、推荐与说明

- **推荐选项 A**：一次执行到位，满足"用软链"，且已有副本与源一致，备份后可安全替换。
- 备份目录 `~/.claude/backups/` 已存在且已有 `agents-20260804`，沿用同一日期目录。
- 若日后仓库路径变动：`rm` 旧软链 + 重新 `ln -s` 新路径即可，2 行命令。
- 软链生效后 `git -C /home/anonymous/skills pull` 即自动更新 grill-me，无需再装。
