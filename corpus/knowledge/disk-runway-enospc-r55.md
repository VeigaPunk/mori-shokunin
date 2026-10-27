# Disk-runway ENOSPC beyond block-only readings (XFS, btrfs, tmpfs)

source: S535 S536 S537 S538 S539 S540 S541 S542 S543
verified-at: 2026-10-27
recheck: on-release — re-open kernel v7.3 statfs implementations, the pinned man-pages 6.19 interface and coreutils 9.12 df documentation; compare the host's statfs/df -P/df -i readings without changing mounts.

## Claim table

| claim | source | quote |
|---|---|---|
| The generic Linux errno header assigns 28 to ENOSPC and labels it “No space left on device,” giving the error name and documented message rather than diagnosing the failed operation | S535 | `#define ENOSPC 28 /* No space left on device */` |
| Before the filesystem's own statfs handler runs, the VFS clears the whole reply buffer, so any field a filesystem never sets reaches userspace as zero | S536 | `memset(buf, 0, sizeof(*buf)); retval = security_sb_statfs(dentry);` |
| When a filesystem leaves the fragment size unset, the VFS fills it with the block size, so block counts on such filesystems are expressed in block-size units | S536 | `if (retval == 0 && buf->f_frsize == 0) buf->f_frsize = buf->f_bsize;` |
| A statfs reply carries two different free-block figures: the plain free count, and a second count limited to what an unprivileged process may still use | S541 | `fsblkcnt_t f_bfree; /* Free blocks in filesystem */ fsblkcnt_t f_bavail; /* Free blocks available to` |
| Inode capacity is reported beside block capacity in the same statfs reply, as a separate pair of total and free counts that a block-only reading ignores | S541 | `fsfilcnt_t f_files; /* Total inodes in filesystem */ fsfilcnt_t f_ffree; /* Free inodes in filesystem */` |
| Linux offers no unprivileged-only inode figure distinct from the plain one: the statvfs field meant for ordinary users always equals the total free inodes | S542 | `Under Linux, .I f_favail is always the same as .IR f_ffree , and there's no way for a filesystem to report otherwise.` |
| The manual justifies that equality by stating that no filesystem keeps inodes back for the superuser, so one free-inode reading serves every caller | S542 | `This is not an issue, since no filesystems with an inode root reservation exist.` |
| The df command shows inode counts only when asked for them, and that mode replaces the block columns rather than adding to them in the same listing | S543 | `List inode usage information instead of block usage.` |
| The XFS statfs handler explicitly assigns its available-block field to the same value as its reported free-block field | S537 | `* XFS does not distinguish between blocks available to privileged and * unprivileged users. */ st->f_bavail = st->f_bfree; return 0;` |
| XFS subtracts an internally unavailable amount from its free-block counter before reporting free space, and clamps that result so it can never fall below zero | S537 | `st->f_bfree = max(0LL, fdblocks - xfs_freecounter_unavailable(mp, XC_FREE_BLOCKS));` |
| XFS computes its reported inode total as inodes already allocated plus how many more the current free blocks could hold, so that total moves with free space | S537 | `uint64_t fakeinos = XFS_FSB_TO_INO(mp, st->f_bfree); st->f_files = min(icount + fakeinos, (uint64_t)XFS_MAXINUMBER);` |
| When an XFS mount has a maximum inode count configured, the reported inode total is additionally capped by that maximum before free inodes are derived | S537 | `if (M_IGEO(mp)->maxicount) st->f_files = min_t(typeof(st->f_files), st->f_files,` |
| Btrfs treats its global block reserve as already consumed when computing free blocks, so the reported free figure sits below raw unallocated capacity by that reserve | S538 | `Account global block reserve as used, it's in logical size already` |
| Btrfs deliberately reports zero available space once its metadata profile can take no further chunk allocations, a condition about metadata rather than file data | S538 | `* We only want to claim there's no available space if we can no longer * allocate chunks for our metadata profile` |
| That zero-available rule also requires the global block reserve not to fit in the remaining free metadata space | S538 | `* allocate chunks for our metadata profile and our global reserve will * not fit in the free metadata space.` |
| The metadata exhaustion test compares remaining metadata room against a fixed four-megabyte threshold, chosen because the gap observed in practice was about two megabytes | S538 | `delta to a 4M threshold. (Practically observed delta was ~2M.)` |
| A btrfs Avail of zero therefore does not guarantee that every write fails: small metadata-consuming operations can still succeed after statfs reports nothing available | S538 | `succeed even if the Avail is zero. But this is better than the other` |
| Btrfs exports each space type's allocated chunk total and the bytes used inside it as separate sysfs counters, alongside pinned, reserved and may-use figures | S539 | `SPACE_INFO_ATTR(total_bytes); SPACE_INFO_ATTR(bytes_used); SPACE_INFO_ATTR(bytes_pinned); SPACE_INFO_ATTR(bytes_reserved); SPACE_INFO_ATTR(bytes_may_use); SPACE_INFO_ATTR(bytes_readonly);` |
| The size of the btrfs global block reserve is published as an attribute of the allocation directory, read from the reserve under its own lock | S539 | `return btrfs_show_u64(&block_rsv->size, &block_rsv->lock, buf); } BTRFS_ATTR(allocation, global_rsv_size, global_rsv_size_show);` |
| A tmpfs instance carries an inode ceiling of its own, set through a mount option that is separate from the instance's size limit | S540 | `nr_inodes The maximum number of inodes for this instance. The default` |
| On a tmpfs with an inode limit, extended attributes draw on that same allowance, so inode usage can grow without any new file being created | S540 | `extended attributes: "df -i"'s IUsed and IUse% increase, IFree decreases.` |
| Setting the tmpfs inode option to zero removes the inode ceiling entirely, an option the documentation itself describes as generally unwise to mount with | S540 | `if nr_inodes=0, inodes will not be limited. It is generally unwise to mount with such options,` |
| A tmpfs mounted without any size option may grow to half of physical memory, so its block runway is bounded by RAM rather than by a disk device | S540 | `the default, when neither size nor nr_blocks is specified, is size=50%` |

## Scope and decision table

Detection and reporting only. ENOSPC is a write failure; it is not a diagnosis by itself. Compare block availability and inode availability separately, then consult filesystem-specific accounting.

| observation | interpretation | read-only next observation |
|---|---|---|
| XFS `df -P` Avail approaches zero | unprivileged block runway is exhausted; XFS statfs equates f_bavail and f_bfree, after internal unavailable blocks are removed | compare `df -i`; inode pressure is a separate count |
| XFS `df -i` IFree approaches zero while Avail remains | inode allocation is the limiting runway; XFS reports an inode total derived partly from remaining free blocks and its configured ceiling | record block and inode columns independently |
| btrfs reports low/zero Avail with nonzero ordinary free blocks | metadata chunk availability/global reserve may be limiting; btrfs applies a heuristic zero-Avail threshold, and some small operations can still succeed | read `/sys/fs/btrfs/<uuid>/allocation/{data,metadata,system}/{total_bytes,bytes_used,bytes_pinned,bytes_reserved,bytes_may_use}` and `global_rsv_size`; do not treat zero Avail as proof every operation fails |
| tmpfs Avail or IFree falls | tmpfs has RAM-backed block limit and a separate inode limit; extended attributes consume the inode allowance | inspect `findmnt` options (`size=`, `nr_inodes=`) and `df -P` plus `df -i` |
| btrfs `df -i` reports zero total/free inode values | btrfs does not supply a fixed inode capacity in the observed statfs result; zero is not evidence of inode exhaustion | classify inode metric unavailable for this filesystem, use btrfs allocation counters for block/metadata runway |
| block runway and inode runway remain, but a write fails | ENOSPC may be from a filesystem-specific resource/quota/metadata path; this entry does not diagnose quota failures | capture the exact errno and filesystem-specific read-only status; EDQUOT is distinct and is covered by `quota-observability-r48.md` |

## On this host

Read-only snapshot 2026-10-27 on Linux 7.2.11-arch1-1: `/tmp` and `/fast` are XFS; `/` and the fleet checkout are btrfs; `/dev/shm` and `/run/user/1000` are tmpfs. `stat -f` on `/tmp` reports f_bfree=f_bavail=32,795,798 blocks and f_files=67,108,864/f_ffree=67,005,211; `/fast` reports f_bfree=f_bavail=147,466,003, f_files=421,271,552/f_ffree=417,090,444. `/` reports f_bfree=164,023,017, f_bavail=154,680,289, f_files=f_ffree=0. `df -P` showed 3% /tmp, 30% /fast and 34% root; `df -i` showed 1% XFS inode use and no btrfs inode count. `/dev/shm` tmpfs has 8 GiB size and 3,965,092 free inodes. Btrfs sysfs metadata total_bytes=61,203,283,968 and bytes_used=41,834,954,752; global_rsv_size=536,870,912. These are point-in-time observations, not an ENOSPC reproduction.

## Boundaries

No writes, mount changes, cache drops, filesystem repair or quota operations. This is source-backed interpretation plus a read-only host snapshot; it adds no probe or live ENOSPC reproduction. btrfs zero-Avail is an estimate/guard, not a universal write-failure prediction. tmpfs is memory-backed and can induce memory pressure; no sizing recommendation is made.

### Captured host snapshot (2026-10-27)

The immediately reproducible point-in-time values are captured at `.ufo/waves/round-55/evidence/host-disk-snapshot.txt` by `stat -f -c 'type=%T bsize=%S blocks=%b bfree=%f bavail=%a files=%c ffree=%d' /tmp /fast / /home/vgpnk/Projects/shokunin /dev/shm /run/user/1000`, `df -P /tmp /fast / /dev/shm`, `df -i /tmp /fast /dev/shm /`, and `cat /sys/fs/btrfs/<uuid>/allocation/{data,metadata,system}/{total_bytes,bytes_used}` plus `global_rsv_{size,reserved}`. `stat -f` returned `/tmp` XFS, blocks 33,529,345, free/available 32,795,553, files 67,108,864, free inodes 67,004,121; `/fast` XFS, blocks 210,532,927, free/available 155,927,507, files 421,271,552, free inodes 418,617,687; `/` btrfs, blocks 243,661,568, free 164,012,985, available 154,665,001, files/free inodes 0/0; `/dev/shm` tmpfs, blocks 2,097,152, free/available 2,096,303, files 3,965,224, free inodes 3,965,173. `df -P` showed 3% `/tmp`, 26% `/fast`, 34% root and 1% `/dev/shm`; `df -i` showed 1% XFS/tmpfs inode use and no btrfs inode count. Btrfs data total/used: 277,033,779,200 / 242,055,213,056 bytes; metadata 61,203,283,968 / 41,824,190,464; system 33,554,432 / 65,536; `global_rsv_size` and `global_rsv_reserved` both 536,870,912. This later read supersedes the earlier same-day sample above for repeatable evidence; both are point-in-time readings and neither reproduces ENOSPC.
