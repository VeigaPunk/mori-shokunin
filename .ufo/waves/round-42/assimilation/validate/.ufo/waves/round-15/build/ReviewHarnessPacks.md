# ReviewHarnessPacks: round-15 fixture pack schema audit (read-only)

Seat: MoriR15.ReviewHarnessPacks (reviewer, leaf). Scope: fixture pack schema, unique ids, literal expected values, and the production anchors the packs will be graded against. No gates, builds, tests or fixture execution were run. No installs were performed; the parent host-safety notice was received and no package operation was needed.

## 1. Current target state (observed)

- `.ufo/waves/round-15/fixtures/` does NOT exist yet. No pack file is present, so no case ids or literals can be audited. Everything below is a schema and anchor audit, not a pack audit.
- `tools/mori-census.sh` has NO `positive_*` token. `grep -rn positive tools/` finds only comments (lines 1301, 3611, 3613, 3658). The production interface named in the assignment is unimplemented. Packs will be literal-expected and will fail until the implementer lands.
- The three MESSAGE_ID literals in the assignment match production exactly, each 32 lowercase hex:
  - kernel `fe6faa94e7774663a0da52717891d8ef` = `JOURNAL_ID_KERNEL_OOM` (`tools/mori-census.sh:966`)
  - unit `d9b373ed55a64feb8242e02dbe79a49c` = `JOURNAL_ID_UNIT_FAILURE` (`:970`)
  - process `98e322203f7a4ed290d09fe03c09fe15` = `JOURNAL_ID_UNIT_SIGKILL` (`:969`)
- Boot fixture `11111111111111111111111111111111` is 32 characters. A foreign boot must be a different 32-hex value, for example `ffffffffffffffffffffffffffffffff`.

## 2. Production anchors the positive tokens must hook into

- `journal_query()` at `tools/mori-census.sh:1046-1136`:
  - stderr and rc gates return early at `:1083-1095`. Positive tokens must default to `unavailable` on these paths, and must not be stored from them.
  - Parsing is ONE `"$JQ_BIN" -s` pass over the whole captured stream at `:1099`. A non-JSON line makes `jrc != 0` and returns `malformed-json` at `:1102`. Positives cannot survive that case.
  - The `case "$parsed"` at `:1103-1105` returns `record-invalid|multi-boot|boot-mismatch` before any count is kept. This is the all-or-nothing behaviour C1 must bypass.
  - Insertion point for the positive pass: after the `jrc` check at `:1101` and before the `case` at `:1103`, running a second `jq -s` over the SAME `$raw` (no new journalctl call). That keeps positives valid when the aggregate is `record-invalid`, and it stays unavailable on capture or parser failure. Store `JQ_POS_*` and reset them at `:1051`.
- The aggregate filters `JOURNAL_JQ_MSGID` (`:974`), `JOURNAL_JQ_SIGKILL` (`:975`) and `JOURNAL_JQ_UNITS` (`:1001-1037`) use `all(.[]; ...)` at `:973`, `:1019` and `:1037`. One bad record grades the whole class `record-invalid`. This is the defect C1 repairs; the positive pass must NOT reuse `all()`.
- The unit class is one pass over the `d9b373ed` record set at `:1201` with `JOURNAL_Q_WIDTH=15`. Keep the 15-column contract unchanged. Compute positive unit OOM and signal in the separate pass, not as added columns.
- `probe_journal` loop at `:1187-1230`: positives must be read per scope (`--user`, `--system`) and must not be summed.
- Existing selftest fixture at `tools/mori-census.sh:3008` writes `"MESSAGE":"MORI_JOURNAL_CANARY"` into records. New pack records must NOT copy that shape (see F7).

## 3. Findings (severity order)

**F1 HIGH: "malformed" must be defined as semantic invalidity, never non-JSON.**
The schema says `user`/`system` are arrays of records. The `jq -s` at `:1099` fails the WHOLE stream on one non-JSON line, so no positive can be proven from that capture. The assignment claims preservation "even when an adjacent malformed/nonmatching/foreign-boot record invalidates the aggregate class". That is only true for parseable JSON objects with invalid fields. Fix: state in the schema that every record is a JSON object (so `invalid_class` may name only semantic invalidity), and that non-JSON capture is covered by the `malformed-json` class with `want_oom=false` and `want_signal=false`, or is excluded from the packs. Do NOT include a raw non-JSON line in a pack expecting survival.

**F2 HIGH: no field expresses raw-count expectations.**
Assignment milestone is "retain validated positives without fabricated totals". The schema has only `want_oom` and `want_signal`. A pack cannot assert that the raw token (`kernel_oom_notice`, `unit_oom`, `unit_sigkill_record`) stays `unavailable:record-invalid` (not `0`). Fix: add an `expect` object, for example `expect: {user: {raw: {kernel_oom_notice: "unavailable:record-invalid", ...}, positive: {positive_kernel_oom: 1, ...}}, system: {...}}`. Each raw value and positive value is a literal, and a `0` raw literal is forbidden where the class is invalid.

**F3 HIGH: `invalid_class` is an open string.**
Seats will invent names, which defeats coverage counting. Fix: a closed enum, for example `null | message-id-not-scalar | message-id-array | boot-id-missing | boot-id-array | boot-foreign | unit-result-array | unit-result-missing | unit-result-not-string | exit-status-not-9 | exit-code-not-killed | subject-ambiguous | subject-missing`. A case with `invalid_class` non-null must carry at least one record of that class, and `want_*` must be literal.

**F4 MEDIUM: id uniqueness scope is unspecified.**
The harness consumes `.ufo/waves/round-15/fixtures/*.json`, so uniqueness must hold across ALL packs, not per file. Many seats write packs (PackUnitUser, PackUnitSystem, PackNegativeInvalid, PackNegativeResults, PackNegativeStatus, PackCrossScope, PackSubjectUnknown, PackFanoutPositive, KnowledgePositive, and others). Fix: state global uniqueness, and require a seat prefix (for example `pu-`, `pn-`, `px-`). The harness must reject duplicate ids across files, not only within one.

**F5 MEDIUM: stub semantics for non-matching records are undefined.**
journalctl applies `MESSAGE_ID=`/`EXIT_CODE=`/`EXIT_STATUS=` matches server-side. If the stub does the same, a "nonmatching" record never reaches jq and the defence-in-depth filter is never exercised. Fix: the stub must pass the pack records through unfiltered by match, and only apply the `--output-fields` projection. Then a nonmatching record tests the SUT filter. Record this rule in the schema.

**F6 MEDIUM: `want_signal` is user-scope only; no case proves system exclusion.**
Production keeps system signal results as info (`KILL_SIGNAL_JOURNAL_SYSTEM`), and the positive user signal path is user-only. Fix: at least one pack case must have a valid system-only signal or sigkill record with `want_signal=false`. The `want_signal` field must be documented as user-scope only.

**F7 MEDIUM: no `MESSAGE` key and no canary strings.**
Assignment says "No raw MESSAGE or secret canaries". The current census selftest (`:3008`) and the round-14 harness both use MESSAGE canaries. Fix: schema forbids a `MESSAGE` key in any record, and the harness rejects any pack containing `MESSAGE` or any string from the round-14 CANARIES list.

**F8 LOW: EXIT_STATUS "scalar 9" is ambiguous in production.**
`JOURNAL_JQ_SIGKILL` uses `(.EXIT_STATUS | tostring) == "9"` (`:975`). That accepts string `"9"` and number `9`, and rejects `["9"]`, `"9.0"` and `true`. The spec says "scalar status 9". Fix: the schema must state the accepted set. Include one case with number `9` and one with string `"9"` in the process pack, plus one rejected `"9.0"`, so the accepted set is pinned by literal expectation.

**F9 LOW: packs cannot be validated yet.**
Positive tokens do not exist (section 1). Packs are literal-expected and will be red until the implementer lands. The report must not present a pack as green before that.

## 4. Minimal coverage matrix the packs must hit (each as a distinct id)

- positive_kernel_oom: user-only valid kernel notice; system-only valid kernel notice; kernel valid + `MESSAGE_ID` array record (C1 repair, want_oom=true); foreign-boot kernel record ignored, want_oom=false.
- positive_unit_oom: fleet subject oom-kill; subjectless oom-kill (system); nonfleet oom-kill; `UNIT_RESULT` array `["oom-kill"]` (not positive, want_oom=false); `UNIT_RESULT` `"OOM-KILL"` (not positive).
- positive_unit_signal (user only): user `UNIT_RESULT="signal"` valid; system `signal` valid with `want_signal=false`; adjacent `UNIT_RESULT` missing record does not block the valid one.
- positive_process_sigkill (user only): `EXIT_CODE="killed"` + `EXIT_STATUS` number 9; string `"9"`; rejected `"9.0"`; `EXIT_CODE="dumped"`, `want_signal=false`; system-only sigkill with `want_signal=false`.
- Mixed boot: current-boot valid positive plus foreign-boot valid OOM. Positive counts only the current-boot record; raw count unavailable with `multi-boot`/`boot-mismatch`.
- Empty stream: valid positives are 0 and the raw class is 0. This is the only zero-positive case.
- Unavailable capture: no pack case, because capture failure is not representable in the record schema. Note this as a verification gap: it must be covered by the harness stub contract, not by packs.

## 5. Necessary fixes (before the packs are consumed)

1. Add `expect` (F2) with literal raw and positive values per scope.
2. Close the `invalid_class` enum (F3) and require it to match actual invalid records.
3. Specify global id uniqueness and a seat prefix (F4).
4. Specify the stub: pass records unfiltered by match, project only `--output-fields` (F5).
5. Add a system-only signal/sigkill case with `want_signal=false` (F6).
6. Forbid `MESSAGE` keys and canary strings (F7).
7. Pin the EXIT_STATUS accepted set (F8).
8. Define "malformed" as semantic-only; drop non-JSON from the packs (F1).

## 6. Verification gaps

- Packs and the fixtures directory do not exist yet; every id and literal is unaudited.
- No positive token is implemented; expected literals cannot be checked against the SUT.
- Positive capture-failure paths (rc, stderr, timeout) cannot be expressed in record packs; they need harness-stub coverage.
- No execution performed, per assignment.

## 7. Tool installs

None. No package operation was run. The host-safety notice was acknowledged, and reads and greps only were used.
