# Round 25 wave 2: CriticC1Admission (critic, C1 as an admission claim)

Seat: `MoriR25.CriticC1Admission`, leaf critic, no subagents. Lane tip read: `07a31ae8e22514bbc603afa13f2de7c8b2424cca`
(`jj-lane.sh state`: `local=remote=07a31ae8…`, `ahead=0`). Code ran only in a private clone
`/fast/scratch/hyaku/mori-r25/w2-CriticC1Admission` (removed when done). RULES.md read (`~/.omp/agent/RULES.md:1-14`).
No tool installed or upgraded.

## Verdict: weakened

The declared after-value reproduces. As a calibration admission claim, though, it is overstated. A strict closure
would admit C1 only as **improved, bounded, calibration 5 → 5**. It would count at most two of the four items as
self-assessment mismatches (D1 and D5). It would read D2 and D3 as record and quality repairs, and it would read D5
as an item added after the measurement against a self-written pin. The three-rounds-running sentinel is tripped
under the class reading that the contract itself defines. That trip binds round 26; it is not a reason to reject
round 25.

## Re-measurement (run, not taken from evidence)

`python3 -I -B tools/mori-routed-r24.py --repo . --rev <rev>` in the private clone, using the tip tool:

| Rev | exit | items | held | mismatches | hygiene | Per-item result |
|---|---|---|---|---|---|---|
| `07a31ae8` (tip) | 0 | 4 | 4 | 0 | held | D1, D2, D3, D5 all held |
| `28b79d3d` (base) | 1 | 4 | 0 | 4 | red | D1 `evidence_file_missing`; D2 seven sub-reasons; D3 `no_line_with_correction_s07_and_pass_marker`; D5 `axis_score_mismatch` coverage 5≠6, operability 6≠7, depth 4≠5 |
| `e54b644b` (A1 tool landed) | 1 | 4 | 3 | 1 | held | only D5 red |

The committed `evidence/routed-r24-after-a5.txt` names `e06d4a02`, not the tip. The tip result matches it.

## Q1: does the counting command count SCORECARD/SHONEN self-assessment against observed state?

Only partly. The rule is: "A calibration claim must count mismatches between the lane's self-assessment
(SCORECARD/SHONEN) and observed repo state" (`.ufo/prompts/mori-round-25.md:347-348`; goal file
`.scratch/goal-20261022-hyaku-12h.md:155-156`; AXES.md:15 "SHONEN.md/SCORECARD entries match observed repo state").

| Item | Self-assessment row read? | Observed state compared to | Fits the rule? |
|---|---|---|---|
| D1 | `SCORECARD.md:1514` (base) claims `PASS 12/12` then `MATCHER: rejected 48/48` | the committed evidence file (the predicate hard-codes the two SCORECARD lines, A3) | **Yes, as a boundary case.** SCORECARD was true about the tool. The mismatch is that a SCORECARD claim had no committed evidence behind it (overreach on support) |
| D2 | No. The predicate reads `corpus/knowledge/system-pressure-r24.md` | its own phrases | **No.** See Q2 |
| D3 | No. The predicate reads `corpus/lessons/round-24.md` | case count at `4f05dd5a` | **No.** See Q2 |
| D5 | Yes: the `## Axes` table, which PROTOCOL.md:436 makes the score register | **`SCORECARD.md:1499-1506` at `28b79d3d`**, the lane's own round-24 *declaration* (`:1497` "Targets, not results") | **Partly.** SCORECARD is compared with SCORECARD, not with observed state (F2) |

SHONEN.md is never read; it has four unchecked boxes.

## Findings

### F1: D2 and D3 are not self-assessment mismatches (high, for admission)

- **D3 counterexample.** The SCORECARD row was right. The base `SCORECARD.md:1521` says `PASS 7/7`, which matches
  the 7 cases at `4f05dd5a`. Only the lesson (`round-24.md:79-80`, `S01–S06`, `PASS 6/6`) was wrong. The lane's own
  correction line admits this: "`SCORECARD.md:1521` already said `PASS 7/7`" (`07a31ae:corpus/lessons/round-24.md`,
  last line). A1's D3 row (`contract.md:108`) labels SCORECARD:1521 as the "self-assessment contradicted", but it is
  the witness, not the contradicted row. D3 is lesson-versus-repo drift.
- **D2 counterexample.** The predicate tests the wording of a knowledge entry. The self-assessment A1 names is the
  round-24 report line "six knowledge statements, which were corrected before this report"
  (`.ufo/reports/round-24/mori.md:96`). That line is a filed fleet report, not a SCORECARD or SHONEN row, and the
  predicate never reads it. The round-24 closure also ruled that the entry's statements were "marked
  (corrections-precedence banner) or defensible in context, so it is not 'false and left unmarked'"
  (`round-24-verifier-spotcheck.md:131`). D2 is a corrections-sweep (quality) defect.
- **Precedent.** The round-24 closure accepted a non-SCORECARD lane record (the dispatch ledger) only "as a
  boundary" (`round-24-verifier-spotcheck.md:98`). That is the most generous reading available for D3. Nothing
  supports reading D2 as calibration.
- **Impacted axes:** calibration (fit to the rule), quality trend (D2 belongs there).
- **Smallest fix:** no target change. The measured outcome and the report should classify the items this way: D1
  and D5 are SCORECARD-anchored, D3 is a lesson record (boundary), and D2 is a knowledge-sweep repair. They should
  state the strict count as "SCORECARD-anchored mismatches 2 → 0" next to the tool's 4 → 0.

### F2: D5's "observed state" is a lane declaration labelled closure-admitted (medium, false provenance)

- **What the tool does.** `tools/mori-routed-r24.py:140-147` and `:670-688` parse the pinned scores with
  `\b(axis)\s+(\d+)\b` from `SCORECARD.md:1499-1506` at `28b79d3d`.
- **What those lines are.** They are the round-24 declaration block, which opens at `:1494-1497` and says "Targets,
  not results".
- **What the tip claims.** The correction note at tip `SCORECARD.md:17-19` and A5 (`contract.md:190`) call this "the
  closure-admitted round-24 section".
- **What the closure actually confirms.** Numbers for only two axes: calibration "Score 5 → 5" (`:68`) and coverage
  "Score 6 → 6" (`:88`). For operability, depth, freshness and adjacency it says only "unchanged" (`:100-109`).
- **Consequence.** Of the three rows that differed at the base, operability 7 and depth 5 trace to the lane's own
  writing; only coverage 6 has a closure number behind it.
- **Impacted axes:** calibration (provenance of the comparator).
- **Smallest fix:** append a correction under the SCORECARD note (no rewrite) that says three things:
  - the pin is the lane's round-24 declaration register;
  - the closure confirms calibration 5 and coverage 6 numerically;
  - the other four axes rest on the lane's held values, which the closure marked "unchanged".

### F3: D5's before-red was already disclosed, and D5 holds with the stale pointers restored (medium)

- **Prior disclosure.** At `28b79d3d` the lane had already named this gap twice:
  - `SCORECARD.md:616-619` (round 12): "Correction to the score table at the top of this file (frozen at round 1; 4
    of 6 pointers stale …): the table is left as filed; this section's scores supersede it."
  - `SCORECARD.md:1064-1077` (round 17): "Current axis register (round17 supersedes frozen historical headers)",
    with coverage 6, operability 7, calibration 5, depth 5, freshness 5, adjacency 6, and "The top round1 table …
    are historical, not the active score/selection register."

  So the gap had been named honestly, which is AXES.md:15's own wording. The A5 text, the `e68855d` note and
  `w1/ReviewLessonR24Counts.md` F1 all omit both supersessions. The table was still the PROTOCOL:436 register,
  so the staleness was real, but it was a disclosed mismatch, not a hidden one.
- **Mutation in the private clone.** I restored the round-1 rows with their stale pointers and changed only the
  scores and the Last-change cells:
  - stale pointers restored: "`--selftest` passes 14/14", "per-surface notes are still owed", "no drift pin yet",
    "`progressing-weak` … deferred". These are the same four pointers round 12 called stale.
  - Last change set to `round 25` for coverage, operability and depth, which is false.

  Result: `exit=0 held 4 mism 0`, with D5 held. D5 tests six digits against the lane's own pin. It does not test the
  pointer state that made the table wrong, or PROTOCOL:436's "counting command … and the commit".
- **Impacted axes:** calibration (what "held" proves).
- **Smallest fix:** disclose this limit in the report and cite `:616-619` and `:1064-1077`. No target change.

### F4: A5 rescoped the claim after it was measured (medium; a tradeoff, not forbidden goalpost moving)

Commit times, all on 2026-10-22, -03:00:

| Time | Commit | Event |
|---|---|---|
| 07:44:02 | `e54b644` | A1 tool lands |
| 07:44:17 | `9b1a2f1` | A1 after-value 3 → 0 committed |
| 07:45:40 | `b5b126f` | lesson routes the Axes-table item to round 26 (`round-25.md:97-99`: "a calibration claim could count") |
| 07:54:12 | `efaa157` | A5 amendment |
| 07:54:52 | `e68855d` | D5 fix |
| 08:07:03 | `e06d4a0` | tool gains D5 |
| 08:07:14 | `26c8485` | evidence 4 → 0 |

- **Legitimate in letter:**
  - A5 precedes both the fix and the code it governs.
  - It narrows nothing and drops no failed item.
  - The before-state is a deterministic read of the pinned base.
- **Not a pre-registered measurement:**
  - A5 was added after the A1 target was already met.
  - The item was already known from wave 1, and the lane's own lesson had deferred it.
  - Its fix is a one-commit text edit by the same author.
  - Its comparator is a pin the same author chose (F2).
  - A5 says it was written "after Main's calibration reminder" (`contract.md:182`), so its purpose was to repair
    the claim's fit to the rule, not to measure something new.
- **How a strict closure reads it:** A1 3 → 0 (pre-registered, held) plus D5 1 → 0 (added after the measurement,
  disclosed). It does not read one "4 → 0" measurement.
- **Impacted axes:** calibration.
- **Smallest fix:** the measured outcome reports the two parts separately, with the commit times above.

### F5: the round leaves new self-record mismatches at its own tip that the count cannot see (medium)

- **Lesson line 97 is false at the tip.** `07a31ae:corpus/lessons/round-25.md:97` says "The SCORECARD Axes table at
  its top still shows round-1 scores (coverage 5, operability 6, depth 4)". At the tip it shows 6, 7 and 5 (fixed by
  `e68855d`). This is the same class as D3 (lesson drift), recurring inside the round that repairs D3.
- **Lesson line 4 is incomplete.** It names "amendments A1–A4" and omits A5.
- **The SCORECARD declaration names the wrong counted set.** `07a31ae:SCORECARD.md:1545`, the round-25 declaration,
  still reads "C1 repair round-24 routed defects D1–D4 … expected `mismatches: 4`". The counted set at the tip is
  D1, D2, D3 and D5, with D4 as hygiene. The coincidence of "`held`: 4 of `items`: 4" hides that the item identity
  changed twice (A1, then A5). No SCORECARD line mentions A1, A5 or D5 except the Axes note.
- **Impacted axes:** calibration (the claim adds a SCORECARD row that does not match the contract).
- **Smallest fix:** these are append-only additions; none touches a predicate input except the SCORECARD Axes
  section, and they leave that section unchanged.
  - append a correction to `round-25.md` that supersedes line 97 (fixed at `e68855d`) and names A5;
  - in the round-25 measured outcome, name the counted set D1, D2, D3, D5 and D4 hygiene, with the A1 and A5
    history.

### F6: the schema id stayed the same when the item set changed (low)

`schema: mori-routed-r24-v1` labels both the 3-item output (`e54b644` tool, `routed-r24-after.txt`) and the 4-item
output (`e06d4a0`+ tool). Only `items` and the row ids tell them apart. Fix: disclose it. Bumping the schema now
would change the tool after its evidence was recorded.

## Q4: sentinel ("same axis+surface claim or same routed defect class in a lane 3 rounds running")

Rule: goal file `:173`, whose action is "The lane's next round must work a different frontier area."

**Tripped under the class reading.** Calibration's counted claim has been a repair of the previous closure's routed
defects three rounds running:

| Round | SCORECARD row (base) | Claim |
|---|---|---|
| 23 | `SCORECARD.md:1422` | "C1 remove misleading `raw_unallowlisted` (routed by r22 closure)" |
| 24 | `:1501` | "C1 repair the four byte-checkable round-23 routed items" |
| 25 | tip `:1545` | "C1 repair round-24 routed defects" |

- The contract defines the defect class itself: "a lane-written statement or record disagrees with the committed
  bytes" (`contract.md:13`).
- Round 24's R4 (lane-written ledger `at` versus commit time) and round 25's D1–D3 all fall in that class.
- A5 does not leave the pattern; D5 is one more repair of a lane-written record.
- The lane's own lesson concedes the reading (`round-25.md:94-96`).

**Not tripped under a strict same-files reading.** Only rounds 24 and 25 share a tool surface: `mori-routed-check.py`,
then `mori-routed-r24.py`. A strict closure should rule it tripped, because the contract supplies the class
definition.

**Consequence.** Round 26's counted calibration claim must not be a routed repair. Routed defects become uncounted
fixes, and the counted claim targets a different frontier area. Round 25 is not rejected on this ground.

## Smallest safe correction set (no target narrowed)

1. **Measured outcome and report.**
   - State the item classes from F1: D1 and D5 are SCORECARD-anchored, D3 is a lesson record (boundary), D2 is a
     knowledge-sweep repair.
   - Report "A1 3 → 0 pre-registered; D5 1 → 0 added by A5 after the measurement".
   - Name the counted set D1, D2, D3, D5 and D4 hygiene.
2. **Appended SCORECARD correction.**
   - Make the D5 pin's provenance accurate: the pin is the round-24 declaration, and the closure confirms only
     calibration 5 and coverage 6 numerically.
   - Cite the round-12 and round-17 supersessions (`:616-619`, `:1064-1077`).
   - Disclose that D5 checks scores only.
3. **Appended `round-25.md` correction.** Supersede line 97 and name A5.
4. **Report.** State that the sentinel tripped under the class reading and bind round 26 to a non-repair calibration
   target.

Checks Main should run after integrating: re-run the C1 command at the final landed tip, then
`git show <tip>:corpus/lessons/round-25.md | grep -n 'still shows'` (expect only lines inside a correction) and
`git show <tip>:SCORECARD.md | grep -n 'D1–D4'` (expect the declaration plus an appended measured-outcome row that
names D5).
