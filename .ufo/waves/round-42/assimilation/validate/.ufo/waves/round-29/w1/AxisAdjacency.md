# AxisAdjacency — C1 draft row for `adjacency` (round 29, wave 1)

Seat: MoriR29.AxisAdjacency. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin` at HEAD
`8a45cefe84af0557b457308e4e0f679ca490f9e9` (contract commit). Measurement rev for every lane byte
below: `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`. Fleet rev for MANIFEST: `63729047`.
I did not edit the Axes table, the counter, any tool, or any product file. Blindness honoured: I never
opened `tools/mori-oom-killers.py` or any round-26/27/28 `w1`/`w2` report.

Commands used (all read-only; no writes outside this report and `/fast/scratch/hyaku/mori-r29/AxisAdjacency/`):

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7118f320:SCORECARD.md | sed -n '8,15p'
git -C /home/vgpnk/Projects/shokunin show 63729047:MANIFEST.json | python3 -c '<rounds[] filter on lanes.mori>'
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree --name-only 7118f320 corpus/lessons/
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7118f320:corpus/lessons/round-N-verifier-spotcheck.md | grep -n 'adjacen'
```

## 1. Admission record, rounds 12-28

"Manifest" is the mori round verdict at `MANIFEST.json@63729047` (blob line of the round-level
`"verdict"` key; `rounds[N]` index in brackets), with the MANIFEST per-axis cell
`verdicts.adjacency` beside it. "Spot-check" is the lane file at `7118f320`; the verbatim adjacency
line is reproduced in §1a under the same `path:line`.

| Round | MANIFEST verdict | Spot-check file | Line | Adjacency verdict | Score number stated (path:line) |
|---|---|---|---|---|---|
| 12 | admitted (`MANIFEST.json:6196`, rounds[313]) | `round-12-verifier-spotcheck.md` (17 lines) | :17 prose | unchanged (prose, no per-axis table) | `SCORECARD.md:618` author table "improved, 6 (held)" — overridden by the spot-check |
| 13 | rejected-harmed (`:6969`, rounds[327]) | `round-13-verifier-spotcheck.md` | :100 | harmed | `SCORECARD.md:700` "6 held" (author table, superseded) |
| 14 | admitted (`:7479`, rounds[339]) | `round-14-verifier-spotcheck.md` | :96 | **improved** | `SCORECARD.md:745` declaration "5/5/5/6"; `SCORECARD.md:797` "**6 held**" |
| 15 | admitted (`:7729`, rounds[345]) | `round-15-verifier-spotcheck.md` | :182 | unchanged | `SCORECARD.md:824` "adjacency **6**"; `SCORECARD.md:879` "6 held" |
| 16 | admitted (`:8069`, rounds[353]) | `round-16-verifier-spotcheck.md` | :133 | unchanged | `SCORECARD.md:1023` "adjacency6 remain observed" |
| 17 | rejected-harmed (`:8869`, rounds[372]) | `round-17-verifier-spotcheck.md` | :239 | **harmed** | `SCORECARD.md:1077` "6, observed, unchanged" (author, superseded by closure) |
| 18 | admitted (`:9458`, rounds[386]) | `round-18-verifier-spotcheck.md` | :124 | **improved** | `SCORECARD.md:1149` "6 held"; `SCORECARD.md:1194` "adjacency6→6" |
| 19 | admitted (`:10129`, rounds[398]) | **none** (no lane file) | — | MANIFEST `verdicts.adjacency` = improved | `SCORECARD.md:1161` "C1 adjacency6 held"; `SCORECARD.md:1217` "6, improved" |
| 20 | rejected-harmed (`:10509`, rounds[405]) | **none** | — | MANIFEST = unchanged | `SCORECARD.md:1241` "adjacency 6"; `SCORECARD.md:1263` "6 held" |
| 21 | admitted (`:10993`, rounds[412]) | **none** | — | MANIFEST = unchanged | `SCORECARD.md:1304` "adjacency6 held" |
| 22 | admitted (`:11992`, rounds[427]) | **none** | — | MANIFEST = unchanged | `SCORECARD.md:1343` / `:1361` "adjacency6" |
| 23 | rejected-honest-stop (`:12249`, rounds[432]) | `round-23-verifier-spotcheck.md` | :26 ("Other axes" row) | unchanged within checked boundary | `SCORECARD.md:1429` "adjacency6"; `:1456` "adjacency6 held" |
| 24 | admitted (`:12895`, rounds[443]) | `round-24-verifier-spotcheck.md` | :109 | unchanged | `SCORECARD.md:1508` / `:1528` "adjacency 6" |
| 25 | admitted (`:13416`, rounds[455]) | `round-25-verifier-spotcheck.md` | :126 (and :49) | unchanged | `SCORECARD.md:1548` / `:1571` "adjacency 6"; `round-25-verifier-spotcheck.md:49` holds `round 1` rows at their round-1 scores |
| 26 | admitted (`:13707`, rounds[462]) | `round-26-verifier-spotcheck.md` | :137 | unchanged | `SCORECARD.md:1600` / `:1622` "adjacency 6" |
| 27 | rejected-honest-stop (`:13960`, rounds[468]) | `round-27-verifier-spotcheck.md` | :107 | unchanged | `SCORECARD.md:1729` / `:1744` "adjacency 6" |
| 28 | admitted (`:14297`, rounds[476]) | `round-28-verifier-spotcheck.md` | :97 | unchanged | `SCORECARD.md:1758` / `:1774` "adjacency 6" |

Rounds **without** a lane verifier spot-check file: **19, 20, 21, 22** (`git ls-tree 7118f320
corpus/lessons/` lists spot-checks only for 12-18 and 23-28). Round 19's MANIFEST
`verification.spotcheck` reads "Inline in this durable closure row; assignment forbids lane/report
edits" and round 22's reads "Recorded in this MANIFEST entry only (no lane writes)"; rounds 20 and 21
carry no `spotcheck` key. So rounds 19-22 have an outside closure recorded in the fleet MANIFEST but
no lane file — relevant to the R question in §2.

MANIFEST per-axis cells (`verdicts.adjacency`), 12→28: unchanged, harmed, improved, unchanged,
unchanged, harmed, improved, improved, unchanged, unchanged, unchanged, unchanged, unchanged,
unchanged, unchanged, unchanged, unchanged. Only 14, 18 and 19 are `improved`; all three rounds are
`admitted`.

### 1a. Verbatim adjacency lines at `7118f320` (exact bytes, pipes kept)

```text
corpus/lessons/round-12-verifier-spotcheck.md:17 (prose in the Adjudication paragraph; no adjacency table line)
  ... Operability/freshness/adjacency unchanged. Runtime 1.9→4.3s is an explicit cost with no declared budget; not evidence of a correctness regr…
corpus/lessons/round-13-verifier-spotcheck.md:100
  | adjacency | harmed | Fleet/non-fleet unit distinction and explicit tsukuroi ownership disappear while same stable failure id expands to all user units. No sibling files were edited, but scope reporting still regressed. |
corpus/lessons/round-14-verifier-spotcheck.md:96
  | adjacency | improved | measured tsukuroi non-fleet route restored; no diagnosis/actuation ownership takeover |
corpus/lessons/round-15-verifier-spotcheck.md:182
  | adjacency | unchanged | aggregate-only subject routing and tsukuroi INFO route retained; no OS remediation, dispatch or ownership expansion |
corpus/lessons/round-16-verifier-spotcheck.md:133
  | adjacency | unchanged | No census cutover, host remediation or ownership expansion. PROVINCE adds only the lane's own window probe. |
corpus/lessons/round-17-verifier-spotcheck.md:239
  | adjacency | **harmed** | Private operator configuration and other-session tool/document/history excerpts were copied into landed evidence despite the field/minimization boundaries. Disclosure does not un-copy them. |
corpus/lessons/round-18-verifier-spotcheck.md:124
  | adjacency | improved | r17 routed private content removed at the tip; must-redact 40→0; metric 116→0; residual rule gaps routed |
corpus/lessons/round-23-verifier-spotcheck.md:26 (inside the "| Other axes |" row; no per-axis line)
  ... Operability, depth, freshness and adjacency **unchanged within the checked boundary**; no universal host-effect or historically harm-free claim. |
corpus/lessons/round-24-verifier-spotcheck.md:109
  | adjacency | unchanged | PROVINCE gains an appended adjacency note (tsukuroi /proc/pressure/memory); routed item 5 is a why-not, not counted |
corpus/lessons/round-25-verifier-spotcheck.md:126
  | adjacency | unchanged | retention scan 4 → 4 at the head; mid-round 88 repaired in-round; history to operator |
corpus/lessons/round-25-verifier-spotcheck.md:49 (D5 row on the Axes table itself)
  ... rows still reading `round 1` (freshness, calibration, adjacency) keep their round-1 scores → held |
corpus/lessons/round-26-verifier-spotcheck.md:137
  | adjacency | unchanged | sibling tsukuroi cited as S125 (tier B), not absorbed; PROVINCE adjacency unchanged |
corpus/lessons/round-27-verifier-spotcheck.md:107
  | adjacency | unchanged | adjacency paragraph added, no claim; no bleed found |
corpus/lessons/round-28-verifier-spotcheck.md:97
  | adjacency | unchanged | held, no claim |
```

## 2. R — latest admitted round with `improved`

**R = 18.** Under contract mismatch kind 1 the two conditions are (a) pinned MANIFEST records mori
round N `admitted` and (b) the **lane** file `corpus/lessons/round-N-verifier-spotcheck.md` at the
measured rev holds a per-axis table line `| adjacency | improved |`. The candidates are 14 and 18
(only files with such a line, both admitted). 18 > 14 → R = 18.
`corpus/lessons/round-18-verifier-spotcheck.md` is 192 lines at `7118f320`, so `:124` resolves.

Current row at `SCORECARD.md:15` cites no spot-check at all ("round 1" in Last change), so at
`7118f320` the adjacency row fails kind 1 (stale closure); this is the row this draft repairs.

## 3. Ready-to-paste replacement row

Replace line 15 of `SCORECARD.md` (`| adjacency | 6 | refuses dispatch ... | round 1 |`) with:

```markdown
| adjacency | 6 | refuses dispatch (kumitate), OS state (tsukuroi) and harness configuration (operator) in PROVINCE and in its tools; the r17 privacy harm was cured at the round-18 tip (must-redact 40→0; metric 116→0), cited at `corpus/lessons/round-18-verifier-spotcheck.md:124` | improved (closure round 18), score held |
```

Column check: four cells, five pipes, no pipe inside a cell.
Pointer resolution at `7118f320` (`git show 7118f320:<path> | wc -l`):

```text
corpus/lessons/round-18-verifier-spotcheck.md  -> 192 lines  >= 124  OK
```

Mismatch-kind check on the row (literal implementation of the four kinds, run in a throwaway
heredoc; the round-29 counter does not exist yet at `8a45cefe`):

- kind 1 (stale closure): row cites `round-18-verifier-spotcheck.md`, R = 18 → passes.
- kind 2 (unadmitted last change): Last change opens with "improved", not `round N`; even if a
  parser scans for `round 18`, MANIFEST admits 18 → passes.
- kind 3 (dead pointer): one backticked `path:L` token, resolves with 192 ≥ 124 lines → passes.
- kind 4 (score without basis): score 6 equals the `7118f320` score 6, so the condition is not
  triggered → passes.

## 4. Judgement calls and honest notes

1. **Round 19 is the one real ambiguity.** MANIFEST records mori round 19 `admitted` with
   `verdicts.adjacency = improved`, but the lane has no `round-19-verifier-spotcheck.md`; its
   `verification.spotcheck` value says the closure was recorded inline in the MANIFEST entry. If the
   landed counter reads kind 1 as "MANIFEST admitted **and** MANIFEST verdict improved", R would be 19
   and the required citation would be a lane file that does not exist, so no row could satisfy it. The
   contract text names the lane file explicitly, so I took R = 18. **Have BuildCountC1 confirm this
   before the counter is frozen**; if the counter disagrees, the counter is wrong against the contract,
   not the row.
2. **Score stays 6.** No admitted closure states a new adjacency number: round 14 writes "**6 held**"
   (`SCORECARD.md:797`) and its declaration says adjacency remains 6 (`SCORECARD.md:745`); round 18
   writes "6 held" (`SCORECARD.md:1149`); round 19 writes "adjacency6→6" (`SCORECARD.md:1194`) and
   "6 | improved" (`SCORECARD.md:1217`). No "adjacency 7" appears anywhere in the SCORECARD at
   `7118f320`. The round-14 declaration also states the principle explicitly: "No new scalar point is
   pre-awarded for repairing a prior harm" (`SCORECARD.md:757`).
3. **Wording of Last change.** I used the contract's exact prescribed phrase
   `improved (closure round 18), score held` rather than `round 18 (6 → 6)`. Semantics: the last
   non-held movement was round 18's closure improvement; the score did not move. A reader must not
   read it as a score change.
4. **Round 12 conflict.** The lane's own round-12 table claims `| adjacency | **improved** | 6 (held) |`
   (`SCORECARD.md:618`), while the outside spot-check for the same admitted round says
   "Operability/freshness/adjacency unchanged" (`corpus/lessons/round-12-verifier-spotcheck.md:17`).
   Kind 1 keys on spot-check lines, and the closure governs, so round 12 is not a candidate and its
   author table is not cited in the row. This is a stale author claim in history, not a row defect.
5. **Round 25's D5 row already ruled the `round 1` cell acceptable at the time**: "rows
   still reading `round 1` (freshness, calibration, adjacency) keep their round-1 scores → held"
   (`corpus/lessons/round-25-verifier-spotcheck.md:49`). That supported the score but did not cure the
   missing closure pointer; kind 1 still fails at `7118f320`, which is why the row changes at all.
6. **NOT MEASURED**: I did not run `.ufo/waves/round-29/count-c1.sh` (absent at `8a45cefe`) and did
   not run the round-28 `count-c1.sh` (different claim). The counter results in §3 come from my own
   literal re-implementation of the four kinds for this one row, not from committed counter bytes.
   [INFERENCE] that a faithful counter accepts the row; that inference rests on the contract text.
7. **Scope discipline.** Only this report was written in the lane. Two throwaway files were created in
   `/tmp` before the scratch dir existed (`/tmp/sc7118.md`, `/tmp/man.json`); no lane, fleet or sibling
   bytes were created or modified. The `corpus/lessons/round-28.md` +8-line working-tree delta and the
   new `w1/SourceJournalMonotonic.md` are other seats' work, untouched.
8. **No installs.** No pacman/uv/npx/cargo action was needed or taken.
9. **Privacy.** No OMP settings values, session ids, uids/pids, unit names, journal MESSAGE text or
   earlyoom configuration values appear in this report or in the row.
