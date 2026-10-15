# Round 3 verdict — integration draft (scribe seat, goal wave)

Integration target: append as a `## Round 3 verdict — 2026-10-15 (goal wave)` section in
`SCORECARD.md` (parent-owned; append-only — the blocked-attempt section and the round-2
verdict stay untouched). Verdict vocabulary only (`improved` / `harmed` / `unchanged` /
`unprovable-but-better`); no scalar scores. Every figure below is bound to a landed
artifact at a cited path (`corpus/evidence/cutover-r3-*.log`,
`corpus/knowledge/silence-cutover-r3.md`, `corpus/evidence/README.md:110-173`);
`[PARENT: …]` marks values only the integration commit, the parent's acceptance re-run,
or another seat's ownership can bind.

- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Round-count claim: `[PARENT: verified-round accounting 2 → 3 on admission]`
- Draft status: seed v1 by the interrupted prior dispatch (16:10Z seed; 16:43Z rewrite
  left every after-side cell `[AWAITING]` — it predated the impl landing at 16:55Z).
  Rewritten again 2026-10-15T17:22Z by the scribe backfill seat from the landed
  artifacts (census r2 sha `fe22a14f…`; after-leg receipts 16:57–16:58Z).

## Round 3 verdict

Round scope (the registered round-2 debt, `SCORECARD.md:128-131`): one coverage move —
land the r2 `probe_silence` in `tools/mori-census.sh` implementing the
`corpus/knowledge/silence-grading-r2.md` contract (per-lane rows, states `silent` /
`progressing` / `progressing-weak` / `young` / `not-open` / `unavailable`, rows A–D,
closure predicate, `LANE_SILENT` only for row D, `unavailable` ≠ unhealthy, strict age
gate), harden the `:517`/`:283` pipefail crash constructs, add selftest cases, and
re-baseline the frozen oracle (`tools/mori-silence-cases.sh` sha `505a7504…`) with
per-case justification; never branching on `MORI_FIXTURE` / fixture paths.

**Before** (r1 census sha `e3073a2b…`; before-leg receipt
`corpus/evidence/cutover-r3-20261015T164140Z-before.log`, 16:41:40–16:49:31Z):

- `bash tools/mori-silence-cases.sh` → exit 1, `MORI_SILENCE_CASES: matched=10 total=27`;
  17 FAILs = 16 measured r2-contract gaps + 1 crash defect
  (`FAIL unreadable-git-unavailable: census emitted no MORI_CENSUS verdict (rc=1) —
  crashed mid-run`).
- `bash tools/mori-census.sh --selftest` → `MORI_CENSUS_SELFTEST: PASS (14 cases,
  14 passed, 0 failed)`, exit 0.
- live census: aggregate-only `SURFACE silence: drift (… silent=7 progressing=2
  progressing_weak=0 skipped=0 window_s=7200)` with 7 × `FINDING LANE_SILENT` carrying
  `head_epoch=`/`newest_epoch=`; `MORI_CENSUS: DRIFT (findings=21 drift=21 unavailable=1
  surfaces=7)`, exit 1.
- `:283` waves-age repro: exit 1, header line only, no verdict; control exit 0 CLEAN
  (before receipt §4).

**After** (r2 census sha `fe22a14f…` — `VERSION=census-r2`, `tools/mori-census.sh:61`;
after-leg receipts 16:57:12–16:58:24Z; census sha verified unchanged before/after every
capture):

- selftest `MORI_CENSUS_SELFTEST: PASS (25 cases, 25 passed, 0 failed)`, exit 0.
- oracle `MORI_SILENCE_CASES: matched=25 total=27`, exit 1 — 15 FAIL→PASS, the 10 r1
  PASSes held; the 2 remaining FAILs are the frozen matcher defect (an expansion-introduced
  `|` is literal in `case "$obs" in $want)`, `tools/mori-silence-cases.sh:362-365`; calls
  at `:455`/`:613`); counterfactual witness at identical census bytes:
  `matched=27 total=27`, exit 0.
- live `census-r2`: 9/9 roster lanes carry per-lane rows, all `progressing` (8 ×
  `basis=row-A`; aggregator `basis=row-B rowb_files=1 attribution=inference`),
  `SURFACE silence: ok (… silent=0 progressing=9 …)`, zero `LANE_SILENT`,
  `DRIFT (findings=14 drift=14 unavailable=1 surfaces=7)` (the 1 unavailable is tmux);
  reverify spot identical in exit and finding-id set.

| axis | verdict | before → after evidence |
|---|---|---|
| coverage | **improved** | Before: r1 graded a rolling commit-mtime window — no launch line, closure or authorship; oracle `matched=10 total=27` (16 r2-contract gaps); live emitted an aggregate-only silence row + 7 × `LANE_SILENT` on commit-sparse/wrapped/sibling-credited lanes. After: every spec element implemented per the 26-row spec-row map (`silence-cutover-r3.md` §1 `:25-57`, every row `implemented` or `verified`), producing per-lane `SURFACE lane.<id>:` rows with the six states; oracle `matched=25 total=27` — 15 FAIL→PASS, the 10 r1 PASSes held, per-case justification for all 27 (`silence-cutover-r3.md` §5 `:152-180`; receipt `…-oracle.log:14-42`); the 2 remaining FAILs are the frozen matcher defect, and the counterfactual proves all 27 satisfy their intended want-sets (`…-oracle-counterfactual.log:43-58`). The registered literal `N = M` is arithmetically unattainable under the frozen oracle (max 25/27) — reported as-is, not weakened. Live: 9/9 lanes per-lane rows, zero false `LANE_SILENT`. |
| operability | **improved** | Before: selftest 14/14 exit 0, but an unreadable lane repo aborted the census (`rc=1`, no verdict; oracle case 9) and the `:283` waves pipeline had the same crash signature (before receipt §4: repro rc 1 header-only vs control rc 0 CLEAN). After: selftest `PASS (25 cases, 25 passed, 0 failed)` exit 0; `unreadable-git-unavailable` grades `unavailable` with a verdict (rc 0); the r1 `:517` construct is deleted (readability gated first, `ps_walk` `:633-641` → `unavailable` `:686-691`) and `:283` is rc-gated (`cap find` `:296-302`, `age_unreadable=` `:320`) with selftest case `waves: unreadable wave age -> no crash, no false finding`; live census runs to a full verdict. Residual (named): `:227` `state_n` is the same bare-pipeline shape, measured still crashing at `fe22a14f` (`silence-cutover-r3.md` §3 `:106-114`) — out of the registered `:517`/`:283` scope, next-round follow-up. |
| depth | **improved** | Before: the decision table + surfaces notes existed as candidates; no implementation anchor, and the r1 divergences stood (measured kasegi-wrapped / aggregator sibling-credit, `LOG.md:73-80`). After: `corpus/knowledge/silence-cutover-r3.md` maps every spec element to file:line (§1), names seven deltas D-a–D-g with reasons (§2 `:59-91`), documents the hardening and its canaries (§3), the 14→25 selftest change (§4 `:119-140`), and the 27-case oracle re-baseline (§5); the crash class is pinned as a lesson with canaries A/B/C and the rc-1/DRIFT collision mechanism (`corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md:12-63`). Rows A–D, closure predicate and identity policy each carry implementation anchors (`tools/mori-census.sh:747-809`; `:648-661`). |
| freshness | **improved narrowly** | Before: three watch receipts bound to the old sha `e3073a2b…`; none at r2. After: five dated, hash-pinned receipts (`cutover-r3-20261015T164140Z-before.log`; `…T165712Z-{selftest,oracle,live,oracle-counterfactual}.log`) with census sha pinned before/after each capture, indexed with re-run recipes in `corpus/evidence/README.md:110-173`; the live receipt carries a reverify spot with identical finding-id set and states its method limitation. Drift pin still absent — carried debt, not part of this move (`silence-cutover-r3.md` §7 `:253-254`). |
| calibration | **improved** | Before: r1 violated the contract's calibration rules — `LANE_SILENT` fired 7× (incl. wrapped kasegi), a crash surfaced as rc 1 with no verdict, no age/closure/attribution discipline. After: strict age gate proven (oracle case `young-age-equals-gate` age==gate → `young`; selftest `silence: strict age gate (age == gate) -> young`); `LANE_SILENT` fires only on the six row-D cases (finding=1 rc=1) and no other case emits a finding (finding=0 rc=0); `unavailable`/`not-open`/`young` never DRIFT (cases 7/8/9; live tmux `unavailable` stays out of DRIFT); no fixture branching in the silence path — zero `MORI_FIXTURE` references in `:503-845` (grep at `fe22a14f`; the only non-selftest-harness branch in the file is the pre-existing r1 journal JSON arm `:358-362`). Honest accounting: 25/27 reported as-is, the harness defect proven by a bash-semantics probe, not asserted (`…-oracle-counterfactual.log:18-24`). No threshold tuning claimed. |
| adjacency | **unchanged** | Scope-sentinel: detection/report only — zero remediation/kill/pkill/systemctl/host-config content in any r3 artifact; fixtures under `/tmp`; frozen oracle untouched (`505a7504…` before/after every run); out-of-province observations (the other surfaces' 14 findings; the `:227` crash instance) are reported, not absorbed. `[PARENT: confirm from the integration diff]` |

Admission: five axes improved (coverage, operability, depth, freshness, calibration),
adjacency unchanged, **none harmed → ADMIT**. No scalar score. The registered literal
`N = M` oracle tally is unmet under the frozen matcher and is reported honestly with a
per-case justification and a 27/27 counterfactual witness; the substantive authorship
half of precondition 6 (cases 12–18) passes end-to-end.

Learning trends (lane idiom):

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **improved** | New: `corpus/knowledge/silence-cutover-r3.md`; `corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md`; the `SKILL.md:111-153` silence section rewritten as the r2 contract with the cutover receipt pointer; `corpus/evidence/README.md:110-173` r3 receipt index; `corpus/README.md` coverage map + known gaps updated (silence cutover, frozen-oracle tally residual, `:227`, row-6 residual). |
| quality | **improved** | Honest tally by construction (25/27 as-is; 15 FAIL→PASS enumerated); the 2 FAILs diagnosed to a one-block matcher defect with a semantics probe + patch + counterfactual run; per-case justification for all 27; `:227` residual disclosed rather than hidden; every claim carries path:line or receipt. |
| discernment | **unchanged** | No outside spot-check of an admit/reject exists — the wave's seats are the lane per protocol; the counterfactual witness is a same-wave scratch experiment, not outside verification. |

`[PARENT: bind the integration commit and the round-count claim; re-run
`bash tools/mori-census.sh --selftest` and `bash tools/mori-silence-cases.sh` (and the live
census) at admission, and replace/confirm the acceptance figures above before appending
this section]`