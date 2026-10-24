# ReviewCorpus — round 16 review of source trio, quotes, immutable row cells and frontier

Reviewer seat: `MoriR16.ReviewCorpus` (leaf, read-only except this report).

## Read-time state (changes in flight; findings are read-time only)

- Repo HEAD: `b83edc6`. Working tree is dirty during this review:
  `M LOG.md`, `M PROVINCE.md`, `M SCORECARD.md`, `M corpus/QUALITY.md`,
  `M corpus/README.md`, `M corpus/SOURCES.md`; untracked
  `corpus/knowledge/journal-cursor-window-r16.md`, `corpus/lessons/round-16.md`,
  `.ufo/waves/round-16/`.
- `corpus/SOURCES.md` changed while I was reading it: 68 lines at my first read,
  74 lines at read time. Digest at 08:51Z: `44ade213…`. `corpus/README.md`: `fd150df9…`.
- `corpus/knowledge/journal-positive-evidence-r15.md` (digest `1653c8d0…`) and
  `corpus/knowledge/structured-journal-scopes-r13.md` (`d425b26a…`) are committed and unchanged at read time.

## Deviations (disclosed per L1 instruction)

1. I ran a `mktemp -d` call (inside a command that discarded its output). It creates an
   empty directory under `/tmp`. Its path was not retained, so I cannot name or remove it.
   This is an outside-lane, non-deliberate write; treat it as an inadmissible artifact.
2. A grep/curl pipeline exceeded the foreground limit and was backgrounded as `bg_2754`.
   It finished on its own, and its S015 output was used only as static source text.
   My attempt to kill it through `proc://bg_2754/kill` failed because proc is
   write-only. No further polling was performed.
3. No `journalctl` was run, no journal was read, and no build/test/gate/probe was executed.
   The work was web source reads (freedesktop.org man pages), read-only `git show`/`git diff`,
   `awk`/`grep` over files, and `sha256sum` of corpus files. No files were written except this report.

## Source trio verification (live primary pages, read 2026-10-20)

- S014 `journalctl.html`: sha256 `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722`.
  This matches the hash in `journal-positive-evidence-r15.md`.
- S015 `systemd.journal-fields.html`: sha256 `906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7`.
  This matches the r15 note.
- Quotes located verbatim on the live page (markup-stripped):
  - S014: "Journal entries permit non-unique fields…", "listing all field values as elements",
    "Fields larger than 4096 bytes are encoded as null values", "non-UTF8 bytes are encoded as arrays",
    "Show messages from a specific boot", "adds a match for `_BOOT_ID=`", "except when the current boot is not the last boot",
    "A comma separated list of the fields which should be included in the output", "The format of the cursor is private and subject to change",
    "Start showing entries from the location in the journal specified by the passed cursor",
    "…after the location specified by the passed cursor", "any warning messages regarding inaccessible system journals when run as a normal user".
  - S015: "A 128-bit message identifier ID for recognizing certain message types", "This should contain a 128-bit ID formatted as a lower-case hexadecimal string, without any separating dashes or suchlike", "recommended to be a UUID-compatible ID", "is not supposed to be parsed for metadata", "User fields are fields that are directly passed from clients", "Fields prefixed with an underscore are trusted fields", "The kernel boot ID for the boot the message was generated in", "The name of a unit. Used by the system and user managers when logging about specific units", "uniquely describes the position of an entry in the journal".
  - S039 page `sd_journal_seek_cursor.html`: "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead"; "do not actually make any entry the new current entry".
  - S040 page `sd_journal_test_cursor.html`: "cursor strings do not uniquely identify an entry", "the same entry might be referred to by multiple different cursor strings", "hence string comparing cursors is not possible", "whether the entry being sought to was actually found".
- Quote not present as worded: "writes the cursor of the last entry" was my test string. The page says "write the cursor of the last entry to FILE" (`--cursor-file=`). The r16 note paraphrases it without quote marks, so this is not a defect.

## Findings (severity order)

### F1 — Medium: `used-by` cells claim usage the knowledge note does not request
`SOURCES.md` in the working tree appends `journal-cursor-window-r16.md` to the used-by cells of
S013, S014, S015, S035 and S037. The r16 note's own "Mutable cells to change" list asks only for
S014 and S015, and says "S037 … no change". Its S013 mention is "not reopened here". The S013,
S035 and S037 used-by entries therefore record a source-use relationship the note disclaims or does not request.
Fix: remove the S013/S035/S037 appends, or have the note state the use.

### F2 — Medium: unsupported frontier claim for `-q` partial reads
`corpus/README.md` coverage row for `journal-cursor-window-r16.md` says "`-q`-hidden
inaccessible-journal partial reads stay unavailable or [UNKNOWN]". FR11 says "unreadable later
journal files under `-q` … remains open". The note itself handles only the fully-empty case
(Evidence §5 "quiet, empty stream", Delivery paths "a scope the user cannot read … no anchor record").
It never names partial reads as unavailable or [UNKNOWN]. The frontier therefore states a limit
the source note does not carry. Fix: add the partial-read case to the note's [UNKNOWN] or Delivery-paths sections.

### F3 — Medium: source line anchors do not reproduce against one declared rendering
Raw HTML served 2026-10-20 gives:
- `--system` 71, `--after-cursor=` 121, `--user-unit=` 151, `--output-fields=` 230, `-k` "This adds the match" 192,
  `Storage=` 76, `-q` "inaccessible system journals" 258, `Exit status` "On success" 352.
- S015: `User fields` 33, `MESSAGE=` id 34, `MESSAGE_ID=` id 40, `recommended to be a UUID` 42,
  `Trusted Journal Fields` 83, `_BOOT_ID=` id 100, `_TRANSPORT=` 106, `UNIT=` id 78.

Against that:
- SOURCES S014 `--after-cursor:187-190` and `--output-fields:489-492` do not match (121, 230).
- SOURCES S015 `_TRANSPORT=:204` does not match (106). `MESSAGE_ID=:41-44` is off by one (id at 40).
- `r12` note cites `journalctl -k:342`, `--output-fields=:489–494`, `_TRANSPORT:204–246`. None matches.
- `r13` note's anchors do match the raw HTML, except `-q :257` against raw 258.

The SOURCES correction line discloses the S014/S015 mismatch and says "for a future source-numbering pass".
Three numbering schemes now exist for one URL, and no note declares its rendering. Fix: name the rendering
(raw HTML, line-numbered) in SOURCES, or cite section headings only. No immutable cell should be rewritten; the correction stays append-only.

### F4 — Low/Medium: S039 alias not disclosed
The S039 URL `sd_journal_seek_cursor.html` serves a page with `<title>sd_journal_seek_head`. The
S039 row names `sd_journal_seek_cursor(3)` and does not disclose the alias. S040's row does disclose
its alias ("page served as sd_journal_get_cursor"). The quote is present on the served page, so the
quote is correct; only the label is incomplete. Fix: add the same parenthetical to S039.

### F5 — Low: precision of trust statement in r16 note
§3 and "Not claimed" say "of the requested output fields, only `_BOOT_ID` is trusted". S015 has an
"Address Fields" section, where `__CURSOR=` is journal-serialized and double-underscore prefixed.
That section is separate from "Trusted Journal Fields". The statement is defensible but should read
"`__CURSOR` is a journal-serialized address field, not client-supplied; `_BOOT_ID` is the only
trusted field the query depends on". The note's "`MESSAGE` is still read internally by the query
process" is unsourced and should be marked [INFERENCE].

### F6 — Low: r15 note omits the `--all` caveat behind the oversized-null rule
S014 says oversized fields are null "(This may be turned off by passing --all…)". The r15 predicates
rely on non-null scalars, so they depend on the query never passing `--all`. The note should state
that as a contract constraint.

### F7 — Low: stale frontier evidence
FR1 first evidence cites `knowledge/audit-r11.md:203-204` (D08 "system-journal coverage — still
absent"). That was true at r11 but superseded by r13/r14, which count system-journal records.
The citation is historical; a "superseded" pointer would prevent misreading.

### F8 — Low: broken cross-repo citation (pre-existing)
FR4 cites `../../fleet-ledger/.ufo/waves/kaika-w1/mori-state.md`. Relative to `corpus/`, the path
resolves to `/home/vgpnk/Projects/shokunin/fleet-ledger/…`, which does not exist. The FR3 kumitate path
does exist. The FR4 citation should be fixed or marked unavailable.

## Verified clean

- Immutable cells: for the 38 committed rows (S001–S038), columns id through recheck (cells 2–11)
  are byte-identical to HEAD. Only the `used-by` column changed, and only by suffix appends. The
  earlier apparent non-prefix result was a trailing-padding artifact in my comparison.
- New rows S039 and S040 are added after S038, with no change to any existing row's identity or status.
- Append-only correction and "Bounded search" blocks: 6 at HEAD, 8 at read time; prior text unchanged.
- S014 and S015 page hashes match the r15 note header.
- Frontier FR11 row now cites the r16 note and states the exact-anchor, same-boot limits; it is consistent with the note's claim section.
- Frontier FR1 r15 mixed-class wording matches the r15 note's own limits.

## Residual risk and verification gaps

- I did not check the host `journalctl` 261.2-1 behavior. The r16 note's version gap (§6) is stated as unverified, which is correct.
- The SOURCES file and the r16 note were still changing at read time. Re-review after settlement.
- No journal, census, fixture or gate evidence was examined. Claims about live counts are out of scope for this review.

## Checks for L1 after settlement (static, no execution)

- `git diff HEAD -- corpus/SOURCES.md`: confirm used-by appends match the note's request list (F1).
- Re-read `corpus/README.md` Frontier FR11 and the note's §5/Delivery paths together (F2).
- Decide one line-numbering rendering for S014/S015 (F3); fix S039 alias label (F4).
