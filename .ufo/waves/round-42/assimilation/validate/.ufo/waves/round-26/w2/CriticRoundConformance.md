# CriticRoundConformance — round-26 conformance attack (mori, wave 2)

Seat: `MoriR26.CriticRoundConformance` (critic, leaf). Target: lane tip `16935e24c93fa7e7567413d7ec091339a5df1474`,
read with git only. Rules attacked: `.ufo/prompts/mori-round-26.md` §2, §2b, §6.9 (fleet root) and
`.scratch/goal-20261022-hyaku-12h.md` sections "Quality bar" (lines 143-161) and "Drift sentinels" (lines 163-178).
Scratch: `/fast/scratch/hyaku/mori-r26/CriticRoundConformance/`. Tool installs or updates: none.

## Verdict summary

| Rule | Verdict |
|---|---|
| R-1 lowest-axis rule (§2 item 2) | pass |
| R-2 learning claim (Quality bar) | pass |
| R-3 sourced claim (§2b item 4) | pass |
| R-4 drift rule (different frontier area from the routed repair) | pass, with a risk for round 27 |
| R-5 claim sizing (§6.9) | pass, with a risk (A2 changed interface rules after landing) |
| R-6 causal separability (§2 item 3) | pass (tested in both directions) |
| R-7 routed R1–R8 disposition (fixed or named debt) | **fail at the tip (medium)**; curable in the report |
| R-8 commit timeline | pass on order; two provenance defects (low) |
| R-9 drift sentinels and seat mix | pass on the checks I ran; report-depth sentinel not run |

## R-1 Lowest-axis rule — pass

- Entering scores (`git show 248408f5:SCORECARD.md`, lines 10-15): coverage 6, operability 7, depth 5,
  freshness 5, calibration 5, adjacency 6. The lowest active score is 5 (depth, freshness, calibration tied).
- C1 targets freshness 5 (`SCORECARD.md:1597` at the tip; `contract.md:19`). AXES.md:14 defines freshness as
  "skill claims re-verified against live surfaces; stale items flagged or fixed", which is what C1 does.
- Note, not a defect: both claims propose a score delta of 0 ("freshness 5 → 5 held pending closure",
  `SCORECARD.md:1608`; "coverage 6 → 6", `:1609`). §2 item 5 asks for the delta; 0 is recorded honestly.

## R-2 Learning claim — pass

- C1 is "a stronger entry superseding a weaker one": `corpus/knowledge/userspace-oom-killers-r26.md` added in
  `327fbcca`; the r12 entry now names it 4 times (`count-c1.sh 16935e2` prints `r12_names_r26=4`).
- C2 is "a capability shown running and entered in SCORECARD's capability table": row at `SCORECARD.md:1616-1620`;
  live receipt `.ufo/waves/round-26/evidence/c2-live-run.txt` (updated in `c6ea248`). The tool sits in the
  lane's own province (FR10, `PROVINCE.md:53` at `248408f5`; detection and report only).

## R-3 Sourced claim — pass

- The r26 entry's `source:` line cites exactly S114–S126; the lesson Gate table (`corpus/lessons/round-26.md:65-79`)
  holds the same 13 ids, each with URL, access date 2026-10-22 and a located quote (set equality checked with
  `grep -oE 'S[0-9]{3}'` over both files at `16935e2`).
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok`, exit 0,
  six W04 duplicate-URL warnings on S035, S037, S073–S076 (rows older than this round). Working-tree
  `corpus/SOURCES.md` is byte-equal to the tip blob (`cmp` printed no difference).
- Risk (low): `count-c1.sh:14` counts "opened in round 26" as "numeric id above 113", not as "has a Gate row".
  It holds here only because the id set equals the Gate set. Smallest correction: none needed for admission;
  a later counter should join against the Gate table.

## R-4 Drift rule — pass, with a risk

- Rounds 23, 24 and 25 each counted a calibration routed repair as C1 (`SCORECARD.md:1426`, `:1505`, `:1545`);
  the round-25 spot-check says the sentinel tripped (`corpus/lessons/round-25-verifier-spotcheck.md:204-206`).
- Round 26 counts freshness (C1) and coverage (C2), both on FR10, and declares R1–R8 uncounted
  (`contract.md:16-17`). Different frontier area: holds.
- Risk A: coverage has been C2 for four rounds running with a new read tool each time and no score movement:
  FR2 quota (`SCORECARD.md:1427`), FR12 pressure (`:1506`), job runway (`:1546`), FR10 (`:1598`), all "6 → 6".
  The sentinel row is "same axis+surface", and the surfaces differ, so it does not trip.
- Risk B: the in-round retention-scan regression recurs: round 25 went 4 → 88 → 4
  (`round-25-verifier-spotcheck.md:90`), round 26 went 4 → 6 → 4 (`corpus/lessons/round-26.md:43-48`, M2). A third
  occurrence in round 27 would trip "same routed defect class in a lane 3 rounds running".

## R-5 Claim sizing (§6.9) — pass, with a risk

- One concrete value per claim, one command over committed bytes: I re-derived both at the tip.
  `count-c1.sh 16935e2` → `stale_present=0`, `r26_entry=present`, `r26_new_source_ids=13`, `r12_names_r26=4`, exit 0.
  `count-c2.sh 16935e2` → `freeze_order=ok`, `cases_changed_since_freeze=0`, `N=32`,
  `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`, `exit=0`. Same values as the measured commit `327fbcca`.
- No unenumerated universal clause: C1's "none of the four phrases" is the frozen list; C2's N/N is fixed at the
  freeze commit. Two claims, as preferred.
- No narrowing after landing on the counted values: A1 (`99338de`) only adds after-fields. Counterexample
  attempted: did A1 pick a counter that only the later tool passes? No: `count-c2.sh c2fdd92` (the blind-built
  first tool) already prints `PASS 32/32`, exit 0.
- Risk (low/medium): A2 changed binding interface rules after the tool landed. Original rule 1 (`contract.md:97`)
  makes any in-scope `sending SIG… to process` line positive evidence; A6 (`contract.md:166-167`) removes dry-run
  sends from it, and the 738eec1 bullet (`contract.md:175-179`) adds out-of-scope sends as positive evidence for a
  non-active earlyoom, against the original scope rule (`contract.md:78-79`) and rule 3 (`:102-104`). The counted
  value is unchanged, but the capability row (`SCORECARD.md:1620`, "as in contract C2 and amendment A2") now
  describes behaviour declared after landing. Smallest correction: the report states that the capability verdict
  covers post-A2 behaviour and that A2 changed rules 1 and 3; the closure judges the row against the tip tool.

## R-6 Causal separability — pass

- C2 without C1: at `c2fdd92`, `99338de`, `825f988` and `21386b9`, `count-c2.sh` prints `PASS 32/32`, exit 0, while
  `count-c1.sh` prints `stale_present=4`, `r26_entry=absent` (commands run per revision, outputs above).
- C1 without C2: sandbox clone at `16935e2` plus one scratch commit removing `tools/mori-oom-killers.py` and
  `tools/fixtures/mori-oom-killers/` (scratch clone `.../CriticRoundConformance/sep`, lane untouched; counters copied
  with only `L=` repointed). C1 still prints `stale_present=0`, `r26_entry=present`, `r26_new_source_ids=13`,
  `r12_names_r26=4`, exit 0; C2 fails with `exit=2` (tool file missing).

## R-7 Routed R1–R8 disposition — fail at the tip (medium)

The spot-check says "the lane fixes these in round 26" (`round-25-verifier-spotcheck.md:172`). The contract and
SCORECARD say only "hygiene or named debt" as a blanket clause (`contract.md:16-17`, `SCORECARD.md:1593`). No file
at the tip gives a per-item disposition (`git grep -E '\bR[1-8]\b'` over LOG, SCORECARD, SKILL, lesson, QUALITY,
README, PROVINCE and the contract finds only R5 and R8). Diff `248408f5..16935e2` (stat, wave reports excluded)
touches none of the files that R1, R3, R4, R6 and R7 name.

| Item | State at the tip | Evidence |
|---|---|---|
| R1 runway false numbers, tool hardening | not fixed, not named | `tools/mori-job-runway.py` absent from the round diff stat |
| R2 SCORECARD runway capability overclaim | not fixed, not named | phrase "never turns an unreadable" still at `SCORECARD.md:1568` |
| R3 SKILL round-25 block rows 1-4 | not fixed, not named | row 2 text "while the cap was full … nothing" still at `SKILL.md:659`; SKILL diff has no removed lines |
| R4 SCORECARD calibration residuals | not fixed, not named | SCORECARD diff is +37 lines, all inside the round-26 sections |
| R5 gate conformance | partly fixed: registry rows added (`SKILL.md:712-718`); routed-check self-test and fail-open paths not fixed, not named | `tools/mori-routed-r24.py` absent from the diff stat |
| R6 round-25 lesson wording | not fixed, not named | `corpus/lessons/round-25.md` absent from the diff stat |
| R7 knowledge corrections | not fixed, not named | `harness-job-capacity-r25.md`, `system-pressure-r24.md` absent from the diff stat |
| R8 retention scan at every candidate tip | fixed | scan 4 at `4dba9cc7` (`SCORECARD.md:1622`); M2 fix `58540501` (`round-26.md:43-48`) |

Aggravating fact: wave-1 scribes drafted byte-exact corrections for R2, R3, R4, R6 and R7
(`.ufo/waves/round-26/w1/DraftHygieneScorecard.md:3,34-119`, `DraftHygieneKnowledge.md:1-5,160-216`) and
`ReviewHygieneDebt.md:1-161` classified R1–R8; none of the drafts landed and none is cited as debt.
§6 item 5 allows "or say in the report why not", so the report can still cure this. Smallest correction: land the
prose drafts (R2, R3, R4, R6, R7 are prose) or add one disposition line per item with a pointer, in the lesson and
the report; R1 and the R5 code half named as debt with the reason.

## R-8 Commit timeline — pass on order; two low defects

- Order: `git log 28b0494^..16935e2` is linear: contract `28b0494` → declaration `5e5e86f` → cases `5b10649` → tool
  `c2fdd92` → A1 `99338de` → tool fix `278f02e` → A2 `825f988` → captures `b4473ed` → allowlist `5854050` → tool
  `93aa1b9` → tool `738eec1` → supplementary `21386b9` → C1 content `327fbcc` → `4dba9cc` → `c6ea248` → `2ecb661` →
  `16935e2`. The counted freeze order (cases strict ancestor of tool) holds (`freeze_order=ok`).
- Byte identity with the seat sandboxes: cases blob `5b4dcee7…` equals sandbox `eaa13ef` in `wt-cases`; tool blob
  `0df359bc…` equals sandbox `74df6f5` in `wt-tool`. The tool sandbox tree holds no cases file (`ls-tree` count 0).
- Observation: both sandboxes branched from `28b0494` and ran in parallel (cases committed 10:18:00, tool 10:18:29);
  the lane freeze order is the L1's integration order. A1 already demotes blindness to a process fact
  (`contract.md:147-148`); git cannot show whether the tool seat read the sibling sandbox [INFERENCE].
- Defect T1 (low, false provenance): the case seat's report, which the lane cites for independence, names a
  different freeze. `w1/WriteOomKillersCases.md:8-22` calls `da9af118` (sha256 `277684eb…`) "the freeze tip" and says
  "No tool existed when either amendment was made". Its amendments `4447597` (10:20:31) and `da9af11` (10:38:21)
  both come after the tool (`74df6f5` 10:18:29; lane `c2fdd92` 10:20:00). The lane correctly counts the original
  file (sha256 `84d2343f…`) and moved the amendments to the uncounted supplementary file (`278f02e`, `21386b9`), but
  neither the lesson nor SCORECARD says so; only commit subjects do. The counted 32 include c19, c24 and c28, which
  the case seat later withdrew for band size, not as wrong (`WriteOomKillersCases.md:225-230`). Smallest correction:
  one sentence in the lesson and report naming the counted sha and why the seat's "freeze tip" is not it.
- Defect T2 (low): A2 is not one amendment. Its heading is dated "after the tool landed", but its text grew in
  three commits (`825f988`, then `93aa1b9` adding "Unbounded invocation", then `738eec1` adding "Earlier
  invocations"), and the malformed-timestamp tool change it adopts landed earlier in `278f02e`. The lesson cites
  "amendment A2" as one event (`round-26.md:4-5`). Smallest correction: tag each A2 bullet with its commit.
- Holds: `278f02e` also changed the self-test harness after the freeze (a setup error is now graded as
  `KILLERS_UNKNOWN`, exit 2, instead of failing the case). No inflation: the pre-change tool `c2fdd92` already
  passes 32/32 under `count-c2.sh`.
- Holds: A1 "before any C1 after-measurement": C1 content first appears in `327fbcc`; every earlier revision prints
  `stale_present=4`, `r26_entry=absent`.
- Observation: commit times are not evidence. `28b0494` has author time 09:28:23 and committer time 10:10:20, and
  `5b10649`, `c2fdd92`, `2ecb661` and `16935e2` carry author times on whole minutes. Only ancestry supports the order.

## R-9 Drift sentinels and seat mix (Quality bar)

- Seat mix: wave 1 has 35 seats (3 critic, 2 mutation-tester, 6 reviewer = 11 attack, 31%); wave 2 has 34 (6 critic,
  5 mutation-tester, 22 reviewer = 33 attack); round total 69 ≤ 100, attack share 44/69. Pass (≥25%).
  Source: `jq` role counts over `wave1-spec.json` and `wave2-spec.json` at `16935e2`.
- Executors only for code: the 3 wave-1 executors are BuildOomKillersTool (tool), WriteOomKillersCases (fixture) and
  HostCapture (capture script). Pass.
- Run-together token: the new heading `### Round26 registry additions` (`SKILL.md:712`, from `327fbcc`) copies the
  older `Round24 registry additions` (`SKILL.md:637` at `248408f5`). SKILL.md is neither a report nor the ledger, so
  the sentinel does not trip; risk (low).
- Not run: report-depth sentinel (the round report is not written yet), dead-seat share (no seat-death data read),
  "2 consecutive rejections" and "first 4 closures" (closure state is outside the lane tip).

## Commands run (all read-only in the lane)

`git log`, `git show`, `git diff --stat`, `git grep`, `git ls-tree`, `git rev-parse` in the lane;
`bash .ufo/waves/round-26/count-c1.sh <rev>` and `count-c2.sh <rev>` for the revisions named above;
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`; `git log`/`rev-parse` in the
`wt-cases` and `wt-tool` sandboxes; one scratch clone with one scratch commit under my scratch directory.
