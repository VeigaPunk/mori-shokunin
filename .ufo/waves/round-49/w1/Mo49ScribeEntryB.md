# Mo49ScribeEntryB — w1 scribe: C2 entry draft (`corpus/knowledge/journal-reach-r49.md`)

Leaf seat. No subagents. Lane repo read-only except this report and `.scratch/r49-Mo49ScribeEntryB/`.
Lane HEAD was `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` before and after this seat; no lane file was
modified, staged, committed or checked out (evidence in *Touched surfaces*).

## Independence

I drafted the entry without reading `.ufo/waves/round-49/w1/Mo49ScribeEntryA.md` or any sibling draft.
Inputs were the frozen contract, the frozen counter, the four committed copies, `corpus/SOURCES.md`,
`SKILL.md`, the five lane entries named in the seat, row S351, and the staged entries under
`/home/vgpnk/Projects/shokuknow/merge/mori/` (bytes read, nothing executed there).

## Behavior — commands and observed output

1. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD` → `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`; `git log --oneline -4` shows the freeze commit above the entering tip `b3e3453d`.
2. Registry rows for the cites: `grep -n "^| S48[5-8] " corpus/SOURCES.md` → no output; `grep -oE '^\| S[0-9]{3,} ' corpus/SOURCES.md | tail -3` → `| S482 `, `| S483 `, `| S484 `; `wc -l corpus/SOURCES.md` → `324`. So S485–S488 do not exist at the freeze: landing them is part of the integration (Finding F3).
3. Copy pins, recomputed with sha256 over the working-tree bytes (`receipts.txt`): all four `MATCH`
   — `journald.conf.5.html b4a9b53e…`, `systemd-journald.service.8.html a7b44356…`,
   `journalctl.1.html 75440570…`, `host-journal-reach.txt be3952cb…`.
4. Quote selection: normalised each copy with the counter's own `normalise()`
   (lengths 22245 / 13421 / 41288 / 2963 chars), then searched the passages on retention
   (`SystemMaxUse`, `MaxRetentionSec`, `RuntimeMaxUse`, `Storage=`), vacuum/disk-usage, the
   persistent/volatile split and the host lines. Every quote below was checked three ways:
   `normalise()` substring (offset recorded), 6–25 words, unique in the table.
5. Counter runs (all read-only):
   - `python3 .ufo/waves/round-49/count-c2.py --selftest` → `C2_SELFTEST pass=26 fail=0`, exit 0.
   - `python3 .ufo/waves/round-49/count-c2.py 0df17b7b` → `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=ok provenance=bad rev=0df17b7b… failed=entry_absent`, exit 1. This is the do-nothing baseline on today's lane: the four copies pin correctly, the entry is absent.
   - `python3 .ufo/waves/round-49/count-c2.py b3e3453d` → `C2=unmet … failed=entry_absent,pins`, exit 1. Matches the frozen `evidence/control-c2-donothing.txt` label.
   - Fixture (a throwaway repo under `.scratch/r49-Mo49ScribeEntryB/fixture.*`, `git init -q`, top
     level verified equal to the fixture path before the first commit, throwaway identity inside that
     repo only): this draft committed with the four rows →
     `C2=met claims=19 located=19 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=4eb64ae098aef12c63b97a4c175cda5be1a734ce`, exit 0.
   - Same fixture, one word changed **inside one quote** (`oldest`→`newest`, S487) →
     `C2=unmet claims=19 located=18 quote_missing=1 … failed=quote_missing`, exit 1; restored →
     `C2=met … rev=7c685990…`, exit 0. The score is not vacuous.
6. Structural checks on the draft: claims table header parses as `['claim','source','quote']`, 19 rows,
   per-source spread S485=6 / S486=3 / S487=4 / S488=6; every claim cell ≥ 5 words; 5 lines in
   `## What this changes for mori` (limit 6); no 32-hex identifier and no hostname anywhere in the entry
   (`re.findall(r'[0-9a-f]{32}', entry)` → `[]`; the committed receipt's sanitiser already writes
   `MACHINE_ID`).
7. All five entries linked from `## What this changes for mori` were opened before being linked:
   `journal-disk-usage-total-r51.md` (whole file), `journal-alarm-routing-r14.md:150-190`
   (lines 166 and 176 read exactly), `oom-evidence-loss-r38.md` (whole), `retention-reconciliation-r22.md`
   (whole), `journal-cursor-window-r16.md` (whole). `SKILL.md:940-979` was read for the existing
   `### Decision row — …` shape.

## Gates

| gate | command | observed | exit |
|---|---|---|---|
| counter selftest | `count-c2.py --selftest` | `C2_SELFTEST pass=26 fail=0` | 0 |
| do-nothing at freeze | `count-c2.py 0df17b7b` | `C2=unmet … pins=ok … failed=entry_absent` | 1 |
| do-nothing at entering tip | `count-c2.py b3e3453d` | `C2=unmet … pins=bad … failed=entry_absent,pins` | 1 |
| draft + rows, fixture commit | `count-c2.py 4eb64ae0 --repo <fixture>` | `C2=met claims=19 located=19 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok` | 0 |
| tamper (one quote word) | same, next commit | `C2=unmet … located=18 quote_missing=1 failed=quote_missing` | 1 |

**UNVERIFIED:** `C2=met` at a *landed lane revision*. This seat may not write the entry into
`corpus/knowledge/` or `corpus/SOURCES.md` and may not commit; the met line above is from a committed
fixture repo whose `corpus/` tree is byte-identical to what the draft plus the four rows would land.

## Draft — `corpus/knowledge/journal-reach-r49.md` (for the L1 to land)

````markdown
# Journal reach — a size ceiling, oldest-first eviction, and a boot that was flushed

source: S485 — https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html — journald.conf(5), systemd 262, opened 2026-10-25
source: S486 — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — journalctl(1), systemd 262, opened 2026-10-25
source: S487 — https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html — systemd-journald.service(8), systemd 262, opened 2026-10-25
source: S488 — own-work: host-journal-reach — read-only capture 2026-10-25T20:43:09-03:00, kernel 7.2.11-arch1-1, corpus/evidence/sources-r49/host-journal-reach.txt
verified-at: 2026-10-25
recheck: 180d — `journalctl --disk-usage`, `journalctl --system --disk-usage`, `journalctl --user --disk-usage`, `systemd-analyze cat-config systemd/journald.conf | grep -E '^(SystemMaxUse|RuntimeMaxUse)='`, `ls -A /run/log/journal | wc -l`, `journalctl --list-boots --no-pager`
coverage-map: FR1
ground: frontier item **FR1** — how far back journal evidence reaches, and what an absent record means inside that reach.

## Claims

Each row is one claim and one located quote from the committed copy of that row's source under
`corpus/evidence/sources-r49/`. The quote proves the words occur; the claim is what this entry reads
them to say. Nothing here is a measurement of kills.

| claim | source | quote |
|---|---|---|
| journald.conf(5) states that its size-limit option group enforces size limits on the journal files stored | S485 | `Enforce size limits on the journal files stored.` |
| MaxRetentionSec deletes journal files whose entries are older than the configured time span | S485 | `The maximum time to store journal entries. This controls whether journal files containing entries older than the specified time span are deleted.` |
| Time-based deletion is off at the page's default value 0, which turns the feature off | S485 | `from the default of 0 (which turns off this feature)` |
| A vacuum reduces the footprint by deleting only archived files, not active ones | S485 | `Also note that only archived files are deleted to reduce the space occupied by journal files.` |
| Per-user journal files require persistent storage; without it journalctl --user is unavailable | S485 | `Note that per-user journal files are not supported unless persistent storage is enabled, thus making journalctl --user unavailable.` |
| journald starts on volatile storage until a journalctl --flush moves it to persistent storage | S485 | `journald will initially use volatile storage, until a call to journalctl --flush` |
| --vacuum-size= removes the oldest archived journal files until their disk use falls below the given size | S486 | `--vacuum-size= removes the oldest archived journal files until the disk space they use falls below the specified size.` |
| --disk-usage reads a sum over archived and active journal files, not a per-journal share | S486 | `Shows the current disk usage of all journal files. This shows the sum of the disk usage of all archived and active journal files.` |
| A vacuum-size run affects the --disk-usage reading only indirectly, because that reading includes active files | S486 | `running --vacuum-size= has only an indirect effect on the output shown by --disk-usage` |
| The daemon itself automatically removes the oldest archived journal files to limit disk use | S487 | `systemd-journald will automatically remove the oldest archived journal files to limit disk use.` |
| The service stores data either persistently below /var/log/journal or volatile below /run/log/journal | S487 | `The journal service stores log data either persistently below /var/log/journal or in a volatile way below /run/log/journal/` |
| Data in the volatile journal is lost at reboot | S487 | `in the latter case, it is lost at reboot` |
| Persistence by default follows whether /var/log/journal exists at boot, with a volatile fallback otherwise | S487 | `By default, log data is stored persistently if /var/log/journal/ exists during boot, with an implicit fallback to volatile storage otherwise.` |
| The host's total journal footprint read 56M at capture | S488 | `Archived and active journals take up 56M in the file system.` |
| The system-scoped reading was 19M at capture | S488 | `Archived and active journals take up 19M in the file system.` |
| The user-scoped reading was 37M at capture | S488 | `Archived and active journals take up 37M in the file system.` |
| The daemon's own boot line named 256M as the system journal's maximum | S488 | `System Journal (/var/log/journal/MACHINE_ID) is 45M, max 256M, 210.9M free.` |
| The daemon's own boot line named 64M as the runtime journal's maximum | S488 | `Runtime Journal (/run/log/journal/MACHINE_ID) is 8M, max 64M, 56M free.` |
| The capture states that no vacuum, rotation or config change was run | S488 | `no vacuum, rotate or config change was run` |

## The rule the pages give

Two different bounds, and only one of them sets reach on a normal host:

- **Size bound.** `SystemMaxUse=`/`RuntimeMaxUse=` cap the space the journal may use; when the store
  passes the cap the daemon deletes **archived** files. `MaxRetentionSec=` is the time bound, and it is
  off by default (`0`), so unless someone sets it the reach is whatever fits under the size cap. The
  service page states the automatic path directly: "systemd-journald will automatically remove the
  oldest archived journal files to limit disk use" (S487).
- **Eviction order.** `--vacuum-size=` "removes the oldest archived journal files until the disk space
  they use falls below the specified size". A vacuum is manual; the daemon's own size enforcement is
  the automatic path. Both act on archived files only, and the manual page warns that "only archived
  files are deleted", so a store can still sit above its cap after a vacuum.
- **Two stores, two kinds of bound.** Persistent data lives below `/var/log/journal`; volatile data
  lives below `/run/log/journal` and "is lost at reboot". A window that spans a reboot can only be
  served by the persistent store.
- **Reading the total.** `--disk-usage` sums archived **and** active files, while the vacuum removes
  only archived ones. A total above the cap is therefore an expected reading, not a fault, and it does
  not mean the next vacuum will bring it under the cap.

## This host, read-only, 2026-10-25T20:43:09-03:00

The capture at `corpus/evidence/sources-r49/host-journal-reach.txt` ran no vacuum, rotation or config
change. It recorded:

- `journalctl --disk-usage` → `Archived and active journals take up 56M in the file system.` (exit 0).
- `journalctl --system --disk-usage` → 19M (exit 0); `journalctl --user --disk-usage` → 37M (exit 0).
  19M + 37M = 56M: on this host the two scoped readings add to the total, which is what a sum over the
  files an invocation can see looks like (S486). [INFERENCE: the equality is arithmetic on the two
  observed readings; the receipt does not print a total for the scopes separately.]
- `systemd-analyze cat-config systemd/journald.conf` shows `/etc/systemd/journald.conf` at its compiled
  defaults plus a drop-in `/etc/systemd/journald.conf.d/size.conf` (46 bytes, mtime 2026-10-16)
  carrying `SystemMaxUse=256M` and `RuntimeMaxUse=64M`. The daemon's own boot lines agree on the
  ceilings: system `max 256M`, runtime `max 64M`. So the drop-in, not a compiled default, is the
  effective cap here.
- `findmnt -no FSTYPE /run` → `tmpfs` (exit 0); `findmnt -no FSTYPE /var/log/journal` → no output,
  exit 1 (not a separate mount point); `ls -A /run/log/journal` → no output, exit 0 (the directory
  exists and is empty at capture).
- `journalctl --list-boots --no-pager` lists exactly two boots: the previous boot's first entry
  2026-10-24 20:57:12 and the current boot's 2026-10-25 13:36:19 through 20:43:03 (exit 0).
- The daemon's boot line for the current boot reports the **system** journal as `45M, max 256M,
  210.9M free` and the **runtime** journal as `8M, max 64M, 56M free`.

Two readings need care:

1. **System journal: 45M at boot vs 19M at capture.** Both are observed lines from the same capture, at
   13:36:20 and 20:43:09. The receipt does not say which files each number counts. This entry does not
   explain the difference; it records that the boot line is a start-of-boot statement and the
   `--disk-usage` reading is taken later. [INFERENCE: a start-of-boot line is a snapshot, so the two
   numbers are not required to agree.]
2. **Runtime journal: `8M` at boot vs an empty `/run/log/journal` at capture.** The pages give the
   mechanism that makes both true: journald "will initially use volatile storage, until a call to
   `journalctl --flush` … This is done automatically on boot via `systemd-journal-flush.service`"
   (S485; S487 repeats the flush sentence). [INFERENCE: on this tmpfs `/run`, the boot's volatile
   files were flushed into the persistent store, which is why the volatile directory is empty while
   both boots are still listed. The receipt does not list `/var/log/journal` contents or the flush
   service's state.]

The consequence is the one that matters for a window: the persistent store, not the tmpfs, is what
carries this host's two retained boots, and the boot's early records are not lost at reboot **after**
they have been flushed. The volatile store's own reach remains the boot: an unflushed volatile record
does not survive it.

## What a short count means inside this reach

- A journal-derived count **lower than a counter** is a difference in populations, not a zero. Some
  records are not in the store: they were never emitted, were rate-limited, were unreadable in scope,
  or were evicted from the oldest archived end. The eviction is oldest-first and size-driven, so a
  shortfall concentrates at the start of the window.
- A window that **predates the oldest retained record** is unavailable, not empty. An anchor older than
  the retained reach cannot match a retained record; whether the CLI then refuses or starts at a
  neighbouring entry is not documented here, so the probe must refuse the window in either case (see
  `corpus/knowledge/journal-cursor-window-r16.md`) rather than report zero.
- A **total above the cap** — 269M against 256M on 2026-10-24, not 56M today — is not itself evidence of
  loss: only archived files are removed, so the active file can hold the overage. Reach is set by the
  oldest archived file still present, not by the printed total.
- A **config value is not the effective cap** by itself. Here they agree because the drop-in is what
  the daemon reads; on a host with only defaults the daemon's own line is the statement to trust.

## [INFERENCE]

- The flush explanation for the empty `/run/log/journal` (above) combines one page sentence with two
  observed facts; it is not printed in the receipt.
- The 45M/19M system-journal difference is attributed to the two readings being taken at different
  times; no file-level accounting is in the capture.
- 19M + 37M = 56M is arithmetic over three observed lines.
- The drop from the 269M recorded in `corpus/knowledge/journal-disk-usage-total-r51.md` (2026-10-24) to
  56M today is consistent with an eviction or a rebuild of the store, but the capture records no
  vacuum by the capturer, so the cause is not identified here.

## [UNKNOWN]

- Why the total fell from 269M to 56M within one day. Not observed; the capture ran no vacuum.
- The exact oldest retained file and its timestamp; the capture lists boots, not files.
- Whether any kill/OOM record was evicted; no query of record classes was made and none is claimed.
- Whether `/var/log/journal` holds per-namespace journals; not listed.
- Whether the runtime journal had already been flushed before the daemon's 8M line, or after it.
- Whether an unflushed volatile record of the previous boot survived its reboot; the volatile store's
  stated reach is the boot, and this capture does not contradict it.

## Not claimed

- No count of kills, OOM victims or events; this entry is about reach.
- No generalisation of 256M/64M or of 56M to any other host or any other day.
- No licence to vacuum, rotate, flush, signal journald or change any configuration; the lane reports.
- No claim that the committed copies match today's live pages; they are the 2026-10-25 copies.

## Decision row

For SKILL.md's decision table:

| situation | do | do not | source |
|---|---|---|---|
| a journal-derived count of kills is lower than a counter | report both readings with their scope and time; read the gap as a coverage/reach limit and say which part of the window is unobserved | report zero events, a corrected counter, or a cause (vacuum, rotation, rate limit) that was not observed | S485 archived-only size limits; S486 oldest-first vacuum and disk-usage total; `corpus/knowledge/journal-alarm-routing-r14.md:166,176` |
| a window predates the oldest retained record | report the window unavailable with the oldest retained entry/boot the journal still returns, and state the size cap and oldest-first eviction | report zero records or a complete window; run a vacuum, rotate, flush or config change to make room; read a config value as the effective cap without the daemon's own line | S486 oldest-first vacuum; S487 persistent/volatile split; S488 two-boot listing and daemon lines |

## What this changes for mori

- `corpus/knowledge/journal-disk-usage-total-r51.md`: a `--disk-usage` reading is a total over visible files; this entry adds that the total may sit above the cap while the oldest archived reach is what disappeared.
- `corpus/knowledge/journal-alarm-routing-r14.md:166,176`: the "vacuumed files / no retained record" class now has a named mechanism — a size cap and oldest-first deletion of archived files — so absence inside the reach is not zero events.
- `corpus/knowledge/oom-evidence-loss-r38.md`: the loss chain gains a store-layer link below the runtime: a record the kernel and runtime wrote can still be evicted by size before a query reaches it.
- `corpus/knowledge/retention-reconciliation-r22.md`: a retention reconciliation must state the window's reach; a count shortfall is a population question and never a clearance.
- `corpus/knowledge/journal-cursor-window-r16.md`: the retention UNKNOWN there becomes a rule here — an anchor older than the retained reach makes the window unavailable, and the refusal is the correct report.

## Registry note (for L1; not applied by this seat)

This entry's rows are S485 (journald.conf(5)), S486 (journalctl(1)), S487
(systemd-journald.service(8)) and S488 (the host receipt), all `mined`, opened 2026-10-25, listing this
entry in `used-by`. S486's `teaches` opens `supersedes S351 —`: the rejected S351 row's flip condition
(the public `--vacuum-size=` sentence from a committed copy plus a committed read-only disk-usage
receipt, and no `MESSAGE` grep) is met by the committed `journalctl.1.html` copy and S488. S351 stays a
rejected row.
````

## SOURCES rows the draft cites (for the L1; not written by this seat)

Each row is 11 cells (verified with the counter's `split_cells`). S488's source cell contains the literal
`own-work: host-journal-reach` because that string is the `COPIES` key the counter matches. S486's
`teaches` opens `supersedes S351 —`, as the frozen contract requires; S351 stays `rejected`.

````
| S485 | journald.conf(5) — https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html | docs | A | the journal service's own retention controls: the size-limit option group, MaxRetentionSec and its default, archived-only deletion, and the persistent requirement for per-user files; not this host's values (S488) and not journalctl's vacuum commands (S486) | Options, the SystemMaxUse=, SystemKeepFree=, SystemMaxFileSize=, SystemMaxFiles=, RuntimeMaxUse=, RuntimeKeepFree=, RuntimeMaxFileSize= and RuntimeMaxFiles= paragraph, MaxRetentionSec=, Storage=; systemd 262 page; committed copy corpus/evidence/sources-r49/journald.conf.5.html sha256 b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340 | The journal's reach is set by size limits that delete only archived files; MaxRetentionSec is a time limit that is off by default at 0; per-user journal files need persistent storage. | mined | 2026-10-25 | 180d | corpus/knowledge/journal-reach-r49.md |
| S486 | journalctl(1) — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | docs | A | the vacuum commands' order and scope and what --disk-usage sums; not the journald.conf size limits (S485) and not any measurement (S488) | Commands, --disk-usage and the --vacuum-size=, --vacuum-time= and --vacuum-files= paragraph; systemd 262 page; committed copy corpus/evidence/sources-r49/journalctl.1.html sha256 75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722 | supersedes S351 — the public --vacuum-size= sentence now rests on the committed copy plus the committed read-only receipt S488, with no MESSAGE grep; the vacuum removes the oldest archived files first and only archived files, while --disk-usage sums archived and active files. | mined | 2026-10-25 | 180d | corpus/knowledge/journal-reach-r49.md |
| S487 | systemd-journald.service(8) — https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html | docs | A | the service's two storage locations and their durability: persistent below /var/log/journal, volatile below /run/log/journal and lost at reboot, plus the automatic oldest-first removal; not the size limits (S485) and not this host's layout (S488) | Description, the paragraph beginning "The journal service stores log data either persistently" and the sentence "systemd-journald will automatically remove the oldest archived journal files"; systemd 262 page; committed copy corpus/evidence/sources-r49/systemd-journald.service.8.html sha256 a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212 | Journal data is either persistent below /var/log/journal or volatile below /run/log/journal and lost at reboot; the daemon itself removes the oldest archived files to limit disk use. | mined | 2026-10-25 | 180d | corpus/knowledge/journal-reach-r49.md |
| S488 | own-work: host-journal-reach — corpus/evidence/sources-r49/host-journal-reach.txt | own-work | A | this host only, read-only on 2026-10-25T20:43:09-03:00, kernel 7.2.11-arch1-1: total, system and user disk usage, the merged journald config, the limit drop-in's stat, /run and /run/log/journal state, the retained boots and the daemon's own boot lines; not any other host, not a vacuum or rotation receipt, and not a count of kills | receipt lines: journalctl --disk-usage (56M), --system (19M), --user (37M); systemd-analyze cat-config systemd/journald.conf; stat of /etc/systemd/journald.conf.d/size.conf; findmnt -no FSTYPE /run (tmpfs); ls -A /run/log/journal (empty, exit 0); journalctl --list-boots (two boots); journalctl -b 0 -u systemd-journald -g 'Journal .* is .*max' | On this host the journal total read 56M (19M system plus 37M user) against a 256M/64M drop-in, with two boots retained and an empty /run/log/journal directory on a tmpfs /run; the capture ran no vacuum, rotation or config change. | mined | 2026-10-25 | 90d | corpus/knowledge/journal-reach-r49.md |
````

## Per-row located-quote verification

Offsets are into the counter-normalised copy of that row's source; `unique=yes` means the span occurs
once in the table.

| # | source | claim words | quote words | normalise offset | unique |
|---|---|---|---|---|---|
| 1 | S485 | 15 | 8 | 9437 | yes |
| 2 | S485 | 13 | 22 | 13371 | yes |
| 3 | S485 | 15 | 10 | 13813 | yes |
| 4 | S485 | 13 | 16 | 11272 | yes |
| 5 | S485 | 12 | 18 | 5840 | yes |
| 6 | S485 | 14 | 12 | 4957 | yes |
| 7 | S486 | 16 | 18 | 25868 | yes |
| 8 | S486 | 14 | 24 | 25664 | yes |
| 9 | S486 | 15 | 13 | 26374 | yes |
| 10 | S487 | 14 | 13 | 12537 | yes |
| 11 | S487 | 12 | 17 | 1497 | yes |
| 12 | S487 | 9 | 9 | 1622 | yes |
| 13 | S487 | 14 | 20 | 1665 | yes |
| 14 | S488 | 9 | 11 | 191 | yes |
| 15 | S488 | 7 | 11 | 296 | yes |
| 16 | S488 | 7 | 11 | 399 | yes |
| 17 | S488 | 12 | 9 | 2878 | yes |
| 18 | S488 | 12 | 9 | 2757 | yes |
| 19 | S488 | 12 | 8 | 122 | yes |

## Touched surfaces

- Written: this report, `.ufo/waves/round-49/w1/Mo49ScribeEntryB.md`.
- Scratch: `.scratch/r49-Mo49ScribeEntryB/entry.md` (draft, sha256 `efa1b4bcc806bb403d418893f97089a3acbe5e8d14ae88b66cd20f2801ee878b`), `.scratch/r49-Mo49ScribeEntryB/receipts.txt`. The fixture repo and the normalised dumps were removed after the runs.
- Read-only: the four copies under `corpus/evidence/sources-r49/`, `corpus/SOURCES.md` (lines 1-20, 248-263), `SKILL.md:1-40,940-979`, five `corpus/knowledge/` entries, `.ufo/waves/round-49/contract.md`, `.ufo/waves/round-49/count-c2.py`, `.ufo/waves/round-49/assimilation/{collisions,staged-ids,reg-ids}`, and staged entries under `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/`.
- Not touched: `SKILL.md`, `SOURCES.md`, `corpus/`, `tools/`, `LOG.md`, `SCORECARD.md`, `QUALITY.md`, the frozen round-49 files, jj state, the git index. `git status --porcelain | grep -v '^?? \.scratch/'` shows only untracked wave bookkeeping and other seats' untracked reports — no ` M `, `A `, `D ` or `R ` line from this seat.

## Out of scope, correctly not done

- Entry not written into the lane and not committed; no gate re-run to decorate the report.
- No host reads: the only host evidence is the committed receipt. The `recheck:` line is a future pattern, not something I ran.
- No `journalctl --vacuum*`, `--rotate`, `systemctl`, flush or config change; no `sudo`.
- No tool installation (nothing was needed), so nothing to record under the tooling directive.
- No subagents.

## Artifact paths

- Report: `.ufo/waves/round-49/w1/Mo49ScribeEntryB.md`
- Draft (copyable): `.scratch/r49-Mo49ScribeEntryB/entry.md` — sha256 `efa1b4bcc806bb403d418893f97089a3acbe5e8d14ae88b66cd20f2801ee878b`
- Receipts (pins, gate lines, per-row offsets): `.scratch/r49-Mo49ScribeEntryB/receipts.txt`

## Findings

- **MED — F1: the receipt carries two system-journal sizes that do not agree.**
  `corpus/evidence/sources-r49/host-journal-reach.txt:97` (daemon boot line, 13:36:20:
  `System Journal … is 45M, max 256M`) vs `:8-9` (`journalctl --system --disk-usage`, 20:43:09: `19M`).
  The capture does not say which files each number counts, so it cannot distinguish a shrink from a
  different counting rule. My draft records both, marks the "start-of-boot snapshot" reading
  `[INFERENCE]`, and claims no explanation. A wave-2 reviewer should treat this as an open limit, not as
  loss evidence.
- **MED — F2: the flush conclusion is inference, not a receipt line.**
  `corpus/evidence/sources-r49/host-journal-reach.txt:83-87`: `findmnt -no FSTYPE /var/log/journal` exits
  1 with no output (proves "not a separate mount point", not "the directory exists and is persistent"),
  and `ls -A /run/log/journal` exits 0 with no output. The positive evidence for a persistent store is
  only the daemon line naming `/var/log/journal/MACHINE_ID` (`:97`). The draft marks the
  flushed-into-persistent reading `[INFERENCE]`; one `ls /var/log/journal/MACHINE_ID` capture would close
  it (not run — host reads are outside this seat's scope).
- **MED — F3: the four registry rows are absent at the freeze tip.**
  `corpus/SOURCES.md` at `0df17b7b` ends at `S484` (`wc -l` = 324), so `count-c2.py 0df17b7b` reports
  `failed=entry_absent` and any run against the landed tip without the rows will report `bad_rows`.
  Integration must land S485–S488 with the entry: 11 cells, `status=mined`, `opened=2026-10-25`,
  `used-by` containing `corpus/knowledge/journal-reach-r49.md`, and S488's source cell containing
  `own-work: host-journal-reach`.
- **LOW — F4: the staged entry invites a stronger reading than the host supports.**
  `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/runtime-journal-reach-is-the-boot-r49.md`
  (whole file) concludes the volatile store cannot contribute to a window, and notes this host's runtime
  directory holds no files. Both statements match the receipt, but the staged text does not mention the
  boot flush, so a reader can take "no files in `/run/log/journal`" as "the boot's records are gone".
  The round-49 draft separates the two: the volatile **copy** is empty, while both boots are still
  listed by the persistent store (`[INFERENCE]` on the flush mechanism).
- **LOW — F5: identifiers in the committed receipt copy.**
  `corpus/evidence/sources-r49/host-journal-reach.txt:91-97` keeps a host name and two 32-hex boot IDs;
  the machine id is already written as `MACHINE_ID`. My entry quotes only the `MACHINE_ID`-sanitised
  spans and no boot ID. The copy is committed evidence and not this seat's to change; noted so a hygiene
  pass can decide whether boot IDs belong in a committed copy.
- **LOW — F6: `claims=` is a row count, not a located count.**
  `count-c2.py:parse_claims/evaluate` counts table rows before validation and prints `claims` next to
  `located`; only when they agree (as here, 19/19) does `claims=N` mean "N located quotes". Worth knowing
  when reading a later receipt.
