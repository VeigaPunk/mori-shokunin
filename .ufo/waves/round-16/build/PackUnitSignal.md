# PackUnitSignal — round-16 report

## Files changed
- `.ufo/waves/round-16/fixtures/UnitSignal.json` (new, 5536 bytes) — fixture pack, 4 cases.
- `.ufo/waves/round-16/build/PackUnitSignal.md` (this report).

## Cases authored (all user|system unit-failure signal vs malformed result)

| id | scope | topic | stdout records after anchor | want_rc | want_id | key want fields |
|---|---|---|---|---|---|---|
| unitsignal_user_exact_signal | user | exact `UNIT_RESULT="signal"` on `MESSAGE_ID=d9b373ed…49c` (unit_failure_record) | 1 | 0 | MORI_JOURNAL_WINDOW_OK | positive_unit_signal=1, records_after_anchor=1 |
| unitsignal_system_exact_signal_two | system | two distinct units, same boot, both exact signal | 2 | 0 | MORI_JOURNAL_WINDOW_OK | positive_unit_signal=2, records_after_anchor=2 |
| unitsignal_user_malformed_result_not_positive | user | UNIT_RESULT = number `9`, array `["signal"]`, and absent — all resunk, none positive; capture itself still valid | 3 | 0 | MORI_JOURNAL_WINDOW_OK | positive_unit_signal=0, records_after_anchor=3 |
| unitsignal_user_nearmiss_strings_not_positive | user | `UNIT_RESULT="signals"`, `"SIGNAL"` (case/prefix misses) plus `UNIT_RESULT="signal"` on wrong MESSAGE_ID `98e32220…fe15` (unit_sigkill_record) | 3 | 0 | MORI_JOURNAL_WINDOW_OK | positive_unit_signal=0, positive_process_sigkill=0, records_after_anchor=3 |

In every case: all four `positive_*` counts asserted, `positive_kernel_oom`/`positive_unit_oom`/`positive_process_sigkill` pinned to 0. Anchor record itself carries `UNIT_RESULT="signal"` on the unit-failure id — verifies the anchor record is dropped and never counted.

## Source bytes verified before writing
`tools/mori-census.sh` (working tree):
- L1035 `JOURNAL_ID_UNIT_SIGKILL=98e322203f7a4ed290d09fe03c09fe15`
- L1036 `JOURNAL_ID_UNIT_FAILURE=d9b373ed55a64feb8242e02dbe79a49c`
- L1096 `def sig: ((.UNIT_RESULT? | type) == "string" and .UNIT_RESULT == "signal");`
- L1095 `def oom:` requires string `"oom-kill"`; L1097 `resunk` = non-string UNIT_RESULT
- L1054 sigkill predicate requires `EXIT_CODE=="killed"` AND `EXIT_STATUS` 9 — the 98e32220 record in case 4 deliberately lacks those, so `positive_process_sigkill=0`.

## Schema conventions used (messaged to WindowHarness)
- Case keys: `id`, `scope`, `anchor{schema,scope,boot_id,cursor}`, `stdout` (literal JSONL string), `stderr`, `returncode`, `want_rc`, `want_id`, `want{…}`.
- JSONL line 1 = anchor record (`__CURSOR` == `anchor.cursor` literally `"anchor"`, `_BOOT_ID` == anchor boot); later lines unique printable journalctl-shaped `__CURSOR` values, same `_BOOT_ID`, requested fields only — no MESSAGE field anywhere.
- Malformed `UNIT_RESULT` (non-string/missing) is modeled as rc0 `resunk`-class evidence per r15 predicates, not a malformed-capture rc2 — contract lists malformed *capture* (bad JSON/missing cursor/foreign boot) for rc2; flag sent to WindowHarness for confirmation.

## No runs — disclosure
No journalctl queries, no tool/harness subprocesses, no live system reads, no background jobs. One gray-area execution disclosed per L1 clarification: after writing the pack I ran a local `python3` heredoc that only JSON-parsed the fixture file itself (asserted anchor-line cursor/boot match, later-cursor uniqueness, `records_after_anchor` == line count minus 1). It read no lane-external state and wrote nothing; treat as author-lane sanity only — inadmissible as verification. Disclosed to MoriR16.Lesson.

## Risks / blockers
- If the harness treats non-string `UNIT_RESULT` as a malformed capture rather than resunk, case 3's `want_rc`/`want` change — awaiting WindowHarness confirmation; coordinate via that seat id only.
- Cursor realism: literal `"anchor"` plus realistic cursors after it; if harness validates cursor charset strictly this still fits (all printable, ≤4096).
- No installs performed; no pacman transactions.
