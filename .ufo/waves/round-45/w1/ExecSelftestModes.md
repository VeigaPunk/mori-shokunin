# ExecSelftestModes — real `--selftest` argv branches for the three lane tools that had none

Wave: round 45 / w1. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Seat: executor (leaf; no dispatch). Contract read: `@W@/contract.md`, including
Correction 1 (C2 requires a "real `--selftest` argv branch", P-C2 item 4).

## What landed

Three files, each with an additive `--selftest` branch that exits before any
production work. No other file was edited; `SKILL.md`, `SCORECARD.md`, `LOG.md`,
`corpus/**`, `contract.md`, `tools/mori-routed-r24.py` and other seats' reports
were not touched.

| file | digest before | digest after | selftest tally (rc) |
|---|---|---|---|
| `tools/mori-silence-cases.sh` | `34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa` | `ff8b69757dea40e0a1aae4969acf633ee306269da100c594f6104e77809a4dcd` | `MORI_SILENCE_CASES_SELFTEST pass=24 fail=0` (rc 0) |
| `tools/mori-round19-regressions.py` | `0ccd17307c9ff21e26ac38c5e2734735a34c09bffb1499eb57bcb1bde993c652` | `3c2c77d4d400412c1b9b3be67e20840ed7af5bda90df168b5e47a98007b7781b` | `R19_SELFTEST pass=26 fail=0` (rc 0) |
| `tools/mori-routed-check.py` | `cd313053ed5305c444db2159e7a4793adad88a162cabf082b7d37773ea1bfdd7` | `b5498a54ceeb8429f262ea85dda2a740d0292c9458344a05d25ea6251ccffbf8` | `ROUTED_CHECK_SELFTEST pass=20 fail=0` (rc 0) |

All three selftests run in well under the 120 s bound (measured 1 s, <1 s, <1 s),
use no network, add no dependency (existing imports plus `shutil`/`tempfile`/
`pathlib` in the Python tools), and build fixtures only under the caller's
`$TMPDIR`.

### 1. `tools/mori-silence-cases.sh`

Before: `CENSUS=${1:-…}` consumed `--selftest` as the census path (so `--selftest`
died with "census not readable"). After:

- argv: `--selftest` is recognised first and shifted out; `--selftest <path>` is a
  usage error (exit 2, "`--selftest` takes no census path"); the original
  `usage: mori-silence-cases.sh [path-to-census]` string is preserved verbatim as
  the first usage line, with the selftest form appended on a second line.
- the pinned-entropy self re-exec (`exec bash "$SELF" "$CENSUS"`) now carries
  `--selftest` when selftest mode is active, so a pinned
  `MORI_SHUFFLE_SEED`/`MORI_RUN_NONCE` does not silently drop back into the suite.
- work dir: selftest mode uses `mktemp -d "$TMPDIR/mori-silence-cases-selftest.XXXXXX"`
  (absolute `TMPDIR` required, else `die` → exit 2); the production branch keeps
  the original `/tmp/mori-silence-cases.XXXXXX` verbatim. The existing `EXIT INT TERM`
  trap removes whichever tree was created.
- `st_main` runs 24 checks and exits 0/1 with the tally line; setup failures exit 2:
  1. table structure (4): table non-empty; ids unique; the `CASE_IDS` registry and
     the set of `case_*` functions are the same set (only `case_skeleton`, the
     shared tree builder, is excluded); every case fixture calls `new_case <own id>`
     (`shape-invariance` builds its own pair by design).
  2. final-roll grader (10): `verdict_grade` accepts CLEAN/rc0 and DRIFT/rc1, and
     rejects — with the documented reason class — a renamed roll (`BANANA`, the r11
     proxy), a duplicate roll, a malformed roll, a non-final roll, CLEAN/rc1,
     CLEAN with `drift>0`, DRIFT with `drift=0`, and CLEAN with the 2^64 drift wrap.
  3. parsing (5): `lane_state_from_out`, `aggregate_state_from_out`, `want_match`
     alternation (a listed alternative matches, an unlisted state does not), and
     `redact` of the run nonce.
  4. order channel (3): the shuffled order is identical for one seed, is a
     permutation of the registry, and is not the source order.
  5. the table's own fixtures end to end (2): `silent-open`, `completed-not-open`
     and `ledger-missing-not-silent` are executed through the real case functions
     and the real census; the check requires 3 runs, 3 passes, 0 failure-list growth.
     Their per-case stdout is captured to `$WORK/selftest-cases.log`; on failure only
     the `FAIL ` lines are echoed to stderr, so the tally line stays machine-readable.

Production behaviour: unchanged. Representative call
`MORI_SHUFFLE_SEED=20261025 MORI_RUN_NONCE=424242 bash tools/mori-silence-cases.sh`
→ rc 0, `MORI_SILENCE_CASES: matched=28 total=28`; stdout sha256
`d010fbc9ebaabdb8b4eb59bad6d1760af66d051e46858f0a6bde2ba145de2e0c` before **and**
after, stderr both empty (`e3b0c442…b855`), `cmp` clean on both streams.

### 2. `tools/mori-round19-regressions.py`

Before: no `--selftest`; argparse required the five flags.
After: `main()` dispatches `--selftest` (alone; any other argument is
"`R19_SELFTEST setup=--selftest-takes-no-other-arguments`", rc 2) to `run_selftest()`
before `parse_args`. Production parsing is unchanged (`parse_args(raw)` with
`raw = sys.argv[1:]`).

`run_selftest()` builds exactly the fixtures the `--mode after` path already builds
(`c2_fixture` inside `require_tmpdir()`, plus a C1 repo committed with
`c1_fixture_payloads()["blob_data"]` via the existing `init_repo`/`commit_files`) and
asserts 26 predicates over them — no production tool is dispatched, so it is
hermetic and offline:

- fixture commits and the `fixture-override` tag resolve to their recorded OIDs;
- register and corrections digests equal the bytes on disk and the recorded SHA-256s;
- claim rows are unique and bind the fixture's own base/tip for every claim
  (the `<synthetic override>` placeholder is checked through the tag);
- the per-claim frozen/implementation path presence matches the documented
  fixture shape (absent frozen for `fixture-absent`, absent implementation for
  `fixture-no-implementation`), with the absent-frozen case also asserted directly;
- the verdict table covers the claims and `fixture-coevolved` is `co-evolved` while
  its declared value is `pre-build` (the co-evolution the harness exists to catch);
- strict JSON: canonical round-trip, duplicate-key rejection, `NaN` rejection;
- `safe_repo_path` traversal/absolute/backslash rejection, `output_path` guards
  (relative, existing target, input overlap, fresh accept), `tool_path` digest,
  absence and directory rejection, `require_tmpdir` rejection when `TMPDIR` is
  unset or outside the lane;
- `counts()`, `process_receipt`/`parsed_stdout`, `marker_leaked`;
- C1 receipt fields: a well-formed receipt passes, a drifted population digest and
  an over-counted finding list are rejected, the finding-row lookup is
  path-sensitive, and both committed C1 blobs match their recorded digests;
- the pinned `.ufo/waves/round-19/frozen/expected.json` validates against
  `ORACLE_REVISION` and its bytes hash to the file digest.

Production behaviour: **raw stdout bytes of a successful run cannot be identical**
for this tool, by construction: the receipt records `inputs.harness_sha256 =
sha256(this file)`, and every fixture commit is stamped with the fixture's own
commit time, so the fixture OIDs and the digests derived from them differ between
any two runs — including two runs of the *unmodified* file. Measured, not assumed:

- pre-edit copy run twice (`p01` vs `p02`): differing paths = 33 (all fixture-OID
  derived: `c1` `inputs_sha256.population`/`expected_pin`/`process.stdout_sha256`,
  `c2.fixture_inputs_sha256.register`, `c2.processes.*.stdout_sha256`);
- pre-edit (`p01`) vs post-edit (`p03`): differing paths = 34, and the **only**
  edit-only path is `/inputs/harness_sha256` (`0ccd1730…` → `3c2c77d4…`, which are
  exactly the two file digests in the table above);
- masking the union of those 34 paths in both receipts yields the same bytes:
  `1770f808d414c1b7d058897dc8ea01a14d34973ca1c4f3d16c4b80a715d08a4c` for both;
- behaviour is identical: `status=pass`, `c1.counts {total 10, pass 10}`,
  `c2.counts {total 12, pass 12}`, `c2.supplemental_counts {total 4, pass 4}`, same
  check names and statuses;
- as a literal byte-identity witness on a production (non-selftest) invocation, the
  setup-error path (`--output relative-out.json`) is byte-identical before/after:
  sha256 `6456ff514edcf8ef6d8ba8b0a997b75afd06d22ad8cc3f6830603af555cd6274`, rc 2,
  `{"error_class":"output-path-must-be-absolute","mode":"after",…,"status":"setup-error"}`.

I did not weaken, reorder or re-word any production code path to buy that evidence;
the residual difference is inherent to the tool's own self-digest and fixture
timestamps, and the control run of the unmodified file proves it.

### 3. `tools/mori-routed-check.py`

Before: no `--selftest`. After: `main()` dispatches `--selftest` (alone; rc 2
otherwise) before argparse; `parse_args(raw)` is otherwise unchanged.

`run_selftest()` builds one isolated repo under `$TMPDIR` — a base commit carrying
the round-23 frozen/evidence/rejected trees, the two retention tools, the committed
dispatch-ledger stub, `SCORECARD.md` and a round-9745 wave spec + attempts ledger +
dispatch file; a benign tip commit; then one commit per mutant — and runs the tool's
own row predicates over it (20 checks):

- rows held on the clean fixture: R1, R2, R3, R4 (`held` with no reasons), R4
  reports `bound_before_call`, finds exactly one ledger and one spec, and R1 reports
  no historical-case hit;
- 13 mutants each rejected for the named reason: changed round-23 tree (R1 and R3),
  added quota path, quota capability present, historical case name under `tools/`,
  added privacy-clearance line, changed retention evidence, changed capture
  evidence, changed rejected tree, round without a ledger, dispatch committed after
  its `at`, invalid `at`, wave spec whose ledger never says `started`.

Fixture shape notes: all commits use a pinned `GIT_*_DATE` (2020-01-01), the R4
`at` values are 2099 / 2001 / non-timestamp, and the committed dispatch-ledger stub
is dispatched exactly as R4 dispatches the real tool (`python3 -I - verify …` on the
blob bytes), so R4's subprocess plumbing is exercised, not mocked out. The
historical-case needle is taken from the module constant `HISTORICAL_CASE_NEEDLE`,
so this file still does not contain the literal.

Production behaviour: unchanged. Representative call
`python3 -I tools/mori-routed-check.py --repo <lane> --rev 3ad8faaa… --round 24`
→ rc 0; stdout sha256 `854528f649f1ddff80260c9c246b6069cb4d77226f246b59bb3d865652092fb3`
before **and** after, stderr both empty, `cmp` clean (`{"held":4,"items":4,…}`).

## Able-to-fail evidence (each selftest fails on a mutant of itself)

Mutants were applied to **copies in scratch**; the shipped files were not modified.

```
-- silence-cases mutant: verdict_grade accepts CLEAN drift>0
FAIL selftest: verdict_grade accepts CLEAN with drift>0
FAIL selftest: verdict_grade accepts a wrapped CLEAN drift value
MORI_SILENCE_CASES_SELFTEST pass=22 fail=2
rc=1
-- round19 mutant: safe_repo_path accepts traversal
FAIL safe-repo-path-rejects-traversal
FAIL pinned-oracle-validates
R19_SELFTEST pass=24 fail=2
rc=1
-- routed-check mutant: 'round23_tree_changed' reason dropped
FAIL r1-rejects-changed-round23-tree
FAIL r3-rejects-changed-round23-tree
ROUTED_CHECK_SELFTEST pass=18 fail=2
rc=1
```

Setup paths (rc 2, no tally):

```
mori-silence-cases: --selftest requires an absolute TMPDIR        rc=2
mori-silence-cases: --selftest takes no census path               rc=2
R19_SELFTEST setup=explicit-lane-tmpdir-required                  rc=2
ROUTED_CHECK_SELFTEST setup=--selftest requires an absolute TMPDIR directory  rc=2
```

Cleanup: no `mori-*-selftest.*` / `mori-r19-selftest-*` / `mori-routed-selftest-*`
directory is left behind in `$TMPDIR` or `/tmp`.

## Evidence locations (retained)

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/ExecSelftestModes/`

- `before/` — pre-edit copies of all three tools, `before/silence.{out,err}`,
  `before/r19.{out,err}`, `before/routed.{out,err}`;
- `final/silence.*`, `final/routed.*` — post-edit production streams;
- `after/r19-p01.out` (pre-edit copy), `r19-p02.out` (pre-edit copy, second run),
  `r19-p03.out` (post-edit), `r19-err-before.out`/`r19-err-after.out`;
- `final-evidence.txt` — the full transcript of every command, digest and diff
  quoted above, in order;
- `mut/` — the three mutant copies plus the census copy they need;
- `before-sha256.txt` — the pre-edit digests.

## Risks / limits (stated, not hidden)

- `mori-silence-cases.sh` selftest executes three real cases against
  `mori-census.sh`, so it needs a readable census and real `git` (exit 2 otherwise,
  by design). It also mutates `RUN_SEED`/`CASE_IDS` in-process while checking the
  shuffle and restores both before exiting; it exits before the suite loop, so the
  production run order is unaffected.
- `mori-round19-regressions.py --selftest` deliberately does **not** dispatch the
  content/freeze tools; their behaviour stays under `--mode after`. Its
  `pinned-oracle-validates` check depends on the committed
  `round-19/frozen/expected.json` and the `ORACLE_REVISION` being present, exactly
  as the harness itself does (it also assumes the script sits at `tools/`, because
  `require_tmpdir()` and the oracle path derive the lane root from `__file__`).
- `mori-routed-check.py --selftest` requires an absolute `$TMPDIR` (rc 2 otherwise),
  matching the round-19 harness rule and the wave's "fixtures under `$TMPDIR` only".
- Production `mori-silence-cases.sh` still builds its suite fixtures in `/tmp`
  (hard-coded, unchanged); only the selftest branch honours `$TMPDIR`.
- No tool was installed or upgraded during this seat (nothing to record under the
  2026-10-19 tooling directive).

## Note for the L1 — registry rows (I cannot edit `SKILL.md`)

My edits do **not** touch any `SKILL.md` row, and they do not touch
`tools/mori-routed-r24.py` (residual seat `ExecSelftestRoutedR24` owns that file).
But three existing rows now understate their tool, and P-C2 wants superseding rows;
the stale one is unambiguous:

- `SKILL.md:646` — "routed round-23 items (r24, C1)": the self-test cell says
  "none built in; able-to-fail evidence is thirteen sandbox mutants in
  `.ufo/waves/round-24/w1/BuildRoutedCheck.md`". That is false as of this seat:
  `--selftest` is built in and itself contains 13 mutant rows.
- `SKILL.md:166` — "silence oracle": self-test cell "itself (hermetic case table,
  28 cases)" does not name the new flag.
- `SKILL.md:182` — "r19 finite regressions": self-test cell describes the
  before/after modes only.

Copy-paste replacement cells (L1 to land, per P-C2 item 2/6 — I am not editing
`SKILL.md`):

```
| routed round-23 items (r24, C1) | gate | `python3 -I tools/mori-routed-check.py --repo <repo> --rev <REV> [--round N]` · `python3 -I tools/mori-routed-check.py --selftest` | 0 clean (`held` == `items` == 4) · 1 failed (any routed row red; R4 includes ledgers that are unclean, unbound, missing for a wave spec, or whose `at` precedes the commit that last changed the dispatch file) · 2 could-not-evaluate (repo, revision or base unreadable, or no absolute TMPDIR for `--selftest`) | `--selftest`: 20 checks — the four rows held on a synthetic repo, then 13 mutant commits each rejected (round-23 tree, added quota path, quota capability, historical case name, privacy-clearance line, retention/capture evidence, rejected tree, missing ledger, dispatch-after-`at`, invalid `at`, unstarted wave), printing `ROUTED_CHECK_SELFTEST pass=<n> fail=<n>`; able-to-fail measured by dropping the `round23_tree_changed` reason (pass=18 fail=2 rc 1) | base `c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130` (fixed in the tool); `corpus/QUALITY.md` criteria 72-75 | read-only git object reads over the measured repo; runs the committed `tools/mori-dispatch-ledger.py` bytes as a subprocess; `--selftest` writes only under `$TMPDIR` | mori |
```

```
| silence oracle | gate | `bash tools/mori-silence-cases.sh` · `bash tools/mori-silence-cases.sh --selftest` | 0 clean (all matched) · 1 failed · 2 could-not-evaluate (incl. no absolute TMPDIR for `--selftest`) | `--selftest`: 24 checks over the case table — registry↔`case_*` bijection, per-id fixture naming, 10 `verdict_grade` fixtures (incl. the r11 `BANANA` proxy and the 2^64 CLEAN-drift wrap), lane/aggregate state parsing, `want_match` alternation, nonce redaction, seed determinism, then three cases run end to end against the real census; prints `MORI_SILENCE_CASES_SELFTEST pass=<n> fail=<n>` | case table in-script; `--selftest` fixtures under `$TMPDIR` | temp fixtures (suite: `/tmp`; selftest: `$TMPDIR`) | mori |
```

```
| r19 finite regressions | gate | `TMPDIR=<lane>/.scratch python3 tools/mori-round19-regressions.py --mode after …` · `TMPDIR=<lane>/.scratch python3 tools/mori-round19-regressions.py --selftest` | 0 all frozen synthetic requirements match · 1 mismatch or capability-absence red · 2 setup, pin, moving-input or no lane-local TMPDIR | `--selftest`: 26 checks over the same `--mode after` fixtures — commit/tag resolution, register+corrections digests, per-claim base/tip/path-presence binding, verdict mapping, strict JSON (dup-key/`NaN`), repo-path and output-path guards, C1 receipt fields and their mutants, pinned-oracle validation; prints `R19_SELFTEST pass=<n> fail=<n>`; no production tool is dispatched | Expected bytes must equal `5e393d20:.ufo/waves/round-19/frozen/expected.json`; extra binding refinements are separate | Explicit lane-local `TMPDIR` (selftest fixtures included); read-only reads of the pinned oracle | mori |
```

## Blockers

None. All three tools carry a real `--selftest` argv branch, all three tallies are
rc 0, and production behaviour is proven unchanged (literal bytes for two tools;
self-digest-only residual for the third, with the control run and the masked-byte
comparison above).
