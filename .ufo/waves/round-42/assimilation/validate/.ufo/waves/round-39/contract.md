# mori round 39 — frozen contract (L1 mori-r39, attempt 1)

Entering tip: `13f3db7e5c7163e7ef300259ff597a42a79f81f1` (round 38 admitted;
closure `corpus/lessons/round-38-verifier-spotcheck.md`).
Frozen before any data seat or data receipt: this contract, `count-c7.py`,
`conform.py` (round-39 version), the modified `tools/mori-sources-appendonly.py`
(the tracked gate, version 2), the fixture builders and the fabricated-witness
payloads. Pins are recorded in `evidence/freeze-r39.txt` (sha256 over the frozen
paths). A change to a predicate after this freeze is a new counter version, not an
edit. The round-38 instruments under `.ufo/waves/round-38/` stay byte-frozen; their
receipts remain valid at their frozen commits.

## Routed inputs this round discharges (r38 closure + lesson)

- M18 residuals (C4 fabricated-content bypasses): one-char anchors satisfy
  `check_anchors`; comment-parked or dead-code anchors pass; a constant-classifier
  probe passes `drift_kill` (symmetric substring check); the fully fabricated
  self-consistent clone prints `C4=met`. → claim C1.
- M19 residuals (conform timeout name-not-value): `communicate(timeout=NAME)` with
  `NAME = None` passes `bounded_reads`; `wait(timeout=…)` + `stdout.read()` drain
  passes; the shipped selftest never exercises the communicate-timeout conjunct.
  → claim C2.
- Gate ancestry F1/F2 (resid/ResidGateTiming): `superseded_as_of` uses path-log
  index order, not ancestry; edit detection compares adjacent walk records, not
  parents. → claim C3.
- S226 anchor suffix `:657-658` → `:657-659`: fixed by a new superseding row S228
  (the `anchor` cell is immutable; an in-place edit would be a gate violation).
- r38 fleet report cites `gate-after-e37dcc6.txt:2` (value at line 22): the report
  is committed fleet history, outside lane write scope; the correction is recorded
  in this round's LOG entry, lesson and report.

## Claims

### C1 — calibration (5, tied lowest): fabricated-content discrimination v2 (r38 M18)

Round 38's P-C4 checks are presence checks: any non-empty substring anchor passes,
a capability path resolving to a directory passes, and `drift_kill` passes when the
mutated run's output merely contains both state strings somewhere (a symmetric
substring test a constant-classifier probe satisfies). This round lands the content
checks a fabrication must actually do the work to satisfy.

**P-C7 (frozen, verbatim in `count-c7.py`'s PREDICATE and in the report):**

> P-C7: at revision R, the committed drift-corpus binding passes five content checks that the round-38 checks could not discriminate — every `anchor:` line in the knowledge entry is a string of eight or more characters that occurs byte-exactly in tools/mori-source-drift.py at R at a position that is not inside a comment; every path the SCORECARD capability row cites resolves at R to a committed file, not a directory; the live receipt names one drifted row per drifted row its summary counts and every named id has a committed source copy at R; and the probe's selftest named-row arm `row_states` is killed by its own mutation, detected as a structural per-row state difference between the honest and mutated runs whose expected post-mutation state is drawn at run time — and the same counter rejects four fabricated witnesses (an entry carrying tokens with no resolvable anchor, a capability row citing a nonexistent path, a live receipt with only the summary sentence, a self-consistent clone whose anchors are parked inside comments) while the real bytes pass.

Counter: `.ufo/waves/round-39/count-c7.py <rev>`. Exit 0 met, 1 unmet, 2 setup error.
Checks: `anchors_v2` (≥3 anchors, unique, each ≥8 chars, each occurring at a
non-comment position in the tool bytes at R), `capability_v2` (every cited path
resolves and `git cat-file -t` is `blob`), `live_rows_v2` (one `S### drifted` line
per summary count, ids in the registry, each named id has a committed copy under
`corpus/evidence/sources-r<N>/` at R), `named_row_drift` (as r38) and `drift_kill_v2`
(honest and mutated selftest `row_states` tables parsed structurally; the tables must
be identical except that the rows drifted in the honest table read exactly the
run-time-drawn state in the mutated table; the drawn state is one of
excerpt/fresh/unavailable/no-copy chosen by a run-time seed and printed in the
receipt, so a probe hard-coding the expected flip string cannot know it in advance).
Negatives: the three r38 witnesses (reused) plus `fixtures/witness-comment-anchors.md`
(an entry whose three anchors are real code strings of the tool but parked inside
comment lines, so the non-comment occurrence fails); each must be rejected.

Disclosed bound (recorded, not hidden): a forgery that copies the real knowledge
entry, the real capability row and the real receipt verbatim is indistinguishable
from the real work under any static check; the run-time-drawn drift arm is the
live-work binding, and the residual static indistinguishability is the same limit
QUALITY 105 records for byte predicates.

**Before** (measured at the entering tip `13f3db7e`, r38 counter bytes taken from
`git show 13f3db7e:.ufo/waves/round-38/count-c4.py`):
`python3 .ufo/waves/round-38/count-c4.py 13f3db7e` → `C4=met` exit 0, and the four
bypass fixtures each pass the r38 check they attack: one-char anchors `#`, `:`, `==`
pass `check_anchors`; a comment-parked anchor entry passes `check_anchors`; a probe
whose selftest prints the expected flip strings passes `drift_kill`; a directory
path passes `capability`. Receipts: `evidence/c7-red-*.txt`.
The same r38 counter prints `C4=met` on the fabricated self-consistent clone
(re-derived: `evidence/c7-red-clone.txt`).
**After** (declared): `python3 .ufo/waves/round-39/count-c7.py <landed tip>` → all
five checks PASS, four negatives rejected, `C7=met` exit 0.

Kill rule: a do-nothing control cannot print `C7=met`; a counter that only adds the
anchor length floor still accepts the comment-parked clone and the
constant-classifier probe → `C7=unmet`; a docs-only control fails
`named_row_drift`/`drift_kill_v2`.

### C2 — operability (7): conformance timeout name-and-value, drain shape (r38 M19)

Round 38's `bounded_reads` requires only the keyword name `timeout` on a
`communicate(` call, never its value, and never the drain's shape. Two real hangs
pass: `communicate(timeout=UNBOUNDED_DRAIN_S)` with `UNBOUNDED_DRAIN_S = None`, and
`proc.wait(timeout=…)` with the drain as `proc.stdout.read()` (both killed by a 45 s
outer timeout in resid/ResidC5Drain, no `C1=` line). This round lands the
conformance checker that reads the value and the shape.

**P-C8 (frozen, verbatim in `conform.py`'s PREDICATE and in the report):**

> P-C8: at revision R, the round-39 conformance checker passes all nine checks on the round-39 counter bytes — the round-38 six (predicate, head_pin, tool_resolve, bounded_reads, timeout_state, scratch) plus `timeout_value` (every `timeout=` keyword in every counter resolves through module-level assignments to a positive numeric literal, so `timeout=NAME` with `NAME = None` fails), `drain_shape` (every `Popen(` in the first counter is drained in its own function by a `communicate(` carrying its own timeout, so a `wait(timeout=…)` plus `stdout.read()` drain fails), and `selftest_conjunct` (the shipped `--selftest`'s bounded_reads mutation exercises the communicate-timeout conjunct) — and each of nine textual mutations flips exactly its own check to FAIL.

Counter: `.ufo/waves/round-39/conform.py <rev> [--counter PATH]… [--selftest]`.
The first `--counter` of record is `.ufo/waves/round-39/count-c7.py` (the r39
instrument; the r38 counters remain scored by the r38 checker, whose pins stay
frozen at their commits).

**Before** (measured at the entering tip):
`python3 .ufo/waves/round-38/conform.py 13f3db7e --counter <bypass A> --counter <bypass B>`
→ `CONFORM=met` exit 0 on both bypass fixtures built from the r38 count-c1 bytes
(`fixtures/make-m19-bypass.py`; receipts `evidence/c8-red-none.txt`,
`evidence/c8-red-wait.txt`), and `evidence/m19-selftest-gap.txt` shows the r38
selftest's bounded_reads mutation leaves the communicate-timeout conjunct
unexercised (the mutated counter still passes `bounded_reads` even with the
conjunct deleted).
**After** (declared): the round-39 checker prints `CONFORM=met` exit 0 on the honest
r39 counter and `CONFORM=unmet` on each bypass fixture, and
`CONFORM_SELFTEST pass=9 fail=0` with each mutation flipping exactly its own check.

Kill rule: a do-nothing control cannot print `CONFORM=met`; a checker that only
constant-folds the value still accepts the `wait`+`read` drain → `CONFORM=unmet`;
a checker whose selftest never mutates the communicate-timeout conjunct fails
`selftest_conjunct`.

### C3 — depth (5, tied lowest): ancestry-based supersede disposition (r38 F1/F2)

Round 38's `supersede_timing` implements "descendant" as path-log index order and
detects edits by comparing adjacent walk records, not parents (resid/ResidGateTiming
F1 HIGH / F2 MEDIUM): on a history with a side-branch superseder the gate reports
as-of for a disposition that never descends from the edit, and on a diamond it
fabricates edits and reversions at the merge. Lane history is linear, so no r38
receipt is falsified; the predicate's words are not what the code checks. This
round makes the gate compute what P-C6 says.

**P-C9 (frozen, verbatim in the gate's PREDICATE and in the report):**

> P-C9: at revision R, tools/mori-sources-appendonly.py reports, after its summary line, `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; an id is superseded-as-of only when its latest superseding row's landing commit is a descendant, by `git merge-base --is-ancestor`, of the commit of the id's last immutable-cell edit, where an edit at a commit is a change against its first parent's state (not the previous walk record), the path walk uses `--full-history`, and the lane-history verdicts are unchanged — S069 is stale at `e37dcc6` and no id is stale at the round-39 tip — and the selftest carries committed fixtures for a side-branch superseder (stale, not as-of) and a merge that must not fabricate an edit (round-38 gate bytes print as-of and a fabricated edit there; the round-39 gate prints stale and no edit).

Gate: `tracked tools/mori-sources-appendonly.py`, version 2. The output format
(per-id lines, `appendonly_violations` summary, `supersede_timing` line) is
byte-identical in shape to v1; on linear histories v1 and v2 agree, which the
receipts show by re-running both byte sets on the lane history.

**Before** (do-nothing control, measured on committed fixture DAGs built by
`fixtures/make-ancestry-dags.py`): the round-38 gate bytes (from
`git show 13f3db7e:tools/mori-sources-appendonly.py`) print `superseded_as_of=[S001]`
for a superseder that never descends from the edit (fixture A) and flag a
fabricated edit + reversion across a merge (fixture C); receipts
`evidence/c9-red-a.txt`, `evidence/c9-red-c.txt`. At the entering tip the gate has
no ancestry primitive (the only git verbs are rev-parse, log, show).
**After** (declared): the round-39 gate prints `stale_supersede=[S001]` on fixture A,
no fabricated edit on fixture C, `MORI_SOURCES_APPENDONLY_SELFTEST pass=11 fail=0`,
and on the lane history byte-identical per-id/summary lines to the round-38 gate
plus `supersede_timing superseded_as_of=[18 ids + S226 once S228 lands] stale_supersede=[]`
at the landed tip.

Kill rule: a do-nothing control cannot print the fixture verdicts; a gate that
keeps index-order timing lists S001 as-of on fixture A → the frozen fixture fails;
a gate whose edit detection still compares adjacent records fabricates the fixture C
edit → the frozen fixture fails.

## P-C7/P-C8/P-C9 evidence paths

`evidence/freeze-r39.txt`, `evidence/c7-red-anchors.txt`, `c7-red-comment.txt`,
`c7-red-classifier.txt`, `c7-red-clone.txt`, `c7-before.txt`, `c7-after.txt`,
`evidence/c8-red-none.txt`, `c8-red-wait.txt`, `m19-selftest-gap.txt`,
`c8-before.txt`, `c8-after.txt`, `c8-after-selftest.txt`,
`evidence/c9-red-a.txt`, `c9-red-c.txt`, `c9-before-lane.txt`, `c9-after-fixture-a.txt`,
`c9-after-fixture-c.txt`, `c9-after-lane.txt`, `gate-selftest-after.txt`,
`census-start.txt`, `census-end.txt`.

## Claim-admission hygiene (r38 lesson)

Targets are one command over committed bytes each; no universal clauses; the
before receipts are recorded before any data seat runs; the do-nothing control for
each claim is the round-38 instrument bytes on the round-39 fixtures (it prints
`met` where the round-39 counter must print `unmet`).
