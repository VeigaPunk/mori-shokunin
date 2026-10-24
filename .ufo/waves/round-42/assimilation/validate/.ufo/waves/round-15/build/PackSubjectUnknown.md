# PackSubjectUnknown: subject-absent/array/ambiguous OOM retention fixtures

Seat: MoriR15.PackSubjectUnknown (executor, leaf). One fixture pack plus this advisory report;
no production edit. No gate, harness, census or fixture execution was run. Host-safety notice
acknowledged: no package operation was needed or attempted (no installs).

## 1. Deliverable

| Path | Change |
|---|---|
| `.ufo/waves/round-15/fixtures/SubjectUnknown.json` | New pack, 4 cases, prefix `psu_`, exact schema `{id,user,system,want_oom,want_signal,invalid_class}` |

Pack bytes SHA-256: `16402ca406853b579b07b78e430541456dcc7dd0114d53c413afc73d595de7cc`
(the harness should hash this file as it reads it — AttackProvenance CE6).

Self-check on the pack only: 4/4 cases parse, schema keys exact, no `MESSAGE` key in any
record, and zero id collisions across the 63 cases present in `fixtures/*.json` at write time.
This is not SUT verification.

Records are minimal JSON objects (`_BOOT_ID`, `MESSAGE_ID`, class field). Current boot is
`11111111111111111111111111111111`; foreign boot is
`ffffffffffffffffffffffffffffffff`. Every record is a parseable JSON object: the invalid
records below are semantically invalid, never a non-JSON line (a non-JSON line fails the whole
capture and cannot prove a retained positive).

## 2. Cases and derived expectations

Each case carries exactly one individually valid current-boot unit `oom-kill` record and an
adjacent semantically invalid record. Case 4 adds one valid current-boot user SIGKILL record.
`positive_unit_oom=1` in that record's scope is the only OOM positive except case 4, which also
has `positive_process_sigkill=1`. The invalid record is never counted as a positive; it only
invalidates its named aggregate class.

### `psu_system_missing_subject_foreign_boot` (system)

- Valid record: `MESSAGE_ID=d9b373ed…`, `UNIT_RESULT="oom-kill"`, no `UNIT`/`USER_UNIT`
  (only `_SYSTEMD_UNIT`, which is not a subject and is projected away by the unit query's
  `--output-fields`).
- Adjacent invalid: same `MESSAGE_ID`, `UNIT_RESULT="oom-kill"`,
  `UNIT=kagi-shokunin.service`, foreign `_BOOT_ID`.
- Expected: `journal.system.unit_failure_record=unavailable:multi-boot` (two string boot ids);
  `positive_unit_oom=1` in the system scope; `OOM_KILL_JOURNAL` crit once; drift 1; no
  KILL_SIGNAL line; owner partition absent (aggregate-only unavailable); raw unit split/count
  tokens never read `0`.

### `psu_array_subject_msgid_array` (user)

- Valid record: `USER_UNIT=["kagi-shokunin.service","pipewire-pulse.service"]`,
  `UNIT_RESULT="oom-kill"`, current boot. The subject array alone was already non-fatal in r14
  (classified `unit_malformed`/unknown), so it is not the poison.
- Adjacent invalid: `MESSAGE_ID=["d9b373ed…"]` (non-scalar), `UNIT_RESULT="oom-kill"`,
  `UNIT=kagi-shokunin.service`, current boot.
- Expected with the malformed record returned: `journal.user.unit_failure_record=
  unavailable:record-invalid`; `positive_unit_oom=1`; OOM crit once; drift 1; no signal.

### `psu_ambiguous_subject_kernel_msgid_array` (user)

- Valid record: `UNIT` and `USER_UNIT` both present (ambiguous; never fleet/nonfleet),
  `UNIT_RESULT="oom-kill"`, current boot.
- Adjacent invalid: `MESSAGE_ID=["fe6faa94…"]` (non-scalar kernel-class id), current boot.
- Expected under the harness's `dup-kernel` mode: `journal.user.kernel_oom_notice=
  unavailable:record-invalid`; the unit class stays valid (`unit_failure_record=1`,
  `unit_ambiguous=1`, raw `unit_oom=1`) and `positive_unit_oom=1`; `positive_kernel_oom=0`
  (the array-id record is excluded); OOM crit once; drift 1; no signal.
- This case is deliberately **not** frozen-red: the raw unit count survives under
  `dup-kernel`, so the entering census still fires OOM. It asserts kernel-class invalidation
  plus independent OOM, not C1 salvage.

### `psu_array_subject_sigkill_foreign_boot` (user)

- Valid records: the same array-subject `oom-kill` record, plus a current-boot SIGKILL record
  (`MESSAGE_ID=98e32220…`, `EXIT_CODE="killed"`, `EXIT_STATUS="9"`).
- Adjacent invalid: a second SIGKILL record with the same fields and a foreign `_BOOT_ID`.
- Expected under `ignore-filters`: `journal.user.unit_sigkill_record=unavailable:multi-boot`;
  the user unit class is collateral-invalid (`unavailable:multi-boot`) because the same stream
  now holds the mixed-class records and two distinct boot ids (the outer `all()` fails on the
  MESSAGE_ID mix; the two boots then grade `multi-boot`); `positive_unit_oom=1`;
  `positive_process_sigkill=1` (foreign record excluded); OOM crit once AND KILL_SIGNAL warn
  once (user scope); drift 2. Raw `process_sigkill` and `count` on the warn line stay
  `unavailable:multi-boot` and must equal each other, never `0`.
- This is the user-signal retention case: the class is invalid, one current-boot record is
  independently valid, and the warn fires from the positive.

## 3. Stub modes, harness policy and what each case needs

Inspected `journal_stub_body` in `tools/mori-round14-regressions.py` (audited sha256
`e2d3dce03e12b0de37cd74df616c7afe28549839f8a9440b747fa696ed1733ab`, 2026-10-20 04:33).

- `honor` (default) applies every `FIELD=value` match word server-side style
  (`str(rec.get(k)) != v` drops a record). A `MESSAGE_ID`-array record is therefore **never
  returned** to a `MESSAGE_ID=<id>` query.
- `ignore-filters` sets `ignore=True` for **every** query in the scope: every record of that
  scope is returned regardless of match words. This is the only existing mode that returns a
  nonmatching record to a non-kernel class query. Collateral: every class in that scope then
  grades `record-invalid` or `multi-boot` instead of `0`. Positives stay correct because they
  select per record.
- `dup-kernel` ignores filters only when the query's match words include the
  `MESSAGE_ID=fe6faa94…` kernel id; every other slot filters normally. Precise for a
  kernel-class poison; leaves the unit aggregate valid.
- `mismatch-kernel` also clears `records` for every non-kernel query. **Must not be used for
  these packs**: it empties the unit stream, so `positive_unit_oom` disappears and every
  `want_oom=true` case fails.
- Foreign-boot records are **not** a nonmatching case: they carry the matching `MESSAGE_ID`
  (and, for the process class, matching `EXIT_CODE`/`EXIT_STATUS`) and pass `honor` filtering.
  Their invalidation happens in the census's `all()` classification
  (`JOURNAL_JQ_TAIL`/`JOURNAL_JQ_MSGID`/`JOURNAL_JQ_UNITS` and the semantic-failure branch of
  `journal_query`): two string boot ids → `multi-boot`; one foreign id → `boot-mismatch`;
  mismatched scalar fields with one current boot → `record-invalid`.

Harness policy read at `mode_for` in `tools/mori-round15-regressions.py` (read while
HarnessBuild was editing; cite symbols, re-pin at integration):
`invalid_class == null` → `honor`; `invalid_class == kernel_oom_notice` → `dup-kernel`; any
other non-null → `ignore-filters`. That policy matches this pack:

| Case | Harness mode | Why |
|---|---|---|
| 1 `psu_system_missing_subject_foreign_boot` | `ignore-filters` | `unit_failure_record` is not the kernel class. Both records match the unit query anyway, so `honor` gives the same alarm/positive outcome. |
| 2 `psu_array_subject_msgid_array` | `ignore-filters` | The array-`MESSAGE_ID` sibling is dropped by `honor`; without `ignore-filters` (or a new `dup-unit` mode) the unit class would read an available count and the named-invalid assertion would fail. |
| 3 `psu_ambiguous_subject_kernel_msgid_array` | `dup-kernel` | Only the kernel query must return the unfiltered stream; the unit query must stay valid. |
| 4 `psu_array_subject_sigkill_foreign_boot` | `ignore-filters` | `unit_sigkill_record` is not the kernel class. `honor` would also invalidate the sigkill class (both records match) but would leave the unit class valid; `ignore-filters` additionally makes the OOM fire only via the positive, which is the stronger C1 assertion. |

A global `ignore-filters` for all four cases preserves every asserted
`want_oom`/`want_signal`/`invalid_class`/positive outcome; it only widens which classes read
`unavailable:*`, never turns one into `0`. The harness grades only the named invalid class and
the positive tokens, so that collateral is not a grading failure (sibling packs share this).

## 4. Evidence anchors and conformance with the landed selector

Audited production state: `tools/mori-census.sh` sha256
`ef720bc3400cbf1b23996a63d8df0819cb624c045239731c002f735cd0f21967` (2026-10-20 04:44; an
earlier read at `b828df37…` had the same wiring). The file was still being edited during this
audit (digest and length changed between reads), so line numbers are omitted; re-pin the
digest that is graded.

- Class ids and aggregate queries: `JOURNAL_ID_KERNEL_OOM`, `JOURNAL_ID_OOMD`,
  `JOURNAL_ID_COREDUMP`, `JOURNAL_ID_UNIT_SIGKILL`, `JOURNAL_ID_UNIT_FAILURE`;
  `JOURNAL_JQ_TAIL`/`JOURNAL_JQ_MSGID`/`JOURNAL_JQ_SIGKILL`/`JOURNAL_JQ_SIGSEGV`/
  `JOURNAL_JQ_UNITS`; `journal_query`.
- Positive selector: `JOURNAL_JQ_POS_BASE` requires a JSON object with scalar string
  `_BOOT_ID` equal to the expected boot and scalar string `MESSAGE_ID` equal to the queried
  class id. `JOURNAL_JQ_POS_KERNEL` counts those; `JOURNAL_JQ_POS_SIGKILL` additionally
  requires scalar string `EXIT_CODE=="killed"` and `EXIT_STATUS` string `"9"` or number `9`;
  `JOURNAL_JQ_POS_UNIT` returns (exact string `UNIT_RESULT=="oom-kill"`, exact string
  `UNIT_RESULT=="signal"`).
- `journal_positive_scan` runs over the SAME captured raw stream only after a semantic
  aggregate failure (`record-invalid|multi-boot|boot-mismatch`, bad width, bad boot token).
  It does not run after rc/stderr/JSON-parse failure, so positives are unavailable there.
- `journal_pos`: aggregate `ok` → the raw-derived count is the positive; semantic failure →
  the validated fallback vector; empty vector → `unavailable:<class-status>`.
- OOM firing: raw > 0 OR positive > 0, exactly one global crit line; `alarm_basis` separates
  `scoped-record-count` from `validated-positive-records`, and later revisions count a positive
  as the firing basis only when the corresponding raw class query is unavailable (on an ok
  aggregate the raw count is the basis). KILL_SIGNAL (user only): raw > 0 OR positive > 0, same
  attribution. Surface rows carry all four `positive_*` values per scope, never summed.
- The harness's `arm_state`/`expected_alarm_basis` mirror that attribution through
  `class_query_available(records, cls, mode)`, so case 3's ok unit aggregate expects
  `scoped-record-count` while cases 1, 2 and 4 expect `validated-positive-records`.

Conformance table, derived read-only from those filters and the current harness predicates
(`record_matches`, `derive_unavailable`, `count_positives`, `mode_for`):

| Case | Named invalid token | Expected positives | Alarms |
|---|---|---|---|
| 1 | system `unit_failure_record=unavailable:multi-boot` | system `positive_unit_oom=1`; all others 0 | OOM crit; drift 1 |
| 2 | user `unit_failure_record=unavailable:record-invalid` | user `positive_unit_oom=1`; all others 0 | OOM crit; drift 1 |
| 3 | user `kernel_oom_notice=unavailable:record-invalid` | user `positive_unit_oom=1`, `positive_kernel_oom=0`; system all 0 | OOM crit; drift 1 |
| 4 | user `unit_sigkill_record=unavailable:multi-boot` | user `positive_unit_oom=1`, `positive_process_sigkill=1`; others 0 | OOM crit + KILL warn; drift 2 |

Frozen-control consequence of the harness rule (`source_hidden` = the source class's whole
aggregate is unavailable under the selected stub mode, mirroring the stub filter plus the
census `all()`): cases 1 and 2 are red because `ignore-filters` makes the unit query
unavailable and hides `positive_unit_oom`; case 4 is red because `ignore-filters` makes both
the unit and the sigkill queries unavailable, hiding `positive_unit_oom` and
`positive_process_sigkill`; case 3 is not red because `dup-kernel` leaves the unit query
available (raw `unit_oom=1`), so it must and does PASS on the entering census. Case 1 is
system-scope to cover the per-scope positive path (a subjectless OOM in the system journal)
while still naming the class that is actually failing; case 4 carries the valid current-boot
SIGKILL record so the named `unit_sigkill_record` class genuinely fails and the user signal
alarm is retained through `positive_process_sigkill`.

- r14 precedent for the subject shapes and retained control: `R14_UNIT_OOM_MISSING_SUBJECT`,
  `R14_UNIT_OOM_SUBJECT_ARRAY`, `R14_SUBJECT_AMBIGUOUS`, `R14_SEC_DUP_MSGID_MIXED` in
  `tools/mori-round14-regressions.py` (audited sha256 `e2d3dce0…`).
- Pack-to-fixture emission is the same NDJSON `journal/<scope>.records` path as
  `build_fixture`; the stub is `journal_stub_body`.

## 5. Risks and limits

- The census was under active edit throughout this audit. A first read found the positive
  contract comment without the fallback wiring; reads at `b828df37…` and `ef720bc3…` found
  `journal_positive_scan` + `journal_pos` wired into the OOM/KILL firing, the surface rows and
  the raw-vs-positive basis attribution, and every expectation above was re-derived against
  those states. No gate was executed; the harness must re-pin the census digest it grades.
- The harness was also under active edit while read. The mode policy, `derive_unavailable`,
  `count_positives`, `class_query_available`, `arm_state`/`expected_alarm_basis` and the frozen
  loop were read directly; a later revision must be re-checked rather than trusted from this
  report.
- The pack schema has no field for literal raw/positive expectations (review F2) and no mode
  field; the harness derives both. This report states the exact literals and the derived mode
  so the harness author can pin them.
- `invalid_class` has no scope field. Bare names make the harness check every scope that holds
  a failing record; case 1's named class is therefore in the system scope and case 4's in the
  user scope. A harness that checked the user surface unconditionally would misgrade case 1.
- Under `ignore-filters`, non-named classes in the affected scope read `unavailable:*` rather
  than `0` (case 4's unit class, cases 1-2's kernel classes). That is the correct "never a
  fabricated zero" behaviour; the harness grades only the named class and the positives.
- The `unit_sigkill_record` aggregate in case 4 is invalidated by a **foreign-boot sibling**,
  not by a non-scalar id; the valid current-boot record is retained as
  `positive_process_sigkill=1`. No case here claims completeness, authenticated ids, unique
  victims, or repair of arbitrary malformed JSON.
- No execution, no builds, no linters, no formatters, no smoke runs; no installs.
