#!/usr/bin/env python3
"""Round 57 C2 counter: verify the sourced unclosed-pairing entry."""
import subprocess, sys
R=sys.argv[1]; repo="/home/vgpnk/Projects/shokunin/mori-shokunin"
def show(path):
 p=subprocess.run(["git","-C",repo,"show",f"{R}:{path}"],capture_output=True,text=True)
 return p.stdout if p.returncode == 0 else None
entry=show("corpus/knowledge/watchdog-unclosed-r57.md")
registry=show("corpus/SOURCES.md")
if entry is None or registry is None:
 print(f"C2=unmet claims=0 source=bad rev={R}"); raise SystemExit(1)
claims=[x for x in entry.splitlines() if x.startswith("| K")]
source_ok="S548" in entry and "| S548 |" in registry and "mined" in registry
quote_ok=all("`" in x and "`" in x for x in claims)
ok=len(claims)==8 and source_ok and quote_ok and "pairing count" in entry
print(f"C2={'met' if ok else 'unmet'} claims={len(claims)} source={'ok' if source_ok else 'bad'} quotes={'ok' if quote_ok else 'bad'} rev={R}")
raise SystemExit(0 if ok else 1)
