# ConnectSourceChain: S014, S015, S037, S038 Source Chain & Cross-Axis Synthesis

**Seat**: `MoriR15.ConnectSourceChain` (Role: connector, leaf member)  
**Lane Root**: `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Milestone**: Retain validated positives without fabricated totals  
**Judged On**: `coverage` (primary owned axis)  
**Safety & Protocol**: Report-only leaf member; no subagent dispatch; no production file edits; no verification or test commands run; no package installs or system updates (parent host-safety directive acknowledged).

---

## 1. Executive Summary & Named Axes

In Mori Round 15, Claim C1 focuses on **coverage** (the lowest owned axis, score 6 vs operability 7):
> *Preserve critical OOM and user signal alarms from individually valid current-boot structured records even when an adjacent malformed/nonmatching/foreign-boot record invalidates the aggregate class. Existing raw aggregate/split counts stay unavailable when invalid. Do not claim completeness, authenticated IDs, unique victims, or repair arbitrary malformed JSON.*

### 1.1 The Declared Axes (Godspeed Step 1)
- **Coverage (Judged Axis, Improves 6 → 7)**:
  Eliminates the dangerous aggregate-suppression defect (F1) where an adjacent foreign-boot, duplicate-array, or malformed record completely silences critical `OOM_KILL_JOURNAL` (crit) or `KILL_SIGNAL_JOURNAL` (warn) alarms despite the presence of individually valid current-boot positive evidence.
- **Operability (Guard Axis, Harmless, Held at 7)**:
  Guarantees that raw aggregate totals and split counters are NEVER faked, salvaged, or represented as numeric zeros when the stream is corrupted; they remain strictly `unavailable:<reason>`. Retains single-query capture without spawning extra journalctl queries or racing time windows.
- **Depth (Harmless, Held at 5)**:
  Grounded strictly in four primary authorities: S014 (`journalctl(1)`), S015 (`systemd.journal-fields(7)`), S037 (subject-unit metadata), and S038 (`src/core/service.c` result vocabulary).
- **Calibration (Harmless, Held at 6)**:
  Maintains explicit trust boundaries (`trust=client-supplied` for `MESSAGE_ID` and `UNIT_RESULT`); distinguishes notice/consequence alarms from authenticated kernel victim counts.
- **Freshness & Adjacency (Harmless, Held at 5 & 6)**:
  Preserves the clear provincial boundary with `tsukuroi` (OS/desktop service owner vs fleet owner) and prevents drift from synthetic or forged counters.

---

## 2. Pinned Authorities & Primary Source Chain Analysis

The round-15 positive evidence architecture connects four primary authorities:

| Source ID | Canonical Authority & Location | Primary Subject / Pinned Anchors | Role in Claim C1 |
|---|---|---|---|
| **S014** | `journalctl(1)` manual (systemd 262 / 261.2) | `--output-fields=`, `-b`, `-o json`, exit codes, field matching | Governs single-query stream capture, field projection without raw `MESSAGE`, exit code handling, and newline-delimited JSON stream ingestion. |
| **S015** | `systemd.journal-fields(7)` manual | `User Journal Fields` vs `Trusted Journal Fields`, array serialization | Defines the strict boundary between trusted fields (`_BOOT_ID`) and client fields (`MESSAGE_ID`, `UNIT_RESULT`), and dictates scalar vs array handling. |
| **S037** | `systemd subject-unit metadata` (`journal-fields(7)`) | `UNIT=`, `USER_UNIT=` vs `_SYSTEMD_UNIT=`, `_SYSTEMD_USER_UNIT=` | Decouples subject-unit routing (fleet vs non-fleet partition) from result consequence alarms (`UNIT_RESULT=oom-kill`). |
| **S038** | `systemd service result vocabulary` (`service.c:6588-6602`) | `service_result_table`, `SERVICE_FAILURE_OOM_KILL` | Establishes the exact primary strings (`"oom-kill"`, `"signal"`) that indicate unit failure consequence without implying kernel victim proof. |

---

## 3. Deep Analysis: Source Evidence vs Policy

### 3.1 S014 (`journalctl(1)`): Query Selection Mechanics & Stream Integrity
- **Upstream Mechanics**:
  - `journalctl` matches command-line arguments (e.g. `MESSAGE_ID=<id>`) server-side. However, journalctl's command-line filtering does not enforce JSON typing or schema validity. If client entries contain repeated keys, journalctl serializes them as JSON arrays (`S014:215`).
  - Specifying `--output-fields=_BOOT_ID,MESSAGE_ID,...` suppresses free-text `MESSAGE` strings while ensuring structured identifiers are present.
  - In `-o json` mode, records are emitted as individual JSON objects separated by newline characters (`\n`).
- **Policy Contract vs Evidence**:
  - *Contract Rule*: "Use same captured successful stderr-free valid JSON stream, no extra journal query."
  - *Connection*: Mori executes `journalctl` once per class/scope into `CAP_OUT`. No secondary journalctl process is allowed. If `journalctl` exits non-zero (e.g. `rc=1` permission denied, `rc=124` timeout) or writes to stderr, both raw aggregates and positive evidence must grade `unavailable:<reason>`. Positive evidence can only be evaluated when the single captured stream is successfully retrieved.

### 3.2 S015 (`systemd.journal-fields(7)`): Field Types, Trust Boundaries, and Representation
- **Upstream Mechanics**:
  - S015 divides metadata into:
    1. **Trusted Journal Fields** (`_` prefix): implicitly added by journald from kernel socket credentials (`SO_PEERCRED`), cgroup paths, or kmsg. Includes `_BOOT_ID`, `_PID`, `_UID`, `_TRANSPORT`, `_SYSTEMD_UNIT`. Client code cannot forge or alter these.
    2. **User Journal Fields** (no `_` prefix): passed directly from clients across `/run/systemd/journal/socket`. Includes `MESSAGE`, `MESSAGE_ID`, `UNIT`, `USER_UNIT`, `UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS`. Journald performs no value or type validation.
  - Crucially: if a journal entry has duplicate keys, S015 dictates that journald serializes the field value as a JSON array.
- **Policy Contract vs Evidence**:
  - *Contract Rule*: "They count ONLY object records with scalar matching MESSAGE_ID and scalar current _BOOT_ID; unit result exact string oom-kill/signal; process exact killed and scalar status 9."
  - *Connection*:
    1. `_BOOT_ID` is trusted. Checking `._BOOT_ID == $boot` guarantees the record belongs to the current boot. To exclude arrays or nulls, jq must enforce `(._BOOT_ID | type) == "string"`.
    2. `MESSAGE_ID` is client-supplied. Any local process can write `MESSAGE_ID=fe6faa94...`. Thus, a positive record proves that a structured record exists; it is NOT authenticated proof of a kernel verdict or unique victim. Trust must remain `trust=client-supplied`.
    3. Type safety: Client fields can arrive as arrays (e.g. `MESSAGE_ID: ["fe6faa94..."]`, `EXIT_STATUS: ["9"]`) or numbers (`EXIT_STATUS: 9`). The positive predicate must strictly enforce scalar checks (`type == "string"` or scalar numbers for status 9) and reject array serializations.

### 3.3 S037: Subject-Unit Metadata (`UNIT=` / `USER_UNIT=`) vs Alarm Consequence
- **Upstream Mechanics**:
  - Added in systemd 251, `UNIT=` and `USER_UNIT=` identify the *subject* unit that a manager daemon logs about.
  - In contrast, trusted `_SYSTEMD_UNIT=` / `_SYSTEMD_USER_UNIT=` describe the *emitting process* (PID 1 `init.scope` or `user@1000.service`), which is never the failed subject.
  - In `src/core/unit.c:6333-6342` (`unit_log_failure`), the manager logs `UNIT_RESULT` alongside `UNIT=` (system) or `USER_UNIT=` (user).
- **Policy Contract vs Evidence**:
  - *Contract Rule*: "Existing info owner partition remains aggregate-only unavailable. OOM fires once if ANY independently valid positive OOM record exists."
  - *Connection*:
    - Subject metadata (`UNIT=` / `USER_UNIT=`) is strictly utilized for the fleet-vs-non-fleet routing partition (`UNIT_FAILURE_JOURNAL` vs `UNIT_FAILURE_OUT_OF_SCOPE`). That partition is aggregate-only; if any record in the stream is invalid or has ambiguous subject fields, the partition becomes `unavailable:record-invalid` / `unavailable:subject-metadata-unknown`.
    - In stark contrast, `positive_unit_oom` and `positive_unit_signal` **do not gate on subject metadata validity**. As proven in `corpus/knowledge/journal-alarm-routing-r14.md:86-89` and `PROVINCE.md:24`, a unit failure resulting from `oom-kill` represents an OOM alarm regardless of whether `UNIT=` is present, absent, ambiguous, or malformed.
    - Thus, subject metadata validity must be completely decoupled from the positive OOM/signal evaluation.

### 3.4 S038: Systemd Service Result Vocabulary (`src/core/service.c:6588-6602`)
- **Upstream Mechanics**:
  - `src/core/service.c` explicitly defines `service_result_table`, mapping `SERVICE_FAILURE_OOM_KILL` to the exact string `"oom-kill"` and `SERVICE_FAILURE_SIGNAL` to `"signal"`.
- **Policy Contract vs Evidence**:
  - *Contract Rule*: "unit result exact string oom-kill/signal; process exact killed and scalar status 9."
  - *Connection*:
    - The string must match `"oom-kill"` exactly. Non-string types (arrays `["oom-kill"]`, null, objects) or case variations (`"OOM-KILL"`) must evaluate to negative (or unknown), never positive evidence.
    - `UNIT_RESULT=oom-kill` represents a unit consequence notice, not an authenticated kernel victim count. It triggers the global `OOM_KILL_JOURNAL` alarm once without adding to raw victim totals.

---

## 4. Cross-Proposal Synthesis & Second-Order Effects

Review of sibling reports reveals critical tensions across runtime, contract, substrate, and verification surfaces:

### 4.1 Tension 1: Where Positive Extraction Hooks into `journal_query`
- **Proposal A (Single-Pass Multiplexed Tail)**:
  `ReviewRouting.md` proposes modifying `JOURNAL_JQ_TAIL` / `JOURNAL_JQ_UNITS` so that on the invalid branch (`else`), jq emits `<status>\t<positive_columns>`.
  - *Risk*: Highly brittle. `journal_query` relies on strict tab-delimited vector widths (`JOURNAL_Q_WIDTH=15` for units, 3 for message ID). Multiplexing status strings with positive columns over variable-width vectors breaks existing parsing and requires rewriting the error handling for all 6 classes.
- **Proposal B (Decoupled Pre-Return Secondary Pass)**:
  `ReviewKernelPredicate.md` and `ReviewProcessPredicate.md` propose inserting an autonomous positive extraction filter inside `journal_query` on `$raw` right after `CAP_RC==0` and `err_bytes==0`, before the `case "$parsed"` early return.
  - *Advantage*: Completely preserves the existing raw aggregate vectors and early-return status strings (`record-invalid`, `multi-boot`, `boot-mismatch`) byte-identical to Round 14, while reliably populating `JQ_POS_*` variables.

### 4.2 Tension 2: Preservation of `paths=` on Positive-Only Alarm Firing
- In `tools/mori-census.sh:1316-1329`, the finding `OOM_KILL_JOURNAL` builds `paths=` from boolean flags `oom_path_k` and `oom_path_u`.
- Currently, those flags are set **only when the raw aggregate count is numeric and > 0**.
- If a positive OOM record fires while the aggregate is `unavailable:record-invalid`, failing to set `oom_path_k` / `oom_path_u` leaves `paths=` completely empty (`paths=`)!
- Existing verifier regexes (`:3036`, `:3068`) and downstream consumers mandate `paths=kernel_oom_notice` or `paths=unit_result_oom_kill`.
- **Second-Order Requirement**: `oom_path_k` must be set if `positive_kernel_oom > 0` (or raw `ko > 0`), and `oom_path_u` must be set if `positive_unit_oom > 0` (or raw `uo > 0`). The path vocabulary must remain canonical.

### 4.3 Tension 3: Collision with Round-14 Regression Test Pin (`R14_SEC_DUP_MSGID_MIXED`)
- `ReviewRawTotals.md` uncovered a direct test conflict:
  In `tools/mori-round14-regressions.py:1552-1564`, test `R14_SEC_DUP_MSGID_MIXED` tests a stream containing one valid OOM record plus one duplicate-array MESSAGE_ID record.
  In Round 14, this test explicitly expected `forbid_ids=FORBID_OOM` (verifying that the OOM alarm was suppressed when the stream had duplicate MESSAGE_IDs).
- Under Round 15 Claim C1, this exact stream **must now fire `OOM_KILL_JOURNAL`** because the valid current-boot record is preserved!
- **Second-Order Requirement**: This is an intentional behavioral improvement of C1. L1 must re-pin `R14_SEC_DUP_MSGID_MIXED` in `tools/mori-round14-regressions.py` during post-integration acceptance so that it expects `OOM_KILL_JOURNAL` while asserting `kernel_oom_notice=unavailable:record-invalid`.

### 4.4 Tension 4: Drift Detection & Volatile Counter Keys
- `ReviewRouting.md:39-42` notes that adding new counter keys to `DRIFT_COUNTER_KEYS` (`tools/mori-census.sh:2272`) alters `volatile_fields`, which causes `--drift` against `baseline-r10-20261015T2231Z.json` to fail with `MORI_DRIFT: volatile_fields`.
- **Second-Order Requirement**: Positive evidence tokens must be emitted in finding metadata (`positive_kernel_oom=...`, `positive_unit_oom=...`) and appended to the surface info string without modifying `DRIFT_COUNTER_KEYS`, unless L1 authorizes an explicit baseline re-pin.

---

## 5. The Proposed Move: Decoupled Dual-Channel Extraction with Path-Preserving Alarm Activation

### 5.1 Proposed Architectural Move
Synthesizing the primary source authorities (S014, S015, S037, S038) and resolving the tensions above, the recommended move consists of three synchronized elements:

1. **Autonomous Positive Extraction within `journal_query`**:
   Execute a lightweight, scalar-guarded positive extraction pass on `$raw` inside `journal_query` immediately after `CAP_RC==0` and `err_bytes==0` (line 1100), prior to the aggregate status evaluation at line 1103.
   - For `kernel_oom_notice`: extract count of records matching scalar `_BOOT_ID == $boot` and scalar `MESSAGE_ID == $id`.
   - For `unit_failure_record`: extract two counts from the same stream:
     - `positive_unit_oom`: `(.UNIT_RESULT? | type) == "string" and .UNIT_RESULT == "oom-kill"`
     - `positive_unit_signal`: `(.UNIT_RESULT? | type) == "string" and .UNIT_RESULT == "signal"`
     *(Both strictly ignore subject `UNIT`/`USER_UNIT` metadata, per S037/S038).*
   - For `unit_sigkill_record`: extract count of records matching scalar `_BOOT_ID == $boot`, scalar `MESSAGE_ID == $id`, `EXIT_CODE == "killed"`, and scalar `EXIT_STATUS` (`string "9"` or `number 9`).
   - On capture error (timeout, rc != 0) or unparseable JSON, assign `positive_*="unavailable:<reason>"`.
   - On empty stream (`[]`), assign `positive_*=0` (the only valid zero).

2. **Decoupled Path-Preserving Alarm Activation**:
   - In `probe_journal` OOM alarm block (`:1303-1332`):
     - `oom_fire` is activated if `ko > 0` OR `uo > 0` OR `positive_kernel_oom > 0` OR `positive_unit_oom > 0`.
     - `oom_path_k=1` is set if `ko > 0` OR `positive_kernel_oom > 0`.
     - `oom_path_u=1` is set if `uo > 0` OR `positive_unit_oom > 0`.
     - `paths=` retains the exact canonical tokens (`kernel_oom_notice`, `unit_result_oom_kill`).
     - Finding metadata appends `positive_kernel_oom=` and `positive_unit_oom=` per scope.
   - In user `KILL_SIGNAL_JOURNAL` warn block (`:1340-1354`):
     - `kill_fire` is activated if `ps > 0` OR `us > 0` OR `positive_process_sigkill > 0` OR `positive_unit_signal > 0`.
     - `kill_paths` similarly preserves canonical paths (`process_sigkill`, `unit_result_signal`).

3. **Untouched Raw Aggregates & Routing Partition**:
   - Every raw aggregate token (`kernel_oom_notice`, `unit_failure_record`, `unit_fleet`, `unit_nonfleet`, `unit_unknown`) remains strictly `unavailable:<reason>` when the stream contains invalid records. No raw total is fabricated or salvaged.
   - The info-level failed unit routing partition (`UNIT_FAILURE_JOURNAL`, `UNIT_FAILURE_OUT_OF_SCOPE`) remains aggregate-only unavailable.

---

## 6. Risks, Contradictions & Tradeoffs

1. **Non-JSON Stream Failure (Parse Boundary)**:
   - If a stream contains a completely truncated or non-JSON byte sequence (e.g. broken line mid-stream), `jq -s` fails (`malformed-json`). Under the round-15 contract, mori explicitly DOES NOT repair arbitrary malformed JSON. Both raw counts and positive tokens must become `unavailable:malformed-json`. This is an accepted boundary condition.
2. **Client-Supplied Spoofability (S015 Trust Boundary)**:
   - Because `MESSAGE_ID` and `UNIT_RESULT` are client-supplied fields (S015), any unprivileged user process can inject records bearing these values.
   - *Mitigation*: The finding line explicitly retains `trust=client-supplied`. Positive evidence demonstrates the presence of matching records in the journal; it is not claimed to be an authenticated kernel verdict.
3. **Downstream Gate Re-pin Requirement**:
   - As noted in Section 4.3, `tools/mori-round14-regressions.py` case `R14_SEC_DUP_MSGID_MIXED` will fail if not updated, because it previously asserted that mixed duplicate-MESSAGE_ID streams suppressed the OOM alarm. L1 must coordinate this re-pin.

---

## 7. Concrete Verification & Checks for L1

The leaf member performs no test execution. The main agent / L1 planner should verify the integrated changes using the following sequence:

1. **Selftest Suite**:
   ```sh
   bash tools/mori-census.sh --selftest
   ```
   *Expected*: Passes all test cases, including new mixed-stream positive preservation cases, exit 0.
2. **Live Read-Only Run**:
   ```sh
   bash tools/mori-census.sh
   ```
   *Expected*: Produces a clean or drift roll without syntax errors or unhandled jq exceptions; exit code matches finding severity (0 CLEAN / 1 DRIFT).
3. **Round-14 Regression Gate Re-pin & Check**:
   ```sh
   python3 tools/mori-round14-regressions.py --selftest
   python3 tools/mori-round14-regressions.py --output /tmp/mori-r14-check
   ```
   *Expected*: `R14_SEC_DUP_MSGID_MIXED` re-pinned to expect `OOM_KILL_JOURNAL` while asserting `kernel_oom_notice=unavailable:record-invalid`; entire suite passes exit 0.
4. **Silence Oracle Parity**:
   ```sh
   bash tools/mori-silence-cases.sh
   ```
   *Expected*: `MORI_SILENCE_CASES: matched=28 total=28`, exit 0.

---

## 8. Tooling & Environment Record

- **Parent Host-Safety Notice**: Received and observed. Sync DB is ~413 packages ahead. `pacman -Sp` dry-run gate required prior to any installation; `-Sy/-Syu/-U/-R` strictly prohibited.
- **Tools Installed / Updated**: **None**. This review was conducted strictly through read-only static analysis using pre-installed system tools (`grep`, `jq`, `read`). No changes were made to system packages or python environments.
