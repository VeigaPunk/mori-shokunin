# Round 14 — Result-record fixtures for the restored OOM alarm and fleet routing

**Seat:** `MoriR14.ResultFixtures` (executor, leaf). **Axis:** coverage (primary). **Milestone:** restore OOM alarm and structured fleet routing.
**Scope:** design only. No census, gate, selftest, harness, journal or live probe was executed. No production file, gate, frozen input, sibling file or manifest was edited. Only this report was written. No tool was installed or updated.

This report supplies the independent `UNIT_RESULT=oom-kill` / `failed` / missing / invalid and generic-SIGKILL fixtures for `tools/mori-round14-regressions.py` (JournalRegression). It states exact JSON payloads, slot placement, alarm/routing tuples, verdicts, and the retained controls. Expectations are derived from the frozen and delivered source, the pinned systemd authorities and the L1 ruling; they are not measurements.

## 1. Binding behavior these fixtures gate

The r13 spot-check rejected the delivered round because positive kernel-OOM notices no longer produced `OOM_KILL_JOURNAL crit`/DRIFT, and because every unit failure reused `UNIT_FAILURE_JOURNAL` with no fleet/non-fleet split or tsukuroi route (`corpus/lessons/round-13-verifier-spotcheck.md:76-89,132-134`). The round-14 contract fixes the observable policy:

- `.ufo/waves/round-14/scoped-counter-contract.json`:
  - six raw counters per scope remain measurable even when subject or result metadata is absent/malformed: `kernel_oom_notice, oomd_notice, coredump_notice, segfault_signal11, unit_sigkill_record, unit_failure_record`;
  - `positive_alarm_policy`: `kernel_oom_notice` or observed `UNIT_RESULT=oom-kill` ⇒ critical `OOM_KILL_JOURNAL` and DRIFT independently of subject classification; user `unit_sigkill_record` ⇒ `KILL_SIGNAL_JOURNAL` WARN;
  - `routing_policy`: `UNIT_FAILURE_JOURNAL` fleet only; `UNIT_FAILURE_OUT_OF_SCOPE` non-fleet with `owner=tsukuroi`; absent/unsafe subject ⇒ unknown, no arbitrary payload echo.
- L1 ruling recorded by `CounterAttack.md` §5: **exactly one global `OOM_KILL_JOURNAL crit` line per run**, carrying separate `user_notice`, `system_notice`, `user_unit_oom`, `system_unit_oom` fields and **no summed count**; fleet `UNIT_FAILURE_JOURNAL` is **info** (the older JournalRegression prompt's `warn` is superseded and would be severity drift); missing/null/array subject ⇒ `UNIT_FAILURE_UNATTRIBUTED_JOURNAL info` per scope, owner unresolved. The `_SYSTEM` ID suffix used by the delivered r13 census is accepted only as an ID-family variant; the `scope=` token is the authoritative separator.
- The frozen r13 input (`.ufo/waves/round-14/frozen/mori-census.sh`, sha256 `39abda0a…3985`, the gate's SUT) emits only per-class INFO and no alarm or split (`:1085-1106`, `:1101-1102`), so the alarm/routing cases below are red on those bytes. The working tree's `tools/mori-census.sh` was repaired while this report was being written; §11 pins the gate to the landed tokens.

### 1.1 Source facts that decide the payload values

| Fact | Anchor |
|---|---|
| `unit_log_failure()` emits `MESSAGE_ID=d9b373ed…`, `UNIT_RESULT=%s`, and the unit message. | pinned `src/core/unit.c:6333-6342`; catalog `:561-575` |
| `unit_log_process_exit()` emits `MESSAGE_ID=98e32220…`, `EXIT_CODE=%s`, `EXIT_STATUS=%i`, `COMMAND=%s`. SIGKILL is exactly `EXIT_CODE=killed`, `EXIT_STATUS=9`. | pinned `src/core/unit.c:6355-6392`; catalog `:568-575` |
| The unit subject field is `UNIT=` for the system manager and `USER_UNIT=` for the user manager; `log_unit_struct` appends it via `LOG_UNIT_ID`. | pinned `src/core/unit.c:6995-7001`, `src/core/unit.h:1166-1177,1193-1194` |
| `UNIT`/`USER_UNIT` are client (user) fields naming the subject; `_SYSTEMD_UNIT`/`_SYSTEMD_USER_UNIT` are trusted fields naming the process the entry originates from. | pinned `man/systemd.journal-fields.xml:177-191,247-261` |
| `oom-kill` is a result string for services and scopes; it is not the only result value. | pinned `src/core/service.c:6588-6600`, `src/core/scope.c:721-726` |
| There is no `failed` result literal in any pinned per-unit result table. `failed` in this report is a deliberate client-set/unrecognized value, not a source-valid enum. | pinned `src/core/{service,scope,mount,socket,swap,timer,path,automount}.c` result tables |
| `journalctl -o json` exports a repeated field as an array, an unprintable value as a byte-number array, and an overlong field as `null`. | pinned `src/shared/logs-show.c:1114-1121`, `JSON_THRESHOLD=4096` at `:43` |
| The per-unit result values are strings; `UNIT_RESULT=oom-kill` is an OOM indication, not a victim count or proof of cause. | catalog `:604-616`; `structured-journal-scopes-r13.md:13-14` |

## 2. Fixture encoding contract for the new gate

The gate must be able to use these payloads without reading the host journal. The contract below mirrors the r13 harness (`build_common`/`census_env`, `tools/mori-round13-regressions.py:581-656`) and closes the stub hazards recorded by `OomAttack.md` CX7 and `CounterAttack.md` CX3/CX5.

1. **Environment.** Use `build_common(base)` and `census_env(base)` unchanged, including:
   - `MORI_BOOT_ID=0123456789abcdef0123456789abcdef` (the `census_env` default);
   - `MORI_JOURNALCTL_BIN=$base/bin/journalctl`; `MORI_JQ_BIN` is left at its system-jq default (the r13 `census_env` does not override it); the journalctl stub reads its fixture data either from a generated stub (the r13 harness pattern) or from a `MORI_FIXTURE` dispatch tree (the census-selftest pattern);
   - quiet `pgrep/df/tmux/git` stubs, empty wave/state trees and zero cgroup counters, so the only findings are the journal ones under test.
2. **Slots.** One JSONL file per scope and class under the fixture tree:
   - `journal-<scope>-unit_failure` for `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c`;
   - `journal-<scope>-unit_sigkill` for `MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15`;
   - `journal-<scope>-kernel_oom` for `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`;
   - the existing `oomd`, `coredump`, `segfault` slots remain as in r13.
   A missing slot is an empty stream (valid zero). Sidecars `journal-<scope>-<class>.rc` (producer exit) and `.err` (presence-only stderr bytes) keep the r13 unavailable semantics.
3. **Stub matching.** The stub MUST select records by the **scope flag** and **AND every `FIELD=value` match word** in argv. It MUST NOT key only on `MESSAGE_ID` and return the whole slot for a second query. This is required because the repair may issue either one partitioned query or a second `UNIT_RESULT=oom-kill` query; a whole-slot answer would turn mixed fixtures into `record-invalid` or over-count. Unknown `MESSAGE_ID` ⇒ empty stream, rc 0.
4. **Output fields.** Honor `--output-fields=_BOOT_ID,MESSAGE_ID,...`: emit only the listed keys, plus `MESSAGE` only when `MESSAGE` is explicitly requested. A field absent from the stored object is omitted (real journalctl behavior). A `leak` mode may force `MESSAGE` into the output even when not requested; the census must still never echo it.
5. **Non-JSON mode.** Return a header line only (the r13 stub behavior). This keeps the structured fixtures observable only through the JSON path. Disclosure: this makes the gate's red-before structural (the structured SUT is blind to it) rather than a re-measurement of the historical text probe; the historical harm is established by the frozen source and the spotcheck, not by this fixture.
6. **Record data.** Every stored record carries `MESSAGE":"R14_MESSAGE_CANARY"`; SIGKILL records additionally carry `COMMAND":"R14_COMMAND_CANARY"`. Unit names and result values are themselves the data under test. The census must never emit any of these bytes.
7. **Isolation.** One fixture root per case unless a case names multiple slots; the token matrix and fan-out cases deliberately use both scopes to prove no summation.

## 3. Expectation notation

- `OOM1` — exactly **one** `FINDING OOM_KILL_JOURNAL` line in the whole output; no `OOM_KILL_JOURNAL_SYSTEM` or `_USER` sibling line, no second alarm line.
- `OOMF(u,s,uo,su)` — that line carries `severity=crit`, `paths=<list>` where the list is `kernel_oom_notice`, `unit_result_oom_kill`, or both comma-joined, and the four independent fields: `user_notice=<u>`, `system_notice=<s>`, `user_unit_oom=<uo>`, `system_unit_oom=<su>`. It may also carry `user_unit_oom_result_unknown=<n>` / `system_unit_oom_result_unknown=<n>`. Each value is an integer, or `unavailable:<reason>` when that source is not ok. No `total=`/`sum=` token and no `count=` that represents a cross-path or cross-scope sum; the four fields are the required counts.
- `RUNK(scope,n)` — the landed result-unknown counter, asserted on `SURFACE journal.<scope>` as `unit_oom_result_unknown=<n>` and, when the OOM line is emitted, as `user_unit_oom_result_unknown=<n>` or `system_unit_oom_result_unknown=<n>`. The landed selector counts this only when the `UNIT_RESULT` key is absent or non-string (array/byte array/`null`); an empty or arbitrary string is a non-oom result, not result-unknown. It is never `unit_result=oom-kill` and never a silent 0.
- `SURF(scope; six counts)` — `^SURFACE journal.<scope>: (ok|unavailable)` with the six named counts in the delivered order: `kernel_oom_notice oomd_notice coredump_notice segfault_signal11 unit_sigkill_record unit_failure_record`. A count is an integer only when its class is ok; otherwise `unavailable:<reason>`.
- `FLEET(scope,n)` — `FINDING UNIT_FAILURE_JOURNAL` (user) or `UNIT_FAILURE_JOURNAL_SYSTEM` (system), `severity=info`, `count=n`, `scope=<scope>`, class token `class=unit_failure` (or the retained `class=unit_failure_record`); no `owner=tsukuroi`.
- `NONFLEET(scope,n)` — `FINDING UNIT_FAILURE_OUT_OF_SCOPE` (user) or `UNIT_FAILURE_OUT_OF_SCOPE_SYSTEM` (system), `severity=info`, `count=n`, `scope=<scope>`, `owner=tsukuroi`.
- `UNATTR(scope,n)` — `FINDING UNIT_FAILURE_UNATTRIBUTED_JOURNAL` (one id; `scope=<scope>`; a `_SYSTEM` suffix is accepted only if a fork emits it), `severity=info`, `count=n`; no `owner=tsukuroi` and no fleet bucket (`owner=unresolved` or no owner token is acceptable).
- `DRIFT1` / `CLEAN0` — `^MORI_CENSUS: DRIFT ` / `CLEAN ` and exit 1 / 0; where deterministic the `drift=N` tally is stated. Info findings never flip the roll.
- `NOECHO` — none of `R14_MESSAGE_CANARY`, `R14_COMMAND_CANARY`, `R14_RESULT_CANARY`, `R14_UNIT_CANARY`, `shokunin-fleet-fixture.service`, `pipewire-pulse.service`, `tmux-spawn-r14.service`, `tmux-spawn@r14.service`, `run-p4175743-i29293759.scope`, `bluetooth.service`, `the-tick@r14.service`, `the-tick.service`, `ufo-sighting.service`, `fleet-runner.service`, `shokunin-watchdog.service`, `kagi-shokunin.service`, `user@1000.service`, `user@1050.service` appears in stdout or stderr; no `"MESSAGE":` key is printed.
- The ID suffix `_SYSTEM` is optional in the gate regex (`UNIT_FAILURE_(JOURNAL|OUT_OF_SCOPE|UNATTRIBUTED_JOURNAL)(_SYSTEM)?`) if CensusRepair retains the r13 naming fork; the `scope=` token must always match. The OOM line is unsuffixed by the L1 ruling.

### 3.1 Case index

| IDs | Plane |
|---|---|
| RF01–RF04 | `UNIT_RESULT=oom-kill` with fleet/non-fleet subjects, system and user scopes |
| RF05–RF10 | oom-kill with array / missing / both-field / scope-boundary / empty / null subjects (alarm must survive) |
| RF11–RF12 | oom-kill from a foreign boot and from an rc-2 producer (unavailable, no alarm) |
| RF13–RF18 | non-OOM results: `failed` (unrecognized string), `timeout`, `signal`, `exit-code`, `resources` |
| RF19 | mixed oom-kill + `exit-code` in one scope (subset, partition, no subtraction) |
| RF20–RF25 | missing / single-array / multi-array / empty / uppercase / injected result values |
| RF26–RF33 | subject selection: emitter trap, token matrix, `\x2d` escape, byte array, malformed, both fields, system-file `USER_UNIT` |
| RF34–RF39 | generic SIGKILL: user warn, system info, SIGTERM/normal-exit filters, bypass validation, overlap with oom-kill |
| RF40–RF45 | fan-out and controls: four-plane incident, empty zero, text-only, leak mode, notice + missing result, both-scope result |

## 4. Group A — `UNIT_RESULT=oom-kill` is an OOM indication (alarm must fire)

Every A case uses one `d9b373ed…` record in the named scope, no kernel notice, no SIGKILL record, and an otherwise quiet fixture. The alarm is independent of the subject: A05–A10 carry absent, ambiguous or non-string subjects (A08 is the scope-field boundary, not an invalid subject). The unit-failure count predicate remains `_BOOT_ID` + `MESSAGE_ID` only; subject/result validity selects the routing/result bucket, never the count.

**RF01 — oom-kill, fleet system subject.**
Slot `journal-system-unit_failure`:
```jsonl
{"__CURSOR":"s=r14rf-RF01-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"shokunin-fleet-fixture.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `OOM1 OOMF(0,0,0,1)`; `SURF(system; 0,0,0,0,0,1)` and `SURF(user; all 0)`; `FLEET(system,1)`; no `NONFLEET`, no `UNATTR`; `DRIFT1` with `drift=1`; `NOECHO`. The line names the result path in `paths=` (`unit_result_oom_kill`) and carries `trust=client-supplied`, and claims no victim/cause.
r13-before: **red** — r13 emits the generic `UNIT_FAILURE_JOURNAL_SYSTEM info count=1`, no OOM line, CLEAN.

**RF02 — oom-kill, non-fleet system subject.**
```jsonl
{"__CURSOR":"s=r14rf-RF02-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"pipewire-pulse.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `OOM1 OOMF(0,0,0,1)` — the non-fleet subject must not demote the alarm; `SURF(system; …,unit_failure_record=1)`; `NONFLEET(system,1)`; no `FLEET`; `DRIFT1`; `NOECHO`.
r13-before: **red** — generic fleet-shaped ID, no OOM, no tsukuroi route.

**RF03 — oom-kill, fleet user subject.**
```jsonl
{"__CURSOR":"s=r14rf-RF03-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"tmux-spawn-r14.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `OOM1 OOMF(0,0,1,0)`; `FLEET(user,1)`; `SURF(user; …,unit_failure_record=1)`; `DRIFT1`; `NOECHO`.
r13-before: **red**.

**RF04 — oom-kill, non-fleet user scope unit (`run-…scope`).**
```jsonl
{"__CURSOR":"s=r14rf-RF04-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"run-p4175743-i29293759.scope","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `OOM1 OOMF(0,0,1,0)`; `NONFLEET(user,1)`; no `FLEET`; `DRIFT1`; `NOECHO`. This is the observed live shape (a non-fleet user scope with an `oom-kill` result) and proves the alarm is not tied to a fleet route. A `.scope` can carry the `oom-kill` unit result (scope result table) but does not emit `98e32220` process-exit records, so no SIGKILL record is expected here.
r13-before: **red**.

**RF05 — oom-kill, array subject (duplicate/multi-value field).**
```jsonl
{"__CURSOR":"s=r14rf-RF05-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":["pipewire-pulse.service","tmux-spawn-r14.service"],"UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `OOM1 OOMF(0,0,1,0)`; `unit_failure_record=1` and the class **ok**, not `record-invalid`; `UNATTR(user,1)` with `malformed=1` (the array is a non-string subject); no `FLEET`/`NONFLEET`; `DRIFT1`; `NOECHO`. The subject array must not be stringified into a fleet hit and must not blank the count.
r13-before: **red**.

**RF06 — oom-kill, subject key absent.**
```jsonl
{"__CURSOR":"s=r14rf-RF06-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `OOM1 OOMF(0,0,1,0)` (the alarm survives a missing subject); `unit_failure_record=1`; `UNATTR(user,1)` with `missing=1`; no fleet/non-fleet claim; `DRIFT1`; `NOECHO`.
r13-before: **red**.

**RF07 — oom-kill, both subject fields present.**
```jsonl
{"__CURSOR":"s=r14rf-RF07-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"shokunin-fleet-fixture.service","USER_UNIT":"pipewire-pulse.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `OOM1 OOMF(0,0,0,1)`; `unit_failure_record=1`; `UNATTR(system,1)` with `ambiguous=1` (both keys present is unknown, not a first-field fleet hit); no `FLEET`/`NONFLEET`; `DRIFT1`.
r13-before: **red**.

**RF08 — oom-kill, only `USER_UNIT` present in the system file.**
```jsonl
{"__CURSOR":"s=r14rf-RF08-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"2345","_UID":"1050","_COMM":"systemd","_SYSTEMD_UNIT":"user@1050.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"tmux-spawn-r14.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `OOM1 OOMF(0,0,0,1)`; `FLEET(system,1)` under the landed subject selector: it counts the present keys and uses `.UNIT // .USER_UNIT`, so a single `USER_UNIT` is the subject even in the system file (a system-file user-manager record with uid<1000 / runtime-journal fallback is source-possible). The `system_unit_oom` field follows the queried journal scope (the record is in the system slot), not the subject field's manager. This is the pinned rule in the delivered bytes; if the selector changes, this case must migrate. Boundary, not a silent default.
r13-before: **red**.

**RF09 — oom-kill, empty-string subject.**
```jsonl
{"__CURSOR":"s=r14rf-RF09-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `OOM1 OOMF(0,0,1,0)`; `unit_failure_record=1`; `UNATTR(user,1)` with `malformed=1` (empty string); `DRIFT1`; `NOECHO`.
r13-before: **red**.

**RF10 — oom-kill, `null` subject (overlong/unprintable journal field).**
```jsonl
{"__CURSOR":"s=r14rf-RF10-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":null,"UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `OOM1 OOMF(0,0,0,1)`; `unit_failure_record=1`; `UNATTR(system,1)` with `malformed=1` (`null`); class ok; `DRIFT1`.
r13-before: **red**.

**RF11 — oom-kill from a foreign boot: unavailable, never a false DRIFT.**
```jsonl
{"__CURSOR":"s=r14rf-RF11-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"ffffffffffffffffffffffffffffffff","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"shokunin-fleet-fixture.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `SURF(system; …,unit_failure_record=unavailable:boot-mismatch)`; no OOM line; no routing line from that class; no `=0` look-alike; `CLEAN0`. The OOM line, if emitted for another positive path, would print `system_unit_oom=unavailable:boot-mismatch`, never 0.
r13-before: **green** (retention control).

**RF12 — oom-kill slot producer rc 2: unavailable, never a false DRIFT.**
Slot `journal-system-unit_failure` (same as RF01 except the cursor), plus sidecar `journal-system-unit_failure.rc` containing `2`:
```jsonl
{"__CURSOR":"s=r14rf-RF12-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"shokunin-fleet-fixture.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `SURF(system; …,unit_failure_record=unavailable:rc-2)`; no OOM or routing line; no 0; `CLEAN0`; quiet user row. If the repair issues a second `UNIT_RESULT=oom-kill` query against the same slot, the stub must return rc 2 for it too, so the source is unavailable as a whole.
r13-before: **green** (retention control).

## 5. Group B — non-OOM results, missing/invalid results, and the `oom-kill` subset

Add to the notation: `RUNK(scope,n)` — the landed result-unknown counter (`unit_oom_result_unknown` on the surface; `user_unit_oom_result_unknown`/`system_unit_oom_result_unknown` on the OOM line). It is **required** when the `UNIT_RESULT` key is absent or non-string (array/byte array/`null`); the landed selector uses `type != "string"`, so an empty or arbitrary string is a non-oom result, not result-unknown. It is never `unit_result=oom-kill` and never a silent 0. The OOM subset fields (`user_unit_oom`/`system_unit_oom`) count **only** records whose `UNIT_RESULT` is the exact JSON string `"oom-kill"`.

> **Source calibration — `failed` is not a systemd result literal.** The pinned per-type result tables enumerate `success, resources, protocol, timeout, exit-code, signal, core-dump, watchdog, start-limit-hit, oom-kill` (services) plus type-specific values; none contains `failed` (`src/core/service.c:6588-6600`, `src/core/scope.c:721-726`). RF13/RF14 therefore use `failed` as the assignment's **unrecognized client-set value**, not as a source-valid enum. RF15–RF18 are the source-valid non-OOM controls. The landed type-based selector treats `failed` as a non-oom string (`unit_oom_result_unknown=0`); the decisive assertions are no OOM, the raw count and the subject route.

**RF13 — `failed`, fleet system subject.**
```jsonl
{"__CURSOR":"s=r14rf-RF13-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"shokunin-fleet-fixture.service","UNIT_RESULT":"failed","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect no OOM line; `SURF(system; …,unit_failure_record=1)`; `FLEET(system,1)`; the landed selector treats `failed` as a non-oom string, so `unit_oom_result_unknown=0` (no `RUNK`); `CLEAN0`; `NOECHO`. A generic fleet failure is **info**, matching frozen `:904-906` and the L1 ruling; `warn` here would be severity drift.
r13-before: **green** on the alarm/route tuple (r13 already emits `UNIT_FAILURE_JOURNAL_SYSTEM info count=1`); no result-unknown token is expected for a string value.

**RF14 — `failed`, non-fleet user subject.**
```jsonl
{"__CURSOR":"s=r14rf-RF14-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"pipewire-pulse.service","UNIT_RESULT":"failed","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect no OOM; `NONFLEET(user,1)` with `owner=tsukuroi`; no `FLEET`; the landed selector treats `failed` as a non-oom string, so `unit_oom_result_unknown=0`; `CLEAN0`.
r13-before: **red** — r13 emits the fleet-shaped `UNIT_FAILURE_JOURNAL`, no tsukuroi route.

**RF15 — `timeout`, fleet user subject (source-valid non-OOM).**
```jsonl
{"__CURSOR":"s=r14rf-RF15-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"the-tick@r14.service","UNIT_RESULT":"timeout","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect no OOM; `FLEET(user,1)`; no `RUNK` positive (recognized enum); `CLEAN0`.
r13-before: **green** (retention/negative control).

**RF16 — `signal`, fleet user subject (not SIGKILL, not OOM).**
```jsonl
{"__CURSOR":"s=r14rf-RF16-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"tmux-spawn-r14.service","UNIT_RESULT":"signal","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect no OOM; `FLEET(user,1)`; the landed repair restores the historical `'signal'` text path as one `FINDING KILL_SIGNAL_JOURNAL severity=warn` with `paths=unit_result_signal`, `count=0 process_sigkill=0 user_unit_signal=1 scope=user`, `attribution=none`; it does **not** claim signal 9 or SIGKILL (`SignalCoverage.md` §5.2: the general signal class remains a result-level fact, not a proven SIGKILL). `DRIFT1` with `drift=1`; `NOECHO`.
r13-before: **red** — r13 warns only on the `98e32220` unit-process SIGKILL record, not on `UNIT_RESULT=signal`. The landed gate's `R14_UNIT_SIGNAL_SYSTEM_INFO` covers the system-scope variant (routing info only, no KILL, CLEAN); it is not duplicated here.

**RF17 — `exit-code`, fleet system subject.**
```jsonl
{"__CURSOR":"s=r14rf-RF17-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"ufo-sighting.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `FLEET(system,1)`; no OOM; no `RUNK`; `CLEAN0`.
r13-before: **green** (negative control).

**RF18 — `resources`, non-fleet system subject.**
```jsonl
{"__CURSOR":"s=r14rf-RF18-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"bluetooth.service","UNIT_RESULT":"resources","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `NONFLEET(system,1)` `owner=tsukuroi`; no `FLEET`; no OOM; `CLEAN0`.
r13-before: **red** — fleet-shaped ID on a non-fleet unit.

**RF19 — `oom-kill` and `exit-code` mixed in one system slot (subset, not subtraction).**
```jsonl
{"__CURSOR":"s=r14rf-RF19-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"shokunin-fleet-fixture.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
{"__CURSOR":"s=r14rf-RF19-2","__REALTIME_TIMESTAMP":"1700000000000002","__MONOTONIC_TIMESTAMP":"1002","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"bluetooth.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `unit_failure_record=2`; `OOM1 OOMF(0,0,0,1)` (the oom subset is 1, never subtracted from 2); `FLEET(system,1)`; `NONFLEET(system,1)`; partition 1+1+0=2; `DRIFT1` with `drift=1`; class ok. To exercise the assignment's literal `failed` in a mixed slot, replace RF19-2's `UNIT_RESULT` with `failed`; the alarm fields and partition are unchanged, the routing stays non-fleet, and the landed selector keeps `unit_oom_result_unknown=0` (a string value).
r13-before: **red** — no OOM, no split.

**RF20 — `UNIT_RESULT` key absent, fleet user subject.**
```jsonl
{"__CURSOR":"s=r14rf-RF20-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"tmux-spawn-r14.service","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect no OOM; `unit_failure_record=1` (the count is untouched by the missing result); `FLEET(user,1)`; `RUNK(user,1)`; **no unlabeled zero**; `CLEAN0`.
r13-before: **red** on the unknown-result control; green on the raw count.

**RF21 — single-element result array (non-string).**
```jsonl
{"__CURSOR":"s=r14rf-RF21-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"pipewire-pulse.service","UNIT_RESULT":["oom-kill"],"MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect **no OOM** (an array is not the string `oom-kill`; no `tostring` smuggling); `RUNK(user,1)`; `NONFLEET(user,1)`; class ok; `CLEAN0`.
r13-before: **red** (no OOM, no route).

**RF22 — two-element result array `["failed","oom-kill"]` (ambiguous).**
```jsonl
{"__CURSOR":"s=r14rf-RF22-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"fleet-runner.service","UNIT_RESULT":["failed","oom-kill"],"MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect **no OOM** (must not pick one array element); `RUNK(system,1)`; `FLEET(system,1)`; `CLEAN0`.
r13-before: **red** on the unknown-result control.

**RF23 — empty-string result.**
```jsonl
{"__CURSOR":"s=r14rf-RF23-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"tmux-spawn-r14.service","UNIT_RESULT":"","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect no OOM; `FLEET(user,1)`; the landed selector is type-based and treats the empty string as a non-oom string, so `unit_oom_result_unknown=0` (no `RUNK`); `CLEAN0`.
r13-before: **green** on the alarm/route tuple (fleet ID matches; no resunk token expected for a string).

**RF24 — uppercase `OOM-KILL` (not the pinned literal).**
```jsonl
{"__CURSOR":"s=r14rf-RF24-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"pipewire-pulse.service","UNIT_RESULT":"OOM-KILL","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect **no OOM** (the comparison is exact); the landed selector treats the string as non-oom, so `unit_oom_result_unknown=0` (no `RUNK`); `NONFLEET(user,1)`; `CLEAN0`.
r13-before: **red** (no OOM is the only shared behavior; no route).

**RF25 — result-value injection canary.**
```jsonl
{"__CURSOR":"s=r14rf-RF25-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"pipewire-pulse.service","UNIT_RESULT":"oOm-kiLL-R14_RESULT_CANARY","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect no OOM; the landed selector treats the string as non-oom, so `unit_oom_result_unknown=0` (no `RUNK`); `NONFLEET(user,1)`; `CLEAN0`; `NOECHO` including `R14_RESULT_CANARY`. The raw result value is never printed; only a closed classification token is.
r13-before: **red** — non-fleet subject under the r13 fleet-shaped ID; no `owner=tsukuroi`.

## 6. Group C — subject selection and routing validity (non-OOM `exit-code`)

These cases isolate routing from the alarm. Every record is a valid `d9b373ed…` with a recognized non-OOM result.

**RF26 — emitter field contains a fleet token; subject is non-fleet.**
```jsonl
{"__CURSOR":"s=r14rf-RF26-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"kagi-shokunin.service","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"pipewire-pulse.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `NONFLEET(system,1)`; **no** `FLEET`; `CLEAN0`. Keying on `_SYSTEMD_UNIT` would invert this and repeat the r13 adjacency harm.
r13-before: **red**.

**RF27 — subject fleet, emitter plain (live shape).**
```jsonl
{"__CURSOR":"s=r14rf-RF27-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"tmux-spawn-r14.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `FLEET(user,1)`; no `NONFLEET`; `CLEAN0`. The live user-manager emitter is `user@1000.service`/`init.scope`; a subject-only rule must still find the fleet unit.
r13-before: **green** (fleet ID retained; negative control).

**RF28 — historical token matrix in both scopes (no summation).**
System slot `journal-system-unit_failure`:
```jsonl
{"__CURSOR":"s=r14rf-RF28-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"shokunin-watchdog.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
{"__CURSOR":"s=r14rf-RF28-2","__REALTIME_TIMESTAMP":"1700000000000002","__MONOTONIC_TIMESTAMP":"1002","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"ufo-sighting.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
{"__CURSOR":"s=r14rf-RF28-3","__REALTIME_TIMESTAMP":"1700000000000003","__MONOTONIC_TIMESTAMP":"1003","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"the-tick.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
{"__CURSOR":"s=r14rf-RF28-4","__REALTIME_TIMESTAMP":"1700000000000004","__MONOTONIC_TIMESTAMP":"1004","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"fleet-runner.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
{"__CURSOR":"s=r14rf-RF28-5","__REALTIME_TIMESTAMP":"1700000000000005","__MONOTONIC_TIMESTAMP":"1005","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"bluetooth.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
```
User slot `journal-user-unit_failure`:
```jsonl
{"__CURSOR":"s=r14rf-RF28u-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"tmux-spawn@r14.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `SURF(system; …,unit_failure_record=5)`, `SURF(user; …,unit_failure_record=1)`; `FLEET(system,4)`; `NONFLEET(system,1)`; `FLEET(user,1)`; no `count=5` on a fleet line, no `total=`, no summed 6; `CLEAN0`. The five tokens `shokunin`, `ufo-sighting`, `the-tick`, `fleet`, `tmux-spawn` are each exercised.
r13-before: **red** — r13 emits `UNIT_FAILURE_JOURNAL_SYSTEM count=5` and never the out-of-scope row.

**RF29 — escaped unit name (`\x2d`) is valid and non-fleet.**
```jsonl
{"__CURSOR":"s=r14rf-RF29-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"app-Hyprland-xdg\\x2dterminal\\x2dexec-dd9e67bd.scope","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `NONFLEET(user,1)`; **not** `UNATTR` — the backslash escape is legal in a unit name and must not be rejected by a naive grammar (`unit-name.c` escapes; live desktop scope shape). `CLEAN0`.
r13-before: **red** — fleet-shaped ID on a non-fleet unit.

**RF30 — byte-number array subject (unprintable value).**
```jsonl
{"__CURSOR":"s=r14rf-RF30-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":[107,97,103,105,45,115,104,111,107,117,110,105,110],"UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `UNATTR(system,1)` with `malformed=1`; `unit_failure_record=1` and class ok; no fleet/non-fleet; `CLEAN0`; no bytes echoed. The array decodes to a fleet-looking name, so treating it as a string would be a false fleet hit.
r13-before: **red**.

**RF31 — malformed subject string (space-separated canary).**
```jsonl
{"__CURSOR":"s=r14rf-RF31-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"R14_UNIT_CANARY not a unit","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `UNATTR(system,1)` with `malformed=1`; no fleet/non-fleet; `CLEAN0`; `NOECHO` including `R14_UNIT_CANARY`. A validated unit-name grammar is the landed rule (`^([A-Za-z0-9_.:@-]|\\x[0-9A-Fa-f]{2})+\\.(service|socket|device|mount|automount|swap|target|path|timer|slice|scope)$`, 1–255 bytes); the decisive point is that a space-containing string is not silently routed to tsukuroi as if it were a real desktop unit, and its bytes are never printed.
r13-before: **red**.

**RF32 — both subject fields, non-OOM.**
```jsonl
{"__CURSOR":"s=r14rf-RF32-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"shokunin-fleet-fixture.service","USER_UNIT":"pipewire-pulse.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `UNATTR(system,1)` with `ambiguous=1`; no fleet/non-fleet; `CLEAN0`. Scope is not resolved by "prefer the first field".
r13-before: **red**.

**RF33 — only `USER_UNIT` in the system file, non-OOM fleet (scope-field boundary).**
```jsonl
{"__CURSOR":"s=r14rf-RF33-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"tmux-spawn-r14.service","UNIT_RESULT":"exit-code","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `FLEET(system,1)` under the landed single-present-key rule; if that selector changes, `UNATTR(system,1)`. `CLEAN0`.
r13-before: **green** (fleet ID) or red under a strict scope rule.

## 7. Group D — generic SIGKILL records (retained warn, never OOM)

The generic SIGKILL record is `98e32220…` filtered exactly `EXIT_CODE=killed` and `EXIT_STATUS=9` (string or numeric 9). It is **not** an OOM record; a kernel OOM victim also exits on SIGKILL, so the finding must say cause unknown, not "not an OOM" (OomAttack CX4d). The delivered r13 warn severity is retained for the user scope only; the system scope remains info (`round-13-verifier-spotcheck.md:82`; `SignalCoverage.md` §1,§6).

**RF34 — user SIGKILL, fleet subject.**
Slot `journal-user-unit_sigkill`:
```jsonl
{"__CURSOR":"s=r14rf-RF34-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"98e322203f7a4ed290d09fe03c09fe15","USER_UNIT":"tmux-spawn-r14.service","EXIT_CODE":"killed","EXIT_STATUS":"9","COMMAND":"R14_COMMAND_CANARY","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `SURF(user; 0,0,0,0,1,0)`; exactly one `FINDING KILL_SIGNAL_JOURNAL severity=warn` with `paths=process_sigkill`, `count=1 process_sigkill=1 user_unit_signal=0 scope=user`, `attribution=none`; the note says cause unknown (a kernel OOM can also deliver SIGKILL); **no OOM line**; **no `UNIT_FAILURE_JOURNAL`/`OUT_OF_SCOPE`/`UNATTRIBUTED`** — the process-exit record is not a unit-failure record even though its subject contains a fleet token; `DRIFT1` with `drift=1`; `NOECHO`. Forbid the literal note `not an OOM` (false precision).
r13-before: **green** (retention control).

**RF35 — system SIGKILL, fleet subject.**
```jsonl
{"__CURSOR":"s=r14rf-RF35-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"98e322203f7a4ed290d09fe03c09fe15","UNIT":"shokunin-watchdog.service","EXIT_CODE":"killed","EXIT_STATUS":"9","COMMAND":"R14_COMMAND_CANARY","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `SURF(system; 0,0,0,0,1,0)`; `KILL_SIGNAL_JOURNAL_SYSTEM severity=info count=1 scope=system`; no OOM; no unit-failure route; `CLEAN0`; `NOECHO`.
r13-before: **green** (retention control).

**RF36 — SIGTERM status 15 is not counted as SIGKILL.**
```jsonl
{"__CURSOR":"s=r14rf-RF36-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"98e322203f7a4ed290d09fe03c09fe15","USER_UNIT":"tmux-spawn-r14.service","EXIT_CODE":"killed","EXIT_STATUS":"15","COMMAND":"R14_COMMAND_CANARY","MESSAGE":"R14_MESSAGE_CANARY"}
```
The stub must AND-filter `EXIT_CODE=killed EXIT_STATUS=9`, so this record is not returned for the SIGKILL query. Expect `unit_sigkill_record=0`; no `KILL_SIGNAL_JOURNAL`; no OOM; `CLEAN0`. This proves the filter is on the signal number, not just the `killed` word.
r13-before: **green** (retention control).

**RF37 — same record, stub bypass (defense in depth).**
If the gate supports a `bypass_match` slot flag, return the RF36 record even though it does not match. The delivered `JOURNAL_JQ_SIGKILL` `all(...)` predicate must then grade the class `unavailable:record-invalid`; no count, no warn, no OOM, `CLEAN0`. A count of 1 or a warn here means the SUT trusts the producer filter instead of validating the record.
r13-before: **green** (the r13 filter already refuses the class).

**RF38 — normal exit `0` is not SIGKILL.**
```jsonl
{"__CURSOR":"s=r14rf-RF38-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"98e322203f7a4ed290d09fe03c09fe15","USER_UNIT":"tmux-spawn-r14.service","EXIT_CODE":"exited","EXIT_STATUS":"0","COMMAND":"R14_COMMAND_CANARY","MESSAGE":"R14_MESSAGE_CANARY"}
```
Filtered out by the match words; `unit_sigkill_record=0`; no KILL; `CLEAN0`.
r13-before: **green**.

**RF39 — one unit, generic SIGKILL and `oom-kill` result (overlap is not a sum).**
Slot `journal-user-unit_sigkill`:
```jsonl
{"__CURSOR":"s=r14rf-RF39-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"98e322203f7a4ed290d09fe03c09fe15","USER_UNIT":"tmux-spawn-r14.service","EXIT_CODE":"killed","EXIT_STATUS":"9","COMMAND":"R14_COMMAND_CANARY","MESSAGE":"R14_MESSAGE_CANARY"}
```
Slot `journal-user-unit_failure`:
```jsonl
{"__CURSOR":"s=r14rf-RF39b-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"tmux-spawn-r14.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `SURF(user; 0,0,0,0,1,1)`; `OOM1 OOMF(0,0,1,0)` — the SIGKILL record does **not** add a second OOM line and does not increment `user_unit_oom`; `KILL_SIGNAL_JOURNAL warn paths=process_sigkill count=1 process_sigkill=1 user_unit_signal=0 scope=user`; `FLEET(user,1)`; `DRIFT1` with `drift=2` (OOM + KILL alarm classes); no `count=2` presented as a kill/victim total; `NOECHO`.
r13-before: **red** — r13 has KILL warn and the generic fleet info, but no OOM line and `drift=1`.

## 8. Group E — fan-out, controls and leak mode

**RF40 — one OOM-shaped incident across four planes (alarm versus counts).**
Slots:
`journal-user-kernel_oom`:
```jsonl
{"__CURSOR":"s=r14rf-RF40u1-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef","USER_UNIT":"pipewire-pulse.service","MESSAGE":"R14_MESSAGE_CANARY"}
```
`journal-system-kernel_oom`:
```jsonl
{"__CURSOR":"s=r14rf-RF40s1-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef","UNIT":"user@1000.service","MESSAGE":"R14_MESSAGE_CANARY"}
```
`journal-user-unit_failure`:
```jsonl
{"__CURSOR":"s=r14rf-RF40u2-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"pipewire-pulse.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
`journal-user-unit_sigkill`:
```jsonl
{"__CURSOR":"s=r14rf-RF40u3-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"98e322203f7a4ed290d09fe03c09fe15","USER_UNIT":"pipewire-pulse.service","EXIT_CODE":"killed","EXIT_STATUS":"9","COMMAND":"R14_COMMAND_CANARY","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `SURF(user; 1,0,0,0,1,1)`; `SURF(system; 1,0,0,0,0,0)`; `OOM1 OOMF(1,1,1,0)` — one line, four separate fields, no summed count and no sum of notice + result paths; `KILL_SIGNAL_JOURNAL warn paths=process_sigkill count=1 process_sigkill=1 user_unit_signal=0 scope=user`; `NONFLEET(user,1)` for the non-fleet service; no fleet claim; `DRIFT1` with `drift=2`; labels `unit=notice`/`unit=record`, `attribution=none`, `victims=unmeasured` (or equivalent); `NOECHO`. The system notice is a per-unit notice for `user@1000.service`, not a second victim; the service supplies a valid unit-failure result and a valid process-exit record, while a `.scope` would supply only the former.
r13-before: **red** — r13 has both notices INFO, the SIGKILL warn, a generic user failure INFO; no OOM line, no out-of-scope row.

**RF41 — empty streams are zero, not unavailable (CLEAN control).**
No records in any slot. Expect both `SURFACE journal.<scope>: ok`; all six counts `=0`; `boot=0123456789abcdef0123456789abcdef`; no journal findings; `CLEAN0` with `drift=0`.
r13-before: **green** (retention control).

**RF42 — legacy text only, no structured records.**
Fallback slot `$FX/stub/journal` contains the historical text; all six structured slots are empty:
```text
kernel: Out of memory: Killed process 4242 status=9/KILL
Failed with result 'oom-kill'
```
Expect no `OOM_KILL_JOURNAL`, no `KILL_SIGNAL_JOURNAL`, no `UNIT_FAILURE_*`; all counts 0; `CLEAN0`; `R14_MESSAGE_CANARY` absent. This pins the structured r13 delivered SUT (which never reads text) and forbids restoring a MESSAGE/text fallback. It is a no-restoration control, not evidence about the pre-r13 text probe.
r13-before: **green**.

**RF43 — leak mode: MESSAGE/COMMAND/unit bytes never reach output.**
Run RF01 and RF40 with a stub `leak` mode that forces the stored `MESSAGE` into the JSON even when `--output-fields` did not request it. Assert `NOECHO` on stdout **and** stderr, no `"MESSAGE":` substring, and no raw `UNIT_RESULT` payload (RF25). The counts and alarm tuples must remain exactly as in the honor-mode run; a leak-mode-only difference is a fixture-stub bug, not SUT behavior.
r13-before: **green** (the r13 census never requests MESSAGE; the leak mode is a guard, not a repair case).

**RF44 — missing result plus a positive kernel notice (alarm from the notice; no look-alike zero).**
`journal-user-kernel_oom`:
```jsonl
{"__CURSOR":"s=r14rf-RF44u1-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef","USER_UNIT":"run-p4175743-i29293759.scope","MESSAGE":"R14_MESSAGE_CANARY"}
```
`journal-user-unit_failure`:
```jsonl
{"__CURSOR":"s=r14rf-RF44u2-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"shokunin-fleet-fixture.service","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `OOM1 OOMF(1,0,0,0)` from the notice; `unit_failure_record=1`; `RUNK(user,1)`; `FLEET(user,1)`; `DRIFT1` with `drift=1`; `NOECHO`. The missing `UNIT_RESULT` must not be rendered as a bare `user_unit_oom=0` without the result-unknown counter, and it must not suppress the notice alarm.
r13-before: **red** (notice INFO, generic fleet ID, no OOM).

**RF45 — oom-kill results in both scopes: separate fields, no sum.**
`journal-system-unit_failure`:
```jsonl
{"__CURSOR":"s=r14rf-RF45s-1","__REALTIME_TIMESTAMP":"1700000000000001","__MONOTONIC_TIMESTAMP":"1001","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1","_UID":"0","_COMM":"systemd","_SYSTEMD_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT":"shokunin-fleet-fixture.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
`journal-user-unit_failure`:
```jsonl
{"__CURSOR":"s=r14rf-RF45u-1","__REALTIME_TIMESTAMP":"1700000000000002","__MONOTONIC_TIMESTAMP":"1002","_BOOT_ID":"0123456789abcdef0123456789abcdef","_TRANSPORT":"journal","_PID":"1234","_UID":"1000","_COMM":"systemd","_SYSTEMD_UNIT":"user@1000.service","_SYSTEMD_USER_UNIT":"init.scope","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","USER_UNIT":"pipewire-pulse.service","UNIT_RESULT":"oom-kill","MESSAGE":"R14_MESSAGE_CANARY"}
```
Expect `SURF(system; …,unit_failure_record=1)` and `SURF(user; …,unit_failure_record=1)`; `OOM1 OOMF(0,0,1,1)` — both unit-oom fields positive in their own fields, no `count=2`, no cross-scope sum; `FLEET(system,1)`; `NONFLEET(user,1)`; `DRIFT1`; `NOECHO`.
r13-before: **red**.

## 9. Invariants the gate must assert across all cases

1. **One alarm line.** `OOM1`: exactly one `FINDING OOM_KILL_JOURNAL` per run, `severity=crit`, no `_USER`/`_SYSTEM` sibling line that also alarms. `drift=` counts alarm classes, not records: OOM + SIGKILL = 2.
2. **No sums, no fake zeros.** The OOM line carries `user_notice`, `system_notice`, `user_unit_oom`, `system_unit_oom`; no `total=`/`sum=` and no `count=` that represents a cross-path/cross-scope sum; an unavailable source prints `unavailable:<reason>`, never `0`. Routing counts are per scope; no summed fleet/non-fleet/unattributed token.
3. **Partition.** For every ok unit-failure class: `fleet + nonfleet + unattributed = unit_failure_record`, per scope. The landed surface exposes the exact split as `unit_fleet`, `unit_nonfleet`, `unit_unknown`, `unit_missing`, `unit_ambiguous`, `unit_malformed`, `unit_oom`, `unit_oom_fleet`, `unit_oom_nonfleet`, `unit_oom_subject_unknown`, `unit_oom_result_unknown`, `unit_signal`; assert the deterministic buckets: `unit_fleet=1` in RF01/RF03/RF08/RF13/RF15–RF17/RF19/RF20/RF22/RF23/RF27/RF28/RF33/RF44/RF45; `unit_nonfleet=1` in RF02/RF04/RF14/RF18/RF21/RF24–RF26/RF29/RF40; `unit_oom_fleet=1` in RF01/RF03/RF08/RF19/RF45; `unit_oom_nonfleet=1` in RF02/RF04/RF40; `unit_oom_subject_unknown=1` in RF05–RF07/RF09/RF10; `unit_oom_result_unknown=1` in RF20–RF22/RF44. The `oom-kill` subset is ≤ `unit_failure_record` and is never subtracted from it.
4. **Count predicate unchanged.** `unit_failure_record` validity is `_BOOT_ID` string == expected boot and `MESSAGE_ID` == the catalog id. `UNIT_RESULT`, `UNIT`, `USER_UNIT` validity selects the routing/result buckets only; a malformed subject/result must not turn the class `record-invalid`. Query error, stderr bytes, malformed JSON, multi-boot, boot mismatch and timeout retain the r13 `unavailable:<reason>` grading.
5. **Six counters retained.** Both `SURFACE journal.user` and `journal.system` rows keep `kernel_oom_notice`, `oomd_notice`, `coredump_notice`, `segfault_signal11`, `unit_sigkill_record`, `unit_failure_record` in the delivered order and are never summed. `oomd_notice` alone stays info/CLEAN (no historical text alarm covered it).
6. **No bytes.** No `MESSAGE`, `COMMAND`, unit-name, raw `UNIT_RESULT`, or subject bytes are printed; only validated integers and closed classification tokens (`trust=client-supplied`, `attribution=none`, `victims=unmeasured`, `routing=unknown`/`owner=tsukuroi`).
7. **Exact enums.** Only the JSON string `"oom-kill"` increments the oom subset. Arrays, `null`, empty strings, case variants and arbitrary strings never do. A `signal` result is not SIGKILL. `failed` is not a pinned result literal.
8. **Subject selection.** Exactly one present string among `{UNIT,USER_UNIT}` selects the subject; both present or neither present is unknown; non-string (array/byte array/null) or an empty string is unknown; the legacy token set `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet` is applied case-insensitively as a substring to that subject only. Emitter fields (`_SYSTEMD_UNIT`, `_SYSTEMD_USER_UNIT`) are never classification input.
9. **Trust.** Findings carry `trust=client-supplied`; no emitter authentication, unique-victim, fleet-cause, or kill-count claim. A notice is a notice.
10. **Gate mechanics.** The frozen input is `.ufo/waves/round-14/frozen/mori-census.sh` (sha256 `39abda0a…3985`); the gate runs the same fixture bytes against the frozen and repaired censuses, asserts the frozen mismatch (exit 1) and repaired pass (exit 0), and `--selftest` exercises the gate's own parsing and fixture builder rather than the production census; report both the frozen-run mismatch count and the repaired-run pass count.

## 10. Red-before map against the frozen r13 census

“Red” means the frozen bytes at `.ufo/waves/round-14/frozen/mori-census.sh` cannot satisfy the expectation; “green” marks a retained control, not a repaired behavior.

| Cases | Frozen r13 output on the fixture | Before | Why |
|---|---|---|---|
| RF01–RF10 | `UNIT_FAILURE_JOURNAL(_SYSTEM) info count=1`, no OOM, CLEAN | red | alarm absent; result path unread (r13 requests only `_BOOT_ID,MESSAGE_ID`) |
| RF11–RF12 | `unit_failure_record=unavailable:boot-mismatch` / `rc-2`, no OOM | green | retained unavailable semantics |
| RF13, RF15, RF17 | generic fleet-shaped info, no OOM | green | negative controls; `failed`/`timeout`/`exit-code` strings are non-oom |
| RF16 | generic fleet info; no signal-result warn | red | `UNIT_RESULT=signal` KILL warn restored |
| RF14, RF18, RF26, RF29 | generic fleet-shaped ID on a non-fleet subject | red | missing tsukuroi route |
| RF19, RF39, RF40, RF44, RF45 | no OOM line; no out-of-scope row | red | alarm and split absent |
| RF20–RF22 | generic fleet-shaped ID; resunk counter absent | red | missing/non-string result discipline absent |
| RF23 | fleet ID info | green | empty string is non-oom under the type-based selector |
| RF24–RF25 | fleet-shaped ID on a non-fleet subject | red | missing tsukuroi route |
| RF27 | fleet ID | green | subject fleet; retained shape |
| RF28 | `UNIT_FAILURE_JOURNAL_SYSTEM count=5` | red | no split; count 5 instead of 4+1 |
| RF30–RF32 | fleet-shaped count on a malformed/ambiguous subject | red | no unknown bucket |
| RF33 | fleet ID (system) | green or red | depends on the pinned scope-field rule |
| RF34–RF35 | `KILL_SIGNAL_JOURNAL warn` / `_SYSTEM info` | green | retained SIGKILL controls |
| RF36, RF38 | `unit_sigkill_record=0` | green | retained filter controls |
| RF37 | `unavailable:record-invalid` | green | retained class validation |
| RF41 | all 12 counts 0, CLEAN | green | retained empty control |
| RF42 | no findings, CLEAN | green | structured SUT is text-blind by design |

The gate's overall frozen exit must be 1 because RF01–RF10, RF14, RF16, RF18–RF22, RF24–RF26, RF28–RF32 and RF39/RF40/RF44/RF45 are red. The retained green cases prevent the gate from “passing by accident” and prove the repair did not trade away existing behavior.

### 10.1 Red-required cases per mutation hook

| Mutation | Cases that must fail the mutant |
|---|---|
| Demote `OOM_KILL_JOURNAL crit` to info | RF01, RF03, RF05, RF07, RF10, RF40, RF45 (severity and roll) |
| Drop the `UNIT_RESULT=oom-kill` path (notice-only alarm) | RF01–RF05, RF19, RF39, RF40, RF45 |
| Fold subject/result validity into the class `all()` predicate | RF05–RF10, RF44 |
| Collapse the fleet/non-fleet partition or omit `owner=tsukuroi` | RF02, RF04, RF14, RF18, RF26, RF28, RF29, RF30–RF32 |
| Route `failed`/array/uppercase as oom-kill | RF13, RF21, RF22, RF24 |
| Treat a user `UNIT_RESULT=signal` as non-alarm or as oom-kill | RF16 |
| Subtract the oom subset from `unit_failure_record` | RF19, RF39, RF45 |
| Emit one OOM line per scope or per path | RF40, RF45 |
| Echo subject/result bytes or MESSAGE/COMMAND | RF25, RF31, RF43 |
| Treat a generic SIGKILL record as OOM or as a unit failure | RF34, RF35, RF39 |
| Count SIGTERM/normal exit as SIGKILL | RF36, RF38 |

## 11. Integration notes for `tools/mori-round14-regressions.py`

1. **Stub filter (must).** Implement the generic AND matcher in §2.3. A `MESSAGE_ID`-only stub is the single most likely cause of a false `record-invalid` for a second `UNIT_RESULT=oom-kill` query and of a false green for a mixed slot (`OomAttack.md` CX7; `CounterAttack.md` CX3).
2. **Pin the landed tokens.** The repair landed while this report was being written; its `probe_journal` now emits one unsuffixed `OOM_KILL_JOURNAL crit` with `paths=`, `user_notice`, `system_notice`, `user_unit_oom`, `system_unit_oom` and the two `*_unit_oom_result_unknown` fields; `UNIT_FAILURE_JOURNAL(_SYSTEM) info` with `subject=fleet owner=mori`; `UNIT_FAILURE_OUT_OF_SCOPE(_SYSTEM) info owner=tsukuroi`; one `UNIT_FAILURE_UNATTRIBUTED_JOURNAL info` with `missing`/`ambiguous`/`malformed` subcounts; and `KILL_SIGNAL_JOURNAL warn` with `paths=process_sigkill` and/or `paths=unit_result_signal`, `count`, `process_sigkill`, `user_unit_signal`. Pin the gate to these delivered tokens. The earlier per-scope OOM/attribution IDs quoted in the draft reports were not delivered; if the bytes change again, report the divergence to L1 rather than weakening the fixture.
3. **`DRIFT_COUNTER_KEYS`.** The landed repair already registers the new tokens (`user_notice`, `system_notice`, `user_unit_oom`, `system_unit_oom`, `*_unit_oom_result_unknown`, `unit_oom*`, `unit_fleet`, `unit_nonfleet`, `unit_unknown`, `unit_missing`, `unit_ambiguous`, `unit_malformed`, `unit_signal`, `process_sigkill`, `user_unit_signal`) in `DRIFT_COUNTER_KEYS` (`tools/mori-census.sh:2248-2267`). Verify they remain registered; a `--drift` run must not report a count field change on a stable fixture. Prefixed keys (`user_kernel_oom_notice=`) do not match the registered `\bkernel_oom_notice` regex; do not rely on them for the mask.
4. **Do not tighten the alarm by subject.** RF05–RF10 and RF44 fail if the implementation folds subject/result validity into the class `all()` predicate. The class count and the alarm must survive malformed metadata.
5. **Do not demote for non-fleet.** RF02/RF04 prove the OOM alarm fires for a non-fleet subject; the same record still routes to tsukuroi. This is a coherent alarm, not a duplicate count (CounterAttack §5 open note).
6. **`oomd_notice` alone is not an alarm.** RF40 exercises the kernel-notice path and does not use `d989611b`; a separate `d989611b`-only fixture must stay info/CLEAN (OomAttack OA14). Do not add an oomd alarm while fixing the kernel/result paths.
7. **Text mode disclosure.** The header-only non-JSON mode is deliberate and matches the r13 harness. State in the gate report that red-before is structural (frozen structured SUT cannot see structured-only records), while the historical text alarm is evidenced by the frozen source and the spotcheck, not re-measured here.
8. **Case mapping.** RF01–RF12 map to OomAttack OA03–OA05/OA10/OA13 and CounterAttack P09/P11; RF13–RF19 map to OA09/OA17 and P07/P09; RF20–RF25 are the result-class extension; RF26–RF33 map to RoutingAttack §4.1–4.5 and P07/P08; RF34–RF39 map to OA06 and MutationDesign's `R14_C1_SIGKILL_NOT_OOM`; RF40–RF45 are independent fan-out/control additions (RF45 is the both-scope result no-sum case).

## 12. Boundaries and risks

- **Alarm ≠ victim ≠ cause.** `fe6faa94`, `d989611b` and `d9b373ed` are notices/records; none identifies a unique victim or proves fleet causation. The fixtures require `attribution=none`/`victims=unmeasured`; a gate that accepts `count=1` as “one kill” would be wrong.
- **Client-set trust.** `MESSAGE_ID`, `UNIT_RESULT`, `UNIT`, `USER_UNIT` are non-underscore fields; only `_BOOT_ID` is the trusted anchor used here. The routing is a name-token heuristic, not an authenticated fleet-membership proof. Keep `trust=client-supplied`.
- **Substring predicate.** The historical rule is case-insensitive, unanchored substring (`frozen/mori-census.sh:891`). Mirroring it preserves false positives such as `fleetwood-…` or `…com.jetbrains.Fleet…`. Do not silently tighten to token boundaries without its own evidence; do label `non-fleet` as “no fleet token”, not “proven desktop/OS”. The `fleetwood` boundary is intentionally **not** a gating case here.
- **Case sensitivity.** The mirror is `-i`; a mixed-case subject containing `UFo-SiGhTiNg` is fleet under the historical rule. This report does not make that a gating case; pin it with L1 if needed.
- **Scope-field coupling.** The landed selector counts the present keys and uses `.UNIT // .USER_UNIT`; RF08/RF33 pin that single-present-key rule because system-file user-manager records are source-possible. If L1 changes it to strict `system→UNIT, user→USER_UNIT`, those two cases flip to unattributed; do not leave both rules in the gate.
- **`UNIT_RESULT=signal`.** The landed repair restores the historical `Failed with result 'signal'` path as a user `KILL_SIGNAL_JOURNAL warn` with separate `process_sigkill`/`user_unit_signal` counters and `attribution=none`. It does **not** prove signal 9 or SIGKILL; the result-level fact is honest, and RF16 pins it. If L1 rejects the restoration, RF16 must migrate with its own severity ruling; do not silently drop it from the gate.
- **`failed` is not source-valid.** The assignment's `UNIT_RESULT=failed` case is exercised as an unrecognized client-set value (RF13/RF14). A gate that assumes `failed` is a pinned enum would overstate source validation.
- **No live measurement.** No host journal, systemd unit inventory, census, gate or selftest was read/run here. The payloads are synthetic and boot-pinned; they do not prove any live host has or lacks these records.

## 13. Tooling and provenance

- **Tools installed/updated:** none. No package, `uv`, `cargo`, npm or binary install was attempted.
- **Read-only fetches:** pinned systemd at `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` was fetched with `curl` into `/tmp/sdpin` for source anchors (`catalog/systemd.catalog.in` sha256 `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592`; `src/core/unit.c`, `src/core/unit.h`, `src/core/service.c`, `src/core/scope.c`, `src/core/cgroup.c`, `src/shared/logs-show.c`, `man/systemd.journal-fields.xml`). Nothing was installed and nothing outside `/tmp` and this report was written.
- **Lane reads:** `tools/mori-census.sh` (`:887-1130`, `:1995-2006`, `:2255-2345`, `:2738-2858`) before the repair landed, then the landed `probe_journal` (`:1000-1400`, `:2248-2267`) and its r14 selftest cases (`:3003-3180`) after CensusRepair wrote them; `.ufo/waves/round-13/frozen/mori-census.sh` (`:847-912`), `tools/mori-round13-regressions.py` (`:100-150`, `:429-700`), `corpus/lessons/round-13-verifier-spotcheck.md`, `corpus/knowledge/structured-journal-scopes-r13.md`, `corpus/SOURCES.md`, `.ufo/waves/round-14/scoped-counter-contract.json`, `.ufo/waves/round-14/frozen/expected.json`, and the peer reports `OomAttack.md`, `RoutingAttack.md`, `SignalCoverage.md`, `JournalFields.md`, `FleetPredicate.md`, `CounterAttack.md`, `MutationDesign.md`.
- **LSP:** not used; this is a shell/Python-toolchain lane with no project language server, and all symbol locations were resolved by direct source reads and `grep`. No cold LSP response is claimed as absence.
- **Verification not run:** no census/gate/selftest/regression command, no `--selftest`, no live journal query. The only validation performed was JSON parsing of this report's payload lines during authoring (all 53 records parse as JSON objects).
