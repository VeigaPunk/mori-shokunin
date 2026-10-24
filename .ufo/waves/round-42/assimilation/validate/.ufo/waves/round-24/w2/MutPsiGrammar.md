# MoriR24.MutPsiGrammar — wave 2 falsify report (C2 selftest sensitivity)

Role: mutation tester (leaf). Claim probed: C2 — `tools/mori-pressure.py --selftest`
must PASS 12/12 over the frozen cases. Mutant family assigned: line grammar loosened
(extra fields, duplicate kinds, or a negative total accepted). Verdict: all three
mutants SURVIVED — the frozen suite does not constrain any of the three grammar
loosenings.

## Setup (evidence)

- Clone: `/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiGrammar` (`git clone --no-hardlinks
  /home/vgpnk/Projects/shokunin/mori-shokunin`), checked out at measured lane tip
  `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (`git rev-parse HEAD` = a730ecf…).
- Frozen cases provenance: blob of `tools/fixtures/mori-pressure/cases.json` at tip
  equals the frozen blob at `f6a29702` (both sha256
  `aeb80ea080436cb344df8dba7ec19eeecc639e347ae87a14bc6835631f28ca94`);
  `git log --oneline -- tools/fixtures/mori-pressure/cases.json` shows only f6a2970
  ("freeze the 12 C2 pressure cases ..."); the tool landed later at `6ee6248`.
- Baseline (pristine, same clone, pinned tip):
  `python3 -I tools/mori-pressure.py --selftest` →
  `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0. Baseline is healthy; kills would be meaningful.
- Environment: python3 3.14.8 (system). No tool installs or upgrades were needed or
  performed (RULES.md read; tooling directive satisfied — nothing installed).
- Detector in every run: `python3 -I tools/mori-pressure.py --selftest`, exit code captured.

## Mutants (each applied alone to the clone, smallest single-point change)

| # | Loosening | Code change (one point) | Behavior probe (confirms loosening acts) | Selftest output | Verdict |
|---|---|---|---|---|---|
| A | extra fields accepted | `LINE_RE` line 123: `total=([0-9]+)$` → `total=([0-9]+)(?: .*)?$` | line `some … total=9 junk=1` now parses `ok`; `avg10=abc` still `malformed`; duplicate kind still `malformed` | `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0 | SURVIVED |
| B | duplicate kinds accepted | `_parse_resource`: removed duplicate-kind rejection block (original lines 177–179) | two `some` lines in one file now parse `ok` (second overwrites first); `avg10=abc` still `malformed` | `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0 | SURVIVED |
| C | negative total accepted | `LINE_RE` line 123: `total=([0-9]+)$` → `total=(-?[0-9]+)$` | `total=-9` now parses `ok`; `avg10=abc` still `malformed` | `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0 | SURVIVED |

Mutant diffs (recorded during runs): A and C are one-line regex changes within `LINE_RE`
(`git diff` showed exactly the one line changed each time); B is the 3-line deletion of
the `if kind in kinds:` guard.

## Why nothing kills them (sensitivity analysis)

Programmatic sweep of every line in every frozen snapshot (87 lines total across all
12 cases, P01–P12), checking each line against the original regex and against mutants A
and C:

- lines newly accepted by mutant A (extra fields): 0
- lines newly accepted by mutant C (negative total): 0
- lines rejected by the original regex: exactly 1 — P08's `avg10=abc` line, which stays
  rejected under all three mutants (probed: still `malformed`).

Duplicate-kind coverage: the baseline passes 12/12, and the pristine parser maps any
duplicate-kind line to `malformed`, so the suite contains no file with two same-kind
lines — mutant B is unexercised by construction.

The frozen suite exercises the grammar only through P08 (non-decimal `avg10`) — i.e. only
the "invalid *value* shape" direction, and only mid-line. The three loosening directions
(extra trailing fields, duplicate kinds, negative totals) are all absent from the data.

## Missing cases (would kill the mutants; none were added — cases.json untouched)

Precise names, each expecting the affected resource `state: malformed`, verdict
`PRESSURE_PARTIAL`, exit 0:

1. Extra fields — e.g. **P13 "trailing extra field after total"**: one file with
   `some avg10=1.23 avg60=0.45 avg300=0.12 total=98765 junk=1` (any extra space-separated
   token after `total=N`; would kill mutant A).
2. Duplicate kinds — e.g. **P14 "duplicate some line"**: memory (or cpu/io) file with two
   `some` lines; or irq with two `full` lines (would kill mutant B).
3. Negative total — e.g. **P15 "negative total"**: a line like
   `some avg10=1.00 avg60=0.50 avg300=0.25 total=-5` (would kill mutant C).

## Restoration evidence

- After each of A, B, C: `git checkout -- tools/mori-pressure.py` in the scratch clone.
- Final state of the clone: sha256 `tools/mori-pressure.py` =
  `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` (pristine hash),
  sha256 `cases.json` = `aeb80ea…` (frozen blob), `git status --porcelain` empty
  (after removing the probe-generated `tools/__pycache__/`), HEAD still `a730ecf…`.
- Lane repo touched only by this report file. No fleet repo, sibling lane, jj state, or
  lane Git index was mutated; no probes or hosts written.

## Conclusion

Mutants A, B, C all survive as `PASS 12/12` — a coverage finding, not a contract change.
The declared after-value remains reproducible at tip (baseline PASS 12/12 recorded above).
The frozen suite is sensitive to mid-line value-shaped grammar violations (P08) but not to
the loosening directions in the assignment; the three missing cases above would close the
gap.
