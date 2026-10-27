# Mo57Critic25 — C1 calibration

## Verdict: false claim (predicate unmet)

Frozen C1 requires the **current SCORECARD capabilities table** to have rows named `driver-liveness` and `vote-binding`, each with a resolvable round-56 evidence pointer and first-working round 56 (`.ufo/waves/round-57/contract.md:5`). At the inspected current `SCORECARD.md`, the registered capability tables/rows contain neither name (search: `grep -nE 'driver-liveness|vote-binding' SCORECARD.md`; the only occurrence is round-56 claim prose, not a capability row). Thus the round-56 demonstrations do not establish the calibration predicate: capability names/pointers are absent from the required table. The round-56 claim table at `SCORECARD.md:2903-2904` documents successful C1/C2 checks for a driver probe and vote binder, but is not the capabilities table. The existing top-level capabilities table at `SCORECARD.md:597-600` is empty; the later capability registry rows likewise do not contain either requested capability. This is the strongest counterexample to treating round-56 claim evidence as table evidence.

## Demonstration evidence and limits

- Driver-liveness: `SCORECARD.md:2903` records C1 `met` at freeze and landed revisions, citing `.ufo/waves/round-56/evidence/c1-at-landed.txt`; that receipt says `C1=met ... rev=097c342b6c7d71444c0d81c9615197dc87d59c50` (line 1). The live output `.ufo/waves/round-56/evidence/driver-liveness-live.txt:295` identifies schema `mori-driver-liveness-v1`; lines 12, 24, 36 etc. show nonzero `unclosed` values. The output's notes at lines 289-292 explicitly say `in_flight/unclosed` are log-shape facts, not health verdicts.
- Vote binder: `SCORECARD.md:2904` records C2 `met` and cites `.ufo/waves/round-56/evidence/c2-at-landed.txt` (the round-56 counter receipt). This demonstrates a round-56 claim check, not a current capability row.

Impact: calibration (C1) only. The round-56 demonstrations themselves are evidenced; the defect is that their claimed calibration/completeness is not represented by the required current capability rows with first-working round and row-level evidence pointers. No C2 judgment or broader predicate is asserted.

Smallest safe correction: none within this critic assignment; report predicate unmet. Do not infer or add capability rows here. 
