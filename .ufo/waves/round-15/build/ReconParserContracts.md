# ReconParserContracts: jq Manual and Valid JSON Semantics for C1 (Round 15)

Seat: `ReconParserContracts` (role: `scout`, axis: `coverage`, milestone: "retain validated positives without fabricated totals").
Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scope: Read-only research of official `jq` manual (`all`, `select`, `type`, `--slurp`), JSON stream parsing semantics, systemd primary sources (S014, S015, S037, S038), scope boundaries, and concrete counterexample for C1.
Verification notice: No code edits, no test/gate execution, no builds, lints, or smoke runs. Only report write.

---

## 1. Godspeed Posture & Axes
- **Axes**: Coverage (judged; preserve critical OOM and user signal alarms from individually valid current-boot records) vs Operability (constraint; maintain honesty, no fabricated totals, raw counts stay unavailable when invalid, no new journal queries or actuations).
- **Frontier walk**: Differentiate universal aggregate validation (`all`) from independent per-record evidence extraction (`select`), allowing positive alarm triggers to survive adjacent malformed/foreign-boot records while keeping raw aggregate counts unavailable.

---

## 2. Primary Sources: jq Official Manual

Source: `jq(1)` official manual (local: `/usr/share/man/man1/jq.1.gz`, verified on host package `jq 1.8.2-1`; online canonical reference: https://jqlang.github.io/jq/manual/).

### A. `--slurp` / `-s` (Stream Invocation)
- **Exact Anchor**: `man jq`, section "Invocation Options", entry `--slurp / -s:` (lines 102–106).
- **Quote (<=25 words)**:
  > "read the entire input stream into a large array and run the filter just once." (15 words)
- **JSON Semantics**:
  - `jq` consumes standard input as a sequence of whitespace-delimited JSON texts (RFC 8259).
  - When `--slurp` (`-s`) is given, all valid JSON texts in the stream are parsed and assembled into a single top-level JSON array `.` passed to the filter.
  - **Syntax Error / Parsing Failure**: If any byte sequence in the stream is syntactically invalid JSON (e.g. truncated JSON object, unclosed string/bracket, or non-JSON text from stderr leakage), `jq` immediately aborts parsing with exit code 5 (syntax error) and writes an error message to stderr.
  - **Empty Input Stream**: If the input stream contains 0 bytes (empty stream), `jq -s` parses zero JSON texts and produces `[]` (an empty array) at exit code 0.

### B. `all`, `all(condition)`, `all(generator; condition)` (Universal Quantification)
- **Exact Anchor**: `man jq`, section "Builtin operators and functions", entry `all, all(condition), all(generator; condition)` (lines 1175–1185).
- **Quotes (<=25 words)**:
  > "The all(generator; condition) form applies the given condition to all the outputs of the given generator." (16 words)
  > "If the input is an empty array, all returns true." (10 words)
- **Semantics**:
  - Evaluates universal quantification over the generator outputs.
  - Returns `true` if and only if the condition evaluates to truthy for *every single item* generated.
  - If a single element evaluates to `false` or `null`, `all` immediately evaluates to `false`.

### C. `select(boolean_expression)` (Per-Item Filter)
- **Exact Anchor**: `man jq`, section "Builtin operators and functions", entry `select(boolean_expression)` (lines 1039–1045).
- **Quote (<=25 words)**:
  > "The function select(f) produces its input unchanged if f returns true for that input, and produces no output otherwise." (19 words)
- **Semantics**:
  - Filters a stream or array comprehension element-by-element.
  - If `f` returns `true` for an element, that element is passed downstream unchanged; if `f` returns `false` or `null`, that element produces no output.
  - Crucially: An invalid or non-matching sibling element produces zero outputs, but does NOT terminate evaluation or alter/suppress valid outputs from other elements.

### D. `type` (Strict Type Guarding)
- **Exact Anchor**: `man jq`, section "Builtin operators and functions", entry `type` (lines 1301–1304).
- **Quote (<=25 words)**:
  > "The type function returns the type of its argument as a string, which is one of null, boolean, number, string, array or object." (23 words)
- **Semantics**:
  - Returns the JSON type as a string primitive.
  - In `jq`, field lookups on non-objects can produce errors unless guarded or using optional traversal (`.?`).
  - Checking `type == "object"` ensures safe field access.
  - Checking `(._BOOT_ID | type) == "string"` and `(.MESSAGE_ID | type) == "string"` ensures scalar comparison and prevents arrays (which journalctl emits for duplicated fields) from accidental coercion or unexpected truthiness.

---

## 3. Systemd Primary Sources (S014, S015, S037, S038)

- **S014 (`journalctl(1)`)**:
  - **Anchor**: Output Options `-o json` (:209, :215), `--output-fields=` (:230).
  - **Quote (<=25 words)**:
    > "formats entries as JSON objects, separated by newline characters" ... "if a non-unique field is encountered a JSON array is used as field value". (24 words)
  - **Implication**: Journal JSON streams consist of discrete JSON objects per line. Multi-valued fields serialize as JSON arrays rather than strings.
- **S015 (`systemd.journal-fields(7)`)**:
  - **Anchor**: User Journal Fields `MESSAGE_ID=` (:40-42); Trusted Journal Fields `_BOOT_ID=` (:100), `_TRANSPORT=` (:106).
  - **Quote (<=25 words)**:
    > "Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly added by the journal and cannot be altered by client code." (24 words)
- **S037 (`systemd.journal-fields(7)`)**:
  - **Anchor**: User Journal Fields `UNIT=`, `USER_UNIT=`.
  - **Quote (<=25 words)**:
    > "Used by the system and user managers when logging about specific units." (12 words)
- **S038 (`src/core/service.c`)**:
  - **Anchor**: `service_result_table` (:6598).
  - **Quote (<=25 words)**:
    > `[SERVICE_FAILURE_OOM_KILL] = "oom-kill",` (3 words)

---

## 4. Scope Boundaries for C1

1. **Syntactic JSON / Capture Failure Boundary**:
   - `jq -s` parses the whole stream. If the stream contains non-JSON text, truncated JSON, nonzero journalctl exit status (`rc-N`), timeout (`124`/`137`), or nonempty stderr, parsing fails.
   - Boundary: Positive evidence tokens (`positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`) must evaluate to `unavailable:<reason>` (e.g. `unavailable:malformed-json`, `unavailable:stderr-nonempty`). They must NEVER be treated as a valid numeric 0.
   - C1 does NOT claim to repair syntactically broken JSON.

2. **Valid Empty Stream Boundary**:
   - If a query succeeds with `rc=0`, zero stderr bytes, and empty stdout, `jq -s` evaluates `[]`.
   - Boundary: In an empty stream, `[ .[] | select(...) ] | length` evaluates to `0`. This is the ONLY valid numeric 0.

3. **Whole-Class Aggregate Boundary (`all`)**:
   - Current aggregate classification uses `all(.[]; predicate)`.
   - If an adjacent record has a foreign boot ID, an array boot ID, or a nonmatching MESSAGE_ID, `all` returns `false`, sending the aggregate to `boot-mismatch`, `multi-boot`, or `record-invalid`.
   - Boundary: Raw aggregate counts (`total`, `boots`, `boot`, `ucnt[...]`) STAY `unavailable:<reason>`. C1 explicitly preserves aggregate unreachability to prevent fabricating un-audited totals.

4. **Independent Positive Evidence Boundary (`select` + `type`)**:
   - Instead of universal quantification (`all`), positive evidence uses existential aggregation over `select(...)`:
     ```jq
     [ .[] | select(
         type == "object"
         and ((._BOOT_ID | type) == "string") and ._BOOT_ID == $boot
         and ((.MESSAGE_ID | type) == "string") and .MESSAGE_ID == $id
         <class-specific exact predicates>
     ) ] | length
     ```
   - Boundary: Each record is evaluated in isolation. A foreign boot or malformed sibling record is dropped by `select` and does not taint or suppress an individually valid current-boot record.

5. **Alarm Actuation Boundary (C1 Target)**:
   - `OOM_KILL_JOURNAL crit` fires if ANY valid positive OOM record exists: `positive_kernel_oom > 0` or `positive_unit_oom > 0` across user or system scope, even if raw counts are `unavailable:<reason>`.
   - User `KILL_SIGNAL_JOURNAL warn` fires if `positive_process_sigkill > 0` or `positive_unit_signal > 0` in user scope.
   - The finding line records the raw tokens as `unavailable:<reason>` while appending positive evidence fields (`positive_kernel_oom=...`).

---

## 5. Counterexample for C1: The Aggregate Blinding Defect

### Input Scenario
A captured system-scope journal stream for `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` (`_BOOT_ID,MESSAGE_ID`) containing two syntactically valid JSON records:
- **Record 1** (valid current-boot kernel OOM notification):
  `{"_BOOT_ID":"11111111111111111111111111111111","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef"}`
- **Record 2** (foreign-boot record retained across journal rotation):
  `{"_BOOT_ID":"22222222222222222222222222222222","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef"}`

Current boot expected: `11111111111111111111111111111111`.

### Trace under Round-14 Aggregate Implementation
1. `CAP_RC=0`, `err_bytes=0`. The stream parses cleanly under `jq -s` into a 2-element array.
2. `tools/mori-census.sh:974` executes `JOURNAL_JQ_MSGID`:
   `if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and (._BOOT_ID == $boot) and (.MESSAGE_ID == $id)) $JOURNAL_JQ_TAIL`
3. Because Record 2 has `._BOOT_ID == "2222..."` (not `$boot`), `all(.[]; ...)` evaluates to `false`.
4. It enters `JOURNAL_JQ_TAIL` else branch (`:973`):
   `([.[]._BOOT_ID] | unique | length) as $b | if $b > 1 then "multi-boot" ...`
   $b equals 2. Filter outputs string `"multi-boot"`.
5. `tools/mori-census.sh:1104` matches `multi-boot` and sets `JQ_STATUS=multi-boot`, leaving `JQ_N=""`.
6. In `probe_journal` (`:1221`), `js["system:kernel_oom_notice"]="multi-boot"`.
7. In OOM alarm block (`:1305`): `ko="unavailable:multi-boot"`.
8. In OOM fire logic (`:1314`): `is_int "$ko"` is false. `oom_fire` is NOT set.
9. Line 1331: `OOM_KILL_JOURNAL crit` DOES NOT FIRE. DRIFT is NOT reported.
10. **Defect**: A real kernel OOM kill in the current boot was silenced because an older boot's record was present in the journal.

### Resolution under C1 Specification
1. The stream is parsed once with `jq -s` (`jrc=0`).
2. Raw aggregate classification continues to evaluate `all(.[]; ...)` -> emits `multi-boot`. Raw token `system_notice=unavailable:multi-boot` is preserved (no fake aggregate total).
3. Positive filter executes on the same parsed stream using `select`:
   - Record 1: matches `type == "object" and ._BOOT_ID == "1111..." and .MESSAGE_ID == "fe6faa94..."` -> retained.
   - Record 2: does not match current boot -> dropped.
   - Count of matched elements: `1`.
   - `positive_kernel_oom` is set to `1`.
4. OOM alarm block detects `positive_kernel_oom > 0`:
   - `oom_fire=1` is set.
   - `oom_paths` includes `kernel_oom_notice`.
   - Single finding `OOM_KILL_JOURNAL crit` fires once, containing evidence:
     `system_notice=unavailable:multi-boot system_positive_kernel_oom=1`
5. **Outcome**: The critical alarm is restored and preserved, while raw aggregate counters truthfully remain unavailable.

---

## 6. Tooling & Host Safety Record
- **Tools installed/updated**: None.
- **Host Safety Directive**: Followed strictly. Read-only inspection of host binaries (`jq`, `man`) was performed; no package managers, services, or system files were modified.

Report completed. Scoped findings committed to `.ufo/waves/round-15/build/ReconParserContracts.md`.
