# Mo51ExecPinCheckLaneRev — v5 re-execution at both tips, off-host env case, no-harm

Seat: executor (leaf). Item: re-run `tools/mori-pin-check.py` v5 in scratch at the data commit
`87e0c374537557754bf71dd68036ded3ddc6699c` and at the entering tip
`aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd`, then reproduce the 2026-10-26 reflection's off-host
case (v5 under `bwrap` with the lane working-tree path hidden, against a `--no-local` clone of the
lane at the entering tip) and answer: does the CONFORM pin print `class=env`? No subagents. No tool
installs or upgrades (python3 3.14.8, git 2.56.0, bubblewrap 0.13.1, kernel 7.2.11-arch1-1 already
present; no pacman). No git/jj mutation in the lane or the fleet root; clones FROM the lane into
scratch only. Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ExecPinCheckLaneRev/` (removed at end;
every cited line is copied below). No host reads beyond `/proc/meminfo`-class files (none needed).

## 0. Tool identity (the v5 bytes I ran are the landed v5 bytes)

```
git -C <lane> diff --quiet 87e0c374537557754bf71dd68036ded3ddc6699c -- tools/mori-pin-check.py      → rc 0
git -C <lane> diff --quiet 87e0c374537557754bf71dd68036ded3ddc6699c -- .ufo/waves/round-40/conform.py → rc 0
sha256sum <lane>/tools/mori-pin-check.py                                                     → 35c69d9115b5e45f91a4b0311ce95c03b3b2b929250e2afb31b571a49687b3bf
git -C <lane> show 87e0c374…:tools/mori-pin-check.py | sha256sum                             → 35c69d9115b5e45f91a4b0311ce95c03b3b2b929250e2afb31b571a49687b3bf
sha256sum <scratch>/mori-pin-check-v5.py (the copy every run below used)                      → 35c69d9115b5e45f91a4b0311ce95c03b3b2b929250e2afb31b571a49687b3bf
```

Environment for every run: `export TMPDIR=/fast/scratch/hyaku/mori-r51/Mo51ExecPinCheckLaneRev/tmp`,
cwd = the scratch dir, absolute paths in every argument. In the command blocks below `<lane>` =
`/home/vgpnk/Projects/shokunin/mori-shokunin` and `<scratch>` =
`/fast/scratch/hyaku/mori-r51/Mo51ExecPinCheckLaneRev`.

## 1. Run A — v5 at the data commit, host, real lane as `--repo`

```
python3 <lane>/tools/mori-pin-check.py --rev 87e0c374537557754bf71dd68036ded3ddc6699c \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <scratch>/run-data     → rc 0, 46 lines
```

45 pin lines = 35 tally + 8 digest + 2 line-count, **all `state=match`, 0 mismatch**. Key lines:

```
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 87e0c374537557754bf71dd68036ded3ddc6699c --selftest'
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=119 fail=0' observed='pass=119 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=87e0c374537557754bf71dd68036ded3ddc6699c baseline=no env=0 stale=0
```

`run-data` was empty after the run (the tool removes its measured tree; see §5). The data tree's
CONFORM pin runs the fixed `conform.py` (LANE derived from its own path) and passes at the data rev.

## 2. Run B — v5 at the entering tip, host, real lane as `--repo`

```
python3 <scratch>/mori-pin-check-v5.py --rev aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <scratch>/run-enter    → rc 0, 46 lines
```

45 pin lines, **all `state=match`, 0 mismatch**. Key lines:

```
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd --selftest'
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=114 fail=0' observed='pass=114 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd baseline=no env=0 stale=0
```

On the host the entering-tip CONFORM pin **holds**, because `conform.py:69` at that rev resolves to
the live lane, where the counter it names exists. That is the reflection's hypothesis ("On the host
the pin likely holds; off-host it can't") confirmed by the host/off-host pair (§1–§3). The only
per-pin difference between the two host runs is the reconciler's own tally, 114 → 119 (v4 → v5).

## 3. Off-host reproduction (the reflection's case)

Fixture (one `--no-local` clone, asserted before any checkout):

```
git clone -q --no-local <lane> <scratch>/clone-aa3af                                   → rc 0
git -C <scratch>/clone-aa3af rev-parse --show-toplevel → /fast/scratch/hyaku/mori-r51/Mo51ExecPinCheckLaneRev/clone-aa3af (equals the fixture dir)
git -C <scratch>/clone-aa3af checkout -q --detach aa3af1ec…                            → rc 0
test -e <scratch>/clone-aa3af/.git/objects/info/alternates                              → absent (self-contained object store)
```

Isolation sanity (same bwrap flags as every run below):

```
bwrap --bind / / --dev /dev --proc /proc --tmpfs /home/vgpnk/Projects/shokunin/mori-shokunin \
  sh -c 'test -e <lane>/SKILL.md …; test -e <scratch>/clone-aa3af/.ufo/waves/round-40/conform.py …'
→ lane_skill=hidden   clone=visible   vgpnk   2      (rc 0)
```

Direct demonstration of the failure the pin sees (measured tree at the entering tip, built the way
`export_rev` builds it: `git clone --shared --no-checkout` of the clone, `checkout --detach aa3af1e`):

```
cd <scratch>/probe-offhost && bwrap --bind / / --dev /dev --proc /proc --tmpfs <lane> \
  python3 .ufo/waves/round-40/conform.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd --selftest
→ rc 2
conformance setup error: [Errno 2] No such file or directory: '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/count-c8.py'
```

### Run C1 — first off-host run (measured tree cloned from a detached-HEAD source)

`git -C clone-aa3af symbolic-ref -q HEAD` → empty (detached), because I had checked the fixture out
at the entering tip. `git clone --shared --no-checkout` from a detached-HEAD source creates **no local
branch**, so the measured tree had no `master`:

```
git -C <measured tree> rev-parse --verify 'master^{commit}'        → rc 128 (probe-detached)
( cd probe-detached && python3 .ufo/waves/round-49/count-c1.py --selftest ) → rc 1, last line `C1_SELFTEST pass=0 fail=1`
```

Every mismatch line and the summary line of that run:

```
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=mismatch pinned='pass=11 fail=0' observed=None rc=2 cmd='python3 .ufo/waves/round-40/conform.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd --selftest' class=env
pin line=1009 kind=tally prefix=C1_SELFTEST state=mismatch pinned='pass=44 fail=0' observed='pass=0 fail=1' rc=1 cmd='python3 .ufo/waves/round-49/count-c1.py --selftest' class=stale
PIN_CHECK=unmet tally_pins=35 digest_pins=8 mismatches=2 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd baseline=no env=1 stale=1
```

The second mismatch is my fixture's shape, not the entering tree: `.ufo/waves/round-49/count-c1.py`
derives `LANE` from its own path (line 53) and resolves `git -C LANE rev-parse --verify master^{commit}`
(lines 353 and 422); with no local branch in the tree the selftest short-circuits and prints a tally,
so v5 classes it `stale`. The host run of the same rev (§2) and a `--shared` clone taken directly from
the lane both carry `refs/heads/master` (`b504cb17…`) and pass.

### Run C2 — corrected fixture: fixture HEAD restored on its natural branch before measuring

```
git -C <scratch>/clone-aa3af checkout -q master ; git -C <scratch>/clone-aa3af symbolic-ref -q HEAD
→ refs/heads/master ; rev-parse HEAD → b504cb1701568a0038aab9d98ec13d28eff801da
git clone -q --shared --no-checkout clone-aa3af <tree> ; git -C <tree> checkout -q --detach aa3af1ec… → rc 0
git -C <tree> rev-parse --verify 'master^{commit}' → b504cb17…   ; rev-parse HEAD → aa3af1ec…
```

This matches the measured tree the host runs of §1–§2 got from the lane (same ref inventory).

```
bwrap --bind / / --dev /dev --proc /proc --tmpfs <lane> \
  env TMPDIR=<scratch>/tmp-off python3 <scratch>/mori-pin-check-v5.py \
  --rev aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd --repo <scratch>/clone-aa3af \
  --scratch <scratch>/run-offhost2                                  → rc 1, 46 lines
```

Every mismatch line and the summary line (the one mismatch is the reflection's case):

```
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=mismatch pinned='pass=11 fail=0' observed=None rc=2 cmd='python3 .ufo/waves/round-40/conform.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd --selftest' class=env
PIN_CHECK=unmet tally_pins=35 digest_pins=8 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd baseline=no env=1 stale=0
```

The other 44 pin lines are `state=match`, including the two that need a repository in the tree
(`pin line=938 … observed='pass=114 fail=0' rc=0`, `pin line=1009 … observed='pass=44 fail=0' rc=0`).

### Run C3 — the same isolation at the data commit (the turn from §1–§2 repeated off-host)

```
bwrap --bind / / --dev /dev --proc /proc --tmpfs <lane> \
  env TMPDIR=<scratch>/tmp-off python3 <scratch>/mori-pin-check-v5.py \
  --rev 87e0c374537557754bf71dd68036ded3ddc6699c --repo <scratch>/clone-aa3af \
  --scratch <scratch>/run-offhost-data                              → rc 0, 46 lines
```

45 pin lines, all `state=match`, 0 mismatch:

```
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 87e0c374537557754bf71dd68036ded3ddc6699c --selftest'
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=119 fail=0' observed='pass=119 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=87e0c374537557754bf71dd68036ded3ddc6699c baseline=no env=0 stale=0
```

**Answer to the item's question: yes.** Off-host at the entering tip the CONFORM pin prints exactly
`state=mismatch … observed=None rc=2 … class=env`, one mismatch total, `env=1 stale=0` — the split
`considerthese/2026-10-26.md` suggestion 1 asks for, at the exact line (SKILL.md:911) the reflection
named. The data-commit tree is not exposed to it: under the same hidden path `--rev 87e0c37` is
`PIN_CHECK=met` with 45/45 pins matching and the CONFORM pin `pass=11 fail=0 rc=0` (run C3), because
the fixed `conform.py` derives `LANE` from its own path instead of the host path.

## 4. considerthese check (suggestion 1, env versus stale)

1. Implemented and effective for the named case: a pinned command that cannot run here (missing
   hardcoded host path, setup exit 2, no tally line) is `class=env`; the summary carries `env=N
   stale=N` with `env + stale = mismatches` (run C2: `env=1 stale=0`; run A: `env=0 stale=0`).
2. The rule is prefix-presence, so an environmental failure that still prints a tally is `stale`.
   Run C1 is a live instance: the round-49 counter prints `C1_SELFTEST pass=0 fail=1` when its
   `master^{commit}` read fails, and v5 calls that `stale`. This is the contract's named limit
   ("a tool that prints a tally and then fails for an environmental reason is classed stale"),
   now reproduced with a concrete trigger (a measured tree without a local branch).
3. The env class reports *that* a host path is missing; it does not name the path. The direct
   `conform.py` run (§3) is what shows `/home/vgpnk/…/round-40/count-c8.py`. A report that only
   quotes the pin line cannot tell "lanes differ" from "a setup file is absent elsewhere".
4. Nothing in v5 writes a host path: all three off-host runs and both host runs left their
   measured trees inside `--scratch` and removed them (`run-data`, `run-enter`, `run-offhost`,
   `run-offhost2`, `run-offhost-data` all empty afterwards).
5. One stale doc line remains (see Findings LOW). Line 114 of the same docstring still says the
   `--rev` export is made "with `git archive`", while the paragraph at lines 128–133 and the code
   at lines 870–890 clone. A reader who reads only "Modes" gets the pre-v5 mechanism.

## 5. No-harm

- The lane's git state is untouched: `git -C <lane> status --porcelain --ignored --untracked-files=all
  -- .ufo/waves/round-40 tools/mori-pin-check.py SKILL.md SHONEN.md` → **0 lines** when run at 19:52,
  after my last run and before the sibling residue noted below appeared (19:53–19:55). No add/commit/
  checkout/reset/stash/push, no jj command, nothing written to `~/.local/bin` or a PATH dir, no
  fleet-root tracked file.
- Writes I did cause, disclosed: (a) all clones and measured trees live only in my scratch and are
  gone; (b) the **host** run B executed the entering-tip CONFORM argv (line 35 of that output), and
  `conform.py` at that rev creates its scratch under the hardcoded `SCRATCH_ROOT` (lines 70, 742–743)
  and removes it in `finally` (line 765) — i.e. one host-side run transiently created and deleted a
  `mori-conform-selftest-*` dir inside the **live lane's** `.ufo/waves/round-40/scratch`. No file
  remains: that dir's children still carry their pre-run mtimes (`selftest-v3-draft.txt`,
  `mutconform-arms2` both 09:07) and its own mtime moved (19:48, then 19:51:37 after my last run).
  At 19:52, after my last run, the status query above answered **0 lines**. Attribution of the
  19:48 bump to my run is INFERENCE. At 19:55 the same path carries two leftover
  `mori-conform-selftest-858cf_2r/` and `mori-conform-selftest-y5k7kzyi/` directories (14 untracked
  files) created by **concurrent sibling seats'** host-side runs at 19:53–19:54 — after my last run
  (19:50:33) and while those seats are live; I did not create them and did not delete them. My own
  runs' residue is zero.
- Not harmed: no cgroup, sysctl, swap, watermark, systemd unit, journal or kernel-log access; no
  OOM triggered; host reads kept to nothing outside the lane repo and scratch.
- Disk guard was checked before the heavy runs (`scripts/hyaku/disk-guard.sh status`, rc 0, /fast
  604G free); /fast ended at 603G free. Nothing unbounded was streamed to a file; every output
  captured is < 50 KB.

## 6. Independent read of the claim's surface (not a verdict on P-C1)

- At `87e0c374` on the host the tool reports `PIN_CHECK=met` over 35 tally + 8 digest + 2 line-count
  pins, and its own selftest tally observed through the registry pin is `pass=119 fail=0`, which
  agrees with `evidence/c1-at-data.txt` (`selftest=pass=119,fail=0`).
- The data commit's CONFORM pin gets `pass=11 fail=0 rc=0` with `--rev 87e0c37`, i.e. the fixed
  `conform.py` runs inside the measured tree; the entering tip's copy of that pin gets `rc=2` and
  `class=env` once the lane path is hidden. The arm-B mechanism the contract describes is therefore
  visible in the direction claimed (relocated execution works at R, fails at the entering tip when
  the path is hidden), but that is a re-execution observation, not a re-scoring of the counter.
- UNVERIFIED by me: arm A (SIGKILL residue timing), arm C (the five-row fixture registry) and the
  frozen `count-c1.py` verdict; I did not run the counter. Also untested: a kill landing while a
  hardcoded-path instrument is writing into the live lane (would require SIGKILL during conform's
  selftest at the entering tip; not part of this item).

## Findings

- **LOW — stale docstring in the landed v5.** `tools/mori-pin-check.py:114` still documents the
  `--rev` mode as "export REV with `git archive`", contradicting lines 128–133 ("a `git clone
  --shared` checked out at the revision") and `export_rev` (lines 870–890). Code is correct; the
  Modes paragraph is pre-v5. Concerns the data commit `87e0c37`.
- **MED — measured-tree ref inventory depends on the source repo's HEAD shape.** A `--shared`
  clone of a detached-HEAD source yields a measured tree with no `refs/heads` at all, and
  `.ufo/waves/round-49/count-c1.py` (path-derived `LANE`, line 53; `master^{commit}` at lines 353
  and 422) then prints `C1_SELFTEST pass=0 fail=1` (rc 1) — classified `class=stale` although the
  cause is the fixture, not drift (run C1, `pin line=1009`, `probe-detached`). Corroborates the
  ambient-ref MED of `w1/Mo51CritExportClone.md` from a different angle: the tree is not a function
  of R alone, and the failure prints a tally so the env/stale split cannot catch it.
- **MED — a pinned instrument with a hardcoded host path writes into the live lane, and the residue
  arm cannot see it.** At the entering tip, `.ufo/waves/round-40/conform.py:69–76` hardcodes
  `LANE`/`SCRATCH_ROOT`; running the pin host-side (`--rev aa3af1ec`, `--repo <lane>`) executed that
  argv to completion (pin `match pass=11 rc=0` in run B), and that revision's selftest is
  `os.makedirs(SCRATCH_ROOT, exist_ok=True)` then `tempfile.mkdtemp(prefix="mori-conform-selftest-",
  dir=SCRATCH_ROOT)` with `shutil.rmtree` in `finally` (lines 742–743, 765) — so one temp dir was
  created and removed under `<lane>/.ufo/waves/round-40/scratch` by my host run (the 19:48 mtime bump
  there is consistent; that bump cannot be attributed to my run alone because sibling host-side runs
  also write that root — they left the two dirs noted in §5 at 19:53–19:54). No residue from my run. The
  same instrument returns `rc=2` off-host
  (`… No such file … count-c8.py`, §3), which v5 reports as `class=env`. C1's arm A counts residue
  only in the repo passed to `--repo`/the measured tree, so this write path is outside what it
  measures. The landed rev is not affected (`conform.py` derives LANE from its own path there, pin
  `match pass=11 rc=0`; no other lane path changed during my data run).
- **LOW — env/stale is a prefix-presence rule, with a reproduced misclassification.** Any
  environmental failure that prints its tally prefix is `stale` (run C1's round-49 pin; the
  contract's named limit). The summary never names the missing path, so a report must pair the pin
  line with a direct run of the instrument (§3) to show the cause.
- **INFO — the reflection's off-host case reproduces exactly.** At `aa3af1ec` with the lane path
  hidden: 1 mismatch, `SKILL.md:911 CONFORM_SELFTEST … class=env`, `env=1 stale=0`, rc 1; on the
  host the same rev is `PIN_CHECK=met` with the same pin `match pass=11 rc=0`. Both tips' full
  registry reads are `mismatches=0` on the host, and the reconciler's own pinned tally is
  `pass=119` at the data rev and `pass=114` at the entering tip.
