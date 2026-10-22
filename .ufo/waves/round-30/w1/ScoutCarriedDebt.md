# ScoutCarriedDebt — round-30 inventory of carried debt

Seat: MoriR30.ScoutCarriedDebt (scout, leaf; no subagents, no background jobs). Question: for each item of the
round-29 named debt (`corpus/lessons/round-29.md:163-175`) and each routed defect R1–R7
(`corpus/lessons/round-29-verifier-spotcheck.md:152-166`), its status at the entering tip `58b6168` with proof, and
whether the round-30 contract (`.ufo/waves/round-30/contract.md`) covers it as a claim, as routed hygiene, or not at
all; plus what is stale in `SCORECARD.md` `## Planned` (`:27-30`) and `## Saturation` (`:594-596`).

Method and basis. Read-only git in the lane (show, rev-parse, log, grep, ls-tree, cat-file); Python reads of committed
fixture bytes; two runs of committed shell checks; the oom-killers tool run only through `--selftest` on committed
fixtures. Lane HEAD at read time was `e936482a6070db40049bff46f7da4754b15d41af`. `git diff --stat 58b6168..HEAD`
reports only `LOG.md` (+16) and `SCORECARD.md` (+14), so `tools/`, the fixtures, `corpus/`, `SKILL.md` and `PROVINCE.md`
are byte-identical to the tip: a run at HEAD reproduces the tip's tool and fixture state. Nothing was written outside
this file and `/fast/scratch/hyaku/mori-r30/ScoutCarriedDebt/gate.txt`. No writer was messaged; no lane tool source
line is quoted here.

Coverage vocabulary: **claim** = a counted condition in the contract; **hygiene** = `## Routed hygiene`
(`contract.md:111-119`), explicitly never a counted claim; **not covered** = no contract line routes the item.

## 1. Round-29 named debt (`corpus/lessons/round-29.md:163-175`)

| # | item | status at 58b6168 | proof | coverage |
|---|---|---|---|---|
| N1 | rule-text amendments before any writers (`:165-167`) | **open** | `.ufo/waves/round-30/rule-text.md:1-3` is a verbatim extract (round-26 contract `:58-110`, `:152-190`; round-27 `:47-58`), not an amendment block. No clause on a stopped unit's retained stamp (`grep -i "stopped\|retained"` → 0 hits). The `dryrun` field is listed at `:41` with no meaning; `actions: null, never zero counts` is inherited at `:49`, the unbounded definition (A2-05) at `:109`, the lost-evidence rule (A2-10) at `:111` | **not covered**: the contract names the writers' extract once (`:81-83`) and never routes an amendment |
| N2 | three `CaseA210c` cases stay frozen (`:168`) | **open** (frozen, failing) | `python3 -I -B tools/mori-oom-killers.py --selftest --cases tools/fixtures/mori-oom-killers/cases-a2-r29.json` → `FAIL 21/24`, exit 1; the three failing ids are exactly the three authored at `.ufo/waves/round-29/w1/CaseA210c.md:8,43,82` (`r29-a2-10-inactive-lone-missing-stamp`, `r29-a2-10-failed-stamped-positive`, `r29-a2-10-not-found-earlier-stamped-positive`); file blob is `cc309d8e30ca…` at both `58b6168` and the freeze `d6d5cb0a` (`git rev-parse`) | **claim C2.1** (`contract.md:60-61`) |
| N3 | A2-07 shape with a non-active unit; `ScoutShapeCoverage` gaps (`:169`) | **open** | all 15 A2-07 cases are `ActiveState=active` (3 in `cases-a2.json`, 12 in `cases-a2-r29.json`; Python scan of committed fixtures, 0 non-active); `.ufo/waves/round-29/w2/ScoutShapeCoverage.md:74-75` records 0/12 non-active, `:76-99` eleven A2-07 gaps, `:101-124` eleven A2-10 gaps | **not covered**: C2.3 pins an active-only shape (`contract.md:64-66`) |
| N4a | C1 counter hole — kind-2 round control, negated prose (`:170`) | **open** | `.ufo/waves/round-29/w2/MutCountC1.md:20` mutant 7 survived (coverage prose claiming "not improved"), `:23` mutant 10 survived (false `(improved, score held)`); the code path is `.ufo/waves/round-29/count-c1.sh:166-176` | **not covered**: C1 (`contract.md:25-42`) declares a new counter with no last-change or round-verdict input; the round-29 script is untouched and unnamed |
| N4b | blind-gate heading grammar and bare `exit N` false positives (`:170-171`) | **open** | `bash .ufo/waves/round-29/check-blind-wave.sh d6d5cb0a .ufo/waves/round-29/w1 '^CaseA2(07\|10)[a-d]\.md$'` → `blind_violations=20`, exit 1, 20 violation lines; adjudication `.ufo/waves/round-29/w2/AdjudicateBlindHits.md:3-5,20` | **claim C2.4** (`contract.md:75-80`) |
| N4c | `count-c2.sh` runs the gate at the passed rev, not the freeze commit (`:171`) | **open** | `.ufo/waves/round-29/count-c2.sh:189` calls the gate with the passed `rev`; the freeze commit is computed separately at `:62-73`, `:185` | **claim C2.4** (requires the freeze commit) |
| N5 | round-28 carried debt (`:172-174`) | **open**, every sub-item | see §1.1 | **not covered**: contract greps for `MutCountC1`, `MutHeadingCheck`, `S146`, `used-by`, `reader-sweep` are all 0 |
| N6 | stale `## Planned` and `## Saturation` text (`:175`) | **open** | see §3 | **not covered**: contract greps for `Planned` and `Saturation` are 0 |

### 1.1 N5 sub-items (all open at 58b6168)

- **MutCountC1 F1** — `.ufo/waves/round-28/count-c1.sh:12` hardcodes `LANE` and `:25,28` runs the fetched check
  unmodified; the check carries its own path at `.ufo/waves/round-27/check-row-identity.py:19`. `git log
  7118f320..58b6168 -- .ufo/waves/round-28/count-c1.sh .ufo/waves/round-27/check-row-identity.py` → 0 commits.
- **F2** — `check-row-identity.py:37` strips cells and `:74` compares the stripped values; unchanged.
- **F3** — `count-c1.sh:36-40` scans every line of `corpus/SOURCES.md` with no `## Registry` bound; unchanged.
- **F6** — `count-c1.sh:51,56` read only `r[7]` teaches, `r[8]` status and `r[11]` used-by; source, anchor and
  opened cells are never inspected; unchanged.
- **F10** — `check-row-identity.py:22` exempts status, recheck and used-by from the `:74` comparison; the carried
  warning that the stated fix would red the real tree stands (`.ufo/waves/round-29/w1/ScoutCarriedDebt.md:97-105`).
- **S146 `teaches`** — `corpus/SOURCES.md:152` still says S097 "stated no flip at all" and calls S001 "the rendered
  page", while S097's own cell at `:103` begins `REJECTED: … flip:` and cites S001 for the same psi.rst lines.
- **reader-sweep ranges** — the four sites are unchanged: `corpus/knowledge/harness-job-capacity-r25.md:3` and
  `:232`, `SKILL.md:646`, `PROVINCE.md:318` still "re-open" `S098–S103`, `S112–S113` and `S138–S141`.
- **"opened this round" dating** — `PROVINCE.md:257` places `(S090–S095, S145)` inside the round-24 landing;
  `PROVINCE.md:318` names only S098–S103 and S112–S113 although the entry also rests on S147 (see
  `.ufo/waves/round-29/w1/ScoutCarriedDebt.md:147-162`).
- **old rows' `used-by`** — S096's cell names `corpus/knowledge/system-pressure-r24.md`; `git grep -c -w -F S096
  58b6168 -- corpus/knowledge/system-pressure-r24.md` exits 1 with no output. The predecessor counted 8 stale cells
  (`.ufo/waves/round-29/w1/ScoutCarriedDebt.md:24,163-191`).
- **r25 R1 residuals** — `tools/mori-job-runway.py` is unchanged since `7118f320` (0 commits). The empty-string
  `--cases` fallback survives at `:519`; no regular-file guard exists (grep for `S_ISREG`, `isfifo`, `st_mode` → 0
  hits); `main` (`:666`) wraps only `parser.parse_args`, and `evaluate` is called outside the guard.
- **r25 R5** — `tools/mori-routed-r24.py:896-901` declares only `--repo`, `--rev`, `--rerun` (no `--selftest`), and
  the expected self-test bytes remain constants at `:96,98`; unchanged since `7118f320`.
- **`MutHeadingCheck.md` `--follow`** — `.ufo/waves/round-28/w2/MutHeadingCheck.md:64-65` still asserts `--follow`
  does not help; the erratum reproduces a hit on git 2.56.0 (`39434eaa…`) at
  `.ufo/waves/round-29/w1/ReviewLateMutHeadingCheck.md:67-72`; the round-28 file is unchanged.

## 2. Routed defects R1–R7 (`round-29-verifier-spotcheck.md:152-166`)

| R | status at 58b6168 | proof | coverage |
|---|---|---|---|
| R1 | **open** | `bash .ufo/waves/round-28/check-tip-receipts.sh b581173a 29` → `tip_receipts=unmet`; `cited_lane=no` for `count-c1.sh` and `count-c2.sh` (retention is `cited_lane=yes`). The two receipts are cited only at `SCORECARD.md:1796-1797`; `git show 58b6168:LOG.md` and `:corpus/lessons/round-29.md` each hold 0 mentions of `tip-c1.txt\|tip-c2.txt` | **hygiene** (`contract.md:113-115`) |
| R2 | **open** | `corpus/lessons/round-29.md:65` rejects S155 with "returned no line in either file" while the same row quotes `kill.h:36-37` (`/* Flag --dryrun was passed */`, `bool dryrun;`); no correction is appended anywhere at the tip | **hygiene** (`contract.md:116-117`) |
| R3 | **open** | the two labels are one high: `round-29.md:60` says "(11 words)" for a quote `wc -w` counts as 10, and `:62` says "(17 words)" for one counting 16 | **hygiene** (`contract.md:116`) |
| R4 | **open** | three failing ids as in N2; Judge02's case `r29-a2-07-dryrun-then-real-missing-enter` (`.ufo/waves/round-29/w2/Judge02.md:1`) passes at the tip but its `earlyoom.dryrun` field is ruled `unclear text` at `Judge02.md:37,43,64` — the case passes while the field's meaning stays undefined | **C2.1** covers the three failing ids; **the Judge02 half is not covered** — no contract line resolves the ruling, and the mismatch-judging clause (`contract.md:97-99`) applies only to the new blind file |
| R5 | **open** | same run as N4b: `blind_violations=20`, exit 1, all 20 adjudicated false positives (`AdjudicateBlindHits.md:3-5,20`) | **claim C2.4** (`contract.md:75-80`) |
| R6 | **open** | 0 cases match the disputed shape (active, stamp absent or `0`, ≥2 version lines, a real send before the last version line, none after) in `cases.json` (32), `cases-supplementary.json` (32), `cases-a2.json` (30) and `cases-a2-r29.json` (24); a Python scan of committed fixtures returns 0. `tools/fixtures/mori-oom-killers/cases-a2-r30.json` is absent at `58b6168` and at HEAD (`git cat-file -e` fails) | **claim C2.3** (`contract.md:64-74`) |
| R7 | **open** | `PROVINCE.md:25` still says "(round-16 build; verification pending"; "admission pending" survives at `:236`, `:294`, `:359`, `:375`; the file blob is identical at `7118f320` and `58b6168` (`00b34504…`), so the carried pointer `:32` does not resolve to the phrase — re-derive it as `:25`. `SKILL.md:661` cites `contract.md:83-84` with no directory | **hygiene** (`contract.md:119`) |

## 3. `SCORECARD.md` stale text

`SCORECARD.md` at HEAD differs from `58b6168` only by the round-30 declaration appended at `:1801-1814`
(`git show e936482 -- SCORECARD.md`), so both sections below are unchanged at the tip and at HEAD.

- **`## Planned` `:27-30`** still reads "Round 2: land one note per surface family and the first watch receipts, and
  add the `progressing-weak` authorship proof." The lane is at round 30 (`:1801`), and the coverage Axes row already
  cites the round-2 note `corpus/knowledge/observability-surfaces-r2.md` (`:11`), so at least the first half is long
  delivered. Nothing records completion or retirement.
- **`## Saturation` `:594-596`** still says the saturation line and stagnation window "are to be declared by the lane
  on its next round …; not asserted by this conformance change", while a declaration already exists at `:637-641`
  (line 8/10 on each owned axis, N = 3, round 12). The section sits inside the rounds 2–11 block that ends at
  `:581-584`; it reads as a live instruction and contradicts `:637`.
- **Adjacent staleness, not in the named debt**: `## Capabilities` `:586-592` still shows "— none yet —", and `:97`
  says "not three blocked rounds and not saturation". [INFERENCE] Both are the same class of leftover as `:594-596`,
  but the named debt does not route them.

## 4. Live obligations observed for the L1 (outside the assigned question)

- At HEAD `e936482`, `.ufo/waves/round-30/count-c1.sh`, `count-c2.sh` and `check-blind-wave.sh` are all absent
  (`git cat-file -e HEAD:<path>` fails); `.ufo/waves/round-30/evidence/` holds only `census-start.txt`; and
  `corpus/lessons/round-30.md` does not exist. The contract and `SCORECARD.md:1810-1811` point at
  `evidence/c1-before.txt` and `c2-before.txt`, so the counters and their `58b61681` before-receipts must be
  committed before the entry, source rows or any case file can carry the declared before-value.
- `check-tip-receipts.sh` matches receipts by file base name in `LOG.md` and the lesson; both currently hold zero
  mentions of the two counter receipts, which is exactly R1's remedy.

## 5. Observed facts, inference, unresolved gaps

Observed: every status above, each with the path:line or command shown; the only non-read commands were the oom
self-test on committed fixtures, the round-29 blind gate, the tip-receipt check, and `git grep`/`rev-parse`.
Inference: (i) the new C1 counter cannot reproduce the old kind-2 hole because its declared conditions consume no
last-change or round-verdict input, but this is contract text only until the script is committed; (ii) the
`## Capabilities` and `:97` phrasing is stale in the same way as `:594-596`.
Unresolved: (a) the round-30 counter bytes do not exist yet, so no behavioural claim about them can be checked;
(b) whether the L1 will treat Judge02's `unclear text` as part of C2 or as an unwritten rule-text amendment — the
contract routes neither, and N1(c) names the same `earlyoom.dryrun` meaning as the amendment that would settle it.

Tooling: no installs or updates, no pacman transaction attempted (host-wide pause respected). Used git 2.56.0
(read-only), bash, and Python 3.14.8 with `python3 -I -B`. `python3 -I -B tools/mori-oom-killers.py --selftest` was
run only on committed fixtures, as the contract allows for counters.

Report: .ufo/waves/round-30/w1/ScoutCarriedDebt.md
