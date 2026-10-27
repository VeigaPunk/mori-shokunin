# Mo57Reviewer13 — C1 round-56 capability calibration review

**Verdict: C1 false/unmet at entering revision `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`.** The round-56 demonstrations and their receipts are real, but the current SCORECARD has no capability-table rows for either capability. This is exactly the frozen contract predicate's required 2 rows; the round-57 counter independently reports `C1=unmet rows=0 evidence=bad` (exit 1) at the entering revision.

## Evidence

- Frozen contract `.ufo/waves/round-57/contract.md:5` requires two SCORECARD capability rows naming `driver-liveness` and `vote-binding`, round-56 evidence pointers resolving, first-working round 56; explicitly records before=0 / after=2.
- `SCORECARD.md:2897-2904` documents the round-56 claims and their counters, not capability-table rows. The capability tables in `SCORECARD.md:2589-2593`, `2616-2621`, `2647-2652`, and `2818-2825` cover rounds 47-53; there is no round-56 capability heading or row. Text search for `driver-liveness`/`vote-binding` finds only the round-56 claim prose, not a capability-table row.
- Round-56 verifier independently identified the same omission: `corpus/lessons/round-56-verifier-spotcheck.md:86` says “Capability row not entered,” noting vote-binding was declared and demonstrated and recommending the driver-liveness row as well.
- Demonstrations/pointers themselves resolve: `corpus/knowledge/driver-liveness-r56.md:1-5` names driver-liveness and its S544 source; `corpus/knowledge/vote-binding-r56.md:1-6` names vote-binding and S545. `.ufo/waves/round-56/evidence/c1-at-landed.txt:1-2` records C1 met at landed revision `097c342b…`; `c2-at-landed.txt:1-2` records C2 met at that same revision. `tally-r55.txt:1-2` records the binder's measured tally. All these files exist at the paths inspected.
- Round-56 lesson `corpus/lessons/round-56.md:56-75` describes the two demonstrations and corrections; lines 80-99 route known limitations but do not supply the missing SCORECARD capability rows.

**Counterexample:** the round-56 claim rows at SCORECARD lines 2903-2904 could be mistaken for capability rows because they describe both tools, but they reside in the claims table and lack the capability-table schema (`Capability | What it can now do | Evidence | First-working round`) and first-working-round cells. Thus real demonstrations/evidence do not satisfy the frozen table-completeness predicate.

No production files were changed. No verification beyond the cited read-only counter invocation and file/pointer inspection was performed.