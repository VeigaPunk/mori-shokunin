# Mo54ExecHostRead — read-only host observation for C2 (hardware memory-failure kills)

Report: `.ufo/waves/round-54/w1/Mo54ExecHostRead.md` (this file). Lane: mori-shokunin.
Scope: verify the `## On this host (read-only, 2026-10-27)` section of
`corpus/knowledge/memory-failure-kills-r54.md` and the host block of
`.ufo/waves/round-54/evidence/sweeps.txt` against the running host; report every mismatch and every host
fact those two documents leave out. Detection and report only: no sysctl write, no poison injection, no
cgroup change, no module load, no kernel line counted by message text.

Session identity: uid 1000, groups `vgpnk docker input wheel` (`id -u` → `1000`; `id -Gn` → `vgpnk docker input wheel`).
Kernel: `uname -r` → `7.2.11-arch1-1` (exit 0). CPU: `AMD Ryzen 9 9950X 16-Core Processor`.
Scratch `/fast/scratch/hyaku/mori-r54/Mo54ExecHostRead` used for two small cgit fetches only, removed after
copying the cited bytes here. No tool installed or upgraded (nothing was needed; pacman untouched).

## Live reads (command → output, exit code)

### Per-node counters

```
$ for f in /sys/devices/system/node/node*/memory_failure/*; do printf '%s: ' "$f"; cat "$f"; done
/sys/devices/system/node/node0/memory_failure/delayed: 0
/sys/devices/system/node/node0/memory_failure/failed: 0
/sys/devices/system/node/node0/memory_failure/ignored: 0
/sys/devices/system/node/node0/memory_failure/recovered: 0
/sys/devices/system/node/node0/memory_failure/total: 0
$ ls -d /sys/devices/system/node/node*
/sys/devices/system/node/node0
```

One NUMA node (`node0`) and no other; the directory holds exactly the five files
`delayed failed ignored recovered total` (`ls -la` → 5 files, `-r--r--r-- root root`, all world-readable,
`test -r` → yes for each, mtime 2026-10-27 01:20).

### meminfo and vm sysctls

```
$ grep -i HardwareCorrupted /proc/meminfo
HardwareCorrupted:     0 kB                          (grep exit 0)
$ for s in memory_failure_early_kill memory_failure_recovery enable_soft_offline \
          panic_on_unrecoverable_memory_failure; do printf '%s: ' "$s"; cat "/proc/sys/vm/$s"; done
memory_failure_early_kill: 0
memory_failure_recovery: 1
enable_soft_offline: 1
panic_on_unrecoverable_memory_failure: cat: /proc/sys/vm/panic_on_unrecoverable_memory_failure: No such file or directory   (cat exit 1)
$ ls /proc/sys/vm | grep -i memory_failure
memory_failure_early_kill
memory_failure_recovery
```

The only `memory_failure*` names under `/proc/sys/vm` are the two round-51-era sysctls; the v7.3 panic switch
is absent (ENOENT, not a permission error). Permissions of the three present knobs: `-rw-r--r-- root root`
(so this seat could write them as root — it did not and never will; Boundaries' prohibition is load-bearing).

### Tracepoint surface

```
$ ls /sys/kernel/tracing/events/ras/
ls: cannot open file '/sys/kernel/tracing/events/ras/': Permission denied     (exit 2)
$ ls /sys/kernel/debug/tracing/events/ras/
ls: cannot open file '/sys/kernel/debug/tracing/events/ras/': Permission denied  (exit 2)
$ cat /sys/kernel/tracing/events/ras/memory_failure_event/format
cat: /sys/kernel/tracing/events/ras/memory_failure_event/format: Permission denied
$ ls -ld /sys/kernel/tracing /sys/kernel/debug/tracing
drwx------ 9 root root 0 Oct 26 12:08 /sys/kernel/tracing
ls: cannot open file '/sys/kernel/debug/tracing': Permission denied
$ grep -E 'tracefs|debugfs' /proc/mounts
tracefs /sys/kernel/tracing tracefs rw,nosuid,nodev,noexec,relatime 0 0
debugfs /sys/kernel/debug debugfs rw,nosuid,nodev,noexec,relatime 0 0
```

Both trace filesystems are mounted and both are `0700 root:root`; an unprivileged reader cannot list
`events/`, cannot ask `available_events`, and therefore cannot confirm from the host whether the running
7.2.11 kernel exports `ras:memory_failure_event` or what its format string is. `software_events`-style
alternatives (`/sys/kernel/tracing`) are all behind the same `drwx------`.

### Kernel-text channels

```
$ journalctl -k -b -o json --no-pager -n 0 | head -1
(empty)                                              (pipeline exit 0, no error on stderr)
$ journalctl -k -b --no-pager -n 1 -o cat | wc -c
236                                                  (access confirmed; only length measured, no text tally)
$ dmesg
dmesg: read kernel buffer failed: Operation not permitted   (exit 1)
$ cat /proc/sys/kernel/dmesg_restrict
1
$ ls -l /dev/kmsg
crw-r--r-- 1 root root 1, 11 Oct 26 12:08 /dev/kmsg
$ cat /proc/sys/kernel/printk
0	4	1	4
$ grep -Eo 'quiet|loglevel=[0-9]+|splash' /proc/cmdline
resume=/dev/mapper/root resume_offset=3795013 quiet splash loglevel=0 ...  (full line read; no mce=, no hwpoison= parameter present)
```

Kernel messages are readable through journald as this user; the raw `dmesg` buffer and `/dev/kmsg` are not
(`dmesg_restrict=1`), and console loglevel is 0 (`quiet splash loglevel=0`), so nothing of this class is
echoed to a console. journald is persistent: `/var/log/journal` exists (`drwxr-sr-x+ root systemd-journal`),
a MACHINE_ID subdirectory is present, `/etc/systemd/journald.conf` carries no overrides (only `[Journal]`),
`journalctl --disk-usage` → `Archived and active journals take up 167.5M in the file system.`

### Error-accounting stack

```
$ for t in rasdaemon mcelog edac-util journalctl dmesg; do command -v "$t" || echo "(not found)"; done
rasdaemon: (not found)
mcelog: (not found)
edac-util: (not found)
journalctl: /usr/bin/journalctl
dmesg: /usr/bin/dmesg
$ ls /sys/devices/system/edac/mc/
power  subsystem  uevent                      (no mc0 instance)
$ cat /sys/devices/system/edac/mc/mc*/ce_count
cat: '/sys/devices/system/edac/mc/mc*/ce_count': No such file or directory
$ ls /dev/mcelog
ls: cannot access '/dev/mcelog': No such file or directory
$ ls /sys/devices/system/machinecheck/
machinecheck0 … machinecheck31, power, uevent   (32 per-CPU dirs; bank0…bankN are files, root-rw injection points, not read or written)
```

So on this host nothing decodes or counts corrected errors: no rasdaemon, no mcelog, no `/dev/mcelog`, no
EDAC memory-controller instance, and the tracepoint path that rasdaemon would consume is unreadable.

### Injection surfaces that exist (never touched)

```
$ ls -l /sys/devices/system/memory/hard_offline_page /sys/devices/system/memory/soft_offline_page
--w------- 1 root root 4096 Oct 27 01:43 /sys/devices/system/memory/hard_offline_page
--w------- 1 root root 4096 Oct 27 01:43 /sys/devices/system/memory/soft_offline_page
$ ls /sys/devices/system/memory/ | head
256 entries, auto_online_blocks, block_size_bytes, crash_hotplug, hard_offline_page, memory0 … soft_offline_page
```

Both offline knobs and the per-CPU MCE trigger files are root-write-only; the seat read their metadata only
(`ls -l`), never their value and never a write.

### Structured corroboration not named by the entry

```
$ cat /proc/sys/kernel/tainted
12288
$ grep -i poison /proc/vmstat
(no match, exit 1)
$ grep -iE 'poison|corrupt' /proc/meminfo
HardwareCorrupted:     0 kB
$ cat /proc/meminfo | grep -E 'MemTotal|MemFree'
MemTotal:       31721796 kB
MemFree:         3484852 kB
```

`tainted=12288 = 4096 + 8192` = bit 12 (externally-built/out-of-tree module) + bit 13 (unsigned module)
per the bit table in `Documentation/admin-guide/tainted-kernels.rst` (fetched at `h=v7.3`, 9340 bytes, table
at lines 80-105). Bit 4 (processor reported an MCE) and bit 5 (bad page referenced) are clear. That is a
second structured signal, independent of the counters and of any log text, that no machine check and no bad
page has been recorded since boot. `/proc/vmstat` has no poison key at all: the poisoned-page total is
reachable only through `HardwareCorrupted` and the per-node files, which matches the entry's evidence list.

## Agreement with the entry and with sweeps.txt

Every value in `## On this host` and in the `sweeps.txt` host block reproduces exactly: five
`node0/memory_failure/*` counters `0`; `HardwareCorrupted: 0 kB`; `memory_failure_recovery 1`;
`memory_failure_early_kill 0`; `enable_soft_offline 1`; `panic_on_unrecoverable_memory_failure` absent;
kernel string `7.2.11-arch1-1`; single node `node0`. The panic-message text quoted in the decision table
(`Memory failure: 0x…: unrecoverable page`) does exist in the committed v7.3 copy at
`corpus/evidence/sources-r54/memory-failure.c.v7.3:1295` (`panic("Memory failure: %#lx: unrecoverable page", pfn);`),
so that row is not misquoted.

Not reproducible from the host, and marked as such rather than counted:

- Whether any `Memory failure:` line exists in this boot's kernel buffer. Measuring that means selecting
  lines by message text, which QUALITY 15 forbids; the structured surfaces (five counters `0`,
  `HardwareCorrupted 0 kB`, taint bits 4 and 5 clear) are the evidence that stands. The decision-table row
  that says "no line and all counters 0 (this host, 2026-10-27)" therefore overstates what was measured for
  its first half.
- Presence and format of `ras:memory_failure_event` on 7.2.11 (tracefs 0700) — UNVERIFIED on the host; the
  S524 row is a v7.3 source fact only.
- That the SIGBUS/SIGKILL `pr_err` lines exist in the *running* 7.2.11 binary (no local kernel source or
  debug info for 7.2.11; the v7.3 tree is the only copy in the lane) — UNVERIFIED for 7.2, while the
  sysctls and counters they depend on are confirmed live.

## Findings

- HIGH none. No number in `## On this host` or in `sweeps.txt` is wrong.
- MED `corpus/knowledge/memory-failure-kills-r54.md` `## On this host` (lines 69-74) and the Claim paragraph:
  the entry lists the `ras:memory_failure_event` tracepoint among the evidence the kernel leaves, but on this
  host `tracefs` is `0700 root:root` and `/sys/kernel/tracing/events/ras` returns `Permission denied` (exit 2),
  the same for `/sys/kernel/debug/tracing`. No unprivileged observer can read that tracepoint, and the entry
  does not say so, so a reader would plan a detection path that cannot run at uid 1000.
- MED `corpus/knowledge/memory-failure-kills-r54.md` `## Decision table` last row, third column — "corrected
  errors are counted by EDAC/rasdaemon, not here": on this host `rasdaemon`, `mcelog` and `edac-util` are not
  installed, `/dev/mcelog` is absent and `/sys/devices/system/edac/mc` has no `mcN` instance (`mc*/ce_count`
  → No such file or directory). Corrected errors are counted by nothing here, so the table's escape route
  is not available on the host it is written about.
- MED `sweeps.txt` host block (lines after the `uname -r` line) and entry `## On this host`: neither records
  that raw kernel-buffer access is closed (`dmesg` → `Operation not permitted`, `dmesg_restrict=1`) while
  `journalctl -k -b` is open (exit 0, 236 bytes for one line). "The kernel log" in the Claim and the decision
  table is, on this host, journald only; a detector written against `dmesg` fails with EPERM here.
- LOW `corpus/knowledge/memory-failure-kills-r54.md` decision table, row "no line and all counters 0 (this
  host, 2026-10-27)": the "no line" half is a text-selected claim. The measured, QUALITY-15-safe statement is
  "all five counters 0, `HardwareCorrupted 0 kB`, taint bits 4 and 5 clear".
- LOW `corpus/knowledge/memory-failure-kills-r54.md:15` recheck line: "re-read … `/proc/sys/vm/memory_failure_*`"
  matches only `memory_failure_early_kill` and `memory_failure_recovery`; it silently skips `enable_soft_offline`
  (the entry's own line 72 cites it) and `panic_on_unrecoverable_memory_failure` (the switch the entry adds in
  v7.3, and the one most worth re-reading when the kernel moves past 7.2).
- LOW `corpus/knowledge/memory-failure-kills-r54.md` `## On this host`: the boot line is `quiet splash loglevel=0`
  and `/proc/sys/kernel/printk` is `0 4 1 4`, so no `Memory failure:` line can appear on the console; the entry
  should name journald as the channel rather than implying the console/log is where the line shows up.
- LOW `corpus/knowledge/memory-failure-kills-r54.md` decision table: `tainted=12288` (bits 12+13 set, bits 4 MCE
  and 5 bad page clear, per v7.3 `tainted-kernels.rst`) is a structured, text-free signal that no MCE and no
  bad-page event has been recorded this boot. It is not in the entry's evidence list; adding it gives a reader
  one more structured check that does not depend on the counters or on log text.
- INFO tool-channel state, 2026-10-27: cgit plain works for tree files (`include/linux/kernel.h?h=v7.3` → HTTP
  200, 6096 bytes; `Documentation/admin-guide/tainted-kernels.rst?h=v7.3` → 200) but `include/linux/tainted.h`
  is 404 at v7.3 (the bit table lives in the doc instead), and GitHub `ls-remote` was rate-limited again
  (`remote: This request was rate-limited…`, HTTP 429). Disk before the run: `/fast/scratch/hyaku` 26 % used,
  596.5 G free (`scripts/hyaku/disk-guard.sh status`).
- INFO host memory at read time: `MemTotal 31721796 kB`, `MemFree 3484852 kB` — recorded only so a later run can
  tell whether the zero counters belong to an idle host; no allocation was made to test the OOM path.

## Bounds observed

Writes: only this report. No write to `/sys`, `/proc/sys`, `/proc/sys/vm/*`, `/sys/devices/system/memory/*`,
`/sys/devices/system/node/*/memory_failure/*`, no `madvise(MADV_HWPOISON)`, no `hwpoison-inject`, no OOM
trigger, no cgroup change, no `systemctl`, no module load, no `pacman`. Reads: the paths listed above only,
plus one cgit fetch of `Documentation/admin-guide/tainted-kernels.rst` (bytes copied into this report) and a
404 probe of `include/linux/tainted.h`; scratch removed. No git or jj command against the lane.
