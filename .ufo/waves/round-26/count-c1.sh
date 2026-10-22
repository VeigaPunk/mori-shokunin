#!/usr/bin/env bash
# Round-26 C1 counter (amendment A1). Usage: bash count-c1.sh <rev>. Reads committed bytes only.
L=/home/vgpnk/Projects/shokunin/mori-shokunin; R=${1:?rev}
git -C "$L" rev-parse -q --verify "$R^{commit}" >/dev/null || { echo bad_rev; exit 2; }
n=0; k=0
while IFS='|' read -r f p; do
  k=$((k+1))
  b=$(git -C "$L" show "$R:$f" 2>/dev/null) || { echo "missing=$f"; exit 2; }
  printf '%s' "$b" | tr -s ' \n\t' '   ' | tr -d '*' | grep -q -F -- "$p" && n=$((n+1))
done < <(git -C "$L" show 28b0494004fe1f064544224eca56dd42605db384:.ufo/waves/round-26/c1-phrases.txt)
[ "$k" -eq 4 ] || { echo "phrases_read=$k"; exit 2; }
echo "stale_present=$n"
e=$(git -C "$L" show "$R:corpus/knowledge/userspace-oom-killers-r26.md" 2>/dev/null) && echo r26_entry=present || echo r26_entry=absent
printf '%s\n' "$e" | grep -m1 '^source:' | grep -oE 'S[0-9]{3}' | sort -u | awk '{sub("S","");if($1+0>113)c++} END{print "r26_new_source_ids=" c+0}'
echo "r12_names_r26=$(git -C "$L" show "$R:corpus/knowledge/userspace-oom-killers-r12.md" | grep -c -F 'userspace-oom-killers-r26.md')"
