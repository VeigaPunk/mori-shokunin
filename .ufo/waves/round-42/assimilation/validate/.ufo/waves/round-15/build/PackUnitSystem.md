# PackUnitSystem — system valid oom-kill with missing `_BOOT_ID`

## Scope and artifacts
- Assignment: fixture pack seat `MoriR15.PackUnitSystem`, named edge **system valid `UNIT_RESULT=oom-kill` plus a missing `_BOOT_ID` record**; no production edits.
- Created: `.ufo/waves/round-15/fixtures/UnitSystem.json` (4 cases, JSON list, shared schema `{id,user,system,want_oom,want_signal,invalid_class}`).
- Report: this file. No other file written. No commit, no verification run of the census/harness/SUT.
- Coordination: fixture shape and stub-mode requirement sent to `MoriR15.HarnessBuild` via `agent://MoriR15.HarnessBuild`.

## Axes
1. **Coverage** — exercise each named `invalid_class` (`unit_failure_record`, `kernel_oom_notice`, `unit_sigkill_record`) while a current-boot system unit OOM positive survives.
2. **Evidence honesty** — invalid class stays unavailable; want_oom=false case proves a boot-invalid `oom-kill` record is not a positive and not a fabricated zero.
3. **Harness compatibility** — records are returned by the r14 stub in `honor` mode without ignore-filters; expectations are static literals independent of the SUT.

## Cases
| id | system records | want_oom | want_signal | invalid_class | intended evidence |
|---|---|---|---|---|---|
| `unitsys_system_oom_valid_plus_unit_missing_boot` | current-boot `d9b373ed` `UNIT_RESULT="oom-kill"` + same record without `_BOOT_ID` | true | false | `unit_failure_record` | `positive_unit_oom` retained although the unit aggregate/splits are invalid |
| `unitsys_system_oom_valid_plus_kernel_missing_boot` | current-boot unit oom-kill + `fe6faa94` record without `_BOOT_ID` | true | false | `kernel_oom_notice` | kernel aggregate invalid (`positive_kernel_oom=0`); unit class aggregate stays valid and alarms |
| `unitsys_system_oom_valid_plus_process_missing_boot` | current-boot unit oom-kill + `98e32220` `EXIT_CODE=killed`/`EXIT_STATUS="9"` without `_BOOT_ID` | true | false | `unit_sigkill_record` | process class invalid (`positive_process_sigkill=0`); no user WARN from a system-scope record |
| `unitsys_system_oom_missing_boot_only` | only `d9b373ed` `UNIT_RESULT="oom-kill"` without `_BOOT_ID` | false | false | `unit_failure_record` | no positive and no alarm; aggregate unavailable, never numeric zero |

All ids are unique. Both scopes carry no raw `MESSAGE` field and no canary. `user` is `[]` in every case — the user KILL_SIGNAL WARN is deliberately not exercised here; system-scope signal/process records must not set `want_signal` (owned by PackCrossScope, respected here).

## Stub behavior grounding (`tools/mori-round14-regressions.py`, `journal_stub_body`)
Both `tools/mori-round14-regressions.py` (ProvenanceCapture) and `tools/mori-census.sh` (CensusPositive) are under concurrent edit this wave; anchors below are content-based, with current observed line numbers.
- Mode docstring `:589-601`: `honor` filters by exact `FIELD=value` argv words and honors `--output-fields` plus always-printed metadata **only if present**; `ignore-filters` returns every scope record regardless of filters; `dup-kernel` ignores filters only for the kernel query.
- `-b` is a no-op (`:630`), so the stub never selects by boot. A record without `_BOOT_ID` that matches the query's `MESSAGE_ID` filter **is returned in `honor` mode**.
- Filter loop `:698-705`: requested pairs are ANDed via `str(rec.get(k)) != v`; a missing `_BOOT_ID` is not a filter key and cannot exclude the record.
- Projection `:715-723`: output fields are intersected with the record; `_BOOT_ID` is only re-emitted when present. So the missing-boot record arrives without `_BOOT_ID`.
- Consumer validation (`tools/mori-census.sh`, `JOURNAL_JQ_MSGID`/`JOURNAL_JQ_SIGKILL`/`JOURNAL_JQ_UNITS`): `all(.[]; ._BOOT_ID | type == "string" && ._BOOT_ID == $boot ...)` fails on the missing field and yields `record-invalid`, making that class's aggregate/splits unavailable.
- r15 positive selectors (`JOURNAL_JQ_POS_PRE` and companions): count only object records with scalar string current `_BOOT_ID`, scalar string matching `MESSAGE_ID`, and the exact class predicate; a parsed stream with no individually valid record yields a real 0 for the positive token, while the raw class count stays unavailable.

### Required harness setting
Use the default **`honor`** stub mode for this pack. `ignore-filters` or `dup-kernel` are wrong here:
- They would feed cross-class records into every query (for example the unit record into the kernel query), invalidating classes beyond the single `invalid_class` and making the expectation ambiguous.
- `dup-kernel` additionally returns the whole scope stream to the kernel slot only, which can poison `kernel_oom_notice` in cases 1, 3, and 4 where no kernel record exists.
- `mismatch-kernel` clears non-kernel slots, erasing the valid unit positive stream.

No ignore-filters capability is needed to reach the poisoned path: the missing-`_BOOT_ID` record still matches `MESSAGE_ID`, so it is returned and poisons the aggregate under `honor`.

## Expected production shape per case
- Case 1: `SURFACE journal.system` shows `unit_failure_record=unavailable:record-invalid` and split tokens unavailable; `OOM_KILL_JOURNAL` crit fires once via `positive_unit_oom` (system counter > 0). No user WARN.
- Case 2: `kernel_oom_notice=unavailable:record-invalid`, `positive_kernel_oom=0`; `unit_failure_record=1` with split counts valid; OOM crit fires via `positive_unit_oom`.
- Case 3: `unit_sigkill_record=unavailable:record-invalid`, `positive_process_sigkill=0`; unit aggregate valid; OOM crit fires via `positive_unit_oom`; no user KILL_SIGNAL WARN (system scope).
- Case 4: `unit_failure_record=unavailable:record-invalid`, `positive_unit_oom=0`; no `OOM_KILL_JOURNAL`, no KILL_SIGNAL. The unavailable token is the only representation; there is no `0` aggregate.

## Boundaries
- Not a completeness claim, authenticated id, unique-victim/kill-total, owner routing, or repair of arbitrary malformed JSON. The fleet/non-fleet/unknown partition remains aggregate-only and unavailable when the class is invalid.
- Positive evidence is record-level scoped evidence, never summed across scopes; case 4's false expectation is an alarm absence, not a proven no-event claim.
- Static fixture assertion only: the pack was parsed locally to confirm schema keys, unique ids, current-or-missing boot values, no `MESSAGE` fields, and enum-valid `invalid_class`. No census/harness invocation was performed.
- Fixture bytes are deterministic (fixed boot/id literals, no timestamps, no canaries, no generated ids), so HarnessBuild can hash this pack at read for CE6 provenance without a moving input here.

## Tooling
No installs or upgrades.
