# Mo50bCritAxesSemantics — C1's premise: what does the Axes table's "Last change" column mean?

Seat: critic, round 50 attempt 2, wave a2w1. Assignment: attack C1's premise, not its code — is
"latest admitted round grading the axis improved or harmed" the right meaning of the Axes table's
Last change column? Argue both sides, derive N\* per axis under a "last score change" convention from
the spot-check files, conclude whether C1 measures a real calibration property, and state the limit.

Revisions read (all read-only): lane `487941b9395e89678af0053cc443cdb49cdee6e3` (landed data, R),
entering `7197160b927f04db294c9553fb48fadcc7a3f4e3`, fleet `e014499613f63f8a467821219b0296121119ca53`
(MANIFEST, manifest tag `a94551c5bc8d`), plus `63729047` for the adjacency cell's own pointer.
Frozen files were run, never edited: `count-c1.py` at R (sha256 compared by the counter itself via its
manifest tag) and five instrument runs; every run had `TMPDIR=/fast/scratch/hyaku/mori-r50/Mo50bCritAxesSemantics/tmp`
and `--scratch` under that directory. No pacman, no repo writes outside this report, no subagents.
Scratch removed at the end (receipts below were copied out first).

---

## 1. The premise is three clauses, and only one of them is contested

The contract's P-C1(a) makes three independent demands of each row's Last change cell:

1. the cell's first `round N` equals N\* = "the highest mori lane round <= 49 that the fleet MANIFEST.json
   records with verdict `admitted` and that axis graded `improved` or `harmed`";
2. the segment from that `round N` to the next `;` names N\*'s verdict word;
3. the Evidence cell names `corpus/lessons/round-N*-verifier-spotcheck.md` when it exists, else `MANIFEST.json`.

Clause 1 is the premise under test. Clauses 2 and 3 are provenance formatting. The semantic question is
only: **does "Last change" date the axis's last *verdict* move or the last *score* move?** A third reading
("last time this cell's text changed") is not viable — after this round's correction it would date every
corrected row to round 50, which no row states — so exactly two readings are live.

- **M1 (score move):** the round in which the Score cell's number last changed.
- **M2 (verdict move):** the latest admitted round whose closure graded the axis improved or harmed.
  This is what the counter implements (`manifest_targets`, `count-c1.py:67-81`; expectations printed by
  the run in §5 receipt R1: `coverage 47, operability 47, depth 49, freshness 28, calibration 49,
  adjacency 19`).

---

## 2. Side A — for M2: it is the table's own convention, inherited, and the only one the record supports

**A1. The column carried M2 phrasing before this round.** At the entering tip every one of the six cells
already read `(improved, score held)`:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7197160b...:SCORECARD.md | sed -n '10,15p'  (rc 0)
coverage    => round 26 (improved, score held)
operability => round 31 (improved, score held); round-37 C2 re-attributed here (score held, 7)
depth       => round 31 (improved, score held)
freshness   => round 28 (improved, score held); ...
calibration => round 25 (improved, score held); ...
adjacency   => round 19 (improved, score held)
```

C1 did not introduce the convention; it moved the lead round forward inside it. A critic who called the
convention an L1 invention would be wrong on the bytes.

**A2. AXES.md makes a row's substantive change either a number or a verdict.** The SCORECARD contract
row reads: "Axis name → score 0–10 + evidence pointer (measurable moves) **or** `unprovable-but-better`
verdict + named non-author reviewer (exploratory moves) → last-change round"
(`/home/vgpnk/Projects/shokunin/AXES.md:79`). And: "The score on a subjectively-moved axis need not
change: the `SCORECARD.md` row then carries the verdict and the reviewer pointer instead of a number"
(`AXES.md:51-53`). If "last-change" meant "last score change", the contract's own alternative — a row that
carries a verdict instead of a number — would have no dateable change at all.

**A3. M2 is the only reading that keeps clause 1 satisfiable for all six axes; M1 is undefined for half.**
Derivation in §3.

**A4. The verdict-vs-score split is the dominant case in the record, not an edge.** Twelve axis verdicts in
seven admitted closures grade an axis improved while the same closure states the score did not move:

| round | closure line saying "improved" | closure line saying the score held |
|---|---|---|
| 24 | `round-24-verifier-spotcheck.md:104` calibration | `:68` "Score 5 → 5." |
| 25 | `round-25-verifier-spotcheck.md:124` calibration | SCORECARD.md:14 "states no new number" |
| 26 | `round-26-verifier-spotcheck.md:132` freshness, `:133` coverage | `:126` "no score changes; … freshness 5 → 5 and coverage 6 → 6" |
| 31 | `round-31-verifier-spotcheck.md:154` depth, `:155` operability | "score stays 5" / "the score stays 7" (same lines) |
| 47 | `round-47-verifier-spotcheck.md:67` operability, `:68` coverage | `:61` "no score change is claimed" |
| 48 | `round-48-verifier-spotcheck.md:67` calibration, `:68` depth | `:61` "no axis-table cell changed and no score change is claimed" |
| 49 | `round-49-verifier-spotcheck.md:75` calibration, `:76` depth | `:75` "no score change claimed" |

Five of the six N\* values C1 demands (`47, 47, 49, 28, 49`) come from exactly this class. The sixth
(adjacency 19) has no lane spot-check file at all and is MANIFEST-only, which is why clause 3 lets that cell
cite `MANIFEST.json`.

**A5. No admitted closure after an axis's N\* grades it improved.** Checked exhaustively for the two axes
whose N\* is old (all `round-*-verifier-spotcheck.md`, `grep -E "^\| ?(freshness|adjacency)[^|]*\|"`,
lines not saying unchanged/held):

```
round-13:100 adjacency harmed | round-14:96 adjacency improved | round-17:239 adjacency harmed |
round-18:124 adjacency improved | round-26:132 freshness improved | round-28:92 freshness improved |
round-32:132 freshness unprovable-but-better
```

Rounds 46-49 grade freshness and adjacency `unchanged` (r46:49-50, r48:71-72, r49:79-80), and rounds
46-49 grade coverage/operability `unchanged` except the round-47 improvements already at N\*. So the landed
data is not stale under M2. The strongest candidate for a missed improvement — round 36's admitted
`freshness-technique` — is defused by its own closure: the reviewer rules `unprovable-but-better` for a
"byte-behavior predicate, **never asserted as a freshness verdict**"
(`round-36-verifier-spotcheck.md:27-31`), and MANIFEST records it under the key `freshness-technique`,
not `freshness`.

---

## 3. Side B — what M1 would say, derived from the spot-check files and the score sections

Scores are `coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6` and identical at
the entering tip and at R (`git show <rev>:SCORECARD.md | sed -n '9,15p'`, both rc 0; the SCORECARD diff
touches only cells 3 and 4 of four rows). Last *score* change per axis:

| axis | M2 N\* (counter) | M1 last score change | derivation |
|---|---|---|---|
| coverage | 47 | **12** (5 → 6) | `round-12-verifier-spotcheck.md:17` "coverage improved (silence grading 9→23 lanes…)"; SCORECARD.md:10 "round 12, score 5 → 6 then"; `round-14-verifier-spotcheck.md:87` holds "coverage6" |
| operability | 47 | **13 or 14** (6 → 7) | SCORECARD.md:11 "7 was first set in round 13's table (6 → 7), which closed rejected-harmed; first held in round 14's admitted table" — the reading forks on whether a rejected table's number counts |
| depth | 49 | **12** (4 → 5) | `round-12-verifier-spotcheck.md:17` "score 4→5" |
| freshness | 28 | **none** | 5 throughout: r12:17 "Operability/freshness/adjacency unchanged"; r14:87 "freshness5"; round 28's `5 → 6` was proposed and not adopted (SCORECARD.md:13) |
| calibration | 49 | **none** | r12:17 "calibration improved … score held 5 because the outside reviewer could not derive 6"; r24:68 "Score 5 → 5" |
| adjacency | 19 (MANIFEST rounds[398]@63729047; r18:124 is the latest lane file) | **none** | 6 throughout: r12:17, r14:87 "adjacency6" |

Consequences of adopting M1:

- Three of six axes have **no derivable value**. A cell would have to invent a round for a score that never
  moved — exactly what AXES.md forbids ("a score no reader can re-derive is an opinion", `AXES.md:64-67`).
- The other three would read 12-14, i.e. 35-37 rounds behind the fleet's verdict record, and the coverage
  row would assert that coverage had not moved since round 12 while the fleet admitted improvements in
  14, 15, 16, 24, 25, 26 and 47.
- The prompt's own defect class (cells lagging four admitted closures) would be *unmeasurable*: under M1
  there is nothing to lag, because nothing moved.

M1 therefore does not merely score worse — it is not implementable on this lane's record. That is the
decisive argument for M2.

---

## 4. What M1 is right about — the honest case against the landed cells

None of the above makes the column well-labelled. Three points stand against the landed data:

**B1. The header says "Last change", unqualified, next to a numeric Score column.** A reader parses
`| coverage | 6 | … | round 47 (improved, score held) |` as "score 6, last changed round 47". Coverage's 6
dates to round 12: the lead round is off by 35 rounds under that parse. The only disambiguating text sits
in the prose correction paragraph (SCORECARD.md:21-26, "scores are unchanged because no closure states a
new number"), not in the column or its cells' shape.

**B2. The lead round is a verdict move, not a table change.** The round-47 closure says in as many words
that the row did not change: "the Axes table is unchanged and no score change is claimed"
(`round-47-verifier-spotcheck.md:61`), yet round 47 is now the lead for coverage and operability. So under
the literal phrase "last change *of this row*", the cells are false; they are true only as "last change of
the axis's fleet grade". (The cited lines do grade both axes improved — `:67`, `:68` — so this is a label
problem, not false provenance.)

**B3. Nothing ties the parenthetical to the closure.** Clause 2 only requires the word `improved` (or
`harmed`) somewhere before the first `;`. A cell writing "improved narrowly" would match; a cell asserting
"score held" where the closure actually moved the score would also match. The counter never compares the
qualifier to the closure, and it never reads the Score cell at all (§5 receipt R4).

Net: M2 is the right meaning, and the cells are correct under it, but the table does not say so at the point
where a reader needs it.

---

## 5. Receipts (frozen instruments, scratch fixtures)

R1 — the landed data, at R, with the frozen counter unchanged:

```
$ python3 count-c1.py 487941b9... --repo .../mori-shokunin --fleet-repo /home/vgpnk/Projects/shokunin --scratch <S>/c1base
item axis coverage expect=round_47_improved got=ok state=ok
item axis operability expect=round_47_improved got=ok state=ok
item axis depth expect=round_49_improved got=ok state=ok
item axis freshness expect=round_28_improved got=ok state=ok
item axis calibration expect=round_49_improved got=ok state=ok
item axis adjacency expect=round_19_improved got=ok state=ok
item pin python3_tools/mori-pin-check.py_--selftest expect=(114/114) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=ok
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0 state=ok
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9...
exit=0
```

R2 — the same table rewritten under M1 (fixture `fixture-m1`, `git archive` of R + `git init` in scratch,
`rev-parse --show-toplevel` verified equal to the fixture, six Last change cells rewritten to their M1
rounds 12/14/12/12/12/14, everything else byte-identical):

```
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=1f2021f8...
failed=mismatch
exit=1
```

`mismatches=6` is digit-for-digit the entering do-nothing control
(`evidence/control-c1-do-nothing.txt`: `mismatches=6`). **The convention is load-bearing: the target is
reachable only under M2, and an M1-convention table is indistinguishable from doing nothing.** No frozen
control separates "correct M2 dates" from "correct M1 dates" — the `all-latest` control tests a third
thing (a blanket round-49 stamp).

R3 — provenance arm is existence-only (fixture `fixture-prov`, R bytes with
`corpus/lessons/round-28-verifier-spotcheck.md` replaced by the single line `stub: this file grades nothing.`):

```
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=2928eff2...
exit=0
```

`check_axes` computes `need = spot if exists(spot) else "MANIFEST.json"` and tests `need not in evidence`
(`count-c1.py:150-156`): the closure file is confirmed to exist, never opened. No landed row exploits this
— I re-opened every cited closure line and each does grade its axis (r47:67 operability, r47:68 coverage,
r49:75 calibration, r49:76 depth, r28:92 freshness, r25:124, r31:154/155, r26:133, r24:104) — but the arm
does not discriminate.

R4 — the Score column is unmeasured (same fixture, `coverage` 6 → 1 and `adjacency` 6 → 0):

```
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=dea8b5b0...
exit=0
```

So the round-50 correction's sentence "scores are unchanged because no closure states a new number"
(SCORECARD.md:24-25) is true, but true by diff, not by instrument: both revisions carry
`6 / 7 / 5 / 5 / 5 / 6`, and C1 would accept any other numbers.

R5 — the obvious "fix" breaks C1. Renaming the header cell to `Last verdict change` (fixture `fixture-hdr`):

```
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=d87f518a...
failed=mismatch
exit=1
```

`axes_table` requires the header cells to equal `["axis","score","evidence pointer","last change"]`
(`count-c1.py:109-115`); with the header renamed the table is not found and every axis reports
`no_axes_table`. **A header rename is not a safe correction.** The fixture's `.ready` marker and commit are
the fixture's alone; the fleet repo received nothing.

R6 — the prose correction I propose is safe (fixture `fixture-fix`, R bytes + one sentence pair appended to
the round-50 correction paragraph, no cell touched):

```
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=6f62b2c6...
exit=0
```

R7 — the adjacency cell's own pointer is accurate: `63729047` exists, is an ancestor of `e0144996`
(`git merge-base --is-ancestor`, rc 0), and its MANIFEST `rounds[398]` is
`{"lane":"mori","lane_round":19,"verdict":"admitted","verdicts":{"adjacency":"improved",…}}` — exactly what
SCORECARD.md:15 states. But the phrase alone does not fix N\*: the lane's own closure series stops at
round 18 for adjacency (`round-18-verifier-spotcheck.md:124`), so "latest admitted round grading the axis
improved" reads 18 under a lane-closures oracle and 19 under the contract's pinned fleet oracle.

---

## 6. Conclusion — does C1 measure a real calibration property?

**Yes, but a narrower one than the axis name suggests, and the report must say which.**

Under M2 the Axes half measures a real, falsifiable property: the lead round of each row equals the fleet
record's latest admitted improved/harmed round, the verdict word is present, and the evidence cell points at
that round's closure. It is non-vacuous — the do-nothing table fails with 6 mismatches, the deletion
and receipt controls fail (pins deleted, pin corrected without a receipt, axes-only, shonen-only, box
dropped), and the `all-latest` control fails four axes, which is the control that proves the check is not
"any late round passes". It is inherited from the entering table rather than invented, and it is the only
convention the lane's record can express. AXES.md's definition of calibration — "SHONEN.md/SCORECARD
entries match observed repo state" (`AXES.md:13`) — is satisfied in the strict sense that the fleet MANIFEST
is observed state.

What it does **not** measure:

1. **Score provenance.** A row may hold a wrong score (R4: 1 and 0) and pass. The Score column is the one
   the word "change" most naturally attaches to, and it is the one C1 never reads.
2. **The cited closure's content.** Existence is enough (R3). A row can cite a file that grades nothing.
3. **Completeness or correctness of the oracle.** `manifest_targets` reads exact axis keys
   (`count-c1.py:76-80`); MANIFEST round 36 carries `freshness-technique` (not an axis) and round 39 omits
   coverage/freshness/adjacency entirely. No live instance is affected (round 36's freshness claim is
   explicitly "never asserted as a freshness verdict"; r36:31), but an admitted improvement recorded under a
   variant key or omitted would make the counter demand a stale round — and the lane would be obliged to
   write it.
4. **Independent re-derivation.** The same artifact the correction transcribes (MANIFEST@e0144996) is the
   counter's oracle. That is legitimate for an "agreement" axis, but it means the half proves correct
   transcription of an upstream grade record, not that the lane re-read its own closures. Round 47/48/49
   each state the table was untouched, so the lead rounds are the fleet's judgment, not the lane's finding.

Verdict for this seat: **C1's premise is sound under the table's own convention; the claim verifies at R
(R1, rc 0); the convention is load-bearing and must be named in the report as a named limit, not left to the
reader.** No data correction is required for the premise itself; R6 is offered as a labelling correction the
L1 may integrate.

---

## 7. The limit the report must state (draft wording, ready to copy)

```text
LIMIT (Axes convention, MED): C1's Last-change rule dates the axis's last *verdict* move (the latest
admitted round whose closure graded the axis improved or harmed), which is the convention the entering
table already used ("round 26 (improved, score held)") and the only one this record can express: under a
"last score change" reading the six cells would read 12/13-14/12/none/none/none, because freshness,
calibration and adjacency have no admitted score change at all and five of the six N* rounds explicitly
state the score was held. The counter does not test the reading: a table rewritten to the score-move
rounds prints mismatches=6, the same number as the do-nothing control, so the target is reachable only
under the stated convention. C1 therefore certifies agreement with the fleet verdict record, not the dating
of the Score column - the Score cells are outside the counter (a row with coverage 1 and adjacency 0 still
prints C1=met), so "scores are unchanged" is a diff fact, not an instrumented one. The evidence arm is
existence-only: the cited spot-check file is confirmed present, never read, so a file that grades nothing
passes. And the manifest it trusts is the same artifact the correction transcribed, with per-round axis
keys incomplete (round 36 stores `freshness-technique`, round 39 omits three axes) and one N* value
(adjacency 19) available only from the fleet record, not from any lane closure.
```

---

## 8. Smallest safe correction (verified against the frozen counter, R6)

Scope: SCORECARD.md prose only. No cell, header, score, SHONEN pin, tool or counter change. Append to the
existing round-50 correction paragraph (SCORECARD.md:21-26), after "scores are unchanged because no closure
states a new number.":

```text
The column dates the last verdict move, not the last
score change: coverage's 6 dates to round 12 (5 → 6), operability's 7 to rounds 13/14 (6 → 7), depth's 5 to
round 12 (4 → 5), and freshness, calibration and adjacency have no admitted score change (freshness 5 and
calibration 5 since round 12; adjacency 6 since round 12). Score provenance stays in each row's Evidence cell.
```

Verified: with exactly this insertion the frozen counter still prints `C1=met … mismatches=0` (R6, rc 0).
Do **not** rename the header (R5, `mismatches=6`), do not add a fifth column, and do not touch the cells
themselves — all three change the frozen instrument's inputs.

---

## 9. Named limits added by this seat (for the C1 ledger)

1. The convention that N\* is a verdict move is load-bearing and has no control: an M1 table prints the
   do-nothing number (R2). Frozen counter — recorded as a limit, not a fix.
2. The Score column is outside every clause of P-C1 (R4).
3. The evidence arm is existence-only (R3).
4. `improved|harmed` is a word test on the first `;`-segment (B3): "improved narrowly" or a false "score
   held" both pass.
5. The `harmed` arm has never fired on an admitted round: MANIFEST@e0144996 records harmed only in
   rejected rounds (13, 17, 20, 45), consistent with AXES.md:34 ("A round is admitted only if … no axis is
   harmed"). It is exercised by the counter's own selftest manifest, not by the record.
6. Oracle incompleteness (round 36 variant key, round 39 missing axes) and oracle choice (adjacency 18 vs
   19) both change N\* without any byte of the lane changing (R7).

## Findings

| # | severity | finding | file / line |
|---|---|---|---|
| F1 | MED | The premise is correct under M2 and the landed cells verify (R1, rc 0); the alternative M1 reading is unimplementable (three axes have no admitted score change) and rewrites the same table to `mismatches=6`, the do-nothing number. The convention is load-bearing, inherited from the entering table, and un-controlled — the report must name it (draft in §7). | `.ufo/waves/round-50/count-c1.py:67-81`; `SCORECARD.md:10-15`; `AXES.md:51-53,79` |
| F2 | MED | The Axes table's header says "Last change" while the cells date the last *verdict* move; the lead round for coverage/operability (47) is a round whose closure states the row was not changed and no score moved. True under M2, false under a reader's natural parse, and the only disambiguation is prose outside the table. | `SCORECARD.md:8`, `:10-11`, `:21-26`; `corpus/lessons/round-47-verifier-spotcheck.md:61` |
| F3 | MED | The Score column is unmeasured: with coverage 6 → 1 and adjacency 6 → 0 the counter still prints `C1=met`. So "scores are unchanged" (correct by diff: 6/7/5/5/5/6 at both revs) is not an instrumented claim. | `.ufo/waves/round-50/count-c1.py:97-157` (no score cell read); `SCORECARD.md:24-25` |
| F4 | LOW | The evidence arm is existence-only: a cited spot-check file replaced by "stub: this file grades nothing." still yields `C1=met`. No landed row exploits it — every cited line was re-opened and does grade its axis. | `.ufo/waves/round-50/count-c1.py:150-156` |
| F5 | LOW | The `harmed` half of the rule has never fired on an admitted round (zero admitted `harmed` verdicts at e0144996; harmed appears only in rejected rounds 13, 17, 20, 45); it is code-selftested only, consistent with AXES.md's admission condition. | `MANIFEST.json@e0144996` mori entries; `AXES.md:34` |
| F6 | LOW | The oracle is structurally incomplete for this use: MANIFEST round 36 stores `freshness-technique` (not an axis key) and round 39 omits coverage/freshness/adjacency; `manifest_targets` keys exactly, so an admitted improvement under a variant or missing key would make C1 demand a stale round. No live instance (r36's freshness claim is "never asserted as a freshness verdict"). | `.ufo/waves/round-50/count-c1.py:76-80`; `corpus/lessons/round-36-verifier-spotcheck.md:27-31`; `MANIFEST.json@e0144996` rounds 36, 39 |
| F7 | LOW | "Latest admitted round grading the axis improved" is oracle-dependent: adjacency reads 19 from the fleet MANIFEST (`rounds[398]@63729047`, cell says so accurately, rev is an ancestor of e0144996) and 18 from the lane's own closure series (`round-18-verifier-spotcheck.md:124`). Only the contract's pinned oracle fixes N\*. | `SCORECARD.md:15`; `MANIFEST.json@63729047` rounds[398] |
| F8 | — (no defect) | The obvious labelling fix (renaming the header to "Last verdict change") breaks the frozen counter (`mismatches=6`); the safe correction is prose only and was verified to keep `C1=met`. | `.ufo/waves/round-50/count-c1.py:109-115`; §8 above |
| F9 | — (no defect) | Convention-side claim checked and refuted: round 36's admitted `freshness-technique` exploratory verdict is *not* a missed freshness move, so freshness N\*=28 holds; likewise no closure after any N\* grades that axis improved. | `corpus/lessons/round-36-verifier-spotcheck.md:27-31`; §2 A5 |
