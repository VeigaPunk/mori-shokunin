# Judge04 — wave-2 falsify findings

Case: `r29-a2-07-real-dryrun-real-missing-enter` (rule A2-07, author CaseA207c) in `tools/fixtures/mori-oom-killers/cases-a2-r29.json`.
Read-only inputs: `.ufo/waves/round-27/contract.md:40-80`, `.ufo/waves/round-26/contract.md` (whole, incl. amendment A2 at :152-200), the case object, and
`/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-07-real-dryrun-real-missing-enter.base.json` (tool at 7118f320) / `.fix.json` (L1 draft).
Not read: tool source, fix diff, other reports, lessons. No tool installs/updates this seat (read tool only).

## Case shape

- `earlyoom_show`: `LoadState=loaded`, `ActiveState=active`, `UnitFileState=enabled` — **no `ActiveEnterTimestampMonotonic`** (A2-05: unbounded invocation, `scope_complete` false; round-26/contract.md:173-174).
- Journal, three version-separated invocations: inv1 real (`sending SIGTERM ...` @62000010), inv2 dry-run (`dryrun mode enabled` @63000010, no sends), inv3 real (`sending SIGKILL ...` @64000010).
- Expect: `KILLER_ACTED`/exit 1; `sigkill=1`, `sigterm=0`, `dryrun=false`, `dryrun_send_lines=0`, `earlier_invocation_send_lines=1`, `scope_complete=false`; A2-07 (round-27/contract.md:55) makes inv3 independent of inv2's dry-run; A2-06/earlier-invocations (round-26/contract.md:175-179) puts inv1's SIGTERM in `earlier_invocation_send_lines`.

## Per-field table

| field | expected | base | fix | ruling | contract line |
|---|---|---|---|---|---|
| verdict | KILLER_ACTED | KILLERS_UNKNOWN | KILLER_ACTED | tool error | round-26/contract.md:97-98; :180-182; round-27/contract.md:55 |
| exit | 1 | 2 | 1 | tool error | round-26/contract.md:97; :180-182; round-27/contract.md:55 |
| earlyoom.state | active | active | active | match (no ruling) | round-26/contract.md:90 |
| earlyoom.version | 1.9.0 | 1.9.0 | 1.9.0 | match | round-26/contract.md:82 |
| earlyoom.grammar | verified-1.9.0 | verified-1.9.0 | verified-1.9.0 | match | round-26/contract.md:91 |
| earlyoom.scope_complete | false | false | false | match | round-26/contract.md:173-174 (A2-05) |
| earlyoom.actions.sigterm | 0 | 0 | 1 | match for base (fix wrong) | fix contradicts round-26/contract.md:175-179 (earlier send → `earlier_invocation_send_lines`, not current action); round-27/contract.md:54 |
| earlyoom.actions.sigkill | 1 | 0 | 1 | tool error | round-27/contract.md:55; round-26/contract.md:85-86,180-182 |
| earlyoom.actions.escalations | 0 | 0 | 0 | match | round-26/contract.md:85-86 |
| earlyoom.actions.kill_failed | 0 | 0 | 0 | match | round-26/contract.md:87 |
| earlyoom.actions.low_memory_warnings | 0 | 0 | 0 | match | round-26/contract.md:88 |
| earlyoom.dryrun | false | true | true | tool error (fix still wrong) | round-27/contract.md:55 (per-invocation); round-26/contract.md:89,166-167 |
| earlyoom.dryrun_send_lines | 0 | 2 | 0 | tool error | round-26/contract.md:166-167,180-182; round-27/contract.md:55 |
| earlyoom.earlier_invocation_send_lines | 1 | 0 | 0 | tool error (fix still wrong) | round-26/contract.md:175-179 |
| oomd.state | inactive | inactive | inactive | match | round-26/contract.md:95 |
| oomd.notices_this_boot | 0 | 0 | 0 | match | round-26/contract.md:95 |

## Reasoning (quoted contract lines)

- A2-07: "dry-run applies per invocation (split at each version line): one dry-run invocation does not zero another invocation's real sends" (round-27/contract.md:55).
- Positive evidence: "any earlyoom `sending SIG…to process` or escalation line in scope … `KILLER_ACTED`, exit 1. Positive evidence stands even when the scope is incomplete." (round-26/contract.md:97-98).
- Earlier invocations: "a new field `earlyoom.earlier_invocation_send_lines` counts send and escalation lines of this boot outside the current invocation." (round-26/contract.md:175-176).
- A2-04: "when the invocation logged `dryrun mode enabled`, send lines go to `earlyoom.dryrun_send_lines`, `sigterm`/`sigkill` stay 0 and they are never positive evidence" (round-26/contract.md:166-167) — per invocation under A2-07; inv2 has no send lines, so `dryrun_send_lines=0`.
- A2-05: "`ActiveEnterTimestampMonotonic` missing or `0` leaves the invocation unbounded, so `scope_complete` is false" (round-26/contract.md:173-174) — consistent on both tools.

### Base (7118f320): tool error on 6 fields
Base applied inv2's dry-run flag to the whole boot (`dryrun=true`, `dryrun_send_lines=2` absorbing both real sends), zeroed `sigkill`/`sigterm`, saw no positive evidence → `KILLERS_UNKNOWN`/exit 2, and reported `earlier_invocation_send_lines=0`. Each contradicts the lines above; the case matches the rule text (no case error, no unclear text on any pinned value).

## Fix (L1 draft)

Matches case on: verdict, exit, sigkill=1, dryrun_send_lines=0, plus all unchanged fields.
Still wrong / newly wrong under the rule text:
- `dryrun=true` — current invocation is real; per-invocation dry-run (round-27/contract.md:55) requires false.
- `earlyoom.actions.sigterm=1` — inv1's SIGTERM is an earlier invocation's send; must go to `earlier_invocation_send_lines` (round-26/contract.md:175-176), leaving sigterm 0.
- `earlier_invocation_send_lines=0` — must be 1 (same lines).

`case_ruling=tool error`
