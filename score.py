#!/usr/bin/env python3
"""score.py — recompute Brier scores from scoreboard.csv. Anyone can run this.
Usage: python3 score.py [scoreboard.csv]

Convention: my_prob and market_prob are always P(event = YES).
outcome: '1' if event happened, '0' if not, 'open'/'' if unresolved.
"""
import csv, sys

path = sys.argv[1] if len(sys.argv) > 1 else "scoreboard.csv"
rows = list(csv.DictReader(open(path)))
resolved = [r for r in rows if r.get("outcome") in ("0", "1")]

if not resolved:
    print(f"{len(rows)} calls logged, 0 resolved. Brier requires resolutions.")
    sys.exit(0)

bm = bk = 0.0
hits = 0
for r in resolved:
    y = int(r["outcome"])
    p_me, p_mkt = float(r["my_prob"]), float(r["market_prob"])
    bm += (p_me - y) ** 2
    bk += (p_mkt - y) ** 2
    hits += int((p_me > p_mkt) == (y == 1))

n = len(resolved)
bm, bk = bm / n, bk / n
print(f"Resolved: {n}")
print(f"Brier (me):     {bm:.4f}")
print(f"Brier (market): {bk:.4f}")
print(f"Delta:          {bm - bk:+.4f}  (negative = beating the market)")
print(f"Directional hits vs market: {hits}/{n}")
print()
print("--- bio line (paste only once N is meaningful) ---")
print(f"Brier {bm:.3f} vs market {bk:.3f} over {n} resolved calls")
