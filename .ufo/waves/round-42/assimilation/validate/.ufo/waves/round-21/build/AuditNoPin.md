# Round 21 audit: no census, no pin, blocker separation

## Finding closed in candidate source — blocker was counted as invalid

The initial candidate snapshot had a concrete counterexample: a structurally valid `state: unresolved`, `independent_disposition: null` row called `add_issue()`, which unconditionally added the ID to `invalid_ids`; the output therefore categorized the expected blocker as invalid accounting too. The contract permits that unresolved state, expects it to block pinning with rc 1, and calls a complete unresolved accounting an observability improvement (`.ufo/waves/round-21/contract.md:14`).

The executor has corrected the source. `add_issue()` now tracks invalidity separately (`ImplLoss/tools/mori-evidence-loss.py:497-509`); the unresolved branch records the blocker with `invalid=False` (`:541-545`), and the pin gate independently blocks on `unresolved` (`:612-619`). Counts and ID arrays are separate in the output (`:620-634`). The selftest now asserts the valid unresolved fixture returns rc 1, `omitted=0`, `retained=1`, `unresolved=1`, `disposed=0`, `invalid=0`, and `pin_allowed=false` (`:867-879`). The source-level issue is closed; the selftest was not executed.

## No finding: audit avoids census and baseline writes

The audit flow reaches `GitEvidence`; its subprocess helper invokes explicit `git` commands only (`ImplLoss/tools/mori-evidence-loss.py:229-255,477-511`). I found no census invocation in the audit path. The write helper and filesystem writes are used for isolated selftest fixtures, not by `audit()` (`:720-722,763-781,477-638`). The audit exposes `pin_allowed` separately and includes no census health result (`:620-634`). This is source inspection, not a runtime side-effect test.

## Residual risks and verification gaps

- No tests, census, pin, or production writes were run. Runtime behavior and absence of side effects were not independently exercised.
- No LSP device was exposed in this session, so references/definition/diagnostics were unavailable; source inspection was the fallback. No tools were installed.
