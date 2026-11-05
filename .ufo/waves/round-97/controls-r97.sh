#!/usr/bin/env bash
# mori round 97 -- pre-freeze control battery for the frozen counters count-c1.py / count-c2.py.
# Usage: controls-r97.sh <entering-rev> <candidate-dir>
#   <candidate-dir> holds the candidate inputs built before the freeze:
#     skill-append.md   (the four registry rows, appended to SKILL.md for the positive control)
#     S615.html S616.html S623.html  (the candidate pinned copies)
# Every fixture is a `git archive` of <entering-rev> under $HYAKU_SCRATCH/mori-r97/controls,
# removed on exit. Expected verdicts are printed BEFORE each run (EXPECT line) and compared.
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
W=$LANE/.ufo/waves/round-97
REV=$1; CAND=$2
ROOT=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r97/controls
rm -rf -- "$ROOT"; mkdir -p "$ROOT"; trap 'rm -rf -- "$ROOT"' EXIT
export TMPDIR=$ROOT
mk() { local d=$ROOT/$1; mkdir -p "$d"; git -C "$LANE" archive "$REV" | tar -x -C "$d"; echo "$d"; }
pins() { mkdir -p "$1/corpus/evidence/sources-r97"; cp "$CAND/S615.html" "$CAND/S616.html" "$CAND/S623.html" "$1/corpus/evidence/sources-r97/"; }
fails=0
run() { # name expect-rc expect-substring cmd...
  local name=$1 erc=$2 esub=$3; shift 3
  echo "## $name"; echo "EXPECT rc=$erc contains='$esub'"; echo "\$ $*"
  local out; out=$("$@" 2>&1); local rc=$?
  printf '%s\n' "$out" | grep -E '^(C1|C2|TARGET|registered=|REGISTRY|DIGEST_CHECK|LIVE S6|LIVE MORI)' 
  if [ "$rc" = "$erc" ] && printf '%s' "$out" | grep -qF -- "$esub"; then echo "OBSERVED rc=$rc -> AS_EXPECTED"; else echo "OBSERVED rc=$rc -> UNEXPECTED"; fails=$((fails+1)); fi
  echo
}
echo "CONTROLS rev=$(git -C "$LANE" rev-parse "$REV") count-c1.sha256=$(sha256sum "$W/count-c1.py" | cut -c1-64) count-c2.sha256=$(sha256sum "$W/count-c2.py" | cut -c1-64) date=$(date -u +%FT%TZ)"
echo "candidate S615=$(sha256sum "$CAND/S615.html" | cut -c1-64) S616=$(sha256sum "$CAND/S616.html" | cut -c1-64) S623=$(sha256sum "$CAND/S623.html" | cut -c1-64) skill-append=$(sha256sum "$CAND/skill-append.md" | cut -c1-64)"
echo

# ---- C1 -------------------------------------------------------------------
D=$(mk c1-donothing)
run "C1 do-nothing (entering tree)" 1 "C1=unmet unregistered=4" python3 "$W/count-c1.py" --root "$D"

D=$(mk c1-junkrows)
{ printf '\n| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n|---|---|---|---|---|---|---|---|\n'
  for t in cgroup-pressure drift-recheck scorecard-calibration source-digest; do
    printf '| junk %s | x | `python3 tools/mori-%s.py` | x | x | x | x | x |\n' "$t" "$t"; done; } >> "$D/SKILL.md"
run "C1 forgery: eight-cell junk rows (auditor alone goes green)" 1 "C1=unmet unregistered=0 registry=met targets_ok=0/4" python3 "$W/count-c1.py" --root "$D"

D=$(mk c1-staleline)
sed -e 's/pass=12 fail=0/pass=11 fail=0/' -e 's/PASS (10 cases)/PASS (9 cases)/' -e 's/CALIB_SELFTEST pass=11/CALIB_SELFTEST pass=10/' -e 's/DIGEST_SELFTEST pass=11/DIGEST_SELFTEST pass=10/' "$CAND/skill-append.md" >> "$D/SKILL.md"
run "C1 forgery: well-formed rows stating a wrong selftest outcome" 1 "C1=unmet unregistered=0 registry=met targets_ok=0/4" python3 "$W/count-c1.py" --root "$D"

D=$(mk c1-notoken)
sed -e 's/DIGEST_CHECK/DIGEST-SUMMARY/g' "$CAND/skill-append.md" >> "$D/SKILL.md"
run "C1 forgery: verdict map without the tool's verdict token (digest row)" 1 "targets_ok=3/4" python3 "$W/count-c1.py" --root "$D"

D=$(mk c1-positive)
cat "$CAND/skill-append.md" >> "$D/SKILL.md"
run "C1 positive control (candidate rows)" 0 "C1=met unregistered=0 registry=met targets_ok=4/4" python3 "$W/count-c1.py" --root "$D"

# ---- C2 -------------------------------------------------------------------
D=$(mk c2-donothing)
run "C2 do-nothing (entering tree)" 1 "unpinned=3" python3 "$W/count-c2.py" --root "$D"

D=$(mk c2-hole)
pins "$D"; head -c 362493 /dev/urandom > "$D/corpus/evidence/sources-r97/S615.html"
run "C2 forgery: random 362493-byte S615 copy (digest tool supersedes it: the r96 hole)" 1 "hole_guard=fail" python3 "$W/count-c2.py" --root "$D" --no-live

D=$(mk c2-livebytes)
pins "$D"; curl -sS -o "$D/corpus/evidence/sources-r97/S616.html" https://docs.python.org/3/library/tokenize.html
run "C2 forgery: today's live S616 bytes pinned as the recorded copy" 1 "C2=unmet mismatch=1" python3 "$W/count-c2.py" --root "$D" --no-live

D=$(mk c2-contentdrift)
pins "$D"; sed -i 's#https://docs.python.org/3/using/cmdline.html#https://docs.python.org/3/using/configure.html#' "$D/corpus/SOURCES.md"
run "C2 forgery: correct pins, S623 row pointed at another live page (live leg must fail alone)" 1 "checks_failed=live" python3 "$W/count-c2.py" --root "$D"

D=$(mk c2-positive)
pins "$D"
run "C2 positive control (candidate pins, live leg on)" 0 "C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass" python3 "$W/count-c2.py" --root "$D"

echo "CONTROLS_DONE unexpected=$fails"
[ "$fails" = 0 ]
