#!/usr/bin/env python3
"""
0xbrier — reproducible scoring script.

Anyone can verify the scoreboard:
    python3 score.py

Conventions:
- `market_prob` and `my_prob` are probabilities assigned to the event (YES).
- `outcome` is 1 if the event happened, 0 if not, "open" if unresolved.
- Brier score = mean of (prob - outcome)^2 over resolved calls. Lower is better.
- The metric that matters: Brier(me) vs Brier(market) on the SAME resolved set.

Integrity rules (enforced by design, verifiable by anyone):
- Every call's canonical text lives in calls/callNNN.txt; its SHA-256 is in
  this CSV and was timestamped pre-resolution via OpenTimestamps (.ots files).
- Losers are never deleted. The universe is every call ever published.
"""

import csv
import hashlib
import math
import sys
from pathlib import Path

ROOT = Path(__file__).parent
CSV_PATH = ROOT / "scoreboard.csv"
CALLS_DIR = ROOT / "calls"


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def verify_hashes(rows):
    """Recompute SHA-256 of each canonical call file and compare to the CSV."""
    ok = True
    for r in rows:
        path = CALLS_DIR / f"call{r['call_id']}.txt"
        if not path.exists():
            print(f"  [WARN] missing canonical file: {path.name}")
            ok = False
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        status = "OK" if digest == r["sha256"] else "MISMATCH"
        if status == "MISMATCH":
            ok = False
        print(f"  call {r['call_id']}: sha256 {status}")
    return ok


def brier(probs_and_outcomes):
    return sum((p - o) ** 2 for p, o in probs_and_outcomes) / len(probs_and_outcomes)


def log_score(probs_and_outcomes):
    """Mean log score (natural log). Higher (closer to 0) is better."""
    eps = 1e-9
    total = 0.0
    for p, o in probs_and_outcomes:
        p = min(max(p, eps), 1 - eps)
        total += math.log(p) if o == 1 else math.log(1 - p)
    return total / len(probs_and_outcomes)


def main():
    rows = load_rows()
    print(f"Loaded {len(rows)} call(s) from {CSV_PATH.name}\n")

    print("Hash verification (canonical files vs CSV):")
    verify_hashes(rows)
    print()

    resolved = [r for r in rows if r["outcome"] in ("0", "1")]
    open_calls = [r for r in rows if r["outcome"] == "open"]

    print(f"Open calls: {len(open_calls)}")
    print(f"Resolved calls: {len(resolved)}\n")

    if not resolved:
        print("No resolved calls yet — Brier comparison starts at first resolution.")
        sys.exit(0)

    me = [(float(r["my_prob"]), int(r["outcome"])) for r in resolved]
    mkt = [(float(r["market_prob"]), int(r["outcome"])) for r in resolved]

    print(f"Brier (me):     {brier(me):.4f}")
    print(f"Brier (market): {brier(mkt):.4f}")
    print(f"Log score (me):     {log_score(me):.4f}")
    print(f"Log score (market): {log_score(mkt):.4f}")
    print("\nLower Brier wins. Same resolved set, no cherry-picking.")


if __name__ == "__main__":
    main()
