#!/usr/bin/env python3
"""校验 SKILL.md 与 agent 定义的 YAML frontmatter。

PostToolUse hook 用法: printf '{"tool_input":{"file_path":"..."}}' | check-frontmatter.py
独立扫描用法:          check-frontmatter.py --scan [目录 ...]   # 默认扫 ~/.claude/skills 与 ~/.claude/agents

不通过 -> stderr 打印原因 + exit 2, Claude Code 会把它回喂给模型当场修。
"""
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # 没 pyyaml 就放行，绝不因缺依赖拦正常写盘
    sys.exit(0)

REQUIRED = ("name", "description")


SKIP_SEGMENTS = {"node_modules", ".cache", ".git"}


def targets(path: Path) -> bool:
    parts = path.parts
    if any(seg in SKIP_SEGMENTS for seg in parts):
        return False
    return path.name == "SKILL.md" or (path.suffix == ".md" and path.parent.name == "agents")


def problems(path: Path) -> list:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [f"读不到文件: {e}"]
    if not text.startswith("---"):
        return []  # 无 frontmatter（如 # SKILL: 纯清单文档）非「坏了」，不在本校验职责内
    try:
        block = text[3 : text.index("\n---", 3)]
    except ValueError:
        return ["frontmatter 没有闭合的 ---"]
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as e:
        return [f"YAML 解析失败: {' '.join(str(e).split())[:200]}"]
    if not isinstance(data, dict):
        return [f"frontmatter 不是键值表，实为 {type(data).__name__}"]
    return [f"缺必填字段 {k}" for k in REQUIRED if k not in data]


def main() -> int:
    args = sys.argv[1:]

    if args and args[0] == "--scan":
        roots = [Path(a).expanduser() for a in args[1:]] or [
            Path.home() / ".claude" / "skills",
            Path.home() / ".claude" / "agents",
        ]
        bad = total = 0
        for root in roots:
            if not root.is_dir():
                continue
            for p in sorted(root.rglob("*.md")):
                if not targets(p):
                    continue
                total += 1
                for msg in problems(p):
                    bad += 1
                    print(f"{p}: {msg}")
        print(f"--scan: 共 {total} 个定义文件，{bad} 处问题")
        return 1 if bad else 0

    raw = sys.stdin.read().strip()
    if not raw:
        return 0
    try:
        path = Path(json.loads(raw)["tool_input"]["file_path"])
    except (KeyError, TypeError, ValueError):
        return 0
    if not targets(path):
        return 0
    msgs = problems(path)
    if msgs:
        print("frontmatter 校验未通过：", file=sys.stderr)
        for m in msgs:
            print(f"  - {path}: {m}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
