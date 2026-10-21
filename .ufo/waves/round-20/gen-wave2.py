#!/usr/bin/env python3
"""Generate the mori round-20 wave-2 (falsify) spec. Every item names what it attacks."""
import json, pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/mori-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-20"
TOOL = f"{L}/tools/mori-wave-settlement.py"
ORA = f"{W}/build/OracleHarness/c2-oracle.py"
REG = f"{L}/corpus/evidence/drift-classification-r20.json"
R13 = f"{L}/.ufo/waves/round-13/evidence/drift-classification.json"
ENT = f"{W}/evidence/c1-drift-entering.json"
PRE = f"{W}/evidence/c1-drift-r10-prepin.txt"
POST = f"{W}/evidence/c1-drift-r20-postpin.txt"
B20 = f"{L}/corpus/evidence/baseline-r20-20261021T1051Z.json"
B10 = f"{L}/corpus/evidence/baseline-r10-20261015T2231Z.json"
CEN = f"{L}/tools/mori-census.sh"
KD = f"{L}/corpus/knowledge/drift-repin-r20.md"
KS = f"{L}/corpus/knowledge/wave-settlement-r20.md"
LES = f"{L}/corpus/lessons/round-20.md"
C = f"{W}/contract.md"

context = f"""# Goal
FALSIFY wave for mori-shokunin round 20 (fleet/host observability; detection and report only). L1 MoriR20 is the single integration owner and judge; you attack ONE item and report what survives. Claims under attack (frozen contract {C}; lesson {LES}):
- C1 freshness: every token of the census drift vs the r10 baseline is classified in {REG} (closed classes census-schema-change|roster-change|live-state|census-regression, evidence per token); counting command unclassified 8 (r13 register) -> 0 (r20 register) on {ENT}; re-pinned {B20}; post-pin drift `none`. Knowledge {KD}.
- C2 coverage: {TOOL} per-seat wave settlement; independent oracle {ORA}: capability_absent 14 -> 14/14 matched (evidence {W}/evidence/c2-before.json, c2-after.json); co-evolved refinements R1-R5 disclosed in the lesson. Knowledge {KS}. Lane-level ground truth from wave 1 is in {W}/build/Gt*.md.

# Paths and reports
Every path is absolute under {L}. Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>, never under {F}. Your FIRST tool call writes the single line `STATUS: started` to that report path; your LAST action overwrites it with your final report: verdict first (`HOLDS`, `BROKEN`, or `PARTIAL`), then evidence (path:line, or exact command + output + exit code). Mark anything unobserved [INFERENCE]. Scratch files only under {W}/falsify/<YourSeatName>/ or /tmp.

# Bounds
Read-only on the fleet repo {F} (MANIFEST.json, scripts/, templates/, .ufo/state/*, .ufo/watchdog.log), every sibling lane, ~/.omp and host services. Never edit any lane production file ({L}/tools, corpus, SKILL.md, PROVINCE.md, baselines), the lane jj state or Git index; never run mutating git/jj commands. Mutation work happens only on copies under your scratch dir. Search ONLY named files/directories: never grep/glob the whole lane or fleet; never read, grep or list `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/` or ~/.omp session logs (round-19/20 breach class). Never message agent://all; message seats only by exact id. Leaf seat: no subagents, no swarms. Run `bash {CEN}` (≈2 min, heavy) only if your item explicitly says so.

# Tooling
Tool installs are authorized for helpful tools after reading /home/vgpnk/.omp/agent/RULES.md: official channels only; record tool, version, channel and reason in your report. pacman guard: ALL pacman transactions are PAUSED host-wide (orchestrator ruling 2026-10-20) — use uv tool / npx / an official binary in ~/.local/bin, or report the need. Never -Sy/-Syu/-U/-R, never restart a host service. Note: bare `jq` in the bash tool is jaq 3.1.1; use /usr/bin/jq (jq 1.8.2) for counts.

# Honesty
An unrun check has not passed. A missing report is not a dead seat. Never fabricate output, URLs, quotes or counts."""

items = []
def add(name, role, prompt):
    items.append({"name": name, "role": role, "prompt": prompt})

# C2 mutation testing
mut = {
 "MutTrailerLastLine": "revert R1: take only the task's final line as the trailer (lines[-1])",
 "MutStubCounted": "remove R2: treat a `STATUS: started` file as present",
 "MutSymlinkFollow": "replace os.lstat with os.stat for the report path (follow symlinks)",
 "MutTraversalAllowed": "remove the `..`/absolute-path rejection in _safe_report_path",
}
for n, m in mut.items():
    add(n, "mutation-tester", f"Attack C2 test strength. Copy {TOOL} to {W}/falsify/{n}/mori-wave-settlement.py, apply exactly one mutant: {m}. Run `python3 <copy> --selftest` and `python3 {ORA} --tool <copy> --out {W}/falsify/{n}/oracle.json` (/usr/bin/jq .counts). Report KILLED (selftest or oracle fails) or SURVIVED with exact output, plus the unmutated control run.")

# C2 per-lane live rechecks
for lane in ["chousa", "kagi", "kaidoku", "kake", "kama", "kasegi", "kengaku", "kumitate", "mado", "revenger", "souji", "tabi", "tameshi", "tsukuroi"]:
    gt = f"{W}/build/GtLane{lane.capitalize()}.md"
    add(f"Live{lane.capitalize()}", "reviewer", f"Attack C2 accuracy on lane {lane}. Run `python3 {TOOL} scan --lane-root {F}/{lane}-shokunin --fleet-root {F} --out {W}/falsify/Live{lane.capitalize()}/scan.json` (read-only) and compare per dispatch file (members/present/missing/misrooted/stub/state) with the wave-1 manual ground truth {gt} and the committed fleet scan {W}/evidence/c2-live-fleet.json. Explain every difference as live lane change since the snapshot (cite file mtimes) or tool error (cite tool path:line). Report HOLDS/BROKEN.")
for tag, path, gt in [("R18W1", "round-18/wave1-dispatch.json", "GtMoriR18W1"), ("R19W1", "round-19/wave1-run.json", "GtMoriR19W1"), ("R19W2", "round-19/wave2-run.json", "GtMoriR19W2")]:
    add(f"LiveMori{tag}", "reviewer", f"Attack C2 at member level on {L}/.ufo/waves/{path}. Run `python3 {TOOL} scan --lane-root {L} --fleet-root {F}` and compare that wave's `missing` name list and counts with the manual name|status table in {W}/build/{gt}.md (set difference both ways). Report HOLDS/BROKEN with the sets.")

add("CountC2", "reviewer", f"Re-run the C2 counting: `/usr/bin/jq -s '[.[].counts.capability_absent]' {W}/evidence/c2-before.json {W}/evidence/c2-after.json` and `/usr/bin/jq .counts.matched {W}/evidence/c2-after.json`; then regenerate both by running `python3 {ORA} --tool /tmp/<scratch>/absent.py --out <scratch>/before.json` and `python3 {ORA} --tool {TOOL} --out <scratch>/after.json`. Confirm [14,0] and 14. Attack whether the before is observed (harness run) rather than assumed.")
add("SelftestC2", "reviewer", f"Run `python3 {TOOL} --selftest` and read REFINEMENT_CASES and _check_case in {TOOL}. Attack: does each refinement case actually assert the refinement (would it pass without it)? Is the frozen oracle loaded unchanged (compare cases with {W}/frozen/c2-expected.json)? Report per case.")
add("SentinelTool", "sentinel", f"Security review of the integrated {TOOL} (lines cited): traversal, symlinked parent directories, TOCTOU, huge JSON (kaidoku has 3,411 JSON files), report-byte emission (the stub read), private path leakage in output (lane_root absolute path), output determinism. Use only scratch fixtures under {W}/falsify/SentinelTool/.")
add("CriticC2Claim", "critic", f"Attack the C2 claim as an admission: is `capability_absent 14 -> 0` plus refinements a real coverage move or a free lunch? Are the co-evolved refinements honestly separated from the frozen cases (lesson {LES} section Co-evolved)? Does the live demonstration (r19 W1 16/64) count as independent (who counted it first: {L}/.ufo/waves/round-19/wave1-settlement.json)? Verdict HOLDS/BROKEN/PARTIAL with reasons.")
add("VocabFleet", "reviewer", f"Attack the 'never says dead/failed/killed' guarantee: run the tool over every {F}/*-shokunin lane (read-only) and search ONLY the tool's own keys and state words (exclude member names and dispatch paths) for dead|failed|killed. Report counts and any leak.")
add("TabiTxtReports", "scout", f"Attack C2 'missing' semantics: in {F}/tabi-shokunin/.ufo/waves/round-12 and round-13, 63 missing .md reports have same-stem .txt files (wave-1 {W}/build/GtLaneTabi.md). Verify, and judge whether the tool's `missing` misleads an operator; propose the minimal honest wording (no code changes).")
add("KakeSuccessors", "scout", f"Attack C2 'missing' semantics: kake round-22 w2 missing seats were re-run in round-23 w1 ({W}/build/GtLaneKake.md). Verify the 18 successor mappings from the task texts and decide whether knowledge note {KS} §4 states this limit correctly.")
add("DeclaredVsDispatched", "revenger", f"Quantify fleet-wide how many tool-reported `unsettled`/`partial` waves were never (fully) spawned: use lane spawn/refusal records next to each dispatch file (e.g. kama round-19/falsify refused-attempt-1.json, round-21; kagi round-25; tsukuroi round-20/build). Read only the named lane wave dirs. Report a table wave|tool state|spawn evidence|verdict and the share of 'missing' members that are declared-only.")
add("ConnKumitateRoute", "connector", f"Draft (in your report only) a routing note mori would send to kumitate and each lane L1: per-lane counts of missing seat reports from {W}/evidence/c2-live-fleet.json, with the explicit boundary that mori reports filesystem shape and kumitate owns dispatch/result semantics ({F}/kumitate-shokunin/PROVINCE.md). Attack whether {L}/PROVINCE.md round-20 notes keep that boundary.")
add("DiffAltImpl", "reviewer", f"Differential attack: run the independent implementation {W}/build/ImplSettlementAlt/tools/mori-wave-settlement.py and {TOOL} over {L} and three sibling lanes of your choice (read-only, --fleet-root {F}); compare per wave. Explain each difference by the R1-R5 refinements or as a defect in one implementation.")
add("CriticStubProtocol", "critic", f"Attack the round's `STATUS: started` seat protocol and the R2 `stub` status: did the marker raise report retention or distort counts? Use {W}/evidence/wave1-settlement-scan.json, {W}/evidence/c2-live-mori.json (10:46Z, 6 stubs) and {W}/build/ContractReview.md. Verdict and recommendation.")

# C1 family re-verification
fam = {
 "FamJournal": "+FINDING:JOURNAL_CLASSES_UNMEASURED +SURFACE:journal.system +SURFACE:journal.user -SURFACE:journal -FINDING:SEGFAULT_JOURNAL -FINDING:KILL_SIGNAL_JOURNAL HEADER volatile_fields +FINDING:COREDUMP_NOTICE_JOURNAL_USER +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER",
 "FamUnitOOS": "+FINDING:UNIT_FAILURE_OUT_OF_SCOPE",
 "FamRosterLanes": "+FINDING:ROSTER_SET_MISMATCH and the 14 +SURFACE:lane.* tokens (kotodama, souji classed roster-change)",
 "FamRosterFields": "+conf_dropped_n +conf_n +roster_n +roster_source +state_dropped_n +state_n",
 "FamWatchdog": "-FINDING:WATCHDOG_STALE +FINDING:WATCHDOG_STATE_LAG round",
 "FamLaneRowsA": "+path age_s basis +reason +gate_s -example",
 "FamLaneRowsB": "+subject_commits -subject_commits +window -window -attribution -rowb_files",
 "FamWavesIo": "-FINDING:WAVE_UNSETTLED_AGE obs io_avg_unavailable",
}
for n, t in fam.items():
    add(n, "reviewer", f"Attack C1 classifications for: {t}. Read their rows in {REG} and verify every evidence pointer (git -C {L} show/log -S, path:line in {CEN}, baseline lines in {B10}). For each token say AGREE or DISAGREE with the class and why; a class is wrong if its cause pointer does not hold. Cite seat reports in {W}/build/Tok*.md only as leads, re-derive yourself.")
add("AdjudicateStale", "critic", f"Adjudicate `-FINDING:WATCHDOG_STALE`: L1 classes it live-state with blind_spot (rule unchanged since r10; the inline driver writes watchdog.log), dissent in {W}/build/VolatileContract.md (H2) says census-regression. Evidence: STALE absent in {ENT}, present again in the pre-pin drift {PRE} (diff the token lists). Under the frozen class definitions in {C}, which class is right? Does either choice harm an axis?")
add("AdjudicateWaves", "critic", f"Adjudicate `-FINDING:WAVE_UNSETTLED_AGE` (and obs): L1 classes live-state with blind_spot (probe_waves byte-identical since r10; aggregator waves emptied by fleet commit e20f4fa), dissent in {W}/build/VolatileContract.md (H3), {W}/build/C1Critic.md and {L}/corpus/evidence/drift-r12-20261019T2204Z-classification.md:33. Which class is right under {C}? Would re-pinning hide a real condition the census can still see?")
add("CriticC1Claim", "critic", f"Attack C1 as a freshness improvement: the L1 wrote both the register and the count (8 -> 0); the re-pin makes `--drift` read none by construction. What independent evidence shows freshness improved rather than bookkeeping? Consider {KD} sections 3-5 and the HistR13 blind spot (positive-gated findings). Verdict HOLDS/BROKEN/PARTIAL.")
add("CountC1", "reviewer", f"Re-run the C1 counting command from {C} (C1 section) on the stdout in {ENT} (`/usr/bin/jq -r .stdout`) and on the first line of {PRE}, against both {R13} and {REG}. Expected 8->0 and 7->0. Also run `python3 {W}/build/RegisterCheck/check-register.py {REG} {ENT}`. Report exact outputs; attack any token-splitting assumption.")
add("PinIntegrity", "reviewer", f"Verify the re-pin: header of {B20} (census_sha256 = sha256 of {CEN}; pinned_ts; volatile_fields), roll line present, {B10} byte-unchanged vs `git -C {L} show 2061780:corpus/evidence/baseline-r10-20261015T2231Z.json`, census unchanged vs entering tip, post-pin receipt {POST}. Report HOLDS/BROKEN.")
add("PostPinWindow", "scout", f"Measure the new baseline's stability window: run `bash {CEN} --drift {B20}` exactly once (≈2 min). Record UTC time, rc and tokens. Classify every token against {REG} and the lane/ledger events since 10:53Z (fleet watchdog.log tail, lane report commits) — read-only. Report the window honestly; a non-none result is expected evidence, not a failure.")

# sources
srcs = {"S066": "https://raw.githubusercontent.com/approvals/ApprovalTests.Python/5d98f0c166ad2dde7ff60effb12427db8183805e/README.md", "S067": "https://michaelfeathers.silvrback.com/characterization-testing", "S068": "https://docs.python.org/3/library/os.html", "S069": "https://docs.python.org/3/library/pathlib.html", "S070": "https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz (doc/bashref.texi)", "S071": "https://kubernetes.io/docs/concepts/architecture/controller/", "S072": "https://en.wikipedia.org/wiki/Characterization_test"}
for sid, url in srcs.items():
    add(f"Reopen{sid}", "scout", f"Re-open source {sid} ({url}) yourself and verify its row in {L}/corpus/SOURCES.md and the Gate quote in {LES}: quote present verbatim at the stated location, ≤25 words, tier honest for its scope, teaches grounded, status/used-by consistent (used-by paths exist and cite {sid}). Report HOLDS/BROKEN per field.")
add("SourcesCensus", "scout", f"Run `{F}/scripts/sources-census.sh validate --root {F} mori` and the CORPUS.md census commands (section 'SOURCES.md — where a shokunin learns' in {F}/CORPUS.md) from {L}; report outputs and the rows/tier/status histogram before (git -C {L} show 2061780:corpus/SOURCES.md) vs now.")

# corpus review
add("ReviewKnowDrift", "reviewer", f"Review {KD} against its evidence: every number, time and sha must match committed receipts ({ENT}, {PRE}, {POST}, {B20}, {REG}). List each mismatch path:line.")
add("ReviewKnowSettlement", "reviewer", f"Review {KS} against its evidence: every count must match {W}/evidence/c2-live-mori.json, c2-live-fleet.json, c2-before/after.json and the wave-1 ground-truth reports. List mismatches path:line.")
add("ReviewSkill", "reviewer", f"Review the round-20 section at the end of {L}/SKILL.md: is it executable without oral context (commands exist, flags right, exit map right vs {TOOL})? Any claim the tool does not implement? path:line findings.")
add("ReviewProvince", "reviewer", f"Review the round-20 appended notes in {L}/PROVINCE.md and {L}/corpus/README.md: do they move only FR3 per-seat filesystem settlement to Core, keep hygiene/dispatch authenticity/successors in Frontier, and keep kumitate/souji/tsukuroi boundaries? Cross-check {F}/kumitate-shokunin/PROVINCE.md.")
add("ReviewQuality", "reviewer", f"Attack the new criteria 64-68 at the end of {L}/corpus/QUALITY.md: can each fail (name a concrete failing case), is each tied to a lesson row in {LES}, does any duplicate an existing criterion (1-63)?")
add("ReviewLesson", "reviewer", f"Attack {LES} `## Mistakes`: each row needs class, evidence pointer that resolves, captured-by, and a fix shown able to fail. Verify each pointer resolves and each fail-capability claim (run read-only commands where cheap).")
add("ReviewGate", "reviewer", f"Count words of every Gate quote in {LES} (must be ≤25) and verify each new SOURCES row S066-S072 has a Gate row with URL and access date; check the bounded-search entry 'Bounded search 11' in {L}/corpus/SOURCES.md arithmetic (identified/screened/included/excluded).")

# admission / trends / harm
add("CriticTrends", "critic", f"Propose and attack trend verdicts for round 20 per {F}/LEARNING.md observables (expansion, quality, discernment): expansion counts admitted knowledge entries citing a mined row on uncovered coverage ground ({KD}, {KS}); quality and discernment per their observables. Give each verdict with evidence and the strongest counter-argument.")
add("NoHarmRun", "reviewer", f"Run the no-harm battery once (hermetic, read-only to the lane): `bash {CEN} --selftest`, `bash {L}/tools/mori-silence-cases.sh`, and the selftest/regression entry points of {L}/tools/mori-round13-regressions.py, mori-round14-regressions.py, mori-round15-regressions.py, mori-round16-regressions.py, mori-round17-seat-regressions.py, mori-round17-jj-regressions.py, mori-round19-regressions.py (read each header for the right argv; see {W}/build/NoHarmCritic.md). Report each command, last line and exit code. Never run git writes in the lane.")
add("SeparationCheck", "reviewer", f"Verify causal separability: C1 needs no C2 artifact (does {REG}/{B20} depend on {TOOL}?) and C2 needs no C1 artifact (does the tool or oracle read the census, baselines or register?). Use grep on those named files only. Report HOLDS/BROKEN.")
add("FleetMisrootEnd", "scout", f"Run `git -C {F} status --porcelain --no-optional-locks` (no pathspec) and list untracked files whose path or content names mori round 20 or a MoriR20 seat name (wave-1 names in {W}/wave1-spec.json, wave-2 names in {W}/wave2-spec.json). Read-only; never delete.")

# scribes
add("DraftLog", "scribe", f"Draft (in your report) a LOG.md entry for round 20 in the style of the tail of {L}/LOG.md: claims, commits e4d9384 (freeze), 2eeae04 (C2 tool), 8f8c58e (C1 register/pin and corpus), measurements, dead seats, and re-verification result. Use only committed evidence; mark L1-TBD where wave-2 results are needed.")
add("DraftScorecard", "scribe", f"Draft (in your report) the round-20 SCORECARD.md section in the style of the round-19 section at the end of {L}/SCORECARD.md: claims table with before->after and counting commands, axis verdict table (scores held unless justified), capabilities table row for the settlement scan (first-working round 20). Use only committed evidence.")

spec = {"wave": "mori-r20-falsify", "reportDir": ".ufo/waves/round-20/falsify", "maxLanes": 100, "context": context, "items": items}
out = pathlib.Path(W) / "wave2-spec.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(items), dict(Counter(i["role"] for i in items)))
