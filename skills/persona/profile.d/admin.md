# 自学习层画像（本机：admin）

miner 从本机 session 日志挖掘、经用户确认的画像条目。**每机一个文件 `profile.d/<hostname>.md`，miner 只写本机自己的文件** → 三机各写各的，`git pull` 零冲突。

- **updated**: 2026-08-06
- **证据**: 🔍miner 提取 + 🗣用户确认（设计：自学习层写入分区）

## 技术栈

- **Python 后端为主（FastAPI + Django）**：session 日志实锤——「优化 FastAPI 接口性能」「配置 config.toml API key」、Python traceback/FastAPI 报错排查、django 开发（3 session）🔍（miner 2026-08-06，用户确认）

## 业务项目

- **/var/www 下有业务开发**：new/license/shyun、shyun、demo 等，session 日志证实业务开发与服务器运维并存 🔍（miner 2026-08-06，用户确认）
