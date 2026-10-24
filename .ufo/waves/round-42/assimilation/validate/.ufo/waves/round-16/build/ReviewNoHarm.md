# ReviewNoHarm — mori round-16 C1 window (no-harm review)

Seat: `MoriR16.ReviewNoHarm` (reviewer, leaf). Read-only except this report.
Target: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Entering HEAD: `b83edc6ee3db6822382ab673d7e6e984e420f22f`.

## Read time and in-flight state (explicit)

Changes were landing while this review ran. Snapshot times are UTC.

- `08:49:24Z`: `M LOG.md`, `M SCORECARD.md`, `?? .ufo/waves/round-16/`.
- `08:50:09Z`: `M PROVINCE.md`, `M corpus/SOURCES.md` added. Untracked round-16 files now include `build/FrontierIndex.md`, `build/ReviewCapture.md`, `build/swarm-registry.json`, `fixtures/KernelUser.json`, `frozen/entering-capability.json`, `frozen/round15-spec.json`, `sources-before.json`, `wave1-assignments.json`, `wave1-dispatch.json`, `wave1-record.json`, `wave1-spec.json`, `wave1-task-response.json`.
- Not present at read time: `tools/mori-journal-window.py`, `tools/mori-round16-regressions.py`, `tools/mori-round16-context-check.py`, `capture-recipe.json`, and most `fixtures/*.json`. Nothing about the new tools was evaluated, so no conclusion below covers them.

No tests, builds, census runs, or harness runs were executed. No tools were installed or updated.

## Verified no-harm facts

1. **Census unchanged.** `tools/mori-census.sh` has a SHA-256 digest (prefix `f1f8d1b62bb617bb`) equal to its HEAD blob. It is not in `git status`. A repo-wide search finds no reference to `mori-journal-window` or `MORI_JOURNAL_WINDOW` in the census, so the window cannot reach census alarms.
2. **Old gates untouched.** `tools/mori-round13-regressions.py`, `tools/mori-round14-regressions.py`, `tools/mori-round15-regressions.py`, and `tools/mori-silence-cases.sh` each match their HEAD digest and are not modified.
3. **Drift pin not re-pinned.** `corpus/evidence/baseline-r10-20261015T2231Z.json` and the r10 pin logs match HEAD. No spec item writes to or re-pins a drift baseline.
4. **Write scope.** The spec has 64 uniquely named items. None owns `tools/mori-census.sh`, `tools/mori-round1[345]-regressions.py`, or `tools/mori-silence-cases.sh`. Scribes write only their own single file: `corpus/knowledge/journal-cursor-window-r16.md` (Knowledge), `SKILL.md` (SkillRegistry), `corpus/SOURCES.md` (Registry), `corpus/QUALITY.md` (Quality), `corpus/lessons/round-16.md` (Lesson), `corpus/README.md` (FrontierIndex), `PROVINCE.md` (Province). ClaimRubric writes only its report. Scouts, connectors, reviewers, and critics write only reports.
5. **Seat accounting.** Role mix is 20 executor, 8 scribe, 10 scout, 6 connector, 10 reviewer, 8 critic, 2 sentinel, totalling 64. This matches LOG.md's stated mix. `swarm-registry.json` has 64 members whose names equal the spec's item names. `wave1-dispatch.json` counts are `spawn: 64, resume: 0`.
6. **Broadcast rule present.** The dispatched `taskCall.context` contains "Never agent://all" and the exact-seat-id rule.
7. **Scores held.** The new SCORECARD and LOG sections claim no score increase. Coverage stays 6 and operability stays 7, consistent with the round-15 entries (SCORECARD lines 870–871 and 913).
8. **Entering source census.** `.ufo/waves/round-16/sources-before.json` has exit 0. Its stdout is exactly two W04 lines (S035, S037 duplicate URLs) plus one `ok` line, matching LOG.md. I read the record and did not re-run the census.
9. **Diffs in flight are additive where it matters.** `LOG.md` (+32) and `SCORECARD.md` (+29) are append-only. `corpus/SOURCES.md` is +5 with 0 deletions, so no immutable cell changed. `PROVINCE.md` is +7/-2 (see finding F4).

## Findings (by severity)

- **F1 (medium, evidence gap; no regression asserted).** The no-harm claim for alarms and scope is currently vacuous at code level. The only checks that can pass now are hash equality and absence of references. Alarm and scope non-regression must rest on the post-build census selftest and harness runs that L1 executes once after all seats settle. This review asserts no alarm or scope regression.
- **F2 (low, design).** The production CLI accepts `--journalctl PATH`, which can point at any executable. The spec's `OK` finding therefore depends on the binary given, the same trust model the census already uses through `MORI_JOURNALCTL_BIN`. Recommend that the `OK` output and the report state that it is not census evidence. Nothing in the census consumes it today.
- **F3 (low, wording).** LOG.md says "Entering tree was clean; no inherited round-16 files were found." That holds for tracked content: HEAD committed at `05:42:41-03:00`, and all round-16 artifacts are dated `05:47`–`05:48`. The untracked files are planner output created after entry. Suggest saying "tracked tree clean; round-16 untracked artifacts created after HEAD" so the entering claim is not read as "no untracked files existed."
- **F4 (low, process).** `PROVINCE.md` edits two existing lines in place rather than appending: the "Owns (read-only probes)" paragraph, and the FR11 frontier bullet, which is rewritten from "[UNKNOWN] behavior after cursor rotation/vacuum and ordering across boots" to a narrower remainder list. The new text keeps the rotation/vacuum and cross-boot unknowns, so no unknown is dropped. The scope narrowing is the spec's intent, but L1 should confirm the in-place edit is accepted.
- **F5 (info, carried citation debt).** The `SOURCES.md` correction records that re-derived S014/S015 numeric anchors do not reproduce the pinned line numbers (e.g. the rendered `--after-cursor=` heading near display line 193, not 187–190). It is correctly recorded as append-only and not edited. It remains unresolved and should be tracked as a source-numbering item, not treated as closed.

## Residual risk and verification gaps

- Nothing about `tools/mori-journal-window.py`, `tools/mori-round16-regressions.py`, or the fixture packs was evaluated (not yet present at read time).
- The new `KernelUser.json` fixture and the `frozen/` files were listed, not read. Fixture ids and predicate correctness belong to ReviewFixtures and ReviewCounts.
- The LOG's claimed live-measurement and source openings (S014/S015, systemd 262 documentation) were not re-checked by this seat.

## Verdict (no-harm lane)

No harm is observed in the current read-time tree. Census and old gates are byte-identical to HEAD, the drift pin is untouched, and no spec item writes to protected paths. The remaining items are documentation and wording issues (F3, F4), a design caveat (F2), and carried citation debt (F5). No alarm or scope regression is asserted. Re-verify F1 once the window tool and harness exist.
