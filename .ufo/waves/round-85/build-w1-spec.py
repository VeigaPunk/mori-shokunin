#!/usr/bin/env python3
"""Build mori round-85 wave w1 spec (one v1 wave, 12 seats, band 8-16).

Writes .ufo/waves/round-85/w1-spec.json. The Godspeed directive bytes are copied verbatim from
the round-84 spec (the host binding), never retyped.
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
R84 = LANE + "/.ufo/waves/round-84/w1-spec.json"
FREEZE = "ab2608655ea52ba6d151b3a31d69a3b18cd2b41e"
ENTERING = "2cc4b1ae35a83e4fd3fc48bae842bdf38df2e80e"

with open(R84, encoding="utf-8") as handle:
    r84 = json.load(handle)
GODSPEED = r84["context"].split("\n\n# Goal", 1)[0]
assert GODSPEED.startswith("/skill:godspeed"), GODSPEED[:40]

CONTEXT = GODSPEED + """

# Goal
mori round 85 (attempt 1), wave w1 — land, record and first-falsify THREE frozen claims.
mori is a fleet/host observability lane: detection and report only. The freeze commit is
`%(freeze)s`; the three counters were frozen there before any seat ran. The entering revision is
`%(entering)s`.

Read first, in this order (absolute paths):
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/contract.md — THE FROZEN
  AUTHORITY: P-C1 (the two surviving r84-counter mutants and their arms), P-C2 (the receipt
  provenance grammar), P-C3 (the counter's own census observation), the targets, the kill rules and
  the measured do-nothing controls.
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/count-c1.py, count-c2.py,
  count-c3.py — the three frozen counters (each has `--selftest`).
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/evidence/controls-r85.txt — the
  measured entering, population and defeat controls.
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/w1/Mo84R01C1.md §4-§5 — the
  acceptance bar and the X1/X2 extra-mutant sweep this round's C1 population comes from.
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/w1/Mo84R03Record.md §0 — the
  executing-counter-bytes gap this round's C2 claim closes.
- /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-84-verifier-spotcheck.md
  (`## Routed defects the lane must fix next round`: D84-1 attribution, D84-2 stale QUALITY 172
  tally + pointer, D84-3 missing rejected SOURCES row, D84-4 uncommitted sweep receipts, D84-5
  battery receipt header).
- /home/vgpnk/Projects/shokunin/mori-shokunin/SCORECARD.md `## Planned (round 85)`.

# Round claims (frozen before this wave; do not change them)
- C1 operability (7): the r84 C1 counter gets the failing arm each of its two surviving mutants
  (X1 `if not k and coupling is not None:` → `if coupling is not None:`; X2
  `coupled = all(base.count(marker) == 1 for marker in coupling)` → `>= 1`) needs, taking its
  selftest 15 → 17 arms. Target `C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met`.
  Entering: `C1=unmet mutants=2 killed=0 survivors=2 total=2 arms=15 harness=stub ...`.
- C2 calibration (5, tied lowest): every after receipt binds its command, its graded revision and
  the sha256 of the subject bytes at that revision. Target `C2=met receipts=3 bindings=5 bound=5
  revs=3 limits=3 cmd=3 summary=3 mismatch=0`. Entering: `C2=unmet receipts=0 harness=absent`.
- C3 depth (5, tied lowest, capability acquisition): the counter runs the census itself (three
  observations from R's own bytes) and reconciles the r83 subject's live reading with its own.
  Target `C3=met observed=3 aa=stable own_tokens=N subject_tokens=N unmatched=0 unnamed=0`.
  Entering: `C3=unmet observed=absent harness=absent` (the counter does not exist there).

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
- Scratch: create your work dir under /fast/scratch/hyaku/mori-r85/<your seat name>/ and delete it
  before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell). Never write under /tmp; a /tmp path is
  never citable evidence. Use `git clone --shared` instead of full clones; never mirror the whole
  lane. `HYAKU_SCRATCH` defaults to /fast/scratch/hyaku.
- Fixture git repos: `D=$(mktemp -d)` then `git -C "$D" init -q`; assert
  `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit; every later
  git/jj call names `-C "$D"`.
- Detection and report only: no lane, OS, unit, service, credential, harness or orchestration
  state may be changed. mori never remediates. Do not run `agent://all`; message only the L1
  (agent id `MoriR85`) for a blocker.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the
  task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate) and
  record tool/version/channel/reason in your report. **pacman guard (orchestrator ruling
  2026-10-20): all pacman transactions are PAUSED host-wide** — install via `uv tool`/`npx`/an
  official binary in `~/.local/bin`, or file nothing; never `-Sy`, `-Syu`, `-U`, `-R`, never a
  partial upgrade.
- Honesty: an unrun check has not passed. Report failures, dead ends and surviving defects plainly;
  never restate a sibling's claim as your own measurement.
"""


def item(name, role, axes, milestone, prompt):
    return {"name": name, "role": role, "axes": axes, "milestone": milestone,
            "prompt": prompt}


ITEMS = [
    item("Mo85E01C1Arms", "executor", ["operability"],
         "round 85 w1: the two failing arms for X1/X2",
         """
Give `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c1.py` the two
failing selftest arms the round-85 C1 counter requires.

Frozen authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/contract.md`
P-C1, and the counter `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/count-c1.py`.

File you may edit: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c1.py`,
`selfcheck()` only. Do not touch `grade()`, `green()`, `killed()`, `MUTANTS`, `EQUIVALENT`, any
other file, or the two mutated lines: `if not k and coupling is not None:` and
`coupled = all(base.count(marker) == 1 for marker in coupling)` must still occur exactly once.

Arms to add (labels frozen; total 15 -> 17). Insert them before the `target_split_ok` arm:
1. `killed_mutant_with_coupling_not_equivalent` — write a fixture `tools/killed_coupled.py` whose
   body contains `GUARD = 1`, the three M24d coupling markers each exactly once
   (`agreed == len(snapshot_tokens)`, `residual += duplicates`, `duplicates == 0`) and a
   `print('FAKE pass=%d fail=%d' ...)`/`raise SystemExit(...)` pair keyed on `GUARD == 1`; grade
   `("tools/killed_coupled.py", "M24d_met_residual", "GUARD = 1", "GUARD = 0")`. Assert the grade
   is met, the tail carries `equivalent=0`, and one line carries ` killed `.
2. `duplicate_coupling_not_equivalent` — write a fixture `tools/dup_coupling.py` whose body
   contains the same three markers but the `agreed == len(snapshot_tokens)` marker twice, and a
   `print('FAKE pass=1 fail=0')` line not keyed on GUARD (so the mutation
   `("GUARD = 1", "GUARD = 0")` is non-killing). Grade with label `M24d_met_residual`. Assert the
   grade is NOT met, a `coupling-absent` extra is present, and the tail carries `survivors=1`.

Acceptance (prove it in your own scratch dir, quote the commands and outputs):
- pristine `python3 -I <copy> --selftest --scratch <dir>` -> `C1_COUNTER_SELFTEST pass=17 fail=0`,
  rc 0.
- the X1 mutant (`if coupling is not None:`) -> `pass=16 fail=1`, rc 1, and the FAIL line is
  `killed_mutant_with_coupling_not_equivalent`.
- the X2 mutant (`coupled = all(base.count(marker) >= 1 ...`) -> `pass=16 fail=1`, rc 1, and the
  FAIL line is `duplicate_coupling_not_equivalent`.
- report `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --numstat --
  .ufo/waves/round-84/count-c1.py` (additions expected: the two arms only).
- the r84 counter's own frozen target must still be reachable: copy the armed counter into scratch,
  seed the r83 counters and run its grade path (or `python3 -I <copy> <freeze-rev> --repo
  /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <dir>`) and report whether it prints
  `C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4`.

If an arm fails on the pristine counter, stop and report that instead of weakening the assertion.
"""),
    item("Mo85E02Receipts", "executor", ["calibration"],
         "round 85 w1: the receipt generator and its provenance grammar",
         """
Write `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/make-receipts.sh` — the
generator that produces the three receipts frozen by P-C2 of
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/contract.md`.

Usage: `make-receipts.sh <rev> [--repo DIR]`, run from the lane root. It writes exactly:
- `.ufo/waves/round-85/evidence/after-r85.txt` — the C1 and C3 counters run at `<rev>`, with
  `# counter-sha256:` lines for `.ufo/waves/round-85/count-c1.py`, `count-c2.py` and `count-c3.py`
  (the sha256 of each file's bytes at `<rev>`), and a body that contains `C1=met` and `C3=met`.
- `.ufo/waves/round-85/evidence/record-sweep-r85.txt` — `python3 -I tools/mori-record-sweep.py
  --root . --pins .ufo/waves/round-82/record-pins.json` run in the lane worktree, body token
  `RECORD_SWEEP`, binding `tools/mori-record-sweep.py` at `<rev>`.
- `.ufo/waves/round-85/evidence/claim-sweep-r85.txt` — `python3 -I tools/mori-claim-sweep.py
  --root . --pins .ufo/waves/round-80/claim-pins.json`, body token `CLAIM_SWEEP`, binding
  `tools/mori-claim-sweep.py` at `<rev>`.

Every receipt's header block (before the single `# ---` line) is exactly:
```
# receipt: <name>
# cmd: <the exact command line that produced the body, run from the lane root>
# rev: <full 40-hex revision>
# counter-sha256: <64-hex sha256 of the path's bytes at <rev>> <repo-relative path>
# limits: <one sentence naming the predicate's limit for this receipt>
# ---
```
One `# cmd:`, one `# rev:`, one `# limits:` each; `# limits:` must contain the word `limit` and at
least three words. The `after-r85` receipt's limit sentence must state that the C1/C3 bodies are
counter runs at the named revision while the two sweep bodies are worktree runs pinned to the same
bytes by the binding. Do not invent a revision: take it from argv and verify with
`git -C <repo> rev-parse <rev>^{commit}`.

Proof in scratch (quote commands and outputs):
1. Generate all three receipts at the freeze revision
   `ab2608655ea52ba6d151b3a31d69a3b18cd2b41e` into a scratch copy of the evidence dir (do NOT
   write the real receipts with that revision; the L1 regenerates them at the measured revision).
2. `python3 -I .ufo/waves/round-85/count-c2.py --selftest` -> `C2_COUNTER_SELFTEST pass=15 fail=0`.
3. Defeat proof: in a scratch clone of the lane at that revision, commit the generated receipts and
   run `python3 -I .ufo/waves/round-85/count-c2.py HEAD`; it must print a `RECEIPT` line per
   receipt. Then corrupt ONE `# counter-sha256:` hex digit, commit, re-run: it must print
   `C2=unmet ... bound=4 mismatch=1`, rc 1.
4. State plainly whether your generated header block parses under the frozen counter
   (`parse_receipt`) and paste the counter's `RECEIPT` lines.

Never edit the three counters or the contract; if the grammar as frozen is unreachable, report the
exact mismatch instead of changing it.
"""),
    item("Mo85E03C3Fixture", "executor", ["depth"],
         "round 85 w1: prove the C3 observation is load-bearing",
         """
Prove that the round-85 C3 counter's own census observation is load-bearing, using only fixture
git repos under your scratch dir.

Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/contract.md` P-C3 and
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/count-c3.py`.

Build two fixtures, each `D=$(mktemp -d)`, `git -C "$D" init -q`, asserted toplevel, committed
with `-c user.name=t -c user.email=t@t`, containing the five paths the counter reads
(`tools/mori-census.sh`, `corpus/evidence/baseline-r10-20261015T2231Z.json`,
`corpus/evidence/drift-classification-r82.txt`,
`.ufo/waves/round-82/evidence/drift-r82-live.txt`, `.ufo/waves/round-83/count-c2.py` copied
byte-exact from the lane):

1. **census-stub** — `tools/mori-census.sh` replaced by `#!/bin/sh` + `exit 1` (no `MORI_DRIFT:`
   line). Expected: `python3 -I <lane>/count-c3.py HEAD --repo "$D" --fleet-root "$D"` prints
   `C3=unmet` with `own_tokens=0` (the three observations are empty/unstable), rc 1.
2. **subject-live-stale** — a real-looking census stub is too expensive; instead take the same
   fixture and a subject copy whose `live_tokens` is decremented by one (edit the copied r83
   subject so `live_tokens=%d` prints `len(live_tokens) - 1`). Keep the census stub out (use the
   lane's real census bytes at the entering revision): expected `C3=unmet` with
   `subject_tokens != own_tokens`, rc 1.

Report in your seat report: the exact fixture construction, the commands, the counter's full
summary lines and rc for each fixture, and which clause of the frozen predicate each control
falsifies. Also state the negative result honestly if a control reads `met` (that would mean the
clause is not load-bearing; say so).

Write only `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/evidence/c3-controls.txt`
and your report; never edit the counter, the subject or the lane history.
"""),
    item("Mo85E04Controls", "executor", ["operability"],
         "round 85 w1: the defeat controls and the battery receipt header",
         """
Two deliverables, both under
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/evidence/`:

1. `controls-r85-defeated.txt` — the three defeat controls of the frozen contract, each run for
   real, each with its command, full output and `rc=` line:
   - C1: run `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/count-c1.py
     <freeze-rev>` (`ab2608655ea52ba6d151b3a31d69a3b18cd2b41e`) and show the `harness=stub` unmet
     line rc 1; then, in scratch, a copy of the r84 counter with BOTH new arms removed must be
     graded by the r85 counter as unmet (arms=15), while the armed copy in the lane worktree reads
     `arms=17` once a sibling lands the arms — if the arms are not yet landed when you run, say so
     and record the pre-arm reading only.
   - C2: build a receipt with a corrupted `# counter-sha256:` (flip one hex digit) in a scratch
     clone, commit it, and show `C2=unmet ... bound=4 mismatch=1` rc 1; also a receipt with no
     header block shows `C2=unmet ... mismatch>=1`.
   - C3: paste the census-stub fixture line from
     `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/evidence/controls-r85.txt`
     (already measured: `C3=unmet observed=3 aa=unstable own_tokens=0 rcs=1,1,1` rc 1) and
     re-derive it yourself on a fresh fixture; do not cite the sibling file as your own run.
2. `battery-r85.txt` — the standing battery with a header (D84-5): first line
   `# battery run at rev=<40-hex worktree revision> date=<ISO-8601>`, then the output of the
   lane's standing battery. Read
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/evidence/battery-r84.txt` to
   find the exact battery command and rerun the same one from the lane root; report
   `BATTERY pass=N setup=N fail=N` and rc. Do not change any tool, test or fixture that the
   battery exercises; if a battery case fails, report it, do not fix it.

Detection only: no lane write outside these two receipt files and your report.
"""),
    item("Mo85Sc01Source", "scout", ["depth", "freshness"],
         "round 85 w1: open and pin the round's source",
         """
Open and pin the round's source for the C2 claim, under
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r85/`.

Question: what source states that reproducibility of an artifact is verified by comparing
independently rebuilt bytes (so a receipt that binds command + revision + subject-bytes digest is a
verification artifact, not an assertion)?

1. Fetch `https://reproducible-builds.org/docs/definition/` three times into
   `corpus/evidence/sources-r85/rb-definition-{1,2,3}.html` (plain `curl -sS -o`, no redirect).
   Record HTTP status, byte size, line count and `sha256sum` for each; require all three
   byte-identical. Record the page's `etag`/`last-modified` if present (a `curl -sSI` head is fine).
2. Locate the sentence on builds being reproducible when the same source/build instructions let any
   party recreate bit-identical copies, and the sentence on verification by bit-by-bit comparison
   with cryptographically secure hash functions. Record the RAW line numbers in the pinned copy
   and a verbatim quote of **at most 25 words** for the row.
3. Screen two more candidate sources for the same question (e.g. Debian's reproducible-builds wiki
   page and one other) — fetch, name the URL, say included or excluded, and give the reason. Stop
   rationale required (identified / screened / included / excluded counts).
4. Append the access log to `corpus/SOURCES.md`? **No** — do not edit `corpus/SOURCES.md`; the
   scribe seat Mo85S01Lesson owns the registry rows. Return in your report: the exact row you
   recommend (11 cells: id placeholder `S600`, source, kind, tier, scope, anchor, teaches, status
   `mined`, opened `2026-11-04`, recheck, used-by
   `corpus/knowledge/receipt-provenance-r85.md`), the located quote, and the three fetch digests.

Also report whether `https://arxiv.org/abs/2404.09241` (the r84 rejected candidate) is still
reachable and whether its abstract states any bias/cost statement that would flip the r84 rejection
(quote it if so, otherwise say `no flip`).
"""),
    item("Mo85S01Lesson", "scribe", ["freshness", "calibration"],
         "round 85 w1: the lesson, the registry rows and the Gate",
         """
Write `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-85.md` and append the
round's rows to `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`.

Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md` section *SOURCES.md — where a shokunin learns*
(census schema: 11 cells, `status` in `mined|queued|rejected|...`, `recheck` an ISO date / `NNd` /
`on-release`, `used-by` repo-relative paths, no literal or escaped `|` in a cell).

1. **Registry rows** (append-only; keep every existing line byte-identical):
   - `S600` — the reproducible-builds definition page opened this round; use the scout seat's
     pinned copy and quote if it is in `corpus/evidence/sources-r85/`, otherwise open
     `https://reproducible-builds.org/docs/definition/` yourself and pin it. One located quote of
     at most 25 words with raw line numbers in the pinned copy; `status mined`; `opened
     2026-11-04`; `used-by corpus/knowledge/receipt-provenance-r85.md` (create that knowledge file
     with K1–K3: the definition, the verification-by-hash rule, and this lane's receipt grammar;
     cite `S600`).
   - `S601` — `arXiv:2404.09241` as a **rejected** row (D84-3): the r84 refusal left no row; give
     the URL, the abstract's equivalence definition and its weaker cost statement, `status
     rejected`, and in the lesson's Gate block the reason + flip condition. Do not claim to have
     re-opened it unless you did.
2. **`## Mistakes`** — mine one mistake from this round or an earlier one: class · evidence pointer ·
   captured-by (the criterion or rule that should have caught it, or `none`) · fix. Candidate: the
   r84 D84-2 stale QUALITY tally (a pre-amendment selftest count quoted as the measured tally).
   Show the sweep command and output that would have caught it.
3. **`## Gate`** — for every new row: URL, access date, ≤25-word located quote. Include ≥1 admit
   (S600) and ≥1 reject (S601). Note `Assimilation: none` (no `merge/mori/` adoption this round).
4. **Census** — run
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
   before your append (record the entering rows count and rc) and after (record rows count and rc);
   paste both outputs' summary lines and exit codes into the lesson. Exit 0 is required after.

Counts to report: rows before (372), rows after, W-tier warnings. Do not touch `corpus/QUALITY.md`,
`SKILL.md`, `SCORECARD.md` or any counter; the other scribe seat owns QUALITY/SKILL.
"""),
    item("Mo85S02Quality", "scribe", ["operability", "calibration"],
         "round 85 w1: QUALITY criteria and the SKILL registry row",
         """
Append to `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/QUALITY.md` and
`/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md`; never rewrite an existing line.

1. **QUALITY 173** — supersede the r84 D84-2 defect: criterion 172 says the r84 `count-c1.py`
   "measured tally is `C1_COUNTER_SELFTEST pass=11 fail=0`", but the counter has carried **15**
   arms since `5a231ef8` and its `:296-300` pointer now lands on argument parsing. Add a criterion
   that a quoted tally is re-run at the cited bytes before it enters a criterion, and that a
   pointer is re-located (`grep -n`) at write time. Show it able to fail against the r84 text.
2. **QUALITY 174** — a mutation-testing counter's arm must fail on the pristine counter when the
   arm's fixture is wrong: every new arm is run against the UNARMED subject first and must read
   red there only when its own fixture is defective (the A4/Sc02 D3 class); a fixture that fails
   the pristine counter is not a kill.
3. **QUALITY 175** — a receipt that binds a revision and a digest must state its own limit where
   the reader meets the number (D84-4/D82-2 class): a `# limits:` line is part of the receipt, not
   a report footnote.
4. **SKILL.md registry** — append ONE new row (row 19) to the Windows-instrument registry section
   (follow row 18's shape at the file end; keep every earlier line byte-identical, including the
   `SKILL.md:905` tally pin). The row names the three r85 counters, their selftests
   (`C1_COUNTER_SELFTEST`, `C2_COUNTER_SELFTEST`, `C3_COUNTER_SELFTEST`), the receipt generator
   `make-receipts.sh`, and the fact that they read `.ufo/waves/round-85/`.

Report the arm counts you cite by RUNNING each `--selftest` from the lane root and pasting the
outputs (the r85 counters currently read pass=18/15/19; re-run them, do not copy). Never edit the
counters, the contract or `SCORECARD.md`.
"""),
    item("Mo85R01C1", "reviewer", ["operability"],
         "round 85 w1: attack the C1 arms and the kill rule",
         """
Adversarial review of round-85 C1. You may read everything and write only your report.

Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/contract.md` P-C1,
`count-c1.py`, `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/w1/Mo84R01C1.md`
§4-§5, and the armed subject `.ufo/waves/round-84/count-c1.py` in the worktree.

Attack list (each item names what it attacks):
1. Anchor exactness at the freeze and at the worktree: `grep -c -F` both anchors; a duplicate or a
   vanished anchor means the counter reads `unanchored` — verify it does.
2. Fake kills: construct, in scratch, at least two arm variants that PASS on the pristine counter
   but do not kill their mutant (a label assertion, a tautology, an arm that never calls `grade()`)
   and show the r85 counter's own detector does not depend on them; then show the real arms kill
   X1/X2 behaviourally (mutated copy's own selftest `pass=16 fail=1`, and the FAIL line names the
   arm).
3. Pristine-first: a fixture that makes the PRISTINE r84 counter red must make the claim unmet
   (build one in scratch and grade it).
4. Target identity: does `C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met` require
   exactly what the contract's sentence says? Name any conjunct that the code enforces less
   strictly (the r84 F4 class) or more.
5. No-harm: does the armed r84 counter still reach its own frozen 4-mutant target at the freeze
   revision? Run it and quote the line.

Verdict per item: **accept** / **reject with reason**. Also state what you would accept the arms
having landed (the five-point bar in Mo84R01C1 §4, restated for X1/X2). Never edit a lane file.
"""),
    item("Mo85R02C2", "reviewer", ["calibration"],
         "round 85 w1: attack the receipt grammar",
         """
Adversarial review of round-85 C2. Read-only.

Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/contract.md` P-C2 and
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/count-c2.py`.

Attack list (name what each attacks):
1. Forgeability: build receipts in a scratch lane clone that pass all five checks but whose body
   is NOT the quoted command's output (e.g. the right `# cmd:`/`# rev:`/sha headers with a
   `C1=met` token pasted in). If they pass, say exactly which clause is missing and whether the
   frozen predicate claims otherwise.
2. Ancestor logic: a receipt whose `# rev:` is a descendant of R, or a sibling branch commit, or
   an abbreviated 39-hex sha — each must read unmet. Build and run them.
3. Path safety: `../x`, `/abs/path`, `a//b`, a path that exists in the worktree but not at the
   named revision — each must read unmet (`unsafe-path` / `absent` / `sha`).
4. Summary token: a receipt whose body carries `C1=met` only inside the header block (before
   `# ---`) must read unmet; one after the separator must read met.
5. The stale-tally hole: a receipt whose sha matches bytes that are themselves stale (the r84
   D84-2 class — a pre-amendment tally quoted with a correct digest) will pass P-C2. Confirm and
   name it as a limit of the predicate in one sentence with a concrete example.
6. Determinism: run the counter twice at the same revision; the summary must be byte-identical.

Verdict per item: accept / reject with the exact line that should change (never change it).
"""),
    item("Mo85C01Critic", "critic", ["calibration", "adjacency"],
         "round 85 w1: falsify the claim set and the mission contract",
         """
Attack the round itself, not its implementation details. Read-only.

Read: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/contract.md`,
`SCORECARD.md ## Planned (round 85)`, `SHONEN.md`, `/home/vgpnk/Projects/shokunin/AXES.md`,
`/home/vgpnk/Projects/shokunin/LEARNING.md`, and the three r85 counters.

Questions, each answered with evidence:
1. **Distinct axes / separability**: C1 (operability), C2 (calibration), C3 (depth) — can each be
   verified without the others' landed bytes? Name any shared byte.
2. **Do-nothing reachability**: for each claim, build the cheapest control in scratch that skips
   the claimed work and score it with the frozen counter. Does it reach the target? (For C3, the
   honest disclosure is that the counter applied retroactively to the entering revision already
   reads met — decide whether that makes C3 a capability acquisition or an empty claim, and say
   which.)
3. **Frozen-before-data**: is there any evidence in the contract, the counters or the evidence
   directory of a target, predicate or class changed after an after-value existed? Check file
   mtimes and the freeze commit `ab260865` against the worktree.
4. **Same-sentence**: does the contract's predicate sentence equal the counter's printed label
   equal the receipt label, for all three claims? List every divergence with line numbers (the
   r84 F1–F5 class).
5. **No-harm**: name any axis the round harms (e.g. does C1's new arms reduce the r84 counter's
   coverage? does C2's grammar make an honest miss look like a defect?).

Deliver a verdict table (claim -> reachable-by-control? same-sentence? harm?) and a list of
required changes before the report may claim admission. Never edit a lane file.
"""),
    item("Mo85M01Mut", "mutation-tester", ["operability", "depth"],
         "round 85 w1: mutation probe of the three r85 counters",
         """
Probe the three round-85 counters for surviving mutants. Detection and report only.

Subjects (byte-exact at the freeze commit `ab2608655ea52ba6d151b3a31d69a3b18cd2b41e`):
`.ufo/waves/round-85/count-c1.py`, `count-c2.py`, `count-c3.py`.

Method:
1. Anchor verification: enumerate every mutation site you use; assert each `old` occurs exactly
   once in the subject before mutating (`occurrences=1`), refuse otherwise.
2. Pristine baseline: each counter's own `--selftest` reads green first.
3. One mutant per scratch copy; run that copy's own `--selftest --scratch <dir>`; kill rule =
   rc != 0 or `fail=<n>` with n > 0.
4. Classify survivors as equivalent (with a coupling/demonstration argument) or non-equivalent
   (with the distinguishing observation). Demonstrate at least three non-equivalent survivors
   end-to-end on a fixture.
5. Aim for coverage of the load-bearing clauses: C1's `killed()/green()/target_split/TAIL_ARMS`
   and the r84-target conjunct; C2's `parse_receipt` boundaries (separator count, safe_path,
   ancestor), binding verification, summary-after-separator; C3's `observe_three` stability rule,
   `reconcile` both directions, `derive` table, subject token equality.

Deliver: `MUTANTS total=N killed=N survivors=N`, per-counter tallies, the survivor table with
class and (for non-equivalent) the observation, and the list of unarmed clauses for the next
round. Write only your report; never edit a counter.
"""),
    item("Mo85K01Conn", "connector", ["adjacency", "coverage"],
         "round 85 w1: sibling-overlap scan and the contract clause sweep",
         """
Two jobs, both read-only except your report.

1. **Sibling-overlap scan**: does any sibling lane already own (a) mutation-arm adjudication /
   equivalent-mutant rules, (b) receipt provenance or hash-bound evidence grammar, (c) census
   re-run reconciliation? Search `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/` and sibling
   `.ufo/waves/round-8*/` for the concepts (grep `mutant`, `receipt`, `sha256` + `rev`,
   `reconcile`, `census`). Name each match with path and one-line scope, say whether it is the
   same surface, an adjacent one, or a contested duplicate, and give mori's adjacency verdict
   (absorb / report / hand off). Do not read or write sibling repos beyond reads.
2. **Contract clause sweep** (the r84 F1-F5 class): compare the round-85 contract's three predicate
   sentences against the three counters' code line by line. For every divergence (a clause the
   prose states and the code does not enforce, or vice versa; a stale anchor; a wrong count),
   quote both sides with line numbers and classify: harmless wording / graded-defect / target
   mismatch. Check at minimum: C1's five conjuncts and the `arms`/`r84` requirements; C2's
   "exactly one `# cmd:`" vs duplicate counts, the `# ---` split, `bindings=5`; C3's `observed=3`,
   `aa=stable`, `own_tokens == subject_tokens`, `unmatched/unnamed` directions.

Deliver a table (divergence -> both quotes -> class) and a one-paragraph adjacency verdict. Never
edit a lane file or a sibling repo.
"""),
]

SPEC = {
    "wave": "mori-r85-w1",
    "milestone": ("Round 85 w1: the two surviving r84-counter mutants, the receipt provenance "
                  "grammar and the counter's own census observation, with first falsifiers; "
                  "counters frozen in ab2608655ea5."),
    "axes": ["coverage", "operability", "depth", "freshness", "calibration", "adjacency"],
    "reportDir": ".ufo/waves/round-85/w1",
    "maxLanes": len(ITEMS),
    "context": CONTEXT % {"freeze": FREEZE, "entering": ENTERING},
    "items": ITEMS,
}

if __name__ == "__main__":
    out = LANE + "/.ufo/waves/round-85/w1-spec.json"
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(SPEC, handle, indent=1)
    print("wrote", out, "items", len(ITEMS))
