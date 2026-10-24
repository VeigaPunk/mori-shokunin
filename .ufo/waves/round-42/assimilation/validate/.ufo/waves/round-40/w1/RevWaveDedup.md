# RevWaveDedup — round-40 wave-1 item dedupe (mori-r40-w1)

Seat: reviewer (leaf, read-only), `RevWaveDedup`, item 34 of 66.
Wave spec: `.ufo/waves/round-40/w1-spec.json` (66 items, `maxLanes` 66;
generated 02:54:09, committed at `8d3badd`). Scored tip
`265a955cc67be4eae97d2dc5a9338a25f31eb29b`; worktree HEAD at review time
`ede486b7a09afbacfb380d5871c46a8051a6dc2e`.
Date: 2026-10-24. No production edits; this report is the only lane write.
No tool installs (nothing needed).

Dedupe criterion used, exactly as tasked: an item is a **true duplicate** only
when it shares **both** the target (the claim/receipt/artifact it attacks) and
the method (the operation it performs) with another item. A shared target with
a different method is a complementary split, not a duplicate; a shared method
on a disjoint target is likewise not a duplicate. Padding is reported in two
senses because the strict one has no hits: (a) no resolvable evidence target,
(b) zero-yield — a resolvable source but no new target because the artifact is
already landed.

## Tooling note (lsp)

No `lsp` device exists in this seat's inventory (`read`, `bash`, `edit`,
`eval`, `glob`, `grep`, `task`, `wait`, `web_search`, `write`, `yield`; `xd://`
devices present: `ast_edit`, `debug`). Caller/definition/diagnostic checks were
therefore done over git objects, the committed receipts, and live read-only
runs. The unavailability is recorded; grep/git output below is not presented as
semantic proof.

## Commands run and decisive outputs

Working directory `/home/vgpnk/Projects/shokunin/mori-shokunin` unless absolute.

1. Wave inventory (JSON parse of `w1-spec.json`):
   `items 66 maxLanes 66`; roles
   `{'connector': 2, 'executor': 18, 'scribe': 6, 'scout': 6, 'simplifier': 2, 'reviewer': 16, 'critic': 9, 'mutation-tester': 4, 'sentinel': 2, 'revenger': 1}`.
   The role subset that sums to the SCORECARD's stated 32
   (reviewer+critic+mutation-tester+sentinel+revenger) = 32/66 = 48.5%,
   matching `SCORECARD.md:2258`.

2. Lane line, live run at the scored tip:
   `python3 tools/mori-sources-appendonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo . | grep '^supersede_timing'`
   → `count= 35`
   `supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]`

3. Receipt parse (Python regex over the three receipts):
   - `c11-after-lane.txt` → `as_of_count= 35`, `stale= []`, `S226_in_asof= True`
   - `c11-before-lane.txt` → `as_of_count= 18`, `stale= []`, `S226_in_asof= False`
   - `c11-after-e37dcc6.txt` → `as_of_count= 33`, `stale= ['S069']`
   (33 + S069 = 34 total superseded at e37dcc6; that is the only place a
   "34" is arithmetically derivable.)

4. Gate selftest:
   `python3 tools/mori-sources-appendonly.py --selftest`
   → `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, `EXIT=0`.
   The whole stdout is those two lines — no per-arm PASS lines (the code prints
   `FAIL <name>` only on failure and one summary line:
   `tools/mori-sources-appendonly.py:843,876`).

5. Tenth generated fixture alone (it is the multicounter second counter):
   `python3 .ufo/waves/round-40/conform.py 265a955cc… --counter .ufo/waves/round-40/fixtures/generated/survivor-barecomm.py`
   → `check drain_bind FAIL …`, `check timeout_state FAIL (exit=None …)`,
   `check selftest_conjunct FAIL …`, `CONFORM=unmet`, `EXIT=1`,
   wall 25.20 s. No `c10-after-barecomm.txt` / `c10-red-barecomm.txt` exists
   (`ls .ufo/waves/round-40/evidence/ | grep -i barecomm` → empty).

6. Counter-of-record replay today:
   `python3 .ufo/waves/round-40/conform.py 265a955cc… --counter .ufo/waves/round-40/count-c8.py`
   → `check head_pin PASS (pin=ede486b7… tip=ede486b7…)`, `CONFORM=met`, `EXIT=0`.
   The committed `c10-after.txt:4` says `pin=265a955cc… tip=265a955cc…`.
   `conform.py:517-525` resolves `pin` from the counter's `--pin-only` (live
   worktree HEAD) and `tip` from `git -C <repo> rev-parse HEAD`, so the after
   receipt is only byte-reproducible at the T1 worktree.

7. Landed-artifact timestamps:
   `git log -3 --format='%h %cI %s'` →
   `ede486b 2026-10-24T02:56:56-03:00 …`, `8d3badd 2026-10-24T02:56:11-03:00 …`,
   `265a955 2026-10-24T02:47:29-03:00 …`.
   `stat -c '%y %n' /home/vgpnk/Projects/shokunin/.ufo/reports/round-40/mori.md`
   → `2026-10-24 02:57:46`.
   `git -C /home/vgpnk/Projects/shokunin log -1 --format='%h %cI %s' -- .ufo/reports/round-40/mori.md`
   → `22fc3dd 2026-10-24T02:57:50-03:00 round-40: mori report`.
   Headings in that report: `10:## Work performed`, `51:## Landed changes`,
   `127:## SHONEN`, with four lines `129/132/134/136`.
   `git show --name-only 8d3badd | grep -E 'SCORECARD|LOG.md|round-40.md'`
   → `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-40.md` all landed there.

8. Erratum / append-only:
   `git diff --stat bb1f2457..HEAD -- .ufo/waves/round-39 corpus/lessons/round-39.md corpus/lessons/round-39-verifier-spotcheck.md`
   → empty (r39 files untouched).
   `ls .ufo/waves/round-38/evidence/c8-red-wait.txt` → **No such file**.
   `find .ufo/waves/round-39 -name 'c8-red-wait*'`
   → `.ufo/waves/round-39/evidence/c8-red-wait.txt`; `cat` it →
   `exit=1`, `check bounded_reads FAIL`, `CONFORM=unmet`,
   `verdict: not reproduced`.

9. Contract evidence list vs disk:
   `sed -n '151,152p' .ufo/waves/round-40/contract.md` →
   `evidence/freeze-r40.txt`, `evidence/census-start.txt`, `census-end.txt`,
   `evidence/c10-red-*.txt`, `c10-after*.txt`, `evidence/c11-red-*.txt`,
   `c11-before-lane.txt`, `c11-after*.txt` — a glob list, not an enumeration.
   `ls .ufo/waves/round-40/evidence/` shows `c10-parity.txt` and
   `wave-plan.txt` present but not named by those globs; `.parity-c7.txt` /
   `.parity-c8.txt` are hidden and also unnamed.

10. Parity receipt (`cat .ufo/waves/round-40/evidence/c10-parity.txt`):
    one seed (`seed 20261024`), `count-c7 sha256: b92c65f2…`, `c8_exit=0`,
    `PARITY: receipts byte-identical`; **no count-c8 sha256**.

11. Census receipts: `wc -l census-start.txt census-end.txt` → 17 / 17;
    each is 16 `W04` rows + `mori ok <path>`; no `command:` line, no `EXIT=`.

12. Receipt inventory: `c10-red-*.txt` = 9 survivor reds + `multicounter` +
    `conjunct`; `c10-after-*.txt` = 9 survivor afters + `multicounter` +
    `conjunct` + `selftest`; `c11-red-*.txt` = `neveredited`, `firstparent`,
    `readd`.

## Inventory and grouping by claim/receipt

All 66 items are grouped below by the primary claim/receipt they attack. Items
listed in two groups attack two artifacts; they are not thereby duplicates.

| Group | Target / receipt | Items (number — seat) | Method |
|---|---|---|---|
| G1 | C1 after counter-of-record + parity (`c10-after.txt`, `c10-parity.txt`, conform bytes) | 3 ExeConformMet, 4 ExeConformSelftest, 12 ExeParity, 32 SimpConformV3, 42 RevConformDiff, 48 RevParityScope, 37 CritExploratoryBoundary, 58 CritScoringHonesty | replay/diff; line accounting; hunk classification; parity review; separability runs; number re-derivation |
| G2 | C1 survivor / multicounter / conjunct receipts (`c10-red-*`, `c10-after-*`, conform selftest) | 11 ExeSurvivorSweep, 17 ExeConjunctAfter, 39 RevC1Receipts, 44 RevScorecardClaims, 51 CritNewSurvivor, 55 CritConjunctSemantics, 56 CritDrainedTuple, 62 MutConformArms | sweep replay; gutted-copy replay; receipt discipline; control coverage; new fixture; semantic attack; tuple-swap fixture; checker mutation |
| G3 | C2 lane line + e37 (`c11-before-lane.txt`, `c11-after-lane.txt`, `c11-after-e37dcc6.txt`) | 6 ExeGateLane, 7 ExeGateE37, 21 ScrScorecardRow, 40 RevC2Receipts, 53 CritLaneLine, 54 CritPredParenthetical, 58 CritScoringHonesty | gate replay; sampled id audit; parenthetical attack; record draft; receipt discipline |
| G4 | C2 DAG fixtures + gate selftest (`c11-{red,after}-fixture-{n,p,r}.txt`, `c11-after-selftest.txt`) | 5 ExeGateSelftest, 8 ExeDagN, 9 ExeDagP, 10 ExeDagR, 16 ExeDagDeterminism, 31 SimpGateV3, 41 RevGateDiff, 52 CritNewDag, 59 MutGateReadd, 60 MutGateEligible, 61 MutGateFirstParent, 66 LabDagDeterminism | replay; repeat-build determinism; dead-code read; hunk classification; new DAG; three branch mutations |
| G4b | Wave `mechanicalMs` budget (both selftests; no receipt) | 38 ExeSelftestTiming | timed run of conform + gate selftests |
| G5 | Freeze / before-bytes / witness provenance (`freeze-r40.txt`, `fixtures/extracted/`, `witness-*`) | 14 ExeWitnessBytes, 15 ExeExtractPins, 18 ExeFreezePins, 39 RevC1Receipts, 49 RevFreezeHonesty, 57 CritFreezeTiming | sha256; git-show equality; freeze-note review; commit-order proof |
| G6 | Census / frontier / S229 / sources (`census-*.txt`, `SOURCES.md`, README, QUALITY, knowledge, lesson Gate) | 1 ConnSiblingOverlap, 2 ConnW04Routing, 13 ExeCensus, 23 ScrSourcesRow, 27 ScoutCorpusFrontier, 28 ScoutQualityBar, 29 ScoutSiblingConform, 35 RevLessonGate, 43 RevContractConformance, 46 RevKnowledgeProvenance, 50 RevCensusPair | sibling grep; census replay; row verification; provenance/criterion review |
| G7 | Contract claims / routed coverage / path set | 26 ScoutInstrumentLayout, 33 RevFindingsCoverage, 36 RevRoutedCoverage, 37 CritExploratoryBoundary, 43 RevContractConformance, 44 RevScorecardClaims | set comparison; mapping; separability; control coverage |
| G8 | Erratum `corpus/lessons/round-39-erratum.md` | 24 ScrErratumCheck, 45 RevErratum | sentence-vs-source verification (24); append-only + sentence verification (45) |
| G9 | Report / record drafts / SHONEN | 19 ScrReportWork, 20 ScrLandedChanges, 21 ScrScorecardRow, 22 ScrLessonDraft, 47 RevShonenBoxes, 58 CritScoringHonesty | drafting/review against landed records |
| G10 | Instrument static review | 31 SimpGateV3, 32 SimpConformV3, 41 RevGateDiff, 42 RevConformDiff | dead-code / line-accounting / hunk classification |
| G11 | Prior waves and history | 25 ScoutPriorWaves, 30 ScoutDriftProbe, 65 RevPriorIntent | report recon; git history; archaeology |
| G12 | Security | 63 SentArtifactSafety, 64 SentToolingBounds | artifact scan; prompt-bound scan |
| — | self | 34 RevWaveDedup | this report |

Every number 1–66 appears at least once above. Deliberate complementary splits
(not duplicates): 8/9/10 (one DAG each), 59/60/61 (one gate branch each),
39/40 (c10 vs c11 receipt sets), 41/42 (gate vs conform diff), 2/13/50 (census
read, census re-run, census pair), 4/5 (conform vs gate selftest).

## Findings (by severity)

### F1 — HIGH: five items and three landed records embed a lane-line count that the receipts contradict (35, not 34)

The measured `superseded_as_of` at T1 is **35 ids** (command 2 and 3 above;
`c11-after-lane.txt` itself lists 35). The wave context, `SCORECARD.md:2234`,
`LOG.md:2296`, and `corpus/lessons/round-40.md:24` (M24) all say **34**; M24's
arithmetic `"16 rows: S226 plus 15 earlier"` counts 16 newcomers, but the
receipt adds **17** (S226 + the 16 never-edited ids S067, S070, S071, S083,
S084, S090, S093, S096, S097, S101, S124, S127, S128, S129, S131, S140):
18 edit-bounded + 17 = 35. The only derivable 34 is the e37dcc6 total
(33 as-of + S069 stale).

Items that bake in 34 and therefore cannot pass as written:

- **6 ExeGateLane** — "verify the `supersede_timing` line lists **34** as-of
  ids including S226 with stale empty"; the line lists 35, so a literal check
  reports a false mismatch (the receipt comparison itself would show no id
  difference).
- **21 ScrScorecardRow** — "mark the measured **34-id** lane line" (and it is
  already landed; see F4).
- **53 CritLaneLine** — "of the **34** as-of ids … pick 5 at random"; the
  sample frame is off by one.
- **54 CritPredParenthetical** — "prove from the committed receipts that the
  measured value is **34**"; the receipts prove 35. The independently written
  neighbour `w1/CritPredParenthetical.md` also measured 35 ("19 predicted + 16
  missed = 35"), so this is not a seat disagreement — the prompt's acceptance
  value is false.
- **58 CritScoringHonesty** — its number list includes 34; a one-command
  re-derivation will flag SCORECARD's 34 as unsupported (correctly).

Recommendation: correct the premise to 35 in the dispatch/report records
(contract after-cell still says 19; SCORECARD/LOG/M24 say 34), and tell 6/21/53
the measured value before they run. This is a claim-sizing defect of the
correction, not of the gate's semantic sentence: the gate line is internally
consistent (35 as-of, stale empty, `superseded` = 35).

### F2 — MEDIUM: one true duplicate — `16 ExeDagDeterminism` and `66 LabDagDeterminism`

Both build the P-C11 fixtures through the same builder
`_make_dag_repo` (`tools/mori-sources-appendonly.py:626`; `run-c11-dags.py:50`
uses it) in isolated `.scratch` dirs and compare the named shas and final
registry bodies for byte-identity. `16` builds dag-n/p/r twice; `66` builds
**dag-p** five times under a conflicted-index-leak hypothesis. The overlapping
case is identical (dag-p repeat-build comparison); `66` adds only three more
repetitions of the same operation and a hypothesis label. `16`'s n/r arms are
the only unique coverage; `66`'s 5× is a superset of `16`'s 2× for dag-p.
Recommendation: one seat — build n and r twice, p five times — or drop `66`.
No other pair in the wave shares both target and method.

### F3 — MEDIUM: `24 ScrErratumCheck` and `45 RevErratum` duplicate the erratum-verification core; `24`'s source list is incomplete

Both target `corpus/lessons/round-39-erratum.md` and verify its sentences
against the receipts. `45` adds the only unique check: append-only discipline
(`git diff --stat bb1f2457..HEAD -- .ufo/waves/round-39 corpus/lessons/round-39.md corpus/lessons/round-39-verifier-spotcheck.md` → empty, command 8).
`24` names three sources (c10 red/after decoy, S227.src, the r39 contract) but
the erratum has more claims than those sources cover: its first paragraph rests
on `.ufo/waves/round-39/evidence/c8-red-wait.txt` (not named by `24`; the
receipt says `exit=1`, `CONFORM=unmet`, `verdict: not reproduced`, matching the
erratum), and its last sentence covers the `fixtures/make-ancestry-dags.py`
path claim, also not in `24`'s three. So `24`'s "each erratum sentence is
backed" cannot be discharged from the sources it names. Recommendation: merge
into `45` (append-only + all four citations); drop `24` or re-scope it to a
subset.

### F4 — MEDIUM: `19`, `20`, `21`, `22` are zero-yield — their artifacts landed before dispatch

The round-40 fleet report `.ufo/reports/round-40/mori.md` (fleet commit
`22fc3dd`, 02:57:50) already contains `## Work performed` (line 10) and
`## Landed changes` (line 51) with T1/T2/T3; `SCORECARD.md:2216-2265` already
contains the round-40 declaration, results rows and the "Correction folded
same-round (number-drift)" paragraph (`:2231-2234`); `corpus/lessons/round-40.md`
already contains the S229 `## Gate` row (`:7`) and M23/M24 (`:23-24`). The
lane docs landed at `8d3badd` (02:56:11); the report at 02:57:50 — all before
the 03:03+ seat reports. Therefore:

- `19 ScrReportWork` would re-draft `## Work performed` that already exists.
- `20 ScrLandedChanges` would re-draft `## Landed changes`; its premise
  "the pending evidence commit" is stale — T2 `8d3badd` is landed, and the
  report already names T2/T3.
- `21 ScrScorecardRow` would re-draft the landed SCORECARD rows (and carries
  the wrong 34; F1).
- `22 ScrLessonDraft` would re-draft M23/M24 and the Gate row that already
  exist, including the exact 15-word quote.

These have a resolvable *source* (the receipts), so they are not "no target"
padding in the strict sense, but they have no *new* target: the artifacts are
complete and committed. Recommendation: cut them or convert to read-only
verification against the landed fleet report (which is outside the lane and
would need its path named; see F14).

### F5 — MEDIUM: `65 RevPriorIntent` asks the seat to confirm a proposition the landed lesson refutes, against an object that no longer exists

`corpus/lessons/round-40.md:51-55` records: `count-c1-r38.py` was a
byte-size-exact extract (recoverable), but `bypass-none.py` / `bypass-wait.py`
"existed in **no commit** — their exact bytes are unrecoverable; only their
class recipes remain committed". The item's parenthetical asks to "confirm they
exist in no commit **and were recoverable from round-38 evidence**": the
"no commit" half is true, the "recoverable" half is false for 2 of 3 strays.
The inherited working tree as an uncommitted state is also gone (its surviving
content was committed at T1/T2/T3 and the strays deleted), so the comparison is
reconstruct-only. The deliverable is already in the fleet report lines 45-49
and the lesson. Recommendation: re-scope to "classify recoverability" (which
the lesson already does) or cut; do not ask for confirmation of a false claim.

### F6 — MEDIUM: `11 ExeSurvivorSweep` targets ten files but the contract maps nine

`fixtures/generated/` holds ten `survivor-*.py`; the P-C10 mapping and the
receipt pairs cover nine (shadow-none, shadow-neg, cond, inf, divzero, decoy,
underscore, second-popen, tuple). The tenth, `survivor-barecomm.py`, is the
**second counter of the two-counter audit**: it is used by
`c10-{red,after}-multicounter.txt` and has no `c10-*-barecomm.txt` of its own.
Run alone it prints `CONFORM=unmet EXIT=1` with `drain_bind`,
`timeout_state` and `selftest_conjunct` failing (command 5), i.e. a different
check set from the nine survivors, and the contract's P-C10 fixture mapping has
no row for it. `11`'s "tabulate … and compare with the contract's P-C10
mapping" therefore has a 10-vs-9 mismatch. Recommendation: sweep the nine and
treat barecomm as the multicounter control (or add an explicit mapping row).
The 25.2 s runtime of the barecomm-alone run is a secondary cost note.

### F7 — LOW/MEDIUM: `38 ExeSelftestTiming` duplicates the timed run `4` already mandates

`4 ExeConformSelftest` says: run conform `--selftest`, confirm pass=11, "time
it; report the wall seconds". `38` says: measure both selftests' wall time and
confirm the 1,800,000 ms budget. The conform half of `38` is the same
instrument, same run, same timing already required by `4`; only the budget
assertion and the gate timing are new. Recommendation: fold the budget check
into `4`/`5` (add a `time` wrapper) and drop `38`, or accept it as the budget
seat with the duplication disclosed.

### F8 — LOW/MEDIUM: `9 ExeDagP`'s "no fabricated changed line" is not observable from the named receipt pair

`c11-after-fixture-p.txt` contains `changed S001 superseded_by=S002` and
`appendonly_violations=1 … round_changed=[S001]`, exactly like
`c11-red-firstparent.txt`; the only red/after discriminator in the printed
output is `stale_supersede=[S001]` (red) vs `[]` (after). The changed line is
legitimate: the dag-p side commit `s1` edits S001 and adds S002
(`tools/mori-sources-appendonly.py:574-582,612-616,665-685`), and the gate's own expected
dag-p case includes `round_changed=["S001"]` (`:612-616`); the merge itself
contributes the fabricated **stale** verdict in v2. The seat can confirm
"stale empty" and the red/after contradiction, but the parenthetical "no
fabricated changed line" needs per-commit attribution the tool does not print.
Recommendation: restate the check as "the merge adds no *stale* verdict; the
round's changed set is the side edit S001" (or print per-commit attribution).

### F9 — LOW: `5 ExeGateSelftest` asks for per-arm PASS lines the gate does not print

The command's entire output is
`MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` (command 4); the gate prints
`FAIL <arm>` only on failure and one summary at
`tools/mori-sources-appendonly.py:843,876`. The seat can confirm pass=15 and
enumerate arms from `_selftest_cases()` / `_selftest_dag_cases()` (source
read), but cannot "report per-arm PASS lines" from the instrument as the item
asks. Recommendation: either add a `--verbose`/per-arm print to the selftest
(a new gate version, so not this round) or re-word the item to "confirm
pass=15; enumerate arms from the case table".

### F10 — LOW/MEDIUM: `50 RevCensusPair` requires exit codes the census receipts do not record

`census-start.txt` and `census-end.txt` are 17 lines each: 16 `W04` rows plus
`mori ok <path>`. There is no `command:` line and no `EXIT=` line (command 11).
"Confirm both exit 0 … report the start/end exit codes explicitly" therefore
cannot be grounded in the named receipts; it requires re-running the census
(duplicating `13 ExeCensus`) or citing the fleet report's prose. The W04-set
comparison itself is resolvable and the two sets are identical. Recommendation:
re-run once in `50` (and then `13` is the duplicate), or add exit capture to
the census receipts.

### F11 — LOW: `12 ExeParity` and `48 RevParityScope` rest on contradictory seed/sha premises

`c10-parity.txt` names **one** seed (`seed 20261024`) and prints only
`count-c7 sha256: b92c65f2…`; there is no count-c8 sha256 (command 10).
`48` reviews the receipt as "byte-identical at one seed". `12` asks to re-run
"with two different seeds" and "report the sha256 of both counters" — a method
the receipt never used and an output it does not contain. The two seats can
each run, but they will produce different claims about the same receipt.
Recommendation: align both on one seed (as the receipt) and ask `12` to add
the missing c8 sha to its report; do not describe the landed receipt as a
two-seed proof.

### F12 — LOW: `26 ScoutInstrumentLayout` and `43 RevContractConformance` duplicate the forward existence check on an under-specified glob list

Both read the contract's evidence-path paragraph (`contract.md:151-152`) and
check the files exist. `26` adds the reverse direction and the instrument tree;
`43` adds the declared content class (red=met on v2, after=unmet on v3). The
"path the contract names" is a glob family (`c10-red-*.txt`, `c10-after*.txt`,
`c11-red-*.txt`, `c11-after*.txt`), not an enumeration, so the forward check is
ambiguous: `c10-parity.txt` and `wave-plan.txt` exist but are not named by
those globs, and `.parity-c7.txt`/`.parity-c8.txt` are hidden (command 9). The
existence half is duplicated; the unique halves are `26`'s reverse map and
`43`'s content class. Recommendation: one seat with both halves, and state
that the contract list is a glob family (or enumerate it).

### F13 — LOW: `33 RevFindingsCoverage` and `36 RevRoutedCoverage` audit the same contract section with the same reading method

Both read `.ufo/waves/round-40/contract.md` `## Routed inputs` and cross-check
it against `corpus/lessons/round-39.md` / the closure's routed-defect list.
`33` asks for exactly-one mapping of 13 findings + 6 routed defects; `36` asks
that each of defects 1–4 be named with its discharging receipt. Different
predicates, same target and same source-reading operation. Not a strict
duplicate, but a merge candidate (one seat: mapping table + receipt column).
Also note the scope difference is real: the closure has 6 defects
(`corpus/lessons/round-39-verifier-spotcheck.md:58-65`), while `36` covers
1–4; `33` covers 6 — keep that explicit if both are kept.

### F14 — LOW: `47 RevShonenBoxes`' target exists only outside the lane and is not named

The report it asks to review is `/home/vgpnk/Projects/shokunin/.ufo/reports/round-40/mori.md`
(fleet commit `22fc3dd`), `## SHONEN` at line 127 with four assessment lines
(129 `[~]`, 132 `[~]`, 134 `[ ]`, 136 `[~]`). There is no
`.ufo/reports/round-40/` in the lane. The item's prompt names no path, and the
wave context says all seat paths are under the lane, so the seat must discover
the fleet-level report. The target is resolvable (read-only) but the item is
under-specified; `LOG.md:2314-2315` already carries the same honest-state line.
Recommendation: name the fleet report path in the item, and make clear the seat
reviews it read-only (never edits the fleet repo).

### F15 — INFO: counter-of-record replay drifts on `head_pin` after T1

`conform.py:517-525` makes `head_pin` a comparison of the counter's live
`--pin-only` (worktree HEAD) against `git rev-parse HEAD`. At T1 both were
`265a955` (`c10-after.txt:4`); today both are `ede486b` (command 6), so
`3 ExeConformMet`'s byte-for-byte diff will report a `head_pin` drift that is
structural, not an instrument regression. The item says "report any drift", so
it is still executable; the main agent should treat the `head_pin` line as
expected drift and compare the other eight checks. This is the same class the
r39 lesson finding 11 recorded ("`head_pin` pins live HEAD … tautological").

### F16 — INFO: seat-count prose mismatch (64 vs 66)

`contract.md:171` says "ONE v2 wave of 64 seats"; `w1-spec.json` has 66 items
and `maxLanes: 66`; `SCORECARD.md:2258` and the fleet report say 66. The
generator docstring also says 64. This does not change the grouping (all 66
were deduped), but it is a claim-admission hygiene note: the frozen contract's
round-shape sentence does not describe the dispatched wave.

### F17 — INFO: `28 ScoutQualityBar`'s receipt-rev check is a subset of `39`/`40`

`28`'s "check each receipt set names its measured rev" is one third of
`39 RevC1Receipts` / `40 RevC2Receipts` (command + rev + exit). `28`'s unique
job is mapping `corpus/QUALITY.md` criteria to the round's claims; the rev
sweep is duplicated. Keep `28` for the criteria mapping, drop the rev clause.

### F18 — INFO: `2`, `13`, `50` are three distinct census methods, not duplicates

`2 ConnW04Routing` reads `census-end.txt` for W04 ownership/S229 URL
occurrence; `13 ExeCensus` re-runs the census; `50 RevCensusPair` compares
start/end. Distinct methods on an overlapping artifact family; no dedupe
action. `2`'s S229 URL occurrence is resolvable and unique:
`corpus/SOURCES.md:235` (row inside `## Registry` at line 3, immediately after
S228 at 234); the URL appears once.

### F19 — INFO: partial overlaps checked and not classified as duplicates

These pairs share a target or a method, but not both; they are complementary and
should stay separate unless the main agent wants to reduce headcount:

- `8`/`9`/`10` (live replay of each DAG pair) vs `40 RevC2Receipts` (static
  three-part audit of all c11 receipts, including whether each red/after pair
  contradicts as declared): same pairs, read-vs-run methods.
- `44 RevScorecardClaims` (control coverage: is the do-nothing control committed
  for every survivor/DAG?) vs `39`/`40` (receipt discipline): different question.
- `23 ScrSourcesRow` (S229 row cells + placement), `35 RevLessonGate` (lesson
  Gate row quote/copy/teaches), `46 RevKnowledgeProvenance` (knowledge-entry
  provenance): three different S229 artifacts.
- `1 ConnSiblingOverlap` (sibling `corpus/SOURCES.md`) vs `29 ScoutSiblingConform`
  (sibling conform/scope-fold artifacts): different targets.
- `31 SimpGateV3`/`41 RevGateDiff` and `32 SimpConformV3`/`42 RevConformDiff`:
  dead-code and line-accounting reads vs behavioral hunk classification.
- `51 CritNewSurvivor` vs `62 MutConformArms`, and `55 CritConjunctSemantics` vs
  `17 ExeConjunctAfter`: new-fixture/semantic attack vs checker mutation or
  pre-built gutted-copy replay.
- `53 CritLaneLine` (sampled 5-id semantic audit) vs `54 CritPredParenthetical`
  (full 16-id enumeration + defect classification): complementary, same claim.
- `54` vs `58 CritScoringHonesty`: the 34/16 numbers recur, but `54` attacks the
  parenthetical while `58` sweeps all SCORECARD numbers.
- `5 ExeGateSelftest` vs `38 ExeSelftestTiming`: `38` reuses `5`'s run for
  timing (see F7); the run itself is already mandated.

## Padding verdict

Strictly (no resolvable evidence target): **none**. Every item names an
artifact that exists or an instrument that runs. The closest cases and their
disposition:

- Zero-yield against landed artifacts (no new target): **19, 20, 21, 22**
  (F4) and **65** (F5, object destroyed + false confirmation). If the wave's
  definition of padding is "cannot produce new evidence", these five are the
  padding set.
- Under-specified target (exists but the item's required datum/output is not
  in it): **5** (per-arm lines), **9** ("no fabricated changed line"), **11**
  (ten vs nine), **12** (two seeds/both shas), **50** (exit codes), **47**
  (report path unnamed).
- `38` is a method duplicate of `4`/`5`, not padding.

## Residual risk and verification gaps

- I did not execute the construction/mutation items' own acceptance runs
  (`51`, `52`, `55`, `56`, `59`, `60`, `61`, `62`); my scope is dedupe, and
  their receipts/arms are theirs to produce. My duplicate analysis of those is
  based on their task text and the builders they name.
- I did not re-verify every receipt's content class or every evidence path
  (that is `39`/`40`/`43`); I verified the paths I cite in F1–F14.
- The F1 count is measured at the current worktree and cross-checked against
  the committed receipt text; the live gate at `265a955` prints 35. The
  neighbour `w1/CritPredParenthetical.md` independently measured 35. I did not
  adjudicate C2's semantic sentence (the gate line is internally consistent);
  only the counted prediction is wrong.
- The fleet report is in the fleet repo (read-only for this seat); I read it
  but did not write or verify its claims beyond the sections used here.
- No `lsp` device was available (recorded above), so definition/reference
  claims were checked by reading the named code lines and running the named
  commands.
- I did not test the conflicted-index hypothesis in `66`; `16`/`66` own that
  probe, and my finding is only that they perform the same repeat-build
  comparison on dag-p.
