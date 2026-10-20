# ReconBootScope — S014 Current Boot Selection & _BOOT_ID Matching (Round 15, C1)

**Seat**: `MoriR15.ReconBootScope`  
**Role**: `scout` (leaf member — read-only research, no subagent dispatch)  
**Milestone**: retain validated positives without fabricated totals  
**Judged Axis**: `coverage` (axis 6, lowest owned vs operability 7)  
**Target File / Locus**: `tools/mori-census.sh` (`probe_journal`, `journal_query`, `JOURNAL_JQ_*`)  
**Report Path**: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-15/build/ReconBootScope.md`  

---

## 1. Posture & Directives

1. **Godspeed posture applied**:
   - **Name the axes**: `coverage` (C1: preserving critical OOM and user signal alarms from valid current-boot records) vs `operability` (retaining `unavailable` semantics on invalid aggregate streams without fabricating numeric totals).
   - **Iterate cheap, in parallel**: Concurrent examination of primary source S014 (`journalctl(1)`), local systemd documentation, existing census r14 implementation, and sibling review audits.
   - **Keep moves that improve any axis and harm none**: Validated positives restore silenced alarm coverage without altering aggregate unavailability contracts or polluting clean streams.
   - **Don't aim — let the frontier walk itself**: Isolate exact boot selection mechanics and per-record matching invariants from first principles.

2. **Host safety directive (parent MoriR15, 2026-10-20)**:
   - Synchronized package database ~413 packages ahead.
   - Directive: No `pacman -Sy`, `-Syu`, `-U`, or `-R`.
   - Tool installations/upgrades: **None performed**. Zero package manager commands executed. Read-only source analysis and report write only.

---

## 2. Primary Named Source: S014 `journalctl(1)`

- **Source Identifier**: `S014`
- **Canonical URL**: `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html`
- **Kind / Tier**: `docs` / Tier `A`
- **Upstream Version**: systemd 262 (Host version: systemd 261, `261.2-1-arch`, Linux 7.2.3-arch1-3)
- **Status in Round 15**: Reopened for claim C1 per `spec.json` context.

---

## 3. Exact Anchors & Verbatim Quotes (≤ 25 words each)

### Anchor 1: Boot Selection Option (`-b`, `--boot`)
- **Location**: Section *Filtering Options*, HTML anchor `<dt id="-b ID±offset|all">`, lines 127–134 in systemd 262 HTML.
- **Exact Quote 1** (13 words):
  > "Show messages from a specific boot. This will add a match for \"_BOOT_ID=\"."
- **Exact Quote 2** (16 words):
  > "The argument may be empty, in which case logs for the current boot will be shown."
- **Exact Quote 3** (22 words):
  > "If the 32-character ID is specified, it may optionally be followed by offset which identifies the boot relative to the one given by boot ID."

### Anchor 2: Mandatory Metadata & Field Restriction (`--output-fields=`)
- **Location**: Section *Output Options*, HTML anchor `<dt id="--output-fields=">`, lines 231–236 in systemd 262 HTML.
- **Exact Quote 4** (14 words):
  > "For the former, the \"__CURSOR\", \"__REALTIME_TIMESTAMP\", \"__MONOTONIC_TIMESTAMP\", and \"_BOOT_ID\" fields are always printed."

### Anchor 3: Kernel Message Boot Default (`-k`, `--dmesg`)
- **Location**: Section *Filtering Options*, HTML anchor `<dt id="-k">`, line 193 in systemd 262 HTML.
- **Exact Quote 5** (5 words):
  > "This adds the match _TRANSPORT=kernel."
- **Exact Quote 6** (7 words):
  > "This implies --boot=0 unless explicitly specified otherwise."

---

## 4. Boot Selection and `_BOOT_ID` Mechanics in Mori

### 4.1 Upstream `journalctl` Invariants
1. **Current Boot Match**: Invoking `journalctl` with `-b` without an argument adds an internal filter matching `_BOOT_ID` equal to the host's current boot ID.
2. **Mandatory `_BOOT_ID` Inclusion**: When requesting `-o json` with `--output-fields=...`, `journalctl` suppresses non-requested fields (such as `MESSAGE`) but **always** emits `_BOOT_ID`, `__CURSOR`, `__REALTIME_TIMESTAMP`, and `__MONOTONIC_TIMESTAMP`.
3. **Format**: As verified in S015 (Trusted Journal Fields, line 100), `_BOOT_ID` is formatted as a 128-bit hexadecimal string (32 lowercase hex characters without hyphens).

### 4.2 Mori SUT Boot Anchor Handling (`tools/mori-census.sh:317-329`)
- `BOOT_ID_EXPECTED` is obtained from `MORI_BOOT_ID` (fixture environment override) or read from `/proc/sys/kernel/random/boot_id` (`BOOT_ID_FILE`).
- Hyphens and newlines are stripped (`tr -d -- '-\n'`).
- The resulting string is strictly validated:
  - Must contain only lowercase hex characters (`*[!0-9a-f]*` rejected).
  - Must have an exact string length of 32 characters (`${#BOOT_ID_EXPECTED} -eq 32`).
- If missing or invalid, `BOOT_ID_EXPECTED` is cleared to `''`, causing `probe_journal` (`:1180-1184`) to immediately grade both `journal.user` and `journal.system` as `unavailable (boot_id=unavailable)`.
- In valid runs, `BOOT_ID_EXPECTED` is passed as `--arg boot "$BOOT_ID_EXPECTED"` to every jq query filter.

---

## 5. Scope Boundaries for C1

Round 15 defines an explicit separation between **aggregate class counters** and **validated-positive evidence**:

### 5.1 The Aggregate Scope Boundary (Honesty & Operability)
- **Scope**: Represents the aggregate set of all records returned in the query stream.
- **Behavior**: If any single record in the query stream fails validation (foreign boot ID, array-typed boot ID, malformed payload, or non-matching `MESSAGE_ID`), the aggregate class count **must remain unavailable** (`unavailable:boot-mismatch`, `unavailable:multi-boot`, or `unavailable:record-invalid`).
- **Rule**: Never fabricate a total count from an untrusted or inconsistent stream.

### 5.2 The Validated-Positive Evidence Boundary (Coverage & Safety)
- **Scope**: Represents concrete, individually authenticated records within the successfully captured, stderr-free, valid JSON stream.
- **Predicate**: A record contributes to `positive_*` evidence if and only if:
  1. It is a valid JSON object (`type == "object"`).
  2. Its `_BOOT_ID` is a scalar string (`(._BOOT_ID | type) == "string"`) and strictly matches `$boot` (`._BOOT_ID == $boot`).
  3. Its `MESSAGE_ID` is a scalar string (`(.MESSAGE_ID | type) == "string"`) and strictly matches `$id` (`.MESSAGE_ID == $id`).
  4. Specific sub-predicates match exactly (e.g. `UNIT_RESULT == "oom-kill"`, `UNIT_RESULT == "signal"`, or `EXIT_CODE == "killed"` and scalar `EXIT_STATUS == "9"`).
- **Rule**: Unsafe, non-matching, foreign-boot, or array-tainted records are excluded from positive counting, but their presence **must not discard** valid current-boot positives.

### 5.3 The Alarm Actuation Boundary
- **OOM Alarm**: `OOM_KILL_JOURNAL crit` must fire if **any** valid current-boot positive record exists (`positive_kernel_oom > 0` or `positive_unit_oom > 0` in user or system scope), even if aggregate counts are `unavailable`.
- **User Signal Warning**: `KILL_SIGNAL_JOURNAL warn` must fire if **any** valid current-boot user positive record exists (`positive_process_sigkill > 0` or `positive_unit_signal > 0`), even if aggregate counts are `unavailable`.

### 5.4 Invariant Non-Claims (Contractual Limits)
1. **No Completeness Claim**: Positive evidence proves only observed lower-bound occurrences, not total events or absence of unrecorded events.
2. **No Emitter Identity Claim**: `MESSAGE_ID`, `UNIT`, and `USER_UNIT` are unprivileged, client-supplied user fields; they are not authenticated kernel credentials.
3. **No Unique Victim Claim**: Unit notices (`fe6faa94...`) and unit failure results (`d9b37...`) are service-manager notices, not per-victim process kill records.
4. **No Arbitrary JSON Repair**: If `jq -s` cannot parse the JSON stream (`malformed-json`), or if `journalctl` exits nonzero or writes stderr, positive evidence is `unavailable`, never guessed or partially repaired.
5. **No Cross-Scope Summing**: User and system scopes remain strictly partitioned.

---

## 6. Concrete Counterexample for C1

### 6.1 The Concrete Scenario
- **Environment**: Pinned current boot `MORI_BOOT_ID="11111111111111111111111111111111"`.
- **Query**: `journalctl --system -b --no-pager -o json --output-fields=_BOOT_ID,MESSAGE_ID MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`.
- **Captured Stdout (2 JSON objects)**:
  ```json
  {"_BOOT_ID":"11111111111111111111111111111111","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef"}
  {"_BOOT_ID":"ffffffffffffffffffffffffffffffff","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef"}
  ```
  *(Record 1 is a valid current-boot kernel OOM unit notice; Record 2 is an unrotated or foreign-boot record).*

### 6.2 Round 14 Execution Trace (Failure / Defect)
1. In `tools/mori-census.sh`, `JOURNAL_JQ_MSGID` (`:974`) executes:
   ```jq
   if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and (._BOOT_ID == $boot) and (.MESSAGE_ID == $id)) ...
   ```
2. Because Record 2 has `._BOOT_ID == "ffff..." != $boot`, the `all(...)` guard evaluates to `false`.
3. Execution drops to `JOURNAL_JQ_TAIL`'s fallback (`:973`):
   ```jq
   ([.[]._BOOT_ID] | unique | length) as $b | if $b > 1 then "multi-boot" ...
   ```
4. Since two distinct boot IDs exist, jq emits `"multi-boot"`.
5. In `journal_query` (`:1104`), `parsed="multi-boot"`, so `JQ_STATUS=multi-boot` and `JQ_N=""`.
6. In `probe_journal` (`:1221`), `js["system:kernel_oom_notice"]="multi-boot"` and `jn` is empty.
7. In the OOM alarm gate (`:1305`):
   ```bash
   if [ "${js[$key]}" = ok ]; then ko=${jn[$key]}; else ko="unavailable:${js[$key]}"; fi
   ```
   `ko` becomes `"unavailable:multi-boot"`.
8. In the alarm fire check (`:1314-1317`):
   ```bash
   case "$ko" in
     unavailable:*) ;;
     *) if [ "$ko" -gt 0 ]; then oom_fire=1; oom_path_k=1; fi ;;
   esac
   ```
9. `oom_fire` remains `0`.
10. **Defect Outcome**: `OOM_KILL_JOURNAL crit` is **silenced**! A real kernel OOM kill event in the current boot was discarded simply because an adjacent record carried a foreign boot ID.

### 6.3 Round 15 C1 Execution Trace (Resolved)
1. Aggregate class processing evaluates stream: `all(...)` is false, `$b > 1` -> aggregate status remains `system:kernel_oom_notice=unavailable:multi-boot`.
2. Per-record positive scanner evaluates Record 1:
   - `type == "object"`: `true`
   - `._BOOT_ID == "11111111111111111111111111111111"`: `true`
   - `.MESSAGE_ID == "fe6faa94e7774663a0da52717891d8ef"`: `true`
   - Increments `positive_kernel_oom` to `1`.
3. Per-record positive scanner evaluates Record 2:
   - `._BOOT_ID == "11111111111111111111111111111111"`: `false`
   - Excluded from positive counts.
4. Positive evidence for system scope: `positive_kernel_oom=1`.
5. Alarm gate evaluates: `positive_kernel_oom > 0` -> sets `oom_fire=1`, `oom_path_k=1`.
6. Finding emitted:
   ```
   FINDING OOM_KILL_JOURNAL severity=crit class=oom_kill alarm=1 paths=kernel_oom_notice ... system_notice=unavailable:multi-boot positive_kernel_oom=1 ...
   ```
7. **Resolution Outcome**: The critical OOM alarm is successfully preserved from the verified current-boot record, while the aggregate total count remains truthfully unavailable without fabrication.
