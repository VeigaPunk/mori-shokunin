# PacmanActorTrace — actor attribution for the 2026-10-20 09:15 `pacman -Syu` and 13:23 `pacman -U zcode`

Seat: MoriR17.PacmanActorTrace-5 (scout). Detection only. **No journal query of any kind was run.** No pacman invocation. No VCS mutation. No tool installed or upgraded. All reads absolute-path, read-only.

Provenance: round-18 privacy repair (C1). Minimized replacement; private values withheld. Original: git blob `2773807b39ac60c3a4a5a5b870d9fdfbf738a5d9` at `29b0dc7:.ufo/waves/round-17/build/PacmanActorTrace.md`, SHA-256 `109e92f4d846c80d08a7ccb18c51dd42d1c0aabb9e921709515421c5f79097ef`, 157 lines. The commit at 29b0dc7 keeps the original text.

Host clock: local `-0300` (pacman.log timestamps).

## Verdict

- **09:15:30 `pacman -Syu --needed --noconfirm` (12 package names, as recorded at pacman.log:2462) — attributed EXACTLY (not inference) to one OMP session's bash tool call**, by identical stream content and a shared systemd invocation identifier (value withheld).
- **13:23:08 `pacman -U --needed --noconfirm ... zcode-3.16.2-1-x86_64.pkg.tar.zst` — attributed to the AUR helper `yay` running as uid 1000 at 13:22:53–13:23:09; no OMP tool output executed it.** The human or agent that invoked `yay` is [INFERENCE]-level only; the exact actor is unrecoverable from non-journal evidence.

## OBSERVED — transaction records (system log, world-readable)

`/var/log/pacman.log` (244858 B, mtime 2026-10-20 13:23:09, mode 644):

- `pacman.log:2462` — 09:15:30 `[PACMAN] Running 'pacman -Syu --needed --noconfirm'` with the 12-name package list.
- `pacman.log:2463-2464` — synchronizing package lists / starting full system upgrade (09:15:30–31).
- `pacman.log:3063` — 09:18:26 `[ALPM-SCRIPTLET]` systemd unit line; last line of that transaction; identifier withheld.
- `pacman.log:3161` — 13:23:08 `[PACMAN] Running 'pacman -U ... zcode-3.16.2-1-x86_64.pkg.tar.zst'`.
- `pacman.log:3164` — `installed zcode (3.16.2-1)`; `pacman.log:3169` — yay's mark-explicit step for zcode.

## OBSERVED — 09:15 actor: exact

- The OMP tool-output artifact that captured this transaction: 104896 B, mtime 2026-10-20 09:18:26.008 (artifact name withheld).
- Head is pacman process stdout (database sync, "starting full system upgrade", dependency resolution), not a log tail.
- Tail is byte-identical to `pacman.log:3063` (same systemd invocation identifier, so the same transaction stream). Granularity: artifact mtime equals the transaction's final hook second.
- Content counts in that artifact: "Starting full system upgrade" = 1; pacman-contrib = 1; nvme-cli = 3; linux-lts = 12.
- Neighbouring tool outputs in the same session at 09:16, 09:18 and 09:31. The 09:31 output is an AUR update run (`aur/elephant` update line) matching pacman.log's yay-driven 09:31:03 transaction.
- Intent record: an operator-owned planning note (contents withheld) predates the run and plans a targeted install rather than a full upgrade. The executed form was a full system upgrade (`pacman.log:2464`).
- Seat-level: `StorageAudit.md:1` and `:184` state that installs were not performed by that seat; `UpdateGate.md:30` refers to "the running `pacman -Syu`" (report mtime 09:19:45, written just after the transaction ended). See INFERENCE.

## OBSERVED — OMP tool-output hits are post-hoc reads, not executions

Every other tool-output hit for the two command strings lives in the current OMP session store (boot-time session; corroborated by the boot log and the wtmp boot at 09:57).

- Exact upgrade command string: 12 files, all later reads (mtimes from 11:01 onward).
- Exact zcode package filename: 4 files, all reads (13:31–15:54). Two of the four are this seat's own reads of pacman.log.
- Bodies confirm observation: heads are pacman.log excerpts or grep output. None contains pacman process progress output, so none is an execution record.
- No `Making package: zcode` and no `makepkg` string exists in any log under the session store (grep rc 1), so build output for the zcode package was never captured by an OMP tool.

## OBSERVED — 13:23 actor: yay / user, no OMP execution

- `~/.cache/yay/zcode/` (owner: user): directory created 13:22:53.5; PKGBUILD, .SRCINFO and .git 13:22:55.40; `.deb` 173324940 B at 13:23:00.79; `zcode-3.16.2-1-x86_64.pkg.tar.zst` 210964061 B at 13:23:08.426 (pacman start 13:23:08).
- `~/.cache/yay/vcs.json` mtime 13:23:09.057 (yay finalization). Sibling `elephant` cache directories at 09:31:04 match the yay-driven 09:31:03 transaction, which carries the same `--config` argv signature, so yay is the AUR helper on this host (`/usr/bin/yay` present; no yay user config file; no paru).
- Window sweep of all logs under the OMP session store with mtime 13:22:00–13:24:00: four files, none a package command.
- A second session-store root under another project: zero logs in 13:15–13:30; its only zcode and `pacman -U` hits are reads from 2026-10-11.
- The operator's interactive shell record was also consulted; its contents and search results are withheld (round-18 privacy repair, second pass). An unflushed interactive shell that ran yay at 13:23 cannot be excluded.
- `/var/log` sweep: in 13:22–13:25 only pacman.log (13:23:09.07) was written; in 09:15:00–09:19:30 no file under /var/log was written. The snapper log has no entries in either window and zero zcode hits (rc 1). No process-accounting file exists. No other agent store has a file in 13:21–13:25.

## INFERENCE

1. **[high]** The 09:15:30 upgrade was issued from OMP's bash tool in one session, most plausibly by the seat that produces `UpdateGate.md` (it alone writes "the running `pacman -Syu`"), while `StorageAudit.md` explicitly disclaims performing installs. The session is exact; the individual seat is not proved.
2. **[high]** `pacman -U ... zcode` was run by `yay` (argv carries yay's `--config` and a `-D --asexplicit` follow-up; yay cache writes land in the same 15 s window), as the login user (build artifacts owned by uid 1000; makepkg refuses root).
3. **[medium]** The 13:23 yay invocation came from an interactive shell or another non-OMP process: no OMP tool output in any session-store root executed it, and no other logged executor exists on the host.
4. **[medium]** The 09:15 run was a privileged invocation from uid 1000 via privilege escalation; pacman.log carries no uid, but the OMP tool call captured root-only pacman stdout.

## UNRESOLVED GAPS

- pacman.log records no uid, pid or ppid, so it cannot name an actor by itself.
- The 13:23 invoking shell or process is unrecoverable without auth or journal data (no process accounting; host logging configuration not reproduced). Only the journal could close it; this seat did not query it.
- Seat-level identity for the upgrade-output artifact is not encoded in any file name. Per-seat transcripts were deliberately not content-mined, and filename or mtime evidence cannot map an artifact to a seat.

## Commands run (all read-only; rc shown)

| check | rc | result |
|---|---|---|
| tail of pacman.log | 0 | 13:23 zcode transaction visible |
| locate 09:15 upgrade line | 0 | line 2462 |
| locate zcode lines | 0 | lines 3161, 3164, 3169 |
| locate 09:18:26 unit line | 0 | line 3063 |
| tool-output sweep, upgrade command string | 0 | 12 files, all later reads |
| tool-output sweep, zcode package filename | 0 | 4 files |
| build-output sweep, "Making package: zcode" | 1 | no match |
| tool-output sweep, mtime 13:22–13:24 | 0 | 4 unrelated files |
| tool-output sweep, mtime 09:00–09:35 | 0 | 3 files (09:16, 09:18, 09:31) |
| stat of 09:18 output | 0 | 104896 B, 09:18:26.008 |
| count of phrase and package names in that output | 0 | 1; linux-lts 12; nvme-cli 3 |
| `last -f /var/log/wtmp -n 12` | 0 | boot 09:57; login still open at check time |
| privileged find /var/log, 13:22–13:25 | 0 | only pacman.log 13:23:09 |
| privileged find /var/log, 09:15–09:19:30 | 0 | none |
| snapper log zcode count | 1 | 0 |
| log search outside session store | 0 | none |
| session-store root locator | 0 | two roots (paths withheld) |
| second root zcode / pacman -U grep | 0 | 2 old reads (2026-10-11) |

No URLs consulted. No external references.
