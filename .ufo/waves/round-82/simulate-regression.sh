#!/usr/bin/env bash
# Delete one r81 survivor-closing fixture per counter, in disposable revisions only.
# Usage: bash simulate-regression.sh [REV [REPO]]
# Exit 0: each deletion exposes exactly its expected survivor; 1: detector defect.
# HYAKU_SCRATCH selects the scratch root; TMPDIR selects allocation within that root.
set -euo pipefail
HERE=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO=${2:-$(git -C "$HERE" rev-parse --show-toplevel)}
REV=$(git -C "$REPO" rev-parse --verify "${1:-HEAD}^{commit}")
ROOT=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r82/Mo82E01C1Regress
mkdir -p -- "$ROOT"
S=$(mktemp -d "$ROOT/simulation.XXXXXXXX")
trap 'rm -rf -- "$S"' EXIT
# A caller's TMPDIR is honoured only when beneath the permitted scratch root.
if [[ -n ${TMPDIR:-} ]]; then
    TMPDIR=$(realpath -m -- "$TMPDIR")
    case "$TMPDIR/" in "$ROOT/"*) mkdir -p -- "$TMPDIR" ;;
        *) printf 'REGRESSION_SETUP TMPDIR must be beneath %s\n' "$ROOT" >&2; exit 2 ;;
    esac
else
    TMPDIR=$S/tmp
    mkdir -p -- "$TMPDIR"
fi
export TMPDIR GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
python3 -I - "$REPO" "$REV" "$S" "$HERE/count-c1.py" <<'PY'
import ast
import hashlib
import io
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile
import zlib

source, revision, scratch, harness = sys.argv[1:]
scratch = Path(scratch)
paths = [".ufo/waves/round-80/count-c1.py", ".ufo/waves/round-80/count-c3.py",
         ".ufo/waves/round-81/count-c2.py", ".ufo/waves/round-80/claim-pins.json",
         ".ufo/waves/round-81/record-pins.json", ".ufo/waves/round-82/count-c1.py"]

def git(*args):
    return subprocess.check_output(["git", "-C", source, *args])

# Copy the revision's real bytes, not synthetic selftest substitutes.
archive = git("archive", revision, "--", *paths)
repo = scratch / "repo"
repo.mkdir()
with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
    bundle.extractall(repo, filter="data")
gitdir = repo / ".git"
(gitdir / "objects/info").mkdir(parents=True)
(gitdir / "refs/heads").mkdir(parents=True)
objects = git("rev-parse", "--path-format=absolute", "--git-path", "objects").decode().strip()
(gitdir / "objects/info/alternates").write_text(objects + "\n")
(gitdir / "HEAD").write_text(revision + "\n")
(gitdir / "config").write_text("[core]\n\trepositoryformatversion = 0\n\tbare = false\n")
assert subprocess.check_output(["git", "-C", str(repo), "rev-parse", "--show-toplevel"]).decode().strip() == str(repo)

# Materialize disposable commit objects directly: no git mutation commands, index,
# hooks, user identity, or writes to the source object database are needed.
def store(kind, body):
    raw = kind.encode() + b" " + str(len(body)).encode() + b"\0" + body
    oid = hashlib.sha1(raw).hexdigest()
    target = gitdir / "objects" / oid[:2] / oid[2:]
    target.parent.mkdir(exist_ok=True)
    target.write_bytes(zlib.compress(raw))
    return oid

def replace_tree(tree, parts, blob):
    entries = git("ls-tree", "-z", tree).split(b"\0")
    result = []
    found = False
    for entry in entries:
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        if name.decode() == parts[0]:
            found = True
            oid = (blob if len(parts) == 1 else
                   replace_tree(oid.decode(), parts[1:], blob)).encode()
        result.append(mode + b" " + name + b"\0" + bytes.fromhex(oid.decode()))
    assert found, parts
    return store("tree", b"".join(result))

def remove_lines(body, start, end):
    lines = body.splitlines(keepends=True)
    return "".join(lines[:start - 1] + lines[end:])

def drop_fixture(body, scenario):
    if scenario == "ignore_sweep_exit":
        function = next(n for n in ast.parse(body).body
                        if isinstance(n, ast.FunctionDef) and n.name == "selfcheck")
        rows = [n for n in ast.walk(function) if isinstance(n, ast.Tuple) and n.elts
                and isinstance(n.elts[0], ast.Constant)
                and n.elts[0].value in ("zero_summary_nonzero_exit", "sweep_zero_summary_nonzero_exit")]
        assert len(rows) == 1, "exit fixture must occur exactly once"
        row = rows[0]
        return remove_lines(body, row.lineno, row.end_lineno), str(row.elts[0].value)
    if scenario == "drop_right_boundary":
        start = "    # right-boundary arm:"
        end = "    # mutation-seat survivors"
        assert body.count(start) == body.count(end) == 1
        first, rest = body.split(start)
        removed, last = rest.split(end)
        assert 'cases.append(("suffix_trap"' in removed
        return first + end + last, "suffix_trap"
    nodes = [n for n in ast.walk(ast.parse(body)) if isinstance(n, ast.Expr)
             and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
             and n.value.func.id == "check" and n.value.args
             and isinstance(n.value.args[0], ast.Constant)
             and n.value.args[0].value == "pending substring is not a cell"]
    assert len(nodes) == 1, "substring fixture must occur exactly once"
    node = nodes[0]
    return remove_lines(body, node.lineno, node.end_lineno), "pending substring is not a cell"

print("BASE_REVISION=" + revision, flush=True)
print("HARNESS_SHA256=" + hashlib.sha256(Path(harness).read_bytes()).hexdigest(), flush=True)
failures = 0
for path, label in zip(paths[:3], ["ignore_sweep_exit", "drop_right_boundary", "pending_substring"]):
    body = (repo / path).read_text()
    changed, fixture = drop_fixture(body, label)
    assert changed != body
    ast.parse(changed)
    blob = store("blob", changed.encode())
    tree = replace_tree(git("rev-parse", revision + "^{tree}").decode().strip(), path.split("/"), blob)
    commit = store("commit", (f"tree {tree}\nparent {revision}\n"
        "author Regression simulator <regression@invalid> 0 +0000\n"
        "committer Regression simulator <regression@invalid> 0 +0000\n\n"
        f"Delete {fixture} only\n").encode())
    print(f"SCENARIO={label} deleted_fixture={fixture} path={path} revision={commit}", flush=True)
    command = ["python3", "-I", harness, commit, "--repo", str(repo), "--scratch", str(scratch)]
    print("$ " + shlex.join(command), flush=True)
    result = subprocess.run(command, cwd=repo, capture_output=True, text=True)
    print(result.stdout, end="", flush=True)
    print(result.stderr, end="", flush=True)
    print(f"rc={result.returncode}", flush=True)
    survived = [line for line in result.stdout.splitlines() if " survived " in line]
    summaries = [line for line in result.stdout.splitlines() if line.startswith("C1=")]
    good = (result.returncode == 1 and len(survived) == 1 and
            survived[0] == f"MUTANT {Path(path).name} {label} survived rc=0" and
            len(summaries) == 1 and summaries[0].startswith(
                "C1=unmet harness=present killed=10 survivors=1 total=11 pristine=green"))
    print(f"REGRESSION_{'PASS' if good else 'DEFECT'} {label}", flush=True)
    failures += not good
print(f"REGRESSION_SIM pass={3 - failures} fail={failures}", flush=True)
sys.exit(1 if failures else 0)
PY
