# 精简 `~/.claude/agents/` 下 engineering-* agents 方案

## 背景

本地 `~/.claude/agents/` 共 22 个 `engineering-*.md`（另有 3 个 `security-*` 不在本次范围），均来自 msitarzewski/agency-agents 仓库的复制产物（非符号链接）。用户反馈「太多太杂」，要求出三档清单，不实际删除。

## 用户真实项目栈（`/var/www/demo`）

- Python 3.11+ / async / FastAPI / SQLite (WAL) / Jinja2+HTMX
- LLM 集成（Anthropic + OpenAI，httpx 直调）
- LangGraph 状态机、Selenium+OpenCV 验证码
- CLI: Click + Rich；Web: FastAPI + SSE
- 单一项目：QQ 音乐歌单整理器（CLI + Web 面板）
- 已有 Ponytail 纪律 + 完整 superpowers 流程 + 大量专用 agent（python-pro、sql-pro、backend-development-*、pr-review-toolkit:*、prompt-engineer 等）

## 关键观察

1. **大量重叠**：这 19 个 engineering-* agent 与系统内置的更专用 agent 高度重叠（python-pro、sql-pro、backend-development-backend-architect、pr-review-toolkit:code-reviewer、prompt-engineer、Technical Writer、SRE、Git Workflow Master 等）。保留全部 = 同一能力多个入口，增加选择成本。
2. **多数未被使用**：用户项目单一、技术栈聚焦，大部分 agent 的专长（Spark/dbt、Feishu、自愈数据管线、影子压测、多 agent 治理）在本项目中无场景。
3. **体积成本**：22 个文件合计 ~230KB，每次会话都作为 agent 类型列表注入上下文，增加 token 消耗与选择噪音。

## 三档清单

### 保留（5 个）—— 与核心栈直接匹配、且无更优内置替代

| 文件 | 理由 |
|------|------|
| `engineering-ai-engineer.md` | LLM 集成是该项目的核心，AI Engineer 直接覆盖 |
| `engineering-prompt-engineer.md` | 项目重度依赖 prompt 工程（classify/explain/interview），专用 prompt-engineer 虽存在但该 agent 仍有独立价值 |
| `engineering-minimal-change-engineer.md` | 与 Ponytail 纪律高度契合，作为「反过度工程」的显式守卫 |
| `engineering-backend-architect.md` | FastAPI 后端是该项目的主体，通用后端架构视角有用 |
| `engineering-software-architect.md` | 系统级设计决策（pipeline v2、interview 状态机、配置改革）需要 |

### 待定（6 个）—— 边界情况，交陛下拍板

| 文件 | 倾向 | 说明 |
|------|------|------|
| `engineering-code-reviewer.md` | 倾向删 | 与 `Code Reviewer`、`pr-review-toolkit:code-reviewer`、`code-review-preshipment` 三重重叠 |
| `engineering-database-optimizer.md` | 倾向删 | SQLite 单文件 WAL，`sql-pro` + `Database Optimizer` 已覆盖 |
| `engineering-technical-writer.md` | 倾向删 | `Technical Writer` + `documentation-generation-*` 已覆盖 |
| `engineering-git-workflow-master.md` | 倾向删 | `Git Workflow Master` 已覆盖，且项目有 ship/land-and-deploy 流程 |
| `engineering-frontend-developer.md` | 倾向保留 | HTMX+Jinja2 前端虽轻，但 Web 面板是用户可见面，需要前端视角 |
| `engineering-sre.md` | 倾向删 | 单用户本地工具，SRE 场景弱；但可留作未来部署参考 |

### 建议删除（8 个）—— 与项目栈无关或严重过杀

| 文件 | 删除理由 |
|------|---------|
| `engineering-feishu-integration-developer.md` | 项目无任何飞书集成，14KB 纯噪音 |
| `engineering-data-engineer.md` | Spark/dbt/lakehouse 对本项目严重过杀（SQLite + 简单 ETL） |
| `engineering-multi-agent-systems-architect.md` | 29KB！LangGraph 状态机 ≠ 多 agent 治理体系，过杀 |
| `engineering-ai-data-remediation-engineer.md` | 自愈数据管线 + Ollama 空气隔离，本项目无此场景 |
| `engineering-autonomous-optimization-architect.md` | 影子压测 + 成本护栏，单用户工具无需 |
| `engineering-devops-automator.md` | 项目无 CI/CD 配置、无云基础设施 |
| `engineering-rapid-prototyper.md` | 项目已过原型阶段（有完整 pipeline v2 + Web 面板） |
| `engineering-codebase-onboarding-engineer.md` | 单人项目，onboarding 场景不存在 |

## 备份方案

执行前统一备份到 `~/.claude/backups/agents-engineering-20260804/`：

```bash
mkdir -p ~/.claude/backups/agents-engineering-20260804
cp ~/.claude/agents/engineering-*.md ~/.claude/backups/agents-engineering-20260804/
```

恢复：`cp ~/.claude/backups/agents-engineering-20260804/*.md ~/.claude/agents/`

## 执行步骤（待陛下确认后）

1. 备份全部 19 个 engineering-* 文件到上述目录
2. 删除「建议删除」8 个文件
3. 「待定」6 个按陛下回复处理（默认按倾向执行）
4. 保留 5 个不动
5. 验证：`ls ~/.claude/agents/ | grep engineering-` 确认剩余符合预期

## 预期收益

- agent 类型列表瘦身：19 → 5~11 个，减少上下文噪音
- 磁盘节省：约 100~150KB（视待定档最终选择）
- 选择成本下降：同能力多入口问题消除

## 未覆盖

- `security-*` 3 个文件不在本次范围（用户只提 engineering-*）
- 符号链接化改造（当前为复制产物，未来若想自动跟新仓库可考虑）
