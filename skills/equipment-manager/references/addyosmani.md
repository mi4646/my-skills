# 仓库档案：addyosmani/agent-skills

## 基本信息
- **作者**：Addy Osmani（Google Chrome 团队）
- **本地路径**：`~/skills/addyosmani/`（2026-08-07 归位，install.sh ④段管理）
- **git remote**：`https://github.com/addyosmani/agent-skills.git`
- **版本**：0.6.6（MIT）
- **规模**：24 skill + 4 agent + 8 slash command + hooks + evals 框架
- **形态**：Claude Code marketplace 插件（`plugin.json` + `.claude-plugin/marketplace.json`）

## 目录结构
- `skills/<name>/SKILL.md`：24 个核心 skill，按 SDLC 六阶段组织（Define/Plan/Build/Verify/Review/Ship + Meta）
- `agents/`：4 个 agent 人格（code-reviewer / test-engineer / security-auditor / web-performance-auditor）
- `.claude/commands/`：8 个 slash command（/spec /plan /build /test /review /webperf /code-simplify /ship）
- `hooks/`：session 生命周期 hooks（SDD 缓存、simplify-ignore）
- `references/`：仓库级共享清单（performance / security / accessibility / observability / testing / def-of-done）
- `evals/`：skill 触发/路由评测框架（`node scripts/run-evals.js`）
- `docs/`：各平台安装指南（Claude/Cursor/Codex/Copilot/Gemini/OpenCode…）

## 安装机制（marketplace 插件形态，与单 skill 档案不同）
1. **Marketplace 整体装**（官方推荐，全量）：`/plugin marketplace add addyosmani/agent-skills` + `/plugin install agent-skills@addy-agent-skills`
2. **npx skills CLI**（可选单 skill）：`npx skills add addyosmani/agent-skills --skill <name>`
3. **手动复制**：`cp -r skills/<name> ~/.claude/skills/<name>`（2026-08-07 已装两项采用此方式）

## 坑位与约定
- 仓库自带 CLAUDE.md 明确：**别把整个仓库复制进全局配置**，可复用资产是 `skills/`
- 单 skill 安装缺仓库级 `references/` 共享清单（官方 issue #361）；`doubt-driven-development` 引用 `references/orchestration-patterns.md`，单装缺文件
- 与本地 gstack 的 `api-and-interface-design` **完全同名同任务**（description 几乎逐字相同）——查重时注意
- 24 个 skill 中 20 个与本地 superpowers/gstack/commit-commands 同任务（2026-08-07 评估结论）
- 上游固定 `~/skills/addyosmani/`，install.sh ④段按独立 skill 目录形态管理（非插件目录）；`--list` 支持第三字段统计

## 评估记录（2026-08-07）
- **已装（复制）**：`context-engineering`（画像核心工作流命中、本地空白）、`interview-me`（用户纠正「哲学重复」类比后提升为建议；任务=校验想法≠推进流程）
- **拍板不装**：`doubt-driven-development`（与 superpowers verification-before-completion 部分重叠 + 单装缺 references）
- **其余 20 skill + 4 agent 不装**：本地已覆盖（同任务）/ 用户工作流用不上
- 同日已登记 my-skills `install.sh`（EQUIP + ④安装段 + THIRD-PARTY.md/README 同步）
