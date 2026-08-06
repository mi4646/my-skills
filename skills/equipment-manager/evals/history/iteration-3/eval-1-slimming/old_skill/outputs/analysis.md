# 精简方案：engineering-* agent 三档清单

> 生成时间：2026-08-04 ｜ 方式：真实扫描本机，不凭记忆 ｜ 状态：**仅清单与方案，未删改任何文件，等【陛下】拍板**

## 一、扫描到的真实情况（先对账，再判断）

1. **`~/.claude/agents/` 当前是空的**。陛下印象里"装了一堆 engineering agent"，实际这 15 个 engineering-* agent 现在不在 agents 目录，而在今天的统一备份目录 `~/.claude/backups/agents-20260804/`（2026-08-04 10:26 生成）。同目录还躺着 7 个 `security-*` agent（不在本次精简范围，先不动）。
2. **来源确认为 `msitarzewski/agency-agents`**（git remote = github.com/msitarzewski/agency-agents.git，本地 clone `~/agency-agents/engineering/`）。备份文件与源仓库**逐字节比对：14/15 完全一致**；唯一例外是 `engineering-solidity-smart-contract-engineer.md`——本地副本比源仓库少了一处链名（源含 "XDC"，本地已删），疑似陛下改过，删除前需确认。
3. **本机真实项目栈**（`/var/www` 实扫 11 个项目）：
   - **Python 后端为主**：rc-api-server / rc-api-server2（FastAPI/Celery API 服务）、rc-platform2 / shy_empower / vietguard2（Django + manage.py）、xiaochu（LLM 助手）、weather-agent（手写 AI Agent）、captcha-ocr-server（Python + ONNX OCR）、demo（AI 歌单整理，pyproject+requirements）；
   - **AI/LLM 方向**：weather-agent、xiaochu、demo 三个 AI 项目，Agent 循环 + LLM 应用；
   - **DevOps**：多项目带 Dockerfile / docker-compose；
   - **少量前端**：i18n_hardening（Node + nginx 前端，明确 i18n 加固）、autojs6-feishu-clock（AutoJS6 飞书打卡脚本，Android 自动化，非原生 App）；
   - **全盘确认无**：WordPress / Drupal / Filament / PHP（无任何 *.php、composer.json）、原生移动 App、区块链/Solidity、嵌入式固件（ESP32/STM32）、网络设备（Cisco/Juniper）、邮件处理、语音 ASR、微信小程序、OrgScript、ITIL/事故响应类流程。
4. **结论先行**：这 15 个全是垂直领域特化 agent，与陛下"太多太杂"的感受一致。按真实栈划分：**7 个领域在本机完全不存在（建议删），7 个方向沾边但无当前项目支撑（待定，均倾向删），仅 1 个算通用兜底（保留）**。

## 二、三档清单

### 保留（1 个）—— 建议留

| Agent | 理由 |
|---|---|
| `engineering-senior-developer` | 15 个里唯一通用型开发角色（资深实现专家）。虽然描述偏 Laravel/Livewire/Three.js，但作为日常开发兜底 agent，Python 主力任务也能顶上；本机无对应专项 agent，留一个通用兜底最划算。若陛下觉得它偏 Laravel 想降为待定，说一声即可。 |

### 待定（7 个）—— 每项都给明确留/删倾向，不糊弄

| Agent | 现状判断（对照 /var/www） | 明确倾向 |
|---|---|---|
| `engineering-email-intelligence-engineer` | AI 数据管线方向，与 weather-agent 等弱相关，但本机没有任何邮件处理项目 | **倾向删**；无邮件需求 |
| `engineering-incident-response-commander` | 方法论类（事故响应/SLO/on-call），与代码栈无关 | **倾向删**；仅当陛下本人负责生产运维时才留 |
| `engineering-it-service-manager` | ITIL 4 服务管理方法论，同上 | **倾向删**；仅当陛下做 IT 服务管理时才留 |
| `engineering-mobile-app-builder` | autojs6-feishu-clock 是 AutoJS6 Android 自动化脚本，**不是**原生 App 开发；本机无 App 项目 | **倾向删**；未来做 App 再装 |
| `engineering-voice-ai-integration-engineer` | 语音 ASR 管线，与 captcha-ocr-server（图像 OCR）同属 AI 管线但方向不同，本机无语音项目 | **倾向删**；若计划做语音再留 |
| `engineering-wechat-mini-program-developer` | 项目是**飞书**（AutoJS6），不是微信小程序；且源仓库里有更贴合的 `engineering-feishu-integration-developer` 但**未安装** | **倾向删**；若陛下要飞书方向，应换装 feishu 那个而非留这个 |
| `engineering-solidity-smart-contract-engineer` | 本机无任何区块链项目；且此文件与源仓库有差异（本地疑似改过，源含 XDC 本地已删） | **倾向删**；若陛下改过想留，请告知改了什么 |

### 删除（7 个）—— 领域在本机项目栈中完全不存在

| Agent | 删除理由（对照 /var/www 实扫） |
|---|---|
| `engineering-cms-developer` | Drupal/WordPress 主题与插件；/var/www 无任何 CMS/PHP 项目 |
| `engineering-drupal-shopping-cart` | Drupal Commerce 电商；无 Drupal 项目 |
| `engineering-wordpress-shopping-cart` | WooCommerce 电商；无 WordPress 项目 |
| `engineering-embedded-firmware-engineer` | ESP32/STM32/RTOS 固件；栈无嵌入式 |
| `engineering-filament-optimization-specialist` | Filament PHP 后台；栈无 PHP |
| `engineering-network-engineer` | Cisco/Juniper/Palo Alto 网络设备；无网络项目 |
| `engineering-orgscript-engineer` | OrgScript 语法/AST；无相关项目 |

**合计：保留 1 + 待定 7（均倾向删）+ 删除 7 = 15。**

## 三、执行方案（等【陛下】确认，现在不动手）

**硬闸门：陛下没说"删"，就不动任何文件。** 确认后再执行，方式如下：

1. **备份（已就位，未用 mv .bak 临时改名）**：15 个 agent 已统一在 `~/.claude/backups/agents-20260804/`（2026-08-04 统一备份目录）。删除执行时，从该备份目录移除即可，无需额外备份动作。
2. **确认删除的**：不再复制回 `~/.claude/agents/`（当前为空），备份保留 N 天后清理（N 由陛下定）。
3. **确认保留/待定中留下的**：从备份复制回 `~/.claude/agents/`（如仅留 senior-developer，则只复制它一个）。
4. **附加建议（换血，可选）**：删除后建议从源仓库 `~/agency-agents/engineering/` 装回真正贴合本机栈的 agent，如 `engineering-backend-architect`、`engineering-ai-engineer`，以及飞书方向的 `engineering-feishu-integration-developer`——删掉 7 个用不上的，补 2-3 个用得上的是这轮精简的完整闭环。安装方式（软链 vs 复制）到时由陛下拍板。

## 四、请【陛下】拍板（一次选一个即可）

- **A**：按"保留 1 + 待定 7 全删 + 删除 7"执行（最终留 1 个）？
- **B**：待定里某几个想留（点名），我调整后再执行？
- **C**：先只删"删除"档的 7 个，待定档再想想？
