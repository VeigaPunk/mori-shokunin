#!/usr/bin/env bash
# Frozen-run verifier for the round-31 blind-writer gate tools/mori-blind-check.sh.
#
# Layout (all paths relative to this script's directory):
#   expected.json                     pinned digests, expected stdout, expected exit
#   snapshot/                         the gate's inputs: the 4 round-30 writer briefs
#                                     (.ufo/waves/round-30/w1/CaseR30[abcd].md) and the
#                                     round-30 allow file (snapshot/allow-r30.txt)
#   tool/mori-blind-check.sh          the pinned gate bytes (copied from lane git objects)
#
# Contract:
#   exit 0  the pinned tool, over the pinned snapshot, reproduced the pinned stdout and exit code
#   exit 1  the run differed from expected.json (stdout, exit code, or the pinned tool bytes)
#   exit 2  snapshot_tampered: a pinned file is missing, or a snapshot input digest differs
#           from expected.json. The tool is NOT run in that case.
#
# The tool reads briefs from a git tree (it takes a lane revision and a wave-report dir),
# so the snapshot is materialised into a throwaway git repository under $TMPDIR. The lane
# is never written to, never read for the run, and never used as the working tree.
set -o nounset -o pipefail
set -f
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE

FC_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
EXPECTED="$FC_DIR/expected.json"
TOOL="$FC_DIR/tool/mori-blind-check.sh"

usage() { printf 'usage: verify.sh\n' >&2; }

# --- 0. the pinned table itself must exist ------------------------------------
if [[ ! -f $EXPECTED ]]; then
    printf 'snapshot_tampered\n'
    printf 'verify: missing pinned table: %s\n' "$EXPECTED" >&2
    exit 2
fi

read_field() { python3 - "$EXPECTED" "$1" <<'PY'
import json, sys
v = json.load(open(sys.argv[1]))
for part in sys.argv[2].split("."):
    v = v[part]
print(v)
PY
}

# A malformed pinned table is a setup error (exit 2, not a compared verdict).
if ! python3 - "$EXPECTED" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
for k in ("tool", "snapshot_inputs", "invocation", "expected_stdout", "expected_exit"):
    if k not in d:
        raise SystemExit(1)
if "sha256" not in d["tool"] or "path" not in d["tool"]:
    raise SystemExit(1)
for k in ("wave_report_dir", "writer_name_regex", "allow_file"):
    if k not in d["invocation"]:
        raise SystemExit(1)
for e in d["snapshot_inputs"]:
    if "path" not in e or "sha256" not in e:
        raise SystemExit(1)
PY
then
    printf 'verify: pinned table is missing, unreadable or not valid JSON/schema: %s\n' "$EXPECTED" >&2
    exit 2
fi

WAVE_DIR=$(read_field invocation.wave_report_dir)
WRITER_RE=$(read_field invocation.writer_name_regex)
ALLOW_REL=$(read_field invocation.allow_file)
EXPECTED_EXIT=$(read_field expected_exit)
TOOL_SHA=$(read_field tool.sha256)

# --- 1. verify every pinned digest before anything else ------------------------
mapfile -t INPUT_ROWS < <(python3 - "$EXPECTED" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
for p in d["snapshot_inputs"]:
    print("%s\t%s" % (p["path"], p["sha256"]))
PY
)

tampered() {
    printf 'snapshot_tampered\n'
    printf 'verify: %s\n' "$1" >&2
    exit 2
}

if [[ ! -f $TOOL ]]; then
    tampered "missing pinned tool: $TOOL"
fi

for row in "${INPUT_ROWS[@]}"; do
    rel=${row%%$'\t'*}
    want=${row#*$'\t'}
    file="$FC_DIR/$rel"
    [[ -f $file ]] || tampered "missing pinned snapshot input: $rel"
    got=$(sha256sum -- "$file" | cut -d' ' -f1)
    [[ $got == "$want" ]] || tampered "digest mismatch: $rel (expected $want, got $got)"
done

tool_got=$(sha256sum -- "$TOOL" | cut -d' ' -f1)
tool_matches=1
if [[ $tool_got != "$TOOL_SHA" ]]; then
    tool_matches=0
    printf 'verify: pinned tool bytes differ (expected %s, got %s)\n' "$TOOL_SHA" "$tool_got" >&2
fi

ALLOW_FILE="$FC_DIR/$ALLOW_REL"
[[ -f $ALLOW_FILE ]] || tampered "missing pinned allow file: $ALLOW_REL"

# --- 2. run the pinned tool over the pinned snapshot ---------------------------
WORK=$(mktemp -d "${TMPDIR:-/tmp}/blind-check-frozen.XXXXXX") || { printf 'verify: cannot create work dir\n' >&2; exit 2; }
cleanup() { rm -rf -- "$WORK"; }
trap cleanup EXIT

REPO="$WORK/repo"
mkdir -p "$REPO"
# The snapshot keeps the lane's own tree under snapshot/: snapshot/.ufo/waves/... is
# committed to the throwaway repo as .ufo/waves/..., so the hit paths the tool prints
# match the pinned expected_stdout byte for byte. snapshot/allow-r30.txt lands at the
# repo root and is passed to the tool by its frozen path, not read from the tree.
for row in "${INPUT_ROWS[@]}"; do
    rel=${row%%$'\t'*}
    repo_rel=${rel#snapshot/}
    mkdir -p "$REPO/$(dirname -- "$repo_rel")"
    cp -- "$FC_DIR/$rel" "$REPO/$repo_rel"
done

git -C "$REPO" init -q . >/dev/null 2>&1 || { printf 'verify: git init failed\n' >&2; exit 2; }
git -C "$REPO" add -A >/dev/null 2>&1
git -C "$REPO" -c user.name='BlindCheckFrozen' -c user.email='frozen@example.invalid' \
    commit -q -m 'frozen snapshot' >/dev/null 2>&1 || { printf 'verify: git commit failed\n' >&2; exit 2; }
REV=$(git -C "$REPO" rev-parse HEAD)

stdout_file="$WORK/stdout.txt"
stderr_file="$WORK/stderr.txt"
( cd -- "$REPO" && bash -- "$TOOL" "$REV" "$WAVE_DIR" "$WRITER_RE" "$ALLOW_FILE" ) \
    >"$stdout_file" 2>"$stderr_file"
actual_exit=$?

mapfile -t EXPECTED_LINES < <(python3 - "$EXPECTED" <<'PY'
import json, sys
for line in json.load(open(sys.argv[1]))["expected_stdout"]:
    print(line)
PY
)
mapfile -t ACTUAL_LINES < "$stdout_file"

diff_report=''
if [[ ${#EXPECTED_LINES[@]} -ne ${#ACTUAL_LINES[@]} ]]; then
    diff_report="line count differs (expected ${#EXPECTED_LINES[@]}, got ${#ACTUAL_LINES[@]})"
else
    for i in "${!EXPECTED_LINES[@]}"; do
        if [[ ${EXPECTED_LINES[$i]} != "${ACTUAL_LINES[$i]}" ]]; then
            diff_report="line $((i + 1)) differs: expected '${EXPECTED_LINES[$i]}', got '${ACTUAL_LINES[$i]}'"
            break
        fi
    done
fi

# --- 3. compare stdout and exit code with expected.json ------------------------
status=0
if [[ -n $diff_report ]]; then
    status=1
    printf 'verify: stdout differs: %s\n' "$diff_report" >&2
fi
if [[ $actual_exit -ne $EXPECTED_EXIT ]]; then
    status=1
    printf 'verify: exit code differs (expected %s, got %s)\n' "$EXPECTED_EXIT" "$actual_exit" >&2
fi
if (( ! tool_matches )); then
    status=1
    printf 'verify: pinned tool bytes changed; the frozen verdict was not reproduced under the pinned tool\n' >&2
fi

printf 'tool_sha256=%s\n' "$tool_got"
printf 'tool_exit=%s (expected %s)\n' "$actual_exit" "$EXPECTED_EXIT"
if (( status == 0 )); then
    printf 'frozen_run: match\n'
    exit 0
fi
printf 'frozen_run: differ\n'
exit 1
