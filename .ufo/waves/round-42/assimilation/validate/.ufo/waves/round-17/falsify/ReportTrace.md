# ReportTrace — round-17 wave2 crosslink falsification (mori)

Seat: `MoriR17.ReportTrace-4` (leaf, read-only, no subagents). No production, SCORECARD, LOG, registry or knowledge edits. No VCS mutation. No live probes, no selftests re-run. No tools installed or upgraded.

## Scope attacked

- LOG.md round-17 section (lines 1118–1182) and the round-12..17 sections of SCORECARD.md (lines 582–1062), including both Capabilities tables and the round-17 claim/score tables (lines 1009–1062).
- corpus/SOURCES.md rows S035–S048 and every `used-by` cell.
- corpus/knowledge/{seat-terminal-status-r17,jj-branch-anchor-r17}.md headers and bodies.
- corpus/lessons/round-17.md (M1–M10 table, Measurement records); corpus/QUALITY.md lines 112–140 (criteria 43–48); PROVINCE.md and corpus/README.md round-17 pointers.
- `.ufo/waves/round-17/PINNED_INPUTS.json`, `evidence/*`, `fixtures/seat/expected.json`, `frozen/*`, `falsify/swarm-registry.json`.
- Measurement revision under test: `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`. Branch tip at audit: `5c1dfb8` (one descendant, "committed claim measurements and preservation receipts"). Entering: `24526ea`.

Not attacked: C1/C2/C3 mechanism correctness (other seats own it); live journal/transcript probes (none run).

## Verdict by requested check

| Check | Result |
|---|---|
| Claims ≤3 distinct axes | PASS. Three claims: C1 coverage, C2 operability, C3 calibration (SCORECARD.md:1009–1013). Caveat F2: C3's axis is not in the lane's own owned-axis header. |
| Scores held | PASS as arithmetic: coverage 6→6, operability 7→7, calibration 5→5 (SCORECARD.md:1039–1041); depth/freshness 5, adjacency 6 held. Caveats F2 (stale top table) and F10 (verdict "improved" with no declared rubric). |
| Capability row only after demonstration | PARTIAL. Round-17 rows `terminal-at-scan seat observation` (seat-after 54/54, seat-live.json) and `no-pathspec misroot witness` have receipts. The witness row's "sibling controls unclaimed" half is not witnessed (F1). Round 12–16 rows point to receipts that exist and, for the ones re-counted, reproduce. |
| SHONEN no self-x | PASS. SHONEN.md:5–8 has four `- [ ]`; `grep '^- \[ \]'` = 4; no `[x]`, `[X]`, `[~]` or ✓ box marker outside `.ufo/` in any `*.md`; SHONEN.md unchanged `24526ea..tip` (empty diff). |
| Measurement revision matches receipts | PASS for tools, fixtures, frozen bytes; MINOR for ledger timing (F3). |
| Broken pointers | See "Broken pointers" below: 1 pending report, 4 `fleet-ledger/` pointers, 1 superseded baseline path, 1 removed sandbox path. |

## Re-executed read-only checks (command → rc → output)

All with `cwd=mori-shokunin`; each `jq` counting command is one the receipt itself names.

- C1 counter `jq -s '[.[] | (.summary.capability_absent + .summary.mismatched)]' seat-before/run-manifest.json seat-after/run-manifest.json` → rc0 `[54,0]`. Matches PINNED_INPUTS claims.C1 (54→0) and count-c1.json `stdout` `[54,0]`.
- C2 counter `jq -s '[.[].totals.failed_assertions]' jj-before/… jj-after/…` → rc0 `[21,0]`. jj-before totals: cases 12, match 7, mismatch 5, assertions 124, failed 21; jj-after: match 12, assertions 134, failed 0. Matches LOG and PINNED.
- C3 counter `jq -s '… 1 - (candidates|select(.path=="MoriR16.Lesson")|length)' c3-before.json c3-after.json` → rc0 `[1,0]`. c3-before: `MORI_MISROOT_CLEAN`, candidate_count 0; c3-after: `MORI_MISROOT_CANDIDATE`, candidate_count 1, path `MoriR16.Lesson`, read_bytes 847.
- Historical counters, re-run: R13 live `[0,2]` (round-13 live-measurement.json); R13 gate `[2,0]`; R14 `[6,0]`; R15 `[34,0]`; R16 capability `[{64 absent,0 match}, {0 absent, 64 match}]`. All match SCORECARD rows 679–687, 772–782, 855–858, 960–963.
- Seat live receipt (`seat-live.json` → `.stdout` parsed): `files_scanned` 469; totals completed 368 + dead_rate_limit 94 + aborted 6 + incomplete 1 + unavailable 0 = 469; `retry_exhausted` 90; per-prefix dead_rate_limit TabiR17 22 / TsukuroiR17 44 / SoujiR17-3 28; settle 900; finding `MORI_SEAT_TERMINAL_DEAD`, rc1. Matches LOG and SCORECARD round-17 rows.
- Seat fixtures: `expected.json` 54 cases = 54 `seat-after/cases/` directories.
- PINNED pins: `expected.json` `.pins` has 81 entries; all 81 verify. 78 regular files and 3 symlinks (`SymlinkIgnore/{Dangling.jsonl,Link.jsonl,linked-dir}`) verify under the convention "sha256 of the link target string" (`readlink` → sha256 matched 3/3). See F12.
- PINNED tool digests: all 9 listed sha256 match on disk (census 12e8e2d9…, seat-terminal 5819c3c0…, seat-regressions 21285c2b…, jj-regressions 1067e4ae…, context-check 4bb17c37…, misroot-sweep 0a852fe6…, expected.json b684c63b…, frozen census f1f8d1b6…, frozen MoriR16.Lesson 15f9f82d…).
- Entering census: `git show 24526ea:tools/mori-census.sh | sha256sum` = `f1f8d1b6…` = `frozen/mori-census.sh`.
- Blob identity: `git rev-parse 273aa74:tools/X` = `git rev-parse refs/heads/master:tools/X` for all six round-17 tools; observed pairs: mori-census.sh 2a847a0b…, mori-seat-terminal.py c70462be…, mori-round17-seat-regressions.py fc536a2d…, mori-round17-jj-regressions.py f123e7f3…, mori-round17-context-check.py 8ae4b224…, mori-misroot-sweep.py f4175acf… (each measured = head).
- `git diff --stat 273aa74 refs/heads/master -- tools corpus/knowledge corpus/SOURCES.md .ufo/waves/round-17/fixtures .ufo/waves/round-17/frozen` → only `frozen/c3-expected.json | 14 +`.
- Selftest receipts (rc0 each): census 125/125; seat 33 arms; seat gate 14 names; jj gate 13 names; misroot 11 arms (fixture_sha256 15f9f82d…, 847 B); context 29 arms; silence oracle `matched=28 total=28`; r13 `claims=24 pass=24`; r14 `claims=44 pass=44`; r15 34/34 frozen-red PASS lines present (63/63 total not re-counted here). `preservation.json`: 7 files `unchanged:true`, 0 false.
- SOURCES: `grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` = 48. `source-count.json` stdout: 24526ea 40 rows (mined 19, queued 20, rejected 1; A37/B2/C1) → 273aa74 48 rows (mined 25, queued 22, rejected 1; A45/B2/C1). `git diff -U0 24526ea 273aa74 -- corpus/SOURCES.md` contains only added `+` lines (S041–S048 plus two search-log lines); zero `-` lines. Existing-row cells unchanged.
- SOURCES `used-by` cells: 13 distinct corpus paths; all exist (including corpus/knowledge/seat-terminal-status-r17.md for S041/S043 and jj-branch-anchor-r17.md for S044–S047; S042/S048 `—`, matching "queued").
- Knowledge `source:` build pointers: `.ufo/waves/round-17/build/{SrcRfc6585,SrcZaiErrorCodes,SrcJjGitCompat,SrcJjMetaedit,SrcGitMergeBase,SrcGitSymbolicRef,SrcRfc9110,SrcPacmanLog,TranscriptShapes,RetryRecoveryShape,CriticC1,LiveLaneHeadVsBranch,ClaimSeparability,DeadSeatCrossCheck,PacmanTxnToday,PacmanActorTrace,OverlapTsukuroi,MisrootR16Facts,R16LessonM7,ScorecardAxisCheck,SentinelTranscripts,SeatNaming,CriticFrontier}.md` all exist.
- QUALITY 43–48 ↔ lesson M1 (Q43), M2 (Q45), M3 (Q44), M4 (Q46), M6 (Q47), M7 (Q48); M5 has no Q (scope-only). Consistent.
- Pacman pointers: `/var/log/pacman.log:2462` = `09:15:30 … pacman -Syu`; `:3161` = `13:23:08 … pacman -U … zcode`. Both match corpus/lessons/round-17.md cross-domain paragraph and LOG.md:1152.
- Registry-to-report: `falsify/swarm-registry.json` (`wave` mori-r17-w2-falsify, `updatedAt` 19:46:54Z) has 64 members (object keyed by name). Per-name `test -e falsify/<name>.md`: 15 present, 49 absent at audit time. Wave still running; see F6.
- Git commands used were read-only only: `rev-parse`, `cat-file -e`, `log --oneline`, `merge-base --is-ancestor`, `diff --stat`, `diff -U0`, `show <rev>:path`, `ls-tree`. No jj command run.

## Findings (ordered by severity)

**F1 — medium. C3 capability row claims "sibling controls unclaimed"; no receipt witnesses a planted sibling.**
- SCORECARD.md:1054 claims the witness "leaves sibling controls unclaimed".
- corpus/lessons/round-17.md, Measurement records, C3 paragraph: "plants the exact 847-byte archived root artifact and a sibling control".
- `evidence/c3-before.json` and `c3-after.json`: `grep -c TabiR16` → 0 and 0. The only candidate in c3-after is `MoriR16.Lesson`. A planted-then-unclaimed sibling and an absent sibling produce identical receipts.
- The receipts' `fleet_root` is `.ufo/worktrees/round-17/MainChecks/c3-fleet`; that path is absent at audit (`ls -d` printed "No such file or directory"; exit status not captured). The sandbox cannot be re-derived from the repo.
- Fix direction: record the sibling's planted path and its per-file scan result in c3-after.json, or narrow the capability text to "single exact-artifact detection".

**F2 — medium. Stale top score table and an owned-axis header that contradicts C3.**
- SCORECARD.md:8–16 `## Axes` still reads coverage 5, operability 6, depth 4, freshness 5, calibration 5, adjacency 6. Current scores (SCORECARD.md:1039–1041, 690–696, 789–794, 874–880) are 6/7/5/5/5/6. The correction is prose only (SCORECARD.md:616–619). Any reader or tool that reads the table gets wrong numbers.
- SCORECARD.md:3–4: "Axes owned by this lane: **coverage + operability**… the owned pair drives the round's axis-move." Round 17 declares C3 on calibration, which is not in that owned pair. The lesson (M5) and LOG.md:1131–1133 adopt the literal all-six reading instead. AXES.md:33 says "lowest-scoring non-retired axis", which supports the all-six reading [INFERENCE]. The header was not amended.

**F3 — low-medium. Ledger timing: measured revision 273aa74 vs bookkeeping committed later.**
- Tool, fixture and frozen-byte content is unchanged from 273aa74 to the tip (see Blob identity and diff-stat above). The measurement revision is sound for those bytes.
- `PINNED_INPUTS.json` is absent at 273aa74 (`git cat-file -e 273aa74:.ufo/waves/round-17/PINNED_INPUTS.json` → rc128) yet its `observed_at` is 16:35:35, after the counters ran at 16:35:15–:20 (`count-c*.json`). LOG.md:1164 and SCORECARD.md:1032–1035 say PINNED binds the measurement.
- `frozen/c3-expected.json` (the "frozen" witness pin named in corpus/lessons/round-17.md) is absent at 273aa74 and is not listed in PINNED `files`. Its bytes are correct now (sha256 of `frozen/MoriR16.Lesson` = 15f9f82d…), so this is a provenance-ledger gap, not a content mismatch.
- Fix direction: add `c3-expected.json` to PINNED `files`, and state in LOG that PINNED and c3-expected were committed in 5c1dfb8, after the 273aa74 measurement.

**F4 — low. Four dead `fleet-ledger/` pointers (round-12 rows).**
- LOG.md:646 `fleet-ledger/.ufo/waves/kaika-w1/mori-state.md`
- LOG.md:648 `fleet-ledger/.ufo/prompts/mori-round-12.md`
- LOG.md:702 `fleet-ledger/.ufo/reports/round-12/mori.md`
- corpus/README.md:335 `../../fleet-ledger/.ufo/waves/kaika-w1/mori-state.md:31,190`
- None resolves literally (`/home/vgpnk/Projects/shokunin/fleet-ledger` and `/home/vgpnk/Projects/fleet-ledger` both absent). The files exist at fleet root: `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w1/mori-state.md`, `.ufo/prompts/mori-round-12.md`, `.ufo/reports/round-12/mori.md`. [INFERENCE: the ledger was folded into fleet root.] Fix: rebase to `../.ufo/…` or record the alias.

**F5 — pending. Round-17 fleet report pointer is not written yet.**
- corpus/lessons/round-17.md:4 cites `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mori.md`. `ls` → absent at audit. This is the scribe's owed output, so it is a pending pointer, not yet a broken one. Re-check after the scribe writes.

**F6 — info/pending. Falsify registry not closed.**
- `falsify/swarm-registry.json`: 64 members; 15 `<name>.md` present, 49 absent (per-name `test -e`). Includes `ReportTrace` (this file). Not a crosslink defect; re-check at closure.

**F7 — low. Knowledge-table precedence reads opposite to the tool and fixture.**
- corpus/knowledge/seat-terminal-status-r17.md:20 lists "type 1113/1308 or quota token → dead_quota" above line 21 "type 1302 or rate-limit/429 token → dead_rate_limit". A reader following row order would expect quota text to beat 1302.
- The tool does the opposite. `tools/mori-seat-terminal.py:263–272`: code 1113/1308 → dead_quota; code 1302 → dead_rate_limit; then quota tokens; then 429/rate tokens. expected.json case `code_rate_1302_beats_quota_token` wants `dead_rate_limit`.
- Fix: state precedence explicitly in the table (codes → quota tokens → status/rate tokens) or reorder rows to match.

**F8 — low. "README" correction claim not matched by the diff.**
- LOG.md:1146–1147: "Routed corrections are appended in PROVINCE, README, r16 cursor note, QUALITY43–48."
- `git diff --stat 24526ea 273aa74 -- README.md` → empty. README.md is 861 B, mtime Oct 19. The changed file is `corpus/README.md` (+18). Either the LOG means corpus/README.md (fix the wording) or the README edit is missing.

**F9 — low. Stale baseline path still live in knowledge bodies.**
- corpus/knowledge/drift-pin-r10.md:195, 200, 209, 226, 227 name `corpus/evidence/baseline-r10-20261015T2210Z.json`; the file is absent (`ls corpus/evidence | grep -c 2210Z` → 0). Correction exists at drift-pin-r10.md:292 and LOG.md:551–556. Also named in corpus/knowledge/audit-r11.md:158, 401 as the F03 defect. Superseded in-note; dead as a live pointer.

**F10 — low. Verdict "improved" with a held score, and no declared round-17 rubric.**
- SCORECARD.md:1039–1041 gives verdicts "improved" for C1/C2/C3 with score `6→6`, `7→7`, `5→5`. Rounds 13–14 declared an explicit score rubric (SCORECARD.md:681–687); round 17 does not state when a point moves. [INFERENCE] The AXES verdict vocabulary has no `improved-but-score-held` state. Recommend an explicit one-line rule.

**F11 — low. Receipts do not record rc for the context checks.**
- LOG and lesson say `context-check-wave2-original.json rc1 → context-check-wave2.json rc0`. The JSON artifacts carry `finding_id`/`contexts_failing` but no rc field (keys: `claims_runtime_prevention, clause_ids, clauses_checked, contexts, finding_id, spec_sha256, static_only` and the wave2-original variant with `contexts_failing:1`, `missing:["transcript_fields_only"]`). The rc claim is unverifiable from the artifact [INFERENCE].

**F12 — info. Symlink pins use an undocumented convention.**
- The three symlink pins hash the link-target string, not the target content: `sha256sum` of the link follows it and mismatches (`Link.jsonl` → `trap.txt`, `linked-dir` → `real-dir`, `Dangling.jsonl` → missing). Under the target-string convention all 81 pins verify. The convention is not documented in `expected.json` or PINNED. Documentation gap only.

**F13 — info. Self-caused scratch writes, cleaned.**
- During this audit my own shell redirections created `/tmp/.none` and `.ufo/.scratch-none`. Both were removed; `ls` → absent (rc2). No other writes outside this report.

## Broken pointers (complete list, current-round relevant first)

| # | Pointer | Where | Status |
|---|---|---|---|
| 1 | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mori.md` | corpus/lessons/round-17.md:4 | pending (absent) — F5 |
| 2 | `fleet-ledger/.ufo/waves/kaika-w1/mori-state.md` | LOG.md:646 | broken; fleet-root target exists — F4 |
| 3 | `fleet-ledger/.ufo/prompts/mori-round-12.md` | LOG.md:648 | broken; fleet-root target exists — F4 |
| 4 | `fleet-ledger/.ufo/reports/round-12/mori.md` | LOG.md:702 | broken; fleet-root target exists — F4 |
| 5 | `../../fleet-ledger/.ufo/waves/kaika-w1/mori-state.md:31,190` | corpus/README.md:335 | broken — F4 |
| 6 | `corpus/evidence/baseline-r10-20261015T2210Z.json` | corpus/knowledge/drift-pin-r10.md:195,200,209,226,227; audit-r11.md:158,401 | superseded (absent); correction at drift-pin-r10.md:292 — F9 |
| 7 | `.ufo/worktrees/round-17/MainChecks/c3-fleet` (fleet_root) | evidence/c3-before.json, c3-after.json | removed sandbox; not re-derivable — F1 |
| 8 | `SCORECARD.md:3–4` owned-axis header | SCORECARD.md | stale vs round-17 C3 — F2 |
| 9 | PINNED `files` omits `frozen/c3-expected.json`; PINNED absent at 273aa74 | PINNED_INPUTS.json | ledger gap — F3 |
| 10 | `.ufo/reports/round-12/mori.md` (no `..` base) | SCORECARD.md:598 | resolves only from fleet root — base ambiguous (low) |

Not counted as broken: `corpus/closure` and `evidence/receipt` (prose nouns); `.ufo/waves/round-17/evidence/recheck-{seat,jj}` (fresh output directories by design); `tools/killsnoop.bt` / `tools/oomkill.bt` (external URL paths in SOURCES S019/S020); `knowledge/frontier` (prose). Bare round-scoped shorthands such as `evidence/c1-count.json` (LOG.md:1083, r16), `evidence/misroot-sweep.json` (LOG.md:1109, r16), `build/ReviewHarnessGate.md` (LOG.md:912, r15), `build/WindowTool.md` (LOG.md:1034, r16), `frozen/entering-capability.json` (SCORECARD.md:952, r16), `evidence/security-probes.json` (LOG.md:748, r13) resolve under their named round's wave directory; they are unqualified but not broken.

## Verified OK (no defect in scope)

- LOG round-17 measured-commit wording (273aa74) matches SCORECARD.md:1032, PINNED `measured_commit`, and all three `count-c*.json` `measured_commit` fields.
- Entering tip 24526ea exists in history; 273aa74 is an ancestor of the branch tip (`merge-base --is-ancestor` rc0).
- Round 16 M33 pointer in LOG.md:1109 resolves to corpus/lessons/round-16.md:244.
- corpus/knowledge/journal-cursor-window-r16.md, roster-truth-r12.md, structured-journal-scopes-r13.md, journal-alarm-routing-r14.md, journal-positive-evidence-r15.md exist; their round-13–16 capability-row evidence files exist (`round-13/evidence/regressions-accepted/evidence.json`, `round-14/evidence/green-after-accepted/evidence.json`, `round-15/evidence/green-after-final/run-manifest.json`, `round-16/evidence/capability-after/run-manifest.json`, `live-window-{user,system}.json`).
- Round-12 evidence paths exist: `corpus/evidence/roster-r12-20261019T220912Z-{live,selftest,oracle,mutation.md,walltime,before-live}.log`, `drift-r12-20261019T2204Z-classification.md`, `drift-r12-20261019T2230Z-after-roster.log`.
- Sibling repo pointers resolve: `../tsukuroi-shokunin/corpus/knowledge/{adjacency-handoffs-fleet-r1,kill-event-deep-r8,oom-event-plane}.md`, `../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md`.
- corpus/knowledge/seat-terminal-status-r17.md `recheck:` commands reference existing `tools/mori-seat-terminal.py`, `tools/mori-round17-seat-regressions.py`, `.ufo/waves/round-17/fixtures/seat`.
- SOURCES S041 quote lines: SOURCES cell "lines 132–135" vs lesson "lines 134–135" — consistent (132 is the section heading, see `build/SrcRfc6585.md:20`).
- LOG `FIFO replaced by fifo_files metadata`: `tools/mori-round17-seat-regressions.py:26,56,215` implement the metadata; `FifoSkip` case has no FIFO on disk (`find -type p` → none).
- `c3-expected.json`: `legacy_expected_detected:false`, `default_expected_detected:true`, `default_expected_matched_in:["path"]`, bytes 847 — matches receipts.

## Not verified (named, not claimed)

- C3 sibling plant (F1): no receipt.
- r15 63/63 total: only the 34/34 frozen-red subset was re-counted.
- External URL quotes in S041–S048 were not re-fetched (out of the artifact-crosslink scope).
- Live transcript/journal state: not re-probed (by assignment).

## Artifacts touched

- Written: `.ufo/waves/round-17/falsify/ReportTrace.md` (this file) only.
- Removed (own scratch, see F13): `/tmp/.none`, `.ufo/.scratch-none`.
- Installed/updated tools: none.
