# RevC4Kill — `drift_kill` check re-derivation (round 38, w1)

Verdict: **PASS** — the `row_states` selftest arm is killed by its own mutation
(`return "drifted"` → `return "excerpt"`) and its FAIL detail names S103.

## Method (all read-only against the lane; mutation on a scratch copy)

1. Extracted the scored-tip tool:
   `git show f725f3076972e6e70595b5ac8279be524a111ff8:tools/mori-source-drift.py > /tmp/drift-orig.py`
   (466 lines; sole `return "drifted"` at line 208, the `classify` fallthrough
   after the `fresh` hash check and the `excerpt` substring check, lines 202–208).
2. Scratch copy `/tmp/revc4kill/drift-mut.py`: replaced `return "drifted"` with
   `return "excerpt"` (verified: line 208 now `return "excerpt"`; lines 207–208
   both read `return "excerpt"`). Lane files untouched.
3. Ran `python3 <each> --selftest` on both copies.

## Unmutated selftest (control)

```
selftest exit_code            PASS
selftest row_states           PASS
selftest summary              PASS
selftest huge_cap             PASS
selftest redirect_private_refused PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)
```

- `row_states` line: `selftest row_states           PASS`
- Exit code: **0**

## Mutated selftest (`return "drifted"` → `return "excerpt"`)

```
selftest exit_code            FAIL (rc=0 want 1 (one drifted))
selftest row_states           FAIL (got=[('S101', 'fresh'), ('S102', 'excerpt'),
  ('S103', 'excerpt'), ('S104', 'unavailable'), ('S105', 'unavailable'),
  ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'),
  ('S109', 'unavailable'), ('S110', 'unavailable')]
  want=[... ('S103', 'drifted') ...])
selftest summary              FAIL (summary=('10', '2', '2', '0', '4', '2'))
selftest huge_cap             PASS
selftest redirect_private_refused PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: FAIL (3/6)
```

- `row_states` line: `selftest row_states           FAIL (...)` — S103
  observed as `'excerpt'` vs expected `'drifted'`; S103 is the only row whose
  state differs between `got` and `want`.
- Exit code: **1**

## Finding

- The mutation flips `row_states` (PASS → FAIL) and the FAIL detail names S103
  (`('S103', 'excerpt')` got vs `('S103', 'drifted')` want). Both acceptance
  criteria met → **PASS**.
- Collateral arms `exit_code` and `summary` also FAIL under the same mutation —
  expected: zero drifted rows means `run()` returns 0 not 1, and the summary
  counts shift (`excerpt=2 drifted=0` vs `excerpt=1 drifted=1`). This is
  consistent with a real kill, not a selftest artifact; the other three arms
  (`huge_cap`, `redirect_private_refused`, `missing_sources_exit2`) stay PASS,
  confirming the selftest harness itself still functions.
- Mechanism: `classify()` (`tools/mori-source-drift.py:202-208`) returns
  `fresh` on hash match, `excerpt` when the stripped copy is a substring of the
  fetched body, else `drifted`. S103's fixture body does not contain its copy,
  so the fallthrough is the only line that can produce `drifted` for it;
  mutating it to `excerpt` provably kills the drifted classification.

## Tooling

No installs or upgrades performed (pacman transactions paused host-wide;
nothing needed beyond `python3` and `git`, already present).

## Bounds

Read-only against the lane repo (only `git show`); mutated copy under
`/tmp/revc4kill/`; this report is the only file written in the lane.
