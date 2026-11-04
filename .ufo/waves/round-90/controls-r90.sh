#!/usr/bin/env bash
# mori round 90 — do-nothing / skip-work controls. Emits evidence/controls-r90.txt.
# Read-only over the lane; scratch under $HYAKU_SCRATCH/mori-r90/controls.
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
ENTERING=037c02ca43a5ff36e23e449d0d6bcf50a1f2cbec
SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r90/controls
mkdir -p "$SCRATCH"
cd "$LANE" || exit 2

echo "# mori round 90 controls"
echo "# lane: $LANE"
echo "# entering: $ENTERING"
echo "# date: $(date -Is)"
echo "# counter-sha256: .ufo/waves/round-90/count-c1.py $(sha256sum .ufo/waves/round-90/count-c1.py | cut -d' ' -f1)"
echo "# counter-sha256: .ufo/waves/round-90/count-c2.py $(sha256sum .ufo/waves/round-90/count-c2.py | cut -d' ' -f1)"
echo
echo "## 1. do-nothing C1 (no gate change): must be unmet"
python3 -I .ufo/waves/round-90/count-c1.py "$ENTERING" --scratch "$SCRATCH/c1" 2>&1 | tail -3
echo "rc=${PIPESTATUS[0]}"
echo
echo "## 2. blanket refusal (a gate that refuses every command): must read harm>0"
python3 -I - "$SCRATCH" <<'PY'
import importlib.util, os, sys
lane = "/home/vgpnk/Projects/shokunin/mori-shokunin"
spec = importlib.util.spec_from_file_location(
    "c1", os.path.join(lane, ".ufo/waves/round-90/count-c1.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class RefuseAll(object):
    @staticmethod
    def binding_problems(cmd, bindings, replayed, repo=None):
        return ["cmd-binding"]


class BindAll(object):
    @staticmethod
    def binding_problems(cmd, bindings, replayed, repo=None):
        return []


cases = [c for c in m.load_cases() if not c.get("reach")]
counts, _ = m.tally(cases, BindAll, RefuseAll, None, "BLANKET")
print("BLANKET " + " ".join("%s=%d" % (k, counts[k]) for k in
                            ("cases", "branch_cases", "branch_open", "harm",
                             "newopen", "open", "gained")))
print("BLANKET verdict=%s (harm>0 means refusal-all is not a gain)"
      % ("not-a-gain" if counts["harm"] > 0 else "REACHED-TARGET"))
sys.exit(0 if counts["harm"] > 0 else 1)
PY
echo "rc=$?"
echo
echo "## 3. do-nothing C2 (labels declared, arms absent): must be unmet"
python3 -I .ufo/waves/round-90/count-c2.py "$ENTERING" --scratch "$SCRATCH/c2" 2>&1 | tail -2
echo "rc=${PIPESTATUS[0]}"
echo
echo "## 4. counter selftests (detectors green before data)"
python3 -I .ufo/waves/round-90/count-c1.py --selftest 2>&1 | tail -1
echo "rc=${PIPESTATUS[0]}"
python3 -I .ufo/waves/round-90/count-c2.py --selftest --scratch "$SCRATCH/c2st" 2>&1 | tail -1
echo "rc=${PIPESTATUS[0]}"
rm -rf -- "$SCRATCH"
