# RevPromptHonesty — w1 plan ↔ round-contract conformance (mori round 48, wave w1)

Scope: conformance of the wave-1 plan (`w1-dispatch.json`, 49 seats; spec source `w1-spec.json`) to
`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-48.md` §2, §2b, §4 and the frozen contract
`.ufo/waves/round-48/contract.md` (commit `4387cf94b69ddce455051a1ff38e93795c2e6cde`, parent =
entering tip `e5dbac05459887d9597ea5d1da0d8e3d024e0d17`; verified: `git log -1 --format='%H %P %s' 4387cf9`).
Method: read the prompt sections, the contract, `v3-spec.md`, all 49 item prompts (spec + dispatch),
all receipts under `evidence/`, SCORECARD.md, SHONEN.md; read-only git; sha256 comparisons against
`evidence/freeze-sha256.txt`; census re-run. Leaf seat, no subagents, no tool installs
(tooling authorization of 2026-10-19 unused; pacman untouched).

## Requirement matrix

| # | Requirement (contract line) | Status |
|---|---|---|
| 1 | 1–3 claims, each on a distinct axis (prompt §2.2; contract header "Active scores entering…") | **Satisfied-by-plan.** Exactly 2 claims in the wave context: C1 → calibration, C2 → depth. Verified in SCORECARD.md Axes table: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. |
| 2 | ≥1 claim on the lowest non-retired axis; no waiver (prompt §2.2; contract "Both claims work a lowest axis; no stagnation waiver is used") | **Satisfied-by-plan.** Both claims work tied-lowest axes (depth 5, calibration 5; freshness 5 also lowest and untouched — allowed, "at least one"). |
| 3 | Claims causally separable (prompt §2.3; contract §Separability) | **Satisfied-by-plan** at item level: C1 items touch scratch copies of `tools/mori-pin-check.py` + fenced SKILL/registry drafts; C2 items touch corpus drafts only; no item writes the other claim's surface. **Landed separability is satisfied-only-when-done**: w2/L1 must actually run "either counter with the other claim's changes reverted" at landing. |
| 4 | Falsifiable before→after with pasteable counting commands (prompt §2.4; contract P-C1/P-C2 "Counting command") | **Satisfied-by-plan for befores** (receipts verified, see #9); **satisfied-only-when-done for afters** — L1 runs `count-c1.py --tool <landed tool> --rev R` → `C1=met` and `count-c2.py R` → `C2=met … N≥8 S≥3` at the landed tip and pastes both. |
| 5 | Per-claim SCORECARD record (delta, evidence, command, measured commit) + LOG append (prompt §2.5) | **Satisfied-only-when-done.** Drafts exist in plan (ScribeScorecard: `## Round 48` declaration with real before-lines from `evidence/`, After column pinned as "to be measured at the landed tip"; ScribeLogErratum: LOG head + r47 erratum). L1 fills After, delta and measured commit at integration. |
| 6 | Capability acquisition runs, verifies, enters capabilities table same round (prompt §2.6) | **Satisfied-only-when-done.** count-c1.py junk-variant counter: selftest receipt already frozen (`C1_SELFTEST pass=34 fail=0`, evidence/selftest-c1.txt). mori-unlanded-check.py: ExecUnlandedCheck must show its selftest green. Capability rows (drafted by ScribeScorecard) enter the table only at L1 integration. |
| 7 | Retire/split axes with reason (prompt §2.7) | **Not triggered** — no claim requires it; SCORECARD Retired: None. No action required by the contract this round. |
| 8 | ≤1 exploratory claim, named reviewer (prompt §2.8) | **Satisfied-by-plan** — zero exploratory claims declared (≤ cap). ConnCrossClaim's QUALITY sentence proposal rides C1/C2 quality work, not an exploratory claim. |
| 9 | Controls built and scored **before data** (contract C1 "Controls… each must stay unmet", C2 "Controls", freeze preamble) | **Satisfied — verified in repo state.** Freeze commit `4387cf9` (2026-10-25 17:53:38 -03) contains contract, both counters, v3-spec, 3 controls, all 8 receipts, 4 source copies; dispatch written 17:53:45, seats started 18:32:59 (`w1.ready.dispatched` mtime). Receipt contents match the contract's semantics: entering tool `C1=unmet junk_met=8 honest_unmet=0 real=met` (do-nothing); stub-always-met green on junk → unmet; stub-always-unmet `honest_unmet=4 real=unmet` → unmet; C2 do-nothing `C2=unmet … failed=entry_absent,pins`; selftests `pass=34 fail=0` (C1) / `pass=22 fail=0` (C2). Working-tree bytes of all frozen instruments matched `freeze-sha256.txt` at read time (see Finding F1 for the one exception and its repair). |
| 10 | Census before → after, both outputs + exit codes, exit 0 at round end (prompt §2b.2; contract "Census … at round start … and round end") | **Before satisfied**: `evidence/census-start.txt` frozen (19×W04 + 1 `ok`); I re-ran `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0, content-identical lines (scratch copy `.scratch/r48-RevPromptHonesty/census-recheck.txt`). **After satisfied-only-when-done** — L1 round-end re-run, both outputs + exit codes pasted in the report. No w1 seat is tasked with it (correct: L1 duty). |
| 11 | One mined mistake, fix shown able to fail (prompt §2b.3; contract "Mistake: round-47 routed defect 1 … with a fix that is shown able to fail") | **Satisfied-by-plan**: ScribeMistakes M1 = routed defect 1 (late seat results never committed; `landing` class) + M2 (frozen v1 scorer green on junk); fix = ExecUnlandedCheck's `mori-unlanded-check.py`, whose item **requires** the able-to-fail demonstration (sandbox repo with an untracked w2 result and a modified tracked report → "exits 1 with the file named", then green). **Shown only-when-done** (seat's selftest output + L1 landing). |
| 12 | ≥1 sourced claim citing a SOURCES row opened this round (prompt §2b.4; contract P-C2) | **Satisfied-by-plan**: C2 rests on S479–S482; four row scribes (ScribeRowXfs/Quotactl/Errno/Aliyun) each open the committed copy AND fetch the live URL, `status mined`, `opened 2026-10-25`, `used-by` the entry; collision/renumber evidence verified (lane registry max id = S478 in `assimilation/reg-ids`; staged quota rows S477–S482; `assimilation/collisions` lists the full staged∩lane set S471–S478). **Lands only-when-done**: rows appended + entry landed + `count-c2.py R` prints `C2=met` at the landed tip. |
| 13 | Assimilation: 1 theme, Gate admit/reject per entry; 3 quarantine hand-checks; considerthese as lesson + QUALITY criterion (contract "Frontier step, assimilation, mistake") | **Satisfied-by-plan**: theme = FR2 quota (staged entries all read by ScoutStagedQuota; ScribeLessonGate drafts `## Gate` with admit/reject per entry); ScoutQuarantineS244/S262/S268 each hand-check one row; ExecPortability implements considerthese/2026-10-25.md suggestion 2 as a counting command, ScribeQuality criterion (c) carries it. Lands only-when-done at integration. |
| 14 | Report at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/mori.md`, six sections in order, marker rule (prompt §4) | **Satisfied-only-when-done** — L1 round-end duty. w1 supplies every input: item reports with evidence pointers (Work performed), LOG head draft (Landed changes), receipts + landed measurements (Before→after), census + row work (Sources & frontier). Trend verdicts and SHONEN lines are written at report time. |
| 15 | SHONEN rule: one line per box, `[x]` only with named non-author verifier (prompt §4) | **Satisfied-only-when-done.** `SHONEN.md` exists at lane root (4 boxes). No w1 item names a verifier — correct sequencing: w2 attack seats and the round-end non-author closure are the candidate verifiers; without a named non-author, boxes must land `[ ]`/`[~]`, never `[x]`. |
| 16 | Round shape: two v1 waves 32–64 each, total 64–100; §3 role floor; godspeed lead; no planner role (contract §Round shape; prompt §3, §6) | **Satisfied-by-plan**: w1 = 49 seats (validated under `ufo-wave-policy.json`: waveMinLanes 32, waveMaxLanes 64; dispatch `counts spawn=49`). Roles: executor 13, scribe 13, scout 6, critic 6, reviewer 4, mutation-tester 3, connector 2, sentinel 1, simplifier 1 — §3 minimum split met (connector/executor/scribe/scout/reviewer/critic all ≥1); planner absent from items (L1 holds the canonical §3 seat per the 2026-10-19 ruling — the mapping must be recorded in the round report, **only-when-done**). All 49 prompts lead `/skill:godspeed`; all 49 dispatched prompts carry lane bounds + a `Report:` path under `.ufo/waves/round-48/w1/`. Attack share 14/49 ≈ 29%. |
| 17 | Leaf bounds honored in plan text: candidates in scratch, no production edits, read-only fleet | **Satisfied-by-plan in text; violated in execution — see F1.** Every C1 implementer is told to copy the tool into its own scratch and "implement … in that copy only"; every scribe drafts fenced, not in place; dispatch bodies are byte-identical to spec bodies (diff = appended trailer only, all 49 names aligned). |

## Findings by severity

### F1 — HIGH — production instrument `tools/mori-pin-check.py` was overwritten mid-wave, four times in ~80 seconds; restored to frozen v2 bytes

Observed timeline (all commands read-only; sha256 + `stat` + `git diff`):

| instant (-03) | tools/mori-pin-check.py | evidence |
|---|---|---|
| 18:35:28.757523563 | 34159 B, sha256 `3e634b30…`, v3-shaped (`is_selftest_header`, `HIDDEN_RE`, `tally_prefix`+NFKC, `TRUNC_HEX_RE`, `TIMEOUT_S`) — same size and same nanosecond mtime as `.scratch/r48-ExecV3ImplA/mori-pin-check.py` (cp -p signature) | `ls -l`, `git diff --stat` (84+/47−) |
| 18:35:43.787790237 | 32259 B (v2-sized), sha not captured at this instant | `ls -l` |
| ~18:36:30 | 33505 B, sha256 `95b27dd0…` | `sha256sum`, `stat` |
| 18:36:50.824795541 | **32259 B, sha256 `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` = frozen v2** — current state | `sha256sum` + `stat` |

- Violates the wave rule every seat received: "never edit … tools/ … A candidate tool lives in your scratch, never in tools/". Writer not attributable from bytes; the 18:35:28 state is byte-size/mtime-identical to ExecV3ImplA's scratch candidate, but that scratch has since been overwritten too (its current sha `1154f304…`), so attribution is UNVERIFIED.
- Contract consequence is already handled by design: freeze preamble — "If the working-tree bytes ever differ, the claim is measured with `git show <freeze>:<path>`." All frozen instruments verified back at manifest bytes after 18:36:50; `corpus/`, SKILL.md, SOURCES.md, LOG.md, SCORECARD.md show no mid-wave drift (`git status --porcelain` on those paths: empty).
- Concrete contamination risk: ExecSkillRowsRun measures by running the **production path** `python3 …/tools/mori-pin-check.py --rev e5dbac05 …` for its before-state re-measurement. If it executed inside 18:35:28–18:36:50 it measured non-v2 bytes. Its report must state the on-disk sha it measured (or be re-run); otherwise treat that item's before-tally as UNVERIFIED.
- Recommended for the L1 at integration: record the churn in the report, re-verify `sha256sum tools/mori-pin-check.py` == `9832e38c…` before any landed-tip C1 measurement, and score the claim from `git show 4387cf9:tools/mori-pin-check.py` / `controls/tool-v2-entering.py` bytes only.

### F2 — LOW — `evidence/census-start.txt` does not record its exit code

The contract asserts "(evidence/census-start.txt, exit 0, 20 lines of output with 19 W04 warnings plus one ok)". The frozen file carries the 20 content lines but no rc. Reproduced today: `TMPDIR=<scratch> sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0, lines 1–20 byte-identical to the receipt, final line `mori	ok	…/corpus/SOURCES.md` (both files show 21 by `wc -l` due to one blank line; content identical). Evidence-completeness defect in the receipt, not in the plan; round-end census must paste outputs **and** exit codes per prompt §2b.2.

### F3 — INFO — `w1-spec.json` is not the dispatched text

Dispatched prompts = spec body + appended "\n\nLane bounds: leaf member …\n\nReport: write your scoped findings to .ufo/waves/round-48/w1/<Name>.md". Verified: all 49 names aligned, every diff is the appended trailer only. Any post-hoc audit must read `w1-dispatch.json` (authoritative); `w1-spec.json` alone omits the seat rules and report paths.

### F4 — RESIDUAL — w2 sizing constraint

Round total must land in 64–100 (run-7 directive; contract §Round shape "Total within 64-100"). With w1 = 49, w2 must be 32–51 distinct attack seats with ≥32 genuine items. Feasible; an L1 dispatch-time duty, not a w1 defect.

## Residual risk and verification gaps

- F1 writer identity: UNVERIFIED (bytes only; both candidate scratch copies have since changed).
- Whether ExecSkillRowsRun (or any other seat) executed a production-path measurement inside the churn window: UNVERIFIED until seat reports land.
- Landed-tip values (`C1=met`, `C2=met`), census-after, SCORECARD deltas, capability rows, report sections and SHONEN verifiers: pending by design — each is named above as satisfied-only-when-done.
- Entering-tip sweep receipt `evidence/sweep-quota-rows.txt` (contract cites it for "no user-space quota surface") was not independently re-executed by this seat; its presence in the freeze commit is verified.

No tooling installed or upgraded (authorization unused); no pacman use; no credential material encountered; all commands read-only.
