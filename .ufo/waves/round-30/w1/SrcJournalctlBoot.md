# SrcJournalctlBoot — frontier source row for C1 (`journalctl -b` scope, `-u` matching)

Seat MoriR30.SrcJournalctlBoot, leaf. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`, entering tip
`58b61681a0e3f3b821a17d38a4e713ccd9921615`. Contract read first: `.ufo/waves/round-30/contract.md`. No subagents, no tool installs (only coreutils and curl
already on the host), no git, nothing written outside
`/fast/scratch/hyaku/mori-r30/MoriR30.SrcJournalctlBoot/` and this report. The shell tool auto-backgrounded two
read-only commands (`bg_6024`, a recursive grep over `corpus/` and `.ufo/` that its 300 s cap cancelled; `bg_6046`,
the numbered-line extraction whose output this report already contains); neither produced evidence used here.

## Outcome

- The named candidate `man/journalctl.xml` carries the fact but is the first URL of row S122 → **reject, duplicate**.
- New primary: `src/journal/journalctl.c` at tag v262 (HTTP 200, 47,020 B). Two companions from the same tag,
  `src/journal/journalctl-filter.c` and `src/journal/journalctl-util.c`, are named in the row's anchor (the S154
  multi-file pattern: one quoted primary, companion paths anchored by line).
- One ready-to-paste row, two admit Gate lines and two reject Gate lines, plus the excerpt body below.

## Commands actually run (read-only in the lane)

- Registry screening: `grep -n "systemd" corpus/SOURCES.md` (hits at rows S007–S040, S120–S133, S150–S155);
  `grep -n "journalctl" corpus/SOURCES.md` → only S014 and S122; `grep -n "journalctl.c\|journal/journalctl"
  corpus/SOURCES.md` → exit 1, no hit; `grep -n "journal-util\|journalctl-filter\|journalctl-util"
  corpus/SOURCES.md` → exit 1, no hit.
- Fetch, in `/fast/scratch/hyaku/mori-r30/MoriR30.SrcJournalctlBoot`: `curl -sS -o <file> -w '%{http_code}'
  https://raw.githubusercontent.com/systemd/systemd/v262/<path>`, then `date -u +%FT%TZ` before and after,
  `sha256sum <file>`, `wc -c -l <file>`.
- Quote and excerpt construction: `awk 'NR>=L && NR<=M {printf "%d\t%s\n", NR, $0}' <file>` (number-tab-verbatim),
  `awk 'NR>=L && NR<=M {printf "%s ", $0}' | sed 's/  */ /g' | wc -w` for each quote count.

## Screening

### Candidate A — opened, carries the fact, rejected as a duplicate URL

`https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml` — HTTP 200, 61,619 B, 1,205 lines,
sha256 `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd`, fetched
2026-10-22T21:12:33Z–21:12:34Z. It carries both halves: `:287-288` "Show messages from a specific boot. This will
add a match for `_BOOT_ID=`." and `:316-323` (`--unit=`; "A match is added for messages from the unit"). Reject
reason is duplicate, verified by `grep -n "journalctl" corpus/SOURCES.md` → `corpus/SOURCES.md:128` is row S122,
whose first source URL is this exact file. The parent's W04/E04 finding is confirmed.

### Candidate B — chosen primary (not in the registry)

`https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c` — HTTP 200, 47,020 B, 1,139
lines, sha256 `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab`, fetched
2026-10-22T21:12:33Z–21:12:34Z. It holds the option grammar: `-b` is `OPTION_OPTIONAL_ARG` and, with no
descriptor, the parser sets `arg_boot = true`, `arg_boot_filter = true`, `arg_boot_id = SD_ID128_NULL`,
`arg_boot_offset = 0` (`:512-517`); `-u` appends its value to `arg_system_units` (`:543-544`). Help string at
`:513` reads "Show current boot or the specified boot".

### Companions opened at the same tag (hashed, anchored, not excerpted)

| file | bytes / lines | sha256 | anchored lines |
|---|---|---|---|
| `src/journal/journalctl-filter.c` | 15,249 B / 495 | `480f7a03040c0ddc93b1b65c0b49d6f0e8a4a377ee1b94168655132dcfd72f48` | `:62-76` `add_boot` calls `add_match_boot_id` then `sd_journal_add_conjunction`; `:94-201` `journal_add_unit_matches` calls `add_matches_for_unit_full` and adds a disjunction per unit; `:203-217` `add_units` passes `arg_system_units`, `UID_INVALID`, `arg_user_units` |
| `src/journal/journalctl-util.c` | 11,114 B / 284 | `a2385abed40d6417c8bf3acb308010a803ad0105bc72b6053054a8ad2797c64b` | `:89-129` `journal_acquire_boot`: null id with zero offset and no `--directory`/`--file`/`--root` calls `id128_get_boot_for_machine(arg_machine, &arg_boot_id)` at `:102`, `arg_boot_id = boot_id` at `:125` |
| `src/journal/journalctl-util.h` | 1,309 B / 35 | `5d5d172fcac2f59d48dc1349062fd23a1dbea328a008a7e141f693f5ee2310e5` | `:9-12` `SYSTEM_UNITS` = `_SYSTEMD_UNIT`, `UNIT`, `OBJECT_SYSTEMD_UNIT` |

Fetched at 2026-10-22T21:13:22Z (filter.c) and 21:13:38Z (util.c), both HTTP 200; the header was re-fetched at
2026-10-22T21:22:59Z with the same sha256 (HTTP 200, 1,309 B, 35 lines).

### Search hop opened and rejected (verified reason)

`https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/journal-util.c` — HTTP 200, 6,927 B, 192 lines,
sha256 `d81dc8bfec7452694c8def5522addb1d608370d5de05e342de3bcfa207ecb5b8`. Opened looking for the unit match
builder: `grep -c "add_matches_for_unit_full" journal-util.c` → `0` (exit 1). That symbol is defined at
`src/shared/logs-show.c:1729`, and `logs-show.c` is already inside row S123, so neither file can host this row.
(This reject reason is a count, not a claim of "no line matched" — round-29 R2.)

## Ready-to-paste SOURCES row (one line, exact column shape of `corpus/SOURCES.md:7-8`)

```markdown
| S15x | systemd v262 journalctl option grammar and filter application — https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl-filter.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl-util.c | code | A | the journalctl read path at the v262 release tag only: how `-b/--boot` takes an optional descriptor and, with none, enables the boot filter with a null boot id and zero offset (help: `Show current boot or the specified boot`), how `-u/--unit` appends its value to the system-unit filter list, how the filter stage resolves a null boot id with zero offset, in the default open with no `--directory`/`--file`/`--root`, to the running machine's boot id and then adds a boot-id match plus a conjunction, and how the unit list becomes unit-name matches over the `SYSTEM_UNITS` fields; not the man-page wording (that URL is S122's and was rejected as a duplicate), not JSON encoding (S122, S123), not this host's journal contents, not journal storage, vacuum or persistence | src/journal/journalctl.c:512-517 (`-b` is `OPTION_OPTIONAL_ARG`; no descriptor sets `arg_boot = true`, `arg_boot_filter = true`, `arg_boot_id = SD_ID128_NULL`, `arg_boot_offset = 0`), :543-544 (`-u` value appended to `arg_system_units`); src/journal/journalctl-filter.c:62-76 (`add_boot`: `add_match_boot_id` then `sd_journal_add_conjunction`), :94-201 (`journal_add_unit_matches`: `add_matches_for_unit_full` plus `sd_journal_add_disjunction` per unit), :203-217 (`add_units` passes `arg_system_units`); src/journal/journalctl-util.c:89-129 (`journal_acquire_boot`: null id and zero offset call `id128_get_boot_for_machine` at :102, `arg_boot_id = boot_id` at :125); src/journal/journalctl-util.h:9-12 (`SYSTEM_UNITS` field list); tag v262 | A descriptorless `-b` restricts the read to the running boot's entries and each `-u UNIT` adds that unit's messages as journal matches rather than text filters; neither option changes which journal files are opened, and neither proves that any killer acted. | mined | 2026-10-22 | on-release | corpus/lessons/round-30.md, corpus/knowledge/earlyoom-invocation-scope-r30.md |
```

## Ready-to-paste Gate lines (add under `## Gate` in `corpus/lessons/round-30.md`)

```markdown
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | 2026-10-22T21:12:34Z | `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` | `:290` (16 words): "The argument may be empty, in which case logs for the current boot will be shown." | reject, duplicate URL: this file is S122's first URL at `corpus/SOURCES.md:128`; it carries the fact but cannot open a new row |
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c | 2026-10-22T21:12:34Z | `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab` | `:514-517` (12 words): "arg_boot = true; arg_boot_filter = true; arg_boot_id = SD_ID128_NULL; arg_boot_offset = 0;" | admit, A, mined |
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c | 2026-10-22T21:12:34Z | `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab` | `:544-546` (10 words): "r = strv_extend(&arg_system_units, opts.arg); if (r < 0) return log_oom();" | admit, A, mined |
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/journal-util.c | 2026-10-22T21:14:19Z | `d81dc8bfec7452694c8def5522addb1d608370d5de05e342de3bcfa207ecb5b8` | grep count (0 hits, exit 1): `add_matches_for_unit_full` occurs 0 times in the fetched bytes | reject, does not carry the unit match builder: `grep -c` returns 0; the builder is `src/shared/logs-show.c:1729`, already inside S123 |
```

Word counts were produced by `wc -w` on the whitespace-collapsed lines named, not estimated: `q1.txt` (`:514-517`)
→ 12, `q2.txt` (`:544-546`) → 10, and `journalctl.xml:290` → 16.

## Excerpt file `corpus/evidence/sources-r30/S15x.txt` (ready to paste)

```text
id: S15x
url: https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c
sha256: 285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab
accessed: 2026-10-22T21:12:34Z
lines: 509-547

509	                        arg_boot_offset = 0;
510	                        break;
511	
512	                OPTION_FULL(OPTION_OPTIONAL_ARG, 'b', "boot", "ID",
513	                            "Show current boot or the specified boot"):
514	                        arg_boot = true;
515	                        arg_boot_filter = true;
516	                        arg_boot_id = SD_ID128_NULL;
517	                        arg_boot_offset = 0;
518	
519	                        if (opts.arg) {
520	                                r = parse_id_descriptor(opts.arg, &arg_boot_id, &arg_boot_offset);
521	                                if (r < 0)
522	                                        return log_error_errno(r, "Failed to parse boot descriptor '%s'", opts.arg);
523	
524	                                arg_boot = r;
525	                                arg_boot_filter = r > 0;
526	
527	                        } else {
528	                                /* Hmm, no argument? Maybe the next word on the command line is supposed to
529	                                 * be the argument? Let's see if there is one and is parsable as a boot
530	                                 * descriptor… */
531	                                char *peek = option_parser_peek_next_arg(&opts);
532	                                if (peek) {
533	                                        r = parse_id_descriptor(peek, &arg_boot_id, &arg_boot_offset);
534	                                        if (r >= 0) {
535	                                                arg_boot = r;
536	                                                arg_boot_filter = r > 0;
537	                                                (void) option_parser_consume_next_arg(&opts);
538	                                        }
539	                                }
540	                        }
541	                        break;
542	
543	                OPTION('u', "unit", "UNIT", "Show logs from the specified unit"):
544	                        r = strv_extend(&arg_system_units, opts.arg);
545	                        if (r < 0)
546	                                return log_oom();
547	                        break;
```

## Privacy scan of the excerpt

`grep -nE 'user@[0-9]+|user-[0-9]+\.(slice|service)|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|/home/|vgpnk|hyaku|\.local' excerpt-body.txt` → printed `no matches` (grep exit 1). The 39 excerpted lines are option-parser
code: no uid, no `user@<digits>`, no `user-<digits>.slice`, no unit name of this host, no host name, no e-mail
address, no `/etc/default/earlyoom` value. The row, the Gate lines and the excerpt carry no host state, and no
journal text was ever read from this host for this seat.

## Limits (state, not pass)

1. One excerpt file per id, so only the primary file's lines are excerpted. The two companions are anchored by
   `path:line` in the row (the S154 one-quoted-primary pattern) and are not quoted in a Gate line; a Gate line per
   companion would need its own excerpt file and sha256, which is not drafted here.
2. `add_match_boot_id` is declared outside the three files: grepping the fetched set finds only the calls at
   `journalctl-filter.c:72` and `:360`, not a definition. The row therefore says "a boot-id match" and does not name
   the journal field it writes; the `_BOOT_ID` wording exists only in the rejected man page (`journalctl.xml:287-288`)
   and is kept out of the row on purpose.
3. The "current boot" resolution lives at `journalctl-util.c:100-102`, which is anchored but not quoted. The excerpted
   primary only shows the null-id/zero-offset parser state; the fact is complete across the anchored lines, but a
   reader checking quotes alone sees the parser half of `-b`.
4. The `-u` half is evidenced by the parser clause (`:543-544`, quoted) plus `add_units`/`journal_add_unit_matches`
   (anchored). The field list `_SYSTEMD_UNIT`, `UNIT`, `OBJECT_SYSTEMD_UNIT` is `journalctl-util.h:9-12`; the man page
   names only `_SYSTEMD_UNIT` and `_SYSTEMD_SLICE` (`journalctl.xml:322-324`). [INFERENCE] that the list is what
   `add_matches_for_unit_full` iterates: its body (`src/shared/logs-show.c:1729`) was located by grep but not read
   line by line.
5. Only one host-visible action was taken: fetching public raw.githubusercontent.com files. No unit, process, setting
   or file outside the scratch dir was touched.

## Findings for L1 (plain English)

1. The candidate is a true duplicate, not merely similar: `corpus/SOURCES.md:128` is row S122 and opens with
   `man/journalctl.xml`, whose `:287-290` and `:316-323` already state both `-b` and `-u`. The reject is recorded
   with a located quote, a sha256 and the registry citation, so it cannot be read as an unverified "no line matched".
2. The new row is adjacent to S122 in topic but different in kind: S122 documents encoding, retention and the match
   set from the manual; S15x is the CLI implementation. Its scope sentence says so and excludes the man-page wording,
   JSON encoding and host state.
3. The claim the entry may build on is a scope claim only: a descriptorless `-b` narrows the read to one boot and
   `-u` narrows it to one unit, as journal matches. Absence inside that read is evidence about that boot and unit and
   nothing more; it cannot support "no killer ran anywhere".
4. Nothing was written to the lane. The row, the Gate lines and the excerpt body are drafts in this report for the L1
   to place; the fetched bytes and the quote files are under
   `/fast/scratch/hyaku/mori-r30/MoriR30.SrcJournalctlBoot/` (`journalctl.c`, `journalctl-filter.c`,
   `journalctl-util.c`, `journalctl-util.h`, `journalctl.xml`, `journal-util.c`, `excerpt-body.txt`, `q1.txt`,
   `q2.txt`).
