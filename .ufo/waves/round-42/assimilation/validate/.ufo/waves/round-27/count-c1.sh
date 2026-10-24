#!/usr/bin/env bash
# Round 27, claim C1 counter. Reads committed bytes only (git objects at <rev>), never the working tree.
# Usage: bash .ufo/waves/round-27/count-c1.sh <rev>
# Prints entry=, new_rows_cited=, skill_rows=, then C1=met|unmet.
# Exit 0 when C1=met, 1 when C1=unmet, 2 on a bad revision or a usage error.
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
ENTRY=corpus/knowledge/oom-victim-selection-r27.md
MIN_ROW=127          # SOURCES ids S127 and above did not exist at the entering tip fc09f96c
NEED_ROWS=3
NEED_SKILL=3
[ $# -eq 1 ] || { echo "usage: count-c1.sh <rev>"; exit 2; }
R=$(git -C "$LANE" rev-parse --verify -q "$1^{commit}") || { echo "bad_rev"; exit 2; }
if ! git -C "$LANE" cat-file -e "$R:$ENTRY" 2>/dev/null; then
  echo "entry=absent new_rows_cited=0 skill_rows=0"; echo "C1=unmet"; exit 1
fi
src=$(git -C "$LANE" show "$R:$ENTRY" | grep -m1 '^source:') || src=""
sources=$(git -C "$LANE" show "$R:corpus/SOURCES.md" 2>/dev/null) || { echo "bad_rev"; exit 2; }
skill=$(git -C "$LANE" show "$R:SKILL.md" 2>/dev/null) || { echo "bad_rev"; exit 2; }
n=0
for id in $(printf '%s\n' "$src" | grep -oE '\bS[0-9]{3}\b' | sort -u); do
  num=$((10#${id#S}))
  [ "$num" -ge "$MIN_ROW" ] || continue
  # the row must exist, be status `mined`, and name the entry in used-by
  row=$(printf '%s\n' "$sources" | grep -E "^\| $id \|") || continue
  printf '%s\n' "$row" | grep -qE '\| mined \|' || continue
  printf '%s\n' "$row" | grep -qF "$ENTRY" || continue
  n=$((n+1))
done
# SKILL.md rows inside the section headed "Round27" (up to the next "## " heading) that cite the entry
m=$(printf '%s\n' "$skill" | awk '/^## /{inside=($0 ~ /Round27/)} inside && /^\|/ && /oom-victim-selection-r27\.md/' | wc -l)
echo "entry=present new_rows_cited=$n skill_rows=$m"
if [ "$n" -ge "$NEED_ROWS" ] && [ "$m" -ge "$NEED_SKILL" ]; then echo "C1=met"; exit 0; fi
echo "C1=unmet"; exit 1
