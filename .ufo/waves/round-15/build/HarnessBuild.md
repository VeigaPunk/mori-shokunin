# HarnessBuild — round-15 C1 fixture gate

Status: implementation complete, then revised for the L1 blocking review
(ReviewHarnessGate F1–F8). No production census, fixture-pack gate run, build,
lint, formatter or smoke run was performed by this seat, and no verification was
run after the F1–F8 edits per L1 instruction. This report and
`tools/mori-round15-regressions.py` are the only write-scope outputs. Earlier
`--selftest` runs (before the F1–F8 edits) executed isolated wrapper processes
only; they never executed `tools/mori-census.sh` or a fixture pack. The revised
selftest intentionally runs the real pinned frozen census against synthetic
mini-fixtures; that revised path has not been executed by this seat.

## Post-review fixes (F1–F8)

| Item | Fix |
|---|---|
| F1 | `classify_control` confirms a red-relevant frozen run only when it completed, had no timeout/exec error/integrity reason, emitted at most one OOM and one WARN with no alarm for an unwanted arm, had actual drift equal to the actual alarm count, had actual rc/word consistent with that count, and specifically missed at least one wanted alarm arm (`oom_lines=0` / `kill_lines=0`). A retained wanted arm is allowed. Any other frozen failure is `control_inconclusive`; unexpected frozen alarm is `unexpected_pass`; both exit 2. |
| F2 | CLI `--selftest-child` and `--no-frozen-control` are deleted. A run always executes the pinned frozen control; there is no exit-0 bypass. Selftest calls the normal gate (full pinned frozen control) on isolated synthetic fixtures. A helper-level `classify_control` check covers frozen exec-error/timeout/integrity/alarm-specific cases without executing census. |
| F3 | Capture rc 124/137 now expects `unavailable:timeout`, matching the census producer-timeout mapping. |
| F4 | `revision.stable`/`status_changed` compare only observed `rev-parse HEAD` plus dirty paths outside the harness output. Full paths and content digests remain separate receipts. |
| F5 | Output guard now refuses an output that covers/equals the frozen file, frozen directory, fixtures, expected file, repo root, tools/.git/corpus, or a declared extra input; it refuses a symlinked output root and symlinked `fixtures/`, `targets/`, `runs/` before writes; a symlinked case fixture root is refused before `rmtree`. |
| F6 | The r14 helper is read once, hashed from those bytes, and executed via `compile`/`exec` into a registered module; no SourceFileLoader or `__pycache__` path. The gate's own bytes are read once for the expected-table pin and re-read only for moving-input detection. |
| F7 | `resolve_frozen` catches only git materialization failure; `SnapshotTampered` from the git blob or on-disk cross-check propagates with exit 2. |
| F8 | Status 9 accepts only integer `9` or string `"9"`; bool/float/null/array/object are rejected, matching the r14 stub's `str()` filter. |

## Files

| Path | Change |
|---|---|
| `tools/mori-round15-regressions.py` | New isolated r15 fixture-pack gate (post-review final SHA-256 `31e8e17a51684c738110078639418d97acd90867f51d017af9e45c21f2d03d27`). |
| `.ufo/waves/round-15/build/HarnessBuild.md` | This report. |

Not modified: `tools/mori-census.sh`, `tools/mori-round14-regressions.py`,
SKILL/index/corpus/fleet/verifier/aggregator files, every fixture pack, and the
frozen directory. No commits, pushes, installs or upgrades.

## Gate contract

Reuses the r14 helper module through importlib (`build_fixture`, `census_env`,
`Case`, `verdict_roll`, `surface_rows`, `findings`, `read_argv_log`,
`message_argv_violations`). No copied harness. The helper file is hashed before
and after import and at end; its SHA-256 is a verdict-driving pin in the
expected table. Import bytecode writing is suppressed.

CLI:

```
python3 tools/mori-round15-regressions.py \
  --census PATH                 # default tools/mori-census.sh
  --fixtures DIR                # default .ufo/waves/round-15/fixtures
  --expected PATH               # default .ufo/waves/round-15/expected.json
  --output DIR                  # required for a run
  --frozen PATH                 # optional override; must match the pin
  --pin-fixtures PATH           # generate/refresh the expected table
  --case ID[,ID...]             # diagnostic subset
  --timeout SECONDS             # default 120 per census run
```

There is no CLI control bypass: every normal run executes the pinned frozen
control for every selected case. `--selftest` is the only mode that does not
take `--output`/`--pin-fixtures`.

Pins:

- frozen entering census SHA-256
  `0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9`
- base commit `0fa5e0de194bcc270a927a166664113e6821442b` (`0fa5e0d`)
- source order: explicit `--frozen`; otherwise `git show
  0fa5e0d:tools/mori-census.sh`; an on-disk
  `.ufo/waves/round-15/frozen/mori-census.sh` is cross-checked byte-for-byte.
  Missing git materialization falls back to the on-disk copy only if it hashes
  to the pin. Any mismatch is exit 2.

Exit map:

- `0` all SUT fixture expectations pass and the frozen control reproduced the
  entering red state (red-relevant cases miss alarms; all other cases pass)
- `1` a SUT fixture expectation failed
- `2` usage/setup/pin/fixture-schema/control error (could not evaluate),
  including no red-relevant case, frozen unexpected pass/fail, or
  `control_inconclusive` (timeout, exec error, integrity failure, or a
  red-relevant failure not explained by the specifically missing alarm)

No baseline waiver exists. `--case` still compares the whole expected table;
it only narrows execution and exits 2 if no red-relevant case is selected.

### Expected-table trust

A normal run refuses to start (exit 2) without the committed expected table.
The table records every fixture pack path/name/SHA-256, every case id,
`want_oom`, `want_signal`, `invalid_class`, derived mode, independently derived
four-token positive counts, derived invalid scope/reason, and red-relevance.
It also records the gate SHA-256, imported r14 helper SHA-256, frozen SHA-256,
base commit and frozen source. At run time the gate compares all of those,
re-parses the packs from the bytes it hashed, and compares case expectations
exactly. An edit to any gate/r14/pack/frozen byte therefore forces a re-pin.
The expected table is evidence, not the source of the frozen pin.

Pin command after all bytes settle (L1 owns timing):

```
python3 tools/mori-round15-regressions.py \
  --fixtures .ufo/waves/round-15/fixtures \
  --pin-fixtures .ufo/waves/round-15/expected.json
```

Run output must not cover/equal the fixture directory, repo root, `tools/`,
`.git/` or `corpus/`; the guard exists so an `--output .ufo/waves/round-15` run
cannot swallow every fixture pack. A safe example is
`.ufo/waves/round-15/evidence/r15-gate`.

## Fixture consumption

Shared six-key schema is consumed unchanged: `{id, user, system, want_oom,
want_signal, invalid_class}`. Case ids must be unique across all packs, match a
safe path regex, and are the only names used for fixture directories. A
`MESSAGE` key anywhere in a record set is a setup error (exit 2); no fixture
record body is copied into the manifest or report. Records are read once from
the hashed bytes and parsed from those same bytes.

Boot handling: after `build_fixture`, both `base/boot_id` and
`MORI_BOOT_ID` are forced to
`11111111111111111111111111111111`; r14's `0123…` default never reaches the SUT.
Every census subprocess gets the explicit r14 `census_env` dictionary, whose
`MORI_JOURNALCTL_BIN` names the generated stub. No host journal or ambient
`MORI_*` value is inherited.

Mode is derived, never read from the pack:

| invalid_class | r14 stub mode |
|---|---|
| `null` | `honor` |
| `kernel_oom_notice` | `dup-kernel` (only the kernel query ignores argv filters) |
| any other non-null | `ignore-filters` (only the named invalid class is asserted, so collateral raw invalidation is not graded) |

Capture controls are an internal selftest extension only (`capture` key), not
part of the shared pack schema.

## Independent expectations

Positive counts are computed from fixture records in the harness, not from SUT
output:

- identity: JSON object, scalar string `_BOOT_ID` equal to the shared boot,
  scalar string `MESSAGE_ID` equal to the exact class id
- kernel: identity only
- unit OOM/signal: identity plus `UNIT_RESULT` exactly `oom-kill` / `signal`
- process SIGKILL: identity plus `EXIT_CODE` exactly `killed` and scalar
  `EXIT_STATUS` string `9` or number 9; null/bool/array/object rejected

The four values must appear exactly per scope on `SURFACE journal.user` and
`SURFACE journal.system` as `positive_kernel_oom`, `positive_unit_oom`,
`positive_unit_signal`, `positive_process_sigkill`, plus
`positive_basis=validated-subset-lower-bound`. A capture/parser failure control
requires `unavailable:<rc-N|stderr-nonempty|malformed-json>` instead of a
fabricated zero and forbids an alarm.

`want_oom` is checked against any independently valid kernel/unit-OOM record in
either scope. `want_signal` is checked against user-scope unit-signal or
process-SIGKILL records only; a system-only signal must be `want_signal=false`
and must not raise the user warn.

Invalid aggregate: for each scope that actually holds a record failing the
named class predicate, the exact SURFACE class token must read
`unavailable:<reason>`. Reasons are re-derived from records with the census
fallback shape: non-object/non-string/empty boot -> `record-invalid`; more than
one boot -> `multi-boot`; one other boot -> `boot-mismatch`; one current boot
with a class mismatch -> `record-invalid`. Empty or clean opposite scopes are
never asserted unavailable. Under `ignore-filters`, collateral invalidation of
other classes is deliberately not asserted.

Alarm grading:

- exactly one `OOM_KILL_JOURNAL severity=crit` iff `want_oom`; exactly one
  `KILL_SIGNAL_JOURNAL severity=warn` iff `want_signal`; exact parsed ids, never
  a prefix
- DRIFT/1 iff any expected alarm, CLEAN/0 otherwise; drift equals the number of
  expected alarm lines
- OOM fields `user_notice`, `system_notice`, `user_unit_oom`,
  `system_unit_oom`, `user_unit_oom_result_unknown`,
  `system_unit_oom_result_unknown`, scoped positive fields
  `user_/system_positive_kernel_oom` and `user_/system_positive_unit_oom`,
  all compare byte-for-byte with their SURFACE tokens; no summed `count=` on
  the OOM line
- WARN raw `count` equals `process_sigkill`; `process_sigkill` and
  `user_unit_signal` compare byte-for-byte with the user SURFACE tokens;
  `user_positive_process_sigkill` and `user_positive_unit_signal` compare with
  the user SURFACE positive tokens
- `positive_basis=validated-subset-lower-bound`; OOM
  `positive_validation=scalar-id+current-boot`; WARN
  `positive_validation=scalar-id+current-boot+exact-fields`;
  `raw_basis=scoped-record-count`
- `alarm_basis` is derived from source arm states: healthy aggregate
  (`scoped-record-count`), positive-only source (`validated-positive-records`),
  or both (`scoped-record-count+validated-positive-records`)
- exact `paths` token set/order: OOM `kernel_oom_notice` then
  `unit_result_oom_kill`; WARN `process_sigkill` then `unit_result_signal`,
  each once
- every FINDING carries `script_sha256` equal to the executed census copy
- every census argv is checked for `MESSAGE` requests and the PATH journalctl
  tripwire must stay empty; at most 12 journalctl calls are allowed, enforcing
  the same-captured-stream/no-extra-query contract

## Frozen red control

The frozen snapshot is run for every selected case. Availability of each alarm
source is derived independently from the selected stub mode and census all()
semantics:

- red-relevant: every expected alarm source's class aggregate is unavailable in
  its scope, so the frozen census must miss the alarm and fail the behavior
  evaluator
- all other cases: the frozen census must pass the legacy behavior evaluator

Frozen grading is behavior-only: stable ids, severity, one-line counts, roll,
rc, invalid raw tokens, script hash, argv/tripwire. It never requires new
positive fields, so old bytes are not failed merely for lacking r15 metadata.
SUT full-schema failures are reported separately from SUT behavior-only
failures; the manifest has `sut`, `sut_behavior`, and `frozen` per case plus
summary counters. A frozen non-mixed failure or a frozen red-relevant pass is a
control problem (exit 2), never counted as a SUT bug. If `--census` names the
frozen bytes, full-schema failures are expected; the behavior-only metric
distinguishes missing alarms from missing metadata.

## Provenance and evidence

Every normal run persists, under the chosen `--output`:

- `expected.json` (byte copy) and its SHA-256
- `run-manifest.json` with gate/r14/census/frozen paths and SHA-256s,
  expected-table SHA-256, per-fixture pack path/name/SHA-256, per-case static
  expectations, per-case SUT/SUT-behavior/frozen verdicts and reasons, and all
  run records
- `runs/<case>.<target>.stdout` / `.stderr` plus SHA-256s; run records carry
  `argv`, `cwd`, `rc`, timeout/exec error, duration, and journal-stub argv count
  and digest
- revision `start`/`end` with real `git rev-parse HEAD`, exact porcelain-v1-z
  path list (renames keep both paths; paths only, no file contents),
  `dirty_outside_harness_output` excluding only the output prefix, and
  `stable`/`head_changed`/`status_changed`
- input hashes at load and at end for gate, r14 helper, expected table, census
  source, executed census copy and executed frozen copy; any change exits 2

No fixture record bodies, unit names or `MESSAGE` values are written to the
manifest or report. Census stdout/stderr are retained exactly as produced under
the stub; no production MESSAGE request exists.

## Static pack analysis (pin mode, no census execution)

Ran the gate's `--pin-fixtures` mode against the current lane fixtures as a
pack-schema/derivation probe only (no census and no fixture execution):

```
python3 tools/mori-round15-regressions.py \
  --fixtures .ufo/waves/round-15/fixtures \
  --pin-fixtures /tmp/mori-r15-expected-probe-final.json
PINNED /tmp/mori-r15-expected-probe-final.json
PIN fixtures=16 cases=63 frozen_sha256=0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9
PIN gate_sha256=<pre-final probe hash> r14_helper_sha256=533218a566030fdabf7ca6a1c78111ca10be3fb3cb0e4a7b22734959f847e4ef
PIN red_relevant_cases=34
```

All 16 packs parsed, 63 case ids were unique, and 34 cases are red-relevant
under the derived mode/availability rule. No expected table was written into
the lane (`/tmp` probe only); L1 must generate and commit the lane table after
all bytes settle. The gate changed after that probe for the F1–F8 review fixes,
so this fixture analysis was not re-executed; the final gate hash is the one in
the Files table.

## Selftest evidence (isolated wrappers only)

Post-review, `--selftest` builds a temp pack and shell wrappers that call a
Python sidecar, then calls the normal gate for each arm. Every arm now runs the
real pinned frozen census against the synthetic mini-fixtures; there is no
no-control bypass. A pure helper-level `classify_control` check covers frozen
exec-error, timeout, integrity, alarm-not-missing and non-red cases without
executing a census.

The last executed selftest below predates the F1–F8 edits. It is retained for
honesty, not as evidence for the revised code; no post-review selftest or gate
run was made under the L1 stop-verification instruction. The revised
helper-level classifier checks now also include partial retention (OOM retained
while WARN missed, and the reverse), unwanted-alarm rejection, and
no-wanted-arm-missing rejection.

```
python3 tools/mori-round15-regressions.py --selftest
SELFTEST pin expectations -> /tmp/mori-r15-selftest-3ltrrn0x/expected.json
SELFTEST PASS selftest_root=/tmp/mori-r15-selftest-3ltrrn0x
```

Pre-review observed subprocess exit codes: green `0` (7/7 SUT and behavior
pass), red `1`, tampered expected finding id `1`, tampered verdict/rc `1`,
frozen pin tamper `2`, tampered expected-table fixture digest `2`. The green
manifest retained `argv`/`rc`/stdout/stderr paths and hashes for all seven
pre-review runs, and `inputs.unchanged` / `revision.stable` were true. The
revised selftest expects 14 runs per green arm (SUT + frozen for seven cases)
and the same 0/1/1/1/2/2 exit arms; these post-review expectations were not
executed here.

Honesty note: the lane instruction said to skip all tests/builds while the
editing wave is in flight. `--selftest` was run during earlier development
because the assignment explicitly required it to perform actual subprocess
red/green/tampered checks; those runs are recorded rather than hidden. After
the L1 stop-verification instruction, no selftest, gate or syntax check was
run. No production gate run was ever made; L1 owns the single
post-integration run.

## Coordination

- `MoriR15` L1: sent pin/run commands, output guard, exit map, final gate and
  r14 SHA-256, and the re-pin requirement.
- `MoriR15.SkillInterface`: sent CLI/expected-table/pin/exit-map facts and the
  final hash correction.
- `MoriR15.CensusPositive`: confirmed the gate enforces the settled surface
  bare positives, scoped finding positives, basis/validation labels, exact
  paths, `count==process_sigkill`, raw/SURFACE equality and the 12-call cap.
- Pack seats: answered mode/scope/positive-count questions; consumed all packs
  unchanged.

## Risks / blockers

- The lane expected table does not exist yet. Normal runs exit 2 until L1 runs
  `--pin-fixtures` and commits the result after gate/r14/census/pack bytes
  settle.
- Any later edit to the gate or the imported r14 helper invalidates the pinned
  expected table (exit 2). This is intentional.
- The frozen source is the pinned git blob plus an on-disk cross-check. A
  divergent on-disk copy is a pin error.
- Captured failures are covered only for producer rc, producer stderr and
  malformed JSON via internal selftest controls; missing-journalctl/jq/boot
  early-return surfaces are outside the fixture schema and are not asserted.
- `ignore-filters` intentionally degrades raw classes beyond the named
  `invalid_class`; the gate never asserts those sibling raws, matching the
  contract. An empty/clean opposite scope is never asserted unavailable.
- No claim of completeness, authenticated ids, unique victims, repaired
  arbitrary malformed JSON or production correctness is made here.
