measured 2026-10-23T05:39:33Z

# JudgeLessonItem6 — Item 6 block (round-34 corrections, round-33.md)

Judged object: the `### Item 6 — the six-cell summary at :79 (and report :52-53)` block in `corpus/lessons/round-33.md` (## Round-34 corrections, lines 236-240) at `8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3`, answering routed defect §8 item 6 of `corpus/lessons/round-33-verifier-spotcheck.md:238-239` (lesson :79 and report :52-53 "no other word changed" vs S062/S064 word edits).

Method: committed bytes only, via read-only git in the lane; all sources dumped to scratch and read there. No tools installed or updated (no installs needed). No processes left running.

## Factual statements vs committed bytes

1. "The sentence at §3 line 79, 'no other word changed', is incorrect." — SUPPORTED. `round-33.md:79` at 8d56809 reads "Each lane-application clause is now declared with `lane rule:`; no other word changed (wave-1 ScopeS041, ScopeS044, ScopeS051, ScopeS062, ScopeS064, ScopeS069)."

2. "All six rows gained `lane rule:` labels" — SUPPORTED. `git diff 7d382043 89791013 -- corpus/SOURCES.md` (SOURCES-diff) shows S041, S044, S051, S062, S064, S069 each gained `lane rule:` insertions (S062 gained two; S064 gained one in scope + one in teaches).

3. "S062 changed 'no whitespace' to 'no whitespace between JSON tokens' (as already noted at :85-88)" — SUPPORTED. Old teaches cell: "no whitespace, error on NaN/Infinity" → new: "no whitespace between JSON tokens, error on NaN/Infinity". Lesson lines 85-88 record exactly this ("(wave-2 AttackScopeEdits: the RFC forbids whitespace between tokens, not inside strings)"). The wave-2 receipt `.ufo/waves/round-33/w2/AttackScopeEdits.md:23` agrees.

4. "S064 changed its teaches wording from 'Resolve a selector once … retain the full object id …' to 'Resolve a selector …; lane rule: do it once, retain the full object id …', moving 'once' and the procedure into the lane-rule clause" — SUPPORTED. Old teaches: "Resolve a selector once with --verify --end-of-options and commit peeling, retain the full object id, then separately bind…" → new: "Resolve a selector with --verify --end-of-options and commit peeling; lane rule: do it once, retain the full object id, then separately bind…" ("once" moved into the lane-rule clause; comma after "peeling" became "; lane rule:").

5. "its scope likewise labels 'not remote publication …' as a lane rule (:89-93)" — SUPPORTED. Scope cell old "existing commit object; not remote publication, source authenticity or input-tree equality" → new "existing commit object; lane rule: not remote publication, source authenticity or input-tree equality". Lesson S064 entry spans lines 89-93.

6. "S041, S044, S051 and S069 only gained the label in the clauses shown at :82-84 and :94." — SUPPORTED. Per-row old→new diffs differ only by insertion of "lane rule: " (S041 at lesson line 82, S044 at 83, S051 at 84, S069 at 94); all other cells byte-identical.

7. "The diff … confirms the S062 and S064 edits (SOURCES.md lines 68 and 70)." — SUPPORTED. At 89791013, SOURCES.md line 68 is S062 and line 70 is S064. The exact command `git -C … diff 7d382043 89791013 -- corpus/SOURCES.md` ran and produced the expected -/+ pairs.

8. "The fleet report's :52-53 summary is abbreviated: it records the label additions and unchanged status/recheck/used-by fields but does not enumerate these two text edits." — SUPPORTED. Report lines 52-54: "Touched: six teaches/scope cells (S041, S044, S051, S062, S064, S069) gained `lane rule:` labels, logged old→new in lesson §3; no status/recheck/used-by change." It does not enumerate the S062/S064 text edits.

## Append-only confirmation

`git diff f10a320d 8d56809 -- corpus/lessons/round-33.md` = single hunk `@@ -209,3 +209,53 @@`, 50 added lines, zero deletions, zero context modifications. Nothing above the "## Round-34 corrections" heading changed; each block, including Item 6, is a pure append. Line 79 is byte-identical across the range, so the correction's premise holds.

## Commit times (as instructed)

- 7d382043: 2026-10-22T23:21:08-03:00 (round-32 verifier spot-check)
- 89791013: 2026-10-23T00:16:50-03:00 (round-33 measured outcome/LOG/census end)
- f10a320d: 2026-10-23T00:27:16-03:00 (round-33 verifier spot-check)
- 8d56809: 2026-10-23T02:34:40-03:00 (round-34 lesson r33 corrections, pre-judgment)

The block cites no commit times; the cited diff endpoints exist and the diff matches.

## VERDICT: repaired

No wrong statement found in the Item 6 block. The six-cell summary at line 79 and the report's :52-53 summary are correctly characterized, the S062/S064 edits are correctly and precisely described (including "once" moving into the lane-rule clause and the scope attribution), and the fix is a pure append that changes nothing above the heading.

## Residual risk / verification gaps

- The fleet report `.ufo/reports/round-33/mori.md` is not committed in this lane (path absent at 8d56809; `git log --all -- <path>` empty; the spotcheck's cited report commit `80c15420…` is not an object in this repo). I verified report :52-53 against the live working-tree copy at the fleet root `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/mori.md` (mtime 2026-10-23 00:17). Its committed state in the fleet repo was not inspected [INFERENCE].
- The preamble's meta-claims (attempt-1 seat drafts, L1 integration, wave-A judging) are outside Item 6's factual core and were not independently re-verified; they do not affect the verdict.
- The "only gained the label" statement for S041/S044/S051/S069 holds for the SOURCES diff; the wave-2 receipt notes an additional S064 comma→semicolon punctuation change (`AttackScopeEdits.md:29`), which the block's S064 description already covers ("…; lane rule: do it once…").
