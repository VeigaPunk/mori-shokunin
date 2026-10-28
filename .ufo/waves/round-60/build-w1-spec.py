#!/usr/bin/env python3
"""Build the round-60 w1 spec (64 seats, policy v2) — build/falsify items for
claims C1 (calibration), C2 (depth), C3 (operability) plus the frontier step.
Run from the lane repo root. Emits .ufo/waves/round-60/w1-spec.json."""
import json
from pathlib import Path

WAVE = "mori-r60-w1"
REPORT_DIR = ".ufo/waves/round-60/w1"
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
FREEZE = "ac496c7cde8cad965079858accae3bedfe4a73f2"
ENTERING = "ddfb12fb0838b4307c445194a844f0c4b1950195"
R59DATA = "7b86704d7c0754a09958d131b64dbfa2a6d3eaed"
R59LAND = "f091bd773c4cfec8877061c84f4bae5f11e8bbe5"

CONTEXT = f"""# mori round 60 — one v2 build/falsify wave (64 seats)
Lane repo: {LANE}. Fleet root: {FLEET}. L1: MoriR60. Frozen contract: {LANE}/.ufo/waves/round-60/contract.md. Frozen counters: {LANE}/.ufo/waves/round-60/count-c1.py, count-c2.py, count-c3.py. Amended freeze revision: {FREEZE} (pre-data amendments 1-2 recorded in the contract; no seat scored before them); entering revision: {ENTERING}. Claims: C1 calibration (round-59 self-record: dead-pointer corrections under r60-correction:, receipts r59-c1-met.txt/r59-c2-met.txt byte-equal to fresh re-runs at {R59DATA}, absent-set table r59-absent-set.md vs git truth, round-60 lesson corrections); C2 depth (hardened verifier tools/mori-entry-claims-check.py — H1 grammar blocks, H2 distinct byte spans >=8, H3 non-degenerate texts, H4 per-copy row binding, H5 attributed drift arm + renamed r54 control — over 13 frozen hostile trees and the real r59 entry); C3 operability (G1 pin-gated execution — an unpinned blob never runs while the r59 counter reproduces the marker hole as control; G2 containment-asserted materialization; G3 frozen expect tables with tamper flagging). C2 and C3 already measure met at the freeze revision (evidence/c2-at-freeze.txt, c3-at-freeze.txt); C1's data (receipts, SCORECARD corrections, absent-set table, lesson, SOURCES rows) lands DURING this wave, so the lane tip may move under you: pin every re-derivation to a named revision and never trust an unpinned working-tree read.

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Write only your own report under {LANE}/.ufo/waves/round-60/w1/. Do not edit production files, corpus registry, SCORECARD, LOG, or lane VCS; return findings/drafts only. Do not write to fleet or sibling repos. Use absolute paths for every file access.

Scratch root for this round is `$HYAKU_SCRATCH/mori-r60/<seat-name>/` (default `/fast/scratch/hyaku`): create it explicitly with mkdir -p, set TMPDIR there, pass --scratch to the counters, clean it before yielding, and copy any small receipt into your report first. `/tmp` only for files under 50 MB, never as evidence. One lightweight clone/worktree per seat only if needed; prefer `git show`/read-only reads (a lane gate or selftest that runs git writes must run on a sandbox clone under your scratch dir, never in the lane). Check `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before heavy work; on ENOSPC report free space and do not rerun until status is green.

Before installing/updating a tool, read `/home/vgpnk/.omp/agent/RULES.md`; use official channels and record tool/version/channel/reason. Pacman transactions are paused host-wide: do not run pacman. Never pipe unverified remote scripts into a shell. Never expose secrets, session material or private URLs. Detection/report only; no remediation or provider-death inference. No seat spawns or additional swarms. Frozen claims, counters, predicates and kill rules are immutable after scoring. Any fixture repo must be initialized at an explicit scratch path (`D=$(mktemp -d -p $HYAKU_SCRATCH/mori-r60/<seat-name>) && git -C "$D" init -q`) and every git command must use `git -C <that path>`; never commit outside that throwaway repo. Never `agent://all`; you report only to the L1 (MoriR60) by agent message when coordination is essential."""

ITEMS = []


GODSPEED = (Path.home() / ".agents/skills/godspeed/directive.md")
try:
    _GS = GODSPEED.read_text()
except OSError:
    _GS = ""  # fail closed to the invocation line only; recorded in report


def add(name, role, text):
    text = text.replace("{REV}", REV)
    lead = "/skill:godspeed\n" + _GS + ("\n" if _GS and not _GS.endswith("\n") else "")
    ITEMS.append({"name": name, "role": role,
                  "prompt": lead + text + BOUNDS})


BOUNDS = (" Work read-only; return concise findings with exact evidence "
          "(commands, outputs, line pointers). No commits, no VCS mutation, "
          "no fleet/sibling writes.")

REV = (f"Read {LANE}/.ufo/waves/round-60/contract.md first (freeze {FREEZE}, "
       f"entering {ENTERING}).")

# ---- reviewer (16) ----
add("Mo60Reviewer01", "reviewer", f"""Mo60Reviewer01: C2 re-derivation at the freeze: run `python3 {LANE}/.ufo/waves/round-60/count-c2.py {FREEZE} --scratch <your scratch>/c2f` and byte-compare with {LANE}/.ufo/waves/round-60/evidence/c2-at-freeze.txt; then re-run at the current lane tip and report any drift in the met line. {{REV}}""")
add("Mo60Reviewer02", "reviewer", f"""Mo60Reviewer02: C3 re-derivation at the freeze: run `python3 {LANE}/.ufo/waves/round-60/count-c3.py {FREEZE} --scratch <your scratch>/c3f` and byte-compare with evidence/c3-at-freeze.txt; confirm the old-counter control arm still reproduces the EXEC-MARKER (a control that stops failing would invalidate the claim). {{REV}}""")
add("Mo60Reviewer03", "reviewer", f"""Mo60Reviewer03: C1 re-derivation at the current lane tip once the data lands: run count-c1.py <tip> and verify the frozen target `C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok`; if the tip does not yet carry the data, say so and retry once after 10 minutes. {{REV}}""")
add("Mo60Reviewer04", "reviewer", f"""Mo60Reviewer04: no-false-negative audit of the hardened verifier: materialize the real entry + registry + 6 copies at {FREEZE} into scratch, run tools/mori-entry-claims-check.py, confirm ok with claims=13 spans=13; then apply three benign mutations in your scratch copy (fix a typo in a claim text, reorder two claim lines, append one prose paragraph) and confirm the verdict stays ok for each. {{REV}}""")
add("Mo60Reviewer05", "reviewer", f"""Mo60Reviewer05: hostile-tree battery: materialize all 13 trees under {LANE}/.ufo/waves/round-60/trees-c2h/ at {FREEZE}, run the tool per tree, and build the per-tree verdict+reason table; confirm each matches its frozen expect (h00 must verify True). {{REV}}""")
add("Mo60Reviewer06", "reviewer", f"""Mo60Reviewer06: H1 grammar-routing: in scratch, append a malformed claim line to the real entry and confirm the tool fails with grammar; then import the r59 counter (git show {R59DATA}:.ufo/waves/round-59/count-c2.py) and drive its eval_entry on the same variant to confirm the old grammar orphaned the reason (the routed hole). {{REV}}""")
add("Mo60Reviewer07", "reviewer", f"""Mo60Reviewer07: H2 span-aliasing: in scratch, build entry variants over the real copies — line+offset to the same span, two claims to one span — and confirm distinct:dup_span; confirm the old r59 eval_entry accepted both. {{REV}}""")
add("Mo60Reviewer08", "reviewer", f"""Mo60Reviewer08: H4 row-binding: registry variants in scratch (status queued, used-by another entry, source cell scrubbed of the artifact path) must yield rows:status / rows:usedby / rows:binding; also confirm the real registry rows S553-S559 bind all six cited copies. {{REV}}""")
add("Mo60Reviewer09", "reviewer", f"""Mo60Reviewer09: receipts arm: re-run the r59 counters at {R59DATA} (`git show {R59DATA}:.ufo/waves/round-59/count-c1.py` to scratch, run with --scratch) and byte-compare each output with the committed {LANE}/.ufo/waves/round-60/evidence/r59-c1-met.txt and r59-c2-met.txt; both rc must be 0. {{REV}}""")
add("Mo60Reviewer10", "reviewer", f"""Mo60Reviewer10: absent-set truth matrix: for Mo59Executor40, Mo59MutationTester31, Mo59MutationTester32, Mo59Critic29, Mo59Reviewer16 run `git -C {LANE} cat-file -e <rev>:.ufo/waves/round-59/w1/<name>.md` at {R59DATA}, {R59LAND} and the current tip; compare with {LANE}/.ufo/waves/round-60/evidence/r59-absent-set.md rows and report any disagreement. {{REV}}""")
add("Mo60Reviewer11", "reviewer", f"""Mo60Reviewer11: dead-name sweep: `grep -n 'c1-entering\\.txt\\|c2-entering\\.txt' {LANE}/SCORECARD.md` at the tip; every occurrence must sit on a line carrying `r60-correction:` and name the real pointer; confirm both control-*.txt real pointers exist at the tip. {{REV}}""")
add("Mo60Reviewer12", "reviewer", f"""Mo60Reviewer12: lesson-correction audit: {LANE}/corpus/lessons/round-60.md must contain `supersedes round-59`, a `supersedes` line for Mo59Critic29 and Mo59Reviewer16, and `late` lines for the other three names carrying {R59LAND[:8]}. {{REV}}""")
add("Mo60Reviewer13", "reviewer", f"""Mo60Reviewer13: QUALITY-154 predicate-identity audit: the contract's frozen target tokens for C1/C2/C3 must each be emitted by the corresponding counter's print line (read the mains); name any token the counter cannot print. {{REV}}""")
add("Mo60Reviewer14", "reviewer", f"""Mo60Reviewer14: C1 control replay: run count-c1.py {ENTERING} and byte-compare with evidence/control-c1-do-nothing.txt (both the line and exit 1). {{REV}}""")
add("Mo60Reviewer15", "reviewer", f"""Mo60Reviewer15: C2/C3 control replay at {ENTERING}: run both counters, confirm unmet with failed lists matching evidence/control-c2-do-nothing.txt and control-c3-do-nothing.txt (token sets, modulo rev). {{REV}}""")
add("Mo60Reviewer16", "reviewer", f"""Mo60Reviewer16: wave-shape conformance: from {LANE}/.ufo/waves/round-60/w1-dispatch.json report the seat count, per-role counts, attack share (reviewer+critic+mutation-tester+sentinel)/total, and that policy v2 band 64-128 applies; flag any duplicate name or unknown role. {{REV}}""")

# ---- critic (8) ----
add("Mo60Critic21", "critic", f"""Mo60Critic21: cheapest-met attack on C2: rebuild Mo59Critic22's semantically-empty construction (ten `x.` claims, one repeated span, fabricated row) against the NEW tool in a scratch root; if any variant returns ok=true, that is a kill — report the exact entry bytes. {{REV}}""")
add("Mo60Critic22", "critic", f"""Mo60Critic22: grammar-orphan hunt: try to make a claim-shaped line that the r60 tool ignores (unicode lookalike dashes, double-star variants, trailing spaces, K-labels inside code spans) yet still counts as a claim or smuggles a false quote past the grammar; report any bypass. {{REV}}""")
add("Mo60Critic23", "critic", f"""Mo60Critic23: row-binding forgery: fabricate rows that satisfy H4 while lying (source cell naming the artifact path but wrong anchor/date; a second row for the same artifact; mined row whose teaches is empty) — map exactly which lies H4 catches and which it structurally cannot (scope boundary, not a defect unless a claim depends on it). {{REV}}""")
add("Mo60Critic24", "critic", f"""Mo60Critic24: drift-arm mutants: build mutant scan tools (filename heuristic, note-nullability, unconditional exit 1) in scratch PoC repos and run the r60 count-c2 drift arm logic against them — attribution (extra_keys) or the renamed r54 control must kill each mutant; verify. {{REV}}""")
add("Mo60Critic25", "critic", f"""Mo60Critic25: receipts determinism: run each r59 counter TWICE at {R59DATA} under different scratch dirs and confirm byte-identical stdout; then analyze at token level whether a committed receipt could byte-equal a re-run yet lie about the revision (the rev= token is the only rev carrier) — report. {{REV}}""")
add("Mo60Critic26", "critic", f"""Mo60Critic26: absent-set lie attack: would a flipped disposition cell or a wrong at-data cell be caught by count-c1 against real git truth? Drive parse_absent_table + the measure() checks on a tampered table copy in scratch; report exactly which lies are caught. {{REV}}""")
add("Mo60Critic27", "critic", f"""Mo60Critic27: dead-name marker gaming: try SCORECARD constructions where a dead name survives outside the marker rule (marker on a neighboring line, mixed into a path, different case) — confirm count-c1 counts them (dead>0) or name the gap. {{REV}}""")
add("Mo60Critic28", "critic", f"""Mo60Critic28: whole-contract falsification sweep: find the cheapest committed-revision path where all three counters print met WITHOUT the claimed work (empty tree, entering rev, counters-only tree); report per-claim why the do-nothing arms hold or break. {{REV}}""")

# ---- mutation-tester (5) ----
add("Mo60MutationTester31", "mutation-tester", f"""Mo60MutationTester31: mutate tools/mori-entry-claims-check.py one predicate at a time in scratch copies (drop the H1 grammar block; MIN_SPAN 8->1; distinct-span collapse off; MIN_TEXT 10->1; H4 binder loop off) — each mutant must flip at least one hostile tree verdict or the h00 control; report the kill table. {{REV}}""")
add("Mo60MutationTester32", "mutation-tester", f"""Mo60MutationTester32: mutate count-c2.py arms in scratch copies (drop the renamed r54 control; accept any nonzero drift exit without verdict check; skip expect.txt equality; skip spans==claims) — each mutant must flip a frozen tree, the drift arm, or the entry arm; report the kill table. {{REV}}""")
add("Mo60MutationTester33", "mutation-tester", f"""Mo60MutationTester33: mutate count-c1.py in scratch copies (ignore the r60-correction: marker filter; skip one receipt byte-compare; accept any 5-cell row; drop the lesson greps) — each must flip the C1 target or a selftest case; report. {{REV}}""")
add("Mo60MutationTester34", "mutation-tester", f"""Mo60MutationTester34: mutate count-c3.py gates in scratch copies (execute the blob regardless of pin; drop the containment assert; accept any expect.txt) — the PoC battery must catch each mutant (marker appears / escape writes / tamper unflagged); report. {{REV}}""")
add("Mo60MutationTester35", "mutation-tester", f"""Mo60MutationTester35: selftest consistency: run all three counters' --selftest plus the tool selftest twice each — once with TMPDIR set to your scratch, once with TMPDIR unset — and confirm identical pass counts, exit 0, and no writes outside the explicit scratch (list any stray dirs). {{REV}}""")

# ---- sentinel (3) ----
add("Mo60Sentinel41", "sentinel", f"""Mo60Sentinel41: execution-boundary re-audit: read all three r60 counters end-to-end and confirm no code path executes repo-supplied bytes whose sha256 differs from the frozen pin (count-c1 executes no repo tool blob at all — verify structurally); drive one unpinned-blob PoC if in doubt. {{REV}}""")
add("Mo60Sentinel42", "sentinel", f"""Mo60Sentinel42: write-boundary audit: snapshot `git -C {LANE} status --porcelain` before and after one full run of each counter; confirm zero lane-tree writes and that materialize() refuses symlink-parent escapes (drive the G2 cases yourself under scratch). {{REV}}""")
add("Mo60Sentinel43", "sentinel", f"""Mo60Sentinel43: leakage audit: confirm the committed receipt bytes contain no scratch/TMPDIR paths and no host paths (receipts must reproduce byte-for-byte on any checkout); grep the counters for absolute host paths (QUALITY 127) and report any hit. {{REV}}""")

# ---- executor (12) ----
add("Mo60Executor51", "executor", f"""Mo60Executor51: materialize the r59 count-c1 from `git show {R59DATA}:.ufo/waves/round-59/count-c1.py` under your scratch and run it at {R59DATA} with --scratch under your scratch; return the exact stdout bytes (cat -A) and rc — this is the C1 receipt payload the L1 lands. {{REV}}""")
add("Mo60Executor52", "executor", f"""Mo60Executor52: same for the r59 count-c2 at {R59DATA}: exact stdout bytes + rc, run twice under different scratch dirs to show determinism. {{REV}}""")
add("Mo60Executor53", "executor", f"""Mo60Executor53: run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` and `grep -cE '^\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|' {LANE}/corpus/SOURCES.md`; return both outputs and the row count (mid-round census).""")
add("Mo60Executor54", "executor", f"""Mo60Executor54: run count-c1 at the current lane tip; return the exact line + rc (C1 progress probe; repeat once if the data has not landed yet). {{REV}}""")
add("Mo60Executor55", "executor", f"""Mo60Executor55: build the absent-set truth matrix: for the five frozen names run `git -C {LANE} cat-file -e` at {R59DATA}, {R59LAND}, and the current tip (path .ufo/waves/round-59/w1/<name>.md); return the 5x3 truth table with rc per cell.""")
add("Mo60Executor56", "executor", f"""Mo60Executor56: dead-name census: `grep -c 'c1-entering\\.txt' {LANE}/SCORECARD.md` and the same for c2-entering.txt at the entering rev, at {FREEZE}, and at the current tip (git show <rev>:SCORECARD.md); return the three counts per name plus how many tip occurrences carry the r60-correction: marker.""")
add("Mo60Executor57", "executor", f"""Mo60Executor57: hostile-tree battery at {FREEZE}: for each of the 13 trees run the tool (--artifacts-json from the counter's frozen map, materialized in scratch) and return the per-tree ok + first three reasons. {{REV}}""")
add("Mo60Executor58", "executor", f"""Mo60Executor58: boundary PoC re-run: build the evil-blob PoC repo (both tool paths) per the git-fixture rule under your scratch; run the r59 counter (materialized at {R59DATA}) and the r60 count-c2 at {FREEZE} against it; return marker-present/marker-absent evidence plus the counter lines. {{REV}}""")
add("Mo60Executor59", "executor", f"""Mo60Executor59: run `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`; list the round-60 scratch dirs under /fast/scratch/hyaku/mori-r60/ with sizes; return both (hygiene receipt).""")
add("Mo60Executor60", "executor", f"""Mo60Executor60: misroot probe: `git -C {FLEET} status --porcelain` (no pathspec); list any untracked file whose content names mori or round-60; return the listing and your per-file ownership guess (report only — never move or delete).""")
add("Mo60Executor61", "executor", f"""Mo60Executor61: selftest battery: run the three counters' --selftest and the tool's --selftest under your scratch TMPDIR; return all four lines + rc. {{REV}}""")
add("Mo60Executor62", "executor", f"""Mo60Executor62: builder determinism: export the lane tree at {FREEZE} (git archive or worktree) into scratch, run .ufo/waves/round-60/build-fixtures-r60.py there into a fresh trees-c2h, and byte-compare (diff -r) against the committed trees; return the diff result. {{REV}}""")

# ---- scribe (6) ----
add("Mo60Scribe71", "scribe", f"""Mo60Scribe71: draft three SOURCES rows (S561 Mo59Critic22 report, S562 Mo59Sentinel57 report, S563 Mo59Critic25 report — own-work, tier A, status mined, used-by corpus/knowledge/entry-claims-hardening-r60.md): read each report at {LANE}/.ufo/waves/round-59/w1/<name>.md, write the 11-cell row (no pipe chars inside cells; anchor = report path + line; teaches = one grounded benefit) and the <=25-word located Gate quote per row; return the exact rows + quotes.""")
add("Mo60Scribe72", "scribe", f"""Mo60Scribe72: draft row S564 for Mo59Sentinel58 as REJECTED (duplicate scope of S562's execution-boundary finding; flip condition: a distinct expect-tamper construction this round actually needs) with reason + flip in teaches; read the report first; return the exact row + Gate quote.""")
add("Mo60Scribe73", "scribe", f"""Mo60Scribe73: draft the knowledge entry corpus/knowledge/entry-claims-hardening-r60.md: one source: line per cited row (S561 S562 S563, artifact paths named), verified-at (freeze {FREEZE}), recheck (`python3 .ufo/waves/round-60/count-c2.py R`), coverage-map line; body: the H1-H5 and G1-G3 predicate table with the routed defect each closes (Mo59Critic22 D1-D4, Mo59Critic23 F1-F3, Mo59Critic25, Mo59Reviewer08 F1, Mo59Sentinel57/58 F1) and the no-false-negative evidence (real entry 13 claims / 13 spans / min span 12). Return the full markdown.""")
add("Mo60Scribe74", "scribe", f"""Mo60Scribe74: draft the round-60 lesson skeleton (Gate section: candidates considered, admitted S561-S563, rejected S564, spot-check pending; Mistakes rows: (a) class reference-drift — r59 report+SCORECARD cited dead evidence names c1-entering.txt/c2-entering.txt, captured-by none, fix = r60-correction: re-pointing + count-c1 dead-name arm + QUALITY 156; (b) class landing — w1-results.json and three late seat reports committed post-report in {R59LAND[:8]}, captured-by none, fix = final post-WAVE-DONE sweep duty; Wave w1 settlement section placeholder). Return full markdown.""")
add("Mo60Scribe75", "scribe", f"""Mo60Scribe75: draft the absent-set reconciliation table exactly in count-c1's grammar: 5-cell rows `| <name> | present|absent at {R59DATA[:8]} | present|absent at tip | late-committed|wrong-superseded | <pointer> |` with header; fill the truth cells from `git cat-file -e` (Mo59Critic29 and Mo59Reviewer16 present at {R59DATA[:8]} -> wrong-superseded; the other three absent there -> late-committed, pointer {R59LAND[:8]}); return the exact table bytes.""")
add("Mo60Scribe76", "scribe", f"""Mo60Scribe76: draft QUALITY criteria 156 and 157: 156 — every evidence pointer cited by a report or SCORECARD claim table must resolve at the cited revision before filing (sweep command included), motivated by the r59 dead-pointer defect; 157 — a verifier's failure reasons must route to the verdict (no orphan grammar class) and every claim must cover a distinct byte span, motivated by the r59 met-flip decertification; each cites its lesson/report and shows the red arm. Return the exact texts.""")

# ---- scout (4) ----
add("Mo60Scout81", "scout", f"""Mo60Scout81: instrument-surface recon: `git -C {LANE} diff --stat {ENTERING}..<current tip>` — name every file the round touched and confirm the instrument set is exactly tools/mori-entry-claims-check.py + the three counters + fixtures; flag anything else.""")
add("Mo60Scout82", "scout", f"""Mo60Scout82: sibling overlap scan: grep sibling corpora (kumitate, kotodama, souji, tabi) for entry-claims verification / counter-boundary hardening equivalents; report any overlap with mori's PROVINCE boundary (detection/report only).""")
add("Mo60Scout83", "scout", f"""Mo60Scout83: assimilation/considerthese pass: read {LANE}/considerthese/2026-10-26.md (absolute-host-path item) and /home/vgpnk/Projects/shokuknow/merge/mori/MERGE-REPORT.md; report whether any theme matches instrument-hardening or whether `Assimilation: none` is the honest line for this round.""")
add("Mo60Scout84", "scout", f"""Mo60Scout84: fresh-start defect ledger: list every routed defect from corpus/lessons/round-57-verifier-spotcheck.md, round-58-verifier-spotcheck.md and round-59-verifier-spotcheck.md with its current disposition pointer (fixed r59 / fixed r60 / open); return the table.""")

# ---- connector (2) ----
add("Mo60Connector91", "connector", f"""Mo60Connector91: cross-claim pattern scan: read the three counters + their frozen targets in the contract; find shared-pattern defects (token drift contract-vs-counter, revision pins disagreeing, receipt paths spelled differently between contract and counter); report findings per claim.""")
add("Mo60Connector92", "connector", f"""Mo60Connector92: cross-round defect classes: compare the routed defects of the round 57, 58 and 59 spot-checks; name recurring classes (instrument false-green, record/pointer drift) with one line each for the round-60 lesson Mistakes table.""")

# ---- revenger (4) ----
add("Mo60Revenger95", "revenger", f"""Mo60Revenger95: reconstruct the r59 C2 decertification chain from the Mo59Critic22/23/25 + Mo59Reviewer08 reports and give one verdict per class (semantically-empty, alias/vacuous spans, drift confound, grammar orphan) on whether the r60 instrument now rejects it — evidence per class.""")
add("Mo60Revenger96", "revenger", f"""Mo60Revenger96: commit archaeology of the dead pointers: when did c1-entering.txt/c2-entering.txt first appear as citations (git log -S on SCORECARD), was any file ever committed under those names, and which commit introduced the real control-*.txt names — return the timeline for the Mistakes row.""")
add("Mo60Revenger97", "revenger", f"""Mo60Revenger97: absent-set arrival reconstruction: from {R59LAND} and the w1 dir listing, derive which of the five seat files landed when (commit, timestamp) vs what the r59 report and lesson each claimed; return the reconciled timeline.""")
add("Mo60Revenger98", "revenger", f"""Mo60Revenger98: the r59 Sentinel57 F1 exploit chain step-by-step vs the r60 counters: (1) unpinned blob executes? (2) materialize join escapes? (3) expect.txt trusted? — for each step give the r59 behavior and the r60 kill with code line pointers.""")

# ---- simplifier (4) ----
add("Mo60SimplifierA1", "simplifier", f"""Mo60SimplifierA1: read {LANE}/.ufo/waves/round-60/count-c2.py; propose minimal deletions that preserve the frozen predicate semantics (dead branches, duplicate failed-append tokens); report only — the committed bytes are frozen.""")
add("Mo60SimplifierA2", "simplifier", f"""Mo60SimplifierA2: same audit for count-c1.py and count-c3.py (unused variables, the selftest good_row reuse); report proposals only.""")
add("Mo60SimplifierA3", "simplifier", f"""Mo60SimplifierA3: same audit for tools/mori-entry-claims-check.py (unused copy_prefix param, unused imports, the artifacts-json CLI path unused by the counter); report proposals only.""")
add("Mo60SimplifierA4", "simplifier", f"""Mo60SimplifierA4: builder audit: {LANE}/.ufo/waves/round-60/build-fixtures-r60.py — the h04 double-replace leftover and the expect/EXPECTS duality; propose the minimal cleanup for a future builder; report only.""")

assert len(ITEMS) == 64, len(ITEMS)
names = [i["name"] for i in ITEMS]
assert len(set(names)) == 64
roles = {}
for i in ITEMS:
    roles[i["role"]] = roles.get(i["role"], 0) + 1
attack = roles.get("reviewer", 0) + roles.get("critic", 0) \
    + roles.get("mutation-tester", 0) + roles.get("sentinel", 0)
print("roles:", json.dumps(roles, sort_keys=True))
print("attack share: %d/64" % attack)
assert attack * 4 >= 64
spec = {
    "wave": WAVE,
    "reportDir": REPORT_DIR,
    "context": CONTEXT,
    "items": ITEMS,
}
with open(".ufo/waves/round-60/w1-spec.json", "w") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print("wrote .ufo/waves/round-60/w1-spec.json")
