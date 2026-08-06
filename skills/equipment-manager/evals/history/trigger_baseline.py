#!/usr/bin/env python3
"""Trigger baseline test (v2): run trigger-eval-set queries via claude -p,
detect ONLY Skill tool calls targeting the real my-skills:equipment-manager."""
import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

EVAL_SET = "/home/anonymous/equipment-manager-workspace/trigger-eval-set.json"
OUT = "/home/anonymous/equipment-manager-workspace/trigger-baseline.jsonl"
TIMEOUT = 50
WORKERS = 4
SKILL_MARK = "equipment-manager"

def detect_trigger(jsonl_path):
    """Return True iff a Skill tool call with 'equipment-manager' in its
    input was made. Uses streaming accumulation so it works before timeout."""
    try:
        lines = open(jsonl_path).read().splitlines()
    except OSError:
        return False
    pending = False
    accum = ""
    for line in lines:
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "stream_event":
            se = e.get("event", {})
            st = se.get("type", "")
            if st == "content_block_start":
                cb = se.get("content_block", {})
                if cb.get("type") == "tool_use" and cb.get("name") == "Skill":
                    pending = True
                    accum = ""
                else:
                    pending = False
            elif st == "content_block_delta" and pending:
                d = se.get("delta", {})
                if d.get("type") == "input_json_delta":
                    accum += d.get("partial_json", "")
                    if SKILL_MARK in accum:
                        return True
            elif st == "content_block_stop":
                if pending and SKILL_MARK in accum:
                    return True
                pending = False
        elif e.get("type") == "assistant":
            for c in e.get("message", {}).get("content", []):
                if c.get("type") == "tool_use" and c.get("name") == "Skill":
                    if SKILL_MARK in str(c.get("input", {}).get("skill", "")):
                        return True
    return False

def run_one(item, idx):
    query = item["query"]
    expect = item["should_trigger"]
    tmp = f"/tmp/trigger_v2_{idx}.jsonl"
    try:
        subprocess.run(
            ["claude", "-p", query, "--output-format", "stream-json",
             "--verbose", "--include-partial-messages"],
            stdout=open(tmp, "w"), stderr=subprocess.DEVNULL,
            timeout=TIMEOUT,
            env={k: v for k, v in os.environ.items() if k != "CLAUDECODE"},
        )
    except subprocess.TimeoutExpired:
        pass
    triggered = detect_trigger(tmp)
    verdict = "TP" if (expect and triggered) else "FN" if expect else ("FP" if triggered else "TN")
    rec = {"idx": idx, "query": query, "should_trigger": expect, "triggered": triggered, "verdict": verdict}
    with open(OUT, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[{verdict}] expect={int(expect)} got={int(triggered)} | {query[:38]}", flush=True)
    return rec

def main():
    items = json.load(open(EVAL_SET))
    open(OUT, "w").close()
    t0 = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(run_one, it, i): i for i, it in enumerate(items)}
        for fut in as_completed(futs):
            results.append(fut.result())
    results.sort(key=lambda r: r["idx"])
    tp = sum(1 for r in results if r["verdict"] == "TP")
    tn = sum(1 for r in results if r["verdict"] == "TN")
    fp = sum(1 for r in results if r["verdict"] == "FP")
    fn = sum(1 for r in results if r["verdict"] == "FN")
    recall = tp / (tp + fn) if (tp + fn) else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    print("\n===== TRIGGER BASELINE v2 =====")
    print(f"TP={tp} TN={tn} FP={fp} FN={fn} | recall={recall:.0%} precision={precision:.0%} accuracy={(tp+tn)/len(results):.0%}")
    print(f"elapsed={time.time()-t0:.0f}s")
    print("\n未触发的正例（优化重点 FN）:")
    for r in results:
        if r["verdict"] == "FN":
            print(f"  - {r['query']}")
    print("\n误触发的负例（防误伤 FP）:")
    for r in results:
        if r["verdict"] == "FP":
            print(f"  - {r['query']}")

if __name__ == "__main__":
    main()
