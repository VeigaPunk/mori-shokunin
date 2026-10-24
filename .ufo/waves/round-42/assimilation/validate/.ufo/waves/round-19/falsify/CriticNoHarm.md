# CriticNoHarm — C1 boundary review

## Blocking counterexample — caller-selected population pin

**Class:** population-scope / denominator integrity. **Impacted axis:** adjacency (C1).

The content gate does not bind the supplied population to the frozen canonical population. The contract requires `P`'s digest to match `--expected-sha256`, but the expected digest is caller-supplied; the frozen oracle contains no canonical population digest. The implementation hashes whatever file `--population` names, compares it only to that argument, accepts its `paths` list, and checks review completeness only against those selected paths. **[INFERENCE]** A caller can therefore substitute a smaller valid population, recompute and pass its digest, provide one valid content-reviewed row per listed blob, and obtain a clean result for a denominator cut. This would not change the old R1–R9 scan, but it defeats C1's “exact frozen population” and “no denominator cuts” guarantee if the C1 result is treated as certification.

**Evidence / anchors:**
- `.ufo/waves/round-19/contract.md:6,10` — exact frozen population / no denominator cuts; the interface compares P to a supplied digest.
- `.ufo/waves/round-19/frozen/expected.json:1-36` — C1 cases and finding codes, but no canonical population digest.
- `tools/mori-content-review.py:213-240,255-265,332-337` — hashes the caller-selected file, compares it to `args.expected_sha256`, accepts its path set, then enforces completeness only for that set.
- `tools/mori-round19-regressions.py:293-319,339-387` — C1 fixtures construct a two-path population and pass its computed digest; the tampered-pin case tests a mismatch, not a replacement population with a newly matching digest.

**Smallest safe correction:** make the gate or its trusted invocation enforce the canonical `content-population.json` digest bound to the frozen revision (not merely a caller-provided digest), and reject any alternate population even when its caller-supplied pin matches. Add a regression requirement for a reduced population with a freshly recomputed pin. Keep the existing R1–R9 policy and allowlist untouched.

## Accepted only under a narrow historical interpretation

I found no evidence that the integrated change altered the original R1–R9 scope or allowlist. The frozen policy defines an all-tracked-blob scan with its stated binary handling and non-author metric exclusion; the retention tool scans the revision tree and applies the existing exact line/class/digest allowlist rules. A read-only diff from the r19 freeze commit to integrated commit `367927c56eb1a00613e1fed65e5c47245fd570b9` returned no changed paths for the frozen R1–R9 policy, `corpus/evidence/retention-allowlist.json`, or `tools/mori-retention-gate.py`.

- `.ufo/waves/round-18/frozen/c1-policy.json:5,27-29` — original all-blob scope, contextual allowlist rule, and recall-floor caveat.
- `tools/mori-retention-gate.py:189-204,239-268,280-300` — whole-tree blob enumeration, exact allowlist matching, must-redact rejection, and non-author-only metric exclusion.
- `.ufo/waves/round-19/frozen/content-population.json:200-205` — the new bounded set explicitly does not replace or shrink the r18 metric.
- `corpus/lessons/round-18-verifier-spotcheck.md:48-55,68-76,171-176,182-188` — the prior zero is allowlist-relative; the r17 routed harm is cured only in the r18 tip's committed bytes; six r16 host-home loci, SW1 content dispositions, short-line-digest guessability, and a final-tip sweep remained distinct residuals; history remains unchanged and operator/kagi-owned.
- `corpus/lessons/round-19.md:19-23` — preserves that narrow r17/tip-only meaning, the six residual loci and digest caveat, and the no-history-rewrite boundary.

Thus “r17 harm cured” is acceptable only as “the identified r17 routed material is absent from the r18 tip's committed bytes”; it is not a claim that the full repository or history is clean. The contract's generic wording at `.ufo/waves/round-19/contract.md:3` should name the r17 routed harm explicitly to avoid that overread. The six residual loci and short-line hashes are not anonymized by omission of source text and must not be described as already cured.

The frozen population has 194 paths; the retained first-wave review snapshot has 26 rows. Missing reviews remain non-clean under `.ufo/waves/round-19/contract.md:6,10`; no complete C1 coverage is claimed here.

## Verification boundary

Static source and retained-artifact review only. No gates, tests, builds, lint, formatting, smokes, or other execution were run. Scope deviation: an early broad search over `.ufo` also traversed `.ufo/interactive-sessions`, and transcript snippets appeared in its tool output. I did not use or copy transcript text into this report and stopped searching that directory once I noticed. This is a boundary breach, not evidence that no exposure occurred.

Report: .ufo/waves/round-19/falsify/CriticNoHarm.md
