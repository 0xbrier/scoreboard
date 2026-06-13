# 0xbrier — public scoreboard

Calibrated probability calls on prediction markets. Every call is hashed and
timestamped **before** resolution. Wins and losses both stay on the board.

## The rules

1. Every call's exact text lives in [`calls/`](calls/), with its SHA-256 in
   [`scoreboard.csv`](scoreboard.csv).
2. Each call file is timestamped pre-resolution via
   [OpenTimestamps](https://opentimestamps.org) (Bitcoin-anchored proof of
   existence). The `.ots` proof files sit next to the call files.
3. Nothing is ever deleted or edited. A modified file breaks its own hash.
4. The only metric that matters: **Brier(me) vs Brier(market)** on the same
   resolved set.

## Verify it yourself

```bash
git clone <this repo>
cd <repo>
python3 score.py
```

The script recomputes every file hash against the CSV and recalculates the
Brier and log scores from raw data. No trust required.

To verify a timestamp: drag `calls/callNNN.txt` and its `.ots` file onto
https://opentimestamps.org (Verify tab).

## Scoreboard

See [`scoreboard.csv`](scoreboard.csv) — rendered as a table by GitHub.

| Column | Meaning |
|---|---|
| `market_prob` | Market-implied probability of the event at my fill |
| `my_prob` | My published calibrated probability |
| `fill_price_cents` | Actual fill price (real ask, net) |
| `outcome` | `1` event happened, `0` it didn't, `open` pending |
| `sha256` | Hash of the canonical call file, stamped pre-resolution |

## Status

Live since 2026-06-10. Calls: 1 open, 0 resolved.

*This is a public track record, not investment advice.*
