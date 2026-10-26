# Mo50bExecSelftestReceipts — K4 selftest inventory (mori round 50, a2w1)

Seat: Mo50bExecSelftestReceipts (leaf executor). Lane: mori-shokunin. Data tip under test:
`487941b9395e89678af0053cc443cdb49cdee6e3` (rev-parse of `487941b^{commit}` reproduced below).
Lane rules honoured: read-only on the lane repo and fleet; no kernel-log MESSAGE text read; no OOM or
cgroup action; no pacman; no subagents. I wrote only this report file.

## 1. Environment and method

Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bExecSelftestReceipts/` (one `git archive` extract plus one
`git clone --shared`; both removed after this report was written).

Disk guard before the run (`bash scripts/hyaku/disk-guard.sh status`, exit 0): `/fast/scratch/hyaku` 24% used,
615.2G free; no ENOSPC.

Tool set: `grep -l -- '--selftest' tools/*.py tools/*.sh` in the extract → **35 tools** (31 `.py`,
4 `.sh`; list is table A). No file under `tools/fixtures/` matches `--selftest`.

Extract (primary environment, exactly as the assignment says):

```
$ git archive 487941b9395e89678af0053cc443cdb49cdee6e3 | tar -x -C /fast/scratch/hyaku/mori-r50/Mo50bExecSelftestReceipts/src
$ sha256sum src/tools/mori-sources-appendonly.py
75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 487941b...:tools/mori-sources-appendonly.py | sha256sum
75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b
```

Per tool: `cd src && TMPDIR=<scratch>/tmp timeout -k 10 900 <python3|bash> tools/<name> --selftest`,
stdout/stderr captured separately, exit code and wall time (`date +%s%N` around the process) recorded.
Four tools were run at a time. No run hit the 900 s cap (longest 21.185 s).

Primary-reading rules: the extract has no `.git`; `TMPDIR` is *outside* the extracted tree
(`.../tmp`), which is the wave's mandated scratch location. Diagnostics then re-ran the same tools
(a) with `TMPDIR` inside the extract and (b) inside the shared clone at R with `TMPDIR` inside/outside
the clone work tree, to separate environment constraints from real failures.

Clone: `git clone --shared --no-checkout ... clone && git checkout -q --detach 487941b939...`;
`git -C clone rev-parse HEAD` → `487941b9395e89678af0053cc443cdb49cdee6e3`.

## 2. Table A — all 35 `--selftest` tools, primary reading (git archive, TMPDIR outside the tree)

`rc` and `s` are the archive run; `clone rc` is the same command in the clone at R with in-tree TMPDIR.

| # | tool | command run | rc | wall s | last tally line | clone rc |
|---|---|---|---|---|---|---|
| 1 | mori-content-review.py | `python3 tools/mori-content-review.py --selftest` | 2 | 0.035 | `{"exit_code":2,"findings":[{"code":"CONTENT_REVIEW_SELFTEST_TMPDIR"}],"schema":"mori-content-review-result-v1","status":"could-not-evaluate"}` | 0 |
| 2 | mori-disk-rate.py | `python3 tools/mori-disk-rate.py --selftest` | 0 | 0.186 | `MORI_DISK_RATE_SELFTEST pass=14 fail=0` | 0 |
| 3 | mori-dispatch-ledger.py | `python3 tools/mori-dispatch-ledger.py --selftest` | 0 | 0.760 | `SELFTEST mori-dispatch-ledger PASS 14/14` | 0 |
| 4 | mori-evidence-loss.py | `python3 tools/mori-evidence-loss.py --selftest` | 0 | 0.167 | `{"checks":114,"failures":[],"finding_id":"mori-evidence-loss:audit:aggregator-r10:unresolved","passed":true,"schema":"mori-evidence-loss-selftest-v1"}` | 0 |
| 5 | mori-freeze-order.py | `python3 tools/mori-freeze-order.py --selftest` | 1 | 0.044 | `SELFTEST freeze-order FAIL 0/11` (stderr) | 0 |
| 6 | mori-gate-registry.py | `python3 tools/mori-gate-registry.py --selftest` | 0 | 0.287 | `GATE_REGISTRY_SELFTEST pass=15 fail=0` | 0 |
| 7 | mori-job-runway.py | `python3 tools/mori-job-runway.py --selftest` | 0 | 0.050 | `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` | 0 |
| 8 | mori-journal-window.py | `python3 tools/mori-journal-window.py --selftest` | 0 | 1.148 | `{"cases":16,"failed":0,"failures":[],"finding_id":"MORI_JOURNAL_WINDOW_SELFTEST","passed":16}` | 0 |
| 9 | mori-misroot-sweep.py | `python3 tools/mori-misroot-sweep.py --selftest` | 0 | 0.588 | `{"arms": 12, "finding": "MORI_MISROOT_SELFTEST_OK", ... , "schema": "mori-misroot-sweep-v1"}` (full line quoted in §3) | 0 |
| 10 | mori-oom-killers.py | `python3 tools/mori-oom-killers.py --selftest` | 0 | 0.043 | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` | 0 |
| 11 | mori-pin-check.py | `python3 tools/mori-pin-check.py --selftest` | 0 | 6.206 | `PIN_CHECK_SELFTEST pass=114 fail=0` | 0 |
| 12 | mori-pressure.py | `python3 tools/mori-pressure.py --selftest` | 0 | 0.048 | `MORI_PRESSURE_SELFTEST: PASS 12/12` (then `MATCHER: rejected 48/48 corrupted expectations`) | 0 |
| 13 | mori-retention-gate.py | `python3 tools/mori-retention-gate.py --selftest` | 2 | 0.048 | `SELFTEST retention-gate FAIL 0/21` | 0 |
| 14 | mori-retention-reconcile.py | `python3 tools/mori-retention-reconcile.py --selftest` | 0 | 0.274 | `{"finding_id":"RECONCILE_SELFTEST_PASS","passed":4,"privacy_clearance":false,"schema":"mori-retention-reconciliation-v2","total":4}` | 0 |
| 15 | mori-round13-regressions.py | `python3 tools/mori-round13-regressions.py --selftest` | 1 | 0.185 | `SELFTEST: fail pure=none cases=isolated-stub-target-red isolated-frozen-manifest-tamper` | 0 |
| 16 | mori-round14-regressions.py | `python3 tools/mori-round14-regressions.py --selftest` | 0 | 1.101 | `SELFTEST: pass checks=20 (parsers + real-gate red rc1/tamper rc2)` | 0 |
| 17 | mori-round15-regressions.py | `python3 tools/mori-round15-regressions.py --selftest` | 2 | 0.195 | `GATE ERROR exit=2` | 0 |
| 18 | mori-round16-context-check.py | `python3 tools/mori-round16-context-check.py --selftest` | 0 | 0.708 | `{"arms": 15, "claims_runtime_prevention": false, "finding_id": "SELFTEST_OK", "static_only": true}` | 0 |
| 19 | mori-round16-regressions.py | `python3 tools/mori-round16-regressions.py --selftest` | 0 | 4.794 | `SELFTEST ok: pin_rc0,green_rc0_verdict_ok,absent_rc1_capability_absent,tool_drift_rc2,bad_want_rc1_mismatch,pack_drift_rc2` | 0 |
| 20 | mori-round17-context-check.py | `python3 tools/mori-round17-context-check.py --selftest` | 0 | 1.482 | `{"arms": 31, "claims_runtime_prevention": false, "clauses_checked": 12, "finding_id": "SELFTEST_OK", "static_only": true}` | 0 |
| 21 | mori-round17-jj-regressions.py | `python3 tools/mori-round17-jj-regressions.py --selftest` | 0 | 5.628 | `SELFTEST ok: <50 arms, full line in §3>` | 0 |
| 22 | mori-round17-seat-regressions.py | `python3 tools/mori-round17-seat-regressions.py --selftest` | 0 | 1.871 | `SELFTEST ok: <19 arms, full line in §3>` | 0 |
| 23 | mori-round19-regressions.py | `python3 tools/mori-round19-regressions.py --selftest` | 2 | 0.043 | `R19_SELFTEST setup=explicit-lane-tmpdir-invalid` (stderr) | 0 |
| 24 | mori-round41-calibration.py | `python3 tools/mori-round41-calibration.py --selftest` | 0 | 0.214 | `MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0` | 0 |
| 25 | mori-routed-check.py | `python3 tools/mori-routed-check.py --selftest` | 0 | 0.280 | `ROUTED_CHECK_SELFTEST pass=20 fail=0` | 0 |
| 26 | mori-routed-r24.py | `python3 tools/mori-routed-r24.py --selftest` | 0 | 0.112 | `ROUTED_R24_SELFTEST pass=26 fail=0` | 0 |
| 27 | mori-seat-terminal.py | `python3 tools/mori-seat-terminal.py --selftest` | 0 | 2.495 | `{"arms":49,"finding_id":"SELFTEST_OK","passed":49,"schema":"mori-seat-terminal-selftest-v1","tool_sha256":"de845692000e0318606562dd31877c9a64a88ee0117fa1f22cbc7d4220468af3"}` | 0 |
| 28 | mori-source-drift.py | `python3 tools/mori-source-drift.py --selftest` | 0 | 4.576 | `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` | 0 |
| 29 | mori-sources-appendonly.py | `python3 tools/mori-sources-appendonly.py --selftest` | 0 | 1.885 | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | 0 |
| 30 | mori-unlanded-check.py | `python3 tools/mori-unlanded-check.py --selftest` | 0 | 0.181 | `UNLANDED_SELFTEST pass=17 fail=0` | 0 |
| 31 | mori-wave-settlement.py | `python3 tools/mori-wave-settlement.py --selftest` | 0 | 0.039 | `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)` | 0 |
| 32 | mori-blind-check.sh | `bash tools/mori-blind-check.sh --selftest` | 0 | 0.065 | `PASS` (no count token) | 0 |
| 33 | mori-census.sh | `bash tools/mori-census.sh --selftest` | 0 | 21.185 | `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` | 0 |
| 34 | mori-index-clean.sh | `bash tools/mori-index-clean.sh --selftest` | 0 | 0.062 | `MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0` | **1** (3/4; see §4.4) |
| 35 | mori-silence-cases.sh | `bash tools/mori-silence-cases.sh --selftest` | 0 | 0.626 | `MORI_SILENCE_CASES_SELFTEST pass=24 fail=0` | 0 |

Primary reading: **29/35 rc 0, 6/35 rc ≠ 0** (rows 1, 5, 13, 15, 17, 23). Serial-equivalent wall time
across the 35 runs ≈ 57.6 s (four at a time: 29.74 s). Command stdout/stderr was the only input; rc and
timings are from the harness loop above, not from the tools' self-reports.

### 3. Full long tally lines

```
mori-misroot-sweep.py:
{"arms": 12, "finding": "MORI_MISROOT_SELFTEST_OK", "fixture_bytes": 847, "fixture_sha256": "15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e", "planted_found_with_legacy_pathspec": false, "planted_found_without_pathspec": true, "planted_matched_in": ["path"], "poisoned_paths_absent": true, "sandbox_unchanged": true, "schema": "mori-misroot-sweep-v1"}

mori-round17-jj-regressions.py (50 arms):
SELFTEST ok: guard_output_repo_root,guard_output_tools,guard_output_corpus,guard_output_git,guard_output_jj,guard_output_dotufo,guard_output_waves_allowed,guard_output_nonempty,guard_output_symlink,guard_output_ancestor_symlink,guard_scratch_ancestor_symlink,guard_output_ancestor,guard_output_gate_source,guard_scratch_tools,guard_scratch_input_file,guard_scratch_input_ancestor,guard_scratch_tmp,guard_scratch_ok,argv_output_symlink_rc2,argv_output_symlink_target_unchanged,argv_output_nested_symlink_rc2,argv_output_nested_symlink_target_unchanged,argv_scratch_symlink_rc2,argv_scratch_symlink_target_unchanged,argv_scratch_symlink_output_untouched,ok_rc0,ok_cases,ok_failed_zero,ok_mismatch_finding,ok_mismatch_severity,ok_exact_head,ok_exact_branch_tip,ok_mismatch_basis,ok_author_finding,ok_author_count,ok_sibling_negative,ok_fallback_head,ok_retained_false,ok_scratch_removed,keep_rc0,keep_retained_true,keep_scratch_present,wrongtip_rc1,wrongtip_names_branch_tip,head_rc1,head_names_missing_mismatch,head_failed_assertions,same_assertion_universe,absent_rc1,absent_capability_absent

mori-round17-seat-regressions.py (19 arms):
SELFTEST ok: green_rc0_and_manifest,capability_absent_rc1,mismatch_rc1,forbidden_key_rc1,seats_map_projection_rc0,a1_main_sessions_rc0,generated_fifo_rc0,symlink_ancestor_fifo_trap_rc2,unreadable_dirs_sandbox_rc0,root_symlink_rebase_rc0,key_metadata_required_rc1,wrong_type_metadata_rc1,pinned_snapshot_tamper_rc2,prefix_filter_rc0,files_scanned_falsifier_rc1,unreadable_fixture_rc0,fixture_drift_rc2,output_guard_rc2,nonempty_output_rc2
```

## 4. The six non-zero primary runs — cause and diagnostic re-run

### 4.1 TMPDIR must be inside the repo root (4 tools)

`mori-content-review.py` (`selftest_tmpdir`, lines 355-368), `mori-freeze-order.py` (`_selftest`,
lines 497-514), `mori-retention-gate.py` (`selftest`, lines 457-468) and `mori-round19-regressions.py`
(`require_tmpdir`, lines 878-892) refuse a `TMPDIR` outside the tool's repo root. `mori-retention-gate.py`
is the strictest: it requires `TMPDIR` to resolve to exactly `<repo-root>/.scratch`.

Primary evidence (TMPDIR `.../tmp`, outside the extract):

```
$ TMPDIR=.../tmp python3 tools/mori-content-review.py --selftest
{"exit_code":2,"findings":[{"code":"CONTENT_REVIEW_SELFTEST_TMPDIR"}],...}   rc=2
$ TMPDIR=.../tmp python3 tools/mori-freeze-order.py --selftest
SELFTEST freeze-order FAIL 0/11                                               rc=1
$ TMPDIR=.../tmp python3 tools/mori-retention-gate.py --selftest
SELFTEST retention-gate FAIL 0/21                                             rc=2
$ TMPDIR=.../tmp python3 tools/mori-round19-regressions.py --selftest
R19_SELFTEST setup=explicit-lane-tmpdir-invalid                               rc=2
```

Diagnostic re-run with `TMPDIR` inside the extract (`src/.scratch-tmp`; `src/.scratch` for
retention-gate), still under `/fast/scratch/hyaku/mori-r50/...`:

```
content-review   -> {"exit_code":0,...,"status":"clean"}                      rc=0  0.507s
freeze-order     -> SELFTEST freeze-order PASS 12/12                          rc=0  0.903s
retention-gate   -> SELFTEST retention-gate PASS 21/21                        rc=0  1.207s
round19          -> R19_SELFTEST pass=25 fail=1 ; FAIL pinned-oracle-validates rc=1 0.096s
```

Round19's remaining arm is the git dependency: in the clone at R with `TMPDIR=clone/.scratch-tmp` it
prints `R19_SELFTEST pass=26 fail=0` (rc 0, 0.098 s). So the primary `rc=2` is an environment refusal,
not a broken instrument.

### 4.2 mori-round13-regressions.py — needs an enclosing git work tree

The two committed cases run the real gate with a fixed env (`PATH=/usr/bin:/bin`, `cwd=<temp root>`,
no `MORI_*` variables). Outside a git repository the gate stops before any verdict:

```
$ TMPDIR=<temp root outside any repo> PATH=/usr/bin:/bin python3 tools/mori-round13-regressions.py \
    --census <stub> --oracle <stub> --shonen <copy> --frozen-dir <none> --output <dir> --timeout 30 --jobs 1
mori-round13-regressions: setup: revision unavailable: git rev-parse failed and MORI_EVIDENCE_REVISION is unset
(a verdict must name its revision; set the env or run inside the lane repository)          rc=2
```

Hence the selftest prints, in the archive and with `TMPDIR` inside the archive:

```
SELFTEST: case isolated-stub-target-red bad rc=2!=1,missing:R13_C1_SYSTEM_NOTICE_COUNTS,no-GATE-line,no-evidence
SELFTEST: case isolated-frozen-manifest-tamper bad missing:R13_SNAPSHOT_TAMPERED,no-GATE-line,no-evidence
SELFTEST: fail pure=none cases=isolated-stub-target-red isolated-frozen-manifest-tamper     rc=1
```

In the clone (temp root lands inside the clone work tree) the same command prints
`SELFTEST: pass checks=33 cases=2` (rc 0, 2.023 s). The selftest therefore only passes when its temp
root is nested inside *some* git work tree — the operator's `/fast/scratch/hyaku/...` TMPDIR is not.

### 4.3 mori-round15-regressions.py — needs cwd inside a git work tree

`_selftest_run` (line 2166) runs the gate with the inherited cwd; the gate calls `git rev-parse HEAD`.
In the archive (cwd = extract, no `.git`) the transcript records
`GATE ERROR: git rev-parse HEAD failed rc=128: fatal: not a git repository ...` and the selftest ends
`SELFTEST ERROR: selftest invocation failed: rc=2 want=0; missing marker 'GATE PASS'` → `GATE ERROR
exit=2`, rc=2. In the clone the same command prints `SELFTEST PASS` (rc 0, 13.579 s). A normal lane run
starts the tool from the lane work tree, so this is an archive-only limitation.

### 4.4 mori-index-clean.sh — one non-hermetic arm (clone diagnostic only)

In the clone with `TMPDIR=clone/.scratch-tmp` (inside the clone work tree) the "not a repository" arm
fails because `git -C <sandbox>/notrepo status` walks up to the enclosing clone:

```
MORI_INDEX_CLEAN_SELFTEST_CASE not_a_repo rc=0 out=MORI_INDEX_CLEAN staged=0 intent_to_add=0
MORI_INDEX_CLEAN_SELFTEST pass=3 fail=1                                       rc=1
```

With `TMPDIR` outside any work tree (`.../tmp5`) the same clone command prints
`MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0` (rc 0, 0.057 s), exactly like the archive reading. The arm is
correct for the normal case; the clone result is a TMPDIR-placement artefact, reported so nobody reads a
3/4 as a tool regression.

## 5. Tally pins outside `SKILL.md`'s registry self-test cells

Scope: `SHONEN.md`, `corpus/QUALITY.md`, `corpus/README.md`, `PROVINCE.md`, `README.md`, `MANPAGE.md`
at R, for a backticked command containing `--selftest` followed by `(N/M)` or `pass=N`.
`PROVINCE.md`, top-level `README.md` and `MANPAGE.md` contain **no** `--selftest` occurrence
(`grep -c -- '--selftest'` → 0 for each). Pinned vs observed:

| # | file:line | pinned command / value | observed at R | verdict |
|---|---|---|---|---|
| 1 | `SHONEN.md:7` | `` `python3 tools/mori-pin-check.py --selftest` `` (114/114) | `PIN_CHECK_SELFTEST pass=114 fail=0`, rc 0 | **MATCH** |
| 2 | `SHONEN.md:7` | `` `python3 tools/mori-unlanded-check.py --selftest` `` (17/17) | `UNLANDED_SELFTEST pass=17 fail=0`, rc 0 | **MATCH** |
| 3 | `corpus/QUALITY.md:885` | `` `python3 .ufo/waves/round-38/conform.py --selftest` `` → `CONFORM_SELFTEST pass=6 fail=0` | as printed: `conformance setup error: expected str, bytes or os.PathLike object, not NoneType`, rc 2 | **NOT-RUNNABLE as printed** |
| 4 | `corpus/QUALITY.md:899-900` | `` `python3 .ufo/waves/round-38/conform.py <rev> --selftest --counter .ufo/waves/round-38/count-c1.py` `` → `pass=6 fail=0` | `CONFORM_SELFTEST pass=6 fail=0`, rc 0 (clone, rev `HEAD`=R) | **MATCH** |
| 5 | `corpus/QUALITY.md:909` | `` `python3 tools/mori-sources-appendonly.py --selftest` `` → `pass=12 fail=0` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, rc 0 | **STALE** (12 → 22) |
| 6 | `corpus/QUALITY.md:934` | `` `python3 .ufo/waves/round-42/conform.py <rev> --repo <lane> --contract .ufo/waves/round-39/contract.md --counter .ufo/waves/round-41/fixtures/c1/count-c8.py --selftest` `` → `CONFORM_SELFTEST pass=17 fail=0` | `CONFORM_SELFTEST pass=17 fail=0`, rc 0 (clone, rev `HEAD`=R, `--repo`=clone) | **MATCH** |
| 7 | `corpus/README.md:607` | `` `--selftest` `` → `pass=9 fail=0` (span has no command; the cell's checker is `.ufo/waves/round-39/conform.py`) | `CONFORM_SELFTEST pass=9 fail=0`, rc 0 (`conform.py HEAD --repo <clone> --counter .ufo/waves/round-39/count-c7.py --selftest`) | **MATCH** |
| 8 | `corpus/README.md:608` | `` `python3 tools/mori-sources-appendonly.py --selftest` `` → `pass=12 fail=0` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | **STALE** (12 → 22) |

Exact observed lines for the conform runs (§5 rows 3, 4, 6, 7), clone at R:

```
[bare]             conformance setup error: expected str, bytes or os.PathLike object, not NoneType   rc=2
[r38 + counters]   CONFORM_SELFTEST pass=6 fail=0                                                    rc=0
[r42 pinned form]  CONFORM_SELFTEST pass=17 fail=0                                                   rc=0
[r39 + counter]    CONFORM_SELFTEST pass=9 fail=0                                                    rc=0
```

### 5.1 Near-misses (same files, no `(N/M)` / `pass=N` token after the span) — reported so the class is not undercounted

| file:line | text | observed at R | reading |
|---|---|---|---|
| `corpus/QUALITY.md:588` | `` `bash .ufo/waves/round-30/check-blind-wave.sh --selftest` `` prints `PASS` | archive: `FAIL`, rc 1 (no git work tree); clone: `PASS`, rc 0, 0.293 s | MATCH in a checkout; NOT-RUNNABLE in a git archive |
| `corpus/QUALITY.md:833` | `` `--selftest` `` exits 0 (`mori-sources-appendonly.py`) | rc 0 | MATCH (no count) |
| `corpus/QUALITY.md:936` | `` `pass=14 fail=0` `` — describes the v4 checker mutant, not a command pin | not a pin | n/a |
| `corpus/README.md:579` | `` `python3 tools/mori-source-drift.py --selftest` `` — `PASS 4 cases at bf0df77` | `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` | STALE-at-R (4 → 6; the line is dated to `bf0df77`) |
| `corpus/README.md:580` | `Self-test PASS 8 cases` (no backticked `--selftest` span in the cell) | `pass=22 fail=0` | STALE-at-R (8 → 22) |
| `corpus/README.md:593` | `` `--selftest` `` 6 cases (`mori-source-drift.py`) | 6 cases | MATCH |
| `corpus/QUALITY.md:987-996` | code/help-string mentions (`no --selftest`, `add_argument("--verbose", help="see --selftest ...")`) — teaching text for the counter class | n/a | not pins |

Context for §5 rows 5 and 8: `corpus/QUALITY.md:1033-1034` records that `SKILL.md`'s cell pinned
`MORI_SOURCES_APPENDONLY_SELFTEST pass=15` through round 47 while the tool printed `pass=22` from
`d72ac167` on. The same stale `12` survives in `QUALITY.md:909` and `README.md:608` at R; the r39 table
value is dated, the QUALITY 112 "Check:" cell is not.

## 6. C1 receipts (cross-check only; counter not re-run)

At R, `.ufo/waves/round-50/evidence/selftests/`:

```
mori-pin-check.txt        PIN_CHECK_SELFTEST pass=114 fail=0    sha256 406c0be203ff9c715165971172ee577ed1486194c782597210336956015f4af9
mori-unlanded-check.txt   UNLANDED_SELFTEST pass=17 fail=0      sha256 392907ac94422e169119e0e0c249f5296c9c23deb01557a11f7d1eda62b1183a
```

Both receipt lines equal the tallies I observed from the archived bytes at R, and both SHONEN pins name
those receipts. `SHONEN.md` has 4 checklist boxes and 2 tally pins, consistent with C1's `pins=2 boxes=4`.

## 7. Limits (what this seat did not establish)

- No exit-code-only arm was judged good: a tally proves the instrument prints it at R on these inputs,
  not that its arms discriminate. Mutation quality was out of scope.
- The primary reading is a git-archive extract. Two tools (`round13`, `round15`) and one arm of a third
  (`index-clean`) read differently in a work-tree checkout; both readings are recorded, and neither is a
  statement about host behaviour.
- The conform pins were run at `rev=HEAD` in a shared clone at R, not at the round each cell was written
  in; a pin naming an older revision is marked "dated" where the cell says so.
- `grep` scope: only files named in the assignment. Other corpus files were not swept for pins.
- No host OOM/kill evidence was read (lane rule), and no system state was changed.

## 8. Findings

| # | severity | file / line concerned | finding |
|---|---|---|---|
| 1 | MED | `tools/mori-content-review.py:355-368`, `tools/mori-freeze-order.py:497-514`, `tools/mori-retention-gate.py:457-468`, `tools/mori-round19-regressions.py:878-892` | Four `--selftest` entries refuse a `TMPDIR` outside the tool's repo root (retention-gate requires exactly `<root>/.scratch`). Under the wave's mandated scratch location (`/fast/scratch/hyaku/mori-r50/<seat>/tmp`) they return rc 2/1 and print FAIL/setup codes: `CONTENT_REVIEW_SELFTEST_TMPDIR`, `SELFTEST freeze-order FAIL 0/11`, `SELFTEST retention-gate FAIL 0/21`, `R19_SELFTEST setup=explicit-lane-tmpdir-invalid`. All three TMPDIR-only tools pass when TMPDIR is moved inside the tree (12/12, 21/21, clean); round19 additionally needs the git store (26/26 in the clone). Not runnable as scoped for a real lane run, whose TMPDIR is outside the work tree. |
| 2 | MED | `tools/mori-round13-regressions.py` selftest (`run_isolated_case`, gate env/cwd) | The committed selftest cases can only pass when the temp root is nested inside a git work tree. In the archive and with a scratch TMPDIR the gate exits 2 with `revision unavailable: git rev-parse failed ... run inside the lane repository`; the selftest reports both cases bad (rc 1). In a clone it is 33 checks / 2 cases, rc 0. A K4-style run under the wave's scratch rule cannot get this tally. |
| 3 | MED | `corpus/QUALITY.md:909`; `corpus/README.md:608` | Pin `pass=12 fail=0` for `python3 tools/mori-sources-appendonly.py --selftest`; the tool prints `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` at R. Stale check cell (the same drift is recorded at `corpus/QUALITY.md:1033-1034` for `SKILL.md`, but not corrected in these two cells). |
| 4 | LOW | `tools/mori-index-clean.sh:195-201` | The "not a repository → 2" selftest arm is non-hermetic: it passes only when TMPDIR is outside any git work tree (archive 4/4; clone with in-tree TMPDIR 3/4, `MORI_INDEX_CLEAN_SELFTEST_CASE not_a_repo rc=0`; clone with outside TMPDIR 4/4), because git discovers the enclosing repository. |
| 5 | LOW | `corpus/QUALITY.md:885` | Pin `` `python3 .ufo/waves/round-38/conform.py --selftest` `` → `pass=6` is not runnable as printed: `conformance setup error: expected str, bytes or os.PathLike object, not NoneType`, rc 2. The runnable form at `corpus/QUALITY.md:899-900` prints `pass=6 fail=0` (MATCH). Documented in the adjacent QUALITY 111 row, so a known interface caveat rather than a new defect. |
| 6 | LOW | `corpus/README.md:579`, `corpus/README.md:580` | Dated counts drift at R: source-drift's "PASS 4 cases" → observed `PASS (6 cases)`; sources-appendonly's "Self-test PASS 8 cases" → observed `pass=22 fail=0`. Near-miss format (no `(N/M)`/`pass=N` token attached to the command). |
| 7 | LOW | `tools/mori-round15-regressions.py:2166-2186` | The selftest inherits cwd; outside a git work tree the nested gate exits 2 (`git rev-parse HEAD failed rc=128`) and the selftest prints `SELFTEST ERROR ... GATE ERROR exit=2` (rc 2). Fine in a lane checkout (rc 0, 13.579 s), unusable in a git archive. |
| 8 | LOW | `corpus/QUALITY.md:588` | Its check `bash .ufo/waves/round-30/check-blind-wave.sh --selftest` prints `PASS` only inside a git work tree (clone: PASS rc 0); in a git archive it prints `FAIL` rc 1 at the `git rev-parse --show-toplevel` guard. The surrounding text already explains older gate failures; the environment dependency is not stated. |

No HIGH finding. All 35 tools' `--selftest` entries print a successful tally in at least one environment
that satisfies their documented TMPDIR/git expectations, so no tool is dead; the defects are stale pins
(3, 5, 6) and environment coupling of the selftests (1, 2, 4, 7, 8).

## 9. Tooling

No tool was installed, upgraded or downgraded. No pacman transaction was attempted (host-wide pause).
Read-only git only (`archive`, `clone --shared`, `checkout` in the seat's own clone, `show`, `rev-parse`).

Scratch removal: `/fast/scratch/hyaku/mori-r50/Mo50bExecSelftestReceipts/` (extract, clone, TMPDIRs,
captures) was deleted after this file was written; no `/tmp` path is cited as evidence.
