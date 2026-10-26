# Mo51SentKillSafety — safety review of `mori-pin-check.py` v5's runtime footprint

Seat: sentinel (dispatched; not an independent judge of C1/C2). Round 51, wave `w1`, attack item
(safety of the landed data, detection and report only; no fleet, lane, jj or git-index mutation).

Subject: `tools/mori-pin-check.py` at `87e0c374537557754bf71dd68036ded3ddc6699c` (the data commit), whose
`--rev` mode now builds the measured tree with `git clone --shared` under `--scratch`/TMPDIR instead of a
`git archive` export under `<repo>/.scratch`.

Acceptance of the bytes I reviewed: `git show 87e0c374…:tools/mori-pin-check.py` written to my scratch hashes
`35c69d9115b5e45f91a4b0311ce95c03b3b2b929250e2afb31b571a49687b3bf`, identical to the working-tree copy at
the current tip `b504cb1701568a0038aab9d98ec13d28eff801da`; so the v5 bytes I probed are the landed bytes.

Environment: Linux 7.2.11-arch1-1, git 2.56.0, strace present, jj 0.45.1 (the lane carries `.jj`, i.e. a jj
colocated repo; `.git` is 113M with 1476 loose objects and 2 packs). No tool was installed or upgraded for
this seat. Scratch: `/fast/scratch/hyaku/mori-r51/Mo51SentKillSafety/` with `TMPDIR` set into it for every
probe; `disk-guard.sh status` read clean before the heavy runs (`/fast` 600G free, `/tmp` 125G free) — no
ENOSPC. All fixtures were `git init` repos under my scratch; I asserted `git rev-parse --show-toplevel` equals
the fixture before the first commit in each. `/tmp` writes were confined to one 1.9M fixture residue, removed
immediately (see R5).

## Verdict per risk

| # | Risk asked about | Verdict | Evidence |
|---|---|---|---|
| R1 | hardlinks written into the source repo | **NO** — with `--shared` the source keeps 0 multi-link object files; the `--local` control adds 5 | R1 |
| R2 | `objects/info/alternates` written into the source repo | **NO** — written into the clone only, holding the source's absolute objects path | R1 |
| R3 | any lock taken in the source repo | **NO** — 0 opens with write flags, 0 creat/unlink/rename/mkdir in the source, 0 `*.lock` in the source; a `chmod -R a-w` source clones and checks out fine | R2 |
| R4 | source repo gc'd/repacked while the clone is in use | **REPACK of reachable objects: SAFE** (80/80 clones + full object reads clean against 150 concurrent `gc --prune=now`; reachable rev re-checkouts after a real gc). **PRUNE of the measured rev: BREAKS the run**, and the failure is reported as a bad revision | R3 |
| R5 | source repo moved/deleted under a live clone | breaks until the path returns (`unable to normalize alternate object path`) — the measured tree is not self-contained | R6 |
| R6 | TMPDIR unset, or pointing at `/tmp` | **Default is `/tmp` and is taken silently**; an unusable TMPDIR also falls back to `/tmp` without an error | R4 |
| R7 | size of a checkout in scratch (the /tmp exposure) | **332M / 12,520 files** per run at `87e0c` (objects are borrowed, 4K); a SIGKILLed run leaves **332M / 12,579 files** behind and nothing reaps it | R5 |
| R8 | process cleanup when the checker dies | **Child pinned commands survive** a SIGTERM/SIGKILL of the parent; only a process-group kill (what the counter does) cleans up | R7 |
| R9 | caller can put the tree back under the repo | **YES** — `--scratch <repo>/…` and `TMPDIR=<repo>` are accepted, and a SIGKILL then leaves the round-50 residue shape inside the repo | R8 |

Nothing in this review proposes a change to a counter, predicate, control or kill rule.

## R1 — what `git clone --shared` writes into the source (hardlinks, alternates)

```
$ git init -q $S/fx1 … (2 commits)
$ find $S/fx1/.git -printf '%P %s %n %T@\n' | sort > $S/fx1-before.txt
$ git clone -q --shared --no-checkout $S/fx1 $S/c1 ; echo CLONE-SHARED-RC=$?
CLONE-SHARED-RC=0
$ find $S/fx1/.git -printf '%P %s %n %T@\n' | sort > $S/fx1-after.txt
$ diff -u $S/fx1-before.txt $S/fx1-after.txt && echo SOURCE-DOTGIT-UNCHANGED
SOURCE-DOTGIT-UNCHANGED
$ cat $S/c1/.git/objects/info/alternates
/fast/scratch/hyaku/mori-r51/Mo51SentKillSafety/fx1/.git/objects
$ ls -l $S/fx1/.git/objects/info/            # source: empty, no alternates there
total 0
$ find $S/fx1/.git/objects -type f -links +1 | wc -l
0
$ git clone -q --local --no-checkout $S/fx1 $S/l1 ; echo CLONE-LOCAL-RC=$?      # control
0
$ find $S/fx1/.git/objects -type f -links +1 | wc -l                            # control: --local DOES hardlink
5
$ du -sh $S/c1/.git $S/fx1/.git/objects
112K …/c1/.git
20K  …/fx1/.git/objects
$ ls -l $S/c1/.git/objects/pack
total 0                                       # the clone copies no packs
```

Recursive size/mtime/link-count listing of the source `.git` is byte-identical across the clone; the only
shared state is the clone-side `alternates` file. `--local` (which the tool does **not** use) is what creates
hardlinks in the source — the v5 choice avoids exactly that.

## R2 — locks and writes in the source during a clone

```
$ strace -f -y -e trace=openat,open,creat,flock,fcntl,unlink,unlinkat,rename,renameat,mkdir,mkdirat,link,linkat,rmdir,utimensat,chmod,fchmod \
      -o $S/strace-clone.log git clone -q --shared --no-checkout $S/fx1 $S/c2
STRACE-CLONE-RC=0
$ grep -c "$S/fx1/.git" $S/strace-clone.log
30
$ grep "$S/fx1/.git" $S/strace-clone.log | grep -E 'O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND' || echo NONE
NONE
$ grep -E "(unlink|unlinkat|rename|renameat|mkdir|mkdirat|link|linkat|rmdir|utimensat|chmod|fchmod)\(" $S/strace-clone.log | grep "$S/fx1" || echo NONE
NONE
$ grep '\.lock' $S/strace-clone.log | grep -c "$S/fx1"
0
$ grep -E 'chdir|execve' $S/strace-clone.log | grep -c "$S/fx1"
0
```

Every `.lock` in that trace is inside the *clone* (`c2/.git/config.lock`, `HEAD.lock`, `packed-refs.lock`,
`refs/heads/main.lock`, `objects/info/alternates.lock`). The clone also copies no credentials: the clone's
`.git/config` holds only `core`, `remote.origin.url = <repo>`, `fetch` and `branch.main`.

Read-only source, same operation:

```
$ chmod -R a-w $S/fx1/.git
$ git clone -q --shared --no-checkout $S/fx1 $S/c5 ; echo CLONE-SHARED-RO-SRC-RC=$?
0
$ git -C $S/c5 checkout -q --detach $(git -C $S/c5 rev-parse refs/remotes/origin/main) ; echo CHECKOUT-RO-SRC-RC=$?
0
```

So `--rev` needs no write access and no lock in the repo it reads. (A concurrent ref update is seen as
old-or-new, not torn: git ref updates are lock+rename, and the clone takes no source lock to exclude them.)

## R3 — source gc/repack while a shared clone is in use

### R3a — prune of an unreachable measured revision breaks the run

```
$ git init -q $S/fx2 … main1=ee5454b6; detached commit U=c9a53bea (unreachable after `git checkout main`)
$ git clone -q --shared --no-checkout $S/fx2 $S/c3 ; echo CLONE-RC=$?
CLONE-RC=0
$ git -C $S/c3 cat-file -e c9a53bea… ; echo U-READABLE-BEFORE-RC=$?
0
$ git -C $S/fx2 reflog expire --expire=now --all && git -C $S/fx2 gc -q --prune=now ; echo GC-RC=$?
0
$ git -C $S/c3 cat-file -e c9a53bea… ; echo CATFILE-U-RC=$?
1
$ git -C $S/c3 checkout -q --detach c9a53bea… ; echo CHECKOUT-U-RC=$?
fatal: unable to read tree (c9a53bea4c379a8900404f4a72cf44dfcb305295)
128
$ git -C $S/c3 checkout -q --detach ee5454b6… ; echo CHECKOUT-MAIN1-RC=$?          # reachable rev: control
0
$ git -C $S/c3 show c9a53bea…:u.txt ; echo SHOW-U-RC=$?
fatal: path 'u.txt' does not exist in 'c9a53bea4c379a8900404f4a72cf44dfcb305295'
128
```

`export_rev()` does `rev-parse --verify` → `clone --shared` → `checkout --detach <full sha>` as three
sequential steps, so the interval between clone and checkout is exactly the window in which a prune lands.
A pinned instrument that reads git objects from the measured tree (the reason the witness chose a clone at
all: `.ufo/waves/round-49/count-c1.py`, `tools/mori-round19-regressions.py`, `conform.py`) fails the same way
mid-run, and — because a failed instrument prints no tally — the failure appears as `class=env`, i.e. the run
attributes a broken object store to the environment rather than to the repository.

Realism of the unreachable-rev case in this lane: the lane is jj-colocated (`/home/vgpnk/Projects/shokunin/mori-shokunin/.jj`,
jj 0.45.1), and its git object store already holds abandoned jj objects:

```
$ git -C <lane> fsck --unreachable --no-reflogs --no-progress | awk '{print $2}' | sort | uniq -c
   3050 tree
     79 blob
$ git -C <lane> count-objects -v | grep -E 'count:|in-pack|packs'
count: 1476
in-pack: 18702
packs: 2
```

`git gc --prune=now` (or `jj util gc`, or a `git gc --auto` once loose objects pass the default 6700 — they are
at 1476 today) has real garbage to delete here. No gc/repack invocation exists in the lane's tools or in
`/home/vgpnk/Projects/shokunin/scripts` (grep for `git gc|git repack|jj util gc` over `mori-shokunin/tools`,
`.ufo/waves/round-5*` and `scripts/`: no hits), so this is a human/closure-time event, not a tool-time one.

Scope of the exposure: the scored C1 path is **immune**, because `count-c1.py` builds `git clone --no-local`
clones and passes those as `--repo` (`.ufo/waves/round-51/count-c1.py:73-77,105-106,133-141`), so pin-check's
source is a throwaway clone, never the live lane. The exposure is the ad-hoc/historical rerun that
`corpus/QUALITY.md:1035` and `:1057` document (`python3 tools/mori-pin-check.py --rev <rev> --baseline-rev
<entering>`, run from the lane, no `--scratch`), which is exactly the shape the lane uses to re-execute pins at
an older tip after a jj rewrite.

### R3b — repack of reachable objects and a concurrent gc are safe

```
$ git -C $S/c4 gc -q --prune=now ; echo CLONE-GC-RC=$?           # gc/repack run INSIDE the measured tree
0
$ git -C $S/c4 repack -q -a -d ; echo CLONE-REPACK-RC=$?
0
$ find $S/fx4/.git/objects -type f | wc -l    # source object files before / after the clone's gc+repack
3 / 3
$ git -C $S/fx4 fsck --no-progress ; echo SRC-FSCK-RC=$?
0
```

The measured tree cannot reach or damage the source's objects: its own `gc`/`repack` adds local packs and a
`commit-graph` in the clone, and the source's object set is unchanged and fsck-clean.

Race test (80 clones against 150 sequential `git commit` + `git gc -q --prune=now` in the source):

```
RACE-RESULT ok=80 fail=0
source-fsck: (no output)  SRC-FSCK-RC=0
source-counts: count: 0 / in-pack: 570 / packs: 1
distinct error texts: (empty)
```

Each iteration ran `clone --shared --no-checkout`, `checkout --detach HEAD`, `rev-list --objects --all` and
`cat-file -e HEAD^{tree}`. So git's new-pack-then-unlink ordering keeps an in-flight shared clone readable while
the source repacks (open fds survive unlink). The dangerous operation is prune, not repack.

## R4 — TMPDIR resolution (unset, `/tmp`, `/proc`, a file)

```
$ env -u TMPDIR python3 -c 'import tempfile,os; print("gettempdir=",tempfile.gettempdir(),"TMPDIR=",os.environ.get("TMPDIR"))'
gettempdir= /tmp TMPDIR= None
$ env -u TMPDIR strace -f -e trace=mkdir,mkdirat,rmdir,unlink,unlinkat -o $S/strace-tmp.log python3 pin-check-v5.py --rev <fix> --repo $S/fx3
mkdir("/tmp/pin-check-diapkf8v", 0700) = 0
mkdir("/tmp/pin-check-diapkf8v/tree", 0777) = 0
mkdir("/tmp/pin-check-diapkf8v/tree/.git", 0777) = 0
$ ls -d /tmp/pin-check-*            # after a NORMAL exit
NONE                                 # `finally: shutil.rmtree(scratch)` did run
$ env TMPDIR=/proc/nope python3 pin-check-v5.py --rev HEAD --repo $S/fx3 ; echo RC=$?
PIN_CHECK_SETUP unreadable /tmp/pin-check-mwig18q6/tree/SKILL.md
RC=2
$ env TMPDIR=$S/log-a.txt python3 pin-check-v5.py --rev HEAD --repo $S/fx3 ; echo RC=$?
PIN_CHECK_SETUP unreadable /tmp/pin-check-rek7o_3h/tree/SKILL.md
RC=2
```

An unusable TMPDIR does not fail: `tempfile.gettempdir()` rejects the candidate and the run silently lands in
`/tmp` (the `PIN_CHECK_SETUP unreadable …/SKILL.md` line above is this fixture's missing `SKILL.md`, printed
from the `/tmp` path). There is no warning and no way for a caller to tell which tree it is measuring.

Additional cost that also goes into TMPDIR: `run_cmd()` sets each pinned command's `TMPDIR` to a fresh dir
under `<measured tree>/.scratch` (`tools/mori-pin-check.py:539-545`), so every pinned command's temp files are
inside the tree that already sits in `/tmp`.

## R5 — size of the measured tree, and what a killed run leaves behind

```
$ git clone -q --shared --no-checkout <lane> $S/measure/tree && git -C $S/measure/tree checkout -q --detach 87e0c374…
CLONE-RC=0  CHECKOUT-RC=0
$ du -sh $S/measure/tree
332M
$ du -sh --exclude=.git $S/measure/tree
330M
$ find $S/measure/tree -type f | wc -l
12520
$ find $S/measure/tree -type f -printf '%s\n' | awk '{s+=$1} END {print s" bytes"}'
321483449 bytes
$ cat $S/measure/tree/.git/objects/info/alternates
/home/vgpnk/Projects/shokunin/mori-shokunin/.git/objects
$ du -sh $S/measure/tree/.git/objects
4.0K
$ du -sh -c $S/measure/tree/* | tail -3
26M  …/tree/corpus ; 2.3M …/tree/tools ; 29M total (top level)
$ find $S/measure/tree -type f -printf '%s %p\n' | sort -rn | head -3
30205427 …/tree/.ufo/waves/round-22/evidence/measure3/synthetic-workspaces.tar.gz
27332977 …/tree/.ufo/waves/round-22/evidence/measure2/synthetic-workspaces.tar.gz
 9127248 …/tree/.ufo/waves/round-23/rejected/owned-round23-scratch-evidence.tar.gz
```

So one `--rev` run materialises **332M / 12,520 files** of the lane at the measured revision — 6.6× the
"files under 50 MB" limit of the 2026-10-25 scratch directive — plus whatever the pinned commands write into
`<tree>/.scratch`. `/tmp` has 125G free today, so no ENOSPC is imminent, but the directive is a per-run rule,
and a wave of 64–100 seats running the documented command would hold `N × 332M` transiently.

Killed-run residue, same run against the lane (killed at 2.5 s, process group, TMPDIR in my scratch):

```
$ du -sh $S/tmp/pin-check-evrzep99
332M
$ find $S/tmp/pin-check-evrzep99 -type f | wc -l
12579
$ pgrep -af 'pin-check-v5.py'
NONE
```

and the same shape with TMPDIR unset, on a bounded 3.8M fixture (so nothing large ever sat in `/tmp`):

```
$ env -u TMPDIR setsid python3 pin-check-v5.py --rev HEAD --repo $S/fx6 &  ; sleep 1.5 ; kill -9 -<pgid>
$ ls -d /tmp/pin-check-* ; du -sh /tmp/pin-check-*
/tmp/pin-check-wrjd8n4y
1.9M
$ find /tmp/pin-check-wrjd8n4y -type f | wc -l
58
$ rm -rf /tmp/pin-check-wrjd8n4y
```

`SIGTERM` behaves the same as `SIGKILL` (no handler, no `finally`):

```
$ env TMPDIR=$S/tmp timeout 3 python3 pin-check-v5.py --rev HEAD --repo $S/fx6 ; echo TIMEOUT-RC=$?
TIMEOUT-RC=124
$ ls -d $S/tmp/pin-check-*
$S/tmp/pin-check-1exobqsa
```

Nothing in the fleet reaps these: grep for `pin-check-*` over `scripts/`, `mori-shokunin/tools` and the
round-50/51 wave dirs finds only prose in three round-50 reports, no sweep. The counter's arm A can only see
this when the scratch is inside the repo it reads — it counts `git -C C0 status` lines, and C0 is a clone.

## R6 — the measured tree is not self-contained

```
$ git clone -q --shared --no-checkout $S/fx8 $S/c8 ; mv $S/fx8 $S/fx8-moved
$ git -C $S/c8 checkout -q --detach HEAD ; echo CHECKOUT-AFTER-MOVE-RC=$?
error: unable to normalize alternate object path: /fast/…/fx8/.git/objects
fatal: unable to read tree (854c50897de5c329a5aecc19d7aa0fcdd8c52ab6)
128
$ mv $S/fx8-moved $S/fx8 ; git -C $S/c8 checkout -q --detach HEAD ; echo CHECKOUT-AFTER-RESTORE-RC=$?
0
```

The alternates path is absolute and re-resolved per command (restoring the path makes the clone work again).
Consequence for residue: a `pin-check-*` tree left by a killed run is not a usable copy of the lane and a
dangling pointer once the source moves — it is only disk usage.

## R7 — process cleanup when the checker dies

```
$ env TMPDIR=$S/tmp setsid python3 pin-check-v5.py --rev HEAD --repo $S/fx6 &
$ sleep 1.5
$ pgrep -af 'foo.py --selftest'
1001475 python3 tools/foo.py --selftest
$ kill -TERM <parent>; echo TERM-RC=$?
0
$ sleep 0.8 ; pgrep -af 'foo.py --selftest'
1001475 python3 tools/foo.py --selftest        # still running, reparented
$ ls -d $S/tmp/pin-check-*
$S/tmp/pin-check-6bp6skw4
```

The tool kills nothing on the way out (no `atexit`, no `prctl(PR_SET_PDEATHSIG)`, no process group of its own
in `run_cmd`), so a pinned instrument that hangs keeps its CPU slice after the checker is gone until it next
writes to the closed stdout pipe (SIGPIPE) or exits. The counter masks this because arm A kills its own session
group (`count-c1.py:120-124`, `os.killpg(proc.pid, SIGKILL)`); after a group kill I found no surviving process
(`pgrep -af 'pin-check-v5|fx6'` → `NONE` twice). A manual `kill <pid>` of a rerun does not get that protection.

## R8 — a caller can put the measured tree back under the repo

```
$ python3 pin-check-v5.py --rev <sha> --repo $S/fx3 --scratch $S/fx3/.scratch ; echo RC=$?
PIN_CHECK_SETUP unreadable …/fx3/.scratch/pin-check-qsr532af/tree/SKILL.md     # accepted, not refused
RC=2
$ env TMPDIR=$S/fx6 setsid python3 pin-check-v5.py --rev HEAD --repo $S/fx6 &  ; sleep 1.5 ; kill -9 -<pgid>
$ git -C $S/fx6 status --porcelain --ignored --untracked-files=all | wc -l
1
$ git -C $S/fx6 status --porcelain --ignored --untracked-files=all | head -1
?? pin-check-igw18min/tree/
```

The v5 docstring states the default and the counter never does this, but the tool refuses neither
`--scratch <repo>/…` nor `TMPDIR=<repo>`. Under a kill, arm A's own measurement command then counts the
residue — the round-50 defect returns, one flag away. It also makes the landed wording false as a general
statement: `SKILL.md:938` says the `--rev` tree is "under `--scratch`/TMPDIR, never under the repo", and
`tools/mori-pin-check.py:130-131` says "under `--scratch DIR` (default: the TMPDIR temp dir, never `<repo>`;
removed on exit, and a killed run leaves it in scratch, not in the repo it reads)". What is true is narrower:
*by default, when TMPDIR is a scratch directory, it is outside the repo; the tool does not enforce it, and a
killed or SIGTERMed run leaves the tree wherever TMPDIR/`--scratch` pointed.*

Also stale in the same docstring: line 114 still says `--rev REV [--repo DIR]   export REV with 'git archive'`,
contradicting the v5 paragraph at 126-132 and `export_rev()` at 870-884.

## Named limits of this review

- All mutation-controls were exercised on synthetic fixtures (`git init` in scratch, two to forty commits).
  I did not run `git gc`, `git repack`, `jj` or any write command in `/home/vgpnk/Projects/shokunin` or the lane
  (read-only `git log/show/diff/rev-parse/fsck/count-objects/status` only), so "the lane is never gc'd at this
  moment" is UNVERIFIED; the timing of any lane-wide gc is outside my seat.
- The 80/80 race result bounds a ~2 s fixture workload, not a 332M lane clone (whose clone step reads the same
  packs only to copy refs; its checkout is slower and therefore has a *wider* window). Whether a real lane gc
  would land inside a real `--rev` run is UNVERIFIED.
- I did not test jj's own object writes (gix packs) against a live shared clone; the lane forbids touching jj
  state. Git's atomic pack write is what R3b measures.
- The concurrency cost figure (`N × 332M`) assumes each seat runs a full `--rev`; the counter's own path uses
  counter scratch under `/fast`, so the wave as dispatched is not exposed.
- Whether the disk-guard would catch a `/tmp` fill is not something I could test without filling it; `/tmp`
  (125G) is not one of the guard's reported roots beyond its own threshold check.

## Findings

1. **HIGH — the `--rev` default lands a 332M tree in `/tmp`, breaking the 2026-10-25 scratch directive.**
   `tools/mori-pin-check.py:912-915` (`scratch_parent = … tempfile.gettempdir()`, `mkdtemp` there) with no
   `--scratch`; measured 332M / 12,520 files at `87e0c` (R5). Unusable TMPDIRs silently fall back to `/tmp`
   (R4). A SIGKILL or SIGTERM leaves the whole tree behind (R5) and nothing reaps it. The documented reviewer
   command (`corpus/QUALITY.md:1035`, `:1057`) passes no `--scratch`, so it takes this path.
2. **MED — a source prune of an unreachable measured revision breaks the run and is misreported.**
   `tools/mori-pin-check.py:884-886` (`except (subprocess.SubprocessError, OSError): return None`) collapses a
   failed `checkout` into `main():919-922`'s `PIN_CHECK_SETUP unresolvable revision <rev>`, byte-identical to a
   genuinely missing rev; proven with an unreadable source object (R3a). Mid-run the same breakage appears as
   `class=env` per pinned instrument. Not reachable from the scored path (counter clones are `--no-local`),
   reachable from the ad-hoc historical rerun the lane documents.
3. **MED — a killed checker leaves its pinned child processes running.** `run_cmd()` (`:539-559`) starts
   children in the caller's session with no group and no death signal; SIGTERM to the parent left
   `python3 tools/foo.py --selftest` alive (R7). Only a process-group kill (what `count-c1.py` does) cleans up.
4. **MED — the "never under the repo" wording in the landed data is not enforced.**
   `SKILL.md:938` and `tools/mori-pin-check.py:130-131`; both `--scratch <repo>/…` and `TMPDIR=<repo>` are
   accepted and reproduce the round-50 residue on a kill (R8). True claim: outside the repo *by default when
   TMPDIR is scratch*, not a guarantee.
5. **LOW — stale mode documentation.** `tools/mori-pin-check.py:114` still describes `--rev` as a `git archive`
   export, contradicting `:126-132` and `export_rev()` (`:870-884`); a reader who follows the mode list will not
   expect alternates or a live dependency on the source repo.
6. **LOW — the measured tree depends on the source's path for its whole life.** alternates is an absolute path
   (R1, R6); a moved/deleted source breaks the tree with `unable to normalize alternate object path`, so
   killed-run residue is unusable and only consumes disk.
7. **LOW — no reaper for `pin-check-*` scratch anywhere in the fleet** (grep in R5), and the counter's arm A can
   only observe residue inside the repo it reads, never residue in TMPDIR. Any future sweep must target
   `$TMPDIR/pin-check-*` (or the `--scratch` parent), not the repo.

## Cleanup

All fixtures, clones, strace logs and residues were removed; `du -sh /fast/scratch/hyaku/mori-r51/Mo51SentKillSafety`
is reclaimed at exit. `/tmp/pin-check-*` was removed immediately after each observation (`ls -d /tmp/pin-check-*`
→ nothing). No install, upgrade, pacman transaction or PATH write was performed.
