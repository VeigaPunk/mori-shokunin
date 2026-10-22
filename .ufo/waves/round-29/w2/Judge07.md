# Judge07 — non-author review of frozen case `r29-a2-10-zero-unbounded-mixed-sigkill`

Scope held: read only round-27 contract.md:40-80, round-26 contract.md (whole), the case object in
`tools/fixtures/mori-oom-killers/cases-a2-r29.json`, and the two tool outputs in
`/fast/scratch/hyaku/mori-r29/L1/judge/`. Did not read tool source, the fix diff, other reports, or lessons.
No tools installed (none needed). No git/jj writes; no live-mode tool run.

## Inputs of the case (cases-a2-r29.json, id `r29-a2-10-zero-unbounded-mixed-sigkill`, rule A2-10)

- `earlyoom_show`: `ActiveState=active`, `ActiveEnterTimestampMonotonic=0`.
- Journal records: (1) `earlyoom 1.9.0` stamped `91000000`; (2) `sending SIGTERM to process 6301 "fictional-cirrus"`
  with **no** `__MONOTONIC_TIMESTAMP` key; (3) `sending SIGKILL to process 6302 "fictional-driftwood"` stamped
  `91000600`. `oomd_notices=0`, oomd `ActiveState=inactive`.
- Expect: verdict `KILLER_ACTED`, exit 1, and 15 pinned `expect.fields` paths.

## Field-by-field: expected vs BASE vs FIX

| field | expected | base | fix | ruling | contract line |
|---|---|---|---|---|---|
| verdict | KILLER_ACTED | KILLER_ACTED | KILLER_ACTED | (match) | round-26:97-98 |
| exit | 1 | 1 | 1 | (match) | round-26:61,97 |
| earlyoom.state | active | active | active | (match) | round-26 output spec |
| earlyoom.version | 1.9.0 | 1.9.0 | 1.9.0 | (match) | round-26:81 |
| earlyoom.grammar | verified-1.9.0 | verified-1.9.0 | verified-1.9.0 | (match) | round-26:81 |
| earlyoom.scope_complete | false | false | false | (match) | round-27:53; round-26:173-174 |
| earlyoom.actions.sigterm | 0 | **1** | 0 | **tool error** | round-27:58; round-26:186-187 |
| earlyoom.actions.sigkill | 1 | 1 | 1 | (match) | round-26:78-79,85 |
| earlyoom.actions.escalations | 0 | 0 | 0 | (match) | round-26:86 |
| earlyoom.actions.kill_failed | 0 | 0 | 0 | (match) | round-26:87 |
| earlyoom.actions.low_memory_warnings | 0 | 0 | 0 | (match) | round-26:88 |
| earlyoom.process_group_lines | 0 | 0 | 0 | (match) | round-27:51 |
| earlyoom.earlier_invocation_send_lines | 0 | 0 | 0 | (match) | round-27:54; round-26:175-177 |
| earlyoom.dryrun | false | false | false | (match) | round-26:89 |
| earlyoom.dryrun_send_lines | 0 | 0 | 0 | (match) | round-27:52 |
| oomd.state | inactive | inactive | inactive | (match) | round-26 output spec |
| oomd.notices_this_boot | 0 | 0 | 0 | (match) | round-26 output spec |

Base↔fix delta confirmed mechanically: `diff` of the two pretty-printed outputs shows exactly one changed key,
`earlyoom.actions.sigterm`: 1 → 0 (both files `# exit: 1`).

## Ruling on the single differing field: `earlyoom.actions.sigterm`

**`tool error`.** The rule text decides the pinned value and the base tool disagrees.

- The SIGTERM record in the case inputs carries no `__MONOTONIC_TIMESTAMP` key.
- Round-27 frozen rule list, A2-10 (`.ufo/waves/round-27/contract.md:58`): *"a journal record without a numeric
  `__MONOTONIC_TIMESTAMP` is left uncounted and makes the scope incomplete; positive evidence elsewhere still stands"*.
- Round-26 amendment A2, wave-2 fix D1 (`.ufo/waves/round-26/contract.md:186-187`): *"a journal record without a
  numeric `__MONOTONIC_TIMESTAMP` is now left uncounted and makes the scope incomplete, instead of a setup error;
  positive evidence elsewhere still stands."*
- "Left uncounted" decides the count: this record must not raise `earlyoom.actions.sigterm`. Base prints `sigterm: 1`,
  so it counted an uncountable record → `tool error`. The text is not ambiguous ("unclear text" does not apply), and
  the case's expect (0) agrees with the rule text ("case error" does not apply).

Consistency cross-checks of the expect under the rule text (no case error found anywhere):

- scope_complete=false is forced by A2-05 (round-27:53: "`ActiveEnterTimestampMonotonic` missing or `0` leaves the
  invocation unbounded: `scope_complete` false"; round-26:173-174).
- The stamped SIGKILL at 91000600 ≥ AETM 0 is in scope (round-26:78-79: scope = lines with
  `__MONOTONIC_TIMESTAMP` ≥ `ActiveEnterTimestampMonotonic`) and follows the current invocation's version line, so
  it counts as one action (round-26:85: "`sending SIGTERM to process ` / `sending SIGKILL to process ` → one action
  each"). Expect sigkill=1 is right; base and fix agree.
- Positive evidence stands despite the incomplete scope (round-26:97-98: "`KILLER_ACTED`, exit 1: any earlyoom
  `sending SIG…to process` or escalation line in scope … Positive evidence stands even when the scope is
  incomplete"; exit = verdict code, round-26:61). Expect verdict/exit KILLER_ACTED/1 is right.

## Fix evaluation

- The FIX output matches the case on every pinned field: verdict, exit, and all 15 `expect.fields` paths.
- The fix changed only `earlyoom.actions.sigterm` (1 → 0). That is exactly what A2-10 requires; no field the fix
  changed is now wrong under the rule text. The corrected `sigterm=0` does not change the verdict, since the SIGKILL
  line remains positive evidence in scope.

## Residual risk and verification gaps

- I did not run the tool myself (outputs taken from the L1's `.base.json`/`.fix.json` as instructed); if those files
  were not produced from the pinned revisions, this judgment would not transfer. [INFERENCE] they are as labeled.
- Line-number citations for round-26 output-spec rows (`state`, `notices_this_boot`) refer to the schema bullet
  block (round-26:90-95 region) without per-row line quotes; the fields matched trivially in both outputs.
- No other seat's findings were consulted, per the read-only scope.

`case_ruling=tool error`
