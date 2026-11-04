# Round 80 — mori verifier spotcheck (non-author closure review)

author: hyaku closure (non-author integrator, @m_zfl)
round: 80
date: 2026-11-04
entering: `d58889220d3c6a18d461f2d31b5ab162ffef1e4e` (lane HEAD before the round)
lane head after: `44bc941a0e3e9676fa33a882b43d6e9793cbf74d` (branch `master`, pushed;
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-remote origin refs/heads/master` prints it)
method: index-free read-only git (`log`, `show`, `diff`, `cat-file`, `ls-tree`,
`merge-base --is-ancestor`, `ls-remote`); my own replication of the frozen sweep's
graded-row/pointer grammar and of the C3 population over committed bytes (the lane's
counters were **not** executed — their committed receipts were read per the gate standard);
a live re-fetch of S595; and the fleet source census. No lane file was edited except this
one; no mutating jj command was run except the lane helper's commit for this file.

## Verdict summary

**status ok, admitted.** All three claims verify on independent re-derivation; no owned axis
is harmed (the six axis scores are byte-unchanged: 6/7/5/5/5/6). The round arrives with two
routed-defect classes of its own making, both status-neutral: the required SCORECARD per-claim
after-cells are still `PENDING` at the landed bytes, and the new capability row's own evidence
cell carries a stale pointer count (`232` vs the landed `233`) plus "integration re-run
pending" wording. Both are named below (D80-1, D80-2) and routed to r81. The round's discernment
spot-check agrees with the sampled admit and with its reject-class decisions; the source gate is
admit-only (named weakness).

## Step-1 conformance

| Check | Result | Evidence |
|---|---|---|
| Report committed by lane identity | PASS | `git log --format='%an %ae %H' -1 -- .ufo/reports/round-80/mori.md` → `mori-shokunin mori@shokunin.local c585abad7ff6511ac31d16b82b1a3afac25a43b2` |
| Report lands last | PASS | report committer `2026-11-04 03:22:51 -0300` > lane tip committer `03:22:31 -0300` (`git log -1 --format='%cd'`); its earlier author stamp `03:22:16` is the jj working-copy change time, not the commit |
| `SHONEN` heading | PASS | `grep -c '^## SHONEN' .ufo/reports/round-80/mori.md` → 1; four `[~]` lines, one per box, each with a resolvable pointer — author-asserted form while SHONEN.md is held |
| Cited lane commits exist + ancestor | PASS | 7/7 (`44bc941a`, `d5888922` as entering, `57451ecb`, `8108dfcc`, `2a826f17`, `97ce0c96`, `108ec314`): `git cat-file -t` = commit and `git merge-base --is-ancestor <h> master` rc 0 for each |
| Lane repo pushed, no uncommitted round work | PASS | `scripts/hyaku/jj-lane.sh state …` → `branch=master local=44bc941a0e3e remote=44bc941a0e3e ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty |
| Report hash pushed on the fleet repo | PASS | `c585abad…` is an ancestor of `origin/main` and `origin/master` (`merge-base --is-ancestor` rc 0); remote refs print `fb58fc3d…` |
| Write scope held | PASS | entering→final diff = 44 paths, all lane-owned (wave evidence, LOG, SCORECARD, SKILL, PROVINCE, corpus, the new `tools/mori-claim-sweep.py`, and the r79 counter's selftest region); no sibling, MANIFEST, fleet-root or `.ufo/state/` path |
| Prompt carries the template contract | PASS | `.ufo/prompts/mori-round-80.md:1-140` is `templates/round-prompt.md` verbatim modulo the working-dir/axis/lane substitutions (byte diff shows only those two substitutions); the addendum §6 carries the five child-lane items: report path §4, report-lands-last line 513, `grep -c '^## SHONEN'` line 518, cite-the-pushed-hash lines 107/513, write scope line 445 |
| L2 floor and route map | PASS | prompt §3 requires ≥8 seats in one batched call; `w1-results.json` carries 14 seats (4 executor, 3 scribe, 2 scout, 2 reviewer, 1 connector, 1 critic, 1 mutation-tester); attack share 4/14 = 28.6 %; the quoted route map is the operator's run-15 amendment (only reviewer `@m_zfl`, all others `@m_flash`), which supersedes the advisory MISSION bucket table and is not contradicted by it |
| Contract frozen before data | PASS | contract commit `57451ecb` 02:53:57; wave dispatch marker `w1.ready` = 03:07, `w1.ready.dispatched` = 03:08:27 |
| Not a marker report | PASS | real work, three frozen counters, checkable hashes and receipts; minimum content complete (work, landed changes, before→after, sources/frontier, trends, SHONEN) |

## Claim re-checks

Re-measured by this reviewer (commands run, not receipts read): C1's before/after carriers and
pointer population, C3's before/after population. Evidence-verified (committed receipts read
and cross-checked, gate not executed): the three counters' selftest tallies and frozen runs,
the C2 mutant kills, the standing battery.

### C1 — calibration (capability acquisition + D79-1 discharge): VERIFIED

- Before: `git cat-file -e d5888922:tools/mori-claim-sweep.py` → rc **128** (absent);
  `git show d5888922:SCORECARD.md | grep -c 'selftest 18 in-memory cases'` → **1**.
- After (my own implementation of the frozen rule — graded SCORECARD `## Axes` rows, every
  capabilities-table data row, every `- [` SHONEN line; the `POINTER` grammar, line/rev suffix
  stripping, fence exclusion and wildcard glob as frozen — over `git show 44bc941a:<carrier>`
  bytes for SCORECARD/SKILL/SHONEN/LOG): **`pointers=233`, unresolved 0, stale 0, mismatches 0**.
  `git show 44bc941a:SCORECARD.md | grep -c 'selftest 19 in-memory cases'` → **1**;
  `… | grep -c 'selftest 18 in-memory cases'` → **0**.
- Committed gate evidence: `.ufo/waves/round-80/evidence/after-r80.txt` —
  `C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=97ce0c96c779`, rc 0;
  the tool's `CLAIM_SWEEP_SELFTEST pass=30 fail=0` (22 `check()` arms + 8 grammar arms = 30,
  read from the source); pins pin `tools/mori-control-receipt.py` to 19 and the superseded
  18-arm literal; SKILL gate-registry row 14 carries all eight fields.
- Entering receipt: `controls-r80.txt` — `C1=unmet tool=absent …`, rc 1; the 18-arm literal
  present at entering. Both readings are independently reproduced, so the r79 D79-1 stale tally
  is discharged. Named limit carried from the reviewer: P-C1's second conjunct is not
  re-derivable by the counter at the tip (HIGH-2; report HIGH-2), and the instrument's
  class/registry cells are not graded by it.
- Grade: **calibration improved.**

### C2 — operability (sourced S595): VERIFIED (evidence-verified; harness not executed)

- Before: `controls-r80.txt` — `MUTATION_C2 survivors=2 killed=4 total=6 rev=d58889220d3c`, rc 1
  (`drop_admitted` and `cut_clause_boundary` survive at `pass=4 fail=0`).
- After: `after-r80.txt` — the harness prints the unmutated run green, six per-mutant `killed`
  lines with red selftest verdicts, then
  `MUTATION_C2 survivors=0 killed=6 total=6 unmutated=green rev=97ce0c96c779`, rc 0.
- The change is confined to the selftest region: `git diff -U0 d5888922 44bc941a -- .ufo/waves/round-79/count-c2.py`
  is one `+16` hunk headed `@@ -159,6 +159,22 @@ def selfcheck(scratch):`, adding exactly three
  cases (`nonadmitted_below_ceiling_ignored_met`, `verdict_after_clause_boundary_unmet`,
  `later_round_in_cell_ignored_unmet`); the total is 7 cases, matching the receipt's `pass=7`.
- Harness integrity: `MUTANTS` holds six (label, old, new) anchors; I extracted them with an
  AST read of the committed harness and checked the committed `count-c2.py` at `44bc941a`:
  all six old strings present, all six replacement strings absent; the harness reads
  `git show <rev>:COUNTER` and refuses to grade unless the unmutated selftest is green.
- Grade: **operability improved.**

### C3 — coverage: VERIFIED (re-measured independently)

- Before (my census at `d5888922`, `git ls-tree -r --name-only d5888922 -- tools/` filtered to
  `tools/<name>.py|.sh`, PROVINCE tokens with the sibling-lane `*-shokunin/` exclusion):
  **present=55, named=14, missing=41, extra=0** — exactly the receipt's line.
- After (same census at `44bc941a`): **present=56, named=56, missing=0, extra=0**. The
  population grows by one because the round lands an instrument; `PROVINCE.md` is a pure
  insertion (`+67`, 0 deletions), an append-only `## Instrument inventory (round 80)` with 56
  rows. `mori-cgroup-pressure.py` is the one registry-less row and the file says why.
- Grade: **coverage improved.**

### No axis harmed

`git diff d5888922 44bc941a -- SCORECARD.md` is 35 insertions / 1 deletion; the `## Axes` score
rows are byte-identical entering→final (coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6). PROVINCE gains only; no existing instrument byte changed except the
r79 counter's selftest region above; the standing 13-instrument battery is 13/13 rc 0 at the
landed bytes (`evidence/battery-r80.txt`, read, not re-run). No axis is harmed.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1: the sweep lands, its 30-arm selftest and the frozen run are committed, and the D79-1 stale tally is corrected 18→19 with a named correction; my independent replication reads 233 pointers / 0 mismatches at the tip |
| operability | improved | C2: three selftest arms inside `selfcheck()` take the frozen six-mutant harness from survivors=2 to survivors=0, with the unmutated-green refusal; the predicate/CLI/output are byte-unchanged |
| coverage | improved | C3: PROVINCE names 56 of 56 committed instruments (from 14 of 55), pure-insertion, registry row 14 added for the new gate |
| depth | unchanged | No depth claim; no depth metric moved |
| freshness | unchanged | No re-verification claim; S595 is new ground, not a stale entry re-verified |
| adjacency | unchanged | No sibling surface touched; the inventory covers the lane's own instruments only |

No axis is harmed. The lowest-non-retired-axis rule is satisfied: depth/freshness/calibration
are tied at the floor (5) and C1 works calibration.

## Discernment spot-check (checked from outside)

The round's `## Gate` records one candidate, S595, admitted; it records no rejected source
candidate (the round's refusals are work-scope refusals). The Gate is therefore admit-only —
a named weakness. I sampled the admit plus the two reject-class decisions the round actually
made.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S595 (arXiv 2102.11378v2) admit, tier A, scope narrowed to "mutation analysis's own definition as a test-adequacy criterion, limited to what the abstract states" | admit | Pinned copy `corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html` (sha256 `28ea1f16…b884`, 43884 bytes / 613 lines) and a fresh live fetch of `https://arxiv.org/abs/2102.11378v2` (HTTP 200, 43884 bytes, byte-identical); anchor line `:121` | **agree** | The located span is the 22-word abstract sentence (≤25); `:121` is the abstract body, not a metadata copy; tier A is right for an original paper and the scope stops where the abstract stops |
| The round's refusal to rewrite the r79 D79-3 adjacency pointer ("re-verified, not changed") | reject (of the prior review's defect premise) | `git -C /home/vgpnk/Projects/shokunin cat-file -e 63729047:MANIFEST.json` rc 0; `rounds[398]` at that revision is `mori 19 … verdicts.adjacency = improved, admitted` | **agree** | The pointer the r79 review asked for already resolves and points at the intended row; the cell's disclosed absent file is a separate, already-stated limit — rewriting would have created a false correction |
| The round's rejection of the r79 seat's prose before-values ("3 of 6"; "15 of 55") in favour of the measured controls | reject (of the prose) | `controls-r80.txt` and my census at `d5888922`: `MUTATION_C2 survivors=2 killed=4 total=6`; C3 `named=14 present=55 missing=41 extra=0` | **agree** | The prose values are not reproducible; the measured entering values are 2 and 14, and the contract's predicate is what grades |
| New SOURCES row quote check (contract rule 1) | admit | Same pinned bytes, `:121`; counted the quoted span (22 words) and the row's anchor sha/size/line cells against the copy | **agree** | Row `S595` is 11 cells, unique id, `paper`/A/`mined`, opened 2026-11-04, `recheck 365d`, `used-by` names the entry, which exists and opens with its provenance trio |
| "Gate declares no rejected source candidate" | observation | `corpus/lessons/round-80.md` `## Gate`; `.ufo/waves/round-80/w1/Mo80Sc02Source.md` ("no `REJECTED` row to reopen") | **agree, with a named weakness** | One candidate was screened and none competed; an admit-only source gate shows less discrimination, but the round's refusals (merge package, tally-pinned instruments, the D79-5 deferral) carry the taste evidence |

## Trend verdicts

- **expansion: improved** — one new admitted `knowledge/` entry on ground the coverage map did
  not hold (mutation analysis as a test-adequacy criterion; the core map's nearest rows are tool
  mutation-kill arms, not adequacy theory), `source: S595` on a `mined` row opened, pinned and
  quoted this round; rows 367 → 368 (my count at entering and at the tip), malformed 0, census
  rc 0; README gained the index row the same round.
- **quality: improved** — a new 30-arm registered gate whose own over-broad arm was found and
  repaired in-round; the r79 counter's two surviving mutants killed (three arms added, six of six
  killed in the committed receipt); the standing battery 13/13 rc 0; both receipt families
  conform to the r79 guard (`unbound=0` in `after-r80.txt`). Counterweights, routed below: the
  SCORECARD after-cells are still `PENDING` and the capability row carries a stale count, and
  three mutants survive on the new tools (r81 work named in the report).
- **discernment: improved** — two mistakes mined with class/evidence/captured-by/fix, the second
  found by the round's own first run (an over-broad wildcard arm), and the sweep bit its own
  author's LOG prose (repaired at `108ec314`); three routed defects stayed r81 work rather than
  widening the round's predicate; the D79-3 premise was checked and refused with evidence. This
  spot-check agrees with the sampled admit and both reject-class decisions. Named weakness: the
  source gate is admit-only, and the round's own record-keeping defects (D80-1/D80-2) were not
  caught by the new sweep.

## Routed defects the lane must fix next round

1. **D80-1 (status-neutral, SCORECARD record incompleteness).** `SCORECARD.md`'s Round 80
   section still says "all three after cells are PENDING for the L1's post-integration
   measurements" (`:4044`) and the three after cells read `PENDING` (`:4048-:4050`) at the
   landed bytes, while the report's after-measurements are measured. The round prompt item 5
   requires the per-claim record in `SCORECARD.md` (score delta, evidence pointer, counting
   command, measured commit). Fix: append a named correction section filling the three after
   cells with the measured values and the measured revision; never rewrite the frozen predicate.
2. **D80-2 (status-neutral, stale numeric claim and pending wording).** The new capabilities row
   (`SCORECARD.md:4036`) states `CLAIM_SWEEP … pointers=232`, while the cited command at the
   landed bytes prints `pointers=233` (my independent replication and `after-r80.txt`); the same
   row ends "both L1 retained receipts over worktree bytes, 2026-11-04; integration re-run
   pending", and SKILL gate-registry row 14 (`SKILL.md:1366`) carries the same "integration re-run
   owned by L1" wording. A count must reproduce from its cited command. Fix: correct 232 → 233
   with a named correction and replace the pending wording with the measured command output and
   the revision it was run against.
3. **D80-3 (status-neutral, contract shorthand vs frozen predicate).** `.ufo/waves/round-80/contract.md`
   keeps the entering shorthand `1 → 0` (C1), "from 3 of 6" (C2) and "from 15 of 55" (C3) in its
   claim table, while P-C2/P-C3 and `controls-r80.txt` measure `survivors=2` and
   `named=14 present=55 missing=41`; P-C1's second conjunct ("the same sweep at the entering
   revision finds at least one mismatch") is unimplementable because the tool is absent at
   entering (reviewer HIGH-2). The report and lesson disclose both readings. Fix: append a
   correction section naming the superseded shorthand and narrow P-C1's second conjunct to the
   receipt the round actually used; do not rewrite the frozen bytes.
4. **D80-4 (status-neutral, report revision precision).** The report says "every after-value was
   re-measured at the final tip `97ce0c96c779…`", but the lane HEAD is `44bc941a`; the after
   receipt cites `97ce0c96` and `44bc941a`'s re-measurement is asserted only in its commit
   subject. The graded bytes changed between `97ce0c96` and `44bc941a` only in the after receipt,
   `w1-results.json` and the reviewer report, so the claims still hold; the citation is the
   defect. Fix: state `97ce0c96` as the measured revision and name `44bc941a` as evidence-only,
   or commit a receipt run at the tip.

## No-harm receipts

- Axis scores: `SCORECARD.md` `## Axes` rows byte-identical entering→final; 6/7/5/5/5/6.
- Round diff: 44 paths, all lane-owned; `PROVINCE.md` +67/−0; `LOG.md` +83/−0; `SCORECARD.md`
  +35/−1 (the D79-1 row correction and two appended sections); no existing instrument byte
  changed except `.ufo/waves/round-79/count-c2.py`'s selftest region.
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → rc 0,
  `mori ok`, 35 tolerated W04 duplicate-URL warnings; rows 367 → 368; malformed 0; duplicate ids 0.
- S595 pin: `sha256sum` = `28ea1f163860348979a3aa9e9ef8e00fc8eb3ecec2762782d639783003f1b884`,
  `wc -lc` = 613 lines / 43884 bytes; live re-fetch byte-identical.
- Fleet leftovers: only `.scratch/` entries and the 24-byte `after` file (operator/orchestrator
  state, not this lane's); the lane tree is clean and `ahead=0`.
