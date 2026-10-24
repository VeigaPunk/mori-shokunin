#!/usr/bin/env python3
"""Generate the round-37 v2 wave spec (one wave, build + attack) next to this file.

Run: python3 .ufo/waves/round-37/gen-wave-spec.py
Writes: .ufo/waves/round-37/w1-spec.json
"""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
W = LANE + "/.ufo/waves/round-37"
TIP = "e57c58b57c025364e79d130fbdf764d2674d83d6"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""

CONTEXT = f"""# mori round 37 — one v2 wave (build + attack), L1 MoriR37

Lane repo: {LANE} (jj-colocated; git is the backend). Fleet repo: {FLEET} (read-only for you).
Scored tip under attack: {TIP} (pushed). Entering tip: 842a32074b5c7972e9728f3f629d83eb92f127c2.

## Claims under attack
- C1 (calibration, measured): `python3 .ufo/waves/round-37/count-c1.py {TIP}` — the C2 gate
  measurement must reject a real-arm memoizer and a summary-only printer while the honest gate
  passes blind (24 run-time histories), real (lane history, rev 6bd57097 / base f10a320d) and
  challenge (real-arm clothing) arms. Predicate P-C1 is verbatim in `{W}/contract.md`; receipts
  `{W}/evidence/c1-before-memo.txt`, `c1-before-summary.txt`, `c1-after.txt`; counter blob pin in
  `{W}/evidence/freeze-r37.txt`.
- C2 (freshness, measured): `python3 .ufo/waves/round-37/count-c2.py {TIP}` — the drift probe's two
  fetch policies (4 MiB bounded read; post-redirect public-destination check) are named, each killed
  by its own mutation, and the corpus binds them. Receipts `{W}/evidence/c2-before.txt`,
  `c2-after.txt`, `drift-live-r37.txt`; arms `tools/mori-source-drift.py --selftest` (6 cases).
- Frontier step: SOURCES rows S221–S225 opened this round (copies `corpus/evidence/sources-r37/`),
  knowledge entry `corpus/knowledge/source-drift-hardening-r37.md`, lesson
  `corpus/lessons/round-37.md` (Gate + M1–M4), QUALITY 106/107.
- Routed r36 debts: (d) `tools/mori-round17-jj-regressions.py` side-effect assertion scoped — see
  `{W}/evidence/r17-jj-selftest-r37.txt`; (e) repo-relative paths in new evidence; (f) `tool_timeout`
  boundary; (g) mkdtemp scratch; (h) nine-row drift prose.

## Hard bounds (every seat)
- Write EXACTLY ONE file: your report at {W}/w1/<YourName>.md . The `Report:` trailer path is
  relative to {LANE} — write it at {LANE}/<that path>. Scratch code/outputs only under
  /fast/scratch/hyaku/mori-r37/<YourName>/ or $TMPDIR.
- The lane repo is READ-ONLY for you: never `git add/commit/push/fetch/reset/stash`, never any
  mutating jj command, never edit lane files. Running the lane's read-only tools and counters is
  fine; mutation-testers run COPIES under their own scratch — never edit the lane's real files.
- Never touch: {FLEET}/MANIFEST.json, {FLEET}/.ufo/state/, {FLEET}/.ufo/watchdog.log,
  {FLEET}/templates/, {FLEET}/scripts/, sibling lane repos, ~/.omp/agent/config.yml,
  ~/.omp/agent/mcp.json.
- No remediation, no kills, no config edits — detection and report only (mori province).
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task via
  official channels (uv tool / npx / official binary into ~/.local/bin) and MUST record any
  install — tool, version, channel, reason — in your report. pacman guard (orchestrator
  2026-10-20): ALL pacman transactions are PAUSED host-wide; never run pacman. Never pass a model
  parameter; never call the `ask` tool.
- Every measurement in your report carries its command and observed output. End with `VERDICT: PASS`
  (no defect found) or `FAIL` (defect, with path:line evidence). Name what your item attacks.
"""


def item(name, role, task):
    return {"name": name, "role": role, "prompt": GODSPEED + task.strip() + "\n"}


ITEMS = [
    # ---------------------------------------------------------------- reviewers (10)
    item("RevC1Predicate", "reviewer", f"""
# Target
Re-measure C1 with three fresh seeds and check the predicate bytes.
cd {LANE} && for s in 41 42 43; do python3 .ufo/waves/round-37/count-c1.py {TIP} --seed $s; echo EXIT=$?; done
# Acceptance
Report each run's blind/real/challenge/negative lines and exit code. Verify the first printed line is
byte-identical to the P-C1 sentence in {W}/contract.md (diff the strings; report any difference).
VERDICT: PASS iff all three runs print C1=met, exit 0, and the sentence matches.
"""),
    item("RevC1Challenge", "reviewer", f"""
# Target
Attack the challenge arm's clothing: is it genuinely distinguishable from the blind sandboxes by a tool
that inspects its environment? Read `challenge_arm` in {W}/count-c1.py. Then write a probe tool in your
scratch that prints its repo path, `git config --local user.name`, the first line of corpus/SOURCES.md,
and its parent cmdline; run the counter with `--tool` pointing at that probe on seed 11.
# Acceptance
Report what a tool can see about the challenge repo vs the blind repos. State whether any surviving
signal would let a memoizer tell the challenge from the blind arm. VERDICT: PASS iff the challenge repo
path, identity and title match the real-arm clothing and the probe shows the blind arms differ on all three.
"""),
    item("RevC1Negatives", "reviewer", f"""
# Target
Re-run each negative fixture alone against the counter and verify the rejection names the intended arm.
for f in memo-n1 const summary-only; do python3 .ufo/waves/round-37/count-c1.py {TIP} --tool
{W}/fixtures/$f.py --seed 11; done
# Acceptance
Report each run. memo-n1 must be rejected by the CHALLENGE arm (its real and blind arms pass);
summary-only must be rejected by the per-id check on the blind arm; const must be rejected by the blind
arm. VERDICT: PASS iff each rejection detail names the arm you expect.
"""),
    item("RevC2Arms", "reviewer", f"""
# Target
Re-run the drift selftest and both mutations by hand.
cd {LANE} && python3 tools/mori-source-drift.py --selftest; echo EXIT=$?
Then copy the tool to /fast/scratch/hyaku/mori-r37/RevC2Arms/ and apply each mutation
(`FETCH_MAX_BYTES = 4 * 1024 * 1024` -> `1 << 40`; `if not _public_redirect_target(final):` -> `if False:`),
run `--selftest` on each copy.
# Acceptance
Report all three outputs. The unmutated copy must PASS 6 cases; each mutant must FAIL exactly its own
named arm and exit 1. VERDICT: PASS iff all three hold.
"""),
    item("RevC2Docs", "reviewer", f"""
# Target
Re-open all five new source rows against their committed copies.
For each of S221..S225 in corpus/SOURCES.md, locate the quoted phrase in corpus/evidence/sources-r37/<id>.src
at the row's anchor line range, and count the quote's words (<=25).
# Acceptance
Report row, anchor lines, whether the quote is contiguous at those lines, and the word count. Report any
row whose teaches sentence is not supported by the quote. VERDICT: PASS iff all five verify.
"""),
    item("RevC2Binding", "reviewer", f"""
# Target
Verify the C2 counter is not self-referential: it must check committed bytes at <rev>, not the working tree.
Read {W}/count-c2.py (`show`, `coverage_map`, `knowledge`, `capability`, `live` checks). Then run
`python3 .ufo/waves/round-37/count-c2.py e57c58b5` and again after `git -C {LANE} show e57c58b5:corpus/README.md | head -2`
to confirm what the counter reads. Also confirm a rev WITHOUT the entry (842a320) still fails.
# Acceptance
Report the commands and outputs. State whether the counter can pass on working-tree-only content.
VERDICT: PASS iff both revs behave as the contract says and no check reads the working tree.
"""),
    item("RevR17JJ", "reviewer", f"""
# Target
Verify the scoped r17-jj assertion still has teeth.
cd {LANE} && python3 tools/mori-round17-jj-regressions.py --selftest --scratch .ufo/waves/round-37/scratch-rev 2>&1 | tail -5
Then read the `jj_config_redirected` block in tools/mori-round17-jj-regressions.py and construct (in your
scratch, not the lane) a mutated copy whose census_env points XDG_CONFIG_HOME outside the case home; run
its `--selftest` and report whether the assertion fails.
# Acceptance
Report the lane selftest exit code and the mutant's result. VERDICT: PASS iff the lane run exits 0 and the
mutant fails the assertion (or the mutant cannot be built — say exactly why).
"""),
    item("RevTimeout", "reviewer", f"""
# Target
Attack the timeout boundary of {W}/count-c1.py. Write a fixture tool in your scratch that sleeps 300s,
run `python3 .ufo/waves/round-37/count-c1.py {TIP} --tool <sleeping> --seed 11`, and time it.
# Acceptance
Report wall time, the arm detail line, whether the state reads `tool_timeout` (not a list mismatch), and
whether any process survived. VERDICT: PASS iff the run reports tool_timeout and terminates within the
budget+grace.
"""),
    item("RevScratch", "reviewer", f"""
# Target
Attack scratch uniqueness and path discipline. Run two counters concurrently with the SAME seed
(`--seed 11`) in the background and compare to a serial run; inspect `_scratch_parent` and the
`mkdtemp` calls. Then check whether any lane-relative path is printed absolutely.
# Acceptance
Report both concurrent outputs, the scratch directories created, and any absolute lane path in the
output. VERDICT: PASS iff concurrent same-seed runs both complete (a collision yields exit 2, never a
wrong verdict) and lane paths print repo-relative.
"""),
    item("RevSHONEN", "reviewer", f"""
# Target
Check the round's SHONEN boxes and every evidence pointer in the lane.
Read SHONEN.md, then resolve each pointer the round report (once it exists at {FLEET}/.ufo/reports/round-37/mori.md)
cites: every `evidence/*.txt` path, every commit hash, every SCORECARD capability row.
# Acceptance
Report each pointer with resolves/absent. VERDICT: PASS iff every pointer resolves at the named rev.
"""),
    # ---------------------------------------------------------------- critics (6)
    item("CritC1Axis", "critic", f"""
# Target
Attack the axis choice for C1. Is "calibration" the right axis for a counter-hardening claim, or is it
operability? Read AXES.md definitions in {FLEET}/AXES.md and {LANE}/SCORECARD.md's Axes table.
# Acceptance
Argue both sides with the definitions quoted, then rule. VERDICT: PASS iff you agree calibration is the
surface the round changes (the lane's self-assessment of what its measurement proves); FAIL with the
better axis named otherwise.
"""),
    item("CritC2Axis", "critic", f"""
# Target
Attack the axis choice and sizing for C2: does verifying a hardening move freshness, or is it operability
(a tool's policies) and therefore not allowed to claim freshness?
# Acceptance
Name what the claim changes (a drift instrument's fetch policies and the corpus binding) and decide whether
"freshness" is the surface or the number. VERDICT: PASS/FAIL with the reason.
"""),
    item("CritClaimSizing", "critic", f"""
# Target
Try to build the cheapest control that meets P-C1 without doing the claimed work: a counter that adds only
the per-id check (no challenge arm), or only the challenge arm (no per-id check). You may write both in
your scratch by copying {W}/count-c1.py and deleting one half; run each against the negative fixtures.
# Acceptance
Report each control's verdict at {TIP}. VERDICT: PASS iff each half-control prints C1=unmet.
"""),
    item("CritC2ContentFree", "critic", f"""
# Target
Try to meet P-C2 content-free: (a) a knowledge entry with the right strings but no located quote;
(b) a capability row that names the tool but points nowhere; (c) a live receipt with the sentence but no
row lines. Build each in scratch and reason about which counter check catches it.
# Acceptance
For each shape name the check that catches it, or state that P-C2 admits it (a defect). VERDICT: PASS iff
every content-free shape fails at least one check.
"""),
    item("CritAdmission", "critic", f"""
# Target
Attack the admission bar. Compute the SCORECARD diff from the entering tip to the scored tip
(`git -C {LANE} diff 842a320..e57c58b5 -- SCORECARD.md`) and check that no axis score was rewritten and
that the new rows are additive. Also check the claims are causally separable: can C1 verify with C2's
changes absent and vice versa?
# Acceptance
Report the diff hunks and the separability argument. VERDICT: PASS iff no axis is harmed and each claim's
counter runs without the other claim's artifacts.
"""),
    item("CritDebtDisposition", "critic", f"""
# Target
Attack the r36 debt table in {W}/contract.md and in corpus/lessons/round-37.md: for each of (a)-(h) find
the artifact that closes it, or name it as not closed. Pay special attention to (f) the SIGKILL boundary
(is a disclosure enough?) and (e) path hygiene (is any new file absolute-pathed?).
# Acceptance
One line per debt: closed-artifact or open. VERDICT: PASS iff every debt is closed or honestly named open.
"""),
    # ---------------------------------------------------------------- mutation-testers (5)
    item("MutC1ChallengeRemoved", "mutation-tester", f"""
# Target
Mutate {W}/count-c1.py in YOUR scratch: make `challenge_arm` return `(True, ...)` without running the tool.
Run the mutant against `fixtures/memo-n1.py` and against the honest tool.
# Acceptance
Report both verdicts. The honest tool should still pass; the memoizer must now be ACCEPTED, proving the
challenge arm is load-bearing. VERDICT: PASS iff the mutation flips memo-n1 to accepted.
"""),
    item("MutC1IdGrammar", "mutation-tester", f"""
# Target
Mutate a scratch copy of {W}/count-c1.py: make `same_id_lines` always return True. Run it against
`fixtures/summary-only.py`.
# Acceptance
Report the verdict. summary-only must now be accepted on the blind arm (or another arm), proving the per-id
check is load-bearing. VERDICT: PASS iff the mutation flips summary-only to accepted.
"""),
    item("MutC2CapArm", "mutation-tester", f"""
# Target
Mutate a scratch copy of {W}/count-c2.py: drop the `cap_kill` check (or make it always PASS). Run it at
{TIP}. Also mutate the drift tool's cap anchor and confirm the arm FAILs when the real tool is mutated.
# Acceptance
Report both runs. The counter mutant must print C2=met while the tool mutant prints `selftest huge_cap FAIL`.
VERDICT: PASS iff the check is load-bearing in both directions.
"""),
    item("MutC2RedirectArm", "mutation-tester", f"""
# Target
Same as MutC2CapArm for the redirect policy: drop `redirect_kill` from a counter copy; mutate
`if not _public_redirect_target(final):` in a tool copy.
# Acceptance
Report both runs. VERDICT: PASS iff the arm is load-bearing in both directions.
"""),
    item("MutC2Knowledge", "mutation-tester", f"""
# Target
Mutate a committed copy of the knowledge entry in your scratch (remove the `S2##` citations and the
`8ff9bba` string), commit it in a throwaway clone of the lane, and run
`python3 .ufo/waves/round-37/count-c2.py <that clone's rev>` with `--repo`.
# Acceptance
Report the clone path, rev, and counter output. VERDICT: PASS iff `knowledge FAIL` and `C2=unmet` there.
"""),
    # ---------------------------------------------------------------- labrats (3)
    item("LabC1Concurrent", "executor", f"""
# Target
Probe one falsifiable hypothesis: two concurrent runs of count-c1 with the same seed never produce a wrong
verdict (either both meet or a collision exits 2). Run two in parallel, three times.
# Acceptance
Report the six runs' exit codes and verdict lines. VERDICT: PASS iff no run prints a verdict other than
C1=met/met or a setup error.
"""),
    item("LabTimeoutBoundary", "executor", f"""
# Target
Measure the timeout boundary precisely: a fixture that sleeps N seconds for N in {{TOOL_TIMEOUT_S-5,
TOOL_TIMEOUT_S+5}}. Read TOOL_TIMEOUT_S and TOOL_GRACE_S from {W}/count-c1.py.
# Acceptance
Report wall time and the state line for each N. VERDICT: PASS iff the below-budget run completes normally
and the above-budget run reports tool_timeout within budget+grace.
"""),
    item("LabC2CapMemory", "executor", f"""
# Target
Measure the cap arm's cost: peak RSS of `tools/mori-source-drift.py --selftest` (e.g. /usr/bin/time -v)
and the body sizes the arm serves. State the memory bound the 4 MiB cap actually enforces at the client.
# Acceptance
Report command, peak RSS, and the largest body served. VERDICT: PASS with the numbers; FAIL if the arm's
own fixture allocates more than the cap allows times a small constant.
"""),
    # ---------------------------------------------------------------- executors (20)
    item("ExecC1Seed41", "executor", f"""
# Target
cd {LANE} && python3 .ufo/waves/round-37/count-c1.py {TIP} --seed 41; echo EXIT=$?
# Acceptance
Paste the full output and exit code. VERDICT: PASS iff C1=met and exit 0.
"""),
    item("ExecC1Seed42", "executor", f"""
# Target
cd {LANE} && python3 .ufo/waves/round-37/count-c1.py {TIP} --seed 42; echo EXIT=$?
# Acceptance
Paste the full output and exit code. VERDICT: PASS iff C1=met and exit 0.
"""),
    item("ExecC1Seed43", "executor", f"""
# Target
cd {LANE} && python3 .ufo/waves/round-37/count-c1.py {TIP} --seed 43; echo EXIT=$?
# Acceptance
Paste the full output and exit code. VERDICT: PASS iff C1=met and exit 0.
"""),
    item("ExecC1ToolAbsent", "executor", f"""
# Target
Find the oldest rev in the lane that lacks `tools/mori-sources-appendonly.py`
(`git -C {LANE} log --diff-filter=A --format=%H -- tools/mori-sources-appendonly.py` then its parent) and run
`python3 .ufo/waves/round-37/count-c1.py <that rev>`.
# Acceptance
Paste output and exit code. VERDICT: PASS iff the tool_absent path prints `C1=unmet` exit 1 (not a crash).
"""),
    item("ExecC2Twice", "executor", f"""
# Target
Run the C2 counter twice at {TIP} and diff the two outputs.
cd {LANE} && python3 .ufo/waves/round-37/count-c2.py {TIP} > /fast/scratch/hyaku/mori-r37/ExecC2Twice/a.txt 2>&1; echo $?
(repeat into b.txt; diff a.txt b.txt)
# Acceptance
Report both exit codes and the diff. VERDICT: PASS iff both exit 0 and the diff is empty.
"""),
    item("ExecCensusStart", "executor", f"""
# Target
Run the frozen source census exactly as CORPUS.md specifies.
bash {FLEET}/scripts/sources-census.sh validate --root {FLEET} mori; echo EXIT=$?
# Acceptance
Paste the last five lines and exit code; compare with {W}/evidence/census-end.txt. VERDICT: PASS iff
exit 0 and `mori ok`.
"""),
    item("ExecDriftLive", "executor", f"""
# Target
Re-run the live drift sweep and compare to the committed receipt.
cd {LANE} && timeout 900 python3 tools/mori-source-drift.py --root . ; echo EXIT=$?
# Acceptance
Report the summary line and exit code; diff against {W}/evidence/drift-live-r37.txt. VERDICT: PASS iff the
summary line matches and exit is 1 or 0 (a network-unavailable row changes the counts — report it).
"""),
    item("ExecR17JJBattery", "executor", f"""
# Target
Run the r17-jj regression gate selftest from a scratch parent inside the allowed area.
cd {LANE} && python3 tools/mori-round17-jj-regressions.py --selftest --scratch .ufo/waves/round-37/scratch-exec 2>&1 | tail -3; echo EXIT=$?
# Acceptance
Paste the tail and exit code; confirm `jj_config_redirected` appears in the ok list. VERDICT: PASS iff exit 0.
"""),
    item("ExecCensusRegression", "executor", f"""
# Target
Run the main census regression battery (read-only): `bash tools/mori-census.sh --selftest` and the oracle
mode if the usage documents it, at {LANE}.
# Acceptance
Paste the tallies (expected selftest 134/134, oracle 28/28 on this host per r36). VERDICT: PASS iff both are
fully green; FAIL with the failing assertions otherwise.
"""),
    item("ExecIndexClean", "executor", f"""
# Target
cd {LANE} && bash tools/mori-index-clean.sh {LANE}; echo EXIT=$?
# Acceptance
Paste output. VERDICT: PASS iff `staged=0 intent_to_add=0` exit 0.
"""),
    item("ExecMisrootSweep", "executor", f"""
# Target
Run the misroot sweep: `git -C {FLEET} status --porcelain` (no pathspec). For every untracked file whose
content names mori or round-37, report its path and content head.
# Acceptance
List every candidate; state whether any is a mori round-37 seat file written to the fleet root. VERDICT:
PASS iff no mori round-37 file is misrooted (or you name each one).
"""),
    item("ExecSourceCensus", "executor", f"""
# Target
Run the four census commands from the CORPUS.md SOURCES contract over {LANE}/corpus/SOURCES.md: row count,
malformed rows (must be 0), duplicate ids (must print nothing), enum violations/tier inflation (must print
nothing). Also print the status histogram.
# Acceptance
Paste all five outputs. VERDICT: PASS iff malformed=0, no duplicate ids, no enum violations.
"""),
    item("ExecFreezeVerify", "executor", f"""
# Target
Verify every freeze pin: `git -C {LANE} hash-object <path>` for the eight paths in
{W}/evidence/freeze-r37.txt, plus sha256 for the three files it lists.
# Acceptance
Paste a table path/pin/recomputed/match. VERDICT: PASS iff all match (a mismatch means the frozen artifact
was edited after the freeze — report it).
"""),
    item("ExecKnowledgeCheck", "executor", f"""
# Target
Check the knowledge entry's code claims against the tool: line ranges cited in
corpus/knowledge/source-drift-hardening-r37.md (`:54,163-166`, `:113-136`, `:156-159`, `:103-108`) must
contain what the entry says. Read those ranges in tools/mori-source-drift.py at {TIP}.
# Acceptance
Report each range and whether the claim holds. VERDICT: PASS iff every range holds at the scored rev.
"""),
    item("ExecReadmeRows", "executor", f"""
# Target
Resolve both new coverage-map rows: every backticked path in the two `source-drift` rows of
{LANE}/corpus/README.md must exist at {TIP}; the cited receipt must contain the summary sentence.
# Acceptance
Report path -> exists. VERDICT: PASS iff all resolve.
"""),
    item("ExecScorecardRows", "executor", f"""
# Target
Resolve the two new capability rows in SCORECARD.md: each evidence path must exist and each receipt must
print the verdict the row claims. Also check the row's key cell is unique in the register.
# Acceptance
Report each row and resolution. VERDICT: PASS iff both resolve and the keys are unique.
"""),
    item("ExecLogAnchors", "executor", f"""
# Target
Verify the LOG.md round-37 entry's anchors: every hash, path and command named there resolves or reruns.
# Acceptance
Report each anchor. VERDICT: PASS iff all resolve; name any that do not.
"""),
    item("ExecQuality106", "executor", f"""
# Target
Show QUALITY 106's check able to fail: build a counter copy in your scratch with the memoizer negative
removed from the fixture list, run it at {TIP}, and report the verdict.
# Acceptance
Report the copy's path, diff summary, and output. VERDICT: PASS iff it prints C1=met (i.e. the criterion's
check would not catch a counter that omits the negative) OR explain why the fixture list is not removable.
"""),
    item("ExecQuality107", "executor", f"""
# Target
Show QUALITY 107's check able to fail: run the round-36 counter against `fixtures/summary-only.py`
(expect C2=met) and the round-37 counter against it (expect rejected). Report both.
# Acceptance
Paste both outputs. VERDICT: PASS iff the before/after pair reproduces.
"""),
    item("ExecGateRegistry", "executor", f"""
# Target
Check the gate registry in {LANE}/SKILL.md: the round-37 capabilities need registry rows (source-drift probe
hardening; the C1 counter's challenge arm). Read the Round-36 registry table format and report the exact
rows that are missing, with the fields the table requires.
# Acceptance
A table of missing rows/fields. VERDICT: PASS iff you name every missing registry row precisely (do not edit).
"""),
    item("ExecLessonGate", "executor", f"""
# Target
Verify the lesson Gate line ranges against the committed copies: for S221..S225, check the quoted text
occurs at the cited `S###.src` lines and count words.
# Acceptance
Report row/range/contiguous/word-count. VERDICT: PASS iff all five are contiguous at their cited lines and
<=25 words.
"""),
    # ---------------------------------------------------------------- scribes (6)
    item("ScribeReport", "scribe", f"""
# Target
Draft the report's **Sources & frontier** and **Trend verdicts** sections into your own report file, from
the committed bytes only: SOURCES rows before (220) -> after (225), five added by tier/kind/status, none
edited in place, and one verdict each for expansion/quality/discernment with a pointer per verdict.
# Acceptance
Your report holds the two drafted sections with the census command and its exit code. VERDICT: PASS iff the
row counts are re-derived by command and every verdict has a pointer.
"""),
    item("ScribeScorecard", "scribe", f"""
# Target
Audit the Round-37 SCORECARD section against the receipts: each before/after cell must name a command that
appears in the evidence file it cites.
# Acceptance
A table claim/cell/command-present. VERDICT: PASS iff every cell's command appears in its cited receipt.
"""),
    item("ScribeLog", "scribe", f"""
# Target
Audit the LOG.md round-37 entry: every measured value in it must appear in the cited receipt.
# Acceptance
A table value/receipt/present. VERDICT: PASS iff every value matches.
"""),
    item("ScribeLesson", "scribe", f"""
# Target
Audit corpus/lessons/round-37.md: the Gate table's five quotes against the copies, and each Mistakes row's
captured-by and fix. Report any row whose "shown able to fail" evidence does not resolve.
# Acceptance
A table row/evidence-resolves. VERDICT: PASS iff all resolve.
"""),
    item("ScribeSkill", "scribe", f"""
# Target
Draft the SKILL.md registry rows for round 37 (source-drift probe hardening; real-arm challenge counter)
following the Round-36 table's columns, into your own report file. Do not edit SKILL.md.
# Acceptance
The drafted rows with every column filled from the receipts. VERDICT: PASS iff every cell cites a path or
command that exists at {TIP}.
"""),
    item("ScribeQuality", "scribe", f"""
# Target
Audit QUALITY 106/107's wording against the measured behaviour: does each criterion's Check sentence name a
command that actually prints the required line, and does its "Shown able to fail" cite a real receipt?
# Acceptance
A table criterion/check-command/output-match. VERDICT: PASS iff both hold.
"""),
    # ---------------------------------------------------------------- scouts (8)
    item("ScoutCensusSurfaces", "scout", f"""
# Target
Confirm no census surface changed this round: `git -C {LANE} diff 842a320..{TIP} --name-status` must list
no `tools/mori-census.sh`, `tools/mori-silence-cases.sh`, oracle or baseline path.
# Acceptance
Paste the name-status list and the conclusion. VERDICT: PASS iff no census surface is in the diff.
"""),
    item("ScoutSentData", "scout", f"""
# Target
Re-run the r36 SentData sweep on THIS round's evidence: scan {W}/evidence/ and corpus/evidence/sources-r37/
for absolute operator paths (`/home/vgpnk`), credentials, cursors. Report each hit with its line.
# Acceptance
A hit list. VERDICT: PASS iff no `/home/vgpnk` path and no credential material in new evidence (a hit is a
FAIL naming the file:line).
"""),
    item("ScoutFreeze", "scout", f"""
# Target
Find any edit to a frozen path after the freeze: compare `git -C {LANE} log --oneline 842a320..{TIP} --`
over the eight frozen paths, and check whether any commit touched them after the freeze pin commit.
# Acceptance
A commit list per path. VERDICT: PASS iff only the freeze commit touched them; FAIL with the commit and diff.
"""),
    item("ScoutClaimsVsBytes", "scout", f"""
# Target
Map each claim to the bytes that carry it: for C1, the counter's challenge/id-grammar code; for C2, the
two arms and the two policy lines. Report file:line for each.
# Acceptance
A map claim -> file:line. VERDICT: PASS iff every element resolves at {TIP}.
"""),
    item("ScoutWaveSpec", "scout", f"""
# Target
Audit {W}/w1-spec.json for distinctness and padding: every item must name distinct work, and no item may be
a renamed duplicate of another. Report duplicates or filler.
# Acceptance
A duplicate/filler list (or "none"). VERDICT: PASS iff no two items share a target and acceptance.
"""),
    item("ScoutPriorRound", "scout", f"""
# Target
Read {LANE}/corpus/lessons/round-36-verifier-spotcheck.md and {LANE}/corpus/lessons/round-36.md, and list
every routed defect with its r37 disposition as claimed in the round-37 contract/lesson.
# Acceptance
A table defect/r37-disposition/artifact. VERDICT: PASS iff every defect has a disposition.
"""),
    item("ScoutCorpusCensus", "scout", f"""
# Target
Census the registry: total rows, status histogram, tier histogram, duplicate ids, and the five new rows'
`used-by` paths resolving.
# Acceptance
Paste commands and outputs. VERDICT: PASS iff counts match 225 rows and no duplicate id.
"""),
    item("ScoutReportContract", "scout", f"""
# Target
Check the round report's required sections against {FLEET}/.ufo/prompts/mori-round-37.md section 4 (once
the report exists): Work performed, Landed changes, Before -> after measurements, Sources & frontier,
Trend verdicts, SHONEN.
# Acceptance
A section-present table plus the marker-rule verdict. VERDICT: PASS iff all required sections are present
with evidence pointers.
"""),
    # ---------------------------------------------------------------- connectors (4)
    item("ConnSiblingOverlap", "connector", f"""
# Target
Scan sibling lanes' recent lessons for work overlapping this round's claims: `ls {FLEET}/*-shokunin/corpus/lessons/`
and read the newest file per lane whose name mentions counters, gates or drift (do not edit).
# Acceptance
A table lane/overlap/none with the file read. VERDICT: PASS iff the scan is complete over the lanes that
exist and each overlap is named.
"""),
    item("ConnKumitate", "connector", f"""
# Target
Kumitate r48 admitted a counter-rerun (run-agreement). Read its report under {FLEET}/.ufo/reports/round-48/
(if present) and compare its run-agreement technique with this round's challenge arm: does mori's C1
duplicate or contradict it?
# Acceptance
A comparison with file:line pointers. VERDICT: PASS iff the relationship (none/duplicate/contradiction) is
stated with evidence.
"""),
    item("ConnChousa", "connector", f"""
# Target
Chousa r34 admitted a dead-zone boundary. Read its report and state whether this round's drift probe touches
chousa's research domain or stays inside mori's detection/report province.
# Acceptance
A verdict with pointers. VERDICT: PASS iff the boundary is stated with evidence.
"""),
    item("ConnKama", "connector", f"""
# Target
Kama r29 calibrated writing revisions. Read its report and report whether any mori r37 artifact (lesson,
entry, report prose) asserts a writing-revision claim that belongs to kama.
# Acceptance
A list of contested sentences (or none). VERDICT: PASS iff the scan is explicit.
"""),
    # ---------------------------------------------------------------- revengers (4)
    item("RevNgC1Env", "revenger", f"""
# Target
Reverse-engineer the remaining arm-detection surface of {W}/count-c1.py: env, cwd, parent cmdline, argv rev
literal, sandbox header, git identity. Build a fixture that detects the CHALLENGE arm specifically (without
reading the history) and report whether it can pass all three arms by lying only on the challenge.
# Acceptance
A detection-key table and a demonstrated attempt (scratch only). VERDICT: PASS iff no detection key lets a
liar pass the challenge (or the surviving key is named as a residual).
"""),
    item("RevNgC1Fixtures", "revenger", f"""
# Target
Attack the realism of the three negative fixtures: are they weak stand-ins that a smarter memoinzer would
defeat? Write your own stronger memoizer in scratch (e.g. one that recomputes only when the history is
short) and run the counter on it.
# Acceptance
Your fixture's verdict plus the reason. VERDICT: PASS iff the counter rejects it or you name the bypass.
"""),
    item("RevNgC2Anchors", "revenger", f"""
# Target
Attack the mutation anchors of {W}/count-c2.py: can a tool keep each policy's effect while breaking the
anchor (e.g. rename the constant, split the condition) and still pass? Report whether the anchor-based
mutation is robust or brittle, and what a semantics-based check would cost.
# Acceptance
A concrete example of an anchor-breaking edit and its effect on the self-test. VERDICT: PASS iff the
limitation is named.
"""),
    item("RevDebtR36", "revenger", f"""
# Target
Reverse-engineer the r36 residuals in {LANE}/corpus/lessons/round-36.md (Collateral note + M4) and in
{W}/contract.md's debt table. Find any residual still open and name the artifact that would close it.
# Acceptance
A residual list with open/closed. VERDICT: PASS iff each is classified with evidence.
"""),
    # ---------------------------------------------------------------- sentinels (3)
    item("SentTools", "sentinel", f"""
# Target
Security-review the new fixtures and counters ({W}/count-c1.py, count-c2.py, fixtures/*.py): subprocess use,
shell=False, path injection via --repo/--tool, scratch cleanup, writes outside scratch, network use.
# Acceptance
A finding list with severity and file:line. VERDICT: PASS iff no high-severity defect; FAIL with the defect.
"""),
    item("SentData", "sentinel", f"""
# Target
Evidence hygiene for the round's committed evidence: credential/cursor/private-data scan, absolute-path
scan, and check that no evidence file contains a lane-external path.
# Acceptance
A scan table with patterns and hits. VERDICT: PASS iff no secrets and no absolute operator paths.
"""),
    item("SentScope", "sentinel", f"""
# Target
Verify write scope: inspect the round's commits (`git -C {LANE} log --name-status 842a320..{TIP}`) and
confirm every path is inside the lane repo and none is a sibling, fleet, or operator config path.
# Acceptance
The path list and conclusion. VERDICT: PASS iff every path is in scope.
"""),
    # ---------------------------------------------------------------- simplifiers (2)
    item("SimpC1", "simplifier", f"""
# Target
Find removable weight in {W}/count-c1.py that does not change P-C1: dead code, duplicated helpers,
over-general branches. Report a deletion plan with line ranges; do not edit.
# Acceptance
A ranked deletion list with the predicate-preservation argument. VERDICT: PASS iff every proposal is
argument-checked.
"""),
    item("SimpC2", "simplifier", f"""
# Target
Same for tools/mori-source-drift.py's round-37 additions and {W}/count-c2.py.
# Acceptance
A ranked deletion list. VERDICT: PASS as above.
"""),
    # ---------------------------------------------------------------- distiller (1)
    item("DistillFindings", "scribe", f"""
# Target
After the other seats land, read the wave reports under {W}/w1/ that exist and deduplicate their findings
into a ranked list: finding, seats that reported it, evidence pointer, severity.
# Acceptance
The ranked list. VERDICT: PASS iff every finding names at least one seat and one path.
"""),
]


def main():
    spec = {
        "wave": "mori-r37-w1",
        "reportDir": ".ufo/waves/round-37/w1",
        "maxLanes": 96,
        "context": CONTEXT,
        "items": ITEMS,
    }
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(spec, handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    roles = {}
    for it in ITEMS:
        roles[it["role"]] = roles.get(it["role"], 0) + 1
    # labrat/distiller are frozen-topology seats (validator SWARM_ROLES): the three
    # bounded-probe items ride executor seats and the dedupe item rides a scribe seat.
    attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester"))
    print("items=%d roles=%s attack=%d (%.1f%%)"
          % (len(ITEMS), dict(sorted(roles.items())), attack, 100.0 * attack / len(ITEMS)))
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
