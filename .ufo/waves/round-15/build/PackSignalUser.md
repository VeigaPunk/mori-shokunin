# PackSignalUser — user UNIT_RESULT=signal fixture pack

**Owner:** MoriR15.PackSignalUser. **Scope:** new `.ufo/waves/round-15/fixtures/SignalUser.json` only.
**Axes:** coverage; milestone *retain validated positives without fabricated totals*.
**Production touched:** none. **Execution:** none (no census, gate, build, lint, or smoke run).

## Deliverable

`SignalUser.json` is a 4-case JSON list in the shared pack schema
`{id,user,system,want_oom,want_signal,invalid_class}`. All four ids use the
`signal_user_` prefix; a point-in-time parse of the ten packs present at write time found
39 cases and 39 unique ids (no collision). No raw `MESSAGE` or canary field appears in
any record. Every record's `_BOOT_ID` is the shared
literal `11111111111111111111111111111111`; only scalar current-boot records can be
positive evidence.

| # | id | user stream | want_oom | want_signal | invalid_class |
|---|---|---|---|---|---|
| 1 | `signal_user_valid_only` | one scalar `MESSAGE_ID=d9b373ed…`, `UNIT_RESULT="signal"`, `USER_UNIT=kagi-shokunin.service` | false | true | null |
| 2 | `signal_user_valid_plus_array_multivalue` | the same scalar signal record + an adjacent `MESSAGE_ID=["d9b373ed…","d989611b…"]` record with `UNIT_RESULT="signal"` | false | true | `unit_failure_record` |
| 3 | `signal_user_valid_plus_array_oom_claim` | the same scalar signal record + an adjacent `MESSAGE_ID=["d9b373ed…","fc2e22bc…"]` record with `UNIT_RESULT="oom-kill"` | false | true | `unit_failure_record` |
| 4 | `signal_user_array_only_not_positive` | only the array record `MESSAGE_ID=["d9b373ed…","98e32220…"]`, `UNIT_RESULT="signal"` | false | false | `unit_failure_record` |

Static expected literals (independent of SUT output; positive counts are derived by the
gate from scalar-only predicate membership, not read back from the census):

| # | raw aggregate token (user) | positive evidence (user) | alarm |
|---|---|---|---|
| 1 | `unit_failure_record=1`, `unit_signal=1` | `positive_unit_signal=1` | `KILL_SIGNAL_JOURNAL` warn, `paths=unit_result_signal`, `count=0 process_sigkill=0 user_unit_signal=1`; no `OOM_KILL_JOURNAL` |
| 2 | `unit_failure_record=unavailable:record-invalid`, `unit_signal=unavailable:record-invalid` | `positive_unit_signal=1` | `KILL_SIGNAL_JOURNAL` warn; no `OOM_KILL_JOURNAL` |
| 3 | `unit_failure_record=unavailable:record-invalid`, `unit_signal=unavailable:record-invalid` | `positive_unit_signal=1`, `positive_unit_oom=0` | `KILL_SIGNAL_JOURNAL` warn; no `OOM_KILL_JOURNAL` |
| 4 | `unit_failure_record=unavailable:record-invalid` | `positive_unit_signal=0` | no `KILL_SIGNAL_JOURNAL`; no `OOM_KILL_JOURNAL` |

Case 3 is the adversarial pairing: the invalid record *claims* `oom-kill`, but it is not a
scalar `MESSAGE_ID` record, so it is neither an OOM positive nor a numeric-zero total;
`want_oom=false` forbids the OOM line while the independently valid signal record still
warns. Case 4 is the over-count guard: an array-only signal must produce
`positive_unit_signal=0` and no warn. The raw counts stay `unavailable` in every mixed
case; nothing here claims completeness, authenticated ids, unique victims, or parsed
repair of malformed JSON.

## Harness-shape coordination (confirmed with MoriR15.HarnessBuild)

- `invalid_class` bare name ⇒ gate runs the case in r14 stub mode `ignore-filters`;
  `invalid_class:null` ⇒ `honor`.
- Scope is inferred from the stream containing the record that fails the strict
  predicate: here the user scope, so the gate asserts
  `journal.user … unit_failure_record=unavailable` only. Other user classes may also be
  unavailable under `ignore-filters`; the gate deliberately does not require them to
  stay `ok`.
- Positive evidence is independent: the gate requires `positive_unit_signal=1` while the
  raw `unit_signal` token reads `unavailable:<reason>`.
- `want_oom=false` forbids `OOM_KILL_JOURNAL` outright.
- The gate overwrites each fixture `_BOOT_ID` with the shared literal; fixture records
  already carry it.

## Why `ignore-filters` is required (stub inspection)

`journal_stub_body` (`tools/mori-round14-regressions.py:404`) reads
`journal/<scope>.records` per `--user`/`--system` and emulates journalctl:

- Broken-out/`--output-fields` projection is exact, and the four `ALWAYS` metadata
  fields (`__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `_BOOT_ID`) are
  re-added when present (`:539-543`). The unit query's requested
  `_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT` therefore reaches the census intact;
  no `MESSAGE` is requested or emitted.
- `honor` mode ANDs exact `FIELD=value` argv words using
  `str(rec.get(k)) != v` (`:523`). An array `MESSAGE_ID` stringifies to something like
  `['d9b373ed…', 'd989611b…']` and can never equal the scalar argv id, so under `honor`
  the poison record is silently filtered out of every `MESSAGE_ID=<id>` query: the
  aggregate would stay `ok`/`1`, `invalid_class` would never fire, and cases 2–4 would
  vacuously test nothing.
- `ignore-filters` (`:510`, documented at `:411`) returns every record of the scope
  regardless of filters. That reproduces the real journald case this claim targets: a
  journal entry whose `MESSAGE_ID` is a multi-value field matches
  `MESSAGE_ID=<one-value>` and is exported by `-o json` as an array. The census's strict
  scalar predicate (`tools/mori-census.sh:1019` in `JOURNAL_JQ_UNITS`) then grades the
  aggregate `record-invalid`, while an independent per-record scan must still retain the
  scalar current-boot `UNIT_RESULT="signal"` record.
- Side effect: under `ignore-filters` the entire user stream is returned to every class
  query, so all user class aggregates can grade unavailable. This is accepted by the gate
  convention; it is not a fixture defect and the record set was not narrowed.
- If the gate later adopts a stricter hybrid (honor scalar matches plus only non-scalar
  records whose array contains the queried id), cases 2–4 remain valid and become more
  precise; case 1 is mode-independent.

## Retained evidence (no run)

- `tools/mori-round14-regressions.py:404` stub definition; `:510` ignore-filters switch;
  `:523` honor comparison that drops arrays; `:539-543` output-field/ALWAYS projection.
- `tools/mori-census.sh:1001-1040` strict `all()` predicate requiring scalar current
  `_BOOT_ID` and `.MESSAGE_ID == $id` for every returned record; `:1043-1145`
  `journal_query` maps a failed predicate to class-unavailable (`record-invalid`),
  never a partial count.
- `tools/mori-census.sh:1342-1343` shows the pre-r15 warn reading `user:signal` only when
  `user:unit_failure_record` is `ok`; the mixed cases require the r15 independent
  positive path to preserve the warn while that class reads `unavailable`.

## Risks / boundaries

- The decisive dependency is the gate actually selecting `ignore-filters` for non-null
  `invalid_class`; the convention is confirmed by HarnessBuild IRC but
  `tools/mori-round15-regressions.py` did not exist when this pack was written. If it
  lands with `honor` for these cases, cases 2–4 will fail the `invalid_class` assertion
  (loudly, not silently) and that is the intended wiring signal.
- The fixture schema carries booleans, not counters; expected positive literals above are
  the static values the gate must derive from the same scalar predicate.
- No system-scope records: cross-scope signal (system signal must not user WARN) belongs
  to `PackCrossScope`; subject-unknown signal behavior belongs to `PackSubjectUnknown`.
- No tool installs or upgrades were performed this seat.
