#!/usr/bin/env bash
# Round 28 (lesson M2): content-hash misroot check. tools/mori-misroot-sweep.py finds a fleet-root file only when its
# path or head text names the lane and the round; upstream source bytes fetched by a seat name neither, so the seven
# round-27 fetches (base.c, oom_kill.c, MANPAGE.md, main.c, meminfo.c, sd-main.c, user@.service.in) read
# MORI_MISROOT_CLEAN. This check instead takes every untracked regular file at the fleet root and reports it when the
# first 16 hex digits of its sha256 occur in a committed lane wave report of round <N> (seats record fetched-byte
# hashes there). Read-only: it never moves or deletes anything.
# Usage: bash .ufo/waves/round-28/misroot-hash-check.sh <round> [<lane-rev>]
# Prints one `misroot <path> sha=<16 hex> cited-by=<report>` line per hit, then `misroot_hits=<k>`.
# Exit 0 when k=0, 1 when k>0, 2 on a usage error or an unreadable revision.
set -u
FLEET=/home/vgpnk/Projects/shokunin
LANE=$FLEET/mori-shokunin
[ $# -ge 1 ] && [ $# -le 2 ] || { echo "usage: misroot-hash-check.sh <round> [<lane-rev>]"; exit 2; }
N=$1
REV=$(git -C "$LANE" rev-parse --verify -q "${2:-master}^{commit}") || { echo "bad_rev"; exit 2; }
k=0
while IFS= read -r -d '' rec; do
  case "$rec" in '?? '*) p=${rec#?? } ;; *) continue ;; esac
  f="$FLEET/$p"
  [ -f "$f" ] && [ ! -L "$f" ] || continue
  h=$(sha256sum -- "$f" | cut -c1-16)
  hit=$(git -C "$LANE" grep -l -F "$h" "$REV" -- ".ufo/waves/round-$N/" 2>/dev/null | head -n 1)
  if [ -n "$hit" ]; then
    echo "misroot $p sha=$h cited-by=${hit#"$REV":}"
    k=$((k+1))
  fi
done < <(GIT_OPTIONAL_LOCKS=0 git -C "$FLEET" status --porcelain=v1 -z --untracked-files=all)
echo "misroot_hits=$k"
[ "$k" -eq 0 ] && exit 0
exit 1
