# HomeSix — content-based falsification

## Findings

No actionable finding in the six assigned loci.

## Evidence and disposition

Five loci retain the mandatory instruction to consult the shared rules file before tool installation or updates, along with the surrounding tool-policy/reporting conditions. The user-home reference is home-relative in each current line:

- `.ufo/waves/round-16/frozen/round15-spec.json:3`
- `.ufo/waves/round-16/wave1-context-corrected-not-dispatched.json:3`
- `.ufo/waves/round-16/wave1-dispatch.json:421`
- `.ufo/waves/round-16/wave1-spec.json:3`
- `.ufo/waves/round-16/wave2-spec.json:3`

The sixth locus, `.ufo/waves/round-16/build/ReviewCounts.md:11`, retains the user-local executable location for the disclosed read and states that the command resolved there; it also preserves that the census uses its configurable executable-name override/default. Its user-home location is home-relative. These contents support the narrowly stated instruction/tool facts in `corpus/lessons/round-19.md:81-102` without needing an account-qualified home prefix.

## Residual risk

This conclusion is limited to the six named retained lines and the round-19 lesson; it is not whole-tree privacy clearance, does not establish anything about unreviewed content, and does not cure historical exposure. No source private values or short-line digests are reproduced.

## Verification gaps

Static content review only. No checks, tests, builds, or live queries were run, as required.