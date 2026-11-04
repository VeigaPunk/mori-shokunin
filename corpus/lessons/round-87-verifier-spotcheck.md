author: hyaku closure (non-author integrator, @m_zfl)
round: 87 · lane: mori · date: 2026-11-04 · attempt 1
entering revision: `6fc09d69edbb11e5070ff33258de49f062c0fb9b` · measured after: `1c9de5f56c62f3fa7f88ce00319d3389e3a49053`
report: `.ufo/reports/round-87/mori.md` (fleet repo, `mori-shokunin <mori@shokunin.local>` at `e00b9ace`, pushed)

This is the non-author closure review: I did not author this round and changed nothing in it
except this file. The two round-87 counters were **not executed** (PROTOCOL §Gate standard, Closure
consequence); their committed receipts and the claimed numbers were verified, and each before→after
was re-derived over committed bytes with plain `git show` / `grep` / `sha256sum` / `python3` reads.
Before this file `jj-lane.sh state` reported `branch=master local=1c9de5f5… remote=1c9de5f5…
ahead=0 behind=0 head=detached tracked=0 untracked=0`, `git status --porcelain` was empty, and
`git ls-remote origin refs/heads/master` printed the same `1c9de5f5…`.

## Step-1 conformance

| check | result | evidence |
|---|---|---|
| report committed by the lane identity | **pass** | `git log --format='%an %ae %H %ad %s' --date=iso -- .ufo/reports/round-87/mori.md` → `mori-shokunin mori@shokunin.local e00b9acee7cab41fdd41140941bcc5f66094d58d 2026-11-04 10:33:57 -0300 round-87: mori report` |
| report pushed | **pass** | `git merge-base --is-ancestor e00b9ace7cab41fdd41140941bcc5f66094d58d refs/remotes/origin/master` holds |
| `SHONEN` heading, one line per box | **pass** | `grep -c '^## SHONEN'` → 1; four `^- \[~\]` lines (one per `SHONEN.md` box); `grep -c '\[x\]'` → 0 |
| every cited lane commit exists and is an ancestor of the branch | **pass** | 15/15 hashes (`142542e0`, `03b66a43`, `98f48dba`, `b9e6f68d`, `728bc5f4`, `a42b1d79`, `1523b6cf`, `a90126ef`, `859b7e9a`, `22fa2919`, `c05b1cad`, `6056d001`, `31982062`, `442b108f`, `1c9de5f5`) pass `git merge-base --is-ancestor <hash> master`; all 15 carry the `mori-shokunin` author |
| lane repo clean and pushed | **pass** | `jj-lane.sh state` → `ahead=0 behind=0 … tracked=0 untracked=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` = `1c9de5f5…` |
| prompt carries the template contract | **pass** | `.ufo/prompts/mori-round-87.md` (705 lines) = `templates/round-prompt.md` §1–5 rendered for `mori`/87/fleet-root/lane-repo plus the hyaku §6 addendum. Round-level items present: MISSION/AXES binding L3–9, L2 floor L80–98, commit-then-push L133–134, push scope L135–137, L0 side channel L138–140. Five child-lane items present: report path/filename L101, commit-before-report ordering L514 (“the report lands last and cites the pushed lane hash”), `SHONEN` heading requirement L118, commit-hash citation rule L106–107, write scope L580. The prompt itself is committed at `7d14cf5e` under the lane identity, the same run-15 dispatch-evidence convention as mori rounds 80–86 and the other lanes |
| marker vs report | **report** | 280 lines, real committed work, a `LOG.md` Round 87 entry, and 15 resolvable hashes; not a completion marker |
| dispatch / completion digest | recorded | `2026-11-04T10:06:52-03:00 launch mori round=87 pgid=1392105 driver=hyaku-inline attempt=1`; `2026-11-04T10:34:59-03:00 complete mori round=87; hyaku-inline attempt=1` |

### Conformance defects (status-neutral, none bars admission)

1. **Probe survivor count off by one.** Work performed says the probe “scores 23 candidate mutants
   … and reports 16 survivors”; the receipt carries **17** (`grep -c 'survived'
   .ufo/waves/round-87/evidence/probe-r87.txt` → 17; `grep -c '^MUTANT'` → 23; `killed` → 6). No
   counting command is given for 16. The six declared mutants are all among the 17 survivors and map
   to the six frozen anchors, so the population selection is sound; the sentence is not.
2. **No round-87 gate-registry row.** `SKILL.md` `## Gates` ends at the r86 row (registry row 20);
   `grep -n 'round-87' SKILL.md` is empty, although r83–r86 each register their counters as gate
   rows and `.ufo/waves/round-87/count-c1.py` / `count-c2.py` have the gate shape (0/1/2 verdict,
   `--selftest`, in-repo pinned expected values). PROTOCOL §Gate standard *Delivery*: closure grades
   no gate conformant until its registry row exists. Routed to round 88.
3. **Two tip re-runs have no committed stdout.** The report states both targets still hold at
   `6056d001` (`rev=6056d0010250`), but no committed receipt carries that revision. The claim is
   derivable: the three r86 subject counters and the seven population receipts are byte-identical at
   `6056d001` and `1c9de5f5` (`git rev-parse 6056d001:<path>` == `1c9de5f5:<path>` for all ten), and
   the two r87 counters' sha256 at HEAD equals the receipt's. Receipt gap, not a false claim.
4. **P-C2 is not literally true at its own named revision.** At R = `98f48dba` the counter still has
   `SUBJECT_ARMS = 11`; `met` exists only with the A1 counter at `b9e6f68d`. Erratum E1
   (`contract.md:89-97`, appended post-data) names the canonical grading form (counter bytes
   `b9e6f68d` over subject `98f48dba`) and corrects A1's timing sentence. Disclosed, appended, and
   no target/population/rule moved — a precision defect, recorded as such.
5. **Abbreviated control output.** `evidence/supersede-controls-r87.txt` prints both call-site
   outputs with `...`, so the fix's able-to-fail evidence is not verbatim stdout.
6. **Selftest tallies have no verbatim receipt.** `C1_COUNTER_SELFTEST pass=18 fail=0` and
   `C2_COUNTER_SELFTEST pass=17 fail=0` are cited in `SCORECARD.md` and the seat reports, but no
   `evidence/` file carries them. They are statically derivable (`grep -c 'cases.append('` → 18 / 17)
   and are implied by each `met` line's own-selftest conjunct.
7. **Inherited, not re-litigated.** The round-86 spot-check's eight routed defects stay open
   (`corpus/lessons/round-86-verifier-spotcheck.md`); this round reports them as inherited.

## Claim re-checks (commands and observed output)

### C1 — operability: six surviving r86-counter clauses get the failing arm each

- **Arm counts, static, at both revisions** —
  `git show <rev>:.ufo/waves/round-86/count-c1.py | grep -c 'cases.append('` → **15** at
  `6fc09d69` and **18** at `1c9de5f5`; `count-c2.py` → **11** → **13**; `count-c3.py` → **22** →
  **23**. Totals: **48 → 54**. The reported 15/11/22 → 18/13/23 and `arms=48` → `arms=54` are
  re-measured, not merely quoted. The two new counters carry 18 and 17 arms respectively
  (`grep -c 'cases.append('`), matching the claimed `pass=18` / `pass=17`.
- **Anchors** — each frozen `old` string occurs **exactly once** in its named counter at
  `1c9de5f5` (M1/M2/M3 in r86 `count-c1.py`, M4/M5 in r86 `count-c2.py`, M6 in r86 `count-c3.py`);
  each also occurs once at `6fc09d69` — the clauses pre-exist, the six *arms* are the new work, which
  is what the claim says.
- **Committed after-receipt** — `.ufo/waves/round-87/evidence/after-r87.txt` carries the six lines
  `MUTANT <file> M1…M6 killed rc=1` and the summary
  `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54 rev=03b66a437e68`.
  Its `# rev:` is `b9e6f68d…`; `sha256sum` of the two counters at `b9e6f68d` is
  `e2ff968721678cc61d6a1674def8da3e27a43f3fed8daab79d53c657ae2c266e` and
  `264a43f04af1f9f939da7b3890f608a669a0c7fc2922656ee83f35adb236b14d` — exactly the receipt's
  `# counter-sha256:` lines (recomputed). Both digests are unchanged at `1c9de5f5`.
- **Control** — `evidence/controls-r87.txt` §C1:
  `C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=48` (rc 1), and the label-only fixture also
  reads `survivors=6`; labels and tallies alone are refused.
- **Re-measured:** arm counts/totals, anchor uniqueness, digests. **Evidence-verified:** the six
  kill outcomes (receipt above plus the wave's `Mo87E01C1Arms.md`, which reports each killer to be
  the newly added arm and the sole killer). Verdict: **improved**.

### C2 — calibration: legacy receipts retire only to replaying successors

- **Population** — at `6fc09d69`: **5 present / 2 absent** (the two r87 successors do not exist);
  at `1c9de5f5`: **7 present / 0 absent**. Re-derived by `git show <rev>:<path>` over the seven
  receipt paths listed in the counter's `POPULATION`.
- **Bindings** — **9** `# counter-sha256:` lines across the seven receipts; **9/9** recompute:
  each named path's bytes at the receipt's own `# rev:` hash to the recorded value
  (`git show <rev>:<path> | sha256sum`). Both receipt revs (`25a74d4c…`, `87644619…`) are ancestors
  of `master`.
- **Header counts** — `revs=7`, `limits=7`, `cmd=7`, `summary=7` (the body carries the population
  token in 7/7), `replay=4` (2 `required`, 2 `clone`). Static parse over the committed bytes.
- **Supersede** — the only two `# supersedes:` edges are `record-sweep-r87.txt →
  record-sweep-r85.txt` and `claim-sweep-r87.txt → claim-sweep-r85.txt`, so `superseded=2`;
  `after-r85.txt` has no superseder → `legacy=1`. `matched=6` / `defeated=1` equal the population
  table's six `met` expectations plus the one `reject` receipt.
- **Committed after-receipt** — `evidence/after-r87.txt` records
  `REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1`,
  `REPLAY claim-sweep-r87.txt mode=clone rc=0 exported=1`, `RECEIPT … met problems=-`, and the target
  line `C2=met … superseded=2 legacy=1 unexpected=0 rev=98f48dba3267`.
- **Re-measured:** population existence, the 9 digest bindings, replay/legacy classification and the
  supersede edges. **Evidence-verified:** the two clone replays' body equality (reviewer
  `Mo87R02ReviewC2.md` reproduced both successors byte-for-byte in a fresh `--shared` clone) and the
  one `defeated=1` receipt; I did not execute the counter. Verdict: **improved** (score held at 5),
  with the disclosed instrument defect below, which does not change the measured data.

### The disclosed C2 falsifier — ruled, not ignored

The wave's attacker reached the exact target line with **zero replays** (fixture `85e8bd76`) by
stripping the `# replay:` headers: the r87 grammar dropped r86's `missing-replay` problem, so such a
receipt is neither flagged nor replayed. The reviewer's F2 adds a vacuous `# cmd:` path (fixture
`47217847`). These make the *rule* forgeable and are truthfully disclosed by the lane; they do not
make the committed data forged — both successors carry `# replay: clone`, both are digest-bound to
the tool they name, and both were replayed. The claim's frozen before→after verifies; the guard is
incomplete. Calibration is therefore **improved** (the lane caught and reported its own overreach)
and the guard gaps are routed to round 88.

## Axis verdicts

| axis | verdict | reason |
|---|---|---|
| operability | **improved** | six arms added (15/11/22 → 18/13/23, re-measured), six mutants each killed by its new arm, both new counters `--selftest`-bearing; score held at 7 |
| calibration | **improved** | two `legacy` receipts retired by replaying successors (`legacy=3 → 1`, re-derived), a defect caught before data and fixed with a failing control, a material falsifier disclosed and routed; score held at 5 |
| coverage | unchanged | no new measured surface claimed; one knowledge entry inside `PROVINCE.md` scope |
| depth | unchanged | decision table and limits added to the corpus, no new domain surface |
| freshness | unchanged | the two successors are dated at their own revisions; no drift pin changed |
| adjacency | unchanged | connector names tameshi/mado/kotodoma complements, absorbs nothing; `PROVINCE.md` untouched, no sibling scope claimed |

Trade check: `git diff 6fc09d69 1c9de5f5 -- SCORECARD.md` is one hunk — the `## Planned (round 87)`
block is replaced by the round-87 section, two capability rows and `## Planned (round 88)`; no axis
row or score changed (scores 6/7/5/5/5/6). `git diff --diff-filter=D --name-only 6fc09d69 1c9de5f5`
is empty.

## Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S603 — git-clone(1) | **ADMIT** (tier A, `docs`, `mined`) | `https://git-scm.com/docs/git-clone`, re-opened 2026-11-04 | **agree** | HTTP 200, 0 redirects, 107882 bytes / 3391 lines, sha256 `d31b6c9f293a5dfc52c551b86be211b2d6dad3d2b4cf0d9c696d5fbed713554a` — exactly the row's and the gate's recorded values. Both quotes occur **exactly once** in the tag-stripped joined text at the stated raw lines: 2627-2628 (18 words) and 2696-2699 (16 words) |
| a second row for S600's URL | **REJECT** (duplicate URL + scope) | `https://reproducible-builds.org/docs/definition/`, re-opened 2026-11-04 | **agree** | HTTP 200, 0 redirects, 37681 bytes / 3662 lines, sha256 `a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb` = S600's registered sha, so the same page under the same scope; the recorded flip condition (a different, freshly pinned scope on that page) is the right one |
| S600 re-opened, `used-by` changed | **RE-OPENED, no status change** | same URL | **agree** | bytes byte-identical to the registered sha; the S600 diff is the `used-by` cell only — `corpus/knowledge/receipt-provenance-r85.md` → `corpus/knowledge/receipt-provenance-r85.md, corpus/knowledge/receipt-supersede-r87.md`; `status`/`opened`/`recheck` unchanged |

The one new row (S603) satisfies the per-row requirement: the lesson's `## Gate` records its URL,
access date, and two located ≤25-word quotes (18 and 16 words). Census:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
→ `mori ok …` rc 0, 35 `W04` warnings (the entering tolerance), zero `E` codes; row count
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **375** at
`6fc09d69`, **376** at `1c9de5f5`, matching the report.

## Trend verdicts

- **expansion: improved.** One admitted entry on ground the coverage map did not hold —
  `corpus/knowledge/receipt-supersede-r87.md`, indexed by a new `corpus/README.md` row — citing
  **S603**, a `mined` tier-A row opened this round; registry 375 → 376, append-only, census rc 0.
- **quality: improved.** Two weaker records superseded by stronger replaying successors
  (`legacy=3 → 1`, re-derived), both frozen targets met, two counters gained 18/17 arms, and no
  admitted entry fails its re-check. The C2 falsifier is disclosed and routed rather than left
  unmarked, so it does not grade quality `harmed`.
- **discernment: improved.** The round's own header-only control caught `supersede-by-presence`
  before data and the fix is shown able to fail (`superseded=2 legacy=1` pre-fix vs
  `superseded=0 legacy=3` fixed, `evidence/supersede-controls-r87.txt`); one rejection carries its
  flip condition; both spot-checked gate decisions agree.

## Routed defects for round 88

1. Register `.ufo/waves/round-87/count-c1.py` and `count-c2.py` as gate rows at the lane's registry
   home (`SKILL.md` `## Gates`, next row 21) — Gate standard Delivery.
2. C2 replay refusal: restore the `missing-replay` problem and arm the stripped-header population
   (fixture `85e8bd76`); the target line must not be reachable with zero replays.
3. C2 `# cmd:` binding: require every `# counter-sha256:` path to appear as a `# cmd:` token, plus an
   arm (F2, fixture `47217847`).
4. `supersede_absent_target` cannot distinguish “successor unclean” from “target absent”; the
   `SUPERSEDE … absent=1` branch has no arm.
5. F3 hermeticity: the two r86 `required` receipts replay against the host lane path, so `replay=4`
   is host-local; move them to clone mode or record the limit in the graded row.
6. Report precision: correct “16 survivors” to 17 (or give the command that yields 16).
7. Evidence precision: add verbatim stdout for the two counters' selftests and for the `6056d001`
   re-runs, and stop eliding control outputs with `...`.
8. Carry, not re-litigated: the eight round-86 routed defects.

## Note for the operator

No `[x]` was written here or in `SHONEN.md`; all four report lines are `[~]`. On current evidence the
four boxes look fully checkable by a non-author — decision tables plus a twenty-row gate registry in
`SKILL.md`, end-to-end rounds logged in `LOG.md`, runnable commands with `--selftest`, and
`PROVINCE.md` unchanged with the new entry's Limits inside lane scope — so a promotion review is
available to you; promotion remains operator-owned. Routed defect 1 (gate registration) should land
before any review treats the round-87 counters as conformant.
