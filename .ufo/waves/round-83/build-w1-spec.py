#!/usr/bin/env python3
"""Build mori round-83 wave w1 spec (one v1 wave, 14 seats, band 8-16).

Writes .ufo/waves/round-83/w1-spec.json. The Godspeed directive bytes are copied verbatim from
the round-82 spec (the host binding), never retyped. Every item prompt is self-contained; shared
rules ride the wave context.
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
ROUND = LANE + "/.ufo/waves/round-83"
R82 = LANE + "/.ufo/waves/round-82/w1-spec.json"

with open(R82, encoding="utf-8") as handle:
    r82 = json.load(handle)
GODSPEED = r82["context"].split("\n\n# Goal", 1)[0]
assert GODSPEED.startswith("/skill:godspeed"), GODSPEED[:40]

CONTEXT = GODSPEED + """

# Goal
mori round 83 (attempt 1), wave w1 — repair, record and first falsifiers for THREE frozen claims.
mori is a fleet/host observability lane: detection and report only. The freeze commit is
`9075c72995095de97babb3d06e3f2d3b2f168062`; the counters were frozen there before any seat ran.

Read first, in this order (absolute paths):
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/contract.md — THE FROZEN
  AUTHORITY: P-C1, P-C2, P-C3, the 23-mutant table with its exact anchors, the snapshot header
  grammar, the anchored-occurrence interface and the do-nothing controls.
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/evidence/controls-r83.txt —
  the measured entering controls (C1 survivors=20 at the freeze; C2 snapshot=absent; C3
  arm=absent).
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/w1/Mo82M01Mutants.md — the
  mutation probe that names, per survivor, the arm it needs ("Coverage findings").
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c1.py, count-c2.py,
  count-c3.py — the three frozen counters that grade this round.
- /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-82-verifier-spotcheck.md
  (`## Routed defects the lane must fix next round`: D82-1, D82-2, carry items).

# Round claims (frozen before this wave; do not change them)
- C1 operability (7): the r82 probe's 20 surviving counter mutants get the failing arm it names,
  so the frozen 23-mutant population reads `C1=met mutants=23 killed=23 survivors=0 total=23
  pristine=green`. Entering: `survivors=20`.
- C2 calibration (5, tied lowest): the drift classification is bound to the committed raw snapshot
  `.ufo/waves/round-82/evidence/drift-r82-live.txt` — hash, as-of and derived classes graded from
  snapshot bytes, plus one live re-derivation — reading `C2=met snapshot=bound asof=1 tokens=64
  agreed=64 residual=0 live=derived`. Entering: `snapshot=absent`.
- C3 depth (5, tied lowest): the record sweep's revision arm scopes its byte occurrence test to a
  line carrying the binding's row anchor, with an `elsewhere` defeated fixture, reading `C3=met
  arm=anchored defeated=2 fixtures=2/2 bindings=3 revisions=0 arms=40`. Entering: `arm=absent`.

# Shared rules (binding on every seat)
- Write scope: /home/vgpnk/Projects/shokunin/mori-shokunin only, and inside it only the paths
  your item names. Absolute paths in every tool call: your tools start at the FLEET root, so a
  relative path lands in the wrong repo. Never write to /home/vgpnk/Projects/shokunin (fleet
  root), another lane's repo, MANIFEST.json, `.ufo/state/`, `.ufo/watchdog.log`, or `.scratch/`.
- Never commit, push, or run a mutating git/jj command anywhere: no `git add`, `git commit`,
  `git checkout`, `git reset`, `git stash`, `git push`, and no mutating `jj` command. Read-only
  git (`log`, `show`, `diff`, `status`, `ls-tree`, `cat-file`, `rev-parse`, `archive`) is fine.
  The L1 owns every commit. Never rewrite another seat's file outside your item's scope.
- Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/mori-shokunin —
  write it at /home/vgpnk/Projects/shokunin/mori-shokunin/<that path>.
- Scratch: create your work dir under /fast/scratch/hyaku/mori-r83/<your seat name>/ and delete
  it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell). Never write under /tmp; a /tmp path
  is never citable evidence. `git clone --shared` / `git worktree add` instead of full clones;
  never mirror the whole lane. `HYAKU_SCRATCH` defaults to /fast/scratch/hyaku.
- Fixture git repos: `D=$(mktemp -d)` then `git -C "$D" init -q`; assert
  `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit; every later
  git/jj call names `-C "$D"`. Never commit with a throwaway identity anywhere but a fixture.
- Detection and report only: no lane, OS, unit, service, credential, harness or orchestration
  state may be changed. mori never remediates.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the
  task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate) and
  record tool/version/channel/reason in your report. pacman is PAUSED host-wide: never run a
  pacman transaction of any kind (`-S`, `-Sy`, `-Syu`, `-U`, `-R`); use `uv tool`, `npx`, or an
  official binary in ~/.local/bin, or file an L0 question instead.
- Never message `agent://all`. Message only your own L1 (`agent://MoriR83`) for a blocker.
- Do not spawn subagents except an executor's single read-only `labrat` probe.
- Your final report must name: what you changed/produced with absolute paths, the exact commands
  you ran with their output, what you verified, what you could not verify, and any defect you
  found in another seat's bytes (file:line). Be adversarial about your own work: an unrun check
  has not passed.
"""

ITEMS = [
    {
        "name": "Mo83E01C1C1",
        "role": "executor",
        "milestone": "round 83 w1: C1 arms for the six count-c1.py survivors",
        "prompt": """
Give `.ufo/waves/round-82/count-c1.py` the failing selftest arm for each of its SIX survivors.
Frozen authority: `.ufo/waves/round-83/contract.md` P-C1 (the table) and
`.ufo/waves/round-82/w1/Mo82M01Mutants.md` "Coverage findings" items 1-7.

File you may edit: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/count-c1.py`
(`selfcheck()` only, plus at most one small pure helper as noted). The six mutants:
1. `green_ignores_fail_token` — arm `pristine_fail_token_with_rc0`: `green(0, "FAKE pass=1 fail=2")`
   is False (a red token with rc 0 must not read green).
2. `killed_ignores_rc` — arm `rc_only_kill`: `killed(1, "traceback only")` is True and
   `killed(0, "FAKE pass=1 fail=0")` is False.
3. `ignore_pristine_red` — arm `red_pristine_with_real_mutant`: a red pristine plus one graded
   mutant must be unmet (the existing red arm has total=0 and cannot see the gate).
4. `accept_empty_population` — make `duplicate_anchor_excluded` assert `not met` as well as
   `total=0` (all-unanchored must be unmet).
5. `unanchored_excused` — arm `unanchored_blocks_met`: one anchor occurring twice plus one real
   killed mutant still reads unmet, with `unanchored` in the extras.
6. `detector_gate_dropped` — arm `red_detector_never_passes`: copy this counter to scratch,
   rewrite ONLY its summary print so it prints `fail=1` while exiting 0, run the copy in
   `<rev>` mode against the real repo (`python3 -I <copy> <rev> --repo <lane>`), and assert the
   copy exits 1 and prints `detector=red`. This arm can only distinguish the gate once the three
   counters are green; say so in your report if it reads red transiently.

Rules: every frozen anchor in the contract table must still occur EXACTLY once (run the round-83
counter to check: `python3 -I .ufo/waves/round-83/count-c1.py 9075c729` while you work — it will
say `unanchored` if you break one). Add real assertions, never tautologies or hardcoded tokens
that do not exercise the function. Keep the r82 summary grammar and the four existing arms.

Evidence: paste `python3 -I .ufo/waves/round-82/count-c1.py --selftest` (must be green, with the
new arms listed), and the round-83 counter's per-mutant lines for your six labels at the current
worktree (`python3 -I .ufo/waves/round-83/count-c1.py <worktree-tip>` — the counter exports the
revision, so use the branch tip you are editing under; if grading needs a commit and none exists
yet, say so and give the `--selftest` tally plus a direct mutated-copy check per mutant).
Report: `.ufo/waves/round-83/w1/Mo83E01C1C1.md`.
""",
    },
    {
        "name": "Mo83E02C1C2",
        "role": "executor",
        "milestone": "round 83 w1: C1 arms for the seven count-c2.py survivors",
        "prompt": """
Give `.ufo/waves/round-82/count-c2.py` the failing selftest arm for each of its SEVEN survivors.
Frozen authority: `.ufo/waves/round-83/contract.md` P-C1 and
`.ufo/waves/round-82/w1/Mo82M01Mutants.md` "Coverage findings" items 8-14.

File you may edit: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/count-c2.py`
(`selfcheck()` only). The seven mutants and the arm each needs:
1. `duplicates_accepted` — a fixture writing a duplicated `DRIFT_CLASS` line must be unmet and
   count the duplicate as residual.
2. `retired_paths_unchecked` — a `## Retired` row that names the baseline but not the
   classification path must read `retired=0`.
3. `red_literal_unchecked` — a freshness cell carrying BOTH `r10 pin retired` and
   `round-10 drift pin still red` must read `cell=0`.
4. `green_census_tokens_accepted` — a census stub that exits 0 while printing a `MORI_DRIFT:`
   token list must be unmet (`metric=census-rc:0`).
5. `finding_branch_inverted` — add a `+FINDING:OOM_KILL_JOURNAL` token to the stub (the baseline
   already holds `FINDING OOM_KILL_JOURNAL`) and assert it derives `value-changed`; a
   `+FINDING:NOT_IN_BASELINE` derives `added-since-r10`.
6. `malformed_not_residual` — one malformed `DRIFT_CLASS` line must appear as residual in the
   tail (`residual=1`) even though `malformed` is separate from `residual` internally.
7. `keyshape_guard_inverted` — a token like `lane.mori` (no `=`/prefix, fails KEYSHAPE) must
   derive `value-changed` per the frozen "anything else" row.

Rules: every anchor in the contract table must still occur exactly once. Real assertions only.
Keep the nine existing arms and the summary grammar.

Evidence: `python3 -I .ufo/waves/round-82/count-c2.py --selftest` green with the new arms listed,
plus per-mutant verdicts for your seven labels from
`python3 -I .ufo/waves/round-83/count-c1.py <worktree-tip>` (or the direct mutated-copy check and
the reason it must fail). Report: `.ufo/waves/round-83/w1/Mo83E02C1C2.md`.
""",
    },
    {
        "name": "Mo83E03C1C3",
        "role": "executor",
        "milestone": "round 83 w1: C1 arms for the seven count-c3.py survivors",
        "prompt": """
Give `.ufo/waves/round-82/count-c3.py` the failing selftest arm for each of its SEVEN survivors.
Frozen authority: `.ufo/waves/round-83/contract.md` P-C1 and
`.ufo/waves/round-82/w1/Mo82M01Mutants.md` "Coverage findings" items 15-21.

File you may edit: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/count-c3.py`.
The seven mutants and the arm each needs:
1. `population_gate_dropped` — main-path arm: build a fixture git repo holding a copy of the real
   tool at a rev plus a `record-pins.json` with ONE binding, run this counter's `main` against it
   (in-process or subprocess with `--repo <fixture>` and the fixture rev) and assert it exits 1
   printing `bindings=frozen-population-mismatch`.
2. `defeated_accepted` — `fixture_run` with a stub tool that exits 1 and prints NO
   `REVISION_MISMATCH` must read not-caught (`ok` False).
3. `carrier_drift_allowed` — main-path arm: a fixture repo whose pinned carrier worktree bytes
   differ from the pinned revision must exit 2 with `worktree differs`. The fixture may pin the
   frozen three bindings as strings even though those revs do not resolve there, because the
   drift check runs before the tool.
4. `bindings_floor_dropped` — lift main's `met` conjunction into one pure helper that main calls,
   keeping both frozen anchors (`fields.get("revisions", -1) == 0` and `and bindings >= 3`)
   literally present, exactly once; an arm must show a conformant run with `bindings=1` is unmet
   while `bindings=3` is met.
5. `selftest_red_accepted` — main-path arm: a tool copy that prints
   `RECORD_SWEEP_SELFTEST pass=40 fail=0` then exits 1 must be refused (`selftest=red`).
6. `revisions_default_zero` — same lifted helper: a summary with no `revisions=` token must read
   unmet (default -1, never 0).
7. `summary_first_line` — `summary()` over two `RECORD_SWEEP` lines must take the LAST one.

Rules: every frozen anchor must still occur exactly once; main's behaviour must be unchanged for
the real lane (the r82 semantics stay byte-compatible); real assertions only, never a tautology.
Any helper you add is pure and lives beside the code it serves; do not weaken the worktree/revision
identity setup or the fixture repo guards (`git rev-parse --show-toplevel` == fixture dir).

Evidence: `python3 -I .ufo/waves/round-82/count-c3.py --selftest` green with the new arms listed,
plus the per-mutant verdicts for your seven labels, plus two lines showing the real lane run still
prints `C3=...` at the tip. Report: `.ufo/waves/round-83/w1/Mo83E03C1C3.md`.
""",
    },
    {
        "name": "Mo83E04Snap",
        "role": "executor",
        "milestone": "round 83 w1: C2 snapshot provenance binding",
        "prompt": """
Bind the round-82 drift classification to its committed raw snapshot.

Frozen authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/contract.md`
P-C2, and the counter `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c2.py`.

Files you may edit:
1. `corpus/evidence/drift-classification-r82.txt` — add exactly these header lines in the existing
   header block (one each, before the first `DRIFT_CLASS` line):
   `# Snapshot: .ufo/waves/round-82/evidence/drift-r82-live.txt`
   `# Snapshot-sha256: <sha256 of that file's bytes>`
   `# As-of: <the snapshot's first "# run-start:" value normalized to UTC whole seconds,
   e.g. 2026-11-04T07:45:13Z>`
   Do not touch any `DRIFT_CLASS` line, the token population or the existing header lines.
2. `SCORECARD.md` — the `## Retired` row `drift-pin-r10` must also name the snapshot path (keep
   the baseline and classification paths and every other word); the `freshness` Axes cell must
   keep `r10 pin retired` and the classification path and must not gain the red literal.

Compute the hash and the as-of yourself and show the commands. Then run
`python3 -I .ufo/waves/round-83/count-c2.py <worktree-tip-or-freeze-rev>` and paste the output:
it must read `snapshot=bound asof=1 tokens=64 agreed=64 residual=0 live=derived` with
`live_tokens=64` (or report the measured live numbers honestly if they differ; a live census is
an observation, not a constant). While you edit, the entering revision still reads
`snapshot=absent` — that is the control, do not pursue it.

Rules: no other file; never touch the classification's classes; never edit the snapshot file.
Report: `.ufo/waves/round-83/w1/Mo83E04Snap.md`.
""",
    },
    {
        "name": "Mo83E05Anchor",
        "role": "executor",
        "milestone": "round 83 w1: C3 anchored occurrence in the revision arm",
        "prompt": """
Scope the record sweep's revision-arm byte occurrence test to the binding's row anchor.

Frozen authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/contract.md`
P-C3 and the counter `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c3.py`.

File you may edit: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py`.

Required behaviour: the `rev-bytes` check requires, on ONE line of `git show <rev>:<path>`, both
the `key=value` token (same boundary rule) AND the binding's `row_contains` string. A value that
only occurs on an unrelated line is `REVISION_MISMATCH <carrier>:<line> rev-bytes`. The carrier-side
`row-value`, `rev-unresolvable` and `path-absent` details stay as they are; the r81 command arm and
the summary grammar stay byte-compatible. Add the literal docstring/marker `ANCHORED_OCCURRENCE`
so the counter can tell the arm exists.

Arms: add at least four selftest arms (the round-83 counter floors `pass` at 40; you start at 36):
1. value on the anchored line → no finding;
2. value only on an unrelated line (the `elsewhere` shape) → `rev-bytes`;
3. anchor absent from the whole file → `rev-bytes` (never a silent pass);
4. the token-boundary rule still rejects `row_tally=190` when the binding is 19.
State each arm's expected arm/line in your report and paste
`python3 -I tools/mori-record-sweep.py --selftest` (`RECORD_SWEEP_SELFTEST pass>=40 fail=0`).

Then run the round-83 counter at the worktree tip and paste its line; it must read
`C3=met arm=anchored defeated=2 fixtures=2/2 bindings=3 revisions=0 arms=<n>`. Also show that the
pre-change tool (r82 bytes) FAILS the counter's `elsewhere` fixture and the new tool passes it —
that is the defeated shape the claim names.

Rules: do not edit the frozen pins file or the counters. Report:
`.ufo/waves/round-83/w1/Mo83E05Anchor.md`.
""",
    },
    {
        "name": "Mo83E06D82",
        "role": "executor",
        "milestone": "round 83 w1: routed-defect discharge D82-1 and D82-2 evidence",
        "prompt": """
Discharge the two routed defects the round-82 non-author closure left addressable from the lane.

Read `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-82-verifier-spotcheck.md`
`## Routed defects the lane must fix next round` — D82-1 (record attribution) and D82-2
(evidence gap).

D82-1: `SCORECARD.md:4038` ("Self-assessment claim sweep" capability row) states
`pointers=249` and its inserted correction, and the same sentence still ends by attributing the
249 run to `075574c8`, the revision where the graded count is 237. MEASURE first: find the
revisions where `python3 -I tools/mori-claim-sweep.py --root . --pins
.ufo/waves/round-80/claim-pins.json` prints `pointers=249` (check the r82 tip `f573c946` and the
current tip with read-only `git show` on `SCORECARD.md` if you cannot run a historical tree).
Then append a NAMED correction paragraph (never rewrite the frozen r80 text) that (a) names the
actual revision whose run produced 249, (b) separates the historical `075574c8`/237 attribution
from it, and (c) states that the r80 sentence's revision label was the defect, not its value.
Give the command output you used as evidence in the report.

D82-2: write `.ufo/waves/round-83/evidence/c3-selftest-r83.txt` holding the exact output of
`python3 -I .ufo/waves/round-82/count-c3.py --selftest` and of
`python3 -I .ufo/waves/round-83/count-c3.py --selftest` with a one-line header naming the bytes
measured (revision or "worktree, uncommitted"). This is the post-repair tally the r82 closure
said was missing. If the r82 counter's selftest is red because a sibling seat is mid-edit, say so
and re-run once before writing; never fabricate a tally.

Files you may edit: `SCORECARD.md` (one appended correction paragraph only) and
`.ufo/waves/round-83/evidence/c3-selftest-r83.txt`. Report:
`.ufo/waves/round-83/w1/Mo83E06D82.md`.
""",
    },
    {
        "name": "Mo83Sc01Source",
        "role": "scout",
        "milestone": "round 83 w1: source pin for mutation adequacy (S598 candidate)",
        "prompt": """
Open and pin ONE source for C1's rule: a mutant that survives reveals a behaviour the test suite
does not constrain, and the killed percentage gauges test adequacy.

Candidate (already fetched once by the L1, re-verify independently):
`https://pitest.org/` — "What is mutation testing?" / "How it works in 51 words". Pin the exact
bytes under
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r83/pitest-home.html`
(write it with curl, not from memory). Record:
- final URL and HTTP status, `last-modified`/`ETag` headers if present;
- sha256, byte count and line count of the pinned bytes;
- a second fetch and a byte-identical comparison (`sha256sum` twice, or `cmp`);
- a located, verbatim quote of at most 25 words that grounds the rule, with the line number in
  the pinned file and the exact `grep -n` command that finds it;
- what the page does NOT say (limits: it defines mutation testing for Java/PIT, it says nothing
  about this lane, about self-tests, or about any exit status).

Also screen one second candidate and refuse it with a reason + flip condition (for example the
PIT mutators page: it lists mutators, not the adequacy rule). Never invent a quote, a hash or a
line number.

The registry's next unused id is S598; do not edit `corpus/SOURCES.md` — the L1 appends the row
after the Gate. Report: `.ufo/waves/round-83/w1/Mo83Sc01Source.md`, naming every command and its
output.
""",
    },
    {
        "name": "Mo83Sc02Arms",
        "role": "scout",
        "milestone": "round 83 w1: arm map and collision scan for the 20 survivors",
        "prompt": """
Read-only reconnaissance for C1. Build the definitive arm map, from current bytes, for the 20
surviving counter mutants the r82 probe named
(`.ufo/waves/round-82/w1/Mo82M01Mutants.md` "Coverage findings" items 1-21).

For each survivor: file:line of the mutated expression, the function it lives in, whether an arm
can reach it in-memory or needs a main-path fixture, the exact assertion that would kill it, and
the existing arm (if any) that looks closest but does not reach it. Flag:
- any frozen anchor that occurs more, or fewer, than once in the CURRENT bytes;
- any proposed arm that would be a tautology or a hardcoded token (the r82 probe found one such
  tautology in count-c3.py:152-153 — check whether more exist);
- any repair that would need to move a frozen anchor (the claim forbids it).

Deliver a table plus a short "fake-arm traps" list. Read-only: no lane file is edited. Report:
`.ufo/waves/round-83/w1/Mo83Sc02Arms.md`.
""",
    },
    {
        "name": "Mo83K01Conn",
        "role": "connector",
        "milestone": "round 83 w1: sibling-overlap scan for the three instruments",
        "prompt": """
Cross-lane overlap scan (read-only) for the three round-83 instruments: (a) counter mutation
adequacy (mutation testing a test suite against anchored mutants), (b) binding a derived
classification to a committed raw snapshot with an as-of moment, (c) line-anchored occurrence
checking of a value inside a revision's bytes.

Search the sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin/` (read-only) for
each surface: where does another lane already hold it, what is its instrument and revision, and is
mori's version a duplicate, a contested scope, or a distinct new surface? Name file paths and the
matching code/doc lines. Also check this lane's own `corpus/knowledge/` and `tools/` for prior
entries that already claim the same ground (the lane has a rule against re-claiming it).

Output: one row per surface with `owner | evidence path:line | verdict (distinct / overlap-declared
/ contested) | what mori must not claim`. Never edit another lane; never claim their surface.
Report: `.ufo/waves/round-83/w1/Mo83K01Conn.md`.
""",
    },
    {
        "name": "Mo83S01Lesson",
        "role": "scribe",
        "milestone": "round 83 w1: lesson with Mistakes and Census, coverage-map row",
        "prompt": """
Draft the round-83 lesson and the coverage-map row. Write prose only; the L1 owns the Gate block,
the SCORECARD and LOG records and every commit.

1. `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-83.md` in the shape of
   `corpus/lessons/round-82.md`: a header block (round, date 2026-11-04, entering revision
   `68185d6e719054c55b107280085b05609e96165b`, freeze `9075c729`), the three claims with their
   keeper commands and targets (targets, not observed values), and:
   - `## Mistakes` — ONE mistake mined this round, with class · evidence pointer · captured-by ·
     fix. Use the D82-1 recurrence: the D80-4/D81-1 revision-attribution class survived inside the
     very correction that claimed to discharge it (`corpus/lessons/round-82-verifier-spotcheck.md`
     D82-1; SCORECARD line 4038). captured-by: QUALITY 168 should have required resolving the
     carrying reference; the fix is this round's C3 anchored-occurrence arm plus the named
     correction D82-1. State what makes the fix able to fail (the `elsewhere` fixture must be
     caught by the new tool and pass the r82 tool).
   - `## Census` — run the census BEFORE line now and paste it verbatim with its exit code:
     `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
     (expected: rc 0, `mori ok`, 370 rows after r82, 35 W04 warnings). Leave a clearly marked
     AFTER slot for the L1.
   Do NOT write a `## Gate` section (the L1 owns it) and do not invent a source, hash or quote.
2. Append one row to `corpus/README.md` under a new `## Round-83 knowledge addition — ...`
   heading, in the shape of the r82 row, naming the knowledge entry the L1 will add
   (`corpus/knowledge/counter-mutation-adequacy-r83.md`) and the source id `S598`. Say it is new
   growth indexed the round it lands.

Files you may edit: `corpus/lessons/round-83.md` (new) and `corpus/README.md` (one appended
section). Report: `.ufo/waves/round-83/w1/Mo83S01Lesson.md`.
""",
    },
    {
        "name": "Mo83R01C1",
        "role": "reviewer",
        "milestone": "round 83 w1: attack C1 — population, anchors and arm honesty",
        "prompt": """
Attack C1 before it is measured. Read P-C1 in `.ufo/waves/round-83/contract.md` and the frozen
counter `.ufo/waves/round-83/count-c1.py`. Do not edit lane files.

1. Re-derive the 23-mutant population yourself from the contract table and independent
   `grep`/Python counts over `.ufo/waves/round-82/count-c{1,2,3}.py` at the current worktree:
   every anchor exactly once, no anchor missing, none duplicated. Report the per-file counts.
2. For every arm a sibling seat adds (read the files as they appear; if they are not edited yet,
   review the frozen counter and the r82 probe's recommendation and state what you will accept),
   judge whether the arm exercises the mutated behaviour or is a fake kill: a tautology, a
   hardcoded token, an assertion on the mutant's label, an arm that passes even if the mutated
   function is never called. Name any fake kill with file:line.
3. Run `python3 -I .ufo/waves/round-83/count-c1.py --selftest` and, if the worktree is committed,
   the `<rev>` mode; paste the output. Attack the counter itself: (a) can a stub counter file
   satisfy `harness=present`? (b) can an empty mutation or an unanchored anchor reach `met`?
   (c) is a `pristine=red` run ever a pass? (d) does the detector- selftest gate actually bind?
4. Try to construct ONE additional mutant of the three counters that still survives the
   post-repair selftests (scratch only) and give its old→new anchors; if you find none, paste the
   sweep that found none.

Report: `.ufo/waves/round-83/w1/Mo83R01C1.md` with a verdict per claim element and every command's
output. An unrun check has not passed.
""",
    },
    {
        "name": "Mo83R02C23",
        "role": "reviewer",
        "milestone": "round 83 w1: attack C2 and C3 — provenance and anchored occurrence",
        "prompt": """
Attack C2 and C3 before they are measured. Read P-C2/P-C3 in
`.ufo/waves/round-83/contract.md`, `.ufo/waves/round-83/count-c2.py` and `count-c3.py`. Do not
edit lane files.

C2 (snapshot provenance):
1. Independently compute the sha256 and the first `# run-start:` of
   `.ufo/waves/round-82/evidence/drift-r82-live.txt`; compare with the header the executor writes
   into `corpus/evidence/drift-classification-r82.txt` (if not written yet, grade the frozen
   predicate and say what shape you will accept).
2. Re-derive all classes from the snapshot tokens and the baseline bytes with your own script;
   report the count of agreements and any disagreement with the token and both classes.
3. Attack the header parser: duplicate `# Snapshot:` lines, a snapshot path below another path,
   trailing spaces, an as-of with fractional seconds or a non-UTC offset, a hash of an edited
   file. Which of these must be unmet, and does the counter read them that way? Give the exact
   readings you observe (run the counter's `--selftest` and any scratch fixture you need).

C3 (anchored occurrence):
4. Verify the `elsewhere` shape really defeats the r82 tool: export the r82 tool bytes to scratch,
   build the fixture (value 19 only on an unrelated note row, anchored row states 18, carrier row
   states 19) and show r82 reads green where the new tool must read `rev-bytes`.
5. Attack the anchored test: a `row_contains` that is a substring of another row's text, two rows
   containing the anchor, a value split across lines, a token that occurs as a prefix of a larger
   number. Say what the code does and what it should do; name any surviving bypass.

Report: `.ufo/waves/round-83/w1/Mo83R02C23.md` with commands, outputs and a verdict per item.
""",
    },
    {
        "name": "Mo83C01Crit",
        "role": "critic",
        "milestone": "round 83 w1: falsify the three frozen claims before data",
        "prompt": """
Falsify the round's three claims as stated, before any after-value exists. Read
`.ufo/waves/round-83/contract.md` (P-C1, P-C2, P-C3 and the do-nothing rule) and the three frozen
counters. Do not edit lane files.

For each claim, answer with evidence:
1. **Do-nothing reachability.** Is the target reachable without doing the claimed work — by
   re-running the counter, by editing documentation, by a stub? Build the cheapest control that
   skips the work and score it with the frozen counter (scratch copies are fine; take the control
   from `evidence/controls-r83.txt` where it already exists).
2. **Predicate ambiguity.** Name every word in the frozen sentence that two honest readers could
   read differently (e.g. "every one of those mutants", "pristine green", "one line", "as-of",
   "bound") and say whether the code resolves it or whether the receipt could be true under one
   reading and false under another.
3. **Kill-rule gaps.** Can a claim read `met` while its motivating defect is still present? Give
   at least one concrete construction for C1 and one for C2/C3 if you can; if you cannot, say so
   and name why.
4. **Axis honesty.** C1 works operability 7, C2 calibration 5, C3 depth 5 — is any of the three
   really a re-score of existing ground rather than a surface move? Name the surface each changes.
5. **Harm.** Does any claim weaken a frozen r82 instrument (predicate, grammar, exit codes), a
   corpus entry, or an axis? Name it.

Report: `.ufo/waves/round-83/w1/Mo83C01Crit.md`. Verdict per claim: `holds`, `ambiguous`, or
`falsified`, with the evidence. Do not soften: a surviving objection is the deliverable.
""",
    },
    {
        "name": "Mo83M01Mut",
        "role": "mutation-tester",
        "milestone": "round 83 w1: independent mutation probe of the round-83 counters",
        "prompt": """
Mutation-test the round's own instruments: `.ufo/waves/round-83/count-c1.py`, `count-c2.py`,
`count-c3.py`. The r82 lesson was that the counters graded their helpers but not themselves; do
not repeat it.

Method (all mutant copies under `/fast/scratch/hyaku/mori-r83/Mo83M01Mut/`, deleted before you
yield; lane bytes are never edited):
1. Pristine first: run each counter's `--selftest` and record the tally; a mutant is graded only
   against a green pristine.
2. Build at least 12 anchored mutants across the three counters (≥4 each), each with an `old`
   anchor occurring exactly once and a `new` that inverts or drops a gate: met clauses, exit
   codes, the `unanchored` exclusion, the snapshot hash/as-of checks, the token population check,
   the fixture expectations, the arms floor, the worktree-identity setup, the marker check.
3. Detector: a mutant is killed iff the mutated copy's own `--selftest` exits non-zero or prints
   `fail=<n>` n>0. For main-path mutants the selftest may be blind; report those as survivors and
   say which fixture would be needed.
4. Print `MUTANTS killed=K total=T survivors=S` and a per-mutant table, then, for every survivor,
   the exact missing arm (file:line and the assertion it needs). These survivors are routed to the
   next round, not fixed by you.

Also verify the frozen counters' anchors at the current bytes (each occurs exactly once) and that
`count-c1.py` counts a stub as `harness=absent`/`markers=missing` rather than `met`.
Report: `.ufo/waves/round-83/w1/Mo83M01Mut.md` with the pristine tallies, the table and the
survivor arms. No lane edit, no commit.
""",
    },
]

SPEC = {
    "wave": "mori-r83-w1",
    "milestone": ("Round 83 w1: repair, record and first falsifiers for C1 (counter mutation "
                  "adequacy), C2 (snapshot-bound drift classification) and C3 (anchored "
                  "occurrence); counters frozen in 9075c729."),
    "axes": ["coverage", "operability", "depth", "freshness", "calibration", "adjacency"],
    "reportDir": ".ufo/waves/round-83/w1",
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
