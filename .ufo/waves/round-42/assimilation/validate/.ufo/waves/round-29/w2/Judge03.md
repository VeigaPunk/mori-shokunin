# Judge03 — non-author judge, frozen case `r29-a2-07-real-then-dryrun-zero-enter` (rule A2-07)

Role: non-author judge. Read only the permitted inputs (rule text, spec, case, base/fix outputs).
No tool source, no fix diff, no other reports, no lessons read. No tools installed (no installs
needed; nothing recorded per tooling directive).

## Inputs read
- Rule text: `.ufo/waves/round-27/contract.md:40-80` (A2-01..A2-10 at :49-58).
- Spec: `.ufo/waves/round-26/contract.md` (output spec :90-106, verdicts/exits :96-106, A2 :152-190).
- Case: `tools/fixtures/mori-oom-killers/cases-a2-r29.json` → object `r29-a2-07-real-then-dryrun-zero-enter`
  (rule A2-07, author CaseA207c, `why` at case object).
- Base output: `/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-07-real-then-dryrun-zero-enter.base.json`
  (tool at 7118f320; verdict KILLERS_UNKNOWN, exit 2).
- Fix output: `/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-07-real-then-dryrun-zero-enter.fix.json`
  (L1 draft; verdict KILLER_ACTED, exit 1).

## Case facts (inputs)
- `ActiveEnterTimestampMonotonic=0` → invocation unbounded → `scope_complete=false`
  (A2-05: round-27/contract.md:53; round-26/contract.md:173-174).
- Journal split at version lines (round-27/contract.md:55; round-26/contract.md:180-181):
  - invocation 1 (version @52000000): one real `sending SIGTERM to process ... violet-fern ...`
    (@52000010) → earlier invocation, real send.
  - invocation 2 (version @53000000, current): `dryrun mode enabled ...` (@53000010) then one
    `sending SIGTERM to process ... amber-lark ...` (@53000020) → current invocation is dry-run.

## Rulings for fields where expect differs from BASE output

| field | expected | base | fix | ruling | contract line |
|---|---|---|---|---|---|
| earlyoom.dryrun_send_lines | 1 | 2 | 1 | tool error | A2-04 round-27/contract.md:52 (`after dryrun mode enabled, send lines go to earlyoom.dryrun_send_lines, sigterm/sigkill stay 0, never positive evidence`); A2-07 round-27/contract.md:55 (`one dry-run invocation does not zero another invocation's real sends`); round-26/contract.md:166-167,180-181 |
| earlyoom.earlier_invocation_send_lines | 1 | 0 | 0 | tool error | A2-06 round-27/contract.md:54 (`send lines of this boot outside the current invocation go to earlyoom.earlier_invocation_send_lines`); round-26/contract.md:175-179 (counts send/escalation lines of this boot outside the current invocation) |

All other expect fields, verdict, and exit match BASE output (state=active, version=1.9.0,
grammar=verified-1.9.0, scope_complete=false, sigterm=0, sigkill=0, escalations=0, kill_failed=0,
low_memory_warnings=0, dryrun=true, oomd.state=inactive, oomd.notices_this_boot=0,
verdict=KILLERS_UNKNOWN, exit=2) — no ruling needed.

### Reasoning
- dryrun_send_lines: current invocation (second) is dry-run; its only send (amber-lark) → dryrun_send_lines=1.
  Base=2 counts both sends as dry-run, i.e. it failed to split per invocation (treated earlier real send as
  dry-run). Contradicts A2-07 / A2-04. `tool error`.
- earlier_invocation_send_lines: invocation 1's real send (violet-fern) is outside the current invocation →
  count 1. Base=0 contradicts A2-06. `tool error`.
- No `case error` / `unclear text` fields: case `why` matches the rule text on every pinned value, and every
  base-vs-expect difference is a rule-decided value the base output violates.

## FIX output vs case
| field | expected | fix | fix matches? | fix wrong under rule text? |
|---|---|---|---|---|
| earlyoom.dryrun_send_lines | 1 | 1 | yes | no (A2-04/A2-07 satisfied) |
| earlyoom.earlier_invocation_send_lines | 1 | 0 | no | yes — should be 1 (round-27/contract.md:54; round-26/contract.md:175-179) |
| earlyoom.actions.sigterm | 0 | 1 | no | yes — earlier real send must not count as current-invocation sigterm (A2-06 round-27/contract.md:54); dry-run invocation keeps sigterm 0 (A2-04 round-27/contract.md:52; round-26/contract.md:166-167) |
| verdict | KILLERS_UNKNOWN | KILLER_ACTED | no | yes — no positive evidence in scope (earlier real send does not change verdict for active earlyoom, A2-06 round-27/contract.md:54; dry-run never positive, A2-04 round-27/contract.md:52); KILLERS_UNKNOWN per round-26/contract.md:99-101 |
| exit | 2 | 1 | no | yes — must be 2 with KILLERS_UNKNOWN (round-26/contract.md:96-101) |

Fix changed 4 fields vs base: dryrun_send_lines (2→1, now correct), sigterm (0→1, wrong),
verdict (KILLERS_UNKNOWN→KILLER_ACTED, wrong), exit (2→1, wrong). All other fix fields equal base.
The fix repairs only dryrun_send_lines; it still contradicts the case and the rule text on
earlier_invocation_send_lines, sigterm, verdict, and exit (it appears to have moved the earlier real
send into current sigterm, making it positive evidence — exactly what A2-06/A2-04 forbid).

## Verdict
- Case is consistent with the rule text on every pinned field; no case errors.
- Base output has 2 tool errors (dryrun_send_lines, earlier_invocation_send_lines); verdict/exit correct.
- Fix output fixes dryrun_send_lines but introduces/keeps 4 errors (sigterm=1, earlier_invocation_send_lines=0,
  verdict=KILLER_ACTED, exit=1), i.e. still not a correct tool for this case.

`case_ruling=tool error`
