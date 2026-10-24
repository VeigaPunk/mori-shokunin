#!/usr/bin/env python3
"""Generate the mori round-20 wave-1 (build) spec. L1-authored; output is committed evidence."""
import json, pathlib

L = "/home/vgpnk/Projects/shokunin/mori-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-20"
C = f"{W}/contract.md"
X = f"{W}/frozen/c2-expected.json"
E = f"{W}/evidence/c1-drift-entering.json"
R13 = f"{L}/.ufo/waves/round-13/evidence/drift-classification.json"
CEN = f"{L}/tools/mori-census.sh"
B10 = f"{L}/corpus/evidence/baseline-r10-20261015T2231Z.json"
PIN = f"{W}/evidence/c1-pin-probe-scratch.json"

context = f"""# Goal
mori-shokunin round 20 (fleet/host observability: fleet liveness, wave settlement, kill/OOM events, resource runway; detection and report only). L1 MoriR20 is the single integration owner and holds the planner seat. Frozen claim contract (read it first): {C}. C1 freshness: classify every live drift token of the census against the r10 baseline and re-pin. C2 coverage: new read-only per-seat wave-settlement tool tools/mori-wave-settlement.py, oracle {X}.

# Paths and reports
Every path is absolute under {L}. Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>, never under {F}. Your FIRST tool call writes the single line `STATUS: started` to that report path; your LAST action overwrites it with your final report (markdown, findings with path:line or command+output evidence; mark anything unobserved [INFERENCE]). Candidate code or drafts go only under {W}/build/<YourSeatName>/ .

# Bounds
Read-only on: the fleet repo {F} (MANIFEST.json, scripts/, templates/, .ufo/state/*, .ufo/watchdog.log), every sibling lane repo, ~/.omp, host services. Never edit {CEN}, any committed baseline, lane production files, the lane jj state or Git index; never run git/jj mutating commands (add, commit, checkout, stash, reset, jj new/describe/...). Never open retained interactive-session transcripts or ~/.omp session logs. Never message agent://all; message seats only by exact id. Leaf seat: no subagents, no swarms (an executor may spawn at most one read-only labrat). Do not run builds/linters/formatters or full lane selftests unless your item says to run something; the L1 runs acceptance once after integration. Do not run tools/mori-census.sh unless your item explicitly says so (it takes ~2 min and heavy CPU).

# Tooling
Tool installs are authorized for helpful tools after reading /home/vgpnk/.omp/agent/RULES.md: official channels only; record tool, version, channel and reason in your report. pacman guard: ALL pacman transactions are PAUSED host-wide (orchestrator ruling 2026-10-20) — use uv tool / npx / an official binary in ~/.local/bin instead, or report the need. Never -Sy/-Syu/-U/-R, never restart a host service.

# Honesty
An unrun check has not passed. A missing report is not a dead seat. Never fabricate output, URLs, quotes or counts."""

items = []
def add(name, role, prompt):
    items.append({"name": name, "role": role, "prompt": prompt})

# ---- C2 code (executors)
add("ImplSettlement", "executor", f"Implement C2 exactly per {C} section C2 as a new stdlib-only Python 3 file {W}/build/ImplSettlement/tools/mori-wave-settlement.py (scan + --selftest). --selftest builds every case of {X} in a TMPDIR and asserts it; print `MORI_WAVE_SETTLEMENT_SELFTEST: PASS|FAIL (N cases, P passed, F failed)`. Use os.lstat (no symlink following), reject absolute/.. paths before any stat, never print report bytes. You may run your own --selftest and one scan of {L} with --fleet-root {F} (read-only). Report: the file path, its sha256, selftest line, and the r19 wave1 counts your scan printed.")
add("ImplSettlementAlt", "executor", f"Write an INDEPENDENT second implementation of the C2 tool from {C} (do not read build/ImplSettlement/) at {W}/build/ImplSettlementAlt/tools/mori-wave-settlement.py, stdlib Python 3, scan only (no selftest needed). Purpose: differential testing. Run it once: `python3 <file> scan --lane-root {L} --fleet-root {F} --out {W}/build/ImplSettlementAlt/mori-scan.json`. Report sha256, exit code, and per-wave members/present/missing/misrooted table.")
add("OracleHarness", "executor", f"Write an independent oracle harness {W}/build/OracleHarness/c2-oracle.py (stdlib) that builds one temp fixture per case of {X} itself (never importing or reading any tool source), runs `python3 TOOL scan ...` as a subprocess, and checks every expect key. Usage: `c2-oracle.py --tool PATH --out FILE`. If TOOL does not exist every case is `capability_absent`. Output JSON schema mori-r20-c2-oracle-v1 with counts {{matched, mismatched, capability_absent}} and per-case results (observed fields + issues). Run it once with --tool {L}/tools/mori-wave-settlement.py (absent now) and write {W}/build/OracleHarness/c2-before-candidate.json. Report sha256 and counts.")
add("LiveRunner", "executor", f"Write {W}/build/LiveRunner/c2-fleet-live.py (stdlib): given --tool PATH and --fleet-root {F}, run `TOOL scan --lane-root <lane> --fleet-root {F} --out <tmp>` for every {F}/*-shokunin lane, collect per-lane totals (waves, members, present, missing, empty, misrooted, unsafe, unparsed, unreadable_json, exit) into one JSON (schema mori-r20-c2-fleet-live-v1) sorted by lane, plus a flag listing dispatch files whose filename contains preview|undispatched|validation|not-dispatched (shape only). Do not run it against a real tool (none exists yet); unit-check it with a 10-line fake tool in your build dir. Report the file sha256 and fake-tool output.")
add("RegisterCheck", "executor", f"Write {W}/build/RegisterCheck/check-register.py (stdlib): validates a drift-classification register (schema mori-drift-classification-v1: object `tokens` mapping token -> {{class, reason, evidence}}; class in census-schema-change|roster-change|live-state|census-regression; reason and evidence non-empty strings) against a drift stdout file. Prints `MORI_DRIFT_REGISTER: unclassified=N invalid=M regression=K tokens=T` and exits 0 only when N=M=K=0, 1 otherwise, 2 on usage/unreadable. Old-style registers whose values are bare strings count as invalid, not classified. Self-check it on {E} stdout vs {R13} and report the printed line.")

# ---- C1 token classification scouts
fam = {
 "TokJournalUser": "+FINDING:COREDUMP_NOTICE_JOURNAL_USER +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER",
 "TokUnitOOS": "+FINDING:UNIT_FAILURE_OUT_OF_SCOPE",
 "TokWatchdog": "-FINDING:WATCHDOG_STALE +FINDING:WATCHDOG_STATE_LAG round",
 "TokPathAge": "+path age_s",
 "TokIoAvg": "io_avg_unavailable",
 "TokJournalSchema": "+FINDING:JOURNAL_CLASSES_UNMEASURED +SURFACE:journal.system +SURFACE:journal.user -FINDING:SEGFAULT_JOURNAL -SURFACE:journal -FINDING:KILL_SIGNAL_JOURNAL HEADER volatile_fields",
 "TokRosterLanes": "+FINDING:ROSTER_SET_MISMATCH and the 14 +SURFACE:lane.<id> tokens (audio chousa game-dev-2d game-dev-3d kaidoku kotodama lore mado mori revenger souji tabi tameshi tsukuroi)",
 "TokRosterFields": "+conf_dropped_n +conf_n +roster_n +roster_source +state_dropped_n +state_n",
 "TokSilenceA": "+subject_commits -subject_commits +window -window -attribution -rowb_files",
 "TokSilenceB": "basis obs +reason +gate_s -example",
 "TokWaves": "-FINDING:WAVE_UNSETTLED_AGE",
}
for n, t in fam.items():
    add(n, "scout", f"C1 token classification. Tokens: {t}. They appear in the entering drift receipt {E} (census `--drift {B10}`). For each token: find which census line(s) emit it now (path:line in {CEN}) and in the baseline file, the commit that introduced the change (`git -C {L} log -S<id> --oneline -- tools/mori-census.sh`, git show), and decide exactly one class: census-schema-change (intended, documented change), roster-change, live-state (host/fleet state differs, census logic same) or census-regression (unintended behavior change). Cite the round LOG/SCORECARD/knowledge line stating intent where one exists. Compare with the older classification in {R13} and say agree/disagree with reasons. Report a JSON-ready table token|class|reason|evidence.")
add("TokPinFlap", "scout", f"C1 stability. The L1 pinned the live census at 10:23:18Z to /tmp/mori-r20/pin-probe.json (copy committed as {PIN} if present; else read /tmp) and drift against it ~65 s later gave rc 1 `+path +reason -subject_commits -window basis round`. Identify which SURFACE line(s) changed between the pin and a fresh run: you MAY run `bash {CEN}` exactly once (read-only, ~2 min) and diff its normalized lane rows against the pin. Classify each flapping field (live-state vs census nondeterminism) with evidence. Report which lane rows flapped and why.")

# census history reviewers
hist = {"HistR12": "1f07f1d", "HistR13": "18d7d55", "HistR14R15": "8d22d18 26f6589", "HistR17": "273aa74 2be8294 fe9fa90"}
for n, c in hist.items():
    add(n, "reviewer", f"C1 census-regression hunt. Review commit(s) {c} to tools/mori-census.sh in {L} (`git -C {L} show <c> -- tools/mori-census.sh`). For each behavior change, state whether it is declared in that round's SCORECARD/LOG/knowledge (cite path:line) and which drift tokens of {E} it explains. Flag any change to default census output that is NOT declared as a candidate census-regression with path:line. Read-only.")
add("VolatileContract", "reviewer", f"C1 masking risk. Read the volatile contract and masking section of {L}/corpus/knowledge/drift-pin-r10.md and the drift code in {CEN} (run_pin/run_drift/drift_normalize). Given that re-pinning makes current behavior the new reference, list what kinds of regression a re-pin could launder and which evidence (per-token classification, census SHA unchanged, selftest) rules each out. Recommend whether any token family should be declared volatile — recommendation only, no edits.")
add("C1Critic", "critic", f"Attack C1 in {C}: is a classified re-pin a real freshness move or bookkeeping? Is `unclassified 8→0` a free lunch (the L1 writes both the register and the count)? Name the strongest falsifier (e.g. a token wrongly classed live-state, a register that classifies by prefix), and what non-author evidence would decide it. Concrete, path:line.")

# ---- C2 ground truth, mori waves
mori_disp = ["round-13/dispatch.json", "round-14/dispatch.json", "round-15/dispatch.json", "round-16/wave1-dispatch.json", "round-17/wave1-dispatch.json", "round-17/wave2-dispatch.json", "round-18/wave1-dispatch.json", "round-18/wave2-dispatch.json", "round-19/wave1-run.json", "round-19/wave2-run.json"]
for d in mori_disp:
    tag = d.replace("round-", "R").replace("/", "").replace("-dispatch.json", "").replace("dispatch.json", "").replace("-run.json", "").replace("wave", "W")
    add(f"GtMori{tag}", "scout", f"C2 independent ground truth (manual, no tool). File {L}/.ufo/waves/{d}. Using jq and ls/stat only: list taskCall.tasks[*].name, extract each task's last `Report: write your scoped findings to <path>` line, and for each member record present (regular non-symlink file >0 bytes under {L}), empty, missing, and whether the same relative path exists under {F} (misrooted). Compare with any settlement/closure count recorded for that wave (wave*-settlement.json, LOG.md, SCORECARD.md, {F}/MANIFEST.json closure notes — read-only). Report a table name|status and totals.")

# ---- C2 ground truth, sibling lanes
for lane in ["chousa", "kagi", "kaidoku", "kake", "kama", "kasegi", "kengaku", "kumitate", "mado", "revenger", "souji", "tabi", "tameshi", "tsukuroi"]:
    add(f"GtLane{lane.capitalize()}", "scout", f"C2 independent fleet ground truth (manual, read-only, no tool). For lane {F}/{lane}-shokunin: list every *.json under .ufo/waves whose top-level schema is ufo-swarm-wave-dispatch-v1 (jq). For each: member count, Report-trailer paths parsed/unparsed, present/empty/missing under the lane root, misrooted (same relative path under {F}), and whether the filename suggests it was never dispatched (preview/undispatched/validation). Do not edit anything in that lane. Report per-file totals and lane totals.")

# ---- revengers
add("RevR19NoReport", "revenger", f"Reverse-engineer why mori round-19 wave 1 retained only 16 of 64 reports. Inputs: {L}/.ufo/waves/round-19/wave1-run.json, wave1-settlement.json, wave1-attempts.json, wave1-context.json, build/, {L}/corpus/lessons/round-19.md, the round-19 closure notes in {F}/MANIFEST.json (read-only). Test hypotheses: misrooted under {F}; wrong report dir; prompt never asked for a file; seat failed before writing. Use file evidence only — never session transcripts. Report each hypothesis supported/refuted with evidence.")
add("RevR18Dead", "revenger", f"Calibration check of `missing report != dead seat`. Mori round 18 wave 1 recorded 15 provider-capacity dead seats ({L}/.ufo/waves/round-18/evidence/wave1-dead-seats.json, wave1-attempts.json). Cross-tabulate dead-seat ids against report presence for {L}/.ufo/waves/round-18/wave1-dispatch.json members: dead-with-report, dead-without, alive-without. Report the 2x2 table with member names.")

# ---- connectors
add("ConnKumitate", "connector", f"Sibling-overlap scan for C2. kumitate owns orchestration/wave lifecycle semantics ({F}/kumitate-shokunin/PROVINCE.md, corpus/knowledge/swarm-wave-lifecycle.md). Does the C2 tool in {C} stay on mori's side (filesystem shape, no result semantics, no 'failed/dead')? Cite boundary lines. Also check whether kumitate already ships an equivalent counter. Read-only.")
add("ConnSoujiTsukuroi", "connector", f"Sibling-overlap scan: souji (artifact cleanup — could hygiene empty/delete reports, FR3 emptied-by-hygiene) and tsukuroi (host OS). Read {F}/souji-shokunin/PROVINCE.md and {F}/tsukuroi-shokunin/PROVINCE.md and mori {L}/PROVINCE.md Adjacent. Name any surface C1/C2 touch that a sibling owns and how mori must route it.")
add("ConnFleetScripts", "connector", f"Overlap scan with fleet tooling: read {F}/scripts/hyaku/wave-live.py, status.sh, wave-slot.sh, inline.sh (read-only). Does any already count per-seat report settlement? Compare its semantics with C2 in {C}; list agreements and differences with path:line. Recommend reuse vs separate.")
add("ConnValidatorSchema", "connector", f"Read /home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs (read-only). Confirm with path:line: the dispatch schema id, where taskCall.tasks come from, the exact rendered Report trailer text, registry schema and member fields, and whether a resume-only wave has taskCall null. List any trailer variant the regex in {C} would miss.")

# ---- reviewers
add("ContractReview", "reviewer", f"Review the frozen C2 contract {C} and cases {X} for ambiguity or untestable wording (trailer regex, state rules, misrooted precedence, symlink semantics, exit codes). Also: dispatch-schema files that were never dispatched (preview/undispatched/validation) — how should output avoid implying dispatch? Give concrete refinement proposals labelled co-evolved (the frozen bytes stay unchanged).")
add("TrailerVariants", "reviewer", f"Across every *.json under {F}/*-shokunin/.ufo/waves with schema ufo-swarm-wave-dispatch-v1, extract the last line of each taskCall task. Count lines matching `^Report: write your scoped findings to \\S+$` vs others per lane; list distinct non-matching shapes (redact nothing private; these are lane files). jq/grep only, read-only.")
add("QualityCriteria", "reviewer", f"Read {L}/corpus/QUALITY.md (criteria 1–63) and {L}/corpus/lessons/round-19.md. Propose 2–4 new numbered criteria (64+) that would have caught: (a) the round-19 48 missing wave-1 reports not being counted until closure; (b) a drift baseline left unpinned for nine rounds while every round re-observed exit 1. Each criterion must be able to fail; give the exact failing condition.")
add("SpotcheckR19", "reviewer", f"Read the mori round-19 closure entry in {F}/MANIFEST.json (jq select lane==mori, round 19; read-only) and {F}/.ufo/reports/round-19/mori.md. List every routed debt/disagreement and say for each whether round 20 must turn it into a QUALITY criterion, a fix, or an explicit carry. No edits.")
add("CensusWavesSurface", "reviewer", f"Document the before state for C2: read the `SURFACE waves` probe in {CEN} (path:line) and its knowledge notes; state exactly what it reports today (presence, age, settled/unsettled at wave level) and confirm it never counts per-seat reports. Quote the emitted key names.")

# ---- critics
add("C2Critic", "critic", f"Attack C2 in {C}: is `capability_absent 14→0` a free lunch? Is the live r19 16/64 reproduction a genuine independent check (who counted 16)? Name inputs where the tool would mislead an operator (undispatched dispatch files, reports deleted by hygiene, renamed report dirs). Concrete.")
add("SeparationCritic", "critic", f"Attack the round's admission frame in {C}: lowest-axis selection (freshness vs depth vs calibration ties), causal separability of C1/C2, and whether either claim harms operability (census untouched?) or adjacency (kumitate scope). Cite {L}/SCORECARD.md lines.")
add("NoHarmCritic", "critic", f"Pre-register no-harm checks: list the exact commands the L1 must run at the measured commit to show no axis harmed (census selftest, oracle, r13–r19 regression scripts in {L}/tools, sources census). Read the tools' headers to give exact argv. Do not run them.")

# ---- sentinel
add("SafetySentinel", "sentinel", f"Security review of the C2 design in {C}: path traversal, symlink following, TOCTOU, huge files, JSON bombs, report-content emission, private path leakage in output (member names vs paths). Propose concrete guards; review any candidate under {W}/build/ImplSettlement*/ if present when you run.")

# ---- scribes
add("DraftDriftNote", "scribe", f"Draft {W}/build/DraftDriftNote/drift-repin-r20.md: knowledge note for C1 — why the r10 pin stayed red nine rounds, the classification closed set, the re-pin ritual (classify all tokens, zero census-regression, census SHA unchanged, pin, immediate re-drift recorded), and the observed immediate-drift flap (`+path +reason -subject_commits -window basis round` 65 s after a pin). Cite {E} and {L}/corpus/knowledge/drift-pin-r10.md. Placeholders where L1 will insert final numbers, marked TODO-L1.")
add("DraftSettlementNote", "scribe", f"Draft {W}/build/DraftSettlementNote/wave-settlement-r20.md: knowledge note for C2 per {C} — states, exit codes, why missing≠dead, misrooted detection, undispatched-file caveat, FR3 boundary with kumitate. Mark final numbers TODO-L1.")
add("DraftLesson", "scribe", f"Draft {W}/build/DraftLesson/round-20-mistakes.md: `## Mistakes` rows (class · evidence pointer · captured-by · fix) for: M1 round-19 wave-1 48 missing reports counted only by hand at recovery/closure (captured-by none; fix = C2 tool shown to fail on that wave); M2 r10 drift pin red for nine rounds without a complete current classification (captured-by none). Evidence pointers into {L} and {F}/MANIFEST.json only.")
add("SrcApprovalTests", "scribe", f"Frontier source for C1. Open the ApprovalTests documentation (e.g. https://approvaltests.com/ and the approvals GitHub docs on approving/received files) and propose one SOURCES row (shape: id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by — read {L}/corpus/SOURCES.md header and CORPUS contract in {F}/CORPUS.md section 'SOURCES.md — where a shokunin learns') with URL, access date 2026-10-21 and a located quote ≤25 words about reviewing a difference before approving a new golden/approved output. If unreachable, say so; never invent a quote.")
add("SrcCharacterization", "scribe", f"Frontier source for C1. Open a primary/authoritative page on characterization (golden-master) tests (e.g. Michael Feathers' writing, or Wikipedia 'Characterization test' as tier C) and propose a SOURCES row with URL, access date 2026-10-21, located ≤25-word quote about a characterization test capturing actual current behavior. Note tier honestly. Never invent a quote.")
add("SrcPythonLstat", "scribe", f"Frontier source for C2. Open https://docs.python.org/3/library/os.html (os.lstat / os.stat follow_symlinks, os.scandir DirEntry.is_symlink) and propose one SOURCES row with a located ≤25-word quote that grounds 'do not follow symlinks when checking report presence'.")
add("SrcPathContainment", "scribe", f"Frontier source for C2. Open https://docs.python.org/3/library/pathlib.html and/or os.path docs (PurePath.is_relative_to, os.path.commonpath, realpath) and propose one SOURCES row with a located ≤25-word quote grounding the lexical-vs-resolved containment check for report paths (and its symlink caveat).")
add("SrcBashLead", "scribe", f"Resolve the open lead in {L}/corpus/SOURCES.md `## Leads (unopened)`: try to open the GNU Bash manual section on pipefail/PIPESTATUS (https://www.gnu.org/software/bash/manual/bash.html or html_node pages). If opened, propose a row with a located ≤25-word quote; if not, record each URL tried and its error.")
add("SrcK8sController", "scribe", f"Frontier source for C2 framing. Open https://kubernetes.io/docs/concepts/architecture/controller/ and propose a SOURCES row (likely tier B for our host) with a located ≤25-word quote on desired vs current state observation, scoped to: mori reports observed-vs-declared settlement, it does not reconcile. Never invent a quote.")
add("DraftSkillSection", "scribe", f"Draft {W}/build/DraftSkillSection/skill-r20.md: a SKILL.md section (≤40 lines) with decision table: when to run the settlement scan, how to read each state, what never to conclude (dead/failed), and the drift re-pin ritual. Read {L}/SKILL.md tail first to match its style.")
add("DraftProvince", "scribe", f"Draft {W}/build/DraftProvince/province-r20.md: exact text to append to {L}/PROVINCE.md and {L}/corpus/README.md Frontier for the FR3 advance (per-seat filesystem settlement into Core; emptied-by-hygiene vs never-written and dispatch authenticity stay frontier).")

# ---- misc scouts
add("SourcesRecheck", "scout", f"Read {L}/corpus/SOURCES.md registry. List rows whose recheck is due by 2026-10-21 (90d/30d/on-release given opened dates), queued rows that C1 (drift baseline) or C2 (wave settlement) could mine, and any malformed row. Run `{F}/scripts/sources-census.sh validate --root {F} mori` once and paste output+rc.")
add("MisrootSweep", "scout", f"Read-only: run `git -C {F} status --porcelain` (no pathspec) and list any untracked file whose content names mori round 20 or this wave's seat names. Also list historical mori misroots documented in {L}/corpus/lessons/round-1[6-9].md. Never delete or move anything.")
add("FleetDispatchInventory", "scout", f"Inventory: for every {F}/*-shokunin lane list each .ufo/waves JSON with schema ufo-swarm-wave-dispatch-v1: path, sha256, wave field, task count, resume count. Write the inventory as JSON at {W}/build/FleetDispatchInventory/inventory.json (this is your report artifact) and summarize lane totals in the report.")

spec = {"wave": "mori-r20-build", "reportDir": ".ufo/waves/round-20/build", "maxLanes": 100, "context": context, "items": items}
out = pathlib.Path(W) / "wave1-spec.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
from collections import Counter
print(len(items), dict(Counter(i["role"] for i in items)))
