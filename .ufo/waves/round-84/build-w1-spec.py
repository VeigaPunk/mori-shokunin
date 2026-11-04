#!/usr/bin/env python3
"""Build mori round-84 wave w1 spec (one v1 wave, 14 seats, band 8-16).

Writes .ufo/waves/round-84/w1-spec.json. The Godspeed directive bytes are copied verbatim from
the round-83 spec (the host binding), never retyped. Every item prompt is self-contained; shared
rules ride the wave context.
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
ROUND = LANE + "/.ufo/waves/round-84"
R83 = LANE + "/.ufo/waves/round-83/w1-spec.json"
FREEZE = "daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4"
ENTERING = "5adf4337b6510dd246b247092c11cbaa97c930d3"

with open(R83, encoding="utf-8") as handle:
    r83 = json.load(handle)
GODSPEED = r83["context"].split("\n\n# Goal", 1)[0]
assert GODSPEED.startswith("/skill:godspeed"), GODSPEED[:40]

CONTEXT = GODSPEED + """

# Goal
mori round 84 (attempt 1), wave w1 — implement, record and first-falsify THREE frozen claims.
mori is a fleet/host observability lane: detection and report only. The freeze commit is
`%(freeze)s`; the counters were frozen there before any seat ran. The entering revision is
`%(entering)s`.

Read first, in this order (absolute paths):
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/contract.md — THE FROZEN
  AUTHORITY: P-C1, P-C2, P-C3, the four-mutant table with exact anchors, the equivalence coupling
  proofs, the all-anchor-rows rule and its three fixtures, the live-delta classes, the targets and
  the do-nothing controls.
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/evidence/controls-r84.txt — the
  measured entering controls (C1 harness=absent, C2 arm=absent, C3 delta=absent, all rc 1).
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c1.py, count-c2.py,
  count-c3.py — the three frozen counters that grade this round (each has --selftest).
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/w1/Mo83R01C1.md §6 — the
  extra-mutant sweep (M24a-M24d) this round's C1 population comes from.
- /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-83-verifier-spotcheck.md
  (`## Routed defects the lane must fix next round`: D83-1 evidence gap, D83-2, D83-3).
- /home/vgpnk/Projects/shokunin/mori-shokunin/SCORECARD.md `## Planned (round 84)`.

# Round claims (frozen before this wave; do not change them)
- C1 operability (7): the r83 counter family's four extra mutants (M24a-M24d) get the failing arm
  each needs, with M24c/M24d adjudicated equivalent behind byte coupling proofs. Target
  `C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green detector=green`.
  Entering: `C1=unmet harness=absent`; population control at the freeze: `C1=unmet mutants=4
  killed=0 equivalent=2 survivors=2`.
- C2 calibration (5, tied lowest): the record sweep's revision arm grades EVERY row the anchor
  selects on both sides, with two defeated ambiguous fixtures. Target `C2=met arm=all-rows
  defeated=2 fixtures=3/3 bindings=3 revisions=0 arms=44`. Entering: `C2=unmet arm=absent`.
- C3 depth (5, tied lowest): the r83 drift counter's live reading becomes a per-token delta
  classification (absent-live / added-live / class-changed / agreed). Target `C3=met
  delta=classified tokens=64 classified=union residual=0 live=derived`. Entering: `C3=unmet
  delta=absent`.

# Shared rules (binding on every seat)
- Write scope: /home/vgpnk/Projects/shokunin/mori-shokunin only, and inside it only the paths your
  item names. Absolute paths in every tool call: your tools start at the FLEET root, so a relative
  path lands in the wrong repo. Never write to /home/vgpnk/Projects/shokunin (fleet root), another
  lane's repo, MANIFEST.json, `.ufo/state/`, `.ufo/watchdog.log`, or `.scratch/`.
- Never commit, push, or run a mutating git/jj command in the LANE repo: no `git add`, `git
  commit`, `git checkout`, `git reset`, `git stash`, `git push`, and no mutating `jj` command.
  Read-only git (`log`, `show`, `diff`, `status`, `ls-tree`, `cat-file`, `rev-parse`, `clone
  --shared`) is fine. The L1 owns every lane commit. A scratch clone under your own scratch dir is
  a fixture: commits there use `-c user.name=t -c user.email=t@t` and are allowed.
- Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/mori-shokunin —
  write it at /home/vgpnk/Projects/shokunin/mori-shokunin/<that path>.
- Scratch: create your work dir under /fast/scratch/hyaku/mori-r84/<your seat name>/ and delete it
  before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell). Never write under /tmp; a /tmp path is
  never citable evidence. Use `git clone --shared` instead of full clones; never mirror the whole
  lane. `HYAKU_SCRATCH` defaults to /fast/scratch/hyaku.
- Fixture git repos: `D=$(mktemp -d)` then `git -C "$D" init -q`; assert
  `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit; every later
  git/jj call names `-C "$D"`.
- Detection and report only: no lane, OS, unit, service, credential, harness or orchestration
  state may be changed. mori never remediates.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the
  task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate) and
  record tool/version/channel/reason in your report. pacman is PAUSED host-wide: never run a
  pacman transaction of any kind (`-S`, `-Sy`, `-Syu`, `-U`, `-R`); use `uv tool`, `npx`, or an
  official binary in ~/.local/bin, or file an L0 question instead.
- Never message `agent://all`. Message only your own L1 (`agent://MoriR84`) for a blocker.
- Do not spawn subagents except an executor's single read-only `labrat` probe.
- Your final report must name: what you changed/produced with absolute paths, the exact commands
  you ran with their output, what you verified, what you could not verify, and any defect you
  found in another seat's bytes. An unrun check has not passed.
""" % {"freeze": FREEZE, "entering": ENTERING}

ITEMS = [
    {
        "name": "Mo84E01C1Arms",
        "role": "executor",
        "milestone": "round 84 w1: the two failing arms for M24a/M24b",
        "prompt": """
Give `.ufo/waves/round-83/count-c1.py` the two failing selftest arms the round-84 C1 counter
requires.

Frozen authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/contract.md`
P-C1, and the counter `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c1.py`.

File you may edit: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c1.py`,
`selfcheck()` only. Do not touch `grade()`, `green()`, `killed()`, `MUTANTS`, `EQUIVALENT`, any
other file, or the two mutated lines: `killed_n = total - survivors - equivalent` and
`return rc == 0 and "fail=0" in out and not FAIL.search(out)` must still occur exactly once.

Arms to add (labels frozen):
1. `blind_case_tally` — grade a two-mutant fixture with one sensitive mutant (killed) and one blind
   mutant (survives); the tail must read `killed=1 survivors=1 total=2` and the run must be unmet.
   Under the M24a mutant (`killed_n = total - equivalent`) the tail reads killed=2, so the arm
   fails and the mutant is killed.
2. `green_requires_fail_zero` — grade a one-mutant fixture whose pristine exits 0 printing exactly
   `SELFTEST skipped` (no `fail=0` token) with a blind mutant; the tail must read `pristine=red`
   and the run must be unmet. Under the M24b mutant (green() drops the `"fail=0"` requirement) the
   pristine reads green, so the arm fails and the mutant is killed.

Use the existing `write()`, `disk()` and `grade()` helpers inside that `selfcheck()`. Keep every
existing arm byte-identical and keep the existing `C1_COUNTER_SELFTEST pass=%d fail=%d` summary.

Verify (put every command and its output in your report):
- `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c1.py --selftest`
  → expect `C1_COUNTER_SELFTEST pass=8 fail=0`, rc 0.
- Shown able to fail, in scratch: `git clone --shared /home/vgpnk/Projects/shokunin/mori-shokunin
  $S/lane`, copy your edited file into the clone, `git -C $S/lane -c user.name=t -c user.email=t@t
  commit -aqm probe`, then
  `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c1.py <probe-rev>
  --repo $S/lane` → expect `C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4
  pristine=green detector=green` rc 0. Never commit in the lane repo.
Report: `.ufo/waves/round-84/w1/Mo84E01C1Arms.md`.
""",
    },
    {
        "name": "Mo84E02C2Rows",
        "role": "executor",
        "milestone": "round 84 w1: the all-anchor-rows rule and its four arms",
        "prompt": """
Implement the all-anchor-rows rule in the record sweep and its four selftest arms.

Frozen authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/contract.md`
P-C2, and the counter `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c2.py`.

File you may edit: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py` only.

Required behaviour: `revision_sweep` stops selecting the first matching row. A binding's
`row_contains` selects EVERY row carrying that string:
- carrier side: every selected row must satisfy `contains_value(row, key, value)`; no selected row
  → `('revision', carrier, 1, 'row-value')`; otherwise the first failing row's line number →
  `row-value`, and no git call is made when the carrier side fails;
- revision side: after `git show <rev>:<path>`, every row of the blob carrying the anchor must
  satisfy `contains_value`; no anchor row or any failing row → `('revision', carrier,
  <first failing line or 1>, 'rev-bytes')`.
Add a module-level marker string `ALL_ANCHOR_ROWS` (comment or docstring) and one small pure
helper (for example `anchor_rows(text, row_contains)`) used by both sides. Keep
`contains_anchored()` or its successor's documented meaning for the tool's own docstring.

Four new arms in `selftest()` (use the existing `revision_case` helper; its `blob=` argument is the
revision-side text): `carrier-all-anchor-rows-green` (two carrier rows both stating the value →
clean), `carrier-all-anchor-rows-red` (second carrier row states another value → `row-value` at
that row, no git calls), `rev-all-anchor-rows-green` (blob carries a second anchor row that also
states the value → clean), `rev-all-anchor-rows-red` (blob carries a second anchor row with another
value → `rev-bytes`). Keep all 40 existing arms passing unchanged: 40 → 44.

Verify (put every command and output in your report):
- `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --selftest`
  → `RECORD_SWEEP_SELFTEST pass=44 fail=0`, rc 0.
- Shown able to fail, in scratch: `git clone --shared /home/vgpnk/Projects/shokunin/mori-shokunin
  $S/lane`, copy your edited tool into the clone, `git -C $S/lane -c user.name=t -c user.email=t@t
  commit -aqm probe`, then
  `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c2.py <probe-rev>
  --repo $S/lane` → expect `C2=met arm=all-rows defeated=2 fixtures=3/3 bindings=3 revisions=0
  arms=44` rc 0 (the counter needs the graded clone's worktree to equal the graded revision, so
  commit before running).
Report: `.ufo/waves/round-84/w1/Mo84E02C2Rows.md`.
""",
    },
    {
        "name": "Mo84E03C3Delta",
        "role": "executor",
        "milestone": "round 84 w1: per-token live-delta classification",
        "prompt": """
Add the per-token live-delta classification to `.ufo/waves/round-83/count-c2.py`.

Frozen authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/contract.md`
P-C3, and the counter `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c3.py`.

File you may edit: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c2.py`
only.

Required behaviour:
- one pure classifier (for example `live_delta(snapshot_tokens, live_tokens, names, stated)`)
  returning an ordered list of `(token, class)` over the union of the snapshot token line and the
  live run's token line, with class words exactly `absent-live`, `added-live`, `agreed`, and
  `class-changed:<snapshot>-><live>` where the live class is `derive(token, names)` from the live
  baseline names and the snapshot class is the `stated` one;
- `grade()` prints exactly one `LIVE_DELTA <token> <class>` line for every non-agreed token and
  none for agreed tokens, and extends the tail with `delta=classified classified=<n> union=<n>
  absent_live=<n> added_live=<n> class_changed=<n> deltas=<n>` while keeping `tokens=`, `residual=`,
  `live=`, `live_tokens=` and `live_agree=`;
- `met` never requires a particular live token count: it requires every union token classified
  exactly once and `agreed == live_agree`, keeping every existing conjunct;
- four selftest arms with the frozen labels `delta_absent_live`, `delta_added_live`,
  `delta_class_changed`, `delta_agreed`, each over a synthetic snapshot/live pair (no census run);
  at least 16 arms total.
- Preserve each of these substrings exactly once (they are P-C1's equivalence proofs):
  `and not unclassified and residual == 0`, `agreed == len(snapshot_tokens)`,
  `residual += duplicates`, `duplicates == 0`. Do not add an arm where `residual` or
  `unclassified` is non-zero while every other `met` conjunct holds.

Verify (put every command and output in your report):
- `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c2.py
  --selftest` → `C2_COUNTER_SELFTEST pass=N fail=0` with N >= 16, the four delta arms PASS.
- Shown able to fail, in scratch: `git clone --shared /home/vgpnk/Projects/shokunin/mori-shokunin
  $S/lane`, copy your edited counter into the clone, commit it there, then
  `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c3.py <probe-rev>
  --repo $S/lane` → expect a `C3=met delta=classified tokens=64 classified=U union=U residual=0
  live=derived ...` line, rc 0. The live census runs inside; report its token count, the delta
  lines and how long it took.
Report: `.ufo/waves/round-84/w1/Mo84E03C3Delta.md`.
""",
    },
    {
        "name": "Mo84E04Controls",
        "role": "executor",
        "milestone": "round 84 w1: independent control and no-harm receipt",
        "prompt": """
Independently re-run the round's frozen controls and the no-harm battery, and write one receipt.

Read `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/contract.md` first. Then run,
capturing stdout/stderr and rc for each, from `/home/vgpnk/Projects/shokunin/mori-shokunin`:
1. the three round-84 counters at the freeze commit
   `daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4`: `python3 -I .ufo/waves/round-84/count-cN.py
   daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4` — expected: `C1=unmet mutants=4 killed=0
   equivalent=2 survivors=2 ...` rc 1; `C2=unmet arm=absent` rc 1; `C3=unmet delta=absent` rc 1;
2. the three round-83 counters at the same freeze commit (no-harm battery):
   `python3 -I .ufo/waves/round-83/count-cN.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4` — record
   each r83 met/unmet line and rc exactly as printed; the r83 C1 run takes a few minutes (23
   mutants), allow it;
3. the three round-84 counters at the entering revision
   `5adf4337b6510dd246b247092c11cbaa97c930d3` — expected `unmet ... absent` lines, rc 1.
Write `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/evidence/controls-verify-r84.txt`
with, per command: the exact command line, its output verbatim and its rc. Name every deviation
from the expected text. Do not edit a counter, tool or record; do not commit.
Report: `.ufo/waves/round-84/w1/Mo84E04Controls.md`.
""",
    },
    {
        "name": "Mo84Sc01Source",
        "role": "scout",
        "milestone": "round 84 w1: open and pin the equivalence source",
        "prompt": """
Open and pin ONE source for C1's equivalence adjudication: an unkillable mutant is a known cost and
bias in mutation testing, not evidence of a missing test.

Candidate (fetch it yourself; never from memory):
`https://arxiv.org/abs/2408.01760` — "Large Language Models for Equivalent Mutant Detection".
Pin the exact bytes under
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/arXiv-2408.01760-abs.html`
(write it with curl). Record:
- final URL and HTTP status, `last-modified`/`ETag` headers if present;
- sha256, byte count and line count of the pinned bytes;
- a second fetch and a byte-identical comparison (`sha256sum` twice, or `cmp`);
- a located, verbatim quote of at most 25 words that grounds the rule, with the line number in the
  pinned file and the exact `grep -n` command that finds it;
- what the page does NOT say (limits: it is an empirical study of Java method-level mutants; it
  says nothing about this lane, its counters, exit statuses or any adjudication procedure).

Also screen ONE second candidate and refuse it with a reason and a flip condition:
`https://arxiv.org/abs/2404.09241` — "An Empirical Evaluation of Manually Created Equivalent
Mutants" (fetch it; if it grounds the rule better than the first, say so and recommend it instead).
Never invent a quote, a hash or a line number.

The registry's next unused id is S599; do not edit `corpus/SOURCES.md` — the L1 appends the row
after the Gate. Report: `.ufo/waves/round-84/w1/Mo84Sc01Source.md`, naming every command and its
output.
""",
    },
    {
        "name": "Mo84Sc02Clauses",
        "role": "scout",
        "milestone": "round 84 w1: unarmed-clause sweep of the r83 counters",
        "prompt": """
Per-surface reconnaissance for the r83 counters' unarmed clauses (sizes the next round's mutation
work; read-only).

For each of `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c1.py` and
`count-c2.py`:
1. list every boolean clause of the `met` expression in `grade()` with its line number;
2. list every branch in `green()`, `killed()`, `grade()` (unanchored / empty-mutation /
   coupling-absent / pristine-red / equivalent) and in `selfcheck()`;
3. mark each clause `armed-by <arm label>` when an existing selftest arm would fail if that clause
   were inverted or deleted, else `UNARMED`;
4. for each `UNARMED` clause name the one arm that would observe it (fixture shape, assertion).
Also list the four round-84 mutant labels (`M24a_killed_tally`, `M24b_green_fail_token`,
`M24c_met_unclassified`, `M24d_met_residual`) and say whether each is observed by an arm before
this round's edits land. Read the code; do not edit any file. A negative claim carries its sweep:
paste the `grep -n` commands that produced your clause list.
Report: `.ufo/waves/round-84/w1/Mo84Sc02Clauses.md`.
""",
    },
    {
        "name": "Mo84K01Conn",
        "role": "connector",
        "milestone": "round 84 w1: sibling-overlap scan of the three grounds",
        "prompt": """
Sibling-overlap scan for the three grounds this round touches (read-only; write only your report).

Search the sibling lanes' corpora and province files (read-only) —
`/home/vgpnk/Projects/shokunin/{kumitate,kengaku,chousa,tsukuroi,kotoba,tameshi}-shokunin/corpus/`
and their `PROVINCE.md` — for:
(a) equivalent-mutant adjudication or mutation-adequacy rules;
(b) record-anchor ambiguity / first-match selection in a gate or probe;
(c) live-versus-snapshot delta classification.
For each ground report `overlap` (same ground, cite the sibling row), `distinct` (adjacent but not
contested, cite what makes it distinct) or `contested` (report the boundary, never absorb it).
Also check whether any sibling already owns a rule that would make this round's all-anchor-rows
rule a duplicate, and whether the mutation-adequacy ground is already covered outside mori.
Cite `path:line` for every claim; a negative claim carries its `grep`/`rg` sweep.
Never write outside your own report file.
Report: `.ufo/waves/round-84/w1/Mo84K01Conn.md`.
""",
    },
    {
        "name": "Mo84S01Lesson",
        "role": "scribe",
        "milestone": "round 84 w1: round lesson, mistake and coverage row",
        "prompt": """
Draft the round-84 lesson and the coverage-map row. Prose only; the L1 owns the Gate block, the
SCORECARD and LOG records and every commit.

1. `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-84.md` in the shape of
   `corpus/lessons/round-83.md`: a header block (round 84, date 2026-11-04, entering revision
   `5adf4337b6510dd246b247092c11cbaa97c930d3`, freeze `daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4`),
   the three claims with their keeper commands and targets (targets, not observed values), and:
   - `## Mistakes` — ONE mistake with class · evidence pointer · captured-by · fix. Use this one:
     the round-83 round reported its counters met while its own mutation-probe seat died without a
     tally, so the r83 counters were never probed for their own survivors (evidence:
     `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/w1/` holds no
     `Mo83M01Mut.md`, and the r83 report names six dead seats; the r84 C1 population exists only
     because the C1 reviewer ran its own 24th-mutant sweep). captured-by: `none` — no QUALITY
     criterion required a counter's own mutation tally before a round reports met. Fix: this
     round's C1 counter plus the M24a/M24b arms, shown able to fail by the population control
     (`C1=unmet mutants=4 killed=0 equivalent=2 survivors=2` at the freeze commit, `survivors=0`
     after the arms).
   - `## Census` — run the census now and paste it verbatim with its exit code:
     `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
     (expected rc 0, `mori ok`, 371 rows, 35 W04 warnings). Leave a clearly marked AFTER slot for
     the L1.
   Do NOT write a `## Gate` section (the L1 owns it) and do not invent a source, hash or quote.
2. Append one section to `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/README.md` under a new
   `## Round-84 knowledge addition — equivalent-mutant adjudication` heading, in the shape of the
   r83 row, naming the knowledge entry the L1 will add
   (`corpus/knowledge/equivalent-mutant-adjudication-r84.md`) and source id `S599`. Say it is new
   growth indexed the round it lands.

Files you may edit: `corpus/lessons/round-84.md` (new) and `corpus/README.md` (one appended
section). Report: `.ufo/waves/round-84/w1/Mo84S01Lesson.md`.
""",
    },
    {
        "name": "Mo84S02Quality",
        "role": "scribe",
        "milestone": "round 84 w1: three QUALITY criteria from this round",
        "prompt": """
Append three criteria to `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/QUALITY.md`
(numbers 170, 171, 172; the file's last row is 169), in that file's existing row shape (statement,
ground with `path:line`, shown-able-to-fail, not-covered):

170 — a revision-arm anchor that selects more than one row is graded as a whole, never by first
match: every selected row must carry the token on the carrier side and in the bound revision's
blob. Ground: QUALITY 169's not-covered clause (`corpus/QUALITY.md` row 169), this round's P-C2
(`.ufo/waves/round-84/contract.md`) and the `ALL_ANCHOR_ROWS` rule in `tools/mori-record-sweep.py`;
the defeated fixtures `carrier-ambiguous`/`rev-ambiguous`. Shown able to fail: the entering tool at
`5adf4337` reads both ambiguous fixtures green and the landed tool reads them red (the r84 C2
counter's `defeated=2`). Not covered: an anchor that selects two rows with the same value is not
distinguished from one intended row; values split across lines; non-numeric tokens.

171 — a live-versus-snapshot comparison names every token's delta class instead of printing two
counts. Ground: this round's P-C3 and the `LIVE_DELTA` classifier in
`.ufo/waves/round-83/count-c2.py`; the r83 reading `live_tokens=63 live_agree=63` named no token
(`SCORECARD.md` Round 83 section). Shown able to fail: the four delta selftest arms over synthetic
snapshot/live pairs. Not covered: the live class is derived from the live baseline's names, not
authenticated; a failed live run is `unavailable`, never a delta; a class-changed token whose
snapshot class is `unexplainable` is outside the frozen table.

172 — a counter that grades a tool's helpers but not its own detector is not yet adequate: every
counter carries a detector selftest and a population control that reads red before the arms land.
Ground: the r82/r83 lesson class (a counter that grades helpers but not itself), the r83
mutation-probe seat's missing tally, this round's P-C1 (M24a/M24b arms, M24c/M24d equivalence with
byte coupling proofs). Shown able to fail: the r84 C1 population control prints `survivors=2` at
the freeze commit and `survivors=0` after the arms. Not covered: a counter whose own logic changes
after its arms land is not re-probed by this rule; an equivalence exemption is only as strong as
its coupling marker.

Rows are append-only: do not rewrite 169 or any earlier row. No external source is needed; cite
the lane's own committed paths. File: `corpus/QUALITY.md` only.
Report: `.ufo/waves/round-84/w1/Mo84S02Quality.md`.
""",
    },
    {
        "name": "Mo84R01C1",
        "role": "reviewer",
        "milestone": "round 84 w1: attack C1's population, counter and arms",
        "prompt": """
Attack C1 before it is measured. Read P-C1 in `.ufo/waves/round-84/contract.md`, the frozen
counter `.ufo/waves/round-84/count-c1.py`, the r83 reviewer's extra-mutant sweep
`.ufo/waves/round-83/w1/Mo83R01C1.md` §6, and the r83 counters as they stand. Do not edit lane
files.

1. Re-derive the four-mutant population yourself: for each `old` anchor count occurrences in the
   named file's current bytes (python `str.count` or `grep -cF`), report per-file counts and the
   exact old→new strings. Flag any anchor that no longer occurs exactly once.
2. Attack the counter: (a) can a stub `.ufo/waves/round-84/count-c1.py` satisfy `harness=present`?
   (b) can an empty mutation, an unanchored anchor, a red pristine or a red detector reach `met`?
   (c) can the equivalence map exempt a mutant whose coupling marker is absent or duplicated? (d)
   is a surviving mutant ever counted killed, and is a killed mutant ever counted equivalent?
   Run `python3 -I .ufo/waves/round-84/count-c1.py --selftest` and paste the output.
3. Judge each new arm as seat Mo84E01C1Arms adds it (read the file as it appears; if it is not yet
   edited, state exactly what you will accept and reject): does the arm exercise the mutated
   behaviour, or is it a fake kill (tautology, hardcoded token, an assertion on the mutant's label,
   an arm that passes even if the mutated function is never called)? Name any fake kill with
   `file:line`.
4. Construct ONE additional mutant of `.ufo/waves/round-83/count-c1.py` or `count-c2.py` that still
   survives the post-arm selftests (scratch copies only) and give its old→new anchors; if you find
   none, paste the sweep that found none.

Report: `.ufo/waves/round-84/w1/Mo84R01C1.md` with a verdict per claim element and every command's
output. An unrun check has not passed.
""",
    },
    {
        "name": "Mo84R02C23",
        "role": "reviewer",
        "milestone": "round 84 w1: attack C2's rule and C3's classifier",
        "prompt": """
Attack C2 and C3 before they are measured. Read P-C2/P-C3 in `.ufo/waves/round-84/contract.md` and
both counters. Do not edit lane files; scratch copies are fine.

C2 (all-anchor-rows):
1. Build the three frozen fixtures yourself in scratch (own git repos, `-C "$D"` everywhere) and
   run both the entering tool (`git show 5adf4337:tools/mori-record-sweep.py`) and the current
   worktree tool on each. Confirm the two ambiguous fixtures read green under the entering tool and
   red under the current one, and that `conformant` stays green under both.
2. Try to satisfy the all-rows rule with a junk carrier (two rows both stating the value, neither
   the intended record) and say whether that is a real gap or the binding's own semantics.
3. Check the four new selftest arms are not tautologies (do they fail if the rule is removed?).
4. Run the tool's `--selftest` and paste the tally.

C3 (live delta):
1. Can the delta classifier be a constant (the same class for every token) and still pass the four
   frozen arms? Build that constant in scratch and say which arm catches it, if any.
2. Does `met` stay independent of the live token count? Name the clause that would make it
   volatile.
3. Is `classified == union` a real invariant, or can a token be classified twice or missed? Read
   the classifier's loop and construct the shape that would break it.
4. Check the four preserved substrings still occur exactly once in the worktree file.

Report: `.ufo/waves/round-84/w1/Mo84R02C23.md` with a verdict per item and every command's output.
""",
    },
    {
        "name": "Mo84C01Crit",
        "role": "critic",
        "milestone": "round 84 w1: falsify the three claims as claims",
        "prompt": """
Falsify the three claims as claims, not as code. Read `.ufo/waves/round-84/contract.md`,
the three counters and `SCORECARD.md` `## Planned (round 84)`.

1. Do-nothing control: for each claim name the cheapest control that skips the claimed work (a stub
   counter file; a tool that prints the target tail without the rule; a constant delta classifier)
   and score it with the frozen counter. If any control reaches the target, the counter or target is
   wrong — say so before data.
2. Separability: is each claim verifiable without the others having landed? Name a revision where
   each counter reads its entering value while the others are landed.
3. Axis attribution: does each claim move the axis it names (operability / calibration / depth) by
   the surface it changes, not by the number it prints?
4. Admission: is any target reachable by the entering bytes (not a real move)? Is any target
   narrowed relative to SCORECARD's `## Planned (round 84)`? Is any claim's before→after a trade
   that harms another axis (name the axis and the evidence)?
5. Wording: does each contract predicate sentence match what the counter actually enforces?

Report a verdict per claim — `admit` or `attack with reason` — and list every defect you find with
`file:line`. Read-only. Report: `.ufo/waves/round-84/w1/Mo84C01Crit.md`.
""",
    },
    {
        "name": "Mo84M01Mut",
        "role": "mutation-tester",
        "milestone": "round 84 w1: independent mutation probe of the r84 counters",
        "prompt": """
Independent mutation probe of the round-84 counters' own logic. The lane's standing rule: a counter
that grades helpers but not itself is not adequate.

1. Enumerate candidate mutants of `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c1.py`,
   `count-c2.py` and `count-c3.py`: invert or delete each guard in `met`, `killed`, `green`, the
   equivalence coupling check, the population check, the arms floor and each summary field. For each
   give `file:label:old->new` and verify the `old` anchor occurs exactly once at the current bytes.
2. Copy each counter to scratch, apply one mutant per copy, and run that copy's own `--selftest`
   (and the `--selftest` of any counter it grades, where the mutant lives in a shared helper).
   Tally `MUTANTS total=N killed=K survivors=S` and name, per survivor, the arm it needs.
3. Classify each survivor as non-equivalent (with the observation that shows it) or equivalent
   (with the coupling proof); do not fix anything.
4. Report the tally and the survivor list as routed findings for the lane's next round.

Scratch only; never edit a lane file and never commit. Report:
`.ufo/waves/round-84/w1/Mo84M01Mut.md`.
""",
    },
    {
        "name": "Mo84R03Record",
        "role": "reviewer",
        "milestone": "round 84 w1: record discipline and revision-precision attack",
        "prompt": """
Attack the round's record discipline before it is written. Read `.ufo/waves/round-84/contract.md`,
the three counters, `SCORECARD.md` `## Planned (round 84)`, and QUALITY 168/169.

1. Same-sentence check: for each claim, is the contract's predicate sentence the same sentence the
   counter's code enforces and the same label the receipt prints? Name any clause the prose states
   but the code does not enforce, or a code requirement the prose omits.
2. Entering-control check: does each control really skip the claimed work, and is each red for the
   named reason (`harness=absent` / `arm=absent` / `delta=absent`)? Could a stub satisfy any of
   them?
3. Revision discipline: at which revision must each after-value be measured, and does the counter
   enforce it (the worktree-versus-revision drift check)? Name any path where a worktree run could
   be cited as a revision run.
4. Record obligations: list every record file this round must update for its claims (SCORECARD
   round section and capability rows, LOG round entry, lesson `## Gate`, QUALITY criteria, SKILL
   gate-registry row, PROVINCE if a surface moved, SHONEN evidence lines) and the exact claim each
   must carry. Flag any obligation the contract omits.
5. Numbers discipline: for every number this round will cite, name the command that re-derives it.

Read-only. Report: `.ufo/waves/round-84/w1/Mo84R03Record.md`.
""",
    },
]

SPEC = {
    "wave": "mori-r84-w1",
    "milestone": ("Round 84 w1: the four extra r83 mutants, the all-anchor-rows rule and the "
                  "live-delta classification, with first falsifiers; counters frozen in "
                  + FREEZE[:12] + "."),
    "axes": ["coverage", "operability", "depth", "freshness", "calibration", "adjacency"],
    "reportDir": ".ufo/waves/round-84/w1",
    "maxLanes": len(ITEMS),
    "context": CONTEXT,
    "items": [],
}

ROLE_AXES = {
    "executor": ["operability", "depth"],
    "scout": ["coverage", "freshness"],
    "scribe": ["coverage", "calibration"],
    "reviewer": ["calibration", "operability"],
    "critic": ["calibration", "depth"],
    "mutation-tester": ["operability", "depth"],
    "connector": ["adjacency", "coverage"],
}

for item in ITEMS:
    SPEC["items"].append({
        "name": item["name"],
        "role": item["role"],
        "axes": ROLE_AXES[item["role"]],
        "milestone": item["milestone"],
        "prompt": item["prompt"],
    })

with open(ROUND + "/w1-spec.json", "w", encoding="utf-8") as handle:
    json.dump(SPEC, handle, indent=1)
    handle.write("\n")
print("wrote", ROUND + "/w1-spec.json", "items", len(SPEC["items"]))
