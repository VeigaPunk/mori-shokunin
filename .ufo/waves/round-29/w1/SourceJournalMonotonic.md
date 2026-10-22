# SourceJournalMonotonic — frontier source row for C2 (journal monotonic timestamp and boot ID)

Seat: MoriR29.SourceJournalMonotonic. Lane tip at start of work: `8a45cefe84af0557b457308e4e0f679ca490f9e9`
(`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD`, read-only). Contract read:
`.ufo/waves/round-29/contract.md` (Sourced claim paragraph: "C2. The case writers and the fix rest on SOURCES rows
opened this round (S153 onward) for the earlyoom dry-run/version log lines and the journal monotonic-timestamp
field"). The oom-killers tool was not opened, grepped or run; no round-26/27/28 w1 or w2 report was opened.

## Behavior — what was done

1. Grepped the registry for the candidate URL before opening anything:
   `grep -c 'sd_journal_get_realtime_usec\|sd_journal_get_monotonic_usec' corpus/SOURCES.md` → `0`.
   The candidate URL is not a row; also `grep -n 'realtime_usec\|monotonic_usec' corpus/SOURCES.md` prints nothing.
2. Fetched the candidate at the v262 tag by curl; recorded URL, access time, sha256 and line-located quotes.
3. Checked the neighbour fact in the registry: row S122 already covers `__MONOTONIC_TIMESTAMP` and the
   `--output-fields=` always-kept set (`corpus/SOURCES.md:128`), so the new row is scoped to the API statement only.
4. Tested the item's alternate (a separately named monotonic page) — it 404s; recorded as a Gate reject.
5. Verified the tag revision independently: `refs/tags/v262` → annotated tag
   `1f7dffaf714cc4488159c498b7a17cf34c5a96d5` → commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`, matching the
   mapping S122 records.

## Gates — opened sources

| id | source | access time | sha256 | located quote | decision |
|---|---|---|---|---|---|
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/man/sd_journal_get_realtime_usec.xml | 2026-10-22T19:55:54Z | `dd224fc99710940d4e5d362aaa54768afc05dc1778c5cffa22595dbc1556d334` | `:61-63` (22 words): "the monotonic clock begins new with every reboot, it only defines a well-defined point in time when used together with an identifier"; `:82-85` (24 words): "If the boot ID parameter was passed NULL and the monotonic timestamp of the current journal entry is not of the current system boot" | admit, A, mined |
| — | https://raw.githubusercontent.com/systemd/systemd/v262/man/sd_journal_get_monotonic_usec.xml | 2026-10-22T19:56:12Z | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` | body line 1 (3 words): "404: Not Found" | reject, 404: the v262 manual source carries both functions on the sd_journal_get_realtime_usec page, so no separately named monotonic page exists to open |

Fetch receipts (no file content reproduced): HTTP 200, 5,372 bytes, 119 lines for the admitted page; HTTP 404,
14 bytes for the reject; tag ref HTTP 200, 364 bytes, sha256 `437155b1e35e586f314227751a1ce7e5e06ac7e5e0b1ea446dcc928f1344ad75`;
tag object HTTP 200, 2,699 bytes, sha256 `d21f2d84ed0cd088b6d31f7a237788a953c6dddaacef120bc8a3030e0c27dcfc`.

## Ready to paste — SOURCES.md registry row

Exact 11-column shape of `corpus/SOURCES.md:8`. Id is the item's placeholder `S15x`; highest existing id is S152
(`grep -nE '^\| *S1(4[5-9]|5[0-9]) ' corpus/SOURCES.md`), so the L1 assigns S153. The literal `S15x` does not match
the census row regex `S[0-9]{3,}` and must not be committed as-is.

```
| S15x | systemd v262 `sd_journal_get_realtime_usec(3)` and `sd_journal_get_monotonic_usec(3)` manual page source — https://raw.githubusercontent.com/systemd/systemd/v262/man/sd_journal_get_realtime_usec.xml | docs | A | systemd 262 release documentation of the journal entry monotonic timestamp only: CLOCK_MONOTONIC microseconds since boot-up of the specific boot, a point in time only together with the boot ID of that boot, the 128-bit third parameter receiving that boot ID, and a NULL boot ID making the call fail for an entry from another boot with -ESTALE; not the journalctl JSON field name, its encoding or the `--output-fields=` always-kept set (S122), not kernel CLOCK_MONOTONIC behavior across suspend, not this host's journal | man/sd_journal_get_realtime_usec.xml:36-39 (signature, `sd_id128_t *boot_id`), :55-69 (Description), :80-86 (Return Value), :100 (both calls added in version 187); tag v262 = commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492; HTTP 200 on 2026-10-22 | A journal entry's monotonic timestamp is measured from boot-up of one specific boot and begins new at every reboot, so it locates an entry in time only together with the boot ID of that boot; for an entry from another boot the call fails with -ESTALE instead of returning a usable stamp. | mined | 2026-10-22 | on-release | corpus/lessons/round-29.md, tools/fixtures/mori-oom-killers/cases-a2-r29.json |
```

## Ready to paste — lessons/round-29.md `## Gate` lines

Shape copied from `corpus/lessons/round-28.md:63-72`. Both lines above are the Gate lines; paste them under the
round-29 Gate heading, substituting the assigned id in the first line's id cell.

## Findings

- **Row is new, not a duplicate URL.** The candidate URL is absent from `corpus/SOURCES.md` (count `0`, command in
  Behavior 1). `grep -c` rather than `grep -l` because the page is not referenced anywhere in the file.
- **Boundary against S122 is explicit in the scope cell.** S122 already teaches that `--output-fields=` always prints
  `_BOOT_ID` and `__MONOTONIC_TIMESTAMP` and anchors `systemd.journal-fields.xml:656-665` (`corpus/SOURCES.md:128`).
  What S122 does not carry is this page's validity rule: the stamp is only a point in time with the boot ID, and a
  NULL boot ID makes the call fail for another boot's entry. The new row states only that, and names S122 as the
  excluded neighbour, so a later reader does not cite the wrong row for the JSON field.
- **`used-by` names two paths that do not exist at `8a45cefe`.** `ls -l corpus/lessons/round-29.md
  tools/fixtures/mori-oom-killers/cases-a2-r29.json` prints "No such file or directory" for both. This is the
  item's mandated `used-by`, and the row is `mined` as mandated, but the frozen census check "mined rows whose
  used-by paths do not exist — must print nothing" will print both until the round-29 lesson and the C2 case file
  land. The L1 should land them in the same round, or the census at the landed tip will flag this row.
- **Anchor revision verified independently, not inherited.** The tag ref and tag object were fetched and
  dereferenced (receipts above); the commit `8cc40e0c…` matches S122's mapping but was re-derived here.
- **Line numbers are from the fetched byte set**, 119 lines, sha256 `dd224fc9…`; a re-render or a different fetch
  could shift them. The quote lines chosen (`:61-63`, `:82-85`) are inside Description and Return Value, which the
  anchor cell names by heading as well as by line.
- **No candidate was opened and rejected for content**, only the 404 alternate; the Gate therefore carries exactly
  one reject line (routed defect 3 satisfied with the one reject met during this work).
- **Privacy.** Every quote is public upstream documentation text at a release tag. No host values, unit names, pids,
  session fields, `/etc/default/earlyoom` values or user-slice names were read into this report.
- **Tooling.** No tool installed, upgraded or restarted; no pacman transaction attempted. No git or jj write in the
  lane or fleet repo; no sandbox clone was needed (all git use was read-only `rev-parse`).

## Touched surfaces

- Written: this report, `.ufo/waves/round-29/w1/SourceJournalMonotonic.md`.
- Written outside the lane: `/fast/scratch/hyaku/mori-r29/SourceJournalMonotonic/jr.xml` (the admitted bytes),
  `monoalt.txt` (404 body), `tagref.json`, `tagobj.json` (revision receipts). Nothing else was created or modified.

## Out of scope

- No registry edit, no `SOURCES.md` append, no lesson edit: lane writes belong to L1 MoriR29.
- No case file, no counter, no tool run, no selftest; C2 assembly and the `sources` key of
  `cases-a2-r29.json` are the case seats' and L1's work.
- No earlyoom dry-run/version log-line row (the other half of the contract's S153-onward sentence); that fact is not
  this seat's ticket.

## Artifact paths

- Lane report: `.ufo/waves/round-29/w1/SourceJournalMonotonic.md`
- Fetched bytes: `/fast/scratch/hyaku/mori-r29/SourceJournalMonotonic/jr.xml`,
  `/fast/scratch/hyaku/mori-r29/SourceJournalMonotonic/monoalt.txt`,
  `/fast/scratch/hyaku/mori-r29/SourceJournalMonotonic/tagref.json`,
  `/fast/scratch/hyaku/mori-r29/SourceJournalMonotonic/tagobj.json`
