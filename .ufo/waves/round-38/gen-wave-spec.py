#!/usr/bin/env python3
"""Generate the round-38 v2 wave spec (one wave, build + attack) next to this file.

Run: python3 .ufo/waves/round-38/gen-wave-spec.py
Writes: .ufo/waves/round-38/w1-spec.json
"""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
W = LANE + "/.ufo/waves/round-38"
TIP = "f725f3076972e6e70595b5ac8279be524a111ff8"
ENTER = "e33bb561712b32f46861362a3fa43762fa70ae4f"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""

CONTEXT = f"""# mori round 38 — one v2 wave (build + attack), L1 MoriR38

Lane repo: {LANE} (jj-colocated; git is the backend). Fleet repo: {FLEET} (read-only for you).
Scored tip under attack: {TIP} (pushed). Entering tip: {ENTER}.

## Claims under attack
- C1 (calibration, measured): `python3 .ufo/waves/round-38/count-c4.py {TIP}` — the drift-corpus
  binding must pass four content checks (entry `anchor:` lines resolve in the probe's bytes; every
  capability-row path resolves from the repo root; the live receipt names one drifted row per summary
  count; the `row_states` arm is killed by its own mutation) and reject three fabricated token
  witnesses. P-C4 is in `{W}/contract.md`; receipts `{W}/evidence/c4-before.txt`, `c4-after.txt`,
  `v3-token-control.txt`, `c4-witness.txt`; fixtures `{W}/fixtures/`.
- C2 (operability, measured): `python3 .ufo/waves/round-38/conform.py {TIP} --counter .ufo/waves/round-38/count-c1.py --counter .ufo/waves/round-38/count-c4.py`
  — six conformance checks (predicate bytes, lane-tip pin, repo-relative tool, bounded reads,
  timeout state, lane scratch) and six mutations each flipping its own check. P-C5 is in the
  contract; receipts `{W}/evidence/c5-before.txt`, `c5-after.txt`, `c5-after-selftest.txt`;
  the C1 counter is v4.1 (freeze v2 pin `{W}/evidence/freeze-r38-v2.txt`).
- C3 (depth, measured): `python3 tools/mori-sources-appendonly.py {TIP} --round-base f10a320d` —
  the gate reports `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; S069 is stale
  at {ENTER} and as-of after S226 lands. Receipts `{W}/evidence/gate-before.txt`, `gate-after.txt`,
  `gate-selftest-after.txt`; `corpus/knowledge/containment-timed-supersede-r38.md`.
- Frontier: S226 opened this round (copy `corpus/evidence/sources-r38/S226.src`), lesson
  `corpus/lessons/round-38.md` (Gate + M1–M6), QUALITY 108–110, erratum
  `corpus/lessons/round-37-erratum.md`, LOG amendment.

## Hard bounds (every seat)
- Write EXACTLY ONE file: your report. The validator renders `Report: .ufo/waves/round-38/w1/<Name>.md`;
  that path is RELATIVE TO {LANE} — write it at {LANE}/<that path>. Scratch code/outputs only under
  `{LANE}/.ufo/waves/round-38/scratch/<YourName>/` or `$TMPDIR`.
- The lane repo is READ-ONLY for you: never `git add/commit/push/fetch/reset/stash`, never any
  mutating jj command, never edit lane files. Running the lane's read-only tools and counters is
  fine; mutation-testers run COPIES under their own scratch — never edit the lane's real files.
- Never touch: {FLEET}/MANIFEST.json, {FLEET}/.ufo/state/, {FLEET}/.ufo/watchdog.log,
  {FLEET}/templates/, {FLEET}/scripts/, sibling lane repos, ~/.omp/agent/config.yml,
  ~/.omp/agent/mcp.json.
- Detection and report only — no remediation, no kills, no config edits (mori province).
- Tooling directive (operator, 2026-10-19): you may install or upgrade tools that help your task —
  read `~/.omp/agent/RULES.md` first (official channels only; never pipe a remote script into a
  shell; record tool/version/channel/reason in your report). **pacman transactions are PAUSED
  host-wide**: install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or file an L0
  question. Never `pacman -Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host service.
- Never use `agent://all`; your result is the report. Cite path:line or a command output for every
  claim; an unrun check has not passed.
"""


def item(name, role, target, acceptance):
    prompt = (GODSPEED + f"# Target\n{target}\n\n# Acceptance\n{acceptance}\n")
    return {"name": name, "role": role, "prompt": prompt}


ITEMS = []
A = ITEMS.append

# ---- C1 attacks (content anchors)
A(item("RevC4Anchors", "reviewer",
  f"Independently verify P-C4's anchor check. Read `{W}/contract.md` P-C4, list every `anchor:` line in `{LANE}/corpus/knowledge/source-drift-content-anchor-r38.md`, and resolve each string with `grep -F` in `tools/mori-source-drift.py` at `{TIP}` (`git show {TIP}:tools/mori-source-drift.py`). Then run `python3 .ufo/waves/round-38/count-c4.py {TIP}` and compare its `check anchors` detail with your own resolution.",
  "Report each anchor's resolution (file:line in the tool) and whether the counter's detail agrees; FAIL on any anchor that does not resolve or a counter verdict that hides one."))
A(item("RevC4Capability", "reviewer",
  f"Independently resolve every path the SCORECARD capability row `source-drift re-fetch probe` cites at `{TIP}`: `git cat-file -e {TIP}:<path>` for each backticked path. Compare with the counter's `check capability` detail.",
  "Report the resolved/missing table; FAIL if any cited path fails to resolve at the tip or the counter misses one."))
A(item("RevC4Live", "reviewer",
  f"Verify the `live_rows` content check: parse `{LANE}/.ufo/waves/round-37/evidence/drift-live-r37.txt` at `{TIP}`, count `<S###> drifted` lines and the summary's `drifted=` value, and check every named id is a registry row at `{TIP}` (`grep -E '^\\| S[0-9]{{3}} '`). Compare with the counter's `check live_rows`.",
  "Report the counts and the id membership; FAIL on a mismatch or an id outside the registry."))
A(item("RevC4Kill", "reviewer",
  f"Re-derive the `drift_kill` check: extract `tools/mori-source-drift.py` at `{TIP}`, replace `return \"drifted\"` with `return \"excerpt\"` in a scratch copy, run `--selftest`, and confirm `selftest row_states FAIL` names S103. Run the unmutated selftest too.",
  "Report both selftest outputs' row_states lines and the exit codes; FAIL if the mutation does not flip row_states or does not name S103."))
A(item("RevC4Negatives", "reviewer",
  f"Project each of `{W}/fixtures/witness-token-entry.md`, `witness-dangling-row.md`, `witness-summary-only-live.txt` onto the real other bytes and name which of the four content checks each one fails. Run `python3 .ufo/waves/round-38/count-c4.py {TIP}` for the receipt.",
  "Report a witness→failed-check table and the counter's three negative lines; FAIL if any witness passes all four checks or the counter's rejection reason differs from yours."))
A(item("CritC4Gaming", "critic",
  f"Build a fabricated binding that satisfies all four P-C4 checks without doing the claimed work (e.g. anchor strings that exist but are dead code, a live receipt whose per-row lines are copied from another round, a capability path that resolves to a stub). Run the counter's checks mentally or in scratch against `{TIP}` bytes.",
  "Report the strongest gaming construction and whether the counter accepts it; if accepted, name the exact check that must be tightened and why the current P-C4 bound permits it."))
A(item("MutC4Anchor", "mutation-tester",
  f"Mutate a copy of `corpus/knowledge/source-drift-content-anchor-r38.md` (scratch only) by changing one `anchor:` string by one byte; run `count-c4.py` against a sandbox revision carrying the mutant (clone `{LANE}` at `{TIP}`, commit the mutant, run with `--repo`).",
  "Report the mutant's `check anchors` line and `C4=` verdict; PASS only if the mutant flips anchors to FAIL."))
A(item("MutC4CapPath", "mutation-tester",
  f"Mutate a copy of `SCORECARD.md` (scratch) so the `source-drift re-fetch probe` row cites `evidence/no-such-file.txt`; build the sandbox as in MutC4Anchor and run `count-c4.py`.",
  "Report the mutant's `check capability` line and `C4=` verdict; PASS only if the mutant flips capability to FAIL."))
A(item("MutC4Live", "mutation-tester",
  f"Mutate a copy of `.ufo/waves/round-37/evidence/drift-live-r37.txt` to keep the summary and drop the per-row lines; sandbox and run `count-c4.py`.",
  "Report the mutant's `check live_rows` line and `C4=` verdict; PASS only if the mutant flips live_rows to FAIL."))
A(item("MutC4KillAlt", "mutation-tester",
  f"In a scratch copy of the probe at `{TIP}`, replace `return \"drifted\"` with `return \"fresh\"` and run `--selftest`; then run the counter's `drift_kill` logic against a sandbox carrying that tool.",
  "Report whether row_states fails and whether S103 is named; PASS if the kill check rejects a different mutation of the same branch."))
A(item("ScoutC4Bounds", "scout",
  f"Read `{W}/count-c4.py` and enumerate exactly what each of its four checks proves and what it cannot prove, with line references. Include the capability 'last row wins' rule and the `anchor:` substring rule.",
  "Report a bounds table (check → proves → does not prove) with line numbers; FAIL if any claim in the contract's P-C4 is stronger than the code."))

# ---- C2 attacks (conformance)
A(item("RevC5Predicate", "reviewer",
  f"Independently compare the contract's P-C1 blockquote (`{W}/contract.md`, the 'P-C1 of record' section) with `python3 .ufo/waves/round-38/count-c1.py --print-predicate` after whitespace normalisation. Also diff the r37 contract's first P-C1 blockquote to show the defect the check closes.",
  "Report both normalised lengths and the equality booleans; FAIL if they differ or the r37 comparison is not reproduced."))
A(item("RevC5Pin", "reviewer",
  f"Verify the pin: `python3 .ufo/waves/round-38/count-c1.py --pin-only --repo {LANE}` against `git -C {LANE} rev-parse HEAD`, and confirm the full-run receipt `{W}/evidence/c1-after-r38.txt` carries the same `head_at_measurement=`.",
  "Report all three values; FAIL if the receipt's pin differs from the tip it names or the flag output."))
A(item("RevC5Tool", "reviewer",
  f"Test repo-relative `--tool` resolution including an escape attempt: run `count-c1.py {TIP} --tool .ufo/waves/round-38/fixtures/summary-only.py --print-tool` and `--print-tool ../outside.py`; inspect `resolve_tool`'s body.",
  "Report the resolved paths and exit codes; FAIL if a repo-relative path resolves outside the lane or the flag executes a missing file."))
A(item("RevC5Bounds", "reviewer",
  f"Audit every child process and git read in `{W}/count-c1.py` and `count-c4.py` for a timeout and the committed-blob read for a byte cap; list each call site with line numbers.",
  "Report the audit table; FAIL on any read without a bound or a cap that cannot be reached."))
A(item("RevC5Timeout", "reviewer",
  f"Run `python3 .ufo/waves/round-38/count-c1.py {TIP} --tool {W}/fixtures/hang-after-flush.py --tool-timeout 3 --arms real --seed 7` and time it. Then check the printed reason and exit code.",
  "Report the wall time, the `real arm` line, the diff line, `C1=` and exit; FAIL if the tool scores a pass, if the reason is not `tool_timeout`, or if wall time exceeds timeout+grace by more than 2 s."))
A(item("RevC5Scratch", "reviewer",
  f"Verify the scratch property: inspect every `tempfile.mkdtemp(` in both round-38 counters and run two concurrent `count-c1.py {TIP} --arms real --seed 11` processes; list the directories created under `{W}/scratch/`.",
  "Report the mkdtemp call sites and the observed directories; FAIL on a shared or seed-derived path."))
A(item("MutC5Predicate", "mutation-tester",
  f"Apply conform's `predicate` mutation to a scratch copy of `count-c1.py` and run `conform.py --selftest --counter <mutant>`.",
  "Report the mutation line and whether only `predicate` failed; PASS only if exactly that check flips."))
A(item("MutC5Pin", "mutation-tester",
  f"Apply conform's `head_pin` mutation to a scratch copy and run the checker's evaluate path for that mutant (via `--selftest --counter <mutant>` or by calling `evaluate` in a scratch harness).",
  "Report whether only `head_pin` failed; PASS only on exactly that flip."))
A(item("MutC5Tool", "mutation-tester",
  f"Apply conform's `tool_resolve` mutation (`return path` instead of the absolute join) to a scratch copy and run the checker.",
  "Report whether only `tool_resolve` failed; PASS only on exactly that flip."))
A(item("MutC5Bounds", "mutation-tester",
  f"Apply conform's `bounded_reads` mutation (drop `timeout=timeout` from the git helper's `run(` call) to a scratch copy and run the checker.",
  "Report whether only `bounded_reads` failed; PASS only on exactly that flip."))
A(item("MutC5Timeout", "mutation-tester",
  f"Apply conform's `timeout_state` mutation (`_TOOL_BUDGET[0] = TOOL_TIMEOUT_S`) to a scratch copy and run the checker.",
  "Report whether only `timeout_state` failed; PASS only on exactly that flip."))
A(item("MutC5Scratch", "mutation-tester",
  f"Apply conform's `scratch` mutation (`SCRATCH_ROOT = \"/tmp/mori-r38-scratch\"`) to a scratch copy and run the checker.",
  "Report whether only `scratch` failed; PASS only on exactly that flip."))
A(item("CritC5Gaming", "critic",
  f"Attack the conformance checker itself: can a counter pass all six checks while being unreplayable or unbounded (e.g. `--pin-only` printing a constant equal to HEAD, `--print-tool` echoing without executing, a timeout path that never runs)? Read `{W}/conform.py`.",
  "Report the strongest bypass and whether the checker or its selftest catches it; name the missing mutation if any."))
A(item("RevC1Negatives", "reviewer",
  f"Re-derive the C1 counter's negative judgement at `{TIP}`: run `python3 .ufo/waves/round-38/count-c1.py {TIP} --seed 20261023` and inspect the four `negative` lines. Verify memo-n1's rejection now names the drawn arm and memo-sha's state is disclosed.",
  "Report each negative line and the `C1=` verdict; FAIL if memo-n1 is rejected only by the challenge arm or memo-sha is unmentioned."))
A(item("RevC1SoundnessBound", "revenger",
  f"Reproduce the r37 RevNgC1Fixtures class against the v4.1 counter: build a short-history memoizer and a content-keyed delegator in scratch, score them on `count-c1.py {TIP}`, and state which are rejected and which pass.",
  "Report each specimen's verdict with the rejecting arm; name the remaining black-box bound (honest delegation) in one sentence."))

# ---- C3 attacks (timed supersede)
A(item("RevGateTiming", "reviewer",
  f"Re-derive the timing field: run `python3 tools/mori-sources-appendonly.py {ENTER}` and `{TIP}` (both `--round-base f10a320d`) and parse `supersede_timing`. For S069 verify `git merge-base --is-ancestor 71abd41 62db24c` (superseder before edit) and that S226's landing commit descends from 62db24c.",
  "Report both timing lines and the ancestry results; FAIL if S069's stale/as-of state contradicts the commits."))
A(item("MutGateTiming", "mutation-tester",
  f"Mutate a scratch copy of the gate so `stale_supersede` is derived from presence (always empty); run its `--selftest`.",
  "Report the selftest verdict; PASS only if the supersede-before-edit fixture fails the mutant."))
A(item("RevGateS226", "reviewer",
  f"Verify S226: the row opens `supersedes S069`, its source copy `corpus/evidence/sources-r38/S226.src:657-658` carries the quoted paragraph, its landing commit is a descendant of 62db24c, and `used-by` resolves.",
  "Report the row, quote, ancestry and path resolution; FAIL on any mismatch."))
A(item("CritGateSemantics", "critic",
  f"Attack the timed semantics: construct two histories in a scratch git repo — (i) a superseder that lands after the edit but whose row is itself later deleted, (ii) a superseder on an unrelated branch. Run the gate and report what `supersede_timing` says.",
  "Report both constructions and the gate's verdicts; name which of the contract's P-C6 sentences is too strong, if any."))
A(item("RevGateCompat", "reviewer",
  f"Check that the r37 C1 counter still parses the new gate output: run `python3 .ufo/waves/round-37/count-c1.py {TIP} --seed 41` and inspect the blind/real arms (the gate prints a predicate line and a timing line now).",
  "Report `C1=` and any malformed-line counts; FAIL if the extra lines break the parser or change a list."))
A(item("ScoutGateRank", "scout",
  f"Walk `tools/mori-sources-appendonly.py`'s supersede code and report the exact index basis (first landing per superseder, max across superseders) with line numbers; state what a merge-heavy history would do.",
  "Report the line-referenced mechanism and the merge caveat; FAIL if the code differs from the contract's 'latest superseding row's landing commit'."))

# ---- documentary / erratum / receipts
A(item("RevErratum", "reviewer",
  f"Verify every sentence of `corpus/lessons/round-37-erratum.md` E1–E8 against git: the 8ff9bba/1caa242 content check, the 225/10 sweep, the before-arm command form, the M1–M10 label, the 5631efa diff, the capability first-working, the axes cells.",
  "Report a sentence→evidence table; FAIL on any sentence the repository contradicts."))
A(item("RevLogAppend", "reviewer",
  f"Verify the LOG amendment is append-only: `git diff 3501d4c2^ 3501d4c2 -- LOG.md` must be additions only, and the appended entry must name the superseded text. Also verify the Round-37 entry is unchanged in that commit.",
  "Report the numstat and the first/last added lines; FAIL on any deletion or an unnamed superseded sentence."))
A(item("RevScorecardCells", "reviewer",
  f"Verify the axes-cell correction and capability rows at `{TIP}`: the `freshness` cell no longer cites round-37 C2, the `operability` cell carries the round-37 pointer, the `round-37 C2` row's first-working is 36, and every path in both round-37 capability rows resolves from the repo root.",
  "Report each cell/row check with the resolution commands; FAIL on any superseded clause left in place or a non-resolving path."))
A(item("RevSourcesAppend", "reviewer",
  f"Verify the round's SOURCES change is append-only: `python3 tools/mori-sources-appendonly.py {TIP} --round-base f10a320d` and `git diff {ENTER} {TIP} -- corpus/SOURCES.md` must add S226 and one search-log note only.",
  "Report the gate line, the diffstat, and the added lines; FAIL on any in-place cell edit (the gate's `round_changed`)."))
A(item("RevQualityCriteria", "reviewer",
  f"Verify QUALITY 108–110 are checkable: run each criterion's named check at `{TIP}` and confirm the 'Shown able to fail' pointer resolves.",
  "Report criterion→command→output; FAIL if any check cannot be run or its fail-evidence is absent."))
A(item("RevSkillRows", "reviewer",
  f"Verify the three new SKILL registry rows: each command's exit map matches the tool's behavior, the pinned values resolve at `{TIP}`, and the r36 gate row's selftest count is 9.",
  "Report row→command→observed; FAIL on an exit-map mismatch or an unresolved pin."))
A(item("RevLessonMistakes", "reviewer",
  f"Verify each round-38 lesson M row: the quoted pre-fix evidence exists (in receipts or git) and the fix is shown able to fail by a named command.",
  "Report M→evidence→fix command; FAIL on a row whose 'shown able to fail' is not re-runnable."))
A(item("RevFreezeV2", "reviewer",
  f"Verify the freeze: `{W}/evidence/freeze-r38.txt` pins the frozen v1 paths, `{W}/evidence/freeze-r38-v2.txt` pins the v4.1 counter and fixtures, and the committed bytes at `{TIP}` hash to the v2 pins. Name the version change (run_negative drawn arm + memo-sha bound).",
  "Report the hash comparison; FAIL on any drift not named in the v2 pin file."))
A(item("RevCensus", "reviewer",
  f"Re-run `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` and compare with `{W}/evidence/census-start.txt`; count rows at `{ENTER}` and `{TIP}`.",
  "Report exit codes, W/E lines and row counts; FAIL on a new error line or a row count other than +1."))
A(item("RevReceipts", "reviewer",
  f"Audit every receipt under `{W}/evidence/`: each carries its `command:` line, no absolute operator path other than the lane root, and its printed verdict matches the claim it supports.",
  "Report a receipt→verdict table and any path-hygiene defect; FAIL on a receipt whose command does not reproduce its output."))
A(item("RevReportSections", "reviewer",
  f"Draft-check the report contract for round 38: required sections in order (Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN), marker rules, and the cites each section needs from `{W}`.",
  "Report a section→required-evidence table; FAIL on a missing section or a verdict written without a receipt."))

# ---- frontier / scout / connector / misc
A(item("ScoutMisroot", "scout",
  f"Run `git -C {FLEET} status --porcelain` (no pathspec) and for every untracked file decide whether a mori seat wrote it (content names this lane/round). Do not delete anything; list candidates with byte sizes.",
  "Report the status output and a candidate table; FAIL if an untracked file naming this lane/round is omitted."))
A(item("ScoutPycache", "scout",
  f"Check for committed bytecode at `{TIP}` (`git ls-tree -r {TIP} | grep -c __pycache__`), the `.gitignore` rule, and whether `tools/mori-index-clean.sh` watches `__pycache__`. Report the r37 RevScratch residual status.",
  "Report the counts and the index-clean watch list; FAIL if a tracked `__pycache__` path exists at the tip."))
A(item("ScoutPriorRound", "scout",
  f"Verify the r37 residual dispositions named in `{W}/contract.md`'s debt table against the repository: predicate equality, pin, tool resolution, bounded reads, timeout state, scratch, capability first-working, debt (f), QUALITY 103 log.",
  "Report debt→evidence→status; FAIL on a row marked done without its artifact."))
A(item("ScoutFrontierRows", "scout",
  f"Check the corpus README's Frontier table and coverage map for the two new r38 entries (`knowledge/source-drift-content-anchor-r38.md`, `knowledge/containment-timed-supersede-r38.md`); verify the rows exist in the map and in the Round-38 section.",
  "Report the rows and line numbers; FAIL if an entry is missing from the map or the section."))
A(item("ConnSibling", "connector",
  f"Scan sibling lanes' recent commits/corpus for overlap with this round's surfaces (drift probe, append-only gate, counter conformance). Name any sibling artifact that already does this work or that this round's changes could break.",
  "Report a sibling-overlap table with paths and verdicts; FAIL if an overlapping sibling artifact is omitted."))
A(item("ConnReceipts", "connector",
  f"Compare this round's receipt style (command: line, EXIT, repo-relative paths) with the fleet's evidence conventions in `{FLEET}/CORPUS.md` and adjacent lanes' recent receipts; name any divergence.",
  "Report the convention comparison; FAIL on an uncited divergence."))
A(item("RevDebtF", "revenger",
  f"Verify debt (f) is named, not decided: check the L0 question in `{FLEET}/.ufo/l0-questions.md`, the lesson row, and the counters' SIGTERM→grace→SIGKILL behavior (`run()` in both round-38 counters).",
  "Report the L0 line, lesson line and the measured signal path; FAIL if the round claims the tradeoff closed or edited a counter to hide it."))
A(item("SentCounters", "sentinel",
  f"Security-review `{W}/count-c1.py` and `count-c4.py`: executing the tool under test, path handling (`--tool`, `--repo`), symlink behavior, temp-file permissions, and the hang fixture's process group.",
  "Report each finding with severity and line; FAIL if a HIGH finding is omitted or a MEDIUM/LOW is claimed fixed without a check."))
A(item("SentWitnessSandbox", "sentinel",
  f"Review `{W}/fixtures/make-witness-sandbox.py`: clone source, identity, substitution paths, and whether the sandbox can be confused with the lane (path/identity/title). Run it once in scratch.",
  "Report the sandbox properties and verdict; FAIL if the sandbox can pass as the lane repo or if it writes outside scratch."))
A(item("SimpC1", "simplifier",
  f"Read `{W}/count-c1.py` v4.1 and list dead code, unused flags, or duplicated logic that can be deleted without changing behavior; do not edit the lane file.",
  "Report a deletion list with line ranges and the behavior-preserving argument; FAIL on a proposal that changes a predicate or a check."))
A(item("SimpC4", "simplifier",
  f"Read `{W}/count-c4.py` and list dead code or duplicated logic (e.g. the unused `anchors`/`named` recomputation in main) that can be deleted without behavior change.",
  "Report a deletion list with line ranges; FAIL on a proposal that changes a check's meaning."))
A(item("ExecWitnessSandbox", "executor",
  f"Rebuild the fabricated-binding control from scratch: run `python3 {W}/fixtures/make-witness-sandbox.py {TIP}` in scratch, then score the sandbox with the r37 counter and with `count-c4.py`.",
  "Report the sandbox sha, both verdicts, and the exact commands; FAIL if the r37 counter is not `C2=met` or count-c4 is not `C4=unmet`."))
A(item("ExecReplay", "executor",
  f"Replay the C1 counter at two seeds (`--seed 20261023` and `--seed 3737`) at `{TIP}` and compare the drawn-arm revs, the challenge results and the negative lines.",
  "Report both runs' key lines and seeds; FAIL if a run's verdict differs from `C1=met` or the receipts' seed differs unexplained."))
A(item("ExecGateDeterminism", "executor",
  f"Run `python3 tools/mori-sources-appendonly.py --selftest` three times and the gate at `{TIP}` twice; compare outputs byte-for-byte.",
  "Report the selftest lines and diff results; FAIL on any nondeterminism."))
A(item("ExecCensusEnd", "executor",
  f"Run the source census end command and store its output in your report; compare with `{W}/evidence/census-start.txt`.",
  "Report the exact command, exit code and verdict lines; FAIL on a new error (E-class) line."))
A(item("ExecIndexCleanLog", "executor",
  f"Verify `{W}/dispatch-log.txt` records `staged=0 intent_to_add=0` after every `landed` line: list the lane's commits since `{ENTER}` (`git log --format='%h %s' {ENTER}..{TIP}`) and compare with the log's entries.",
  "Report commit→log-entry table; FAIL on a landed commit without its index-clean record."))
A(item("ExecR17Battery", "executor",
  f"Run the r17-jj regression battery at `{TIP}` (`python3 tools/mori-round17-jj-regressions.py --selftest`) in scratch and report the assertion count.",
  "Report exit code and pass/fail counts; FAIL on a red assertion not disclosed."))
A(item("ExecCensusSelftest", "executor",
  f"Run `bash tools/mori-census.sh --selftest` and `bash tools/mori-silence-cases.sh` at `{TIP}` in scratch; report the tallies.",
  "Report both tallies and exits; FAIL on a regression against the last recorded counts."))
A(item("ScribeReportBullets", "scribe",
  f"Draft the report's **Work performed** bullets for C1–C3 and the routed items from `{W}/evidence/` receipts and the SCORECARD declaration; one bullet per item with a path:line or command pointer.",
  "Report the drafted bullets; FAIL on a bullet without a resolvable pointer."))
A(item("ScribeTrendVerdicts", "scribe",
  f"Draft the report's **Trend verdicts** (expansion, quality, discernment) with evidence pointers from this round's receipts, lesson M1–M6, the erratum and the QUALITY additions.",
  "Report the three verdict lines and their evidence; FAIL on a verdict without a receipt or a scalar score."))
A(item("ScribeSHONEN", "scribe",
  f"Draft the SHONEN checklist lines (four boxes) for the report, each `[~]` with a resolvable pointer or `[ ]`; never `[x]` without a named non-author verifier.",
  "Report the four lines and the pointers; FAIL on a `[x]` without a named verifier."))
A(item("RevAdmission", "critic",
  f"Judge the round for admission: each claim's after-state re-derived from a receipt, no universal clauses, no axis harmed (compare SCORECARD scores before/after). Read `{W}/contract.md` and the SCORECARD Round-38 section.",
  "Report claim→verdict→evidence and the no-harm table; FAIL on an admitted claim without a re-derivable value or a harmed axis left unnamed."))

# roles summary guard
ROLES = {i["role"] for i in ITEMS}
assert len(ITEMS) == len({i["name"] for i in ITEMS}), "duplicate names"
assert len(ITEMS) >= 64, len(ITEMS)

spec = {
    "wave": "mori-r38-w1",
    "reportDir": ".ufo/waves/round-38/w1",
    "maxLanes": 72,
    "context": CONTEXT,
    "items": ITEMS,
}
out = os.path.join(W, "w1-spec.json")
with open(out, "w", encoding="utf-8") as handle:
    json.dump(spec, handle, indent=1)
print("wrote %s (%d items; roles: %s)" % (out, len(ITEMS), sorted(ROLES)))
