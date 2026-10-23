measured 2026-10-23T08:52:14Z
# Round 12 capabilities-register finding

ROW: | rounds[313].capabilities_added[0] | sources registry | Provide a 34-row source registry with a clean census (MANIFEST.json:6211; .ufo/reports/round-12/mori.md:203). | `corpus/SOURCES.md` | 12 |
WHY: corpus/SOURCES.md is the registry itself; the closure report names it as added and records a clean contract census (.ufo/reports/round-12/mori.md:13,25,27).
VERDICT: supported

## Citations
- `MANIFEST.json:6211` records the exact capability string and 34 rows; `MANIFEST.json:6213-6226` identifies the report, closure commit, and lane round.
- `.ufo/reports/round-12/mori.md:13,25,27` names the added registry and its clean contract census. Line 25 reports the initial 33 rows; line 197 records own-work row S034; line 203 records validator output `mori-shokunin ok`, exit 0.
- At closure commit `bf7cdc4783d0748d525fbfe3ba8fb3d285eb929a`, `corpus/SOURCES.md:3-6,7-40` is the registry and contains rows S001-S034. This is the selected strong path.

## Gates and provenance
- Strong-path checks for the selected path: local read confirms `corpus/SOURCES.md` exists at the lane tip; `git ls-tree` and `git show` below confirm it exists at the closure commit; previous-to-closure name-status reports it as added; the path is within the allowed `corpus/` scope and appears whole in the closure report at `.ufo/reports/round-12/mori.md:13,25,27`. The capability string does not name a more specific tools/ or corpus/knowledge/ path.
- `timeout 120s date -u +%FT%TZ` → `2026-10-23T08:52:14Z`.
- `timeout 120s bash -c 'git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json | jq ".rounds[313]"'` → admitted; capability `sources-registry (34 rows; census clean)`; report `.ufo/reports/round-12/mori.md`; lane round 12; commit `mori-shokunin@bf7cdc478`.
- `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-status 20e2255e7b3ebb05a52272f35a996421cab14848 bf7cdc4783d0748d525fbfe3ba8fb3d285eb929a -- corpus/SOURCES.md corpus/evidence/drift-r12-20261019T2204Z-classification.md corpus/evidence/roster-r12-20261019T220912Z-live.log corpus/evidence/roster-r12-20261019T220912Z-mutation.md corpus/knowledge/oom-kill-counter-kernel-only-r12.md corpus/knowledge/roster-truth-r12.md tools/mori-census.sh` → `A corpus/SOURCES.md`; five evidence/knowledge candidates are added and `tools/mori-census.sh` is modified.
- `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree bf7cdc4783d0748d525fbfe3ba8fb3d285eb929a corpus/SOURCES.md corpus/evidence corpus/knowledge tools/mori-census.sh` → the closure tree contains the `corpus/SOURCES.md` blob and the listed evidence, knowledge, and tool paths.
- `timeout 120s bash -c 'git -C /home/vgpnk/Projects/shokunin/mori-shokunin show bf7cdc4783d0748d525fbfe3ba8fb3d285eb929a:corpus/SOURCES.md | nl -ba'` → printed the registry through S034 at line 40.
- `timeout 120s git -C /home/vgpnk/Projects/shokunin diff --exit-code 37b51a243302e8009c7067431e8a47f9a722fd14 -- .ufo/reports/round-12/mori.md` → exit 0, no output; report lines cited above match the fleet revision.

## Touched surfaces, limits, and artifacts
- Written surface: `.ufo/waves/round-35/w1/RowR12.md` only. Read-only sources: fleet `MANIFEST.json`, the round-12 fleet report, and lane `corpus/SOURCES.md` and Git history.
- No product code, manifest, or scorecard changed. No tools were installed or updated.
- The frozen C1 counter was not run. This is a supported verdict for the single requested row, not a full C1 result or a ruling on the other candidates/rows.
- Report artifact: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/w1/RowR12.md`.
