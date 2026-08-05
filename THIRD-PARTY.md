# 三方装备说明

本仓库 `install.sh` 一键安装的第三方 skill、agents、plugins 总览，来源独立、更新互不影响。

## Skills

| 资产 | 类型 | 用途 | 内含 | 来源 |
|---|---|---|---|---|
| mattpocock | 插件 | 精选个人工作流技能集：写作、原型、研究、Git 协作等 | 10 个技能，命名空间 `mattpocock:` | `github.com/mattpocock/skills` |
| baoyu-design | 技能 + 内置子技能/agents | 设计原型生成：网页、PPT、图表、设计系统等交付物 | 主技能 + 50 余个流程子技能 + 3 只读子代理 | `github.com/jimliu/baoyu-design` |
| hallmark | 纯技能 | 反 AI 味设计指导：新页面 / 重设计 / 审计 | 1 | `github.com/nutlope/hallmark` |
| storage-analyzer | 技能 + Python 脚本 | 磁盘 / 仓库存储占用扫描分析 | 1 | `github.com/KKKKhazix/khazix-skills` |

## Agents

仅 baoyu-design 自带 3 个只读子代理，由主流程内部 spawn，**无全局调用命令**：

- **vision-probe-agent** — 任务前探测当前模型/提供商是否支持图像输入
- **fork-verifier-agent** — 校验刚生成的设计交付物，回报 `done` / `needs_work`
- **design-system-checker** — 只读校验便携设计系统，输出一行健康摘要

## Plugins

仅 mattpocock 是插件（`.claude-plugin/plugin.json` 声明），其余为独立技能目录。

## 维护

- 安装：`bash install.sh`（幂等，已装跳过）
- 升级：`bash install.sh --update`（`git pull` + 强制重新复制）
- 实时清单：`bash install.sh --list`
- 调用方式：见主 README「使用方式」章节
