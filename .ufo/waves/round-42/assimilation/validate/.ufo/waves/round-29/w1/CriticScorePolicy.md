author: MoriR29.CriticScorePolicy (critic, wave 1, leaf seat)

# Round 29 C1: what score the admitted closure record supports, per axis, at 7118f320

Scope: this is a falsifier for the C1 Axes-table fix, written before the fix exists. Inputs were read only with read-only git:
`git show 7118f320:SCORECARD.md`, `git show 7118f320:corpus/lessons/round-{12..28}-verifier-spotcheck.md`, and
fleet `git show 63729047:MANIFEST.json` and `63729047:.ufo/reports/round-2{4..8}/mori.md`. I did not open, grep or run
the oom-killers tool, and I opened no round-26/27/28 wave report. I installed no tools, made no writes outside this
file, and fetched no URLs.

## Bottom line

- Five of the six rows are settled by a number that a closure states, or by an explicit lane "held" proposal that an
  admitted closure did not dispute: coverage 6, operability 7, depth 5, calibration 5, adjacency 6.
- Freshness is the only contested row. The record supports 5. A score of 6 is **unprovable from committed bytes**: no
  closure states 6, the round-28 declaration does not propose 6, and the round-28 closure records "no held score
  changed" without ruling on the 5 → 6 proposal.
- Three of the four cases the assignment calls "improved with no number" are not ambiguous. In round 26 (freshness
  and coverage) and round 28 (operability), the lane itself proposed "held" in the section the closure read.
- Policy defect: the count-c1 mismatch kinds cannot detect a score overclaim. Kind 4 accepts any score in a row that
  cites an admitted `improved` closure, so freshness 9 or operability 8 citing the round-28 spot-check would count as
  `mismatches=0`. The fix is in the last section.

## The closure convention: "improved" is a verdict, not a score point

Admitted closures have repeatedly granted `improved` while stating, or keeping, a held score:

| Evidence | Verbatim (at most 25 words) |
|---|---|
| `corpus/lessons/round-12-verifier-spotcheck.md:17` | "Depth improved (… score 4→5); calibration improved … score held 5 because the outside reviewer could not derive 6; coverage improved" |
| `corpus/lessons/round-14-verifier-spotcheck.md:87` | "holds coverage6/operability7/depth5/freshness5/calibration5/adjacency6. Repair is not an extra scalar point." (the same closure rules coverage and adjacency `improved` at :91, :96) |
| `corpus/lessons/round-15-verifier-spotcheck.md:177` | "coverage \| improved \| … owned score6 held" |
| `corpus/lessons/round-16-verifier-spotcheck.md:128` | "coverage \| improved \| … Score 6 held." |
| MANIFEST rounds[339] (r14) notes | "no extra scalar point" |
| MANIFEST rounds[405] (r20) notes | "No numeric score increase is inferred" |
| MANIFEST rounds[427] (r22) | "ADMITTED for one bounded calibration capability at held score"; "all scores held (calibration 5→5)" |
| `corpus/lessons/round-24-verifier-spotcheck.md:68`, `:88` | calibration "Score 5 → 5."; coverage "Ruling: improved, bounded. … Score 6 → 6." |

Count: the lane spot-check files record `| <axis> | improved |` lines in admitted rounds as follows. Coverage: 14,
15, 16, 24, 25, 26. Operability: 18, 28. Freshness: 26, 28. Calibration: 18, 24, 25. Adjacency: 14, 18. Depth: only
round 27, which was not admitted. (This is a loop of `git show 7118f320:<file> | rg "^\| <axis> \| improved \|"` over
rounds 12–28, filtered by MANIFEST `admitted`.) That is 15 admitted `improved` verdicts, and none of them raised a
score unless a closure stated the number. Only two raises appear in rounds 12–28:

1. Depth 4 → 5 in round 12: stated by the closure (`round-12-verifier-spotcheck.md:17`).
2. Coverage 5 → 6 in round 12, plus operability 6 → 7 from the rejected round 13: neither was stated when it was
   made. Both were ratified by name later, at `round-14-verifier-spotcheck.md:87`. This is the only precedent that
   favours raising freshness (see the freshness row below).

## Per-axis verdict table

| Axis | Standing at 7118f320 | Supported score | Pointer for the number | Last admitted `improved` closure (R; required citation under contract kind 1) | Confidence |
|---|---|---|---|---|---|
| coverage | 6 | **6** | `round-24-verifier-spotcheck.md:88` "Score 6 → 6"; `round-26-verifier-spotcheck.md:126` records "coverage 6 → 6 pending closure" with no objection | R = 26 (`round-26-verifier-spotcheck.md:133`). The row cites only round 24, so it is a stale closure | high |
| operability | 7 | **7** | `round-14-verifier-spotcheck.md:87` "operability7"; `round-16-verifier-spotcheck.md:129` "Score 7 held."; `round-25-verifier-spotcheck.md:128` "held 7"; SCORECARD:1771 has the lane's "operability held at 7" | R = 28 (`round-28-verifier-spotcheck.md:93`). The row cites no closure, so it is a stale closure | high |
| depth | 5 | **5** | `round-12-verifier-spotcheck.md:17` "score 4→5"; `round-25-verifier-spotcheck.md:127` "held 5"; `round-28-verifier-spotcheck.md:94` "held" | none. Round 27 is the only `improved` (:102), and MANIFEST rounds[468] has `admitted: false` | high |
| freshness | 5 | **5** (6 is unprovable) | `round-14-verifier-spotcheck.md:87` "freshness5"; `round-25-verifier-spotcheck.md:129` "held 5"; `round-26-verifier-spotcheck.md:126` records "freshness 5 → 5". No closure after round 26 states a number | R = 28 (`round-28-verifier-spotcheck.md:92`). The row cites `corpus/README.md` only, so it is a stale closure | medium on 5; 6 is unprovable |
| calibration | 5 | **5** | `round-24-verifier-spotcheck.md:68` "Score 5 → 5"; `round-12-verifier-spotcheck.md:17` "score held 5"; MANIFEST rounds[427] "calibration 5→5"; `round-25-verifier-spotcheck.md:49` lists the six table scores (calibration is the fifth, 5) as "all equal" | R = 25 (`round-25-verifier-spotcheck.md:124`). The row cites round 24, so it is a stale closure | high |
| adjacency | 6 | **6** | `round-14-verifier-spotcheck.md:87` "adjacency6", in the same closure that rules adjacency `improved` at :96; `round-25-verifier-spotcheck.md:49` (sixth score, 6, "all equal"); SCORECARD:1194 has the lane's round-19 "adjacency6→6" | R = 18 (`round-18-verifier-spotcheck.md:124`). The row cites no closure, so it is a stale closure | medium-high |

Expected count-c1 result at `7118f320`, by hand [INFERENCE: count-c1.sh is not in the lane tree at 8a45cefe, so I
did not run it]:

- Kind 1 (stale closure): 5 mismatches, on coverage, operability, freshness, calibration and adjacency.
- Kind 2 (unadmitted last change): 0. The Last change rounds are 12, 14 and 1. Rounds 12 and 14 are `admitted` in
  MANIFEST rounds[313] and rounds[339], and round 1 is below 12, so the rule does not apply to it.
- Kind 3 (dead pointer): 0. The only `path:L` tokens are `round-24-verifier-spotcheck.md:68` and `:88`, and that file
  has 148 lines.
- Kind 4 (score without basis): 0, because no score has moved yet.
- Total: `mismatches=5`. If BuildCountC1's before-count differs, one of the two is wrong.

## The four "improved, no number" cases, argued both ways

**Round 26, freshness.** Raise: the closure says `improved` (:132). Hold: the lane's round-26 measured outcome
proposed "freshness 5 → 5 held pending closure" (SCORECARD:1608), and the closure read it back as "the round-26
sections hold freshness 5 → 5" (:126). Raising on round 26 would credit more than the lane asked for and the closure
saw, so a non-author would call it an overclaim. Holding is not an underclaim. **Hold 5.**

**Round 26, coverage.** The case is identical: "coverage 6 → 6 held pending closure" (SCORECARD:1609), read back at
:126. **Hold 6.**

**Round 28, operability.** Raise to 8: the closure says `improved` (:93). Hold: the lane wrote "operability held at
7 (case pinning strengthens an existing capability)" (SCORECARD:1772). The closure read the same diff ("append-only
… no held score changed", :78), and no artifact anywhere proposes 8. A raise to 8 is a plain overclaim. **Hold 7.**

**Round 28, freshness.** This is the only real dispute.

- Arguments for raising to 6:
  - The lane proposed "freshness 5 → 6 proposed" (SCORECARD:1771).
  - The closure ran `git diff 6ebd518f 1fc6bb0e -- SCORECARD.md` (:78), so it saw that cell, and it did not refuse
    it. In round 12, by contrast, the closure refused calibration 6 by name.
  - Round 12's coverage 5 → 6 (lane, SCORECARD:615) also met a silent closure `improved` (:17) and still stood. It was
    ratified two rounds later at `round-14-verifier-spotcheck.md:87`.
  - So a reviewer reading round 12 as precedent could call a hold an underclaim.
- Arguments for holding at 5:
  1. The round-28 declaration offers no 6. Its axis cell reads "freshness 5 (tied lowest …)" (SCORECARD:1755). The 6
     appears only in the measured-outcome cell, written after the results. The round-29 score policy
     (`contract.md:47-49`) allows a change only where "the admitted round's declaration proposed it". Read literally,
     that test fails.
  2. The judged artifact, fleet `.ufo/reports/round-28/mori.md` at 63729047, proposes no number. Grepping it for
     `propos|→ ?6|held` finds no freshness proposal; the only score mention is "score 5, tied lowest" at :7.
  3. The closure's only statement about scores is "no held score changed" (:78). That describes the diff; it is not
     an award.
  4. Every admitted `improved` verdict since round 14 has kept its score unless a closure stated the number (table
     above). The round-12 coverage raise was ratified by a later closure, never by the lane alone. Raising freshness
     now would be the lane ratifying its own proposal: two authorities over one number.
  5. The round-29 contract holds freshness as "Held, not claimed" (`contract.md:84`). A C1 calibration fix that
     raises freshness would move an unclaimed axis by self-ratification.

Which choice draws which label:

- A non-author closure would call raising to 6 an **overclaim**. It harms calibration, the very axis C1 claims; round
  20 closed `rejected-harmed` with calibration harmed (MANIFEST rounds[405]).
- A reviewer applying the round-12 precedent might call holding at 5 an **underclaim**. Holding harms no axis, and the
  contract provides that exact form: "improved (closure round N), score held" (`contract.md:49`).

The risks are asymmetric. **Hold 5**, and write the cell so the proposal stays visible and is routed to the closure:

```text
| freshness | 5 | improved (closure round 28, `corpus/lessons/round-28-verifier-spotcheck.md:92`), score held: the round-28 measured outcome proposed 5 → 6 (`SCORECARD.md:1771`); no admitted closure states 6 | round 28 (improved, score held at 5; 6 unproven) |
```

## Rows where the honest answer is `unprovable`

1. **Freshness = 6: unprovable** from committed bytes, for the reasons above. Freshness = 5 is supported by the
   convention, but it has not been restated by any closure since round 26 (:126).
2. **Adjacency: partial provenance gap.** The latest admitted adjacency `improved` is round 19 (MANIFEST rounds[398]).
   Its spot-check is "Inline in this durable closure row" in MANIFEST, and no lane `round-19-verifier-spotcheck.md`
   exists. Kind 1 therefore picks R = 18. A row whose prose calls round 18 "the last closure" would carry false
   provenance; one that says "cites round 18 per kind 1" is accurate. The score of 6 is not affected: it is
   restated at `round-25-verifier-spotcheck.md:49`. Freshness (round 21) and calibration (rounds 19, 21, 22) have the
   same MANIFEST-only closures, but their R is later, so they are not affected.
3. **Depth = 6: not unprovable but refused.** Round 27 verified the depth work (:102), but the round closed
   `rejected-honest-stop`. Raising on it fails kind 2 and the policy's "admitted" test, and round 23's honest-stop
   closure says "Scores may hold" (`round-23-verifier-spotcheck.md:8`).

## Counterexample against the counter, and the smallest safe correction

- **Counterexample.** Suppose the fix writes freshness `6`, or operability `8`, and cites
  `corpus/lessons/round-28-verifier-spotcheck.md` in the row. Kind 1 is satisfied: R = 28 is cited. Kind 4 is
  satisfied: the score differs from 7118f320, but the row cites an admitted round whose per-axis line reads
  `improved`. Kinds 2 and 3 are unaffected. The counter prints `mismatches=0` and `C1=met`, so the score policy at
  `contract.md:47-49` is enforced only by the author of the fix.
- **Axes affected.** Calibration directly. Freshness and operability are the axes whose scores could be overclaimed
  without detection.
- **Defect or tradeoff.** This is a fixable defect, not a tradeoff. The counter is landed before the table edit,
  following the round-28 A1 precedent, so it can be amended before any data.
- **Smallest safe correction.** Amend kind 4 before the table edit, then re-measure the before value:

```text
4. Score without basis (amended). The row's score must equal its score at 7118f320 unless some admitted round N's
   `corpus/lessons/round-N-verifier-spotcheck.md` at <rev>, cited in the row, holds a line that names the axis and
   the new score as a number (e.g. `Score <old> → <new>` or `<axis><new>`). A score that differs with no such line
   is a mismatch. Under the record at 7118f320 no such line exists for any axis, so every score is pinned:
   coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6.
```

Also pin the policy wording: "declaration" in `contract.md:48` means the `## Round N declaration` table, not the
measured-outcome cell. Otherwise the L1 decides freshness alone, which is the duplicate-authority problem described
above.

## Checks for the L1

- `git show 7118f320:corpus/lessons/round-28-verifier-spotcheck.md | sed -n '78p;92,93p'`
- `git show 7118f320:SCORECARD.md | sed -n '1755p;1771,1772p'`
- `git -C /home/vgpnk/Projects/shokunin show 63729047:MANIFEST.json | jq '.rounds[468].admitted, .rounds[476].verdicts'`
- Compare BuildCountC1's before-count with the expected `mismatches=5` (all of kind 1).
