# PackFanoutPositive — round 15 fixture pack

Status: COMPLETE. Fixture pack written; no execution, no verification run (lane bounds).
Only assigned production path plus this report were written.

## Files changed

- `.ufo/waves/round-15/fixtures/FanoutPositive.json` (new; the only production file touched)
- `.ufo/waves/round-15/build/PackFanoutPositive.md` (this report)

No sibling/fleet/MANIFEST/SHONEN/verifier/aggregator edits. No commits. No tool installs
(host-safety notice received; no pacman/uv/npm operations were needed or run).

## Behavior: what the pack asserts

Three concretely distinct cases, schema exactly
`{id, user:[records], system:[records], want_oom:bool, want_signal:bool, invalid_class:string|null}`.
All valid records use `_BOOT_ID=11111111111111111111111111111111`; no `MESSAGE` field exists
anywhere. Ids: kernel `fe6faa94e7774663a0da52717891d8ef`, unit
`d9b373ed55a64feb8242e02dbe79a49c`, process `98e322203f7a4ed290d09fe03c09fe15`.
Case ids are unique (`fanout-positive-*`); 15 record cursors, all unique.

| case id | scope records | invalid record | invalid_class | want_oom | want_signal |
|---|---|---|---|---|---|
| `fanout-positive-msgid-array-kernel` | user: 2 valid kernel OOM, 1 kernel `MESSAGE_ID` **array**, 1 valid unit `UNIT_RESULT=signal`, 1 valid process `killed`/`"9"`; system: 1 valid kernel OOM | user kernel record `MESSAGE_ID=["fe6f..."]` | `kernel_oom_notice` | true | true |
| `fanout-positive-unit-boot-array` | user: valid unit `oom-kill`, valid unit `signal`, unit `resources` with `_BOOT_ID=["1111..."]`, valid process `killed`/`"9"` | user unit record with same-class scalar id but array boot | `unit_failure_record` | true | true |
| `fanout-positive-process-boot-missing` | user: valid process `killed`/`"9"`, process `killed`/`"9"` **without `_BOOT_ID`**, valid unit `signal`, valid unit `oom-kill`, valid kernel OOM | user process record with matching id/EXIT_CODE/EXIT_STATUS but no boot | `unit_sigkill_record` | true | true |

Independent-record semantics encoded by the expectations:

- Case 1: one OOM line must fire from three independently valid kernel-OOM positives
  (2 user + 1 system) even though the user kernel class aggregate is invalid; one user
  `KILL_SIGNAL_JOURNAL` warn fires once from a valid unit-signal record and a valid
  process-sigkill record. User unit/process classes remain valid, so their raw counts may
  stay available; only `kernel_oom_notice` goes unavailable.
- Case 2: the OOM line depends **only** on `positive_unit_oom=1`; there is no kernel OOM in
  the case. The unit aggregate is invalid, so `unit_failure_record` and its splits read
  unavailable, yet the valid unit signal plus valid process record must produce exactly one
  user WARN.
- Case 3: the process aggregate is invalid; one WARN still fires from the valid process
  record plus the valid unit signal. Two OOM positives (unit `oom-kill`, kernel OOM) must
  yield exactly one OOM line.

All three cases pin one OOM crit line and one user KILL warn line (not one per record);
raw aggregate/split counts are never asserted as zeros or totals. Static positive
literals derivable from the records (independent of SUT):

| case | positive fields (user scope / system scope) |
|---|---|
| `fanout-positive-msgid-array-kernel` | user `positive_kernel_oom=2`, `positive_unit_signal=1`, `positive_process_sigkill=1`, `positive_unit_oom=0`; system `positive_kernel_oom=1`, others 0 |
| `fanout-positive-unit-boot-array` | user `positive_unit_oom=1`, `positive_unit_signal=1`, `positive_process_sigkill=1`, `positive_kernel_oom=0`; system all 0 |
| `fanout-positive-process-boot-missing` | user `positive_process_sigkill=1`, `positive_unit_signal=1`, `positive_unit_oom=1`, `positive_kernel_oom=1`; system all 0 |

## Stub delivery analysis (why a harness mode is required)

Read-only anchors in `tools/mori-round14-regressions.py` (observed at 2026-10-20 04:34;
ProvenanceCapture was actively editing this file, so line numbers drift — cite by symbol):

- `journal_stub_body` (`def` at `:585` at observation) docstring names the modes: `honor`
  (apply exact `FIELD=value` argv filters), `ignore-filters` (return every record of the
  scope for every query), `dup-kernel` (ignore filters only for the kernel `MESSAGE_ID`
  query).
- Mode selection and the keep loop (`:691`–`:705` at observation): records are compared
  with `str(rec.get(k)) != v` for each argv filter word. A record whose `MESSAGE_ID` is an
  array stringifies to e.g. `['fe6f...']` and **never matches** `MESSAGE_ID=<id>`;
  `honor` filters it out. `ignore-filters` and the kernel-leg of `dup-kernel` return it.
- Projection (`:717`–`:724` at observation): `--output-fields` is honored plus the four
  always fields (`__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`,
  `_BOOT_ID`). A missing `_BOOT_ID` stays missing; an array `_BOOT_ID` is serialized as an
  array.

Census query/validation anchors in `tools/mori-census.sh` (observed at 2026-10-20 04:34;
CensusPositive was actively editing this file, so line numbers drift — cite by symbol):

- `journal_query "$flag"` call sites: coredump query (`COREDUMP_SIGNAL=11`), process query
  (filters `MESSAGE_ID=$JOURNAL_ID_UNIT_SIGKILL EXIT_CODE=killed EXIT_STATUS=9`), unit
  query (`JOURNAL_Q_WIDTH=15`, filter `MESSAGE_ID` only; projects
  `UNIT/USER_UNIT/UNIT_RESULT`), and kernel/notice query (filter `MESSAGE_ID` only,
  `JOURNAL_JQ_MSGID`).
- `JOURNAL_JQ_MSGID` / `JOURNAL_JQ_SIGKILL` / `JOURNAL_JQ_UNITS` require every returned
  record to be an object with string current `_BOOT_ID` and the class `MESSAGE_ID`; a
  single unsafe record grades the whole class `record-invalid` (or `boot-mismatch` /
  `multi-boot`), never a fabricated zero.
- `emit_finding OOM_KILL_JOURNAL` emits exactly one global crit per census;
  `emit_finding KILL_SIGNAL_JOURNAL` emits exactly one user warn for process-SIGKILL
  and/or unit-result signal positives.

Consequences for HarnessBuild:

1. `fanout-positive-msgid-array-kernel` **must** run with `mode="dup-kernel"` (or a new
   per-query equivalent that bypasses argv filters on the kernel `MESSAGE_ID` query).
   Under `honor` the array-`MESSAGE_ID` record is filtered out, `kernel_oom_notice` stays
   available, and the case becomes a clean-OOM case: vacuous for this wave's claim.
   Global `ignore-filters` also delivers it but additionally invalidates the user unit and
   process classes, so only the kernel leg should bypass.
2. `fanout-positive-unit-boot-array` and `fanout-positive-process-boot-missing` work under
   `mode="honor"`: their corrupt records keep the scalar class `MESSAGE_ID` (and the
   process record keeps `EXIT_CODE`/`EXIT_STATUS`) so the argv filters still return them;
   the corruption is discovered by JSON validation, which is exactly the aggregate
   invalidation under test.
3. The pack schema has no `mode` field. HarnessBuild must map mode per case id (preferred)
   or derive it from `invalid_class` where unambiguous. I messaged `MoriR15.HarnessBuild`
   with this mapping. If the harness hard-codes `honor`, case 1's `invalid_class` assertion
   will fail for fixture-delivery reasons, not SUT behavior.

## Retained evidence (static reads only; line numbers drift under concurrent owners)

- `tools/mori-round14-regressions.py`: `journal_stub_body` (mode docstring; filter /
  `ignore-filters` / `dup-kernel` logic), and `build_fixture` (materializes
  `user.records` / `system.records` and the mode stub). Observed `def` anchors at
  2026-10-20 04:34: `journal_stub_body` `:585`, mode/keep `:691`–`:705`, projection
  `:717`–`:724`, `build_fixture` `:1850`.
- `tools/mori-round14-regressions.py`: `R14_FANOUT_ONE_SIGNAL_PER_KIND` (one global OOM
  line + one SIGKILL line, drift=2) and `R14_SEC_DUP_MSGID_MIXED` (mode `dup-kernel`).
  The latter was observed re-migrated by a concurrent owner to the r15 partial-positive
  expectation: `kernel_oom_notice=unavailable:record-invalid` with
  `positive_kernel_oom=1`, one retained crit line — supporting the same mode/positive
  mapping this pack encodes.
- `tools/mori-census.sh`: `JOURNAL_JQ_MSGID` / `JOURNAL_JQ_SIGKILL` / `JOURNAL_JQ_UNITS`
  validation, the four `journal_query "$flag"` class call sites, and the
  `emit_finding OOM_KILL_JOURNAL` / `KILL_SIGNAL_JOURNAL` lines (cite by token).
- Static pack check (JSON parse only; no SUT/gate execution): 3 cases, 3 unique case ids,
  15 unique cursors, exact schema key set, `MESSAGE` key absent from every record,
  `MESSAGE_ID` values only the three pinned ids or `[kernel]`.

## Risks, residuals, blockers

- Concurrent repo change observed while this seat read its prerequisites: both
  `tools/mori-census.sh` (CensusPositive) and `tools/mori-round14-regressions.py`
  (ProvenanceCapture) were rewritten repeatedly (mtimes 04:33–04:35; query/validation
  line numbers moved tens of lines, and `R14_SEC_DUP_MSGID_MIXED` was re-migrated to the
  r15 partial-positive expectation). The pack was built from the **semantics** read at
  that time (stub modes, class validation, one-line alarm emission) and does not depend on
  any specific line number. I did not edit either file.
- No encoded mode in the shared schema (see above). This is the one delivery risk; it is
  coordinated with HarnessBuild, not silently assumed.
- `invalid_class` carries no reason string: the pack pins class *unavailability*, not
  `record-invalid` vs `boot-mismatch` reason tokens. Case 1's invalid record is
  current-boot with an array `MESSAGE_ID`, so its reason is `record-invalid`; cases 2–3
  corrupt only `_BOOT_ID` shape, which also lands on `record-invalid` (single boot value
  present). The pack deliberately does not pin either reason string.
- `EXIT_STATUS` uses the r14 pinned scalar string `"9"` (journal JSON scalar); a numeric
  `9` is deliberately not encoded. Harness should compare via the production predicate,
  which already stringifies.
- Positive fields must be asserted as independent evidence counts (e.g.
  `positive_unit_oom=1`, `positive_kernel_oom>=1`), never as numeric-zero totals for the
  invalid class; the pack does not preclaim completeness, authenticated ids, unique
  victims, or repair of malformed JSON.
- Capture/parser-failure unavailability is out of scope for this pack (other seats test
  rc/stderr/malformed/timeout), as is route/actuation behavior.
- No execution was performed. L1 runs the integrated gate once post-integration.

Report: .ufo/waves/round-15/build/PackFanoutPositive.md
