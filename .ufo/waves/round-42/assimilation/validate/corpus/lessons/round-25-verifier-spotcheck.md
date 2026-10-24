# Round 25 — non-author verifier spot-check (mori)

author: hyaku closure (non-author integrator, @m_opus)

Runtime model as exposed to this closure session: `anthropic/claude-opus-5-5` (configured `task` route, no
model parameter passed). Closure dispatched by the hyaku orchestrator, not by the lane. Measured
2026-10-22 (UTC ~12:30Z) against base `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf` and head
`829d8c9072d5907b9050d06c16cc34b0bb73d0f8` (`master` = `origin/master`). Report:
`.ufo/reports/round-25/mori.md` (fleet repo). Three read-only reviewer seats (SpotCheckSources,
RetentionHarm, RunwayAndSkill) ran re-checks for this note; their outputs are folded in below. No lane tool or
gate was executed by this closure (PROTOCOL §Gate standard, Closure consequence); every measurement below is
git, grep, jq, curl or a Python regex over committed blobs.

**Admitted.** Both declared claims re-derive against committed bytes and no owned axis is harmed at the head.
C1 was re-measured with plain git reads (4 → 0), under both the amended (A1/A3/A5) and the original contract
predicates. C2's before-value and freeze order were re-measured; its `PASS 21/21` is evidence-verified, not
re-run. Both claim statements are wider than their counters; the verdict rests only on the counted values, and
the excess is routed below. This note checks no SHONEN box.

## Conformance (step 1)

| Check | Command | Observed |
|---|---|---|
| report lands under the lane identity | `git -C <fleet> log --format='%an %H %ci' -- .ufo/reports/round-25/mori.md` | 10 commits, all `mori-shokunin`; last `b17dff0a` at 09:06:34-03:00, after the lane tip (09:06:19) and before the driver `complete` line (09:07:00) |
| driver digest (copied from mutable `.ufo/watchdog.log`) | `grep 'mori round=25' .ufo/watchdog.log` | `2026-10-22T06:42:03-03:00 launch mori round=25 pgid=2248596 driver=hyaku-inline attempt=1`; `2026-10-22T09:07:00-03:00 complete mori round=25; hyaku-inline attempt=1` |
| SHONEN heading, one line per box | report `## SHONEN`; `SHONEN.md` | 4 report lines (`[~]`, `[~]`, `[ ]`, `[~]`) for 4 boxes; `SHONEN.md` unchanged in the round, all `[ ]` |
| cited commits exist and are ancestors | every backticked 8–40 hex token; `git merge-base --is-ancestor <h> master` | 46 distinct commit tokens, all ancestors of `master`; `48df844a` is a blob (the frozen cases file), as the report says |
| pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain` | `local=remote=829d8c90… ahead=0 behind=0 tracked=0 untracked=1`; the one untracked path is `.scratch/` (newest mtime 2026-10-21, inherited, not round work) |
| prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/mori-round-25.md) templates/round-prompt.md` | 22 differing lines, every one a placeholder substitution (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §6 hyaku addendum appended (lines 141–350) |
| seat shape | `wave{1,2}-run.json` `tasks[].agent` counts | wave 1: 34 (12 scribe, 6 scout, 5 reviewer, 4 executor, 4 critic, 2 connector, 1 mutation-tester; 10 attack, 29%); wave 2: 38 (15 reviewer, 13 mutation-tester, 6 critic, 4 scout; 34 attack). Total 72, as reported. `ls-tree w1/` 34 reports, `w2/` 38 reports |
| sources census | `scripts/sources-census.sh validate --root <fleet> mori` | exit 0, `ok`; 6 W04 warnings (S035, S037, S073–S076), all pre-existing rows, as the report says |

Conformance defects (status-neutral): the report's opening "Lane tip" line names `e0e33c11`; the true final tip
`829d8c90` appears only in addendum 8. Gate standard: `tools/mori-routed-r24.py` and `tools/mori-job-runway.py`
both return verdict exit codes but have no registry row in `SKILL.md` (the round-24 tools have one at
`SKILL.md:641-642`); `mori-routed-r24.py` has no self-test. Neither is graded conformant as a gate.

## Claims (step 2)

### C1 — calibration: routed-check mismatches 4 → 0 (re-measured)

Plain reads, no lane code run:

| Item | Command (abridged) | at `28b79d3d` | at `829d8c90` |
|---|---|---|---|
| D1 (SCORECARD:1514 vs evidence) | `git cat-file -e <rev>:.ufo/waves/round-25/evidence/pressure-selftest.txt`; compare header `tool_blob`/`fixtures_tree` with `git rev-parse <R>:tools/mori-pressure.py`, `<R>:tools/fixtures/mori-pressure` and the same at head | file absent → red | R = `ec840f9d` (ancestor); tool blob `5785c5b2` and fixtures tree `c28ccfdf` equal at R, header and head; `exit: 0`; body is exactly the two lines SCORECARD:1514 claims → held |
| D2 (entry banner vs body) | Python over `git show <rev>:corpus/knowledge/system-pressure-r24.md`, emphasis stripped, whitespace folded, split at `## ` headings | outside corrections: `refreshed on (each\|every) read` 1, `spike…invisible` 1, `null…means…undefined` 1; `this section wins` 1 (whole entry); `only when the next` 0, `not tracked` 0; `(k4)`+`total` row 0 → red | 0, 0, 0, 0; 1, 1; 1; one corrections heading, Facts and Decision table present → held |
| D3 (round-24 lesson vs SCORECARD:1521) | `git show <rev>:corpus/lessons/round-24.md \| grep Correction \| grep S07`; case count at `4f05dd5a` via `jq '.cases\|length'` | no line → red | line 100 carries `Correction`, `S07`, `PASS 7/7`, `4f05dd5a`; file has 7 cases → held |
| D5 (Axes table vs round-24 scores) | `git show <rev>:SCORECARD.md \| sed -n 8,16p` vs `sed -n 1497,1508p` at base | coverage 5, operability 6, depth 4 differ from 6, 7, 5 → red | 6, 7, 5, 5, 5, 6, all equal; rows still reading `round 1` (freshness, calibration, adjacency) keep their round-1 scores → held |
| D4 hygiene (not counted) | `git show <rev>:.gitignore`; `git ls-tree -r --name-only <rev> -- tools \| grep -c 'pyc\|__pycache__'` | no rule → red | `tools/__pycache__/` at line 3; 0 tracked under `tools/` (212 tracked `.pyc` elsewhere stay tracked, which is why the rule was narrowed) → held |

Result: 4 → 0, matching the report. Re-checked also against the original `7634be75` predicates (D1–D4,
`items 4`): all four hold at the head too, so the A1/A5 amendments did not decide the outcome. Order check:
A1 (07:05) preceded the C1 tool (07:44:02); A5 (07:54:12) widened the claim after the 3-of-3 result and 40 s
before the Axes-table fix `e68855d5` (07:54:52); A4 (`9b1a2f12`, 07:44:17) landed 15 s after the tool, so the
lesson header's "A1–A4 preceded their code" is wrong for A4.

**Width ruling:** the statement ("repair the round-24 routed defects and the standing SCORECARD Axes table") is
wider than the counter. D5 checks scores and the `round 1` rule only; the head Axes row for operability credits
"round 13 (6 → 7)", but MANIFEST records mori round 13 `rejected-harmed` and round 14 `admitted`. D2 and D3
are lane self-records outside SCORECARD/SHONEN (disclosed). The counted value verifies; the prose excess is
routed (R4).

### C2 — coverage: `tools/mori-job-runway.py`, PASS 21/21 on frozen cases (before re-measured, after evidence-verified)

| Check | Command | Observed |
|---|---|---|
| before | `git cat-file -e 28b79d3d:tools/mori-job-runway.py` | exit 128 |
| cases frozen before the tool | `git rev-parse 7634be75:<cases> 829d8c90:<cases>`; `git log 28b79d3d..829d8c90 -- <cases>`; `git log --diff-filter=A -- tools/mori-job-runway.py` | both `48df844a…`; only `7634be7` (06:49:49) touches it; tool added `09f55b6` (07:02:38); `jq` 21 cases J01–J21 |
| committed evidence | `git show 829d8c90:.ufo/waves/round-25/evidence/runway-selftest.txt` | `revision: d3b7af2a…` (ancestor), `tool_blob 239dd8eb…` = blob at d3b7af2a = blob at head, fixtures tree `eddd10fb…` matches, `exit: 0`, `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` |
| live run | `runway-live-run.txt` | same revision and blob; configured `set` above the clamp, clamp `found 100 sites 1`, setting default `found 100`, effective 100, `RUNWAY_CLAMPED`, exit 1 — consistent with this session's own refusal threshold of 100 jobs |

**Does the after-value hold given the 72 broken configs?** The declared after-value holds: it is a tally over
the 21 frozen cases, and none of the 72 forms is among them (RunwayAndSkill: all 21 are block-style or the J20
inline form, which reads `malformed`). The 72 come from wave-2 ReviewRunwayCode's 307-config probe against
Bun 1.4.3 (62 quoted/escaped/anchored `async` headers, 10 flow-child, flow-root or indented-root forms). Code
reading at the head confirms the mechanism: with no exact column-0 `async:` line, or no exactly spelled
`maxJobs:` child, rule 1 yields `absent`, rule 5 `RUNWAY_DEFAULT`, exit 0, effective 100, where omp reads 50.
The tool obeys its frozen rule 1; the rule contradicts A2's own principle ("must abstain on forms it cannot
read the way omp does"). The probe script is not committed, so "72 of 307" is evidence-cited, not re-derived;
the mechanism is confirmed. The knowledge entry marks the defect (decision-table row "No `async:` block…",
"a false number … a known tool defect for round 26"; Limits "The config reader is a line grammar, not YAML").

**Width ruling:** the statement is wider than the counter. The counter measures agreement with 21 L1-written
examples (the lane says so in SCORECARD); the SCORECARD capability row says the tool gives "a verdict that never
turns an unreadable, ambiguous or unparseable input into a number", which the 72 forms contradict, and that row
is not marked. The capability is shown running correctly on this host's block-style settings file, so coverage
moves; the "never" clause is routed (R1, R2).

## Disclosed harm — retention scan 4 → 88 → 4 (re-measured)

RetentionHarm re-implemented the frozen policy's nine classes (`.ufo/waves/round-18/frozen/c1-policy.json`,
sha256 matches the receipt header) as a Python regex scan over `git ls-tree`/`git cat-file` blobs with the
contemporaneous allowlist, printing counts only:

| Revision | Unallowlisted hits |
|---|---|
| `28b79d3d` | 4 (all in the pre-existing round-20 fixture `.ufo/waves/round-20/falsify/NoHarmRun/…/c1-policy.json`) |
| `07a31ae8` | 88 (80 operator-config path/line references, 2 routing-key, 2 session-store-path class, 1 session identity, 1 session-record field, 2 other policy classes) — reproduces the reported 88 |
| `829d8c90` | 4 (the same four fixture lines, byte-identical; 0 in round-changed files) |

The 14 allowlist rows added this round are name-only (surface paths, key names, 40-hex blob ids; no values).
The receipt `evidence/retention-scan-after-repair.txt` names `98fd5b08`; the head tree differs from it by six
late wave-2 reports, and the head re-scan still gives 4.

**Ruling: no axis is harmed at the head** (adjacency 4 → 4). The round-17 precedent (`rejected-harmed`) turned
on private material retained at the tip; here it was removed at the tip within the round.

**Earlier pushed commits (kinds only, no material reproduced).** `origin` is a public GitHub repository and every
carrier is reachable from `origin/master`. Between `7634be7` and `f137046` (redacted by `86477e8`, `098d1a5`,
`98fd5b0`), history holds: about 80 lines of operator settings-file path and line-number references, including
file-listing metadata and grep excerpts of that file; copied values of four settings keys; a key-layout listing
with line offsets (10 keys); routing-key name mentions; one session identifier, one session-store path and one
session-record field (introduced `9ec786e`). A sweep of all added and removed lines in the 45 round commits for
API-key, token, bearer, cookie, password and `op://` patterns found **0 credential or secret values**.
**History disposition is needed and is the operator's decision** (with kagi for the exposure assessment, as in
round 17): accept and document the metadata-grade exposure, or authorize a rewrite. This closure rewrites
nothing and recommends no force-push on its own authority.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 4 → 0 re-measured; three wrong Axes scores corrected; new uncounted residuals routed (R4) |
| coverage | improved | C2 capability shown running; FR15 new ground; bounded to block-style single-file configs (R1, R2) |
| adjacency | unchanged | retention scan 4 → 4 at the head; mid-round 88 repaired in-round; history to operator |
| depth | unchanged | not claimed, held 5; the new SKILL block adds grounded rows but row 2 is over-scoped (R3) |
| operability | unchanged | not claimed, held 7; two new tools lack registry rows, the C1 tool lacks a self-test (R5) |
| freshness | unchanged | not claimed, held 5; the system-pressure-r24 rewrites are counted under the quality trend |

## Discernment spot-check (step 3)

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S099 oh-my-pi `sdk.ts` @ `45c35e40` | admit (A, mined) | raw.githubusercontent.com …/sdk.ts — HTTP 200, 255,525 B, sha256 equals the row | agree | line 2284 `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),` and the `parentTaskPrefix` guard at 2282; Gate quote 6 words, located, verbatim |
| S103 oh-my-pi `docs/tools/eval.md` @ `45c35e40` | admit (A, mined) | raw …/docs/tools/eval.md — HTTP 200, 28,027 B, sha256 equals the row | agree | line 258: "counted against the session-wide `async.maxJobs` cap (default and maximum 100)"; Gate quote ≤25 words, located, verbatim |
| S110 oh-my-pi issue #14636 | reject (C) | api.github.com …/issues/14636 — HTTP 200, open, created 2026-10-06T20:23:29Z | agree | the body pairs the module fallback 15 with "up to 100", the wrong-default risk the rejection names; 0 comments, so the flip condition (maintainer rationale) is unmet |
| S105 oh-my-pi-termux README | reject (C) | raw README.md @ main — HTTP 200, 5,518 B, sha256 equals the row | agree (partial) | 0 hits for `maxJobs` or "background job" in the README; the row's "in any file" was not re-verified (GitHub tree API rate-limited) |

New-row quote check: S099 and S103 above (both ≤25 words, located, verbatim). Gate completeness: 16 of 16 new
rows S098–S113 carry a Gate line (URL or, for S102, a local binary locator; access date; quote and location or
an honest "none" for rejects; S109 unopenable, HTTP 521). Census exit 0.

## Report addenda (eight) — checked

| Addendum | Claim | Check | Result |
|---|---|---|---|
| 1 (late finding) | retention 4 → 88, all 84 new in round-25 files | independent re-scan | reproduced (88; class split above) |
| 2 (repair) | 4 at the repaired tip; 14 name-only allowlist rows | re-scan; allowlist diff | reproduced; rows name-only |
| 3 (final tip `e0591e48`) | ReviewRunwayCode: 72 of 307 false absents | `w2/ReviewRunwayCode.md` (added `f137046`); tool code | mechanism confirmed; count evidence-cited (probe not committed) |
| 4 (correction) | addendum 3's "all 38 returned" false; ReviewSkillPattern: SKILL block broken | upstream re-open: `eval/agent-bridge.ts:210`, `task/workpool.ts:175,363` register without a capacity check; S103 line 258 | honest correction; row-2 contradiction confirmed (R3) |
| 5 | ReviewRoutedCode fail-open paths; the SCORECARD D5 note is wrong | `round-24.md:79-80` still say `PASS 6/6` beside the appended correction; `SCORECARD.md:1584` "D5 checks scores only, not … Last change" vs contract A5's `round 1` rule | confirmed (R4, R5) |
| 6 | ReviewD2Sweep held; lines 143 and 158 imprecise | D2 re-measurement above; the line-143 text exists at base line 137 | confirmed; pre-existing, not introduced |
| 7 | A4 15 s after the tool; U1 "only the default moved" wrong | commit times 07:44:02 / 07:44:17; U1 text at entry lines 266-271 | timing confirmed; U1 text present (R7) |
| 8 | 38 of 38 wave-2 seats returned; MutRoutedD1 held with gaps | `ls-tree w2/` = 38 reports; MutRoutedD1 added at `829d8c90` | confirmed; gate release is a harness ledger fact, not checkable from committed bytes |

## Trend verdicts

- **Expansion: improved.** `corpus/knowledge/harness-job-capacity-r25.md` is new ground (FR15, new coverage-map
  row in `corpus/README.md`); its `source:` cites S098–S104 and S112–S113, all `mined`, tier A, opened this
  round. Registry 97 → 113 rows (+9 admitted, +7 rejected), census exit 0. Two SCORECARD capability rows, both
  shown running in committed evidence. Its known false-number limit is marked in the entry, so the entry does
  not fail the bar it was admitted under.
- **Quality: improved.** The round-24 admitted entry `system-pressure-r24.md` had its K5, K4, P3, K3 and P4
  statements corrected in place and its "this section wins" banner removed (D2 re-measurement above;
  ReviewD2Sweep re-opened v7.2 `psi.c`/`psi.rst`). Its remaining imprecisions (lines 143 and 158, the
  `psi.c:1538-1550` range) were present at base and are routed, not left unrecorded.
- **Discernment: improved.** The outside spot-check agrees with the gate on two admits and two rejects.
  QUALITY 76–77 each cite a lesson (`round-24-verifier-spotcheck.md:137`, `:138-143`). Wave 2 corrected the
  S101 overclaim before the report. Mistakes M1–M4 are mined with fixes.

## Routed defects (the lane fixes these in round 26; this note changes no target)

- **R1 — C2 false numbers.** `RUNWAY_DEFAULT`, effective 100, exit 0 for configs omp reads as 50 (quoted,
  escaped or anchored `async` headers; flow children, flow roots, indented roots). Make rule 1 abstain
  (`RUNWAY_UNKNOWN`) on any top-level form it cannot read the way omp does, and commit the probe corpus as
  fixtures so the count can be re-derived. Also from ReviewRunwayCode: `set` for files Bun refuses to parse;
  `--selftest --cases ""` silently runs the frozen cases; uncaught exceptions exit 1 (the `RUNWAY_CLAMPED`
  code); no guard on FIFO or `/dev/zero`; untested CLI exit and unreadable-binary paths.
- **R2 — SCORECARD capability row overclaims.** "never turns an unreadable, ambiguous or unparseable input into a
  number" is false until R1 lands. Append a scoped correction (block-style, single settings file).
- **R3 — SKILL round-25 block.** Row 2 ("a bash or eval call … while the cap was full → nothing") holds only for
  auto-backgrounded calls; eval `agent()`, `workpool()` and explicit `async: true` bash refuse (S103 `eval.md:258`;
  upstream `agent-bridge.ts:210`, `workpool.ts:175,363`). Row 3 lists too few refusing paths, row 4 lacks the
  false-number caveat, and the retention repair garbled row 1's host sentence.
- **R4 — SCORECARD calibration residuals.** The Axes operability row credits round 13 (rejected-harmed); 7 was
  first admitted in round 14. The note at `SCORECARD.md:1584` misstates D5's Last-change rule. The round-12 line
  at `SCORECARD.md:620-621` is left stale by the D5 rewrite.
- **R5 — gate conformance.** Add registry rows for `tools/mori-routed-r24.py` and `tools/mori-job-runway.py` at
  the registry home (`SKILL.md`). Give the routed check a committed self-test. Close its fail-open paths: D1
  compares the body with a constant (only `--rerun` detects a forged PASS); D5 reads columns by position; D2
  skips headings; D3 holds beside the uncorrected `PASS 6/6` line; a missing baseline exits 1, not 2; a
  promisor clone gets objects written; a sub-directory `--repo` changes results.
- **R6 — lesson wording.** In `corpus/lessons/round-25.md`: "100, whatever the config says" is false below 100;
  "only registration paths throw" omits `agent()`; the A1–A4 ordering claim (A4 came 15 s after the tool, A5 is
  unlisted); the shadowed round-26 Axes bullet breaks QUALITY 77; the refusal-count wording.
- **R7 — knowledge corrections.** `harness-job-capacity-r25.md` U1 ("only the default moved"; the "(1-100)"
  description was removed 2026-05-03 and the clamp rewritten 2026-09-24) and the mis-cited F10 parenthetical.
  `system-pressure-r24.md` lines 143 and 158 and the `psi.c:1538-1550` range.
- **R8 — no-harm check.** Run the retention scan over the real tree at every candidate tip, not only the gate's
  self-test. History disposition of the earlier pushed commits goes to the operator (with kagi); the lane takes
  no rewrite action.

Sentinel note for the orchestrator: the lane reports that the three-rounds-running routed-repair sentinel is
tripped (rounds 23–25 each counted a routed repair on calibration), so round 26 must work a different frontier
area; R1–R8 ride as corrections, not as the counted claim.

For the operator (promotion is operator-owned): SHONEN box 2 (an end-to-end task logged in `LOG.md`) looks
checkable by a non-author (`LOG.md` round-25 outcome plus `evidence/runway-live-run.txt`). Box 1 is not
certifiable while R3 stands.
