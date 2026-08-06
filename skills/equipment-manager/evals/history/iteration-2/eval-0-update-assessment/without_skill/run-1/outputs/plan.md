# wshobson/agents 新 skill 安装方案

> 只读分析，未做任何安装/修改。本文档为方案，供陛下审阅后决定是否执行。

## 一、分析背景

- **来源仓库**：`~/agents`（wshobson/agents，已 `git pull`）
- **仓库规模**：94 plugins / 203 agents / 175 skills / 109 commands
- **已装全局 skills**：`~/.claude/skills/` 共 70+ 个（含 gstack、my-skills 等）
- **已装的 Python/LLM 相关 skills**：
  - `api-design-principles`、`architecture-patterns`、`postgresql`
  - `python-async-patterns`、`python-error-handling`、`python-performance-optimization`、`python-testing-patterns`、`python-type-safety`
  - `llm-evaluation`、`prompt-engineering-patterns`、`rag-implementation`
  - `uv-package-manager`
- **安装方式**：复制（非软链），目标 `~/.claude/skills/<skill-name>/`

## 二、推荐清单（分三档）

### 第一档：强烈推荐（直接匹配项目技术栈，立即收益）

| # | Skill 名 | 来源 plugin | 推荐理由 |
|---|----------|-------------|----------|
| 1 | `fastapi-templates` | api-scaffolding | 项目 Web 面板用 FastAPI + Jinja2 + HTMX + SSE。该 skill 提供生产级 FastAPI 项目结构、async 模式、依赖注入、中间件、错误处理模板，可直接指导 `app/` 目录重构或新路由编写 |
| 2 | `langchain-architecture` | llm-application-dev | 项目 `interview/` 模块用 LangGraph 构建交互式状态机。该 skill 覆盖 LangChain 1.x + LangGraph StateGraph、agent/memory/tool 集成、多步工作流，是当前项目最缺的架构级指导 |
| 3 | `python-observability` | python-development | 项目用 loguru 文件日志 + rich 终端输出，但缺少结构化日志、指标采集、分布式追踪模式。该 skill 可指导升级现有日志体系，加入 Prometheus 指标、correlation ID 传播 |
| 4 | `python-resilience` | python-development | 项目通过 httpx 调用 LLM API（Anthropic/OpenAI）+ QQ Music API，已有指数退避实现。该 skill 提供完整的重试/退避/超时/熔断/限压模式，可系统性加固外部调用层 |

### 第二档：推荐（LLM 应用深度补充，与已装 skills 形成完整知识体系）

| # | Skill 名 | 来源 plugin | 推荐理由 |
|---|----------|-------------|----------|
| 5 | `embedding-strategies` | llm-application-dev | 已装 `rag-implementation`，但嵌入模型选择（Voyage AI / OpenAI / 开源）、维度权衡、批处理策略未覆盖。该 skill 是 RAG 的自然补充 |
| 6 | `hybrid-search-implementation` | llm-application-dev | 混合搜索（向量 + 关键词 + 重排序）是生产 RAG 的标配，项目未来若引入知识库检索可立即用上 |
| 7 | `vector-index-tuning` | llm-application-dev | HNSW/IVF/PQ 索引策略、参数调优、性能 vs 精度权衡。与 `embedding-strategies` 配套 |
| 8 | `similarity-search-patterns` | llm-application-dev | 相似度搜索模式（余弦/欧氏/内积）、过滤、分页、批查询。与上述三个 skill 构成完整的向量检索知识栈 |
| 9 | `eval-harness-first` | llm-finetuning | 评估框架优先于训练。项目已有 `evaluate.py` 精度评估模块，该 skill 提供 golden set 构建、grader 校准、base-model baseline 的系统方法，可升级现有评估体系 |

### 第三档：可选（通用 Python 工程能力提升，按需安装）

| # | Skill 名 | 来源 plugin | 适用场景 |
|---|----------|-------------|----------|
| 10 | `python-design-patterns` | python-development | SoC/SRP/组合优于继承。代码评审时作为参考标准 |
| 11 | `python-anti-patterns` | python-development | 反模式识别（God class、循环依赖、泄漏抽象）。重构时对照检查 |
| 12 | `python-background-jobs` | python-development | 后台任务模式。项目 `task_manager.py` 已有 SSE 进度推送，可参考更通用的异步任务队列方案 |
| 13 | `python-configuration` | python-development | 配置管理模式。项目已有 `config.toml` + dataclass + env var 回退体系，该 skill 可作为配置重构的参考 |
| 14 | `python-packaging` | python-development | 打包发布（pyproject.toml、wheel、PyPI）。项目用 `pip install -e .`，若未来发布到 PyPI 可参考 |
| 15 | `python-resource-management` | python-development | 上下文管理器、资源释放、连接池。项目有 SQLite WAL + httpx 连接池，可加固资源管理 |
| 16 | `python-code-style` | python-development | 代码风格（Black/Ruff/isort）。项目已有 ruff 配置，该 skill 可作为风格统一的参考 |

### 不推荐安装（项目当前不需要）

| Skill 名 | 来源 plugin | 不推荐原因 |
|----------|-------------|-----------|
| `microservices-patterns` | backend-development | 项目是单体 CLI + Web，无微服务需求 |
| `workflow-orchestration-patterns` | backend-development | Temporal 持久化工作流，项目用 LangGraph 已足够 |
| `cqrs-implementation` | backend-development | CQRS 模式，项目无读写分离需求 |
| `event-store-design` | backend-development | 事件存储，项目用 SQLite 单库 |
| `saga-orchestration` | backend-development | 分布式事务 Saga，项目无跨服务事务 |
| `projection-patterns` | backend-development | 读模型投影，项目无 CQRS 需求 |
| `lora-qlora-recipes` | llm-finetuning | LoRA/QLoRA 微调，项目调用 API 不自训模型 |
| `dataset-curation` | llm-finetuning | 数据集策展，项目无自训数据需求 |
| `finetuning-method-selection` | llm-finetuning | 微调方法选择，项目调用 API 不自训模型 |
| `temporal-python-testing` | backend-development | Temporal 测试，项目不用 Temporal |

## 三、安装命令（待陛下批准后执行）

```bash
# 第一档：强烈推荐（4 个）
for skill in fastapi-templates langchain-architecture python-observability python-resilience; do
  src="/home/anonymous/agents/plugins/*/skills/$skill"
  dst="$HOME/.claude/skills/$skill"
  if [ -d "$src" ]; then
    cp -r "$src" "$dst"
    echo "✓ 已安装 $skill"
  else
    echo "✗ 未找到 $skill"
  fi
done

# 第二档：推荐（5 个）
for skill in embedding-strategies hybrid-search-implementation vector-index-tuning similarity-search-patterns eval-harness-first; do
  src="/home/anonymous/agents/plugins/*/skills/$skill"
  dst="$HOME/.claude/skills/$skill"
  if [ -d "$src" ]; then
    cp -r "$src" "$dst"
    echo "✓ 已安装 $skill"
  else
    echo "✗ 未找到 $skill"
  fi
done

# 第三档：可选（7 个，按需）
for skill in python-design-patterns python-anti-patterns python-background-jobs python-configuration python-packaging python-resource-management python-code-style; do
  src="/home/anonymous/agents/plugins/*/skills/$skill"
  dst="$HOME/.claude/skills/$skill"
  if [ -d "$src" ]; then
    cp -r "$src" "$dst"
    echo "✓ 已安装 $skill"
  else
    echo "✗ 未找到 $skill"
  fi
done
```

## 四、预期收益

### 立即收益（第一档 4 个）
- **FastAPI 开发效率**：`fastapi-templates` 提供生产级项目结构、async 模式、依赖注入模板，减少 `app/` 目录的架构决策成本
- **LangGraph 开发效率**：`langchain-architecture` 直接指导 `interview/` 模块的状态机设计、agent/memory/tool 集成
- **生产可观测性**：`python-observability` 升级 loguru 日志体系，加入结构化日志、指标采集、分布式追踪
- **外部调用鲁棒性**：`python-resilience` 系统性加固 httpx 调用层（LLM API + QQ Music API）的重试/退避/熔断

### 长期收益（第二档 5 个）
- **RAG 知识体系完整化**：与已装的 `rag-implementation` 配套，形成 嵌入 → 索引 → 混合搜索 → 相似度查询 的完整链路
- **评估体系升级**：`eval-harness-first` 提供 golden set + grader 校准方法，可升级现有 `evaluate.py` 精度评估模块

### 工程能力提升（第三档 7 个）
- **代码质量**：设计模式 + 反模式识别，代码评审时作为参考标准
- **工程规范**：配置管理、打包发布、资源管理、代码风格，统一团队开发规范

## 五、风险与注意事项

1. **命名冲突**：已装 skills 中无同名 skill，无覆盖风险
2. **依赖关系**：所有 skill 均为独立 Markdown 文档，无外部依赖
3. **版本更新**：复制安装后需手动 `git pull` + 重新复制以更新
4. **磁盘占用**：每个 skill 约 10-50KB，16 个 skill 总计 < 1MB

## 六、建议执行顺序

1. **先装第一档**（4 个）：立即收益，直接匹配项目技术栈
2. **观察一周**：看是否频繁触发这些 skills，评估实际价值
3. **再装第二档**（5 个）：若项目引入 RAG 或升级评估体系时安装
4. **按需装第三档**（7 个）：若团队需要统一工程规范时安装

## 七、替代方案

若陛下认为一次性安装过多 skills 会增加上下文负担，可考虑：

- **方案 A**：只装第一档 4 个，观察后再决定
- **方案 B**：装第一档 + 第二档共 9 个，第三档按需
- **方案 C**：全装 16 个，通过 `.claude/skills/.gitignore` 或 `settings.json` 控制自动触发条件

**推荐方案 B**：9 个 skills 覆盖项目核心技术栈（FastAPI + LangGraph + LLM API 调用 + RAG + 评估），且不引入项目当前不需要的微服务/Temporal/自训模型等概念。

---

**方案完毕，请陛下审阅。**
