# FamLaneRowsA: C1 falsification of `+path`, `age_s`, `basis`, `+reason`, `+gate_s`, `-example`

**Verdict: HOLDS.** All six classes are `live-state` and each cause re-derives from fleet state under unchanged census rules. Four rows carry incomplete or mislabeled pointers, one seat lead is wrong, and two residual blind spots need routing (section 4 to 6). None of these falsifies a class.

## 1. Scope, bounds, disclosure
- Rows checked in `corpus/evidence/drift-classification-r20.json`: `+gate_s` 145-149, `+path` 150-154, `+reason` 155-159, `-example` 223-227, `age_s` 248-252, `basis` 253-257. Receipt: `.ufo/waves/round-20/evidence/c1-drift-entering.json` (census `87b8d680...ab28`, 50 tokens).
- Read-only on fleet and lane. No mutating git or jj. No lane file edited. Scratch only in `.ufo/waves/round-20/falsify/FamLaneRowsA/`.
- `tools/mori-census.sh` was **not executed**. For section 3.3 I sourced scratch copies with the trailing `main "$@"` removed and called only `probe_silence` (the lane-row grader), with `MORI_TIMELINE_FILE` set to truncated copies of `.ufo/watchdog.log` and `MORI_NOW_EPOCH` fixed. Nothing was written to fleet or lane state.
- Seat reports (`build/TokPathAge.md`, `TokSilenceA.md`, `TokSilenceB.md`) were used as leads only. Every claim below was re-derived.
- Not read: `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`, `~/.omp`.
- Tooling: none installed or updated. Used existing git, awk, sha256sum, grep, date.

## 2. Verdicts
| Token | Class | Verdict | Re-derived cause (entering world) |
|---|---|---|---|
| `+path` | live-state | AGREE | kagi, kake, kengaku reach row-6 (census 2409-2411). Each anchor-round report is on master and its newest commit lies in (launch, NOW]: kagi r24 `1eed508` ct 1792577229 > launch 1792561390; kake r23 `4487889` ct 1792573299 > 1792564004; kengaku r26 `9a28017` ct 1792572867 > 1792560147. |
| `age_s` | live-state | AGREE | kumitate: `launch kumitate round=38` at watchdog.log:561 (04:04:24-03), then `complete kumitate round=38` at :579 (05:10:38-03). LA_CLOSED=1, so row-4 returns at 2363-2364 before `GL_AGE=$age` (2375). GL_AGE stays `'-'` (2295). The digits-only mask (2783) does not mask `-`. |
| `basis` | live-state | AGREE | Six matched arms change: aggregator B->A (commit 1bcf59e, section 3.4), kama A->8 (watchdog.log:583), kumitate A->4 (:579), kagi A->6 (:543 plus 1eed508), kake A->6 (:558 plus 4487889), kengaku A->6 (:541 plus 9a28017). |
| `+reason` | live-state | AGREE | `reason=` appears on exactly five matched lanes: kumitate row-4 (2364), kagi, kake, kengaku row-6 (2411), kama row-8 (2377). |
| `+gate_s` | live-state | AGREE | kama is the only matched row-8 lane. Age 117 s at NOW 10:19:00Z and 237 s at 10:21:00Z, gate 7200 (census 360, 2377). Relaunch at watchdog.log:583 = epoch 1792577823 (10:17:03Z). |
| `-example` | live-state | AGREE | aggregator row-B (`example=` at 2494) became row-A. Commit 1bcf59e (fleet root, author `aggregator-shokunin`, ct 1792459053) is the only aggregator-authored commit in (1792039857, NOW] under the root pathspec. Row-A is tested before row-B (2471 before 2477). |

## 3. Evidence

### 3.1 Census identity (rc 0 for every command)
- `sha256sum tools/mori-census.sh` = `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`. Matches receipt `census_sha256`.
- `git show 2061780117e6ca637725004897bd288d3ba7e988:tools/mori-census.sh | sha256sum` = `87b8d680...`. Measured commit exists (`cat-file -t` = commit). `merge-base --is-ancestor fe9fa90 2061780...` = ancestor.
- `git show 5be8943:tools/mori-census.sh | sha256sum` = `d7710981aa1c...`. Matches baseline line 2 (r10 pin).
- `git diff --stat 5be8943 HEAD -- tools/mori-census.sh`: 2027 insertions, 116 deletions. The file is not byte-identical since r10, so the "unchanged" claim must be scoped to the rows used by these tokens (done in 3.2).

### 3.2 Emitter identity, r10 (`5be8943`) vs HEAD
Normalized-line sha256, first 12 hex, r10 vs HEAD:
- `reason=ledger-close` (row-4 GL_EXTRA): r10 1312 / HEAD 2364, `7da88d88554b` = `7da88d88554b`
- `reason=age_le_gate` (row-8): r10 1325 / HEAD 2377, `8ba80f6cd050` = `8ba80f6cd050`
- `reason=committed-report` (row-6): r10 1340 / HEAD 2411, `4337521eeb15` = `4337521eeb15`
- `rowb_files=... example=` (row-B): r10 1401 / HEAD 2494, `f5ee137fd947` = `f5ee137fd947`
- `subject_commits=yes window=` (row-A): r10 1380 / HEAD 2473, `aaf9d6fb853c` = `aaf9d6fb853c`
- `GL_AGE` assignments (combined sha): r10 1269 and 1323 / HEAD 2295 and 2375, `29ef3f8a54a2` = `29ef3f8a54a2`
- `basis=${GL_BASIS}` (SURFACE lane line): r10 1439 / HEAD 2545, `7a3f5fe79e83` = `7a3f5fe79e83`
- Function bodies `ledger_anchor`, `probe_waves`, `probe_watchdog`: sha identical r10 vs HEAD (`6a6e74d356a6b5ef`, `c34c3839c994d784`, `9b0ff043ffba2189`).
- `ps_report_closed` differs (`76558d7f95cb8ee3` vs `986f29fec73ecbea`). Commit 273aa74 (r17) added the `rev` argument.
- `diff grade_lane.r10.txt grade_lane.head.txt` (147 vs 216 lines). Changes: r17 branch probe and `ref-unresolved` row-1 arm; `root_rev` and `rev` set to `refs/heads/<branch>`; pathspec placement; bash membership test equivalent to the old `grep -Fxq`; `git_cap` hardening. Decision branches for rows 4, 6 (except root_rev), 8, A and B, plus all reason strings, are unchanged. The rev change is inert for the six arms: rows 4 and 8 decide before any rev read, the root has no `.jj` and its HEAD is `refs/heads/master`, and no token-bearing lane is graded at row-9.
- `git log -S` on the census file: `committed-report`, `age_s=${GL_AGE}`, `gate_s=`, `row-8`, `row-4`, `path=.ufo`, `subject_commits=yes`, `age_le_gate`, `basis=${GL_BASIS}` all resolve to 1439c47 only (round-3). `example=` and `rowb_files` resolve to 1439c47 and 5be8943 (volatile-mask edit). `reason=ledger-close` resolves to 1439c47 and 5b62c89 (r4 close-tracking and selftest fixture; emitter text unchanged). So "emitter unchanged since r3" is true for emitted text. The r4 predicate change is pre-pin.
- Mask: r10 1659 and HEAD 2783 are `s/\bage_s=[0-9]+/age_s=<V>/g`. A `-` sentinel is not masked, so `age_s` shows as a changed value.

### 3.3 Harness re-derivation (lane grader only)
Ledger cuts: `watchdog-world-r10pin.log` = first 402 lines. Every line at or before 2026-10-15T19:26:29-03:00 is inside the cut, and none after it (crossover counts 0 and 0). `watchdog-world-entering.log` = first 584 lines. Line 585 (kagi round=25, 07:23:21-03) is post-receipt.

| Run | Code | Ledger | NOW | Lane rows for the nine baseline lanes |
|---|---|---|---|---|
| E1 | HEAD | r10 pin | 1792103189 (22:26:29Z) | protocol, kasegi, kengaku, kake, kumitate, kotoba, kagi, kama row-A; aggregator row-C (see R3) |
| E2 | r10 | r10 pin | same | identical to E1 |
| E3 | HEAD | entering | 1792577940 (10:19:00Z) | protocol, kasegi, kotoba row-A; aggregator row-A `subject_commits=yes`; kagi, kake, kengaku row-6 with `path=` round 24, 23, 26; kumitate row-4 `age_s=-` `reason=ledger-close`; kama row-8 `age_s=117 gate_s=7200` |
| E4 | r10 | entering | same | identical to E3 |
| E5 | HEAD | entering | 1792578060 (10:21:00Z) | same states; kama age 237 s |

- Lanes absent from the baseline (audio, chousa, game-dev-2d, game-dev-3d, kaidoku, kotodama, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi) are 14 lanes. They account for the 14 `+SURFACE:lane.*` tokens in the receipt. Their row-6 and row-8 fields do not create `+path`, `+reason` or `+gate_s` tokens, because those lines are added rather than matched.
- Conclusion: E3 equals E4, so no r10-to-HEAD code change alters any of these arms. The token causes are input-driven: ledger lines, report commits, one aggregator commit, and the clock.
- Saved outputs: `E1-head-r10pin-world.txt`, `E2-r10-r10pin-world.txt`, `E3-head-enter-1019.txt`, `E4-r10-enter-1019.txt`, `E5-head-enter-1021.txt`.

### 3.4 Pointer checks
Census (HEAD; r10 copy identical where noted):
- 360 `LANE_SILENCE_S=${MORI_LANE_SILENCE_S:-7200}`: holds.
- 2295 `GL_AGE='-'` (r10 1269): holds.
- 2363-2364 row-4 return (r10 1311-1312): holds.
- 2375 `GL_AGE=$age`, after the row-4 return: holds.
- 2377 row-8 `gate_s` (r10 1325): holds.
- 2409-2411 row-6 `path=` (r10 1338-1340): holds.
- 2471-2474 row-A (r10 1378-1381): holds. 2472-2473 are the emitted arm and `window=launch..NOW`.
- 2477-2496 row-B, with 2488 `example=$path` (r10 1395) and 2493-2494 (r10 1400-1401): holds.
- 2545 SURFACE lane emitter (r10 1439): holds.

Ledger, `.ufo/watchdog.log` (the TIMELINE_FILE default, mori-census.sh:301):
- 390 `launch aggregator round=10` at 2026-10-15T01:50:57-03 (aggregator LA_EPOCH 1792039857): holds.
- 541 `launch kengaku round=26` 02:22:27-03; 543 `launch kagi round=24` 02:43:10-03; 558 `launch kake round=23` 03:26:44-03: all hold.
- 561 `launch kumitate round=38` 04:04:24-03 (not cited by the classification): holds.
- 562 `launch kama round=20` 04:06:01-03, with no close line before 583 (see R2).
- 579 `complete kumitate round=38` 05:10:38-03: holds.
- 583 `launch kama round=21` 07:17:03-03: holds.
- 585 `launch kagi round=25` 07:23:21-03, post-receipt (see R1).

Baseline `corpus/evidence/baseline-r10-20261015T2231Z.json`:
- Line 2 census sha `d7710981...`: holds.
- Line 4 volatile list includes `age_s`, `example`, `rowb_files`, `round`: holds.
- Lines 13-21 are the nine lane rows: row-A everywhere except line 14 (aggregator, row-B: `rowb_files=<V> attribution=inference example=<V>`). Line 18 is kumitate row-A with `age_s=<V>`: holds.

Fleet root (`git -C /home/vgpnk/Projects/shokunin`, rc 0 throughout):
- `cat-file -e` at `HEAD` and `refs/heads/master` succeeds for `.ufo/reports/round-24/kagi.md`, `round-23/kake.md` and `round-26/kengaku.md`. `log -1 --format=%ct` gives `1eed508` 1792577229, `4487889` 1792573299 and `9a28017` 1792572867.
- `1bcf59e`: `show -s` gives 2026-10-19T22:17:33-03:00, author `aggregator-shokunin <aggregator@shokunin.local>`. It touches `LOG.md`, `README.md` and `SCORECARD.md`, which survive the root pathspec excludes.
- `git log --since=@1792039857 --author=aggregator-shokunin refs/heads/master -- . ':(exclude).ufo' ':(exclude,glob)**/*-shokunin/**'` returns only `1bcf59e 1792459053`.
- The census maps `protocol|aggregator` to `$ROOT` (`lane_repo`, 2009-2013). No `aggregator-shokunin` directory exists in the fleet root.

## 4. Defects to correct (pointer level; none changes a class)
- **D1 `-example`.** "aggregator-shokunin 1bcf59e" names a repository that does not exist. Replace with "fleet-root commit 1bcf59e (author aggregator-shokunin, 2026-10-19T22:17:33-03:00)".
- **D2 `basis`.** The aggregator arm cites no commit and no anchor. Add `1bcf59e` and watchdog.log:390.
- **D3 `age_s`.** Cites only the code early return. Add the cause lines watchdog.log:561 and :579, the mechanism lines 2295, 2545 and 2783, and baseline line 18.
- **D4 `+reason`.** Cites code only. Add watchdog.log:579 and :583 and report commits `1eed508`, `4487889`, `9a28017`.
- **D5 `+path`.** Add the three report commit ids.
- **D6 `basis` and `+reason`.** "Emitters unchanged since r3" is true for emitted text. Add that r4 (5b62c89) changed the row-4 close predicate (pre-pin) and r17 (273aa74) changed the row-6 and row-9 revision argument, which is inert for these arms (3.2).
- **D7 all six.** No baseline comparator pointer. Add baseline lines 13-21, with 14 for `example=` and `rowb_files=` and 18 for `age_s=<V>`.
- **D8 all live-state tokens.** No `future_flip`, although these tokens expire. Suggest: `+gate_s` and `basis` for kama and kagi flip at gate expiry (R4); `+path`, `basis`, `+reason` for kagi flip at the round-25 launch (R1).

## 5. Seat-lead correction
- `TokSilenceA.md` lines 35, 48 and 57 say kumitate went row-A to row-6 and emits `+path` and `-subject_commits` through row-6. That is wrong. Kumitate's row-4 test (2362-2364) precedes row-6 (2409), and E3 shows row-4. The JSON is right (`basis` and `age_s` say A to 4). Do not import the kumitate row-6 claim.
- `TokSilenceB.md` (aggregator row-A via 1bcf59e; `+gate_s` on kama; reason on five lanes) and `TokPathAge.md` (row-4 mechanism for `age_s`; row-6 for `+path`) both match E3.

## 6. Residual risks and blind spots
- **R1 (time-bound).** The entering state holds only while NOW is before 10:23:21Z, when kagi's round-25 launch (watchdog.log:585) takes over kagi's anchor. The re-pin already shows it: `baseline-r20-20261021T1051Z.json` line 22 has `kagi: young ... basis=row-8 reason=age_le_gate gate_s=7200`, pinned_ts 10:53:07Z. The receipt records "exact start second not recorded", so the upper bound is [INFERENCE] from wall time 103.98 s.
- **R2 (design residual, unchanged since r3).** Kama round 20 launched at 04:06:01-03 (watchdog.log:562). It has no `complete` or `lane-dead-no-report` line before the round-21 relaunch (583). `ledger_anchor` keeps only the last launch (byte-identical since r10), so the two-hour young state hides round 20. This is not a census regression under the C1 definition. The `+gate_s` and `basis` reasons should record it, and it should route as a design residual like M6.
- **R3 (harness limit).** The r10 aggregator row-B cannot be replayed, because row-B reads the live dirty set. E1 and E2 both give row-C. Baseline line 14 is the only evidence of row-B at pin. The six entering-state causes do not depend on it.
- **R4 (re-pin, not re-run).** Gate expiries fall at kama 12:17:03Z and kagi 12:23:21Z. "Post-pin drift none" can hold only until then [INFERENCE, not re-run].

## 7. Command log (all read-only; exit codes shown)
- `sha256sum tools/mori-census.sh`: rc 0, `87b8d680...`.
- `git show 5be8943:tools/mori-census.sh | sha256sum`: rc 0, `d7710981...`.
- `git log -S '<string>' -- tools/mori-census.sh` for the strings in 3.2: rc 0.
- `git merge-base --is-ancestor fe9fa90 2061780...`: rc 0.
- `git show 2061780...:tools/mori-census.sh | sha256sum`: rc 0, `87b8d680...`.
- `git -C /home/vgpnk/Projects/shokunin log --since=@1792039857 --author=aggregator-shokunin refs/heads/master -- . ':(exclude).ufo' ':(exclude,glob)**/*-shokunin/**'`: rc 0, `1bcf59e 1792459053` only.
- `ls -d /home/vgpnk/Projects/shokunin/aggregator-shokunin`: rc 2 (absent).
- Harness: `bash silence-probe-driver.sh census-*-stripped.sh` with `MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin`, E1 to E5 as in 3.3: rc 0 each.

## 8. Scratch artifacts (under `.ufo/waves/round-20/falsify/FamLaneRowsA/`)
- `census-head-copy.sh` (sha `87b8d680...`), `census-r10-5be8943.sh` (sha `d7710981...`), `census-head-stripped.sh`, `census-r10-stripped.sh`.
- `silence-probe-driver.sh`, `watchdog-world-r10pin.log` (402 lines), `watchdog-world-entering.log` (584 lines).
- `E1` to `E5` output files, `grade_lane.r10.txt`, `grade_lane.head.txt`.
