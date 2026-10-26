# Mo50bRevAxesCells — review of the four edited `## Axes` rows and the Round-50 correction paragraph

- Seat: Mo50bRevAxesCells (reviewer, wave a2w1, mori round 50 attempt 2). Leaf seat; no subagents used.
- Object: `SCORECARD.md` diff `9b8562a371dc916fdc0fc686619ea1e271a3e118` → `487941b9395e89678af0053cc443cdb49cdee6e3`
  (blobs `b4c6ef77b7c2051457beecf4804f30ebc0384b0e` → `9a01ef4dfc4b5fc587a51d343ffbce022f482647`, from
  `git rev-parse <rev>:SCORECARD.md`), plus the four cited spot-check pointers in
  `corpus/lessons/round-47-verifier-spotcheck.md:67/:68` and `corpus/lessons/round-49-verifier-spotcheck.md:75/:76`
  (both files read at `487941b` via `git show`; line numbers are those blobs' line numbers).
- All reads were repo/git/jq reads. No host log, cgroup or service state was touched; no MACHINE_ID owed.
- No tools installed or upgraded. Scratch `/fast/scratch/hyaku/mori-r50/Mo50bRevAxesCells/` (disk-guard status taken
  first: 615.5G free on `/fast/scratch/hyaku`); removed after this report was written; all quotes below are copied here.

## Method (commands and results)

- `git -C mori-shokunin diff 9b8562a 487941b -- SCORECARD.md` → exactly one hunk `@@ -7,17 +7,23 @@`, 10 insertions /
  4 deletions: the coverage, operability, depth and calibration rows rewritten and a 6-line `Round-50 correction`
  paragraph inserted at lines 21-25. Freshness (line 13) and adjacency (line 15) rows and the Score column of every
  row are byte-identical (confirmed by materializing both blobs to scratch and `diff -u`-ing them: same single hunk).
- `git show 487941b:corpus/lessons/round-47-verifier-spotcheck.md`, `…round-49…`, `…round-12/14/24/25/26/28/31…` →
  every line cited by the four rows opened at its cited number.
- `git -C shokunin show e014499613f63f8a467821219b0296121119ca53:MANIFEST.json | jq …` → per-axis latest admitted
  mori `improved` round (see §5).
- `python3 .ufo/waves/round-50/count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3` → `C1=met items=8 axes=6 pins=2
  boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b…`, rc 0. `manifest=a94551c5bc8d` is
  sha256 of the MANIFEST.json bytes at `e014499` (recomputed: `a94551c5bc8d0cc0…`), i.e. the counter measured the
  same manifest the paragraph cites.

## 1. The four cited spot-check pointers — parentheticals faithful

| Cell (SCORECARD.md line) | Pointer | Line content (quoted) | Cell's parenthetical | Verdict |
|---|---|---|---|---|
| :11 operability | `round-47-verifier-spotcheck.md:67` | ``\| operability \| improved \| new reconciler `tools/mori-pin-check.py` with a registered 34-arm selftest (evidence-verified, not executed) \|`` | "(new reconciler `tools/mori-pin-check.py`, evidence-verified)" | Faithful on grade and subject; **drops the closure's "(…, not executed)" qualifier and the 34-arm detail** — see Finding 1 |
| :10 coverage | `round-47-verifier-spotcheck.md:68` | ``\| coverage \| improved \| FR13 held as a full event set plus lifecycle; README block added; previously only abstract-level S262 and queued S005 \|`` | "(FR13 held as a full event set plus lifecycle)" | Verbatim prefix of the basis. Faithful |
| :14 calibration | `round-49-verifier-spotcheck.md:75` | `\| calibration \| 5 \| improved \| C1 verified; no score change claimed \|` | "(C1 verified, no score change claimed)" | Verbatim (semicolon → comma). Faithful |
| :12 depth | `round-49-verifier-spotcheck.md:75→76` | `\| depth \| 5 \| improved \| C2 re-measured 21/21 \|` | "(C2 re-measured 21/21)" | Verbatim. Faithful |

Two wording notes, both with the claim itself true:

- Finding 2 (LOW): the clauses "and states no new number (`…round-47-verifier-spotcheck.md:67`)":11 and "(…:68)":10
  are supported at `round-47-verifier-spotcheck.md:61` — "`git diff 2d85e33 dd17d927 -- SCORECARD.md` is 22
  insertions, 0 deletions; the Axes table is unchanged and no score change is claimed." — not on the cited lines
  themselves, which carry only the per-axis grade rows. Citation imprecision, not a false claim.
- The depth cell's "states the score 5" (:12) rests on the `entering` column 5 at r49:76 plus the section header
  `### C2 (depth, held 5)` (r49:57); calibration's "states the score 5" (:14) on `entering` 5 plus "no score change
  claimed" at r49:75, and r49:55 "The score stays 5 and the lane claims no score change". Supported.

## 2. Old history kept after `;` — not altered in meaning

Compared cell-by-cell between blobs `b4c6ef77` (old) and `9a01ef4d` (new):

- coverage :10 — old evidence history kept verbatim; the only edit inside kept text is the rename
  "latest admitted closure grades coverage improved and states no new number (…:133)" → "round-26 closure grades…".
  Required once a newer latest entry (round 47) is prepended contextually; meaning preserved. Last change cell keeps
  the old lead: "round 26 (improved, score held) before the round-50 correction".
- operability :11 — same single rename for the round-31 segment ("latest admitted closure grades operability
  improved (blind-writer gate `tools/mori-blind-check.sh`, C2 verified) and states the score stays 7" → "round-31
  closure grades…"); the round-35 and round-37 segments ("round-37 C2 verified the probe's hardening as named,
  mutation-killable arms and re-attributed that claim here (SCORECARD round-37 post-data correction; round-38
  axes-cell correction)") are verbatim. Last change keeps "round 31 … before the round-50 correction; round-37 C2
  re-attributed here (score held, 7)" verbatim.
- depth :12 — round-31 segment renamed identically; "round 27's depth improvement was verified under a
  rejected-honest-stop closure and is not counted" and the round-35 correction verbatim; new round-49 segment
  appended at the end. Last change keeps "round 31 (improved, score held) before the round-50 correction".
- calibration :14 — round-25 segment renamed identically; round-24 "Score 5 → 5" segment and the round-37 trailing
  history ("round-37 claim C1 closed the r36 measurement-discrimination defect and states no new number") verbatim.

Kept-history spot-checks beyond the diff: the depth parenthetical "(watchdog identity decision table, C1
re-measured)" matches `round-31-verifier-spotcheck.md:81` ("### C1 — depth: watchdog identity decision table —
**verified (re-measured)**"); the operability round-31 "blind-writer gate … C2 verified … stays 7" matches r31:155
("\| operability \| improved \| C2 verified (§3); the score stays 7 \|") with the gate named in the round-31
residual list (r31:214).

## 3. Scores untouched

Score column (col 2) identical old → new in all six rows: coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6. Freshness and adjacency rows are byte-identical. No other region of SCORECARD.md changed
(single hunk). The frozen C1 counter explicitly does not check the Score column (`count-c1.py:25`, "the Score column
is not checked (MANIFEST holds verdicts, not scores)"); that gap is what this manual check closes.

## 4. No closure states a different score

Every closure cited by the four edited rows, at its cited line, at `487941b`:

- r24:68 — "…unchecked, as disclosed. Score 5 → 5." (calibration 5 ✓)
- r24:88 — "Ruling: improved, bounded. … Score 6 → 6." (coverage 6 ✓)
- r26:133 — "\| coverage \| improved \| C2 capability evidence-verified, before and freeze re-measured \|" (no number ✓)
- r25:124 — "\| calibration \| improved \| C1 4 → 0 re-measured; three wrong Axes scores corrected; … \|" (no axis-score number; "4 → 0" is a mismatch count ✓)
- r28:93 — "\| operability \| improved \| C2 verified: ten A2 rules pinned by 30 frozen cases, PASS 30/30, tool unchanged \|" (✓)
- r31:154 — "\| depth \| improved \| C1 verified (§3); score stays 5 unless a closure states the move. This closure states none \|" (✓)
- r31:155 — "\| operability \| improved \| C2 verified (§3); the score stays 7 \|" (✓)
- r14:87 — "…holds coverage6/operability7/depth5/freshness5/calibration5/adjacency6. Repair is not an extra scalar point." (all six ✓)
- r12:17 — "ADMITTED after post-review fixes a7f1ecb. Depth improved (…score 4→5); calibration improved …, score held 5 …; coverage improved (silence grading 9→23 lanes …)." (✓; the kept coverage "score 5 → 6 then" clause matches SCORECARD's own round-12 table row, line 621)
- r47 (new citations): :61 "no score change is claimed"; per-axis rows :65-:70 grade only, no scores stated.
- r49 (new citations): :55 "The score stays 5 and the lane claims no score change"; :57 "### C2 (depth, held 5)";
  per-axis :75-:80 entering 5/5/6/7/5/6, verdicts improved/improved/unchanged×4, no new numbers.

**No closure states a score different from the cell's score; nothing to quote as a contradiction.**

## 5. `Round-50 correction` paragraph (SCORECARD.md:21-25) fact-check

- "they named rounds 26, 31, 31 and 25" — old Last change cells: coverage "round 26", operability "round 31",
  depth "round 31", calibration "round 25". ✓
- "the fleet `MANIFEST.json` at `e014499613f63f8a467821219b0296121119ca53` records the latest admitted mori round
  grading each axis improved as 47, 47, 49 and 49" — jq over that blob:
  `{coverage: 47, operability: 47, depth: 49, calibration: 49}` (max `lane_round` with `verdict=="admitted"` and
  `verdicts.<axis>=="improved"`; round 48/49 graded coverage/operability unchanged, so 47 is genuinely their last).
  ✓ Cross-check: the same manifest's freshness/adjacency targets (28, 19) match the two untouched Last change cells.
- "Each cell now leads with that round and keeps the older history after a `;`" — verified per row in §2. ✓
- "scores are unchanged because no closure states a new number" — verified in §4. ✓
- "Checked by `python3 .ufo/waves/round-50/count-c1.py <rev>`" — rerun by this seat at the landed rev: `C1=met …
  mismatches=0 errors=0 hidden=0`, rc 0; the counter's per-axis items (`axis calibration expect=round_49_improved
  got=ok`, etc.) agree with the manual reading. ✓

## Findings

- **LOW — SCORECARD.md:11** (operability row, new round-47 segment): the parenthetical "(new reconciler
  `tools/mori-pin-check.py`, evidence-verified)" drops the closure's disclosure "(evidence-verified, **not
  executed**)" (`round-47-verifier-spotcheck.md:67`) and the "registered 34-arm selftest" detail. The cell stays
  literally true — "evidence-verified" is the closure's own word — but a reader of the scorecard alone loses that
  the reconciler's selftest was not executed. Suggested wording for the L1 if adopted: "(new reconciler
  `tools/mori-pin-check.py`, evidence-verified not executed)".
- **LOW — SCORECARD.md:10 and :11**: the "and states no new number (`corpus/lessons/round-47-verifier-spotcheck.md:
  67`/:68)" clauses cite the per-axis grade rows; the "no score change is claimed" statement those clauses assert
  lives six lines earlier in the same section (`round-47-verifier-spotcheck.md:61`). Claim true; pointer imprecise.

No HIGH or MED findings. The four parentheticals are faithful, kept history is meaning-preserving (only the four
necessary "latest admitted closure" → "round-N closure" renames), scores are untouched, and no cited closure states
a different score.

## Residual risk / verification gaps

- I did not re-open the full bodies of rounds 12-14, 24-28, 31 beyond the cited lines and the two kept
  parentheticals (r31:81, r31:214); their cited lines all check out as quoted in §4.
- The counter's named limits stand (`count-c1.py:25-28`): it does not check the Score column and does not prove a
  tally's arms are good — both outside this seat's scope; the Score column was checked manually here (§3).
- MANIFEST verdicts are per-round grades, not per-line quotes; the r47/r49 verdict rows were verified verbatim, and
  both rounds are `admitted` in the same manifest (r47 and r49 present in the admitted set).
- Scratch removed; nothing cited remains outside this report.
