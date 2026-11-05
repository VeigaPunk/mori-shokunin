# Round 96 frozen contract — mori (L1 MoriR96, attempt 1)

Entering HEAD `66c5518e239eeacd6070be26d78085ef702392cb` (lane `master`). Freeze: the commit that adds this file, before any wave output.
Axes (SCORECARD): **calibration** 5 (C1) and **freshness** 5 (C2) — both tied lowest non-retired with depth 5
(depth not claimed). Trend targets: discernment (C1), quality (C2 re-verification).
Planner: the L1 holds the §3 planner seat by disclosure (validator refuses `planner`; L0 D1 open with operator).
Frozen predicates below are written by the L1 before any wave seat runs; seats never edit them.

## Claim C1 — calibration: SCORECARD `Last change` cells against the fleet record

Self-assessment under test: each `## Axes` row's `Last change` cell names the highest admitted mori closure that
graded that axis improved or harmed (`MANIFEST.json` rows with `lane: mori` and `admitted: true`; the r50/r79
convention).

Before (measured at `66c5518e239eeacd6070be26d78085ef702392cb`, receipt `evidence/before-c1-count-c2-through95.txt`): the frozen round-79 counter with
`--through 95` reports `C2=unmet mismatches=5`: coverage (cell r56, expect r80), operability (r78 vs r93),
depth (r76 vs r86), freshness (r78 vs r82), calibration (r78 vs r93). The same counter at its default bound
(`evidence/before-c1-count-c2-default.txt`) reports met: the frozen `THROUGH=78` bound hides rounds 79–95.

Predicate P1 (same sentence in the counter's docstring and this receipt): at revision R, for each of the six axes the
`Last change` cell leads with the round and verdict word of the highest admitted mori closure row (any round, no bound)
that graded that axis improved or harmed, and the `Score` and `Evidence pointer` cells equal their bytes at `66c5518e239eeacd6070be26d78085ef702392cb`.

Counter: NEW file `tools/mori-scorecard-calibration.py` (the r79 counter is NOT amended). Command:
`python3 tools/mori-scorecard-calibration.py <rev> --manifest /home/vgpnk/Projects/shokunin/MANIFEST.json`.
Met iff `mismatches=0`, `COLUMNS_UNCHANGED` and `--selftest` green. Its selftest must include a stale-cell fixture
that is unmet (red-before demonstration).

Target: mismatches 0 at the landing revision (before 5). Expected landing cells (the counter's own derivation):
coverage r80 improved; operability r93 improved; depth r86 improved; freshness r82 improved; calibration r93 improved.
Kill rule: any remaining mismatch, a missing stale-cell selftest arm, or any Score/Evidence cell change.
Do-nothing control: SCORECARD unchanged at `66c5518e239eeacd6070be26d78085ef702392cb` → mismatches 5 → unmet (scored above, before freeze).
Axis-harm check: no Score value changes; the `Last change` cells are the only edited cells.

## Claim C2 — freshness: SOURCES registry pinned-copy digests re-verified against live bytes

Self-assessment under test: every `corpus/SOURCES.md` row that names a recorded sha256 and a pinned copy re-verifies
through `tools/mori-source-digest.py`.

Before (measured at `66c5518e239eeacd6070be26d78085ef702392cb`, receipt `evidence/before-c2-digest.txt`):
`DIGEST_CHECK rows=124 ok=86 mismatch=0 superseded=1 prefix_only=31 unpinned=6`; unpinned rows S125, S612, S615, S616,
S622, S623. The round-95 lesson's `unpinned=3` was not the measured value (routed as a mistake below).

Predicate P2: the same command at the landing revision (`python3 tools/mori-source-digest.py corpus/SOURCES.md corpus/evidence`)
prints `unpinned=0 mismatch=0`, `prefix_only=31` (unchanged; the L0 question on prefix-only rows is out of scope) and `ok=92`.

Method constraints: a copy is pinned only if its live bytes, fetched this round with an access date, hash to the row's
recorded digest. A recorded digest is never edited or replaced. Pinned copies go under `corpus/evidence/`. No row is
edited in place except the existing status/recheck/used-by rules (CORPUS rule 2).
Kill rule: a row whose live bytes do not hash to its recorded digest stays unpinned and is named stale (freshness flag);
C2 is then unmet. Declared obstacle before data: S125 names a sibling-repo path (`tsukuroi-shokunin/...`) and the others name
copies absent from `corpus/evidence/`; whether a copy placed there resolves the row is measured by the tool, not assumed.
Target: unpinned 6 → 0, mismatch 0. Do-nothing control: unchanged → unpinned 6 → unmet (scored above).

## Frontier step (CORPUS §2b)

- Census before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0 (`mori ok`,
  42 W04 duplicate-URL warnings; `evidence/before-census.txt`). Must be exit 0 at round end.
- Mistakes (`corpus/lessons/round-96.md` `## Mistakes`): (1) frozen counter bound stale (`THROUGH=78`), captured-by none,
  fixed by C1's unbounded counter; (2) round-95 lesson cited `unpinned=3` with no command; measured 6; captured-by the
  CORPUS count rule, not applied; fixed by the command receipt here.
- Sourced claim: C2 rests on rows S622, S623, S125, S612, S615, S616 re-opened this round (Gate block: URL, access date,
  ≤25-word located quote per re-opened row).

## Not claimed

No new axis beyond calibration and freshness; no exploratory claim; no SHONEN box change; no prefix-only digest repair;
no remediation of any fleet surface.
