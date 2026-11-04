# Round 81 — mori verifier spotcheck (non-author closure review)

author: hyaku closure (non-author integrator, @m_zfl)
round: 81
date: 2026-11-04
entering: `d144672c986a25642e59fee3b9de238f27e6b769` (lane HEAD before the round; the
round's own record names `44bc941a0e3e9676fa33a882b43d6e9793cbf74d`, the lane-authored tip —
see D81-6)
lane head after: `142998f53fb3393838180b4eb60fb6045333c643` (branch `master`, pushed;
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-remote origin refs/heads/master`
prints it)
method: index-free read-only git (`log`, `show`, `diff`, `cat-file`, `ls-tree`,
`merge-base --is-ancestor`, `ls-remote`); my own replication of the frozen claim-sweep's
graded-row/pointer grammar over committed bytes (the lane's counters and gates were **not**
executed — their committed receipts were read per the gate standard); one live re-fetch of
the rejected ACM page; the fleet source census. No lane file was edited except this one; no
mutating jj command was run except the lane helper's commit for this file.

## Verdict summary

**status ok, admitted.** Both claims verify on the round's frozen predicates; no owned axis
is harmed (the six axis scores are byte-unchanged: 6/7/5/5/5/6). C1's seven fixtures are the
r80 counter reviewer's routed shapes (six defect ids, seven fixtures) and the r80
frozen contract is byte-unchanged. C2's after-run is independently supported for
`pending=0`, `pinned=0` and `tool=present`, with the claim-sweep pointer count re-derived by
my own implementation (240 at the tip; 237 at the after commit the row names — D81-1). The
round arrives with six status-neutral record/evidence defects of its own making, routed
below; the most important is a repeat of the D80-4 class: the new capability row states
`pointers=240` as measured at `075574c8`, where the count is 237. The discernment
spot-check agrees with the sampled admit and with both reject-class decisions; the source
Gate is admit-one-with-three-refusals, as the report itself names.

## Step-1 conformance

| Check | Result | Evidence |
|---|---|---|
| Report committed by lane identity | PASS | `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H %s' -- .ufo/reports/round-81/mori.md` → `mori-shokunin <mori@shokunin.local> a64df598… round-81: mori report`, then `3e390603… round-81: mori report erratum` |
| Report lands last | PASS | lane tip committer `2026-11-04 04:12:49 -0300`; report `04:13:17`; erratum `04:13:40` |
| `SHONEN` heading, one line per box | PASS | `grep -c '^## SHONEN'` → 1; four `[~]` lines at `:199`, `:202`, `:204`, `:207`, one per `SHONEN.md` box, each with a resolvable pointer |
| Cited lane commits exist + ancestor of the branch | PASS | 11 lane hashes (`6b021d29`, `19765553`, `1106afd3`, `075574c8`, `b10e91ee`, `482dc48d`, `ed2f3e11`, `9335bdbd`, `142998f5`, plus `44bc941a` and `97ce0c96` as measured revisions): `git cat-file -t` = commit and `git merge-base --is-ancestor <h> master` rc 0 for each; the fleet report commit `a64df598` is an ancestor of `origin/master` |
| Lane repo pushed, no uncommitted round work | PASS | `scripts/hyaku/jj-lane.sh state …` → `branch=master local=142998f53fb3 remote=142998f53fb3 ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty |
| Prompt carries the template contract | PASS | the rendered `templates/round-prompt.md` (lane/round/root/axes substitutions) is an exact 8,359-character prefix of the 62,749-character, 704-line prompt; addendum §6 follows; the five child-lane items are present — report path §4, commit-then-report ordering §5 + addendum §4, `SHONEN` heading §4 and the pre-report `grep -c '^## SHONEN'` line, cite-the-pushed-hash lines, lane write scope §3 |
| L2 floor and wave shape | PASS | `w1-results.json`: 14 seats in one wave (4 executor, 3 scribe, 2 scout, 2 reviewer, 1 connector, 1 critic, 1 mutation-tester); attack share 4/14 = 28.6 %; connector 1 ≤ 2; every seat output non-empty, no notes/errors; L1 holds the planner seat (validator rejects `planner`); `w1-validator.out` `counts.spawn=14`; `w1.ready` 03:43:43 → `.ready.dispatched` 03:44:06 with all 14 names; no `model` field in any of the 14 tasks |
| Contract frozen before data | PASS | freeze commit `6b021d29` committer `03:41:54`; `w1.ready` `03:43:43`; `.ready.dispatched` `03:44:06`; the contract's do-nothing controls are committed in the freeze |
| Entering revision naming | DEFECT (D81-6, status-neutral) | the report/contract/lesson name entering `44bc941a`; the actual pre-round lane HEAD is `d144672c` (`git log --format='%H %P' -1 6b021d29` → parent `d144672c`; `git diff --stat 44bc941a d144672c` is the 202-line r80 verifier spotcheck only). The claim measurements at `44bc941a` are valid (the spotcheck file is not a claim carrier; the r80 real arms were re-read at `ed2f3e11`: `battery-r81.txt:722-727`), but the entering hash is misnamed |
| Route-map precision | OBSERVATION (D81-4, status-neutral) | the prompt's "latest routing amendment" (2026-11-03) puts only reviewer on `@m_zfl`; the live `~/.omp/agent/config.yml` (mtime `2026-11-04 01:09:53`, before the 03:33 launch) also puts critic, executor, mutation-tester, connector, sentinel and scribe on `@m_zfl` (the `config.yml.pre-zfl-split-20261104` backup carries the report's pre-split map). The report's parenthetical is the pre-split map and is self-contradictory ("every other role on `@m_flash`, scout on `@m_antigravity`"); no model was passed and no claim depends on it |
| Write scope held | PASS | entering→final diff 50 paths, all under the lane repo (`.ufo/waves/round-81/`, the two r80 counters' implementation, `LOG.md`, `SCORECARD.md`, `SKILL.md`, `PROVINCE.md`, `corpus/`); no sibling lane, fleet-root, `templates/`, `scripts/` or `.ufo/state/` path |
| Not a marker report | PASS | real work, frozen counters, checkable hashes, committed controls/gate receipts; minimum content complete (work, landed changes, before→after, sources/frontier, trends, SHONEN) |

## Claim re-checks

Re-measured by this reviewer (commands run, not receipts read): the r80 contract byte
identity, the r80 counter post-measurement diff, the PENDING-cell population at entering and
at the tip, the claim-sweep pointer population at entering/after/tip, the SOURCES census,
and the source quotes. Evidence-verified (committed receipts read and cross-checked; the
lane's gates not executed): the r81 keepers' selftest tallies, the fixture-run outputs, the
mutation kills and the standing batteries.

### C1 — operability (7, score held): VERIFIED (evidence-verified + logic-invariance re-measure)

- Before at `44bc941a` (`controls-r81.txt`): all seven expected≠got —
  `A2 expected=unmet got=met`, `A3 …got=met`, `A4 …got=met`, `A5 expected=met got=setup`,
  `B1 …got=met`, `B2 expected=met got=unmet`, `B6 expected=met got=unmet`;
  `C1=unmet wrong=7 fixtures=7 real_c1=met real_c3=met rev=44bc941a0e3e`, rc 1. The seven
  fixture shapes are exactly `.ufo/waves/round-80/w1/Mo80R01Counter.md` MEDIUM-6 (`B1`),
  MEDIUM-7 (`A2`, `A3`), MEDIUM-8 (`A4`), LOW-10 (`A5`), LOW-11 (`B2`), LOW-12 (`B6`).
- After at `075574c8` (`corpus/lessons/round-81.md` after-block): all seven expected=got,
  `C1=met wrong=0 fixtures=7 real_c1=met real_c3=met rev=075574c83eae`, rc 0.
- Frozen predicates unchanged: `git diff 44bc941a 142998f5 -- .ufo/waves/round-80/contract.md | wc -l`
  → **0**. The implementation fixes are visible in `git diff 44bc941a 075574c8 --
  .ufo/waves/round-80/count-c1.py .ufo/waves/round-80/count-c3.py`: all-lines parse +
  mismatch-line/summary consistency (A2/A3), all matching rows with disagreement → `None`
  (A4), argv+tar-stdin export (A5), left boundary + own-prefix token and directory typing
  (B1/B2/B6).
- Post-measurement invariance: `git diff 075574c8 142998f5 --` the two r80 counters is
  selftest-case additions only (`zero_summary_nonzero_exit` into the 9-case r80 count-c1
  selfcheck; `suffix_trap` into the 8-case r80 count-c3 selfcheck). The r80 real arms were
  read green at `ed2f3e11` (`battery-r81.txt:722-727`: `C1=met … row_tally=19 live_tally=19`,
  `C3=met named=57 present=57 missing=0 extra=0`), and `git diff --name-only ed2f3e11
  142998f5` changes only evidence files, so the report's final-tip re-run is consistent.
- Grade: **operability improved**; the score stays 7.

### C2 — calibration (5, score held): VERIFIED (pending/tool re-measured; pinned re-measured independently; agree evidence-verified)

- Before at `44bc941a` (`controls-r81.txt`): `C2=unmet pending=3 pinned=1 tool=absent agree=0
  rev=44bc941a0e3e`, rc 1. `git show 44bc941a:SCORECARD.md | grep -cE '\|[[:space:]]*PENDING[[:space:]]*\|'`
  → **3** (`:4048-4050`); `git cat-file -e 44bc941a:tools/mori-record-sweep.py` → rc **128**;
  my pointer count at `44bc941a` is **233** against the row's stated 232 (pinned=1).
- After at `142998f5`: no exact `PENDING` cell in any `## Round` section (`grep` → 0); the
  tool exists (`wc -l` → 225), registry row 15 parses as **8 cells**, `PROVINCE.md` names it,
  and its self-test tally is pinned and matching (`evidence/gates-r81.txt`: pin line 1367
  `RECORD_SWEEP_SELFTEST pass=26 fail=0`, state `match`).
- `pinned=0` re-derived by plain measurement: my implementation of the frozen sweep's
  graded-row/pointer grammar over `git show <rev>:<carrier>` bytes for
  SCORECARD/SKILL/SHONEN/LOG gives **233** at `44bc941a`, **237** at `075574c8`, and **240**
  at `482dc48d` and `142998f5` (SCORECARD 192 + SHONEN 48 at the tip). The capability row
  states `pointers=240`, and the pinned command's argument is the same claim-sweep invocation,
  so the pinned arm is 0 at the tip. The pins file hash matches the counter's frozen
  `PINS_SHA256` (`b991e0bd…`).
- Before/after receipt (read, not executed): the report's `C2=met pending=0 pinned=0
  tool=present agree=1` rc 0 at the final tip; the lesson explains that a lane-side receipt
  for this reading cannot be committed in the same commit it grades (D81-2).
- Grade: **calibration improved**; the score stays 5. Counterweights: D81-1 (the 240 value's
  revision label is wrong), D81-2 (no standalone after-receipt), and the claim's "no
  self-disagreeing count" is only as strong as the pinned arm, which cannot see a revision
  label.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1: the seven r80 routed counter exposures are graded to their declared verdicts at the landed bytes, the r80 frozen predicates are byte-unchanged, and both r80 real arms re-read green; the r81 keeper guards (setup-never-a-pass, fixture identity, deletion/pins tampering) are pre-data amendments with re-measured controls |
| calibration | improved | C2: the record has no `PENDING` result cell (3→0), the tool lands, and the capability row's stated 240 matches the pinned command at the tip; the D80-1..D80-4 corrections are applied append-only. Routed: D81-1/D81-2 |
| coverage | unchanged | no coverage claim; the new knowledge entry's coverage-map row is a corpus index addition, and `PROVINCE.md`'s frontier table is unchanged (named by the report) |
| depth | unchanged | no depth claim; the new gate's selftest and the knowledge entry are not a depth re-verification of an existing entry |
| freshness | unchanged | no re-verification claim; S596 is new ground, not a stale entry re-verified |
| adjacency | unchanged | no sibling surface touched; the new tool reads only lane record carriers and spawns only pinned read-only commands |

No axis is harmed. The lowest-non-retired-axis rule is satisfied: depth/freshness/calibration
are tied at the floor (5) and C2 works calibration; C1 works operability (7).

## No axis harmed — receipts

- Axis scores: `git diff d144672c 142998f5 -- SCORECARD.md` leaves the `## Axes` rows
  byte-identical; scores 6 (coverage), 7 (operability), 5 (depth), 5 (freshness), 5
  (calibration), 6 (adjacency).
- Round diff: 50 paths, all lane-owned; `PROVINCE.md` gains one inventory row; `SKILL.md`
  gains registry row 15 and corrects row 14's wording; `QUALITY.md` and `SHONEN.md` unchanged;
  no existing instrument byte changed except the two r80 counters' implementation fixes and
  their following selftest-case additions.
- Batteries (read): `BATTERY13 pass=13 total=13`; `BATTERY pass=57 setup=4 fail=0`
  (`evidence/battery-r81.txt`).
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
  → rc 0, `mori ok`, 369 rows, malformed 0, 35 tolerated W04 duplicate-URL warnings.
- Append-only: `appendonly_violations=50` at entering and at the tip; registry
  `registered=61 unregistered=2 no_selftest=0 duplicate=0 wrong_row=0` (`REGISTRY=unmet` at
  entering and tip, the two unregistered pre-existing); pin-check at both revisions
  `mismatches=0`, `unparsed=1` (the pre-existing 9-cell row), `no_command=0`.
- Lane tree: clean, `ahead=0`; the round's `/fast/scratch/hyaku/mori-r81` tree is removed;
  the fleet repo shows only orchestrator `.scratch/` state and the pre-existing 24-byte
  `after` file.

## Discernment spot-check (checked from outside)

The round's `## Gate` records one admitted source (S596), a duplicate rejection (Python
`os.DirEntry.is_dir`), an unreachable rejection (ACM artifact badging), an over-broad-reading
rejection, and the `merge/mori` refusal. I sampled the admit, the duplicate rejection and the
unreachable rejection, and re-checked the new registry row's located quote.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S596 — Linux man-pages stat(2), tier A, scope "the file type carried in st_mode and the lstat() field guarantee" | admit | Pinned copy `corpus/evidence/sources-r81/stat.2.man-pages-6.19.html` (sha256 `0067346d…`, 25836 bytes / 544 lines); `nl -ba` lines 234-236; row `S596` in `corpus/SOURCES.md:377`; entry `corpus/knowledge/record-claim-integrity-r81.md:1-3` | **agree** | The located sentence is the 22-word lstat()/st_mode span (≤25 words), lines 234-236 are inside the POSIX paragraph (not the file header), tier A fits official man-pages docs for this scoped type-bit claim, and the row is the registry's next unused id (S596; no duplicate id or URL) and is cited by the knowledge entry |
| Python `os` library, `os.DirEntry.is_dir` — reject as a second row | reject | Pinned copy `corpus/evidence/sources-r81/python-os-3.15.2.html` lines 3446-3449; existing `S068` at `corpus/SOURCES.md:74` (same base URL `docs.python.org/3/library/os.html`) | **agree** | The quote "Return True if this entry is a directory or a symbolic link pointing to a directory" is 16 words and located as claimed; the page is a new section of an already-registered base URL and adds no ground the stat(2) type bits and S068's lstat scope do not carry. Note D81-5: the exclusion is recorded in the search log and lesson, not as a `rejected` SOURCES row — the contract's duplicate rule supports that, but the report should say so |
| ACM artifact review and badging — unreachable, not a row | reject (unreachable) | Live `curl -sS -o /dev/null -w '%{http_code}'` to `https://www.acm.org/publications/policies/artifact-review-and-badging-current` on 2026-11-04 → **403** | **agree** | No quote can be located; the round correctly neither admits nor rejects on content, names the flip condition, and files no row; an unreachable source is a lead, not evidence |
| New `SOURCES.md` row quote check (contract rule 1) | admit | Row `S596` anchor cell (pin lines 234-236, sha256, 25836 bytes/544 lines) vs the lesson's located quote | **agree** | The row's anchor and the lesson's quote resolve to the same bytes; the quote is 22 words, the id is unique, `status=mined`, `recheck 365d`, `used-by` names the entry, and the entry opens with `source:`/`verified-at:`/`recheck:` lines |
| Census at round end | pass | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → rc 0, `mori ok`, 369 rows, 35 W04 warnings | **agree** | The after-count matches the report (368 → 369, one A row, malformed 0); the warnings are the same tolerated class as at entering |

## Trend verdicts

- **expansion: improved** — one new admitted `knowledge/` entry on ground the coverage map
  did not hold (record-claim integrity as a cell-value discipline), `source: S596` on a
  `mined` row opened, pinned (`sha256 0067346d…`, 25836 bytes / 544 lines) and quoted this
  round; my count reads 368 rows at `44bc941a` and 369 at the tip, malformed 0, census rc 0;
  the coverage map gains the round-81 row (`corpus/README.md:877`) and the record-sweep
  capability enters the SCORECARD capabilities table in the same round.
- **quality: improved** — the seven routed r80 counter exposures are closed with fixture
  arms and a byte-unchanged r80 contract; the r81 keepers' control corrections were made
  pre-data and their entering controls re-measured; five mutation survivors are killed by
  failing arms in the committed recheck; the wider battery reads `pass=57 setup=4 fail=0`.
  Counterweights, routed: D81-1 (wrong measured-revision label on the new 240 cell), D81-2
  (no lane-committed C2 after-receipt), D81-3 (mutation harness path is scratch-only), and no
  new `QUALITY.md` criterion for the revision-label class this round added.
- **discernment: improved** — the r80 closure's D80-1..D80-4 are discharged against receipts
  (3 PENDING cells filled at `97ce0c96`, the 232→233→240 count history named, the r80
  contract shorthand corrected in prose with the frozen bytes untouched, `97ce0c96` named as
  the measured revision); the three pre-data counter amendments are disclosed with
  re-measured controls; the invalid first mutation receipt is named rather than deleted. This
  spot-check agrees with the sampled admit and both reject-class decisions. Named weakness:
  the source Gate is admit-one-with-three-refusals, and the new D81-1 record error was not
  caught by the lane's own sweep because its pinned arm compares values, not revision labels.

## Routed defects the lane must fix next round

1. **D81-1 (status-neutral, SCORECARD measured-revision label).** The r80 capability row
   (`SCORECARD.md:4036`) states `CLAIM_SWEEP … pointers=240` and says it was "re-run
   2026-11-04 at this round's record commit `075574c8`". At `075574c8` the graded pointer
   count is **237** (my replication; the lane's own `b10e91ee` subject says "pointers=237
   measured at 075574c8"), and **240** first holds at `482dc48d` and at the tip. The count at
   the tip is correct; the revision label is false, and it is a repeat of the D80-4 class in
   lane bytes. Fix: append a named correction naming the actual measured revision (482dc48d
   or the run revision) beside the 240, never rewrite the frozen predicates; consider a
   correction-sweep rule for revision labels (the existing pinned arm cannot see them).
2. **D81-2 (status-neutral, C2 after-receipt not in the lane).** The `C2=met pending=0
   pinned=0 tool=present agree=1` reading at the final tip exists only in the fleet report
   and the lesson's prose; the SCORECARD Round-81 table says "at the landed record commit"
   without a hash. Fix: commit a C2 after-run receipt at a named revision (as the round did
   for the pin-check receipt at `142998f5`), or name the exact revision in the row and the
   receipt that carries it.
3. **D81-3 (status-neutral, mutation receipt not re-runnable).** `evidence/mutation-recheck-r81.txt`
   cites the harness as `/fast/scratch/hyaku/mori-r81/l1/mut5.py`, which was removed at
   landing. The five mutant anchors and the pristine runs are committed in
   `.ufo/waves/round-81/w1/Mo81M01Mutants.md`, so the receipt is reconstructible, but the
   receipt's own command no longer resolves. Fix: commit a self-contained re-run harness
   beside the receipt (or make the receipt a reproducible command over committed bytes).
4. **D81-4 (status-neutral, route-map precision).** The dispatched prompt quotes the
   2026-11-03 net map (only reviewer on `@m_zfl`); the live `~/.omp/agent/config.yml` was
   changed at `2026-11-04 01:09:53` to also put critic, executor, mutation-tester, connector,
   sentinel and scribe on `@m_zfl`, and the report's parenthetical repeats the pre-split map
   (and contradicts itself on scout). No model was passed and no claim depends on it. Fix:
   record the config revision (or each seat's actual answering model) in the report; the
   prompt's map is operator-side and should be reconciled there.
5. **D81-5 (status-neutral, frontier attribution and reject recording).** `Sources & frontier`
   says S596 grounds "the directory-vs-instrument boundary of the new record gate"; S596
   grounds C1's B6 fixture and the knowledge entry's row 4 (the r80 `count-c3` directory
   typing), not the record-sweep tool. The Python rejection is in the search log and lesson,
   not a `rejected` SOURCES row; name the contract's duplicate-rule basis and label the
   round's sourced claim (C1's B6 reading) explicitly.
6. **D81-6 (status-neutral, entering revision naming).** The contract, lesson and report name
   entering `44bc941a`; the lane HEAD before the round was `d144672c` (the r80 verifier
   spotcheck commit, the direct parent of the freeze commit `6b021d29`). The measurements at
   `44bc941a` are valid (the spotcheck file is not a claim carrier; the r80 real arms were
   re-read at `ed2f3e11`), but the record should name the actual pre-round HEAD or qualify
   `44bc941a` as the lane-authored tip.

## Residue and operator notes

- The four `SHONEN.md` boxes look checkable by a non-author from committed bytes (decision
  tables/registry rows, the logged end-to-end round work, the runnable counter/contract
  instructions, and the diff-scoped no-bleed check); the file still carries `[~]` only, and
  promotion is operator-owned. This reviewer writes no `[x]`.
- No tool was installed or upgraded; no pacman transaction was run; no lane, OS, unit,
  credential or orchestration state was changed.
- The three mori L0 lines the report names (round-62 wave-surface waiver, round-65
  instrument-change ruling, round-73 label-sweep instrument) are present and unanswered;
  no new line was filed. Older mori L0 lines remain in the file and are not restated here.
