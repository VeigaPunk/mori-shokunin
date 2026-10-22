# ReviewAxesPointers — C1 input screen before counter freeze (wave 1, round 29)

Seat: MoriR29.ReviewAxesPointers (reviewer, leaf). Read-only git at the pinned revisions; no lane, fleet or
counter writes; the oom-killers tool was never opened and no round-26/27/28 w1 or w2 report was read.
Screening axes: pointer validity, citation truth, closure agreement (Last change vs MANIFEST), record coverage
(spot-check files 12-28), and parse safety of the inputs the C1 counter will read. No tooling was installed
(git and jq already present sufficed); nothing to record under the tooling directive.

Revisions: lane tip `7118f320` (entering tip per contract), fleet `63729047` (pinned MANIFEST). All line
numbers below are at those revisions. The C1 counter (`.ufo/waves/round-29/count-c1.sh`) did not exist in the
working tree at screen time (`ls` returned "No such file"), so every statement about what the counter will do
is from the round-29 contract kind 1-4 text and is marked [INFERENCE] where implementation could differ.

## 1. Six-row pointer screen (SCORECARD.md:10-15 at 7118f320)

Every backticked pointer in the `## Axes` rows; kind-3 tokens are those with a `:L` suffix.

| Row (path:line) | Backticked pointer | Resolves | Cited line says what the row claims |
|---|---|---|---|
| coverage (SCORECARD.md:10) | `corpus/knowledge/observability-surfaces-r2.md` (no `:L`) | yes, 395 lines | n/a (no line cited) |
| coverage (SCORECARD.md:10) | `corpus/lessons/round-24-verifier-spotcheck.md:88` | yes, file has 148 lines | yes — line 88: "Ruling: improved, bounded. The declared after-value holds as declared. ... Score 6 → 6." |
| operability (SCORECARD.md:11) | `SCORECARD.md` (self, no `:L`) | yes, 1775 lines | n/a |
| depth (SCORECARD.md:12) | none | — | — |
| freshness (SCORECARD.md:13) | `corpus/README.md` (no `:L`) | yes, 524 lines | content supports the claim — :406 "## Round21 correction — loss accounting before baseline acceptance", :408 "The round20 drift re-pin coverage-map row is historical, not an acceptance", :428 "the invalid r20 baseline is not accepted or re-pinned"; :367 "R10 drift pin remains red debt without a re-pin" |
| calibration (SCORECARD.md:14) | `corpus/lessons/round-24-verifier-spotcheck.md:68` | yes, file has 148 lines | yes — line 68 ends: "... clauses of routed item 4 are unchecked, as disclosed. Score 5 → 5." |
| adjacency (SCORECARD.md:15) | none | — | — |

No dead kind-3 pointer exists today. Both `:L` citations quote truthfully.

## 2. Last change cells vs pinned MANIFEST verdicts

| Row | Last change cell | Cell round admitted in MANIFEST? | MANIFEST per-axis verdict at that round |
|---|---|---|---|
| coverage :10 | round 12 (5 → 6) | yes | coverage "improved" — consistent |
| operability :11 | round 14 (6 → 7; r13's 7 not held) | yes | operability "unchanged" — see F5 |
| depth :12 | round 12 (4 → 5) | yes | depth "improved" — consistent |
| freshness :13 | round 1 | N < 12: kind 2 does not check | no per-axis verdicts exist for r1 |
| calibration :14 | round 1 | N < 12: kind 2 does not check | no per-axis verdicts exist for r1 |
| adjacency :15 | round 1 | N < 12: kind 2 does not check | no per-axis verdicts exist for r1 |

All kind-2 checks pass at `7118f320`. The freshness/calibration/adjacency "round 1" cells are factually stale
against the record (MANIFEST: freshness improved in admitted 21/26/28, calibration in 12/18/19/21/22/24/25,
adjacency in 14/18/19), which kind 1 is supposed to catch — see §4 for where it will and will not.

## 3. Closure inputs: spot-check files for rounds 12-28 at 7118f320

Exist: 12, 13, 14, 15, 16, 17, 18, 23, 24, 25, 26, 27, 28. Missing: **19, 21, 22**. Whole-tree
`git ls-tree -r | grep -i spotcheck` finds no other copy under corpus/lessons; the only r19-shaped artifact is
`.ufo/waves/round-20/build/SpotcheckR19.md` (106 lines, a routed-debt disposition review with **no per-axis
table**), never landed at the canonical path.

Per-axis verdict lines (`| <axis> | <verdict> | ...`), path:line at 7118f320:

| File | Lines | Verdicts found | All six axes? | Format ok? |
|---|---|---|---|---|
| round-12-verifier-spotcheck.md | 17 lines total | none — prose only (:17: "Depth improved ... calibration improved ... coverage improved ... Operability/freshness/adjacency unchanged") | no table | **NO** — admitted round, no table (F2) |
| round-13-verifier-spotcheck.md | :95-100 | coverage harmed, operability improved, depth/freshness/calibration unchanged, adjacency harmed | yes | yes (round not admitted) |
| round-14-verifier-spotcheck.md | :91-96 | coverage improved, adjacency improved, rest unchanged | yes | yes |
| round-15-verifier-spotcheck.md | :177-182 | coverage improved, rest unchanged | yes | yes |
| round-16-verifier-spotcheck.md | :128-133 | coverage improved, rest unchanged | yes | yes |
| round-17-verifier-spotcheck.md | :234-239 | coverage improved, operability improved, calibration improved, depth/freshness unchanged, adjacency `**harmed**` | yes | **NO** — bolded verdict :239 (F4) |
| round-18-verifier-spotcheck.md | :124-129 | adjacency improved, calibration improved, operability improved, depth/coverage/freshness unchanged | yes | yes |
| round-23-verifier-spotcheck.md | :22-26 | 3-column table, verdicts embedded in prose ("Improved, bounded", "Unprovable, not admitted", "unchanged within the checked boundary") | no `| axis \| verdict \|` shape | **NO** (round not admitted; F4) |
| round-24-verifier-spotcheck.md | :104-109 | calibration improved, coverage improved, rest unchanged | yes | yes |
| round-25-verifier-spotcheck.md | :124-129 | calibration improved, coverage improved, rest unchanged | yes | yes |
| round-26-verifier-spotcheck.md | :132-137 | freshness improved, coverage improved, rest unchanged | yes | **NO** — stray second `| operability |` row at :125 from the "No-harm checks" table (:121-126), before the real table at :128 (F3) |
| round-27-verifier-spotcheck.md | :102-107 | depth improved (round rejected-honest-stop, so inert), rest unchanged | yes | yes |
| round-28-verifier-spotcheck.md | :92-97 | freshness improved, operability improved, rest unchanged | yes | yes |

MANIFEST cross-notes: the round-28 entry pins this exact spot-check blob
("mori-shokunin/corpus/lessons/round-28-verifier-spotcheck.md@7118f320a5ef…"), so file and record agree at the
tip. MANIFEST round 23 uses verdict vocabulary "unprovable" (coverage) where the counter vocabulary is
"unprovable-but-better" — divergent naming inside the closure record itself (round 23 is not admitted, so
inert today).

## 4. Blind spots and consequences

R per axis under the contract kind-1 algorithm ([INFERENCE] — algorithm as contracted, counter not yet
landed): largest admitted round N in 12-28 whose spot-check file holds `| <axis> | improved |`.

| Axis | Counter-visible R | Record-true R (MANIFEST admitted + verdicts[axis]="improved") | Divergence |
|---|---|---|---|
| coverage | 25 (:125) | 25 | none |
| operability | 28 (:93) | 28 | none |
| depth | none (round 12 admitted-improved but file has no table) | 12 | kind 1 vacuous for depth |
| freshness | 28 (:92) | 28 | none |
| calibration | 25 (:124) | 25 | none |
| adjacency | 18 (:124 of round-18 file) | 19 | **counter directs the fix at the wrong closure** |

- **B1 (stale row can pass): adjacency.** MANIFEST round 19 is admitted with adjacency "improved"; no
  spot-check file exists for 19, so the counter's R falls back to 18. The C1 fix will add a citation of
  `round-18-verifier-spotcheck.md` to the adjacency row and the counter will print `mismatches=0` while the
  table still does not reflect the record's latest admitted adjacency improvement. This is exactly the
  "admitted round with no spot-check file lets a stale row pass" case, and it fires today, not hypothetically.
- **B2 (no protection): depth.** The only admitted depth improvement (round 12) is invisible because its file
  is prose-only. Kind 1 never fires for depth, so a stale depth row would pass at any future tip within the
  12-28 window. Today's depth row happens to be current (12 is the record-true R), so no falsehood yet.
- **B3 (latent): rounds 21 and 22.** Admitted improvements (freshness+calibration at 21, calibration at 22)
  are invisible, but later file-bearing rounds (26/28 freshness, 24/25 calibration) dominate every axis they
  touched, so no row can currently pass on their account.
- **B4 (parse hazard): round-26 :125.** A first-match parser over `^\| operability \|` hits the no-harm row
  whose second cell is "committed `w2/OperabilityNoHarm.md`", not a verdict. A vocabulary check on cell 2
  disambiguates; a bare first-match does not.
- **B5 (inert format deviations): round-17 :239 `**harmed**`** and round-23's 3-column prose table. Both
  rounds are non-admitted, so kind 1 never reads them; they matter only if the counter well-formality-scans
  all 13 files and exits 2 on a deviation.

## 5. Findings and smallest corrections

| # | Severity | Finding | Evidence | Smallest correction |
|---|---|---|---|---|
| F1 | HIGH | Admitted rounds 19/21/22 have no spot-check file; counter kind 1 is file-line-based, so record-true R is unreachable for adjacency (19) and silently older for calibration/freshness histories | MANIFEST rounds 19/21/22 (lane mori, admitted, verdicts above); §3 file list | Contract+counter: derive R from the pinned MANIFEST (admitted ∧ verdicts[axis]=="improved", max N in 12-28); require the row to cite `round-R-verifier-spotcheck.md` only when that file exists at rev with the `| <axis> | improved |` line, otherwise require the row to name `round R` as a plain token in its cells. No new lesson files are written into closed rounds |
| F2 | HIGH | Admitted round 12's spot-check file has no per-axis table (prose verdicts at :17), leaving kind 1 vacuous for depth | round-12-verifier-spotcheck.md:17 (file is 17 lines) | Same fix as F1 — MANIFEST-derived R makes the missing table non-load-bearing while keeping the citation duty resolvable |
| F3 | MEDIUM | Round-26 file carries a second `| operability |` row (:125) in a different table before the verdict table (:128-137); a naive first-match parser reads a non-verdict cell | round-26-verifier-spotcheck.md:121-137 | Counter: accept a per-axis line only when cell 2 is exactly one of improved/unchanged/harmed/unprovable-but-better (and treat two conflicting cell-2-valid rows for one axis as malformed input, exit 2) |
| F4 | LOW | Bolded verdict `**harmed**` (:239 of round-17) and round-23's prose table deviate from the contracted line shape; MANIFEST round 23 also says "unprovable" not "unprovable-but-better" | §3 rows for 17 and 23 | Counter validates only files of admitted rounds; non-admitted files are out of scope for kind 1 and must not trip a global well-formedness scan |
| F5 | INFO | Operability's Last change names round 14, which is admitted, but MANIFEST round-14 verdicts.operability is "unchanged"; the admitted per-axis improved basis for the standing 7 is round 18 (round-18 file :126) and round 28 (:93). Kind 2 checks admission only, so nothing fires; the round-26 spot-check :126 shows the "first admitted in round 14" phrasing was itself a routed r26 correction | MANIFEST round 14; round-14-verifier-spotcheck.md:92; round-26-verifier-spotcheck.md:126 | None needed for the counter; the contract's score policy already governs future score cells. Record nuance only |
| F6 | INFO | Hygiene in a cited input: corpus/README.md:410 reads "QUALITY69 now supersedes67." (run-together words) inside the Round21 correction the freshness row leans on; the meaning survives | corpus/README.md:410 | Optional QUALITY note; not a counter input defect |

Direct answers to the two assigned questions: (a) files whose per-axis table does not use the contracted
shape — round-12 (no table, admitted: material via F2), round-23 (prose table), round-17 (bolded verdict),
round-26 (extra stray row); (b) admitted rounds with no spot-check file — 19, 21, 22, and yes, the blind spot
is real and live for adjacency (B1), vacuous-but-open for depth (B2), latent for 21/22 (B3).

## 6. Residual risk and verification gaps

- The counter is not landed; all kind-1..4 outcomes are derived from the contract text, not an executable
  [INFERENCE]. BuildCountC1 should re-run this screen against the frozen script (the §4 table is the expected
  result at `7118f320`).
- Heading text (`## Per-axis verdicts`) was verified only in round-26 (:128); the §5 F3 correction therefore
  anchors on cell-2 vocabulary, not headings.
- I did not open `.ufo/waves/round-21|22/evidence/source-spotcheck.json`; their names suggest SOURCES
  verification, not per-axis closure verdicts, and no per-axis verifier file exists for 21/22 in corpus/lessons.
- Bounds honored: no oom-killers tool path opened or run; no round-26/27/28 w1/w2 report opened; no installs;
  read-only git only, with inherited GIT_* env unset.
