# Round 29 wave 1 — CriticC1Design: attack on claim C1 (calibration) before data

Seat: MoriR29.CriticC1Design (critic, leaf). Inputs read: `.ufo/waves/round-29/contract.md` at `8a45cefe`, `AXES.md`
(fleet root), `SCORECARD.md` and `corpus/lessons/round-N-verifier-spotcheck.md` at `7118f320`, fleet `MANIFEST.json` at
`63729047`. Not opened: the oom-killers tool, any round-26/27/28 w1/w2 report, the C1 counter draft. No files written
except this report. No tools installed or upgraded. No web sources fetched.

Method for the counterexamples: a throwaway Python script fed on stdin (nothing saved to disk) applies the four
mismatch kinds exactly as the contract words them (`contract.md:29-37`). It reads the six Axes rows
(`SCORECARD.md:10-15` at `7118f320`), takes the admitted rounds from MANIFEST `verdict == "admitted"`, and treats
"improved" as a lane line matching `^| <axis> | improved |`. On the unmodified table it reports kind-1 mismatches
for coverage (R=26), operability (R=28), freshness (R=28), calibration (R=25) and adjacency (R=18), and no other
kind. That matches the contract's expectation that the before value is non-zero. [INFERENCE] The committed counter
may differ in parsing details. The findings below follow from the contract wording, not from that counter.

## Verdict

C1 as written can reach `mismatches=0` through bookkeeping alone. Two in-memory edits of the 7118f320 table, which
add pointers only and leave every stale cell in place, both score 0 mismatches. Kind 4 becomes vacuous on any row
that satisfies kind 1. Kind 3 checks line counts, not content. Kind 2 does not check what the last-change cell
asserts. Lane-file-only closure detection also hides admitted improvements from rounds 12 and 19. The defects are
fixable inside the counter. The amendments below make C1 harder to meet and keep all six rows in scope.

## Ranked findings

### F1 (critical): kind 4 is vacuous once kind 1 holds, so any score passes, lowered or raised

- Counterexample 1 (simulated, mismatches=0): append `` `corpus/lessons/round-R-verifier-spotcheck.md:1` `` to the
  coverage, operability, freshness, calibration and adjacency rows. Set freshness 5 → 9 and adjacency 6 → 2. Leave
  every Last change cell unchanged. Result: `[]`, `mismatches= 0`.
- Why: kind 4 (`contract.md:36-37`) is met whenever the row cites any admitted spot-check that says `improved` for
  that axis. Kind 1 (`contract.md:29-31`) forces exactly that citation on every axis that has an R. So for 5 of the 6
  rows, any score is accepted if kind 1 passes. Kind 4 never checks direction or size. It also never checks that the
  closure states the new number.
- A lowered score evades kind 4. The adjacency row goes 6 → 2 while citing round 18, whose adjacency line reads
  `improved` (`round-18-verifier-spotcheck.md:124`).
- The score policy, which would block this, is declared "binding on the fix, not on the counter"
  (`contract.md:47`). So the counted claim does not check the score policy.
- Axes hit: calibration (the claim's own axis), because a passing counter would certify misstatements.

### F2 (high): pointers are checked for line count and substring only

- Counterexample 2 (simulated, mismatches=0). Each edit below would pass:
  - Coverage evidence becomes the prose "no closure ever cited `corpus/lessons/round-26-verifier-spotcheck.md` (not
    used)". Kind 1 is a substring test, so this negated citation passes.
  - Operability score becomes `11`. Its evidence becomes `` `tools/no-such-tool.sh`; `corpus/lessons/round-28-verifier-spotcheck.md:97` ``.
    Line 97 is the adjacency line (`round-28-verifier-spotcheck.md:97`), and the bare dead path is never checked.
  - Freshness score becomes `unprovable-but-better` with no reviewer, citing round 28 line 1.
  - Calibration last change becomes `r29`.
  - Depth evidence becomes `-`.
- Why:
  - Kind 3 (`contract.md:34-35`) covers only `path:L` tokens and only checks `max(L, M)` against the line count.
    The cited line is never required to support the row.
  - Kind 1 says the row "must cite" a file, with no form required.
- Also hit: AXES requires a score of 0–10 (`AXES.md:79`). No kind checks the range or that the score is a number.

### F3 (high): two closure authorities, and the lane-file one is blind to rounds 12 and 19 (hides a stale adjacency row)

- The pinned MANIFEST has its own per-axis `verdicts` map for every mori round. The contract uses it only for
  admission and reads "improved" from lane files. MANIFEST dump (command:
  `git show 63729047:MANIFEST.json | python3 …`, mori `lane_round` 12–28):
  - Round 12: admitted, depth, calibration and coverage improved. The lane `round-12-verifier-spotcheck.md` has no
    per-axis table, only prose at line 17 ("Depth improved … score 4→5").
  - Round 19: admitted, adjacency and calibration improved, spot-check "Inline in this durable closure row"
    pointing to `corpus/lessons/round-19.md`. There is no lane spot-check file.
  - Round 21: admitted, freshness and calibration improved, spot-check `None`.
  - Round 22: admitted, calibration improved, spot-check "Recorded in this MANIFEST entry only".
- Effect on R (lane files vs MANIFEST):
  - Adjacency: 18 vs **19**.
  - Depth: none vs **12**.
  - Coverage 26, operability 28, freshness 28 and calibration 25 agree.
- So yes, rounds 19–22 hide one stale row. A counter built from lane files accepts an adjacency row that cites
  round 18, even though round 19 is a later admitted improved closure. Depth gets no kind-1 check at all.
- Where both sources exist (rounds 13–18 and 23–28), the lane per-axis lines and the MANIFEST verdicts agree on every
  axis (same script, 0 disagreements). Agreement is a current fact, not an enforced one.
- `admitted: true` and `verdict: "admitted"` agree for all mori rounds 12–28. The counter should name the one it reads.

### F4 (high): the Last change cell is not checked for what it asserts

- Kind 2 (`contract.md:32-33`) checks only that a leading `round N` with N ≥ 12 is an admitted round. It does not
  check the following:
  - **"round 1" is exempt.** Freshness, calibration and adjacency say `round 1` (`SCORECARD.md:13-15`). Yet MANIFEST
    has admitted improved verdicts for them in rounds 21/26/28, 12/18/19/21/22/24/25 and 14/18/19. That state passes
    kind 2 now and after the fix.
  - **Non-matching text skips the check.** `r29`, `Round 29` and `(none)` never trigger kind 2 (counterexample 2).
  - **The round's own record is not consulted.** Operability says `round 14 (6 → 7)` (`SCORECARD.md:11`). The
    round-14 closure gives operability `unchanged` (`round-14-verifier-spotcheck.md:92`), and the round-14 table
    says `**7 held**` (`SCORECARD.md:793`). The 7 came from rejected round 13 (`SCORECARD.md:744`; MANIFEST round 13
    `rejected-harmed`). Kind 2 passes this row because round 14 is admitted.
  - **The `(X → Y)` inside the cell** is never compared with the score cell or the closure.
- This answers the full-enumeration question. Each row asserts six things:
  1. The axis identity.
  2. A 0–10 score, or the exploratory form (verdict plus named reviewer, `AXES.md:79`).
  3. The evidence prose ("held 7 in every round table since round 13", "round-10 drift pin still red").
  4. That each cited line supports the row.
  5. A last-change round.
  6. A before → after pair inside that cell.
- The four kinds cover only pointer existence, citation presence, admission of the named round, and score
  difference from the baseline. Items 2, 4, 5 (beyond admission) and 6 are unchecked. Evidence prose (item 3) needs
  judgment; it is out of a counter's reach and should be named as an uncounted residual.

### F5 (medium): the score policy overreaches by admitting author-proposed numbers, and underreaches on the exploratory form

- Overreach: `contract.md:47-48` lets a score move when "the admitted round's declaration proposed it and its closure
  verdict is `improved`". The closure judges the claim, not the number:
  - Round 12's closure held calibration at 5 "because the outside reviewer could not derive 6"
    (`round-12-verifier-spotcheck.md:17`).
  - Round 28's per-axis lines carry no numbers (`round-28-verifier-spotcheck.md:92-97`), and its no-harm line says
    "no held score changed" (`:78-79`).
  - The live case: "round 28 proposed 6; C1 decides the row" (`contract.md:84`). Under this clause freshness moves
    5 → 6 on the author's number alone. AXES says "a score no reader can re-derive is an opinion, not a measurement"
    (`AXES.md:52-55`).
- Underreach: the policy and the kinds cover only numeric scores. The AXES contract also allows "`unprovable-but-better`
  verdict + named non-author reviewer" (`AXES.md:79`). None of mori rounds 12–28 has that verdict on an axis
  (MANIFEST dump; round 23 coverage is `unprovable`, rejected), so the gap is latent. The policy also says nothing
  about the Last change cell (see F4).

### F6 (medium): the kind 4 baseline lets the 7118f320 scores through unchecked

- Every row at its 7118f320 score passes kind 4 by definition. The baseline is itself the thing under calibration.
  Operability 7 is the example: earned in rejected round 13, held under an `unchanged` closure in round 14 (F4). Any
  error in the baseline is certified by `mismatches=0`.
- A1 below still defaults to the baseline when no closure states a number. The smallest harder step is to make
  every row report its basis, so a reader sees which scores rest on no closure.

### F7 (low, tradeoff, not a counter defect): the observable is narrower than the axis signal

- AXES gives the calibration signal as "SHONEN.md/SCORECARD entries match observed repo state" (`AXES.md:15`). C1
  compares six rows against the closure record, not against repo state. Outside the table, entries are visibly stale:
  - `## Planned` still says "Round 2: …" (`SCORECARD.md:27-30`).
  - `## Saturation` says the line is "to be declared" (`SCORECARD.md:594-596`), but it was declared in round 12
    (`SCORECARD.md:637-640`).
- The contract scopes C1 to the table explicitly (`contract.md:13-14`), so this is a declared tradeoff. The lesson
  must not describe C1=met as "SCORECARD matches repo state". Route the two sections as hygiene.

## Direct answers to the assignment questions

| Question | Answer | Finding |
|---|---|---|
| Can `mismatches=0` be reached by bookkeeping? | Yes. Two simulated pointer-only variants reach 0 with stale and arbitrary cells | F1, F2 |
| Is "latest admitted improved closure must be cited" the right observable? | It tests whether the citation is current, not whether the row agrees. It is necessary but not sufficient | F1, F4 |
| Are the four kinds a full enumeration? | No. Score value and range, cited-line content, last-change semantics and the inner before → after pair are unchecked | F2, F4 |
| Do rounds 19–22 without a lane file hide stale rows? | Yes for adjacency (R 18 vs 19). Round 12 also hides depth (R none vs 12) | F3 |
| Can a lowered score evade kind 4? | Yes. Adjacency 6 → 2 passes while citing round 18 | F1 |
| Does the score policy overreach or underreach AXES? | Both. It admits author numbers, and it ignores the exploratory form and the last-change cell | F5 |

## Smallest amendment (harder, never narrower; all six rows stay counted)

Text to paste as a contract amendment, fixed before the counter lands:

```text
C1 amendment A1 (fixed before the counter lands; replaces kinds 1, 2, 4 and extends 3; adds 5):

Closure authority: the pinned fleet MANIFEST. For axis a, Imp(a) = { N in 12..28 : the mori round-N entry has
verdict "admitted" and verdicts.a == "improved" }; R(a) = max Imp(a). Cite(N) = the lane file
corpus/lessons/round-N-verifier-spotcheck.md when it exists at <rev>, else the path named by the entry's
verification.spotcheck, else the token `MANIFEST.json@63729047 mori round N`.

1. Stale closure: if R(a) exists, the row carries a backticked `Cite(R):L` token. When Cite(R) is a lane
   spot-check with a per-axis table, line L must match `^| a | improved |`.
2. Last change: the cell opens with `round N`, otherwise mismatch. N is an admitted round (any N), and N >= R(a)
   when R(a) exists. If the cell carries `(X → Y)`, Y equals the score cell.
3. Dead pointer: every backticked token containing `/` or ending in `.md`/`.json`/`.py`/`.sh` names a file that
   exists at <rev>; `path:L`/`path:L-M` also need max(L, M) lines.
4. Score without basis: the score cell is an integer 0..10, or reads `unprovable-but-better` with a named
   non-author reviewer and cites an admitted closure that records that verdict for a. A numeric score differs from
   its 7118f320 value only if the row cites `Cite(N):L` for an admitted N whose line L states `Score X → Y` (or
   `X → Y`) for a, with X = the 7118f320 score and Y = the new score. This applies in either direction.
   Declaration-proposed numbers are not a basis.
5. Closure disagreement: for every N in 12..28 with a lane per-axis table, each axis line's verdict equals the
   MANIFEST verdicts.a for round N.

The counter prints one line per row: axis, score, basis=<closure round N | baseline>, R, and the kinds hit.
Score policy (contract.md:47-49): delete "or the admitted round's declaration proposed it".
```

Expected effect of A1, from my reading of the contract wording [INFERENCE until the committed counter runs]:

- Both simulated variants become non-zero.
- At 7118f320, the new kind 2 fails freshness, calibration and adjacency (`round 1` < R). It also fails
  operability, because `round 14` < R = 28 (the cell's `(6 → 7)` gives Y = 7, which equals the score, so only the
  N >= R check fails).
- Adjacency must now cite round 19 (`corpus/lessons/round-19.md`, per MANIFEST `verification.spotcheck`), not
  round 18.
- Depth gains a round-12 pointer requirement.
- Freshness can reach 6 only if some admitted closure states "5 → 6" for freshness. Round 28's closure states no
  number (`round-28-verifier-spotcheck.md:92-97`), so the row would read "improved (closure round 28), score held"
  at 5.
- Kind 5 is 0 at 7118f320 by my cross-check, so it adds protection without moving the before value.

## Residuals routed (not counted)

- Evidence-prose truth per row, for example "census `--selftest` PASS (134 cases)" (`SCORECARD.md:11`) and
  "round-10 drift pin still red" (`SCORECARD.md:13`), needs a non-author reader in wave 2. Name it in the lesson as
  uncounted.
- `## Planned` and `## Saturation` staleness (F7): hygiene, outside C1.

## Evidence index

- Contract kinds and policy: `.ufo/waves/round-29/contract.md:29-37`, `:44-49`, `:84`.
- AXES: `AXES.md:15`, `:52-55`, `:75-83`.
- Axes table: `SCORECARD.md:8-15` at `7118f320`. Also `:27-30`, `:594-596`, `:637-640`, `:744`, `:793`, `:1151`.
- Lane per-axis lines (`git show 7118f320:corpus/lessons/round-N-verifier-spotcheck.md | grep -n '^| <axis> |'`):
  - round 13 at `:95-100`, round 14 at `:91-96`, round 15 at `:177-182`, round 16 at `:128-133`;
  - round 17 at `:234-239`, round 18 at `:124-129`, round 24 at `:104-109`, round 25 at `:124-129`;
  - round 26 at `:132-137`, round 27 at `:102-107`, round 28 at `:92-97`;
  - round 12 has no table (`:17` is prose); round 23 has none.
- MANIFEST mori rounds 12–28 (verdict, `admitted`, `verdicts`, `verification.spotcheck`): pinned revision
  `63729047`. Notes fields not copied (privacy).
- Cited pointer check: `round-24-verifier-spotcheck.md:88` ends "Score 6 → 6." and `:68` ends "Score 5 → 5.", so
  the existing coverage and calibration pointers are content-correct.
- Report written 2026-10-22T19:59Z (`date -u`).
