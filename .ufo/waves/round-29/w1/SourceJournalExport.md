# SourceJournalExport — C2 frontier row: how journald renders `__MONOTONIC_TIMESTAMP`

Seat `MoriR29.SourceJournalExport`, 2026-10-22. Lane `mori-shokunin`, entering tip `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`;
claim contract `.ufo/waves/round-29/contract.md` at `8a45cefe84af0557b457308e4e0f679ca490f9e9`. Read-only seat: no lane
edit, no git/jj write, no subagent, no background job, and `tools/mori-oom-killers.py` was never opened, grepped or run.
No report under `.ufo/waves/round-26/`, `round-27/` or `round-28/` w1/w2 was opened. No tool was installed or upgraded.

## Behavior — what was done

1. Grepped the registry for the candidate URL first (`grep -c 'JOURNAL_EXPORT_FORMATS' corpus/SOURCES.md`), at
   2026-10-22T19:57:53Z: the candidate `https://raw.githubusercontent.com/systemd/systemd/v262/docs/JOURNAL_EXPORT_FORMATS.md`
   is already inside row **S122** (`corpus/SOURCES.md:128`), so it cannot become a new row.
2. Selected other primary files at the same release tag, fetched each by `curl` from `raw.githubusercontent.com`
   (HTTP 200), and recorded URL, access time and `sha256sum` of the fetched bytes. All quoted line numbers were read
   from those downloaded bytes with `awk`/`grep -n`, not from a rendering.
3. Verified the revision independently: `git ls-remote https://github.com/systemd/systemd 'refs/tags/v262*'` at
   2026-10-22T19:58:25Z gives annotated tag `1f7dffaf714cc4488159c498b7a17cf34c5a96d5` peeled to commit
   `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`, matching S122's anchor. The GitHub REST ref endpoint returned HTTP 403
   (rate limit, 280 B) at 19:58:18Z and was replaced by `ls-remote`; no repo was written.
4. Did not run the C2 counter, did not author or touch fixtures, did not edit `SOURCES.md`. The row below is a draft for
   L1, who assigns the id.

## Findings

### F1 — the candidate URL is a duplicate (reject, not a row)
`corpus/SOURCES.md:128` (row S122) already names `docs/JOURNAL_EXPORT_FORMATS.md` and admits its Journal JSON Format
section plus the `--output-fields=` always-kept set. Re-sourcing the same page would be a second row for one source.

### F2 — no dedicated `journal-export.c` exists at v262 (reject)
`https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-journal/journal-export.c` answered HTTP 404,
14 B, sha256 `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed`, body `404: Not Found`. At this tag the
export writer is `src/shared/logs-show.c:911` (`static int output_export(`). Anyone mapping the export format from a
newer branch should not assume that path exists at v262.

### F3 — the JSON value is a decimal string, and it is taken from the entry, not from the field list
Opened `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c` at 2026-10-22T19:56:08Z, 87,278 B,
sha256 `abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f`. At `:1266-1267` the writer does
`xsprintf(usecbuf, USEC_FMT, monotonic);` then `r = update_json_data(h, flags, "__MONOTONIC_TIMESTAMP", usecbuf, SIZE_MAX);`.
`update_json_data` turns printable ASCII into a JSON string (`utf8_is_printable` → `sd_json_variant_new_stringn`,
`:1126-1127`); its `null` branch needs `strlen(name) + 1 + size >= JSON_THRESHOLD`, and `JSON_THRESHOLD` is `4096U`
(`:43`, `:1124-1125`), far above this ~30-byte value. So `-o json` emits `__MONOTONIC_TIMESTAMP` as a JSON **string** of
decimal digits. The export writer in the same file prints `"__MONOTONIC_TIMESTAMP=" USEC_FMT "\n"` in the unconditional
header block (`:966-969`). Both sites live in S123's file, so this is corroboration only; the Gate below records a reject
for that URL.

### F4 — the stamp is stored in the entry object, so a valid entry always yields one
`journal-def.h:120` has `le64_t monotonic;` inside `EntryObject__contents` (macro opens at `:116`), i.e. it is part of
every entry's object header rather than one more entry in the data-field list. `sd-journal.c:2839-2841` reads
`uint64_t t = le64toh(o->entry.monotonic);` and returns `-EBADMSG` only when `!VALID_MONOTONIC(t)`. Writers that call
`sd_journal_get_monotonic_usec` therefore do not depend on a `__MONOTONIC_TIMESTAMP=` data field being enumerated.

### F5 — the export token is bare unsigned decimal, never quoted
`time-util.h:10-12` defines `PRI_USEC PRIu64` and `USEC_FMT "%" PRI_USEC`, so `USEC_FMT` is exactly `"%" PRIu64`
(unsigned decimal). Two export writers format with it: `journal-upload-journal.c:87-101` prints
`"__MONOTONIC_TIMESTAMP="USEC_FMT"\n"` once per entry (the entry state machine restarts at `ENTRY_CURSOR`, `:331`/`:391`),
and journald's forward-socket path synthesizes it at `journald-socket.c:146-154`, terminated by a blank line:
`xsprintf(monotonic_buf, "__MONOTONIC_TIMESTAMP="USEC_FMT"\n\n", ts->monotonic);`. Nothing quotes or escapes the value.

### F6 — the importer matches the line but parses leniently (not rowed)
`journal-importer.c:251-255` matches `__MONOTONIC_TIMESTAMP=` and calls `safe_atou64`; that forwards base 0
(`parse-util.h:86-88` → `safe_atollu_full(s, 0, ...)`, `parse-util.c:522`), and `mangle_base` accepts `0b`/`0o`/`0x`
prefixes (`parse-util.c:403-421`), with a bare leading `0` falling through to `strtoull(..., 0)`. It confirms the line
shape but cannot support a decimal-only claim, so it is excluded from the row and gets its own Gate reject.

### F7 — adjacency, not conflict
The round-29 w1 report `SourceJournalMonotonic.md` (seat `MoriR29.SourceJournalMonotonic`) rows the v262 manual page
`man/sd_journal_get_realtime_usec.xml` for the API semantics of the monotonic timestamp and its boot ID. This report rows
the storage and export-rendering code instead; the URL sets are disjoint, and the JSON string form stays with S122/S123.

## Draft row — `corpus/SOURCES.md` registry (11 columns, shape of `:8-15`; id assigned by L1)

```markdown
| S15x | systemd v262 entry-object monotonic stamp and its export-format rendering — https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-journal/journal-def.h ; https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-journal/sd-journal.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-socket.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/journal-remote/journal-upload-journal.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/time-util.h | code | A | the per-entry monotonic stamp at the v262 release tag: where the entry object stores it, the accessor that reads it, and the export-format writers that print it as a bare decimal line; not the JSON rendering (S122 carries the `--output-fields=` always-kept set and S123 the JSON field encoder that makes a printable value a string), not this host's journal, not a claim that a `__MONOTONIC_TIMESTAMP=` data field is present in every entry's enumerated field list | journal-def.h:120 (`le64_t monotonic;` inside `EntryObject__contents`, macro opens :116); sd-journal.c:2839-2841 (`le64toh(o->entry.monotonic)`, `-EBADMSG` when `!VALID_MONOTONIC`); journald-socket.c:146-154 (`Synthesise __REALTIME_TIMESTAMP and __MONOTONIC_TIMESTAMP`, `"__MONOTONIC_TIMESTAMP="USEC_FMT"\n\n"`); journal-upload-journal.c:87-101 (`case ENTRY_MONOTONIC`, `"__MONOTONIC_TIMESTAMP="USEC_FMT"\n"`); time-util.h:10-12 (`PRI_USEC PRIu64`, `USEC_FMT "%" PRI_USEC`); tag v262 = annotated tag 1f7dffaf714cc4488159c498b7a17cf34c5a96d5 peeled to commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492; HTTP 200 on 2026-10-22; sizes and sha256 journal-def.h 11,593 B 3ab41534b3d6ef19ada59f6df60c74742f2900a2c278980ea3d16b8379d8473d, sd-journal.c 128,242 B 36f5b8e64cd60b6843705734cc49fdf129c6740e236118f3cde6603c44ad726f, journald-socket.c 6,874 B 6cb575c9f43d1293004b2d6184826a4a819b222ad6fdcaa69a1778f8cda5d926, journal-upload-journal.c 17,651 B ff643fa4a9af51184e12aa4581b3e1b19f98d0d68a4b8d8cf6e41a4de81fd03f, time-util.h 10,883 B 45e934d294f2ff0ca92cc7f1fcede1ef92862d20b276e305282cec5f3cba37e6 | The monotonic stamp is a member of the entry object header, not of the enumerated field list, so every complete entry yields one; the export format prints it from that accessor as an unquoted unsigned decimal microsecond count (`USEC_FMT` is `"%" PRIu64`), never as a quoted string. | mined | 2026-10-22 | on-release | corpus/lessons/round-29.md, tools/fixtures/mori-oom-killers/cases-a2-r29.json |
```

## Gate — opened sources and rejects (shape of `corpus/lessons/round-28.md:63-72`)

```markdown
| id | source | access time | sha256 | located quote | decision |
|---|---|---|---|---|---|
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-journal/journal-def.h (with sd-journal.c, journald-socket.c, journal-upload-journal.c and time-util.h at the same tag) | 2026-10-22T19:57:34Z | `3ab41534b3d6ef19ada59f6df60c74742f2900a2c278980ea3d16b8379d8473d` | `journal-def.h:120` "le64_t monotonic;" (2 words); `sd-journal.c:2839-2841` "uint64_t t = le64toh(o->entry.monotonic); if (!VALID_MONOTONIC(t)) return -EBADMSG;" (8 words); `journald-socket.c:153` "xsprintf(monotonic_buf, \"__MONOTONIC_TIMESTAMP=\"USEC_FMT\"\\n\\n\", ts->monotonic);" (3 words); `journal-upload-journal.c:100-101` "r = snprintf(buf + pos, size - pos, \"__MONOTONIC_TIMESTAMP=\"USEC_FMT\"\\n\", monotonic);" (11 words); `time-util.h:12` "#define USEC_FMT \"%\" PRI_USEC" (4 words) | admit, A, mined |
| — | https://raw.githubusercontent.com/systemd/systemd/v262/docs/JOURNAL_EXPORT_FORMATS.md | 2026-10-22T19:57:53Z (grep only; URL not fetched) | — | `corpus/SOURCES.md:128` shows this URL inside row S122 | reject, duplicate URL already carried by S122 |
| — | https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-journal/journal-export.c | 2026-10-22T19:56:08Z | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` | body line 1 (3 words): "404: Not Found" | reject, HTTP 404 at v262 — no such file; the export writer is src/shared/logs-show.c:911 |
| — | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c | 2026-10-22T19:56:08Z | `abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f` | `:1266-1267` (11 words): "xsprintf(usecbuf, USEC_FMT, monotonic); r = update_json_data(h, flags, \"__MONOTONIC_TIMESTAMP\", usecbuf, SIZE_MAX);" | reject, duplicate URL already carried by S123 (corpus/SOURCES.md:129); JSON string form kept as corroboration only |
| — | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/journal-importer.c | 2026-10-22T19:57:34Z | `bfef6c03c28cc2f6fff3792dafb723a35c0831bc9b72ca4bd3ff6ea9eb9e0bdc` | `:251` (4 words): "value = startswith(line, \"__MONOTONIC_TIMESTAMP=\");"; `:255` (5 words): "r = safe_atou64(value, &x);" | reject, adds no format evidence: it only matches the field name and parses base 0 (parse-util.h:86-88), so it cannot support a decimal-only claim |
```

## Checks run

- Five raw GETs, all HTTP 200, sizes and digests as in the row anchor: `journal-def.h` 11,593 B; `sd-journal.c`
  128,242 B; `journald-socket.c` 6,874 B; `journal-upload-journal.c` 17,651 B; `time-util.h` 10,883 B
  (fetched 2026-10-22T19:57:34Z, `time-util.h` 19:58:18Z).
- `logs-show.c` GET HTTP 200, 87,278 B, 2026-10-22T19:56:08Z; `journal-export.c` GET HTTP 404, 14 B, same second.
- `systemd-v262.tar.gz` GET HTTP 200, 19,038,647 B, 2026-10-22T19:56:30Z, sha256
  `6aa77506c0644aa67f940a48e3d3a7368601f787e4f249139516d353f107bcab`; used only to confirm that the chosen files are the
  only v262 carriers of the literal `__MONOTONIC_TIMESTAMP` in C, Markdown and XML (eight files, of which the docs, two
  man pages and `logs-show.c` are already registered, and `log-generator.py` is a test fixture writer).
- Line numbers re-read from the downloaded bytes: `journal-def.h:116,120`; `sd-journal.c:2839-2841`;
  `journald-socket.c:146-154`; `journal-upload-journal.c:87,100-101,331,391`; `time-util.h:10-12`;
  `journal-importer.c:251-255`; `logs-show.c:43,911,966-969,1124-1127,1266-1267`; `parse-util.h:86-88`;
  `parse-util.c:403-421,522-557`.
- Not run: the C2 counter `count-c2.sh` (its case file does not exist yet and this seat authored none), any build,
  lint, test or formatter, and any `git`/`jj` write.

## Touched surfaces

- Wrote only `.ufo/waves/round-29/w1/SourceJournalExport.md` (this file).
- Scratch: `/fast/scratch/hyaku/mori-r29/MoriR29.SourceJournalExport/` holds the fetched bytes and the v262 tarball.
  Nothing else in the lane, the fleet root or a sibling lane was changed; lane git and jj state untouched.

## Out of scope / limits

- `corpus/SOURCES.md` was not edited. The row is a paste-ready draft; the literal `S15x` does not match the census row
  regex and must be replaced by L1 with the next free id (highest existing is S152, `grep -oE '^\| S[0-9]{3,}'`).
- Both `used-by` targets are forward references: `corpus/lessons/round-29.md` and
  `tools/fixtures/mori-oom-killers/cases-a2-r29.json` were absent at 2026-10-22T19:57:53Z. The census check "mined rows
  whose used-by paths do not exist" will flag this row until the round lesson lands and a C2 seat authors the case file.
- The topic's JSON half is already admitted: S122 (`corpus/SOURCES.md:128`) covers `--output-fields=` keeping
  `__MONOTONIC_TIMESTAMP`, and S123 (`:129`) owns `logs-show.c`. This row deliberately does not re-source either URL;
  the digest and quotes for `logs-show.c` above are corroboration for C2, not a row.
- The `journald-socket.c` path is journald's forward-socket export stream, not the local journal file writer; the
  "always present" claim rests on the entry-object header (F4), not on that path.
- GitHub REST was rate-limited (HTTP 403) once; the tag mapping was taken from `git ls-remote` instead. No other check
  was blocked.
- No tool installed, upgraded or restarted. No host unit, `/etc` file, harness setting or fleet script was touched.
