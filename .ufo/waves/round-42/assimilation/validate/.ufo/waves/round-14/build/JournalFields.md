# JournalFields — S015/S037 Trusted vs Client Journal Metadata Analysis

**Seat**: `MoriR14.JournalFields` (scout, leaf)  
**Lane Root**: `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Milestone**: Restore OOM alarm and structured fleet routing  
**Judged On**: `coverage` (primary)  
**Safety & Bounds**: Leaf member — no subagent dispatch, no background jobs, no build/test/lint runs, no git commits/pushes. Owns only this report at `.ufo/waves/round-14/build/JournalFields.md`.

---

## 1. Executive Summary & Named Axes

- **Coverage (Primary Axis)**:
  - Mori round 13 achieved structured, MESSAGE-free record counting across independent `journal.user` and `journal.system` surfaces, but suffered an admission rejection (`rejected-harmed`) due to two fatal regressions:
    1. Demoting critical `OOM_KILL_JOURNAL` (DRIFT) to an informational notice.
    2. Collapsing fleet-unit failure triage (`UNIT_FAILURE_JOURNAL`) and non-fleet desktop/OS triage (`UNIT_FAILURE_OUT_OF_SCOPE`, owner `tsukuroi`) into a single unclassified notice without owner routing.
  - S015 (`systemd.journal-fields(7)`) and new row S037 provide the structured metadata foundation required to repair fleet routing **without reverting to regex matching on unparsed `MESSAGE` text**.
  - Restoring fleet routing requires extracting the **subject unit** (`UNIT=` / `USER_UNIT=`), not the **emitting process unit** (`_SYSTEMD_UNIT=` / `_SYSTEMD_USER_UNIT=`).

- **Adjacency & Operability (Harm None)**:
  - **Adjacency**: Restores clean division between mori-owned fleet failures (`shokunin`, `ufo-sighting`, `tmux-spawn`, `the-tick`, `fleet`) and adjacent owner `tsukuroi` (`UNIT_FAILURE_OUT_OF_SCOPE` for desktop/OS services like `pipewire-pulse.service`).
  - **Operability**: Prevents misidentifying the service manager daemon (`systemd --user` / `user@1000.service` or PID 1 `init.scope`) as the failed service. Enforces Quality Criterion 30: missing, malformed, or array subject metadata must evaluate to explicit `UNKNOWN` / `unavailable`, never defaulting to non-fleet or zero.

---

## 2. Pinned Authorities & Source Anchors

| Source Key | Authority & URL | Pinned Anchor / Location | Teaches |
|---|---|---|---|
| **S015** | `systemd.journal-fields(7)` — [Canonical man page](https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html) | `User Journal Fields > MESSAGE=:34-36, MESSAGE_ID=:40-42`; `Trusted Journal Fields > _BOOT_ID=:100, _TRANSPORT=:106-128`; systemd 262 / 261 | `MESSAGE` is unparsed display text; `MESSAGE_ID` is client-supplied typed key; underscore-prefixed fields are kernel/daemon trusted metadata. |
| **S037** | `systemd subject-unit journal metadata` — [Canonical man page](https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html) | `User Journal Fields > UNIT=, USER_UNIT=`; `Trusted Journal Fields > _SYSTEMD_UNIT=, _SYSTEMD_USER_UNIT=`; systemd 262 / 261 | `UNIT`/`USER_UNIT` specify the subject unit a manager logs about; trusted `_SYSTEMD_UNIT` describes the emitting process, not the failed subject. |
| **S036** | `systemd unit.c emitter` — [systemd commit cf8ebfc6](https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c) | `src/core/unit.c:6333-6392` (`unit_log_failure`, `unit_log_process_exit`), `src/core/unit.c:6772-6778` (`unit_log_field`), `src/core/unit.h:601-605` (`LOG_UNIT_ID`) | Emitter macro `LOG_UNIT_ID` attaches `UNIT=` for system manager and `USER_UNIT=` for user manager; writes `UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS`. |

---

## 3. Trusted vs Client (User) Journal Metadata in S015

S015 formally establishes a strict boundary between two categories of fields:

### 3.1 Client / User Journal Fields (No Leading Underscore)
- **Upstream Definition** (S015 `User Journal Fields`):
  > *"User fields are fields that are directly passed from clients and stored in the journal."*
  > *"Note that the journal service does not validate the values of any structured journal fields whose name is not prefixed with an underscore..."*
- **Characteristics**:
  - Passed across the journal datagram socket (`/run/systemd/journal/socket`).
  - Stored verbatim without journald kernel verification of caller authority.
  - Includes: `MESSAGE`, `MESSAGE_ID`, `PRIORITY`, `CODE_FILE`, `ERRNO`, `INVOCATION_ID`, `USER_INVOCATION_ID`, and **`UNIT=, USER_UNIT=`**.
  - **Trust Status**: `trust=client-supplied`. Any local process can write arbitrary values to these fields unless authenticated via trusted peer fields.

### 3.2 Trusted Journal Fields (Leading Underscore `_`)
- **Upstream Definition** (S015 `Trusted Journal Fields`):
  > *"Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly added by the journal and cannot be altered by client code."*
- **Characteristics**:
  - Added automatically by `systemd-journald` using kernel socket credentials (`SO_PEERCRED`), cgroup inspection (`/proc/$PID/cgroup`), or kernel subsystem ingestion (`/dev/kmsg`).
  - Cannot be forged or overridden by unprivileged clients.
  - Includes: `_PID`, `_UID`, `_GID`, `_COMM`, `_EXE`, `_TRANSPORT`, `_BOOT_ID`, `_SYSTEMD_CGROUP`, and **`_SYSTEMD_UNIT=, _SYSTEMD_USER_UNIT=`**.
  - **Trust Status**: Authoritative origin identity.

---

## 4. Subject Metadata (`UNIT`/`USER_UNIT`) vs Emitter Fields (`_SYSTEMD_UNIT`/`_SYSTEMD_USER_UNIT`)

The fundamental architectural distinction between subject and emitter metadata is critical to correct journal parsing:

```
+-----------------------------------------------------------------------------------------------+
| Log Entry Generated When A Unit Fails (e.g. the-tick.service)                                 |
+-----------------------------------------------------------------------------------------------+
| EMITTING PROCESS: systemd manager daemon (PID 1 or systemd --user)                            |
|   -> Kernel / journald attaches TRUSTED fields describing the EMITTER:                        |
|        _COMM = "systemd"                                                                      |
|        _SYSTEMD_UNIT = "user@1000.service" (user scope) or "init.scope" (system scope)       |
|        _SYSTEMD_USER_UNIT = "init.scope"   (user scope)                                       |
+-----------------------------------------------------------------------------------------------+
| SUBJECT OF LOG MESSAGE: the unit being managed (the-tick.service)                             |
|   -> Manager code explicitly passes CLIENT / USER fields describing the SUBJECT:              |
|        UNIT = "the-tick.service"           (in system manager)                                |
|        USER_UNIT = "the-tick.service"      (in user manager)                                  |
|        UNIT_RESULT = "failed" / "oom-kill"                                                    |
+-----------------------------------------------------------------------------------------------+
```

### 4.1 Specification & S015 Anchors

1. **`UNIT=, USER_UNIT=` (Subject Unit)**:
   - S015 Section: `USER JOURNAL FIELDS`.
   - Upstream text:
     > *"The name of a unit. Used by the system and user managers when logging about specific units. When --unit=name or --user-unit=name are used with journalctl(1), a match pattern that includes 'UNIT=name.service' or 'USER_UNIT=name.service' will be generated. Added in version 251."*
   - Function: Explicitly conveys **which service failed, exited, or was acted upon**.

2. **`_SYSTEMD_UNIT=, _SYSTEMD_USER_UNIT=` (Emitter Unit)**:
   - S015 Section: `TRUSTED JOURNAL FIELDS`.
   - Upstream text:
     > *"The control group path in the systemd hierarchy, the systemd slice unit name, the systemd unit name, the unit name in the systemd user manager (if any), the systemd session ID (if any), and the owner UID of the systemd user unit or systemd session (if any) of the process the journal entry originates from."*
   - Function: Conveys **which process emitted the log message**.

### 4.2 Upstream Emitter Implementation (S036 Verification)

In systemd core (`src/core/unit.c` and `src/core/unit.h` at commit `cf8ebfc6`):
- When a unit fails (`unit_log_failure`) or a process exits (`unit_log_process_exit`):
  ```c
  // src/core/unit.h:603
  #define LOG_UNIT_ID(unit) LOG_ITEM("%s%s", unit_log_field((unit)), (unit)->id)

  // src/core/unit.c:6772-6774
  const char* unit_log_field(const Unit *u) {
          return MANAGER_IS_SYSTEM(ASSERT_PTR(u)->manager) ? "UNIT=" : "USER_UNIT=";
  }
  ```
- In the system manager (`systemd` PID 1), `MANAGER_IS_SYSTEM()` is true $\rightarrow$ emits `UNIT=<unit_id>`.
- In the user manager (`systemd --user`), `MANAGER_IS_SYSTEM()` is false $\rightarrow$ emits `USER_UNIT=<unit_id>`.

---

## 5. Live Host Empirical Verification

Empirical evidence retrieved from the active host journal (`systemd 261.2-1-arch`, Linux `7.2.3-arch1-3`):

### 5.1 User Scope Lifecycle Event (`systemd --user` logging about `ai-usage.service`)
```json
{
  "_COMM": "systemd",
  "_SYSTEMD_UNIT": "user@1000.service",
  "_SYSTEMD_USER_UNIT": "init.scope",
  "USER_UNIT": "ai-usage.service",
  "MESSAGE_ID": "39f53479d3a045ac8e11786248231fbf",
  "_BOOT_ID": "430d3038185949e682cf5fc475d1b3d0"
}
```
- **Observed Emitter**: `_SYSTEMD_UNIT="user@1000.service"`, `_SYSTEMD_USER_UNIT="init.scope"` (the user manager daemon).
- **Observed Subject**: `USER_UNIT="ai-usage.service"` (the unit being managed).

### 5.2 System Scope Lifecycle Event (PID 1 logging about `snapperd.service`)
```json
{
  "_COMM": "systemd",
  "_PID": "1",
  "_SYSTEMD_UNIT": "init.scope",
  "UNIT": "snapperd.service",
  "MESSAGE_ID": "7ad2d189f7e94e70a38c781354912448",
  "_BOOT_ID": "430d3038185949e682cf5fc475d1b3d0"
}
```
- **Observed Emitter**: `_SYSTEMD_UNIT="init.scope"`, `_PID="1"` (the system manager daemon).
- **Observed Subject**: `UNIT="snapperd.service"` (the unit being managed).

---

## 6. Architectural Warning: Operational Risks of Misinterpreting Manager Emitter Identity as Failed Unit

If a census probe or monitoring classifier inspects `_SYSTEMD_UNIT` or `_SYSTEMD_USER_UNIT` instead of subject fields to identify a failed service, significant classification risks arise:

### 6.1 Risk 1: Hypothetical False Non-Fleet Misclassification & Dropped Fleet Outages (Under Shown Manager Metadata)
- In user scope, manager-emitted records (`d9b373ed...` unit failure, `98e32220...` process exit, `fe6faa94...` OOM notice) observe:
  `_SYSTEMD_UNIT="user@1000.service"`, `_SYSTEMD_USER_UNIT="init.scope"` in the measured host traces.
- In system scope, PID 1 lifecycle entries observe:
  `_SYSTEMD_UNIT="init.scope"`.
- Under the fleet unit predicate (`shokunin|ufo-sighting|tmux-spawn|the-tick|fleet`), neither `user@1000.service` nor `init.scope` matches the pattern.
- **Qualification & Causal Scope**:
  - The claim that testing `_SYSTEMD_UNIT` produces "100% false non-fleet misclassification" or drops "all fleet outages" is a **hypothetical deduction based on the specific manager emitter metadata observed in host traces**, not an empirically measured universal fact across every systemd setup or unit execution model.
  - Emitter metadata may vary under different unit types, delegation configurations, container runtimes, or systemd versions.
  - Nevertheless, under the shown manager emitter values, any classifier relying on `_SYSTEMD_UNIT` would misroute those specific manager notices away from fleet alerting to non-fleet routing (`UNIT_FAILURE_OUT_OF_SCOPE`).

### 6.2 Risk 2: Potential Spurious Manager-Level Failure Attribution
- If a consumer naively treats the emitter unit field as the failed subject, records emitted by the manager daemon when a unit fails could be misinterpreted as indicating an issue with `init.scope` (the OS init system) or `user@1000.service` (the user manager session).
- **Qualification**:
  - A field-only read of journal metadata does not prove that every implementation or downstream consumer will trigger false-positive manager crash alarms. Downstream alert logic may apply secondary filtering, severity thresholds, or exit code constraints.
  - The architectural distinction remains vital: emitter fields describe the reporter, not the failed subject.

### 6.3 Risk 3: Loss of Subject Granularity
- In records where the manager logs about distinct failed child services, relying on the emitter field collapses different failed services into the manager's own cgroup/unit identity (`init.scope` or `user@1000.service`), obscuring which specific child unit triggered the entry.

---

## 7. Mandatory Conformance: Quality Criterion 30 & Missing Metadata Discipline

To prevent silent misclassification, round 14 established **Quality Criterion 30** (`corpus/QUALITY.md:72`):

> *"30. Unit classification is read from the failed subject's own `UNIT`/`USER_UNIT` structured metadata, never inferred from manager emitter fields; missing, malformed or unreadable subject metadata is an explicit UNKNOWN/unavailable class and is never counted as fleet, non-fleet, or zero."*

### Defensive Rules for Consumers (`CensusRepair` / `probe_journal`):
1. **Never Fall Back to `_SYSTEMD_UNIT`**:
   If `USER_UNIT` and `UNIT` are absent, the subject is **unidentifiable**. Do not use `_SYSTEMD_UNIT`.
2. **Missing Metadata $\rightarrow$ Explicit `UNKNOWN` / `unavailable`**:
   A failure record lacking subject unit metadata must never be defaulted to non-fleet (`UNIT_FAILURE_OUT_OF_SCOPE`) and never silently discarded as zero. It must be accounted as `class=unit_failure_unknown status=unknown`.
3. **JSON Array Handling**:
   Journal entries with duplicate fields or non-UTF8 bytes serialize as JSON arrays (per S014 `json` rules). If `USER_UNIT` or `UNIT` is an array rather than a single string, parse strictly or treat as `record-invalid`/`unknown`.
4. **Zero Record Leakage**:
   In accordance with C1 safety rules, never echo unvalidated unit string bytes to findings or logs; report validated integer counts only.

---

## 8. Exact Located Quotes for Pinned Source Rows (≤ 25 Words)

These quotes substantiate the subject vs. emitter distinction for the source registry and knowledge notes:

1. **S037 / S015 (User Journal Fields — Subject Unit)**:
   - **Source**: `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html`
   - **Section**: `USER JOURNAL FIELDS > UNIT=, USER_UNIT=`
   - **Located Quote** (16 words, $\le 25$):
     > *“The name of a unit. Used by the system and user managers when logging about specific units.”*

2. **S015 / S037 (Trusted Journal Fields — Emitter Unit)**:
   - **Source**: `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html`
   - **Section**: `TRUSTED JOURNAL FIELDS > _SYSTEMD_UNIT=`
   - **Located Quote** (18 words, $\le 25$):
     > *“...of the systemd user unit or systemd session (if any) of the process the journal entry originates from.”*

3. **S036 (Core Unit Emitter Implementation)**:
   - **Source**: `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c`
   - **Location**: `src/core/unit.c:6773` (`unit_log_field`)
   - **Located Quote** (6 words, $\le 25$):
     > `return MANAGER_IS_SYSTEM(ASSERT_PTR(u)->manager) ? "UNIT=" : "USER_UNIT=";`

---

## 9. Sourced Recommendation for `CensusRepair` Implementation

To restore `UNIT_FAILURE_JOURNAL` (fleet) vs `UNIT_FAILURE_OUT_OF_SCOPE` (tsukuroi) without reading `MESSAGE`:

1. **Journal Query Fields**:
   Pass `--output-fields=_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT` for unit failure queries (`MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c`).
2. **JQ Subject Unit Extraction**:
   Extract `unit_name` via:
   ```jq
   (.USER_UNIT // .UNIT // null)
   ```
3. **Structured Classification**:
   - If `unit_name == null` or `(unit_name | type) != "string"`: Increment `n_unit_unknown`.
   - If `unit_name | test("shokunin|ufo-sighting|tmux-spawn|the-tick|fleet")`: Increment `n_unit_fleet`.
   - Else: Increment `n_unit_nonfleet`.
4. **Finding Emission**:
   - `n_unit_fleet > 0` $\rightarrow$ `emit_finding UNIT_FAILURE_JOURNAL info "class=unit_failure count=$n_unit_fleet scope=fleet-units"`
   - `n_unit_nonfleet > 0` $\rightarrow$ `emit_finding UNIT_FAILURE_OUT_OF_SCOPE info "class=unit_failure count=$n_unit_nonfleet note=non-fleet units (desktop/OS) — tsukuroi owns these"`
   - `n_unit_unknown > 0` $\rightarrow$ `emit_finding UNIT_FAILURE_UNCLASSIFIED info "class=unit_failure count=$n_unit_unknown note=missing or non-string unit metadata"`
5. **OOM Restoration**:
   Positive `fe6faa94...` kernel OOM notice in either scope or `UNIT_RESULT=oom-kill` restores `emit_finding OOM_KILL_JOURNAL crit` $\rightarrow$ `DRIFT`.

---

## 10. Tooling Record

- **Tools Installed / Updated**: None. Standard system utilities (`man 7 systemd.journal-fields`, `journalctl`, `jq`, `curl`) used strictly read-only.
