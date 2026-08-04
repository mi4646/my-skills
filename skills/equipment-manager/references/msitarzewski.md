# 仓库档案：msitarzewski/agency-agents

## 基本信息
- **本地路径**：`/home/anonymous/agency-agents`
- **git remote**：`https://github.com/msitarzewski/agency-agents.git`

## 目录结构
- 按 domain 分目录：`engineering/`、`security/`、`design/`、`marketing/`、`sales/` 等
- agent 文件命名 `<domain>-<name>.md`（如 `engineering-backend-architect.md`）

## 安装机制（官方 `scripts/install.sh`）
- 按清单安装：`./scripts/install.sh --tool claude-code --agents-file scripts/agents-to-install.example`
- 装单个：`--agent <slug>`；按团队：`--division <a,b>`
- `--link`：符号链接安装（更新自动传播，多仓库用户推荐）
- `--path <dir>`：覆盖安装目录
- 清单文件：`scripts/agents-to-install.example`（每行一个 slug 或名字，`#` 注释）
- ⚠️ 安装方式（软链/复制）按主流程第⑦步让用户拍板：官方默认复制，需软链时用 `--link` 参数

## 坑位与约定
- 本地 `~/.claude/agents/engineering-*.md` 是该仓库复制产物（非链接）
- `install.sh` 会覆盖同名文件

## 已知实践（2026-08）
- 本地保留 22 个 engineering-* agents；删除 22 个无方向 agent（PHP/CMS、移动/小程序、区块链、嵌入式、网络、ITIL、安全冗余），备份于 `~/.claude/backups/agents-20260804/`
