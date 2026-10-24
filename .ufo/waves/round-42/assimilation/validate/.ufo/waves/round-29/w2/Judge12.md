# Judge12 — Non-author judge findings: `r29-a2-10-failed-stamped-positive` (rule A2-10)

## Scope read (only)
- `.ufo/waves/round-26/contract.md` (whole spec, incl. Amendment A2 at :152-200 and output spec :90-108).
- `.ufo/waves/round-27/contract.md:40-80` (frozen rule list; A2-10 at :58).
- Case object `r29-a2-10-failed-stamped-positive` in `tools/fixtures/mori-oom-killers/cases-a2-r29.json`.
- Tool outputs: `r29-a2-10-failed-stamped-positive.base.json` (tool at 7118f320) and `.fix.json` (L1 draft).
- Not read (per assignment): tool source, fix diff, other reports, lessons. No tool installs performed.

## Case summary
- Inputs: `earlyoom_show` ActiveState=failed, ActiveEnterTimestampMonotonic=5200000; journal lines: version `earlyoom 1.9.0` @5200000, `sending SIGTERM to process …` @5200001 (stamped), `sending SIGKILL to process …` with `__MONOTONIC_TIMESTAMP: "not-a-number"` (nonnumeric); `oomd_notices`=0.
- Expect: verdict `KILLER_ACTED`, exit 1, 8 pinned `expect.fields` paths.

## Field-by-field rulings (expected vs base)

| field | expected | base | fix | ruling | contract line |
|---|---|---|---|---|---|
| earlyoom.state | unavailable | unavailable | unavailable | match | round-26:162-163 (A2b) |
| earlyoom.version | "1.9.0" | null | null | tool error | round-26:82 |
| earlyoom.grammar | verified-1.9.0 | unverified | unverified | tool error | round-26:91 |
| earlyoom.scope_complete | false | false | false | match | round-26:186-187 (A2-10) |
| earlyoom.earlier_invocation_send_lines | 0 | 2 | 1 | tool error | round-26:175-177 |
| earlyoom.dryrun_send_lines | 0 | null | null | tool error | round-27:52 (A2-04) |
| earlyoom.process_group_lines | 0 | null | null | tool error | round-27:51 (A2-03) |
| oomd.notices_this_boot | 0 | 0 | 0 | match | round-26:97-98 |
| verdict | KILLER_ACTED | KILLER_ACTED | KILLER_ACTED | match | round-26:97-100 |
| exit | 1 | 1 | 1 | match | round-26:97 |

## Rulings detail
1. **version** (expect "1.9.0", base null): version line `earlyoom 1.9.0` at T=5200000 is at `ActiveEnterTimestampMonotonic` and thus in scope (round-26:78-79; boundary line at `ActiveEnterTimestampMonotonic` included, round-26:115-117). Round-26:82: `earlyoom <version>` → version. Tool returns null → tool error.
2. **grammar** (expect verified-1.9.0, base unverified): with version determined as 1.9.0, grammar is `verified-1.9.0` (round-26:91). `unverified` → tool error.
3. **earlier_invocation_send_lines** (expect 0, base 2): the stamped SIGTERM @5200001 belongs to the current invocation (in scope); the nonnumeric SIGKILL is left uncounted (A2-10, round-26:186-187) and cannot be placed in an earlier invocation. No earlier-invocation sends → 0. Base 2 → tool error.
4. **dryrun_send_lines** (expect 0, base null): no `dryrun mode enabled` line occurs, so no send line goes to `dryrun_send_lines` (A2-04, round-27:52); count is 0. Base null → tool error. (Minor note: A2-04 only defines the field's content for the dryrun-enabled case; the pinned 0 follows from "every count is a count of log lines" semantics, and the case pins 0.)
5. **process_group_lines** (expect 0, base null): no `killing whole process group ` line occurs (A2-03, round-27:51); count is 0. Base null → tool error. (Same minor caveat as #4.)

## Fix vs case
- Fix matches case on: `earlyoom.state`, `earlyoom.scope_complete`, `oomd.notices_this_boot`, `verdict`, `exit`.
- Fix still mismatches case on: `version` (null ≠ "1.9.0"), `grammar` (unverified ≠ verified-1.9.0), `earlier_invocation_send_lines` (1 ≠ 0), `dryrun_send_lines` (null ≠ 0), `process_group_lines` (null ≠ 0).
- Only field the fix changed vs base: `earlier_invocation_send_lines` 2 → 1. It still does not match expect (0) and is still wrong under the rule text (round-26:175-177 + A2-10: the stamped SIGTERM is in the current invocation; the nonnumeric record is uncounted → 0). No field changed by the fix is now correct; the draft resolves none of the mismatches.

## Residual risk / verification gaps
- Root causes not attributed: tool source and fix diff unread per assignment.
- [INFERENCE] Base=2 likely counts both sends as earlier-invocation because no version/grammar is recognized (version null → no current invocation established); fix=1 likely leaves the nonnumeric record uncounted but still misplaces the stamped SIGTERM as earlier-invocation. Inferred from outputs only, not observed internally.

case_ruling=tool error
Report: .ufo/waves/round-29/w2/Judge12.md
