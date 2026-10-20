# FieldDocs — S014/S015 field limits for the round-16 journal window

- Seat: `MoriR16.FieldDocs` (scout, leaf). Owned file: this report only.
- Read time: 2026-10-20. Target: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
- Method: static reads only. Primary man pages and API pages were fetched; local spec, fixtures and knowledge notes were read; the pinned systemd implementation source for JSON serialization was read. No `journalctl` invocation, no cursor read, no fixture/harness/tool/selftest/gate/smoke/formatter run, no build/test/lint. No writes outside this report. No `/tmp` output, no outside-lane staging.
- Disclosure: several static `ls`/`cat`/`curl` reads were momentarily backgrounded by the shell; each was killed or collected before this report. They produced only static file/source text. No live probe, no synthetic/fixture run, no journal query, no outside-lane write occurred.
- Read-time state: `tools/mori-journal-window.py` and `tools/mori-round16-regressions.py` were **absent** at my last static check. `.ufo/waves/round-16/fixtures/`, the spec and `corpus/knowledge/journal-cursor-window-r16.md` were present. This report reviews field/query **sources**, not delivered code; wave2 code review is out of scope.
- Tools installed/updated: none.

## Axes

- **Coverage**: pin the exact documented limits that the window's anchor continuity, boot check, MESSAGE-free query and client-set classification depend on.
- **Harm**: prevent overclaims (cursor identity, authenticated emitter, unique victim, completeness), prevent cursor parsing, and prevent a boot filter that turns a reboot into a false clean zero.

Confidence tags: **[DOC]** observed in S014/S015/S039/S040, **[SRC]** observed in the pinned systemd implementation source at commit `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af`, **[INFERENCE]** derived from the sources, **[UNKNOWN]** not established.

## 1. Sources opened

| Key | Document | Sections used | Use |
|---|---|---|---|
| S014 | `journalctl(1)`, systemd 262, https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | Source Options; Filtering Options (`--cursor`, `--after-cursor`, `--cursor-file`, `--boot`); Output Options (`json`, `--output-fields`, `-n`, `--show-cursor`, `--no-tail`, `-q`); Exit status | Query shape, output encoding, quiet/access caveat |
| S015 | `systemd.journal-fields(7)`, systemd 262, https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | Description; User Journal Fields; Trusted Journal Fields; Fields to log on behalf of a different program; Address Fields | Cursor meta-field, `_BOOT_ID` trust, `MESSAGE_ID`/`MESSAGE`, client vs trusted fields |
| S039 | `sd_journal_seek_cursor(3)` (served with `sd_journal_seek_head`), https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html | Description, Return Value | Seek and next-closest fallback |
| S040 | `sd_journal_get_cursor(3)` / `sd_journal_test_cursor(3)`, https://www.freedesktop.org/software/systemd/man/latest/sd_journal_get_cursor.html | Description, Return Value | Cursor opacity, printable text, non-identity |
| — | Journal Export Formats, https://systemd.io/JOURNAL_EXPORT_FORMATS/ | Journal JSON Format | Addressing fields, null/array encoding, unknown-field rule |
| [SRC] | `src/shared/logs-show.c` and `src/journal/journalctl.c` at commit `cf8ebfc6` | `JSON_THRESHOLD`, `update_json_data`, `update_json_data_split`, `journal_entry_to_json`; option/default handling | Implementation confirmation of always-printed fields, null threshold, `_BOOT_ID` source, JSON quiet flag |

Note: the numeric anchors in `corpus/SOURCES.md` for S014/S015 (for example `--after-cursor:187-190`, `--output-fields:489-492`) did **not** reproduce from the rendered pages. This report cites section names and verbatim quotes instead. Registry already logged this discrepancy; FieldDocs confirms it.

## 2. Findings

### D1. Cursor is opaque, printable text; exact equality is a conservative gate, not identity proof — high confidence [DOC]

**Documented nature.**

- S040: a cursor is "a serialization of the current journal position formatted as text"; "The string only contains printable characters and can be passed around in text form."; "The cursor string should be considered opaque and not be parsed by clients."
- S014 `--show-cursor`: "The format of the cursor is private and subject to change."
- S015 `__CURSOR=`: "The cursor for the entry. A cursor is an opaque text string that uniquely describes the position of an entry in the journal and is portable across machines, platforms and journal files."

**Entry identity is not one-to-one.**

- S040: "cursor strings do not uniquely identify an entry: the same entry might be referred to by multiple different cursor strings, and hence string comparing cursors is not possible."
- S040: "Seeking to a cursor position without the specific entry being available locally will seek to the next closest (in terms of time) available entry."
- S039 repeats the fallback: "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead."

Consequences for the window:

1. **Mismatch must refuse, and the reason must be observational.** A first-record cursor mismatch means only "the first returned record is not the anchor string". It does not establish vacuum, rotation or absence. A reason such as `anchor-not-first-record` is defensible; `anchor-vacuumed` or `anchor-missing` is not.
2. **Match is an operational gate, not proof of entry identity.** The same entry can have alias strings, and the format is private and may change. A byte-equal first record is the best available CLI evidence, but the claim is "the capture started at a record whose `__CURSOR` string and trusted `_BOOT_ID` match the anchor", not "the cursor globally identifies the entry".
3. **Never parse cursor components.** The fixture cursors visibly contain `;b=<boot>;`, `i=`, `m=`, `t=`, `x=`, and sometimes `p=`. Those components are not a contract. Parsing `b=` to obtain a boot id would both violate S040 and duplicate a field that is already trusted (`_BOOT_ID`). The cursor must be compared as one opaque string.
4. **No uniqueness claim.** The docs do not establish that distinct entries always have distinct cursor strings. The interface's "unique valid scalar cursor" for every later record, with the seen-set seeded by the anchor, is a conservative ambiguity gate. It is not dedup, not a global uniqueness assertion, and a duplicate observed string should refuse rather than be merged.

**Length/character policy.**

- Printable is documented; an exact maximum length is not. S014's JSON limit is the closest documented bound: "Fields larger than 4096 bytes are encoded as null values. (This may be turned off by passing `--all`, but be aware that this may allocate overly long JSON objects.)"
- [SRC] The implementation threshold is stricter than the man-page wording. `logs-show.c` has `#define JSON_THRESHOLD 4096U` and applies `if (!(flags & OUTPUT_SHOW_ALL) && strlen(name) + 1 + size >= JSON_THRESHOLD)` before emitting `null`. For the field name `__CURSOR` (8 characters), the null boundary is cursor length `>= 4087`, not `> 4096`. An anchor cursor accepted at 4087–4096 bytes could therefore never match a JSON record cursor. The interface's `<= 4096` cap is safe in the refusal direction but contains a dead band. If setup should reject only unmatchable anchors, cap at `<= 4086`; otherwise keep 4096 and document the unavoidable refusal. This is a policy choice, not a doc requirement.
- "Printable" is not an enumerated charset. A policy of printable ASCII (or printable UTF-8 without controls) is defensible; a stricter policy only risks false SETUP refusals. Pass the cursor as one argv token, `--cursor=<value>` in a list argv, so a leading `-` cannot be re-parsed as an option.

**Cursor is journal-generated addressing metadata, not a client field.**

- S015 Address Fields: double-underscore fields "are not proper fields when stored in the journal but for addressing metadata of entries. They cannot be written as part of structured log entries via calls such as `sd_journal_send(3)`. They may also not be used as matches for `sd_journal_add_match(3)`."
- Therefore a record's `__CURSOR` is not client-writable and cannot be used as a query match; the window can only seek with it. The anchor **file** is still local, unauthenticated state: its schema check proves shape, not who wrote it.

### D2. Boot trust: `_BOOT_ID` is trusted; the anchor boot is an unauthenticated claim; never add `-b` — high confidence [DOC] + [SRC]

**Documented trust.**

- S015 Trusted Journal Fields: "Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly added by the journal and cannot be altered by client code."
- S015 `_BOOT_ID=`: "The kernel boot ID for the boot the message was generated in, formatted as a 128-bit hexadecimal string."
- S014 `--output-fields=`: for JSON and the other full-field modes, "the `__CURSOR`", "`__REALTIME_TIMESTAMP`", "`__MONOTONIC_TIMESTAMP`", and "`_BOOT_ID`" fields are always printed."
- S014 `-b`: "Show messages from a specific boot. This will add a match for `_BOOT_ID=`." An empty argument selects the current boot.

**Implementation confirmation.** [SRC] `journal_entry_to_json` in `logs-show.c` inserts `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `_BOOT_ID`, `__SEQNUM` and `__SEQNUM_ID` unconditionally (around lines 1251–1274). `update_json_data_split` explicitly skips a regular data field beginning `_BOOT_ID=` (around line 1171) and the emitted `_BOOT_ID` comes from the journal API's boot id. The JSON `_BOOT_ID` is therefore the journal's trusted value, not a record-stored field. This is stronger than the man-page wording and supports the per-record comparison.

**Anchor trust ceiling.**

- The anchor's `boot_id` is external state. A 32-lowercase-hex check is shape validation only. The first-record check pairs the anchor cursor string with the anchor boot id; together they prove the capture started at the claimed record of that boot. They do not authenticate the anchor writer. If the anchor file is tampered to another real record, the window anchors there; that is still a genuine same-boot record, but its provenance is outside this probe.
- A later record with missing, `null`, array, object or non-string `_BOOT_ID`, or a scalar other than the anchor boot, makes the whole window unavailable. Do not drop foreign-boot records and keep the rest; that would present a same-boot segment as the whole window.

**Do not add `-b` or a `_BOOT_ID=` match.** This is the highest-risk "helpful optimization".

- `-b` adds a `_BOOT_ID=` match. If the window filtered to the anchor boot, a reboot's new-boot records would be excluded from the stream. The stream could then contain only the anchor record, yielding `rc0`, `records_after_anchor: 0` — a false "no new records" success across a reboot.
- The contract's query has no `-b` and no `_BOOT_ID=` match. That is what allows a new-boot record to appear and trigger `unavailable`. Adding the match would break the boot-boundary refusal.
- Residual: if no new-boot record is returned (for example because the query reaches the end of the retained journal before any new-boot entry), the reboot is undetectable. The window is then a valid anchor-boot window, not proof that no reboot occurred. Use "anchor boot", never "current boot".
- `_BOOT_ID` is not a machine identity. S015 calls cursors "portable across machines, platforms and journal files"; the query does not request `_MACHINE_ID`. No same-machine or cross-machine claim is made.

### D3. `MESSAGE_ID` and the result fields are client-set, not authenticated — high confidence [DOC]

**Field classes.**

- S015 Description: journal entries have "field values that may include binary data, and with non-unique field names permitted"; "New fields may freely be defined by applications".
- S015 User Journal Fields: "User fields are fields that are directly passed from clients and stored in the journal."
- S015 SYSLOG fields: "Note that the journal service does not validate the values of any structured journal fields whose name is not prefixed with an underscore, and this includes any syslog related fields such as these."
- S015 `MESSAGE_ID=`: "A 128-bit message identifier ID for recognizing certain message types, if this is desirable. This should contain a 128-bit ID formatted as a lower-case hexadecimal string, without any separating dashes or suchlike. This is recommended to be a UUID-compatible ID, but this is not enforced, and formatted differently."
- S015 `MESSAGE=`: "The human-readable message string for this entry... and is not supposed to be parsed for metadata."

**Limits this imposes on the four positive tokens.**

1. **`MESSAGE_ID` is a client-supplied type label.** Any process able to write to the queried journal scope can set any value; journald does not validate its format. A matching ID classifies a claimed message type. It does not authenticate the emitting process, prove that a kill occurred, or identify a victim.
2. **Exact scalar equality only.** A `MESSAGE_ID` that is an array (permitted non-unique field), `null` (oversize JSON encoding), a number, or a differently-cased/whitespace-padded string is not a match. No prefix, substring, case-fold, trim or catalog lookup may repair it. The r15 predicate set is the right conservative reading.
3. **The result fields have the same trust class.** `UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS`, `UNIT` and `USER_UNIT` are User Journal Fields. Of the fields the window requests, only `_BOOT_ID` is trusted. `positive_unit_oom`, `positive_unit_signal` and `positive_process_sigkill` therefore count writer-claimed structured values in the anchor boot, not manager-authenticated facts. They remain record witnesses, never victim counts, cause claims or severity overrides.
4. **`positive_kernel_oom` is a notice class.** The r15 predicate is the exact `fe6faa94e7774663a0da52717891d8ef` catalog notice ("A process of @UNIT@ unit has been killed by the OOM killer"), not a kernel-transport record. The window does not request `_TRANSPORT`, so it cannot and must not claim a kernel-origin record. Keep the r15 notice wording.
5. **`MESSAGE` is never requested and never matched.** "Never emitted" is the claim; journalctl may still read the field internally. S015's "not supposed to be parsed for metadata" is the reason the window must not fall back to text.

**Strongest sentence the probe supports:** "In this capture, the first returned record carried the anchor's exact cursor string and trusted `_BOOT_ID`; the following N records were scalar-cursor objects with the same trusted boot; of those, k satisfied the r15 scalar predicates." It does not support "authenticated emitter", "unique victim", "complete window", "kernel-caused", or "fleet-caused".

### D4. Query-shape facts the field docs force — high confidence [DOC] + [SRC]

| Option | Documented behavior | Consequence for the window |
|---|---|---|
| `--cursor=` | "Start showing entries from the location in the journal specified by the passed cursor." (inclusive) | The first record is the anchor if it is retained. Drop exactly one record only after cursor **and** boot match. |
| `--after-cursor=` | "Start showing entries from the location in the journal after the location specified by the passed cursor." | Forbidden. It skips the anchor without proving it exists; a missing anchor would look like a successful window. |
| `--cursor-file=` | "If FILE exists and contains a cursor, start showing entries after this location... At the end, write the cursor of the last entry to FILE." | Forbidden twice: after-semantics with no anchor proof, and cursor state mutation. The tool writes nothing. |
| `--no-tail` | "Show all stored output lines, even in follow mode. Undoes the effect of `--lines=`." `-n` has a documented default of 10. | Keep it. Without it a tail/line limit can silently truncate the stream, producing a false zero or hiding a malformed/foreign record. |
| `--system` / `--user` | "Show messages from system services and the kernel (with `--system`). Show messages from service of current user (with `--user`). If neither is specified, show all messages that the user can see." `--user` "only works if persistent logging is enabled, via the `Storage=` setting". | Pass exactly one scope flag. Without one the stream mixes accessible journals and the counts are mislabelled. A missing user journal surfaces as unavailable, not a clean zero. |
| `--output-fields=` | Affects verbose/export/json modes and `cat`; for those, `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP` and `_BOOT_ID` are always printed. | Requesting `__CURSOR`/`_BOOT_ID` is redundant but harmless. `MESSAGE_ID`, `UNIT_RESULT`, `EXIT_CODE` and `EXIT_STATUS` are **not** always printed; omitting any of them silently removes the predicate field and turns a positive into zero. The parser must tolerate the four always-printed keys plus `__SEQNUM`/`__SEQNUM_ID` and future double-underscore fields. |
| `-o json` | "formats entries as JSON objects, separated by newline characters". | One JSON object per line; no surrounding array. A blank or non-object line is malformed. |
| `--all` | Disables the >4096-byte `null` encoding, "but be aware that this may allocate overly long JSON objects." | Do not use. The max-bytes bound must still hold; `--all` weakens the serializer's natural per-field bound. |
| `--show-cursor` | Prints the cursor "after two dashes"; "The format of the cursor is private and subject to change." | Do not parse or echo the raw cursor. If an end cursor is reported, hash the cursor string with a pinned digest input; report only the digest. |
| `-q` / `--quiet` | "Suppresses all informational messages (i.e. '-- Journal begins at …', '-- Reboot --'), any warning messages regarding inaccessible system journals when run as a normal user." | Empty stderr is not access or completeness proof. An empty stdout with rc0 is possible (the "no entries" informational message is suppressed), and it is unavailable because the anchor was not observed. |
| Exit status | "On success, 0 is returned; otherwise, a non-zero failure code is returned." No codes are enumerated. | Treat any nonzero rc as unavailable without inventing meaning for the number. A wrapper timeout kill is not a journalctl semantic code. |
| Timeout | No journalctl option. | The tool's timeout is policy. On timeout, discard the partial stream; do not parse it. |
| Overflow | No journalctl option. | The tool's byte cap is policy. On overflow, discard; do not keep a prefix. |

**JSON quiet is automatic.** [SRC] `journalctl.c` sets `arg_quiet = true` when the output mode is export/JSON (around lines 649–650). The man page attaches access-warning suppression to `-q`. Therefore the JSON query is already quiet even before the explicit `--quiet`, and stderr silence is even weaker as an access proof. The explicit `--quiet` is redundant but harmless.

**No-pager note.** The man page describes paging as a tty behavior; the window captures stdout through a pipe. `--no-pager` is not in the interface list and is not required for a piped capture. This is [INFERENCE]; no live check was made.

### D5. JSON encoding facts and parser consequences — high confidence [DOC] + [SRC]

- **Values are strings, `null`, or arrays.** S014 documents the three exceptions: oversize fields become `null`; non-unique fields become arrays; non-printable/non-UTF8 bytes become arrays of unsigned byte numbers. The Journal Export Formats JSON section repeats the same rules.
- **`__CURSOR` validity.** A record cursor must be a scalar string. `null`, an array, a missing key, a number or an object is `record-invalid` and makes the whole window unavailable. This is the correct strict reading: the record count would otherwise be a partial total.
- **`MESSAGE_ID` and result fields may be non-scalar without invalidating the record.** An array or `null` `MESSAGE_ID` means the record is a valid record but not a positive witness. The same applies to `UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS`. This matches the r15 aggregate/positive distinction.
- **Extra keys are guaranteed.** [SRC] `journal_entry_to_json` unconditionally adds `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `_BOOT_ID`, `__SEQNUM`, `__SEQNUM_ID` (around lines 1251–1274). The man page names only four of these; the JSON format document says "Additional fields prefixed with two underscores might be added later on, your parser should skip over the fields it does not know." Field order is undefined. A parser that requires an exact key set, or rejects unknown keys, will reject every real record. Require only the keys the predicates use and ignore the rest.
- **`_BOOT_ID` is not filtered by `--output-fields`.** [SRC] `update_json_data_split` skips regular data beginning `_BOOT_ID=`; the emitted value comes from the journal API. Requesting `_BOOT_ID` is redundant but confirms intent; the parser must still reject a non-scalar or missing `_BOOT_ID`.
- **`--output-fields` does not warn on unknown names.** [SRC] The set is consulted with `set_contains`; names not present in a record simply do not appear. No stderr is generated. Consequently `__CURSOR` in the field list is harmless, and a misspelled predicate field is a silent coverage loss, not a visible error.
- **Corrupt entries can be skipped silently.** [SRC] `journal_entry_to_json` returns 0 (skips the entry) on journal-corruption errors while fetching cursor/timestamps/seqnum, and `sd_journal_enumerate_data` skips unreadable messages with a debug log. A JSON stream can therefore omit a corrupt entry without a nonzero rc or stderr. The window cannot detect a skipped entry between two valid cursors. This is a source-level residual for the host build; it reinforces "no completeness claim".
- **Synthetic streams vs real journalctl.** Real journalctl JSON field values are strings, `null`, or arrays (plus the address strings). Booleans, JSON numbers, and floats are not the documented encoding for these fields. The fixtures use them to attack the parser; predicates must reject them. For `EXIT_STATUS`, the documented normal encoding is the string `"9"`; r15's wording "scalar equal to 9" and the harness fixtures also probe `true`/`false`. Pin the accepted set explicitly (string `"9"` is the safe journalctl reading; any acceptance of integer `9` is an additional policy choice and must still reject `true`, `9.0`, arrays and `null`).

### D6. Corrections and gaps in `corpus/knowledge/journal-cursor-window-r16.md` (advisory; append-only; I do not edit that file)

1. **"The fields the query requests are all that are emitted" is false.** The same note cites S014 correctly: `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP` and `_BOOT_ID` are always printed; the pinned source adds `__SEQNUM` and `__SEQNUM_ID`. Correct wording: "The query's field list is all that is *requested* for regular fields; the JSON object additionally carries the always-printed addressing fields, so the parser must tolerate extra keys."
2. **"No dedup by cursor" conflicts with the interface's uniqueness rule.** The note says byte equality is "an acceptance test for the first record only"; the interface requires every later record to have a unique valid scalar cursor, and ReviewAnchor recommends seeding the seen-set with the anchor. Correct wording: cursor equality is also used as a conservative duplicate-string refusal gate for later records; it is not used to merge counts, deduplicate records, or assert global cursor uniqueness.
3. **"The CLI therefore does not fail when the anchor is absent" is an inference, not S014 text.** S039 is a library API; S014 does not state that the CLI implements `--cursor` through `sd_journal_seek_cursor`. Correct wording: "If the CLI implements the documented seek semantics, a missing anchor starts at a neighbour; if it fails instead, rc is nonzero. Either path refuses; the reason is observational." The Registry note already makes this distinction; the knowledge note should match it.
4. **Numeric anchors in `corpus/SOURCES.md` do not reproduce from the rendered pages.** Cite section names and verbatim quotes. This is already logged by Registry; FieldDocs confirms it independently.
5. **Host version gap.** The pages are systemd 262; the host reports systemd 261.2-1. Cursor format is private and subject to change. Receipts must record `journalctl --version`; no 261/262 equivalence claim. This is already in the note's UNKNOWN section; keep it explicit.
6. **"Same-boot" should be "anchor-boot".** The query does not pass `-b`; the window is same-**anchor**-boot. A reboot is caught only if a new-boot record is returned. This is currently implicit in the note and should be explicit in every claim.
7. **Add the non-validation and non-unique quotes to the trust section.** "Only `_BOOT_ID` is trusted" is correct, but the *why* is missing: non-underscore fields are passed from clients and not validated, `MESSAGE_ID` format is not enforced, and fields may be non-unique. Without these, "client-supplied" looks like a stylistic label rather than a hard limit.
8. **Empty stdout with rc0 is documented-possible.** The note treats empty as unavailable; add the reason: `-q` suppresses the informational "no entries" message, and exit status is 0 on success. Empty is unavailable because the anchor is unproven, not because journalctl necessarily failed.
9. **The note's end-cursor statement is sound.** S014 calls the format private; report only a digest with a pinned input. No correction needed.

### D7. Remaining unknowns

- Whether the **host** `journalctl` 261.2-1 actually applies `sd_journal_seek_cursor`'s next-closest fallback for `--cursor=`. No execution was performed; the refusal design holds under either fallback or failure, but the exact reason path on the host is unmeasured.
- How often a retained entry is presented under a different cursor string (alias), and whether two distinct entries can ever share a cursor string. S040 establishes non-uniqueness of strings per entry, not the converse. The wrapper must not claim global uniqueness either way.
- Whether journal rotation/renaming changes the cursor string of an unchanged entry, and whether an anchor recorded under one systemd version byte-matches under another. Format is private; not measured.
- Whether `--system` or `--user` include imported/remote journal files in the host configuration, and whether cursor portability across machines could make a foreign copied entry satisfy the anchor. The query does not request `_MACHINE_ID`; no same-machine claim is made.
- The snapshot/atomicity semantics of a non-follow window under concurrent writes and rotation. S014 does not promise a point-in-time snapshot; no consistency or completeness claim is made.
- Journald retention, vacuum, rate-limit and loss behavior. The journald configuration/retention pages were not opened by this seat; window counts are retained-returned-record lower bounds.
- Whether `-q` suppresses every possible stderr diagnostic, not only the informational and inaccessible-journal warnings named by the man page. Empty stderr remains not an access proof.
- The host build's corrupt-entry skip behavior versus the pinned commit's `logs-show.c`. The source shows silent skips; the host was not measured.
- Live counts, window sizes and any positive values. None were measured.

## 3. Handoff checks for the implementer / L1 (advisory; no execution by this seat)

1. **Argv**: `--user` or `--system` exactly one; `--cursor=<anchor>` as one list-argv token; `--no-tail`; `--output=json`; `--output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS`; no `-b`/`_BOOT_ID=` match; no `--after-cursor`; no `--cursor-file`; no `--all`; no `--show-cursor` raw; no `MESSAGE` output or match.
2. **Parser**: split on newlines; each non-empty line must parse to a JSON object; reject duplicate keys, `NaN`/`Infinity`, non-object top-level values; tolerate `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `__SEQNUM`, `__SEQNUM_ID` and any future double-underscore fields; do not require an exact key set or a field order.
3. **First record**: exact string equality on `__CURSOR` and exact scalar equality on `_BOOT_ID` to the anchor; drop exactly one record only after both match. A missing/null/array cursor or boot → unavailable, not "skip and retry".
4. **Later records**: every record must be an object, same `_BOOT_ID` scalar, and carry a unique valid scalar printable cursor; seed the seen-set with the anchor cursor. Any violation → whole window unavailable. Do not salvage a same-boot subset.
5. **Capture failures**: empty stdout, malformed JSON, any stderr byte, nonzero rc, timeout, or overflow → rc2 unavailable with no numeric positive totals. Discard partial output.
6. **Positives**: exact scalar r15 predicates only. `MESSAGE_ID` array/null/number/unknown/case variant is not a positive; `UNIT_RESULT` exact `oom-kill`/`signal`; `EXIT_CODE` exact `killed`; `EXIT_STATUS` pin the accepted encoding (string `"9"` is the documented journalctl form) and reject bool/float/array/null. `positive_kernel_oom` means the `fe6faa94…` notice, not a kernel-transport record.
7. **Output**: one JSON object on stdout; `MORI_JOURNAL_WINDOW_OK` only with the window observed; `MORI_JOURNAL_WINDOW_UNAVAILABLE`/`SETUP` as specified; no raw cursor or raw record echoed; anchor/end cursor only as a SHA-256 digest with the digest input pinned (cursor string vs file bytes); no file writes; the anchor is never advanced automatically.
8. **Receipts**: record `journalctl --version`, scope, argv, rc, stdout byte count, stderr byte count, and whether the host is 261 versus the 262 docs. The harness manifest already owns the raw streams; the tool must not write them.
9. **Claim wording**: "exact-retained, anchor-boot, MESSAGE-free window"; not "anchor entry identity proven", not "authenticated emitter", not "unique victim", not "complete", not "no reboot detected means no reboot".

## Bottom line

The field documents support the contract's conservative shape, with three implementation traps that the sources make explicit:

1. **Do not add `-b` or a `_BOOT_ID=` match.** It would filter away the new-boot records that make a reboot unavailable, producing a false `records_after_anchor: 0` success.
2. **Do not parse the cursor.** It is opaque printable text, its format is private and may change, and the same entry can carry multiple strings. Exact string equality is a conservative acceptance gate; mismatch means `anchor-not-first-record`, not vacuum.
3. **Do not require an exact JSON key set.** Real records always carry `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `__SEQNUM` and `__SEQNUM_ID` in addition to the requested fields; unknown double-underscore fields must be skipped.

`MESSAGE_ID` is a client-set type label, not authentication, and the result fields are client-set too. Only `_BOOT_ID` of the requested fields is trusted and journal-added. The four positives are retained-record witnesses in the anchor boot, never an authenticated emitter, a unique victim, or a completeness claim.
