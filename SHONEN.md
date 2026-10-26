# mori-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:1069-1141` (Round51 section: runway decision row, pin mismatch classes); `SKILL.md:1018-1067` (Round50); `corpus/QUALITY.md:1252-1352`
- [~] At least one end-to-end domain task executed and logged in LOG.md — `LOG.md:2765-2802` (Round 51: MemAvailable entry with per-row entailment votes, hermetic pin re-execution); `LOG.md:2732-2763` (Round 50)
- [~] Instructions executable by an agent without oral context — `python3 tools/mori-pin-check.py --selftest` (125/125); `python3 tools/mori-unlanded-check.py --selftest` (17/17); receipts `.ufo/waves/round-51/evidence/selftests/mori-pin-check.txt`, `.ufo/waves/round-51/evidence/selftests/mori-unlanded-check.txt` (round-51 C1: pin-check v5/v5.1 add eleven arms)
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md:3-16` unchanged; `corpus/knowledge/quota-observability-r48.md` Boundaries (read-only, no quota command run); `.ufo/waves/round-48/w2/R48ConnSiblings.md` (no contested scope); `corpus/knowledge/oom-memcg-stat-r50.md` Boundaries (cgroup limit configuration is tsukuroi's); `corpus/knowledge/memavailable-estimate-r51.md` Boundaries (OS state is tsukuroi's to diagnose, the operator's to change; the hyaku gates are the orchestrator's)
