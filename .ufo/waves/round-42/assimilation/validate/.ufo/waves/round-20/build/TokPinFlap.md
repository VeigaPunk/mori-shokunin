# TokPinFlap — C1 pin-vs-fresh lane-row flap (round 20)

Seat: MoriR20.TokPinFlap (leaf). Read-only. `tools/mori-census.sh` run exactly once (live, no args; job bg_339, 71.12 s; the census's own roll exited 1 = `MORI_CENSUS: DRIFT`, not a `--drift` result; stderr 0 bytes). No git/jj mutation, no lane file touched, no subagent, no selftest, no install (none needed).

## 1. Verdict

- **Two SURFACE lane rows differ** between the pin and the fresh run: `lane.mado` (progressing → not-open) and `lane.kagi` (not-open → young). Nothing else in the 62-line normalized block changed.
- **The L1's drift output is exactly the `lane.mado` flip alone.** Reproduced offline: `+path +reason -subject_commits -window basis round`. The `lane.kagi` flip (new round-25 launch at 10:23:21Z) happened after that drift's ledger snapshot, so the L1's run could not show it.
- **Every flapping field is live-state**, tied to two events: mado-shokunin commit `850b075` (ct 10:22:39Z) landing `.ufo/reports/round-21/mado.md` on master, and the watchdog ledger line `launch kagi round=25` (10:23:21Z). `round` is a comparator artifact (duplicate key), not a round change. **No census nondeterminism observed.** Code-level non-atomic capture points exist (§6); none fired.
- **The pin will keep flapping.** Predicted next: `lane.tameshi` → not-open once NOW ≥ 10:35:42Z (commit `7fd7c78`, `.ufo/reports/round-20/tameshi.md`). Time-driven gate expiries follow: tabi 11:47:50Z, kama 12:17:03Z, mori 12:18:05Z, kagi 12:23:21Z.

## 2. Inputs

| item | value | evidence |
|---|---|---|
| pin file | `/tmp/mori-r20/pin-probe.json`, sha256 `33027b82…`; identical to `evidence/c1-pin-probe-scratch.json` | `sha256sum` |
| pin NOW | `pinned_ts=2026-10-21T10:22:12Z` = epoch 1792578132 (census start) | pin header line 3 |
| pin write | mtime 10:23:18.568Z (07:23:18.568 -03). The task's "pinned at 10:23:18Z" is the write time; the census's NOW is 10:22:12Z | `stat` |
| fresh run | `bash tools/mori-census.sh`, ts=10:33:39Z (epoch 1792578819) | `build/TokPinFlap/census-fresh.out` line 1 |
| census script | sha256 `87b8d680…ab28` (unchanged) | `sha256sum` |

## 3. Normalized diff, pin vs fresh

Method: the census's own drift helpers were extracted verbatim (`tools/mori-census.sh` lines 2744–2772, 2776–2792, 2808–2918) and applied offline (`build/TokPinFlap/drift-offline.sh`) to the pin's canonical block and the captured fresh output. No second census run.

Full comparator result: `MORI_DRIFT: +gate_s +path +reason -path -subject_commits -window basis reason round` (rc 1).

Changed lines (`build/TokPinFlap/diff-pin-vs-fresh.txt`):
```
-SURFACE lane.kagi: not-open (lane=kagi round=<V> launch_epoch=<V> age_s=<V> basis=row-6 reason=committed-report round=<V> path=.ufo/reports/round-24/kagi.md; ts=<V>)
+SURFACE lane.kagi: young (lane=kagi round=<V> launch_epoch=<V> age_s=<V> basis=row-8 reason=age_le_gate gate_s=7200; ts=<V>)
-SURFACE lane.mado: progressing (lane=mado round=<V> launch_epoch=<V> age_s=<V> basis=row-A subject_commits=yes window=launch..NOW; ts=<V>)
+SURFACE lane.mado: not-open (lane=mado round=<V> launch_epoch=<V> age_s=<V> basis=row-6 reason=committed-report round=<V> path=.ufo/reports/round-21/mado.md; ts=<V>)
```

Counterfactuals (pin block with only the named row replaced by its fresh normalized line; `cf-*.block`):

| variant | comparator output |
|---|---|
| no-op (pin block unchanged) | `MORI_DRIFT: none` |
| mado only | `MORI_DRIFT: +path +reason -subject_commits -window basis round` (**identical to the L1 report**) |
| kagi only | `MORI_DRIFT: +gate_s -path basis reason round` |
| all rows (fresh run) | `MORI_DRIFT: +gate_s +path +reason -path -subject_commits -window basis reason round` |

Lane tallies: counted from the rows. Pin 12 progressing / 8 not-open / 3 young (the pin's silence counts are masked). Fresh 11 / 8 / 4, matching the fresh `SURFACE silence` line (`progressing=11 young=4 not_open=8 unavailable=0 silent=0`).

## 4. Timeline and cause (UTC; epochs; evidence)

| time | event | epoch | evidence |
|---|---|---|---|
| 10:22:12 | pin census NOW | 1792578132 | pin header |
| 10:22:39 | mado-shokunin commit `850b075` adds `.ufo/reports/round-21/mado.md` (and `.ufo/l0-questions.md`) to master | ct 1792578159 | `git log`, `git show --name-only 850b075`; `cat-file -e refs/heads/master:…` present |
| 10:22:55 | protocol `e291923` (MANIFEST.json only) | 1792578175 | `git log` |
| 10:23:18.57 | pin file written | 1792578198 | `stat` |
| 10:23:20 | kagi-shokunin `5034728` adds `.ufo/prompts/kagi-round-25.md` | ct 1792578200 | `git show --stat` |
| 10:23:21.68 | `watchdog.log:585` `launch kagi round=25` | 1792578201 | `grep -n` |
| 10:24:45 | protocol `8bf7f8a` (MANIFEST.json only, mado r21 closure note) | 1792578285 | `git log` |
| 10:33:39 | fresh census NOW | 1792578819 | `census-fresh.out` |
| 10:35:42 | tameshi-shokunin `7fd7c78` adds `.ufo/reports/round-20/tameshi.md` | ct 1792578942 | `git show --stat 7fd7c78` |

**mado (progressing → not-open).** `grade_lane` row-6 (`ps_report_closed`, census lines 2274–2289) asks `refs/heads/master` (root branch: `lane.branch` unset, HEAD → master) whether `.ufo/reports/round-21/mado.md` exists and whether its last-touch commit time lies in (LA_EPOCH, NOW]. LA_EPOCH = launch 04:49:56-03 = 1792568996. Pin NOW 1792578132 < ct 1792578159, so the pin correctly grades row-A. Fresh NOW ≥ ct, so row-6 wins. Row-6 runs before row-A (2409–2412 vs 2471–2475).

**kagi (not-open → young).** `ledger_anchor` keeps the last `launch kagi` line. Pin: round 24 (launch 02:43:10-03), closed by its committed round-24 report `1eed508` (ct 1792577229). Fresh: round 25, LA_EPOCH 1792578201, age 618 s ≤ gate 7200 → row-8 young (lines 2357–2377). The lane rows use the ledger copy read in `probe_silence` (lines 2513–2514). `probe_watchdog` also reads the ledger (line 783) for the state-lag findings, but only the `probe_silence` copy feeds `ledger_anchor`. The L1 drift's output has no kagi token, so its ledger snapshot preceded the 10:23:21.68Z line. [INFERENCE: the drift output carries no timestamp.] The journal probes are cheap on this host (one `journalctl --user -b … MESSAGE_ID=…` query measured at 0.03 s; the probe makes about 12 such queries), which suggests the `probe_silence` snapshot lands within seconds of NOW. [INFERENCE: other probes not timed.] The ~65 s of a run is probably mostly the 23-lane grading loop. [INFERENCE.] This reconciles the task's "~65 s later": the L1 drift started about 10:23:19, after the pin write at 10:23:18.57, and its result arrived about 65 s later. The bounds are [10:23:18.57, 10:23:21.68), and the start time is not logged.

Why the L1 drift saw mado but not kagi: git facts are read live in the lane loop, and commit times are bounded by NOW (lines 2287, 2459), so commit `850b075` (10:22:39) was visible. The ledger copy was taken at probe entry, before the 10:23:21 launch. This is as-of skew between rows, not nondeterminism.

## 5. Field classification

| token | flapped in | class | evidence |
|---|---|---|---|
| `+path` | mado (row-6 adds `path=`); kagi drops it (`-path`) | live-state | `850b075`; kagi launch 10:23:21; census line 2411 |
| `+reason` | mado | live-state | same row-6 template (line 2411) |
| `-subject_commits`, `-window` | mado (row-A keys disappear once row-6 closes) | live-state | row-6 precedes row-A (2409–2412 vs 2471–2475) |
| `basis` | mado row-A→row-6; kagi row-6→row-8 | live-state | row ids change with the grade |
| `reason` (value) | kagi `committed-report`→`age_le_gate` | live-state | young template, line 2377 |
| `+gate_s` | kagi young row | live-state | line 2377 |
| `round` | mado and kagi | comparator artifact, deterministic | row-4/row-6 emit `round=$LA_ROUND` in GL_EXTRA (2364, 2411) after the template's `round=${GL_ROUND}` (2545). `drift_scan` concatenates duplicate keys (2839–2840), so the masked value is `<V><V>` (verified: mado pin `<V>`, fresh `<V><V>`). Mado's round is 21 in both. No round number changed. |

No token changed without a corresponding ledger or ref event. None is classed census-nondeterminism.

## 6. Census-nondeterminism check

Only one fresh run was allowed, so repeatability was not tested. [INFERENCE: each row is a function of (ledger snapshot, root tip, NOW, state files, lane working tree).] Code points where the census is not NOW-consistent. None fired in the observed comparison:

- **Row-B** takes `mtime > LA_EPOCH` with no upper bound (2484–2487). A file written mid-run can move a lane between row-B and row-D. The count is masked, so only class flips show. Tsukuroi stayed row-B (`rowb_files=142` in the fresh run).
- **Row-7** reads `.ufo/state/<lane>.round` live per lane (2368), not from a snapshot.
- **Row-3** fires when a launch line lands after NOW but before the `probe_silence` snapshot (2358–2360). Its output is `young … basis=row-3 reason=launch-in-future` with `age_s=-`. The window is seconds.
- **Ledger snapshot** is not bounded by NOW, while git facts are. A single run can therefore mix instants (the L1 run: mado as of ≥10:22:39, kagi as of <10:23:21).

## 7. Drift-comparator properties relevant to C1 (verified offline)

- Tokens name fields, not lanes. `+path` does not say which lane. Attribution needs the line diff (§3).
- `round` is masked, so a relaunch that keeps the row class produces no token. A round advance is visible only through a change in row shape.
- Same-identity FINDING lines collapse when added or removed. `+FINDING:WATCHDOG_STATE_LAG` (13 such lines) or `+FINDING:WAVE_UNSETTLED_AGE` (10) names no lane or wave.

## 8. Implications for the L1 (C1)

- The pin is as of 10:22:12Z for lane rows, not 10:23:18Z. Its first post-pin row change was mado (10:22:39). Then kagi (10:23:21), and tameshi is predicted next. That is two observed row-changing events and one predicted within 13 minutes at the current commit rate, so any pin is stale within minutes.
- Classify each lane token against its event (commit SHA or ledger line), as in §4–§5. Treat `round` as the duplicate-key artifact.
- Time-driven flips need no commit: tabi 11:47:50Z, kama 12:17:03Z, mori 12:18:05Z, kagi 12:23:21Z (launch + 7200 s).
- The census roll `MORI_CENSUS: DRIFT` (findings=29, drift=11: 10 WAVE_UNSETTLED_AGE warnings plus WATCHDOG_ABSENT) is independent of the `--drift` rc.

## 9. Predicted, not observed

Tameshi: commit `7fd7c78` (ct 1792578942) adds `.ufo/reports/round-20/tameshi.md`. Tameshi's LA_EPOCH is 1792567996 (launch 04:33:16-03, round 20), so for any NOW ≥ 1792578942 the row-6 rule grades it not-open, as it did mado. [INFERENCE: outcome from the rule; census not re-run.]

## 10. Artifacts (`build/TokPinFlap/`)

- `census-fresh.out` (fresh census stdout, ts 10:33:39Z), `census-fresh.err` (empty).
- `drift-helpers-extracted.sh` (verbatim census helpers), `drift-offline.sh` (driver: `bash drift-offline.sh <pin> <captured> [diff-out]`).
- `diff-pin-vs-fresh.txt` (+ `.pin`, `.fresh`), `cf-none.block`, `cf-mado-only.block`, `cf-kagi-only.block` (+ `cf-*.txt`).

## 11. Unobserved / [INFERENCE] list

- The L1 drift's start and snapshot time (not logged). Bounded only by the output and code order.
- Repeat-run determinism (one run allowed).
- The tameshi outcome (§9).
- The row-3 and row-B transients (code-level only; not observed).
