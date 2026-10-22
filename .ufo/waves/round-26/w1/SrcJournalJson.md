# SrcJournalJson — SOURCES row draft (systemd v262 journal JSON, `--output-fields=`, `-u UNIT`, monotonic clocks)

Scope: open the systemd v262 documentation named in the assignment and answer four questions that
the round-26 C2 tool interface depends on, then draft one `corpus/SOURCES.md` row plus its Gate
line. `corpus/SOURCES.md` was **not** edited (draft only). No lane commit, no jj, no product-code
edit, no host service touched.

Registry note: the assignment says "the last rows S098-S127". At the entering tip
`248408f5b6610a85bcbdebe7ac0b4fa7ed51422a` the committed registry has **113** rows and ends at
**S113** (`git show 248408f5:corpus/SOURCES.md | grep -c '^| S[0-9]*'` → `113`; last id `S113`).
Rows S114–S127 do not exist, so the row drafted below would land as **S114** if no other round-26
row is admitted first. The id is left as `S???` per the assignment.

## Verdict in one line

All four questions are answered by primary systemd v262 documentation, and **nothing found
contradicts the contract**; two real gaps are found (JSON `null` for oversized fields, JSON array
of strings for a repeated field — neither is in the contract's inputs shape) plus one undefined
case (`ActiveEnterTimestampMonotonic = 0`).

## Files fetched (all HTTP 200, access date 2026-10-22)

| # | URL | Bytes | Lines | sha256 of fetched bytes |
|---|---|---|---|---|
| 1 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | 61,619 | 1,205 | `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` |
| 2 | https://raw.githubusercontent.com/systemd/systemd/v262/docs/JOURNAL_EXPORT_FORMATS.md | 8,556 | 178 | `207a646c067be133ff711f039bb2997a706bc5c146b7db6aa0f0350997b25543` |
| 3 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml | 165,445 | 2,861 | `eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6` |
| 4 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml | 343,315 | 5,308 | `44b89bffce737aff803966c207329e9fe2d28ad07709a4bb8e0edf6a4ec0d844` |
| 5 | https://raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml | 603,472 | 13,332 | `59cfeea5144e169369ee81f2b797fe9eb63ec18cb6aa918c2e66a7d5218117ca` |
| 6 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.journal-fields.xml | 30,086 | 695 | `ff1c00abcc8b60f3bc8243edc241f8c72da2c9249ff0e69a0286d356aad93335` |
| 7 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c | 87,278 | 2,346 | `abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f` |
| 8 | https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/utf8.c | 18,186 | 648 | `7cbebe621330509d7ed4928ea0e8374cf7155e954fee2745ebf08b90cd030d27` |
| 9 | https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/utf8.h | 2,280 | 61 | `2adc446e1e5d13f497b59f6e2fe1c02752b022cc7eaec35393f87689c6ea297a` |

Files 3 and 4 were opened because the assignment named them for the `ActiveEnterTimestampMonotonic`
question; **neither contains the property** (0 hits for `ActiveEnterTimestamp` in `systemd.unit.xml`,
0 hits for `Timestamp` in either). The property is documented in the D-Bus API page (5), which is
where `systemctl show` gets it, so files 5 and 6 were opened for it. Files 7–9 are a code cross-check
that pins the exact byte-array trigger the prose leaves loose (see the optional second row below).

Tag provenance (checked independently of the sibling seat): `refs/tags/v262` → tag object
`1f7dffaf714cc4488159c498b7a17cf34c5a96d5` → commit
`8cc40e0c5e9234bf45084751ac53b1fbfe70b492` ("systemd v262").

Local copies (read-only scratch for this seat):
`/fast/scratch/hyaku/mori-r26/MoriR26.SrcJournalJson/`.

## Answers to the four questions

Quotes in this section are given without the surrounding XML markup of the man sources; the Gate
section gives the same sentences verbatim from the fetched bytes.

### Q1 — How does `-o json` encode a field that is not valid UTF-8 or holds control characters?

As a JSON **array of unsigned byte numbers**, one element per byte, value 0…255 — not as a string
with escapes and not as `null`.

- `man/journalctl.xml:599-600`: "Fields containing non-printable or non-UTF8 bytes are encoded as
  arrays containing the raw bytes individually formatted as unsigned numbers."
- `docs/JOURNAL_EXPORT_FORMATS.md:145-147`: "A field that contains non-printable or non-UTF8 is
  serialized as a number array instead." and "Each byte of the binary field will be mapped to its
  numeric value in the range 0…255."
- `man/journalctl.xml:587-590` names three exceptions to "field values are generally encoded as JSON
  strings": (a) `:591-593` fields larger than 4096 bytes are encoded as `null`; (b) `:595-597` a
  non-unique field becomes a JSON array of its values; (c) `:599-600` non-printable/non-UTF-8 bytes
  become a byte array. `:603`: "Note that this encoding is reversible (with the exception of the size
  limit)."
- Code (exact trigger, `src/shared/logs-show.c:1124-1131`): if `strlen(name) + 1 + size >= 4096`
  (`JSON_THRESHOLD`, `logs-show.c:43`) the value is `null`; else if `utf8_is_printable(value, size)`
  it is a string; else it is `sd_json_variant_new_array_bytes`. `src/basic/utf8.h:23-24` defines
  `utf8_is_printable` as `utf8_is_printable_newline(str, length, true)`, and
  `src/basic/utf8.c:30-40,105-127` reject any C0 control except tab and newline, plus DEL and the
  C1 range, plus invalid UTF-8. **Consequence:** a `MESSAGE` containing `\n` or `\t` stays a JSON
  string; a `MESSAGE` containing `\r`, another C0 control, DEL/C1 bytes or invalid UTF-8 becomes a
  byte array. A repeated field becomes a JSON **array of strings**, not a byte array.

### Q2 — What does `--output-fields=` keep? Are `__MONOTONIC_TIMESTAMP` and `__REALTIME_TIMESTAMP` always present?

Yes — with the output modes that show all fields, the addressing fields are printed **in addition**
to the requested list, so both timestamps are always there.

- `man/journalctl.xml:667-675`: "A comma separated list of the fields which should be included in the
  output. This has an effect only for the output modes which would normally show all fields
  (`verbose`, `export`, `json`, `json-pretty`, `json-sse` and `json-seq`), as well as on `cat`. For
  the former, the `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, and `_BOOT_ID` fields
  are always printed."
- The serializer-level wording is weaker: `docs/JOURNAL_EXPORT_FORMATS.md:153-156`: "If the JSON data
  originates from a journal file it may include the special addressing fields `__CURSOR`,
  `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `__SEQNUM`, `__SEQNUM_ID`" and the timestamps are
  "formatted numeric string of usec since the respective epoch". So a **consumer of arbitrary JSON
  journal data** cannot assume the fields exist, while a **consumer of `journalctl -o json`** can.
  The round-26 tool reads through `journalctl`, so the stronger guarantee applies to it.
- `docs/JOURNAL_EXPORT_FORMATS.md:31-32` (export format, different format) says the meta-fields "are
  only generated when actual journal files are serialized. They are omitted for entries that do not
  originate from a journal file" — the same origin caveat, for the export format.

### Q3 — What does `-u UNIT` match?

`-u UNIT` is a **compound filter**, wider than `_SYSTEMD_UNIT` alone.

- `man/journalctl.xml:1164-1171`: "To show all fields emitted *by* a unit and *about* the unit,
  option `-u`/`--unit=` should be used. `journalctl -u name` expands to a complex filter similar to"
  ```
  _SYSTEMD_UNIT=name.service
    + UNIT=name.service _PID=1
    + OBJECT_SYSTEMD_UNIT=name.service _UID=0
    + COREDUMP_UNIT=name.service _UID=0 MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1
  ```
- `man/journalctl.xml:321-324`: "For each unit name, a match is added for messages from the unit
  (`_SYSTEMD_UNIT=UNIT`), along with additional matches for messages from systemd and messages about
  coredumps for the specified unit. A match is also added for `_SYSTEMD_SLICE=UNIT`".
- So for `earlyoom.service` the selection is: (1) the unit's own messages (`_SYSTEMD_UNIT=`), which
  is where earlyoom's own log lines are; (2) the **manager's** messages *about* the unit
  (`UNIT=` **and** `_PID=1`); (3) `OBJECT_SYSTEMD_UNIT=` messages; (4) that unit's coredumps.
  Note the `UNIT=` arm requires `_PID=1`, so a `UNIT=` line emitted by a non-manager process does
  **not** match `-u`.

### Q4 — `ActiveEnterTimestampMonotonic` vs the journal's monotonic clock: same boot, same clock?

**Yes — same clock, comparable within one boot; but the journal value is the *reception* time.**

- `man/org.freedesktop.systemd1.xml:2244`: `readonly t ActiveEnterTimestampMonotonic = ...;` (the
  `org.freedesktop.systemd1.Unit` property that `systemctl show` prints).
- `man/org.freedesktop.systemd1.xml:2780, :2783-2790`: `ActiveEnterTimestampMonotonic` and its siblings
  "contain `CLOCK_REALTIME` and `CLOCK_MONOTONIC` 64-bit microsecond timestamps of the last time a
  unit left the inactive state, entered the active state, exited the active state, or entered an
  inactive state. … The fields are 0 in case such a transition has not yet been recorded on this boot."
- `man/systemd.journal-fields.xml:656-665`: "`__MONOTONIC_TIMESTAMP=` … The monotonic time
  (`CLOCK_MONOTONIC`) at the point in time the entry was received by the journal in microseconds,
  formatted as a decimal. To be useful as an address for the entry, this should be combined with the
  boot ID in `_BOOT_ID=`."
- Therefore: both are `CLOCK_MONOTONIC` microseconds of the current boot, so the contract's scope
  comparison (`__MONOTONIC_TIMESTAMP ≥ ActiveEnterTimestampMonotonic`, current boot only) is
  clock-consistent. Two caveats: the journal stamp is when the entry was **received**, not when it
  was written, so a line written before the unit became active but received after it falls inside
  the scope (over-inclusion is possible, under-inclusion is not); and `ActiveEnterTimestampMonotonic
  = 0` means "no active-enter transition recorded on this boot", which is not a usable scope bound.

## Facts the round can rest on (each with its line number)

| # | Fact | Source and line |
|---|---|---|
| 1 | `-o json` encodes a non-printable / non-UTF-8 field as an array of byte values | `man/journalctl.xml:599-600`; `docs/JOURNAL_EXPORT_FORMATS.md:145-147` |
| 2 | Each byte maps to its numeric value 0…255 | `docs/JOURNAL_EXPORT_FORMATS.md:147` |
| 3 | A field larger than 4096 bytes is encoded as `null` (not a byte array) | `man/journalctl.xml:591-593` |
| 4 | A field repeated within one entry becomes a JSON array of its values | `man/journalctl.xml:595-597`; `docs/JOURNAL_EXPORT_FORMATS.md:150-152` |
| 5 | The byte encoding is reversible except for the size limit | `man/journalctl.xml:603` |
| 6 | `--output-fields=` keeps the requested fields **plus** `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `_BOOT_ID`, always | `man/journalctl.xml:667-675` |
| 7 | `--output-fields=` applies to `verbose`, `export`, `json`, `json-pretty`, `json-sse`, `json-seq` and `cat` | `man/journalctl.xml:670-672` |
| 8 | At the JSON-serializer level the addressing fields are only present when the data came from a journal file | `docs/JOURNAL_EXPORT_FORMATS.md:153-156`; `:31-32` |
| 9 | `-u UNIT` selects the unit's own messages (`_SYSTEMD_UNIT=`), the manager's messages about it (`UNIT=` + `_PID=1`), `OBJECT_SYSTEMD_UNIT=` and that unit's coredumps | `man/journalctl.xml:1164-1171`; `:321-324` |
| 10 | `ActiveEnterTimestampMonotonic` is a `CLOCK_MONOTONIC` 64-bit microsecond timestamp of the last active-enter transition, and is 0 if no such transition was recorded on this boot | `man/org.freedesktop.systemd1.xml:2780, :2783-2790`; property declaration `:2244` |
| 11 | `__MONOTONIC_TIMESTAMP` is `CLOCK_MONOTONIC` microseconds at the moment the entry was received by the journal, and should be combined with `_BOOT_ID` | `man/systemd.journal-fields.xml:656-665` |
| 12 | `-o json` prints one JSON object per entry, separated by newline characters | `man/journalctl.xml:587-588` |

Fact 12 is what makes the contract's `oomd_notices` line count sound: JSON string values escape
control characters, so one entry occupies exactly one output line.

## Contract flags

Nothing found contradicts the contract. The following are gaps or scope notes for the L1 and the
tool seat.

| Id | Kind | Finding (with line cite) | Suggested handling |
|---|---|---|---|
| F1 | gap, medium | The contract names only one non-string `MESSAGE` form ("a byte array … decoded as UTF-8 with replacement"). The docs add two more: JSON `null` for an oversized field (`man/journalctl.xml:591-593`) and a JSON **array of strings** for a field that occurs twice in one entry (`man/journalctl.xml:595-597`; `docs/JOURNAL_EXPORT_FORMATS.md:150-152`) | Do not read "array" as "bytes": a number array is bytes, a string array is multiple values, `null` is "too large / suppressed". A `null` `MESSAGE` = no readable text (not a zero count, not an error); a string array is joined before the prefix-anchored grammar match |
| F2 | gap, medium | `ActiveEnterTimestampMonotonic` is 0 when no active-enter transition was recorded on this boot (`man/org.freedesktop.systemd1.xml:2789-2790`). The contract's scope rule ("≥ `ActiveEnterTimestampMonotonic`") would then admit every earlyoom line of the boot | Treat 0 as "scope not establishable" and land in `KILLERS_UNKNOWN` (verdict rule 2's `scope_complete` false pathway), never in `KILLERS_QUIET` |
| F3 | scope note, low | The scope test is reception-time based: `__MONOTONIC_TIMESTAMP` is the time the journal *received* the entry (`man/systemd.journal-fields.xml:657-660`), so a line emitted before the unit became active but received afterwards is in scope. Over-inclusion possible, under-inclusion not [INFERENCE from the two definitions] | Keep the rule; state the over-inclusion bound in the entry |
| F4 | scope note, low | `-u earlyoom.service` also returns the manager's messages *about* the unit (`UNIT=` + `_PID=1`, `man/journalctl.xml:1169`) | Skip unmatched lines; the contract's prefix-anchored grammar already excludes manager lines, but they are not malformed input |
| F5 | supported | The live command `journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE` keeps `MESSAGE` and always also prints `__MONOTONIC_TIMESTAMP` (`man/journalctl.xml:673-675`) | No change; the contract's `__MONOTONIC_TIMESTAMP` dependency holds |
| F6 | supported | `-o json` emits one object per entry, newline-separated (`man/journalctl.xml:587-588`), and JSON strings escape control characters | No change; the `oomd_notices` line count equals the entry count |
| F7 | wording | The assignment's file choice for Q4 was wrong, not the contract: neither `man/systemd.unit.xml` nor `man/systemd.exec.xml` mentions `ActiveEnterTimestampMonotonic` (0 hits for `Timestamp` in both) | Cite `man/org.freedesktop.systemd1.xml`, the page that documents the `systemctl show` property the contract reads |

## Draft row (exact column order of `corpus/SOURCES.md`)

```markdown
| S??? | systemd v262 journal JSON encoding, `--output-fields=` retention, `-u UNIT` match set and unit monotonic timestamps — https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml ; https://raw.githubusercontent.com/systemd/systemd/v262/docs/JOURNAL_EXPORT_FORMATS.md ; https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.journal-fields.xml ; https://raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml | docs | A | systemd 262 release documentation for the journal read path only: how `-o json` encodes a field that is not printable UTF-8, what `--output-fields=` always keeps, which entries `-u UNIT` selects, and what `ActiveEnterTimestampMonotonic` and the journal's `__MONOTONIC_TIMESTAMP` measure; documentation at one released tag, not this host's journal content, not the earlyoom message grammar, not an entry-completeness guarantee | man/journalctl.xml:586-603 (json field encoding), :667-675 (`--output-fields=`), :315-328 and :1164-1171 (`-u UNIT` match set); docs/JOURNAL_EXPORT_FORMATS.md:143-156 (Journal JSON Format); man/systemd.journal-fields.xml:656-665 (`__MONOTONIC_TIMESTAMP`); man/org.freedesktop.systemd1.xml:2244 and :2780, :2783-2790 (`ActiveEnterTimestampMonotonic`); tag v262 = commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492; sha256 journalctl.xml d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd, JOURNAL_EXPORT_FORMATS.md 207a646c067be133ff711f039bb2997a706bc5c146b7db6aa0f0350997b25543, systemd.journal-fields.xml ff1c00abcc8b60f3bc8243edc241f8c72da2c9249ff0e69a0286d356aad93335, org.freedesktop.systemd1.xml 59cfeea5144e169369ee81f2b797fe9eb63ec18cb6aa918c2e66a7d5218117ca; HTTP 200 on 2026-10-22 | A field that is not printable UTF-8 arrives as an array of byte values, so the reader must decode bytes rather than read a string, and an oversized field arrives as null; `--output-fields=` still always prints `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP` and `_BOOT_ID`; `-u UNIT` selects the unit's own messages plus the manager's messages about it, so the scope is wider than `_SYSTEMD_UNIT` alone; the unit property and the journal stamp are both CLOCK_MONOTONIC microseconds of the same boot and therefore comparable, but the journal stamp is the reception time and the unit property is 0 when no active-enter transition was recorded this boot. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |
```

Tier **A** — reason: these are the upstream release documents of the exact systemd version in use on
this host (systemd 262, per the round-26 contract), pinned to the released tag `v262` (commit
`8cc40e0c…`). They are the normative description of the JSON output format, of the `--output-fields=`
retention rule, of the `-u UNIT` filter and of the unit timestamp properties — not a blog, a
rendered man page of an unspecified version, or a secondary summary. Scope is deliberately limited to
the journal read path: the row says nothing about this host's journal content, about earlyoom's
message grammar, or about entry completeness.

Status **mined** — the row is opened and quotable now; the facts above were read in the fetched
bytes, not inferred.

Recheck **on-release** — the facts are pinned to tag `v262`; re-open when systemd moves to a new
release tag.

## Optional second row (L1's choice; code cross-check)

The prose leaves the exact byte-array trigger loose, so the trigger was pinned in upstream code at
the same tag. Admitting this as a second, code-kind row keeps the docs row clean; it is offered
here because the L1 asked for one row, not two.

```markdown
| S??? | systemd v262 journal JSON field encoder and printable-UTF-8 rule — https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/utf8.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/utf8.h | code | A | the encoder that produces `journalctl -o json` field values at the v262 release tag: the 4096-byte null threshold, the printable check that decides string versus byte array, and the definition of "printable"; the file that builds the JSON object only, not the journal's own storage or matching code | src/shared/logs-show.c:43 (`JSON_THRESHOLD 4096U`), :1124-1131 (null / string / `sd_json_variant_new_array_bytes` decision); src/basic/utf8.h:23-24 (`utf8_is_printable` macro); src/basic/utf8.c:30-40 (`unichar_is_control`), :105-127 (`utf8_is_printable_newline`); tag v262 = commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492; sha256 logs-show.c abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f, utf8.c 7cbebe621330509d7ed4928ea0e8374cf7155e954fee2745ebf08b90cd030d27, utf8.h 2adc446e1e5d13f497b59f6e2fe1c02752b022cc7eaec35393f87689c6ea297a; HTTP 200 on 2026-10-22 | A field is a JSON string only when it is valid UTF-8 and carries no control character other than tab or newline; other C0 controls, DEL, the C1 range and invalid UTF-8 yield a byte array, and a field whose name plus value reaches 4096 bytes yields null instead. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |
```

## Gate

Source 1 — `man/journalctl.xml`

- URL: https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml
- Access date: 2026-10-22 (HTTP 200); 61,619 B, 1,205 lines; sha256
  `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd`
- Quote, `man/journalctl.xml:599-600` (verbatim, 19 words):
  > `Fields containing non-printable or non-UTF8 bytes are encoded as arrays containing the raw bytes individually formatted as unsigned numbers.`
- Quote, `man/journalctl.xml:673-675` (verbatim, 13 words; XML markup kept as fetched):
  > `For the former, the <literal>__CURSOR</literal>, <literal>__REALTIME_TIMESTAMP</literal>, <literal>__MONOTONIC_TIMESTAMP</literal>, and <literal>_BOOT_ID</literal> fields are always printed.`
- Quote, `man/journalctl.xml:1168-1171` (verbatim, 4 lines of filter; XML markup kept as fetched):
  > `_SYSTEMD_UNIT=<replaceable>name</replaceable>.service`
  > `  + UNIT=<replaceable>name</replaceable>.service _PID=1`
  > `  + OBJECT_SYSTEMD_UNIT=<replaceable>name</replaceable>.service _UID=0`
  > `  + COREDUMP_UNIT=<replaceable>name</replaceable>.service _UID=0 MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1`

Source 2 — `docs/JOURNAL_EXPORT_FORMATS.md`

- URL: https://raw.githubusercontent.com/systemd/systemd/v262/docs/JOURNAL_EXPORT_FORMATS.md
- Access date: 2026-10-22 (HTTP 200); 8,556 B, 178 lines; sha256
  `207a646c067be133ff711f039bb2997a706bc5c146b7db6aa0f0350997b25543`
- Quote, `docs/JOURNAL_EXPORT_FORMATS.md:145` (verbatim, 14 words):
  > `A field that contains non-printable or non-UTF8 is serialized as a number array instead.`
- Quote, `docs/JOURNAL_EXPORT_FORMATS.md:147` (verbatim, 17 words):
  > `Each byte of the binary field will be mapped to its numeric value in the range 0…255.`
- Quote, `docs/JOURNAL_EXPORT_FORMATS.md:153-154` (verbatim, 16 words):
  > `If the JSON data originates from a journal file it may include the special addressing fields`

Source 3 — `man/systemd.journal-fields.xml`

- URL: https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.journal-fields.xml
- Access date: 2026-10-22 (HTTP 200); 30,086 B, 695 lines; sha256
  `ff1c00abcc8b60f3bc8243edc241f8c72da2c9249ff0e69a0286d356aad93335`
- Quote, `man/systemd.journal-fields.xml:658-661` (verbatim, 22 words; XML markup kept as fetched):
  > `The monotonic time (<constant>CLOCK_MONOTONIC</constant>) at the point in time the entry was received by the journal in microseconds, formatted as a decimal.`

Source 4 — `man/org.freedesktop.systemd1.xml`

- URL: https://raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml
- Access date: 2026-10-22 (HTTP 200); 603,472 B, 13,332 lines; sha256
  `59cfeea5144e169369ee81f2b797fe9eb63ec18cb6aa918c2e66a7d5218117ca`
- Quote, `man/org.freedesktop.systemd1.xml:2783-2784` (verbatim, 21 words; XML markup kept as fetched):
  > `contain <constant>CLOCK_REALTIME</constant> and <constant>CLOCK_MONOTONIC</constant> 64-bit microsecond timestamps of the last time a unit left the inactive state, entered the active state`
- Quote, `man/org.freedesktop.systemd1.xml:2789-2790` (verbatim, 17 words):
  > `The fields are 0 in case such a transition has not yet been recorded on this boot.`

Source 5 — `src/shared/logs-show.c` (code cross-check)

- URL: https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c
- Access date: 2026-10-22 (HTTP 200); sha256
  `abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f`
- Quote, `src/shared/logs-show.c:1124` (verbatim, 12 words):
  > `if (!(flags & OUTPUT_SHOW_ALL) && strlen(name) + 1 + size >= JSON_THRESHOLD)`
- Quote, `src/shared/logs-show.c:1126-1127` (verbatim, 9 words):
  > `else if (utf8_is_printable(value, size)) r = sd_json_variant_new_stringn(&v, value, size);`

Source 6 — `src/basic/utf8.c` (code cross-check)

- URL: https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/utf8.c
- Access date: 2026-10-22 (HTTP 200); sha256
  `7cbebe621330509d7ed4928ea0e8374cf7155e954fee2745ebf08b90cd030d27`
- Quote, `src/basic/utf8.c:38-39` (verbatim, 17 words):
  > `return (ch < ' ' && !IN_SET(ch, '\t', '\n')) || (0x7F <= ch && ch <= 0x9F);`

## Out of scope (not done by this seat)

- `corpus/SOURCES.md` was not edited; the rows above are drafts for the L1 to paste.
- No lane commit, no `jj` invocation, no `git` write in the lane; only read-only `git log`/`show`/
  `git cat-file` style reads were used on committed bytes.
- No host unit was started, stopped, enabled or restarted; no journal was modified; no `systemd`
  setting was edited; no `omp` run was started.
- No earlyoom source, no earlyoom message-grammar claim and no host kill history is asserted here;
  those are other seats' scope.
- No private or host data was copied: no journal `MESSAGE` text, no process names, no command lines,
  no uids, no `--avoid`/`--prefer` expressions and no `/etc/default/earlyoom` value appears in this
  report; the only `_UID=0` strings are upstream man-page filter patterns quoted from
  `man/journalctl.xml:1169-1171`.

## Tooling

No tool was installed or upgraded for this seat: the work needed only `curl` (already present),
`sha256sum`, `grep` and the read tool. No pacman transaction was run, so the host-wide pacman pause
was untouched.
