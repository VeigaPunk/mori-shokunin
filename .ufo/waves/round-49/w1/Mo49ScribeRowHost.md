# Mo49ScribeRowHost — SOURCES.md row S488 (own-work host receipt)

Seat: `Mo49ScribeRowHost` (scribe, leaf). Author date: 2026-10-25T21:46-0300.
Lane tip read: `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (round-49 freeze; entering tip
`b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` is its parent). Nothing in the lane was edited,
staged, committed or moved by this seat.

## Behavior

Deliver, inside this report only: one 11-column `corpus/SOURCES.md` registry row `S488` for the
own-work host receipt, one `## Gate` line for it, and a two-sentence statement of why the staged
own-work rows S524/S537/S544 are not adopted. Drafts below; the L1 integrates.

The row's source cell carries the literal token `own-work: host-journal-reach`, which is the key
the round-49 C2 counter matches (`count-c2.py` `COPIES`: `"own-work: host-journal-reach"` →
`corpus/evidence/sources-r49/host-journal-reach.txt`, sha256
`be3952cb6fdac6d6ced15a9a0092447db80fe699221b8478970bb402a558eb12`). The cell names none of the
three freedesktop URLs, so the counter's URL loop can only bind this row to the receipt copy.

`teaches` deliberately does **not** open `supersedes S351 —`: the S351 flip (public `--vacuum-size=`
sentence plus a committed read-only receipt) is carried by S486, the journalctl(1) row (seat
`Mo49ScribeRowCtl`). S488 is the receipt row; keeping the supersede phrase off it avoids two rows
claiming the same flip.

## Draft — row S488 (one physical line; 11 columns; no `|` inside any cell)

```markdown
| S488 | own-work: host-journal-reach — this host's journald limits and journal reach, read-only receipt corpus/evidence/sources-r49/host-journal-reach.txt | own-work | A | this host only (7.2.11-arch1-1), read-only on 2026-10-25: the effective [Journal] limits the size.conf drop-in sets, the runtime and system journal paths the journald start line names with their caps and usage, and the 56M reach at capture; not the retention rule (S485), not the vacuum order (S486) and not any other host | receipt corpus/evidence/sources-r49/host-journal-reach.txt, sha256 be3952cb6fdac6d6ced15a9a0092447db80fe699221b8478970bb402a558eb12, captured 2026-10-25T20:43:09-03:00; command headings journalctl --disk-usage, journalctl --system --disk-usage, journalctl --user --disk-usage, systemd-analyze cat-config systemd/journald.conf, stat -c '%n %s bytes mtime %y' /etc/systemd/journald.conf.d/size.conf, findmnt -no FSTYPE /run, findmnt -no FSTYPE /var/log/journal, ls -A /run/log/journal, journalctl --list-boots --no-pager, journalctl -b 0 -u systemd-journald --no-pager -q -g 'Journal .* is .*max' | A read-only receipt shows this host's computed journal ceilings against its current use — 56M total under SystemMaxUse=256M and RuntimeMaxUse=64M, the 46-byte size.conf drop-in setting them — so a journal-derived kill count can be bounded before it is trusted; the byte sizes move with use and boot while that drop-in is the stable part. | mined | 2026-10-25 | 90d | corpus/knowledge/journal-reach-r49.md |
```

Cell-by-cell justification (all read from the receipt, never from the staged notes):

| column | value | grounding in the receipt |
|---|---|---|
| id | `S488` | next unused id; registry maximum at the freeze is S484 (`git show 0df17b7:corpus/SOURCES.md`), S485-S487 are this wave's other row seats |
| source | token + receipt path | receipt exists, is tracked, sha256 matches the C2 pin |
| kind | `own-work` | own-work enum (CORPUS.md contract v1); `S477` sets the same precedent for a read-only host receipt |
| tier | `A` | the lane's own re-runnable gate output, scoped to this host only |
| scope | this host only, 2026-10-25 | receipt line 1 (`captured 2026-10-25T20:43:09-03:00 on 7.2.11-arch1-1; no vacuum, rotate or config change was run`) |
| anchor | receipt + sha256 + timestamp + the ten command headings | receipt `$` headings at lines 4, 8, 12, 16, 75, 79, 83, 86, 89, 95 |
| teaches | one benefit + volatility caveat | 56M at line 5; 256M/64M drop-in at lines 71-72; drop-in size and date at line 76 |
| status | `mined` | the round entry `corpus/knowledge/journal-reach-r49.md` cites it |
| opened | `2026-10-25` | capture date |
| recheck | `90d` | host state is volatile (see teaches caveat); the drop-in half is stable, the sizes are not |
| used-by | `corpus/knowledge/journal-reach-r49.md` | the one entry this wave admits |

## Draft — Gate-block line (house shape: `corpus/lessons/round-47.md` `## Gate`)

```markdown
| S488 | own-work: read-only `journalctl --disk-usage`, `journalctl --system --disk-usage`, `journalctl --user --disk-usage`, `systemd-analyze cat-config systemd/journald.conf`, `stat` of `/etc/systemd/journald.conf.d/size.conf`, `findmnt` for `/run` and `/var/log/journal`, `ls -A /run/log/journal`, `journalctl --list-boots --no-pager` and the `systemd-journald` start line, all on 7.2.11-arch1-1; receipt `corpus/evidence/sources-r49/host-journal-reach.txt` (sha256 `be3952cb…558eb12`), captured 2026-10-25T20:43:09-03:00 | 2026-10-25 | "System Journal (/var/log/journal/MACHINE_ID) is 45M, max 256M, 210.9M free." — 9 words, receipt line 97, from `journalctl -b 0 -u systemd-journald --no-pager -q -g 'Journal .* is .*max'` | admit, mined |
```

If the L1 prefers the total-reach sentence as the Gate quote, the alternative is
`"Archived and active journals take up 56M in the file system."` — 11 words, receipt line 5, from
`journalctl --disk-usage`. I chose the System Journal line because one sentence carries the
ceiling/use distinction the row teaches; the 56M total, the 64M runtime cap and the drop-in's own
bytes are anchored in the row's anchor cell instead.

The quote contains only the already-redacted token `MACHINE_ID`; no host machine id, session URL or
credential appears in this report.

## Why S524 / S537 / S544 are not adopted (two sentences)

Those three staged own-work rows are `mined 2026-10-24` rows whose locator is a `file://` note under
`/home/vgpnk/Projects/shokuknow/lanes/mori/round{8,9,10}/.deepresearch/notes/` — outside this lane,
outside its git history and unpinned, so no committed copy and no frozen sha256 exist for the C2
counter to locate a quote in. This round's host receipt replaces them: the same read-only,
detection-only content, but its bytes are committed in this lane at
`corpus/evidence/sources-r49/host-journal-reach.txt` and hash-pinned, which is exactly the property
the staged notes lack.

## Evidence (command → output → exit code)

1. `sha256sum corpus/evidence/sources-r49/host-journal-reach.txt` →
   `be3952cb6fdac6d6ced15a9a0092447db80fe699221b8478970bb402a558eb12` — exit 0. Equals the C2
   `COPIES` pin for `own-work: host-journal-reach`.
2. `git rev-parse HEAD` → `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (freeze) — exit 0.
   `git show 0df17b7b…:corpus/evidence/sources-r49/host-journal-reach.txt | sha256sum` → the same
   digest. `git show b3e3453d…:corpus/evidence/sources-r49/host-journal-reach.txt` → exit 128
   (absent at the entering tip), i.e. the copy is introduced by the freeze, matching the C2
   do-nothing receipt `pins=bad`.
3. `git ls-files --error-unmatch corpus/evidence/sources-r49/host-journal-reach.txt` → path printed,
   exit 0 (tracked).
4. `grep -c '|' corpus/evidence/sources-r49/host-journal-reach.txt` → `0` (grep exit 1, no match).
   No receipt text can break a table row; the draft row still split into exactly 11 cells under the
   frozen counter's own `split_cells`.
5. Structural check with the frozen counter's own functions (`count-c2.py` loaded read-only via
   `importlib`, `split_cells`, `sources_row`, `COPIES`, `normalise`):
   `cells 11`; `sources_row match: True`; `url match: ['own-work: host-journal-reach']`;
   `status/opened/usedby: mined 2026-10-25 ['corpus/knowledge/journal-reach-r49.md']`;
   `receipt sha256 ok: True`; `gate quote words: 9 located: True`.
6. Census A/B on a scratch copy (no lane file touched): `scripts/sources-census.sh validate --file`
   on the copy → exit 1 (E11 noise from the scratch root); with the row inserted before `## Paths`
   → exit 1, and `diff` of the two outputs adds exactly one line:
   `file	E11	S488 missing used-by corpus/knowledge/journal-reach-r49.md`.
   No E01/E02/E03/E04/E05/E06/E07/E08/E09/E10/E12 and no W04 appeared. Frozen manual census:
   rows with `NF!=13` → `0`; duplicate ids → none; the S488 line itself → `NF=13`.
7. `test -e corpus/knowledge/journal-reach-r49.md` → exit 1: the entry does not exist yet (seat
   `Mo49ScribeEntryA`/`B` drafts it), which is the whole of the E11 line in item 6.
8. Read-only host checks of the receipt's own claims (no `journalctl --vacuum*`, no `--rotate`, no
   `systemctl`, no config change):
   - `ls -ld /var/log/journal` → `drwxr-sr-x+ 1 root systemd-journal 76 Oct  3 17:42`, exit 0;
     `ls -A /var/log/journal` → one machine-id directory (written `MACHINE_ID` here), exit 0.
   - `findmnt -no FSTYPE /var/log/journal` → no output, exit 1 (reproduces receipt line 84);
     `findmnt -no FSTYPE -T /var/log/journal` → `btrfs`, exit 0.
   - `ls -la /run/log/journal` → empty (`total 0`, dir mtime `Oct 25 13:36`), exit 0;
     `sudo -n ls -A /run/log/journal` → empty, exit 0; `sudo -n ls -A /proc/1/root/run/log/journal`
     → empty, exit 0 (so the empty listing is not a namespace or permission artefact of my shell).
   - `sudo -n ls -l /var/log/journal/MACHINE_ID/` → five `.journal` files, apparent sizes
     `8388608 + 16777216 + 16777216 + 16777216 + 16777216 = 75497472` bytes.
   - `stat -c '%n %s bytes mtime %y' /etc/systemd/journald.conf.d/size.conf` → `46 bytes mtime
     2026-10-16 11:53:47.069871418 -0300`, exit 0; the file's body is `[Journal]`,
     `SystemMaxUse=256M`, `RuntimeMaxUse=64M` (matches receipt lines 71-72 and 76).
9. Staged locator files: all three `file://` notes named by S524/S537/S544 exist on disk under
   `/home/vgpnk/Projects/shokuknow/lanes/mori/round{8,9,10}/.deepresearch/notes/` (exit 0 for
   `test -e`), and none is inside this lane's git tree — read only, nothing run there.

## Gates run (and their honest reach)

- **S488 ↔ P-C2 row requirements**: each of the four row-level conditions the counter tests is
  checked by the counter's own parser — `srow[7]=="mined"`, `srow[8]=="2026-10-25"`, the source
  token binding to the receipt copy, and `used-by` splitting to exactly
  `corpus/knowledge/journal-reach-r49.md`. The **end-to-end** `count-c2.py R` run is **UNVERIFIED at
  this seat**: the entry is not landed, so `claims=` and `sources=` do not exist yet. Running the
  counter against a synthetic entry would measure my fixture, not the lane.
- **SOURCES-CONTRACT-v1 (census)**: 11 columns / `NF=13`, no new findings other than the expected
  E11; no duplicate id; no URL in the source cell, so neither E04 nor W04 can fire from this row.
- **Rule 1 (a row is a claim)**: every value in the row is read from the pinned receipt or from the
  freeze commit; nothing is copied from the staged notes, which I read only as documents to reject.
- **Rule 2 (append-only)**: the draft is a new row; no existing row, status, recheck or used-by is
  changed. S351 stays `rejected`; its flip is S486's.

## Touched surfaces

- Written: this report (`.ufo/waves/round-49/w1/Mo49ScribeRowHost.md`) and scratch only.
- Scratch (lane): `.scratch/r49-Mo49ScribeRowHost/row-s488.txt`,
  `.scratch/r49-Mo49ScribeRowHost/corpus/SOURCES.md` and `SOURCES.row.md` (validation copies),
  `validate-base.out`, `validate-row.out`.
- Not touched: `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/evidence/`, `tools/`, `SKILL.md`,
  `LOG.md`, `SCORECARD.md`, `QUALITY.md`, the frozen round-49 files (`contract.md`,
  `count-c1.py`, `count-c2.py`, `controls/`, `evidence/`), any sibling lane, the fleet repo, the
  lane's git index or jj state, `/home/vgpnk/Projects/shokuknow*` (read-only reads).
- No tool installs or upgrades were needed; `pacman` was not run (host-wide pause respected).
- No subagents were spawned (leaf seat).

## Out-of-scope / not checked

- Entry prose, the S485/S486/S487 rows, the lesson, SKILL.md registry rows, SCORECARD/LOG/QUALITY —
  other seats.
- Whether `56M` is still the reach today: I did not re-measure `journalctl --disk-usage` on purpose
  (re-running it would change the row's numbers; the receipt is the pinned capture). **UNVERIFIED**
  for any later reading.
- Wave-2 style re-open of the three manual pages: not my seat.

## Findings

- **MED** — `corpus/evidence/sources-r49/host-journal-reach.txt:86-87` (**`ls -A /run/log/journal`**,
  empty) sits ten lines above line 96 (**`Runtime Journal (/run/log/journal/MACHINE_ID) is 8M, max
  64M, 56M free.`**). Today the runtime directory is still empty for root and through
  `/proc/1/root` (evidence item 8), while `/var/log/journal/MACHINE_ID/` holds `system.journal` and
  `user-1000.journal`. Read alone, the empty listing invites the false conclusion "the runtime
  journal is unused"; the consistent reading is that the boot's runtime entries were already
  flushed to the persistent store before the capture. [INFERENCE on the flush; the empty directory
  and the persistent files are observed.] Any entry row quoting line 86 must not turn it into "no
  volatile journal exists".
- **LOW** — `corpus/evidence/sources-r49/host-journal-reach.txt:83-84`:
  `findmnt -no FSTYPE /var/log/journal` exits 1 (reproduced). Exit 1 here means "/var/log/journal is
  not itself a mountpoint", not "the path is absent": `findmnt -no FSTYPE -T /var/log/journal` →
  `btrfs` (exit 0) and the directory exists with the machine-id subdirectory. A reader who quotes
  the exit code as "no persistent journal" would contradict the `System Journal
  (/var/log/journal/MACHINE_ID)` line at 97.
- **LOW** — receipt line 5 (`56M` total) versus the five committed journal files' apparent sizes
  (`75497472` bytes, evidence item 8). `journalctl --disk-usage` reports disk usage, not apparent
  bytes (journal files are allocation-rounded and compression is on by default), so the two numbers
  are not comparable unit-for-unit and must not be summed against each other in the entry.
- **LOW** — receipt lines 96-97 (start-of-boot readings `8M` / `45M`) versus lines 9 and 13
  (capture-time `--system 19M` / `--user 37M`). The system reading moved `45M → 19M` within one
  boot. The row's Gate quote is the `45M` start line (chosen because it carries `max 256M`); the
  entry must not present `45M` as the current system usage. This is the row's own volatility
  caveat, and the reason `recheck` is `90d` rather than `on-release`.
- **LOW** — `corpus/SOURCES.md` (pending append): S488's `used-by`
  `corpus/knowledge/journal-reach-r49.md` does not exist yet, so the census emits
  `E11 S488 missing used-by corpus/knowledge/journal-reach-r49.md` (evidence item 6/7). It clears
  when the entry lands with that exact path; if the entry is renamed, the row's `used-by` and the
  entry's `source:` line must both change together.
