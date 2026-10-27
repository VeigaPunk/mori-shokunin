# Mo57Reviewer14 — C1 counter attack

## Finding (actionable counterexample)

`count-c1.py:10-12` checks only that the SCORECARD text between `## Capabilities` and `## Saturation` has exactly two pipe-prefixed lines mentioning the capability names, and that each contains the literal substring `.ufo/waves/round-56/` and `| 56 |`. It never resolves either evidence pointer or verifies that first-working is actually round 56. A junk table can therefore satisfy the frozen row-count target without any demonstrations or even existing evidence.

Exact fixture bytes (replace the existing capabilities section with these lines; any other content can be empty):

```text
## Capabilities
| Capability | First working | Evidence |
|---|---|---|
| driver-liveness | 56 | .ufo/waves/round-56/no-such-file |
| vote-binding | 56 | .ufo/waves/round-56/no-such-file |
## Saturation
```

Expected counter output for a commit `R` containing those bytes as `SCORECARD.md`:

```text
C1=met rows=2 evidence=ok rev=R
```
(exit 0). The table contains no resolving evidence and no demonstration; both bogus paths are accepted solely by substring match.

## Evidence / verdict

Frozen predicate in `.ufo/waves/round-57/contract.md` requires two capability rows, resolvable round-56 evidence pointers, and first-working round 56. Counter implementation at `.ufo/waves/round-57/count-c1.py:7-13` instead performs substring checks and does not resolve pointers. Thus C1's counter is forgeable for the exact frozen target; calibration is not independently established by the counter. I did not alter production files or run a fixture commit.

Verification gap: the counterexample's expected output is derived directly from the checked conditions; it was not run against a synthetic commit because the counter hardcodes the lane repository path.
