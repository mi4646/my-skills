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
MANIFEST=false
case "${1:-}" in
  --update)   UPDATE=true ;;
  --list)     LIST=true ;;
  --manifest) MANIFEST=true ;;
esac

say()  { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
skip() { printf '  · %s 已存在，跳过\n' "$*"; }

# 默认复制安装：软链指向缓存 vendor 目录，误删会断链，故全平台一律复制。
# vendor 为临时 clone 缓存（~/.cache/equipment-manager/vendor），安装完即删，不持久占用用户目录
INSTALL_MODE="${INSTALL_MODE:-copy}"
[ "$UPDATE" = true ] && LABEL="升级" || LABEL="安装"
[ "$LIST" = false ] && [ "$MANIFEST" = false ] && printf '  · 安装方式: %s | 模式: %s\n' "$INSTALL_MODE" "$LABEL"

# 三方装备元数据（来源与下方 repo URL 同源；第三字段=独立 skill 目录形态的已装清单，逗号分隔；第四字段=独立 agent 文件的已装清单）
# 2026-10-28 卸载四厂商装备（addyosmani/mattpocock/wshobson/msitarzewski），已装清单见 ~/.config/equipment-manager/state.json
EQUIP=(
  "hallmark|github.com/nutlope/hallmark|hallmark"
  "storage-analyzer|github.com/KKKKhazix/khazix-skills|storage-analyzer"
  "find-skills|github.com/vercel-labs/skills|find-skills"
  "api-and-interface-design|github.com/addyosmani/agent-skills|api-and-interface-design"
  "mattpocock-grill|github.com/mattpocock/skills|grill-me,grill-with-docs,grilling,domain-modeling"
)

# --manifest：每个已装 skill 输出一行 name<TAB>repo，供 scan-installed.sh --check 做双向一致性断言
if [ "$MANIFEST" = true ]; then
  for kv in "${EQUIP[@]}"; do
    IFS='|' read -r name repo indep agents <<< "$kv"
    for s in ${indep//,/ }; do printf '%s\t%s\n' "$s" "$repo"; done
  done
  exit 0
fi

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
# 第 4 参 sha：安装/更新后在副本目录写 .upstream-commit；--update 打印 旧 → 新
skill() {
  local src="$1" dest="$2" name="$3" sha="${4:-}" old=""
  [ -f "$dest/.upstream-commit" ] && old="$(cat "$dest/.upstream-commit")"
  if [ "$UPDATE" = true ]; then
    rm -rf "$dest"
    if [ "$INSTALL_MODE" = "copy" ]; then
      cp -r "$src" "$dest"; printf '  复制 %s\n' "$name"
    else
      ln -s "$src" "$dest"; printf '  软链 %s\n' "$name"
    fi
  elif [ -e "$dest" ]; then
    skip "$name"
    return
  else
    if [ "$INSTALL_MODE" = "copy" ]; then
      cp -r "$src" "$dest"; printf '  复制 %s\n' "$name"
    else
      ln -s "$src" "$dest"; printf '  软链 %s\n' "$name"
    fi
  fi
  [ -n "$sha" ] || return 0
  printf '%s\n' "$sha" > "$dest/.upstream-commit"
  if [ -n "$old" ] && [ "$old" != "$sha" ]; then
    printf '  版本 %s → %s\n' "$old" "$sha"
  elif [ -z "$old" ]; then
    printf '  版本 %s（首次记录）\n' "$sha"
  fi
}

# ---------- ① hallmark ----------
say "[1/5] hallmark"
REPO="$VENDOR_DIR/hallmark"
repo https://github.com/nutlope/hallmark.git "$REPO"
skill "$REPO/skills/hallmark" "$SKILLS_DIR/hallmark" "hallmark" "$(git -C "$REPO" rev-parse --short HEAD)"

# ---------- ② storage-analyzer ----------
say "[2/5] storage-analyzer"
REPO="$VENDOR_DIR/khazix-skills"
repo https://github.com/KKKKhazix/khazix-skills.git "$REPO"
skill "$REPO/storage-analyzer" "$SKILLS_DIR/storage-analyzer" "storage-analyzer" "$(git -C "$REPO" rev-parse --short HEAD)"

# ---------- ③ find-skills ----------
say "[3/5] find-skills"
REPO="$VENDOR_DIR/vercel-labs-skills"
repo https://github.com/vercel-labs/skills.git "$REPO"
skill "$REPO/skills/find-skills" "$SKILLS_DIR/find-skills" "find-skills" "$(git -C "$REPO" rev-parse --short HEAD)"

# ---------- ④ api-and-interface-design ----------
say "[4/5] api-and-interface-design"
REPO="$VENDOR_DIR/addyosmani-agent-skills"
repo https://github.com/addyosmani/agent-skills.git "$REPO"
skill "$REPO/skills/api-and-interface-design" "$SKILLS_DIR/api-and-interface-design" "api-and-interface-design" "$(git -C "$REPO" rev-parse --short HEAD)"

# ---------- ⑤ mattpocock grill 四件套（两个入口壳依赖后两个） ----------
say "[5/5] mattpocock grill"
REPO="$VENDOR_DIR/mattpocock-skills"
repo https://github.com/mattpocock/skills.git "$REPO"
SHA="$(git -C "$REPO" rev-parse --short HEAD)"
for pair in "productivity/grill-me:grill-me" "engineering/grill-with-docs:grill-with-docs" "productivity/grilling:grilling" "engineering/domain-modeling:domain-modeling"; do
  skill "$REPO/skills/${pair%%:*}" "$SKILLS_DIR/${pair##*:}" "${pair##*:}" "$SHA"
done

# 临时缓存用完即删：vendor 目录只用于 clone 厂商仓库，安装完成后清理，不持久占用用户目录
if [ "$INSTALL_MODE" = "copy" ]; then
  rm -rf "$VENDOR_DIR"
  echo "  · 已清理临时缓存 $VENDOR_DIR"
fi

say "完成！重启 Claude Code 或 /reload-plugins 生效。"
