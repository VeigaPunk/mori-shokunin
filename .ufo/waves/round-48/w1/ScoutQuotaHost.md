# ScoutQuotaHost — host facts for FR2 boundary

Read-only host/lane observations. No tools installed; no production files changed. Lane tools were run with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ScoutQuotaHost`. No subagents dispatched.

## Host filesystem and quota options

- `findmnt -T /home/vgpnk/Projects/shokunin -o TARGET,FSTYPE,OPTIONS` → `/home btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=257,subvol=/@home` (exit 0). The lane repo and its `.scratch` are under this `/home` mount. No `usrquota`, `grpquota`, `prjquota`, or `quota` option appears in the mount options.
- `findmnt -T /tmp -o TARGET,FSTYPE,OPTIONS` → `/tmp xfs rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota` (exit 0). `/tmp` explicitly has `noquota`.
- `grep -nE '(usrquota|grpquota|prjquota|noquota|,quota)' /proc/mounts` (exit 0) showed `/dev/shm` tmpfs with `usrquota`, and `/tmp` plus `/fast` XFS mounts with `noquota`; no `grpquota`, `prjquota`, or `,quota` option. `findmnt -T /home/vgpnk/Projects/shokuknow/merge/mori -o TARGET,FSTYPE,OPTIONS` also resolved to `/home` btrfs (exit 0).
- `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/features/` listed `block_group_tree`, `compress_zstd`, `extended_iref`, `free_space_tree`, `no_holes`, `skinny_metadata`, `verity`; it did not list `simple_quota`. `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/quota_override` contained `0`. The global `/sys/fs/btrfs/features/` lists `simple_quota` as supported. Observed: the mounted filesystem's per-filesystem features listing lacks `simple_quota`.

## Quota command availability

- `for t in quota repquota xfs_quota quotactl btrfs; do command -v "$t"; done` → `quota`, `repquota`, and `quotactl` not found; `xfs_quota` is `/usr/bin/xfs_quota`; `btrfs` is `/usr/bin/btrfs` (exit 0). Direct checks of `/usr/bin/quota`, `/usr/bin/repquota`, `/usr/sbin/quota`, `/usr/sbin/repquota`, and `/usr/bin/quotactl` reported no such files. `/var/lib/pacman/local/` name listing found `btrfs-progs-7.1-1` and `xfsprogs-7.2.0-1` (read-only listing; no pacman command run).
- `xfs_quota -V` → `xfs_quota version 7.2.0` (exit 0); `btrfs --version` → `btrfs-progs v7.1` (exit 0). `xfs_quota --version` was also tried and returned usage/invalid-option, exit 1; `-V` is the working version flag.
- `sudo -n -l` (exit 0) included `(ALL : ALL) NOPASSWD: ALL`. `btrfs --help` listed `btrfs qgroup show [options] <path>` (exit 0). **`sudo -n btrfs qgroup show` was not run**, as instructed: wave rules allow sudo only for read-only `ls`/`cat`-style reads and expressly prohibit this command.

## EDQUOT / “Disk quota exceeded” search

Commands searched the requested lane paths; literal matches:

- `grep` for `EDQUOT` in `tools/` → `tools/mori-census.sh:354`: `# fleet's own reported disk failures are quota events (EDQUOT), which a capacity-%`. No `Disk quota exceeded` matches in `tools/`.
- `corpus/knowledge/audit-r11.md:96` contains `printf: write error: Disk quota exceeded`; line 168 repeats the phrase in F13's evidence.
- `corpus/knowledge/observability-surfaces-r2.md:258` contains `... fleet's own reported disk failures were EDQUOT quota events ...`; no `Disk quota exceeded` match there.
- Additional source-copy context: `corpus/evidence/sources-r48/errno.h:107` is `#define EDQUOT 122 /* Quota exceeded */`; host `/usr/include/asm-generic/errno.h:107` has the same definition. Host `uname -r` → `7.2.11-arch1-1` (exit 0).

## Additional FR2 path-boundary observation

The frozen C2 counter names its required entry `corpus/knowledge/quota-observability-r48.md` (`.ufo/waves/round-48/count-c2.py:29`). `tools/mori-routed-check.py` has R1 roots `("tools/", "corpus/knowledge/")` and marker `"quota"` (`:77-88`); `_added_paths` uses `git diff --diff-filter=A` (`:284-300`), and R1 flags added matching paths as `quota_path_added` (`:393-414`). I tested this in a scratch clone, not the lane repo: after adding that exact path, running the lane tool against the clone produced `R1 held=False reasons=['quota_path_added']`, with `quota_paths_added=['corpus/knowledge/quota-observability-r48.md']` (exit 1). This is a concrete compatibility conflict between the required C2 path and that R1 rule if the routed check is run against a revision containing the new entry. At real lane `HEAD` (freeze `4387cf94…`), R1 was held with no added quota paths; the overall tool returned exit 1 because R4 reported `no_round_ledger`.
