# wshobson/agents 技能安装方案

> 目标：从 `~/agents`（wshobson/agents，已 git pull）中挑选适合「Python 后端 + LLM 应用」开发者的高质量 skill，复制到全局 `~/.claude/skills/`。不装软链。

---

## 一、现状盘点

### 已安装的相关 skill（gstack + my-skills）

| 类别 | 已装 |
|------|------|
| Python | python-async-patterns, python-error-handling, python-performance-optimization, python-testing-patterns, python-type-safety, uv-package-manager |
| LLM | rag-implementation, llm-evaluation, prompt-engineering-patterns |
| 数据库 | postgresql |
| 工程流程 | investigate, review, tdd (superpowers), ship, land-and-deploy |
| 调试 | investigate (gstack), smart-debug (superpowers) |
| Bash | bash-defensive-patterns |

### wshobson/agents 仓库结构

- 94 个 plugin，每个 plugin 包含 `agents/` + `skills/` + `commands/`
- skill 格式：`<plugin>/skills/<skill-name>/SKILL.md`，带 frontmatter（name + description + when-to-use）
- 安装方式：把 `<skill-name>/` 整个目录复制到 `~/.claude/skills/`

---

## 二、推荐安装清单

### Tier 1 — 强烈推荐（直接填补能力空白）

#### 1. `llm-finetuning` 整个 plugin（10 skills + 3 agents + 2 commands）

**理由**：陛下做 LLM 应用，微调是迟早的事。这套 skill 覆盖完整生命周期，且每个 skill 明确标注了上下游衔接关系（"assumes X already routed here"），质量明显高于平均水平。目前全局没有任何微调相关 skill。

| 组件 | 路径 | 用途 |
|------|------|------|
| finetuning-method-selection | `llm-finetuning/skills/finetuning-method-selection/` | 路由器：是否微调？SFT/DPO/GRPO/预训练？ |
| eval-harness-first | `llm-finetuning/skills/eval-harness-first/` | Phase 0：先建评估套件再训练 |
| dataset-curation | `llm-finetuning/skills/dataset-curation/` | 数据准备、chat template、sequence packing |
| lora-qlora-recipes | `llm-finetuning/skills/lora-qlora-recipes/` | LoRA/QLoRA 超参最佳实践 |
| preference-optimization | `llm-finetuning/skills/preference-optimization/` | DPO/ORPO/KTO/SimPO 选择与调参 |
| grpo-rlvr-training | `llm-finetuning/skills/grpo-rlvr-training/` | GRPO + RLVR（可验证奖励的强化学习） |
| checkpoint-promotion | `llm-finetuning/skills/checkpoint-promotion/` | 四阶段上线门禁（drift/paired/forgetting） |
| quantized-export | `llm-finetuning/skills/quantized-export/` | GGUF/FP8/merged safetensors 导出 |
| trace-to-training-data | `llm-finetuning/skills/trace-to-training-data/` | 评估 trace → 训练数据飞轮 |
| vision-sft | `llm-finetuning/skills/vision-sft/` | VLM 视觉微调 |
| llm-finetuning-architect | `llm-finetuning/agents/llm-finetuning-architect.md` | agent：微调架构师 |
| llm-finetuning-eval-engineer | `llm-finetuning/agents/llm-finetuning-eval-engineer.md` | agent：评估工程师 |
| llm-finetuning-training-engineer | `llm-finetuning/agents/llm-finetuning-training-engineer.md` | agent：训练工程师 |
| finetune | `llm-finetuning/commands/finetune.md` | command：启动微调 |
| promote-checkpoint | `llm-finetuning/commands/promote-checkpoint.md` | command：上线 checkpoint |

#### 2. `python-development` 中的增量 skills（9 skills + 1 agent）

**理由**：陛下已装 6 个 python skill，但还缺配置管理、可观测性、容错、资源管理等——这些在 QQ 音乐项目中都有实际对应（config.toml 配置系统、loguru 日志、httpx timeout + 指数退避、async context manager）。

| 组件 | 路径 | 与项目的关联 |
|------|------|-------------|
| python-configuration | `python-development/skills/python-configuration/` | 项目用 config.toml + settings dataclass，直接相关 |
| python-observability | `python-development/skills/python-observability/` | 项目用 loguru + rich，可参考结构化日志/metrics 模式 |
| python-resilience | `python-development/skills/python-resilience/` | 项目有 httpx timeout + 指数退避，直接对应 |
| python-resource-management | `python-development/skills/python-resource-management/` | 项目大量 async context manager（QQMusicClient） |
| python-background-jobs | `python-development/skills/python-background-jobs/` | 项目有后台任务（task_manager.py + SSE） |
| python-design-patterns | `python-development/skills/python-design-patterns/` | 设计原则参考（KISS、SoC、组合优于继承） |
| python-anti-patterns | `python-development/skills/python-anti-patterns/` | code review checklist |
| python-code-style | `python-development/skills/python-code-style/` | ruff/mypy 配置参考 |
| python-project-structure | `python-development/skills/python-project-structure/` | 项目组织参考 |
| python-pro | `python-development/agents/python-pro.md` | agent：Python 专家（与已装的 python-pro agent 可能重复，需检查） |

#### 3. `llm-application-dev` 中的增量 skills（4 skills + 2 agents）

**理由**：陛下已有 RAG、LLM eval、prompt engineering，但缺 embedding 策略、混合搜索、向量索引调优——这些是 RAG 系统的下一层深化。项目当前用 SQLite，但如果未来引入向量搜索，这些 skill 直接可用。

| 组件 | 路径 | 用途 |
|------|------|------|
| embedding-strategies | `llm-application-dev/skills/embedding-strategies/` | 嵌入模型选择、维度、批处理 |
| hybrid-search-implementation | `llm-application-dev/skills/hybrid-search-implementation/` | 稀疏+稠密混合搜索 |
| similarity-search-patterns | `llm-application-dev/skills/similarity-search-patterns/` | 相似度搜索模式 |
| vector-index-tuning | `llm-application-dev/skills/vector-index-tuning/` | 向量索引调优（HNSW/IVF/PQ） |
| ai-engineer | `llm-application-dev/agents/ai-engineer.md` | agent：AI 工程师 |
| vector-database-engineer | `llm-application-dev/agents/vector-database-engineer.md` | agent：向量数据库工程师 |

---

### Tier 2 — 可选（有参考价值但非刚需）

#### 4. `api-scaffolding/fastapi-templates`（1 skill）

**理由**：项目用 FastAPI，但已成熟。这个 skill 适合新建 FastAPI 项目时参考。如果陛下不常新建项目，可跳过。

| 组件 | 路径 |
|------|------|
| fastapi-templates | `api-scaffolding/skills/fastapi-templates/` |

#### 5. `machine-learning-ops`（2 skills + 3 agents + 1 command）

**理由**：ML pipeline 和推荐系统 pipeline。陛下做 AI 应用，如果涉及推荐系统或 ML 训练 pipeline 可装。当前项目不涉及，但未来可能。

| 组件 | 路径 |
|------|------|
| ml-pipeline-workflow | `machine-learning-ops/skills/ml-pipeline-workflow/` |
| recsys-pipeline-architect | `machine-learning-ops/skills/recsys-pipeline-architect/` |
| data-scientist | `machine-learning-ops/agents/data-scientist.md` |
| ml-engineer | `machine-learning-ops/agents/ml-engineer.md` |
| mlops-engineer | `machine-learning-ops/agents/mlops-engineer.md` |
| ml-pipeline | `machine-learning-ops/commands/ml-pipeline.md` |

---

### Tier 3 — 不推荐（与已装 skill 重复或不匹配）

| Plugin | 原因 |
|--------|------|
| debugging-toolkit | 已有 gstack `/investigate` + superpowers `smart-debug`，功能重叠 |
| tdd-workflows | 已有 superpowers TDD 三件套，功能重叠 |
| shell-scripting/bash-defensive-patterns | 已装同名 skill |
| database-design/postgresql | 已装 gstack `postgresql` |
| backend-development | 微服务/CQRS/saga——项目是单体，暂不需要 |
| data-engineering | airflow/dbt/spark——不匹配 |
| 前端/移动端/区块链/游戏/SEO | 完全不匹配 |

---

## 三、安装命令

### 复制脚本（只读方案，未执行）

```bash
# Tier 1.1: llm-finetuning 整个 plugin
cp -r ~/agents/plugins/llm-finetuning/skills/* ~/.claude/skills/
cp -r ~/agents/plugins/llm-finetuning/agents/* ~/.claude/agents/
# commands 需手动放到 ~/.claude/commands/（如目录存在）

# Tier 1.2: python-development 增量（跳过已装的 6 个）
for s in python-configuration python-observability python-resilience \
         python-resource-management python-background-jobs \
         python-design-patterns python-anti-patterns python-code-style \
         python-project-structure; do
  cp -r ~/agents/plugins/python-development/skills/$s ~/.claude/skills/
done

# Tier 1.3: llm-application-dev 增量（跳过已装的 3 个）
for s in embedding-strategies hybrid-search-implementation \
         similarity-search-patterns vector-index-tuning; do
  cp -r ~/agents/plugins/llm-application-dev/skills/$s ~/.claude/skills/
done

# Tier 2（可选）
cp -r ~/agents/plugins/api-scaffolding/skills/fastapi-templates ~/.claude/skills/
cp -r ~/agents/plugins/machine-learning-ops/skills/* ~/.claude/skills/
cp -r ~/agents/plugins/machine-learning-ops/agents/* ~/.claude/agents/
```

### 安装后验证

```bash
# 确认 skill 数量
ls ~/.claude/skills/ | wc -l
# 预期新增：10 (finetuning) + 9 (python 增量) + 4 (llm 增量) + 1 (fastapi) + 2 (mlops) = 26 skills

# 确认 agent 数量
ls ~/.claude/agents/ | wc -l
# 预期新增：3 (finetuning) + 1 (python-pro, 可能重复) + 2 (llm) + 3 (mlops) = 9 agents

# 重启 Claude Code 后验证 skill 是否被识别
# 在 Claude Code 中输入 / 看是否出现新 skill
```

---

## 四、风险与注意事项

1. **命名冲突**：`python-pro` agent 可能与已装的 `python-pro`（gstack 或 my-skills）冲突。安装前先 `ls ~/.claude/agents/ | grep python-pro` 检查。

2. **skill 质量参差**：wshobson/agents 是社区仓库，skill 质量不如 gstack 经过实战验证。建议安装后先用 `/skill-name` 触发几次，看实际效果。

3. **context 占用**：每个 skill 被触发时会加载到 context。装太多不用的 skill 会浪费 context window。建议只装 Tier 1，Tier 2 按需再装。

4. **commands 目录**：Claude Code 的 commands 目录是 `~/.claude/commands/`，不是 `~/.claude/skills/`。安装 commands 需确认目录存在。

5. **后续更新**：复制方式意味着 `~/agents` git pull 后不会自动同步。需要定期手动重新复制，或改用脚本自动化。

---

## 五、总结

| 优先级 | 数量 | 价值 |
|--------|------|------|
| Tier 1（强烈推荐） | 23 skills + 6 agents + 2 commands | 填补微调、Python 工程化、向量搜索三大空白 |
| Tier 2（可选） | 3 skills + 3 agents + 1 command | FastAPI 模板 + ML pipeline，非刚需 |
| Tier 3（不推荐） | — | 与已装 skill 重复或不匹配 |

**建议**：先装 Tier 1（26 个组件），用一周后再决定是否加 Tier 2。
