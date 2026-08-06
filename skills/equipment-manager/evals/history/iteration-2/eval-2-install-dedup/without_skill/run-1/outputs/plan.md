# 安装方案：grill-me skill（软链方式）

## 一、查重结果

### 1.1 是否已安装

| 检查项 | 结果 |
|--------|------|
| 已安装路径 | `~/.claude/skills/my-skills/skills/grill-me/` |
| 安装方式 | **普通目录**（非软链接） |
| 内容 | `SKILL.md`（147 字节）+ `agents/` 子目录 |
| 是否可被 Claude 识别 | 是（已在可用 skills 列表中） |

**结论：grill-me 已安装，但安装方式是普通目录拷贝，不是用户要求的软链。**

### 1.2 来源仓库定位

用户提到来源是 `mattpocock` 的 skills 仓库。实际文件系统情况：

| 路径 | 是否包含 grill-me |
|------|-------------------|
| `/home/anonymous/.gstack/projects/mattpocock-skills/` | **否**（仓库内无此 skill） |
| `/home/anonymous/skills/skills/productivity/grill-me/` | **是**（实际来源） |

**结论：用户所说的 `mattpocock` 仓库内没有 `grill-me`。实际来源是 `/home/anonymous/skills/` 仓库。**

---

## 二、安装方案

### 方案 A（推荐）：删除旧目录，重建为软链

**理由：** 用户明确要求"用软链"，当前是普通目录，需重建。软链的好处是源仓库 `git pull` 后 skill 自动同步，无需重复拷贝。

**步骤：**

```bash
# 1. 备份当前普通目录（保险起见）
mv ~/.claude/skills/my-skills/skills/grill-me \
   ~/.claude/skills/my-skills/skills/grill-me.bak

# 2. 创建软链接，指向实际来源
ln -s /home/anonymous/skills/skills/productivity/grill-me \
      ~/.claude/skills/my-skills/skills/grill-me

# 3. 验证
ls -la ~/.claude/skills/my-skills/skills/grill-me
# 预期输出：grill-me -> /home/anonymous/skills/skills/productivity/grill-me

# 4. 确认 skill 仍可被识别
# （重启 Claude 或重新加载 skills 后检查）

# 5. 确认无误后删除备份
rm -rf ~/.claude/skills/my-skills/skills/grill-me.bak
```

**风险：** 低。skill 内容不变，只是改变了引用方式。

### 方案 B：保持现状，不做任何操作

**理由：** 已安装且可用，普通目录 vs 软链对功能无影响。

**适用场景：** 用户不关心安装方式，只关心能否使用。

**缺点：** 不符合用户"用软链"的明确要求；源仓库更新时需手动同步。

### 方案 C：先确认来源仓库再决定

**待澄清：**
- 用户提到的 `mattpocock` 仓库（`/home/anonymous/.gstack/projects/mattpocock-skills/`）内没有 `grill-me`
- 实际来源是 `/home/anonymous/skills/` 仓库
- 需确认用户是否接受此来源，或是否期望从其他仓库安装

---

## 三、推荐

**推荐方案 A**（重建为软链）。

执行前需与用户确认：
1. 来源仓库 `/home/anonymous/skills/skills/productivity/grill-me/` 是否正确（用户原话是 `mattpocock`，但该仓库内无此 skill）
2. 是否接受备份后重建软链的操作

---

## 四、备注

- 如果用户确实想从 mattpocock 仓库安装，该仓库（`/home/anonymous/.gstack/projects/mattpocock-skills/`）内没有 `grill-me`，无法完成
- `my-skills:equipment-manager` 技能可能提供标准化的安装流程，但本方案按"无 skill"基线要求，仅基于文件系统直接检查
