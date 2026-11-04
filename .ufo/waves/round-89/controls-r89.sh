#!/usr/bin/env bash
# mori round-89 controls: do-nothing (entering revision) and skip-work (labels without work).
# Read-only over the lane: every fixture is a `--shared` clone under $SCRATCH.
# Usage: bash .ufo/waves/round-89/controls-r89.sh <entering-rev>
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
REV=${1:?usage: controls-r89.sh <entering-rev>}
SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r89/controls
rm -rf -- "$SCRATCH"
mkdir -p "$SCRATCH"
trap 'rm -rf -- "$SCRATCH"' EXIT
cd "$LANE" || exit 2

echo "== controls-r89: lane=$LANE entering=$REV scratch=$SCRATCH"
echo
echo "== 1. do-nothing control: the entering revision, no work landed"
python3 -I .ufo/waves/round-89/count-c1.py "$REV" --scratch "$SCRATCH/enter-c1"
echo "rc=$?"
python3 -I .ufo/waves/round-89/count-c2.py "$REV" --scratch "$SCRATCH/enter-c2"
echo "rc=$?"
echo

patch() { python3 - "$@"; }

echo "== 2a. skip-work control C1: the gate gains the three arm labels but not the rule"
D="$SCRATCH/c1-skip"
git clone --shared -q "$LANE" "$D" && git -C "$D" checkout -q "$REV" || exit 2
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$(cd "$D" && pwd -P)" ] || exit 2
patch "$D/.ufo/waves/round-87/count-c2.py" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
anchor = "    ok = sum(1 for _, good_case, _ in cases if good_case)\n"
add = ("    cases.append((\"binding_path_identity\", True, \"skip\"))\n"
       "    cases.append((\"binding_comment_dropped\", True, \"skip\"))\n"
       "    cases.append((\"binding_selfprint_refused\", True, \"skip\"))\n")
assert s.count(anchor) == 1
open(p, "w", encoding="utf-8").write(s.replace(anchor, add + anchor))
PY
git -C "$D" -c user.name=t -c user.email=t@t commit -qam "round89 control c1-skip" || exit 2
python3 -I .ufo/waves/round-89/count-c1.py "$(git -C "$D" rev-parse HEAD)" --repo "$D" \
  --scratch "$SCRATCH/skip-c1"
echo "rc=$?"
echo

echo "== 2b. skip-work control C2: the r88 counters gain twelve arm labels, no assertion"
D="$SCRATCH/c2-skip"
git clone --shared -q "$LANE" "$D" && git -C "$D" checkout -q "$REV" || exit 2
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$(cd "$D" && pwd -P)" ] || exit 2
patch "$D/.ufo/waves/round-88/count-c1.py" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
anchor = "    ok = sum(1 for _, good, _ in cases if good)\n"
add = ("    cases.append((\"arms_last_tally\", True, \"skip\"))\n"
       "    cases.append((\"green_mixed_fail\", True, \"skip\"))\n"
       "    cases.append((\"own_ok_red\", True, \"skip\"))\n")
assert s.count(anchor) == 1 and s.count("EXPECTED_ARMS = 25") == 1
s = s.replace(anchor, add + anchor).replace("EXPECTED_ARMS = 25", "EXPECTED_ARMS = 28")
s = s.replace('ARMS_BY_FILE = {"count-c1.py": 24}', 'ARMS_BY_FILE = {"count-c1.py": 28}')
open(p, "w", encoding="utf-8").write(s)
PY
patch "$D/.ufo/waves/round-88/count-c2.py" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
anchor = "    ok = sum(1 for _, good_case, _ in cases if good_case)\n"
labels = ("target_full", "met_line_derived", "clean_wrong_split", "receipt_name_bound",
          "clone_top_bound", "own_ok_red", "verdict_last_wins", "absent_without_supersedes",
          "vacuous_body_fabricated")
add = "".join('    cases.append(("%s", True, "skip"))\n' % label for label in labels)
assert s.count(anchor) == 1
open(p, "w", encoding="utf-8").write(s.replace(anchor, add + anchor))
PY
git -C "$D" -c user.name=t -c user.email=t@t commit -qam "round89 control c2-skip" || exit 2
python3 -I .ufo/waves/round-89/count-c2.py "$(git -C "$D" rev-parse HEAD)" --repo "$D" \
  --scratch "$SCRATCH/skip-c2"
echo "rc=$?"
echo

echo "== 3. checksum-canary negative control (the counters' own selftest arms)"
python3 -I .ufo/waves/round-89/count-c2.py --selftest --scratch "$SCRATCH/st-c2" \
  | grep -E 'canary_unattributed|arm_boundary|C2_COUNTER_SELFTEST'
python3 -I .ufo/waves/round-89/count-c1.py --selftest --scratch "$SCRATCH/st-c1" \
  | grep -E 'C1_COUNTER_SELFTEST'
