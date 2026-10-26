# The journal's reach is set by size limits and the boot, and a record the store no longer holds is unavailable, not zero

source: S485 — journald.conf(5), https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html — docs, tier A for the retention options; systemd 262 page, copy `corpus/evidence/sources-r49/journald.conf.5.html`, opened 2026-10-25
source: S486 — journalctl(1), https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — docs, tier A for `--disk-usage` and the vacuum switches; copy `corpus/evidence/sources-r49/journalctl.1.html`, opened 2026-10-25; supersedes the rejected row S351
source: S487 — systemd-journald.service(8), https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html — docs, tier A for storage placement; copy `corpus/evidence/sources-r49/systemd-journald.service.8.html`, opened 2026-10-25
source: S488 — own-work: host-journal-reach, this host only, read-only capture 2026-10-25T20:43:09-03:00; copy `corpus/evidence/sources-r49/host-journal-reach.txt`, tier A for that day
verified-at: 2026-10-25 (the three manual-page copies were byte-identical to a live fetch the same day)
recheck: 180d — `curl -s https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html | grep -c SystemMaxUse` → 5 on 2026-10-25; host rows: `journalctl --disk-usage` and `journalctl --list-boots` (neither is a message grep; both move, see Limits)
coverage-map: FR1 evidence reach — how far back the journal records mori reads can go, and what an absent record means
ground: frontier item FR1 ("Kernel OOM event-time attribution and fleet correlation"), boundary "a host record alone does not prove a fleet-caused kill". This entry supplies the retention rule behind that boundary and attributes nothing. Sweep before the entry: `SystemMaxUse`, `MaxRetentionSec`, `RuntimeMaxUse` → 0 in `corpus/SOURCES.md` and `corpus/knowledge/` at `b3e3453d` (`.ufo/waves/round-49/evidence/sweep-journal-rows.txt`).

## What reach means here

Reach is how far back a mori read of the journal can look. The rows below give two bounds of different kinds, plus a time rule that is off by default. The **persistent** store is bounded by **size**: the use limits cap the space it may take, and both journald's automatic removal and the vacuum switches take the **oldest archived** files first and never an active file. The **volatile** store is bounded by the **boot**: its data is lost at reboot. `MaxRetentionSec=` is a third, separate time rule whose default of 0 turns it off.

The rule this entry exists for: **a record the store no longer holds is unavailable, not a zero.** A count of zero over a window says only what the store held when the window was read. The lane already refuses "vacuumed" as a zero for alarms (`corpus/knowledge/journal-alarm-routing-r14.md:166,176`); this entry names the rule that decides where the retained set begins. It is context for evidence loss, not a way to recover a record.

## The rule, claim by claim

Every quote is a span of the committed copy named in `source:`. A claim stops at its quote.

| claim | source | quote |
|---|---|---|
| The `System`-prefixed size limits govern the journal stored on a persistent file system under /var/log/journal. | S485 | `apply to the journal files when stored on a persistent file system, more specifically /var/log/journal` |
| The `Runtime`-prefixed size limits govern the journal stored on the volatile in-memory file system under /run/log/journal. | S485 | `apply to the journal files when stored on a volatile in-memory file system, more specifically /run/log/journal` |
| During early boot, or with persistent logging disabled, only the Runtime-prefixed limits apply. | S485 | `during early boot and if the administrator disabled persistent logging, only the latter options apply` |
| The default size ceilings are percentages of the file system, not fixed sizes. | S485 | `The first pair defaults to 10% and the second to 15% of the size of the respective file system` |
| Size-based deletion removes only archived files, so active files are not reduced by it. | S485 | `Also note that only archived files are deleted to reduce the space occupied by journal files.` |
| Time-based deletion is a separate rule that deletes journal files holding entries older than a configured span. | S485 | `This controls whether journal files containing entries older than the specified time span are deleted` |
| The time-based rule is off by default. | S485 | `it might make sense to change this value from the default of 0 (which turns off this feature)` |
| The disk-usage reading is a sum over archived and active journal files, so it is a total. | S486 | `This shows the sum of the disk usage of all archived and active journal files.` |
| A size vacuum removes the oldest archived files until the space they use falls below the requested size. | S486 | `--vacuum-size= removes the oldest archived journal files until the disk space they use falls below the specified size` |
| A time vacuum removes archived files older than the requested span. | S486 | `--vacuum-time= removes archived journal files older than the specified timespan` |
| A file-count vacuum may leave more files than requested because it cannot remove active files. | S486 | `--vacuum-files= might not actually reduce the number of journal files to below the specified number, as it will not remove active journal files` |
| The service stores log data persistently below /var/log/journal or volatilely below /run/log/journal. | S487 | `The journal service stores log data either persistently below /var/log/journal or in a volatile way below /run/log/journal/` |
| Volatile storage does not survive a reboot. | S487 | `(in the latter case, it is lost at reboot)` |
| Persistent storage is the default when /var/log/journal exists during boot. | S487 | `By default, log data is stored persistently if /var/log/journal/ exists during boot, with an implicit fallback to volatile storage otherwise.` |
| A flush switches journald from volatile to persistent logging. | S487 | `a call to journalctl --flush (or sending SIGUSR1 to journald) will cause it to switch to persistent logging` |
| journald itself removes the oldest archived files to limit disk use, apart from any operator vacuum. | S487 | `systemd-journald will automatically remove the oldest archived journal files to limit disk use` |
| That day's capture: the whole-store footprint, archived and active, was 56M. | S488 | `Archived and active journals take up 56M in the file system.` |
| That day's capture: the system scope alone reported 19M. | S488 | `Archived and active journals take up 19M in the file system.` |
| That day's capture: the user scope alone reported 37M. | S488 | `Archived and active journals take up 37M in the file system.` |
| That day's capture: a local drop-in sets the system and runtime ceilings, so they are not the compile-time defaults. | S488 | `# /etc/systemd/journald.conf.d/size.conf [Journal] SystemMaxUse=256M RuntimeMaxUse=64M [exit 0]` |
| That day's capture: the previous boot was still listed, with its first and last entry times. | S488 | `Sat 2026-10-24 20:57:12 -03 Sun 2026-10-25 13:35:39 -03` |

## This host, as captured on 2026-10-25

Everything numeric here is the receipt `corpus/evidence/sources-r49/host-journal-reach.txt` of that day, not a standing value. The drop-in names a 256M system and a 64M runtime ceiling; the capture shows 56M in use in total (19M system, 37M user), so on that day the 256M ceiling was not what bounded the reach — the store held two boots, the older one from 2026-10-24 20:57. Two readings in the receipt must not be merged: the daemon's boot-time line puts the system journal at 45M and the later `--system --disk-usage` reports 19M. They count different things (a directory at boot against files the command can see), the receipt records no cause, and no row above rests on either the 45M or the 8M runtime line, because those lines came from a unit-scoped message search (`journalctl -b 0 -u systemd-journald -g …`) that the refusal row S351 asked the flip to avoid; the receipt keeps them as captured, and this entry does not use them.

The lane's earlier reading (`corpus/knowledge/journal-disk-usage-total-r51.md`, S470, added round 43) was 269M on 2026-10-24. Two dated readings do not make a rate. A seat that read the shell history while this entry was drafted found a `sudo journalctl --vacuum-size=50M` line at 2026-10-25 13:10:39 (`.ufo/waves/round-49/w1/Mo49ScoutHostJournal.md` finding D1; not a frozen source, and the actor is unverified). [INFERENCE] The fall from 269M to 56M is consistent with that vacuum; the entry states no cause as fact.

## Limits

- A located quote proves the words exist in the committed copy. It does not prove a claim beyond the sentence, and it does not prove the copy is today's page; the three manual-page copies were equal to a live fetch on 2026-10-25 only.
- Host rows are one capture. The 269M, 56M and 45M figures belong to three moments; none is a ceiling, a rate or a prediction of when the store will next evict.
- The empty `/run/log/journal` listing in the receipt is a capture, not a reading of absence. The service page says a flush moves volatile data to persistent storage; the receipt does not record the flush, so this entry draws no conclusion from the empty listing.
- `--disk-usage` reports allocated space, not file sizes. It is the figure the command can see, which is why the 56M total is not a per-journal share.
- Another host's drop-in or mount layout sets a different reach; nothing here is observable from another machine.

## Boundaries

- **Detection and report only.** No vacuum, rotation, flush, configuration write or service signal was run or is recommended here. The drop-in is reported as read.
- **journald configuration is not this lane's.** `PROVINCE.md` leaves OS package, systemd unit and boot state to tsukuroi; mori reads the journal as fleet evidence. This entry reports reach so a reader can tell a retained zero from a lost record; it advises no change to the ceilings. The sibling corpora that hold journald configuration read it as defaults-only on 2026-10-14 (`../tsukuroi-shokunin/corpus/knowledge/journal-boot-plane.md:51-52`); the drop-in above is dated 2026-10-16, so those readings are older, not contradicted.
- A missing record is evidence of where the retained set begins, never of an event that did not happen, and never a zero that a fleet count may be summed with.
