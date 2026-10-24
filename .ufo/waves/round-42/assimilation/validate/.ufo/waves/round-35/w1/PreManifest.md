measured 2026-10-23T08:52:28Z
# PreManifest — round-35 wave-1 findings (PreManifest seat)

Scope: five capability rows at SCORECARD.md:627-635 (`## Capabilities (round 12 demonstrations)`); contract-field table at :586-592; fleet MANIFEST frozen at 37b51a243302e8009c7067431e8a47f9a722fd14 (read via `git show`, never edited); pointer resolvability at lane commit dd76eb79ef4f6d39c9c26647a56d3fb607308f8f (round-34 verifier spot-check, 2026-10-23). Read-only git only; no tool installs made (tooling directive: none needed).

## Findings by severity

- **F1 (medium, dangling admission-record pointer):** `.ufo/reports/round-12/mori.md` does not exist at dd76eb79 or HEAD, and `git log --oneline -- .ufo/reports/round-12/mori.md` shows no commit ever added it. It is cited by SCORECARD.md:601-602 (round-12 measurement pointer) and by MANIFEST rounds[313].report (mori r12 closure). The r12 capability row itself does not depend on it (row pointer = `corpus/SOURCES.md`, resolves). [evidence: `git cat-file -e dd76eb79:.ufo/reports/round-12/mori.md` → MISSING; `git cat-file -e HEAD:…` → MISSING; `git log --oneline -3 -- <path>` → empty]
- **F2 (low, text delta):** row says "33 opened, tiered, anchored rows" (SCORECARD.md:631) while MANIFEST rounds[313] capabilities_added records "sources-registry (34 rows; census clean)". Explained by the post-review S034 append (LOG.md:708: "Added opened own-work source S034 for the final-census live roster receipt"); the MANIFEST closure (2026-10-19T23:15:19Z) closed after the append. Not a defect in either record; note for the register.

## Per-row verdicts

- VERDICT: source registry (r12) supported — admitted by fleet MANIFEST rounds[313] (admitted true; verdict admitted; capabilities_added "sources-registry (34 rows; census clean)"; verification.reviewer W3ReviewMori (admit with corrections); closed 2026-10-19T23:15:19Z). Row pointer `corpus/SOURCES.md` resolves at dd76eb79. Round-12 verifier spot-check exists and resolves (`corpus/lessons/round-12-verifier-spotcheck.md` at dd76eb79); LOG.md:712 records W3ReviewMori's non-author sample 4/4 (two admits, two rejects).
- VERDICT: live census (r1) supported — first-working round 1; admitting record is the fleet closure MANIFEST rounds[140] (closed 2026-10-15T00:35:46Z; lanes.mori ok; lane_rounds.mori 1; selftest PASS 14/14; note names lane commit 7ca17b1), a record the lane cannot author (non-lane fleet ledger). Lane-side records: SCORECARD.md:25 (move log) and LOG.md:5-30 (round 1 entry). Row pointer resolves at dd76eb79 (`corpus/evidence/roster-r12-20261019T220912Z-live.log`; `corpus/knowledge/observability-census-r1.md`; `tools/mori-census.sh`).
- VERDICT: census self-test (r1) supported — same r1 admission (fleet closure rounds[140] note: selftest PASS 14/14); row pointer resolves at dd76eb79 (`corpus/evidence/roster-r12-20261019T220912Z-selftest.log`).
- VERDICT: silence oracle (r2) supported — round-2 goal-wave admission: SCORECARD.md:122-126 (ADMIT, none harmed) and LOG.md:192 ("Round 2 — goal-wave admission"), with acceptance re-run by the parent (SCORECARD.md:111). Not admitted by a named non-author then: SHONEN all four remain `[ ]`, "no named non-author verifier yet; wave seats are the lane" (SCORECARD.md:128-130). Row pointer resolves at dd76eb79 (`corpus/evidence/roster-r12-20261019T220912Z-oracle.log`; `tools/mori-silence-cases.sh`; `corpus/knowledge/silence-grading-r2.md`).
- VERDICT: drift pin (r10) supported — round-10 goal-wave admission: SCORECARD.md:519-525 (ADMIT) and LOG.md:479 ("Round 10 — goal-wave admission"); parent acceptance 2026-10-15T22:40Z (SCORECARD.md:493). No named non-author verifier then; the r11 capstone audit later found SHONEN 0/4 and held promotion (SCORECARD.md:550-554) and carried named-non-author SHONEN verification to the operator (SCORECARD.md:581-584). Row pointer resolves at dd76eb79 (`corpus/evidence/drift-r12-20261019T2230Z-after-roster.log`; `corpus/evidence/baseline-r10-20261015T2231Z.json`; `corpus/knowledge/drift-pin-r10.md`).

## Register relation (why P-C1 does not count these rows)

Frozen MANIFEST (37b51a2) carries no mori lane round with `capabilities_added` before rounds[313] (lane_round 12); the only pre-12 mori presence is fleet closure rounds[140] (round 1, lanes.mori ok, lane_rounds.mori 1, no capabilities_added key). The r11 contract-field table stands empty (SCORECARD.md:586-592: "— none yet —"; rows enter only through a demonstrating round per AXES.md §Capabilities). The four pre-MANIFEST rows were demonstrated/admitted before the register was keyed to MANIFEST rounds[i].capabilities_added, so P-C1 (18 rows at keyed, admitted mori entries) correctly excludes them.

DRAFT register-note
```
These four rows predate the MANIFEST-keyed register: live census and census self-test first worked round 1, silence oracle round 2, drift pin round 10 — all admitted before MANIFEST carried any mori capabilities_added key (first keyed mori entry is rounds[313], lane_round 12). Their admissions stand in the fleet closure rounds[140] (r1) and goal-wave verdicts (r2/r10, SCORECARD/LOG), not in the register, so P-C1 does not count them; each row's evidence pointer resolves at dd76eb79. They remain documented demonstrated capabilities, not register rows.
```

## Residual risk and verification gaps

- F1: the MANIFEST rounds[313].report field and SCORECARD.md:601-602 cite a report that never existed in the lane tree — any future register tooling that resolves r12 evidence through `report` would dangle. The capability rows themselves do not rely on it.
- Non-author admission at the time: r2/r10 were admitted by goal-wave verdicts with parent acceptance re-runs but no named non-author verifier (SHONEN 0/4; carried to operator, SCORECARD.md:581-584); r1's admitting record is fleet-level (non-lane) but names no verifier; only r12 has a named reviewer (W3ReviewMori) in the MANIFEST verification field.
- I did not run count-c1.py (frozen counter, keyed to the MANIFEST; my scope is the rows, not the count). All pointer checks were `git cat-file -e` at dd76eb79 / HEAD (read-only).
