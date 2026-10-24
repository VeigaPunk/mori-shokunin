# PackNegativeInvalid — round-15 fixture pack (malformed/array MESSAGE_ID + boot metadata)

Status: COMPLETE (fixture pack only; nothing executed, no production file touched).

- File changed: `.ufo/waves/round-15/fixtures/NegativeInvalid.json` (new; 4 cases, 2,083 bytes,
  sha256 `a25b39f14f838a70af8e6d0c694f729cb1d6bc3ec89b61b076c1b1e6c386902a`, emitted 2026-10-20).
  This is the hash the harness should record when it loads the pack (CE6); the file is final from this seat.
- Coordination: wrote the stub-mode requirement below to `agent://MoriR15.HarnessBuild`.
- No installs or updates were performed. Host-safety rule observed; nothing from the sync-DB warning was needed.

## Axis and move

Owned axis: coverage against milestone "retain validated positives without fabricated totals". This pack is
the all-negative control for the new positive-evidence interface: every record is malformed on at least one
scalar gate (`MESSAGE_ID` non-scalar, or `_BOOT_ID` non-scalar/absent), so no `positive_kernel_oom`,
`positive_unit_oom`, `positive_unit_signal`, or `positive_process_sigkill` may be emitted, no OOM alarm and no
user KILL_SIGNAL WARN may fire, while the named aggregate class must stay unavailable — never a numeric zero.

## Cases (schema exactly `{id,user,system,want_oom,want_signal,invalid_class}`)

| id | scope | record shape | gate that fails | want_oom | want_signal | invalid_class |
|---|---|---|---|---|---|---|
| `NEG_INVALID_KERNEL_MSGID_ARRAY_USER` | user | kernel notice id as an array `["fe6f…d8ef"]`, `_BOOT_ID` scalar current | MESSAGE_ID not a scalar string | false | false | `kernel_oom_notice` |
| `NEG_INVALID_UNIT_MSGID_ARRAY_USER` | user | unit-failure id as an array, `USER_UNIT=kagi-shokunin.service`, `UNIT_RESULT="oom-kill"`, `_BOOT_ID` scalar current | MESSAGE_ID not a scalar string | false | false | `unit_failure_record` |
| `NEG_INVALID_SIGKILL_BOOT_ARRAY_SYSTEM` | system | `MESSAGE_ID` scalar process id, `EXIT_CODE="killed"`, `EXIT_STATUS="9"`, `_BOOT_ID` as array `["1111…1111"]` | _BOOT_ID not a scalar string | false | false | `unit_sigkill_record` |
| `NEG_INVALID_KERNEL_BOOT_MISSING_SYSTEM` | system | kernel notice id scalar, `_BOOT_ID` key absent | _BOOT_ID not a scalar string | false | false | `kernel_oom_notice` |

All ids use `_BOOT_ID=11111111111111111111111111111111` where a scalar boot is present; the fixed
kernel/unit/process MESSAGE_IDs from the contract are used verbatim. Every record carries only
`__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `_BOOT_ID` (where valid-by-shape), `_TRANSPORT`,
`MESSAGE_ID`, and the routing/result fields; **no `MESSAGE` key and no canary string exists in the pack**.
`__CURSOR` values are unique. Record arrays are one-object-per-line materialized by the r14
`build_fixture` writer (`tools/mori-round14-regressions.py:1839-1844`).

`UNIT_RESULT="oom-kill"` in case 2 and `EXIT_CODE="killed"/EXIT_STATUS="9"` in case 3 are deliberate
positive-shaped payloads placed behind an invalid scalar gate: the contract allows positives only on
"object records with scalar matching `MESSAGE_ID` and scalar current `_BOOT_ID`", so these look-alikes must
remain non-evidence, not be repaired into evidence.

## Needed harness setting (blocking for meaningfulness)

A nonmatching/MESSAGE_ID-array record is invisible unless the stub returns it. In
`tools/mori-round14-regressions.py:584` `journal_stub_body`, mode `honor` applies exact `FIELD=value`
filtering (`:698-708`), and the census asks for `MESSAGE_ID=<id>` (plus
`EXIT_CODE=killed EXIT_STATUS=9` for the sigkill class) as journalctl argv match words
(`mori-census.sh:1241-1266`). Therefore:

- **MESSAGE_ID-array cases (1, 2) require `mode="ignore-filters"`** (`r14:592`, `ignore` set at
  `r14:690`), or `mode="dup-kernel"` (`r14:593-594`, `:691-693`) for a kernel-only array case. Under
  `honor`, journalctl's own filter drops the array-id record, the census sees an empty stream, the class
  grades `ok`/`0`, and the case **false-greens** without ever exercising invalidity.
- **Boot-metadata cases (3, 4) also work under `honor`**: `_BOOT_ID` is never a stub filter (the census uses
  `-b`, not `_BOOT_ID=<id>`), so a record with `_BOOT_ID` array/absent is returned by the MESSAGE_ID match and
  then rejected by the census jq predicates (`JOURNAL_JQ_MSGID`, `JOURNAL_JQ_SIGKILL`). `ignore-filters` is still
  safe for them.

Because the JSON pack schema has no `mode` field, the harness must choose the mode harness-side: use
`ignore-filters` for any pack containing a MESSAGE_ID-array record (uniformly safe for all four cases here),
or derive it per case (`dup-kernel` when only the kernel class is poisoned). `leak`/`text`/`malformed` modes
are not applicable and would invalidate capture for the wrong reasons.

## Expected invalidity semantics under `ignore-filters`

`ignore-filters` returns the scope's records to **every** class query in that scope. The census validation
is all-or-nothing per class (`JOURNAL_JQ_MSGID` `:1021`, `JOURNAL_JQ_SIGKILL` `:1022`, unit predicate
inside `JOURNAL_JQ_UNITS` `:1066`; non-`ok` statuses mapped at `:1151`), so every class queried in the
non-empty scope grades `record-invalid`. Consequently the harness should assert, per case:

1. the `invalid_class` aggregate token is `unavailable:record-invalid` (or a documented unavailable status),
   never `0`;
2. no `positive_*` token carries a value;
3. no `FINDING OOM_KILL_JOURNAL` and no `KILL_SIGNAL_JOURNAL`/`KILL_SIGNAL_JOURNAL_SYSTEM` finding;
4. the empty scope keeps `ok` zero counts;
5. it must **not** require the other classes in the poisoned scope to be numeric zero — they are honestly
   unavailable under this stub mode. This is a harness expectation-setting issue, not fixture ambiguity.

If instead the harness adds a narrower per-class stub mode (not present in r14), the same case expectations
hold with only `invalid_class` unavailable; case 2 would then be the strongest check that an array-id record
is not counted as OOM evidence while its class aggregate is unavailable.

## Retained evidence (read-only)

- `tools/mori-round14-regressions.py:584-729` — stub mode contract (mode docs `:588-599`); `ignore = MODE ==
  "ignore-filters"` at `:690`; `dup-kernel` override at `:691-693`; exact field projection at `:719-723`
  (arrays preserved by `json.dumps`; `_BOOT_ID` absent stays absent; non-leak modes strip `MESSAGE`).
  Line numbers are as read 2026-10-20; `ProvenanceCapture` owns concurrent edits to the revision-capture
  region of this file, and the stub/builder semantics cited here were re-read after the shift.
- `tools/mori-round14-regressions.py:1839-1844` — fixture writer: per-scope `<scope>.records`, one JSON
  object per line; r14 `jrec` shape at `:868-879`.
- `tools/mori-census.sh` — all-or-nothing predicates `JOURNAL_JQ_MSGID` (`:1021`), `JOURNAL_JQ_SIGKILL`
  (`:1022`), and the unit predicate inside `JOURNAL_JQ_UNITS` (`:1066`) require an object with scalar
  non-empty `_BOOT_ID` equal to the expected boot and `MESSAGE_ID == $id`; any violation yields
  `record-invalid`/`multi-boot`/`boot-mismatch` (status mapping `:1151`) and the class counts stay
  unavailable (`:1169-1181`). Line numbers are as read 2026-10-20; `CensusPositive` owns concurrent edits
  that shift them upward, so anchor on these jq names.
- `tools/mori-census.sh:1241-1266` — actual match words and output fields: kernel/oomd/coredump use
  `MESSAGE_ID=<id>`; sigkill adds `EXIT_CODE=killed EXIT_STATUS=9`; unit failure adds
  `UNIT,USER_UNIT,UNIT_RESULT`; no `_BOOT_ID` match word.
- Shared contract in `spec.json`/dispatch (round 15): positives require scalar matching `MESSAGE_ID` plus
  scalar current `_BOOT_ID`; raw aggregate/split counts stay unavailable when invalid; no completeness,
  authenticated-id or unique-victim claim.

## Risks and limits

- Harness mode selection is the single failure mode that can hide these cases (honor ⇒ all four pass
  trivially). If the harness cannot select a mode, cases 3–4 still exercise boot-metadata invalidity under
  `honor`, but cases 1–2 exercise nothing.
- Under `ignore-filters`, `invalid_class` names the primary class only; sibling classes in the same scope are
  also unavailable. Stated above so the harness does not assert a fake zero for them.
- No claim made about the census's new positive selectors beyond the contract: this pack only fixes the
  expected observations; it does not verify them.
- Cross-file id uniqueness: ids are prefixed `NEG_INVALID_`; siblings were still running, so uniqueness
  against other packs could not be checked from this seat.
