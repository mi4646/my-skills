# OpenCode Go 官方参考数据

来源：https://opencode.ai/docs/go/

## 提供商配置

OpenCode Go 的 provider ID 是 `opencode-go`，模型 ID 格式 `opencode-go/<model-id>`。

配置示例：
```json
{
  "provider": {
    "opencode-go": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "OpenCode Go",
      "models": {
        "deepseek-v4-pro": { "name": "DeepSeek V4 Pro" },
        "qwen3.7-max": { "name": "Qwen3.7 Max" }
      }
    }
  }
}
```

注意：MiniMax M3、Qwen3.7 Max/Plus/Plus(>256K) 等使用 Anthropic 消息格式，需用 `@ai-sdk/anthropic` npm 包。

## 模型 ID 列表

| 显示名 | 模型 ID |
|--------|---------|
| Grok 4.5 | grok-4.5 |
| GLM-5.2 | glm-5.2 |
| GLM-5.1 | glm-5.1 |
| Kimi K3 | kimi-k3 |
| Kimi K2.7 Code | kimi-k2.7-code |
| Kimi K2.6 | kimi-k2.6 |
| MiMo-V2.5 | mimo-v2.5 |
| MiMo-V2.5 Pro | mimo-v2.5-pro |
| MiniMax M3 | minimax-m3 |
| MiniMax M2.7 | minimax-m2.7 |
| Qwen3.7 Max | qwen3.7-max |
| Qwen3.7 Plus | qwen3.7-plus |
| Qwen3.6 Plus | qwen3.6-plus |
| DeepSeek V4 Pro | deepseek-v4-pro |
| DeepSeek V4 Flash | deepseek-v4-flash |

## 使用限制

- 5 小时限制：**$12** 使用额度
- 每周限制：**$30** 使用额度
- 每月限制：**$60** 使用额度

限制以美元价值定义。实际请求数取决于模型定价。

## 各模型使用额度与价格

### 预估请求数（按模型定价折算）

| 模型 | 每5小时 | 每周 | 每月 | 月使用额度 | 备注 |
|------|---------|------|------|-----------|------|
| Grok 4.5 | 120 | 300 | 600 | $15 | 低额度模型 |
| GLM-5.2 | 880 | 2,150 | 4,300 | $60 | |
| GLM-5.1 | 880 | 2,150 | 4,300 | $60 | |
| Kimi K3 | 110 | 250 | 490 | $15 | 低额度模型 |
| Kimi K2.7 Code | 1,350 | 4,630 | 9,250 | $60 | |
| Kimi K2.6 | 1,150 | 2,880 | 5,750 | $60 | |
| MiMo-V2.5 | 30,100 | 75,200 | 150,400 | $60 | |
| MiMo-V2.5 Pro | 3,250 | 8,150 | 16,300 | $15 | 低额度模型 |
| MiniMax M3 | 3,200 | 8,000 | 16,000 | $60 | |
| MiniMax M2.7 | 3,400 | 8,500 | 17,000 | $60 | |
| Qwen3.7 Max | 950 | 2,390 | 4,770 | $60 | |
| Qwen3.7 Plus | 4,300 | 10,800 | 21,600 | $60 | ≤256K input |
| Qwen3.7 Plus (>256K) | — | — | — | $60 | 价格贵3倍 |
| Qwen3.6 Plus | 3,300 | 8,200 | 16,300 | $60 | |
| DeepSeek V4 Pro | 3,450 | 8,550 | 17,150 | $15 | 低额度模型 |
| DeepSeek V4 Flash | 31,650 | 79,050 | 158,150 | $60 | |

### 定价详情（每百万 token）

| 模型 | 输入 | 输出 | 缓存读 | 缓存写 |
|------|------|------|--------|--------|
| Grok 4.5 | $2.00 | $6.00 | $0.30 | — |
| GLM-5.2 | $1.40 | $4.40 | $0.26 | — |
| Kimi K3 | $3.00 | $15.00 | $0.30 | — |
| Kimi K2.7 Code | $0.95 | $4.00 | $0.19 | — |
| MiMo-V2.5 | $0.14 | $0.28 | $0.0028 | — |
| MiMo-V2.5 Pro | $0.435 | $0.87 | $0.003625 | — |
| MiniMax M3 | $0.30 | $1.20 | $0.06 | — |
| MiniMax M2.7 | $0.30 | $1.20 | $0.06 | $0.375 |
| Qwen3.7 Max | $2.50 | $7.50 | $0.50 | $3.125 |
| Qwen3.7 Plus (≤256K) | $0.40 | $1.60 | $0.04 | $0.50 |
| Qwen3.7 Plus (>256K) | $1.20 | $4.80 | $0.12 | $1.50 |
| DeepSeek V4 Pro | $0.435 | $0.87 | $0.003625 | — |
| DeepSeek V4 Flash | $0.14 | $0.28 | $0.0028 | — |

## 单次请求成本估算

基于官方 token 消耗模式（每次请求约 1,100 输入 / 71,500 缓存 / 220-300 输出 tokens）。

| 模型 | 约单次成本 | 备注 |
|------|-----------|------|
| Grok 4.5 | ≈$0.10 | 昂贵 |
| Kimi K3 | ≈$0.109 | 昂贵 |
| Qwen3.7 Max | ≈$0.0126 | 中等 |
| DeepSeek V4 Pro | ≈$0.0035 | 便宜 |
| DeepSeek V4 Flash | ≈$0.00038 | 近乎免费 |
| MiMo-V2.5 | ≈$0.0004 | 近乎免费 |

## 低额度模型

以下模型月使用额度仅为 $15（其他模型为 $60），配额显著更少：
- Grok 4.5（120/5h）
- Kimi K3（110/5h）
- MiMo-V2.5 Pro（3,250/5h — 注意不是配额低而是单价高）
- DeepSeek V4 Pro（3,450/5h — 同上）

官方说明：这些模型尚未获得批量折扣，"获取的使用额度仍会略高于直接向模型提供商付费"。

## 计量方式

OpenCode Go 按**美元价值**计算配额，而非请求次数。请求次数是根据模型定价折算的预估值。用户实际配置时看到的配额可能略有不同（取决于实际 token 用量），但上述表格是官方给出的预估参考值。

## 超出限制

用户可在控制台启用"使用余额"选项，超出 Go 配额后回退使用 Zen 余额。

## Agent 配置格式（参考）

在 OpenCode 中配置不同 agent 使用不同模型：

```json
{
  "agent": {
    "build": {
      "mode": "primary",
      "model": "opencode-go/deepseek-v4-pro"
    },
    "plan": {
      "mode": "primary",
      "model": "opencode-go/qwen3.7-max"
    }
  }
}
```

## API 端点

- 大部分模型（OpenAI 兼容）：`https://opencode.ai/zen/go/v1/chat/completions`
- MiniMax M3 / Qwen 系列（Anthropic 格式）：`https://opencode.ai/zen/go/v1/messages`
