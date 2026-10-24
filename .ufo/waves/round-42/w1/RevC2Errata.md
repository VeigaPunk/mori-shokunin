# RevC2Errata — review: round-42 LOG/SCORECARD errata vs r41 routed defects 1–3

Role: reviewer (round-42 v2 wave). Scope: errata correctness and completeness;
sweep for uncontradicted re-assertions in lane-owned r42 records.
Attack tip: `34b926730c30e0251e1aec531863d8355dc491f1`. Read-only review; no repo
writes. Reference: routed defects 1–3 in
`corpus/lessons/round-41-verifier-spotcheck.md:99-103`.

## Verdict

**All three errata discharge the routed defects.** No actionable defect found in
scope. One informational residual noted below.

## Per-item verification

### (a) "8/8 mutants killed" → "5/8 killed, 3 SURVIVED" — VERIFIED

- Superseded text named and accurately quoted: the fleet r41 report at
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/mori.md:127` reads
  "…w1 mutation seats: 8/8 mutants killed" — verbatim to the errata quote.
- Correction is true: exactly 8 mutation reports exist under
  `.ufo/waves/round-41/w1/`. The three named files each carry a SURVIVED verdict —
  `MutC1Walrus.md:72` "**Verdict: SURVIVED.**", `MutC1Tuple.md:124`
  "**SURVIVED** — coverage finding", `MutC1DropSort.md:10` "**SURVIVED.**".
  The other five declare killed (`MutC1DeadLoop.md:98`, `MutC1EarlyContinue.md:107`,
  `MutC2DeadPair.md:87`, `MutC2GlobalColmap.md:98`, `MutC2WalkIndex.md:117`).
  5 killed + 3 SURVIVED = 8; the routed defect's tally is exact.
- Recorded in `LOG.md:2397-2401` and `SCORECARD.md:2335-2336`; the three
  SURVIVED reports are named in both, per the defect's remedy.

### (b) "34 attack seats (53%)" → "31 attack seats of 64 (48.4%)" — VERIFIED

- Superseded text verbatim: fleet r41 report `:143` reads "= 34 attack seats
  (53%)" and "attack seats returned 9/34".
- Spec definition re-derived: `.ufo/waves/round-41/w1-spec.json` roles =
  {scout 22, reviewer 12, critic 11, mutation-tester 8, scribe 7, executor 3,
  connector 1}, total 64; its context line states "31/64 seats are attack roles
  (48.4%)". 12+11+8 = 31; 31/64 = 48.4375% → 48.4%. Executors are correctly
  excluded from attack roles.
- "matching w1-spec.json, LOG and SCORECARD" confirmed: `LOG.md:2360`
  "64 seats, 31 attack = 48.4%" and `SCORECARD.md:2306-2307` "64 seats
  (31 attack = 48.4%)" — both r41 records held the spec definition; only the
  fleet report prose deviated.
- Recorded in `LOG.md:2402-2405` and `SCORECARD.md:2336-2338` with the full
  spec-definition decomposition.

### (c) "2 scouts, 4 scribes" → "1 scout, 5 scribes", total 19 — VERIFIED

- Superseded text verbatim: fleet r41 report `:143` reads "(1 connector,
  3 executors, 8 mutation-testers, 1 reviewer, 2 scouts, 4 scribes — …)".
- Correction is true: `.ufo/waves/round-41/w1/` holds 19 `.md` reports —
  5 `Scr*` (ScrLog, ScrM25Survivor, ScrM26Number, ScrReport, ScrS230Quote),
  1 `Scout*` (ScoutSOURCESRows); the five scribe files are named in the LOG
  erratum (`LOG.md:2407-2408`), total 19 correct and unchanged.
- The frozen counter independently derives this: `count-c2.py:76-81`
  counts `Scr*`/`Scout*` prefixes and asserts Scr=5 Scout=1;
  `evidence/c2-after.txt` shows `evidence_roles PASS` at tip.

## Sweep: no lane-owned r42 record re-asserts superseded values uncontradicted

Greps for `8/8 mutants`, `34 attack`, `9/34`, `53%`, `2 scouts`, `4 scribes`,
`all eight mutants`, `two scouts`, `four scribes`, `thirty-four attack`,
`9/31` over `LOG.md`, `SCORECARD.md`, `corpus/`, `.ufo/waves/round-42/`:

- `LOG.md` / `SCORECARD.md`: the only occurrences are the errata blocks
  themselves (LOG:2397-2409, SCORECARD:2334-2341), each superseded string
  quoted inside a "superseded by" clause. Other numeric hits ("all eight
  checks", "49–53%" PSI figures, r25/r32 tallies) are unrelated round or
  data contexts.
- `corpus/lessons/round-41-verifier-spotcheck.md`: quotes "8/8 mutants killed"
  at `:96` **with inline contradiction** ("is wrong — 5/8") — pre-existing
  contradiction, satisfied.
- `.ufo/waves/round-42/w1-spec.json` / `evidence/wave-plan.json`: hits are
  frozen seat-prompt text (including this seat's own item) that *quotes* the
  superseded strings together with their corrections — contradicted in place,
  not asserted as current values.
- `.ufo/waves/round-42/w1/MutC2Record.md`, `CritRecordsAppend.md`: peer
  reports describe the superseded values as mutation/critic targets — always
  in contradicted context.
- `contract.md:55-59` restates all three corrections verbatim; `:89` codifies
  "no record asserting 8/8, 34 attack, 53%, or 2 scouts, 4 scribes as
  current" as a contract clause.
- `corpus/QUALITY.md` 114 (new rule citing the r41 survivor class): no
  superseded figures.
- The frozen counter's own sweep (`count-c2.py:140-154`) checks the two
  append-only record surfaces; mutation-tested live by `w1/MutC2Record.md`
  (mutant re-asserting 8/8 → `C2=unmet` rc 1, both `log_erratum_tally` and
  `sweep_log_clean` flipped). KILLED — the erratum record is load-bearing.

## Residual risk / informational

- The defect-2 quote "attack seats returned **9/34**" is not restated in
  either erratum; the correction supersedes the 34-seat figure, which makes
  the correct denominator (31) available, but the "9/34" fraction is never
  explicitly corrected to 9/31. This matches the defect's stated remedy
  ("Fix the prose definition") and no lane record re-asserts "9/34", so it
  is not a defect — noted for the closure only.

## Tooling

No installs or updates. `python3`/`grep`/`ls` reads only; no pacman, no
sandbox execution needed.

Report: .ufo/waves/round-42/w1/RevC2Errata.md
