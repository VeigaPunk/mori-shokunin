#!/bin/bash
# mori round-79 AFTER receipts — run once per rev; writes the round's conformance evidence.
# Usage: gen-after.sh <rev> [out-file]
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
cd "$LANE" || exit 2
export HYAKU_SCRATCH=/fast/scratch/hyaku
REV="${1:?rev}"
OUT="${2:-.ufo/waves/round-79/evidence/after-r79.txt}"
runc() {
  printf '$ %s\n' "$1"
  out=$(eval "$1" 2>&1); rc=$?
  if [ -n "$out" ]; then printf '%s\n' "$out" | sed 's/^/  /'; fi
  printf 'rc=%s\n' "$rc"
  return 0
}
printf '# mori round-79 AFTER receipts (C1 tool, the three counters, the standing battery, the census)\n'
printf 'run-start=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf 'rev=%s\n' "$REV"
printf 'tree=%s (the lane working tree at %s; the census reads this working tree, not a revision)\n' "$LANE" "$REV"
printf '\n## 1. the C1 instrument at the landed bytes\n'
runc "git -C $LANE cat-file -e $REV:tools/mori-control-receipt.py"
runc "git -C $LANE show $REV:tools/mori-control-receipt.py | sha256sum"
runc "python3 -I tools/mori-control-receipt.py --selftest | tail -1"
runc "python3 -I tools/mori-control-receipt.py --dir $LANE/.ufo/waves/round-78/evidence | tail -3"
runc "python3 -I tools/mori-control-receipt.py --dir $LANE/.ufo/waves/round-79/evidence | tail -2"
printf '\n## 2. the three frozen counters at the landed rev\n'
for c in 1 2 3; do
  runc "python3 .ufo/waves/round-79/count-c$c.py $REV | tail -2"
done
printf '\n## 3. the standing battery (13 instruments, anchored rc counting)\n'
B=.ufo/waves/round-79/evidence/battery-r79.txt
: > "$B"
for t in register-check settlement-scan vote-bind pin-check drift-adjudicate drift-recheck \
         ua-variance uptime-win workstate-win events-context-win anchor-check rotation-schedule \
         counter-win; do
  printf '$ python3 tools/mori-%s.py --selftest | tail -1\n' "$t"
  out=$(python3 "tools/mori-$t.py" --selftest 2>&1 | tail -1); rc=$?
  printf '  %s\n' "$out"
  printf 'rc=%s\n' "$rc"
  printf '$ python3 tools/mori-%s.py --selftest\n' "$t" >> "$B"
  printf '  %s\n' "$out" >> "$B"
  printf 'rc=%s\n' "$rc" >> "$B"
done
runc "grep -c '^rc=0$' $B"
runc "grep -c '^rc=[0-9]*$' $B"
printf '\n## 4. the round-end census (conformance gate)\n'
runc "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori | tail -3"
printf '\n## 5. the no-harm tree facts (SCORECARD axes table and frozen registry bytes)\n'
runc "git -C $LANE show $REV:SCORECARD.md | sed -n '1,6p' | sha256sum"
runc "git -C $LANE show $REV:corpus/SOURCES.md | sed -n '1,373p' | sha256sum"
runc "git -C $LANE show $REV:SKILL.md | sed -n '1,1352p' | sha256sum"
