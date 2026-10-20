# CursorDocs — journalctl cursor, `--no-tail`, and JSON field openings

Seat: `MoriR16.CursorDocs` (scout, leaf). Date: 2026-10-20.
Target: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Mode: static documentation review only. No live `journalctl` invocation, no journal read,
no build/test/lint/gate/selftest, no `/tmp` output, no outside-lane write. No deviation to
disclose. At this seat's read time `tools/mori-journal-window.py` was absent from the working
tree; no implementation was reviewed, so the contract mapping below is documentary evidence for
the tool owners and wave-2 review, not an implementation finding or a pass prediction.

## Question

Which documented `journalctl` cursor, `--no-tail`, `--quiet` and JSON-output semantics constrain
the round-16 new-since-anchor window, and which of them does the contract's first-record
anchor test actually rely on?

## Sources opened (all 2026-10-20, native HTML fetch, no file saved)

| id | document | URL | self-version |
|---|---|---|---|
| S014 | `journalctl(1)` — Print log entries from the systemd journal | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | systemd 262 |
| S015 | `systemd.journal-fields(7)` — Special journal fields | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | systemd 262 |
| S039 | `sd_journal_seek_cursor(3)` family — Seek to a position in the journal | https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html | systemd 262 |
| S040 | `sd_journal_get_cursor(3)` / `sd_journal_test_cursor(3)` | https://www.freedesktop.org/software/systemd/man/latest/sd_journal_get_cursor.html | systemd 262 |

S039/S040 are already present in the working-tree registry (`corpus/SOURCES.md:45-46`,
Registry-owned, not written by this seat). Quotes below were independently located from the URLs
above. Word counts are whitespace tokens after removing markup; every quote is ≤25 words.

## Located quotes

### S014 — `journalctl(1)`

- **Description, default range** — "If called without parameters, it will show the contents of the journal accessible to the calling user, starting with the oldest entry collected." (23)
- **`-c, --cursor=`** — "Start showing entries from the location in the journal specified by the passed cursor." (14)
- **`--after-cursor=`** — "Start showing entries from the location in the journal after the location specified by the passed cursor." (17)
- **`--cursor-file=` first sentence** — "If FILE exists and contains a cursor, start showing entries after this location." (13)
- **`--cursor-file=` fallback** — "Otherwise, show entries according to the other given options." (9)
- **`--cursor-file=` last sentence** — "At the end, write the cursor of the last entry to FILE." (12)
- **`-b, --boot`** — "Show messages from a specific boot. This will add a match for _BOOT_ID=." (13)
- **`-o json`** — "formats entries as JSON objects, separated by newline characters" (9)
- **`-o json`, size rule** — "Fields larger than 4096 bytes are encoded as null values." (10)
- **`-o json`, non-unique rule** — "if a non-unique field is encountered a JSON array is used as field value" (14)
- **`--output-fields=` applicability** — "This has an effect only for the output modes which would normally show all fields" (15)
- **`--output-fields=` always-printed set** — "For the former, the __CURSOR, __REALTIME_TIMESTAMP, __MONOTONIC_TIMESTAMP, and _BOOT_ID fields are always printed." (13)
- **`-n, --lines=`** — "Show the most recent journal events and limit the number of events shown." (13)
- **`-n` default** — "The default value is 10 if no argument is given." (10)
- **`-f, --follow` implies `-n`** — "If --follow is used, this option is implied." (8)
- **`--no-tail`** — "Show all stored output lines, even in follow mode. Undoes the effect of --lines=." (14)
- **`-q, --quiet`** — "any warning messages regarding inaccessible system journals when run as a normal user." (13)
- **`--show-cursor`, display position** — "The cursor is shown after the last entry after two dashes:" (11)
- **`--show-cursor`, format stability** — "The format of the cursor is private and subject to change." (11)
- **`--system` / `--user` default** — "If neither is specified, show all messages that the user can see." (12)
- **`--user` storage note** — "Note that --user only works if persistent logging is enabled, via the Storage= setting in journald.conf(5)." (16)
- **Description, file interleaving** — "Output is interleaved from all accessible journal files, whether they are rotated or currently being written" (16)
- **Exit status** — "On success, 0 is returned; otherwise, a non-zero failure code is returned." (12)

### S015 — `systemd.journal-fields(7)`

- **User Journal Fields intro** — "User fields are fields that are directly passed from clients and stored in the journal." (15)
- **`MESSAGE=`** — "is not supposed to be parsed for metadata." (8)
- **`MESSAGE_ID=` role** — "A 128-bit message identifier ID for recognizing certain message types, if this is desirable." (14)
- **`MESSAGE_ID=` enforcement** — "This is recommended to be a UUID-compatible ID, but this is not enforced" (13)
- **Trusted Journal Fields intro** — "Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly added by the journal and cannot be altered by client code." (24)
- **`_BOOT_ID=`** — "The kernel boot ID for the boot the message was generated in, formatted as a 128-bit hexadecimal string." (18)
- **Address Fields intro** — "these are not proper fields when stored in the journal but for addressing metadata of entries" (16)
- **Address Fields, match prohibition** — "They may also not be used as matches" (8)
- **`__CURSOR=` position** — "an opaque text string that uniquely describes the position of an entry in the journal" (15)
- **`__CURSOR=` portability** — "portable across machines, platforms and journal files" (7)
- **`__MONOTONIC_TIMESTAMP=` address rule** — "To be useful as an address for the entry, this should be combined with the boot ID" (17)
- **`UNIT=` / `USER_UNIT=`** — "Used by the system and user managers when logging about specific units." (12)

### S039/S040 — cursor API

- **Seek fallback** — "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead." (23)
- **Seek is not positioning** — "these calls do not actually make any entry the new current entry" (12)
- **Test after seek** — "sd_journal_test_cursor(3) may be used to verify whether the newly selected entry actually matches the cursor." (15)
- **Cursor representation** — "A cursor is a serialization of the current journal position formatted as text." (13)
- **Printable transport** — "The string only contains printable characters and can be passed around in text form." (14)
- **Opacity** — "The cursor string should be considered opaque and not be parsed by clients." (13)
- **Local absence fallback** — "Seeking to a cursor position without the specific entry being available locally will seek to the next closest (in terms of time) available entry." (24)
- **String identity limit** — "cursor strings do not uniquely identify an entry" (8)
- **Alias statement** — "the same entry might be referred to by multiple different cursor strings" (12)
- **No cursor comparison** — "string comparing cursors is not possible" (6)
- **Test result meaning** — "whether the entry being sought to was actually found in the journal or the next closest entry was used instead" (20)

## Findings

1. **`--cursor=` is inclusive; `--after-cursor=` is exclusive. [OBSERVED]** The first option starts
   "from the location"; the second starts "after the location". The contract's choice of
   `--cursor=` is therefore the only CLI form under which the anchor record itself is expected in
   the stream. The drop-first-record protocol depends on this inclusivity. `--after-cursor=` would
   skip the anchor without ever testing that it exists; a missing anchor would make the query start
   at an unknown later entry, with no record in the stream proving where the window actually began.
   A retained anchor with no newer records and an absent anchor with no later entry can both produce
   empty output, so the exclusive form cannot separate "quiet window" from "unresolved anchor". This
   is the documentary basis for the contract's prohibition.

2. **The cursor API treats a missing cursor as a seek to the next closest entry, not an error.
   [OBSERVED]** Both S039 and S040 state the fallback, and S039's return-value section says success
   is 0. S039 adds that a seek does not make an entry current until a subsequent positioning call,
   and names `sd_journal_test_cursor` as the verification step. `journalctl` exposes no test-cursor
   flag in S014. **[INFERENCE]** The only CLI-available test is comparing the first returned
   record's `__CURSOR` and `_BOOT_ID` to the anchor, and the CLI follows the same seek path.

3. **A first-record mismatch is refusal evidence only. [OBSERVED + INFERENCE]** S040 says cursor
   strings do not uniquely identify an entry and the same entry may have several strings. Therefore
   a byte mismatch can be an alias false-unavailable, not proof of vacuum, rotation or deletion.
   The contract's reason must be positional (`anchor-not-first-record` or equivalent) and must never
   name a cause. This matches the FR11 boundary in `PROVINCE.md:54`.

4. **The cursor is opaque printable text and an address field, not a stored field. [OBSERVED]**
   S040 says not to parse it; S014 calls the display format private and subject to change; S015
   places `__CURSOR` under Address Fields, says these are "not proper fields when stored" and "may
   also not be used as matches". **[INFERENCE]** Anchor validation is shape-only; the probe cannot
   use a `__CURSOR=` match to validate the anchor, cannot decompose a cursor into sequence or
   timestamp components, and must not scrape the `--show-cursor` text line. Mori's no-echo rule is
   policy, supported by — not mandated by — the opacity/private-format statements.

5. **`--output-fields=` cannot suppress four address fields. [OBSERVED]** In JSON modes the four
   address fields are "always printed" even if only `__CURSOR` and `_BOOT_ID` were requested.
   **[INFERENCE]** Captured journalctl stdout will always contain `__CURSOR`,
   `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP` and `_BOOT_ID` per record. The tool's own stdout
   no-echo rule is enforced at its output layer, not by field selection. Parsers must tolerate the
   two unrequested timestamp fields; a record-shape test asserting an exact key set equal to the
   requested list would contradict the man page. These extras are documented address metadata, not
   `MESSAGE` leakage.

6. **JSON record shape is object-per-line, but values can be arrays or null. [OBSERVED]** S014 says
   newline-separated JSON objects; non-unique fields become arrays; fields over 4096 bytes become
   `null` unless `--all`. **[INFERENCE]** A scalar cursor or `_BOOT_ID` that is an array, `null`,
   number, or object is invalid and must make the window unavailable. Do not add `--all`: it
   removes the 4096-byte null cap and enlarges capture without helping the probe. The anchor's
   4096-character cap is mori's schema, not a documented journal cursor limit.

7. **`--no-tail` undoes a line limit; it does not bound bytes, time, retention or completeness.
   [OBSERVED + INFERENCE]** `-n` shows "the most recent" events and carries a documented default of
   10 when no argument is given; `--follow` implies `-n`; `--no-tail` shows all stored lines and
   undoes `--lines=`. **[INFERENCE]** Without `-n`/`-f`, the start position is the only bound, so
   `--no-tail` acts as a documented guard against an injected or implied line limit rather than
   changing a default non-follow limit. It says nothing about
   vacuumed records, loss before storage, or an upper byte bound. `--max-bytes` and `--timeout` are
   wrapper-owned; overflow must be `rc2` unavailable, never a truncated positive window.

8. **`--quiet` suppresses information and access warnings, not the need for the anchor test.
   [OBSERVED + INFERENCE]** S014 says `-q` suppresses informational output and "any warning messages
   regarding inaccessible system journals when run as a normal user." A normal user can therefore
   receive rc0 with an empty stream for an unreadable scope. Because `--cursor=` is inclusive, a
   genuine zero-new-record window still contains the anchor record; empty stdout means the seek did
   not resolve to any entry, so it is unavailable, not `records_after_anchor=0`. Stderr absence is
   not access proof. Explicit `--system` or `--user` is required; omitting both shows "all messages
   that the user can see", mixing scopes.

9. **Boot selection is a match filter, not continuity proof. [OBSERVED + INFERENCE]** `-b` "will add
   a match for _BOOT_ID="; `_BOOT_ID` is a trusted, journal-added 128-bit hex field. A
   `-b`/`_BOOT_ID=` filter would silently exclude a foreign-boot record instead of letting the probe
   refuse the whole window. The contract's no-`-b` query plus a per-record `_BOOT_ID` check is the
   only form that can detect a boot boundary. First record and every later record must agree with
   the anchor boot; one foreign-boot record makes the entire window unavailable, not a same-boot
   subset.

10. **`--cursor-file=` and `--show-cursor` are excluded by their own documented behavior.
    [OBSERVED + INFERENCE]** `--cursor-file=` uses after-location semantics when the file exists and
    "at the end, write[s] the cursor of the last entry" — both an automatic cursor advance and an
    on-disk write, which the contract forbids, and it skips the anchor record. `--show-cursor`
    appends a private-format display line; parsing it contradicts the opacity/private-format
    statements. Use the JSON `__CURSOR` value only as data; if an end cursor is reported, report a
    SHA-256 digest and write nothing.

11. **Success rc is necessary but not sufficient. [OBSERVED + INFERENCE]** S014's exit status says 0
    on success and nonzero on failure; S039 says an absent cursor still seeks successfully. A
    zero exit therefore proves neither retention nor same-boot continuity. The first-record test,
    not the exit code, is the continuity proof.

12. **`MESSAGE` is a client user field; typed IDs are not authentication. [OBSERVED]** S015 says user
    fields are passed directly from clients, `MESSAGE` is not to be parsed for metadata, and the
    `MESSAGE_ID` UUID form is recommended but not enforced. The underscore fields alone are trusted.
    **[INFERENCE]** The MESSAGE-free query follows the documented role of the field, not merely a
    style preference. `MESSAGE_ID`, `UNIT_RESULT`, `EXIT_CODE` and `EXIT_STATUS` remain validated
    client records; the four positive counters remain evidence subsets, never an authenticated
    emitter or total.

## Contract mapping (advisory, for the tool/harness owners)

- Pass the anchor cursor verbatim to `--cursor=<anchor>`; never `--after-cursor=`, `--cursor-file=`
  or `--show-cursor`. Do not add `-b` or a `_BOOT_ID=` match.
- Pass explicit `--system` or `--user`; pass `--output=json --output-fields=__CURSOR,_BOOT_ID,...`
  with no `MESSAGE`, plus `--no-tail --quiet`. Do not add `--all` or `--follow`.
- The first parsed record must be a JSON object whose `__CURSOR` and `_BOOT_ID` are scalar strings
  exactly equal to the anchor; drop it. Every later record must be an object with the same scalar
  boot and a scalar cursor. Empty output, a non-object line, a null/array cursor or boot, a
  boot mismatch, any stderr, nonzero rc, timeout or byte overflow is `rc2` unavailable.
- `records_after_anchor=0` is valid only when the stream contains the anchor record and nothing
  after it. It is not an absence-of-events claim.
- Do not parse cursors, sort by cursors, or use byte cursor equality as entry deduplication. Unique
  scalar cursors are a contract-level rejection guard; the documents do not establish one-to-one
  entry identity.

## Corrections, registry and carry-forward

- **r13 correction (append-only).** `corpus/knowledge/structured-journal-scopes-r13.md:21,81`
  records `--after-cursor=` as the documented cursor mechanism. The r16 design uses inclusive
  `--cursor=` plus a first-record test because `--after-cursor=` cannot prove the anchor exists.
  `corpus/knowledge/journal-cursor-window-r16.md` already records this; the historical r13 file is
  not rewritten.
- **r15 quote status.** `RegistryFrontier`'s `--after-cursor=` quote is accurate but is not a
  presence proof. No r15 factual correction is needed from this lane.
- **Count note for the r16 lesson draft.** `corpus/lessons/round-16.md` lists `--cursor=` as 13
  words; whitespace count is 14. Its `--boot` match sentence counts 7 alone (13 with the preceding
  sentence), not 10. All remain ≤25; this is a count-accuracy note for the append-only reconciliation,
  not a claim dispute.
- **Registry (observed, not written here).** `corpus/SOURCES.md` currently has S014 and S015 with
  r16-note used-by, and S039/S040 added in the uncommitted working tree. New quotes above fall
  inside S014's existing scope (source/filter/output options) and S015's field scope. No new row is
  needed from this lane. One scope-label observation: S015's anchor names MESSAGE/MESSAGE_ID/
  `_TRANSPORT`, while r16 relies on Address Fields (`__CURSOR`) and `_BOOT_ID`; r13 already cited
  `__CURSOR` under S015, so this is a pre-existing label gap, not a missing source. The Registry
  seat/L1 decide any append; immutable cells are not rewritten here.
- **C15-4 active fix (observed, not written here).** The stale prose the r16 lesson draft cites at
  `SKILL.md:134` is absent from the current working tree. `SKILL.md:169` now states that the r15 CLI
  has no hidden flags, that `--selftest-child` and `--no-frozen-control` were removed, and that any
  unknown argument is refused by argparse with rc2. This seat edited nothing; the draft's "OPEN"
  status is stale as of this read and L1 should reconcile it append-only.
- **Old drift pin.** Not executed, not re-pinned, not turned green. The r10 drift debt (C15-5)
  remains red and status-neutral.
- **Round-15 procedural feedback.** No new deviation: this lane wrote only this report, used no
  `/tmp`, ran no checks, and made no broadcast.

## Remaining unknowns

- Whether the host `journalctl` (peer-reported systemd 261.2-1; this seat did not run
  `journalctl --version`) implements the documented 262 seek fallback identically. No live query was
  made; 262 semantics are not transferred to the host by this report.
- Whether a live journal can present the anchor entry under a different cursor string than the one
  stored, and how often. S040 says aliases are permitted; frequency is unmeasured.
- Whether two distinct entries can ever share one cursor string. The opened pages do not establish
  this; no uniqueness/dedup claim is made.
- Whether `--quiet` alone guarantees a JSON-only stdout stream in every failure mode. The man page
  does not specify the stream of informational messages, so the probe still parses every line and
  refuses on anything non-object.
- Retention, vacuum and rate-limit behavior that determines which records survive to be returned;
  journald configuration documents were not opened this round.

No claim here is a gate, admission decision or outside verification; this is author-lane advisory
evidence for L1's integration read.
