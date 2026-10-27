# Mo55Exec04 — read-only host reproduction of the C2 disk-runway snapshot

Seat scope: reproduce the host facts behind C2's "On this host" material (`df -P`, `df -i`, `stat -f`,
btrfs sysfs allocation counters) read-only and compare them to the landed C2 entry. No source edits, no
host mutation, no ENOSPC/EDQUOT forcing, no mount/sysctl/cgroup writes. This is a falsification seat, not a
C2 entailment voter and not a C1 reviewer, so **this report emits no vote line of any kind** (none of the
four C1/C2 vote verbs appears here, at line start or elsewhere).

Lane: `mori-shokunin` at `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scratch (created, used, removed before yield): `/fast/scratch/hyaku/mori-r55/Mo55Exec04/`.
No git/jj mutation was performed; `git status --porcelain` was read only.

## 0. Pre-flight

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
/tmp                               3%   125.1G
/var/tmp                           34%   589.9G
/fast/scratch/hyaku               27%   594.2G
exit=0
```
No ENOSPC condition. Guard `status` exits 0; heavy work proceeded.

Revisions inspected (read-only `git show`/`ls-tree`, no checkout):
- entering tip `ca52426ea496bc6592e3e867cc9d28843e45f196`
- frozen inputs `c9b908f0bb89974f30b927776ce2450ae4198b10`
- data revs `51ebd3d3ff5bfa2cdd532f79d5eb6d9702363072` and the measured `b8b7064c2b54c8b6b22c288232a96c43fae1af47`
- lane HEAD `b8a70adf93ebd9d1e4e95bef8627a220f2fa816b`

Host under test: `uname -r` = `7.2.11-arch1-1`; `df 0.8.0`, `stat 0.8.0`, `findmnt from util-linux 2.42.4`.

## 1. Reproduction transcript (verbatim, all read-only)

```
started=2026-10-27T03:45:07-03:00
host=7.2.11-arch1-1

$ stat -f -c 'type=%T bsize=%S blocks=%b bfree=%f bavail=%a files=%c ffree=%d' /tmp /fast / /home/vgpnk/Projects/shokunin /dev/shm /run/user/1000
type=xfs bsize=4096 blocks=33529345 bfree=32795425 bavail=32795425 files=67108864 ffree=67004118
type=xfs bsize=4096 blocks=210532927 bfree=155100439 bavail=155100439 files=421271552 ffree=418155576
type=btrfs bsize=4096 blocks=243661568 bfree=163972155 bavail=154625075 files=0 ffree=0
type=btrfs bsize=4096 blocks=243661568 bfree=163972155 bavail=154625075 files=0 ffree=0
type=tmpfs bsize=4096 blocks=2097152 bfree=2090355 bavail=2090355 files=3965224 ffree=3965127
type=tmpfs bsize=4096 blocks=793044 bfree=792423 bavail=792423 files=793044 ffree=791551
exit=0

$ df -P /tmp /fast / /dev/shm
Filesystem       1024-blocks      Used Available Capacity Mounted on
/dev/nvme1n1p1     134117380   2935680 131181700       3% /tmp
/dev/nvme1n1p2     842131708 221729952 620401756      27% /fast
/dev/mapper/root   974646272 318757652 618500300      35% /
tmpfs                8388608     27188   8361420       1% /dev/shm
exit=0

$ df -i /tmp /fast /dev/shm /
Filesystem          Inodes   IUsed     IFree IUse% Mounted on
/dev/nvme1n1p1    67108864  104746  67004118    1% /tmp
/dev/nvme1n1p2   421271552 3115976 418155576    1% /fast
tmpfs              3965224      97   3965127    1% /dev/shm
/dev/mapper/root         0       0         0     - /
exit=0

$ findmnt -n -o TARGET,FSTYPE,OPTIONS /tmp /fast / /dev/shm     # the form recorded in the frozen evidence file
exit=1                       # no stdout, no stderr (0 bytes each)

$ findmnt -n -o TARGET,FSTYPE,OPTIONS <one target per call>
/dev/shm tmpfs rw,nosuid,nodev,size=8388608k,inode64,huge=advise,usrquota        exit=0
/run/user/1000 tmpfs rw,nosuid,nodev,relatime,size=3172176k,nr_inodes=793044,mode=700,uid=1000,gid=1000,inode64,huge=advise   exit=0
/tmp xfs rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota         exit=0
/fast xfs rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota        exit=0
/ btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@   exit=0

$ ls /sys/fs/btrfs/<uuid>/allocation/{data,metadata,system}/      uuid=1d02a454-c549-4a35-b567-89d60902af8e
each space dir contains: total_bytes bytes_used bytes_pinned bytes_reserved bytes_may_use bytes_readonly
                        bytes_zone_unusable chunk_size disk_total disk_used flags dynamic_reclaim
                        bg_reclaim_threshold periodic_reclaim reclaim_bytes reclaim_count reclaim_errors
                        size_classes single (data) / dup (metadata,system)
exit=0

$ cat /sys/fs/btrfs/<uuid>/allocation/{data,metadata,system}/{total_bytes,bytes_used,bytes_pinned,bytes_reserved,bytes_may_use,bytes_readonly}
$ cat /sys/fs/btrfs/<uuid>/allocation/global_rsv_{size,reserved}
data/total_bytes=277033779200 exit=0
data/bytes_used=242218749952 exit=0
data/bytes_pinned=0 exit=0
data/bytes_reserved=0 exit=0
data/bytes_may_use=7446528 exit=0
data/bytes_readonly=65536 exit=0
metadata/total_bytes=61203283968 exit=0
metadata/bytes_used=41826041856 exit=0
metadata/bytes_pinned=0 exit=0
metadata/bytes_reserved=98304 exit=0
metadata/bytes_may_use=631635968 exit=0
metadata/bytes_readonly=65536 exit=0
system/total_bytes=33554432 exit=0
system/bytes_used=65536 exit=0
system/bytes_pinned=0 exit=0
system/bytes_reserved=0 exit=0
system/bytes_may_use=0 exit=0
system/bytes_readonly=0 exit=0
global_rsv_size=536870912 exit=0
global_rsv_reserved=536870912 exit=0
```

A second read of the same commands at `03:42:45-03:00` was also taken (earlier values in the scratch
transcript); both reads agree on every structural field.

## 2. Comparison against the landed C2 entry

Target file: `mori-shokunin/corpus/knowledge/disk-runway-enospc-r55.md` at data rev
`b8b7064c2b54c8b6b22c288232a96c43fae1af47` (identical at HEAD `b8a70adf`).
Pinned evidence file: `mori-shokunin/.ufo/waves/round-55/evidence/host-disk-snapshot.txt`
(blob `540b5845b36e40a7a23c6b77fdb0e9dd7b558483`, present at both data rev and HEAD).

### 2a. Structural agreement — every static field reproduces exactly

| mount | fstype | bsize | blocks (total) | files (inode total) | verdict vs frozen evidence |
|---|---|---|---|---|---|
| `/tmp` | xfs | 4096 | 33,529,345 | 67,108,864 | identical |
| `/fast` | xfs | 4096 | 210,532,927 | 421,271,552 | identical |
| `/` | btrfs | 4096 | 243,661,568 | 0 | identical |
| fleet checkout | btrfs | 4096 | 243,661,568 | 0 | identical |
| `/dev/shm` | tmpfs | 4096 | 2,097,152 | 3,965,224 | identical |
| `/run/user/1000` | tmpfs | 4096 | 793,044 | 793,044 | identical |

btrfs uuid `1d02a454-c549-4a35-b567-89d60902af8e` identical; `data/metadata/system total_bytes`
(277,033,779,200 / 61,203,283,968 / 33,554,432) and `global_rsv_size`/`global_rsv_reserved`
(both 536,870,912) are byte-identical between the frozen capture and my read. The filesystem *types*
claimed at entry line 50 (`/tmp` and `/fast` XFS; `/` and the fleet checkout btrfs; `/dev/shm` and
`/run/user/1000` tmpfs) are confirmed by both `stat -f` and per-target `findmnt`.

### 2b. Free/used counters drift — expected, and correctly scoped by the entry

Between the frozen capture (~03:39) and my read (03:45) the free/used counters moved:

| mount | bfree/bavail delta | ffree delta | cause |
|---|---|---|---|
| `/tmp` | −128 blocks (−512 KiB) | −3 | background churn |
| `/fast` | −827,068 blocks (−3.38 GiB) | −462,111 | concurrent lane scratch writes (inode delta `df -i` IUsed 2,653,865 → 3,115,976 matches the ffree delta exactly) |
| `/` | −40,830 blocks (−156 MiB) | 0 | btrfs churn |
| `/dev/shm` | −5,948 blocks | −46 | tmpfs churn |
| `/run/user/1000` | −14 blocks | −208 | tmpfs churn |

`df -P` capacity moved 26% → 27% on `/fast` and 34% → 35% on `/`, driven by the same churn. Every
static field is unchanged. This is exactly the "point-in-time reading" the entry claims, so the drift is
not a defect in the entry; it does mean the entry's numbers are not reproducible as *values* and must be
read as observations.

### 2c. Arithmetic self-consistency — the frozen evidence file verifies exactly

Re-deriving `df -P` from `stat -f` under coreutils semantics (`used = (blocks−bfree)·bsize/1024`,
`avail = bavail·bsize/1024`, `Capacity = ceil(used/(used+avail))`):

| mount | df total | df used | df avail | df capacity | verdict |
|---|---|---|---|---|---|
| `/tmp` | OK | OK | OK | 3% = ceil(2.189%) | consistent |
| `/fast` | OK | OK | OK | 26% = ceil(25.937%) | consistent |
| `/` | OK | OK | OK | 34% = ceil(33.992%) | consistent |
| `/dev/shm` | OK | OK | OK | 1% = ceil(0.040%) | consistent |

`df -i` totals/IFree equal `stat -f` files/ffree for every mount, including btrfs reporting
`0 0 0 -` for `/`. `df` uses `f_bavail` (not `f_bfree`) for its Available column: for XFS and tmpfs
`f_bfree == f_bavail` here, while on btrfs `/` they differ by 9,347,984 blocks (35.66 GiB) — `f_bavail`
is the one `df` prints. The frozen evidence file is internally coherent on every row.

### 2d. Semantic claims the host actually corroborates

- **XFS `f_bavail == f_bfree`** — confirmed on both XFS mounts (`/tmp`, `/fast`) in every read,
  matching entry row 41's premise.
- **btrfs `df -i` reports zero total/free inodes** — confirmed: `/dev/mapper/root 0 0 0 - /`
  (entry row 45). Zero is not evidence of inode exhaustion on btrfs; the entry states this correctly.
- **tmpfs inode ceiling is separate from its size limit** — confirmed on the host and *not* visible in
  the frozen evidence file. `/run/user/1000` is mounted with `nr_inodes=793044` and `stat -f` reports
  `files=793044` (exact match), while `/dev/shm` carries no `nr_inodes` option and reports
  `files=3,965,224`, which equals exactly half of RAM pages (MemTotal 31,721,796 kB → 7,930,449 pages →
  half = 3,965,224) per the pinned tmpfs documentation
  (`corpus/evidence/sources-r55/tmpfs.rst.v7.3:83-86`). Entry row 44's prescription
  ("inspect `findmnt` options (`size=`, `nr_inodes=`) and `df -P` plus `df -i`") is the right one and is
  reproducible — but only with one `findmnt` target per invocation (see 2e).
- **btrfs global reserve is far smaller than the Avail/free gap** — `f_bfree − f_bavail` = 9,347,984
  blocks (35.66 GiB) on `/`, while `global_rsv_size` = 536,870,912 B (131,072 blocks) explains only
  1.40% of that gap; the remaining ~35.16 GiB is metadata space reservation. This is consistent with
  entry rows 43 and 13, and with the entry's own boundary that btrfs zero-Avail is an estimate/guard.

### 2e. Discrepancies found

**D1 (medium) — the frozen evidence file records a `findmnt` invocation that failed silently.**
`.ufo/waves/round-55/evidence/host-disk-snapshot.txt:24-25` records
`$ findmnt -n -o TARGET,FSTYPE,OPTIONS /tmp /fast / /dev/shm` followed by `exit=1` with no output.
`findmnt` accepts a single target; the multi-target form exits 1 with empty stdout and empty stderr.
Reproduced verbatim: `exit=1`, 0 bytes stdout, 0 bytes stderr. Consequence: the frozen evidence file
contains **no** mount-option record, so the tmpfs `size=`/`nr_inodes=` options that entry row 44 tells
the reader to inspect are not evidenced in the captured artifact — only implied by `stat -f` totals. The
entry's "Captured host snapshot" paragraph (line 58) lists the capture commands but does not list
`findmnt` among them, so it does not claim the failed call produced output; the defect is in the
evidence file, not in a C2 claim cell.

**D2 (low) — the entry's first host paragraph is not reproducible and is superseded only implicitly.**
`disk-runway-enospc-r55.md:50` ("On this host") reports `/fast` `f_bfree=f_bavail=147,466,003`,
`f_ffree=417,090,444`, `/` `f_bfree=164,023,017` / `f_bavail=154,680,289`, `/tmp`
`f_bfree=f_bavail=32,795,798` / `f_ffree=67,005,211`, `/dev/shm` `3,965,092` free inodes, btrfs
`metadata bytes_used=41,834,954,752`, and `df -P` `30% /fast`. **None of these eight values appear in
the frozen evidence file**, and none is reproducible now (`/fast` free blocks read 155,100,439; `/fast`
capacity 27%). The later paragraph at line 58 does state "This later read supersedes the earlier
same-day sample above", and the earlier paragraph's own figures are internally self-consistent under df
semantics (its `147,466,003` free blocks imply exactly 30% on `/fast`), so it is a genuine earlier
sample rather than a fabrication. The residual defect is that the entry presents two mutually exclusive
host snapshots in the same file with the supersession only stated eight lines later, and the earlier
paragraph's `/fast` free-space figure (147,466,003) is ~8.46M blocks (32 GiB) below the captured one —
large enough that a reader quoting the first paragraph would be materially wrong about `/fast` runway.
Note this concerns the *prose* host paragraph only; the 23-row C2 claim table (lines 9-35) is
source-quoted and unaffected, and the contract (C2, "The live host snapshot is a read-only observation,
not an ENOSPC reproduction or a counted subclaim") excludes the host snapshot from the counted surface.

**D3 (info) — the host snapshot is not in the freeze manifest.**
`evidence/freeze-sha256.txt` (35 pinned paths) covers the contract, both counters, their control and
selftest code, the scope listing and the nine `corpus/evidence/sources-r55/` copies, but **not**
`evidence/host-disk-snapshot.txt`. The file is committed (blob `540b5845…`, identical at data rev and
HEAD) so it is reproducible by revision, but it is outside the sha256-pinned freeze set that the
contract describes for "the source copies and their pins". Its content is verified here against a live
read anyway (2a–2c).

**D4 (info) — the entry's `/` capacity figure is sensitive to the btrfs reserved gap.**
Entry line 50 says "`df -P` showed ... 34% root" and line 58 repeats 34%; my read gives 35%. The
difference is churn plus df's rounding of `used/(used+avail)`, not a discrepancy in the claim: the
captured file's own `/` row is arithmetically exact (33.992% → 34%). Noted only so a re-reader does not
read the 34%/35% difference as a contradiction.

## 3. Scope discipline

- Host: read-only. No `sysctl`, `mount`, `umount`, `cgroup`, quota, module load, cache drop, repair or
  write of any kind. No ENOSPC/EDQUOT was induced. `stat -f`, `df -P`, `df -i`, `findmnt`,
  `/proc/meminfo`, `/proc/mounts` and `/sys/fs/btrfs/**` reads only.
- Repo: no file written except this report. `git status --porcelain` was read; no `git`/`jj` mutation
  (`commit`, `checkout`, `reset`, `push`) was issued.
- Scratch: `/fast/scratch/hyaku/mori-r55/Mo55Exec04/` created and removed before yield. Nothing was
  written to `/tmp`. No tool installs were performed (no package manager invoked; `/home/vgpnk/.omp/agent/RULES.md`
  install authorization was therefore not needed).
- This seat is not a C2 entailment voter (`Mo55En01`–`Mo55En12` only) and not a C1 reviewer
  (`Mo55Rc01`–`Mo55Rc16` only); it emits no vote line of any kind.

## Findings

- MEDIUM — The frozen host-snapshot evidence records a `findmnt` call that failed silently
  (`exit=1`, no output) because `findmnt` takes one target per invocation, so no mount-option evidence
  (`size=`, `nr_inodes=`) exists in the captured artifact even though entry row 44 prescribes exactly
  that inspection. Evidence: `mori-shokunin/.ufo/waves/round-55/evidence/host-disk-snapshot.txt:24-25`;
  reproduced `exit=1` with 0 bytes stdout and 0 bytes stderr; corrected one-target-per-call form exits 0
  and yields `/dev/shm size=8388608k` (no `nr_inodes`) and `/run/user/1000 size=3172176k,nr_inodes=793044`.
  Also `mori-shokunin/corpus/knowledge/disk-runway-enospc-r55.md:44`.
- LOW — The entry carries two mutually exclusive host snapshots; the first (line 50) reports `/fast`
  `147,466,003` free blocks and `30%` capacity, eight values that appear nowhere in the pinned evidence
  file and are not reproducible (live `/fast` free blocks 155,100,439, capacity 27%). The supersession
  is stated only at line 58, eight lines later. The first paragraph's figures are internally consistent
  under df semantics, so it is an earlier genuine sample, not a fabrication; the risk is a reader quoting
  the earlier `/fast` runway figure. The 23-row C2 claim table and the counted C2 surface are unaffected.
  Evidence: `mori-shokunin/corpus/knowledge/disk-runway-enospc-r55.md:50,56-58`;
  `mori-shokunin/.ufo/waves/round-55/evidence/host-disk-snapshot.txt:1-35`.
- INFO — `evidence/host-disk-snapshot.txt` is committed (blob `540b5845b36e40a7a23c6b77fdb0e9dd7b558483`
  at both `b8b7064c` and HEAD `b8a70adf`) but is not listed in `evidence/freeze-sha256.txt`, so it sits
  outside the sha256-pinned freeze set the contract describes.
  Evidence: `mori-shokunin/.ufo/waves/round-55/evidence/freeze-sha256.txt` (35 paths, no snapshot entry);
  `git ls-tree b8b7064c .ufo/waves/round-55/evidence/host-disk-snapshot.txt`.
- INFO — Every static field of the C2 host material reproduces exactly on this host at `7.2.11-arch1-1`:
  filesystem types, block sizes, total blocks and total inode counts for all six paths, btrfs uuid, the
  three btrfs space `total_bytes`, and `global_rsv_size`/`global_rsv_reserved` (both 536,870,912). Only
  free/used counters drift, by amounts fully explained by concurrent lane scratch writes
  (`/fast` `df -i` IUsed 2,653,865 → 3,115,976 equals the `ffree` delta 462,111 exactly). The frozen
  evidence file is arithmetically self-consistent on every `df -P`/`df -i` row.
  Evidence: `mori-shokunin/.ufo/waves/round-55/evidence/host-disk-snapshot.txt:2-23` versus the
  reproduction transcript in §1 of this report.
- INFO — The host independently corroborates the entry's tmpfs inode-ceiling semantics in a way the
  captured evidence file does not show: `/run/user/1000` `nr_inodes=793044` equals its `stat -f`
  `files=793044` exactly, and `/dev/shm` with no `nr_inodes` option reports `files=3,965,224` = half of
  RAM pages (31,721,796 kB → 7,930,449 pages → 3,965,224), matching
  `corpus/evidence/sources-r55/tmpfs.rst.v7.3:83-86`. btrfs `/` shows `df -i` `0 0 0 -`, confirming
  entry row 45's "zero is not evidence of inode exhaustion". Evidence: reproduction transcript §1;
  `mori-shokunin/corpus/knowledge/disk-runway-enospc-r55.md:44-45`.
