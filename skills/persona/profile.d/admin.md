# 自学习层画像（本机：admin）

miner 从本机 session 日志挖掘、经用户确认的画像条目。**每机一个文件 `profile.d/<hostname>.md`，miner 只写本机自己的文件** → 三机各写各的，`git pull` 零冲突。

- **updated**: 2026-08-24
- **证据**: 🔍miner 提取 + 🗣用户确认（设计：自学习层写入分区）

## 技术栈

- **Python 后端为主（FastAPI + Django）**：FastAPI 🗣（用户 2026-08-06 口述确认「确实在用」；session 日志仅以 uvicorn/接口 表述，字面 fastapi 无真实命中——早期「优化 FastAPI 接口性能」证据经核为 equipment-manager 评测夹具重放污染，已从画像证据中剔除）。Django 🔍（3 session，/var/www/shyun 业务）
- **Docker 容器化部署（docker-compose 前后端分离 + nginx）** 🔒稳定：`docker-compose.full.yml` 前后端分离 + `Dockerfile.web` + nginx 502 排障 + 前端 html 容器化更新流程。证据：/var/www/vietguard2 4 sessions（2026-08-10/11，miner，用户确认 2026-08-11）

## 业务项目

- **/var/www 下有业务开发**：new/license/shyun、shyun、demo 等，session 日志证实业务开发与服务器运维并存 🔍（miner 2026-08-06，用户确认）
- **vietguard2 是 Django + Docker 前后端分离项目**：/var/www/vietguard2（manage.py + 多 app + html 前端），`docker-compose.full.yml` 前后端分离部署，含前端 html 更新流程；2026-08-10/11 活跃（nginx 502 排障、docker 部署升级咨询）🔍（miner 2026-08-11，用户确认）
- **shyun 是 Django 项目**：「python manage.py dbshell 连接的 mysql」「Internal Server Error: /api/captcha/」django 3 sessions 举证 🔍（miner 2026-08-06，用户确认）
- **QQ音乐歌单业务域**：/var/www/demo 歌单项目（AI 分类后推送到账号流程）+ ~/.qqplaylist 目录活跃（日志落盘 ~/.qqplaylist/logs）🔍（miner 2026-08-07，用户确认）。**2026-08-21 高峰 ✅**：新建歌单流程迭代（先查用户端同名歌单→询问客户更新/新建）、push_service 云拉取功能调研（src/qqplaylist/push_service.py:72-100）、QQMusicApi 0.7.2 版本适配 🔍（用户确认 2026-08-24；证据 /var/www/demo · b0f0e0ba/fbb9c8da/b7187dc2 08-21 歌单流程 ×3 + agent-aed5e64566fc154af push_service 云拉取调研 + 944e1c95 QQMusicApi 0.7.2）

## 运维

- **服务器运维/时间同步**：「timedatectl set-ntp false 干嘛的」「date 显示 2015 年」08-05 日志举证 🔍（miner 2026-08-06，用户确认）
