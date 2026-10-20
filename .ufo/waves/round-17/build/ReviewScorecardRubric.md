# Round 17 scorecard rubric review

## Recommendation

Keep the scalar scores at **coverage 6 / operability 7**. Record C1 under coverage and C2 under operability as separate claims. R15 and R16 consistently distinguish an improved axis verdict from an increase in its active score: r15 reports coverage improved at 6 and operability unchanged at 7 (SCORECARD.md:868-875); r16 likewise reports coverage improved at 6 and operability unchanged at 7 (SCORECARD.md:977-984). The active starting pair for both rounds is coverage 6 / operability 7 (SCORECARD.md:817-820; 913-920). Neither r17 claim, on its own, warrants adding a scalar point.

The following are **proposed, conditional rows**, not a claim that r17 has passed acceptance. The inspected contract declares C1 and C2 and their intended tests, but no r17 before/after run result was included in the scorecard material reviewed. [INFERENCE] Do not publish either as a measured improvement until the corresponding acceptance evidence exists.

## Proposed axis verdict rows

| Axis | Proposed verdict | Active score | Evidence / limitation |
|---|---|---:|---|
| coverage | **improved, conditional on C1 acceptance** | **6 held** | The new, standalone read-only seat terminal-status capability is a coverage acquisition, not a count of newly discovered seat deaths. Require the same synthetic fixture cases and gate against entering and delivered tool bytes, with per-case manifest and input digests; the absent entering tool should be reported as `capability_absent`, not as historical production failures. Confirm the delivered output is restricted to the specified fields and the tool never edits, resumes, or reroutes. Contract: `.ufo/waves/round-17/contract.md:9-15,24-67,69-78`. The exact scope remains last-observed state in a bounded tail; dead counts are seats, not incidents; name prefixes do not authenticate lane membership. Do not claim whole-transcript, all-session, or future-finality coverage. |
| operability | **improved, conditional on C2 acceptance** | **7 held** | C2 is the separate census operability claim. Require the same jj-colocated regression gate against the entering census and delivered census, with the promised branch-resolution and finding cases passing, and no changes to A/B/C grading semantics. Use the lane branch ref for the specified row-6 and row-9 probes; assert `HEAD_BRANCH_MISMATCH` only under the declared non-ancestor predicate and `LANE_AUTHOR_MISMATCH` only for the declared post-launch lane-committer/other-author condition. A passing test count alone is insufficient without the case-level assertions and pre/post evidence. Contract: `.ufo/waves/round-17/contract.md:16-22,80-94`. |

If the acceptance runs have not yet been made or their manifests do not show these criteria, use **pending/unverified** rather than `improved`; retain the scores regardless. C1's coverage result must not be credited to operability, and C2's census result must not be credited to coverage: the claims are explicitly causally separable (`contract.md:22`).

## Proposed C1 capability-table row

Add this row only once C1 is accepted; populate its evidence cell with the actual retained artifacts, not a guessed path:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| bounded seat terminal-status inventory | Read a bounded tail of each selected `*.jsonl` seat file and classify the last parseable `message` record as completed, dead-rate-limit, dead-quota, dead-other-error, aborted, incomplete, or unavailable; tally by seat prefix and provider/model; emit only the allowlisted metadata. Detection/report only—no edit, resume, or reroute. | Accepted C1 before/after `run-manifest.json` files and the delivered `tools/mori-seat-terminal.py`; add a live bounded-observation receipt only if one was actually taken and its scope is stated. The contract specifies the gate manifest contents, but not an accepted evidence-directory pathname (`contract.md:24-78`). | 17, conditional on acceptance |

Keep the limitations adjacent to the capability wording: the last observed terminal error is not proof that a session will never resume; totals count seats, not incidents; prefixes are naming conventions, not authenticated lane membership (`contract.md:65-67`). Also preserve the bounded-tail and unreadable/no-message behavior as unavailable rather than treating it as zero or complete coverage (`contract.md:31-50`).

## What could justify a scalar change

The scorecard's r15/r16 precedent expressly holds scores despite finite, demonstrated capability gains (SCORECARD.md:834, 868-875, 913-920, 977-984). Accordingly, **no point change is recommended for this wave**. A future score change would require an explicit, prospective scoring threshold for that axis—none is stated in the reviewed r15/r16 sections—plus evidence that meets the threshold at a scope broader than merely adding a tool or passing its targeted fixtures. For C1 that would require a defined measure of coverage and evidence bounded to what the read-only source can actually observe; for C2 it would require a defined operability threshold and complete before/after case evidence. A green selftest, case-count increase, capability addition, or same-wave assertion by itself is not a scalar rubric.

## Verification boundary

Reviewed the r15/r16 scorecard sections and the round-17 contract/context. No selftest, regression gate, census, transcript scan, or live journal query was run; therefore there are no command exit codes or runtime observations to report. No URL was consulted. The recommendations above are scorecard guidance, not acceptance, admission, or a finding that either implementation is complete.