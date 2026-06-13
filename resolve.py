#!/usr/bin/env python3
"""resolve.py — resolve a call in one command.

Usage:
  python3 resolve.py 002 0        # outcome = 0 (event did NOT happen)
  python3 resolve.py 002 1        # outcome = 1 (event happened)

Does: set outcome in scoreboard.csv -> run score.py -> git commit + push.
Never edits a published call file. Never invents a number.
"""
import csv, subprocess, sys, pathlib

def run(cmd): subprocess.run(cmd, check=True)

def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ("0", "1"):
        sys.exit("usage: python3 resolve.py NNN OUTCOME   (OUTCOME = 0 or 1)")
    n, outcome = sys.argv[1].zfill(3), sys.argv[2]

    path = pathlib.Path("scoreboard.csv")
    rows = list(csv.DictReader(path.open()))
    fields = rows[0].keys()

    hit = False
    for r in rows:
        if r["call_id"] == n:
            if r["outcome"] not in ("", "open"):
                sys.exit(f"call {n} already resolved (outcome={r['outcome']}). Refusing to overwrite.")
            r["outcome"] = outcome
            hit = True
    if not hit:
        sys.exit(f"call {n} not found in scoreboard.csv")

    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    print(f"[csv] call {n} outcome set to {outcome}")

    run(["python3", "score.py"])
    run(["git", "add", "scoreboard.csv"])
    run(["git", "commit", "-m", f"call {n} resolved: outcome={outcome}"])
    run(["git", "push"])
    print("[git] pushed.")

if __name__ == "__main__":
    main()
