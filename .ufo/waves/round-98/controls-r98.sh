#!/usr/bin/env bash
# mori round 98 — pre-freeze control battery for count-c1.py and count-c2.py.
# Usage: bash controls-r98.sh <entering-rev>   (writes receipt lines to stdout)
# Scratch: $HYAKU_SCRATCH/mori-r98/L1controls (deleted on exit). Read-only on the lane:
# trees come from `git archive`; C2 fixtures commit only inside a `git clone --shared` scratch clone.
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
W=$LANE/.ufo/waves/round-98
ENT=${1:?entering rev}
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r98/L1controls
rm -rf -- "$S"; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT
export TMPDIR=$S
unexp=0
echo "CONTROLS_HEADER entering=$(git -C $LANE rev-parse $ENT) count-c1.py=$(sha256sum $W/count-c1.py | cut -c1-64) count-c2.py=$(sha256sum $W/count-c2.py | cut -c1-64) candidate-tool=$(sha256sum $W/candidate/tools/mori-userns-runway.py | cut -c1-64) date=$(date -u +%FT%TZ)"

mk() { # mk NAME -> fresh entering tree at $S/NAME
  mkdir -p "$S/$1" && git -C $LANE archive "$ENT" | tar -x -C "$S/$1"
}
full() { # full NAME -> entering tree + every candidate surface (stub knowledge + stub SOURCES row)
  mk "$1"; local D=$S/$1
  cp $W/candidate/tools/mori-userns-runway.py "$D/tools/"
  cat $W/candidate/SKILL-append.md >> "$D/SKILL.md"
  cat $W/candidate/PROVINCE-append.md >> "$D/PROVINCE.md"
  printf 'source: S999 — control stub\nverified-at: 2026-11-05\nrecheck: 90d\n' > "$D/corpus/knowledge/userns-runway-r98.md"
  printf '| S999 | control stub — https://example.invalid/ | docs | A | stub | stub | stub | mined | 2026-11-05 | 90d | corpus/knowledge/userns-runway-r98.md |\n' >> "$D/corpus/SOURCES.md"
}
mut() { # mut NAME PYEXPR -> apply a python str.replace on the tool in tree NAME; fail loudly if no-op
  python3 - "$S/$1/tools/mori-userns-runway.py" "$2" "$3" <<'E'
import sys
p, a, b = sys.argv[1:]
t = open(p).read()
assert a in t, "mutation anchor absent"
open(p, "w").write(t.replace(a, b, 1))
E
}
c1() { # c1 LABEL NAME EXPECT(met|unmet)
  local out rc; out=$(python3 $W/count-c1.py --root "$S/$2" --work "$S" 2>&1); rc=$?
  local got=unmet; [[ $out == C1=met* ]] && got=met
  local v=AS_EXPECTED; [[ $got == "$3" ]] || { v=UNEXPECTED; unexp=$((unexp+1)); }
  echo "CONTROL c1 $1 expect=$3 rc=$rc $v :: ${out% root=*}"
}

mk ent0; c1 K0-do-nothing-entering ent0 unmet
full P1; c1 P1-positive-candidate P1 met
full K1; cat > "$S/K1/tools/mori-userns-runway.py" <<'E'
import sys
if "--selftest" in sys.argv: print("MORI_USERNS_RUNWAY_SELFTEST: PASS (11 cases)"); sys.exit(0)
if "--journal" in sys.argv or "--journal-live" in sys.argv: print("SYSCTL_WRITES n=6 keys=1 userns_zero=2"); sys.exit(1)
print("USERNS_RUNWAY limit=122865 used_lb=3 pids=15 unreadable=3 runway=122862 low=32 state=ok"); sys.exit(0)
E
c1 K1-constant-printer K1 unmet
full K2; mut K2 "        if ino != init_ino:
            seen.add(ino)" "        if ino != init_ino:
            seen.add(p)"; c1 K2-counts-pids-not-namespaces K2 unmet
full K3; mut K3 '        raise Setup("limit unreadable: %s" % e.__class__.__name__)' '        raw = "0"' ; c1 K3-fail-open-missing-limit K3 unmet
full K4; mut K4 '            elif not a.startswith("-") and "=" in a:' '            elif not a.startswith("-") or a == "-a":'; c1 K4-reads-as-writes K4 unmet
full K5; mut K5 'TS_PID_RE = re.compile(r"^(\S+)\s+\S+\s+sudo\[(\d+)\]:")' 'TS_PID_RE = re.compile(r"^(\S+)\s+\S+\s+.*?sudo\[(\d+)\]")'; c1 K5-accepts-decoy-lines K5 unmet
full K6; git -C $LANE show "$ENT:SKILL.md" > "$S/K6/SKILL.md"; c1 K6-no-registry-row K6 unmet
full K7; rm "$S/K7/corpus/knowledge/userns-runway-r98.md"; c1 K7-no-knowledge-entry K7 unmet
full K8; sed -i 's/| mined | 2026-11-05 | 90d | corpus\/knowledge\/userns-runway-r98.md |/| queued | 2026-11-05 | 90d | — |/' "$S/K8/corpus/SOURCES.md"; c1 K8-row-not-mined K8 unmet
full K9; git -C $LANE show "$ENT:PROVINCE.md" > "$S/K9/PROVINCE.md"; c1 K9-no-province-line K9 unmet
full K10; mut K10 '    if runway == 0:
        state = "exhausted"' '    if runway == 0 and limit > 0:
        state = "exhausted"
    elif runway == 0:
        state = "ok"'; c1 K10-limit-zero-reads-ok K10 unmet
full K11; mut K11 '            out.append({"ts": m.group(1),' '            print(line); out.append({"ts": m.group(1),'; c1 K11-echoes-raw-journal-line K11 unmet

# ---- C2 controls: scratch clone, fixture commits only there
D=$S/c2clone
git clone -q --shared $LANE "$D"
[[ $(git -C "$D" rev-parse --show-toplevel) == "$D" ]] || { echo "CONTROL c2 SETUP clone toplevel mismatch"; exit 3; }
git -C "$D" checkout -q --detach "$ENT"
gc() { git -C "$D" -c user.name=mori-r98-control -c user.email=control@invalid commit -q -am "$1" && git -C "$D" rev-parse HEAD; }
fix_cells() { python3 - "$D/SCORECARD.md" "$1" <<'E'
import sys
p, which = sys.argv[1:]
L = open(p).read().split("\n")
def lead(i, old, new):
    assert ("| " + old) in L[i], (i, old)
    L[i] = L[i].replace("| " + old, "| " + new + "; " + old, 1)
if which in ("both", "op"):
    lead(10, "round 93 (improved, score held)", "round 97 (improved, score held)")
if which in ("both", "fr"):
    lead(12, "round 82 (improved, score held)", "round 97 (improved, score held)")
if which == "harmed":
    lead(10, "round 93 (improved, score held)", "round 97 (harmed, score held)")
    lead(12, "round 82 (improved, score held)", "round 97 (improved, score held)")
open(p, "w").write("\n".join(L))
E
}
c2() { local out rc; out=$(python3 $W/count-c2.py "$2" --repo "$D" --work "$S" 2>&1); rc=$?
  local got=unmet; [[ $out == C2=met* ]] && got=met
  local v=AS_EXPECTED; [[ $got == "$3" ]] || { v=UNEXPECTED; unexp=$((unexp+1)); }
  echo "CONTROL c2 $1 expect=$3 rc=$rc $v :: $out"; }
c2 K0c-do-nothing-entering "$ENT" unmet
fix_cells both; P=$(gc "P1c"); c2 P1c-positive-both-cells "$P" met
git -C "$D" checkout -q --detach "$ENT"; fix_cells op; R=$(gc "K1c"); c2 K1c-one-cell-only "$R" unmet
git -C "$D" checkout -q --detach "$ENT"; fix_cells harmed; R=$(gc "K2c"); c2 K2c-wrong-verdict-word "$R" unmet
git -C "$D" checkout -q --detach "$P"; sed -i '11s/^| operability | 7 |/| operability | 8 |/' "$D/SCORECARD.md"; R=$(gc "K3c"); c2 K3c-score-cell-edited "$R" unmet
git -C "$D" checkout -q --detach "$P"; printf '\n# forged\n' >> "$D/tools/mori-scorecard-calibration.py"; R=$(gc "K4c"); c2 K4c-tool-bytes-changed "$R" unmet
echo "CONTROLS_DONE unexpected=$unexp"
