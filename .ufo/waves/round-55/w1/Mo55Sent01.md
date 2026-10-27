# Mo55Sent01 — sentinel: implicit write/recovery advice and privilege assumptions in the C2 table

Surface: `corpus/knowledge/disk-runway-enospc-r55.md` at the measured data revision `b8b7064c2b54c8b6b22c288232a96c43fae1af47`
(read via `git show b8b7064c:corpus/knowledge/disk-runway-enospc-r55.md`, lane repo
`/home/vgpnk/Projects/shokunin/mori-shokunin`). Frozen predicate read from `.ufo/waves/round-55/count-c2.py:1-45`.
Role: detection-only sentinel. No production edits, no git/jj mutation, no votes emitted (this seat is not on the
frozen C2 voter list, so no vote line of any kind appears in this report).

## 1. Axis and method

Axes named before data: (a) does the entry, read literally by an operator under disk pressure, induce any write,
repair, mount-option or escalation action; (b) does any row assume a privilege level that a read-only unprivileged
reader does not have; (c) is every privilege-relevant statement in the table distinguishable from a statement about
the *reported field* only.

Method: read the frozen entry and its decision table; read the pinned source copies for XFS/btrfs privilege-relevant
code; re-ran the table's own "read-only next observation" recipes verbatim as uid 1000 (1000/vgpnk); compared the
entry's prose against its committed receipt `.ufo/waves/round-55/evidence/host-disk-snapshot.txt`.

Disk guard checked first: `/fast/scratch/hyaku` 26% used, 594.6G free, `/var/tmp` 589.9G free, `/tmp` 125.1G free — no
ENOSPC condition; work proceeded, no installs (pacman not invoked), no host changes.

## 2. Commands, output, exit codes

Reproducing the tmpfs row's documented observation recipe (row 44 of the entry, verbatim argument list):

```
$ findmnt -n -o TARGET,FSTYPE,OPTIONS /tmp /fast / /dev/shm
EXIT=1
```
Zero stdout rows. The committed receipt records the same failure and no rows:
`.ufo/waves/round-55/evidence/host-disk-snapshot.txt:24-25` (`$ findmnt -n -o TARGET,FSTYPE,OPTIONS /tmp /fast / /dev/shm`
then `exit=1`).

Per-target form succeeds:

```
$ for t in /tmp /fast / /dev/shm; do findmnt -n -o TARGET,FSTYPE,OPTIONS "$t"; echo "$t EXIT=$?"; done
/tmp xfs rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota
/tmp EXIT=0
/fast xfs rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota
/fast EXIT=0
/ btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@
/ EXIT=0
/dev/shm tmpfs rw,nosuid,nodev,size=8388608k,inode64,huge=advise,usrquota
/dev/shm EXIT=0
$ findmnt -n -o TARGET,FSTYPE,OPTIONS --mountpoint /dev/shm
/dev/shm tmpfs rw,nosuid,nodev,size=8388608k,inode64,huge=advise,usrquota
EXIT=0
```

btrfs sysfs counters named by row 43, read as uid 1000 (the recipe's six paths plus the reserve size):

```
$ cat /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/allocation/{data,metadata,system}/{total_bytes,bytes_used}
277033779200
242206216192
61203283968
41825992704
33554432
65536
EXIT=0
$ ls -l .../allocation/global_rsv_size .../allocation/data/total_bytes .../allocation/system/total_bytes
-r--r--r-- 1 root root 4096 ... global_rsv_size
-r--r--r-- 1 root root 4096 ... data/total_bytes
-r--r--r-- 1 root root 4096 ... system/total_bytes
$ cat /sys/fs/btrfs/*/allocation/global_rsv_size     -> 536870912 (also prints one error line for
                                                        /sys/fs/btrfs/features/allocation/global_rsv_size, absent)
```

Privilege probe for quota state (`quota -u vgpnk`, `repquota /dev/shm`): both commands absent from the host
(`error: command not found`). Whether a per-user limit is *set* on `/dev/shm` is therefore unverified; the mount
option `usrquota` itself is verified above.

## 3. Negative results (assurance, not gaps)

- No write or recovery instruction exists in the decision table. All six rows of
  `disk-runway-enospc-r55.md:41-46` put a read-only verb first in the third column: compare / record / read / inspect /
  classify / capture. Row 46 ends at "capture the exact errno" and explicitly declines diagnosis. Boundaries line 54
  states "No writes, mount changes, cache drops, filesystem repair or quota operations", and repeats that no sizing
  recommendation is made.
- No privileged read is assumed. Every counter the row-43 recipe names (`total_bytes`, `bytes_used`, `bytes_pinned`,
  `bytes_reserved`, `bytes_may_use`, `bytes_readonly`, `global_rsv_size`) is `-r--r--r--` and succeeded at uid 1000.
  The same directory holds root-writable knobs (`bg_reclaim_threshold`, `chunk_size`, `dynamic_reclaim`,
  `periodic_reclaim`, mode 0644) that the table does not name; a non-root reader cannot write them and line 54 forbids
  it, so no write path is implied.
- The only privilege-relevant near-advice in a claim is `nr_inodes=0` (entry line 32): the claim retains the upstream
  warning "generally unwise", so it reads as a hazard note, not a recommendation. Read-only axis unchanged.

## 4. Gaps

### F1 — documented tmpfs observation is a false-negative recipe (MEDIUM)

Exploit path: an operator under write pressure follows row 44 literally — "inspect `findmnt` options (`size=`,
`nr_inodes=`)" — runs `findmnt -n -o TARGET,FSTYPE,OPTIONS /tmp /fast / /dev/shm`, gets no output and exit 1, and
records "no explicit tmpfs size/inode options". The truth on this host is `size=8388608k` on `/dev/shm`. Because an
empty result is indistinguishable from a clean result at a glance, the recipe can *confirm* the wrong hypothesis, and
the receipt carries the same failure with no note: the evidence file records `exit=1` at
`.ufo/waves/round-55/evidence/host-disk-snapshot.txt:24-25`, while the entry's reproducibility sentence (line 58) lists
only `stat -f`, `df -P`, `df -i` and the sysfs `cat`, silently dropping the failing `findmnt`. Evidence:
`disk-runway-enospc-r55.md:44` (recipe), `:58` (omitted command), `evidence/host-disk-snapshot.txt:24-25` (failure).
Impact: a detection lane whose stated next observation cannot run as written; the tmpfs branch of the decision table is
unexecutable on the very host it documents.
Smallest remediation: replace the multi-target invocation with a per-mount form (`findmnt -n -o TARGET,FSTYPE,OPTIONS
<one-mount>` or `--mountpoint <dir>`) and cite the recorded exit code in line 58's command list rather than omitting it.

### F2 — tmpfs row omits the per-user quota limit present on the observed mount (MEDIUM-LOW)

Exploit path: `/dev/shm` is mounted `...,size=8388608k,inode64,huge=advise,usrquota` (verified). With accounting and
enforcement enabled, an unprivileged writer can fail with EDQUOT while `df -P` and `df -i` on that mount both look
healthy — the exact "columns fine, write fails" case. Row 44 describes only two limits (RAM-backed blocks, inode
ceiling) and names only `size=` and `nr_inodes=` as the things to inspect, so the recipe would not surface `usrquota`.
Row 46 covers EDQUOT generically and defers to `quota-observability-r48.md` (verified present; `:30-31` states XFS never
enforces limits on the superuser and that a user at the hard limit sees EDQUOT), so the entry is not wrong — it is
incomplete on the one host mount where a per-user limit can fire. `/tmp` and `/fast` verify as `noquota`, which the
entry never records. Evidence: `disk-runway-enospc-r55.md:44`, `:46`, `:50` (no mount options captured);
`evidence/host-disk-snapshot.txt:24-25` (the only options source, and it fails).
Impact: an unprivileged EDQUOT on `/dev/shm` is attributed to block/inode runway or to a generic "filesystem-specific
resource" instead of to the observed per-user quota.
Smallest remediation: in row 44 add the mount's quota option (`usrquota`/`usrquota,grpquota`/`prjquota`) to the list to
inspect, and note in "On this host" that `/dev/shm` carries `usrquota` (limit value unverified here — `quota` and
`repquota` are not installed on this host).

### F3 — XFS statfs is project-quota scoped, so Avail is not a caller-invariant unprivileged runway (MEDIUM-LOW)

Exploit path: on an XFS mount with project quota enforced, an operator sees `df -P` Avail collapse for one project
directory and reads row 41 ("unprivileged block runway is exhausted"; "XFS statfs equates f_bavail and f_bfree, after
internal unavailable blocks are removed"). The row then sends them to `df -i`, and the generic row-46 escape hatch sends
them hunting for a "filesystem-specific resource" — while the actual mechanism sits inside XFS's own statfs:
`xfs_fs_statfs` calls `xfs_qm_statvfs(ip, st)` when the stat'ed inode is project-inheriting *and* both
`XFS_PQUOTA_ACCT` and `XFS_PQUOTA_ENFD` are set (`sources-r55/xfs_super.c.v7.3:993-996`), and only after that call does
`st->f_bavail = st->f_bfree;` run (`:999-1002`). The reply therefore depends on which path is stat'ed and on the
project's remaining allowance, not on the caller's privilege: two unprivileged users in different projects can read
different Avail values on the same mount, and the failing write returns EDQUOT from the accounting/enforcement path
rather than ENOSPC. The kernel comment claim 9 quotes ("XFS does not distinguish between blocks available to privileged
and unprivileged users") scopes only the post-adjustment assignment, so the table's use of it to justify a single global
unprivileged runway is wider than the code.
Impact: Avail near zero on a pquota XFS mount is misattributed to physical exhaustion — the escalation F4 warns about —
and `df -P` readings become non-comparable across paths and hosts.
On this host the branch cannot fire: `/tmp` and `/fast` both carry the `noquota` option (verified, section 2), and the
entry records no mount options at all (F2). The defect is in the table's generic wording.
Smallest remediation: add a clause to row 41's interpretation — with `prjquota` enforced, Avail is path/project-scoped
and a small value is quota-limited (EDQUOT), which row 46 already defers to `quota-observability-r48.md`.
Label: call site, ordering and mount flags are grounded in the pinned copy; that `xfs_qm_statvfs` reduces the figures to
the project's remaining blocks is [INFERENCE] because its body is not part of S537's copy.

### F4 — XFS reserve is subtracted before reporting, but the table never says a privileged metadata reserve still exists (LOW, partly inference)

Evidence: claim 20 quotes `st->f_bfree = max(0LL, fdblocks - xfs_freecounter_unavailable(mp, XC_FREE_BLOCKS));`
(`sources-r55/xfs_super.c.v7.3:919-920`), `st->f_bavail = st->f_bfree;` (`:1002`), and the per-AG reserve machinery
`xfs_save_resvblks`/`xfs_restore_resvblks` → `xfs_reserve_blocks(mp, i, resblks)` with
`resblks = xfs_default_resblks(mp, i)` (`:1007-1031`). Claim 9's quote is the kernel comment "XFS does not distinguish
between blocks available to privileged and unprivileged users", which is a statement about the two *reported fields*,
not about whether a reserve exists.
Exploit path: an operator reads claim 9 plus row 41 ("unprivileged block runway is exhausted") and concludes the
filesystem has no privileged headroom at all, then escalates to repair/grow on a mount that is merely out of user-data
runway. The entry's Boundaries (line 54) forbids repair, so the residual risk is an inference, not an instruction.
Impact: escalation to a destructive filesystem action on the strength of `df -P` Avail = 0.
Smallest remediation: one clause in row 41 — the reported free figure already excludes the filesystem's internal
reserve (claim 20), so Avail = 0 means the *user-data* runway is exhausted while metadata allocations can still draw on
the reserve.
Label: the body of `xfs_freecounter_unavailable` is not in the pinned copy, so "the reserve is inside that
unavailable set" is [INFERENCE]; what is grounded is that a reserve exists, is re-established at mount, and is
subtracted before the reported figure.

### F5 — two host samples, one receipt; the receipt's own scope is wider than the reported values (LOW)

Entry line 50 presents f_bfree=f_bavail=32,795,798, `/fast` 147,466,003 and `/dev/shm` 3,965,092 free inodes; the
committed receipt reports 32,795,553 / 155,927,507 / 3,965,173 (`evidence/host-disk-snapshot.txt:3,4,7`). Line 58 labels
the later read as superseding, so the earlier sample is not presented as receipted — but the `/fast` difference alone is
8,461,504 blocks (~32.3 GiB) within the same day with no cause cited, and line 58 says the values come from a command
list that also measured `/home/vgpnk/Projects/shokunin` and `/run/user/1000` (both present in the receipt, `:6` and `:8`)
without reporting either. Impact: numbers in the prose cannot all be traced to a receipt; a recheck cannot tell which
sample a quoted figure belongs to. Smallest remediation: label line 50's figures as an uncaptured earlier sample, or
drop them, and either report or stop claiming the two extra mounts.

### F6 — informational: `<uuid>` placeholder is load-bearing (INFO)

`/sys/fs/btrfs/*/allocation/...` expands `*` onto `/sys/fs/btrfs/features` as well, which has no `allocation`
directory, producing `cat: .../features/allocation/...: No such file or directory` before the real values. The entry
correctly writes `<uuid>`; recording why the glob form is unsafe keeps a copy-pasting reader from treating the error as
a broken counter. No action required beyond a parenthetical.

## 5. Verification status

- Verified live at uid 1000 2026-10-27: `findmnt` failure with the documented argument list (exit 1, empty), per-target
  success, `/dev/shm` `usrquota` and `size=8388608k`, XFS `noquota` on `/tmp` and `/fast`, sysfs counter modes 0444 and
  readability, the six-path sysfs recipe exit 0.
- Verified from frozen copies at `b8b7064c`: entry text and decision table, XFS statfs project-quota branch and
  reserve/statfs code lines, tmpfs
  documentation quotes (`nr_inodes`, `size=50%`, `nr_inodes=0`, xattr/`df -i` paragraph present at
  `sources-r55/tmpfs.rst.v7.3:83,92,95,100-101`), quota cross-reference existence and content.
- Not verified: whether a quota limit value is set on `/dev/shm` (`quota`/`repquota` not installed; no install made, per
  seat authorization), and the internals of `xfs_freecounter_unavailable` (not in the pinned copy). Both marked above.
- No vote lines emitted by this seat. No production file touched; scratch `/fast/scratch/hyaku/mori-r55/Mo55Sent01`
  removed before yield.

## Findings

| id | severity | finding | evidence |
|---|---|---|---|
| F1 | MEDIUM | row 44's tmpfs "read-only next observation" is the multi-target `findmnt` form, which exits 1 with no output; the receipt records that failure while the entry's command list drops it, so empty output can be read as "no `size=`/`nr_inodes=` set" when `/dev/shm` has `size=8388608k` | `mori-shokunin/corpus/knowledge/disk-runway-enospc-r55.md:44,58`; `mori-shokunin/.ufo/waves/round-55/evidence/host-disk-snapshot.txt:24-25`; live repro exit 1 |
| F2 | MEDIUM-LOW | tmpfs row names only `size=`/`nr_inodes=`, omitting the `usrquota` option present on the observed `/dev/shm`; a per-user hard limit yields EDQUOT while both df columns are healthy, and the entry records no mount options for any observed mount (`/tmp`, `/fast` verify as `noquota`) | `disk-runway-enospc-r55.md:44,46,50`; live `findmnt /dev/shm` |
| F3 | MEDIUM-LOW | the table treats XFS `df -P` Avail as one caller-invariant unprivileged runway, but `xfs_fs_statfs` adjusts the reply through `xfs_qm_statvfs` for project-inheriting inodes when project accounting+enforcement are on, before `f_bavail = f_bfree`, so Avail is path/project-scoped and a small value there means EDQUOT, not physical exhaustion | `sources-r55/xfs_super.c.v7.3:993-1002`; `disk-runway-enospc-r55.md:19,41,46`; live `findmnt` shows `noquota` on `/tmp` and `/fast` |
| F4 | LOW | claim 9 (field-level "XFS does not distinguish between blocks available to privileged and unprivileged") plus row 41 never state that the reported free figure already excludes the filesystem's internal reserve, so Avail=0 can be misread as "no headroom at all" and escalate to repair (guarded only by Boundaries line 54) | `sources-r55/xfs_super.c.v7.3:919-920,1002,1007-1031`; `disk-runway-enospc-r55.md:19,20,41,54` |
| F5 | LOW | two same-day host samples, one receipted; prose figures (32,795,798 / 147,466,003 / 3,965,092) are absent from the receipt (32,795,553 / 155,927,507 / 3,965,173), `/fast` differs by ~32.3 GiB with no cited cause, and two measured mounts are not reported | `disk-runway-enospc-r55.md:50,58`; `evidence/host-disk-snapshot.txt:3,4,7` |
| F6 | INFO | `<uuid>` must stay literal; a `*` glob also matches `/sys/fs/btrfs/features` and emits misleading errors before the real counters | live `cat /sys/fs/btrfs/*/allocation/global_rsv_size` |

Assurance (no defect): the decision table contains no write, recovery, mount-change or escalation instruction (all six
next-observation cells are read-only verbs; Boundaries line 54 excludes writes, cache drops, repair and quota ops), and
every sysfs counter the table names is world-readable 0444 and was read successfully as uid 1000.
