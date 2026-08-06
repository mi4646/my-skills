# 接入新仓库方案：`~/new-skill-repo`（agents + skills 混合）

> 按 `equipment-manager` 技能「接入新仓库」五步流程出具方案。
> 本方案只读、不执行；所有改动在用户拍板后由技能主流程落地。

---

## 0. 背景与目标

- 用户本地已接入 3 个仓库：`msitarzewski/agency-agents`、`wshobson/agents`、`mattpocock/skills`。
- 新仓库位于 `~/new-skill-repo`，**agents 与 skills 混合**，需要按装备管理方法论归档。
- 目标：把「新仓库情报」沉淀到 `references/` 档案，让后续「盘点 / 安装 / 精简」复用同一套流程，方法论不动。

---

## 1. 接入流程总览（五步）

| # | 步骤 | 产出 |
|---|------|------|
| 1 | 确认来源 | 拿到 `git remote -v` 的真实 URL，避免「本地目录名 ≠ 仓库名」 |
| 2 | 摸清结构 | 目录布局、命名约定、安装机制（复制 vs 符号链接）、是否有官方脚本 |
| 3 | 建档案 | 在 `references/` 下新建一个 markdown 档案 |
| 4 | 登记 | 在 SKILL.md「支持的仓库」表格加一行 |
| 5 | 更新 description | 在 SKILL.md frontmatter 的「已接入」列表追加新仓库名 |

---

## 2. 步骤 1 — 确认来源

```bash
git -C ~/new-skill-repo remote -v
# 预期输出：origin  https://github.com/<author>/<repo>.git (fetch)
#            origin  https://github.com/<author>/<repo>.git (push)
```

- 记下 `<author>` 与 `<repo>`，档案文件名与登记表格都依赖这两个值。
- 若 remote 为空 → 让用户确认是否忘记 `git remote add`，**不凭目录名猜测**。

---

## 3. 步骤 2 — 摸清结构

按以下清单逐项探查，结果写进档案：

```bash
# 顶层目录
ls ~/new-skill-repo

# agents 与 skills 的分布
find ~/new-skill-repo -maxdepth 3 -type d \( -name agents -o -name skills \)

# 命名约定（看前 20 个文件）
find ~/new-skill-repo -name '*.md' | head -20

# 是否有官方安装脚本
ls ~/new-skill-repo/scripts/ 2>/dev/null
grep -lE 'install|link' ~/new-skill-repo/scripts/*.sh 2>/dev/null
```

重点关注：
- **agents 与 skills 是否同目录**（混合）还是**分目录**（如 `agents/` + `skills/`）。
- **按 domain 分目录**（如 `engineering/`、`security/`）还是**平铺**。
- **命名约定**：`<domain>-<name>.md`（msitarzewski 风格）还是 `<name>/SKILL.md`（mattpocock 风格）还是 plugins 嵌套（wshobson 风格）。
- **安装机制**：有无官方脚本？脚本默认复制还是软链？有无 `--link` 类参数？
- **坑位信号**：`agents/openai.yaml`（Codex 专用，Claude Code 忽略）、符号链接嵌套、`deprecated/` 目录等。

---

## 4. 步骤 3 — 建档案（模板）

**文件路径**：`/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/references/<author>.md`
（按 `<author>` 命名，与现有 `msitarzewski.md` / `wshobson.md` / `mattpocock.md` 保持一致）

**档案模板**（仿照现有三个档案的五段式）：

```markdown
# 仓库档案：<author>/<repo>

## 基本信息
- **本地路径**：`/home/anonymous/new-skill-repo`
- **git remote**：`https://github.com/<author>/<repo>.git`
- **内容类型**：agents + skills 混合（按实际填写）

## 目录结构
- <顶层布局描述，例如：`agents/<domain>/` + `skills/<domain>/`，规模 N agents / M skills>
- <命名约定，例如：agent 文件命名 `<domain>-<name>.md`，skill 为 `<name>/SKILL.md` 目录>
- <常见 domain 列表>

## 安装机制
- <有无官方脚本？脚本命令示例>
- <默认复制还是软链？有 `--link` 类参数吗？>
- 符号链接安装示例：
  ```bash
  # agents
  ln -s /home/anonymous/new-skill-repo/agents/<domain>/<name>.md ~/.claude/agents/<name>.md
  # skills
  ln -s /home/anonymous/new-skill-repo/skills/<name> ~/.claude/skills/<name>
  ```
- ⚠️ 安装方式（软链/复制）按主流程第⑦步让用户拍板，不默认

## 坑位与约定（重要）
- <本仓库特有的陷阱，例如：本地名 vs 仓库名不一致、`cp -r` 复制链接行为、`deprecated/` 目录、OpenAI 专用 yaml 等>
- <断链排查三步（若涉及符号链接）>

## 已知实践（<当前年月>）
- <首次接入时的初始盘点结论，例如：本地已装 N 个、建议保留/待定/建议删的分布>
- <与现有 3 个仓库的重复项>
```

**写作要点**：
- 只写事实，不写推测；不确定的标「待用户确认」。
- 「坑位」段是未来自己踩坑的救命索，**宁多勿少**。
- 「已知实践」段记录首次接入时的决策，方便未来回溯。

---

## 5. 步骤 4 — 登记到「支持的仓库」表格

**文件**：`/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/SKILL.md`

**当前表格**（SKILL.md 第 20–25 行）：

```markdown
| 档案 | 仓库 | 内容 |
|------|------|------|
| `references/msitarzewski.md` | msitarzewski/agency-agents | agent 按 domain 分目录，install.sh 清单安装 |
| `references/wshobson.md` | wshobson/agents（Marketplace） | plugins 多域结构，符号链接惯例 |
| `references/mattpocock.md` | mattpocock/skills | 按 domain 分目录，link-skills.sh |
```

**追加一行**（放在表格末尾，保持插入顺序 = 接入顺序）：

```markdown
| `references/<author>.md` | <author>/<repo> | <一句话结构描述，例如：agents + skills 混合，按 domain 分目录，无官方脚本> |
```

**示例**（假设 remote 是 `https://github.com/jdoe/ai-toolkit.git`，agents/skills 按 domain 分目录、无官方脚本）：

```markdown
| `references/jdoe.md` | jdoe/ai-toolkit | agents + skills 混合，按 domain 分目录，无官方脚本，符号链接惯例 |
```

---

## 6. 步骤 5 — 更新 frontmatter description

**文件**：`/home/anonymous/.claude/skills/my-skills/skills/equipment-manager/SKILL.md`

**当前 description**（SKILL.md 第 3 行）：

```
description: 管理第三方 skill/agent 仓库的安装、筛选与精简。已接入：msitarzewski/agency-agents、wshobson/agents、mattpocock/skills（新仓库可按流程接入）。当用户提到某个 skill/agent 仓库的更新、安装、精简、盘点时使用——包括 git pull 后评估新内容、从这些仓库装新装备、删除无用的旧装备、或想接入一个新的第三方仓库。凡涉及"要不要装、装什么、删什么"的 skill/agent 决策都用本技能，不直接动手。各仓库结构/安装机制见 references/ 下档案。
```

**修改点**：把「已接入：A、B、C」改成「已接入：A、B、C、<新仓库>」。

**示例**（假设新仓库是 `jdoe/ai-toolkit`）：

```
description: 管理第三方 skill/agent 仓库的安装、筛选与精简。已接入：msitarzewski/agency-agents、wshobson/agents、mattpocock/skills、jdoe/ai-toolkit（新仓库可按流程接入）。当用户提到某个 skill/agent 仓库的更新、安装、精简、盘点时使用——包括 git pull 后评估新内容、从这些仓库装新装备、删除无用的旧装备、或想接入一个新的第三方仓库。凡涉及"要不要装、装什么、删什么"的 skill/agent 决策都用本技能，不直接动手。各仓库结构/安装机制见 references/ 下档案。
```

**description 写作纪律**：
- 「已接入」列表是**触发精准度**的关键——用户提到其中某个仓库时，技能会被自动唤起。
- 不写「等」「...」这类模糊词；每加一个仓库就显式列名。
- 列表过长（>6 个）时考虑分组：「已接入（agents）：...；已接入（skills）：...」。

---

## 7. 验收清单

完成以下五项即视为接入成功：

- [ ] `references/<author>.md` 已按模板填写完整（五段式：基本信息 / 目录结构 / 安装机制 / 坑位 / 已知实践）
- [ ] SKILL.md「支持的仓库」表格新增一行
- [ ] SKILL.md frontmatter `description` 的「已接入」列表已追加新仓库名
- [ ] 用户已确认仓库的「安装机制」（软链 vs 复制）与「首次盘点结论」（保留 / 待定 / 建议删）
- [ ] 方法论主体（SKILL.md 七步流程）未被改动——仓库差异全走档案

---

## 8. 不做的事（克制边界）

- **不改方法论**：七步流程、三档筛选、备份安装验证等通用内核保持不动。
- **不替用户决定安装方式**：软链 vs 复制由用户在主流程第⑦步拍板。
- **不擅自执行安装/删除**：本方案只产出情报，安装动作需用户按「军师出方案，主公定夺」原则确认。
- **不凭目录名猜测 remote**：`git remote -v` 为空时必须追问，不瞎填。
