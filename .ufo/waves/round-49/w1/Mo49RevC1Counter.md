# Mo49RevC1Counter — line-by-line review of `count-c1.py` (round 49, w1)

Seat: Mo49RevC1Counter, reviewer (leaf; no subagents dispatched). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Target: `.ufo/waves/round-49/count-c1.py`, frozen at `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`
(entering tip `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`). Date of this report: 2026-10-25, after both revisions.
Scratch used: `.scratch/r49-Mo49RevC1Counter/`. No lane file edited; lane `HEAD` and index unchanged (checked before/after:
`git rev-parse HEAD` = `0df17b7b…`, `git diff --cached --stat` empty).

No tool chain was needed or installed for this seat (host python 3.14 + git only); nothing was installed or upgraded.

## Summary

The counter's scoring logic is sound: for the 27 runs it plans, a tool can reach `C1=met` only by returning the right
`met`/`unmet` for all 18 junk edits and all 7 honest edits plus the two reads of R's own `SKILL.md`; every failure
direction I could construct (ignore `--skill`, read the working tree, literal name-sniffing, crash, timeout, exit-code
disagreement) lands on `unmet`, never on `met`. I found **no defect that makes the committed receipt line wrong about the
tool's behaviour**.

**But the predicate does not establish what the claim says it does.** I wrote two stub tools that score the exact target
line — `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26` — while implementing no pin rule at all: one
inverts the content-hash filename (`sha256(rev, body)` is recomputable from the committed counter), the other ranks the
staged copies by `mtime` in the shared scratch directory (§11, F22/F23). The counter's own sniffer arm cannot see either.
So `C1=met` cannot distinguish a reconciler that reads what a reader sees from a lookup table, which is the calibration
property C1 claims.

I also found **one divergence between the frozen predicate sentence and what the counter actually runs** (F1: N10/H5 are
scored with `--min-tally-pins 1` and the fixture's own baseline, not `26`/`2d85e33d`, and at `26` the honest control
H5 reads `unmet` — so P-C1 as written is unsatisfiable), one **landing-critical coupling** the receipt does not show
(F2: the reconciler row's `PIN_CHECK_SELFTEST pass=60` is re-executed *inside the exported revision*, so the landed
tool's own arm count must be pinned in the same commit or `real` fails), and a set of selftest-coverage and
hygiene defects (F3–F21), five of which I demonstrate by mutation surviving the full 44-arm selftest.

## 1. Identity and freeze bytes

```
$ sha256sum .ufo/waves/round-49/count-c1.py
3c262a15ae28adffa63f6646d5ec15498d1a4c735dbc3c38f68af16afc616b6d  .ufo/waves/round-49/count-c1.py
```
Matches `.ufo/waves/round-49/evidence/freeze-sha256.txt` line 2 exactly, so I reviewed the frozen bytes (463 lines).
`git diff --stat b3e3453d 0df17b7b -- SKILL.md` is empty: R's `SKILL.md` is byte-identical at the entering tip and at
the freeze commit, so the selftest (which reads `master`'s `SKILL.md`) and the receipts (which name `b3e3453d`) score
the same text. The `rev=` recorded in every receipt is the resolved commit id (`main` L324-330 resolves
`<rev>^{commit}` before any run), which is correct.

## 2. Selftest reproduction

```
$ TMPDIR=…/.scratch/r49-Mo49RevC1Counter python3 .ufo/waves/round-49/count-c1.py --selftest
… C1_SELFTEST pass=44 fail=0        (exit 0)
```
Identical to `evidence/selftest-c1.txt` (`pass=44 fail=0`), so the frozen bytes reproduce the frozen receipt.

## 3. Do the variant edits do what the docstring says?

I applied every edit function to `git show b3e3453d:SKILL.md` (155 067 bytes, 979 lines) and diffed. All nine new junk
edits and both new honest edits match their docstring lines (L20-32) exactly:

| variant | observed diff against R | matches docstring |
|---|---|---|
| N1 | 1 line appended: `<!-- \| r49 html comment \| gate \| … \| PIN_CHECK_SELFTEST pass=999 fail=0 \| …` after a blank line | yes (gate row in an HTML comment) |
| N2 | new table whose header reads `self test` with U+00A0 and whose self-test cell is `` `PIN_CHECK_\u200bSELFTEST pass=999 fail=0` `` | yes (NBSP header + ZWSP in the token) |
| N3 | fenced block containing a tab-indented pipe row, pin `pass=999` | yes |
| N4 | 4-space-indented pipe row, no fence, pin `pass=999` | yes |
| N5 | second row for `python3 tools/mori-pin-check.py --rev <rev>` whose verdict map says `1 → PIN_CHECK_SETUP`, pin `pass=60` (the live tally) | yes (contradicting exit contract) |
| N6 | pin-less row + prose `pass=60 fail=0`, then a continuation line `PIN_CHECK_SELFTEST pass=60` / `fail=3` | yes |
| N7 | `<table><tr><td>…` with `<code>PIN_CHECK_SELFTEST pass=999 fail=0</code>` | yes |
| N8 | re-points the single reconciler row's self-test cell to `mori-unlanded-check.py --selftest` and pins `UNLANDED_SELFTEST pass=13 fail=0` (the value `_cur_pin` reads from R) | yes (entry names the reconciler, self-test runs the unlanded check) |
| N9 | new row whose entry cell is `tools/mori-gate-registry.py … --audit`, self-test cell runs `mori-pin-check.py --selftest` and pins `pass=60` | yes (misattributed tally) |
| H6 | HTML comment + HTML table, no pin token | yes |
| H7 | 4-space pipe row + fenced tab-indented row, no pin token | yes |

Parseability by the entering v3 tool is demonstrated by `evidence/control-c1-tool-v3-entering.txt`: all 27 runs return a
clean `met`/`unmet` with `rc=0/1` and `errors=0` — no `PIN_CHECK_SETUP`, so v3 parsed every edited file. I also sampled
detection *reasons* with the committed witness on a lane-repo probe (3 of 12 runs completed before the 900 s clamp) and on
a shadow copy:

| variant | finding line (verbatim, truncated) | class as documented |
|---|---|---|
| N1 | `pin line=981 kind=row state=hidden row='<!-- \| r49 html comment \| gate \| `python3 tools/mori-pin-check.py --rev <rev>` \|'` | gate row inside an HTML comment ✓ |
| N3 | `pin line=982 kind=row state=hidden row='\t\| r49 tab fence \| gate \| …'` | tab-indented pipe row in a fence ✓ |
| N2 | `pin line=… kind=span state=unparsed reason=non-ascii-token` (shadow run, same bytes) | NBSP/ZWSP token ✓ |
| N9 | `pin line=… kind=tally prefix=PIN_CHECK_SELFTEST state=misattribut…` (shadow run) | misattributed tally ✓ |

The reasons for N4-N8, N10, H5-H7 are **not observable from any receipt** (F4).

## 4. `plan()` — opaque names, ordering, fixture flags

- Names: staged copy `s-<sha256(rev,body)[:12]>.md`, run scratch `t-<same tag>`, fixture repo `w-<sha256("fixture",
  str(move_pin), dest)[:12]>`, commit messages `c`/`c`. No variant name reaches the tool: verified by mutation K05
  (naming the copy by `name` fails `handles_carry_no_variant_name`) and by direct inspection of a fixture
  (`w-e44d43dc4b5c`, `w-665e8fbb606d`, log `['c','c']`).
- Ordering: `jobs.sort(key=basename(tmpdir))` (L275) orders the *submission* list by hash. Under `--jobs > 1` the actual
  execution order is whatever thread scheduling gives (`as_completed`, L289), so "run order follows that hash" in the
  contract is true of submission only. No observable consequence for the tool (each run has its own tmpdir).
- **Fixture flags diverge from the frozen sentence.** L265-267 appends the two fixture jobs with
  `(base, 1)`: `--min-tally-pins 1 --baseline-rev <fixture c0>`. P-C1's trailing clause says "every run with
  `--min-tally-pins 26 --baseline-rev 2d85e33d…`", and the module docstring L10 repeats it. I built the fixture and ran
  the committed witness and the entering v3 against it:

  | tool | `--min-tally-pins` | N10 (stale pin) | H5 (moved pin) |
  |---|---|---|---|
  | `controls/tool-r48-merged-witness.py` | 1 | `PIN_CHECK=unmet rc=1` | `PIN_CHECK=met rc=0` |
  | `controls/tool-r48-merged-witness.py` | 26 | `PIN_CHECK=unmet rc=1` | **`PIN_CHECK=unmet rc=1`** |
  | `controls/tool-v3-entering.py` | 1 / 26 | `unmet` / `unmet` | `met` / `unmet` |

  So with the frozen flags the honest control H5 is red for every tool (the fixture has one tally pin, below a floor of
  26), i.e. `C1=met` is unreachable under P-C1's literal sentence. The receipt line does not print per-run flags, so the
  divergence is invisible in `evidence/control-c1-tool-r48-merged-witness.txt`.

## 5. `run_tool()` (L224-246)

Behaviour matches its contract; probed directly with six one-line fake tools:

| fake tool | returned |
|---|---|
| prints `PIN_CHECK=met`, exit 0 | `('met', 0)` |
| prints `PIN_CHECK=met`, exit 1 | `('error', 1)` |
| prints `PIN_CHECK=unmet`, exit 0 | `('error', 0)` |
| prints `PIN_CHECK_SETUP`, exit 2 | `('error', 2)` |
| prints `unmet` then `met`, exit 0 | `('met', 0)` (last line wins — intended: the tool prints one line per finding, then the verdict) |
| `raise SystemExit("boom")` | `('error', 1)` |

`-I -B` (L225) makes the invocation stricter than the registry's documented `python3 tools/mori-pin-check.py --rev R`:
`-I` implies `-P`, so a future tool that imported a sibling module from `tools/` would fail here with `error` although
its documented command works (F13). `env` is the caller's environment plus `TMPDIR`/`PYTHONDONTWRITEBYTECODE`; an
exported `GIT_DIR`/`GIT_WORK_TREE` in a reviewer's shell would reach the tool (minor).

The **rc/agreement block (L241-244) is load-bearing and untested**: removing it (mutation K19) leaves 44/44 PASS. A tool
that prints `PIN_CHECK=unmet` but exits 0 would then be scored as correctly rejecting junk, i.e. a swallowed exit code
— exactly the CI contract the row advertises — would pass C1.

## 6. `verdict()` (L298-307)

Counters are correct as defined: `junk_met` = junk rows not `unmet`; `honest_unmet` = honest rows (all but `real`) not
`met`, which correctly includes `real-opaque`; `real` is separate; `met` requires all four conditions. Two notes:

- **No inventory check.** `variants` is `len(results) - 1` (L305) and `met` never compares the row set with `ORDER`.
  Feeding a truncated result set reproduces the target line with a smaller count and `met=True`:

  ```
  rows=27 -> C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=0df17b7b…
  minus N9 -> C1=met … variants=25   (met: True)
  minus N9,N8,N7,H7 -> C1=met … variants=22   (met: True)
  ```
  So a future edit that drops a variant from `NEW_VARIANTS` still exits 0; the only guard is the literal
  `variants=26` in the contract, and the selftest's count arm is derived from the same tuple, so it moves with the drop.
- `errors == 0` (L303) is **dead**: an `error` on a junk row already increments `junk_met`, on an honest row
  `honest_unmet`, on `real` sets `real="error"`. Removing the conjunct (K10) leaves 44/44 PASS, and so does
  `verdict_error_unmet`, which is satisfied by `junk_met` rather than by the error count. Cosmetic in the line, but it
  means `junk_met` double-counts errors: with a non-existent `--tool` the line reads
  `C1=unmet junk_met=18 honest_unmet=8 real=error errors=27` (F11).

## 7. The clone helper — can it ever touch the lane?

`fixture_variant()` (L174-201): `os.makedirs(d/tools)` (no `exist_ok`), `git -C d init -q`, a one-time
`git -C d rev-parse --show-toplevel` compared with `realpath(d)` (L182-184), then two commits with `-c user.name=c1
-c user.email=c1@example.invalid` passed per invocation (never written to any config).

- **Isolation check is sound and fails closed.** Mutating the `init` to target the parent (K17) makes the guard fire
  (`r48c1.Anchor: fixture is not its own repository`); in the real path that Anchor is caught at L268-269 and becomes
  `C1_SETUP` (exit 2). A poisoned `GIT_DIR` environment would also make `rev-parse` return the outer repo and trip the
  guard before any commit. `git add -A`/`commit` run with `-C d`, so they cannot reach the lane's index: I re-checked
  `git -C lane diff --cached --stat` (empty) and `HEAD` (unchanged) after all my fixtures.
- **But the fixture is created *inside the lane* by default.** `main` L332 defaults `--scratch` to
  `tempfile.mkdtemp(prefix="c1-", dir=<repo>/.scratch)`, and the fixture dir is `scratch/w-<hash>`. My sanctioned scratch
  (also inside the lane) shows the resulting shape:

  ```
  .scratch/r49-Mo49RevC1Counter/fixt/w-e44d43dc4b5c/.git -> toplevel …/fixt/w-e44d43dc4b5c
  .scratch/r49-Mo49RevC1Counter/fixt/w-665e8fbb606d/.git -> toplevel …/fixt/w-665e8fbb606d
  ```
  `.scratch` is **not** gitignored at the freeze (`git check-ignore -v .scratch` → no output; `git status` lists
  `?? .scratch/…`). A nested repository at 160 000 becomes a gitlink on the next `git add -A`; proved in a throwaway
  repo (`D`): `warning: adding embedded git repository: .scratch/w-abc`, then
  `160000 398b16c3… 0  .scratch/w-abc`. Lane `.scratch` is 26 G with 199 entries today. The counter never cleans up
  (`shutil.rmtree` appears only inside the selftest, L381/L398/L425).
- `--scratch` is **not reusable**: `plan()` builds `<scratch>/w-<hash("fixture", move_pin, scratch)>`, so a second run
  against the same directory dies:

  ```
  first : jobs=27
  second: ERR fixture variant: [Errno 17] File exists: …/reuse-hzxh6iqh/w-c4cd6317b9c4/tools
  ```
  → `C1_SETUP` (exit 2) with a message that reads like a variant failure (F8).

Also worth recording: the tool under test does **not** confine itself to `--scratch`. `tools/mori-pin-check.py`
L649-652 does `scratch_parent = os.path.join(repo, ".scratch"); makedirs; mkdtemp(prefix="pin-check-")` before any
revision is resolved. Running the committed witness against a fixture repo created `.scratch` *inside that repo*
(observed: `['.git', '.scratch', 'SKILL.md', 'tools']` after the run, with `TMPDIR` pointing elsewhere). Lane runs
therefore write `lane/.scratch/pin-check-*`: 73 such directories existed when I started a 12-run probe and 87 existed
when it ended, with concurrent seats also running the same tool, so the rate is one directory per invocation (~90 s per
invocation at the freeze). The module docstring L38-40 ("the lane repo is only read") is false as observed (F7).

## 8. Exit codes (L319-343)

| invocation | exit | observed |
|---|---|---|
| `--selftest` (all pass) | 0 | `C1_SELFTEST pass=44 fail=0` |
| `--tool` = entering v3 at R | 1 | `C1=unmet junk_met=9 …` (receipt) |
| `--rev deadbeef` | 2 | `C1_SETUP unresolvable revision deadbeef` |
| stray positional arg | 2 | `C1_SETUP usage: …` |
| `--tool` with no value | **1** | `IndexError: list index out of range` (traceback, L318) |
| `--jobs 0` | **1** | `ValueError: max_workers must be greater than 0` (L334→L286) |
| `--tool …/nope.py` (typo/absent) | **1** | `C1=unmet junk_met=18 honest_unmet=8 real=error errors=27`, 0.25 s |

The last row matters for the kill rule: a mistyped tool path, or a tool that fails to import, produces `C1=unmet`
(exit 1) rather than `C1_SETUP` (exit 2). There is no `os.path.isfile`/executable check on `--tool` (F6).

## 9. Kill-arm battery

I could not mutate the frozen file, so I built a shadow lane (throwaway git repo `D=$(mktemp -d)`, `git -C "$D" init
-q`, toplevel verified equal to `$D` before the first commit, `SKILL.md` = `git show b3e3453d:SKILL.md`, round-48 and
round-49 counters copied in) and mutated one line at a time in `D/.ufo/waves/round-49/count-c1.py`, running
`--selftest` after each. Baseline in the shadow: `C1_SELFTEST pass=44 fail=0`. All 20 mutations are anchored exactly
once in the frozen source.

| # | mutation (guarded line) | result |
|---|---|---|
| K01 | `_append` returns `text` unchanged | FAIL: apply_N1,N2,N3,N4,N5,N6,N7,N9,H6,H7,variants_pairwise_distinct |
| K02 | `v_h7` returns H6's body (duplicate) | FAIL: variants_pairwise_distinct |
| K03 | `plan_text_only` stages an empty variant list | FAIL: order_not_expect_sorted, filename_sniffer_not_met |
| K04 | **`plan()` stage path uses `name` instead of the hash tag** | **SURVIVED: 44/44** |
| K05 | `plan_text_only` stage path uses `name` | FAIL: handles_carry_no_variant_name |
| K06 | **drop `plan_text_only`'s hash sort (L448)** | **SURVIVED: 44/44** |
| K07 | `junk_met` counts correct rejections | FAIL: verdict_all_good_met, verdict_junk_green_unmet, verdict_line_shape, filename_sniffer_not_met |
| K08 | `honest_unmet` counts correct accepts | FAIL: verdict_all_good_met, verdict_line_shape |
| K09 | drop `real == "met"` from `met` | FAIL: verdict_real_red_unmet |
| K10 | **drop `errors == 0` from `met`** | **SURVIVED: 44/44** |
| K11 | `line` format changed (`"C1=%s  junk_met=%d`) | FAIL: verdict_line_shape |
| K12 | `order_covers_every_variant` count +1 | FAIL: order_covers_every_variant |
| K13 | fixture base pin written as 5 | FAIL: fixture_False_baseline_pin_two, fixture_True_baseline_pin_two |
| K14 | fixture tip instrument keeps 2 arms | CRASH: `CalledProcessError` on the second `git commit` (nothing changed) |
| K15 | fixture pin never moves | FAIL: fixture_True_pin_moved |
| K16 | **toplevel guard neutered (`raise` → `pass`)** | **SURVIVED: 44/44** |
| K17 | fixture `git init` targeted at the parent | CRASH: `r48c1.Anchor: fixture is not its own repository` (guard fires; uncaught in the selftest) |
| K18 | `lane_head_unchanged` comparison inverted | FAIL: lane_head_unchanged |
| K19 | **`run_tool` rc/agreement block replaced by `pass`** | **SURVIVED: 44/44** |
| K20 | `opaque()` returns a constant | CRASH: `FileExistsError` (no collision handling) |

Five mutations survive the full selftest (K04, K06, K10, K16, K19); they correspond to F3, F9, F11, F12 and F5 below.
Two mutations kill arms only because of a *different* mechanism than the one they "guard" (K10 → junk_met; K06 →
insertion order already differs from `ORDER` because `real-opaque` is appended last, so the arm passes with no sort).

## 10. What the counter cannot see

1. **Whether the tool bytes are the bytes at R.** `--tool` is only `os.path.abspath`'d (L334); nothing compares it with
   `git show R:tools/mori-pin-check.py`. The receipt's `rev=` names R's *registry*, not the scored tool's revision. The
   L1's own command uses the working-tree path, so a pre-landing draft scored against `--rev <tip>` would be recorded as
   "tool at R" (F21).
2. **Why a variant was rejected.** `run_tool` keeps only the last `PIN_CHECK=met|unmet` line (L238-240) and drops the
   finding lines; neither `measure` nor `main` prints them. `junk_met=0` proves 18 reduce to `unmet`, not that each
   reduced for its stated class. A variant can silently change class (e.g. N5's row caught as a tally mismatch instead
   of as a contradicting exit contract) and the receipt looks identical (F4).
3. **The tool's own `--selftest` pass/fail** — but note the nuance at the landed tip: the reconciler row's command is
   `python3 tools/mori-pin-check.py --selftest`, and `tools/mori-pin-check.py` L408 runs row commands with
   `cwd=root` where `root` is the *exported* revision (L614 `git archive`). At the landed tip that export contains the
   tool under test, so the counter *does* invoke the tool's selftest through the row and scores the pin. It just does not
   score the pass/fail semantics.
4. **The counter's own residue and the tool's writes to the lane.** No before/after snapshot of the lane worktree or
   index around a run (only `lane_head_unchanged`, and only inside `--selftest`). The tool writes
   `<repo>/.scratch/pin-check-*` on every run.
5. **Whether `--skill` was honoured.** Inferred from verdicts only; there is no echo of the file the tool read. (This
   direction fails closed: a tool that ignores `--skill` scores all 25 staged runs on R and lands at `junk_met=18`.)
6. **The delta channel.** Every staged run passes `--repo lane --rev R` together with `--skill <copy>`, so the tool can
   `git show R:SKILL.md` and diff the copy, classifying by *which lines were appended* rather than by any registry rule.
   Opaque file names do not close this: N1-N9 append after the last line and are trivially recognisable by their diff
   shape. Inherited from round 48 (`r48.measure` also passed `--repo`/`--rev`), but it means a "narrower than the junk"
   tool can pass without implementing the rules.
6b. **The identity channel (see §11).** The copy's *name* is a hash of its *content*, and all copies are staged into one
   directory in a fixed order, so a tool can identify the edit from the filename (replaying the committed counter) or
   from the mtime rank of its siblings — without reading any registry text. Both falsifiers reach the target line.
7. **Old named residue is still on disk.** `lane/.scratch/c1-<rand>/` holds round-48 artefacts
   (`c1-J1-ypbkh418`, …, `variant-J1.md`, from `r48` L247 `mkdtemp(prefix="c1-%s-" % name, …)`). They describe round 48,
   not the current run, so they carry no signal about the edit being scored — but a tool that globs `lane/.scratch`
   finds variant names there, and the "opaque handles" claim is about this run's arguments only.
8. The contract's own named limits (K2-K8 classes; the tool may be narrower than the junk).

## 11. Falsifier: the target line is reachable without reading the registry at all

Two stubs I wrote under `.scratch/r49-Mo49RevC1Counter/` score the exact target line. Neither parses a registry row,
neither computes a pin, neither runs `tools/mori-pin-check.py`, neither reads the *copy's* text. Both need only the
committed `.ufo/waves/round-49/count-c1.py` (in-tree at R, and inside the export the tool is given), which yields the
variant list and the naming function.

**(1) `sniffer-lookup.py` — content-hash inversion.** `plan()` names each copy `s-<sha256(rev, body)[:12]>.md` (L257-258).
The stub re-applies every variant function to `git show R:SKILL.md`, hashes the results with the counter's own `opaque()`
imported from the in-tree file, and looks its own basename up:

```python
rev  = git(repo, "rev-parse", "--verify", a.rev + "^{commit}").strip()
text = git(repo, "show", rev + ":SKILL.md")
m    = import_frozen(os.path.join(repo, ".ufo/waves/round-49/count-c1.py"))
table = {m.opaque(rev, fn(text)): expect for name, expect, fn in list(m.r48.VARIANTS) + m.NEW_VARIANTS}
table[m.opaque(rev, text)] = "met"                      # real-opaque
got  = table.get(os.path.basename(a.skill)[2:-3], "unmet")
```

Smoke test (each variant staged under exactly the counter's name): **23/23 verdicts matched**, no registry read. Full
battery:

```
$ python3 .ufo/waves/round-49/count-c1.py --tool .scratch/r49-Mo49RevC1Counter/sniffer-lookup.py \
      --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 4 --scratch .scratch/r49-Mo49RevC1Counter/fullrun
…
variant name=N10 expect=unmet got=unmet rc=1
variant name=H5 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
variant name=real-opaque expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
exit=0
```

The only "rule" it contains is for the two fixture runs (compare the `PROBE_SELFTEST` pin in the fixture `SKILL.md` with
the arm count in `tools/probe.py`); the 24 staged runs are answered purely by name lookup, and the no-`--skill` registry
run is answered blind (`met`).

**(2) `sniffer-mtime.py` — staging order.** `plan()` writes all 24 copies (23 variants then `real-opaque`) into one
scratch directory, in `list(r48.VARIANTS) + NEW_VARIANTS` order, and *before* any run starts. `os.stat().st_mtime_ns`
preserves that order exactly (verified in `fullrun/`: `s-49383f5a8376.md` 22:03:25.398302379, `s-3f9babd911bb.md`
.412259250, `s-c2c3e40dce45.md` .420622725, … — I also checked the three leading tags against `opaque(rev, body)` for
J1..J3 and they match). The stub ranks its own copy among its siblings by mtime and uses the rank as the variant index,
hashing nothing and reading no Markdown:

```
$ python3 .ufo/waves/round-49/count-c1.py --tool .scratch/r49-Mo49RevC1Counter/sniffer-mtime.py \
      --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 4 --scratch .scratch/r49-Mo49RevC1Counter/mtimerun
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
exit=0
```
`grep -c 'expect=unmet got=met\|expect=met got=unmet'` → 0: no row misclassified.

**Why the selftest cannot see either.** `filename_sniffer_not_met` (L393-401) matches only the literal names
`variant-[JN]|/c1-[JN]|junk` against the `--skill` path, the run tmpdir and `--repo`; a 12-hex basename and an mtime rank
match none of them. `handles_carry_no_variant_name` (L367) only asserts that the *names* contain no variant string.
Both arms stay green under tools that are entirely keyed to identity.

**What this means.** The receipt is honest — the committed witness really is a reconciler — but `C1=met` does not
establish the claim's calibration property ("the counter hides which edit it is scoring"), and the round-48 F1 class
("a tool keyed on the harness's variant filename passed C1") is reopened in two forms that the counter's own sniffer
pair cannot detect. Content-addressing is the wrong primitive here: P-C1 prescribes "named by a sha256 prefix of their
bytes", and any tool can recompute that prefix from the frozen generator. Closing it needs (a) a per-run, non-content
name (`os.urandom`), (b) a per-run directory holding exactly one copy, and (c) copies created in an order (or with
mtimes) that does not encode the variant sequence — none of which can be changed after scoring under this round's kill
rule, so this is a wave-2/successor-counter finding.

Receipts and stubs kept for the L1 (inside my scratch, which is cleaned at round end): `sniffer-lookup.py`,
`sniffer-mtime.py`, `fullrun-receipt.txt`, `mtimerun-receipt.txt`, and `selftest-base.txt`. The peer critic
`Mo49CritC1Counter` reports the same two channels (content-addressed handles; one shared staging directory / staging
order) as HIGH; the runs above are the end-to-end receipts for them, obtained independently of that report.

## Residual risk and verification gaps

- I did not run the full 27-run measurement with the committed witness (≈90 s per tool invocation at the freeze, so a
  faithful re-run is ~10 min at `--jobs 4`); I relied on `evidence/control-c1-*.txt` for the per-variant verdicts. I did
  run the full battery twice with my own stubs (§11) — those complete in <3 s because the stub returns immediately — and
  the arm inventory / fixture behaviour was reproduced directly. An independent re-run of the witness would confirm the
  committed receipt bit-for-bit; it is not needed for any defect above.
- My 12-run "detection reason" probe was killed by the 900 s clamp after 3 of 12 runs (N1, N2, N3); reasons for N4-N9,
  N10, H5-H7 are UNVERIFIED and the ones quoted for N2/N9 come from a shadow-repo run of the same bytes. Operational note
  for the tip measurement: on this loaded host the witness took ~300 s per invocation (3 sequential runs in 900 s) against
  ~90 s at the freeze. The tool's per-pinned-command cap is 600 s (`tools/mori-pin-check.py:100`) and the counter's
  per-run cap is 900 s (`TOOL_TIMEOUT`, imported from round 48), so a host ~2× slower than my probe would start turning a
  correct tool's runs into `timeout`/`error` → `C1=unmet`. A tip measurement taken while other seats run the same counter
  is therefore a false-red risk, not a verdict.
- No LSP device is mounted in this session (`xd://lsp` → "No such tool"); `references`/`definition`/`diagnostics` were
  therefore unavailable and every cross-reference below is a literal-text check (`grep`/`read`), not semantic proof.
- Not applicable to this seat: resume paths / `resume_continuity_v1`, runtime rerouting, saturation claims (no such
  surface in this claim).

## Findings

**HIGH**

- **F22 — the content-hash handle is invertible, so a tool with no pin logic scores the exact target line.**
  `count-c1.py:216-221` (`opaque` = sha256 prefix), `:257-258` (`s-<tag>.md`), `:261`/`:275` (`t-<tag>` and hash sort). The
  variant set, R's `SKILL.md` and the naming function are all in the committed tree, so a tool can build
  name → expected-verdict and print it. Proven end-to-end: `sniffer-lookup.py` →
  `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…`, exit 0, 23/23 in the smoke test. The
  selftest's `filename_sniffer_not_met` (L393-401) only matches literal names and stays green. This is the round-48 F1
  class in a new dress.
- **F23 — all copies are staged into one directory in variant order, so the copy's mtime rank identifies it.**
  `count-c1.py:255-262` (one `stage()` loop into `scratch`, `real-opaque` last), `:264`. Verified: the 24 staged copies'
  `st_mtime_ns` ascend exactly in `list(r48.VARIANTS) + NEW_VARIANTS` order, and the three leading tags equal
  `opaque(rev, body)` for J1..J3. Proven end-to-end: `sniffer-mtime.py` (no hashing, no Markdown) →
  `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…`, exit 0, zero rows misclassified.
  No selftest arm covers staging order or sibling visibility (`order_not_expect_sorted` is vacuous, F9).
- **F1 — the frozen predicate's flag clause is not what the counter runs for N10/H5; at the literal flags the honest
  control H5 is red.** `count-c1.py` L265-267 (`base, 1`) and docstring L10 (`every run with --min-tally-pins 26
  --baseline-rev 2d85e33d`). Evidence: witness at `--min-tally-pins 26` on the built fixture → `H5 PIN_CHECK=unmet`;
  at `1` → `met`. Reproduction of `C1=met` from P-C1's literal sentence is impossible, and the receipt line carries no
  per-run flags. Remedy is a contract erratum naming the fixture runs' flags (or a counter line that prints them), not a
  post-scoring counter edit. `count-c1.py:265-267`, `count-c1.py:10`, `contract.md` P-C1.
- **F2 — landing-critical: the reconciler row's `PIN_CHECK_SELFTEST pass=60` is re-executed inside the exported R tree, so
  the landed tool's arm count must be pinned in the same commit or `real` fails.** `tools/mori-pin-check.py` L408
  (`cwd=root`) + L614 (`git archive`); `SKILL.md:938` pins `pass=60`; the committed witness's own selftest prints
  `pass=65`. The freeze receipt passes only because the export at `b3e3453d` still contains v3 (60). If the landing seat
  lands a tool whose selftest prints anything other than the pinned number, `real` → `unmet` → `C1=unmet`.
  `SKILL.md:938`, `count-c1.py:274`. Corroboration (peer, not my run): seat Mo49ExecFlaggedFixed reports that at the
  round-48 landing `e4dfff32` the landed bytes printed
  `pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=60 fail=0' observed='pass=60 fail=0'` —
  i.e. the same-commit obligation held there, and it is the obligation this round inherits.

**MED**

- **F3 — the selftest guards a *duplicate* of the staging logic, not `plan()` itself.** `plan()` L255-261 has its own copy
  of `stage()`; the arms exercise `plan_text_only()` L434-450. Naming the real path's copies by variant name (K04)
  survives 44/44. This is the round-48 F1 leak class, untested in the path that runs. `count-c1.py:255-261`,
  `count-c1.py:434-450`, `count-c1.py:365-368`.
- **F4 — receipts are reason-blind: the tool's finding lines are discarded, so `junk_met=0` cannot show *why* a variant
  reduced.** `count-c1.py:238-240` keeps only the verdict line; `measure`/`main` print only `name/expect/got/rc`. A
  variant whose rejection cause changes (e.g. `_cur_pin` L74-78 picking an example pin, or another row's command starting
  to fail) still reduces to `unmet` and reads identically. `count-c1.py:238-240`, `count-c1.py:74-78`, `count-c1.py:336-338`.
- **F5 — `run_tool`'s rc/agreement block is untested; deleting it leaves 44/44 (K19).** With it gone, a tool that prints
  `PIN_CHECK=unmet` but exits 0 is scored as correctly rejecting junk — the exit-code contract the registry advertises
  would silently stop being measured. `count-c1.py:241-244`.
- **F6 — a mistyped or absent `--tool` is reported as `C1=unmet` (exit 1), not `C1_SETUP` (exit 2).** Under the contract's
  kill rule that reads as a failed claim. Observed: `C1=unmet … errors=27` in 0.25 s with `--tool …/nope.py`. No
  existence check at `count-c1.py:334`.
- **F7 — docstring claim "the lane repo is only read" is false, and the default scratch puts 25 tool scratch dirs plus 2
  nested git repositories inside the lane per run, uncleaned.** `count-c1.py:38-40`, `:332`, `:178` (no `exist_ok`),
  `:186`; tool side `tools/mori-pin-check.py:649-652` (the 2 fixture runs write their tool scratch inside the fixture
  repos instead). `.scratch` is not gitignored at the freeze (26 G, 199 entries); a nested repo becomes a 160 000
  gitlink on the next `git add -A` (proved in a throwaway repo). Lane observables checked after my runs: `HEAD`
  `0df17b7b…`, empty staged diff — no lane git state was touched.
- **F8 — `--scratch` is not reusable: the second `plan()` into the same directory raises `FileExistsError` and the counter
  exits 2.** `count-c1.py:178` (`os.makedirs(d/tools)` without `exist_ok`), `:176` (deterministic fixture dir name).
  A reviewer comparing two runs into one scratch directory sees `C1_SETUP fixture variant: … File exists`.
- **F9 — `order_not_expect_sorted` cannot fail for the reason it names.** It passes with no sort at all (K06), because
  `plan_text_only` appends `real-opaque` before `real` and `ORDER` lists them last, so insertion order already differs
  from `ORDER` order. The hash sort at `:275` / `:448` is unprotected.
- **F14 — `verdict` does not assert the variant inventory.** Dropping a name from `NEW_VARIANTS` still prints
  `C1=met` with a smaller `variants=` and exits 0 (`C1=met … variants=25`, `variants=22` observed). Only the literal
  `variants=26` in the contract catches it; `:305`, `:403`.
- **F15 — N8's anchor is brittle against a legitimate landing edit.** It requires exactly one row containing both
  `python3 tools/mori-pin-check.py --selftest` and a `PIN_CHECK_SELFTEST` pin (`:128-132`); a second such row (e.g. a new
  rule row that also runs `--selftest`) turns the whole counter into `C1_SETUP` exit 2. Fail-closed, but it converts a
  correct landing into "claim not verified".
- **F21 — no binding between the tool under test and R's `tools/mori-pin-check.py`.** `--tool` is only `abspath`'d
  (`:334`); the receipt's `rev=` pins the registry, not the scored bytes. P-C1 says "the tool bytes under test
  (`tools/mori-pin-check.py` at R)", which the counter neither checks nor prints. A one-line
  `sha256(tool) == sha256(git show R:tools/mori-pin-check.py)` assertion (or a `tool_sha=` field in the line) would close
  it; today a pre-landing draft scored against `--rev <tip>` is indistinguishable from the landed bytes.

**LOW**

- **F10 — `plan_ok` is a tautology.** `plan_text_only` returns `(jobs, None)` unconditionally (`:449`), so `err is None`
  (`:365`) can never be false; the arm only "fails" if the function raises, which aborts the selftest with a traceback
  rather than a `FAIL` line.
- **F11 — `errors == 0` is unreachable as a discriminator and `junk_met` double-counts errors.** `:299`, `:303`; K10
  survives; `--tool …/nope.py` prints `junk_met=18 … errors=27`.
- **F12 — the toplevel guard is not exercised by the selftest (K16 survives).** `fixture_*_own_toplevel` (`:418-420`)
  re-implements the check instead of driving the guard; the guard itself works (K17), but it can be deleted with the
  selftest staying green. `:182-184`.
- **F13 — `-I -B` invocation is stricter than the documented command.** `:225`; `-I` implies `-P` on 3.11+, so a tool
  that imports a sibling module or user-site package would be scored `error` although its registry command works.
- **F16 — argument parsing crashes instead of exiting 2.** A flag with no value → `IndexError` (`:318`), `--jobs 0` →
  `ValueError` (`:334`→`:286`), both exit 1 with a traceback.
- **F17 — `_cur_pin` takes the first matching pin anywhere in the document.** `:74-78`; at R there is exactly one
  `PIN_CHECK_SELFTEST pass=` (line 938) and one `UNLANDED_SELFTEST` (line 973), so N5/N8/N9 are unambiguous today, but a
  future example pin would silently change which tally N5/N9 embed, and with it the variant's class.
- **F18 — staged copies are never re-hashed after the runs.** A tool could rewrite sibling copies in `--scratch`
  (not exploitable in the direction of a pass, since honest copies would then also be rejected, but copy integrity is
  unverified).
- **F19 — the selftest hardcodes `master`** (`:354`, `:421`) and reports a bare `C1_SELFTEST pass=0 fail=1` if the default
  branch is renamed or `SKILL.md` is missing; in my shadow repo (init default branch `main`) that was the only symptom.
  `plan_text_only` also hardcodes `LANE` as the repo (`:444-447`), so it cannot be pointed at `--repo`.
- **F20 — `measure()`'s `jobs` parameter is the worker count, not the plan** (`:281`, `:286`), while `plan()` calls its
  returned list "jobs". Readable only via the call site; a future caller passing a plan would be silently ignored
  (`measure` re-plans).
