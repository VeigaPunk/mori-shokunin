#!/usr/bin/env python3
"""Build the round-79 wave spec (13 seats -> 12 here) for ufo-swarm-wave validation."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
WAVE = ".ufo/waves/round-79/w1"
SCRATCH = "/fast/scratch/hyaku/mori-r79"

GODSPEED = """\
/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = GODSPEED + f"""
# Goal
mori round 79 (attempt 1), wave w1 — the build + first-falsifier wave for three frozen
claims. The lane is a fleet/host observability lane (detection and report only).

Read first (absolute):
- {LANE}/.ufo/waves/round-79/contract.md  (the frozen claims, predicates, targets, controls)
- {LANE}/SCORECARD.md (the `## Axes` table and the round-78 section at end of file)
- {LANE}/corpus/QUALITY.md (the criteria, esp. 159, 161, 162, 163)
- {LANE}/SKILL.md (the instrument registry table near line 1290-1320)

Claims:
- C1 operability (capability acquisition): build `tools/mori-control-receipt.py`, the
  control-receipt binding guard, to the spec in contract.md; the D78-1 witness is
  `{LANE}/.ufo/waves/round-78/evidence/controls-r78.txt` (a control receipt stating a count
  with no counting command).
- C2 calibration: SCORECARD.md's axes-table `Last change` cells must lead with the latest
  admitted mori closure grading the axis improved/harmed, per the fleet MANIFEST.
- C3 freshness (sourced): open RFC 9111 §4.1, pin it, and land
  `corpus/knowledge/ua-serving-normative-r79.md` grounding the lane's empirical
  `ua-serving` drift class in the normative Vary-selection text.

# Bounds (all seats)
- Your tools start at the FLEET root, not the lane: every path you read, write or run is
  ABSOLUTE and under {LANE} unless this prompt names the fleet repo or a scratch copy.
  Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.
- You never commit, push, tag, stash, checkout, reset, switch, or run any mutating git/jj
  command in the lane or the fleet repo. Read-only git (`git -C {LANE} show/log/cat-file/
  rev-parse/ls-files`) is fine. The L1 integrates and commits; seats return findings+files.
- Never edit `MANIFEST.json`, the fleet root, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`,
  the round-79 counters, `contract.md`, or any sibling lane repo.
- A seat never edits a file another seat is told to write. If your work needs a file outside
  your named targets, write your version under {LANE}/.ufo/waves/round-79/w1/ and name it in
  your report.
- Scratch discipline: every clone/temp/counter work dir lives under `{SCRATCH}/<your-name>/`
  (mkdir -p, pass it explicitly); delete it before you yield (`trap 'rm -rf -- "$S"' EXIT`);
  /tmp only for files under 50 MB. A tree left on disk is a defect you must report.
- Git fixtures: any fixture repo is `D=$(mktemp -d -p {SCRATCH}/<your-name>) && git -C "$D"
  init -q`, every later call names `-C "$D"`, and `git -C "$D" rev-parse --show-toplevel`
  must equal `$D` before the first commit.
- Leaf seat: no subagent dispatch of your own (an executor may spawn exactly one read-only
  labrat probe for one falsifiable hypothesis; every other role is a leaf).
- Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help
  the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety
  gate; record tool/version/channel/reason in your report). pacman is PAUSED host-wide:
  install via `uv tool`/`npx`/an official binary in `~/.local/bin`, never `pacman -S`,
  `-Sy`, `-Syu`, `-U`, `-R` or a partial upgrade; file the need in your report instead.
- Never message `agent://all`. Detection and report only: no remediation, no OS/unit state
  changes, no session/credential material.
- English, evidence-dense: every claim you make carries a command you ran and its output, at
  the bytes it ran over. A check you did not run is not a check that passed.

# Deliverable form
Write your findings to your `Report:` path with: what you did (numbered), the commands and
outputs, what you found (including negative results and anything you could not verify), and
your own defects (what you got wrong and how you caught it). Keep committed artifacts small
and text-only.
"""


def item(name, role, prompt):
    return {"name": name, "role": role, "axes": ["operability", "calibration", "freshness"],
            "milestone": "round 79 w1: C1 control-receipt guard, C2 axes-cell reconciliation, "
                         "C3 RFC 9111 Vary row + entry", "prompt": prompt}


ITEMS = [
    item("Mo79E01ReceiptTool", "executor", f"""\
Build `{LANE}/tools/mori-control-receipt.py` — the control-receipt binding guard (C1) —
exactly to the spec in `{LANE}/.ufo/waves/round-79/contract.md` § C1 (read that section
first; it is frozen). Python 3 standard library only, `python -I` safe, single file.

Required behaviour (the contract is authoritative; this is the summary):
- inputs: one or more receipt paths, or `--dir DIR` (every `*.txt` directly under DIR,
  sorted); `--selftest`; `--help`.
- split each receipt into sections at lines matching `^## `; content before the first
  heading is section `(head)`.
- a count claim = a stripped line matching `^[A-Za-z][A-Za-z0-9_.-]*=-?[0-9]+$`.
- a section is bound iff it holds at least one command line: a non-comment line whose
  stripped text starts with `$ ` or whose first token is in the contract's verb list, or a
  non-comment line containing ` cmd=`.
- output per file `CONTROL_RECEIPT <path> sections=S claims=C bound=B unbound=U` plus one
  `unbound <path>#<section> claims=N keys=<k1,k2>` per unbound section, then
  `CONTROL_RECEIPT_SUMMARY files=F sections=S claims=C unbound=U`.
- rc 0 iff no section with claims is unbound; 1 if any is; 2 setup (usage, missing path,
  unreadable file). stdout only: no writes, no network, no subprocess, no `/tmp` path.

Acceptance (run all three and paste the outputs in your report):
1. `python3 {LANE}/tools/mori-control-receipt.py --selftest` -> `CONTROL_RECEIPT_SELFTEST
   pass=P fail=0` with P >= 10, rc 0. Build >=10 in-script cases, including: a bound
   section (`$ cmd` above the count), an unbound section, a `# comment` line that must NOT
   count as a command, the inline `cmd=` form, a section-level split across two `##`
   headings, a non-integer `key=value` line that is NOT a claim, a negative integer claim,
   an empty file, a missing path (rc 2), and a receipt with no claims at all.
2. `python3 {LANE}/tools/mori-control-receipt.py --dir {LANE}/.ufo/waves/round-78/evidence`
   -> rc 1 (that dir is the D78-1 witness set; its `controls-r78.txt` states counts with no
   counting command). Your stdout must name `controls-r78.txt` and the key
   `correction_marker_in_LOG_at_entering`.
3. `python3 {LANE}/tools/mori-control-receipt.py --dir {LANE}/.ufo/waves/round-79/evidence`
   -> rc 0 with `unbound=0` (the round's own receipts are written in the bound form).

Do not edit the counters, the contract, SCORECARD.md, SOURCES.md or any other lane file.
Report at the trailer path with the three command transcripts and the selftest case list."""),

    item("Mo79E02AxesCells", "executor", f"""\
C2 data walk — produce the corrected `Last change` cells for SCORECARD.md's `## Axes`
table, WITHOUT editing SCORECARD.md.

1. Read `{LANE}/.ufo/waves/round-79/contract.md` § C2 (the frozen predicate) and the `## Axes`
   table in `{LANE}/SCORECARD.md`.
2. Derive N* per axis yourself with your own command: read
   `/home/vgpnk/Projects/shokunin/MANIFEST.json`, keep `lane == "mori"` and `admitted: true`
   rows with `round <= 78`, and for each axis take the highest round whose verdict is
   `improved` or `harmed`. Paste the command and its output (a six-line table) — do not copy
   the numbers the contract lists; why the contract's list could be wrong is part of the job.
3. Run `python3 {LANE}/.ufo/waves/round-79/count-c2.py {LANE} 2>/dev/null` is NOT valid (the
   counter wants a revision): run it as
   `python3 {LANE}/.ufo/waves/round-79/count-c2.py 84c6cbc3b47c536a504aaee329c77897d389935e`
   and paste the axis lines. If your own derivation disagrees with the counter, say which and
   why (that is a finding, not a failure).
4. For each of the six axes write the replacement cell text into
   `{LANE}/.ufo/waves/round-79/w1/Mo79E02AxesCells-cells.md` as a markdown table
   (axis | current cell | proposed cell). Rules: the proposed cell LEADS with
   `round N (verdict, score held)` for N* and its verdict word; keep every existing clause
   after the first `;` byte-for-byte (history is preserved, nothing is deleted); adjacency
   already reads round 19 and stays unchanged — mark it `unchanged`. Also draft the short
   `Round-79 correction (C2, calibration)` paragraph the L1 will append after the r50
   correction paragraph: it states the mismatch count before (5 of 6), the one axis that was
   right, the fleet manifest revision you read, and the convention sentence it enforces.
5. Run `python3 {LANE}/.ufo/waves/round-79/count-c2.py 84c6cbc3b47c536a504aaee329c77897d389935e`
   once more at the end and name it as the entering-state control (it must read
   `mismatches=5`); this proves your proposed cells are not already the state.

Do not edit SCORECARD.md, the counters, or any other lane file. Report at the trailer path
with the derivation command, the cells table, and the draft paragraph."""),

    item("Mo79E03SourcePin", "executor", f"""\
C3 source opening — sweep, fetch, pin and locate RFC 9111 §4.1.

Order is fixed and receipted:
1. DUPLICATE SWEEP FIRST, into your receipt, BEFORE the fetch. Run
   `grep -cE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|' {LANE}/corpus/SOURCES.md`
   (row count), then grep the registry for `rfc9111`, `9111`, `HTTP Caching`, `Vary` and the
   exact URL `https://www.rfc-editor.org/rfc/rfc9111.txt`. Record every hit with its row id
   and state the interpretation (which held rows are nearest neighbours, whether the exact
   URL is already registered).
2. Fetch `https://www.rfc-editor.org/rfc/rfc9111.txt` with curl (`-sS -D <headers> -o
   {LANE}/corpus/evidence/sources-r79/rfc9111.txt`); record the HTTP status, byte size,
   sha256, and the first line of the body (the document title) BEFORE pinning. A non-200 or
   an HTML error body is a failed fetch: report it, do not pin.
3. Locate the quote lines for §4.1 "Calculating Cache Keys with the Vary Header Field":
   `grep -n` for the section heading and for the sentences about the selecting header fields
   / the request header fields matching / the stored response. For each chosen quote record
   the exact line number, the verbatim text, and its `wc -w` word count; every quote must be
   <= 25 words and must be a contiguous span on ONE line. Name at least 4 quotes.
4. Machine-verify them: `python3 {LANE}/tools/mori-anchor-check.py --pin
   {LANE}/corpus/evidence/sources-r79/rfc9111.txt --check <line>:<quote>` for each (check the
   tool's `--help` first; it takes `--check SPEC` repeated). Record PASS plus an able-to-fail
   arm: the same quote against a wrong line must FAIL rc 1.
5. Write the whole transcript as `{LANE}/.ufo/waves/round-79/evidence/source-rfc9111-r79.txt`
   (sections with `## ` headings; every count line preceded by the `$ command` that produced
   it — the lane's new control-receipt rule) and also state in your report which line numbers
   you found.

The pin file is yours to write. Do not edit SOURCES.md, SCORECARD.md, the counters, or the
knowledge entry. Report at the trailer path with the sweep output, the fetch facts, the quote
table (line | words | text) and the anchor-check transcript."""),

    item("Mo79S01EntryProse", "scribe", f"""\
C3 prose — write the knowledge entry `{LANE}/corpus/knowledge/ua-serving-normative-r79.md`
grounding the lane's empirical `ua-serving` drift class in normative text.

Read first: `{LANE}/corpus/QUALITY.md` criterion 159, the existing entry
`{LANE}/corpus/knowledge/counter-semantics-r78.md` (the shape a recent admitted entry takes),
`{LANE}/corpus/knowledge/source-drift-hardening-r37.md`, and the receipts
`{LANE}/.ufo/waves/round-78/evidence/pin-family-r78.txt` + `-final.txt` (what the `ua-serving`
class looked like when it fired three times: S591/S592/S593).

Open the source yourself: `curl -sS https://www.rfc-editor.org/rfc/rfc9111.txt -o
{SCRATCH}/Mo79S01EntryProse/rfc9111.txt` (mkdir -p first), then `grep -n` §4.1 and read the
surrounding lines. Every quote you use must be verbatim from that file, on one line, <= 25
words, with its line number and `wc -w` count recorded in the entry's provenance block.

Entry shape (follow the lane's admitted-entry form):
- title + a one-paragraph statement of what the entry teaches;
- provenance trio as separate lines: `source:` naming `S594` and the URL,
  `verified-at:` the date you opened it (2026-11-04), `recheck:` a cadence token (use `365d`);
- a `## K1`..`## K4` body: K1 the normative mechanism (Vary selects among stored
  representations; the selecting header fields are named by the response), K2 what that makes
  a per-User-Agent byte difference (a legitimate representation selection, not content drift
  by itself), K3 the boundary the lane keeps (a difference still needs the standard
  adjudication before it is classed anything; the vendor's bot-management policy is not the
  lane's to infer), K4 the reader rule (compare variant to variant, or pin per-client; a
  variant mismatch is `ua-serving`, never `content-drift`);
- a `## Limits` and a `## Boundaries` section in the lane's style (what this does not prove).

Do not edit SOURCES.md, README.md, SCORECARD.md or any receipt. Report at the trailer path
with the grep output you used and any place the normative text was weaker than expected."""),

    item("Mo79S02SourcesRow", "scribe", f"""\
C3 registry prose — draft the `S594` registry row and the README index row, in the wave dir
only (the L1 appends them).

Read: `{LANE}/corpus/SOURCES.md` header + the last ten registry rows (S585-S593) for the
exact 11-column shape (`| id | source | kind | tier | scope | anchor | teaches | status |
opened | recheck | used-by |`), `{LANE}/corpus/README.md`'s knowledge-index table tail, and
`{LANE}/.ufo/waves/round-79/contract.md` § C3.

Row content: id `S594`, source `HTTP Caching (RFC 9111) §4.1 — https://www.rfc-editor.org/rfc/rfc9111.txt`,
kind `spec`, tier `A`, scope = the Vary-selected representation and the cache-key rule, anchor
= `§4.1` plus the located lines and the pin path `corpus/evidence/sources-r79/rfc9111.txt`
plus its sha256 (read the sha from `{LANE}/.ufo/waves/round-79/evidence/source-rfc9111-r79.txt`
if it exists, else `sha256sum` the pin file yourself — never invent one), teaches = one
sentence, status `mined`, opened `2026-11-04`, recheck `365d`, used-by
`corpus/knowledge/ua-serving-normative-r79.md`.

Hard rules: no cell may contain a literal or escaped `|` (rewrite a quote so it parses as 11
columns); the row must pass the census schema (recheck is a valid ISO date, `NNd`, or a
symbolic token — `365d` is fine); `used-by` names exactly the entry that cites it.

Deliver `{LANE}/.ufo/waves/round-79/w1/Mo79S02SourcesRow-append.md` with: the exact row line
in a fenced block, the README index row line in a fenced block, the insertion points (which
existing line each follows), and a self-check that the row splits into exactly 11 cells
(show the command). Do not edit SOURCES.md or README.md. Report at the trailer path."""),

    item("Mo79C01Overlap", "connector", f"""\
Sibling-overlap scan (read-only) — find what the fleet already holds against this round's
three claims, so the lane does not re-invent another lane's instrument or source.

1. C1 class: search the sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin/`
   (read-only, `grep -rl`/`grep -rn`) for a receipt-binding / count-without-command /
   report-contract checker (`control-receipt`, `receipt-complete`, `command`+`claim`,
   `count.*cmd`). Name the closest instruments with path and one-line capability, or say none.
2. C2 class: does any sibling hold an axes-table / self-assessment reconciliation gate against
   the fleet MANIFEST? Look for `MANIFEST.json` readers in `tools/` and `verifiers/`, and name
   the closest with its verdict contract. Also check whether the fleet protocol already fixes
   the "Last change" convention (grep `/home/vgpnk/Projects/shokunin/PROTOCOL.md` and
   `AXES.md` for `Last change`).
3. C3 class: does any sibling lane already cite RFC 9111 (`grep -rn 'rfc9111'`) or hold the
   Vary-selection rule as a corpus row? Name lane + row id, or say none.
4. For each of the three, state the overlap verdict: `duplicate` (the lane would duplicate a
   standing sibling capability), `adjacent` (a different surface, worth citing as neighbour),
   or `clear`.

Read-only. Write a short findings file at the trailer path with the commands, the matched
paths, and the three verdicts. Do not modify any sibling repo."""),

    item("Mo79Sc01Recon", "scout", f"""\
Bounded data walk for the integration step (read-only) — pin the exact insertion points and
byte facts the L1 needs to land this round without guessing.

For each item, give the command you ran and its output:
1. `{LANE}/SCORECARD.md`: the line numbers of the `## Axes` heading, the six axis rows, the
   table's closing line, and the two correction paragraphs after it (round-25 and round-50);
   the total line count and sha256 of the file at
   `git -C {LANE} show 84c6cbc3b47c536a504aaee329c77897d389935e:SCORECARD.md`.
2. `{LANE}/corpus/SOURCES.md`: total lines, the last registry row's line number and id, the
   line number of the `## Paths` heading (the registry ends just before it), and the row count
   under both the strict `^\\|` form and the 0-3-space tolerant form.
3. `{LANE}/corpus/README.md`: the knowledge-index table's header line, the last index row
   (line number + text), and the total line count.
4. `{LANE}/SKILL.md`: the line number of the instrument-registry table's last row (the r77
   counter probe row), the table's header line, and how many columns that table has.
5. `{LANE}/corpus/lessons/round-78.md`: its `## Gate` and `## Mistakes` heading line numbers,
   so this round's lesson can follow the same shape.

Constraints: read-only; no writes outside your report; do not open huge files whole (use
`sed -n`/`grep -n`). Report at the trailer path as a compact numbered list of facts with
commands, plus any inconsistency you noticed (e.g. a heading that is not where the file's own
text says it is)."""),

    item("Mo79R01Review", "reviewer", f"""\
Adversarial review of C1 (the new `{LANE}/tools/mori-control-receipt.py`, built by another
seat in this wave). Your job is to make it fail.

Read `{LANE}/.ufo/waves/round-79/contract.md` § C1 first, then the tool's bytes, then attack:
1. Re-run `--selftest` yourself at the working-tree bytes; record pass/fail and rc.
2. Re-run both live dirs (`--dir {LANE}/.ufo/waves/round-78/evidence` must be rc 1 naming
   `controls-r78.txt` + `correction_marker_in_LOG_at_entering`; `--dir
   {LANE}/.ufo/waves/round-79/evidence` must be rc 0 with `unbound=0`).
3. Build hostile fixtures under `{SCRATCH}/Mo79R01Review/` and check the predicate the
   contract froze, not the tool's intentions:
   - a section whose only "command" is an indented `$ cmd` (must bind — the contract strips);
   - a section whose only "command" is `# $ git status` (a comment; must NOT bind);
   - a count claim with a trailing comment `x=0 # note` (not a bare `key=integer` line: must
     NOT count as a claim);
   - `x=-1` (a negative integer: must count as a claim);
   - `x=1.5` and `x=1e3` (not integers: must not count);
   - two `##` sections, one bound one not (only the unbound one is reported);
   - a `key=0` line directly under a `$ cmd` line (bound);
   - a receipt with CRLF line endings and one with a BOM (state what happens; a crash is a
     defect, a documented rc-2 is not);
   - a directory with no `.txt` files (`--dir` behaviour; rc must be 0 or 2 by the contract,
     never a traceback).
4. State which attacks land and which the tool refuses, with the exact command + output. A
   landed attack is a defect to report by name; do not fix the tool.

Report at the trailer path. Detection and report only: never edit the tool or any lane file."""),

    item("Mo79K01Critic", "critic", f"""\
Falsify C2 — the axes-table calibration claim — independently of the seat that produced the
candidate cells.

1. Read `{LANE}/.ufo/waves/round-79/contract.md` § C2 and `{LANE}/SCORECARD.md`'s `## Axes`
   table.
2. Derive N* per axis with your own command over `/home/vgpnk/Projects/shokunin/MANIFEST.json`
   (lane `mori`, `admitted: true`, `round <= 78`, verdict `improved` or `harmed`, highest
   round). Print the per-axis candidate rounds including the ones you rejected and why (e.g.
   a higher round that is not admitted, or a verdict of `unchanged`/`unprovable`).
3. Compare against the entering cells (`git -C {LANE} show
   84c6cbc3b47c536a504aaee329c77897d389935e:SCORECARD.md`) and against
   `{LANE}/.ufo/waves/round-79/w1/Mo79E02AxesCells-cells.md` if it exists.
4. Attack the frozen predicate itself: (a) is "the first `round N` in the cell" the right
   parse for cells like `round 51 (improved, score held); ...`? (b) does dropping the
   `Evidence` cell check let a cell pass while its named closure spotcheck file does not
   exist? Test the adjacency cell (round 19: does
   `corpus/lessons/round-19-verifier-spotcheck.md` exist?) and say what the narrowed
   predicate therefore misses; (c) can a do-nothing round reach `mismatches=0` — i.e. is the
   entering state already conformant? Show the counter's entering verdict.
5. Grade the claim: `holds`, `holds-with-named-limit`, or `fails`. A limit you name must be
   one a reader could check.

Read-only: do not edit SCORECARD.md, the counters or any lane file. Report at the trailer
path with every command and its output."""),

    item("Mo79M01Mutant", "mutation-tester", f"""\
Mutation-test C1's guard `{LANE}/tools/mori-control-receipt.py` (built by another seat in
this wave). A mutant that survives is a hole in the selftest, not a licence.

Work on a COPY under `{SCRATCH}/Mo79M01Mutant/` (never edit the lane tool). Apply at least
six mutants, one at a time, each a minimal source edit:
1. treat a `#`-comment line as a command line;
2. drop the `$ ` prefix arm (keep only the verb list);
3. drop the verb-list arm (keep only `$ `);
4. drop the ` cmd=` inline arm;
5. make section splitting ignore `##` headings (one section per file);
6. accept any non-empty `key=value` line as a count claim (drop the integer test);
7. (seventh, if the code allows) make the rc always 0.
For each mutant: record the diff hunk (line + before/after), run the tool's own `--selftest`,
and record rc + the `CONTROL_RECEIPT_SELFTEST pass=P fail=F` line. A mutant is KILLED iff the
selftest turns red; SURVIVED otherwise.
Also run the contract's two live dirs against each mutant and record whether the mutant
changes the observable verdict on real receipts (a mutant that keeps the selftest green AND
changes a live verdict is the worst class — name it).
Use `python3 -I` for every run and delete your copy at the end (`trap` or explicit rm).

Report at the trailer path: a table (mutant | hunk | selftest | verdict | live-dir effect)
and the list of SURVIVED mutants with the arm the selftest should gain."""),

    item("Mo79M02MutantCounter", "mutation-tester", f"""\
Mutation-test the C2 counter `{LANE}/.ufo/waves/round-79/count-c2.py` — it is the frozen
instrument that grades the calibration claim, so its selftest must kill its own weakening.

Work on copies under `{SCRATCH}/Mo79M02MutantCounter/` (never edit the lane counter). Reading
`{LANE}/.ufo/waves/round-79/contract.md` § C2 first. Apply at least five mutants, one at a
time, each a minimal edit:
1. drop the `admitted` filter in `expectations`;
2. raise the round ceiling `through` comparison to a constant far above 78;
3. treat `unchanged`/`unprovable` as counting verdicts;
4. cut the `;` clause boundary so the whole rest of the cell is searched for a verdict word;
5. accept any `round N` occurrence anywhere in the cell rather than only the first;
6. (sixth) make `grade` return `met: True` when `mismatches == 0` is false but errors are 0.
For each: record the hunk, run `python3 -I <copy> --selftest`, record
`C2_COUNTER_SELFTEST pass=P fail=F` and the verdict (KILLED iff the selftest goes red).
Then run each surviving mutant against the real entering revision
`84c6cbc3b47c536a504aaee329c77897d389935e` and record whether its mismatch count changes
(a survivor that changes the real reading is a hole the selftest must close — name the arm).
Delete your copies at the end.

Report at the trailer path: the mutant table and the surviving-mutant analysis."""),

    item("Mo79N01Sentinel", "sentinel", f"""\
Write-scope and redaction audit of this round's new artifacts (C1 tool, the C3 pin receipt,
the C2 cells file) — the lane is detection-and-report only, so a new instrument that writes,
phones home or leaks host identity is a defect.

Audit, with commands and outputs:
1. `{LANE}/tools/mori-control-receipt.py`: enumerate every import and every call that could
   write or run a child (`grep -nE 'open\\(|subprocess|os\\.(remove|unlink|rename|makedirs|mkdir)|socket|urllib|requests|shutil|tempfile'`).
   State whether the tool writes any file, spawns any process, opens any socket, or uses
   `/tmp`; a hit must be justified by the frozen spec (it allows none).
2. Data touched: run the tool on the round-78 evidence dir with a wrapper that lists the
   paths it opened (`strace -f -e trace=openat -o <scratch>/trace.txt` if available, else
   `python3 -c` with an audit hook, or state the method) and confirm it only reads the named
   dir's `*.txt`.
3. Redaction: scan every text artifact this wave wrote under `{LANE}/.ufo/waves/round-79/`
   (excluding binaries) for host-identifying material — the hostname, the user name, an
   absolute `/home/<user>` path outside the lane's own documented roots, an IP address, a
   credential-shaped token (`grep -nEi 'password|token=|secret|BEGIN .*PRIVATE KEY|\\b[0-9]{{1,3}}\\.[0-9]{{1,3}}\\.[0-9]{{1,3}}\\.[0-9]{{1,3}}\\b'`).
   The RFC pin is public-document bytes: say so explicitly rather than flagging its content.
4. Boundary check: does anything in this round's artifacts cross into dispatch/orchestration,
   OS/unit state, model-serving health or credential material? Name what you checked.
5. Report any finding with file:line and severity, or state `no finding` per item.

Read-only: do not edit the tool or any lane file. Report at the trailer path."""),
]

spec = {
    "wave": "mori-r79-w1",
    "milestone": "Round 79 w1: build + first falsifiers for C1 (control-receipt guard, D78-1 "
                 "witness), C2 (axes Last-change vs MANIFEST) and C3 (RFC 9111 §4.1 Vary row); "
                 "counters frozen in aa53b485.",
    "axes": ["operability", "calibration", "freshness", "coverage", "depth", "adjacency"],
    "reportDir": WAVE,
    "maxLanes": 12,
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
    with open(out, "w") as fh:
        json.dump(spec, fh, indent=1)
    print(out, len(ITEMS), "items")
