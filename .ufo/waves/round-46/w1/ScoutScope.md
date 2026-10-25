# ScoutScope — repair scope: detection/report scope and sibling domains

Wave: mori-r46-calibration-repair. Lane: mori-shokunin.
Question: does the repair change detection/report scope, or touch sibling domains?

## Method

- `git status --porcelain=v1 -b`, `git log --oneline -8`, `git diff` / `git diff --cached` (full, plus `-U0` and `--word-diff` on SKILL.md).
- Ran the frozen counter (read-only) on three inputs: repaired working-tree `SKILL.md`, the round's control snapshot, and `HEAD:SKILL.md` materialized to `/tmp`.
- `cmp` control vs `HEAD:SKILL.md`; `sha256sum` of the counter vs the hash claimed in SCORECARD.md; needle-presence grep on the repaired SKILL.md.

## Findings

### 1. Detection/report scope — unchanged

- Instrument: `.ufo/waves/round-46/count-repins.py` (new this round, untracked; not part of the tracked repair diff). Its detection surface is frozen: a hardcoded `ROWS` dict of exactly 4 row titles (`r44 gate registry (C2)`, `r45 ledger counter (C1)`, `r45 gate conformance (C2)`, `r44 gate registry (C2) — write scope superseded`), per-row needle containment (`startswith("| <row> |")`, then `needle not in row`), one report line `MORI_R45_REPINS mismatches=N rows=4` plus per-row error lines, exit 0/1. The script reads exactly one file argument, spawns no subprocess, writes nothing.
- The tracked repair edits only those four existing SKILL.md rows (git diff shows 4 changed lines, one per key; titles, row count 1 each, and seven-cell structure unchanged). What changed are cell values only: selftest tallies (`pass=6`→`pass=15`; `pass=10`→`pass=16`; `pass=10`→`pass=14`), digests (`5f2deea0…`, `153423c4…`, `9850b3fc…`, `8b82ac99…`), line counts ("743 lines"), and explanatory wording.
- Observed behavior (predicate as frozen):
  - Repaired `SKILL.md` → `MORI_R45_REPINS mismatches=0 rows=4`, exit 0.
  - Control `.ufo/waves/round-46/control-skill.md` → `mismatches=4 rows=4`, exit 1 (stale/missing pins: 1/2/5/3 per row). `cmp` shows the control is byte-identical to committed `HEAD:SKILL.md` (empty diff), i.e. the do-nothing control is exactly the prior committed snapshot and stays red.
- The instrument's own hash claim in SCORECARD.md (`ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327`) equals the actual `sha256sum` of the on-disk counter.
- Conclusion: the repair does not change what is detected (same four rows, same needle set, same mismatch granularity) nor how results are reported; it only changes the values of already-detected cells to equal measured pins.
- Note: some needles occur in more than one row in the repaired file (`GATE_REGISTRY_SELFTEST pass=15 fail=0` ×3, `8b82ac99…` ×3, "743 lines" ×3), but the predicate checks are per-row containment, so cross-row occurrences do not alter detection.

### 2. Sibling domains — no writes outside the lane repo

- Tracked repair diff is confined to four in-lane files;  `w/LOG.md` — appended round-46 correction entry (append-only, documentary).
  - `w/SCORECARD.md` — appended "Round 45 closure-reconciled claims" + "Round 46 calibration repair" sections; existing score cells untouched (scores remain coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6; "No score delta is claimed").
  - `w/SKILL.md` — the four target registry rows above.
  - `w/corpus/SOURCES.md` — one added row `S474 | mori AXES calibration criterion — /home/vgpnk/Projects/shokunin/AXES.md | own-work | A | …`.
- Untracked additions are also in-lane: `.ufo/waves/round-46/` (spec, dispatch, counter, control snapshot, w1 reports) and `corpus/lessons/round-46.md`; plus mutation-tester scratch `.scratch/MutMissing/`, `.scratch/MutStaleC2/` (peer run artifacts).
- The only path outside the lane repo referenced anywhere is `/home/vgpnk/Projects/shokunin/AXES.md` (fleet root), named in S474 and the lesson as the calibration-criterion source. It is referenced read-only (quote at `AXES.md:15`); the file exists (5160 bytes) and is not modified. No other fleet/lane files are touched, and no git/jj mutations were made.

## Confidence / unknowns

- High confidence on both questions: all observations are direct (read-only runs of the frozen counter, full diffs, byte comparisons).
- Outside this seat's scope (peers cover): whether the embedded digests/tallies themselves match committed tool bytes (ScoutDigests, ScoutTally, ExecAuditorLines) and whether the round-45 29/29 freeze-manifest claim correction is exact (ExecFreeze). The repair's S474 row adds one row to the lane's own sources census surface — within-lane detection surface, not sibling.
