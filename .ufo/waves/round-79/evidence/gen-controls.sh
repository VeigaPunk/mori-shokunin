#!/bin/bash
set -u
cd /home/vgpnk/Projects/shokunin/mori-shokunin
export HYAKU_SCRATCH=/fast/scratch/hyaku
R="$1"
run1() { # $1 = command string
  printf '$ %s\n' "$1"
  out=$(eval "$1" 2>&1); rc=$?
  if [ -n "$out" ]; then printf '%s\n' "$out" | sed 's/^/  /'; fi
  printf 'rc=%s\n' "$rc"
  return 0
}
printf '# mori round-79 do-nothing controls (every claimed after-state absent at entering)\n'
printf 'run-start=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf 'entering=%s\n' "$R"
printf 'generator=%s (committed under .ufo/waves/round-79/evidence/gen-controls.sh)\n' "gen-controls.sh"
printf '\n## 1. the C1 instrument absent at entering\n'
run1 "git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e $R:tools/mori-control-receipt.py"
run1 "git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --all --oneline -- tools/mori-control-receipt.py | wc -l"
printf '\n## 2. the C2 target absent at entering (axes cells vs the fleet record)\n'
run1 "python3 .ufo/waves/round-79/count-c2.py $R"
printf '\n## 3. the C3 row, pin and entry absent at entering\n'
run1 "python3 .ufo/waves/round-79/count-c3.py $R"
run1 "git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e $R:corpus/evidence/sources-r79/rfc9111.txt"
run1 "git -C /home/vgpnk/Projects/shokunin/mori-shokunin show $R:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S594[[:space:]]*\|'"
printf '\n## 4. this round'"'"'s receipts absent at entering\n'
for p in corpus/knowledge/ua-serving-normative-r79.md corpus/lessons/round-79.md .ufo/waves/round-79/contract.md; do
  run1 "git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e $R:$p"
done
printf '\n## 5. the three counters'"'"' own selftests at the freeze commit\n'
for c in 1 2 3; do
  run1 "python3 .ufo/waves/round-79/count-c$c.py --selftest | tail -1"
done
printf '\n## 6. the fleet record the C2 counter reads (admitted mori rows only, through 78)\n'
run1 "python3 -c \"import json;d=json.load(open('/home/vgpnk/Projects/shokunin/MANIFEST.json'));m=[r for r in d['rounds'] if r.get('lane')=='mori' and r.get('admitted')];print('admitted_mori_rows',len(m));print('max_round',max(r['round'] for r in m))\""
