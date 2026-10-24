# SignalCoverage — Round 14 Scout Audit: SIGKILL, Signal 11, Alarm Retention, and Signal Distinctions

- **Seat:** `MoriR14.SignalCoverage` (leaf scout, report only)
- **Lane:** `mori-shokunin`
- **Milestone:** Restore OOM alarm and structured fleet routing (Round 14 C1 coverage repair)
- **Assigned Scope:** Inspect r13 current SIGKILL and signal11 structured paths plus sources; identify necessary retained behavior when restoring alarms, overbroad no-anchored reason, GPF/text/general signal unsupported distinctions. Report only.
- **Report Path:** `.ufo/waves/round-14/build/SignalCoverage.md` (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-14/build/SignalCoverage.md`)
- **Authority / Grounding:** Sources S013, S014, S015, S032, S035, S036; `corpus/lessons/round-13-verifier-spotcheck.md`; `tools/mori-census.sh` (at delivered r13 / frozen r14 commit `18d7d55` / `39abda0a…`); `tools/mori-round13-regressions.py`; baseline `1f07f1d`.

---

## 1. Inspection: r13 Current SIGKILL Structured Path & Sources

### 1.1 Implementation in `tools/mori-census.sh`
At commit `18d7d55` (SHA-256 `39abda0a…`), the census implements the structured SIGKILL query in `probe_journal()`:

- **Catalog Identifier & Filters (`tools/mori-census.sh:922, 928`):**
  ```bash
  JOURNAL_ID_UNIT_SIGKILL=98e322203f7a4ed290d09fe03c09fe15
  JOURNAL_JQ_SIGKILL="if all(.[]; type == \"object\" and (._BOOT_ID | type) == \"string\" and (._BOOT_ID == \$boot) and (.MESSAGE_ID == \$id) and (.EXIT_CODE == \"killed\") and ((.EXIT_STATUS | tostring) == \"9\")) $JOURNAL_JQ_TAIL"
  ```
- **Query Invocation (`tools/mori-census.sh:1069–1070`):**
  ```bash
  journal_query "$flag" '_BOOT_ID,MESSAGE_ID,EXIT_CODE,EXIT_STATUS' \
    "MESSAGE_ID=$JOURNAL_ID_UNIT_SIGKILL EXIT_CODE=killed EXIT_STATUS=9" \
    "$JOURNAL_JQ_SIGKILL" --arg boot "$BOOT_ID_EXPECTED" --arg id "$JOURNAL_ID_UNIT_SIGKILL"
  ```
- **Finding ID Mapping (`tools/mori-census.sh:1025–1026`):**
  ```bash
  user:unit_sigkill_record)   printf '%s' KILL_SIGNAL_JOURNAL ;;
  system:unit_sigkill_record) printf '%s' KILL_SIGNAL_JOURNAL_SYSTEM ;;
  ```
- **Severity & Emission (`tools/mori-census.sh:1093–1094, 1099–1100`):**
  - Scope `user`: severity `warn` (preserves the baseline DRIFT roll via `st=drift`).
  - Scope `system`: severity `info`.
  - Subject payload:
    `class=unit_sigkill_record unit=record message_id=98e322203f7a4ed290d09fe03c09fe15 signal=9 count=$n scope=$scope attribution=none note=unit process exited on SIGKILL; not an OOM or fleet-caused kill boot=$boot`
- **Surface Row Output (`tools/mori-census.sh:1110–1128`):**
  Included in `SURFACE journal.<scope>` under `record_classes=segfault_signal11,unit_sigkill_record,unit_failure_record`.

### 1.2 Authoritative Source Backing
- **S035 (`catalog/systemd.catalog.in:568–575`, commit `cf8ebfc6`):**
  - Message ID: `98e322203f7a4ed290d09fe03c09fe15` (`SD_MESSAGE_UNIT_PROCESS_EXIT_STR`).
  - Located Quote (12 words, ≤25 words): *"The process' exit code is '@EXIT_CODE@' and its exit status is @EXIT_STATUS@."*
  - Semantics: Defines structured unit process exit records containing `EXIT_CODE` and `EXIT_STATUS`.
- **S036 (`src/core/unit.c:6355–6392`, commit `cf8ebfc6`):**
  - Emitter function `unit_log_process_exit()` emits `LOG_MESSAGE_ID(SD_MESSAGE_UNIT_PROCESS_EXIT_STR)` with:
    `EXIT_CODE=%s` (mapped from `sigchld_code_to_string(code)`; `CLD_KILLED` maps to `"killed"` in `process-util.c:2308`),
    `EXIT_STATUS=%i` (signal integer `9` when `code == CLD_KILLED`).
- **S014 (`journalctl(1)`):**
  - Output fields limited via `--output-fields=_BOOT_ID,MESSAGE_ID,EXIT_CODE,EXIT_STATUS`.
  - Guarantees zero `MESSAGE` text payload leakage while extracting numeric status.
- **S015 (`systemd.journal-fields(7)`):**
  - `_BOOT_ID` is a trusted, underscore-prefixed field that cannot be spoofed by unprivileged client code; `EXIT_CODE` and `EXIT_STATUS` are passed by the unit manager.

### 1.3 Observability Boundaries & Delivery Blind Spots
- **Unit Process Scope Only:** Observes only processes directly monitored as a unit process by systemd (PID 1 or `systemd --user`).
- **Delivery Paths It Cannot See:**
  1. Arbitrary host processes killed by SIGKILL outside a managed systemd unit (e.g. processes inside an unmanaged tmux pane, raw background CLI processes, subshells).
  2. The sender/initiator of the SIGKILL (`kill(pid, 9)`) — `unit_log_process_exit` records only that the process received signal 9, not who sent it.
  3. Distinction between manager-escalated timeouts (`TimeoutStopSec=`) versus kernel/OOM/external SIGKILLs.

---

## 2. Inspection: r13 Current Signal 11 Structured Path & Sources

### 2.1 Implementation in `tools/mori-census.sh`
At commit `18d7d55`, the census implements the structured signal 11 query in `probe_journal()`:

- **Catalog Identifier & Filters (`tools/mori-census.sh:921, 929`):**
  ```bash
  JOURNAL_ID_COREDUMP=fc2e22bc6ee647b6b90729ab34a250b1
  JOURNAL_JQ_SIGSEGV="if all(.[]; type == \"object\" and (._BOOT_ID | type) == \"string\" and (._BOOT_ID == \$boot) and (.MESSAGE_ID == \$id) and ((.COREDUMP_SIGNAL | tostring) == \"11\")) $JOURNAL_JQ_TAIL"
  ```
- **Query Invocation (`tools/mori-census.sh:1067–1068`):**
  ```bash
  journal_query "$flag" '_BOOT_ID,MESSAGE_ID,COREDUMP_SIGNAL' \
    "MESSAGE_ID=$JOURNAL_ID_COREDUMP COREDUMP_SIGNAL=11" \
    "$JOURNAL_JQ_SIGSEGV" --arg boot "$BOOT_ID_EXPECTED" --arg id "$JOURNAL_ID_COREDUMP"
  ```
- **Finding ID Mapping (`tools/mori-census.sh:1023–1024`):**
  ```bash
  user:segfault_signal11)   printf '%s' SEGFAULT_SIGNAL11_JOURNAL_USER ;;
  system:segfault_signal11) printf '%s' SEGFAULT_SIGNAL11_JOURNAL_SYSTEM ;;
  ```
- **Severity & Emission (`tools/mori-census.sh:1092, 1097–1098`):**
  - Both user and system scopes emit severity `info`.
  - Subject payload:
    `class=segfault_signal11 unit=record source_field=COREDUMP_SIGNAL value=11 count=$n scope=$scope basis=scoped-record-count boot=$boot`
- **Surface Row Output (`tools/mori-census.sh:1110–1128`):**
  Included in `SURFACE journal.<scope>` under `record_classes=segfault_signal11,unit_sigkill_record,unit_failure_record`.

### 2.2 Authoritative Source Backing
- **S013 (`catalog/systemd.catalog.in:66–75`, commit `cf8ebfc6`):**
  - Message ID: `fc2e22bc6ee647b6b90729ab34a250b1` (`SD_MESSAGE_COREDUMP`).
  - Located Quote (5 words, ≤25 words): *"Process @COREDUMP_PID@ (@COREDUMP_COMM@) dumped core."*
  - Semantics: Identifies crash core-dump events recorded by `systemd-coredump`.
- **S032 (`systemd-coredump(8)`):**
  - Documents `COREDUMP_SIGNAL` as the numeric termination signal (integer `11` for SIGSEGV) and `COREDUMP_SIGNAL_NAME` (`SIGSEGV`).
  - Provides a structured numeric metadata anchor that eliminates relying on regex matches over error message strings.
- **S014 / S015:**
  - Restricts query output fields to `_BOOT_ID,MESSAGE_ID,COREDUMP_SIGNAL`, guaranteeing zero display string (`MESSAGE`) inspection.

### 2.3 Observability Boundaries & Delivery Blind Spots
- **Core Dump Dependent:** Observes only crashes handled by `systemd-coredump`.
- **Delivery Paths It Cannot See:**
  1. Crashes where core dumping was disabled (`ulimit -c 0` without coredump socket interception).
  2. Processes that caught `SIGSEGV` with a custom signal handler or terminated abnormally without generating a coredump notice (`1f4e0a44a88649939aaea34fc6da8c95`).
  3. Direct kernel trap log lines that do not trigger a userspace coredump.

---

## 3. Necessary Retained Behavior When Restoring Alarms

### 3.1 The Round-13 Rejected-Harmed Regressions
The Round 13 verifier spot-check (`corpus/lessons/round-13-verifier-spotcheck.md:72–89`) rejected the round on coverage and adjacency:
1. **OOM Alarm Regression:** In baseline `1f07f1d:893–895`, positive OOM (`c_oom > 0`) raised `OOM_KILL_JOURNAL crit` => `st=drift` (DRIFT). Round 13 demoted `kernel_oom_notice` to `info`, completely dropped the `OOM_KILL_JOURNAL` finding, and allowed the census to roll `CLEAN` (exit 0) in the presence of positive kernel OOM notices.
2. **Fleet Routing Regression:** In baseline `1f07f1d:904–908`, unit failures were split: fleet unit failures emitted `UNIT_FAILURE_JOURNAL info scope=fleet-units`, while non-fleet failures emitted `UNIT_FAILURE_OUT_OF_SCOPE info` routed to `tsukuroi`. Round 13 collapsed all unit failures under `unit_failure_record` into `UNIT_FAILURE_JOURNAL` (with note *"no fleet classification"*), erasing the fleet boundary and eliminating tsukuroi triage routing.

### 3.2 Invariants to Retain from Round-13 Gains (No-Harm Requirements)
When restoring alarms in Round 14, the following round-13 improvements **MUST BE RETAINED**:
1. **All Six Scoped Counters Retained on Surface Rows:**
   Every `SURFACE journal.user` and `SURFACE journal.system` row must continue to output all six structured counts:
   - `kernel_oom_notice`
   - `oomd_notice`
   - `coredump_notice`
   - `segfault_signal11`
   - `unit_sigkill_record`
   - `unit_failure_record`
2. **Strict Dual-Scope Separation:**
   User and system scopes must remain strictly independent surfaces (`journal.user` and `journal.system`). Per M19 and Quality Criterion 16, scopes must **NEVER** be summed.
3. **MESSAGE-Free Query Discipline:**
   Never restore raw `MESSAGE` regexes or request `MESSAGE`/`COMMAND` in `--output-fields`. Queries must extract only structured metadata (`_BOOT_ID`, `MESSAGE_ID`, `EXIT_CODE`, `EXIT_STATUS`, `COREDUMP_SIGNAL`, `UNIT_RESULT`, `UNIT`, `USER_UNIT`).
4. **Boot Integrity & Fault Gating:**
   Validate `_BOOT_ID` against `/proc/sys/kernel/random/boot_id` (or `MORI_BOOT_ID`). Preserve strict `unavailable` grading on parser missing, timeout, stderr bytes, malformed JSON, multi-boot, or boot mismatch.
5. **SIGKILL Warning Retained:**
   Positive `unit_sigkill_record` in the user scope must continue emitting `KILL_SIGNAL_JOURNAL warn` (causing `st=drift`).

### 3.3 Restored Alarm Specifications
1. **Restored Kernel OOM Alarm (`OOM_KILL_JOURNAL crit`):**
   - Positive `kernel_oom_notice` (`fe6faa94e7774663a0da52717891d8ef`) in *either* `user` or `system` scope must emit:
     `emit_finding OOM_KILL_JOURNAL crit "class=kernel_oom_notice count=$n scope=$scope trust=client-supplied unit=notice basis=scoped-record-count boot=$boot"`
   - Setting severity `crit` forces `st=drift` (triggering a `MORI_CENSUS: DRIFT` roll, exit 1).
   - Labeling must state `unit=notice` and `trust=client-supplied`. Do not claim it is a unique victim count or proof of fleet causation (S013 / S003).
2. **Account for `UNIT_RESULT=oom-kill`:**
   - In `unit_log_failure()` (S036 `unit.c:6333–6342`), systemd records `UNIT_RESULT=oom-kill` on `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c` when a unit is terminated by OOM.
   - When `UNIT_RESULT=oom-kill`, this structured record also represents an OOM event and must trigger the critical OOM alarm.
3. **Restored Structured Fleet Routing:**
   - Query unit metadata fields: `UNIT` (system scope) or `USER_UNIT` (user scope) (S015 / S036).
   - Evaluate against the fleet predicate regex: `'shokunin|ufo-sighting|tmux-spawn|the-tick|fleet'`.
   - Fleet matches emit: `UNIT_FAILURE_JOURNAL` (for fleet units).
   - Non-fleet matches emit: `UNIT_FAILURE_OUT_OF_SCOPE info` with note/owner stating `tsukuroi owns these`.
   - Missing, malformed, or unreadable unit metadata must grade as `UNKNOWN`/`unavailable`, **NEVER** silently defaulted to non-fleet or zero (Quality Criterion 30).

---

## 4. Overbroad "no-anchored-structured-field" Reason

### 4.1 The Overbroad Assertion in Delivered r13
In `tools/mori-census.sh:1041` and `:1127`:
```bash
emit_finding JOURNAL_CLASSES_UNMEASURED info "classes=oom_kill_text,other_signals,other_unit_failure_text basis=unmeasured reason=no-anchored-structured-field note=..."
d="$d; unmeasured=oom_kill_text,other_signals,other_unit_failure_text reason=no-anchored-structured-field; ts=$TS_UTC"
```
The spot-check (Defect 3 & routed note 3) identified this as an overbroad assertion:
> *"Delivered :1041/:1127 attributes other_signals,other_unit_failure_text to 'no-anchored-structured-field'. Newly admitted S035/S036 demonstrate EXIT_CODE/decimal EXIT_STATUS and UNIT_RESULT fields. What remains unimplemented or unobserved must not be described as lacking structured fields categorically."*

### 4.2 Detailed Factual Critique
1. **`other_unit_failure_text` has structured fields:**
   - Primary sources S035 (`systemd.catalog.in:561–566`) and S036 (`unit.c:6333–6342`) prove that `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c` emits `UNIT_RESULT=%s`.
   - Possible values in systemd: `resources`, `timeout`, `exit-code`, `signal`, `core-dump`, `watchdog`, `start-limit-hit`, `oom-kill`.
   - Therefore, structured fields exist for differentiating unit failures. The reason they were omitted in r13 is **`unimplemented-structured-filter`**, not absence of structured fields in systemd.
2. **`other_signals` for managed units have structured fields:**
   - Primary sources S035 (`systemd.catalog.in:568–575`) and S036 (`unit.c:6355–6392`) prove that `MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15` emits `EXIT_CODE=killed` with decimal `EXIT_STATUS=<signal>` for *all* signals killing unit processes (e.g. SIGTERM=15, SIGINT=2, SIGABRT=6, SIGHUP=1).
   - Primary source S032 (`systemd-coredump(8)`) proves that `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1` emits `COREDUMP_SIGNAL=<signal>` for all core-dumping signals (e.g. SIGABRT=6, SIGFPE=8, SIGBUS=7, SIGILL=4, SIGQUIT=3).
   - Therefore, structured fields exist for all systemd-supervised process termination signals and crash signals.
3. **What genuinely lacks retained structured records:**
   - Arbitrary signals sent between unmanaged host processes outside systemd unit supervisor observation (and not dumping core) leave **no retained record in the journal in any field**.
   - Raw regex matching over message bodies was retired per Quality Criterion 15 (M13).

### 4.3 Recommended Attribution Disaggregation
The census must distinguish between:
| Category | Identified Classes | Valid Attribution / Reason |
|---|---|---|
| **Unimplemented Structured Queries** | `other_unit_results`, `other_exit_signals`, `other_coredump_signals` | `reason=unimplemented-structured-query` (systemd provides `UNIT_RESULT`, `EXIT_STATUS`, and `COREDUMP_SIGNAL`, but census queries are currently narrowed to specific values). |
| **Architecturally Unrecorded Signals** | `unmanaged_process_signals` | `reason=no-retained-journal-record` (signals delivered outside systemd supervisor observation generate no journal entries). |
| **Retired Text Matching** | `oom_kill_text`, `failed_unit_text`, `gpf_dmesg_text` | `reason=retired-unstructured-message-text` (retired per Criterion 15 / M13; MESSAGE text is display data, not metadata). |

---

## 5. GPF, Text, and General Signal Unsupported Distinctions

### 5.1 General Protection Fault (GPF) Technical Distinction
- **Historical Baseline Text Grep (`1f07f1d:878`):**
  `c_seg=$(printf '%s\n' "$text" | grep -ciE 'segfault|general protection fault' || true)`
- **Architectural Mechanics in Linux x86/x86_64:**
  - Hardware exception `#GP` (vector 13, general protection fault) is handled by the Linux kernel in `arch/x86/kernel/traps.c:do_general_protection()`.
  - The kernel prints a trap notice to the kernel log buffer (`traps: <comm>[<pid>] general protection fault ip:...`).
  - The kernel then delivers **`SIGSEGV` (signal 11)** to the offending userspace process (`force_sig_fault(SIGSEGV, SEGV_ACCERR, ...)` or `SEGV_MAPERR`).
  - When the userspace process crashes, `systemd-coredump` captures the termination and emits:
    `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1`
    `COREDUMP_SIGNAL=11` (`COREDUMP_SIGNAL_NAME=SIGSEGV`)
- **Status of GPF Coverage:**
  - When a retained signal11 coredump-ID record (`MESSAGE_ID=fc2e22bc…` and `COREDUMP_SIGNAL=11`) exists, it is counted under `segfault_signal11`.
  - Any GPF producing no such retained record (such as in-kernel faults, disabled or unintercepted coredumps, or trap events logging only to kernel dmesg) remains unmeasured.
  - Spot-check Note 3 explicitly confirms: *"No proof here establishes a live GPF regression."* However, absence of proof is not proof of no regression: a live GPF regression remains unestablished by source-only inspection.
  - The dropped surface is raw kernel dmesg text matching `"general protection fault"`. Systemd provides no dedicated catalog `MESSAGE_ID` for kernel `#GP` trap lines; counting them required arbitrary text grepping, which was retired per Criterion 15 (M13).
  - Thus, GPF text matching is properly classified as **`retired-unstructured-message-text`**, while retained coredump signal 11 records continue to be counted.

### 5.2 General Signal Coverage Taxonomy
Signal handling in systemd journals falls into three distinct architectural tiers:

```
+---------------------------------------------------------------------------------------+
| 1. MEASURED STRUCTURED CLASSES (Census r13/r14)                                       |
|    - SIGKILL (9) on Unit Processes : MESSAGE_ID=98e32220... EXIT_CODE=killed STATUS=9  |
|    - SIGSEGV (11) on Coredumps      : MESSAGE_ID=fc2e22bc... COREDUMP_SIGNAL=11        |
+---------------------------------------------------------------------------------------+
| 2. UNIMPLEMENTED STRUCTURED CLASSES (Systemd records exist; queries not built)        |
|    - Other Unit Exit Signals        : MESSAGE_ID=98e32220... EXIT_STATUS=<1..8, 10..31> |
|    - Other Coredump Signals         : MESSAGE_ID=fc2e22bc... COREDUMP_SIGNAL=<3,4,6..> |
|      (e.g. SIGABRT=6, SIGBUS=7, SIGFPE=8, SIGILL=4 are grouped in coredump_notice)   |
+---------------------------------------------------------------------------------------+
| 3. ARCHITECTURALLY UNRECORDED SIGNALS (No journal entry created by systemd)           |
|    - Inter-process signals between unmanaged processes (e.g. kill -9 $PID)            |
|    - Signals handled/ignored by the application (no process exit or coredump)         |
|    - Processes killed inside unmonitored tmux scopes/subshells                        |
+---------------------------------------------------------------------------------------+
```

---

## 6. Summary of Findings & Clear Path for Repair Seats

| Domain | Observed Fact | Necessary Action / Contract |
|---|---|---|
| **SIGKILL (`unit_sigkill_record`)** | Uses S035/S036 structured `EXIT_CODE=killed EXIT_STATUS=9` on `98e32220…`. Warns on user scope (`KILL_SIGNAL_JOURNAL warn`), triggering DRIFT. | **Retain verbatim.** Do not modify query fields, filters, or warning roll behavior. |
| **Signal 11 (`segfault_signal11`)** | Uses S013/S032 structured `COREDUMP_SIGNAL=11` on `fc2e22bc…`. Captures both page faults and userspace GPFs. | **Retain verbatim.** Emits `info`; strictly subsets coredump notices. |
| **OOM Alarm** | Demoted to `info` in r13, causing `rejected-harmed` verdict. | **Restore `OOM_KILL_JOURNAL crit` => DRIFT** for positive `kernel_oom_notice` in user/system scope and for `UNIT_RESULT=oom-kill`. |
| **Fleet Unit Failure Routing** | Collapsed in r13 with note *"no fleet classification"*, dropping `UNIT_FAILURE_OUT_OF_SCOPE` and tsukuroi routing. | **Restore fleet vs non-fleet routing** using structured `UNIT`/`USER_UNIT` metadata. Malformed/missing metadata must grade `UNKNOWN`, never false non-fleet. |
| **Unmeasured Reason** | Categorical `reason=no-anchored-structured-field` is overbroad and inaccurate. | **Update reason strings** to distinguish `unimplemented-structured-query` from `no-retained-journal-record` and `retired-unstructured-message-text`. |
| **GPF Coverage** | When a retained signal11 coredump-ID record exists, it is counted. Any GPF producing no such retained record remains unmeasured; live GPF regression is unestablished (absence of proof != proof of no regression). | **Annotate honestly** as retired unstructured dmesg text; do not claim full coredump coverage or prove absence of live regression from source inspection alone. |

- **Tools Installed / Updated:** None.
- **Verification Runs:** None executed (leaf scout contract). All observations derived from source reading and committed evidence.
