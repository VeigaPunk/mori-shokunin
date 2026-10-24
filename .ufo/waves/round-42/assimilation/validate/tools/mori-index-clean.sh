#!/usr/bin/env bash
# mori-index-clean.sh — read-only gate: is the git index of <repo> clean?
#
# Exit codes
#   0  clean: no staged path and no intent-to-add entry (unstaged worktree
#      edits to tracked files are not index state and do not count; L1 round 36)
#   1  not clean: at most 20 offending paths are listed
#   2  usage error, <repo> missing or not a git repository, or git failed
#
# Nothing is written. Every git call runs with --no-optional-locks and
# GIT_OPTIONAL_LOCKS=0, so git never refreshes or rewrites .git/index, and no
# command in this script mutates the repository it inspects.
#
# Detection method for intent-to-add entries (`git add -N`):
#   `git diff --cached` does NOT list intent-to-add entries, and
#   `git ls-files --stage` cannot tell them apart from a genuinely staged
#   empty file (both carry the empty blob e69de29...). The two reliable
#   signals are the porcelain records:
#     - porcelain v1: an intent-to-add path shows as XY = " A"
#     - porcelain v2: an intent-to-add path shows as a type-1 record whose XY
#       is ".A" (index side unmodified, worktree side added)
#   This script counts them from both and refuses to report a verdict when the
#   two disagree.
set -o nounset -o pipefail
set -f
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
export GIT_OPTIONAL_LOCKS=0

MAX_PATHS=20
SUMMARY_PREFIX='MORI_INDEX_CLEAN'
SELFTEST_PREFIX='MORI_INDEX_CLEAN_SELFTEST'

err() { printf '%s_ERROR %s\n' "$SUMMARY_PREFIX" "$*" >&2; }

usage() {
    printf 'usage: mori-index-clean.sh <repo> | --selftest\n' >&2
}

# git, with the ambient index/work-tree overrides removed and no optional
# locks (so git never writes .git/index just to refresh stat information).
g() { env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git --no-optional-locks "$@"; }

# Collect the staged paths (index vs HEAD) into the global array STAGED[].
# Intent-to-add entries are deliberately absent here: git skips them.
collect_staged() {
    local repo=$1 p
    STAGED=()
    while IFS= read -r -d '' p; do
        STAGED+=("$p")
    done < <(g -C "$repo" diff --cached --name-only -z 2>/dev/null)
}

# Parse `git status --porcelain --untracked-files=no -z` records.
# Fills STATUS_PATHS[] (every tracked path not in a clean state) and
# ITA_PATHS[] (the subset whose XY is " A", i.e. intent-to-add).
collect_status() {
    local repo=$1 rec xy path
    STATUS_PATHS=()
    ITA_PATHS=()
    while IFS= read -r -d '' rec; do
        xy=${rec:0:2}
        path=${rec:3}
        STATUS_PATHS+=("$path")
        if [[ $xy == ' A' ]]; then
            ITA_PATHS+=("$path")
        fi
        # In -z form a rename/copy record is followed by its original path.
        if [[ ${xy:0:1} == R || ${xy:0:1} == C ]]; then
            IFS= read -r -d '' _ || true
        fi
    done < <(g -C "$repo" status --porcelain --untracked-files=no -z 2>/dev/null)
}

# Count intent-to-add entries from porcelain v2 (type-1 record, XY == ".A").
count_ita_v2() {
    local repo=$1 out
    out=$(g -C "$repo" status --porcelain=v2 --untracked-files=no 2>/dev/null) || return 1
    printf '%s\n' "$out" | grep -c '^1 \.A ' || true
}

# check_repo <repo>
# Sets SUMMARY and LISTED[]; returns 0 (clean) / 1 (not clean) / 2 (error).
check_repo() {
    local repo=$1
    local ita_v2 ita_v1 staged_n shown extra=0
    local -A seen=()
    local p

    if [[ ! -d $repo ]]; then
        err "not a directory: $repo"
        return 2
    fi
    if ! g -C "$repo" rev-parse --git-dir >/dev/null 2>&1; then
        err "not a git repository: $repo"
        return 2
    fi
    if ! g -C "$repo" diff --cached --name-only -z >/dev/null 2>&1; then
        err "git diff --cached failed in $repo"
        return 2
    fi
    if ! g -C "$repo" status --porcelain --untracked-files=no -z >/dev/null 2>&1; then
        err "git status failed in $repo"
        return 2
    fi

    collect_staged "$repo"
    collect_status "$repo"
    ita_v2=$(count_ita_v2 "$repo") || { err "git status --porcelain=v2 failed in $repo"; return 2; }
    ita_v1=${#ITA_PATHS[@]}
    if (( ita_v1 != ita_v2 )); then
        err "intent-to-add disagreement in $repo: porcelain v1=$ita_v1 porcelain v2=$ita_v2"
        return 2
    fi

    staged_n=${#STAGED[@]}
    SUMMARY="${SUMMARY_PREFIX} staged=${staged_n} intent_to_add=${ita_v1}"
    LISTED=()

    if (( staged_n == 0 && ita_v1 == 0 )); then
        return 0
    fi

    # List offenders: intent-to-add paths, then staged paths. Deduplicated,
    # capped at MAX_PATHS.
    for p in ${ITA_PATHS[@]+"${ITA_PATHS[@]}"}; do
        [[ -n ${seen[$p]+x} ]] && continue
        seen[$p]=1
        LISTED+=("$p")
    done
    for p in ${STAGED[@]+"${STAGED[@]}"}; do
        [[ -n ${seen[$p]+x} ]] && continue
        seen[$p]=1
        LISTED+=("$p")
    done
    shown=${#LISTED[@]}
    if (( shown > MAX_PATHS )); then
        extra=$(( shown - MAX_PATHS ))
        LISTED=("${LISTED[@]:0:MAX_PATHS}")
    fi
    MORE=$extra
    return 1
}

run_selftest() {
    local repo out rc pass=0 fail=0

    if ! SANDBOX=$(mktemp -d "${TMPDIR:-/tmp}/mori-index-clean.XXXXXX"); then
        err "mktemp failed"
        return 2
    fi
    trap 'rm -rf "$SANDBOX"' RETURN
    repo="$SANDBOX/repo"
    mkdir -p "$repo" "$SANDBOX/notrepo"

    g init -q -b main "$repo" >/dev/null 2>&1 || { err "git init failed"; return 2; }
    g -C "$repo" config user.email mori@example.invalid
    g -C "$repo" config user.name mori
    printf 'tracked\n' >"$repo/tracked.txt"
    g -C "$repo" add tracked.txt
    g -C "$repo" commit -qm 'init' >/dev/null 2>&1 || { err "git commit failed"; return 2; }

    # case 1: clean repository -> 0
    out=$(bash "$SCRIPT" "$repo" 2>&1); rc=$?
    if (( rc == 0 )) && [[ $out == *"$SUMMARY_PREFIX staged=0 intent_to_add=0"* ]]; then
        pass=$(( pass + 1 ))
    else
        fail=$(( fail + 1 ))
        printf '%s_CASE clean rc=%d out=%s\n' "$SELFTEST_PREFIX" "$rc" "$out" >&2
    fi

    # case 2: `git add -N newfile` -> 1, seen as intent_to_add=1
    printf 'new\n' >"$repo/newfile"
    g -C "$repo" add -N newfile
    out=$(bash "$SCRIPT" "$repo" 2>&1); rc=$?
    if (( rc == 1 )) && [[ $out == *"$SUMMARY_PREFIX staged=0 intent_to_add=1"* ]]; then
        pass=$(( pass + 1 ))
    else
        fail=$(( fail + 1 ))
        printf '%s_CASE intent_to_add rc=%d out=%s\n' "$SELFTEST_PREFIX" "$rc" "$out" >&2
    fi

    # case 3: `git add trackedmod` (staged modification) -> 1
    g -C "$repo" reset -q
    printf 'modified\n' >"$repo/tracked.txt"
    g -C "$repo" add tracked.txt
    out=$(bash "$SCRIPT" "$repo" 2>&1); rc=$?
    if (( rc == 1 )) && [[ $out == *"$SUMMARY_PREFIX staged=1 intent_to_add=0"* ]]; then
        pass=$(( pass + 1 ))
    else
        fail=$(( fail + 1 ))
        printf '%s_CASE staged rc=%d out=%s\n' "$SELFTEST_PREFIX" "$rc" "$out" >&2
    fi

    # case 4: not a repository -> 2
    out=$(bash "$SCRIPT" "$SANDBOX/notrepo" 2>&1); rc=$?
    if (( rc == 2 )); then
        pass=$(( pass + 1 ))
    else
        fail=$(( fail + 1 ))
        printf '%s_CASE not_a_repo rc=%d out=%s\n' "$SELFTEST_PREFIX" "$rc" "$out" >&2
    fi

    printf '%s pass=%d fail=%d\n' "$SELFTEST_PREFIX" "$pass" "$fail"
    (( fail == 0 ))
}

SUMMARY=''
MORE=0
STAGED=()
STATUS_PATHS=()
ITA_PATHS=()
LISTED=()
SANDBOX=''
SCRIPT=$(readlink -f "$0" 2>/dev/null || printf '%s' "$0")

main() {
    local rc p
    if (( $# == 1 )) && [[ $1 == '--selftest' ]]; then
        run_selftest
        return $?
    fi
    if (( $# != 1 )); then
        usage
        return 2
    fi
    check_repo "$1"
    rc=$?
    if (( rc == 2 )); then
        return 2
    fi
    printf '%s\n' "$SUMMARY"
    for p in ${LISTED[@]+"${LISTED[@]}"}; do
        printf '%s_PATH %s\n' "$SUMMARY_PREFIX" "$p"
    done
    if (( MORE > 0 )); then
        printf '%s_MORE %d\n' "$SUMMARY_PREFIX" "$MORE"
    fi
    return "$rc"
}

main "$@"
exit $?
