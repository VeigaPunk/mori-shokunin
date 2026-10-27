#!/usr/bin/env python3
"""Round 57 C1 counter: verify the two round-56 capabilities are recorded."""
import subprocess, sys

R = sys.argv[1]
repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
p = subprocess.run(["git", "-C", repo, "show", f"{R}:SCORECARD.md"], capture_output=True, text=True)
if p.returncode:
    print("C1=unmet rows=0 evidence=bad"); raise SystemExit(1)
s = p.stdout.split("## Capabilities", 1)[1].split("## Saturation", 1)[0]
rows = [line for line in s.splitlines() if line.startswith("|") and ("driver-liveness" in line or "vote-binding" in line)]
ok = len(rows) == 2 and all(".ufo/waves/round-56/" in x and "| 56 |" in x for x in rows)
print(f"C1={'met' if ok else 'unmet'} rows={len(rows)} evidence={'ok' if ok else 'bad'} rev={R}")
raise SystemExit(0 if ok else 1)
