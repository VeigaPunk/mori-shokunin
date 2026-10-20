# ReconResultEmitter: S036 / S038 Result Enum & Emitter Research (Round 15, C1)

- **Seat**: `MoriR15.ReconResultEmitter` (role: scout, leaf member).
- **Judged on**: `coverage` (claim C1: preserve critical OOM and user signal alarms from individually valid current-boot structured records without fabricating totals).
- **Milestone**: retain validated positives without fabricated totals.
- **Report path**: `.ufo/waves/round-15/build/ReconResultEmitter.md` (relative to `/home/vgpnk/Projects/shokunin/mori-shokunin`).
- **Tooling record**: no packages installed or updated. Host safety notice acknowledged (sync DB ~413 packages ahead); no package management commands executed. Pinned source artifacts `/tmp/unit.c` and `/tmp/service.c` verified via local SHA-256 computation against registered registry digests.

---

## 1. Named Axes

1. **Coverage (Judged Axis)**:
   - Preserve critical OOM alarms (`OOM_KILL_JOURNAL crit`) and user signal warnings (`KILL_SIGNAL_JOURNAL warn`) whenever individually valid, current-boot structured evidence records exist in the journal stream.
   - Prevent alarm suppression caused by an adjacent malformed, non-matching, or foreign-boot record invalidating the aggregate class.
2. **Operability (Context Axis)**:
   - Raw aggregate totals and split classifications must remain strictly `unavailable:<reason>` when invalid or unparsable.
   - Never fabricate, guess, or extrapolate total record counts from partial positive evidence.
   - Positive evidence tokens (`positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`) report verified counts of valid current-boot records; they remain `unavailable:<reason>` on capture/parse failure, never defaulting to numeric zero `0`.

---

## 2. Primary Source Inspection & Hashing

Both primary sources were opened and verified at pinned upstream systemd master commit `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af`:

| Source ID | Primary URL / File Path | Kind | Tier | SHA-256 Digest | Status |
|---|---|---|---|---|---|
| **S036** | `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c` | code | A | `4833056a6313b250ad6b53de3121a51e8dee602733e1aedf4a7d3d2687d547ed` | Verified (`/tmp/unit.c`) |
| **S038** | `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c` | code | A | `669cccf4356bd838b0ac9541ef435c9c1307f989a36f2c0f35584b8184d7731f` | Verified (`/tmp/service.c`) |
| **Supporting** | `src/core/service.h` (in `/tmp/systemd-pin.tgz`) | code | A | `d14efd3f8bcacd735ad70b4b768adc786c449bab4bc366b9617c3218ea94b0d1` | Verified (archive read) |
| **Supporting** | `src/core/scope.c` (in `/tmp/systemd-pin.tgz`) | code | A | `8f1e031a0279d0be38e3e4a74fe3eb03a89182312d8a4369e96f1d82121e42ea` | Verified (archive read) |
| **Supporting** | `src/basic/process-util.c` (in `/tmp/systemd-pin.tgz`) | code | A | `a749f285bf168bdbb74bc7021055e8f121ec7a0bbbcb6a40e40283f5f699a4fe` | Verified (archive read) |
| **Supporting** | `src/systemd/sd-messages.h` (in `/tmp/systemd-pin.tgz`) | code | A | `fb613f71807344eb29b9353cad8c09cb644fff4a18b1651fda9b49e0a23064fc` | Verified (archive read) |

---

## 3. Exact OOM and Signal Result Enum Sources

### 3.1 Primary Authority S036: `src/core/unit.c` Emitter

S036 is the core systemd unit emitter responsible for logging unit failures and process terminations with structured catalog message identifiers and structured fields.

#### Anchor 1: Unit Failure Emitter (`unit_log_failure`)
- **Path**: `src/core/unit.c:6333-6342`
- **Concrete Implementation**:
  ```c
  6333: void unit_log_failure(Unit *u, const char *result) {
  6334:         assert(u);
  6335:         assert(result);
  6336: 
  6337:         log_unit_struct(u, LOG_WARNING,
  6338:                         LOG_MESSAGE_ID(SD_MESSAGE_UNIT_FAILURE_RESULT_STR),
  6339:                         LOG_UNIT_INVOCATION_ID(u),
  6340:                         LOG_UNIT_MESSAGE(u, "Failed with result '%s'.", result),
  6341:                         LOG_ITEM("UNIT_RESULT=%s", result));
  6342: }
  ```
- **Located Quotes ($\le 25$ words)**:
  - `unit.c:6338`: `"LOG_MESSAGE_ID(SD_MESSAGE_UNIT_FAILURE_RESULT_STR),"` (1 word)
  - `unit.c:6340`: `"LOG_UNIT_MESSAGE(u, \"Failed with result '%s'.\", result),"` (6 words)
  - `unit.c:6341`: `"LOG_ITEM(\"UNIT_RESULT=%s\", result));"` (2 words)
- **Field & Message ID Provenance**:
  - `SD_MESSAGE_UNIT_FAILURE_RESULT_STR` maps in `src/systemd/sd-messages.h:178-179` to `SD_ID128_MAKE(d9,b3,73,ed,55,a6,4f,eb,82,42,e0,2d,be,79,a4,9c)` (hex: `d9b373ed55a64feb8242e02dbe79a49c`).
  - Writes structured field `UNIT_RESULT=%s` where string `%s` is passed directly from unit/service subsystem state.

#### Anchor 2: Unit Process Exit Emitter (`unit_log_process_exit`)
- **Path**: `src/core/unit.c:6355-6392`
- **Concrete Implementation**:
  ```c
  6355: void unit_log_process_exit(
  6356:                 Unit *u,
  6357:                 const char *kind,
  6358:                 const char *command,
  6359:                 bool success,
  6360:                 int code,
  6361:                 int status) {
  ...
  6372:         if (success)
  6373:                 level = LOG_DEBUG;
  6374:         else if (code == CLD_EXITED)
  6375:                 level = LOG_NOTICE;
  6376:         else
  6377:                 level = LOG_WARNING;
  6378: 
  6379:         log_unit_struct(u, level,
  6380:                         LOG_MESSAGE_ID(SD_MESSAGE_UNIT_PROCESS_EXIT_STR),
  6381:                         LOG_UNIT_MESSAGE(u, "%s exited, code=%s, status=%i/%s%s", ...),
  6388:                         LOG_ITEM("EXIT_CODE=%s", sigchld_code_to_string(code)),
  6389:                         LOG_ITEM("EXIT_STATUS=%i", status),
  6390:                         LOG_ITEM("COMMAND=%s", strna(command)),
  6391:                         LOG_UNIT_INVOCATION_ID(u));
  6392: }
  ```
- **Located Quotes ($\le 25$ words)**:
  - `unit.c:6380`: `"LOG_MESSAGE_ID(SD_MESSAGE_UNIT_PROCESS_EXIT_STR),"` (1 word)
  - `unit.c:6388`: `"LOG_ITEM(\"EXIT_CODE=%s\", sigchld_code_to_string(code)),"` (2 words)
  - `unit.c:6389`: `"LOG_ITEM(\"EXIT_STATUS=%i\", status),"` (2 words)
- **Field & Message ID Provenance**:
  - `SD_MESSAGE_UNIT_PROCESS_EXIT_STR` maps in `src/systemd/sd-messages.h:184-185` to `SD_ID128_MAKE(98,e3,22,20,3f,7a,4e,d2,90,d0,9f,e0,3c,09,fe,15)` (hex: `98e322203f7a4ed290d09fe03c09fe15`).
  - `EXIT_CODE`: derived from `sigchld_code_to_string(code)` (`src/basic/process-util.c:2308`), mapping `CLD_KILLED` to `"killed"`.
  - `EXIT_STATUS`: formatted via `%i` as an integer signal number (`status == 9` for `SIGKILL`).

---

### 3.2 Primary Authority S038: `src/core/service.c` Result Vocabulary & Enum Source

S038 establishes the exact string table and lookup mapping internal service failure enum values to the string literal emitted in `UNIT_RESULT`.

#### Anchor 1: Service Result String Table
- **Path**: `src/core/service.c:6588-6602`
- **Concrete Implementation**:
  ```c
  6588: static const char* const service_result_table[_SERVICE_RESULT_MAX] = {
  6589:         [SERVICE_SUCCESS]                 = "success",
  6590:         [SERVICE_FAILURE_RESOURCES]       = "resources",
  6591:         [SERVICE_FAILURE_PROTOCOL]        = "protocol",
  6592:         [SERVICE_FAILURE_TIMEOUT]         = "timeout",
  6593:         [SERVICE_FAILURE_EXIT_CODE]       = "exit-code",
  6594:         [SERVICE_FAILURE_SIGNAL]          = "signal",
  6595:         [SERVICE_FAILURE_CORE_DUMP]       = "core-dump",
  6596:         [SERVICE_FAILURE_WATCHDOG]        = "watchdog",
  6597:         [SERVICE_FAILURE_START_LIMIT_HIT] = "start-limit-hit",
  6598:         [SERVICE_FAILURE_OOM_KILL]        = "oom-kill",
  6599:         [SERVICE_SKIP_CONDITION]          = "exec-condition",
  6600: };
  6601: 
  6602: DEFINE_STRING_TABLE_LOOKUP(service_result, ServiceResult);
  ```
- **Located Quotes ($\le 25$ words)**:
  - `service.c:6594`: `"[SERVICE_FAILURE_SIGNAL] = \"signal\","` (2 words)
  - `service.c:6598`: `"[SERVICE_FAILURE_OOM_KILL] = \"oom-kill\","` (2 words)
  - `service.c:6602`: `"DEFINE_STRING_TABLE_LOOKUP(service_result, ServiceResult);"` (2 words)

#### Anchor 2: Service Result Enum Definition (`ServiceResult`)
- **Path**: `src/core/service.h:79-93`
- **Concrete Implementation**:
  ```c
  79: typedef enum ServiceResult {
  80:         SERVICE_SUCCESS,
  81:         SERVICE_FAILURE_RESOURCES,
  82:         SERVICE_FAILURE_PROTOCOL,
  83:         SERVICE_FAILURE_TIMEOUT,
  84:         SERVICE_FAILURE_EXIT_CODE,
  85:         SERVICE_FAILURE_SIGNAL,
  86:         SERVICE_FAILURE_CORE_DUMP,
  87:         SERVICE_FAILURE_WATCHDOG,
  88:         SERVICE_FAILURE_START_LIMIT_HIT,
  89:         SERVICE_FAILURE_OOM_KILL, /* OOM Kill by the Kernel or systemd-oomd */
  90:         SERVICE_SKIP_CONDITION,
  91:         _SERVICE_RESULT_MAX,
  92:         _SERVICE_RESULT_INVALID = -EINVAL,
  93: } ServiceResult;
  ```
- **Located Quotes ($\le 25$ words)**:
  - `service.h:85`: `"SERVICE_FAILURE_SIGNAL,"` (1 word)
  - `service.h:89`: `"SERVICE_FAILURE_OOM_KILL, /* OOM Kill by the Kernel or systemd-oomd */"` (9 words)

#### Anchor 3: Service Termination Callsite Passing Enum String to S036
- **Path**: `src/core/service.c:2518`
- **Implementation**:
  ```c
  2517:         } else {
  2518:                 unit_log_failure(UNIT(s), service_result_to_string(s->result));
  2519:                 end_state = SERVICE_FAILED;
  ```
- **Located Quote ($\le 25$ words)**:
  - `service.c:2518`: `"unit_log_failure(UNIT(s), service_result_to_string(s->result));"` (3 words)

#### Anchor 4: Corroboration in Scope Units (`src/core/scope.c`)
- **Path**: `src/core/scope.c:721-728`
- **Concrete Implementation**:
  ```c
  721: static const char* const scope_result_table[_SCOPE_RESULT_MAX] = {
  722:         [SCOPE_SUCCESS]           = "success",
  723:         [SCOPE_FAILURE_RESOURCES] = "resources",
  724:         [SCOPE_FAILURE_TIMEOUT]   = "timeout",
  725:         [SCOPE_FAILURE_OOM_KILL]  = "oom-kill",
  726: };
  727: 
  728: DEFINE_STRING_TABLE_LOOKUP(scope_result, ScopeResult);
  ```
- **Located Quote ($\le 25$ words)**:
  - `scope.c:725`: `"[SCOPE_FAILURE_OOM_KILL] = \"oom-kill\","` (2 words)

---

## 4. Scope Boundaries for Claim C1

Under Claim C1, the census must preserve critical OOM and user signal alarms from individually valid, current-boot structured records while keeping raw aggregate totals strictly unavailable when any adjacent record is invalid.

### 4.1 Positive Evidence Tokens

The contract requires four per-scope positive evidence tokens:
1. `positive_kernel_oom`:
   - Matches: JSON object with scalar `MESSAGE_ID == "fe6faa94e7774663a0da52717891d8ef"` and scalar `_BOOT_ID == $boot`.
   - Scope: user and system scopes.
2. `positive_unit_oom`:
   - Matches: JSON object with scalar `MESSAGE_ID == "d9b373ed55a64feb8242e02dbe79a49c"`, scalar `_BOOT_ID == $boot`, and scalar `UNIT_RESULT == "oom-kill"`.
   - Scope: user and system scopes.
   - Independence: does **not** require valid `UNIT` or `USER_UNIT` subject metadata. A unit failure record with missing or malformed subject name still evidences unit OOM termination.
3. `positive_unit_signal`:
   - Matches: JSON object with scalar `MESSAGE_ID == "d9b373ed55a64feb8242e02dbe79a49c"`, scalar `_BOOT_ID == $boot`, and scalar `UNIT_RESULT == "signal"`.
   - Scope: user and system scopes (user scope feeds `KILL_SIGNAL_JOURNAL warn`).
4. `positive_process_sigkill`:
   - Matches: JSON object with scalar `MESSAGE_ID == "98e322203f7a4ed290d09fe03c09fe15"`, scalar `_BOOT_ID == $boot`, scalar `EXIT_CODE == "killed"`, and scalar `EXIT_STATUS` equal to string `"9"` or integer `9`.
   - Scope: user and system scopes (user scope feeds `KILL_SIGNAL_JOURNAL warn`).

### 4.2 In-Scope vs. Out-of-Scope Boundaries

| Field / Dimension | In-Scope (Counts toward Positive Token) | Out-of-Scope (Excluded from Positive Count) |
|---|---|---|
| **JSON Carrier** | Single JSON object record inside the valid JSON array stream | Primitive JSON types (strings, numbers, booleans, null), top-level arrays |
| **Boot Match** | Scalar string `_BOOT_ID` strictly matching queried current boot | Non-matching boot ID, missing `_BOOT_ID`, array-wrapped boot ID `["..."]` |
| **Message ID** | Scalar string matching exact 32-char hex message ID | Mismatched ID, missing `MESSAGE_ID`, array-wrapped ID |
| **Unit Result** | Exact scalar string `"oom-kill"` (for OOM) or `"signal"` (for signal) | Non-matching strings (`"resources"`, `"timeout"`, `"exit-code"`, etc.), missing `UNIT_RESULT`, array `["oom-kill"]` |
| **Process Exit Code** | Exact scalar string `"killed"` | `"exited"`, `"dumped"`, missing `EXIT_CODE`, array `["killed"]` |
| **Process Exit Status** | Exact scalar integer `9` or decimal string `"9"` | Non-9 status (e.g. `15` for SIGTERM, `1` for SIGHUP), missing `EXIT_STATUS`, array `[9]` |
| **Subject Metadata** | Ignored for positive token evaluation | Irrelevant: subject defects affect aggregate routing, not positive evidence |
| **Stream Capture** | Clean stream (`CAP_RC=0`, empty stderr, valid JSON parse) | Nonzero exit code, stderr output, unparseable JSON stream $\rightarrow$ `unavailable:<reason>` |

---

## 5. Concrete Counterexamples for C1

### 5.1 Primary Counterexample: Aggregate Invalidation with Valid Positive Current-Boot OOM Record

Consider a journal query result for `unit_failure_record` (`MESSAGE_ID=d9b373ed...`) in the user journal containing two records:

```json
[
  {
    "_BOOT_ID": "11111111111111111111111111111111",
    "MESSAGE_ID": "d9b373ed55a64feb8242e02dbe79a49c",
    "USER_UNIT": "kagi-shokunin.service",
    "UNIT_RESULT": "oom-kill"
  },
  {
    "_BOOT_ID": "22222222222222222222222222222222",
    "MESSAGE_ID": "d9b373ed55a64feb8242e02dbe79a49c",
    "USER_UNIT": "ancient-service.service",
    "UNIT_RESULT": "oom-kill"
  }
]
```

- **R14 Pre-C1 Behavior**:
  1. `JOURNAL_JQ_TAIL` runs `all(.[]; ._BOOT_ID == $boot)`. Because record 2 belongs to boot `2222...`, `all()` evaluates to `false`.
  2. The parser evaluates `[.[]._BOOT_ID] | unique | length` $\rightarrow 2 > 1$, returning status `"multi-boot"`.
  3. The entire scoped class returns `unavailable:multi-boot`.
  4. Aggregate counters `unit_failure_record`, `unit_oom`, `user_unit_oom` fall to `unavailable`.
  5. The OOM check evaluates `user_unit_oom` as non-numeric, suppressing `oom_path_u=0`.
  6. **Defect**: If no kernel notice was logged, `OOM_KILL_JOURNAL crit` failed to fire, discarding valid evidence of an OOM event in the current boot.
- **R15 C1 Repaired Behavior**:
  1. The aggregate raw total and split counts stay strictly `unavailable:multi-boot` (preventing fabricated totals).
  2. The positive extraction evaluates record 1 independently: scalar current boot `1111...`, scalar message ID `d9b373ed...`, scalar `UNIT_RESULT="oom-kill"`.
  3. Positive token records: `positive_unit_oom=1`.
  4. Record 2 is excluded from positive tokens (foreign boot).
  5. The OOM evaluator observes `positive_unit_oom=1 > 0` and **fires `OOM_KILL_JOURNAL crit`** once, recording:
     `paths=unit_result_oom_kill ... positive_kernel_oom=0 positive_unit_oom=1`.

### 5.2 Negative Counterexamples: Non-Matching Records that Must NOT Trigger Positive Evidence

1. **Non-OOM / Non-Signal Unit Failure Result**:
   ```json
   {
     "_BOOT_ID": "11111111111111111111111111111111",
     "MESSAGE_ID": "d9b373ed55a64feb8242e02dbe79a49c",
     "USER_UNIT": "build.service",
     "UNIT_RESULT": "exit-code"
   }
   ```
   - Result is `"exit-code"`, mapped from `SERVICE_FAILURE_EXIT_CODE` (`service.c:6593`).
   - Does not match `"oom-kill"` or `"signal"`.
   - `positive_unit_oom=0`, `positive_unit_signal=0`. No OOM or signal alarm fired.
2. **Process Termination by Non-SIGKILL Signal (e.g. SIGTERM)**:
   ```json
   {
     "_BOOT_ID": "11111111111111111111111111111111",
     "MESSAGE_ID": "98e322203f7a4ed290d09fe03c09fe15",
     "EXIT_CODE": "killed",
     "EXIT_STATUS": "15"
   }
   ```
   - Process was killed (`CLD_KILLED`), but status is 15 (SIGTERM).
   - Does not match scalar `9`.
   - `positive_process_sigkill=0`. No warning raised.
3. **Array-Wrapped Result Type Mutation**:
   ```json
   {
     "_BOOT_ID": "11111111111111111111111111111111",
     "MESSAGE_ID": "d9b373ed55a64feb8242e02dbe79a49c",
     "UNIT_RESULT": ["oom-kill"]
   }
   ```
   - `UNIT_RESULT` is an array `["oom-kill"]`, not a scalar string.
   - Guard `(type == "string")` rejects it.
   - `positive_unit_oom=0`.
4. **Capture / Stream Failure (Nonzero RC or Stderr Output)**:
   - When `journalctl` terminates with exit code 1 or writes error bytes to stderr, the entire stream is suspect.
   - `positive_*` tokens evaluate to `unavailable:<reason>` (e.g. `unavailable:rc-1` or `unavailable:stderr-nonempty`), **never** numeric zero `0`.

---

## 6. Summary of Architectural Contract for Downstream Integrators

1. **Enum Authority**:
   - `SERVICE_FAILURE_OOM_KILL` $\rightarrow$ exact string `"oom-kill"` (S038 `service.c:6598` / `service.h:89`).
   - `SERVICE_FAILURE_SIGNAL` $\rightarrow$ exact string `"signal"` (S038 `service.c:6594` / `service.h:85`).
   - `CLD_KILLED` $\rightarrow$ exact string `"killed"` with status `9` (S036 `unit.c:6388-6389`, `process-util.c:2308`).
2. **Positive Filter Separation**:
   - Aggregate JQ validation (`all(.[]; ...)`) remains unchanged to ensure raw totals and split buckets are safely unavailable on corrupted streams.
   - A secondary per-record extraction on the same successfully parsed JSON stream extracts positive counts (`select(...) | length`) without being blocked by stream-wide `all()` failures.
3. **Alarm Triggers**:
   - `OOM_KILL_JOURNAL crit` triggers if `(positive_kernel_oom > 0) || (positive_unit_oom > 0)`.
   - `KILL_SIGNAL_JOURNAL warn` triggers in user scope if `(positive_process_sigkill > 0) || (positive_unit_signal > 0)`.
   - Aggregate tokens stay `unavailable`, preserving both signal detection and accounting integrity.
