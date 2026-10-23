# RevC2Binding — C2 counter reads committed bytes at <rev>, not the working tree

Item attacked: claim C2 (`count-c2.py`) — is the counter self-referential? I.e., could it
pass on content that exists only in the working tree rather than committed at `<rev>`?

## Static read of `.ufo/waves/round-37/count-c2.py`

Every repo-content read goes through `show(repo, rev, rel)` (lines 102–112):

- `git -C <repo> cat-file -e <rev>:<path>` existence gate (line 104), then
- `git -C <repo> show <rev>:<path>` under `clean_env()` (lines 108–109) — `clean_env`
  strips `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_CONFIG_GLOBAL` (95–99).

Call sites of `show()`: `tool_text` (151, `tools/mori-source-drift.py`), `knowledge`
(187), `scorecard` (195), `readme`→`coverage_map` (202), `live` (208). All five corpus
checks consume `show()` output. The only `open()` calls in the counter (157, 167, 174)
are **writes** into `work = tempfile.mkdtemp(prefix="mori-c2-r37-")` (153): the pristine
tool copy, `cap-mutant.py`, `redirect-mutant.py`. `selftest()` (115–127) runs
`python3 <scratch-copy> --selftest` with `cwd=<mkdtemp dir>` — no lane path is passed.
The drift tool's `--selftest` builds its own fixture corpus under
`tempfile.mkdtemp` (tools/mori-source-drift.py:300,422) — it never touches the lane tree.

Docstring line 7–8: "Everything is read from committed bytes at <rev>
(`git show <rev>:<path>`)". Confirmed by inspection — no working-tree read exists.

## Commands and outputs

Run from `/home/vgpnk/Projects/shokunin/mori-shokunin`.

### 1. `python3 .ufo/waves/round-37/count-c2.py e57c58b5` (scored tip, ~14 s)

```
check tool_present   PASS (path=tools/mori-source-drift.py)
check selftest       PASS (exit=0 arms=[('exit_code', 'PASS'), ('huge_cap', 'PASS'), ('missing_sources_exit2', 'PASS'), ('redirect_private_refused', 'PASS'), ('row_states', 'PASS'), ('summary', 'PASS')])
check cap_kill       PASS (exit=1 huge_cap=FAIL)
check redirect_kill  PASS (exit=1 redirect_private_refused=FAIL)
check knowledge      PASS (present=True rows=['S205', 'S221', 'S222', 'S223', 'S224', 'S225'] cited_commit=True)
check capability     PASS (rows=1 names_tool=True)
check readme         PASS (r36_row=True r37_row=True)
check live           PASS (present=True sentence=True)
C2=met                                exit 0
```

### 2. `git -C <lane> show e57c58b5:corpus/README.md | head -2`

```
# mori-shokunin — corpus
```

Same committed bytes the `readme`/`coverage_map` check consumed.

### 3. `python3 .ufo/waves/round-37/count-c2.py 842a320` (entering tip, ~14 s)

```
check tool_present   PASS (path=tools/mori-source-drift.py)
check selftest       FAIL (exit=0 arms=[('exit_code', 'PASS'), ('missing_sources_exit2', 'PASS'), ('row_states', 'PASS'), ('summary', 'PASS')])
check cap_kill       FAIL (exit=1 huge_cap=None)
check redirect_kill  FAIL (exit=1 redirect_private_refused=None)
check knowledge      FAIL (present=False rows=[] cited_commit=False)
check capability     FAIL (rows=0 names_tool=False)
check readme         FAIL (r36_row=False r37_row=False)
check live           FAIL (present=False sentence=False)
C2=unmet                             exit 1
```

Matches the contract's do-nothing control exactly (only 4 unnamed arms at that rev).

### 4. Working-tree state (the non-self-referential proof)

`git rev-parse HEAD e57c58b5 842a320` → `c31076ed…`, `e57c58b5…`, `842a320…`.
`git status --porcelain`: `M .gitignore`, `M corpus/lessons/round-37.md`, `?? .scratch/`,
`?? .ufo/waves/round-37/w1/`.

```
-rw-r--r-- .ufo/waves/round-37/evidence/drift-live-r37.txt   (exists in worktree)
-rw-r--r-- corpus/knowledge/source-drift-hardening-r37.md    (exists in worktree)
-rwxr-xr-x tools/mori-source-drift.py                        (hardened copy in worktree)
```

HEAD is `c31076ed` — a commit *past* the scored tip — and the working tree carries every
r37 artifact. Yet run 3 against `842a320` reports `knowledge present=False`,
`live present=False`, `selftest` with only the four pre-hardening arms. If any check read
the working tree, `knowledge`, `capability`, `readme`, `live`, and the named selftest arms
would all have passed. They did not.

## Can the counter pass on working-tree-only content?

**No.** Every check is bound to `git show <rev>:<path>` output; the executable checks run
scratch copies under `mkdtemp`; the tool's selftest fabricates its own fixture corpus.
Run 3 is a live demonstration: all r37 content present in the working tree, `C2=unmet` at
the old rev.

## Residual risk / nits (not defects of the claim)

- `cat-file -e` (line 104) runs without `clean_env()`, so a hostile `GIT_DIR` could skew
  the existence probe. Effect is conservative only: `show` returns `None` → checks fail →
  `unmet`. Content itself always comes from `git show` under `clean_env`; no false-pass
  path, no working-tree read.
- Mutations use `str.replace` (all occurrences). If the tool gained a second
  `FETCH_MAX_BYTES =` literal, a partially-mutated copy would fail the kill check →
  `unmet`. Conservative direction again.
- `show()` decodes with `text=True`; a non-UTF-8 blob would raise and exit 2 (setup
  error), not silently pass.

Tool installs: none.

VERDICT: PASS
