#!/usr/bin/env python3
"""Generate the round-38 wave-2 spec (falsify, v1 band) next to this file.

Run: python3 .ufo/waves/round-38/gen-wave2-spec.py
Writes: .ufo/waves/round-38/w2-spec.json
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
W = LANE + "/.ufo/waves/round-38"
TIP = "f725f3076972e6e70595b5ac8279be524a111ff8"
ENTER = "e33bb561712b32f46861362a3fa43762fa70ae4f"
BASE = "f10a320d"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""

CONTEXT = f"""# mori round 38 — wave 2 (falsify), L1 MoriR38

Lane repo: {LANE} (jj-colocated; git is the backend). Fleet repo: {FLEET} (read-only for you).
Scored tip under attack: {TIP} (pushed). Entering tip: {ENTER}.

This is the round's second wave: fresh seats attack what wave 1 produced. Wave 1's C4 attack
seats (critic + four mutation-testers) died when the orchestrator session froze; their gaps are
this wave's items. Every finding must be re-derived by running the command, not read from a report.

## Claims under attack (frozen in {W}/contract.md)
- C1 (calibration): `python3 .ufo/waves/round-38/count-c4.py {TIP}` must print `C4=met`, exit 0:
  four content checks (`anchors`, `capability`, `live_rows`, `named_row_drift`+`drift_kill`) PASS and
  three fabricated witnesses are rejected. Before at `e37dcc6`: `C4=unmet`, exit 1
  (`{W}/evidence/c4-before.txt`). Token-discrimination control: the round-37 counter prints
  `C2=met` on the fabricated sandbox while `count-c4.py` prints `C4=unmet`
  (`{W}/evidence/v3-token-control.txt`, `{W}/evidence/c4-witness.txt`).
- C2 (operability): `python3 .ufo/waves/round-38/conform.py {TIP} --counter .ufo/waves/round-38/count-c1.py --counter .ufo/waves/round-38/count-c4.py`
  must print `CONFORM=met`, exit 0: six checks PASS on six mutations each flipping its own check
  (`{W}/evidence/c5-before.txt`, `c5-after.txt`, `c5-after-selftest.txt`).
- C3 (depth): `python3 tools/mori-sources-appendonly.py {TIP} --round-base {BASE}` prints
  `supersede_timing superseded_as_of=[...] stale_supersede=[]`; at `e37dcc6` it prints
  `stale_supersede=[S069]` (`{W}/evidence/gate-before.txt`, `gate-after.txt`,
  `{W}/evidence/gate-after-e37dcc6.txt`, `gate-selftest-after.txt`, `gate-selftest-before.txt`).

## Hard bounds (every seat)
- Write EXACTLY ONE file: your report. The validator renders `Report: .ufo/waves/round-38/w2/<Name>.md`;
  that path is RELATIVE TO {LANE} — write it at {LANE}/<that path>. Every `Report:` trailer path is
  relative to {LANE}.
- Scratch code/outputs only under `{LANE}/.ufo/waves/round-38/scratch/<YourName>/` or `$TMPDIR`.
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
  claim; an unrun check has not passed. A dead command is not a pass.
"""


def item(name, role, target, acceptance):
    prompt = (GODSPEED + f"# Target\n{target}\n\n# Acceptance\n{acceptance}\n")
    return {"name": name, "role": role, "prompt": prompt}


ITEMS = []
A = ITEMS.append

# ---------------- C1: content-anchor counter (calibration) ----------------
A(item("RevC4Anchors", "reviewer",
  f"Independently verify P-C4's anchor check at `{TIP}`. Read P-C4 in `{W}/contract.md`, list every `anchor:` line in `{LANE}/corpus/knowledge/source-drift-content-anchor-r38.md`, and resolve each string with `grep -F` in `git show {TIP}:tools/mori-source-drift.py`. Then run `python3 .ufo/waves/round-38/count-c4.py {TIP}` and compare its `check anchors` detail with your own resolution. Watch for anchors that exist only inside comments or dead code.",
  "Report each anchor with its tool line and whether it is executable or comment-only; report the counter's anchors detail. FAIL on any anchor that does not resolve, or a counter verdict that hides one."))
A(item("RevC4Capability", "reviewer",
  f"At `{TIP}`, independently resolve every path cited by the SCORECARD capability row `source-drift re-fetch probe`: `git cat-file -e {TIP}:<path>` for each backticked path. Compare with the counter's `check capability` detail. Also check whether the counter reads the row's last occurrence (a later row could shadow it).",
  "Report the resolved/missing table and the counter detail; FAIL if any cited path fails to resolve at the tip, if the counter misses one, or if last-row-wins lets a later row shadow the target."))
A(item("RevC4Live", "reviewer",
  f"Verify `live_rows` at `{TIP}`: parse `{LANE}/.ufo/waves/round-37/evidence/drift-live-r37.txt`, count `<S###> drifted`/per-row lines and the summary's `drifted=` value, and check every named id is a registry row at `{TIP}` (`grep -E '^\\| S[0-9]{{3}} '`). Compare with `check live_rows`.",
  "Report the counts, the id membership and the counter detail; FAIL on any mismatch, a duplicate id, or an id outside the registry."))
A(item("RevC4Negatives", "reviewer",
  f"Name which of the four content checks each of `{W}/fixtures/witness-token-entry.md`, `witness-dangling-row.md`, `witness-summary-only-live.txt` fails when projected onto the real other bytes at `{TIP}`. Then run `count-c4.py {TIP}` and compare its three negative lines.",
  "Report a witness→failed-check table and the counter's three negative lines; FAIL if any witness passes all four checks, or the counter's rejection reason differs from yours."))
A(item("CritC4Gaming", "critic",
  f"Build the strongest fabricated binding that satisfies all four P-C4 checks without doing the claimed work, using scratch only (e.g. an anchor string present only in a comment; a live receipt whose per-row lines are copied from another round's rows; a capability path resolving to an unrelated file; a named-row arm satisfied by a fixture-only path). Test it against a sandbox built from `{TIP}` with `count-c4.py --repo`.",
  "Report the construction, whether `C4=met` accepts it, and the exact check that stays silent. If accepted, name the tightening that would reject it; if rejected, name the check that kills it and the false-positive risk of that check."))
A(item("MutC4Anchor", "mutation-tester",
  f"Mutate a scratch copy of `corpus/knowledge/source-drift-content-anchor-r38.md`: change one byte inside one `anchor:` string. Build a sandbox clone of `{LANE}` at `{TIP}`, commit the mutant there, and run `python3 .ufo/waves/round-38/count-c4.py {TIP} --repo <sandbox>`.",
  "Report the mutant's `check anchors` line and `C4=` verdict with exit code; PASS only if the mutant flips anchors to FAIL. Restore/report the sandbox hash and confirm the lane files were untouched (`git -C {LANE} status --porcelain -- corpus/knowledge/source-drift-content-anchor-r38.md` empty)."))
A(item("MutC4CapPath", "mutation-tester",
  f"Mutate a scratch copy of `SCORECARD.md` so the `source-drift re-fetch probe` row cites `evidence/no-such-file.txt`; sandbox as in MutC4Anchor and run `count-c4.py {TIP} --repo <sandbox>`.",
  "Report the mutant's `check capability` line and `C4=` verdict with exit code; PASS only if the mutant flips capability to FAIL. Confirm the lane `SCORECARD.md` was untouched."))
A(item("MutC4Live", "mutation-tester",
  f"Mutate a scratch copy of `.ufo/waves/round-37/evidence/drift-live-r37.txt` to keep the summary sentence and drop the per-row lines; sandbox as in MutC4Anchor and run `count-c4.py {TIP} --repo <sandbox>`. Also try a variant that keeps the rows but changes one named id to an unregistered S999.",
  "Report both mutants' `check live_rows` lines and `C4=` verdicts; PASS only if each mutant flips live_rows to FAIL. Confirm lane files untouched."))
A(item("MutC4KillAlt", "mutation-tester",
  f"In a scratch copy of `tools/mori-source-drift.py` at `{TIP}`, replace `return \"drifted\"` with `return \"fresh\"`, run `--selftest` on the copy, then run `count-c4.py`'s `drift_kill` logic over a sandbox carrying that tool. Compare with the shipped mutation (`return \"excerpt\"`).",
  "Report whether `selftest row_states` fails and whether S103 is named under the alternative mutation, and the counter's `drift_kill` detail; PASS only if the kill check rejects a different mutation of the same branch."))
A(item("ScoutC4Bounds", "scout",
  f"Read `{W}/count-c4.py` and enumerate what each of its four content checks proves and cannot prove, with line references; include the `anchor:` substring rule, the capability last-row rule, the live-row grammar, and the mutation arm. Also read the knowledge entry `{LANE}/corpus/knowledge/source-drift-content-anchor-r38.md` and list any sentence stronger than the code supports.",
  "Report a bounds table (check → proves → does not prove) with line numbers and an overclaim list; FAIL if any claim in P-C4 or the entry is stronger than the code."))
A(item("RevC4Before", "reviewer",
  f"Reproduce the C1 before-state at `{ENTER}`/`e37dcc6` exactly as `{W}/evidence/c4-before.txt` prints it: run `python3 .ufo/waves/round-38/count-c4.py e37dcc6` from `{LANE}`. Explain the `check capability` line's mix of `.ufo/waves/...` and `evidence/...` paths and whether the missing-path trigger is the genuine one.",
  "Report the full five check lines plus `C4=` and exit code; FAIL if they differ from the receipt, or if the before-state passes the counters it must fail."))
A(item("RevC4WitnessControl", "reviewer",
  f"Re-derive the discrimination control: build the witness sandbox from `{W}/fixtures/make-witness-sandbox.py` at `{TIP}` into your own scratch, run the round-37 counter `{W}/../round-37/count-c2.py <sandbox-commit> --repo <sandbox>` and `count-c4.py <sandbox-commit> --repo <sandbox>`. Verify the sandbox's identity signals (path, author, title) do not impersonate the lane.",
  "Report both verdicts and the sandbox identity evidence; FAIL if the r37 counter does not print `C2=met`, the r38 counter does not print `C4=unmet`, or the sandbox could be mistaken for the lane. Record the Medium `--out` escape finding if it persists."))

# ---------------- C2: conformance checker (operability) ----------------
A(item("RevC5Predicate", "reviewer",
  f"Independently compare the contract's P-C1 blockquote (section `P-C1 of record` in `{W}/contract.md`) with `python3 .ufo/waves/round-38/count-c1.py --print-predicate` after whitespace normalisation. Reproduce the r37 defect: diff the r37 contract's first P-C1 blockquote against `{W}/../round-37/count-c1.py --print-predicate`.",
  "Report both normalised lengths, equality booleans, and the r37 inequality; FAIL if the r38 pair differs, or the r37 defect is not reproduced as the check's motivation."))
A(item("RevC5Pin", "reviewer",
  f"Verify `head_pin`: run `python3 .ufo/waves/round-38/conform.py {TIP} --print-pin-only` (or the checker's declared flag) and compare with `git -C {LANE} rev-parse {TIP}` and `git rev-parse master`. Check what happens when `--pin-only` is given a non-tip revision (does it still print the lane tip?).",
  "Report every printed pin, the rev-parse values, and the non-tip behaviour; FAIL if the pin is not the lane tip, is not 40 lowercase hex, or the checker reports PASS for a pin it did not compare to the tip."))
A(item("RevC5Tool", "reviewer",
  f"Verify `tool_resolve`: from `{LANE}` and from `/` run the checker's `--print-tool .ufo/waves/round-38/fixtures/summary-only.py` and confirm it returns the absolute lane path both times. Then test a path outside the lane (`/etc/passwd`) and a `..`-escaping path.",
  "Report the printed paths and exit codes for all four calls; FAIL if a lane-relative path does not resolve to the lane absolute path, or an outside/escaping path is accepted silently."))
A(item("RevC5Bounds", "reviewer",
  f"Audit `bounded_reads` independently: parse `{W}/count-c1.py` and `{W}/count-c4.py` with Python's `ast`, list every `subprocess.run`/`Popen` call and whether it carries a `timeout` keyword, and find the committed-blob read's byte cap. Compare with the checker's detail line.",
  "Report the AST table (call site, timeout present/absent, cap) and the checker detail; FAIL if any call lacks a timeout, the cap is absent, or the checker reports PASS on a call it did not parse."))
A(item("RevC5Timeout", "reviewer",
  f"Re-derive `timeout_state`: run the checker with `--tool-timeout 5` and `{W}/fixtures/hang-after-flush.py` (use the checker's declared flags), and separately run `count-c1.py` with the same tool to see its raw verdict. Confirm the verdict is `C1=unmet` with a `tool_timeout` reason, never `C1=met` and never a silent pass.",
  "Report both outputs and exit codes, and the elapsed seconds; FAIL if any path prints `C1=met` on the hanging tool or hides the timeout as a generic unmet."))
A(item("RevC5Scratch", "reviewer",
  f"Verify `scratch`: grep every `mkdtemp` in `{W}/count-c1.py` and `{W}/count-c4.py`, check each passes `dir=` under `{LANE}/.ufo/waves/round-38/scratch`, and confirm no `mkdtemp()` without `dir=` remains. Run the checker and compare its detail.",
  "Report each mkdtemp line (file:line, dir argument) and the checker detail; FAIL if any scratch directory is created outside the round-38 scratch root or the checker's PASS is not backed by the grep."))
A(item("MutC5Predicate", "mutation-tester",
  f"Mutate a scratch copy of `count-c1.py` so `--print-predicate` differs from the contract by a non-whitespace token; run `conform.py {TIP} --counter <mutant> --counter {W}/count-c4.py`.",
  "Report the `predicate` line and the `CONFORM=` verdict with exit code; PASS only if exactly the predicate check flips to FAIL. Confirm the lane counters were not modified."))
A(item("MutC5Pin", "mutation-tester",
  f"Mutate a scratch copy of `count-c1.py` so `--pin-only` prints the entering tip `{ENTER}` instead of the lane tip; run `conform.py {TIP} --counter <mutant> --counter {W}/count-c4.py`.",
  "Report the `head_pin` line and `CONFORM=` verdict with exit code; PASS only if exactly `head_pin` flips. Confirm lane counters untouched."))
A(item("MutC5Timeout", "mutation-tester",
  f"Mutate a scratch copy of `count-c1.py` so a tool that flushes then hangs maps to a pass (or to a plain unmet without a timeout reason); run `conform.py {TIP} --counter <mutant> --counter {W}/count-c4.py`.",
  "Report the `timeout_state` line and `CONFORM=` verdict with exit code; PASS only if `timeout_state` flips to FAIL. Confirm lane counters untouched."))
A(item("MutC5Scratch", "mutation-tester",
  f"Mutate a scratch copy of `count-c1.py` to call `tempfile.mkdtemp()` without `dir=` (system temp); run `conform.py {TIP} --counter <mutant> --counter {W}/count-c4.py`.",
  "Report the `scratch` line and `CONFORM=` verdict with exit code; PASS only if `scratch` flips to FAIL. Confirm lane counters untouched."))
A(item("CritC5Gaming", "critic",
  f"Ask whether the six checks can all PASS on a counter that is still wrong: e.g. a counter whose `--print-predicate` is hardcoded to the contract, whose `--pin-only` echoes the argument, whose timeout mapping is never exercised by any real arm, or whose scratch path is the round root. Inspect `{W}/conform.py` and `{W}/count-c1.py` and test the strongest case in scratch.",
  "Report the construction and whether `CONFORM=met` survives it; if it does, name the missing check and the exact false-pass; if not, name the check that kills it."))
A(item("RevC5Selftest", "reviewer",
  f"Run `python3 .ufo/waves/round-38/conform.py --selftest` and independently inspect all six mutations the checker applies: for each, confirm the mutated bytes differ non-trivially from the pristine and that the declared check is the only one that flips. Report the pass/fail tally.",
  "Report the selftest tally and a per-mutation table (mutation, check expected, observed flip); FAIL if a mutation is whitespace-only or a second check flips."""))

# ---------------- C3: timed supersede (depth) ----------------
A(item("RevGateTiming", "reviewer",
  f"Re-derive `supersede_timing` at `{TIP}`: run `python3 tools/mori-sources-appendonly.py {TIP} --round-base {BASE}`; for S069 and S073 independently recover the commit order (`git log --format='%H %ad' -- <path>` filtered by the rows' landing commits) and check the as-of/stale classification the gate prints. Report the full timing line.",
  "Report the timing line, the S069/S073 commit order evidence, and the classification; FAIL if any id is classified against the observed commit order or the line is absent."))
A(item("RevGateTimingE37", "reviewer",
  f"At `e37dcc6` run the same gate command and verify `stale_supersede=[S069]`; explain why S073 cannot dispose S069's in-place edit at `62db24c`. Also check whether any other id should be stale at that revision but is not.",
  "Report the timing line at `e37dcc6`, the S069/S073 order, and any missed stale id; FAIL if S069 is not stale at `e37dcc6` or another stale id is silently classified as-of."))
A(item("MutGateTiming", "mutation-tester",
  f"In a scratch copy of `tools/mori-sources-appendonly.py` at `{TIP}`, replace the first-landing/maximum logic with presence-based classification (or the buggy `if index > previous[0]` overwrite quoted in lesson M3), then run it at `e37dcc6` and `{TIP}`. Compare with the shipped gate.",
  "Report both timing lines and whether the mutation lists S069 in `superseded_as_of` at `e37dcc6`; PASS only if the mutant is killed by the stale-set or by the selftest fixture, and the lane tool was untouched."))
A(item("RevGateS226", "reviewer",
  f"Verify S226 in `{LANE}/corpus/SOURCES.md`: its `teaches` opens `supersedes S069`, its row is well-formed, and its landing commit postdates `62db24c` on the file's history. Check `git log --format='%h %ad %s' -S 'S226' -- corpus/SOURCES.md` and the row's source copy `{LANE}/corpus/evidence/sources-r38/S226.src`.",
  "Report the row text, the landing commit and its order vs `62db24c`, and the source-copy quote; FAIL if the row is malformed, does not supersede S069, or lands before the edit."))
A(item("CritGateSemantics", "critic",
  f"Attack P-C6's `descendant` wording versus the code's per-path commit walk: construct a case (or find one in the lane history) where a superseding row lands in a merge/parallel branch such that `git log -- <path>` order and true ancestry disagree. Read `{W}/contract.md` P-C6 and the gate's implementation.",
  "Report the strongest counterexample or an argued impossibility with the command that would show it; FAIL if the contract says descendant while the code only uses path history and no bound is disclosed."))
A(item("RevGateCompat", "reviewer",
  f"Compare the gate's output at `{ENTER}`, `e37dcc6` and `{TIP}` on the fields other than `supersede_timing` (ids, deleted, superseded, round_changed, per-id changed lines). Confirm adding the timing field changed no pre-existing verdict, and that the new selftest cases are additive.",
  "Report a field-by-field diff table and the selftest case count before/after; FAIL on any changed pre-existing verdict not disclosed, or a removed selftest case."))
A(item("RevGateSelftest", "reviewer",
  f"Run `python3 tools/mori-sources-appendonly.py --selftest` and inspect the two new cases (supersede after edit, supersede before edit) in the tool source. Verify the before-edit fixture actually lists its id in `stale_supersede` and that the after-edit case prints `sto=[]`.",
  "Report the tally, both new case outputs and their fixture bytes; FAIL if the before-edit case does not list the id, or the tally regressed."))
A(item("RevGateRegistry", "scout",
  f"Check the `SKILL.md` gate registry at `{TIP}` for the append-only gate's row: entry command, verdict map, selftest command, pinned values, write scope. Verify the row's selftest spelling and the new `supersede_timing` description exist and resolve. Also check the r38 instruments' rows.",
  "Report the rows' cells and any missing field from the Gate standard's registry schema; FAIL if the gate or r38 instruments lack a complete row."))

# ---------------- frontier / corpus / bookkeeping ----------------
A(item("RevS226Row", "scribe",
  f"Verify the frontier step's record: `{LANE}/corpus/lessons/round-38.md` `## Gate` must record S226's URL, access date and a ≤25-word located quote; `## Mistakes` must carry M1–M6 with class/evidence/captured-by/fix. Re-open `corpus/evidence/sources-r38/S226.src` and locate the quote. Check every mistake's \"shown able to fail\" claim against a receipt.",
  "Report the quote with its location, the mistake-table completeness, and any claim not backed by a receipt; FAIL on a missing quote, a >25-word quote, or a fix with no red-before state."))
A(item("RevCensusFresh", "reviewer",
  f"Re-run `bash {FLEET}/scripts/sources-census.sh validate --root {FLEET} mori` and compare line-by-line with `{W}/evidence/census-start.txt` (which carries a `CENSUS_EXIT` trailer). Count registry rows at `{ENTER}` and `{TIP}` with the contract's frozen grep. Check the round's lesson census paragraph matches.",
  "Report exit code, the diff against the start receipt, the row delta and the lesson's claim; FAIL on any E-line, a row delta other than the claimed +1, or a lesson claim the command does not reproduce."))
A(item("RevLessonGate", "scribe",
  f"Audit `{LANE}/corpus/lessons/round-38.md` as a round lesson: `## Gate` present with candidates/admitted/rejected/spot-check; `## Mistakes` rows use the mistakes.md vocabulary; every registry status/recheck/used-by change is logged old→new (or 'none' is true). Verify the spot-check duty: a non-author spot-check of at least one admit and one reject — if absent, say so.",
  "Report a section-by-section conformance table with line numbers; FAIL on a missing section, an unlogged cell change, or an unlabeled absence of the non-author spot-check."))
A(item("RevQualityRows", "reviewer",
  f"Read the round-38 additions to `{LANE}/corpus/QUALITY.md` (rows 108–110) and verify each criterion cites the lesson that produced it, states an observable fail state, and is not satisfied by the lane's own fabricated witnesses. Check the row numbering is append-only and no earlier row was rewritten (`git diff {ENTER} {TIP} -- corpus/QUALITY.md` must be additions only).",
  "Report each row's citation, fail state and the diff stat; FAIL on an uncited criterion, an unobservable fail state, a rewritten earlier row, or one the fabricated witnesses satisfy."))
A(item("RevScorecardClaims", "reviewer",
  f"Re-derive each of the SCORECARD round-38 claim rows at `{TIP}`: run every counting command in the before→after cells and compare the printed before and after values verbatim with the cells. Specifically compare claim 3's after cell against the gate's real `supersede_timing` line. Check the capability rows' paths resolve and the axes cells claim no wrong move.",
  "Report a claim→declared-vs-observed table; FAIL on any cell whose literal value the command does not print, any unresolved capability path, or an axis move contradicted by the receipts."))
A(item("RevTrends", "scribe",
  f"Re-derive the round's three trend verdicts from committed bytes at `{TIP}`: expansion (new knowledge entries citing mined rows on uncovered ground), quality (superseded/re-verified entries with no failing recheck), discernment (gate decisions vs outside spot-check, QUALITY criteria grounded in lessons). Cite receipt paths for each.",
  "Report one verdict per trend with evidence pointers and the counter-evidence you found; FAIL if a verdict is asserted without a receipt, or the discernment row hides that no non-author spot-check exists yet."))
A(item("ConnReceipts", "connector",
  f"Map every claim and every evidence pointer in `{W}/contract.md`, the SCORECARD round-38 rows and `{LANE}/corpus/lessons/round-38.md` to an existing file at `{TIP}` (`git cat-file -e {TIP}:<path>`), a re-runnable command, or a commit. List orphan pointers (named but absent), stale pointers (named but a different round's), and pointers that resolve only in the working tree.",
  "Report an orphan/stale/working-tree-only table with the resolution command per row; FAIL on any orphan or working-tree-only pointer in a claim's evidence."))
A(item("SimpR38", "simplifier",
  f"Find dead weight the round added: duplicate evidence receipts, superseded artifacts still cited, redundant fixtures, counters' unused flags, or report-only files that duplicate a receipt. Detection only — propose deletions/replacements with the exact path and what would be lost.",
  "Report a table (path, why dead, what depends on it, proposal); FAIL if you propose deleting anything a committed claim or the closure gate cites, or edit a file."))
A(item("RevMisroot", "reviewer",
  f"Run `git -C {FLEET} status --porcelain` (no pathspec) and inspect every untracked file whose content names mori/round-38. The known candidate is `.ufo/waves/round-38/scratch/RevC4Anchors/mori-source-drift-f725f30.py`; verify whether it is a seat misroot that must be copied byte-exact into the lane and removed from the fleet root, and whether any other fleet-root file is a mori seat misroot.",
  "Report each candidate with a sha256 and byte-exact `cmp` plan, and the final disposition; FAIL if a mori-seat fleet-root file is left unnamed or an unrelated lane's file is proposed for deletion."))
A(item("RevIndexClean", "reviewer",
  f"Audit `{W}/dispatch-log.txt` against the five round-38 commits (`{ENTER}..{TIP}`): QUALITY 103's second clause requires an index-clean record after every `landed` line. Run `bash tools/mori-index-clean.sh {LANE}` yourself and report its staged/intent_to_add values. Identify every commit with no record and whether the log discloses it.",
  "Report a commit→record table, the live index-clean output, and each missing record; FAIL if a landed line lacks a following clean-index record and the log does not disclose the gap."))
A(item("RevSHONEN", "reviewer",
  f"Check `{LANE}/SHONEN.md` against the canonical seed block in `{FLEET}/PROTOCOL.md` (file contract table, byte-identical modulo the name) and report the current marks. Then check whether this round's evidence can support a non-author `[x]` on any box — do not write `[x]` yourself; name which box a non-author could check and the evidence pointer.",
  "Report the seed diff (empty or the exact lines) and a per-box assessment with evidence pointers; FAIL if the seed differs, a mark carries no pointer, or an `[x]` exists without a named non-author verifier."))


SPEC = {
    "wave": "mori-r38-w2",
    "reportDir": ".ufo/waves/round-38/w2",
    "maxLanes": 64,
    "context": CONTEXT,
    "items": ITEMS,
}

with open(LANE + "/.ufo/waves/round-38/w2-spec.json", "w") as fh:
    json.dump(SPEC, fh, indent=1)
    fh.write("\n")

import collections
print("items", len(ITEMS))
print(collections.Counter(i["role"] for i in ITEMS))
print("written", LANE + "/.ufo/waves/round-38/w2-spec.json")
