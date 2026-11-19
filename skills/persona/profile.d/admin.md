# 自学习层画像（本机：admin）

miner 从本机 session 日志挖掘、经用户确认的画像条目。**每机一个文件 `profile.d/<hostname>.md`，miner 只写本机自己的文件** → 三机各写各的，`git pull` 零冲突。

- **updated**: 2026-11-19
- **证据**: 🔍miner 提取 + 🗣用户确认；每条带 provenance

## 技术栈

- **Python**（pyenv，主力语言；后端以 FastAPI + Django 为主）
  - provenance: 🔍 `.pyenv`/`.python_history` 存在；vietguard2(Django 5.2) + demo 两个活跃项目
  - FastAPI 🗣（用户 2026-08-06 口述确认「确实在用」；session 日志仅以 uvicorn/接口 表述，字面 fastapi 无真实命中——早期「优化 FastAPI 接口性能」证据经核为 equipment-manager 评测夹具重放污染，已从画像证据中剔除）
- **Docker / Docker Compose**（主力部署方式，前后端分离 + nginx）
  - provenance: 🔍 vietguard2/`docker-compose.full.yml` 前后端分离 + `Dockerfile.web` + nginx 502 排障 + 前端 html 容器化更新流程；ocr-api docker compose up（4 sessions，2026-08-10/11）
- **MySQL**（主力数据库）
  - provenance: 🔍 `.mysql_history` 存在；vietguard2 Django 项目
- **Bash**（脚本与部署）
  - provenance: 🔍 11 sessions / 67 hits；update-agents.sh 等维护脚本

## 业务工作流

- **子代理驱动开发**（worktree → plans → subagent → review → merge）
  - provenance: 🔍 session 8366a939(9-2) / 0abb4682(8-30) / 508f380e(8-26) 三个不同日期一致模式
- **设计文档先行**（design doc → review doc → 开发）
  - provenance: 🔍 同上三 session「基于项目设计文档和评审文档」；508f380e「docs/designs/llm-timeout-per-caller.md」
- **装备管理**（定期评估第三方 skill/agent）
  - provenance: 🔍 session 9b596c86(9-2) / 03766261(8-24) / 2b282ae0(8-20)

## 业务项目

- **/var/www 下有业务开发**：new/license/shyun、shyun、demo 等，session 日志证实业务开发与服务器运维并存 🔍（miner 2026-08-06，用户确认）
- **vietguard2**：Django + Docker 前后端分离（manage.py + 多 app + html 前端），`docker-compose.full.yml` 部署；2026-08-10/11 活跃（nginx 502 排障、docker 部署升级咨询）🔍
- **shyun**：Django 项目（`python manage.py dbshell` 连 mysql；`Internal Server Error: /api/captcha/`）🔍 3 sessions
- **QQ音乐歌单业务域**：/var/www/demo 歌单项目（AI 分类后推送到账号流程）+ ~/.qqplaylist 日志 🔍。**2026-08-21 高峰 ✅**：新建歌单流程迭代（先查用户端同名歌单→询问更新/新建）、push_service 云拉取调研（src/qqplaylist/push_service.py:72-100）、QQMusicApi 0.7.2 适配 🔍（用户确认 2026-08-24）

## 运维

- **服务器运维/时间同步**：「timedatectl set-ntp false 干嘛的」「date 显示 2015 年」08-05 日志举证 🔍

## 明确排除的领域（🗣用户表态）

- 不做 PPT（🗣评估时拍板）
- 不微调 LLM（🗣评估时拍板）
- 无 DGX 硬件（🗣评估时拍板）
