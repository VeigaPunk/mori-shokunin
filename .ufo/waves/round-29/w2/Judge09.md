# Judge09 — non-author judge: `r29-a2-10-stamped-send-survives` (A2-10)

Role: UFO-FSD reviewer / non-author judge, wave 2 (falsify). Leaf seat: no subagents, no background jobs.
Read-only inputs per assignment: round-27 contract.md:40-80, round-26 contract.md (whole, incl. A2 at :152-200
and the output spec), case object in `tools/fixtures/mori-oom-killers/cases-a2-r29.json` (id
`r29-a2-10-stamped-send-survives`), BASE output (tool at 7118f320) and FIX output (L1 draft) under
`/fast/scratch/hyaku/mori-r29/L1/judge/`. Did not read tool source, fix diff, other reports, or lessons.

## Case summary
- Object: `tools/fixtures/mori-oom-killers/cases-a2-r29.json` (case id `r29-a2-10-stamped-send-survives`,
  author CaseA210b, rule A2-10).
- Inputs: earlyoom active, `ActiveEnterTimestampMonotonic=8300000`; journal has version line at 8300000,
  in-scope stamped `sending SIGTERM to process 58152` at 8300020, and `sending SIGKILL to process 58153`
  with `__MONOTONIC_TIMESTAMP: "clock-unavailable"` (non-numeric); oomd inactive, notices 0.
- Expect: `KILLER_ACTED` / exit 1, `scope_complete=false`, `actions.sigterm=1`, `actions.sigkill=0`,
  `earlier_invocation_send_lines=0`.

## Field-by-field comparison (expected vs BASE vs FIX)

| Field | Expected | Base | Fix | Ruling | Contract line |
|---|---|---|---|---|---|
| verdict | KILLER_ACTED | KILLER_ACTED | KILLER_ACTED | match | round-26 contract.md:97-98; round-27 contract.md:58 |
| exit | 1 | 1 | 1 | match | round-26 contract.md:97-98 |
| earlyoom.state | active | active | active | match | input show; round-26 contract.md:90-91 |
| earlyoom.version | 1.9.0 | 1.9.0 | 1.9.0 | match | round-26 contract.md:82 (version line) |
| earlyoom.grammar | verified-1.9.0 | verified-1.9.0 | verified-1.9.0 | match | round-26 contract.md:91-92, :82 |
| earlyoom.scope_complete | false | false | false | match | round-26 contract.md:186-187; round-27 contract.md:58 |
| earlyoom.actions.sigterm | 1 | 1 | 1 | match | round-26 contract.md:85, :97-98 |
| earlyoom.actions.sigkill | 0 | 0 | 0 | match | round-26 contract.md:186-187 (non-numeric record uncounted) |
| earlyoom.actions.escalations | 0 | 0 | 0 | match | no escalation line; round-26 contract.md:86 |
| earlyoom.actions.kill_failed | 0 | 0 | 0 | match | no line; round-26 contract.md:87 |
| earlyoom.actions.low_memory_warnings | 0 | 0 | 0 | match | no line; round-26 contract.md:88 |
| earlyoom.dryrun_send_lines | 0 | 0 | 0 | match | no dryrun; round-26 contract.md:166-167 |
| earlyoom.process_group_lines | 0 | 0 | 0 | match | no line; round-26 contract.md:164-165 |
| earlyoom.earlier_invocation_send_lines | 0 | **1** | 0 | **tool error** | round-26 contract.md:186-187; round-27 contract.md:58 |
| oomd.state | inactive | inactive | inactive | match | input show; round-26 contract.md:95 |
| oomd.notices_this_boot | 0 | 0 | 0 | match | round-26 contract.md:95, :98 |

## The one discrepancy

- Field `earlyoom.earlier_invocation_send_lines`: expected 0, BASE 1, FIX 0.
- Rule text decides the value 0. round-26 contract.md:186-187: "a journal record without a numeric
  `__MONOTONIC_TIMESTAMP` is now **left uncounted** and makes the scope incomplete, instead of a setup error;
  positive evidence elsewhere still stands." The SIGKILL record's timestamp is the non-numeric string
  `clock-unavailable`, so it must not be counted in any counter — including `earlier_invocation_send_lines`
  (whose definition at round-26 contract.md:175-179 counts send/escalation lines of this boot outside the
  current invocation; an unpositionable, uncounted record contributes nothing). round-27 contract.md:58
  restates A2-10: "left uncounted and makes the scope incomplete; positive evidence elsewhere still stands".
- BASE's 1 therefore contradicts the rule text → **tool error**.

## FIX vs case

- FIX changes only `earlier_invocation_send_lines` 1 → 0; it now matches the case on every expect field,
  verdict, and exit (exit 1 both).
- No field the FIX changed is wrong under the rule text: the 0 matches the decided value, and the verdict
  stays `KILLER_ACTED` per round-26 contract.md:97-98 (the in-scope stamped SIGTERM at 8300020 is positive
  evidence that stands despite the incomplete scope).

## Residual risk / verification gaps

- [INFERENCE] I did not read the tool source or the L1 diff; conclusion "tool error" rests solely on the
  observed BASE output vs rule text (as instructed). The mechanism by which BASE assigned the non-numeric
  record to `earlier_invocation_send_lines` is unobserved.
- The BASE output's `thresholds: null` is not an expect field and is not ruled (no expectation either way).
- Case `why` cites round-26 contract.md:80-95, :164-179, :186-187, :97-98; all quoted rule lines were
  verified in the round-26 contract file read.

## Tooling note

- No tools installed/updated (nothing needed; read-only inspection via `read` and one `python3 -c` JSON
  extraction of the case object).

case_ruling=tool error
