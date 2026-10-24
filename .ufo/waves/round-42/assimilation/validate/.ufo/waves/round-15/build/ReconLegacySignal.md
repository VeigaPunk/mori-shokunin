# ReconLegacySignal — Round-15 C1 (Coverage) Read-Only Audit

**Seat:** `MoriR15.ReconLegacySignal`  
**Role:** `scout`  
**Judged on:** `coverage`  
**Milestone:** retain validated positives without fabricated totals  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Scope:** Read-only research of existing `KILL_SIGNAL` raw unavailable interface and independent unit-signal path.  
**Boundaries:** Leaf member — no subagent dispatch, no production edits, no verification execution, no test runs, no commits.  
**Tooling Directive Compliance:** No tools installed or updated. Host safety directive acknowledged (pacman dry-run check enforced, no `-Sy/-Syu/-U/-R`).

---

## 1. Executive Summary

In round 14, the user-scope warning `KILL_SIGNAL_JOURNAL warn` was restored across two structured arms:
1. `user:unit_sigkill_record` (`MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15`, `EXIT_CODE=killed`, `EXIT_STATUS=9`).
2. `user_unit_signal` (`MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c`, `UNIT_RESULT=signal`).

However, under the existing implementation in `tools/mori-census.sh`, both paths are evaluated through all-or-nothing aggregate `jq` filters (`if all(.[]; ...)`) wrapped in `JOURNAL_JQ_TAIL`. An adjacent malformed record, a nonmatching `MESSAGE_ID`, a foreign boot, or an array-wrapped `_BOOT_ID` marks the entire class as `record-invalid`, `multi-boot`, or `boot-mismatch`. At the finding emitter, `case "$ps"` and `case "$us"` discard `unavailable:*` tokens, completely suppressing `KILL_SIGNAL_JOURNAL warn` even when an individually valid current-boot signal or SIGKILL record is present in the stream.

Claim C1 repairs this alarm suppression by introducing validated positive evidence tokens (`positive_process_sigkill`, `positive_unit_signal`) that fire the user signal warning while keeping raw aggregate counts unavailable.

---

## 2. Existing KILL_SIGNAL Raw Unavailable Interface

### Code Anchors in `tools/mori-census.sh`

1. **Identifier and Predicate Declarations (`:969–976`):**
   - Line 969: `JOURNAL_ID_UNIT_SIGKILL=98e322203f7a4ed290d09fe03c09fe15`
   - Line 970: `JOURNAL_ID_UNIT_FAILURE=d9b373ed55a64feb8242e02dbe79a49c`
   - Line 973: `JOURNAL_JQ_TAIL='then [length, ([.[]._BOOT_ID] | unique | length), ([.[]._BOOT_ID][0] // "none")] | @tsv else (if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and ((._BOOT_ID | length) > 0)) then ([.[]._BOOT_ID] | unique | length) as $b | if $b > 1 then "multi-boot" elif all(.[]; ._BOOT_ID == $boot) then "record-invalid" else "boot-mismatch" end else "record-invalid" end) end'`
   - Line 975: `JOURNAL_JQ_SIGKILL="if all(.[]; type == \"object\" and (._BOOT_ID | type) == \"string\" and (._BOOT_ID == \$boot) and (.MESSAGE_ID == \$id) and (.EXIT_CODE == \"killed\") and ((.EXIT_STATUS | tostring) == \"9\")) $JOURNAL_JQ_TAIL"`
   - Lines 1001–1037: `JOURNAL_JQ_UNITS` wraps unit-failure splitting in `if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and (._BOOT_ID == $boot) and (.MESSAGE_ID == $id)) then ... else ... end`.

2. **Query Status Mapping in `journal_query` (`:1083–1136`):**
   - Lines 1083–1089: If process return code is non-zero, sets `JQ_STATUS="rc-$CAP_RC"` or `timeout`.
   - Lines 1091–1094: If stderr byte count > 0, sets `JQ_STATUS="stderr-nonempty"`.
   - Lines 1102: If jq parsing fails, sets `JQ_STATUS="malformed-json"`.
   - Lines 1103–1105: If jq output returns `record-invalid`, `multi-boot`, or `boot-mismatch`, `JQ_STATUS` takes that literal token and returns early.
   - Lines 1111–1135: Column count mismatches or non-integer fields also fall back to `malformed-json` or `record-invalid`.

3. **Query Invocations in `probe_journal` (`:1187–1230`):**
   - Lines 1195–1196: `journal_query "$flag" '_BOOT_ID,MESSAGE_ID,EXIT_CODE,EXIT_STATUS' "MESSAGE_ID=$JOURNAL_ID_UNIT_SIGKILL EXIT_CODE=killed EXIT_STATUS=9" "$JOURNAL_JQ_SIGKILL" --arg boot "$BOOT_ID_EXPECTED" --arg id "$JOURNAL_ID_UNIT_SIGKILL"`
   - Lines 1197–1217: `JOURNAL_Q_WIDTH=15 journal_query "$flag" '_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT' "MESSAGE_ID=${ids[$cls]}" "$JOURNAL_JQ_UNITS" --arg boot "$BOOT_ID_EXPECTED" --arg id "${ids[$cls]}" --arg fleet "$FLEET_UNIT_TOKENS"`
   - Line 1221: `jn[$key]=$JQ_N; js[$key]=$JQ_STATUS`

4. **User `KILL_SIGNAL_JOURNAL warn` Gating (`:1334–1354`):**
   ```bash
   key='user:unit_sigkill_record'
   if [ "${js[$key]}" = ok ]; then ps=${jn[$key]}; else ps="unavailable:${js[$key]}"; fi
   key='user:unit_failure_record'
   if [ "${js[$key]}" = ok ]; then us=${ucnt["user:signal"]}; else us="unavailable:${js[$key]}"; fi
   case "$ps" in
     unavailable:*) ;;
     *) if [ "$ps" -gt 0 ]; then kill_fire=1; kill_paths=process_sigkill; fi ;;
   esac
   case "$us" in
     unavailable:*) ;;
     *) if [ "$us" -gt 0 ]; then kill_fire=1; kill_paths="${kill_paths:+$kill_paths,}unit_result_signal"; fi ;;
   esac
   if [ "$kill_fire" -eq 1 ]; then
     emit_finding KILL_SIGNAL_JOURNAL warn "class=kill_signal paths=$kill_paths count=$ps process_sigkill=$ps user_unit_signal=$us scope=user attribution=none basis=scoped-record-count boot=$BOOT_ID_EXPECTED note=unit process exited on SIGKILL and/or unit failed with result signal; cause unknown (a kernel OOM can also deliver SIGKILL); counters are separate and never summed"
   fi
   ```

5. **Surface Token Emission (`:1360–1379`):**
   - Lines 1362–1367: `cls=unit_sigkill_record`: if `js[$key] != ok`, emits `unit_sigkill_record=unavailable:${js[$key]}`.
   - Lines 1374–1378: `uf=signal`: if `js[$key] != ok`, emits `unit_signal=unavailable:${js[$key]}`.

### Unavailable Semantics

When `js[$key]` is not `ok`, both `ps` and `us` receive `unavailable:<reason>` strings. The `case` statements explicitly drop `unavailable:*` without setting `kill_fire=1`. If either path has an invalid record, its count is lost to `unavailable:*`. If both paths encounter an invalid record (or one is 0 and the other is `unavailable:*`), `kill_fire` remains `0`, and `KILL_SIGNAL_JOURNAL warn` is completely suppressed.

---

## 3. Independent Unit-Signal Path

### Architecture and Origins

1. **Historical Text Origin:**
   Prior to round 13, the legacy text grep scanned journal output for `Failed with result 'signal'`. This matched raw message text indiscriminately.
2. **Round-14 Structured Replacement:**
   In round 14, `user_unit_signal` was anchored to catalog ID `d9b373ed55a64feb8242e02dbe79a49c` with `UNIT_RESULT="signal"`.
3. **Independence from `process_sigkill`:**
   - `process_sigkill` represents an individual process exit notification (`MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15`) carrying `EXIT_CODE=killed` and `EXIT_STATUS=9`.
   - `user_unit_signal` represents a unit state transition to `failed` (`MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c`) carrying `UNIT_RESULT=signal`.
   - The two paths are separate and never summed (`process_sigkill=$ps user_unit_signal=$us`).
   - A unit signal result alone is sufficient to flip DRIFT via `KILL_SIGNAL_JOURNAL warn` (verified in round-14 fixture `R14_UNIT_SIGNAL_WARN`: `paths=unit_result_signal count=0 process_sigkill=0 user_unit_signal=1`).
4. **Subject Metadata Independence:**
   Per `journal-alarm-routing-r14.md` and `tools/mori-census.sh:945`, subject metadata (`UNIT` / `USER_UNIT`) validity never gates the alarm. An unattributed, missing, or malformed subject unit record with `UNIT_RESULT=signal` still constitutes a valid signal alarm.
5. **Coupling Defect in Existing Implementation:**
   In r14, `user_unit_signal` is computed in the same 15-column jq pass as the subject unit partition (`fleet`, `nonfleet`, `unknown`) and `oom` results. Because `JOURNAL_JQ_UNITS` is aggregate-gated with `if all(.[]; ...)`, a defect in any other record in that query invalidates `user:unit_failure_record`, wiping out `user_unit_signal`.

---

## 4. Primary Named Sources

### S035: systemd Process-Exit and Unit-Result Catalog
- **URL:** `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in`
- **Pinned Commit:** `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` (2026-10-19)
- **Unit Failed Anchor:** `catalog/systemd.catalog.in:561–566` (`d9b373ed55a64feb8242e02dbe79a49c`)
  - **Quote (≤25 words):**
    > "The unit @UNIT@ has entered the 'failed' state with result '@UNIT_RESULT@'." (11 words)
- **Process Exit Anchor:** `catalog/systemd.catalog.in:568–575` (`98e322203f7a4ed290d09fe03c09fe15`)
  - **Quote (≤25 words):**
    > "The process' exit code is '@EXIT_CODE@' and its exit status is @EXIT_STATUS@." (12 words)

### S036: systemd Unit Termination Emitter
- **URL:** `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c`
- **Pinned Commit:** `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` (2026-10-19)
- **Anchors:**
  - `src/core/unit.c:6333–6342` (`unit_log_failure`): Line 6342: `LOG_ITEM("UNIT_RESULT=%s", result));`
  - `src/core/unit.c:6355–6392` (`unit_log_process_exit`): Lines 6388–6389:
    `LOG_ITEM("EXIT_CODE=%s", sigchld_code_to_string(code)),`
    `LOG_ITEM("EXIT_STATUS=%i", status));`
  - **Quote (≤25 words):**
    > "The process' exit code is '%s' and its exit status is %i." (12 words)

### S038: systemd Service Result Vocabulary
- **URL:** `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c`
- **Pinned Commit:** `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` (2026-10-19)
- **Anchor:** `src/core/service.c:6588–6602` (`service_result_table`), Line 6593:
  - `[SERVICE_FAILURE_SIGNAL] = "signal",`
  - **Quote (≤25 words):**
    > `[SERVICE_FAILURE_SIGNAL] = "signal",` (3 words)

### S015: systemd Journal Fields Reference
- **URL:** `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html`
- **Anchor:** User Journal Fields (`MESSAGE_ID=`), Trusted Journal Fields (`_BOOT_ID=`)
  - **Quote (≤25 words):**
    > "User fields are fields that are directly passed from clients and stored in the journal." (14 words)

### S014: journalctl Reference
- **URL:** `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html`
- **Anchor:** Output Options `--output-fields=`, JSON format
  - **Quote (≤25 words):**
    > "If a non-unique field is encountered a JSON array is used as field value." (13 words)

---

## 5. Scope Boundaries

1. **User vs System Scope:**
   - `KILL_SIGNAL_JOURNAL warn` is strictly a **user-scope** warning. A user-scope signal result or process SIGKILL flips DRIFT.
   - In system scope, `unit_sigkill_record` emits `KILL_SIGNAL_JOURNAL_SYSTEM info` (`tools/mori-census.sh:1147, 1250`). System scope does not emit a unit-signal finding or warning.
2. **Raw Aggregate Counts vs Validated Positive Tokens:**
   - Raw tokens (`unit_sigkill_record=`, `unit_signal=`, `unit_fleet=`, etc.) remain aggregate-only. If any record in the query is invalid, the raw count MUST stay `unavailable:<reason>` (e.g. `unavailable:record-invalid`). It must NEVER be reported as `0` or as a partial sum.
   - Validated positive evidence tokens (`positive_process_sigkill`, `positive_unit_signal`):
     - Count ONLY object records with scalar matching `MESSAGE_ID` and scalar current `_BOOT_ID`.
     - `positive_process_sigkill` requires `EXIT_CODE="killed"` and scalar `EXIT_STATUS="9"`.
     - `positive_unit_signal` requires exact string `UNIT_RESULT="signal"`.
     - Derived from the same captured, successful, stderr-free valid JSON stream (`CAP_OUT`) without running an extra journal query.
     - If capture or parser fails (`rc != 0`, `stderr-nonempty`, `malformed-json`, `timeout`, `no-timeout-bin`), positive tokens must report `unavailable:<reason>`.
3. **Alarm Emission Contract:**
   - `KILL_SIGNAL_JOURNAL warn` MUST fire if `positive_process_sigkill > 0` OR `positive_unit_signal > 0` (or legacy `ps > 0` / `us > 0`).
   - The warning retains its finding fields: `paths=$kill_paths count=$ps process_sigkill=$ps user_unit_signal=$us` and appends validated positive evidence tokens (`positive_process_sigkill`, `positive_unit_signal`).
   - Counters are separate and never summed.

---

## 6. Counterexample for C1

### Scenario: Valid User Unit Signal Record Beside Foreign Boot Record

Consider a user journal response containing two records for `unit_failure_record`:

**Payload Stream:**
```json
{"_BOOT_ID":"11111111111111111111111111111111","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"shokunin.service","UNIT_RESULT":"signal"}
{"_BOOT_ID":"22222222222222222222222222222222","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"shokunin.service","UNIT_RESULT":"signal"}
```
*(Assume expected boot is `11111111111111111111111111111111`, and `user:unit_sigkill_record` returned 0 records).*

### Existing r14 Behavior (Vulnerability)
1. `journal_query` runs `JOURNAL_JQ_UNITS` against the 2-record stream.
2. In `JOURNAL_JQ_UNITS` (`:1019`), `if all(.[]; ... and (._BOOT_ID == $boot) ...)` fails because the second record belongs to a different boot (`2222...`).
3. The `else` clause at line 1037 detects two unique boot IDs (`$b > 1`) and returns `"multi-boot"`.
4. Line 1104 matches `"multi-boot"` and sets `JQ_STATUS=multi-boot`.
5. Line 1221 sets `js['user:unit_failure_record']="multi-boot"`.
6. Line 1343 evaluates:
   `us="unavailable:multi-boot"`
7. Lines 1348–1351 evaluate:
   ```bash
   case "$us" in
     unavailable:*) ;; # Match! Skipped!
     *) if [ "$us" -gt 0 ]; then kill_fire=1; kill_paths="${kill_paths:+$kill_paths,}unit_result_signal"; fi ;;
   esac
   ```
8. `kill_fire` remains `0`.
9. Line 1352: `if [ "$kill_fire" -eq 1 ]` evaluates to FALSE.
10. `KILL_SIGNAL_JOURNAL warn` is **NOT emitted**. The census rolls `CLEAN`, silently dropping a critical alarm caused by an actual process/unit crash during the current boot.

### Required C1 Behavior
1. Aggregate status remains `unavailable:multi-boot`.
2. Raw surface tokens in `SURFACE journal.user` remain `unit_failure_record=unavailable:multi-boot`, `unit_signal=unavailable:multi-boot`, `unit_fleet=unavailable:multi-boot`, etc. No fabricated total is generated.
3. The validated-positive pass scans the same parsed JSON stream:
   - Record 1 is an object with scalar `_BOOT_ID=="11111111111111111111111111111111"`, matching `MESSAGE_ID=="d9b373ed55a64feb8242e02dbe79a49c"`, and exact string `UNIT_RESULT=="signal"`. It increments `positive_unit_signal` to `1`.
   - Record 2 fails the scalar boot match and is safely excluded from positive evidence.
4. Positive token is emitted in `SURFACE journal.user` as `positive_unit_signal=1`.
5. Alarm evaluator checks `positive_unit_signal > 0` and sets `kill_fire=1` and `kill_paths=unit_result_signal`.
6. `emit_finding KILL_SIGNAL_JOURNAL warn` **fires**, preserving the DRIFT roll while honestly reflecting `process_sigkill=0 user_unit_signal=unavailable:multi-boot positive_unit_signal=1`.

---

## 7. Remaining Unknowns and Non-Goals

1. **Non-Goals:**
   - No attempt to authenticate client-supplied `MESSAGE_ID` or `USER_UNIT` fields (`trust=client-supplied`).
   - No attempt to identify the specific signal number (e.g. SIGTERM vs SIGABRT vs SIGKILL) or sender PID for `UNIT_RESULT=signal` records; the catalog and service result table provide no such fields.
   - No repair of invalid JSON streams or synthesis of aggregate counts when stream validation fails.
2. **Remaining Unknowns:**
   - Whether the harness runner will accept `positive_unit_signal` appended to the finding's observation string or requires an exact field format. (Checked: existing regex `:3043`, `:3121` uses `.*user_unit_signal=1 .*scope=user`, which tolerates appended tokens).
   - Exact naming of positive surface tokens: `spec.json` specifies `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`.
