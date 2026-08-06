# grill-me 安装方案（软链方式）

## 查重结果

**已安装**：`grill-me` 已存在于 `/home/anonymous/.claude/skills/my-skills/skills/grill-me/`

### 当前状态

- **安装方式**：复制（非软链）
  - `readlink` 返回空，`ls -la` 显示为普通目录（无 `->` 箭头）
  - 内容来自 `/home/anonymous/skills/skills/productivity/grill-me`
- **内容对比**：`diff -rq` 显示本地与源仓库完全一致
- **同仓库其他技能**：`prototype`、`research`、`resolving-merge-conflicts` 均为复制安装

### 告知用户

```
grill-me 已安装（复制方式），内容与 mattpocock/skills 仓库一致。
当前为独立副本，不随仓库更新自动同步。

用户要求以软链方式安装，需替换现有副本。
```

## 安装方案（软链）

### 步骤

1. **备份现有安装**
   ```bash
   mkdir -p ~/.claude/backups/2026-08-04
   cp -r ~/.claude/skills/my-skills/skills/grill-me ~/.claude/backups/2026-08-04/grill-me-copy
   ```

2. **删除现有副本**
   ```bash
   rm -rf ~/.claude/skills/my-skills/skills/grill-me
   ```

3. **创建软链**
   ```bash
   ln -s /home/anonymous/skills/skills/productivity/grill-me ~/.claude/skills/my-skills/skills/grill-me
   ```

4. **验证**
   ```bash
   readlink ~/.claude/skills/my-skills/skills/grill-me
   # 应输出: /home/anonymous/skills/skills/productivity/grill-me

   ls -la ~/.claude/skills/my-skills/skills/grill-me
   # 应显示: grill-me -> /home/anonymous/skills/skills/productivity/grill-me

   test -f ~/.claude/skills/my-skills/skills/grill-me/SKILL.md && echo "OK"
   # 应输出: OK
   ```

### 方案对比（供用户选择）

| 方式 | 优点 | 缺点 | 适合 |
|------|------|------|------|
| **软链（推荐）** | 仓库更新自动传播，无需重装；省磁盘 | 依赖仓库路径存在，仓库移动/删除会断链 | 仓库长期稳定、想省维护 |
| **复制（当前）** | 完全独立，不依赖仓库路径，永不断链 | 仓库更新需手动重装；占磁盘 | 仓库可能变动、图省心 |

**推荐软链**：mattpocock/skills 仓库稳定，且 my-skills 生态已引入 4 个本仓库技能，统一管理更方便。

### 执行前确认

需用户确认：
- [ ] 是否同意删除现有复制版本（已备份）
- [ ] 是否选择软链方式安装
- [ ] 是否接受软链依赖仓库路径存在的风险

## 参考

- 仓库档案：`/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/references/mattpocock.md`
- 源路径：`/home/anonymous/skills/skills/productivity/grill-me`
- 目标路径：`/home/anonymous/.claude/skills/my-skills/skills/grill-me`
