# TokPathAge — C1 token classification: `+path` and `age_s`

Seat: MoriR20.TokPathAge · 2026-10-21 · leaf, read-only, no census run (bounds).
Inputs: `.ufo/waves/round-20/evidence/c1-drift-entering.json` (rc 1, 50 tokens, census sha `87b8d680…ab28`, measured commit `2061780`), baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` (census `d7710981…`, census-r5, pinned 2026-10-15T22:26:29Z), prior register `.ufo/waves/round-13/evidence/drift-classification.json`.
Method: offline reconstruction of `--drift` (algorithm read at `tools/mori-census.sh:2805-3002`; never executed) + live read-only state checks + the L1 witness capture `.ufo/waves/round-20/evidence/c1-pin-probe-scratch.json` (same census sha, pinned 2026-10-21T10:22:12Z, full canonical output). No tools installed (none needed).

## Drift token grammar (observed, `tools/mori-census.sh`)

`drift_line_id` :2808-2818 (SURFACE/FINDING keep id; header/verdict are singletons) → pass 1 exact-line match :2881-2890 → pass 2 same-id field diff :2891-2901 (`drift_field_report` :2849-2867: changed value names `key`, removed `-key`, added `+key`, no field change names the line id) → pass 3 `+id` :2908 → `sort -u` :2916. Volatile masking is integer-only per key (`drift_normalize` :2776-2791, e.g. `s/\bage_s=[0-9]+/age_s=<V>/g` :2783); the baseline volatile list is compared as a contract (`run_drift` :2981).

## Result table (JSON-ready)

```json
[
  {
    "token": "+path",
    "class": "live-state",
    "reason": "Field ADDED on matched SURFACE:lane.* pairs: kengaku r26, kake r23 and kagi r24 reports became committed at fleet HEAD inside (launch, now], so grade_lane grades row-6 whose GL_EXTRA emits path=.ufo/reports/round-N/<lane>.md. The emitting census line is byte-identical to the r10 census (introduced 1439c47 round-3, BEFORE the r10 pin; git log -S 'reason=committed-report' -> only 1439c47), so no census logic change and no regression; what changed is fleet state (rounds closed). Row-1 'reason=ledger-unreadable path=' (:2301) is ruled out: it would add a state_ledger=unreadable field token, absent from the receipt.",
    "evidence": "emit: tools/mori-census.sh:2411 (row-6 GL_EXTRA), surfaced via :2545; r10 copy .ufo/waves/round-20/build/TokSilenceB/census-r10-5be8943.sh:1340 identical; baseline corpus/evidence/baseline-r10-20261015T2231Z.json has path= only on :24 (FINDING WATCHDOG_STALE), none on lane lines :13-21; commit 1439c47 2026-10-15 round-3; live: git cat-file -e HEAD:.ufo/reports/round-{26,23,24}/{kengaku,kake,kagi}.md rc 0 with last-touch ct 1792572867/1792573299/1792577229, all in-window at the 07:19:49-03 drift; witness c1-pin-probe-scratch.json: 'SURFACE lane.kengaku: not-open (... basis=row-6 reason=committed-report round=<V> path=.ufo/reports/round-26/kengaku.md)'; intent: corpus/knowledge/silence-cutover-r3.md:43, corpus/knowledge/drift-pin-r10.md:50, census header :195-198 and :2730-2731"
  },
  {
    "token": "age_s",
    "class": "live-state",
    "reason": "Changed VALUE on the matched SURFACE:lane.kumitate pair: a ledger 'complete kumitate round=38' line (2026-10-21T05:10:38-03) postdates the anchor launch (04:04:24, same round), so ledger_anchor sets LA_CLOSED=1 and grade_lane returns at row-4 (reason=ledger-close) BEFORE GL_AGE=$age is assigned; the lane line therefore emits the GL_AGE default '-' where the baseline had a masked integer age_s=<V>. The sed mask covers integers only, so the '-' sentinel is compared and named bare 'age_s' - exactly the documented behavior (masking suppresses magnitudes only, never token existence). All emitting lines predate r10 (template 1439c47 round-3; watchdog sentinel 7ca17b1 round-1; row-4 close tracking 5b62c89 round-4; git log -S 'age_s=${GL_AGE}' -> only 1439c47): no census change, no regression; a kumitate round completion is the live event.",
    "evidence": "emit: tools/mori-census.sh:2545 (age_s=${GL_AGE}), :2295 (GL_AGE='-'), :2363-2364 (row-4 return before :2375 GL_AGE=$age), :2084-2113 (ledger_anchor complete|wrap -> LA_CLOSED); baseline :4 (volatile list), :13-21 (age_s=<V> lane rows); ledger /home/vgpnk/Projects/shokunin/.ufo/watchdog.log: '2026-10-21T04:04:24-03:00 launch kumitate round=38' + '2026-10-21T05:10:38-03:00 complete kumitate round=38'; witness c1-pin-probe-scratch.json: 'SURFACE lane.kumitate: not-open (lane=kumitate round=<V> launch_epoch=<V> age_s=- basis=row-4 reason=ledger-close round=<V>)'; intent: corpus/knowledge/verdict-machine-r4.md:261-287, corpus/knowledge/drift-pin-r10.md:50, baseline volatile_note line 5"
  }
]
```

## Mechanism reconstruction (validation)

Row map of the nine baseline lanes at the drift run (reconstructed from live ledger/git + 10:22 witness; all transitions complete before 07:19:49-03): kumitate row-A→**row-4** (complete line) → contributes `age_s`, `basis`, `+reason`, `-subject_commits`, `-window`, `round` (row-4 repeats the `round=` key, so drift_scan concatenates `<V><V>` vs baseline `<V>`); kengaku/kake/kagi row-A→**row-6** (committed reports) → `+path`, `+reason`, `-subject_commits`, `-window`, `round`, `basis`; kama row-A→**row-8** young (launch 07:17:03 < drift) → `+gate_s`, `+reason`, `-subject_commits`, `-window`, `basis`; aggregator row-B→row-A → `+subject_commits`, `+window`, `-rowb_files`, `-attribution`, `-example`; protocol/kasegi/kotoba row-A→row-A byte-identical. That is 13 field tokens; adding silence-surface r12 roster fields (+roster_n +roster_source +conf_n +conf_dropped_n +state_n +state_dropped_n), 9 journal line-tokens, live line-tokens (-FINDING:WATCHDOG_STALE fresh log ~166s; +FINDING:WATCHDOG_STATE_LAG, 13+ lines; `obs` and -FINDING:WAVE_UNSETTLED_AGE from aggregator-r10/-resume settled while shokunin-train-20261016-w24 aged in), +FINDING:ROSTER_SET_MISMATCH, 14 new lane surfaces, volatile_fields (boot key added 18d7d55), HEADER (census-r5→census-r6), io_avg_unavailable (disk device set now includes nvme0n1p1) = **50/50 receipt tokens accounted**. No token requires a census-regression explanation.

## Comparison with the round-13 register

- The r13 register (42 tokens, measured at `c13df48`, 2026-10-20T04:33Z against the SAME r10 baseline) contains **no entry for `+path` or `age_s`** — those tokens did not occur in its comparison (no matched lane was row-4/row-6 then, and the r14/r15 journal findings did not exist yet). So there is no direct older classification to agree or disagree with for my two tokens.
- **Agree** in kind: r13 classed the same mechanism family (lane-row live transitions: `+gate_s`, `+reason`, `basis`, `±subject_commits`, `±window`, `-rowb_files/-attribution/-example`) as "current watchdog/wave/lane activity", which is my `live-state`; round-13 report states the intent: "Its 42 tokens are classified as intentional journal schema, carried r12 roster schema, or explicitly inferred live-state families; no regression-free proof or re-pin is claimed" (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-13/mori.md:76`).
- **Disagree** (method, not class): r13's entries are free-text, several tagged [INFERENCE], with no evidence pointers and no closed class set — precisely the gap the r20 contract names ("a classification lacking an evidence pointer" falsifies). For these two tokens the mechanism is now fully observed (ledger `complete` line; committed report blobs), so the [INFERENCE] qualifier can be dropped and `live-state` asserted with pointers.
- Neither of my tokens is `census-regression`; both are the documented intended behavior reacting to real fleet progress. They therefore do not block the C1 re-pin (the re-pin decision itself belongs to the L1, and the r13 verdict "red retained; no re-pin" applied to its own broader token set, which included genuine un-evidenced inference).

## Intent citations (round LOG/SCORECARD/knowledge)

- `corpus/knowledge/silence-cutover-r3.md:43` — row 6 "closed by committed report": `cat-file -e HEAD:<path>` rc 0 AND newest path commit `launch < ct ≤ NOW` (introduced 1439c47).
- `corpus/knowledge/verdict-machine-r4.md:261-287` — row 4 `complete <lane> round=N` → `basis=row-4 reason=ledger-close`, per-round close tracking fixed at 5b62c89.
- `corpus/knowledge/drift-pin-r10.md:41-43` — SCORECARD r9 intent ("a committed behavioral baseline plus a --drift mode with a declared volatile-fields list, so census behavioral drift is itself detected"); :50 — `--drift` names "changed non-volatile field names".
- `tools/mori-census.sh:195-198, 2730-2739` — added/dropped fields surface as drift by design; roster/count fields intentionally non-volatile.
- `c1-drift-entering.json` volatile_note / baseline :5 — masking suppresses magnitudes only; "token existence … never masked".

## Honesty / residual unknowns

- `tools/mori-census.sh` was NOT executed (bounds). The 07:19 per-line output was not retained (receipt keeps only the token line); the per-lane attribution above is reconstructed from the ledger, committed blob timestamps and the same-census 10:22:12Z witness capture — marked [reconstructed, witnessed]; the class decision does not depend on which specific lane carried the token, only on the unchanged emitting lines plus a live ledger/report event.
- Exact introduction commit of the `boot` volatile key: 18d7d55 (round-13) per `git log -S 'state_val_unread_reasons boot script_sha256'` — context only, not my token.
- No pacman/uv/npm installs were performed; no mutations to repo, jj/git state, or host services.
