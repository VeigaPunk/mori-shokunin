# CriticC2Final — wave-2 falsification of C2 (branch-anchored census)

Attacked: delivered `tools/mori-census.sh` @ 273aa74 (sha 12e8e2d9…3d85), gate
`tools/mori-round17-jj-regressions.py` (sha 1067e4ae…e0e3), retained streams
`evidence/jj-{before,after}/` (21→0 failed assertions, cases 7/12→12/12).
Scope: off-branch credit, sibling-author rule, errors-vs-mismatches, fallback
concealment, gate realism, no-harm. Read-only inspection of code, manifests,
case streams, helper script and live refs only; no probes rerun.

## Verdict shape

The three named properties hold **in the exercised slice**: off-branch HEAD
gets no commit/closure credit (`git-detached-commit`, `jj-commit-no-bookmark`,
`git-report-off-branch` all read `silent`/`has_head=1` with the mismatch
finding), sibling `@shokunin.local` author stays quiet (`jj-sibling-author`,
CLEAN), and `merge-base` rc≠0/1 emits nothing (stub arm + code read). The
defects below are the **residual cone**: every one is a reachable repo state
the 12-case suite never constructs.

## C2-F1 — resolver drops the *recorded* branch authority; attached HEAD re-anchors the lane (defect)

`lane_branch_probe` (mori-census.sh:2110-2138) resolves `symbolic-ref HEAD →
refs/remotes/origin/HEAD → unique master/main`, copying `detect_branch`
(jj-lane.sh:115-126) — which is documented "**used ONLY by init for a first
recording**" (jj-lane.sh:113-114). The helper's steady-state read path is
`lane_branch_jj` (jj `trunk()` alias) → `lane_branch_git` (`git config
lane.branch`) → `detect_branch` → unique master/main (jj-lane.sh:387, :162,
:98-103). Live proof the authority exists and is read:
`git -C mori-shokunin config --get lane.branch` → `master` (kama, mado, souji,
tabi, tameshi, tsukuroi likewise `master`; kaidoku `main`).

Consequence: a lane whose HEAD is **attached to any other local branch**
(`wip`, a stray `topic`) resolves that branch as the lane branch. Row-9 log,
row-6 closure and `head_branch_probe` all re-anchor silently — and
`HEAD_BRANCH_MISMATCH` becomes *impossible* to fire (HEAD == the resolved ref
by construction, `merge-base` trivially rc0). The off-branch hazard is not
detected; it is renamed as the lane's anchor. Wave1 CriticC2 O3 (build/
CriticC2.md:111-117) recommended the `lane.branch`-first order; the delivered
code chose the contract-literal `detect_branch` shape, so the recommendation
stands unimplemented and the finding is unchanged.

**Smallest fix:** prepend `git config --get lane.branch` (validated by the
existing `valid_branch`) and, for colocated repos, the jj `trunk()` alias read,
mirroring `cmd_state` (jj-lane.sh:162). One extra `git config` call per lane.

## C2-F2 — fallback conceals the exact hazard class the claim targets (defect, gate-blind)

A1's "unresolved branch ⇒ exact old HEAD behavior" keeps r13-r15 byte-parity,
but the unresolved state also disables `head_branch_probe` entirely
(`if [ -n "$GL_BRANCH" ]`, census:2237): on a repo with a detached HEAD ahead
of a non-canonical branch (`trunk`), or with both `master` and `main` present
(ambiguous → no branch, census:2136), the merge-base invariant can never fire,
row 9 grades the drifted HEAD directly, and `cat-file -e HEAD:report` closes
on off-branch commits. `case_git_fallback_head` (gate :679-691) exercises only
the *benign* arm — detached **at** `trunk`'s tip — so the suite cannot see the
drifted variant. This is the direct answer to the wave question: **yes, the
fallback conceals the hazard it exists against**; C2 detection degrades to
exactly the pre-C2 blind spot in exactly the repos where branch identity is
already ambiguous.

**Smallest fix:** emit a non-roll `BRANCH_UNRESOLVED` info finding when the
resolver fails while HEAD resolves (info never flips the roll,
`emit_finding` census:411-424). Preserves byte-parity of SURFACE rows and
rolls; removes the silent re-admission.

## C2-F3 — proven mismatch withheld when the display field fails; second log error silently counts zero (defect)

`head_branch_probe`: after `merge-base --is-ancestor` returns **1** (the
mismatch is *proven*), `rev-parse --verify -q refs/heads/$branch` failing or
answering non-hex hits `|| return 0` (census:2163-2166) — the finding is
suppressed because `branch_tip=` cannot be decorated. Same class: the
committer/author second pass treats a failed `log` as `GL_AMN=0`
(census:2362-2372, `if [ "$CAP_RC" -eq 0 ]` else nothing), while the *first*
log's failure grades `unavailable` row-1 (census:2327-2331). "Errors are not
mismatches" holds, but errors are also not *anything*: a real mismatch or a
failed audit produces zero signal either way (acknowledged as silent in
build/CensusJj.md risk 2; still a defect — silence is not the stated contract,
which names only the two findings).

**Smallest fix:** on merge-base rc1 emit the finding with
`branch_tip=unresolved` when the tip query fails; on second-log rc≠0 leave
GL_AMN=0 but reuse the existing `unavailable`/`reason=` row-1 path.

## C2-F4 — root-repo drift invisible to every child lane; only `LANE_SILENT` reports the symptom (residual hole)

`head_branch_probe` runs only on `$repo` (the lane repo); the root repo's
HEAD-vs-branch invariant is never measured. Retained stream
`jj-after/cases/git-report-off-branch.out`: root HEAD detached, report
committed only off-branch → row 6 correctly does not close, lane reads
`silent` + `LANE_SILENT warn`, **no finding names the actual cause** (root
HEAD ahead of root branch). An operator is told the lane is silent; the real
fault is root-repo drift. Only `protocol`/`aggregator` (repo == `$ROOT`,
lane_repo census:1973-1977) get the mismatch check. JjGate.md:267-274 flagged
the same scope ambiguity; the delivered resolution was to not check root.

**Smallest fix:** one extra `head_branch_probe`-style pass on `$ROOT` once per
run, emitting a root-named finding — not per-lane (avoids the child-lane
misattribution JjGate named).

## C2-F5 — `LANE_AUTHOR_MISMATCH` inherits the row-9 pathspec: `.ufo`-only and child-lane-only commits invisible on root lanes (defect)

The second `log` reuses `lg_paths` (census:2362), which for root lanes is
`-- . ':(exclude).ufo' ':(exclude,glob)**/*-shokunin/**'` (census:2323-2325).
The pathspec exists to scope *progress attribution*, but the finding audits
*committer identity* — a different property. On `protocol`/`aggregator`, a
lane-committed, foreign-authored commit touching only `.ufo/**` (the F4 shape
applied to fleet-report commits) is invisible. Same bound: commits with ct >
NOW fall outside the awk window (census:2365-2366).

**Smallest fix:** drop the pathspec on the second pass only (grading pass
unchanged — rows A/C untouched per A1).

## C2-F6 — detection window is launch-bounded: closed lanes cannot be audited (limit, inherent)

`LANE_AUTHOR_MISMATCH` is computed inside the row-9 pass, reachable only for
lanes that are still open and not early-returned (rows 2/4/6/7/8 return
first). Once a lane's round closes (ledger close, report committed), in-window
foreign-author commits on its branch become permanently undetectable — next
round's launch resets the `(launch, NOW]` window past them. `HEAD_BRANCH_MISMATCH`
does not have this limit (it is computed before the early returns, census:2231-2237).
This is the mirror of wave1 O6 (transient positives): **transient detection** —
the finding can only see the defect while the round is open. Contract
window semantics are deliberate; the limit should be recorded, not fixed by
expanding the window.

## C2-F7 — gate realism gaps (no-harm evidence is thinner than the manifest implies)

1. No case where the resolver picks a ref that does not exist locally:
   origin/HEAD arm is declared exercised "only as an absent input" (gate
   docstring :35). Concretely: detached HEAD + `origin/HEAD → main` + no local
   `refs/heads/main` + lane commits on `master` → resolver picks `main`, every
   branch query fails, `has_head=0` → row-D `silent` + `LANE_SILENT warn` —
   **a false drift finding the entering census never produced** (it graded
   HEAD). C2's own origin/HEAD arm manufactures this regression shape.
2. No case for HEAD attached to a non-canonical local branch (C2-F1).
3. No case for a real `merge-base` error (rc≥128): only the stub selftest arm
   (census:4048-4057) covers it; a shallow/corrupt real repo is untested.
4. `refs_unchanged` snapshots only `HEAD` and `refs/heads/master` per repo
   (gate :447-455). In `git-fallback-head` the branch slot reads a ref that
   does not exist (`trunk`) both times — a census bug deleting/moving any
   other ref passes the no-mutation assertion.
5. `forbid` checks only the two expected finding ids; an extra, misnamed or
   duplicate `FINDING` line passes silently (gate :801-802).

## C2-F8 — confirmed non-defects (so the record is exact)

- `warn` severity flips `ROLL` (census:418-423) — a `progressing` lane in the
  helper's normal mid-commit window emits DRIFT. Contract-accepted (A1 chose
  `warn`; "drift" severity would have been *quieter*). The detail carries both
  short hashes, enabling rerun disambiguation (O6's condition). Tradeoff, not
  a defect.
- `HEAD_BRANCH_MISMATCH` fires for lanes on rows 2-8 early returns too —
  correct per CriticC2 recommendation 5.
- Row B `ls-files -mo` still credits uncommitted working-tree work under a
  drifted HEAD — that is the entering row-B semantics, unchanged.
- Sibling rule is email-suffix only (`ae !~ /@shokunin\.local$/`,
  census:2369): a forged name `Not A Lane <kengaku@shokunin.local>` passes —
  contract-literal; git idents are unauthenticated anyway. Boundary note only.
- `jj-sibling-author` retained stream: CLEAN, `progressing-weak`,
  `other_authored_commits=1` — the negative arm is real, not vacuous.

## Impacted axes

operability (F1 re-anchor defeats the anchor; F2 fallback hole; F3 suppressed
findings; F4 undiagnosed root drift; F5 audit blind path; F7 untested
regression shape producing false `LANE_SILENT`), identity (F1 duplicate
branch authority vs `lane.branch`; F5/F6 identity-audit scope), calibration
(F3/F7: errors and unexercised shapes produce silence, not measurement).
Coverage/C1 untouched.

## Strongest single counterexample

F2+F1 combined: on a lane colocated by jj with HEAD attached to a side branch
(or detached on `trunk` with no master/main), C2's entire detection surface
either re-anchors to the wrong ref or silently reverts to pre-C2 HEAD grading
— the F3 hazard the claim exists to close survives intact and unreported,
while the gate's only fallback case asserts the benign arm.

## Tooling

No installs or upgrades performed; all work used committed code, retained
receipts and read-only `git` queries.
