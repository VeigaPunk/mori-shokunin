# Mo52RevAxesCells — review of the edited SCORECARD `## Axes` cells and the freshness locator fix (mori round 52, wave w1)

Seat: Mo52RevAxesCells (reviewer, leaf — no subagents). Date 2026-10-26. Scope: the SCORECARD.md diff
`4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d → 8524904adb25e44f24d9f25aac7eae909625c18c` (three rows: operability,
depth, freshness), checked against `corpus/lessons/round-51-verifier-spotcheck.md:126-135`, the fleet
`/home/vgpnk/Projects/shokunin/MANIFEST.json` (mori round 51), and every other Axes-cell locator. Read-only
throughout; no counter was changed or proposed changed; scratch `/fast/scratch/hyaku/mori-r52/Mo52RevAxesCells/`
(removed afterwards).

## What the diff does

`git diff 4f266ef2 8524904 -- SCORECARD.md`: 3 insertions, 3 deletions, all in the `## Axes` table; Score cells
untouched (coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6).

- operability Evidence cell gains: `; round-51 closure grades operability improved (C1: a `--rev` pin re-execution
  is hermetic and classes mismatches) and states the score 7 (`corpus/lessons/round-51-verifier-spotcheck.md:130`)`;
  Last change now leads `round 51 (improved, score held); round 47 (improved, score held); round 31 …`.
- depth Evidence cell gains: `; round-51 closure grades depth improved (C2 re-measured 21/21, the MemAvailable
  entry) and states the score 5 (`corpus/lessons/round-51-verifier-spotcheck.md:131`)`; Last change leads
  `round 51 (improved, score held); round 50 …; round 49 …; round 31 …`.
- freshness Evidence cell: locator `SCORECARD.md:1771` → `SCORECARD.md:1781`; no other change to the row.

## Verification performed (command → observed)

1. Round-51 closure per-axis table (`sed -n '126,135p' corpus/lessons/round-51-verifier-spotcheck.md`):
   `| operability | 7 | improved | C1: committed receipts before unmet → after met (125/0 self-test), frozen bytes
   intact, code re-measured. Score held |` at :130 and `| depth | 5 | improved | C2 re-measured 21/21 located,
   21/21 entailed, live sources equal the copies. Score held |` at :131. §2 headings: `### C1 (operability, held 7):
   `--rev` pin re-execution is hermetic and classes mismatches` and `### C2 (depth, held 5): what MemAvailable is
   at v7.2`. Both cell paraphrases are the closure's own wording; both cited lines carry the score numbers and
   "Score held". "States the score 7/5" is accurate: the closure grades (improved) and holds (7 / 5).
2. Fleet MANIFEST, mori round 51 (`rounds[786]`): `admitted: true`, `verdicts: {operability: improved, depth:
   improved, coverage/freshness/calibration/adjacency: unchanged}` — exactly what the two appended sentences and the
   untouched Score cells say. Rounds 48 (`rounds[714]`) and 49 (`rounds[723]`) have operability unchanged, so round
   51 is the first admitted round to grade operability improved since 47. No newer mori admission exists (mori's
   newest MANIFEST round is 51 at index 786; the list ends at index 788, a kama round).
3. Freshness locator: at 8524904, `SCORECARD.md:1781` is the `### Round 28 measured outcome` C1 row and holds
   "freshness 5 → 6 proposed"; the old `:1771` was the "Round-28 amendment A1" paragraph, which holds no 5 → 6
   (this was entering mismatch #8). Fix is correct and the row's "not adopted because no closure states it" matches
   the line's "improved, pending closure" wording.
4. Every other cell still resolves — direct reads of all cited locators at 8524904: round-12:17 (depth 4→5 stated),
   round-14:87 (holds coverage6/operability7/depth5/freshness5/calibration5/adjacency6; per-axis table two lines
   below grades operability unchanged), round-24:88 ("Score 6 → 6"), round-24:68 ("Score 5 → 5"), round-25:124 and
   round-26:133 and round-28:92/93, round-31:154/155 ("score stays 5"/"the score stays 7"), round-47:67/68,
   round-49:75/76, round-50:125/126, round-51:130/131, `SCORECARD.md` "Round 24 measured outcome" section pointer
   (heading at SCORECARD.md:1523), and the adjacency citation `MANIFEST.json@63729047` — `63729047` is a commit;
   its `MANIFEST.json` `rounds[398]` is mori round 19, `admitted: true`, `verdicts.adjacency: improved`.
5. Counter corroboration (committed receipt `.ufo/waves/round-52/evidence/c1-at-data.txt`, literal command with
   scratch path recorded): at 8524904, `C1=met items=42 axes=6 … locators=27 mismatches=0 errors=0 … exit=0`; arm A
   prints `operability expect=round_51_improved got=ok` and `depth expect=round_51_improved got=ok`; arm D prints
   `SCORECARD.md:1781 expect=pair:5_→_6 got=found` and `round-51…:130/:131 expect=range got=ok`.
6. `git diff 8524904 HEAD -- SCORECARD.md` is empty (HEAD now 075436b1), so the reviewed cells are the live bytes.

## Findings

- MED — SCORECARD.md operability Evidence cell (row 11 at 8524904): the diff appends the round-51 sentence after an
  untouched clause that still reads "latest admitted closure grades operability improved (new reconciler
  `tools/mori-pin-check.py`, evidence-verified) and states no new number
  (`corpus/lessons/round-47-verifier-spotcheck.md:67`)". With mori round 51 admitted and grading operability
  improved (MANIFEST rounds[786]), that superlative is now false inside the same cell the calibration claim
  surfaces — the cell names round 47 as the latest admitted closure and then cites a later admitted closure that
  states the score 7. True at the entering tip (rounds 48-51 operability unchanged before 51), made false by this
  append. Data-side fix for the L1: demote to "the round-47 closure …" (the depth and calibration cells carry the
  same stale superlative, see next item). Frozen counters, predicates and controls untouched; the frozen counter
  passes over it because prose before a pointer is only range-checked (contract named limit).
- LOW — pre-existing, not introduced here: depth and calibration Evidence cells keep "latest admitted closure …"
  pointing at round-49 lines while later admitted closures grading the axis improved (round 50, now also round 51
  for depth) are cited later in the same cell (MANIFEST rounds[754] admitted, calibration+depth improved). The
  convention of appending without demoting the earlier superlative is what produced the MED item; a one-line demotion
  in each cell would make the whole table self-consistent.
- LOW — counter named limit confirmed in the wild (routed, not fixable this round): arm A validates the Last-change
  lead and the newest closure's per-axis scores but never reads the "latest admitted closure" prose, so a cell can
  be internally contradictory and still read `state=ok` (`c1-at-data.txt`). Record as a round-53 counter item.

## Verified accurate (no finding)

- "states the score 7/5" for the round-51 closure: accurate — the closure's per-axis rows carry `| operability | 7 |`
  / `| depth | 5 |` with verdict "improved" and "Score held", and §2 headings say "(operability, held 7)" /
  "(depth, held 5)".
- Both appended parentheticals quote the closure's own §2 headings; "C2 re-measured 21/21, the MemAvailable entry"
  matches the closure's C2 subject (what MemAvailable is at v7.2).
- Last-change leads "round 51 (improved, score held)" for operability and depth agree with MANIFEST rounds[786] and
  with the counter's expectation line.
- Freshness `SCORECARD.md:1781` fix lands on the quoted "5 → 6" pair; the row's story (proposed at round 28's
  measured outcome, never stated by a closure) matches the cited line.
- All six Score values unchanged; diff touches exactly the three named rows; nothing else in SCORECARD.md moved at
  the data commit or since.

## Residual risk and verification gaps

- I did not re-execute `count-c1.py` myself; the `C1=met … mismatches=0` reading is cited from the committed receipt
  `.ufo/waves/round-52/evidence/c1-at-data.txt` (UNVERIFIED by my own run, VERIFIED as a committed receipt whose
  literal command is recorded). Every locator and MANIFEST claim above I did verify directly by read.
- Fleet MANIFEST.json was read from the working tree at /home/vgpnk/Projects/shokunin; rounds 48-51 fields could in
  principle differ in a pinned revision (the adjacency cell pins its own blob and I checked that one at 63729047).
- Whether the L1 treats the stale "latest admitted closure" prose as data-correctable wording (allowed: data diff
  may be corrected by the L1) is the L1's call; this report proposes wording only, never counter/predicate changes.
