# Mo55Crit12 — C2 operational safety review

## Scope
Reviewed the C2 decision table in `corpus/knowledge/disk-runway-enospc-r55.md` for unsafe advice, privilege assumptions, and misleading btrfs/df interpretations. No production files changed and no C1/C2 votes emitted.

## Findings

- **No unsafe or privileged action recommended (no finding).** Every decision-table next step is observational: `df -P`, `df -i`, reading btrfs allocation sysfs attributes, and inspecting tmpfs mount options. The table and Boundaries section explicitly exclude writes, mount changes, cache drops, repairs, and quota operations (knowledge file lines 37–46). Verified as uid 1000 that the listed metadata `bytes_may_use` is readable (`-r--r--r--`) and `cat` succeeded; `df -P` succeeded. No escalation or modification is implied.
- **No misleading btrfs inode interpretation found (no finding).** The table says btrfs zero inode totals/free values are unavailable rather than evidence of exhaustion (line 41). Captured `df -i` shows `/dev/mapper/root` with `Inodes=0`, `IUsed=0`, `IFree=0`, `IUse%=-` (`.ufo/waves/round-55/evidence/host-disk-snapshot.txt`, df -i block). The advice properly avoids treating that as inode pressure.
- **Btrfs zero-Avail caveat is appropriately bounded (no finding).** The table associates low/zero Avail with possible metadata chunk/global-reserve pressure, directs readers to read-only allocation counters, and warns zero Avail does not prove all operations fail (knowledge file lines 39–46). This is consistent with the entry's Boundaries statement that zero-Avail is not a universal write-failure prediction (line 46).
- **Low — host mount-option observation was not captured by the cited command.** The snapshot evidence records `findmnt -n -o TARGET,FSTYPE,OPTIONS /tmp /fast / /dev/shm` exiting 1 with no output (`.ufo/waves/round-55/evidence/host-disk-snapshot.txt`, findmnt block). The tmpfs decision-table next observation says to inspect `findmnt` options (knowledge file line 40), which is still safe, but this captured command does not substantiate mount options or the cited size/nr_inodes settings. Small correction: query each target separately with `findmnt -n -o TARGET,FSTYPE,OPTIONS -T /dev/shm` (and the other targets as needed), or state explicitly that mount options were not captured. Do not infer mount-option values from the failed command.
- **No same-snapshot numeric contradiction.** The “On this host” paragraph's earlier point-in-time figures differ from the later captured snapshot; its following paragraph explicitly says the later read supersedes the earlier same-day sample (knowledge file line 52). The evidence file matches the later reported `/tmp`, `/fast`, `/`, tmpfs, and btrfs values. This is disclosed and not a misleading df assumption.

## Evidence / commands

- `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` — completed; scratch free 594.2G; no stop condition.
- Read `.ufo/waves/round-55/evidence/host-disk-snapshot.txt`: recorded `stat -f`, `df -P`, and `df -i` commands exit 0; captured `findmnt` multi-target invocation exit 1.
- `id` — uid 1000; sysfs listing showed `bytes_may_use` mode `-r--r--r--`; `cat .../allocation/metadata/bytes_may_use` succeeded (value 1075052544).
- `findmnt -n -o TARGET,FSTYPE,OPTIONS /tmp /fast / /dev/shm` — exit 1, no output (reproduced); no mount mutation.
- `df -P /tmp` — exit 0.

No tools installed. No verification beyond the read-only checks above.

## Findings

- Low: captured multi-target `findmnt` invocation failed, so mount options were not established by that evidence; `.ufo/waves/round-55/evidence/host-disk-snapshot.txt` findmnt block. Suggested correction is per-target `findmnt -T` query or an explicit capture gap.
