#!/usr/bin/env bash
# scan-installed.sh — 本地装备地图·事实层扫描（纯只读）
# 输出 TSV: NAME SOURCE FORM ENABLED DESCRIPTION
# --check 模式: 自动断言（见设计文档第 1 节验证标准 1-5）
set -euo pipefail

EM_HOME="${EM_HOME:-$HOME/.claude}"

# 兼容 darwin 的 realpath 缺失
realpath_() { case "$(uname -s)" in Darwin) python3 -c "import os,sys;print(os.path.realpath(sys.argv[1]))" "$1";; *) realpath "$1";; esac; }

die() { echo "ERROR: $*" >&2; exit 1; }
command -v claude >/dev/null 2>&1 || die "claude CLI 不可用"

print_row() { printf '%s\t%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" "$5"; }

# 插件部分：官方 CLI 权威来源
scan_plugins() {
  local plugin list_line name mp details
  # plugin list 的块格式: "  ❯ name@marketplace" + Version/Scope/Status 行
  while IFS= read -r list_line; do
    case "$list_line" in
      "  ❯ "*)
        name="${list_line#  ❯ }"
        mp="${name#*@}"; name="${name%@*}"
        if [ "$mp" = "skills-dir" ]; then
          # skills-dir 插件无缓存路径，直接读 ~/.claude/skills/<name>/ 下 skills
          scan_skills_dir_plugin "$name"
        else
          details="$(claude plugin details "${name}@${mp}" 2>/dev/null)" || continue
          # LSP/工具插件天然报 Skills (0)，跳过
          if echo "$details" | grep -qE '^  Skills \(0\)'; then continue; fi
          scan_plugin_cache "$name" "$mp" "$details"
        fi
        ;;
    esac
  done < <(claude plugin list 2>/dev/null | grep -E '^  ❯ ')
}

# 从 details 的 Skills (N) 清单 + 缓存路径读各 SKILL.md 的 description
scan_plugin_cache() {
  local name="$1" mp="$2" details="$3" skill_line skill
  local skills_line cachedir
  skills_line="$(echo "$details" | grep -E '^  Skills \([0-9]+\)' | head -1 || true)"
  [ -z "$skills_line" ] && return
  # skills_line = "  Skills (14)  brainstorming, executing-plans, ..."
  cachedir="$EM_HOME/plugins/cache/$mp/$name"
  [ -d "$cachedir" ] || return
  # 版本目录取最新（sort 排序末尾，旧版本如 6.1.1 忽略）
  local ver="$(ls "$cachedir" 2>/dev/null | sort -V | tail -1)"
  [ -n "$ver" ] || return
  for skill_line in $(echo "${skills_line#*  Skills (}" | sed 's/^[0-9]*)[[:space:]]*//' | tr ',' '\n' | tr -d ' ' | grep -v '^$'); do
    skill="$cachedir/$ver/skills/$skill_line"
    [ -f "$skill/SKILL.md" ] || continue
    print_row "$skill_line" "$name" "skill" "yes" "$(frontmatter_desc "$skill/SKILL.md")"
  done
}

# skills-dir 插件（如 my-skills@skills-dir）：直接读 ~/.claude/skills/<name>/skills/
scan_skills_dir_plugin() {
  local name="$1" d skill
  for d in "$EM_HOME/skills/$name/skills/"*/; do
    [ -f "$d/SKILL.md" ] || continue
    skill="$(basename "$d")"
    print_row "$skill" "$name" "skill" "yes" "$(frontmatter_desc "$d/SKILL.md")"
  done
}

# 提取 SKILL.md frontmatter 的 description（第一行非空 description）
frontmatter_desc() {
  awk 'NR==1&&$0=="---"{infm=1;next} infm&&$0=="---"{exit} infm&&/^description:/{sub(/^description:[[:space:]]*/, ""); print; exit}' "$1"
}

# 顶层扁平 skill：目录含 SKILL.md 即算一个；排除插件包（.claude-plugin/plugin.json）
# gstack 命令（名字 ∈ gstack 仓库内部含 SKILL.md 的目录）→ source=gstack
scan_flat_skills() {
  local d name in_gstack
  for d in "$EM_HOME/skills/"*/; do
    name="$(basename "$d")"
    [ -f "$d/SKILL.md" ] || continue
    [ -f "$d/.claude-plugin/plugin.json" ] && continue   # 插件包（my-skills）排除
    [ "$name" = "gstack" ] && continue                    # gstack 容器目录排除（命令已逐条计）
    if [ -d "$EM_HOME/skills/gstack/$name" ] && [ -f "$EM_HOME/skills/gstack/$name/SKILL.md" ]; then
      in_gstack=yes
    else
      in_gstack=no
    fi
    if [ "$in_gstack" = yes ]; then
      print_row "$name" "gstack" "skill" "yes" "$(frontmatter_desc "$d/SKILL.md")"
    else
      print_row "$name" "顶层" "skill" "yes" "$(frontmatter_desc "$d/SKILL.md")"
    fi
  done
}

# agents: 每个 .md = 1 个 agent
scan_agents() {
  local f
  for f in "$EM_HOME/agents/"*.md; do
    [ -f "$f" ] || continue
    print_row "$(basename "$f" .md)" "agents" "agent" "yes" ""
  done
}

# gstack 5 套宿主副本折叠成一条来源标注（不逐条输出）
gstack_host_copies() {
  local n=0 h
  for h in .cursor .opencode .agents .factory .kiro; do
    [ -d "$EM_HOME/skills/gstack/$h/skills" ] && n=$((n+1))
  done
  if [ "$n" -gt 0 ]; then print_row "gstack@宿主副本" "gstack" "skill" "yes" "${n} 套宿主副本（.cursor/.opencode/.agents/.factory/.kiro）折叠"; fi
}

# --check: 设计文档第 1 节验证标准 1-5
check_all() {
  local fail=0 statejson tagsfile out
  statejson="${EM_CONFIG:-$HOME/.config/equipment-manager}/state.json"

  # 断言 1: 覆盖度——插件 skill 数 + 顶层扁平 + agents 无遗漏（输出行数 ≥ 断言基线，避免重复计数陷阱）
  local n_plugin n_flat n_agent
  n_plugin=$(scan_plugins | grep -c $'\tskill\tyes' || true)
  n_flat=$(scan_flat_skills | grep -c $'\tskill\tyes' || true)
  n_agent=$(scan_agents | grep -c $'\tagent\tyes' || true)
  echo "CHECK 覆盖度: 插件skill=$n_plugin 顶层扁平=$n_flat agents=$n_agent"
  [ "$n_flat" -ge 60 ] || { echo "FAIL 1: 顶层扁平 skill 异常偏少 ($n_flat < 60)"; fail=1; }
  [ "$n_agent" -ge 5 ] || { echo "FAIL 1: agents 偏少 ($n_agent < 5)"; fail=1; }

  # 断言 2: LSP/工具插件（Skills (0)）不得进清单
  local lsp_leak
  lsp_leak=$( { scan_plugins; } | grep -E '^(pyright-lsp|typescript-lsp|playwright|context7)\t' || true)
  [ -z "$lsp_leak" ] || { echo "FAIL 2: LSP/工具插件泄漏: $lsp_leak"; fail=1; }

  # 断言 3: gstack 宿主副本折叠后不出现 54×5 重复——每 gstack 命令名只 1 行
  local dup
  dup=$( { scan_flat_skills; } | awk -F'\t' '$2=="gstack"' | awk -F'\t' '{print $1}' | sort | uniq -d)
  [ -z "$dup" ] || { echo "FAIL 3: gstack 命令重复: $dup"; fail=1; }

  # 断言 4: inventory 完整性——每个 enabled=true 装备都有 purpose/tags（完整报告，不中途退出）
  if [ -f "$statejson" ]; then
    if out=$(python3 - "$statejson" <<'PYEOF'
import json,sys
d=json.load(open(sys.argv[1]))
inv=d.get("inventory",{})
bad=[f"FAIL 4: {k} enabled 但缺 purpose/tags" for k,v in inv.items()
     if v.get("enabled") and (not v.get("purpose") or not v.get("tags"))]
if bad:
    print("\n".join(bad))
else:
    print(f"CHECK inventory: {len(inv)} 条, enabled 装备全部有 purpose/tags")
PYEOF
    ); then
      echo "$out"
      if echo "$out" | grep -q '^FAIL 4:'; then fail=1; fi
    else
      echo "FAIL 4: state.json 解析失败 ($statejson)"; fail=1
    fi
  else
    echo "FAIL 4: state.json 不存在 ($statejson)"; fail=1
  fi

  # 断言 5: tags 合规——∈ 受控词表 且 数量 2-4（完整报告，不中途退出）
  if [ -f "$statejson" ]; then
    if out=$(python3 - "$statejson" <<'PYEOF'
import json,sys
d=json.load(open(sys.argv[1]))
WORDS={"需求澄清","方案审查","代码质量","测试","部署发布","上下文管理","调试排障","创意评估","教学","装备管理","自动化","评测"}
bad=[]
for k,v in d.get("inventory",{}).items():
    for t in v.get("tags",[]):
        if t not in WORDS:
            bad.append(f"FAIL 5: {k}.tags 含非词表项「{t}」")
    n=len(v.get("tags",[]))
    if not (2 <= n <= 4):
        bad.append(f"FAIL 5: {k}.tags 数量 {n}（需 2-4）")
if bad:
    print("\n".join(bad))
else:
    print("CHECK tags: 全部 ∈ 受控词表 且 数量 2-4")
PYEOF
    ); then
      echo "$out"
      if echo "$out" | grep -q '^FAIL 5:'; then fail=1; fi
    else
      echo "FAIL 5: state.json 解析失败 ($statejson)"; fail=1
    fi
  fi

  [ "$fail" = 0 ] || die "check_all 失败"
  echo "CHECK: 全部通过"
}

case "${1:-}" in
  --check) check_mode=1 ;;
  -h|--help) echo "scan-installed.sh — 本地装备地图事实层（纯只读）
用法: $0 [--check]
输出: NAME SOURCE FORM ENABLED DESCRIPTION (TSV)
--check: 自动断言覆盖度/合规性，失败非零退出"; exit 0 ;;
esac

check_mode=${check_mode:-0}
scan_plugins
scan_flat_skills
scan_agents
gstack_host_copies
# Task 2 追加: check_all (check_mode 时执行)
[ "$check_mode" = 1 ] && check_all
exit 0
