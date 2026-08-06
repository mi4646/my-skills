#!/usr/bin/env bash
# 扫描环境信号，供 equipment-manager 评估时核对用户画像（profile.md）
# 证据分层：环境扫描实测 —— 与 记忆记录 / 用户口述 交叉验证，不以单一来源为准
set -uo pipefail

echo "== 1. 家目录 git 仓库（自有 vs 装备源）=="
for d in $(find "$HOME" -maxdepth 2 -name ".git" -type d 2>/dev/null); do
  repo=$(dirname "$d")
  url=$(git -C "$repo" remote get-url origin 2>/dev/null)
  [ -n "$url" ] && echo "  ${repo#$HOME/} → $url"
done

echo "== 2. 已装 Claude 插件 =="
python3 -c "import json;d=json.load(open('$HOME/.claude/plugins/installed_plugins.json'));[print('  '+p) for p in d['plugins']]" 2>/dev/null || echo "  (无/不可读)"

echo "== 3. 语言运行时证据 =="
for t in pyenv nvm bun dotnet python_history mysql_history; do
  [ -e "$HOME/.$t" ] && echo "  .$t 存在"
done

echo "== 4. 模型分层配置 =="
grep -oE 'ANTHROPIC_DEFAULT_[A-Z]+_MODEL[^,]*' "$HOME/.claude/settings.json" 2>/dev/null | head -8

echo "== 5. 最近7天活跃的家目录子目录 =="
find "$HOME" -maxdepth 1 -mindepth 1 -type d -mtime -7 2>/dev/null | sed "s|$HOME/||"
