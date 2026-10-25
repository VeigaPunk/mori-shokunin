# Round 40 — verifier spot-check (closure, non-author)

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-24
lane tip scored: ede486b7a09afbacfb380d5871c46a8051a6dc2e (local=remote, ahead=0)
report: .ufo/reports/round-40/mori.md @ 22fc3dd (fleet repo, author mori-shokunin)
wave: 66/66 seats landed under .ufo/waves/round-40/w1/ (67 files incl. this spec's index file; w1-spec.json items=66)

## Verdict

**Rejected (rejected-honest-stop).** Both claims fail verification as frozen: C1's
predicate P-C10 ("every `timeout=` keyword … resolves in the scope of its read site …
the value must be a finite positive number") is falsified by a live new-survivor class
(walrus / tuple-unpack / dead-loop rebind — all three print `CONFORM=met` with runtime
read-site value `None`, reproduced below); C2's headline measured value ("34 as-of ids",
recorded in report, SCORECARD after-cell, LOG and lesson M24) is wrong by one — the gate
at T1 prints **35** as-of ids (re-measured below), and P-C11's words are further
contradicted on adversarial DAG classes (dag-2l walk-order arbitration, dag-h stale
global colmap, dag-z dead-branch eligible set — dag-z reproduced below). No owned axis
was harmed (diff bb1f2457..ede486b over corpus/, SCORECARD.md, LOG.md: 1084 insertions,
0 deletions), so this is a refusal of admission, not a harm ruling. All findings are
routed defects with named fixes; the lane's own disposition (M23/M24, honest stray
handling) is sound.

## Step-1 conformance

| check | result |
|---|---|
| report committed by lane identity | PASS — `git log --format='%an %H' -- .ufo/reports/round-40/mori.md` → `mori-shokunin 22fc3dd331251eb7f580f8eb48f4c32f9a5e9a65` |
| SHONEN heading, one line per box | PASS — 4 boxes ([~]×3, [ ]×1) |
| cited commits exist + ancestors of master | PASS — bb1f2457, 265a955, 8d3badd, ede486b all `merge-base --is-ancestor … master` rc=0 |
| lane pushed | PASS — `jj-lane.sh state` → local=remote=ede486b, ahead=0 behind=0 |
| no uncommitted round work | **DEFECT** — `git status --porcelain`: M `evidence/c10-after-conjunct.txt`, M `c10-after-selftest.txt`, M `c10-red-conjunct.txt` (wave-executor rewrites: absolute-path command lines + wall_seconds/timing lines; verdict bodies unchanged); untracked `.scratch/`, `.ufo/waves/round-40/scratch/mutconform-arms2/`, `.ufo/waves/round-40/w1/` (66 wave reports); stray root file `265a955` (24 bytes, "=== GATE DELTA bb1f245-", misrooted capture) |
| prompt carries template contract | PASS — rendered `templates/round-prompt.md` + hyaku addendum §6 present |

Marker predicate: not a marker (substantive report + checkable commits) → lane status ok.

## Per-claim re-check (commands run by this closure)

### C1 — conformance checker v3 (operability)

Re-measured (this session, worktree bytes = freeze pins, per ExeFreezePins all 9 pins match):

| measurement | command | observed | report says | match |
|---|---|---|---|---|
| after, record counter | `python3 .ufo/waves/round-40/conform.py 265a955cc… --counter .ufo/waves/round-40/count-c8.py` | `CONFORM=met` exit 0 (3.2 s) | met | YES |
| selftest | `… --selftest` | 11 `PASS` lines, `CONFORM_SELFTEST pass=11 fail=0`, exit 0, wall 57.234 s | pass=11 fail=0 | YES |
| after survivors (9 receipts read) | `grep CONFORM evidence/c10-after-{shadow-none,shadow-neg,cond,inf,divzero,decoy,underscore,second-popen,tuple,multicounter}.txt` | all `CONFORM=unmet` + named check FAIL + EXIT=1 | unmet + named check | YES |
| before receipts | 9 c10-red files carry `CONFORM=met`; `c10-red-divzero.txt` prints EXIT=2 (setup-error class, no CONFORM line) | "nine survivors + two-counter audit → met" | **WORDING OVERCLAIM** — 8 survivors met + divzero exit-2 class + multicounter audit (wave CritScoringHonesty finding 21; contract line 82 already concedes the class) |
| counter parity | wave ExeParity re-derived: count-c7-r39 = count-c8 delta = 5 removed lines, parity receipt byte-identical | "parity proven byte-identical" | YES (evidence-verified, not re-run) |
| **new-survivor falsification** | see below | **C1 FALSIFIED** | — | NO |

New-survivor reproduction (fixtures from wave seat CritNewSurvivor, `.scratch/CritNewSurvivor/`,
each derived from frozen count-c8.py by one insertion overriding the caller's `timeout` with
`None` inside `run`'s body):

```
$ python3 .ufo/waves/round-40/conform.py 265a955cc… --counter .scratch/CritNewSurvivor/survivor-deadloop-rebind.py
check timeout_scope PASS (… value=[]) ; CONFORM=met
$ … survivor-walrus-none.py        → timeout_scope PASS (value=[]) ; CONFORM=met
$ … survivor-tupleunpack-none.py   → timeout_scope PASS (value=[]) ; CONFORM=met
```

Runtime discrimination (this session, honest vs tampered `run`, child sleeps 2 s, caller
passes `timeout=0.2`): all three fixtures complete rc=0 in 2.01 s — the read-site value is
`None` (unbounded) while the checker resolves 120 / parameter default. Mechanism confirmed
in the landed bytes: `_function_bindings` collects `Assign`/`AnnAssign` via breadth-first
`ast.walk` and takes `local_values[-1]` (a dead nested binding outranks an earlier
unconditional rebind); `ast.NamedExpr` and `Tuple`/`List` destructuring targets are
invisible to it. This is exactly the name-not-value survivor class P-C10's words claim to
close. **The claim "v3 computes P-C10" does not verify.**

### C2 — append-only gate v3 (depth)

| measurement | command | observed | report says | match |
|---|---|---|---|---|
| before lane line | read `evidence/c11-before-lane.txt` + wave re-derivation | 18 as-of ids, S226 absent, stale empty, exit 1 | 18, S226 absent | YES |
| after lane line (re-measured) | `python3 tools/mori-sources-appendonly.py 265a955cc… --repo .` | `superseded_as_of=[35 ids S041…S226]` `stale_supersede=[]` exit 0 | **34** as-of ids | **NO — measured 35** |
| after e37dcc6 (re-measured) | `python3 tools/mori-sources-appendonly.py e37dcc6 --repo .` | as_of 33, `stale_supersede=[S069]` | stale [S069] | YES |
| gate selftest | `python3 tools/mori-sources-appendonly.py --selftest` | `pass=15 fail=0` exit 0 | pass=15 fail=0 | YES |
| dag-n/p/r receipts | read + wave ExeDagDeterminism byte-stable rebuilds | P-C11 verdicts as claimed | claimed verdicts | YES |
| **P-C11-words counterexamples** | see below | **C2 claim-as-frozen FALSIFIED** (semantic intent delivered on the lane corpus) | gate computes the predicate | NO |

dag-z reproduction (wave seat CritNewDag fixture, `.scratch/critnewdag/repos/dag-z` — the
superseding row S002 lands on a side branch whose content is discarded at the merge; at R
no row supersedes S001):

```
$ python3 tools/mori-sources-appendonly.py HEAD --repo .scratch/critnewdag/repos/dag-z --round-base <b0>
deleted S002
appendonly_violations=1 ids=[] deleted=[S002] superseded=[S001] …
supersede_timing superseded_as_of=[S001] stale_supersede=[]
```

v3 labels S001 superseded-as-of at R on the basis of a row it itself reports `deleted` —
internally inconsistent with P-C11's words ("eligible set is every superseded id present
at R"; the superseding row is not present at R). Companion classes recorded by the wave
with builder + runlog: dag-2l (identical ancestry+content, commit date alone flips
`superseded_by` S003→S002 and as_of→stale — latest-walk-index arbitration, line 348,
while the docstring disclaims walk order) and dag-h/dag-h2 (header column permutation
fabricates `changed` events + drains the timing eligible set through one stale global
colmap — inherited verbatim from v2). The sanctioned lane-history verdicts (35 as-of,
S069 stale at e37dcc6, first-parent/no-readd semantics) are correct — wave CritLaneLine
independently swept all 35 ids against `merge-base --is-ancestor` and passed each; the
claim's **measured-value layer** is what fails.

### Number-drift in the correction layer (committed)

`grep`: SCORECARD.md:2234 "measured value is **34 as-of ids**", LOG.md:2296 "lists 34
as-of ids", corpus/lessons/round-40.md M24 "lists **34** … (16 rows: S226 plus 15
earlier)". My gate re-run at T1 and the committed `c11-after-lane.txt` both enumerate 35
ids; the never-edited extension admits 17 rows (S226 + 16 earlier). M24's correction of
the frozen "(19 ids)" parenthetical recurred off-by-one — the second counting slip in the
same claim family, now standing in three committed files.

## Discernment spot-check (LEARNING.md §Discernment)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S229 admit (lesson Gate, mined) | admit | `corpus/evidence/sources-r40/S229.src` + live URL (HTTP 200) | **agree** | quote "When a name is used in a code block, it is resolved using the nearest enclosing scope." present verbatim at src line 294 (§4.2.2); grounds C1's scope-aware fold. Two defects: word count is **17**, not the 15 recorded in lesson/report; the row's located range ":254-256" resolves under neither raw-HTML (294–295) nor stripped-text (284) numbering of the copy. |
| reject sample | — none exists this round | lesson Gate: "Rejected: none new"; search log excluded 0 | n/a | nothing to sample — bounded search identified 1, excluded 0. Recorded as a thin-Gate note, not a violation. |
| S229 SOURCES.md row (new) | registry row | corpus/SOURCES.md:235 (inside ## Registry after T3 repair) | agree | quote 17 words ≤ 25; tier/scope/status cells consistent with census (`sources-census.sh validate mori` → exit 0, `mori ok`, 16 standing W04 rows = pre-existing fleet debt); locator imprecision as above. |

Census: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0 (re-run this session; matches committed census receipts' class set). Note: committed `census-end.txt` (02:50) predates the T3 S229 placement repair (02:56) — it validated the pre-repair layout; my closure-time re-run covers the shipped layout.

## Per-axis verdicts

- **operability — unprovable**: C1's declared before→after verifies on the nine enumerated
  classes (re-measured), but the frozen predicate is falsified by the walrus/tuple/
  dead-loop class (runtime read-site `None` under a `met`). The artifact is strictly
  better than v2; the claimed end-state does not hold.
- **depth — unprovable**: the lane-history verdicts verify (35 as-of incl. S226, S069
  stale at e37dcc6, selftest 15/0 — all re-measured), but the claim layer records 34
  (true: 35) and P-C11's words are contradicted on dag-2l/dag-h/dag-z classes.
- **coverage, freshness, calibration, adjacency — unchanged**: not touched this round;
  diff append-only, no registry cell edited in place.

## Trend verdicts

- **expansion — improved**: +1 tier-A row (S229, quote verified), +1 knowledge entry,
  +2 capability rows; census clean at the tip; no deletions.
- **quality — unchanged**: the declared receipt layer largely verifies (this closure
  re-measured met/selftest/unmet/stale), but the M24 correction recurred off-by-one in
  three committed files, three c10 receipts were rewritten in the worktree and left
  uncommitted, and the freeze receipt has consume-then-commit gaps (both conjunct-gutted
  interpreters ran before any commit held them; `conform-v3-conjunct-gutted.py` first
  committed at ede486b, after its receipt landed at 8d3badd). Net: no quality gain over
  the r39-routed baseline.
- **discernment — unchanged**: one admit verified (with word-count and locator defects),
  zero rejects to sample, M23/M24 self-mined honestly — but M24 itself miscounts, so the
  mined-mistake layer is not yet trustworthy.

## Routed defects for round 41 (lane must fix)

1. **C1 binding model** (CritNewSurvivor): collect function-local bindings in source
   order `(lineno, col_offset)`; count `NamedExpr`, `Tuple`/`List` destructuring, and
   loop/with targets as bindings; fail closed when a read name has multiple bindings that
   cannot linearize into one dominating last binding. Add the three fixtures as selftest
   arms; re-pin.
2. **C2 eligible-set grounding** (CritNewDag): (a) ancestry-grounded `supersede_landing`
   arbitration (no latest-walk-index date sensitivity; re-pin dag-2l both ways);
   (b) per-commit `imm_idx`/`teaches_idx` from each commit's own colmap (fixes dag-h/h2;
   inherited-from-v2 but P-C11 is this gate's frozen contract); (c) constrain `sup_map`
   eligible pairs to rows present at R, or put an explicit ruling in P-C11 (dag-z/z2).
3. **Number correction, append-only erratum line**: 34→35 and 16→17 in SCORECARD
   after-cell, LOG round-40 line, lesson M24 (and any r41 drafts); update the erratum to
   record the correction itself was wrong once.
4. **Receipt hygiene**: commit-or-revert the three modified c10 receipts; delete the
   stray root file `265a955`; commit the w1/ wave reports and scratch per lane policy or
   sweep them — uncommitted round work blocks clean closure.
5. **Freeze completeness**: pin the two conjunct-gutted interpreter bytes in
   freeze-r40.txt; re-run and persist a census receipt at the post-repair tip.
6. **Claim wording**: "nine survivors CONFORM=met" → "eight survivors + a two-counter
   audit; the divzero fixture exits 2 in setup" (dag-p "fabricated changed line" and
   dag-r `stale=[S008]` signature wording per CritScoringHonesty findings 27–28).
7. **selftest_conjunct application gap** (CritConjunctSemantics): the conjunct checks
   table presence/references, not that `selftest` applies the arm (early-continue mutant
   passes with pass=11). Strengthen to apply-then-compare.
8. **Contract reconciliation**: frozen contract promises a 64-seat wave; w1-spec.json
   carries 66 (validated, plan exit 0). Append-only note or accepted-band ruling.
9. **S229 locator/word-count**: correct the 15→17 word count; fix the ":254-256"
   located range against the committed copy's actual coordinates.
10. **Exploratory boundary note** (CritExploratoryBoundary F2): the C1 `rev` argument
    feeds only the `timeout_state` arm; `head_pin` compares live HEAD — receipts named
    "at T1" are HEAD-ede486b runs unless run in a detached checkout; bind or reword.

## Notes boundary

No SHONEN box was promoted; none is `[x]`-able by a non-author this round (no named
non-author verifier for `[~]`). The `[ ]` executable-instructions box remains lane-owned.
Wave seats were dispatched by the orchestrator (accepted host mapping); the report's
"prepared-but-undispatched" line was true at report commit time and is superseded by the
landed wave. No tools installed by this closure (python3 stdlib + git only).
