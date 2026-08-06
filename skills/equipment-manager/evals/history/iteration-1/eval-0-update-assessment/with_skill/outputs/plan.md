# wshobson/agents 新增装备筛选方案

## 一、盘点现状

### 本地已装（来自 wshobson，均为符号链接）

| 来源域 | 已装 skill |
|--------|-----------|
| python-development | python-async-patterns, python-error-handling, python-performance-optimization, python-testing-patterns, python-type-safety, uv-package-manager |
| backend-development | api-design-principles, architecture-patterns |
| database-design | postgresql |
| llm-application-dev | llm-evaluation, prompt-engineering-patterns, rag-implementation |
| documentation-generation | openapi-spec-generation, architecture-decision-records |
| shell-scripting | bash-defensive-patterns |

共 15 个 skill，全部为 `~/.claude/skills/` 下的符号链接。

### 本次 pull 新增 plugin

| Plugin | 类型 | 内容 |
|--------|------|------|
| llm-finetuning | skills x10 | 微调全生命周期（方法选择→数据→训练→导出） |
| skill-forge-essentials | skills x3 | ai-debt-detector, session-guard, visual-edit-precision |
| dgx-spark-ops | skills x3 | NVIDIA DGX Spark 硬件运维 |
| operating-kit | agents x4, skills x0 | 会话生命周期（无 skill 可装） |
| pptx-deck-creation | skills x1 | PPT 生成 |
| hermes-tweet / ciagent | 各 x1 | 社交/CI，不相关 |

### 已存在但未装的候选（旧 plugin 里的遗珠）

python-development 9 个、llm-application-dev 5 个、api-scaffolding 1 个、backend-development 5 个、data-engineering 4 个、machine-learning-ops 2 个。

---

## 二、三档筛选

用户核心栈：**Python 后端 + LLM 应用**（FastAPI + SQLite + Anthropic/OpenAI + LangGraph）。

### 推荐安装（与核心栈强相关）

#### 新增 plugin 中

| Skill | 来源 | 理由 |
|-------|------|------|
| **finetuning-method-selection** | llm-finetuning | 微调入口路由，决定 SFT/DPO/RLVR/是否微调，LLM 应用必备决策框架 |
| **lora-qlora-recipes** | llm-finetuning | LoRA/QLoRA 超参配置最佳实践，微调实操核心 |
| **eval-harness-first** | llm-finetuning | 评估先于训练，与项目已有的 llm-evaluation skill 互补形成闭环 |
| **dataset-curation** | llm-finetuning | 训练数据格式化/校验/chat template，微调必经步骤 |
| **ai-debt-detector** | skill-forge-essentials | AI 生成代码后的隐性债务审计，与项目 ponytail 纪律互补 |
| **session-guard** | skill-forge-essentials | 长会话上下文退化防护，40+ tool call 场景实用 |

#### 旧 plugin 中（一直存在但未装）

| Skill | 来源 | 理由 |
|-------|------|------|
| **fastapi-templates** | api-scaffolding | 项目就是 FastAPI，直接对标 |
| **python-background-jobs** | python-development | Web 后台任务（项目有 task_manager.py），直接对标 |
| **python-observability** | python-development | 结构化日志+指标+追踪，项目 fmt.py+loguru 体系可参考对照 |
| **python-resilience** | python-development | 重试/退避/超时，项目 LLM 调用已有指数退避，可对照补全 |
| **python-resource-management** | python-development | context manager 模式，项目 DB/连接管理直接相关 |
| **embedding-strategies** | llm-application-dev | 嵌入模型选择+分块策略，RAG 前置步骤 |
| **hybrid-search-implementation** | llm-application-dev | 向量+关键词混合检索，RAG 进阶 |
| **langchain-architecture** | llm-application-dev | 项目用 LangGraph，此 skill 覆盖 LangChain 1.x + LangGraph 架构 |

### 待定（边界情况，交陛下定夺）

| Skill | 来源 | 倾向 |
|-------|------|------|
| preference-optimization | llm-finetuning | DPO/ORPO/KTO，有偏好数据时用；暂无偏好数据场景可缓 |
| grpo-rlvr-training | llm-finetuning | RLVR，需可验证奖励信号的场景（代码/数学）；当前项目不涉及 |
| checkpoint-promotion / quantized-export | llm-finetuning | 微调后部署门禁+量化导出；需实际跑微调才有用 |
| trace-to-training-data | llm-finetuning | trace 转训练数据飞轮；需先有 eval harness |
| vector-index-tuning / similarity-search-patterns | llm-application-dev | 向量索引调优；当前项目未用向量数据库 |
| python-design-patterns | python-development | 设计模式通用参考；已有 architecture-patterns 覆盖 |
| python-packaging / python-project-structure | python-development | 打包/项目结构参考；项目结构已稳定 |

### 建议不装

| Skill / Plugin | 理由 |
|----------------|------|
| dgx-spark-ops 全部 | NVIDIA DGX Spark 硬件运维，无对应硬件 |
| visual-edit-precision | 前端/UI 视觉编辑，项目为 CLI+Web 后端 |
| pptx-deck-creation | PPT 生成，不相关 |
| hermes-tweet / ciagent | 社交/CI agent，不相关 |
| operating-kit | 只有 agents 无 skills，且功能与已有 superpowers 重叠 |
| data-engineering 全部 | Airflow/dbt/Spark，项目不涉及 |
| machine-learning-ops 全部 | ML pipeline/MLOps，项目是 LLM 应用非传统 ML |
| backend-development 的 cqrs/event-store/microservices/temporal | 事件源/CQRS/Temporal 工作流，项目为单体 FastAPI+SQLite |
| python-anti-patterns / python-code-style / python-configuration | 偏基础参考，已有 ponytail + 项目纪律覆盖 |

---

## 三、安装方案

### 用户偏好：复制安装（非符号链接）

按 skill 第⑦步，复制方式特点：
- 优点：完全独立，不依赖仓库路径存在，永不断链
- 缺点：仓库更新需手动重装

### 安装命令（待陛下确认后执行）

```bash
# 新增 plugin - llm-finetuning（推荐 4 个核心 skill）
for s in finetuning-method-selection lora-qlora-recipes eval-harness-first dataset-curation; do
  cp -r /home/anonymous/agents/plugins/llm-finetuning/skills/$s ~/.claude/skills/
done

# 新增 plugin - skill-forge-essentials（2 个）
for s in ai-debt-detector session-guard; do
  cp -r /home/anonymous/agents/plugins/skill-forge-essentials/skills/$s ~/.claude/skills/
done

# 旧 plugin 遗珠（8 个）
cp -r /home/anonymous/agents/plugins/api-scaffolding/skills/fastapi-templates ~/.claude/skills/
for s in python-background-jobs python-observability python-resilience python-resource-management; do
  cp -r /home/anonymous/agents/plugins/python-development/skills/$s ~/.claude/skills/
done
for s in embedding-strategies hybrid-search-implementation langchain-architecture; do
  cp -r /home/anonymous/agents/plugins/llm-application-dev/skills/$s ~/.claude/skills/
done
```

### 验证

```bash
# 确认全部为普通目录（非符号链接）且含 SKILL.md
for s in finetuning-method-selection lora-qlora-recipes eval-harness-first dataset-curation \
         ai-debt-detector session-guard \
         fastapi-templates python-background-jobs python-observability python-resilience \
         python-resource-management embedding-strategies hybrid-search-implementation langchain-architecture; do
  if [ -d ~/.claude/skills/$s ] && [ -f ~/.claude/skills/$s/SKILL.md ]; then
    echo "OK: $s"
  else
    echo "FAIL: $s"
  fi
done
```

---

## 四、总结

- **推荐装 14 个**：llm-finetuning 4 核心 + skill-forge 2 + 旧遗珠 8
- **待定 10 个**：微调进阶 + 向量索引 + 基础参考，按需再装
- **不装**：硬件运维、前端视觉、PPT、数据工程、MLOps、CQRS/Temporal 等与核心栈无关的

安装后全局 skill 从 15 → 29（wshobson 来源），加上 gstack/my-skills 等总计约 80+。
