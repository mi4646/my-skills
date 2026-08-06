# wshobson/agents 增量评估方案

## 一、盘点本地现状

### 全局 `~/.claude/skills/` 已装（来自 wshobson/agents 的符号链接，共 15 个）

| 本地名 | 仓库源 |
|--------|--------|
| api-design-principles | backend-development |
| architecture-decision-records | documentation-generation |
| architecture-patterns | backend-development |
| bash-defensive-patterns | shell-scripting |
| llm-evaluation | llm-application-dev |
| openapi-spec-generation | documentation-generation |
| postgresql | database-design |
| prompt-engineering-patterns | llm-application-dev |
| python-async-patterns | python-development/async-python-patterns |
| python-error-handling | python-development |
| python-performance-optimization | python-development |
| python-testing-patterns | python-development |
| python-type-safety | python-development |
| rag-implementation | llm-application-dev |
| uv-package-manager | python-development |

### 项目级 `/var/www/demo/.claude/skills/` 已装（同源符号链接，共 18 个）

与全局高度重叠，额外含：design-system-patterns、responsive-design、visual-design-foundations（均为 ui-design 域，前端设计相关）。

## 二、识别增量（近 90 天新增 skill）

`git log --diff-filter=A --since="90 days"` 筛出以下**新增 plugin/skill**：

| 日期 | Plugin | 新增 skill | 域 |
|------|--------|-----------|-----|
| 2026-07-19 | pptx-deck-creation | 5 个（pptx-deck-context, pptx-quality-gates, pptx-reference-deck-analysis, pptx-slide-specification, pptx-visual-assets） | 演示文稿 |
| 2026-07-14 | **llm-finetuning** | **10 个**（checkpoint-promotion, dataset-curation, eval-harness-first, finetuning-method-selection, grpo-rlvr-training, lora-qlora-recipes, preference-optimization, quantized-export, trace-to-training-data, vision-sft） | **LLM 微调** |
| 2026-07-08 | hermes-tweet | 1 个（hermes-tweet） | 社交发布 |
| 2026-07-08 | **skill-forge-essentials** | **3 个**（ai-debt-detector, session-guard, visual-edit-precision） | **开发辅助** |
| 2026-06-12 | **before-you-build** | **1 个**（before-you-build） | **产品预检** |
| 2026-06-11 | file-conversion | 1 个（file-conversion） | 文件转换 |
| 2026-05-25 | social-publishing | 1 个（social-publishing） | 社交发布 |
| 2026-05-22 | multi-harness marketplace | 仅给已有 plugin 补 details.md 引用，无新 skill | — |
| 2026-05-17 | machine-learning-ops | 1 个（recsys-pipeline-architect） | 推荐系统 |
| 2026-05-12 | ship-mate | 1 个（scan） | 发布 |

## 三、查重

新增 skill 与本地已装 15 个**无任何重叠**。全部为首次出现。

## 四、三档筛选（基于用户真实项目栈：Python 后端 + LLM 应用）

### 推荐安装（与核心栈强匹配）

| Skill | 来源 plugin | 推荐理由 |
|-------|------------|----------|
| **eval-harness-first** | llm-finetuning | 微调前的评估体系搭建——golden set、grader、judge calibration。用户做 LLM 应用，评估是核心能力，且与已装的 `llm-evaluation` 互补（后者偏 prompt/RAG 评估，这个偏 fine-tuning 评估） |
| **dataset-curation** | llm-finetuning | SFT/DPO/KTO 数据准备、ChatML 格式化、sequence packing、合成数据防 collapse。用户若走向微调，这是必经之路 |
| **lora-qlora-recipes** | llm-finetuning | LoRA/QLoRA 超参配置最佳实践（target_modules=all-linear、rank/alpha 选择）。当前微调的事实标准 |
| **finetuning-method-selection** | llm-finetuning | 微调方法路由（SFT vs DPO vs GRPO vs KTO）。决策入口，装了它才能串起整个 llm-finetuning 流程 |
| **ai-debt-detector** | skill-forge-essentials | AI 生成代码后的专项债务审计——失败模式、孤儿资源、边界用例、幻觉包。用户日常 LLM 辅助开发直接受益 |
| **session-guard** | skill-forge-essentials | 长会话保护（>40 tool calls 预警、context compaction 后规则锚定）。对 agent 开发和长任务场景实用 |

### 待定（边界情况，交陛下定夺）

| Skill | 来源 plugin | 说明 |
|-------|------------|------|
| **before-you-build** | before-you-build | 产品/功能风险预检（demand/positioning/monetization/retention/trust/distribution 七维）。对独立开发决策有价值，但不是技术刚需。陛下若常用 Claude 做产品构思可装 |
| **preference-optimization** | llm-finetuning | DPO/ORPO/KTO 偏好优化。如果陛下计划做偏好对齐训练就装，否则 SFT 三件套（eval + dataset + lora）已够用 |
| **grpo-rlvr-training** | llm-finetuning | GRPO/RLVR 强化学习微调。更进阶，适合有验证器可打分场景（如代码生成、数学）。当前项目不太需要 |

### 不推荐（与用户栈无关）

| Skill | 来源 plugin | 排除理由 |
|-------|------------|----------|
| pptx-deck-creation 全系列（5 个） | pptx-deck-creation | PPT 制作，用户不做演示文稿自动化 |
| hermes-tweet | hermes-tweet | 社交媒体发布，不相关 |
| social-publishing | social-publishing | 社交发布，不相关 |
| file-conversion | file-conversion | 通用文件转换，太泛，无特定价值 |
| recsys-pipeline-architect | machine-learning-ops | 推荐系统架构，用户不做推荐系统 |
| ship-mate/scan | ship-mate | 已有 gstack `/ship` + `/review`，功能重叠 |
| visual-edit-precision | skill-forge-essentials | 视觉编辑精度，面向 UI/CSS 场景，用户是后端 |
| checkpoint-promotion, quantized-export, trace-to-training-data, vision-sft | llm-finetuning | 进阶/专项：checkpoint 晋升、量化导出、trace 转训练数据、视觉 SFT。当前阶段非刚需，等实际用到再装 |

## 五、推荐安装清单（6 个）

1. `eval-harness-first` ← `plugins/llm-finetuning/skills/eval-harness-first`
2. `dataset-curation` ← `plugins/llm-finetuning/skills/dataset-curation`
3. `lora-qlora-recipes` ← `plugins/llm-finetuning/skills/lora-qlora-recipes`
4. `finetuning-method-selection` ← `plugins/llm-finetuning/skills/finetuning-method-selection`
5. `ai-debt-detector` ← `plugins/skill-forge-essentials/skills/ai-debt-detector`
6. `session-guard` ← `plugins/skill-forge-essentials/skills/session-guard`

## 六、安装说明（复制方式）

陛下指定用复制方式。安装命令：

```bash
# llm-finetuning 四件套
cp -r /home/anonymous/agents/plugins/llm-finetuning/skills/eval-harness-first ~/.claude/skills/
cp -r /home/anonymous/agents/plugins/llm-finetuning/skills/dataset-curation ~/.claude/skills/
cp -r /home/anonymous/agents/plugins/llm-finetuning/skills/lora-qlora-recipes ~/.claude/skills/
cp -r /home/anonymous/agents/plugins/llm-finetuning/skills/finetuning-method-selection ~/.claude/skills/

# skill-forge-essentials 二件套
cp -r /home/anonymous/agents/plugins/skill-forge-essentials/skills/ai-debt-detector ~/.claude/skills/
cp -r /home/anonymous/agents/plugins/skill-forge-essentials/skills/session-guard ~/.claude/skills/
```

### 验证

```bash
for s in eval-harness-first dataset-curation lora-qlora-recipes finetuning-method-selection ai-debt-detector session-guard; do
  [ -f "$HOME/.claude/skills/$s/SKILL.md" ] && echo "OK: $s" || echo "MISSING: $s"
done
```

### 注意事项

- 复制方式意味着仓库 `git pull` 后这些 skill **不会自动更新**，需手动重新 `cp -r` 覆盖
- 复制不产生符号链接，永不断链，完全独立于仓库路径
- 若后续想切回符号链接方式：先 `rm -rf ~/.claude/skills/<name>`，再 `ln -s`

## 七、可选扩展（待定区，陛下拍板）

如果陛下对微调方向感兴趣，可追加安装：
- `preference-optimization` — DPO/ORPO 偏好对齐
- `grpo-rlvr-training` — GRPO 强化学习微调
- `before-you-build` — 产品风险预检
