source: S479 — https://man7.org/linux/man-pages/man8/xfs_quota.8.html — §QUOTA OVERVIEW, §QUOTA ADMINISTRATION items 3, 8, 9, §USER COMMANDS `quot`; xfsprogs-dev.git 2026-08-04, HTML 2026-09-09
source: S480 — https://man7.org/linux/man-pages/man2/quotactl.2.html — §DESCRIPTION, §ERRORS ESRCH, §NOTES `quotactl_fd`; man-pages 6.19 (2026-06-05)
source: S481 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h — line 107; tag v7.2
source: S482 — https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes — 验证目录配额限制; page meta last-modified 2026-10-13
source: S483 — https://raw.githubusercontent.com/torvalds/linux/v7.2/arch/mips/include/uapi/asm/errno.h — line 131; tag v7.2 (boundary, not in the claims table)
source: S484 — https://raw.githubusercontent.com/torvalds/linux/v7.2/arch/sparc/include/uapi/asm/errno.h — line 43; tag v7.2 (boundary, not in the claims table)
verified-at: 2026-10-25
recheck: 180d — `curl -fsSL 'https://man7.org/linux/man-pages/man8/xfs_quota.8.html' | grep -c 'Quota exceeded'` -> 1 (ran 2026-10-25)
recheck: 180d — `curl -fsSL 'https://man7.org/linux/man-pages/man2/quotactl.2.html' | grep -c 'No disk quota is found for the indicated user'` -> 1 (ran 2026-10-25)
recheck: on-release — `curl -fsSL 'https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h' | grep -cE 'EDQUOT[[:space:]]+122'` -> 1 (ran 2026-10-25)
recheck: on-release — `for a in mips sparc; do curl -fsSL "https://raw.githubusercontent.com/torvalds/linux/v7.2/arch/$a/include/uapi/asm/errno.h" | grep -E 'EDQUOT'; done` -> mips 1133, sparc 69 (ran 2026-10-25)
recheck: 180d — `curl -fsSL -A 'Mozilla/5.0' 'https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes' | grep -c 'Disk quota exceeded'` -> 1 or more (ran 2026-10-25; the page body is also embedded as JSON, so the count varies with the rendering)
coverage-map: FR2

# Quota exhaustion is a per-id state with its own error and its own counters; `df` cannot see it

## Claims

Each row is one fact a probe author can act on. The quote is copied from the committed copy of the source
under `corpus/evidence/sources-r48/` (tags stripped, entities decoded, whitespace collapsed); the counter
`.ufo/waves/round-48/count-c2.py` proves the quote is located there, not that the claim follows from it —
that is the reviewer's check (`corpus/lessons/round-48.md` Gate).

| claim | source | quote |
|---|---|---|
| On XFS, quota accounting and limit enforcement are separate states; a mount can account without enforcing. | S479 | `XFS distinguishes between quota accounting and limit enforcement.` |
| Accounting is chosen at mount time, while enforcement can be switched afterwards. | S479 | `Quota accounting must be turned on at the time of mounting the XFS filesystem.` |
| XFS accounts usage for every user, including users that have no limit set, so a zero limit and a zero usage are different things. | S479 | `XFS filesystems perform quota accounting whether the user has quota limits or not.` |
| An XFS filesystem with enforcement turned off is still a usage-accounting source. | S479 | `XFS filesystems with limit enforcement turned off can be used as an effective disk usage accounting system` |
| XFS never enforces limits on the superuser or on group and project ID zero (it still accounts their usage), so enforcement is not what fails a root-owned write. | S479 | `limits are never enforced on the superuser (nor are they enforced for group and project ID zero)` |
| A user at the hard limit sees the write or create fail with the EDQUOT error. | S479 | `If a user's usage reaches the hard limit, further requests for space (or attempts to create a file) fail with the "Quota exceeded" (EDQUOT) error.` |
| The `quot` subcommand reads usage by scanning the whole filesystem, also with quotas off, and can be slow, so it is not a one-shot probe. | S479 | `This command can be used even when filesystem quota are not enabled, as it is a full-filesystem scan (it may also take a long time...).` |
| Quota limits are per user, per group and per project on one filesystem. | S480 | `can be used to set per-user, per-group, and per- project limits on the amount of disk space used on a filesystem` |
| After the grace period a soft limit is treated as a hard limit. | S480 | `at a time; after this, the soft limit counts as a hard limit` |
| `ESRCH` from the quota syscall means quotas are not turned on, which is not the same observation as a usage of zero. | S480 | `No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem.` |
| `quotactl_fd()` addresses the filesystem by mount point, so it works where no block device exists. | S480 | `quotactl_fd () instead works on the mount point, which avoids this limitation and is simpler to use` |
| The generic Linux ABI header gives EDQUOT the number 122. | S481 | `#define EDQUOT 122 /* Quota exceeded */` |
| In the vendor's directory-quota example the failing write prints the English string `Disk quota exceeded`. | S482 | `dd: closing output file '/data/1G.txt': Disk quota exceeded` |
| The vendor's directory quota is a feature of a subdirectory mounted by `subPath`. | S482 | `CSI 组件支持为通用型 NAS 存储卷的子目录设置配额限制。使用 subPath 方式挂载 NAS 子目录时，可启用目录配额功能，限制子目录容量，提升资源利用率。` |
| The vendor shows the quota state in a separate console page, not in the failing write. | S482 | `然后单击 配额管理 。在 配额管理 页面，单击目录对应的 管理配额 可查看详细信息。` |

## What the lane held before

`git show e5dbac05:corpus/SOURCES.md | grep -cE 'xfs_quota|quotactl|EDQUOT|repquota'` → 0 (receipt
`.ufo/waves/round-48/evidence/sweep-quota-rows.txt`, 2026-10-25). The lane held the kernel's quota flags
(S078, S084, S088, S089) and the mount-option vocabulary (S077, S082, S085): what the kernel emits and
accepts, and no row on the user-space reporting surface or on the error a workload receives. The lane's own
census once failed with `printf: write error: Disk quota exceeded`
(`corpus/knowledge/audit-r11.md:96`; its F13 row at line 168 is the same class). The symptom was held; the
state and its vocabulary were not. (`seat-terminal-status-r17.md`'s `dead_quota` is a provider API quota
token, not a filesystem quota; the staged entry's link between the two is refused, lesson Gate.)

## Boundaries

- **Read-only.** mori observes and reports quota state; it never sets a limit, starts accounting, changes a
  grace period or runs a repair. No quota command was run against this host for this entry.
- **The number is per architecture.** 122 is the generic header's value (S481). Linux v7.2 `arch/mips`
  defines `EDQUOT` as 1133 (S483, `#define EDQUOT 1133 /* Quota exceeded */`, line 131) and `arch/sparc` as 69
  (S484, line 43). A probe matches the platform's own constant, or the symbolic name, never a copied number.
  A Japanese vendor document that quotes `errno=49` describes Solaris and stays rejected for this lane.
- **Filesystem-specific surface.** `xfs_quota(8)` is XFS; the `quotactl(2)` syscall is common to
  quota-supporting Linux filesystems but its reporting tools are not (S480). The root and ID-zero exemption is
  stated for XFS (S479); this entry does not extend it to other filesystems.
- **Another product's semantics.** S482 documents one vendor's NAS directory quota. It is a comparison shape for
  the failing-write string and the separate console view, not authority for mori's own alert thresholds, which
  stay local and labelled (FR8). The page embeds its body twice (rendered text and JSON), so a byte-identical
  re-fetch is not expected; the quotes are stable, the file hash is not.
- **Not adopted this round.** The staged entry's RHEL 9 Japanese PDF claims (the `+` soft-limit marker and the
  `grace` column) have no lane row or committed copy: the PDF answered HTTP 403 to the freeze fetch, and the
  claims stay out until a lane row is opened for them (`corpus/lessons/round-48.md` Gate, flip condition).

## Probe shape

A quota probe reads per-id state, never filesystem capacity:

- read accounting and enforcement separately (`xfs_quota -x -c state` on XFS) so that quotas off is not
  confused with usage zero; treat `ESRCH` as not turned on, never as zero;
- match the platform's own EDQUOT constant when reading the workload's failing write, or match the string the
  libc renders for it;
- price the reading: a syscall read per id is cheap, `quot` scans the filesystem (S479);
- address the filesystem by mount point where it has no block device (`quotactl_fd`, S480).

[INFERENCE] A seat or census that reports `Disk quota exceeded` has a per-id filesystem limit in play, not a
full device: the sources say the string comes from the failing write and the state lives in a separate
report. Nothing in them says what limit the fleet's own filesystems carry; this host's mounts were not read
for this entry.

## Delivery paths this cannot see

A filesystem with accounting off and no way to turn it on; a quota held by a remote file system whose counters
lag behind the write; exhaustion bounded by a capacity limit rather than a quota limit; a non-XFS filesystem
whose superuser is subject to its limits; the live page state between rechecks (the copies are dated
2026-10-25).

## Recheck at Linux v7.3 (appended 2026-10-27, round 54)

The claim rows of this entry that pin Linux v7.2 are re-read at tag v7.3 in `corpus/knowledge/kernel-v7.3-recheck-r54.md` (one row per claim hash: status, the v7.3 line the quote now begins on, disposition and its RECHECK votes). The rows above are unchanged and keep their v7.2 anchors; read moved line numbers through that ledger's `## Where the quotes moved` table.
