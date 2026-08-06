# 新仓库接入方案：`~/new-skill-repo`（agents + skills 混合）

> 本方案按装备管理器方法论「接入新仓库」流程出具，仅出方案、不动手。
> 仓库 `~/new-skill-repo` 本机尚不存在，以下为通用接入方案，落地时按实际结构校对。

## 现状
- 方法论已固化（盘点→查重→三档筛选→提问澄清→备份安装→验证），仓库差异全部走 `references/` 档案。
- 已接入 3 个仓库：msitarzewski/agency-agents（agent 为主）、wshobson/agents（plugins 多域，agents+skills 混合，最接近本仓库形态）、mattpocock/skills（skill 为主）。
- 新仓库为 **agents + skills 混合**，结构与 wshobson 最像，档案格式可直接参照。

---

## 接入五步

### 第 1 步：确认来源
- `git -C ~/new-skill-repo remote -v`，确认远程地址、是否 fork、作者。
- 核对 `git log -1 --format='%h %ad %s'`，确认 clone 版本时间点。
- 产出：来源信息写入档案「基本信息」。

### 第 2 步：摸清结构
- `tree ~/new-skill-repo -L 3`（或 `ls -R`）看顶层目录。
- 确认 agents 与 skills 各自位置：是 `agents/`、`skills/` 分开，还是 `plugins/<domain>/{agents,skills}/` 混合（参照 wshobson）。
- 确认命名约定：`<domain>-<name>.md` 还是 `skills/<name>/SKILL.md`。
- 确认安装机制：官方脚本（`install.sh`/`link-skills.sh`）、还是惯例符号链接/复制（参照 wshobson 惯例软链）。
- 检查每个 skill 是否有 `SKILL.md`、agent 是否有 frontmatter `name`/`description`，宿主兼容性（是否含 `agents/openai.yaml` 之类非 Claude 宿主文件，参照 mattpocock 坑位）。
- 产出：结构结论写入档案「目录结构」「安装机制」。

### 第 3 步：建档案
在 `references/` 下新建档案文件（按仓库名命名，如 `references/new-skill-repo.md`），**仿照现有三个档案的五段式结构**：

```markdown
# 仓库档案：<owner>/<repo>

## 基本信息
- **本地路径**：`~/new-skill-repo`
- **git remote**：`<git clone 的远程地址>`

## 目录结构
- 顶层结构：<实际结构，如 `agents/`、`skills/` 分开，或 `plugins/<domain>/{agents,skills}/` 混合>
- 命名约定：<如 `<domain>-<name>.md` / `skills/<name>/SKILL.md`>
- 规模：<如 N agents / M skills，按实际统计>

## 安装机制
- <官方脚本命令 / 惯例软链命令>
- ⚠️ 安装方式（软链/复制）按主流程第⑦步让用户拍板，不默认

## 坑位与约定
- <与既有仓库冲突、非 Claude 宿主文件、本地名 vs 仓库名差异等>

## 已知实践（<日期>）
- <接入评估后的结论：装了哪些/删了哪些/备份位置>
```

要点：
- 档案 = 仓库专属情报，方法论不复制进档案。
- 首次建档案时「已知实践」可先留空或写「待评估」，等真正安装后再回填。

### 第 4 步：登记
在 SKILL.md 的「支持的仓库」表格中加一行：

| 档案 | 仓库 | 内容 |
|------|------|------|
| `references/new-skill-repo.md` | <owner>/<repo> | <一句话描述结构与安装机制，如 agents+skills 混合，惯例软链> |

### 第 5 步：更新 description
在 SKILL.md frontmatter `description` 的「已接入」列表补上仓库名：

```
description: ... 已接入：msitarzewski/agency-agents、wshobson/agents、mattpocock/skills、<owner>/<repo>（新仓库可按流程接入）...
```

保持触发精准：只加名字，不展开细节（细节在档案里）。

---

## 通用内核不动
- 五步全部是「建档案 + 表格一行 + description 补一个名字」，方法论正文（七步流程、克制原则）零改动。
- 加仓库不改内核 = 后续任何新仓库都能走同一流程。

## 下一步（待用户拍板后才执行）
1. 仓库 clone 就绪后，实际执行第 1~2 步（确认来源、摸清结构）。
2. 按七步流程评估具体该装哪些：盘点本地 → 查重 → 按真实项目栈三档筛选 → 一次一问澄清 → 出方案。
3. 安装方式（符号链接 vs 复制）由用户选择，默认推荐符号链接。
4. 任何覆盖/删除前先备份到 `~/.claude/backups/<日期>/`。

本方案不包含任何实际创建档案、登记或修改 description 的动作。
