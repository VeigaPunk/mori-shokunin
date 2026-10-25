# RevDuplicates — duplicate target rows vs a false pass

**Seat:** L1Mori46.RevDuplicates (reviewer, leaf — no subagent dispatch)
**Scope:** frozen predicate `.ufo/waves/round-46/count-repins.py` (MORI_R45_REPINS); question: can duplicate target rows produce `mismatches=0 rows=4` (false green)?
**Method:** empirical run of the frozen predicate against synthetic SKILL.md snapshots built in `/tmp/revdup/` (report-only scratch; nothing written into the lane repo except this file). No installs; pacman untouched.

## Baseline confirmation

| Case | Input | Output | rc |
|---|---|---|---|
| Control (committed snapshot) | `.ufo/waves/round-46/control-skill.md` | `MORI_R45_REPINS mismatches=4 rows=4` (stale/missing 1/2/5/3 pins per row) | 1 — red as required |
| Green candidate | all four target rows exactly once, each containing its needles | `MORI_R45_REPINS mismatches=0 rows=4` | 0 |

The green candidate confirms the only green path: exactly one conforming row per target, pins present.

## Duplicate probes (conforming duplicates — match the `| <row> |` prefix)

| Case | Duplicate inserted on top of full green | Result | rc |
|---|---|---|---|
| dup C1 full row | `r45 ledger counter (C1)` ×2 | `expected one row, found 2` | 1 |
| dup r44 plain row | `r44 gate registry (C2)` ×2 | `expected one row, found 2` | 1 |
| dup superseded row | `r44 gate registry (C2) — write scope superseded` ×2 | `expected one row, found 2` | 1 |
| dup r45 C2 row | `r45 gate conformance (C2)` ×2 | `expected one row, found 2` | 1 |
| dup, stale copy (no needles) | canonical row + copy lacking pins | `expected one row, found 2` | 1 |
| triplicate | `r45 ledger counter (C1)` ×3 | `expected one row, found 3` | 1 |
| dup with extra trailing cell text | row + `| r45 ledger counter (C1) | gate | extra-cell |` | `expected one row, found 2` | 1 |
| dup with trailing space | row + same line ending in a space | `expected one row, found 2` | 1 |
| dup with CRLF line ending | row again with `\r\n` terminator (mixed or pure) | `expected one row, found 2` | 1 |

Every conforming duplicate of any of the four targets — full, stale, triplicated, extra-cell, trailing-whitespace, or CRLF-terminated — forces `len(matches) != 1` and yields rc 1 red. No conforming-duplicate arrangement produced `mismatches=0`.

Per-row identity is prefix-exact: `startswith("| " + row + " |")`. Note `r44 gate registry (C2)` does **not** match the superseded row `r44 gate registry (C2) — write scope superseded` (the matcher requires ` |` immediately after the name, and the superseded row has ` —` there), and conversely. The two r44 rows are checked independently; no cross-contamination.

## Non-conforming copies (the only green-with-two-copies scenario)

| Case | Input | Result |
|---|---|---|
| tab instead of space after row name | full green + `| r45 ledger counter (C1)\t| …` | `mismatches=0 rows=4` rc 0 |
| double leading space after pipe | full green + `|  r45 ledger counter (C1) | …` | `mismatches=0 rows=4` rc 0 |

A second physical copy whose spacing deviates from the exact `| <row> |` prefix is invisible to the matcher and does not trip the count. This is not a false pass: the predicate's contract is "only when four specific SKILL.md rows match measured pins", and the four pattern-matched rows still match and carry the pins. The invisibility is a documented strictness limitation (near-duplicates evade the count), not a duplicate-induced green.

## Findings

1. **[Safe] Conforming duplicate target rows cannot yield a false pass.** Every duplicate of any of the four targets (full/partial/triplicate/extra-cell/trailing-space/CRLF) moves the count to ≥2 and produces `expected one row, found N` with rc 1. Deterministic — `len(matches) != 1` is the guard (`.ufo/waves/round-46/count-repins.py:30`). Falsification attempt fails: no duplicate input reports `mismatches=0`.
2. **[Limitation, not a defect] Prefix-exact matching is blind to spacing variants.** A copy of a target row that deviates from `| <row> |` (tab, extra space) is not counted, so it neither fails nor passes the check; the verdict stays green if the one conforming row is healthy. If a duplicate *replaced* the conforming row in this form it would be caught as `found 0` (probe 08: superseded row in place of the plain row → `expected one row, found 0`). No input with two or more rows matching the same target identity ever yields green.
3. **Reported-value sanity:** the summary line always prints `rows=4` (`len(ROWS)`, constant) — duplicate inputs do not alter the row count, only `mismatches`.

## Residual risk / verification gaps

- The probes exercise the four frozen targets with synthetic minimal rows; they reuse the exact needle strings from `ROWS`. Full-size live-table reproduction was not needed: the matcher only inspects `startswith` plus substring needle presence, and the live rows at `SKILL.md:184/190/191/194` were confirmed present and conforming by grep.
- Invisible (whitespace-variant) duplicates are out of the predicate's view by design; if the lane wanted structural uniqueness enforcement, that would be a new check, not a repair to this one.

## Reproduction

Commands (inputs under `/tmp/revdup/`):
- Baseline: `python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md` → rc 1
- Green: `python3 .ufo/waves/round-46/count-repins.py /tmp/revdup/00_green_baseline.md` → rc 0
- Duplicates: cases `01`–`16` in `/tmp/revdup/`; generator scripts `gen.py`, `gen2.py`, `gen3.py` (all under `/tmp/revdup/`), outputs re-printed above.
