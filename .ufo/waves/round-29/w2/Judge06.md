# Judge06 — frozen case judgment

Case: `r29-a2-10-zero-unbounded-mixed-sigterm` (`tools/fixtures/mori-oom-killers/cases-a2-r29.json`). Expected values are compared to BASE `/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-10-zero-unbounded-mixed-sigterm.base.json` and FIX `/fast/scratch/hyaku/mori-r29/L1/judge/r29-a2-10-zero-unbounded-mixed-sigterm.fix.json`.

| field | expected | base | fix | ruling | contract line |
|---|---:|---:|---:|---|---|
| verdict | `KILLER_ACTED` | `KILLER_ACTED` | `KILLER_ACTED` | — (base matches) | round-26 `:96-99` |
| exit | 1 | 1 | 1 | — (base matches) | round-26 `:96-99` |
| `earlyoom.state` | `active` | `active` | `active` | — (base matches) | round-26 `:90-95` |
| `earlyoom.version` | `1.9.0` | `1.9.0` | `1.9.0` | — (base matches) | round-26 `:80-84,90-95` |
| `earlyoom.grammar` | `verified-1.9.0` | `verified-1.9.0` | `verified-1.9.0` | — (base matches) | round-26 `:80-89,90-95` |
| `earlyoom.scope_complete` | `false` | `false` | `false` | — (base matches) | round-27 `:53,58`; round-26 `:78-79,173-174` |
| `earlyoom.actions.sigterm` | 1 | 1 | 1 | — (base matches) | round-26 `:78-85,96-99`; A2 `:186-188` |
| `earlyoom.actions.sigkill` | 0 | 1 | 0 | **tool error** | round-27 `:58`: a record without a numeric timestamp is “left uncounted” and positive evidence elsewhere still stands; round-26 `:186-188` |
| `earlyoom.actions.escalations` | 0 | 0 | 0 | — (base matches) | round-26 `:86,90-95` |
| `earlyoom.actions.kill_failed` | 0 | 0 | 0 | — (base matches) | round-26 `:87,90-95` |
| `earlyoom.actions.low_memory_warnings` | 0 | 0 | 0 | — (base matches) | round-26 `:88,90-95` |
| `earlyoom.process_group_lines` | 0 | 0 | 0 | — (base matches) | round-26 `:164-165` |
| `earlyoom.earlier_invocation_send_lines` | 0 | 0 | 0 | — (base matches) | round-26 `:175-179` |
| `earlyoom.dryrun` | `false` | `false` | `false` | — (base matches) | round-26 `:89-95,166-167` |
| `earlyoom.dryrun_send_lines` | 0 | 0 | 0 | — (base matches) | round-26 `:166-167` |
| `oomd.state` | `inactive` | `inactive` | `inactive` | — (base matches) | round-26 `:90-95,99-104` |
| `oomd.notices_this_boot` | 0 | 0 | 0 | — (base matches) | round-26 `:90-95,96-104` |

Only `earlyoom.actions.sigkill` differs between case expectation and BASE. Its timestamp is `not-numeric`; A2-10 requires that record be left uncounted and makes scope incomplete (round-27 `:58`, round-26 `:186-188`), so expected zero is correct and BASE's one is a tool error. The numeric SIGTERM record is in the scope beginning at active-enter timestamp zero (round-26 `:78-79`); its positive evidence supports `KILLER_ACTED` despite incomplete scope (round-26 `:96-99`). FIX matches the case on every listed field, including `sigkill=0`; the field it changes is now correct under the rule text.

Residual risk / verification gaps: none within the assigned case, contract passages, and supplied BASE/FIX outputs; no runtime or other cases were examined.

case_ruling=tool error
