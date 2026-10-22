#!/usr/bin/env bash
# Round 28, claim C1 counter (freshness): first-published SOURCES cells restored and the eight carried row defects
# superseded by rows re-opened this round. Reads committed bytes only (git objects at <rev>), never the working tree.
# Usage: bash .ufo/waves/round-28/count-c1.sh <rev>
# Prints row_identity=<summary line of the round-27 QUALITY 81 check run at <rev>>, superseding=<k>/8 and the
# superseded ids found, then C1=met|unmet.
# Exit 0 when C1=met, 1 when C1=unmet, 2 on a bad revision, a missing input or a usage error.
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
CHECK=.ufo/waves/round-27/check-row-identity.py
SRC=corpus/SOURCES.md
# The eight carried defects routed by the round-27 closure (round-27-verifier-spotcheck.md routed defects 3 and 4).
OWED="S096 S097 S101 S127 S128 S129 S131 S140"
MAX_OLD=144          # superseding rows must be new: ids above S144 (the highest id at the entering tip 6ebd518f)
[ $# -eq 1 ] || { echo "usage: count-c1.sh <rev>"; exit 2; }
R=$(git -C "$LANE" rev-parse --verify -q "$1^{commit}") || { echo "bad_rev"; exit 2; }
T=$(mktemp -d) || exit 2
trap 'rm -rf "$T"' EXIT
# the check script is taken from the round-27 landed tip df886be1 (frozen), never from the working tree
git -C "$LANE" show "df886be1cc75f1052002698bdb4a3d18a2eaf6c6:$CHECK" > "$T/check.py" || { echo "check_absent"; exit 2; }
git -C "$LANE" show "$R:$SRC" > "$T/sources.md" 2>/dev/null || { echo "sources_absent"; exit 2; }
ri=$(python3 -I -B "$T/check.py" "$R" 2>/dev/null | grep -E '^rows=[0-9]+ changed=' | tail -n 1)
[ -n "$ri" ] || { echo "row_identity=error"; echo "C1=unmet"; exit 2; }
read -r k ids < <(python3 -I -B - "$T/sources.md" "$OWED" "$MAX_OLD" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
owed = sys.argv[2].split()
max_old = int(sys.argv[3])
sep = re.compile(r"(?<!\\)\|")
found = set()
for line in text.split("\n"):
    if not re.match(r" {0,3}\|[ \t]*S[0-9]{3,}[ \t]*\|", line):
        continue
    cells = [c.strip() for c in sep.split(line.strip())]
    if len(cells) != 13:
        continue
    rid, teaches, status = cells[1], cells[7], cells[8]
    if int(rid[1:]) <= max_old:
        continue
    m = re.match(r"supersedes (S[0-9]{3}) — ", teaches)
    # a superseding row counts only when it was opened and verified, never as a candidate or rejection
    if m and m.group(1) in owed and status in ("mined", "verified"):
        found.add(m.group(1))
print(len(found), ",".join(sorted(found)) or "none")
PY
)
echo "row_identity=$ri"
echo "superseding=$k/8 ids=$ids"
case "$ri" in
  *" changed=0 removed=0 bad=0") ok_ri=1 ;;
  *) ok_ri=0 ;;
esac
if [ "$ok_ri" -eq 1 ] && [ "$k" -eq 8 ]; then echo "C1=met"; exit 0; fi
echo "C1=unmet"; exit 1
