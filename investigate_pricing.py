#!/usr/bin/env python3
import csv
import json
from decimal import Decimal, getcontext

getcontext().prec = 28

CSV_PATH = "pricing_diff.csv"

def d(x):
    return Decimal(x)

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

records = []
for row in rows:
    v1 = d(row["v1_total"])
    v2 = d(row["v2_total"])
    records.append({
        **row,
        "v1": v1,
        "v2": v2,
        "diff": v2 - v1,
    })

# Q1: exact inequality count
q1_naive_nonzero_count = sum(r["v1"] != r["v2"] for r in records)

# Assignment says one- or two-cent differences are expected noise.
# Exclude books because its changed rate is explicitly intentional.
affected = [
    r for r in records
    if r["category"] != "books" and abs(r["diff"]) > Decimal("0.02")
]

q2_affected_count = len(affected)
categories = sorted({r["category"] for r in affected})
q2_affected_category = categories[0] if len(categories) == 1 else ",".join(categories)

q3_total_overcharge = sum((r["diff"] for r in affected), Decimal("0.00"))

# Baseline: non-books and not in the identified bug pattern.
baseline = [
    r for r in records
    if r["category"] != "books"
    and not (r["category"] == "fragile" and r["express"] == "True")
]
q4_baseline_mean_abs_diff = (
    sum((abs(r["v1"] - r["v2"]) for r in baseline), Decimal("0"))
    / Decimal(len(baseline))
)

answers = {
    "q1_naive_nonzero_count": q1_naive_nonzero_count,
    "q2_affected_count": q2_affected_count,
    "q2_affected_category": q2_affected_category,
    "q3_total_overcharge": float(q3_total_overcharge),
    "q4_baseline_mean_abs_diff": float(q4_baseline_mean_abs_diff),
}

print(json.dumps(answers, indent=2))

# Optional diagnostics used in the write-up.
from collections import Counter
coupon_counts = Counter(r["coupon"] or "empty" for r in affected)
print("coupon breakdown:", dict(coupon_counts))
print("avg affected diff:", q3_total_overcharge / Decimal(q2_affected_count))
