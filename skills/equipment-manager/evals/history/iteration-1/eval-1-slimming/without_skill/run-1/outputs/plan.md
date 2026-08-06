# engineering-* Agent 精简方案

> 只读评估，未做任何变更。待陛下确认后执行。

## 评估原则

1. **项目相关性** — 本项目是 Python/FastAPI/SQLite CLI+Web 工具，不是大数据/微服务/飞书集成项目
2. **Skill 覆盖度** — 已有 skill 覆盖的能力不保留独立 agent（ponytail、/review、/ship、/document-generate 等）
3. **去重叠** — 功能高度重叠的 agent 合并保留一个
4. **使用频率** — 极少触发的 niche 场景删除

---

## 三档清单

### 保留（4 个）

| Agent | 理由 |
|-------|------|
| `engineering-code-reviewer` | 核心工作流，/review skill 的底层执行者，代码质量门禁 |
| `engineering-software-architect` | 系统设计决策（bounded context、ADR、架构模式），项目演进需要 |
| `engineering-backend-architect` | Python/FastAPI 后端聚焦，与 software-architect 互补（一个战略层一个实现层） |
| `engineering-database-optimizer` | SQLite WAL 优化、查询计划、索引策略，项目核心依赖 |

### 待定（3 个）

| Agent | 理由 | 建议 |
|-------|------|------|
| `engineering-frontend-developer` | 项目前端仅 Jinja2+HTMX 模板，无复杂 SPA | 若后续无 React/Vue 前端需求可删 |
| `engineering-prompt-engineer` | 项目有 LLM prompt 构建（prompts/ 包），但已有 prompt-engineering-patterns skill | 若 skill 覆盖足够可删 |
| `engineering-technical-writer` | 有 /document-generate skill，但 agent 可做更深入的文档架构 | 若 skill 满足需求可删 |

### 删除（12 个）

| Agent | 删除理由 |
|-------|----------|
| `engineering-ai-data-remediation-engineer` | 极度小众（SLM 自修复数据管道），项目完全无关 |
| `engineering-autonomous-optimization-architect` | LLM 成本优化/shadow testing，项目不需要 |
| `engineering-feishu-integration-developer` | 飞书/Lark 专用，项目不用飞书 |
| `engineering-data-engineer` | ETL/Spark/lakehouse，项目用 SQLite 不需要 |
| `engineering-multi-agent-systems-architect` | 已有 skill 覆盖（subagent-driven-development 等） |
| `engineering-rapid-prototyper` | 项目已成熟，不需要快速原型验证 |
| `engineering-ai-engineer` | 与 prompt-engineer 重叠，项目 LLM 调用简单（httpx 直调） |
| `engineering-devops-automator` | 已有 /ship、/land-and-deploy、/canary skills 覆盖 |
| `engineering-sre` | 项目规模不需要 SRE（无 SLO/error budget 需求） |
| `engineering-git-workflow-master` | 已有 /ship skill 覆盖 git 工作流 |
| `engineering-minimal-change-engineer` | 已有 ponytail 模式覆盖（最小变更原则） |
| `engineering-codebase-onboarding-engineer` | 极少触发，Explore agent 可替代 |

---

## 精简结果

- **保留**: 4 个
- **待定**: 3 个（建议陛下根据实际使用频率决定）
- **删除**: 12 个
- **精简率**: 63%（12/19）

若待定 3 个全部删除，精简率达 79%（15/19）。

---

## 执行命令（待确认后）

```bash
# 删除确认的 12 个
rm ~/.claude/agents/engineering-ai-data-remediation-engineer.md
rm ~/.claude/agents/engineering-autonomous-optimization-architect.md
rm ~/.claude/agents/engineering-feishu-integration-developer.md
rm ~/.claude/agents/engineering-data-engineer.md
rm ~/.claude/agents/engineering-multi-agent-systems-architect.md
rm ~/.claude/agents/engineering-rapid-prototyper.md
rm ~/.claude/agents/engineering-ai-engineer.md
rm ~/.claude/agents/engineering-devops-automator.md
rm ~/.claude/agents/engineering-sre.md
rm ~/.claude/agents/engineering-git-workflow-master.md
rm ~/.claude/agents/engineering-minimal-change-engineer.md
rm ~/.claude/agents/engineering-codebase-onboarding-engineer.md

# 待定 3 个（根据陛下决定）
# rm ~/.claude/agents/engineering-frontend-developer.md
# rm ~/.claude/agents/engineering-prompt-engineer.md
# rm ~/.claude/agents/engineering-technical-writer.md
```

---

## 补充说明

1. **backend-architect vs software-architect** — 两者有重叠但定位不同：
   - `software-architect`: 战略层（bounded context、ADR、架构模式选择）
   - `backend-architect`: 实现层（schema 设计、API 开发、性能优化）
   - 建议保留两个，分别处理不同抽象层级的问题

2. **Skill 替代性** — 删除的 agent 能力已被 skill 覆盖：
   - DevOps → /ship, /land-and-deploy
   - Git → /ship
   - Minimal change → ponytail 模式
   - Multi-agent → subagent-driven-development skill

3. **项目特性** — 本项目是单体 Python 应用，不需要微服务/分布式/大数据相关 agent
