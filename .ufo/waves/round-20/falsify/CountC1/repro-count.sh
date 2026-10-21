#!/usr/bin/env bash
# CountC1 falsify scratch. Re-runs the contract C1 counting command with explicit GNU
# binaries (absolute /usr/bin paths; bare names in the agent shell resolve to builtins).
# Inputs are read-only; every output lands under the CountC1 scratch directory.
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
S="$LANE/.ufo/waves/round-20/falsify/CountC1"
E="$LANE/.ufo/waves/round-20/evidence"
R13="$LANE/.ufo/waves/round-13/evidence/drift-classification.json"
R20="$LANE/corpus/evidence/drift-classification-r20.json"
mkdir -p "$S" && cd "$LANE" || exit 2

# DRIFT inputs: (a) .stdout of the entering capture, (b) first line of the r10 pre-pin capture.
/usr/bin/jq -r .stdout "$E/c1-drift-entering.json" > "$S/drift-entering.stdout.txt"
IFS= read -r R10L1 < "$E/c1-drift-r10-prepin.txt"
printf '%s\n' "$R10L1" > "$S/drift-r10-prepin.line1.txt"

# Controls: whole r10 pre-pin file (includes rc=1 trailer); whole post-pin file; raw entering JSON.
drifts="entering:$S/drift-entering.stdout.txt r10L1:$S/drift-r10-prepin.line1.txt r10full:$E/c1-drift-r10-prepin.txt postpin:$E/c1-drift-r20-postpin.txt entering-json:$E/c1-drift-entering.json"
regs="r13:$R13 r20:$R20"

for dpair in $drifts; do
  dlabel=${dpair%%:*}; dr=${dpair#*:}
  for rpair in $regs; do
    rlabel=${rpair%%:*}; rg=${rpair#*:}
    # gnu-ambient: contract text with GNU tools; only the first sort inherits LANG=en_US.UTF-8.
    # gnu-c: every stage LC_ALL=C (collation-safe reference).
    for mode in gnu-ambient gnu-c; do
      out="$S/unclassified.$mode.$dlabel.$rlabel.txt"
      err="$S/stderr.$mode.$dlabel.$rlabel.txt"
      first="$S/first-input.$mode.$dlabel.txt"
      if [ "$mode" = gnu-ambient ]; then
        /usr/bin/tr ' ' '\n' < "$dr" | /usr/bin/grep -v '^MORI_DRIFT:$' | /usr/bin/grep . | /usr/bin/sort -u > "$first"
        LC_ALL=C /usr/bin/comm -23 "$first" \
          <(/usr/bin/jq -r '.tokens|keys[]' "$rg" | LC_ALL=C /usr/bin/sort -u) > "$out" 2> "$err"
      else
        LC_ALL=C /usr/bin/tr ' ' '\n' < "$dr" | LC_ALL=C /usr/bin/grep -v '^MORI_DRIFT:$' | LC_ALL=C /usr/bin/grep . | LC_ALL=C /usr/bin/sort -u > "$first"
        LC_ALL=C /usr/bin/comm -23 "$first" \
          <(/usr/bin/jq -r '.tokens|keys[]' "$rg" | LC_ALL=C /usr/bin/sort -u) > "$out" 2> "$err"
      fi
      rc=$?
      # Is the first input really in C order (the order comm -23 assumes)?
      LC_ALL=C /usr/bin/sort -c -u "$first" 2> "$first.sortcheck"; sc=$?
      echo "mode=$mode DRIFT=$dlabel REG=$rlabel count=$(/usr/bin/wc -l < "$out") comm_rc=$rc first_is_C_sorted_rc=$sc stderr_bytes=$(/usr/bin/wc -c < "$err")"
    done
  done
done
