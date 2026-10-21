# CriticCalibration — round 21 C2

## Finding

**Acceptance blocker: the supersession plus six cases demonstrates conformance to a chosen rule, but does not establish that C2 learned the outside disagreement.** The cases encode the desired classification in `expected_class` / `expected_pin_allowed` and feed the decisive `required_evidence_lost` / `independent_disposition` booleans to a classifier. They do not bind those inputs or expectations to the actual round-20 disputed observations. Thus an incorrect mapping of the real evidence to those booleans can pass all six cases.

## Counterexample

The non-author closure’s actual disagreement was not a single generic “lost evidence” example. It distinguished:

- `WAVE_UNSETTLED_AGE`: removed markers left the historical wave disposition unproved, so classify the evidence-assurance component as `census-regression` and block the pin; do not claim the wave is still unsettled.
- `WATCHDOG_STALE`: `live-state` is defensible only as log-mtime drift, not daemon health; retain the blind spot and route heartbeat provenance. The independently observed `WATCHDOG_ABSENT` remains.
- Newly aged `w24`: separate `live-state`.

Those are the outcomes in fleet `MANIFEST.json`, `/rounds/405/verification/C1_class_ruling` (entry 405; `.ufo/waves/round-21/contract.md:3`). The round-20 disagreement is documented at `.ufo/waves/round-20/falsify/AdjudicateWaves.md:5-7,29` and `.ufo/waves/round-20/falsify/AdjudicateStale.md:1,5-9,15`; `corpus/lessons/round-20.md:27` calls M6 an open disagreement. `.ufo/waves/round-20/falsify/ReviewQuality.md:24-34` says QUALITY67 writes the disputed live-state choice into the criterion and lets the wave-loss re-pin pass.

Round 21’s six frozen rows do not contain any of those three identities or bind them to their source evidence (`.ufo/waves/round-21/frozen/cases.json:3-50`). Instead, they stipulate two abstract loss cases as regression and four abstract controls as live-state. The contract’s classifier consumes already-decided booleans and applies a one-flag rule (`contract.md:15`); it does not adjudicate whether the actual watchdog token is “required evidence lost” or an ordinary log-mtime change. For example, the same `WATCHDOG_STALE` observation can be made to produce either result by choosing that caller-supplied bit, while every frozen case still passes. The actual closure’s bounded expected distinction is therefore not exercised.

There is some valid protection here: `before-rule.json:3-5` explicitly models Q67 as `evidence_loss_blocks:false` rather than pretending Q67 had executable code, and the new rule is independently exercised against the frozen input table (`contract.md:15,18-25`). This can prove that the evaluator implements the declared policy and that the old modeled permission disagrees on the first two cases. It cannot, by itself, prove the policy’s input classification matches the outside ruling. The named external source is not a substitute oracle: `contract.md:27` explicitly limits S066 to an ApprovalTests decision, not mori policy.

## Impacted axes

- **Calibration (primary):** expected outcomes are the contract’s chosen answers, not a source-bound replay of the outside dispute.
- **Freshness (conditional):** if callers mislabel a disappeared required observation as an ordinary state change, the rule can permit the very baseline acceptance the closure rejected; if a safe ordinary change is mislabeled as evidence loss, it over-blocks. The case table currently cannot detect either mapping error.
- No separate axis impact is established beyond this calibration blocker.

## Smallest safe correction

Add a source-bound, frozen round-20 crosswalk (or two/three named rows in the existing table) for `WAVE_UNSETTLED_AGE`, `WATCHDOG_STALE`, and `w24`, with the relevant closure/evidence pointers, independently adjudicated input bits, expected class, and pin decision. Make the classifier’s case oracle exercise that evidence-to-input mapping, not only the rule after booleans have already been chosen. If the watchdog observation is deliberately outside C2’s classifier scope, state that boundary and do not claim the finite suite learned the full M6 disagreement.

## Evidence limits

Read-only review of the round-21 contract and frozen cases, QUALITY67/69, round-20 M6 review/adjudications, lesson, and fleet closure entry 405. No tests, build, census, pin, or edits to production were run. No tool installs.