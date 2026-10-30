#!/usr/bin/env python3
"""Build the round-61 w1 spec (64 seats, policy v2) — build/falsify items for
claims C1 (calibration: gate registry r52-60), C2 (freshness: PSI v7.3 recheck
ledger), C3 (operability: counter execution boundary v2) plus the frontier
step. Run from the lane repo root. Emits .ufo/waves/round-61/w1-spec.json."""
import json
from pathlib import Path

WAVE = "mori-r61-w1"
REPORT_DIR = ".ufo/waves/round-61/w1"
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
FREEZE = "7370a731abcafc4c803111de7c22cd6264d63be1"
ENTERING = "325f7e639916fcbc77fa2ec7475951a1b86bb1cb"
R60FREEZE = "ac496c7cde8cad965079858accae3bedfe4a73f2"

CONTEXT = f"""# mori round 61 — one v2 build/falsify wave (64 seats)
Lane: mori-shokunin (森, fleet and host observability: fleet liveness, wave settlement, kill and OOM
events, resource runway; detection and report only). Lane repo: {LANE}. Fleet root: {FLEET}.
L1: MoriR61. Frozen contract: {LANE}/.ufo/waves/round-61/contract.md — read it first. Freeze revision
{FREEZE} (controls + selftests committed; amendments barred: no seat may propose a counter/contract
change — report findings instead); entering revision {ENTERING}. Frozen counters:
{LANE}/.ufo/waves/round-61/count-c1.py (C1 gate registry r52-60 over gate-manifest.json, 25 paths),
count-c2.py (C2 PSI v7.3 recheck ledger; pointer floor 40; live run needs --floor default),
count-c3.py (C3 boundary v2; r60 red-before pinned at {R60FREEZE}). Pinned v7.3 copies:
{LANE}/corpus/evidence/sources-r61/ (psi.rst, psi.c, psi_types.h, cgroup-v2.rst, Kconfig,
kernel-parameters.txt; sha256s frozen in count-c2.py).

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Write only your
own report under {LANE}/.ufo/waves/round-61/w1/. Do not edit production files (SKILL.md, corpus/,
SCORECARD.md, LOG.md, tools/), the registry, or any VCS state; return findings and draft blocks only —
the L1 integrates. Do not write to the fleet repo or sibling repos. Use absolute paths for every file
access. Never run a mutating git/jj command anywhere in the lane or fleet; a fixture repo must be
created at an explicit scratch path (`D=$(mktemp -d -p <your scratch>) && git -C "$D" init -q`), every
later git call must name `git -C "$D"`, and the throwaway identity `t <t@t>` is valid ONLY inside such
repos. Never call `task`; you are a leaf (an executor may spawn one read-only labrat probe for a
falsifiable hypothesis; nothing else spawns). Never message agent://all.

Scratch root for this round is `$HYAKU_SCRATCH/mori-r61/<your seat name>/` (default
`/fast/scratch/hyaku`): create it with mkdir -p, set TMPDIR there, pass --scratch to every counter,
clean it before yielding (trap/finally), and copy any small receipt into your report first. `/tmp` is
for files under 50 MB only and is never citable evidence. Check
`{FLEET}/scripts/hyaku/disk-guard.sh status` before heavy work; on ENOSPC report the free space you saw
and do not re-run until status is green. One lightweight clone (`git clone --shared`) or `git worktree`
per seat only if needed; prefer `git show`/read-only reads.

Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help your item — read
`/home/vgpnk/.omp/agent/RULES.md` first (official channels only) and record tool/version/channel/reason
in your report. Pacman transactions are PAUSED host-wide: never run pacman; use uv tool / npx / an
official binary in ~/.local/bin. Never pipe an unverified remote script into a shell. Never expose
secrets, session material or private URLs. Detection/report only — no remediation, no service or config
changes, no provider-death inference. Frozen claims, counters, predicates and kill rules are immutable
after this freeze; if you can defeat one, that is a finding to report, not a fix to apply.
"""

ITEMS = []
GS_PATH = Path.home() / ".agents/skills/godspeed/directive.md"
try:
    GS = GS_PATH.read_text()
except OSError:
    GS = ""

BOUNDS = (" Work read-only; return concise findings with exact evidence "
          "(commands, outputs, path:line pointers). No commits, no VCS "
          "mutation, no fleet/sibling writes.")


def add(name, role, text):
    lead = "/skill:godspeed\n" + GS + ("\n" if GS and not GS.endswith("\n") else "")
    ITEMS.append({"name": name, "role": role, "prompt": lead + text + BOUNDS})


REV = (f"Read {LANE}/.ufo/waves/round-61/contract.md first (freeze {FREEZE}, "
       f"entering {ENTERING}).")

REGROWS = ("Put every drafted row on ONE line each inside a fenced block in your report, "
           "exact 8 cells: | name | kind | entry | verdict map | self-test | pinned values | "
           "write scope | owner |. The entry cell names the artifact path verbatim. The "
           "self-test cell names the runnable --selftest command AND the measured output line "
           "(run it once at the landing commit, materialized to your scratch). The owner cell "
           "names the landing round's L1 (e.g. MoriR53) or `hyaku closure` for spotcheck-only "
           "artifacts. Rows are drafts; the L1 appends them to SKILL.md.")

# ---- scribes: registry rows (6) ----
add("Mo61ScribeReg5253", "scribe", f"""Mo61ScribeReg5253: draft the SKILL.md gate-registry rows for the round-52 and round-53
gates in {LANE}/.ufo/waves/round-61/gate-manifest.json (4 paths, rounds 52-53). For each: materialize
the artifact at its landing commit (`git show <landing>:<path>` into your scratch), read its docstring,
argparse surface and selftest; run the selftest once (TMPDIR=<your scratch>, --scratch where taken) and
record the measured output line; check where LOG.md round 52/53 names it. {REGROWS} {{REV}}""")
add("Mo61ScribeReg5455", "scribe", f"""Mo61ScribeReg5455: same task as Mo61ScribeReg5253 for the round-54 and round-55 gates
(4 paths in gate-manifest.json, rounds 54-55). {REGROWS} {{REV}}""")
add("Mo61ScribeReg5657", "scribe", f"""Mo61ScribeReg5657: same task as Mo61ScribeReg5253 for the round-56 and round-57 gates
(7 paths: r56 count-c1/count-c2 plus tools/mori-vote-bind.py and tools/mori-driver-liveness.py; r57
count-c1/count-c2 plus .ufo/waves/round-57/verify-c2-source.py). {REGROWS} {{REV}}""")
add("Mo61ScribeReg5859", "scribe", f"""Mo61ScribeReg5859: same task as Mo61ScribeReg5253 for the round-58 and round-59 gates
(6 paths: r58 count-c1/count-c2; r59 count-c1/count-c2 plus tools/mori-register-check.py and
tools/mori-settlement-scan.py). {REGROWS} {{REV}}""")
add("Mo61ScribeReg60", "scribe", f"""Mo61ScribeReg60: same task as Mo61ScribeReg5253 for the round-60 gates (4 paths:
count-c1.py, count-c2.py, count-c3.py, tools/mori-entry-claims-check.py). For count-c3 note in the
verdict-map cell that round 61 decertified its composition (r60 closure defect 2-3) — the row
registers the r60 artifact as it is, defects named. {REGROWS} {{REV}}""")
add("Mo61ScribeRegReview", "scribe", f"""Mo61ScribeRegReview: cross-check pass over the gate registry drafts: after the five
drafters' reports exist under {LANE}/.ufo/waves/round-61/w1/, verify every one of the 25 manifest paths
has exactly one drafted row, each with 8 non-empty cells, a --selftest spelling, an owner, and an entry
path that resolves at {FREEZE} (`git cat-file -e`). Assemble the full 25-row draft (manifest order)
into your report as ONE fenced block, fixing only mechanical gaps you can verify yourself (rerun the
selftest; do not invent a cell you cannot measure — mark it `TBD(<why>)` instead). {{REV}}""")

# ---- scribes: PSI ledger (3) + sources ----
PTRAWS = ("Draft one ledger row per assigned pointer: | <file>:<start> | same|moved|changed | "
          "<loc or -> | `<quote>` |. The quote must be a VERBATIM <=25-word span (>=8 distinct "
          "bytes, no two rows sharing a quote) copied from the pinned v7.3 copy at the stated "
          "location: status same -> the enumerated range itself; moved -> the copy line where the "
          "same words now live (loc names it); changed -> the words are gone; quote the nearest "
          "v7.3 wording that now governs the same claim (loc names its line). Read the r24 entry "
          "context around each pointer first so the quote carries the claim the pointer supports. "
          "Put rows in a fenced block in your report, one line per row, plus a one-line note per "
          "changed/moved row naming what drifted.")
add("Mo61ScribePsi1", "scribe", f"""Mo61ScribePsi1: draft ledger rows for the psi.rst and psi.c pointers enumerated from
{LANE}/corpus/knowledge/system-pressure-r24.md (regex:
'(psi\\.rst|psi\\.c|psi_types\\.h|cgroup-v2\\.rst|Kconfig|kernel-parameters\\.txt):[0-9]+(-[0-9]+)?',
dedup, normalize to <file>:<start>[-<end>]). Yours: every pointer whose file is psi.rst or psi.c.
Pinned v7.3 copies: {LANE}/corpus/evidence/sources-r61/. {PTRAWS} {{REV}}""")
add("Mo61ScribePsi2", "scribe", f"""Mo61ScribePsi2: same as Mo61ScribePsi1 for the remaining files: psi_types.h,
cgroup-v2.rst, Kconfig, kernel-parameters.txt pointers from
{LANE}/corpus/knowledge/system-pressure-r24.md. {PTRAWS} {{REV}}""")
add("Mo61ScribePsiProv", "scribe", f"""Mo61ScribePsiProv: draft the ledger entry shell
{LANE}/corpus/knowledge/psi-v73-recheck-r61.md: frontmatter trio (source: the six new S-rows plus
S090-S095 as the v7.2 side; verified-at: 2026-10-30 with the fetch note; recheck: next kernel
release), a scope paragraph (what the ledger covers: the 47 enumerated v7.2 line pointers of
system-pressure-r24.md; what it does not: prose anchors outside the six files), status definitions
(same/moved/changed as the counter verifies them), and the `## Gate` block ground for rows S565-S570:
per row the URL, access date 2026-10-30, and a <=25-word located quote from the pinned copy. Also
draft the six SOURCES.md rows (11 cells, no literal or escaped pipes in any cell, status mined,
recheck on-release or 180d, used-by corpus/knowledge/psi-v73-recheck-r61.md) in a second fenced block.
{{REV}}""")
add("Mo61ScribePsiQa", "scribe", f"""Mo61ScribePsiQa: mechanical QA over all drafted ledger rows (Psi1 + Psi2 reports
under {LANE}/.ufo/waves/round-61/w1/): parse each row with count-c2's ROW regex, check <=25 words,
>=8 distinct bytes, pairwise-distinct quotes, anchor normalization matches the enumeration, and no
cell carries a literal or escaped pipe; verify every quote byte-present in the pinned copy at the
stated location (small script, committed in your report). Output: the corrected full 47-row block, one
line per row, ready for the L1 to land, with a per-row status tally (same/moved/changed). {{REV}}""")
add("Mo61ExecFetch", "executor", f"""Mo61ExecFetch: verify the pinned copies are what the URLs serve: re-fetch the six files
at tag v7.3 (git.kernel.org plain URLs, same paths as the copies under {LANE}/corpus/evidence/sources-r61/)
into your scratch, sha256 each, byte-compare with the committed copies, and record per-file: URL,
bytes, sha256, match verdict, access timestamp. If any byte differs, that is a HIGH finding (the C2
pins are frozen) — report it, do not fix. {{REV}}""")

# ---- dry-run integration seats ----
add("Mo61ExecLedgerDry", "executor", f"""Mo61ExecLedgerDry: dry-run C2 before the L1 lands data: clone the lane with
`git clone --shared` into your scratch, checkout {FREEZE} (read-only operations only), write the
drafted ledger (from Mo61ScribePsiProv/Psi1/Psi2 reports) + the six registry rows + copies at the same
paths IN THE CLONE ONLY, commit there with the throwaway identity, then run
`python3 {LANE}/.ufo/waves/round-61/count-c2.py <clone-rev> --repo <clone> --scratch <your scratch> --floor 40`.
Report the full output; for every failed anchor, name the exact row defect. Do not touch the real lane.
{{REV}}""")
add("Mo61ExecLedgerFix", "executor", f"""Mo61ExecLedgerFix: after Mo61ExecLedgerDry's report exists, produce the corrected
ledger: for every anchor its dry-run failed, fix the row (relocate the quote in the pinned copy, fix
the status, or re-locate moved words) and re-run the counter on an updated scratch clone until it
prints met or the residual failures are defects you can name precisely. Output: the final full ledger
row block + the met line. {{REV}}""")
add("Mo61ExecRegDry", "executor", f"""Mo61ExecRegDry: dry-run C1 before the L1 lands data: clone the lane with
`git clone --shared` into your scratch, checkout {FREEZE}, append Mo61ScribeRegReview's 25-row draft to
the SKILL.md gate-registry tables IN THE CLONE ONLY, commit there (throwaway identity), then run
`python3 {LANE}/.ufo/waves/round-61/count-c1.py <clone-rev> --repo <clone> --scratch <your scratch>`.
Report the full output and every failing gate with its defect. {{REV}}""")
add("Mo61ExecC3Run", "executor", f"""Mo61ExecC3Run: run `python3 {LANE}/.ufo/waves/round-61/count-c3.py {FREEZE} --scratch
<your scratch>` at the freeze and byte-compare with a fresh run at the current lane tip; also run it at
{ENTERING} and byte-compare with
{LANE}/.ufo/waves/round-61/evidence/control-c3-do-nothing.txt (modulo rev). Confirm the r60hole arm
still holds at {R60FREEZE} bytes and that no arm prints ok from a literal. {{REV}}""")
add("Mo61ExecReplay", "executor", f"""Mo61ExecReplay: replay all three controls at {ENTERING} (`python3
{LANE}/.ufo/waves/round-61/count-c{{1,2,3}}.py {ENTERING} --scratch <your scratch>`; for C1 pass
--manifest {LANE}/.ufo/waves/round-61/gate-manifest.json) and byte-compare each with the committed
{LANE}/.ufo/waves/round-61/evidence/control-c*-do-nothing.txt files (modulo rev). Then run the three
--selftests and byte-compare with evidence/selftest-c*.txt. Report any drift. {{REV}}""")
add("Mo61ExecSourcesRows", "executor", f"""Mo61ExecSourcesRows: validate the drafted SOURCES rows before any append: build a
scratch mirror of the lane corpus (copy corpus/ + insert Mo61ScribePsiProv's six rows into the
registry table of the COPY), then run
`{FLEET}/scripts/sources-census.sh validate --file <copy>/corpus/SOURCES.md` and the manual census
commands from {FLEET}/CORPUS.md (row count, malformed rows, enum violations, duplicate ids). Report
exit codes and every finding; flag any cell containing a literal or escaped pipe. {{REV}}""")
add("Mo61ExecQuarantine", "executor", f"""Mo61ExecQuarantine: the mori absent-defect-register slice is
{LANE}/.ufo/waves/round-61/assimilation/quarantine-slice (S244, S262, S268 — read-only register at
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md; never edit it).
Re-derive each verdict this round: fetch the cited source (or its arXiv companion for S244 per round-55),
attempt to locate a quote, and output verdict PRESENT (with the anchor you located) / UNVERIFIABLE /
FABRICATED per row. These rows were adjudicated r54-r55; your job is the fresh verdict + any drift.
No adoption — the lane adopts nothing from merge/mori this round (94 id collisions:
{LANE}/.ufo/waves/round-61/assimilation/collisions). {{REV}}""")
add("Mo61ExecCensusMid", "executor", f"""Mo61ExecCensusMid: run
`{FLEET}/scripts/sources-census.sh validate --root {FLEET} mori` at the freeze and record the full
output (expect exit 0, standing W04 set) plus `grep -c '^| S[0-9]' {LANE}/corpus/SOURCES.md` (337) into
your report — this is the census-before receipt. {{REV}}""")
add("Mo61ExecGodspeed", "executor", f"""Mo61ExecGodspeed: verify the dispatch payload carries the godspeed directive bytes:
read {LANE}/.ufo/waves/round-61/w1-dispatch.json and for each of the 64 tasks confirm the task text
starts with `/skill:godspeed` AND contains the directive's distinctive body (e.g. its final axis line).
Report per-seat ok/missing as a 64-line tally plus a summary (this is the r60 dispatch-payload defect
check). Read-only; do not rewrite the dispatch. {{REV}}""")

# ---- scouts / connectors / revenger / simplifier ----
add("Mo61ScoutTableShape", "scout", f"""Mo61ScoutTableShape: per-surface recon for the registry drafters: from
{LANE}/SKILL.md gate-registry tables, extract 3 exemplar rows (r44/r50/r51), the exact header cells,
and the conventions that made r44-r51 rows conformant (kind vocabulary, self-test spelling, pinned
values style, write scope, owner). Output a style sheet the drafters can follow. {{REV}}""")
add("Mo61ScoutPsiNovelty", "scout", f"""Mo61ScoutPsiNovelty: novelty sweep for the PSI ledger: grep {LANE}/corpus/knowledge/
for psi/pressure claims (system-pressure-r24.md is the source entry — the ledger rechecks it; anything
ELSE already holding v7.3 PSI ground?). Also read registry rows S090-S095 and S520 and report what the
new S565-S570 rows must say to not duplicate them (different artifact: v7.3 raw .rst/.c files vs
rendered html). Output: overlap verdict + per-row differentiation note. {{REV}}""")
add("Mo61ScoutAnchorMap", "scout", f"""Mo61ScoutAnchorMap: bounded data walk feeding the ledger drafters: enumerate the
pointers exactly as count-c2 does (read the NAMES regex from
{LANE}/.ufo/waves/round-61/count-c2.py), and for each of the 47 write one line: pointer | the r24
claim it supports (<=15 words from the entry) | the v7.2-side context. This is the checklist the
scribes work from; do not draft rows yourself. {{REV}}""")
add("Mo61ScoutFloor", "scout", f"""Mo61ScoutFloor: independent selftest floor: run all three counter selftests
(`python3 {LANE}/.ufo/waves/round-61/count-c1.py --selftest`; count-c2 with --selftest --floor 1;
count-c3 --selftest) under your own scratch and byte-compare the pass/fail tallies with
{LANE}/.ufo/waves/round-61/evidence/selftest-c*.txt. Report any divergence. {{REV}}""")
add("Mo61ScoutS090", "scout", f"""Mo61ScoutS090: read registry rows S090-S095, S145-S146 and S520 of
{LANE}/corpus/SOURCES.md plus {LANE}/corpus/knowledge/system-pressure-r24.md in full; output the
v7.2-side map the ledger frontmatter needs: per pinned file (psi.rst, psi.c, psi_types.h,
cgroup-v2.rst, Kconfig, kernel-parameters.txt) the S-row that backs its v7.2 side, the URL pattern for
the v7.3 twin, and any r24 claim that cites a file with NO pinned copy (pointer-for-next-round rows).
{{REV}}""")
add("Mo61ConnSibling", "connector", f"""Mo61ConnSibling: sibling-overlap scan: do tsukuroi/kama/kumitate/souji hold PSI
reading, kernel-source recheck ledgers, gate registries or vote binders that overlap the round-61
surfaces (grep their tools/ and corpus/)? For each hit: path, what they claim, whether mori's surface
(report-only PSI ledger, own-gate registry, own-counter boundary) conflicts or stays lane-internal.
Cite sibling paths; do not absorb. {{REV}}""")
add("Mo61ConnConsider", "connector", f"""Mo61ConnConsider: read {LANE}/considerthese/ (2026-10-19..26 files) and name the
latest still-unimplemented proposal that fits the round-61 surfaces (instrument hardening / registry /
freshness rechecks), with a one-paragraph grounding plan; and check
/home/vgpnk/Projects/shokuknow/merge/mori/MERGE-REPORT.md for ONE theme that would have fit C2 had the
id collisions not blocked adoption (they did: see assimilation/collisions, 94 rows) — say which theme
and why it is deferred. Neither lands this round; this is the assimilation/considerthese report line.
{{REV}}""")
add("Mo61RevPoc", "revenger", f"""Mo61RevPoc: reconstruct Mo60Reviewer13's proof end-to-end: in a scratch clone at
{R60FREEZE}, build the smallest state where the r60 count-c3 prints its exact met line while the
count-c1 blob sha differs from its pin (their construction: clone with count-c1 sha != PIN_C1;
`failed=g2_escape_written` beside containment=ok). Verify the r61 counter's r60hole static arm
correctly asserts this hole over the frozen bytes, and report any respect in which the static arm's
story diverges from the live PoC. {{REV}}""")
add("Mo61RevC2", "revenger", f"""Mo61RevC2: bypass hunt on the frozen count-c2: craft (in scratch fixtures) ledger
rows that satisfy every arm while lying — a quote assembled from two copy lines; a moved row whose loc
names a line inside the ORIGINAL range; a changed row quoting v7.3 words that appear far from the
claim; pointers on lines whose content the r24 entry mis-cites. Report every construction the counter
accepts with the exact bytes. {{REV}}""")
add("Mo61RevC1", "revenger", f"""Mo61RevC1: bypass hunt on the frozen count-c1: registry rows that pass while lying —
entry cell naming the path inside a longer token; two live rows where one is marked superseded but is
the only real one; owner cell whitespace-only; a self-test cell naming --selftest for a tool that has
none (the row for a tool without --selftest mode). Report which lies the counter catches and which it
structurally cannot (scope boundary, named). {{REV}}""")
add("Mo61SimplC1", "simplifier", f"""Mo61SimplC1: read {LANE}/.ufo/waves/round-61/count-c1.py and count-c2.py end to end;
report dead code, unused arms, or needless complexity (advisory only — frozen bytes; simplifications
route to a future round). One paragraph each, no edits. {{REV}}""")
add("Mo61SimplC3", "simplifier", f"""Mo61SimplC3: read {LANE}/.ufo/waves/round-61/count-c3.py end to end; report dead
code, unused arms, or needless complexity (advisory only — frozen bytes). Also verify the docstring's
arm list matches the code. One paragraph, no edits. {{REV}}""")
add("Mo61ScribeLesson", "scribe", f"""Mo61ScribeLesson: draft the round-61 lesson skeleton
({LANE}/.ufo/waves/round-61/w1/DraftLessonR61.md): `## Gate` (candidates = the six S-rows with
URL/date/quote; admitted/rejected with reasons), `## Mistakes` (mine the r60 godspeed-bytes-absent
dispatch defect: class landing · evidence .ufo/waves/round-60 dispatch · captured-by none · fix =
embed + verify at dispatch time), and a `## Wave w1` section skeleton for the integrated findings.
Draft only; the L1 owns the file. {{REV}}""")
add("Mo61ScribeLogScore", "scribe", f"""Mo61ScribeLogScore: draft the LOG.md `## Round 61` entry and the SCORECARD.md
round-61 section (claim table with counting commands, before-cells from
{LANE}/.ufo/waves/round-61/evidence/control-*.txt, after-cells marked AT-DATA pending) as report
drafts. Follow the r58-r60 sections' shape exactly. Draft only. {{REV}}""")
add("Mo61ScribeQuality", "scribe", f"""Mo61ScribeQuality: from the fresh-start reading (r58-r60 closures and
{LANE}/corpus/lessons/round-58/59/60-verifier-spotcheck.md), draft 1-2 QUALITY.md criteria this round's
evidence grounds (e.g. a counter's printed tokens must each be bound to a measured boolean — grounded
in r60 routed defect 2 and the r61 C3 repair), each citing the lesson/round that produced it. Draft
only. {{REV}}""")

# ---- reviewers (8) ----
add("Mo61Reviewer01", "reviewer", f"""Mo61Reviewer01: C1 re-derivation at the freeze: run
`python3 {LANE}/.ufo/waves/round-61/count-c1.py {FREEZE} --scratch <your scratch>` and report the
output; confirm it reads unmet (registry rows r52-60 do not exist yet) and that the same command with
--manifest {LANE}/.ufo/waves/round-61/gate-manifest.json (the on-disk fallback) still reads unmet with
missing=25. Also confirm the committed control equals a fresh run at {ENTERING} modulo rev. {{REV}}""")
add("Mo61Reviewer02", "reviewer", f"""Mo61Reviewer02: C2 re-derivation at the freeze: run
`python3 {LANE}/.ufo/waves/round-61/count-c2.py {FREEZE} --scratch <your scratch>` — expect unmet
entry_absent with pointers=47 enumerated; confirm the pointer set matches
Mo61ScoutAnchorMap's checklist and the committed control at {ENTERING} modulo rev. {{REV}}""")
add("Mo61Reviewer03", "reviewer", f"""Mo61Reviewer03: C3 re-derivation at the freeze: run
`python3 {LANE}/.ufo/waves/round-61/count-c3.py {FREEZE} --scratch <your scratch>`; confirm unmet with
livepins FAIL and r60hole ok; independently verify the r60 pin: `git show
ac496c7c:.ufo/waves/round-60/count-c3.py | sha256sum` equals the counter's R60_SHA, and the PIN_C1/
PIN_C2 constants equal the sha256 of the two sibling counters at {FREEZE}. {{REV}}""")
add("Mo61Reviewer04", "reviewer", f"""Mo61Reviewer04: C1 hostile-tree audit: in a scratch clone, build three lying-registry
variants (a row whose self-test cell names --selftest for a tool without one; a whitespace-only owner;
two live rows separated by a superseded marker) and run count-c1 against each — report exactly which
lies are caught and which pass (named scope boundary vs defect). {{REV}}""")
add("Mo61Reviewer05", "reviewer", f"""Mo61Reviewer05: C2 no-false-negative audit: once the ledger draft exists, apply three
benign mutations in a scratch clone (reorder rows; fix a typo in the ledger prose; rewrap one quote's
whitespace) and confirm the counter still meets — a benign change that flips met is a counter defect.
{{REV}}""")
add("Mo61Reviewer06", "reviewer", f"""Mo61Reviewer06: ledger quote spot-check: mechanically verify 12 drafted ledger rows
(pick every 4th): quote byte-presence in the pinned copy at the stated location, <=25 words, >=8
distinct bytes, pairwise distinct, status semantics correct (same/moved/changed). Report per-row
verdicts. {{REV}}""")
add("Mo61Reviewer07", "reviewer", f"""Mo61Reviewer07: manifest completeness audit: from {LANE}/LOG.md rounds 52-60 and the
wave directories, enumerate every gate/checker artifact those rounds landed; diff against
{LANE}/.ufo/waves/round-61/gate-manifest.json (25 paths). Report any landed gate artifact the manifest
misses (naming its landing commit) or any manifest entry that is not a gate. {{REV}}""")
add("Mo61Reviewer08", "reviewer", f"""Mo61Reviewer08: selftest-scrutiny: map each selftest case of the three counters to
the arm it claims to exercise (read the case lists); name any arm with no case and any case that does
not exercise what its name says. {{REV}}""")
add("Mo61Reviewer09", "reviewer", f"""Mo61Reviewer09: wave-shape conformance: from
{LANE}/.ufo/waves/round-61/w1-dispatch.json report seat count, per-role counts, attack share
(reviewer+critic+mutation-tester+sentinel+labrat+revenger)/total, connector count, duplicate names,
unknown roles; confirm policy v2 band 64-128 applies (per the dispatch metadata). {{REV}}""")

# ---- critics (7) ----
add("Mo61Critic21", "critic", f"""Mo61Critic21: cheapest-met attack on C1: build the smallest scratch-clone state
where count-c1 prints met WITHOUT the claimed work (25 fabricated rows with filler cells; rows naming
paths that exist but whose selftests were never run). If any construction meets, that is a kill —
report exact bytes. {{REV}}""")
add("Mo61Critic22", "critic", f"""Mo61Critic22: cheapest-met attack on C2: smallest state where count-c2 meets
without a real recheck (one quote reused across anchors via moved-loc games; a ledger that rows only
the subset of pointers the counter's regex catches while the entry gains pointer-like strings the
regex misses — can the enumeration be gamed from the SOURCE side? the source entry is frozen bytes,
reason about it). Report kills with exact bytes. {{REV}}""")
add("Mo61Critic23", "critic", f"""Mo61Critic23: cheapest-met attack on C3: met-composition mutants (rename
TOKEN_MAP keys; drop c1_ok; make blobrefusal a constant) applied in scratch copies and driven through
the counter's own selftest arms — which mutants does the selftest itself catch (the self-mutant case),
and which survive? {{REV}}""")
add("Mo61Critic24", "critic", f"""Mo61Critic24: whole-contract falsification sweep: find the cheapest committed-revision
path where ALL THREE counters print met without the claimed work (empty tree, entering rev, counters-
only tree). Report per-claim why the do-nothing arms hold or break. {{REV}}""")
add("Mo61Critic25", "critic", f"""Mo61Critic25: freeze-integrity: contract vs counters — every frozen met token in
{LANE}/.ufo/waves/round-61/contract.md must be printed by its counter; every pinned sha in the
contract must appear in a counter or evidence file; amendment history (1-2) must be pre-seat. Report
any mismatch. {{REV}}""")
add("Mo61Critic26", "critic", f"""Mo61Critic26: fresh-start adversarial review: for each of the three claims, name the
do-nothing control and check it cannot reach the after-state (the three control receipts committed);
then check each claim against the r58-60 rejection causes (unprintable target tokens, controls that
pass, instruments decertified by their own wave) and report whether any cause recurs. {{REV}}""")
add("Mo61Critic27", "critic", f"""Mo61Critic27: assimilation ruling sanity: with 94 id collisions
({LANE}/.ufo/waves/round-61/assimilation/collisions), CORPUS.md §10 says mass id drift → L0 question +
adopt nothing. Verify the collision extraction used the 0-3-space-tolerant pattern (the corpus census
clause) and that the count is right (recompute); name what a false-green would have looked like.
{{REV}}""")

# ---- mutation-testers (8) ----
MUT = ("Drive each mutant through the counter's --selftest and at least one committed control/hostile "
       "state in your scratch; a mutant that survives every committed witness is a ROUTED DEFECT (the "
       "arm has no witness), not a fix — report the kill table.")
add("Mo61MutC1a", "mutation-tester", f"""Mo61MutC1a: mutate {LANE}/.ufo/waves/round-61/count-c1.py in scratch copies:
drop the dup arm; drop the thin (empty-cell) arm; drop the noselftest arm. {MUT} {{REV}}""")
add("Mo61MutC1b", "mutation-tester", f"""Mo61MutC1b: mutate count-c1.py in scratch copies: accept any row kind (skip the
header match, parse ALL markdown rows); treat superseded rows as live; skip the unres arm. {MUT}
{{REV}}""")
add("Mo61MutC2a", "mutation-tester", f"""Mo61MutC2a: mutate {LANE}/.ufo/waves/round-61/count-c2.py in scratch copies:
drop span_small; drop quote_dup; drop the anchor set-equality (rows>=pointers instead). {MUT} {{REV}}""")
add("Mo61MutC2b", "mutation-tester", f"""Mo61MutC2b: mutate count-c2.py in scratch copies: drop the copy sha pins; accept
status loc = anchor for moved; drop the sources>=4 arm; drop provenance. {MUT} {{REV}}""")
add("Mo61MutC3a", "mutation-tester", f"""Mo61MutC3a: mutate {LANE}/.ufo/waves/round-61/count-c3.py in scratch copies:
drop c1_ok from met; rename TOKEN_MAP keys without updating fmt; make blobrefusal constant True.
{MUT} {{REV}}""")
add("Mo61MutC3b", "mutation-tester", f"""Mo61MutC3b: mutate count-c3.py in scratch copies: EXPECT_PIN check off;
tamper-acceptance off; livepins leniency (any sha). {MUT} {{REV}}""")
add("Mo61MutC2c", "mutation-tester", f"""Mo61MutC2c: mutate count-c2.py row grammar in scratch copies: accept quotes
without backticks; accept extra table columns; accept anchor case differences. {MUT} {{REV}}""")
add("Mo61MutC1c", "mutation-tester", f"""Mo61MutC1c: mutate count-c1.py parse layer in scratch copies: require the header
cells in different order (does the registry table variant break?); strip cells before compare vs not
(whitespace games). {MUT} {{REV}}""")

# ---- sentinels (3) ----
add("Mo61Sentinel41", "sentinel", f"""Mo61Sentinel41: execution-boundary probe: can any committed tree make the r61
counters execute attacker bytes? Audit every subprocess/exec site in the three counters; drive
count-c3's livepins arm with a scratch repo whose count-c1.py blob is hostile — confirm it is only
hashed, never run. Report any reachable execution of repo-supplied bytes. {{REV}}""")
add("Mo61Sentinel42", "sentinel", f"""Mo61Sentinel42: secrets/credential scan of everything new this freeze:
{LANE}/.ufo/waves/round-61/ and {LANE}/corpus/evidence/sources-r61/ — grep for tokens, keys, session
material, private URLs; confirm the v7.3 copies are pristine kernel sources (spot-open 3 files). {{
REV}}""")
add("Mo61Sentinel43", "sentinel", f"""Mo61Sentinel43: input-hardening probe on the counters: catastrophic regex
backtracking on count-c2's NAMES/ROW patterns (hostile ledger/source bytes in scratch); path traversal
via manifest cells in count-c1 (a manifest entry naming ../../secrets); unbounded memory on a 100 MB
ledger. Report crashes/hangs with repro bytes; a hang is a HIGH finding (frozen counters run in
closures). {{REV}}""")

# ---- labrats (2) ----
add("Mo61LabPressure", "executor", f"""Mo61LabPressure: falsifiable probe for the C2 ledger's live relevance: read
/proc/pressure/{{cpu,memory,io,irq}} twice ~10s apart (read-only) and test whether `total` advances and
whether avg10 can move without total moving (the r24 K4/K5 limits). Falsifiable hypothesis: the
v7.3-pinned semantics match this host's 7.2 behavior. Report numbers, no remediation, no
interpolation beyond the two reads. {{REV}}""")
add("Mo61LabDeterminism", "executor", f"""Mo61LabDeterminism: run count-c2 --selftest --floor 1 and count-c1 --selftest
three times each under three different scratch dirs; every tally must be byte-identical. Falsifiable
hypothesis: the selftests are deterministic (r25 lesson: nondeterministic fixtures are routed defects).
Report the three outputs. {{REV}}""")

assert len(ITEMS) == 64, len(ITEMS)

spec = {"wave": WAVE, "reportDir": REPORT_DIR, "context": CONTEXT, "items": ITEMS}
out = Path(".ufo/waves/round-61/w1-spec.json")
out.write_text(json.dumps(spec, indent=1))
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print("wrote", out, len(ITEMS), "items")
print(json.dumps(roles, sort_keys=True))
attack = roles.get("reviewer", 0) + roles.get("critic", 0) + roles.get("mutation-tester", 0) \
    + roles.get("sentinel", 0) + roles.get("labrat", 0) + roles.get("revenger", 0)
print(f"attack share {attack}/64 = {attack / 64:.0%}")
