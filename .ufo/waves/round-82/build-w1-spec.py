#!/usr/bin/env python3
"""Build mori round-82 wave w1 spec (one v1 wave, 15 seats, band 8-16).

Writes .ufo/waves/round-82/w1-spec.json. The Godspeed directive bytes are copied verbatim
from the round-81 spec (the host binding), never retyped. Every item prompt is self-contained;
shared rules ride the wave context.
"""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
ROUND = LANE + "/.ufo/waves/round-82"
R81 = LANE + "/.ufo/waves/round-81/w1-spec.json"

with open(R81, encoding="utf-8") as handle:
    r81 = json.load(handle)
GODSPEED = r81["context"].split("\n\n# Goal", 1)[0]
assert GODSPEED.startswith("/skill:godspeed"), GODSPEED[:40]

CONTEXT = GODSPEED + """

# Goal
mori round 82 (attempt 1), wave w1 — build, record and first falsifiers for THREE frozen
claims. mori is a fleet/host observability lane: detection and report only. Entering revision
`ebcf2c72df203c855cfafb5223c6e22b1e12c481`; the freeze commit is `20551e56`.

Read first, in this order (absolute paths):
- {round}/contract.md — THE FROZEN AUTHORITY: P-C1, P-C2, P-C3, the mutation set, the drift
  derivation table, the revision-arm interface, the real bindings and the do-nothing controls.
- {round}/evidence/controls-r82.txt — the measured entering controls.
- {lane}/SCORECARD.md (`## Axes`, `## Retired`, `## Round 80`, `## Round 81`, `## Planned (round
  82)`, the capabilities tables), {lane}/SKILL.md (the gate registry near the end),
  {lane}/PROVINCE.md (`## Instrument inventory (round 80)`), {lane}/corpus/QUALITY.md (last
  criteria), {lane}/corpus/README.md (`## Frontier`).
- {lane}/corpus/lessons/round-81.md and {lane}/corpus/lessons/round-81-verifier-spotcheck.md
  (`## Routed defects the lane must fix next round` — D81-1..D81-6).

# Round claims (frozen before this wave; do not change them)
- C1 operability (7), capability acquisition: a committed, revision-agnostic mutation harness
  (`.ufo/waves/round-82/count-c1.py`) re-derives the r81 five-survivor set and prints
  `C1=met harness=present killed=11 survivors=0 total=11 pristine=green`; entering is
  `C1=unmet harness=absent`. The delta is the capability (r81's harness was scratch-only and
  deleted, D81-3).
- C2 freshness (5, tied lowest): the red round-10 drift pin is retired with a derived
  classification of all 64 live drift tokens; entering is `C2=unmet tokens=64 classified=0
  retired=0 cell=0`, target `C2=met tokens=64 classified=64 agreed=64 residual=0 retired=1 cell=1`.
- C3 depth (5, tied lowest): `tools/mori-record-sweep.py` gains the `revision` arm (a row's
  stated value must exist in the bytes of the revision it names) plus real bindings; entering is
  `C3=unmet tool=present arm=absent`, target `C3=met tool=present arms>=30 defeated=1
  bindings=3 revisions=0`.

# Shared rules (binding on every seat)
- Write scope: {lane} only, and inside it only the paths your item names. Absolute paths in every
  tool call: your tools start at the FLEET root, so a relative path lands in the wrong repo.
  Never write to /home/vgpnk/Projects/shokunin (fleet root), another lane's repo, MANIFEST.json,
  `.ufo/state/`, `.ufo/watchdog.log`, or `.scratch/`.
- Never commit, push, or run a mutating git/jj command anywhere: no `git add`, `git commit`,
  `git checkout`, `git reset`, `git stash`, `git push`, and no mutating `jj` command. Read-only
  git (`log`, `show`, `diff`, `status`, `ls-tree`, `cat-file`, `rev-parse`, `archive`) is fine.
  The L1 owns every commit. Never rewrite another seat's file outside your item's scope.
- Every `Report:` trailer path is relative to {lane} — write it at {lane}/<that path>.
- Scratch: create your work dir under /fast/scratch/hyaku/mori-r82/<your seat name>/ and delete
  it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell). Never write under /tmp; a /tmp path
  is never citable evidence. Clone with `git clone --shared` or `git worktree add`; never mirror
  the whole lane. `HYAKU_SCRATCH` defaults to /fast/scratch/hyaku.
- Detection and report only: no lane, OS, unit, service, credential, harness or orchestration
  state may be changed. mori never remediates.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the
  task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate) and
  record tool/version/channel/reason in your report. pacman is PAUSED host-wide: never run a
  pacman transaction of any kind (`-S`, `-Sy`, `-Syu`, `-U`, `-R`); use `uv tool`, `npx`, or an
  official binary in ~/.local/bin, or file an L0 question instead.
- Never message `agent://all`. Message only your own L1 (`agent://MoriR82`) for a blocker.
- Do not spawn subagents except an executor's single read-only `labrat` probe.
- Your final report must name: what you changed/produced with absolute paths, the exact commands
  you ran with their output, what you verified, what you could not verify, and any defect you
  found in another seat's bytes (file:line). Be adversarial about your own work: an unrun check
  has not passed.
"""


def item(name, role, prompt, milestone):
    return {"name": name, "role": role,
            "axes": ["operability", "freshness", "depth", "coverage", "calibration", "adjacency"],
            "milestone": milestone, "prompt": prompt}


MIL_C1 = "round 82 w1: C1 mutation-harness capability and its regression simulation"
MIL_C2 = "round 82 w1: C2 drift-pin retirement with derived classification"
MIL_C3 = "round 82 w1: C3 revision-precision arm, real bindings, source and knowledge"
MIL_REC = "round 82 w1: record, sources and falsification"

ITEMS = [
    item("Mo82E01C1Regress", "executor", """
Prove the C1 harness can FAIL — a capability is not a capability until its detector is shown
sensitive on the lane's own bytes.

Frozen authority: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/contract.md
(P-C1 and its mutant table).

1. Read `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/count-c1.py` and state,
   per mutant, whether the kill is produced by the r81-added arm or by an older arm.
2. Build a **committed** regression simulator at
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/simulate-regression.sh`:
   it copies `.ufo/waves/round-80/count-c1.py` (a scratch copy, never the lane file) and
   **deletes** the r81-added `sweep_zero_summary_nonzero_exit` fixture row from its selftest
   tuple, then runs the round-82 harness against that mutated revision-producing copy and shows
   it reports `survivors=1` for `ignore_sweep_exit`. Do the same for one `count-c3.py` and one
   `count-c2.py` arm. The harness must be driven without touching lane bytes: use `git archive`
   or a scratch tree plus `count-c1.py --repo <scratch repo>`; the script must honour `TMPDIR`
   and `HYAKU_SCRATCH` and must not hardcode `/tmp`.
3. Run it; write the receipt to
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/evidence/regression-sim-r82.txt`
   (command, output, rc, the exact revision used).
4. If the harness reports `survivors=0` for a deleted arm, that is a detector defect — report it
   with file:line instead of working around it.

Report: paths, commands, output, and the per-mutant kill attribution table.
""", MIL_C1),

    item("Mo82E02C3Arm", "executor", """
Implement the frozen `revision` arm in the lane's record sweep.

Frozen authority: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/contract.md,
section "Frozen arm interface" (P-C3). Read it exactly; the r81 arms and summary tokens must stay
byte-compatible.

File: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py` (225 lines, r81).

Requirements:
- pins file may carry `"revisions": [{carrier, row_contains, key, value, rev, path}, ...]`;
- per binding, in order: the carrier's FIRST table row containing `row_contains` must state
  `key=value` (else `REVISION_MISMATCH <carrier>:<line> row-value`); `rev` must resolve to a
  commit (else `rev-unresolvable`); `path` must exist at `rev` (else `path-absent`); and
  `key=value` must occur in `path`'s bytes at `rev` (else `REVISION_MISMATCH <carrier>:<line>
  rev-bytes`). Every binding is graded, never the first only; a missing row is a mismatch.
- git reads use `--git DIR` (default: `--root`); the summary line gains `revisions=<count>`;
  the three r81 counters (`pending=`, `pinned=`, plus `bindings=`/`carriers=`) keep their names
  and meanings.
- `--selftest` gains arms for: conformant binding, the D81-1 defeated shape (row states
  pointers=240, the named revision's bytes hold pointers=237), unresolvable rev, path absent at
  rev, missing row, and a two-binding list where the second is stale. Keep the existing 26 arms
  and add at least four; print `RECORD_SWEEP_SELFTEST pass=N fail=0`.
- `python3 -I` safe, standard library only, stdout only, no writes outside `git` reads.

Run `python3 -I tools/mori-record-sweep.py --selftest` and paste the tally. Do not write the
lane's pins file (another seat owns it) and do not edit SCORECARD/LOG/SKILL/PROVINCE.
""", MIL_C3),

    item("Mo82E03C3Pins", "executor", """
Write and independently verify the lane's real revision bindings.

Frozen authority: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/contract.md —
the "Real bindings" table (3 rows).

1. Write `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/record-pins.json` with
   a `revisions` list holding exactly those three bindings (`carrier`, `row_contains`, `key`,
   `value`, `rev` as full 40-hex shas, `path`), plus an empty-or-absent `bindings` list for the
   r81 pinned arm (do not invent r81 pinned bindings).
2. Independently verify each binding with plain read-only git BEFORE trusting the tool: print the
   matching SCORECARD row at the carrier revision, and `git show <rev>:<path> | grep -c
   '<key>=<value>'`. All three must be green at the freeze; if one is red, report it with the
   measured count and do not weaken the binding.
3. Write the receipt
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/evidence/c3-bindings-r82.txt`
   (each binding, its row line number at the carrier revision, the grep count, rc).
4. Also record the same three checks with a deliberately **wrong** revision substituted
   (e.g. `075574c8` for the pointers binding) to show the check is sensitive; name it
   `defeated-shape` in the receipt and do not write it into the pins file.

Do not edit `tools/mori-record-sweep.py` (another seat owns it) and do not touch SCORECARD.
""", MIL_C3),

    item("Mo82E04C2Drift", "executor", """
Produce the C2 drift evidence and the derived classification file.

Frozen authority: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/contract.md —
P-C2 and the frozen derivation table. The measured entering control is
`.ufo/waves/round-82/evidence/controls-r82.txt` (`tokens=64`).

1. In the lane worktree run
   `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json`
   (exit 1 expected) and save the raw output verbatim to
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/evidence/drift-r82-live.txt`
   with the command, timestamp and rc.
2. For EVERY token on the `MORI_DRIFT:` line, derive its class from the baseline bytes with the
   contract's frozen table — derive it, do not guess: `SURFACE:<name>`/`FINDING:<NAME>` are
   `value-changed` when that id exists in the baseline canonical block, else `added-since-r10`;
   `VERDICT`/`HEADER`/`BLANK` are `value-changed`; a bare/`+`/`-` key is `value-changed` when
   `<key>=` occurs in the baseline bytes, else `added-since-r10`. Write a small throwaway runner
   in your scratch that applies the table mechanically and prints the token, its derived class
   and the evidence line that decided it.
3. Write `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/drift-classification-r82.txt`:
   a short header comment (baseline path, the census command, the token count, the date
   2026-11-04) and exactly one `DRIFT_CLASS <token> <class>` line per live token, in the live
   order. No token may be missing, none may be extra, none may be `unexplainable`.
4. Re-run the census once more and confirm the token list is byte-identical; if it changed
   between runs, report both lists and stop — do not pick one.

Do not edit SCORECARD.md, LOG.md or the contract; the L1 owns them.
""", MIL_C2),

    item("Mo82E05Battery", "executor", """
Re-run the lane's standing verification battery at the round-82 tip and capture the no-harm
receipt.

Inputs: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/battery.sh` (the r81
runner) and `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/evidence/`
(receipts the r81 round used).

1. Read the r81 runner and list the instruments it covers. Add the three round-82 counters
   (`count-c1.py`, `count-c2.py`, `count-c3.py` under `.ufo/waves/round-82/`) in `--selftest`
   mode to a scratch copy of the runner; keep the rest as-is.
2. Run it with `HYAKU_SCRATCH=/fast/scratch/hyaku/mori-r82/Mo82E05Battery`. Save the full output
   to `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/evidence/battery-r82.txt`
   and report the per-instrument rc and the tallies.
3. Any instrument that fails at the tip is a finding: name the file:line, the command and the
   first failing case. Do not "fix" any instrument other than the three round-82 counters (which
   belong to the L1 freeze; report a defect instead of editing them).
4. Report the four known setup refusals the r81 receipt classified as lane-scoped-scratch setup,
   or the new classification if it differs.

Do not edit any lane instrument.
""", MIL_REC),

    item("Mo82S01Lesson", "scribe", """
Draft the round-82 lesson.

Output: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-82.md`. Sections, in
this order, using the r81 lesson as the shape:
- header (round, date 2026-11-04, entering `ebcf2c72df203c855cfafb5223c6e22b1e12c481`, freeze
  `20551e56`), the three claims with their keepers and targets, and the axes;
- entering controls, copied verbatim from `.ufo/waves/round-82/evidence/controls-r82.txt`
  (state that they are inherited receipts, not rerun by you);
- `## Gate`: the source dispositions for this round — ONE admitted row for the git revision
  syntax source the scout `Mo82Sc01Source` opened (cite its pinned copy path, sha256, byte/line
  count and the ≤25-word located quote; the next unused row id is **S597**, verify that against
  `corpus/SOURCES.md`), and at least one rejection with its flip condition. If the scout's
  material is not on disk when you start, write the Gate as a recommendation table with a clear
  `PENDING SCOUT` marker rather than inventing a quote;
- `## Mistakes`: at least three rows, class · evidence pointer · captured-by (the criterion or
  rule that should have caught it, or `none`) · fix. Mine at least: (a) D81-1/D80-4 the
  revision-label class the lane repeated twice, captured only by a non-author closure; (b) D81-3
  the scratch-only mutation harness whose receipt no longer resolves; (c) the round-10 drift pin
  kept red for 72 rounds with no classification surface. Each fix must be something this round
  actually landed, and say what makes it able to fail;
- `## Census`: the before/after source-row census with the exact command
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
  and both exits; the entering count is 369 rows exit 0 (read it from the r81 lesson) and the
  after count is whatever you measure — do not guess.

Do not edit SCORECARD.md, LOG.md, SKILL.md, PROVINCE.md or SOURCES.md.
""", MIL_REC),

    item("Mo82S02Knowledge", "scribe", """
Draft the round-82 knowledge entry for the revision-precision gate.

Output: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/record-revision-precision-r82.md`.

Content requirements:
- opening `source: S597`, `verified-at: 2026-11-04`, `recheck: 365d` lines (the S-id is assigned
  by the scout's Gate; if `corpus/SOURCES.md` does not yet carry S597 when you write, put
  `source: S597 (pending Gate landing)` and say so in your report — never invent a URL);
- the defect class in one paragraph: a record row states a measured value and a revision, and the
  revision does not contain the value (D80-4 at `97ce0c96`, D81-1 at `075574c8` with
  `pointers=240`, where the graded count is 237);
- a decision table for the arm: row-value / rev-unresolvable / path-absent / rev-bytes, with the
  exact message token for each and what a reader should do;
- the real binding population (the three frozen bindings) and why presence of `key=value` in the
  named path's bytes at the named revision is a cheap, sufficient lower bound — and what it does
  NOT prove (it cannot tell a coincidental occurrence in an unrelated line from the graded one;
  it does not prove the command's output, only the record's arithmetic);
- one worked example over the D81-1 shape with the actual command and its output (you may run
  `git show 075574c8:SCORECARD.md | grep -c 'pointers=240'` — read-only — and paste the `0`);
- a boundary paragraph: this gate grades the lane's own record, never another lane's, and it is
  not a lifecycle or admission decision.

Do not edit SCORECARD.md, LOG.md, SKILL.md, PROVINCE.md or SOURCES.md.
""", MIL_C3),

    item("Mo82Sc01Source", "scout", """
Open the source that grounds the revision-precision arm, and pin it.

Target ground: git's `<rev>:<path>` object-name syntax and its exit behaviour — the arm reads
`git show <rev>:<path>` and `git rev-parse --verify <rev>^{commit}`.

1. Fetch the official git documentation pages (man7/progit/git-scm or the git project's own
   Documentation), choose the one that states the `<rev>:<path>` syntax precisely (candidates:
   `gitrevisions(7)` section "Specifying revisions", `git-cat-file(1)` / `git-show(1)`), and
   record: URL, HTTP status, access date 2026-11-04, final URL after redirects.
2. Save a durable pinned copy under
   `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r82/` named after the
   document and version (e.g. `gitrevisions.7.git-2.51.0.html`), with its sha256 and byte/line
   count. Prefer an authoritative source over a mirror; if only a mirror is reachable, say so and
   downgrade the tier.
3. Locate the exact quote (≤25 words) that states the `<rev>:<path>` syntax and give its line
   numbers in the pinned copy.
4. Check the lane registry for a duplicate: is the same base URL already a `corpus/SOURCES.md`
   row? Print the matching ids. The next unused row id should be S597 — verify with
   `grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort | tail -3`.
5. Report a reject candidate too (one source you deliberately did NOT admit, with the reason and
   a flip condition), so the lesson has ≥1 reject.

Write only under `corpus/evidence/sources-r82/`; never edit `corpus/SOURCES.md`, the lesson or a
knowledge entry.
""", MIL_C3),

    item("Mo82Sc02Surface", "scout", """
Reconnaissance: every consumer of the round-10 drift baseline and of the freshness axis cell, so
the retirement is consistent and nothing silently keeps the red literal.

1. Search the lane (`grep -rn`) for `baseline-r10-20261015T2231Z`, `drift pin`, `--drift`,
   `drift-classification`, `MORI_DRIFT`, restricted to the lane repo. Report every hit with
   file:line and classify it: record claim (SCORECARD/LOG), tool behaviour (tools/), lesson
   history (corpus/lessons), knowledge entry, or other.
2. Read `SCORECARD.md`'s `## Axes` freshness row, `## Retired`, the round-20/21/22 sections and
   `corpus/README.md`'s round-21 correction, and state exactly which sentences would have to
   change for a retirement to be honest and which must stay byte-unchanged (history).
3. Read `tools/mori-census.sh`'s drift block (`drift_normalize`, `drift_line_id`, `drift_report`)
   and state, from the code, what kinds of tokens a `MORI_DRIFT:` line can carry and how a
   whole-line fallback token (`drift_field_report` last line) is named.
4. Report insertion points for the L1: the exact table row and section where a `drift-pin-r10`
   retirement row belongs, and any other file that must mention the classification path
   (SKILL.md gate registry row? PROVINCE inventory?). Give line numbers at the current tip.
5. Name any consumer that would be BROKEN by the retirement (e.g. a tool that expects a red
   `--drift` exit as an input) — that is the most important finding.

Read-only: change no file.
""", MIL_REC),

    item("Mo82R01C1", "reviewer", """
Adversarial review of C1 (the mutation-harness capability). Attack the claim.

1. Read `.ufo/waves/round-82/contract.md` P-C1 and `.ufo/waves/round-82/count-c1.py`. Re-derive
   the claimed numbers yourself: for each of the 11 mutants, apply the anchored replacement to a
   scratch copy of the file at `ebcf2c72`, run that copy's own `--selftest --scratch <dir>`, and
   report rc and the `fail=` tally. Compare with the harness's verdict per mutant.
2. Attack the detector: (a) a counter whose selftest exits 0 with `fail=0` but whose graded
   behaviour is inverted — does the harness report `survived`? (b) a counter whose selftest
   prints `fail=0` in a comment and `fail=1` elsewhere — which wins? (c) an anchor occurring
   twice — is it excluded or double-counted? (d) a pristine file that is already red — is it
   `pristine=red` and unmet? (e) does `--selftest` of the harness itself assert anything the
   real run does not?
3. Attack the claim boundary: the contract says the delta is the capability, not new kills. Is
   that honest? State what a do-nothing round cannot reach and whether `harness=absent` at
   `ebcf2c72` is genuinely the only delta.
4. Name every defect with file:line and a severity. Do not fix anything: report only.

Report: the per-mutant table you measured, each attack's outcome, and a verdict line
`C1_REVIEW: agree|disagree <reason>`.
""", MIL_REC),

    item("Mo82R02C2", "reviewer", """
Adversarial review of C2 (the drift-pin retirement). Attack the claim.

1. Read `.ufo/waves/round-82/contract.md` P-C2 and `.ufo/waves/round-82/count-c2.py`. Run the
   counter's `--selftest` and re-derive two of its arms by hand.
2. Re-derive the classification independently: run the census drift yourself, and for ten tokens
   (include at least one `SURFACE:`, one `FINDING:`, one `VERDICT`, one bare key and one
   `+`-prefixed key) derive the class from the baseline bytes without reading
   `corpus/evidence/drift-classification-r82.txt`, then compare.
3. Vacuity attacks: (a) could the claim be met by deleting the freshnes cell's red literal
   without the retired row or the classification? (b) by labelling everything
   `added-since-r10`? (c) by pointing the retired row at a different baseline file? (d) by
   editing the baseline? (e) is a green census run accepted as `met`?
4. Judge the retirement itself: does it hide the retained-evidence-loss blocker from round 21?
   Read `SCORECARD.md`'s round-21 correction and `corpus/README.md`'s round-21 note, and say
   whether the landed retirement text keeps every unresolved item visible. That is the most
   important question in this review.

Report each attack's measured outcome and a verdict line `C2_REVIEW: agree|disagree <reason>`.
Never edit a lane file.
""", MIL_REC),

    item("Mo82C01Contract", "critic", """
Falsify the round's frozen contract before the L1 measures anything. One verdict per item, with
reasons and, where you can, a measured attempt in scratch.

Read `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/contract.md`.

1. **Do-nothing reachability.** Could a round that changes nothing pass P-C1, P-C2 or P-C3?
   Try the cheapest cheats: a stub counter that prints the target line; a `count-c1.py` copy that
   hardcodes `killed=11`; a classification file that copies the token list and labels every token
   `added-since-r10`; a `record-pins.json` with one binding; a `REVISION_MISMATCH` string pasted
   into the tool without an arm. Report each attempt's result against the real counters.
2. **Over-broad arms.** Does any predicate accept a shape a broken instrument also meets? In
   particular: P-C1's `killed=11 total=11` when the harness's own anchors are absent; P-C2's
   agreement when the derivation table collapses to one class; P-C3's `defeated=1` when the
   fixture is graded by the same code under test.
3. **Claim sizing (§9).** Is each after-state one concrete value re-derivable with one command
   over committed bytes? Name any universal clause, any target a do-nothing control could reach,
   and any predicate that cannot be re-derived by a non-author.
4. **Axis assignment.** C1 operability, C2 freshness, C3 depth — is each claim on a distinct axis,
   is at least one on the lowest non-retired axis, and is any axis harmed? (depth/freshness/
   calibration are tied at 5.)
5. **C2's honesty.** Does retiring the r10 pin conflict with the round-21 correction that kept the
   r20 baseline "invalid for acceptance"? Quote the contract text that resolves or fails to
   resolve it.

Report `CONTRACT_CRITIC: pass|defect <n>` with the defect list and, per defect, the exact fix
sentence you would freeze. Do not edit the contract.
""", MIL_REC),

    item("Mo82M01Mutants", "mutation-tester", """
Independent mutation test of the round-82 build. Report only; never edit a lane file — every
mutant is a scratch copy under `/fast/scratch/hyaku/mori-r82/Mo82M01Mutants`.

Population: the worktree bytes of (a) `tools/mori-record-sweep.py` AFTER the `revision` arm lands
(if it has not landed when you start, mutate the r81 bytes and say so explicitly), (b) the three
counters `.ufo/waves/round-82/count-c{1,2,3}.py`.
For each file define ≥4 single-string mutants that invert a GRADED behaviour (examples for the
revision arm: skip the rev-bytes check; check only the first binding; treat a missing row as
green; resolve `rev` against `--root` instead of `--git`; for the counters: accept a
`fail=0`-free run as green, ignore the pristine arm, accept a stale classification, accept a
green census run as met).
Run each mutated copy's own `--selftest` (and, for record-sweep, a small pins fixture) with a
120 s bound and `TMPDIR` under your scratch. Killed iff rc != 0 or `fail>0`; pristine must be
green first.
Report the table (file · label · old→new · rc · verdict), `MUTANTS killed=K total=T survivors=S`,
and for each survivor the exact missing selftest arm (file:line where it belongs).
""", MIL_REC),

    item("Mo82K01Connector", "connector", """
Sibling-overlap scan for the two new surfaces this round adds.

1. **Revision-precision record gate.** Does any sibling lane already own a gate that binds a
   stated value to a revision (or checks a record's arithmetic against committed bytes)? Search
   the sibling repos under /home/vgpnk/Projects/shokunin/*-shokunin for `pointers=`, `measured
   at`, `REVISION`, `git show`-based gates, and their `tools/`. Report file:line hits and a
   verdict: distinct ground, or overlap that mori must defer to.
2. **Drift-pin retirement.** Does any lane retire a baseline/pin with a classification receipt,
   or keep a permanently-red drift predicate? Check tabi, chousa, kotoba, kumitate, tsukuroi and
   kengaku `PROVINCE.md`/`SCORECARD.md`/`corpus/lessons/` for `drift`, `retire`, `baseline`.
   Report the closest pattern and whether mori should cite it.
3. **Ownership boundary.** mori is detection-and-report only; kumitate owns orchestration
   semantics, tsukuroi the OS, chousa sources, kotoba prompt craft. State, per overlap found,
   which lane owns the decision and what mori may only observe.
4. Read `../kumitate-shokunin/PROVINCE.md` and `../chousa-shokunin/PROVINCE.md` at least, and
   cite line numbers.

Report a three-column table (surface · sibling hit · verdict) and one sentence naming what mori
must NOT claim as a result.
""", MIL_REC),

    item("Mo82R03GitPrimer", "revenger", """
Reverse-engineer the git primitives the revision arm relies on: one bounded, falsifiable probe.

Hypothesis: `git -C <repo> show <rev>:<path>` alone is a sufficient, unambiguous primitive for the
revision arm's four failure modes — row-value, rev-unresolvable, path-absent, rev-bytes — and its
exit codes distinguish them without parsing stderr.

Probe (all read-only, in a scratch fixture repo you create with `mktemp -d` under
`/fast/scratch/hyaku/mori-r82/Mo82L01SourceProbe`; verify `git -C "$D" rev-parse
--show-toplevel` equals `$D` before the first commit):
1. unresolvable rev: `git rev-parse --verify deadbeef^{commit}` → rc and stderr shape;
2. path absent at a valid rev: `git show <rev>:nope.md` → rc and stderr shape;
3. a path that is a directory at the rev: `git show <rev>:tools` → rc and final line;
4. a path with a space, and a rev that is a short 8-hex prefix, and a rev expressed as
   `<branch>~1`: do they resolve as expected?
5. `git cat-file -e <rev>:<path>` rc for present vs absent.
Then state whether the arm can rely on rc alone or must distinguish stderr text — and which
choice is robust to locale (`LC_ALL=C`) and to a repo with a different default branch.

Report the exact commands, rc values and the one-line conclusion. Change no lane file.
""", MIL_REC),
]

SPEC = {
    "wave": "mori-r82-w1",
    "milestone": ("Round 82 w1: build, record and first falsifiers for C1 (committed mutation "
                  "harness), C2 (drift-pin retirement with derived classification) and C3 "
                  "(revision-precision arm); counters frozen in 20551e56."),
    "axes": ["operability", "freshness", "depth", "coverage", "calibration", "adjacency"],
    "reportDir": ".ufo/waves/round-82/w1",
    "maxLanes": len(ITEMS),
    "context": CONTEXT,
    "items": ITEMS,
}

out = os.path.join(ROUND, "w1-spec.json")
os.makedirs(os.path.join(ROUND, "w1"), exist_ok=True)
with open(out, "w", encoding="utf-8") as handle:
    json.dump(SPEC, handle, indent=1)
print(out, len(ITEMS), "items")
for entry in ITEMS:
    print(" ", entry["name"], entry["role"], len(entry["prompt"]))
