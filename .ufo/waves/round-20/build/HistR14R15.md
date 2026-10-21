# C1 census-regression hunt: commits 8d22d18 (round-14) and 26f6589 (round-15)

Seat: MoriR20.HistR14R15 (leaf, read-only). Lane: mori-shokunin. Frozen claim: `.ufo/waves/round-20/contract.md` (C1). Entering drift receipt: `.ufo/waves/round-20/evidence/c1-drift-entering.json`.

## 1. Findings

1. **No census-regression found** in 8d22d18 or 26f6589 by code and declaration review. Every roll- or severity-changing default-output change in either commit is declared in that round's knowledge note and SKILL.md (r14 claim also in LOG/SCORECARD). No coverage was lost without a state cause: each per-scope class counter is kept, each failed unit is routed to exactly one bucket, and every positive/alarm path is additive.
2. **Six default-output or drift-contract changes are undeclared** in SCORECARD, LOG, knowledge, SKILL, QUALITY, PROVINCE, README and lessons. Per the assignment they are flagged as candidate census-regressions (F1 to F6, section 4). Under the contract's definition none is a regression: none changes a roll without a declared rule and none loses coverage. They are undeclared schema, label and drift-contract edits. Recommended class: census-schema-change, with the commit path:line as evidence.
3. **Token effect on the 50 entering tokens** (`c1-drift-entering.json:13-62`):
   - Caused by these commits: `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` (8d22d18).
   - Widened by these commits: `volatile_fields` (8d22d18 adds 20 names, 26f6589 adds 10; 18d7d55 already produces the token).
   - Content edited by these commits but first produced by 18d7d55: `+SURFACE:journal.system`, `+SURFACE:journal.user`, `+FINDING:JOURNAL_CLASSES_UNMEASURED`. The drift shows only the row-level token, so the edits are invisible at token level.
   - The other 44 tokens are not produced or changed by either commit (section 5 table). `-FINDING:KILL_SIGNAL_JOURNAL` is a neighbour: both commits widen its trigger, so they cannot cause its absence.
4. **Unclassified-8 check** (`c1-drift-entering.json:64-74`): only `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` has a cause in these two commits. The other seven trace to 18d7d55 identities, live counts, lane or watchdog state, or disk targets (section 5).
5. **Measured census is not 26f6589.** Three round-17 commits (273aa74, 2be8294, fe9fa90) changed `tools/mori-census.sh` after 26f6589 and touch lane-probe code. The journal probe and drift code are unchanged (section 6).

## 2. Scope, method, bounds

- Commits reviewed: `git show 8d22d18 -- tools/mori-census.sh` and `git show 26f6589 -- tools/mori-census.sh` (full diffs), plus `git show <c> -- LOG.md SCORECARD.md` and per-commit doc snapshots.
- Read-only git only: `show`, `log -S` (pickaxe), `rev-parse`, `merge-base --is-ancestor`, `config --get-regexp`. No `status`, `diff` on the worktree, `add`, `commit` or `checkout`.
- Snapshots for every line citation are in `.ufo/waves/round-20/build/HistR14R15/at/` (`r10-census.sh`, `r13-census.sh` = 8d22d18^, `r14-census.sh`, `r15-census.sh`, `measured-census.sh` = 2061780; `r14-*`/`r15-*` = per-commit docs). Unified diffs: `build/HistR14R15/{r10-to-r13,r13-to-r14,r14-to-r15,r15-to-measured}.diff`. Line numbers below are at the named commit unless marked "measured".
- Census SHA-256 lineage (`git show <rev>:tools/mori-census.sh | sha256sum`):
  - 8d22d18^ (r13): `39abda0a…3985` (matches the r13 knowledge note's own citation, `r14-knowledge-structured-scopes-r13.md:2`).
  - 8d22d18 (r14): `0e41cb83…16d9`.
  - 26f6589 (r15): `f1f8d1b6…01ff7`.
  - 2061780 (measured) and HEAD: `87b8d680…ab28`, matching the contract.
- Not run: `tools/mori-census.sh` (not authorized for this item), tests, builds, live journal reads. Anything about live state is marked [INFERENCE] and rests on the entering drift output.
- Tooling: no installs or updates. Filter semantics were probed with the existing `/usr/bin/jq` and `~/.local/bin/jq` (both jq-1.8.2). An earlier probe ran through a shell-level `jq` builtin reporting `jaq 3.1.1`; results were identical.

## 3. Changes in 8d22d18 (round-14)

Default-output effect unless marked otherwise. "Declared" lists where each change is named. Line refs: `r14-*.md` = commit snapshots; census lines are at 8d22d18.

| # | Change | Code (8d22d18) | Declared in | Token effect |
|---|---|---|---|---|
| R14-1 | Kernel-OOM notice: INFO per scope becomes one global `OOM_KILL_JOURNAL` CRIT, either scope, DRIFT. Per-scope `KERNEL_OOM_NOTICE_JOURNAL_{USER,SYSTEM}` IDs retired (replaced by counters inside the OOM line). | `tools/mori-census.sh:239`, `:1294-1331` (emit `:1331`); r13 mapping at `r13-census.sh:1016-1017` removed | LOG.md:758-771 ("restore boot-scoped structured OOM_KILL_JOURNAL critical/DRIFT"); SCORECARD.md:745-749; `corpus/knowledge/journal-alarm-routing-r14.md:9-16` (one global alarm), `:188-196`, `:211-217` (system-scope notice and unit-result arms called "explicit operator-required extension"); SKILL.md:31; PROVINCE.md:24. The ID retirement itself is only implied by the replacement. | none (no OOM_KILL or KERNEL_OOM token; neither ID is in the r10 baseline) |
| R14-2 | `UNIT_FAILURE_JOURNAL` (user) becomes fleet-only INFO. Non-fleet goes to `UNIT_FAILURE_OUT_OF_SCOPE` INFO (owner tsukuroi). Unknown subject goes to `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` INFO. | `:1272`, `:1279`, `:1286` | LOG.md:766-768; SCORECARD.md:745-747; knowledge `:115-127`, `:223-230`; SKILL.md:32-33. The user routing restores r10 behaviour (`r10-census.sh:781`, `:784`, text-based). | see R14-3 |
| R14-3 | `UNIT_FAILURE_OUT_OF_SCOPE` (user) re-emitted. It existed in r10 (text), was removed by 18d7d55, and is restored here as a structured ID. | `:245`; emit `:1279`, conditional on `nonfleetn -gt 0` (`:1277`) | knowledge `:120-122`; LOG.md:766-768 | **`+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` explained** by 8d22d18. Presence needs live non-fleet user records [INFERENCE from the emit condition]. |
| R14-4 | System scope: `UNIT_FAILURE_JOURNAL_SYSTEM` changes from all system unit failures (r13) to fleet-only. New `UNIT_FAILURE_OUT_OF_SCOPE_SYSTEM` and `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` (system). | `:1274`, `:1281`, `:1288`; header `:244-246`, `:934-937` | census header comment only (`:934-937`). No LOG, SCORECARD, knowledge or SKILL line names the `_SYSTEM` IDs. **Flag F2.** | none |
| R14-5 | User `KILL_SIGNAL_JOURNAL` WARN now also fires on user `UNIT_RESULT=signal` (roll-flipping). | `:1344-1353` (emit `:1353`) | knowledge `:17-23`, `:202-210`, `:315-316`; SKILL.md:34. LOG r14 section: only in a later round-14 commit, 52512ae, at 26f6589 `LOG.md:845-847`. SCORECARD r14: not named. | none (widens trigger) |
| R14-6 | `KILL_SIGNAL` note text: "not an OOM or fleet-caused kill" becomes "cause unknown (a kernel OOM can also deliver SIGKILL)" (both scopes). | `:1250`, `:1353` (r13: `r13-census.sh:1100`) | Substance declared: `r13 structured-scopes-r13.md:46` ("sender/cause unknown"); r14 knowledge `:158-164`; SKILL.md:34. The new sentence is not announced. **Flag F5.** | none |
| R14-7 | `JOURNAL_CLASSES_UNMEASURED` classes and reasons rewritten; `unmeasured=` row text rewritten. | `:962-965`, `:1167`, `:1386` | knowledge `:158-166` (table), `:313-314` ("Replace the categorical no-anchored-structured-field wording..."); SKILL.md:35 | `+FINDING:JOURNAL_CLASSES_UNMEASURED` token is from 18d7d55; body edit invisible |
| R14-8 | Journal SURFACE rows: `field=user:MESSAGE_ID` becomes `field=$scope:MESSAGE_ID` (r13 wrote `user:` in both rows). | `:1384` (r13: `r13-census.sh:1126`) | none. grep of all r14 docs for `user:MESSAGE_ID` and `field=user` returns nothing. **Flag F1.** | inside `+SURFACE:journal.{user,system}` (invisible) |
| R14-9 | Journal SURFACE rows gain 12 `unit_*` counters, `unit_subject_fields`, `unit_query_output_fields`, `fleet_predicate`, `fleet_tokens`, `fleet_owner`, `nonfleet_owner`, `unattributed_owner`, `classification_rule`, `nonfleet_basis`, and `unmeasured_reasons`. | hunk `@@ -1119,12 +1366,24 @@` (`:1366-1389`: the `unit_$uf` loop and `:1385-1386`) | concept only: knowledge `:115-127`; SKILL.md:32-33. Field names are not declared anywhere. **Flag F3.** | inside `+SURFACE:journal.*` (invisible) |
| R14-10 | `DRIFT_COUNTER_KEYS` gains 20 names (`user_notice`, `system_notice`, `user_unit_oom`, `system_unit_oom`, the `*_result_unknown` pair, `unit_fleet`, `unit_nonfleet`, `unit_oom*`, `unit_signal`, `user_unit_signal`, `process_sigkill`, ...). Masked magnitudes and `volatile_fields` change. | `:2265-2269` (list `:2254-2270`; `DRIFT_VOLATILE_LIST` `:2273`) | none in r14 docs (grep for DRIFT_COUNTER, counter key, volatile). The r13 register (`drift-classification.json:44`, `:47`) and r15 (lessons `:100-104`, SKILL.md `:196-199`) each declare their own mask change. **Flag F4.** | `volatile_fields` (co-explained, see section 5) |
| R14-11 | New jq filters: `JOURNAL_JQ_TAIL`, `_MSGID`, `_SIGKILL`, `_SIGSEGV` restructured; `JOURNAL_JQ_UNITS` added. | `:973-976`; unit split block from `:978` | mechanics; covered by R14-1 to R14-9 | none directly |

Hunk inventory, `r13-to-r14.diff` (16 hunks, all journal, drift-list, selftest or comment regions; numbers are r13-side): 12, 232, 876 (comment-only inside the waves function's neighbourhood; `emit_surface waves` line unchanged), 900, 928, 937, 982, 1008, 1023, 1068, 1082, 1119, 2003, 2733, 2747, 2784. No watchdog, lane, cgroup, disk or tmux probe is touched.

## 4. Changes in 26f6589 (round-15)

| # | Change | Code (26f6589) | Declared in | Token effect |
|---|---|---|---|---|
| R15-1 | Scope-local positive tokens on both journal SURFACE rows: `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`, plus `positive_basis`, `positive_validation`. | `r15-census.sh:1621-1625`; header `:17-28`, `:989-1005` | knowledge `journal-positive-evidence-r15.md:17-21`, `:109-113`, `:232-237`; SKILL.md:52-72; LOG.md:877-880, `:900-904`; SCORECARD.md:822-827; PROVINCE.md:32-33 | inside `+SURFACE:journal.*` (invisible) |
| R15-2 | `OOM_KILL_JOURNAL` CRIT also fires from individually valid current-boot positives when the raw class is unavailable. Adds `{user,system}_positive_*` fields, `alarm_basis`, `raw_basis`, `positive_basis`. | `:1534` | knowledge `:213-220`; SKILL.md:31, `:78-80` | none (no OOM line in entering output) |
| R15-3 | User `KILL_SIGNAL_JOURNAL` WARN fires from positives. Adds `user_positive_process_sigkill`, `user_positive_unit_signal`, and `trust=client-supplied`. | `:1588` | fire rule knowledge `:221-225`; SKILL.md:34, `:80-83`. **`trust=client-supplied` is undeclared. Flag F6.** | none |
| R15-4 | Positive fallback on semantic aggregate failure, same captured stream, no extra query. | `:1052-1055` (JOURNAL_JQ_POS_*); `journal_positive_scan`/`journal_query` changes | LOG.md:900-904; knowledge `:128-131` ("Same capture, no rescue query"); lessons `:108-111` | none |
| R15-5 | Guard rewrite: `type == "object" and ...` becomes `if type == "object" then ... else false end` (aggregate filters). Claimed as tightening. | `:1039-1042` (r14: `:973-976`) | LOG.md:921-922; lessons `:113-119` ("remove dependence on boolean short-circuit"). Output-equivalent, see section 6.2. | none |
| R15-6 | `DRIFT_COUNTER_KEYS` gains 10 `positive_*` / `*_positive_*` names. | `:2516-2519`; comment `:2521-2525` | lessons `:100-104`; SKILL.md:196-199 | `volatile_fields` (co-explained) |
| R15-7 | Pinned-header `volatile_note` text. Not default output; `--drift` does not compare header lines. | `:2685` | substance in lessons `:100-104`; the "MAGNITUDES only" sentence is not separately declared | none |

Hunk inventory, `r14-to-r15.diff` (20 hunks; numbers are r14-side): 17, 163, 946, 970, 1016, 1034, 1094, 1119, 1153, 1190, 1218, 1290, 1377, 2267, 2427, 3067, 3117, 3135, 3143, 3176. All journal, drift-list, selftest or comment regions.

## 5. Drift-token attribution (all 50 entering tokens)

Cause column: commit that first produced or last changed the token's cause, or the state that makes it appear. Pickaxe results are from `git log -S`. "Mine" means 8d22d18 or 26f6589.

| # | Token (`c1-drift-entering.json`) | Cause | Mine? |
|---|---|---|---|
| 1 | `+FINDING:COREDUMP_NOTICE_JOURNAL_USER` | ID from 18d7d55 (pickaxe). Emitted only when count>0 (`r14-census.sh` "Positive counts only" loop, which contains `:1250`). Presence = live coredump notices [INFERENCE]. | no |
| 2 | `+FINDING:JOURNAL_CLASSES_UNMEASURED` | ID from 18d7d55. Body rewritten by R14-7 (`:1167`). | token no; body yes (invisible) |
| 3 | `+FINDING:ROSTER_SET_MISMATCH` | 1f07f1d (r12 roster) | no |
| 4 | `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER` | ID from 18d7d55; positive-only, so live count>0 [INFERENCE] | no |
| 5 | `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` | Re-emitted by R14-3 (`:1279`, `:245`). Live nonfleet records [INFERENCE]. | **yes** |
| 6 | `+FINDING:WATCHDOG_STATE_LAG` | Emit path unchanged since d30b4e4 (`r14-census.sh:769`). Live lag [INFERENCE] | no |
| 7 | `+SURFACE:journal.system` | Row created by 18d7d55; content edited by R14-8/9 (`:1384-1386`) and R15-1/3 (`r15-census.sh:1621-1631`) | row token no; content yes |
| 8 | `+SURFACE:journal.user` | Same as 7 | row token no; content yes |
| 9-22 | `+SURFACE:lane.audio`, `lane.chousa`, `lane.game-dev-2d`, `lane.game-dev-3d`, `lane.kaidoku`, `lane.kotodama`, `lane.lore`, `lane.mado`, `lane.mori`, `lane.revenger`, `lane.souji`, `lane.tabi`, `lane.tameshi`, `lane.tsukuroi` | r12 roster expansion (1f07f1d; r13 register `:11-24`) | no |
| 23-31 | `+conf_dropped_n`, `+conf_n`, `+roster_n`, `+roster_source`, `+state_dropped_n`, `+state_n` | Roster fields, 1f07f1d (pickaxe) | no |
| 25 | `+gate_s` | Young-lane row, `reason=age_le_gate gate_s=` (`r15-census.sh:2172`). Probe unchanged since r3 (pickaxe 1439c47). Live state [INFERENCE] | no |
| 26 | `+path` | Row-6 arm `path=` (`r15-census.sh:2190`). Live arm [INFERENCE] | no |
| 27 | `+reason` | Row-6 `reason=committed-report` (`:2190`) and row-8 `reason=age_le_gate` (`:2172`). Live arm [INFERENCE] | no |
| 32 | `+subject_commits` | Row-A `subject_commits=yes window=launch..NOW` (`:2241`). Live arm [INFERENCE] | no |
| 33 | `+window` | Row-A (`:2241`). Live arm [INFERENCE] | no |
| 34 | `-FINDING:KILL_SIGNAL_JOURNAL` | r10 text class (`r10-census.sh:774`) retired by 18d7d55. R14-5 and R15-3 only widen the trigger, so they cannot cause absence. Zero live count [INFERENCE] | no (neighbour) |
| 35 | `-FINDING:SEGFAULT_JOURNAL` | r10 text class (`r10-census.sh:778`) retired by 18d7d55 | no |
| 36 | `-FINDING:WATCHDOG_STALE` | Live: watchdog log fresh; emit unchanged (`r15-census.sh:694`) | no |
| 37 | `-FINDING:WAVE_UNSETTLED_AGE` | Live: no aged unsettled wave; waves probe unchanged since r13 | no |
| 38 | `-SURFACE:journal` | r10 text row (`r10-census.sh:787`) replaced by 18d7d55 | no |
| 39 | `-attribution` | Row-B key on lane.aggregator (r10 baseline line 14); row-B arm absent live [INFERENCE] | no |
| 40 | `-example` | Row-B key (same) | no |
| 41 | `-rowb_files` | Row-B key (same) | no |
| 42 | `-subject_commits` | Row-A key; arm moved live [INFERENCE] | no |
| 43 | `-window` | Row-A key (same) | no |
| 44 | `HEADER` | `VERSION=census-r5` to `census-r6` by 18d7d55 (`r10-to-r13.diff:65-66`; `r14-census.sh:261`) | no |
| 45 | `age_s` | `age_s=-` for an unlaunched lane. `drift_normalize` masks digits only, so `-` stays visible (`tools/mori-census.sh:2783`). Live [INFERENCE] | no |
| 46 | `basis` | Lane arm value changed (row-A, row-B, row-6) [INFERENCE] | no |
| 47 | `io_avg_unavailable` | Disk row value; field from d30b4e4 (pickaxe). Live target list [INFERENCE] | no |
| 48 | `obs` | FINDING `obs=` value for WAVE/WATCHDOG lines; probes unchanged [INFERENCE] | no |
| 49 | `round` | `round=-` for an unlaunched lane (same masking gap as `age_s`) | no |
| 50 | `volatile_fields` | List delta vs r10 header (`r10-census.sh:1647` has no `boot`). First produced by 18d7d55 (+6 counters, `boot` special). 8d22d18 adds 20 names (`:2265-2269`, flag F4). 26f6589 adds 10 names (`:2516-2519`). | **widened by both** |

Causal: row 5. Widened: row 50. Content edited by these commits but first produced by 18d7d55: rows 2, 7, 8. Neighbour, not causal: row 34. Unaffected: the other 44 tokens.

Of the eight unclassified tokens (`c1-drift-entering.json:64-74`): `+FINDING:COREDUMP_NOTICE_JOURNAL_USER` (row 1), `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER` (row 4), `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` (row 5), `+path` (26), `-FINDING:WATCHDOG_STALE` (36), `age_s` (45), `io_avg_unavailable` (47), `round` (49). Only row 5 has a cause in these commits.

Note for the register: the r13 register (`drift-classification.json`) lists 42 tokens. Its class vocabulary (`intentional journal schema/version/mask change`, `r12 roster schema carried since r10`, `[INFERENCE] ...`) is not the contract's closed set. The mapping above does not depend on it.

## 6. Checks run

### 6.1 Declaration greps (commit snapshots)

- `census-regression` (and `census-schema-change`): no hit in any r14 or r15 document. The class names first appear in the round-20 contract.
- `user:MESSAGE_ID` and `field=user`: no hit in r14 docs (F1).
- `UNIT_FAILURE_JOURNAL_SYSTEM`, `OUT_OF_SCOPE_SYSTEM`: no hit in r14 docs (F2).
- `unit_fleet`, `unit_subject_fields`, `fleet_predicate`, `fleet_owner`, `nonfleet_owner`: no hit in r14 docs (F3).
- `DRIFT_COUNTER`, `counter key`, `volatile` in r14 docs: generic r10 drift-pin text only (F4).
- `trust=` in r15 docs: no hit (F6).
- `UNIT_RESULT` in the r14 LOG section at 8d22d18: no hit. It appears at 26f6589 `LOG.md:845-847` (from 52512ae, a later round-14 commit): "NH2 additionally restored user UNIT_RESULT=signal WARN without treating it as signal9."
- `cause st`: SKILL.md r14 `:34` is truncated in the view, but r15 `SKILL.md:34` reads "cause stays unknown (a kernel OOM can also deliver SIGKILL)".

### 6.2 Guard-rewrite equivalence (R15-5)

Command: `jq -n -c 'false and error("boom")'` gives `false`, rc 0. On the same binary, `printf '%s\n' '"noise"' '[1]' '9' '{"MESSAGE_ID":"m"}' | jq -s -c 'all(.[]; type == "object" and (._BOOT_ID | type) == "string")'` gives `false`, rc 0, and the `if type == "object" then ... else false end` form gives `false`, rc 0. Checked with `/usr/bin/jq` and `~/.local/bin/jq` (both jq-1.8.2). `A and B` and `if A then B else false end` agree for boolean A, so no default-output change.

### 6.3 Hunk and SHA checks

- The measured census differs from 26f6589 in 18 hunks (`r15-to-measured.diff`). None is in `probe_journal`, `JOURNAL_JQ_*`, `DRIFT_COUNTER_KEYS`, `DRIFT_VOLATILE_*`, `drift_normalize`, `run_drift`, `run_pin` body or the `VERSION` line. The lane probe (about 2089-2300 in r15 numbering, now about 2131-2440) and selftests change.
- So the journal and drift tokens above are fully explained by the r15 code as it stands.

### 6.4 Pickaxe (token to introducing commit, `git log -S`)

- `COREDUMP_NOTICE_JOURNAL_USER`, `SEGFAULT_SIGNAL11_JOURNAL_USER`: 18d7d55 (r13). `JOURNAL_CLASSES_UNMEASURED`: 18d7d55, 8d22d18.
- `UNIT_FAILURE_OUT_OF_SCOPE`: 486a4e3 (r1), 18d7d55, 8d22d18.
- `KILL_SIGNAL_JOURNAL`, `SEGFAULT_JOURNAL`, `SURFACE journal`: 7ca17b1 (r1), 18d7d55; `KILL_SIGNAL_JOURNAL` also 26f6589.
- `OOM_KILL_JOURNAL`: 7ca17b1, 18d7d55, 8d22d18, 26f6589.
- `KERNEL_OOM_NOTICE_JOURNAL`: 18d7d55, 8d22d18.
- `VERSION=census-r6`: 18d7d55.
- `volatile_fields`: 5be8943 (r10 pin).
- `ROSTER_SET_MISMATCH`, `roster_source`, `conf_n`, `state_dropped_n`: 1f07f1d (r12).
- `WATCHDOG_STATE_LAG`: d30b4e4 (r7). `WATCHDOG_STALE`: 7ca17b1, 5be8943. `gate_s`, `subject_commits`: 1439c47 (r3). `io_avg_unavailable`: d30b4e4.

## 7. Open items and recommendations for L1 (no action taken)

1. **UNIT_FAILURE_OUT_OF_SCOPE**: classify census-schema-change (8d22d18, `tools/mori-census.sh:245`, `:1279`; LOG.md:766-768). Presence is live state [INFERENCE]; not a regression.
2. **volatile_fields**: census-schema-change. Cite 18d7d55 (first production), 8d22d18 (`:2265-2269`, undeclared, F4), 26f6589 (`:2516-2519`, declared, lessons `:100-104`). A new pin would differ from the r10 list by 36 added names (6 from 18d7d55, 20 from 8d22d18, 10 from 26f6589), 3 dropped names (kill_signal, segfault, unit_failure; not touched by 8d22d18 or 26f6589), and the `boot` special. Record that in the pin reason.
3. **F1 to F6** (undeclared): none is a census-regression under the contract's definition. Options: a declaration line in a round document, or classify census-schema-change with the path:line above as evidence. The L1 decides; this seat does not.
4. **Live evidence gap**: whether the absent `OOM_KILL_JOURNAL` and `KILL_SIGNAL_JOURNAL` lines mean zero or unavailable cannot be read from the drift output, because journal rows are `+SURFACE` tokens. A captured live run's `SURFACE journal.user` and `journal.system` rows would settle it. Not run here.
5. **Comment accuracy** (no behaviour change): `r15-census.sh:2524` says `unavailable:<reason>` "contains no digits". `unavailable:rc-1` contains a digit. Masking needs digits immediately after `=`, so the value stays visible and behaviour is correct.
6. **Lane-arm tokens (26, 27, 32, 33, 39-43, 46)**: round-17 changed row-6 and lane probe code (`measured-census.sh` near 2394-2442, `refs/heads` anchor). HistR17 or the L1 should confirm these are live-state and not an r17 arm-logic change before classing them. [INFERENCE]

## 8. Installs and updates

None. No tool was installed or updated by this seat.

## 9. Write and safety bounds

No census edit, no baseline edit, no lane production file edit, no git mutation, no MANIFEST or ledger write. Writes limited to this report and seat scratch under `.ufo/waves/round-20/build/HistR14R15/` (regenerable with `git show <rev>:<path>`).
