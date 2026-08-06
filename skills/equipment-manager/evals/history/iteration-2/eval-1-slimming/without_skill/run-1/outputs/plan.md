# ~/.claude/agents engineering-* 精简方案

> 共 19 个 `engineering-*.md` agent。以下按 **保留 / 待定 / 删除** 三档分类。

---

## 一、保留（4 个）

这些 agent 在内置 agent 列表中没有同名替代，且定位清晰、使用场景明确。

| 文件名 | 名称 | 保留理由 |
|--------|------|----------|
| `engineering-ai-data-remediation-engineer.md` | AI Data Remediation Engineer | 独特定位：自愈数据管线 + 语义聚类修复，无内置替代 |
| `engineering-codebase-onboarding-engineer.md` | Codebase Onboarding Engineer | 独特定位：代码库新人引导，只读溯源，无内置替代 |
| `engineering-database-optimizer.md` | Database Optimizer | 专注 DB 性能（EXPLAIN、索引、连接池），比 Backend Architect 更聚焦 |
| `engineering-multi-agent-systems-architect.md` | Multi-Agent Systems Architect | 独特定位：多 agent 管线拓扑/容错/信任治理，当前项目正用多 agent 架构 |

---

## 二、待定（5 个）

这些 agent 有价值但存在重叠或低频使用风险，由陛下最终定夺。

| 文件名 | 名称 | 待定理由 | 建议 |
|--------|------|----------|------|
| `engineering-autonomous-optimization-architect.md` | Autonomous Optimization Architect | 定位独特（LLM 自动 A/B 路由 + FinOps 护栏），但极 niche，日常几乎用不到 | 若不做 LLM 成本优化项目可删 |
| `engineering-feishu-integration-developer.md` | Feishu Integration Developer | 飞书平台深度集成专家，极 niche | 若当前项目不用飞书可删；若用则保留 |
| `engineering-minimal-change-engineer.md` | Minimal Change Engineer | 理念与 ponytail 高度重叠（最小 diff、反 scope creep） | ponytail 已覆盖此角色，可删 |
| `engineering-prompt-engineer.md` | Prompt Engineer | 有价值，但 `prompt-engineering-patterns` skill 已覆盖大部分场景 | 若常做 prompt 迭代可保留 |
| `engineering-ai-engineer.md` | AI Engineer | 内置已有同名 agent（见下方删除分析），本地版本内容更丰富 | 二选一，建议保留本地版 |

---

## 三、删除（10 个）

这些 agent 与内置 agent 完全同名重复，或与已有 skill 高度重叠。

| 文件名 | 名称 | 删除理由 |
|--------|------|----------|
| `engineering-backend-architect.md` | Backend Architect | **内置同名 agent 已存在**。本地版与内置版 description 几乎一致 |
| `engineering-code-reviewer.md` | Code Reviewer | **内置同名 agent 已存在** + `review` skill + `code-review` skill 三重覆盖 |
| `engineering-data-engineer.md` | Data Engineer | **内置同名 agent 已存在** |
| `engineering-devops-automator.md` | DevOps Automator | **内置同名 agent 已存在** |
| `engineering-frontend-developer.md` | Frontend Developer | **内置同名 agent 已存在** |
| `engineering-git-workflow-master.md` | Git Workflow Master | **内置同名 agent 已存在** |
| `engineering-rapid-prototyper.md` | Rapid Prototyper | **内置同名 agent 已存在** |
| `engineering-software-architect.md` | Software Architect | **内置同名 agent 已存在** |
| `engineering-sre.md` | SRE | **内置同名 agent 已存在** |
| `engineering-technical-writer.md` | Technical Writer | **内置同名 agent 已存在** + `document-generate` skill 覆盖 |

---

## 四、总结

| 档位 | 数量 | 操作 |
|------|------|------|
| 保留 | 4 | 不动 |
| 待定 | 5 | 等陛下确认 |
| 删除 | 10 | 确认后 `rm` |
| **合计** | **19** | 精简后剩 **4~9** 个 |

### 删除依据说明

10 个建议删除的 agent 全部满足同一条件：**内置 agent 列表（Claude Code 自带）中已有完全同名的 agent**。本地 `~/.claude/agents/` 中的版本与内置版 description 高度一致，属于冗余安装。保留它们不会报错，但会增加 agent 列表噪音，降低选择效率。

### 待定的 5 个需要陛下回答的问题

1. **Autonomous Optimization Architect** — 当前或近期有 LLM 成本优化 / A/B 路由项目吗？没有 → 删
2. **Feishu Integration Developer** — 当前项目用飞书吗？不用 → 删
3. **Minimal Change Engineer** — ponytail 已覆盖此理念，还需要独立 agent 吗？不需要 → 删
4. **Prompt Engineer** — 经常需要独立做 prompt 迭代/测试吗？不经常 → 删（skill 够用）
5. **AI Engineer** — 要保留本地版（内容更丰富）还是用内置版？二选一

---

*方案由只读检查生成，未修改任何文件。等陛下确认后执行删除。*
