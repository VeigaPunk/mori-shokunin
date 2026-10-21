# TokWaves: C1 classification of `-FINDING:WAVE_UNSETTLED_AGE`

Seat: MoriR20.TokWaves (leaf). Entering tip 2061780; HEAD e4d9384. Census blob identical at both (sha256 `87b8d680…ab28`). Receipt: `.ufo/waves/round-20/evidence/c1-drift-entering.json` (50 tokens).

**Verdict: `live-state`.** The emitting path (`probe_waves` and its helpers) is byte-identical to the r10 pin. Two baseline wave lines lost their census inputs because the fleet's wave directories changed. One new aged wave took over one line's slot, which the drift pairing reports as token `obs`. This token does not block a re-pin by itself.

## A. Token row (JSON-ready)

| token | class | reason | evidence |
|---|---|---|---|
| -FINDING:WAVE_UNSETTLED_AGE | live-state | Census wave probe unchanged since r3 (identical to r10 pin); fleet changed: `aggregator-r10` and `aggregator-r10-resume` dirs emptied at 2026-10-18 23:56:16 -0300, so census empty branch stops emitting them; new aged wave `shokunin-train-20261016-w24` pairs with the `aggregator-r10` baseline line and surfaces as token `obs`. | E1-E9 |

```json
{
  "token": "-FINDING:WAVE_UNSETTLED_AGE",
  "class": "live-state",
  "reason": "Census wave probe and helpers are byte-identical to the r10 pin (last touched r1/r3); the fleet changed: aggregator-r10 and aggregator-r10-resume wave dirs were emptied at 2026-10-18 23:56:16 -0300 (both had dispatch.json on 2026-10-15), so the census empty branch no longer emits them; the new aged wave shokunin-train-20261016-w24 pairs with the aggregator-r10 baseline line and is reported as token obs.",
  "evidence": [
    "E1 tools/mori-census.sh:923 emit; :917-921 gates; :890-899 settle test; :907-915 age; :352 threshold 7200; :2703 call; HEAD sha256 87b8d680",
    "E2 corpus/evidence/baseline-r10-20261015T2231Z.json:26-27 (baseline lines); :2 census_sha256=d7710981 = sha256 of git show 5be8943:tools/mori-census.sh",
    "E3 git log -S WAVE_UNSETTLED_AGE --oneline -- tools/mori-census.sh -> 486a4e3, 7ca17b1; git blame -L 862,932 -> 7ca17b1, 486a4e3, 1439c47 (none after 5be8943)",
    "E4 function-level diff 5be8943..HEAD: probe_waves, emit_finding, emit_surface, cap, drift_report identical; drift_normalize adds boot= mask only",
    "E5 corpus/knowledge/observability-surfaces-r2.md:60-61 (2026-10-15T15:27:57Z: aggregator-r10 and -resume reg=0 disp=1 run=0)",
    "E6 find/stat on .ufo/waves: aggregator-r10 and -resume hold no regular files, dir mtime 2026-10-18 23:56:16 -0300; shokunin-train-20261016-w24 birth 2026-10-16 09:25:21 -0300, dispatch.json only",
    "E7 .ufo/waves/round-13/evidence/live-measurement.json (2026-10-20T04:33:08Z and :11Z): 10 aged names incl. w24, no aggregator-r10",
    "E8 build/TokWaves/predict-wave-tokens.py output: predicted WAVE tokens '-FINDING:WAVE_UNSETTLED_AGE obs', both in receipt tokens; +FINDING:WAVE_UNSETTLED_AGE absent",
    "E9 LOG.md:35-36 (wave-age clock provisional, carried debt); .ufo/waves/round-13/build/ReviewEvidence.md:67 (WAVE_UNSETTLED_AGE ids named as live-state tokens); .ufo/round-10/goal-wave/measurements-ledger.md:42-43 (x11 at r10 entering)"
  ]
}
```

## B. Census lines that emit it now (HEAD, `tools/mori-census.sh`)

- `:923` `emit_finding WAVE_UNSETTLED_AGE warn "wave=$base age_s=... settle=0"`. Reached only when:
  - `:917` has_settle=0 and `:919` registry|dispatch|run present;
  - `:921` `age > WAVE_UNSETTLED_S`; `:924` sets `st=drift`.
- Settle test `:890` (results.json | closeout.json | mission-result.json | closeout.md) and `:893-898` (typed `"closed"|"settled": true` or `"status": "closed"`).
- Age `:907` `find "$d" -type f -printf '%T@'`; `:914-915` age=0 unless a newest file exists, else NOW-newest.
- Empty branch `:926-927`: no registry/dispatch/run and not settled → `n_empty`, no emission.
- Threshold `:352` `WAVE_UNSETTLED_S=${MORI_WAVE_UNSETTLED_S:-7200}`. Call `:2703` (`run_census`). Surface `:931`.
- Contract text `:862-864`; finding id list `:258`.
- Counters (`empty`, `aged_unsettled`, `unsettled`, `reg`, `disp`, `run`, `settle`) are masked in drift via `DRIFT_COUNTER_KEYS` (`:2744-2764`), identical in the r10 baseline header.

Baseline emission: the same function at `5be8943:tools/mori-census.sh:712`. Its 11 lines are `corpus/evidence/baseline-r10-20261015T2231Z.json:26-36`. The removed ones are lines 26 (`aggregator-r10`) and 27 (`aggregator-r10-resume`).

## C. Introducing commits and unchanged path

- `git log -S WAVE_UNSETTLED_AGE --oneline -- tools/mori-census.sh`:
  - `486a4e3 round-1: scope cgroup and journal probes to fleet evidence; accept the host settlement tokens; correct the OOM headline`
  - `7ca17b1 round-1: land the observability census gate and the live receipt`
- `git blame -L 862,932`: emit `:923` and age `:914-915` from 7ca17b1; typed settle test `:885-899` from 486a4e3; locals `:867`, age read `:901-913` and `emit_surface` `:931` from 1439c47 (round-3). No line of the probe body comes from a commit after 5be8943 (r10 pin, 2026-10-15).
- Helpers by blame: WAVES_DIR `:303`, WAVE_UNSETTLED_S `:352`, NOW_EPOCH `:382-384`, emit_finding `:419-431`, emit_surface `:433-440`, cap `:561-566`, run_census `:2698-2704`. All from r1 (7ca17b1, 3d7aadc). VERSION `:281` (census-r6, 18d7d55) affects only the HEADER token.
- Function-level diff, 5be8943 vs HEAD: `probe_waves`, `emit_finding`, `emit_surface`, `cap`, `drift_scan`, `drift_line_id`, `drift_field_report`, `drift_report` IDENTICAL. `drift_normalize` adds one mask (`s/\bboot=…/boot=<V>/`), which no WAVE key uses.

## D. Live cause (fleet state; observed, not census)

| wave (baseline line) | r10 pin | now (2026-10-21 ~10:37Z) |
|---|---|---|
| aggregator-r10 (26) | aged; dir had dispatch.json at 2026-10-15T15:27:57Z (E5) | class=empty: no regular files, only an empty `seats/`; dir mtime 2026-10-18 23:56:16 -0300 (E6) |
| aggregator-r10-resume (27) | aged; disp=1 (E5) | class=empty: no entries; mtime 23:56:16.515 -0300; round-12 already found it empty (E10) |
| shokunin12h-20261014-p1..p5 (5 lines) | aged | still aged (exact baseline text) |
| shokunin-train-20261013, -w2, -w3, -w4 (4 lines) | aged | still aged (exact baseline text) |
| shokunin-train-20261016-w24 | not present (born 2026-10-16) | aged: dispatch.json only, newest file 2026-10-16 12:55:40 -0300, age 412904 s |

Predictor output (`build/TokWaves/predict-wave-tokens.py`, read-only; uses `wave-probe-replica.sh` and the census drift pairing):

```
baseline WAVE lines: 11
live AGED_UNSETTLED (now_epoch=1792579044): 10
removed from baseline: ['aggregator-r10', 'aggregator-r10-resume']
added vs baseline    : ['shokunin-train-20261016-w24']
predicted WAVE-family tokens: -FINDING:WAVE_UNSETTLED_AGE obs
all predicted tokens in receipt: True
-FINDING:WAVE_UNSETTLED_AGE in receipt: True
+FINDING:WAVE_UNSETTLED_AGE in receipt: False
obs in receipt: True
SURFACE:waves in receipt: False | predicted SURFACE waves state: drift
replica classes: ['AGED_UNSETTLED', 'empty', 'settled'] rows: 49
```

Mechanism: `drift_report` (`:2874-2918`) pairs baseline line 26 with the only unpaired new WAVE line (w24). The only differing key is `obs`, so the token is `obs`. Baseline line 27 has no partner, so it gives `-FINDING:WAVE_UNSETTLED_AGE`. There is no `+` token because the count of new lines (1) does not exceed the leftover baseline count (2). SURFACE waves stays `drift` because ten waves are still aged, so no `SURFACE:waves` token appears.

Timeline (local -0300 unless marked Z):
- 2026-10-15 15:27:57Z: both aggregator dirs have `disp=1` (E5).
- 2026-10-15 22:26:29Z: r10 pin, 11 WAVE lines.
- 2026-10-16 09:25: `shokunin-train-20261016-w24` created.
- 2026-10-18 23:56:16: aggregator-r10 and -resume emptied (same 24 ms window).
- Round-12 inspection (2026-10-19 by its own dating): `-resume` already empty (E10).
- 2026-10-20 04:33:08Z: round-13 live measurement, 10 aged names, no aggregator row (E7). The round-13 retained drift (started 04:33:14Z) already carries `-FINDING:WAVE_UNSETTLED_AGE` and `obs`.
- 2026-10-21 ~07:18 (10:18Z): entering receipt. 10:37Z replica: same 10 names.

Cause of the emptying: not recorded in `MANIFEST.json` or `.ufo/reports` (grep: no match). [INFERENCE] a hygiene removal; not established.

## E. Intent lines

- `LOG.md:35-36` (round-1 correction, 2026-10-15): "Carried debt: the wave-age clock is provisional (`WaveAgeMath`)."
- `tools/mori-census.sh:168-171` (r10 pin purpose): a behavioral baseline plus `--drift`, "so census behavioral drift is itself detected."
- `tools/mori-census.sh:862-864`: "Age = NOW - newest file mtime in the wave dir (observation only)"; "Never call unsettled 'failed'."
- `.ufo/waves/round-13/build/ReviewEvidence.md:67` (round-13 review, build doc): expected families include "live-state tokens treated as baseline aging (`other_authored_commits`, `WAVE_UNSETTLED_AGE` ids)."
- `.ufo/round-10/goal-wave/measurements-ledger.md:42-43`: `WAVE_UNSETTLED_AGE ×11` at r10 entering.
- `SCORECARD.md:13` (round 1): freshness "no drift pin yet", the gap the r10 pin closed.
- `.ufo/waves/round-13/build/SiblingOverlap.md:146` (build proposal): "empty-by-removal" vs "never-written" distinction. Not implemented: no such string in the census.

## F. Comparison with round-13 classification

Round-13 (`.ufo/waves/round-13/evidence/drift-classification.json:37`): `"[INFERENCE] current watchdog/wave/lane activity or finding context; no re-pin/admission claim"`.

- **Agree on the bucket.** Not a census-schema-change and not a census-regression. The round-13 review expected WAVE ids to be live-state (E9).
- **Disagree on basis and granularity.**
  - The round-13 label is not one of the four closed classes and carries no evidence pointer.
  - It does not identify the two concrete changes (two emptied waves, one new aged wave).
  - It misses that the new wave is reported under `obs`, so a register keyed only on the token would not show the w24 change.

## G. Related token and residual risks (not classified here)

- `obs` (receipt token, also round-13 `drift-classification.json:46` [INFERENCE]) has the same root cause. I did not classify it; the register owner should give it the same evidence. Its attribution to the WAVE pair is by the comparator algorithm and elimination (the other same-id candidate, WATCHDOG_ABSENT, has constant obs text, census `:830`). A full census run was out of bounds, so this is not run-verified end to end.
- Blind spot, by design and not drift: the census keeps no memory of earlier waves. A dispatched wave whose registry/dispatch/run files are removed becomes `empty` (`:927`), a masked counter. Only a `-FINDING` token reveals it. Changing this is a census change, outside C1.
- Age clock moves without a census change. For three waves I checked (p1-audit, shokunin-train-20261013, shokunin-train-20261016-w24), the newest-file times implied by the 2026-10-20 measurement are exactly 19200 s (5 h 20 min) later than today's listing. Unexplained. The `.ufo/waves` root mtime is 2026-10-21 06:56:45 -0300 (an entry added or removed; not identified). Membership and aged status are identical across both runs, and every aged wave exceeds 7200 s by at least 412,000 s, so no classification depends on it.

## H. Scope, bounds, disclosures

- Ran (read-only): `git log -S`, `git log`, `git blame`, `git show`, function-level extraction and diff; `find`/`stat` on `.ufo/waves`; reads of LOG.md, SCORECARD.md, `corpus/knowledge`, round-10/12/13 evidence and reports; a JSON query on round-13 evidence; the bash replica and python predictor (both write nothing to the fleet).
- Did not run `tools/mori-census.sh`, builds, tests, linters, or any subagent. No edits to the census, baselines, MANIFEST, lane state or git index. No mutating git commands.
- Disclosure: a repo-wide grep under `mori-shokunin` returned snippets from `.ufo/interactive-sessions/*.jsonl` transcripts. I did not open those files and cite nothing from them.
- Written: this report; `.ufo/waves/round-20/build/TokWaves/wave-probe-replica.sh`; `.ufo/waves/round-20/build/TokWaves/predict-wave-tokens.py`.
- Installs or updates: none. Used git, find, stat, bash and python3 as already installed; no pacman, uv or npm.
- Checks for the L1 (read-only): `python3 .ufo/waves/round-20/build/TokWaves/predict-wave-tokens.py` should reproduce section D. The function-level diff in section C should stay empty.
