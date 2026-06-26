---
name: obsidian-icon-assigner
description: 为Obsidian知识库的Markdown文档自动分配Iconic插件的图标和颜色。目录级颜色继承，文件级图标尽量唯一。当用户需要为Obsidian文档批量设置视觉标识、整理知识库视觉层次、或需要一致的图标配色方案时，使用此技能。特别适用于新知识库初始化、目录结构调整后重新分配图标、或需要批量更新大量未设置图标的文档。
---

# Obsidian 图标自动分配器

## 快速开始

### 1. 安装依赖
确保Python 3.7+环境，无额外依赖包

### 2. 运行技能
```bash
cd /path/to/vault
python ${CLAUDE_PLUGIN_ROOT}/skills/obsidian-icon-assigner/scripts/assign_icons.py --vault-path .
```

### 3. 检查结果
1. 查看控制台输出统计
2. 重启Obsidian查看图标分配
3. 检查`.obsidian/plugins/iconic/data.json`更新

## 使用模式

### 模式1：新知识库初始化
```bash
# 为所有文件分配图标和颜色
python ${CLAUDE_PLUGIN_ROOT}/skills/obsidian-icon-assigner/scripts/assign_icons.py --vault-path /path/to/vault
```

### 模式2：增量更新（推荐）
```bash
# 只处理未设置图标的文件
python ${CLAUDE_PLUGIN_ROOT}/skills/obsidian-icon-assigner/scripts/assign_icons.py --vault-path /path/to/vault --skip-existing
```

### 模式3：试运行分析
```bash
# 预览分配结果，不实际修改
python ${CLAUDE_PLUGIN_ROOT}/skills/obsidian-icon-assigner/scripts/assign_icons.py --vault-path /path/to/vault --dry-run
```

### 模式4：强制重新分配
```bash
# 覆盖所有现有图标
python ${CLAUDE_PLUGIN_ROOT}/skills/obsidian-icon-assigner/scripts/assign_icons.py --vault-path /path/to/vault --force
```

### 模式5：查看图标库
```bash
# 列出所有可用图标
python ${CLAUDE_PLUGIN_ROOT}/skills/obsidian-icon-assigner/scripts/assign_icons.py --list-icons
```

## 核心特性

### 🔍 智能颜色继承
- 已有颜色的目录保留原配置
- 新子目录继承最近父目录的颜色
- 没有可继承父目录颜色时，才使用哈希生成HSL颜色
- 同一目录下文件颜色统一

### 🎯 图标唯一性
- 每个文件尽量获得唯一图标
- 图标冲突时使用变体（如lucide-file-text-2）
- 300+个Lucid图标支持

### 🔄 非破坏性更新
- 尊重用户手动设置的图标（默认）
- 支持增量处理
- 自动备份配置文件

### 🧠 确定性分配
- 同一文件路径永远获得相同的图标+颜色
- 基于SHA256哈希的确定性映射
- 分配结果可重复验证


## 参数说明

```bash
# 完整参数列表
python ${CLAUDE_PLUGIN_ROOT}/skills/obsidian-icon-assigner/scripts/assign_icons.py --help

# 主要参数：
--vault-path PATH      Obsidian vault路径（必需）
--config-path PATH     Iconic配置文件路径，默认.obsidian/plugins/iconic/data.json
--skip-existing        跳过已有图标的文件（默认：true）
--force                强制重新分配所有文件图标（覆盖现有设置）
--dry-run              试运行，不实际修改配置文件
--list-icons           列出所有可用图标
```

## 高级配置

### 自定义图标映射
如需自定义特定目录或文件的图标，可直接编辑Iconic插件的data.json文件，此技能会尊重已有配置。

### 颜色调整
目录颜色分配顺序：
1. 目录自身已有 `color` 时，保留现有配置
2. 新子目录优先继承最近父目录的 `color`
3. 如果没有任何父目录颜色，使用目录路径哈希生成HSL颜色：
   - 色相：目录路径哈希值 % 360
   - 饱和度：固定70%
   - 亮度：固定50%

如需调整，可手动修改data.json中的color字段。

## 故障排除

### 常见问题
1. **配置文件不存在**：确保Iconic插件已安装并启用
2. **权限不足**：确保有文件写入权限
3. **Python版本**：需要Python 3.7+

### 恢复备份
每次运行会自动创建备份文件：`data.json.YYYYMMDD_HHMMSS.bak`
如需恢复：
```bash
cp .obsidian/plugins/iconic/data.json.20240420_143025.bak .obsidian/plugins/iconic/data.json
```

## 工作原理简述

1. **扫描**：递归扫描vault中所有.md文件
2. **分析**：读取现有Iconic配置，提取已分配图标和颜色
3. **分配**：
   - 目录颜色：保留自身已有颜色；新子目录继承最近父目录颜色；无父级颜色时哈希生成
   - 文件图标：基于文件路径SHA256哈希分配唯一图标
4. **更新**：写入配置并创建备份
5. **报告**：输出统计信息

## 性能提示
- 大型知识库（1000+文件）可能需要几秒钟
- 使用`--dry-run`先预览结果
- 增量更新时使用`--skip-existing`（默认）

---

*技能设计遵循"最小惊讶原则"，用户手动设置的图标和颜色始终优先分配。*