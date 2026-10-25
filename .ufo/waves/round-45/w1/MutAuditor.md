# MutAuditor — mutation test of `tools/mori-gate-registry.py` (v2)

Seat: mutation-tester, mori round 45 wave 1. Leaf seat; no subagents dispatched.

Target (never edited by me):
`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-gate-registry.py`
sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`, 743 lines,
31165 bytes — the version `ExecRegistryAuditor.md` declares final (same sha in its
head). Lane hash measured before and after every step; unchanged.

Scratch (`TMPDIR` per wave spec): `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/MutAuditor/`
(pristine copy `pristine.py`, six mutants `mutants/*.py`, probes `probe.py`,
driver `drive.py`, raw log `receipts.txt`, determinism receipts `det/`).
Nothing installed or upgraded this seat.

## Method

Each mutant is the pristine bytes with **one** textual disable, asserted unique
(`text.count(anchor) == 1`) and proven one-hunk by `diff -u`. Every property is
checked in two directions, so "selftest green" is never confused with "mutation
was a no-op":

1. a bounded behavioral probe (`probe.py`) that states what a correct auditor
   must do, built on an isolated throwaway git repo under the scratch TMPDIR —
   run on pristine (must pass; otherwise the mutant is *inconclusive*, not
   killed) and on the mutant (must fail = property really disabled);
2. the mutant's own `--selftest`, with its tally line and rc, plus the failing
   arm name.

Baseline (pristine, unmutated):
`GATE_REGISTRY_SELFTEST pass=15 fail=0`, rc=0; all six probes pass on pristine.

## Results

| # | property disabled (one hunk) | mutant sha256 (first 16) | `GATE_REGISTRY_SELFTEST` line | rc | caught by |
|---|---|---|---|---|---|
| a | read only the FIRST registry table (`i = j` → `break` after the first append) | `97c104e1333924be` | `GATE_REGISTRY_SELFTEST pass=14 fail=1` | 1 | **arm `second_table_registered`** |
| b | accept a substring occurring anywhere in a cell as attribution (re-adds the v1 fallback `safe in cells[2] or basename in cells[2]`) | `430477ea71cca2fe` | `GATE_REGISTRY_SELFTEST pass=15 fail=0` | 0 | **NONE — mutant survives** |
| c | accept a comment-only `--selftest` in a `.sh` tool (`masked = mask_shell(text)` → `masked = text`) | `9965002cf9765434` | `GATE_REGISTRY_SELFTEST pass=15 fail=0` | 0 | **NONE — mutant survives** |
| d | allow duplicate registry names (`if duplicates or wrong_rows` → `if wrong_rows`) | `85dbbd10340a870a` | `GATE_REGISTRY_SELFTEST pass=14 fail=1` | 1 | **arm `duplicate_name_rejected`** |
| e | skip entry-path resolution at the audited revision (`if not exists_at(...)` → `if False and ...`) | `06bf1a0f303f521d` | `GATE_REGISTRY_SELFTEST pass=14 fail=1` | 1 | **arm `unresolved_entry_rejected`** |
| f | enumerate a caller-supplied population instead of `git ls-tree` (`targets = population(...) if --audit-all else list(--audit)` → `targets = list(--audit)`) | `d31f637ddc12725a` | `GATE_REGISTRY_SELFTEST pass=14 fail=1` | 1 | **arm `population_mode_and_digest`** |

Every mutant is a one-hunk diff (`changed_lines=2`, except b which inserts a
4-line fallback block: 1 hunk, 4 `+` lines). Lane bytes restored/untouched:
`lane_sha_before == lane_sha_after == 8b82ac99…f5832` (`lane_restored=yes`).

Raw tallies and the arm text, as emitted:

```
=== a_first_table   selftest rc=1 GATE_REGISTRY_SELFTEST pass=14 fail=1
caught_by selftest FAIL second_table_registered: a row in a second table was not read: {... 'ok': False, 'tables': 1, ...}
=== b_substring     selftest rc=0 GATE_REGISTRY_SELFTEST pass=15 fail=0
caught_by NONE (selftest green on a disabled property)
=== c_comment_only  selftest rc=0 GATE_REGISTRY_SELFTEST pass=15 fail=0
caught_by NONE (selftest green on a disabled property)
=== d_duplicate     selftest rc=1 GATE_REGISTRY_SELFTEST pass=14 fail=1
caught_by selftest FAIL duplicate_name_rejected: a duplicate registry name was accepted
=== e_unresolved    selftest rc=1 GATE_REGISTRY_SELFTEST pass=14 fail=1
caught_by selftest FAIL unresolved_entry_rejected: {'status': 'no_selftest', ...}
=== f_population    selftest rc=1 GATE_REGISTRY_SELFTEST pass=14 fail=1
caught_by selftest FAIL population_mode_and_digest: (2, 'REGISTRY_SETUP empty population: an audit with no paths cannot be met\n')
```

Probe evidence that each mutation is behaviorally live (pristine → mutant):

- **a** `tables=2, status=registered, ok=true` → `tables=1, status=unregistered, ok=false`.
- **b** prose row `` `bash tools/other-tool.sh` (see tools/fixture-tool.sh) ``, auditing
  `tools/fixture-tool.sh`: pristine `status=unregistered` (`no row names tools/fixture-tool.sh`)
  → mutant `status=registered, ok=true`. A prose mention now attributes the tool.
- **c** script with a real `case "$1" in … esac` and a comment
  `# --selftest is not wired yet; only the --run case above exists`:
  pristine `status=no_selftest` → mutant `status=registered, ok=true`.
- **d** two rows named `fixture gate`: pristine `duplicates=[fixture gate], ok=false`
  → mutant `duplicates=[fixture gate], ok=true`.
- **e** row entry `tools/ghost-tool.sh`: pristine `status=wrong_row`,
  detail `entry path tools/ghost-tool.sh does not resolve at …` → mutant falls
  through to `status=no_selftest` (resolution never consulted).
- **f** `--rev WORK --audit-all` on a one-tool fixture: pristine
  `registered=1 … mode=population … REGISTRY=met` rc 0 → mutant
  `REGISTRY_SETUP empty population: an audit with no paths cannot be met` rc 2.

## Findings

**F1 (surviving mutant, property b — attribution).** No selftest arm exercises
the rule "a substring elsewhere in a cell is not an attribution". The v1
fallback can be re-inserted and the tally stays `pass=15 fail=0`; `--audit`
then attributes a path by prose mention alone (`row='prose gate'`),
which is exactly the P-C2 item 2 failure. The nearest arm,
`unregistered_path_rejected`, uses `tools/other-tool.sh`, which is not a
substring of the fixture row, so it cannot see the fallback. Coverage gap, not
a contract change: a `substring_not_attribution` arm (prose row above,
expecting `unregistered`) kills this mutant.

**F2 (surviving mutant, property c — comment-only `--selftest`).** The arm
`comment_only_selftest_rejected` exists but does not test what it names. Its
fixture is
`#!/bin/sh\n# --selftest is deliberately a comment here\nexit 0\n`
(lines 589–594). Direct measurement of `selftest_flag()` on that exact body:

```
selftest-arm fixture   pristine_flag=False mutant_flag=False
probe fixture          pristine_flag=False mutant_flag=True
```

So with shell comment masking removed the arm still passes — for the wrong
reason: the fixture contains no argv marker anywhere, so `selftest_flag` returns
False regardless of masking. The arm is vacuous for this property. A fixture
whose comment sits inside a two-line window that contains `case`/`$@`/`$#`
(there: `case "$1" in … esac` immediately above the comment) distinguishes
pristine (False) from mutant (True) and would kill it. Same class as the r44
silence-oracle false positive the round exists to close.

**F3 (killed, but noted — property e).** The one-site mutation is caught, but
`ok` would have stayed false anyway: the independent `wrong_rows` pre-scan
resolves every row's entry path and reports it as a finding. The property is
redundantly enforced (pre-scan + per-target check); the arm only distinguishes
them through its status assertion (`wrong_row`/`bad_row` + "does not resolve"),
which the mutant breaks by falling through to `no_selftest`. The arm's
status vocabulary was recalibrated during this wave (`bad_row` → `wrong_row`);
my probe accepts both so it measures "entry resolved and reported", not a
status label.

**F4 (no vacuous `met` on an empty population).** On pristine,
`--audit-all` with an empty target list is now `REGISTRY_SETUP` rc 2 (mutant f
shows the guard firing), and `--audit-all` combined with `--audit` is refused
(`REGISTRY_SETUP --audit cannot be combined with --audit-all: population mode
enumerates the declared population and takes no explicit paths`, rc 2), so the
caller cannot narrow the population — probe `f_caller_subset` passes on
pristine. Earlier in the wave the same probe failed on an intermediate build
(`subset_met=true`, rc 0, `registered=1 while the population is 2`); the final
bytes close it.

## `--audit-all` determinism at one revision

Bytes above, revision `3ad8faaa637ae466c61f9427fea1c208bf49ea82` (contract tip):

```
for n in 1 2; do python3 tools/mori-gate-registry.py --rev 3ad8faaa --audit-all \
    > det/run$n.out 2> det/run$n.err; echo "run$n rc=$?"; done
cmp det/run1.out det/run2.out   # stdout byte-identical
cmp det/run1.err det/run2.err   # stderr byte-identical
```

```
run1 rc=1
run2 rc=1
stdout byte-identical
stderr byte-identical
4e555d6075978b5d3f3f357f49b5b2bfc98c5372f14b4558b7c16bb6f857e4bd  det/run1.out
4e555d6075978b5d3f3f357f49b5b2bfc98c5372f14b4558b7c16bb6f857e4bd  det/run2.out
```

Both runs: 36 `audit` lines (33 `tools/*.py|sh` + 3 `round-44/count-c*.py`;
no `round-45/count-c*.py` exists at this revision), 0-byte stderr:

```
tables=7
rev=3ad8faaa637ae466c61f9427fea1c208bf49ea82
mode=population
population_digest=4dbf0ca9823d2af1d6de352b54138bbc261c68a10c9a81e6ef77eb88576292f1
registered=29 unregistered=3 no_selftest=4 duplicate=0 wrong_row=0 tables=7
REGISTRY=unmet
```

`unregistered=3` is the C2 work this round (`mori-disk-rate.py`,
`mori-wave-settlement.py`, `mori-round41-calibration.py`); `no_selftest=4` is
`mori-round19-regressions.py`, `mori-routed-check.py`, `mori-routed-r24.py`,
`mori-silence-cases.sh`. This receipt is pinned to `3ad8faaa` only: at
measurement time the peers' edits to `mori-disk-rate.py`,
`mori-round41-calibration.py`, `mori-routed-r24.py` and the other tools were
still uncommitted, so both counters necessarily describe the committed tip, not
the integration tip. L1 must re-run `--audit-all` once those edits and the new
`round-45/count-c*.py` are committed — until then this is a determinism
receipt, not a `C2=met` receipt.

## Reproduce

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/MutAuditor
TMPDIR=$PWD/box/main python3 drive.py            # six mutants, probes, tallies
TMPDIR=$PWD/box/main python3 probe.py b_substring mutants/b_substring.py
TMPDIR=$PWD/box/main python3 probe.py c_comment_only mutants/c_comment_only.py
```

The driver refuses to silently mis-report: a probe that fails on pristine is
printed as `INCONCLUSIVE`, a mutation that does not change probe behaviour is
`INEFFECTIVE`, and only the cross product (probe flips ∧ selftest red) is
counted as killed.
