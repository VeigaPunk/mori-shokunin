# MoriR16.Quality — round 16 report (revised twice)

Scope: `corpus/QUALITY.md` only (plus this report). Leaf seat; no subagents, no live journalctl queries, no probes, no builds/tests/gates/smoke runs, no commits, no /tmp writes. Only static reads, path checks, web reads of primary systemd docs, and edits to QUALITY.md and this report.

## Behavior

`## Criteria added round 16` at `corpus/QUALITY.md:94-110` (Q37–Q42). No existing criterion edited or renumbered.

| Q | Subject | Lesson id (per MoriR16.Lesson) | Notes |
|---|---|---|---|
| 37 | Dispatcher carries messaging restrictions (no `agent://all`) | `lessons/round-16.md#M1` = C15-1 | precedent `lessons/round-15.md:22` |
| 38 | Probe/download/expected-output writes only to authorized in-lane paths | `#M2` = C15-2 | precedent `lessons/round-15.md:23` |
| 39 | Selftest implementation is not execution permission | `#M3` = C15-3 | precedent `lessons/round-15.md:24` |
| 40 | Active registry sweep (generic) | `#M4` = C15-4 | Read-time stale observation at `SKILL.md:134` is historical; no current-state claim |
| 41 | Green fixture/sibling gate never establishes drift freshness | `lessons/round-16.md#C15-5` (debt, **not** a mistake) | No M5 asserted; QUALITY #10 cross-referenced |
| 42 | Cursor continuity (exact-match anchor only; opaque cursors) | `lessons/round-16.md` ## Gate, S039/S040 | see below |

Revision history:
- Q41 first cited a nonexistent `lessons/round-16.md#M5`. It now cites C15-5 as carried debt.
- Q40 first asserted the `SKILL.md:134` defect was open. It is now generic and cites M4 only. Its current status is whatever the active row shows after correction. Per MoriR16, the active row is corrected; this report does not assert the current state.

Q42 grounding, verified by reading primary docs:
- S039 `sd_journal_seek_cursor` (systemd 262): "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead." A seek fallback is therefore not an anchor observation.
- S040 `sd_journal_test_cursor`: "cursor strings do not uniquely identify an entry" (string comparison not valid; test via the entry).
- S014 `journalctl(1)` `--show-cursor`: "The format of the cursor is private and subject to change."
- Transfer caveat in Q42: S039/S040 describe the libsystemd API. `journalctl --cursor` missing-anchor behavior is not stated in the S014 text read and is not measured, so the criterion does not assume it.

Q42 is a contract, not a measured result. S039/S040 are Registry-assigned ids pending L1 verification against `corpus/SOURCES.md`.

## Checks (static only)

- `tools/mori-census.sh`, `tools/mori-round13/14/15-regressions.py`, `tools/mori-silence-cases.sh`, `.ufo/waves/round-15/{frozen/mori-census.sh,fixtures,expected.json}`, `.ufo/waves/round-14/frozen/mori-census.sh`, `corpus/evidence/baseline-r10-20261015T2231Z.json`: PRESENT. `tools/mori-round16-regressions.py`, `tools/mori-journal-window.py`: ABSENT (round-16 deliverables; expected at read time).
- `corpus/lessons/round-16.md` was present earlier, with ids C15-1…C15-5, M1–M4, and the S039/S040 gate row. MoriR16 reports it was clobbered and is being restored. I have not re-verified the restored content.

## Disclosure

No deviations from the L1 clarification. Pre-clarification actions were static reads and primary-doc fetches only. No live journalctl query, probe, background job, or /tmp write.

## Installs

None.

## Findings for L1

1. Admit or reject Q37–Q42 only after the restored `lessons/round-16.md` is verified for C15-1…C15-5, M1–M4, and S039/S040. Q41 must not cite a nonexistent M5.
2. Q40 is generic. Its admission depends on M4's content in the restored lesson, not on the read-time `SKILL.md:134` state.
3. Q42's libsystemd-to-journalctl transfer gap needs a measured receipt or a stated limit before any claim of journalctl behavior.
