#!/usr/bin/env bash
# make-receipts.sh — generate the three frozen round-85 P-C2 receipts (the D84-4 receipt gap).
#
# Usage (from the lane root):  .ufo/waves/round-85/make-receipts.sh <rev> [--repo DIR]
#
# Writes exactly three files, each carrying the frozen P-C2 header grammar graded by
# .ufo/waves/round-85/count-c2.py (exactly one `# cmd:`, one `# rev:`, one `# limits:`,
# exactly one `# ---` separator, at least one `# counter-sha256: <64-hex> <path>` whose
# sha256 is the named path's bytes at <rev>, body after the separator):
#
#   .ufo/waves/round-85/evidence/after-r85.txt
#       body: count-c1.py then count-c3.py run at <rev> from the lane root;
#       bindings pin count-c1.py, count-c2.py, count-c3.py bytes at <rev>.
#   .ufo/waves/round-85/evidence/record-sweep-r85.txt
#       body: `python3 -I tools/mori-record-sweep.py --root . --pins
#       .ufo/waves/round-82/record-pins.json` worktree run; binding pins
#       tools/mori-record-sweep.py at <rev>.
#   .ufo/waves/round-85/evidence/claim-sweep-r85.txt
#       body: `python3 -I tools/mori-claim-sweep.py --root . --pins
#       .ufo/waves/round-80/claim-pins.json` worktree run; binding pins
#       tools/mori-claim-sweep.py at <rev>.
#
# The revision is taken from argv and resolved with `git rev-parse <rev>^{commit}` — never
# invented. Scratch stays under HYAKU_SCRATCH (default /fast/scratch/hyaku), never /tmp; the
# counters inherit HYAKU_SCRATCH for their own scratch. Each body is the raw stdout of its
# command(s) with raw stderr appended when non-empty — nothing is added or edited. Read-only
# on the repo: only `git rev-parse`, `git cat-file -e` and `git show` touch git; the script
# writes nothing else in the repo. Exit 0 receipts written, 2 setup error.
set -euo pipefail

usage() {
    printf 'usage: make-receipts.sh <rev> [--repo DIR]\n' >&2
    exit 2
}

REV=""
REPO="$PWD"
while [ $# -gt 0 ]; do
    case "$1" in
        --repo)
            [ $# -ge 2 ] || usage
            REPO="$2"; shift 2 ;;
        --repo=*)
            REPO="${1#--repo=}"; shift ;;
        -h|--help)
            printf 'usage: make-receipts.sh <rev> [--repo DIR]\n'
            exit 0 ;;
        -*)
            usage ;;
        *)
            [ -z "$REV" ] || usage
            REV="$1"; shift ;;
    esac
done
[ -n "$REV" ] || usage
[ -d "$REPO" ] || { printf 'make-receipts.sh: not a directory: %s\n' "$REPO" >&2; exit 2; }

TOP="$(git -C "$REPO" rev-parse --show-toplevel 2>/dev/null || true)"
[ -n "$TOP" ] || { printf 'make-receipts.sh: not a git repository: %s\n' "$REPO" >&2; exit 2; }
if [ "$TOP" != "$REPO" ]; then
    printf 'make-receipts.sh: --repo must be the lane root (git toplevel: %s)\n' "$TOP" >&2
    exit 2
fi
REPO="$TOP"
cd "$REPO"

# Frozen inputs (repo-relative), per P-C2 of .ufo/waves/round-85/contract.md.
W=".ufo/waves/round-85"
EV="$W/evidence"
C1="$W/count-c1.py"
C2="$W/count-c2.py"
C3="$W/count-c3.py"
RS="tools/mori-record-sweep.py"
CS="tools/mori-claim-sweep.py"
RP=".ufo/waves/round-82/record-pins.json"
CP=".ufo/waves/round-80/claim-pins.json"

for p in "$C1" "$C2" "$C3" "$RS" "$CS" "$RP" "$CP"; do
    [ -f "$p" ] || { printf 'make-receipts.sh: missing worktree file %s\n' "$p" >&2; exit 2; }
done

# Resolve the revision; never invent one.
REV="$(git -C "$REPO" rev-parse --verify "${REV}^{commit}")" || {
    printf 'make-receipts.sh: unresolvable revision %s\n' "$REV" >&2
    exit 2
}
for p in "$C1" "$C2" "$C3" "$RS" "$CS"; do
    git -C "$REPO" cat-file -e "$REV:$p" 2>/dev/null || {
        printf 'make-receipts.sh: %s absent at %s\n' "$p" "$REV" >&2
        exit 2
    }
done

# Scratch under HYAKU_SCRATCH (never /tmp); the counters inherit it for their own scratch.
S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r85/make-receipts-$$"
mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
export HYAKU_SCRATCH="$S"

sha_at_rev() { # repo-relative path -> sha256 of its bytes at $REV (as count-c2.py measures)
    git -C "$REPO" show "$REV:$1" | sha256sum | cut -d' ' -f1
}

run_to() { # run_to <stdout-file> <stderr-file> <cmd...> — rc visible in the body's summary
    local o="$1" e="$2"
    shift 2
    "$@" >"$o" 2>"$e" || true
}

warn_missing() { # <file> <token> — note only; the counter, not this script, grades the token
    if ! grep -qF -- "$2" "$1"; then
        printf 'make-receipts.sh: note: body lacks %s (the run did not print it at %s)\n' \
            "$2" "$REV" >&2
    fi
}

# --- body 1: the C1 and C3 counters run at $REV from the lane root (cmd order = body order)
run_to "$S/c1.out" "$S/c1.err" python3 -I "$C1" "$REV"
run_to "$S/c3.out" "$S/c3.err" python3 -I "$C3" "$REV"
: > "$S/body1"
cat "$S/c1.out" >> "$S/body1"
if [ -s "$S/c1.err" ]; then cat "$S/c1.err" >> "$S/body1"; fi
cat "$S/c3.out" >> "$S/body1"
if [ -s "$S/c3.err" ]; then cat "$S/c3.err" >> "$S/body1"; fi

# --- body 2/3: the two sweeps run in the lane worktree (cwd = lane root)
run_to "$S/rs.out" "$S/rs.err" python3 -I "$RS" --root . --pins "$RP"
: > "$S/body2"
cat "$S/rs.out" >> "$S/body2"
if [ -s "$S/rs.err" ]; then cat "$S/rs.err" >> "$S/body2"; fi

run_to "$S/cs.out" "$S/cs.err" python3 -I "$CS" --root . --pins "$CP"
: > "$S/body3"
cat "$S/cs.out" >> "$S/body3"
if [ -s "$S/cs.err" ]; then cat "$S/cs.err" >> "$S/body3"; fi

warn_missing "$S/body1" 'C1=met'
warn_missing "$S/body1" 'C3=met'
warn_missing "$S/body2" 'RECORD_SWEEP'
warn_missing "$S/body3" 'CLAIM_SWEEP'

sha_c1="$(sha_at_rev "$C1")"
sha_c2="$(sha_at_rev "$C2")"
sha_c3="$(sha_at_rev "$C3")"
sha_rs="$(sha_at_rev "$RS")"
sha_cs="$(sha_at_rev "$CS")"

LIMIT_AFTER='named limit — the C1 and C3 bodies above are counter runs at the named revision while the two sweep receipts'"'"' bodies are worktree runs pinned to the same bytes by their counter-sha256 bindings'
LIMIT_RS='named limit — this body is a worktree run while the binding pins the sweep tool bytes at the revision, not the worktree bytes'
LIMIT_CS='named limit — this body is a worktree run while the binding pins the sweep tool bytes at the revision, not the worktree bytes'

mkdir -p "$EV"

tmp="$EV/.after-r85.txt.$$"
{
    printf '# receipt: after-r85.txt\n'
    printf '# cmd: python3 -I %s %s; python3 -I %s %s\n' "$C1" "$REV" "$C3" "$REV"
    printf '# rev: %s\n' "$REV"
    printf '# counter-sha256: %s %s\n' "$sha_c1" "$C1"
    printf '# counter-sha256: %s %s\n' "$sha_c2" "$C2"
    printf '# counter-sha256: %s %s\n' "$sha_c3" "$C3"
    printf '# limits: %s\n' "$LIMIT_AFTER"
    printf '# ---\n'
    cat "$S/body1"
} > "$tmp"
mv -f "$tmp" "$EV/after-r85.txt"

tmp="$EV/.record-sweep-r85.txt.$$"
{
    printf '# receipt: record-sweep-r85.txt\n'
    printf '# cmd: python3 -I %s --root . --pins %s\n' "$RS" "$RP"
    printf '# rev: %s\n' "$REV"
    printf '# counter-sha256: %s %s\n' "$sha_rs" "$RS"
    printf '# limits: %s\n' "$LIMIT_RS"
    printf '# ---\n'
    cat "$S/body2"
} > "$tmp"
mv -f "$tmp" "$EV/record-sweep-r85.txt"

tmp="$EV/.claim-sweep-r85.txt.$$"
{
    printf '# receipt: claim-sweep-r85.txt\n'
    printf '# cmd: python3 -I %s --root . --pins %s\n' "$CS" "$CP"
    printf '# rev: %s\n' "$REV"
    printf '# counter-sha256: %s %s\n' "$sha_cs" "$CS"
    printf '# limits: %s\n' "$LIMIT_CS"
    printf '# ---\n'
    cat "$S/body3"
} > "$tmp"
mv -f "$tmp" "$EV/claim-sweep-r85.txt"

printf 'make-receipts.sh: wrote %s (rev %s)\n' "$EV/after-r85.txt" "$REV"
printf 'make-receipts.sh: wrote %s (rev %s)\n' "$EV/record-sweep-r85.txt" "$REV"
printf 'make-receipts.sh: wrote %s (rev %s)\n' "$EV/claim-sweep-r85.txt" "$REV"
