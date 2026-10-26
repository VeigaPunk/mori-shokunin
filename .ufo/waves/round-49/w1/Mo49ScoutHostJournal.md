# Mo49ScoutHostJournal — what moved the journal total from 269M to 56M

Author date: 2026-10-25 21:51 -0300 (lane tip `0df17b7b`, authored 2026-10-25 20:30:53 -0300). Seat: scout, read-only. Host reads only (`journalctl` read verbs, `sudo -n ls/stat/journalctl --header`, `stat`, `du`, `findmnt`). No vacuum, rotate, flush, restart, config edit, or pacman. Machine id written as MACHINE_ID.

## Answer in one paragraph

The drop is explained by an invocation recorded in the host's own journal, not by journald's configured ceilings. `sudo[3394677]: vgpnk : USER=root ; COMMAND=/usr/bin/journalctl --vacuum-size=50M` is logged at 2026-10-25 13:10:39 -03 (boot -1), 26 minutes before the 13:35:39 shutdown. After the reboot journald itself reported the directory at 45M (13:36:20), and every file older than the surviving set (system 2026-10-24 22:20:50, user 2026-10-24 20:57:12) is absent. That is consistent with a vacuum to about 50M having deleted older archived files. What the facts do not establish: who typed or scripted it, what it printed, or how many bytes it freed (the output never entered the journal), and which files it deleted (no file list survives). The reduction was not journald's own `SystemMaxUse=256M` pruning: 269M is above that ceiling and a size ceiling only removes enough to get back under 256M, never down to ~45M. Also, `journalctl --list-boots` shrinking to 2 boots is a downstream effect of the same deletion (round 26 saw 6 boots on 2026-10-22).

## Observed facts

All commands run 2026-10-25 between 21:48 and 21:51 -03, exit 0 unless stated. Ordering: oldest evidence first in each group.

### A. Totals and what they count

| # | fact | command | observed output | note |
|---|---|---|---|---|
| A1 | total now | `journalctl --disk-usage` | `Archived and active journals take up 56M in the file system.` | same as the receipt (captured 20:43); unchanged 65 min later |
| A2 | split now | `journalctl --system --disk-usage` / `--user --disk-usage` | 19M / 37M | 19+37=56; matches the receipt |
| A3 | per-file allocation | `sudo -n stat -c '%n birth=%w mtime=%y size=%s blocks=%b' <dir>/*` | system.journal 8388608 B / 16384 blocks; system@…3227c8… 16777216 B / 22528 blocks; user-1000.journal 16777216 B / 32768 blocks; user-1000@…31b43b… 16777216 B / 22656 blocks; user-1000@…324118… 16777216 B / 20400 blocks | blocks are 512 B: allocated bytes = 8.0M + 11.0M + 16.0M + 11.1M + 10.0M ≈ 56M |
| A4 | allocated vs apparent | `sudo -n du -k -s <dir>/` vs `sudo -n du -k --apparent-size -s <dir>/` | 57368 K vs 73728 K | the `--disk-usage` number is allocated blocks (the archived 16M files occupy 10-11M because of btrfs compression/hole-punching [INFERENCE]), not the file sizes `ls` shows |
| A5 | prior readings | `git grep` in lane | round 26: `86.4M` (2026-10-22, `.ufo/waves/round-26/w1/ScoutHostJournal.md:26`); round 43: `269M` (2026-10-24, `.ufo/waves/round-43/evidence/disk-usage-r43.txt:3`, committed `dde525ea` 2026-10-24 21:13:07 -0300); round 49: `56M` (2026-10-25) | three readings in four days: 86.4M → 269M → 56M; moves up and down |

### B. Files present

| # | fact | command | observed output |
|---|---|---|---|
| B1 | store dir | `sudo -n ls -la --time-style=full-iso /var/log/journal/` | `432d02b5…` (MACHINE_ID) dir mtime 2026-10-25 13:36:21.477; `remote` empty; parent dir created 2026-10-03 17:42:07 |
| B2 | file set | `sudo -n ls -la --time-style=full-iso /var/log/journal/MACHINE_ID/` | 5 files: `system.journal` (active, mtime 21:48:17), `system@c55f…-00000000003227c8-…journal` (archived, mtime 2026-10-25 13:36:21), `user-1000.journal` (active), `user-1000@…31b43b…journal` (archived, mtime 2026-10-24 22:42:24), `user-1000@…324118…journal` (archived, mtime 2026-10-25 03:11:45) |
| B3 | oldest file (stat) | `sudo -n stat -c '%n birth=%w mtime=%y' …31b43b….journal` | birth 2026-10-24 22:42:24.736, mtime 2026-10-24 22:42:24.735 (its rotation moment, not its first entry) |
| B4 | per-file content range | `sudo -n journalctl --file=<f> --header` (State/Head/Tail/Entry objects) | see table B4 below |
| B5 | `/run` journal | `sudo -n ls -laR --time-style=full-iso /run/log/journal` | one empty dir (`.`, 40 B), created 2026-10-25 13:36:20; `findmnt -no FSTYPE /run` is tmpfs (receipt). Runtime journal is empty after the 13:36:21 flush to `/var` |
| B6 | persistence | `findmnt -no TARGET,FSTYPE,SOURCE -T /var/log` and options | `/var/log btrfs /dev/mapper/root[/@log]`, options `rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvol=/@log`; `df -h /var/log`: 930G, 573G avail, 38% |
| B7 | boot list | `journalctl --list-boots --no-pager` | -1 `0a3785aa…` 2026-10-24 20:57:12 → 2026-10-25 13:35:39; 0 `7ab69ee4…` 2026-10-25 13:36:19 → now. Only two boots |

B4 content range (from `--header`, system files vs user files):

| file | state | head (first entry) | tail (last entry) | entries | boot id in header |
|---|---|---|---|---|---|
| system@…3227c8… | ARCHIVED | 2026-10-24 22:20:50 | 2026-10-25 13:36:21 | 25294 | `7ab69ee4…` (boot 0) |
| system.journal | ONLINE | 2026-10-25 13:36:21 | now | 4174 (and growing) | `7ab69ee4…` |
| user-1000@…31b43b… | ARCHIVED | 2026-10-24 20:57:12 | 2026-10-24 22:42:24 | 16470 | `0a3785aa…` (boot -1) |
| user-1000@…324118… | ARCHIVED | 2026-10-24 22:42:24 | 2026-10-25 03:11:45 | 11623 | `0a3785aa…` |
| user-1000.journal | ONLINE | 2026-10-25 03:11:45 | now | 15688 | `7ab69ee4…` |

Oldest retained entry per kind: system 2026-10-24 22:20:50 (`journalctl --system … | sed -n 1p` → a kernel line `try_charge_memcg+0x3d1/0x5d0`, i.e. the file starts mid-message, so its predecessor ended at a rotation boundary); user 2026-10-24 20:57:12 (`tmux child pane … launched`). The oldest system entry therefore lies **after** the 21:13 commit that holds the 269M reading, while the oldest user entry lies before it. Whole retention reach at 21:51 is ≈ 24 h 54 min (user) / ≈ 23 h 30 min (system).

Note the oldest surviving file is the **user** file; the system store has no entry for the first ~83 minutes of boot -1 that the user store has (system 23540 entries vs user 36923 entries for `-b -1`).

### C. journald's own lines

| # | fact | command | observed output |
|---|---|---|---|
| C1 | journald lines retained | `journalctl -u systemd-journald --no-pager -q -o short-iso` | only boot 0: `13:36:19 Journal started`; `13:36:19 Runtime Journal (/run/log/journal/MACHINE_ID) is 8M, max 64M, 56M free.`; `13:36:20 Time spent on flushing to /var/log/journal/MACHINE_ID is 12.476ms for 1701 entries.`; `13:36:20 System Journal (/var/log/journal/MACHINE_ID) is 45M, max 256M, 210.9M free.`; `13:36:21 Received client request to flush runtime journal.` |
| C2 | journald lines from boot -1 | `journalctl -b -1 -u systemd-journald --no-pager -q \| wc -l` | `0` — the retained boot -1 files begin after journald's boot -1 start, so no start/vacuum line from that boot can be read |
| C3 | vacuum/deleted lines | grep of the C1 output for `Vacuum|Deleted|Rotat` | none. (Rotation/vacuum messages from journald are not guaranteed to be logged at normal level [INFERENCE, not checked against the 262 source here]; absence is not evidence of no deletion) |
| C4 | active config | `systemd-analyze cat-config systemd/journald.conf` (non-comment) | `[Journal]` `SystemMaxUse=256M` `RuntimeMaxUse=64M` only (receipt L69-72; `size.conf` mtime 2026-10-16 11:53:47, 6 days before round 26's capture and 8 before the 269M reading) |
| C5 | `45M` meaning | arithmetic from B3/B4 allocations at 13:36:20 | "System Journal … is 45M" at 13:36:20 vs `--system --disk-usage` 19M now: the journald line is [INFERENCE] the whole `/var/log/journal/MACHINE_ID` directory (system + user files, ≈ 11 + 11 + 10 + ~14 ≈ 46M at that moment), and today's 19M is system files only. The same directory is 56M now = growth of active files since boot |
| C6 | systemd | `systemctl --version` first line | `systemd 262 (262-1-arch)` |

### D. The vacuum invocation

| # | fact | command | observed output |
|---|---|---|---|
| D1 | the only vacuum/rotate invocation in retention | `journalctl -t sudo --no-pager -q -o short-iso \| grep -E 'vacuum\|--rotate\|journald\|--flush\|--relinquish\|systemctl (restart\|kill)'` (2209 sudo lines retained) | `2026-10-25T13:10:39-03:00 plazir27 sudo[3394677]:    vgpnk :  USER=root ; COMMAND=/usr/bin/journalctl --vacuum-size=50M` (working directory omitted) |
| D2 | session around it | `journalctl -b -1 -o short-iso --since '2026-10-25 13:10:30' --until '2026-10-25 13:12:20'` filtered to sudo/journalctl | 13:10:33–34 three sudo runs `find /tmp -maxdepth 1 -mindepth 1 -mmin +1440 …`, `xargs -0 -r du -scb` (a temp-space survey), then 13:10:39 the vacuum with `pam_unix(sudo:session): session opened for user root(uid=0) by vgpnk(uid=1000)`; 13:12:09 `du -sh /var/log/journal /var/cache /var/tmp` |
| D3 | shutdown after | `last -x -F` | `shutdown system down … Sun Oct 25 13:35:39 2026 - 13:36:19`; `reboot … 13:36:19` (wtmp begins at the shutdown, so nothing earlier can be read there) |
| D4 | no vacuum in boot 0 | same D1 command, boot 0 | no further vacuum/rotate line; this seat ran none |
| D5 | other journal reads by an agent before | `journalctl -b -1 -t sudo` lines | 2026-10-25 03:31–03:34 seven `journalctl --no-pager --since …` reads from a sibling lane working directory; reads, not vacuums |

## What moved (reading of the facts)

1. Direction: 86.4M (10-22) → 269M (10-24) → 45M (13:36:20, 10-25, journald line) → 56M (21:50, 10-25). The 269M → 56M change happened between 2026-10-24 21:13 (commit time of the 269M receipt; the capture itself is only dated 2026-10-24) and 2026-10-25 13:36:20.
2. One logged command in that window that is defined to delete archived journal files down to a size: `journalctl --vacuum-size=50M` at 13:10:39 on 10-25 (D1). The post-reboot 45M is within that figure (C5) and the retained files then are exactly the ones named in B2.
3. The surviving oldest boundaries (user 20:57:12, system 22:20:50 on 10-24) are where files rotated; they are consistent with those files being the active or newest archived ones that a `--vacuum-size` pass leaves in place [INFERENCE: whether `--vacuum-size` counts active files is not verified here].
4. journald's own limit does not explain it: `SystemMaxUse=256M` is a ceiling, not a target (C4); a 269M directory would be trimmed to below 256M at most, and no `SystemMaxFiles=100` or `MaxRetentionSec` (default 0, unlimited, receipt L52) pressure exists with 5 files. `MaxFileSec=1month` only rotates.
5. The 13:35:39 shutdown/13:36:19 boot is not a deleting event for persistent files here: Storage persisted (`/var/log` is a btrfs subvolume on disk, B6; `/run/log/journal` empty after flush, B5; the `system@` file was rotated at 13:36:21 right after flush).

## What the facts do not establish

- A smaller total is not proof of a vacuum. It is proof only that fewer allocated bytes sit in the directory now. Here the proof of a vacuum is the sudo log line, which shows invocation by `vgpnk` (uid 1000) with a size argument, not its output or its deleted-file list.
- Who ran D1 (the person or an agent/script under that uid) is UNVERIFIED; attribution is not claimed.
- The 269M reading's capture time is only "2026-10-24, before 21:13:07"; whether files had already been archived or rotated by size between that time and the vacuum is UNVERIFIED. journald may also have rotated/deleted archived files by size on its own (journald logs from boot -1 start were deleted, C2), so a partial contribution by journald's ceiling or by rotation cannot be excluded or measured.
- Archived `@…` files can rotate away by size (SystemMaxUse/KeepFree/MaxFiles) or by an explicit vacuum; from the files left, the two causes are indistinguishable. Only the sudo line distinguishes this case, and that line itself disappears when its file is vacuumed or when `sudo` entries age out.
- `--list-boots` listing 2 boots (B7) is the join of files retained; it does not say how many boots happened.
- The `--disk-usage` figure is allocated blocks on btrfs with zstd compression (A4, B6): 56M vs 72M apparent. The same data on another filesystem would print a different number.
- `--system` and `--user` figures add up (19+37=56) only because this host has only these two kinds of files in the directory (B2); `journalctl --disk-usage` counts a directory the invoker can read. As a non-root invocation without `systemd-journal` group membership the same command would count a different set [INFERENCE, not tested; this session read with permission as shown by the output].
- The journald line `System Journal … is 45M` and `--system --disk-usage` 19M name the same word with different scopes (C5); the entry must not equate them.

## Limits the entry must state about volatile numbers

1. Every size on this page is a capture: `56M` (system 19M, user 37M) on 2026-10-25 at 20:43 -03, still 56M at 21:48. The lane's own earlier captures were 86.4M (2026-10-22) and 269M (2026-10-24). A reader must treat a size as a dated sample, never as a standing property of the host.
2. The size can fall by a large factor within a day without any journald setting changing: here 269M → 45M within about 16 hours, with the config file unchanged since 2026-10-16.
3. The retention reach (oldest readable entry) is the actual ceiling for any evidence claim: at capture it is 2026-10-24 20:57:12 (user) / 22:20:50 (system), ≈ 24 h, with 2 boots. A reach read at one time may not exist at the next; do not cite a boot older than `--list-boots` shows today.
4. `SystemMaxUse=256M` (and `RuntimeMaxUse=64M`) are upper bounds that journald enforces on rotation; the effective reach is whatever is smaller among that ceiling, `SystemKeepFree`, `SystemMaxFiles`, `MaxRetentionSec` and any operator vacuum. A host receipt must name which of these was observed, not infer it from the total.
5. The three scopes differ: `--disk-usage` (everything it can read), `--system`, `--user`, and journald's own `System Journal … is NM` line (directory). State which one a number comes from.
6. A vacuum or rotation leaves no result in the journal except the invoking `sudo` line (D1) and whatever journald logs at its boot; a reader who finds a smaller total should look for the invocation record before saying "vacuumed", and say "unattributed" when the record is absent or aged out.
7. The runtime journal at `/run/log/journal` is empty after the boot flush on this host (B5); the reach is a persistent-store reach, bounded by the previous vacuum and by rotation, not by the boot, except in the sense that a boot's early part may be missing (system files lack the first ~83 min of boot -1 that user files hold).
8. For the receipt's quote rows: quote `Runtime Journal … is 8M, max 64M, 56M free.` and `System Journal … is 45M, max 256M, 210.9M free.` as the 13:36:19–20 boot-time journald statements (they are the receipt's L96-97), not as the current usage.

## Suggested receipt addition (host-journal-reach.txt is frozen; for the L1's discretion, not edited)

The frozen receipt does not carry the vacuum invocation, the per-file header ranges or the allocated-versus-apparent figures. If the entry's limits paragraph names a vacuum as the cause of 269M → 56M, the only committed support would be this report; the receipt shows no vacuum. The entry should either say "the 269M reading was a day earlier and the total fell; a recorded `journalctl --vacuum-size=50M` invocation exists in the host journal at 2026-10-25 13:10:39 (this report D1)" with that report path as the source, or say only that the total moved and not claim a cause.

## Commands run (exact, for replay)

- `sudo -n ls -la --time-style=full-iso /var/log/journal/` ; same on `/var/log/journal/MACHINE_ID/` and `/var/log/journal/remote/` ; `sudo -n ls -laR --time-style=full-iso /run/log/journal`
- `journalctl --disk-usage`, `--system --disk-usage`, `--user --disk-usage`, `--list-boots --no-pager`
- `sudo -n journalctl --file=<each file> --header` (grep State/Boot ID/Head/Tail/Entry objects/Disk usage/Arena size) and `--list-boots`
- `sudo -n du -k -s` and `--apparent-size`; `sudo -n stat -c '%n birth=%w mtime=%y size=%s blocks=%b'`
- `journalctl -u systemd-journald --no-pager -q -o short-iso`; `journalctl -b -1 …` (`-u systemd-journald`, `-t sudo`, `-k`, `--system`, `--user`); `journalctl -t sudo -q -o short-iso`
- `systemd-analyze cat-config systemd/journald.conf`; `systemctl --version`; `findmnt -no … -T /var/log`; `df -h /var/log`; `last -x -F`
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep` / `git log` (read-only)

Not run: any `--vacuum*`, `--rotate`, `--flush`, `--sync`, systemctl, config edit, pacman. No tooling installed. Scratch dir not used.

## Findings

- MED — `corpus/knowledge/journal-reach-r49.md` (to be written) and `corpus/evidence/sources-r49/host-journal-reach.txt` (frozen): the receipt shows 56M/19M/37M and no cause for the fall from 269M. The cause evidence (the `sudo … journalctl --vacuum-size=50M` line at 2026-10-25 13:10:39, plus the per-file ranges) lives only in this report. An entry that says "vacuumed" would cite a non-frozen source; either name this report as the source of that sentence or claim only that the total moved.
- MED — contract `contract.md:108-109` ("the journal total moved from 269M … to 56M within one day"): the statement is true as a pair of readings but "within one day" is a window of up to ~24 h (269M captured on 2026-10-24 before 21:13; 56M at 2026-10-25 20:43). The size dropped to 45M by 13:36:20 on 10-25, so the fall happened in under 16.5 h of the first reading, around a recorded vacuum invocation. Say "dated readings", not a rate.
- MED — the entry's "System Journal … is 45M" quote (receipt L97) versus `--system --disk-usage 19M` (receipt L9): different scopes (directory vs system files only; C5 is an INFERENCE from the file allocations, not a source statement). A reader summing or comparing them gets a wrong reach; the limits paragraph must name the scope of each number.
- LOW — `journalctl --disk-usage` counts allocated blocks (btrfs zstd, A4): 56M allocated vs 72M apparent for the same five files. Not in the receipt; the entry should not call the figure "file size".
- LOW — the receipt's `ls -A /run/log/journal` is empty with exit 0 and `findmnt -no FSTYPE /var/log/journal` exits 1 (receipt L83-87): the second line is "not a mount point", not an error about persistence; `/var/log` is a btrfs subvolume (B6). The entry should not read exit 1 as "no persistent store".
- LOW — the retained journald-unit lines start at 13:36:19 of boot 0; boot -1's journald lines were deleted (C2). Any claim about journald's own rotation or vacuum decisions in that boot is UNVERIFIED.
- LOW — attribution of the vacuum invocation (D1) is UNVERIFIED: it is a `sudo` line under uid 1000, not evidence of the person or tool.
