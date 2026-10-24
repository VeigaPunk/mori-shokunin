# Knowledge — round 16 journal cursor window (scoped findings)

Author lane: MoriR16.Knowledge. Writes: `corpus/knowledge/journal-cursor-window-r16.md` (new) and this report only. No live journal query, no probe loop, no test, gate, build, smoke run or formatter, no commit, no fleet file touched.

## Disclosure
- This seat's journalctl invocations were `journalctl --help`, `journalctl --version` and `man journalctl` only. None reads journal contents.
- A background job's result delivered output from `scripts/sources-census.sh validate` that this seat did not launch. It is read-only, and its output is not used as verification here.

## Behavior (as stated in the note)
- A window is available only when the first parsed record has the anchor's exact `__CURSOR` string and exact `_BOOT_ID`. The anchor is dropped; every later record must be a scalar-cursor object from the same boot.
- The `journalctl --cursor=` behaviour for an absent cursor is not documented in S014; the API fallback (S039) does not establish a CLI success case. The wrapper refuses any first record that is not the anchor, any nonzero exit and any empty capture. No reason enum is named here.
- Byte equality is a conservative acceptance test only. S040 says the same entry may have several strings; the cursor identifies an entry globally and stably. No claim is made that a string belongs to only one entry, and no collision claim is made either way. No dedup.
- Same-boot: no `-b` match is added. A captured foreign-boot record refuses the current window; no permanent-retention claim is made for that record.
- Subsets: `records_after_anchor` and the four `positive_*` tokens are subsets of the captured stream, not totals or victim counts. `MESSAGE` is not requested and not emitted; the note makes no claim about what `journalctl` reads internally.
- Access: `--user`/`--system` must be explicit. `-q` can hide inaccessible-system warnings, so the anchor and an accessible subset can come back quietly; anchor presence does not prove full scope access.

## Gate
- Static reads of the systemd 262 pages for S014, S015, S039 and S040 on 2026-10-20. No host version verified.
- Registry: the parent reports two distinct rows, S039 (seek) and S040 (test). This note cites both. Earlier single-S039 message is superseded.

## Touched surfaces
- `corpus/knowledge/journal-cursor-window-r16.md` (new).
- Registry: used-by appends requested for S014, S015, S039, S040 (not written by this seat).
- Lesson and Registry informed of final cited IDs and the disclosure above.

## Out of scope
- No edits to SOURCES.md, README, QUALITY, PROVINCE, SKILL.md, LOG.md, tools or the wrapper.
- No tool installs; no pacman transaction.

## Unknowns (not measured)
- CLI behaviour for an absent cursor, on any version.
- Frequency of alias strings in a live journal.
- Whether a foreign-boot record is still retained at a later query.
- journald retention and rate-limit behaviour (not opened).

## Verification for L1 (not run here)
- The recheck commands in the note header (static curl of the four pages).
- Registry validation of the four cited IDs and their used-by appends.
