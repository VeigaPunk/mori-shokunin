# ReopenS153 — falsification of SOURCES row S153, its Gate lines and its `used-by` citations

Seat: MoriR29.ReopenS153. Lane tip inspected (read-only `git log -1 --format='%H %s'`, output
`8809a3fe1eaa87a0afa177a15263d174378e7462 round-29: rows S153-S155 (sourced, Gate with reject rows)…`).
Row: `corpus/SOURCES.md:159`. Gate: `corpus/lessons/round-29.md:55` (admit) and `:56` (reject).
Drafting report: `.ufo/waves/round-29/w1/SourceJournalMonotonic.md:26-27` (Gate table rows `S15x` and `—`);
its paste-ready row at `:40`, receipts at `:29-30`.
Nothing in the lane, the fleet, or the L1 judge scratch was written; only this Report. One incident: the `write`
tool resolved my relative Report path against the shell cwd (the fleet root) and created
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-29/w2/ReopenS153.md`; I moved that file here and removed the three
now-empty directories it had created (`w2`, `round-29`, the fleet-root `.ufo/waves` chain was pre-existing and left
untouched). `rmdir` removes only empty directories, so nothing else was created or deleted; the fleet-root `.ufo`
pre-dates this seat.

## Method (re-fetch, not re-read of receipts)

Fresh fetch into `/fast/scratch/hyaku/mori-r29/w2/ReopenS153/` at 2026-10-22T20:32:30Z:

```
200 5372 sd_journal_get_realtime_usec.xml
404 14 sd_journal_get_monotonic_usec.xml
dd224fc99710940d4e5d362aaa54768afc05dc1778c5cffa22595dbc1556d334  sd_journal_get_realtime_usec.xml
d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed  sd_journal_get_monotonic_usec.xml
119 sd_journal_get_realtime_usec.xml
```

Quotes and anchors were tested mechanically (tags stripped, whitespace collapsed, substring test and
first/last-word line test) rather than by eye.

## Claim table

| claim | recorded | observed | holds? |
|---|---|---|---|
| Row URL answers | `HTTP 200 on 2026-10-22` (`corpus/SOURCES.md:159` anchor cell) | HTTP 200, 5,372 B, 119 lines at 2026-10-22T20:32:30Z | yes |
| Page bytes for that URL | `dd224fc99710940d4e5d362aaa54768afc05dc1778c5cffa22595dbc1556d334` (`corpus/lessons/round-29.md:55`); row carries no sha256 of its own | `dd224fc…d334` (sha256sum, above) — identical | yes |
| Gate quote 1 text and line span | `:61-63` (22 words): "the monotonic clock begins new with every reboot, it only defines a well-defined point in time when used together with an identifier" (`round-29.md:55`) | 22 words; exact substring of tag-stripped text; first word on line 61, last word on line 63 (`segment: …Since the monotonic clock begins new…`) | yes |
| Gate quote 2 text and line span | `:82-85` (24 words): "If the boot ID parameter was passed NULL and the monotonic timestamp of the current journal entry is not of the current system boot" (`round-29.md:55`) | 24 words; exact substring; first word line 82, last word line 85 (`…system boot, -ESTALE is returned by…`) | yes |
| Anchor `:36-39` = signature with `sd_id128_t *boot_id` | `corpus/SOURCES.md:159` anchor cell | lines 36-39 = `int sd_journal_get_monotonic_usec sd_journal *j uint64_t *usec sd_id128_t *boot_id` | yes |
| Anchor `:55-69` = Description | same cell | lines 55-69 are the monotonic paragraph; contains `CLOCK_MONOTONIC` and "microseconds since boot-up of the specific boot" (line 60) | yes |
| Anchor `:80-86` = Return Value | same cell | lines 80-86 carry "If the boot ID parameter was passed NULL … not of the current system boot, -ESTALE is returned" | yes |
| Anchor `:100` = "both calls added in version 187" | same cell | line 100 alone: "sd_journal_get_monotonic_usec() were added in version 187."; both call names span lines 99-100 | yes for the fact; pointer one line short (see note N1) |
| `teaches`: stamp measured from boot-up of one specific boot | `corpus/SOURCES.md:159` teaches cell | line 59-61: "The timestamp is in microseconds since boot-up of the specific boot, i.e. CLOCK_MONOTONIC" | yes |
| `teaches`: begins new at every reboot | same | line 61-62: "Since the monotonic clock begins new with every reboot" | yes |
| `teaches`: point in time only with the boot ID | same | line 62-64: "it only defines a well-defined point in time when used together with an identifier identifying the boot" | yes |
| `teaches`: entry from another boot fails with `-ESTALE` | same | line 82-86: NULL boot ID + entry not of current boot → "-ESTALE is returned by sd_journal_get_monotonic_usec()" | yes (condition "NULL boot ID" is in the row's scope cell) |
| Scope: 128-bit third parameter receives the boot ID | `corpus/SOURCES.md:159` scope cell | line 58-59: "as well as a 128-bit ID buffer to store the boot ID of the monotonic timestamp"; third `paramdef` at line 39 | yes |
| Scope exclusion points at S122 for the JSON field / `--output-fields=` | same | `corpus/SOURCES.md:128` is S122 and names `--output-fields=` (journalctl.xml:667-675) and `__MONOTONIC_TIMESTAMP` (systemd.journal-fields.xml:656-665) at the same tag | yes |
| Scope exclusion "not kernel CLOCK_MONOTONIC behavior across suspend" | same | `grep -in 'suspend\|hibernate\|CLOCK_BOOTTIME'` on the fetched page → no match | yes (page is silent) |
| Tag mapping `v262 = 8cc40e0c…b492` | `corpus/SOURCES.md:159` anchor cell | `git ls-remote --tags https://github.com/systemd/systemd refs/tags/v262*` → `1f7dffaf…96d5 refs/tags/v262`, `8cc40e0c5e9234bf45084751ac53b1fbfe70b492 refs/tags/v262^{}` | yes |
| Page at that commit is the same bytes | implied by the mapping | raw fetch at `8cc40e0c…b492` → HTTP 200, 5,372 B, sha256 `dd224fc…d334`, identical | yes |
| Row shape | 11-column registry (`corpus/SOURCES.md:5` header: id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by) | `awk -F'|'` on line 159: 11 cells, 12 pipes, no empty cell; id appears once (`grep -cE '^\| *S153 \|'` → `1`) | yes |
| Vocabularies | row cells: `docs` / `A` / `mined` / `on-release` | all four are in the file's existing vocabulary (69 rows `docs`, 132 rows `A`, 98 rows `mined`+`on-release`) | yes |
| URL not duplicated | row is a new source (drafting report: count `0`) | `grep -c 'sd_journal_get_realtime_usec.xml' corpus/SOURCES.md` → `1`, only line 159 | yes |
| `used-by` cites S153 as a word (lesson) | `corpus/lessons/round-29.md` | `grep -nE '\bS153\b'` → `:20` ("meaningful only within its boot (S153)"), `:55` (Gate line), `:69` (row-change log) | yes |
| `used-by` cites S153 as a word (fixture) | `tools/fixtures/mori-oom-killers/cases-a2-r29.json` | JSON top-level `sources` = `["S153","S154","S155"]`; `"S153"` at file line 6, exact array element | yes |
| Both `used-by` paths exist | — | lesson 10,542 B, cases 54,620 B (`ls -l`) | yes |
| Reject URL returns 404 and its body hash | `round-29.md:56`: sha256 `d5558cd4…512ed`, "body line 1 (3 words): \"404: Not Found\"" | HTTP 404, 14 B; `od -c` → `4 0 4 :   N o t   F o u n d`; sha256 identical | yes |
| Reject reason: page carries both functions | `round-29.md:56` decision text | synopsis lines 35-40 declare `sd_journal_get_monotonic_usec`; Description 55-69 documents it; History 99-100 names both | yes |
| Gate line shape | 6-column Gate table (`round-29.md:52-53`) | lines 55 and 56 each 6 cells, 7 pipes | yes |
| Lesson claim supported | `corpus/lessons/round-29.md:20` "A journal entry's monotonic stamp is meaningful only within its boot (S153)" | directly follows the `:61-63` sentence the Gate quotes | yes |

## Notes (no recorded value falsified)

- **N1 — anchor `:100` is one line short of its own parenthetical.** The cell says ":100 (both calls added in
  version 187)"; line 100 holds only "sd_journal_get_monotonic_usec() were added in version 187.", the first call
  name sits on line 99. Version-187 fact holds; `:99-100` would match the wording. Cosmetic.
- **N2 — the admitted Gate quotes are prefixes cut at the word limit with no ellipsis.** Quote 2 stops at "system
  boot" and so omits the `-ESTALE` the row teaches; that fact is still inside the row's `:80-86` anchor span
  (line 85-86). Verbatim and within 25 words, so it is not a mismatch, but the quote alone under-evidences the
  strongest clause of `teaches`.
- **N3 — row carries no sha256 of its own.** Unlike S122 (`corpus/SOURCES.md:128`, which lists three sha256s in the
  anchor cell), S153's anchor cell records only the tag mapping and access date; the page hash exists only in the
  Gate line. The hash does match, so no claim is false; a future reader of the row alone cannot re-verify bytes.
- **N4 — the drafting report names the wrong line for the registry header.** It says "Exact 11-column shape of
  `corpus/SOURCES.md:8`" (`.ufo/waves/round-29/w1/SourceJournalMonotonic.md:35`), but line 8 is the S002 data row;
  the header is `corpus/SOURCES.md:5`. The committed row's shape is still correct (11 cells, verified against :5);
  only the drafting report's pointer is off.

## Unresolved / not verifiable here

- The Gate line's recorded access time `2026-10-22T19:55:54Z` is a statement about the drafting seat's own fetch.
  I cannot re-observe a past access time; my fetch of the same URL produced byte-identical content at
  2026-10-22T20:32:30Z, which is the substantive check.
- The drafting seat's GitHub-API receipts (tag ref 364 B `437155b1…`, tag object 2,699 B `d21f2d84…`, in
  `.ufo/waves/round-29/w1/SourceJournalMonotonic.md:29-30`) could not be re-hashed: `api.github.com` answered
  `403 {"message":"API rate limit exceeded for <egress IP redacted>.…"}` for both endpoints. The identifiers the receipts
  stand for were independently confirmed by `git ls-remote` (tag `1f7dffaf…96d5` → commit `8cc40e0c…b492`).

## Tooling

No tool installed, upgraded or removed; no pacman transaction attempted. Tools used: `curl`, `git ls-remote`
(read-only, network), `sha256sum`, `awk`, `grep`, `od`, `python3` (stdlib only). All writes confined to
`/fast/scratch/hyaku/mori-r29/w2/ReopenS153/` and this Report.
