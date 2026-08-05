# My Skills

个人自研技能集合。**本仓库只含自研技能**；第三方技能由 `install.sh` 一键安装，来源一目了然、更新互不影响。

## 技能列表（自研 7 个）

### [equipment-manager](./skills/equipment-manager)
管理从第三方仓库安装的 skill/agent——对话式流程：盘点 → 查重 → 三档筛选 → 备份安装 → 验证。

### [obsidian-icon-assigner](./skills/obsidian-icon-assigner)
为 Obsidian 知识库的 Markdown 文档自动分配 Iconic 插件的图标和颜色。

- 目录级颜色继承，文件级图标尽量唯一
- 基于 SHA256 哈希的确定性映射，同一文件路径始终获得相同结果
- 300+ Lucide 图标，中文关键词优先匹配

### [opencode-model-optimizer](./skills/opencode-model-optimizer)
为 OpenCode Go 等平台的 Claude Code 模型层级提供分层配置推荐。

- 先问后答：了解场景、预算、配额后才给方案
- 支持分层配置、成本最优、配额友好等推荐模式

### [playlist-organizer](./skills/playlist-organizer)
将音乐收藏、歌单链接、本地 txt/csv 整理成自定义场景歌单。

- 先访谈确认分类场景、覆盖规则、重复归属
- 内置 Python 脚本生成导入友好的 txt 歌单和报告

### [release-skills](./skills/release-skills)
通用发布工作流，支持多语言 changelog，自动检测版本文件和发布策略。

### [update-version](./skills/update-version)
根据 git diff 差异自动更新版本号。

### [weekly-report](./skills/weekly-report)
根据 git commit 历史归纳本周/上周工作成果，生成结构化开发周报。

---

## 部署备忘录（三平台通用）

> 部署 = clone 本仓库 → 跑 `install.sh` → 重启 Claude Code。三步。

### 一键安装（推荐）

```bash
# ① clone 本仓库（自带 install.sh）
git clone https://github.com/mi4646/my-skills.git ~/.claude/skills/my-skills

# ② 一键脚本：clone 三个上游仓库 + 建 mattpocock 插件 + 软链 10 个 + 复制 3 个独立技能
bash ~/.claude/skills/my-skills/install.sh

# ③ 重启 Claude Code，或输入 /reload-plugins
```

`install.sh` 幂等：已装的跳过，重复运行安全。`install.sh --update` 升级：pull 全部上游 + 强制重装。**自动检测平台**：Windows 全复制（无需开发者模式、无软链权限坑），Linux/macOS 全软链；可用 `INSTALL_MODE=symlink` 强制软链。

### install.sh 会做什么

| 步骤 | 内容 |
|---|---|
| ① mattpocock 精选 10 个 | clone `mattpocock/skills` → 建 `mattpocock/` 插件目录 → 10 个技能 |
| ② baoyu-design | clone `jimliu/baoyu-design` → 技能 `skills/baoyu-design` |
| ③ hallmark | clone `nutlope/hallmark` → 技能 `skills/hallmark` |
| ④ storage-analyzer | clone `KKKKhazix/khazix-skills` → 技能 `storage-analyzer` |

> 安装方式：Linux/macOS 全部**软链**（git pull 自动更新）；Windows 自动改**复制**（升级跑 `--update`）。

### 手动步骤（脚本出问题时参照）

#### mattpocock 精选 10 个（软链官方仓库）

```bash
git clone https://github.com/mattpocock/skills.git ~/skills/mattpocock
mkdir -p ~/.claude/skills/mattpocock/skills ~/.claude/skills/mattpocock/.claude-plugin
# plugin.json（技能靠自动发现，无需声明）：
#   {"name":"mattpocock","version":"1.0.0","description":"mattpocock/skills 精选"}
R=~/skills/mattpocock/skills
for kv in "obsidian-vault:personal/obsidian-vault" \
          "edit-article:personal/edit-article" \
          "git-guardrails-claude-code:misc/git-guardrails-claude-code" \
          "grill-with-docs:engineering/grill-with-docs" \
          "domain-modeling:engineering/domain-modeling" \
          "handoff:productivity/handoff" \
          "grill-me:productivity/grill-me" \
          "prototype:engineering/prototype" \
          "research:engineering/research" \
          "resolving-merge-conflicts:engineering/resolving-merge-conflicts"; do
  name="${kv%%:*}"; src="${kv#*:}"
  ln -s "$R/$src" ~/.claude/skills/mattpocock/skills/$name
done
```

#### 独立第三方工具

| 技能 | 上游仓库 | 仓库内技能路径 |
|------|----------|----------------|
| baoyu-design | `jimliu/baoyu-design` | `skills/baoyu-design/` |
| hallmark | `nutlope/hallmark` | `skills/hallmark/` |
| storage-analyzer | `KKKKhazix/khazix-skills` | `storage-analyzer/` |

```bash
git clone <上游仓库> ~/skills/<仓库名>
ln -s ~/skills/<仓库名>/<技能路径> ~/.claude/skills/<技能名>   # Linux 软链
# Windows 复制：cp -r ~/skills/<仓库名>/<技能路径> ~/.claude/skills/<技能名>
```

### 平台差异对照

| 平台 | 技能目录 | 安装方式 | 注意 |
|------|----------|----------|------|
| Linux（本机 WSL / 腾讯云） | `~/.claude/skills/` | 全部软链（git pull 自动更新） | 腾讯云无桌面，命令同左 |
| Windows | `%USERPROFILE%\.claude\skills\` | 全部复制 | 用 Git Bash 跑 `bash install.sh`，无需开发者模式；升级跑 `--update` |

### 日常更新

```bash
# 一键升级：pull 全部上游 + 强制重装（Windows 复制安装必用）
bash ~/.claude/skills/my-skills/install.sh --update

# 或手动（Linux 软链自动生效，只需 pull 上游）
cd ~/skills/mattpocock && git pull
cd ~/skills/baoyu-design && git pull
cd ~/skills/hallmark && git pull
cd ~/skills/khazix-skills && git pull
```

### 卸载

```bash
rm -rf ~/.claude/skills/mattpocock ~/.claude/skills/baoyu-design \
       ~/.claude/skills/hallmark ~/.claude/skills/storage-analyzer
```

---

## 使用方式

安装后通过带命名空间的技能名调用：

```
/my-skills:obsidian-icon-assigner
/my-skills:opencode-model-optimizer
/my-skills:playlist-organizer
/my-skills:release-skills
/my-skills:update-version
/my-skills:weekly-report
/my-skills:equipment-manager
```

第三方技能：

```
/mattpocock:obsidian-vault   /mattpocock:grill-me   /mattpocock:domain-modeling
/baoyu-design                /hallmark              /storage-analyzer
```
