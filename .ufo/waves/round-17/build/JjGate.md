# JjGate — C2 jj-colocation regression gate (round 17, wave 1, build)

Seat: `MoriR17.JjGate-5` (executor, leaf). Date 2026-10-20. Advises only; L1
`MoriR17` is the sole judge/integrator.

Deliverable (the only implementation file I wrote):

```
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/JjGate/tools/mori-round17-jj-regressions.py
sha256 1067e4ae97ba8a60c55f1cc65bfaf042a6c6384ae1064a644919cdfd409ee0e3
1319 lines / 52989 bytes / mode 0755
```

No other implementation file, harness, MANIFEST, `.ufo/state`, fleet script or
sibling lane was written. This report is the only retained write outside that
clone (the one accidental `/tmp` file is disclosed and removed below).
No VCS write happened in the lane, the fleet root, or the clone's own repo; all
git/jj writes were fixture commits inside throw-away sandbox repos the gate
creates under `--scratch` (my `.scratch`), exactly as contract C2 prescribes.
Scratch is untracked in the clone; no `git add`, `commit`, `stash`, `checkout`,
`switch`, `reset`, `pull` or `push` was run against it.

## Verdict (measured)

| run | census sha256 | cases | match | mismatch | assertions | failed | rc |
|---|---|---|---|---|---|---|---|
| entering census (`git show 24526ea:tools/mori-census.sh`) | `f1f8d1b62bb617bbcc4664057ab807d3fed8c275b7aabbdf7b373323c5501ff7` | 12 | 7 | 5 | 124 | **21** | **1** |
| scratch reference carrying C2 + the A1 amendment | `33e2120a4c39b8d50c3bc55f359e91e4a1ba0def95e3d6458892a7b4535bc56c` | 12 | **12** | 0 | 134 | **0** | **0** |
| `--selftest` (dormant fixture census + HEAD mutant + missing census) | n/a | n/a | n/a | n/a | n/a | 0 | **0** |

The reference is **validation scaffolding only**, saved under
`.scratch/mori-census-c2.sh` (not a deliverable, not installed): it exists so a
green run is possible to measure and so the gate is proven able to pass. The
census edit itself belongs to its own seat. The gate records both digests in
`run-manifest.json` (`gate.sha256`, `census.sha256`).

## Interface (implemented)

```
mori-round17-jj-regressions.py --census PATH --output DIR [--scratch DIR]
mori-round17-jj-regressions.py --selftest [--scratch DIR]
```

- `--scratch` default: `<output>/scratch`; with `--selftest` it is the temp
  parent (`tempfile.mkdtemp(dir=scratch)`). No `/tmp` is used by a run that
  passes `--scratch`.
- Writes `DIR/run-manifest.json` (schema `mori-round17-jj-regressions-v1`) and
  `DIR/cases/<id>.out` = the exact combined census stream for that case.
- Manifest: `gate{path,sha256}`, `census{path,present,sha256}`, `tools{git,jj,
  bash,jq,timeout}` with versions, `scratch_run`, `environment`, per-case
  `status` (`match|mismatch|capability_absent|setup_failed`), `assertions[]`
  (`id, ok, detail`), `failed_assertions`, `observed{state,basis,roll,rc,
  findings,verdict_fields,refs}`, and `totals` + top-level `failed`
  (failed-assertion count) and `failed_cases`.
- Exit 0 only when every assertion holds; 1 on any failed assertion or
  capability gap (a missing census marks all cases `capability_absent` and exits
  1, mirroring the C1 gate); 2 on gate setup/usage error.

## Sandbox design

One fleet root per case under `--scratch`:

```
<case>/root/shokunin.conf              LANES="\nalpha|alpha-shokunin|axis\n"
<case>/root/.ufo/state/alpha.round     1 (equal to the ledger anchor)
<case>/root/.ufo/watchdog.log          one launch line, age 8000 s > 7200 gate
<case>/root/.ufo/reports/round-1/      report path root for closure cases
<case>/root/alpha-shokunin/            real child lane repo (git or jj-colocated)
<case>/root/                           real git repo (row-6 closure is root-relative)
<case>/home/                           HOME, XDG_CONFIG_HOME, JJ_CONFIG, GIT_CONFIG_GLOBAL
<case>/stub/                           pgrep, df, journalctl, tmux, jq-fail
<case>/fix/                            cgroup files, meminfo, diskstats, uptime, boot_id
```

`MORI_NOW_EPOCH` is pinned at run start +120 s, so every fixture commit
(real clock) falls inside the `(launch, NOW]` window and the 8000 s age stays
over the census's 7200 s silence gate.

Guard compliance (L1 interjection, SentinelJjSandbox) is enforced in code:

- every non-init jj call is `jj -R <sandbox> ...` **after** asserting
  `<sandbox>/.jj` is a directory (`tools/...:249-255`);
- `jj git init --colocate <absolute sandbox path>` is the only exception, run
  from `<case>` (outside every repo) (`:268-274`);
- every git call is `git -C <sandbox dir> ...` (repo commands use the repo, the
  init uses the case directory as the `-C` target), with
  `GIT_CEILING_DIRECTORIES` set to the case sandbox and
  `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE` absent (`git` helper `:206-207`,
  init `:210-215`, env `:187`, `:396`);
- `HOME`, `XDG_CONFIG_HOME`, `JJ_CONFIG`, `GIT_CONFIG_GLOBAL`,
  `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` point into
  `<case>/home` for both the fixturing tools and the census. Observed positive
  evidence: `<case>/home/.config/jj/` is created by `jj git init --colocate` in
  every jj case (assertion `jj_config_redirected`), and reference runs passed
  it for all jj cases.
- no remote is configured in any sandbox; `refs/remotes/origin/HEAD` is absent.

## Hermetic census run

The census is executed as `bash <census>` with its own override environment
(census header, `tools/mori-census.sh:202-241`), all pinned to sandbox files or
stubs: `MORI_SHOKUNIN_ROOT`, `MORI_UFO_DIR`, `MORI_WATCHDOG_LOG`,
`MORI_TIMELINE_FILE`, `MORI_STATE_DIR`, `MORI_WAVES_DIR`, `MORI_FLEET_CONF`,
`MORI_ROSTER_LANES=`, `MORI_CGROUP_{EVENTS,CURRENT,PRESSURE,MAX,PEAK,
LOCAL_EVENTS,SERVICE_EVENTS}`, `MORI_DISKSTATS`, `MORI_UPTIME`, `MORI_MEMINFO`,
`MORI_BOOT_ID_FILE`, `MORI_DF_BIN`, `MORI_PGREP_BIN`, `MORI_JOURNALCTL_BIN`,
`MORI_JQ_BIN`, `MORI_TMUX_BIN`, `MORI_TIMEOUT_BIN`, `MORI_GIT_BIN`,
`MORI_DISK_TARGETS`, `MORI_TMUX_SCOPE_ROOT`, `MORI_NOW_EPOCH`.

Observed in every case output (e.g.
`.scratch/out-final-c2/cases/jj-helper-commit.out`): journal rows name
`<case>/stub/journalctl`; the tmux rows name `<case>/stub/tmux`; the disk row
names `<case>/stub/df`; the watchdog row names `<case>/stub/pgrep`; the cgroup
row names `<case>/fix/cgroup/memory.events` and prints
`current=refused:outside-sysfs-cgroup` (the census refuses to read a
`MORI_CGROUP_CURRENT` outside `/sys/fs/cgroup`, so no live cgroup read is even
attempted). No surface lacked an override, so the "stop and report" branch was
not needed. `MORI_JQ_BIN` is the real `jq` (present at `/usr/bin/jq`); if it is
absent the census itself degrades the journal rows to `unavailable` before any
query.

Read-only proof: each case snapshots lane/root `HEAD` and `refs/heads/master`
before and after the census and asserts equality (`refs_unchanged`). It passed
in every case of every run.

## Cases (12) and measured behaviour

`E` = entering census observed; `R` = reference observed.

| # | case | fixture | expected delivered | E | R |
|---|---|---|---|---|---|
| 1 | `git-plain-progress` | plain git, lane-authored commit on branch | progressing row-A, no findings, CLEAN 0 | pass | pass |
| 2 | `git-detached-at-tip` | detached exactly at branch tip | progressing row-A, no mismatch | pass | pass |
| 3 | `git-detached-commit` | plain git commit on detached HEAD (ahead) | silent row-D + `HEAD_BRANCH_MISMATCH`, DRIFT 1 | **fail 5** (progressing row-A, no finding) | pass |
| 4 | `git-detached-behind` | lane commit on branch, then detach at `HEAD~1` | progressing row-A from the branch, no mismatch | **fail 4** (silent row-D) | pass |
| 5 | `git-report-on-branch` | report committed on root branch | not-open row-6 | pass | pass |
| 6 | `git-report-off-branch` | report committed only on detached root HEAD | silent row-D (**not** row-6) | **fail 4** (not-open row-6) | pass |
| 7 | `git-foreign-author` | ambient author+committer on branch | progressing-weak row-C, **no** author finding | pass | pass |
| 8 | `jj-helper-commit` | jj colocated; `metaedit --update-author` + `commit` + `bookmark set` | progressing row-A, no findings | pass | pass |
| 9 | `jj-commit-no-bookmark` | jj `commit` only (HEAD ahead, branch lags) | silent row-D + `HEAD_BRANCH_MISMATCH`, DRIFT 1 | **fail 5** (progressing-weak row-C, no finding) | pass |
| 10 | `jj-ambient-author` | ambient author in `@`, lane committer, bookmark moved | progressing-weak row-C + `LANE_AUTHOR_MISMATCH`, DRIFT 1 | **fail 3** (no author finding; CLEAN) | pass |
| 11 | `jj-sibling-author` | `kengaku-shokunin <kengaku@shokunin.local>` author, alpha committer, bookmark moved | progressing-weak row-C, **no** author finding (A1 negative control) | pass | pass |
| 12 | `git-fallback-head` | branch `trunk`, detached at tip, no master/main/origin HEAD | progressing row-A via unchanged HEAD fallback | pass | pass |

Both findings are asserted `severity=warn` exactly (not merely warn|crit), per
the L1 amendment. `HEAD_BRANCH_MISMATCH` detail is asserted to contain
`lane=alpha` and the short HEAD and short branch-tip hashes; `LANE_AUTHOR_MISMATCH`
detail is asserted to contain `lane=alpha`. Field names other than `lane=` are
not over-specified.

Entering failures in detail (21 failed assertions over 5 cases; cases 1,2,5,7,8,
11,12 match):

- `git-detached-commit`: `census_exit`, `verdict_roll`, `lane_state`,
  `lane_basis`, `finding:HEAD_BRANCH_MISMATCH:present`.
- `git-detached-behind`: `census_exit`, `verdict_roll`, `lane_state`,
  `lane_basis`.
- `git-report-off-branch`: `census_exit`, `verdict_roll`, `lane_state`,
  `lane_basis`.
- `jj-commit-no-bookmark`: same five as `git-detached-commit`.
- `jj-ambient-author`: `census_exit`, `verdict_roll`,
  `finding:LANE_AUTHOR_MISMATCH:present`.

Exact entering lines (from `out-final-entering/cases/`):

```
jj-commit-no-bookmark: SURFACE lane.alpha: progressing-weak (... basis=row-C other_authored_commits=1; ...)
                       MORI_CENSUS: CLEAN (findings=2 drift=0 unavailable=0 surfaces=8)
git-report-off-branch: SURFACE lane.alpha: not-open (... basis=row-6 reason=committed-report round=1 ...)
git-detached-behind:   SURFACE lane.alpha: silent (... basis=row-D ...)
```

Exact reference lines (`out-final-c2/cases/`):

```
jj-commit-no-bookmark: SURFACE lane.alpha: silent (... basis=row-D ...)
  FINDING HEAD_BRANCH_MISMATCH severity=warn obs=lane=alpha head=8edc03e branch=master branch_tip=820d1fd rule=merge-base-is-ancestor
  MORI_CENSUS: DRIFT (findings=4 drift=2 unavailable=0 surfaces=8)
jj-ambient-author:     SURFACE lane.alpha: progressing-weak (... basis=row-C ...)
  FINDING LANE_AUTHOR_MISMATCH severity=warn obs=lane=alpha commits=1 rule=committer-lane-author-email-foreign
  MORI_CENSUS: DRIFT (findings=3 drift=1 unavailable=0 surfaces=8)
jj-sibling-author:     SURFACE lane.alpha: progressing-weak (... basis=row-C ...)
  MORI_CENSUS: CLEAN (findings=2 drift=0 unavailable=0 surfaces=8)      # no author finding
git-fallback-head:     SURFACE lane.alpha: progressing (... basis=row-A ...)
  MORI_CENSUS: CLEAN (findings=2 drift=0 unavailable=0 surfaces=8)
```

## Mutation checks on the gate itself

Three red controls prove the assertions are not tautological:

| mutant (scratch only) | gate rc | failed assertions / cases | named failure |
|---|---|---|---|
| reference with the pre-amendment author rule (`author != committer`) | 1 | 3 / 1 | `jj-sibling-author`: `finding:LANE_AUTHOR_MISMATCH:absent`, `verdict_roll`, `census_exit` |
| reference emitting both findings as `severity=info` | 1 | 5 / 3 | `finding:HEAD_BRANCH_MISMATCH:severity` (cases 3,9), `finding:LANE_AUTHOR_MISMATCH:severity` + roll/rc (case 10) |
| missing census path | 1 | 12 / 12 (`capability_absent` each) | `census_present` |

`--selftest` (green, 13 checks) additionally asserts: fixture rc0 / 12 cases /
0 failed; stable ids `finding:HEAD_BRANCH_MISMATCH:present` and
`finding:LANE_AUTHOR_MISMATCH:present` pass under the compliant fixture;
`finding:LANE_AUTHOR_MISMATCH:absent` passes for the sibling control;
`git-fallback-head` passes; the HEAD-only mutant exits 1 and names
`finding:HEAD_BRANCH_MISMATCH:present` as failed; the missing census exits 1
with all cases `capability_absent`. Its fixture census is dormant source in the
gate (never installed) and its temp tree is created under `--scratch` when
given.

## Commands and exit codes (retained)

All run from
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/JjGate`.

```
$ git show 24526ea:tools/mori-census.sh > .scratch/mori-census-entering.sh      rc 0   (4189 lines)
$ python3 tools/mori-round17-jj-regressions.py \
    --census .scratch/mori-census-entering.sh \
    --output .scratch/out-final-entering --scratch .scratch/jj-final-entering   rc 1
  cases=12 match=7 mismatch=5 capability_absent=0 setup_failed=0 assertions=124 failed=21
$ python3 tools/mori-round17-jj-regressions.py \
    --census .scratch/mori-census-c2.sh \
    --output .scratch/out-final-c2 --scratch .scratch/jj-final-c2               rc 0
  cases=12 match=12 mismatch=0 capability_absent=0 setup_failed=0 assertions=134 failed=0
$ python3 tools/mori-round17-jj-regressions.py --selftest --scratch .scratch/selftest-root   rc 0
  SELFTEST ok: ok_rc0,ok_cases,ok_failed_zero,ok_mismatch_finding,ok_mismatch_severity,
  ok_author_finding,ok_sibling_negative,ok_fallback_head,head_rc1,
  head_names_missing_mismatch,head_failed_assertions,absent_rc1,absent_capability_absent
$ python3 tools/mori-round17-jj-regressions.py --census .scratch/mori-census-oldauthor.sh \
    --output .scratch/out-oldauthor --scratch .scratch/jj-gate-oldauthor         rc 1  (3 failed / 1 case)
$ python3 tools/mori-round17-jj-regressions.py --census .scratch/mori-census-info.sh \
    --output .scratch/out-info --scratch .scratch/jj-gate-info                   rc 1  (5 failed / 3 cases)
$ python3 tools/mori-round17-jj-regressions.py --census .scratch/mori-census-c2.sh \
    --output .scratch/out-default2                                              rc 0  (default scratch: <output>/scratch)
$ python3 tools/mori-round17-jj-regressions.py --census .scratch/no-such-census.sh \
    --output .scratch/out-missing2                                              rc 1  (12 capability_absent)
```

Manifests (evidence): `.scratch/out-final-entering/run-manifest.json`,
`.scratch/out-final-c2/run-manifest.json`, `.scratch/out-oldauthor/`,
`.scratch/out-info/`, `.scratch/out-default2/`, `.scratch/out-missing2/`;
per-case streams under each `cases/<id>.out`. The two mutant runs' sandbox
trees were deleted after measurement; their manifests and case streams were
retained.

## Reference scaffold (validation only, not delivered)

`.scratch/mori-census-c2.sh` is the entering census plus the C2 changes needed
to make a green run measurable:

1. `detect_branch()` with the `jj-lane.sh:115-126` order
   (`symbolic-ref HEAD` -> `refs/remotes/origin/HEAD` -> unique
   `master`/`main`);
2. row 6 closure queries `refs/heads/<branch>` for `cat-file -e` and
   `log -1`, with HEAD as the fallback when the resolver has no input;
3. row 9 `rev-parse` and `log --since` are branch-anchored (HEAD fallback);
4. `HEAD_BRANCH_MISMATCH` when `merge-base --is-ancestor HEAD
   refs/heads/<branch>` fails (branch resolvable only);
5. `LANE_AUTHOR_MISMATCH` (warn) for a post-launch branch commit whose
   committer is the lane identity and whose author email does **not** end in
   `@shokunin.local` (A1 amendment; sibling lanes are quiet);
6. both findings are `warn`.

The gate does not depend on this file; it is hashed and named only so the green
run can be reproduced.

## Risks, limits, blockers

- **Root-vs-lane scope of `HEAD_BRANCH_MISMATCH`.** The gate assumes the
  mismatch check is evaluated in the lane's own repo (contract: "detail names
  lane"). `git-report-off-branch` therefore forbids `HEAD_BRANCH_MISMATCH` while
  the *root* HEAD is detached ahead of the root branch, because the lane repo is
  clean. An implementation that evaluates the mismatch against `$ROOT` for every
  lane (instead of `$repo`) would fail case 6. Flagged for L1; I did not encode
  the alternative because it would make the finding fire for child lanes on
  unrelated main-repo churn.
- **Detail field names are free.** Only `lane=<id>` and the short hashes are
  asserted for `HEAD_BRANCH_MISMATCH`; a rename of `head=`/`branch_tip=` is
  tolerated as long as the short hashes appear.
- **Fallback case can pass for the wrong reason.** `git-fallback-head` asserts
  the surface (progressing row-A), not that the resolver specifically failed;
  the fixture guarantees no master/main/origin HEAD, so the resolver has no
  input.
- **A1 churn.** If the author rule changes again, cases 10 and 11 (`jj-ambient
  author`, `jj-sibling-author`) must move with it; they are the two arms of the
  amendment.
- **jj version.** Behaviour is measured with `jj 0.45.1-7c41cdeb...`; a jj
  upgrade that changes where colocated git HEAD lands after `commit`/`bookmark
  set` would change the fixtures (and the C2 premise), not just the gate.
- **Sandbox placement.** `--scratch` may be under the lane tree (my clone's
  `.scratch` is). The `-R`/`GIT_CEILING_DIRECTORIES` guard is what keeps that
  safe; the gate never relies on cwd discovery.
- No blockers: all 12 cases and the selftest are executable and green against a
  contract-compliant census.

## Guard disclosure (SentinelJjSandbox interjection)

Before the L1 guard arrived I ran jj in sandbox repos under this clone's
`.scratch` **without `-R`**, and ran `jj git init --colocate` without an
explicit path. Exact commands (all cwd inside my own `.scratch` experiment
repos, all removed afterwards):

- `jj git init --colocate` (cwd `.scratch/exp/repo`), then in that repo:
  `jj bookmark list`, `jj log --no-graph -r '@ | @-'`,
  `jj --config user.name/user.email ... file track`, `jj --config ...
  metaedit --update-author`, `jj --config ... commit -m ...`,
  `jj --ignore-working-copy log --no-graph -r '@-' -T commit_id`,
  `jj --ignore-working-copy bookmark set master -r <hash>`;
- `jj git init --colocate` (cwd `.scratch/exp2/lane`), then
  `jj --ignore-working-copy log`, `jj --config ... commit`,
  `jj --ignore-working-copy log`, `jj --ignore-working-copy bookmark set`;
- `jj git init --colocate` (cwd `.scratch/exp3/lane`), then
  `jj --ignore-working-copy log -r @`, `jj --config ... commit`;
- two gate runs (`out-entering`, the first `out-c2`) whose then-current code
  also ran `jj git init --colocate` with cwd = sandbox lane and no `-R` on the
  follow-up calls.

The lane's `.jj` (`/home/vgpnk/Projects/shokunin/mori-shokunin/.jj`) exists; I
did not read it, and no jj command was ever given the lane as target. After
`jj git init --colocate` each sandbox had its own `.jj` (observed with `ls -d`),
so the nearest-workspace discovery would have selected the sandbox — but I did
not observe what those pre-guard calls read, so this is **[INFERENCE]**, not a
claim. All post-guard gate runs use `-R <sandbox>` after asserting `.jj`, and
`jj git init --colocate <absolute sandbox path>` from `<case>`.

Also disclosed: one mistaken shell redirection wrote a 237-byte file at
`/tmp/does-not-exist` (it captured one gate summary line). I removed it
immediately (`rm -f`, path confirmed absent). No probe outputs, downloads or
scratch were written to `/tmp`; the only `/tmp` artifact was that accidental
file, and every gate/selftest run used `--scratch` under the clone.

## Tools and installs

No install or upgrade. Versions observed:
`jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`
(`/home/vgpnk/.local/bin/jj`), `git version 2.56.0`, `Python 3.14.8`, real
`jq` (`/usr/bin/jq`) and `/usr/bin/timeout` used as census dependencies.

## Axes (godspeed)

1. **Contract fidelity** — one assertion per contract sentence (branch anchor,
   two findings, warn severity, A1 sibling arm, HEAD fallback), written as
   stable ids in the manifest.
2. **Hermeticity** — every census host surface pinned to a sandbox stub/file;
   the census output itself names those paths and `refused:outside-sysfs-cgroup`.
3. **Fixture realism** — real git and real jj colocation, helper-shaped command
   order, real branch/bookmark semantics; no stub git.
4. **Red-ness** — the entering census, a pre-amendment author rule, an
   info-severity mutant and a missing census all turn the gate red and name the
   failing assertion.
