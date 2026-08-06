# 装备评估：wshobson/agents 增量筛选与复制安装方案

> 按《装备管理器》七步方法论执行：盘点 → 增量识别 → 查重 → 三档筛选 → 方案。用户已指定**复制(cp)方式**、仅出方案不执行。
> 评估时间：2026-08-04

---

## ① 盘点本地现状

| 位置 | 现状 |
|------|------|
| `~/.claude/skills/` | 61 个条目：绝大多数为 gstack 生态（gstack、review、qa、spec、ship…）+ `my-skills`（内含来自 mattpocock 的 grill-me / prototype / research / resolving-merge-conflicts）+ find-skills、learned。**无任何 wshobson 系 skill** |
| `~/.claude/agents/` | 空 |
| `~/.claude/plugins/` | `installed_plugins.json` 的 plugins 列表为空；已知 marketplace 有 karpathy-skills、claude-plugins-official、ponytail、claude-hud 等，**wshobson/agents 未接入 marketplace** |
| `/var/www/demo/.claude/skills/` | 档案中记载的 15 个 wshobson 知识包符号链接**已不存在**（当前 .claude 下仅 settings.local.json 与 worktrees），档案「已知实践」已过期 |

结论：本机当前**零** wshobson 系 skill，本次全部候选均为净新增。

## ② 增量识别（git log，近 90 天新增）

- 仓库确认存在：`/home/anonymous/agents`，remote 正确（`https://github.com/wshobson/agents.git`）。
- 依据：`git log --diff-filter=A --since="90 days" --name-only`，只取 `plugins/*/skills/*/SKILL.md`，按插件聚合。

新增插件与 skills（11 个插件、共 31 个 skill）：

| 插件 | 新增 SKILL | 提交日期 |
|------|-----------|---------|
| **llm-finetuning** | checkpoint-promotion、dataset-curation、eval-harness-first、finetuning-method-selection、grpo-rlvr-training、lora-qlora-recipes、preference-optimization、quantized-export、trace-to-training-data、vision-sft（10 个） | 2026-07-14 |
| **dgx-spark-ops** | spark-environment-setup、spark-memory-thermal-ops、spark-training-gotchas（3 个） | 2026-07-14 |
| **pptx-deck-creation** | pptx-deck-context、pptx-quality-gates、pptx-reference-deck-analysis、pptx-slide-specification、pptx-visual-assets（5 个） | 2026-07-19 |
| **skill-forge-essentials** | ai-debt-detector、session-guard、visual-edit-precision（3 个） | 2026-07-08 |
| **machine-learning-ops** | recsys-pipeline-architect（仅此 1 个为新增，ml-pipeline-workflow 为旧有） | 90 天内 |
| **before-you-build** | before-you-build | 90 天内 |
| **file-conversion** | file-conversion | 90 天内 |
| **hermes-tweet** | hermes-tweet | 2026-07-08 |
| **ship-mate** | scan | 90 天内 |
| **social-publishing** | social-publishing | 90 天内 |
| **operating-kit** | （仅 agents，无 skill：code-review-preshipment / deploy-with-verification / prod-logs-health-check / session-start / session-end） | 2026-07-08 |

## ③ 查重

- 逐一对照 `~/.claude/skills/`（61 项）、`~/.claude/plugins/installed_plugins.json`（空）、`/var/www/demo/.claude/skills/`（已无）——**上述 31 个新增 skill 均未本地安装，无同源重复**。
- 无同名或同功能近亲：本地无 llm-evaluation / rag / prompt-engineering 等旧档案记载的知识包残留。
- 结论：推荐清单无需剔除重复项。

## ④ 基于真实需求三档筛选

真实栈扫描（/var/www 下 11 个项目）：`demo`（FastAPI + uvicorn + httpx + playwright，LLM 歌单整理）、`weather-agent`、`captcha-ocr-server`（OCR）、`rc-api-server/rc-api-server2`（FastAPI 后端）、`i18n_hardening`（前端）、`xiaochu`、`vietguard2` 等。核心方向：**Python 后端（FastAPI）+ LLM 应用 + 少量前端/自动化**。无 GPU/Spark、无 PPT 办公、无社媒运营、无产品孵化。

| 档位 | 候选 | 理由 |
|------|------|------|
| **保留（推荐装）** | **llm-finetuning 全套 10 个 skill** | 用户核心栈即 LLM 应用；该套件覆盖微调全生命周期（方法选型→数据清洗→LoRA/QLoRA→eval 先行→偏好优化→GRPO/RLVR→trace 转训练数据→checkpoint 门禁→量化导出→VLM 微调），是 LLM 应用工程师的进阶能力包，与栈直接匹配。若想收敛，最小子集为 `finetuning-method-selection` + `dataset-curation` + `eval-harness-first`（RAG/提示词 vs 微调选型与评估门禁，应用层也适用） |
| **保留（推荐装）** | **ai-debt-detector**（skill-forge-essentials） | 审查 AI 生成代码的脆弱点/债务，与「Python 后端 + AI 辅助开发」强匹配，是对 AI 产出把关的通用工程技能 |
| **保留（推荐装）** | **recsys-pipeline-architect**（machine-learning-ops） | Source→Hydrator→Filter→Scorer→Selector→SideEffect 六段框架直接覆盖「top-K 筛选 / RAG 重排 / 内容推荐」；用户的歌单整理（对歌曲打分发牌）与 weather-agent 正是此类场景 |
| 待定 | **session-guard**（skill-forge-essentials） | 长会话/多步任务行为约束，适合你高频多步开发会话；行为类收益因人而异，倾向装 |
| 待定 | **visual-edit-precision**（skill-forge-essentials） | 面向前端/UI 视觉改动；你偏后端，仅 i18n_hardening 等少量前端，倾向不装 |
| 待定 | **scan**（ship-mate） | 扫描生成 AGENTS.md/project-doc.md；你的仓库已有 CLAUDE.md 体系，边际价值有限，若要做 agent 友好新仓库可装 |
| 建议不装 | before-you-build（产品/创业风险评审） | 面向 founder/PM，非工程栈 |
| 建议不装 | file-conversion（网页转换服务封装） | 一次性工具壳，价值低 |
| 建议不装 | hermes-tweet、social-publishing | 社媒/推特，无对应项目 |
| 建议不装 | dgx-spark-ops（3 个） | 无 GPU/Spark/DGX 基础设施 |
| 建议不装 | pptx-deck-creation（5 个） | 无 PPT 工作流 |
| 超范围说明 | operating-kit | 产出为 agents（非 skills），不符「装到 ~/.claude/skills」需求；若日后想要，`code-review-preshipment` 与 `prod-logs-health-check` 值得考虑装到 ~/.claude/agents |

## ⑤ 澄清点（供定夺，一次一问）

1. **llm-finetuning 装全套 10 个还是最小 3 个子集？**（你当前项目偏「应用层消费 LLM」，若短期无微调/训练计划，3 个评估类即可；装全套也无害，纯增量。）
2. skill-forge-essentials 装 1 个（ai-debt-detector）还是 3 个全装？
3. scan 是否要？

## ⑥ 推荐清单与理由（定稿）

### 强烈推荐（3 个来源、共 12+ 个 skill）
1. `llm-finetuning` 全套 10 个（或最小子集 3 个）— LLM 应用核心栈的微调全生命周期能力包
2. `ai-debt-detector` — AI 生成代码质量把关，Python 后端 + AI 辅助开发强匹配
3. `recsys-pipeline-architect` — top-K/推荐/RAG 重排框架，直接命中歌单整理类项目

### 待定（3 个，倾向顺序：session-guard > scan > visual-edit-precision）
4. `session-guard` — 长会话行为约束，适合高频多步开发
5. `scan` — AGENTS.md 引导，适合新建 agent 友好仓库
6. `visual-edit-precision` — 偏前端，弱匹配

### 建议不装（11 个）
before-you-build、file-conversion、hermes-tweet、social-publishing、dgx-spark-ops×3、pptx-deck-creation×5

## ⑦ 复制(cp)安装方案（不执行）

> 用户指定复制方式、不软链。复制后完全独立于仓库路径，永不断链；仓库更新需手动重装。

```bash
# 0) 备份（本次为净新增、无覆盖，可选）
mkdir -p ~/.claude/backups/20260804 && cp -r ~/.claude/skills ~/.claude/backups/20260804/skills

# 1) llm-finetuning 全套（10 个 skill，每个是独立目录，含 SKILL.md + references/）
for s in /home/anonymous/agents/plugins/llm-finetuning/skills/*/; do
  cp -r "$s" ~/.claude/skills/
done
# 收敛为最小子集时改为逐目录复制：
# cp -r /home/anonymous/agents/plugins/llm-finetuning/skills/finetuning-method-selection ~/.claude/skills/
# cp -r /home/anonymous/agents/plugins/llm-finetuning/skills/dataset-curation ~/.claude/skills/
# cp -r /home/anonymous/agents/plugins/llm-finetuning/skills/eval-harness-first ~/.claude/skills/

# 2) ai-debt-detector
cp -r /home/anonymous/agents/plugins/skill-forge-essentials/skills/ai-debt-detector ~/.claude/skills/

# 3) recsys-pipeline-architect
cp -r /home/anonymous/agents/plugins/machine-learning-ops/skills/recsys-pipeline-architect ~/.claude/skills/

# 4) 待定项（确认后再加）：
# cp -r /home/anonymous/agents/plugins/skill-forge-essentials/skills/session-guard ~/.claude/skills/
# cp -r /home/anonymous/agents/plugins/ship-mate/skills/scan ~/.claude/skills/

# 5) 验证（每个复制目录须含非空 SKILL.md）
for s in ai-debt-detector recsys-pipeline-architect; do
  [ -s ~/.claude/skills/$s/SKILL.md ] && echo "OK: $s" || echo "FAIL: $s"
done
# llm-finetuning 的 10 个子目录按各自 skill 名落到 ~/.claude/skills/，
# 复制前先 ls /home/anonymous/agents/plugins/llm-finetuning/skills/ 核对实际目录名
```

复制方式特性（参考档案 wshobson.md）：`cp -r` 遇符号链接会原样保留链接；本清单源均为真实目录（非链接），复制后为普通目录，完全独立。仓库 git pull 更新后不会自动传播，需手动重跑以上命令。

---

## 附：方法执行对照

- 增量识别 ✅：`git log --diff-filter=A --since="90 days"` 定位 11 插件/31 skill，非罗列全仓库
- 查重 ✅：对照 ~/.claude/skills、plugins 清单、demo 项目，无重复可推
- 复制方案 ✅：按用户指定 cp -r 出安装命令与验证
- 未执行任何安装/删除/改动 ✅
