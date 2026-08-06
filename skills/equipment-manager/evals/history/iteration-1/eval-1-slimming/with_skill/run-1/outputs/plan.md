# engineering-* Agent 精简方案

> 只读评估，未做任何安装/删除/修改。待陛下确认后执行。

## 盘点现状

`~/.claude/agents/` 下共 22 个 `engineering-*` + 3 个 `security-*`，全部源自 `msitarzewski/agency-agents` 仓库的复制产物（非符号链接，文件时间戳均为 Jul 6 14:16）。

用户实际项目栈（扫描 `/var/www/`）：
- **demo**：Python 3.11 + FastAPI + SQLite + LLM（Anthropic/OpenAI）+ CLI/Web 双端
- **autojs6-feishu-clock**：AutoJS 脚本（非飞书 Open Platform SDK）
- 其余：captcha-ocr-server、rc-api-server{,2}、rc-platform2、vietguard2、weather-agent、xiaochu、html、i18n_hardening、shy_empower

核心栈 = Python 后端 / LLM / SQLite / 代码质量 / git 纪律 / 文档。

## 三档清单

### 保留（9 个）——与核心栈直接匹配

| Agent | 理由 |
|-------|------|
| `engineering-backend-architect` | Python/FastAPI 后端是 demo 主战场 |
| `engineering-code-reviewer` | CLAUDE.md 强制 review 纪律，高频使用 |
| `engineering-database-optimizer` | SQLite WAL 是核心存储，查询优化刚需 |
| `engineering-devops-automator` | CI/CD、部署自动化，ship/land-and-deploy 流程依赖 |
| `engineering-git-workflow-master` | CLAUDE.md 合并纪律、分支管理 |
| `engineering-minimal-change-engineer` | 与 ponytail 哲学一致，surgical changes 的执行纪律 |
| `engineering-software-architect` | 系统设计、架构决策 |
| `engineering-sre` | 可靠性、监控、canary 发布配套 |
| `engineering-technical-writer` | document-generate 文档生成配套 |

### 待定（5 个）——边界情况，交陛下定夺

| Agent | 倾向 | 待定理由 |
|-------|------|----------|
| `engineering-ai-engineer` | 倾向删 | 内置 `AI Engineer` / `ai-engineer` agent 已覆盖 LLM 应用开发，功能重叠 |
| `engineering-frontend-developer` | 倾向留 | demo 有 Jinja2+HTMX+CSS 的 Web 面板，但前端量轻；若后续 Web 功能加重则留 |
| `engineering-prompt-engineer` | 倾向删 | 内置 `Prompt Engineer` / `prompt-engineer` agent 已覆盖 |
| `engineering-rapid-prototyper` | 倾向删 | 内置 `Rapid Prototyper` agent 已覆盖 |
| `engineering-feishu-integration-developer` | 倾向删 | `autojs6-feishu-clock` 是 AutoJS 脚本，非飞书 Open Platform SDK（bots/bitable/approval）；除非陛下有 SDK 级飞书开发计划 |

### 建议删除（8 个）——无对应项目或严重重叠

| Agent | 删除理由 |
|-------|----------|
| `engineering-ai-data-remediation-engineer` | 数据管道自修复（SLM+语义聚类），无对应项目 |
| `engineering-autonomous-optimization-architect` | 成本治理/影子测试，无对应需求 |
| `engineering-codebase-onboarding-engineer` | 内置 `Explore` / `Codebase Onboarding Engineer` 已覆盖 |
| `engineering-data-engineer` | Spark/dbt/流处理，无数据管道项目 |
| `engineering-multi-agent-systems-architect` | 多 agent 编排架构，当前无 multi-agent 项目 |
| `security-appsec-engineer` | 内置 `Application Security Engineer` 已覆盖 |
| `security-cloud-security-architect` | 无云安全/零信任架构项目 |
| `security-senior-secops` | 内置 `Senior SecOps Engineer` 已覆盖 |

## 汇总

| 档位 | 数量 | 操作 |
|------|------|------|
| 保留 | 9 | 不动 |
| 待定 | 5 | 等陛下拍板 |
| 建议删 | 8 | 确认后删除 |

若待定的 5 个全部按"倾向"执行，最终保留 9 + 1（frontend）= 10 个，删除 12 个。

## 执行前须知（待陛下确认后执行）

1. **备份**：`mkdir -p ~/.claude/backups/agents-<日期>/`，将涉及删除的 `.md` 文件 `cp` 进去
2. **删除**：`rm ~/.claude/agents/<slug>.md`
3. **验证**：`ls ~/.claude/agents/` 确认剩余文件符合预期
4. **可恢复**：如需恢复，从备份目录 `cp` 回来即可；或重新跑 `install.sh --agent <slug>` 从仓库重装

## 文件路径

- 方案：`/home/anonymous/equipment-manager-workspace/iteration-1/eval-1-slimming/with_skill/outputs/plan.md`
- 涉及目录：`~/.claude/agents/`（22 个 engineering-* + 3 个 security-*）
- 参考 skill：`/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/SKILL.md`
- 仓库档案：`/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/references/msitarzewski.md`
