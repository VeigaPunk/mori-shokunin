#!/bin/sh
# mori round-86 receipt generator (P-C2): writes the two r86 receipts bound to a measured
# revision.
#
# Usage: make-receipts-r86.sh <rev> [--repo DIR]
#
# Writes, into <repo>/.ufo/waves/round-86/evidence/:
#   after-c1-r86.txt      — headers + the command's stdout verbatim (expect met)
#   replay-defeat-r86.txt — same headers plus `# expectation: reject`, one body byte changed
#
# The `# cmd:` line is exactly
#   python3 -I .ufo/waves/round-86/count-c1.py <40-hex rev> --repo <abs repo> --scratch .
# and the body is produced by rehearsing that exact command in a scratch export of the same
# revision (the replay surface the C2 subject and counter use), so the recorded body matches the
# replay byte-for-byte modulo trailing newlines. The command must exit 0 and print a `C1=met`
# reading; the generator refuses to write receipts from any other output.
#
# Transient files live only under ${TMPDIR:-/tmp} and are removed on exit. Read-only on the
# repo (`git rev-parse`, `git show`); the only writes are the two receipt files.
set -eu

usage() {
    echo "usage: $0 <rev> [--repo DIR]" >&2
    exit 2
}

REV=""
REPO=""
while [ $# -gt 0 ]; do
    case "$1" in
        --repo)
            [ $# -ge 2 ] || usage
            REPO=$2
            shift 2
            ;;
        --*)
            usage
            ;;
        *)
            if [ -n "$REV" ]; then
                usage
            fi
            REV=$1
            shift
            ;;
    esac
done
[ -n "$REV" ] || usage
SELF_DIR=$(cd "$(dirname "$0")" && pwd)
LANE=$(cd "$SELF_DIR/../../.." && pwd)
if [ -n "$REPO" ]; then
    REPO=$(cd "$REPO" && pwd)
else
    REPO=$LANE
fi

COMMIT=$(git -C "$REPO" rev-parse "$REV^{commit}") || {
    echo "make-receipts: unresolvable revision $REV in $REPO" >&2
    exit 2
}

C1=".ufo/waves/round-86/count-c1.py"
SHA=$(git -C "$REPO" show "$COMMIT:$C1" | sha256sum | cut -d" " -f1)

WORK=$(mktemp -d "${TMPDIR:-/tmp}/make-receipts-r86.XXXXXX")
trap 'rm -rf -- "$WORK"' EXIT
mkdir -p "$WORK/.ufo/waves/round-86"
git -C "$REPO" show "$COMMIT:$C1" > "$WORK/.ufo/waves/round-86/count-c1.py"

# Rehearse the receipt command exactly as the replay rule will run it: same script bytes at the
# same revision, same working-directory shape, scratch inside the rehearsal tree.
set +e
OUT=$(cd "$WORK" && python3 -I "$C1" "$COMMIT" --repo "$REPO" --scratch . 2>&1)
RC=$?
set -e
if [ "$RC" -ne 0 ]; then
    echo "make-receipts: count-c1 rc=$RC at $COMMIT (need a met reading); output:" >&2
    printf '%s\n' "$OUT" >&2
    exit 3
fi
LAST=$(printf '%s\n' "$OUT" | tail -n 1)
case "$LAST" in
    C1=met\ *) ;;
    *)
        echo "make-receipts: body is not a C1=met reading at $COMMIT" >&2
        printf '%s\n' "$OUT" >&2
        exit 3
        ;;
esac

DEFEAT=$(printf '%s\n' "$OUT" | sed 's/killed=6/killed=7/')
if [ "$DEFEAT" = "$OUT" ]; then
    echo "make-receipts: one-byte defeat edit did not apply (killed=6 absent)" >&2
    exit 3
fi

LIMITS="named limit — the digest pins the counter bytes but not the body; the replay rule closes that gap by re-executing the command in a scratch export of the named revision"

EVDIR="$REPO/.ufo/waves/round-86/evidence"
mkdir -p "$EVDIR"

{
    printf '# receipt: after-c1-r86.txt\n'
    printf '# cmd: python3 -I %s %s --repo %s --scratch .\n' "$C1" "$COMMIT" "$REPO"
    printf '# rev: %s\n' "$COMMIT"
    printf '# counter-sha256: %s %s\n' "$SHA" "$C1"
    printf '# replay: required\n'
    printf '# limits: %s\n' "$LIMITS"
    printf '# ---\n'
    printf '%s\n' "$OUT"
} > "$EVDIR/after-c1-r86.txt"

{
    printf '# receipt: replay-defeat-r86.txt\n'
    printf '# cmd: python3 -I %s %s --repo %s --scratch .\n' "$C1" "$COMMIT" "$REPO"
    printf '# rev: %s\n' "$COMMIT"
    printf '# counter-sha256: %s %s\n' "$SHA" "$C1"
    printf '# replay: required\n'
    printf '# expectation: reject\n'
    printf '# limits: %s\n' "$LIMITS"
    printf '# ---\n'
    printf '%s\n' "$DEFEAT"
} > "$EVDIR/replay-defeat-r86.txt"

echo "make-receipts: wrote after-c1-r86.txt replay-defeat-r86.txt at $COMMIT in $EVDIR"
