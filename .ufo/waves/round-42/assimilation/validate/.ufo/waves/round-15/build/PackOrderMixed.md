# PackOrderMixed — round-15 fixture pack for record-order stability

Seat: `MoriR15.PackOrderMixed` (executor, leaf).
Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Axis judged: **coverage**. Secondary axis: **operability** (the harness must be able to
select the right stub mode without a per-case schema deviation).
Milestone: retain validated positives without fabricated totals.

## 1. Write scope and result

Wrote exactly two files:

| file | sha256 | role |
|---|---|---|
| `.ufo/waves/round-15/fixtures/OrderMixed.json` | see §1.1 | the assigned fixture pack |
| `.ufo/waves/round-15/build/PackOrderMixed.md` | this report | advisory findings |

No production file, harness, frozen input, manifest, sibling pack, SHONEN/verifier or
aggregator was edited. No commit, build, test, gate, selftest, census, oracle or fixture
execution was performed. No tool was installed or upgraded.

### 1.1 Pack identity and shape

- Pack: 4 cases, JSON top-level list. Every case has exactly the shared keys
  `id, user, system, want_oom, want_signal, invalid_class`; no `mode`, no `expect`, no
  extra keys.
- Every record is a JSON object with no `MESSAGE` key and no canary string. Every
  `_BOOT_ID` is the shared current boot `11111111111111111111111111111111`.
- All ids are globally unique in `.ufo/waves/round-15/fixtures/*.json` at the time of
  writing (`order-` prefix; `jq -r '.[].id' fixtures/*.json | sort | uniq -d` printed
  nothing).
- Static JSON validity check: `jq -e 'type=="array" and length==4'` passed.

Static hash of the pack as written (unchanged after this report):

```
5a054dc6b1056ee1fef838a6ee63d5e61a057a36636d5472b352116c1c432d4e  .ufo/waves/round-15/fixtures/OrderMixed.json
```

## 2. The edge this pack covers

The same mixed record sequence, reversed and duplicated, must produce the same alarm
outcome:

- A valid current-boot kernel OOM record and a valid current-boot unit `oom-kill`
  record remain individually valid evidence.
- An adjacent record that is not a valid instance of the queried class — a
  `MESSAGE_ID` array or a malformed process status — invalidates the **raw aggregate
  class** (`record-invalid`), never the individual positive evidence.
- The critical `OOM_KILL_JOURNAL` line fires exactly once if any positive OOM record
  exists; the user `KILL_SIGNAL_JOURNAL` warn fires exactly once if any positive
  user unit-signal or process-sigkill record exists.
- Positive counts are per scope and are never summed. Raw counts keep their existing
  `unavailable:<reason>` semantics when the aggregate is invalid.
- Duplicate records change the positive **count** (record evidence, not unique
  victims) but not the number of alarm **lines**.

This pack does not claim completeness, authenticated ids, unique victims, a repaired
parser, or any routing from positive records. The fleet/non-fleet/unknown split stays
aggregate-only and unavailable on an invalid stream.

## 3. Stub behavior: why a filter-bypassing mode is required

Source read: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round14-regressions.py`
(function `journal_stub_body`; read-time snapshot `533218a5…47e4ef`). The file was
under active sibling edit, so anchor by function name, not by a frozen line number.

- `journal_stub_body` docs the modes: `honor` applies every `FIELD=value` match word as
  an AND filter; `ignore-filters` returns every record of the scope regardless of
  filters; `dup-kernel` ignores filters only when the argv contains
  `MESSAGE_ID=fe6faa94…` (a mixed valid + malformed-MESSAGE_ID kernel stream).
- In `honor` mode the stub loop `if str(rec.get(k)) != v: ok = False` drops a
  nonmatching or `MESSAGE_ID`-array record **before the census sees it**. A fixture run
  under `honor` would leave the aggregate valid and would not exercise this round's
  claim at all.
- `ignore = MODE == "ignore-filters"` skips that filter block entirely, so every class
  query for a scope receives **every** record of that scope. It is the only generic
  r14 mode that can deliver a heterogeneous mixed stream to
  `unit_failure_record` and `unit_sigkill_record`.
- `dup-kernel` is narrower: only the kernel `MESSAGE_ID` query ignores argv filters.
  It delivers a mixed kernel stream while every other class query keeps exact-filter
  semantics (and therefore keeps its own raw count valid when its records match).
- `build_fixture(base, case)` writes `<scope>.records` and installs the stub with
  `journal_stub_body(base, case.mode)`, so the r15 loader sets the mode on the
  constructed `Case`.

**Needed harness setting — read from the landed loader, not assumed.** The IRC from
`MoriR15.HarnessBuild` (2026-10-20) first said "non-null `invalid_class` ⇒
`ignore-filters`", but the loader that landed special-cases kernel OOM:

```python
def mode_for(invalid_cls, capture):
    if invalid_cls is None: return "honor"
    if invalid_cls == "kernel_oom_notice": return "dup-kernel"
    return "ignore-filters"
```

(`tools/mori-round15-regressions.py:486-493`, read-time snapshot `f349c8d3…0261d`.)
The landed loader is authoritative; the expectations in §4 follow it:

1. `invalid_class == null` ⇒ `honor`.
2. `invalid_class == "kernel_oom_notice"` ⇒ `dup-kernel`: the user kernel aggregate is
   invalid, while the unit/process/notice class queries keep exact filtering and their
   raw counts. In the system scope a homogeneous valid kernel record stays a valid
   raw count of 1.
3. Any other non-null `invalid_class` ⇒ `ignore-filters`: every class query in the
   affected scope sees the whole stream, so all six raw classes there become
   `unavailable:record-invalid`. Only the named class is asserted (plus positives and
   alarms); collateral raw invalidation is not graded.
4. Derive the affected scope by scanning each scope for a record that fails the named
   class's strict predicate. Assert aggregate unavailability only in that scope, for
   that class.
5. Compute the expected positive tokens from the fixture and require them on
   `SURFACE journal.user` / `journal.system` for the SUT profile, including when the
   named aggregate is unavailable.
6. `want_oom` / `want_signal` are existence semantics over individually valid records,
   independent of raw availability.

Consequence for the two kernel cases: `dup-kernel` does **not** degrade the sibling
raw classes in the user scope. The unit `oom-kill` record keeps
`unit_failure_record=1` and `unit_oom=1`, and the system kernel record keeps
`kernel_oom_notice=1`. For the two signal/process cases (`ignore-filters`) every raw
class in the user scope is `unavailable:record-invalid`; that collateral invalidation
is expected and must not be asserted as a product failure.

## 4. Cases and exact static expectations

Records are listed in file order. `K` = `fe6faa94e7774663a0da52717891d8ef`,
`U` = `d9b373ed55a64feb8242e02dbe79a49c`,
`S` = `98e322203f7a4ed290d09fe03c09fe15`, boot `B` =
`11111111111111111111111111111111`.

### 4.1 `order-kernel-forward-unit-oom-mixed`

user: `K` valid → `K` as `MESSAGE_ID:[K]` → `U` + `USER_UNIT=shokunin-fixture.service` +
`UNIT_RESULT="oom-kill"`. system: one `K` valid.
`want_oom=true`, `want_signal=false`, `invalid_class="kernel_oom_notice"`.

| scope | positive expected | raw expected |
|---|---|---|
| user | `positive_kernel_oom=1`, `positive_unit_oom=1`, `positive_unit_signal=0`, `positive_process_sigkill=0` | `kernel_oom_notice=unavailable:record-invalid`; `unit_failure_record=1` (raw unit query stays exact-filtered under `dup-kernel`), `unit_oom=1`, `unit_signal=0`, `unit_fleet=1`; the notice/sigsegv/process classes stay `ok` at `0` |
| system | `positive_kernel_oom=1`, others `0` | `kernel_oom_notice=1`; every other raw class `0` (the homogeneous kernel record is not returned to their exact-filtered queries) |

Alarms: exactly one `FINDING OOM_KILL_JOURNAL severity=crit`, with no summed `count=`;
its `user_notice` field byte-equals `user:kernel_oom_notice=unavailable:record-invalid`,
`user_unit_oom=1`, `system_notice=1`, `system_unit_oom=0`, and its positive fields
byte-equal the SURFACE positives above. No `KILL_SIGNAL_JOURNAL`; no second OOM line.
Drift 1. The valid raw unit class also emits one `UNIT_FAILURE_JOURNAL info count=1
subject=fleet owner=mori scope=user` routing line; it is info and does not flip the
roll. No routing line is invented for the invalid kernel class.

### 4.2 `order-kernel-reversed-unit-oom-mixed`

Exactly the records of 4.1 with the user sequence reversed:
`U` oom-kill valid → `K` as `MESSAGE_ID:[K]` → `K` valid. system: one `K` valid.
Same booleans and `invalid_class`.

Expected surface and alarm literals are **identical** to 4.1. This is the order-
independence arm: reversing the stream changes neither the positive counts nor the
alarm count.

### 4.3 `order-unit-signal-duplicated-array-poison`

user: `U` + fleet subject + `UNIT_RESULT="signal"` → the same record again with a
distinct cursor/timestamp (two valid records, not a byte-identical line) → `U` as
`MESSAGE_ID:[U]` + fleet subject + `UNIT_RESULT="signal"` (deliberately carries a
would-be-valid result string; the array id must exclude it).
system: empty.
`want_oom=false`, `want_signal=true`, `invalid_class="unit_failure_record"`.

| scope | positive expected | raw expected |
|---|---|---|
| user | `positive_unit_signal=2`, `positive_kernel_oom=0`, `positive_unit_oom=0`, `positive_process_sigkill=0` | all six raw class tokens `unavailable:record-invalid`; `unit_failure_record=unavailable:record-invalid` |
| system | all four positive tokens `0` | all six raw counts `0`, state `ok` |

Alarms: exactly one `FINDING KILL_SIGNAL_JOURNAL severity=warn`; no `OOM_KILL_JOURNAL`.
Drift 1. No unit routing line (raw split unavailable). The poison record must not make
`positive_unit_signal` 3: it has a non-scalar `MESSAGE_ID`.

### 4.4 `order-process-sigkill-duplicated-status-array-poison`

user: `S` + `EXIT_CODE="killed"` + `EXIT_STATUS="9"` → the same record again with a
distinct cursor/timestamp → `S` + `EXIT_CODE="killed"` + `EXIT_STATUS:["9"]` (scalar id,
non-scalar status; a naive status reader would count it).
system: empty.
`want_oom=false`, `want_signal=true`, `invalid_class="unit_sigkill_record"`.

| scope | positive expected | raw expected |
|---|---|---|
| user | `positive_process_sigkill=2`, `positive_kernel_oom=0`, `positive_unit_oom=0`, `positive_unit_signal=0` | all six raw class tokens `unavailable:record-invalid`; `unit_sigkill_record=unavailable:record-invalid` |
| system | all four positive tokens `0` | all six raw counts `0`, state `ok` |

Alarms: exactly one `FINDING KILL_SIGNAL_JOURNAL severity=warn`; no `OOM_KILL_JOURNAL`.
Drift 1. The array-status record must not make `positive_process_sigkill` 3.

## 5. Independent derivation of the literals

I derived the positive matrix from the pack itself, not from the SUT, with a read-only
`jq` expression over `fixtures/OrderMixed.json` implementing the shared selector:
object, scalar `_BOOT_ID` equal to `B`, scalar `MESSAGE_ID` equal to the class id, then
`UNIT_RESULT == "oom-kill"` / `"signal"` for unit records and
`EXIT_CODE == "killed"` and scalar status 9 for process records. Result:

```
order-kernel-forward-unit-oom-mixed          user K=1 Uoom=1 Usig=0 P=0  system K=1 Uoom=0
order-kernel-reversed-unit-oom-mixed         user K=1 Uoom=1 Usig=0 P=0  system K=1 Uoom=0
order-unit-signal-duplicated-array-poison    user K=0 Uoom=0 Usig=2 P=0  system K=0 Uoom=0
order-process-sigkill-duplicated-status...   user K=0 Uoom=0 Usig=0 P=2  system K=0 Uoom=0
```

This matches the production selectors read in `tools/mori-census.sh`
(read-time snapshot `280ef5da…e5f44`; the file was under active sibling edit):

- `JOURNAL_JQ_POS_BASE` requires object, scalar-string `_BOOT_ID == $boot`,
  scalar-string `MESSAGE_ID == $id`;
- `JOURNAL_JQ_POS_KERNEL` counts those records;
- `JOURNAL_JQ_POS_UNIT` requires `UNIT_RESULT` to be exactly the string
  `oom-kill` or `signal`;
- `JOURNAL_JQ_POS_SIGKILL` accepts scalar string `"9"` or number `9`, rejecting
  arrays, null and booleans;
- `journal_positive_scan` runs over the **same** captured stream only after a
  semantic aggregate failure, and stays empty/unavailable on capture or parser
  failure;
- `journal_pos` maps a healthy aggregate's raw/split count to the positive token, so a
  valid homogeneous class still reports a positive count;
- SURFACE tokens are emitted as `positive_kernel_oom=`, `positive_unit_oom=`,
  `positive_unit_signal=`, `positive_process_sigkill=`, and the alarm lines carry
  scope-prefixed `user_positive_*` / `system_positive_*` fields that byte-equal those
  surface tokens.

No second journal query is needed by the fixture or by the expected literals.

## 6. Evidence read (author anchors)

Read-time snapshots: r14 helper `533218a5…47e4ef`, census `280ef5da…e5f44`,
r15 loader `f349c8d3…0261d`. All three were under active sibling edit; function names
are the durable anchors.

- `tools/mori-round14-regressions.py`, `journal_stub_body` — stub modes and the
  honor/`ignore-filters`/`dup-kernel` difference.
- `tools/mori-round14-regressions.py`, `build_fixture` — writes `<scope>.records` and
  installs the stub with the case mode.
- `tools/mori-census.sh`, `JOURNAL_JQ_MSGID` / `JOURNAL_JQ_SIGKILL` — all-or-nothing
  aggregate filters.
- `tools/mori-census.sh`, `JOURNAL_JQ_UNITS` — unit aggregate/predicate
  (`MESSAGE_ID == $id` only; unit result shape is not record-poison).
- `tools/mori-census.sh`, r15 positive contract comment — tokens, alarms,
  unavailable-on-capture, no routing.
- `tools/mori-census.sh`, `JOURNAL_JQ_POS_BASE` / `_KERNEL` / `_UNIT` / `_SIGKILL` —
  positive jq selectors.
- `tools/mori-census.sh`, `journal_positive_scan` — same captured bytes, semantic
  failures only.
- `tools/mori-census.sh`, `journal_pos` and the SURFACE emitter — healthy-aggregate
  mapping and `positive_*` tokens.
- `tools/mori-census.sh`, OOM and KILL_SIGNAL emit blocks — scope-prefixed positive
  evidence fields.
- `tools/mori-round15-regressions.py`, `mode_for`, `record_matches`,
  `derive_unavailable`, `count_positives` — landed loader semantics used in §3/§4.
- Existing fixture conventions: `fixtures/KernelSystem.json`, `fixtures/ProcessUser.json`,
  `fixtures/FanoutPositive.json`, `fixtures/CrossScope.json`.
- Harness owner convention: IRC from `MoriR15.HarnessBuild`, 2026-10-20, superseded for
  kernel cases by the landed `mode_for` code cited in §3.

Snapshot note: `tools/mori-census.sh`, `tools/mori-round14-regressions.py` and
`tools/mori-round15-regressions.py` were under active sibling edit while this pack was
written. At the final read the positive selectors, the same-stream scan, the
healthy-aggregate mapping, the SURFACE tokens and the alarm consumption were all
present. I traced this pack statically through the landed loader functions
`mode_for`, `record_matches`, `derive_unavailable` and `count_positives`: all four cases
parse under the allowed-key/id rules, every `invalid_class` names a record that actually
fails that class predicate, and the `want_*` flags agree with the independently counted
positives. That was a source-read trace, not an execution. The pack's expected literals
are independent of the implementation state; no execution was performed here and the
harness gate remains unrun by this seat.

## 7. Risks and integration conditions

1. **Stub mode is load-bearing.** If the r15 gate loads this pack under `honor`, the
   malformed/nonmatching records are filtered out and every case becomes a valid
   homogeneous stream; the gate may then pass without testing C1, or fail because
   `invalid_class` is not unavailable. The landed loader must keep its derived mapping
   (`kernel_oom_notice` ⇒ `dup-kernel`; other non-null ⇒ `ignore-filters`; null ⇒
   `honor`). A blanket `ignore-filters` would also work for the kernel cases but would
   make the expected sibling raw counts in §4.1/4.2 wrong; a blanket `honor` defeats
   every case.
2. **Raw expectations differ by mode.** In cases 4.1/4.2 (`dup-kernel`) only the user
   `kernel_oom_notice` aggregate is invalid; the unit raw class stays `ok=1` and the
   system kernel raw stays `ok=1`. Do not assert all six user raws unavailable there.
   In cases 4.3/4.4 (`ignore-filters`) all six user raws are
   `unavailable:record-invalid`; that collateral invalidation is expected and only the
   named class is graded. Never assert a sibling raw class that the selected stub mode
   degrades.
3. **Duplicates are intentional records, not duplicate lines.** Each repeated positive
   has a distinct `__CURSOR`/timestamp. A loader or SUT that dedupes by cursor would
   report positive 1 instead of 2. Production counts captured records with
   `jq ... | length`, and the expected literals are 2. Do not dedupe.
4. **Poison records are adversarial in the useful direction.** The unit poison carries
   `UNIT_RESULT="signal"` with an array `MESSAGE_ID`; the process poison carries a
   scalar id with `EXIT_STATUS:["9"]`; the kernel poison carries a current boot and the
   kernel id inside an array. A positive selector that drops the scalar-id or scalar-
   status requirement will overcount and turn the gate red. That is the intended
   discrimination.
5. **Positive token names are per scope on the SURFACE rows.** The literals in §4 are
   scope-local. There is no cross-scope positive sum and no alarm `count=` derived from
   positives.
6. **Implementation timing.** At the final read the positive selectors, same-stream
   scan, healthy-class mapping, SURFACE tokens and alarm consumption were all present
   in `tools/mori-census.sh`; sibling files were still changing. These packs were not
   executed and this report does not claim a green. If a later census revision drops a
   positive token or changes a selector, the expected literals in §4 remain the
   contract and the gate should fail.
7. **Capture failure is not representable in this schema.** Per `ReviewHarnessPacks`
   F1, these records are all valid JSON objects; non-JSON capture, rc, stderr and
   timeout remain harness-stub coverage, not pack coverage.
8. **Frozen-control roles.** Cases 4.1/4.2 are intentionally **non-red**: their OOM
   alarm also has raw sources outside the invalid kernel class (`user unit_oom=1`,
   `system_notice=1`), so the entering frozen census should pass them (one OOM crit,
   DRIFT 1). Cases 4.3/4.4 are **red-relevant**: the only signal trigger is the
   positive record in a class the named `invalid_class` makes unavailable, so the
   frozen census must miss the `KILL_SIGNAL_JOURNAL` warn and the gate must count it
   red-confirmed. If the harness instead reports 4.1/4.2 as red, the mode/expectation
   mapping has drifted from the landed `mode_for`/`derive_unavailable` code.

## 8. Tool installs

None. No package operation was run. The parent host-safety notice was received before
any install decision; this seat needed no tool.
