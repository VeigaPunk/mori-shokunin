#!/usr/bin/env python3
"""Build the round-54 wave w1 spec (L1 MoriR54; one v2 wave after the data commit: the C1 RECHECK votes, the C2
ENTAILMENT votes, attacks on both counters, both claims and the new entry, independent source re-fetching, the
host read, frontier drafting, the considerthese item and routed-defect checks). Usage: build-w1-spec.py <freeze> <data>.
Paths derive from this file's location."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
L = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))  # lane repo
F = os.path.dirname(L)  # fleet root
W = HERE
E = "39dcf4d7e410d362781a47e8365ca23b5c807598"  # entering tip
FZ = sys.argv[1]
T = sys.argv[2]
C1 = W + "/count-c1.py"
C2 = W + "/count-c2.py"
SRC = L + "/corpus/evidence/sources-r54"
SRC53 = L + "/corpus/evidence/sources-r53"
LEDGER = "corpus/knowledge/kernel-v7.3-recheck-r54.md"
ENTRY = "corpus/knowledge/memory-failure-kills-r54.md"
C1CL = W + "/evidence/c1-claims.txt"
C2CL = W + "/evidence/c2-claims.txt"
X = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku") + "/mori-r54"
P = "Mo54"
CG = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/"
with open(os.path.expanduser("~/.agents/skills/godspeed/directive.md")) as f:
    GODSPEED = "/skill:godspeed\n" + f.read().rstrip("\n")

context = f"""# mori round 54 — wave w1 (one v2 wave: RECHECK and ENTAILMENT votes, attacks on both claims, frontier drafting)
Lane: mori-shokunin (森, fleet and host observability: fleet liveness, wave settlement, kill and OOM events, resource runway; detection and report only). Lane repo: {L}. Fleet root: {F}.
The L1 (MoriR54) froze two claims at {FZ} ({W}/contract.md — read it first; entering tip {E}) and landed the data at {T}:
- C1 freshness: every remaining claim row of the lane that pins Linux v7.2 (31 rows: oom-memcg-stat-r50 22, commit-runway-read-r53 8, quota-observability-r48 1) re-verified at v7.3. Ledger {L}/{LEDGER} (one row per claim hash: derived status held/absent, a v7.3 source row S515-S520 or S508/S514, the v7.3 LINE where the quote begins, the quote, a disposition holds/changed). v7.3 copies under {SRC}/ (and {SRC53}/util.c.v7.3, mm_init.c.v7.3). `python3 {C1} {T}` -> `… line_ok=31 quote_ok=31 … voted=0 … failed=votes` ({W}/evidence/c1-at-data.txt). P-C1 requires, per row, the row's disposition as the FINAL unfenced `RECHECK <hash> holds|changed` line of at least TWO of the twelve RECHECK seats Mo54Rc01-Mo54Rc12, no RECHECK seat's final line with the other word, and each voter listed in the orchestrator's w1-results.json. Claim text, v7.2 and v7.3 locations per row: {C1CL}.
- C2 depth: new entry {L}/{ENTRY} — hardware memory-failure kills at Linux v7.3 (SIGBUS/SIGKILL from mm/memory-failure.c, the recovery-action line, the per-node memory_failure counters, HardwareCorrupted, the early/late kill and recovery sysctls, v7.3's panic_on_unrecoverable_memory_failure, the ras:memory_failure_event tracepoint): 21 claim|source|quote rows over six copies (S521 memory-failure.c, S522 hwpoison.rst, S523 sysfs-devices-node, S524 trace/events/memory-failure.h under {SRC}/; S507 vm.rst, S502 proc.rst under {SRC53}/). `python3 {C2} {T}` -> `claims=21 located=21 … entailed=0 … failed=entailment` ({W}/evidence/c2-at-data.txt). P-C2 requires, per row, an unfenced `ENTAIL <hash> entailed` line from at least TWO of the twelve ENTAILMENT seats Mo54En01-Mo54En12 (listed in w1-results.json), none of them writing `ENTAIL <hash> overclaim`. Rows per hash: {C2CL}.
The counters, predicates, controls and kill rules are FROZEN: never propose a change to them as a fix for this round; a counter weakness you find is a named limit for the report and a routed item for round 55. Data (ledger dispositions and prose, entry wording, SOURCES rows) may still be corrected by the L1 if you show it is wrong.
Vote lines (read even if your item is not a vote item): the C1 counter reads unfenced lines starting (after spaces) with `RECHECK <12 hex> holds|changed` or `QUOTE <12 hex> :: <text>` ONLY in {W}/w1/Mo54Rc01.md … Mo54Rc12.md; the C2 counter reads `ENTAIL <12 hex> entailed|overclaim` and `REPLACE <12 hex> :: <text>` ONLY in {W}/w1/Mo54En01.md … Mo54En12.md. Every other seat must never start a line with RECHECK, QUOTE, ENTAIL or REPLACE (quote such text inside a sentence if needed).
Rules for every seat:
- Paths: every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Use absolute paths for every read and write. Write ONLY your own report file. Drafts go INSIDE your report as fenced blocks; never edit SKILL.md, SHONEN.md, SCORECARD.md, LOG.md, PROVINCE.md, corpus/, tools/, considerthese/, or any file under {W} except your own report. The L1 integrates.
- Scratch (operator directive 2026-10-25): every clone, work tree, fixture and temp file lives under {X}/<your seat name>/ — `mkdir -p` it, `export TMPDIR={X}/<your seat name>/tmp`, and remove it before you finish (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree` in Python); copy anything you cite into your report first. /tmp only for files under 50 MB; a /tmp path is never evidence. One clone per seat at most (`git clone --shared` or `git archive`), never a full mirror. Check `{F}/scripts/hyaku/disk-guard.sh status` before a heavy run; on ENOSPC report the free space and stop.
- Never mutate the fleet repo, sibling lanes, the lane's jj state or git index: no git add/commit/stash/checkout/reset/pull/push in {L} or {F}, no mutating jj command. Read-only git (log/show/diff/rev-parse/ls-files/grep/archive/clone FROM the lane) is fine. Any fixture repo: D=$(mktemp -d -p {X}/<seat>) && git -C "$D" init -q (or a clone into your scratch), name -C "$D" on every later call, and verify `git -C "$D" rev-parse --show-toplevel` equals $D before the first commit; never commit under a throwaway identity anywhere else. Never write into ~/.local/bin or any PATH directory.
- The tools' cwd is the fleet root: cd into your scratch dir before running anything that writes relative paths.
- Network: use git.kernel.org cgit (`{CG}<path>?h=<tag>`) or a blob-filtered fetch into your scratch; raw.githubusercontent.com answered 429 and cdn.jsdelivr.net 403 for some paths on 2026-10-27. Keep fetches small and few.
- /home/vgpnk/Projects/shokuknow is read-only: read bytes, run nothing there.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): ALL pacman transactions are PAUSED host-wide — never run pacman (no -S, -Sy, -Syu, -U, -R); install via uv tool/npx/an official binary in ~/.local/bin, or report the need; before any future pacman -S the dry-run rule applies (`pacman -Sp --print-format '%n %v' <pkgs>`, proceed only if none is installed).
- Host reads are read-only (detection and report only). Never write a sysctl, never inject or unpoison memory (no madvise(MADV_HWPOISON), no hwpoison-inject, no /sys/devices/system/memory writes), never trigger an OOM or a large allocation, never change a cgroup, never run systemctl or any config change, never load a kernel module. Reading /proc/meminfo, /proc/sys/vm/*, /sys/devices/system/node/*/memory_failure/*, /proc/zoneinfo and /proc/vmstat is allowed. Never count kernel log lines by MESSAGE text (lane rule, QUALITY 15): a text match is attribution, not a count.
- No credential material, session or private URLs in any report; write a machine id as MACHINE_ID.
- Leaf seat: no subagents. Do not ask questions. Report observed evidence only (command + output + exit code); say UNVERIFIED where you could not check. A dispatched seat is not an independent judge. End your report with a section `## Findings` listing each finding with a severity (HIGH/MED/LOW) and the file or line it concerns.
"""

items = []


def add(name, role, text):
    n = P + name
    items.append({"name": n, "role": role, "prompt": f"{GODSPEED}\n\n{n}: {text} Scratch: {X}/{n}/."})


RECHECK_RULE = (
    f"Method per row: take the claim text, the v7.2 quote and both locations from {C1CL}; read the quote in the v7.2 "
    f"copy and at the ledger's line in the v7.3 copy; `diff -u` the enclosing function or documentation section "
    f"between the two copies; read about 30 lines of v7.3 context; judge whether the CLAIM, read against the v7.3 file, "
    f"is still true (the words being present is not enough: check the condition, caller, unit or default the claim "
    f"states). For the rendered cgroup-v2 rows, compare the 7.2 page copy (corpus/evidence/sources-r50/cgroup-v2.7.2.html) "
    f"with {SRC}/cgroup-v2.7.3.html as tag-stripped text. Also confirm the ledger's line number (the v7.3 copy line on "
    f"which the quote begins). Then write on its own unfenced line exactly `RECHECK <hash> holds` or "
    f"`RECHECK <hash> changed — <what changed, with the v7.3 line>`. If the ledger's quote no longer carries the claim "
    f"and a better v7.3 quote exists, propose it on its own line as `QUOTE <hash> :: <6-25 words located in the v7.3 "
    f"copy>` (your own vote does not count for a quote you propose). A later RECHECK line for the same hash replaces "
    f"your earlier one (last unfenced line wins). Exactly one RECHECK line per row you were given; none for other rows; "
    f"never inside a fenced block. Be strict: a renamed function, a moved check, a new condition or a changed default "
    f"the claim states is `changed`; a moved or reformatted line that keeps the rule is `holds`.")
C1_BLOCKS = [(1, 8), (9, 15), (16, 23), (24, 31)]
C1_DESC = ["the commit-runway band rows (percpu_counter.h, percpu_counter.c, mm_init.c, util.c)",
           "the rendered cgroup-v2 rows (memory.stat units and keys, memory.events oom_kill)",
           "the mm/memcontrol.c rows (memcg OOM report lines and the memory.stat reader)",
           "the mm/oom_kill.c rows and the EDQUOT row"]
for i in range(12):
    a, b = C1_BLOCKS[i // 3]
    add("Rc%02d" % (i + 1), "reviewer" if i % 2 == 0 else "critic",
        f"RECHECK item. Judge ledger rows {a}-{b} of {L}/{LEDGER} at {T} ({C1_DESC[i // 3]}; "
        f"`git -C {L} show {T}:{LEDGER}`; rows numbered in table order, the same numbering as {C1CL}). {RECHECK_RULE} "
        f"Also note, per row, anything in the v7.2→v7.3 diff a careless reader might miss.")

ENTAIL_RULE = (
    f"Method per row: read the claim and the quote ({C2CL}); open the copy the row's source names and read the quote "
    f"in context (at least the whole function or documentation section, plus every caller or definition the claim "
    f"relies on — grep the copy); decide whether the CLAIM is fully supported by the copy (the quote plus its context "
    f"in that same file), with no word that says more than the source. Then write on its own unfenced line exactly "
    f"`ENTAIL <hash> entailed` or `ENTAIL <hash> overclaim — <the word or clause the source does not support, and what "
    f"it does say, with line numbers>`. If you judge overclaim and can write a supported claim, add `REPLACE <hash> :: "
    f"<new claim text>` on its own line (your own entailed vote then does not count for that new text). One ENTAIL line "
    f"per row you were given; none for other rows; never inside a fenced block. Be strict: 'only', 'every', 'never', a "
    f"default, a unit, or a cause the source does not state is overclaim.")
C2_BLOCKS = [(1, 6), (7, 11), (12, 16), (17, 21)]
C2_DESC = ["the kill and signal rows from mm/memory-failure.c", "the recovery-action, counter-update and panic rows "
           "from mm/memory-failure.c", "the recovery-mode rows from hwpoison.rst and vm.rst",
           "the sysfs counter, tracepoint and meminfo rows"]
for i in range(12):
    a, b = C2_BLOCKS[i // 3]
    add("En%02d" % (i + 1), "reviewer" if i % 2 == 0 else "critic",
        f"ENTAILMENT item. Judge claim rows {a}-{b} of {L}/{ENTRY} at {T} ({C2_DESC[i // 3]}; rows numbered in table "
        f"order, the same numbering as {C2CL}). {ENTAIL_RULE}")

# ---------- C1: sources, ledger, counter ----------
add("ExecRefetchCgit", "executor",
    f"Re-fetch the C1 v7.3 copies from git.kernel.org cgit ({CG}<path>?h=v7.3 for mm/memcontrol.c, mm/oom_kill.c, lib/percpu_counter.c, include/linux/percpu_counter.h, include/uapi/asm-generic/errno.h, mm/util.c, mm/mm_init.c) and report HTTP status, bytes and sha256 against the frozen pins in {C1} (_COPIES) and {W}/evidence/freeze-sha256.txt. Also re-fetch the same paths at v7.2 and compare with the lane's committed v7.2 copies (corpus/evidence/sources-r50/, sources-r52/util.c.v7.2, sources-r53/*.v7.2, sources-r48/errno.h).")
add("ExecRefetchGit", "executor",
    f"Independent channel for the C1 and C2 pins: in your scratch `git init`, `git remote add origin https://github.com/torvalds/linux`, `git fetch --depth 1 --filter=blob:none origin tag v7.3` (never a full clone), then `git show v7.3:<path>` for every cgit path behind S515-S519 and S521-S524 (mm/memcontrol.c, mm/oom_kill.c, lib/percpu_counter.c, include/linux/percpu_counter.h, include/uapi/asm-generic/errno.h, mm/memory-failure.c, Documentation/mm/hwpoison.rst, Documentation/ABI/stable/sysfs-devices-node, include/trace/events/memory-failure.h) and `git rev-parse v7.3^{{commit}}`; compare each blob's sha256 with the copies in {SRC}/. Report per path: equal / differs.")
add("ExecRefetchDocs", "executor",
    f"The rendered cgroup-v2 page (S520): fetch https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html twice, a minute apart, and compare sha256 with {SRC}/cgroup-v2.7.3.html (pin in {C1}); fetch https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html and compare with corpus/evidence/sources-r50/cgroup-v2.7.2.html (S489). Also fetch the raw rst at cgit ?h=v7.3 (Documentation/admin-guide/cgroup-v2.rst) and check that each of the seven S489-derived quotes in {L}/{LEDGER} (rows 9-15) has a matching passage in the rst. Is the rendered page tag-pinned (footer `7.3.0`)?")
add("ExecLineArm", "executor",
    f"Independent line arm for C1: write your OWN locator (do not import {C1}): for each of the 31 ledger rows of {L}/{LEDGER} at {T}, find every line of the v7.3 copy on which the quote begins (whitespace-collapsed match; for the HTML copy, strip tags and decode entities first and map back to raw lines), and compare with the ledger's line cell. Then do the same against the v7.2 copies and check the table `## Where the quotes moved` in the ledger (every v7.2 line, v7.3 line and moved value). Report every disagreement.")
add("ExecC1Replay", "executor",
    f"Independent run: `python3 {C1} {T}`, `python3 {C1} --selftest`, `python3 {C1} --scope` (cd into your scratch first); compare with {W}/evidence/c1-at-data.txt, selftest-c1.txt and c1-scope.txt. Then re-run the do-nothing control `python3 {C1} {E}` and compare with control-c1-do-nothing.txt; and check that the scope equals your own enumeration: every claim|source|quote row in corpus/knowledge/*.md at {E} whose SOURCES row URL names Linux v7.2, minus the round-53 ledger's hashes.")
add("ExecControlsReplay", "executor",
    f"Replay all fourteen controls: copy {W}/controls/ into your scratch, edit ONLY your copy of controls.py so EVID points into your scratch (the original writes into {W}/evidence/ — never run it in place), keep it importing the frozen counters from {W}, and run it with HYAKU_SCRATCH={X}/{P}ExecControlsReplay. Compare every verdict line with {W}/evidence/control-*.txt (rev hashes will differ; fields must not). Report differences.")
add("MutC1", "mutation-tester",
    f"Mutation-test the frozen counter {C1} in scratch copies: >= 16 single-point mutations (MIN_VOTES 2->1; drop the fence toggle; last-wins -> first-wins; drop the results-file binding; accept any `name`-less result; drop the QUOTE authorship subtraction; status always held; quote check without `q == q72` for held rows; line arm accepts line±1; line arm skipped; norm_map HTML drops entity decoding; word bounds; scope read at R instead of ENTERING; r53-hash exclusion dropped; used-by check dropped; OPENED widened to any date; v7.2 URL accepted; pins check skipped; rows==len(d) dropped). Run `--selftest` on each; killed iff it exits nonzero. Table: mutation -> killed/survived -> killing check; arm text for each survivor (a routed limit).")
add("RevC1Counter", "reviewer",
    f"Review {C1} line by line: the docstring predicate vs the code (same sentence? every clause enforced?), scope() (exactly the 31 rows; the four URL forms; what if a SOURCES row cites v7.2 in a non-URL cell), norm_map()/lines_of() (offset mapping, HTML tokens, whitespace), final_votes() (results binding, fences, last-wins, QUOTE parsing), evaluate() (each arm, the failed list), and the selftest arms vs the arms. Defects with line numbers and severity.")
add("CritC1Junk", "critic",
    f"Find the cheapest edit set that makes `python3 {C1} <rev>` print C1=met WITHOUT an honest v7.3 recheck (a results file the L1 writes listing voter names; voter files written by a non-voter; votes copied wholesale; a line located in an unrelated part of the file; a disposition the votes support but the file contradicts). Build each in a `--shared` clone under your scratch, commit there (fixture identity, verify toplevel), score with `python3 {C1} <rev> --repo <clone>`, and report each class met / unmet with the code line that lets it through.")
add("CritC1Scope", "critic",
    f"Attack C1's scope and axis: D is every claim-table row pinning v7.2 (31 rows). List every other lane artefact at {T} that pins a kernel v7.2 (or older tag) byte with an on-release or release-triggered recheck (`git -C {L} grep -n -E 'recheck:.*(on-release|kernel release|release)' {T} -- corpus/knowledge`; SOURCES rows with a v7.2 anchor) and say which ones the round leaves unrechecked (oom-tracepoints-r47 catalogue, system-pressure-r24 anchors, disk-write-rate-r33, watchdog-identity-r31, oom-victim-selection-r27…). Is `freshness` the honest axis? Does the line arm add anything a do-nothing control could reach? Verdict with pointers.")
add("RevSourcesC1", "reviewer",
    f"Review rows S515-S520 and the used-by changes of S508 and S514 in {L}/corpus/SOURCES.md at {T} against the registry contract in {F}/CORPUS.md (section `SOURCES.md — where a shokunin learns`): kind, tier, scope, anchor (the `quote lines` list vs the ledger's line cells; sha256 prefix vs the copy), teaches, status mined, opened 2026-10-27, recheck, used-by. Run `{F}/scripts/sources-census.sh validate --root {F} mori` and compare with {W}/evidence/census-start.txt. Defects with severity.")
add("RevLedgerProse", "reviewer",
    f"Review the prose of {L}/{LEDGER} at {T} (header lines, `## What this ledger is`, `## Where the quotes moved` paragraph, `## Release drift`): verify every number (changed-line counts per file: `diff <v7.2 copy> <v7.3 copy> | grep -c '^[<>]'`; 'four files did not change'; errno.h sha256 equal to S481's copy; util.c 14 changed lines none at the quoted lines; the +45/+84/+4/+31 moves) and every statement. Quote each wrong sentence with the correct text.")
add("CritLedgerDrift", "critic",
    f"Attack the `## Release drift` section of {L}/{LEDGER} at {T}: verify against the v7.3 rst (cgit Documentation/admin-guide/cgroup-v2.rst ?h=v7.3 and ?h=v7.2) and code that (a) memory.pressure and io.pressure were documented read-only at 7.2 and read-write at 7.3, and that the files accepted trigger writes at v7.2 (kernel/cgroup/cgroup.c at v7.2: the pressure write handlers); (b) the io.stat throttle field became `delay_nsec` in nanoseconds (block/blk-iolatency.c at v7.2 vs v7.3: what does io.stat print?); (c) the cpu.stat bandwidth-stats note. Overclaims with fenced replacement text; the leads line in {L}/corpus/SOURCES.md `## Leads` too.")
add("ScoutRecheckDebt", "scout",
    f"Per-surface reconnaissance for freshness debt at {T}: for every corpus/knowledge entry with a `recheck:` line, classify the trigger (date cadence, on-release, tool change, none) and whether it has fired by 2026-10-27 (Linux v7.3 tagged; host kernel 7.2.11; systemd 262 on host? `systemctl --version | head -1`; procps `pgrep -V`). Table: entry, trigger, fired?, answered by (ledger/round) or open. Paste the commands.")

# ---------- C2: the entry, the counter ----------
add("ExecMfCallers", "executor",
    f"Read {SRC}/memory-failure.c.v7.3 around every C2 row that quotes it (rows 1-11 of {C2CL}) and trace the callers: who calls kill_proc and kill_procs (forcekill conditions; when is tk->addr -EFAULT), when MF_ACTION_REQUIRED is set, which paths reach action_result with MF_MSG_KERNEL/MF_IGNORED, whether update_per_node_mf_stats has any other caller, and whether every pr_* in the file goes through pr_fmt (any printk/dev_* bypassing the prefix?). Not a vote: report facts with line numbers; never start a line with ENTAIL or REPLACE.")
add("ExecMfV72", "executor",
    f"This host runs Linux 7.2.11. Fetch mm/memory-failure.c, Documentation/mm/hwpoison.rst, Documentation/ABI/stable/sysfs-devices-node and include/trace/events/memory-failure.h at ?h=v7.2 from cgit into your scratch (the last may not exist at v7.2: then find where memory_failure_event lived — include/ras/ras_event.h?) and diff each against {SRC}/*.v7.3. For each of the 21 rows of {C2CL}: does the quote also occur at v7.2 (whitespace collapsed)? Which rows are v7.3-only? Check the entry's `## On this host` and Boundaries sentences ('the kill and recovery lines, the counters and the two older sysctls exist on 7.2') against the v7.2 bytes.")
add("ExecHostRead", "executor",
    f"Read-only host observation for C2: `uname -r`; every file under /sys/devices/system/node/node*/memory_failure/ (values); `grep HardwareCorrupted /proc/meminfo`; /proc/sys/vm/memory_failure_early_kill, memory_failure_recovery, enable_soft_offline, panic_on_unrecoverable_memory_failure (exists?); `ls /sys/kernel/tracing/events/ras/ 2>&1` and `ls /sys/kernel/debug/tracing/events/ras/ 2>&1` (permission errors are results); `journalctl -k -b -o json --no-pager -n 0 2>&1 | head -1` to check access only — never count kernel lines by text. Is rasdaemon/mcelog/edac-util installed (`command -v`)? Compare with the entry's `## On this host` section and {W}/evidence/sweeps.txt. Report every mismatch.")
add("ExecC2Replay", "executor",
    f"Independent run: `python3 {C2} {T}`, `python3 {C2} --selftest`, `python3 {C2} --hashes {T}` (cd into your scratch first); compare with {W}/evidence/c2-at-data.txt, selftest-c2.txt and {C2CL}. Then the do-nothing control `python3 {C2} {E}` vs control-c2-do-nothing.txt. Also write your own located-quote check (not importing the counter) for all 21 rows and report any row whose quote you cannot find in its copy.")
add("MutC2", "mutation-tester",
    f"Mutation-test the frozen counter {C2} in scratch copies: >= 14 single-point mutations (MIN_VOTES 2->1; results binding dropped; REPLACE authorship dropped; fence toggle dropped; words_beyond threshold 3->0; MIN_CLAIMS 14->1; MIN_SOURCES 4->1; quote uniqueness dropped; claim uniqueness dropped; OPENED widened; used-by dropped; pins skipped; provenance subset check dropped; overclaim dissent ignored). Run `--selftest`; killed iff nonzero. Table and the arm text each survivor needs.")
add("RevC2Counter", "reviewer",
    f"Review {C2} line by line: the docstring predicate vs the code, parse_claims (where the table ends; fences), the COPIES map (URLs exactly as S521-S524 and S502/S507 carry them?), entail_votes (results binding, REPLACE authorship by hash, fences), evaluate (every arm and failed name), the selftest arms. Defects with line numbers and severity.")
add("CritC2Junk", "critic",
    f"Find the cheapest edit set that makes `python3 {C2} <rev>` print C2=met without honest depth (claims padded with three unrelated words to pass words_beyond; quotes from license headers or comments that say nothing; a results file the L1 writes; one claim restated 14 times with word swaps). Build each in a `--shared` clone under your scratch (fixture identity, verify toplevel), score with `--repo <clone>`, report met / unmet with the code line responsible. Which classes only the entailment votes stop is a named limit.")
add("CritC2Overclaim", "critic",
    f"Attack the prose of {L}/{ENTRY} at {T} outside the claim table: the `## Claim` paragraph (is it true that a memory-failure kill raises no memcg oom_kill and no oom:mark_victim? grep the v7.3 copies and {L}/corpus/evidence/sources-r47/ for the OOM paths), the decision table (each 'what it means' / 'what it does not mean' cell against the code), the sysctl table (defaults), `## On this host` and Boundaries. Every unsupported word with fenced replacement text and line numbers.")
add("CritC2Axis", "critic",
    f"Attack C2 as a depth move on new ground: AXES.md ({F}/AXES.md) defines depth as verifiable technical detail (decision tables with real thresholds, named error signatures, cited sources). Is the entry that, or coverage/expansion? Is the ground new (`git -C {L} grep -n -iE 'memory.failure|hwpoison|SIGBUS|BUS_MCEERR|HardwareCorrupted' {E} -- .`), and does {L}/PROVINCE.md at {T} cover it (kill events core? frontier?)? Does it cross into a sibling's province (tsukuroi host repair; any lane owning hardware health)? Verdict with pointers and the PROVINCE line that should change.")
add("RevDecisionTable", "reviewer",
    f"Review the two decision tables of {L}/{ENTRY} at {T} against {SRC}/memory-failure.c.v7.3, {SRC}/hwpoison.rst.v7.3, {SRC53}/vm.rst.v7.3 and {SRC}/sysfs-devices-node.v7.3: every row's line text exactly as the kernel prints it (format string → printed form: `%#lx` prints `0x…`), every 'means' cell, every sysctl default, and whether a mori operator could act on SKILL.md with these rows alone. Fenced corrections.")
add("ScoutMfSurfaces", "scout",
    f"Reconnaissance of the other memory-error surfaces around the entry's boundary (read sources, no host writes): what the MCE/EDAC path prints before memory_failure runs (arch/x86/kernel/cpu/mce/core.c at v7.3: the `Hardware Error` / `Memory failure` handoff), what rasdaemon records, what systemd-coredump records for a SIGBUS death (signal 7, `COREDUMP_SIGNAL`), and how `si_code` BUS_MCEERR_AR/AO reach userspace. Which of these is a structured (non-text) signal mori could count? Propose lead rows (URL, what it would teach) — do not claim anything as admitted.")
add("ScoutMoriTools", "scout",
    f"How do mori's existing tools see a non-OOM kernel kill? Read {L}/tools/mori-oom-killers.py, mori-census.sh, mori-seat-terminal.py, mori-pressure.py and SKILL.md's kill/OOM sections at {T}: what would each report for a process killed by SIGBUS from memory failure (silent, misattributed as OOM, 'unknown')? Pointers with line numbers; propose the SKILL.md error-pattern row (fenced) that tells an operator to check the memory-failure counters before calling a death unexplained.")
add("SentC2Boundary", "sentinel",
    f"Boundary review of {L}/{ENTRY} and {L}/{LEDGER} at {T}: does any sentence advise or imply writing a sysctl, injecting or unpoisoning memory, loading hwpoison-inject, or grepping kernel text as a count (QUALITY 15 in {L}/corpus/QUALITY.md)? Are the host reads in the entry and in {W}/evidence/sweeps.txt read-only? Do the Boundaries hand host repair to tsukuroi/operator correctly ({L}/PROVINCE.md Adjacent)? Findings with line numbers.")
add("RevSourcesC2", "reviewer",
    f"Review rows S521-S524 and the used-by changes of S502 and S507 in {L}/corpus/SOURCES.md at {T} against {F}/CORPUS.md's registry contract: anchors (open each named line range in the copy: pr_fmt 37; sysctls 72-78, 134-171; kill_proc 286-311; kill_procs 462-490; action_name 871-876; action_result 1281-1298; hwpoison 54-73, 74-105; sysfs-devices-node 192-229; trace TRACE_SYSTEM line 7, TRACE_EVENT 74-98), sha256 prefixes, kind/tier/scope/teaches, opened 2026-10-27, used-by. Also the `## Leads` additions. Defects with severity.")
add("ConnSiblings", "connector",
    f"Sibling-overlap scan: `grep -rliE 'memory.failure|hwpoison|SIGBUS|HardwareCorrupted|EDAC|rasdaemon|mcelog|v7\\.3' {F}/*-shokunin/corpus/knowledge {F}/*-shokunin/SKILL.md {F}/*-shokunin/PROVINCE.md 2>/dev/null` (paste the command; skip .scratch and .ufo). For each hit: owning lane, whether mori's new entry or ledger duplicates or contradicts it, contested scope (tsukuroi: host OS-state triage and repair). Does any sibling already recheck kernel-pinned claims at v7.3?")
add("ConnCrossClaim", "connector",
    f"Cross-claim pattern: C1 (a located quote is not a located claim — the line arm and the vote carry place and meaning) and C2 (a death without an OOM record is not an unexplained death — the memory-failure counters carry the cause). Read {W}/contract.md, {L}/{LEDGER}, {L}/{ENTRY}. Name the shared principle, the QUALITY rows that state part of it (grep {L}/corpus/QUALITY.md), and any other lane surface where the same gap is open (a tool that reports 'no cause' after checking only OOM evidence; an entry whose anchors are line numbers at an old tag). Table with pointers.")

# ---------- frontier drafting ----------
add("ScribeGate", "scribe",
    f"Draft the lesson's `## Gate` block (fenced; house shape: `## Gate` in {L}/corpus/lessons/round-53.md) for rows S515-S524 (and the used-by changes of S502, S507, S508, S514): per row the URL, access date 2026-10-27, sha256 of the copy, and one located quote of <= 25 words that you verify yourself with a substring test on the copy (paste the test). Rejections to record with reason and flip condition: include/ras/ras_event.h at v7.3 (the L1's first pick for the tracepoint; check it no longer defines memory_failure_event), cdn.jsdelivr.net @v7.3 (HTTP 403 on several paths 2026-10-27 — fetch one yourself), and the docs.kernel.org `latest` page. At least one admit and one reject.")
add("ScribeMistakes", "scribe",
    f"Draft the lesson's `## Mistakes` section (fenced; class · evidence pointer · captured-by · fix; a fix counts only once shown able to fail; shape: {L}/corpus/lessons/round-53.md `## Mistakes`): M1 receipt-revision — the round-53 SCORECARD C1/C2 After cells cite the at-salvage receipts (R = 0df80303), not the landed ones ({L}/corpus/lessons/round-53-verifier-spotcheck.md D2); M2 stale-strays — eight lane-root files from the round-28 and round-38 misroot sweeps carried for 26 rounds (D3; {W}/evidence/d3-relocation.txt); M3 wrong-file — the L1 first picked include/ras/ras_event.h for the tracepoint, which moved to include/trace/events/memory-failure.h (caught pre-freeze by grep). For each, captured-by (a QUALITY criterion number or `none`) and the fix.")
add("ScribeQuality", "scribe",
    f"Draft QUALITY.md criteria continuing the numbering (fenced; read the last 80 lines of {L}/corpus/QUALITY.md for numbering and house style: Lesson, Check, Shown able to fail, Not covered): (a) a SCORECARD claim row cites the receipt measured at the landed revision, never an intermediate one (round-53 D2); (b) a misroot relocation lands under the sweeping round's wave directory, never the lane root (D3); (c) a release recheck names the line where each quote now begins (C1 line arm; shown able to fail: control-c1-no-line); (d) a death with no OOM record is not called unexplained before the memory-failure counters are read (C2). Cite the receipts.")
add("ScribeSkill", "scribe",
    f"Draft a `## Round54` section for {L}/SKILL.md (fenced; house shape: the `## Round53` section at the end of SKILL.md): a decision table for memory-failure kills (kernel line → class → what to read next; counters; sysctls; v7.3 vs this host's 7.2), one error-pattern row (a death with no OOM record), and the v7.3 recheck reading rule (lines moved; the release-drift leads). Every row must cite {L}/{ENTRY} or {L}/{LEDGER} with a line. Never edit SKILL.md.")
add("ScribeReadme", "scribe",
    f"Draft the corpus/README.md additions (fenced): a `## Round-54 coverage additions` block in the house shape of the round-53 block at the end of {L}/corpus/README.md — a coverage-map row for hardware memory-failure kills (kill and OOM events: a non-OOM kill class, knowledge only), one for the v7.3 recheck of the remaining v7.2-pinned rows, and a dated frontier note (the release-drift leads: io.stat delay_nsec, pressure files read-write; the memory-error surfaces before memory_failure — MCE/EDAC/rasdaemon — not held). Never rewrite a Frontier row.")
add("ScribeLog", "scribe",
    f"Draft the LOG.md `## Round 54` entry (fenced; append-only; shape: the round-53 entry at the end of {L}/LOG.md): entering tip {E}, freeze {FZ}, data {T}, the two claims with before receipts and counting commands, the re-verification result (31 held at v7.3; lines moved in three files), assimilation none, the considerthese item (suggestion 3), the round-53 closure routed defects D1-D3 with dispositions (contract `## Frontier step …`), every number not yet measured marked `[L1 fills]`.")
add("ScribeScorecard", "scribe",
    f"Draft the SCORECARD.md additions (fenced; house shape: the round-53 section at the end of {L}/SCORECARD.md): (1) an appended `**Round-53 correction:**` naming `evidence/c1-at-landed.txt` and `evidence/c2-at-landed.txt` (R = 0b36d23e596276c70725873621fe15a28c87189f) as the landed measurement of the round-53 C1/C2 rows, whose After cells cite the at-salvage receipts (round-53 closure D2) — verify the tokens are identical yourself (`diff` of the receipt lines without rev); (2) the `## Round 54` section: claim table (claim, axis, counting command, before, after `[L1 fills]`), controls line, limits, `Planned (round 55)`.")
add("ScribeShonen", "scribe",
    f"Draft the SHONEN.md box updates (fenced, one line per box; read {L}/SHONEN.md): each box keeps its pointers and leads with round-54 evidence (SKILL `## Round54`, LOG round 54, the memory-failure entry's decision table and Boundaries, the selftest receipts the L1 will commit under {W}/evidence/selftests/ — name the files you expect). Tally pins stay in the form `python3 <path> --selftest` (N/N).")
add("ScribeProvince", "scribe",
    f"Read {L}/PROVINCE.md in full. Draft (fenced) the minimal append that keeps it accurate after this round: hardware memory-failure kills (SIGBUS/SIGKILL from mm/memory-failure.c; the per-node counters; HardwareCorrupted) as kill-event ground, knowledge only, with the boundary (no injection, no sysctl write; host repair → tsukuroi/operator; MCE/EDAC hardware health not held) — or say no change is needed and why, with line pointers.")

# ---------- sweeps, routed defects, no-harm ----------
add("ScoutMistakeSweep", "scout",
    f"Mistake sweep for the frontier step: read {L}/corpus/lessons/round-49-verifier-spotcheck.md through round-53-verifier-spotcheck.md; list every disagreement or routed defect, and for each whether a QUALITY.md criterion, lesson fix, erratum or later commit now captures it (grep {L}/corpus/QUALITY.md, lessons, SCORECARD) — CAPTURED (pointer) / OPEN. Paste the grep commands.")
add("ExecConsiderthese", "executor",
    f"considerthese/2026-10-26.md suggestion 3 (read {L}/considerthese/2026-10-26.md): re-execute what the round-53 closure only evidence-verified. From a `git archive` of 28401324ca5e0205645490d8e538b30d5ef4d1bf in your scratch (TMPDIR there): run `python3 .ufo/waves/round-53/count-c1.py 0b36d23e596276c70725873621fe15a28c87189f --repo {L}`, `python3 .ufo/waves/round-53/count-c2.py 0b36d23e596276c70725873621fe15a28c87189f --repo {L} --scratch <scratch>`, both `--selftest`s, and `python3 -I -B tools/mori-commit-runway.py --selftest`; compare each line token by token with {L}/.ufo/waves/round-53/evidence/c1-at-landed.txt, c2-at-landed.txt, selftest-c1.txt, selftest-c2.txt, selftests/mori-commit-runway-a2.txt. Report agreement or the exact divergence (the live leg depends on the host).")
add("RevenD2", "revenger",
    f"Reconstruct how the round-53 SCORECARD C1/C2 rows came to cite the at-salvage receipts (R = 0df80303) while the report measured 0b36d23e: `git -C {L} log --format='%h %ad %s' --date=iso -- SCORECARD.md .ufo/waves/round-53/evidence/` and the order of the salvage, SCORECARD and receipts commits. Timeline with hashes, the check that would have caught it, and whether the same pattern exists in an earlier round's rows (grep SCORECARD for `at-data`/`at-salvage` receipts cited in After cells).")
add("ExecMisrootSweep", "executor",
    f"Misroot pre-sweep (read-only): `git -C {F} status --porcelain` (no pathspec) and list every untracked file at the fleet root or under {F}/.ufo that could belong to mori round 54 (content names mori, round 54, Mo54 or this lane's paths). Never touch .ufo/state/, .scratch/ or other lanes' files. Output: path, evidence it is mori's. Also verify the D3 relocation at {T}: for each line of {W}/evidence/d3-relocation.txt, `git -C {L} show {E}:<old path> | sha256sum` equals `git -C {L} show {T}:<new path> | sha256sum`, and the old path is gone at {T}.")
add("ExecCensusCounts", "executor",
    f"Frontier-step census before -> after: count Registry rows by status and tier at {E} and {T} (`git -C {L} show <rev>:corpus/SOURCES.md`, an awk accepting 0-3 leading spaces), and run `{F}/scripts/sources-census.sh validate --root {F} mori` (rc, W04 count; compare with {W}/evidence/census-start.txt). Paste commands, outputs, exit codes and the delta (expect +10 rows S515-S524, tier A, mined; four used-by cells changed).")
add("ExecPinCheckNoHarm", "executor",
    f"Operability no-harm check: run `python3 {L}/tools/mori-pin-check.py --rev {T}` with the options its `--help` gives for repo and scratch (scratch under {X}/{P}ExecPinCheckNoHarm/) and compare with {L}/.ufo/waves/round-53/evidence/pin-check-at-landed.txt. Any pin that changed state since round 53 is a finding (the round removed eight lane-root files: does any tool, pin or selftest read them?).")
add("SentHostPaths", "sentinel",
    f"Portability audit (round prompt §7 item 4; QUALITY 127) of the round-54 files at {T}: `git -C {L} grep -n '/home/vgpnk' {T} -- .ufo/waves/round-54/`; `git -C {L} grep -nE 'mkdtemp\\(dir=\"/tmp|/tmp/' {T} -- .ufo/waves/round-54/`. Classify each hit: executable default that breaks off-host replay / honours TMPDIR or HYAKU_SCRATCH / prose only. Are count-c1.py, count-c2.py and controls/*.py portable?")
add("SentReceipts", "sentinel",
    f"Receipt integrity: for every file under {W}/evidence/ at {T}, check that it records the literal command it ran and its exit code, and that re-running the cheap commands reproduces the verdict line (count-c1/count-c2 at {T}, selftests, the sweeps' git greps). Also check {W}/evidence/freeze-sha256.txt against the bytes at {FZ} (`git -C {L} show {FZ}:<path> | sha256sum`). List each receipt: literal yes/no, reproduced yes/no/not run.")
add("SimpCode", "simplifier",
    f"Dead weight in {C1}, {C2}, {W}/controls/*.py and {W}/build-w1-spec.py: unused imports/variables/constants, duplicated helpers, dead branches. Prove each deletion on scratch copies (selftest tallies unchanged; a real run gives identical output). The counters are frozen: deletions there are proposals for a successor.")
add("RevNoHarm", "reviewer",
    f"No-harm audit across all six axes: `git -C {L} diff --stat {E} {T}` and read every changed tracked file. For coverage, operability, depth, freshness, calibration, adjacency: name anything the round's changes could have harmed (a removed file another file points at, a broken pointer, a stale pin, a changed instrument verdict, a scope crossed into a sibling, an entry weakened) and check it. Verdict per axis: harmed / not harmed, with evidence.")
add("ExecSelftestReceipts", "executor",
    f"Produce the SHONEN tally-pin receipts for round 54 (content only, inside your report as fenced blocks; the L1 commits them): from a `git archive` of {T} in your scratch with TMPDIR there, run `python3 tools/mori-pin-check.py --selftest`, `python3 tools/mori-unlanded-check.py --selftest`, `python3 -I -B tools/mori-commit-runway.py --selftest`; paste each literal command, the last lines and exit codes. Compare with {L}/.ufo/waves/round-53/evidence/selftests/.")


def main():
    spec = {"wave": "mori-r54-w1", "reportDir": ".ufo/waves/round-54/w1", "context": context, "items": items}
    with open(os.path.join(W, "w1-spec.json"), "w") as f:
        json.dump(spec, f, indent=1)
    roles = {}
    for it in items:
        roles[it["role"]] = roles.get(it["role"], 0) + 1
    attack = sum(v for k, v in roles.items() if k in ("reviewer", "critic", "mutation-tester", "labrat"))
    print(len(items), roles, "attack=%d" % attack)


if __name__ == "__main__":
    main()
