# Mo54SentHostPaths — portability audit of the round-54 frozen files

Seat: Mo54SentHostPaths (leaf). Lane: mori-shokunin. Subject: `78295c764093ff1f6cee08d7246679900bde7265`
(the data commit), tracked file set under `.ufo/waves/round-54/` = 29 files (11 scripts+doc, 4 control/data
scripts, 12 evidence receipts/sweeps, 2 selftest receipts, 1 claims list per claim, 1 scope list, 1 census).
Read-only throughout: no write outside this report and `/fast/scratch/hyaku/mori-r54/Mo54SentHostPaths/` (removed
before finishing). No tool installed or upgraded.

## 1. The two mandated greps, at the pinned revision

Command (fleet-root cwd, `git -C /home/vgpnk/Projects/shokunin/mori-shokunin`):

```
git grep -n '/home/vgpnk' 78295c76 -- .ufo/waves/round-54/          # exit 0, 16 hits
git grep -nE 'mkdtemp\(dir="/tmp|/tmp/' 78295c76 -- .ufo/waves/round-54/   # exit 1, 0 hits
```

The second grep's exit 1 is the whole answer for the `/tmp` axis, and a wider one confirms it (no temp-file
creation of any kind in the frozen set):

```
$ git grep -nE 'mkdtemp|tempfile|NamedTemporary|TemporaryDirectory|TMPDIR|tempdir' 78295c76 -- .ufo/waves/round-54/
EXIT=1        (no output)
```

### 1.1 Classification of the 16 `/home/vgpnk` hits

| # | file:line | text | class |
|---|---|---|---|
| 1 | `evidence/census-start.txt:24` | `mori  ok  /home/vgpnk/.../mori-shokunin/corpus/SOURCES.md` | prose only — census tool output, path sits in the DATA column |
| 2-15 | `evidence/control-c1-*.txt:3`, `evidence/control-c2-*.txt:3` (14 files) | `command: python3 -B /home/vgpnk/.../count-c1.py --repo /fast/scratch/hyaku/mori-r54/l1/controls/<name> <rev>` | prose only (a receipt), but non-replayable — see F5 |
| 16 | `evidence/sweeps.txt:32` | `$ assimilation sweep: grep -rliE "…" /home/vgpnk/Projects/shokuknow/merge/mori \| wc -l` | prose only — recorded command line |

Zero hits in any `.py` file: no frozen script contains a `/home/vgpnk` default, a home-relative path, or an
`expanduser`/`$HOME` lookup. The only absolute-path default in the frozen scripts is a `/fast` path:

```
controls/controls.py:21:
SCRATCH = os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "mori-r54", "l1", "controls")
```

That is the single *executable* default in the round-54 set that is host-specific, and it honours
`HYAKU_SCRATCH` (verified in §3.1). No `/tmp` default exists to honour `TMPDIR`, and nothing reads `TMPDIR` at all:
`grep -n environ` over the five scripts returns exactly one line, `controls.py:21`.

## 2. Per-script portability verdict

| script | path resolution | cwd | env | locale | verdict |
|---|---|---|---|---|---|
| `count-c1.py` | `lane_root()` = 4× `dirname(abspath(__file__))` (`:398`); `--repo DIR` overrides (`:406-408`) | independent (ran from `/`) | independent (`env -i PATH=…`) | independent (explicit `.decode("utf-8","surrogateescape")`) | portable, with the layout precondition in F4 |
| `count-c2.py` | same 4× idiom (`:309`, `:318`; selftest `:340-341`); `--repo` (`:321`), `--entry` (`:323`) | independent | independent | independent | portable, same precondition |
| `controls/controls.py` | `HERE`/`WAVE`/`LANE` from `__file__` (`:17-19`); scratch from `HYAKU_SCRATCH` (`:21`) | independent | scratch root is env-driven; nothing else | **NO** — unencoded `open()` reads (F2) | partially portable |
| `controls/c1data.py` | `HERE` from `__file__` (`:15`); loads `../count-c1.py` via `spec_from_file_location` (`:16`); writes only under `argv[1]` | independent (ROOT is an argument) | independent | utf-8 pinned on every read/write (`:56,95,106,115`) | portable |
| `controls/c2data.py` | same idiom (`:13-14`); writes only under `argv[1]` | independent | independent | utf-8 pinned (`:50,64`) | portable |

Syntax floor: an AST scan of all five scripts finds no `JoinedStr`, `NamedExpr`, `Match` or builtin-generic
subscript — nothing above Python 3.5 was used. Observed interpreter: Python 3.14.8; no older interpreter is
installed on this host, so a low-version *run* is UNVERIFIED (the AST result is the evidence). Shebang is
`#!/usr/bin/env python3` and all five blobs are mode `100755`; the documented invocations call `python3` explicitly.

`git` surface used: `git -C <repo> rev-parse --verify <rev>^{commit}`, `show <rev>:<path>`, `ls-tree --name-only
<rev> <dir>` — all long-stable plumbing, always passed as an argument vector (no shell, so spaces/quotes in the
repo path are safe; verified in §3.2).

## 3. Executed evidence (scratch clone of the lane at `/fast/scratch/hyaku/mori-r54/Mo54SentHostPaths/lane`)

The clone is `git clone --shared --no-hardlinks` of the lane; its working-tree `count-c1.py` sha256 equals the
freeze manifest entry `e97a11986694b60f3a5d9d50b151553072f08a8a8d46cbea8f4b63a90dff433c`. Every command below
ran with `TMPDIR` pointed at the seat scratch and cwd `/` unless stated.

### 3.1 Path resolution of `controls.py` (module import only, nothing executed)

```
$ env -u HYAKU_SCRATCH python3 -B -c "…exec_module(controls)…"        exit=0
HERE= …/lane/.ufo/waves/round-54/controls
WAVE= …/lane/.ufo/waves/round-54
LANE= …/lane
SCRATCH= /fast/scratch/hyaku/mori-r54/l1/controls                  <- host default
EVID= …/lane/.ufo/waves/round-54/evidence

$ HYAKU_SCRATCH=/fast/scratch/hyaku/alt … same import                exit=0
SCRATCH= /fast/scratch/hyaku/alt/mori-r54/l1/controls              <- override honoured
LANE= …/Mo54SentHostPaths/lane                                     <- still __file__-relative
```

`LANE` followed the clone, so the clone's controls drove the clone's tree; the real lane was never the target.

### 3.2 Counter replay from a foreign cwd, foreign absolute path, and hostile argv

```
CWD=/ python3 -B <clone>/.ufo/waves/round-54/count-c1.py --repo <clone> 78295c76
C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok
  held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 rev=78295c76… failed=votes            exit=1
CWD=/ python3 -B <clone>/.ufo/waves/round-54/count-c2.py --repo <clone> 78295c76
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok
  entailed=0 dissent=0 rev=78295c76… failed=entailment                                        exit=1
```

These are byte-identical to `evidence/c1-at-data.txt` and `evidence/c2-at-data.txt` (which were produced with a
*relative* script path from the lane root). Same result with no `--repo` (script inside the clone), with a
relative `--repo .` from the clone root, with `env -i PATH=/usr/local/bin:/usr/bin:/bin`, with
`LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0`, and with `--repo "<clone> link"` (a symlink whose name contains a
space) — all exit 1 with the same counter line. A repo path with a space is not a quoting hazard.

Graceful failures (no traceback, setup exit 2):

```
--repo <dir that is not a git repo>   -> C1_SETUP unresolvable revision … / C2_SETUP unresolvable revision …  exit=2
env PATH=/nonexistent (no git)        -> C1_SETUP unresolvable revision … / C2_SETUP unresolvable revision …  exit=2
relocated fake layout, --scope        -> scope=0                                                              exit=2
```

### 3.3 Selftests reproduce the frozen receipts

```
CWD=/ python3 -B <clone>/.ufo/waves/round-54/count-c1.py --selftest  -> 58 lines, C1_SELFTEST pass=57 fail=0, exit=0
CWD=/ python3 -B <clone>/.ufo/waves/round-54/count-c2.py --selftest  -> 55 lines, C2_SELFTEST pass=54 fail=0, exit=0
```

`diff` against `evidence/selftest-c1.txt` / `selftest-c2.txt` differs by one trailing `exit=0` line that the
receipt carries and the counter does not. (An early 33-line view of the c1 output was a display truncation of the
harness; the piped, counted run is the one cited.)

### 3.4 The whole control battery, off the lane, under a foreign scratch root

```
cd <seat>; HYAKU_SCRATCH=<seat>/hyaku python3 -B lane/.ufo/waves/round-54/controls/controls.py   exit=0 (28.8s)
```

All 14 controls scored; every counter line matches the frozen receipt field-for-field once `rev=` is elided
(`MATCH` for all 14 of `control-c1-*.txt`, `control-c2-*.txt`). The final `shutil.rmtree(SCRATCH)` removed the
clone tree (`du` = 0, directory gone). Re-run under `LC_ALL=C` (UTF-8 mode still auto-enabled on 3.14): exit 0,
all 14 still match. The lane's own receipts were never touched — `sha256sum -c` of the 14 receipts and 2 selftest
receipts against `evidence/freeze-sha256.txt` prints `OK` for all 16.

### 3.5 Where it breaks: a non-UTF-8 default encoding

```
env -i PATH=/usr/local/bin:/usr/bin:/bin LC_ALL=C LANG=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 \
    HYAKU_SCRATCH=<seat>/hyaku3 python3 -B lane/.ufo/waves/round-54/controls/controls.py      exit=1
  … controls.py:109 in run_c1 -> c1_votes(d, c1)
  … controls.py:91  open(os.path.join(d, c1.LEDGER)).read()
  UnicodeDecodeError: 'ascii' codec can't decode byte 0xe2 in position 172: ordinal not in range(128)
```

Byte 172 of the generated ledger is the first byte of the em dash in the line
`recheck: on-release — \`python3 .ufo/waves/round-54/count-c1.py <rev>\``, which `c1data.py:111` writes with
`encoding="utf-8"` (`:115`) while `controls.py` reads the same file with the locale default. Re-running the same
failing command with the receipt hashes snapshotted first changed exactly two evidence files before the abort:

```
lane/.ufo/waves/round-54/evidence/control-c1-copies-only.txt: FAILED
lane/.ufo/waves/round-54/evidence/control-c1-do-nothing.txt: FAILED
```

(the two controls scored before the witness stage, in code order `controls.py:104,106,109`). The `finally`
cleanup still removed the scratch tree.

### 3.6 Relocating the script alone

```
<seat>/fake/.ufo/waves/round-54/count-c1.py --scope     -> scope=0  exit=2            (clean)
<seat>/fake/.ufo/waves/round-54/count-c1.py --selftest  -> FileNotFoundError: …/fake/corpus/evidence/sources-r54/
                                                           memcontrol.c.v7.3   exit=1  (traceback, not C1_SETUP)
```

### 3.7 Byte-code side effect of the data appliers

`c1data.py:16` / `c2data.py:14` load the frozen counters through `SourceFileLoader`, which writes a `.pyc` unless
`-B`/`sys.dont_write_bytecode` is set. Running `python3 lane/…/controls/c2data.py` (no args, no `-B`) created
`lane/.ufo/waves/round-54/__pycache__/count-c2.cpython-314.pyc`; the real lane already carries
`__pycache__/count-c1.cpython-314.pyc` and `count-c2.cpython-314.pyc` from the same mechanism. The directory is
ignored (`.gitignore:3: __pycache__/`), is not in `git ls-tree 78295c76 -- .ufo/waves/round-54/__pycache__`
(empty), and is not in the freeze manifest, so frozen bytes are unaffected; it is untracked state in the lane.

## 4. Related items outside the frozen script set (scope note)

- `.ufo/waves/round-54/build-w1-spec.py`, `checks/receipt-stage.py`, `w1-dispatch.json`, `w1-spec.json` are
  untracked at `78295c76` and therefore outside this audit's pinned set. A working-tree scan for `/tmp/` finds
  only prose there (the seat prompt text) and one sibling seat report (`w1/Mo54ScribeMistakes.md:28-30`) that
  documents `> /tmp/s` / `> /tmp/l` in a round-53 comparison command — prose in another seat's report, not an
  executable default of the round-54 tooling, and outside my write scope.
- `/fast/scratch/hyaku/mori-r54/l1/controls` (the `--repo` targets named by the 14 receipts) no longer exists:
  `ls` exit 2. The receipts record a run that cannot be replayed from the receipt text.

## 5. Limits of this audit

- Interpreters other than Python 3.14.8 and git other than 2.56.0 are UNVERIFIED; the version-floor claim rests on
  the AST scan, not a run.
- No ISO-8859/latin-1 locale is installed (`locale -a | grep -ciE 'iso-8859|latin'` = 0), so the non-UTF-8 failure
  was produced with `LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0`; a genuine latin-1 default is the same code
  path but was not observed directly.
- Windows/macOS behaviour is out of scope (POSIX shebang, `git -C`, `--shared` clone); only the lane's Linux host
  was exercised.
- The battery replay scored the counters; it did not re-fetch the v7.3 copies, so "portable" here means the
  scripts resolve inputs and produce the same verdict, not that the upstream bytes still match (other seats hold
  the pin re-fetch).
- I did not run `controls.py` against `/home/vgpnk/Projects/shokunin/mori-shokunin` itself: by construction it
  writes into the lane's `evidence/` (F1), which would have mutated frozen receipts.

## Findings

- **MED — `controls/controls.py:40-41,72-73,251`**: the control runner always writes its 14 receipts into the
  lane's `evidence/` directory (`open(..., "w")` over files listed in `freeze-sha256.txt`) and has no
  `--out`/`--dry-run`. Replay inside *any* lane checkout (off-host re-execution, ci, a reviewer's tree) rewrites
  frozen bytes with new absolute paths and revs, and a mid-run failure leaves the set partially rewritten — the
  locale abort rewrote exactly `control-c1-do-nothing.txt` and `control-c1-copies-only.txt` before exit 1. My
  replay against the clone confirms the overwrite semantics (only the `command:` line differs from the frozen
  receipt). Impact: contorts the "frozen file is never edited in place" rule for the seat that replays, and the
  receipt set can end up half-old/half-new with no marker.
- **MED — `controls/controls.py:91,127,135,174,237`** (writer `controls/c1data.py:111`): text I/O without
  `encoding=`, against a file the sibling applier writes as UTF-8. Under a non-UTF-8 default encoding
  (`LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0`) `controls.py` aborts at the witness stage with
  `UnicodeDecodeError … byte 0xe2 in position 172` on the ledger's `recheck: on-release — …` line. Impact: the
  control battery is not re-runnable in a C/ASCII-default CI environment; the five sites should pin
  `encoding="utf-8"` (or `errors="surrogateescape"`) exactly as the counters and appliers already do.
- **LOW — `controls/controls.py:21`**: `/fast/scratch/hyaku` is a host-specific default; it honours
  `HYAKU_SCRATCH` (verified: override produced `<HYAKU_SCRATCH>/mori-r54/l1/controls`), so off-host replay works
  only if the variable is set, and the default is otherwise an executable absolute path with no fallback to
  `TMPDIR`. Also `:251` `shutil.rmtree(os.environ-derived SCRATCH)` has no containment check on the env value.
- **LOW — `count-c1.py:398,437-440` / `count-c2.py:340-344`**: `--selftest` resolves its corpus from
  `__file__` + 4 levels and fails with a bare `FileNotFoundError` traceback (exit 1) when the script is copied
  away from its corpus, instead of the `C1_SETUP`/`C2_SETUP` exit 2 the same scripts use for every other setup
  fault. Path resolution itself is sound: no absolute default, `--repo` overrides, and the normal mode works from
  any cwd, any absolute location, a minimal env and a hostile locale.
- **LOW — `evidence/control-c1-*.txt:3` (14 files), `evidence/census-start.txt:24`, `evidence/sweeps.txt:32`**:
  absolute `/home/vgpnk` and `/fast` paths appear only in prose/receipt text — never in an executable default — so
  they cannot break a run, but the 14 `command:` lines name a `--repo` clone that the runner deletes
  (`/fast/scratch/hyaku/mori-r54/l1/controls` no longer exists, `ls` exit 2), making the recorded command
  non-replayable as written. The replayable form is the `HYAKU_SCRATCH=<dir> … controls.py` invocation, which no
  receipt records.
- **LOW — `contract.md` "Counting command" and the ledger `recheck:` line (`controls/c1data.py:111`)**: the
  documented form `python3 .ufo/waves/round-54/count-c1.py R` is cwd-relative (lane root), while the cwd-free form
  exists only in the counter's usage line (`count-c1.py:31`, `count-c2.py:25`; `--repo` at `:406`, `:320`). An
  operator replaying from another directory must know the flag, which the contract does not name.
- **LOW — `controls/c1data.py:16`, `controls/c2data.py:14`**: `spec_from_file_location` + `exec_module` writes
  `__pycache__/*.pyc` next to the frozen counters whenever the appliers run without `-B`; the lane already carries
  those two `.pyc` files (gitignored, not tracked, not in the freeze manifest). Untracked state only, but it means
  "run the data applier" has a write side effect in the frozen directory's parent.
- **INFO — positive**: `count-c1.py` and `count-c2.py` are portable in the audit's sense — no absolute or home
  default, `__file__`-relative lane root with `--repo` override, cwd-independent, env-independent, locale-independent
  (explicit UTF-8 decode with `surrogateescape`), argument-vector `git` calls that tolerate spaces, and clean
  exit-2 setup failures; both reproduce `c1-at-data.txt`/`c2-at-data.txt` and `selftest-c1.txt`/`selftest-c2.txt`
  from a relocated clone, and the 14-control battery reproduces every frozen receipt field with exit 0.
- **INFO — positive**: the round-54 frozen set contains no `/tmp`, `mkdtemp`, `tempfile` or `TMPDIR` reference
  (two greps, both exit 1); the only environment variable any script reads is `HYAKU_SCRATCH`, and only via a
  default that can be overridden.
