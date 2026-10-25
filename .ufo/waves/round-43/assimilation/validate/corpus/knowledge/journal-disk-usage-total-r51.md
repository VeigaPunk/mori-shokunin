# journalctl --disk-usage is a total, not a per-journal share

source: S470 — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — docs, tier A, systemd journalctl(1), opened 2026-10-24
verified-at: 2026-10-24
recheck: 180d
coverage-map: resource runway (journal store size). Not FR1 kernel-victim attribution.

`journalctl(1)` says `--disk-usage` "Shows the current disk usage of all journal files. This shows the sum of the disk usage of all archived and active journal files." A reading is therefore a total over the files that invocation can see, not a per-journal bound and not a vacuum ceiling.

Read-only on this host, 2026-10-24: `journalctl --disk-usage --no-pager` printed `Archived and active journals take up 269M in the file system.` and exited 0. That number is what the command could see. It is not a per-journal share, and it is not a license to vacuum, rotate, or change journald.

S014 already cites this manual for cursor and field selection. This entry cites the `--disk-usage` sentence only. No service was signaled.
