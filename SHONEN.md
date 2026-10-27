# mori-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:1211` (Round54 hardware-memory-failure table and error patterns), `SKILL.md:1178` (Round53 commit-runway table); `corpus/QUALITY.md:1479-1514` (QUALITY 148-151; added at round 54)
- [~] At least one end-to-end domain task executed and logged in LOG.md — `LOG.md` Round56 (C1 FR5 driver-liveness probe; C2 dual-shape vote binder re-binding the round-55 tally); `.ufo/waves/round-56/evidence/c1-at-freeze.txt`, `c2-at-freeze.txt`, `driver-liveness-live.txt`
- [~] Instructions executable by an agent without oral context — `python3 tools/mori-driver-liveness.py --selftest` (13/13), `python3 tools/mori-vote-bind.py --selftest` (16/16), `python3 tools/mori-pin-check.py --selftest` (125/125); round-56 receipts `.ufo/waves/round-56/evidence/selftest-vote-bind.txt`, `.ufo/waves/round-56/evidence/controls.txt`
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `corpus/knowledge/driver-liveness-r56.md` Boundaries (log-shape facts only, no health verdict, state values never read); `corpus/knowledge/vote-binding-r56.md` Limits (binding proves carriage, not authorship); kumitate settlement semantics untouched (wave connector check)
