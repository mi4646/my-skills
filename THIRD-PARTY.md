# 三方装备说明

本仓库 `install.sh` 一键安装的第三方 skill 总览，来源独立、更新互不影响。

## Skills

| 资产 | 类型 | 用途 | 内含 | 来源 |
|---|---|---|---|---|
| hallmark | 纯技能 | 反 AI 味设计指导：新页面 / 重设计 / 审计 | 1 | [github.com/nutlope/hallmark](https://github.com/nutlope/hallmark) |
| storage-analyzer | 技能 + Python 脚本 | 磁盘 / 仓库存储占用扫描分析 | 1 | [github.com/KKKKhazix/khazix-skills](https://github.com/KKKKhazix/khazix-skills) |
| find-skills | 纯技能 | 发现并安装其他 skill（skills.sh / `npx skills`） | 1 | [github.com/vercel-labs/skills](https://github.com/vercel-labs/skills) |
| api-and-interface-design | 纯技能 | API / 模块边界与类型契约设计指导 | 1 | [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| mattpocock-grill | 纯技能 | 拷问式访谈：`grill-me` / `grill-with-docs` 是入口壳，实际调用 `grilling` + `domain-modeling` | 4 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) |

## 维护

- 安装：`bash install.sh`（幂等，已装跳过）
- 升级：`bash install.sh --update`（`git pull` + 强制重新复制）
- 实时清单：`bash install.sh --list`

### 调用方式

**独立第三方（无前缀）**

```
/hallmark   /storage-analyzer   /find-skills   /api-and-interface-design
/grill-me   /grill-with-docs
```

`grilling` 与 `domain-modeling` 由模型按需自动调用（`/grill-me`、`/grill-with-docs` 的内部依赖），不必手动唤起。
