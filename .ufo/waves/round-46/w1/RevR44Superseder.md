# RevR44Superseder — r44 superseding registry row review

## Counterexample

The superseding row says “v2 scrubs GIT_* in child_env,” but its self-test cell records a tally for `tools/mori-gate-registry.py --selftest`. A passing tally verifies the auditor's self-test, not that the changed write-scope behavior was exercised. The digest and 743-line pin identify the auditor bytes the row describes; they do not by themselves demonstrate the subprocess environment behavior.

## Evidence

- `SKILL.md:194` states that the prior row remains the verdict-map authority and that the new row supersedes only its write-scope cell.
- `.ufo/waves/round-44/evidence/freeze-r44.txt:9` records the earlier auditor digest, distinct from the current row's pin.
- `.ufo/waves/round-46/w1/ScoutDigests.md:19` confirms the new digest matches the current committed auditor bytes. Its lines 51–54 explicitly say the tally was not rerun by that seat.

This establishes a provenance gap, not that the write-scope claim is false.

## Impacted axes

Factual accuracy, scope, provenance. The verdict-map scope is explicitly retained from the original row; the weakness is that the cited self-test tally is not behavior-specific evidence for the changed write-scope claim, and the row does not itself bridge the frozen r44 implementation to the changed implementation.

## Smallest safe correction

State the revision/date at which the “v2 scrubs GIT_*” behavior was inspected or tested and cite a behavior-specific receipt for that claim. Keep the existing verdict-map authority unchanged.

No tools installed or updated.
