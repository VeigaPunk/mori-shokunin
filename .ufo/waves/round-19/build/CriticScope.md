# C1 Scope Critique

## Counterexample and failure condition

A complete `clean` result from the new bounded content-review gate is not a whole-tree privacy proof. C1 fails if that result is used to claim whole-repository privacy, replace or narrow the prior R1–R9 all-blob scan, expand or narrow the existing allowlist, or reduce the old scan denominator. The new gate only establishes review coverage and dispositions for the exact frozen population it receives; it says nothing about blobs outside that population. The prior scan’s zero metric was allowlist-relative, not evidence that all repository content was reviewed or safe.

## Evidence

- `.ufo/waves/round-19/contract.md:6` — bounded-population scope; unchanged R1–R9 all-blob policy and allowlist; no denominator cuts; final-tip receipt requirements. **Class:** scope boundary.
- `.ufo/waves/round-19/contract.md:10` — exact population membership, per-path review, blob-digest matching, and unresolved/provenance-only failure semantics. **Class:** bounded gate, not whole-tree scan.
- `corpus/lessons/round-18-verifier-spotcheck.md:43-55` — prior policy scan and allowlist-relative metric. **Class:** allowlist-relative measurement.
- `corpus/lessons/round-18-verifier-spotcheck.md:71-76` — residual out-of-metric content/disposition classes and absent final-tip sweep. **Class:** coverage gap.

## Impacted axis

**Adjacency.** Treating the bounded gate as whole-tree proof or shrinking the old scan/allowlist scope would overstate C1 and reopen the privacy/adjacency risk. Missing the required gate is a capability failure, not evidence of a production defect (`contract.md:6`).

## Smallest safe correction

Keep the R1–R9 all-blob scan and exact allowlist unchanged, with no denominator cuts. Add the content-review gate only for every exact path in the frozen population, bound to the committed final-content tip and its blob digests. Describe a clean result only as complete, content-based review/disposition of that population—not whole-tree privacy clearance. Missing, stale, unresolved, or provenance-only reviews must remain non-clean.

No implementation or execution result was available in the local build artifacts; this is the C1 acceptance boundary, not a claim that a delivered implementation violates it.