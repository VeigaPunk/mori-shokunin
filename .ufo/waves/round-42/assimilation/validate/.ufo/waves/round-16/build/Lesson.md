# MoriR16.Lesson — round-16 lesson report

Scope: owned file `corpus/lessons/round-16.md` (restored in full after a reported overwrite, see M20) and this report. No runs, builds, tests, gates, selftests, commits, or installs by this seat. No `/tmp` writes by this seat. No `agent://all` messages.

## Behavior

`corpus/lessons/round-16.md` is the round-16 lesson for C1 coverage: a bounded, MESSAGE-free, same-boot new-since-anchor journal window. It is pre-measurement: candidates are admitted only as pending measurement and outside closure.

## Restoration

Another seat (`MoriR16.ReviewCounts`) overwrote the owned lesson with an 11-byte placeholder (observed as `placeholder`, hash `#7739`). This seat restored the full file from its authored content, carrying forward every correction, source row, gate candidate, and routed item. The restored text is this seat's reconstruction; the owner should confirm it against its own source copy. Recorded as M20.

## Corrections to round-15 (append-only)

- C15-1 broadcast context: L1 omission, seat broadcast stays a violation.
- C15-2 `/tmp` probe (`HarnessBuild.md:256`) plus `/tmp` downloads: r15 provenance, disclosed debt.
- C15-3 false selftest-permission rationale (`HarnessBuild.md:301–307`): implementation is not permission to execute.
- C15-4 `SKILL.md` hidden-flag line: **corrected in the working tree** (`SKILL.md:168` now says the r15 CLI has no hidden flags); not yet committed. Commit owned by `mori`.
- C15-5 drift pin: carried debt, not a mistake; no re-pin.

## Mistakes recorded (M1–M26; M5 intentionally not asserted, M6 unused)

- M1–M4: the C15 items above.
- M7–M10, M12–M19, M21–M25: deviations self-disclosed or reported by peers (BootContinuity `/tmp` writes and `bg_2667`; SiblingScope live probes; BudgetPricing live loops and `/tmp` scratch; HostSafety background wait `bg_2692`; ReviewAnchor version/man reads; SourceChain `/run/user/1000` downloads; PackProcessSignal `/tmp/_pack_ps.txt`; own-fixture parses; AttackBound host reads; Registry `bg_2643`; AttackOutputLeak live `journalctl --user -n0`; AttackMixedBoot in-lane scratch; AttackPermission-reported `/tmp` writes; ReviewCorpus `/tmp` directory and `bg_2754`; Province `/tmp/x`; AttackVacuity `bg_2749`; AttackPreservation host reads).
- M11: dispatch-hint unit-failure id, caught by pack seats before fixtures; census bytes are authority.
- M20: overwrite of this lesson file by another seat (restored here).
- M26: static eval arithmetic (disclosed, not a deviation).

No runtime prevention exists for any of these. An admonition or static context instruction is not counted as prevention; the r16 instruction repair is untested and was itself violated in this round.

Per L1's clarification: static reads, version/help/man lookups, and static parses of a seat's own fixture are allowed and are not counted as runtime violations. Real outside-lane writes, live or synthetic probes, and background jobs are deviations regardless of intent. All deviations are excluded from delivered verification.

## Source openings

Opened by this seat (2026-10-20, systemd 262 pages): S014 journalctl (`--cursor=`, `--after-cursor=`, `--show-cursor`, `--no-tail`, `--boot`) and S040 `sd_journal_test_cursor` (alias statement "the same entry might be referred to by multiple different cursor strings", 12 words).

Peer-reported, not re-verified here: S039 `sd_journal_seek_cursor` next-closest quote (23 words, corrected by Knowledge); S015 field quotes; further S014 quotes.

Version gap: doc pages are systemd 262; host `journalctl` is 261.2-1. No host semantics are claimed.

## Source rows and used-by (Registry final, reported)

- S039 (`sd_journal_seek_cursor`) and S040 (`sd_journal_test_cursor`): both `mined`, opened 2026-10-20, used-by `corpus/knowledge/journal-cursor-window-r16.md`. Both rows stand.
- S014 and S015 used-by each gained the same note.
- S013, S035, S037 used-by appends reverted; the note does not cite them (static check by this seat).
- No immutable cell changed. Registry-reported; L1 verifies against `corpus/SOURCES.md`.
- The note's line 111 is stale (describes a combined S039 row); routed to `MoriR16.Knowledge`.

## Gate (candidates; none admitted by this lesson)

- Exact-anchor first-record drop plus same-boot scalar unique later records: candidate, pending measurement.
- Same-boot as the anchor's `_BOOT_ID` (historical boot permitted): candidate, pending measurement.
- Exact-byte comparison with no alias resolution: admitted only as conservative, with documented false-unavailable (S040).
- Byte mismatch as proof of vacuum or deletion: rejected.
- Byte-unique cursors as dedup or completeness: rejected.
- `--after-cursor` without anchor proof: rejected.
- Zero records as "no event": rejected.
- MESSAGE parsing or malformed-JSON salvage: rejected.
- Foreign-boot or non-scalar identity promoted to positive: rejected.
- Automatic anchor advance or cursor write: rejected.
- FR11 advanced by fixtures: rejected.
- Drift re-pin: rejected.
- Census cutover: rejected.
- Pre-spawn current-boot gate (SiblingScope §3, retracted in its §8): rejected.
- Any result from the deviating live, `/tmp`, or background probes: rejected.
- Source rows S039/S040: candidate, pending L1 verification.

## Touched surfaces

- `corpus/lessons/round-16.md` (owned file; restored after overwrite).
- `.ufo/waves/round-16/build/Lesson.md` (this report).
- Message to `agent://MoriR16.Quality` (exact id): mapping M1–M4 to C15-1 through C15-4; no M5 asserted.

## Out of scope (routed)

- `SKILL.md` commit for the C15-4 correction: `mori`.
- `SCORECARD.md:781` "fixture" label and QUALITY #36 citation: `mori` and `MoriR16.Quality`.
- `corpus/SOURCES.md` verification and the knowledge note's stale line 111: L1 and `MoriR16.Knowledge`.
- Production tool, harness, fixture packs, and all measurement: other seats and L1, once after integration.

## Verification

None run by this seat. For the main agent after all seats settle: verify S039/S040 rows and the used-by cells against `corpus/SOURCES.md`; confirm the knowledge note's citations; run the r16 gate once against committed inputs; re-check `SKILL.md:168` after the `mori` commit; have the lesson owner confirm the restored `corpus/lessons/round-16.md` text.

## Tool installs

None. No pacman, `uv`, or other installs by this seat.
