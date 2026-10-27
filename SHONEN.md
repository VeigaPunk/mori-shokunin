# mori-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:1211` (Round54 hardware-memory-failure table and error patterns), `SKILL.md:1178` (Round53 commit-runway table); `corpus/QUALITY.md:1479-1514` (QUALITY 148-151; added at round 54)
- [~] At least one end-to-end domain task executed and logged in LOG.md — `LOG.md` Round54 (C1 v7.3 recheck; C2 hardware memory-failure kill-path entry); `.ufo/waves/round-54/evidence/c1-at-landed.txt`, `c2-at-landed.txt`
- [~] Instructions executable by an agent without oral context — `python3 tools/mori-pin-check.py --selftest` (125/125), `python3 tools/mori-unlanded-check.py --selftest` (17/17), `python3 -I -B tools/mori-commit-runway.py --selftest` (31/31); round-54 receipts `.ufo/waves/round-54/evidence/selftests/mori-pin-check.txt`, `mori-unlanded-check.txt`, `mori-commit-runway.txt`
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md` Round-54 appended scope notes; `corpus/knowledge/memory-failure-kills-r54.md` Boundaries (no poison injection, sysctl writes or remediation; MCE/EDAC owner remains adjacent)
