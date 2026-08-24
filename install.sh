#!/usr/bin/env bash
# 一键安装/升级第三方技能装备
# 用法：
#   bash install.sh           幂等安装（已装跳过）
#   bash install.sh --update  升级（git pull 上游 + 强制重新复制/软链）
# 依赖：git、bash 4+（Windows 用 Git Bash）
set -euo pipefail

SKILLS_DIR="${HOME}/.claude/skills"
VENDOR_DIR="${HOME}/.cache/equipment-manager/vendor"

UPDATE=false
LIST=false
case "${1:-}" in
  --update) UPDATE=true ;;
  --list)   LIST=true ;;
esac

say()  { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
skip() { printf '  · %s 已存在，跳过\n' "$*"; }

# 默认复制安装：软链指向缓存 vendor 目录，误删会断链，故全平台一律复制。
# vendor 为临时 clone 缓存（~/.cache/equipment-manager/vendor），安装完即删，不持久占用用户目录
INSTALL_MODE="${INSTALL_MODE:-copy}"
[ "$UPDATE" = true ] && LABEL="升级" || LABEL="安装"
[ "$LIST" = false ] && printf '  · 安装方式: %s | 模式: %s\n' "$INSTALL_MODE" "$LABEL"

# 三方装备元数据（来源与下方 repo URL 同源；第三字段=独立 skill 目录形态的已装清单，逗号分隔；第四字段=独立 agent 文件的已装清单）
EQUIP=(
  "hallmark|github.com/nutlope/hallmark|"
  "storage-analyzer|github.com/KKKKhazix/khazix-skills|"
  "addyosmani|github.com/addyosmani/agent-skills|context-engineering,interview-me,source-driven-development"
  "mattpocock|github.com/mattpocock/skills|teach"
  "wshobson|github.com/wshobson/agents|avoid-ai-writing|eval-judge,python-development-fastapi-pro,python-development-django-pro,bash-pro"
)

# 三方装备清单：扫描已安装目录实时统计（不联网、不写盘）
if [ "$LIST" = true ]; then
  printf '\n\033[1;36m==> 三方装备清单\033[0m\n'
  printf '%-16s %-6s %-8s %-8s %s\n' "资产" "插件" "技能数" "agents" "来源"
  for kv in "${EQUIP[@]}"; do
    IFS='|' read -r name repo indep agents <<< "$kv"
    d="$SKILLS_DIR/$name"
    plugin=$([ -f "$d/.claude-plugin/plugin.json" ] && echo ✓ || echo -)
    n=0
    if [ -n "$indep" ]; then
      # 独立 skill 目录形态（如 addyosmani）：按清单统计已装数
      for s in ${indep//,/ }; do [ -d "$SKILLS_DIR/$s" ] && n=$((n + 1)); done
    else
      [ -d "$d/skills" ] && n=$((n + $(ls "$d/skills" | wc -l)))
      [ -f "$d/SKILL.md" ] && n=$((n + 1))
      [ -d "$d/built-in-skills" ] && n=$((n + $(ls "$d/built-in-skills" | wc -l)))
    fi
    a=0
    if [ -n "$agents" ]; then
      # 独立 agent 文件形态（如 wshobson）：按清单统计已装数
      for ag in ${agents//,/ }; do [ -f "$HOME/.claude/agents/$ag.md" ] && a=$((a + 1)); done
    else
      [ -d "$d/agents" ] && a=$(find "$d/agents" -maxdepth 1 -name '*.md' | wc -l)
    fi
    printf '%-16s %-6s %-8s %-8s %s\n' "$name" "$plugin" "$n" "$a" "$repo"
  done
  exit 0
fi

mkdir -p "$SKILLS_DIR" "$VENDOR_DIR"

# 仓库：有 .git 则 --update 时 git pull；目录存在但无 .git（如手动复制）则 --update 时重装 clone、否则跳过；不存在则 clone
repo() {
  local url="$1" dir="$2"
  if [ -d "$dir/.git" ]; then
    if [ "$UPDATE" = true ]; then
      echo "  · git pull: $dir"
      git -C "$dir" pull --ff-only 2>&1 | sed 's/^/    /' || true
    fi
  elif [ -d "$dir" ]; then
    if [ "$UPDATE" = true ]; then
      echo "  · 无 .git，重装 clone: $dir"
      rm -rf "$dir"
      git clone --depth 1 "$url" "$dir"
    else
      echo "  · $dir 已存在（无 .git），跳过"
    fi
  else
    git clone --depth 1 "$url" "$dir"
  fi
}

# 技能：--update 强制覆盖重装；否则存在跳过
skill() {
  local src="$1" dest="$2" name="$3"
  if [ "$UPDATE" = true ]; then
    rm -rf "$dest"
    if [ "$INSTALL_MODE" = "copy" ]; then
      cp -r "$src" "$dest"; printf '  复制 %s\n' "$name"
    else
      ln -s "$src" "$dest"; printf '  软链 %s\n' "$name"
    fi
  elif [ -e "$dest" ]; then
    skip "$name"
  else
    if [ "$INSTALL_MODE" = "copy" ]; then
      cp -r "$src" "$dest"; printf '  复制 %s\n' "$name"
    else
      ln -s "$src" "$dest"; printf '  软链 %s\n' "$name"
    fi
  fi
}

# ---------- ① hallmark ----------
say "[1/6] hallmark"
REPO="$VENDOR_DIR/hallmark"
repo https://github.com/nutlope/hallmark.git "$REPO"
skill "$REPO/skills/hallmark" "$SKILLS_DIR/hallmark" "hallmark"

# ---------- ② storage-analyzer ----------
say "[2/6] storage-analyzer"
REPO="$VENDOR_DIR/khazix-skills"
repo https://github.com/KKKKhazix/khazix-skills.git "$REPO"
skill "$REPO/storage-analyzer" "$SKILLS_DIR/storage-analyzer" "storage-analyzer"

# ---------- ③ addyosmani 精选 3 个（独立 skill 目录形态）----------
say "[3/6] addyosmani 精选 3 个"
REPO="$VENDOR_DIR/addyosmani"
repo https://github.com/addyosmani/agent-skills.git "$REPO"
skill "$REPO/skills/context-engineering" "$SKILLS_DIR/context-engineering" "context-engineering"
skill "$REPO/skills/interview-me" "$SKILLS_DIR/interview-me" "interview-me"
skill "$REPO/skills/source-driven-development" "$SKILLS_DIR/source-driven-development" "source-driven-development"

# ---------- ④ mattpocock teach（独立 skill 目录形态，纯用户唤起）----------
say "[4/6] mattpocock teach"
REPO="$VENDOR_DIR/mattpocock"
repo https://github.com/mattpocock/skills.git "$REPO"
skill "$REPO/skills/productivity/teach" "$SKILLS_DIR/teach" "teach"

# ---------- ⑤ wshobson 精选 agents 4 个（复制到 ~/.claude/agents/，用户偏好一律复制不软链）----------
say "[5/6] wshobson agents 4 个"
AGENTS_DIR="${HOME}/.claude/agents"
REPO="$VENDOR_DIR/wshobson"
repo https://github.com/wshobson/agents.git "$REPO"
mkdir -p "$AGENTS_DIR"
agent() {
  local src="$1" dest="$2" name="$3"
  if [ "$UPDATE" = true ]; then
    rm -f "$dest"; cp "$src" "$dest"; printf '  复制 %s\n' "$name"
  elif [ -e "$dest" ]; then
    skip "$name"
  else
    cp "$src" "$dest"; printf '  复制 %s\n' "$name"
  fi
}
agent "$REPO/plugins/python-development/agents/fastapi-pro.md" "$AGENTS_DIR/python-development-fastapi-pro.md" "fastapi-pro"
agent "$REPO/plugins/python-development/agents/django-pro.md" "$AGENTS_DIR/python-development-django-pro.md" "django-pro"
agent "$REPO/plugins/shell-scripting/agents/bash-pro.md" "$AGENTS_DIR/bash-pro.md" "bash-pro"
agent "$REPO/plugins/plugin-eval/agents/eval-judge.md" "$AGENTS_DIR/eval-judge.md" "eval-judge"

# ---------- ⑥ wshobson avoid-ai-writing（独立 skill 目录形态，复制到 ~/.claude/skills/，纯 markdown 零依赖）----------
say "[6/6] wshobson avoid-ai-writing"
REPO="$VENDOR_DIR/wshobson"
repo https://github.com/wshobson/agents.git "$REPO"
skill "$REPO/plugins/avoid-ai-writing/skills/avoid-ai-writing" "$SKILLS_DIR/avoid-ai-writing" "avoid-ai-writing"

# 临时缓存用完即删：vendor 目录只用于 clone 厂商仓库，安装完成后清理，不持久占用用户目录
if [ "$INSTALL_MODE" = "copy" ]; then
  rm -rf "$VENDOR_DIR"
  echo "  · 已清理临时缓存 $VENDOR_DIR"
fi

say "完成！重启 Claude Code 或 /reload-plugins 生效。"
