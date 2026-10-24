# CensusJj — C2 branch anchoring + diagnostics/env hardening (round 17, wave 1)

Executor: `MoriR17.CensusJj-5` (leaf). Clone (recreated):
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/CensusJj`,
base `5c1dfb8d0530c74eb0e1630c2b522b735b486274`. Scope: `tools/mori-census.sh` +
this report only. Lane checkout untouched; no VCS mutation; no jj command run.

**No tests or probes were executed in this turn** (L1 instruction). The only
execution is a static parse: `bash -n tools/mori-census.sh` → rc 0. Every selftest
arm added or changed here is **unexecuted**.

## State delivered on this base

The base commit already contains the first C2 delivery (branch-anchored rows 6/9,
`HEAD_BRANCH_MISMATCH` / `LANE_AUTHOR_MISMATCH`, warn severity, A1 output-stability
rules). This turn adds three corrections:

### 1. A2 — the lane mirror is the authority (CriticC2Final / CensusNewBranches)

`lane_branch_probe` (census:2158-2196) resolves in this order:

1. **Recorded helper mirror** — scrubbed `git config --get lane.branch`
   (`scripts/hyaku/jj-lane.sh:98-103`), accepted only when `valid_branch` accepts it
   **and** `rev-parse --verify -q refs/heads/<branch>` succeeds.
2. **`.jj`-colocated repo = mirror-only.** `[ -d "$repo/.jj" ]` with no accepted
   mirror → unresolved, with no attached/origin/unique fallback. This is the fix for
   the side-branch self-anchoring counterexample.
3. **Ordinary non-jj git** keeps attached HEAD → origin/HEAD → unique master/main,
   then the entering HEAD anchor when nothing resolves (A1; r13/r14/r15 stubs).

`grade_lane` (census:2322-2335) turns a colocated repo with no authoritative branch
into `unavailable` with `reason=ref-unresolved` (before the ledger anchor), so no
row is graded from an attached side bookmark. Row 6 resolves the **fleet-root**
mirror independently (census:2396-2409); a `.jj` root with no mirror skips closure
instead of reading HEAD, and row 9 still grades the lane mirror.

### 2. LANE_AUTHOR_MISMATCH no longer hides behind early returns

CensusNewBranches: the diagnostic lived inside row 9, so a young lane
(`age <= LANE_SILENCE_S`) or a report-closed lane returned before it ran — hidden
for 40/47 jj rounds.

- New `lane_author_probe` (census:2247-2262) runs only the **committer pass**
  (`--format='%ct%x09%cn <%ce>%x09%an <%ae>'`) over the same strict `(launch, NOW]`
  window and the same root-lane pathspecs as rows A/C.
- It is called after `ledger_anchor` in `grade_lane` (census:2339-2347), **before**
  the no-launch / unparseable / future-launch / ledger-close / round-advanced /
  young returns — the same placement class as the HEAD diagnostic.
- Row 9's exact-author scan and parser are byte-identical to the entering code; the
  old in-row committer block was removed (census diff `@@ -2356,18 +2468,0`).
- Rule unchanged (A1): committer is the lane identity, author differs, author email
  is not `@shokunin.local`. A failed scan emits nothing.

### 3. One scrubbed Git child environment (`GIT_SCRUB` + `git_cap`)

Every Git invocation now goes through one helper (census:580-593) instead of
repeating an inline `env` list at each site (all 16 call sites converted; a `GIT_BIN`
scan now finds only the helper):

```text
GIT_SCRUB = -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE
            -u GIT_TRACE -u GIT_TRACE_PACKET -u GIT_TRACE_PACK_ACCESS
            -u GIT_TRACE_PACKFILE -u GIT_TRACE_PERFORMANCE -u GIT_TRACE_SETUP
            -u GIT_TRACE_CURL -u GIT_TRACE_CURL_NO_DATA -u GIT_TRACE_REDACT
            -u GIT_TRACE2 -u GIT_TRACE2_EVENT -u GIT_TRACE2_EVENT_NESTING
            -u GIT_TRACE2_PERF -u GIT_TRACE2_PERF_BRIEF
            -u GIT_TRACE2_CONFIG_PARAMS -u GIT_TRACE2_DST_DEBUG
            -u GIT_CONFIG -u GIT_CONFIG_GLOBAL -u GIT_CONFIG_SYSTEM
            -u GIT_CONFIG_NOSYSTEM -u GIT_CONFIG_COUNT -u GIT_CONFIG_PARAMETERS
git_cap <repo> <args...>  ->  cap env $GIT_SCRUB GIT_OPTIONAL_LOCKS=0 git -C repo args
```

`GIT_CONFIG_COUNT` is the gate for the `GIT_CONFIG_KEY_n/VALUE_n` pair, so unsetting
it disables that override family. `MORI_*`, `PATH`, `HOME` and every non-GIT variable
pass through untouched — the fixture stubs depend on `MORI_GIT_BIN`/`MORI_FIXTURE`.
Tracing is neutralised for both hazards: it can no longer write outside the read-only
contract, and it cannot poison `CAP_OUT` (captured with `2>&1`) which is where every
probe answer is read.

## Selftest arms added (all unexecuted)

| fixture | setup | assertion |
|---|---|---|
| `jj-sidebranch-mirror` (4206) | `.jj`; mirror `master` with existing ref; HEAD attached `sidework`; per-ref `git-log-master` subject, base `git-log` sibling | `progressing` row-A (proves master chosen; a sidework anchor would be weak), CLEAN, no C2 finding |
| `jj-no-mirror` (4229) | `.jj`; no `lane.branch`; attached `sidework`; `master` ref exists | `unavailable … reason=ref-unresolved`, CLEAN |
| `jj-dangling-mirror` (4244) | `.jj`; mirror `ghost`; mirror-ref rev-parse rc1; HEAD `sidework` | `unavailable … reason=ref-unresolved`, CLEAN |
| `young-ambient-author` (4260) | launch `NOW-900` (age == gate → young); committer line with lane committer + foreign author in `(launch, NOW]` | `FINDING LANE_AUTHOR_MISMATCH severity=warn … count=1`, lane `young`/row-8, exit 1 DRIFT |
| `git-trace-scrub` (4273) | `GIT_TRACE`, `GIT_TRACE2_EVENT`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_COUNT` injected into the census env; stub writes a canary whenever it still sees a trace variable | lane `progressing` row-A; **no** trace canary file |

Stub support added: the dispatcher's `config` verb and optional per-revision log
slot `git-log[-committer|-1]-<branch>` (census:3122-3143), plus the trace-sink
simulation at census:3034-3036.

## Evidence

### Static (observed this turn)

```
$ bash -n tools/mori-census.sh   -> rc 0
$ grep -n 'cap env' …            -> only inside git_cap (census:592)
$ grep -n 'GIT_BIN' …            -> definition, doc, selftest binding, git_cap
```

### Live control state (read-only, observed this turn; unchanged)

```
$ ls -d /home/vgpnk/Projects/shokunin/mori-shokunin/.jj      -> .jj
$ git -C … config --get lane.branch                          -> master (rc 0)
$ git -C … rev-parse --verify -q refs/heads/master            -> 5c1dfb8d… (rc 0)
$ git -C … symbolic-ref -q HEAD                               -> empty, rc 1 (detached)
```

The live lane resolves via the mirror (`master`) and is not newly unavailable;
detached HEAD is exactly why the mirror, not HEAD, must anchor the rows.

### Historical selftest runs — prior clone, base `24526ea` (NOT re-run)

```
entering file:  PASS (113 cases, 113 passed, 0 failed)  rc 0
first C2 (A1):  PASS (125 cases, 125 passed, 0 failed)  rc 0
```

This base adds five `check` cases and one absence assertion; expected ~131 total,
**no count is claimed** for this state.

### External gates (static reasoning only, [INFERENCE])

- r13/r14 synthetic git stubs exit 2 for `config` and any trace variable is not
  consulted by them; no `.jj` exists in their fixtures → mirror absent → ordinary
  fallback → same anchors as entering. r15/r16 reuse r14's fixture/env.
- `mori-silence-cases.sh`: real attached-`main` repos without `.jj`/`lane.branch`
  → ordinary fallback; state and `LANE_SILENT` assertions unchanged.
- JjGate-5 was messaged: jj sandbox controls must set `git config lane.branch <b>`;
  a raw colocated checkout is now `unavailable reason=ref-unresolved` by design.

## Diff summary

A2 + this correction wave vs base `5c1dfb8`: `tools/mori-census.sh`,
**283 insertions(+), 73 deletions(-)**.

```
@@ -35,6  +35,13    header: A2 mirror authority + diagnostic placement + env scrub
@@ -560   +568,29   GIT_SCRUB array + git_cap helper (one scrubbed Git child env)
@@ -2102,3 +2138,15  resolver header: authority order A2
@@ -2111,3 +2159,16  lane_branch_probe: mirror -> ref check -> jj stop -> legacy chain (via git_cap)
@@ -2121,2 +2182,2   resolver calls converted to git_cap
@@ -2130,2 +2191,2   resolver calls converted to git_cap
@@ -2133,2 +2194,2   resolver calls converted to git_cap
@@ -2150,2 +2211,2   head_branch_probe calls converted to git_cap
@@ -2157,2 +2218,2   head_branch_probe calls converted to git_cap
@@ -2162,2 +2223,2   head_branch_probe calls converted to git_cap
@@ -2174   +2236,30  lane_author_probe (early committer-author diagnostic)
@@ -2186,2 +2277,2   row-6 cat-file via git_cap
@@ -2189,2 +2280,2   row-6 log -1 via git_cap
@@ -2218   +2309      row-1 git-dir via git_cap
@@ -2235,2 +2326,11  colocated-unresolved gate + branch anchor
@@ -2240   +2341,8   diagnostic call after ledger_anchor (before early returns)
@@ -2274,3 +2382,4   facts comment: non-jj fallback only
@@ -2280   +2389      ls-files via git_cap
@@ -2289,3 +2398,5   row-6 root mirror + jj no-HEAD policy
@@ -2297   +2408,2   row-6 call guarded by non-empty root_rev
@@ -2306,2 +2418,3   row-9 comment: fallback non-jj only
@@ -2312   +2425      row-9 rev-parse via git_cap
@@ -2326   +2439      row-9 author log via git_cap
@@ -2356,18 +2468,0   row-9 committer block removed (moved to lane_author_probe)
@@ -2938   +3034,5   stub git trace-sink simulation
@@ -3021   +3122      stub git: config verb
@@ -3029   +3131,13  stub git: optional per-revision log slot
@@ -3103,6 +3217,9   fx_quiet: baseline ordinary git lane + slot list
@@ -4061,3 +4178,3   relabel prior no-branch arm `git:`
@@ -4072   +4189      comment wording
@@ -4077   +4194      comment wording
@@ -4079   +4196,94  five selftest arms + trace-canary assertion
```

Cumulative C2 work vs the round-16 tip (`24526ea`): 565 insertions, 28 deletions.

## Risks / blockers

1. **Everything in this wave is unexecuted.** The resolver, the relocated
   diagnostic, the env helper and all five arms are only syntax-parsed. The owning
   gate must run `bash tools/mori-census.sh --selftest` from the clone before merge
   evidence is claimed; expect the five new assertions to be the first failures if
   any stub slot is mis-keyed.
2. **New diagnostic scope.** Lanes that are young/report-closed/round-advanced now
   emit `LANE_AUTHOR_MISMATCH` where they previously returned first. That is the
   requested widening; it also means a live lane with an ambient-author, lane-
   committed post-launch commit will flip the roll even before the silence gate.
3. **Cost.** One extra committer `log` per anchored lane; for lanes that grade
   through row 9 the total log count is unchanged (the row-9 committer pass moved,
   not duplicated) — except young/closed lanes, which now pay one scan they
   previously skipped.
4. **Live config semantics.** `GIT_CONFIG_GLOBAL/SYSTEM` are scrubbed for Git
   children, so a mirror stored only in user/system config is invisible. The helper
   writes the mirror into the lane repo config, so lane and census agree; a hostile
   or accidental global `lane.branch` can no longer disable the probes.
5. **Root row 6 on a broken jj root.** Closure is skipped (never HEAD), so a child
   lane can still grade without the report-closure cross-check; flagged to JjGate-5.
6. **No `/tmp` writes, no installs.** `MORI_SELFTEST_WORK` still honors
   `${TMPDIR:-/tmp}` (census:3012); nothing was installed or upgraded this turn and
   no scratch file was created (no test run).
