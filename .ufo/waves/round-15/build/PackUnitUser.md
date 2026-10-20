# PackUnitUser — user UNIT_RESULT oom-kill + malformed MESSAGE_ID

Scope: fixture-only executor. Owned artifact `/.ufo/waves/round-15/fixtures/UnitUser.json`; this report is advisory. No production code, census, harness, or frozen artifact was edited. No census, harness, or fixture behavior was executed.

## Delivered pack

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-15/fixtures/UnitUser.json`
Top-level JSON list, 4 cases, each exactly `{id, user, system, want_oom, want_signal, invalid_class}`. Case ids are prefixed `unituser_` and are unique against the sibling packs present at write time (`kernsys_*`, etc.).

Common record pins: `_BOOT_ID = "11111111111111111111111111111111"` on every record; unit `MESSAGE_ID = "d9b373ed55a64feb8242e02dbe79a49c"`; no `MESSAGE` key, no unit-subject canary, no secret material. Valid positive records also carry `UNIT_RESULT: "oom-kill"` and `USER_UNIT: "kagi-shokunin.service"`; the subject is incidental to positive detection, not a claim of unique victim or authenticated id.

| id | valid records | malformed sibling (same user scope, same current boot) | want_oom | want_signal | invalid_class |
|---|---|---|---|---|---|
| `unituser_msgid_array_retains_valid_oom` | unit oom-kill | `MESSAGE_ID` array of unit+kernel ids, `UNIT_RESULT:"oom-kill"` | true | false | `unit_failure_record` |
| `unituser_msgid_missing_retains_valid_oom` | unit oom-kill | `MESSAGE_ID` absent, `UNIT_RESULT:"oom-kill"` | true | false | `unit_failure_record` |
| `unituser_msgid_object_retains_valid_oom` | unit oom-kill | `MESSAGE_ID` JSON object `{"id":"d9b3…"}`, `UNIT_RESULT:"oom-kill"` | true | false | `unit_failure_record` |
| `unituser_malformed_signal_sibling_no_warn` | unit oom-kill | `MESSAGE_ID` array `["d9b3…"]`, `UNIT_RESULT:"signal"` | true | false | `unit_failure_record` |

Expectation basis (shared contract, not SUT observation): a positive requires an object record with scalar matching `MESSAGE_ID` and scalar current `_BOOT_ID`; unit result must be the exact string `oom-kill`/`signal`. Every valid record above satisfies that, so each case's global OOM alarm must fire once. Every malformed sibling fails scalar-`MESSAGE_ID` validation and must be excluded from positives, never read as numeric zero and never repaired. Case 4 is the confusable control: its `UNIT_RESULT:"signal"` sibling has a malformed `MESSAGE_ID`, so it must not fire the user `KILL_SIGNAL_JOURNAL` WARN; `want_signal` stays false. All cases make the raw `unit_failure_record` aggregate unavailable, while raw kernel/process/six-count classes remain governed by their own streams (empty system scope here).

## r14 stub behavior that decides whether these cases are meaningful

Read from `tools/mori-round14-regressions.py` (function `journal_stub_body` at :404; file was concurrently modified by another seat during this read, mtime 04:32, so line numbers are as observed):

- Filters: :685-700. `ignore = MODE == "ignore-filters"`. Otherwise every argv `FIELD=value` word is ANDed with exact string comparison `str(rec.get(FIELD)) == value`.
- Consequence: under the r14 default `mode="honor"`, a sibling with `MESSAGE_ID` as an array, object, `null`, or missing never equals the queried unit id, so the stub drops it and the census never receives it. The case would then only prove a clean positive and would not exercise C1's "adjacent malformed record invalidates the aggregate class". The same is true of case 4's malformed signal sibling.
- Existing filter-ignoring modes: :686-692. `dup-kernel` ignores filters only when argv contains `MESSAGE_ID=fe6faa94…`; `mismatch-kernel` does that and empties every other slot. There is no unit-query or process-query equivalent in the r14 generator.
- Projection: :603 `ALWAYS = (__CURSOR, __REALTIME_TIMESTAMP, __MONOTONIC_TIMESTAMP, _BOOT_ID)`; :710-719 emits only requested `--output-fields` keys that exist on the record, then re-adds any `ALWAYS` key present. So `_BOOT_ID` reaches the census even if omitted from `--output-fields`, while `UNIT_RESULT`/`USER_UNIT` reach it only if requested. A census that does not request `UNIT_RESULT` cannot classify these records and must not be credited for this pack.
- `MESSAGE`: the pack has no `MESSAGE` key, and `leak` mode only injects the synthetic canary; there is nothing target-derived to spill.
- Records are read from `<base>/journal/<scope>.records`; `-b`/`--boot`/`--no-pager` are accepted no-ops (:628), so the current-boot check is entirely SUT-side `_BOOT_ID` comparison.
- Boot configuration: r14's `build_common` writes `JOURNAL_BOOT = "0123456789abcdef0123456789abcdef"` (:195, :801) into `boot_id` and `MORI_BOOT_ID` (:848). Round-15 fixtures use `1111…`. The round-15 harness MUST set `MORI_BOOT_ID` and its `boot_id` file to `11111111111111111111111111111111`, or every valid record in this pack reads as boot-mismatch.

## Needed harness setting (reported to HarnessBuild)

Recommended: derive the stub mode from `invalid_class` and target only the named class, symmetric with r14 `dup-kernel`:

| `invalid_class` | stub mode | change needed |
|---|---|---|
| `kernel_oom_notice` | `dup-kernel` | none (exists) |
| `unit_failure_record` | `dup-unit` | small extension: if mode is `dup-unit`/`mismatch-unit` and argv contains `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c`, set `ignore=True`; `mismatch-unit` additionally empties every other slot |
| `unit_sigkill_record` | `dup-sigkill` | same, keyed on `MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15` |
| `null` | `honor` | none |

This keeps the `invalid_class` assertion exact: only the unit-failure query sees the malformed sibling, so `positive_unit_oom` must remain available while raw `unit_failure_record` goes unavailable.

Fallback (no stub extension): run the scope stub in `ignore-filters`. Then every query in a scope returns every record of that scope, so the wrong-class records also invalidate the kernel and process classes. In that mode the harness may assert only the designed `invalid_class` (here `unit_failure_record`) and must not assert that the other aggregates stayed valid. Alarm booleans still follow independent record semantics and are unaffected.

## Evidence retained

- Authored pack parse (syntax only, no execution): 4 cases, key set `['id','invalid_class','system','user','want_oom','want_signal']`, ids `unituser_msgid_array_retains_valid_oom`, `unituser_msgid_missing_retains_valid_oom`, `unituser_msgid_object_retains_valid_oom`, `unituser_malformed_signal_sibling_no_warn`.
- Stub reads cited above; record helper shape `jrec` at :866; boot constant at :195, ids at :199-203 (unit `d9b373ed…`, kernel `fe6faa94…`, process `98e32220…`), fleet unit at :205.
- Cross-pack id uniqueness at write time: 55 case objects across all present `fixtures/*.json`; zero duplicate ids, and the four `unituser_*` ids occur only in this pack.
- Sibling pack `KernelSystem.json` read for shape consistency (records keyed `_BOOT_ID`/`MESSAGE_ID` only).
- Peer message sent to `MoriR15.HarnessBuild` with the mode mapping, boot-id requirement, projection rule, and expected positive/aggregate split.

## Risks and non-claims

- These fixtures do not assert total counts, authenticated ids, unique victims, or arbitrary malformed-JSON repair; they assert only alarm retention plus named-class invalidation.
- If the harness uses `honor` mode, all four cases silently lose their adversarial half. That is the single largest false-green risk in this pack.
- If the harness leaves r14's default boot id (`0123…`), every case misreads as boot-mismatch.
- `UNIT_RESULT`/`USER_UNIT` are absent from `ALWAYS`; a census that fails to request them cannot be distinguished from a correct one by these fixtures alone.
- The r14 harness and `tools/mori-census.sh` were being edited by sibling seats during this read; line references are pinned to the observed revision, not guaranteed stable afterwards.

## Tooling

No installations or updates. The parent host-safety notice (no `pacman -S` while the sync DB is ahead) was received; nothing was installed, so the `pacman -Sp` pre-check was not needed. No LSP operation was applicable to this JSON-fixture task.
