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

## 本地安装现状
安装状态（已装清单/评估结论）见 `~/.config/equipment-manager/state.json`，不进本档案。
- 2026-08-06 实测：`~/.claude/skills` 无任何 mattpocock 痕迹，**本地 0 已装**（8-04 档案记录的精选 10 个软链已全部消失，原因待查）
- 8-04 曾精选 10 个软链到 `~/.claude/skills/mattpocock/`，`git pull` 即更新；该目录现已不存在

## 一键安装（维护于 my-skills/install.sh）
- `install.sh` 跨平台：`install`（幂等）/ `--update`（pull 全部上游 + 强制重装）；**Linux 全软链、Windows 全复制**（自动检测平台）
- 对应 my-skills/README「部署备忘录」；Windows 用 Git Bash，无需开发者模式
- **更新**：`bash ~/.claude/skills/my-skills/install.sh --update` 或逐仓库 `git pull`；**卸载**：`rm -rf ~/.claude/skills/mattpocock`

