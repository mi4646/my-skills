# grill-me 技能安装方案

## 查重结果

**已安装**：`/home/anonymous/.claude/skills/my-skills/skills/grill-me`

- 类型：普通目录（非软链）
- 来源：commit `918b5aa` 引入 mattpocock 第三方技能
- 内容：与源仓库完全一致（`diff -rq` 无差异）

## 源仓库位置

- 仓库路径：`/home/anonymous/skills/`
- 远程地址：`https://github.com/mattpocock/skills.git`
- 技能源路径：`/home/anonymous/skills/skills/productivity/grill-me`

## 安装方案

### 当前状态

grill-me 已存在于 my-skills，但作为**普通目录**而非软链。这意味着：
- 源仓库更新时，my-skills 的版本不会自动同步
- 需要手动 `git pull` 或重新拷贝才能获取更新

### 推荐操作：转换为软链

**步骤 1：备份现有目录**
```bash
cd /home/anonymous/.claude/skills/my-skills/skills
mv grill-me grill-me.bak
```

**步骤 2：创建软链**
```bash
ln -s /home/anonymous/skills/skills/productivity/grill-me grill-me
```

**步骤 3：验证**
```bash
ls -la grill-me
# 应显示：grill-me -> /home/anonymous/skills/skills/productivity/grill-me
```

**步骤 4：提交变更**
```bash
cd /home/anonymous/.claude/skills/my-skills
git add skills/grill-me
git commit -m "refactor: grill-me 改为软链指向 mattpocock 源仓库"
```

**步骤 5：清理备份（确认无误后）**
```bash
rm -rf grill-me.bak
```

## 替代方案

### 方案 A：保持现状（不推荐）
- 优点：无需改动
- 缺点：无法自动同步源仓库更新

### 方案 B：删除后重新安装（冗余）
- 由于内容已一致，无需删除重装

## 验收标准

- [ ] `ls -la skills/grill-me` 显示软链指向 `/home/anonymous/skills/skills/productivity/grill-me`
- [ ] `cat skills/grill-me/SKILL.md` 正常输出技能定义
- [ ] `git status` 显示变更已提交

## 预计耗时

5 分钟（含验证和提交）
