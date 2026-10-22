# Judge13 — non-author judge: r29-a2-10-not-found-earlier-stamped-positive

Seat: MoriR29.Judge13 (leaf, wave-2 falsify). Assignment: /skill:godspeed; non-author judge for frozen case `r29-a2-10-not-found-earlier-stamped-positive` (amendment A2 of round-28 contract carried into round-29 C2 "Mismatch judging").

Sources read (permitted set only):
- `.ufo/waves/round-27/contract.md:41-60` (C2 rule table; A2-03 at :51, A2-04 at :52, A2-09 at :57, A2-10 at :58)
- `.ufo/waves/round-26/contract.md` (whole spec incl. amendment A2 at :152-200; D1 supersede at :186-187)
- `tools/fixtures/mori-oom-killers/cases-a2-r29.json` — case object id `r29-a2-10-not-found-earlier-stamped-positive`
- `/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-10-not-found-earlier-stamped-positive.base.json` (tool at 7118f320)
- `/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-10-not-found-earlier-stamped-positive.fix.json` (L1 draft)

Not read: tool source, fix diff, other reports, lessons. Tools installed: none (no install/update performed this run).

## Case summary
Rule under test A2-10 (round-27:58): "a journal record without a numeric `__MONOTONIC_TIMESTAMP` is left uncounted and makes the scope incomplete; positive evidence elsewhere still stands".
Inputs: earlyoom_show `LoadState=not-found/ActiveState=inactive/UnitFileState=not-found/ActiveEnterTimestampMonotonic=6300000`; oomd_show inactive, `ActiveEnterTimestampMonotonic=0`; journal: SIGTERM send at 6299000 (before boundary), version line "earlyoom 1.9.0" at 6300000 (at boundary), SIGKILL send with timestamp `"unknown"`; `oomd_notices=0`.
Expect: `KILLER_ACTED` / exit 1; fields per table below.

## Field-by-field rulings (expect vs BASE)

| field | expected | base | fix | ruling | contract line |
|---|---|---|---|---|---|
| verdict | KILLER_ACTED | KILLER_ACTED | KILLER_ACTED | match | round-26:97-98,175-179,182-183 |
| exit | 1 | 1 | 1 | match | round-26:97-98 |
| earlyoom.state | absent | absent | absent | match | round-26:90; round-27:57 |
| earlyoom.version | 1.9.0 | null | null | tool error | round-26:82 (scope :78-79) |
| earlyoom.grammar | verified-1.9.0 | unverified | unverified | tool error | round-26:82,91 |
| earlyoom.scope_complete | false | false | false | match | round-27:58 |
| earlyoom.actions | null | null | null | match | round-26:102-104 |
| earlyoom.earlier_invocation_send_lines | 1 | 2 | 1 | tool error (base); fix matches | round-26:175-179,186-187; round-27:58 |
| earlyoom.dryrun_send_lines | 0 | null | null | tool error | round-27:52; round-26:166-167 |
| earlyoom.process_group_lines | 0 | null | null | tool error | round-27:51; round-26:164-165 |
| oomd.notices_this_boot | 0 | 0 | 0 | match | round-26:95,98 |

## Rationale
- verdict/exit: the SIGTERM send at 6299000 (< ActiveEnterTimestampMonotonic) is an earlier-invocation send of this boot; the unit is `not-found`/not active, so a non-zero earlier count is positive evidence (round-26:175-179) and send lines of a removed unit this boot are positive evidence (round-26:180-183; round-27:57) → `KILLER_ACTED`, exit 1 (round-26:97-98). The `"unknown"`-timestamp SIGKILL is left uncounted (round-27:58) and adds nothing. Base and fix agree.
- state: `LoadState=not-found` → `absent` (round-26:90 value list; round-27:57 "removed (not-found)").
- version: "earlyoom 1.9.0" at 6300000 = ActiveEnterTimestampMonotonic is in scope (round-26:78-79, ≥ boundary), so version = "1.9.0" per round-26:82. Base/fix null → tool error.
- grammar: version is pinned to 1.9.0 (above) and every parseable message matches the 1.9.0 patterns (round-26:83-89); the grammar field value is `verified-1.9.0` or `unverified` (round-26:91). The `unverified` output follows from the missed version line (same root defect) → tool error.
- scope_complete: false — required by round-27:58 (uncounted nonnumeric record makes the scope incomplete). Base and fix match.
- earlier_invocation_send_lines: counts send/escalation lines of this boot outside the current invocation (round-26:176-177). Only the SIGTERM at 6299000 qualifies; the `"unknown"`-timestamp SIGKILL is left uncounted (round-27:58). Expected 1. Base 2 counts the uncounted record → tool error. Fix 1 matches.
- dryrun_send_lines: no `dryrun mode enabled` message occurs, so no send lines are assigned to `dryrun_send_lines` (round-27:52; round-26:166-167) → 0. Base/fix null → tool error.
- process_group_lines: no `killing whole process group ` message occurs → 0 (round-27:51; round-26:164-165). Base/fix null → tool error.
- oomd.notices_this_boot: input `oomd_notices=0` → 0 (round-26:95). Match.

## FIX vs case; correctness of changed fields
Fix differs from case on exactly one field: `earlyoom.earlier_invocation_send_lines` (2 → 1). It matches the case and is correct under the rule text (the nonnumeric-timestamp record is no longer counted, round-27:58). No field the fix changed is now wrong under the rule text.
The fix leaves four tool-error mismatches open: version (null vs "1.9.0"), grammar (unverified vs verified-1.9.0), dryrun_send_lines (null vs 0), process_group_lines (null vs 0). All five mismatches are judged `tool error`, so under the L1 landing rule ("draft lands only for mismatches judged tool error") all five qualify; the draft currently fixes only one.

## Conclusion
All expect-vs-BASE differences are `tool error`; no case error, no unclear-text field. The fix resolves one of the five mismatches and introduces no wrong field.

case_ruling=tool error
