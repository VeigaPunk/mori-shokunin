# Mo82E04C2Drift — C2 derived drift evidence

Date: 2026-11-04. Axes: operability, freshness, depth, coverage, calibration, adjacency. Scope: detection/report only.

## Produced files

- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/evidence/drift-r82-live.txt: both census outputs verbatim, each with run-start, cwd, command and rc.
- /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/drift-classification-r82.txt: 64 classifications in live order; 45 added-since-r10, 19 value-changed; no unexplainable entry.
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/w1/Mo82E04C2Drift.md: this derivation report.

SCORECARD.md, LOG.md, contract, baseline and census were not edited. No tool install/update, VCS mutation, service/configuration change, background job or subagent was performed.

## Executed commands and observed output

The throwaway runner executed this argv twice with cwd /home/vgpnk/Projects/shokunin/mori-shokunin:

```sh
bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json
```

TMPDIR was set to /fast/scratch/hyaku/mori-r82/Mo82E04C2Drift (not /tmp); no other environment override was introduced. Stdout and stderr were captured together without filtering. Each raw output is retained in the receipt above. Both runs exited 1. Run starts:

- 2026-11-04T07:45:13.552564+00:00
- 2026-11-04T07:45:34.131157+00:00

Both printed exactly:

```text
MORI_DRIFT: +FINDING:CGROUP_OOM_KILL_CUMULATIVE +FINDING:COREDUMP_NOTICE_JOURNAL_USER +FINDING:JOURNAL_CLASSES_UNMEASURED +FINDING:OOM_KILL_JOURNAL +FINDING:ROSTER_SET_MISMATCH +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER +FINDING:UNIT_FAILURE_JOURNAL +FINDING:UNIT_FAILURE_OUT_OF_SCOPE +FINDING:WATCHDOG_STATE_LAG +SURFACE:journal.system +SURFACE:journal.user +SURFACE:lane.audio +SURFACE:lane.chousa +SURFACE:lane.game-dev-2d +SURFACE:lane.game-dev-3d +SURFACE:lane.kaidoku +SURFACE:lane.kotodama +SURFACE:lane.lore +SURFACE:lane.mado +SURFACE:lane.mori +SURFACE:lane.revenger +SURFACE:lane.souji +SURFACE:lane.tabi +SURFACE:lane.tameshi +SURFACE:lane.tsukuroi +alarm_basis +attribution +conf_dropped_n +conf_n +gate_s +note +paths +positive_basis +positive_validation +process_sigkill +raw_basis +reason +repo +roster_n +roster_source +state_dropped_n +state_n +trust +user_positive_process_sigkill +user_positive_unit_signal +user_unit_signal -FINDING:SEGFAULT_JOURNAL -FINDING:WATCHDOG_STALE -FINDING:WAVE_UNSETTLED_AGE -SURFACE:journal -attribution -example -rowb_files -subject_commits -window HEADER age_s basis boot io_avg_unavailable launch_epoch obs round volatile_fields
```

Actual runner invocations, made through Python subprocess.run (capture_output=True, text=True, timeout=340):

```text
['python3', '-I', '/fast/scratch/hyaku/mori-r82/Mo82E04C2Drift/derive.py']
runner_rc 0
2026-11-04T07:45:13.552564+00:00 census_rc 1 tokens 64 {'added-since-r10': 45, 'value-changed': 19}

['bash', '-c', 'S=/fast/scratch/hyaku/mori-r82/Mo82E04C2Drift; trap 'rm -rf -- "$S"' EXIT; python3 -I "$S/derive.py"']
runner_rc 0
2026-11-04T07:45:34.131157+00:00 census_rc 1 tokens 64 {'added-since-r10': 45, 'value-changed': 19}
drift_line_byte_identical=True
```

Comparison was `first['drift_line'].encode() == second['drift_line'].encode()` over the complete MORI_DRIFT line (not a set or sorted list). It returned True. The classification was written between the two runs. The shell EXIT trap removed the exclusive scratch directory, including the deliberately throwaway runner; that path is not durable evidence or an active rerun dependency.

## Mechanical derivation and per-token evidence

Baseline SHA-256: `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478` (39 lines). The runner stripped leading +/- from each token, checked SURFACE ids only after the canonical marker, checked exact FINDING id prefixes, applied the special HEADER rule, and otherwise extracted whitespace-delimited keys using:

```python
re.findall(r'(?:^|\s)([A-Za-z0-9_]+)=', line)
```

This follows the frozen counter implementation and the L1's explicit precision instruction. A bare substring lookup would falsely match `note=` inside baseline line 5's `volatile_note=`; no such lookup was used. Thus +note and +paths are added, while +attribution, -attribution, and volatile_fields are value-changed. Each absent-id/key decision scanned all baseline lines (SURFACE limited to canonical lines). An absence has no matching evidence line; that negative result is stated rather than inventing a line.

Throwaway runner output (token, derived class, deciding evidence):

```text
+FINDING:CGROUP_OOM_KILL_CUMULATIVE	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); baseline FINDING id
+FINDING:COREDUMP_NOTICE_JOURNAL_USER	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); baseline FINDING id
+FINDING:JOURNAL_CLASSES_UNMEASURED	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); baseline FINDING id
+FINDING:OOM_KILL_JOURNAL	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); baseline FINDING id
+FINDING:ROSTER_SET_MISMATCH	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); baseline FINDING id
+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); baseline FINDING id
+FINDING:UNIT_FAILURE_JOURNAL	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); baseline FINDING id
+FINDING:UNIT_FAILURE_OUT_OF_SCOPE	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); baseline FINDING id
+FINDING:WATCHDOG_STATE_LAG	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); baseline FINDING id
+SURFACE:journal.system	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:journal.user	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.audio	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.chousa	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.game-dev-2d	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.game-dev-3d	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.kaidoku	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.kotodama	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.lore	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.mado	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.mori	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.revenger	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.souji	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.tabi	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.tameshi	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+SURFACE:lane.tsukuroi	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); canonical SURFACE id
+alarm_basis	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key alarm_basis=
+attribution	value-changed	baseline:14: SURFACE lane.aggregator: progressing (lane=aggregator round=<V> launch_epoch=<V> age_s=<V> basis=row-B rowb_files=<V> attribution=inference example=<V>; ts=<V>)
+conf_dropped_n	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key conf_dropped_n=
+conf_n	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key conf_n=
+gate_s	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key gate_s=
+note	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key note=
+paths	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key paths=
+positive_basis	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key positive_basis=
+positive_validation	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key positive_validation=
+process_sigkill	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key process_sigkill=
+raw_basis	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key raw_basis=
+reason	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key reason=
+repo	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key repo=
+roster_n	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key roster_n=
+roster_source	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key roster_source=
+state_dropped_n	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key state_dropped_n=
+state_n	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key state_n=
+trust	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key trust=
+user_positive_process_sigkill	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key user_positive_process_sigkill=
+user_positive_unit_signal	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key user_positive_unit_signal=
+user_unit_signal	added-since-r10	no matching evidence line in baseline (all 39 lines scanned); whitespace-delimited baseline key user_unit_signal=
-FINDING:SEGFAULT_JOURNAL	value-changed	baseline:38: FINDING SEGFAULT_JOURNAL severity=info obs=class=segfault count=<V> boot=current scope=user ts=<V> script_sha256=<V>
-FINDING:WATCHDOG_STALE	value-changed	baseline:24: FINDING WATCHDOG_STALE severity=warn obs=watchdog.log mtime_age_s=<V> threshold_s=900 path=/home/vgpnk/Projects/shokunin/.ufo/watchdog.log ts=<V> script_sha256=<V>
-FINDING:WAVE_UNSETTLED_AGE	value-changed	baseline:26: FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=aggregator-r10 age_s=<V> threshold_s=7200 reg=<V> disp=<V> run=<V> settle=<V> ts=<V> script_sha256=<V>
-SURFACE:journal	value-changed	baseline:10: SURFACE journal: drift (cmd=journalctl --user -b --no-pager; oom_kill=<V> kill_signal=<V> segfault=<V> unit_failure=<V> rc=0; ts=<V>)
-attribution	value-changed	baseline:14: SURFACE lane.aggregator: progressing (lane=aggregator round=<V> launch_epoch=<V> age_s=<V> basis=row-B rowb_files=<V> attribution=inference example=<V>; ts=<V>)
-example	value-changed	baseline:14: SURFACE lane.aggregator: progressing (lane=aggregator round=<V> launch_epoch=<V> age_s=<V> basis=row-B rowb_files=<V> attribution=inference example=<V>; ts=<V>)
-rowb_files	value-changed	baseline:14: SURFACE lane.aggregator: progressing (lane=aggregator round=<V> launch_epoch=<V> age_s=<V> basis=row-B rowb_files=<V> attribution=inference example=<V>; ts=<V>)
-subject_commits	value-changed	baseline:13: SURFACE lane.protocol: progressing (lane=protocol round=<V> launch_epoch=<V> age_s=<V> basis=row-A subject_commits=yes window=launch..NOW; ts=<V>)
-window	value-changed	baseline:13: SURFACE lane.protocol: progressing (lane=protocol round=<V> launch_epoch=<V> age_s=<V> basis=row-A subject_commits=yes window=launch..NOW; ts=<V>)
HEADER	value-changed	baseline:7: mori-census census-r5 — ts=<V> — mode=live — read-only; classification mandated by frozen HEADER rule
age_s	value-changed	baseline:8: SURFACE watchdog: drift (cmd=pgrep -af shokunin-watchdog; stat /home/vgpnk/Projects/shokunin/.ufo/watchdog.log; ls /home/vgpnk/Projects/shokunin/.ufo/state; pids=<V>; log=ok; age_s=<V>; stale_threshold_s=900; state_rounds=<V> state_rounds_max=<V> state_lag=<V> state_ahead=<V> state_cmp=<V> state_val_unreadable=<V> state_val_unread_reasons=<V>; ts=<V>)
basis	value-changed	baseline:13: SURFACE lane.protocol: progressing (lane=protocol round=<V> launch_epoch=<V> age_s=<V> basis=row-A subject_commits=yes window=launch..NOW; ts=<V>)
boot	value-changed	baseline:37: FINDING KILL_SIGNAL_JOURNAL severity=warn obs=class=kill_signal count=<V> boot=current scope=user ts=<V> script_sha256=<V>
io_avg_unavailable	value-changed	baseline:12: SURFACE disk: ok (cmd=df -P; targets=/home/vgpnk/Projects/shokunin /tmp; warn_pct=85 crit_pct=95; io_basis=since-boot io_avg_since_boot=dm-0:<V>Bps/<V>s io_avg_unavailable=tmpfs:not-a-block-device; ts=<V>)
launch_epoch	value-changed	baseline:13: SURFACE lane.protocol: progressing (lane=protocol round=<V> launch_epoch=<V> age_s=<V> basis=row-A subject_commits=yes window=launch..NOW; ts=<V>)
obs	value-changed	baseline:24: FINDING WATCHDOG_STALE severity=warn obs=watchdog.log mtime_age_s=<V> threshold_s=900 path=/home/vgpnk/Projects/shokunin/.ufo/watchdog.log ts=<V> script_sha256=<V>
round	value-changed	baseline:13: SURFACE lane.protocol: progressing (lane=protocol round=<V> launch_epoch=<V> age_s=<V> basis=row-A subject_commits=yes window=launch..NOW; ts=<V>)
volatile_fields	value-changed	baseline:4: # volatile_fields=ts age_s mtime_age_s *_epoch mem_peak_anchor psi_some_avg10 psi_full_avg10 io_avg_since_boot state_val_unread_reasons script_sha256 example age_unreadable aged_unsettled avail count current disp drift empty findings foreign freshness_unavailable has_head high host_mem_avail_pct idle idle_s kill_signal ledger_round local_oom_kill max mem_fill_pct mem_peak not_open oom oom_kill other_authored_commits pids probed progressing progressing_weak reg relevant round rowb_files run segfault sessions settle settled silent size skipped state_ahead state_cmp state_lag state_round state_rounds state_rounds_max state_val_unreadable surfaces total unclassified unit_failure unavailable unsettled used used_pct young
```

## Verification boundaries, risks and handoff

Verified only the assignment's explicitly requested live measurements and token-list comparison. No build, lint, formatter, selftest, mutation battery or C2 keeper was run. The L1 should run `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/count-c2.py <landed-revision>` after integration; retirement/cell updates belong to the L1 and are not certified here. These are mutable worktree/live-host readings, not claimed measurements of a committed revision. Two identical token lists do not guarantee future host-state invariance. Classification is structural baseline membership, not a causal explanation or approval to re-pin, remove evidence, or remediate host state.

No additional independently established defect in another seat's bytes is asserted. Noted precision discrepancy: the contract's shorthand “<key>= occurs” must be read with the frozen counter's whitespace-key grammar (`.ufo/waves/round-82/count-c2.py:46,61,64-73`), as explicitly resolved by L1; this report does not amend the frozen contract. LSP tools were unavailable in the exposed tool inventory; no implementation-symbol refactor was needed.

Self-assessment: accuracy 4 (live readings, not committed-revision proof); completeness 4 (seat outputs complete, integrated C2 predicate deliberately unrun); clarity 4 (all 64 decisions retained, necessarily long); actionability 4 (L1 landed-revision keeper still required); conciseness 4 (raw output is duplicated intentionally for exact-command evidence). Overall 4.0. Improvement: integrate and measure the final revision with the parent-owned keeper; the scope boundary prevents claiming it here.
