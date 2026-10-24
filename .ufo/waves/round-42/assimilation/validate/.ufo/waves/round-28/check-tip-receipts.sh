#!/usr/bin/env bash
# Round 28, QUALITY 84 check: a round's last lane batch carries tip receipts of every counter and of the retention
# scan, measured at the first parent of that batch, and the round's report cites every receipt.
#
# Reads committed bytes only (git objects at <rev>); the working tree is never read.
#
# Usage: bash .ufo/waves/round-28/check-tip-receipts.sh <rev> <round> [<report-path>...]
#   <rev>          the round's LAST lane batch (its final lane commit)
#   <round>        round number, e.g. 28
#   <report-path>  lane-relative files that must cite the receipts; default: LOG.md and the round lesson
#   --report-repo DIR --report-rev REV  also require the fleet round report .ufo/reports/round-<N>/mori.md at REV
#                         in that repository to cite the receipts
#
# The measured revision is the first parent of <rev>: a batch cannot hold a receipt of its own hash, so the
# receipt a batch carries measures the state its parent had. A receipt must (1) live under
# .ufo/waves/round-<round>/evidence/ in the tree at <rev>, (2) name the counter it ran or the retention scan it
# ran, (3) name the measured revision as its full 40-hex first parent, (4) carry an "exit:" line and at least one
# line of stdout, and (5) be cited by name in a report. A receipt for a withdrawn claim is still required: it
# records the withdrawal at the tip.
#
# Exit 0 when every counter and the retention scan have a receipt and every receipt is cited; 1 otherwise;
# 2 on a bad revision, a missing input or a usage error.
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
[ $# -ge 2 ] || { echo "usage: check-tip-receipts.sh <rev> <round> [<report-path>...]"; exit 2; }
REV=$1; ROUND=$2; shift 2
FLEET_REPO=""
FLEET_REV=""
REPORTS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --report-repo) FLEET_REPO=$2; shift 2 ;;
    --report-rev) FLEET_REV=$2; shift 2 ;;
    *) REPORTS+=("$1"); shift ;;
  esac
done
[ ${#REPORTS[@]} -gt 0 ] || REPORTS=("LOG.md" "corpus/lessons/round-$ROUND.md")
R=$(git -C "$LANE" rev-parse --verify -q "$REV^{commit}") || { echo "bad_rev"; exit 2; }
P=$(git -C "$LANE" rev-parse --verify -q "$R^1^{commit}") || { echo "no_parent"; exit 2; }
CONTRACT=".ufo/waves/round-$ROUND/contract.md"
EVID=".ufo/waves/round-$ROUND/evidence"
git -C "$LANE" cat-file -e "$R:$CONTRACT" 2>/dev/null || { echo "missing_contract"; exit 2; }
COUNTERS=$(git -C "$LANE" show "$R:$CONTRACT" | grep -oE 'count-[a-z0-9-]+\.sh' | sort -u)
[ -n "$COUNTERS" ] || { echo "no_counters"; exit 2; }
RECEIPTS=$(git -C "$LANE" ls-tree -r --name-only "$R" -- "$EVID/" | sort)
[ -n "$RECEIPTS" ] || { echo "no_receipts"; exit 1; }
lane_text=""
for f in "${REPORTS[@]}"; do
  lane_text="$lane_text$(git -C "$LANE" show "$R:$f" 2>/dev/null)
"
done
fleet_text=""
if [ -n "$FLEET_REPO" ]; then
  [ -n "$FLEET_REV" ] || { echo "missing_report_rev"; exit 2; }
  fleet_text=$(git -C "$FLEET_REPO" show "$FLEET_REV:.ufo/reports/round-$ROUND/mori.md" 2>/dev/null)
fi
rc=0
for c in $COUNTERS; do
  hit=""
  for f in $RECEIPTS; do
    body=$(git -C "$LANE" show "$R:$f" 2>/dev/null)
    case "$body" in *"$c"*) ;; *) continue ;; esac
    case "$body" in *"$P"*) ;; *) continue ;; esac
    printf '%s\n' "$body" | grep -qE '^exit: *[0-9]+' || continue
    [ "$(printf '%s\n' "$body" | grep -cE '.')" -ge 3 ] || continue
    hit=$f; break
  done
  if [ -n "$hit" ]; then
    base=$(basename "$hit")
    case "$lane_text" in *"$base"*) cl=yes ;; *) cl=no; rc=1 ;; esac
    cf=na
    if [ -n "$FLEET_REPO" ]; then
      case "$fleet_text" in *"$base"*) cf=yes ;; *) cf=no; rc=1 ;; esac
    fi
    echo "counter=$c receipt=$hit measured=$P cited_lane=$cl cited_fleet=$cf"
  else
    echo "counter=$c receipt=MISSING measured=$P"; rc=1
  fi
done
hit=""
for f in $RECEIPTS; do
  body=$(git -C "$LANE" show "$R:$f" 2>/dev/null)
  case "$body" in *mori-retention-gate.py*) ;; *) continue ;; esac
  case "$body" in *"$P"*) ;; *) continue ;; esac
  printf '%s\n' "$body" | grep -qE '^exit: *[0-9]+' || continue
  [ "$(printf '%s\n' "$body" | grep -cE '.')" -ge 3 ] || continue
  hit=$f; break
done
if [ -n "$hit" ]; then
  base=$(basename "$hit")
  case "$lane_text" in *"$base"*) cl=yes ;; *) cl=no; rc=1 ;; esac
  cf=na
  if [ -n "$FLEET_REPO" ]; then
    case "$fleet_text" in *"$base"*) cf=yes ;; *) cf=no; rc=1 ;; esac
  fi
  echo "retention receipt=$hit measured=$P cited_lane=$cl cited_fleet=$cf"
else
  echo "retention receipt=MISSING measured=$P"; rc=1
fi
[ $rc -eq 0 ] && echo "tip_receipts=met" || echo "tip_receipts=unmet"
exit $rc
