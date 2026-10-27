#!/usr/bin/env python3
"""Build the round-53 wave w1 spec (L1 MoriR53; one v2 wave after the data commit: the C1 RECHECK votes,
attacks on both claims and the new tool, independent fixture recomputation, frontier drafting, routed-defect
evidence). Usage: build-w1-spec.py <freeze> <data>. Paths derive from this file's location."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
L = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))  # lane repo
F = os.path.dirname(L)  # fleet root
W = HERE
E = "20edafa59b38dac1ca358893f0259b1f436372d3"  # entering tip
FZ = sys.argv[1]
T = sys.argv[2]
C1 = W + "/count-c1.py"
C2 = W + "/count-c2.py"
SRC = L + "/corpus/evidence/sources-r53"
LEDGER = "corpus/knowledge/kernel-v7.3-recheck-r53.md"
BAND = "corpus/knowledge/commit-runway-read-r53.md"
TOOL = "tools/mori-commit-runway.py"
CASES = "tools/fixtures/mori-commit-runway/cases.json"
CLAIMS = W + "/evidence/c1-claims.txt"
X = "/fast/scratch/hyaku/mori-r53"
P = "Mo53"
CG = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/"
with open(os.path.expanduser("~/.agents/skills/godspeed/directive.md")) as f:
    GODSPEED = "/skill:godspeed\n" + f.read().rstrip("\n")

context = f"""# mori round 53 — wave w1 (one v2 wave: RECHECK votes, attacks on both claims and the new tool, frontier drafting)
Lane: mori-shokunin (森, fleet and host observability: fleet liveness, wave settlement, kill and OOM events, resource runway; detection and report only). Lane repo: {L}. Fleet root: {F}.
The L1 (MoriR53) froze two claims at {FZ} ({W}/contract.md — read it first; entering tip {E}) and landed the data at {T}:
- C1 freshness: Linux v7.3 is tagged; the round-51 and round-52 entries pin 46 claim rows to v7.2 bytes with `recheck: on-release`. New ledger {L}/{LEDGER} (one row per claim hash: derived status held/absent, v7.3 source row S502-S510, a quote located in the v7.3 copy under {SRC}/, a disposition holds/changed). `python3 {C1} {T}` -> `… status_ok=46 quote_ok=46 … voted=0 … failed=votes` ({W}/evidence/c1-at-data.txt). P-C1 requires, per row, the row's disposition as the FINAL unfenced `RECHECK <hash> holds|changed` line of at least TWO of the twelve RECHECK seats Mo53Fr01-Mo53Fr12, and no RECHECK seat's final line with the other word. Claim text per hash: {CLAIMS} (row numbers = ledger row order).
- C2 coverage: new read-only tool {L}/{TOOL} (CommitLimit/Committed_AS by overcommit mode; under mode 2 the per-CPU error band), fixtures {L}/{CASES}, SKILL.md `## Round53` registry row, entry {L}/{BAND} (rows S511-S513). `python3 {C2} {T} --scratch {X}/<your seat>/c2` -> `C2=met … agree=80 disagree=0 registry=ok live=ok` ({W}/evidence/c2-at-data.txt). The counter's REF function is the reading the tool is compared with; REF and the tool share one author.
The counters, predicates, controls and kill rules are FROZEN: never propose a change to them as a fix for this round; a counter weakness you find is a named limit for the report and a routed item for round 54. Data (ledger rows and dispositions, entry wording, SOURCES rows, the tool, its fixtures, SKILL text) may still be corrected by the L1 if you show it is wrong.
RECHECK and QUOTE lines (read even if your item is not a RECHECK item): the C1 counter reads unfenced lines that start (after spaces) with `RECHECK <12 hex> holds|changed` or `QUOTE <12 hex> :: <text>` ONLY in the reports {W}/w1/Mo53Fr01.md … Mo53Fr12.md. Every other seat must never start a line with the word RECHECK or QUOTE (quote such text inside a sentence if needed).
Rules for every seat:
- Paths: every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Use absolute paths for every read and write. Write ONLY your own report file. Drafts go INSIDE your report as fenced blocks; never edit SKILL.md, SHONEN.md, SCORECARD.md, LOG.md, PROVINCE.md, corpus/, tools/, considerthese/, or any file under {W} except your own report. The L1 integrates.
- Scratch (operator directive 2026-10-25): every clone, work tree, fixture and temp file lives under {X}/<your seat name>/ — `mkdir -p` it, `export TMPDIR={X}/<your seat name>/tmp`, pass it explicitly to every tool (count-c2.py takes `--scratch`), and remove it before you finish (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree` in Python); copy anything you cite into your report first. /tmp only for files under 50 MB; a /tmp path is never evidence. One clone per seat at most (`git clone --shared`/`--no-local` or `git archive`), never a full mirror. Check `{F}/scripts/hyaku/disk-guard.sh status` before a heavy run; on ENOSPC report the free space and stop. Never write an unbounded stream to a file.
- Never mutate the fleet repo, sibling lanes, the lane's jj state or git index: no git add/commit/stash/checkout/reset/pull/push in {L} or {F}, no mutating jj command. Read-only git (log/show/diff/rev-parse/ls-files/grep/archive/clone FROM the lane) is fine. Any fixture repo: D=$(mktemp -d -p {X}/<seat>) && git -C "$D" init -q (or a clone into your scratch), name -C "$D" on every later call, and verify `git -C "$D" rev-parse --show-toplevel` equals $D before the first commit; never commit under a throwaway identity anywhere else. Never write into ~/.local/bin or any PATH directory.
- The tools' cwd is the fleet root: cd into your scratch dir before running anything that writes relative paths. Some frozen round-38..49 instruments hardcode the lane path: run them only from an archive or clone in your scratch, and report any file they create inside {L}.
- Network: raw.githubusercontent.com answered HTTP 429 on 2026-10-26; use git.kernel.org cgit (`{CG}<path>?h=<tag>`) or a sparse `git clone --filter=blob:none` into your scratch. Keep fetches small and few.
- /home/vgpnk/Projects/shokuknow is read-only: read bytes, run nothing there.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): ALL pacman transactions are PAUSED host-wide — never run pacman (no -S, -Sy, -Syu, -U, -R); install via uv tool/npx/an official binary in ~/.local/bin, or report the need; before any future pacman -S the dry-run rule applies (`pacman -Sp --print-format '%n %v' <pkgs>`, proceed only if none is installed).
- Host reads are read-only (detection and report only). Never write a sysctl, never trigger an OOM or a large allocation, never change a cgroup limit, swap or watermark, never run systemctl/journalctl --vacuum/--rotate or any config change. Reading /proc/meminfo, /proc/sys/vm/*, /sys/devices/system/cpu/*, /proc/zoneinfo and /proc/vmstat is allowed. Never grep kernel log MESSAGE text for kill records (lane rule, QUALITY 15).
- No credential material, session or private URLs in any report; write a machine id as MACHINE_ID.
- Leaf seat: no subagents, except an executor may spawn one read-only labrat probe. Do not ask questions. Report observed evidence only (command + output + exit code); say UNVERIFIED where you could not check. A dispatched seat is not an independent judge. End your report with a section `## Findings` listing each finding with a severity (HIGH/MED/LOW) and the file or line it concerns.
"""

items = []


def add(name, role, text):
    n = P + name
    items.append({"name": n, "role": role, "prompt": f"{GODSPEED}\n\n{n}: {text} Scratch: {X}/{n}/."})


RECHECK_RULE = (
    f"Method per row: take the claim text from {CLAIMS}; find the row's v7.2 quote in the committed v7.2 copy "
    f"({L}/corpus/evidence/sources-r51/ or sources-r52/) and the ledger row's quote in the v7.3 copy under {SRC}/ "
    f"(give both line numbers); diff the enclosing function or section between the two copies (`diff -u`); read about "
    f"30 lines of v7.3 context; judge whether the CLAIM, read against the v7.3 file, is still true. Then write on its "
    f"own unfenced line exactly `RECHECK <hash> holds` or `RECHECK <hash> changed — <what changed, with the v7.3 line>`. "
    f"For a row whose status is `absent`, also judge whether the ledger's replacement quote states the same rule; if "
    f"not, propose one on its own line as `QUOTE <hash> :: <6-25 words located in the v7.3 copy>` (your own vote does "
    f"not count for a quote you propose). A later RECHECK line for the same hash replaces your earlier one (last "
    f"unfenced line wins) — use that only if the L1 messages you new evidence. Exactly one RECHECK line per row you were "
    f"given (plus any revision); none for other rows; never inside a fenced block. Be strict: a renamed function, a "
    f"moved check, a new condition or a changed default the claim states is `changed`; a reformatted line that keeps "
    f"the rule is `holds`.")
BLOCKS = [(1, 12), (13, 24), (25, 35), (36, 46)]
for i in range(12):
    a, b = BLOCKS[i // 3]
    add("Fr%02d" % (i + 1), "reviewer" if i % 2 == 0 else "critic",
        f"RECHECK item. Judge ledger rows {a}-{b} of {L}/{LEDGER} at {T} (`git -C {L} show {T}:{LEDGER}`; rows "
        f"numbered in table order, the same numbering as {CLAIMS}). {RECHECK_RULE} Also note, per row, anything in the "
        f"v7.2→v7.3 diff a careless reader might miss.")

# ---------- C1: sources, ledger, counter ----------
add("ExecRefetchCgit", "executor",
    f"Re-fetch the twelve copies under {SRC}/ from git.kernel.org cgit ({CG}<path>?h=v7.3 for the nine `.v7.3` files, ?h=v7.2 for mm_init.c, percpu_counter.c, percpu_counter.h) and report HTTP status, bytes and sha256 against the frozen pins in {C1} (V73) and {W}/evidence/freeze-sha256.txt. Also re-fetch the same nine paths at v7.2 and compare with the lane's committed v7.2 copies under {L}/corpus/evidence/sources-r51/ and sources-r52/ (same bytes?).")
add("ExecRefetchGit", "executor",
    f"Independent channel for the C1 pins: in your scratch run `git init` + `git remote add origin https://github.com/torvalds/linux` + `git fetch --depth 1 --filter=blob:none origin tag v7.3` (or a sparse `git clone --filter=blob:none --no-checkout --depth 1 --branch v7.3`), then `git show v7.3:<path>` for the nine paths of S502-S510 and `git rev-parse v7.3^{{commit}}`; compare each blob's sha256 with the copies in {SRC}/ and the commit with `c03c1a14507d` in the rows' anchors. Report per path: equal / differs. Keep the fetch blob-filtered (never a full clone).")
add("ExecDiffAudit", "executor",
    f"For each of the 46 ledger rows of {L}/{LEDGER} at {T}: locate the v7.2 quote's line in the v7.2 copy and the enclosing function/section, run `diff -u` of that function/section between the v7.2 copy and the v7.3 copy in {SRC}/, and list the rows whose enclosing function or section changed at all (with the hunk). This is input for the RECHECK voters' attackers, not a vote: never start a line with RECHECK.")
add("ExecReplacementQuotes", "executor",
    f"The two `absent` rows (hashes 0fbd62f51ce8 and d7a1dc88dcb3) carry replacement quotes from {SRC}/mmap.c.v7.3. Verify: each replacement occurs (whitespace collapsed) in the v7.3 copy (give lines), has 6-25 words, and states the same condition as the v7.2 quote in {L}/corpus/evidence/sources-r52/mmap.c.v7.2 (show both blocks side by side; explain `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)` vs `vm_flags |= VM_NORESERVE` by reading the v7.3 definitions in a blob-filtered fetch of include/linux/mm.h at v7.3 if needed). Verdict per row.")
add("ExecC1Replay", "executor",
    f"Independent run: `python3 {C1} {T}`, `python3 {C1} --selftest`, `python3 {C1} --scope` (cd into your scratch first); compare with {W}/evidence/c1-at-data.txt, selftest-c1.txt and c1-scope.txt. Then run the do-nothing control `python3 {C1} {E}` and compare with {W}/evidence/control-c1-do-nothing.txt.")
add("ExecControlsReplay", "executor",
    f"Replay all ten controls independently: copy {W}/controls/controls.py and c1-data.py into your scratch, edit ONLY the receipt output directory in your copies to your scratch (the originals write into {W}/evidence/ — never run them in place), and run `python3 <copy>/controls.py {X}/{P}ExecControlsReplay/ctl` with TMPDIR in your scratch. Note the copy must still import the frozen counters from {W}. Compare every verdict line with {W}/evidence/control-*.txt (rev hashes will differ; fields must not). Report differences.")
add("MutC1", "mutation-tester",
    f"Mutation-test the frozen counter {C1} in scratch copies: >= 14 single-point mutations (MIN_VOTES 2->1; drop the fence toggle; last-wins -> first-wins; dissent check over any voter vs RECHECK voters; drop the QUOTE authorship subtraction; status derivation always held; quote check without `q == q72` for held rows; word bounds; scope read at R instead of ENTERING; drop the used-by check; drop the opened-date check; accept the v7.2 URL; pins check skipped; rows==len(d) dropped). Run `--selftest` on each; killed iff it exits nonzero. Table: mutation -> killed/survived -> killing check; arm text for each survivor (a routed limit).")
add("RevC1Counter", "reviewer",
    f"Review {C1} line by line: the docstring predicate vs the code (same sentence? every clause enforced?), scope() (does it read exactly the 46 rows; what if an entry gains or loses rows after {E}), final_votes() (fence handling, last-wins, QUOTE parsing), evaluate() (status/quote/source/disposition arms, counters, failed list), the selftest arms vs the arms. Defects with line numbers and severity.")
add("CritC1Junk", "critic",
    f"Find the cheapest edit set that makes `python3 {C1} <rev>` print C1=met WITHOUT an honest v7.3 recheck (e.g. a voter file written by a non-voter seat under a voter's name; votes copied wholesale; a QUOTE evasion; a ledger row whose quote is located but from an unrelated part of the file; a disposition that the votes support but the file contradicts). Build each in a `--shared` clone under your scratch, commit there (fixture identity, verify toplevel), score with `python3 {C1} <rev> --repo <clone>`, and report each class: met / unmet, with the code line that lets it through.")
add("CritC1Scope", "critic",
    f"Attack C1's scope and axis: D is two entries' claim tables (46 rows). List every other lane artefact at {T} that pins a kernel v7.2 (or older tag) byte with an on-release or release-triggered recheck (`git -C {L} grep -n -E 'recheck:.*(on-release|kernel release)' {T} -- corpus/knowledge`; SOURCES rows with recheck `on-release` and a v7.2 anchor) and say which ones the round leaves unrechecked. Is `freshness` (AXES.md: drift detection, claims re-verified against live surfaces) the honest axis for this move, or is it depth/quality work? Verdict with pointers.")
add("ExecOtherEntriesV73", "executor",
    f"Informational drift probe for round 54 (not this claim): fetch at v7.3 from cgit the files behind {L}/corpus/knowledge/oom-tracepoints-r47.md (copies in {L}/corpus/evidence/sources-r47/) and {L}/corpus/knowledge/oom-memcg-stat-r50.md (sources-r50/: memcontrol.c, oom_kill.c; the cgroup-v2 page at https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html if it exists) into your scratch; run the round-47 counter `{L}/.ufo/waves/round-47/count-c2.py` logic against the v7.3 copies if it can take them (read it first; otherwise test its names/fields by grep), and test every round-50 claim quote for presence in the v7.3 bytes. Report held/absent counts and each absent quote.")
add("RevSourcesRows", "reviewer",
    f"Review rows S502-S513 of {L}/corpus/SOURCES.md at {T} against the registry contract in {F}/CORPUS.md (section `SOURCES.md — where a shokunin learns`): kind, tier, scope, anchor (exact lines + revision), teaches (one grounded benefit), status mined, opened 2026-10-26, recheck, used-by (paths exist; each row is cited by the entry it names). Also the S499 used-by change (old -> new) and the round-53 search-log note. Run `{F}/scripts/sources-census.sh validate --root {F} mori` and compare with {W}/evidence/census-start.txt. Defects with severity.")
add("ExecAnchorCheck", "executor",
    f"For every line range named in the `anchor` cells of S502-S513 ({L}/corpus/SOURCES.md at {T}), print those lines from the copy in {SRC}/ (`sed -n`) and say whether they hold what the row's scope and teaches cells say. Also check the teaches claims 'byte-identical to v7.2' (S504, S506, S509) by sha256 against the round-51/52 copies, and the change summaries (S503, S505, S507, S508, S510) against `diff -u` of the copies. Propose exact replacement anchor text for any drift.")
add("RevLedgerProse", "reviewer",
    f"Review the prose of {L}/{LEDGER} at {T} (intro, `## What changed` table, reading rules, Boundaries — not the ledger rows): verify every number (changed-line counts: rerun `diff -u <v7.2 copy> <v7.3 copy> | grep -c '^[-+][^-+]'` per file), every 'untouched' statement (si_mem_available, folio_is_file_lru, vm_commit_limit, __vm_enough_memory) and the tag/commit ids. Quote each wrong sentence with the correct text.")
add("CritLedgerProse", "critic",
    f"Attack {L}/{LEDGER} at {T} for overclaims: any sentence that says more than the copies in {SRC}/ and the round-51/52 copies support, any reading rule a mori operator could misread as 'the v7.2 entries are now wrong' or 'safe on any kernel', and whether the provenance trio and the Boundaries say exactly what was and was not rechecked. Fenced replacement text per finding.")
add("ExecTagCommit", "executor",
    f"Provenance of the anchors: confirm `refs/tags/v7.3` -> 091b06388b117fefdcb63336ac09956a4914b961 and its peeled commit c03c1a14507dfaf8b856c2608f9ac216021fc222 (`git ls-remote https://github.com/torvalds/linux 'refs/tags/v7.3*'`), the v7.2 tag ids cited in S511-S513, and the release date of v7.3 (from https://www.kernel.org/ or the tag object via a blob-filtered fetch). Report whether the round-52 closure's 'latest renders 7.3.0' observation dates the release before round 52 landed — i.e. how long the on-release trigger stood unanswered.")

# ---------- C2: the tool, the counter, the reading ----------
add("ExecFixtureOracleA", "executor",
    f"Independent oracle for C2, frozen fixtures: import ONLY `mk`, `frozen_fixtures` from {C2} (do not read or call `ref`), and for each of the 16 frozen fixtures compute the expected verdict, exit, batch_pages, band_kb, usable_kb, reserve_kb, single_request_cap_kb, limit_recomputed_kb and limit_consistent yourself from the kernel sources {SRC}/mm_init.c.v7.2, {L}/corpus/evidence/sources-r52/util.c.v7.2 and the tool's documented rules in {L}/{TOOL}'s docstring. Then run the tool on each fixture (write the fixture files into your scratch the way `write_fixture` does) and compare. Report every disagreement with your arithmetic.")
add("ExecFixtureOracleB", "executor",
    f"Independent oracle for C2, seeded fixtures: import ONLY `seeded_fixtures` and `write_fixture` from {C2}; seed = sha256 of the full commit id {T} (`hashlib.sha256('{T}'.encode()).hexdigest()`); for all 64 fixtures compute the expected exit and fields yourself (your own implementation from the kernel source lines, not `ref`), run the tool, and compare. Report counts and every disagreement.")
add("ExecHostLive", "executor",
    f"Live host check of {L}/{TOOL} at {T} (run from a `git archive` in your scratch with `python3 -I -B`): run it 3 times, read /proc/meminfo, /proc/sys/vm/overcommit_* and *_reserve_kbytes, /sys/devices/system/cpu/present yourself, and recompute vm_commit_limit() by hand (show the arithmetic) against the tool's limit_recomputed_kb and the printed CommitLimit; state the mode, verdict and findings. If `strace` is available, run the tool under `strace -f -e trace=openat,write,connect` and list every file opened and every write.")
add("ExecBandDerivation", "executor",
    f"Check the C2 band rule against the kernel: read {SRC}/mm_init.c.v7.2 (mm_compute_batch), {SRC}/percpu_counter.c.v7.2 (percpu_counter_add_batch, __percpu_counter_sum, the CPU masks it iterates), {SRC}/percpu_counter.h.v7.2 and {L}/corpus/evidence/sources-r52/util.c.v7.2 (overcommit_policy_handler, __vm_enough_memory). Is `band = batch x present CPUs` a true upper bound on |global count - exact sum| (online vs present vs possible CPUs; dying CPUs; hotplug fold)? Is the batch recomputed when the mode changes at run time and when memory is hot-added? Does mm_compute_batch differ at v7.3 (fetch mm/mm_init.c?h=v7.3 from cgit)? Quote lines (<= 25 words each) with line numbers.")
add("MutC2Tool", "mutation-tester",
    f"Mutation-test {L}/{TOOL} at {T} in scratch copies (a `git archive` of {T}): >= 14 single-point mutations (`<=` -> `<` at the band test; batch floor 32 -> 16; /256 -> /4; present-CPU count off by one; ignore Hugetlb; ignore overcommit_kbytes; subtract only the admin reserve; mode 0 verdict OK; mode 1 LOW when over; duplicate-line check removed; `kB` unit check removed; integer division -> float; page size ignored; reversed CPU range accepted). For each: does the tool's own `--selftest` kill it, and does `python3 {C2} <rev> --repo <clone>` (commit the mutant in a `--shared` clone under your scratch) kill it? Table with both columns; survivors are findings.")
add("MutC2Counter", "mutation-tester",
    f"Mutation-test the frozen counter {C2} in scratch copies: >= 12 single-point mutations of REF and the harness (band `<=` -> `<`; batch floor; reserve terms; `limit_consistent` always true; type check dropped in compare(); exit-code check dropped; selftest floor 12 -> 1; n == total check dropped; seeded fixtures not run; live leg skipped; registry check dropped; tool_absent not failing). Run `--selftest` (TMPDIR in your scratch); killed iff nonzero. Table and the arm text a survivor needs.")
add("RevC2Tool", "reviewer",
    f"Review {L}/{TOOL} at {T} line by line against its docstring and the interface frozen in {W}/contract.md (`## C2`): parsing (meminfo keys, duplicates, units, cpulist), the limit formula vs `util.c.v7.2:904-916`, the mode branches vs `util.c.v7.2:959-1003`, the band vs mm_compute_batch, exit codes, the usage-error path, `--selftest` (temp dir under TMPDIR, cleanup, matcher check, the PASS line). Defects with line numbers and severity.")
add("RevC2Counter", "reviewer",
    f"Review {C2} line by line: REF vs the kernel lines it cites, the fixture generators (do the seeded fixtures reach every verdict and the band edge?), compare() strictness (types, missing keys), the selftest's hand arithmetic (recompute each by hand), the harness (archive extraction, cwd, timeouts, scratch cleanup), the live leg (which fields, why). Is the docstring predicate the same condition as the code? Defects with line numbers.")
add("CritC2Junk", "critic",
    f"Find the cheapest tool that makes `python3 {C2} <rev>` print C2=met without honest work (e.g. a tool that imports the counter's REF from `.ufo/waves/round-53/`; a tool that reads the fixture directory name; a selftest that prints PASS without running cases; a SKILL row that only names the path). Build each in a `--shared` clone under your scratch, commit (fixture identity, verify toplevel), score with `--repo <clone> --scratch <your scratch>`, and report each class: met / unmet. Which of them the predicate cannot separate is a named limit.")
add("CritC2Semantics", "critic",
    f"Attack the reading of {L}/{TOOL} and {L}/{BAND} at {T}: does `COMMIT_LOW` mislead (root keeps the admin reserve; the user reserve is per process; the band is an upper bound); does mode 0's `single_request_cap_kb` match `__vm_enough_memory` (pages > totalram + total_swap: strictly greater?); is `headroom_kb` negative in mode 0 safe to print; would a mori operator read any field as advice to change a sysctl? Also: is `coverage` (a new surface the tool governs) the honest axis, or is this operability? Verdict with pointers and fenced replacement text.")
add("SentC2ReadOnly", "sentinel",
    f"Safety review of {L}/{TOOL} at {T}: confirm it is read-only (no writes outside the selftest temp dir, no network, no subprocess), safe under `python3 -I -B`, and bounded on hostile inputs: point `--meminfo` at /dev/zero, a FIFO, a 2 GiB sparse file, a directory, a symlink loop (all inside your scratch; /dev/zero only with `timeout 10`). Report each: verdict, exit, time, peak RSS (`/usr/bin/time -v` if present). An unbounded read is a HIGH finding with a proposed bound.")
add("SentC2Hostile", "sentinel",
    f"Fuzz {L}/{TOOL} at {T} with malformed inputs in your scratch: empty files, unicode digits, negative and huge integers (2**70), leading/trailing spaces, CRLF line ends, `kB` vs `KB`, tabs, a meminfo with the four lines in reverse order, cpulists like `0-`, `,`, `00-03`, a vm file holding `2\\n3`. Every case must give a valid JSON verdict (`COMMIT_UNKNOWN` when malformed) and never a traceback. Table: input -> verdict/exit; tracebacks are HIGH.")
add("ExecC2Replay", "executor",
    f"Independent run: `python3 {C2} {T} --scratch {X}/{P}ExecC2Replay/c2`, `TMPDIR={X}/{P}ExecC2Replay/tmp python3 {C2} --selftest`, `python3 -I -B {L}/{TOOL} --selftest` (from a `git archive` of {T} in your scratch), and `python3 {C2} --fixtures {T}` (first and last 3 lines). Compare with {W}/evidence/c2-at-data.txt and selftest-c2.txt. Then re-run the do-nothing control `python3 {C2} {E} --scratch …` and compare with control-c2-do-nothing.txt.")
add("ExecToolPortability", "executor",
    f"Portability of {L}/{TOOL} and {L}/{CASES} at {T}: run the selftest from a `git archive` under your scratch with every python3.x interpreter present (`ls /usr/bin/python3*`), with TMPDIR set to your scratch (does the selftest honour it? list what it creates), with `--page-kb 16` and `--page-kb 64` on the live host, and with HOME unset. `git -C {L} grep -n '/home/vgpnk' {T} -- {TOOL} {CASES} {W}/` — classify each hit (executable default / prose).")
add("CritCapability", "critic",
    f"Attack C2 as a capability and coverage move: AXES.md ({F}/AXES.md §Capabilities) requires the capability to run and its output to verify in the round; PROVINCE ({L}/PROVINCE.md) must list the surface. Does {L}/PROVINCE.md at {T} name the commit ledger / CommitLimit as a core or frontier surface (grep), and what line should change? Does the SCORECARD capabilities table already hold a row that covers this (`grep -n -A40 '^## Capabilities' {L}/SCORECARD.md`)? Is the move frontier->core or new ground? Verdict with pointers.")
add("ScoutRunwayTools", "scout",
    f"Per-surface reconnaissance for resource runway at {T}: list every lane tool and knowledge entry that reads /proc/meminfo, /proc/sys/vm, /proc/pressure or cgroup memory files (`git -C {L} grep -n -E 'meminfo|/proc/sys/vm|pressure|MemAvailable|CommitLimit|memory.max' {T} -- tools corpus/knowledge SKILL.md`), what each prints, and which runway question each answers. Where does the new commit-runway tool overlap (census, pressure, memavailable entry) and what runway question is still unanswered after this round?")
add("ConnSiblings", "connector",
    f"Sibling-overlap scan: `grep -rliE 'overcommit|CommitLimit|Committed_AS|percpu_counter|v7\\.3|on-release' {F}/*-shokunin/corpus/knowledge {F}/*-shokunin/SKILL.md {F}/*-shokunin/PROVINCE.md {F}/*-shokunin/tools 2>/dev/null` (skip .scratch and .ufo/waves; paste the command). For each hit: owning lane, whether mori's tool or ledger duplicates or contradicts it, contested scope (tsukuroi owns host OS-state triage; kama local model serving memory). Also: does any sibling already run a release-recheck of kernel-pinned claims?")
add("ConnCrossClaim", "connector",
    f"Cross-claim pattern: C1 (a pinned quote is not the claim — the disposition carries the meaning) and C2 (a printed number is not the enforced number — the mode and the band carry the meaning). Read {W}/contract.md, {C1}, {C2}, {L}/{LEDGER}, {L}/{BAND}. Name the shared principle, the existing QUALITY rows that state part of it (grep {L}/corpus/QUALITY.md), and any other lane surface where the same gap is still open (a gate trusting a printed value, an entry trusting a located quote). Table with pointers.")

# ---------- frontier drafting ----------
add("ScribeGate", "scribe",
    f"Draft the lesson's `## Gate` block (fenced; house shape: `## Gate` in {L}/corpus/lessons/round-52.md) for rows S502-S513: per row the URL, access date 2026-10-26, sha256 of the copy, and one located quote of <= 25 words that you verify yourself with a substring test on the copy in {SRC}/ (paste the test). Add at least one admit and one reject decision: reject candidates — the raw.githubusercontent.com v7.3 URLs (HTTP 429 on 2026-10-26; fetch one yourself and record the status) and https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html (rendered `latest`, not pinned) — each with reason and flip condition. Also the S499 used-by change old -> new.")
add("ScribeMistakes", "scribe",
    f"Draft the lesson's `## Mistakes` section (fenced; class · evidence pointer · captured-by · fix; a fix counts only once shown able to fail; read {L}/corpus/lessons/round-52.md `## Mistakes` for the shape): M1 number-drift — the round-52 SCORECARD C1 row carries the at-data tally (42/27) while citing c1-at-landed.txt (43/28) ({L}/corpus/lessons/round-52-verifier-spotcheck.md D2); M2 landing — `[FILL]` left where the report's own hash belongs (D1); M3 stale-premise — the v7.2 entries' on-release trigger fired (v7.3 tagged) and no round noticed until 53 (fix shown able to fail: {W}/evidence/control-c1-do-nothing.txt vs c1-at-data.txt). For each, captured-by (QUALITY criterion or `none`) and the fix.")
add("ScribeQuality", "scribe",
    f"Draft QUALITY.md criteria from 144 onward (fenced; read the last 80 lines of {L}/corpus/QUALITY.md for numbering and house style: Lesson, Check, Shown able to fail, Not covered): (a) an entry pinned to a tag with `recheck: on-release` is answered by a recheck ledger when a newer tag exists (C1 counter; shown able to fail: control-c1-do-nothing); (b) a runway verdict names the enforcement mode and the error band (C2; controls mode-blind, no-band); (c) a SCORECARD row's numbers are the numbers of the receipt it cites (round-52 D2); (d) a report never carries a placeholder where its own commit belongs (D1). Cite the counters and receipts.")
add("ScribeSkill", "scribe",
    f"Review the new `## Round53` section at the end of {L}/SKILL.md at {T} against {L}/{TOOL}, {L}/{BAND} and {L}/{LEDGER}: every row true? every pointer resolves? missing error patterns (e.g. reading the band as a deviation measurement)? Draft fenced additions only (never edit). Check the registry row has every field PROTOCOL.md §Gate standard `Registry` requires ({F}/PROTOCOL.md).")
add("ScribeReadme", "scribe",
    f"Draft the corpus/README.md additions (fenced): a `## Round-53 coverage additions` block in the house shape of the round-52 block at the end of {L}/corpus/README.md — one coverage-map row for the commit-runway tool (resource runway: knowledge -> tool), one for the v7.3 recheck ledger (freshness of the r51/r52 entries), and a dated frontier note (FR8 threshold calibration still open; the v7.3 `panic_on_unrecoverable_memory_failure` lead; the unrechecked r47/r50 entries). Never rewrite a Frontier row.")
add("ScribeLog", "scribe",
    f"Draft the LOG.md `## Round 53` entry (fenced; append-only; read the round-52 entry at the end of {L}/LOG.md for the shape): entering tip {E}, freeze {FZ}, data {T}, the two claims with their before receipts and counting commands, the re-verification result (freshness axis: 44 held / 2 absent at v7.3), assimilation none, the considerthese item, the round-52 closure routed defects 1-3 with dispositions (contract `## Round-52 closure routed defects`), every number not yet measured marked `[L1 fills]`.")
add("ScribeScorecard", "scribe",
    f"Draft the SCORECARD.md additions (fenced; house shape: the round-52 section at the end of {L}/SCORECARD.md): (1) an appended `Round-52 correction` line naming the superseded text of the round-52 C1 row (42/27 -> 43/28 from evidence/c1-at-landed.txt), per the round-52 closure D2; (2) the `## Round 53` section: claim table (claim, axis, counting command, before, after `[L1 fills]`), controls line, limits, a `### capabilities` row for the commit-runway read (name, what it can do, evidence command, first-working round 53), and `Planned (round 54)`.")
add("ScribeShonen", "scribe",
    f"Draft the SHONEN.md box updates (fenced, one line per box; read {L}/SHONEN.md): each box keeps its pointers and leads with round-53 evidence (SKILL `## Round53`, LOG round 53, `python3 -I -B tools/mori-commit-runway.py --selftest` (23/23) next to the existing tally pins with round-53 receipts under {W}/evidence/selftests/ — the L1 will create them; name the files you expect, the commit-runway and ledger Boundaries). Tally pins must stay in the form `python3 <path> --selftest` (N/N).")
add("ScribeProvince", "scribe",
    f"Read {L}/PROVINCE.md in full. Draft (fenced) the minimal change that keeps it accurate after this round: the commit ledger (CommitLimit/Committed_AS via `tools/mori-commit-runway.py`) as a core resource-runway surface, and the v7.3 recheck as freshness work on existing surfaces — or say no change is needed and why, with line pointers. Never claim host configuration (operator) or OS-state triage (tsukuroi).")
add("ScribeReportConvention", "scribe",
    f"Routed defect 2 of the round-52 closure ({L}/corpus/lessons/round-52-verifier-spotcheck.md): the round-52 report left `[FILL]` where its own commit hash belongs. Read the report ({F}/.ufo/reports/round-52/mori.md) and two sibling reports of round 52 under {F}/.ufo/reports/round-52/ that cite their own commit (grep 'Report commit'). Draft (fenced) the convention text for the lesson: how a report names its own commit without a placeholder (a command over the fleet repo), and the erratum line for round 52 (the existing hash aacd7a83027cdee8e950a2c39d490feaed3be13c, verified with `git -C {F} log --format='%H %an' -- .ufo/reports/round-52/mori.md`).")

# ---------- sweeps, routed defects, no-harm ----------
add("ScoutMistakeSweep", "scout",
    f"Mistake sweep for the frontier step: read {L}/corpus/lessons/round-48-verifier-spotcheck.md through round-52-verifier-spotcheck.md; list every disagreement or routed defect, and for each whether a QUALITY.md criterion, lesson fix, erratum or tool now captures it (grep {L}/corpus/QUALITY.md and lessons) — CAPTURED (pointer) / OPEN. Paste the grep commands.")
add("ExecConsiderthese", "executor",
    f"considerthese/2026-10-26.md suggestion 2 (follow unfixed critic flags forward; read {L}/considerthese/2026-10-26.md): from {L}/corpus/lessons/round-52.md (`## Wave w1 — integrated findings`) and the HIGH/MED findings in {L}/.ufo/waves/round-52/w1/*.md, list every flag the round-52 wave raised; for each say whether it was fixed (commit), routed (to which planned line), or silently dropped as of {E} (`git -C {L} log --oneline 4f266ef2..{E}`, grep SCORECARD `Planned (round 53)`). Output a carry-over ledger table with counts flagged / fixed / routed / dropped.")
add("RevenR52Row", "revenger",
    f"Reconstruct how the round-52 SCORECARD C1 row came to carry the at-data tally (`items=42 … locators=27`) while citing `evidence/c1-at-landed.txt` (`items=43 … locators=28`): `git -C {L} log --format='%h %ad %s' --date=iso -- SCORECARD.md .ufo/waves/round-52/evidence/c1-at-landed.txt`, the order of the integration and receipts commits, and what changed between the at-data and landed runs (which item and locator were added). Timeline with hashes, and the check that would have caught it.")
add("ExecMisrootSweep", "executor",
    f"Misroot pre-sweep (read-only): `git -C {F} status --porcelain` (no pathspec) and list every untracked file at the fleet root or under {F}/.ufo that could belong to mori round 53 (content names mori, round 53, Mo53 or this lane's paths). Never touch .ufo/state/, .scratch/ or other lanes' files. Output: path, evidence it is mori's, the `cmp` command to copy it into {L}. Also `git -C {L} status --porcelain --ignored` outside `.ufo/waves/round-53/`, and the lane-root oddities `--repo` (a directory?) and `0`: `git -C {L} ls-files -- 0 '--repo'`, `git -C {L} log --format='%h %s' -- 0`, contents — are they seat misroots of an earlier round?")
add("ExecCensusCounts", "executor",
    f"Frontier-step census before -> after: count Registry rows by status and tier at {E} and {T} (`git -C {L} show <rev>:corpus/SOURCES.md`, an awk accepting 0-3 leading spaces), and run `{F}/scripts/sources-census.sh validate --root {F} mori` (rc, W04 count; compare with {W}/evidence/census-start.txt). Paste commands, outputs, exit codes, and the delta (expect +12 rows S502-S513, tier A, mined).")
add("ExecPinCheckNoHarm", "executor",
    f"Operability no-harm check: run `python3 {L}/tools/mori-pin-check.py --rev {T} --repo {L} --scratch {X}/{P}ExecPinCheckNoHarm/pc` (read `--help` first; minutes) and `python3 {L}/tools/mori-unlanded-check.py --repo {L} --round 53`; compare with the round-52 receipts under {L}/.ufo/waves/round-52/evidence/ (selftests/, c1-at-landed.txt). Is the new SKILL pin `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23` enumerated and green? Any pin that changed state since round 52 is a finding.")
add("SentHostPaths", "sentinel",
    f"Portability audit (round prompt §7 item 4; QUALITY 127) of the round-53 files at {T}: `git -C {L} grep -n '/home/vgpnk' {T} -- .ufo/waves/round-53/ tools/mori-commit-runway.py`; `git -C {L} grep -nE 'mkdtemp\\(dir=\"/tmp|/tmp/' {T} -- .ufo/waves/round-53/ tools/mori-commit-runway.py`. Classify each hit: executable default that breaks off-host replay / honours TMPDIR / prose only. Are count-c1.py, count-c2.py, controls/*.py and the tool portable?")
add("SentReceipts", "sentinel",
    f"Receipt integrity (literal commands): for every file under {W}/evidence/ at {T}, check that it records the literal command it ran, its exit code, and that re-running the command reproduces the verdict line (run the cheap ones — count-c1 runs, selftests, sweeps' git greps; count-c2 runs with --scratch in your scratch). List each receipt: literal yes/no, reproduced yes/no/not run. Also check {W}/evidence/freeze-sha256.txt against the bytes at {FZ} (`git -C {L} show {FZ}:<path> | sha256sum`).")
add("SimpCode", "simplifier",
    f"Dead weight in {C1}, {C2}, {W}/controls/c1-data.py, {W}/controls/controls.py and {L}/{TOOL}: unused imports/variables/constants, duplicated helpers, dead branches. Prove each deletion on scratch copies (selftest tallies unchanged; a real run gives identical output). The counters are frozen: deletions there are proposals for a successor; the tool is data and may change — say which deletions are safe now.")
add("RevNoHarm", "reviewer",
    f"No-harm audit across all six axes: `git -C {L} diff --stat {E} {T}` and read every changed tracked file. For coverage, operability, depth, freshness, calibration, adjacency: name anything the round's changes could have harmed (a removed row, a broken pointer, a stale pin introduced, a changed instrument verdict, a scope crossed into a sibling, a recheck weakened) and check it. Verdict per axis: harmed / not harmed, with evidence.")
add("ExecSelftestReceipts", "executor",
    f"Produce the SHONEN tally-pin receipts for round 53 (content only, inside your report as fenced blocks; the L1 commits them): from a `git archive` of {T} in your scratch with TMPDIR there, run `python3 tools/mori-pin-check.py --selftest`, `python3 tools/mori-unlanded-check.py --selftest`, `python3 -I -B tools/mori-commit-runway.py --selftest`; paste each literal command, full last lines and exit codes. Compare with {L}/.ufo/waves/round-52/evidence/selftests/.")


def main():
    spec = {"wave": "mori-r53-w1", "reportDir": ".ufo/waves/round-53/w1", "context": context, "items": items}
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
