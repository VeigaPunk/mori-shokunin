measured 2026-10-23T07:47:31Z

# ReJudgeLesson6 — independent re-judgment of `### Item 6` (round-34 corrections)

Judged object: `corpus/lessons/round-33.md` lines 236–240 (`### Item 6 — the six-cell summary at :79 (and report :52-53)` + `#### Correction to §3's six-row change summary (append-only)`) at `8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3`, answering routed defect §8 item 6 (`corpus/lessons/round-33-verifier-spotcheck.md:238-239`). All facts re-derived from committed bytes with read-only git before opening the attempt-2 report. No tools installed; no processes left running.

## Independent fact-check of the Item 6 block

1. `:79` reads "Each lane-application clause is now declared with `lane rule:`; no other word changed (wave-1 ScopeS041, …)" — verified; the phrase is present and wrong (verified bytes, `round-33.md:79` at 8d56809).
2. "All six rows gained `lane rule:` labels" — verified: `git diff 7d382043 89791013 -- corpus/SOURCES.md` shows `lane rule:` insertions in S041, S044, S051, S062, S064, S069 only among the touched rows (S062 ×2 teaches; S064 ×1 scope + ×1 teaches).
3. "S062 and S064 also changed wording or attribution" — verified: S062 teaches "no whitespace," → "no whitespace between JSON tokens,"; S064 teaches moved "once" into the lane-rule clause; S064 scope gained `lane rule:` before "not remote publication".
4. S062 change "(as already noted at :85-88)" — verified: lesson :85-88 records the exact old→new and AttackScopeEdits rationale.
5. S064 description and "(:89-93)" — verified byte-for-byte against the SOURCES diff and lesson :89-93, including "not remote publication …" labelled in scope.
6. "S041, S044, S051 and S069 only gained the label in the clauses shown at :82-84 and :94" — verified: full-line diffs of those four rows show `lane rule:` insertion as the only change (S041 :82, S044 :83, S051 :84, S069 :94).
7. "diff … confirms the S062 and S064 edits (SOURCES.md lines 68 and 70)" — verified: at 89791013, `corpus/SOURCES.md:68` = S062 row, `:70` = S064 row; the cited command runs and shows both −/+ pairs.
8. "The fleet report's :52-53 summary is abbreviated … does not enumerate these two text edits" — verified: fleet `.ufo/reports/round-33/mori.md` committed in the fleet repo at `80c1542073dbf7d33a806d72725d186de3f2cb26` (committer 2026-10-23T00:17:20-03:00, subject "round-33: mori report"); :52-53 = "Touched: six teaches/scope cells (S041, S044, S051, S062, S064, S069) gained `lane rule:` labels, logged old→new in lesson §3; no status/recheck/used-by change." It names neither the S062 "between JSON tokens" edit nor the S064 teaches edit. Working-tree fleet copy is byte-identical to the committed blob (`git diff` empty).
9. Appendix-only: `git diff f10a320d 8d56809… -- corpus/lessons/round-33.md` = one hunk `@@ -209,3 +209,53 @@`, numstat `50 0` — zero deletions; the only `-` line is the `--- a/…` header.
10. Commit times: `7d382043` = 2026-10-22T23:21:08-03:00 ("round-32 verifier spot-check"); `89791013` = 2026-10-23T00:16:50-03:00 ("round-33: measured outcome, LOG, census end"). The diff endpoints straddle the label/word edits as the block implies.

Every factual statement in the block matches the committed bytes it points to. The correction names both word edits the defect flagged, is a pure append, and preserves both the wrong sentence (documented, not deleted) and the receipts.

## Audit of /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/JudgeLessonItem6.md

- Claim: judged block at `round-33.md:236-240` at 8d56809; defect at spotcheck `:238-239` — agree (verified: block :236-240; spotcheck item 6 at :238-239).
- Claim 1: `:79` contains "no other word changed" — agree (same bytes).
- Claim 2: six rows gained labels; S062 two, S064 one scope + one teaches — agree (diff counted).
- Claim 3: S062 "no whitespace" → "no whitespace between JSON tokens"; lesson :85-88; `AttackScopeEdits.md:23` agrees — agree (:23 shows the S062 `{+lane rule:+}` pair; the word edit is recorded in lesson :85-88 and the SOURCES diff).
- Claim 4: S064 teaches "once" moved into lane-rule clause — agree (byte-exact vs diff).
- Claim 5: S064 scope labels "not remote publication"; lesson span :89-93 — agree.
- Claim 6: S041/S044/S051/S069 insertion-only at lesson :82-84, :94 — agree (full-line diffs).
- Claim 7: SOURCES.md :68 = S062, :70 = S064 at 89791013; command runs — agree.
- Claim 8: report :52-53 "Touched: six … `lane rule:` labels … no status/recheck/used-by change", no word edits enumerated — agree (report text at 80c1542 :52-53 says "Touched: six teaches/scope cells" — the report's paraphrase "teaches/scope cells" is verbatim; the claim that the summary is abbreviated is fair since :52-53 omits the two text edits).
- Claim: append-only single hunk `@@ -209,3 +209,53 @@`, 50 added, 0 deleted — agree (numstat `50 0`, hunk header matches).
- Claim: commit times 7d382043 23:21:08-03; 89791013 00:16:50-03; f10a320d 00:27:16-03; 8d56809 02:34:40-03 with subjects — agree (all four `%cI` values and subjects confirmed).
- Residual claim: `.ufo/reports/round-33/mori.md` absent at lane 8d56809, `80c15420…` not a lane object — agree (`ls-tree` at 8d56809 shows no `.ufo/reports/`; `cat-file -t` fails in the lane repo).
- Residual claim: fleet committed state "not inspected [INFERENCE]" — agree as stated; note it is resolvable and now resolved against it: the file IS committed in the fleet repo at 80c1542 (2026-10-23T00:17:20-03:00) and equals the working-tree copy the report used, so the residual does not stand as a real gap.
- Residual claim: `AttackScopeEdits.md:29` notes the S064 comma→semicolon — agree (:29 states exactly that).
- Report verdict `repaired` — agree.

AUDIT: agree 15 / disagree 0

VERDICT: repaired
