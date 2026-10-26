# Round 49 w1 — Mo49ScribeEntryA (scribe): journal-reach entry draft + located-quote verification

Deliverable: a full draft of `corpus/knowledge/journal-reach-r49.md` and the four candidate
`corpus/SOURCES.md` rows S485-S488, with every quote re-checked against the four frozen copies.
Nothing was landed in the lane. The only line I wrote is this report (plus scratch under
`.scratch/r49-Mo49ScribeEntryA/`). Report author date 2026-10-25, at or after the lane tip cited below.

Lane revision read: HEAD `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (the freeze commit); the
contract's entering tip `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` is its ancestor
(`git merge-base --is-ancestor b3e3453d HEAD` exit 0). Working-tree bytes of
`corpus/evidence/sources-r49/*` equal the freeze-commit blobs (four byte-compares: yes).

## 1. Provenance opened

| source | committed copy | sha256 | equals `evidence/freeze-sha256.txt` |
|---|---|---|---|
| S485 journald.conf(5) | `corpus/evidence/sources-r49/journald.conf.5.html` | `b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340` | yes |
| S486 journalctl(1) | `corpus/evidence/sources-r49/journalctl.1.html` | `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722` | yes |
| S487 systemd-journald.service(8) | `corpus/evidence/sources-r49/systemd-journald.service.8.html` | `a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212` | yes |
| S488 own-work host receipt | `corpus/evidence/sources-r49/host-journal-reach.txt` | `be3952cb6fdac6d6ced15a9a0092447db80fe699221b8478970bb402a558eb12` | yes |

Each page's own `<title>` and the literal `systemd 262` were read in the copy, so the copies are the
262 man pages the rows name. Each copy contains one `<script` block and zero `<!--` blocks; the
counter's `normalise()` drops script/style/comment bodies, and section 3 shows no quote of mine
survives only there.

Read as candidates to correct, not as evidence (their receipts sit outside this lane, so no number
of theirs was reused): `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/`
`journal-effective-retention-r45.md`, `journal-reach-at-ceiling-r46.md`,
`runtime-journal-reach-is-the-boot-r49.md`.

Read in the lane: `corpus/SOURCES.md:248` (S351, `rejected`, flip sentence), `PROVINCE.md:9-16`
(the refuse line that makes journald configuration tsukuroi's), `corpus/knowledge/journal-disk-usage-total-r51.md`
(S470's `--disk-usage` sentence and its 269M reading), `corpus/knowledge/journal-alarm-routing-r14.md:166,176`,
`corpus/QUALITY.md:1079-1086` (rule 128).

## 2. Commands, outputs, exit codes

| # | command (cwd = lane unless noted) | output | exit |
|---|---|---|---|
| 1 | `sha256sum corpus/evidence/sources-r49/*` | the four digests in section 1 | 0 |
| 2 | `grep -n "S48[5-8]\|S351" corpus/SOURCES.md` | one hit, line 248, the S351 journalctl(1) row, status `rejected` — **no S485-S488 row exists at HEAD** | 0 |
| 3 | `grep -o '<title>[^<]*</title>'` + `grep -o 'systemd [0-9][0-9]*'` per copy | `journald.conf`, `journalctl`, `systemd-journald.service`; each `systemd 262` | 0 |
| 4 | counter `normalise()` over the four copies (imported from the frozen `count-c2.py`) | 22245 / 41288 / 13421 / 2963 chars | 0 |
| 5 | 16 candidate quotes screened against those normalised texts | all 16 located; 8-18 words each | 0 |
| 6 | `curl -s <conf page> \| grep -c SystemMaxUse` (live) | `5` | 0 |
| 7 | `grep -c SystemMaxUse` (committed copy) | `5` | 0 |
| 8 | `curl -s` the three pages into scratch, then `sha256sum` live vs committed | all three live pages byte-identical to the committed copies | 0 |
| 9 | `journalctl --disk-usage` / `--system` / `--user` (read-only re-read, 2026-10-25 ~21:43) | `56M` / `19M` / `37M`, same three sentences as the receipt | 0 |
| 10 | `journalctl --list-boots --no-pager` | boots `-1` and `0`; boot 0 last entry 21:43:40 | 0 |
| 11 | `ls -A /run/log/journal` (and `sudo -n` same) | no output | 0 |
| 12 | `findmnt -no FSTYPE /run` | `tmpfs` | 0 |
| 13 | frozen counter on the fixture, final draft (section 4) | `C2=met claims=13 located=13 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=e4d0c36f140a118642f23250f54403d6732c6d05` | 0 |
| 14 | frozen counter on the fixture, only S485-S488 deleted (negative control) | `C2=unmet claims=13 located=0 quote_missing=0 bad_rows=13 sources=0 source_rows=bad pins=ok provenance=ok rev=f7165f0c304bddccb676453ba329e7db19e213be failed=bad_rows,source_rows,sources_floor` | 1 |
| 15 | `git status --porcelain \| cut -c1-2 \| sort \| uniq -c` | `177 ??` — every lane change is untracked, **no tracked path modified** | 0 |

## 3. Quote location — every row, checked twice

Checked with the counter's own `normalise()`, then again against the script/style/comment bodies
extracted from each raw copy, and scanned for negation tokens (rule 128's "no negation or example
context"):

| row | source copy | quote words | located in counter `normalise()` | occurs inside script/style/comment body | negation token in quote |
|---|---|---|---|---|---|
| 1 | journald.conf.5.html | 15 | yes | no | no |
| 2 | journald.conf.5.html | 16 | yes | no | no |
| 3 | journald.conf.5.html | 15 | yes | no | no |
| 4 | journalctl.1.html | 15 | yes | no | no |
| 5 | journalctl.1.html | 17 | yes | no | no |
| 6 | journalctl.1.html | 9 | yes | no | no |
| 7 | systemd-journald.service.8.html | 17 | yes | no | no |
| 8 | systemd-journald.service.8.html | 9 | yes | no | no |
| 9 | systemd-journald.service.8.html | 12 | yes | no | no |
| 10 | systemd-journald.service.8.html | 12 | yes | no | no |
| 11 | host-journal-reach.txt | 11 | yes | no | no |
| 12 | host-journal-reach.txt | 9 | yes | no | no |
| 13 | host-journal-reach.txt | 9 | yes | no | no |

The script also confirmed for every row: 3 cells, claim cell at least 5 words, exactly one
backticked span, quote unique in the table, 6 <= words <= 25, and 4 distinct sources.
Balances: 3 rows journald.conf(5), 3 journalctl(1), 4 systemd-journald.service(8), 3 host receipt.

Raw-context spot check (the quote's opening words as they sit in the raw copy, tags intact), showing
each quote is body prose rather than script text:

- row 2: `The options prefixed with "<code class="literal">System</code>" apply to the journal files when stored o…`
- row 3: `…href="#MaxRetentionSec=">¶</a></dt><dd><p>The maximum time to store journal entries. This controls whether journal files cont…`
- row 5: `…<code class="option">--vacuum-size=</code> removes the oldest archived journal file…`
- row 7: `…may be up to 2⁶⁴-1 bytes in size.</p><p>The journal service stores log data eith…`
- row 13: `…journalctl -b 0 -u systemd-journald --no-pager -q -g 'Journal .* is .*max' Oct 25 13:36:19 … runtime Journal (/run/log/journal/MACHIN…`

Row 1's opening words span a `<code>` boundary in the raw copy (`SystemMaxUse=` is a `<code class="option">`
element), so its raw-context probe is empty by construction; its location is the `normalise()` hit,
which is what the counter scores. It is list-item prose in the Options section, not script text.

## 4. Counter run — the frozen predicate scores the draft met (fixture, not the lane tip)

Rules followed for the fixture, per the seat's fixture rule:

```
D=$(mktemp -d)          # /tmp/tmp.zJ2iCFmuGE
git -C "$D" init -q
git -C "$D" rev-parse --show-toplevel   -> /tmp/tmp.zJ2iCFmuGE   (verified before the first commit)
```

D contents: `corpus/SOURCES.md` = the lane's own `SOURCES.md` bytes with the four candidate rows
inserted after line 263 (`| S484 |`), so the registry table continues; `corpus/evidence/sources-r49/*`
= the four committed copies (byte-identical, pins `ok`); the draft at the canonical path
`corpus/knowledge/journal-reach-r49.md`. Commits used a throwaway identity only inside $D
(`git -C "$D" -c user.name=... -c user.email=... commit`); no commit was made anywhere else.

Final run (draft sha256 `a99683b2586636366475d7691c962625740d0ef26e1206deec850ae254ab917b`, rows sha256 `12e3bdff3b9217ac63917c871f9ff075e298bc457deaac909229c2d56aa0faac`):

```
$ TMPDIR=.scratch/r49-Mo49ScribeEntryA python3 .ufo/waves/round-49/count-c2.py HEAD --repo "$D"
C2=met claims=13 located=13 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=e4d0c36f140a118642f23250f54403d6732c6d05
exit=0
```

Negative control: a commit on the same fixture branch after the final one, whose only change is the
deletion of the four S485-S488 rows (`git -C "$D" show --stat f7165f0` -> `1 file changed, 4 deletions(-)`,
and `git -C "$D" show f7165f0 -- corpus/SOURCES.md` lists exactly those four rows as removed). The
counter resolves it by SHA even though the fixture branch was reset back to the final commit to keep
the `met` state reproducible:

```
$ TMPDIR=.scratch/r49-Mo49ScribeEntryA python3 .ufo/waves/round-49/count-c2.py f7165f0c304bddccb676453ba329e7db19e213be --repo "$D"
C2=unmet claims=13 located=0 quote_missing=0 bad_rows=13 sources=0 source_rows=bad pins=ok provenance=ok rev=f7165f0c304bddccb676453ba329e7db19e213be failed=bad_rows,source_rows,sources_floor
exit=1
```

What this shows, and what it does not. It shows the draft plus these four rows satisfy P-C2's
mechanical arms — head lines, table header and floor, one located quote per row, unique quotes,
4 distinct sources, row status/opened/used-by, the provenance binding — and that `met` depends on
the rows (deleting them flips the same entry to `unmet`). It does **not** measure the lane tip: at
HEAD the entry is absent (command 2), so the lane itself cannot print `C2=met` until the L1 lands the
entry and the rows. The fixture rev strings above are fixture commits, not lane commits.

## 5. Freshness and host re-reads (read-only)

- All three man pages re-fetched on 2026-10-25 were byte-identical to the committed copies
  (`journald.conf` `b4a9b53e…`, `journalctl` `75440570…`, `systemd-journald.service` `a7b44356…`).
  That is a fact about today and it is why the entry's `recheck:` line carries a sha256 comparison
  for each of the three pages, not only the `grep -c` count.
- The host still reports `56M` / `19M` / `37M` and the same two boots about an hour after the
  receipt's capture; the receipt remains a faithful reading of a store that is not moving at the
  moment I looked. `ls -A /run/log/journal` is empty for me too (exit 0), which confirms the
  receipt's empty listing was not a truncated capture.

## 6. Draft — `corpus/knowledge/journal-reach-r49.md`

```md
# The journal's reach is a size ceiling plus a boot boundary, and a missing record is not a zero

source: S485 — https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html — journald.conf(5), docs, tier A, systemd 262 page; copy corpus/evidence/sources-r49/journald.conf.5.html; opened 2026-10-25
source: S486 — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — journalctl(1), docs, tier A, systemd 262 page; copy corpus/evidence/sources-r49/journalctl.1.html; opened 2026-10-25
source: S487 — https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html — systemd-journald.service(8), docs, tier A, systemd 262 page; copy corpus/evidence/sources-r49/systemd-journald.service.8.html; opened 2026-10-25
source: S488 — own-work: host-journal-reach — this host's journal reach, read-only capture 2026-10-25T20:43:09-03:00; copy corpus/evidence/sources-r49/host-journal-reach.txt; tier A
verified-at: 2026-10-25
recheck: 90d — `curl -s https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html | grep -c SystemMaxUse` -> 5; `curl -s https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | sha256sum` -> 75440570…; `curl -s https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html | sha256sum` -> a7b44356… (all three ran 2026-10-25, and all three live pages were byte-identical to the committed copies); `journalctl --disk-usage` -> 56M (ran 2026-10-25; a moved total is the limit, not a failure)
coverage-map: FR1 evidence reach — how far back the journal records mori reads can go, and what an absent record is
ground: frontier item **FR1** — "Kernel OOM event-time attribution and fleet correlation"; boundary: "No raw `MESSAGE` is emitted, and a host record alone does not prove a fleet-caused kill." This entry supplies the retention rule behind that boundary; it attributes nothing.

### What reach means here

Reach is how far back a mori read of the journal can look. On the evidence below it is
two bounds of different kinds, not one age limit. The **persistent** store is bounded by
**size**: the use limits cap the disk space the journal may occupy, and the vacuum order
takes the **oldest** archived files first, so a store at its ceiling is always the store
that has lost its oldest history. The **volatile** store is bounded by the **boot**: its
data is lost at reboot, so it cannot serve a window that spans one. Time-based deletion
exists as a third, separate control and is not what sets the reach measured here.

A mori journal read is a read of what the store still retains. That fixes the rule this
entry exists for: **an absent record is unavailable, not a zero.** A count of zero over a
window says the store held no matching record when the window was read; the event may have
been evicted at the ceiling oldest-first, may have lived only in a volatile store of an
earlier boot, or may predate the retained set. The lane already carries that reading for
alarms — `corpus/knowledge/journal-alarm-routing-r14.md:166,176` refuses "vacuumed" as a
zero — and this entry supplies the rule that decides where the retained set begins.

### This host, captured read-only on 2026-10-25

The capture is `corpus/evidence/sources-r49/host-journal-reach.txt` (2026-10-25T20:43:09-03:00,
kernel 7.2.11-arch1-1, no vacuum, rotation or configuration change run). Everything numeric
below is that day's capture, not a standing value:

- Disk usage, as the three scopes reported it: **56M** total, **19M** for `--system`,
  **37M** for `--user`.
- Merged configuration: the drop-in `/etc/systemd/journald.conf.d/size.conf` (46 bytes,
  mtime 2026-10-16) sets `SystemMaxUse=256M` and `RuntimeMaxUse=64M`; the main file holds
  the commented compile-time defaults, `MaxRetentionSec` among them at `0`.
- The daemon's own boot lines (boot 0, 13:36:19): runtime journal is **8M, max 64M**, and
  the system journal is **45M, max 256M** with **210.9M free**.
- Two boots are listed: `-1` from 2026-10-24 20:57:12 to 2026-10-25 13:35:39, and `0` from
  2026-10-25 13:36:19. One earlier boot is therefore retained, which is the reach the
  current ceiling is producing.
- `/run` is `tmpfs`, and `/var/log/journal` is **not** a separate mount (`findmnt` exit 1),
  so the persistent store's reach is the ceiling above and not a mount lifetime.
- `ls -A /run/log/journal` printed nothing and exited 0: the volatile directory held no
  files at capture. The service page records that the daemon starts on volatile storage and
  moves to persistent after a flush, and the page says that flush is done automatically at
  boot; the receipt does not record the flush, so this entry reports the empty listing and
  not a cause for it.

Two readings must not be collapsed. The capture's boot line reports the **system** journal
at 45M while the same capture's later `--system --disk-usage` reports 19M. Both are as
captured; the receipt does not explain the movement, so neither is quoted as the other.
The same caution applies across days: the lane's earlier entry (`journal-disk-usage-total-r51.md`,
S470) recorded **269M** on 2026-10-24, this capture records **56M**. Reach is a moving
target read per capture, which is why the table's host rows say "that day's capture".

### The rule, claim by claim

| claim | source | quote |
|---|---|---|
| The two use limits control the most disk space the stored journal may occupy. | S485 | `SystemMaxUse= and RuntimeMaxUse= control how much disk space the journal may use up at most.` |
| Runtime-prefixed options govern the journal stored on the volatile in-memory file system below /run/log/journal. | S485 | `apply to the journal files when stored on a volatile in-memory file system, more specifically /run/log/journal` |
| Time-based deletion is a third bound: it deletes journal files whose entries are older than a configured span. | S485 | `This controls whether journal files containing entries older than the specified time span are deleted.` |
| The disk-usage reading is a sum over archived and active journal files, so it is a total. | S486 | `This shows the sum of the disk usage of all archived and active journal files.` |
| A size vacuum takes the oldest archived files until the store falls below the requested size. | S486 | `removes the oldest archived journal files until the disk space they use falls below the specified size` |
| A time vacuum takes archived journal files older than the requested span. | S486 | `removes archived journal files older than the specified timespan` |
| The service stores persistent data below /var/log/journal and volatile data below /run/log/journal. | S487 | `The journal service stores log data either persistently below /var/log/journal or in a volatile way below /run/log/journal/` |
| Volatile store contents are lost at reboot, so their reach ends with the boot. | S487 | `in the latter case, it is lost at reboot` |
| Persistent storage is the default placement when /var/log/journal/ exists during boot. | S487 | `By default, log data is stored persistently if /var/log/journal/ exists during boot` |
| The daemon starts on volatile storage and moves to persistent storage after a flush call. | S487 | `journald will initially use volatile storage, until a call to journalctl --flush` |
| That day's capture: the reported journal disk usage was 56M in the file system. | S488 | `Archived and active journals take up 56M in the file system.` |
| That day's capture: the daemon reported the system journal at 45M against a 256M ceiling. | S488 | `System Journal (/var/log/journal/MACHINE_ID) is 45M, max 256M, 210.9M free.` |
| That day's capture: the daemon reported the runtime journal at 8M against a 64M ceiling. | S488 | `Runtime Journal (/run/log/journal/MACHINE_ID) is 8M, max 64M, 56M free.` |

### Limits

- A located quote proves the words exist in the committed copy. It does not prove the copy
  is today's page, and it does not prove a claim beyond what the quoted sentence says. The
  three man-page copies were re-fetched on 2026-10-25 and were byte-identical to the
  committed copies; that equality is a fact about that day.
- The host rows are one capture. The total moved 269M -> 56M between the lane's 2026-10-24
  reading and this one, so no host row is a standing value, and no row states when the
  store will next evict.
- The reach figures describe this host only. Another host's drop-in or mount layout sets a
  different reach, and nothing here is observable from another machine.
- 19M + 37M equals the 56M total in this capture; that arithmetic is consistency of one
  capture, not a per-scope guarantee, and the manual's own sentence is why: a `--disk-usage`
  total is what the invocation can see.

### Boundaries

- **Detection and report only.** This entry reports reach as evidence-loss context for mori
  reads. No `journalctl --vacuum-size`, `--vacuum-time`, `--vacuum-files` or `--rotate` was
  run, and none is recommended here; no configuration was written, and no service was
  signalled or restarted.
- **journald configuration is not this lane's.** Per `PROVINCE.md`, OS package, systemd
  unit, driver/firmware and boot state belong to tsukuroi; mori reads journal events as
  fleet evidence. The drop-in named above is reported as it was read, not advised on.
- A missing record is evidence of a retained set's boundary, never of an event that did not
  happen, and never a zero that a fleet count may be summed with.
```

## 7. Draft — `corpus/SOURCES.md` rows S485-S488 (insert after `| S484 |`, currently line 263)

```md
| S485 | journald.conf(5) — https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html | docs | A | journal store size limits, time-based retention, and the persistent-versus-volatile option split | Options: Storage=; SystemMaxUse=, SystemKeepFree=, SystemMaxFileSize=, SystemMaxFiles=, RuntimeMaxUse=, RuntimeKeepFree=, RuntimeMaxFileSize=, RuntimeMaxFiles=; MaxRetentionSec=; systemd 262 page, copy corpus/evidence/sources-r49/journald.conf.5.html sha256 b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340, opened 2026-10-25 | The use limits are the default size bound on the stored journal, the Runtime-prefixed options address the volatile hierarchy, and time-based deletion is a separate control. | mined | 2026-10-25 | 90d | corpus/knowledge/journal-reach-r49.md |
| S486 | journalctl(1) — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | docs | A | vacuum order and scope, and what a --disk-usage total covers | Commands: --disk-usage; --vacuum-size=, --vacuum-time=, --vacuum-files=; systemd 262 page, copy corpus/evidence/sources-r49/journalctl.1.html sha256 75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722, opened 2026-10-25 | supersedes S351 — the public --vacuum-size= and --disk-usage sentences from the committed copy plus the committed read-only host receipt, and no MESSAGE grep; reach is stated from the retention rule the vacuum order implies. | mined | 2026-10-25 | 90d | corpus/knowledge/journal-reach-r49.md |
| S487 | systemd-journald.service(8) — https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html | docs | A | where journald stores data, the volatile-versus-persistent placement default, and the boot flush | Description: storage placement paragraph and the journalctl --flush switch; systemd 262 page, copy corpus/evidence/sources-r49/systemd-journald.service.8.html sha256 a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212, opened 2026-10-25 | Persistent placement bounds reach by size while the volatile placement's reach is the boot, and the daemon starts volatile until the boot flush switches it. | mined | 2026-10-25 | 90d | corpus/knowledge/journal-reach-r49.md |
| S488 | own-work: host-journal-reach — corpus/evidence/sources-r49/host-journal-reach.txt | own-work | A | this host only, read-only on 2026-10-25: journal disk usage per scope, the merged journald drop-in, the daemon's boot limits, the boot list and the volatile directory listing; no other host and no config change | receipt lines for the three --disk-usage calls, systemd-analyze cat-config journald.conf, stat of size.conf, findmnt of /run and /var/log/journal, ls -A /run/log/journal, journalctl --list-boots and the two daemon limit lines; capture 2026-10-25T20:43:09-03:00, kernel 7.2.11-arch1-1 | That day's capture: the store measured 56M in total, split 19M system and 37M user, against a 256M system and 64M runtime ceiling from the drop-in, with one earlier boot retained and no files in the volatile directory. | mined | 2026-10-25 | 30d | corpus/knowledge/journal-reach-r49.md |
```

`S486`'s `teaches` cell opens `supersedes S351 — `, which is the C2 flip: the public
`--vacuum-size=` / `--disk-usage` sentences from the committed copy plus the committed read-only
receipt, and no MESSAGE grep. `S351` itself stays `rejected` and is not edited.

## 8. Out of scope / not done

- Nothing landed: no edit to `SKILL.md`, `SOURCES.md`, `corpus/`, `tools/`, `LOG.md`, `SCORECARD.md`,
  the frozen `.ufo/waves/round-49` files, or anything else in the lane. Command 15 shows no tracked
  change.
- No git/jj mutation in the lane; only `rev-parse`, `log`, `merge-base`, `status`, `show`, `diff` and
  in-fixture commits.
- No host action: no vacuum, rotate, `systemctl`, signal, or configuration write. `journalctl
  --disk-usage`, `--list-boots`, `findmnt`, `ls -A` and `sudo -n ls` are reads.
- No tool installed or upgraded (nothing was needed).
- I did not run `count-c2.py --selftest` (not my seat's work) and I did not score C1.
- Read-only elsewhere: `/home/vgpnk/Projects/shokuknow/**` was opened for bytes only, nothing run there.

## 9. UNVERIFIED

- Why the volatile directory is empty while the daemon reported an 8M runtime journal at boot:
  UNVERIFIED. The entry reports the empty listing and the manual's flush sentence, and states no cause.
- Why the persistent store reads 19M at 20:43 after the boot line said 45M: UNVERIFIED. The entry
  quotes both as captured and refuses to equate them.
- Whether the journal total will stay at 56M: not knowable from one capture; the entry says so.
- Claim/quote entailment beyond the quoted sentence, and whether "latest" keeps serving systemd 262:
  reviewer/wave-2 work, not verifiable here.

## Findings

- **MED** — `corpus/evidence/sources-r49/host-journal-reach.txt:97` vs `:9`: the same capture reports
  the system journal at `45M` in the daemon's boot line and at `19M` in the later
  `journalctl --system --disk-usage`. The receipt records no cause and the two are not the same
  quantity; the draft therefore quotes each verbatim and says neither is the other. Any later entry that
  transcribes this receipt must not collapse them (the staged r45 entry's single "243.6M" number shows
  the failure mode).
- **MED** — the staged entries under `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/`
  carry host numbers this lane cannot reproduce from its own receipt: `journal-effective-retention-r45.md:16,26-28`
  has the system journal at 243.6M inside a store of 250.3M against a 256M ceiling and six boots
  retained, and `journal-reach-at-ceiling-r46.md:25-27` has 258.3M against the same ceiling with six
  boots. This capture has the system journal at 45M inside a 56M total against the same 256M drop-in,
  with two boots. `runtime-journal-reach-is-the-boot-r49.md:16-19` agrees with this capture on the
  256M/64M ceilings and on the empty volatile directory, so the divergence is confined to the r45/r46
  size and boot counts. The draft adopts the rule and none of their numbers; an integrator that
  transcribes those numbers instead would publish stale host facts under a 2026-10-25 `verified-at`.
- **LOW** — `corpus/evidence/sources-r49/host-journal-reach.txt:86-88`: the `ls -A /run/log/journal`
  step records no output and does not show the directory was the parent (not
  `/run/log/journal/<machine-id>`), and the capture's boot line at `:96` says the runtime journal held
  8M. A reader can take the empty listing as "the volatile store was never written". I re-ran the
  listing read-only (empty, exit 0) and the draft states the listing without a cause; a future receipt
  should list the machine-id subdirectory and record the `systemd-journal-flush.service` state.
- **LOW** — `host-journal-reach.txt:96-97` prints the host name `plazir27` and full boot IDs. Not
  credential material, and the machine id was already substituted to `MACHINE_ID`; noted only so the
  2026-10-25 receipt's identifiers are not carried into an entry unexamined.
- **LOW** — lane root residue observed while reading: `--repo/` (empty directory, mtime 2026-10-24) and
  a 31-byte file named `0` (content `NF=13 cells=11 double_quotes=0`) are untracked at
  `/home/vgpnk/Projects/shokunin/mori-shokunin/`. `git status --porcelain` reports `177 ??` entirely
  untracked, dominated by `.scratch/` and `.ufo/waves/round-40/scratch/`; the count moved 180 -> 177
  between two of my checks while sibling seats cleaned. Cleanup is the hygiene seat's, not mine.
- **LOW** — the draft's prose sentence comparing 269M (2026-10-24) with 56M (this capture) depends on
  `corpus/knowledge/journal-disk-usage-total-r51.md` (S470), not on S488. It is attributed in the
  sentence; if that entry is re-pointed, the sentence must move with it.
- **LOW** — `corpus/QUALITY.md:1082-1084` requires a reviewer to re-open every row against the page
  text around its quote, and the counter cannot check entailment, negation context or example context.
  My rows pass the located/uniqueness/negation-token checks I could run; entailment remains wave 2's
  check, and the counter's receipt cannot be read as having made it.
