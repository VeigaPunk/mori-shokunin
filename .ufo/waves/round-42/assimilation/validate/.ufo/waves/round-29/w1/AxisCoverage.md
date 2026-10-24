# AxisCoverage — round 29 wave 1: `coverage` row evidence and draft

Seat: MoriR29.AxisCoverage (leaf, no subagents). Lane repo at `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Read only: `.ufo/waves/round-29/contract.md` (C1 + score policy), `SCORECARD.md` at `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`,
fleet `MANIFEST.json` at `63729047`, and `corpus/lessons/round-N-verifier-spotcheck.md` for N=12..28.
Never opened, grepped or ran `tools/mori-oom-killers.py`; opened no round-26/27/28 w1/w2 report. No installs.

## 1. Round-by-round record (mori, 12–28)

MANIFEST column from `git -C /home/vgpnk/Projects/shokunin show 63729047:MANIFEST.json`, entries with
`lane: mori`, `type: closure` (one per round; indices 313..476). Spot-check lines are quoted verbatim from
`7118f320`; `\|` is an escaped pipe inside a quoted table row, all other characters are as written.

| Round | MANIFEST verdict | spot-check coverage line (verbatim, path:line) | score number stated (path:line) |
|---|---|---|---|
| 12 | admitted | no per-axis table in the file; prose clause `corpus/lessons/round-12-verifier-spotcheck.md:17`: "coverage improved (silence grading 9→23 lanes, conf read textually plus driver counters; selftest 66→77, oracle 28/28)" | `SCORECARD.md:615`: `\| coverage \| **improved** \| 5 → 6 \| claim 3; 14 lanes graded that were invisible (incl. mori itself) \|` |
| 13 | rejected-harmed | `corpus/lessons/round-13-verifier-spotcheck.md:95`: `\| coverage \| harmed \| Explicit scoped surfaces 0→2, five fixture checks and accurate all-zero live 12/12 comparison verify a bounded gain, but OOM alert coverage and the fleet-unit distinction are lost. The capability cutover is a trade, not a pure coverage improvement. \|` | declaration proposed `SCORECARD.md:695`: `\| coverage \| improved \| **6 → 7** \|`; withdrawn at `SCORECARD.md:743`: "The unrestricted coverage point is withdrawn: active coverage **6**, not 7." |
| 14 | admitted | `corpus/lessons/round-14-verifier-spotcheck.md:91`: `\| coverage \| improved \| C1 six selected arms 6→0, raw scoped gains retained, unknown-subject classification explicit \|` | `SCORECARD.md:792`: `\| coverage \| improved \| **6 held** \|` |
| 15 | admitted | `corpus/lessons/round-15-verifier-spotcheck.md:177`: `\| coverage \| improved \| C1 finite mixed-invalid alarm failures34→0, raw-total unavailability preserved; owned score6 held \|` | `SCORECARD.md:874`: `\| coverage \| improved \| **6 held** \|` |
| 16 | admitted | `corpus/lessons/round-16-verifier-spotcheck.md:128`: `\| coverage \| improved \| Re-measured 64→0 unmet. A new exact-anchor, anchor-boot window capability. Live 2/2 OK at anchor-only scope. Score 6 held. \|` | `SCORECARD.md:983`: `\| coverage \| improved \| 6 held \|` |
| 17 | rejected-harmed | `corpus/lessons/round-17-verifier-spotcheck.md:234`: `\| coverage \| improved \| New bounded C1 capability; 66/66 receipt and real metadata-only observation, not universal transcript coverage. \|` | `SCORECARD.md:1116`: `\| coverage \| improved \| 6 held \|` |
| 18 | admitted | `corpus/lessons/round-18-verifier-spotcheck.md:128`: `\| coverage \| unchanged \| no coverage-map row added; no new-surface claim \|` | `SCORECARD.md:1152`: `\| coverage, depth, freshness \| unchanged \| 6/5/5 held \|` |
| 19 | admitted | no spot-check file at `7118f320` | `SCORECARD.md:1219`: `\| coverage \| 6 \| unchanged \| retrospective index repair, no newly covered observability ground \|` |
| 20 | rejected-harmed | no spot-check file at `7118f320` | `SCORECARD.md:1259`: `\| coverage \| improved \| 6 held \| per-seat settlement over 21 lanes / 196 dispatch files; FR3 partially to Core; dispatch authenticity and hygiene stay Frontier \|` |
| 21 | admitted | no spot-check file at `7118f320` | `SCORECARD.md:1303`: "Other active scores coverage6, operability7,"; `SCORECARD.md:1343`: "Other axes coverage6/operability7/depth5/adjacency6 unchanged." |
| 22 | admitted | no spot-check file at `7118f320` | `SCORECARD.md:1361`: "scores held coverage6/operability7/depth5/freshness5/adjacency6."; `SCORECARD.md:1409`: "Other axes coverage6/operability7/depth5/freshness5/adjacency6 unchanged." |
| 23 | rejected-honest-stop | no axis row; claim row opens `corpus/lessons/round-23-verifier-spotcheck.md:25` with the label `C2 coverage / FR2 capability` and rules "**Unprovable, not admitted.**" (full row at that line) | `SCORECARD.md:1439`: "... current capability absent, strict target unprovable/not admitted; coverage6→6, no Core/repertoire advance" |
| 24 | admitted | `corpus/lessons/round-24-verifier-spotcheck.md:105`: `\| coverage \| improved \| C2 above \|` | `SCORECARD.md:1518`: "improved: capability demonstrated; coverage 6 → 6 pending closure"; closure `corpus/lessons/round-24-verifier-spotcheck.md:88`: "Score 6 → 6." |
| 25 | admitted | `corpus/lessons/round-25-verifier-spotcheck.md:125`: `\| coverage \| improved \| C2 capability shown running; FR15 new ground; bounded to block-style single-file configs (R1, R2) \|` | `SCORECARD.md:1556`: "coverage 6 → 6 pending closure" |
| 26 | admitted | `corpus/lessons/round-26-verifier-spotcheck.md:133`: `\| coverage \| improved \| C2 capability evidence-verified, before and freeze re-measured \|` | `SCORECARD.md:1609`: "coverage 6 → 6 held pending closure"; closure `corpus/lessons/round-26-verifier-spotcheck.md:126`: "the round-26 sections hold freshness 5 → 5 and coverage 6 → 6 pending closure" |
| 27 | rejected-honest-stop | `corpus/lessons/round-27-verifier-spotcheck.md:104`: `\| coverage \| unchanged \| no tool or case change \|` | `SCORECARD.md:1729`: "Held and observed: freshness 5, calibration 5, coverage 6, adjacency 6." |
| 28 | admitted | `corpus/lessons/round-28-verifier-spotcheck.md:96`: `\| coverage \| unchanged \| held, no claim \|` | `SCORECARD.md:1744`: "Held: freshness 5, calibration 5, coverage 6, operability 7, adjacency 6." |

Rounds with **no** spot-check file at `7118f320` (confirmed by `git ls-tree --name-only 7118f320 corpus/lessons/`):
**19, 20, 21, 22**. Files exist for 12–18 and 23–28.

Score numbers stated by an admitted closure or its declaration across 12–28: 5→6 (round 12, `SCORECARD.md:615`),
6→7 proposed then withdrawn (round 13, `SCORECARD.md:695`, `SCORECARD.md:743`), and 6 held by every later one
(`SCORECARD.md:792`, `:874`, `:983`, `:1116`, `:1259`, `:1518`, `:1556`, `:1609`;
`corpus/lessons/round-24-verifier-spotcheck.md:88`).
No admitted closure and no declaration inside an admitted round states any number above 6 after round 12.

## 2. R = 26

Contract kind 1 requires both (a) pinned MANIFEST `admitted` and (b) the lane file holding a per-axis table line
`| coverage | improved |`. Admitted rounds with that line: 14 (`:91`), 15 (`:177`), 16 (`:128`), 24 (`:105`),
25 (`:125`), 26 (`:133`). Excluded: 17 has the line (`:234`) but MANIFEST says `rejected-harmed`; 12 has prose
only (`:17`, 17-line file, decision table only, no axis table); 20 declares `improved`
(`SCORECARD.md:1259`) but has no spot-check file; 23 has no axis row and was `rejected-honest-stop`;
27/28 read `unchanged`. **R = 26.**

## 3. Replacement row (ready to paste, replaces `SCORECARD.md:10` at `7118f320`)

```markdown
| coverage | 6 | per-surface notes landed (`corpus/knowledge/observability-surfaces-r2.md`); silence roster over the declared lanes (round 12); one-shot system pressure read (round 24); improved (closure round 26), score held (`corpus/lessons/round-26-verifier-spotcheck.md:133`; round-24 closure "Score 6 → 6" `corpus/lessons/round-24-verifier-spotcheck.md:88`; `SCORECARD.md:1609`) | round 12 (5 → 6; round 13's self-assessed 7 was not held) |
```

Score stays 6: kind 4 needs an admitted closure stating a new number; only 6→6 is stated (rounds 24/25/26), and
round 13's 6→7 was withdrawn (`SCORECARD.md:743`). Per the contract the row therefore records
"improved (closure round 26), score held" with the pointer, which it does.

Pointer resolution at `7118f320` (`git show 7118f320:<path> | wc -l`):

| token | file lines | status |
|---|---|---|
| `corpus/knowledge/observability-surfaces-r2.md` | 395 | exists, no line cited |
| `corpus/lessons/round-26-verifier-spotcheck.md:133` | 195 | resolves, line 133 is the `| coverage | improved |` row |
| `corpus/lessons/round-24-verifier-spotcheck.md:88` | 148 | resolves; line is "… Score 6 → 6." (round-24 closure number) |
| `SCORECARD.md:1609` | 1775 | resolves; round-26 declaration row, "coverage 6 → 6 held pending closure" |

## 4. Checks I actually ran (non-canonical)

`count-c1.sh` was **absent** from `.ufo/waves/round-29/` when I read it (directory held only `contract.md`,
`wave1-dispatch.json`, `wave1-run.json`, `wave1-spec.json`, `evidence/`, `w1/`; re-checked at the end of the seat,
still absent), so I could not run the canonical
judge. In a sandbox clone (`git clone --no-hardlinks`, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset) I applied
the row verbatim to `SCORECARD.md:10`, committed it (sandbox commit `1f130896ee34dd6b3d9cc547c41755fe9fa2f2e2`,
`1 insertion, 1 deletion`) and ran my own replication of the contract's four mismatch kinds:

- before, at `7118f320`: row cites `round-24-verifier-spotcheck.md:88` but not `round-26-…` → **1 mismatch, kind 1
  (stale closure)**; kind 2 opens "round 12" and MANIFEST admits 12; no dead pointer; score 6 equals 6.
- after, at the sandbox commit: kind 1 ok (round-26 file cited), kind 2 ok, kind 3 ok (all four backticked tokens
  resolve in the token table above), kind 4 not applicable (6 = 6) → **0 mismatches** in my replication.

This is my replication, not the counter's output; the canonical Rust judge decides. Repeat: the old row's only
defect under the four kinds is the stale round-24 pointer, which is exactly what kind 1 targets.

## 5. Judgement calls and honest notes

1. **Round 12's credit has no per-axis line.** The 5→6 score is stated in the round-12 declaration
   (`SCORECARD.md:615`) and round 12 is admitted, so the standing 6 has a basis under the score policy; but the
   round-12 spot-check file has no axis table, so kind 1 cannot be anchored there. I kept "round 12 (5 → 6 …)" in
   `Last change` because it is the last round that actually moved the number.
2. **Round 20 is the one admitted `improved` closure excluded from R** purely because the contract's R test reads a
   lane file that does not exist for round 20. If the L1 reads the definition differently, the next candidate below
   26 is 25. I did not silently substitute.
3. **Round 17 shows why the MANIFEST conjunct matters.** Its spot-check says `improved` but the closure was
   `rejected-harmed`; excluded.
4. **Round 23's number** (`coverage6→6`) sits in a disposition row after a withdrawn capability, not in an axis
   table; it is quoted only, not used for R.
5. **Kept the round-24 pointer** in the new row: it is the closure that states "Score 6 → 6" for the standing score
   and the reason the round-25 correction rewrote this row. It resolves, and removing it would drop provenance for
   the 6. It is not a substitute for the round-26 citation.
6. **Not touched:** I did not edit `SCORECARD.md`, the counter, or any product file; the lane tree gained only this
   report. Sandbox files live under my scratch dir.

## 6. Artifact paths

- Report: `.ufo/waves/round-29/w1/AxisCoverage.md`
- Candidate row text: `/fast/scratch/hyaku/mori-r29/AxisCoverage/newrow.txt`
- Sandbox clone + applied-row commit `1f130896`: `/fast/scratch/hyaku/mori-r29/AxisCoverage/sandbox`

## 7. Out of scope / handoff

- Applying the row and running `bash .ufo/waves/round-29/count-c1.sh <landed-tip> 63729047…` is the L1's call.
- Wave-wide blindness held: no tool source or output was read, and no tool was run.
