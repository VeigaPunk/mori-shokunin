# Mo82E05Battery — standing battery receipt

## Result and axes

Axes: operability 7, freshness 5, depth 5, coverage 6, calibration 5, adjacency 6. This seat measures the standing battery, not an axis promotion or claim admission.

At committed round-82 dispatch tip **08e13729b60382e121956c461f4ad0fd9194553a**, the extended r81 runner returned **rc 2**, `BATTERY 60/64`, `BATTERY pass=60 setup=4 fail=0`. The four unavailable setup arms are unchanged from r81 (`57/61`, `pass=57 setup=4 fail=0`). The three additional passes are the r82 counter selftests: 4/0, 9/0, 5/0. No newly failing instrument was observed.

This is NOT an all-green receipt: the four setup refusals did not execute their case populations. No first failing behavioral case exists for those refusals; setup stops them before cases.

## Produced paths

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/evidence/battery-r82.txt`: full merged stdout/stderr, every instrument command and rc, and both battery summary lines. SHA256 `7f6b75de9e3e1f9d695068b4c292d6efa89a4263ee68e4950ad0d77c8e8b9d7b`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/w1/Mo82E05Battery.md`: this report.

No lane instrument or counter was edited. No tools installed or upgraded. No credentials/configuration/session material read. No LSP symbol operation was applicable (receipt-only assignment).

## Exact execution and reproducibility

Read-only lane inspection ran:

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin && git rev-parse HEAD && git log --oneline -4 && git status --porcelain | sed -n '1,25p'
```

It printed HEAD `08e13729b60382e121956c461f4ad0fd9194553a`; log subjects were dispatch/spec at `08e13729`, freeze at `20551e56`, r81 verifier at `ebcf2c72`, and pin-check at `142998f5`. Status showed modified `SCORECARD.md` and `corpus/QUALITY.md`, and untracked r82 ready/dispatch markers and `w1/`. Those in-flight working-tree edits were deliberately excluded: the receipt runs a clean **committed-tip shared clone**, not the concurrently edited live tree.

The initial clone invocation was rejected before execution because its requested cwd did not yet exist (`Working directory does not exist: /fast/scratch/hyaku/mori-r82/Mo82E05Battery`). The successful setup command, cwd `/fast/scratch`, was:

```sh
mkdir -p /fast/scratch/hyaku/mori-r82/Mo82E05Battery && git clone --quiet --shared /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r82/Mo82E05Battery/r82tip && git -C /fast/scratch/hyaku/mori-r82/Mo82E05Battery/r82tip rev-parse HEAD && git -C /fast/scratch/hyaku/mori-r82/Mo82E05Battery/r82tip rev-parse --show-toplevel
```

Output (rc 0):

```text
08e13729b60382e121956c461f4ad0fd9194553a
/fast/scratch/hyaku/mori-r82/Mo82E05Battery/r82tip
```

The scratch runner was written with the r81 runner bytes unchanged except insertion of these three lines immediately before its first `printf 'BATTERY %d/%d\n'`:

```sh
run 'round-82/count-c1.py --selftest' python3 -I .ufo/waves/round-82/count-c1.py --selftest
run 'round-82/count-c2.py --selftest' python3 -I .ufo/waves/round-82/count-c2.py --selftest
run 'round-82/count-c3.py --selftest' python3 -I .ufo/waves/round-82/count-c3.py --selftest
```

Reconstruction: copy the committed `.ufo/waves/round-81/battery.sh` into the clone at `.ufo/waves/round-82/battery.sh`, insert only those lines, then execute the command below. Keeping the same three-directory depth preserves the runner's original ROOT calculation; `--rev` overrides its historical default without changing the runner.

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/mori-r82/Mo82E05Battery bash /fast/scratch/hyaku/mori-r82/Mo82E05Battery/r82tip/.ufo/waves/round-82/battery.sh --rev 08e13729b60382e121956c461f4ad0fd9194553a
```

Executed using Python `subprocess.run` with exactly the argv above, cwd `/fast/scratch/hyaku/mori-r82/Mo82E05Battery/r82tip`, inherited environment plus the stated `HYAKU_SCRATCH`, `stdout=PIPE`, `stderr=STDOUT`, `text=True`, timeout 3500 seconds. The complete captured string was written through the file-write tool to the receipt path without filtering. Each child command and its output appears verbatim there; each has the original `timeout --kill-after=5s 120s` wrapper. Runner rc 2 was retained separately here.

## Coverage and per-instrument rc/tallies

The r81 runner discovers shell and Python instruments whose text contains `--selftest` in `tools/*.py tools/*.sh`; it does not enumerate every historical wave counter or every registry entry. It adds r80 C1/C3 revision runs and r81 C1/C2 selftests. This run discovered 57 instruments, plus those four standing counter entries and the three r82 additions, totaling 64. The table lists every executed instrument (and hence the complete discovered population). Tallies retain their native heterogeneous grammars; they are not summed into a fabricated case total.

| Instrument / mode | rc | Result/tally |
|---|---:|---|
| `tools/mori-anchor-check.py --selftest` | 0 | `ANCHOR_CHECK_SELFTEST: PASS (11 cases)` |
| `tools/mori-cgroup-pressure.py --selftest` | 0 | `MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0` |
| `tools/mori-claim-sweep.py --selftest` | 0 | `CLAIM_SWEEP_SELFTEST pass=30 fail=0` |
| `tools/mori-commit-runway.py --selftest` | 0 | `MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31` |
| `tools/mori-content-review.py --selftest` | 2 | `{"exit_code":2,"findings":[{"code":"CONTENT_REVIEW_SELFTEST_TMPDIR"}],"schema":"mori-content-review-result-v1","status":"could-not-evaluate"}` |
| `tools/mori-control-receipt.py --selftest` | 0 | `CONTROL_RECEIPT_SELFTEST pass=19 fail=0` |
| `tools/mori-counter-win.py --selftest` | 0 | `COUNTER_WIN_SELFTEST: PASS (12 cases)` |
| `tools/mori-disk-rate.py --selftest` | 0 | `MORI_DISK_RATE_SELFTEST pass=14 fail=0` |
| `tools/mori-dispatch-ledger.py --selftest` | 0 | `SELFTEST mori-dispatch-ledger PASS 14/14` |
| `tools/mori-drift-adjudicate.py --selftest` | 0 | `MORI_DRIFT_ADJUDICATE_SELFTEST: PASS (5 cases)` |
| `tools/mori-drift-recheck.py --selftest` | 0 | `MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)` |
| `tools/mori-driver-liveness.py --selftest` | 0 | `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0` |
| `tools/mori-entry-claims-check.py --selftest` | 0 | `ENTRYCLAIMS_SELFTEST pass=13 fail=0` |
| `tools/mori-events-context-win.py --selftest` | 0 | `EVENTS_CONTEXT_SELFTEST: PASS (10 cases)` |
| `tools/mori-evidence-loss.py --selftest` | 0 | `{"checks":114,"failures":[],"finding_id":"mori-evidence-loss:audit:aggregator-r10:unresolved","passed":true,"schema":"mori-evidence-loss-selftest-v1"}` |
| `tools/mori-freeze-order.py --selftest` | 1 | `SELFTEST freeze-order FAIL 0/11` |
| `tools/mori-gate-registry.py --selftest` | 0 | `GATE_REGISTRY_SELFTEST pass=15 fail=0` |
| `tools/mori-host-events-win.py --selftest` | 0 | `HOST_EVENTS_WIN_SELFTEST pass=10 fail=0` |
| `tools/mori-job-runway.py --selftest` | 0 | `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` |
| `tools/mori-journal-window.py --selftest` | 0 | `{"cases":16,"failed":0,"failures":[],"finding_id":"MORI_JOURNAL_WINDOW_SELFTEST","passed":16}` |
| `tools/mori-misroot-sweep.py --selftest` | 0 | `PASS; named arms retained in full receipt (no numeric tally inferred)` |
| `tools/mori-oom-killers.py --selftest` | 0 | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` |
| `tools/mori-pin-check.py --selftest` | 0 | `PIN_CHECK_SELFTEST pass=125 fail=0` |
| `tools/mori-pressure.py --selftest` | 0 | `MORI_PRESSURE_SELFTEST: PASS 12/12; MATCHER rejected 48/48` |
| `tools/mori-receipt-complete.py --selftest` | 0 | `RECEIPT_COMPLETE_SELFTEST pass=8 fail=0` |
| `tools/mori-record-sweep.py --selftest` | 0 | `RECORD_SWEEP_SELFTEST pass=26 fail=0` |
| `tools/mori-register-check.py --selftest` | 0 | `REGCHECK_SELFTEST pass=12 fail=0` |
| `tools/mori-retention-gate.py --selftest` | 2 | `SELFTEST retention-gate FAIL 0/21` |
| `tools/mori-retention-reconcile.py --selftest` | 0 | `{"finding_id":"RECONCILE_SELFTEST_PASS","passed":4,"privacy_clearance":false,"schema":"mori-retention-reconciliation-v2","total":4}` |
| `tools/mori-rotation-schedule.py --selftest` | 0 | `MORI_ROTATION_SCHEDULE_SELFTEST: PASS (13 cases)` |
| `tools/mori-round13-regressions.py --selftest` | 0 | `SELFTEST: pass checks=33 cases=2` |
| `tools/mori-round14-regressions.py --selftest` | 0 | `SELFTEST: pass checks=20 (parsers + real-gate red rc1/tamper rc2)` |
| `tools/mori-round15-regressions.py --selftest` | 0 | `SELFTEST PASS (scratch fixture path retained in receipt; fixture subsequently removed)` |
| `tools/mori-round16-context-check.py --selftest` | 0 | `{"arms": 15, "claims_runtime_prevention": false, "finding_id": "SELFTEST_OK", "static_only": true}` |
| `tools/mori-round16-regressions.py --selftest` | 0 | `SELFTEST ok: pin_rc0,green_rc0_verdict_ok,absent_rc1_capability_absent,tool_drift_rc2,bad_want_rc1_mismatch,pack_drift_rc2` |
| `tools/mori-round17-context-check.py --selftest` | 0 | `{"arms": 31, "claims_runtime_prevention": false, "clauses_checked": 12, "finding_id": "SELFTEST_OK", "static_only": true}` |
| `tools/mori-round17-jj-regressions.py --selftest` | 0 | `PASS; named arms retained in full receipt (no numeric tally inferred)` |
| `tools/mori-round17-seat-regressions.py --selftest` | 0 | `PASS; named arms retained in full receipt (no numeric tally inferred)` |
| `tools/mori-round19-regressions.py --selftest` | 2 | `R19_SELFTEST setup=explicit-lane-tmpdir-invalid` |
| `tools/mori-round41-calibration.py --selftest` | 0 | `MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0` |
| `tools/mori-routed-check.py --selftest` | 0 | `ROUTED_CHECK_SELFTEST pass=20 fail=0` |
| `tools/mori-routed-r24.py --selftest` | 0 | `ROUTED_R24_SELFTEST pass=26 fail=0` |
| `tools/mori-runway-win.py --selftest` | 0 | `RUNWAY_WIN_SELFTEST: PASS (9 cases)` |
| `tools/mori-seat-terminal.py --selftest` | 0 | `{"arms":49,"finding_id":"SELFTEST_OK","passed":49,"schema":"mori-seat-terminal-selftest-v1","tool_sha256":"de845692000e0318606562dd31877c9a64a88ee0117fa1f22cbc7d4220468af3"}` |
| `tools/mori-settlement-scan.py --selftest` | 0 | `SETSCAN_SELFTEST pass=10 fail=0` |
| `tools/mori-source-drift.py --selftest` | 0 | `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` |
| `tools/mori-sources-appendonly.py --selftest` | 0 | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` |
| `tools/mori-ua-variance.py --selftest` | 0 | `MORI_UA_VARIANCE_SELFTEST: PASS (14 cases)` |
| `tools/mori-unlanded-check.py --selftest` | 0 | `UNLANDED_SELFTEST pass=17 fail=0` |
| `tools/mori-uptime-win.py --selftest` | 0 | `UPTIME_WIN_SELFTEST: PASS (8 cases)` |
| `tools/mori-vote-bind.py --selftest` | 0 | `VOTE_BIND_SELFTEST pass=16 fail=0` |
| `tools/mori-wave-settlement.py --selftest` | 0 | `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)` |
| `tools/mori-workstate-win.py --selftest` | 0 | `WORKSTATE_WIN_SELFTEST: PASS (10 cases)` |
| `tools/mori-blind-check.sh --selftest` | 0 | `PASS` |
| `tools/mori-census.sh --selftest` | 0 | `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` |
| `tools/mori-index-clean.sh --selftest` | 0 | `MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0` |
| `tools/mori-silence-cases.sh --selftest` | 0 | `MORI_SILENCE_CASES_SELFTEST pass=24 fail=0` |
| `round-80/count-c1.py` | 0 | `C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=08e13729b603` |
| `round-80/count-c3.py` | 0 | `C3=met named=57 present=57 missing=0 extra=0 rev=08e13729b603` |
| `round-81/count-c1.py --selftest` | 0 | `C1_COUNTER_SELFTEST pass=8 fail=0` |
| `round-81/count-c2.py --selftest` | 0 | `C2_COUNTER_SELFTEST pass=21 fail=0` |
| `round-82/count-c1.py --selftest` | 0 | `C1_COUNTER_SELFTEST pass=4 fail=0` |
| `round-82/count-c2.py --selftest` | 0 | `C2_COUNTER_SELFTEST pass=9 fail=0` |
| `round-82/count-c3.py --selftest` | 0 | `C3_COUNTER_SELFTEST pass=5 fail=0` |

## Four setup findings (unchanged classification)

Commands below ran from the scratch checkout root with TMPDIR `/fast/scratch/hyaku/mori-r82/Mo82E05Battery/battery.hbRzPSXC/tmp` and HYAKU_SCRATCH its parent. Each is wrapped by `timeout --kill-after=5s 120s` in the full receipt. Source locations refer to committed `08e13729` bytes (not an unversioned assertion about later edits).

| Command | Source location under lane | First failing output / boundary | Classification |
|---|---|---|---|
| `python3 -I tools/mori-content-review.py --selftest` | `tools/mori-content-review.py:364-365` | rc 2, JSON finding `CONTENT_REVIEW_SELFTEST_TMPDIR`; TMPDIR must be beneath checkout | lane-scoped-scratch setup, unavailable |
| `python3 -I tools/mori-freeze-order.py --selftest` | `tools/mori-freeze-order.py:509-514` | rc 1, `SELFTEST freeze-order FAIL 0/11`; TMPDIR must be beneath checkout | lane-scoped-scratch setup, unavailable, despite rc 1 |
| `python3 -I tools/mori-retention-gate.py --selftest` | `tools/mori-retention-gate.py:459,467-468` | rc 2, `SELFTEST retention-gate FAIL 0/21`; TMPDIR must equal checkout/.scratch | lane-scoped-scratch setup, unavailable |
| `python3 -I tools/mori-round19-regressions.py --selftest` | `tools/mori-round19-regressions.py:888-891` | rc 2, `R19_SELFTEST setup=explicit-lane-tmpdir-invalid`; requires canonical checkout descendant | lane-scoped-scratch setup, unavailable |

The runner's exact-match setup classifications agree with the r81 receipt and source guards. No attempt was made to bypass these guards, create lane `.scratch`, or fix the instruments. Their unavailable populations are not counted as passed or stale (QUALITY 167).

## Limits, risks, and handoff

- This measures committed tip `08e13729`, **not** sibling uncommitted implementation edits or a later landed round-82 revision. In particular record-sweep here has `pass=26 fail=0`, not the proposed C3 revision-arm population. L1 must run the post-integration battery against its final committed input; this receipt cannot certify that future tree.
- The r82 additions are **selftests only**, not executions of P-C1/P-C2/P-C3 against a graded revision. No frozen claim is declared met from them.
- Existing four setup refusals remain real coverage gaps. No behavioral failures or additional defects in another seat's bytes were observed within this committed-tip battery. Uncommitted sibling bytes were not audited.
- No scalar score move, host health, exhaustive correctness, or external remediation is claimed. The historical runner is retained in the lane; the exact three-line extension and invocation above reconstruct this deleted scratch runner (FR9/D81-3 concern).
- Runner's EXIT trap removed its temporary battery directory. The seat's shared clone and scratch runner are removed before terminal handoff using the command below; the retained receipt and report are outside that cleanup root.

```sh
rm -rf -- /fast/scratch/hyaku/mori-r82/Mo82E05Battery
```

## Self-evaluation

Accuracy 4: all rc/tallies come from the retained output; committed-tip scope is explicit, not final integrated scope. Completeness 4: all 64 instruments listed, but four populations unavailable by existing setup policy. Clarity 4: full native output plus summary table; long named-arm lists stay in receipt. Actionability 4: extension and exact revision are reconstructible; L1 owns integrated gate execution. Conciseness 4: inventory is necessarily long. Overall 4.0; no score substitutes for admission. Most important improvement is the L1's later integrated-tip run, not an unauthorized rerun of in-flight sibling edits.
