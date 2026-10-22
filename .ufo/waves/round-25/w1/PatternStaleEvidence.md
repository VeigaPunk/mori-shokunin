# PatternStaleEvidence — is D1 a one-off or a pattern? (round 25, wave 1, connector)

Seat: `MoriR25.PatternStaleEvidence`. This seat is read-only on the lane except for this file. It changes no C1 target.
Measured at lane commit `0099a391eccaf3b6b9910d8d71d4d48ca4ea539f`. The tip later moved to `51ddd019`
(contract amendment A1, after `09f55b6` and `129832e`).
`git diff --stat 0099a391 51ddd019 -- .ufo/waves/round-1{8,9} .ufo/waves/round-2{0,1,2,3,4} corpus/evidence tools/mori-pressure.py`
prints nothing, so every count below also holds at `51ddd019`.
Tool installs and updates: none. Toolchain as found: Python 3.14.8 and GNU bash 5.3.20.

## Verdict

**D1 is a pattern, not a one-off. It has two separate parts.**

1. **Names no revision.** 16 selftest-output data files bind to no revision and no tool hash. All of them are bare
   `.txt` or `.stdout` files written in rounds 18 (1 file), 20 (14 files) and 24 (1 file, D1 itself). Rounds 19 and 21–23
   wrote JSON command receipts with `measured_revision`, and the corpus receipts from rounds 3–12 carry `CENSUS_SHA256`.
   Those groups have 0 unbound files.
2. **Predates the tool it shipped with.** I re-ran 15 of the 16 unbound files with the named tool at their evidence
   commit. 3 are stale: D1 and two round-20 files. In all three, the commit that landed the evidence also edited the
   named tool. Of the 10 re-run unbound files whose landing commit did not touch the tool, 0 are stale.

The required sample of 5 found 1 stale file and 4 matches. Re-running the whole unbound class found 3 stale, 11 matching
and 1 unrun.

## 1. Surface and counts

Surface command, as assigned. The same count comes from `git ls-tree -r --name-only 0099a391` filtered the same way:

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files | grep -iE 'selftest|evidence' \
  | grep -cE '^(\.ufo/waves/round-(1[89]|2[0-4])/|corpus/evidence)'      # -> 1404
```

**What counts as a selftest-output file.** It is one of the 1404 paths whose blob contains a tool selftest summary line,
excluding `.py`, `.pyc`, `.sh` and `.gz` files. Those excluded files are tool copies and committed bytecode. That
removes 212 `__pycache__/*.pyc` blobs inside round-20 SelftestC2 mutant trees and 239 source copies.

The summary-line formats were read from every tool in lane history:
`git log --all --format= --name-only -- 'tools/*'` gives 24 tools. Each `print` or `finding_id` was read with
`git grep -nE '(SELFTEST|selftest)…' HEAD -- tools/…`. That yields 18 marker families:

| Tool(s) | Marker |
|---|---|
| census.sh / pressure / wave-settlement / journal-window | `MORI_CENSUS_SELFTEST:`, `MORI_PRESSURE_SELFTEST:`, `MORI_WAVE_SETTLEMENT_SELFTEST:`, `MORI_JOURNAL_WINDOW_SELFTEST` |
| misroot-sweep | `MORI_MISROOT_SELFTEST_(OK\|FAIL\|SETUP)` |
| retention-gate / freeze-order / dispatch-ledger | `SELFTEST retention-gate PASS`, `SELFTEST freeze-order PASS`, `SELFTEST mori-dispatch-ledger PASS` (and FAIL) |
| round13 / round14 / round15 regressions | `SELFTEST: pass checks=N cases=`, `SELFTEST: pass checks=N (parsers`, `SELFTEST PASS selftest_root=` / `SELFTEST control classifier checks:` |
| round16-regr / round17-jj / round17-seat | `SELFTEST (ok\|FAIL\|SETUP\|kept):` |
| round16/17 context-check / seat-terminal | `"SELFTEST_(OK\|FAIL)"` |
| quota-surface / content-review / retention-reconcile / evidence-loss | `QUOTA_SELFTEST_*`, `CONTENT_REVIEW_SELFTEST_*`, `RECONCILE_SELFTEST_*`, `mori-evidence-loss-selftest-v1` |
| silence-cases.sh (census oracle) | `MORI_SILENCE_CASES: matched=` |

A file **names a full revision** when it holds a 40-hex token, not adjacent to other hex, that
`git cat-file --batch-check` resolves as `<tok>^{commit}` in the lane.

| | Names a full revision | Names none | Total |
|---|---|---|---|
| Selftest-output files (all) | **41** | **33** | **74** |
| …data files (`.json`, `.txt`, `.log`, `.stdout`) | 40 | 31 | 71 |
| …prose (`.md`: `corpus/evidence/README.md`, `round-20/falsify/SelftestC2.md`, `roster-r12-…-mutation.md`) | 1 | 2 | 3 |

Naming a revision does not mean naming the *measured* one. So each of the 71 data files also gets a binding class.
The evidence commit is `git log -1 --format=%H 0099a391 -- <path>`, and the named tool is the one whose marker the file
carries:

| Class | Meaning | Files | Where |
|---|---|---|---|
| A | names a commit at which the named tool blob equals the tool blob at the evidence commit | 24 | rounds 19 (6), 21 (1), 22 (4), 23 (11), corpus (2) |
| B | no such commit, but a sha256 in the bytes equals the named tool's bytes at the evidence commit | 28 (13 with a commit, 15 without) | corpus rounds 3–12 (`CENSUS_SHA256=` and `ORACLE_SHA256` headers) |
| C | names a commit or tool hash, but none matches the tool at the evidence commit | 3 | round-22 `measure2/{selftest,summary}.json`, round-23 `quota-selftest-delivered.json` |
| D | names no commit and no tool hash | **16** | round 18 (1), round 20 (14), round 24 (1, D1) |

All three class-C files are honest. Each records `measured_revision` equal to the parent of its evidence commit, and the
`stdout` field equals that revision's tool output byte for byte:

- round-22 `measure2`: `50b6f754` and `da40bb20` both print the recorded `RECONCILE_SELFTEST_PASS 4/4` (`cmp` EQUAL at both).
- `quota-selftest-delivered.json`: `56ac3bad` prints the recorded `QUOTA_SELFTEST_FAIL` exactly (`cmp` EQUAL).
  The corrected tool at `f3dc07c0` prints `QUOTA_SELFTEST_OK`, which differs; this is the intended "delivered vs
  corrected" pair.

## 2. Re-runs: does the named tool at the evidence commit print the same lines?

**Method.** Extract the evidence commit with `git archive <commit> | tar -x -C ~/.cache/mori-r25-pse/<commit8>`.
Several tools refuse to run from a `/tmp` extract, so the extracts live under `~/.cache`; see the risks section.
Each tool runs as `python3 -I -B <tool> --selftest`, or `bash tools/mori-census.sh --selftest`, under
`env -i PATH=<tripwire>:/usr/local/bin:/usr/bin:/bin:~/.local/bin HOME=<scratch> TMPDIR=<extract>/.scratch LANG=C LC_ALL=C TZ=UTC`.
The tripwire puts `journalctl` and `omp` stubs first on PATH; neither fired, and `/tmp/pse/out/tripwire.log` was never
created. Comparison is `cmp` of the evidence bytes against the run's stdout. Lane annotation lines (`rc=N`,
`<gate> rc=N`) are removed first.

**Sample of 5.** I chose one file per producing context instead of using a path hash, because a hash picked five
round-20 NoHarmRun logs. D1 was run as a control.

| # | Evidence file (no revision) | Evidence commit | Run (UTC, 2026-10-22) | Result |
|---|---|---|---|---|
| S1 | `round-18/evidence/final-selftests.txt` | `3786f3f1` | 10:02:52–10:03:16; retention-gate, freeze-order, dispatch-ledger, census, round17-context-check | **match.** All 5 summary lines are byte-equal: `PASS 21/21`, `PASS 12/12`, `PASS 14/14`, `PASS (134 cases…)`, and the JSON `{"arms": 31, … "clauses_checked": 12, …}`. round16-context-check prints `arms: 15`, so round17 is the producer |
| S2 | `round-20/evidence/c2-final-selftest.txt` | `71abd41f` | 10:02:33 wave-settlement | **match.** `PASS (23 cases, 23 passed, 0 failed)` |
| S3 | `round-20/evidence/mut-r7/selftest-production.txt` | `71abd41f` | same run as S2 | **STALE.** The file says `PASS (22 cases, 22 passed…)` and the tool at `71abd41f` prints `23 cases` (`cmp`: differ at char 39, line 1) |
| S4 | `round-20/falsify/NoHarmRun/logs/17-r18-freeze-order-selftest.stdout` | `71abd41f` | 10:02:52 freeze-order | **match.** The whole stdout is byte-equal |
| S5 | `round-20/falsify/NoHarmRun/logs/05-r14-selftest.stdout` | `71abd41f` | 10:03:01 round14-regressions | **match.** The whole stdout is byte-equal |
| control | `round-24/evidence/c2-selftest-after.txt` (D1) | `89849a76` | 10:02:33 pressure | **STALE**, reproducing D1. The tool at `89849a76` prints `PASS 12/12` plus `MATCHER: rejected 48/48 corrupted expectations` (`cmp`: EOF after byte 35). The tool at the parent `13208d2a` prints exactly the committed 35 bytes (`cmp` EQUAL) |

**Beyond the sample: the rest of class D, all at `71abd41f`, run 10:05:26–10:06:09Z.**

| File | Result |
|---|---|
| NoHarmRun `01-census`, `03-r13`, `09-r16`, `11-r17-seat`, `16-dispatch-ledger`, `20-retention` | match, whole stdout byte-equal |
| NoHarmRun `07-r15` | match except the tool-printed random path `selftest_root=…/mori-r15-selftest-<random>`, which no rerun can reproduce |
| NoHarmRun `18-c2-settlement-selftest.stdout` | **STALE.** The file says `22 cases`; the tool at `71abd41f` prints `23 cases` |
| `mut-r7/selftest-mutant.txt` | Its producer is the committed mutant, not the tool. `.ufo/waves/round-20/evidence/mut-r7/mutant-no-lexical-dotdot.py` prints the file's bytes exactly: `FAIL (22 cases, 21 passed, 1 failed)` |
| NoHarmRun `13-r17-jj` | **not run.** That selftest drives `jj`, and I kept `jj` out of scope. This is not a pass |

Totals over class D: **3 stale, 11 match, 1 unrun.**

**Why the two round-20 stale files have no reproducible source.**

- Only two wave-settlement blobs were ever committed, in any ref:
  `git log --all --raw --no-abbrev -- tools/mori-wave-settlement.py` gives `b13d9436` (sha256 `c6e60919…`, at `2eeae04`)
  and `cf2f5dcd` (sha256 `79e7f9de…`, at `71abd41f`).
- `2eeae04` prints `PASS (21 cases…)` (run at 10:05:06Z) and `71abd41f` prints `23 cases`. No commit prints 22.
- NoHarmRun's own sidecar `logs/pre-hashes.json` records the tool it ran as `e5c06dad…`. That matches neither committed
  blob, while 19 of its 20 other recorded hashes equal `71abd41f`.
- The 22-case output therefore came from a working tree that was never committed. The mut-r7 mutant sits 9 diff lines
  from `2eeae04` and 39 from `71abd41f`, which fits that intermediate base.

## 3. The mechanism: a mechanical screen over git objects only

Script: `/tmp/pse/cocommit.py`. For each file it checks whether `git diff-tree -r --name-only <evidence commit>` lists
the named tool.

| Class D files | Evidence commit edits the named tool | Does not |
|---|---|---|
| count | 5: `c2-final-selftest.txt`, `selftest-mutant.txt`, `selftest-production.txt`, NoHarmRun `18`, D1 | 11 |
| stale after re-run | **3** (D1, S3, NoHarmRun 18) | **0** of 10 re-run (1 unrun) |

The screen has false positives: `c2-final-selftest.txt` was regenerated after the last edit, and `selftest-mutant.txt`
has a different producer. It had no false negatives in this population. Across all 71 data files the evidence commit
edits the named tool in 30 cases. 25 of those (22 B and 3 C) are safe only because the file also carries a measured
revision or tool hash. Binding is what neutralizes the co-commit risk.

## 4. Proposed move (one bounded proposal; changes no C1 target)

**Move.** Write two things into the round-25 lesson, and into draft criterion 76
(`.ufo/waves/round-25/w1/QualityCriteriaDraft.md:20-33`):

- **The rate.** D1 recurs: 16 unbound selftest-output files, all from bare-stdout rounds 18, 20 and 24. 3 of 15 re-run
  are stale, and all 3 landed in a commit that also edited the tool.
- **A wider definition of stale.** Criterion 76's red clause currently reads "names no revision, or whose output
  **lacks a line** the shipping tool prints at that revision" (`QualityCriteriaDraft.md:29-30`). Replace it with
  "…or whose bytes **differ from** the stdout the shipping tool prints at that revision".

**Why it is non-obvious.** D1's visible symptom was a missing line (`MATCHER`). The two other stale instances lack no
line: they carry the same summary line with a different value, `22 cases` against `23 cases`. So "lacks a line" would
grade both round-20 files green. "Differ from" catches both shapes and matches the criterion's own earlier sentence:
"the remaining bytes are the complete stdout…".

**Compatibility.**

- *Amendment A1 (`51ddd019:.ufo/waves/round-25/contract.md:96-131`).* A1's D1 row requires `tool_blob` and
  `fixtures_tree` equal at R and REV. That is the forward-looking form of the screen in §3; this sizing shows the
  clause targets the actual failure mode. A1's committed-evidence rule ("written after the last change to the measured
  tool") closes the co-commit path for round 25's three evidence files.
- *CriticC1Predicates F2 (`w1/CriticC1Predicates.md:100-104`).* F2 proposes generalizing D1 to every round-25 evidence
  file containing `_SELFTEST:`. That is compatible for round 25, because both round-25 gates print `MORI_*_SELFTEST:`.
  But `_SELFTEST:` matches only 3 of the 18 historical marker families (census, pressure and wave-settlement). Lifted
  lane-wide, it would miss formats like `SELFTEST freeze-order PASS 12/12` and `"SELFTEST_OK"`.

**Affected axes.** Calibration improves: the lesson states the measured recurrence and shape instead of one instance,
and the criterion's red clause covers the observed value-drift case. Coverage (C2) and the held axes are untouched,
because there are no tool, contract or target edits.

## 5. Risks and contradictions (stated, not smoothed)

- **The marker set is mine.** It holds 18 regexes read from tool sources. A selftest format not in it would leave a file
  out, so 74 is a lower bound on the population. `.md` files are excluded from the binding classes.
- **A "full revision" is any 40-hex token that resolves to a lane commit.** Class A, not the raw 41, is the measure of
  "names the measured revision".
- **The reruns are today's.** They used Python 3.14.8 and bash 5.3.20 on 2026-10-22, not the original runs' interpreter
  or host. A match shows the committed tool reproduces the bytes now. It does not prove the original run used that tool.
  NoHarmRun's `pre-hashes.json` is the only sidecar that pins the original run.
- **Scratch guards.** freeze-order, retention-gate, dispatch-ledger, round17-seat and round17-jj all refuse a `TMPDIR`
  under `/tmp` or `/var/tmp`, or outside the checkout. Examples: `tools/mori-freeze-order.py:503` and
  `tools/mori-dispatch-ledger.py:429-434` at HEAD; the first runs from a `/tmp` extract printed `FAIL 0/11`, `FAIL 0/21`
  and `SELFTEST_SCRATCH_FORBIDDEN`. Any rerun-based check that extracts to a system temp directory, including A1's
  optional `--rerun` if generalized beyond pressure, will report false reds for those tools.
  `tools/mori-pressure.py` at `89849a76` ran fine from `/tmp`.
- **A1's D1 pins tallies.** It requires `PASS 12/12` and `MATCHER: rejected 48/48`. If round 25 adds main pressure cases,
  rather than only supplementary ones, a fresh file goes red [INFERENCE: from the contract's "six surviving mutants …
  killed by new supplementary cases" (`contract.md:34-36`)]. A change limited to `supplementary-cases.json` leaves
  12/12 intact.
- **Severity differs by round.** In round 20 the claim evidence (`c2-final-selftest.txt`, cited at `SCORECARD.md:1277`)
  is current; only the supporting files are stale. In round 24 the stale file was the C2 after-evidence
  (`round-24-verifier-spotcheck.md:80,137`).

## 6. Verification (re-runnable; throwaway scripts outside the lane)

```
python3 -I -B /tmp/pse/classify.py <lane> 0099a391eccaf3b6b9910d8d71d4d48ca4ea539f > rows.json   # 74 = 41 rev + 33 none
python3 -I -B /tmp/pse/binding.py  <lane> rows.json      # counts {"A":24,"B":28,"C":3,"D":16}
python3 -I -B /tmp/pse/cocommit.py <lane> rows.json      # evidence commit edits named tool, per file
/tmp/pse/run.sh <extract> <label> python3 -I -B tools/<tool> --selftest   # scrubbed env + tripwire; logs /tmp/pse/out/runs.log
cmp <(git -C <lane> show 0099a391:<evidence path> | grep -v '^rc=') /tmp/pse/out/<label>.stdout
```

Every rerun's argv, start and end times, and exit code are in `/tmp/pse/out/runs.log`. The stdout sha256 prefixes are:

| Run | stdout sha256 prefix |
|---|---|
| D1 control (pressure at `89849a76`) | `d767d1b6fd53e45c` |
| wave-settlement at `71abd41f` | `5a0306628695dc2f` |
| freeze-order | `1b88c110df1daa75` |
| round14-regressions | `6e5451e3c3fba0bd` |
| census at `3786f3f1` | `a67a336bf02cb9d8` |

The large tree extracts under `~/.cache/mori-r25-pse` and `/tmp/pse/x` were removed after this report was written.
The small scripts and outputs in `/tmp/pse` were kept for re-derivation.
