# PackCleanControls — round-15 C1 clean controls

Owned output: `.ufo/waves/round-15/fixtures/CleanControls.json` (4 cases).
No production file edited. No execution, build, lint, test or formatter run. No installs.

## Named axes

- **Coverage (judged):** clean empty and homogeneous valid streams must keep the previous
  OOM crit / user KILL_SIGNAL warn behavior and must expose available raw counts, so a later
  invalid-adjacency case can only change the *aggregate* tokens, not the alarms that the
  independently valid records justify.
- **Operability context:** raw aggregate counters stay meaningful on clean streams
  (`N ok`, including a proven 0 for the empty scope) and no positive token fabricates a total.

## Pack content

All four cases carry `invalid_class: null`; records use `_BOOT_ID` `1111…1111` and the frozen
ids (`fe6faa94…` kernel, `d9b373ed…` unit failure, `98e32220…` process sigkill). Records are
journal `-o json` shaped strings (`EXIT_STATUS` is the string `"9"`; `UNIT_RESULT` exact
strings), with distinct `__CURSOR`/timestamps. No `MESSAGE` field and no canary.

| id | stream | want_oom | want_signal | previous-behavior expectation on a clean capture |
|---|---|---|---|---|
| `clean-empty-user-and-system` | user [], system [] | false | false | every class `ok` with count 0; no OOM/KILL finding; positives 0; roll CLEAN |
| `clean-user-kernel-oom-homogeneous-three` | user 3× kernel notice | true | false | user `kernel_oom_notice=3`; exactly one `OOM_KILL_JOURNAL` crit, `paths=kernel_oom_notice`, `user_notice=3`; `positive_kernel_oom=3`; roll DRIFT |
| `clean-user-unit-signal-single` | user 1× `UNIT_RESULT=signal`, fleet subject | false | true | user unit record total/fleet/signal = 1, oom = 0; one `KILL_SIGNAL_JOURNAL` warn, `paths=unit_result_signal`, `process_sigkill=0 user_unit_signal=1`; `positive_unit_signal=1`; `UNIT_FAILURE_JOURNAL` info (fleet); roll DRIFT |
| `clean-user-process-sigkill-single` | user 1× `killed`/`"9"` | false | true | user `unit_sigkill_record=1`; one `KILL_SIGNAL_JOURNAL` warn, `paths=process_sigkill`, `count=1 process_sigkill=1 user_unit_signal=0`; `positive_process_sigkill=1`; roll DRIFT |

Expected alarms follow independent-record semantics: a flag is true iff at least one record
satisfying that positive predicate exists. None of these cases may show
`unavailable:<reason>` on a raw count or a positive field — the captures are successful,
stderr-free, valid JSON, so every queried class is `ok`.

Anchors in the current `tools/mori-census.sh` (line numbers moved during the concurrent
CensusPositive edit; treat as approximate): class/query catalog at the `probe_journal` comment
block, `journal_query` width validation and `JOURNAL_JQ_*` filters (`:973-975`),
unit split (`JOURNAL_JQ_UNITS`), OOM emission (`emit_finding OOM_KILL_JOURNAL`, `:1331`) and
KILL emission (`emit_finding KILL_SIGNAL_JOURNAL`, `:1353`).

## Stub mode finding (needed harness setting)

`journal_stub_body` (`tools/mori-round14-regressions.py:588-731`) honors `--output-fields`
plus the four always-printed metadata fields and filters records by exact `FIELD=value` under
mode `honor` (`:698-707`). A record that does not match the query is therefore **not returned
to the census** under `honor`; it cannot invalidate the aggregate class.

- **CleanControls requires `mode="honor"`.** A clean stream must reach the SUT as exactly the
  homogeneous class records, so counts stay available (`0` included for the empty scope).
- **Invalid-adjacency packs require `mode="ignore-filters"`** (or `dup-kernel` /
  `mismatch-kernel` when only the kernel query must return a wrong-class record). Under
  `ignore-filters` (`:690-697`) *every* query receives *every* record of that scope, so a
  nonmatching sibling actually reaches `journal_query` and grades the class
  `record-invalid`; positives must then be computed per record from the same captured
  stream. Under `honor` such a pack is vacuous: the stub silently withholds the poison
  record and the aggregate stays valid.
- Scope of poisoning: `ignore-filters` poisons all classes of the scope; `dup-kernel` poisons
  only the kernel `MESSAGE_ID` query; `mismatch-kernel` returns the wrong-class stream only to
  the kernel slot and a valid empty stream to other slots. There is no narrower unit-only
  mode, so unit-adjacency packs must either use `ignore-filters` or pre-split records.
- Projection: with `--output-fields`, only requested fields plus the four `ALWAYS` fields are
  emitted; `MESSAGE` is dropped (`:718-725`). This pack requests no extra query and adds no
  `MESSAGE`.

Since the shared schema has no `mode` key, the harness must derive it: `invalid_class=null`
→ `honor`; `kernel_oom_notice` → `dup-kernel` (narrow) or `ignore-filters`;
`unit_failure_record`/`unit_sigkill_record` → `ignore-filters`. This was sent to
`MoriR15.HarnessBuild`.

## Checks performed (non-verification)

- JSON parses; every case has exactly the six schema keys with bool/str|null types as
  specified; all four ids are unique. Across the 9 packs present at write time (36 cases),
  no duplicate case id.
- No SUT invocation, no stub execution, no file outside the owned pack and this report.

## Risks / boundaries

- The positive token placement/names are owned by CensusPositive; the pack only asserts
  alarm booleans and clean aggregates, so it does not pin token spelling. The harness must
  derive expected positives from `want_*` or from the records, not assume a fixed count.
- Clean `UNIT_RESULT=oom-kill` (positive_unit_oom) is not a separate case: the 4-case cap is
  spent on empty + kernel OOM + unit signal + process SIGKILL. PackUnitUser/PackUnitSystem
  own the unit-OOM path (with invalid adjacency); clean unit-OOM's only distinct assertion
  over the unit-signal control is the OOM block from the unit subset, already exercised by
  the kernel clean case.
- Multiplicity is exercised only inside the kernel clean case (3 records → count 3, one alarm
  line); FanoutPositive owns multi-source positive cardinality.
