# w1 seat — Mo49ExecQuotesHost: host-receipt quote inventory + live comparison

Seat: `Mo49ExecQuotesHost` (leaf, mori round 49, wave w1). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Work done 2026-10-25 between 21:41:37 and 21:43:00 -03. Read-only host access only; no vacuum, rotate,
`systemctl`, or config change was run. No lane file was edited except this report; scratch is under
`.scratch/r49-Mo49ExecQuotesHost/` (listed in §7).

Inputs and pins (verified before any quote work):

```
$ sha256sum corpus/evidence/sources-r49/host-journal-reach.txt
be3952cb6fdac6d6ced15a9a0092447db80fe699221b8478970bb402a558eb12  corpus/evidence/sources-r49/host-journal-reach.txt
```

`be3952cb…` is the digest `count-c2.py` freezes for `own-work: host-journal-reach` (counter lines 36-45), so
the host receipt the entry may quote is byte-identical to the frozen copy. Same check passed for the three
pages (`b4a9b53e…` journald.conf.5, `a7b44356…` systemd-journald.service.8, `75440570…` journalctl.1).
`git -C <lane> rev-parse HEAD` = `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` = the contract's freeze commit
(the entering tip `b3e3453d` is its parent).

Method: I imported the frozen counter (read-only `importlib` load, no edit) and applied its own
`normalise()` — drop `script`/`style` blocks, drop `<!-- -->`, strip tags, `html.unescape`, collapse
whitespace (`re.sub(r"\s+", " ", t)`) — then took the counter's exact acceptance rule for a quote cell:
one backticked span, `6 <= words <= 25` on `q.split(" ")`, unique in the table, and `q in norm[source]`.
The receipt is plain text: `tag_count=0 script_count=0 comment_count=0`, so normalisation there is
whitespace collapse only and no quote can ride on tag-stripping (the round-48 survivor). Script is
`.scratch/r49-Mo49ExecQuotesHost/verify_quotes.py` + `verify_repairs.py`; runs and exit codes are in §1-§2.

## 1. Quote inventory — ten verified spans from `host-journal-reach.txt`

All ten were located by substring test in the normalised frozen copy and pass the counter's word and
uniqueness rules (`verify_quotes.py`, `verify_repairs.py`, `rc=0`). They are all from the receipt, i.e.
they can ground only rows whose source cell is the own-work receipt row (S488 in the planned numbering).

| # | quote (this is the exact cell content) | w | located | claim it supports | what it does **not** support |
|---|---|---|---|---|---|
| Q1 | `Archived and active journals take up 56M in the file system.` | 11 | yes | the whole-store footprint at capture: archived + active, system + user, is 56M | not a per-journal or per-boot share (S470 already says the sum is over files the command can see); not a ceiling; not an age; not a value that holds on another day |
| Q2 | `Archived and active journals take up 19M in the file system.` | 11 | yes | the *system* store's share of the total is 19M, so the persistent system journal alone is well under its 256M cap | not the runtime store's size; not that the 19M is all from this host's system unit (the store also holds an empty `remote/` directory — see §3); not stable |
| Q3 | `Archived and active journals take up 37M in the file system.` | 11 | yes | the *user* journals are 37M — about two thirds of the 56M — so a user-scope read has the larger share and any total must say which scope it measured | not that user journals are volatile (they are `user-1000*.journal` under `/var/log/journal/MACHINE_ID`, observed live); not per-user attribution beyond what the receipt shows (it shows one scope total, no uid) |
| Q4 | `System Journal (/var/log/journal/MACHINE_ID) is 45M, max 256M, 210.9M free.` | 9 | yes | the effective system ceiling at boot was 256M — i.e. the drop-in is loaded, not a compile-time default — and the system store had 210.9M headroom | not that 45M is the current size (live `--system --disk-usage` = 19M, §3); not the retention age; not the vacuum order; not the file granularity; the `45M`/`210.9M` are a boot-time snapshot |
| Q5 | `Runtime Journal (/run/log/journal/MACHINE_ID) is 8M, max 64M, 56M free.` | 9 | yes | the effective runtime ceiling at boot was 64M (again the drop-in, not a default), and the runtime store held 8M then | not that the runtime store still holds 8M (live listing is empty, §3); not that runtime records are reachable now; not a floor on runtime reach |
| Q6 | `tmpfs [exit 0] $ findmnt -no FSTYPE /var/log/journal` | 8 | yes | `/run` is a tmpfs, and `/var/log/journal` is not itself a mountpoint | not that the runtime journal is *in use* (needs the unit/`Storage=` row); not that the persistent store is on the root filesystem — live `findmnt -T /var/log/journal` shows the btrfs subvolume `root[/@log]` mounted at `/var/log` (§3); not that journals survive reboot (that is the page's `Storage=` text plus the directory's existence) |
| Q7 | `$ ls -A /run/log/journal [exit 0]` | 6 | yes | at the capture the volatile store held no files, and the `ls` itself exited 0 (an empty directory, not a failed read) | not that journald never wrote there (Q5 shows 8M at boot); not that no runtime record exists earlier in the boot; not that runtime records are absent from the 56M total |
| Q8 | `/etc/systemd/journald.conf.d/size.conf 46 bytes mtime 2026-10-16 11:53:47.069871418 -0300` | 7 | yes | the ceiling is local configuration: a drop-in file of 46 bytes last written 2026-10-16, i.e. not a compile-time default and not changed since | not the file's *content* (that is Q9/DROP-b); not that the file is currently effective (only Q4/Q5's `max` values show that); an mtime is not a load time |
| Q9 | `#SystemMaxUse= #SystemKeepFree= #SystemMaxFileSize= #SystemMaxFiles=100 #RuntimeMaxUse= #RuntimeKeepFree= #RuntimeMaxFileSize= #RuntimeMaxFiles=100 #MaxRetentionSec=0` | 9 | yes | the shipped `/etc/systemd/journald.conf` leaves every size and retention key commented out, and its compile-time default for `MaxRetentionSec` is `0` — so no age limit is configured there and retention is size-governed | not the effective values (these are commented defaults; the drop-in overrides two of them); not that `0` means "no limit" (that needs the journald.conf(5) `MaxRetentionSec=` row); not any runtime value |
| Q10 | `Sat 2026-10-24 20:57:12 -03 Sun 2026-10-25 13:35:39 -03` | 8 | yes | the previous boot is still fully present, from 2026-10-24 20:57:12 to 2026-10-25 13:35:39, so the reach at capture was at least two boots / about one day | not a retention limit (56M against a 256M cap, so the cap is not what bounds reach); not the entry count; not stable — it is boot `-1`'s fixed range, but the current boot's row and the whole list move (§4) |

Quotes Q1-Q3 differ only in the size token and Q4/Q5 only in scope: the counter's uniqueness rule is on the
whole span, so they coexist, but an entry that used all three size quotes would be spending three rows on
one volatile observable. Recommended pick from this set for the S488 row(s): **Q4 or Q5** (ceiling is
effective), **Q6 + Q7** (volatile store is separate and currently empty), **Q8 + Q9** (the ceiling is a
local drop-in, not a default), **Q10** (reach is two boots), with at most one of Q1-Q3 for the footprint.

## 2. Rejected spans and their lawful repairs (falsifiers for the entry author)

Every line below was tested with the same normalise + word/duplicate rule; `verify_quotes.py` and
`verify_repairs.py`, `rc=0`.

| probe | span | w | located | verdict | why |
|---|---|---|---|---|---|
| NEG-1 | `SystemMaxUse=256M` | 1 | yes | REJECT | the assignment's named "drop-in `SystemMaxUse=256M`" cannot be a quote by itself: below the 6-word floor |
| NEG-2 | `# /etc/systemd/journald.conf.d/size.conf [Journal] SystemMaxUse=256M RuntimeMaxUse=64M` | 5 | yes | REJECT | the whole drop-in stanza, leading comment included, is still 5 words: below the floor |
| DROP-b | `# /etc/systemd/journald.conf.d/size.conf [Journal] SystemMaxUse=256M RuntimeMaxUse=64M [exit 0]` | 7 | yes | PASS | smallest span that carries both directives; costs the harness exit marker |
| DROP-c | `#Audit=yes # /etc/systemd/journald.conf.d/size.conf [Journal] SystemMaxUse=256M RuntimeMaxUse=64M` | 6 | yes | PASS | alternative repair: absorb the last default line instead of the exit marker (noisier, mixes two stanzas) |
| NEG-3 | `tmpfs $ findmnt -no FSTYPE /var/log/journal` | 6 | **no** | REJECT | the printed `[exit 0]` sits between `tmpfs` and the next `$`; any span crossing a command boundary **must** include the marker (repair: Q6) |
| NEG-4 | `Runtime Journal (/run/log/journal/<32-hex>) is 8M, max 64M, 56M free.` with a real 32-hex id | 9 | **no** | REJECT | the frozen copy masks the id as `MACHINE_ID`; a span pasted from a live run is not located. Probed with a synthetic id, not the host's |
| NEG-5 | `Archived and active journals take up 56M in the file system. [exit 0]` | 13 | yes | PASS but noisy | legal; prefer Q1 without the marker |
| POS-1 | boot row typed single-spaced (`0 <bootid> Sun 2026-10-25 13:36:19 -03 ...`) | 10 | yes | PASS | the receipt's column padding is collapsed by `normalise`, so single spaces are correct |
| POS-2 | a quote wrapped across two source lines | 11 | yes | PASS | counter collapses `\s+`, but an entry table row is one line, so a span with a newline cannot be written into a cell |
| POS-3 | `$ journalctl --disk-usage Archived and active journals take up 56M in the file system. [exit 0]` | 16 | yes | PASS | legal; mixes a command and its output |

## 3. Live re-run of the same read-only commands (2026-10-25 21:41:37 -03, kernel 7.2.11-arch1-1)

I re-ran exactly the receipt's commands (plus `findmnt -T` and store listings, read-only) through
`.scratch/r49-Mo49ExecQuotesHost/live_capture.sh` into `live.txt` (`capture_rc=0`). The committed receipt
was not touched.

| observable | receipt (20:43:09) | live (21:41-21:42) | changed |
|---|---|---|---|
| `journalctl --disk-usage` | `56M` | `56M` (`rc=0`) | no |
| `journalctl --system --disk-usage` | `19M` | `19M` (`rc=0`) | no |
| `journalctl --user --disk-usage` | `37M` | `37M` (`rc=0`) | no |
| boots listed | 2 (`-1`, `0`) | 2 (`-1`, `0`) | no |
| boot `-1` range | Oct 24 20:57:12 → Oct 25 13:35:39 | identical | no (boot ended) |
| boot `0` first entry | Oct 25 13:36:19 | Oct 25 13:36:19 | no |
| boot `0` **last entry** | Oct 25 20:43:03 | **Oct 25 21:42:45** | **yes** |
| boot `0` entry count | 9677 (`--until '2026-10-25 20:43:09' \| wc -l`) | 12675 (`wc -l`) | **+2998 in 59m** |
| boot `-1` entry count | 60463 (fixed) | 60463 | no |
| `systemd-analyze cat-config systemd/journald.conf` | defaults + `size.conf` block | byte-identical (`rc=0`) | no |
| `stat size.conf` | `46 bytes mtime 2026-10-16 11:53:47.069871418 -0300` | identical (`rc=0`) | no |
| `findmnt -no FSTYPE /run` | `tmpfs` | `tmpfs` (`rc=0`) | no |
| `findmnt -no FSTYPE /var/log/journal` | empty, `[exit 1]` | empty, `rc=1` | no |
| `ls -A /run/log/journal` | empty | empty, `rc=0` | no |
| journald limit lines (`-b 0 -g 'Journal .* is .*max'`) | `8M, max 64M, 56M free` / `45M, max 256M, 210.9M free` | identical (`rc=0`) | no |

Extra read-only measurements (not in the receipt, so **not** quotable in the entry):

```
$ sudo -n ls -la /var/log/journal/*/ | sed 's/[0-9a-f]\{32\}/MACHINE_ID/g'
./MACHINE_ID/:
-rw-r-----+ 16777216 Oct 25 13:36 system@MACHINE_ID-…-00065ea0061764c1.journal
-rw-r-----+  8388608 Oct 25 21:42 system.journal
-rw-r-----+ 16777216 Oct 24 22:42 user-1000@MACHINE_ID-…-00065e9edb0552dd.journal
-rw-r-----+ 16777216 Oct 25 03:11 user-1000@MACHINE_ID-…-00065ea0533f96da.journal
-rw-r-----+ 16777216 Oct 25 21:43 user-1000.journal
./remote/:   total 0        # empty; owned by systemd-journal-remote, mtime Oct 3 17:41
system bytes=25165824 (24.0 MiB)   user bytes=50331648 (48.0 MiB)   # apparent size, 5 files
$ journalctl -b 0 -u systemd-journald -q -g 'Flushing|flush|Rotat|rotat|vacuum'
Oct 25 13:36:20 … Time spent on flushing to /var/log/journal/MACHINE_ID is 12.476ms for 1701 entries.
Oct 25 13:36:21 … Received client request to flush runtime journal.       # rc=0
$ findmnt -T /var/log/journal -no FSTYPE,TARGET,SOURCE
btrfs /var/log root[/@log]                                                # rc=0
$ findmnt -no FSTYPE,TARGET /var
                                                                          # rc=1 (/var not a mountpoint)
$ findmnt -no FSTYPE,TARGET,OPTIONS /run
tmpfs /run rw,nosuid,nodev,relatime,mode=755,inode64,huge=advise           # rc=0
```

Reading of these extras (kept out of the entry's quoted cells because they are not in the frozen copies):

- The empty `/run/log/journal` is explained, not contradicted, by the boot flush: journald reported an 8M
  runtime journal at 13:36:19 and 1701 entries were flushed to `/var/log/journal` at 13:36:20-21, after
  which the tmpfs directory is empty. That is exactly what journald.conf(5) describes (journald starts
  volatile, `journalctl --flush`/SIGUSR1 switches it, done automatically on boot via
  `systemd-journal-flush.service` — committed copy lines 77-80). So runtime reach here is **zero by the
  time a reader looks**, and a claim must not say "the runtime journal holds this boot's early records".
- `--disk-usage` figures are allocated usage, not apparent size: 5 journal files are 72.0 MiB apparent
  (24.0 system + 48.0 user) while the command reports 56M total (19M system + 37M user) — sparse
  allocation. Do not derive one from the other.
- The boot-time `45M` (system) does not match the live `19M` (`--system --disk-usage`) for the same store,
  and the user share (37M) is the larger part of the total; the active user journal had mtime 21:43.
- `/var/log/journal` is not a mountpoint, but `/var/log` **is** a btrfs subvolume mount (`root[/@log]`); the
  persistent store is therefore on a dedicated subvolume of the root device, not "on the root filesystem"
  in the naive sense. The receipt's `[exit 1]` line cannot carry either statement.

## 4. Diff: what changed since the capture

Masking the 32-hex machine id to `MACHINE_ID` in both transcripts and normalising both with the counter's
`normalise()`, the receipt and the live transcript differ in **exactly two** places
(`diff -u receipt.norm live.norm`, `rc=1`):

```
-# captured 2026-10-25T20:43:09-03:00 on 7.2.11-arch1-1; no vacuum, rotate or config change was run …
+# captured 2026-10-25T21:42:45-03:00 on 7.2.11-arch1-1 …
 … 0 MACHINE_ID Sun 2026-10-25 13:36:19 -03 Sun 2026-10-25 20:43:03 -03
 … 0 MACHINE_ID Sun 2026-10-25 13:36:19 -03 Sun 2026-10-25 21:42:45 -03
```

So in 59 minutes: totals unchanged at 1M resolution (56/19/37), config, drop-in, mount facts and the
boot-time journald lines unchanged, boot set unchanged; only the current boot's `LAST ENTRY` advanced, and
the entry count grew 9677 → 12675. The `--disk-usage` number is rounded to 1M and would not show a few
hundred KiB of growth; the entry count is the sensitive measure of "the journal is still growing".

## 5. Stable facts vs volatile observations (what the entry may and may not state as constants)

Stable — unchanged across the 20:43 capture and the 21:42 re-run, and not moved by any journal read; only
an operator/package action would change them:

- the drop-in `/etc/systemd/journald.conf.d/size.conf` exists, 46 bytes, mtime `2026-10-16 11:53:47.069871418 -0300`, containing `SystemMaxUse=256M` and `RuntimeMaxUse=64M` (Q8 + DROP-b);
- the effective ceilings are 256M system / 64M runtime (Q4, Q5) — stable while the drop-in and the unit are unchanged;
- the shipped `/etc/systemd/journald.conf` leaves all size and retention keys commented, `MaxRetentionSec` default `0` (Q9);
- `/run` is tmpfs and `/var/log/journal` is not a mountpoint (Q6) — mount-layout facts, re-established each boot but not moving within one;
- the capture's own provenance line: read-only, no vacuum/rotate/config change (13 words, located; supports "the numbers are a passive snapshot", and is itself only self-declared — see F6).

Volatile — must never be written as constants: the 56M/19M/37M totals (S470 recorded 269M on 2026-10-24, so
this moves by day, and it is 1M-rounded); the 45M/8M usages and 210.9M/56M free figures (boot-time
snapshots that no longer match the live store); the boot list, its `LAST ENTRY`, boot ids, and the boot
count; entry counts (9677 → 12675 in 59 min); the emptiness of `/run/log/journal` (a single post-flush
observation); journal file mtimes and the 5-file/72-MiB apparent inventory.

Consequence for the entry: the reach statement it can defend is structural — ceiling 256M/64M from a local
drop-in, retention governed by size (no age limit), the runtime store drained at boot, and *at capture* two
boots were visible. It must not present 56M, 19M, 37M, 45M, 8M, 210.9M or "two boots" as the reach; 56M is
far below the 256M cap, so the cap is not what bounds the current reach, and the receipt contains no
evidence of what removed older journals (UNVERIFIED here; no vacuum was run by this seat).

## 6. Integration notes for the L1 (no files written outside this report)

1. **Cell contract for the new row.** `sources_row()` returns `split_cells` of an 11-cell row; the counter
   reads `[1]` for the source URL, `[7]` for status, `[8]` for the opened date, `[10]` for `used-by`
   (confirmed by dumping S351 and S470). For the host receipt the `COPIES` key is the literal string
   `own-work: host-journal-reach`, so cell `[1]` must contain that substring; `[7]` must be `mined`, `[8]`
   `2026-10-25`, and `[10]` must contain `corpus/knowledge/journal-reach-r49.md` (comma/semicolon-separated).
2. **Three-source floor.** All ten quotes above come from the own-work receipt. C2 needs `sources>=3`, so
   this inventory can only carry the S488 row(s); the rows quoting journald.conf(5), journalctl(1) and
   systemd-journald.service(8) must come from the other w1 seats. Receipt-only rows cannot reach `met`.
3. **Rows and entry are absent at freeze.** `grep -c 'S48[5-8]' corpus/SOURCES.md` = 0 and
   `corpus/knowledge/journal-reach-r49.md` does not exist, so at this moment the counter would report
   `entry_absent` and `bad_rows`/`source_rows` for any table; nothing here is a measured C2 result.
4. **Draft row for S488 (fenced, for the L1 to integrate; not written to `SOURCES.md`):**

```
| S488 | own-work: host-journal-reach — read-only capture of this host's journal store, 2026-10-25 | own-work | A | the effective ceilings and the store split this host's journald actually applies: a local drop-in sets 256M system / 64M runtime, the shipped config sets no age limit, and the volatile store is drained at boot | `journalctl --disk-usage`, `--system`/`--user`, `systemd-analyze cat-config systemd/journald.conf`, `stat` of the drop-in, `findmnt`, `ls -A /run/log/journal`, `--list-boots`, journald's own `Journal .* is .*max` lines; captured 2026-10-25T20:43:09-03:00 | supersedes S351 — the size ceiling is now grounded in the public journald.conf(5) text plus this read-only receipt, with no MESSAGE grep | mined | 2026-10-25 | 180d | corpus/knowledge/journal-reach-r49.md |
```

   (Cell `[6]` opens `supersedes S351 —` as the contract requires; if the L1 instead attaches the flip to the
   journalctl(1) row, keep that row's own quote from the page, and this row drops the supersede sentence.)
5. Candidate entry rows from this inventory (each cell 3 = one backticked span from §1): Q4 → "the system
   ceiling in force is 256M"; Q5 → "the runtime ceiling is 64M"; Q6+Q7 → "the volatile store is a tmpfs
   directory that is empty when read"; Q8+Q9 → "the ceiling comes from a 46-byte local drop-in, not a
   compiled default, and no age limit is configured"; Q10 → "at capture, two boots were visible". Keep at
   most one of Q1-Q3 and phrase it as "at capture", never as the reach.

## 7. Files, scratch, tooling

- Written: `.ufo/waves/round-49/w1/Mo49ExecQuotesHost.md` (this report). No other lane file created or edited;
  the committed receipt, `SOURCES.md`, `SKILL.md`, `corpus/`, `tools/`, the frozen `round-49/` files and the
  git/jj state were left untouched (no `git add/commit/stash/checkout/reset/pull/push`; only
  `git rev-parse`/`git show`-class reads).
- Scratch (round-end cleanup candidates, 24 KiB total): `.scratch/r49-Mo49ExecQuotesHost/` containing
  `verify_quotes.py`, `verify_repairs.py`, `live_capture.sh`, `live.txt`, `live.norm`, `receipt.norm`.
  All lane-tool runs used `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecQuotesHost`.
- Tooling: nothing installed or upgraded; no `pacman` transaction was attempted. `sudo -n` was used only for
  read-only `ls`/`find` under `/var/log/journal` (permitted by the seat rules); `journalctl` was run without
  sudo.
- Not run: no `journalctl --vacuum*`, `--rotate`, `systemctl`, config write, or anything under
  `/home/vgpnk/Projects/shokuknow`.

## Findings

- **MED — `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/journal-reach-r49.md` (missing) +
  `corpus/SOURCES.md` (S485-S488 absent).** The entry and its four source rows do not exist at this seat's
  run; the counter would currently report `entry_absent` plus row failures. Nothing in §1-§5 is a C2
  measurement. Integration must add cells `[1]/[7]/[8]/[10]` exactly as in §6.1.
- **MED — quotes can only come from the receipt for the S488 row (`count-c2.py:36-45`, `MIN_SOURCES=3`).**
  All ten legal spans are own-work receipt text; the `sources>=3` floor means receipt rows alone cannot
  satisfy C2, and the page rows must be supplied by other seats with page text (not with these spans).
- **MED — drop-in stanza is 5 words (below the floor).** The assignment's named quote "the drop-in
  `SystemMaxUse=256M`" is not quotable: `SystemMaxUse=256M` is 1 word and the full stanza with its path
  comment is 5. Lawful spans are DROP-b (7 words, absorbs `[exit 0]`) or DROP-c (6 words). Entry authoring
  must not paste the bare setting.
- **MED — command-crossing spans need the printed `[exit N]` marker.** `tmpfs $ findmnt -no FSTYPE
  /var/log/journal` reads correctly but is **not** in the copy; the receipt prints an exit marker between
  commands. The lawful repair is Q6 (8 words). This is the most likely silent `quote_missing` for the
  "tmpfs line".
- **MED — live output is not quotable (id masking).** The frozen copy masks the machine id as `MACHINE_ID`;
  any span copied from a live `journalctl -g 'Journal .* is .*max'` run carries a real 32-hex id and is not
  located. Probe with a synthetic id returned `located=False`. Same applies to the flush messages.
- **MED — sizes are not interchangeable (`host-journal-reach.txt` limit lines vs live store).** The boot
  line says 45M system while live `--system --disk-usage` says 19M; five files are 72.0 MiB apparent against
  a 56M allocated total. No size from this receipt may be stated as current or converted to apparent size.
- **MED — "max 256M" is not the reach.** The store is at 56M against a 256M cap, i.e. the cap is not
  binding, while only two boots are visible; the receipt holds no evidence of what removed older journals
  (S470 recorded 269M on 2026-10-24). The entry must present the cap as a ceiling and "two boots" as the
  2026-10-25 observation, never as the retention reach.
- **MED — the `[exit 1]` findmnt line does not establish where the persistent store lives.** Live
  `findmnt -T /var/log/journal` shows btrfs `root[/@log]` mounted at `/var/log`; `/var` itself is not a
  mountpoint. A claim "on the root filesystem" would be imprecise and is not supported by the receipt.
- **LOW — the runtime-journal contradiction is reconcilable but not from the copies.** Journald reports 8M
  runtime at 13:36:19 and `/run/log/journal` is empty now because of the boot flush (live journald
  messages: 1701 entries flushed at 13:36:20, "Received client request to flush runtime journal" at
  13:36:21; page text at journald.conf.5 lines 77-80 explains the automatic boot flush). None of the flush
  messages is in the committed receipt, so a "drained at boot" claim must rest on the page row, not on a
  receipt quote.
- **LOW — boot ids are unmasked in the receipt** (`host-journal-reach.txt` `--list-boots` rows) while the
  machine id is masked; if the lane's masking rule is meant to cover host identifiers generally, this is a
  shape inconsistency to note, not a secret leak.
- **LOW — 1M rounding hides growth.** `--disk-usage` stayed at 56M while boot `0` grew 9677 → 12675
  entries; an entry that cites the single number as "current usage" cannot detect the change it is
  describing. Prefer the ceiling/drain structure.
