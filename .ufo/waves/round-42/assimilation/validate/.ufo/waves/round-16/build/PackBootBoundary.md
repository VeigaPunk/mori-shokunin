# PackBootBoundary — BootBoundary.json

## Files changed
- `.ufo/waves/round-16/fixtures/BootBoundary.json` (new, sole owned file)

## Behavior delivered
Four shared-schema cases covering the boot-boundary topic: anchor-record boot
mismatch and later foreign-boot injection, plus one same-boot success control
so the pack cannot be satisfied by a tool that always refuses.

| id | scope | shape | want_rc | want_id | selected want |
|---|---|---|---|---|---|
| `anchor_record_foreign_boot` | user | first record echoes exact anchor `__CURSOR` but carries `_BOOT_ID=bbbb…` (foreign boot occupying the anchor slot); a second same-boot record follows | 2 | `MORI_JOURNAL_WINDOW_UNAVAILABLE` | `{}` (refusal; no positive totals) |
| `foreign_boot_immediately_after_anchor` | system | valid anchor record (cursor+boot exact), then the very next record is a foreign boot (`cccc…`) with a kernel-OOM catalog id that must never be counted | 2 | `MORI_JOURNAL_WINDOW_UNAVAILABLE` | `{}` |
| `foreign_boot_after_same_boot_positive` | user | anchor, then a valid same-boot `UNIT_RESULT=oom-kill` unit-failure record, then a foreign-boot oom-kill record — a partial rc0 success would leak a positive total across the boundary | 2 | `MORI_JOURNAL_WINDOW_UNAVAILABLE` | `{}` |
| `same_boot_boundary_ok` | user | anchor + two same-boot records: one kernel-OOM catalog id, one benign coredump id | 0 | `MORI_JOURNAL_WINDOW_OK` | `records_after_anchor=2, positive_kernel_oom=1, positive_unit_oom=0, positive_unit_signal=0, positive_process_sigkill=0` |

Design notes:
- `__CURSOR` strings are journalctl-shaped (`s=…;i=…;b=<record's _BOOT_ID>;m=…;t=…;x=…`) and unique per record; anchor record echoes `anchor.cursor` byte-exactly.
- Records carry only the contract field set (`__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS`); no `MESSAGE`, no unit-name fields.
- Refusal `want` objects are empty: the contract pins only rc and stable finding id; no `reason` vocabulary is specified, so none is asserted (coordinated decision, see Risks).
- All refusal cases emit rc0+empty stderr from the fake producer, so unavailability must come from tool-side boot validation, not producer failure.

## Source bytes verified
Catalog ids read directly from `tools/mori-census.sh` (verified at lines 1032–1036,
byte-exact via `cat -A`):
- `JOURNAL_ID_KERNEL_OOM = fe6faa94e7774663a0da52717891d8ef`
- `JOURNAL_ID_COREDUMP = fc2e22bc6ee647b6b90729ab34a250b1`
- `JOURNAL_ID_UNIT_FAILURE = d9b373ed55a64feb8242e02dbe79a49c`

NOTE: the wave spec text for sibling lane PackUnitOom shows
`d9b373ed55a64e6c8e2e7d70a0fce472`, which does NOT match the source bytes
(`d9b373ed55a64feb8242e02dbe79a49c`). I used the source-verified id; the spec
was labeled hints-not-authority, so this is a spec-typo observation for L1, not
a schema question.

## Evidence retained
- `python3 json.load` + per-line `json.loads` over every `stdout` field: pack parses, 4 cases, all JSONL lines valid objects.
- No executions of tool or harness performed (per contract: never execute now; L1 owns post-integration gate).

## Coordination
- WindowHarness (exact id `WindowHarness`): no open schema question — the wave-spec shared schema is explicit and self-contained. Flag for harness author: refusal cases express assertions as `want:{}` + `want_rc`/`want_id`; a refusal-specific `reason` assertion would need a pinned reason vocabulary.

## Risks / blockers
- Empty `want` on refusal cases relies on the harness treating it as "no field assertions"; if the harness requires an explicit absence marker, schema adjustment needed (WindowHarness owner).
- No blocker.

Report: .ufo/waves/round-16/build/PackBootBoundary.md
