# mori-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:1178` (Round53 section: the commit-runway decision table by mode, its error patterns, the release recheck rule and the registry row); `SKILL.md:1144` (Round52); `corpus/QUALITY.md:1381-1477` (criteria 144-147)
- [~] At least one end-to-end domain task executed and logged in LOG.md — `LOG.md:2841` (Round 53: the 46 v7.2-pinned claim rows re-read at v7.3 with two-voter RECHECK dispositions; the commit-runway read run on this host, `COMMIT_HEURISTIC`, limit recomputed exactly); `LOG.md:2808` (Round 52)
- [~] Instructions executable by an agent without oral context — `python3 tools/mori-pin-check.py --selftest` (125/125); `python3 tools/mori-unlanded-check.py --selftest` (17/17); round-53 receipts `.ufo/waves/round-53/evidence/selftests/mori-pin-check.txt`, `.ufo/waves/round-53/evidence/selftests/mori-unlanded-check.txt`, `.ufo/waves/round-53/evidence/selftests/mori-commit-runway.txt`
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md:402` (round-53 appended scope notes: the commit-ledger runway read as Core, the v7.3 recheck as freshness work, no ownership change); `corpus/knowledge/commit-runway-read-r53.md:53` Boundaries (choosing a mode, ratio or reserve is the operator's; OS-state triage is tsukuroi's); `corpus/knowledge/kernel-v7.3-recheck-r53.md:107` Boundaries
