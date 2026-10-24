# SentinelProbe — C2 real-mode input boundary

**Verdict:** The listed APIs are read-only and do not imply `quotactl(2)`, `ioctl(2)`, a quota utility, or a privileged interface. However, the contract cannot honestly guarantee *no blocking* or *no mount side effect*: ordinary path resolution may traverse an automount or slow remote/FUSE filesystem. Real-mode permission-error semantics are also underspecified, and Python's default `realpath()` can suppress access errors.

## Findings

### M — Path lookup can block and can indirectly trigger an automount

**Exploit path:** A caller supplies an absolute `--path` whose ancestors cross an autofs mount, or a mount-source path requiring remote/FUSE lookup. `os.stat(path)` and `os.path.realpath(...)` perform synchronous pathname resolution. Traversing an automount point in a path prefix can request an automount; NFS/FUSE lookups can wait on the filesystem/server. `realpath()` also resolves symlinks through filesystem lookups. The contract accepts arbitrary absolute `--path` values and applies `realpath()` to a mount source, so these are not limited to the two default paths.

**Evidence:** Contract §C2 lists `os.stat(path)`, `os.path.realpath(path)`, `os.path.realpath(mount_source)`, and sysfs listing/existence/read operations (lines 77–80), while the CLI permits repeatable caller-selected absolute paths (lines 73–75). Linux `stat(2)` documents `AT_NO_AUTOMOUNT` as covering only the terminal component (and says it is implied since Linux 4.11); it does not make traversal of earlier path components a general no-automount guarantee. Python documents `os.stat()` as a `stat()` system call and `realpath()` as resolving encountered symlinks. These are synchronous calls; the contract provides no timeout or nonblocking mechanism.

**Impact:** The probe has no explicit `mount()` call, but path traversal can cause an automount, violating an unqualified “never mounts” promise. It can also hang for an unbounded period relative to the probe's control flow. This is a path-resolution side effect, not a quota syscall.

**Smallest remediation:** Narrow real-mode paths to an explicitly controlled set and document that ordinary lookup may wait/trigger automount; if “never mounts/nonblocking” is a hard guarantee, do not perform unconstrained path resolution. Do not claim the current API list is unconditionally nonblocking or side-effect-free.

### M — Permission failures can be hidden or confused with absence

**Exploit path:** Deny search/read access to a path component or sysfs entry. `os.stat()` can raise `PermissionError`/`OSError`; directory listing and opening a mode file can likewise fail. More subtly, the contract names `os.path.realpath(path)` without `strict=True`: Python's default `strict=False` ignores errors including access denied, returns the resolvable prefix with the remaining components appended, and may return a path that is not fully resolved. If “existence” checks are implemented with `os.path.exists()`, Python documents that access restrictions can produce `False` even when the path exists.

**Evidence:** C2 depends on `st_dev`, canonical path, sysfs `devices` listings, `qgroups` existence and optional `qgroups/mode` (lines 77–80), but specifies real-mode permission-error results only indirectly; it does not say how an unreadable mountinfo/sysfs entry or failed path lookup is represented. The output distinguishes a `qgroups` directory's presence from absence (table lines 115–117) but does not define an unreadable case. Python `os.path.realpath()` documentation explicitly says default non-strict mode suppresses errors such as “access denied”; Python `os.stat()` is the equivalent of `stat(2)`, whose `EACCES` condition includes missing search permission on a path directory.

**Impact:** Treating a denied `qgroups` listing as absent could falsely report `disabled`; treating a failed source/path resolution as a valid partial canonical path could choose no/wrong covering mount. That would turn lack of evidence into a confident verdict. A `null` mode alone does not distinguish “not present” from “could not read” unless the output has another status.

**Smallest remediation:** Define error mapping before implementation: unreadable/unparseable mountinfo → setup error; per-path `stat`/resolution errors and unreadable sysfs state → explicit `unknown` (never `disabled`); preserve `QUOTA_ENABLED` when another path has positive evidence, per the existing verdict precedence. Do not consume permissive `realpath()` output as a conclusive canonical path after an access error; distinguish special/non-path mount-source tokens from paths that must resolve.

### H (conditional) — Real-mode `qgroups/mode` read can hit Btrfs ASSERT

**Exploit path:** On a kernel built with `CONFIG_BTRFS_ASSERT=y`, a real-mode read of
`/sys/fs/btrfs/<uuid>/qgroups/mode` while quota-disable is in flight can enter
`qgroup_mode_show()` and fail its `ASSERT(btrfs_qgroup_enabled(fs_info))`. A guard that
first reads `qgroups/enabled` is not race-safe: the `mode` assertion checks the runtime
`BTRFS_FS_QUOTA_ENABLED` state, while `enabled` reports the on-disk `FLAG_ON`; during
disable, the runtime bit is cleared before `FLAG_ON` and the sysfs directory are removed.
Thus `enabled=1` can overlap a failing `mode` assertion.

**Evidence:** The source-only reports
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/SrcBtrfsSysfs.md`
and `SrcBtrfsQgroup.md` locate `ASSERT(btrfs_qgroup_enabled(fs_info))` in
`fs/btrfs/sysfs.c:2378`, the `enabled` read of `qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON`
at `sysfs.c:2363`, and the disable ordering in `fs/btrfs/qgroup.c:1367,1404–1411`.
Those reports state `ASSERT` becomes `BUG()` with `CONFIG_BTRFS_ASSERT=y`; this host's
kernel configuration was not read and the condition is therefore explicitly conditional.

**Impact:** A nominally read-only probe could trigger a kernel BUG/oops and, depending on
kernel panic policy, host availability loss. No quota syscall or userspace write is needed.

**Smallest remediation:** Never read `qgroups/mode` in real mode; emit `null` with an
explicit contract meaning of “not observed by policy,” not “attribute absent.” Fixture
mode may project its synthetic mode value without host access. An `enabled`-first gate
does not close the assertion window.

This safety change does **not** validate the separate `qgroups`-directory-present ⇒
`quota_state: enabled` claim. The cited qgroup source also shows a mounted filesystem can
retain the directory with the ON flag clear, so classification correctness needs its own
disposition.


## Confirmed boundaries

- `/proc/self/mountinfo` read, `os.stat()` metadata lookup, `realpath()` resolution and sysfs listing/existence checks do not themselves write files or change quota state. No block device is opened by these operations. Reading `qgroups/mode` is syntactically a read, but has the conditional kernel-assertion hazard above and is not safe merely because it has no userspace write effect.
- These calls do not imply `quotactl(2)`, `ioctl(2)`, `btrfs qgroup`, `xfs_quota`, `repquota`, `mount()`, or elevated capabilities. Contract §C2 explicitly excludes these interfaces (lines 67–71). Ordinary DAC/LSM/proc/sysfs visibility may still deny reads; that is not a need for privilege and must not be silently interpreted as absence.
- `mountinfo` and sysfs are synchronous pseudo-filesystem observations, not quota queries. There is no explicit sleep/poll/retry in the listed input surface, but pseudo-filesystem status is not a guarantee of a bounded, nonblocking syscall.
- Reads are not an atomic snapshot: path metadata, mountinfo and sysfs can change between operations. The contract already states that enable/disable/remount races are not excluded (line 139).
- No live host probes, implementation reads, tests, installs, or mutating operations were performed for this review.

## Evidence references

- Frozen contract: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`, §C2 lines 65–80, 105–140.
- Python `os.path.realpath()` (strict default and access-error behavior): https://docs.python.org/3/library/os.path.html#os.path.realpath
- Python `os.stat()` (stat syscall; follows symlinks by default): https://docs.python.org/3/library/os.html#os.stat
- Linux `stat(2)` (`EACCES`, path search permission, terminal-component automount flag): https://man7.org/linux/man-pages/man2/stat.2.html
- Btrfs source reasoning: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/SrcBtrfsSysfs.md` (`sysfs.c:2363,2378`) and `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/SrcBtrfsQgroup.md` (`qgroup.c:1367,1404–1411`).
- Linux `sysfs(5)` (pseudo-filesystem; individual attributes may be read-only or writable): https://man7.org/linux/man-pages/man5/sysfs.5.html
