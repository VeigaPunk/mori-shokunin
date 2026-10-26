# r49 w1 — Mo49ExecQuotesSvc — quote inventory: systemd-journald.service(8) and journalctl(1)

Seat: Mo49ExecQuotesSvc (leaf executor, round 49 wave 1, lane mori-shokunin).
Assignment: 14 candidate quotes (7 per page, 6–25 words) from the committed copies of
`systemd-journald.service.8.html` and `journalctl.1.html`, each verified by plain substring test
after `count-c2.py`'s own `normalise()`, covering: persistent versus volatile storage and the reboot
loss; the default (persistent if `/var/log/journal` exists, volatile otherwise); `--disk-usage` and
what it counts; `--vacuum-size`/`--vacuum-time`/`--vacuum-files` and which files they remove; the
named `--list-boots`/`--boot`; `--system`/`--user` scopes.

Date: 2026-10-25 (local), after the lane tip it cites.

## Read and measured

- Contract: `.ufo/waves/round-49/contract.md` (freeze `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`).
- Counter: `.ufo/waves/round-49/count-c2.py` — `normalise()` (script/style and comment blocks dropped,
  tags stripped, entities decoded, whitespace collapsed) imported by path with `importlib`, together
  with its `COPIES` pins and its word rule (`MIN_WORDS, MAX_WORDS = 6, 25`; the counter collapses the
  quote and counts `q.split(" ")`). Not copied, not re-implemented.
- Lane head read-only: `git rev-parse HEAD` → `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (exit 0). No
  git/jj write of any kind was run.
- Copies read: `corpus/evidence/sources-r49/systemd-journald.service.8.html` (28143 bytes on disk,
  28116 decoded characters) and `corpus/evidence/sources-r49/journalctl.1.html` (87375 bytes on disk,
  87235 decoded characters). Both header-render as `systemd 262` (first 40 chars of
  `normalise(copy)`). The verification script's `bytes=` field prints the decoded character count.
- Both digests match `count-c2.COPIES` exactly, recomputed in the verification run below:
  `a7b443568865bb09…` (service page) and `75440570fb1f7185…` (command page).

## Copy geometry (raw copy line numbers, observed by `grep -n` / `sed -n`)

`systemd-journald.service.8.html`: `<h2 id="Description">` 23, `<h2 id="Files">` 160,
`<dt id="SIGUSR1">` 103, `<dt id="SIGUSR2">` 110. The storage paragraph (persistent/volatile,
default, flush switch) starts at line 36 and runs to 43; the `/run/ is used when …` sentence sits in
`Files` at 169–174; the automatic-eviction sentence at 181–182; `Request immediate rotation of the
journal files.` at 110.

`journalctl.1.html`: `<h2 id="Source Options">` and `<dt id="--system">` 71 (the `--system, --user`
term and its paragraph, 71–73), `-b [ ID ][ ±offset ]|all` term 127–128, `<dt id="--list-boots">` 277,
`<dt id="--disk-usage">` 289, `<dt id="--vacuum-size=">` 290 (the three vacuum options share one term,
290–303), `<dt id="--flush">` 324, `<dt id="--rotate">` 331.

Topic words present in `normalise(copy)` (`grep -o | wc -l`, exit 0): service page —
`vacuum` 0, `disk-usage` 0, `list-boots` 0, `reboot` 1, `archived` 3; command page — `vacuum` 17,
`disk-usage` 2, `list-boots` 1, `reboot` 1, `archived` 7. The service page therefore carries no
vacuum/disk-usage/list-boots text at all, which is why the split below is by page (storage side from
the service page, command side from the command page) and the six assigned bullets are covered across
the 14, not 7 bullets per page.

## The 14 candidates

Locations are the section/term anchor in the copy plus the character offset into `normalise(copy)` from
the verification run; every quote is one single-line span with no backtick and no `|`, so it drops into
one backticked table cell as the counter requires.

### systemd-journald.service(8) — 7 quotes, cite S487

| id | anchor (copy) | words | verbatim quote |
|---|---|---|---|
| SVC1 | `#Description`, char 1497 | 17 | `The journal service stores log data either persistently below /var/log/journal or in a volatile way below /run/log/journal/` |
| SVC2 | `#Description`, char 1621 | 9 | `(in the latter case, it is lost at reboot)` |
| SVC3 | `#Description`, char 1665 | 20 | `By default, log data is stored persistently if /var/log/journal/ exists during boot, with an implicit fallback to volatile storage otherwise.` |
| SVC4 | `#Description`, char 1996 | 18 | `a call to journalctl --flush (or sending SIGUSR1 to journald) will cause it to switch to persistent logging` |
| SVC5 | `#Files`, char 11982 | 19 | `/run/ is used when /var/log/journal is not available, or when Storage=volatile is set in the journald.conf (5) configuration file.` |
| SVC6 | `#Signals` / `SIGUSR1`, char 7336 | 23 | `This must be used after /var/ is mounted, as otherwise log data from /run/ is never flushed to /var/ regardless of the configuration.` |
| SVC7 | `#Files`, char 12537 | 13 | `systemd-journald will automatically remove the oldest archived journal files to limit disk use` |

**SVC1 — claim it supports.** Journal storage is one of two stores: persistent below `/var/log/journal`
or volatile below `/run/log/journal/`. **does NOT support:** which store this host uses, or that the two
cannot both exist at a moment; the sentence is a dichotomy of storage modes, not a statement about
existence on any machine.

**SVC2 — claim it supports.** Volatile journal records are lost at reboot. **does NOT support:** that
nothing is copied to `/var` before the reboot, or that a given boot's records are absent — the loss is
scoped to the volatile store, and the flush path (SVC4, SVC6) is what moves `/run` data into `/var`.
The sentence starts with a bare parenthesis; its antecedent ("the latter case" = the volatile store) is
in SVC1, so a row quoting SVC2 alone must name the volatile store in its claim cell.

**SVC3 — claim it supports.** The default storage decision is persistent if `/var/log/journal/` exists
during boot, and volatile otherwise. **does NOT support:** what this host's configuration resolves to (a
`Storage=` setting or drop-in overrides it), nor that creating the directory later moves existing
`/run` records — that needs the flush path, and the "during boot" qualifier is in the quoted span.

**SVC4 — claim it supports.** journald starts volatile and switches to persistent logging on
`journalctl --flush` or `SIGUSR1`. **does NOT support:** that a flush ever ran, nor that the switch
succeeds before `/var` is mounted (SVC6 says it does not), nor any bound on how long the persistent
store is kept. The span stops before "(under the conditions mentioned above)".

**SVC5 — claim it supports.** `/run/` holds the journal when `/var/log/journal` is unavailable or
`Storage=volatile` is set. **does NOT support:** that the unavailability is temporary, nor any size
ceiling for the runtime store (`RuntimeMaxUse=` is a journald.conf(5) option, not on this page).

**SVC6 — claim it supports.** The flush signal is effective only after `/var/` is mounted; otherwise
`/run` data is never flushed. **does NOT support:** that `/var` is mounted in a given boot, nor that the
boot-time `systemd-journal-flush.service` path ran — this span is scoped to the SIGUSR1 remedy.

**SVC7 — claim it supports.** journald itself evicts the oldest archived journal files to limit disk
use. **does NOT support:** any value — no size, no timespan, no count; the page points at
`SystemMaxUse=` and related settings in journald.conf(5) instead (POOL9). Nor active files, nor that the
result is what `--disk-usage` reports.

### journalctl(1) — 7 quotes, cite S486

| id | anchor (copy) | words | verbatim quote |
|---|---|---|---|
| CTL1 | `#Commands` / `--disk-usage`, char 25715 | 15 | `This shows the sum of the disk usage of all archived and active journal files.` |
| CTL2 | `#Commands` / `--vacuum-size=`, char 25868 | 18 | `--vacuum-size= removes the oldest archived journal files until the disk space they use falls below the specified size` |
| CTL3 | `#Commands` / `--vacuum-time=`, char 26067 | 10 | `--vacuum-time= removes archived journal files older than the specified timespan` |
| CTL4 | `#Commands` / `--vacuum-files=`, char 26590 | 23 | `--vacuum-files= might not actually reduce the number of journal files to below the specified number, as it will not remove active journal files` |
| CTL5 | `#Commands` / `--list-boots`, char 24631 | 14 | `Show a tabular list of boot numbers (relative to the current boot), their IDs` |
| CTL6 | `-b/--boot` term, char 9434 | 16 | `The argument may be empty, in which case logs for the current boot will be shown.` |
| CTL7 | `#Source Options` / `--system, --user`, char 4574 | 21 | `Show messages from system services and the kernel (with --system ). Show messages from service of current user (with --user ).` |

**CTL1 — claim it supports.** `--disk-usage` reports one total over archived *and* active journal
files. **does NOT support:** per-journal or per-boot attribution, nor which directories are summed (the
page does not enumerate them here), nor that the total equals any retention ceiling.

**CTL2 — claim it supports.** `--vacuum-size=` deletes the oldest archived files until the disk space
they use falls below the size. **does NOT support:** that active files or the runtime journal are
touched (they are not — CTL4, and the sentence at char 26374 says vacuuming "only operates on archived
journal files"), nor that it bounds what the current boot is still writing, nor the suffix grammar. This
sentence is word-for-word the sentence row **S351** recorded, which is the public half of the S351
flip.

**CTL3 — claim it supports.** `--vacuum-time=` deletes archived files older than the timespan.
**does NOT support:** which timestamp the age is measured from (the page does not say), nor that active
files are exempt (that is the separate sentence, ALT6/char 26374), nor the accepted suffix set
(separate sentence).

**CTL4 — claim it supports.** `--vacuum-files=` may leave more than the requested number of files
because it does not remove active files. **does NOT support:** a definition of "separate journal files"
(the preceding sentence defines the count), nor that this option applies a size or time test, nor that
"archived" is the removal set inside this span — the span carries the active exemption, the archived set
comes from the neighbouring sentences.

**CTL5 — claim it supports.** `--list-boots` prints a table of boot numbers relative to the current
boot, with their IDs. **does NOT support:** that every listed boot still has records — a boot whose
files were vacuumed away is not covered by this span; nor the first/last timestamps, which continue
after the quoted cut.

**CTL6 — claim it supports.** `--boot` with an empty argument restricts output to the current boot.
**does NOT support:** how many boots the store holds, nor that the current boot's records are all
present, nor the ID/offset lookup rules (following clauses).

**CTL7 — claim it supports.** `--system` reads system services and kernel messages; `--user` reads the
current user's service messages. **does NOT support:** whether `--user` sees a volatile per-user store —
a later sentence says `--user` only works if persistent logging is enabled (ALT7, char 4842); nor access
control, nor which files either scope opens. Normalisation note: the spaces inside `(with --system )`
and `(with --user )` are tag-stripping artifacts (the option is wrapped in `<code>`, which
`normalise()` replaces with a space), present in the committed copy's normalised text, so the span
verifies as written — but it renders with an odd gap. ALT2 + ALT3 (or ALT4) avoid the artifact at the
cost of naming only one scope per row.

### Verified alternates (informational, not part of the 14)

| id | page | words | quote | use |
|---|---|---|---|---|
| ALT1 | svc | 20 | `Request that journal data from /run/ is flushed to /var/ in order to make it persistent (if this is enabled).` | SIGUSR1's own statement of what flushing does |
| ALT2 | ctl | 8 | `Show messages from system services and the kernel` | clean `--system` half of CTL7 |
| ALT3 | ctl | 7 | `Show messages from service of current user` | clean `--user` half of CTL7 |
| ALT4 | ctl | 12 | `If neither is specified, show all messages that the user can see.` | default scope when neither is given |
| ALT5 | ctl | 10 | `All users are granted access to their private per-user journals.` | per-user journals exist for all users |
| ALT6 | ctl | 13 | `running --vacuum-size= has only an indirect effect on the output shown by --disk-usage` | vacuum sees archived only, disk usage sees both |
| ALT7 | ctl | 16 | `Note that --user only works if persistent logging is enabled, via the Storage= setting in journald.conf` | `--user` reach requires persistent storage |

### Verified swap pool (informational, not part of the 14)

| id | page | words | quote |
|---|---|---|---|
| POOL1 | ctl | 15 | `all active files are rotated first, and the requested vacuuming operation is executed right after` |
| POOL2 | ctl | 12 | `The rotation has the effect that all currently active files are archived` |
| POOL3 | ctl | 16 | `Specifying any of these three parameters as zero is equivalent to not enforcing the specific limit` |
| POOL4 | ctl | 16 | `This command effectively guarantees that all data is flushed to /var/log/journal/ at the time it returns.` |
| POOL5 | ctl | 18 | `Journal file rotation has the effect that all currently active journal files are marked as archived and renamed` |
| POOL6 | ctl | 19 | `the vacuuming operation has the greatest effect as it can take all log data written so far into account` |
| POOL7 | ctl | 12 | `removes archived journal files older than the specified timespan. Accepts the usual` |
| POOL8 | svc | 7 | `Request immediate rotation of the journal files.` |
| POOL9 | svc | 7 | `See SystemMaxUse= and related settings in journald.conf` |
| POOL10 | svc | 12 | `When systemd-journald ceases writing to a journal file, it will be renamed` |

POOL1/POOL5/POOL6 are the rotate-then-vacuum path (journalctl.1.html:308–333): rotation archives the
active files first, and only then does the vacuum reach the data just written. POOL3 is the
"zero means no limit" rule. POOL4 is `--flush`'s guarantee. POOL9 is the pointer that keeps every
number off these two pages.

## Coverage map to the assigned bullets

| assigned bullet | quotes |
|---|---|
| persistent versus volatile and the reboot loss | SVC1, SVC2 |
| the default (persistent if `/var/log/journal` exists) | SVC3 |
| `--disk-usage` and what it counts | CTL1 (ALT6 for the archived-only contrast) |
| `--vacuum-size`/`--vacuum-time`/`--vacuum-files`, archived only, oldest first | CTL2, CTL3, CTL4 (SVC7, POOL1, POOL5 for the daemon-side eviction and rotation order) |
| `--list-boots` and `--boot` | CTL5, CTL6 |
| `--system`/`--user` scopes | CTL7 (ALT2, ALT3, ALT4, ALT7) |

## Paste constraints checked by the script

- 14/14 are substrings of `normalise(copy)`; word counts 9–23, inside 6–25; per-page split 7 + 7.
- No quote contains a backtick or a `|`, so each fits one backticked cell and no cell split occurs.
- No quote is a duplicate of another across the 14 (checked as a set).
- Claims above are ≥ 5 words and name what the quote establishes, not the adjacent sentence.
- Every quote is unique in this inventory; the entry must still avoid re-using a span twice in its own
  table (the counter counts duplicates as `bad_rows`).
- Shape caution: this inventory's tables are 4 columns (id, anchor, words, quote) for review. The entry
  needs exactly 3 cells per row (`claim | S-id | quote`), so an inventory row must not be pasted as-is —
  drop the id/anchor/words columns, and keep the quote cell to one backticked span with no second span
  anywhere in the row.

## Verification command and output

Scratch (created by this seat): `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecQuotesSvc/`
holding `dump.py` (writes the normalised dumps), `ctx.py` (context printer), `verify_quotes.py` (the
verifier), `verify_quotes.out` (its saved output) and the two `*.norm.txt` dumps. `TMPDIR` was set to
that directory, never `/tmp`.

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecQuotesSvc
$ TMPDIR=$PWD python3 verify_quotes.py > verify_quotes.out 2>&1; echo "rc=$?"
rc=0
```

```
copy corpus/evidence/sources-r49/systemd-journald.service.8.html bytes=28116 sha256=a7b443568865bb09… frozen=a7b443568865bb09… MATCH
copy corpus/evidence/sources-r49/journalctl.1.html bytes=87235 sha256=75440570fb1f7185… frozen=75440570fb1f7185… MATCH

== 14 candidates (7 service + 7 journalctl) ==
SVC1  words=17 PASS
        at char 1497 of normalise(corpus/evidence/sources-r49/systemd-journald.service.8.html)
        ctx: ...he journal may be up to 2⁶⁴-1 bytes in size. The journal service stores log data either persistently below /var/log/journal or in a volatile way below /run/log/journal/ (in the latter case, it is lost at reboot). ...
        quote: The journal service stores log data either persistently below /var/log/journal or in a volatile way below /run/log/journal/
SVC2  words=9  PASS
        at char 1621 of normalise(corpus/evidence/sources-r49/systemd-journald.service.8.html)
        ctx: ...or in a volatile way below /run/log/journal/ (in the latter case, it is lost at reboot). By default, log data is stored persistently...
        quote: (in the latter case, it is lost at reboot)
SVC3  words=20 PASS
        at char 1665 of normalise(corpus/evidence/sources-r49/systemd-journald.service.8.html)
        ctx: ... (in the latter case, it is lost at reboot). By default, log data is stored persistently if /var/log/journal/ exists during boot, with an implicit fallback to volatile storage otherwise. Use Storage= in journald.conf (5) to configu...
        quote: By default, log data is stored persistently if /var/log/journal/ exists during boot, with an implicit fallback to volatile storage otherwise.
SVC4  words=18 PASS
        at char 1996 of normalise(corpus/evidence/sources-r49/systemd-journald.service.8.html)
        ctx: ...d will initially use volatile storage, until a call to journalctl --flush (or sending SIGUSR1 to journald) will cause it to switch to persistent logging (under the conditions mentioned above). This...
        quote: a call to journalctl --flush (or sending SIGUSR1 to journald) will cause it to switch to persistent logging
SVC5  words=19 PASS
        at char 11982 of normalise(corpus/evidence/sources-r49/systemd-journald.service.8.html)
        ctx: ...stemd-journald starts writing to a new file. /run/ is used when /var/log/journal is not available, or when Storage=volatile is set in the journald.conf (5) configuration file. When systemd-journald ceases writing to a jo...
        quote: /run/ is used when /var/log/journal is not available, or when Storage=volatile is set in the journald.conf (5) configuration file.
SVC6  words=23 PASS
        at char 7336 of normalise(corpus/evidence/sources-r49/systemd-journald.service.8.html)
        ctx: ... to make it persistent (if this is enabled). This must be used after /var/ is mounted, as otherwise log data from /run/ is never flushed to /var/ regardless of the configuration. Use the journalctl --flush command to reques...
        quote: This must be used after /var/ is mounted, as otherwise log data from /run/ is never flushed to /var/ regardless of the configuration.
SVC7  words=13 PASS
        at char 12537 of normalise(corpus/evidence/sources-r49/systemd-journald.service.8.html)
        ctx: ...ad all entries that have been fully written. systemd-journald will automatically remove the oldest archived journal files to limit disk use. See SystemMaxUse= and related settings in j...
        quote: systemd-journald will automatically remove the oldest archived journal files to limit disk use
CTL1  words=15 PASS
        at char 25715 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...the current disk usage of all journal files. This shows the sum of the disk usage of all archived and active journal files. Added in version 190. --vacuum-size= , --vac...
        quote: This shows the sum of the disk usage of all archived and active journal files.
CTL2  words=18 PASS
        at char 25868 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...m-size= , --vacuum-time= , --vacuum-files= ¶ --vacuum-size= removes the oldest archived journal files until the disk space they use falls below the specified size. Accepts the usual " K ", " M ", " G " and "...
        quote: --vacuum-size= removes the oldest archived journal files until the disk space they use falls below the specified size
CTL3  words=10 PASS
        at char 26067 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ... " and " T " suffixes (to the base of 1024). --vacuum-time= removes archived journal files older than the specified timespan. Accepts the usual " s " (default), " m ", "...
        quote: --vacuum-time= removes archived journal files older than the specified timespan
CTL4  words=23 PASS
        at char 26590 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...erates on archived journal files. Similarly, --vacuum-files= might not actually reduce the number of journal files to below the specified number, as it will not remove active journal files. --vacuum-size= , --vacuum-time= and --vacuu...
        quote: --vacuum-files= might not actually reduce the number of journal files to below the specified number, as it will not remove active journal files
CTL5  words=14 PASS
        at char 24631 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...ournal. Added in version 195. --list-boots ¶ Show a tabular list of boot numbers (relative to the current boot), their IDs, and the timestamps of the first and last me...
        quote: Show a tabular list of boot numbers (relative to the current boot), their IDs
CTL6  words=16 PASS
        at char 9434 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...ot. This will add a match for " _BOOT_ID= ". The argument may be empty, in which case logs for the current boot will be shown. If the boot ID is omitted, a positive offset...
        quote: The argument may be empty, in which case logs for the current boot will be shown.
CTL7  words=21 PASS
        at char 4574 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...ad journal records from: --system , --user ¶ Show messages from system services and the kernel (with --system ). Show messages from service of current user (with --user ). If neither is specified, show all messages t...
        quote: Show messages from system services and the kernel (with --system ). Show messages from service of current user (with --user ).
per-page counts: 7 + 7 OK

== alternates (informational) ==
ALT1  words=20 PASS
        at char 7226 of normalise(corpus/evidence/sources-r49/systemd-journald.service.8.html)
        ctx: ...MACHINE_ID . NAMESPACE . Signals ¶ SIGUSR1 ¶ Request that journal data from /run/ is flushed to /var/ in order to make it persistent (if this is enabled). This must be used after /var/ is mounted, as...
        quote: Request that journal data from /run/ is flushed to /var/ in order to make it persistent (if this is enabled).
ALT2  words=8  PASS
        at char 4574 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...ad journal records from: --system , --user ¶ Show messages from system services and the kernel (with --system ). Show messages from service...
        quote: Show messages from system services and the kernel
ALT3  words=7  PASS
        at char 4642 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...em services and the kernel (with --system ). Show messages from service of current user (with --user ). If neither is specified, sho...
        quote: Show messages from service of current user
ALT4  words=12 PASS
        at char 4701 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...from service of current user (with --user ). If neither is specified, show all messages that the user can see. The --user option affects how --unit= argume...
        quote: If neither is specified, show all messages that the user can see.
ALT5  words=10 PASS
        at char 3186 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...directory= , and --file= options, see below. All users are granted access to their private per-user journals. However, by default, only root and users who...
        quote: All users are granted access to their private per-user journals.
ALT6  words=13 PASS
        at char 26374 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ... number of separate journal files. Note that running --vacuum-size= has only an indirect effect on the output shown by --disk-usage , as the latter includes active journal file...
        quote: running --vacuum-size= has only an indirect effect on the output shown by --disk-usage
ALT7  words=16 PASS
        at char 4842 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...--unit= arguments are treated. See --unit= . Note that --user only works if persistent logging is enabled, via the Storage= setting in journald.conf (5) . Added in version 205. -M , --machine= ...
        quote: Note that --user only works if persistent logging is enabled, via the Storage= setting in journald.conf

== swap pool (informational) ==
POOL1 words=15 PASS
        at char 27134 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...bined with --rotate into one command. If so, all active files are rotated first, and the requested vacuuming operation is executed right after. The rotation has the effect that all curren...
        quote: all active files are rotated first, and the requested vacuuming operation is executed right after
POOL2 words=12 PASS
        at char 27233 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...vacuuming operation is executed right after. The rotation has the effect that all currently active files are archived (and potentially new, empty journal files op...
        quote: The rotation has the effect that all currently active files are archived
POOL3 words=16 PASS
        at char 26930 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...f files limit on the archived journal files. Specifying any of these three parameters as zero is equivalent to not enforcing the specific limit, and is thus redundant. These three switches...
        quote: Specifying any of these three parameters as zero is equivalent to not enforcing the specific limit
POOL4 words=16 PASS
        at char 29268 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ... any operation if this has already happened. This command effectively guarantees that all data is flushed to /var/log/journal/ at the time it returns. Added in version 217. --rotate ¶ Asks the jo...
        quote: This command effectively guarantees that all data is flushed to /var/log/journal/ at the time it returns.
POOL5 words=18 PASS
        at char 29524 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...rn until the rotation operation is complete. Journal file rotation has the effect that all currently active journal files are marked as archived and renamed, so that they are never written to in future...
        quote: Journal file rotation has the effect that all currently active journal files are marked as archived and renamed
POOL6 words=19 PASS
        at char 27382 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...rnal files opened as replacement), and hence the vacuuming operation has the greatest effect as it can take all log data written so far into account. Added in version 218. --verify ¶ Check the ...
        quote: the vacuuming operation has the greatest effect as it can take all log data written so far into account
POOL7 words=12 PASS
        at char 26082 of normalise(corpus/evidence/sources-r49/journalctl.1.html)
        ctx: ...ffixes (to the base of 1024). --vacuum-time= removes archived journal files older than the specified timespan. Accepts the usual " s " (default), " m ", " h ", " days ", " w...
        quote: removes archived journal files older than the specified timespan. Accepts the usual
POOL8 words=7  PASS
        at char 7651 of normalise(corpus/evidence/sources-r49/systemd-journald.service.8.html)
        ctx: ...for details. Added in version 186. SIGUSR2 ¶ Request immediate rotation of the journal files. Use the journalctl --rotate command to reque...
        quote: Request immediate rotation of the journal files.
POOL9 words=7  PASS
        at char 12633 of normalise(corpus/evidence/sources-r49/systemd-journald.service.8.html)
        ctx: ...st archived journal files to limit disk use. See SystemMaxUse= and related settings in journald.conf (5) . Added in version 206. /dev/kmsg , /dev...
        quote: See SystemMaxUse= and related settings in journald.conf
POOL10 words=12 PASS
        at char 12113 of normalise(corpus/evidence/sources-r49/systemd-journald.service.8.html)
        ctx: ...in the journald.conf (5) configuration file. When systemd-journald ceases writing to a journal file, it will be renamed to " original-name @ suffix.journal " (or " ...
        quote: When systemd-journald ceases writing to a journal file, it will be renamed

candidates=14 verified=yes alternates_verified=yes pool_verified=yes pins=ok
exit=0
```

## Files changed

- Wrote this report only: `.ufo/waves/round-49/w1/Mo49ExecQuotesSvc.md`.
- Scratch only: `.scratch/r49-Mo49ExecQuotesSvc/{dump.py,ctx.py,verify_quotes.py,verify_quotes.out,systemd-journald.service.8.html.norm.txt,journalctl.1.html.norm.txt}` (`TMPDIR` set there).
- No lane file, no frozen file, no jj/git state touched; no commit/add/stash/checkout/reset/pull/push.
- No tool installed or upgraded (nothing was needed; no pacman transaction attempted).

## Findings

1. **MED** — Neither page carries a numeric retention ceiling. `MaxRetentionSec` and `RuntimeMaxUse` occur 0 times across both normalised copies; `SystemMaxUse` occurs once, only as a cross-reference, in `corpus/evidence/sources-r49/systemd-journald.service.8.html:181-182`. Any figure in `corpus/knowledge/journal-reach-r49.md` must come from S485 (journald.conf(5)) or S488 (host receipt); no number may be attributed to S486/S487.
2. **MED** — The vacuum contract on the command page is archived-only and oldest-first, and active files are exempt until rotation: `corpus/evidence/sources-r49/journalctl.1.html:290-303` (CTL2/CTL3/CTL4) versus `journalctl.1.html:308-333` (POOL1/POOL5, rotate-then-vacuum). An entry claiming that vacuuming bounds what the current boot writes would quote across that exemption; it must say the vacuum reaches the current data only via `--rotate` or after the daemon archives the file.
3. **LOW** — The S351 flip material is present and word-for-word: CTL2 equals the sentence recorded on row S351 (`corpus/SOURCES.md:248`), so S486's `teaches` can open `supersedes S351 —` and this inventory supplies the public sentence that flip named.
4. **LOW** — CTL7 verifies but carries tag-stripping artifacts, `(with --system ).` and `(with --user ).`, because the option tokens are wrapped in `<code>` in `corpus/evidence/sources-r49/journalctl.1.html:71-73`; they will render with a stray space. ALT2 + ALT3 (or ALT4) are artifact-free but name one scope per row.
5. **LOW** — SVC2 begins with `(` and its antecedent is in SVC1 (`systemd-journald.service.8.html:36-37`). A row quoting SVC2 alone is located but not self-contained, so its claim cell must itself name the volatile store.
6. **LOW** — Both copies are the `systemd 262` revision of the page. A count-only recheck (e.g. `grep -c SystemMaxUse`) would pass after a version bump that kept the sentence; the entry's `recheck:` should also read the rendered version string.
7. **LOW** — CTL1 quotes the same sentence that row S470 already records as its `teaches` and that `corpus/knowledge/journal-disk-usage-total-r51.md` carries (`corpus/SOURCES.md:249`). C2's uniqueness rule is per-table, so a second use is legal, but the lane would hold one sentence in two entries — decide deliberately whether CTL1 or S470 carries it.
8. **LOW** — All 14 candidates sit on two sources (S486, S487). The C2 floor of 3 distinct sources and 8 rows still needs at least one journald.conf(5) row and the host-receipt row from the other w1 seats; nothing in this inventory satisfies that arm by itself.
9. **LOW** — Scratch residue: `.scratch/r49-Mo49ExecQuotesSvc/` holds 6 files, and `git status --porcelain` at the freeze tip already lists many untracked `.scratch/c1-*` directories. Round 48's routed defect (114 untracked scratch dirs) recurs; this directory is listed under "Files changed" for round-end cleanup and `.gitignore` entry.
