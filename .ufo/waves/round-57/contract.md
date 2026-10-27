# mori round 57 — working contract (MoriR57)

Entering tip: `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`. Scores: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. Claims: C1 calibration (capability-table completeness for the two capabilities demonstrated in round 56); C2 depth (source-grounded interpretation of the round-56 driver-liveness `unclosed` field). Freeze this contract and counters before wave data; any failure is reported honestly. C1 and C2 are separable.

C1 predicate: the current SCORECARD capabilities table has two rows naming `driver-liveness` and `vote-binding`, each with a resolvable round-56 evidence pointer and first-working round 56. Before: 0 matching rows; after: 2 matching rows. Counter: `python3 .ufo/waves/round-57/count-c1.py R`.

C2 predicate: `corpus/knowledge/watchdog-unclosed-r57.md` exists, opens with `source:`, `verified-at:`, `recheck:`, cites a newly opened source row, contains eight claim rows each with a located quote in the source copy, and states that `unclosed` is a pairing count rather than a present-running count. Before: entry absent; after: eight located claims. Counter: `python3 .ufo/waves/round-57/count-c2.py R`.

No axis score delta asserted. Lowest owned axis coverage is observed but not claimed this round; calibration is lowest non-retired at score 5. Frontier step and census remain required. Vote output is not itself independent verification. This is a working contract and must be frozen with the counters before dispatch.