# Judge02 — wave-2 falsify: case `r29-a2-07-dryrun-then-real-missing-enter` (A2-07)

Seat: MoriR29.Judge02 (non-author judge, leaf). Judgment evidence was limited to the allowed rule text,
case object, and supplied base/fix outputs. No tool source, fix diff, other report, or lesson was read.

## Case (frozen `tools/fixtures/mori-oom-killers/cases-a2-r29.json:354-402`)

- rule A2-07; author CaseA207c; inputs: `earlyoom_show` `ActiveState=active`, no
  `ActiveEnterTimestampMonotonic` (missing); journal records at ts 42000000 (version `earlyoom 1.9.0`),
  42000010 (`dryrun mode enabled`), 43000000 (version), 43000010 (`sending SIGTERM to process …`).
- why (line 358): A2-05 ⇒ scope_complete false; A2-07 ⇒ second invocation real despite first dry-run;
  the SIGTERM send is in the current invocation ⇒ `actions.sigterm` 1; no dry-run sends in current
  invocation, no send lines in earlier invocation (A2-04/A2-06); positive evidence despite incomplete
  scope ⇒ `KILLER_ACTED`/exit 1 (round-26/contract.md:97-101).
- expect: verdict `KILLER_ACTED`, exit 1, fields as below.

## Rulings (base at 7118f320, fix = L1 draft)

Base output: `/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-07-dryrun-then-real-missing-enter.base.json:1-28`;
fix output: `/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-07-dryrun-then-real-missing-enter.fix.json:1-28`.
In the table, `r26/contract.md` and `r27/contract.md` abbreviate
`.ufo/waves/round-26/contract.md` and `.ufo/waves/round-27/contract.md`, respectively.

| field | expected | base | fix | ruling | contract line |
|---|---|---|---|---|---|
| verdict | KILLER_ACTED | KILLERS_UNKNOWN | KILLER_ACTED | tool error | r26/contract.md:97-98 (in-scope send = positive evidence), 180-182 (A2-07) |
| exit | 1 | 2 | 1 | tool error | r26/contract.md:97-98 (verdict ⇒ exit 1), 180-182 (A2-07) |
| earlyoom.state | active | active | active | match | — |
| earlyoom.version | 1.9.0 | 1.9.0 | 1.9.0 | match | — |
| earlyoom.grammar | verified-1.9.0 | verified-1.9.0 | verified-1.9.0 | match | — |
| earlyoom.scope_complete | false | false | false | match | r27/contract.md:53 (A2-05) |
| earlyoom.actions.sigterm | 1 | 0 | 1 | tool error | r26/contract.md:180-182 (A2-07: second invocation real), 85-88; case why line 358 |
| earlyoom.actions.sigkill | 0 | 0 | 0 | match | r26/contract.md:85-88 (SIGKILL has a separate grammar line; no such line in the case) |
| earlyoom.actions.escalations | 0 | 0 | 0 | match | r26/contract.md:85-88 |
| earlyoom.actions.kill_failed | 0 | 0 | 0 | match | r26/contract.md:85-88 |
| earlyoom.actions.low_memory_warnings | 0 | 0 | 0 | match | r26/contract.md:85-88 |
| earlyoom.dryrun | false | true | false | unclear text | r26/contract.md:89, 90-95, 180-182 (names flag; schema lists field; per-invocation rule does not define the output field's aggregation) |
| earlyoom.dryrun_send_lines | 0 | 1 | 0 | tool error | r26/contract.md:180-182 (A2-07: no dry-run sends in current invocation) |
| earlyoom.earlier_invocation_send_lines | 0 | 0 | 0 | match | r26/contract.md:175-179 (A2-06), case why line 358 |
| oomd.state | inactive | inactive | inactive | match | — |
| oomd.notices_this_boot | 0 | 0 | 0 | match | r26/contract.md:74-75 |

The `earlyoom.dryrun` divergence is `unclear text`: the output schema names `dryrun` and the grammar names a
dry-run flag (r26/contract.md:89, 90-95), while A2-07 specifies per-invocation handling of send lines but
does not say whether the output boolean means “any invocation” or “current invocation” (r26/contract.md:180-182).
The other divergences are decided by the rule text; base disagrees, so they are `tool error`. No divergence is
`case error`.

## Fix vs case

The fix matches the case on every field in `expect.fields`, plus verdict and exit. It changed
`sigterm` 0→1, `dryrun` true→false, `dryrun_send_lines` 1→0, verdict, and exit. No changed field is
contradicted by the rule text: the sends, count, verdict, and exit are correct under A2-07
(r26/contract.md:180-182) and the verdict rule (97-98). The `dryrun` output field remains undecidable under
the written contract; thus the fix's value matches the case but is not established as correct by the rule.

## Residual risk and verification gaps

The contract does not define whether `earlyoom.dryrun` is scoped to the current invocation or aggregated
across invocations; the fix matches the expected `false`, but that value cannot be confirmed against A2-07.
No independent tool run was performed; the assignment supplied base/fix outputs and prohibited reading tool
source or other artifacts.

case_ruling=mixed: tool error, unclear text

