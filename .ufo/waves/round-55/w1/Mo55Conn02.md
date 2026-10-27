# Mo55Conn02 — cross-axis pattern scan

## Axes
Freshness (C1) and depth (C2); operationally, provenance/source integrity and independent adjudication are common control surfaces.

## Evidence
- Frozen contract scopes C1 to 78 pointer groups with statuses 69 same/7 moved/2 changed and requires two or more settled output-bound votes per row with zero dissent (`.ufo/waves/round-55/contract.md:13-27`).
- C2 spans 23 claims/9 sources and likewise requires pinned sources, located quotations, two or more settled output-bound votes per claim, and no overclaims (`.ufo/waves/round-55/contract.md:29-41`).
- At-data receipts report both sets fully enumerated but zero votes, so neither axis has adjudication evidence yet (assignment's frozen data summaries; corroboration not independently re-run).

## Proposed bounded move
Use a single, read-only evidence binding index for both ledgers: normalize each row/claim hash to its exact source locator(s), pinned source identity, and settled voter identities/output-bound vote lines. Keep the two verdict vocabularies and independent counter predicates untouched. This cross-axis synthesis makes shared provenance/vote gaps visible once, while preserving separate semantic judgments and the contract's no-dissent requirement.

## Affected axes
Potentially improves freshness and depth evidence completeness without changing scope or predicates. No axis harm identified; this is a reporting/control-layer proposal only, not a verdict or integration.

## Risks
A shared index could create correlated clerical errors or tempt reviewers to treat provenance validity as semantic correctness. Keep separate C1 line/status and C2 entailment checks authoritative; require independent source-level review and no inferred verdict from index completeness.

## Verification
Read-only proposal; no counter, host, production, or ledger execution performed. Before adoption, compare every index locator and pinned source identity against each frozen counter's independently derived records, then run both frozen counters and confirm voter binding and dissent checks remain independent. Unverified.

## Findings
- INFO — Both axes share pinned-source/provenance and voter-binding controls, while semantic criteria remain distinct: `.ufo/waves/round-55/contract.md:13-41`.
- INFO — Data summaries show complete enumeration but no votes; this proposal does not establish either axis: assignment-provided data summary (not re-run).
