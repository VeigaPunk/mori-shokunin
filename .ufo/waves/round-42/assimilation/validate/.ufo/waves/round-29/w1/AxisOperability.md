# AxisOperability — C1 draft row for `operability` (round 29, wave 1)

Seat `MoriR29.AxisOperability` (leaf, no subagents). Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering tip `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`. The lane moved while this seat worked: HEAD was
`8a45cefe84af0557b457308e4e0f679ca490f9e9` (contract landing) when the seat started, then `3a14713` (contract
amendment A1, "C1 counter hardened before data") and `6612516` (amendment A2, "C1 kind 2b, C2 shape lines,
corrections"). **A1 and A2 change C1's mismatch kinds and its score policy, so the replacement row in §4 is derived
against the amended contract** (`.ufo/waves/round-29/contract.md`, 153 lines, 12867 bytes at `6612516`); the first
draft of this report, written against the pre-amendment text, is superseded and not quoted here as a candidate.
At seat start `git status --porcelain` showed `M corpus/lessons/round-28.md` (another seat's landing in progress);
it is clean at `6612516`. This seat made no such change.
Pinned fleet record `63729047`; C1 counter absent throughout (see §5). Blindness kept: `tools/mori-oom-killers.py`
never opened, no report under `.ufo/waves/round-2[678]/w[12]/` opened. No URL fetched, no install or upgrade.
Only file written: this one.

## 1. Method (commands actually run, all read-only)

```
git -C /home/vgpnk/Projects/shokunin show 63729047:MANIFEST.json > /tmp/manifest-r29.json   # exit 0, 1110380 bytes
git -C <lane> show 7118f320:SCORECARD.md | wc -l                                            # 1775
git -C <lane> show 6612516:SCORECARD.md | wc -l                                             # 1775 (identical row at :11)
git -C <lane> show 7118f320:corpus/lessons/round-28-verifier-spotcheck.md | wc -l           # 135
git -C <lane> ls-tree --name-only 7118f320:corpus/lessons/                               # spot-check inventory
git -C <lane> show <rev>:corpus/lessons/round-N-verifier-spotcheck.md | grep -n '^| operability'
git -C <lane> show <rev>:SCORECARD.md | grep -n 'operability'
git -C <lane> cat-file -e 6612516:.ufo/waves/round-29/count-c1.sh                        # exit 128: absent
python3 (stdin heredoc)   # MANIFEST mori-row extraction; hand check of the amended kinds
```

Read-only git only (`show`, `ls-tree`, `cat-file -e`, `rev-parse`, `log`, `status`); no git/jj write, no clone.

## 2. Round table (rounds 12–28)

MANIFEST rows are the `lane: "mori"` entries of `63729047:MANIFEST.json` (`lane_round`, `admitted`, `verdict`,
`verdicts.operability`). Spot-check lines are quoted verbatim at `7118f320` (identical at `6612516`); a literal
`…` marks elided words inside a quote (verdict cells are never elided).

```
round | MANIFEST mori verdict / verdicts.operability | spot-check operability line (path:line) | score number stated (path:line)
12 | admitted / unchanged  | corpus/lessons/round-12-verifier-spotcheck.md:17 — prose only, no per-axis table: "Operability/freshness/adjacency unchanged." | SCORECARD.md:616 round-12 table: | operability | **unchanged** | 6 |
13 | rejected-harmed / improved | corpus/lessons/round-13-verifier-spotcheck.md:96: | operability | improved | C2's F01/F02 repairs independently verify: named defects 2→0, BANANA 28/28→0/28 and honest 28/28 held. This does not offset harm on coverage/adjacency. | | SCORECARD.md:696: | operability | improved | **6 → 7** | (closure rejected, so not a change basis)
14 | admitted / unchanged  | corpus/lessons/round-14-verifier-spotcheck.md:92: | operability | unchanged | verified r13/F01/F02 behavior retained; delivered gate selftests/registries supplied; setup failure honestly corrected | | SCORECARD.md:793: | operability | unchanged | **7 held** |
15 | admitted / unchanged  | corpus/lessons/round-15-verifier-spotcheck.md:178: | operability | unchanged | settled selftests, frozen controls, boundaries and prior routing/silence receipts hold; stale registry wording routed, not a gate bypass | | SCORECARD.md:875: | operability | unchanged | **7 held** |
16 | admitted / unchanged  | corpus/lessons/round-16-verifier-spotcheck.md:129: | operability | unchanged | New gate selftests pass after committed setup repairs. Prior production bytes are unchanged (6/6). Score 7 held. | | SCORECARD.md:984: | operability | unchanged | 7 held |
17 | rejected-harmed / improved | corpus/lessons/round-17-verifier-spotcheck.md:235: | operability | improved | C2 same-harness 204 assertions, 60→0; retained failed/passing oracle runs. | | SCORECARD.md:1044: | C2 operability | … | 7→7 | improved; SCORECARD.md:1117: | operability | improved | 7 held |
18 | admitted / improved  | corpus/lessons/round-18-verifier-spotcheck.md:126: | operability | improved | dispatch-ledger capability runs; w1 1/1, w2 2/2 bound; residual 7/7 bound with a reported failing shape | | SCORECARD.md:1151: | operability | improved (capability) | 7 held |
19 | admitted / unchanged  | NO SPOT-CHECK FILE at 7118f320 | SCORECARD.md:1220: | operability | 7 | unchanged |
20 | rejected-harmed / unchanged | NO SPOT-CHECK FILE at 7118f320 | SCORECARD.md:1260: | operability | unchanged | 7 held |
21 | admitted / unchanged  | NO SPOT-CHECK FILE at 7118f320 | SCORECARD.md:1343: Other axes coverage6/operability7/depth5/adjacency6 unchanged.
22 | admitted / unchanged  | NO SPOT-CHECK FILE at 7118f320 | SCORECARD.md:1409: Other axes coverage6/operability7/depth5/freshness5/adjacency6 unchanged.
23 | rejected-honest-stop / unchanged | corpus/lessons/round-23-verifier-spotcheck.md:26: | Other axes | … | Operability, depth, freshness and adjacency **unchanged within the checked boundary**; … | | SCORECARD.md:1429: Other scores held operability7/depth5/freshness5/adjacency6.
24 | admitted / unchanged  | corpus/lessons/round-24-verifier-spotcheck.md:106: | operability | unchanged | git diff --name-status c725aa37 4f05dd5a: 101 A, 7 M, 0 D, … The census was byte-identical and its selftest passed 134/134 per the report (not re-run here) | | SCORECARD.md:1526: census no-harm selftest PASS (134 cases, 134 passed, …); SCORECARD.md:1527: Held: operability 7
25 | admitted / unchanged  | corpus/lessons/round-25-verifier-spotcheck.md:128: | operability | unchanged | not claimed, held 7; two new tools lack registry rows, the C1 tool lacks a self-test (R5) | | SCORECARD.md:1548: Held and observed: operability 7
26 | admitted / unchanged  | corpus/lessons/round-26-verifier-spotcheck.md:134: | operability | unchanged | selftests and tallies hold (committed wave-2 report) | (a second line, :125, sits in the No-harm-checks table, not the per-axis table) | SCORECARD.md:1600: Held and observed: operability 7
27 | rejected-honest-stop / unchanged | corpus/lessons/round-27-verifier-spotcheck.md:103: | operability | unchanged | C2 unmet (withdrawn); tools/ identical, self-test tallies unchanged | | SCORECARD.md:1744: Held: … operability 7 …
28 | admitted / improved  | corpus/lessons/round-28-verifier-spotcheck.md:93: | operability | improved | C2 verified: ten A2 rules pinned by 30 frozen cases, PASS 30/30, tool unchanged | | SCORECARD.md:1756 declaration: operability 7 (before-column); SCORECARD.md:1772: improved, pending closure; operability held at 7 (case pinning strengthens an existing capability)
```

Rounds with **no** `corpus/lessons/round-N-verifier-spotcheck.md` at `7118f320` or `6612516`: **19, 20, 21, 22**
(`git ls-tree --name-only 7118f320:corpus/lessons/` lists `round-19.md` … `round-22.md` without spot-check files).
Round 12 has a spot-check file but no per-axis table (prose at line 17); round 23's operability sentence is in a
`| Other axes |` row, not an axis row.

Amended kind 5 (`Closure disagreement`) is satisfied for operability: in every row above the lane's operability
verdict equals MANIFEST `verdicts.operability` (13, 17, 18, 28 `improved`; all others `unchanged`).

## 3. R under the amended closure-authority rule

Imp(operability) = { N ∈ 12..28 : mori round N admitted and `verdicts.operability == "improved"` }.
Admitted-with-improved: **18, 28** (13 and 17 carry `improved` but are `rejected-harmed`). So **R = 28**, and
Cite(28) is the lane file `corpus/lessons/round-28-verifier-spotcheck.md` (it exists at the rev, so the literal
`MANIFEST.json@63729047 mori round 28` token does not apply). The seat's own scan of rounds 12–28 printed
`R = 28`. This is [not the C1 counter].

## 4. Ready-to-paste replacement row

Score policy under A1: the declaration clause is deleted and an `improved` verdict alone is never a basis, so a
numeric change needs a `Cite(N):L` line stating `X → Y`. No such operability line exists (round 18
`SCORECARD.md:1151` and round 28 `SCORECARD.md:1772` both say "7 held"; round 13's `6 → 7` at `SCORECARD.md:696`
belongs to a `rejected-harmed` round). Score therefore **stays 7** and the held form is used.

```markdown
| operability | 7 | census `--selftest` PASS (134 cases) before and after round 24 (`SCORECARD.md:1526` round-24 measured outcome); held 7 in every round table since round 13, first admitted in round 14 (round 13 closed rejected-harmed); improved (closure round 28), score held — ten A2 rules pinned by 30 frozen cases, PASS 30/30 (`corpus/lessons/round-28-verifier-spotcheck.md:93`; `tools/fixtures/mori-oom-killers/cases-a2.json`) | round 28 (improved, score held) |
```

Current row at `7118f320:SCORECARD.md:11` (identical at `6612516:SCORECARD.md:11`), for diffing:

```markdown
| operability | 7 | census `--selftest` PASS (134 cases) before and after round 24 (`SCORECARD.md` round-24 measured outcome); held 7 in every round table since round 13, first admitted in round 14 (round 13 closed rejected-harmed) | round 14 (6 → 7; round 13's self-assessed 7 was not held) |
```

Two cells change. Evidence cell: the census pointer gains `:1526`; the round-28 held improvement and its closure
pointer are appended; the round-25 R4a lineage sentence is kept word for word. Last change cell: `round 14 (6 → 7;
…)` becomes `round 28 (improved, score held)` — the old form is now a mismatch twice over: amended kind 2 wants
`N ≥ R = 28`, and amendment A2's kind 2b catches exactly `round 14 (6 → 7)` because MANIFEST mori round 14 is
`verdicts.operability: unchanged`. Score stays `7`.

### Pointer resolution (amended kind 3), checked at `7118f320` and `6612516`

| token | check | result |
|---|---|---|
| `SCORECARD.md:1526` | `git show <rev>:SCORECARD.md \| wc -l` | 1775 ≥ 1526; line 1526 is inside the round-24 measured outcome (1513–1529) |
| `corpus/lessons/round-28-verifier-spotcheck.md:93` | `git show <rev>:corpus/lessons/round-28-verifier-spotcheck.md \| wc -l` | 135 ≥ 93; line 93 is `\| operability \| improved \| C2 verified: …` |
| `tools/fixtures/mori-oom-killers/cases-a2.json` | `git cat-file -e <rev>:…` | exit 0 at both revs; JSON holds 30 cases |
| `--selftest` | no `/`, no `.md/.json/.py/.sh` suffix | not a path token |

### Hand check of the amended kinds on the candidate row ([not the counter])

1. Stale closure: backticked `corpus/lessons/round-28-verifier-spotcheck.md:93` present and line 93 matches
   `^| operability | improved |` — pass.
2. Last change: opens `round 28`; round 28 admitted; `28 ≥ R = 28`; no `(X → Y)` so kind 2b is vacuous — pass.
   Held form matches `round N (improved, score held)`.
3. Dead pointer: all three path tokens resolve (table above) — pass.
4. Score without basis: `7` equals the `7118f320` value, so no basis line is required — pass (not applicable).
5. Closure disagreement: no operability disagreement exists in the lane files (§2) — pass for this axis.

## 5. Unrun gates and honest notes

1. **The C1 counter was never run.** `git cat-file -e 6612516:.ufo/waves/round-29/count-c1.sh` exits 128 (no such
   path); `ls .ufo/waves/round-29/` lists only `contract.md`, `evidence/`, `w1/` and the three wave-1 JSON files.
   Nothing here claims `mismatches=0` or `C1=met`; the five-kind check in §4 is a hand re-implementation of the
   amended text, not the committed counter. I did not create a scratch clone to test the row because there was no
   counter to run against it.
2. **Score held at 7 is the only defensible value** under the amended kind 4: the basis must be a `Cite(N):L` line
   stating `X → Y` with X = 7. Round 13's `6 → 7` (`SCORECARD.md:696`) is not admitted; round 18
   (`SCORECARD.md:1151`) and round 28 (`SCORECARD.md:1772`) say "7 held". Raising to 8 would have no basis and
   would also contradict the contract's "Held, not claimed" list, which omits operability (implicitly holding 7).
3. **Where the held phrasing lives.** A1 prescribes the held form for the Last change cell
   (`round N (improved, score held)`); the evidence cell repeats "improved (closure round 28), score held" so the
   row still reads correctly if only the evidence cell is skimmed. The round-14 first-admission history now lives
   only in the evidence cell — deliberate, so kind 2b stays vacuous.
4. **Round-26 hazard for the counter (not for this row).** `corpus/lessons/round-26-verifier-spotcheck.md:125` is
   `| operability | committed `w2/OperabilityNoHarm.md` | five assigned selftests exit 0 … |` inside the
   "No-harm checks" table (table header at :121); the per-axis table starts at :130 and its operability row is
   :134. A kind-5 scan keyed on `^| operability |` alone would read :125 as a verdict that disagrees with MANIFEST
   `unchanged`. The counter should scope kind 5 to the per-axis table (after the `| Axis | Verdict |` header) or it
   will report a spurious disagreement that no row can clear. Reported, not worked around in the row.
5. **Census claim is carried, not re-executed.** `census --selftest` PASS (134 cases) comes from
   `SCORECARD.md:1526` and `corpus/lessons/round-24-verifier-spotcheck.md:106`, which explicitly says "per the
   report (not re-run here)". I did not run the census.
6. **A2 substance is quoted, not re-measured.** "ten A2 rules pinned by 30 frozen cases, PASS 30/30" is from the
   round-28 spot-check line 93, which itself records evidence-verification rather than execution. I did not run the
   tool (wave-wide blindness) and only counted the fixture's cases from committed JSON bytes (30).
7. **Round-12 tabulated score is 6** (`SCORECARD.md:616`), consistent with the 6 → 7 move credited at round 13 and
   first admitted at round 14.
8. **MANIFEST shape.** `63729047` carries rounds 1–11 only as fleet-level `lanes.mori: "closed"`; rounds 12–28 are
   `lane: "mori"` entries with `admitted`, `verdict` and `verdicts`. All mori entries 12–28 have `claims: null`
   (checked), so no closure-stated scalar exists to adopt even if the policy allowed one.
9. **Round 17 states `7→7` twice** (`SCORECARD.md:1044`, `:1098`) and `7 held` once (`:1117`) across two instrument
   generations; the closure is `rejected-harmed`, so none is a basis.
10. **Elision convention:** `…` marks removed words inside a verbatim quote in §2; no verdict word is elided, and
    no quote is paraphrased inside quotation marks.

## 6. Findings summary

- **Behavior observed:** with the amended contract, the standing operability row fails two counted kinds as
  written — kind 2 (`Last change` opens `round 14`, R = 28) and A2 kind 2b (`round 14 (6 → 7)` against a round-14
  `unchanged` verdict). The score 7 itself has no basis to change. The row must cite
  `corpus/lessons/round-28-verifier-spotcheck.md:93` for kind 1 and carry `round 28 (improved, score held)`.
- **Gates:** none run by this seat. Not run and not claimed: the C1 counter (absent), census selftest, OOM module,
  retention scan, any wave-1 counter. Evidence only.
- **Touched surfaces:** this report.
- **Out of scope:** C2 case writing, counter authorship, the SCORECARD edit itself (L1 owns the cutover), lesson
  text, fleet files, allowlist/retention changes, the round-26 counter hazard's repair.
- **Artifact path:** `.ufo/waves/round-29/w1/AxisOperability.md`.
