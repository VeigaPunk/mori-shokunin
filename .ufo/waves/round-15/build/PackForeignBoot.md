# PackForeignBoot — round-15 C1 fixture pack (foreign-boot adjacency)

Scope: own `.ufo/waves/round-15/fixtures/ForeignBoot.json` only. No production edits, no execution.
Fixtures are data: synthetic structured records, no MESSAGE text, no canaries.

## Files changed

- `.ufo/waves/round-15/fixtures/ForeignBoot.json` (new, 4 cases)
- `.ufo/waves/round-15/build/PackForeignBoot.md` (this report)

## Cases (schema: `{id, user:[records], system:[records], want_oom, want_signal, invalid_class}`)

Current boot `11111111111111111111111111111111`; foreign boot `22222222222222222222222222222222`.
Every foreign record is otherwise an exact match for its class query (same scalar `MESSAGE_ID`,
same class fields), so only `_BOOT_ID` distinguishes it.

| id | scope / records | want_oom | want_signal | invalid_class | expected aggregate | expected alarm |
|---|---|---|---|---|---|---|
| `foreignboot_user_kernel_mixed` | user: current kernel OOM + foreign kernel OOM | true | false | `kernel_oom_notice` | `unavailable:multi-boot` | one OOM crit from the current record |
| `foreignboot_system_unit_oom_mixed` | system: current `UNIT_RESULT=oom-kill` + foreign `oom-kill` | true | false | `unit_failure_record` | `unavailable:multi-boot` | one OOM crit (system scope fires the global alarm) |
| `foreignboot_user_unit_signal_mixed` | user: current `UNIT_RESULT=signal` + foreign `signal` | false | true | `unit_failure_record` | `unavailable:multi-boot` | KILL_SIGNAL_JOURNAL warn (user only) |
| `foreignboot_user_unit_oom_with_foreign_process_sigkill` | user: current `UNIT_RESULT=oom-kill` + foreign `EXIT_CODE=killed/EXIT_STATUS=9` | true | false | `unit_sigkill_record` | `unavailable:multi-boot` | one OOM crit from the current unit record; NO KILL_SIGNAL warn (foreign SIGKILL is not a valid positive) |

Positive evidence each case must retain from the single current-boot record (foreign record excluded):
`positive_kernel_oom=1` (case 1), `positive_unit_oom=1` (case 2), `positive_unit_signal=1`
(case 3), `positive_unit_oom=1` and `positive_process_sigkill=0` (case 4). If a wrong
implementation counted both records the token would read `2`; if it let aggregate invalidity
suppress positives the token would read `0`/`unavailable`. Case 4 is the boolean-level control:
its only process record is foreign, so `want_signal=false` fails if a foreign SIGKILL is
accepted as positive evidence, while its unit positive (`positive_unit_oom=1`) is retained and
fires the OOM crit even though `ignore-filters` makes the unit raw aggregate itself unavailable
(unasserted; the foreign process record rides the same stream). This is the sharpest mixed
case: the positive survives aggregate invalidity and the foreign SIGKILL still produces no
warn. Raw tokens in the invalid class keep the `unavailable:<reason>` form. Other classes in
the same scope are not asserted: under `dup-kernel` they honor filters and stay empty, under
`ignore-filters` they also see the whole scope and may read unavailable; only the named invalid
class and the `positive_*` tokens are graded.

## Harness wiring (HarnessBuild canonical loader)

HarnessBuild derives the r14 stub mode from `invalid_class` only:

- `kernel_oom_notice` → `dup-kernel`: only the kernel `MESSAGE_ID` query ignores filters and
  sees the whole scope; every other class query honors filters. Case 1: kernel stream = both
  kernel records → two boots → `unavailable:multi-boot`; other classes empty.
- any other non-null `invalid_class` (my `unit_failure_record` cases 2–3, `unit_sigkill_record`
  case 4) → `ignore-filters`: every class query sees every record of the scope. Side effects on
  other raw classes are **not asserted** by the gate (per HarnessBuild), and per-class positive
  counting is static from the pack, so this mapping does not weaken my expectations:
  - case 2 system unit stream = both `oom-kill` records → `multi-boot`; kernel/process raw
    classes also see them and would read unavailable, unasserted; positive kernel/process = 0.
  - case 3 user unit stream = both `signal` records → `multi-boot`; positive kernel/process = 0,
    positive_unit_signal = 1, so the warn fires with no OOM.
  - case 4 user streams: the process query sees the current unit record and the foreign process
    record → two unique `_BOOT_ID` values → `unavailable:multi-boot` (there is no foreign-only
    class stream in this pack, so no `boot-mismatch` case). The unit query also sees both
    records and its raw aggregate is unavailable (unasserted), yet positive_unit_oom must still
    count the current `oom-kill` record (= 1) and positive_process_sigkill must stay 0, so the
    OOM crit fires and the user warn does not.
- `invalid_class: null` → `honor` (unused in this pack).

Mode mechanics that make the pack observable under all three modes
(`tools/mori-round14-regressions.py:748`, `:450`, `:510-528`, `:535-544`): the stub treats `-b`
as a no-op, so `_BOOT_ID` is never filtered producer-side; the census must reject foreign
records per record. Under `honor`/`dup-kernel`/`ignore-filters` the stub filters only by the
`FIELD=value` argv words it honors, then projects each record onto `--output-fields` plus the
always-printed metadata. My process records carry literal `EXIT_CODE="killed"` /
`EXIT_STATUS="9"` and unit records carry the exact `MESSAGE_ID` so they survive the honor
filters; records only carry fields the census queries (`_BOOT_ID,MESSAGE_ID` for kernel,
`_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT` for unit,
`_BOOT_ID,MESSAGE_ID,EXIT_CODE,EXIT_STATUS` for process). No extra query and no MESSAGE request.

Reason token: mixed scalar current + foreign boots → `unique` boot count 2 → `multi-boot`
(census `JOURNAL_JQ_MSGID` `:973-976`, `JOURNAL_JQ_UNITS` `:1019-1037`). The gate's derived
`multi-boot` for case 4 matches this because `ignore-filters` feeds both scope records into the
process query. `boot-mismatch` would require a single foreign-only boot stream; this pack does
not contain one.

## Evidence anchors (retained)

- `tools/mori-census.sh:317-329` boot anchor is 32 lowercase dashless hex; invalid/absent anchor
  disables counting rather than producing a zero.
- `tools/mori-census.sh:966-976` class ids and all-or-nothing jq: any record failing
  `type=="object" and _BOOT_ID string and == $boot and .MESSAGE_ID == $id` routes the whole
  class to `multi-boot`/`boot-mismatch`/`record-invalid`.
- `tools/mori-census.sh:1000-1037` single-pass unit partition (fleet/nonfleet/unknown, oom,
  signal) shares the validated record set; a foreign record makes every unit token unavailable.
- `tools/mori-census.sh:1151-1230` six queries per scope, `--user/--system -b --no-pager -o
  json --output-fields=… MESSAGE_ID=<id>`; `-b` is in argv but the fixture stub ignores it.
- `tools/mori-round14-regressions.py:404-546` stub modes/filter/projection; `:620-623` boot id
  file wiring; `:1659-1683` `build_fixture` writes `journal/<scope>.records` JSONL per case.

## Risks / non-claims

- Positive-token encoding is CensusFix's production work; this pack only supplies records that
  make the distinction observable. If positive tokens are emitted only on `state=ok` surfaces,
  case 4 will read red (its unit aggregate is unavailable) — that is the intended C1 failure,
  not a fixture defect.
- The gate must keep the exact static positive counts: case 1 `positive_kernel_oom=1`, case 2
  system `positive_unit_oom=1`, case 3 `positive_unit_signal=1`, case 4 `positive_unit_oom=1`
  with `positive_process_sigkill=0`. It must not accept `positive_*=0`/unavailable for cases
  1–4 or widen `invalid_class` to "any unavailable".
- Case 4's `want_signal=false` must not be relaxed to "unchecked": the foreign SIGKILL is
  returned by the process query and is the only process record, so a false positive there is
  a real regression. Likewise case 3's `want_oom=false` must stay checked.
- Records contain no `MESSAGE` key (the gate rejects packs that do) and no arrays/nulls in
  `_BOOT_ID`; array/null boot encoding belongs to PackBootArray.
- One invalid class per case keeps `invalid_class` unambiguous; the pack claims no
  `boot-mismatch` reason (no foreign-only class stream).
- No completeness, authenticated-id, unique-victim, or repair-of-malformed-JSON claim.

## Tooling

No installs or upgrades. No execution (no builds, tests, linters, formatters, census runs).
