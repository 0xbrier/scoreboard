# CLAUDE.md — 0xbrier scoreboard repo

## What this repo is
Public, verifiable track record of calibrated calls on prediction markets.
Every call is hashed and OTS-stamped BEFORE resolution. Nothing is ever
deleted or edited after publication. Nostr is NOT used (dropped 2026-06).

## Conventions (do not deviate)
- Call files: `calls/callNNN.txt` (zero-padded), canonical "0xBRIER CALL #NNN"
  format — see call002/call003 for the template. Must contain the REAL fill
  price. A call file is FROZEN once `publish.py` has run on it.
- Tweet drafts: `tweets/callNNN_tweets.txt` with three sections (main /
  why reply / scoreboard reply) and a `{HASH}` placeholder in tweet 1.
- Scoreboard: `scoreboard.csv`. Probabilities are always P(event = YES),
  whatever side was traded. `outcome`: 1 / 0 / open.
- Scoring: `score.py` must stay dependency-free and reproducible by anyone.

## Canonical sequence for a new call NNN
1. Human fills the order on Polymarket (manual, always).
2. Write `calls/callNNN.txt` with the real fill — ask the human for it,
   NEVER invent a price or probability.
3. Write `tweets/callNNN_tweets.txt` (main + why + scoreboard).
4. Append the row to `scoreboard.csv`.
5. Run `python publish.py NNN` (hash + OTS + git push + prints tweets).
6. Human pastes the 3 tweets into X manually (no API posting — OPSEC + cost).
7. Next day: `ots upgrade calls/callNNN.txt.ots`, commit, push.

## On resolution of call NNN
1. Set `outcome` in scoreboard.csv (1/0), run `python score.py`.
2. Commit "call NNN resolved".
3. Draft the resolution tweet: result, updated Brier(me) vs Brier(market),
   link to repo. Losses are posted with the same prominence as wins.

## Hard rules
- Never fabricate numbers. Prices come from the live book via the human.
- Never modify a published call file or delete a row.
- Never reference the owner's real identity, location, or background.
