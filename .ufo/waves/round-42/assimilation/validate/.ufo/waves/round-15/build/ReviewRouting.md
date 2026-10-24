# ReviewRouting — round 15, claim C1 (positive evidence routing)

Seat: MoriR15.ReviewRouting (reviewer, read-only). Production files not edited. No builds, tests, linters, or census runs. Tools installed: none (parent host-safety directive received; no installation was needed for a read-only audit).

Axis: coverage (owned axis 6). Milestone: retain validated positives without fabricated totals.

Target inspected: `tools/mori-census.sh` @ HEAD working tree (`#DC7D`). The round-15 `positive_*` tokens are not yet present in the file (`grep positive_` → no match), so this review checks the current routing that the positive path must extend.

## Summary

Today a single adjacent invalid record suppresses a valid current-boot alarm. Each class gates on its whole-stream aggregate. When `js[...] != ok`, the class count is replaced by `unavailable:<reason>`, and the alarm and warn gates fall through silently. The three gates are:

- OOM alarm (`probe_journal` 1303–1332)
- user KILL_SIGNAL warn (1340–1354)
- unit-failure OOM and signal subsets (`ucnt[...]`, set only when `JQ_STATUS=ok`, 1202–1217)

The aggregate jq filters return a bare status string on any invalid record (`record-invalid`, `multi-boot`, `boot-mismatch`, 973–976, 1019–1037), so no per-record evidence leaves the filter. The required fix is to emit per-scope positive counts from the same jq pass in the invalid branch, and route the alarms on those counts.

## Findings (by severity)

### F1 — HIGH (coverage): OOM alarm is suppressed by any adjacent invalid record
- Anchors: `tools/mori-census.sh:1303-1321` (`ko="unavailable:${js[$key]}"` when not ok; `case "$ko" in unavailable:*) ;;` skips the fire), `1330` (`oom_fire` only from raw counts).
- Mechanism: `journal_query` returns on `record-invalid|multi-boot|boot-mismatch` at 1104 with no count vector. Any one record with a non-current `_BOOT_ID`, a non-string `MESSAGE_ID`, or a bad `UNIT_RESULT` type sends the whole class to unavailable. The current-boot valid kernel-OOM notice or `UNIT_RESULT=oom-kill` record is then lost. Result: CLEAN with a silent OOM.
- Required fix: the jq filter's invalid branch (`JOURNAL_JQ_TAIL` else arm, 973; `JOURNAL_JQ_UNITS` else arm, 1037) must emit `positive_*` counts. Count only objects where `type=="object"`, `_BOOT_ID` is a string equal to `$boot`, `MESSAGE_ID` is a string equal to `$id`. Must be guarded first with `select(type=="object" and ...)`. Do not index `.[].MESSAGE_ID` directly. `"str" | .MESSAGE_ID` is a jq error, which would turn a valid stream into `malformed-json` and erase the positives.
- `journal_query` must split that tail. Currently line 1104 compares the whole `$parsed` string to the status tokens. Change it to parse `<status>\t<positive columns>` on the invalid path, while keeping the raw status token exactly as today (raw counts stay unavailable).

### F2 — HIGH (coverage): user KILL_SIGNAL warn is suppressed the same way
- Anchors: `1340-1351` (`ps="unavailable:..."`, `us="unavailable:..."`), `1344-1350` (no fire on unavailable), `1352` (`kill_fire` only from raw counts).
- Required: add `positive_process_sigkill` (`user:unit_sigkill_record`, `EXIT_CODE` exact `killed`, `EXIT_STATUS` scalar `9`) and `positive_unit_signal` (`user:unit_failure_record`, `UNIT_RESULT` exact string `signal`). Fire when either is `>0` even if the raw counts are unavailable. `kill_paths` (1346, 1350) must then name the positive source.

### F3 — MEDIUM (honesty): `paths=` and `oom_fields` lose the positive source
- Anchors: `1316-1321` set `oom_path_k`/`oom_path_u` only from raw counts. `1328-1329` build `paths=`. `1323-1325` build `user_notice=$ko` etc.
- Required: `paths=` must include `kernel_oom_notice` or `unit_result_oom_kill` when the positive count fires, even if the raw field is `unavailable:record-invalid`. Keep the raw `unavailable:<reason>` tokens unchanged, and add the positive counts as separate named fields. Do not reuse `user_notice=` / `user_unit_oom=` names for positive counts.

### F4 — MEDIUM (fragility): scalar checks rely on `tostring`
- Anchor: `JOURNAL_JQ_SIGKILL` at 975 uses `(.EXIT_STATUS | tostring) == "9"`. This accepts the string `"9"` and the number `9`, and rejects arrays and objects. It works, but the spec says "scalar status 9". Make it explicit: `((.EXIT_STATUS|type) as $t | ($t=="string" or $t=="number")) and (.EXIT_STATUS|tostring)=="9"`. Same for `COREDUMP_SIGNAL` at 976 if it is reused.
- Note: `JOURNAL_JQ_UNITS` `oom()`/`sig()` (1016–1017) already check `type == "string"`. Good; reuse them for `positive_unit_*`.

### F5 — MEDIUM (contract): drift list changes if new counter keys are added
- Anchors: `DRIFT_VOLATILE_LIST` 2272–2273 (`${DRIFT_COUNTER_KEYS[*]}`), `drift_normalize` 2278–2279 (masks `\b(cre)=[0-9]+` to `<V>`), 2482 (volatile list change is itself drift).
- Consequence: adding `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill` to `DRIFT_COUNTER_KEYS` changes `volatile_fields`, so the pinned baseline reads `MORI_DRIFT: volatile_fields`. Either add them to the counter list and re-pin (a round-15 repin decision, flagged to L1), or state the drift as intentional schema drift. Do not hide it. Round-13 contract also says no repin this round, so the decision belongs to L1.

### F6 — LOW (test surface): existing field-once assertions must not collide
- Anchors: `3050` (OOM line must not contain `count=`), `3051-3053` (each of `user_notice`, `system_notice`, `user_unit_oom`, `system_unit_oom` exactly once via `\b$f=`).
- Constraint: new names must not contain `count=` and must not add a second `user_unit_oom=` or `system_unit_oom=` token. `positive_unit_oom=` is safe under `\b`, but `user_positive_unit_oom=` would not be.
- Existing fixture 3225 (foreign-boot record only, expects `CLEAN`) and 3230–3236 (multi-boot, expects `unavailable:multi-boot` with CLEAN) still hold, because they contain no current-boot positive. A new fixture is needed for the mixed case: one current-boot valid notice plus one foreign-boot record must yield `OOM_KILL_JOURNAL severity=crit` and `kernel_oom_notice=unavailable:boot-mismatch`.

### F7 — Known limits (stated, not claimed)
- A syntactically broken JSON line makes `jq -s` fail (`malformed-json`, 1102). The positive path cannot recover from that and must report positives as unavailable. The spec forbids repairing malformed JSON, so this is by design.
- `journal_query` refuses to run a stream with `stderr` bytes (1091–1094). That is the same capture used for positives, so positives also become unavailable there. Correct per the spec ("same captured successful stderr-free valid JSON stream").
- `MESSAGE_ID` is client-supplied (no underscore). A positive count proves a record with that field, not an authenticated victim. Name this in the finding note, as the existing text does at 1331.

## Verified routing (no change needed)
- OOM alarm fires once (1330–1332). Per-scope counters are separate and never summed (1323–1325).
- The kernel-OOM notice does not gate on `unit_failure_record` (1305–1306 are per scope). Good.
- The unit subject partition stays aggregate-only (1264–1291). Matches the spec's "Existing info owner partition remains aggregate-only unavailable".
- `emit_finding` (399–411) rolls DRIFT only on `warn|crit`. The positive OOM and kill paths therefore flip DRIFT only through the existing crit/warn lines. No new route or actuation.

## Required fixes (summary)
1. Extend `JOURNAL_JQ_TAIL`, `JOURNAL_JQ_UNITS`, and the SIGKILL/SIGSEGV filters to emit positive counts on the invalid branch, guarded with `type=="object"` first.
2. Change `journal_query` (1102–1105, 1111–1119) to split the invalid-branch tail. Keep raw status tokens exact.
3. Change the OOM gate (1303–1332) and KILL gate (1340–1354) to fire on `positive_*>0`. Keep raw `unavailable:<reason>` tokens unchanged.
4. Add positive fields to `paths=`, `oom_fields`, and `kill_paths` without reusing existing field names.
5. Make the scalar checks explicit (F4).
6. Decide the drift counter-list change with L1 (F5). Do not repin in this seat.
7. Add a mixed-record fixture (current-boot valid plus foreign or malformed record) for each of OOM kernel, OOM unit, user kill process, and user unit signal. Each fixture needs the expected positive token and DRIFT verdict.

## Verification gaps
- No execution performed (per assignment). The jq behaviour claims (`"str" | .MESSAGE_ID` errors; `tostring` on arrays) are from jq semantics, not run here [INFERENCE: standard jq semantics; L1 should confirm with the pinned jq].
- Production positive code does not exist yet, so the findings above describe the required change, not observed behaviour.
