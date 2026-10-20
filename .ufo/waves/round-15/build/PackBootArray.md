# PackBootArray — round-15 fixture pack

**Seat:** MoriR15.PackBootArray (executor, leaf).
**Assigned file (only production-path write):** `.ufo/waves/round-15/fixtures/BootArray.json`.
**Milestone:** retain validated positives without fabricated totals. **Axis:** C1 coverage (owned axis6 vs operability7).
**SHA-256:** `a746fa2b6d5bb5ea5b8df450c3b6e114577eca030aab3bcbcc6ba9812f7931ed` (3344 B).
**No execution.** No census/harness run, no build/lint/test/formatter. No tool installs or upgrades
(nothing installed, so the host sync-DB warning had no effect). No production file outside the pack edited.

## What was written

A JSON list of 4 case objects in the shared schema `{id, user:[records], system:[records],
want_oom:bool, want_signal:bool, invalid_class:string|null}`. Records are raw structured
journal field maps and map 1:1 to r14 `build_fixture`'s `journal/<scope>.records` JSONL
(`tools/mori-round14-regressions.py:1659-1668`). No `MESSAGE` key, no canary, no secret.
`_BOOT_ID='11111111111111111111111111111111'`; ids kernel `fe6faa94e7774663a0da52717891d8ef`,
unit `d9b373ed55a64feb8242e02dbe79a49c`; process id not used. Cursors are unique (`s=r15-bootarray-*`).

| # | id | records | want_oom | want_signal | invalid_class | intended expectation |
|---|---|---|---|---|---|---|
| 1 | `bootarray-user-kernel-oom-boot-array-current` | user: valid current kernel-OOM object + same-class object with `_BOOT_ID:["1111…"]` (single element = current boot) | true | false | `kernel_oom_notice` | raw `kernel_oom_notice=unavailable:record-invalid`; `positive_kernel_oom=1`; exactly one global `OOM_KILL_JOURNAL` crit; system row valid-empty (all raw counts 0) |
| 2 | `bootarray-user-kernel-oom-boot-null` | user: valid current kernel-OOM object + same-class object with `_BOOT_ID:null` | true | false | `kernel_oom_notice` | same as #1: aggregate unavailable, positive survives |
| 3 | `bootarray-system-kernel-oom-boot-array-multi` | system: valid current kernel-OOM object + same-class object with a two-element `_BOOT_ID` array (current + foreign) | true | false | `kernel_oom_notice` | system row aggregate `unavailable:record-invalid`; `positive_kernel_oom=1` on the system row; one global crit (scope is not summed) |
| 4 | `bootarray-user-unit-signal-boot-null` | user: valid `UNIT_RESULT="signal"` object + same-class `UNIT_RESULT="oom-kill"` object with `_BOOT_ID:null` | false | true | `unit_failure_record` | `unit_failure_record=unavailable:record-invalid` (all unit split tokens unavailable); `positive_unit_signal=1`; `positive_unit_oom=0` (unsafe record excluded, never a fabricated OOM); user `KILL_SIGNAL_JOURNAL` warn, no OOM crit |

Each case has exactly one unusable class, so `invalid_class` is unambiguous. Empty scopes in cases
1/2/4 are genuine valid-empty queries: raw class counts 0 and the row's `boot=` falls back to the
current expected boot (`tools/mori-census.sh:1383`, `${sboot[$scope]:-$BOOT_ID_EXPECTED}`), never a
boot-mismatch or an alarm. (The r13 `boot=unavailable:no-records` token is gone in r14; do not
assert it.)

## Expected production behavior these pin (C1 contract)

- A record counts as positive evidence only if it is an object with a **scalar matching MESSAGE_ID**
  and a **scalar `_BOOT_ID` equal to the current boot**; unit result must be the exact string
  `oom-kill`/`signal`; process record must be exact `killed` + scalar `status 9`. Cases 1-3 keep
  `positive_kernel_oom` from the one valid object while the array/null object poisons only the
  aggregate. Case 4 keeps `positive_unit_signal` from the valid signal object while the null-boot
  `oom-kill` object is excluded from `positive_unit_oom`.
- Existing raw aggregate/split tokens are unchanged in meaning: the mixed class stays
  `unavailable:record-invalid`; no summed/total fabricated, no completeness claim, no authenticated
  ids, no unique victims, no arbitrary malformed-JSON repair.
- OOM warns/fires once if **any** independently valid positive OOM record exists even when raw
  counts are unavailable; the user `KILL_SIGNAL_JOURNAL` WARN likewise uses independently valid
  user unit-signal (and, in sibling packs, process-sigkill) records.
- `positive_*` fields are unavailable only on capture/parser failure. Here capture succeeds, so
  case 4's `positive_unit_oom=0` is a real validated count of zero, not an unavailable token.

## `journal_stub_body` behavior / required harness setting

Read r14 `journal_stub_body` (`tools/mori-round14-regressions.py:404-556`). It parses
`--user|--system`, `-b`, `-o json`, `--output-fields=`, and `FIELD=value` argv filters;
`-b` is a no-op (records are already current-boot), and projection emits exactly the requested
`--output-fields` plus `ALWAYS = (__CURSOR,__REALTIME_TIMESTAMP,__MONOTONIC_TIMESTAMP,_BOOT_ID)`.
Modes: `honor` (default), `leak`, `ignore-filters`, `dup-kernel`, `mismatch-kernel`, `malformed`,
`text`, `hang`, `unit-rc`.

**Required setting: default `mode="honor"`.** In honor mode the filter test is
`str(rec.get("MESSAGE_ID")) == "<id>"` per `want` token; every poison record here carries a matching
**scalar** MESSAGE_ID, so it is returned and its array/null `_BOOT_ID` is projected into the class
stream. The class jq (`JOURNAL_JQ_MSGID`) then rejects it (`_BOOT_ID|type != "string"`) and emits
`record-invalid` — i.e. the aggregate is genuinely invalidated by a record the real filter would
return, not by the stub smuggling it. `ignore-filters`/`dup-kernel` are **not needed** for this pack
and should not be used, since they would also return nonmatching records and weaken the pin. A
nonmatching MESSAGE_ID record only reaches the aggregate under `ignore-filters`/`dup-kernel`
(that edge belongs to the KernelUser/KernelSystem packs). For case 4 the unit query likewise
matches both records on the scalar unit MESSAGE_ID, and `UNIT/USER_UNIT/UNIT_RESULT` are projection
fields, not filters.

Reason expected is `record-invalid`, not `multi-boot`: r14's else-branch checks the `_BOOT_ID`
string/length predicate before boot uniqueness, so an array (even a two-element one containing a
foreign boot) and a null both grade `record-invalid`. Harness should assert
`=unavailable:record-invalid`, not `:multi-boot`/`:boot-mismatch`.

## Retained evidence

- Fixture file bytes and digest: `.ufo/waves/round-15/fixtures/BootArray.json`,
  sha256 `a746fa2b6d5bb5ea5b8df450c3b6e114577eca030aab3bcbcc6ba9812f7931ed`, 3344 B.
- Query/validation source read: `.ufo/waves/round-15/spec.json` (shared contract, fixture schema,
  id/boot constants), `tools/mori-round14-regressions.py:404-556` (`journal_stub_body`, modes,
  filter + projection semantics), `:637-716` (`census_env`, `jrec`/`unit_fail`/`kernel_oom` shapes,
  `MORI_BOOT_ID`), `:743-774` (`Case`), `:1659-1682` (`build_fixture` → `journal/<scope>.records`),
  `tools/mori-census.sh:895-1005` (`JOURNAL_JQ_*`, aggregate all-record validation, scoped classes,
  OOM/KILL semantics, no-MESSAGE queries). No SUT outputs were produced.
- Coordination: sent the pack shape, per-case expectations, and the `mode="honor"` requirement to
  `MoriR15.HarnessBuild`; case ids are `bootarray-*` to stay globally unique if packs are flattened.

## Risks / blockers

- Token spelling/casing of the new `positive_*` fields is owned by the production seat; the pack
  only encodes alarm booleans and invalid_class. Harness must assert the contract names
  `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`
  on the same surface row as the raw class tokens.
- Exact positive counts are 1 (`positive_kernel_oom` cases 1-3, `positive_unit_signal` case 4) and
  0 (`positive_unit_oom` case 4). A `>=1`-only assertion would miss a bug that also counts the
  array/null record; HarnessBuild can derive the exact counts from the records plus the scalar rule
  and should pin them.
- Case 4 is the discrimination for "unsafe oom-kill record is not evidence": if the implementation
  counts any `oom-kill` string, `want_oom=false`/`positive_unit_oom=0` fails.
- Not covered here (owned by sibling packs): process-sigkill record with bad boot, wrong/array
  MESSAGE_ID, foreign boot, missing boot. No blocker; this pack is complete for its named edge.
- No production, fleet, MANIFEST, SHONEN, verifier, aggregator, or sibling fixture/report path was
  touched; no commits; nothing was executed.
