# Judge10 — non-author judge, frozen case `r29-a2-10-oomd-evidence-survives` (A2-10)

Reviewed: case object at `tools/fixtures/mori-oom-killers/cases-a2-r29.json:912-952`
(id/rule/why at :913-916); rule text round-27 `contract.md:47-58` (A2-10 at :58) and
round-26 `contract.md` (output spec :90-106; added counters :164-179; A2-10 supersession
:186-187); base tool output `r29-a2-10-oomd-evidence-survives.base.json` (tool at
7118f320, exit 1); fix tool output `r29-a2-10-oomd-evidence-survives.fix.json` (L1
draft, exit 1). Per assignment, tool source, fix diff, other reports and lessons were not
read. No tools installed (none needed); no scratch files written.

## Comparison

Only one expect field differs from BASE:

| field | expected | base | fix | ruling | contract line |
|---|---|---|---|---|---|
| `earlyoom.earlier_invocation_send_lines` | 0 | 1 | 0 | tool error | round-27 contract.md:58; round-26 contract.md:175-176, 186-187 |

All other expect fields match BASE and FIX identically: `verdict` `KILLER_ACTED`,
`exit` 1, `earlyoom.state` active, `version` `1.9.0`, `grammar` `verified-1.9.0`,
`scope_complete` false, `actions.sigterm`/`sigkill`/`escalations`/`kill_failed`/
`low_memory_warnings` 0, `dryrun_send_lines` 0, `process_group_lines` 0,
`oomd.state` active, `oomd.notices_this_boot` 2.

## Ruling for the differing field

- Deciding text: round-27 contract.md:58: "a journal record without a numeric
  `__MONOTONIC_TIMESTAMP` is left uncounted and makes the scope incomplete; positive
  evidence elsewhere still stands". Same rule at round-26 contract.md:186-187 ("is now
  left uncounted and makes the scope incomplete, instead of a setup error; positive
  evidence elsewhere still stands").
- The field counts lines "of this boot outside the current invocation" (round-26
  contract.md:175-176). A record "left uncounted" under A2-10 cannot populate any
  counter, including `earlier_invocation_send_lines`. The case inputs hold exactly one
  malformed timestamp (`__MONOTONIC_TIMESTAMP: "not-a-decimal"`, cases file :927) on
  the SIGTERM line; no other line can be an earlier-invocation send.
- Therefore the rule text decides `earlier_invocation_send_lines` = 0; BASE output 1
  disagrees → **tool error** (not `case error` — the case matches the rule text; not
  `unclear text` — the rule decides the pinned value).

## Fix status

- FIX matches the case on every expect field, including `earlier_invocation_send_lines`
  0.
- The only field FIX changed (1 → 0) is correct under the rule text: it now complies
  with "left uncounted" (round-27 contract.md:58; round-26 contract.md:186-187). No
  changed field is wrong under the rule text.

case_ruling=tool error
