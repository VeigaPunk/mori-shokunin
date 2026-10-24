measured 2026-10-23T08:51:41Z

# ConnSiblings — sibling-overlap scan, mori round 35 (capabilities register C1)

## Axes (this seat)
- **adjacency** (primary): name sibling owners of MANIFEST-bound capability registers / calibration counters; state what mori keeps.
- **calibration** (companion): C1 must not duplicate a sibling claim; controls must close the falsification that killed the sibling counter.
- Harm check: no coverage/depth/operability/freshness move claimed; siblings untouched (read-only).

## Scan method (read-only)
- Sibling lanes: `/home/vgpnk/Projects/shokunin/*-shokunin` excluding `mori-shokunin` (20 lanes).
- Grep 1: `capabilities_added` in sibling SCORECARD.md → 0 matches in any sibling SCORECARD (only fleet prompts/reports and kaidoku lesson cites).
- Grep 2: `## Capabilities` in sibling SCORECARD.md → present in most lanes, but all are human-curated registers (capability name → what it can do → evidence → first-working round), none keyed to MANIFEST `capabilities_added`.
- Grep 3: `rounds[` in sibling SCORECARD.md → only citation-style references (kake :2544 `rounds[523]`; kama :1067/:1192; kotodama :732; mado :1446/:1529; souji :13/:14/:15/:18/:21/:103/:104; tameshi :1226; tsukuroi :634/:710). No register keyed by `rounds[i].capabilities_added[j]`.
- Grep 4: counters in sibling `.ufo/waves` reading MANIFEST.json → one: kaidoku's `c2-capability-calibration*.py`.

## Patterns worth reusing (path:line)
- kaidoku counter scaffolding: `kaidoku-shokunin/tools/round-32/c2-capability-calibration-v3.py:1-40` (frozen predicate `P2-match`, docstring), `:manifest_statements` (reads `capabilities_added` of admitted lane closures), `:section_rows` (parses `## Capabilities` table), `FLEET_PIN` (line 18). Reuse: freeze pin + forward/reverse matching + selftest + exit codes.
- kaidoku denial control: `kaidoku-shokunin/.ufo/waves/round-32/controls/c2-negative/receipt.json` and `control.patch` — scores explicit denial prose 4/4 on the unchanged counter; the control that exposed the falsification. Reuse as a mandatory control shape.
- kaidoku register shape: `kaidoku-shokunin/SCORECARD.md:615-624` (`## Capabilities` table, header + rows + entry-rule note). Reuse: header/entry rule; do not reuse its regex-keyed first cell.
- kake register shape: `kake-shokunin/SCORECARD.md:187-192` (same header, evidence pointer + first-working round). Reuse: column order.
- kaidoku plain-measurement recipe: `kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md:63-80` (`awk '/^## /{s=($0 ~ /^## Capabilities/)}` row counts, before/after). Reuse for independent verification.

## Overlaps / contested scope
- No sibling maintains a MANIFEST-bound capabilities register (rows keyed by `rounds[i].capabilities_added[j]`). mori C1 is therefore not a duplicate of any sibling register; it is a new shape on mori's own surface.
- The only sibling calibration counter against MANIFEST capabilities is kaidoku's C2 (`c2-capability-calibration-v3.py`), which compares SCORECARD `## Capabilities` to MANIFEST `capabilities_added`. It was ruled **unprovable** (kaidoku round 32): the lexical counter (first cell matches a frozen regex key, last cell names the round) credited explicit denial prose and word bags (4/4 on `controls/c2-negative`). See `kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md` §R32-C2 and routed defect 4.
- Contested: mori's C1 must not reuse kaidoku's lexical match. mori's counter keys the first cell to the literal MANIFEST key (`rounds[i].capabilities_added[j]`), not a regex, and binds each row to one or two strong evidence paths that changed in that closure and appear in that closure's record. This closes the denial/word-bag loophole (a denial row cannot reuse a real MANIFEST key without also citing a strong artifact the closure names), at the cost of requiring evidence-path resolution (already bounded by P-C1's lower/upper arms).
- No contested ownership: capabilities are lane-local (mori's own closures); no sibling claims mori's capability rows. kaidoku/kake registers are their own lanes' capabilities.

## Lane whose approach was rejected for the same shape (cite spot-check)
- kaidoku-shokunin, round 32, C2 (calibration): `corpus/lessons/round-32-verifier-spotcheck.md` §R32-C2 (plain measurement `caprows=6→9`, `r13/r14/r17/r27=1`) and routed defect 4: "C2v3 lexical counter is falsified: it credits denial and word bags. Any next calibration claim must be frozen with denial, word-bag and off-topic controls scored before data (QUALITY 58). Do not reuse C2v3 as admission evidence." Verdict: calibration **unprovable**; coverage improved. Register repair itself (restoring 3 rows) was truthful and admitted as maintenance, but the *measure* was not.

## Proposed move (one bounded proposal)
- Synthesize: reuse kaidoku's counter scaffolding (freeze pin, forward/reverse matching, selftest, denial control) but replace the regex key pattern with the literal MANIFEST key `rounds[i].capabilities_added[j]` in cell 1, and require cell 4 (evidence) to be one or two strong paths that changed in that closure and appear in that closure's record. This is the synthesis of kaidoku's calibration goal with mori's C1 evidence-path bounds; it improves calibration by making row identity unambiguous while keeping kaidoku's denial/word-bag control shape, and harms no other axis (no tool/knowledge/gate added beyond the register).
- Residual risk carried: the counter does not judge the prose of the "what it can now do" cell (contract §Predicate); non-author review of prose remains required, as in kaidoku's routed defect 4.

## Verification
- No sibling file edited; no sibling gate run; no tool installed.
- Grep commands above (read-only) are the evidence; re-run: `cd /home/vgpnk/Projects/shokunin && for d in *-shokunin; do [ "$d" = "mori-shokunin" ] && continue; grep -c capabilities_added "$d/SCORECARD.md"; done` → all 0.
- Counter unaffected: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py` unchanged by this report.

VERDICT: agree — C1 duplicates no sibling claim.
