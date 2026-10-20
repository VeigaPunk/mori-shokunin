# ReconFieldTypes — S015 Field Duplicate Values Arrays and Binary Encodings

**Seat**: `MoriR15.ReconFieldTypes` (scout, leaf)  
**Lane Root**: `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Judged Axis**: `coverage`  
**Milestone**: retain validated positives without fabricated totals  
**Report Target**: `.ufo/waves/round-15/build/ReconFieldTypes.md`

---

## 1. Godspeed Posture & Axis Declaration

1. **Name the axes**:
   - **Coverage (Primary / Judged)**: Preserving critical OOM (`OOM_KILL_JOURNAL crit`) and user signal alarms (`KILL_SIGNAL_JOURNAL warn`) from individually valid, current-boot structured records even when adjacent records have duplicate-field arrays, binary encodings, or invalid metadata.
   - **Operability (Constraint / Harm None)**: Aggregate class totals stay strictly `unavailable` (`record-invalid`) when invalid; no fabricated totals, no false-zero interpretations, and no new journal queries or stream re-execution.
   - **Depth & Calibration**: Grounded directly in primary documentation S015 (`systemd.journal-fields(7)`) and S014 (`journalctl(1)`), separating scalar string specifications from permissive journal serialization.

2. **Iterate cheap, in parallel**:
   - Researched local systemd 261 man pages and upstream systemd 262 documentation for S015 and S014. Evaluated jq parser behavior against JSON array representations without running test suites or mutating production code.

3. **Keep moves that improve any axis and harm none**:
   - Establishing strict per-record scalar string type guards (`(._BOOT_ID | type) == "string"` and `(.MESSAGE_ID | type) == "string"`) for positive evidence tokens while maintaining class-level fail-closed `unavailable:record-invalid` aggregate status.

4. **Don't aim — let the frontier walk itself**:
   - Truthfully exposing that `systemd-journald` permits non-unique fields and arbitrary binary bytes on user fields, which `journalctl -o json` serializes as JSON arrays, explaining why all-or-nothing stream validation collapsed aggregate classes and suppressed alarms.

---

## 2. Primary Sources & Exact Anchors

### 2.1 S015: `systemd.journal-fields(7)` — Special Journal Fields
- **Source Registry ID**: `S015` (`corpus/SOURCES.md:21`)
- **Canonical Upstream URL**: `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html`
- **Host Manual**: `man 7 systemd.journal-fields` (systemd 261 / 262)

#### Anchor 1: Section `DESCRIPTION` — Binary Data and Non-Unique Field Names
- **Location**: Section `DESCRIPTION`, paragraphs 1–2
- **Source Text**:
  > *"Entries in the journal (as written by systemd-journald.service(8)) resemble a UNIX process environment block in syntax but with field values that may include binary data, and with non-unique field names permitted. Primarily, field values are formatted UTF-8 text strings —— binary encoding is used only where formatting as UTF-8 text strings makes little sense."*
- **Exact Quote 1** (14 words, $\le 25$ words):
  > *"with field values that may include binary data, and with non-unique field names permitted."*
- **Exact Quote 2** (14 words, $\le 25$ words):
  > *"binary encoding is used only where formatting as UTF-8 text strings makes little sense."*

#### Anchor 2: Section `DESCRIPTION` — Logging Subsystem Uniqueness Policy
- **Location**: Section `DESCRIPTION`, paragraph 2
- **Source Text**:
  > *"Even though the logging subsystem makes no restrictions on which fields to accept non-unique values for, it is strongly recommended to avoid relying on this for the fields listed below (except where listed otherwise, as mentioned) in order to avoid unnecessary incompatibilities with other applications."*
- **Exact Quote 3** (24 words, $\le 25$ words):
  > *"Even though the logging subsystem makes no restrictions on which fields to accept non-unique values for, it is strongly recommended to avoid relying on this"*

#### Anchor 3: Section `USER JOURNAL FIELDS > MESSAGE=` — Multiple Values Prohibition
- **Location**: Section `USER JOURNAL FIELDS`, subsection `MESSAGE=`
- **Source Text**:
  > *"Do not add multiple values of this field type to the same entry (also see above), as consuming applications generally do not expect this and are unlikely to show all values in that case."*
- **Exact Quote 4** (20 words, $\le 25$ words):
  > *"Do not add multiple values of this field type to the same entry... as consuming applications generally do not expect this"*

#### Anchor 4: Section `USER JOURNAL FIELDS > MESSAGE_ID=` — Scalar 128-bit Hex String Specification
- **Location**: Section `USER JOURNAL FIELDS`, subsection `MESSAGE_ID=`
- **Source Text**:
  > *"A 128-bit message identifier ID for recognizing certain message types, if this is desirable. This should contain a 128-bit ID formatted as a lower-case hexadecimal string, without any separating dashes or suchlike."*
- **Exact Quote 5** (18 words, $\le 25$ words):
  > *"This should contain a 128-bit ID formatted as a lower-case hexadecimal string, without any separating dashes or suchlike."*

#### Anchor 5: Section `TRUSTED JOURNAL FIELDS > _UDEV_DEVLINK=` — Explicit Multi-Occurrence Exception
- **Location**: Section `TRUSTED JOURNAL FIELDS`, subsection `_UDEV_DEVLINK=`
- **Source Text**:
  > *"Additional symlink names pointing to the device node in /dev/. This field is frequently set more than once per entry."*
- **Exact Quote 6** (10 words, $\le 25$ words):
  > *"This field is frequently set more than once per entry."*

---

### 2.2 S014: `journalctl(1)` — JSON Array Serialization Mechanics
- **Source Registry ID**: `S014` (`corpus/SOURCES.md:20`)
- **Canonical Upstream URL**: `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html`
- **Host Manual**: `man 1 journalctl` (systemd 261 / 262)

#### Anchor 1: Section `OUTPUT OPTIONS > -o json` (Rule 2) — Duplicate Field Serialization as JSON Array of Strings
- **Location**: Section `OUTPUT OPTIONS`, item `json`, rule 2
- **Source Text**:
  > *"Journal entries permit non-unique fields within the same log entry. JSON does not allow non-unique fields within objects. Due to this, if a non-unique field is encountered a JSON array is used as field value, listing all field values as elements."*
- **Exact Quote 7** (20 words, $\le 25$ words):
  > *"if a non-unique field is encountered a JSON array is used as field value, listing all field values as elements."*

#### Anchor 2: Section `OUTPUT OPTIONS > -o json` (Rule 3) — Binary Field Serialization as JSON Array of Numbers
- **Location**: Section `OUTPUT OPTIONS`, item `json`, rule 3
- **Source Text**:
  > *"Fields containing non-printable or non-UTF8 bytes are encoded as arrays containing the raw bytes individually formatted as unsigned numbers."*
- **Exact Quote 8** (19 words, $\le 25$ words):
  > *"Fields containing non-printable or non-UTF8 bytes are encoded as arrays containing the raw bytes individually formatted as unsigned numbers."*

#### Anchor 3: Section `OUTPUT OPTIONS > -o json` (Rule 1) — Oversized Field Serialization as Null
- **Location**: Section `OUTPUT OPTIONS`, item `json`, rule 1
- **Source Text**:
  > *"Fields larger than 4096 bytes are encoded as null values. (This may be turned off by passing --all...)"*
- **Exact Quote 9** (10 words, $\le 25$ words):
  > *"Fields larger than 4096 bytes are encoded as null values."*

---

## 3. Scope Boundaries & Field Type Semantics

### 3.1 Upstream Journal Storage vs. Permissive Ingestion
1. **Journal Ingestion Layer (`systemd-journald`)**:
   - `systemd-journald` ingests structured fields over native Unix sockets (`sd_journal_sendv`).
   - The logging subsystem enforces **no uniqueness restrictions** on field names across entries. Any client can submit multiple instances of the same field name within a single datagram.
   - The logging subsystem accepts arbitrary binary data in field values. While field values are primarily UTF-8 text strings, binary encoding is permitted for any user field.
2. **Metadata Contract**:
   - `MESSAGE_ID` is documented as a 128-bit lowercase hexadecimal string (32 ASCII hex chars).
   - `_BOOT_ID` is a 128-bit kernel boot identifier (32 ASCII hex chars).
   - `UNIT_RESULT` is an enum string (`"oom-kill"`, `"signal"`, `"timeout"`, etc.).
   - `EXIT_CODE` is a process termination code string (`"killed"`, `"exited"`).
   - `EXIT_STATUS` is a numeric exit status / signal ordinal (string or integer `"9"`).
3. **Trust & Spoofability Boundary**:
   - Fields without leading underscore (including `MESSAGE_ID`, `UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS`) are client-supplied **User Journal Fields**. They carry unauthenticated source trust (`trust=client-supplied`).
   - A client process can intentionally or unintentionally send duplicate `MESSAGE_ID` fields or non-UTF-8 payloads.
   - Trusted underscore fields (`_BOOT_ID`, `_TRANSPORT`, `_UID`, `_PID`) are attached by the kernel or daemon, but corrupted data or synthesized test streams can also exhibit non-scalar encodings.

### 3.2 Downstream Serialization in `journalctl -o json`
When `journalctl -o json` outputs entries:
1. **Scalar String Representation (Standard)**:
   - A single, valid UTF-8 string $\le 4096$ bytes serializes as `"FIELD_NAME": "string_value"`.
2. **JSON Array of Strings (Duplicate Field Names)**:
   - If an entry contains two or more `MESSAGE_ID` fields (e.g. `MESSAGE_ID=fe6f...` and `MESSAGE_ID=fe6f...`), `journalctl` serializes:
     `"MESSAGE_ID": ["fe6faa94e7774663a0da52717891d8ef", "fe6faa94e7774663a0da52717891d8ef"]`
3. **JSON Array of Unsigned Numbers (Binary / Non-UTF-8 Bytes)**:
   - If a field contains binary or non-printable bytes (e.g. raw memory dump, unescaped ANSI escapes, or raw byte sequence), `journalctl` serializes:
     `"MESSAGE_ID": [102, 101, 54, 102, 97, 97, 57, 52, ...]` (raw bytes as `0..255` integers).
4. **JSON Null (Oversized Payloads)**:
   - If a field value exceeds 4096 bytes without `--all`, it serializes as `"FIELD_NAME": null`.

### 3.3 Consumer & Parser Invariants (`jq` / `jaq`)
1. **Scalar Equality Fails on Arrays**:
   - In jq, `["fe6faa94e7774663a0da52717891d8ef"] == "fe6faa94e7774663a0da52717891d8ef"` evaluates to `false`.
   - In jq, `[102, 101, ...] == "fe6faa94e7774663a0da52717891d8ef"` evaluates to `false`.
2. **Type Discrepancy**:
   - `(.MESSAGE_ID | type)` for a duplicate field or binary field returns `"array"`, not `"string"`.
   - `(._BOOT_ID | type)` for duplicate boot IDs returns `"array"`, not `"string"`.
3. **Strict Validation Invariant for Positive Evidence**:
   - To prevent malformed arrays, binary dumps, or injected collections from being misidentified or causing type errors, positive evidence predicates **must enforce scalar string types**:
     - `(._BOOT_ID | type) == "string" and ._BOOT_ID == $boot`
     - `(.MESSAGE_ID | type) == "string" and .MESSAGE_ID == $id`
     - For unit OOM: `(.UNIT_RESULT? | type) == "string" and .UNIT_RESULT == "oom-kill"`
     - For unit signal: `(.UNIT_RESULT? | type) == "string" and .UNIT_RESULT == "signal"`
     - For process sigkill: `(.EXIT_CODE? | type) == "string" and .EXIT_CODE == "killed" and ((.EXIT_STATUS? | tostring) == "9")`
   - Any record with an array-valued `MESSAGE_ID`, array-valued `_BOOT_ID`, or binary byte array is **strictly excluded** from positive evidence counts.

---

## 4. Counterexample for Claim C1 (Coverage)

### 4.1 Concrete Scenario: Valid Positive Witness Suppressed by Duplicate/Binary Array
Consider a journal output stream from `journalctl --system -b -o json --output-fields=_BOOT_ID,MESSAGE_ID MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` containing two entries for the current boot (`11111111111111111111111111111111`):

- **Record 1 (Legitimate Kernel OOM Notice)**:
  A genuine kernel OOM notice logged by systemd:
  ```json
  {
    "_BOOT_ID": "11111111111111111111111111111111",
    "MESSAGE_ID": "fe6faa94e7774663a0da52717891d8ef"
  }
  ```
- **Record 2 (Adjacent Entry with Duplicate Field or Binary Encoding)**:
  An adjacent entry emitted by a misconfigured or adversarial client that supplied duplicate `MESSAGE_ID` fields or non-printable binary data, serialized by `journalctl -o json` as an array:
  ```json
  {
    "_BOOT_ID": "11111111111111111111111111111111",
    "MESSAGE_ID": [
      "fe6faa94e7774663a0da52717891d8ef",
      "extra_unvalidated_identifier"
    ]
  }
  ```
  *(Alternative Record 2 with binary encoding: `{"_BOOT_ID": "11111111111111111111111111111111", "MESSAGE_ID": [102, 101, 54, 102]}`)*

### 4.2 Defect in Round 14 Baseline (False Clean / Alarm Suppression)
1. **Aggregate Query Execution**:
   In Round 14 (`tools/mori-census.sh:974, 973`), `journal_query` evaluated the entire stream with `JOURNAL_JQ_MSGID`:
   ```jq
   if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and (._BOOT_ID == $boot) and (.MESSAGE_ID == $id))
   then [length, ([.[]._BOOT_ID] | unique | length), ([.[]._BOOT_ID][0] // "none")] | @tsv
   else (if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and ((._BOOT_ID | length) > 0))
         then ([.[]._BOOT_ID] | unique | length) as $b | if $b > 1 then "multi-boot" elif all(.[]; ._BOOT_ID == $boot) then "record-invalid" else "boot-mismatch" end
         else "record-invalid" end) end
   ```
2. **Outcome on Stream**:
   - For Record 2, `.MESSAGE_ID == $id` is `false` (array does not equal scalar string).
   - Therefore, `all(.[]; ...)` across the slurped array evaluates to `false`.
   - The filter falls into the error branch: since `._BOOT_ID` is valid current boot, it outputs `"record-invalid"`.
   - `journal_query` sets `JQ_STATUS=record-invalid` and `JQ_N=""`.
3. **Alarm Evaluation Suppression**:
   - In `probe_journal` (`tools/mori-census.sh:1305, 1314`):
     ```bash
     ko=${jn[system:kernel_oom_notice]}  # evaluates to empty string
     # ...
     if [ -n "$ko" ] && [ "$ko" -gt 0 ]; then oom_fire=1; fi
     ```
   - Since `ko` is not an integer `> 0`, `oom_fire` remains `0`.
   - **Severe Coverage Failure**: An actual, verified kernel OOM kill (Record 1) occurred on the system, but the critical alert `OOM_KILL_JOURNAL crit => DRIFT` **failed to fire**. The system reported false clean / no alarm because an adjacent record contained a duplicate field array.

### 4.3 Claim C1 Resolution in Round 15
1. **Separation of Aggregate Completeness and Positive Evidence**:
   - The raw aggregate class `kernel_oom_notice` remains `unavailable:record-invalid`. This is honest: the aggregate count cannot be certified as complete.
   - A per-record positive evidence filter processes the captured stream without re-querying `journalctl`.
2. **Independent Per-Record Evaluation**:
   - Record 1:
     - `type == "object"`: `true`
     - `(._BOOT_ID | type) == "string" and ._BOOT_ID == $boot`: `true`
     - `(.MESSAGE_ID | type) == "string" and .MESSAGE_ID == $id`: `true`
     - Evaluates as **1 validated positive witness**.
   - Record 2:
     - `(.MESSAGE_ID | type) == "string"`: `false` (type is `"array"`).
     - Excluded from positive evidence count (count does not increment).
     - Not treated as a numeric zero total.
3. **Alarm Triggering**:
   - `positive_kernel_oom` is emitted as `1`.
   - The OOM alarm predicate checks:
     `if [ "$positive_kernel_oom" -gt 0 ]; then oom_fire=1; fi`
   - `oom_fire` is set to `1`, and `OOM_KILL_JOURNAL crit` fires.
4. **Milestone Achieved**:
   - **Retain validated positives without fabricated totals**:
     - The real OOM event triggers the alarm (coverage improved).
     - The aggregate count is not fabricated as `1` or `2`; it remains `unavailable` (operability preserved).
     - The array-valued record is rejected without suppressing the valid scalar positive.

---

## 5. Summary Matrix for JQ Parser Implementation

| Representation in JSON Stream | JQ Type | Scalar Match `== $id` | R14 Aggregate Outcome | R15 C1 Positive Evidence Status |
|---|---|---|---|---|
| Scalar ASCII hex string (`"fe6f..."`) | `"string"` | `true` (if matching) | Passes aggregate | **Counted in `positive_*`** |
| Duplicate values array (`["fe6f...", "extra"]`) | `"array"` | `false` | Collapses class to `record-invalid` | **Excluded** (not scalar string) |
| Binary byte array (`[102, 101, 54, ...]`) | `"array"` | `false` | Collapses class to `record-invalid` | **Excluded** (not scalar string) |
| Oversized payload (`null`) | `"null"` | `false` | Collapses class to `record-invalid` | **Excluded** (not scalar string) |
| Foreign boot scalar (`"2222..."`) | `"string"` | N/A (boot mismatch) | Collapses class to `boot-mismatch` | **Excluded** (`._BOOT_ID != $boot`) |
| Duplicate `_BOOT_ID` array (`["111...", "111..."]`) | `"array"` | N/A (type mismatch) | Collapses class to `record-invalid` | **Excluded** (not scalar string) |

---

## 6. Verification and Tooling Receipt

- **Tool Installs / Updates**: None performed.
- **Verification Execution**: None performed (leaf scout research seat; no builds, tests, linters, or live journal queries run).
- **Deliverable**: Findings written to `.ufo/waves/round-15/build/ReconFieldTypes.md`.
