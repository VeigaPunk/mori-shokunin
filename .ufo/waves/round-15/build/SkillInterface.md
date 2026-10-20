# SkillInterface — round 15 (C1 coverage)

Seat: `MoriR15.SkillInterface` (executor, leaf). Axes: coverage (primary);
operability/calibration as constraints (no fabricated totals, existing raw
tokens and alarm semantics preserved). No builds, tests, gates, census runs,
linters or formatters were executed. No installs or updates were performed.
Parent host-safety rule received; no package operation was needed.

## Files changed

- `/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md`
  — sha256 `04d878d010c15ce802cdf7d3b7b2bac5ac2a89fd0bbc1ccf2b98847a069834f4`
    at this report's write time (the report does not modify it).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-15/build/SkillInterface.md`
  — this report. No other file was written or edited by this seat.

## Delivered interface documentation

`SKILL.md` now documents the r15 positive-evidence interface and its limits:

- **Decision table line 17** — the kill surface names the per-scope
  `positive_kernel_oom` / `positive_unit_oom` / `positive_unit_signal` /
  `positive_process_sigkill` tokens as positive evidence that survives an
  adjacent invalid record, while raw aggregate/split tokens stay `unavailable`.
  The OOM alarm fires when any independently valid positive OOM record exists;
  the user signal warn fires from independently valid user records even when
  raw `count`/`process_sigkill` is unavailable.
- **Error-pattern rows 30, 31, 33, 34, 36** — corrected the active
  all-or-nothing wording:
  - raw class/split counts are aggregate-only and stay `unavailable` on a
    nonzero rc, stderr, timeout, malformed JSON or any class-invalidating
    adjacent record;
  - a raw OOM counter can be `unavailable:<reason>` while the positive token is
    > 0 (the aggregate is invalid, the individually valid record is not);
  - the fleet/non-fleet/unattributed owner partition is aggregate-only and
    takes no positive salvage;
  - the user `KILL_SIGNAL_JOURNAL` warn can fire from a positive while raw
    `count=`/`process_sigkill`/`user_unit_signal` read `unavailable:<reason>`;
    those raw fields are never rewritten as positive counts;
  - r15 positive tokens are alarms, not victim/PID/time attribution.
- **New section lines 46-102, “Positive evidence vs an unavailable aggregate
  (r15)”** — records the narrow repair and the exact predicates:
  - JSON object + scalar `MESSAGE_ID` equal to the class id + scalar `_BOOT_ID`
    equal to the current boot;
  - unit OOM/signal require `UNIT_RESULT` exactly `oom-kill`/`signal`; process
    requires `EXIT_CODE` exactly `killed` and scalar `EXIT_STATUS` 9 (string
    `"9"` or number `9`; bool/array/null rejected);
  - subject metadata is irrelevant to the predicates;
  - same captured, stderr-free, valid JSON stream; no second journal query;
  - capture/parser failure makes positives `unavailable:<reason>`, never 0; a
    parsed stream with no individually valid record is a real 0 for that
    positive token, not a class total; excluded records never become counts;
  - no completeness, victim count, unique victim, authenticated emitter, fleet
    causation, owner routing or malformed-JSON repair is claimed;
  - exact token placement is documented: scope-local bare tokens plus
    `positive_basis=validated-subset-lower-bound` and
    `positive_validation=scalar-id+current-boot` on `journal.<scope>` surface
    rows; scope-prefixed `user_positive_*`/`system_positive_*` plus the same
    two basis tokens on the single OOM line;
    `user_positive_process_sigkill`/`user_positive_unit_signal` with
    `positive_validation=scalar-id+current-boot+exact-fields` on the user
    signal line (the system INFO path carries no positive fields);
    `alarm_basis=validated-positive-records` (or
    `scoped-record-count+validated-positive-records`) names the firing basis.
  - ground pointer added to `corpus/knowledge/journal-positive-evidence-r15.md`
    (S014/S015/S037/S038; interface reading, not a measured live positive).
- **Journal-arm summary lines 138-152** — positive pass reuses each class
  capture (no new query); the global OOM alarm may rest on reported notices or
  independently valid positive records, with four never-summed raw arms plus
  per-scope positives; positives are unavailable on capture/parser failure and
  never a total when the class is invalid.
- **Wording sweep** — r14 red selftest receipt disclosed at lines 176-178
  (`8d22d18` exit 1 on `real-gate-red-oom-id`/`real-gate-red-unit-id`/
  `real-gate-red-evidence`, superseded by the `5601d12` accepted receipt), and
  the drift note at lines 196-199 records that the positive counters join the
  declared count-magnitude volatile list, so the old r10 baseline reports
  `volatile_fields`; no re-pin is performed or claimed.

## r15 gate registration (full fields, no predicted tally)

`SKILL.md` line 134 registers `r15 regressions` with every PROTOCOL gate field:

| field | registered value |
|---|---|
| name / kind | `r15 regressions` / `gate` |
| entry | `python3 tools/mori-round15-regressions.py --output <dir>` (`--census` default `tools/mori-census.sh`; `--fixtures` default `.ufo/waves/round-15/fixtures`; `--expected` default `.ufo/waves/round-15/expected.json`; `--frozen` default `.ufo/waves/round-15/frozen/mori-census.sh`, else `git show 0fa5e0d:tools/mori-census.sh`; `--pin-fixtures <path>` regenerates the expected table after packs settle) |
| verdict map | 0 clean (all SUT expectations pass and the frozen control reproduces the entering red state on red-relevant cases) · 1 failed (a SUT fixture expectation failed) · 2 could-not-evaluate (usage/setup/pin/fixture-schema/control error, digest or expected-table mismatch, `snapshot_tampered`, missing expected table, unexpected internal error) |
| self-test | `python3 tools/mori-round15-regressions.py --selftest` — actual isolated gate subprocesses with temp packs/wrappers, asserting exit and stable expected ids; `--no-frozen-control` is selftest-internal and requires the hidden `--selftest-child`; the tally is measured by L1 after integration and is **not predicted** in `SKILL.md` |
| pinned values | in-script `PINNED_FROZEN_SHA256` `0e41cb83…` and `PINNED_BASE_COMMIT` `0fa5e0d…` (never trusted from a manifest; digest mismatch exits 2); expected table `.ufo/waves/round-15/expected.json` pins each fixture pack SHA-256, static per-case expectations, and gate/r14-helper/frozen digests (any later gate or r14 edit requires re-pin); runs store `expected.json` + `run-manifest.json` (revision, dirty path scope) under `<dir>` |
| write scope | `<dir>` evidence tree only, and `--output` must not equal/cover the fixture directory, repository root, `tools/`, `.git/` or `corpus/`; fixture packs read-only; a `MESSAGE` key is a setup error |
| owner | mori |

Source of these fields: direct read of the delivered
`tools/mori-round15-regressions.py` — constants/defaults `:121-136`, frozen
load/digest `:698-713`, expected table build/compare `:843-876`, pin path
`:1323-1334`, output guard `:1348-1367`, gate run `:1369-1395`, manifest
`:1639-1669`, selftest `:1999-2090`, CLI `:2092-2107`, exit-2 paths
`:2113-2150` — plus `MoriR15.HarnessBuild`'s final CLI/pin IRC. Final harness
SHA-256 is `3f1cdcfd7c9a3486c0dd941a145a2cbbd31deaaa9db133445f40b12477e5627b`;
the r14 helper SHA-256 is
`533218a566030fdabf7ca6a1c78111ca10be3fb3cb0e4a7b22734959f847e4ef`.
HarnessBuild's static pin-mode analysis (not executed here) reports 16 packs,
63 cases and 34 red-relevant cases. No tally from either source is stated as
measured.

The adjacent r15 narrative at lines 180-195 states the frozen-control rule
(red-relevant cases miss the alarm there; every other case passes), the
required committed expected table, and the explicit non-claims (no malformed
JSON parse, no completeness/authenticated ids/unique victims). No live-positive
claim and no predicted test count appear.

## Retained evidence (observed, not executed)

- **Fixture packs:** `.ufo/waves/round-15/fixtures/` contains all 16 assigned
  packs; `jq` file-data count is 63 case objects total. `grep -l '"MESSAGE"'`
  over the packs returned no file, consistent with the no-MESSAGE contract.
  This is file data, not a gate run.
- **Knowledge note:** `corpus/knowledge/journal-positive-evidence-r15.md`
  exists with the S014/S015/S037/S038 sources, predicate table, decision table
  and explicit non-claims; `SKILL.md` cites it as ground.
- **Census interface (read-only anchors):** `tools/mori-census.sh` contains the
  r15 contract at `:955-995`, the positive jq expressions at `:1033-1036`, the
  positive scan at `:1100-1131`, OOM firing/fields at `:1448-1509`, user
  KILL_SIGNAL at `:1512-1551`, per-scope surface tokens at `:1578-1588`, and
  the positive drift keys at `:2479-2481`. The seat did not run the census.
- **Producer-shape confirmation:** `MoriR15.CensusPositive` reported the exact
  emission shape — bare per-scope tokens plus `positive_basis` on both surface
  rows; scope-prefixed positives on the OOM line; `user_positive_process_sigkill`
  / `user_positive_unit_signal` on the user KILL line; the system signal INFO
  carries no positive fields; a parsed stream with no valid record is a real 0.
  The SKILL field names were aligned to that report and the census anchors.
- **Final harness interface:** `MoriR15.HarnessBuild` confirmed the committed
  `--expected` table + `--pin-fixtures`, the output guard, the selftest-internal
  flag pair, the re-pin rule, final gate SHA-256
  `3f1cdcfd7c9a3486c0dd941a145a2cbbd31deaaa9db133445f40b12477e5627b`, r14 helper
  SHA-256 `533218a566030fdabf7ca6a1c78111ca10be3fb3cb0e4a7b22734959f847e4ef`,
  and the static pin-mode analysis (16 packs / 63 cases / 34 red-relevant).
  These are owner-reported/static facts; this seat executed nothing.
- **r14 receipt reconciliation:** `.ufo/waves/round-14/evidence/r14-selftest.json`
  records `measured_commit 8d22d18…`, exit 1, stdout
  `SELFTEST: fail real-gate-red-oom-id | real-gate-red-unit-id | real-gate-red-evidence`;
  `.ufo/waves/round-14/evidence/r14-selftest-accepted.json` records
  `measured_commit 5601d12…`, exit 0, `SELFTEST: pass checks=20`. The SKILL
  wording now names the superseded red run instead of reporting only green.
- **Documentation-review fixes:** `ReviewDocumentation.md` finding 2 (undisclosed
  r14 red receipt) is addressed in the r14 narrative. Finding 4 was already
  satisfied by the existing r14 row, which names `5601d12` beside the
  `c39e5a73…` harness SHA; it was left unchanged. The historically scoped
  “twelve in the r13 bytes” phrase was left scoped, as that review recommended
  no current-byte count without a measurement.
- **No live positive evidence:** no journal query, fixture run, census run,
  gate run or selftest was performed by this seat. “Alarm fires” statements in
  `SKILL.md` describe the required interface, not an observed host event.

## Risks and blockers

1. **Expected table absent at write time.** `.ufo/waves/round-15/expected.json`
   does not exist yet. A normal `r15 regressions` run therefore exits 2
   (could-not-evaluate) until the table is generated after the packs settle and
   committed: `python3 tools/mori-round15-regressions.py --fixtures
   .ufo/waves/round-15/fixtures --pin-fixtures .ufo/waves/round-15/expected.json`.
   Any later gate or r14-helper edit requires a re-pin. The registered row
   states this as exit 2, never a pass; no tally is claimed. This is the only
   blocker to a clean r15 gate run and belongs to the harness/L1 integration
   step, not this documentation seat.
2. **Harness interface was finalized during this seat's work.** The registry
   row and report were aligned to the final delivered bytes
   (`tools/mori-round15-regressions.py` SHA-256 `3f1cdcfd…`; r14 helper
   `533218a5…`), including the committed `--expected` table, the output guard,
   and the `expected.json` + `run-manifest.json` evidence names. If the gate or
   r14 helper changes before integration, the row's entry/pin cells and the
   expected table must be rechecked/re-pinned.
3. **Census implementation was observed read-only, not executed.** The positive
   jq expressions, OOM/KILL firing, surface tokens, drift keys and final basis
   labels were checked against the producer’s confirmed shape, but this seat ran
   nothing. The documented predicates and unavailable/zero rules match the census
   header and the r15 knowledge note; L1's selftest and gate run are the
   behavioral verification.
4. **r14 harness migration is a sibling's scope.** `ReviewHarnessGate.md` H2
   (`R14_SEC_DUP_MSGID_MIXED` must invert `forbid_ids` to expect the positive
   alarm) and the provenance CE items are harness-owner work. If they are not
   landed, the r14 regression gate may go red at integration independently of
   this documentation change.
5. **No predicted tally or live positive.** `SKILL.md` states no measured r15
   selftest/gate count and no live positive value. Any integration report must
   supply those from actual runs.

## L1 checks once after integration (not run here)

- Generate/verify the r15 expected table after packs settle:
  `python3 tools/mori-round15-regressions.py --fixtures .ufo/waves/round-15/fixtures --pin-fixtures .ufo/waves/round-15/expected.json`
  (then commit the table; any later gate/r14 edit requires a re-pin)
- `python3 tools/mori-round15-regressions.py --selftest`
- `python3 tools/mori-round15-regressions.py --output <dir>` (normal gate with
  the frozen control)
- `bash tools/mori-census.sh --selftest` (census-side positive fixtures)
- `python3 tools/mori-round14-regressions.py --output <dir>` (existing r14
  semantics; expected to require the H2 migration if not already landed)
- `bash tools/mori-silence-cases.sh` and the drift pin remain the other
  registered gates; the old r10 baseline is expected to name `volatile_fields`
  until a re-pin decision, not to pass green by this change.

## Integration corrections applied

L1 applied the two narrow wording ambiguities before this report's final
digest: the `journal class counts` row now separates capture/parser failure
(both aggregate and positive evidence unavailable) from a semantic record
failure in a parsed capture (raw aggregate unavailable, qualified positives may
remain), and the failure-rule examples no longer list
`record-invalid`/`multi-boot`/`boot-mismatch` as capture/parser failures.

At L1's request, this seat then updated the basis labels in the r15 section:
`positive_basis=validated-subset-lower-bound` and
`positive_validation=scalar-id+current-boot` on both surface rows and the OOM
line; the user signal line uses
`positive_validation=scalar-id+current-boot+exact-fields`. This was checked
against the current census anchors (`tools/mori-census.sh:1002-1003`, `:1534`,
`:1588`, `:1625`). The four positive field spellings, raw tokens, scope split
and user-only warn are unchanged. This report's SHA and line references
describe the current, post-correction `SKILL.md`.

## Tooling

No installs, upgrades, pacman dry-runs or other package operations were
performed. No credential, auth, `agent.db` or OMP process surface was touched.
