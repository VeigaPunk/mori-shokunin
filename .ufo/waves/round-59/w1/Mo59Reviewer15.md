# Mo59Reviewer15 — Scratch/TMPDIR audit (round-59 w1)

Scope: verify no committed counter or tool writes outside `TMPDIR`/`--scratch`,
and that `--scratch` is accepted. Objects audited at their frozen bytes
(verified: working-tree sha256 == freeze-revision `60b3a76a` blobs for all five
files):

- `.ufo/waves/round-59/count-c1.py`  (`2be6fda8…0c9dfd`)
- `.ufo/waves/round-59/count-c2.py`  (`2df3ae84…877be`)
- `tools/mori-register-check.py`     (`38b733d8…472b8` = contract PIN)
- `tools/mori-settlement-scan.py`    (`4c04bf21…5ac9a9` = contract PIN)
- `contract.md`                      (`427fca0b…107e`)

## Verdict

**No counterexample on the claim-bound artifacts.** Both frozen counters and
both claimed tools write exclusively under `--scratch` or `TMPDIR`-rooted
`tempfile.mkdtemp` directories, and all four accept `--scratch`. Empirical
runs left zero files in system `/tmp` and zero writes in lane/fleet repos.

Two boundary observations (not counter-predicate defects, reported for
completeness): committed wave tool `build-w1-spec.py` writes
`.ufo/waves/round-59/w1-spec.json` directly in the lane (by design, pre-data
build product, already committed), and *importing* either counter as a module
drops `__pycache__/*.pyc` inside the lane tree (gitignored; seat item "import
count-c2.py" in `build-w1-spec.py:70` invites exactly this).

## Evidence — static

All write syscalls in the four audited files (grep: `/tmp|mkdtemp|tempfile|
write_text|write_bytes|mkdir|open(|scratch`):

| File | Write sites | Destination |
|---|---|---|
| count-c1.py | L86-87,104-106,141-144,175-180,193 | `scratch / …` only (`tool.py`, `st/`, `fx/<name>/`, `real/`, `real/_root/`) |
| count-c1.py | L258-260 | `tempfile.mkdtemp(dir=os.environ.get("TMPDIR") or None)` when `--scratch` absent |
| count-c2.py | L195-206,228-230,255-257,284-294,334-345 | `scratch / …` only (`tool2.py`, `real2/`, `root2/`, `trees/<name>/`) |
| count-c2.py | L392-425,446-448 | selftest `mkdtemp(TMPDIR)` + `shutil.rmtree` cleanup; `mkdtemp(TMPDIR)` fallback in `main` |
| mori-register-check.py | L209-216,240-248,285-287 | selftest-only writes under `scratch or mkdtemp(TMPDIR)`; verify mode (`check()`, L105-189) read-only — `read_text`/`is_file` only |
| mori-settlement-scan.py | L129-137,196-198 | selftest-only writes under `scratch or mkdtemp(TMPDIR)`; `scan()` L113-126 read-only |

Escapes checked and closed:

- **Subprocess cwd**: `run_tool` runs the tool with `cwd=str(scratch)`
  (count-c1.py L64-69); c2 scan/drift subprocesses inherit counter cwd but the
  tool writes nothing in scan mode anyway (only `--selftest` writes, always
  passed `--scratch` by the counters: c1 L112-115, c2 L210-213, both with
  `TMPDIR=scratch` in env).
- **Path traversal into `materialize`** (c1 L77-88) and tree materialization
  (c2 L336-345): all source paths come from `git ls-tree`/`git show` output or
  tool-emitted `pointers`. Git tree entries cannot contain `/` or `..`; the
  counter only materializes a pointer after `git cat-file -e rev:rel2` succeeds
  (L187-193) — `git show rev:<path>`/`cat-file` reject `..` and absolute
  pathspecs, so `root / rel` cannot escape scratch.
- **Tool pointer validation**: `pointer_ok` (mori-register-check.py L92-102)
  rejects empty, `/`-leading, `~`-leading, and `..`-segment tokens; file probes
  are `(Path(root) / rel).is_file()` (L185) — reads confined to `--root`.
- **`eval_entry` file reads** (c2 L139-160): `fb_path = root / cfile` is opened
  only when `cfile in ARTIFACTS` (L141, six whitelisted relative paths); a
  hostile `outside-file` claim is rejected as data, never opened.
- **Git invocations**: only `show`, `ls-tree`, `cat-file -e` — all read-only
  (c1 L53-61,124,145,189; c2 L90-97,320,336). No `checkout`/`write-tree`/
  `update-index`/`hash-object -w`.
- **`--scratch` accepted**: c1 L255-256, c2 L443-444, register-check L285-286,
  settlement-scan L196-197.

## Evidence — empirical (all under `TMPDIR=/fast/scratch/hyaku/mori-r59/Mo59Reviewer15/tmpdir*`)

```
$ python3 .ufo/waves/round-59/count-c1.py --selftest          → C1_SELFTEST pass=6 fail=0  rc=0
$ python3 .ufo/waves/round-59/count-c2.py --selftest          → C2_SELFTEST pass=9 fail=0  rc=0
$ python3 tools/mori-register-check.py --selftest --scratch … → REGCHECK_SELFTEST pass=12 fail=0  rc=0
$ python3 tools/mori-settlement-scan.py --selftest --scratch …→ SETSCAN_SELFTEST pass=10 fail=0 rc=0
```

Control (entering rev, `--scratch` given):
```
$ count-c1.py 2b9f0397… --scratch $S/sc-c1
C1=unmet … failed=tool_absent,selftest,fixtures_absent,real,pointers  rc=1
$ count-c2.py 2b9f0397… --scratch $S/sc-c2
C2=unmet … failed=copy_absent:…,drift,entry_absent,scan,selftest,tool_absent,tree,trees,trees_absent  rc=1
```

`TMPDIR`-only (no `--scratch`):
```
$ count-c1.py 2b9f0397…  → C1=unmet … failed=tool_absent,… rc=1
$ count-c2.py 2b9f0397…  → C2=unmet … failed=…,tool_absent,… rc=1
$ ls $S/tmpdir2 → mori-r59-c1-*/, mori-r59-c2-*/, mori-register-check-*/, mori-settlement-scan-*/   (4 dirs, all under TMPDIR)
$ ls /tmp | grep -c '^mori-r59'  → 0   (before and after all runs)
```

`--scratch` honored (HEAD): `count-c1.py HEAD --scratch $S/sc-c1h` →
`C1=met selftest=ok fixtures=ok real=ok pointers=ok` rc=0; all materialized
trees (`st/`, `fx/`, `real/`) under `$S/sc-c1h`, zero `mori-r59*` in `/tmp`.

## Minor findings (non-fatal, outside counter predicates)

1. **`build-w1-spec.py` writes `w1-spec.json` into the lane tree** (L158:
   `(W / 'w1-spec.json').write_text(...)`), not under scratch. Committed
   artifact `w1-spec.json` exists, so this was its intended product; it is a
   committed wave tool, hence technically inside this audit's letter. Impact:
   none on frozen claims — pre-data build, already landed.
2. **`.pyc` residue in lane**: `.ufo/waves/round-59/__pycache__/count-c{1,2}.
   cpython-314.pyc` present (untracked, `git check-ignore` → `.gitignore:3`).
   `count-c1.py --selftest` does **not** create one (verified: deleted, re-ran,
   not recreated — `spec_from_file_location` at L216 is dead code, module never
   exec'd). Source is module import — consistent with the dispatched seat item
   "run eval_entry-equivalent (count-c2.py internal — import it)"
   (`build-w1-spec.py:70`): CPython writes the bytecode cache beside the source
   unless `sys.dont_write_bytecode`/`PYTHONDONTWRITEBYTECODE` is set. Seats that
   import the counters should run with `PYTHONDONTWRITEBYTECODE=1` to keep the
   lane tree pristine.
3. **`--scratch` as last argv token**: counters read `argv[i+1]` unguarded
   (c1 L256, c2 L444) → `IndexError` traceback; both tools guard it
   (register-check L286, settlement-scan L197 fall back to `mkdtemp`). Cosmetic
   robustness delta only; frozen bytes are immutable anyway.

## Method bound

Audited files are pinned by sha256 to the freeze revision, so no other committed
artifact can silently substitute. Coverage: every `open`/`write_*`/`mkdir`/
`mkdtemp`/`tempfile`/`subprocess`/`git` call site in the four files
(enumerated above), every materialization path-join traced to a scratch-anchored
base, and three empirical runs (selftest ×4, entering-rev control ×2 with and
without `--scratch`, HEAD run ×2) with before/after `/tmp` and TMPDIR listing.
Not covered: behavior of non-committed callers (seat drivers), and Windows
path semantics (irrelevant — posix host).

Lane/fleet repos: zero writes observed (`git status` clean on audited paths;
all counter git calls read-only). Scratch used:
`/fast/scratch/hyaku/mori-r59/Mo59Reviewer15/` (cleaned after this report).
No installs/updates performed; no pacman. Disk guard green (592.6G free on
/fast/scratch/hyaku).
