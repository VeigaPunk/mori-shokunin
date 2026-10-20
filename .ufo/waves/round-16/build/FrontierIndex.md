# FrontierIndex — round 16 (FR11 cursor window)

Seat: MoriR16.FrontierIndex (scribe, leaf). Owned file: `corpus/README.md`. Dated 2026-10-20.
Lane base: not re-read; no git subcommands run. No builds, tests, census, journal queries, or harness runs.

## Status

- `corpus/README.md`: **not edited this round.** The only indexable new knowledge would be a round-16 note under `corpus/knowledge/`. At check time that directory held no round-16 file (newest: `journal-positive-evidence-r15.md`). Rule: index only after the file exists. Held README edits are in §4.
- `tools/mori-journal-window.py`: absent at check time. Nothing to index.
- No source registry rows were written by this seat (`corpus/SOURCES.md` is not owned here).

## 1. Sources opened this round (access 2026-10-20)

| Source | URL | Used for |
|---|---|---|
| S014 journalctl(1), systemd 262 | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | `--cursor=`, `--after-cursor=`, `--boot`, `-o json`, `--output-fields=`, `--no-tail`, `-q`, Exit status |
| S015 systemd.journal-fields(7), systemd 262 | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | `__CURSOR=`, `MESSAGE_ID=`, trusted `_`-prefixed fields |
| sd_journal_seek_cursor(3), systemd 262 (page title reads sd_journal_seek_head) | https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html | seek-to-cursor semantics when the entry is absent |
| sd_journal_get_cursor(3) / sd_journal_test_cursor(3), systemd 262 | https://www.freedesktop.org/software/systemd/man/latest/sd_journal_get_cursor.html (sd_journal_test_cursor.html serves the same page) | cursor identity: string vs entry |

Short quotes (each ≤25 words) for the lesson `## Gate` row:

- S014 `--cursor=`: "Start showing entries from the location in the journal specified by the passed cursor."
- S014 `--after-cursor=`: "Start showing entries from the location in the journal *after* the location specified by the passed cursor."
- S014 `-q`: "any warning messages regarding inaccessible system journals when run as a normal user"
- S014 `--output-fields=`: "For the former, the "__CURSOR", "__REALTIME_TIMESTAMP", "__MONOTONIC_TIMESTAMP", and "_BOOT_ID" fields are always printed."
- S014 `--boot`: "This will add a match for "_BOOT_ID="."
- S015 `__CURSOR=`: "A cursor is an opaque text string that uniquely describes the position of an entry in the journal"
- sd_journal_seek_cursor: "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead."
- sd_journal_test_cursor: "cursor strings do not uniquely identify an entry: the same entry might be referred to by multiple different cursor strings"

## 2. Findings for FR11 (bounded to exact retained same-boot window)

1. **Anchor absence seeks forward, it does not fail.** Per sd_journal_seek_cursor, a missing cursor yields the next closest entry. A window query with `--cursor=<anchor>` whose anchor was rotated or vacuumed therefore starts at a different entry. The tool's exact first-record check must map that to `unavailable`. [INFERENCE that journalctl's `--cursor` uses seek semantics; L1 must confirm in its own selftest.]
2. **Byte mismatch is conservative only.** sd_journal_test_cursor says one entry may carry several different cursor strings. An exact-byte first-record mismatch can therefore be a *false unavailable* when the anchor is present under an alias. It does **not** prove vacuum, deletion, or a boot boundary.
3. **Byte uniqueness is not entry dedup.** The "unique valid scalar cursor" check removes repeated identical strings only. Two aliases of one entry in one window would both pass. No dedup, no completeness claim.
4. **Silent partial reads under `-q`.** S014 says `-q` suppresses warnings about inaccessible system journals for a normal user. The rc0 + empty-stderr path therefore does not prove full access. Anchor-first and non-empty checks cover an unreadable anchor, not later unreadable journal files. Positive counts are lower bounds over readable records, matching `evidence_basis=validated-record-subsets`.
5. **Boot boundary.** The spec does not add `-b`, so a window crossing a reboot returns foreign-boot records. Those map to unavailable, never to a zero count.
6. **JSON shape.** S014 encodes non-unique fields as arrays, fields over 4096 bytes as null, and non-UTF8 as numeric arrays. The scalar requirement on `_BOOT_ID`, `MESSAGE_ID`, `UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS` and `__CURSOR` is therefore structural: any non-scalar value must reject the record or the window.
7. **Trust.** S015: `MESSAGE_ID` and `UNIT_RESULT` are client-supplied user fields; only `_BOOT_ID` (and other `_`-prefixed fields) is trusted. Counts are record-type labels, not authenticated emitters or unique victims.

## 3. Frontier boundary (README unchanged until a knowledge file lands)

FR11 may advance only to: **exact-retained, same-boot, MESSAGE-free, new-since-anchor record counts; false-unavailable under aliases is accepted.** It stays open for: cursor rotation/vacuum recovery, cross-boot ordering, unreadable later journal files under `-q`, entry-level dedup, and completeness.

## 4. Held README edits (apply only after the round-16 knowledge file exists)

- Frontier row FR11, "first evidence": append the round-16 note path plus `S014`, `S015`, sd_journal_seek_cursor, sd_journal_get_cursor. Keep the existing `SOURCES.md:20-21` reference.
- Frontier row FR11, "boundary": keep the existing sentence and append: "Exact-byte anchor match is conservative: alias strings give false unavailable, never proof of loss. Rotation/vacuum, cross-boot, unreadable later files under `-q`, entry dedup, and completeness remain unavailable/[UNKNOWN]." Append-only; do not delete the old sentence.
- Coverage map: one new row for the round-16 note, only once its path exists.

## 5. Mutable-cell requests for the lesson/registry owners (not edited here)

- New source rows requested: sd_journal_seek_cursor and sd_journal_get_cursor/test_cursor (access 2026-10-20), quotes in §1. Registry: `MoriR16.Registry` (`corpus/SOURCES.md` rows and IDs).
- Lesson: `MoriR16.Lesson` (`## Gate` records URL, access date, quote; S014/S015 used-by cells updated once the round-16 note exists; existing rows immutable).

## 6. Residuals / not done

- No journal query, fixture run, selftest, or census. The alias, `-q` and seek behaviours are source-derived; L1's verification decides them.
- No README edit made, because no knowledge file exists yet. Re-check `corpus/knowledge/` before applying §4.
- Tooling: none installed or updated by this seat.

## 7. Routing and current state

- Ownership: `corpus/README.md` retained by MoriR16.FrontierIndex. Knowledge will notify this seat by exact id when the round-16 note exists.
- Routing ids: Lesson = `MoriR16.Lesson`; Registry = `MoriR16.Registry`.
- README state: unchanged. The round-16 note and `tools/mori-journal-window.py` are both absent at the last check, so the §4 edits are not applied.
- Pending on Knowledge notice: apply §4 (FR11 first evidence and boundary, plus the coverage-map row). Preserve historical entries; append only.
- Runs: none. No builds, tests, journal reads, census, or harness executions. No installs or updates.
- Process note: a `write` to an existing path replaces the whole file. This seat's earlier attempt to append §7 replaced the file with §7 alone; this revision restores §1–§6 and keeps §7.

## 8. Final state (after Knowledge notice)

- Knowledge note landed: `corpus/knowledge/journal-cursor-window-r16.md` (18228 bytes, per MoriR16.Knowledge). Indexed in `corpus/README.md` coverage map as the row after `journal-positive-evidence-r15.md`, sources S014/S015/S039/S040.
- FR11 row in `corpus/README.md` Frontier updated (existing text kept in substance; first evidence now adds the round-16 note). Boundary: exact-retained same-boot window; alias false-unavailable accepted; no dedup, no completeness; rotation/vacuum, cross-boot and unreadable-later-files under `-q` remain open.
- Lesson routing: `MoriR16.Lesson`. Registry routing: `MoriR16.Registry`. Neither edited here.
- Runs: none. No builds, tests, journal reads, census, harness runs, or installs.
