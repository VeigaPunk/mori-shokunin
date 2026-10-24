# Round 37 wave 1 — distilled findings

**Target:** scored tip `e57c58b57c025364e79d130fbdf764d2674d83d6` (entering tip `842a32074b5c7972e9728f3f629d83eb92f127c2`). Findings below are limited to what the named wave seats reported. Post-tip corrections are separated from the scored-tip observations.

## Behavior and gates observed by seats

| Surface | Command / observed result | Source |
|---|---|---|
| C1 v1 | `python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 41` → blind `24/24`, real and challenge pass, all three negatives rejected, `C1=met`, `EXIT=0`. Seeds 41–43 also pass. | `ExecC1Seed41.md:18-45`, `RevC1Predicate.md:12-16,20-74` |
| C2 v1 | `python3 .ufo/waves/round-37/count-c2.py e57c58b57c025364e79d130fbdf764d2674d83d6` → all eight checks PASS, `C2=met`, `EXIT=0`. | `RevC2Binding.md:30-41`, `ExecC2Twice.md:30-76` |
| Fetch-policy selftest | `python3 tools/mori-source-drift.py --selftest` → six cases PASS, `EXIT=0`; cap and redirect mutants each fail their named arm with `EXIT=1`. | `RevC2Arms.md:8-77` |
| Freeze/census | Freeze verifier reports 8/8 blob and 3/3 SHA-256 pins match. SOURCES census reports 225 rows, 0 malformed rows, no duplicate IDs, and S221–S225 present. | `ExecFreezeVerify.md:23-56,143-148`; `ExecSourceCensus.md:29-73,92-98` |
| r17 regression | `python3 tools/mori-round17-jj-regressions.py --selftest --scratch .ufo/waves/round-37/scratch-rev` → `SELFTEST ok`, `EXIT=0`; an XDG-escape mutant fails the selftest, `EXIT=1`. | `RevR17JJ.md:19-26,44-76` |
| Post-tip re-score | At `4bfa0490`, C1 v2 reports `C1=met`, `EXIT=0`; C2 v3 reports all eight checks PASS, `C2=met`, `EXIT=0`. These are amendments after e57, not measurements by the scored-tip v1 counters. | `SCORECARD.md:2134-2142`; `evidence/c1-after-v2.txt:8-20`; `evidence/c2-after-v3.txt:1-11`; `evidence/freeze-r37-v3.txt:1-13` |

## Ranked findings

1. **HIGH — C1 v1's “real-arm clothing” leaves a real-arm-only memoizer discriminator.**
   - **Seats:** `RevC1Challenge` (FAIL); `RevNgC1Env` (PASS on a challenge-only liar, with a real-only bypass boundary); corroborated by `ExecC1Seed43`'s residual note.
   - **Evidence:** the scored counter sets `LANE_TITLE` to a string containing `"(challenge arm)"` at `.ufo/waves/round-37/count-c1.py:288`, while the real lane title is `corpus/SOURCES.md:1`; the challenge repo is nested under the lane scratch path while the real repo is the lane root (`count-c1.py:56,762-768`; `RevC1Challenge.md:37-46,51-66`). `RevC1Challenge`'s probe command was `python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --tool /fast/scratch/hyaku/mori-r37/RevC1Challenge/probe.py --seed 11`; the probe printed no summary and the counter returned `C1=unmet`, so this was not a measured successful exploit. The report's proposed title/path-keyed real-only acceptance is explicitly a projection, not an end-to-end mutant run (`RevC1Challenge.md:97-110`). `RevNgC1Env.md:108-111` independently states that a tool honest on blind+challenge but lying only on the real arm “does pass all three arms.”
   - **Status:** v2 later made challenge title equal the lane title and added a drawn ancestor arm (`SCORECARD.md:2138`; `freeze-r37-v2.txt:13`; `c1-after-v2.txt:8-19`). However, `ExecC1Seed43.md:142-155` records a residual: a tool keyed on the published real-arm revision can still use that one fixed answer; the v2/v3 honest-tool receipts do not test that targeted liar. The scored-tip v1 finding remains.

2. **HIGH — C1 timeout handling misses its promised boundary and can pass a timed-out real arm.**
   - **Seats:** `LabTimeoutBoundary` (FAIL); `ExecC1Seed43` records the same timeout machinery on v1/v2; `CritDebtDisposition` identifies the still-open r36 debt (f).
   - **Evidence:** with `TOOL_TIMEOUT_S=120`, `TOOL_GRACE_S=5`, `.ufo/waves/round-37/count-c1.py:533` launches GNU `timeout 120`, but `:535` gives the outer `run()` a 180-second timeout. `FIX_SLEEP=125 python3 arm_probe.py ... 125 real` produced `WALL_S=120.13`, exit 124, `no summary line (exit 124)`, not `tool_timeout`; a SIGTERM-deaf 200-second fixture reached `tool_timeout` only after 185.24 seconds (`LabTimeoutBoundary.md:75-150`). A fixture that flushes the correct summary and then hangs produced `ARM_VERDICT pass`, `TOOL_EXIT 124` in `real_arm()` because `.ufo/waves/round-37/count-c1.py:733-734` does not check the child exit code (`LabTimeoutBoundary.md:171-205`).
   - **Status:** the v1/v2 timeout code was byte-identical in the seat's comparison (`LabTimeoutBoundary.md:207-222`). Main later marked debt (f) OPEN, but the measured boundary mismatch and real-arm false pass are not fixed by that disclosure (`SCORECARD.md:2087-2093`).

3. **HIGH — C2 v1 accepts stale or content-free corpus-binding evidence.**
   - **Seats:** `ExecDriftLive`, `CritC2ContentFree`, `ExecKnowledgeCheck`, `ScribeReport`, `ExecScorecardRows`, `RevDebtR36`.
   - **Evidence:** at e57 the registry has 225 rows (`corpus/SOURCES.md:227-231`) while the committed `drift-live-r37.txt` reports `rows=220 fresh=49 drifted=9 no-copy=162` (`evidence/drift-live-r37.txt:221-223`). The exact-tip sweep in `ExecDriftLive.md:117-130` reported `rows=225 fresh=52 excerpt=0 drifted=10 unavailable=0 no-copy=163`, `EXIT=1`; S223 is the added timestamp-only drift at `corpus/evidence/sources-r37/S223.src:1953`. Yet `python3 .ufo/waves/round-37/count-c2.py e57c58b57c025364e79d130fbdf764d2674d83d6` returns `C2=met`, `EXIT=0`, because `count-c2.py:49,208-211` checks a fixed summary substring. Independently, three scratch-only counterexamples—a knowledge entry with tokens but no located quote, a capability row pointing to a missing file, and a live receipt containing only the summary line—each pass; combined, all eight checks still pass and C2 is met (`CritC2ContentFree.md:46-110,112-129`). The knowledge check also accepted the wrong hardening commit string: the entry/counter named `8ff9bba`, but the tool change landed at `1caa242` (`ExecKnowledgeCheck.md:94-115`).
   - **Status:** v3 at `4bfa0490` now checks the actual `1caa242` tool-touch and the 225-row live sentence and reports C2 met (`evidence/c2-after-v3.txt:1-11`; `SCORECARD.md:2139-2142`). The content-free discrimination gap remains explicitly disclosed and routed to round 38 (`SCORECARD.md:2101-2108`); no seat report here demonstrates that v3 rejects the three fabricated shapes.

4. **MEDIUM — C2's freshness attribution is disputed; the measured delta is operability verification.**
   - **Seats:** `CritC2Axis` (FAIL) versus `CritAdmission` (PASS); `ScribeReport` reports the trend/claim limits.
   - **Verbatim conflict:** `CritAdmission.md:5`: “C1 targets calibration; C2 targets freshness.” `CritC2Axis.md:9-11`: “Freshness is the application surface here, not the measured number”; the counter does not establish that “a taught source claim was re-verified or became less stale.”
   - **Status:** the later scorecard correction re-attributes C2 to operability (held at 7) and says freshness did not move (`SCORECARD.md:2081-2086`). The score remains unchanged; the original declaration still labels C2 freshness at `SCORECARD.md:2045,2066`.

5. **HIGH / MEDIUM / LOW — caller-controlled code execution and unbounded C2 Git reads.**
   - **Seat:** `SentTools` (static review only; no untrusted candidate was executed).
   - **Evidence:** C1 runs the caller-selected `--tool` or tool extracted from the selected repo with the invoking user's privileges (`count-c1.py:80-85,532-535,874-888`); C2 runs the committed tool selftest and preserves the rest of the environment (`count-c2.py:95-99,151-160`). The report rates this HIGH if `--repo`/`--tool` are untrusted. It also rates C2 `show()` without timeout/output bound MEDIUM (`count-c2.py:102-112`) and relative `--tool` validate/execute-from-different-cwd LOW (`count-c1.py:532-535,874-878`).
   - **Status:** the main records the caller-selected tool as an accepted trust boundary and routes the C2 read bounds and relative-path fix to round 38 (`SCORECARD.md:2128-2132`).

6. **MEDIUM — r36 no-SIGKILL obligation remains open.**
   - **Seats:** `CritDebtDisposition`, `ScoutPriorRound`, `RevDebtR36`, `LabTimeoutBoundary`.
   - **Evidence:** `SCORECARD.md:2025-2026` routed “restructure the timeout path to avoid SIGKILL”; the scored counters still send SIGKILL after the grace (`count-c1.py:102-109`, `count-c2.py:79-86`). The timeout-disclosure change is not the original restructuring. Main records it as an operator-owned tradeoff and OPEN (`SCORECARD.md:2087-2093`; `corpus/lessons/round-37.md:74-77`). No timeout experiment was run by the static critics; `LabTimeoutBoundary` separately measured the C1 boundary behavior above.

7. **MEDIUM — C1/C2 gate capabilities had no SKILL registry rows at e57.**
   - **Seats:** `ExecGateRegistry`, `ScribeSkill`.
   - **Evidence:** e57 `SKILL.md:872-876` had only round-36 rows, while `SCORECARD.md:2058-2059` registered round-37 C1/C2 capabilities; `grep -n "round-37\|Round37\|R37\|r37" SKILL.md` returned `NONE` (`ExecGateRegistry.md:21-31`). The draft C1 row in `ScribeSkill.md:10` used kind `counter`, outside the `gate|probe` vocabulary; the conformant current rows use `probe` and C1 self-test `none` (`ExecGateRegistry.md:57-65`).
   - **Status:** rows are now present at current `SKILL.md:877-878` (also recorded by `ExecLogAnchors.md:45-50`); the scored-tip omission remains historical.

8. **LOW — absolute operator-home paths were committed in the scored evidence.**
   - **Seats:** `SentData` (LOW), `ScoutSentData`, `CritDebtDisposition`.
   - **Evidence:** the committed-snapshot scan found `/home/vgpnk` at `evidence/c1-before-memo.txt:2`, `c1-before-summary.txt:2`, and `census-start.txt:16`; the current-worktree scan additionally found `census-end.txt:16`. The archive scan found no credentials or raw cursors (`SentData.md:7-18`; `ScoutSentData.md:16-26`).
   - **Status:** erratum `5631efa` re-emitted receipts with repo-relative paths and `redacted:` lines; later lesson calls debt (e) closed by erratum, not by e57 (`SCORECARD.md:2094-2097`; `corpus/lessons/round-37.md:78`). The e57 bytes still disclose the paths.

9. **LOW — S225's source copy was absent from the scored tip, then added later.**
   - **Seats:** `ScribeReport`, `ExecLessonGate`, `RevC2Docs`; `SentScope` conflicts.
   - **Evidence:** `git ls-tree e57c58b ... corpus/evidence/sources-r37/` listed S221–S224 only; S225.src landed at `52d636d5` (`ScribeReport.md:61-64`; `ExecLessonGate.md:16-24`; `RevC2Docs.md:24-29,97-105`). `evidence/s225-copy.txt:1-12` records the later 1,854,393-byte copy.
   - **Verbatim inventory conflict:** `SentScope.md:34-38` lists `A corpus/evidence/sources-r37/S225.src`; `ExecReadmeRows.md:92-96` says the scored-tip directory “holds S221–S224 only; S225 … no committed copy.” The later copy commit is `52d636d5`.

10. **LOW — S225's lesson quote range initially omitted its final source line.**
    - **Seats:** `ScribeLesson`, `ExecLessonGate` (FAIL); `RevC2Docs` (PASS under a start-line interpretation).
    - **Evidence:** `corpus/lessons/round-37.md:13` cited `S225.src:8355`, but `network error` is on line 8356 (`ExecLessonGate.md:55,86-106`). `RevC2Docs.md:48,70-74` treated `:8355` as the start line and the broader SOURCES anchor `8318-8360` as covering both.
    - **Verbatim conflict:** `ExecLessonGate.md:55`: `S225.src:8355 … FAIL`; `RevC2Docs.md:48`: `S225 … YES … wraps to 8356`.
    - **Status:** commit `30dfe70` widened the lesson citation to `S225.src:8355-8356`; current gate report verifies PASS (`ExecLessonGate.md:60-81,138-155`).

11. **MEDIUM / LOW — LOG and scorecard anchors retain documentary inconsistencies.**
    - **Seats:** `ScribeScorecard`, `ScribeLog`, `ExecScorecardRows`, `ExecLogAnchors`, `RevSHONEN`.
    - **Evidence:** the original scorecard audit found 0/6 receipt cells with their producer command (`ScribeScorecard.md:5-15`); these headers were later added to the receipts (`evidence/c1-after.txt:1`, `c2-after.txt:1`, `5631efa`). `census-rows.txt`, `s225-copy.txt`, and the r17 receipt's `pre_fix:` line later support values previously missing in `ScribeLog.md:15-26`; held scores remain expressly self-assessed (`LOG.md:2168-2169`). Remaining: `LOG.md:2157` still pairs the 220-row summary with `drift-live-r37.txt`, while `LOG.md:2178-2180` says that file is now the 225-row sweep; `LOG.md:2147-2149` gives a before-arm shorthand that is not rerunnable as written (r37 counter rejects `--tool/--seed`; r36 counter needs the absolute fixture path). `ExecLogAnchors.md:79-94,96-100,121-138` records the exact failed and corrected command forms. The after receipts are at bcf65505, not at scored tip e57 (`ExecScorecardRows.md:34-57`).
    - **Additional LOW report defect:** fleet report `.ufo/reports/round-37/mori.md:146` says `w1-taskcall.json` is 82,884 bytes; `RevSHONEN.md:94-99` measured 83,204 bytes.

12. **LOW — QUALITY 106's literal expected line does not match the counter's padding.**
    - **Seat:** `ScribeQuality`.
    - **Evidence:** `corpus/QUALITY.md:856-859` requires the contiguous text `negative memo-n1.py rejected`; `count-c1.py:937-943` formats the fixture name with `%-14s`, and the receipt prints `negative memo-n1.py     rejected` (`evidence/c1-after-tip.txt:11`; `ScribeQuality.md:7-12`). The rejection is semantically present; the quoted exact string is not.

13. **LOW — repeated C1 seed tasks duplicated an existing review loop.**
    - **Seat:** `ScoutWaveSpec` (FAIL).
    - **Evidence:** `w1-spec.json:8-10,128-140`: `ExecC1Seed41/42/43` share one normalized target except `--seed`, while `RevC1Predicate` already runs all three seeds plus the predicate-byte check (`ScoutWaveSpec.md:48-52`). Lesson records this as M7 (`corpus/lessons/round-37.md:43`).

14. **LOW — round-37 dispatch log lacked the QUALITY 103 index-check record at the time of audit.**
    - **Seat:** `ExecIndexClean`.
    - **Evidence:** `bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin` → `MORI_INDEX_CLEAN staged=0 intent_to_add=0`, `EXIT=0`; but `dispatch-log.txt:7,13` had no `staged=`/`index` entry (`ExecIndexClean.md:110-135`). Later lines 17-19 now record the checks, so closed in the current log.

## Conflicts preserved verbatim for the canonical judge

- **C2 axis:** `CritAdmission.md:5`: “C1 targets calibration; C2 targets freshness.” `CritC2Axis.md:9-11`: “Freshness is the application surface here, not the measured number.” Later correction: `SCORECARD.md:2081-2086` says C2 is operability, with freshness not claimed to move.
- **Debt (f):** `ScoutPriorRound.md:19`: “disclosed: 120 s, SIGTERM then SIGKILL after 5 s, state `tool_timeout` … Not the SCORECARD ‘avoid SIGKILL’ plan”; `CritDebtDisposition.md:12`: “OPEN, behavior disclosed but the original obligation not closed.” Later status is OPEN at `SCORECARD.md:2087-2093`.
- **S225 source copy:** `SentScope.md:34-38` reports `A …/S225.src`; `ExecReadmeRows.md:92-96` says “S221–S224 only” and S225 has “no committed copy” at e57. Later seats and `s225-copy.txt` place the copy at `52d636d5`.
- **S225 quote range:** `ExecLessonGate.md:55` calls `S225.src:8355` a FAIL because the quote extends to 8356; `RevC2Docs.md:48` records `YES (wraps to 8356)` because it interprets 8355 as the start line and the registry anchor as the wider range. `30dfe70` later widened the lesson line citation.
- **C1 real-arm direction:** `RevNgC1Env.md:96-106` says “no detection key lets a liar pass the challenge” for a challenge-only lie; the same report's `:108-111` says a fixture that lies on the real arm only “does pass all three arms.” `RevC1Challenge.md:51-66` describes title/path separators enabling that opposite direction. These statements concern different lie directions and are retained as written.

## Surfaces, provenance, and limits

- **Behavior/gates:** positives and negatives above are transcribed from the named seat reports and receipts. My work was read-only; I did not rerun counters, tests, mutations, builds, or linters, and did not execute untrusted code.
- **Touched files:** only this distillation report was written. Product code, contract, judge, scorecard, logs, evidence and VCS state were not edited by this seat.
- **Later work:** the e57 findings must not be conflated with the 4bfa0490 re-score, C1 v2/C2 v3 freezes, erratum `5631efa`, source-copy commit `52d636d5`, or lesson-range fix `30dfe70`. These later artifacts are noted only as subsequent disposition/evidence.
- **Out of scope:** adjudicating conflicting seat interpretations, testing v2/v3 against every adversarial class, or deciding the operator-owned no-SIGKILL tradeoff.
- **Tools installed/updated:** none.

Report: `.ufo/waves/round-37/w1/DistillFindings.md`

VERDICT: FAIL — scored-tip defects include C1 timeout false-accept behavior at `.ufo/waves/round-37/count-c1.py:533-535,733-739` and C2's stale/content-free binding at `.ufo/waves/round-37/count-c2.py:49,187-211`.