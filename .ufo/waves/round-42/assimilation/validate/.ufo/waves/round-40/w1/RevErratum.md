# RevErratum — round-39 erratum: append-only discipline, receipt fidelity, completeness

Axes: **append-only fidelity** (no round-39 byte rewritten; corrections only in the
erratum), **receipt fidelity** (every corrected sentence matches the receipt it cites),
**completeness** (every routed item the round says the erratum carries is actually in it),
**same-identity controls** (the re-claim's before/after run the same fixture under the named
instrument versions), **no-harm** (read-only; only this report written).

Verdict: **PASS on append-only discipline** — no round-39 file was rewritten; the erratum is a
new file at `265a955cc` and is unchanged since. **PASS on the substantive corrections**
(r38 printed unmet on bypass-wait; S227 quote is 17 words; r39 contract `pass=11` is stale and
`fixtures/make-ancestry-dags.py` is a phantom path). The C2 before-control is genuine and I
reproduced both sides. **FAIL on completeness**: the erratum does not carry the P-C7
narrowed-reading correction that the round-40 contract and lesson say it records. Two accuracy
defects (C2 mechanism clause; S227 rationale/duplicate label) and one residual phantom citation
follow.

No tools installed. No production file edited. No lane jj/Git state touched.

## Findings

### HIGH — the erratum is missing the P-C7 correction it is cited for

`.ufo/waves/round-40/contract.md:32-34` says:

> Finding 1 (P-C7 prose "between the honest and mutated runs" exceeds the
> code): narrowed reading recorded in the r39 erratum — the code compares the
> mutant run's got table against the arm's expected (want) table, drawn at run
> time; a wording fix needs no re-freeze.

`corpus/lessons/round-40.md:42-43` repeats it:

> Finding 1 (P-C7 prose) narrowed reading recorded in the same erratum.

The erratum (`corpus/lessons/round-39-erratum.md`, 28 lines, read whole) contains no P-C7
paragraph. `grep -nEi 'P-C7|drift|row_states|honest|mutant|want table|expected'
corpus/lessons/round-39-erratum.md` → no output (rc=1). The erratum has exactly three
paragraphs: C2 bypass-wait/drain re-claim, S227 word count, `pass=11` + `make-ancestry-dags.py`.

Consequence: routed w1/ScoutC7Bounds finding 1 is recorded as discharged via a note that does
not exist; the round-40 report's own erratum bullet lists only three items (S227 label, C2
wording, stale r39 contract citations), so the report and the contract/lesson disagree. The
correction text itself already exists at contract lines 32-34; only the erratum paragraph is
absent. Fix: append that paragraph to the erratum (a round-40 file — the round-39 bytes stay
frozen) or drop the "recorded in the r39 erratum" claim from the contract/lesson.

### MEDIUM — the C2 sentence misnames the r38 failing clause and omits `timeout_state`

Erratum lines 5-9:

> The committed receipt `c8-red-wait.txt` shows the r38 checker printed
> `CONFORM=unmet exit=1` ("not reproduced"): the r38 checker rejected the
> final pure wait+read fixture via its `bounded_reads` popen detection, not
> via drain shape …

The receipt (`.ufo/waves/round-39/evidence/c8-red-wait.txt`) prints **two** failing checks:

```
check bounded_reads    FAIL (bypass-wait.py: run=True popen=False cap=True mkdtemp=True scratch=True)
check timeout_state    FAIL (exit=None timeout_reason=False pass=False)
CONFORM=unmet
verdict: not reproduced
```

The receipt does not say *why* `popen=False`. The r38 implementation does: `conform.py:103-124`
sets `saw_communicate` only on a `communicate` call and ends with
`popen_ok = popen_ok and saw_communicate` (line 124). I rebuilt the fixture from committed
bytes (`make-m19-bypass.py 13f3db7e …` → `derived 2 drain(s) into bypass-none.py; bypass-wait.py
from the primary communicate drain`) and inspected it: **0 `communicate` calls, 1 `Popen`**
(the `Popen` carries `start_new_session`, so its per-call clause passes). r38 `static_checks`
returns `(True, False, True, True, True)` — matching the receipt's `run=True popen=False
cap=True mkdtemp=True scratch=True` exactly. The failure is therefore the **absence of any
`communicate`** (`saw_communicate=False`), not detection of a bad `Popen`. The erratum's own
cited source, round-39 lesson finding 11, says exactly that ("lacking any communicate at all
(`saw_communicate`)"). The erratum also omits the second failing check, `timeout_state`
(`exit=None`): a direct re-run of the reconstructed fixture with the r38 timeout_state arguments
(`timeout 30 python3 /tmp/m19rev/bypass-wait.py 13f3db7e --repo … --tool
…/hang-after-flush.py --tool-timeout 3 --arms real --seed 5`) did not exit (`direct_rc=124` at
30 s; the predicate and `tool:` lines printed, then the process hung), matching the checker's
`exit=None` cap.

This matters because it is the sentence that explains why r38 did *not* catch the drain defect:
r38 has no `drain_shape` check (`CHECK_NAMES` = predicate, head_pin, tool_resolve,
bounded_reads, timeout_state, scratch) and its `bounded_reads` rejection is a structural
"no communicate at all" rule, not a detection of the wait+read bypass. Suggested wording:
"rejected by `bounded_reads`' `saw_communicate` conjunct (the pure wait+read fixture has no
`communicate` at all) and by `timeout_state` (the drain hangs); r38 has no `drain_shape`
check."

Minor, same paragraph: `verdict: not reproduced` is emitted by the receipt generator
`run-c8-receipts.py`, not by the r38 checker; the checker printed `CONFORM=unmet` and exited 1.
The erratum quotes the receipt faithfully, but the sentence reads as if the checker printed the
verdict word.

### MEDIUM — the S227 correction has the right number, the wrong rationale, and leaves a second `18 words`

Erratum lines 18-22 say the lesson Gate row labels the quote "(18 words)", the quote is 17
words, and "the registry row's anchor cell is immutable, so the count is corrected here rather
than by an in-place edit."

The number is right. Programmatic count and source slice:

```
words: 17
source slice: 'you can ask for commits that are reachable from r2 excluding those that are reachable from r1'
equal: True | words: 17
```

The rationale does not match where the label lives. The S227 registry row
(`corpus/SOURCES.md:233`) has no word count at all; its anchor cell reads
`The .. (two-dot) Range Notation:2538-2544; "you can ask …":2542-2544; page fetched 2026-10-24`.
The `(18 words)` label is in `corpus/lessons/round-39.md` (Gate row) and in
`corpus/SOURCES.md:292` (Round 39 bounded search: "`S227.src:2542-2544` (the two-dot range
sentence, 18 words)"). The gate's immutability rule is real (`MUTABLE = ("status", "recheck",
"used-by")`, r39 gate at `13bfba23:66`, so `anchor` is immutable), but it is not the reason the
count cannot be edited in place; the reason is the round-39 freeze, which the erratum's last
line states. The search-log instance at `SOURCES.md:292` still says 18 and the erratum does not
name it, so a reader of SOURCES sees the stale count with no supersede pointer. Fix: name both
records (or state that the erratum supersedes every "18 words" label for S227).

The closure reference checks out: `corpus/lessons/round-39-verifier-spotcheck.md:63` →
"4. Lesson Gate: S227 quote word-count label says 18, actual 17."

### LOW — the C3 citation cleanup leaves a second phantom path (`evidence/c9-red-c.txt`)

The erratum's third paragraph (lines 24-28) corrects `fixtures/make-ancestry-dags.py` (a path in
no commit: `git rev-list --all --objects | grep -c make-ancestry-dags` → `0`) and `pass=11`.
The same round-39 C3 before-cell cites a second path that exists in no commit:
`evidence/c9-red-c.txt` (`contract.md:143` and again in the evidence-path list at `:162`).
`git rev-list --all --objects | grep -c c9-red-c` → `0`; `git log --all --oneline --
'*c9-red-c.txt'` → empty. The verdicts are covered: `c9-red-a.txt` contains all three fixture
blocks (A, C, D) and its command is `run-c9-dags.py`. RevReceipts F4 already lists five
declared-but-absent files (`c7-before.txt`, `c7-red-anchors.txt`, `c8-before.txt`,
`c9-before-lane.txt`, `c9-red-c.txt`); the erratum addresses none of them, while the round-40
report describes the erratum as correcting "stale r39 contract citations" (plural). Not a
misstatement of a cited receipt (the erratum names only the builder path), but the same-class
cleanup is partial. Also stale: `run-c8-receipts.py:8` (frozen r39 file, sha `5ecaef10…`) still
documents `c8-red-wait.txt … -> CONFORM=met`, the claim the erratum supersedes.

### INFO — the "intermediate form" sentence has no committed receipt

Erratum lines 8-9: "the intermediate form that r38 accepted also passes the round-39 checker."
No committed receipt shows that form, and the round-40 report records that the two bypass
fixtures existed in no commit and "their exact bytes are unrecoverable" (only the class recipe
`make-m19-bypass.py` remains). The claim is sourced to round-39 lesson finding 11's narrative,
not to a receipt; it is not independently re-verifiable from committed bytes. [INFERENCE] It is
consistent with the r38 rule (a kept grace `communicate(timeout=TOOL_GRACE_S)` sets
`saw_communicate=True`, satisfies the per-call timeout clause, and the per-function r39
`drain_shape` would see a used communicate), but I did not run it because the bytes are gone.
Not a misstatement of a cited receipt; recorded as a verification gap.

## Verified passes

### Append-only discipline — PASS

- `git log --oneline bb1f2457..HEAD -- .ufo/waves/round-39 corpus/lessons/round-39.md
  corpus/lessons/round-39-verifier-spotcheck.md` → empty.
- `git show bb1f2457:corpus/lessons/round-39.md | sha256sum` and
  `sha256sum corpus/lessons/round-39.md` → both `4efbb0accada57dcb070e7e6d4069e90b5ca06787718f92b0c1eb05015e018a2`.
- `git diff bb1f2457..HEAD --stat -- .ufo/waves/round-39 corpus/lessons/round-39.md
  corpus/lessons/round-39-verifier-spotcheck.md` → empty.
- `git diff bb1f2457..HEAD --numstat -- SCORECARD.md LOG.md QUALITY.md SKILL.md README.md
  corpus/SOURCES.md corpus/lessons/` →
  `41 0 LOG.md`, `46 0 SCORECARD.md`, `2 1 SKILL.md`, `1 0 corpus/SOURCES.md`,
  `28 0 corpus/lessons/round-39-erratum.md`, `59 0 corpus/lessons/round-40.md`.
  `git diff … | grep '^-' | grep -v '^---'` over SCORECARD/SOURCES/LOG/QUALITY → empty, so no
  round-39 row was rewritten. The one SKILL deletion is the living "SOURCES append-only timing
  (r38)" row re-added with v3 text; the r39 row "counter conformance v2 (r39)" remains at
  `SKILL.md:887`.
- `git log --oneline -- corpus/lessons/round-39-erratum.md` → `265a955 round-40: instruments …`;
  `git status --porcelain` → only `?? .scratch/` and `?? .ufo/waves/round-40/w1/` untracked at
  the time of this check (later sibling edits are listed in the concurrent-changes note below).
- The erratum is a new file; it supersedes without editing. The fleet report is outside lane
  write scope, as stated.

### The C2 before/after re-claim is genuine — PASS (reproduced both sides)

Pinned checker: `sha256sum .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py` →
`fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987` (matches `freeze-r40.txt`).
Fixture: `sha256sum …/fixtures/generated/survivor-decoy.py` → `cfdb030c…`.

- `python3 .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py bb1f2457 --counter
  .ufo/waves/round-40/fixtures/generated/survivor-decoy.py` → all nine PASS including
  `drain_shape PASS (violations=[])`, `CONFORM=met`, `r39_rc=0`.
- `python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter
  …/survivor-decoy.py` → `drain_bind FAIL (survivor-decoy.py: violations=['Popen at line 143
  not drained by a bound, consumed communicate in its function'])`, `CONFORM=unmet`,
  `r40_rc=1`.

This confirms the erratum's parenthetical (`c10-red-decoy.txt` accepts; `c10-after-decoy.txt`
rejects via `drain_bind`) on the same fixture bytes. The only line that differs from the
receipts is `head_pin` (live HEAD, now `ede486b7…`), the known live-HEAD self-check; every
check result and the CONFORM verdict reproduce.

### `pass=11` is stale — PASS

- `grep -n 'pass=11' .ufo/waves/round-39/contract.md` → line 146.
- `cat .ufo/waves/round-39/evidence/gate-selftest-after.txt` →
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0`, `EXIT=0`.
- `git show 97b826a9:tools/mori-sources-appendonly.py | sha256sum` →
  `62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7`, identical to the r39
  freeze pin and the gate at `13bfba23`; the contract's 11 never matched the frozen gate.

### Phantom builder path / real builders — PASS

- `git rev-list --all --objects | grep -c make-ancestry-dags` → `0`;
  `git log --all --oneline -- '*make-ancestry-dags.py'` → empty.
- `sha256sum .ufo/waves/round-39/fixtures/run-c9-dags.py` →
  `d75d774092aac06da9690310782a4e95c83975c7e59282264dc71d04791e59b8` (matches `freeze-r39.txt`).
- `c9-red-a.txt`'s command is `python3 .ufo/waves/round-39/fixtures/run-c9-dags.py …` and it
  prints the A/C/D blocks; the r39 gate at `13bfba23` has `_selftest_dag_cases` (line 501).

### S227 count — PASS (number)

17 words, source slice equals the quoted string (output above); lesson row says 18; closure
defect 4 names it. See the MEDIUM finding for the rationale/duplicate-label defect.

### The superseded sentences exist as described — PASS

- `SCORECARD.md:2199` before cell: `… --counter fixtures-derived/bypass-none.py` → `CONFORM=met`
  exit 0 (`evidence/c8-red-none.txt`); bypass-wait likewise (`evidence/c8-red-wait.txt`)`.
- Fleet report `.ufo/reports/round-39/mori.md:57`: `… --counter <bypass-none|bypass-wait>` →
  `CONFORM=met` exit 0 (`evidence/c8-red-none.txt`, `c8-red-wait.txt`).
- The receipt contradicts both: `exit=1`, `CONFORM=unmet`, `verdict: not reproduced`.

## Commands run (exact, with key output)

| # | Command | Key output |
|---|---|---|
| 1 | `git log --oneline bb1f2457..HEAD -- .ufo/waves/round-39 corpus/lessons/round-39.md corpus/lessons/round-39-verifier-spotcheck.md` | empty |
| 2 | `git show bb1f2457:corpus/lessons/round-39.md \| sha256sum; sha256sum corpus/lessons/round-39.md` | both `4efbb0ac…` |
| 3 | `git diff bb1f2457..HEAD --numstat -- SCORECARD.md LOG.md QUALITY.md SKILL.md README.md corpus/SOURCES.md corpus/lessons/` | `41 0 LOG.md`; `46 0 SCORECARD.md`; `2 1 SKILL.md`; `1 0 corpus/SOURCES.md`; `28 0 …/round-39-erratum.md`; `59 0 …/round-40.md` |
| 4 | `git diff bb1f2457..HEAD -- SCORECARD.md corpus/SOURCES.md LOG.md QUALITY.md \| grep '^-' \| grep -v '^---'` | empty |
| 5 | `git log --oneline -- corpus/lessons/round-39-erratum.md` | `265a955 …` |
| 6 | `git status --porcelain` | `?? .scratch/`; `?? .ufo/waves/round-40/w1/` |
| 7 | `cat .ufo/waves/round-39/evidence/c8-red-wait.txt` | `bounded_reads FAIL (… run=True popen=False …)`; `timeout_state FAIL (exit=None …)`; `CONFORM=unmet`; `verdict: not reproduced` |
| 8 | `python3 .ufo/waves/round-39/fixtures/make-m19-bypass.py 13f3db7e <lane> /tmp/m19rev` | `derived 2 drain(s) into bypass-none.py; bypass-wait.py from the primary communicate drain` |
| 9 | import `.ufo/waves/round-38/conform.py`; `static_checks(bypass-wait)`; AST count | `(True, False, True, True, True)`; `communicate calls: 0`; `Popen calls: 1`; `CHECK_NAMES` has six entries, no `drain_shape` |
| 10 | `grep -n "popen_ok = popen_ok and saw_communicate" .ufo/waves/round-38/conform.py` | line 124 |
| 11 | `python3 …/extracted/conform-v2-r39.py bb1f2457 --counter …/survivor-decoy.py` | 9× PASS, `drain_shape PASS (violations=[])`, `CONFORM=met`, rc 0 |
| 12 | `python3 .ufo/waves/round-40/conform.py 265a955cc… --counter …/survivor-decoy.py` | `drain_bind FAIL (… Popen at line 143 …)`, `CONFORM=unmet`, rc 1 |
| 13 | `sha256sum …/extracted/conform-v2-r39.py …/generated/survivor-decoy.py` | `fe0be179…`; `cfdb030c…` |
| 14 | `cat .ufo/waves/round-39/evidence/gate-selftest-after.txt` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0`; `EXIT=0` |
| 15 | `grep -n 'pass=11' .ufo/waves/round-39/contract.md` | line 146 |
| 16 | `git show 97b826a9:tools/mori-sources-appendonly.py \| sha256sum` | `62cd4132…` |
| 17 | `git rev-list --all --objects \| grep -c make-ancestry-dags` | `0` |
| 18 | `sha256sum .ufo/waves/round-39/fixtures/run-c9-dags.py` | `d75d7740…` |
| 19 | `git rev-list --all --objects \| grep -c c9-red-c` | `0` |
| 20 | word-count/slice check on `S227.src:2542-2544` | `words: 17`; `equal: True` |
| 21 | `grep -nEi 'P-C7\|drift\|row_states\|honest\|mutant\|want table\|expected' corpus/lessons/round-39-erratum.md` | no output (rc=1) |
| 22 | `sed -n '32,34p' .ufo/waves/round-40/contract.md`; `sed -n '42,43p' corpus/lessons/round-40.md` | P-C7 "recorded in the r39 erratum" claims |
| 23 | `grep -n "S227" corpus/SOURCES.md` | `:233` anchor cell (no count); `:292` search log "(…, 18 words)" |
| 24 | `grep -n "Lesson Gate: S227" corpus/lessons/round-39-verifier-spotcheck.md` | line 63, defect 4 |
| 25 | `sha256sum .ufo/waves/round-39/fixtures/run-c8-receipts.py`; `grep -n "c8-red-wait.txt" …` | `5ecaef10…`; line 8 still says `-> CONFORM=met` |
| 26 | `timeout 30 python3 /tmp/m19rev/bypass-wait.py 13f3db7e --repo <lane> --tool …/hang-after-flush.py --tool-timeout 3 --arms real --seed 5` | `direct_rc=124`; predicate + `tool:` printed, then hang (matches receipt `timeout_state FAIL (exit=None)`) |

Not run: the full r38 checker end-to-end on the reconstructed fixture (I ran its `static_checks`
function, which is the failing clause), the gate `--selftest` (I verified the frozen gate hash
and read the committed 12/12 receipt), and the census (out of this seat's scope).

## Residual risk / verification gaps

1. The P-C7 correction is absent from the erratum; the contract/lesson claim it is present.
   Until one side is fixed, routed finding 1 has no correction of record in the erratum.
2. The "intermediate form passes the round-39 checker" sentence is narrative-only; its bytes
   are unrecoverable, so it cannot be independently re-verified.
3. The C2 mechanism sentence and the S227 rationale need re-wording; the substantive verdicts
   are unaffected.
4. `evidence/c9-red-c.txt` (and RevReceipts F4's other declared-but-absent files) remain
   phantom citations in the frozen round-39 contract; the erratum's cleanup is partial.
5. The SCORECARD C2 row remains false in place and has no in-file pointer to the erratum; the
   supersede is discoverable only via the round-40 contract/report. This is an append-only
   supersede, not a rewrite, so it is not a discipline breach, but it is a discoverability gap.

## Concurrent worktree changes observed (not made by this seat)

While this review ran, the lane worktree gained changes from other live seats. I did not touch
them; recording them for the round's hygiene sweep:

- `M .ufo/waves/round-40/evidence/c10-after-conjunct.txt`,
  `M .ufo/waves/round-40/evidence/c10-red-conjunct.txt` — `command:` lines rewritten to
  absolute paths (03:01).
- `M .ufo/waves/round-40/evidence/c10-after-selftest.txt` — command line wrapped in
  `TIMEFORMAT`/`time`, `revision:`/`wall_seconds` lines added (03:02).
- `?? 265a955` at the lane root (24 bytes, content starts `=== GATE DELTA bb1f245-`), 03:07 —
  looks like a misrooted scratch capture.

None of these are round-39 records, so the append-only finding above is unaffected. My own
writes: only this report file.
