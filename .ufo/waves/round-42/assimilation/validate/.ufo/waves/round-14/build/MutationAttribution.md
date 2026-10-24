# MutationAttribution — round 14 audit of exact-locus F01/F02 wording

Owner: `MoriR14.MutationAttribution` (leaf, report-only). Axes: coverage (mention completeness), operability (F01/F02 status accuracy).
Scope: SKILL.md, corpus/knowledge/*, SCORECARD.md, LOG.md under `/home/vgpnk/Projects/shokunin/mori-shokunin`. No edits to those files, no builds, tests, selftests, or harness runs. Reads and greps only.

## Ground truth used

- Round-13 spotcheck (`corpus/lessons/round-13-verifier-spotcheck.md`, item 5): F01 "exact-locus" means a **whole frozen `grade_lane` transplant** (includes GIT_* env hardening and `core.fsmonitor=false`), not a membership-lines-only reversal. F02 means a **reconstructed prefix-presence shim** (`frozen_source=null`, `reverted_by=pre_fix_prefix_presence_shim`), not original `verdict_grade` bytes. Original-frozen before-runs (`regressions-before-final`) are the primary evidence of the historical defects.
- Mutation harness, current locations (read-only grep):
  - `tools/mori-round13-regressions.py:250` — `PRE_FIX_VERDICT_GRADE` reconstructed shim (R13 mutation).
  - `tools/mori-census.sh:1608` — `grade_lane()`; `:1712-1715` — comment describing the old F01 pipe.
  - `tools/mori-silence-cases.sh:594-595` — `VERDICT_RE` and `verdict_grade()` (fixed gate, working tree at c13df48 measurement).
- Accepted measurement at c13df48: census `39abda0a…`, oracle `34cd5770…`; `regressions-accepted` 19 pass + 2 mutation-red, exit 0. Frozen before-final: F01 row-C 12001, F02 BANANA 28/28 rc0.

## A. Misleading "exact-locus" / mutation-attribution mentions (current-state docs)

| # | File:line | Current text (quoted) | Problem | Recommended wording |
|---|---|---|---|---|
| A1 | `SCORECARD.md:679` (round-13 C2 claim row, evidence cell) | "2 exact-locus mutation-red witnesses" | Reads as original-byte reversion. F01 is a whole-function transplant; F02 is a reconstructed shim. | "2 function-locus mutation-red witnesses: whole frozen `grade_lane` transplant (F01) and reconstructed prefix-presence `verdict_grade` shim (F02, `frozen_source=null`); historical defect proof is the original-frozen before-final run." |
| A2 | `SCORECARD.md:684-685` (rubric for the operability point) | "both exact-locus negative witnesses reproduce the old failure" | Rubric condition is satisfied by transplant/shim, not by original-byte restoration. | "both function-locus mutation witnesses (F01 whole-`grade_lane` transplant; F02 reconstructed verdict shim) reproduce the old failure; the named defects themselves are shown by the original-frozen before-final receipts." |
| A3 | `corpus/knowledge/structured-journal-scopes-r13.md:86-87` (Measured round-13 receipt) | "2 exact-locus mutations reproduced the old defects" | Same misreading, in an active knowledge note. | "2 function-locus mutations (whole `grade_lane` transplant; reconstructed `verdict_grade` shim) reproduced the old defects; original-byte before evidence is `regressions-before-final`." |
| A4 | `corpus/knowledge/verdict-contract-r13.md:252` (Measured implementation, F01 bullet) | "Reverting only grade_lane reproduces row-C with 12,001 records." | "Reverting only" implies a membership-only reversal. The mutation swaps the whole frozen function, which also drops GIT_* env hardening and fsmonitor pin. | "Transplanting the whole frozen `grade_lane` (not a membership-only reversal; includes env hardening and `-c core.fsmonitor=false` changes) reproduces row-C with 12,001 records." |
| A5 | `corpus/knowledge/verdict-contract-r13.md:257` (F02 bullet) | "Reverting only verdict validation makes BANANA green 28/28 again." | Implies original `verdict_grade` bytes were restored. The mutant is a reconstructed prefix-presence shim. | "Replacing `verdict_grade` with a reconstructed prefix-presence shim (`frozen_source=null`; the old oracle had no such function) makes BANANA green 28/28 again; this proves single-locus sufficiency, not original-byte restoration." |
| A6 | `SKILL.md:128-132` (Round 13 verdict contract) | "This closes audit F02's demonstrated prefix-only acceptance … Production exact-author membership consumes captured history without an early-exiting producer pipe (audit F01)" | Accurate, but stated without the residual scope. Lane readers could take it as full F02/D01 closure. | Append: "…for the measured class (BANANA/missing/duplicate/rc-inconsistent rolls; a >pipe-capacity exact-author window). Tally corruption and aggregate vacuity (D02) and full adaptive forgery remain open." |

## B. Stale or superseded status statements (historical or append-only, need L1 appended correction, not rewrite)

| # | File:line | Current text | Problem | Recommended action |
|---|---|---|---|---|
| B1 | `corpus/knowledge/audit-r11.md:196` (D01) | "**open defect**, F01 …" | Status as of r11. Round 13 repaired the measured class (`verdict-contract-r13.md` §Measured; accepted row-A / row-C controls). | Append correction: "Round 13 c13df48: measured fixture class closed; production generalisation not claimed; see verdict-contract-r13 §Measured." |
| B2 | `corpus/knowledge/audit-r11.md:197` (D02) | "**open defect**, F02 …" | Partially closed: BANANA/roll-rc/duplicate/missing reject; tally corruption, aggregate vacuity and full adaptive forgery remain open. | Append correction: "D02 partially addressed at c13df48; residual tally/aggregate classes remain open." |
| B3 | `corpus/knowledge/audit-r11.md:156` (F01 row) | "Current `tools/mori-census.sh:1366-1374`" | Known stale pointer (MistakeScribe N11). Round-12 F01 site was `:1494`; current `grade_lane` is `:1608` and the old-pipe comment is `:1712-1715`. | Append pointer correction; do not rewrite the audit row. |
| B4 | `corpus/knowledge/audit-r11.md:243-245` (Top recommendation 1: "Select a future … round for F01 and F02") | Action item | Partly executed in round 13. | Append "executed in r13 for the measured classes; residuals D01 production generalisation and D02 tally class remain." |
| B5 | `corpus/knowledge/verdict-contract-r13.md:204-209` (§6 Pointer status) | "the same constructs sit at `:1490-1494` and `:570` after r12 edits" | Pre-C1 anchors. C1 added a probe block (spotcheck: census `:935-1128`), and F01 now sits at `grade_lane` `:1608` / comment `:1712`; F02 gate is `mori-silence-cases.sh:595`. Base-bound per its own provenance, but a current reader will mis-locate. | Append current anchors: census `grade_lane` `:1608`, F01 comment `:1712-1715`; oracle `verdict_grade` `:595` (working tree at measurement). |
| B6 | `SCORECARD.md:644-646` (Planned round 13, item 2: "close audit F01/F02") | Plan text | Historical plan; "close" now overstated. | Append note beside the plan: "Round-13 outcome: partially closed (see round-13 table; D02 residuals)." |
| B7 | `SCORECARD.md:720-721` (Round 13 trends: "quality improved (F01/F02 repairs…)") | "F01/F02 repairs" | Accurate for named classes; "repairs" without scope. | Append qualifier: "F01 repair verified on the measured fixture class; F02 repair closes the verdict channel only (`verdict-contract-r13` §Measured)." |
| B8 | `LOG.md:725` (Round 13 declared claims) | "close audit F01's long-history authorship loss and F02's invalid-verdict oracle acceptance" | Declared intent; already caveated at `LOG.md:744` ("D02 … not claimed closed"). The declaration alone reads as full closure. | Append correction block: "Declared claim was 'close'; measured outcome is partial closure for the named classes; residuals in LOG:744 and verdict-contract-r13 §Measured." Do not edit the declaration. |

## C. Mentions reviewed and found accurate (no action)

- `SCORECARD.md:678`, `SCORECARD.md:690-692` — "demonstrated named defects 2→0", "BANANA 28/28→0/28" — backed by original-frozen before-final evidence.
- `LOG.md:744` — "Subject-first history is progressing; sibling control remains progressing-weak; … D02 … not claimed closed." Accurate and already qualified.
- `verdict-contract-r13.md:253-256` — F02 rc/cardinality proxy counts (7/28, 21/28) and "not asserted to reject every unaffected case." Accurate.
- `verdict-contract-r13.md:258-262` — residual list including D02 partial. Accurate.
- `audit-r11.md:157` — F02 row (vocabulary-only BANANA proof). Accurate as an audit-time finding.

## D. Out-of-scope occurrences (outside SKILL/knowledge/score/LOG; for L1 awareness only, not edited)

- `.ufo/waves/round-13/build/RegressionHarness.md:152` — "exact-locus reverts" (same misreading as A1–A3).
- `.ufo/waves/round-13/build/CountDesign.md:308-309` — "frozen `grade_lane` is transplanted" (accurate).
- `tools/mori-round13-regressions.py:249-250` — comment "Used only to build an isolated mutant" (accurate; the shim is named `PRE_FIX_VERDICT_GRADE`).
- `corpus/lessons/round-13-verifier-spotcheck.md` item 5 — the authoritative wording requirement this audit implements.

## E. Counts

- "exact-locus" occurrences in scope: 3 (SCORECARD:679, SCORECARD:685, structured-journal-scopes-r13:87). Plus 2 `exact-locus`-equivalent "reverting"/"reverting only" phrasings (verdict-contract-r13:252, :257).
- Misleading-as-written active statements requiring editable correction: A1–A6 (6).
- Stale/superseded historical statements requiring appended correction: B1–B8 (8).

## F. Notes and limits

- Anchors were read at the working tree during the audit; the census and oracle are in-flight in the wave, so line numbers may move before L1 integrates. L1 should re-resolve anchors at the final SHA.
- I did not verify the mutation or shim behaviour; wording above relies on the round-13 spotcheck and the harness source comments.
- Tooling: none installed or updated.
- Checks run by main agent: none run by this seat.
