# Registry — round 16 (MoriR16.Registry)

- **Owned file:** `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` only
- **Report path:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-16/build/Registry.md`
- **Scope:** cursor-continuity sources for the round-16 C1 journal-window tool (no census cutover, no cursor state, no authenticated-emitter or unique-victim claim)
- **Runs:** no build, test, lint, format, smoke, selftest or harness execution. No subagent, commit, or write outside the owned file and this report.
- **Tools installed or updated:** none.

## 1. Axes named

- **Coverage:** the registry carries primary, located sources for the cursor seek and identity semantics the window gate relies on.
- **No harm:** no immutable cell of an existing row changed; the two new rows are additive; `used-by` appends point only to a note that exists.

## 2. Sources opened (2026-10-20, systemd 262 `latest` pages)

| Row | URL | Use |
|---|---|---|
| S014 | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | Re-opened. `--cursor=`, `--after-cursor=`, `--boot`, `--output-fields=` headings confirmed. |
| S015 | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | Re-opened. `MESSAGE=`, `MESSAGE_ID=`, trusted fields and `_BOOT_ID=` confirmed. |
| S039 (new) | https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html | Opened. Seek and next-closest fallback. |
| S040 (new) | https://www.freedesktop.org/software/systemd/man/latest/sd_journal_test_cursor.html (serves the `sd_journal_get_cursor` page) | Opened. Entry-identity test and cursor-string non-uniqueness. |

### Located quotes

- **S039**, sd_journal_seek_cursor, Description: "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead." Note: the full sentence is 23 words, not 18 as Knowledge's relay stated; the quote is exact.
- **S040**, sd_journal_test_cursor, Description: "the same entry might be referred to by multiple different cursor strings" (12 words).
- **S040**, sd_journal_get_cursor, Description: "The cursor string should be considered opaque and not be parsed by clients." (13 words).

## 3. Mutable transitions (exact old → new)

1. **S014 `used-by`:** old `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-positive-evidence-r15.md` → new same list plus `, corpus/knowledge/journal-cursor-window-r16.md`.
2. **S015 `used-by`:** old `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-alarm-routing-r14.md, corpus/knowledge/journal-positive-evidence-r15.md` → new same list plus `, corpus/knowledge/journal-cursor-window-r16.md`.
3. **S039 (my own row from earlier this round, not a prior immutable row):** replaced. Earlier combined row covering seek, get and test is removed. New S039 is seek-only: `status` `mined`, `opened` `2026-10-20`, `recheck` `on-release`, `used-by` `corpus/knowledge/journal-cursor-window-r16.md`.
4. **S040 added** (new row): `status` `mined`, `opened` `2026-10-20`, `recheck` `on-release`, `used-by` `corpus/knowledge/journal-cursor-window-r16.md`.
5. **S037, S038, and all other rows:** unchanged.
6. **Search log:** "Bounded search 7" and one append-only correction were appended earlier this round; this turn adds nothing to the log.

## 4. Existence check for `used-by`

`corpus/knowledge/journal-cursor-window-r16.md` existed (129 lines) before any `used-by` cell named it. Its header and body name S014, S015, S039 and S040.

## 5. Numeric anchor discrepancy (recorded, not edited)

S014/S015 numeric anchors (for example `--after-cursor:187-190`) did not reproduce from the rendered pages. Section headings were confirmed; anchor cells are unchanged. The discrepancy is logged in the search log.

## 6. Contract notes

- A byte-unequal first record is conservative only. It does not prove vacuum or deletion. Byte-equal strings do not establish general deduplication or completeness, per S040.
- S039 supports the next-closest seek fallback. It does not document the `journalctl --cursor` CLI's own matching behavior; no such claim is made.
- The libsystemd `sd_journal_test_cursor` call is not reachable from the CLI wrapper; that is recorded in the Knowledge note, not claimed here.

## 7. Risks and out-of-scope

- No claim about journal retention, vacuum timing, or cross-boot cursor behavior is made.
- Nothing was verified by execution; L1 owns post-integration checks.

## 8. Execution disclosure

- No live `journalctl` query, probe loop, measurement, test, gate, build, smoke run or formatter was executed by this seat. No `/tmp` output was written.
- One background job was started: `bg_2643`, a read-only `grep` over `corpus/knowledge` and `corpus/lessons` for S-ID and cursor citations. It only read repository files. Its result matched the foreground grep and is not verification evidence.
- No package was installed or updated.

## 9. Final transitions (supersede sections 3 and 4)

- S039 (`sd_journal_seek_cursor`): `mined`, opened 2026-10-20, used-by `corpus/knowledge/journal-cursor-window-r16.md`. KEPT.
- S040 (`sd_journal_test_cursor`): `mined`, opened 2026-10-20, used-by `corpus/knowledge/journal-cursor-window-r16.md`. KEPT; both rows are distinct valid sources and immutable rows are never deleted.
- S014 and S015: used-by each includes `corpus/knowledge/journal-cursor-window-r16.md` (applied earlier).
- S013, S035, S037: earlier appends of the note path were REVERTED to their pre-round used-by lists, because the note's citations of these IDs were incidental drafting mentions. Logged transition: each removed the trailing `, corpus/knowledge/journal-cursor-window-r16.md`. Restore only if the note later cites them genuinely.
- No immutable cell changed. Shared edits stop here.
