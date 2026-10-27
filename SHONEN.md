# mori-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:1144` (Round52 section: the overcommit-ledger decision rows and the calibration mismatch classes); `SKILL.md:1069-1141` (Round51); `corpus/QUALITY.md:1252-1373`
- [~] At least one end-to-end domain task executed and logged in LOG.md — `LOG.md:2808` (Round 52: overcommit entry with per-row entailment votes, the two pins re-run at the data tip); `LOG.md:2765-2805` (Round 51)
- [~] Instructions executable by an agent without oral context — `python3 tools/mori-pin-check.py --selftest` (125/125); `python3 tools/mori-unlanded-check.py --selftest` (17/17); round-52 receipts `.ufo/waves/round-52/evidence/selftests/mori-pin-check.txt`, `.ufo/waves/round-52/evidence/selftests/mori-unlanded-check.txt`
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md:3-16` unchanged; `corpus/knowledge/overcommit-commit-limit-r52.md:68-75` Boundaries (v7.2 ledger bytes only; no host sysctl value claimed and no threshold proposed; choosing the overcommit mode is the operator's; OS-state triage is tsukuroi's); `corpus/knowledge/memavailable-estimate-r51.md` Boundaries
