# wshobson/agents 仓库更新评估方案

> 评估日期：2026-08-04
> 评估范围：仓库近 90 天新增 skill（`git log --diff-filter=A`）
> 用户栈：Python 后端 + LLM 应用（`/var/www/demo` 项目：FastAPI + Anthropic/OpenAI + SQLite）
> 安装偏好：**复制安装**（`cp -r`），不要软链

---

## 一、盘点本地现状

### 全局 `~/.claude/skills/`（已装 80 项）

**来自 wshobson/agents 的符号链接（15 项，已装）**：
- `python-development` 域（5）：python-async-patterns、python-error-handling、python-performance-optimization、python-testing-patterns、python-type-safety
- `llm-application-dev` 域（3）：llm-evaluation、prompt-engineering-patterns、rag-implementation
- `backend-development` 域（2）：api-design-principles、architecture-patterns
- `documentation-generation` 域（2）：architecture-decision-records、openapi-spec-generation
- `database-design` 域（1）：postgresql
- `shell-scripting` 域（1）：bash-defensive-patterns
- `python-development` 域（1）：uv-package-manager

**其他来源**：gstack 系列（browse、ship、review 等约 40 项）、my-skills 系列（playlist-organizer、weekly-report 等约 15 项）、find-skills、learned 等。

### 项目级 `/var/www/demo/.claude/skills/`（20 项，全部为 wshobson 软链）
与全局高度重叠，是项目作用域的同源安装。

**结论**：Python 后端 + LLM 应用的核心知识包已齐全。新增评估应聚焦「仓库新增且本地未覆盖」的 skill。

---

## 二、识别仓库新增内容（近 90 天 `git log --diff-filter=A`）

新增 SKILL.md 共 27 个，分布在 8 个新 plugin：

| Plugin | 新增 skill 数 | 域 |
|--------|--------------|---|
| `llm-finetuning` | 10 | LLM 微调 |
| `pptx-deck-creation` | 5 | PPT 制作 |
| `dgx-spark-ops` | 3 | DGX Spark 硬件运维 |
| `skill-forge-essentials` | 3 | 元技能（行为守卫） |
| `before-you-build` | 1 | 产品预检 |
| `file-conversion` | 1 | 文件格式转换 |
| `machine-learning-ops` | 1 | 推荐系统 pipeline |
| `hermes-tweet` / `social-publishing` / `ship-mate` | 各 1 | 社交/发布/扫描 |

---

## 三、三档筛选

### 保留（强烈推荐安装）

#### 1. `llm-finetuning` 插件（10 个 skill）— 整体推荐

| Skill | 用途 | 与用户栈的关联 |
|-------|------|---------------|
| `finetuning-method-selection` | SFT/DPO/GRPO 路由决策 | 项目用 Anthropic/OpenAI API，未来若微调自有模型必用 |
| `eval-harness-first` | 评估 harness 先行（golden set + grader） | 与项目 `evaluate.py` 精度评估思路一致，可补强 |
| `dataset-curation` | 训练数据格式化/打包/验证 | ChatML/ShareGPT 格式规范，做 LLM 应用的基础功 |
| `lora-qlora-recipes` | LoRA/QLoRA 超参配置（target_modules、rank/alpha） | 2025-09 "LoRA Without Regret" 最新共识，MLP 层 target |
| `checkpoint-promotion` | 检查点晋升门禁 | 微调后上线的质量关卡 |
| `preference-optimization` | DPO/ORPO/KTO 偏好优化 | 项目分类 prompt 若做偏好对齐可用 |
| `grpo-rlvr-training` | GRPO/RLVR 强化学习微调 | 进阶，但有 verifier 场景（如分类准确率）适用 |
| `quantized-export` | 量化导出 | 本地部署 SLM 时用 |
| `trace-to-training-data` | 生产 trace → 训练数据 | 项目 LLM 调用日志回流训练 |
| `vision-sft` | 视觉 SFT | 边缘，但插件整体性强 |

**推荐理由**：用户栈核心是 LLM 应用，本地已有 `llm-evaluation`、`prompt-engineering-patterns`、`rag-implementation`，但**微调方向完全空白**。这套 skill 构成完整微调生命周期（路由→数据→训练→评估→导出），且内容质量高（引用 Schulman 2025、xAI 开源算法等一手资料）。10 个 skill 作为整体插件安装，内部互相引用（如 `dataset-curation` 引用 `finetuning-method-selection`），拆开装会破坏交叉引用。

#### 2. `skill-forge-essentials/session-guard` — 推荐

**用途**：长会话（>40 tool calls）行为自守卫，防止 context compaction 后指令遗忘。
**推荐理由**：项目 CLAUDE.md 纪律严格（TDD→review→subagent），长会话中 agent 遗忘规则是真实痛点。纯行为协议，无依赖，零成本。与项目已有的 `superpowers` 体系互补。

#### 3. `skill-forge-essentials/ai-debt-detector` — 推荐

**用途**：AI 生成代码后的专项债务审计（失败模式/孤儿资源/边缘输入/幻觉包）。
**推荐理由**：项目强调准确率 + 开发纪律，AI 生成代码的隐性债务（missing error handling、orphaned resources）正是 `review` skill 的盲区（review 偏风格/正确性，ai-debt 专攻 AI 特有失败模式）。与项目 `superpowers:verification-before-completion` 互补。

#### 4. `before-you-build` — 推荐

**用途**：动手前的产品/功能风险预检（demand/positioning/monetization/retention/trust/distribution 七维）。
**推荐理由**：用户是独立开发者（QQ 音乐工具），做功能前快速过一遍风险清单有价值。输出格式精简（5 行决策导向），不阻塞开发。与 `office-hours`（产品构思）互补——office-hours 发散，before-you-build 收敛。

### 待定（交用户定夺）

#### 5. `machine-learning-ops/recsys-pipeline-architect` — 倾向不装

**用途**：推荐系统六阶段 pipeline（Source→Hydrator→Filter→Scorer→Selector→SideEffect），源自 xAI For You 算法。
**倾向理由**：内容是好的（六阶段框架通用），但用户当前项目是「歌单分类工具」，不是推荐系统。若未来做「智能歌单推荐」可装。占位不大，装了也无害。

#### 6. `file-conversion` — 倾向不装

**用途**：通过 changethisfile.com 免费 API 做 999 种格式转换。
**倾向理由**：实用但与核心栈无关。依赖外部服务（changethisfile.com），文件上传到第三方有隐私考量。用户若偶尔需要格式转换，直接用 ffmpeg/libreoffice 本地转更可控。

### 建议不装

| Skill | 理由 |
|-------|------|
| `pptx-deck-creation`（5 个） | PPT 制作，与 Python 后端/LLM 栈无关 |
| `dgx-spark-ops`（3 个） | DGX Spark 硬件运维，用户无此硬件 |
| `hermes-tweet` | 推文发布，非用户需求 |
| `social-publishing` | 社交发布，非用户需求 |
| `ship-mate/scan` | 依赖 understand-anything + context-mode 插件，用户已有 gstack 体系 |
| `llm-finetuning/vision-sft` | 视觉 SFT，用户无视觉任务（可随插件整体装，不单独拆） |

---

## 四、推荐安装清单

| # | Skill / Plugin | 源路径 | 安装方式 | 理由 |
|---|---------------|--------|---------|------|
| 1 | `llm-finetuning`（整体 10 skill） | `/home/anonymous/agents/plugins/llm-finetuning/` | `cp -r` | 微调全生命周期，补全 LLM 栈空白 |
| 2 | `session-guard` | `/home/anonymous/agents/plugins/skill-forge-essentials/skills/session-guard/` | `cp -r` | 长会话行为守卫，防 context compaction 遗忘 |
| 3 | `ai-debt-detector` | `/home/anonymous/agents/plugins/skill-forge-essentials/skills/ai-debt-detector/` | `cp -r` | AI 生成代码专项债务审计 |
| 4 | `before-you-build` | `/home/anonymous/agents/plugins/before-you-build/skills/before-you-build/` | `cp -r` | 动手前风险预检，5 行决策输出 |

**总计**：13 个 skill（1 个插件整体 + 3 个独立 skill）

---

## 五、安装命令（复制方式，用户确认后执行）

```bash
# 备份（按 equipment-manager 流程）
mkdir -p ~/.claude/backups/2026-08-04

# 1. llm-finetuning 插件整体复制
cp -r /home/anonymous/agents/plugins/llm-finetuning ~/.claude/skills/llm-finetuning

# 2. session-guard
cp -r /home/anonymous/agents/plugins/skill-forge-essentials/skills/session-guard ~/.claude/skills/session-guard

# 3. ai-debt-detector
cp -r /home/anonymous/agents/plugins/skill-forge-essentials/skills/ai-debt-detector ~/.claude/skills/ai-debt-detector

# 4. before-you-build
cp -r /home/anonymous/agents/plugins/before-you-build/skills/before-you-build ~/.claude/skills/before-you-build

# 验证
for d in llm-finetuning session-guard ai-debt-detector before-you-build; do
  [ -d ~/.claude/skills/$d ] && echo "OK: $d" || echo "MISSING: $d"
done
```

**关于复制安装的说明**：
- 用户明确要求复制方式，本方案严格遵循
- 复制的优点：完全独立，不依赖 `/home/anonymous/agents/` 路径存在，永不断链
- 复制的代价：仓库更新需手动重装（`cp -r` 覆盖）；占磁盘约 2-3 MB（可忽略）
- 注意：`llm-finetuning` 插件内部 skill 互相引用（如 `lora-qlora-recipes` 引用 `dataset-curation`），整体复制保持内部引用完整

---

## 六、执行前需用户确认

1. 推荐清单（4 项）是否同意？有无想增删的？
2. 「待定」2 项（recsys-pipeline-architect、file-conversion）是否要装？
3. 确认后执行上述 `cp -r` 命令
