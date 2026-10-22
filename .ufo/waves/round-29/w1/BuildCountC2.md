# BuildCountC2 — round 29

## Deliverable

- Script: /fast/scratch/hyaku/mori-r29/BuildCountC2/count-c2.sh (scratch only; L1 copies it into the lane).
- SHA-256: 220eb99122d0cb9a4c96f6f88656f4170d025427afaca895a7d4f2bd89c2c51f
- No tools installed or updated.
- The counter reads committed tool, case, report and checker bytes; extracts and the checker worktree are temporary. It checks both old blob baselines and self-tests, exact-once markers, full-history single-add freeze, unchanged blob, A2 shape pins, fixed-writer provenance, global canonical input uniqueness, and the committed blind-wave check.

## Sandbox scenarios

All cases/reports were invented only in the scratch clone. The new-case self-test was stubbed in the sandbox counter copy only; the two older-file self-tests used the actual tool. No synthetic case or report content is included here.

| Scenario | Evidence | Exit |
|---|---|---:|
| Absent file at 7118f320 | a2_r29_schema=absent; C2=unmet | 1 |
| Strict-schema failure | a2_r29_schema=error top_level_keys_mismatch; C2=unmet | 1 |
| Too few cases | 10 total, 5/rule; rule checks failed | 1 |
| Too few authors | 2/rule; four missing writers printed; rule checks failed | 1 |
| Missing required pin | A2-07 unpinned=1; A2-07 shape fell to 1/1 | 1 |
| Duplicate id | a2_r29_schema=error duplicate_id | 1 |
| Edited after freeze | freeze_edits=1; cases_changed_since_freeze=1 | 1 |
| Unselected report case | provenance=12/12 unselected=1 | 1 |
| Duplicate input across rules | a2_r29_distinct_inputs=11/12; input checks failed | 1 |
| Blindness violation | blind_exit=1; blind_violations=1 | 1 |
| Met-path logic | 12 cases; both shapes 2/2; provenance=12/12 unselected=0; blind_violations=0; old self-tests pass | 0 |
| Invalid revision | error=bad_rev; C2=unmet | 2 |

The met-path run used the sandbox-only new-case self-test stub; it does not establish an actual new-file self-test pass.
Risk [INFERENCE]: production journal phrasing was not inspected; version/send token matching is tested on synthetic inputs only. The real new-file self-test and final provenance/blind receipt remain for L1 to exercise at the freeze tip.

## Exact output at 7118f320

Exit code: 1.

```text
rev=7118f320a5ef18d20c1e361eff77db0e1a97b2d6
tool_blob=3fb78bbc2612c38e463e04083bdb213954647568
cases_blob=5b4dcee7b682c896c8e9f22ed1f8ac58d0176556
cases_baseline_blob=5b4dcee7b682c896c8e9f22ed1f8ac58d0176556
cases_blob_state=match
cases_a2_blob=7ba553d45e3b00d507e57132cc3c28fb140f83fd
cases_a2_baseline_blob=7ba553d45e3b00d507e57132cc3c28fb140f83fd
cases_a2_blob_state=match
cases_a2_r29_blob=absent
cases_selftest=PASS 32/32
cases_a2_selftest=PASS 30/30
freeze_commit=none
freeze_path=none
freeze_adds=0
freeze_adds_raw=0
freeze_renames=0
freeze_deletes=0
freeze_edits=0
freeze_blob_versions=0
cases_changed_since_freeze=1
tool_blob_at_freeze=none
writer_absent=CaseA207a
writer_absent=CaseA207b
writer_absent=CaseA207c
writer_absent=CaseA207d
writer_absent=CaseA210a
writer_absent=CaseA210b
writer_absent=CaseA210c
writer_absent=CaseA210d
blind_exit=not_run
blind_violations=not_run
provenance=0/0 unselected=0
provenance_errors=0
a2_r29_schema=absent
a2_r29_cases=0
a2_r29_ids=absent
a2_r29_rules_covered=0/2
a2_r29_distinct_inputs=0/0
a2_r29_legacy_input_overlaps=0
a2_r29_input_checks=fail:file_absent
a2_r29_rule_checks=fail:file_absent
shape_a207=0/0
shape_a210=0/0
a2_r29_selftest=absent
C2=unmet
```

