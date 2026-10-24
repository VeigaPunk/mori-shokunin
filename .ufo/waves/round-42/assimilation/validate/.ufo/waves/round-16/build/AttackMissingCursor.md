# AttackMissingCursor — can a nearest-seek pass as the exact anchor?

Lane: critic (leaf). Read-only except this report. Nothing was executed against journald. No runtime changes, no installs.

## Read-time state (2026-10-20T05:52:17-03:00, HEAD `b83edc6ee3db6822382ab673d7e6e984e420f22f`)

- `tools/mori-journal-window.py`: **ABSENT**. `tools/mori-round16-regressions.py`: **ABSENT**. This review checks the contract and the landed fixtures. It is not a verdict on production code.
- Fixtures read, with sha256:
  - `MissingAnchor.json`: `fca571e2…a7646`
  - `ExactAnchor.json`: `193dc63c…cbd3`
  - `CursorShape.json`: `b29a4a1d…6c8436c6`
- Host: `systemd 261 (261.2-1-arch)`, from `journalctl --version` (a read-only version query).

## Primary sources opened this round

- P1 sd_journal_get_cursor(3), systemd 262 — https://www.freedesktop.org/software/systemd/man/latest/sd_journal_get_cursor.html: "Seeking to a cursor position without the specific entry being available locally will seek to the next closest (in terms of time) available entry." It also says: "the same entry might be referred to by multiple different cursor strings, and hence string comparing cursors is not possible. Use this call to verify after an invocation of sd_journal_seek_cursor(3), whether the entry being sought to was actually found."
- P2 sd_journal_seek_cursor(3), systemd 262 — https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_head.html: "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead."
- P3 journalctl source, tag v261 — `src/journal/journalctl-show.c` `seek_journal()`, lines 73–102 (https://raw.githubusercontent.com/systemd/systemd/v261/src/journal/journalctl-show.c):
  - Line 76: `--cursor` calls `sd_journal_seek_cursor`.
  - Line 80: `sd_journal_step_one(j, !arg_reverse)`.
  - Lines 84–97: only with `--after-cursor`/`--cursor-file` does it call `sd_journal_test_cursor`, and it skips the first entry only if that entry matches. Otherwise it prints the nearest entry with no message and no nonzero rc.
  - Lines 100–102: if no entry is found, it shows nothing.
  - Lines 605–619: `-- No entries --` is printed only without `--quiet`, and the rc is 0.
- P4 sd-journal.c, tag v261 (https://raw.githubusercontent.com/systemd/systemd/v261/src/libsystemd/sd-journal/sd-journal.c):
  - `sd_journal_seek_cursor` (lines 1263–1333) accepts a **partial** cursor. It needs only (`s`+`i`) or (`b`+`m`) or `t`.
  - `sd_journal_test_cursor` (lines 1366–1425) compares only the fields present in the cursor.
  - `s=` and `b=` are parsed with `sd_id128_from_string`, so each must be a 128-bit id.
- P5 `src/shared/journal-util.c` v261, lines 95–150 (https://raw.githubusercontent.com/systemd/systemd/v261/src/shared/journal-util.c): a per-file `EACCES` hits `continue`, so it is skipped silently once any file opens. The "Hint" notice is gated on `!quiet`, and it is also skipped for root and for members of `systemd-journal` (lines 27–37). Truncated or corrupted files log a warning on stderr whether or not `--quiet` is set.

Axes: **C1 coverage** (FR11 window), **claim soundness** (no false-exact or false-complete), **availability** (avoid false refusals), **preservation** (r15 predicates unchanged).

## Findings

### F1 — Mistaking a nearest-seek for the anchor is excluded only by byte-exact string equality, and that defense holds. Severity: guard; must stay strict
- **Counterexample:** the anchor entry has been vacuumed. `journalctl --cursor=A` prints the closest later entry N first, with rc 0, empty stderr, and a well-formed `__CURSOR` (P2, P3 line 80).
- **Defense:** the contract requires the first record's `__CURSOR` to be **byte-equal** to the anchor cursor and its `_BOOT_ID` to equal the anchor `boot_id`. Two different entries cannot produce identical full cursor strings, because the string is made of seqnum_id, seqnum, boot, monotonic, realtime and xor_hash. So equality cannot pass a nearest entry.
- **Tradeoff:** P1 says string comparison has false negatives (one entry, several strings). That makes the check **fail-closed**: an availability cost, not a soundness defect. The canonical judge should accept this tradeoff and reject any change that removes it.
- **Forbidden relaxations** (each one re-admits a nearest-seek or a wrong entry):
  - (a) prefix or `startswith` matching;
  - (b) parsing the cursor and comparing a subset of fields (P1 calls cursors opaque);
  - (c) emulating `sd_journal_test_cursor`, which matches any entry containing the anchor's *present* fields (P4). A partial anchor such as `t=…` or `b=…;m=…` would then "match" whatever entry happens to be nearest;
  - (d) whitespace or case normalisation;
  - (e) "skip records until the anchor appears";
  - (f) treating a matching `_BOOT_ID` as evidence of the anchor.
- **Smallest correction:** none needed in the contract. The WindowTool code must use plain `==` on the decoded JSON string, with no `.strip()`/`.lower()`, and compare exactly one record (the first).

### F2 — No fixture can catch the argv flags that make journalctl hide a nearest-seek or truncate the window. Severity: high for coverage honesty
- **Problem:** every pack feeds canned stdout through a wrapper that ignores its arguments. In real use, these argv drifts are all invisible (rc 0, empty stderr), yet every current fixture would still pass:

| argv drift | real effect (P3) | fixture result |
|---|---|---|
| `--after-cursor=A` or `--cursor-file` | If A was vacuumed, the nearest entry is printed **as if it followed A**. This is the exact mistake this lane attacks. If A exists, it is skipped, so the tool always refuses. | passes |
| `--reverse` | seeks to the closest *preceding* entry, then outputs older entries; these would be counted as "after anchor" | passes |
| `-n N` / `--lines=N`, `--until=` | the loop stops silently at N or at the time limit (P3 `show()` lines 172, 183–194): the window is truncated with rc 0 | passes |
| `-k`, `-u`, `-b`, `--grep`, `FIELD=` matches | the seek lands on the nearest *matching* entry, so the anchor is never first: permanent refusal, or with `--grep`, a MESSAGE read | passes |
| `--system` omitted for scope=system while running as root | user-journal entries get mixed into the system window | passes |
- **Smallest correction (harness/selftest owner):**
  - The per-case journalctl wrapper must write its own argv as JSON to a per-case file in the harness output dir.
  - The harness must assert that argv equals the canonical list exactly:
    - `--user` or `--system`, matching the scope;
    - `--cursor=<anchor>`, `--no-tail`, `--quiet`, `--output=json`;
    - `--output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS`.
  - Any extra or missing flag fails the case.
  - The `--selftest` must include one arm that asserts the argv.
  - Without this, "nearest-seek is refused" is shown only for the stdout-parsing half, not for the query half.

### F3 — Fixture blind spots for subset comparison. Severity: medium (cheap to fix)
- **Current coverage:**
  - `MissingAnchor.nearest_cursor_not_anchor` differs from the anchor only in `x=`, so it kills any comparison that ignores `x`.
  - `anchor_present_but_not_first` and `anchor_vacuumed_positive_trap` differ in `m`, `t` and `x` together.
- **Gaps:** no case pins:
  - (i) a **partial anchor**, e.g. `s=<32hex>;i=4d2`, whose first record is the full cursor that starts with it. Expected rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE`; this kills (a) and (c).
  - (ii) a first record whose `__CURSOR` equals the anchor but whose `_BOOT_ID` differs. Expected rc2; this kills a cursor-only check. It may already exist in `BootBoundary.json`, which was not audited here.
  - (iii) an anchor with trailing or leading whitespace (still printable) against an untrimmed first record. Expected rc2 (either setup or unavailable, but stable); this kills (d).
- **Smallest correction:** add (i)–(iii) to `MissingAnchor.json` (owner PackMissingAnchor / the CursorShape owner). Do not edit existing cases.

### F4 — Fixture "realistic" cursors could not be parsed by systemd. Severity: low; provenance accuracy
- In `MissingAnchor.json` (all four cases) and `CursorShape.json`, the `s=` value has 16 hex digits.
- P4 parses `s=` with `sd_id128_from_string`, which needs 32 hex digits. Real journalctl would fail with "Failed to seek to cursor" and rc 1. It would never return the modelled stdout.
- `ExactAnchor.anchor-realistic-cursor…` correctly uses 32 hex digits.
- This does not break the tests: the wrapper is fake, and the anchor schema treats the cursor as opaque.
- **Correction:** no fixture or report should call these cursors "realistic" or "real-format". If realism is claimed, use 32-hex `s=` values.

### F5 — An exact anchor proves the start point, not a gap-free window. Severity: high if claimed; this is a claim-rubric item, not a code defect
- **Counterexample:** the anchor sits in a readable journal file, and a later file in the same scope returns `EACCES`. sd-journal skips that file silently (P5 `case EACCES: continue;`). `--quiet` suppresses the only hint, and the hint is never printed for root or for `systemd-journal` members anyway. Result: rc 0, empty stderr, the first record equals the anchor, and the tool returns OK with records missing.
- Truncated or corrupted files *do* print a warning on stderr whatever `--quiet` says, so the stderr refusal catches them.
- **Contract assessment:** the contract already forbids a completeness claim. "Exact retained cursor continuity" must therefore mean *the anchor entry is still retained and is the first record*. It must not mean *every entry after the anchor was observed*.
- **Correction:** WindowTool output and FR11 wording must say that the counts are lower bounds over readable retained records after an exact anchor. The judge must reject wording such as "continuous", "complete", "no OOM since anchor", or "all entries since". Removing `--quiet` does **not** fix this (P5 lines 27–37).

### F6 — Empty stdout is the correct refusal for a vacuumed anchor with nothing newer. Severity: confirmed guard
- With `--cursor`, if the anchor is gone and no newer entry exists, P3 lines 100–102 and 605 give: no output, `-- No entries --` suppressed by `--quiet`, rc 0.
- `MissingAnchor.empty_stdout_anchor_unproven` (want rc2 UNAVAILABLE) models this exactly.
- **Note:** without `--quiet`, `-- No entries --` goes to **stdout** and would be refused as a malformed capture. That is also safe, but it needs a different stable reason; keep `--quiet` in argv.

## Out-of-axis note (for BootContinuity / AttackMixedBoot, not judged here)

The tool never compares the anchor's `boot_id` with the current boot. Take an anchor that is the last entry of a previous boot in a scope with no current-boot entries yet. The window returns OK with 0 records and labels it "same-boot", even though a boot boundary lies between the anchor and now. The literal counts are true, but the label is not.

## Verdict

- **Fixable defects:** F2 (argv pin in harness and selftest), F3 (three refusal cases), F4 (wording).
- **Tradeoff for the judge:** F1 fail-closed string equality. Accept it, and reject any relaxation.
- **Claim boundary:** F5. Reject any continuity or completeness wording.
- **Impacted axes:** C1 coverage (F2, F3), claim soundness (F1, F5), availability (F1 false refusals, accepted).
- **Preservation:** r15 predicates were not touched here.

## Tooling record

- No tools installed or updated.
- Read-only commands only: `curl` of official systemd sources and man pages, `journalctl --version`, `sha256sum`, `date`, `test -e`.

## Deviation disclosure (after L1 clarification)

- I ran `journalctl --version` once to record the host systemd version, `systemd 261 (261.2-1-arch)`.
  - This command reads no journal and queries no records, cursors or boots.
  - It still executed the journalctl binary, so this disclosure treats it as a deviation.
  - The version result is **inadmissible as verification**. No finding depends on it: every finding cites the upstream v261 source and the systemd 262 man pages.
- Also run, all static and read-only: `ls tools/`, `git rev-parse HEAD`, `sha256sum` of three fixtures, `date`, `test -e`.
- No queries against the live journal, no probe loops, no background jobs, no tests, no writes outside this report, no output to /tmp. Upstream sources were piped from `curl` to stdout only.
- This disclosure was also sent to MoriR16.Lesson.
