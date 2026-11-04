#!/usr/bin/env bash
# Run from any cwd; discovery and instrument execution use the lane root.
set -u

REV=44bc941a0e3e9676fa33a882b43d6e9793cbf74d
while (($#)); do
    case "$1" in
        --rev)
            if (($# < 2)) || [[ -z "$2" ]]; then
                printf 'BATTERY_SETUP --rev requires a revision\n' >&2
                exit 2
            fi
            REV=$2
            shift 2
            ;;
        *)
            printf 'BATTERY_SETUP unknown argument: %s\n' "$1" >&2
            exit 2
            ;;
    esac
done

ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd -P) || exit 2
cd -- "$ROOT" || exit 2
BASE=${HYAKU_SCRATCH:-/fast/scratch/hyaku/mori-r81/Mo81E04Battery}
mkdir -p -- "$BASE" || exit 2
S=$(mktemp -d -- "$BASE/battery.XXXXXXXX") || exit 2
trap 'rm -rf -- "$S"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
mkdir -p -- "$S/tmp" || exit 2
# These two variables also contain scratch allocated by child instruments.
# TMPDIR is essential: disk-rate and round41-calibration otherwise report 0/0.
export TMPDIR="$S/tmp"
export HYAKU_SCRATCH="$S"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C

passed=0
total=0
setup=0
failed=0
run() {
    local label=$1 rc output reason=''
    shift
    printf '$ timeout --kill-after=5s 120s'
    printf ' %q' "$@"
    printf '\n'
    timeout --kill-after=5s 120s "$@" > "$S/output" 2>&1
    rc=$?
    cat -- "$S/output"
    output=$(< "$S/output")
    printf '%s rc=%d\n' "$label" "$rc"
    total=$((total + 1))
    if ((rc == 0)); then
        passed=$((passed + 1))
    else
        # Only exact known early scratch refusals are setup, never arbitrary reds.
        case "$label:$rc:$output" in
            'tools/mori-content-review.py --selftest:2:{"exit_code":2,"findings":[{"code":"CONTENT_REVIEW_SELFTEST_TMPDIR"}],"schema":"mori-content-review-result-v1","status":"could-not-evaluate"}')
                reason='TMPDIR must be beneath lane; tools/mori-content-review.py:364-365' ;;
            'tools/mori-freeze-order.py --selftest:1:SELFTEST freeze-order FAIL 0/11')
                if [[ "$TMPDIR" != "$ROOT/"* ]]; then
                    reason='TMPDIR must be beneath checkout; tools/mori-freeze-order.py:509-514'
                fi ;;
            'tools/mori-retention-gate.py --selftest:2:SELFTEST retention-gate FAIL 0/21')
                if [[ "$TMPDIR" != "$ROOT/.scratch" ]]; then
                    reason='TMPDIR must equal lane/.scratch; tools/mori-retention-gate.py:459,467-468'
                fi ;;
            'tools/mori-round19-regressions.py --selftest:2:R19_SELFTEST setup=explicit-lane-tmpdir-invalid')
                reason='TMPDIR must be canonical lane descendant; tools/mori-round19-regressions.py:888-891' ;;
        esac
        if [[ -n "$reason" ]]; then
            setup=$((setup + 1))
            printf 'SETUP %s rc=%d %s\n' "$label" "$rc" "$reason"
        else
            failed=$((failed + 1))
        fi
    fi
}

# This is textual discovery, including shell instruments, not a fixed registry.
shopt -s nullglob
candidates=(tools/*.py tools/*.sh)
if ((${#candidates[@]} == 0)); then
    printf 'BATTERY_SETUP no instrument candidates\n' >&2
    exit 2
fi
grep -l -- '--selftest' "${candidates[@]}" > "$S/instruments"
discovery_rc=$?
if ((discovery_rc > 1)); then
    printf 'BATTERY_SETUP discovery rc=%d\n' "$discovery_rc" >&2
    exit 2
fi
while IFS= read -r tool; do
    case "$tool" in
        *.py) run "$tool --selftest" python3 -I "$tool" --selftest ;;
        *.sh) run "$tool --selftest" bash "$tool" --selftest ;;
    esac
done < "$S/instruments"

run 'round-80/count-c1.py' python3 -I .ufo/waves/round-80/count-c1.py "$REV"
run 'round-80/count-c3.py' python3 -I .ufo/waves/round-80/count-c3.py "$REV"
run 'round-81/count-c1.py --selftest' python3 -I .ufo/waves/round-81/count-c1.py --selftest
run 'round-81/count-c2.py --selftest' python3 -I .ufo/waves/round-81/count-c2.py --selftest
printf 'BATTERY %d/%d\n' "$passed" "$total"
printf 'BATTERY pass=%d setup=%d fail=%d\n' "$passed" "$setup" "$failed"
if ((failed)); then exit 1; fi
if ((setup)); then exit 2; fi
exit 0
