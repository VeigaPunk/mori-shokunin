# ReviewAxisRowsProse — wave 2 findings (round 29, attempt 1)

Seat: MoriR29.ReviewAxisRowsProse (leaf; no subagents).
Scope: verify the six rewritten `## Axes` rows (SCORECARD.md:10-15) at lane tip
8809a3fe1eaa87a0afa177a15263d174378e7462 against cited pointers and pinned fleet
MANIFEST @63729047; check the round-25 correction paragraph (:17-19); flag stale
text in `## Planned` and `## Saturation`.

Method: rows read via `git -C <lane> show 8809a3fe:SCORECARD.md` (worktree lines
10-15 identical to tip; `git diff --exit-code 8809a3fe -- SCORECARD.md` shows the
worktree differs from tip ONLY by an uncommitted append of the Round 29 declaration,
:1777-1790, +15 lines). MANIFEST read via `git -C /home/vgpnk/Projects/shokunin
show 63729047:MANIFEST.json` (jq). No tools installed (jq already present); no
external sources opened; no git writes.

## 1. coverage row (SCORECARD.md:10)
- "per-surface notes landed (`corpus/knowledge/observability-surfaces-r2.md`)" — TRUE.
  File exists at tip; `git grep -cE '^## [1-7]\.' 8809a3fe -- corpus/knowledge/
  observability-surfaces-r2.md` → 7; round-2 verdict :115 records "seven per-surface
  sections ... → 7".
- "silence roster over the declared lanes (round 12, score 5 → 6 then)" — TRUE.
  :615 "| coverage | **improved** | 5 → 6 | claim 3; 14 lanes graded that were
  invisible"; claim 3 at :609: "silence roster = declared lanes ∪ driver counters ...
  live `SURFACE lane.*` rows 9 → 23".
- "one-shot system pressure read (round 24)" — TRUE. :1534 capability row
  "one-shot system pressure read ... | `tools/mori-pressure.py --selftest` PASS
  12/12 ... | 24".
- "round-24 closure "Score 6 → 6" (`corpus/lessons/round-24-verifier-spotcheck.md:88`)" —
  TRUE. That line reads "- **Ruling: improved, bounded.** ... Score 6 → 6."
- "latest admitted closure grades coverage improved and states no new number
  (`corpus/lessons/round-26-verifier-spotcheck.md:133`)" — TRUE. :133 reads
  "| coverage | improved | C2 capability evidence-verified, before and freeze
  re-measured |". Latest admitted coverage-improved closure is 26 (MANIFEST r25
  cov=improved admitted, r26 cov=improved admitted, r27 rejected, r28 cov=unchanged).
- Last change "round 26 (improved, score held)" — TRUE (score 6 held throughout
  26-29 held lines; r26 admitted).

## 2. operability row (SCORECARD.md:11)
- "census `--selftest` PASS (134 cases) before and after round 24 (`SCORECARD.md`
  round-24 measured outcome)" — TRUE. :1526-1527 "selftest `PASS (134 cases, 134
  passed, 0 failed)` before and after".
- "7 first held in round 13's table" — TRUE. Round-13 table :696 "| operability |
  improved | **6 → 7** |"; no earlier table ≥7 (r12 :616 = 6; rounds 2-11 ≤6).
- "which closed rejected-harmed" — TRUE. MANIFEST @63729047 rounds[13] mori:
  admitted=false verdict=rejected-harmed; :740 "Outside closure ... rejected round 13
  as harmed".
- "kept in every admitted round table since" — TRUE (checked). Admitted round tables:
  r14 :793 "7 held", r15 :875 "7 held", r16 :984 "7 held", r18 :1151 "7 held",
  r19 :1220 "7", r21/r22/r24 op=unchanged (MANIFEST), rounds 24-29 held lines record
  operability 7 (:1508,1527,1548,1571,1600,1622,1744,1774,1788). r17, r20, r23
  closed rejected (excluded from "admitted"); r17 table also shows 7 held (:1117).
- "round 14's closure grades operability unchanged" — TRUE. MANIFEST r14
  op=unchanged; :793 "7 held".
- "latest admitted closure grades operability improved (ten A2 rules pinned by 30
  frozen cases) and states no new number (`corpus/lessons/round-28-verifier-spotcheck.md:93`)" —
  TRUE. :93 reads "| operability | improved | C2 verified: ten A2 rules pinned by 30
  frozen cases, PASS 30/30, tool unchanged |". r28 is the latest admitted closure
  (r27 rejected); no new number stated.
- Last change "round 28 (improved, score held)" — TRUE (r28 admitted op=improved;
  score 7 held).

## 3. depth row (SCORECARD.md:12)
- "source-linked knowledge entries with `source:`/`verified-at:`/`recheck:` lines
  (round 12 claim 1)" — TRUE. Claim 1 at :607 "knowledge entries with `source:`/
  `verified-at:`/`recheck:` on lines 1–3 citing an A/mined row 0 → 4"; at tip
  `git grep -cE '^(source|verified-at|recheck):'` → those fields present in the r12
  knowledge family (kernel-oom-line-attribution-r12.md:3, kill-classes-by-message-id-r12.md:3,
  oom-kill-counter-kernel-only-r12.md:3, userspace-oom-killers-r12.md:3,
  roster-truth-r12.md:4) and elsewhere.
- "the round-12 closure states the move (`corpus/lessons/round-12-verifier-spotcheck.md:17`)" —
  TRUE. :17 "Depth improved (SKILL primary links 0→5; four sourced OOM notes; score
  4→5)".
- "round 27's depth improvement was verified under a rejected-honest-stop closure and
  is not counted" — TRUE. :1749 "round 27 closed `rejected-honest-stop`: C1 depth
  verified, C2 withdrawn and so not verified"; MANIFEST r27 admitted=false
  verdict=rejected-honest-stop dep=improved; table last-change remains round 12,
  score 5.
- Last change "round 12 (4 → 5)" — TRUE.

## 4. freshness row (SCORECARD.md:13)
- "the round-20 re-pin was rejected (`corpus/README.md` Round21 correction)" — TRUE.
  corpus/README.md:406-410 "CloseMori20 rejected the pin and QUALITY67's universal
  permission; QUALITY69 now supersedes67".
- "latest admitted closure grades freshness improved and states no new number
  (`corpus/lessons/round-28-verifier-spotcheck.md:92`)" — TRUE. :92 "| freshness |
  improved | C1 verified: eight carried row defects superseded by rows re-opened this
  round (hashes reproduced below), readers repointed |". Latest admitted
  freshness-improved closure is 28 (r26 fr=improved, r27 rejected, r28 fr=improved).
- "round 28's measured outcome proposed 5 → 6 (`SCORECARD.md:1771`), not adopted
  because no closure states it" — TRUE. :1771 ends "freshness 5 → 6 proposed";
  round-28 spotcheck :92 states no number; round-29 declaration :1788 holds
  "freshness 5".
- Last change "round 28 (improved, score held)" — TRUE.

## 5. calibration row (SCORECARD.md:14)
- "round 12's self-assessed 5 → 6 was not re-derived by the outside reviewer and held
  at 5" — TRUE. :658 "scalar score **held at 5**, not 6, because the non-author
  reviewer could not re-derive 6"; spotcheck :17 "score held 5 because the outside
  reviewer could not derive 6".
- "round-24 closure "Score 5 → 5" (`corpus/lessons/round-24-verifier-spotcheck.md:68`)" —
  TRUE. :68 ends "Score 5 → 5."
- "latest admitted closure grades calibration improved and states no new number
  (`corpus/lessons/round-25-verifier-spotcheck.md:124`)" — TRUE. :124 "| calibration |
  improved | C1 4 → 0 re-measured; three wrong Axes scores corrected; new uncounted
  residuals routed (R4) |". Latest admitted calibration-improved closure is 25
  (r26 cal=unchanged, r27 rejected, r28 cal=unchanged).
- Last change "round 25 (improved, score held)" — TRUE.

## 6. adjacency row (SCORECARD.md:15)
- "refuses dispatch (kumitate), OS state (tsukuroi) and harness configuration
  (operator) in PROVINCE and in its tools" — TRUE. PROVINCE.md:12-15 "**Refuses:**
  dispatch and orchestration mechanism (→ kumitate); OS package, systemd unit,
  driver/firmware and boot state (→ tsukuroi)"; harness configuration is operator-owned
  at PROVINCE.md:335-344 "the operator owns the configuration ... Changing harness
  configuration is operator-owned"; tool boundaries: mori-job-runway.py "never writes a
  settings file and never touches another configuration surface" (PROVINCE.md:314-316),
  mori-pressure.py read-only, no service/package change (PROVINCE.md:250-253).
- "latest admitted closure grading adjacency improved has no lane spot-check file:
  MANIFEST.json@63729047 mori round 19 (fleet MANIFEST.json rounds[398],
  verdicts.adjacency improved)" — TRUE. rounds[398] (mori, round 19, closure,
  admitted=true) verdicts.adjacency="improved"; its verification.spotcheck reads
  "Inline in this durable closure row; assignment forbids lane/report edits" (no lane
  spot-check file). Glob corpus/lessons/*verifier-spotcheck.md has no round-19 file
  (rounds 13-18,23-28 exist). Mori adj-improved admitted closures are only r14, r18,
  r19 → r19 is the latest.
- Last change "round 19 (improved, score held)" — TRUE (MANIFEST r19 admitted,
  adj=improved; score 6 held in every held line).

## 7. Round-25 correction paragraph (SCORECARD.md:17-19) — still accurate
- "until round 25 this table still showed the round-1 scores (coverage 5, operability
  6, depth 4) with 'round 1' in every row" — TRUE. At 28b79d3d (round-25 entering tip,
  :1540) `git show 28b79d3d:SCORECARD.md` lines 10-15 read coverage 5 / operability 6 /
  depth 4 / freshness 5 / calibration 5 / adjacency 6, all Last change "round 1".
- "while the round tables below held 6, 7 and 5" — TRUE. Round-24 section at
  28b79d3d:1501-1502 shows "calibration 5" and "coverage 6"; :1504 "Held and observed:
  operability 7, depth 5, freshness 5, adjacency 6".
- "The scores above are the ones the closure-admitted round-24 section records
  (`SCORECARD.md:1499-1506` at `28b79d3d`)" — TRUE. That section records calibration 5,
  coverage 6, operability 7, depth 5, freshness 5, adjacency 6 = the six current scores
  (6,7,5,5,5,6). Paragraph remains a correct description of the current table.
  (Related: the round-12 stale-pointer paragraph at :620-623 was already declared stale
  by R4c, :1690-1704, after the D5 rewrite.)

## 8. Stale text
- `## Planned` :27-30 — STALE. "Round 2: land one note per surface family and the
  first watch receipts, and add the `progressing-weak` authorship proof." Round 2
  completed (verdict at :101+): per-surface notes landed (7 sections, verified above),
  watch receipts landed (`corpus/evidence/watch-r2-20261015T15{2746,2855,3003}Z.log`,
  :115), authorship proof landed (`MORI_AUTHORSHIP_CHECK: matched=10 total=10` exit 0,
  :115). :44 already says "The following plan supersedes the broad round-2 paragraph
  under **Planned**".
- `## Saturation` :594-596 — STALE. "The lane's saturation line + stagnation window N
  are to be declared by the lane on its next round per `AXES.md` §The stagnation
  nudge; not asserted by this conformance change." Superseded by `## Saturation
  (declared round 12)` :637-641: "Saturation line: **8/10** on each owned axis
  (coverage, operability). Stagnation window **N = 3**".
- Informational (not in scope, already self-labeled historical): :98 "Next actual
  round remains **2**" inside the round-2 blocked-attempt section (superseded by the
  round-2 verdict heading, which marks the blocked attempt as "prior record", :101);
  :620-623 round-12 paragraph (declared stale by R4c, :1690-1704).

## 9. Residual risk / verification gaps
- Worktree at review time = tip 8809a3fe plus an uncommitted append of the Round 29
  declaration (:1777-1790; +15 lines). The six Axes rows at the tip are identical to
  the worktree rows reviewed. Rows 10-15 verified via `git show` bytes, not just the
  worktree read.
- "kept in every admitted round table since": verified against per-axis score tables
  for rounds 14-20, MANIFEST verdicts (op=unchanged) for r21/r22/r24, and held lines
  for rounds 24-29. Rounds 21-23 carry no per-axis score tables in SCORECARD, so the
  "table" part of the claim is unverifiable there (MANIFEST supports it).
- MANIFEST assertions are all at the pinned rev 63729047 as instructed. No external
  source was opened, so no URL/access-time/sha256 records apply.

Findings: no false statement found in the six evidence cells; the round-25 correction
paragraph still describes the table; stale text flagged in `## Planned` (:27-30) and
`## Saturation` (:594-596). No action taken (detection/report only).
