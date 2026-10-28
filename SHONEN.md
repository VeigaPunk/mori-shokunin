# mori-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:1211` (Round54 hardware-memory-failure table and error patterns), `SKILL.md:1178` (Round53 commit-runway table); `corpus/QUALITY.md:1479-1514` (QUALITY 148-151; added at round 54); QUALITY 154 (frozen claim output/predicate identity, added round 58)
- [~] At least one end-to-end domain task executed and logged in LOG.md — `LOG.md` Round58 (C1 active-register counter + C2 driver-events depth entry, both unverified under frozen targets, honestly reported); `.ufo/waves/round-58/evidence/` receipts; `LOG.md` Round56 (C1 FR5 driver-liveness probe; C2 dual-shape vote binder)
- [~] Instructions executable by an agent without oral context — `python3 tools/mori-register-check.py --selftest` (12/12), `python3 tools/mori-settlement-scan.py --selftest` (10/10), `python3 tools/mori-vote-bind.py --selftest` (16/16), `python3 tools/mori-pin-check.py --selftest` (125/125); round-59 receipts `.ufo/waves/round-59/evidence/selftests.txt`
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `corpus/knowledge/wave-settlement-artifacts-r59.md` Limits (artifact shape facts only, no settlement semantics; sibling settlement collection stays kumitate's, S549 held rejected); `corpus/knowledge/driver-liveness-r56.md` Boundaries (log-shape facts only)
