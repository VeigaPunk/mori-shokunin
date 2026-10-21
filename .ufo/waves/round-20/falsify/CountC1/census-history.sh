#!/usr/bin/env bash
# CountC1 falsify scratch: read-only git history of tools/mori-census.sh (no index/ref writes).
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
cd "$LANE" || exit 2
echo "entering tip: $(git rev-parse --short 2061780117e6ca637725004897bd288d3ba7e988 2>&1)"
echo "HEAD: $(git rev-parse --short HEAD 2>&1)"
echo "census sha at entering tip: $(git show 2061780117e6ca637725004897bd288d3ba7e988:tools/mori-census.sh 2>&1 | sha256sum)"
echo "census sha working tree: $(sha256sum tools/mori-census.sh)"
echo "--- commits touching tools/mori-census.sh (newest first): sha256 | commit | date | subject"
for h in $(git log --format=%H -- tools/mori-census.sh); do
  s=$(git show "$h:tools/mori-census.sh" 2>/dev/null | sha256sum | cut -c1-64)
  m=$(git log -1 --format='%h %ad %s' --date=short "$h")
  echo "$s | $m"
done
echo "--- commits whose census blob hash is d7710981 (r10 header) or 87b8d680 (r20 register):"
for h in $(git log --format=%H -- tools/mori-census.sh); do
  s=$(git show "$h:tools/mori-census.sh" 2>/dev/null | sha256sum | cut -c1-64)
  case "$s" in d7710981*|87b8d680*) echo "$s $(git log -1 --format='%h %ad %s' --date=short "$h")";; esac
done
echo "--- r10 pin commit candidates (touching baseline-r10 file)"
git log --format='%h %ad %s' --date=iso -- corpus/evidence/baseline-r10-20261015T2231Z.json | head -5
echo "--- fleet-root pointer existence (evidence pointers from r20 register, fleet-relative)"
for p in .ufo/reports/round-24/kagi.md scripts/hyaku/inline.sh scripts/shokunin-watchdog.sh; do
  if [ -e "/home/vgpnk/Projects/shokunin/$p" ]; then echo "exists-fleet: $p"; else echo "MISSING-fleet: $p"; fi
done
