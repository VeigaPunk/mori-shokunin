# PackCursorShape — round-16 fixture pack report

## Files changed
- `.ufo/waves/round-16/fixtures/CursorShape.json` (new, 4431 bytes)

## Cases (4, shared schema `{"cases":[...]}`)
All four are refusal cases specific to the pack's topic (later-record `__CURSOR` shape/identity defects). Each stdout is a literal JSONL string: line 1 is the exact-anchor record (cursor + `_BOOT_ID` match `anchor`), line 2 is a clean valid later record (so the defect, not stream shape, is the isolated cause), line 3 is the defective record.

| id | scope | defect (record 3) | want_rc | want_id |
|---|---|---|---|---|
| `cursorshape-user-later-cursor-array` | user | `__CURSOR` is a JSON array of one string | 2 | `MORI_JOURNAL_WINDOW_UNAVAILABLE` |
| `cursorshape-user-later-cursor-null` | user | `__CURSOR` is `null` | 2 | `MORI_JOURNAL_WINDOW_UNAVAILABLE` |
| `cursorshape-system-later-cursor-missing` | system | `__CURSOR` key absent entirely | 2 | `MORI_JOURNAL_WINDOW_UNAVAILABLE` |
| `cursorshape-user-later-cursor-duplicate` | user | `__CURSOR` string identical to record 2's later cursor | 2 | `MORI_JOURNAL_WINDOW_UNAVAILABLE` |

- `want` is `{}` for all cases: no numeric totals may appear on an unavailable result per the contract, and no stable `reason` string is specified in the wave contract, so no reason is asserted.
- `stderr` empty, `returncode` 0 everywhere — the capture itself succeeds; the refusal must come from record validation, matching "malformed … missing/mismatched/duplicate cursor → rc2 unavailable".
- Duplicate-cursor case uses two *later* records sharing a cursor (distinct from the anchor cursor), the "duplicate later cursor" variant assigned to this lane; anchor-cursor-echo variants belong to PackExactAnchor territory and were left alone.
- No `MESSAGE` field appears in any record. No `timeout`/`overflow` flags — out of topic scope.

## Catalog ids used (verified bytes, `tools/mori-census.sh:1032-1036`)
- `fe6faa94e7774663a0da52717891d8ef` = `JOURNAL_ID_KERNEL_OOM`
- `d989611b15e44c9dbf31e3c81256e4ed` = `JOURNAL_ID_OOMD`
- `fc2e22bc6ee647b6b90729ab34a250b1` = `JOURNAL_ID_COREDUMP`
- `98e322203f7a4ed290d09fe03c09fe15` = `JOURNAL_ID_UNIT_SIGKILL` (paired with `EXIT_CODE:"killed"`, `EXIT_STATUS:"9"`)
- `d9b373ed55a64feb8242e02dbe79a49c` = `JOURNAL_ID_UNIT_FAILURE` (paired with `UNIT_RESULT:"oom-kill"`)

Catalog ids are decoration on otherwise-invalid records; refusal depends only on cursor validation.

## Verification exercised
- `python3 -c json.load` on the written file: parses, 4 cases, first record cursor/boot matches its anchor exactly, later cursors as designed. No tool/harness runs (per lane rules: never execute).

## Open schema notes for WindowHarness (advisory, non-blocking)
- `want: {}` on rc2 cases relies on `want` being a subset-assert map; if the harness requires `want` absent on unavailable cases, all four cases degrade identically — trivial mechanical fix.
- Reason strings for unavailable are unasserted; if the harness wants a `want_reason` pin, contract needs a stable vocabulary.

## Risks / blockers
- None blocking. Sibling pack schema convergence is unverifiable from this lane (no peer fixtures existed on disk at write time); the shape follows the dispatch contract verbatim.
- No tools installed; no pacman transactions (host-wide pause respected).
