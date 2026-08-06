# grill-me 安装方案

## 1. 查重结果

| 位置 | 类型 | 状态 |
|------|------|------|
| `~/.claude/skills/grill-me` | — | **不存在** |
| `/home/anonymous/.claude/skills/my-skills/skills/grill-me` | 真实目录（非软链） | **已存在**，内容与源完全一致（`diff -r` 无差异） |
| `/home/anonymous/skills/skills/productivity/grill-me` | mattpocock 源 | 源目录 |

**结论：grill-me 已经装过了。** 当前以「复制」方式安装在 my-skills 内，不是软链。

## 2. 内容对比

```
my-skills/skills/grill-me/
├── SKILL.md          (147 B)
└── agents/
    └── openai.yaml   (137 B)
```

与 mattpocock 源 `/home/anonymous/skills/skills/productivity/grill-me/` 完全相同，无本地修改。

## 3. 软链安装方案

用户要求用软链安装。当前是复制安装的实目录，需替换为软链：

```bash
# 1. 备份当前实目录（防本地有未察觉改动）
mkdir -p ~/.claude/backups/2026-08-04
mv /home/anonymous/.claude/skills/my-skills/skills/grill-me \
   ~/.claude/backups/2026-08-04/grill-me

# 2. 创建软链指向 mattpocock 源
ln -s /home/anonymous/skills/skills/productivity/grill-me \
      /home/anonymous/.claude/skills/my-skills/skills/grill-me

# 3. 验证
readlink /home/anonymous/.claude/skills/my-skills/skills/grill-me
# 期望输出: /home/anonymous/skills/skills/productivity/grill-me
ls -la /home/anonymous/.claude/skills/my-skills/skills/grill-me/SKILL.md
# 期望: 文件存在且非空
```

## 4. 风险评估

- **低风险**：`diff -r` 确认内容完全一致，替换为软链无功能变化
- **好处**：仓库 `git pull` 后自动传播更新，无需重装
- **注意**：mattpocock 仓库路径 `/home/anonymous/skills` 若被移动/删除，软链会断

## 5. 建议

当前实目录与源完全一致，说明是之前通过复制安装的。替换为软链是合理的——用户明确要求软链方式，且内容无本地修改，替换无风险。

**是否执行：需用户确认。**
