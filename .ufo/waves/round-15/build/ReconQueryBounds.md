# ReconQueryBounds: Census Journal Timeout, Stderr, and Capture Failure Bounds (Round 15, C1)

**Scope**: Read-only research of existing census journal query timeout, stderr, and capture failure paths in `tools/mori-census.sh`, anchored against primary source S014 (`journalctl(1)`). Report exact anchors, <=25-word quote, scope boundaries, and a concrete counterexample for C1.  
**Role**: Leaf scout (`MoriR15.ReconQueryBounds`).  
**Judged axis**: Coverage (milestone: retain validated positives without fabricated totals).  
**Execution**: No builds, tests, linters, formatters, or verification runs. Report write only.

---

## 1. Named Axes

- **Coverage (judged)**: Preserving critical OOM (`OOM_KILL_JOURNAL` crit) and user signal (`KILL_SIGNAL_JOURNAL` warn) alarms from individually valid current-boot structured records when an adjacent record invalidates the aggregate class.
- **Operability (context)**: Existing raw aggregate and split counts remain `unavailable:<reason>` when invalid; no fabricated totals; capture timeouts, nonzero exit codes, and non-empty stderr strictly propagate as `unavailable`.

---

## 2. Primary Named Source (S014 `journalctl(1)`)

- **Source Registry**: `corpus/SOURCES.md` row S014 (`journalctl(1)`).
- **Primary Source URL**: `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html` (systemd 262 docs; host systemd 261.2-1-arch).
- **Exact Anchors & Verbatim Quotes (<= 25 words each)**:
  1. **Anchor**: `#Exit%20status` (Exit status, line 352)
     - **Quote**: *"On success, 0 is returned; otherwise, a non-zero failure code is returned."* (11 words)
  2. **Anchor**: `#--output-fields=` (Output Options, lines 489–494)
     - **Quote**: *"A comma separated list of the fields which should be included in the output."* (14 words)
  3. **Anchor**: `#-b%20ID%C2%B1offset%7Call` (Filtering Options, line 187)
     - **Quote**: *"Show messages from a specific boot. This will add a match for \"_BOOT_ID=\"."* (13 words)
  4. **Anchor**: `#-q` (Output Options, lines 257–260)
     - **Quote**: *"Suppresses all informational messages (i.e. \"-- Journal begins at …\", \"-- Reboot --\"), any warning messages regarding inaccessible system journals when run as a normal user."* (22 words)

---

## 3. Existing Census Journal Capture Failure Paths in `tools/mori-census.sh`

In `tools/mori-census.sh`, journal queries are executed by `journal_query()` (`:1046-1136`) and driven by `probe_journal()` (`:1151-1389`). The existing failure paths and exact anchors are:

### Path 1: Missing Timeout Binary (`no-timeout-bin`)
- **Anchor**: `tools/mori-census.sh:1052-1055`
- **Mechanism**:
  ```bash
  if ! have "$TIMEOUT_BIN" && [ ! -x "$TIMEOUT_BIN" ]; then
    JQ_STATUS=no-timeout-bin
    return 0
  fi
  ```
- **Semantics**: An unbounded journal query is refused because a wedged journal store can hang the census indefinitely. Status is set to `no-timeout-bin`, returning immediately before calling `journalctl`.

### Path 2: Latency Timeout (`timeout`)
- **Anchor**: `tools/mori-census.sh:1072, 1083-1089`
- **Configuration**: `MORI_JOURNAL_TIMEOUT_S` (default 2s latency bound; `:225, 316`).
- **Invocation**:
  ```bash
  CAP_OUT=$("$TIMEOUT_BIN" -k 1 "$JOURNAL_TIMEOUT_S" "$JOURNALCTL_BIN" "$flag" -b --no-pager -o json --output-fields="$fields" "${m[@]}" 2>&"$w")
  CAP_RC=$?
  ```
- **Exit Code Classification**:
  ```bash
  if [ "$CAP_RC" -ne 0 ]; then
    case "$CAP_RC" in
      124|137) JQ_STATUS=timeout ;;
      *) JQ_STATUS="rc-$CAP_RC" ;;
    esac
    return 0
  fi
  ```
- **Semantics**: If `timeout` terminates `journalctl` (exit code 124 or SIGKILL 137), `JQ_STATUS=timeout`. No stdout is parsed, preventing partial buffer truncation from being counted.

### Path 3: Subprocess Exit Code Failure (`rc-$CAP_RC`)
- **Anchor**: `tools/mori-census.sh:1083-1090`
- **Mechanism**: Any non-zero exit code other than 124/137 (e.g. `rc=1` when unprivileged user accesses system journal without permissions) maps directly to `JQ_STATUS="rc-$CAP_RC"`.
- **Semantics**: S014 states that `rc != 0` indicates failure. Partial bytes on failure are discarded.

### Path 4: Non-Empty Stderr Detection (`stderr-nonempty`)
- **Anchor**: `tools/mori-census.sh:1057-1082, 1091-1095`
- **Mechanism**:
  ```bash
  coproc JOURNAL_ERR { wc -c; }
  ...
  exec {w}>&"$cin"
  ... 2>&"$w"
  ...
  exec {w}>&-
  IFS= read -r err_bytes <&"$r" || true
  ...
  if [ "$err_bytes" -gt 0 ]; then
    JQ_STATUS=stderr-nonempty
    return 0
  fi
  ```
- **Semantics**: A background `wc -c` coprocess drains stderr continuously to avoid pipe-buffer deadlocks on large warnings. Any stderr output (`err_bytes > 0`) immediately sets `JQ_STATUS=stderr-nonempty`. Stderr bytes are counted and closed, never stored or echoed to stdout, preventing canary leakage or output corruption.

### Path 5: Stream Parser Failure (`malformed-json`)
- **Anchor**: `tools/mori-census.sh:1098-1102`
- **Mechanism**:
  ```bash
  parsed=$("$JQ_BIN" -s -r "$@" "$filter" <<< "$raw" 2>/dev/null)
  jrc=$?
  if [ "$jrc" -ne 0 ]; then JQ_STATUS=malformed-json; return 0; fi
  ```
- **Semantics**: If `jq` fails to parse `$raw` as JSON (syntax error, truncated input), `jrc != 0` sets `JQ_STATUS=malformed-json`.

### Path 6: Missing Tool or Boot Prerequisites in `probe_journal`
- **Anchor**: `tools/mori-census.sh:1168-1185`
- **Mechanisms**:
  - `! have "$JOURNALCTL_BIN"` (`:1168`) -> emits `SURFACE journal.<scope> unavailable ... journalctl=missing`.
  - `! have "$JQ_BIN"` (`:1174`) -> emits `SURFACE journal.<scope> unavailable ... parser=missing bin=$JQ_BIN`.
  - `[ -z "$BOOT_ID_EXPECTED" ]` (`:1180`) -> emits `SURFACE journal.<scope> unavailable ... boot_id=unavailable`.

---

## 4. Scope Boundaries

1. **Per-Scope Isolation**:
   - `journalctl --user` and `journalctl --system` execute as separate queries.
   - User and system scope outputs are emitted on distinct surface rows (`journal.user` vs `journal.system`) and are **never summed** (QUALITY #16; `structured-journal-scopes-r13.md`).
2. **Boot Scope Boundary**:
   - Every structured query passes `-b` to restrict retrieval to the current boot.
   - The census expects a 32-character lowercase hex `BOOT_ID_EXPECTED` (derived from `/proc/sys/kernel/random/boot_id`).
   - If an entry has a different boot ID, it belongs to another boot session and cannot be counted toward the current boot's total.
3. **Capture Boundary vs. Record Boundary (The C1 Boundary)**:
   - **Capture Failure Boundary**: If the query fails at the process, timeout, stderr, or JSON syntax level (`no-timeout-bin`, `timeout`, `rc-N`, `stderr-nonempty`, `malformed-json`), the stream is **untrusted/unusable**. Per the round-15 contract:
     - Positive tokens (`positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`) **MUST** be `unavailable:<reason>`.
     - Positive tokens **MUST NOT** be numeric zero `0` (which would falsely imply "verified 0 events").
     - Positive tokens **MUST NOT** trigger any alarm (`oom_fire` and `kill_fire` remain 0).
   - **Record Validation Boundary**: If the stream was successfully captured and stderr-free (`rc=0`, `err_bytes=0`, valid JSON):
     - If all records match current boot and schema: aggregate counts are numeric, positive counts are numeric.
     - If the stream is empty (`[]`): aggregate counts are `0`, positive counts are `0`.
     - If the stream contains mixed records (e.g., valid records alongside foreign-boot or malformed records):
       - The aggregate class total becomes `unavailable:record-invalid`, `unavailable:boot-mismatch`, or `unavailable:multi-boot`.
       - The validated-positive evidence tokens inspect individual object records: each record with scalar matching `MESSAGE_ID` and scalar current `_BOOT_ID` (plus required unit/process status) increments the positive counter.
       - A positive count > 0 triggers the alarm (`OOM_KILL_JOURNAL` crit or user `KILL_SIGNAL_JOURNAL` warn), preserving critical visibility without fabricating an aggregate count.

---

## 5. Concrete Counterexamples for C1

### Counterexample A: The Mixed-Boot OOM Alarm Loss (SUT Defect C1 Solves)
- **Scenario**: System scope journal query for kernel OOM notice (`MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`).
- **Captured JSON Stream**:
  ```json
  {"_BOOT_ID":"11111111111111111111111111111111","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef"}
  {"_BOOT_ID":"ffffffffffffffffffffffffffffffff","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef"}
  ```
  *(Current boot is `11111111111111111111111111111111`).*
- **SUT Behavior Prior to C1 (Round 14)**:
  1. `JOURNAL_JQ_MSGID` runs: `all(.[]; ... and (._BOOT_ID == $boot) ...)` fails because record 2 has `_BOOT_ID="ffff..."`.
  2. Fallback logic runs: `[.[]._BOOT_ID] | unique | length` equals 2 (`> 1`), emitting `"multi-boot"`.
  3. `JQ_STATUS` is set to `multi-boot` (`tools/mori-census.sh:1104`).
  4. In `probe_journal`:
     - `system:kernel_oom_notice` receives `js="multi-boot"`, `jn=""`.
     - `ko` is formatted as `"unavailable:multi-boot"` (`:1305`).
     - `oom_fire` check (`:1314-1317`): `case "$ko" in unavailable:*) ;; *) if [ "$ko" -gt 0 ]; then oom_fire=1; fi ;; esac` treats it as unavailable and **does not set `oom_fire=1`**.
     - `OOM_KILL_JOURNAL` critical alarm is **suppressed entirely**.
  5. **Defect**: A real kernel OOM kill occurred during the current boot (Record 1), but was silenced because an adjacent record carried a foreign boot ID.
- **Expected Behavior under C1**:
  1. Raw aggregate count remains `kernel_oom_notice=unavailable:multi-boot` (conformance: no fabricated total).
  2. Positive token `positive_kernel_oom` independently validates Record 1: matches current boot `1111...` and `fe6faa94...` -> `positive_kernel_oom=1`.
  3. `oom_fire` evaluates positive evidence: `positive_kernel_oom=1` sets `oom_fire=1`.
  4. `FINDING OOM_KILL_JOURNAL severity=crit` fires once, carrying `system_notice=unavailable:multi-boot positive_kernel_oom=1`.

### Counterexample B: The Capture Failure Boundary (Negative Counterexample)
- **Scenario**: System scope journal query for kernel OOM notice times out (`CAP_RC=124`) or produces stderr noise (`err_bytes > 0`).
- **Stream**: Stderr emitted `"journalctl: error reading journal"` or command timed out after 2s.
- **Contract Requirement**:
  - The probe must not attempt to parse partial stdout.
  - `JQ_STATUS` is `timeout` or `stderr-nonempty`.
  - Positive evidence token `positive_kernel_oom` **MUST NOT** be defaulted to `0` (a false clean zero). It must be `unavailable:timeout` or `unavailable:stderr-nonempty`.
  - No OOM alarm fires from this unavailable class (`oom_fire=0`).

---

## 6. Implementation Notes for Production Seat (`MoriR15.CensusPositive`)

1. **Positioning of Positive Evaluation**:
   - The positive filter must run on the **same captured `$raw`** inside `journal_query()` (or immediately following it), after `CAP_RC` and `err_bytes` checks, but **before** the aggregate returns `record-invalid`, `multi-boot`, or `boot-mismatch`.
2. **Filter Independence**:
   - Validated positive counts must be computed independently of `all(.[]; ...)` aggregate validity.
   - For positive kernel OOM: `map(select(type == "object" and (._BOOT_ID|type) == "string" and ._BOOT_ID == $boot and (.MESSAGE_ID|type) == "string" and .MESSAGE_ID == $id)) | length`.
   - For positive unit OOM: `map(select(type == "object" and (._BOOT_ID|type) == "string" and ._BOOT_ID == $boot and (.MESSAGE_ID|type) == "string" and .MESSAGE_ID == $id and (.UNIT_RESULT?|type) == "string" and .UNIT_RESULT == "oom-kill")) | length`.
3. **Preservation of Raw Fields**:
   - Existing tokens (`kernel_oom_notice`, `unit_failure_record`, `unit_fleet`, `unit_oom`, etc.) must remain unchanged in name and semantics.
   - Positive fields are purely additive: `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`.

---

## 7. Tooling & Environment Record

- **Host Safety Directive**: Received parent IRC message confirming sync DB is ~413 packages ahead and forbidding `-Sy`, `-Syu`, `-U`, `-R`, downgrades, or service restarts.
- **Installs/Updates**: None. Read-only research seat; no tools installed or updated.
- **Verification Commands**: None executed (L1 integration rule respected).
