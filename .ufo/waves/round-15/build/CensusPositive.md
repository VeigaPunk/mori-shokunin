# CensusPositive — r15 validated-positive retention (tools/mori-census.sh)

Seat: `MoriR15.CensusPositive` (executor, leaf). Axis: **coverage** (C1: lowest owned
axis6 vs operability 7). Milestone: **retain validated positives without fabricated
totals**.

Owned and changed: `tools/mori-census.sh` only. Report: this file. No commits, no other
production/fleet/sibling/verifier/MANIFEST edit. No builds, tests, linters, formatters,
smoke runs, census runs or harness runs were performed (L1 owns the single post-integration
verification). No tools installed or upgraded.

## Behaviour landed

Raw aggregate semantics are unchanged: a class containing any malformed / nonmatching /
foreign-boot record still reports every raw token and split as `unavailable:<reason>`
(`record-invalid`, `multi-boot`, `boot-mismatch`, `malformed-json`, `rc-N`, `timeout`,
`stderr-nonempty`, ...). What changed is that the same successful, stderr-free capture is
reused for a **validated-positive fallback**, so one real OOM/SIGKILL record next to a bad
record can no longer be silenced.

- On a healthy aggregate the raw count **is** the positive count; no extra parser runs.
- Only after a semantic aggregate failure (`record-invalid` / `multi-boot` /
  `boot-mismatch`) does `journal_positive_scan` run one index-safe jq pass over the SAME
  captured bytes. No second journalctl invocation, no second query, no extra query field
  projection.
- A positive counts ONLY a JSON object with **scalar string** `_BOOT_ID` exactly equal to
  the expected current boot and **scalar string** `MESSAGE_ID` exactly equal to the class
  id, plus the class field: `UNIT_RESULT` the exact string `oom-kill` / `signal`;
  `EXIT_CODE` the exact string `killed` and `EXIT_STATUS` scalar string `"9"` or scalar
  number `9`. `null`, bool, array, object, missing, foreign boot, wrong id and non-object
  lines are excluded, never coerced. No tostring/default/recursive salvage.
- Fail closed: capture failure (rc, nonempty stderr, timeout, missing timeout/journalctl/
  jq), an aggregate jq error, or a structurally malformed aggregate/fallback response
  leaves positives empty → `unavailable:<aggregate-status>`. Nothing is salvaged from an
  invalid parser response. A parsed stream with no individually valid record is a real
  `0` for the positive token; it is never presented as a class total.
- OOM fires exactly once if ANY `positive_kernel_oom` or `positive_unit_oom` is > 0, even
  while the raw counter is `unavailable:<reason>`. OOMD notices stay INFO-only and never
  feed a positive. The user KILL_SIGNAL warn fires from independently valid
  `positive_process_sigkill` / `positive_unit_signal` records; `KILL_SIGNAL_JOURNAL_SYSTEM`
  remains aggregate-gated INFO. OOM and signal fire flags are independent.
- Owner routing (fleet / non-fleet / unattributed) stays aggregate-only: an invalid unit
  class emits no routing finding and no positive subject classification is invented.

### Emitted shape (exact)

`SURFACE journal.user` and `SURFACE journal.system` keep every existing raw token and add,
scope-local, before `; boot=`:

```
positive_kernel_oom=<n|unavailable:reason> positive_unit_oom=...
positive_unit_signal=... positive_process_sigkill=...
positive_basis=validated-subset-lower-bound positive_validation=scalar-id+current-boot
```

`OOM_KILL_JOURNAL` (crit, one line) keeps `paths`, `user_notice`, `user_unit_oom`,
`user_unit_oom_result_unknown`, `system_notice`, `system_unit_oom`,
`system_unit_oom_result_unknown`, `scope`, `trust`, `boot`, and adds exactly once each:
`user_positive_kernel_oom=`, `system_positive_kernel_oom=`, `user_positive_unit_oom=`,
`system_positive_unit_oom=`, plus `positive_basis=validated-subset-lower-bound`
`positive_validation=scalar-id+current-boot` and
`alarm_basis=scoped-record-count|validated-positive-records|scoped-record-count+validated-positive-records`,
`raw_basis=scoped-record-count`.

`KILL_SIGNAL_JOURNAL` (warn, user only) keeps raw `count=`, `process_sigkill=`,
`user_unit_signal=`, `paths`, `scope`, `attribution`, `boot`, adds
`trust=client-supplied`, `user_positive_process_sigkill=`, `user_positive_unit_signal=`,
the two basis tokens (`positive_validation` gains `+exact-fields`), and the same
`alarm_basis`/`raw_basis` semantics. Signal paths are built once from two kind flags
(`process_sigkill` first, then `unit_result_signal`), so raw + mirrored positive evidence
cannot duplicate a path token. No unit name is emitted.

## Code map

| Area | Lines (current file) |
|---|---|
| header journal/r15 contract and field shape | ~15-25, ~888-1017 |
| strict positive jq selectors | ~1043-1056 |
| `journal_positive_scan` (same-capture fallback, fail-closed) | ~1108-1138 |
| `journal_query` positive plumbing + semantic-failure hooks | ~1140-1267 |
| `probe_journal` positive lookup and per-class wiring | ~1292-1405 |
| OOM alarm (raw + positive, basis attribution) | ~1465-1535 |
| user KILL_SIGNAL warn (raw + positive, single path build) | ~1537-1589 |
| journal surface positive tokens | ~1612-1626 |
| drift counter keys + magnitude-only note | ~2486-2503, ~2685 |
| in-script mixed-stream selftests | ~3493-3565 |

## Evidence retained (static only)

- Journalctl invocation count is unchanged at **12** (six classes × two scopes): the
  positive pass reuses the captured bytes and never adds a producer call. Capture failure
  (rc, stderr, timeout, missing bins) and invalid aggregate parser responses leave all four
  positive tokens `unavailable:<status>`.
- Final interface matches the r15 gate's pinned tokens: scope-prefixed OOM positives, subset
  lower-bound basis, exact raw/scoped aggregate preservation, exact single-token signal
  paths, and capture-failure unavailability. `HarnessBuild` confirmed the gate asserts this
  shape; `SkillInterface` updated SKILL.md against the same anchors.
- Existing raw tokens, severity, finding ids and unavailable spellings are untouched; the
  diff is additive fields plus the alarm firing predicate.
- Targeted review of all new/changed blocks; a missing quote introduced during the basis
  rename at the surface line was found by re-read and fixed before this report.
- Read (not executed) all round-15 fixture packs under `.ufo/waves/round-15/fixtures/`
  (16 packs). Their invalid classes are structurally bad **objects** (MESSAGE_ID arrays,
  `_BOOT_ID` null/array/missing, UNIT/USER_UNIT arrays, UNIT_RESULT arrays/null/missing,
  EXIT_CODE arrays, EXIT_STATUS arrays/null/string-non-9, foreign boots, wrong ids). The
  landed selectors and fallback cover these: aggregate stays unavailable, the one valid
  current-boot sibling is counted, OOM/warn fire from it, and subject-only records still
  reach the alarm through `positive_unit_oom` without owner routing.
- New hermetic selftest fixtures (static, not run): mixed kernel stream with array/wrong
  MESSAGE_ID siblings; unit oom-kill with a foreign-boot sibling; unit signal with a
  foreign-boot sibling; numeric-9 process status with a non-9 sibling; unsafe statuses
  (`null`, `true`, `[9]`, `{"n":9}`) never positive; foreign-only stream positive `0` and
  no alarm. Raw-token assertions that could substring-match a new positive were re-anchored
  with `[ ]` (`unit_oom`, `unit_signal`, `process_sigkill`).

## Risks, limits, blockers

1. **No execution in this seat.** Correctness of shell/jq syntax and fixture behaviour is
   statically argued, not measured; L1's single gate run is the authority.
2. **Drift pin now reports `volatile_fields`.** The four bare positives, four scoped
   positives and two scoped signal positives were added to `DRIFT_COUNTER_KEYS` so their
   magnitudes are masked like every other count. Changing the declared list is itself
   drift; no repin was authorized and none was attempted. Masking removes magnitudes only,
   never token existence, finding-line presence or severity (documented in the code and
   pin header).
3. **Non-object valid-JSON neighbors.** If an aggregate filter evaluation errors on a
   non-object line, the class reports `malformed-json` and positives are unavailable
   (fail-closed parser rule). Packs use structurally bad objects, which take the fallback
   path. Salvaging past a jq aggregate error was deliberately not implemented because L1
   ruled invalid parser responses leave positives unavailable.
4. **Boot anchor is env/trust input.** `MORI_BOOT_ID`/`MORI_BOOT_ID_FILE` are trusted for
   the expected current boot; no stale-env crosscheck was added (out of scoped debt). The
   surface echoes only `${sboot[$scope]:-$BOOT_ID_EXPECTED}`, where `sboot` advances only
   from an aggregate whose filter enforced equality with the expected id; positives carry
   no boot value.
5. **Parser identity.** Host `jq` may resolve to jaq 3.1.1 while `/usr/bin/jq` is 1.8.2;
   existing `-s -r` selection is unchanged and L1 pins the verification parser. The
   selectors use basic jq/jaq constructs (`type`, `select`, `@tsv`, numeric equality).
6. **No completeness, authentication, victim or total claim.** A positive is a validated
   subset lower bound from client-supplied journal fields, not proof of completeness, an
   authenticated id, a unique victim or a kill total. Malformed JSON is not repaired; no
   new route or actuation exists.

## Coordination

Sent exact shape/semantics to `MoriR15.SkillInterface`, `MoriR15.HarnessBuild`,
`MoriR15.ProvenanceCapture`, `MoriR15.SecurityPrivacy`, `MoriR15.AttackSignalConfusion`,
and a design note to `MoriR15`. `AttackSignalConfusion` confirmed R1-R3 closed read-only;
`SecurityPrivacy` confirmed P1-P4/P6 fixed and its 9.0 note reclassified info.
