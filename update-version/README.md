# Update Version Skill

根据 git diff 差异自动更新版本号到 `update_info.txt` 和 `version` 文件。

## 功能特性

- 自动根据修改规模判断版本号递增
- `update_info.txt` 仅保留最新更新
- `version` 文件追加保留完整历史
- 集成 `humanizer-zh` 优化提交信息

## 使用

```
/update-version
```
或
```
skill: "update-version"
```

## 版本递增规则

- **小改**（局部修改、bug 修复、优化）→ 小版本号递增（v2.3.7 → v2.3.8）
- **大修**（新增功能、重构）→ 次版本号递增（v2.3.8 → v2.4）
- **破坏性变更** → 主版本号递增（v2.x → v3.0）

## 格式

- `update_info.txt`: 仅保留最新版本，`###vX.X.X` 开头，不带日期
- `version`: 追加历史记录，每条带日期 `###vX.X.X - YYYY.MM.DD`
