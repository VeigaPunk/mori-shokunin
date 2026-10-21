# Round 23 — real-mode filesystem read-fence review

**Axes:** filesystem-read boundary; fail-closed behavior under incomplete sysfs evidence.

**Scope and method:** static review only. The quota source blob at production revision `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` matches the checked-out source blob (`439ff4c1a68fc4f98182c6b855b3b4c790286851`); the source file had no working-tree change. No live host reads, selftests, builds, or runtime probes were performed.

## Finding — Medium: partial per-UUID sysfs listing failures can be treated as a unique device mapping

**Exploit path (conditional static scenario):** For a btrfs target whose resolved mount source basename is `dm-3`, suppose one visible UUID maps `dm-3` and has no `qgroups` directory, while another UUID also maps `dm-3` but its `devices/` listing fails with a permission error. `scan_btrfs_sysfs()` converts the failed devices listing to `[]`, then retains the UUID record; similarly, a UUID directory for which `os.path.isdir()` returns false is silently skipped. `classify_btrfs()` counts only the remaining visible matches. It can therefore see exactly one match and report disabled (or enabled) instead of unknown, even though the mapping is ambiguous or incompletely inspected. This is a source-derived scenario, not an observed host condition.

**Evidence:**
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:585-596` skips a false `isdir()` result and turns `os.listdir(.../devices)` `OSError` into an empty device list.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py:465-484` decides from the count of UUIDs that remain matched; exactly one match can be classified disabled or enabled.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseBtrfsTwoUuids.json:4-53` establishes the contract case: two UUIDs listing the same device must yield unknown. `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md:37-45,59-67` requires parent sysfs permission/listing errors to be unknown and zero/multiple UUID matches to remain unknown.

**Impact:** A partial sysfs view can suppress the required unknown result and make a btrfs quota-mechanism status appear determinate, including falsely disabled. This can mislead runway reporting; the probe does not itself change quota configuration.

**Smallest remediation:** Track an incomplete-scan condition for UUID-directory and `devices/` inspection failures, and prevent btrfs enabled/disabled classification when the device-to-UUID inventory is incomplete. Do not collapse those errors into “not a directory” or an empty device list.

## Read-fence checks

- The production real-mode path reads `/proc/self/mountinfo`; stats and resolves each requested path; resolves the mount-source path to its basename; lists `/sys/fs/btrfs`, checks UUID directories, lists `devices/`, stats `qgroups`, and reads `qgroups/enabled`. The code does not open `qgroups/mode` in real mode: its local mode value remains `None` (`mori-quota-surface.py:571-678`). This matches the safety correction in `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md:132-140`; S079 documents that `qgroup_mode_show` asserts qgroups are enabled (`.../evidence/sources/S079-fs_btrfs_sysfs.c:2355-2395`). Fixture-only mode metadata is separate.
- Direct error handling is fail-closed in the inspected paths: mountinfo-open and requested-path `stat` errors become setup errors with no partial verdict (`mori-quota-surface.py:658-678,1894-1916`); a top-level `/sys/fs/btrfs` listing error yields no UUID matches and therefore unknown; qgroups-path errors other than `FileNotFoundError`, and unreadable/invalid `enabled`, remain unknown (`:601-615`, `:465-484`). The per-UUID/device-list gap above is the exception.
- Static review found no fstab, mount-unit, Snapper/config, or on-disk superblock reads, and no quota command, `quotactl`, `ioctl`, mount, or write operation in the production real-mode path. The `superblock` occurrences are descriptive unknown/limit labels, not reads. The only `subprocess.run` is inside the explicitly separate selftest and invokes this script with fixture arguments (`:1810-1823`); it is not a quota command and was not run.

No source or frozen case bytes were changed.

Report: .ufo/waves/round-23/falsify/ReviewReadFence.md
