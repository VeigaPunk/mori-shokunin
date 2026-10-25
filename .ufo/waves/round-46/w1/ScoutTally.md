# ScoutTally — rerun of the three selftest tallies

Scope: this seat only reruns and reports the three selftest tallies pinned by
`.ufo/waves/round-46/count-repins.py`. No edits made; no other seat's files touched.

## Commands and results (run 2026-10-25, cwd = lane repo root)

### 1. Gate registry auditor — `python3 tools/mori-gate-registry.py --selftest`

15 `selftest PASS` lines:
`registered_row_met`, `missing_cell_rejected`, `unresolved_entry_rejected`,
`unregistered_path_rejected`, `no_selftest_rejected`, `seven_cell_row_rejected`,
`second_table_registered`, `duplicate_name_rejected`, `comment_only_selftest_rejected`,
`empty_population_rejected`, `audit_all_with_audit_refused`, `population_mode_and_digest`,
`escape_flag_accepted`, `escape_flag_name_rejected`, `escape_flag_mention_rejected`.

```
GATE_REGISTRY_SELFTEST pass=15 fail=0
EXIT=0
```

### 2. R45 ledger counter — `python3 .ufo/waves/round-45/count-c1.py --selftest`

16 `selftest PASS` lines:
`honest_ledger_met`, `offbyone_row_mismatch`, `junk_producer_rejected`,
`below_floor_rejected`, `absent_ledger_unmet`, `duplicate_id_rejected`,
`duplicate_command_rejected`, `head_reading_row_rejected`, `revision_constant_row_rejected`,
`witness_dir_one_passing_witness`, `all_const_ledger_unmet`, `const_heavy_ledger_unmet`,
`witness_without_floor_unmet`, `stage_option_injection_rejected`, `short_sha_tip_rejected`,
`absent_path_zero_rejected`.

```
C1_SELFTEST pass=16 fail=0
EXIT=0
```

### 3. R45 gate conformance — `python3 .ufo/waves/round-45/count-c2.py --selftest`

14 `selftest PASS` lines:
`conformant_met`, `auditor_absent_unmet`, `auditor_red_unmet`, `duplicate_row_unmet`,
`comment_only_selftest_unmet`, `surviving_mutant_unmet`, `writescope_mismatch_unmet`,
`narrowed_v1_unmet`, `registered_mismatch_unmet`, `tables_floor_unmet`,
`env_auditor_ignored`, `git_dir_poisoned_ignored`, `worktree_mutant_not_counted`,
`path_escape_refused`.

```
C2_SELFTEST pass=14 fail=0
EXIT=0
```

## Agreement with the frozen pins (count-repins.py ROWS)

| Pinned tally (needle) | Pinned in row(s) | Measured this run | Match |
|---|---|---|---|
| `GATE_REGISTRY_SELFTEST pass=15 fail=0` | `r44 gate registry (C2)`, `r44 gate registry (C2) — write scope superseded` | `pass=15 fail=0`, rc 0 | ✓ |
| `C1_SELFTEST pass=16 fail=0` | `r45 ledger counter (C1)` | `pass=16 fail=0`, rc 0 | ✓ |
| `C2_SELFTEST pass=14 fail=0` | `r45 gate conformance (C2)` | `pass=14 fail=0`, rc 0 | ✓ |

All three measured tallies equal the pins and the round-45 freeze record
(`.ufo/waves/round-45/evidence/freeze-r45.txt` records the same instrument
digests; tally replay is consistent). Each printed `pass=N` corresponds to a
distinct printed `selftest PASS <arm>` line (15/16/14 arms), so the counts are
not fabricated strings — arm names are observable in the same output.

## Notes

- The three tally strings are emitted by three distinct instruments: `tools/mori-gate-registry.py`
  (GATE_REGISTRY_SELFTEST), `.ufo/waves/round-45/count-c1.py` (C1_SELFTEST),
  `.ufo/waves/round-45/count-c2.py` (C2_SELFTEST). `GATE_REGISTRY_SELFTEST` is pinned in two rows.
- Instrument digests / line counts are out of this seat's scope (ScoutDigests / ExecAuditorLines).
- No tool installs/upgrades made; no pacman; no git/jj mutations.
