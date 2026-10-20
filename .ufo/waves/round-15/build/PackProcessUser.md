# PackProcessUser — user process SIGKILL positive vs malformed EXIT_STATUS

Scope: fixture pack only. No production edit, no execution, no installs.

## Axes (godspeed)

- Coverage: a valid user-scope process SIGKILL record must still emit the user
  KILL_SIGNAL warning when an adjacent malformed-`EXIT_STATUS` record invalidates
  the raw `unit_sigkill_record` aggregate class.
- Precision: malformed / nonmatching `EXIT_STATUS` records must never become a
  numeric-zero total and must never be counted as a positive (no false alarm).
- Contract fidelity: records are current-boot objects with the frozen process
  MESSAGE_ID and only queried fields; no raw MESSAGE, no canary, no new route.

## File

- `.ufo/waves/round-15/fixtures/ProcessUser.json` — 4 cases, schema exactly
  `{id, user, system, want_oom, want_signal, invalid_class}`.

All records: `_BOOT_ID=11111111111111111111111111111111` (scalar, current),
`MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15` (scalar), `EXIT_CODE="killed"`,
`EXIT_STATUS` varied. `system` is empty in every case. No `MESSAGE` key exists
in the pack (`grep -c '"MESSAGE":'` = 0).

| id | user records (`EXIT_STATUS`) | want_oom | want_signal | invalid_class | expected `positive_process_sigkill` |
|---|---|---|---|---|---|
| `process-user-valid-string9-plus-status-array` | `"9"` valid; `["9"]` malformed | false | true | `unit_sigkill_record` | 1 |
| `process-user-valid-numeric9-plus-status-null` | `9` numeric valid; `null` invalid | false | true | `unit_sigkill_record` | 1 |
| `process-user-status-array-only-no-positive` | `[9]` only, no valid record | false | false | `unit_sigkill_record` | 0 |
| `process-user-valid-string9-plus-wrong-scalar-137` | `"9"` valid; `"137"` nonmatching | false | true | `unit_sigkill_record` | 1 |

Static expected semantics (independent of the SUT): a process positive exists
only for an object record with scalar matching `MESSAGE_ID`, scalar current
`_BOOT_ID`, `EXIT_CODE == "killed"`, and a scalar `EXIT_STATUS` whose string form
is `"9"`. Cases 1/2/4 each contain exactly one such record, so the user
KILL_SIGNAL warning fires once even though the raw class aggregate is
unavailable. Case 3 contains none, so no warning and no fabricated zero total:
the raw count stays unavailable while the validated-positive count is 0. No case
contains an OOM record, so `want_oom` is false everywhere.

## Provenance of this pack

- Static bytes, no generated/dynamic content: sha256
  `0e7c89c52f552bbc800612b67cefb149087d8d4dcb3dc78154bb92f31a0ed077`,
  2156 bytes (double-checked by `sha256sum` and Python `hashlib`).
- The file is untracked (`?? .ufo/waves/round-15/fixtures/ProcessUser.json`);
  porcelain status alone cannot detect a rewrite, so the harness must hash the
  bytes it loads and compare a re-hash at emit (AttackProvenance CE1/CE6).
- Zero `"MESSAGE"` keys, seven `"MESSAGE_ID"` occurrences; parsing must read the
  pack once and `json.loads` those same bytes.
- The fixtures directory is a declared input: an output-prefix exclusion of
  `.ufo/waves/round-15` would swallow it (AttackProvenance CE3).

## r14 helper behavior actually read

`tools/mori-round14-regressions.py`:

- `journal_stub_body` at `:404`; modes documented at `:410-421`
  (`honor`, `leak`, `ignore-filters`, `dup-kernel`, `malformed`, `text`,
  `hang`, `unit-rc`).
- Filter semantics `:510-527`: `ignore = MODE == "ignore-filters"`; `dup-kernel`
  sets `ignore = True` only when the argv contains the kernel MESSAGE_ID;
  otherwise every `FIELD=value` word is ANDed with strict
  `str(rec.get(k)) != v`. There is no OR-within-a-repeated-field handling.
- Projection `:536-546`: `--output-fields` narrows each emitted record, the
  `ALWAYS` metadata tuple is added only when present, and `leak` mode is the
  only path that force-injects `MESSAGE`.
- Records are loaded losslessly from `journal/<scope>.records`
  (`:495-506`); `build_fixture` at `:1659` writes those lines verbatim.

## Needed harness setting (decisive)

`honor` mode cannot exercise this pack. The census process query carries
`MESSAGE_ID=98e32220... EXIT_CODE=killed EXIT_STATUS=9`; the stub compares
`str(EXIT_STATUS)` to `"9"`, so array, null and `"137"` records are dropped
before the SUT sees them and `invalid_class` can never become unavailable.

The harness MUST materialize these cases with filter-ignoring behavior for the
process class:

- simplest: r14 mode `ignore-filters` for every case whose `invalid_class` is
  non-null (all four here); or
- tighter: a new per-class mixed mode analogous to `dup-kernel`, keyed on
  `MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15`, so only the
  `unit_sigkill_record` query ignores filters and the other class queries answer
  valid empty streams.

If global `ignore-filters` is used, every other class query also receives the
process records and its aggregate is legitimately unavailable. The harness must
therefore assert only the named `invalid_class` (plus `want_oom` / `want_signal`
and the process positive), not that kernel/unit/coredump aggregates stay `ok`.

## Risks / blockers

- Harness owner must choose the mixed mode above; default r14 `Case.mode` is
  `honor`, which would make these `invalid_class` expectations untestable and
  mis-red a correct SUT.
- The harness schema does not carry positive counts; the static expected values
  are inferred from the record semantics above and must be computed by the
  harness oracle from the records, not hard-coded from the SUT.
- All four cases target the same invalid class by design; they differ in the
  malformed `EXIT_STATUS` type and in whether a valid positive survives.
- No execution, no package installs, no production files touched.
