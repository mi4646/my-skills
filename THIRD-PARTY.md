# 三方装备说明

本仓库 `install.sh` 一键安装的第三方 skill 总览，来源独立、更新互不影响。

## Skills

| 资产 | 类型 | 用途 | 内含 | 来源 |
|---|---|---|---|---|
| hallmark | 纯技能 | 反 AI 味设计指导：新页面 / 重设计 / 审计 | 1 | [github.com/nutlope/hallmark](https://github.com/nutlope/hallmark) |
| storage-analyzer | 技能 + Python 脚本 | 磁盘 / 仓库存储占用扫描分析 | 1 | [github.com/KKKKhazix/khazix-skills](https://github.com/KKKKhazix/khazix-skills) |

## 维护

- 安装：`bash install.sh`（幂等，已装跳过）
- 升级：`bash install.sh --update`（`git pull` + 强制重新复制）
- 实时清单：`bash install.sh --list`

### 调用方式

**独立第三方（无前缀）**

```
/hallmark   /storage-analyzer
```
