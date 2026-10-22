author: MoriR29.CriticC1Admission (critic, wave 2, leaf seat)

# Round 29 wave 2 — attack on C1's admission (calibration, standing Axes table)

Inputs, all read-only: `.ufo/waves/round-29/contract.md` (C1, A1, A2) at the lane working tree; `git diff 7118f320
8809a3fe -- SCORECARD.md`; `evidence/c1-before.txt`, `evidence/c1-after.txt`; `count-c1.sh`; wave-1 `Axis*.md`,
`CriticC1Design.md`, `CriticScorePolicy.md`; lane files at `8809a3fe`; fleet `MANIFEST.json` at `63729047`;
fleet `AXES.md`. No tool installed or upgraded. No URL fetched. No oom-killers run. One sandbox clone at
`/fast/scratch/hyaku/mori-r29/w2/CriticC1Admission/clone` (sandbox commit only; lane untouched). Written
2026-10-22T20:35Z.

## Bottom line

- `mismatches=0` at the wave tip is real and the six rows are true against the closure record on every claim
  that I checked. No score moved. Every backticked pointer resolves, and the cited line says what the row says
  (table below). The one claim the counter cannot see, the evidence prose, is mostly true. It has one wording
  error (F6) and one dropped gap that is still true (F4).
- The counter is weaker than `mismatches=0` suggests. A sandbox mutant with three false `Last change` cells still
  prints `mismatches=0` (F1). The present cells are true, so this is a defect to route, not a reason to reject.
- Calibration score: **hold 5** (propose `5 → 5`, "improved, score held"). Do not propose 6.
- Verdict proposal for C1: **improved** (bounded). Restore the drift-pin clause (F4) and fix the lesson count
  (F2) before landing. That keeps "harm none".

## Reproduction of the counted value

```
$ bash .ufo/waves/round-29/count-c1.sh 8809a3fe1eaa87a0afa177a15263d174378e7462 63729047644f839fe4c8cc97abd0d8bf741a5787
axis=coverage score=6 basis=held R=26 kinds=none   ... (all six rows kinds=none)
mismatches=0
C1=met
exit: 0
```

The counter's sha256 in the working tree equals its committed blob at `8809a3fe`:
`a26604ee…d4e791`, the same hash recorded in `evidence/c1-before.txt:1`. MANIFEST mori rounds 12–28 (my
`python3` dump of `.rounds[]`, `lane=="mori"`): every R the counter reports matches `max{N admitted, verdicts.a
== improved}`. The values are coverage 26, operability 28, depth 12, freshness 28, calibration 25, adjacency 19
(rounds[476], [462], [455], [398], [313]).

## Per-row claim check at 8809a3fe (each claim against its pointer)

| Row | Claim | Pointer content (verbatim, ≤25 words) | Holds? |
|---|---|---|---|
| coverage | round-24 closure "Score 6 → 6" | `round-24-verifier-spotcheck.md:88` "Ruling: improved, bounded. … Score 6 → 6." | yes |
| coverage | latest admitted closure grades coverage improved | `round-26-verifier-spotcheck.md:133` "\| coverage \| improved \| C2 capability evidence-verified…" | yes; MANIFEST r26 coverage improved |
| coverage | "(round 12, score 5 → 6 then)" | `SCORECARD.md:615` "\| coverage \| **improved** \| 5 → 6 \|" (lane table; closure ratified 6 at `round-14-verifier-spotcheck.md:87`) | yes, as lane history |
| operability | census selftest PASS 134 cases, round 24 | `SCORECARD.md:1526` "selftest `PASS (134 cases, 134 passed," | yes (token `SCORECARD.md` has no line) |
| operability | "7 first held in round 13's table" | `SCORECARD.md:696` "\| operability \| improved \| **6 → 7** \|" | **wording false**: raised, not held (F6) |
| operability | round 14 closure grades operability unchanged | `round-14-verifier-spotcheck.md:92`; MANIFEST rounds[339] operability unchanged | yes (no pointer in row) |
| operability | latest closure improved, ten A2 rules / 30 cases | `round-28-verifier-spotcheck.md:93` "C2 verified: ten A2 rules pinned by 30 frozen cases, PASS 30/30" | yes |
| depth | round-12 closure states the move | `round-12-verifier-spotcheck.md:17` "Depth improved (… score 4→5)" | yes |
| depth | round 27 depth improved under rejected-honest-stop | `round-27-verifier-spotcheck.md:102` "\| depth \| improved \|"; MANIFEST rounds[468] `rejected-honest-stop` | yes |
| freshness | round-20 re-pin rejected | `corpus/README.md:406-411` "CloseMori20 rejected the pin" | yes |
| freshness | latest closure improved, no new number | `round-28-verifier-spotcheck.md:92`; `:78-79` "no held score changed" | yes |
| freshness | round 28 measured outcome proposed 5 → 6 | `SCORECARD.md:1771` "freshness 5 → 6 proposed" | yes |
| calibration | round 12 self-assessed 5 → 6, held at 5 | `round-12-verifier-spotcheck.md:17` "score held 5 because the outside reviewer could not derive 6" | yes |
| calibration | round-24 closure "Score 5 → 5" | `round-24-verifier-spotcheck.md:68` "… Score 5 → 5." | yes |
| calibration | latest closure improved | `round-25-verifier-spotcheck.md:124` "\| calibration \| improved \| C1 4 → 0 re-measured; three wrong Axes scores corrected" | yes |
| adjacency | refuses kumitate / tsukuroi / operator in PROVINCE | `PROVINCE.md:12-13` "**Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package, systemd unit…" | yes |
| adjacency | MANIFEST mori round 19 rounds[398] adjacency improved | dump: `398 19 admitted True … "adjacency": "improved"` | yes |

The six Last change cells name R(a), and MANIFEST records each of those rounds as admitted with `verdicts.a ==
improved`. The depth cell `round 12 (4 → 5)` passes A2 kind 2b: rounds[313] has depth improved.

## Ranked findings

### F1 (high; counter defect, fixable; does not falsify the current table)

- **Counterexample.** Mutant M1 changes three Last change cells: coverage, depth and calibration now read `round
  28 (improved, score held)`. MANIFEST rounds[476] grades all three `unchanged`. M1 is sandbox commit `fcc23352`
  on top of `8809a3fe`. The counter, run with `MORI_C1_LANE_REPO=<clone>`, prints `kinds=none` on all six rows,
  `mismatches=0`, `C1=met`, exit 0.
- **Cause.** Kind 2 (`count-c1.sh:166-176`) requires only three things: N admitted, N ≥ R, and the literal
  `(improved, score held)`. Kind 2b (`:174`) checks the verdict only when an arrow `(X → Y)` is present. A held
  cell can therefore claim an improvement that the named round never graded.
- **Axes hit.** Calibration. A passing count can certify a false Last change cell.
- **Smallest safe correction.** When R(a) exists and the cell has no arrow, require N == R(a). Equivalently,
  require MANIFEST `verdicts.a == "improved"` for round N whenever the cell reads `(improved, …)`. This is 0 at
  `8809a3fe`, because every cell names R. Changing the counter after data has landed would be post-hoc, so route
  it as a named residual or as a next-round tightening, and attach a receipt showing that the stricter rule still
  gives 0 at the tip.

### F2 (medium; false statement in the lesson about C1's before value)

- `corpus/lessons/round-29.md:9-11` says "five of six rows did not cite the latest admitted `improved` closure and
  five Last change cells predated it (`mismatches=11`)". In fact `evidence/c1-before.txt` shows kind 1 on all
  **six** rows (depth `kinds=1`, the other five `kinds=1,2`). Six plus five is the 11. As written, the lesson's
  numbers add to 10.
- Correction: "all six rows lacked a citation of the latest admitted improved closure (depth: round 12) and five
  Last change cells predated it".

### F3 (medium; A1 obligation unmet in the draft lesson)

- A1 requires the following: "Uncounted residual named in the lesson: the truth of each row's evidence prose
  beyond its pointers" (`contract.md:129-130`).
- `git show 8809a3fe:corpus/lessons/round-29.md | rg -i 'residual|uncounted|prose'` returns no match.
- Correction: name the residual and cite this report and ReviewAxisRowsProse as the wave-2 non-author read.

### F4 (medium; a true, named gap was deleted from the freshness row)

- At `7118f320` the row opened "round-10 drift pin still red". At `8809a3fe` that clause is gone.
- The gap is still true at `8809a3fe`. `corpus/README.md:367` says "R10 drift pin remains red debt without a
  re-pin". `corpus/README.md:428` says "the invalid r20 baseline is not accepted or re-pinned". No later re-pin
  is in the history (`git log 8809a3fe -- corpus/knowledge/drift-*` ends at round 21).
- Neither AxisFreshness nor CriticScorePolicy asked for the clause to be removed.
- Calibration's own signal is "gaps named honestly" (`AXES.md:15`). Removing a live gap from the standing row is
  a small calibration loss that the counter cannot see.
- Smallest correction: restore the clause, citing `corpus/README.md:367`.

### F5 (low-medium; three scores carry no pointer to a closure that states their number)

- Each score is defensible: CriticScorePolicy's table agrees, and I re-read the lines. But only coverage
  (`round-24:88`), depth (`round-12:17`) and calibration (`round-24:68`) cite a closure line that states the
  number.
- Operability 7, freshness 5 and adjacency 6 cite none. One exists: `round-14-verifier-spotcheck.md:87` "holds
  coverage6/operability7/depth5/freshness5/calibration5/adjacency6". Freshness also has `round-26:126` "freshness
  5 → 5".
- `AXES.md:52-55`: "a score no reader can re-derive is an opinion".
- Correction: add `corpus/lessons/round-14-verifier-spotcheck.md:87` to those three rows. Kind 3 passes, because
  the file is longer than 87 lines.

### F6 (low; prose wording)

- The operability row says "7 first held in round 13's table". Round 13's table raises the score (`SCORECARD.md:696`
  "**6 → 7**"). The first "7 held" is round 14 (`SCORECARD.md:793`).
- Correction: "7 first claimed in round 13's table (6 → 7)".

### F7 (tradeoff, declared scope; this bounds the score, not C1=met)

C1 counts six rows (`contract.md:13-14`). The axis signal is "SHONEN.md/SCORECARD entries match observed repo
state" (`AXES.md:15`). At `8809a3fe` several entries outside the table do not match the repo:

- `## Move log` has only the round-1 row (`SCORECARD.md:21-25`).
- `## Planned` still reads "Round 2: land one note per surface family…" (`:27-30`).
- `## Capabilities` reads "— none yet —" (`:586-590`), but `## Capabilities (round 12 demonstrations)` follows at
  `:627`.
- `## Saturation` says the line is "to be declared" (`:594-596`), but it was declared at `:637-640`.
- `SHONEN.md` (8 lines, last touched in `1f07f1d`, round 12) has every promotion box unchecked. [INFERENCE] At
  least "end-to-end domain task … logged in LOG.md" may now be met. That is a judgment call, not a byte mismatch.

## Calibration score: 5 → 6, or held?

**Hold 5.** The reasons, strongest first:

1. **Contract.** A1 kind 4: a numeric change needs an admitted closure line stating `X → Y`, and "a number a
   declaration proposed is never a basis" (`contract.md:120-124`). No closure states calibration 5 → 6, and round
   29 is not closed, so the lane cannot move the cell. The only question is what the measured outcome proposes.
2. **Precedent.** MANIFEST grades calibration `improved` in seven admitted rounds: 12, 18, 19, 21, 22, 24 and 25.
   The score stayed 5 every time (`round-12:17`, `round-24:68`, `SCORECARD.md:1386`, `:1555`). Round 25's C1 did
   the same kind of work and more: it corrected "three wrong Axes scores" (`round-25-verifier-spotcheck.md:124`).
   It was still held at 5. Round 29 re-cites rows and moves no score. Proposing 6 for a weaker instance of a move
   the closure held at 5 would be an overclaim on the claim's own axis.
3. **Axis signal.** The signal covers SHONEN.md and SCORECARD entries in general. F7 lists five such entries that
   still disagree with the repo, and F1 shows the counter accepts false cells. A reader cannot derive 6 from
   "six rows match the closure record".
4. **Consistency.** The round-29 declaration in the uncommitted working tree lists "calibration 5" and proposes no
   6 (`git diff -- SCORECARD.md`). Keep it that way. In the measured outcome, write "improved, bounded; calibration
   5 → 5 pending closure".

## Verdict proposal for C1

**Improved** (bounded):

- The counted value moved from 11 to 0 on committed bytes, and I reproduced it at the wave tip.
- Every row claim I checked is true against MANIFEST and its pointer.
- The real defects at `7118f320` are fixed: operability's `round 14 (6 → 7)` contradicted round 14's
  `unchanged`, and adjacency cited no closure while round 19 was admitted improved.
- No score moved.

It is not harmed, provided F4 is restored. If F4 lands as is, a closure can fairly read the row as having dropped a
named gap. That would be the only harm I found, and it is small.

It is not "unchanged": the before value, the after value and the content of the rows all differ, and the change is
true.

## Checks for the L1

- `bash .ufo/waves/round-29/count-c1.sh <landed tip> 63729047644f839fe4c8cc97abd0d8bf741a5787` (expect 0 after the
  F4/F5/F6 prose edits; the added pointers are kind-3 safe).
- `git show 8809a3fe:corpus/README.md | sed -n '367p;428p'` (F4).
- `git show 8809a3fe:corpus/lessons/round-14-verifier-spotcheck.md | sed -n '87p'` (F5).
- `sed -n '2,8p' .ufo/waves/round-29/evidence/c1-before.txt` (F2: depth `kinds=1`).
- M1 reproduction: in a sandbox clone at `8809a3fe`, replace the coverage, depth and calibration Last change cells
  with `round 28 (improved, score held)`, commit, then run the counter with `MORI_C1_LANE_REPO=<clone>` (F1).
