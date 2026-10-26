# r49 w1 — Mo49ExecQuotesConf — quote inventory: journald.conf(5)

Seat: Mo49ExecQuotesConf (leaf executor, round 49 wave 1, lane mori-shokunin).
Assignment: 12 candidate quotes of 6–25 words from the committed journald.conf(5) copy, verified by
substring test against `count-c2.py`'s own `normalise()`, covering the System*/Runtime* split
(/var/log/journal vs /run/log/journal), when the persistent options apply, `MaxRetentionSec=` and its
default of 0, `MaxFileSec=`, `SystemKeepFree=`/`RuntimeKeepFree=`, and the page's own default-ceiling
statement.

Date: 2026-10-25 (local), after the lane tip it cites.

## Read and measured

- Contract: `.ufo/waves/round-49/contract.md` (frozen at `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`).
- Counter: `.ufo/waves/round-49/count-c2.py` — `normalise()`, `evaluate()` word rule
  (`q = re.sub(r"\s+"," ",span).strip()`, `words = q.split(" ")`, 6 ≤ len ≤ 25, one backticked span per
  quote cell, claim cell ≥ 5 words, `|` must not appear unescaped in a cell) imported, not copied.
- Source copy: `corpus/evidence/sources-r49/journald.conf.5.html`.
- Lane head read-only: `git rev-parse HEAD` → `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (exit 0);
  lane tip `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`, committed 2026-10-25 20:30:53 -0300.

Copy pin (exit 0):

```
$ sha256sum corpus/evidence/sources-r49/*
be3952cb6fdac6d6ced15a9a0092447db80fe699221b8478970bb402a558eb12  corpus/evidence/sources-r49/host-journal-reach.txt
75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722  corpus/evidence/sources-r49/journalctl.1.html
b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340  corpus/evidence/sources-r49/journald.conf.5.html
a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212  corpus/evidence/sources-r49/systemd-journald.service.8.html
```

The four digests equal the frozen pins in `count-c2.COPIES` (the verification script re-checks the
journald.conf pin against the counter's own dictionary and prints `pin : ok`).

Page shape (evidence for the `source`/location column): `grep -oE '<h[1-4][^>]*id="[^"]*"'` (exit 0) shows
only h2 anchors — `Name`, `Synopsis`, `Description`, `Configuration Directories and Precedence`, `Options`,
`Forwarding to traditional syslog daemons`, `See Also`; there is no `<h3>` in the page and every option is a
`<dt id="…">` term. Anchors used below, with copy line numbers from `grep -n`:
`#Storage=` (line 64), `#SystemMaxUse=` (line 139, the group of eight size options),
`#MaxFileSec=` (line 195), `#MaxRetentionSec=` (line 209).

## Inventory — 12 verified quotes

All twelve occur exactly once (`hits=1`) in `normalise()` output of the committed copy; word counts are the
counter's own (`q.split(" ")`). Source row for every one of them: **S485** (journald.conf(5) row; the w1 row
spec fixes S485 = this URL, so the quote's source cell must be `S485`).

| # | verbatim text | words | location | claim it supports | does NOT support |
|---|---|---|---|---|---|
| Q1 | `journal log data will be stored only in memory, i.e. below the /run/log/journal hierarchy (which is created if needed)` | 19 | `Options` → `#Storage=` (line 64) | `Storage=volatile` keeps the journal only below the in-memory `/run/log/journal` hierarchy, created if needed | does NOT support "the journal is always volatile", nor that `/var/log/journal` is skipped in persistent mode |
| Q2 | `data will be stored preferably on disk, i.e. below the /var/log/journal hierarchy (which is created if needed), with a fallback to /run/log/journal` | 22 | `Options` → `#Storage=` (line 64) | `Storage=persistent` prefers `/var/log/journal` and falls back to `/run/log/journal` during early boot or an unwritable disk | does NOT support "persistent data never lands in /run/log/journal", nor that the fallback is permanent |
| Q3 | `apply to the journal files when stored on a persistent file system, more specifically /var/log/journal` | 15 | `Options` → `#SystemMaxUse=` (line 139) | the `System*` size limits govern the persistent journal under `/var/log/journal` | does NOT support "System* limits also bound /run/log/journal", nor that the options are absent at runtime |
| Q4 | `apply to the journal files when stored on a volatile in-memory file system, more specifically /run/log/journal` | 16 | `Options` → `#SystemMaxUse=` (line 139) | the `Runtime*` size limits govern the volatile journal under `/run/log/journal` | does NOT support "Runtime* limits are inert when persistent logging is on", nor anything about deletion over time |
| Q5 | `The former is used only when /var/ is mounted, writable, and the directory /var/log/journal exists` | 15 | `Options` → `#SystemMaxUse=` (line 139) | the persistent (`System*`) limits apply only with `/var/` mounted and writable and `/var/log/journal` present | does NOT support "System* values are ignored forever when the directory is missing" — the page raises the limit to what is free, which this quote does not say |
| Q6 | `Note that this means that during early boot and if the administrator disabled persistent logging, only the latter options apply` | 20 | `Options` → `#SystemMaxUse=` (line 139) | during early boot, or with persistent logging disabled, only the `Runtime*` limits apply | does NOT support "the journal stays at the Runtime* ceiling for the whole boot", nor that persistent files are deleted |
| Q7 | `The maximum time to store journal entries. This controls whether journal files containing entries older than the specified time span are deleted` | 22 | `Options` → `#MaxRetentionSec=` (line 209) | `MaxRetentionSec=` is a time-based deletion rule: files holding entries older than the span are deleted | does NOT support "size limits enforce the same span", nor any particular default length |
| Q8 | `However, to enforce data retention policies, it might make sense to change this value from the default of 0 (which turns off this feature)` | 24 | `Options` → `#MaxRetentionSec=` (line 209) | `MaxRetentionSec=` defaults to 0, which turns the feature off | does NOT support "0 disables all deletion" (size-based vacuuming still runs), nor that the page recommends a value |
| Q9 | `The maximum time to store entries in a single journal file before rotating to the next one` | 17 | `Options` → `#MaxFileSec=` (line 195) | `MaxFileSec=` bounds the age of entries inside one file and rotates to the next file | does NOT support "MaxFileSec= deletes files" (it rotates), nor its one-month default (not in this span) |
| Q10 | `control how much disk space systemd-journald shall leave free for other uses` | 12 | `Options` → `#SystemMaxUse=` (line 139) | `SystemKeepFree=`/`RuntimeKeepFree=` are a free-space floor left for other users of the file system | does NOT support "KeepFree reserves space for the journal" (opposite), nor that it caps the journal's own size |
| Q11 | `The first pair defaults to 10% and the second to 15% of the size of the respective file system` | 19 | `Options` → `#SystemMaxUse=` (line 139) | default ceilings: `SystemMaxUse=`/`RuntimeMaxUse=` default to 10% of the file system, `KeepFree` to 15% | does NOT support "the journal may always consume 10%" — the pair is clamped to the smaller and these are caps, not reservations |
| Q12 | `but each of the calculated default values is capped to 4G` | 11 | `Options` → `#SystemMaxUse=` (line 139) | each calculated default ceiling (the 10%/15% pair) is capped at 4G | does NOT support "a configured value is capped at 4G" (only the calculated defaults are), nor a per-file cap |

The page's ceiling statement, quoted rather than recalled, is one 30-word sentence:
`The first pair defaults to 10% and the second to 15% of the size of the respective file system, but each of
the calculated default values is capped to 4G` (30 words, hits=1). Thirty words exceed the 25-word span
limit, so it must be split — that is why Q11 and Q12 are two rows.

## Verification script and its output

Script: `.scratch/r49-Mo49ExecQuotesConf/verify-quotes.py` (imports `normalise()` and `COPIES` from the frozen
counter; asserts the copy digest; word rule copied from `evaluate()`; section attribution by injecting
markers before every `<h2 id=…>`/`<dt id=…>` opening tag and mapping the quote's offset to the preceding
markers; three negative controls that must be absent).

Command and full output (`TMPDIR` set to the seat scratch; exit 0):

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && TMPDIR=$PWD/.scratch/r49-Mo49ExecQuotesConf \
    python3 .scratch/r49-Mo49ExecQuotesConf/verify-quotes.py
copy          : corpus/evidence/sources-r49/journald.conf.5.html
sha256        : b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340
frozen pin    : b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340
pin           : ok
normalised len: 22245 words: 3501
markers       : 20 h2/dt anchors

Q1 PASS
  quote      : journal log data will be stored only in memory, i.e. below the /run/log/journal hierarchy (which is created if needed)
  words      : 19 (limits 6-25)
  substring  : hits=1 first_index=4086
  section    : h2='Options' dt='Storage=' (expected h2='Options' dt='Storage=')
  supports   : Storage=volatile keeps the journal only below /run/log/journal (memory), created if needed
  note       : does NOT support 'the journal is always volatile', nor that /var/log/journal is skipped for the persistent mode.

Q2 PASS
  quote      : data will be stored preferably on disk, i.e. below the /var/log/journal hierarchy (which is created if needed), with a fallback to /run/log/journal
  words      : 22 (limits 6-25)
  substring  : hits=1 first_index=4225
  section    : h2='Options' dt='Storage=' (expected h2='Options' dt='Storage=')
  supports   : Storage=persistent prefers /var/log/journal and falls back to /run/log/journal during early boot or an unwritable disk
  note       : does NOT support 'persistent storage never lands in /run/log/journal', nor that the fallback is permanent.

Q3 PASS
  quote      : apply to the journal files when stored on a persistent file system, more specifically /var/log/journal
  words      : 15 (limits 6-25)
  substring  : hits=1 first_index=9523
  section    : h2='Options' dt='SystemMaxUse=' (expected h2='Options' dt='SystemMaxUse=')
  supports   : the System* size limits govern the persistent journal under /var/log/journal
  note       : does NOT support 'System* limits also bound /run/log/journal', nor that the options exist only when /var/ is mounted.

Q4 PASS
  quote      : apply to the journal files when stored on a volatile in-memory file system, more specifically /run/log/journal
  words      : 16 (limits 6-25)
  substring  : hits=1 first_index=9666
  section    : h2='Options' dt='SystemMaxUse=' (expected h2='Options' dt='SystemMaxUse=')
  supports   : the Runtime* size limits govern the volatile journal under /run/log/journal
  note       : does NOT support 'Runtime* limits are inert when persistent logging is on', nor anything about retention in time.

Q5 PASS
  quote      : The former is used only when /var/ is mounted, writable, and the directory /var/log/journal exists
  words      : 15 (limits 6-25)
  substring  : hits=1 first_index=9779
  section    : h2='Options' dt='SystemMaxUse=' (expected h2='Options' dt='SystemMaxUse=')
  supports   : the persistent (System*) limits apply only with /var/ mounted and writable and /var/log/journal present
  note       : does NOT support 'the System* values are ignored forever once missing'; the page's raise-the-limit behaviour is separate.

Q6 PASS
  quote      : Note that this means that during early boot and if the administrator disabled persistent logging, only the latter options apply
  words      : 20 (limits 6-25)
  substring  : hits=1 first_index=9915
  section    : h2='Options' dt='SystemMaxUse=' (expected h2='Options' dt='SystemMaxUse=')
  supports   : during early boot, or with persistent logging disabled, only the Runtime* limits apply
  note       : does NOT support 'the journal stops at the Runtime* ceiling for the whole boot', nor that persistent data is deleted.

Q7 PASS
  quote      : The maximum time to store journal entries. This controls whether journal files containing entries older than the specified time span are deleted
  words      : 22 (limits 6-25)
  substring  : hits=1 first_index=13371
  section    : h2='Options' dt='MaxRetentionSec=' (expected h2='Options' dt='MaxRetentionSec=')
  supports   : MaxRetentionSec= is the time-based deletion rule: files holding entries older than the span are deleted
  note       : does NOT support 'the entry-level time span is enforced by size limits', nor any specific default length.

Q8 PASS
  quote      : However, to enforce data retention policies, it might make sense to change this value from the default of 0 (which turns off this feature)
  words      : 24 (limits 6-25)
  substring  : hits=1 first_index=13727
  section    : h2='Options' dt='MaxRetentionSec=' (expected h2='Options' dt='MaxRetentionSec=')
  supports   : MaxRetentionSec= defaults to 0, which turns the feature off
  note       : does NOT support '0 disables all deletion' (size-based vacuuming still runs), nor that the page recommends a value.

Q9 PASS
  quote      : The maximum time to store entries in a single journal file before rotating to the next one
  words      : 17 (limits 6-25)
  substring  : hits=1 first_index=12674
  section    : h2='Options' dt='MaxFileSec=' (expected h2='Options' dt='MaxFileSec=')
  supports   : MaxFileSec= bounds the age of entries inside one file and triggers rotation to the next file
  note       : does NOT support 'MaxFileSec= deletes files'; it rotates, and time-based rotation is normally unnecessary.

Q10 PASS
  quote      : control how much disk space systemd-journald shall leave free for other uses
  words      : 12 (limits 6-25)
  substring  : hits=1 first_index=10492
  section    : h2='Options' dt='SystemMaxUse=' (expected h2='Options' dt='SystemMaxUse=')
  supports   : SystemKeepFree=/RuntimeKeepFree= are a free-space floor for other users of the file system
  note       : does NOT support 'KeepFree reserves space for the journal' (it is the opposite), nor that it caps the journal's own size.

Q11 PASS
  quote      : The first pair defaults to 10% and the second to 15% of the size of the respective file system
  words      : 19 (limits 6-25)
  substring  : hits=1 first_index=10651
  section    : h2='Options' dt='SystemMaxUse=' (expected h2='Options' dt='SystemMaxUse=')
  supports   : default ceilings: SystemMaxUse=/RuntimeMaxUse= default to 10% of the file system, KeepFree to 15%
  note       : does NOT support 'the journal may always consume 10%'; the pair is clamped by KeepFree and the values are caps, not reservations.

Q12 PASS
  quote      : but each of the calculated default values is capped to 4G
  words      : 11 (limits 6-25)
  substring  : hits=1 first_index=10747
  section    : h2='Options' dt='SystemMaxUse=' (expected h2='Options' dt='SystemMaxUse=')
  supports   : each calculated default ceiling (the 10%/15% pair) is capped at 4G
  note       : does NOT support 'the configured value is capped at 4G' — only the calculated defaults are; nor a per-file cap.

negative controls (each MUST be absent from the page text):
  SystemMaxUse default is 10% of the file system size, capped at 4G      absent (good)
  MaxRetentionSec defaults to one month                                  absent (good)
  journald keeps every entry for at least 30 days by default             absent (good)

RESULT: PASS (12 rows, 0 failures)
exit=0
```

## Ready-to-paste rows (draft only — integrator decides)

Every row cites S485; claim cells are ≥5 words as `evaluate()` requires; no cell contains `|` or a backtick
other than the quote's delimiters. Order follows the reading order of the page.

```markdown
| claim | source | quote |
|---|---|---|
| Storage=volatile keeps the journal only below the in-memory /run/log/journal hierarchy, created if needed | S485 | `journal log data will be stored only in memory, i.e. below the /run/log/journal hierarchy (which is created if needed)` |
| Storage=persistent prefers /var/log/journal and falls back to /run/log/journal during early boot or an unwritable disk | S485 | `data will be stored preferably on disk, i.e. below the /var/log/journal hierarchy (which is created if needed), with a fallback to /run/log/journal` |
| The System* size limits govern the persistent journal under /var/log/journal | S485 | `apply to the journal files when stored on a persistent file system, more specifically /var/log/journal` |
| The Runtime* size limits govern the volatile in-memory journal under /run/log/journal | S485 | `apply to the journal files when stored on a volatile in-memory file system, more specifically /run/log/journal` |
| The persistent limits apply only when /var/ is mounted and writable and /var/log/journal exists | S485 | `The former is used only when /var/ is mounted, writable, and the directory /var/log/journal exists` |
| During early boot, or with persistent logging disabled, only the Runtime* limits apply | S485 | `Note that this means that during early boot and if the administrator disabled persistent logging, only the latter options apply` |
| MaxRetentionSec= deletes journal files whose entries are older than the configured time span | S485 | `The maximum time to store journal entries. This controls whether journal files containing entries older than the specified time span are deleted` |
| MaxRetentionSec= defaults to 0, which turns the time-based feature off | S485 | `However, to enforce data retention policies, it might make sense to change this value from the default of 0 (which turns off this feature)` |
| MaxFileSec= bounds how long entries stay in one file before rotation to the next file | S485 | `The maximum time to store entries in a single journal file before rotating to the next one` |
| SystemKeepFree= and RuntimeKeepFree= set the free space journald leaves for other uses | S485 | `control how much disk space systemd-journald shall leave free for other uses` |
| The default size ceilings are 10% of the file system for max use and 15% for keep free | S485 | `The first pair defaults to 10% and the second to 15% of the size of the respective file system` |
| Each calculated default ceiling is capped at 4G | S485 | `but each of the calculated default values is capped to 4G` |
```

## Verified alternates (found by substring test, exit 0)

Not part of the twelve; listed so the integrator does not have to re-verify if a claim needs them.

| verbatim text | words | hits | location | note |
|---|---|---|---|---|
| `it might make sense to change this value from the default of one month` | 14 | 1 | `#MaxFileSec=` | the only statement of MaxFileSec's one-month default; Q9 does not carry it |
| `Set to 0 to turn off this feature` | 8 | 1 | `#MaxFileSec=` | rotation off; the same sentence shape does not exist for MaxRetentionSec (that one says "the default of 0 (which turns off this feature)") |
| `systemd-journald will respect both limits and use the smaller of the two values` | 13 | 1 | `#SystemMaxUse=` | MaxUse vs KeepFree interplay; Q10/Q11 do not state it |
| `SystemMaxUse= and RuntimeMaxUse= control how much disk space the journal may use up at most` | 15 | 1 | `#SystemMaxUse=` | the System*/Runtime* pair for max use in one sentence |
| `the existence of the directory controls the storage mode` | 9 | 1 | `#Storage=` | `Storage=auto` decision rule without the tagged literal quotes |
| `only archived files are deleted to reduce the space occupied by journal files` | 13 | 1 | `#SystemMaxUse=` | vacuum deletes archived files only |
| `This means that, in effect, there might still be more space used than SystemMaxUse= or RuntimeMaxUse= limit after a vacuuming operation is complete` | 23 | 1 | `#SystemMaxUse=` | reach can exceed the configured ceiling after a vacuum |
| `The default timeout is 5 minutes` | 6 | 1 | `#SyncIntervalSec=` | lowest permitted length; unrelated to retention |

## Hazards, measured

1. **Inline tag spacing.** `normalise()` strips tags to a space, so every `<code class="literal">volatile</code>`
   arrives as `" volatile "` with spaces inside the quotes. Probe
   `.scratch/r49-Mo49ExecQuotesConf/hazard-probe.py` (exit 0):
   `" volatile ", journal log data` → `FOUND hits=1`; the cleaned `"volatile", journal log data` → `absent hits=0`.
   Context printed by the probe: `Storage= ¶ Controls where to store journal data. One of " volatile ", " persistent ", " auto " and " none ". If " volatile ", journal log data will be stored only in memory, …`.
   Any quote that spans one of these literals must keep the stray spaces, which is why Q1/Q2 start after the
   literal instead of inside it.
2. **The ceiling statement is 30 words** as one sentence (measured above), so it cannot be a single span;
   Q11 and Q12 are the split. Q12 read alone ("capped to 4G") does not say *what* is capped — the claim cell
   must say "calculated default values".
3. **Five-word neighbours below the floor**: `This setting defaults to 100` (5 words) and
   `Otherwise, only the latter applies` (5 words) both occur exactly once but are one word short of the
   6-word floor; splicing either into a row makes `bad_rows`.
4. **Ambiguous short spans across sections**: `Normally, time-based` has hits=2 (MaxFileSec and
   MaxRetentionSec paragraphs); `takes time values which may be suffixed with the units` also recurs. A span
   that fits both sections locates but does not distinguish the two options.
5. **Single-source block**: all twelve quotes come from one copy, so twelve S485 rows satisfy
   `claims≥8` but give `sources=1`; the entry still needs rows citing S486 (journalctl(1)), S487
   (systemd-journald.service(8)) and/or S488 (host receipt) to reach `sources≥3`.
6. `evaluate()` matches a quote against `norm[url]` for the URL found in the cited row's source cell, so an
   S485 row whose source cell lacks the exact URL string
   `https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html` fails `bad_rows` even with a
   correct quote.
7. The page has no `<h3>`; options are `<dt id="…">` terms inside `Options`. A location cited as a heading
   ("Storage= section") names something that does not exist as a heading; the term anchors above are the
   grounded locations.

## What I did not do

- Did not fetch the live page; every statement is about the committed copy at
  sha256 `b4a9b53e…`, matching its frozen pin. Whether the live page still reads this way is unverified here.
- Did not edit SKILL.md, SOURCES.md, corpus/, tools/, LOG.md, SCORECARD.md, QUALITY.md or any frozen
  round-49 file; the only lane writes are this report and `.scratch/r49-Mo49ExecQuotesConf/`.
- No git index, jj, or fleet-repo mutation; no pacman, no tool installs.
- Did not run the counters (the L1 owns the gate run).

## Files changed

- `.ufo/waves/round-49/w1/Mo49ExecQuotesConf.md` (this report).
- `.scratch/r49-Mo49ExecQuotesConf/dump-text.py` (dumps counter-normalised page text; used for reading).
- `.scratch/r49-Mo49ExecQuotesConf/journald.conf.5.wrapped.txt` (152-line wrapped dump, read as source).
- `.scratch/r49-Mo49ExecQuotesConf/verify-quotes.py` (12 quotes + pins + locations + negative controls).
- `.scratch/r49-Mo49ExecQuotesConf/hazard-probe.py` (inline-tag spacing and alternates probe).

## Findings

- **MED** `corpus/evidence/sources-r49/journald.conf.5.html` — inline literals normalise with spaces inside
  their quotes (`" volatile "`); a drafted quote written the clean way (`"volatile"`) fails the substring test
  (probe hits=0 vs 1). Any entry row touching `Storage=`/`Forward*` literals must reproduce the spacing or
  start after it.
- **MED** page text, `#SystemMaxUse=` paragraph — the ceiling statement is a single 30-word sentence, over the
  25-word span limit; splitting (Q11/Q12) loses the subject of "capped to 4G" from Q12, so the claim cell must
  carry "calculated default values" or the row supports an over-read ("configured 4G cap").
- **MED** page text, `#SystemMaxUse=` paragraph — the twelve quotes do not include the page's own
  "more space used than SystemMaxUse= … after a vacuuming operation is complete" (verified 23-word span,
  alternates table); an entry claiming journal reach equals the configured ceiling would be contradicted by
  the page and no row in the twelve fences it.
- **LOW** all twelve quotes are from one copy — twelve S485 rows alone give `sources=1` and cannot satisfy
  `sources≥3`; the entry needs S486/S487/S488 rows regardless of how many journald.conf rows are used.
- **LOW** `count-c2.py` `evaluate()` — a row's `bad_rows` outcome depends on the cited SOURCES row containing
  the exact URL string from `COPIES`; an S485 row phrased around the URL fails with a correct quote.
- **LOW** page text — `This setting defaults to 100` and `Otherwise, only the latter applies` are 5 words and
  fall below the counter's 6-word floor despite being unique; splicing them yields `bad_rows`.
- **LOW** page text — `Normally, time-based` recurs in both `#MaxFileSec=` and `#MaxRetentionSec=`; a short
  span there locates but does not distinguish the two rules.
- **LOW** page structure — no `<h3>` exists; a "section heading" citation for an option should name the
  `<dt id="…">` term (`#Storage=`, `#SystemMaxUse=`, `#MaxFileSec=`, `#MaxRetentionSec=`), not a heading.
