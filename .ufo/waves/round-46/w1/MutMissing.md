# MutMissing — missing target row probe against count-repins.py

Seat: `MutMissing` (mutation-tester). Probe: delete one entire target row from an
isolated scratch copy of the live `SKILL.md` and run the frozen counter on the
result. No source/production/sibling files edited; no git/jj mutations; no tool
installs.

## Detector

- `count-repins.py` (`.ufo/waves/round-46/count-repins.py`)
  sha256 `ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327`
- Behavioral contract: `MORI_R45_REPINS mismatches=0 rows=4` (exit 0) iff each of
  the four `ROWS` entries finds exactly one `| <row> |`-prefixed line containing
  all its needles; otherwise exit 1 with per-row error lines.

## Inputs and hashes

| Input | sha256 |
|---|---|
| Live `SKILL.md` (pristine baseline) | `15a3385d9329a0cb2d6fea931e3a032ec3ef0630fa9de152a78a402d5eb6dc47` |
| `control-skill.md` (prior committed snapshot, do-nothing control) | `ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad` |
| Mutant scratch copy `skill-missing-row.md` | `158d5b5accf8800dda1d210a2cd2b206ae3429df736612721a45bcef0c5c7c69` |
| Counter script | `ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327` |

## Mutation

Smallest behavior-bearing point: remove the whole target row
`| r44 gate registry (C2) | …` (line 184 of pristine `SKILL.md`) from the
isolated scratch copy `~/.scratch/MutMissing/skill-missing-row.md` (created by
`cp SKILL.md`, byte-identical at creation). Target-row prefix matches in the
mutant: 4 → 3 (the other three rows `r45 ledger counter (C1)`,
`r45 gate conformance (C2)`, `r44 gate registry (C2) — write scope superseded`
remain present). Nothing else changed.

## Detector runs (same bounded detector, pristine / control / mutant)

1. **Pristine** — `python3 .ufo/waves/round-46/count-repins.py SKILL.md`:
   output `MORI_R45_REPINS mismatches=0 rows=4`, exit **0** (green arm of the
   frozen predicate holds).
2. **Control** — `python3 …/count-repins.py .ufo/waves/round-46/control-skill.md`:
   output `MORI_R45_REPINS mismatches=4 rows=4`, exit **1**:
   ```
   r44 gate registry (C2): stale/missing 1 pin(s)
   r45 ledger counter (C1): stale/missing 2 pin(s)
   r45 gate conformance (C2): stale/missing 5 pin(s)
   r44 gate registry (C2) — write scope superseded: stale/missing 3 pin(s)
   ```
   i.e. the do-nothing prior snapshot remains red, as required.
3. **Mutant** — `python3 …/count-repins.py .scratch/MutMissing/skill-missing-row.md`:
   output `MORI_R45_REPINS mismatches=1 rows=4`, exit **1**:
   ```
   r44 gate registry (C2): expected one row, found 0
   ```
   The removed row is reported exactly; no other row errors appear.

## Verdict

**KILLED.** The counter detects the missing target row: the mutation changes the
verdict from green (`mismatches=0`, exit 0) to red (`mismatches=1 rows=4`,
exit 1) with the precise per-row finding. It is not a surviving mutant.

## Restoration evidence

- Pristine `SKILL.md` sha256 before and after the probe: `15a3385d…` —
  unchanged; no live-file edit occurred.
- Mutant scratch copy is disposable; deleted row line 184 is recoverable
  byte-for-byte from pristine `SKILL.md` (same hash as creation source). No
  restore was needed since the detector run was non-destructive on the pristine.
- No files written outside the seat's own scratch copy and this report.
