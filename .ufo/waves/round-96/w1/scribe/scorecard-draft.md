# SCORECARD round-96 section — draft for the L1 to paste

Source: `.ufo/waves/round-96/contract.md` (frozen; read, not edited). Entering lane HEAD
`66c5518e239eeacd6070be26d78085ef702392cb`. Axes: **calibration** (C1) and **freshness** (C2).
Draft only: `<<...>>` values are for the L1 to fill from the landing receipts. No score move is claimed by this draft.

## Round 96 (2026-11-05, L1 MoriR96, attempt 1) — <<ROUND-96-HEADLINE>>

Entering `66c5518e239eeacd6070be26d78085ef702392cb`; frozen contract `.ufo/waves/round-96/contract.md`
at `<<CONTRACT-COMMIT>>`. Wave `w1`, 10 seats. Axes: **calibration** (C1, score 5) and **freshness** (C2, score 5),
both tied lowest non-retired. Depth is not claimed. No score moves are claimed by this draft.

| Claim | Axis | Predicate | Before | After | Command | Commit |
|---|---|---|---|---|---|---|
| C1 — SCORECARD `Last change` cells against the fleet record | calibration (5) | At revision R, for each of the six axes the `Last change` cell leads with the round and verdict word of the highest admitted mori closure row (any round, no bound) that graded that axis improved or harmed, and the `Score` and `Evidence pointer` cells equal their bytes at `66c5518e239eeacd6070be26d78085ef702392cb`. | `5 mismatches` (`evidence/before-c1-count-c2-through95.txt`) | `<<AFTER>>` | `python3 tools/mori-scorecard-calibration.py <rev> --manifest /home/vgpnk/Projects/shokunin/MANIFEST.json` | `<<COMMIT>>` |
| C2 — SOURCES registry pinned-copy digests re-verified against live bytes | freshness (5) | Every `corpus/SOURCES.md` row that names a recorded sha256 and a pinned copy re-verifies through `tools/mori-source-digest.py`; met iff the command prints `unpinned=0 mismatch=0` with `prefix_only=31` unchanged and `ok=92`. | `unpinned=6` (`evidence/before-c2-digest.txt`) | `<<AFTER>>` | `python3 tools/mori-source-digest.py corpus/SOURCES.md corpus/evidence` | `<<COMMIT>>` |

### Last change cells (L1 to paste the counter's own derivation)

The frozen counter's unbounded derivation for the landing revision — L1 to confirm against the landing run and paste
the confirmed values; the draft does not assert them as measured:

- coverage: `<<AFTER>>`
- operability: `<<AFTER>>`
- depth: `<<AFTER>>`
- freshness: `<<AFTER>>`
- calibration: `<<AFTER>>`
- adjacency: `<<AFTER>>` (no change expected)

### Axis-harm check

No `Score` value changes; the `Last change` cells are the only edited cells. Landing confirmation: `<<AFTER>>`.

### Round-96 correction note (L1)

<<CORRECTION-NOTE: one paragraph stating what the `Last change` cells led with before this round, what the fleet
`MANIFEST.json` records as the highest admitted mori closure grading each axis improved or harmed, and how the new
unbounded counter differs from the round-79 counter's frozen `THROUGH=78` bound.>>

### Round-96 sources & frontier

Census before: exit 0 (`evidence/before-census.txt`). Census after: `<<AFTER>>`.
Rows re-opened this round for C2: S125, S612, S615, S616, S622, S623 (gate block with URL, access date and a located
quote of at most 25 words per row): `<<AFTER>>`.
