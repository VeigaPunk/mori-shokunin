# drift re-pin r20 — why the r10 pin stayed red, the closed classification set, the re-pin ritual, and the immediate-drift flap

source: `tools/mori-census.sh` at the measured commit `2061780117e6ca637725004897bd288d3ba7e988`, census SHA-256 `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` (unchanged by this round; the census is not edited by C1).

status: **DRAFT by the scribe (MoriR20.DraftDriftNote).** Every number that depends on L1's register, pin or re-drift is a `TODO-L1` placeholder. Nothing in this draft is a re-pin, and no command was run against the census by this seat.

scope: detection and report only. This note states the procedure; it does not claim a clean drift, and it does not claim the new baseline is valid until L1 has run §4 and §5.

## 0. Evidence used

| id | path | what it shows |
|---|---|---|
| E1 | `.ufo/waves/round-20/evidence/c1-drift-entering.json` (`mori-r20-c1-entering-v1`) | entering `--drift corpus/evidence/baseline-r10-20261015T2231Z.json` at `87b8d680…`: rc 1, `token_count` 50, `unclassified_count` 8, list of the 8 |
| E2 | `corpus/knowledge/drift-pin-r10.md` | the r10 design, volatile contract, masking risks and the admission ritual (§5); erratum at the end (interim `2210Z` path is dead; adopted baseline is `2231Z`) |
| E3 | `corpus/evidence/baseline-r10-20261015T2231Z.json` | the adopted baseline: 39 lines, sha256 `0993b235…9670478`, header `census_sha256=d7710981…`, `pinned_ts=2026-10-15T22:26:29Z` |
| E4 | `corpus/evidence/drift-r12-20261019T2204Z-classification.md` | the first post-r10 classification (prose, not machine-readable): "no token is a census regression" |
| E5 | `corpus/evidence/drift-r12-20261019T2230Z-after-roster.log` | r12 re-drift at census `3da5b098…`, rc 1; line 4: "No re-pin this round" |
| E6 | `.ufo/waves/round-13/evidence/drift-classification.json` | the newest machine-readable register: 42 keys; class strings `r12 roster schema carried since r10` (21), `[INFERENCE] current watchdog/wave/lane activity … no re-pin/admission claim` (14), `intentional journal schema/version/mask change` (7) |
| E7 | `.ufo/waves/round-20/evidence/c1-pin-probe-scratch.json` | a copy of the L1's pin probe at census `87b8d680…`, header `pinned_ts=2026-10-21T10:22:12Z`; 23 lane rows (see §4) |
| E8 | `.ufo/waves/round-20/wave1-run.json`, scout `TokPinFlap` task text (line ~578) | the L1's report of the flap: pin at 10:23:18Z, drift ~65 s later, rc 1, tokens `+path +reason -subject_commits -window basis round`. The drift output itself was not written to a file; this note relies on the L1's report of it. |
| E9 | `tools/mori-census.sh` at `87b8d680…` | emit sites of the lane arms: `:2377` (row-8, `reason=age_le_gate gate_s=`), `:2411` (row-6, `reason=committed-report round= path=`), `:2473` (row-A, `subject_commits=yes window=launch..NOW`) |

Fact check run for this draft (read-only, no census run): the entering 50 tokens minus the 42 register keys is exactly the 8 listed in E1 (`+FINDING:COREDUMP_NOTICE_JOURNAL_USER`, `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER`, `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE`, `+path`, `-FINDING:WATCHDOG_STALE`, `age_s`, `io_avg_unavailable`, `round`). All 42 register keys are present in the live output.

## 1. Why the r10 pin stayed red for nine rounds (r12 → r20)

The r10 pin was first measured red at round 12 (E4, E5). The contract's count of nine rounds is r12 through r20 inclusive. Four causes, each evidenced:

1. **The census moved under the baseline.** The census SHA chain is `d7710981…` (pin, E3) → `3da5b098…` (r12 re-drift, E5, after the intended roster change of round 12) → `87b8d680…` (entering, E1). Each move is a real change; none was a re-pin.
2. **The host moved under the baseline.** The current boot began `2026-10-19 08:11:44` (E4 §A), which is why the boot-scoped kill and segfault findings are removed from the live output. The operator's sweep `e20f4fa` removed 96 pushed-receipt artifacts, including aggregator wave markers (E4 §A, `WAVE_UNSETTLED_AGE` and `basis` rows).
3. **The classification never closed.** E4 is prose. E6 is machine-readable but covers 42 keys, and 14 of them are tagged `[INFERENCE] … no re-pin/admission claim`. E6's own verdict field reads "red retained; categories are not a regression-free proof; no re-pin". The 8 tokens listed in E1 were not in E6 at all.
4. **The admission rule had no exit.** The r10 ritual (E2 §5.2) forbids re-pinning to make red green and requires a recorded reason. It does not define when the classification is complete. With no closed set and no completeness check, no round could certify "zero census-regression", so every round correctly declined to re-pin (E5 line 4). The red stayed because the procedure had no way to go green honestly, not because anything hid it.

Lesson for the ritual: a register must be complete by construction (every live token has exactly one class from a closed set, with an evidence pointer) before the question "re-pin or not" is even askable.

## 2. The classification closed set (draft; L1 ratifies)

Every token of the measured drift output receives exactly one class:

| class | use when | required evidence pointer |
|---|---|---|
| `census-schema-change` | a committed census edit changed the emitted key or id set on purpose (added, renamed or retired a field) | commit sha and `path:line` in the census at the measured commit, plus the census's own selftest or header line that records it |
| `roster-change` | the lane roster changed (conf or state set), or a roster-derived field moved | the `roster_n`, `conf_n`, `state_n`, `roster_source` values at pin and at drift |
| `live-state` | the census logic that emits the token is unchanged, and host, fleet or lane state differs | a command and its observed output with a UTC timestamp, read at the time of the drift; for lane arms, the `basis=` value and the git fact it depends on |
| `census-regression` | the output differs in a way the census's own documented contract does not predict, or a finding or surface loses coverage with no state cause | the failing case: command, expected, observed; **a token of this class blocks the re-pin and is reported, not hidden** |

Decision rules:

- One class per token. A token is never "unclassified", and never `[INFERENCE]`. If a cause cannot be observed, the token is `census-regression` until shown otherwise, which blocks the re-pin.
- Classify by **cause**, not by effect. A token that looks like coverage loss can have a live-state cause (a deleted directory) and a census-logic cause (the probe treats empty directories as empty). Both must be checked; the class follows the observed cause.
- The register is `corpus/evidence/drift-classification-r20.json` (`mori-drift-classification-v1`). Its key set must equal the live token set exactly; the counting command in the contract (`comm -23 … | wc -l`) must return 0.

Hard case already in the record: `-FINDING:WAVE_UNSETTLED_AGE` was called "Yes—coverage/evidence-loss regression" in E4. Under this rule that label is not enough: the deleted markers are live-state, and whether the probe's treatment of empty directories is a census regression is a census-logic question. Verdict: `TODO-L1` (pending the TokWaves scout).

Other tokens that need a cause check before classing (not classed here):

- `volatile_fields`: the masked-field list changed between r10 and the current census (E7 header vs E3 header). The register (E6) already calls this `intentional journal schema/version/mask change`; L1 should confirm that the list change is a committed census edit (`census-schema-change`).
- `+FINDING:JOURNAL_CLASSES_UNMEASURED`, `+FINDING:COREDUMP_NOTICE_JOURNAL_USER`, `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER`, `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE`, `+SURFACE:journal.*`: the journal schema change in the census. Candidate `census-schema-change`, to be confirmed against the commit that introduced the ids.
- `+SURFACE:lane.*` (14), `+conf_n +conf_dropped_n +roster_n +roster_source +state_n +state_dropped_n +ROSTER_SET_MISMATCH`: candidate `roster-change`, since E6 already names them the r12 roster schema.
- `age_s`, `round`, `io_avg_unavailable`: value-shape tokens. In E7 the not-launched lanes emit `round=- launch_epoch=- age_s=-` (kotodama) and `age_s=-` (kumitate). [INFERENCE] these are `live-state` shape changes, not masked numbers. Confirm with TokIoAvg and TokPathAge.

Counts: `TODO-L1` (per class), `TODO-L1` (census-regression count, must be 0 before the re-pin).

## 3. The re-pin ritual (r20 form)

Replaces r10 §5 for re-pins. The r10 steps still apply where they are not restated.

1. **Classify all tokens first.** Capture the drift output once to a file at the measured commit. Build the register (§2) so that its key set equals the live set. Verify with the contract's counting command; it must print `0`.
2. **Zero census-regression check.** If any token is `census-regression`, stop. Report the token, its failing case and the reason. Do not pin.
3. **Census SHA unchanged.** `sha256sum tools/mori-census.sh` must equal `87b8d680…ab28` at the measured commit. If it moved, the register is for the wrong census; redo step 1.
4. **Pin.** `bash tools/mori-census.sh --pin corpus/evidence/baseline-r20-<UTC>.json`, run by L1 at the measured commit. The r10 file stays byte-unchanged. Record the path, header `pinned_ts`, the baseline sha256 and `census_sha256`. The pin's exit code is 0 even on a DRIFT host (E2 §1); the roll inside the file is not a pin failure.
5. **Immediate re-drift, recorded whatever it is.** Run `--drift` against the new baseline after the pin, and record rc and every token. A non-`none` result is the measured stability window, not a failure to hide. Repeat at about 60 s and at the end of the round if the L1 wants a window.
6. **Reason.** The re-pin reason and the new sha go in the round record (`TODO-L1` link).

Important change from r10 §5.5: the r10 acceptance leg "drift after ≥60 s of live churn = `none`" held for clock and counter churn (E2 §2). It does not hold for lane arms. See §4.

## 4. The immediate-drift flap (observed, 2026-10-21)

Observed by the L1 (E8): the census was pinned at `10:23:18Z` to `/tmp/mori-r20/pin-probe.json`, and `--drift` about 65 s later returned rc 1 with `+path +reason -subject_commits -window basis round`.

Discrepancy to resolve: the pin file header records `pinned_ts=2026-10-21T10:22:12Z` (E7), which is the census run's own clock. The L1's `10:23:18Z` is the wall-clock write time. Both are consistent with a census run of about 66 s. For scale: the r10 note measured about 30–45 s wall at wave load (E2 §5.6), and the entering run took 103.98 s (E1). `TODO-L1` confirm.

What the token set says, by the census's own grammar (E2 §1: `+` = present live and absent in the baseline; `-` = present in the baseline, absent live):

- `+path +reason` are the row-6 keys (`reason=committed-report round= path=`, E9 `:2411`). They are present live, absent in the pin.
- `-subject_commits -window` are the row-A keys (`subject_commits=yes window=launch..NOW`, E9 `:2473`). They are present in the pin, absent live.
- `basis` changed value (`row-A` → `row-6`), and `round` changed shape (a masked number versus `-`).

[INFERENCE] One lane's row moved from row-A to row-6 between `10:22:12Z` and the drift: a committed report at the root's branch closed it (E9 `:2411`, the `ps_report_closed` branch). Only one lane line is implicated, because the flap token set contains no other lane key and no other finding.

The pin's row-A lanes are the only possible identities (E7, 11 rows): `protocol`, `aggregator`, `kasegi`, `kotoba`, `lore`, `tameshi`, `mado`, `souji`, `audio`, `game-dev-2d`, `game-dev-3d`. The lane identity, and the commit that closed it, are `TODO-L1` (pending the TokPinFlap scout; read-only `git log` of `.ufo/reports/round-20/`).

Classification: `live-state`. The census logic that emits row-6 is unchanged at `87b8d680…` (E9 is the same file). The change is a lane's report landing, which is exactly the signal the census is meant to show.

What it teaches:

1. **The 60-second absorption claim is scoped.** The r10 volatile list absorbs clock and counter churn. It does not absorb a lane's arm change, because `basis`, `path`, `reason`, `subject_commits` and `window` are deliberately unmasked (E2 §2, §3.3: the state word and basis are the visible signals). An arm change is therefore drift by design, and the r10 acceptance leg must say so.
2. **A pin is a snapshot of lane arms.** A baseline pinned while a lane is in row-A will read red as soon as that lane's report lands. Pinning during an active round is valid only as a dated snapshot, and the re-drift result must be recorded beside it.
3. **Do not re-pin to chase the flap.** Re-pinning after each lane arm change turns the baseline into a log of the wave, which is the masking failure E2 §3 warns against. The flap is recorded as the stability window; the baseline is re-pinned on the round's schedule, not on the lane's.

Open for L1: whether the flap's lane is in the 11-row list above, and whether a re-drift at ~60 s after the new pin reproduces it.

## 5. What this note does not claim

- No token of the entering output is classed here; the register is L1's and is not yet written (`TODO-L1`).
- No new baseline exists yet. `corpus/evidence/baseline-r20-<UTC>.json` is `TODO-L1`.
- The flap output is relayed from the L1's report (E8); the drift text itself was not stored. This seat did not run the census and did not verify the flap.
- The census's line numbers in E9 are at `87b8d680…`; they will move with any later census edit. The r10 note's line numbers (E2) are at `d7710981…` and are historical.
- E7 is named `.json` but is the `mori-drift-baseline v1` text format, not JSON (E2 §4). A reader using `jq` on it will fail.

## 6. Placeholders for L1 to fill

- `TODO-L1` register path and class counts (`census-schema-change`, `roster-change`, `live-state`, `census-regression`); `census-regression` must be 0.
- `TODO-L1` new baseline path, sha256, `pinned_ts`, `census_sha256` (must be `87b8d680…`).
- `TODO-L1` immediate re-drift rc and tokens (`10:xx:xxZ`), and the second reading if taken.
- `TODO-L1` flap lane identity and the commit that closed it; confirmation of the 10:22:12Z vs 10:23:18Z discrepancy.
- `TODO-L1` WAVE_UNSETTLED_AGE verdict (pending TokWaves).
- `TODO-L1` round record link and the re-pin reason.
