# Mo51SentBwrap — sentinel: write/kill isolation of the C1 counter and its controls

Seat: Mo51SentBwrap (sentinel, leaf). Lane: mori-shokunin. Wave w1, round 51.
Scratch: `/fast/scratch/hyaku/mori-r51/Mo51SentBwrap/` (created, used, `rm -rf`d at the end; `TMPDIR` was `<scratch>/tmp`).
Host reads only; the lane, the fleet root, the jj/git state and the frozen bytes were not modified by this seat.

Surface reviewed (bytes = frozen bytes; sha256 re-checked against `evidence/freeze-sha256.txt`):

```
$ sha256sum .ufo/waves/round-51/count-c1.py .ufo/waves/round-51/controls/c1-controls.py
622f650c1ade984d8c9abed20e7a7fd08930861a698398f36d4c3a770aff355c  .ufo/waves/round-51/count-c1.py
8351ba6d4008037ef3f2694b73f9e2e9cad41bb5cb77ea21dc7511556266887a  .ufo/waves/round-51/controls/c1-controls.py
$ grep -n 'count-c1\.py\|c1-controls\.py' .ufo/waves/round-51/evidence/freeze-sha256.txt
10:622f650c...aff355c  .ufo/waves/round-51/count-c1.py
 7:8351ba6d...6266887a  .ufo/waves/round-51/controls/c1-controls.py
```

Both match the freeze file, so this review is of the frozen counter. Disc guard before heavy work:
`bash scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku 26% free 599.7G`, rc 0; after cleanup 603G free.
Nothing was installed or upgraded (no pacman — paused host-wide — and no other channel needed).

Host context measured for this review: bubblewrap 0.13.1 (`/usr/bin/bwrap`, mode 755, not setuid),
`/proc/sys/kernel/yama/ptrace_scope = 1`, lane at 491M (`.git` 113M), lane path a plain directory
(`drwxr-xr-x vgpnk vgpnk`) under `btrfs rw,noatime,compress=zstd:3`, writable by uid 1000.

Landed invocation context (read from `evidence/c1-at-data.txt`): the claim's run used
`--scratch /fast/scratch/hyaku/mori-r51/L1/atdata` (outside the lane), no `--keep` (grep for `--keep`
over `evidence/*.txt` → none), and the same path for every control receipt. So the landed measurement did
**not** exercise any of the unsafe arguments below; the findings are about the counter's API, its failure
modes, and what the bwrap arm can be cited for, not about the correctness of the C1=met receipt.

## V1 — `--bind / /` + `--tmpfs <lane>`: can the measured tool write to the host outside scratch, and can it reach the real lane?

**Writes to the host outside scratch: YES, by construction.** `count-c1.py:140-141` binds the host root
read-write and mounts only one tmpfs over the lane:

```python
argv = ["bwrap", "--bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", lane_hidden,
        "--chdir", w, "--setenv", "TMPDIR", tmp, "--", sys.executable, "-c", probe]
```

Observed from inside that exact argv shape (`--tmpfs` over a scratch dir; writes confined to my scratch):

```
$ bwrap --bind / / --dev /dev --proc /proc --tmpfs <hide> -- sh -c \
    'id; grep -E "^(CapEff|NoNewPrivs|Seccomp)" /proc/self/status; test -r /etc/shadow && echo SHADOW-READABLE; test -w /etc && echo ETC-WRITABLE'
uid=1000(vgpnk) gid=1000(vgpnk)
CapEff:	0000000000000000
NoNewPrivs:	1
Seccomp:	0
shadow-unreadable
etc-not-writable
rc=0

$ bwrap --bind / / --dev /dev --proc /proc --tmpfs <hide> -- sh -c \
    'for p in /home/vgpnk/Projects/shokunin /home/vgpnk/.local/bin /home/vgpnk/.config /tmp; do test -w "$p" && echo "writable $p"; done'
writable /home/vgpnk/Projects/shokunin
writable /home/vgpnk/.local/bin
writable /home/vgpnk/.config
writable /tmp

$ bwrap --bind / / --dev /dev --proc /proc -- sh -c 'printf "BIND-RW\n" > <scratch>/plain-write.txt && echo plain-write-ok'
plain-write-ok        exit 0        # no tmpfs on that path: the bind is read-write
```

So the sandbox is a **one-path mask**, not a write barrier: no `--unshare-net`, no seccomp
(`Seccomp: 0`), same uid, no `--clearenv`. The caller's whole environment is inherited — verified with a
marker variable and with the host's SSH agent socket:

```
$ PROBE_TOKEN=secret-value-xyz bwrap --bind / / --dev /dev --proc /proc --tmpfs <hide> -- sh -c \
    'echo PROBE_TOKEN=${PROBE_TOKEN:-<unset>}; echo ssh=$SSH_AUTH_SOCK'
PROBE_TOKEN=secret-value-xyz
ssh=/run/user/1000/ssh-agent.socket        exit 0
```

and the network namespace is shared (`net:[4026531833]` inside and outside; `/sys/class/net` inside lists
`enp7s0`, `docker0`, `br-*`). Merely path-visibility is claimed by the contract, and the contract's named
limits say the counter "trusts bubblewrap's mount namespace" — that disclosure is accurate; the arm must
not be cited as evidence of confinement.

**Through to the real lane: not found on this host.** Three candidate paths were checked:

1. *Masked path itself*: `<hide>` inside is an empty tmpfs (`ls -A` → nothing; marker file invisible), while
   visible outside — the mask works for plain path resolution.
2. *`/proc/<pid>/root` of a same-uid process outside the sandbox*: read and write both denied, i.e. the
   mask cannot be bypassed this way here:
   ```
   $ bwrap ... --tmpfs <hide> -- sh -c 'ls -A /proc/<host-pid>/root<hide>; cat /proc/<host-pid>/root<hide>/marker.txt'
   ls: cannot access '/proc/935460/root/.../probe/hidden': Permission denied
   cat: /proc/935460/root/.../probe/hidden/marker.txt: Permission denied          exit 1
   $ bwrap ... -- sh -c 'printf X > /proc/<host-pid>/root<hide>/via-proc.txt'
   /bin/sh: line 1: .../via-proc.txt: Permission denied                           exit 1
   ```
   The denial is the user-namespace boundary (sandbox `CapEff=0`, target in the parent namespace), so it does
   not depend on Yama being 1 on another host — but any host where the sandboxed process holds
   `CAP_SYS_PTRACE` in the target namespace, or where the sandbox is disabled, reopens this.
3. *Hardlinks / alternate mounts*: `find <lane> -xdev -type f -links +1` → no output (no hardlinked lane
   file); `findmnt -l` shows no second mount of the lane subvol (`@home` mounted only at `/home`). A
   hardlinked inode or a bind mount of the lane elsewhere would bypass the tmpfs; neither exists now.

Residual (not a claim defect): the measured code at R runs with host-rw, network and the caller's
environment for up to 3000 s (`count-c1.py:142`). If a revision's instrument ever executes fetched code,
that is exfiltration + host write in one step.

## V2 — Does `killpg` on `start_new_session` reach only the child group?

**Yes — and only members that do not call `setsid`/`setpgid`.** `count-c1.py:106-108` starts the measured
tool with `start_new_session=True`; `:121` does `os.killpg(proc.pid, SIGKILL)`. `proc.pid` is the new
session/group leader, so the signal covers the leader and every descendant that stayed in that group —
which is what the counter needs. Two verified properties, one positive and one limit:

Positive, the pid cannot be recycled on the normal path: the child is a zombie until `proc.wait()` (`:124`),
which runs *after* `killpg`, so the pgid is still owned by the unreaped leader.

Limit, an escaped descendant survives (generic POSIX, demonstrated with the same primitive):

```
child:  subprocess.Popen([sys.executable, "-c", code], start_new_session=True)
code:   subprocess.Popen(['setsid', 'sleep', '47']); time.sleep(30)
parent: os.killpg(c.pid, SIGKILL); c.wait()      # -> child gone
survivor: pid 940314  pgid=940314 sid=940314  cmd='sleep 47'
```

`tools/mori-pin-check.py` at the landed revision spawns no session of its own (`grep -nE
'start_new_session|setsid|os.fork|daemon'` over `git show 87e0c37:tools/mori-pin-check.py` → no matches;
all its children are `subprocess.run(...)` at lines 551, 877, 880, 882, 936, 1466-1490 without
`start_new_session`), so for the landed tool the group kill is complete. A *pinned instrument* run by
pin-check that calls `setsid` would escape and keep writing into C0 after the residue snapshot; the residue
would then be an undercount. That belongs to the contract's named limit "arm A kills at one moment"; the
mechanism (group-only reach) is now on record.

Two secondary defects in the same block (LOW): `:112` can `poll()` (and therefore reap) the child, and then
`:121` kills `proc.pid` after it has been reaped — if that pid is reused as a group leader in the gap, an
unrelated group is killed (microsecond window); and `:124` has no timeout, so a tool left in D state makes
the counter hang forever after the kill.

## V3 — Can a scratch dir inside the lane be passed (the `commonpath` check)?

**Directly (lexically) no; through a symlink yes.** `:225-229`:

```python
base = os.path.abspath(a.scratch) if a.scratch else tempfile.mkdtemp(prefix="mori-r51-c1-")
for inside in (repo, os.path.abspath(a.hide)):
    if os.path.commonpath([base, inside]) == inside:
        print("C1_SETUP scratch inside %s" % inside); return 2
```

`abspath` is lexical; no `realpath`. Acceptance matrix computed with the same two lines:

```
candidate-scratch                                            | lexical-in-lane | realpath-in-lane | counter
/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/x       | True            | True             | REFUSED
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/.../x       | True            | True             | REFUSED
/home/vgpnk/Projects/shokunin/scratch-r51                    | False           | False            | accepted
/home/vgpnk/.local/bin                                       | False           | False            | accepted
/tmp/mori-x                                                  | False           | False            | accepted
<scratch>/lane-link/.scratch/x   (lane-link -> lane)          | False           | True             | accepted
```

End-to-end proof of the symlink bypass with a throwaway fixture repo in scratch (a symlinked `--scratch`
pointing at the `--hide` path; no lane path touched):

```
$ python3 count-c1.py HEAD --repo <scratch>/fxrepo --scratch <scratch>/lnk --hide <scratch>/inner --keep
C1_SETUP tool absent at rev            exit 2
$ ls <scratch>/inner
c1-la0f_9m8        # c0, c1, relocated.out, tmpA, tmpB, tool-at-rev
```

So a symlinked `--scratch` is materialised *inside* the path the counter was told to keep writes out of;
pointed at the lane, the two `--no-local` clones, the archive tree and the fixture tree would land in it.
Two related gaps, same lines: (a) the guard protects the lane only — a scratch in the fleet repo root or in
a PATH directory (`~/.local/bin`) is accepted; (b) when `--scratch` is omitted, `mkdtemp` at `:225` creates
the base *before* the check, so the refusal at `:229` leaks it:

```
$ TMPDIR=<hide2>/tmp python3 count-c1.py 87e0c37... --repo <lane> --hide <hide2>
C1_SETUP scratch inside <hide2>        exit 2
leftovers in <hide2>/tmp: ['mori-r51-c1-thk6lffv']     # created at :225, never removed
```

With `TMPDIR` inside the lane this is a lane write on the refusal path; with the default TMPDIR it is a
leaked directory per refused invocation.

## V4 — Does `--keep` leak?

**Yes, and abnormal termination leaks without `--keep`.** `:258-262` removes `w` (and a self-created `base`)
only in the `finally` of an in-process exception path. Consequences, all reproduced:

* `--keep` keeps `w` = two `--no-local` clones (≈113M objects each) + checked-out working trees + the
  archive tree + fixture ≈ 1 GB class per run; with the default scratch it also keeps the `mkdtemp` base.
  The landed receipts did not use `--keep`, and the L1's scratch is empty now (`du -sh .../L1/atdata` → 0).
* SIGKILL/SIGTERM/SIGHUP run no `finally`: clones stay and the measured tool keeps running. Fixture with a
  stub tool that writes beats into `TMPDIR`; the counter was SIGKILLed once arm A was inside its window:

```
counter rc=-9 dead=True
orphaned measured tool: pid 1094766  'python3 .../kill/c1-3plpqoou/c0/tools/mori-pin-check.py --rev ...'
beats written AFTER counter death: 6
clone left behind: ['c1-3plpqoou']  (c0, tmpA)
```

The orphan is expected from V2/V5: arm A's child is in its own session, so even a group SIGKILL of the
counter cannot reach it; arm B's bwrap child has no `--die-with-parent` (see V5).

## V5 — Is any write unbounded?

**Yes, in the output path, and the host-rw process has a 3000 s budget.** Evidence:

* `relocated.out` (`:144-145`) is the full captured stdout of the bwrap'd tool, no cap, no size check. A
  fixture tool printing 16 MiB produced `relocated.out bytes=16777218` — every byte the tool prints lands
  in the scratch file, and the same bytes were first accumulated in memory by `sh()` (`:70`,
  `stdout=PIPE` at `:142`; arm D has the same shape at `:198`). This is exactly the "unbounded stream to a
  file" shape the operator directive 2026-10-26 forbids in seat processes.
* `:142` gives the host-rw sandbox 3000 s; on `subprocess.run` timeout only **bwrap** is killed, and the
  inner tool survives — no `--die-with-parent`, demonstrated:

```
$ bwrap --bind / / --dev /dev --proc /proc --tmpfs <hide> -- sh -c 'echo <token>; sleep 45'
# from the parent: os.kill(p.pid, SIGKILL); p.wait()
ORPHAN after bwrap SIGKILL: [(935584, '/bin/sh -c echo ORPHAN-R51-BWRAP-PROBE-93; sleep 45; ...')]
```

  i.e. after the counter's own timeout/exit, a process with host-rw and network access keeps running while
  the `finally` deletes the scratch tree underneath it. Arm A has the same orphan property (own session).
* `count_entries` (`:95-101`) is bounded at 100 entries (good); arm A's own stdout goes to `DEVNULL`
  (`:107`, good). Arm A's writes into scratch are bounded by the 3 s window after the first observed write,
  not by size, and the counter never consults the disk guard.

## V6 — `controls/c1-controls.py`: every `git -C` target, and can a commit reach the lane?

Inventory of every git invocation (grep of `["git"`): `git()` helper at `:36-38` builds
`["git", "-C", k] + args`; the only other call is the clone at `:48`
(`git clone -q --no-local <LANE> <scratch>/K`, destination explicit). So every mutating call — `checkout
--detach` `:67`, `add` `:71`, `commit` `:72-73`, `branch -f` `:74` — names `-C K` inside scratch, and the
toplevel assertion at `:49` precedes the first commit. Identity is per-commit (`-c user.name=... -c
user.email=...`), so no `~/.gitconfig` write. Verified by a dry run (bogus base rev, scratch paths only):

```
$ python3 c1-controls.py 0000...0000 <scratch>/ctl <scratch>/ctl/out
subprocess.CalledProcessError: Command '['git', '-C', '<scratch>/ctl/K', 'rev-parse', '--verify', '000...0^{commit}']' returned non-zero
$ git -C <scratch>/ctl/K rev-parse --show-toplevel
<scratch>/ctl/K                                      # assertion target is the fixture, not the lane
$ git -C <lane> rev-parse HEAD
b504cb1701568a0038aab9d98ec13d28eff801da             # unchanged across my whole review
$ git -C <lane> for-each-ref | grep -c ctl-  ->  0
```

Positive: no commit can reach the lane; the lane is read through `clone`/`rev-parse`/`show`/`archive` only,
and `count-c1.py` itself writes only under its own `w`. **The list contains only read-only lane access.**

Weaknesses in the driver (LOW/MED, resource not integrity): nothing is ever removed — on failure (as
above) `K` (a 113M–1G clone with five control commits) stays, and `s-<name>` scratch dirs stay after a
successful run too (`:76-90`, no `rmtree` anywhere). All six counters are launched concurrently
(`:79-86`), each cloning the lane twice with `--no-local` (≈1.2 GB and a full checkout each), with no
disk-guard call and no cap on total concurrency. Receipts are opened at `:81` and receive the counter's
whole stdout unbounded; `p.wait()` at `:87` has no timeout; if `Popen` raises after `open`, the receipt fd
leaks and a receipt without an `exit=` line is left behind. `BASE_REV` is passed to `rev-parse` without a
`--` guard (`:51`); harmless while the L1 passes a hash.

## Verdicts

| item | verdict |
|---|---|
| bwrap `--bind / /` rw + `--tmpfs` lane — tool can write host outside scratch | **YES** (rw root, no seccomp, shared net/PID ns, caller env inherited); arm B is a path-visibility test only, as the contract's named limit says |
| anything inside writes through to the real lane | **Not on this host** (mask holds; `/proc/<pid>/root` denied by the userns boundary; no hardlinked lane file; no alternate mount). Userns/permission-dependent, not counter-enforced |
| arm A (unsandboxed) writes to the lane | **Not measured at all** — arm A runs code at R with no sandbox and checks only `git -C C0 status`; a tool writing elsewhere leaves `kill_residue=0` |
| `killpg` reaches only the child group | **Yes**, plus every same-group descendant; a `setsid` descendant escapes (demonstrated). pin-check at R creates no session, so the landed tool is reached fully |
| scratch inside the lane via `commonpath` | **Refused lexically**; **accepted through a symlink** (demonstrated, clones materialised inside the hidden path); fleet-root and PATH-dir scratches accepted |
| `--keep` leak | **Yes** (clones + base); SIGKILL/SIGTERM leaks without `--keep`; refusal path leaks the `mkdtemp` base |
| unbounded write | **Yes** — `relocated.out` = full tool stdout (16 MiB reproduced), PIPE capture unbounded, host-rw process up to 3000 s, no disk-guard check |
| bwrap mount-point creation | `--tmpfs` over a nonexistent path is created **through the rw bind**, i.e. the counter mkdirs on the host; the setup probe then passes trivially and a fixture printing `PIN_CHECK=met` scored `relocated=met` with nothing hidden: `C1=unmet kill_residue=none relocated=met reloc_mismatch=0 ...` with the hide dir created empty |
| controls' `git -C` targets | all `-C K` in scratch, toplevel asserted, no commit or ref reaches the lane; lane HEAD `b504cb17…` unchanged |

Scope statement: none of the above shows the landed `C1=met` receipt wrong. The receipt's `--scratch` is
outside the lane, no `--keep` was used, arm B used the default `--hide` (the real lane, which exists and
contains `SKILL.md`), and the measured tool at R spawns no session of its own. What the findings say is that
(a) the counter is not a write barrier or a sandbox for the code it executes, (b) the bwrap arm's green
proves path visibility only, and (c) several counter arguments can be pointed at the lane or at the host
without the counter noticing. Two readings I could not check and mark **UNVERIFIED**: whether the landed
arm A run wrote to the lane from inside the tool at any moment (the counter records no such evidence), and
whether a closure re-execution passes registry values other than the L1's (that path is out of this seat).

Seat discipline note: I ran `git -C <lane> status --porcelain` twice as a read-only check before switching
to `ls-files --others`; `git status` may refresh `.git/index` (stat cache; index mtime 19:44:21, which may
be mine). No ref, HEAD, worktree or file content changed (`HEAD b504cb17…` before and after, 1663 refs, no
`ctl-*` ref). The untracked count moved 5 → 4 between my two reads while ~200 seats are live; I attribute
that to concurrent seats, not to my commands.

## Findings

1. **HIGH — arm A executes the revision's code with no sandbox, and its only write check is the clone.**
   `count-c1.py:98-128` (Popen at `:106-108`, residue at `:127`). The tool at R runs as uid 1000 with the
   lane, fleet root and `~/.local/bin` writable, for up to 180 s before the kill; only `git -C C0 status` is
   inspected, so a tool (or a control commit's overreach) that writes the lane or any host path outside C0
   still yields `kill_residue=0`. Smallest remediation: run arm A under the same mask as arm B
   (`bwrap --ro-bind / / --tmpfs <lane> --bind <w> <w> --die-with-parent --new-session`), or at minimum
   record `git -C <lane> status` before/after arm A in the counter output — as a named limit of this frozen
   counter, not a change to it this round.
2. **MED — the bwrap arm is a one-path mask, not confinement, and it inherits the caller's environment and
   network.** `count-c1.py:140-141`. `--bind / /` read-write, `Seccomp: 0`, same uid, `--unshare-net` absent
   (`net:[4026531833]` shared), env not cleared (`SSH_AUTH_SOCK` visible inside). The contract discloses the
   mount-namespace trust; the environment/network inheritance is not disclosed. Smallest remediation:
   `--clearenv --setenv TMPDIR <tmp> --unshare-net --die-with-parent --new-session`, and `--ro-bind / /`
   with a rw bind for the scratch that must be written.
3. **MED — no `--die-with-parent`: a timeout or counter death orphans a host-rw process.** `count-c1.py:142`
   (`sh(..., timeout=3000)` kills bwrap only) and arm A's `start_new_session` child (`:106-108`). Reproduced:
   the inner `sh` survived bwrap's SIGKILL; the measured tool wrote 6 files after the counter died. Smallest
   remediation: `--die-with-parent` on bwrap, and kill the arm A session in a `finally`/signal handler.
4. **MED — scratch containment is lexical and lane-only, and the refusal path leaks.** `count-c1.py:225-229`.
   A symlinked `--scratch` was accepted and a full clone tree materialised inside the `--hide` path
   (`c1-la0f_9m8` with `c0, c1, relocated.out, tmpA, tmpB, tool-at-rev`, rc 2); a scratch in the fleet root
   or `~/.local/bin` is accepted; the `mkdtemp` at `:225` runs before the check and the refusal at `:229`
   leaves `mori-r51-c1-thk6lffv` behind. Smallest remediation: compare `os.path.realpath` on both sides,
   check the base only after it exists, refuse PATH directories and the fleet root, and remove the base on
   the refusal path.
5. **MED — unbounded file write and unbounded capture of the measured tool's stdout.** `count-c1.py:70`,
   `:142-145` (and `:198` for arm D). `relocated.out` was 16,777,218 bytes for a 16 MiB fixture print; the
   same bytes are held in memory first; the host-rw process has a 3000 s budget and the counter never calls
   the disk guard. Smallest remediation: cap the captured output (stream to a bounded file, stop at N MiB)
   and check free space before the bwrap arm.
6. **MED — a nonexistent `--hide` gives a vacuous green `relocated` and makes the counter mkdir on the
   host.** `count-c1.py:140` (`--tmpfs` creates the mount point through the rw bind), `:146-147` (the only
   check is that `<hide>/SKILL.md` is absent *inside*). Demonstrated: `relocated=met` with a fixture printing
   `PIN_CHECK=met`, the hide path created empty on the host, setup probe not tripped. Smallest
   remediation: require `os.path.isdir(hide)` and snapshot `<hide>/SKILL.md`'s existence before bwrap, and
   assert it was visible outside first.
7. **MED — cleanup only on the in-process exception path.** `count-c1.py:258-262`: SIGKILL/SIGTERM/SIGHUP
   skip `finally`; SIGKILLed run left `c1-3plpqoou` (clone + tmpA) in scratch. Smallest remediation: install
   SIGTERM/SIGHUP handlers that set a flag and let `finally` run, and record the scratch path in the output
   line so a killed run's leftovers are findable.
8. **LOW — `killpg` after `poll()` may target a reused pgid; `proc.wait()` has no timeout.**
   `count-c1.py:111-124`. Smallest remediation: only `killpg` when `proc.poll() is None`, and `wait(timeout=…)`
   with a second `killpg` on expiry.
9. **LOW — `os.makedirs(base)` / `mkdtemp(dir=base)` sit outside the `try` and outside the documented
   exit codes.** `count-c1.py:230-231`: an OSError there exits with a traceback (rc 1) instead of
   `C1_SETUP`/rc 2 and leaves the base behind.
10. **LOW — `controls/c1-controls.py` has no cleanup and no resource cap.** `:48-49`, `:76-90`: `K` and the
    six `s-<name>` scratch dirs are never removed (observed `K` left on failure), six counters run
    concurrently (≈1.2 GB of `--no-local` lane clones each, no disk-guard call), receipts are written
    unbounded, `p.wait()` has no timeout, and a `Popen` failure after `open` leaks the receipt fd and leaves
    an `exit=`-less receipt. Smallest remediation: `try/finally` around the whole driver with `rmtree` of
    `K`/`s-*`, sequential or capped concurrency, and a timeout on `p.wait()`.
