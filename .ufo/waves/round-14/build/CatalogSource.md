# CatalogSource Scout Report: S013/S035 Catalog Semantics & OOM Indications

- **Seat**: `MoriR14.CatalogSource` (scout, leaf).
- **Lane Root**: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
- **Milestone**: Restore OOM alarm and structured fleet routing.
- **Judged Axis**: **Coverage** (C1).
- **Target Report File**: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-14/build/CatalogSource.md`.

---

## 1. Godspeed Posture & Named Axes

1. **Name the axes**:
   - **Coverage (Primary Axis)**:
     - Resolve the Round 13 no-harm regression where structured journal cutover eliminated the critical `OOM_KILL_JOURNAL` alarm and flattened fleet versus non-fleet failure routing.
     - Ground journal detection in authoritative catalog entries: S013 (OOM unit notices `fe6faa94…`, systemd-oomd notices `d989611b…`, coredumps `fc2e22bc…`, loss `e9bf28e6…`) and S035 (unit-failed records `d9b373ed…`, unit-process-exit records `98e32220…`).
     - Decouple **OOM alarm indication** (memory exhaustion forcing unit/process termination requiring `crit => DRIFT`) from **unique kernel victim attribution** (accounting individual process deaths at `mm/oom_kill.c`).
   - **Operability**:
     - Maintain strict field-limited JSON queries (`--output-fields=_BOOT_ID,MESSAGE_ID,...`) and structured token matching (`UNIT_RESULT=oom-kill`, `EXIT_CODE=killed EXIT_STATUS=9`).
     - Never parse, match, or echo raw `MESSAGE` strings or canary lines.
   - **Adjacency**:
     - Partition unit failure records by structured unit metadata (`UNIT` / `USER_UNIT`), preserving `UNIT_FAILURE_JOURNAL` (warn) for fleet units and routing non-fleet units to `UNIT_FAILURE_OUT_OF_SCOPE` (info, owner `tsukuroi`).
2. **Iterate cheap, in parallel**:
   - Re-verified pinned upstream git catalog URL, commit digest, local systemd 261 catalog database, and related systemd unit emitter sources concurrently.
3. **Keep moves that improve any axis and harm none**:
   - Restoring the OOM alarm and structured fleet routing repairs the round-13 harm while preserving all round-13 scoped-counter gains.
4. **Don't aim — let the frontier walk itself**.

---

## 2. Pinned Primary Sources S013 & S035 Identity & Integrity

S013 and S035 share the same pinned repository URL and commit bytes, but define two distinct, complementary scopes in `corpus/SOURCES.md`:

| Field | S013 Specification | S035 Specification |
|---|---|---|
| **Registry ID** | `S013` (`corpus/SOURCES.md:19`) | `S035` (`corpus/SOURCES.md:41`) |
| **Title** | systemd message catalog (`systemd.catalog.in`) | systemd process-exit and unit-result catalog |
| **Pinned URL** | `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in` | `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in` |
| **Commit** | `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` (2026-10-19) | `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` (2026-10-19) |
| **SHA-256 Digest** | `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592` | `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592` |
| **Recheck Command** | `curl -fsSL <URL> \| sha256sum` | `curl -fsSL <URL> \| sha256sum` |
| **Recheck Digest** | `e53707db...` (exact match) | `e53707db...` (exact match) |
| **Catalog Scope** | `catalog/systemd.catalog.in:66,604,884` | `catalog/systemd.catalog.in:561-575` |
| **Declared Semantics** | Message IDs for coredumps, kernel OOM unit notices, and systemd-oomd kills | Message IDs for unit failure (`UNIT_RESULT`) and process exit (`EXIT_CODE`/`EXIT_STATUS`) |
| **Access Date** | `2026-10-20` (re-opened) | `2026-10-20` (re-opened) |

---

## 3. Exact Located Quotes (≤ 25 Words)

All quotes are taken verbatim from the verified S013/S035 pinned catalog bytes (`catalog/systemd.catalog.in` at commit `cf8ebfc6`):

| Source ID | Catalog ID / Field | Location in Catalog | Exact Verbatim Quote | Word Count |
|---|---|---|---|:---:|
| **S013** | `fe6faa94e7774663a0da52717891d8ef` (Subject) | Line 605 | `Subject: A process of @UNIT@ unit has been killed by the OOM killer.` | 13 words |
| **S013** | `fe6faa94e7774663a0da52717891d8ef` (Body) | Lines 609–610 | `A process of unit @UNIT has been killed by the Linux kernel out-of-memory (OOM) killer logic.` | 15 words |
| **S013** | `fe6faa94e7774663a0da52717891d8ef` (Causation) | Line 615 | `Note that the memory pressure might or might not have been caused by @UNIT@.` | 14 words |
| **S013** | `d989611b15e44c9dbf31e3c81256e4ed` (Subject) | Line 885 | `Subject: systemd-oomd killed one or more processes in unit @UNIT@` | 10 words |
| **S013** | `d989611b15e44c9dbf31e3c81256e4ed` (Body) | Lines 890–891 | `One or more processes in the @UNIT@ unit have been killed by systemd-oomd, in order to counter an out-of-memory situation on the system.` | 22 words |
| **S013** | `d989611b15e44c9dbf31e3c81256e4ed` (Causation) | Line 895 | `Note that the memory pressure might or might not have been caused by @UNIT@.` | 14 words |
| **S013** | `e9bf28e6e834481bb6f48f548ad13606` (Body) | Lines 63–64 | `Kernel messages have been lost as the journal system has been unable to process them quickly enough.` | 17 words |
| **S013** | `fc2e22bc6ee647b6b90729ab34a250b1` (Body) | Line 72 | `Process @COREDUMP_PID@ (@COREDUMP_COMM@) crashed and dumped core.` | 8 words |
| **S035** | `d9b373ed55a64feb8242e02dbe79a49c` (Subject) | Line 562 | `Subject: Unit failed` | 3 words |
| **S035** | `d9b373ed55a64feb8242e02dbe79a49c` (Body) | Line 566 | `The unit @UNIT@ has entered the 'failed' state with result '@UNIT_RESULT@'.` | 11 words |
| **S035** | `98e322203f7a4ed290d09fe03c09fe15` (Subject) | Line 569 | `Subject: Unit process exited` | 4 words |
| **S035** | `98e322203f7a4ed290d09fe03c09fe15` (Body 1) | Line 573 | `An @COMMAND@= process belonging to unit @UNIT@ has exited.` | 9 words |
| **S035** | `98e322203f7a4ed290d09fe03c09fe15` (Body 2) | Line 575 | `The process' exit code is '@EXIT_CODE@' and its exit status is @EXIT_STATUS@.` | 12 words |
| **S035** | `3e650c8227694f479ea5e57fe9cf6a1f` (Body) | Lines 558–560 | `The unit @UNIT@ was skipped due to an ExecCondition= command failure, and has entered the 'dead' state with result '@UNIT_RESULT@'.` | 20 words |

Every quote strictly respects the $\le 25$ words limit and references verifiable lines in `systemd.catalog.in`.

---

## 4. Extraction of Semantics: OOM Notices vs Unit Results & Process Exits

### 4.1 S013: OOM Notices (`fe6faa94…` and `d989611b…`)
1. **Kernel OOM Unit Notice (`fe6faa94e7774663a0da52717891d8ef`)**:
   - **Emitter**: systemd (PID 1 / user manager) upon receiving kernel OOM notification or detecting cgroup termination.
   - **Semantic Unit**: Notification that a process belonging to `@UNIT@` was forcibly terminated by the Linux kernel OOM killer logic.
   - **Cardinality**: **Not 1:1 with kernel victim events** [SOURCE: S013:605/609 is singular ("A process of unit @UNIT@ has been killed"), whereas S013 specifies no cross-manager emission cardinality guarantee].
   - **Fan-Out [INFERENCE & EMPIRICAL OBSERVATION]**: Multi-unit fan-out across manager scopes is an `[INFERENCE]` supported by empirical trace (e.g. host boot `7bd93aee…` produced 5 kernel printk kills vs 7 user + 9 system journal notices). S013 does not define fan-out mechanics.
   - **Causality**: The catalog explicitly warns: *"Note that the memory pressure might or might not have been caused by @UNIT@."* The unit is an observed victim container, not necessarily the culprit.
   - **Data Carried**: Unit name (`@UNIT@`), but no victim PID, UID, or comm in the catalog structured template.
2. **Userspace OOM Kill Notice (`d989611b15e44c9dbf31e3c81256e4ed`)**:
   - **Emitter**: `systemd-oomd.service`.
   - **Semantic Unit**: Userspace termination of one or more processes within `@UNIT@` to relieve pressure.
   - **Cardinality**: Explicitly $\ge 1$ (*"killed one or more processes in unit @UNIT@"*).
   - **Kernel Counter Bypass**: These kills are executed directly via `SIGKILL` / `cgroup.kill` and do not increment kernel `mm/oom_kill.c` counters.

### 4.2 S035: Unit Results (`d9b373ed…`) & Process Exits (`98e32220…`)
1. **Unit Failure Record (`d9b373ed55a64feb8242e02dbe79a49c`)**:
   - **Emitter**: `unit_log_failure(Unit *u, const char *result)` in `src/core/unit.c:6333-6342`.
   - **Semantic Unit**: Lifecycle transition of unit `@UNIT@` to the `failed` state with failure reason `@UNIT_RESULT@`.
   - **Structured Fields**: Emits `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c`, `UNIT_RESULT=%s`, plus unit invocation ID and unit names.
   - **Result Domain**: In `src/core/service.c:6598` and `src/core/service.h:89`, systemd defines `SERVICE_FAILURE_OOM_KILL` which renders string `"oom-kill"`.
2. **Process Exit Record (`98e322203f7a4ed290d09fe03c09fe15`)**:
   - **Emitter**: `unit_log_process_exit(...)` in `src/core/unit.c:6355-6392`.
   - **Semantic Unit**: Direct notification that a specific process belonging to unit `@UNIT@` exited.
   - **Structured Fields**: Emits `MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15`, `EXIT_CODE=%s` (e.g. `"killed"`), `EXIT_STATUS=%i` (e.g. `9`), and `COMMAND=%s`.
   - **Distinction**: Captures the process-level signal/exit code, whereas `d9b373ed…` captures the aggregate unit lifecycle state.

---

## 5. Decision: Does Result `oom-kill` Constitute an OOM Indication Without a Unique Victim Claim?

### Decision: **YES.**

`UNIT_RESULT=oom-kill` constitutes a valid, **structured client-labeled OOM indication sufficient for policy alarm (`OOM_KILL_JOURNAL crit => DRIFT`)**, while **not constituting authenticated emitter or kill proof**, and **strictly refraining from making any unique victim claim**.

### Evidence & Rationale:

1. **Structured Client-Labeled OOM Indication (Sufficient for Policy Alarm, Not Authenticated Emitter/Kill Proof)**:
   - **Trust Boundary (S015)**: Under S015 (`systemd.journal-fields(7)`), fields without an underscore prefix (such as `MESSAGE_ID` and `UNIT_RESULT`) are client-supplied fields carrying unvalidated source trust (`trust=client-supplied`). They do not constitute cryptographically or kernel-authenticated emitter proof.
   - **Policy Alarm Sufficiency**: In operational monitoring, a structured client-labeled event indicating `UNIT_RESULT=oom-kill` or catalog notice `fe6faa94…` is sufficient to trigger a node policy alarm (`OOM_KILL_JOURNAL crit => DRIFT`). It informs the fleet that memory exhaustion forced unit/process termination, without requiring authenticated kernel victim proof.
   - **Source Mapping (S035 / S038)**:
     - In systemd service execution (`systemd.service(5)`), services terminated due to kernel or userspace OOM enter the `"oom-kill failed state"`.
     - In `src/core/service.h:89` and `src/core/service.c:4723-4752, 6588, 6598` (which L1 is opening as `S038`), `SERVICE_FAILURE_OOM_KILL` is mapped to string `"oom-kill"`.
     - When this occurs, systemd emits unit failure catalog entry `d9b373ed55a64feb8242e02dbe79a49c` (S035 line 566) with `UNIT_RESULT=oom-kill`.

2. **Alarm Indication $\ne$ Unique Victim Accounting**:
   - As ruled by the Round 13 outside verifier spot-check (`corpus/lessons/round-13-verifier-spotcheck.md:85`):
     > *"Structured selection is better than unsafe text matching, but it does not require discarding the OOM warning/DRIFT behavior; a notice need not identify a unique victim to be reported as an OOM warning. The analogous client-set-ID caveat did not prevent retaining SIGKILL WARN."*
   - An operational alarm answers: *"Did an unhandled memory crisis force process termination on this node?"* The answer is YES, requiring `OOM_KILL_JOURNAL crit => DRIFT`.
   - Unique victim accounting answers: *"How many distinct tasks were terminated at `mm/oom_kill.c:935`?"* That question belongs exclusively to kernel dmesg attribution (`oom-kill:constraint=...`) and `/proc/vmstat` counters.

3. **Why `UNIT_RESULT=oom-kill` Makes NO Unique Victim Claim**:
   - **Unit-Level Granularity**: The catalog entry at S035 line 566 states: *"The unit @UNIT@ has entered the 'failed' state with result '@UNIT_RESULT@'."* It names the unit, not a process.
   - **No Victim Process Metadata**: The record carries no victim PID, task name, UID, or virtual memory size.
   - **Indeterminate Multi-Process Cardinality**: A unit may contain multiple processes. Under cgroup v2 `memory.oom.group=1`, a single OOM event kills all processes in the cgroup simultaneously, yet results in a single `UNIT_RESULT=oom-kill` unit failure. Conversely, multiple child processes in different units may fail during a single system-wide OOM crisis.
   - **Causal Uncertainty**: In accordance with S013:615 and S013:895, memory pressure affecting a unit might or might not have been caused by that unit.
   - Therefore, asserting that an OOM failure occurred does not assert that the unit was the sole cause, nor does it assert that the record represents a $1:1$ count of unique kernel-killed processes.

4. **Preservation of Scoped Counters**:
   - Scoped counter gains from Round 13 remain intact: `UNIT_RESULT=oom-kill` and OOM notices (`fe6faa94…`) are recorded under explicit `user` and `system` scopes, and are **never summed**.
   - Emitting `OOM_KILL_JOURNAL crit` whenever an OOM notice (`fe6faa94…`) or a failed unit with `UNIT_RESULT=oom-kill` is observed directly resolves the verifier's admission failure without violating any accounting constraint.

---

## 6. Recommendations for Implementation Seats

1. **For `MoriR14.CensusRepair` (`tools/mori-census.sh`)**:
   - **OOM Alarm Restoration**: If any positive kernel OOM notice (`fe6faa94…`) OR any unit failure with `UNIT_RESULT=oom-kill` is detected in either `user` or `system` scope, emit `emit_finding OOM_KILL_JOURNAL crit "..."` (which triggers `DRIFT`).
   - **Unit Failure Classification & Fleet Routing**:
     - Query `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c` requesting fields `_BOOT_ID,MESSAGE_ID,UNIT_RESULT,UNIT,USER_UNIT`.
     - Partition failures by unit subject:
       - Fleet units (matching fleet prefixes / conventions): emit `UNIT_FAILURE_JOURNAL warn`.
       - Non-fleet units (OS/system units): emit `UNIT_FAILURE_OUT_OF_SCOPE info` with attribute `owner=tsukuroi`.
     - If `UNIT_RESULT=oom-kill`, also trigger the `OOM_KILL_JOURNAL crit` alarm.
   - **Zero & Error Integrity**:
     - Empty query returns count 0 and `CLEAN`.
     - Missing unit metadata or corrupted JSON returns status `unknown` / `malformed-json`, never a fabricated zero.
     - Never output or parse raw `MESSAGE` strings.
2. **For `MoriR14.EmitterSource` & `MoriR14.JournalFields`**:
   - Confirm that `unit_log_failure` emits `UNIT_RESULT` alongside unit names (`UNIT` / `USER_UNIT`).
   - Warn against using manager emitter fields (`_SYSTEMD_UNIT`) as the failed unit, because in user journals `_SYSTEMD_UNIT` is `user@1000.service`, whereas `UNIT` or `USER_UNIT` identifies the actual target unit.
3. **For `MoriR14.QualityCriteria`**:
   - Verify that Q29+ requires no-harm alarm and severity preservation, and explicitly distinguishes structured OOM alarms from unique victim claims.

---

## 7. Evidence Limits

- Upstream catalog URL verified via remote SHA-256 digest (`e53707db...`) matching `corpus/SOURCES.md:19` and `:41`.
- Local catalog entries verified via host `journalctl --list-catalog`.
- All quotes verified against `/tmp/systemd.catalog.in` with exact word counts $\le 25$ words.
- No production scripts or test suites were executed by this seat.
- No modifications were made outside of writing this report at `.ufo/waves/round-14/build/CatalogSource.md`.
