---
name: persona
description: 维护用户的画像（使用习惯）时用本技能：用户要求「更新我的画像/自学习我的使用习惯/挖掘我的偏好」、或设备评估前需要画像举证时。本技能从 Claude Code session 日志挖掘用户实际使用证据，产出带证据与置信度的候选画像，用户确认后写入画像。画像分人工层（profile.md）与自学习层（profile.d/<hostname>.md，每机一个文件、miner 只写本机 → 多机 git pull 零冲突）。不处理装备安装/评估本身。
version: v1.1.0
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
| **自学习层** | `profile.d/<hostname>.md` | miner 举证 + 用户确认后写入 | ✅ |
| **纠正状态** | `~/.config/equipment-manager/miner-state.json` | `--correct` 降权记录 | ❌（本机状态） |

**多机零冲突**：miner 只写本机自己的 `profile.d/<hostname>.md`（文件名=主机名），三机各写各的 → `git pull` 无冲突；确认后的画像结论随 git 汇聚，原始日志不离开本机。

## 证据来源分级

🧠记忆记录 / 🔍环境扫描实测（`scripts/scan_profile.sh`）/ 🔍日志挖掘（`scripts/profile_miner.py`）/ 🗣用户口述 / ⚠️推断
**负面偏好不推断**——只有用户明确表态「用不上 X」才记入，标记 🗣。

## 核心流程（更新画像）

```
1. 环境扫描     scripts/scan_profile.sh        （家目录/git/插件/运行时/模型/活跃目录）
2. 日志举证     scripts/profile_miner.py --days 90 --evaluate
                产出候选条目（session 数/置信度/状态），✅建议确认 即机器举证
3. 亮候选拍板   确认 → 写入 profile.d/<hostname>.md；忽略 → 丢弃；纠正 → --correct <关键词>
4. 写入画像     本机自学习文件 + 标记 🔍miner 证据 + 用户确认 + updated + commit
5. 核对         updated 超 90 天提示确认；人工层条目只在用户明确表态时改动
```

## 命令速查

| 命令 | 用途 |
|------|------|
| `python3 scripts/profile_miner.py --days 90 --evaluate` | 产出候选画像条目（session 数/置信度/状态） |
| `--verify <关键词>` | 证据追溯：不足 --min-sessions 个 session 即 FAIL（防编造） |
| `--correct <关键词>` | 纠正降权（写 miner-state.json） |
| `--self-test` | 核心逻辑自检（过滤/分词/置信度） |
| `--json` | 结构化候选画像证据 |
| `bash scripts/scan_profile.sh` | 环境扫描（家目录/git/插件/运行时/模型） |

**内置噪声过滤**（miner 自动执行，无需手动）：排除 SDK 批量重放（`entrypoint=sdk-*`、首行 `queue-operation` 的评测会话）与 `<task-notification>` 注入块——只保留用户真实交互输入，防止评测夹具/脚本注入污染画像证据。

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

- 每台设备跑 `git pull` 拉到共享画像，**本机 miner 只挖本机日志、只写本机 `profile.d/<hostname>.md`**
- 新设备部署 my-skills（install.sh）即带上画像，`profile.d/` 自动出现
- 评估时画像 = `profile.md`（人工层）+ 全部 `profile.d/*.md`（自学习层汇总）

## 设计依据

见 `~/.gstack/projects/mi4646-my-skills/anonymous-main-design-persona-self-learning-20260806-113000.md`（方案 B：半自动、机器举证、用户拍板；吸收 emulo 证据追溯 + tom-swe 置信度/衰减/纠正）。
