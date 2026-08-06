# 精简方案：engineering-* agent 三档清单

> 生成时间：2026-08-04 ｜ 方式：真实扫描本机 ｜ 状态：**仅清单与方案，未删改任何文件，等你拍板**

## 一、先说扫描到的真实情况（别凭记忆）

1. **`~/.claude/agents/` 当前是空的** —— 你印象里"装了一堆 engineering agent"，但这 15 个 agent 现在不在 agents 目录里，而是躺在今天的备份目录 `~/.claude/backups/agents-20260804/`（2026-08-04 10:26 生成）。同目录还躺着 6 个 `security-*` agent（不在本次精简范围，先不动）。
2. **来源**：全部来自 `msitarzewski/agency-agents`（git remote = github.com/msitarzewski/agency-agents.git），本地 clone 在 `~/agency-agents/engineering/`。备份文件与源仓库 **14/15 逐字节一致**；唯一例外是 `engineering-solidity-smart-contract-engineer.md` 与源有差异（可能你本地改过）。
3. **本机真实项目栈**（`/var/www` 扫描）：以 **Python 后端为主**（rc-api-server / rc-api-server2 / rc-platform2 / shy_empower / vietguard2 / xiaochu / weather-agent / captcha-ocr-server，Django/FastAPI + Celery），配少量 JS 项目（i18n_hardening、autojs6-feishu-clock 飞书打卡脚本）。**没有任何** WordPress / Drupal / 固件 / 区块链 / 嵌入式 / 微信小程序 / PHP-Filament / 网络设备项目。
4. **结论先行**：已装的 15 个全是垂直领域特化 agent，和你"太多太杂"的感受一致 —— 其中 **7 个的领域在本机完全不存在**，另有 7 个方向沾边但无当前项目支撑，仅 1 个勉强算通用兜底。

## 二、三档清单

### 保留（1 个）—— 建议留

| Agent | 理由 |
|---|---|
| `engineering-senior-developer` | 15 个里唯一通用型开发角色（资深实现专家）。虽描述偏 Laravel/Three.js，但可作为日常开发兜底 agent；本机 Python 主力任务它能顶上。若你觉得它太偏 Laravel 而想降级为待定，说一声即可。 |

### 待定（7 个）—— 每项都给了明确留/删倾向

| Agent | 现状判断 | 明确倾向 |
|---|---|---|
| `engineering-email-intelligence-engineer` | AI 数据管线方向，与 weather-agent 等 agent 弱相关，但本机没有任何邮件处理项目 | **倾向删** |
| `engineering-incident-response-commander` | 方法论类（事故响应/SLO/on-call），跟代码栈无关 | **倾向删**；仅当你本人负责生产运维时留 |
| `engineering-it-service-manager` | ITIL 4 服务管理方法论，同上 | **倾向删**；仅当你做 IT 服务管理时留 |
| `engineering-mobile-app-builder` | autojs6-feishu-clock 是 Android 自动化脚本，不是原生 App 开发；本机无 App 项目 | **倾向删**；未来做 App 再装 |
| `engineering-voice-ai-integration-engineer` | 语音 ASR 管线，与现有 captcha-ocr-server（图像 OCR）同属 AI 管线但方向不同 | **倾向删**；若计划做语音再留 |
| `engineering-wechat-mini-program-developer` | 项目是**飞书**（AutoJS6）不是微信小程序。且源仓库里有更贴合的 `engineering-feishu-integration-developer` 但**未安装** | **倾向删**；若你要飞书方向，应换装 feishu 那个而不是留这个 |
| `engineering-solidity-smart-contract-engineer` | 本机无任何区块链项目；且此文件与源仓库有差异（疑似你改过） | **倾向删**；如果你改过想留，告诉我你改了什么 |

### 删除（7 个）—— 领域在本机项目栈中完全不存在

| Agent | 删除理由 |
|---|---|
| `engineering-cms-developer` | Drupal/WordPress 主题与插件，/var/www 无任何 CMS 项目 |
| `engineering-drupal-shopping-cart` | Drupal Commerce 电商，无 Drupal 项目 |
| `engineering-wordpress-shopping-cart` | WooCommerce 电商，无 WordPress 项目 |
| `engineering-embedded-firmware-engineer` | ESP32/STM32 固件，栈无嵌入式 |
| `engineering-filament-optimization-specialist` | Filament PHP 后台，栈无 PHP |
| `engineering-network-engineer` | Cisco/Juniper/Palo Alto 网络设备，无网络项目 |
| `engineering-orgscript-engineer` | OrgScript 语法/AST，无相关项目 |

**合计：保留 1 + 待定 7 + 删 7 = 15。**

## 三、执行方案（等你确认，现在不动手）

按技能硬闸门：**你没说"删"，我就不动任何文件。** 你确认后我再执行，方式如下：

1. **备份**：全部 15 个已在 `~/.claude/backups/agents-20260804/`（今天已统一备份，不是 mv .bak 临时改名）。确认删除的，从 `~/.claude/agents/`（或备份）移除，备份再保留一段时间确认无碍后清理。
2. **保留/待定中确认留下的**：从备份复制回 `~/.claude/agents/`（当前是空的）。
3. **确认删除的**：不再复制回 agents 目录；备份目录里的文件在 N 天后清理（N 由你定）。
4. **附加建议（换血，可选）**：删除后建议从源仓库 `~/agency-agents/engineering/` 装回真正贴合本机栈的 agent，如 `engineering-backend-architect`、`engineering-ai-engineer`，以及飞书方向的 `engineering-feishu-integration-developer` —— 删掉 7 个用不上的，补 2-3 个用得上的是这轮精简的完整闭环。

## 四、请你拍板

一次选一个就好：
- **A**：按"保留 1 + 待定 7 全倾向删 + 删 7"执行（最终留 1 个）？
- **B**：待定里某几个你想留（点名），我调整后再执行？
- **C**：先只删"删除"档的 7 个，待定档再想想？
