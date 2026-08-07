---
name: persona
description: 维护用户的画像（使用习惯）时用本技能：用户要求「更新我的画像/自学习我的使用习惯/挖掘我的偏好」、或设备评估前需要画像举证时。本技能从 Claude Code session 日志挖掘用户实际使用证据，产出带证据与置信度、经 LLM 蒸馏的候选画像，用户确认后写入画像。画像分人工层（profile.md）与自学习层（profile.d/<hostname>.md 技术栈/业务工作流供 equipment-manager 评估 + profile.d/prefs/<hostname>.md 个人习惯仅备忘；每机一个文件、miner 只写本机 → 多机 git pull 零冲突）。不处理装备安装/评估本身。
version: v1.3.0
---

# 用户画像（User Profile）

维护「用户是谁、用什么、不做什么」的画像，供装备评估、模型配置、任何个性化场景消费。**画像 = 🧠记忆 + 🔍扫描/miner 实测 + 🗣口述交叉验证，单一口述不落地。**

## 触发时机

- 用户要求「更新我的画像 / 自学习我的使用习惯 / 挖掘我的偏好」
- equipment-manager 等下游评估前需要画像举证（消费 `profile.d/`）
- 画像 `updated` 超 90 天需刷新确认

## 数据分层

| 层 | 文件 | 谁写 | 进 git |
|----|------|------|--------|
| **人工层** | `profile.md` | 用户手工维护（结构性事实 + 明确表态） | ✅ |
| **自学习层·评估** | `profile.d/<hostname>.md` | miner 举证 + 用户确认（技术栈/业务工作流，喂 equipment-manager） | ✅ |
| **自学习层·备忘** | `profile.d/prefs/<hostname>.md` | 同上（个人习惯/工具习惯，仅备忘；`profile.d/*.md` 通配符天然不读子目录） | ✅ |
| **纠正状态** | `~/.config/equipment-manager/miner-state.json` | `--correct` 降权记录 | ❌（本机状态） |

**多机零冲突**：miner 只写本机自己的 `profile.d/<hostname>.md` 与 `profile.d/prefs/<hostname>.md`（文件名=主机名），三机各写各的 → `git pull` 无冲突；确认后的画像结论随 git 汇聚，原始日志不离开本机。

## 证据来源分级

🧠记忆记录 / 🔍环境扫描实测（`scripts/scan_profile.sh`）/ 🔍日志挖掘（`scripts/profile_miner.py`）/ 🗣用户口述 / ⚠️推断
**负面偏好不推断**——只有用户明确表态「用不上 X」才记入，标记 🗣。

## 核心流程（更新画像）

```
1. 环境扫描     scripts/scan_profile.sh        （家目录/git/插件/运行时/模型/活跃目录）
2. 日志举证     scripts/profile_miner.py --days 90 --distill
                → 证据绑定的候选线索 JSON（关键词 + 置信度 + top3 证据 session/时间/文本）
3. 蒸馏提炼     Claude 把线索提炼为画像候选：一句话主张 + 判定依据 + ≥1 证据 session 引用；
                证据不足/不确定 → 明确跳过（宁可漏判不编造）；负面偏好不推断
4. 亮候选拍板   逐条展示（主张 + 证据），默认「忽略」；确认 → 写入；纠正 → --correct <关键词>
5. 写入画像     技术栈/业务工作流 → `profile.d/<hostname>.md`（技术栈条目标 🔒稳定）；个人习惯 → `profile.d/prefs/<hostname>.md`；每条带 provenance 证据行 + updated + commit
6. 核对         updated 超 90 天提示确认；人工层条目只在用户明确表态时改动
```

## 证据与防编造

- **蒸馏必须绑定证据**：每条画像候选的「一句话主张」必须引用 `--distill` 输出的至少 1 个证据 session；引用不了证据的主张不得产出（防 AI 编造画像，参考 FastAPI 假证据教训）。
- **provenance 落盘**：写入画像的条目带证据行（项目 · session 文件名 · 时间 · 文本片段），`--verify <关键词>` 重扫日志时可精确回溯到具体 session。
- **确认防 rubber-stamp**：逐条亮候选（主张 + 证据），默认「忽略」——没有明确「确认」就不写入画像。

## 稳定偏好（技术栈不随窗口衰减）

- 技术栈条目（编程语言/框架/数据库/部署目标）确认写入后标记 **🔒稳定**——核心栈是「一贯用什么」，不因最近窗口（90 天）内无新证据就被提议删除
- 衰减只作用于「活动型」条目（业务域/运维等近期活动）；🔒条目除非用户 `--correct` 纠正，否则保留
- 判断标准：技术性（语言/框架/DB/部署）→ 🔒稳定；一次性业务活动 → 活动型

## 命令速查

| 命令 | 用途 |
|------|------|
| `python3 scripts/profile_miner.py --days 90 --distill` | 产出证据绑定的候选线索 JSON（关键词 + 置信度 + top3 证据 session/时间/文本），供 LLM 蒸馏提炼画像候选 |
| `--verify <关键词>` | 证据追溯：不足 --min-sessions 个 session，**或被纠正降权/置信度跌破 --min-confidence** 即 FAIL（防编造 + 防纠正失效） |
| `--correct <关键词>` | 纠正降权（写 miner-state.json） |
| `--self-test` | 核心逻辑自检（过滤/分词/置信度） |
| `--json` | 结构化候选画像证据 |
| `bash scripts/scan_profile.sh` | 环境扫描（家目录/git/插件/运行时/模型） |

**内置噪声过滤**（miner 自动执行，无需手动）：排除 SDK 批量重放（`entrypoint=sdk-*`、首行 `queue-operation` 的评测会话，且**文件层排除不占扫描预算**）、`<task-notification>` 注入块、子代理 SendMessage 回传/任务派发文本——只保留用户真实交互输入，防止评测夹具/脚本注入污染画像证据。分词层过滤中文口语弱词（这个/里面/什么意思）与代码残留（src/data/traceback 片段），避免「什么都记」挤占真实画像信号。**这是 token 层过滤；`--distill` 之上再由 LLM 蒸馏做语义层判定（是否真画像信号），两层结合根治「什么都记」。**

## 置信度公式与参数

```
confidence = min(1.0, 支持session数/3) × 衰减因子 × correctionPenalty^纠正次数
衰减因子   = max(0.1, 1 − 距最近证据天数 / (2 × preferenceDecayDays))
```

| 参数 | 默认 | CLI | 说明 |
|------|------|-----|------|
| preferenceDecayDays | 90 | `--decay-days` | 无新证据过期天数 |
| correctionPenalty | 0.5 | `--correction-penalty` | 纠正一次降权倍数 |
| minConfidence | 0.5 | `--min-confidence` | 亮为「建议确认」的置信度下限 |

## 多机注意

- 每台设备跑 `git pull` 拉到共享画像，**本机 miner 只挖本机日志、只写本机 `profile.d/<hostname>.md` + `profile.d/prefs/<hostname>.md`**
- 新设备部署 my-skills（install.sh）即带上画像，`profile.d/` 自动出现
- 评估时画像 = `profile.md`（人工层）+ 顶层 `profile.d/*.md`（技术栈/工作流；`prefs/` 子目录不读，个人习惯不参与评估）

## 设计依据

见 `~/.gstack/projects/mi4646-my-skills/anonymous-main-design-persona-self-learning-20260806-113000.md`（方案 B：半自动、机器举证、用户拍板；吸收 emulo 证据追溯 + tom-swe 置信度/衰减/纠正）。
