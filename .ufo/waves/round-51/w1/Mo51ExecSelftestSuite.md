# Mo51ExecSelftestSuite — round 51 w1 (no-harm: every registry selftest, both tips)

Seat: leaf executor, no-harm for operability. Scope: run every tool selftest the SKILL.md registry pins, at the
data commit `87e0c374537557754bf71dd68036ded3ddc6699c` and, for anything that differs, at the entering tip
`aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd`; compare each last tally line with its pin. No file outside my own
report and my scratch was written; no counter, predicate, control or kill rule was changed or proposed.

Environment: Linux x64, kernel 7.2.11-arch1-1, Python 3.14.8 (`/usr/bin/python3`), GNU bash 5.3.20, git 2.56.0.
No tool was installed or upgraded (no pacman; nothing from uv/npx/release channels was needed).
`bash scripts/hyaku/disk-guard.sh status` before starting: rc 0, `/fast` 27 % used, 589 G free.

## Method

1. Read the frozen contract, then parsed the eleven gate-registry tables of `SKILL.md` **at the data commit**
   (`git show 87e0c374:SKILL.md`): 62 rows, 59 with `--selftest` in the self-test cell, 52 unique commands after
   de-duplication (rows 193–196 restate rows 183–186; rows 165, 546, 905, 908, 910, 911, 912 write only
   `--selftest` and were resolved from their own entry cell, exactly as `mori-pin-check.py`'s
   `derive_command`/`pin_commands` do).
2. One measurement clone: `git clone --no-local <lane> <scratch>/data`, `git checkout --detach 87e0c374`
   (verified `git -C <scratch>/data rev-parse --show-toplevel` = `<scratch>/data`). All 52 commands were run with
   `bash -c`, cwd = clone root, `TMPDIR=<clone>/.scratch` (created), `PYTHONDONTWRITEBYTECODE` untouched, 900 s cap
   per command; rc, stdout and stderr captured. Then `git checkout --detach aa3af1ec` in the same clone and the
   same 52 commands re-run. No second clone, no full mirror; the lane repo, the fleet repo, any git index and any
   jj state were never mutated (reads only: `git show`, `git diff`, `git clone` FROM the lane).
3. The three `conform.py` rows were additionally run with the `<rev>` positional their entry cells require
   (the self-test cells abbreviate to `--selftest`); those runs are the observed values in the table, and the
   literal-argv result is recorded as an anomaly (B2).
4. `tools/mori-index-clean.sh --selftest` was run three ways to attribute its one red arm (B1): `TMPDIR` inside the
   clone's `.scratch` (in-tree, as `mori-pin-check.py` sets it), `TMPDIR` outside any git work tree, and code read.
5. Pins were compared as exact strings against the data commit's SKILL.md cells (a pin is a backticked
   `<PREFIX>SELFTEST …` span in the self-test cell). Rows whose cell carries no such tally pin are marked "no pin"
   and only the observed tally is reported. Digest pins and line-count pins in self-test cells were checked too.

One clone is the only heavy artifact; it was removed at the end (`rm -rf` of my scratch directory).

## Result summary

- 52/52 unique registered selftest commands executed at both tips, all 52 rc and last tally lines reproduced.
- 33 rows carry a tally pin (29 unique commands): **all 29 observed tallies equal their pins exactly at the data
  commit, rc 0**, including the row the data commit touched (`PIN_CHECK_SELFTEST pass=119 fail=0`,
  `CONFORM_SELFTEST pass=11 fail=0`). `SHONEN.md` 119/119 also matches.
- Entering tip: identical except the instruments that legitimately changed across the commit —
  `mori-pin-check.py --selftest` prints `pass=114` at `aa3af1ec` (entering SKILL.md pin 114) and `pass=119` at
  `87e0c374` (data SKILL.md pin 119); `round-40/conform.py --selftest` prints `pass=11` at both. `round-15`'s
  tail contains a random `selftest_root` path, not a tally difference.
- Two anomalies, both pre-existing and identical at both tips (neither is caused by the data commit):
  `mori-index-clean.sh --selftest` fails its `not_a_repo` arm when `TMPDIR` is inside a git work tree (B1);
  the three `conform.py` self-test cells, taken literally without `<rev>`, exit 2 with an internal-shaped error (B2).
- Coverage fact about the C1 instrument: only rows that carry a tally pin are executed by
  `mori-pin-check.py --rev`; 23 of the 52 unique registered selftest commands are never run by it (B3).

## Table

`<REV>` = the tip being measured (the entry cell's `<rev>`, resolved as the reconciler does). Observed strings are
the exact last tally line; long ones are shortened here with `…` and given in full in Appendix A. "Match" compares
the observed tally and rc with the pin.

| # | command | pinned tally (data-commit SKILL.md) | observed @87e0c374 (rc) | observed @aa3af1ec (rc) | match |
|---|---|---|---|---|---|
| 1 | `bash tools/mori-census.sh --selftest` | — (pointer: "r17 measured tally and hash in round-17 evidence") | `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` (0) | same (0) | no pin |
| 2 | `bash tools/mori-silence-cases.sh --selftest` | `MORI_SILENCE_CASES_SELFTEST pass=24 fail=0` | `MORI_SILENCE_CASES_SELFTEST pass=24 fail=0` (0) | same (0) | yes |
| 3 | `python3 tools/mori-round13-regressions.py --selftest` | — (pointer: "measured tally in round-14 evidence") | `SELFTEST: pass checks=33 cases=2` (0) | same (0) | no pin |
| 4 | `python3 tools/mori-round14-regressions.py --selftest` | — (prose: "20 checks") | `SELFTEST: pass checks=20 (parsers + real-gate red rc1/tamper rc2)` (0) | same (0) | no tally pin; prose count matches |
| 5 | `python3 tools/mori-round15-regressions.py --selftest` | — | `SELFTEST PASS selftest_root=<scratch>/mori-r15-selftest-<random>` (0) | same shape (0) | no pin |
| 6 | `python3 tools/mori-round16-regressions.py --selftest` | — | `SELFTEST ok: pin_rc0,green_rc0_verdict_ok,absent_rc1_capability_absent,tool_drift_rc2,…` (0) | same (0) | no pin |
| 7 | `python3 tools/mori-round16-context-check.py --selftest` | — | `{"arms": 15, …, "finding_id": "SELFTEST_OK", "static_only": true}` (0) | same (0) | no pin |
| 8 | `python3 tools/mori-journal-window.py --selftest` | — | `{"cases":16,"failed":0,…,"passed":16}` (0) | same (0) | no pin |
| 9 | `python3 tools/mori-seat-terminal.py --selftest` | — | `{"arms":49,…,"passed":49,…}` (0) | same (0) | no pin |
| 10 | `python3 tools/mori-round17-seat-regressions.py --selftest` | — | `SELFTEST ok: green_rc0_and_manifest,…,nonempty_output_rc2` (0) | same (0) | no pin |
| 11 | `python3 tools/mori-round17-jj-regressions.py --selftest --scratch <scratch>/jj` | — | `SELFTEST ok: guard_output_repo_root,…` (0) | same (0) | no pin |
| 12 | `python3 tools/mori-misroot-sweep.py --selftest` | — | `{"arms": 12, "finding": "MORI_MISROOT_SELFTEST_OK", …}` (0) | same (0) | no pin |
| 13 | `python3 tools/mori-round17-context-check.py --selftest` | — | `{"arms": 31, …, "clauses_checked": 12, …}` (0) | same (0) | no pin |
| 14 | `mkdir -p .scratch && TMPDIR=$PWD/.scratch python3 tools/mori-retention-gate.py --selftest` | — | `SELFTEST retention-gate PASS 21/21` (0) | same (0) | no pin |
| 15 | `python3 tools/mori-freeze-order.py --selftest` | — | `SELFTEST freeze-order PASS 12/12` (0) | same (0) | no pin |
| 16 | `python3 tools/mori-dispatch-ledger.py --selftest` | — | `SELFTEST mori-dispatch-ledger PASS 14/14` (0) | same (0) | no pin |
| 17 | `TMPDIR=$PWD/.scratch python3 tools/mori-content-review.py --selftest` | — | `{"exit_code":0,…,"status":"clean"}` (0) | same (0) | no pin |
| 18 | `python3 tools/mori-round19-regressions.py --selftest` | `R19_SELFTEST pass=26 fail=0` | `R19_SELFTEST pass=26 fail=0` (0) | same (0) | yes |
| 19 | `python3 .ufo/waves/round-44/count-c1.py --selftest` | `C1_SELFTEST pass=6 fail=0` | `C1_SELFTEST pass=6 fail=0` (0) | same (0) | yes |
| 20 | `python3 tools/mori-gate-registry.py --selftest` | `GATE_REGISTRY_SELFTEST pass=15 fail=0` (+ `sha256 8b82ac99…`, 743 lines) | `GATE_REGISTRY_SELFTEST pass=15 fail=0` (0) | same (0) | yes (digest + line count too) |
| 21 | `python3 .ufo/waves/round-44/count-c2.py --selftest` | `C2_SELFTEST pass=5 fail=0` | `C2_SELFTEST pass=5 fail=0` (0) | same (0) | yes |
| 22 | `python3 .ufo/waves/round-44/count-c3.py --selftest` | `C3_SELFTEST pass=6 fail=0` | `C3_SELFTEST pass=6 fail=0` (0) | same (0) | yes |
| 23 | `python3 tools/mori-disk-rate.py --selftest` | `MORI_DISK_RATE_SELFTEST pass=14 fail=0` | `MORI_DISK_RATE_SELFTEST pass=14 fail=0` (0) | same (0) | yes |
| 24 | `python3 tools/mori-wave-settlement.py --selftest` | `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)` | same line (0) | same (0) | yes |
| 25 | `python3 tools/mori-round41-calibration.py --selftest` | `MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0` | same line (0) | same (0) | yes |
| 26 | `python3 .ufo/waves/round-45/count-c1.py --selftest` | `C1_SELFTEST pass=16 fail=0` (+ `sha256 5f2deea0…`) | `C1_SELFTEST pass=16 fail=0` (0) | same (0) | yes |
| 27 | `python3 .ufo/waves/round-45/count-c2.py --selftest` | `C2_SELFTEST pass=14 fail=0` (+ `sha256 153423c4…`) | `C2_SELFTEST pass=14 fail=0` (0) | same (0) | yes |
| 28 | `python3 .ufo/waves/round-45/count-c3.py --selftest` | `C3_SELFTEST pass=19 fail=0` (+ `sha256 37fd7c24…`) | `C3_SELFTEST pass=19 fail=0` (0) | same (0) | yes |
| 29 | `TMPDIR=$PWD/.scratch python3 tools/mori-evidence-loss.py --selftest` | — | `{"checks":114,"failures":[],…,"passed":true,…}` (0) | same (0) | no pin |
| 30 | `python3 tools/mori-evidence-loss.py --selftest` | — (same `--selftest`) | same JSON (0) | same (0) | no pin |
| 31 | `TMPDIR=<scratch> python3 tools/mori-retention-reconcile.py --selftest` | — | `{"finding_id":"RECONCILE_SELFTEST_PASS","passed":4,…,"total":4}` (0) | same (0) | no pin |
| 32 | `python3 tools/mori-pressure.py --selftest` | `MORI_PRESSURE_SELFTEST: PASS 12/12` | `MORI_PRESSURE_SELFTEST: PASS 12/12` (0; next line `MATCHER: rejected 48/48 corrupted expectations`) | same (0) | yes |
| 33 | `python3 -I tools/mori-routed-check.py --selftest` | `ROUTED_CHECK_SELFTEST pass=20 fail=0` | same line (0) | same (0) | yes |
| 34 | `python3 -I -B tools/mori-oom-killers.py --selftest` | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` | same line (0) | same (0) | yes |
| 35 | `python3 -I -B tools/mori-routed-r24.py --selftest` | `ROUTED_R24_SELFTEST pass=26 fail=0` | same line (0) | same (0) | yes |
| 36 | `python3 -I -B tools/mori-job-runway.py --selftest` | `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` | same line (0) | same (0) | yes |
| 37 | `bash tools/mori-blind-check.sh --selftest` | `PASS` (plus expected `scanned=14`/`blind_violations=13` — internal assertions, see B4) | `PASS` (0) | same (0) | yes (stdout) |
| 38 | `python3 tools/mori-source-drift.py --selftest` | `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` (r37 row) | same line (0) | same (0) | yes |
| 39 | `python3 tools/mori-sources-appendonly.py --selftest` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | same line (0) | same (0) | yes |
| 40 | `bash tools/mori-index-clean.sh --selftest` | — (prose: clean, `add -N`, `add`, not-a-repo) | `MORI_INDEX_CLEAN_SELFTEST pass=3 fail=1` (**1**) | identical (**1**) | no pin; arm fails in-tree (B1) |
| 41 | `python3 .ufo/waves/round-38/conform.py <REV> --selftest` | — (prose: "six mutations") | `CONFORM_SELFTEST pass=6 fail=0` (0) | same (0) | no tally pin; prose count matches |
| 42 | `python3 .ufo/waves/round-39/conform.py <REV> --selftest` | — (prose: "nine mutations") | `CONFORM_SELFTEST pass=9 fail=0` (0) | same (0) | no tally pin; prose count matches |
| 43 | `python3 .ufo/waves/round-40/conform.py <REV> --selftest` | `CONFORM_SELFTEST pass=11 fail=0` | `CONFORM_SELFTEST pass=11 fail=0` (0) | same (0) | yes |
| 44 | `python3 tools/mori-pin-check.py --selftest` | `PIN_CHECK_SELFTEST pass=119 fail=0` (data) / `pass=114` (entering) | `PIN_CHECK_SELFTEST pass=119 fail=0` (0) | `PIN_CHECK_SELFTEST pass=114 fail=0` (0) | yes (each tip against its own pin) |
| 45 | `python3 .ufo/waves/round-47/count-c2.py --selftest` | `C2_SELFTEST pass=13 fail=0` | same line (0) | same (0) | yes |
| 46 | `python3 .ufo/waves/round-48/count-c1.py --selftest` | `C1_SELFTEST pass=34 fail=0` | same line (0) | same (0) | yes |
| 47 | `python3 .ufo/waves/round-48/count-c2.py --selftest` | `C2_SELFTEST pass=22 fail=0` | same line (0) | same (0) | yes |
| 48 | `python3 tools/mori-unlanded-check.py --selftest` | `UNLANDED_SELFTEST pass=17 fail=0` | same line (0) | same (0) | yes |
| 49 | `python3 .ufo/waves/round-49/count-c1.py --selftest` | `C1_SELFTEST pass=44 fail=0` | same line (0) | same (0) | yes |
| 50 | `python3 .ufo/waves/round-49/count-c2.py --selftest` | `C2_SELFTEST pass=26 fail=0` | same line (0) | same (0) | yes |
| 51 | `python3 .ufo/waves/round-50/count-c1.py --selftest` | `C1_SELFTEST pass=34 fail=0` | same line (0) | same (0) | yes |
| 52 | `python3 .ufo/waves/round-50/count-c2.py --selftest` | `C2_SELFTEST pass=31 fail=0` | same line (0) | same (0) | yes |

Wall time: 52 commands in ≈ 76 s at the data tip and ≈ 88 s at the entering tip; longest single command
`round-40/conform.py <REV> --selftest` at 57.6 s; the 900 s cap never fired.

## Appendix A — full tally lines shortened in the table

```
# rows 6, 9, 10, 11, 12 (data tip; entering tip byte-identical apart from ephemeral paths)
SELFTEST ok: pin_rc0,green_rc0_verdict_ok,absent_rc1_capability_absent,tool_drift_rc2,bad_want_rc1_mismatch,pack_drift_rc2
{"arms":49,"finding_id":"SELFTEST_OK","passed":49,"schema":"mori-seat-terminal-selftest-v1","tool_sha256":"de845692000e0318606562dd31877c9a64a88ee0117fa1f22cbc7d4220468af3"}
SELFTEST ok: green_rc0_and_manifest,capability_absent_rc1,mismatch_rc1,forbidden_key_rc1,seats_map_projection_rc0,a1_main_sessions_rc0,generated_fifo_rc0,symlink_ancestor_fifo_trap_rc2,unreadable_dirs_sandbox_rc0,root_symlink_rebase_rc0,key_metadata_required_rc1,wrong_type_metadata_rc1,pinned_snapshot_tamper_rc2,prefix_filter_rc0,files_scanned_falsifier_rc1,unreadable_fixture_rc0,fixture_drift_rc2,output_guard_rc2,nonempty_output_rc2
SELFTEST ok: guard_output_repo_root,guard_output_tools,guard_output_corpus,guard_output_git,guard_output_jj,guard_output_dotufo,guard_output_waves_allowed,guard_output_nonempty,guard_output_symlink,guard_output_ancestor_symlink,guard_scratch_ancestor_symlink,guard_output_ancestor,guard_output_gate_source,guard_scratch_tools,guard_scratch_input_file,guard_scratch_input_ancestor,guard_scratch_tmp,guard_scratch_ok,argv_output_symlink_rc2,argv_output_symlink_target_unchanged,argv_output_nested_symlink_rc2,argv_output_nested_symlink_target_unchanged,argv_scratch_symlink_rc2,argv_scratch_symlink_target_unchanged,argv_scratch_symlink_output_untouched,ok_rc0,ok_cases,ok_failed_zero,ok_mismatch_finding,ok_mismatch_severity,ok_exact_head,ok_exact_branch_tip,ok_mismatch_basis,ok_author_finding,ok_author_count,ok_sibling_negative,ok_fallback_head,ok_retained_false,ok_scratch_removed,keep_rc0,keep_retained_true,keep_scratch_present,wrongtip_rc1,wrongtip_names_branch_tip,head_rc1,head_names_missing_mismatch,head_failed_assertions,same_assertion_universe,absent_rc1,absent_capability_absent
{"arms": 12, "finding": "MORI_MISROOT_SELFTEST_OK", "fixture_bytes": 847, "fixture_sha256": "15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e", "planted_found_with_legacy_pathspec": false, "planted_found_without_pathspec": true, "planted_matched_in": ["path"], "poisoned_paths_absent": true, "sandbox_unchanged": true, "schema": "mori-misroot-sweep-v1"}
```

```
# row 5, data tip (the suffix is mktemp-random; entering tip: .../mori-r15-selftest-0r8zwzeo)
SELFTEST PASS selftest_root=/fast/scratch/hyaku/mori-r51/Mo51ExecSelftestSuite/data/.scratch/mori-r15-selftest-z7enapod
```

## Appendix B — anomalies and attribution

### B1 `mori-index-clean.sh --selftest`: the `not_a_repo` arm depends on `TMPDIR` being outside a git work tree

```
$ cd <clone>; TMPDIR=<clone>/.scratch bash tools/mori-index-clean.sh --selftest
MORI_INDEX_CLEAN_SELFTEST pass=3 fail=1
MORI_INDEX_CLEAN_SELFTEST_CASE not_a_repo rc=0 out=MORI_INDEX_CLEAN staged=0 intent_to_add=0   (stderr)
rc=1

$ cd <clone>; TMPDIR=<scratch>/tmp bash tools/mori-index-clean.sh --selftest
MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0
rc=0
```

Identical at `87e0c374` and `aa3af1ec` (tool bytes unchanged by the data commit). Cause: the selftest builds its
sandbox with `mktemp -d "${TMPDIR:-/tmp}/mori-index-clean.XXXXXX"`
(`tools/mori-index-clean.sh:147`) and asserts that `<sandbox>/notrepo` is *not* a repository (case 4, lines
204–210). With `TMPDIR` inside a git work tree, `git -C <sandbox>/notrepo` resolves to the enclosing repository,
so the tool prints `MORI_INDEX_CLEAN staged=0 intent_to_add=0` and exits 0 instead of 2 — the arm flips red.
This is the arrangement `mori-pin-check.py` uses for every registered selftest:
`tmp_parent = os.path.join(root, ".scratch")` (`tools/mori-pin-check.py:542`, comment 540–541 says lane tools
refuse a `TMPDIR` outside their lane root). The row carries no tally pin, so the reconciler never executes this
command (B3) and the C1 arms are unaffected; the registry cell still advertises the `not-a-repo` arm
(`SKILL.md:904`).

### B2 `conform.py` self-test cells omit the required `<rev>` positional

```
$ cd <clone>; python3 .ufo/waves/round-38/conform.py --selftest
conformance setup error: expected str, bytes or os.PathLike object, not NoneType   (stderr)
rc=2
$ cd <clone>; python3 .ufo/waves/round-39/conform.py --selftest      -> same message, rc=2
$ cd <clone>; python3 .ufo/waves/round-40/conform.py --selftest      -> same message, rc=2
```

Same at both tips. With the entry cell's revision supplied, all three are green:
`python3 .ufo/waves/round-38/conform.py <REV> --selftest` → `CONFORM_SELFTEST pass=6 fail=0` rc 0 (41.7 s);
`round-39` → `pass=9 fail=0` rc 0 (50.6 s); `round-40` → `pass=11 fail=0` rc 0 (57.6 s).
Cause: `main` accepts `rev` as `nargs="?"` (`round-40/conform.py:772`), routes `--selftest` to
`selftest(repo, rev, …)` (`:781`), and `selftest` calls `evaluate(repo, rev, …)` (`:754`) which puts `rev` into a
subprocess argv (`:573`) — `None` there produces the TypeError-shaped message instead of a usage error.
Only the `round-40` row carries a tally pin, and the reconciler resolves its command from the entry cell
(`python3 .ufo/waves/round-40/conform.py <rev> … --selftest`, with `<rev>` substituted), so the pinned tally is
still compared correctly; the `round-38`/`round-39` rows are unpinned and never executed by the reconciler.

### B3 which registered selftests the reconciler actually executes

`pin_commands` (`tools/mori-pin-check.py:432-449`) yields a binding only for a backticked `<PREFIX>SELFTEST`
tally span, and the run loop executes only bindings (`:801`). At the data commit 33 of the 59 self-test rows carry
such a pin (29 unique commands, 29 + 23 = the 52 unique command strings). The 23 command strings **never executed
by `mori-pin-check.py --rev`** cover 22 tools:

- shell: `mori-census.sh --selftest`, `mori-blind-check.sh --selftest`, `mori-index-clean.sh --selftest`;
- gate regressions and probes: `mori-round13-regressions.py`, `mori-round14-regressions.py`,
  `mori-round15-regressions.py`, `mori-round16-regressions.py`, `mori-round16-context-check.py`,
  `mori-journal-window.py`, `mori-seat-terminal.py`, `mori-round17-seat-regressions.py`,
  `mori-round17-jj-regressions.py`, `mori-misroot-sweep.py`, `mori-round17-context-check.py`,
  `mori-retention-gate.py`, `mori-freeze-order.py`, `mori-dispatch-ledger.py`, `mori-content-review.py`,
  `mori-retention-reconcile.py`;
- `.ufo/waves/round-38/conform.py` and `.ufo/waves/round-39/conform.py` (each with `--selftest`);
- `mori-evidence-loss.py` in both spellings (plain and `TMPDIR=$PWD/.scratch`) — the 23rd string.

`mori-source-drift.py` and `mori-sources-appendonly.py` are reached through their r37/r38 rows and are not in the
list, and `mori-silence-cases.sh` is pinned and executed. This is a named coverage limit of the C1 instrument, not
a change request.

### B4 `mori-blind-check.sh` stdout does not carry the counts its cell quotes

`bash tools/mori-blind-check.sh --selftest` prints exactly `PASS` (rc 0). The cell's expected
`scanned=14`/`blind_violations=13` are asserted against the tool's own summary inside `selftest()`
(`tools/mori-blind-check.sh:344`), not printed. Exit code and `PASS` match the pin; the two counts are not
observable from the output and the row has no tally pin (B3).

### B5 corroboration with the committed receipts

`.ufo/waves/round-51/evidence/selftests/mori-pin-check.txt` contains 119 `PASS` lines, the line
`PIN_CHECK_SELFTEST pass=119 fail=0` and `exit=0` — matching my `--selftest` run at `87e0c374` (119 PASS lines
counted in my stdout too). `…/mori-unlanded-check.txt` ends `UNLANDED_SELFTEST pass=17 fail=0` / `exit=0`,
matching row 48. `SHONEN.md` pins 119/119 for pin-check and 17/17 for unlanded in the data commit.

### B6 digest and line-count pins in self-test cells (all match at `87e0c374`)

`tools/mori-round14-regressions.py` → `533218a566030fda…`; `tools/mori-gate-registry.py` →
`8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` and 743 lines (`wc -l` = 743);
`.ufo/waves/round-45/count-c1.py` → `5f2deea0b35c…`; `count-c2.py` → `153423c48ca9…`;
`fixtures/mutants/count-c2.py` → `9850b3fcc888…`; `count-c3.py` → `37fd7c24ff52…`;
`fixtures/mutants/count-c3.py` → `69bf9b6eb29b…`.

## Named limits of this seat's check

- A green tally line is the instrument's own self-report. I executed the registered commands and compared their
  tallies; I did not audit every arm's assertion (the two anomalies above are the ones that surfaced).
- Measured in one `--no-local` clone under scratch at two commits, with `TMPDIR` inside the measured tree as the
  seat spec and `mori-pin-check.py` do; not the live lane worktree. `index-clean`'s `TMPDIR` sensitivity is shown
  by the two-run contrast, and no other command was re-run with an out-of-tree `TMPDIR`.
- One run per command per tip; no repetition for flakes. The 900 s cap never fired.
- Commands were run through `bash -c` so the registry cells' shell-isms (`mkdir -p .scratch &&`, `$PWD`,
  `TMPDIR=…`) mean what they say; `<scratch>` and `<REV>` are placeholders for my scratch paths and the measured
  revision.
- Findings below are observations of the current bytes; I do not propose a counter, predicate or kill-rule change
  (frozen), and none of these anomalies changes the C1 or C2 verdict as measured by the round's counters.

## Findings

- **MED** — `tools/mori-index-clean.sh:147` and `:204-210`: the `not_a_repo` selftest arm fails whenever `TMPDIR`
  lies inside a git work tree (sandbox `notrepo` resolves to the enclosing repo, `rc=0
  out=MORI_INDEX_CLEAN staged=0 intent_to_add=0`), so `--selftest` prints `pass=3 fail=1` rc 1 in exactly the
  `TMPDIR=<repo>/.scratch` arrangement `tools/mori-pin-check.py:542` uses; it passes 4/4 with `TMPDIR` outside a
  work tree. Pre-existing (identical at both tips), and invisible to C1 because the row at `SKILL.md:904` carries
  no tally pin and the reconciler never runs it.
- **LOW** — `SKILL.md:908`, `SKILL.md:910`, `SKILL.md:911` (rows `counter conformance (r38)`, `…v2 (r39)`,
  `…v3 (r40)`): the self-test cell writes `--selftest` alone, but the entry cells require the `<rev>` positional;
  taken literally the argv exits 2 with `conformance setup error: expected str, bytes or os.PathLike object, not
  NoneType` (`round-38/conform.py:220,275`, `round-39/conform.py:425,528`, `round-40/conform.py:738,754,781,573`)
  instead of a usage message. The reconciler supplies `<rev>` for the only pinned row (r40) and its
  `CONFORM_SELFTEST pass=11 fail=0` matched.
- **LOW** — `tools/mori-pin-check.py:432-449` and `:801`: only tally-pinned rows are executed, so 23 of the 52
  unique registered selftest commands (including `mori-census.sh`, `mori-blind-check.sh`, the r13–r17 gate
  regressions, the journal window, seat terminal, misroot sweep, retention gate, freeze-order, dispatch ledger,
  content review, evidence loss, retention reconcile, index clean and the r38/r39 conformance checkers — 23 command
  strings over 22 tools, B3) are never run by
  `mori-pin-check.py --rev`. Named limit of the instrument's coverage; no count/predicate change proposed.
- **LOW** — `SKILL.md:817` (blind-writer gate row): the cell quotes `scanned=14`/`blind_violations=13` as expected
  output, but `bash tools/mori-blind-check.sh --selftest` prints only `PASS`; the counts are internal assertions at
  `tools/mori-blind-check.sh:344`, unobservable from stdout, and the row is unpinned.
- **INFO** — 29/29 tally-pinned unique commands match their pins exactly at `87e0c374`, the same at
  `aa3af1ec`, except `mori-pin-check.py`'s own 114→119 step which matches each tip's own SKILL.md pin; the
  seven digest pins and the 743-line pin in self-test cells match their files, and the committed round-51
  selftest receipts for pin-check and unlanded check agree with my runs.
