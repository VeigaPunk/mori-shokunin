# Mo58Critic25 — considerthese status attack

## Bounded method

Read the frozen round-58 contract and counters, then inspected `tools/mori-pin-check.py` and the considerthese record at the freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d`; compared the round-58 lesson with the round-56 considerthese report and QUALITY criteria. No counter was executed, no production/operator input was edited, and no claim about C1/C2 correctness is made.

## Finding — curation status is not supported as written

The round-58 lesson says suggestions 2 and 3 “remain unimplemented” (`corpus/lessons/round-58.md:21-23`). Suggestion 3's binary status conflicts with the prior considerthese seat: `Mo56ScribeConsiderthese.md:21` classifies it **implemented**, citing QUALITY 136 and round-50 counter re-execution receipts; its finding at lines 166-168 says suggestions 1 and 3 were already landed as QUALITY 138 and 136. QUALITY 136 (`corpus/QUALITY.md:1223-1232`) explicitly names the 2026-10-26 suggestion and says round 50 re-ran its counters at the landed revision. This is evidence of adoption and one concrete execution, not proof that every r47-r49 closure was replayed or that this is a recurring practice. Round 58 should distinguish “criterion/adoption and r50 instance exist” from “all requested replays complete,” rather than label it simply unimplemented.

Suggestion 2 is different: QUALITY 153 (`corpus/QUALITY.md:1522-1541`) adopts the carry-over criterion but its shown-failure arm says every prior flag had `later=0` at revision `8be2717b`; `Mo56ScribeConsiderthese.md:20,53-57` and `corpus/lessons/round-57.md:49` call the carry-over ledger unimplemented/planned. Therefore “criterion landed; operational carry-over remains pending” is the well-supported status. Do not conflate criterion adoption with a functioning ledger.

Suggestion 4 is a weak round pick: the round-56 considerthese report rejected it as adding only a prose habit with no checkable artifact, because per-round lessons already state dispositions (`Mo56ScribeConsiderthese.md:22-27,166-168`). The round-58 paragraph is a useful status note, but one note does not establish the proposed daily/ongoing practice. The smallest safe correction is to call it a one-round status record, not an implemented standing practice; it is optional rather than a substantive new capability.

## Suggestion 1 check — implemented split, bounded exception

At the freeze revision, `tools/mori-pin-check.py:138-150` documents v5's env/stale classes and its v5.1 boundary. The functional tally path classifies no observed tally as `env`, a differing tally as `stale`, and a nonzero exit after the pinned tally as `stale` (code around lines 832-853); the summary reports `env` and `stale`. Selftest arms at lines 1473-1527 exercise setup-error/no-output as env, wrong tally as stale, and timeout cases.

There is one explicit counterexample to an unqualified “implemented” reading of suggestion 1. That suggestion asks for `env` when the command exits with a setup error or missing absolute path (`considerthese/2026-10-26.md:47-50`), while the v5.1 named limit says a tally printed before a crash on a missing host path is still `stale` (`tools/mori-pin-check.py:145-150`). Thus the split exists and is tested, but that setup-failure shape is intentionally classified on the stale side. The smallest safe correction is to preserve the implemented status with this boundary stated; do not claim complete separation for every setup failure.

A historical status conflict reinforces the need for qualification: `corpus/lessons/round-55.md:106` calls the pin-environment split “outstanding,” although the round-51 v5 commit `87e0c374` already contains the env/stale code and cites suggestion 1. The named v5.1 limit could explain the narrower outstanding interpretation, but the record does not say so.

## Impact and correction

- **Counterexample:** round-58's plain “suggestion 3 remains unimplemented” conflicts with the prior explicit adoption/implementation status and QUALITY 136/r50 receipt evidence; suggestion 1 has a documented tally-before-crash boundary.
- **Impacted axes:** considerthese bookkeeping / evidence provenance and claim calibration only. No direct C1 calibration or C2 depth counterexample was tested.
- **Smallest safe correction:** record suggestion 3 as “QUALITY 136 adopted; r50 replay evidenced; full r47-r49 replay coverage not established here.” Keep suggestion 2 as “criterion adopted, operational carry-over pending.” Describe suggestion 4 as this round's status note, not a standing practice. Qualify suggestion 1 with its explicit v5.1 boundary.

No production edits or counter runs.