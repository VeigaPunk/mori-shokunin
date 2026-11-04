author: hyaku closure (non-author integrator, @m_zfl)
round: mori 84 (lane round 84, attempt 1) — non-author closure verification
report: `.ufo/reports/round-84/mori.md` (fleet repo, `2c53c51d` + `afbb6796`)
lane repo: `mori-shokunin` @ `72fc09247aae134057336e99f7db34a7123d5759` (branch `master`, pushed)
entering: `5adf4337b6510dd246b247092c11cbaa97c930d3`
dispatch digest (copied from `.ufo/watchdog.log`, mutable):
`2026-11-04T06:21:52-03:00 launch mori round=84 pgid=482385 driver=hyaku-inline attempt=1`
`2026-11-04T07:24:22-03:00 complete mori round=84; hyaku-inline attempt=1`

This reviewer authored no part of the round. Claims were re-derived with plain measurements over
committed bytes and compared with the reported values; where a claim rests on a lane-owned counter
or selftest, its **committed evidence** was verified and the instrument was not executed
(PROTOCOL §Gate standard, Closure consequence). No lane-authored file (report, SCORECARD, LOG,
lessons, SKILL, PROVINCE) was edited and no `[x]` was written into `SHONEN.md`.

## Conformance (step 1)

| Check | Result | Evidence |
|---|---|---|
| Report committed in the fleet repo by the lane identity | pass | `git log --format='%an %ae %H' -- .ufo/reports/round-84/mori.md` → `mori-shokunin mori@shokunin.local 2c53c51d…` (204 lines) and `afbb6796…` (+5, misroot-sweep note) |
| Report lands after the lane's work | pass | report committer `2026-11-04T07:22:40-03:00` / `07:23:02`; lane tip `72fc0924` committer `07:21:39` |
| `SHONEN` heading, one line per box | pass | report `## SHONEN` with four `[~]` bullet lines, each with a resolvable pointer; lane `SHONEN.md` carries the four canonical boxes and no `[x]` (its diff only appends r84 evidence to the four `[~]` lines) |
| Every cited lane commit exists and is an ancestor of the branch | pass | 13 hashes tested (`5adf4337 daa77bd5 dbdb1aaa 39190f8a 5a231ef8 4a83e6aa 0a843033 792a824d da7631f4 d9574692 72fc0924 fce96d1f c4845c83`), `git merge-base --is-ancestor <h> master` → all ancestor |
| No uncommitted round work; pushed | pass | `jj-lane.sh state` → `branch=master local=72fc0924… remote=72fc0924… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` = `72fc09247aae…` |
| Prompt committed and carries the contract | pass with defects | `.ufo/prompts/mori-round-84.md` (704 lines) at `ce0ad11e` (committed by the **lane identity** — a write-scope defect, D84-1). Its §1–§5 reproduce `templates/round-prompt.md` verbatim after substitution (only the template's placeholder working-dir line is rendered); §6 carries the five child-lane items as well (write scope at §6 line 445) and the L2 floor. The base run-15 route map is superseded by the prompt's own later line 149 (only reviewer `@m_zfl`, all other roles `@m_flash`), the same pattern the r83 closure accepted; `MISSION.md`'s route bucket is advisory by its own text |
| Real report, not a marker | pass | work performed, evidence pointers, landed changes each tied to a `LOG.md` entry (`LOG.md` Round 84), resolvable commit citations → status `ok` |
| Wave shape | pass | `w1-dispatch.json` `counts={spawn:14,resume:0,total:14}`; roles 4 executor / 3 reviewer / 2 scout / 2 scribe / 1 critic / 1 mutation-tester / 1 connector, attack 5/14 = 35.7 %; `w1-results.json` has 14 entries, two empty output (`Mo84E02C2Rows`, `Mo84R02C23`) matching the report's dead-seat disclosure; 12 seat reports on disk |
| Fleet repo cleanliness | pass | `git -C /home/vgpnk/Projects/shokunin status --porcelain` shows no file written by this lane's round; the untracked `after` (mtime 2026-11-03), `agent:/`, `round-81/kumitate.md`, `round-82/kengaku.md` and the run-state/`.ufo/l0-questions.md` modifications belong to other lanes or run state |

Status-neutral defects are named in **Routed defects**.

## Per-claim re-check

### C1 — operability (score 7) — verdict **improved**

Subject: the r83 counter family's four extra mutants (M24a–M24d, measured at `c4845c83`) get the
failing arm each needs; M24c/M24d are adjudicated equivalent behind byte coupling proofs.
Target: `C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green detector=green`.

Static re-derivation (no lane counter executed):

- Anchors, exact-occurrence count via `grep -o -F '<anchor>' <file> | wc -l` at `72fc0924`:
  M24a `killed_n = total - survivors - equivalent` (r83 `count-c1.py`) = 1;
  M24b four-space-indented `    return rc == 0 and "fail=0" in out and not FAIL.search(out)` = 1;
  M24c/M24d A2 anchors `and not unclassified` = 1 and `and residual == 0` (r83 `count-c2.py`) = 1
  each. (The contract's original table anchors, unindented M24b and the combined clause, occur 2×
  and 0× — superseded by amendment A2 and the amendment is what the counter grades.)
- Coupling markers at the graded revision, exact count 1 each:
  `agreed == len(snapshot_tokens)` (line 290), `residual += duplicates` (272), `duplicates == 0`
  (289).
- New arms present with their assertions: `blind_case_tally` (r83 `count-c1.py:274-276`, asserts
  `killed=1 survivors=1 total=2` and `not met`, the A4 correction) and
  `green_requires_fail_zero` (`:280-285`, `SELFTEST skipped` fixture → `pristine=red`, unmet).
- Arm tally by `grep -c 'cases.append(('` in `selfcheck()`: 6 at `5adf4337` → **8** at HEAD.
  `git diff --stat 5adf4337 72fc0924 -- .ufo/waves/round-83/count-c1.py` = **1 file changed, 23
  insertions(+)**, a single insertion inside `selfcheck()`; `green()`/`killed()`/`grade()` bodies
  untouched.
- Committed evidence: `evidence/controls-r84.txt` entering control `C1=unmet harness=absent`
  rc 1; `evidence/controls-verify-r84.txt:22` and `controls-r84-defeated.txt` freeze population
  control `C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 total=4 pristine=green
  detector=green` rc 1; `evidence/after-r84.txt` `C1=met mutants=4 killed=2 equivalent=2
  survivors=0 total=4 pristine=green detector=green` rc 0 at `da7631f4` (10:17:36Z) and
  `d9574692` (10:21:29Z), per-mutant lines `M24a killed rc=1`, `M24b killed rc=1`,
  `M24c equivalent rc=0`, `M24d equivalent rc=0`.
- Graded bytes stable: `git show <rev>:<path> | sha256sum` for the r83 counters and the r84 counter
  is identical at `da7631f4` and the tip, so the receipt applies to the final tree.

Verdict **improved**: the claim's subject changed by exactly the two arm additions plus zero
body edits, both exemptions carry their coupling marker exactly once, and the target line is the
committed receipt. Evidence-verified, not re-executed.

### C2 — calibration (score 5, tied lowest) — verdict **improved**

Subject: `tools/mori-record-sweep.py` grades every row the anchor selects on both sides
(`ALL_ANCHOR_ROWS`), with two defeated ambiguous fixtures and three real frozen bindings.
Target: `C2=met arm=all-rows defeated=2 fixtures=3/3 bindings=3 revisions=0 arms=44`.

Static re-derivation:

- `grep -n 'ALL_ANCHOR_ROWS\|def anchor_rows' tools/mori-record-sweep.py` → marker at :119,
  `anchor_rows()` at :122-125; `contains_anchored()` applies it to the `git show <rev>:<path>` blob
  (:130-131) and `revision_sweep()` reports the first failing carrier row as `row-value` (:139-146)
  and the blob mismatch as `rev-bytes`. Both sides are all-rows.
- Four new arms exactly: `carrier-all-anchor-rows-green` (:307), `-red` (:310),
  `rev-all-anchor-rows-green` (:314), `rev-all-anchor-rows-red` (:317). The red fixtures put the
  failing value on the **second** selected row (carrier) or in a second blob row (revision), so a
  first-match tool reads them green — they genuinely exercise the rule.
- Arm tally by AST over the `check(...)` calls in `selftest()` (40 literal + one 4-item loop):
  **40** at `5adf4337` → **44** at HEAD; the entering arm-name set is a strict subset (only the four
  additions). `git diff --stat 5adf4337 72fc0924 -- tools/mori-record-sweep.py` = 1 file changed,
  33 insertions, 9 deletions (the deletions are the replaced first-match expressions).
- Frozen bindings: `.ufo/waves/round-82/record-pins.json` has `revisions[]` = exactly **3**
  (`row_tally=19` @ `075574c8`, `survivors=0` @ `075574c8`, `wrong=0 fixtures=7` @ `482dc48d`),
  `bindings[]` empty; all named revisions exist as commits.
- Anchor populations (`git show <rev>:SCORECARD.md` read as bytes): at `075574c8` `row_tally=19`
  selects 1 row carrying the token and `survivors=0` 1/1; at `482dc48d` `wrong=0 fixtures=7`
  selects 1/1; at `da7631f4` `survivors=0` selects **5** rows, all carrying the token; at the tip
  it selects 7, all carrying the token — the binding stays green and `revisions=0` holds. (The
  contract's "five rows" is exact at `da7631f4` and descriptive-only at the tip.)
- Committed evidence: entering `C2=unmet arm=absent` rc 1; freeze `C2=unmet arm=absent` rc 1;
  after `C2=met arm=all-rows defeated=2 fixtures=3/3 bindings=3 revisions=0 arms=44` rc 0 at
  `da7631f4` and `d9574692`; `RECORD_SWEEP_SELFTEST pass=44 fail=0` in
  `evidence/battery-r84.txt:403`.

Verdict **improved**: the rule is behavioral on both sides, the arms discriminate against the
entering tool, and the tally 40 → 44 is reproduced statically. Evidence-verified, not re-executed.

### C3 — depth (score 5, tied lowest) — verdict **improved**

Subject: `.ufo/waves/round-83/count-c2.py` gains a per-token `live_delta` classification.
Target: `C3=met delta=classified tokens=64 classified=union residual=0 live=derived`.

Static re-derivation:

- `grep -n 'LIVE_DELTA\|def live_delta' .ufo/waves/round-83/count-c2.py` → classifier definition
  :90, one `LIVE_DELTA <token> <class>` line per non-agreed token at :328, call at :282; the four
  delta arms exist (`delta_absent_live`, `delta_added_live`, `delta_class_changed`,
  `delta_agreed`), 0 occurrences at `5adf4337`.
- Arm tally by `grep -c 'cases.append(('`: **12** at `5adf4337` → **16** at HEAD.
- A7 preservation list, exact count 1 each: `and not unclassified`, `and residual == 0`,
  `agreed == len(snapshot_tokens)`, `residual += duplicates`, `duplicates == 0`.
- r84 counter (`count-c3.py`) grading, read from bytes: imports the extracted subject under
  `contextlib.redirect_stdout` and catches `(Exception, SystemExit)` (→ `import-failed:<type>`);
  requires arms ≥ 16 and `PASS <name>` for all four delta labels; recounts the snapshot from
  `.ufo/waves/round-82/evidence/drift-r82-live.txt` and requires `tokens == recount`; grades the
  pure classifier on five frozen cases (`classifier=5/5`); requires `classified == union`,
  `residual == 0`, `live=derived`, `deltas == union - live_agree == len(pairs)`.
- Committed evidence: entering `C3=unmet delta=absent` rc 1; after
  `C3=met delta=classified tokens=64 classified=64 union=64 residual=0 live=derived
  live_tokens=64 live_agree=64 deltas=0 arms=16 classifier=5/5` rc 0 at both after revisions.
  The real live run printed zero `LIVE_DELTA` lines (all 64 tokens agreed), so the classification
  is exercised by the imported synthetic cases — the frozen predicate's named limit (A6), not a
  claim failure.

Verdict **improved**: the classifier is pure, imported and independently graded; the
preservation conjuncts survive; the tally 12 → 16 is reproduced statically. Evidence-verified,
not re-executed.

### Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1 target met; the r83 counters gained the two arms and 6 → 8 arms |
| calibration | improved | C2 target met; the record sweep now grades every selected row on both sides, 40 → 44 arms |
| depth | improved | C3 target met; per-token delta classification imported and graded, 12 → 16 arms |
| coverage | unchanged | no surface claim this round; `PROVINCE.md` Round-84 note correctly says no new census surface |
| freshness | unchanged | no score move; one stale quoted tally in a new QUALITY criterion is routed (D84-2), not a regression of an existing surface |
| adjacency | unchanged | the connector reports the contested tameshi boundary, absorbed nothing; no adjacency claim |

No axis harmed: `git diff 5adf4337 72fc0924 -- SCORECARD.md` is additive only (the r83 score rows
and the axis table are unchanged; the round section says "No score moves"); the r83 counters at the
freeze still read their r83 `met` lines (`controls-verify-r84.txt:64-74`); the standing battery is
unchanged at `BATTERY pass=57 setup=4 fail=0`.

## Discernment spot-check (LEARNING.md)

The `## Gate` carries one admit, one reject and one no-change note. Both external decisions were
re-opened.

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S599 — arXiv:2408.01760v1 "Large Language Models for Equivalent Mutant Detection: How Far Are We?" | **admit** (tier A, paper) | pinned `corpus/evidence/sources-r84/arXiv-2408.01760-abs.html` | **agree** | sha256 `688224106999973f3b5c318af871b77923df2c36d0e3e2d799424e2c697cff49`, 42566 bytes, 597 newlines reproduce; the quoted sentence sits at body line 121 and counts 24 words ("However, the presence of equivalent mutants is known to introduce redundant cost and bias issues, hindering the effectiveness of mutation testing in practical use."); the row's scope is bounded to that premise (not an adjudication procedure), which is exactly what the abstract states |
| arXiv:2404.09241 "An Empirical Evaluation of Manually Created Equivalent Mutants" | **reject** (no row) | live `https://arxiv.org/abs/2404.09241` (fetched to stdout, not saved) | **agree on the decision; disagree on the record form** | re-fetched 40386 bytes, sha256 `4bcb20b23ad5046657a65a29595517da973128a289ff75ba13ad8926c5511a80`; the abstract defines equivalence ("mutants that differ only in syntax but not semantics"), reports a weaker "hamper this process" cost over manually created mutants in the Code Defenders game study, and carries no bias statement and no adjudication procedure (`bias*`/`adjudicat*` 0 hits) — the reason and flip condition hold; but the refusal has no `rejected` SOURCES row (D84-3) |
| S595 — arXiv:2102.11378v2 | no row change | `corpus/SOURCES.md:376` | **agree** | different document; its scope is the abstract's test-adequacy definition and its own limit line does not discuss equivalent mutants |
| Newly written SOURCES row S599 | row is a claim | `corpus/SOURCES.md:380` + pinned page | **agree** | the only added row; `awk -F'|'` on the row gives NF=13 (11 clean cells), id/kind/tier/scope/anchor/status/opened/recheck/used-by all conform; `used-by corpus/knowledge/equivalent-mutant-adjudication-r84.md` exists; the row's 24-word quote matches the lesson's located quote |
| Sources census | gate | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` | **agree** | rc 0, `mori ok`, 35 tolerated W04 duplicate-URL warnings (same class as entering), 0 malformed rows, no duplicate ids, no missing `used-by` path; rows 371 → 372 by `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` (`git show` at `5adf4337` and `72fc0924`) |

## Trend verdicts (with evidence)

- **expansion: improved** — one admitted `corpus/knowledge/` entry on ground the coverage map did
  not hold as a distinct line (`equivalent-mutant-adjudication-r84.md`, K1–K4), whose `source:`
  cites the `mined` row S599 opened, pinned and quoted this round; coverage-map row added in
  `corpus/README.md`; registry 371 → 372 by the grammar count; census rc 0; no existing row's
  status/recheck/used-by changed (diff is one row plus the search-log note).
- **quality: improved** — the round's instruments gained graded, working arms measured from
  committed bytes (r83 `count-c1` 6 → 8, r83 `count-c2` 12 → 16, record sweep 40 → 44) and three
  QUALITY criteria (170–172) were added with "shown able to fail" demonstrations; the standing
  battery is unchanged at `BATTERY pass=57 setup=4 fail=0`. Counterweights routed, not hidden: the
  mutation probe still reports `MUTANTS total=49 killed=23 survivors=26`, the C1 reviewer found two
  new surviving counter mutants (X1/X2) for r85, and the new QUALITY 172 tally is stale (D84-2).
- **discernment: improved** — the non-author spot-check agrees with the sampled admit and reject
  decisions and the new registry row; the Gate's reject is externally reproducible (same bytes and
  hash); the round discloses nine pre-data amendments and two dead seats rather than presenting
  seat output that does not exist; independent seats (S01, S02, K01, R01, C01, R03, Sc02) found the
  freeze's prose-anchor defect before any after-value, and the critic's controls that reached the
  target were defeated and committed. Named weakness: the amendments' volume says the freeze
  under-checked its own prose (the QUALITY 168 class), and the reject's record-form defect (D84-3).

## Routed defects the lane must fix next round

1. **D84-1 (status-neutral, write scope / attribution).** `.ufo/prompts/mori-round-84.md` was
   committed in the fleet repo by the **lane** identity (`ce0ad11e`, `mori-shokunin`), a path the
   integrator owns (PROTOCOL §Round-robin step 4 / §Invariants: lanes write only inside their child
   repo and their lane report). The prompt needed committing; the defect is attribution. Do not
   rewrite history; note it and leave `.ufo/prompts/*` commits to the integrator next round.
2. **D84-2 (status-neutral, stale quoted evidence + pointer drift).** `corpus/QUALITY.md` 172
   states the r84 `count-c1.py` "measured tally is `C1_COUNTER_SELFTEST pass=11 fail=0`", but the
   counter has carried **15** arms since `5a231ef8` (A5) and the same round's SCORECARD capability
   row and `SKILL.md` registry row 18 both cite 15; the criterion's `:296-300` pointer now lands on
   argument parsing, not the detector gate. Fix in r85 as a superseding criterion row (append-only)
   and cite the re-run output, not a pre-amendment session value (Evidence standard, "claimed ≠
   re-executed").
3. **D84-3 (status-neutral, registry contract).** The refused candidate arXiv:2404.09241 was not
   given a `rejected` row, although prompt §2b says "Rejections stay as rows with reason and flip"
   and `corpus/SOURCES.md` status `rejected` exists for that purpose ("kept — a rejection is
   evidence of taste"). The reason and flip survive only in the lesson Gate and the search log.
   Append the rejected row next round.
4. **D84-4 (status-neutral, receipt gap; the D82-2/D83-1 class recurring).** The report quotes two
   supporting outputs with no committed receipt or command: `RECORD_SWEEP pending=0 pinned=0
   carriers=1 bindings=3 revisions=0` and `CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0
   carriers=4 pointers=266`. Commit those runs beside the after receipt.
5. **D84-5 (minor, record precision).** `evidence/battery-r84.txt` carries no revision/date header
   although the report dates it at `da7631f4`; and the defeated-control receipts cite
   `/fast/scratch/...` clone paths that no longer resolve (recorded observations, not re-runnable).
   Add a header and a resolution note to future receipts.
6. **Minor descriptive drift (no fix required).** `contract.md` §P-C2 says the after revision's
   `survivors=0` "selects five rows"; that is exact at `da7631f4` and 7 at the record commit/tip,
   all carrying the token. Certificates are unaffected.

## Operator notes (non-lane)

- The four `SHONEN` boxes look checkable by a non-author from committed bytes (registry row 18,
  the logged end-to-end round work, the runnable keepers, and the diff-scoped no-bleed note); this
  reviewer writes no `[x]` and promotion stays operator-owned.
- Operator-side, restated from r83: `templates/round-prompt.md` carries no literal write-scope
  child item (it reaches the lane only via the addendum), and the run-15 base route map in the
  addendum is superseded by its own line 149 (not a defect of this round's prompt).
- No tool was installed or upgraded; no pacman transaction, no sibling or fleet write, and no lane,
  OS or orchestration state was changed. The dispatch/complete digests above are copied into this
  file because `.ufo/watchdog.log` is mutable.
