# DriftDebt — why the r10 drift pin remains red, and why this round neither reruns nor re-pins it

Seat: `MoriR16.DriftDebt` (scout, leaf). Own write: this report only.
Read time: 2026-10-20T08:52Z; repo HEAD `b83edc6ee3db6822382ab673d7e6e984e420f22f`.
No live journal query, no census run, no probe loop, no background job, no gate/build/test/selftest/formatter, no tool install, no `/tmp` write, no commit. Only static reads, `sha256sum`, and `git show/log/status`. Nothing outside this report was written.

## Axes

1. **Drift-signal fidelity** — does the committed red mean what the pin says it means, and is every token classifiable?
2. **Provenance** — are the receipt's inputs the bytes they claim, and does the round-15 narrative match the committed bytes?
3. **No-harm** — does preserving red require (or permit) a rerun or a re-pin this round? (No.)

## 1. The two committed artifacts

### 1a. r15 drift-current receipt (committed)

- Path `.ufo/waves/round-15/evidence/drift-current.json`, sha256 `63d123642b0a4415046df5e630530cc92142f0643e105d6bc587ebda86e43867`; introduced by commit `1822145` ("round-15: bind measured evidence and correct capture boundary oracle"), whose parent is `26f6589` ("round-15: retain valid positive alarms beside unavailable class totals").
- `argv`: `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json`; `generated_utc` `2026-10-20T08:23:07Z`; `exit` **1**; `stderr` empty; `inputs_changed` false; `elapsed_s` 3.108.
- Bound inputs (start = end): `tools/mori-census.sh` `f1f8d1b62bb617bbcc4664057ab807d3fed8c275b7aabbdf7b373323c5501ff7`; baseline `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478`; frozen control `.ufo/waves/round-15/frozen/mori-census.sh` `0e41cb83…`.
- `scope_start.head` = `scope_end.head` = `26f6589…`; porcelain 3,401 entries on both ends (dirty tree, inputs stable).
- These two input hashes are **still current** today (measured 08:52Z): `tools/mori-census.sh` = `f1f8d1b6…`, baseline = `0993b235…`. Nothing that `--drift` compares has moved since the receipt.

### 1b. r10 pin bytes (committed)

- Path `corpus/evidence/baseline-r10-20261015T2231Z.json`, sha256 `0993b235…`, 6,779 bytes / 39 lines; committed in `5be8943` ("round-10 evidence: drift pin …"), untouched since.
- Header: `census_sha256=d7710981aa1c7571ff9d6fd7f75822811173010e5f4e298ac3c47fab274a0b20`, `pinned_ts=2026-10-15T22:26:29Z`, a **69-token** `volatile_fields` list, then the canonical block.
- Canonical first line: `mori-census census-r5 — ts=<V> — mode=live — read-only`. The block contains 9 lane rows (`protocol`, `aggregator`, `kasegi`, `kengaku`, `kake`, `kumitate`, `kotoba`, `kagi`, `kama`), one `SURFACE journal` row, and the roll `MORI_CENSUS: DRIFT`.

### 1c. Current bytes the receipt would compare

- `VERSION=census-r6` (`tools/mori-census.sh:268`) whereas the pin records `census-r5`.
- 23-lane roster era (r12 commit `1f07f1d`: "census roster = declared lanes ∪ driver counters (9 -> 23)"); current code emits `SURFACE journal.$scope` in a loop (`:1338,1344,1350,1633`), not a single `SURFACE journal`.
- Current `volatile_fields` = **103 tokens**: `DRIFT_COUNTER_KEYS` (`:2500-2523`) + `DRIFT_VOLATILE_SPECIAL` (`:2527`), versus the pin's 69. Exact diff: **+37 / −3**.
  - Added: `boot`, `kernel_oom_notice`, `oomd_notice`, `coredump_notice`, `segfault_signal11`, `unit_sigkill_record`, `unit_failure_record`, `user_unit_oom_result_unknown`, `system_unit_oom_result_unknown`, `user_unit_oom`, `system_unit_oom`, `user_notice`, `system_notice`, `unit_oom_subject_unknown`, `unit_oom_result_unknown`, `unit_oom_fleet`, `unit_oom_nonfleet`, `unit_nonfleet`, `unit_fleet`, `unit_unknown`, `unit_missing`, `unit_ambiguous`, `unit_malformed`, `unit_oom`, `unit_signal`, `user_unit_signal`, `process_sigkill`, `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`, `user_positive_kernel_oom`, `system_positive_kernel_oom`, `user_positive_unit_oom`, `system_positive_unit_oom`, `user_positive_process_sigkill`, `user_positive_unit_signal`.
  - Removed: `kill_signal`, `segfault`, `unit_failure` (superseded by the structured scoped counters above).

## 2. Why the old red remains red

**It is structurally impossible for the committed pair to go green, independent of host state.** `run_drift` compares the baseline's recorded `volatile_fields` line against the current list before the output comparison (`tools/mori-census.sh:2726-2737`) and sets `volatile_fields` when they differ. The committed pair declares 69 vs 103 tokens, so `--drift` must emit at least `MORI_DRIFT: volatile_fields` and exit 1 even in the hypothetical case where every canonical output line matched. The pin note states this design explicitly: "Changing the list is itself drift" (`corpus/knowledge/drift-pin-r10.md` §1, §2) and the pre-r15 reading already predicted this token (`SkillInterface.md:77`: "the old r10 baseline reports `volatile_fields`; no re-pin is performed or claimed").

Second, the *unmasked* line/field set also differs by contract, not accident. Token-by-token reading of the committed stdout:

| Receipt token | Cause | Static evidence site | Class |
|---|---|---|---|
| `+FINDING:JOURNAL_CLASSES_UNMEASURED` | Retired text classes are now named as unmeasured instead of silently absent | `tools/mori-census.sh:1335` (header list `:254`) | intended contract (r14/r15) |
| `+FINDING:ROSTER_SET_MISMATCH` | Conf/state lane declarations disagree on this host | `:539`, selftest `:3137,3157` | host observation + new r12 finding |
| `+FINDING:WATCHDOG_STATE_LAG` | A state round sits below the ledger round | `:776`, header `:243` | host observation + new finding |
| `+SURFACE:journal.system`, `+SURFACE:journal.user` | One journal surface split into two scopes | `:1338,1344,1350,1633` (comment `:3256`) | intended contract (r13-r15) |
| 14 `+SURFACE:lane.*` (`audio`…`tsukuroi`) | Roster 9 → 23 | r12 `1f07f1d`; `resolve_roster` `:431-470`; arithmetic on the receipt: 9 baseline + 14 added = 23 | intended contract (r12) |
| `+conf_dropped_n +conf_n +roster_n +roster_source +state_dropped_n +state_n` | New silence-surface roster fields | `:2308` | intended contract (r12) |
| `+gate_s +reason` | At least one existing lane left the row-A arms for a row-2..row-8 state | `:2172` and neighbors | host state + new row fields |
| `+subject_commits +window` / `-subject_commits -window` | Opposite row-A membership changes on two paired lane lines; field-report is deduplicated, so the values are not printed | `:2241` vs `:2172`; pairing rule `drift_report` pass 2 (`:2630-2674`) | host state |
| `-FINDING:KILL_SIGNAL_JOURNAL` | Fire-conditioned on a positive raw/positive count; the current boot has none (r12 measured new boot `2026-10-19 08:11:44`, counts 0) | `:1588` inside the `kill_fire` guard (`:1548-1586`) | boot boundary / aging |
| `-FINDING:SEGFAULT_JOURNAL` | The r10 id was retired, not merely zeroed: the current census emits only the structured, scoped forms `SEGFAULT_SIGNAL11_JOURNAL_{USER,SYSTEM}` (`COREDUMP_SIGNAL=11`) | id map `:1285-1286`, emit `:1419-1420`; no `emit_finding SEGFAULT_JOURNAL` exists | intended contract (r13 structuration) + zero records |
| `-FINDING:WATCHDOG_STALE` | Log not stale at receipt time | fire guard `:692-694` | host state |
| `-FINDING:WAVE_UNSETTLED_AGE`, `obs` | Wave-directory set changed; the id-pairs are matched across different wave names, so `obs` names the field change (known lossy pairing) | `drift_line_id`/`drift_report` (`:2564-2674`); r12 classification: souji sweep `e20f4fa` deleted old aggregator markers | host state / evidence-set change |
| `-SURFACE:journal` | Replaced by `journal.user`/`journal.system` | same as split above | intended contract |
| `-attribution -example -rowb_files` | Aggregator left row-B (its row-B inference fields are gone); `+subject_commits +window` is consistent with that same line now grading row-A | `:2247-2263` (row-B extras), `:2241` (row-A extras) | host/evidence state |
| `HEADER` | Version token changed: pin `census-r5`, current `census-r6` (`:268`); `VERSION` is deliberately unmasked | `:2456` header printer | intended contract |
| `basis` | Lane row-basis changes (deduplicated across the two lane lines above) | as above | host state |
| `obs` | Same-id wave-finding pairing across changed wave names | as above | pair limitation |
| `volatile_fields` | 69-token vs 103-token mask contract | `:2726-2737` | intended contract, self-reported |

The verdict line itself is an exact match (`MORI_CENSUS: DRIFT`, values masked) and is **not** in the report — the roll word is unmasked and unchanged. The report is `sort -u` deduplicated (`drift_report` pass 3 / final join), so tokens prove existence, not multiplicity: one `-FINDING:WAVE_UNSETTLED_AGE` does not mean one removed wave line.

**No census regression is demonstrated.** The r12 per-token measurement already classified the boot/aggregator/wave tokens as fleet-evidence change, not gate misbehavior (`corpus/evidence/drift-r12-20261019T2204Z-classification.md`), and the r15 additions are the intended positive-evidence and scoped-journal contract. Exit 1 is the drift-pin contract's "drift" class; with `stderr` empty and `inputs_changed:false` it is a valid measured red, not a `2 could-not-evaluate` setup failure. The red is exactly the artifact policy prefers over a false green (`drift-pin-r10.md` §3, "Direction of safety").

## 3. Why no rerun this round

1. **It cannot change the answer.** The receipt binds the exact census and baseline bytes; both still hash to the receipt's values. `--drift` is deterministic given (census bytes, baseline bytes, volatile contract) — and the contract comparison alone forces exit 1. A rerun only re-observes host state.
2. **A new run would be inadmissible, not additional evidence.** It would execute at a different HEAD (`b83edc6` vs the receipt's `26f6589`), inside a tree being mutated by dozens of concurrent seats, and it would be uncommitted. L1's round-16 ruling forbids live journal/census probes by seats; early-seat measurements are not admissible verification.
3. **The host-state tokens are already classified, and the id-retirement token is code-structural.** `KILL_SIGNAL_JOURNAL`/`WATCHDOG_STALE`/wave-set changes were measured in r12; `SEGFAULT_JOURNAL` cannot exist in the current code at all (replaced by the scoped `SEGFAULT_SIGNAL11_JOURNAL_*` ids). Re-observing them adds nothing to the drift verdict.
4. **Scope.** R16 changes no census byte. The worktree `SKILL.md` r16 section (in flight by `MoriR16.SkillRegistry` at read time; worktree sha `e64a2728…`, `M` vs HEAD) states the probe "does not call it, adds no SURFACE or FINDING row, and changes no alarm, drift verdict or positive token". Running the census is not this round's deliverable.

## 4. Why no re-pin this round

- **Policy forbids re-pinning to silence red.** "A red result is a named finding in the round's before-state, not something to silence"; re-pin is "a recorded act with a reason", and the anti-pattern is "re-pinning to make red green" (`drift-pin-r10.md` §5.2-5.3; `audit-r11.md` D16: re-pin only with a reason, never to hide red).
- **Round 15 routed the item as status-neutral conformance debt with a closure gate.** Re-pin "only after reasoned semantic review of each drift token, committed with per-token classification. Otherwise keep it routed as status-neutral debt. No silent re-pin." (`ScribeRoutedDebt.md:20,81`; `ReconProtectedTeaching.md:47,286`; `ConnectSiblingOverlap.md:167`; `SkillInterface.md:77`). The r16 lesson likewise lists "Drift re-pin: rejected" (`corpus/lessons/round-16.md`, per `Lesson.md`; quality criterion Q41).
- **The round goal says so explicitly**: "old drift pin remains red, no re-pin"; "No census cutover". `--pin` writes the baseline path (outside this seat's read-only scope) and would be a census cutover.
- **A re-pin now would bake in the wrong normal.** `run_pin` records whatever roll the live census produced (`run_pin`, `:2676-2694`; the pin note §1: pinning a DRIFT host is still a pin). The current host rolls `MORI_CENSUS: DRIFT` with `JOURNAL_CLASSES_UNMEASURED`, `ROSTER_SET_MISMATCH`, and `WATCHDOG_STATE_LAG`; a new pin would freeze those findings as the baseline's normal without resolving or reviewing them, and it would silently adopt the 37 newly masked keys. That is precisely the masking/laundering move the pin design calls out.
- **Invocation/environment is not recorded in the baseline** (`drift-pin-r10.md` §3.2). A re-pin today would bind the 23-lane roster/conf+state environment and a 3,401-entry dirty tree; the r10 baseline did not record env, so "same invocation" cannot be reconstructed later. Re-pinning under those conditions manufactures an untraceable baseline.
- **Ownership.** The baseline is the mori drift-pin owner's artifact and any re-pin is an L1/operator decision. This seat is read-only and the report is advisory; §2's per-token table is the input that decision needs.

## 5. Provenance correction for round 15 (append-only; routed, not edited here)

`HistoryDirtyHistory.md` (round-15 build) states: "`drift-current.json` is another exit-1 receipt at `5601d12` … census SHA-256 `0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9`." That pair is internally consistent — `git show 5601d12:tools/mori-census.sh` hashes exactly `0e41cb83…` (the r14-era census bytes, byte-identical to `.ufo/waves/round-15/frozen/mori-census.sh`) — but it is **not the committed receipt's pair**:

- the committed `drift-current.json` binds `scope_start`/`scope_end` head `26f6589`, not `5601d12`;
- the executed census in the committed receipt is `f1f8d1b6…`, not `0e41cb83…`;
- `0e41cb83…` appears in the committed receipt only in its `sha256` table as the *frozen control copy*, which is byte-identical to those r14-era bytes.

So the note describes an earlier receipt state (before the r15 census change `26f6589` landed or before the final receipt was regenerated), not the bytes committed in `1822145`. The verdict is unchanged — exit 1 in both — and the three finding ids the note names (`JOURNAL_CLASSES_UNMEASURED`, `ROSTER_SET_MISMATCH`, `WATCHDOG_STATE_LAG`) are all present in the committed receipt's report. No reclassification follows. This is a documentation/provenance correction only; owner: Knowledge/Registry append-only correction (r15 files are historical, not editable here). The note's substantive disclaimer stands and is worth keeping: the drift receipt "is a dirty broad drift receipt, not a clean-status claim and not an R15 gate result" and its journal deltas are census surface/shape, not journal-record evidence.

## 6. Confidence and remaining unknowns

- **High:** receipt/pin identity, sizes, hashes, commit binding, exit/stderr/input-stability; the 69→103 mask diff; `VERSION` r5→r6; journal surface split; 9→23 roster arithmetic; the `SEGFAULT_JOURNAL` → `SEGFAULT_SIGNAL11_JOURNAL_{USER,SYSTEM}` id retirement; the structural impossibility of `--drift` returning 0 with the committed pair (contract-list check); the policy citations.
- **Medium ([INFERENCE] where marked):** mapping of the remaining host-state tokens (`-KILL_SIGNAL_JOURNAL`, `-WATCHDOG_STALE`, wave/`obs`, `basis`, `subject_commits`/`window`) to specific lane/boot events. This rests on the r12 measured classification and static code reading, not on a live observation by this seat. In particular, "aggregator is now row-A" and "one existing lane is row-8/young" are inferences from the deduplicated field deltas, not printed values.
- **Unknown:** which exact lane id moved row-A → row-8 (the field report suppresses ids on same-id pairs and prints only changed keys); exact current values of the changed keys (masked or not printed); whether a separate `5601d12` receipt existed and was overwritten before commit (not reconstructable from committed history, and live re-observation is forbidden this round).
- **Not claimed:** that the red is a code defect; that the census is broken; that a re-pin would be correct today; that r16's journal-window tool has any bearing on the drift result (it does not: no census byte changed).

## 7. Checks for L1 (not run here)

1. Re-hash `tools/mori-census.sh` (`f1f8d1b6…`) and `corpus/evidence/baseline-r10-20261015T2231Z.json` (`0993b235…`) before any decision; if either moved, §1's binding is void.
2. If a re-pin is ever authorized, do it as a dedicated act: record reason, per-token classification, new baseline sha, new `census_sha256`, `pinned_ts`, and the 103-token `volatile_fields`; never as part of a journal-window round.
3. Route §5 to the Knowledge/Registry append-only correction owner; do not edit the r15 historical note.
4. Confirm the worktree `SKILL.md` drift-pin row still names `corpus/evidence/baseline-r10-20261015T2231Z.json` and states red/not-re-pinned after siblings settle (read at 08:52Z: worktree `SKILL.md` sha `e64a2728…`, `M` vs HEAD; r16 text at worktree `:109-111`, row at `:164`; HEAD row at `:130`).
