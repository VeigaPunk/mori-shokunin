#!/usr/bin/env python3
"""Build the round-56 wave w1 spec (L1 MoriR56; one v2 wave, 64 seats: recon,
build verification, attacks on both claims/counters/tools, frontier drafting).
Usage: build-w1-spec.py.  Paths derive from this file's location."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
L = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))  # lane repo
F = os.path.dirname(L)  # fleet root
W = HERE
E = "5b295eeebd87ebd610d8d39bfe2035742f740cfa"  # entering tip
T = "8be2717b0809281d07dffe83dad424a4859e0747"  # freeze+receipts tip (current lane tip)
C1 = W + "/count-c1.py"
C2 = W + "/count-c2.py"
TOOL1 = L + "/tools/mori-driver-liveness.py"
TOOL2 = L + "/tools/mori-vote-bind.py"
FIX = W + "/fixtures/driver"
R55 = W + "/../round-55"
X = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku") + "/mori-r56"
P = "Mo56"
with open(os.path.expanduser("~/.agents/skills/godspeed/directive.md")) as f:
    GODSPEED = "/skill:godspeed\n" + f.read().rstrip("\n")

context = f"""# mori round 56 — wave w1 (one v2 wave: verify + falsify the driver-liveness and vote-binding claims)
Lane: mori-shokunin (森, fleet and host observability: fleet liveness, wave settlement, kill and OOM events, resource runway; detection and report only). Lane repo: {L}. Fleet root: {F}.
The L1 (MoriR56) froze two claims at the freeze tip {T} ({W}/contract.md — read it first; entering tip {E}); data commits c419fe6d + 6ced9da9 landed the tools, entries, source rows, fixtures and receipts; freeze commit 3f494b49 landed contract + pinned counters; 8be2717b landed controls + receipts.
- C1 coverage (FR5 advance): tools/mori-driver-liveness.py reads .ufo/watchdog.log launch/complete/dead/wrap/fail lines and reports per-lane log-shape facts only (13-case selftest, 9 frozen fixtures under {FIX}). Counter: `python3 {C1} R` -> `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok` ({W}/evidence/c1-at-freeze.txt). Do-nothing at {E}: `failed=tool_absent` ({W}/evidence/controls.txt).
- C2 operability (capability): tools/mori-vote-bind.py binds seat-output votes in BOTH plain-text and JSON string-scalar shapes (16-case selftest) and re-binds the round-55 RECHECK tally over committed bytes: `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15` ({W}/evidence/tally-r55.txt), where the frozen round-55 C1 counter reads `voted=0` on the same bytes ({W}/evidence/c2-old-counter-voted0.txt). Counter: `python3 {C2} R` -> `C2=met ... contrast=voted0` ({W}/evidence/c2-at-freeze.txt).
The counters, predicates, controls and kill rules are FROZEN: never propose changing them as a fix for this round; a weakness you find is a named limit + a routed item for round 57. Data (tool code, entries, rows) may still be corrected by the L1 if you show it is wrong — but expect re-pin consequences to be weighed.
Vote-line protocol: this wave carries NO vote items. Never start a line in your report with RECHECK, ENTAIL, QUOTE or REPLACE (quote such text inside a sentence if needed); the L1 and future binders must not find vote-shaped lines in non-voter reports.
Rules for every seat:
- Paths: every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Use absolute paths for every read and write. Write ONLY your own report file ({W}/w1/<your seat name>.md). Drafts go INSIDE your report as fenced blocks; never edit SKILL.md, SHONEN.md, SCORECARD.md, LOG.md, PROVINCE.md, corpus/, tools/, considerthese/, or any file under {W} except your own report. The L1 integrates.
- Scratch (operator directive 2026-10-25): every clone, work tree, fixture and temp file lives under {X}/<your seat name>/ — `mkdir -p` it, `export TMPDIR={X}/<your seat name>/tmp`, and remove it before you finish (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree` in Python); copy anything you cite into your report first. /tmp only for files under 50 MB; a /tmp path is never evidence. One clone per seat at most (`git -C {L} archive <rev> | tar -x -C <scratch>` or `git clone --shared`), never a full mirror. Check `{F}/scripts/hyaku/disk-guard.sh status` before a heavy run; on ENOSPC report the free space and stop.
- Never mutate the fleet repo, sibling lanes, the lane's jj state or git index: no git add/commit/stash/checkout/reset/pull/push in {L} or {F}, no mutating jj command. Read-only git (log/show/diff/rev-parse/ls-files/grep/archive) is fine. Any fixture repo: D=$(mktemp -d -p {X}/<seat>) && git -C "$D" init -q, name -C "$D" on every later call, and verify `git -C "$D" rev-parse --show-toplevel` equals $D before the first commit; never commit under a throwaway identity anywhere else. Never write into ~/.local/bin or any PATH directory.
- Seat tools start at the fleet root: cd into your scratch dir before running anything that writes relative paths.
- Network: keep fetches few and small; git.kernel.org and rfc-editor.org worked on 2026-10-27. /home/vgpnk/Projects/shokuknow is read-only: read bytes, run nothing there.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): ALL pacman transactions are PAUSED host-wide — never run pacman; install via uv tool/npx/an official binary in ~/.local/bin, or report the need.
- Host reads are read-only (detection and report only). Never write a sysctl, never change a cgroup, never run systemctl, never kill/steer any process or session, never write .ufo/watchdog.log or .ufo/state. Reading /proc, /sys, journalctl and the fleet log is allowed. Never count journal records by MESSAGE text (lane rule).
- No credential material, session or private URLs in any report; write a machine id as MACHINE_ID.
- Leaf seat: no subagents. Do not ask questions. Report observed evidence only (command + output + exit code); say UNVERIFIED where you could not check. A dispatched seat is not an independent judge. End your report with a section `## Findings` listing each finding with a severity (HIGH/MED/LOW) and the file or line it concerns.
"""

items = []


def add(name, role, text):
    n = P + name
    items.append({"name": n, "role": role,
                  "prompt": f"{GODSPEED}\n\n{n}: {text} Scratch: {X}/{n}/."})


# ---------------- scouts (recon) ----------------
add("ScoutLogGrammar", "scout",
    f"Recon every DISTINCT line shape in {F}/.ufo/watchdog.log (all 1728 lines) against the frozen grammar in {TOOL1} (docstring lines 13-30). For each shape NOT accepted, paste the line and its count. Then check: are all accepted shapes actually produced by the writer source ({F}/scripts/hyaku/inline.sh:149,176,182; {F}/scripts/shokunin-watchdog.sh:266,398,405,448)? Report grammar shapes with zero live occurrences (candidates for over-breadth).")
add("ScoutCensusOverlap", "scout",
    f"Read the census watchdog surface ({L}/tools/mori-census.sh probe_watchdog, lines ~703-853) and {TOOL1}. List exactly which reads overlap (log mtime? state entries? launch lines?) and which are probe-unique (per-event pairing, in_flight, unclosed, deads, wraps, other_lines). Is the probe's claim — 'the census fires WATCHDOG_ABSENT every round and reads no launch/complete lines' — true at {T}? (census SURFACE watchdog vs the probe's reading).")
add("ScoutR55Shapes", "scout",
    f"Classify the captured `output` of every seat in {L}/.ufo/waves/round-55/w1-results.json into shapes (JSON object with vote_lines / JSON string doc / plain text with unfenced lines / fenced / mixed / empty). For each of the 16 Mo55Rc seats state which channel of {TOOL2} binds it and show the bound vote count. Any shape that binds NEITHER channel? Any shape that binds but should not?")
add("ScoutSiblingOverlap", "scout",
    f"Sibling-overlap scan: do kumitate/tsukuroi/souji/kama hold a driver-liveness reader of .ufo/watchdog.log or a seat-output vote binder (grep their tools/ and corpus/knowledge/)? Check whether sibling corpus/SOURCES.md registries already hold an rfc-editor.org/rfc8259 row or an own-work row for the fleet driver scripts (duplicate-url class). Report overlap or its absence with pointers.")

# ---------------- executors (runs, replays, independent derivations) ----------------
add("ExecDriverSelftest", "executor",
    f"From a `git -C {L} archive {T}` in your scratch: run `python3 tools/mori-driver-liveness.py --selftest` 3 times; all must print `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0` exit 0; paste the three runs. Compare with {W}/evidence (selftest was not separately receipted — note if absent). Also run with TMPDIR and HOME redirected into your scratch (portability).")
add("ExecDriverFixtures", "executor",
    f"For EACH of the 9 fixture dirs under {FIX}: run `python3 {TOOL1} --fixture {FIX}/<name>` and verify verdict DRIVER_LIVENESS_OK and the frozen malformed count (hyaku-pairing 0, attempt-rollover 0, legacy-grammar 0, in-flight 0, malformed 5, fails-and-dead 0, state-shapes 0, two-lanes 0, variants 0). Independently re-derive each expected count by reading the fixture bytes with your own one-liner (awk/grep) — report any fixture whose hand-count disagrees with the frozen value.")
add("ExecDriverLive", "executor",
    f"Run `python3 {TOOL1}` live 3 times (capture full JSON each time). Verify: valid JSON, verdict DRIVER_LIVENESS_OK, lanes set == union of lane ids in {F}/shokunin.conf and *.round names in {F}/.ufo/state/, mori in_flight true, malformed 0. Report the per-run lane count and mori unclosed across runs (mutable values allowed to differ). Paste one full JSON.")
add("ExecBinderSelftest", "executor",
    f"From a `git -C {L} archive {T}`: run `python3 tools/mori-vote-bind.py --selftest` 3 times; all must print `VOTE_BIND_SELFTEST pass=16 fail=0` exit 0. Then run `extract` over one synthetic plain-text output and one JSON-wrapped output you write in scratch; paste the VOTE lines.")
add("ExecBinderTally", "executor",
    f"Reproduce `python3 {TOOL2} tally --ledger {L}/corpus/knowledge/kernel-v7.3-recheck-r55.md --results {L}/.ufo/waves/round-55/w1-results.json --verb RECHECK --voter Mo55Rc01 .. Mo55Rc16` -> the frozen line ({W}/evidence/tally-r55.txt). Then build your OWN independent counter (scratch, do not import the tool): for each of the 78 ledger hashes, list the distinct final words across the 16 captured outputs (any reasonable JSON-aware extraction), and verify: 68 hashes reach >=2 agreeing votes, 10 reach exactly 1, 0 reach 0, 0 dissent. Paste your per-hash table head and the four totals.")
add("ExecBinderControls", "executor",
    f"Run `python3 {W}/controls/controls.py {E} --repo {L}` (scratch TMPDIR). Verify: do-nothing-c1 and do-nothing-c2 PASS, all 8 mutants KILLED, rc 0 — compare {W}/evidence/controls.txt. Then MANUALLY replay two mutants (substring-scalar-binding, roster-filter-dropped) by applying the substitutions yourself and confirm the named selftest arm is the one that kills each (paste the failing arm line).")
add("ExecCounters", "executor",
    f"Run `TMPDIR=<scratch> python3 {C1} {T}` and `python3 {C2} {T}` (expect both met, rc 0), then both at {E} (expect both unmet with failed=tool_absent, rc 1), then both `--selftest`. Also run `python3 {C1} {T}` and `{C2} {T}` with the env var MORI... none exist — instead run them from a different cwd (cd <scratch>) to prove no cwd dependence. Paste every command, last line and exit code.")
add("ExecCensus", "executor",
    f"Census before-state (routed defect: captured bytes only): run `{F}/scripts/sources-census.sh validate --root {F} mori` with stdout+stderr redirected straight into a file, append `exit=$?`; then run the CORPUS.md manual counting commands (row count awk, malformed-row awk expecting 0, tier histogram, status histogram, duplicate-id check, used-by existence check) over {L}/corpus/SOURCES.md. Paste all bytes; compare with {W}/evidence/census-start.txt (start of round: 316 rows, 23 W04, exit 0).")
add("ExecPortability", "executor",
    f"QUALITY 127 + §7 item 4 audit of the four round-56 code files ({TOOL1}, {TOOL2}, {C1}, {C2}) plus controls.py: `grep -nE 'mkdtemp\\(dir=[\"'\"']/tmp|/tmp/' files; `grep -n '/home/vgpnk' files. Classify every hit: executable default that breaks off-host replay / honours TMPDIR or an argument / prose only. Then PROVE both tools honour TMPDIR: run each with TMPDIR=<your scratch>/tmp (created) and show no /tmp write (strace if available, else check /tmp for new files before/after).")
add("ExecR55Contrast", "executor",
    f"Re-run `TMPDIR=<scratch> python3 {L}/.ufo/waves/round-55/count-c1.py {T}` and confirm it still prints `voted=0 ... failed=votes` rc 1 at the freeze tip (the C2 contrast arm). Also re-run it at {E} and diff the two outputs — only the rev field should differ. Paste both last lines.")
add("ExecReceiptStage", "executor",
    f"Routed-defect-2 machinery: run `python3 {L}/.ufo/waves/round-54/checks/receipt-stage.py {T}` (if it accepts a rev; check its usage) against the SCORECARD round-55 rows: confirm the round-55 After cells now cite the landed revision consistently. Then list every receipt file under {W}/evidence and verify each carries its measured revision (grep for rev=/exit=) — name any receipt that does not stamp where it measured.")
add("ExecQuarantine", "executor",
    f"Re-derive the mori slice of the absent-defect register: `awk -F'|' -v l='mori' '$2 ~ (\"`\" l \"`\") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {{print $4, $5}}' {F}/../shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (the shokuknow root is /home/vgpnk/Projects/shokuknow). For each row: fetch the cited source read-only (curl), locate the quoted text if a locator exists, and land a verdict PRESENT/ABSENT/UNVERIFIABLE with the fetch evidence. Append-style output to your report only — never edit the register.")
add("ExecRowsCensus", "executor",
    f"Registry mechanical validation at {T}: run every manual census command from {F}/CORPUS.md section 'SOURCES.md — where a shokunin learns' (row count, malformed NF!=13 expecting 0, tier histogram, status histogram, duplicate ids expecting none, enum/tier-inflation check expecting none, mined used-by existence expecting none missing) over `git -C {L} show {T}:corpus/SOURCES.md`. Paste outputs. Expect 318 rows (+S544/S545), 0 malformed, 23 W04-class duplicates unchanged.")
add("ExecGateSelftests", "executor",
    f"No-harm to the lane's standing instruments: from a `git -C {L} archive {T}`: run `python3 tools/mori-pin-check.py --selftest`, `python3 tools/mori-unlanded-check.py --selftest`, `python3 -I -B tools/mori-commit-runway.py --selftest`, and `bash tools/mori-census.sh --selftest` if present. Compare each tally with {L}/.ufo/waves/round-53/evidence/selftests/ and {L}/corpus/lessons references; any new failure caused by the round-56 files is a HIGH finding. Paste every command, tally, exit code.")

# ---------------- scribes ----------------
add("ScribeDriverEntry", "scribe",
    f"Read {L}/corpus/knowledge/driver-liveness-r56.md and {TOOL1} at {T} side by side. Verify every sentence of the entry against the code (grammar variants, counts, fixture names, limits). Propose precise corrections where wrong (as fenced replacement text in your report); check the two S544 anchor quotes are true substrings of {L}/corpus/evidence/sources-r56/watchdog-log-grammar.txt and <=25 words each.")
add("ScribeBinderEntry", "scribe",
    f"Read {L}/corpus/knowledge/vote-binding-r56.md and {TOOL2} at {T} side by side. Verify every sentence against the code and the receipts ({W}/evidence/tally-r55.txt, c2-old-counter-voted0.txt). Check the three S545 quotes are true substrings of {L}/corpus/evidence/sources-r56/rfc8259.txt (lines 251/308/461) and <=25 words. Propose corrections as fenced text.")
add("ScribeRows", "scribe",
    f"Audit the S544/S545 rows in {L}/corpus/SOURCES.md at {T}: 11 columns each (awk -F'|' NF==13), no literal or escaped pipe inside cells, ids continue the registry, tier/scope/status cells honest (is own-work tier A defensible for S544? argue both ways), opened=2026-10-27, recheck valid, used-by paths exist. Compare the row claims with the Gate table in {L}/corpus/lessons/round-55.md for format. Report defects with the exact cell.")
add("ScribeLesson", "scribe",
    f"Draft the round-56 lesson skeleton (fenced, for the L1 to land at {L}/corpus/lessons/round-56.md): (a) `## Gate` table for S544/S545 — id, URL, accessed 2026-10-27, <=25-word located quote each (from the committed copies); (b) `## Mistakes` — class/evidence/captured-by/fix rows for: the round-55 census row-count misstatement (routed defect 1: report said 298->298, committed bytes 298->316; fix = captured counting-command output, QUALITY 152) and the measurement-revision misattribution (routed defect 2: report cited d27d943a, receipt stamped a27ec482; fix = cite the receipt's stamped rev); (c) census before->after placeholders. Do NOT invent round-56 mistakes — the L1 fills them after the wave.")
add("ScribeScorecard", "scribe",
    f"Draft the SCORECARD.md round-56 section (fenced): two claim rows in the established shape (Claim | Axis | Counting command | Before | After), Before = the controls.txt do-nothing lines at {E}, After = the c1/c2-at-freeze lines at {T} (replace with at-landed placeholders the L1 fills post-integration), plus the Planned(round 57) line naming the dispatch-coverage validator and any routed items. Match the exact table style of the round-55 section.")
add("ScribeConsiderthese", "scribe",
    f"Mine {L}/considerthese/2026-10-26.md (read-only): pick at most ONE still-unimplemented proposal, open what it points at, and draft it as a QUALITY.md criterion (fenced, with the check command and a shown-able-to-fail note) or explain why none qualifies this round. The 2026-10-26 suggestions: (1) split pin-check mismatches into can't-run-here vs stale; (2) follow unfixed critic flags forward; (3) re-execute closures' evidence-verified counters; (4) suggestion-adoption status line. Ground the pick in the actual tool behavior at {T} (run the tool).")

# ---------------- reviewers ----------------
add("RevC1Counter", "reviewer",
    f"Mechanism review of {C1}: hunt false-green paths — can C1=met print while the probe is broken? Check: pin scope (is the sha over the whole file?), selftest string matching (substring vs line), fixture-expectation loopholes (a tool hardcoding the expected malformed counts per fixture name?), the norem check scope (production-only split — can a verdict word hide in the production section via a synonym the list misses?), entry/row substring checks (would a comment in the registry row satisfy 'mined'?). Try 3 concrete bypass constructions on scratch copies; report each as KILLED/BYPASSED with evidence.")
add("RevC2Counter", "reviewer",
    f"Mechanism review of {C2}: same hunt — pin scope; the exact-tally substring check (could the tool print the line on stderr or twice?); the junk control (is junk really junk — no accidental vote surface?); the contrast arm (does it prove what the predicate claims — same bytes, different binding?); entry/row checks. Try 3 concrete bypass constructions; report KILLED/BYPASSED with evidence.")
add("RevDriverProbe", "reviewer",
    f"Code review of {TOOL1}: grammar looseness (what junk does LAUNCH_REST_RE accept? try ` pgid=x`, ` pgid=1 driver=a attempt=b`, huge rest); pairing semantics (can a complete close the wrong round's launch? does dead clear too much? does wrap close attempts?); other_lines vs malformed boundary (line `2026-01-01T00:00:00+00:00` alone? `2026-01-01T00:00:00+00:00 foo`?); state_shapes (broken symlink counts as symlink — intended?); mtime_age None handling. Rate each finding HIGH/MED/LOW with a fixture line that exhibits it.")
add("RevBinder", "reviewer",
    f"Code review of {TOOL2}: the anchored VOTE_RE (word charset, rest capture, trailing spaces, tabs); channel selection edge (output that is JSON `null`/a number/a bool — channel json with zero scalars?); last-wins across the SAME channel only (a text vote then a JSON vote for one hash can never co-occur — prove why); tally agree-counting for single votes (agree==1 for a lone agreeing voter — is that the intended honest surfacing?); read_ledger disposition cell index for ENTAIL-shaped tables (is cell 6 right for an ENTAIL ledger? — construct one and test). Rate findings with exhibiting inputs.")
add("RevClaims", "reviewer",
    f"Read {W}/contract.md and verify against AXES.md rules ({F}/AXES.md): the two claims are on distinct owned axes (coverage, operability), causally separable (name the shared files and why separation still holds), each falsifiable with one command, neither reachable by a do-nothing control (inspect the controls.txt receipts — does a no-op meet either counter?), no universal clause without an enumerating command. Attack the wording of both predicates; list any ambiguity a closure could mis-read.")
add("RevReceipts", "reviewer",
    f"Receipt integrity for every file in {W}/evidence at {T}: each must be literal captured command bytes (no retyped summaries — the r55 routed defect class), each must carry its exit status, and each must name the revision it measured where a revision exists. Re-run the cheap ones (tally, selftests, census validate) and byte-compare with the committed receipts. List each receipt: literal yes/no, exit yes/no, rev-stamped yes/no, reproduces yes/no.")
add("RevSHONEN", "reviewer",
    f"Check {L}/SHONEN.md's four boxes against {T}: every cited pointer must resolve (file exists at {T}, line/section matches the claim). Verify the new round-56 instruments are eligible pointers (run the two new selftests and confirm the tallies the boxes could cite). Propose the exact [~] line updates for round 56.")
add("RevNoHarm", "reviewer",
    f"No-harm audit across all six axes of `git -C {L} diff --stat {E} {T}`: read every changed tracked file. For coverage/operability/depth/freshness/calibration/adjacency name anything the changes could harm (a registry row another entry points at, a census behavior change, a stale pin elsewhere, a scope crossing into kumitate/tsukuroi/souji/kama/kagi). Verdict per axis: harmed/not harmed with evidence.")

# ---------------- critics ----------------
add("CritC1Claim", "critic",
    f"Falsify C1: (a) is FR5's launch/complete ground really unworked before this round — read corpus/README.md FR5 + lessons/round-33.md + the census silence grading; is the probe genuinely new surface? (b) Could a do-nothing control (no probe, just an entry) meet count-c1.py? Read the counter and try. (c) Is 'coverage' the right axis label vs operability? (d) Does the probe duplicate what inline.sh:193 already does (DISPATCH_LINES grep)? Verdict: claim stands / falls, with reasons.")
add("CritC2Claim", "critic",
    f"Falsify C2: (a) is re-binding round-55 bytes an operability capability or just re-scoring history (AXES.md: 'Re-scoring a rule the lane already holds ... is quality work, never coverage or depth')? Argue the operability classification both ways and verdict it. (b) Could a do-nothing control meet count-c2.py (e.g., a preexisting tool that happens to tally)? (c) Is the capability-table row (SCORECARD capabilities) warranted and did the round demonstrate the capability running? Verdict with reasons.")
add("CritDriverSemantics", "critic",
    f"Attack the probe's fact semantics with constructed fixture logs (scratch, run the probe with --fixture): (1) launch r1, launch r2, complete r1 -> what are in_flight/unclosed? (2) dead r1 then launch r1 attempt=2 then complete r1 attempt=1 (stale complete) -> what closes? (3) wrap r1 then launch r1 -> in_flight? (4) two lanes, kake completes mori's round (impossible in grammar but test the pairing keying). For each, state whether the probe's output is misleading as a liveness fact, with severity.")
add("CritBinderSemantics", "critic",
    f"Attack the exact-scalar rule with 10 crafted outputs (run the tool's extract on each): vote with trailing period; vote with markdown bullet '- RECHECK h holds'; vote inside a JSON array element with trailing comma in the RAW text (not parsed as JSON); vote as the ONLY content of a JSON array; vote split across two JSON strings; vote word 'HOLDS' uppercase; 'RECHECK h holds!' with bang; a JSON number 42 doc; empty object {{}}; a JSON array of numbers with the vote as digits. For each: binds or not, and is the answer DEFENSIBLE under the frozen grammar? Name any false negative a reasonable seat could produce.")
add("CritC1CounterFences", "critic",
    f"Attempt to make {C1} print C1=met at a revision where the probe is subtly broken (scratch git fixtures + the counter run with --repo your fixture): try (1) a probe that hardcodes fixture outputs, (2) a probe whose selftest skips when fixtures are missing, (3) a probe with a health-verdict word in a Unicode lookalike. Report each construction and whether the counter printed met (BYPASSED) or unmet (KILLED).")
add("CritC2CounterFences", "critic",
    f"Same fence attack on {C2} at scratch fixture revisions: (1) a binder that binds substring (overclaim) — does the tally arm catch it? (2) a binder that hardcodes the TALLY line regardless of inputs; (3) a binder that reads the ledger from a hardcoded path ignoring --ledger. Report BYPASSED/KILLED each.")
add("CritRegistry", "critic",
    f"Attack the two new registry rows: is S544 tier A defensible (own-work tier rule: 'the lane's own re-runnable gate output' — the driver scripts are the FLEET's, not the lane's; argue the tier both ways and verdict)? Is the S544 anchor a located line range or prose? Does S545 duplicate an existing row (grep the registry for rfc 8259 / json.org)? Does either row's used-by name a path that does not exist at {T}? Severity-rated findings.")
add("CritAssim", "critic",
    f"Attack the 'Assimilation: none' stance for round 56: read /home/vgpnk/Projects/shokuknow/merge/mori/MERGE-REPORT.md and the 3-row quarantine slice; is there any staged entry that OBVIOUSLY should have been adopted this round (e.g., a reconciliation-rules or wave-settlement entry overlapping the claims)? Judge per the per-entry gates (PROVINCE scope, QUALITY bar, coverage-map ground). Verdict: none defensible / name the entry and why.")

# ---------------- mutation testers ----------------
MUT_DRIVER = [
    "LAUNCH_REST_RE opened to accept any rest (r'.*')",
    "in_flight computed as launches>completes instead of last event",
    "malformed counter never incremented (delete _bad body)",
    "other_lines classified as malformed (merge the counters)",
    "state_shapes follows symlinks (os.path.isfile on the target)",
    "dead does not clear open_launches",
    "attempt keying dropped (complete closes (round,None) only)",
    "parse_ts accepts any token (return 0.0)",
]
add("MutDriver1", "mutation-tester",
    f"Mutation-test {TOOL1} in scratch copies (one point each, >=8): " + "; ".join(MUT_DRIVER[:4]) + ". For each mutant run --selftest; KILLED iff rc!=0. Name the killing case for each; a SURVIVOR is a HIGH finding. Also run each mutant over the 9 fixtures and report any fixture that does NOT catch it.")
add("MutDriver2", "mutation-tester",
    f"Mutation-test {TOOL1} (>=8 more): " + "; ".join(MUT_DRIVER[4:]) + ". Same protocol as MutDriver1. Table: mutation -> killed/survived -> killing case; fixture coverage per mutation.")
MUT_BINDER = [
    "VOTE_RE word charset opened to [A-Za-z0-9_-] leading digit",
    "rest made required (vote without rest rejected)",
    "JSON walk skips dict values (lists+top strings only)",
    "tally counts a voter twice if it appears twice in --voter",
    "channel forced to text always (parse JSON skipped)",
    "fence state never toggles (treat all as unfenced)",
    "read_ledger takes disposition from cell 5 instead of 6",
    "dissent counted per voter pair instead of per hash",
]
add("MutBinder1", "mutation-tester",
    f"Mutation-test {TOOL2} in scratch copies (>=8): " + "; ".join(MUT_BINDER[:4]) + ". Protocol: run --selftest; KILLED iff rc!=0; name the killing case; SURVIVOR = HIGH finding. Cross-check each survivor against the tally over the real r55 bytes (does it also corrupt the frozen line?).")
add("MutBinder2", "mutation-tester",
    f"Mutation-test {TOOL2} (>=8 more): " + "; ".join(MUT_BINDER[4:]) + ". Same protocol; add one mutant of your own devising and report it. Cross-check survivors against the real r55 tally.")
add("MutC1Counter", "mutation-tester",
    f"Mutation-test {C1} (the counter itself) with cross-products: >=6 single-point mutants (EXPECT_FIX value softened, a HEALTH_WORDS entry deleted, entry check reduced to file existence, fixture arm deleted, PIN check deleted, rev-parse acceptance of abbreviated revs widened). For each mutant counter, run it at {T} AND at a scratch fixture revision with a matching mutant tool; report every combination that prints C1=met incorrectly (BYPASSED) — the honest finding the freeze pins cannot catch (the counter sha is pinned but nothing re-verifies it at runtime).")
add("MutC2Counter", "mutation-tester",
    f"Mutation-test {C2} with cross-products: >=6 mutants (EXPECT_TALLY substring shortened to 'TALLY', junk control weakened to junk without outputs, contrast arm deleted, entry check reduced to existence, PIN deleted, voters list defaulted to results contents). Run each at {T} and at scratch fixtures; report BYPASSED combinations that print C2=met incorrectly.")

# ---------------- connectors ----------------
add("ConnKumitate", "connector",
    f"Boundary check against kumitate: read {F}/kumitate-shokunin/PROVINCE.md and its corpus/knowledge/swarm-wave-lifecycle.md. Do the driver-liveness probe (per-lane launch/complete/in_flight facts) or the vote binder touch kumitate-owned semantics (wave plan/run/record/collect, lifecycle settlement, result acceptance)? The FR3 boundary says mori reports filesystem/log shape only — verify the probe stays inside it (in_flight is a log fact, not a settlement verdict — is that claim airtight against kumitate's definitions?). Report agreement or a contested boundary with pointers.")
add("ConnSources", "connector",
    f"Cross-lane SOURCES scan: grep every sibling corpus/SOURCES.md (kumitate, tsukuroi, souji, kama, kake, kengaku, kotoba, kaidoku, tabi, chousa, kasegi, mado, tameshi, kaika, kagi if present) for 'rfc8259' and for the fleet driver scripts (inline.sh / shokunin-watchdog.sh as a cited source). Also scan for 'watchdog.log' as a cited source in any sibling registry. Report every hit with the sibling's row id (duplicate-url / overlap class) or state the scan found none, with the grep commands pasted.")

# ---------------- sentinels / revenger / simplifier / labrats / security ----------------
add("SentPorts", "sentinel",
    f"Portability sweep over the round-56 diff ({E}..{T}): `git -C {L} grep -n '/home/vgpnk' {T} -- .ufo/waves/round-56 tools/mori-driver-liveness.py tools/mori-vote-bind.py corpus/knowledge/driver-liveness-r56.md corpus/knowledge/vote-binding-r56.md corpus/evidence/sources-r56` (and the default-repo fallbacks in the two counters). Classify each hit: executable default that breaks off-host replay / honours an argument / prose. Any committed tool that writes under /tmp regardless of TMPDIR is a routed defect (§7 item 4) — report precisely.")
add("SentReceipts", "sentinel",
    f"Freeze integrity: verify {W}/evidence/freeze-sha256.txt — recompute the sha256 of contract.md, count-c1.py, count-c2.py, controls.py at {T} (`git -C {L} show {T}:<path> | sha256sum`) and the two tool shas at 6ced9da9; every line must match. Then verify the two registry anchor sha256 cells (S544 38ba3e6b…, S545 61a5378f…) against the committed copies. Report any mismatch with the exact line.")
add("RevR55", "revenger",
    f"Reconstruct the round-55 binding failure history: `git -C {L} log --format='%h %ad %s' --date=iso -- .ufo/waves/round-55/count-c1.py .ufo/waves/round-54/count-c1.py` and diff the vote-arm code r54 -> r55. When was the stripped-line binding introduced, and where (if anywhere) was the seat-output format rule written down before the r55 wave dispatched? Was the JSON-wrap shape foreseeable from r54's seats? Timeline with hashes, and the check that would have caught it (captured-by).")
add("SimpTools", "simplifier",
    f"Dead-weight review of {TOOL1}, {TOOL2}, {C1}, {C2}, controls.py: unused imports/variables/dead branches/duplicated helpers (e.g., git_ls in count-c1 if unused after the rewrite). Prove each deletion verdict-neutral on scratch copies (selftest tallies unchanged, counter verdict lines identical). The counters are frozen — deletions there are proposals for a successor; the tools may be corrected by the L1 if proven neutral. List each candidate with the proof.")
add("LabProbe", "labrat",
    f"Probe the probe empirically: copy the REAL {F}/.ufo/watchdog.log into scratch and inject, one at a time, 12 unobserved-but-plausible lines (e.g. 'launch x round=1 driver=hyaku-inline slot=2' without attempt; 'complete x round=1; hyaku-inline' without attempt; 'launch x round=1 pgid=1 driver=hyaku-inline attempt=1 extra=1'; a line with a future timestamp; a 5000-char rest). Run the probe per injection and report the classification (parsed/malformed/other) vs your expectation under the frozen grammar. Any crash or hang is a HIGH finding.")
add("LabBinder", "labrat",
    f"Probe the binder empirically: craft 12 synthetic captured outputs spanning the shape space (compact JSON array; pretty-printed JSON; JSON with vote_lines nested 3 deep; a JSON string doc; plain unfenced; fenced; prose-mention; mixed prose+vote; vote with trailing spaces; CRLF line endings; a JSON array containing the vote with a leading newline in the scalar; unicode escape in the hash). Run extract (and tally where meaningful) per output; report bound/not-bound and whether each answer matches the frozen grammar. Any crash is HIGH.")
add("SecTools", "security-reviewer",
    f"Security review of {TOOL1} and {TOOL2}: both parse untrusted text. Check: regex catastrophic backtracking (test the VOTE_RE and LINE_RE/rest regexes against pathological inputs — 2000 nested brackets, 10k-char tokens, alternating quotes); unbounded reads (any max-bytes cap? should there be?); path handling of --log/--ledger/--results/--fixture (traversal, symlink following); any eval/exec/os.system (must be none); tempfile usage (predictable names?). Rate findings; confirm nothing is executed.")
add("SecReports", "security-reviewer",
    f"Scan every round-56 artifact ({W} at {T}, the two tools, the two entries, the evidence copies rfc8259.txt + watchdog-log-grammar.txt, the evidence receipts) for credential material (BEGIN PRIVATE KEY, op://, server.token, session=, cookies), private URLs, and live hostnames beyond the fleet. Also check the new registry rows against the no-credential rule. Report each hit with severity (expect none).")
add("ExecMisroot", "executor",
    f"Misroot pre-sweep (read-only): `git -C {F} status --porcelain` (no pathspec) and list every untracked file at the fleet root or under {F}/.ufo that could belong to mori round 56 (content names mori, round 56, Mo56). Never touch .ufo/state/, .scratch/ or other lanes' files. Output: path + the evidence it is mori's. Expect: none yet (the wave has not run) — the post-wave sweep re-runs this.")
add("CritFrontier", "critic",
    f"Attack the round-56 frontier step as designed in {W}/contract.md: (a) is the mined mistake (r55 census row-count misstatement) the RIGHT class, or should the vote-emission format mistake have been mined instead? (b) does the sourced-claim rule hold — BOTH claims must rest on a row opened this round: C1 on S544, C2 on S545 — read the two entries and verify the citations are load-bearing (remove the citation: does the entry still stand?). (c) is the census before->after command the frozen one? Verdict per item.")
add("RevSourcesContract", "reviewer",
    f"End-to-end SOURCES.md contract-v1 conformance at {T}: shape (header, Registry table, Paths, Search log, Leads), row schema (11 columns, id/kind/tier/scope/anchor/teaches/status/opened/recheck/used-by cells), the 0-3 leading-space parser rule, no pipes in cells, append-only discipline (diff {E}..{T} shows only S544/S545 added and no in-place edits to other rows — verify with git diff). Report every violation with the line.")
add("ScribeSearchLog", "scribe",
    f"Draft the round-56 Search-log entry (fenced) for corpus/SOURCES.md `## Search log`: question ('what grounds the JSON vote-surface grammar and the watchdog-log line grammar'), where searched (rfc-editor.org; the fleet writer scripts), date 2026-10-27, identified/screened/included counts, exclusion reasons, stop rationale. Match the style of the round-38/39 entries at the tail of the section.")
add("ExecDriftPin", "executor",
    f"No-harm to the freshness instruments: locate the pinned drift baseline ({L}/corpus/evidence/baseline-r10-*.json) and run `bash {L}/tools/mori-census.sh --drift <baseline>` read-only; confirm the pin still evaluates (exit code + verdict line). Then confirm the round-56 changes did not touch the census, the baseline, or the silence oracle (git diff --name-only {E}..{T}). Any regression is a HIGH finding.")
add("LabCensusSpace", "labrat",
    f"Probe the census parser's 0-3 leading-space rule: copy corpus/SOURCES.md into scratch, append one row with TWO leading spaces whose id collides with a staged shokuknow id (use S471 from merge/mori), run `{F}/scripts/sources-census.sh validate --file <copy>` and show the collision/malformed behaviour; then append the same row at column zero and diff the validator output. Report whether the 0-3-space pattern matters for mori's registry hygiene (per the assimilation contract's collision check).")
add("ExecAssimSlice", "executor",
    f"Re-derive the mori absent-defect register slice independently of ExecQuarantine: same awk over /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md; count the rows; compare with the 2026-10-24 census note (mori slice) and with any prior round's verdict file ({L}/.ufo/waves/round-5*/assimilation/quarantine-verdicts.txt). Report row count, ids, and whether prior verdicts (S244 flip, S262/S268 PRESENT) are consistent with the register text.")


def main():
    spec = {"wave": "mori-r56-w1", "reportDir": ".ufo/waves/round-56/w1", "context": context, "items": items}
    with open(os.path.join(W, "w1-spec.json"), "w") as f:
        json.dump(spec, f, indent=1)
    roles = {}
    for it in items:
        roles[it["role"]] = roles.get(it["role"], 0) + 1
    attack = sum(v for k, v in roles.items() if k in ("reviewer", "critic", "mutation-tester", "labrat", "security-reviewer"))
    print(len(items), roles, "attack=%d (%.1f%%)" % (attack, 100.0 * attack / len(items)))


if __name__ == "__main__":
    main()
