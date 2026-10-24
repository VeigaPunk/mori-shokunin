# Round 24 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-22. Seat: HyakuCloseMori24, a fresh closure task dispatched by the hyaku orchestrator,
not by the lane. Runtime model as exposed to this seat: `anthropic/claude-opus-5-5`. No review seats
were dispatched; every check below was run by this seat. Base `c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130`,
head `4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e`, fleet report `.ufo/reports/round-24/mori.md`
(fleet commit `c7613588b56c2ee06824dd03788157fb954a58d9`).

## Decision

**Admitted.** Both declared claims verify against committed bytes and no owned axis is harmed.
C1 was re-measured with plain git and JSON reads. C2 was re-measured for its before-value and its
freeze order; its 12/12 selftest tally is evidence-verified, not re-run, because
`tools/mori-pressure.py` is a registered lane gate (`SKILL.md:641`; PROTOCOL §Gate standard,
Closure consequence). Bounds and routed defects are listed below. This note checks no SHONEN box.

## Conformance (step 1)

| Check | Command | Observed |
|---|---|---|
| report lands under the lane identity | `git -C <fleet> log --format='%an %H' -- .ufo/reports/round-24/mori.md` | `mori-shokunin c7613588…`; committed 06:25:40-03:00, after the lane tip (06:24:43-03:00) and before the driver's `complete` line (06:26:03-03:00) |
| SHONEN heading, one line per box | report `## SHONEN`; `grep -cE '^\s*- \[[ x~]\]' SHONEN.md` | 4 report lines (`[~]`, `[~]`, `[ ]`, `[~]`) for 4 boxes |
| cited commits exist and are ancestors | every 8–40 hex token in the report, `git merge-base --is-ancestor <h> master` | 27 lane hash tokens (25 distinct commits) all ancestors of `master`; `52b1364ba0b1` is the Linux commit of S096, not a lane hash; `22772c1` (round 23) exists |
| pushed, nothing left uncommitted | `scripts/hyaku/jj-lane.sh state <lane>` | `local=remote=4f05dd5a… ahead=0 behind=0 tracked=0 untracked=2` |
| untracked paths | `git status --porcelain`; `find .scratch -newermt '2026-10-21T20:34:00-03:00' \| wc -l` | `.scratch/`: 151,344 files, newest mtime 2026-10-21T12:30, 0 files newer than the attempt-1 launch; inherited round-22 scratch, **not round work**. `tools/__pycache__/mori-dispatch-ledger.cpython-314.pyc` (05:19 on 2026-10-22): bytecode cache from importing the ledger tool, no source content, **not round work** (hygiene item below) |
| dispatched prompt carries the contract | `.ufo/prompts/mori-round-24.md` (26,221 bytes, committed clean, lane author `3c2bf2f`) | MISSION/AXES binding, 1–3 claims, L2 minimum, push, L0 channel, report path, SHONEN, hash citation, write scope, frontier step and claim sizing all present |
| sources census | `scripts/sources-census.sh validate --root <fleet> mori` | exit 0, `ok`, the same six W04 warnings (S035, S037, S073–S076) the report names |
| seat shape | `wave{1,2}-run.json` `taskCall.tasks[].agent` counts | wave 1: 33 (12 scribe, 5 executor, 5 critic, 4 scout, 4 reviewer, 2 connector, 1 mutation-tester; 10 attack seats, 30%); wave 2: 36 (16 mutation-tester, 14 reviewer, 4 critic, 2 scout). Total 69, matching the report |

Driver digest (copied from the mutable `.ufo/watchdog.log`):
`2026-10-21T20:34:11-03:00 launch mori round=24 pgid=2902434 driver=hyaku-inline attempt=1`;
`2026-10-22T04:58:59-03:00 lane-dead-no-report mori round=24; retry same round (hyaku-inline attempt=1: superseded at 2026-10-22T04:56:36-03:00: stale 2026-10-21/22 author; fresh attempt)`;
`2026-10-22T05:03:02-03:00 launch mori round=24 pgid=7946 driver=hyaku-inline attempt=2`;
`2026-10-22T06:26:03-03:00 complete mori round=24; hyaku-inline attempt=2`.

## Per-claim re-check

### C1 — calibration: routed round-23 items (declared after: `"held": 4` of `"items": 4`, exit 0)

Re-measured independently of `tools/mori-routed-check.py`, which was not executed:

- **R4, before.** For each row of `.ufo/waves/round-23/*-attempts.json` and `*-ledger.json` at `c725aa37`,
  compare the row's `at` with the committer time of `git log -1 --format=%cI <rev> -- <dispatch_path>`.
  Result: 9 rows carry a `dispatch_path`; **8 mismatches**. All eight are `wave1-ledger.json` rows
  (`at` 17:03:11Z–17:24:14Z), each earlier than dispatch commit `22772c10` (15:10:59-03:00 = 18:10:59Z).
  The wave-2 row is in order. The eight `wave1-attempts.json` rows have no `dispatch_path`.
- **R4, after.** Same reading at `4f05dd5a` for round 24: 2 rows, **0 mismatches**.
  Wave 1: dispatch commit `06d4f4d2` 05:13:57, `at` 05:14:13, ledger commit `4059ffb5` 05:14:40.
  Wave 2: `753d2273` 05:56:36, `at` 05:56:44, ledger commit `13208d2a` 05:56:58 (all -03:00). Each `at` lies
  between the payload commit and the ledger commit.
  In both rows, `sha256` of `json.dumps(taskCall, sort_keys, compact, ensure_ascii=False)` equals
  `payload_sha256`. The byte length equals `payload_bytes`, and the task count equals `tasks_count` (33 and 36).
  Both `wave*-spec.json` files have a ledger whose last row is `started`.
- **R1–R3 regression guards, at both revisions:** `git rev-parse <rev>:.ufo/waves/round-23` is
  `3e5b2c9d…` at base and head. The `frozen` subtree is `0c067e21…` at both. The `tools/mori-retention-gate.py` blob
  (`988c5484…`) and `tools/mori-retention-reconcile.py` blob (`78c676e6…`) are unchanged.
  `git cat-file -e 4f05dd5a:tools/mori-quota-surface.py` and the `corpus/knowledge/quota-surface-r23.md` read
  each exit 128. 0 added paths under `tools/` or `corpus/knowledge/` contain `quota`, and
  `git grep -l CaseEscapedSpace 4f05dd5a -- tools` finds 0 files. 0 added lines in SCORECARD, PROVINCE, SKILL, LOG, README or `corpus/` match
  the privacy-clearance-true pattern.
- Committed tool evidence agrees: `evidence/c1-before-round23.json` `held 3`; `evidence/c1-after-13208d2.json`
  `held 4`. The report states `held 4` at the tip, after the `1046aca3` and `575a9f3f` hardening.
- **Ruling: improved, bounded.** The repair is that round 24 bound both dispatches before their calls, and a
  check now detects the round-23 defect. The eight round-23 rows remain in history, unchanged and pinned. Both
  times are written by the lane, so a backdated commit would pass. The denominator is 2 rows. The
  separate-worktree and invocation-reporting clauses of routed item 4 are unchecked, as disclosed. Score 5 → 5.

### C2 — coverage: system CPU, IO and IRQ pressure capability (declared after: `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0, over cases landed before the tool)

- **Before, re-measured:** `git cat-file -e c725aa37:tools/mori-pressure.py` exits 128.
- **Freeze order, re-measured:**
  - `git cat-file -e f6a29702:tools/mori-pressure.py` exits 128.
  - `git merge-base --is-ancestor f6a29702 6ee62487` holds.
  - `cases.json` has one commit (`f6a2970`), and its blob `39cc96ab…` is identical at `f6a29702` and `4f05dd5a`.
  - `jq '.cases|length'` gives 12, ids P01–P12.
  - The selftest code at the tip (`_selftest`, lines 528–588) reads `cases.json` and sets `total = len(cases)`; it skips no case.
- **Tally, evidence-verified:**
  - `evidence/c2-selftest-after.txt` reads `PASS 12/12`. It names no revision, and it lacks the `MATCHER` line that the tool printed by the time the file was committed (`89849a7`), so it is stale (defect D1).
  - Wave-2 RerunC2Count shows `PASS 12/12` at `a730ecfe`. That revision carries the `6ee62487` tool, so it is not the final tool.
  - The report and SCORECARD at the tip show `PASS 12/12` plus `MATCHER: rejected 48/48`. That equals 12 passing cases × 4 controls, which the code runs only for passing cases.
  - Static read of the later tool diff (`git diff 6ee62487 4f05dd5a -- tools/mori-pressure.py`, +56/−6): the changes are the non-UTF-8 → malformed path, thresholding of a regressed counter, the matcher controls and `--cases`. None of them changes an expected path of P01–P12 (P12's avg10 values are all below 10; no case carries non-UTF-8 bytes).
- **Independence, as the L1 discloses:**
  - The expected values are independent of the tool. FreezePressureCases wrote them from the contract and the v7.2 PSI sources, and its report states that it opened no implementation. The bytes prove that no tool existed in the lane at the freeze; they cannot prove what the seat did not read in a sibling clone.
  - The tool is not independent of the cases: `w1/BuildPressureTool.md:228` reads them during the build (lesson M8). Order is shown, not independent authorship.
  - Wave 2 killed 10 mutants and 6 survived: the threshold edge, a matcher that ignores `findings_include`, three grammar shapes, and PARTIAL outranking HIGH. The twelve cases therefore do not cover those behaviours. The responses (matcher controls 48/48 and the co-evolved supplementary file, 7 cases at the tip) are disclosed as not counted.
- **Ruling: improved, bounded.** The declared after-value holds as declared. The capability was shown running: `evidence/bracket-check-run.json` 5/5, and the SCORECARD capability row. Strength is limited by the survivors above. Score 6 → 6.

### Claim sizing

- Two claims on distinct axes, each with one after-value from one command over committed bytes.
- R4's "every row" is enumerated by the counting command. No other universal clause carries the result.
- Amendments A1–A4 landed before the code they govern:
  - `f7eb430` and `f38dbbd` precede `88f9620`;
  - `11d8f71` and `f299bd7` precede `f6a2970` and `6ee6248`.
- A5 (`a730ecf`) came after the tools but changed no target: it drops the unopenable `proc_pressure(5)` from the sourced list, and it narrows a before-state description, not a measurement.
- The calibration claim counts mismatches between a lane self-record (the dispatch ledger's `at`) and repo state (commit times). That record is the ledger, not SCORECARD or SHONEN. It meets the counted-not-asserted rule; that is noted here as a boundary.

## Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | improved | C1 above (R4 8 → 0 mismatches; R1–R3 held) |
| coverage | improved | C2 above |
| operability | unchanged | `git diff --name-status c725aa37 4f05dd5a`: 101 A, 7 M, 0 D, and no pre-existing `tools/` file modified. The census was byte-identical and its selftest passed 134/134 per the report (not re-run here) |
| depth | unchanged | SKILL additions are appended only (the whole diff has 0 deleted lines) and unclaimed; sweep defect D2 is in new material |
| freshness | unchanged | no pre-existing entry re-verified or modified |
| adjacency | unchanged | PROVINCE gains an appended adjacency note (tsukuroi `/proc/pressure/memory`); routed item 5 is a why-not, not counted |

`git diff c725aa37 4f05dd5a -- SCORECARD.md`: +39/−0. It holds the declaration, the measured outcome and two capability
rows; no score changed and no row was rewritten.

## Discernment spot-check

Sources re-opened by this seat on 2026-10-22 with `curl`. The digests are the first 16 hex characters of the SHA-256.

| Item | Gate decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S091 (admit, tier A) | mined | `https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c`, HTTP 200, sha256 `452318beaca3e6d1` (= Gate) | **agree** | Lines 1282–1283 read exactly `/* CPU FULL is undefined at the system level */` and `if (!(group == &psi_system && res == PSI_CPU && full)) {`. Line 1274 `only_full = res == PSI_IRQ;`, lines 1257–1263 (EOPNOTSUPP) and lines 1710–1721 (`psi_proc_init`) match their anchors. Primary code, tag-pinned |
| S093 (admit, newly written row) | mined | `https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig`, HTTP 200, sha256 `a43f09d89309a6bd` (= Gate) | **agree** | The Gate quote (19 words, within 25) is byte-exact at lines 730–731: "If you say Y here, the kernel will create /proc/pressure/ with the pressure statistics files cpu, memory, and io." The row's corrected anchor `730-731` is right |
| S097 (reject, tier C) | rejected | `https://man7.org/linux/man-pages/man5/proc_pressure.5.html`, HTTP 404, sha256 `80c3fe2ae1062abf` (= Gate) | **agree** | Body line 6: "The requested URL was not found on this server." The man7 section-5 index (`dir_section_5.html`, HTTP 200) has 0 matches for `pressure`. A nonexistent page supports no claim, and the flip condition (a published page) is sound |

Knowledge spot-reads against the re-opened psi.c:

- K5 correction ("averages recomputed only when the next 2-second update is due", `psi.c:1268-1270`): agree.
- K6 correction (`window_us == 0 || window_us > WINDOW_MAX_US`, lines 1372–1373; unprivileged `% 2000000`, lines 1379–1380): agree.

## Trend verdicts

- **Expansion: improved.** `corpus/knowledge/system-pressure-r24.md` is new ground (FR12 one-shot system PSI). Its `source:` cites S090–S096, all `mined`, tier A, opened this round. The registry grew from 89 to 97 rows, with 0 malformed and 0 old rows removed. A SKILL decision table and two SCORECARD capability rows were added, both shown running.
- **Quality: unchanged.** No pre-existing entry was re-verified, deepened or superseded: the diff deletes no line and modifies no file under `corpus/knowledge/`. The wave-2 corrections improve this round's own new entry before admission, not the corpus it held. No admitted entry failed its re-check. Sweep defect D2 is marked (corrections-precedence banner) or defensible in context, so it is not "false and left unmarked".
- **Discernment: improved.** The outside spot-check agrees with the gate on two admits and one reject. QUALITY 72–75 each cite a lesson (`round-23-verifier-spotcheck.md:62-65`, A4, CriticC1Admission). M3, M4 and M8 turn author errors into lessons with fixes.

## Routed defects (the lane fixes these next round; this note changes no target)

- **D1 — stale gate evidence.** `.ufo/waves/round-24/evidence/c2-selftest-after.txt` names no revision and predates the tool it shipped with: no `MATCHER` line, committed at `89849a7`. Commit future selftest outputs with the measured revision and the full stdout (§Gate standard, "a verdict names the revision").
- **D2 — correction sweep incomplete in the knowledge entry** (§Evidence standard, "Corrections sweep every mention"). At `4f05dd5a`, three lines still say what wave-2 CriticKnowledgeOverclaim corrected:
  - line 94–95 says the averages are "refreshed on each read" (K5);
  - the decision-table row at line 170 says "a shorter spike between two reads can be invisible" (K4 row 1, which the critic named explicitly and the corrections section does not cover);
  - the row at line 171 says "`null` means *undefined*" (P3).

  The report says all six statements were corrected before the report. Fix the body lines in place, with a correction note, and stop relying on a "this section wins" banner.
- **D3 — lesson count drift.** `corpus/lessons/round-24.md:79-80` says the supplementary file is S01–S06, `PASS 6/6`. At the tip it holds 7 cases, and the report says `PASS 7/7` (S07 was added at `c484f6d`). Append a correction.
- **D4 — hygiene.** The untracked `tools/__pycache__/` was produced this round by importing the ledger tool. Add an ignore rule or run with `-B`. Leave `.scratch/` (round 22) to its owner's disposition, with no deletion by closure.
- **Carried bound (not a defect):** C1 R4 trusts lane-written times and has no upper bound on `at`. A harness-observed dispatch time (for example the wave-slot grant) would close the backdating gap.

SHONEN: no box is fully checkable by a non-author at this tip. The report itself grades three boxes `[~]` and one `[ ]`.
