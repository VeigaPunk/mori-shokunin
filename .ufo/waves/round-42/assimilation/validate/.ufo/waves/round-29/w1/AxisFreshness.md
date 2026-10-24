# AxisFreshness — C1 draft row for `freshness` (round 29, wave 1)

Seat: `MoriR29.AxisFreshness`. Lane tip read: `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`. Closure record read:
`git -C /home/vgpnk/Projects/shokunin show 63729047:MANIFEST.json` (pinned fleet revision
`63729047644f839fe4c8cc97abd0d8bf741a5787`). Contract read: `.ufo/waves/round-29/contract.md` (C1 four mismatch
kinds, score policy, `R` definition). Blindness: I did not open, grep, cat, copy or run `tools/mori-oom-killers.py`
or any copy, and I read no round-26/27/28 `w1`/`w2` report. No git/jj writes, no installs, no pacman.

## 1. Round table, 12–28

MANIFEST cell is `verdict / verdicts.freshness` from `git show 63729047:MANIFEST.json`; every other cell is a quote
from `git show 7118f320:<path>`. MANIFEST closure rows carry no numeric score field; `no closure score field` means
only that. Score cells are filled where the closure or the lane declaration/measured-outcome section states a number.

| Round | MANIFEST verdict / freshness | Spot-check line for freshness (verbatim, path:line) | Score number stated (path:line) |
|---|---|---|---|
| 12 | admitted / unchanged | prose only, no table row: `Operability/freshness/adjacency unchanged.` — `corpus/lessons/round-12-verifier-spotcheck.md:17` | no closure score field |
| 13 | rejected-harmed / unchanged | `\| freshness \| unchanged \| Entering old drift baseline remains red and is explicitly retained; no re-pin claim. \|` — `corpus/lessons/round-13-verifier-spotcheck.md:98` | no closure score field |
| 14 | admitted / unchanged | `\| freshness \| unchanged \| live bracket rechecked; old drift pin still red, not silently re-pinned \|` — `corpus/lessons/round-14-verifier-spotcheck.md:94` | `holds coverage6/operability7/depth5/freshness5/calibration5/adjacency6` — `corpus/lessons/round-14-verifier-spotcheck.md:87` |
| 15 | admitted / unchanged | `\| freshness \| unchanged \| live observation retained; old red pin is pre-existing disclosed debt, not newly blessed \|` — `corpus/lessons/round-15-verifier-spotcheck.md:180` | no closure score field |
| 16 | admitted / unchanged | `\| freshness \| unchanged \| The r10 pin is preserved without re-pin, and its red is pre-existing debt. \|` — `corpus/lessons/round-16-verifier-spotcheck.md:131` | no closure score field |
| 17 | rejected-harmed / unchanged | `\| freshness \| unchanged \| Seven historical bytes preserved; r10 remains marked red; stale pending wording superseded append-only. \|` — `corpus/lessons/round-17-verifier-spotcheck.md:238` | no closure score field |
| 18 | admitted / unchanged | `\| freshness \| unchanged \| old r10 drift red carried; no repin \|` — `corpus/lessons/round-18-verifier-spotcheck.md:129` | no closure score field |
| 19 | admitted / unchanged | **no spot-check file at 7118f320** (`git cat-file -e` exits nonzero) | no closure score field |
| 20 | rejected-harmed / **harmed** | **no spot-check file at 7118f320** | lane table claims `\| freshness \| improved \| 5 held \|` — `SCORECARD.md:1258`; closure overrides with `harmed` |
| 21 | admitted / **improved** | **no spot-check file at 7118f320** | `freshness5→5 held` — `SCORECARD.md:1320` (declared `freshness5→5` at `SCORECARD.md:1299`) |
| 22 | admitted / unchanged | **no spot-check file at 7118f320** | no closure score field |
| 23 | rejected-honest-stop / unchanged | composite row: `Operability, depth, freshness and adjacency **unchanged within the checked boundary**` — `corpus/lessons/round-23-verifier-spotcheck.md:26` | no closure score field |
| 24 | admitted / unchanged | `\| freshness \| unchanged \| no pre-existing entry re-verified or modified \|` — `corpus/lessons/round-24-verifier-spotcheck.md:108` | no closure score field |
| 25 | admitted / unchanged | `\| freshness \| unchanged \| not claimed, held 5; the system-pressure-r24 rewrites are counted under the quality trend \|` — `corpus/lessons/round-25-verifier-spotcheck.md:129` | `held 5` — `corpus/lessons/round-25-verifier-spotcheck.md:129` |
| 26 | admitted / **improved** | `\| freshness \| improved \| C1 re-measured 4 → 0 with dated corrections and a superseding entry; three r14 \`systemd 261\` lines dated too \|` — `corpus/lessons/round-26-verifier-spotcheck.md:132` | `freshness 5 → 5 held pending closure` — `SCORECARD.md:1608` |
| 27 | rejected-honest-stop / unchanged | `\| freshness \| unchanged \| corrections to older entries are hygiene (routed defects), not a declared claim \|` — `corpus/lessons/round-27-verifier-spotcheck.md:105` | no closure score field |
| 28 | admitted / **improved** | `\| freshness \| improved \| C1 verified: eight carried row defects superseded by rows re-opened this round (hashes reproduced below), readers repointed \|` — `corpus/lessons/round-28-verifier-spotcheck.md:92` | `freshness 5 → 6 proposed` — `SCORECARD.md:1771`; declaration claim table itself says `freshness 5` — `SCORECARD.md:1755` |

Rounds with no spot-check file: **19, 20, 21, 22** (checked per round with
`git cat-file -e 7118f320:corpus/lessons/round-N-verifier-spotcheck.md`; the working tree listing of
`corpus/lessons/` at the tip agrees). Round 21's closure records why: findings `retained in this durable closure row
instead of a lane spotcheck file` (`git show 63729047:MANIFEST.json`, round 21 `verification.scope`).

## 2. R

**R = 28.** Applying the contract definition literally: admitted rounds whose lane spot-check has a
`| freshness | improved |` per-axis line are 26 and 28 (round 21 is admitted with freshness `improved` in MANIFEST but
has no lane spot-check file, so it cannot satisfy the definition); 28 is the largest. The `## Axes` row at
`SCORECARD.md:13` cites no `round-N-verifier-spotcheck.md` at all, so **mismatch kind 1 (stale closure) fires today**.

## 3. Ready-to-paste replacement row

Exact column shape `| freshness | <score> | <evidence pointer> | <last change> |`:

```
| freshness | 6 | round-28 C1 re-measured: eight carried SOURCES row defects superseded by rows re-opened this round, readers repointed (`corpus/lessons/round-28-verifier-spotcheck.md:92`); round-26 C1 re-measured stale FR10 statements 4 → 0 (`corpus/lessons/round-26-verifier-spotcheck.md:132`) | round 28 (5 → 6, proposed at `SCORECARD.md:1771`) |
```

Pointer resolution at `7118f320` (`git show 7118f320:<path> | wc -l`): `corpus/lessons/round-28-verifier-spotcheck.md`
135 lines ≥ 92; `corpus/lessons/round-26-verifier-spotcheck.md` 195 lines ≥ 132; `SCORECARD.md` 1775 lines ≥ 1771.
`Last change` opens with `round 28`, and MANIFEST 63729047 records round 28 `admitted`. All three backticked
`path:L` tokens resolve, so kind 3 is clear; kind 2 is clear; kind 4 is clear because 6 ≠ 5 at `7118f320` and the
row cites round 28, admitted, whose per-axis line reads `improved` (`round-28-verifier-spotcheck.md:92`).

## 4. Honest notes and judgement calls

1. **Score 6 basis.** The only statement of 6 is `freshness 5 → 6 proposed` at `SCORECARD.md:1771`, inside
   `### Round 28 measured outcome` under the `## Round 28 declaration` heading; the declaration claim table at
   `SCORECARD.md:1755` says only `freshness 5`. The fleet closure row states `verdicts.freshness: improved` and
   `admitted` but carries no numeric score, and the round-28 spot-check calls its SCORECARD diff `append-only ...
   no held score changed` (`corpus/lessons/round-28-verifier-spotcheck.md:78-79`). Judgement: the measured outcome is part of the
   admitted round's declaration section and the closure verdict is `improved`, so the score-policy clause
   "the admitted round's declaration proposed it and its closure verdict is `improved`" permits 6. If the L1 reads
   "declaration" strictly as the claim table (line 1755), the safe fallback is score 5 with
   `improved (closure round 28), score held` and the same `round-28-verifier-spotcheck.md:92` pointer; that fallback
   also satisfies kinds 1–3 and cannot fire kind 4.
2. **Round 20 conflict, reported verbatim.** The lane's own round-20 table says `| freshness | improved | 5 held |`
   (`SCORECARD.md:1258`) while the admitted closure record says `rejected-harmed` with `verdicts.freshness: harmed`
   (`git show 63729047:MANIFEST.json`). The current Axes row's phrase "the round-20 re-pin was rejected" agrees with
   the closure, not with the lane table. This is a closure-record disagreement outside the C1 row's four kinds; it is
   flagged, not resolved here.
3. **Round 21 divergence.** MANIFEST marks round 21 `admitted` with freshness `improved`, but the round's lane
   outcome holds the score (`freshness5→5 held`, `SCORECARD.md:1320`) and no spot-check file exists. Under the
   contract's `R` definition it is invisible; the row does not cite it. No number from round 21 is adopted.
4. **Round 26 held.** Round 26 is improved by its spot-check but the measured outcome explicitly held
   `freshness 5 → 5` (`SCORECARD.md:1608`), so only round 28 supplies a new number.
5. **Round 12 and 23 shapes.** Round 12 has no per-axis table row (prose at `:17`); round 23 has one composite
   "Other axes" row (`:26`), not a `| freshness |` row. Neither can satisfy the contract's `| <axis> | improved |`
   pattern.
6. **Old row dropped clauses.** The current row's `corpus/README.md` token has no `:L`, so it is not a kind-3 token,
   but I did not carry it: the new row points at the admitted improvement. I also did not carry the "drift pin
   still red" clause; no admitted spot-check after round 18 re-asserts a re-pin, and round 25 states freshness
   `not claimed, held 5` (`corpus/lessons/round-25-verifier-spotcheck.md:129`). If the L1 wants the drift-pin status
   preserved, append prose without a `path:L` token so kind 3 stays clear.
7. **Counter unrun.** `.ufo/waves/round-29/count-c1.sh` does not exist in the lane yet (`ls .ufo/waves/round-29/`),
   so `mismatches=0`/`C1=met` is **[INFERENCE]** from the four contract kinds checked by hand; it is not an executed
   pass. Verification the L1 should run after the edit:
   `bash .ufo/waves/round-29/count-c1.sh <landed-tip> 63729047644f839fe4c8cc97abd0d8bf741a5787`.
8. **Scope limits.** I edited nothing; this report is my only write. I read no tool source and no wave report under
   the forbidden directories. No tool installed or updated.
