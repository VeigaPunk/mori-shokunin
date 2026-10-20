# CensusJj — C2 branch-anchored census probes (round 17, wave 1)

Executor: `MoriR17.CensusJj-5` (leaf; the only clone write besides this report is
`tools/mori-census.sh` inside the assigned clone).
Clone: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/CensusJj`
(base `24526ea9617cd020fee16c28fe4d4a2789dc28cb`). Lane checkout was not touched; no
VCS mutation (no `git add/commit/stash/checkout/…`, no jj write command).

Verdict: **implemented and self-tested green** — `bash tools/mori-census.sh --selftest`
= 125/125 pass, rc 0 (entering file: 113/113, rc 0). Contract C2 plus L1 amendment A1
are both satisfied as written below.

## Files changed

- `tools/mori-census.sh` only: `353 insertions(+), 26 deletions(-)` (owning clone).
- `.scratch/` in the clone: the selftest transcripts named under "Exact retained
  evidence" and nothing else. No writes outside the clone; no `/tmp` selftest
  directory survives.
- Tool installs/upgrades: **none** (no pacman/uv/npx/cargo/`~/.local/bin` change).

## Behavior (as delivered)

### Branch resolution (mirrors `scripts/hyaku/jj-lane.sh:115-126` + `:162-167`)

`valid_branch` (census:2108) and `lane_branch_probe` (census:2110):
`symbolic-ref -q HEAD` → `refs/heads/<b>` (name validated), else
`symbolic-ref -q refs/remotes/origin/HEAD` → `refs/remotes/origin/<b>`, else exactly
one of `show-ref -q --verify refs/heads/master|main` **by exit code** (`show-ref -q`
prints nothing on success — the rc0/empty-output trap named by CensusGitSites).
Every call carries the row-1/row-9 hardening: `env -u GIT_DIR -u GIT_WORK_TREE
-u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C <repo> …`.

### Row 6 — report closure (`ps_report_closed`, census:2183)

`cat-file -e <rev>:.ufo/reports/round-<N>/<lane>.md` and
`log -1 --format=%ct <rev> -- <path>`, with `<rev>` = `refs/heads/<ROOT branch>` when
the ROOT repo resolves a branch, else the literal `HEAD` (A1(4)). The signature is
`<lane> <round> <launch> <rev>`. Env hardening added to both calls (previously
`GIT_OPTIONAL_LOCKS=0` only; audit F10).

### Row 9 — authorship (`grade_lane`, census:2301-2371)

- Anchor revision: `refs/heads/<lane branch>` when resolved, else `HEAD` (A1(4)).
  `rev-parse --verify -q "$rev"` and `log --since=@<launch> --format='%ct %an <%ae>'
  "$rev" [--paths]` (rev before `--`; root-lane pathspecs unchanged).
- The **existing author format and parser are byte-identical** (A1(3)); rows A/B/C
  grading is untouched.
- A **second** log — `--since`, `--format='%ct%x09%cn <%ce>%x09%an <%ae>'`, same rev
  and same pathspecs — answers committer identity. Its `NF==3` guard makes a tab in a
  name inert rather than mis-parsed; the strict `(launch, NOW]` `%ct` window is
  applied in the same awk (no producer/consumer pipeline, F01 lesson kept).

### New findings (`probe_silence`, census:2443/2446), severity `warn` (A1(1))

- `HEAD_BRANCH_MISMATCH`: `HEAD` resolves to a 40/64-hex object and
  `merge-base --is-ancestor HEAD refs/heads/<branch>` returns **rc 1**. Detail:
  `lane= head=<12hex> branch= branch_tip=<12hex> basis=merge-base-not-ancestor`.
  Probe runs after the repo/tree readability gates, before every early return, so
  young/not-open lanes still report a drifted HEAD; it never changes a row state.
  **rc 0 = consistent, rc > 1 = probe error → no finding** (S046: "not measured" is
  not "measured false").
- `LANE_AUTHOR_MISMATCH`: a post-launch commit (same strict window and pathspecs) on
  the resolved branch whose committer is exactly `<lane>-shokunin
  <lane@shokunin.local>` **and** whose author is neither the lane identity nor an
  `@shokunin.local` email (A1(2): sibling fleet authors such as
  `kengaku-shokunin <kengaku@shokunin.local>` are legitimate). Detail:
  `lane= count=N committer=<lane identity> window=launch..NOW
  basis=committer-lane-author-foreign-email`.
- A1(4)/(5): when no branch resolves, neither probe runs (no finding) and the census
  keeps the entering HEAD anchor; **no `GL_EXTRA`/`SURFACE` text changed in any mode**
  — the diff itself is the proof: no production `SURFACE …` line is added or removed.

### Selftest harness (owning clone, not live behavior)

- Stub-git dispatcher (census:2999-3040) extended arg-aware:
  `rev-parse` (HEAD) vs `rev-parse-branch` (`refs/heads/*`), `symbolic-ref` vs
  `symbolic-ref-origin` (`refs/remotes/origin/HEAD`), `show-ref-<branch>` per
  `refs/heads/<name>`, `merge-base`, `log-committer` (format contains `%cn`),
  retaining `log1`/`log`/`cat-file`/`ls-files`; absent slot still = empty output rc 0.
- `fx_quiet` defaults the fixture lane to an attached `master`
  (`stub/git-symbolic-ref` = `refs/heads/master`), so all 113 entering cases exercise
  branch mode with identical stub answers.
- `MORI_SELFTEST_WORK` now uses `"${TMPDIR:-/tmp}/mori-census-selftest.XXXXXX"`
  (census:2917) and the two doc lines were updated — this lets the mandated
  `TMPDIR=<clone>/.scratch` run obey the wave's no-`/tmp` rule; default behavior is
  unchanged when `TMPDIR` is unset.

### New selftest cases (census:3937-4081; 7 checks + 5 absence assertions = 12 new)

| case | fixture evidence | asserted |
|---|---|---|
| HEAD ahead of branch | `merge-base.rc=1`, head `111…`, tip `222…` | `FINDING HEAD_BRANCH_MISMATCH severity=warn … head=111111111111 … branch_tip=222222222222`, lane still `progressing`/row-A, exit 1 DRIFT |
| author != lane, lane committer | author pass `Joao Pedro <jp@example.invalid>`; committer pass `kagi-shokunin <kagi@…>` + foreign author | `FINDING LANE_AUTHOR_MISMATCH severity=warn … count=1 …`, row-C `progressing-weak`, exit 1 |
| sibling-lane author | committer `kagi-shokunin`, author `kengaku-shokunin <kengaku@shokunin.local>` | no finding, `progressing-weak`, CLEAN drift=0 (A1(2) falsifier) |
| detached HEAD at branch tip | `symbolic-ref` rc1/empty, `show-ref master` rc0, `main` rc1, HEAD sha == tip sha, merge-base rc0 | no C2 finding, `progressing`, same verdict as attached |
| plain attached lane | default `refs/heads/master`, same shas/log as detached | no C2 finding, `progressing`, same verdict |
| merge-base probe error | `merge-base.rc=2` | no `HEAD_BRANCH_MISMATCH`, CLEAN drift=0, surface text unchanged |
| no resolvable branch | all four resolution stubs rc1 | falls back to HEAD, `progressing`/row-A, no C2 finding, CLEAN drift=0 |

## Exact retained evidence

Commands (run only inside the owning clone; `cd` = clone root):

```
$ TMPDIR="$PWD/.scratch" bash tools/mori-census.sh --selftest   # entering file, before edits
rc=0; PASS=113 FAIL=0; wall 12.65 s
MORI_CENSUS_SELFTEST: PASS (113 cases, 113 passed, 0 failed)

$ TMPDIR="$PWD/.scratch" bash tools/mori-census.sh --selftest   # delivered file (A1 final)
rc=0; PASS=125 FAIL=0; wall 13.95 s
MORI_CENSUS_SELFTEST: PASS (125 cases, 125 passed, 0 failed)
```

- Baseline transcript: `.scratch/selftest-before.txt` (113 PASS / 0 FAIL, rc 0).
- Delivered transcript: `.scratch/selftest-a1-final.txt` (125 PASS / 0 FAIL, rc 0).
- Intermediate A1 run: `.scratch/selftest-a1.txt` (125/125, rc 0) after the amendment.
- TMPDIR proof run (mktemp fix in place): `rc=0 before_tmp_dirs=0 after_tmp_dirs=0`,
  `122/122` at that point (pre-A1 case set); no `mori-census-selftest.*` remained under
  either `.scratch/` or `/tmp`.
- `bash -n tools/mori-census.sh` → rc 0 after every edit round.
- Diff: `git diff --stat` = `tools/mori-census.sh | 379 +++…, 1 file changed,
  353 insertions(+), 26 deletions(-)`.

### Unified diff summary (hunk line ranges, delivered vs `24526ea`)

```
@@ -34    +34,7    header: silence rows 6/9 branch-anchored, finding vocabulary, A1 fallback
@@ -199   +205     selftest temp-dir doc honors TMPDIR
@@ -394   +400     usage: --selftest path honors TMPDIR
@@ -2092,7 +2098,87  valid_branch, lane_branch_probe, head_branch_probe (new helpers)
@@ -2100  +2186,2   ps_report_closed: cat-file -e <rev>:<path>        (refs/heads/<branch> | HEAD)
@@ -2102  +2189,2   ps_report_closed: log -1 --format=%ct <rev> -- <path>
@@ -2116  +2205      grade_lane: new GL_* state (branch, HBM, shorts, AMN)
@@ -2141  +2231,8    grade_lane: resolve branch + HEAD invariant after row-1/tree gates
@@ -2176  +2274,3    grade_lane: rows 6/9 comment (branch vs HEAD, A1)
@@ -2188  +2288,10   row 6: ROOT revision (refs/heads/<branch> | HEAD) + call
@@ -2194  +2304,6    row 9: anchor rev (branch | HEAD), original author format
@@ -2197  +2312      row 9: rev-parse --verify -q "$rev"
@@ -2199  +2315,2    row 9: comment on entering format
@@ -2201,3 +2318,5  row 9: lg_paths separated; log args rev before `--`
@@ -2205  +2324      row 9: log with "$rev" + guarded paths
@@ -2207  +2326      row 9: same
@@ -2236  +2356,18   row 9: second committer log + LANE_AUTHOR_MISMATCH count
@@ -2271  +2409,2    row-D: has_head token comment (output unchanged)
@@ -2298  +2438,10   probe_silence: emit the two warn findings; surface line untouched
@@ -2768  +2917      selftest mktemp honors ${TMPDIR:-/tmp}
@@ -2850  +2999,23   stub git: rev-parse-branch / symbolic-ref[-origin] / show-ref-<b> / merge-base
@@ -2854  +3025,5    stub git log: log1 vs log-committer (%cn) vs log
@@ -2928  +3103,8    fx_quiet: attached-master default + slot list
@@ -3745  +3926,3    row-6 case comment: branch wording
@@ -3754  +3937,145  seven C2 selftest cases + five absence assertions
```

## Risks and boundaries

1. **Surface `cmd=` text was deliberately left stale.** `probe_silence`'s `cmd=` string
   still advertises the entering probes (`… cat-file -e HEAD:…`), even though branch mode
   runs `symbolic-ref`/`merge-base`/branch-rev probes. A1(5) requires SURFACE text to stay
   byte-identical, so the CensusGitSites recommendation to update it was declined. A future
   round that may change surface text should update this string together with its pin.
2. **Probe errors are silent.** `merge-base` rc>1 (and a non-hash HEAD/tip) emit nothing;
   A1(5) forbids adding a row token, and no new finding id is authorised. This is the
   strongest reading of S046 as amended ("record unavailable/reason" loses to "output
   identical"). L1 may want a follow-up finding id if silent probe failure is unacceptable.
3. **Fallback semantics (A1(4)) mean a repo with no resolvable branch is graded from HEAD
   exactly as before**, including its jj hazard; the branch fix cannot apply there. This is
   intentional and is what keeps r13/r14/r15 and the r10 pin byte-identical.
4. **Ambiguous fallback**: a repo that genuinely has both `refs/heads/master` and
   `refs/heads/main` resolves no branch → HEAD fallback. Mirrors `jj-lane.sh` (unique-only).
5. **Costs**: two branch-resolution probes (+ up to 2 `show-ref`) per readable lane, plus
   one extra `log` per graded lane when a branch resolves. Selftest wall time 12.65 s →
   13.95 s; no live-run measurement attempted (live census not in my command list).
6. **External gates not run (seat discipline).** Expected [INFERENCE], not measured:
   `tools/mori-silence-cases.sh` uses real attached `main` repos, asserts lane state and
   `LANE_SILENT` presence only, and its `author=sibling/committer=subject` case
   (`mori-silence-cases.sh:899-907`) has an `@shokunin.local` author → no new finding, so
   its `0 0` expectation holds. `mori-round14-regressions.py`'s synthetic git
   (`:794-808`) exits 2 for `symbolic-ref`/`show-ref`/`merge-base` → branch unresolved →
   HEAD fallback → journal assertions and CLEAN/DRIFT roll unchanged. Parent should run
   those gates.
7. **Reported by a peer, confirmed and fixed**: the selftest's hardcoded
   `/tmp/mori-census-selftest.XXXXXX` would have made the mandated `TMPDIR`-scoped run
   write to `/tmp`; it now honors `TMPDIR` (census:2917).
8. **Not changed / not in scope**: `mori-silence-cases.sh:152` doc comment still names
   `git cat-file -e` (behavior unaffected); `MANIFEST.json`, `.ufo/state`, fleet scripts,
   sibling lanes untouched.
