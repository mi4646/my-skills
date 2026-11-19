# 自学习层画像·个人习惯备忘（本机：admin）

miner 挖掘、用户确认的个人习惯/工具习惯。**仅备忘**：`profile.d/*.md` 通配符不匹配 prefs/ 子目录，equipment-manager 评估不消费本文件。

- **updated**: 2026-11-19
- **证据**: 🔍miner 提取 + 🗣用户确认

## 工具习惯

- **固定 prompt 模板**：开发任务用固定五步 prompt（worktree → plans → subagent → review → cleanup），三个不同日期 session 逐字相同
  - provenance: 🔍 session 8366a939 / 0abb4682 / 508f380e
- **子代理工作流偏好**：复杂功能用 `/using-git-worktrees` 基于 main 建开发分支 + `/writing-plans` 拆 2-5 分钟可验证的子代理任务 + `/subagents` 执行，任务逐条带文件路径与验证断言 🔍（miner 2026-08-21，用户确认 2026-08-24）
- **中文交互**：所有用户输入为中文，但项目代码/注释要求英文
  - provenance: 🔍 全部 session 用户输入中文；🗣 vietguard2 CLAUDE.md「Every code comment…must be in English」

## 沟通偏好

- **复杂改动前先提问确认**：先问、一次只问一个问题，根据回答持续追问，等 95% 理解真实需求目标后再给方案（带建议及理由），确保完全理解再执行 🗣确认（2026-08-24，用户两次明确要求）
