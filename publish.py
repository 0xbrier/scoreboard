#!/usr/bin/env python3
"""publish.py — 0xbrier publication pipeline (post-fill).

Canonical sequence: FILL -> freeze callNNN.txt (with real fill) -> this script.

What it does:
  1. sha256 of calls/callNNN.txt (exact bytes — never edit the file again)
  2. OTS stamp -> calls/callNNN.txt.ots   (pip install opentimestamps-client)
  3. injects the hash into tweets/callNNN_tweets.txt ({HASH} placeholder)
  4. git add + commit + push (proof goes public pre-resolution)
  5. prints the three tweets ready to paste into X

X posting is deliberately manual: the X API write tier costs money, automated
posting is an OPSEC surface, and pasting 3 tweets takes 60 seconds.

Usage:  python publish.py 003
Later:  ots upgrade calls/call003.txt.ots && git commit -am "ots upgrade 003" && git push
"""
import glob, hashlib, pathlib, shutil, subprocess, sys

def run(cmd): subprocess.run(cmd, check=True)

def find_ots() -> str:
    """Locate the ots binary, including macOS --user installs not on PATH."""
    found = shutil.which("ots")
    if found:
        return found
    candidates = glob.glob(str(pathlib.Path.home() / "Library/Python/*/bin/ots"))
    candidates += glob.glob(str(pathlib.Path.home() / ".local/bin/ots"))
    if candidates:
        return sorted(candidates)[-1]
    sys.exit("ots binary not found.\n"
             "Install it:   python3 -m pip install --user opentimestamps-client\n"
             "Then re-run:  python3 publish.py NNN")

def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python publish.py NNN   (e.g. 003)")
    n = sys.argv[1].zfill(3)
    call = pathlib.Path(f"calls/call{n}.txt")
    tweets = pathlib.Path(f"tweets/call{n}_tweets.txt")
    if not call.exists():
        sys.exit(f"{call} not found")

    digest = hashlib.sha256(call.read_bytes()).hexdigest()
    print(f"[hash] {digest}")

    ots = call.with_suffix(".txt.ots")
    if not ots.exists():
        run([find_ots(), "stamp", str(call)])
        print(f"[ots] stamped -> {ots} (Bitcoin anchor confirms in a few hours; "
              f"run 'ots upgrade {ots}' tomorrow and push the upgraded proof)")
    else:
        print(f"[ots] proof already exists, not re-stamping")

    if tweets.exists():
        tweets.write_text(tweets.read_text(encoding="utf-8")
                          .replace("{HASH}", digest), encoding="utf-8")
        print(f"[tweets] hash injected into {tweets}")

    run(["git", "add", "-A"])
    run(["git", "commit", "-m", f"call {n}: published pre-resolution"])
    run(["git", "push"])
    print("[git] pushed — proof is public")

    if tweets.exists():
        print("\n" + tweets.read_text(encoding="utf-8"))

if __name__ == "__main__":
    main()
