# mori round 37 — frozen contract (L1 MoriR37, attempt 1)

Entering tip: `842a32074b5c7972e9728f3f629d83eb92f127c2` (round 36 admitted).
Frozen before any data seat or data receipt: this contract, both counters, and the three negative
fixtures. The pins are recorded in `evidence/freeze-r37.txt` (git blob hashes over the frozen
paths). A change to a predicate after this file's freeze is a new counter version, not an edit.

## Claims

### C1 — measurement discrimination (calibration, score 5 — tied lowest)

The round-36 C2 measurement admits a tool that never computes the real-arm answer: `count-c2.py`
compares only the summary line, and the real-arm expectation is published in the receipt, so a
tool that gates on the sandbox git identity and prints the constant (w2/RevNgC2 N1) scores
`C2=met`. It also compares only the summary line, so a program that prints the four summary lists
correctly and omits the per-id `deleted <id>` lines (w2/MutC2Deleted limit 3) scores `C2=met`.

**P-C1 (frozen, verbatim in the counter's PREDICATE and in the report):**

> P-C1: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth
> for ids, deleted, superseded and round_changed, and exactly the truth's per-id
> `changed`/`deleted` lines, on each of 24 sandbox SOURCES.md histories drawn at run time, on the
> lane's own history (rev 6bd57097, round base f10a320d) where the independent oracle lists at
> least one id, and on one run-time-drawn challenge history presented in real-arm clothing (lane
> path, lane git identity, lane title); and the same counter rejects all three negative fixtures:
> a real-arm memoizer, a constant printer, and a summary-only printer.

Counter: `.ufo/waves/round-37/count-c1.py <rev>`. Exit 0 met, 1 unmet, 2 setup error.
Challenge arm: `tempfile.mkdtemp` under `<lane>/.ufo/waves/round-37/scratch/`, even sandbox index
(forced deletion witness), git identity `mori-shokunin <mori@shokunin.local>`, lane SOURCES title;
truth from the counter's op log, never from the receipt. Negatives: `fixtures/memo-n1.py`
(honest on `user.name == "mori counter"`, published constant + its 18 `changed` lines elsewhere),
`fixtures/const.py`, `fixtures/summary-only.py`. Each negative is judged on a 4-history blind
draw, the real arm and a challenge; it must fail at least one arm.

**Before** (do-nothing and shortcut controls, measured with the round-36 counter):
`count-c2.py bf0df77 --tool fixtures/memo-n1.py --seed 11` → `C2=met` exit 0;
`count-c2.py bf0df77 --tool fixtures/summary-only.py --seed 12` → `C2=met` exit 0.

Kill rule: a do-nothing control (no counter change) cannot print `C1=met`; a counter that only
adds the per-id check but no challenge arm fails the memoizer negative (its real arm passes and
its blind arm passes), so `C1=unmet`.

**Timeout boundary (r36 routed debt f):** the tool budget is 120 s; on expiry the child's process
group gets SIGTERM, then SIGKILL after a 5 s grace, and the arm reports `tool_timeout` — a distinct
state, never a list mismatch. The counter cannot distinguish a slow honest tool from a hung one;
that is the disclosed boundary.

**Scratch uniqueness (r36 routed debt g):** every arm uses `tempfile.mkdtemp`; no seed-derived
shared directory, so two seats replaying the same seed do not collide (r36 ExecReC2B §5).

### C2 — drift-probe hardening verification (freshness, score 5 — tied lowest)

Round 36 landed two fetch policies at `8ff9bba` (4 MiB bounded read; post-redirect
public-destination policy) with only row-level selftest evidence. This round names them, pins each
with a mutation that must kill it, and binds the corpus.

**P-C2 (frozen, verbatim in the counter's PREDICATE and in the report):**

> P-C2: at revision R, tools/mori-source-drift.py passes its selftest with the named arms
> `huge_cap` and `redirect_private_refused`, each of those arms fails in a copy with its policy
> removed (4 MiB read cap; post-redirect public-destination policy), and the committed corpus
> binds the hardening (knowledge entry citing this round's source rows and commit 8ff9bba, a
> SCORECARD capability row, two README coverage-map rows) with the round's live sweep receipt
> present.

Counter: `.ufo/waves/round-37/count-c2.py <rev>`. Checks: `tool_present`, `selftest`, `cap_kill`,
`redirect_kill`, `knowledge`, `capability`, `readme`, `live`. Mutations are textual: 
`FETCH_MAX_BYTES = 4 * 1024 * 1024` → `1 << 40`; `if not _public_redirect_target(final):` →
`if False:`. The named-arm fixture uses a literal 4 MiB body so a mutated cap cannot resize it.

**Before** (do-nothing control): `count-c2.py 842a320` → `selftest FAIL` (the tool at the entering
tip carries only the four unnamed arms), `knowledge FAIL`, `capability FAIL`, `readme FAIL`,
`live FAIL`, `C2=unmet` exit 1.

Kill rule: a do-nothing control cannot print `C2=met`. A docs-only control (entry written, tool
unchanged) fails `selftest`/`cap_kill`; a tool-only control (arms added, no corpus binding) fails
`knowledge`/`capability`/`readme`/`live`.

## Debt disposition (r36 routed, r37)

| # | debt | disposition |
|---|---|---|
| a | drift hardening verify + knowledge entry | claim C2 |
| b | count-c2 memoization hardening (N1 class) | claim C1 |
| c | per-id `deleted <id>` line checks | claim C1 |
| d | r17-jj environment red | `tools/mori-round17-jj-regressions.py`: the side-effect assertion is scoped to the testable redirect property, with the positive jj-file evidence required when a sandbox carries a jj workspace; receipt `evidence/r17-jj-selftest-r37.txt` (exit 0; r36 `w2/ExecCensusRegression.md` is the pre-fix red) |
| e | SentData path redaction hygiene | this round's counters print repo-relative paths for lane paths (`display_path`); no new evidence file carries an absolute operator path |
| f | sandbox SIGKILL boundary | disclosed in C1's predicate output and timeout contract (above) |
| g | seed-collision scratch paths | `mkdtemp` per arm (C1), no seed-derived directories |
| h | 9-vs-7 drifted prose | re-verified: the landed prose names nine with S210/S211 (`corpus/knowledge/source-drift-r36.md:24-33`, `corpus/README.md` Round-36) |

## Evidence paths

`evidence/c1-before-memo.txt`, `evidence/c1-before-summary.txt`, `evidence/c1-after.txt`,
`evidence/c2-before.txt`, `evidence/c2-after.txt`, `evidence/drift-live-r37.txt`,
`evidence/r17-jj-selftest-r37.txt`, `evidence/census-start.txt`, `evidence/census-end.txt`,
`evidence/freeze-r37.txt`.
