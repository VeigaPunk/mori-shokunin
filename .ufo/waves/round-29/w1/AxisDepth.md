# w1 · C1 axis row draft — `depth`

Seat: MoriR29.AxisDepth (wave 1, leaf). Lane `mori-shokunin`. Judged revision `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`.
Fleet closure record read at `63729047644f839fe4c8cc97abd0d8bf741a5787` (pinned). Detection and report only: no lane
write outside this file, no git/jj write, no tool source opened, no host state read.

## 0. Inputs and how they were read

- Contract: `.ufo/waves/round-29/contract.md` (C1 statement, four mismatch kinds, score policy).
- Axes table at `7118f320`: `git show 7118f320:SCORECARD.md | sed -n '8,15p'`. Working-tree `SCORECARD.md` blob
  `cf994540ba0c249cd9cbd099fc23f4d4cf661527` equals `git rev-parse 7118f320:SCORECARD.md` — every `SCORECARD.md:L`
  below is therefore valid at both the pinned rev and the current tree (1775 lines).
- Fleet verdicts: `git -C /home/vgpnk/Projects/shokunin show 63729047:MANIFEST.json`, filtered to `lane == "mori"`:
  17 entries, all `type: closure`, rounds 12–28, one per round (no `closure-correction` entries for mori in that
  window). Field used: `verdict` plus `verdicts.depth`.
- Spot-checks: `corpus/lessons/round-N-verifier-spotcheck.md`, `grep -n depth` per file.
  **No spot-check file exists for rounds 19, 20, 21, 22.** Files exist for 12–18 and 23–28.
- Provenance spot: round-27 spot-check blob `23b22323cfd4b5da8dab8217d9afadfec6b229d1` identical at `7118f320` and
  in the working tree (158 lines).

## 1. Table — rounds 12–28

Pipes inside verbatim quotes are escaped as `\|` (markdown table necessity); everything else is byte-verbatim.
`SB` = `corpus/lessons/round-N-verifier-spotcheck.md`, `SC` = `SCORECARD.md`.

| round | MANIFEST verdict (depth) | spot-check depth line | depth score stated by closure or declaration |
|---|---|---|---|
| 12 | `admitted` (depth: improved) | `SB-12:17` — no per-axis table in the 17-line file; adjudication reads: "Depth improved (SKILL primary links 0→5; four sourced OOM notes; score 4→5)" | `SC:613` `\| depth \| **improved** \| 4 → 5 \|` (round-12 measured outcome); declaration `SC:607` claim 1 (targets, no score) |
| 13 | `rejected-harmed` (depth: unchanged) | `SB-13:97` `\| depth \| unchanged \| Source-linked detail supports C1/C2; no independent depth move established. \|` | `SC:697` `\| depth \| unchanged \| **5 held** \|` |
| 14 | `admitted` (depth: unchanged) | `SB-14:93` `\| depth \| unchanged \| sourced typed semantics support C1; no separate depth move \|` | `SC:794` `**5 held**`; `SC:745` "remain **5/5/5/6**" |
| 15 | `admitted` (depth: unchanged) | `SB-15:179` `\| depth \| unchanged \| primary-source typed predicates are grounded; no separate depth claim \|` | `SC:876` `**5 held**`; `SC:823` "**5/5/5**" |
| 16 | `admitted` (depth: unchanged) | `SB-16:130` `\| depth \| unchanged \| S014/S015/S039/S040 ground narrow cursor mechanics. No separate depth claim. \|` | `SC:985` `5 held` |
| 17 | `rejected-harmed` (depth: unchanged) | `SB-17:237` `\| depth \| unchanged \| Primary-source detail added; no independent depth move claimed. \|` | `SC:1075` `\| depth \| 5 \| observed, unchanged \|`; `SC:1119` `5 held` |
| 18 | `admitted` (depth: unchanged) | `SB-18:127` `\| depth \| unchanged \| no depth claim \|` | `SC:1152` `\| coverage, depth, freshness \| unchanged \| 6/5/5 held \|` |
| 19 | `admitted` (depth: unchanged) | **no spot-check file** | `SC:1221` `\| depth \| 5 \| unchanged \|` |
| 20 | `rejected-harmed` (depth: unchanged) | **no spot-check file** | `SC:1262` `\| depth \| unchanged \| 5 held \|`; `SC:1241` "depth 5" |
| 21 | `admitted` (depth: unchanged) | **no spot-check file** | `SC:1304` "depth5, adjacency6 held." |
| 22 | `admitted` (depth: unchanged) | **no spot-check file** | `SC:1343` "Other axes coverage6/operability7/depth5/adjacency6 unchanged." |
| 23 | `rejected-honest-stop` (depth: unchanged) | `SB-23:26` — no per-axis depth row; "Other axes" row: "Operability, depth, freshness and adjacency **unchanged within the checked boundary**" | `SC:1409` "Other axes … depth5/freshness5/adjacency6 unchanged."; declaration `SC:1429` "depth5" held |
| 24 | `admitted` (depth: unchanged) | `SB-24:107` `\| depth \| unchanged \| SKILL additions are appended only (the whole diff has 0 deleted lines) and unclaimed; sweep defect D2 is in new material \|` | measured `SC:1527` "Held: operability 7, depth 5, freshness 5, adjacency 6."; declaration `SC:1508` "depth 5" |
| 25 | `admitted` (depth: unchanged) | `SB-25:127` `\| depth \| unchanged \| not claimed, held 5; the new SKILL block adds grounded rows but row 2 is over-scoped (R3) \|` | measured `SC:1571` "Held: operability 7, depth 5, …"; declaration `SC:1548` "depth 5" |
| 26 | `admitted` (depth: unchanged) | `SB-26:135` `\| depth \| unchanged \| held \|` | measured `SC:1622` "Held: operability 7, depth 5, …"; declaration `SC:1600` "depth 5" |
| 27 | `rejected-honest-stop` (depth: **improved**) | `SB-27:102` `\| depth \| improved \| C1 re-measured 0/0 → 7/11, \`C1=met\`; entry facts hold against upstream bytes \|` | measured outcome `SC:1741`: "improved, bounded: … ; depth 5 → 6 proposed, pending closure"; declaration `SC:1726` "depth 5" |
| 28 | `admitted` (depth: unchanged) | `SB-28:94` `\| depth \| unchanged \| held, no claim \|` | measured `SC:1774` "Held: depth 5, calibration 5, coverage 6, adjacency 6."; declaration `SC:1758` "depth 5" |

Round 27's own file states the closure outcome at `SB-27:77`: "… this is an honest stop, not a harm: verdict
**rejected-honest-stop**." The lane records the same at `SC:1749`: "round 27 closed `rejected-honest-stop`: C1 depth
verified, C2 withdrawn and so not verified".

Out of window but noted once: the round-2…round-11 verdict tables also carry `| depth | **improved** |` rows
(`SCORECARD.md:117,176,228,283,329,380,432,472,514,569`); the contract's window is 12–28, so they are not counted.

## 2. R — latest admitted round with `improved`

Contract rule 1 defines R as the largest N in 12–28 where the pinned MANIFEST records mori round N `admitted` **and**
`corpus/lessons/round-N-verifier-spotcheck.md` holds a per-axis line `| depth | improved |`.

- By that test **no round qualifies**: round 27 holds the `improved` line but its MANIFEST verdict is
  `rejected-honest-stop`; round 12 is `admitted` with `verdicts.depth = improved` but its 17-line spot-check predates
  the per-axis table (`git show 7118f320:corpus/lessons/round-12-verifier-spotcheck.md | wc -l` → `17`).
- By the weaker reading (MANIFEST `admitted` ∧ `verdicts.depth == improved`), **R = 12**, and it is the only such
  round. Both readings are cited in the row below, so the row satisfies either one.

## 3. Replacement row (ready to paste, one line)

```markdown
| depth | 5 | source-linked knowledge entries with `source:`/`verified-at:`/`recheck:` lines (round 12 claim 1); round-12 outside spot-check records depth improved and score 4 → 5 (`corpus/lessons/round-12-verifier-spotcheck.md:17`); improved (closure round 27), score held: the round-27 per-axis verdict reads improved (`corpus/lessons/round-27-verifier-spotcheck.md:102`) under a closure ruled rejected-honest-stop (`corpus/lessons/round-27-verifier-spotcheck.md:77`), so the 5 → 6 proposed by the round-27 measured outcome (`SCORECARD.md:1741`) is not counted | round 12 (4 → 5) |
```

Pointer resolution at `7118f320` (`git show 7118f320:<path> | wc -l`):

- `corpus/lessons/round-12-verifier-spotcheck.md` → `17` (cites `:17`, inclusive edge).
- `corpus/lessons/round-27-verifier-spotcheck.md` → `158` (cites `:77`, `:102`).
- `SCORECARD.md` → `1775` (cites `:1741`).
- Non-path backticked tokens `source:` / `verified-at:` / `recheck:` carry no line number and are key names, not
  pointers; the cell contains no other `path:N` token.

Score policy application: the score stays **5**. No admitted closure states a depth number other than 5 after round
12 (round 12's admitted closure states `4 → 5`, already in the cell), and the one round that proposed `5 → 6`
(round 27) closed `rejected-honest-stop`, so its number is not counted; the row records "improved (closure round 27),
score held" with the closure pointers. The `Last change` cell keeps opening with `round 12`, which the pinned MANIFEST
records `admitted` (mismatch kind 2 cannot fire).

## 4. Judgement calls and limits (honest notes)

1. **R is empty under the literal rule.** I did not invent a round to satisfy rule 1. Because the rule is conditional
   ("If R exists"), the row needs no `round-R` citation to pass; I cite round 12 anyway so that a counter computing
   R from `verdicts.depth` alone (R = 12) also passes. If the counter computes R from the per-axis line only, R is
   absent and the extra citation is harmless.
2. **Round 27 is recorded but not credited.** Its spot-check genuinely rules `improved` (`SB-27:102`) and the
   declaration/measured outcome genuinely proposes `5 → 6` (`SC:1741`), but the closure is
   `rejected-honest-stop` (`SB-27:77`, `SC:1749`, MANIFEST `verdict`). The score policy admits a change only on an
   admitted closure or an admitted declaration plus `improved` closure verdict; neither holds, so 5 is held and the
   move is written down as uncounted. This is a judgement call only in the sense of *where* to write it.
3. **Where the round-27 record sits.** I put "improved (closure round 27), score held" and all round-27 pointers in
   the **Evidence pointer** cell and left `Last change` as `round 12 (4 → 5)`. Reasons: (a) rule 2's test reads only
   the `Last change` cell and only its opening token, so any `round 27` there would be a needless trap given mori 27
   is not `admitted`; (b) the coverage and calibration rows set the precedent — closure score citations live in the
   evidence cell (`corpus/lessons/round-24-verifier-spotcheck.md:88` and `:68`); (c) `Last change` is the last
   *score* change, and no score changed. If L1 prefers the policy phrase in `Last change` instead, the same text can
   move there verbatim and `Last change` would then open with `improved`, not `round N`; that variant is *not*
   authored here because it trades a certain rule-2 reading for a stylistic match.
4. **Unrun check.** `bash .ufo/waves/round-29/count-c1.sh 7118f320 63729047…` was not run: the counter does not
   exist yet (`cat .ufo/waves/round-29/count-c1.sh` → `No such file or directory` at the time of this report). This
   row's compliance is argued against the contract text, not measured by the counter. [INFERENCE] How the landed
   counter tokenizes "opens with `round N`" and "backticked `path:L`".
5. **Verbatim fidelity.** Quotes are copied from `grep -n`/`sed -n` output at `7118f320`; only the table separators
   inside quotes are escaped (`\|`). Round 12's quote is a prose fragment of a long line, not a table row, because
   that file has no axis table — the absence is the finding, not an omission.
6. **No claim about depth itself.** This draft judges table-versus-record agreement only. Whether depth *is* 5 is not
   re-derived here.

## 5. Bounds, provenance and tooling

- Files written: this report only. No lane edit, no fleet edit, no scratch dir created (none needed).
- Read-only git only (`show`, `rev-parse`, `hash-object` via `git hash-object` on a working-tree file). No clone.
- Blindness respected: `tools/mori-oom-killers.py` was not opened, grepped or run; no report under round-26/27/28
  `w1`/`w2` was opened (only `corpus/lessons/round-27-verifier-spotcheck.md` and the SCORECARD/MANIFEST sources named
  by this item).
- No tool installed or upgraded; no package transaction; no service touched. No host identifiers or settings values
  transcribed.
- Commands that mattered, with outcomes: `git show 63729047:MANIFEST.json` (17 mori closures, rounds 12–28);
  `git show 7118f320:SCORECARD.md | sed -n '8,15p'` (six rows, depth = 5, `round 12 (4 → 5)`);
  `git rev-parse 7118f320:SCORECARD.md` = `git hash-object SCORECARD.md` = `cf994540…`;
  `git show 7118f320:corpus/lessons/round-12-verifier-spotcheck.md | wc -l` → 17;
  `git show 7118f320:corpus/lessons/round-27-verifier-spotcheck.md | wc -l` → 158.
