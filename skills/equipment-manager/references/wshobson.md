# 仓库档案：wshobson/agents（Agentic Plugin Marketplace）

## 基本信息
- **本地路径**：`/home/anonymous/agents`
- **git remote**：`https://github.com/wshobson/agents.git`

## 目录结构
- `plugins/<domain>/{agents,skills,plugins}/`，规模 94 plugins / 203 agents / 175 skills / 109 commands
- 常见域：`python-development`、`backend-development`、`database-design`、`llm-application-dev`、`documentation-generation`、`shell-scripting`

## 安装机制
- 无官方统一脚本，**惯例为符号链接**：
  ```bash
  ln -s /home/anonymous/agents/plugins/<domain>/skills/<name> ~/.claude/skills/<name>
  # 或项目级：
  ln -s /home/anonymous/agents/plugins/<domain>/skills/<name> <repo>/.claude/skills/<name>
  ```
- 符号链接特性：仓库更新自动传播到本地（无需重装）；但仓库路径被移动/删除会**断链**
- ⚠️ 本仓库惯例为符号链接，但安装方式仍按主流程第⑦步让用户选择（软链/复制），不默认

## 坑位与约定（重要）
- **本地名 vs 仓库名可能不一致**——建链接前先 `ls` 仓库实际目录核对名字
  - 案例：本地 `python-async-patterns` 断链，仓库实际叫 `async-python-patterns`（2026-08 发现并修复）
- `cp -r` 复制链接时，链接会被**原样保留**（GNU coreutils 对链接参数的行为），目标位置同样是链接
- 断链排查三步：
  ```bash
  ls -la ~/.claude/skills/                    # 看 -> 指向，识别来源
  readlink <link>                              # 解析链接真实目标
  [ -e <target> ] && echo OK || echo BROKEN    # 判断目标是否还存在
  ```

