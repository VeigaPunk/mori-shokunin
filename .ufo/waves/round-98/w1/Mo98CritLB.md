# Mo98CritLB — fd-held user namespace vs `used_lb` (critic probe, wave w1 round 98)

Seat: Mo98CritLB (critic) · 2026-11-05 · Scope: falsifiable probe of the 'Lower bound' paragraph of
`corpus/knowledge/userns-runway-r98.md` against `tools/mori-userns-runway.py`. Lane bounds obeyed: no sudo, no
sysctl changes, one unprivileged `unshare -Ur sleep 30`, read-only on the lane except this report file.

## Hypothesis

H: a user namespace kept alive only by an open file descriptor (no process inside it) is NOT counted by
`mori-userns-runway.py` (`used_lb`) although the namespace still exists.

## Method

Python driver: T0 baseline tool read; spawn `unshare -Ur sleep 30`; `os.open('/proc/<pid>/ns/user', O_RDONLY)` fd
kept open; T1 tool read; SIGKILL child + wait; verify ns still exists via `os.fstat(fd).st_ino` and
`ls -l /proc/<driver-pid>/fd`; T2 tool read; `lsns -t user` at T1 and T2. Because sibling seats churn /proc
concurrently, attribution is by direct set membership: the driver independently recomputes the tool's exact
counting logic (distinct non-initial inodes over readable `/proc/<pid>/ns/user` links) and checks membership of the
child inode. Tool: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-userns-runway.py` (no args →
runway read on live /proc).

## Outputs (pass 1)

```
== T0: baseline, nothing spawned yet ==
tool[T0] rc=0 stdout=USERNS_RUNWAY limit=122865 used_lb=6 pids=3451 unreadable=3185 runway=122859 low=32 state=ok stderr=''
my-count[T0] distinct non-initial ns/user inodes=6
== spawn: unshare -Ur sleep 30 ==
child pid=1307663 alive=True
opened fd=3 on /proc/1307663/ns/user: fstat st_ino=4026533827 st_nlink=1 fresh_ns=True
readlink /proc/1307663/ns/user -> user:[4026533827]
readlink /proc/self/fd/3 -> user:[4026533827]
== T1: child alive in its userns, fd held by parent ==
tool[T1] rc=0 stdout=USERNS_RUNWAY limit=122865 used_lb=7 pids=3458 unreadable=3191 runway=122858 low=32 state=ok stderr=''
my-count[T1] distinct non-initial ns/user inodes=7
attribution T1: child_ino=4026533827 in_set=True delta_vs_T0=1
lsns[T1] rc=0 child_ino_listed=True   (row: 4026533827 user  1  1307663 vgpnk sleep 30)
== kill child, wait, fd still held ==
after kill+wait: child_rc=-9 fstat(fd) st_ino=4026533827 same_ino=True -> ns still exists via fd
== T2: no process inside the ns, only our fd holds it ==
tool[T2] rc=0 stdout=USERNS_RUNWAY limit=122865 used_lb=6 pids=3458 unreadable=3191 runway=122859 low=32 state=ok stderr=''
my-count[T2] distinct non-initial ns/user inodes=6
attribution T2: child_ino=4026533827 in_set=False delta_vs_T1=-1 delta_vs_T0=0
lsns[T2] rc=0 child_ino_listed=True   (row: 4026533827 user  0  — empty PID and COMMAND)
```

## Outputs (pass 2 — corrects pass 1's `ls -l /proc/self/fd`, which had run inside the `ls` subprocess and so
listed ls's own fds, not the driver's; parent pid named explicitly here)

```
driver pid=1315590 child pid=1315642 fd=3 ns_ino=4026533827
after kill+wait: child_rc=-9 fstat(fd).st_ino=4026533827 unchanged=True
ls -l /proc/1315590/fd (the driver that holds the fd):
total 0
lrwx------ 1 vgpnk vgpnk 64 Nov  5 18:37 0 -> /dev/null
l-wx------ 1 vgpnk vgpnk 64 Nov  5 18:37 1 -> pipe:[494881680]
l-wx------ 1 vgpnk vgpnk 64 Nov  5 18:37 2 -> pipe:[494881680]
lr-x------ 1 vgpnk vgpnk 64 Nov  5 18:37 3 -> user:[4026533827]
lrwx------ 1 vgpnk vgpnk 64 Nov  5 18:37 36 -> /dev/pts/1
lrwx------ 1 vgpnk vgpnk 64 Nov  5 18:37 38 -> /dev/pts/1
lr-x------ 1 vgpnk vgpnk 64 Nov  5 18:37 4 -> pipe:[495016459]
lr-x------ 1 vgpnk vgpnk 64 Nov  5 18:37 6 -> pipe:[495016460]
lsns rows mentioning 4026533827:
4026533827 user      0         
tool[pass2-after-kill] rc=0 stdout=USERNS_RUNWAY limit=122865 used_lb=6 pids=3474 unreadable=3211 runway=122859 low=32 state=ok
lsns from util-linux 2.42.4
```

## Findings

1. **H holds.** `used_lb` went 6 → 7 (+1, child inode 4026533827 present, child alive) → 6 (−1, child dead, fd
   still open). `os.fstat(fd).st_ino` unchanged and `ls -l` shows fd 3 → `user:[4026533827]` after the child died:
   the namespace exists, is charged against the host's 122865 limit, yet is invisible to the tool. Net vs T0: 0,
   with membership of the exact inode tracked, so background churn (pids 3451→3474, unreadable 3185→3211) does not
   confound attribution.
2. **Knowledge entry wording is accurate.** "Namespaces held only by an open file descriptor or a bind mount have
   no process link" — verified for the fd case exactly as stated; the `used_lb` name is honest (a lower bound), and
   the entry's table row "runway >= low … not proof of room: `used_lb` is a lower bound" is the right reading.
   This is an accepted blind spot of a /proc-link reader, not a defect in the tool or entry.
3. **Contrast a reader should know (informational, not an entry error):** `lsns -t user` (util-linux 2.42.4) still
   lists the fd-held namespace after the child died, with NPROCS=0 and empty PID/COMMAND — while the tool does not
   count it. So `lsns` and `mori-userns-runway.py` can disagree on fd-held namespaces. [INFERENCE] lsns presumably
   scans open-fd holders, but its mechanism is not doc-verified here (`lsns --help` mentions no fd scanning; man
   page check returned nothing on this host).

## Not run (named unrun)

- Bind-mount-held namespace case (entry mentions it alongside fds) — unrun.
- Other-users/unreadable-link behavior and per-user charge claims (S629 claims 3–4) — unrun here.
- Journal-scan paths (`--journal`, SYSCTL_WRITE classification) — unrun here.

## Cleanup

Scratch `/fast/scratch/hyaku/mori-r98/Mo98CritLB` (driver scripts + outputs) removed after this report was written.
No other host, lane, or fleet state touched.
