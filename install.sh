#!/usr/bin/env bash
# 一键安装/升级第三方技能装备
# 用法：
#   bash install.sh           幂等安装（已装跳过）
#   bash install.sh --update  升级（git pull 上游 + 强制重新复制/软链）
# 依赖：git、bash 4+（Windows 用 Git Bash）
set -euo pipefail

SKILLS_DIR="${HOME}/.claude/skills"
VENDOR_DIR="${HOME}/skills"

UPDATE=false
LIST=false
case "${1:-}" in
  --update) UPDATE=true ;;
  --list)   LIST=true ;;
esac

say()  { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
skip() { printf '  · %s 已存在，跳过\n' "$*"; }

# 默认复制安装：软链指向 ~/skills/ vendor 目录，误删该目录会断链，故全平台一律复制
INSTALL_MODE="${INSTALL_MODE:-copy}"
[ "$UPDATE" = true ] && LABEL="升级" || LABEL="安装"
[ "$LIST" = false ] && printf '  · 安装方式: %s | 模式: %s\n' "$INSTALL_MODE" "$LABEL"

# 三方装备元数据（来源与下方 repo URL 同源）
EQUIP=(
  "mattpocock|github.com/mattpocock/skills"
  "baoyu-design|github.com/jimliu/baoyu-design"
  "hallmark|github.com/nutlope/hallmark"
  "storage-analyzer|github.com/KKKKhazix/khazix-skills"
)

# 三方装备清单：扫描已安装目录实时统计（不联网、不写盘）
if [ "$LIST" = true ]; then
  printf '\n\033[1;36m==> 三方装备清单\033[0m\n'
  printf '%-16s %-6s %-8s %-8s %s\n' "资产" "插件" "技能数" "agents" "来源"
  for kv in "${EQUIP[@]}"; do
    name="${kv%%|*}"; repo="${kv#*|}"
    d="$SKILLS_DIR/$name"
    plugin=$([ -f "$d/.claude-plugin/plugin.json" ] && echo ✓ || echo -)
    n=0
    [ -d "$d/skills" ] && n=$((n + $(ls "$d/skills" | wc -l)))
    [ -f "$d/SKILL.md" ] && n=$((n + 1))
    [ -d "$d/built-in-skills" ] && n=$((n + $(ls "$d/built-in-skills" | wc -l)))
    a=0
    [ -d "$d/agents" ] && a=$(find "$d/agents" -maxdepth 1 -name '*.md' | wc -l)
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

# ---------- ① mattpocock 精选 10 个 ----------
say "[1/4] mattpocock 精选 10 个"
REPO="$VENDOR_DIR/mattpocock"
repo https://github.com/mattpocock/skills.git "$REPO"

PLUGIN_DIR="$SKILLS_DIR/mattpocock"
mkdir -p "$PLUGIN_DIR/skills" "$PLUGIN_DIR/.claude-plugin"
if [ ! -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
  cat > "$PLUGIN_DIR/.claude-plugin/plugin.json" <<'EOF'
{"name":"mattpocock","version":"1.0.0","description":"mattpocock/skills 精选 10 个"}
EOF
fi

MAP=(
  "obsidian-vault:personal/obsidian-vault"
  "edit-article:personal/edit-article"
  "git-guardrails-claude-code:misc/git-guardrails-claude-code"
  "grill-with-docs:engineering/grill-with-docs"
  "domain-modeling:engineering/domain-modeling"
  "handoff:productivity/handoff"
  "grill-me:productivity/grill-me"
  "prototype:engineering/prototype"
  "research:engineering/research"
  "resolving-merge-conflicts:engineering/resolving-merge-conflicts"
)
for kv in "${MAP[@]}"; do
  name="${kv%%:*}"; src="${kv#*:}"
  skill "$REPO/skills/$src" "$PLUGIN_DIR/skills/$name" "$name"
done

# ---------- ② baoyu-design ----------
say "[2/4] baoyu-design"
REPO="$VENDOR_DIR/baoyu-design"
repo https://github.com/jimliu/baoyu-design.git "$REPO"
skill "$REPO/skills/baoyu-design" "$SKILLS_DIR/baoyu-design" "baoyu-design"

# ---------- ③ hallmark ----------
say "[3/4] hallmark"
REPO="$VENDOR_DIR/hallmark"
repo https://github.com/nutlope/hallmark.git "$REPO"
skill "$REPO/skills/hallmark" "$SKILLS_DIR/hallmark" "hallmark"

# ---------- ④ storage-analyzer ----------
say "[4/4] storage-analyzer"
REPO="$VENDOR_DIR/khazix-skills"
repo https://github.com/KKKKhazix/khazix-skills.git "$REPO"
skill "$REPO/storage-analyzer" "$SKILLS_DIR/storage-analyzer" "storage-analyzer"

say "完成！重启 Claude Code 或 /reload-plugins 生效。"
