#!/usr/bin/env python3
"""Build the round-80 wave spec (14 seats) for ufo-swarm-wave validation."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
WAVE = ".ufo/waves/round-80/w1"
SCRATCH = "/fast/scratch/hyaku/mori-r80"
W = f"{LANE}/.ufo/waves/round-80"

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
mori round 80 (attempt 1), wave w1 — build + first falsifiers for three frozen claims. The
lane is a fleet/host observability lane (detection and report only).

Read first (absolute):
- {W}/contract.md  — THE FROZEN CONTRACT: claims, predicates P-C1/P-C2/P-C3, targets,
  deliverable list, sweep-tool specification, bounds. It wins over this context.
- {W}/evidence/controls-r80.txt — the do-nothing controls (every claimed after-state is
  absent at entering `d5888922`).
- {LANE}/SCORECARD.md (the `## Axes` table; the capabilities tables; the r79 section at EOF)
- {LANE}/SKILL.md (the gate registry near line 1360; the vocabulary of instrument rows)
- {LANE}/corpus/QUALITY.md (the criteria; esp. 90, 154, 159, 161-164)
- {LANE}/PROVINCE.md (the province; the r30-named gap: many tools are not named there)

The three claims in one line each:
- C1 calibration — land `tools/mori-claim-sweep.py` (frozen interface in the contract § "Sweep
  tool specification") and correct the stale `18`-arm tally, so the self-assessment sweep reads
  `CLAIM_SWEEP mismatches=0`.
- C2 operability, sourced by S595 — `.ufo/waves/round-79/count-c2.py` gains one selftest arm per
  surviving mutant; the frozen six-mutant harness must read `MUTATION_C2 survivors=0`.
- C3 coverage — `PROVINCE.md` names every committed `tools/*.py|*.sh` instrument (14 of 55
  named at entering; target 55 of 55) with class, registry row and a one-line purpose.

# Bounds (all seats)
- Your tools start at the FLEET root, not the lane: every path you read, write or run is
  ABSOLUTE and under {LANE} unless this prompt names the fleet repo or a scratch copy.
  Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.
- You never commit, push, tag, stash, checkout, reset, switch, or run any mutating git/jj
  command in the lane or the fleet repo. Read-only git (`git -C {LANE} show/log/cat-file/
  rev-parse/ls-files/ls-tree`) is fine. The L1 integrates and commits; seats return files.
- Never edit `MANIFEST.json`, the fleet root, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`,
  the frozen round-80 counters (`count-c1.py`, `count-c3.py`, `mutate-c2.py`), `contract.md`,
  or any sibling lane repo.
- FILE OWNERSHIP: edit only the files your item names. If your work needs another file, write
  your version under {W}/ and name it in your report. Two seats never edit one file.
- Scratch discipline: every clone/temp/counter work dir lives under `{SCRATCH}/<your-name>/`
  (mkdir -p, pass it explicitly, `export TMPDIR` to it); delete it before you yield
  (`trap 'rm -rf -- "$S"' EXIT`); /tmp only for files under 50 MB. A tree left on disk is a
  defect you must report.
- Git fixtures: `D=$(mktemp -d -p {SCRATCH}/<your-name>) && git -C "$D" init -q`, every later
  call names `-C "$D"`, and `git -C "$D" rev-parse --show-toplevel` must equal `$D` before the
  first commit.
- Leaf seat: no subagent dispatch of your own (an executor may spawn exactly one read-only
  labrat probe for one falsifiable hypothesis; every other role is a leaf).
- Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help the
  task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate;
  record tool/version/channel/reason in your report). pacman is PAUSED host-wide: install via
  `uv tool`/`npx`/an official binary in `~/.local/bin`, never `pacman -S`, `-Sy`, `-Syu`,
  `-U`, `-R` or a partial upgrade; file the need in your report instead.
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
    return {"name": name, "role": role, "axes": ["calibration", "operability", "coverage"],
            "milestone": "round 80 w1: C1 claim sweep, C2 counter arms, C3 province inventory",
            "prompt": prompt}


ITEMS = [
    item("Mo80E01SweepTool", "executor", f"""\
Build `{LANE}/tools/mori-claim-sweep.py` — the self-assessment claim sweep (C1) — exactly to
the frozen interface in `{W}/contract.md` § "Sweep tool specification". Read that section
first; it is the spec. Python 3 standard library only, `python -I` safe, one file.

Summary of the frozen interface:
- `--root DIR` (required for a run), `--pins FILE`, `--carriers A[,B]`, `--selftest`, `--help`.
- Graded rows: `SCORECARD.md`'s `## Axes` table, every capabilities-table data row of
  `SCORECARD.md`, every `- [` checklist line of `SHONEN.md`.
- arm `unresolved`: backticked `corpus/…|tools/…|.ufo/…` tokens in graded rows must exist
  under `--root` (strip a `:N`/`:N-M` line suffix and an `@<sha>` rev suffix; ignore tokens
  inside fenced code blocks).
- arm `tally`: each `tallies` entry `{{tool_path: int}}` in the pins file must equal the tool's
  live `--selftest` count, parsed by the frozen grammar (`pass=N … fail=0`, `PASS (N cases)`,
  `PASS N/N`, `pass=N`); a failing or unparseable selftest is a setup error (rc 2), never a pass.
- arm `stale`: each literal in the pins file's `stale_literals` must occur 0 times in the
  carriers (default `SCORECARD.md,SKILL.md,SHONEN.md,LOG.md`).
- output: `CLAIM_SWEEP_MISMATCH <class> <carrier>:<line> <detail>` lines then
  `CLAIM_SWEEP mismatches=M unresolved=U tallies=T stale=S carriers=C pointers=P`; rc 0 iff
  M=0, 1 if M>0, 2 setup. Read-only: no writes, no socket, no `/tmp` path of its own.

Also write `{W}/claim-pins.json` (schema `mori-claim-pins-v1`) pinning
`tools/mori-control-receipt.py` to the live count you measure (`--selftest` prints 19 now) and
the stale literal `selftest 18 in-memory cases`; do NOT pin your own tool.

Acceptance (run all and paste outputs):
1. `python3 -I {LANE}/tools/mori-claim-sweep.py --selftest` -> `CLAIM_SWEEP_SELFTEST pass=P
   fail=0` with P >= 12, rc 0. Arms must include at least: a stale literal present/absent, a
   tally equal/mismatched, a dead pointer, a live pointer with `:12-14` and one with `@abcdef1`,
   a token inside a fenced block that must NOT count, a token naming a sibling lane path that
   must NOT count as a lane pointer, an unreadable carrier (rc 2), a missing pins file (rc 2),
   and a clean fixture tree (rc 0).
2. `python3 -I {LANE}/tools/mori-claim-sweep.py --root {LANE} --pins {W}/claim-pins.json` ->
   rc 1 at today's bytes, and the output's first mismatch line must be the SCORECARD
   control-receipt row's stale literal. Paste both.
3. `python3 -I {LANE}/tools/mori-claim-sweep.py --root {LANE} --pins {W}/claim-pins.json
   --carriers SCORECARD.md` after you temporarily copy SCORECARD.md to your scratch and
   fix the literal there (never on the lane file) -> `mismatches=0` rc 0: prove the sweep can
   reach zero on corrected bytes.

Report at the trailer path: the selftest tally, the two run receipts, the interface you built,
and any place the frozen spec was ambiguous and how you resolved it."""),

    item("Mo80E02Correct", "executor", f"""\
The r79 closure's routed defect D79-1: `{LANE}/SCORECARD.md`'s capabilities row for the
control-receipt guard states `selftest 18 in-memory cases` while the committed
`tools/mori-control-receipt.py --selftest` prints `pass=19 fail=0`. Discharge it and register
the round's new sweep instrument.

You own exactly two files: `{LANE}/SCORECARD.md` and `{LANE}/SKILL.md`.

1. `SCORECARD.md`: correct that row's tally to `19` in place, keeping every other byte of the
   row. Append, at end of file, a `## Round-80 correction (D79-1, calibration)` paragraph that
   names the r79 spot-check (`corpus/lessons/round-79-verifier-spotcheck.md`, routed defect
   D79-1), the entering bytes, the live count, and the fact that no score moved. Then append a
   capabilities-table row for `tools/mori-claim-sweep.py` (first-working round 80, evidence =
   its selftest tally + the sweep run), and a short `## Round 80` section carrying the round's
   three claim rows in the same shape as the round-79 section (leave the "after" cells to be
   filled by the L1: write `PENDING` there and say so).
2. `SKILL.md`: append gate-registry row 14 for `tools/mori-claim-sweep.py` at the registry home
   (after row 13, the control-receipt guard, near line 1365). The row must carry all eight
   registry fields: name, kind (`gate`), entry command, verdict map (rc 0/1/2), self-test cell
   with the landed tally, pinned values, write scope (stdout only), owner (`mori`). Mirror the
   shape of row 13 exactly. Do not touch any other row.

Rules:
- Do not edit the r79 artefacts; do not rewrite history; the correction rides as a named
  addition plus the one in-place cell. Keep every line you add free of literal `|` inside cells.
- Run `python3 -I {LANE}/tools/mori-control-receipt.py --selftest` yourself and cite its line.
- After your edits run `python3 -I {LANE}/.ufo/waves/round-80/count-c1.py d5888922` — it must
  still read `C1=unmet` (the tool does not exist at that rev; your SCORECARD edit cannot make
  the entering claim pass) and state why in your report.
- Report every other occurrence you find of a superseded control-receipt tally across
  `SCORECARD.md`, `SKILL.md`, `SHONEN.md`, `LOG.md` with `file:line` (`grep -n` receipts).

Report at the trailer path: the diffs, the greps, the live selftest line, and your judgement of
whether the D79-1 class appears anywhere else in the two files."""),

    item("Mo80E03Arms", "executor", f"""\
C2 (operability): `.ufo/waves/round-79/count-c2.py`'s selftest must kill the mutants its own
frozen harness finds. The harness is `{W}/mutate-c2.py` (frozen; read it first). At the
entering bytes it reports `MUTATION_C2 survivors=2 killed=4 total=6` with `drop_admitted` and
`cut_clause_boundary` surviving.

You own exactly one file: `{LANE}/.ufo/waves/round-79/count-c2.py`.

1. Add THREE selftest arms to `selfcheck()` — one per class the r79 mutation seat named, which
   also kills the two survivors above:
   a. a non-admitted round BELOW the ceiling must not win: fixture rounds
      `[(60, False, {{"coverage": "improved"}}), (47, True, {{"coverage": "improved"}})]` with
      the coverage cell `round 47 (improved, score held)`, expect met=True;
   b. a verdict word AFTER the first `;` must not count: depth cell
      `round 78 (score held); round 40 (improved, score held)`, expect met=False;
   c. a later `round N` in the cell must not win: operability cell
      `round 40 (score held); round 78 (improved, score held)`, expect met=False.
   Keep the existing four arms and their labels byte-identical.
2. Change ONLY the selftest region: `def selfcheck(` to `def main(`. The predicate, the
   `grade()`/`expectations()` logic, the CLI, the output grammar and the module docstring stay
   byte-identical. Prove it: `git -C {LANE} diff -U0 -- .ufo/waves/round-79/count-c2.py` must
   show hunks only inside that region (paste the diff).
3. Acceptance: `python3 -I {LANE}/.ufo/waves/round-79/count-c2.py --selftest` -> 
   `C2_COUNTER_SELFTEST pass=7 fail=0` rc 0, and
   `python3 -I {W}/mutate-c2.py --rev <your-worktree-state>` is not possible before the L1
   commits — instead run the harness against a temp commit: clone the lane into
   `{SCRATCH}/Mo80E03Arms/clone` (`git clone --shared {LANE} <dir>`), make a fixture commit
   there with your edit under lane identity is NOT allowed — use `git -C <dir> -c
   user.name=t -c user.email=t@t commit` ONLY inside that scratch clone, then run
   `python3 -I {W}/mutate-c2.py --rev <that commit> --repo <dir>` and paste
   `MUTATION_C2 survivors=0 killed=6 total=6`. Delete the clone before you yield.

Report at the trailer path: the diff, the before/after harness lines, the selftest tally, and a
note on whether any of your three arms is vacuous (would pass on the mutant too)."""),

    item("Mo80E04Inventory", "executor", f"""\
C3 (coverage): `{LANE}/PROVINCE.md` names 14 of the 55 committed `tools/*.py|*.sh`
instruments. Close the gap the lane has carried since round 30 (ScoutProvinceStale items 4-5)
with an APPEND-ONLY section.

You own exactly two files: `{LANE}/PROVINCE.md` and `{W}/inventory-src.txt`.

1. Build the population yourself: `git -C {LANE} ls-tree -r --name-only HEAD -- tools/` and
   keep only `tools/<name>.py|*.sh` (fixtures and directories excluded). Expect 55.
2. For EVERY such file, establish: its class (`gate` / `probe` / `counter` / `regression` /
   fixture-helper), its SKILL gate-registry row (number or name, `—` if none), and a one-line
   purpose. Ground each line in the file itself (docstring/`--help`) or its SKILL registry row
   — never invent. Rows with no registry row: say what class the code shows and name the
   evidence (`grep -n` of the docstring line).
3. Append `## Instrument inventory (round 80)` at the end of `PROVINCE.md` (append-only: not one
   byte above it changes) with a table `| tool | class | registry row | purpose |` holding one
   row per instrument, preceded by two sentences stating what the table is (an inventory of
   the lane's own read-only instruments) and what it is not (not a scope expansion, not a
   claim that every instrument is a census surface).
4. Write `{W}/inventory-src.txt`: the raw population, the classification evidence per row, and
   the count.
5. Acceptance: `python3 -I {W}/count-c3.py d5888922` must still read `C3=unmet` (entering rev),
   and after your edit run `python3 -I {W}/count-c3.py $(git -C {LANE} rev-parse HEAD)` is not
   yet possible — instead copy your edited PROVINCE.md into a scratch clone, commit it there
   under `t <t@t>`, and run `python3 -I {W}/count-c3.py <that commit> --repo <clone>` -> paste
   `C3=met named=55 present=55 missing=0`. Delete the clone.

Report at the trailer path: the row count, the classification method, the met/absent evidence
for registry-less instruments, and the scratch-clone `C3=met` line."""),

    item("Mo80Sc01Recon", "scout", f"""\
Read-only reconnaissance for the round's three claims — the data-walk the L1's planner seat
would otherwise do. Gather, with commands and outputs:

1. **C1 population.** For `{LANE}/SCORECARD.md` (capabilities tables + `## Axes`) and
   `{LANE}/SHONEN.md`: enumerate every backticked `corpus/…|tools/…|.ufo/…` pointer and every
   stated selftest tally. Report how many pointers there are, how many resolve TODAY, and every
   pointer that does not (file:line + token). Report every place a superseded control-receipt
   arm count (`18`) still appears across `SCORECARD.md SKILL.md SHONEN.md LOG.md README.md`.
2. **C1 risk.** Does `SCORECARD.md`'s adjacency `## Axes` cell cite anything that does not
   resolve? The r79 spot-check (D79-3) claimed it cited a non-existent
   `corpus/lessons/round-19-verifier-spotcheck.md`; check both the cell and whether
   `MANIFEST.json@63729047` resolves in the fleet repo (`git -C /home/vgpnk/Projects/shokunin
   cat-file -e 63729047:MANIFEST.json`) and `rounds[398]` is mori round 19. State the verdict.
3. **C2 population.** List every selftest arm label currently inside
   `{LANE}/.ufo/waves/round-79/count-c2.py` `selfcheck()`, and state which of the three r79
   reported survivors are already killed at the entering bytes (the harness is
   `{W}/mutate-c2.py`; run `python3 -I {W}/mutate-c2.py --rev d5888922`).
4. **C3 population.** The `tools/*` population at `d5888922` (count + list), the tools
   `PROVINCE.md` already names, and the tools that are NOT instruments (fixture helpers,
   round-only regressions) with the evidence for the exclusion.
5. **Assimilation check.** Does `/home/vgpnk/Projects/shokuknow/merge/mori/` still hold the
   staged package, and what does `.ufo/l0-questions.md` say about its id collision (grep the
   mori lines)? Report the status, do not adopt anything.

Read-only: write nothing outside your `Report:` path and your scratch dir."""),

    item("Mo80Sc02Source", "scout", f"""\
Source work for C2's grounding (S595): open, pin and quote-locate one source.

Candidate: `https://arxiv.org/abs/2102.11378v2` ("Practical Mutation Testing at Scale"). Do the
lane's gate in this order and paste every step:

1. **Duplicate sweep BEFORE the fetch** (the r69 rule): `grep -n` `corpus/SOURCES.md` for the
   exact URL, for `2102.11378`, and for `mutation test` (case-insensitive); name the nearest
   held rows. Report hits.
2. **Fetch** the abstract page twice (your fetch + one re-fetch) into
   `{SCRATCH}/Mo80Sc02Source/`; `sha256sum` and `wc -lc` both copies; they must be identical
   byte-for-byte. If arxiv.org is unreachable, say so with the curl code and stop — never
   substitute another source silently.
3. **Locate the quote.** Find the abstract's first sentence and give its `grep -n` line number
   in the pinned copy plus the exact contiguous span. The quote must be <= 25 words; count them
   (`wc -w`). Propose the shortest span that still supports "mutation analysis assesses a test
   suite's adequacy by measuring its ability to detect small artificial faults".
4. **Verify with the lane's own checker** if it applies: try
   `python3 -I {LANE}/tools/mori-anchor-check.py --pin <copy> --check '<spec>'` and report the
   verdict or the reason it does not apply to an HTML page.
5. Copy the pinned bytes to `{LANE}/corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html`
   and write `{LANE}/corpus/evidence/sources-r80/README.md` (one short paragraph: what the pin
   is, the sha256, the byte/line count, the fetch date, and that it is public-document bytes).
6. State what the abstract does NOT support (no claim about equivalent mutants, no claim about
   any Python tool, no claim that a green selftest is adequate) — the entry's Limits will quote
   this list.

Report at the trailer path: the sweep, both shas, the line number, the word count, the checker
verdict, and the not-supported list."""),

    item("Mo80S01Row", "scribe", f"""\
Write the SOURCES row for S595 and its index row (C2's sourced claim).

You own exactly two files: `{LANE}/corpus/SOURCES.md` and `{LANE}/corpus/README.md`.

1. Append row `S595` at the end of the SOURCES registry, 11 cells, exact current schema (see
   the header row and `S594` at `corpus/SOURCES.md:375` for shape). Content:
   - source: `Practical Mutation Testing at Scale — arXiv:2102.11378v2 —
     https://arxiv.org/abs/2102.11378v2`
   - kind `paper`; tier `A` with scope narrowed to what the abstract states
     (`mutation analysis's own definition as a test-adequacy criterion`); scope cell says so.
   - anchor: the pinned copy `corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html` with the
     `grep -n` line of the abstract sentence, the sha256, and the byte/line count (take them
     from `{W}/../round-80/w1/Mo80Sc02Source.md` if it exists, else re-measure yourself —
     never copy a hash you did not see printed).
   - teaches: one grounded benefit, <= 25 words of paraphrase, no quote marks needed here.
   - status `mined`; opened `2026-11-04`; recheck `365d`; used-by
     `corpus/knowledge/mutation-adequacy-r80.md`.
   No cell may contain a literal `|`. Verify with the census:
   `awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ && NF!=13 {{n++}} END{{print n+0}}'
   corpus/SOURCES.md` -> `0`, and
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin mori` -> rc 0 (35 tolerated W04 warnings).
2. Append one index row to `{LANE}/corpus/README.md` naming
   `corpus/knowledge/mutation-adequacy-r80.md` in the same shape as the r79 row (`:865`).
3. If `S595` is already taken, take the next unused id and say which in your report.

Report at the trailer path: the row bytes, the two census commands with their output, and the
exact id you used."""),

    item("Mo80S02Entry", "scribe", f"""\
Write the knowledge entry that grounds C2, plus the two QUALITY rules this round lands.

You own exactly two files: `{LANE}/corpus/knowledge/mutation-adequacy-r80.md` and
`{LANE}/corpus/QUALITY.md`.

1. Entry `mutation-adequacy-r80.md`, opening with the provenance trio (`source:`, `verified-at:`,
   `recheck:`) per CORPUS.md: `source:` cites S595, the arXiv URL and the pinned copy's sha;
   `verified-at: 2026-11-04`; `recheck: 365d`. Then:
   - K1 what mutation analysis measures (the abstract's own words, paraphrased, with the
     located line from the pin);
   - K2 the consequence for a selftest: an arm that no mutant can turn red is not evidence the
     arm exists — one mutant per surviving mutation is the repair, and the grade is the
     selftest's own verdict;
   - K3 the direction of the inference (a killed mutant proves an arm discriminates; a survivor
     proves only that no current arm discriminated that edit) and the cost side (every mutant
     costs one selftest run, so the set is bounded and named);
   - K4 the lane's own instance: the r79 counter's 4 arms, the 6-mutant harness at `d5888922`
     reading `survivors=2`, and what a green selftest that prints `pass=0 fail=0` under a
     missing `TMPDIR` means (a setup failure, not a pass — the lane observed this in
     `tools/mori-disk-rate.py` and `tools/mori-round41-calibration.py` on 2026-11-04).
   - `## Limits`: the abstract does not discuss equivalent mutants, does not name any Python
     tool, and does not support a completeness claim; a surviving mutant is a lead for a human
     judgement, never proof that a test is missing. `## Boundaries`: this is the lane's own
     gate-quality craft, not a claim about another lane's tests.
2. `QUALITY.md`: append exactly two criteria at end of file, numbered in the file's own
   sequence (read the last number first):
   - the survivor-as-lead rule (a selftest arm added for a named surviving mutant must fail
     on that mutant and pass on the real bytes — cite the r80 harness);
   - the D79-4 limit record: the control-receipt guard enforces section-level textual
     co-presence, not command relevance — a `$ <any text>` line binds a section and
     decimal/exponent-only values are outside the declared integer grammar (record it beside
     the QUALITY 164 rule that introduced the guard).
   Faithfully cite `corpus/lessons/round-79-verifier-spotcheck.md` for D79-4. Do not renumber or
   rewrite existing criteria.

Report at the trailer path: the entry's full text path, the two QUALITY numbers you used, and
the grep proving they are appended (not inserted)."""),

    item("Mo80S03Lesson", "scribe", f"""\
Draft `{LANE}/corpus/lessons/round-80.md` — the round's mined mistake, its Gate scaffold and
the census record. The L1 fills the final numbers; you write everything that does not depend on
the landed revision.

You own exactly one file: `{LANE}/corpus/lessons/round-80.md`.

Sections, in this order:
1. Front matter: `# Round 80 — mori (L1 MoriR80): three claims …`, author, round, date,
   entering revision `d58889220d3c6a18d461f2d31b5ab162ffef1e4e`, and what the round ruled out.
2. `## Gate` — one section per NEW source row (S595): the URL, the access date 2026-11-04, the
   <=25-word located quote with its line number and word count, the pinned copy path + sha256,
   the pre-fetch duplicate sweep result, and the verdict (admitted, scope narrowed). If the
   source seat's report (`{W}/w1/Mo80Sc02Source.md`) exists, use its shas; otherwise state
   `PIN PENDING — filled by the L1` rather than inventing a hash.
3. `## Mistakes` — mine ONE mistake with class · evidence pointer · captured-by · fix. The
   mistake to mine is the r79 spot-check's D79-1 class (a corrected fact left standing in a
   sibling file: `SKILL.md` said 19, `SCORECARD.md` said 18 after the tool grew an arm), which
   is a spot-check disagreement, not a new invention. Give it the round's own fix (the sweep
   instrument + the corrected row) and show the fix can fail: state the command that is red on
   the entering bytes and green after, and paste the entering line
   (`grep -c 'selftest 18 in-memory cases' SCORECARD.md` -> 1). Add a SECOND mistake only if
   you can name one from this round's own evidence with the same four fields.
4. `## Census` — paste the round-start census command and its exit code, obtained by running
   it yourself:
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin mori`
   Record the row count before (`grep -cE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|'
   corpus/SOURCES.md`) and note that the after-value is filled by the L1.
5. `## Refusals` — the things this round declined and why: the `merge/mori/` package (r61 L0),
   the boot-scoped events window and any SOURCES-wide label sweep (the mori|round-65 and
   round-73 L0s), touching `tools/mori-control-receipt.py`'s selftest (a registered tally-pinned
   instrument; the r79 closure made D79-5 conditional), and any axis score change (no closure
   states a new number).

Report at the trailer path and name every placeholder the L1 must fill."""),

    item("Mo80Cn01Siblings", "connector", f"""\
Sibling-overlap scan for the round's three claims: does another lane already hold the same
ground, and is any of this round's work a duplicate?

Read-only. Check, with file:line evidence:
1. **C1 (self-assessment claim sweep).** Search the fleet for an existing instrument that
   resolves a lane's own declared claims against committed bytes: `grep -rn` for
   `claim`, `self-assessment`, `resolve`, `pointer` under `/home/vgpnk/Projects/shokunin/*/tools/`
   and `*/scripts/`. Name the nearest three and state `adjacent`/`duplicate` per claim. Check
   kumitate (which owns orchestration/tooling) and the fleet `scripts/hyaku/` helpers.
2. **C2 (mutation adequacy of a selftest).** Does any lane already run mutation testing or own
   a mutant harness? Check `kumitate`, `tameshi`, `protocol`, and the fleet `scripts/`. Report
   every hit and whether the r80 harness duplicates it.
3. **C3 (province instrument inventory).** Does another lane keep a tools inventory in its
   PROVINCE/SKILL that mori's shape should match? Quote the closest one's shape (2-3 lines) so
   the scribe can align formats.
4. **Boundary.** For each claim state whether it stays inside mori's province
   (`{LANE}/PROVINCE.md:1-20`): detection/report only; no dispatch, OS state, endpoint health or
   credential material.
5. Name any sibling artifact that would be *harmed* by mori's edit (a lane whose files mori's
   sweep might scan, or a shared `scripts/` file) — mori edits none of them.

Report at the trailer path: the three claims' verdicts with evidence, and the closest-match
shapes."""),

    item("Mo80R01Counter", "reviewer", f"""\
Attack C1 and C3 as an adversary: the counters and the instruments they will grade.

Read `{W}/contract.md` (frozen predicates) and `{W}/evidence/controls-r80.txt` first.

1. **Counter selftests.** Run `python3 -I {W}/count-c1.py --selftest` and
   `python3 -I {W}/count-c3.py --selftest`. For each counter, name one fixture it does NOT
   exercise that could flip its verdict, and prove it with a scratch fixture of your own (build
   it under `{SCRATCH}/Mo80R01Counter/`, own git repo, `t -c user.name=t -c user.email=t@t`).
   Candidates: `count-c1` — a sweep that exits 0 but prints `mismatches=0` with a stale row
   (covered?), a row tally stated twice, a SCORECARD with no capabilities table, a sweep that
   prints the summary twice; `count-c3` — a PROVINCE naming a tool in a fenced code block, a
   tool named with a trailing colon, a directory under `tools/` with a `.py` suffix, a tool
   named in another lane's relative path (must not count).
2. **The sweep's own arms.** When `{LANE}/tools/mori-claim-sweep.py` exists (the executor seat
   builds it in this same wave; if absent, say so and attack the frozen spec instead): run its
   `--selftest`, then plant a defect it should catch in a scratch copy of the lane
   (dead pointer, stale literal, mismatched pin) and confirm it goes red; then plant a benign
   variant (a pointer with `:12-14`, a token in a fenced block) and confirm it stays green.
   Report every false negative and false positive with the bytes.
3. **Predicate identity.** For each of P-C1/P-C2/P-C3 state whether the contract sentence, the
   counter's code path and the printed receipt label are the same claim. Name any gap (the
   r79 closure graded three claims this way; a gap is a routed defect now, not later).
4. Independent re-derivation: run `python3 -I {W}/mutate-c2.py --rev d5888922` and
   `python3 -I {W}/count-c3.py d5888922` yourself and report the lines — do not read them from
   the controls receipt.

Report at the trailer path: findings with severity, the fixtures you built, and a clear
`no finding` per numbered item where you found none."""),

    item("Mo80C01Contract", "critic", f"""\
Falsify the round's claim design before the data is final.

Read `{W}/contract.md`, `{W}/evidence/controls-r80.txt`, `{LANE}/SCORECARD.md` (`## Axes`, the
capabilities tables), and `{LANE}/.ufo/waves/round-79/contract.md` (the r79 shape it follows).

1. **Do-nothing control.** For each claim, is the target reachable without the claimed work?
   Build the cheapest counter-example you can and report it: C1 — could the SCORECARD row alone
   make `count-c1` read met without a working sweep (no: the counter runs the sweep blob at R —
   verify that reading)? C2 — could the harness read `survivors=0` by a selftest that always
   exits 1 (a vacuous counter-killer)? Check: `mutate-c2` calls the selftest and grades the
   verdict — a selftest that always fails would kill every mutant and also fail the real bytes;
   verify the real bytes' selftest is green at the worked revision, and say whether the
   predicate needs an explicit "and the unmutated selftest passes" clause (the r79 closure
   precedent: a counter that cannot be red on real bytes is broken). C3 — could a mechanical
   dump of 55 rows pass with wrong classifications? State whether the predicate (names + paths)
   admits that and whether the claim's text overreaches.
2. **Axis fit.** Are the three axes distinct and is at least one on the lowest non-retired axis
   (depth/freshness/calibration = 5)? Is C1 really calibration (a mismatch count between the
   lane's self-assessment and observed repo state — AXES.md), C2 operability, C3 coverage?
3. **Sizing.** Is each after-state one concrete value a closure can re-derive with one command
   over committed bytes? Name any universal clause ("all", "every", "no harm anywhere") that
   the counting command does not enumerate.
4. **Harm.** Does any claim trade another axis? Check: does C3's inventory (55 rows) risk
   asserting scope it does not own, or stale facts? Does C1's sweep hard-code a pin that will
   rot (the tallies pin is a maintenance cost — say how the successor round must treat it)?
5. **Same-sentence rule.** Quote contract sentence, counter output label and receipt label per
   claim; name every mismatch in wording that could let a closure read a different claim.

Report at the trailer path: one verdict per claim (`sound` / `needs the named clause` /
`unsound`), the counter-examples you built, and the exact clause text you recommend — the L1
freezes before any seat scores."""),

    item("Mo80M01Mutant", "mutation-tester", f"""\
Mutate the round's own new gates and report survivors with the exact hunk.

Targets (attack in this order; skip a target that does not exist yet and say so):
1. `{LANE}/tools/mori-claim-sweep.py` — if the executor seat landed it in this wave: at least
   six mutants, one per frozen arm and boundary: (a) drop the `:line` suffix stripping,
   (b) drop the `@rev` stripping, (c) make the fenced-block skip a no-op, (d) make the tally
   comparison `>=` instead of `==`, (e) make a missing carrier default to empty instead of
   rc 2, (f) make `mismatches` count only `unresolved`. For each: run `--selftest`; KILLED iff
   it goes red. Paste hunks and verdicts.
2. `{LANE}/.ufo/waves/round-80/count-c3.py` — three mutants: (a) drop the sibling-lane skip,
   (b) compare only `named >= present` (allow extra), (c) count directories as instruments.
3. `{LANE}/.ufo/waves/round-79/count-c2.py` after the executor's arms land — run the frozen
   harness yourself: `python3 -I {W}/mutate-c2.py --rev <scratch clone commit>` and paste it.
4. Report every surviving mutant with the class it belongs to and the arm that would kill it —
   a survivor found this round is a routed defect for round 81, not a reason to change the
   round's predicate.

Never edit the lane files: copy to `{SCRATCH}/Mo80M01Mutant/`, mutate the copy, run it. Any
scratch git repo is `git -C <dir> -c user.name=t -c user.email=t@t`.

Report at the trailer path: the mutant table (target, mutant, hunk, killed/survived), and the
survivor analysis."""),

    item("Mo80R02Probe", "reviewer", f"""\
One bounded empirical hypothesis, independently of the seats asserting the claims:

**H: the round's deliverable shape can fail — a self-assessment sweep that grades tallies will
report the r79 stale-tally class on a tree that carries it, and report clean on the same tree
with the tally corrected, with no other change.**

Build it, read-only, under `{SCRATCH}/Mo80L01Probe/`:
1. `git -C {LANE} archive d5888922 | tar -x -C <dir>` — the entering tree.
2. If `{LANE}/tools/mori-claim-sweep.py` exists (built in this wave), run it over that tree with
   the pins file and record rc + the first mismatch line. Then edit ONLY the SCORECARD row's
   `18` to `19` in your scratch copy and re-run: record rc + `CLAIM_SWEEP mismatches=`.
3. If the sweep does not exist, prove the same shape with two pinned greps: the literal
   `selftest 18 in-memory cases` present (rc/line) and absent after the one-number edit, and
   say explicitly that this is a degraded probe of the same hypothesis.
4. Add one adversarial variant: correct the number but leave a *different* dead pointer
   (`corpus/lessons/does-not-exist.md` planted into a capabilities row in the copy) and check
   whether the sweep's `unresolved` arm fires (if it exists) or whether the probe cannot
   distinguish (say so — that is a finding).
5. Report the sha256 of the two copies' `SCORECARD.md` so the delta is one edit.

Report at the trailer path: hypothesis, the two runs, the adversarial variant, and the verdict
(`supported` / `not supported` / `degraded probe`). Delete your scratch tree before yielding."""),
]

spec = {
    "wave": "mori-r80-w1",
    "milestone": "Round 80 w1: build + first falsifiers for C1 (claim sweep + D79-1), C2 "
                 "(count-c2 arms vs the 6-mutant harness), C3 (province instrument inventory); "
                 "counters frozen in 57451ecb.",
    "axes": ["calibration", "operability", "coverage", "depth", "freshness", "adjacency"],
    "reportDir": WAVE,
    "maxLanes": 14,
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
    with open(out, "w") as fh:
        json.dump(spec, fh, indent=1)
    print(out, len(ITEMS), "items")
