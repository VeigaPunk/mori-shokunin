# Judge08 — non-author judge, frozen case `r29-a2-10-unclocked-send-alone` (A2-10)

## Scope read (only permitted sources)
- Rule text: `.ufo/waves/round-27/contract.md:40-80` (C2 table; A2-10 at line 58).
- Round-26 contract whole spec: `.ufo/waves/round-26/contract.md` (interface :58-109, verdicts/exits :96-106,
  Amendment A2 :152-190; key lines 166-169, 186-187).
- Case object: `tools/fixtures/mori-oom-killers/cases-a2-r29.json`, id `r29-a2-10-unclocked-send-alone`
  (rule A2-10, author CaseA210b), extracted via jq.
- Tool outputs: `/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-10-unclocked-send-alone.base.json`
  (tool at 7118f320) and `.fix.json` (L1 draft).
- Did NOT read: tool source, fix diff, other reports, lessons.

## Case input facts
- `earlyoom_show`: ActiveState=active, ActiveEnterTimestampMonotonic=7200000.
- `earlyoom_journal` (2 records):
  1. "earlyoom 1.9.0", `__MONOTONIC_TIMESTAMP` = "7200000" (version line of current invocation);
  2. "sending SIGTERM to process 48152" — **no `__MONOTONIC_TIMESTAMP` field at all** (unclocked).
- `oomd_show`: inactive; `oomd_notices`=0.

## Field-by-field comparison
Field | expected | base | fix | ruling | contract line
---|---|---|---|---|---
`earlyoom.state` | active | active | active | match | round-26 contract.md:90
`earlyoom.version` | 1.9.0 | 1.9.0 | 1.9.0 | match | round-26 contract.md:91
`earlyoom.grammar` | verified-1.9.0 | verified-1.9.0 | verified-1.9.0 | match | round-26 contract.md:92
`earlyoom.scope_complete` | false | false | false | match | round-27 contract.md:58; round-26 contract.md:186-187
`earlyoom.actions.sigterm` | 0 | 0 | 0 | match | round-27 contract.md:58 (uncounted)
`earlyoom.actions.sigkill` | 0 | 0 | 0 | match | round-27 contract.md:58
`earlyoom.actions.escalations` | 0 | 0 | 0 | match | round-27 contract.md:58
`earlyoom.actions.kill_failed` | 0 | 0 | 0 | match | round-27 contract.md:58
`earlyoom.actions.low_memory_warnings` | 0 | 0 | 0 | match | round-27 contract.md:58
`earlyoom.dryrun_send_lines` | 0 | 0 | 0 | match | round-26 contract.md:166-167 (A6)
`earlyoom.process_group_lines` | 0 | 0 | 0 | match | round-26 contract.md:164 (A5)
`earlyoom.earlier_invocation_send_lines` | **0** | **1** | 0 | **tool error** | round-27 contract.md:58; round-26 contract.md:186-187
`oomd.state` | inactive | inactive | inactive | match | round-26 contract.md:90
`oomd.notices_this_boot` | 0 | 0 | 0 | match | round-26 contract.md:73,97
`verdict` | KILLERS_UNKNOWN | KILLERS_UNKNOWN | KILLERS_UNKNOWN | match | round-26 contract.md:99-101
`exit` | 2 | 2 | 2 | match | round-26 contract.md:99-101

## Ruling for the single differing field

**`earlyoom.earlier_invocation_send_lines`: expected 0, base 1, fix 0.**

- Rule A2-10 (round-27 contract.md:58; restated round-26 contract.md:186-187): a journal record without a
  numeric `__MONOTONIC_TIMESTAMP` "is left uncounted and makes the scope incomplete; positive evidence
  elsewhere still stands". "Left uncounted" means the record contributes to **no** count — including
  `earlier_invocation_send_lines`.
- The BASE output counted the unclocked "sending SIGTERM to process 48152" line as
  `earlier_invocation_send_lines` = 1, contradicting A2-10's "left uncounted".
- Supporting reading: A2-06 (round-27 contract.md:54) defines `earlier_invocation_send_lines` as send lines
  "of this boot outside the current invocation"; an unclocked record has no timestamp, so it cannot be
  placed outside the current invocation either.
- The case's own `why` (cases-a2-r29.json) pins the same reading: "round-26 contract.md:186-187 leaves this
  send uncounted and makes scope incomplete".
- **Ruling: tool error.**

## Fix check

- The FIX output matches the case on **every** expect field: verdict (KILLERS_UNKNOWN), exit (2), and all 14
  `expect.fields` paths, including the corrected `earlier_invocation_send_lines` = 0.
- The only field the fix changed (`earlier_invocation_send_lines` 1 → 0) is now correct under the rule text
  (A2-10); no field changed by the fix is wrong under the rule text. All other fix fields are identical to
  base and still match the case.

## Verdict

`case_ruling=tool error`

Residual risk / verification gaps: none material — the case has exactly one field where base differs from
expect; verdict and exit agree in base and fix, so no verdict-side ambiguity exists. The draft fix resolves
the single mismatch; no other field changes.
