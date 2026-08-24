# 三方装备说明

本仓库 `install.sh` 一键安装的第三方 skill、agents、plugins 总览，来源独立、更新互不影响。

## Skills

| 资产 | 类型 | 用途 | 内含 | 来源 |
|---|---|---|---|---|
| hallmark | 纯技能 | 反 AI 味设计指导：新页面 / 重设计 / 审计 | 1 | [github.com/nutlope/hallmark](https://github.com/nutlope/hallmark) |
| storage-analyzer | 技能 + Python 脚本 | 磁盘 / 仓库存储占用扫描分析 | 1 | [github.com/KKKKhazix/khazix-skills](https://github.com/KKKKhazix/khazix-skills) |
| addyosmani | 独立技能目录 | 生产级工程方法论 | `/context-engineering`（上下文工程：优化 CLAUDE.md/规则文件与上下文分层）<br>`/interview-me`（需求访谈：一次一问挖真实需求）<br>`/source-driven-development`（官方文档驱动开发：框架代码查文档+给来源） | [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| mattpocock | 独立技能目录 | 结构化多会话教学 | `/teach`（纯用户唤起：MISSION.md + 教案 HTML + 学习记录） | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) |
| wshobson | 独立技能目录 | 反 AI 味写作审计 | `/avoid-ai-writing`（detect/rewrite/edit 三模式 + 三级词表，纯 markdown 零依赖） | [github.com/wshobson/agents](https://github.com/wshobson/agents) |

## Agents

**独立安装（install.sh ⑤段，复制到 `~/.claude/agents/`，不用软链）**：

| 资产 | 类型 | 用途 | 内含 | 来源 |
|---|---|---|---|---|
| wshobson | agents 文件（复制） | 生产级开发专家人格 + skill 评测裁判 | `eval-judge`（skill 质量评测裁判：触发准确度/编排/输出质量/范围 4 维评分）<br>`python-development-fastapi-pro` + `python-development-django-pro`（Python 后端专家人格）<br>`bash-pro`（防御性 Bash 专家） | [github.com/wshobson/agents](https://github.com/wshobson/agents) |

## 维护

- 安装：`bash install.sh`（幂等，已装跳过）
- 升级：`bash install.sh --update`（`git pull` + 强制重新复制）
- 实时清单：`bash install.sh --list`

### 调用方式

**独立第三方（无前缀）**

```
/hallmark   /storage-analyzer
```

**addaysomani 独立技能（无前缀，自动路由触发）**

```
/context-engineering   /interview-me   /source-driven-development   /teach
```

**wshobson agents（无前缀，Agent 工具/子代理按名调用）**

```
eval-judge   python-development-fastapi-pro   python-development-django-pro   bash-pro
```

**wshobson 独立技能（无前缀）**

```
/avoid-ai-writing
```
