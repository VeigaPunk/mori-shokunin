# AttackSignalConfusion — round 15 (report-only critic)

Seat: `MoriR15.AttackSignalConfusion`. Axis judged: **coverage**. Milestone: retain validated positives
without fabricated totals. Attack surface: (a) generic `UNIT_RESULT=signal` vs process signal 9, and
(b) system/user scope conflation in the new `positive_*` evidence. No execution, no production edit.

## Inputs read (snapshots as read 2026-10-20)

- `tools/mori-census.sh#DC7D`. `CensusPositive` had not landed yet: there were no `positive_` tokens.
  - `:975` `JOURNAL_JQ_SIGKILL` all-records gate: `EXIT_CODE == "killed"` and `(EXIT_STATUS|tostring) == "9"`.
  - `:1016-1017` unit `oom`/`sig` predicates: exact string `oom-kill` / `signal`.
  - `:1240-1254` per-scope info findings, gated on the aggregate (`js == ok`). System `KILL_SIGNAL_JOURNAL_SYSTEM` is emitted here.
  - `:1303-1331` global OOM line. Fields are built in the scope loop with `user_`/`system_` prefixes.
  - `:1340-1353` user-only KILL warn, built from `user:unit_sigkill_record` and `user:signal`.
  - `:1360-1379` surface row tokens. `:2269` drift counter keys. `:2292` mask regex `\b(key)=[0-9]+`.
  - `:3043`, `:3120-3121` selftest regexes.
- `tools/mori-round14-regressions.py#9B04`:
  - `journal_stub_body`: the `honor` filter is `str(rec.get(k)) != v`. `ignore-filters` hands every scope record to every query. Line numbers shift under concurrent edits, so it is cited by name.
  - `:275` `TOKEN_RE`; `:554` and `:568` parse tokens with `dict(...)`, so the last duplicate key wins.
  - `:576` `count_ids` uses exact id equality.
- `spec.json` items: CensusPositive, HarnessBuild, and the Pack* seats.
- Fixtures present: SignalUser, ProcessUser, NegativeStatus, CleanControls, KernelUser, KernelSystem, ForeignBoot, BootArray, NegativeInvalid. CrossScope, NegativeResults and FanoutPositive did not exist yet.
- Sibling reports I grepped to avoid repeating them: AttackFalsePositive, AttackFixtureOracle, ReviewKernelPredicate, ReviewProcessPredicate, ReviewHarnessPacks, ReconResultEmitter.

## Counterexamples

### S1 — A generic unit-result signal is relabelled as a SIGKILL (identity / false provenance)
- **Mutant.** `positive_process_sigkill` (or the raw `process_sigkill`) is fed from the `d9b373ed` stream's `UNIT_RESULT=="signal"`. Or the warn line gains `signal=9` when only `paths=unit_result_signal` fired.
  - `UNIT_RESULT=signal` is any non-clean signal death: SIGABRT, SIGKILL, SIGTERM where it is not a success status, and so on. Core dumps are `core-dump`, not `signal`. Only `98e32220` with `EXIT_CODE=killed` and `EXIT_STATUS=9` names signal 9.
- **Evidence.** `:1250` puts `signal=9` on the system `unit_sigkill_record` line only. `:1353` carries no `signal=` token. `:995-997` already says "a result ordinal, not proof of SIGKILL".
- **Booleans do not catch it.** `want_signal=true` holds either way.
- **Smallest required behavior.**
  - `positive_unit_signal` comes only from the `sig` predicate (`:1017`) over the `d9b373ed` stream.
  - `positive_process_sigkill` comes only from the `98e32220` stream.
  - The warn `paths=` is built from the two *positive* values, keeping the existing literals `process_sigkill` and `unit_result_signal`.
  - No `signal=` token on the KILL warn line.
- **Harness.** SignalUser cases must assert the exact user-row values `positive_process_sigkill=0`, `positive_unit_signal=1`, and the exact finding token `paths=unit_result_signal`. ProcessUser cases must assert the mirror: `paths=process_sigkill`, `positive_unit_signal=0`.

### S2 — The SIGKILL predicate is widened to "any kill" or to "numeric 9"
- **Mutants.**
  - The positive selector checks `EXIT_CODE=="killed"` only.
  - Or it uses `(.EXIT_STATUS|tonumber?)==9`, which accepts `"09"`, and possibly `"9.0"` and `" 9"` depending on the jq version `[INFERENCE]`.
  - Or it checks `EXIT_STATUS==9` and ignores `EXIT_CODE`. Then `EXIT_CODE=exited` with `EXIT_STATUS=9` is exit code 9, not signal 9.
- **Current coverage.**
  - Covered: `"137"` (ProcessUser case 4), `exited`/`"9"` (NegativeStatus case 4), and arrays and null.
  - Missing: the realistic generic-signal record `EXIT_CODE=killed` with `EXIT_STATUS="15"` (SIGTERM), and `"09"`.
- **Smallest required behavior.** Keep the `:975` predicate shape: `.EXIT_CODE == "killed" and ((.EXIT_STATUS|tostring) == "9")`, on a scalar `MESSAGE_ID`/`_BOOT_ID`. `tostring` on arrays gives `"[...]"`, null gives `"null"`, and `"09"` stays `"09"`, so all are excluded. Do **not** switch to `tonumber`.
- **Fixture to add.** Use `ignore-filters`. In honor mode, journalctl's `EXIT_STATUS=9` match drops the record before it reaches jq, so the case would be vacuous.
  - user: `[{98e32220, killed, "9", boot 1111}, {98e32220, killed, "15", boot 1111}]`
  - Expected: `want_signal=true`, `invalid_class=unit_sigkill_record`, `positive_process_sigkill=1`.
  - Variant with only the `"15"` record: `want_signal=false`, `positive_process_sigkill=0`.
  - Owners: PackNegativeStatus / PackProcessUser.

### S3 — A positive selector omits the `MESSAGE_ID` check (cross-class leakage under `ignore-filters`)
- **Mutant.** One shared per-record helper tests only `UNIT_RESULT` or only `EXIT_CODE`/`EXIT_STATUS`, without `.MESSAGE_ID == $id`. Under `ignore-filters`, each class stream gets every scope record. Projection keeps cross-class fields because the queries request them: the unit query requests `UNIT_RESULT`, and the sigkill query requests `EXIT_CODE,EXIT_STATUS`.
- **Evidence.** No current pack discriminates this.
  - SignalUser case 4 has a cross-id record, but its `MESSAGE_ID` is an array, so it is invalid for any predicate.
  - Every other `EXIT_CODE` carrier is a `98e32220` record, and every `UNIT_RESULT` carrier is a `d9b373ed` record.
- **Fixtures to add** (`ignore-filters`, user scope, boot 1111, scalar ids):
  1. `{MESSAGE_ID:98e32220, EXIT_CODE:"exited", EXIT_STATUS:"0", UNIT_RESULT:"signal"}`
     - Expected: `want_signal=false`, `invalid_class=unit_failure_record`.
     - Exact values: `positive_unit_signal=0`, `positive_process_sigkill=0`.
  2. `{MESSAGE_ID:d9b373ed, USER_UNIT:"kagi-shokunin.service", UNIT_RESULT:"resources", EXIT_CODE:"killed", EXIT_STATUS:"9"}`
     - Expected: `want_signal=false`, `invalid_class=unit_sigkill_record`.
     - Exact value: `positive_process_sigkill=0`.
  3. Optional: `{MESSAGE_ID:d9b373ed, USER_UNIT:..., UNIT_RESULT:"oom-kill"}`
     - Expected: `want_oom=true` (unit path).
     - Exact values: `positive_kernel_oom=0`, `positive_unit_oom=1`. The kernel stream sees this record but must not count it.
  - Realism: honest journalctl cannot return a record whose scalar id is different. These are defective-producer mutant catchers, as the AttackFixtureOracle realism caveat describes, not frequency claims.
- **Smallest required behavior.** Every positive selector is class-local and ANDs `type=="object"`, scalar `._BOOT_ID == $boot`, and scalar `.MESSAGE_ID == $id` for **its own** class id, before the result/status test. This is exactly the contract text.

### S4 — The user warn is fed by system-scope positives (scope conflation)
- **Mutant.** `kill_fire` is computed inside a `for scope` loop, or from a summed or unscoped positive variable, so a system `98e32220` killed/9 record or a system `UNIT_RESULT=signal` record raises `KILL_SIGNAL_JOURNAL severity=warn`.
- **Evidence.** Today the warn reads only `user:` keys (`:1340-1343`). r14 pins `R14_UNIT_SIGNAL_SYSTEM_INFO` (system signal stays info, CLEAN). ReviewHarnessPacks F6 notes that no pack proves system exclusion. PackCrossScope was not written yet.
- **Strongest variant (mixed, honor mode suffices, because the stub ignores `-b`):**
  - user: `[{98e32220, killed, "9", boot 2222}]`. The only user record is foreign-boot, so it is invalid and gives no positive.
  - system: `[{98e32220, killed, "9", boot 1111}, {d9b373ed, USER_UNIT:"kagi-shokunin.service", UNIT_RESULT:"signal", boot 1111}]`
  - Expected: `want_signal=false`, `want_oom=false`, `invalid_class=unit_sigkill_record`. The scope is user.
  - User row: `unit_sigkill_record=unavailable:boot-mismatch`, `positive_process_sigkill=0`.
  - System row: `positive_process_sigkill=1`, `positive_unit_signal=1`.
  - Findings: `KILL_SIGNAL_JOURNAL_SYSTEM` info is present (the system aggregate is valid). There is **no** `KILL_SIGNAL_JOURNAL` finding. Roll CLEAN, rc 0.
- **Smallest required behavior.**
  - The warn decision reads only `user:` positive values.
  - `KILL_SIGNAL_JOURNAL_SYSTEM` stays aggregate-gated as at `:1243`. The system positive appears only on the `journal.system` row, with no new route.
  - `want_signal` is documented as *user warn only*.
  - The harness checks warn absence by exact parsed id (`count_ids` exact equality, r14 `:576`). It never uses a prefix or substring match, because `KILL_SIGNAL_JOURNAL` is a prefix of `KILL_SIGNAL_JOURNAL_SYSTEM`.

### S5 — Duplicate unprefixed keys on the global OOM line erase one scope
- **Mutant.** The positive fields are appended inside the `:1322-1326` scope loop as bare `positive_kernel_oom=$x positive_unit_oom=$y`. The single OOM line then carries each key twice.
- **Effect.**
  - r14 parsing (`dict(TOKEN_RE.findall(...))`, `:568`) keeps the *system* value. A user-only positive case reads `positive_kernel_oom=0` on the finding, which is a false red. Asserting the system value would instead mask a lost user positive.
  - A bash regex matches either copy.
  - `drift_field_report` keys collapse.
- **Smallest required behavior.** On the two global lines, mirror the existing `user_notice`/`system_unit_oom` convention:
  - OOM line: `user_positive_kernel_oom`, `user_positive_unit_oom`, `system_positive_kernel_oom`, `system_positive_unit_oom`.
  - KILL line (user only): `user_positive_process_sigkill`, `user_positive_unit_signal`.
  - The per-scope SURFACE rows keep bare `positive_*`, because the row is already scoped.
- **Agreement.** Same conclusion as ReviewKernelPredicate and ReviewProcessPredicate. It is listed here because it is the scope-conflation instance.

### S6 — Census selftest regexes alias raw and positive tokens by substring
- **Evidence.**
  - `:3120` `'unit_signal=1'` also matches inside `positive_unit_signal=1`.
  - `:3043` `.*process_sigkill=1 ` also matches inside `positive_process_sigkill=1 `.
- **Counterexamples.** Neither depends on harness parsing.
  1. In a mixed arm, a mutant that salvages nothing but drops or renames the raw token still passes `'unit_signal=1'` through the positive token. The "keep every existing raw token" guard is lost.
  2. A check for raw `unavailable` that is written as a non-anchored positive regex passes vacuously.
- **Not affected.** Drift masking: `\b(process_sigkill)=` cannot match inside `positive_process_sigkill=`, because `_` is a word character. Whether to add the new keys to `DRIFT_COUNTER_KEYS` (`:2269`) is a separate drift decision, ReviewKernelPredicate F6.
- **Smallest required behavior (CensusPositive selftest).**
  - Anchor raw-token checks on a separator: `[ (]unit_signal=` and `[ ]process_sigkill=`.
  - New mixed arms assert both literals: `unit_signal=unavailable:<reason>` and `positive_unit_signal=1`.
  - Re-anchoring the two existing arms is cheap and closes the identity gap.

### S7 — The SIGKILL warn is deduplicated when an OOM positive exists
- **Mutant.** Following the `:1250`/`:1353` note "a kernel OOM can also deliver SIGKILL", the user warn is suppressed whenever an OOM positive fires.
- **Why this is wrong.** systemd records an OOM-killed unit as `UNIT_RESULT=oom-kill`, not `signal`, and its process record is `killed`/`9`. One event therefore legitimately yields the OOM crit plus the KILL warn on the `process_sigkill` path. That is r14 behavior, and suppressing either is an identity change.
- **Fixture (honor mode works, because the stub ignores `-b`):**
  - user: `[{d9b373ed, USER_UNIT:"kagi-shokunin.service", UNIT_RESULT:"oom-kill", 1111}, {98e32220, killed, "9", 1111}, {98e32220, killed, "9", 2222}]`
  - Expected: `want_oom=true`, `want_signal=true`, `invalid_class=unit_sigkill_record` (`multi-boot`).
  - Exactly one `OOM_KILL_JOURNAL` line and one `KILL_SIGNAL_JOURNAL` line. `paths=process_sigkill`.
  - `user_positive_unit_signal=0`, because `oom-kill` is not `signal`, as the `:984` mutual exclusion says.
- **Existing inverse pin.** BootArray case 4 already covers the inverse: a valid `signal` plus an invalid `oom-kill` gives `want_oom=false`, `want_signal=true`. Owner for the new case: PackFanoutPositive / PackUnitUser.

## Tradeoffs the judge must keep (not fixes)

- **Scope means journal query scope, not subject scope.** A system-journal `d9b373ed` record with `USER_UNIT` and `UNIT_RESULT=signal` gives a system positive and no warn. Promoting it to the user warn would be a new route plus an identity change, so reject it.
  - `[INFERENCE]` With volatile or non-split journal storage, user-manager records may land in the system journal, so a user unit's signal death can be info-only. This residual predates r15 and stays named.
- **`positive_unit_signal` is not "all signal deaths".** It excludes `core-dump`, `watchdog` and `timeout`, and services' clean-signal exits produce no failure record `[INFERENCE: systemd SuccessExitStatus defaults]`.
- **Other signal numbers stay unmeasured.** The `other_signals:structured-field-unimplemented` token (`:1167`, `:1386`) must stay. Positive evidence does not close it.

## Impacted axes

- **coverage (owned).**
  - S2 and S4 are false-positive warns.
  - S7 is a false-negative warn.
  - S3 is false positives in either direction.
  - S5 and S6 hide a lost user positive or a lost raw token from the gate.
- **identity.**
  - S1: false SIGKILL provenance.
  - S5: duplicate keys.
  - S6: raw-token removal goes undetected.
- **No route or actuation change is proposed.**

## Coordination
- Short peer notes sent to `MoriR15.CensusPositive` (S1/S3/S5/S6), `MoriR15.HarnessBuild` (S4 exact-id
  absence, S6, per-case modes for S2/S3), `MoriR15.PackCrossScope` (S4 mixed variant). Results reach L1
  automatically. No sibling file edited. AttackProvenance IRC received; out of this seat's scope, no action.

## Addendum — read of landed CensusPositive (`tools/mori-census.sh#9898`)

CensusPositive reported S1–S7 covered. A spot read confirms S3 (class-local selectors), S4 (user-only
warn, `KILL_SIGNAL_JOURNAL_SYSTEM` aggregate-gated), S5 (`user_positive_*`/`system_positive_*` once each
at `:1510`, `:1512`, `:1567`) and S6 (`[ ]unit_signal=1` at `:3354`). One new defect, plus two minor issues:

- **R1 (regression, identity/coverage): duplicated `paths=` on the KILL warn.**
  - **Cause.** `journal_pos` returns the raw count on an ok aggregate (`:1309-1313`), so `pus == us` and
    `pps == ps`. The warn block then sets each path once from raw (`:1545`, `:1549`) and again from
    positive (`:1553`, `:1557`).
  - **Counterexample.** The pure valid user `UNIT_RESULT=signal` case (selftest `:3355`, r14
    `R14_UNIT_SIGNAL_WARN`) gives `ps=0 us=1 pps=0 pus=1`. `:1549` sets `kill_paths=unit_result_signal` and
    `:1557` appends it again, giving `paths=unit_result_signal,unit_result_signal`. The `:3355` regex
    `paths=unit_result_signal .*` then fails because a comma follows.
  - **Process path, correct only by accident.** `:1553` assigns instead of appending. With `us>0` and an
    unavailable process aggregate, it wipes `unit_result_signal`, and `:1557` restores it only because
    `pus>0`.
  - **Smallest fix.** Copy the OOM idiom (`:1515-1516`): set flags `kp=1`/`ku=1` in the four tests, then build
    `kill_paths` once, `process_sigkill` first, then `unit_result_signal`.
- **R2 (minor, provenance): the raw-only `alarm_basis` branch is unreachable.** Because positive equals raw
  on an ok aggregate, every raw fire is also a positive fire. The `scoped-record-count` branches (`:1520`,
  `:1562`) can never be taken, and every ok case reports `scoped-record-count+validated-positive-records`.
  Either set `*_pos_fire` only when the aggregate is not ok, or delete the dead branch and document the
  value.
- **R3 (minor, docs): the header contradicts the code.** `:999-1000` says KILL carries bare
  `positive_process_sigkill`/`positive_unit_signal`. `:1005` and the emit at `:1567` use `user_positive_*`.
- **Harness interface mismatch.** `tools/mori-round15-regressions.py#DAAB` `:1715-1719` prints a fake
  KILL line with bare `positive_unit_signal=1`; the SUT emits `user_positive_unit_signal=`.

All three findings and the harness mismatch were sent to `MoriR15.CensusPositive` and
`MoriR15.HarnessBuild`. Not executed.

**Follow-up read (`tools/mori-census.sh#87C2`, not executed).** R1, R2 and R3 are closed.
- **R1 closed.** The four tests set `kill_k`/`kill_u` (`:1556-1573`). `kill_paths` is built once, in fixed
  order, at `:1578-1579`, so no path token can appear twice.
- **R2 closed.** `*_pos_fire` is now set only when that class's aggregate status is not `ok` (`:1508`,
  `:1515`, `:1566`, `:1573`). A healthy aggregate therefore reports `alarm_basis=scoped-record-count` again.
- **R3 closed.** The header at `:1001` now matches the emit at `:1588` (`user_positive_*`).
- **New basis labels (L1 decision).** `positive_basis=validated-subset-lower-bound` and
  `positive_validation=…`. The SURFACE rows keep bare `positive_*` (`:1624-1625`).
- **Harness.** The fake KILL line in the round-15 harness (`:1715-1719`, bare `positive_unit_signal`) still
  needs HarnessBuild to align it. I did not re-read it.

## Tooling

None installed or updated.
