# AxisCalibration — C1 `calibration` row draft (round 29, wave 1)

Seat: `MoriR29.AxisCalibration`. Lane tip read: `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`. Fleet pin for
closure record: `63729047644f839fe4c8cc97abd0d8bf741a5787`. No tool installs; nothing written outside this file.
I did not open, grep or run `tools/mori-oom-killers.py`, and I read no round-26/27/28 w1 or w2 report.

Reading rule used for the spot-check column: only a per-axis table line `| calibration | <verdict> | ... |` counts
as the closure's calibration verdict (the counter spec, `.ufo/waves/round-29/wave1-spec.json` items[8], restricts
matching to `| <axis> | <verdict> |` with verdict in improved/unchanged/harmed/unprovable-but-better). Narrative
sentences that mention calibration are listed but do not qualify as a per-axis line.

## 1. Round table, 12–28 (mori entries only, `git show 63729047:MANIFEST.json`)

`rounds[N]` below is the 0-based index in the pinned MANIFEST `rounds` array (cross-check: the round-22 mori entry
is `rounds[427]`, which `SCORECARD.md:1420` itself cites).

| round | MANIFEST verdict (calibration sub-verdict) | spot-check calibration line (verbatim, path:line at 7118f320) | score number stated by closure/declaration (path:line) |
|---|---|---|---|
| 12 | `rounds[313]` verdict `admitted`, calibration `improved` | narrative only, no per-axis line: `corpus/lessons/round-12-verifier-spotcheck.md:17` "calibration improved under campaign binding (26 mined mistake classes; 20 grounded criteria), score held 5 because the outside reviewer could not derive 6" | declaration `SCORECARD.md:614` "\| calibration \| **improved** \| 5 → 6 \|"; withdrawn by `SCORECARD.md:658` "scalar score **held at 5**, not 6, because the non-author reviewer could not re-derive 6" |
| 13 | `rounds[327]` `rejected-harmed`, `unchanged` | `corpus/lessons/round-13-verifier-spotcheck.md:99` "\| calibration \| unchanged \| No separate calibrated improvement is established. ... no extra scalar credit is earned. \|" | none |
| 14 | `rounds[339]` `admitted`, `unchanged` | `corpus/lessons/round-14-verifier-spotcheck.md:95` "\| calibration \| unchanged \| bounded claims, fixture/live separation and historical corrections; no scalar or outside self-credit \|" | `SCORECARD.md:87` lists "calibration5" among held scores |
| 15 | `rounds[345]` `admitted`, `unchanged` | `corpus/lessons/round-15-verifier-spotcheck.md:181` "\| calibration \| unchanged \| fixture/live and subset/total boundaries explicit; procedural and wording debt remain, no universal or score-increase claim \|" | none |
| 16 | `rounds[353]` `admitted`, `unchanged` | `corpus/lessons/round-16-verifier-spotcheck.md:132` "\| calibration \| unchanged \| ... No score increase. \|" | none |
| 17 | `rounds[372]` `rejected-harmed`, `improved` | `corpus/lessons/round-17-verifier-spotcheck.md:236` "\| calibration \| improved \| Exact externally identified C3 witness, 1→0; honest failed runs and historical red retained. ... \|" | `SCORECARD.md:1118` "\| calibration \| improved \| 5 held \| ..."; not admitted, so no basis |
| 18 | `rounds[386]` `admitted`, `improved` | `corpus/lessons/round-18-verifier-spotcheck.md:125` "\| calibration \| improved \| r17-C3 overclaim corrected by appended row; r18 claims pre-build; 4→0 reproduced from committed evidence \|" | `SCORECARD.md:1150` "\| calibration \| improved narrowly \| 5 held \| \|" |
| 19 | `rounds[398]` `admitted`, `improved` | **no spot-check file at 7118f320** | `SCORECARD.md:1218` "\| calibration \| 5 \| improved \| C2 exact input/script/revision receipts and actual before counter ... \|" |
| 20 | `rounds[405]` `rejected-harmed`, `harmed` | **no spot-check file at 7118f320** | declaration `SCORECARD.md:1261` "\| calibration \| unchanged \| 5 held \| ... \|"; closure graded `harmed` (conflict noted in §4) |
| 21 | `rounds[412]` `admitted`, `improved` | **no spot-check file at 7118f320** | `SCORECARD.md:1321` "... \| calibration5→5 held \| frozen synthetic mismatches2→0 of6 ... \| improved bounded calibration ..." |
| 22 | `rounds[427]` `admitted`, `improved` | **no spot-check file at 7118f320** | `SCORECARD.md:1359` "One C1 **calibration capability**, score5→5 held"; `SCORECARD.md:1386` "... \| calibration5→5 held \| frozen24 capability_absent24→0 ... \|" |
| 23 | `rounds[432]` `rejected-honest-stop`, `improved` | `corpus/lessons/round-23-verifier-spotcheck.md:24` row is "\| C1 calibration \| ... \| **Improved, bounded; evidence-verified, not rerun.** ... \|" — first cell is not the bare axis name, so not a per-axis line | `SCORECARD.md:1438` "... calibration5→5; supplementary guards are separate evidence ..." |
| 24 | `rounds[443]` `admitted`, `improved` | `corpus/lessons/round-24-verifier-spotcheck.md:104` "\| calibration \| improved \| C1 above (R4 8 → 0 mismatches; R1–R3 held) \|"; the closure sentence `:68` ends "Score 5 → 5." | `SCORECARD.md:1517` "... \| improved, bounded: ... calibration 5 → 5 \|" |
| 25 | `rounds[455]` `admitted`, `improved` | `corpus/lessons/round-25-verifier-spotcheck.md:124` "\| calibration \| improved \| C1 4 → 0 re-measured; three wrong Axes scores corrected; new uncounted residuals routed (R4) \|" | `SCORECARD.md:1555` "... calibration 5 → 5 pending closure \|" |
| 26 | `rounds[462]` `admitted`, `unchanged` | `corpus/lessons/round-26-verifier-spotcheck.md:136` "\| calibration \| unchanged \| held; no calibration claim \|" | `SCORECARD.md:1600` "Held and observed: operability 7, depth 5, calibration 5, adjacency 6." |
| 27 | `rounds[468]` `rejected-honest-stop`, `unchanged` | `corpus/lessons/round-27-verifier-spotcheck.md:106` "\| calibration \| unchanged \| no claim \|" | `SCORECARD.md:1729` "Held and observed: freshness 5, calibration 5, coverage 6, adjacency 6." |
| 28 | `rounds[476]` `admitted`, `unchanged` | `corpus/lessons/round-28-verifier-spotcheck.md:95` "\| calibration \| unchanged \| held, no claim \|" | `SCORECARD.md:1758` "Held and observed: depth 5, calibration 5, coverage 6, adjacency 6." |

Rounds with no `corpus/lessons/round-N-verifier-spotcheck.md` at 7118f320: **19, 20, 21, 22** (verified with
`git ls-tree -r --name-only 7118f320 corpus/lessons/`, which lists spot-check files for 12–18 and 23–28 only).
Additional trap found: the round-12 file exists but is 17 lines of narrative with **no per-axis table at all**
(`git show 7118f320:corpus/lessons/round-12-verifier-spotcheck.md | wc -l` → `17`; grep for `^\| *calibration *\|`
returns nothing), so round 12 cannot satisfy mismatch kind 1's table-line condition despite being admitted with
`improved`.

No admitted closure in 12–28 states a calibration score other than 5: round 12's declaration proposed 6
(`SCORECARD.md:614`) and its own post-review correction withdrew it (`SCORECARD.md:658`), and every later admitted
calibration round is explicit `5 held` / `5 → 5` (`SCORECARD.md:1150`, `:1218`, `:1321`, `:1359`, `:1386`, `:1517`,
`:1555`).

## 2. R

**R = 25.** Largest N in 12–28 with MANIFEST `admitted` and a per-axis line `| calibration | improved |`:
candidates 12 (no table line), 18, 19 (no file), 21 (no file), 22 (no file), 24, 25 → largest = 25
(`corpus/lessons/round-25-verifier-spotcheck.md:124`). R is robust to the stricter table-line condition: using
MANIFEST verdicts alone the admitted-and-improved set is {12, 18, 19, 21, 22, 24, 25}, whose maximum is still 25.

## 3. Replacement row (ready to paste)

Exact column shape kept; score held at 5; pointer moved to the round-25 closure.

```markdown
| calibration | 5 | improved (closure round 25), score held; round-25 spot-check grades calibration improved (`corpus/lessons/round-25-verifier-spotcheck.md:124`); round-24 closure "Score 5 → 5" (`corpus/lessons/round-24-verifier-spotcheck.md:68`); the round-12 post-review correction held the score at 5, not 6, because the non-author reviewer could not re-derive 6 (`SCORECARD.md:658`) | round 1 |
```

Pointer receipts, run against the lane (`git show 7118f320:<path> | wc -l`):

```
corpus/lessons/round-25-verifier-spotcheck.md  210 lines  (need 124)  OK
corpus/lessons/round-24-verifier-spotcheck.md  148 lines  (need 68)   OK
SCORECARD.md                                  1775 lines  (need 658)  OK
```

Local simulation of the counter's parse on this exact row (stdlib python, no files written): 4 cells; three
backticked tokens, all `path:L`, all resolving; the row contains the string `round-25-verifier-spotcheck.md`; the
`Last change` cell opens with `round 1`. Kinds 1–3 therefore read clean on the draft, and kind 4 cannot fire because
the score equals the 7118f320 baseline (5). **The counter itself is not written yet** — `.ufo/waves/round-29/`
holds `contract.md`, `evidence/`, `w1/`, `wave1-dispatch.json`, `wave1-run.json`, `wave1-spec.json`, and no
`count-c1.sh` — so `mismatches=0 / C1=met` is **unrun and not a pass**; this row is a reading-level draft only.

## 4. Judgement calls (honest notes)

1. **Round 12 is the one place the score policy's second clause could be read as licensing 6.** The clause allows a
   change where "the admitted round's declaration proposed it and its closure verdict is `improved`". Round 12's
   declaration did propose 5 → 6 (`SCORECARD.md:614`), the MANIFEST entry is `admitted` with calibration `improved`
   (`rounds[313]`), and the round-12 spot-check is `improved` on calibration. I still hold 5, because the same
   admitted closure record withdraws the number: `corpus/lessons/round-12-verifier-spotcheck.md:17` says "score held
   5 because the outside reviewer could not derive 6" and `SCORECARD.md:658` says "scalar score **held at 5**, not
   6". The sub-verdict `improved` is the verdict; 6 was the proposal and was explicitly not carried. Raising to 6
   would put the row in conflict with the closure record, which is what C1 exists to prevent. Note the hole this
   exposes: the counter's kind 4 only asks whether *some* admitted improved round is cited, so a 6 in this row would
   pass the counter while overclaiming — worth a routed item, not a counter change made by me.
2. **`Last change` kept as `round 1`.** No round after round 1 changed the calibration number, and the round-25
   correction explicitly treats the round-1 scores as the base it repaired (`SCORECARD.md:17-19`, `:1555`). Mismatch
   kind 2 only constrains N ≥ 12, so `round 1` passes; writing `round 25` would also pass kinds 1–2 but would read as
   a score move that did not happen. I recommend `round 1`.
3. **Round 20 contradicts itself across sources and is rejected anyway.** The declaration table says calibration
   `unchanged, 5 held` (`SCORECARD.md:1261`) while the closure sub-verdict is `harmed` (`rounds[405]`). Recorded so
   the L1 does not read agreement where there is none; it cannot affect R because round 20 is not admitted.
4. **Round 12 table absence is a closure-record gap, not a lane defect.** I did not treat the narrative sentence as
   a per-axis line; if the L1's counter is laxer (substring "improved" near "calibration" in the whole file), round
   12 still loses to 25, so the chosen R does not depend on this reading.
5. **Score-cell shape.** I left the score cell as a bare `5` to match the other five rows; the history lives in the
   evidence cell per the contract's "score held" wording.
6. **Out of scope, untouched:** I did not edit `SCORECARD.md`, the counter, fixtures, or any tool; I ran no git or
   jj writes, no unit or process commands, and installed nothing.

## 5. Commands actually run (read-only)

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7118f320:SCORECARD.md | sed -n '1,40p'
git -C /home/vgpnk/Projects/shokunin show 63729047:MANIFEST.json   # parsed with python3 json, lane=="mori"
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7118f320:<spotcheck> | nl -ba   # per-round lines
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only 7118f320 corpus/lessons/
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7118f320:<path> | wc -l          # pointer receipts
```

Env hygiene: all lane git calls ran with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`; read-only verbs only.
