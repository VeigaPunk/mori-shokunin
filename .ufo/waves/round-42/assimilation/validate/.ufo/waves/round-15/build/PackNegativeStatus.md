# PackNegativeStatus — round-15 process-status negative fixtures

Scope: `.ufo/waves/round-15/fixtures/NegativeStatus.json` only. No production, harness, sibling pack, or registry edits. No execution, builds, tests, linters, formatters, or smoke runs. No tools installed or updated.

## Deliverable

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-15/fixtures/NegativeStatus.json` — JSON list, 4 case objects, exact shared schema keys (`id,user,system,want_oom,want_signal,invalid_class`). Every record uses only `_BOOT_ID`, `MESSAGE_ID`, `EXIT_CODE`, `EXIT_STATUS`; no `MESSAGE`, no canary, no secret material. All records carry the fixed current boot `11111111111111111111111111111111`; process id `98e322203f7a4ed290d09fe03c09fe15`; kernel id `fe6faa94e7774663a0da52717891d8ef`. Case ids are unique and pack-prefixed (`negative-status-*`), so they stay unique against the other packs.

## Cases and expected literals

| case id | scope | records | want_oom | want_signal | invalid_class |
|---|---|---|---|---|---|
| `negative-status-code-array-killed` | user | process id, `EXIT_CODE:["killed"]`, `EXIT_STATUS:"9"` | false | false | `unit_sigkill_record` |
| `negative-status-status-array-string9` | user | process id, `EXIT_CODE:"killed"`, `EXIT_STATUS:["9"]` | false | false | `unit_sigkill_record` |
| `negative-status-status-null` | user | process id, `EXIT_CODE:"killed"`, `EXIT_STATUS:null` | false | false | `unit_sigkill_record` |
| `negative-status-wrong-code-exited-adjacent-kernel-oom` | user | valid kernel id record AND process id, `EXIT_CODE:"exited"`, `EXIT_STATUS:"9"` | **true** | false | `unit_sigkill_record` |

All four cases have `system: []`, so any OOM/signal expectation comes only from the user-scope records; system zeros are valid empty streams, not evidence.

Semantics the pack pins, per the shared contract:

- Positive SIGKILL requires MESSAGE_ID exactly the process id, scalar current `_BOOT_ID`, `EXIT_CODE` exactly `killed`, and scalar `EXIT_STATUS` whose exact value is 9. An array in either field, a non-null non-9 status, or a wrong code is excluded from positive evidence — it is never converted into a numeric-zero total or a SIGKILL claim.
- The three fully negative cases therefore leave `positive_process_sigkill` at 0 while the raw `unit_sigkill_record` aggregate stays unavailable (`unavailable:record-invalid` when the record is delivered). Expected alarms: no OOM, no user signal WARN.
- Case 4 is the independence case: the wrong-code record must never become SIGKILL, yet the adjacent valid current-boot kernel OOM record must still fire exactly one global OOM alarm even though the same user scope's `kernel_oom_notice` aggregate is invalidated by the foreign record. It is a cross-class variant of the C1 claim, not a duplicate of `ProcessUser.json` (which pairs a valid SIGKILL record with a malformed status).
- No case claims completeness, authenticated ids, unique victims, or repaired JSON.

## r14 helper behavior actually read

`tools/mori-round14-regressions.py` (both this file and `tools/mori-census.sh` are being edited by other seats while this pack is written; line numbers below are the last observed values and drift — the symbol and code snippet are the stable reference):

- `def journal_stub_body` (observed at `:579`, first read at `:404` before a +180-line concurrent insertion above it); documented modes in its docstring; argv-to-filter parsing fills `want` with `(field, value)` words.
- `ignore = MODE == "ignore-filters"` (observed `:685`); the filter loop runs only `if not ignore:` (observed `:693`). So **ignore-filters returns every record of the scope regardless of the `MESSAGE_ID=`, `EXIT_CODE=`, `EXIT_STATUS=` argv words**.
- Projection is independent of filtering: `elif fields is not None:` (observed `:714`) emits only requested present fields plus `ALWAYS = ("__CURSOR", "__REALTIME_TIMESTAMP", "__MONOTONIC_TIMESTAMP", "_BOOT_ID")` (observed `:603`); `MESSAGE` is forced only in `leak` mode (`emit = dict(rec)` followed by `emit["MESSAGE"] = CANARY`, observed `:712-713`). My pack contains no MESSAGE, so honor and ignore-filters projections agree on record content.
- `dup-kernel`/`mismatch-kernel` override filters only for the kernel `MESSAGE_ID` query; `malformed`, `text`, `hang` are capture-level failure modes, not applicable here.
- `build_fixture` writes the stub from `case.mode` (`write_exec(journal / "journalctl-stub", journal_stub_body(base, case.mode))`, observed `:1856`); `Case.mode` defaults to `"honor"` (observed `:923`). Fixture packs have no mode field, so the harness chooses it.

Production SUT anchors confirming what these records mean (`tools/mori-census.sh`): `JOURNAL_JQ_SIGKILL=` (observed `:1022`) requires `.EXIT_CODE == "killed"` and `(.EXIT_STATUS | tostring) == "9"`; `JOURNAL_JQ_TAIL=` (observed `:1020`) grades any returned record that is not an object with scalar non-empty `_BOOT_ID`, or whose MESSAGE_ID/filters fail, as `record-invalid` (class unavailable, never 0). The query argv that the honor stub would enforce is the `unit_sigkill_record)` case (`MESSAGE_ID=$JOURNAL_ID_UNIT_SIGKILL EXIT_CODE=killed EXIT_STATUS=9`, observed `:1254`).

## Required harness setting (blocker for observability)

Build these cases with the r14 stub in **`mode="ignore-filters"`**. Under the default `honor` mode the census's own argv (`MESSAGE_ID=98e... EXIT_CODE=killed EXIT_STATUS=9`, the `unit_sigkill_record)` query case in `probe_journal`) makes the stub drop cases 1-3 before the SUT ever sees them: the SUT then reports a valid empty stream (a real 0), `invalid_class` is not unavailable, and the negative cases stop testing per-record exclusion. With ignore-filters the records are delivered, the aggregate class grades `record-invalid`, and the asserted behavior is the round-15 claim.

Case 4 is mode-robust for `want_oom`/`want_signal` (honor: kernel query returns the one valid record, count 1; ignore-filters: kernel aggregate unavailable but the independently valid record still yields one positive). Its `invalid_class` check, however, also needs ignore-filters: under honor the process record is filtered out and `unit_sigkill_record` is `0`, not unavailable. On the frozen r14 red control under ignore-filters, case 4 correctly produces **no** OOM alarm (user kernel aggregate unavailable), i.e. it is expected to fail the round-15 expectation there — that red differential is the point of the case, not a fixture defect.

## Risks / limits

- `invalid_class` is a single string; in these cases it names the record's own class (`unit_sigkill_record`). Under ignore-filters a foreign record is returned to every class query in that scope, so `kernel_oom_notice`/`unit_failure_record` in the same scope also grade unavailable. The harness should assert the named class is unavailable, not that it is the only unavailable class.
- Case 4's `want_oom=true` is contingent on the round-15 per-record positive implementation; if the SUT still gates alarms on the aggregate class, case 4 fails. That is intended coverage of the C1 claim, not uncertainty in the fixture.
- `EXIT_STATUS` is accepted in both numeric and string form by the existing jq (`tostring`), so the invalid cases deliberately target non-scalars, null, and a wrong `EXIT_CODE` rather than re-testing numeric/string parity (covered by `ProcessUser.json`).
- No fixture was executed; the expected booleans are derived from the cited jq/stub literals and the shared contract, not from a run.

## Coordination

Messaged `MoriR15.HarnessBuild` with the pack shape, the `mode="ignore-filters"` requirement, the exact helper anchors, and the red-control expectation for case 4.

## Tooling

No installs or updates. Parent host-safety notice acknowledged; no pacman/uv/npx use occurred.
