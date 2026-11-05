#!/usr/bin/env bash
# equiv-c2.sh — round-93 wave w1 C2 equivalence harness (seat Mo93E03Equiv).
#
# Proves byte-level equivalence of the four C2-relevant tools between two
# revisions of the lane repo. For each revision the three C2 tools plus
# tools/mori-round17-jj-regressions.py are git-archived into that side's own
# scratch subdirectory; then each tool's --help and --selftest is run with cwd
# at the extracted tree root, capturing stdout, stderr and rc on both sides.
# Artifacts compared per tool: the archived file itself plus the six capture
# files of --help and --selftest.
#
# Usage: equiv-c2.sh <rev-A> <rev-B> [scratch-root]
#   rev-A rev-B    revisions resolvable in the source repo; the repo is
#                  "$EQUIV_REPO" if set, else the caller's cwd
#   scratch-root   optional parent for this run's work tree; default is a
#                  fresh mkdtemp directory under TMPDIR. This run's work tree
#                  (including every side tree and captured artifact) is removed
#                  on exit; a caller-named scratch-root itself is left in place.
# Output: "A=<sha>", "B=<sha>", one "<tool>: identical|different" line per
#         tool (different lines name the differing artifacts), and
#         "OVERALL: identical|different".
# Exit: 0 every tool identical; 1 at least one difference; 2 setup error.
# No host literals; honours TMPDIR; writes only inside its own work tree.
set -u -o pipefail

die() { printf 'EQUIV_SETUP %s\n' "$*" >&2; exit 2; }

A=${1:-}; B=${2:-}; SCRATCH=${3:-}
[ -n "$A" ] && [ -n "$B" ] || die "usage: equiv-c2.sh <rev-A> <rev-B> [scratch-root]"
REPO=${EQUIV_REPO:-$PWD}
git -C "$REPO" rev-parse --verify -q "$A^{commit}" >/dev/null || die "revision unresolvable: $A"
git -C "$REPO" rev-parse --verify -q "$B^{commit}" >/dev/null || die "revision unresolvable: $B"
RA=$(git -C "$REPO" rev-parse "$A^{commit}") || die "rev-parse failed: $A"
RB=$(git -C "$REPO" rev-parse "$B^{commit}") || die "rev-parse failed: $B"

# The three C2 tools (count-c2.py TOOLS) plus the fourth file named by the
# round-93 wave spec. --selftest runs on all four: each declares one.
TOOLS=(
    mori-blind-check.sh
    mori-misroot-sweep.py
    mori-round17-context-check.py
    mori-round17-jj-regressions.py
)

if [ -n "$SCRATCH" ]; then
    mkdir -p -- "$SCRATCH" || die "cannot create scratch-root: $SCRATCH"
    WORK=$(mktemp -d "$SCRATCH/equiv-c2.XXXXXXXX") || die "mkdtemp failed under: $SCRATCH"
else
    WORK=$(mktemp -d) || die "mkdtemp failed (is TMPDIR usable?)"
fi
trap 'rm -rf -- "$WORK"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

run_side() { # <side-label> <resolved-sha>
    local side=$1 rev=$2
    local tree="$WORK/$side/tree" tmp="$WORK/$side/tmp" t
    mkdir -p -- "$tree" "$tmp" || die "cannot lay out work tree for side $side"
    if ! git -C "$REPO" archive "$rev" -- "${TOOLS[@]/#/tools/}" | tar -x -C "$tree"; then
        die "git archive of the four tools failed for side $side at $rev"
    fi
    for t in "${TOOLS[@]}"; do
        [ -f "$tree/tools/$t" ] || die "tools/$t missing at $rev"
    done
    # Tool scratch stays outside the extracted trees (tools must not see the
    # tree they came from as ambient repo state, and mori-round17-jj-regressions
    # refuses a scratch parent that overlaps the tree or cwd).
    local t run
    for t in "${TOOLS[@]}"; do
        case $t in
            *.sh) run=(bash "tools/$t") ;;
            *)    run=(python3 -I "tools/$t") ;;
        esac
        ( cd "$tree" && TMPDIR="$tmp" "${run[@]}" --help ) \
            >"$WORK/$side/$t.help.out" 2>"$WORK/$side/$t.help.err"
        echo $? >"$WORK/$side/$t.help.rc"
        ( cd "$tree" && TMPDIR="$tmp" "${run[@]}" --selftest ) \
            >"$WORK/$side/$t.selftest.out" 2>"$WORK/$side/$t.selftest.err"
        echo $? >"$WORK/$side/$t.selftest.rc"
    done
}

run_side A "$RA"
run_side B "$RB"

printf 'A=%s\nB=%s\n' "$RA" "$RB"
VERDICT=0
for t in "${TOOLS[@]}"; do
    bad=""
    for a in "tree/tools/$t" "$t.help.out" "$t.help.err" "$t.help.rc" \
             "$t.selftest.out" "$t.selftest.err" "$t.selftest.rc"; do
        cmp -s "$WORK/A/$a" "$WORK/B/$a" || bad="$bad $a"
    done
    if [ -z "$bad" ]; then
        printf '%s: identical\n' "$t"
    else
        printf '%s: different [%s ]\n' "$t" "${bad# }"
        VERDICT=1
    fi
done
if [ "$VERDICT" -eq 0 ]; then
    printf 'OVERALL: identical\n'
else
    printf 'OVERALL: different\n'
fi
exit "$VERDICT"
