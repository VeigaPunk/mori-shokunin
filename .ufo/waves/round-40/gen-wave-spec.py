#!/usr/bin/env python3
"""Generate the round-40 wave spec (one v2 wave, 64 seats, >=25% attack)."""
import json
from collections import Counter

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"

CONTEXT = f"""# mori round 40 — wave 1 (single v2 wave: build + attack together), L1 mori-r40 attempt 1

Lane repo: {LANE} (jj-colocated; git is the backend; never run mutating git/jj yourself).
Fleet repo: {FLEET} — READ-ONLY for you: never write, commit or push there; never touch sibling lanes, lane jj state, the lane Git index, .ufo/state/ or .ufo/watchdog.log.
Scored tip (instruments): 265a955cc67be4eae97d2dc5a9338a25f31eb29b (pushed). Entering tip: bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3.
All seat paths are ABSOLUTE under {LANE} — your tools start at the fleet root; a relative path lands in the FLEET repo. Every `Report:` trailer path printed by the harness is relative to {LANE} — write your report at {LANE}/<that path>.
Bounds: read-only seats return findings without production edits; executor seats write ONLY the single artifact their item names, under .ufo/waves/round-40/w1/ or .scratch/. Seats never mutate the fleet repo, sibling lanes, lane jj state or lane Git index.
Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — official channels only (uv tool / npx / official binary in ~/.local/bin); record tool/version/channel/reason in your report. Pacman guard (orchestrator ruling 2026-10-20): ALL pacman transactions are PAUSED host-wide — never run pacman; install via uv/npx/official binary or file an L0 question instead.

## Claims under attack (frozen in {LANE}/.ufo/waves/round-40/contract.md; pins in evidence/freeze-r40.txt)
- C1 operability: `python3 {LANE}/.ufo/waves/round-40/conform.py <rev>` must print CONFORM=met on the counter of record and CONFORM=unmet on nine survivor fixtures + a two-counter audit; `--selftest` prints CONFORM_SELFTEST pass=11 fail=0.
- C2 depth: `python3 {LANE}/tools/mori-sources-appendonly.py` v3 (P-C11) — eligible set is every superseded id present at R; an edit compares against the first parent's own state only; a delete-then-re-add contributes no changed event. Lane line at the tip carries 34 as-of ids including S226, none stale; at e37dcc6 stale=[S069].
- Frontier: SOURCES.md S229 (opened this round) grounds C1; census exit 0; lesson round-40 mines >=1 mistake.

## Evidence layout (already landed; your ground truth)
{LANE}/.ufo/waves/round-40/evidence/c10-*.txt and c11-*.txt (before receipts ran extracted v2 bytes from fixtures/extracted/; after receipts ran the landed bytes at 265a955cc).
Before instruments: fixtures/extracted/gate-v2-bb1f2457.py, conform-v2-r39.py, count-c7-r39.py. New P-C11 DAG fixtures: dag-n (never-edited superseded), dag-p (first-parent-lacks-path merge), dag-r (delete-then-re-add of a superseded row).
"""

items = []


def add(name, role, task):
    items.append({"name": name, "role": role,
                  "prompt": GODSPEED + "\n\n" + task +
                  "\n\nWrite your seat report at the `Report:` trailer path given to you (relative to " + LANE + "). Name the exact commands you ran and their outputs; an unrun check has not passed."})


E = f"{LANE}/.ufo/waves/round-40/evidence"
FIX = f"{LANE}/.ufo/waves/round-40/fixtures"

add("ConnSiblingOverlap", "connector",
    "Sibling-overlap scan: does any sibling lane's corpus/SOURCES.md already hold the Python execution-model URL admitted this round as S229 (" + FLEET + "/*/corpus/SOURCES.md), and does any sibling knowledge entry teach Python name-resolution scoping for static folds? Report overlap or honest absence with the grep commands used. Do not edit sibling repos.")
add("ConnW04Routing", "connector",
    "Routed-defect-6 check: enumerate the standing W04 duplicate-URL rows from " + E + "/census-end.txt (S035, S037, S073-S076, S147-S150, S166, S168, S201, S218, S220, S228) and confirm each duplicated URL is owned by a non-mori source row (historical fleet debt), not introduced by mori round-40 rows. Name the file:line for S229's URL proving it appears once.")

exe = [
 ("ExeConformMet", "Re-derive " + E + "/c10-after.txt: run `python3 " + LANE + "/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b` and diff stdout against the committed receipt byte-for-byte; report any drift."),
 ("ExeConformSelftest", "Re-derive " + E + "/c10-after-selftest.txt: run the conform v3 `--selftest` at the scored tip and confirm CONFORM_SELFTEST pass=11 fail=0; time it; report the wall seconds."),
 ("ExeGateSelftest", "Re-derive " + E + "/c11-after-selftest.txt: run `python3 " + LANE + "/tools/mori-sources-appendonly.py --selftest` and confirm pass=15 fail=0; report per-arm PASS lines."),
 ("ExeGateLane", "Re-derive the C2 lane line: run the gate at 265a955cc67be4eae97d2dc5a9338a25f31eb29b and verify the supersede_timing line lists 34 as-of ids including S226 with stale empty; name every id that differs from " + E + "/c11-after-lane.txt."),
 ("ExeGateE37", "Re-derive " + E + "/c11-after-e37dcc6.txt: run the gate at e37dcc6 and confirm stale_supersede=[S069]; report the full timing line."),
 ("ExeDagN", "Re-derive " + E + "/c11-after-fixture-n.txt via `" + FIX + "/run-c11-dags.py " + LANE + "/tools/mori-sources-appendonly.py " + LANE + " <out> dag-n`; confirm as_of=[S001] stale=[] and compare against the red " + E + "/c11-red-neveredited.txt."),
 ("ExeDagP", "Re-derive " + E + "/c11-after-fixture-p.txt via run-c11-dags.py dag-p; confirm the merge contributes no edit (no fabricated changed line) and stale empty; compare to red " + E + "/c11-red-firstparent.txt."),
 ("ExeDagR", "Re-derive " + E + "/c11-after-fixture-r.txt via run-c11-dags.py dag-r; confirm as_of=[S008] stale=[] (re-add is not an edit); compare to red " + E + "/c11-red-readd.txt."),
 ("ExeSurvivorSweep", "Run the conform v3 against all ten generated survivors in " + FIX + "/generated/ and confirm each prints CONFORM=unmet exit 1; tabulate which named check failed per fixture and compare with the contract's P-C10 mapping."),
 ("ExeParity", "Re-derive " + E + "/c10-parity.txt: run count-c7 (round-39 bytes) and count-c8 (round-40 bytes) on rev bb1f2457 with two different seeds and confirm byte-identical receipts per pair; report the sha256 of both counters."),
 ("ExeCensus", "Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root " + FLEET + " mori` and confirm exit 0 with the same standing W04 set as " + E + "/census-end.txt (S229 must introduce no new warning)."),
 ("ExeWitnessBytes", "Verify the four witness files in " + FIX + "/ (witness-token-entry.md, witness-dangling-row.md, witness-summary-only-live.txt, witness-comment-anchors.md) are byte-identical to their round-39 counterparts (sha256 both sets); report the comparison."),
 ("ExeExtractPins", "Verify the extracted before-instruments in " + FIX + "/extracted/ equal the committed bytes at bb1f2457: `git show bb1f2457:tools/mori-sources-appendonly.py | sha256sum` vs gate-v2-bb1f2457.py, same for conform-v2-r39.py vs .ufo/waves/round-39/conform.py and count-c7-r39.py vs .ufo/waves/round-39/count-c7.py."),
 ("ExeDagDeterminism", "Build each P-C11 DAG twice via the gate module's _make_dag_repo in an isolated .scratch dir and confirm both runs produce byte-identical registry bodies at every named sha (report the cmp results); determinism underpins receipt replay."),
 ("ExeConjunctAfter", "Re-derive " + E + "/c10-after-conjunct.txt: run the v3-conjunct-gutted copy (`--selftest`) and confirm pass=0 with selftest_conjunct in every failing list; also re-run the r39 gutted copy and confirm pass=8 fail=0 (" + E + "/c10-red-conjunct.txt)."),
 ("ExeFreezePins", "Re-derive " + E + "/freeze-r40.txt: sha256 every path it lists at the scored tip via `git show 265a955cc67be4eae97d2dc5a9338a25f31eb29b:<path>` and confirm each matches the recorded digest; report mismatches."),
]
for name, task in exe:
    add(name, "executor", task)

scr = [
 ("ScrReportWork", "Draft the report's 'Work performed' section prose from the landed evidence in " + E + "/ (name each claim, target axis, and evidence pointer; no invented numbers — quote the receipts). Output: a markdown fragment under .ufo/waves/round-40/w1/ only."),
 ("ScrLandedChanges", "Draft the 'Landed changes' bullet list mapping each receipt set to its commit 265a955cc67be4eae97d2dc5a9338a25f31eb29b and the pending evidence commit; cite LOG.md entries by title."),
 ("ScrScorecardRow", "Draft the SCORECARD.md round-40 declaration + results rows for C1 (operability, 7 held) and C2 (depth, 5 held) with before/after cells quoting receipt paths; mark the measured 34-id lane line and note the contract's '19 ids' parenthetical mis-prediction as an erratum-class correction."),
 ("ScrLessonDraft", "Draft corpus/lessons/round-40.md ## Mistakes rows (M23 inherited-unverified-freeze, M24 parenthetical arithmetic) and a ## Gate table row for S229 with the located quote 'When a name is used in a code block, it is resolved using the nearest enclosing scope' (15 words, section 4.2.2)."),
 ("ScrSourcesRow", "Verify the S229 registry row's cells against the contract (kind docs, tier A scoped to Python name resolution, status mined, used-by corpus/knowledge/conform-scope-r40.md, opened 2026-10-24) and confirm append-only placement directly after S228 inside ## Registry."),
 ("ScrErratumCheck", "Verify corpus/lessons/round-39-erratum.md against its three sources: " + E + "/c10-red-decoy.txt + c10-after-decoy.txt (drain before-control), the S227 17-word quote in corpus/evidence/sources-r39/S227.src, and the r39 contract's stale pass=11 citation; confirm each erratum sentence is backed."),
]
for name, task in scr:
    add(name, "scribe", task)

sco = [
 ("ScoutPriorWaves", "Recon .ufo/waves/round-38/w1/ and .ufo/waves/round-39/w1/ seat reports: list every finding class those seats raised against the conform/gate instruments that round-40 evidence does NOT address; name the report file per finding."),
 ("ScoutInstrumentLayout", "Map the round-40 instrument tree under " + LANE + "/.ufo/waves/round-40/ (contract, counters, fixtures, extracted, evidence) against the contract's 'P-C10/P-C11 evidence paths' list; name any path on disk missing from the contract list or vice versa."),
 ("ScoutCorpusFrontier", "Read corpus/README.md ## Frontier and confirm the round-40 admission (S229 row, conform-scope-r40.md knowledge entry) leaves the frontier statement accurate; flag any README claim the round contradicts."),
 ("ScoutQualityBar", "Read corpus/QUALITY.md and list the criteria that govern the round-40 claims (measurement discipline, fix-shown-able-to-fail, quote word counts); check each receipt set names its measured rev (r39 lesson finding 9 discipline)."),
 ("ScoutSiblingConform", "Check whether any sibling lane owns a 'counter conformance' or 'scope-aware static fold' artifact that could collide with mori's conform v3 (search " + FLEET + "/*/SKILL.md and */tools/ for conform/timeout-fold references); report collisions or absence."),
 ("ScoutDriftProbe", "Recon whether tools/mori-source-drift.py (the C7 drift probe's target) changed since round 39: `git log --oneline bb1f2457..265a955cc -- tools/mori-source-drift.py` and diff if touched; the anchors_v2 check reads it, so a silent change would matter."),
]
for name, task in sco:
    add(name, "scout", task)

add("SimpGateV3", "simplifier", "Read tools/mori-sources-appendonly.py at the scored tip and hunt dead code introduced or left behind by v3: unused imports, unused helpers, unreachable branches (e.g. anything orphaned by the P-C11 first-parent change). Report findings with file:line; do NOT edit the gate — findings only.")
add("SimpConformV3", "simplifier", "Read " + LANE + "/.ufo/waves/round-40/conform.py and count lines versus the r39 bytes (" + FIX + "/extracted/conform-v2-r39.py): confirm the +delta is accounted for by the three new checks (timeout_scope hardening, drain_bind, selftest_conjunct v3) plus their mutations; flag any line you cannot account for.")

add("RevFindingsCoverage", "reviewer", "Cross-check the 13 round-39 wave-1 findings (corpus/lessons/round-39.md) and the closure's 6 routed defects against the round-40 contract's 'Routed inputs' list: every finding must map to exactly one claim or one explicit non-claim disposition; report uncovered or double-covered findings.")
add("RevWaveDedup", "reviewer", "Deduplicate THIS wave's items: group them by the claim/receipt they attack and report any item that shares both target and method with another (true duplicates), and any item with no resolvable evidence target (padding). Findings only, no edits.")
add("RevLessonGate", "reviewer", "Review the round-40 lesson's ## Gate table for S229: the located quote must be <=25 words, name the copy path (corpus/evidence/sources-r40/S229.src) and the access date, and the teaches cell must match the knowledge entry's claim; flag drift.")
add("RevRoutedCoverage", "reviewer", "Verify the contract's 'Routed inputs' list names each round-39 closure routed defect (1: drain-shape re-claim + wording; 2: name-not-value survivors + decoy; 3: C9 prose/predicate single source; 4: S227 17-word label) with the receipt that discharges it; report any routed defect with no discharging receipt.")
add("CritExploratoryBoundary", "critic", "Attack the claim structure: confirm exactly 2 claims on distinct axes (C1 operability, C2 depth), that no third claim hides in the corpus/evidence edits, and that C1 and C2 are causally separable — show the C1 receipts are runnable without the gate v3 bytes and the C2 receipts without the conform v3 bytes.")
add("ExeSelftestTiming", "executor", "Measure both selftests' wall time at the scored tip (conform v3 --selftest and gate --selftest, one run each) and confirm they complete inside the wave's mechanicalMs budget (1800000 ms); report the measured seconds and any risk of lane_timeout under dispatch.")

rev = [
 ("RevC1Receipts", "Review every " + E + "/c10-*.txt: confirm each names its command, measured rev and exit code; confirm red receipts ran v2 bytes (extracted shas) and after receipts ran landed bytes at 265a955cc; report any receipt missing one of the three."),
 ("RevC2Receipts", "Review every " + E + "/c11-*.txt with the same three-part discipline (command, rev, exit); confirm the red/after pair for each fixture DAG contradicts exactly as the contract declares."),
 ("RevGateDiff", "Review `git diff bb1f2457 265a955cc -- tools/mori-sources-appendonly.py` hunk by hunk: classify each hunk as (a) P-C11 eligible-set change, (b) P-C11 first-parent change, (c) P-C11 re-add removal, (d) fixture/selftest addition, (e) other; flag any hunk you cannot classify or that changes behavior beyond P-C11's words."),
 ("RevConformDiff", "Review the conform diff between the r39 bytes and the landed v3 bytes hunk by hunk with the same classification against P-C10's three made-sound checks; flag behavior changes beyond the predicate's words."),
 ("RevContractConformance", "Compare " + LANE + "/.ufo/waves/round-40/contract.md against the landed evidence set: every evidence path the contract names must exist with the declared content class (red=met on v2, after=unmet on v3, etc.); name missing or mismatched files."),
 ("RevScorecardClaims", "Review the claimed kill rules: (C1) a do-nothing control cannot print CONFORM=met — is the r39-checker-on-survivors control committed for every survivor? (C2) can a do-nothing gate print the fixture verdicts — is the v2-on-DAGs control committed for n/p/r? Report gaps."),
 ("RevErratum", "Review corpus/lessons/round-39-erratum.md for append-only discipline: it must correct without rewriting round-39 files; verify the corrected sentences against the cited receipts; flag any correction that misstates the receipt it cites."),
 ("RevKnowledgeProvenance", "Review corpus/knowledge/conform-scope-r40.md: provenance trio (source: S229 + URL, verified-at, recheck) must open the entry; every technical claim must cite S229 section 4.2.2 or the r39 findings; flag unsourced claims."),
 ("RevShonenBoxes", "Review the report's SHONEN checklist requirements against the round's evidence: which boxes can move from [ ] to [~] with a resolvable pointer, and which stay [ ] for lack of a named non-author verifier; report the honest state."),
 ("RevParityScope", "Review " + E + "/c10-parity.txt: confirm the parity claim is scoped correctly (receipts byte-identical at one seed, not 'counters identical' — they differ by the 16 dead lines); flag any report wording that would overclaim."),
 ("RevFreezeHonesty", "Review " + E + "/freeze-r40.txt: the note must disclose that the freeze receipt was persisted at integration by the resuming L1, not before data; confirm the sha256 set covers every path the contract froze; flag omissions."),
 ("RevCensusPair", "Compare " + E + "/census-start.txt and " + E + "/census-end.txt: confirm both exit 0, both name the same standing W04 set, and S229 adds no new warning class; report the start/end exit codes explicitly."),
]
for name, task in rev:
    add(name, "reviewer", task)

cri = [
 ("CritNewSurvivor", "Falsify C1: construct ONE new counter fixture from count-c8 that the v3 checker still accepts but violates the plain words of P-C10 (candidates: a lambda-bound timeout alias, a conditional rebind inside the function, a timeout= read via attribute). If you cannot construct one after 3 bounded attempts, report the attempts and their receipts as the failure evidence."),
 ("CritNewDag", "Falsify C2: construct ONE new fixture DAG (candidates: octopus merge with two side supersede rows, re-add with MODIFIED immutable cells, merge whose first parent is the walk root) on which v3's output contradicts P-C11's words. Report the DAG construction and both gates' outputs, or the bounded attempts."),
 ("CritLaneLine", "Attack the lane line: of the 34 as-of ids in " + E + "/c11-after-lane.txt, pick 5 at random and independently verify each is (i) present at the tip, (ii) superseded by a row whose teaches cell opens 'supersedes S<ID> —', (iii) genuinely never-edited since first sighting or edited before its superseder landed. Report per-id verdicts."),
 ("CritPredParenthetical", "Attack the P-C11 parenthetical '(19 ids)': prove from the committed receipts that the measured value is 34 and enumerate the 16 never-edited superseded ids the parenthetical arithmetic missed; classify the defect (claim-sizing vs predicate) and state which sentence is the claim's real counter."),
 ("CritConjunctSemantics", "Attack selftest_conjunct: is 'the checker's own table carries a live entry' the property P-C10's words claim, or a weaker proxy? Try to make a checker whose table carries the entry but whose selftest does not actually exercise the conjunct (entry_live true, conjunct unwired); report whether v3 catches it."),
 ("CritDrainedTuple", "Attack drain_bind: construct a counter whose Popen result is drained by a communicate bound to a DIFFERENT name via tuple swap (a, b = b, a after assignment) yet consumed; does v3's same-name binding rule accept or reject? Report the fixture and verdict against P-C10's words."),
 ("CritFreezeTiming", "Attack the freeze discipline: the contract says instruments were frozen before any data seat, but the freeze receipt was written after the data commit; enumerate exactly which before-receipts could have been contaminated by post-freeze instrument edits and show from `git show` that the extracted v2 bytes predate any data commit."),
 ("CritScoringHonesty", "Attack the round's calibration: collect every number in the drafted SCORECARD rows (11, 15, 34, 16, 9, 8, 228->229) and re-derive each from a committed receipt with one command; report any number that no receipt supports."),
]
for name, task in cri:
    add(name, "critic", task)

mut = [
 ("MutGateReadd", "Mutation-test the gate: transplant the v2 `elif not is_merge` re-add branch back into a copy of the v3 gate and run the selftest — exactly the dag-r arm must FAIL (stale=[S008]); report the mutated sha and the arm's output."),
 ("MutGateEligible", "Mutation-test the gate: restore the edit-bounded eligible set (`superseded = cid for cid in ids if cid in sup_map`) in a v3 copy — exactly the dag-n and dag-r arms must FAIL (and the lane line must lose never-edited ids); report which arms failed."),
 ("MutGateFirstParent", "Mutation-test the gate: restore the v2 per-parent fall-through loop in a v3 copy — exactly the dag-p arm must FAIL (fabricated changed + stale at the merge); report the arm's output."),
 ("MutConformArms", "Mutation-test conform v3: in a copy, neuter the conditional-rebind arm of timeout_scope (treat conditional as unconditional) and run `--selftest` — the timeout_scope arm must still fail but the cond survivor after-receipt must flip to met; report both outputs."),
]
for name, task in mut:
    add(name, "mutation-tester", task)

add("SentArtifactSafety", "sentinel", "Security review of the round-40 artifact set under " + LANE + "/.ufo/waves/round-40/ and corpus/: no credential material (secrets, tokens, op:// refs), no absolute paths outside the lane/fleet roots, no shell-injection hazards in the fixture builders (they write fixed paths under .scratch and mktemp dirs only), no fleet-root writes. Report findings with file:line.")
add("SentToolingBounds", "sentinel", "Security review of the wave context itself: confirm every seat prompt bounds writes to .ufo/waves/round-40/w1/ or .scratch, forbids pacman, forbids fleet/sibling writes, and names absolute paths; flag any prompt missing a bound.")

add("RevPriorIntent", "revenger", "Reverse-engineer the dead launch's intent: compare the inherited working tree (contract.md, count-c8.py, conform.py, the gate modification, fixtures, scratch drafts) against what actually landed at 265a955cc; name every inherited artifact you re-verified, every one you changed or discarded (the three root strays bypass-none.py, bypass-wait.py, count-c1-r38.py were deleted — confirm they exist in no commit and were recoverable from round-38 evidence), and any contract promise the landed bytes still owe.")

add("LabDagDeterminism", "executor", "Bounded empirical probe (read-only): hypothesize 'the dag-p modify/delete merge fixture is not deterministic across git re-runs because conflicted index state could leak' — build dag-p five times in isolated .scratch dirs and compare the named shas and final registry body each time; accept or reject the hypothesis with the comparison output.")

spec = {
    "wave": "mori-r40-w1",
    "reportDir": ".ufo/waves/round-40/w1",
    "maxLanes": 66,
    "context": CONTEXT,
    "items": items,
}
out = LANE + "/.ufo/waves/round-40/w1-spec.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
attack = sum(1 for i in items if i["role"] in ("reviewer", "critic", "mutation-tester", "sentinel", "revenger", "labrat"))
print("items:", len(items), "attack:", attack, "(%.1f%%)" % (100 * attack / len(items)))
print(Counter(i["role"] for i in items))
