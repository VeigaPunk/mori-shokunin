#!/usr/bin/env python3
"""Generate the round-39 wave-1 spec (build + first falsifiers, v1 band, 32 seats).

Run: python3 .ufo/waves/round-39/gen-wave1-spec.py
Writes: .ufo/waves/round-39/w1-spec.json
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
W = LANE + "/.ufo/waves/round-39"
TIP = "13bfba23b7ca063c76d3504a2ff6eb7b6a294932"
ENTER = "13f3db7e5c7163e7ef300259ff597a42a79f81f1"
BASE = "f10a320d"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""

RULES = """
Time-box: return within 15 minutes with your best findings+evidence; partial results are acceptable.
You are an independent leaf: never block on or wait for another seat; if a needed artifact is absent, record the dependency as a finding and return.
"""

CONTEXT = f"""# mori round 39 — wave 1 (build + first falsifiers), L1 mori-r39

Lane repo: {LANE} (jj-colocated; git is the backend). Fleet repo: {FLEET} (read-only for you).
Scored tip: {TIP} (pushed). Entering tip: {ENTER}. Round base of record: {BASE}.

## Claims under attack (frozen in {W}/contract.md, pins in {W}/evidence/freeze-r39.txt)
- C1 calibration: `python3 .ufo/waves/round-39/count-c7.py {TIP} --seed 20261024` must print `C7=met` exit 0
  (five v2 checks + four rejected witnesses; `{W}/evidence/c7-after.txt`). The r38 counter accepts four M18
  bypass classes: `{W}/evidence/c7-red-one-char.txt`, `c7-red-comment.txt`, `c7-red-classifier.txt`,
  `c7-red-clone.txt`. Predicate P-C7 is in the contract.
- C2 operability: `python3 .ufo/waves/round-39/conform.py {TIP}` must print `CONFORM=met` exit 0 and
  `--selftest` → `CONFORM_SELFTEST pass=9 fail=0` (`{W}/evidence/c8-after.txt`, `c8-after-selftest.txt`);
  the two M19 bypass fixtures are rejected (`c8-after-none.txt`, `c8-after-wait.txt`) where the r38 checker
  printed `CONFORM=met` (`c8-red-none.txt`, `c8-red-wait.txt`). Predicate P-C8 in the contract.
- C3 depth: `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0`
  (`{W}/evidence/gate-selftest-after.txt`); the r38 gate bytes fabricate `round_changed=[S001]` on fixture C
  and print stale on fixture D (`c9-red-a.txt`); v2 prints the predicate-word verdicts
  (`c9-after-fixture-a.txt`, `c9-after-fixture-c.txt`, `c9-after-fixture-d.txt`) and byte-identical
  lane-history lines (`c9-after-lane.txt`). Predicate P-C9 in the contract and the gate's PREDICATE.
- Frontier: S227 (gitrevisions), S228 (supersedes S226, corrected quote) — `corpus/SOURCES.md`,
  copies `corpus/evidence/sources-r39/`; lesson `corpus/lessons/round-39.md`; knowledge
  `corpus/knowledge/gate-ancestry-r39.md`.

## Hard bounds (every seat)
- Write EXACTLY ONE file: your report. The validator renders `Report: .ufo/waves/round-39/w1/<Name>.md`;
  that path is RELATIVE TO {LANE} — write it at {LANE}/<that path>. Scratch code/outputs only under
  {LANE}/.ufo/waves/round-39/scratch/<YourName>/ or $TMPDIR.
- The lane repo is READ-ONLY for you: never `git add/commit/push/fetch/reset/stash`, never any mutating
  jj command, never edit lane files. Read-only tool and counter runs are fine; mutation-testers run COPIES
  under their own scratch — never edit the lane's real files.
- Never touch: {FLEET}/MANIFEST.json, {FLEET}/.ufo/state/, {FLEET}/.ufo/watchdog.log, {FLEET}/templates/,
  {FLEET}/scripts/, sibling lane repos, ~/.omp/agent/config.yml, ~/.omp/agent/mcp.json.
- Detection and report only — no remediation, no kills, no config edits (mori province).
- Tooling directive (operator, 2026-10-19): you may install or upgrade tools that help the task — read
  `~/.omp/agent/RULES.md` first (official channels only; never pipe a remote script into a shell; record
  tool/version/channel/reason in your report). **pacman transactions are PAUSED host-wide**: install via
  `uv tool`/`npx`/an official binary in `~/.local/bin`, or file an L0 question. Never `pacman -Sy`,
  `-Syu`, `-U`, `-R`, downgrade, or restart a host service.
- Never use `agent://all`; your result is the report. Cite path:line or a command output for every claim;
  an unrun check has not passed.
"""


def item(name, role, target, acceptance):
    prompt = (GODSPEED + f"# Target\n{target}\n\n# Acceptance\n{acceptance}\n" + RULES)
    return {"name": name, "role": role, "prompt": prompt}


ITEMS = []
A = ITEMS.append

# ---- connector / scouts (recon)
A(item("ConnSibling", "connector",
  f"Scan sibling lanes' repos under {FLEET} for overlap with this round's surfaces: tools/mori-sources-appendonly.py ancestry semantics, wave-directory counters (count-c7/conform), and the gate-ancestry knowledge entry. Name any sibling artifact that already implements this work or that this round's gate-v2 change could break.",
  "Report a sibling-overlap table with paths and verdicts; FAIL if an overlapping sibling artifact is omitted."))
A(item("ScoutC7Bounds", "scout",
  f"Read {W}/count-c7.py and produce a bounds table for each of the five v2 checks (anchors_v2, capability_v2, live_rows_v2, named_row_drift, drift_kill_v2): what it proves, what it cannot prove, with line references. Include the disclosed verbatim-clone bound.",
  "Report check → proves → does-not-prove with line numbers; FAIL if any contract claim is stronger than the code."))
A(item("ExecC7Seeds", "executor",
  f"Replay `python3 {W}/count-c7.py {TIP}` at three seeds (20261024, 7, 99). Record each run's drawn state, all check lines, the negative lines and the verdict; confirm C7=met at all three and that the drawn state differs or not across seeds.",
  "Report the three runs' key lines; FAIL if any verdict differs from C7=met or a check line is seed-dependent beyond the drawn state."))
A(item("ExecC8Replay", "executor",
  f"Replay `python3 {W}/conform.py {TIP}` twice sequentially and both bypass-fixture runs from {W}/fixtures/make-m19-bypass.py (rebuild the fixtures from {ENTER} yourself). Record exit codes and the load-bearing FAIL lines. Then run two `conform.py {TIP}` processes concurrently and list the scratch dirs created.",
  "Report both honest runs' verdicts, both bypass rejections with their failing check names, and the concurrent scratch dirs; FAIL on a shared/seed-derived scratch path."))
A(item("ExecC9Dags", "executor",
  f"Rebuild the three fixture DAGs via `python3 {W}/fixtures/run-c9-dags.py <gate> {LANE} <out>` twice: once with the round-38 gate bytes (extract: `git -C {LANE} show {ENTER}:tools/mori-sources-appendonly.py`) and once with the v2 gate bytes (`git -C {LANE} show {TIP}:tools/mori-sources-appendonly.py`). Compare each block against {W}/evidence/c9-red-a.txt and the c9-after-fixture-*.txt receipts.",
  "Report both runs' timing/round_changed/exit lines per fixture; FAIL if any block contradicts its committed receipt."))

# ---- reviewers (independent re-derivation)
A(item("RevC7Anchors", "reviewer",
  f"Independently verify the anchors_v2 check at {TIP}: extract `corpus/knowledge/source-drift-content-anchor-r38.md` and tools/mori-source-drift.py at {TIP} (`git show {TIP}:<path>`), apply the ≥8-char and non-comment occurrence rule yourself (line-by-line), and compare with the counter's `check anchors_v2` line in {W}/evidence/c7-after.txt.",
  "Report per-anchor resolution (tool line numbers) and agreement; FAIL on any anchor that fails your own resolution or a counter detail that hides one."))
A(item("RevC7CapPath", "reviewer",
  f"Independently resolve every path in the SCORECARD capability row `source-drift re-fetch probe` at {TIP} with `git cat-file -t {TIP}:<path>` (must be blob), and verify no other SCORECARD row contains that capability key (the check reads the last single row).",
  "Report the path→type table and the row-count check; FAIL on a non-blob or an ambiguous row match."))
A(item("RevC7Live", "reviewer",
  f"Verify live_rows_v2 at {TIP}: parse {LANE}/.ufo/waves/round-37/evidence/drift-live-r37.txt at {TIP}, count per-row `S### drifted` lines vs the summary, check each named id is a registry row, and find each id's committed copy (`git ls-tree -r --name-only {TIP} corpus/evidence/` → sources-r<N>/<id>.<ext>, highest N).",
  "Report the counts, the id→copy-path table, and any id without a copy; FAIL on a mismatch with the counter's detail."))
A(item("RevC7Kill", "reviewer",
  f"Re-derive drift_kill_v2 end-to-end: run the probe's --selftest from bytes at {TIP} (extract to scratch), then a mutant with `return \"drifted\"` replaced by `return \"<state>\"` for each of the four drawn states. For each, verify the row_states FAIL detail's got table shows exactly the want-drifted rows reading the drawn state and everything else unchanged.",
  "Report the four mutants' got-vs-want comparison results; FAIL if any state flips a non-drifted row or leaves a drifted row unflipped."))
A(item("RevC7Negatives", "reviewer",
  f"Project each of the four witnesses in {W}/fixtures/ onto the real other bytes at {TIP} and name which v2 check rejects it: witness-token-entry.md, witness-dangling-row.md, witness-summary-only-live.txt, witness-comment-anchors.md. Then run `count-c7.py {TIP} --seed 20261024` and compare its four `negative` lines.",
  "Report a witness→failed-check table and the counter lines; FAIL if any witness passes all five v2 checks or a rejection reason differs from yours."))
A(item("RevC7Clone", "reviewer",
  f"Rebuild the fabricated self-consistent clone yourself (stub entry with the three real anchors; invented live receipt = real ten drifted rows plus `S103 drifted` with summary drifted=11; commit as a sandbox child of {TIP}). Run the r38 counter (`git show {ENTER}:.ufo/waves/round-38/count-c4.py`, fixtures beside it) and count-c7 on it.",
  "Report both verdicts with commands; FAIL unless the r38 counter prints C4=met and count-c7 prints C7=unmet with no_copy=['S103']."))
A(item("RevC8Value", "reviewer",
  f"Audit the timeout_value folder in {W}/conform.py: read `_resolve` and list what it can and cannot fold (Name via params/assignments, List/Tuple, Subscript, BinOp, UnaryOp, IfExp?). Then build three counter variants from count-c7 bytes with timeout=NAME where NAME binds to -1, to 0, and to a string; run the checker on each.",
  "Report the fold-capability list and the three variants' verdicts; FAIL if any non-positive or non-numeric variant passes timeout_value."))
A(item("RevC8Drain", "reviewer",
  f"Audit drain_shape in {W}/conform.py: verify that a counter whose Popen result is drained by a communicate in a DIFFERENT function fails, and one whose communicate result is unused (bare expression statement) fails. Build both variants from count-c7 bytes and run the checker.",
  "Report both variants' drain_shape verdicts; FAIL if either passes."))
A(item("RevC8Conjunct", "reviewer",
  f"Verify selftest_conjunct: run the strip test mentally/on a scratch copy of count-c7 (strip the first `proc.communicate(timeout=...)`), confirm the checker's rule catches it, and confirm the honest counter passes. Also verify the r38 selftest gap claim in {W}/evidence/m19-selftest-gap.txt against the r38 conform bytes at {ENTER}.",
  "Report both sides with commands; FAIL if the strip is not caught or the gap receipt misquotes the r38 bytes."))
A(item("RevC9Ancestry", "reviewer",
  f"Independently re-derive the fixture verdicts: build dag-a and dag-c with {W}/fixtures/run-c9-dags.py's machinery (import the gate module's _selftest_dag_cases/_make_dag_repo in a scratch script), then run `git merge-base --is-ancestor` yourself for each fixture's edit/landing commits and compare against the v2 gate's printed timing.",
  "Report your merge-base results vs the gate's lines for both fixtures; FAIL on any contradiction."))
A(item("RevC9Compat", "reviewer",
  f"Run the r37 C1 counter at {TIP}: `python3 {LANE}/.ufo/waves/round-37/count-c1.py {TIP} --seed 41` and confirm C1=met (its real arm reads gate bytes at 6bd57097, its drawn arm draws lane revs). Inspect the blind/real/challenge arm lines for malformed per-id lines caused by the new gate output.",
  "Report the arm lines and C1= verdict; FAIL on unmet or a malformed-line count > 0."))
A(item("RevC9Live", "reviewer",
  f"Re-run the gate at {TIP} and at e37dcc6 (both `--round-base {BASE}`) and diff your outputs against the round-38 receipts ({W}/../round-38/evidence/gate-after.txt and gate-after-e37dcc6.txt, ignoring the command:/predicate lines). Confirm the S069 receipt value sits at gate-after-e37dcc6.txt line 22.",
  "Report the diff results and the line-22 check; FAIL on any non-header difference or a wrong line number."))
A(item("RevC9Walk", "reviewer",
  f"Verify the walk claims in {W}/evidence/c9-after-lane.txt: count commits of `git log --full-history -- corpus/SOURCES.md` vs default at {TIP}; confirm 6531ac60 appears only with --full-history; verify the gate's log call carries %P parents (read the gate source at {TIP}).",
  "Report the counts and the source line; FAIL on any mismatch with the receipt."))
A(item("RevCensus", "reviewer",
  f"Re-run `bash {FLEET}/scripts/sources-census.sh validate --root {FLEET} mori`; count registry rows at {ENTER} and {TIP} (`git show <rev>:corpus/SOURCES.md | grep -c '^| S'`); verify no existing row's status/recheck/used-by cell changed between the two revs.",
  "Report exit code, row counts, and the append-only diff verdict; FAIL on a new error line, a count other than +2, or an in-place cell edit."))
A(item("RevGateS228", "reviewer",
  f"Verify S228: the row opens `supersedes S226`; the quoted sentence is verbatim at corpus/evidence/sources-r39/S228.src:657-659 (25 words or fewer); S228's landing commit descends from S226's landing commit (`git merge-base --is-ancestor`); the gate at {TIP} lists S226 in superseded_as_of; the S226 row at {ENTER} still prints the `:657-658` suffix.",
  "Report each check with its command output; FAIL on any mismatch."))
A(item("RevFreeze", "reviewer",
  f"Verify the freeze: recompute sha256 of every path listed in {W}/evidence/freeze-r39.txt at {TIP} and compare. Name any drift. Also verify the round-38 instruments under .ufo/waves/round-38/ are byte-identical to their bytes at {ENTER} (git show comparisons for count-c4.py, conform.py, count-c1.py, contract.md).",
  "Report the hash comparison table; FAIL on any drift not explained by a named new version."))
A(item("RevReceipts", "reviewer",
  f"Audit every file in {W}/evidence/: each receipt carries a `command:` first line, no absolute operator path other than the lane root, and its printed verdict matches the claim it supports (compare against the contract's C1-C3 after-values).",
  "Report a receipt→verdict→claim table and any hygiene defect; FAIL on a receipt whose command does not reproduce its output."))
A(item("RevScorecard", "reviewer",
  f"Re-derive each counting command in the SCORECARD round-39 declaration rows at {TIP}: run every command quoted in the before/after cells and compare printed literals verbatim (count-c7 C7=met; conform CONFORM=met + selftest 9/9; gate selftest 12/12; the red receipts' RED verdicts).",
  "Report a claim→declared-vs-observed table; FAIL on any cell whose literal the command does not print."))

# ---- mutation-testers
A(item("MutC7Cheat", "mutation-tester",
  f"Re-derive the cheat-probe discrimination: build the r38-M18 cheat probe (row_states detail always appends both `('S103', 'drifted')` and `('S103', 'excerpt')`), run the r38 drift_kill logic on it (PASS = red) and count-c7's drift_kill_v2 on a sandbox carrying it (must FAIL the check).",
  "Report both verdicts; PASS only if the r38 check accepts and drift_kill_v2 rejects."))
A(item("MutC8NoneVal", "mutation-tester",
  f"Re-derive bypass-none: run {W}/fixtures/make-m19-bypass.py {ENTER} {LANE} <scratch>, then the r39 checker on bypass-none.py; expected timeout_value FAIL (lines naming UNBOUNDED_DRAIN_S).",
  "Report the failing check lines; PASS only if timeout_value fails."))
A(item("MutC9IndexOrder", "mutation-tester",
  f"Mutation-test the gate's timing: take the v2 gate bytes at {TIP}, patch the timing decision back to index order (`landing > last_edit` style) in scratch; run its --selftest. Expected: the fixture-D case fails the mutant (selftest not 12/12).",
  "Report the mutant selftest tail; PASS only if pass=11 fail=1 (or worse) naming fixture D."))
A(item("CritC7Gaming", "critic",
  f"Attack P-C7: construct the strongest fabricated binding that still passes all five v2 checks without doing the claimed work (consider: anchors copied from code positions, a receipt naming only rows with copies, a probe that prints expected tables). Read {W}/contract.md's disclosed bound and state whether your construction refutes it or fits inside it.",
  "Report the strongest construction and whether it refutes the disclosed bound; if it passes, name exactly which check should tighten and why the current P-C7 bound permits it."))
A(item("CritC8Gaming", "critic",
  f"Attack P-C8: can a counter pass all nine checks while being unreplayable or unbounded? Consider computed timeouts (function calls, getattr, conditional rebinding of the budget), a communicate drained via a helper alias, or a mkdtemp dir passed positionally. Read {W}/conform.py.",
  "Report the strongest bypass and whether the checker or its selftest catches it; name the missing mutation if any."))
A(item("CritC9Semantics", "critic",
  f"Attack P-C9's words against the implementation: the re-add rule on linear histories, 'latest superseding row' selection on incomparable branches, last-edit attribution when two incomparable commits edit the same id, and nearest_path_commit fallback. Which contract sentence is stronger than the code, if any?",
  "Report a sentence-by-sentence verdict table; FAIL (the round) if any sentence exceeds the code without being named in the contract's disclosed bounds."))

# ---- sentinels / simplifier / scribes
A(item("SentCounters", "sentinel",
  f"Security-review {W}/count-c7.py and {W}/conform.py: --tool/--repo path handling, symlink behavior, scratch permissions, the executed-tool boundary (count-c7 runs the probe under test; conform runs counters), and the hang fixture's process group.",
  "Report findings by severity with lines; FAIL if a HIGH is omitted or a MEDIUM/LOW is claimed fixed without a check."))
A(item("SimpCounters", "simplifier",
  f"Find dead weight in {W}/count-c7.py and {W}/conform.py (unused constants such as ROWSTATES_RE or has_communicate_timeout, unused flags, duplicated logic). Do NOT edit the lane files — the freeze pins them; propose deletions routed to round 40.",
  "Report a deletion list with line ranges and the behavior-preserving argument; FAIL on a proposal that changes a predicate, a check, or a printed line."))
A(item("ScribeLesson", "scribe",
  f"Verify `corpus/lessons/round-39.md`: the Gate rows' quotes are verbatim in corpus/evidence/sources-r39/S227.src (lines 2542-2544) and S228.src (657-659) with ≤25 words; M20-M22 each carry evidence pointers that resolve at {TIP} and a fix shown able to fail by a runnable command.",
  "Report a row-by-row verification table; FAIL on a misquote, a word count over 25, or a fix without a fail-showing command."))

SPEC = {
    "wave": "mori-r39-w1",
    "reportDir": ".ufo/waves/round-39/w1",
    "maxLanes": 32,
    "context": CONTEXT,
    "items": ITEMS,
}

with open(LANE + "/.ufo/waves/round-39/w1-spec.json", "w") as fh:
    json.dump(SPEC, fh, indent=1)
    fh.write("\n")

import collections
print("items", len(ITEMS))
print(collections.Counter(i["role"] for i in ITEMS))
print("written", LANE + "/.ufo/waves/round-39/w1-spec.json")
