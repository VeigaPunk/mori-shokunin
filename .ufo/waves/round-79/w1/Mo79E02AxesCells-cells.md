# C2 candidate cells — no SCORECARD edit

Axes: coverage, operability, depth, freshness, calibration, adjacency. Proposed moves update closure attribution only; scores and Evidence pointers are outside this change.

New clauses are prepended to the complete current cell, retaining even the displaced leading clause. Every existing byte after the original first semicolon is therefore retained. Adjacency is unchanged; `unchanged` is an annotation below, not replacement cell text.

| axis | current cell | proposed cell |
|---|---|---|
| coverage | round 47 (improved, score held); round 26 (improved, score held) before the round-50 correction | round 56 (improved, score held); round 47 (improved, score held); round 26 (improved, score held) before the round-50 correction |
| operability | round 51 (improved, score held); round 47 (improved, score held); round 31 (improved, score held) before the round-50 correction; round-37 C2 re-attributed here (score held, 7) | round 78 (improved, score held); round 51 (improved, score held); round 47 (improved, score held); round 31 (improved, score held) before the round-50 correction; round-37 C2 re-attributed here (score held, 7) |
| depth | round 51 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 31 (improved, score held) before the round-50 correction | round 76 (improved, score held); round 51 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 31 (improved, score held) before the round-50 correction |
| freshness | round 28 (improved, score held); round-37 C2 is re-attributed to operability (round-38 axes-cell correction below) and round 38 claims no freshness move | round 78 (improved, score held); round 28 (improved, score held); round-37 C2 is re-attributed to operability (round-38 axes-cell correction below) and round 38 claims no freshness move |
| calibration | round 50 (improved, score held); round 49 (improved, score held); round 25 (improved, score held) before the round-50 correction; round-37 claim C1 closed the r36 measurement-discrimination defect and states no new number | round 78 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 25 (improved, score held) before the round-50 correction; round-37 claim C1 closed the r36 measurement-discrimination defect and states no new number |
| adjacency | round 19 (improved, score held) | round 19 (improved, score held) |

Adjacency: **unchanged**.

## Draft paragraph for insertion after the round-50 correction

Round-79 correction (C2, calibration): at entering revision `84c6cbc3b47c536a504aaee329c77897d389935e`, 5 of 6 Last change cells disagreed with the latest admitted mori closures through round 78 in fleet `MANIFEST.json` at `37c313715318eea4a59d30ffae5f77c28301ec72`; adjacency alone was already right (round 19, improved). Coverage, operability, depth, freshness and calibration now lead with rounds 56, 78, 76, 78 and 78 respectively (all improved), retaining the full older cell text after a `;`; scores and Evidence pointers are unchanged. "Last change" here means the latest admitted closure grading the axis improved or harmed, not the latest score move.
