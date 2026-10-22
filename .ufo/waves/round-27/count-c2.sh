#!/usr/bin/env bash
# Round 27, claim C2 counter. Reads committed bytes only: the tool and both case files are extracted from <rev>
# into a temporary directory and the self-test runs there, never on the working tree.
# Usage: bash .ufo/waves/round-27/count-c2.sh <rev>
# Prints a2_cases=, a2_rules_covered=, freeze_commit=, cases_changed_since_freeze=, a2_selftest=, frozen32_selftest=,
# then C2=met|unmet.
# Exit 0 when C2=met, 1 when C2=unmet (including any self-test that does not print PASS N/N), 2 on a bad revision or
# a usage error. Unlike round 26's count-c2.sh, a failing self-test never exits 0.
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
TOOL=tools/mori-oom-killers.py
FROZEN=tools/fixtures/mori-oom-killers/cases.json
A2=tools/fixtures/mori-oom-killers/cases-a2.json
# The ten round-26 amendment-A2 rules this claim must pin (contract .ufo/waves/round-27/contract.md, C2 rule list).
RULES="A2-01 A2-02 A2-03 A2-04 A2-05 A2-06 A2-07 A2-08 A2-09 A2-10"
MIN_CASES=20
[ $# -eq 1 ] || { echo "usage: count-c2.sh <rev>"; exit 2; }
R=$(git -C "$LANE" rev-parse --verify -q "$1^{commit}") || { echo "bad_rev"; exit 2; }
git -C "$LANE" cat-file -e "$R:$TOOL" 2>/dev/null || { echo "tool_absent"; exit 2; }
if ! git -C "$LANE" cat-file -e "$R:$A2" 2>/dev/null; then
  echo "a2_cases=0 a2_rules_covered=0/10"; echo "C2=unmet"; exit 1
fi
T=$(mktemp -d) || exit 2
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/tools/fixtures/mori-oom-killers"
for f in "$TOOL" "$FROZEN" "$A2"; do git -C "$LANE" show "$R:$f" > "$T/$f" || { echo "bad_rev"; exit 2; }; done
read -r ncases covered < <(python3 -I -B - "$T/$A2" "$RULES" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    cases = d["cases"]
    rules = set(sys.argv[2].split())
    # a rule counts as covered only by a case that pins both a verdict and an exit code
    seen = {c.get("rule") for c in cases if isinstance(c, dict) and isinstance(c.get("expect"), dict)
            and "verdict" in c["expect"] and "exit" in c["expect"]} & rules
    print(len(cases), len(seen))
except Exception:
    print(0, 0)
PY
)
# freeze commit: the oldest commit reachable from <rev> that added the A2 case file
freeze=$(git -C "$LANE" log --diff-filter=A --format=%H "$R" -- "$A2" | tail -n 1)
changed=1
[ -n "$freeze" ] && [ "$(git -C "$LANE" rev-parse "$freeze:$A2")" = "$(git -C "$LANE" rev-parse "$R:$A2")" ] && changed=0
a2=$(cd "$T" && python3 -I -B "$TOOL" --selftest --cases "$A2" 2>/dev/null | grep -E '^MORI_OOM_KILLERS_SELFTEST: ' | tail -n 1)
f32=$(cd "$T" && python3 -I -B "$TOOL" --selftest --cases "$FROZEN" 2>/dev/null | grep -E '^MORI_OOM_KILLERS_SELFTEST: ' | tail -n 1)
echo "a2_cases=$ncases a2_rules_covered=$covered/10 freeze_commit=${freeze:-none} cases_changed_since_freeze=$changed"
echo "a2_selftest=${a2#MORI_OOM_KILLERS_SELFTEST: } frozen32_selftest=${f32#MORI_OOM_KILLERS_SELFTEST: }"
if [ "$covered" -eq 10 ] && [ "$ncases" -ge "$MIN_CASES" ] && [ "$changed" -eq 0 ] \
   && [ "$a2" = "MORI_OOM_KILLERS_SELFTEST: PASS $ncases/$ncases" ] \
   && [ "$f32" = "MORI_OOM_KILLERS_SELFTEST: PASS 32/32" ]; then
  echo "C2=met"; exit 0
fi
echo "C2=unmet"; exit 1
