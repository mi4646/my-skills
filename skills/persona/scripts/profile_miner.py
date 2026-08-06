#!/usr/bin/env python3
"""profile_miner.py — 用户画像自学习 miner 原型（只读）

从 Claude Code session 日志提取「用户自己输入的话」，聚合为候选画像证据。
严格只读：不写任何文件，不修改任何配置。

用法：
  python3 profile_miner.py [--days 30] [--min-len 20] [--limit 5] [--json]

设计依据：见 ~/.gstack/projects/mi4646-my-skills/anonymous-main-design-user-profile-self-learning-20260806-113000.md
"""
import argparse
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# 纯确认词黑名单（只放"无信息量"的词，别误伤真实输入）
BLACKLIST = {
    "继续", "继续吧", "continue", "yes", "ok", "好的", "好", "可以",
    "👍", "✓", "done", "确认", "对", "行", "嗯", "嗯嗯", "谢谢", "好的，谢谢",
}
# 英文停用词（轻量）
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "is", "are", "was", "were", "be", "been", "it", "this", "that", "these",
    "those", "you", "your", "please", "can", "could", "would", "should",
    "have", "has", "had", "do", "does", "did", "i", "we", "me", "my", "if",
    "then", "than", "but", "not", "no", "at", "by", "from", "as", "into",
    "about", "after", "before", "what", "when", "where", "which", "who",
    "why", "how", "all", "any", "both", "each", "few", "more", "most",
    "other", "some", "such", "only", "own", "same", "so", "than", "too",
    "very", "just", "also", "again", "once", "here", "there", "now", "then",
    # 弱信息通用词（无画像区分度）
    "call", "file", "line", "directory", "home", "anonymous", "real", "back",
    "above", "self", "run", "www", "another", "exception", "old", "issues",
    "task", "code", "one", "list", "time", "repo", "user", "manager",
    "completed", "resolved", "version", "lib", "tmp", "dir", "path", "name",
    "case", "need", "need", "make", "make", "want", "get", "let", "know",
    "thing", "way", "part", "use", "used", "using", "see", "show", "look",
    "work", "works", "working", "put", "set", "create", "add", "remove",
    "first", "last", "next", "new", "old", "good", "bad", "well", "better",
    "really", "actually", "still", "already", "always", "never", "often",
}


def clean_user_input(content):
    """去掉系统注入块，返回(干净文本, 是否仍视为用户输入)。"""
    # 去掉 <local-command-*> / <command-*> / <bash-*> 注入块
    content = re.sub(r"<(?:local-command|command|bash)-[^>]*>.*?</(?:local-command|command|bash)-[^>]*>",
                     " ", content, flags=re.S)
    content = re.sub(r"</?(?:local-command|command|bash)-[^>]*>", " ", content)
    # 去掉 <task-notification> 注入块（Claude Code 自动插入的子代理完成通知，非用户输入）
    content = re.sub(r"<task-notification>.*?</task-notification>", " ", content, flags=re.S)
    content = re.sub(r"</?task-notification[^>]*>", " ", content)
    # 去掉 skill 注入文本（Base directory... / AUTO-GENERATED / <!-- -->
    content = re.sub(r"Base directory for this skill:.*?(?=\n|$)", " ", content, flags=re.S)
    content = re.sub(r"<!--.*?-->", " ", content, flags=re.S)
    content = re.sub(r"<[^>]+>", " ", content)
    # 去掉服务器终端残留行
    content = re.sub(r"\[root@[^\]]*\]\s*(?:#|\$)", " ", content)
    content = re.sub(r"\s+", " ", content).strip()
    # skill 正文注入：以 markdown 标题开头且超长的块（Claude Code 把 slash 命令调用的 skill 内容记为 user turn）
    if re.match(r"^#{1,3} ", content) and len(content) > 150:
        return "", False
    # 上下文压缩摘要注入
    if re.match(r"^(this session is being continued|the summary below covers)", content.lower()):
        return "", False
    if "request interrupted by user" in content.lower():
        return "", False
    # 子代理任务注入特征：面向 agent 的指令/派发，非用户自由输入
    head = content[:40].lower()
    if re.match(r"^(you are|你是|the coordinator|review (the |this )|read (the|this) design|i need you|task:|你的任务)", head):
        return "", False
    return content, True


def is_sdk_replay(entry):
    """SDK 批量重放检测：entrypoint 为 sdk-* 的 user turn 是评测/脚本注入，非用户交互输入。
    （如 equipment-manager benchmark 用 sdk-cli/sdk-py 批量重放 synthetic 查询，会污染画像证据）"""
    return (entry.get("entrypoint") or "").startswith("sdk")


def user_turns(path, min_len, since_ts):
    """yield (text, ts, source_path) for each qualifying user turn in a jsonl."""
    try:
        fh = open(path, encoding="utf-8")
    except OSError:
        return
    mtime = os.path.getmtime(path)
    if since_ts and mtime < since_ts:
        fh.close()
        return
    with fh:
        # SDK 批量重放 session 以 queue-operation 标记开头，整段为非交互输入，跳过
        first = fh.readline()
        if first and '"queue-operation"' in first:
            return
        fh.seek(0)
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") != "user":
                continue
            if is_sdk_replay(e):
                continue
            m = e.get("message") or {}
            content = m.get("content")
            if isinstance(content, list):  # content blocks 形式
                texts = [
                    b.get("text", "")
                    for b in content
                    if isinstance(b, dict) and b.get("type") == "text"
                ]
                content = "\n".join(texts)
            if not isinstance(content, str):
                continue
            content, keep = clean_user_input(content)
            if not keep or len(content) < min_len:  # 过滤：长度 + 注入
                continue
            low = content.lower()
            if low in BLACKLIST or low[:8] in BLACKLIST:  # 过滤：纯确认词
                continue
            ts = e.get("timestamp") or ""
            yield content, ts, str(path)


def project_label(path):
    """把 -var-www-demo → /var/www/demo，-home-anonymous-my-skills → ~/my-skills"""
    name = path.parent.name  # jsonl 所在目录 = 项目名
    m = re.match(r"^-(home-anonymous)(.*)$", name)
    if m:
        inner = m.group(2).replace("-", "/")
        return "~" + inner if inner else "~"
    m = re.match(r"^-var-www-(.+)$", name)
    if m:
        return "/var/www/" + m.group(1).replace("-", "/")
    return name


# 常见代码噪声词（用户粘贴代码的残留，不作为画像线索）
NOISE = {
    "null", "true", "false", "undefined", "const", "let", "var", "function",
    "return", "import", "export", "async", "await", "this", "class", "new",
}


def tokens(text):
    """轻量中英文 token：英文单词(≥3字符) + 连续中文串，去停用/噪声"""
    out = []
    for m in re.finditer(r"[a-z]+|[一-鿿]{2,}", text.lower()):
        t = m.group(0)
        if t.isascii():
            if len(t) < 3 or t in STOPWORDS or t in NOISE:
                continue
        out.append(t)
    return out


def load_state(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def save_state(path, state):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)


def confidence(n_sessions, last_ts, corrections, now, decay_days, penalty):
    """置信度 = min(1, session/3) × 衰减因子 × penalty^纠正次数（设计文档公式）"""
    support = min(1.0, n_sessions / 3)
    days_since = 0.0
    if last_ts:
        try:
            last_dt = datetime.fromisoformat(last_ts.replace("Z", "+00:00"))
            days_since = max(0.0, (now - last_dt.timestamp()) / 86400)
        except ValueError:
            pass
    decay = max(0.1, 1 - days_since / (2 * decay_days))
    return support * decay * (penalty ** corrections), days_since


def self_test():
    """最小自检：核心逻辑（过滤/分词/置信度公式）出错即断言失败。"""
    # clean_user_input：注入剔除
    assert clean_user_input("优化一下这段 FastAPI 接口的性能")[0] == "优化一下这段 FastAPI 接口的性能"
    assert clean_user_input("<local-command-caveat>xx</local-command-caveat> 你好")[0] == "你好"
    assert clean_user_input("<bash-stdout>out</bash-stdout> <bash-input>ls</bash-input>")[0] == ""
    assert clean_user_input("<task-notification>任务完成</task-notification> 你好")[0] == "你好"
    assert clean_user_input("## When to invoke this skill " + "x" * 200)[1] is False   # skill 正文
    assert clean_user_input("You are a reviewer, judge independently. " + "y" * 50)[1] is False  # 子代理注入
    assert clean_user_input("This session is being continued from a previous conversation")[1] is False  # 压缩摘要
    # tokens：停用词/噪声过滤，保留领域词
    toks = tokens("fastapi python the skill null 优化 性能")
    assert "fastapi" in toks and "python" in toks and "skill" in toks
    assert "the" not in toks and "null" not in toks and "优化" in toks
    # is_sdk_replay：SDK 批量重放（评测/脚本注入）应被排除，真实 cli 交互应保留
    assert is_sdk_replay({"type": "user", "entrypoint": "sdk-cli"})
    assert is_sdk_replay({"type": "user", "entrypoint": "sdk-py"})
    assert is_sdk_replay({"type": "user", "entrypoint": "sdk"})
    assert not is_sdk_replay({"type": "user", "entrypoint": "cli"})
    assert not is_sdk_replay({"type": "user", "entrypoint": ""})
    assert not is_sdk_replay({"type": "user"})
    # confidence 公式
    now = time.time()
    c1, _ = confidence(9, "", 0, now, 90, 0.5)      # 9 session 满支持、新证据 → 1.0
    assert abs(c1 - 1.0) < 1e-6, c1
    c2, _ = confidence(9, "", 2, now, 90, 0.5)      # 2 次纠正 → 0.25
    assert abs(c2 - 0.25) < 1e-6, c2
    c3, _ = confidence(1, "", 0, now, 90, 0.5)      # 1 session → support 1/3
    assert abs(c3 - 1 / 3) < 1e-6, c3
    old_ts = datetime.fromtimestamp(now - 90 * 86400).isoformat()
    c4, _ = confidence(9, old_ts, 0, now, 90, 0.5)  # 90 天前证据 → decay = 1-90/180 = 0.5
    assert abs(c4 - 0.5) < 1e-6, c4
    print("self-test: 全部通过（clean_user_input/tokens/confidence）")
    return 0


def main():
    ap = argparse.ArgumentParser(description="从 Claude Code 日志提取用户输入（只读）")
    ap.add_argument("--days", type=int, default=30, help="只扫最近 N 天的日志（按文件 mtime）")
    ap.add_argument("--min-len", type=int, default=20, help="用户输入最短字符数")
    ap.add_argument("--limit", type=int, default=5, help="每个项目展示的样本条数")
    ap.add_argument("--json", action="store_true", help="输出 JSON（候选画像证据）")
    ap.add_argument("--verify", default="", help="验证模式：搜含该关键词的用户输入，不足 --min-sessions 个 session 即 FAIL")
    ap.add_argument("--min-sessions", type=int, default=2, help="verify 通过所需的最少不同 session 数")
    ap.add_argument("--evaluate", action="store_true", help="输出候选画像条目（关键词 → 置信度/状态）")
    ap.add_argument("--correct", default="", help="记录一次纠正降权：--correct <关键词>，写入状态文件")
    ap.add_argument("--state", default=os.path.expanduser("~/.config/equipment-manager/miner-state.json"),
                    help="纠正记录状态文件（默认 ~/.config/equipment-manager/miner-state.json）")
    # 置信度参数（对应设计文档参数表，可覆盖校准）
    ap.add_argument("--decay-days", type=int, default=90, help="preferenceDecayDays：无新证据过期天数")
    ap.add_argument("--correction-penalty", type=float, default=0.5, help="correctionPenalty：纠正一次对置信度的降权")
    ap.add_argument("--min-confidence", type=float, default=0.5, help="minConfidence：亮为建议确认的置信度下限")
    ap.add_argument("--self-test", action="store_true", help="运行最小自检（核心逻辑断言）")
    ap.add_argument("--projects", default=str(Path.home() / ".claude" / "projects"),
                    help="日志根目录")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())

    # --correct：记录纠正（写状态文件，仅动自身状态，不动日志/配置）
    if args.correct:
        state = load_state(args.state)
        kw = args.correct.lower()
        entry = state.setdefault(kw, {"corrections": 0})
        entry["corrections"] = entry.get("corrections", 0) + 1
        save_state(args.state, state)
        print(f"已记录纠正: {kw} → 纠正 {entry['corrections']} 次（置信度 ×{args.correction_penalty ** entry['corrections']:.3f}）")
        return

    since = time.time() - args.days * 86400 if args.days else 0
    root = Path(args.projects)
    files = list(root.rglob("*.jsonl"))
    # 按 mtime 从新到旧，总量兜底：最多扫前 200 个文件、总预算 60s
    files = sorted(
        [f for f in files if os.path.getmtime(f) >= since],
        key=os.path.getmtime,
        reverse=True,
    )[:200]

    per_project = defaultdict(list)   # project -> [(ts, text, source)]
    verify_hits = []                  # [(label, ts, text, source)] for --verify
    token_stats = {}                  # keyword -> {sessions:set, last_ts, count}（仅 --evaluate）
    kw_counter = Counter()
    n_turns = 0
    n_chars = 0
    t0 = time.time()

    for f in files:
        if time.time() - t0 > 60:  # 兜底：超时截断
            print("!! 扫描超时（60s），本次仅覆盖部分日志", file=sys.stderr)
            break
        for text, ts, src in user_turns(f, args.min_len, since):
            label = project_label(f)
            per_project[label].append((ts, text, src))
            n_turns += 1
            n_chars += len(text)
            kw_counter.update(tokens(text))
            if args.verify and args.verify.lower() in text.lower():
                verify_hits.append((label, ts, text, src))
            if args.evaluate:
                for t in tokens(text):
                    st = token_stats.setdefault(t, {"sessions": set(), "last_ts": "", "count": 0})
                    st["count"] += 1
                    st["sessions"].add(src)
                    if ts and ts > st["last_ts"]:
                        st["last_ts"] = ts

    # 证据追溯 verify：搜支持证据，不足 min-sessions 个不同 session 即 FAIL
    if args.verify:
        sessions = set()
        print(f"== verify \"{args.verify}\" ==")
        for label, ts, text, src in verify_hits[:20]:
            sessions.add(src)
            print(f"  [{label}] {ts[:10]} :: {text[:110]}  @ {Path(src).name}")
        n_sess = len(sessions)
        print(f"\n  命中 {len(verify_hits)} 条 | 来自 {n_sess} 个 session | 要求 ≥{args.min_sessions}")
        verdict = "PASS" if n_sess >= args.min_sessions else "FAIL（证据不足，候选丢弃）"
        print(f"  结论: {verdict}")
        sys.exit(0 if n_sess >= args.min_sessions else 1)

    # 候选画像条目：关键词 → 置信度（公式见 confidence()），供用户逐个确认
    if args.evaluate:
        state = load_state(args.state)
        now = time.time()
        rows = []
        for kw, st in token_stats.items():
            corr = state.get(kw, {}).get("corrections", 0)
            c, days = confidence(len(st["sessions"]), st["last_ts"], corr, now,
                                 args.decay_days, args.correction_penalty)
            rows.append((c, kw, len(st["sessions"]), days, corr, st["count"]))
        rows.sort(key=lambda r: -r[0])
        print("== 候选画像条目（参数: decay=%dd penalty=%.1f minConf=%.1f）==" % (
            args.decay_days, args.correction_penalty, args.min_confidence))
        print("  %-24s %7s %7s %6s %7s %6s  %s" % (
            "关键词", "session", "次数", "纠正", "距证据", "置信度", "状态"))
        for c, kw, ns, days, corr, cnt in rows[:30]:
            status = "✅ 建议确认" if c >= args.min_confidence else ("◐ 低证据" if c >= 0.3 else "○ 衰减/丢弃")
            print("  %-24s %7d %7d %6d %6.0fd %7.2f  %s" % (
                kw, ns, cnt, corr, days, c, status))
        n_confirm = sum(1 for r in rows if r[0] >= args.min_confidence)
        print(f"\n  候选 {len(rows)} 条 | 建议确认 {n_confirm} 条 | 其余为低证据/衰减")
        return

    n_projects = len(per_project)
    n_files = len(files)

    if args.json:
        # 候选画像证据 JSON：每项目提炼 top 关键词 + 样本证据
        out = {
            "meta": {"files": n_files, "turns": n_turns, "chars": n_chars,
                     "projects": n_projects, "days": args.days},
            "keywords": [w for w, _ in kw_counter.most_common(40)],
            "projects": [],
        }
        for label, turns in sorted(per_project.items(), key=lambda kv: -len(kv[1])):
            turns_sorted = sorted(turns, key=lambda x: x[0], reverse=True)  # 按 ts 新→旧
            samples = [{"ts": ts, "text": text[:200], "source": src}
                       for ts, text, src in turns_sorted[:3]]
            out["projects"].append({
                "project": label, "turns": len(turns), "samples": samples,
            })
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    # 人类可读输出
    print(f"== 扫描结果 ==")
    print(f"  文件 {n_files} | 用户输入 {n_turns} 条 | {n_chars} 字符 | {n_projects} 个项目（近 {args.days} 天）")
    print(f"\n== Top 关键词（候选画像线索）==")
    print("  " + "  ".join(f"{w}×{c}" for w, c in kw_counter.most_common(20)))
    print(f"\n== 各项目用户输入样本 ==")
    for label, turns in sorted(per_project.items(), key=lambda kv: -len(kv[1]))[:8]:
        turns_sorted = sorted(turns, key=lambda x: x[0], reverse=True)
        print(f"\n  [{label}] {len(turns)} 条")
        for ts, text, _src in turns_sorted[: args.limit]:
            text1 = text.replace("\n", " ")[:120]
            print(f"    · {text1}")


if __name__ == "__main__":
    main()
