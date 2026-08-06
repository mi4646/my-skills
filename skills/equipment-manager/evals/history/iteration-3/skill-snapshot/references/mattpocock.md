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

## 已知实践（2026-08）
- my-skills 生态已引入 4 个本仓库技能：`grill-me`、`prototype`、`research`、`resolving-merge-conflicts`
