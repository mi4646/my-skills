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
# 中文弱信息词/口语填充（与英文 STOPWORDS 对称；miner 是中文日志，无停用词表导致
# 「这个/里面/什么意思」全进候选，挤占真实画像信号）
CHINESE_WEAK = {
    "这个", "这些", "那个", "那些", "里面", "这里", "那里", "怎么", "怎么样",
    "为什么", "什么", "一个", "一些", "一下", "东西", "地方", "情况", "时候",
    "有什么疑问", "与我沟通", "你有什么建议", "附理由", "什么意思", "感觉",
    "觉得", "可以", "需要", "应该", "能够", "可能", "继续", "然后", "现在",
    "我们", "你们", "他们", "大家", "只是", "其实", "还有", "比如", "就是",
    "真的", "好像", "大概", "明白", "知道", "看到", "问题", "更新", "完成",
    "进行", "使用", "解决", "处理", "重新", "一种", "真的", "吗", "呢", "吧",
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
    # 子代理 SendMessage 回传通知（"Another Claude session sent a message: ..."）
    if head.startswith("another claude session sent a message"):
        return "", False
    # 子代理任务派发（"你在 <worktree> 中继续你刚完成的 Task ..."）
    if "继续你刚完成的 task" in content.lower() or "中继续你刚完成的" in content:
        return "", False
    return content, True


def is_sdk_replay(entry):
    """SDK 批量重放检测：entrypoint 为 sdk-* 的 user turn 是评测/脚本注入，非用户交互输入。
    （如 equipment-manager benchmark 用 sdk-cli/sdk-py 批量重放 synthetic 查询，会污染画像证据）"""
    return (entry.get("entrypoint") or "").startswith("sdk")


def is_sdk_replay_file(path):
    """SDK 批量重放文件检测：首行含 queue-operation 标记即整个 session 为非交互评测重放。
    在文件层排除，避免其占用扫描预算、把真实开发日志挤出窗口（实测近 90 天 520/1439 个文件是 SDK 重放）。"""
    try:
        with open(path, encoding="utf-8") as fh:
            first = fh.readline()
            return bool(first and '"queue-operation"' in first)
    except OSError:
        return False


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
    # 代码残留：traceback/路径/参数名（出现再多次也是粘贴残留，不是使用习惯）
    "src", "data", "args", "kwargs", "during", "handling", "start", "rename",
    "project", "versions", "update", "views", "main", "init", "setup", "test",
    "tests", "py", "pyc", "api", "http", "url", "get", "post", "self",
    "traceback", "shutil", "str", "files", "text", "index", "valueerror",
    "cannot", "stdout", "stderr", "encoding", "attributeerror",
    "open", "packages", "core",
}


def tokens(text):
    """轻量中英文 token：英文单词(≥3字符) + 连续中文串，去停用/噪声/中文弱词"""
    out = []
    for m in re.finditer(r"[a-z]+|[一-鿿]{2,}", text.lower()):
        t = m.group(0)
        if t.isascii():
            if len(t) < 3 or t in STOPWORDS or t in NOISE:
                continue
        elif t in CHINESE_WEAK:  # 中文弱词/口语填充同样过滤
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


def distill_rows(token_stats, evidence, state, now, decay_days, penalty, min_conf):
    """蒸馏输入：候选线索 → 置信度 + top3 证据（项目/session/时间/文本片段）。

    词频只是「线索」，是否真是画像信号由上层 LLM 蒸馏判定（语义层）；
    本函数只负责把每条线索绑上可追溯证据，供蒸馏逐条引用、防编造（参考 FastAPI 假证据教训）。
    """
    rows = []
    for kw, st in token_stats.items():
        corr = state.get(kw, {}).get("corrections", 0)
        c, days = confidence(len(st["sessions"]), st["last_ts"], corr, now,
                             decay_days, penalty)
        evs = []
        for src, info in sorted(evidence.get(kw, {}).items(),
                                key=lambda kv: kv[1]["ts"], reverse=True)[:3]:
            evs.append({
                "project": project_label(Path(src)),
                "session": Path(src).name,
                "ts": info["ts"],
                "snippet": info["snippet"],
            })
        rows.append({
            "keyword": kw,
            "sessions": len(st["sessions"]),
            "count": st["count"],
            "confidence": round(c, 3),
            "days_since": round(days),
            "corrections": corr,
            "status": "建议确认" if c >= min_conf else ("低证据" if c >= 0.3 else "衰减/丢弃"),
            "evidence": evs,
        })
    rows.sort(key=lambda r: -r["confidence"])
    return rows


def self_test():
    """最小自检：核心逻辑（过滤/分词/置信度公式）出错即断言失败。"""
    # clean_user_input：注入剔除
    assert clean_user_input("优化一下这段 FastAPI 接口的性能")[0] == "优化一下这段 FastAPI 接口的性能"
    assert clean_user_input("<local-command-caveat>xx</local-command-caveat> 你好")[0] == "你好"
    assert clean_user_input("<bash-stdout>out</bash-stdout> <bash-input>ls</bash-input>")[0] == ""
    assert clean_user_input("<task-notification>任务完成</task-notification> 你好")[0] == "你好"
    assert clean_user_input("## When to invoke this skill " + "x" * 200)[1] is False   # skill 正文
    assert clean_user_input("You are a reviewer, judge independently. " + "y" * 50)[1] is False  # 子代理注入
    assert clean_user_input("Another Claude session sent a message: 任务已完成 plan.md 已落盘")[1] is False  # SendMessage 回传
    assert clean_user_input("你在 /var/www/demo/.claude/worktrees/feature-x 中继续你刚完成的 Task 8（Web 推送端点）")[1] is False  # 子代理任务派发
    assert clean_user_input("This session is being continued from a previous conversation")[1] is False  # 压缩摘要
    # tokens：停用词/噪声过滤，保留领域词
    toks = tokens("fastapi python the skill null 优化 性能")
    assert "fastapi" in toks and "python" in toks and "skill" in toks
    assert "the" not in toks and "null" not in toks and "优化" in toks
    # tokens：中文弱词/口语填充过滤（这个/里面/附理由 不进候选）
    toks2 = tokens("这个 里面 什么意思 附理由 python")
    assert "python" in toks2
    assert "这个" not in toks2 and "里面" not in toks2
    assert "什么意思" not in toks2 and "附理由" not in toks2
    # tokens：代码残留（traceback 路径/参数名）不进候选
    toks3 = tokens("src data args kwargs handling src")
    assert toks3 == []
    # is_sdk_replay：SDK 批量重放（评测/脚本注入）应被排除，真实 cli 交互应保留
    assert is_sdk_replay({"type": "user", "entrypoint": "sdk-cli"})
    assert is_sdk_replay({"type": "user", "entrypoint": "sdk-py"})
    assert is_sdk_replay({"type": "user", "entrypoint": "sdk"})
    assert not is_sdk_replay({"type": "user", "entrypoint": "cli"})
    assert not is_sdk_replay({"type": "user", "entrypoint": ""})
    assert not is_sdk_replay({"type": "user"})
    # is_sdk_replay_file：首行 queue-operation 的评测重放文件应整文件排除（不占扫描预算）
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as tf:
        tf.write('{"type":"queue-operation","operation":"enqueue","content":"Review this change"}\n')
        tf.write('{"type":"user","entrypoint":"sdk-cli","message":{"content":"优化一下这段 FastAPI 接口的性能"}}\n')
        sdk_path = tf.name
    try:
        assert is_sdk_replay_file(sdk_path)
    finally:
        os.unlink(sdk_path)
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as tf:
        tf.write('{"type":"user","message":{"content":"帮我优化一下这段接口的性能"}}\n')
        real_path = tf.name
    try:
        assert not is_sdk_replay_file(real_path)
    finally:
        os.unlink(real_path)
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
    # distill：候选线索绑定 top3 证据（项目/session/时间/文本），供 LLM 蒸馏逐条引用
    dts = datetime.fromtimestamp(now - 86400).isoformat()
    d_stats = {"shyun": {"sessions": {"a.jsonl", "b.jsonl"}, "last_ts": dts, "count": 4}}
    d_ev = {"shyun": {"a.jsonl": {"ts": dts, "snippet": "帮我看看 shyun 的接口"},
                      "b.jsonl": {"ts": dts, "snippet": "shyun mysql 连不上"}}}
    rows = distill_rows(d_stats, d_ev, {}, now, 90, 0.5, 0.5)
    assert rows and rows[0]["keyword"] == "shyun"
    assert len(rows[0]["evidence"]) == 2
    for ev in rows[0]["evidence"]:
        assert sorted(ev.keys()) == ["project", "session", "snippet", "ts"]
        assert ev["session"].endswith(".jsonl")
    print("self-test: 全部通过（clean_user_input/tokens/confidence/distill）")
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
    ap.add_argument("--distill", action="store_true",
                    help="输出蒸馏输入 JSON：候选线索 + 置信度 + top3 证据（项目/session/时间/文本），供 LLM 提炼画像候选")
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
    # 先排除 SDK 批量重放文件（评测夹具），再按 mtime 从新到旧取总量兜底（最多前 200 个文件、总预算 60s）。
    # 若在预算窗口内排除，评测重放会挤占真实开发日志名额（实测近 90 天 SDK 文件占 36%）。
    files = sorted(
        [f for f in files
         if os.path.getmtime(f) >= since and not is_sdk_replay_file(f)],
        key=os.path.getmtime,
        reverse=True,
    )[:200]

    per_project = defaultdict(list)   # project -> [(ts, text, source)]
    verify_hits = []                  # [(label, ts, text, source)] for --verify
    token_stats = {}                  # keyword -> {sessions:set, last_ts, count}（--evaluate/--distill）
    distill_ev = {}                   # keyword -> {src: {ts, snippet}}（--distill，top3 证据）
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
            if args.evaluate or args.distill:
                for t in tokens(text):
                    st = token_stats.setdefault(t, {"sessions": set(), "last_ts": "", "count": 0})
                    st["count"] += 1
                    st["sessions"].add(src)
                    if ts and ts > st["last_ts"]:
                        st["last_ts"] = ts
                    if args.distill:
                        ev = distill_ev.setdefault(t, {})
                        if len(ev) < 3:
                            ev.setdefault(src, {"ts": ts, "snippet": text[:150]})

    # 证据追溯 verify：搜支持证据，不足 min-sessions 个不同 session 即 FAIL
    # （v1.1.1）再叠加纠正降权与置信度门槛：即使有 ≥min-sessions 个 session，
    # 被 --correct 纠正过（或置信度因衰减跌破 min-confidence）的关键词同样 FAIL，
    # 防「纠正后仍因旧 session 复活」。防编造 + 防纠正失效双闸。
    if args.verify:
        sessions = set()
        last_ts = ""
        print(f"== verify \"{args.verify}\" ==")
        for label, ts, text, src in verify_hits[:20]:
            sessions.add(src)
            if ts and ts > last_ts:
                last_ts = ts
            print(f"  [{label}] {ts[:10]} :: {text[:110]}  @ {Path(src).name}")
        n_sess = len(sessions)
        state = load_state(args.state)
        corr = state.get(args.verify.lower(), {}).get("corrections", 0)
        c, _days = confidence(n_sess, last_ts, corr, time.time(),
                              args.decay_days, args.correction_penalty)
        print(f"\n  命中 {len(verify_hits)} 条 | 来自 {n_sess} 个 session | 纠正 {corr} 次 | 置信度 {c:.3f}")
        print(f"  门槛: session ≥{args.min_sessions} 且 置信度 ≥{args.min_confidence}")
        verdict = "PASS" if n_sess >= args.min_sessions and c >= args.min_confidence \
            else "FAIL（证据不足/已纠正降权，候选丢弃）"
        print(f"  结论: {verdict}")
        sys.exit(0 if verdict == "PASS" else 1)

    # 蒸馏输入：证据绑定的候选线索 JSON。语义判定（是否真画像信号）由执行 skill 的 LLM 蒸馏做，
    # 本脚本只保证每条线索带可追溯证据（项目/session/时间/文本），供蒸馏逐条引用、防编造。
    if args.distill:
        state = load_state(args.state)
        rows = distill_rows(token_stats, distill_ev, state, time.time(),
                            args.decay_days, args.correction_penalty, args.min_confidence)
        out = {
            "meta": {"files": len(files), "turns": n_turns, "days": args.days},
            "rules": "对每条候选：① 先给 keyword 打维度标签（技术栈/业务工作流/个人习惯/工具习惯/噪声）；"
                     "② 技术栈与业务工作流 → 产出候选（一句话主张 + 判定依据 + ≥1 证据 session 引用）到主画像；"
                     "③ 个人习惯/工具习惯 → 产出到 prefs 备忘（equipment-manager 不读）；项目名/仓库名/噪声 → 不产出；"
                     "④ 证据不足/不确定 → 明确不产出（宁可漏判不编造）；⑤ 负面偏好不推断",
            "candidates": rows[:40],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

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
