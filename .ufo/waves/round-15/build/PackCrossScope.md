# PackCrossScope — round-15 fixture pack report

Seat: `MoriR15.PackCrossScope` (executor, axes `coverage`; milestone "retain validated positives without fabricated totals").
Owned file: `.ufo/waves/round-15/fixtures/CrossScope.json` (only production artifact written).
Report-only claim: this file records static pack design and helper behavior. No census run, no harness run, no gate, no build, lint, test, formatter, or smoke run. No installs, no commits.

## Axes named

- **Coverage (primary):** an individually valid current-boot OOM record must still fire `OOM_KILL_JOURNAL crit` when a different-scope record is invalid, and a valid *system*-scope signal record must never fire the user `KILL_SIGNAL_JOURNAL warn`.
- **No fabricated totals (guard):** the invalid record's class must keep its raw aggregate/split counts `unavailable:<reason>`; the positive token is evidence of at least one record, never a total. The pack asserts `want_oom` / `want_signal` only, plus the named invalid class.
- **Operability (no-harm):** no new query, token rename, route, or actuation is implied by these cases; existing alarm ids and raw tokens are untouched.

## Pack content (4 cases)

File is a JSON list; every case has exactly `{id,user,system,want_oom,want_signal,invalid_class}`. All records use `_BOOT_ID` `11111111111111111111111111111111` unless the case deliberately negatives it; the four catalog ids are the contract literals.

| id | user records | system records | want_oom | want_signal | invalid_class | purpose |
|---|---|---|---|---|---|---|
| `crossscope_system_unit_signal_no_user_warn` | none | `d9b373ed…` + `UNIT_RESULT:"signal"`, `USER_UNIT:"kagi-shokunin.service"` | false | **false** | `null` | A system-scope unit signal is individually valid (`system:positive_unit_signal=1`) but is out of scope for the user warn. The system unit aggregate stays `ok` count 1; no class is invalid. |
| `crossscope_system_signal_positives_user_foreign_sigkill_no_warn` | `98e32220…` + `EXIT_CODE:"killed"`, `EXIT_STATUS:"9"`, foreign boot `222…` | `98e32220…` killed/`"9"` current boot, plus `d9b373ed…` + `UNIT_RESULT:"signal"`, `USER_UNIT:"kagi-shokunin.service"` | false | **false** | `unit_sigkill_record` (user scope) | Adopted from `AttackSignalConfusion` S4: both system signal paths are individually valid (`system:positive_process_sigkill=1`, `system:positive_unit_signal=1`) yet must not raise the user warn; the foreign-boot user process record makes the user aggregate `boot-mismatch`, so its raw counts are unavailable and its positive is `0`. Catches a warn fed by system-scope or summed positives. |
| `crossscope_user_boot_array_kernel_negative_vs_system_kernel_oom` | `fe6faa94…` with `_BOOT_ID:["111…"]` (array) | `fe6faa94…`, current boot | **true** | false | `kernel_oom_notice` | User kernel aggregate is `record-invalid` → user raw counts unavailable and the array-boot record is excluded from positives; the separately valid system kernel record still fires exactly one OOM line. |
| `crossscope_user_foreign_unit_negative_vs_system_unit_oom` | `d9b373ed…` + `USER_UNIT:"kagi-shokunin.service"`, `UNIT_RESULT:"oom-kill"`, foreign boot `222…` | same fields, current boot | **true** | false | `unit_failure_record` | User unit aggregate is `boot-mismatch` → user raw counts/splits unavailable and the foreign record is excluded from positives; the current-boot system unit OOM still fires exactly one OOM line. `oom-kill` is not a signal result, so no warn. |

Semantics used, matching the shared contract and the r15 production header (`tools/mori-census.sh:960-990` at read time):

- A positive record must be a JSON object with scalar string `_BOOT_ID` equal to expected boot and scalar string `MESSAGE_ID` equal to the class id, plus the class field (`UNIT_RESULT` exactly `oom-kill`/`signal`; `EXIT_CODE` exactly `killed` and `EXIT_STATUS` scalar `9`). `EXIT_STATUS:"9"` (string) is accepted; the production header also admits number `9`.
- `want_oom` is true iff at least one independently valid `positive_kernel_oom` or `positive_unit_oom` exists in either scope. `want_signal` is true iff a *user*-scope `positive_unit_signal` or `positive_process_sigkill` exists.
- `invalid_class` names the class whose aggregate raw counts must be `unavailable:<reason>` in the scope that holds the invalid record. Case 1 has no invalid record (`null`, no class unavailable). Case 2 names `unit_sigkill_record` in the **user** scope (`unavailable:boot-mismatch`), even though the system aggregate for that class stays `ok` with its valid positive. Cases 3–4 name the user-scope kernel/unit classes invalid while the system aggregate stays valid.
- Positive tokens are scope-local and are never summed. Case 1 should expose `system:positive_unit_signal=1, user:positive_unit_signal=0`; case 2 `system:positive_process_sigkill=1`, `system:positive_unit_signal=1`, `user:positive_process_sigkill=0`, `user:positive_unit_signal=0`. Cases 3–4 expose the system positive and no user positive.
- In cases 2–4 the scope holding the invalid record still has a parsed stream, so its positive token is a real `0` (no individually valid record), **not** `unavailable:<reason>`; only that class's raw aggregate/splits are unavailable. `unavailable` for a positive token is reserved for capture/stderr/JSON-parse failure, and this pack contains no such failure.

No raw `MESSAGE` field appears in any case, and no secret/canary value is used.

## r14 stub behavior (read, not executed)

Helper: `journal_stub_body` at `tools/mori-round14-regressions.py:579` (generated Python stub; re-read after a sibling edit shifted its line numbers, behavior unchanged); fixture writer `build_fixture` at `:1834` writes `journal/<scope>.records` as one JSON object per line. Projection (`:710-724`): `--output-fields` keeps only requested keys plus the four `ALWAYS` metadata keys (`__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `_BOOT_ID`, `:606`) when present; `MESSAGE` is dropped unless requested (never requested by the census). Filters (`:688-704`): in `honor` mode, records must match every `FIELD=value` argv pair (`str(rec.get(k)) == v`); `ignore-filters` returns every record of the selected scope regardless of filters; `dup-kernel`/`mismatch-kernel` ignore filters only for a kernel `MESSAGE_ID` query; `malformed` emits a non-JSON line at rc 0; per-scope `.rc`/`.stderr` drive producer failure.

Production query shape: `journal_query` (`tools/mori-census.sh:1104`, command template at `:1210`) invokes `journalctl <--user|--system> -b --no-pager -o json --output-fields=… MESSAGE_ID=<id>`; the only structured match word is `MESSAGE_ID=<id>`. The SUT never passes `_BOOT_ID=<expected>` on the command line, so the stub's honor-mode filter cannot drop a boot-anchored negative:

- `_BOOT_ID` array, `_BOOT_ID` missing, or foreign scalar `_BOOT_ID` with a matching scalar `MESSAGE_ID` **is returned under `honor`** and poisons that class's aggregate in jq. Cases 3 and 4 are built this way; they need **no non-honor mode**.
- `MESSAGE_ID` array/object/null or a wrong scalar id is **filtered out under `honor`** (its `str()` does not equal the argv value). Such a negative only reaches the parser under `ignore-filters` (all scope records leak to every class query) or, for kernel-class-only cases, `dup-kernel`/`mismatch-kernel`.

### Needed harness setting (for `tools/mori-round15-regressions.py`)

1. Run **`CrossScope.json` in `honor` mode**. All three invalid records in this pack (case 2 user process, case 3 user kernel, case 4 user unit) are boot-anchored with matching scalar `MESSAGE_ID`, so they are delivered without loosening filters; loosening filters would leak system signal/sigkill records and the foreign user process record into other class queries and manufacture extra `record-invalid` classes that the pack does not expect.
2. For sibling packs whose negatives are `MESSAGE_ID` arrays or wrong ids, the harness must select `ignore-filters` (or `dup-kernel` when every such record is kernel-class and cross-class leakage must be avoided). The shared schema has no `mode` field, so derive it: `honor` unless a record's `MESSAGE_ID` is not a string equal to one of the four catalog ids; then `ignore-filters`, with `dup-kernel` preferred when all such records carry the kernel catalog id. (Message sent to `MoriR15.HarnessBuild` with this recommendation.)
3. `invalid_class` is scope-local in this pack: assert the named class unavailable in the scope containing the invalid record, and assert the other scope keeps its valid count. A purely global "class unavailable" assertion would contradict the C1 cross-scope goal in cases 2–4.
4. Match finding ids as exact tokens (`FINDING KILL_SIGNAL_JOURNAL ` with trailing space), not substrings: case 2 legitimately emits the separate info row `KILL_SIGNAL_JOURNAL_SYSTEM` (the system aggregate is valid), which must not be read as the user warn.

## Static validation performed (no execution)

- JSON parse: all 16 packs present at the final check parse as lists (63 cases); every case has exactly the six schema keys with correct types. Earlier checks with 13 and 14 packs had the same result; the pack set grew while the wave ran.
- `CrossScope.json`: 4 cases, 4 unique ids (prefix `crossscope_`); no id collides with any other pack at the final check (63 ids total, 0 duplicates). The S4-derived case id was checked after the rewrite.
- `CrossScope.json` SHA-256: `31bf81c0ae64e5c245a19da08d6771286ca317dda6b8a3f75f3f91e05ad776b7` (2330 bytes).
- No raw `MESSAGE`/canary text; all literals are the contract boot id and catalog ids.

## Observations and risks

- At the time of the read, `tools/mori-census.sh` had grown to 3900 lines and its header declared the four positive tokens and the positive-gated alarms; the validated-positive jq expressions had landed at lines 1025–1035 (`JOURNAL_JQ_POS_*`), but the alarm emission read at lines 1341–1400 still referenced only raw counters (`ko`, `uo`, `ps`, `us`) and emitted no `positive_*` fields. `tools/mori-round15-regressions.py` did not exist. These are mid-flight states of sibling seats, not findings against my pack; nothing here is verified by execution.
- Harness expectation risk: `invalid_class:null` applies only to case 1; case 2 intentionally makes the **user** `unit_sigkill_record` unavailable while the system row keeps `ok`/positive 1 (adopted from `AttackSignalConfusion` S4, build/AttackSignalConfusion.md). A global `ignore-filters` run would violate case 1's "no class unavailable" through cross-class leakage.
- Process status type was resolved from the current production header (string `"9"` or number `9` both scalar). `EXIT_STATUS:"9"` follows the r14 corpus and sibling packs.
- Not claimed: completeness of any count, authenticated ids, unique victims, or repair of arbitrary malformed JSON. Positive evidence means "at least one individually valid record".

## Handoff checks for the main agent (not run here)

- Run the r15 regression pack suite after CensusPositive and HarnessBuild land; confirm case 1 and case 2 emit no `KILL_SIGNAL_JOURNAL warn` (only `KILL_SIGNAL_JOURNAL_SYSTEM` info in case 2), case 2's user `unit_sigkill_record` is `unavailable:boot-mismatch` with user positives `0` and system positives `1`, cases 3–4 emit exactly one `OOM_KILL_JOURNAL crit` while the user raw class is `unavailable:record-invalid` / `unavailable:boot-mismatch`, and the system counts remain `1`.
- Confirm the harness honors the per-scope `invalid_class` assertion and exact finding-id matching.

## Installations and tool changes

None. The parent host-safety amendment (sync DB ~413 packages ahead; `pacman -Sp` pre-check; no `-Sy`/`-Syu`/`-U`/`-R`; record installs) was received. No package command was run by this seat.

Report: .ufo/waves/round-15/build/PackCrossScope.md
