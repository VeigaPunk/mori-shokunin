#!/usr/bin/env python3
"""Build mori round-81 wave w1 spec (one v1 wave, 14 seats, band 8-16).

Writes .ufo/waves/round-81/w1-spec.json. Every item prompt is self-contained; shared
rules ride the wave context.
"""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
ROUND = LANE + "/.ufo/waves/round-81"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = GODSPEED + """

# Goal
mori round 81 (attempt 1), wave w1 — build and first falsifiers for TWO frozen claims.
The lane is a fleet/host observability lane: detection and report only.

Read first, in this order (absolute paths):
- {round}/contract.md — THE FROZEN AUTHORITY. Predicates P-C1 and P-C2, fixture table,
  the record-sweep interface, and the do-nothing controls. It is not rewritten.
- {lane}/SCORECARD.md (the `## Round 80` and `## Round 81` sections, the Axes table and
  the capabilities tables), {lane}/SKILL.md (the gate registry near the end),
  {lane}/PROVINCE.md (`## Instrument inventory (round 80)`),
  {lane}/corpus/QUALITY.md (the last criteria), {lane}/corpus/README.md (`## Frontier`).
- {lane}/corpus/lessons/round-80.md and {lane}/corpus/lessons/round-80-verifier-spotcheck.md
  (`## Routed defects the lane must fix next round`).
- {lane}/.ufo/waves/round-80/w1/Mo80R01Counter.md (the counter reviewer's fixtures).

# Round claims (frozen before this wave; do not change them)
- C1 operability (7): the r80 counters' seven routed exposures are closed; the keeper is
  `python3 -I .ufo/waves/round-81/count-c1.py <rev>` reading `C1=met wrong=0 fixtures=7
  real_c1=met real_c3=met`, red `wrong=7` at entering `44bc941a`.
- C2 calibration (5, lowest non-retired axis): `tools/mori-record-sweep.py` lands and the
  record's PENDING after-cells and stale pinned counts are corrected; the keeper is
  `python3 -I .ufo/waves/round-81/count-c2.py <rev>` reading `C2=met pending=0 pinned=0
  tool=present agree=1`, red `pending=3 pinned=1 tool=absent` at entering.

# Shared rules (binding on every seat)
- Write scope: {lane} only. Absolute paths in every tool call: your tools start at the
  FLEET root, so a relative path lands in the wrong repo. Never write to
  /home/vgpnk/Projects/shokunin (fleet root), another lane's repo, MANIFEST.json,
  `.ufo/state/`, `.ufo/watchdog.log`, or `.scratch/`.
- Never commit, push, or run a mutating git/jj command anywhere; never run `git add`,
  `git commit`, `git checkout`, `git reset`, `git stash`, `git push`, or any mutating
  `jj` command. Read-only git (`log`, `show`, `diff`, `status`, `ls-tree`, `cat-file`,
  `rev-parse`) is fine. The L1 owns every commit.
- Every `Report:` trailer path is relative to {lane} — write it at {lane}/<that path>.
- Scratch: create your work dir under /fast/scratch/hyaku/mori-r81/<your seat name>/ and
  delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell). Never write under
  /tmp; a /tmp path is never citable evidence. Clone with `git clone --shared` or
  `git worktree add` when you need one; never mirror the whole lane.
- Read-only on everything you grade. Detection and report only: no lane, OS, unit,
  service, credential, harness or orchestration state may be changed.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that
  help the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels,
  update-safety gate) and record tool/version/channel/reason in your report. pacman is
  PAUSED host-wide: never run a pacman transaction of any kind (`-S`, `-Sy`, `-Syu`,
  `-U`, `-R`); use `uv tool`, `npx`, or an official binary in ~/.local/bin, or file an
  L0 question instead.
- Never message `agent://all`. Message only your own L1 (`agent://MoriR81`) for a blocker.
- Do not spawn subagents except an executor's single read-only `labrat` probe.
- Your final report must name: what you changed/produced with absolute paths, the exact
  commands you ran with their output, what you verified, what you could not verify, and
  any defect you found in another seat's bytes (file:line). Be adversarial about your
  own work: an unrun check has not passed.
"""


def item(name, role, prompt, milestone="round 81 w1: C1 r80-counter defects closed; C2 record gate + corrections"):
    return {"name": name, "role": role, "axes": ["operability", "calibration", "coverage", "depth", "freshness", "adjacency"],
            "milestone": milestone, "prompt": prompt}


ITEMS = []

ITEMS.append(item("Mo81E01SweepFix", "executor", """
Fix `.ufo/waves/round-80/count-c1.py` (absolute: {lane}/.ufo/waves/round-80/count-c1.py) so
it grades the three r80-routed exposures filed at
{lane}/.ufo/waves/round-80/w1/Mo80R01Counter.md MEDIUM-7, MEDIUM-8 and LOW-10:

1. MEDIUM-7 — the counter reads a single `CLAIM_SWEEP` summary with `re.search`, so a sweep
   that prints a `CLAIM_SWEEP_MISMATCH ...` line and then an all-zero summary, or two
   contradicting summaries with exit 0, grades `met`. Fix: parse **all** `CLAIM_SWEEP` lines;
   any `CLAIM_SWEEP_MISMATCH` line, any non-zero field, more than one distinct summary, or a
   nonzero exit is `met=False`.
2. MEDIUM-8 — `row_tally()` returns the first capability row naming
   `tools/mori-control-receipt.py`. Fix: collect **every** such row's `selftest N in-memory`
   reading and require every one to equal the live `--selftest` count; a row without the
   phrase, or disagreeing rows, is a mismatch.
3. LOW-10 — `export()` runs `git -C {repo} archive {rev} | tar -x -C {dest}` through a shell
   string, so a repo path containing a space degrades to a setup error. Fix: two argv
   subprocess calls (archive bytes → tar stdin), no shell, no interpolation.

Constraints: the frozen predicate in .ufo/waves/round-80/contract.md and the counter's
graded output grammar stay byte-identical; the real lane bytes at `44bc941a` must still
grade `C1=met ... row_tally=19 live_tally=19`. Add one `--selftest` fixture per fix to
`selfcheck()` (a contradicting-summary case, a second-stale-row case, a repo path with a
space case) — and keep every existing arm green. Then verify:

```
cd {lane}
python3 -I .ufo/waves/round-80/count-c1.py --selftest
python3 -I .ufo/waves/round-80/count-c1.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d
```

(the second must print `C1=met ... rev=44bc941a0e3e`). Report: the diff hunks by line range,
selftest tally before/after, and the 44bc941a reading. Do not touch count-c3.py.
"""), )

ITEMS.append(item("Mo81E02C3Fix", "executor", """
Fix `.ufo/waves/round-80/count-c3.py` (absolute: {lane}/.ufo/waves/round-80/count-c3.py) so
it grades the three r80-routed exposures filed at
{lane}/.ufo/waves/round-80/w1/Mo80R01Counter.md MEDIUM-6, LOW-11 and LOW-12:

1. MEDIUM-6 — `TOKEN` has no left boundary, so `` `corpus/tools/mori-census.sh` `` counts as
   naming a lane instrument. Fix: require a left boundary (the sweep's convention is
   `(?<![\\w./-])`), so only a path segment that starts at `tools/` after a non-path
   character names an instrument.
2. LOW-11 — the `SIBLING` exclusion (`*-shokunin/`) also drops the lane's **own** prefixed
   path `mori-shokunin/tools/<name>`. Fix: compute the lane repo's own directory basename
   and allow `OWN/tools/<name>`; still exclude every other `*-shokunin/` prefix.
3. LOW-12 — a named `tools/<name>.py` that exists only as a **directory** at R counts as
   `extra`. Fix: a named path that exists at R as a directory is not an instrument (not
   `named`, not `extra`); a path that does not exist at all is still `extra`. Use
   `git ls-tree -r -t` or the export to decide file vs directory.

Constraints: the frozen predicate in .ufo/waves/round-80/contract.md and the output grammar
stay byte-identical; the real lane bytes at `44bc941a` must still grade
`C3=met named=56 present=56 missing=0 extra=0`. Add one `--selftest` arm per fix. Verify:

```
cd {lane}
python3 -I .ufo/waves/round-80/count-c3.py --selftest
python3 -I .ufo/waves/round-80/count-c3.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d
```

Report the diff hunks, the selftest tally before/after, and the 44bc941a reading. Do not
touch count-c1.py.
"""), )

ITEMS.append(item("Mo81E03RecordTool", "executor", """
Build `{lane}/tools/mori-record-sweep.py` exactly to the frozen interface in
{lane}/.ufo/waves/round-81/contract.md § "`tools/mori-record-sweep.py` — frozen interface".

Deliverable: one read-only Python 3 standard-library file, `python3 -I` safe:
- `--root DIR` (required for a run), `--pins FILE` (default `DIR/.ufo/waves/round-81/record-pins.json`),
  `--carriers A[,B]` (default: the bindings' carriers plus SCORECARD.md), `--selftest`, `--help`.
- arm `pending`: a table cell whose trimmed value is exactly `PENDING` inside a `## Round ...`
  section of a carrier (a claim table's result column).
- arm `pinned`: for each binding `{carrier,row_contains,key,command}` (schema
  `mori-record-pins-v1`), the first table row containing `row_contains` and stating
  `<key>=<integer>` must equal the `<key>=<integer>` the command prints when run with
  cwd=root; a missing stated value, a missing live value, conflicting live values, or a
  nonzero command exit is a mismatch.
- output: `RECORD_SWEEP_MISMATCH <pending|pinned> <carrier>:<line> <detail>` per mismatch,
  then `RECORD_SWEEP pending=N pinned=M carriers=C bindings=B`; exit 0 clean, 1 mismatches,
  2 setup (missing root, malformed pins/unreadable carrier).
- `--selftest`: at least 12 in-memory arms (pending in/out of a round section, prose
  PENDING ignored, stated/live agreement, conflict, tool-absent-style bindings, malformed
  pins, clean/dirty totals). No filesystem writes, no temp files, no sockets; the pinned
  commands are the only children.

Acceptance you must run and paste:
```
cd {lane}
python3 -I tools/mori-record-sweep.py --selftest
python3 -I tools/mori-record-sweep.py --root . --pins .ufo/waves/round-81/record-pins.json
```
The second MUST read `RECORD_SWEEP pending=3 pinned=1` rc 1 at the current worktree (the
r80 PENDING cells and the 232-vs-233 count are the entering debt; the L1 corrects them).
Do not edit SCORECARD/SKILL/PROVINCE; the L1 integrates your registry row. In your report,
give the exact SKILL gate-registry row (the eight columns of the table ending SKILL.md) and
one PROVINCE inventory row (`| \\`tools/mori-record-sweep.py\\` | gate | ... | ... |`) for the
L1 to paste.
"""), )

ITEMS.append(item("Mo81E04Battery", "executor", """
Build the round's re-runnable instrument battery and run it at the entering revision.
Deliverable: `{lane}/.ufo/waves/round-81/battery.sh` — one shell script, `set -u`, that from
the lane root runs, in order, and prints one `<label> rc=<n>` line per instrument plus a
final `BATTERY <passed>/<total>` line:

1. every `tools/*.py` with a `--selftest` option (discover with
   `grep -l -- '--selftest' tools/*.py tools/*.sh`), each via
   `python3 -I <tool> --selftest` (or `bash <tool> --selftest` for `.sh`), run with
   `TMPDIR` pointed inside your scratch dir;
2. `python3 -I .ufo/waves/round-80/count-c1.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d` and
   the same for `count-c3.py`;
3. `python3 -I .ufo/waves/round-81/count-c1.py --selftest` and `count-c2.py --selftest`.

It must accept `--rev <sha>` and pass it to the two r80 counters, defaulting to
`44bc941a0e3e9676fa33a882b43d6e9793cbf74d`; it must honour `HYAKU_SCRATCH` and create its
own scratch under `/fast/scratch/hyaku/mori-r81/Mo81E04Battery`, removed on exit. Write the
entering run to `{lane}/.ufo/waves/round-81/evidence/battery-entering.txt` and report the
pass total and every red line with its full output. Note in the report: two instruments
(`mori-disk-rate.py`, `mori-round41-calibration.py`) are known to print `pass=0 fail=0` at
rc 0 with TMPDIR unset (r80 QUALITY 167); the script must export a TMPDIR inside scratch so
they exercise their fixtures. Do not edit any tool.
"""), )

ITEMS.append(item("Mo81Sc01RecordCensus", "scout", """
Read-only data walk over the lane's record at the entering revision `44bc941a`
(branch `master`). Do not edit any file; report findings only.

Produce `.ufo/waves/round-81/w1/Mo81Sc01RecordCensus.md` with:
1. Every cell whose trimmed value is exactly `PENDING` inside a `## Round ...` section table
   of `{lane}/SCORECARD.md`: file:line, the round, the claim, and the after-column value.
   Also state whether any such cell exists in `SKILL.md`, `LOG.md` or `SHONEN.md`
   (command + output).
2. Every table row in `SCORECARD.md`'s capabilities tables and in `SKILL.md`'s gate registry
   that states a `<key>=<integer>` count whose command is quoted in the same row; for each,
   the stated value, the command, and the live value at the entering revision (run it
   read-only with cwd=the lane; it is the same working tree). Name every disagreement.
3. For the three r80 PENDING cells (SCORECARD lines 4048-4050), the measured after-values
   already committed in `{lane}/.ufo/waves/round-80/evidence/after-r80.txt` and
   `{lane}/.ufo/waves/round-80/evidence/controls-r80.txt`: quote the exact lines, so the L1
   can fill the cells from receipts rather than re-invent them.
4. Any other row whose stated count disagrees with the same count stated in a sibling
   carrier (SCORECARD vs SKILL vs LOG) — e.g. the control-receipt 19/18 class.
Use `git show 44bc941a:<path>` for the committed bytes and say so; where you read the
worktree, say that instead. Every count carries its command and exit code.
"""), )

ITEMS.append(item("Mo81Sc02Source", "scout", """
Open and pin the round's source row(s). Candidates, in order of fit; admit at most two and
only those you actually open:
1. `https://man7.org/linux/man-pages/man2/stat.2.html` — grounded fact for C1's B6 fixture:
   a path's type is carried in `st_mode` and a directory is not a regular file. Scope the
   tier to that exact statement.
2. `https://docs.python.org/3/library/os.html` (section `os.scandir` / `DirEntry`) — a
   `DirEntry`'s type and the `follow_symlinks` default. Scope: what a directory listing
   proves about an entry's type.
Do NOT use acm.org (403 to this host) or any paywalled page. Use an external source only if
a fresh `curl -sSL` fetch returns HTTP 200 and the located quote is at a named line.

Deliverables (absolute paths):
- `{lane}/corpus/evidence/sources-r81/<slug>.html` — the pinned page bytes (fetched this
  round), plus `sha256sum` and `wc -lc` in your report.
- `.ufo/waves/round-81/w1/Mo81Sc02Source.md` — for each candidate: URL, access date
  (2026-11-04), the exact located quote (≤25 words) with its pinned HTML line number, the
  line's text before/after for context, the duplicate sweep over
  `{lane}/corpus/SOURCES.md` (commands + output; the registry's last id is S595, so the next
  unused ids are S596 and S597), a proposed 11-column Registry row (id/source/kind/tier/scope/
  anchor/teaches/status `queued`/opened/recheck/used-by `—`), and at least one REJECTED
  candidate with reason and flip condition. No `|` inside any cell; anchor names the pinned
  file line and the page revision/date.
Admit-or-reject is the L1's call at the Gate; you propose, with the evidence.
"""), )

ITEMS.append(item("Mo81S01Corrections", "scribe", """
Draft the append-only corrections the r80 closure routed to this round, in ONE draft file
`.ufo/waves/round-81/w1/Mo81S01Corrections.md` (the L1 integrates into SCORECARD.md and
LOG.md; do not edit SCORECARD/SKILL/LOG yourself — shared carriers have one writer).

Read first: `{lane}/corpus/lessons/round-80-verifier-spotcheck.md` `## Routed defects the
lane must fix next round` (D80-1..D80-4), `{lane}/.ufo/waves/round-80/evidence/after-r80.txt`,
`{lane}/.ufo/waves/round-80/evidence/controls-r80.txt`, `{lane}/SCORECARD.md:4038-4050`,
`{lane}/SKILL.md` gate registry row 14 (near the end).

Produce, ready to paste, each as a named section that states the superseded text verbatim
and its replacement:
1. **D80-1** — the three r80 after-cells (`| PENDING |` at SCORECARD:4048/4049/4050) get the
   measured values from `after-r80.txt` (C1: `C1=met tool=present sweep=0 mismatches=0
   unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=97ce0c96c779`; C2:
   `MUTATION_C2 survivors=0 killed=6 total=6 unmutated=green rev=97ce0c96c779`; C3:
   `C3=met named=56 present=56 missing=0 extra=0 rev=97ce0c96c779`) — verify each line in
   the receipt before quoting it, and name the measured revision as `97ce0c96`.
2. **D80-2** — the capability row's `pointers=232` becomes `pointers=233` (re-run the pinned
   command and quote its output with the revision you ran it at), and the "integration re-run
   pending" wording in SCORECARD:4036 and SKILL.md row 14 becomes the measured command and
   revision. Name the supersession explicitly.
3. **D80-3** — append a correction naming the r80 contract's shorthand values (`1 -> 0`,
   "from 3 of 6", "from 15 of 55") as superseded by the measured controls, and narrow
   P-C1's second conjunct to the receipt the round actually used (`C1=unmet tool=absent` rc 1
   at `d5888922`), stating that the entering red is measured by running the same counter at
   the entering revision. Do not rewrite the r80 contract bytes.
4. **D80-4** — state `97ce0c96` as the measured revision and `44bc941a` as the final tip
   whose only graded-byte change after 97ce0c96 was the after receipt, `w1-results.json` and
   the reviewer report (check that claim against `git diff --stat 97ce0c96 44bc941a` and
   quote the output; if it is false, say so instead of copying it).

Every quoted count must carry its command. Flag anything you could not verify.
"""), )

ITEMS.append(item("Mo81S02Knowledge", "scribe", """
Write `{lane}/corpus/knowledge/record-claim-integrity-r81.md` — the round's admitted
knowledge entry (C2's sourced ground).

Shape (required):
- Provenance trio first: `source: S596` (the row `Mo81Sc02Source` pins at
  `{lane}/corpus/evidence/sources-r81/`; if its file is not yet written when you start,
  read `{lane}/.ufo/waves/round-81/w1/Mo81Sc02Source.md` for the URL/anchor and cite
  `S596` — the L1 reconciles), `verified-at: 44bc941a0e3e9676fa33a882b43d6e9793cbf74d`,
  `recheck:` one command that re-derives the entry's central claim.
- A decision table with ≥5 rows, each row: the record shape · why it is a claim, not a
  result · the check that catches it · the observed instance (file:line at the entering
  revision). Ground the rows in this round's measured facts: a `PENDING` after-cell; a
  numeric claim that disagrees with its own cited command (232 vs 233); a gate that trusts
  a summary line against its own evidence lines; a fixture the gate cannot see (a
  directory named like a tool; a subdirectory path counted as a name); a count corrected in
  one carrier and left standing in a sibling.
- `## Limits/Boundaries` — this is the lane's own record, not fleet semantics; no claim
  about another lane's records; a cell-value test is not a reading of intent; the source's
  own scope limit.
- ≤90 lines. No `|` inside table cells beyond the column separators.
Also append one index row for the entry to `{lane}/corpus/README.md`'s knowledge index
(find the index table and follow its row shape) — README is not written by any other seat
this wave, so you own that single append. Report the row you added.
"""), )

ITEMS.append(item("Mo81S03Lesson", "scribe", """
Draft `{lane}/corpus/lessons/round-81.md` (write it as the final file; the L1 appends the
measured after-blocks and the Gate verdicts before committing).

Required sections, in this order:
- Header: `# Round 81 — mori (L1 MoriR81)`, `round: 81`, `date: 2026-11-04`,
  `entering: 44bc941a0e3e9676fa33a882b43d6e9793cbf74d`, the two claims and their axes, and
  a line naming `.ufo/waves/round-81/contract.md` as the frozen authority.
- The entering controls verbatim from `{lane}/.ufo/waves/round-81/evidence/controls-r81.txt`
  (`C1=unmet wrong=7 fixtures=7 ...`; `C2=unmet pending=3 pinned=1 tool=absent ...`) with
  the note that these are the same commands a do-nothing round leaves unchanged.
- `## Gate` — candidates: the `Mo81Sc02Source` source candidates (admit/reject with reason
  and, for each admitted row, URL + access date 2026-11-04 + ≤25-word located quote), and
  the r80 correction set (D80-1..D80-4) as work items. State the intended entry path
  `corpus/knowledge/record-claim-integrity-r81.md` and the next unused row id S596.
- `## Mistakes` — one row per mistake: class · evidence pointer · captured-by · fix.
  Mine at least these two: (a) the r80 record's three after-cells stayed `PENDING` at the
  landed bytes while its report declared them measured — captured-by `none` (the r80 sweep
  graded pointers and tallies, not round-table cells), fix = the r81 `pending` arm and the
  `count-c2` keeper; (b) the r80 counter reviewer's MEDIUM-7/8 class: a gate that trusts a
  summary line against its own MISMATCH lines — captured-by the r80 spotcheck's fixture A2,
  fix = the all-lines parse plus a selftest arm shown to fail on the old code.
- `## Census` — the before census (rows 368, exit 0, 35 tolerated W04) with the command, and
  a placeholder line `AFTER: filled by the L1 at landing` for the L1 to replace.
- `## Refusals` — the `merge/mori/` package (first staged id S471 collides with the lane's
  registry whose ids reach S595; adoption needs document-keyed renumbering) and any candidate
  you reject.
Do not invent measurements. Where a value is the L1's to fill, mark it exactly.
"""), )

ITEMS.append(item("Mo81Cn01Siblings", "connector", """
Sibling-overlap scan (adjacency ground), read-only. Question: does another lane, or the
fleet protocol/aggregator duty, already own "a lane's own record claims must reproduce from
their cited command"? Answer with evidence, not opinion.

Steps:
1. `grep -rn` (bounded, `--include` narrow) across `/home/vgpnk/Projects/shokunin/*-shokunin/`
   for record-claim patterns: `PENDING` cells in SCORECARD round tables, `pointers=`,
   `selftest .* in-memory`, "record sweep", "claim sweep", "self-assessment". Exclude
   `mori-shokunin/` from the *population* (name it separately) and exclude `.git`.
2. For each hit in another lane, read the surrounding ≤10 lines and classify: (a) the same
   lane-local duty (a lane gating its own SCORECARD) — not contested; (b) a fleet-level
   duty (protocol/aggregator closing rounds) — contested, name the owner file:line;
   (c) unrelated prose.
3. Check `{lane}/PROVINCE.md` `## Adjacent` and `{lane}/corpus/README.md` `## Frontier`
   against what you found; name any row that is now wrong or incomplete.
4. Write `.ufo/waves/round-81/w1/Mo81Cn01Siblings.md`: the sweep commands + counts, a table
   of hits (path:line · class · owner), and a recommendation: what mori may keep, what it
   must report and not absorb. No edits outside your report file.
"""), )

ITEMS.append(item("Mo81R01C1Attack", "reviewer", """
Adversarial review of C1 (r80 counter fixes). Attack the claim, not the prose.

Test at the current worktree (the fixes are being written by seats E01/E02 in this wave; if a
file is still unmodified when you look, review the unmodified bytes and say so — do not wait):
1. Re-run `.ufo/waves/round-81/count-c1.py` at the tip worktree and at
   `44bc941a0e3e9676fa33a882b43d6e9793cbf74d` with `--scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack`.
   Paste both full outputs.
2. For each of the seven fixtures, build your own variant (not the counter's) that the fix
   should still catch, and one that it should *not* flag (a legitimate shape near the
   boundary: a `CLAIM_SWEEP_MISMATCH` line with exit 1 and a zero summary; a single summary
   with nonzero `unresolved`; a capability table with two identical rows; `tools/x.py` named
   from a fenced block; a directory named `tools/y.sh` with no real tool of that name).
   Report each: shape, expected, observed.
3. Check the r80 frozen predicate bytes are unchanged (`git diff 44bc941a -- .ufo/waves/round-80/contract.md`
   must be empty) and that the graded output grammar is unchanged.
4. Hunt for a false green: can any single edit make `count-c1.py` print `C1=met` while a
   fixture is defeated? Name it with the exact line.
Write `.ufo/waves/round-81/w1/Mo81R01C1Attack.md` with a VERDICT line per numbered check
(`AGREE` / `DISAGREE <reason>`), every command+output, and a severity table
(BLOCKER/HIGH/MEDIUM/LOW) of what you found. Never edit the counters or the counters' fixtures.
"""), )

ITEMS.append(item("Mo81R02C2Attack", "reviewer", """
Adversarial review of C2 (record gate + corrections). Attack the claim.

1. Read `{lane}/tools/mori-record-sweep.py` (if present) and
   `{lane}/.ufo/waves/round-81/count-c2.py`; run both at the tip worktree and at
   `44bc941a0e3e9676fa33a882b43d6e9793cbf74d` with a scratch under
   `/fast/scratch/hyaku/mori-r81/Mo81R02C2Attack`. Paste outputs.
2. Fixtures that should be caught: a `PENDING` cell in a round table; `PENDING` in prose
   (must NOT be caught); `PENDING` in a table outside a `## Round` section (must NOT be
   caught); a pending row inside a fenced block (say what happens and whether that is a
   defect); a binding whose stated `pointers=232` and live `pointers=233`; a binding whose
   command exits nonzero; a binding whose stdout prints two different `key=` values; a
   binding whose row was deleted (must the arm still fire? state the reading you think the
   contract's sentence implies and whether the implementation matches).
3. Attack the `agree` arm: can a stub `tools/mori-record-sweep.py` make `agree=1` while the
   record is dirty? Try it in scratch and report.
4. Check the corrections the wave drafts: does the D80-2 correction quote the live output at
   a named revision, and does the corrected `pointers` value reproduce
   (run the pinned command yourself)? Does the D80-1 fill match `after-r80.txt` byte for
   byte?
Write `.ufo/waves/round-81/w1/Mo81R02C2Attack.md` with AGREE/DISAGREE per check, commands
and outputs, and a severity table. Never edit the tool, the counter or the record.
"""), )

ITEMS.append(item("Mo81C01Contract", "critic", """
Falsify the round's frozen contract as a critic, before the L1 measures anything.

Read `{lane}/.ufo/waves/round-81/contract.md` and judge, one verdict per item with reasons:
1. **Do-nothing reachability** — could a do-nothing round pass P-C1 or P-C2? Try the cheapest
   cheat you can implement in scratch (a stub counter, a record edit that deletes the
   offending row, a `PENDING` reworded to `pending`). Report each attempt's result.
2. **Vacuous or over-broad arms** — does any fixture expectation admit a shape a broken
   counter also meets? Is `wrong=0` reachable by a counter that simply refuses everything
   (the always-unmet stub)? The contract claims the discrimination selftest covers this —
   check that it does, and that the check itself can fail.
3. **Freeze order** — verify the contract commit `6b021d29` predates the wave dispatch
   (`.ufo/waves/round-81/w1.ready` mtime > commit time) and that no graded value was
   changed after the freeze (`git log --oneline -- .ufo/waves/round-81/`).
4. **Causal separability** — can C1 be verified without C2's tool and vice versa? Name the
   command for each.
5. **No-harm** — are the no-harm conditions in the contract testable at the landed revision?
   Name any that are not, and the cheapest check that would make it testable.
6. **Claim-vs-counter drift** — does each claim sentence in the contract say exactly what its
   counter prints? Quote both and diff them.
Write `.ufo/waves/round-81/w1/Mo81C01Contract.md` with one section per item and a BLOCKER /
HIGH / MEDIUM / LOW severity per finding. Do not edit the contract.
"""), )

ITEMS.append(item("Mo81M01Mutants", "mutation-tester", """
Independent mutation test of the fix targets and the new gate. Report only; never edit lane
files — every mutant lives in your scratch (/fast/scratch/hyaku/mori-r81/Mo81M01Mutants) as
a copy of the committed file, and you run the copy.

Population: the tip-worktree bytes of (a) `.ufo/waves/round-80/count-c1.py`,
(b) `.ufo/waves/round-80/count-c3.py`, (c) `tools/mori-record-sweep.py` (if it is not there
when you start, mutate `.ufo/waves/round-81/count-c2.py` instead and say so).
For each file define ≥4 string-anchored mutants that invert a *graded* behaviour (e.g.
count only `unresolved`; accept the first summary; read only the first capability row;
drop the left boundary; count a directory as extra; count only the first binding; treat a
nonzero command exit as agreement; drop the `PENDING` scope to all tables). For each mutant:
1. run the file's own `--selftest` on the mutant (copied to the same relative path inside a
   scratch mirror; use `--root`/`--scratch` inside scratch),
2. record `killed` when the selftest exits nonzero or prints `fail>0`,
3. for any survivor, name the exact missing arm and what it would assert.
Write `.ufo/waves/round-81/w1/Mo81M01Mutants.md`: a table (file · label · old→new · selftest
rc · killed/survived) and a final `MUTANTS killed=K total=T survivors=S` line. A survivor is
a defect finding, not a failure of your seat: report it plainly with the arm text that would
kill it. Also state whether the unmutated copies are green first (a harness that grades a
red baseline proves nothing).
"""), )

ITEMS = [{"name": i["name"], "role": i["role"], "axes": i["axes"], "milestone": i["milestone"],
          "prompt": i["prompt"].replace("{lane}", LANE).replace("{round}", ROUND)} for i in ITEMS]

SPEC = {
    "wave": "mori-r81-w1",
    "milestone": ("Round 81 w1: build + first falsifiers for C1 (r80 counter exposures closed, "
                  "count-c1 fixtures) and C2 (record gate + D80 corrections); counters frozen in 6b021d29."),
    "axes": ["operability", "calibration", "coverage", "depth", "freshness", "adjacency"],
    "reportDir": ".ufo/waves/round-81/w1",
    "maxLanes": len(ITEMS),
    "context": CONTEXT.replace("{lane}", LANE).replace("{round}", ROUND),
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(SPEC, handle, indent=1)
    print("wrote %s items=%d" % (out, len(ITEMS)))
