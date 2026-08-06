#!/usr/bin/env python3
"""分析 trigger-baseline.jsonl：去重 → 统计 TP/TN/FP/FN → 列出 FN/FP 与缺失样本。"""
import json
from collections import Counter
from pathlib import Path

BASE = Path("/home/anonymous/equipment-manager-workspace")
JSONL = BASE / "trigger-baseline.jsonl"
EVAL = BASE / "trigger-eval-set.json"

# 1. 读取并按 idx 去重（保留最后一条，追加式并发写入会产生重复行）
rows = [json.loads(l) for l in JSONL.read_text().splitlines() if l.strip()]
dedup = {r["idx"]: r for r in rows}

# 2. 统计
c = Counter(r["verdict"] for r in dedup.values())
tp, tn, fp, fn = c["TP"], c["TN"], c["FP"], c["FN"]
recall = tp / (tp + fn) if tp + fn else float("nan")
precision = tp / (tp + fp) if tp + fp else float("nan")

# 3. 与 eval-set 对比，找出本次没跑到的样本
eval_rows = {i: it for i, it in enumerate(json.loads(EVAL.read_text()))}
missing = sorted(set(eval_rows) - set(dedup))

print("===== TRIGGER BASELINE 分析 =====")
print(f"原始记录 {len(rows)} 行，去重后 {len(dedup)} 条")
print(f"TP={tp} TN={tn} FP={fp} FN={fn} | recall={recall:.0%} precision={precision:.0%}")
print(f"eval-set 共 {len(eval_rows)} 条，结果缺失 {len(missing)} 条: {missing}")
print("\nFN（应触发未触发）:")
for r in sorted(dedup.values(), key=lambda r: r["idx"]):
    if r["verdict"] == "FN":
        print(f"  [{r['idx']}] {r['query']}")
print("\nFP（误触发）:")
for r in sorted(dedup.values(), key=lambda r: r["idx"]):
    if r["verdict"] == "FP":
        print(f"  [{r['idx']}] {r['query']}")
