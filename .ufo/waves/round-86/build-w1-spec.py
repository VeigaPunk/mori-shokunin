#!/usr/bin/env python3
"""Build mori round-86 wave w1 spec (one v1 wave, 12 seats, band 8-16).

Writes .ufo/waves/round-86/w1-spec.json. The Godspeed directive bytes are copied verbatim from
the round-85 spec (the host binding), never retyped.
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
R85 = LANE + "/.ufo/waves/round-85/w1-spec.json"
FREEZE = "5e80229a450fa007d73ad0fb8bc3147e4adf5438"
ENTERING = "fec2b328a4c83e0c61bc09d70e254ca47d547d34"

with open(R85, encoding="utf-8") as handle:
    r85 = json.load(handle)
GODSPEED = r85["context"].split("\n\n# Goal", 1)[0]
assert GODSPEED.startswith("/skill:godspeed"), GODSPEED[:40]

CONTEXT = GODSPEED + """

# Goal
mori round 86 (attempt 1), wave w1 — land, record and first-falsify THREE frozen claims.
mori is a fleet/host observability lane: detection and report only. The freeze commit is
`%(freeze)s`; the three r86 counters and the do-nothing controls were frozen there before any seat
ran. The entering revision is `%(entering)s`.

Read first, in this order (absolute paths):
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/contract.md — THE FROZEN
  AUTHORITY: P-C1 (six surviving r85-C3-counter mutants get their arms), P-C2 (the receipt body is
  bound to its command), P-C3 (the classification's value channel), the targets, kill rules and the
  measured do-nothing controls.
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/count-c1.py, count-c2.py,
  count-c3.py — the three frozen counters (each has `--selftest`).
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/evidence/controls-r86.txt — the
  measured entering, stub and retroactive controls.
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/w1/Mo85M01Mut.md §5 and §7 —
  the mutation-probe survivors this round arms.
- /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-85-verifier-spotcheck.md
  (`## Routed defects the lane must fix next round`: a literal `<fill>` placeholder in LOG.md, the
  contradictory controls-r85-entering.txt, the missing contract A4 block, the overstated amendment
  disclosure, the prompt-attribution recurrence).
- /home/vgpnk/Projects/shokunin/mori-shokunin/SCORECARD.md `## Planned (round 86)`.

# Round claims (frozen before this wave; do not change them)
- C1 operability (7): .ufo/waves/round-85/count-c3.py gains six arms (selftest 20 -> 26) that kill
  H-C3-metverdict, C3-01-rc-range, C3-02-rc-dropped, C3-03-order, C3-04-agreed-skip and
  C3-07-subject-tokens. Target `C1=met mutants=6 killed=6 survivors=0 total=6 arms=26`.
  Entering control: `C1=unmet` (arms=20, anchors absent).
- C2 calibration (5, tied lowest): the r85 C2 counter gains a replay pass that executes each
  `required` receipt's `# cmd:` in a scratch export of the receipt's `# rev:` and compares the
  body; two new r86 receipts, one of them a stale-body defeat. Selftest 18 -> 21 arms.
  Target `C2=met receipts=5 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2 matched=4
  defeated=1 legacy=3 unexpected=0`. Entering: `C2=unmet subject=stub`.
- C3 depth (5, tied lowest; capability acquisition): the r86 counter observes the census twice
  through two surfaces (drift token line and full report's values) and reconciles the r82
  classification's 14 bare-key `value-changed` rows with the value channel: `contradicting=2`
  names the two rows whose live value equals the baseline's. Target `C3=met observations=2
  aa=stable tokens=64 derived=64 name_agree=64 value_rows=14 contradicting=2`. Disclosed: applied
  retroactively the counter already reads met — the claim is the capability.

# Shared rules (binding on every seat)
- Write scope: /home/vgpnk/Projects/shokunin/mori-shokunin only, and inside it only the paths your
  item names. Absolute paths in every tool call: your tools start at the FLEET root, so a relative
  path lands in the wrong repo. Never write to /home/vgpnk/Projects/shokunin (fleet root), another
  lane's repo, MANIFEST.json, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`,
  `/home/vgpnk/Projects/shokuknow`, or `considerthese/`.
- Never commit, push, or run a mutating git/jj command in the LANE repo: no `git add`, `git
  commit`, `git checkout`, `git reset`, `git stash`, `git push`, and no mutating `jj` command.
  Read-only git (`log`, `show`, `diff`, `status`, `ls-tree`, `cat-file`, `rev-parse`, `clone
  --shared`) is fine. The L1 owns every lane commit. A scratch clone under your own scratch dir is
  a fixture: commits there use `-c user.name=t -c user.email=t@t` and are allowed.
- Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/mori-shokunin —
  write it at /home/vgpnk/Projects/shokunin/mori-shokunin/<that path>.
- Scratch: create your work dir under /fast/scratch/hyaku/mori-r86/<your seat name>/ and delete it
  before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell). Never write under /tmp; a /tmp path is
  never citable evidence. Use `git clone --shared` instead of full clones; never mirror the whole
  lane. `HYAKU_SCRATCH` defaults to /fast/scratch/hyaku.
- Fixture git repos: `D=$(mktemp -d -p your scratch)` then `git -C "$D" init -q`; assert
  `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit; every later
  git/jj call names `-C "$D"`.
- Detection and report only: no lane, OS, unit, service, credential, harness or orchestration
  state may be changed. mori never remediates. Do not run `agent://all`; message only the L1
  (agent id `MoriR86`) for a blocker.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the
  task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate) and
  record tool/version/channel/reason in your report. **pacman guard (orchestrator ruling
  2026-10-20): all pacman transactions are PAUSED host-wide** — install via `uv tool`/`npx`/an
  official binary in `~/.local/bin`, or file nothing; never `-Sy`, `-Syu`, `-U`, `-R`, never a
  partial upgrade.
- Honesty: an unrun check has not passed. Report failures, dead ends and surviving defects plainly;
  never restate a sibling's claim as your own measurement. Record the file hashes/revision you
  actually read, since siblings land work while you run.
"""


def item(name, role, axes, milestone, prompt):
    return {"name": name, "role": role, "axes": axes, "milestone": milestone,
            "prompt": prompt}


ITEMS = [
    item("Mo86E01C1Arms", "executor", ["operability"],
         "round 86 w1: six failing arms for the surviving r85-C3-counter mutants",
         """
Give `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/count-c3.py` the six
selftest arms the round-86 C1 counter requires, by extracting three pure helpers and wiring them in.

Frozen authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/contract.md`
P-C1 (the exact anchors, arm labels and target), and the counter
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/count-c1.py`.

File you may edit (sole writer): `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/count-c3.py`.
Do not touch any other file. The 20 existing selftest arms must stay green and unchanged.

Required after-form anchors (each exactly once; the mutants are applied to these):
- `return (rc == 0 and fields.get("verdict") == "met"` inside a new `subject_ok(rc, fields)` helper
  that also requires `fields.get("live") == "derived"`; `main()` calls `subject_ok(rc, fields)` in
  place of its inline `if rc != 0 or fields.get("verdict") != "met" or ...:` gate.
- `all(rc == 1 for rc in rcs)` and `all(tokens == first for tokens in token_lines[1:])` inside a new
  `stability(rcs, token_lines)` helper (compute `first = token_lines[0] if token_lines else []`);
  `observe_three` calls `stability` instead of its inline expression.
- `if word == "agreed":` stays exactly once in `reconcile`.
- `and subject_tokens == len(own_tokens)` inside a new `met_verdict(own_ok, stable, own_tokens,
  subject_tokens, unmatched, unnamed, malformed, duplicates)` helper carrying the whole current met
  expression; `main` calls it.

Arms to add (labels frozen; 20 -> 26), each a `cases.append((label, condition, line))`:
1. `stability_rc_must_be_1` — `not stability([0, 1, 1], [["a"], ["a"], ["a"]])`.
2. `stability_rc_required` — `not stability([2, 2, 2], [["a"], ["a"], ["a"]])`.
3. `stability_exact_order` — `not stability([1, 1], [["a", "b"], ["b", "a"]])`.
4. `subject_verdict_met_required` — `not subject_ok(0, {"verdict": "unmet", "live": "derived"})`.
5. `reconcile_agreed_skip` — `reconcile([("A", "agreed")], [])[1] == 0` (pristine unnamed=0; the
   `if False:` mutant makes it 1).
6. `met_requires_subject_tokens` — `not met_verdict(True, True, ["a"], 99, 0, 0, 0, 0)`.

Acceptance (in your own scratch, quote commands and outputs; do not weaken an assertion):
- a scratch copy of the edited file: `python3 -I <copy> --selftest` -> `C3_COUNTER_SELFTEST
  pass=26 fail=0`, rc 0;
- `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/count-c1.py HEAD
  --repo <a fixture repo containing your edited file at .ufo/waves/round-85/count-c3.py> --scratch
  <your scratch>` -> `C1=met mutants=6 killed=6 survivors=0 total=6 arms=26`, rc 0;
- the six anchors each occur exactly once: `grep -c` per anchor;
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --numstat --
  .ufo/waves/round-85/count-c3.py` (report it; the live behaviour of `main` must be unchanged apart
  from the helper extraction).
"""),
    item("Mo86E02C2Replay", "executor", ["calibration"],
         "round 86 w1: the receipt replay pass and its generator",
         """
Give `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/count-c2.py` a replay pass
that binds a receipt's body to its `# cmd:`, and write the r86 receipt generator.

Frozen authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/contract.md`
P-C2, and the counter `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/count-c2.py`
(read it: it defines the population, the expectation accounting and the exact target line).

File you may edit (sole writer): `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/count-c2.py`.
Also create: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/make-receipts-r86.sh`.
Do not touch any other file; the 18 existing arms must stay green.

What the subject must gain (frozen shape):
1. Header parsing of `# replay: required|none` and, for `none`, `# no-replay: <>=3 words>`; a
   missing reason on a `none` receipt is a problem.
2. `def replay_receipt(fields, repo, scratch, export_rev)` — write every repo-relative path the
   `# cmd:` names at the receipt's `# rev:` into a scratch export (use `git show <rev>:<path>` and
   `git cat-file -e`), run `bash -c "<cmd>"` there with `cwd=<export>`, `TMPDIR=<export>`,
   `GIT_CONFIG_GLOBAL=/dev/null`, `PYTHONDONTWRITEBYTECODE=1`, and compare stdout to the body
   modulo trailing newlines. A nonzero rc or a mismatch is a problem (`replay-rc:<n>` /
   `replay-mismatch`).
3. RECEIPTS grows to the five frozen receipts of the contract, each carrying `(expect, replay)`:
   the three r85 ones stay `legacy` (header grammar only; a named limit), plus
   `.ufo/waves/round-86/evidence/after-c1-r86.txt` (`required`, expect met) and
   `.ufo/waves/round-86/evidence/replay-defeat-r86.txt` (`required`, expect reject).
4. The tail becomes exactly
   `receipts=5 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2 matched=4 defeated=1 legacy=3 unexpected=0`
   with `met` iff every `expect=met` receipt has no problems and the `expect=reject` receipt has at
   least one; `bindings`/`bound` still count `# counter-sha256:` lines and their verified hashes at
   the receipt's own rev. Existing single-receipt counters' behaviour on the three legacy receipts
   must not regress.
5. Three new selftest arms: `replay_match` (a synthetic `# cmd:` that prints a known body taped to
   that body -> no problem), `replay_stale_mismatch` (same cmd, body one byte different ->
   `replay-mismatch`), `replay_none_requires_reason` (a `none` receipt without `# no-replay:` ->
   `missing-no-replay`). Total 21 arms.
6. `make-receipts-r86.sh <rev> [--repo DIR]` writes the two receipts: header lines `# receipt:`,
   `# cmd:` (exactly `python3 -I .ufo/waves/round-86/count-c1.py <rev> --repo <abs lane> --scratch
   .`), `# rev:`, one `# counter-sha256:` for `.ufo/waves/round-86/count-c1.py` at `<rev>`,
   `# replay: required`, `# limits: <sentence naming the limit>`, `# ---`, then the command's
   stdout verbatim; the defeat receipt is the same with one body byte changed (and a
   `# expectation: reject` line). Verify the revision with `git -C <repo> rev-parse <rev>^{commit}`.
   Do NOT write the real evidence files with the freeze revision: write them under your scratch and
   paste them in your report; the L1 regenerates them at the measured revision.

Acceptance: a scratch copy of the edited subject runs `--selftest` -> `C2_COUNTER_SELFTEST pass=21
fail=0` rc 0; a fixture repo containing your `make-receipts-r86.sh` output at a real revision makes
the subject print the target line (use a fixture repo whose `.ufo/waves/round-86/count-c1.py` is a
copy of the real counter and prove the replay matches; show the defeat receipt reading
`replay-mismatch` and the population summary `defeated=1 unexpected=0`). If a frozen shape is
unreachable, report the exact mismatch instead of changing it.
"""),
    item("Mo86E03C3Value", "executor", ["depth"],
         "round 86 w1: prove the C3 value channel is load-bearing",
         """
Prove the round-86 C3 counter's value channel is load-bearing, with fixtures only.

Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/contract.md` P-C3 and
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/count-c3.py`.

Deliverable: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/evidence/c3-value-controls.txt`
— one dated section per control with the command, full output and `rc=`:
1. **equal / contradicting**: a synthetic classification row whose field name has the same value in
   the baseline and in the live report must read `equal` and increment `contradicting` (build a
   fixture git repo carrying five paths the counter reads: a census stub that prints a full report
   with `window=launch..NOW`, a baseline carrying the same, the classification with one
   `DRIFT_CLASS -window value-changed` row, the snapshot and any `count-c2.py` stub the counter
   requires; the counter must read `C3=unmet` with `contradicting=1` and `tokens` matching your
   fixtures, not `met`).
2. **differs**: the same fixture with `window=other` live -> that row reads `differs`, so
   `contradicting=0` and the run is red on the token/derivation floors instead (report the exact
   unmet reason).
3. **masked**: baseline `window=<V>` -> the row reads `masked` and is never a contradiction.
4. **absent**: the live report lacks the field -> the row reads `absent`.
5. **stability**: two census runs that print the same tokens in different order must give
   `aa=unstable` (the exact-order rule), and two runs with the same tokens in the same order but a
   different non-volatile value must also give `aa=unstable` (the atom rule).
Also state, with a command, how many `VALUE` lines the real run prints and that the two
`contradicting` rows are `-subject_commits` and `-window` (paste the `VALUE` lines).
Fixture repos: `D=$(mktemp -d -p <your scratch>)`, `git init -q`, assert toplevel, commits with
`-c user.name=t -c user.email=t@t`. Never edit the counter, the contract or lane files.
"""),
    item("Mo86E04Controls", "executor", ["operability"],
         "round 86 w1: the standing battery and the freeze-time population controls",
         """
Two deliverables under `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/evidence/`:

1. `battery-r86.txt` — a dated battery receipt with a header line carrying the revision you ran at
   (`git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse fec2b328a4c83e0c61bc09d70e254ca47d547d34`
   for the baseline run) plus the command list and each command's rc/output summary. Use the
   command list in `.ufo/waves/round-85/evidence/battery-r85.txt` (its first ~40 lines name the
   commands and the SETUP class); run the same commands from the lane worktree with `TMPDIR` inside
   your scratch, classify `rc=2`-because-TMPDIR cases as SETUP exactly as that file does, and print
   `BATTERY pass=<n> setup=<n> fail=<n>` at the end. Do not change any tool.
2. `population-controls-r86.txt` — the C1 label-only stub control re-run at the freeze plus the
   three r86 counters' own selftest tallies, each with command, output and rc:
   - build the stub fixture repo under your scratch with a `.ufo/waves/round-85/count-c3.py` that
     prints the six PASS labels and `C3_COUNTER_SELFTEST pass=26 fail=0` while implementing
     nothing; `python3 -I .ufo/waves/round-86/count-c1.py HEAD --repo <stub repo> --scratch <dir>`
     must print `C1=unmet ... survivors=6`;
   - `python3 -I .ufo/waves/round-86/count-c1.py --selftest`, `count-c2.py --selftest`,
     `count-c3.py --selftest` -> `pass=15/11/22 fail=0` (or the current arm counts; report what you
     measure and the file hashes).
Report the exact numbers you measured; if the lanes' arms are already landed when you run, record
both readings and say which revision each belongs to.
"""),
    item("Mo86S01Lesson", "scribe", ["calibration", "freshness"],
         "round 86 w1: the round lesson with one mined mistake and the source Gate block",
         """
Write `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-86.md` in the shape of
`corpus/lessons/round-85.md` (read it first): a short `## What the round did`, a `## Mistakes`
section with ONE mined mistake in the frozen four-field shape (`class · evidence pointer ·
captured-by (the criterion or rule that should have caught it, or none) · fix`), and a `## Gate`
block that records, for every SOURCES row the round adds or touches, the URL, the access date
(2026-11-04) and a ≤25-word located quote.

Candidates for the mined mistake (pick ONE, verify it yourself from committed bytes):
- the r85 receipt grammar bound a digest, not a body, so a stale body passed (the r85 mutation
  probe's C2 survivors and `corpus/lessons/round-85.md` name it) — class `predicate-underreach`,
  captured-by `r85 C2's own named limit` (or `none`), fix = the replay pass;
- the r82 classification labels every baseline-present key `value-changed` on name existence
  alone; the r86 value channel shows 2 of 14 rows carry equal live values (`-subject_commits`,
  `-window`) — class `class-label-overreach`;
- a pivot: the r85 verifier's routed defects (the `<fill>` placeholder, the contradictory
  `controls-r85-entering.txt`, the missing contract A4 block) — class `record-integrity`.
For the Gate block, coordinate with the scribe `Mo86S02Sources` (write only if it has not already
written the block; if it has, append your Gate rows after it and say so).

Constraints: never rewrite an existing lesson; the file is new. No commits. Write only that path.
"""),
    item("Mo86S02Sources", "scribe", ["coverage", "depth"],
         "round 86 w1: one opened source row and one knowledge entry that cites it",
         """
Carry the round's sourced claim: open ONE source this round, add its row to
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`, and write ONE knowledge entry
that cites the row.

Frozen contract: `/home/vgpnk/Projects/shokunin/CORPUS.md` section *SOURCES.md — where a shokunin
learns* (contract v1) and `corpus/README.md` `## Frontier`. Read
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` (374 rows; the last ids are S600,
S601 — verify the highest id yourself with the census parser pattern `^ {0,3}\\|[[:space:]]*S[0-9]{3,}`)
and `corpus/knowledge/receipt-provenance-r85.md` for the shape.

Topic that fits the round: a primary source on **reproducible/verifiable execution evidence** —
the property that a recorded output can be re-derived by re-running the recorded command (the r86
C2 replay rule), or on **mutation testing / test-suite adequacy** (the r86 C1 arm rule). Candidate
primary sources to open (verify each live; use the one whose located quote you can stand behind):
- https://reproducible-builds.org/docs/definition/ (already S600 — do not duplicate; cite it if
  apt)
- https://www.sqlite.org/testing.html (sec. on mutation testing / test coverage)
- https://arxiv.org/abs/2404.09241 (already rejected S601)
- https://google.github.io/oss-fuzz/ or the AFL++ docs on test oracles (if apt)
Pick one NOT already in SOURCES.md (check by URL with the census parser pattern; a duplicate URL
is an E-code). Mechanics:
1. Fetch the source (curl with a User-Agent), save the bytes under
   `.ufo/waves/round-86/evidence/sources-r86/<slug>.html` (that path is yours), record size, lines,
   sha256, HTTP status and the final URL.
2. Write the knowledge entry at `corpus/knowledge/<topic>-r86.md` with `source: S###`,
   `verified-at: 2026-11-04`, `recheck:`, `coverage-map:` lines and a `## Gate` block carrying the
   URL, access date and a located ≤25-word quote (quote must be ≤25 words and verbatim at the
   cited lines).
3. Append the SOURCES row in the 11-column schema (`S###`, url, title, tier, kind, status `mined`,
   verified date, recheck cadence, `used-by` naming your entry, notes). Insert it at the end of the
   registry table, append-only; never edit an existing row.
4. Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin mori` and paste the output with its rc (must be 0; W04 warnings
   tolerated).
If you cannot open a source that fits, say so plainly and leave the registry untouched; a fabricated
row is worse than none.
"""),
    item("Mo86Sc01Scout", "scout", ["coverage"],
         "round 86 w1: every consumer of the changed surfaces",
         """
Read-only reconnaissance: map every consumer of the three surfaces round 86 changes, so the L1
knows what a landing could break. Report absolute paths and line numbers, no edits.

Surfaces:
1. `.ufo/waves/round-85/count-c2.py` — every receipt in the lane that carries a `# cmd:`/`# rev:`/
   `# counter-sha256:` header (grep the lane and the fleet `.ufo/reports/`), plus every tool that
   writes or reads such receipts (`tools/mori-receipt-complete.py`, `tools/mori-control-receipt.py`,
   `tools/mori-claim-sweep.py`, `tools/mori-record-sweep.py`, `.ufo/waves/round-*/make-receipts*.sh`).
   For each, state whether a `# replay:` header addition breaks its parser (read the parser).
2. `.ufo/waves/round-85/count-c3.py` — everything that imports or copies its helpers (`stability`,
   `reconcile`, `derive`, `subject_signal`), and every counter that shells out to it.
3. `corpus/evidence/drift-classification-r82.txt` — every reader (grep `drift-classification`,
   `DRIFT_CLASS`), and whether any of them would be affected by a value-channel reading.
4. Sibling-lane overlap (read-only): grep `/home/vgpnk/Projects/shokunin/*-shokunin/.ufo/waves/`
   and `/home/vgpnk/Projects/shokunin/*-shokunin/tools/` for receipt replay, body-vs-command
   binding, or `value-changed` classification logic; name each and whether mori's rule duplicates,
   complements or conflicts with it. Report only; never edit a sibling lane.
Deliverable: your seat report (no other file), naming for each surface the consumers, the exact
lines, and a one-line risk verdict (`none` / `breaks:<what>` / `needs-review`).
"""),
    item("Mo86R01ReviewC1", "reviewer", ["operability"],
         "round 86 w1: falsify the C1 arms claim",
         """
Adversarial review of the round-86 C1 claim. Author no part of it; re-derive from committed bytes.

Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/contract.md` P-C1 and
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/count-c1.py`.

Do:
1. Independently locate the six anchors in `.ufo/waves/round-85/count-c3.py` at the revision you
   read (state the file sha256 you measured, since a sibling may still be landing the arms). For
   each anchor: occurrence count, and whether the mutated line can change the subject selftest's
   exit or `fail=` tally.
2. Re-derive the arm count yourself (`grep -c 'cases.append('`) and the six labels' presence.
3. Try to defeat the claim without doing the work: build a stub subject that prints the labels and
   `pass=26 fail=0` and grade it with the r86 counter — it must read `C1=unmet` with six survivors.
   Then build a stub that *also* carries the six anchors as live code that the mutations do not
   reach (e.g. anchors inside functions the selftest never calls) — if that reads `C1=met`, the
   claim is fakeable: report it as a defect of the claim with the fixture.
4. Check the kill rule's edges: an anchor occurring twice (`unanchored`), an empty mutation, a red
   pristine, a missing label — does the counter read unmet in each case (write the fixture)?
5. Verify no other lane file was changed by the arms (diff numstat against the entering revision
   for `.ufo/waves/round-85/count-c3.py` only).
Deliverable: your seat report with a verdict per item (`holds` / `defect:<what>`), the exact
commands and outputs, and the revision/hashes you measured. Never edit lane files.
"""),
    item("Mo86R02ReviewC2", "reviewer", ["calibration"],
         "round 86 w1: falsify the C2 replay claim",
         """
Adversarial review of the round-86 C2 claim. Author no part of it; re-derive from committed bytes.

Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/contract.md` P-C2 and
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/count-c2.py`.

Do (state the revision and every file sha256 you read; a sibling may still be landing the work):
1. Read the amended `.ufo/waves/round-85/count-c2.py` (when present) and verify the replay pass: it
   must execute the `# cmd:` in an export of the receipt's own `# rev:`, not at the tip, and must
   compare stdout, not a digest. Name any line where it could still read only a digest or read at
   the tip.
2. Build a stale-body receipt yourself in a fixture repo: correct headers, correct rev, correct
   `# counter-sha256:`, body with one changed byte. Show the amended subject rejects it
   (`replay-mismatch`) and a header-only grader accepts it (that difference is the claim).
3. Attack the replay export: a cmd naming a path that exists at the tip but not at the receipt's
   rev (must not be exported and must fail, not silently pass); a cmd that writes a file (must not
   mutate the lane); a cmd whose stdout differs only by trailing newlines (must match — the frozen
   normalization).
4. Verify the five-receipt population and the expectation accounting: with the defeat receipt
   present the summary is `matched=4 defeated=1 unexpected=0`; delete it and the run must be unmet.
Deliverable: your seat report with a verdict per item (`holds` / `defect:<what>`), commands,
outputs, and the exact revision read. Never edit lane files.
"""),
    item("Mo86C01Critic", "critic", ["calibration"],
         "round 86 w1: falsify all three claims and their counters",
         """
Falsify the round's three claims as claimed. You author none of them.

Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/contract.md` (P-C1,
P-C2, P-C3), the three counters, and `evidence/controls-r86.txt`.

For each claim, answer with evidence:
1. **Do-nothing control.** Name the cheapest action that reaches the target without the work, and
   measure it. (C1: a label-only stub must read unmet; C2: a header-only gate against the defeat
   receipt must read met — which is why replay is the claim; C3: the counter applied retroactively
   reads met, disclosed — check the contract says so and that the capability row is what is
   claimed.)
2. **Counter self-reference.** Does the counter's own selftest gate the same clause it grades? Try to
   make the counter print `met` while the subject is unarmed (e.g. mutate the counter's TARGET
   constants, or feed a fixture repo whose subject bytes satisfy the target but not the contract).
3. **Predicate-to-code identity.** For each of the three target lines, name the code expression that
   computes each field and any field that is printed but not computed (a fabricated number is a
   fatal defect).
4. **Harm check.** Do the three claims touch the same file? (They must not: C1 = r85 count-c3.py,
   C2 = r85 count-c2.py + receipts, C3 = r86 count-c3.py.) Diff the lane against the entering
   revision and name every changed path with its author-facing purpose.
5. **Claim sizing.** Is each after-state one concrete value a closure can re-derive with one
   command? Is any target narrowed after data (compare the contract at the freeze commit
   `5e80229a450fa007d73ad0fb8bc3147e4adf5438` with the file at the tip)?
Deliverable: your seat report, one verdict per claim (`holds` / `defect:<what>`), with commands and
outputs. Never edit lane files.
"""),
    item("Mo86M01Mut", "mutation-tester", ["operability"],
         "round 86 w1: mutation probe of the three r86 counters",
         """
Probe the three round-86 counters with mutations, as the r85 probe did for its subjects.

Subjects (byte-exact at the freeze `5e80229a450fa007d73ad0fb8bc3147e4adf5438`, or at the tip if
they changed — report the sha256 you used):
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/count-c1.py`, `count-c2.py`,
`count-c3.py`.

Method (frozen by the r85 probe's rule): for each mutant, one scratch copy, the anchor `old` must
occur exactly once (`occurrences=1`, else refuse), then that copy's own `--selftest`; killed iff
rc != 0 or `fail=<n>` with n > 0. Pristine baselines first. Then, for non-equivalent survivors,
demonstrate an end-to-end verdict flip with a fixture repo where feasible (a counter that prints
`met` for an unarmed subject, or `unmet` for a correct one).
Targets worth mutating (non-exhaustive; add what you find): the TARGET/TARGET_ARMS constants and
the `target_split` conjuncts in count-c1; the population/replay expectation logic and `tail`
arithmetic in count-c2; the `value_rows`/`contradicting`/`name_agree` conjuncts and the
volatile-drop in count-c3; the three counters' `own_ok` self-detector gates.
Deliverable: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-86/evidence/mutation-r86.md`
with `MUTANTS total=<n> killed=<n> survivors=<n>` headline, a per-mutant table (site, mutation,
class, observation) and a `## Unarmed clauses to arm next round` list for round 87. Fixture repos
under your scratch, `-c user.name=t -c user.email=t@t`, toplevel asserted. Never edit a lane file.
"""),
    item("Mo86K01Conn", "connector", ["adjacency"],
         "round 86 w1: sibling-lane overlap scan",
         """
Read-only cross-lane scan: does any sibling lane already hold the rule mori lands this round, and
does mori's version conflict with it?

Scan (read-only; never write to a sibling repo):
- `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge/` and `corpus/lessons/` for
  receipt/evidence replay, body-versus-command binding, `# cmd:`/`# rev:` grammars, or value-level
  drift classification;
- `/home/vgpnk/Projects/shokunin/*-shokunin/.ufo/waves/round-*/count-c*.py` for counters that
  grade a subject's bytes at a revision (mori's pattern) and for any that already replay commands;
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/` (orchestration) and
  `/home/vgpnk/Projects/shokunin/kotodama-shokunin/` for a receipt gate with the same claim.
For each hit: absolute path, the rule it implements, and a verdict — `duplicate` (mori should cite
it and not re-claim), `complement` (mori's rule adds a distinct axis), or `conflict` (the two rules
would disagree on the same input; name the input). Also name any lane whose tools read mori's
`drift-classification-r82.txt` or the r85 counters, so the L1 knows who to notify.
Deliverable: your seat report; no edits anywhere. If the scan finds nothing, say so with the exact
greps you ran.
"""),
]

SPEC = {
    "wave": "mori-r86-w1",
    "milestone": ("Round 86 w1: six surviving r85-C3-counter mutants armed, the receipt body bound "
                  "to its command, and the classification's value channel; counters frozen in "
                  "5e80229a450f."),
    "axes": ["coverage", "operability", "depth", "freshness", "calibration", "adjacency"],
    "reportDir": ".ufo/waves/round-86/w1",
    "maxLanes": len(ITEMS),
    "context": CONTEXT,
    "items": ITEMS,
}

with open(LANE + "/.ufo/waves/round-86/w1-spec.json", "w", encoding="utf-8") as handle:
    json.dump(SPEC, handle, indent=1)
    handle.write("\n")
print("wrote", LANE + "/.ufo/waves/round-86/w1-spec.json", "items:", len(ITEMS),
      "roles:", sorted({it["role"] for it in ITEMS}))
