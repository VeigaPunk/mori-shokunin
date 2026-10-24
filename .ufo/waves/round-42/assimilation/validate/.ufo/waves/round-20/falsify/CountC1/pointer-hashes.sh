#!/usr/bin/env bash
# CountC1 falsify scratch: do cited commit-like hashes in the r20 register resolve? (read-only git)
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
FLEET=/home/vgpnk/Projects/shokunin
S="$LANE/.ufo/waves/round-20/falsify/CountC1"
cd "$LANE" || exit 2
echo "multi-line reason/evidence entries: $(/usr/bin/jq '[.tokens[] | select(((.reason // "") | test("\n")) or ((.evidence // "") | test("\n")))] | length' corpus/evidence/drift-classification-r20.json)"
/usr/bin/jq -r '.tokens[] | .evidence' corpus/evidence/drift-classification-r20.json | /usr/bin/grep -oE '\b[0-9a-f]{7,40}\b' | LC_ALL=C /usr/bin/sort -u > "$S/pointer-hashes.txt"
echo "distinct hash-like pointers: $(/usr/bin/wc -l < "$S/pointer-hashes.txt")"
while read -r h; do
  if git -C "$LANE" cat-file -e "$h^{commit}" 2>/dev/null; then echo "lane-commit $h"
  elif git -C "$FLEET" cat-file -e "$h^{commit}" 2>/dev/null; then echo "fleet-commit $h"
  else echo "UNRESOLVED $h"; fi
done < "$S/pointer-hashes.txt"
