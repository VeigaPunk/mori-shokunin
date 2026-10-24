# ExeConjunctAfter — Round 40 wave 1

## Result

Re-derived both conjunct mutation receipts. The v3 gutted copy failed all 10 selftests; every failing list includes `selftest_conjunct`. The r39 gutted copy passed all 8 selftests with no failures.

## Commands and exact outputs

Working directory for both commands: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

Command:
```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest
```
Output:
```text
FAIL predicate          predicate token changed -> failing=['predicate', 'selftest_conjunct'] (want [predicate])
FAIL head_pin           pin label renamed -> failing=['head_pin', 'selftest_conjunct'] (want [head_pin])
FAIL tool_resolve       relative resolution removed -> failing=['selftest_conjunct', 'tool_resolve'] (want [tool_resolve])
FAIL bounded_reads      git helper run timeout removed -> failing=['bounded_reads', 'selftest_conjunct'] (want [bounded_reads])
FAIL timeout_scope      timeout value replaced with None -> failing=['selftest_conjunct', 'timeout_scope'] (want [timeout_scope])
FAIL timeout_scope_shadow function-local None shadow inserted -> failing=['selftest_conjunct', 'timeout_scope'] (want [timeout_scope])
FAIL drain_bind         communicate drains replaced by wait+read -> failing=['drain_bind', 'selftest_conjunct'] (want [drain_bind])
FAIL drain_bind_decoy   decoy used communicate beside a wait+read drain -> failing=['drain_bind', 'selftest_conjunct'] (want [drain_bind])
FAIL timeout_state      budget flag ignored -> failing=['selftest_conjunct', 'timeout_state'] (want [timeout_state])
FAIL scratch            scratch parent moved off-lane -> failing=['scratch', 'selftest_conjunct'] (want [scratch])
CONFORM_SELFTEST pass=0 fail=10
EXIT=1
```

Command:
```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/conform-r39-conjunct-gutted.py bb1f2457 --selftest
```
Output:
```text
PASS predicate          predicate token changed -> only predicate failed
PASS head_pin           pin label renamed -> only head_pin failed
PASS tool_resolve       relative resolution removed -> only tool_resolve failed
PASS bounded_reads      git helper run timeout removed -> only bounded_reads failed
PASS timeout_value      timeout value replaced with None -> only timeout_value failed
PASS drain_shape        communicate drains replaced by wait+read -> only drain_shape failed
PASS timeout_state      budget flag ignored -> only timeout_state failed
PASS scratch            scratch parent moved off-lane -> only scratch failed
CONFORM_SELFTEST pass=8 fail=0
EXIT=0
```

## Artifacts and notes

- Updated `.ufo/waves/round-40/evidence/c10-after-conjunct.txt` and `.ufo/waves/round-40/evidence/c10-red-conjunct.txt` with these command outputs.
- No tool installs. No blockers.
- These receipts exercise the named gutted copies; they are mutation-selftest evidence, not a separate run of the unmodified checker.
