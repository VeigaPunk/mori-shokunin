# mori round 91 — frozen contract (attempt 1)

Lane: mori. Round: 91. L1: MoriR91 (planner and integration owner).
Entering revision: `79eaa8cfe5e0b9b1c5ff45f524199d4a123f0520` (lane `master`, clean, remote-equal,
`jj-lane.sh state` ahead=0 behind=0 tracked=0 untracked=0). Frozen before any after-value exists.

Axes and scores (SCORECARD.md `## Axes`): coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6. Retired: drift-pin-r10. The lowest non-retired scores are depth,
freshness and calibration (5). The round's claims are on **calibration** (C1) and **freshness**
(C2), both at the lowest score, so the lowest-axis obligation is met without the stagnation nudge.
No score move is claimed; each claim verifies by its own predicate below.

Carried, not claimed (declared before data; Planned (round 90) items): operability — the
counter-synthesized nonce guard for the round-90 C1 gate (QUALITY 191); depth — the supersession
record for the round-89/90 arm pins. Reason: two claims at the lowest-score axes are the round's
cap; a third claim would need a population this contract cannot size honestly.

## Claim C1 — calibration: the round-87 receipt gate's unarmed clause families are armed

Subject: `.ufo/waves/round-87/count-c2.py` (receipt gate). Named families this claim must arm
(frozen by name; carried from the round-89 contract): `c2-replay-compare-off`, `c2-supersede`,
`c2-absent`, `c2-defeated-accounting`.

Landing constraint (frozen): the landing edits ONLY the selftest block of the subject (appended
arms and the arm-count pin). It never edits a clause's code, so every P2 anchor still occurs exactly
once at R.

Mutant populations (both frozen before data):
* **P1, lane-declared** — `.ufo/waves/round-91/mutants-c1.json`, written by executor `Mo91E01Arms`
  from the subject's clause code. Each entry: `family` (one of the four names), `anchor_old`,
  `anchor_new` (text at R), and `arm` (the selftest arm name the lane expects).
* **P2, independent** — `.ufo/waves/round-91/mutants-c1-independent.json`, written by mutation-tester
  `Mo91M01Mut` against the entering bytes without seeing P1. Same fields. P2 is the attack population.

Counting command: `python3 -I .ufo/waves/round-91/count-c1.py <rev> --repo <clone>`.

Predicate (frozen; this sentence is the counter's condition and the receipt label): at revision R the
command prints `C1=met families=4 unarmed=0 p1_killed=<n> p1_survivors=0 p2_killed=<m> p2_survivors=0 unattributed=0 isolated=0 pins=<a> rev=<12>` and exits 0, where `unarmed` counts the four
named families with no P1 mutant at R; every P1 and P2 mutant is `killed` at R; and `pins` is the
subject's selftest arm count at R (the counter prints it; the landing may change it, recorded as a
supersession of the frozen round-89/90 pins, not as an edit of their receipts).

Kill rule (frozen before data): a mutant is `killed` iff `(rc≠0 ∨ fail>0)`, `failset(out)` is
nonempty, and every FAIL label in it begins with the mutant's declared family name. A red run with
any label outside the family is `isolated`; a red run with no FAIL label is `unattributed`; an
absent anchor is `unanchored`; a red pristine copy is `pristine`. Met iff every field above matches
and exit is 0. Exit 2 is setup, never a pass; a counter whose own selftest is not green exits 2.

Do-nothing control: the same command at the entering revision `79eaa8cf` (P1 absent). Required
output there: `C1=unmet families=4 unarmed=4 ...` and exit 1. The receipt is committed before the
landing commit.

## Claim C2 — freshness: a dated full-census snapshot of the value channel

Subject: the round-86 value channel of the classification (`differs`, `masked`, `absent`), as
defined in the round-86 entry of `SCORECARD.md` and `corpus/lessons/round-86.md`. Raw inputs are
copied byte-exact into `.ufo/waves/round-91/evidence/raw/` (committed). The snapshot is
`corpus/evidence/value-census-2026-11-05.txt`, produced from the raw inputs only.

Counting command: `python3 -I .ufo/waves/round-91/count-c2.py <rev> --repo <clone>`.

Predicate (frozen): at revision R the command prints
`C2=met snapshot=present date=2026-11-05 tokens=<n> differs=<a> masked=<b> absent=<c> unclassified=0 rederived=match mismatches=0 rev=<12>` and exits 0, where the counter re-derives every token's class from the committed raw inputs at R and compares it with the snapshot line for that token; `tokens = differs + masked + absent`; `unclassified` counts tokens with no class; `mismatches` counts tokens whose snapshot class differs from the re-derivation.
Kill rule: met iff every field matches and exit is 0. A snapshot whose date is not `2026-11-05`, a missing raw input, a token listed twice, or a class not re-derivable from the raw inputs keeps the claim unmet. Exit 2 is setup.

Do-nothing control: the same command at `79eaa8cf`: `C2=unmet snapshot=absent` and exit 1.

## Frontier step (protocol §2b, round-91)

- Mined mistake: round-90 `corpus/lessons/round-90-verifier-spotcheck.md` defect R8 — the admitted
  row S615's recorded sha256 is not the pinned copy's digest (prefix matches, full digest does not).
  Captured-by: none (the census validator reads no pinned digest). Fix: a digest check over the
  pinned copies, shown able to fail on a corrupted copy in scratch before it counts.
- Sourced claim: C1 rests on at least one `corpus/SOURCES.md` row opened this round (mutation-testing
  practice, cited in the knowledge entry).

## Out of scope (declared before data)

No change to the fleet root, sibling lanes, MANIFEST.json, `.ufo/state/`, the watchdog log, host
configuration, routing, or domain trees. No pacman. No pushes outside the mori lane remote and the
fleet repo.

## Ordering (binding)

1. This contract and P2 (`mutants-c1-independent.json`) committed before any candidate counter runs.
2. Do-nothing control receipts at `79eaa8cf` committed (`evidence/controls-r91.txt`) before any landing.
3. Landing commit(s) through `jj-lane.sh`; after-receipt `evidence/after-r91.txt` at the landing revision.
4. Any change to a frozen predicate, population, kill rule or landing constraint after step 2 voids the claim; nothing is rewritten.
