# Mo49ScoutStagedJournal — staged journal-theme entries: claim, support, verdict

Seat: scout (leaf, read-only). Date: 2026-10-25 (host clock 21:45 -03). Lane tip read: `0df17b7b` (freeze). Nothing edited except this file; scratch under `.scratch/r49-Mo49ScoutStagedJournal/` (HTML-to-text copies, live-page copies).
Machine id is written MACHINE_ID throughout. No `systemctl`, vacuum, rotate or config change was run; host reads were `journalctl --disk-usage`, `--list-boots`, `-g` greps of the daemon's own limit line, `ls`, and `sudo -n ls -la` of `/var/log/journal/MACHINE_ID`.

## 0. What was checked, and the one-line result

| item | observed |
|---|---|
| live page vs committed copy (sha256 prefix, bytes) | `journald.conf.5.html` b4a9b53e3e53dc53 = live, 39204 B; `systemd-journald.service.8.html` a7b443568865bb09 = live, 28143 B; `journalctl.1.html` 75440570fb1f7185 = live, 87375 B. The three pages are byte-identical live (`curl`, exit 0 each) and committed. |
| sentences every staged quote relies on | `--vacuum-size=` "removes the oldest archived journal files until the disk space they use falls below the specified size" (found 1×), "only operates on archived journal files" (1×), `--disk-usage` "shows the sum of the disk usage of all archived and active journal files" (1×), journald.service "stores log data either persistently below /var/log/journal or in a volatile way below /run/log/journal/ (in the latter case, it is lost at reboot)" (1×). All four located in the committed copies after the counter's `normalise` rules. |
| host today (`host-journal-reach.txt` and my own re-read, 21:45) | `--disk-usage` 56M; `--system` 19M, `--user` 37M; 2 boots listed (oldest first entry `2026-10-24 20:57:12`); daemon line this boot: `Runtime Journal … is 8M, max 64M, 56M free.` and `System Journal … is 45M, max 256M, 210.9M free.`; drop-in `size.conf` 46 bytes mtime 2026-10-16 with `SystemMaxUse=256M`, `RuntimeMaxUse=64M`; `/run` is `tmpfs`; `ls -A /run/log/journal` prints nothing and `/run/log/journal` itself is an empty directory (my `ls -la`: `total 0`, no machine-id subdirectory); `/var/log/journal/MACHINE_ID` holds 5 files (`system.journal`, one archived `system@…`, `user-1000.journal`, two archived `user-1000@…`). |
| one-day movement | Staged captures (2026-10-24): 250.3M, 258.3M, 6 boots, oldest file 2026-10-22 03:10. Lane S470 entry (2026-10-24): 269M. Today 2026-10-25: 56M, 2 boots, oldest 2026-10-24 20:57. The store fell by ~200M in about a day while the daemon logged 210.9M free of a 256M ceiling at 13:36 today. The cause is **UNVERIFIED** (no `Vacuuming`/`Deleted` line exists in the retained boots: `journalctl -u systemd-journald -g 'Vacuuming|Deleted|Rotating'` printed nothing, exit 0 — an absence over only two retained boots, not proof of no vacuum). What it proves is that a size ceiling did not drive this reach. |
| boot -1 daemon limit line | `journalctl -b -1 --no-pager -q -g 'Journal .* is'` prints nothing (exit 0): the retained history holds no copy of the staged "243.6M, max 256M, 12.3M free" line, so that line cannot be re-observed from here (it came from a boot no longer retained, or was never filed). |

## 1. Per-entry findings

### 1.1 `journal-effective-retention-r45.md` (source: S524) — REFUSE as staged; one fragment adoptable

Claim: the daemon's own start-up numbers are the effective retention; this host's drop-in (256M/64M) *is* the ceiling; the store "measures 250.3M against 256M, retains 6 boots, oldest 2026-10-22 03:10:10", and "the store is **at** that ceiling and evicting".

`source:` rows: one, S524 — a `file:///home/vgpnk/Projects/shokuknow/lanes/mori/round8/…` note, tier "own-work". This is exactly S351's refusal reason (a shokuknow `file://` note); the lane cannot open it. `recheck:` is `journalctl -b 0 -u systemd-journald | grep -c 'max 256M'` — a MESSAGE grep, the other thing S351's flip excludes (and it returns a different thing every boot).

Public support: S524 cites no public page (the "companion upstream" URL is a journald.conf page the lane did not hold at b3e3453d). The committed `journald.conf` copy supports only the generic frame: "systemd-journald will respect both limits and use the smaller of the two values" (SystemMaxUse= vs SystemKeepFree=), so "the ceiling is the drop-in" is incomplete — KeepFree (default 15% of the file system), `SystemMaxFiles=` (default 100) and `MaxRetentionSec=` also bound the reach; the entry names only the size limit.

Receipt-visible today (adoptable fragment, now this round's own committed receipt): drop-in values `SystemMaxUse=256M` / `RuntimeMaxUse=64M`, 46 bytes, mtime 2026-10-16 (`host-journal-reach.txt`, exit 0); the daemon's limit-line shape `System Journal (…) is 45M, max 256M, 210.9M free.` agrees with the drop-in.

Stronger than its own evidence:
- "at that ceiling and **evicting**": its own numbers are 250.3M < 256M and 243.6M + 12.3M free = 255.9M, so no eviction is shown; "evicting" is an inference the entry never evidences. r46 then says 258.3M ("over"), contradicting r45's "at".
- "reach is bounded by a **size** ceiling, **not** by a time limit": the `MaxRetentionSec=` default of 0 supports "no time limit by default" but not "the size ceiling is what set this reach" — today's data shows the reach shrank ~200M with 210.9M free (see §0). A reach is set by whatever last deleted files, not by the ceiling that sits above it.
- "does not license a statement about which boots the journal will still hold tomorrow" — correct, and today's 6→2 boots confirms it.
- The entry quotes the full machine id twice; the lane rule is MACHINE_ID.

One-day numbers: 243.6M, 250.3M, 6 boots, 2026-10-22 03:10:10, the 12.3M-free figure — all the capture of a day that no longer reads that way.

Depends on staged receipts this lane cannot see: every number (S524 note) and the `size.conf` mtime (now covered by `host-journal-reach.txt`).

Verdict: **REFUSE** the entry. **ADOPT-AS-REWRITTEN** only the claim "the drop-in is the configured ceiling and the daemon's start-up line states the limits it applied" from the committed receipt (rows below, 9–11). Flip to adopting the staged numbers: never — the numbers are replaced by 2026-10-25; flip for any "at ceiling / evicting" sentence: a receipt showing a daemon vacuum line (`Vacuuming done`) or two successive `--disk-usage` readings at ≥ the ceiling with the oldest file's date moving.

### 1.2 `journal-reach-at-ceiling-r46.md` (S532 + S537) — ADOPT-AS-REWRITTEN (S532 only); S537 refused

Claim: reach is bounded by size not age and shrinks from the oldest end; `--disk-usage` counts active files so the total can sit above the ceiling; on this host the store is "already over its ceiling" (258.3M vs 256M), 67 = 67 kill records agree, `max` counter 1798 → 2215, 6 boots, oldest file 2026-10-22 03:10.

`source:` rows: S532 — `journalctl(1)` public page, supported, quotes verified live and committed (`--vacuum-size=`, "only operates on archived", `--disk-usage`); S537 — `file://…/r9-journal-reach-now.txt` own-work note, not openable.

What the page supports, exactly:
- "removes the oldest archived journal files until the disk space they use falls below the specified size" — about the **`--vacuum-size=` command**. Supported.
- "the vacuuming operation only operates on archived journal files" and `--disk-usage` "sum of … archived and active" — supports "total can sit above the ceiling"; `journald.conf` says the same independently: "there might still be more space used than SystemMaxUse= or RuntimeMaxUse= limit after a vacuuming operation is complete" and "only archived files are deleted to reduce the space occupied".

Stronger than its quote:
- Title and first paragraph say the reach "**shrinks from the oldest end**". The `oldest` word is stated for `--vacuum-size=` only. The committed `journald.conf` copy has zero occurrences of "oldest"; the daemon-side rule is "size limits are enforced synchronously when journal files are extended" with "deletion of historic data" under SystemMaxFileSize=. The order of the daemon's own automatic enforcement is therefore not stated by these pages — say "the vacuum command removes the oldest archived files first", not "the journal's reach shrinks from the oldest end".
- "bounded by size, **not by age**" — `MaxRetentionSec=` is "the maximum time to store journal entries" with default 0 (off): a configured time limit would also bound reach; the page-level claim is "off by default", host-level claim needs the receipt (`#MaxRetentionSec=0` in `cat-config`, observed). `--vacuum-time=` also exists.
- "already **over** its ceiling" reads as a fault; the page says over-ceiling totals are expected (active files are counted, only archived files are deleted). A total above SystemMaxUse= is not evidence of a shortfall.
- "the next vacuum removes archived files, oldest first" — no vacuum is scheduled by anything cited.

One-day / own-work numbers: 258.3M, `oom_kill 67` = 67 retained kill records, 1798 → 2215, six boots, 2026-10-22 03:10. All are captures of 2026-10-24; today 56M, 2 boots, oldest 2026-10-24 20:57. The kill counters and cgroup `max` counter are FR1 content from another lane's note and do not bear on journal retention; `recheck: … grep -c 'Killed process'` is a kernel MESSAGE grep (S351's explicit "no MESSAGE grep").

Depends on staged own-work receipts this lane cannot see: S537 entirely (258.3M, 67/67, 1798/2215, boots, oldest file).

Verdict: **ADOPT-AS-REWRITTEN** — keep the S532 rule rows with the wording fixed as above; **drop** the "this host" section (replace with today's receipt: 56M, 2 boots, oldest 2026-10-24 20:57). Flip for restoring "reach shrinks from the oldest end" as a daemon-wide statement: a public page sentence about the daemon's own deletion order (none in the three committed pages), or a receipt of the retained-file list across two readings with the oldest file removed first.

### 1.3 `reach-is-per-journal-r47.md` (S544) — REFUSE; the rule is re-derivable from public pages

Claim: the reach is a property of a journal not a host; this host has two journals (256M system, 64M runtime); only one host is measurable (the lane's "186 saved evidence files name 0 host tokens", `plazir15` only a push target).

`source:` row: S544 only — own-work `file://…/r10-reach-hosts.txt` note; a sweep of **another lane's** corpus. Unopenable; the two quoted daemon lines are real in shape (today's receipt carries both) but the numbers in the staged quote (243.6M, 12.3M free) are the stale boot's. Note the quoted pair is staged with the *machine id in full*.

Public support not cited by the entry: `journald.conf` "The options prefixed with System apply to the journal files when stored on a persistent file system … The options prefixed with Runtime apply to the journal files when stored on a volatile in-memory file system" and "The former is used only when /var/ is mounted, writable, and the directory /var/log/journal exists. Otherwise, only the latter applies." (both found, 1×, committed copy). That sentence is the whole public basis for "two journals, two sets of limits"; the staged entry never uses it.

Stronger than its evidence:
- "A host running two journals has two **reaches**" and "one is volatile and one is persistent, which is exactly why their ceilings differ" — the page says the limits are separate options, not that the ceilings differ *because* of volatility; the 64M/256M split on this host is the **drop-in's** values (`size.conf`), a configuration choice. The "why" is an inference the entry states as fact.
- "the lane's own 186 saved evidence files name **0** host tokens" counts the shokuknow lane's corpus. This lane's own tree names `plazir…` host tokens in 9 tracked files besides the new receipt (`git grep -lE 'plazir[0-9]+' HEAD`: rounds 14, 17, 24, 33, 44 waves/evidence) and the new receipt's own daemon lines carry `plazir27`. So the sweep result is not transferable to this lane and "only one host is measurable" is a claim about a different corpus.
- "**only one host is measurable from this seat**" — the title; not checkable here (UNVERIFIED), and not needed for the rule.

Depends on staged receipts this lane cannot see: the sweep ("0", "two", `plazir15` as a push target) and the 186-file count.

Verdict: **REFUSE** as an entry; its rule is carried by the page sentences above (row 7–8 of the rewrite, below). Flip: a committed, lane-visible host sweep command with its output that shows how many hosts' limit lines the lane's own evidence holds — not the other lane's count.

### 1.4 `reach-per-journal-second-instance-r48.md` (S554) — REFUSE; its central reading is contradicted by the committed `systemd-journald.service(8)` page

Claim: the runtime journal "holds **no files and no records at all** — its directory is empty"; "ceilings of 256M and 64M, reaches of six boots and **none**"; title: "a ceiling of 64M and a reach of nothing at all".

`source:` row: S554 — `file://…/r11-reach-second-journal.txt` own-work; the quoted block `runtime journal (/run/log/journal)   max 64M    no files, no records` is a transcription in the note ("as transcribed in the note"), not a daemon line or command output.

What today's receipt and page show:
- The observation replicates: `ls -A /run/log/journal` → nothing, exit 0 (`host-journal-reach.txt`; my own `ls -la`: `total 0`; the machine-id subdirectory does not exist at all).
- The **interpretation** does not follow: `systemd-journald.service(8)` (committed, located 1×): "journald will initially use volatile storage, until a call to journalctl --flush (or sending SIGUSR1 to journald) will cause it to switch to persistent logging … This is done automatically on boot via systemd-journal-flush.service". `journalctl(1)` `--flush`: "Asks the journal daemon to flush any log data stored in /run/log/journal/ into /var/log/journal/, if persistent storage is enabled." On this host `/usr/lib/systemd/system/systemd-journal-flush.service` exists (`ExecStart=journalctl --flush`, `After=systemd-journald.service`, read-only `grep`). The daemon's own boot-0 lines show the runtime journal at 8M at 13:36:19 and the system journal at 45M a second later (13:36:20): the early-boot records moved to `/var`. So an empty `/run/log/journal` is the **post-flush state** of a host with persistent storage; boot 0's records are in the system journal (`--list-boots` lists boot 0 with entries from 13:36:19). The runtime journal has "no files" because its records were flushed, not because it has no reach — "a reach of nothing at all" is false; the records of the current boot are reachable.
- "six boots" is the system journal's one-day-old count; today two.
- The "no files" fact is a one-instant observation (the directory is empty when it is read after the flush; it holds files during early boot).

Depends on staged receipts this lane cannot see: the S554 note (transcribed line, directory listing).

Verdict: **REFUSE**. Flip: the entry's reading would hold only if a receipt showed records for the current boot present in neither journal (`journalctl -b 0` empty) — the opposite is observed today. The corrected claim is "the runtime journal is flushed into the persistent journal early in boot, so after boot it is empty and the current boot's records are in the system journal" (rows 9–10 below).

### 1.5 `runtime-journal-reach-is-the-boot-r49.md` (S560) — ADOPT-AS-REWRITTEN

Claim: the runtime journal's reach is the boot, not its 64M ceiling; "a window that spans a reboot can only be served by the persistent journal".

`source:` row: S560 — `systemd-journald.service(8)` public page. The quote "stores log data either persistently below /var/log/journal or in a volatile way below /run/log/journal/ (in the latter case, it is lost at reboot)" is verified (1×, committed = live). This is the one fully public-supported entry: **supported** for "volatile store is lost at reboot".

Stronger than its quote:
- "the runtime journal is bounded by the boot — its **64M ceiling binds it within a boot**": the page's own next sentences make the volatile store the *early-boot* store, flushed to `/var` automatically (see 1.4); `journald.conf` says the Runtime options apply "during early boot and if the administrator disabled persistent logging", the System options "if persistent logging is enabled and the system is fully booted up". On this host the daemon logged `Runtime Journal … is 8M, max 64M` before flush and `System Journal … is 45M, max 256M` after. The staged entry presents the runtime journal as the second journal that serves the boot; per the page it is a transient early-boot buffer on a persistent-storage host, and in-boot records live in the system journal under its own limits.
- The consequence "The volatile store cannot contribute to it at all" is right for a window across a reboot (lost at reboot), but the entry never says that records of the **current** boot *do* survive in the persistent journal after the flush; a reader would conclude a mid-boot window cannot be served by anything persistent.
- "On this host `/run` is a `tmpfs` and the runtime journal's directory holds **no files**" — `findmnt -no FSTYPE /run` → `tmpfs`, exit 0 (receipt); the directory is empty (observed) — but both are post-flush observations. The staged `recheck: … ls -A /run/log/journal/<machine-id> | wc -l` points at a subdirectory that does not exist on this host (`ls -la /run/log/journal` → `total 0`); I did not run that exact command (its output is UNVERIFIED), but a count of 0 from it could not tell "absent" from "empty". Use `ls -A /run/log/journal | wc -l`, which the receipt shows as exit 0 with no output.
- Title wording "is the boot" should read "is lost at reboot": the page states what is lost, not a reach.

One-day numbers: none beyond "no files", which replicated today.

Depends on staged receipts this lane cannot see: nothing — the entry stands on S560 plus a `findmnt`/`ls` that the new receipt reproduces.

Verdict: **ADOPT-AS-REWRITTEN** (S560, rewritten per the corrections). Flip: if the rewrite keeps "64M ceiling binds within a boot" without the early-boot qualifier, REFUSE.

## 2. Corrections the rewritten entry (`corpus/knowledge/journal-reach-r49.md`) needs

1. Rows come from the four frozen sources only; the staged own-work rows (S524, S537, S544, S554) are not cited at all — they are `file://` notes (S351's own refusal reason) and their one-day numbers are overtaken.
2. Strip every number from 2026-10-24 (243.6M, 250.3M, 258.3M, 12.3M free, 6 boots, oldest 2026-10-22, 67/67 kill counts, `max` 1798/2215). The contract's named limit says the same. Replace with today's receipt, labelled as the 2026-10-25 capture: 56M (19M system + 37M user), 2 boots, oldest first entry 2026-10-24 20:57:12, `System Journal … is 45M, max 256M, 210.9M free.`, `Runtime Journal … is 8M, max 64M, 56M free.`
3. Say "56M against a 256M ceiling" without "at ceiling/evicting/over ceiling". Add the movement: S470 entry 269M on 2026-10-24 (committed lane row) → 56M on 2026-10-25, and state the cause as UNVERIFIED.
4. Do not write "shrinks from the oldest end" as a rule for the journal; write it for `--vacuum-size=`.
5. Do not write "bounded by size, not by age" as a host fact; write: `MaxRetentionSec=` default 0 (the page), `#MaxRetentionSec=0` in the receipt's `cat-config`, `SystemMaxUse=256M` set by the drop-in, and the page's "use the smaller of the two values" for MaxUse vs KeepFree (so the effective ceiling is the smaller of the two).
6. Keep the runtime-journal story to what the three pages and the receipt show: volatile store lost at reboot (page); initially volatile then flushed on boot (page); empty `/run/log/journal` after boot (receipt) is therefore not "no reach" — current-boot records are in the system journal. Mark "persistent journal serves the boot after flush" as inference from the flush sentences plus `--list-boots`, not as quoted.
7. Do not carry any recheck command that greps MESSAGE text (`grep -c 'max 256M'`, `grep -c 'Killed process'`) — the lane's S351 flip says no MESSAGE grep. Use `journalctl --disk-usage`, `journalctl --list-boots`, `findmnt -no FSTYPE /run`, `ls -A /run/log/journal | wc -l`.
8. Replace the full machine id with MACHINE_ID everywhere (staged r45 and r47 print it in full).
9. SOURCES: new rows (ids S485–S488 per the contract range, assigned by the L1): journald.conf(5) (the retention page, rule rows), systemd-journald.service(8), journalctl(1) (the S351 flip row: `teaches` opens `supersedes S351 —`), host receipt; each `mined`, `opened 2026-10-25`, used-by the entry. S516/S532/S560's staged wording ("front-truncating", "oldest records go first", "the boot bounds it across boots") should not be copied into `teaches`.
10. The named limit on the host-receipt row: the receipt is one capture of 2026-10-25; the 269M → 56M shift in a day means no number in it is a standing fact.

## 3. Proposed rows (each quote verified against the committed copies with `count-c2.py`'s `normalise`: word count, count in the copy; every quote appears exactly once)

Source letters: **C** journald.conf.5.html, **V** systemd-journald.service.8.html, **L** journalctl.1.html, **H** host-journal-reach.txt. Map to S485–S488 by the L1.

| # | claim (for the `claim` cell) | src | quote (words, occurrences) |
|---|---|---|---|
| 1 | only archived files are removed by size limits, so the total can exceed the limit | C | `only archived files are deleted to reduce the space occupied by journal files` (13, 1) |
| 2 | a total above SystemMaxUse=/RuntimeMaxUse= after a vacuum is documented, not a fault | C | `there might still be more space used than SystemMaxUse= or RuntimeMaxUse= limit after a vacuuming operation is complete` (18, 1) |
| 3 | no time limit by default | C | `from the default of 0 (which turns off this feature)` (10, 1) |
| 4 | the ceiling is the smaller of the MaxUse and KeepFree values | C | `systemd-journald will respect both limits and use the smaller of the two values` (13, 1) |
| 5 | size limits are enforced when a file is extended, with no time-triggered step | C | `size limits are enforced synchronously when journal files are extended, and no explicit rotation step triggered by time is needed` (20, 1) |
| 6 | System/Runtime option sets apply to separate stores | C | `apply to the journal files when stored on a volatile in-memory file system, more specifically /run/log/journal` (16, 1) |
| 7 | the persistent store is used only when /var is mounted, writable and the directory exists | C | `The former is used only when /var/ is mounted, writable, and the directory /var/log/journal exists` (15, 1) |
| 8 | the vacuum command removes oldest archived files first (command only) | L | `removes the oldest archived journal files until the disk space they use falls below the specified size` (17, 1) |
| 9 | --disk-usage is a total over archived and active files | L | `This shows the sum of the disk usage of all archived and active journal files.` (15, 1) |
| 10 | the volatile store is lost at reboot | V | `in a volatile way below /run/log/journal/ (in the latter case, it is lost at reboot)` (15, 1) |
| 11 | journald starts volatile and is switched to persistent by a flush | V | `journald will initially use volatile storage, until a call to journalctl --flush (or sending SIGUSR1 to journald) will cause it to switch to persistent logging` (25, 1) |
| 12 | --flush moves the /run data into /var | L | `Asks the journal daemon to flush any log data stored in /run/log/journal/ into /var/log/journal/ , if persistent storage is enabled.` (20, 1) — note the spaces before commas are the normalised page text |
| 13 | host 2026-10-25: journals total | H | `Archived and active journals take up 56M in the file system.` (11, 1) |
| 14 | host 2026-10-25: persistent journal limit line | H | `System Journal (/var/log/journal/MACHINE_ID) is 45M, max 256M, 210.9M free.` (9, 1) |
| 15 | host 2026-10-25: runtime journal limit line | H | `Runtime Journal (/run/log/journal/MACHINE_ID) is 8M, max 64M, 56M free.` (9, 1) |
| 16 | host 2026-10-25: oldest retained boot | H | `0a3785aac7104585a914f6cda41795a7 Sat 2026-10-24 20:57:12 -03 Sun 2026-10-25 13:35:39 -03` (9, 1) |

Sixteen rows, four sources; the counter's minimum is 8 rows, 3 sources. Row 12's quote holds the page's spaced punctuation exactly; if the L1 prefers a shorter span, `Asks the journal daemon to flush any log data stored in /run/log/journal/` is 13 words (not separately counted by me).

The claim cell must not exceed its quote: rows 3 and 6 are page statements ("default 0", "separate option sets"), not host facts; rows 8 and 11 state the vacuum command's and the early-boot order, not the daemon's deletion order; rows 13–16 are one capture. The counter proves only that the quote is in the copy (contract named limit), so each claim cell above is worded to stop at its quote.

## 4. Verdict table

| staged entry | S-rows | verdict | flip condition |
|---|---|---|---|
| journal-effective-retention-r45 | S524 | REFUSE; one fragment (drop-in values, daemon limit-line shape) re-derived from today's receipt | "at ceiling and evicting": a daemon `Vacuuming done` line, or two `--disk-usage` readings at ≥ ceiling with the oldest file's date moving |
| journal-reach-at-ceiling-r46 | S532 (S537) | ADOPT-AS-REWRITTEN (S532 only; S537 refused) | "shrinks from the oldest end" for the daemon: a public sentence on the daemon's own deletion order, or a two-reading file-list receipt |
| reach-is-per-journal-r47 | S544 | REFUSE; the rule is re-derived from `journald.conf` System/Runtime sentences | a lane-visible host sweep with its command and output |
| reach-per-journal-second-instance-r48 | S554 | REFUSE; its reading ("no records") is contradicted by the flush sentences and `--list-boots` | a receipt showing the current boot's records in neither journal |
| runtime-journal-reach-is-the-boot-r49 | S560 | ADOPT-AS-REWRITTEN | refuse the rewrite if "64M ceiling binds within a boot" survives without the early-boot/flush qualifier |
| (rule row from S516) | S516 | adopt as the `journald.conf` rule rows; do not copy "front-truncating … oldest records go first" (no "oldest" in the page copy, 0 occurrences) | — |

## 5. Limits of this report

- Observed: page text, byte identity with live, host reads listed in §0, `git grep` of this lane's tree. UNVERIFIED: the cause of the 269M → 56M drop; the content of any staged `file://` note (none opened — they are shokuknow paths outside the lane's reach and the contract forbids running anything there; I did not read them); whether the S516/S532/S560 staged `teaches` wording was already used by any lane entry beyond `counter-window-precondition-r44.md` (S516's `used-by`).
- A scout is not an independent judge; row 12's and 16's quote forms follow the counter's `normalise` output as run on the committed copies, not a full `count-c2.py` run on a drafted entry.
- No install or upgrade was performed.

## Findings

- HIGH — staged `reach-per-journal-second-instance-r48.md` (title and "no records at all" paragraph): reads an empty `/run/log/journal` as "a reach of nothing"; the committed `systemd-journald.service.8.html` ("journald will initially use volatile storage, until a call to journalctl --flush … done automatically on boot via systemd-journal-flush.service") and `journalctl.1.html` (`--flush`) say records of the boot are flushed to `/var`; today's `--list-boots` shows boot 0 with records. Do not carry this into `journal-reach-r49.md`.
- HIGH — staged `runtime-journal-reach-is-the-boot-r49.md` "its 64M ceiling binds it within a boot": omits that the volatile store is the early-boot store and the System limits apply after boot (journald.conf: "during early boot … only the latter options apply"); a rewrite must carry the flush qualifier (§1.5).
- HIGH — staged r45/r46: every number (243.6M, 250.3M, 258.3M, 6 boots, oldest 2026-10-22 03:10:10, 67/67, 1798→2215) is a 2026-10-24 own-work capture the lane cannot open; today 56M, 2 boots, oldest 2026-10-24 20:57:12 (`host-journal-reach.txt`); S470's 269M (lane row) shows the movement within one day. Do not carry any of them; label the receipt a single capture.
- HIGH — staged r45 sentence "the store is **at** that ceiling and evicting" is stronger than its own figures (250.3M < 256M; 243.6M + 12.3M free = 255.9M) and r46 says "over", contradicting it; neither is supported by a public page; today's reach shrank with 210.9M free, so "size ceiling set the reach" is falsified for this host.
- MED — staged r46 "the reach shrinks from the oldest end": `oldest` appears in the cited `journalctl.1.html` only for `--vacuum-size=`; `journald.conf.5.html` has 0 occurrences of "oldest"; claim must be scoped to the command.
- MED — staged r46 `recheck:` (`grep -c 'Killed process'`) and r45 `recheck:` (`grep -c 'max 256M'`) are MESSAGE greps, excluded by S351's flip text ("no MESSAGE grep"); the rewritten entry's `recheck:` must use `--disk-usage`/`--list-boots`/`findmnt`/`ls -A`.
- MED — staged r45 and r47 print the full machine id inside quoted daemon lines; the lane rule is MACHINE_ID (the new receipt already does).
- MED — staged r47 "186 evidence files name 0 host tokens" counts another lane's corpus; this lane's tree names `plazir…` in 9 tracked files plus the new receipt; the "only one host measurable" claim is not transferable and not needed for the rule (the per-journal rule is supported by journald.conf's System/Runtime option-prefix sentences, rows 6–7).
- MED — staged r45 names the ceiling as the drop-in's size and omits that the page makes the effective limit "the smaller of" MaxUse and KeepFree (row 4), and that SystemMaxFiles (default 100) and MaxRetentionSec also bound reach.
- LOW — staged r49 `recheck:` `ls -A /run/log/journal/<machine-id> | wc -l`: the machine-id subdirectory does not exist on this host (`ls -la /run/log/journal` shows `total 0`); I did not run the command as written, but it cannot separate "absent" from "empty"; use `ls -A /run/log/journal | wc -l`.
- LOW — staged S516 row `anchor` says "the paragraph under `MaxRetentionSec=`"; in the page the size paragraph (SystemMaxUse=) sits above it, and the text under `MaxRetentionSec=` is `SyncIntervalSec=`. Anchor wording needs fixing if copied.
- LOW — `reach-is-per-journal-r47.md` title/final line "one is volatile and one is persistent, which is exactly why their ceilings differ": the 64M/256M values are the drop-in's choice (`size.conf`), not a consequence of volatility; keep as inference or drop.
- LOW — the three source pages are byte-identical live and committed (sha256 prefixes in §0); the C2 quote rows in §3 are located, but "located" is not "supports the claim" — each claim cell must stop at its quote (contract named limit).
