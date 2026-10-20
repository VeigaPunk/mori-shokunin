# MoriR14.EmitterSource — pinned S036 unit.c trace, service UNIT_RESULT oom-kill anchor, and safe journal field routing

Seat: MoriR14.EmitterSource (role: scout, leaf member).
Milestone: restore OOM alarm and structured fleet routing.
Axis: coverage.
Report path: `.ufo/waves/round-14/build/EmitterSource.md` (relative to `/home/vgpnk/Projects/shokunin/mori-shokunin`).

Scope: open pinned primary authority S036 (`src/core/unit.c`), trace `unit_log_failure`, `unit_log_process_exit`, and `log_unit` macros/functions (`UNIT=` vs `USER_UNIT=`), locate concrete anchors and located quotes, trace direct primary anchors for `UNIT_RESULT=oom-kill` from service/scope string tables (`service.c` / `service.h`), note registered S038 covering `service.c:6588-6602`, and recommend safe journal field selection and result classification. Report only. No production file edits, no tests, no sibling writes.

Tooling record: no tools installed or updated. Existing `/tmp/unit.c` artifact verified against pinned SHA-256 digest.

---

## 1. Primary Authority: S036 `unit.c`

| Attribute | Observed Value |
|---|---|
| Source ID | **S036** (registered in `corpus/SOURCES.md:42`) |
| URL | `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c` |
| Commit | `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` (systemd upstream master, 2026-10-19) |
| SHA-256 Digest | `4833056a6313b250ad6b53de3121a51e8dee602733e1aedf4a7d3d2687d547ed` |
| Recheck Command | `curl -fsSL https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c \| sha256sum` |
| Access Date | 2026-10-20 |

Supporting source files inspected at the same pinned commit `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af`:
- `src/core/unit.h` — macro definitions `log_unit_struct`, `LOG_UNIT_ID`, `LOG_UNIT_INVOCATION_ID`, `LOG_UNIT_MESSAGE` (:1166–1196); inline `unit_log_result` (:1058–1063).
- `src/core/service.c` — service termination callsite `:2518`, `service_result_table` `:6588–6600`, string lookup `:6602` (sha256: `669cccf4356bd838b0ac9541ef435c9c1307f989a36f2c0f35584b8184d7731f`). Proposed as **S038** below.
- `src/core/service.h` — `ServiceResult` enum definition and comment at `:79–93` (sha256: `d14efd3f8bcacd735ad70b4b768adc786c449bab4bc366b9617c3218ea94b0d1`).
- `src/core/scope.c` — scope dead state callsite `:273`, `scope_result_table` `:721–728`.
- `src/systemd/sd-messages.h` — message catalog IDs `SD_MESSAGE_UNIT_FAILURE_RESULT` (:178–179), `SD_MESSAGE_UNIT_PROCESS_EXIT` (:184–185), `SD_MESSAGE_UNIT_OUT_OF_MEMORY` (:198–199).
- `src/basic/process-util.c` — `sigchld_code_to_string` (`CLD_KILLED` → `"killed"`, :2308).

---

## 2. Trace: `unit_log_failure` in S036

### 2.1 Implementation and Concrete Source Anchors

In `src/core/unit.c:6333–6342`:

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

### 2.2 Located Quotes (≤25 words)

- `unit.c:6338`: `"LOG_MESSAGE_ID(SD_MESSAGE_UNIT_FAILURE_RESULT_STR),"` (1 word)
- `unit.c:6340`: `"LOG_UNIT_MESSAGE(u, \"Failed with result '%s'.\", result),"` (6 words)
- `unit.c:6341`: `"LOG_ITEM(\"UNIT_RESULT=%s\", result));"` (2 words)

### 2.3 Emitted Field Analysis

1. **Log Level**: Fixed at `LOG_WARNING` (severity 4).
2. **`MESSAGE_ID`**: Emits `SD_MESSAGE_UNIT_FAILURE_RESULT_STR`.
   - Mapped in `src/systemd/sd-messages.h:178–179` to `SD_ID128_MAKE(d9,b3,73,ed,55,a6,4f,eb,82,42,e0,2d,be,79,a4,9c)`.
   - String hex: `d9b373ed55a64feb8242e02dbe79a49c`.
3. **`UNIT_RESULT`**: Explicit structured field `UNIT_RESULT=%s`.
   - Passes the string argument `const char *result` directly to `LOG_ITEM("UNIT_RESULT=%s", result)`.
   - `unit.c` does not hardcode enum strings itself; concrete string values originate from the subsystem string tables (e.g., `service_result_table`, `scope_result_table`), detailed in Section 3.
4. **Subject Unit Identity**: Appended automatically by `log_unit_struct` (see Section 5):
   - System manager instance (`MANAGER_IS_SYSTEM`): `UNIT=%s`
   - User manager instance (`MANAGER_IS_USER`): `USER_UNIT=%s`
   *(Note: Manager type indicates which manager emitted the record, independent of whether the record is read from system or user journal storage).*
5. **Invocation ID**: Appended via `LOG_UNIT_INVOCATION_ID(u)`:
   - System manager instance: `INVOCATION_ID=%s`
   - User manager instance: `USER_INVOCATION_ID=%s`
6. **`MESSAGE`**: Formatted display string `"%s: Failed with result '%s'."` (prefixed with unit ID). `MESSAGE` must never be parsed for metadata (S015 / QUALITY #15).

---

## 3. Direct Primary Anchors for `UNIT_RESULT=oom-kill`

To avoid inventing enum semantics or presuming string values from generic `unit_log_failure`, we open the primary string table and termination callsites in `src/core/service.c` and `src/core/service.h`.

### 3.1 Service Result String Table in `src/core/service.c`

In `src/core/service.c:6588–6602`:

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

### 3.2 Service Failure Callsite in `src/core/service.c`

In `src/core/service.c:2506–2521` (within `service_enter_dead`):

```c
2506:         if (s->result == SERVICE_SUCCESS || f == SERVICE_FAILURE_START_LIMIT_HIT)
2507:                 s->result = f;
2508: 
2509:         if (s->result == SERVICE_SUCCESS) {
2510:                 unit_log_success(UNIT(s));
2511:                 end_state = service_determine_dead_state(s);
2512:                 restart_state = SERVICE_DEAD_BEFORE_AUTO_RESTART;
2513:         } else if (s->result == SERVICE_SKIP_CONDITION) {
2514:                 unit_log_skip(UNIT(s), service_result_to_string(s->result));
2515:                 end_state = service_determine_dead_state(s);
2516:                 restart_state = _SERVICE_STATE_INVALID; /* Never restart if skipped due to condition failure */
2517:         } else {
2518:                 unit_log_failure(UNIT(s), service_result_to_string(s->result));
2519:                 end_state = SERVICE_FAILED;
2520:                 restart_state = SERVICE_FAILED_BEFORE_AUTO_RESTART;
2521:         }
```

Line `service.c:2518` explicitly calls `unit_log_failure(UNIT(s), service_result_to_string(s->result));`. When `s->result == SERVICE_FAILURE_OOM_KILL`, `service_result_to_string()` returns `"oom-kill"`, emitting journal field `UNIT_RESULT=oom-kill`.

### 3.3 Semantic Definition in `src/core/service.h`

In `src/core/service.h:79–93`:

```c
79: typedef enum ServiceResult {
80:         SERVICE_SUCCESS,
81:         SERVICE_FAILURE_RESOURCES, /* a bit of a misnomer, just our catch-all error for errnos we didn't expect */
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

Line `service.h:89` proves the exact semantics directly from primary systemd source:
`/* OOM Kill by the Kernel or systemd-oomd */`.

### 3.4 Corroboration in Scope Units (`src/core/scope.c`)

Scope units (which manage process trees such as sessions and transient jobs) use the identical string:
- `src/core/scope.c:721–728`:
  ```c
  static const char* const scope_result_table[_SCOPE_RESULT_MAX] = {
          [SCOPE_SUCCESS]           = "success",
          [SCOPE_FAILURE_RESOURCES] = "resources",
          [SCOPE_FAILURE_TIMEOUT]   = "timeout",
          [SCOPE_FAILURE_OOM_KILL]  = "oom-kill",
  };
  DEFINE_STRING_TABLE_LOOKUP(scope_result, ScopeResult);
  ```
- `src/core/scope.c:273`:
  `unit_log_result(UNIT(s), s->result == SCOPE_SUCCESS, scope_result_to_string(s->result));`
  which delegates directly to `unit_log_failure(u, result)` via `src/core/unit.h:1058–1063`:
  ```c
  static inline void unit_log_result(Unit *u, bool success, const char *result) {
          if (success)
                  unit_log_success(u);
          else
                  unit_log_failure(u, result);
  }
  ```

### 3.5 Located Quotes for `UNIT_RESULT=oom-kill` (≤25 words)

- `service.c:2518`: `"unit_log_failure(UNIT(s), service_result_to_string(s->result));"` (4 words)
- `service.c:6598`: `"[SERVICE_FAILURE_OOM_KILL] = \"oom-kill\","` (3 words)
- `service.c:6602`: `"DEFINE_STRING_TABLE_LOOKUP(service_result, ServiceResult);"` (2 words)
- `service.h:89`: `"SERVICE_FAILURE_OOM_KILL, /* OOM Kill by the Kernel or systemd-oomd */"` (9 words)
- `scope.c:725`: `"[SCOPE_FAILURE_OOM_KILL] = \"oom-kill\","` (3 words)

---

## 4. Trace: `unit_log_process_exit` in S036

### 4.1 Implementation and Concrete Source Anchors

In `src/core/unit.c:6355–6392`:

```c
6355: void unit_log_process_exit(
6356:                 Unit *u,
6357:                 const char *kind,
6358:                 const char *command,
6359:                 bool success,
6360:                 int code,
6361:                 int status) {
6362: 
6363:         int level;
6364: 
6365:         assert(u);
6366:         assert(kind);
6367: 
6368:         /* If this is a successful exit, let's log about the exit code on DEBUG level. If this is a failure
6369:          * and the process exited on its own via exit(), then let's make this a NOTICE, under the assumption
6370:          * that the service already logged the reason at a higher log level on its own. Otherwise, make it a
6371:          * WARNING. */
6372:         if (success)
6373:                 level = LOG_DEBUG;
6374:         else if (code == CLD_EXITED)
6375:                 level = LOG_NOTICE;
6376:         else
6377:                 level = LOG_WARNING;
6378: 
6379:         log_unit_struct(u, level,
6380:                         LOG_MESSAGE_ID(SD_MESSAGE_UNIT_PROCESS_EXIT_STR),
6381:                         LOG_UNIT_MESSAGE(u, "%s exited, code=%s, status=%i/%s%s",
6382:                                          kind,
6383:                                          sigchld_code_to_string(code), status,
6384:                                          strna(code == CLD_EXITED
6385:                                                ? exit_status_to_string(status, EXIT_STATUS_FULL)
6386:                                                : signal_to_string(status)),
6387:                                          success ? " (success)" : ""),
6388:                         LOG_ITEM("EXIT_CODE=%s", sigchld_code_to_string(code)),
6389:                         LOG_ITEM("EXIT_STATUS=%i", status),
6390:                         LOG_ITEM("COMMAND=%s", strna(command)),
6391:                         LOG_UNIT_INVOCATION_ID(u));
6392: }
```

### 4.2 Located Quotes (≤25 words)

- `unit.c:6372-6377`: `"if (success) level = LOG_DEBUG; else if (code == CLD_EXITED) level = LOG_NOTICE; else level = LOG_WARNING;"` (17 words)
- `unit.c:6380`: `"LOG_MESSAGE_ID(SD_MESSAGE_UNIT_PROCESS_EXIT_STR),"` (1 word)
- `unit.c:6388`: `"LOG_ITEM(\"EXIT_CODE=%s\", sigchld_code_to_string(code)),"` (2 words)
- `unit.c:6389`: `"LOG_ITEM(\"EXIT_STATUS=%i\", status),"` (2 words)
- `unit.c:6390`: `"LOG_ITEM(\"COMMAND=%s\", strna(command)),"` (2 words)

### 4.3 Emitted Field Analysis

1. **Log Level**: Dynamically selected:
   - `LOG_DEBUG` if `success == true`.
   - `LOG_NOTICE` if process exited on its own via `exit()` (`code == CLD_EXITED`).
   - `LOG_WARNING` for abnormal termination (`CLD_KILLED` or `CLD_DUMPED`).
2. **`MESSAGE_ID`**: Emits `SD_MESSAGE_UNIT_PROCESS_EXIT_STR`.
   - Mapped in `src/systemd/sd-messages.h:184–185` to `SD_ID128_MAKE(98,e3,22,20,3f,7a,4e,d2,90,d0,9f,e0,3c,09,fe,15)`.
   - String hex: `98e322203f7a4ed290d09fe03c09fe15`.
3. **`EXIT_CODE`**: Emits string via `sigchld_code_to_string(code)` (`src/basic/process-util.c:2308`):
   - `CLD_KILLED` → `"killed"`
   - `CLD_EXITED` → `"exited"`
   - `CLD_DUMPED` → `"dumped"`
   - `CLD_TRAPPED` → `"trapped"`
   - `CLD_STOPPED` → `"stopped"`
   - `CLD_CONTINUED` → `"continued"`
4. **`EXIT_STATUS`**: Emits formatted integer `%i` (decimal string, e.g. `9` for SIGKILL, `11` for SIGSEGV, or exit code `0..255`).
5. **`COMMAND`**: Emits command string or `"n/a"`.
6. **Subject Unit Identity**: Appended automatically by `log_unit_struct` (Section 5):
   - System manager instance (`MANAGER_IS_SYSTEM`): `UNIT=%s`
   - User manager instance (`MANAGER_IS_USER`): `USER_UNIT=%s`
7. **Invocation ID**: `INVOCATION_ID=%s` (system manager) / `USER_INVOCATION_ID=%s` (user manager).

---

## 5. Trace: `log_unit` `UNIT` vs `USER_UNIT` Fields

### 5.1 Macro Expansion Chain in `src/core/unit.h`

In `src/core/unit.h:1166–1196`:

```c
1166: #define log_unit_struct_errno(unit, level, error, ...)                  \
1167:         ({                                                              \
1168:                 const Unit *_u = (unit);                                \
1169:                 const int _l = (level);                                 \
1170:                 LOG_CONTEXT_SET_LOG_LEVEL(unit_get_log_level_max(_u));  \
1171:                 const ExecContext *_c = _u ? unit_get_exec_context(_u) : NULL; \
1172:                 LOG_CONTEXT_PUSH_IOV(_c ? _c->log_extra_fields : NULL,  \
1173:                                      _c ? _c->n_log_extra_fields : 0);  \
1174:                 log_struct_errno(_l, error, __VA_ARGS__, LOG_UNIT_ID(_u)); \
1175:         })
1176: 
1177: #define log_unit_struct(unit, level, ...) log_unit_struct_errno(unit, level, 0, __VA_ARGS__)
...
1194: #define LOG_UNIT_ID(unit) LOG_ITEM("%s%s", unit_log_field((unit)), (unit)->id)
1195: #define LOG_UNIT_INVOCATION_ID(unit) LOG_ITEM("%s%s", unit_invocation_log_field((unit)), (unit)->invocation_id_string)
```

### 5.2 Field Name Dispatch Functions in `src/core/unit.c`

In `src/core/unit.c:6995–7001`:

```c
6995: const char* unit_log_field(const Unit *u) {
6996:         return MANAGER_IS_SYSTEM(ASSERT_PTR(u)->manager) ? "UNIT=" : "USER_UNIT=";
6997: }
6998: 
6999: const char* unit_invocation_log_field(const Unit *u) {
7000:         return MANAGER_IS_SYSTEM(ASSERT_PTR(u)->manager) ? "INVOCATION_ID=" : "USER_INVOCATION_ID=";
7001: }
```

Located quote: `unit.c:6996`: `"return MANAGER_IS_SYSTEM(ASSERT_PTR(u)->manager) ? \"UNIT=\" : \"USER_UNIT=\";"` (7 words).

### 5.3 Subject vs Emitter Metadata: The Architectural Distinction and Subject Selection

| Field | Source Type | Producer | What it Represents |
|---|---|---|---|
| `UNIT` | Explicit client field | System manager (`systemd --system`) | The system unit **subject** being logged about (`u->id`) |
| `USER_UNIT` | Explicit client field | User manager (`systemd --user`) | The user unit **subject** being logged about (`u->id`) |
| `_SYSTEMD_UNIT` | Implicit trusted field (`_` prefix) | `systemd-journald` | The cgroup/unit of the **logging process** (emitter) |
| `_SYSTEMD_USER_UNIT` | Implicit trusted field (`_` prefix) | `systemd-journald` | The user-unit cgroup of the logging process (emitter) |

**Manager Type vs Journal Query Scope**:
- The emitter code `unit_log_field` (`unit.c:6996`) dispatches on **manager type** (`MANAGER_IS_SYSTEM` vs `MANAGER_IS_USER`), **not** journal query scope.
- `UNIT=` indicates the record was emitted by a system manager instance; `USER_UNIT=` indicates emission by a user manager instance.
- System journal stores (`journalctl --system`) can and do store records emitted by user managers (`USER_UNIT`) when unprivileged user journals are merged, forwarded, or multiplexed.
- Therefore, subject selection cannot presume that `--system` records only carry `UNIT` or `--user` records only carry `USER_UNIT`.

**The Fatal Emitter-Confusion Trap**:
- When `systemd --user` logs about a failed user service, the emitter process is the user manager itself (`systemd --user`), running within system slice `user@1000.service`.
- Therefore, the trusted field `_SYSTEMD_UNIT` attached by `systemd-journald` is `user@1000.service`!
- Reading `_SYSTEMD_UNIT` will always yield `user@1000.service` (or `init.scope`), completely masking the actual failing service.
- **Rule**: Never fall back to emitter metadata (`_SYSTEMD_UNIT`, `_SYSTEMD_USER_UNIT`).

**Durable Subject Selection Contract (`scoped-counter-contract.json`)**:
- The failed unit subject is selected by **exactly one valid `UNIT` or `USER_UNIT` field, independent of journal query scope**.
- If **both** `UNIT` and `USER_UNIT` are present, the subject is classified as `unknown` (even if identical).
- If **neither** is present, or if the field is null, empty string, or a JSON array, the subject is classified as `unknown`.
- Classification never falls back to emitter metadata (`_SYSTEMD_UNIT`, `_SYSTEMD_USER_UNIT`).

---

## 6. Registered Source Row S038 for Service Result Emitter

L1 has registered `src/core/service.c` as **S038** (with anchor `src/core/service.c:6588-6602`, line 6598 mapping `[SERVICE_FAILURE_OOM_KILL] = "oom-kill"`):

| Field | Value |
|---|---|
| **id** | **S038** |
| **source** | systemd service termination and result table — `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c` |
| **kind** | code |
| **tier** | A |
| **scope** | service failure logging and `service_result_table` string mapping for `UNIT_RESULT` |
| **anchor** | `src/core/service.c:2518,6588-6602`; commit `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` |
| **teaches** | `unit_log_failure` receives `service_result_to_string(s->result)`, where `[SERVICE_FAILURE_OOM_KILL]` directly maps to string `"oom-kill"` in `service_result_table`. |
| **status** | mined |
| **opened** | 2026-10-20 |
| **recheck** | on-release |
| **used-by** | `corpus/knowledge/journal-alarm-routing-r14.md` |
| **SHA-256** | `669cccf4356bd838b0ac9541ef435c9c1307f989a36f2c0f35584b8184d7731f` |

---

## 7. Recommended Safe Journal Field Selection

Because system journal storage may contain records emitted by user managers, queries in both `--system` and `--user` scopes should request both `UNIT` and `USER_UNIT` subject fields alongside validated boot and record metadata:

### 7.1 Kernel OOM Unit Notice (`fe6faa94e7774663a0da52717891d8ef`)
- **System Scope**:
  ```sh
  journalctl --system -b --no-pager -o json \
    --output-fields=_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT \
    MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef
  ```
- **User Scope**:
  ```sh
  journalctl --user -b --no-pager -o json \
    --output-fields=_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT \
    MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef
  ```

### 7.2 Unit Failure Record (`d9b373ed55a64feb8242e02dbe79a49c`)
- **System Scope**:
  ```sh
  journalctl --system -b --no-pager -o json \
    --output-fields=_BOOT_ID,MESSAGE_ID,UNIT_RESULT,UNIT,USER_UNIT \
    MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c
  ```
- **User Scope**:
  ```sh
  journalctl --user -b --no-pager -o json \
    --output-fields=_BOOT_ID,MESSAGE_ID,UNIT_RESULT,UNIT,USER_UNIT \
    MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c
  ```

### 7.3 Unit Process Exit Record (`98e322203f7a4ed290d09fe03c09fe15`)
- **System Scope**:
  ```sh
  journalctl --system -b --no-pager -o json \
    --output-fields=_BOOT_ID,MESSAGE_ID,EXIT_CODE,EXIT_STATUS,UNIT,USER_UNIT \
    MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15
  ```
- **User Scope**:
  ```sh
  journalctl --user -b --no-pager -o json \
    --output-fields=_BOOT_ID,MESSAGE_ID,EXIT_CODE,EXIT_STATUS,UNIT,USER_UNIT \
    MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15
  ```

### 7.4 Mandatory Query and Validation Invariants
1. **Never request or parse `MESSAGE`**: display text is not metadata (S015 HTML:34–36, QUALITY #15).
2. **Current-Boot Anchoring**: Every record must validate that `._BOOT_ID == $current_boot_id`. Multiple boots or mismatches grade `unavailable:multi-boot` or `unavailable:boot-mismatch`.
3. **Structured Single-Pass JQ**: Parse slurped JSON arrays with `jq -s`. Reject non-string or array fields.
4. **Never Echo Unit String Bytes**: Avoid log-injection or token-splitting vulnerabilities; report counts and structured findings only.

---

## 8. Recommended Result Classification and Alarm Routing

### 8.1 Restoring OOM Critical Alarm & DRIFT (`OOM_KILL_JOURNAL`)
- **Alarm Policy (`scoped-counter-contract.json`)**:
  - Exactly **one** `OOM_KILL_JOURNAL crit` alarm per census on positive kernel notice (`fe6faa94...`) or positive `UNIT_RESULT=oom-kill` in either scope.
  - Forces census status `st=drift`.
  - Four separate counters: `user_notice`, `system_notice`, `user_unit_oom`, `system_unit_oom` (never summed).
  - Unknown arms remain explicitly unknown/unavailable; a known positive arm still alarms.
- **Unit Result Integration**: A unit failure record with `UNIT_RESULT=oom-kill` (grounded in S038 `service.c:6598` / `service.h:89`) directly evidences an OOM-induced failure across fleet and non-fleet units and accounts into OOM alarm tracking.

### 8.2 Fleet vs Non-Fleet Unit Partitioning
When classifying unit failure records (`d9b373ed...`):
1. **Subject Selection (`scoped-counter-contract.json`)**:
   - Failed subject is selected by **exactly one valid `UNIT` or `USER_UNIT`** field, independent of journal query scope.
   - If both `UNIT` and `USER_UNIT` are present: classify as `unknown` (even if identical).
   - If neither is present, or value is empty, null, or a JSON array: classify as `unknown`.
   - Never fall back to emitter metadata (`_SYSTEMD_UNIT`, `_SYSTEMD_USER_UNIT`).
2. **Fleet Regex**:
   - Case-insensitive historical token match: `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet`
3. **Routing and Severities**:
   - **Fleet Units** (subject matches fleet regex):
     - Emit `UNIT_FAILURE_JOURNAL` (`severity=info`, `scope=fleet-units`).
   - **Non-Fleet Units** (subject does not match fleet regex):
     - Emit `UNIT_FAILURE_OUT_OF_SCOPE` (`severity=info`, `owner=tsukuroi`, `note=non-fleet units (desktop/OS) — tsukuroi owns these`).
   - **Unknown / Unattributed Subject**:
     - Emit `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` (`severity=info`, `scope=user|system`, `owner=unresolved`, `reason=subject-metadata-unknown`).
     - Fulfills QUALITY #30 / `lessons/round-14.md#M2`: missing or ambiguous subject metadata is never falsely classified as non-fleet or zero.

### 8.3 Signal-9 Process Exit Warning (`KILL_SIGNAL_JOURNAL`)
- For `MESSAGE_ID=98e32220...` with `EXIT_CODE == "killed"` and `EXIT_STATUS == 9`:
- Maintain `KILL_SIGNAL_JOURNAL warn` in user scope (attribution none).

### 8.4 Unmeasured Reason Refinement
- Correct the categorical `reason=no-anchored-structured-field`:
- S035, S036, and S038 demonstrate that `UNIT_RESULT`, `EXIT_CODE`, and `EXIT_STATUS` are valid structured fields.
- Differentiate:
  1. Retired unsafe MESSAGE regexes (GPF text heuristics).
  2. Unimplemented structured signal/result classes pending measurement.
  3. Signals that genuinely leave no retained record in the journal.
