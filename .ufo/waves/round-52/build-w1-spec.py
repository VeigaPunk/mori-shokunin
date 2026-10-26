#!/usr/bin/env python3
"""Build the round-52 wave w1 spec (L1 MoriR52; one v2 wave after the data commit: the C2 entailment votes,
attacks on both claims, frontier drafting, routed-defect evidence). Usage: build-w1-spec.py <freeze> <data>.
Paths derive from this file's location."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
L = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))  # lane repo
F = os.path.dirname(L)  # fleet root
W = HERE
E = "4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d"  # entering tip
FZ = sys.argv[1]  # freeze
T = sys.argv[2]  # data commit
C1 = W + "/count-c1.py"
C2 = W + "/count-c2.py"
SRC = L + "/corpus/evidence/sources-r52"
ENTRY = "corpus/knowledge/overcommit-commit-limit-r52.md"
X = "/fast/scratch/hyaku/mori-r52"
P = "Mo52"
HASHES = W + "/evidence/c2-hashes-at-data.txt"
R51 = L + "/.ufo/waves/round-51"
HASH1 = ("python3 -c 'import hashlib,re,sys;print(hashlib.sha256(re.sub(r\"\\s+\",\" \",sys.argv[1]).strip()"
         ".encode()).hexdigest()[:12])' \"<claim text>\"")
GODSPEED = """/skill:godspeed
1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

context = f"""# mori round 52 — wave w1 (one v2 wave: entailment votes, attacks on both claims, frontier drafting)
Lane: mori-shokunin (森, fleet and host observability: fleet liveness, wave settlement, kill and OOM events, resource runway; detection and report only). Lane repo: {L}. Fleet root: {F}.
The L1 (MoriR52) froze two claims at {FZ} ({W}/contract.md — read it first; entering tip {E}) and landed the data at {T}:
- C1 calibration: `python3 {C1} {T} --scratch {X}/<your seat>/c1` -> see {W}/evidence/c1-at-data.txt; entering `C1=unmet … mismatches=8` ({W}/evidence/control-c1-do-nothing.txt). Arms: (A) SCORECARD `## Axes` vs the fleet MANIFEST and the newest closure's per-axis scores; (B) SHONEN tally pins run at R with round-52 receipts; (C) K4 beyond SHONEN — every single-line command-tally pin in corpus/QUALITY.md and corpus/README.md runs today or is superseded by a later line, never rewritten; (D) `path:N` locators in the Axes rows and SHONEN boxes land on the quoted words. Data diff: `git -C {L} diff {E} {T} -- SCORECARD.md SHONEN.md corpus/QUALITY.md corpus/README.md .ufo/waves/round-52/evidence/selftests`.
- C2 depth: new entry {L}/{ENTRY} (what /proc/meminfo's CommitLimit and Committed_AS are at kernel v7.2: the overcommit ledger, enforced only under vm.overcommit_memory=2), rows S497-S501 in {L}/corpus/SOURCES.md, copies under {SRC}/. `python3 {C2} {T}` -> `… located=28 … entailed=0 … failed=entailment` ({W}/evidence/c2-at-data.txt). P-C2 also requires, for every claim row, `entailed` votes from at least TWO of the twelve ENTAILMENT seats Mo52Ent01-Mo52Ent12 that did not write the row's text. Row hashes: {HASHES}.
The counters, predicates, controls and kill rules are FROZEN: never propose a change to them as a fix for this round; a counter weakness you find is a named limit for the report and a routed item for round 53. Data (entry wording, SOURCES rows, SCORECARD/SHONEN cells, the appended QUALITY/README text) may still be corrected by the L1 if you show it is wrong.
ENTAIL and REPLACE lines (read even if your item is not an entailment item): the C2 counter reads unfenced lines that start (after spaces) with `ENTAIL <12 hex> entailed|overclaim` or `REPLACE <12 hex> :: <text>` ONLY in the reports {W}/w1/Mo52Ent01.md … Mo52Ent12.md. Every other seat must never start a line with the word ENTAIL or REPLACE (quote such text inside a sentence if needed).
Rules for every seat:
- Paths: every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Use absolute paths for every read and write. Write ONLY your own report file. Drafts go INSIDE your report as fenced blocks; never edit SKILL.md, SHONEN.md, SCORECARD.md, LOG.md, corpus/, tools/, considerthese/, or any file under {W} except your own report. The L1 integrates.
- Scratch (operator directive 2026-10-25): every clone, work tree, fixture and temp file lives under {X}/<your seat name>/ — `mkdir -p` it, `export TMPDIR={X}/<your seat name>/tmp`, pass it explicitly to every tool (counters take `--scratch`), and remove it before you finish (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree` in Python); copy anything you cite into your report first. /tmp only for files under 50 MB; a /tmp path is never evidence. One clone per seat at most (`git clone --shared`/`--no-local` or `git archive`), never a full mirror. Check `{F}/scripts/hyaku/disk-guard.sh status` before a heavy run; on ENOSPC report the free space and stop. Never write an unbounded stream to a file.
- Never mutate the fleet repo, sibling lanes, the lane's jj state or git index: no git add/commit/stash/checkout/reset/pull/push in {L} or {F}, no mutating jj command. Read-only git (log/show/diff/rev-parse/ls-files/grep/archive/clone FROM the lane) is fine. Any fixture repo: D=$(mktemp -d -p {X}/<seat>) && git -C "$D" init -q (or a clone into your scratch), name -C "$D" on every later call, and verify `git -C "$D" rev-parse --show-toplevel` equals $D before the first commit; never commit under a throwaway identity anywhere else. Never write into ~/.local/bin or any PATH directory.
- The tools' cwd is the fleet root: cd into your scratch dir before running anything that writes relative paths. Some frozen round-38..49 instruments hardcode the lane path: run them only from an archive or clone in your scratch, and report any file they create inside {L}.
- /home/vgpnk/Projects/shokuknow is read-only: read bytes, run nothing there.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): ALL pacman transactions are PAUSED host-wide — never run pacman (no -S, -Sy, -Syu, -U, -R); install via uv tool/npx/an official binary in ~/.local/bin, or report the need; before any future pacman -S the dry-run rule applies (`pacman -Sp --print-format '%n %v' <pkgs>`, proceed only if none is installed).
- Host reads are read-only (detection and report only). Never write a sysctl, never trigger an OOM or a large allocation, never change a cgroup limit, swap or watermark, never run systemctl/journalctl --vacuum/--rotate or any config change. Reading /proc/meminfo, /proc/sys/vm/*, /proc/zoneinfo and /proc/vmstat is allowed. Never grep kernel log MESSAGE text for kill records (lane rule, QUALITY 15).
- No credential material, session or private URLs in any report; write a machine id as MACHINE_ID.
- Leaf seat: no subagents, except an executor may spawn one read-only labrat probe. Do not ask questions. Report observed evidence only (command + output + exit code); say UNVERIFIED where you could not check. A dispatched seat is not an independent judge. End your report with a section `## Findings` listing each finding with a severity (HIGH/MED/LOW) and the file or line it concerns.
"""

items = []


def add(name, role, text):
    n = P + name
    items.append({"name": n, "role": role, "prompt": f"{GODSPEED}\n\n{n}: {text} Scratch: {X}/{n}/."})


ENTAIL_RULE = (f"Method per row: find the quote in the committed copy under {SRC}/ (give the line number), read about "
               f"20 lines around it, and judge whether the CLAIM cell follows from the quote plus that context. Then write, "
               f"on its own unfenced line in your report, exactly `ENTAIL <hash> entailed` or `ENTAIL <hash> overclaim — "
               f"<the exact words that go beyond the source>` (hashes: {HASHES}; recompute one with `{HASH1}` and check it "
               f"matches). Only for an overclaim: propose a replacement claim cell (>= 6 words, >= 3 words of 3+ letters "
               f"not in the quote) on its own line as `REPLACE <oldhash> :: <replacement text>`; do NOT vote on your own "
               f"replacement (the counter ignores an author's vote; two other voters must judge it). Exactly one verdict "
               f"line per row you were given; no ENTAIL line for any other row; never put ENTAIL or REPLACE lines inside a "
               f"fenced block. Be strict: a claim that adds a consequence, a number or a scope the source does not state "
               f"is an overclaim.")
BLOCKS = [(1, 7), (8, 14), (15, 21), (22, 28)]
vroles = ["reviewer", "critic", "reviewer", "critic", "reviewer", "critic",
          "reviewer", "critic", "reviewer", "critic", "reviewer", "critic"]
for i in range(12):
    a, b = BLOCKS[i // 3]
    add("Ent%02d" % (i + 1), vroles[i],
        f"ENTAILMENT item. Judge claim rows {a}-{b} of the `## Claims` table of {L}/{ENTRY} at {T} "
        f"(`git -C {L} show {T}:{ENTRY}`). {ENTAIL_RULE} Also say, for each row, which part of the source a careless "
        f"reader might over-read.")

# ---------- C2: sources, entry prose, counter ----------
add("ExecSourceRefetch", "executor",
    f"Re-fetch the five source URLs of S497-S501 live (`curl -fsSL`, URLs in the COPIES table of {C2}) and report HTTP status, byte count and sha256 against the frozen copies in {SRC}/; for each of the 28 quotes of {L}/{ENTRY} report whether it still occurs (whitespace collapsed) in the live bytes. Also confirm tag v7.2 resolves (`git ls-remote https://github.com/torvalds/linux refs/tags/v7.2`).")
add("ExecAnchorCheck", "executor",
    f"Check the `anchor` cells of rows S497-S501 in {L}/corpus/SOURCES.md at {T}: for every line range they name, print those lines from the copy in {SRC}/ and say whether they hold what the row's scope and teaches cells say. Also check each row parses as 11 cells (0-3 leading spaces) and its `used-by` names {ENTRY}. Propose exact replacement anchor text for any drift.")
add("ExecProseLines", "executor",
    f"Verify every `file:line` reference in the prose, reading-rules table and Boundaries of {L}/{ENTRY} at {T} (e.g. `meminfo.c:125-126` in the round-51 copy {L}/corpus/evidence/sources-r51/meminfo.c.v7.2, `util.c.v7.2:937-940`, `:969-977`, `:994`) by printing the named lines with `sed -n`. Report each reference: holds / drifted (correct line) / wrong.")
add("ExecHostCommit", "executor",
    f"Read-only host check of the entry's formula: read /proc/sys/vm/overcommit_memory, overcommit_ratio, overcommit_kbytes, user_reserve_kbytes, admin_reserve_kbytes and the MemTotal, SwapTotal, Hugetlb, HugePages_Total, Hugepagesize, CommitLimit, Committed_AS lines of /proc/meminfo (twice, 5 s apart). Compute vm_commit_limit() by the v7.2 formula ({SRC}/util.c.v7.2:904-916) and compare with the printed CommitLimit (difference in kB and in pages). Say whether Committed_AS exceeds CommitLimit here and which mode is active. Paste the raw reads. This is own-work evidence; it is not claimed in the entry.")
add("ExecBatchDeviation", "executor",
    f"The entry says the mode-2 test uses an approximate per-CPU read. Size the error: fetch https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/mm_init.c into your scratch (sha256 it), find mm_compute_batch() and the vm_committed_as_batch rule, and compute on this host (nproc, MemTotal) the batch under mode 0/1 and under mode 2 and the worst-case deviation (batch x nr_cpus pages, in MiB). Quote the lines you use (<= 25 words each) with line numbers. Say whether this belongs in the entry's Boundaries and draft one sentence (fenced).")
add("ExecC2Replay", "executor",
    f"Run `python3 {C2} {T}`, `python3 {C2} --selftest` and `python3 {C2} --hashes {T}`; compare the hashes with {HASHES}. Then import the counter as a module (scratch copy) and score five in-memory variants of the entry built from `git show {T}:{ENTRY}`: drop one row; give one row a quote from the wrong copy; a REPLACE line by voter A plus votes from A and one other voter on that row; two votes from non-voter seats; votes inside a fenced block. Report each verdict line.")
add("MutC2Arm", "mutation-tester",
    f"Mutation-test the hardened entailment arm of the frozen counter {C2} in scratch copies: >= 10 single-point mutations (MIN_VOTES 2->1; drop the fence toggle; accept any `.md` under w1/; drop the VOTERS filter; drop the authorship subtraction; count overclaim only from voters vs from anyone; REPLACE regex that also matches inside a line; hash without whitespace folding; accept uppercase hex; entailed>=claims instead of ==). Run `--selftest` on each; killed iff it exits nonzero. Table: mutation -> killed/survived -> killing arm; arm text to add for each survivor (a routed limit).")
add("MutC2Entry", "mutation-tester",
    f"Mutation-test the entry-level arms of {C2} (copied from round 51, `{R51}/count-c2.py`): >= 8 single-point mutations (opened date, used-by, unique quote, sources floor, word bounds, words-beyond floor, pins, row status). Run `--selftest`; killed iff nonzero. Table and arm text for survivors.")
add("RevC2Counter", "reviewer",
    f"Review {C2} line by line, focusing on what changed from {R51}/count-c2.py (`diff` them): entail_votes() (VOTERS filter, fence handling, REPLACE parsing, authorship set), the per-row MIN_VOTES rule, the docstring predicate vs the code (same sentence?), and the selftest arms that guard each new rule. Defects with line numbers and severity; limits, not edits.")
add("CritC2Voters", "critic",
    f"Attack the voter design of P-C2 ({W}/contract.md, {C2}): can a row reach `entailed` without two independent judgments (one seat writing two files? a voter quoting another voter's line? an author evading the REPLACE signal by proposing text in prose? a dissent cleared by a REPLACE whose new text equals the old after whitespace folding?). Build the cheapest junk in scratch and score it with the counter as a module. Report each class: reaches met / blocked, with the code line.")
add("CritC2Prose", "critic",
    f"Attack the PROSE of {L}/{ENTRY} at {T} (intro, `## Reading rules (mori)` table, `## Boundaries`) — not the claim rows: every sentence that says more than the five copies in {SRC}/ (and the round-51 meminfo copy) support, or that a mori operator could misread as advice to change a sysctl. Quote the sentence, the source line it needs, and a fenced replacement.")
add("CritC2Coverage", "critic",
    f"Attack the expansion claim behind C2: is overcommit accounting really new ground for mori (sweep {W}/evidence/sweep-overcommit.txt)? Grep the whole lane at {T} (`git -C {L} grep -n -i -E 'overcommit|commitlimit|committed_as|enomem'`) and the sibling lanes' corpus/ and SKILL.md under {F}/*-shokunin (read-only, skip .scratch/.ufo) for the same terms. Is it in mori's PROVINCE ({L}/PROVINCE.md) — resource runway — or another lane's? Verdict with pointers.")
add("RevSourcesRows", "reviewer",
    f"Review rows S497-S501 of {L}/corpus/SOURCES.md at {T} against the registry contract in {F}/CORPUS.md (section `SOURCES.md — where a shokunin learns`): kind, tier, scope, anchor, teaches (one sentence a reader can act on?), status mined, opened 2026-10-26, recheck `on-release`, used-by. Also run `{F}/scripts/sources-census.sh validate --root {F} mori` and compare with {W}/evidence/census-start.txt (W04 count). Defects with severity.")
add("ConnSiblings", "connector",
    f"Sibling-overlap scan for C2: `grep -rliE 'overcommit|CommitLimit|Committed_AS|overcommit_memory|user_reserve_kbytes' {F}/*-shokunin/corpus {F}/*-shokunin/SKILL.md {F}/*-shokunin/PROVINCE.md` (skip .scratch and .ufo/waves; paste the command). For each hit: owning lane, whether mori's entry duplicates or contradicts it, and contested scope (tsukuroi owns host OS-state triage). Then check {L}/{ENTRY} Boundaries wording against {F}/tsukuroi-shokunin/PROVINCE.md:8-14,28.")
add("SentBoundary", "sentinel",
    f"Adjacency and safety review of the round's data at {T}: `git -C {L} diff {E} {T}`. Flag any text that instructs a reader to write a sysctl, trigger allocations, change swap or cgroup limits, or that claims ownership of host configuration; any command in the entry or the appended QUALITY/README text that writes; any new absolute host path in committed executable code (`git -C {L} grep -n '/home/vgpnk' {T} -- .ufo/waves/round-52/`). Verdict per finding.")

# ---------- C1: counter, controls, scope ----------
add("ExecC1Replay", "executor",
    f"Independent run: `python3 {C1} {T} --scratch {X}/{P}ExecC1Replay/c1` (about 20 s; heavy CPU) and `python3 {C1} --selftest`; paste every non-ok `item` line and the verdict line with exit code; compare with {W}/evidence/c1-at-data.txt. Then re-run the do-nothing control `python3 {C1} {E} --scratch {X}/{P}ExecC1Replay/c0` and compare with {W}/evidence/control-c1-do-nothing.txt.")
add("ExecC1Controls", "executor",
    f"Replay the C1 controls independently: read {W}/controls/c1-controls.py and c1-data.py, then run `python3 {W}/controls/c1-controls.py {X}/{P}ExecC1Controls/ctl rewrite-in-place repeat-stale-tally witness` — NOTE it overwrites the receipts under {W}/evidence/: instead copy both control scripts into your scratch, edit only the receipt output directory in the copy to your scratch, and run the copy. Compare each verdict line with {W}/evidence/control-c1-*.txt. Report differences.")
add("ExecC1Unenumerated", "executor",
    f"Named-limit inventory for C1 arm (C): list every command-tally pin in {L}/corpus/QUALITY.md and {L}/corpus/README.md at {T} that the counter does NOT enumerate (span across lines, `<rev>`-style placeholders, tally outside backticks, `(N/M)` after a non-backticked command). For each: line, the text, and what the command prints today (run it in a `git archive` of {T} under your scratch with TMPDIR there; use a real revision for placeholders). Count how many would be mismatches if enumerated.")
add("ExecLogPinsHistory", "executor",
    f"Calibration history check (K4 scope decision in {W}/contract.md): LOG.md holds 10 command-tally pins (lines 2224, 2256, 2262, 2285, 2295, 2332, 2338, 2642 and two more — enumerate them with the counter's LPIN regex imported from {C1}). For each, find the round's landed commit (the `## Round N` heading above it and `git -C {L} log --format=%H -1 --grep='round-N'`), run the pinned command in a `git archive` of that commit under your scratch (supply the revision argument where needed), and report pinned vs observed. Were the dated records true when written?")
add("ExecScorecardPinsHistory", "executor",
    f"Same as the LOG history check but for the 9 command-tally pins in the round sections of {L}/SCORECARD.md (lines near 2209, 2210, 2238, 2239, 2300, 2593, 2620, 2621, 2651; enumerate with the LPIN regex of {C1}). For each, run the pinned command at the round's landed commit in a `git archive` under your scratch and report pinned vs observed, with the exact command and exit code.")
add("ExecLocatorSweep", "executor",
    f"Inventory for round 53: apply the counter's locator rules (import check_locators logic from {C1} into a scratch script) to EVERY backticked `path:N[-M]` locator in {L}/SCORECARD.md and {L}/LOG.md at {T} that follows a double-quoted string or a `proposed A → B` phrase (not just the Axes rows), resolving each at {T}. Report counts (total, in range, quote found, quote absent, file absent) and list the misses. Read-only.")
add("MutC1Arms", "mutation-tester",
    f"Mutation-test {C1} in scratch copies: >= 12 single-point mutations across all four arms (verdict whole-word -> substring; accept 2 `## Axes`; drop the Score arm; `admitted` -> startswith; drop the symlink/regular check; drop receipt check; drop pin_removed check; superseded() accepting the pin's own criterion; quotation skip without the same-line replacement rule; drop rc==0; locator quote check -> range only; lane_writes ignored). Run `--selftest`; killed iff nonzero. Table and arm text for survivors.")
add("MutC1Controls", "mutation-tester",
    f"Which control isolates which arm of {C1}? Read the control receipts {W}/evidence/control-c1-*.txt and the mutation list in your own design: for each arm (A axes, B shonen, C living, D locators) and each sub-rule, name the control whose verdict would change if that rule were removed, and the rules no control isolates (the round-51 closure routed this class: 7 of 9 single-arm mutants kept every control verdict). Demonstrate 3 by running mutated counter copies against the witness control commit rebuilt in scratch with {W}/controls/c1-data.py.")
add("RevC1Counter", "reviewer",
    f"Review {C1} line by line: the docstring predicate vs the code (same sentence?), axes_table() heading/fence logic, closure_scores() table parsing (does it pick the right column on every closure file in {L}/corpus/lessons/ at {T}? list what it returns per axis), living_pins()/superseded()/the quotation rule, the runner (archive, TMPDIR, timeout, ANY_TALLY fallback), lane_writes. Defects with line numbers and severity.")
add("CritC1Junk", "critic",
    f"Find the cheapest edit set that makes `python3 {C1} <rev>` print C1=met WITHOUT honest calibration work (e.g. a supersede line with a pin that prints the right tally but names an unrelated instrument; a quoted string chosen to match any line; a Score cell copied from a wrong closure; receipts written by hand). Build it in a `--no-local` clone under your scratch, commit there (fixture identity, verify toplevel), score it with `--repo <clone>`, and report each class: met / unmet.")
add("CritC1Scope", "critic",
    f"Attack the K4 scope decision in {W}/contract.md (LOG.md and SCORECARD round sections are dated records and not run; QUALITY.md and README.md are living). Is that line honest and consistent with the round-50 closure's routed defect 3 (`{L}/corpus/lessons/round-50-verifier-spotcheck.md` §5)? Find any current-tense self-claim with a tally outside the two living files and SHONEN (SKILL.md is checked by tools/mori-pin-check.py — confirm), and any living pin that is in fact a dated record. Verdict with pointers.")
add("CritContractFreeze", "critic",
    f"Attack {W}/contract.md against {C1}, {C2} and the receipts in {W}/evidence/: is every predicate sentence the same condition as the counter's code and the receipt label; do the before-values equal the receipts; do the controls really skip the claimed work; are the claims causally separable (run each counter with the other claim's data reverted in a scratch clone); are the named limits honest? Check `{W}/evidence/freeze-sha256.txt` against the bytes at {FZ}. Quote contract line and code line for every discrepancy.")
add("LabLaneWrites", "labrat",
    f"Hypothesis: C1's `lane_writes` guard catches a pinned command that writes into the measured repo. Falsify it: in a `--no-local` clone of the lane at {T} under your scratch, add a fixture QUALITY.md pin whose command writes (a) an untracked file in the clone root, (b) an ignored path (e.g. `__pycache__`), (c) a file under `.git/`, (d) a file under the clone's `.ufo/waves/round-38/scratch` — commit in the clone (fixture identity, verify toplevel) and run `python3 {C1} <clonecommit> --repo <clone> --scratch {X}/{P}LabLaneWrites/c1`. Report which writes are caught. NOTE: the counter runs commands in an archive, not in the repo: say whether (a)-(d) can reach the repo at all.")
add("RevQualityRows", "reviewer",
    f"Review the appended QUALITY.md criteria 141-142 and the README `## Round-52 corrections` block at {T} (`git -C {L} diff {E} {T} -- corpus/QUALITY.md corpus/README.md`): are the factual statements true (e.g. 'the committed tool has printed 22 since the round-41 freeze d72ac167' — check with `git -C {L} log` and by running the tool at d72ac167 and its parent in archives under your scratch), are the criteria in the house style (cite lesson, Check, Shown able to fail, Not covered), do they duplicate an existing criterion (grep 123-140)?")
add("RevenStalePins", "revenger",
    f"Reverse-engineer when each stale living pin went stale: for `QUALITY.md:909` / `README.md:608` (`mori-sources-appendonly.py --selftest` -> pass=12) find with `git -C {L} log -S` the commit that grew the tool's selftest past 12 and every later tally (15, 22), and for `README.md:607` (bare `--selftest` -> pass=9) find the round-39 command it meant. Was any round's QUALITY/README edit an in-place rewrite of a pin (search `git log -p` for changed pin lines)? Timeline with hashes.")

# ---------- routed defects and considerthese ----------
add("ExecR51C1Rerun", "executor",
    f"considerthese/2026-10-26.md suggestion 3 (re-execute what closures only evidence-verified): the round-51 closure did not run `{R51}/count-c1.py`. Run it at the measured revision: `python3 {R51}/count-c1.py 70e68cdd28c44a95039b9175a947e15664618351 --scratch {X}/{P}ExecR51C1Rerun/s` (minutes; run in the background, read the file; it needs bubblewrap). Compare with {R51}/evidence/c1-at-landed.txt field by field. Report agreement or the exact divergence.")
add("ExecR51C2Rerun", "executor",
    f"Same as considerthese suggestion 3 for C2: run `python3 {R51}/count-c2.py 70e68cdd28c44a95039b9175a947e15664618351` and `--selftest`, compare with {R51}/evidence/c2-at-landed.txt and selftest-c2.txt, and also at the lane tip {T}. Report agreement or divergence.")
add("ExecR51ArmControls", "executor",
    f"Round-51 closure routed defect 3: 7 of 9 single-arm mutants of `{R51}/count-c1.py` kept every control verdict ({L}/corpus/lessons/round-51.md `## Wave w1 — integrated findings`). The counter is frozen; design (do not apply) one control per arm A-D that a single-arm mutant would flip, state the control's construction, and demonstrate two of them in scratch. Output: a table arm -> control -> expected verdict under the intact and mutated counter.")
add("ExecWritersConform", "executor",
    f"Round-51 closure routed defect 8 (read-only inventory): for `.ufo/waves/round-38/conform.py`, `round-39/conform.py`, `round-41/conform.py`, `round-42/conform.py` under {L}, list every path each writes or reads under the hardcoded LANE (grep LANE/SCRATCH_ROOT/mkdtemp/open(..., 'w')), and run each `--selftest` form named in SKILL.md (find with `git -C {L} grep -n 'conform.py' {T} -- SKILL.md`) from a `git archive` of {T} under your scratch; record `git -C {L} status --porcelain --ignored` before and after. Report: writes into the lane yes/no per instrument, with the paths.")
add("ExecWritersCounters", "executor",
    f"Same inventory for `.ufo/waves/round-48/count-c1.py` and `round-49/count-c1.py` (each defaults `--scratch` to `<repo>/.scratch`): run each `--selftest` and one default run from a `git archive`/clone of {T} under your scratch, and record lane status before/after. Then draft (fenced) the successor-freeze design the round-51 closure routed defect 6 allows: copy-on-change successors under `.ufo/waves/round-53/` vs in-place edits with a recorded successor freeze — which keeps SKILL.md pins valid with fewer moving parts?")
add("RevenRound40Conform", "revenger",
    f"Round-51 closure D-e: `.ufo/waves/round-40/conform.py` was edited in place (round 51) so it no longer matches `{L}/.ufo/waves/round-40/evidence/freeze-r40.txt` (5025b966… -> 7f5174d5…). Reconstruct: the diff between the frozen bytes and the current bytes (`git -C {L} log --format=%H -- .ufo/waves/round-40/conform.py`), which receipts were measured with which bytes, and whether any SKILL.md pin or QUALITY row now names a tally only the edited bytes print. Draft (fenced) the successor-freeze record text.")
add("ScribeErratum51", "scribe",
    f"Draft `corpus/lessons/round-51-erratum.md` (fenced, append-only erratum; read {L}/corpus/lessons/round-39-erratum.md for the house shape) fixing the round-51 closure's D-c and D-d ({L}/corpus/lessons/round-51-verifier-spotcheck.md §1): (1) re-derive every S493 locator the round-51 lesson's `### Spot-check` cites with `grep -n` on {L}/corpus/evidence/sources-r51/show_mem.c.v7.2 (paste the commands and outputs) and give old -> new; (2) correct the famzah attribution (the 2017 comment is the blog author's reply; `MemAvailable` occurs 0 times case-sensitively — verify by fetching https://blog.famzah.net/2014/09/22/know-your-linux-memory-usage/ into scratch). Never rewrite the filed lesson.")

# ---------- frontier drafting ----------
add("ScribeGate", "scribe",
    f"Draft the lesson's `## Gate` block for rows S497-S501 (fenced; house shape: read `## Gate` in {L}/corpus/lessons/round-51.md): for each row the URL, access date 2026-10-26, sha256 of the copy, and one located quote of <= 25 words that you verify yourself with a substring test on the copy in {SRC}/ (paste the test). Add one admit and one reject decision: the reject candidate is https://www.kernel.org/doc/html/latest/mm/overcommit-accounting.html (rendered `latest`, not pinned to v7.2) — fetch it and record why a pinned tag copy is preferred, with its flip condition.")
add("ScribeSkill", "scribe",
    f"Draft SKILL.md `## Round52` (fenced; house shape: read `## Round51` at the end of {L}/SKILL.md): a decision row for reading CommitLimit/Committed_AS by mode (from {L}/{ENTRY} Reading rules), the refusal log line as a detection signal (rate-limited, not a count), and the living-pin rule for QUALITY/README (supersede, never rewrite; counter arm C). Every row cites the entry or the counter. No sysctl advice.")
add("ScribeReadme", "scribe",
    f"Draft the corpus/README.md additions (fenced): a `## Round-52 coverage additions` block in the house shape of the round-51 block at the end of {L}/corpus/README.md — one coverage-map row for the overcommit entry (resource runway, new ground; sweep {W}/evidence/sweep-overcommit.txt), and a dated superseding note for the frontier (FR8 alert-threshold calibration stays open: no Committed_AS/CommitLimit threshold is proposed). Never rewrite a Frontier row.")
add("ScribeQuality", "scribe",
    f"Draft QUALITY.md criterion 143 onward (fenced; read the last 60 lines of {L}/corpus/QUALITY.md for numbering and the house style: Lesson, Check, Shown able to fail, Not covered): (a) a depth row needs two `entailed` votes from voters that did not write its text (P-C2 arm; selftest arms entail_one_voter_unmet, entail_author_vote_not_counted_unmet in {W}/evidence/selftest-c2.txt); (b) a runway reading of CommitLimit is mode-dependent: under modes 0/1 it is printed, not enforced. Cite the counter and the entry.")
add("ScribeMistakes", "scribe",
    f"Draft the lesson's `## Mistakes` section (fenced; class · evidence pointer · captured-by · fix; a fix counts only once shown able to fail): M1 a living check pinned at one round's tally and never superseded (QUALITY 112 / README round-39 rows; captured-by: none until C1 arm C; fix shown able to fail: {W}/evidence/control-c1-do-nothing.txt vs control-c1-witness.txt); M2 the round-51 lesson's locator drift (closure D-c; captured-by: none — propose the check); M3 the self-assessment lagging the fleet record by one round (Axes cells, round 51; captured-by: C1 arm A); M4 a frozen file edited in place (D-e). Read {L}/corpus/lessons/round-51.md `## Mistakes` for the shape.")
add("ScribeLog", "scribe",
    f"Draft the LOG.md `## Round 52` entry (fenced; append-only; read the round-51 entry at the end of {L}/LOG.md for the shape): entering tip, freeze {FZ}, data {T}, the two claims with their before receipts and counting commands, assimilation none, the considerthese item, the mistakes, the round-51 closure routed defects 1-8 with each disposition (contract `## Round-51 closure routed defects`), every deviation from the contract marked `[L1 fills]`. Claim nothing landed beyond the data commit.")
add("ScribeScorecard", "scribe",
    f"Draft the SCORECARD.md `## Round 52` section (fenced; house shape: the round-51 section at the end of {L}/SCORECARD.md): claim table (claim, axis held, counting command, before, after `[L1 fills]`), controls line, limits, and a `Planned (round 53)` paragraph (the in-lane writers successor freeze; the locator sweep beyond the Axes rows; the counter limits the wave finds).")
add("ScribeShonen", "scribe",
    f"Draft the SHONEN.md box updates (fenced, one line per box; read {L}/SHONEN.md): each box keeps its pointers and leads with the round-52 evidence (SKILL `## Round52` section, LOG round 52 entry, the two tally pins with their round-52 receipts under {W}/evidence/selftests/, the overcommit entry Boundaries). Tally pins must stay in the exact form `python3 <path> --selftest` (N/N) — read the counter {C1} arm (B) and the receipts to get N.")

# ---------- sweeps, connectors, scouts, no-harm ----------
add("ScoutMistakeSweep", "scout",
    f"Mistake sweep for the frontier step: read {L}/corpus/lessons/round-47-verifier-spotcheck.md through round-51-verifier-spotcheck.md; list every disagreement or routed defect, and for each whether a QUALITY.md criterion, lesson fix, erratum or tool now captures it (grep {L}/corpus/QUALITY.md and lessons) — CAPTURED (pointer) / OPEN. Paste the grep commands.")
add("ScoutRunwaySurfaces", "scout",
    f"Per-surface reconnaissance for resource runway: list every lane instrument and knowledge entry at {T} that reads /proc/meminfo, /proc/sys/vm or /proc/pressure (`git -C {L} grep -n -E 'meminfo|/proc/sys/vm|pressure/memory|MemAvailable|CommitLimit' {T} -- tools corpus/knowledge SKILL.md`), what each reads and prints, and which runway question each answers (memory left before swap, allocation refusal, stall time). Name the gaps after this round's entry.")
add("ConnCrossClaim", "connector",
    f"Cross-claim and cross-round pattern: C1's living-pin rule (supersede, never rewrite) and C2's authorship rule (a voter never judges text it wrote) — read {W}/contract.md, {C1} and {C2}. Find the shared principle and the QUALITY rows that already state part of it (grep {L}/corpus/QUALITY.md 100-142), and any place in the lane where the same mistake class is still open (an instrument that grades its own output; a document that rewrites its own pin). Table with pointers.")
add("ExecMisrootSweep", "executor",
    f"Misroot pre-sweep (read-only): `git -C {F} status --porcelain` (no pathspec) and list every untracked file at the fleet root or under {F}/.ufo that could belong to mori round 52 (content names mori, round 52, Mo52 or this lane's paths). Never touch .ufo/state/, .scratch/ or other lanes' files. Output: path, evidence it is mori's, the `cmp` command to copy it into {L}. Also `git -C {L} status --porcelain --ignored` for stray files outside `.ufo/waves/round-52/` (the lane root holds tracked stray files `0`, `base.c`, `main.c`, `meminfo.c`, `oom_kill.c`, `sd-main.c`, `user@.service.in` — find the commits that added them with `git -C {L} log --format='%h %s' -- <file>` and say whether they are seat misroots).")
add("ExecCensusCounts", "executor",
    f"Frontier-step census before -> after: count Registry rows by status and tier at {E} and {T} (`git -C {L} show <rev>:corpus/SOURCES.md`, an awk accepting 0-3 leading spaces), and run `{F}/scripts/sources-census.sh validate --root {F} mori` (rc, W04 count; compare with {W}/evidence/census-start.txt). Paste commands, outputs, exit codes, and the delta (expect +5 rows S497-S501, tier A, mined).")
add("ExecPinCheckNoHarm", "executor",
    f"Operability no-harm check: run `python3 {L}/tools/mori-pin-check.py --rev {T} --repo {L} --scratch {X}/{P}ExecPinCheckNoHarm/pc` (read `--help` first; minutes) and `python3 {L}/tools/mori-unlanded-check.py --repo {L} --round 52`; compare the pin verdict with the round-51 landed receipt {R51}/evidence/c1-at-landed.txt (`PIN_CHECK=met tally_pins=36 …`). Any pin that changed state since round 51 is a finding.")
add("SentHostPaths", "sentinel",
    f"Portability audit (round prompt §7 item 4; QUALITY 127) of the round-52 files at {T}: `git -C {L} grep -n '/home/vgpnk' {T} -- .ufo/waves/round-52/`; `git -C {L} grep -nE 'mkdtemp\\(dir=\"/tmp|/tmp/' {T} -- .ufo/waves/round-52/`. Classify each hit: executable default that breaks off-host replay / honours TMPDIR / prose only. Are count-c1.py, count-c2.py, controls/c1-controls.py, controls/c1-data.py portable?")
add("SentReceipts", "sentinel",
    f"Receipt integrity (round-51 closure routed defect 7: literal commands): for every file under {W}/evidence/ at {T}, check that it records the literal command it ran (no `<scratch>`-style placeholder without a stated rule), its exit code, and that re-running the command reproduces the verdict line (run the cheap ones; for count-c1 runs use your scratch). List each receipt: literal yes/no, reproduced yes/no/not run.")
add("SimpCounters", "simplifier",
    f"Dead weight in {C1}, {C2}, {W}/controls/c1-controls.py and {W}/controls/c1-data.py: unused imports/variables/constants (e.g. the `ws` helper, LIVING, HIDDEN reuse), duplicated helpers shared with the round-50/51 counters, dead branches. Prove each deletion on scratch copies (selftest tallies unchanged; a real run gives identical output). The counters are frozen: these are proposals for the successor.")
add("RevNoHarm", "reviewer",
    f"No-harm audit across all six axes: `git -C {L} diff --stat {E} {T}` and read every changed tracked file. For coverage, operability, depth, freshness, calibration, adjacency: name anything the round's changes could have harmed (a removed row, a broken pointer, a stale pin introduced, a changed instrument verdict, a scope crossed into a sibling, a recheck weakened) and check it. Verdict per axis: harmed / not harmed, with evidence.")
add("RevAxesCells", "reviewer",
    f"Review the two edited SCORECARD `## Axes` cells (operability, depth) and the freshness locator fix at {T} (`git -C {L} diff {E} {T} -- SCORECARD.md`): do they say what {L}/corpus/lessons/round-51-verifier-spotcheck.md:126-135 and the fleet MANIFEST ({F}/MANIFEST.json, mori round 51) say; is 'states the score 7/5' accurate for that closure (it grades and holds); does every other cell still resolve?")


def main():
    spec = {"wave": "mori-r52-w1", "reportDir": ".ufo/waves/round-52/w1", "context": context, "items": items}
    with open(os.path.join(W, "w1-spec.json"), "w") as f:
        json.dump(spec, f, indent=1)
    roles = {}
    for it in items:
        roles[it["role"]] = roles.get(it["role"], 0) + 1
    flash = sum(v for k, v in roles.items() if k in ("executor", "labrat", "scribe", "sonic", "sentinel",
                                                      "simplifier", "revenger"))
    attack = sum(v for k, v in roles.items() if k in ("reviewer", "critic", "mutation-tester", "labrat"))
    print(len(items), roles, "flash=%d attack=%d" % (flash, attack))


if __name__ == "__main__":
    main()
