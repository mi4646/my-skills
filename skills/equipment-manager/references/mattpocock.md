# 仓库档案：mattpocock/skills

## 基本信息
- **本地路径**：`/home/anonymous/skills`
- **git remote**：`https://github.com/mattpocock/skills.git`

## 目录结构
- `skills/<domain>/`：`deprecated`、`engineering`、`in-progress`、`misc`、`personal`、`productivity`
- `scripts/`：link-skills.sh、list-skills.sh

## 安装机制（官方）
```bash
./scripts/link-skills.sh   # 符号链接安装到本地，更新自动传播
./scripts/list-skills.sh   # 列出技能
```
⚠️ 官方为 link-skills.sh（软链），但安装方式仍按主流程第⑦步让用户选择（软链/复制）

## 坑位与约定
- 每个技能可能带 `agents/openai.yaml`（面向 Codex/OpenAI 宿主，Claude Code 忽略），改动时注意保持同步

## 本地安装现状（2026-08-04）
- **方式**：插件目录 `~/.claude/skills/mattpocock/`（`.claude-plugin/plugin.json` 只写元信息，技能靠自动发现），10 个技能全部**软链**到仓库 → `git pull` 即更新
- **软链源**：`/home/anonymous/skills/skills/<domain>/<name>`
- **精选 10 个**（未装全家桶——to-spec/to-tickets/wayfinder/triage 需配 issue tracker 且与 gstack 规划工具重复，评估不装）：
  - `personal/`：obsidian-vault、edit-article
  - `misc/`：git-guardrails-claude-code
  - `engineering/`：grill-with-docs、domain-modeling、grill-me、prototype、research、resolving-merge-conflicts
  - `productivity/`：handoff
- 前置已装：grill-me/prototype/research/resolving-merge-conflicts 原从 my-skills 复制迁入，与仓库逐字一致（未本地改动）

## 一键安装（维护于 my-skills/install.sh）
- `install.sh` 跨平台：`install`（幂等）/ `--update`（pull 全部上游 + 强制重装）；**Linux 全软链、Windows 全复制**（自动检测平台）
- 对应 my-skills/README「部署备忘录」；Windows 用 Git Bash，无需开发者模式
- **更新**：`bash ~/.claude/skills/my-skills/install.sh --update` 或逐仓库 `git pull`；**卸载**：`rm -rf ~/.claude/skills/mattpocock`

