#!/usr/bin/env python3
"""Generate the wave-2 (falsify) spec for mori round 36 — JSON written next to this file."""
import json, os

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
W2 = LANE + "/.ufo/waves/round-36/w2"
TIP = "bf0df77fee4b6ef54a90aea09335c7617f125151"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""

CONTEXT = f"""# mori round 36 — wave 2 (falsify + verify), attempt 2 (L1 MoriR36)

Lane repo: {LANE} (jj-colocated; git is the backend). Fleet repo: {FLEET} (read-only for you).
Landed data tip: {TIP} (pushed). Round base (entering): 6bd57097.

## Claims under attack
- C2 (measured, operability): `python3 tools/mori-sources-appendonly.py` — frozen predicate P-C2 in
  {LANE}/.ufo/waves/round-36/contract.md; counter `.ufo/waves/round-36/count-c2.py` (sha256 pinned in
  evidence/freeze-v2.txt); data receipt evidence/c2-after.txt (C2=met, blind 24/24, real arm pass).
- C1 (exploratory, freshness technique; declared before data by attempt 1): probe
  `python3 tools/mori-source-drift.py` — P-C1 byte-behavior receipt evidence/c1-after.txt
  (blind 40/40 mismatches=0; real arm oracle_fetched=58 fresh=49 drifted=9 excluded=0 mismatches=0).
  C1 admits NO freshness verdict; it verifies only as unprovable-but-better with a named non-author
  reviewer, else lands unprovable. Attack any place that infers freshness admission from it.
- Routed round-35 repairs: SOURCES supersede rows S205–S220 (18 in-place-edited ids discharged),
  gate registry rows in SKILL.md, QUALITY 103–105, index-clean gate.

## Hard bounds (every seat)
- Write EXACTLY ONE file: your report at {W2}/<YourName>.md . The `Report:` trailer path is relative to
  {LANE} — write it at {LANE}/<that path>. Scratch code/outputs only under
  /fast/scratch/hyaku/mori-r36/<YourName>/ or $TMPDIR.
- The lane repo is READ-ONLY for you: never `git add/commit/push/fetch/reset`, never any mutating jj
  command, never edit lane files. Running the lane's own read-only tools is fine; mutation-tester seats
  run the FROZEN COUNTER with a `--tool` control/mutant path — never edit the lane's real tool.
- Never touch: {FLEET}/MANIFEST.json, {FLEET}/.ufo/state/, {FLEET}/.ufo/watchdog.log,
  {FLEET}/templates/, {FLEET}/scripts/, sibling lane repos, ~/.omp/agent/config.yml, ~/.omp/agent/mcp.json.
- No remediation, no kills, no config edits — detection and report only (mori province).
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task via
  official channels (uv tool / npx / official binary into ~/.local-bin), and MUST record any
  install — tool, version, channel, reason — in your report. pacman guard: ALL pacman transactions are
  PAUSED host-wide; never run pacman.
- Every measurement in your report carries its command and observed output. End with VERDICT: PASS
  (no defect found) or FAIL (defect, with path:line evidence). Name what your item attacks.

## Where things stand (measured by L1 after the data commit)
- count-c2.py {TIP}: C2=met, seed 15440749816798970567, evidence/c2-after.txt.
- count-c1.py {TIP}: C1 byte-evidence met, seed 7388485190103051243, evidence/c1-after.txt.
- Round append-only gate: `python3 tools/mori-sources-appendonly.py {TIP} --round-base 6bd57097`
  -> round_changed=[] exit 0. Index clean: staged=0 intent_to_add=0.
- wave-1 (attempt 1, settled): 33 seats, 28 reports under .ufo/waves/round-36/w1/, dead: MutC1Novel,
  MutC2Novel (provider rate limit), refused-hold: CritC1Counter, CritC2Counter (provider cyber_policy).
  C0: 25 controls, all unmet under v2 (evidence/c0-rescore-v2.txt), REF references met.
"""

def item(name, role, body):
    return {"name": name, "role": role,
            "prompt": GODSPEED + "\n# Target\n" + body +
                      "\n\nReport: .ufo/waves/round-36/w2/%s.md\n" % name}

items = []

# ---------------- executors (run commands; capture output into the report)
items.append(item("ExecReC2A", "executor", f"""Re-score the measured claim with a fresh draw.
cd {LANE} && python3 .ufo/waves/round-36/count-c2.py {TIP}
Paste the full output and exit code. Verify: first line is the P-C2 sentence byte-identical to
{LANE}/.ufo/waves/round-36/contract.md:23; blind arm 24/24; real arm pass with ids listing exactly
18 ids; final line C2=met; a fresh seed is printed. Also `sha256sum .ufo/waves/round-36/count-c2.py`
and compare to evidence/freeze-v2.txt."""))

items.append(item("ExecReC2B", "executor", f"""Determinism check across fixed seeds.
cd {LANE} && python3 .ufo/waves/round-36/count-c2.py {TIP} --seed 42 and again --seed 7.
Paste both outputs. Verify both score C2=met and that the real-arm lists (ids/deleted/superseded/
round_changed) are identical across seeds while the blind-arm sandbox histories differ (drawn at run
time). Flag any seed-dependent verdict."""))

items.append(item("ExecReC1A", "executor", f"""Re-score the C1 byte predicate with a fresh draw (network).
cd {LANE} && python3 .ufo/waves/round-36/count-c1.py {TIP}
Paste the full output and exit code. Verify: P-C1 sentence byte-identical to contract.md:21; blind
40/40 mismatches=0; real arm fetched>=10 with fresh>=1 and drifted>=1, mismatches=0; C1=met; fresh
seed printed; counter sha256 matches evidence/freeze-v2.txt. Note this run is byte-behavior evidence
only, NOT a freshness admission (see w1/CritAxisFit.md)."""))

items.append(item("ExecGateRound", "executor", f"""Round landing gate checks.
cd {LANE} && python3 tools/mori-sources-appendonly.py {TIP} --round-base 6bd57097 (expect
round_changed=[] exit 0) and without --round-base (expect 18 ids, exit 1). Paste both. Verify the
ids list is the gate's own `ids=[...]` line (count 18 per `evidence/c2-after.txt:6` and QUALITY
102:809 — criterion 104 names no ids) and that every id has a `supersedes S<NNN> —` row at the tip
(`grep -cE 'supersedes S[0-9]{3}' corpus/SOURCES.md` returns 35 lines / 37 occurrences, not 18; the
carried-id subset is a different set from that count)."""))

items.append(item("ExecIndexClean", "executor", f"""Index-clean gate live check.
cd {LANE} && bash tools/mori-index-clean.sh {LANE} (expect staged=0 intent_to_add=0 exit 0) and
git status --porcelain --untracked-files=no (expect empty). Paste both outputs. List any tracked
dirty file as a FAIL."""))

items.append(item("ExecSelftests", "executor", f"""Run all three round-36 tool selftests.
cd {LANE} && python3 tools/mori-source-drift.py --selftest ;
python3 tools/mori-sources-appendonly.py --selftest ; bash tools/mori-index-clean.sh --selftest
Paste each output and exit code; expect three PASS lines."""))

items.append(item("ExecCensusEnd", "executor", f"""Round-end source-census conformance gate.
{FLEET}/scripts/sources-census.sh validate --root {FLEET} mori
Paste the full output and exit code (exit 0 required). Compare against the round-start receipt
{LANE}/.ufo/waves/round-36/evidence/census-start.txt and report any new W-lines."""))

items.append(item("ExecCensusRegression", "executor", f"""Lane census regression battery after the round changes.
cd {LANE} && bash tools/mori-census.sh --selftest ; bash tools/mori-silence-cases.sh
Paste outputs and exit codes; compare tallies to the SCORECARD-measured baselines (selftest PASS all
cases; oracle matched=28 total=28 exit 0). Any drop is a FAIL (no-harm to operability)."""))

items.append(item("ExecDriftLive", "executor", f"""Live drift-probe run for the report.
cd {LANE} && python3 tools/mori-source-drift.py --root {LANE}
Paste the full output and exit code. Verify rows=N equals the registry row count (220), the summary
counts sum to N, and the drifted ids match the receipt claims in evidence/c1-after.txt (49 fresh /
9 drifted / etc. per the counter's oracle subset — report both your full-tool counts and the counter
subset)."""))

items.append(item("ExecManualOracleSample", "executor", f"""Independent manual sample of the C1 real arm.
For rows S205, S206, S212, S156, S160, S176: run `curl -sS <row URL> | sha256sum` and compare with
`sha256sum corpus/evidence/sources-r36/<id>.src` (or the r30 copy for S156/S160, r33-era copy for
S176 — use tools/mori-source-drift.py's find_copy rule: highest sources-r<N>). Classify each of the 5
rows fresh/excerpt/drifted/unavailable by hand per contract.md:38-45, then run
`python3 tools/mori-source-drift.py --root {LANE}` once and confirm your 5 hand-classifications equal
the tool's lines. Paste every command and output."""))

# ---------------- reviewers
items.append(item("RevC2Receipt", "reviewer", f"""Audit the C2 data receipt. Attack: evidence/c2-after.txt.
Verify against {LANE}: first line == contract.md:23 P-C2 sentence (byte compare); counter
sha256 == evidence/freeze-v2.txt line for count-c2.py; blind arm 24/24 with coverage note
(deletions>=12, changed-back>=12, superseded>=1); real arm tool output == oracle output exactly
(all four lists + violations); exit 0; seed printed; no lines obviously truncated. FAIL any mismatch."""))

items.append(item("RevC1Receipt", "reviewer", f"""Audit the C1 byte-behavior receipt. Attack: evidence/c1-after.txt.
Verify: first line == contract.md:21 P-C1 sentence; counter sha256 == freeze-v2.txt; blind 40/40
mismatches=0 tool exit in (0,1); real arm: fetched>=10, fresh>=1, drifted>=1, mismatches=0,
excluded rows listed with reasons (429 re-probe rule per contract.md:53-57); exit 0; seed printed.
Confirm no wording in the receipt asserts a freshness/axis verdict."""))

items.append(item("RevC2Oracle", "reviewer", f"""Re-derive the C2 real-arm oracle WITHOUT the counter's code.
Attack: the independence of the receipt's oracle. Using only `git log --follow -p -- corpus/SOURCES.md`
(or per-commit `git show`), recompute at rev 6bd57097 (round base f10a320d): ids (immutable-cell
changes vs first commit holding the id; immutable = all but status/recheck/used-by; cells stripped),
deleted, superseded (an ids id with a tip row whose teaches opens `supersedes S###`), round_changed
(ids changed or deleted in f10a320d..6bd57097 touching the path). Compare to evidence/c2-after.txt's
oracle block (18 ids, deleted [], superseded [S069,S182,S193], round_changed [S182,S193]). Scratch
scripts under /fast/scratch/hyaku/mori-r36/RevC2Oracle/ only."""))

items.append(item("RevC1Interface", "reviewer", f"""C1 tool vs its registry row and knowledge note.
Attack: SKILL.md's `source drift (r36)` registry row and corpus/knowledge/source-drift-r36.md against
the actual tool (read tools/mori-source-drift.py). Check: entry command matches; verdict map (0/1/2)
matches code; selftest claim matches (`--selftest` exists, offline 127.0.0.1, temp dir removed);
the knowledge-note state table matches classify() semantics exactly (fresh/excerpt/drifted/
unavailable/no-copy + reader actions); the note's `drifted is not a changed source` warning is present
in both places. FAIL on any divergence."""))

items.append(item("RevC2Interface", "reviewer", f"""C2 tool vs its registry row and QUALITY 104.
Attack: SKILL.md's `SOURCES append-only (r36)` row and corpus/QUALITY.md criterion 104 against
tools/mori-sources-appendonly.py. Check entry/verdict-map/selftest claims, the `--round-base`
semantics, and that 104's stated check command runs as written:
`python3 tools/mori-sources-appendonly.py {TIP} --round-base 6bd57097` exits 0 with round_changed=[].
FAIL on any divergence."""))

items.append(item("RevQuality103", "reviewer", f"""Criterion 103 shown-able-to-fail audit. Attack: QUALITY.md:103.
Re-run `bash tools/mori-index-clean.sh --selftest` and confirm the add -N case exits 1 with
intent_to_add=1 while `git diff --cached --name-only` in the same sandbox prints nothing (the
round-35 M4 blind spot). Verify the live check command in 103 runs green at {TIP}. FAIL if the
selftest's red arm is absent or the live check disagrees."""))

items.append(item("RevQuality104", "reviewer", f"""Criterion 104 shown-able-to-fail audit. Attack: QUALITY.md:104.
Verify from evidence/c0-rescore-v2.txt that J2 (round-35 script) and J5 (no-deletion variant) both
score C2=unmet under the frozen counter, and that the selftest's deletion history prints
deleted=[S###] with exit 1. Verify 104 names the lesson and the supersession of the round-35 wave
script. FAIL on any missing red arm."""))

items.append(item("RevQuality105", "reviewer", f"""Criterion 105 witness re-derivation. Attack: QUALITY.md:105 + w1/MineCopyFidelity.md.
For each of the 7 drifted rows named there (S156–S160, S176, S177): run
`curl -sS <URL> | sha256sum` and compare against the sha256 recorded in the copy header (or the
lesson Gate digest for the row). Confirm the header/body sha matches (representation difference, not
a source change) for the excerpts and that S176/S177 differ only in the docs.python.org build footer
(diff the copy against the curl body and paste the differing lines). FAIL if any row is actually a
changed source."""))

items.append(item("RevSkillRows", "reviewer", f"""Gate-registry integrity for the three new rows.
Attack: SKILL.md Round36 section + registry table. Verify each of the three rows (source drift,
SOURCES append-only, index clean) carries the gate-standard fields (name/kind/entry/verdict map/
self-test/pinned values/write scope/owner) and that each entry command actually runs at {TIP} with
the mapped exits (run them; paste outputs). FAIL on any missing field or wrong exit map."""))

items.append(item("RevDebtR35", "reviewer", f"""Round-35 spotcheck §6 routed items — final disposition.
Attack: corpus/lessons/round-35-verifier-spotcheck.md §6 items 1–5 vs the landed bytes at {TIP}.
Item 1: no calibration claim this round (contract.md anti-loop ruling) — verify. Item 2: the 15
in-place ids + S069 superseded — verify 18 supersede rows exist and name their ids. Item 3: gate
registered with selftest — verify. Item 4: M4 check landed — verify 103 + the tool. Item 5:
operator items (LOG.md:1801 setting value, refs/jj/keep 3b19cac, .scratch/ 2026-10-21, SHONEN
promotion) — verify untouched and name them as operator-owned. FAIL any item silently dropped."""))

items.append(item("RevContractSizing", "reviewer", f"""Claim-sizing audit per prompt section 9.
Attack: contract.md + this round's shape. Verify: each after-state is one command over committed
bytes (count-c1.py/count-c2.py at the tip); no universal clauses in the targets; the kill rule
(predicate sentence + counter sha + receipt label) is identical in plan/counter/receipt; the control
receipts (c0-rescore-v2) predate data; a do-nothing control cannot reach the target (K1/J1 unmet in
c0-rescore-v2). FAIL any sizing violation."""))

items.append(item("RevFreezeIntegrity", "reviewer", f"""Freeze integrity at the landed tip.
Attack: evidence/freeze-v2.txt. Run sha256sum on contract.md, count-c1.py, count-c2.py at {TIP}
(`git show {TIP}:...`) and compare to freeze-v2.txt. Verify the c0 control programs under
.ufo/waves/round-36/c0/controls/ are byte-identical to the sha256s recorded in
evidence/c0-rescore-v2.txt headers (spot-check at least 6). Verify no file under
.ufo/waves/round-36/ was modified after the data commit (git log --name-only 5842dc0..{TIP}).
FAIL on any drift."""))

items.append(item("RevPredIdentity", "reviewer", f"""Predicate byte-identity re-check post-landing.
Attack: contract.md:21/23 vs the counters at {TIP}. Repeat the w1/ReviewPredicateIdentity check:
extract PREDICATE from count-c1.py (lines ~50-56) and count-c2.py (~32-38) and compare byte-exact
and whitespace-collapsed to the contract sentences; confirm each counter prints its predicate as the
first stdout line (run both with `--tool /bin/false --seed 1` against 6bd57097 and capture first
lines). FAIL on any drift."""))

items.append(item("RevNoHarm", "reviewer", f"""No-harm audit of the full round diff.
Attack: `git diff 6bd57097..{TIP}` (and `git diff-tree --name-status`). Verify: every changed path
is lane-local (no fleet/sibling paths); no path deleted; no existing SOURCES row edited in place
(only appends); SCORECARD/SHONEN/PROVINCE byte-unchanged so far this round; no remediation content
(no kills/restarts/config edits in any added text); census/oracle/silence surfaces untouched except
documented registry rows. List every path changed and classify it. FAIL on any harm."""))

items.append(item("RevMisroot", "reviewer", f"""Misroot sweep of the fleet root.
Attack: seat-output misrooting (r16-r17 lesson class). Run `git -C {FLEET} status --porcelain` (no
pathspec) and for every untracked file whose content names mori or round-36, report it (do NOT copy
or delete — L1 owns the sweep). Also confirm no w2 report files appear at {FLEET}/.ufo/waves/...
(misrooted trailer resolution). PASS means none found; list what you checked."""))

items.append(item("RevKnowledgeDrift", "reviewer", f"""Knowledge-note quality review.
Attack: corpus/knowledge/source-drift-r36.md against CORPUS.md rules. Verify: provenance trio first
(source with S205 citation, verified-at, recheck); every count carries its command (the 7 drifted /
5 excerpts / 2 footer rows claim cites w1 evidence — re-derive from evidence/c1-after.txt and
MineCopyFidelity); the state table is falsifiable; no universal claims; no credential material.
FAIL on any violation."""))

items.append(item("RevSupS205", "reviewer", f"""Re-open S205 (the row both claims rest on).
Attack: corpus/SOURCES.md row S205. Fetch
https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md
and verify the anchor lines 105-106,116-118 carry the append-only rule and recheck contract the
teaches cell asserts (located quote <=25 words, contiguous). Verify the copy
corpus/evidence/sources-r36/S205.src sha256 equals the fetched body. FAIL on any mismatch and say
whether the row's tier A holds."""))

items.append(item("RevSupS206S207", "reviewer", f"""Re-open S206 (RFC 6585) and S207 (jj git-compatibility).
Attack: their SOURCES rows + copies. Fetch both URLs; verify the S206 anchor (section 4, 429
definition) quote and the S207 anchor (detached-HEAD feature row) quote are contiguous and <=25
words; verify both copies sha256-equal the fetched bodies; verify the `supersedes S041/S044` form
follows CORPUS rule 2 and the superseded rows are untouched. FAIL on any mismatch."""))

items.append(item("RevSupS208S209", "reviewer", f"""Re-open S208 (NIST SP 800-122) and S209 (RFC 8785).
Attack: their SOURCES rows + copies. Fetch both; verify the located quotes (NIST ES-2 minimization
language; RFC 8785 section 1 hashable-output language) are contiguous at their anchors and <=25
words; copies sha256-equal; tier A justified (primary standards-body documents). FAIL on mismatch."""))

items.append(item("RevSupS210", "reviewer", f"""Re-open S210 (git-rev-parse docs).
Attack: row + copy. Fetch https://git-scm.com/docs/git-rev-parse ; verify the --verify/--end-of-options
language the teaches cell asserts is present at the options anchor; copy sha256-equal; the lane rule
in teaches (resolve once, bind bytes separately) is consistent with corpus usage
(lessons/round-19.md). FAIL on mismatch."""))

items.append(item("RevSupS212S213", "reviewer", f"""Re-open S212 (stat.rst) and S213 (iostats.rst).
Attack: rows + copies (v7.2 tag-pinned URLs). Fetch both; verify the anchor quotes (17-value line /
512-byte sector for S212; cumulative-monotonic fields and reset conditions for S213) are contiguous
and <=25 words; copies sha256-equal; the `supersedes S180/S181` form is rule-2 conformant. FAIL on
mismatch."""))

items.append(item("RevSupS214S217", "reviewer", f"""Re-open S214 (part_stat.h), S215 (blk-core.c), S216 (blk-mq.c), S217 (blk_types.h).
Attack: rows + copies. Fetch all four v7.2-pinned files; verify each teaches quote (partition add
also adds to whole disk; bdev_end_io_acct accounting; blk_account_io_completion sectors shift;
SECTOR_SHIFT 9 / bdev_whole) is contiguous at its anchor and <=25 words; copies sha256-equal; rule-2
form. FAIL on any mismatch."""))

items.append(item("RevSupS218S219", "reviewer", f"""Re-open S218 (flush iostats commit) and S219 (discard iostats commit).
Attack: rows + copies. Fetch both .patch URLs; verify the commit-message quotes (fields 16-17 flush
semantics; discard's own four statistics) are contiguous in the patch headers and <=25 words; copies
sha256-equal; rule-2 form. FAIL on mismatch."""))

items.append(item("RevSupS220", "reviewer", f"""Re-open S220 (sysstat iostat.c v12.8.0).
Attack: row + copy. Fetch https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c ; verify
the write_ext_stat current/previous sample language the teaches cell asserts is at lines 1444-1464
(contiguous quote <=25 words); copy sha256-equal; the row's scope caveat (extended-stat path only) is
honored — check the teaches cell does not claim the basic-stat path. FAIL on mismatch."""))

items.append(item("RevSupS211", "reviewer", f"""Re-check the rejected row S211 (PMC mirror).
Attack: corpus/SOURCES.md row S211 and S056. Verify S056's source cell already carries the exact PMC
URL S211 rejects as duplicate (quote both cells); the rejection reason and flip follow contract rule
2's rejection shape; S211 keeps status rejected. FAIL if the duplicate claim is false or the row
reads as evidence rather than a rejection."""))

items.append(item("RevSHONEN", "reviewer", f"""SHONEN checklist evidence review.
Attack: SHONEN.md against this round's evidence. For each of the 4 boxes state whether the round's
work gives [~] (resolvable pointer) or [ ] and why; verify no box is flipped to [x] without a named
non-author verifier. Recommend the correct marks for the report."""))

items.append(item("RevDispatchLog", "reviewer", f"""Dispatch-log truthfulness audit.
Attack: .ufo/waves/round-36/dispatch-log.txt. Reconcile every claim against artifacts: c0 25 seats
(25 Ctl*.md reports present), w1 33 tasks (count w1/*.md reports and the registry; name the dead and
refused seats with their error texts from the log), the three attempt-1 commits (da12b37, c1a026c,
5842dc0), the data commit {TIP}, the two counter receipts, the gate/index checks. FAIL any claim the
artifacts do not support."""))

items.append(item("RevCensusRows", "reviewer", f"""SOURCES.md census self-check at the tip.
Attack: corpus/SOURCES.md at {TIP}. Run the frozen census commands from {FLEET}/CORPUS.md (row count
via `grep -cE '^\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|'`, awk malformed-row check expecting 0, tier
and status histograms, duplicate-id check expecting none, enum/tier-inflation check expecting none,
mined used-by path existence check expecting none missing). Paste every command and output. FAIL on
any nonzero where zero is required. Expect rows=220."""))

items.append(item("RevAppendDebt", "reviewer", f"""Append-only debt closure count.
Attack: QUALITY 102's debt. Run one command over committed bytes that lists the ids the gate now
reports (read the gate's own `ids=[...]` line; QUALITY 104 names no ids and the count is receipted in
`evidence/c2-after.txt:6` — 18 at the scored tip) and verify each has a superseding row at the tip
whose teaches opens `supersedes S<id> —`; use `grep -cE 'supersedes S[0-9]{3}'` for the occurrence
count, never a bare `supersedes S0`. Verify no other id appears in the gate's ids list. FAIL on
count mismatch."""))

items.append(item("RevR13R16Gates", "reviewer", f"""Lane regression-gate battery (no-harm to operability).
Attack: the pre-existing gates after the round changes. Run at {TIP}:
python3 tools/mori-round13-regressions.py --selftest ; python3 tools/mori-round14-regressions.py --selftest ;
python3 tools/mori-round15-regressions.py --selftest ; python3 tools/mori-round16-regressions.py --selftest ;
python3 tools/mori-round17-seat-regressions.py --selftest (TMPDIR={LANE}/.scratch if required) ;
python3 tools/mori-retention-gate.py --selftest and python3 tools/mori-freeze-order.py --selftest and
python3 tools/mori-dispatch-ledger.py --selftest and python3 tools/mori-content-review.py --selftest
(TMPDIR={LANE}/.scratch where the registry rows require it). Paste each output and exit code; any
failure is a FAIL (round changes must not break the battery). Note: selftests may create state only
in throwaway sandboxes per their registry rows — never in the lane."""))

items.append(item("RevCapabilityRow", "reviewer", f"""SCORECARD capability-row consistency (pre-landing).
Attack: the pending C2 capability row. The integration commit will add a capabilities row for the
append-only gate keyed to this round. From the current bytes, verify: the capability is demonstrated
running in this round (receipts exist); the evidence pointer will resolve at the tip; the row does
not pre-claim unrun capabilities (check the existing 18 rows' pointers still resolve —
`git cat-file -e` each at {TIP}). FAIL on any dangling pointer."""))

items.append(item("RevReportSections", "reviewer", f"""Report-readiness gap scan.
Attack: the report contract (prompt section 4). List every required section (Work performed, Landed
changes, Before->after measurements, Sources & frontier, Trend verdicts, SHONEN, plus Stale-lane and
tool installs) and for each point at the committed evidence that will fill it, or name the gap. The
report must open by naming C1 (exploratory, freshness) and C2 (measured, operability). FAIL nothing —
report gaps as findings."""))

items.append(item("RevExploratoryHonesty", "reviewer", f"""Exploratory-claim honesty sweep.
Attack: any freshness overreach. Grep the round's artifacts (SKILL.md, corpus/QUALITY.md,
corpus/knowledge/source-drift-r36.md, .ufo/waves/round-36/) for any sentence that presents C1's
byte result as a freshness admission, a verified-stale-facts claim, or an axis score move. The only
admissible C1 outcome without a named non-author reviewer is `unprovable`; verify the artifacts say
so or name the missing reviewer condition. FAIL on any overreach."""))

items.append(item("RevOracle429", "reviewer", f"""Counter 429-handling vs contract amendment.
Attack: contract.md:53-57 amendment vs count-c1.py. Read the oracle_fetch and re-probe code
(~lines 190-235, 600-640) and verify it implements: up to five tries, Retry-After honored on 429
(capped), 5/10/20/30 backoff, a row answering 429 at any point is excluded even if a later try
succeeded, 4xx (non-429) after the last try is unavailable, and the tool-unavailable re-probe rule
(re-probe once; mismatch if the re-probe fetches; excluded when it does not). FAIL on any divergence."""))

items.append(item("RevWave1Audit", "reviewer", f"""Wave-1 seat accounting recount.
Attack: the report's seat accounting. List w1/*.md (expect 28 reports + swarm-registry.json), read
.ufo/waves/round-36/w1-dispatch.json task count (33), and reconcile: 28 reports + 2 dead
(MutC1Novel, MutC2Novel) + 2 refused-hold (CritC1Counter, CritC2Counter) + 1 unaccounted — identify
the 33rd task by name from the dispatch file and state whether it returned (check its report file by
name). FAIL if the arithmetic cannot be made truthful."""))

# ---------------- critics
items.append(item("CritC1Axis", "critic", f"""Adversarial pass on C1 (attempt-2 retry of the refused w1 critic).
Attack the exploratory declaration itself: (1) is the axis-fit defect (byte classifier certifies
representation differences, w1/CritAxisFit.md) real and unresolved? (2) is `unprovable` the honest
landing given no named non-author reviewer exists inside the round? (3) does the probe still improve
freshness technique (first programmatic re-fetch of every copied row) and is that claimed modestly?
(4) hunt any path by which the round or a closure could read C1=met (byte evidence) as C1 admitted.
Give an independent VERDICT line: does C1 land unprovable honestly, or is there a defect?"""))

items.append(item("CritC2Axis", "critic", f"""Adversarial pass on C2 (attempt-2 retry of the refused w1 critic).
Attack the measured claim: (1) does P-C2 carry an operability verdict — is a gate that flags
append-only violations with deleted-row detection genuinely runnable craft, or is it bookkeeping?
(2) is the blind-arm truth truly hidden (check whether a tool could read c0 control programs or
counter temp files during a run — reason from the counter code paths)? (3) does the real arm at
6bd57097 bind history that actually happened (cross-check one id, e.g. S069, against
`git log -p corpus/SOURCES.md`)? (4) hunt for a do-nothing or denial control that would meet P-C2
(the c0 set should have failed it — verify J8's receipt). Independent VERDICT line."""))

items.append(item("CritAdmission", "critic", f"""Whole-round admission dry run.
Attack the round as the closure will: assemble every claim's verdict (C2 measured; C1 exploratory),
check 'every claim verifies and no axis is harmed', check the two trend-proof obligations (sources
census exit 0 at end; at least one sourced claim — C2 rests on S205 opened this round), check the
L2 floor was met (c0 25 + w1 33 + w2), and hunt for any harm/trade the lane report would hide. Name
the exact ruling you would give and why."""))

items.append(item("CritLoop", "critic", f"""Anti-loop check vs r32–r35.
Attack: is this round another spin of the same loop? Verify: no calibration claim (the four-round
failed pattern); capability claims with run-time-hidden-truth counters and pre-data control scoring
(r34 mechanism) — but check the r34 failure mode (harness-keyed programs) is actually closed by the
v2 real-arm-on-repo design and K9/J11 receipts; the repair-first sequencing (r35 rejection) is
honored. Name any residual loop behavior."""))

# ---------------- mutation-testers (mutants run via --tool against the frozen counters)
MUT = f"""Mutation-tester discipline: copy the ORIGINAL tool from {LANE}/tools/<name> into
/fast/scratch/hyaku/mori-r36/<YourName>/mutant.py, apply exactly the described one-purpose mutation,
then run the FROZEN counter with `--tool` pointing at the mutant:
`python3 {LANE}/.ufo/waves/round-36/count-cN.py {TIP} --tool /fast/scratch/hyaku/mori-r36/<YourName>/mutant.py --seed 11`
The mutant MUST score unmet (the counter must be able to fail). Paste mutant diff, full counter
output, and exit code. Also run the mutant's selftest if applicable and note whether it still
passes (a mutant whose selftest passes while the counter fails is the strongest receipt)."""

items.append(item("MutC1Copy", "mutation-tester", MUT + """

Target: tools/mori-source-drift.py (C1). Mutation: read the OLDEST copy (lowest sources-r<N>)
instead of the newest (the K13 control class). Expect: blind arm fails (decoy rows flip states)."""))

items.append(item("MutC1Excerpt", "mutation-tester", MUT + """

Target: tools/mori-source-drift.py. Mutation: delete the excerpt rule (only fresh/else drifted).
Expect: blind arm fails on the 8 excerpt rows."""))

items.append(item("MutC1Unavailable", "mutation-tester", MUT + """

Target: tools/mori-source-drift.py. Mutation: treat 404/connection-close as drifted instead of
unavailable. Expect: blind arm fails on the unavailable rows AND the exit code may flip; the counter
must catch it."""))

items.append(item("MutC1Strip", "mutation-tester", MUT + """

Target: tools/mori-source-drift.py. Mutation: skip the whitespace strip in the excerpt test (require
the raw copy bytes to occur in the body). Expect: blind arm fails on the padded excerpt rows."""))

items.append(item("MutC2Deleted", "mutation-tester", MUT + """

Target: tools/mori-sources-appendonly.py (C2). Mutation: remove the deleted-row arm (never report
deleted ids). Expect: blind arm fails on histories with deletions (J5 class)."""))

items.append(item("MutC2Endpoint", "mutation-tester", MUT + """

Target: tools/mori-sources-appendonly.py. Mutation: compute round_changed as endpoint-only
(ignore intermediate changed-back commits; J4 class). Expect: blind arm fails on changed-back
histories."""))

items.append(item("MutC2Cols", "mutation-tester", MUT + """

Target: tools/mori-sources-appendonly.py. Mutation: compare only the first four columns when
deciding immutable-cell changes (so status/recheck/used-by edits look like violations). Expect:
blind arm fails on histories with mutable-cell edits."""))

# ---------------- sentinels
items.append(item("SentTools", "sentinel", f"""Safety sweep of the three new tools.
Attack: tools/mori-source-drift.py, tools/mori-sources-appendonly.py, tools/mori-index-clean.sh.
Check: no credential/secret/token patterns; no writes outside selftest temp dirs (grep open()/write
calls and shell redirects); drift tool's only network egress is GET via urllib with bounded timeout
and bounded retries; index-clean uses --no-optional-locks; append-only tool is read-only git;
selftests clean up their temp dirs. FAIL on any unbounded write, unbounded loop, or credential
handling."""))

items.append(item("SentData", "sentinel", f"""Evidence-file safety sweep.
Attack: .ufo/waves/round-36/evidence/ and corpus/evidence/sources-r36/. Scan for credential
material (tokens, cookies, op:// refs, private key blocks), for raw cursors/journal text (mori
rule: stdout never carries raw journal cursors — check c1/c2 receipts and census logs), and for
anything that looks like another lane's or operator's private data. FAIL on any hit."""))

items.append(item("SentCensus", "sentinel", f"""Live-surface safety review of the round diff.
Attack: `git diff 6bd57097..{TIP} --stat` + the census tools. Verify the round's changes add no
live-host write path: the census, oracle, silence and journal arms are byte-unchanged (name-status
must not list tools/mori-census.sh, tools/mori-silence-cases.sh); the new tools are probes/gates
that write nothing in production runs; no threshold/tuning changes anywhere. FAIL on any live-surface
mutation."""))

# ---------------- revengers
items.append(item("RevNgC1", "revenger", f"""Reverse-engineer count-c1.py for truth leaks and harness keys.
Attack: the hidden-truth architecture. Read {LANE}/.ufo/waves/round-36/count-c1.py fully. Answer with
code line evidence: (1) is the blind-arm truth ever written under the fixture root or any path the
--tool program can read (check build_fixture, serve, scratch paths, env inheritance, /proc leaks)?
(2) can a tool detect it is under the blind arm via path, env, parent pid, server headers, or timing
— and does the v2 real-arm-on-repo design make such a key useless (a harness-keyed program fails the
real arm)? (3) re-run the K9 control (controls/K9.py) under the frozen v2 counter and confirm it is
unmet (evidence should already show this — verify, don't assume). (4) one novel bypass attempt of
your own design against the blind arm; report what the counter does."""))

items.append(item("RevNgC2", "revenger", f"""Reverse-engineer count-c2.py the same way.
Attack: {LANE}/.ufo/waves/round-36/count-c2.py. With line evidence: (1) is the sandbox-history op
log or truth ever written where the --tool program can read it? (2) any harness key (paths under
/fast/scratch or /tmp, env, argv) that lets a tool behave differently — and does the v2 real arm on
the repo itself (fixed rev 6bd57097) defeat it? (3) re-run control J11 under v2 and confirm unmet.
(4) one novel bypass attempt; report the counter's response."""))

# ---------------- connector + scouts
items.append(item("ConnSibling", "connector", f"""Sibling-overlap scan for the 16 new source rows.
Attack: absorption/overlap. Compare the URLs and scopes of S205–S220 against sibling corpora
({FLEET}/tsukuroi-shokunin/corpus/SOURCES.md, kumitate, chousa, kake, kotoba — read-only) for exact
or near URL duplicates and for scope overlap (e.g. iostats/disk accounting vs kake/tsukuroi ground,
RFC 8785 vs chousa). Report hits with file:line; per kaika practice exact-URL sharing means a row is
not merged but noted. Also confirm none of the rows absorbs a sibling-owned scope (PROVINCE
adjacency table)."""))

items.append(item("ScoutFreshness", "scout", f"""Freshness sweep of the round's new claims.
Recon only, no edits: list every file added/changed at {TIP} vs 6bd57097 with its one-line role;
for each, name the SCORECARD/LOG/lesson pointer that must reference it for freshness (every LOG entry
needs a re-verification result). Report the checklist the integration commit must satisfy so no
orphaned artifact survives the round."""))

# ---------------- scribes
items.append(item("ScribeLesson", "scribe", f"""Draft corpus/lessons/round-36.md (skeleton for L1).
From committed evidence only (no new measurements): write the lesson draft with ## Gate (candidates:
C1 exploratory byte probe / C2 append-only gate; admitted/rejected with reasons; the spot-check
result line left for the outside closure) and ## Mistakes rows. Candidate mistakes to evaluate from
evidence: (M-a) C1's axis-fit defect found pre-data by the w1 critic (class: axis-fit; captured-by:
none — became the exploratory declaration); (M-b) attempt-1 died before landing the drift tool
(class: landing; captured-by: addendum §5 inheritance). Each row: class · evidence pointer ·
captured-by · fix. Write the draft to your report; L1 copies the accepted text — you write no lane
file."""))

items.append(item("ScribeScorecard", "scribe", f"""Draft the SCORECARD round-36 section (for L1).
From the receipts at {TIP}: draft the move-log rows and capabilities row for C2 (name: sources
append-only gate with deleted-row detection; what: flags in-place edits/deletions/superseders of
corpus/SOURCES.md; evidence: count-c2 receipt + gate command; first-working round 36) and the C1
exploratory row (verdict unprovable pending named non-author reviewer; pointer to
evidence/c1-after.txt as byte evidence). Also draft the Planned row for round 37. Write the draft in
your report; L1 lands the final text."""))

items.append(item("ScribeLog", "scribe", f"""Draft the LOG.md round-36 entry (for L1).
One entry from the dispatch log + receipts: freeze (da12b37), C0 v2 re-score (c1a026c), exploratory
declaration (5842dc0), data commit ({TIP}), the two counter receipts with seeds, gate/index checks,
wave accounting. Every line carries its command or commit. Write the draft in your report."""))

spec = {
    "wave": "mori-r36-w2",
    "reportDir": ".ufo/waves/round-36/w2",
    "maxLanes": 96,
    "context": CONTEXT,
    "items": items,
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w2-spec.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
print("wrote", out, "items:", len(items))
from collections import Counter
print(Counter(i["role"] for i in items))
