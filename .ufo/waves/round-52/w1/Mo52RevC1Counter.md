# Mo52RevC1Counter — review of `count-c1.py` (round-52 C1 counter, frozen)

Seat: Mo52RevC1Counter (review). Scope: line-by-line review of
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c1.py` (786 lines,
frozen at `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2`, unchanged at `8524904a`): docstring
predicate vs code, `axes_table()` heading/fence logic, `closure_scores()` table parsing
(column picked per closure file at R), `living_pins()`/`superseded()`/the quotation rule,
the runner (archive, TMPDIR, timeout, ANY_TALLY fallback), `lane_writes` and `main`/selftest.

Method: read the frozen counter line-by-line; ran the frozen selftest; re-ran the counter at
the data rev `8524904a` from seat scratch; re-derived every parse function against the actual
git objects at R; scanned all 89 `corpus/lessons/*-verifier-spotcheck.md` files at R for the
rows `closure_scores` sees. No lane/fleet repo mutation (all `git show/ls-tree/cat-file/archive`
read-only; writes only into seat scratch). Scratch: `/fast/scratch/hyaku/mori-r52/Mo52RevC1Counter/`.

## 1. Commands run (evidence)

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c1.py --selftest
PASS ... (42 checks)
C1_SELFTEST pass=42 fail=0          # exit 0

$ cd /fast/scratch/hyaku/mori-r52/Mo52RevC1Counter/run
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c1.py \
    8524904adb25e44f24d9f25aac7eae909625c18c \
    --scratch /fast/scratch/hyaku/mori-r52/Mo52RevC1Counter/run/scratch
```

Replay at R produced **all 42 item lines identical** to the committed receipt
`evidence/c1-at-data.txt` (same axes/pins/living/locators states, `items=42 axes=6 pins=2
boxes=4 living=7 superseded=4 locators=27 mismatches=0 hidden=0 manifest=6209bdb8e400
rev=8524904a`), with one environmental difference: the replay's final line read

```
C1=unmet items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=1
hidden=0 lane_writes=5 manifest=6209bdb8e400 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=errors,lane_writes
lane_write ?? .ufo/waves/round-52/w1/Mo52CritC1Scope.md
lane_write ?? .ufo/waves/round-52/w1/Mo52ExecBatchDeviation.md
lane_write ?? .ufo/waves/round-52/w1/Mo52ExecC2Replay.md
lane_write ?? .ufo/waves/round-52/w1/Mo52MutC2Arm.md
lane_write ?? .ufo/waves/round-52/w1/Mo52MutC2Entry.md
```

Those five files are **untracked report files written concurrently by sibling w1 seats**, not by
any pinned command. The official data receipt (run before peers wrote) shows `lane_writes=0`;
the replay, run mid-wave, shows 5. See finding F1.

## 2. Predicate vs code (same sentence)

P-C1 is carried verbatim as the docstring (lines 3-35) and matches contract.md. Arm (A) axes,
(B) shonen, (C) living pins, (D) locators, floors held; `evaluate()` (line 416) maps each arm
to checks and fails on `mismatch`/`error`/`hidden`/floors/`lane_writes` (lines 428-458).
Observed behavior equals the predicate in every exercised path.

## 3. Function-by-function review

### `manifest_targets()` (96-111)
Only `lane == "mori"`, `verdict == "admitted"`, `lane_round <= 51`, axis verdict in
{"improved","harmed"}, highest round wins (ties: later list entry). At `f0b61b4` this returns
coverage (47, improved), operability (51, improved), depth (51, improved), freshness (28,
improved), calibration (50, improved), adjacency (19, improved) — matches `check_axes` targets
and the receipt. Correct.

### `unfenced()` (113-121) / `axes_table()` (123-145)
Skips fence lines (```/~~~) and requires **exactly one** `## Axes` heading outside fences.
Header must be exactly `Axis|Score|Evidence pointer|Last change`; delimiter row skipped; rows
collected until first `#` line or first non-table line after rows began. In SCORECARD.md at R:
one `## Axes` (line 6), header at line 8, 6 rows, 4 cells each — `heads=1`, `len(rows)=6`.
Edge cases (zero/2 headings, fenced heading, duplicate axis row, 3-cell row) are all covered by
the selftest. No defect found.

### `closure_scores()` (147-171) — the parse/column question
For every `corpus/lessons/round-K-verifier-spotcheck.md` at R (89 files), it scans **every**
unfenced pipe row, and for the first row whose first cell (stripped) is an axis name with a
**numeric second cell** (`\d{1,2}`) it records `(K, score)`, newest closure first. A
`Score N → M` phrase found in the rest of the row overrides the score to M.

What it returns per axis at R (re-derived from the actual tree, then confirmed by the full
replay): all six axes resolve to the round-51 closure's per-axis table:
- operability → (51, 7)
- depth → (51, 5)
- coverage → (51, 6)
- freshness → (51, 5)
- calibration → (51, 5)
- adjacency → (51, 6)

Why: of the 89 closures, only rounds 49/50/51 have per-axis tables whose second column is
numeric (the table format `| axis | entering | verdict | basis |`; round-51 is the newest and
lists all six). Older closures' per-axis tables (e.g. rounds 13-18, 24-34, 37, 42-48) use the
**verdict** as the second cell (`| coverage | harmed | … |`), so their rows are correctly
skipped by the numeric filter. No mis-parse occurs at R. See finding F2 for the shape-risk.

### `check_axes()` (173-215)
For each axis: `round N` from the Last change cell's first `\bround[ -]?(\d+)\b` must equal the
manifest target; the segment from that match to the next `;` must contain the verdict word; the
Evidence cell must contain the round-N* spot-check path when that file exists at R (else
"MANIFEST.json"); the Score cell must equal the closure score. All six rows pass at R (e.g.
operability cell `round 51 (improved, score held); …` → 51/improved, evidence names
`round-51-verifier-spotcheck.md`, score cell `7` = closure (51,7)). Correct.

### `parse_shonen()` (217-226) + `bound_path()` (228-238)
Boxes counted by `^\s*[-*] \[[ ~xX]\]` → 4 at R. Pins via PIN regex (73-75); hidden tally
tokens after pin substitution → 0 at R. `bound_path` requires exactly
`python3 <relative .py path> --selftest` (no `..`, no absolute). Both SHONEN pins bind
(`tools/mori-pin-check.py`, `tools/mori-unlanded-check.py`; modes 100755/100755 — regular
files, not symlinks). Correct.

### `check_pins()` (265-289) + receipts
Runs each pinned tool in the archive; takes its last tally line; requires an exact line match in
`.ufo/waves/round-52/evidence/selftests/<stem>.txt` at R. Receipts exist and contain the
observed lines (`PIN_CHECK_SELFTEST pass=125 fail=0`; `UNLANDED_SELFTEST pass=17 fail=0`).
`tally_ok` (254-262) checks (N/M): `N == pass and M == pass+fail`; arrow form compares prefix
and pass/fail. Observed states ok. Correct.

### `living_pins()` (291-303) / `superseded()` (305-319) / `check_living()` (322-366)
Single-line pins enumerated with criterion tracking (`CRIT` = `^(\d+)\. `; headings reset).
Supersession: (a) QUALITY.md later numbered criterion matches `supersedes N's check`; (b) either
file later line contains the word `supersedes` **and** the stale pin's span-and-tally text
verbatim. The quotation rule in `check_living` (quoted span on a superseding line next to its
replacement pin is not counted) is exact.

Verifications at R: entering pins (QUALITY 885/909, README 607/608) are still present
byte-for-byte at R; 885 → superseded by criterion 111 ("This row supersedes 109's check cell
only"); 909 → superseded by criterion 141 ("This row supersedes 112's check cell only"); README
607/608 → superseded by the appended round-52 notes (lines 727/728) which quote the stale spans
verbatim and carry the replacements; the replacement pins (QUALITY 1360, README 727/728) run and
match (22/22, 22/22, 9/9). Correct.

### `check_locators()` (368-414)
Scans the six Axes rows' Evidence/Last-change cells and SHONEN box lines. For each `` `path:N[-M]` ``:
file exists at R, `1 <= N <= M <= lines`; if the preceding fragment (back to last `;`) holds a
double-quoted string, its whitespace-collapsed form must appear in lines N..M; if it holds
`proposed A → B`, `A → B` must appear. At R all 27 locator items check ok, incl. quote checks
(`Score 6 → 6`, `Score 5 → 5`) and the pair check `SCORECARD.md:1781` → `5 → 6` found.
Correct; see F4 for the fragment-splitting nuance.

### Runner (main 465-579): archive / TMPDIR / timeout / ANY_TALLY
- Archive: `git archive <rev>` piped to `tar -x` in `--scratch/tree` (539-544); verified it
  extracts the revision's tree; pinned commands run with `cwd=tree`.
- TMPDIR: set to `<scratch>/tmp`, plus `PYTHONDONTWRITEBYTECODE=1` (545). Verified (scratch
  tmp dir created/removed).
- Timeout: `TOOL_TIMEOUT=900` default, overridable (`--timeout`); `TimeoutExpired` → None →
  item error (550-551). Correct.
- TALLY/ANY_TALLY (71-72): TALLY requires a `*SELFTEST` prefix; ANY_TALLY allows a bare
  `pass=N fail=M` and is the fallback (uses the last match). Correct for the tools observed.
- `exe = [sys.executable] + argv[1:] if argv[0] == "python3" else argv` (546) — runs `bash`
  entries as written and python3 entries via the host interpreter. Fine.
- Cleanup: with `--scratch`, removes `tree/` and `tmp/` in `finally` (572-575); confirmed empty
  scratch after replay. Without `--scratch`, removes the whole tempdir. Correct.

### `lane_writes()` (562-569)
Diff of `git status --porcelain --ignored --untracked-files=all` before vs after the run; any new
line prints `lane_write …` and flips the result to unmet (via `errs += 1 if writes else 0`,
436; `failed.append("lane_writes")`, 443). See finding F1 — the replay exposed that concurrent
untracked writes (this wave's own seat reports) flip the verdict even though no pinned command
wrote anything. This is the only divergence the replay found.

### selftest (582-786)
42 checks, all PASS, covering: manifest target selection; axes-table errors (missing row,
duplicate row, second heading, fenced heading, stale round, wrong verdict word, substring
verdict, evidence pointer, score cell, score-move from closure, newest-closure-wins); shonen
(stale pin, missing receipt, symlink, hidden tally, box floor, timeout); living (stale,
rewritten-in-place, deleted, wrong superseding pin, self-supersede, fragment/placeholder,
non-zero rc, lane_writes); locators (quote ws-folding, found/absent, pair, out-of-range,
missing file); ANY_TALLY parsing. No defect found in the selftest itself.

## Findings


- **F1 — MED — `count-c1.py:562-569` (lane_writes): the arm is a working-tree diff, not a
  causal write detector; concurrent untracked writes by other seats flip C1 to unmet.** Evidence:
  replaying the frozen counter at `8524904a` (with `--scratch`) reproduced every item line of
  `evidence/c1-at-data.txt` but ended `C1=unmet … errors=1 lane_writes=5 failed=errors,lane_writes`,
  the five "lane_write" lines being `.ufo/waves/round-52/w1/Mo52CritC1Scope.md`,
  `Mo52ExecBatchDeviation.md`, `Mo52ExecC2Replay.md`, `Mo52MutC2Arm.md`, `Mo52MutC2Entry.md`
  — untracked reports written concurrently by sibling seats, not by any pinned command (pinned
  commands run in the extracted archive tree, so they cannot write the measured repo at all
  unless they deliberately reach outside it; thus the arm can in practice only fire on external
 /concurrent mutations). The committed receipt was taken before peers wrote. Also note the five
  files shown were observed by my run, not created by it. Recommended framing for round 53: a
  named limit — "lane_writes may be nonzero when any other actor writes the working tree during
  the run; verification must run in a quiescent tree" — and/or scope the arm to tracked-path
  changes only.
- **F2 — LOW — `count-c1.py:147-171` (closure_scores): row-shape heuristic, not a table-typed
  parse.** The score is taken from the first *anywhere* pipe row in the newest closure whose
  first cell is an axis name and whose second cell is numeric; there is no check that the row
  belongs to the per-axis grade table (no header/title context). Verified safe at R: across all
  89 closures only rounds 49/50/51 have numeric-second-cell axis rows, and round-51's per-axis
  table supplies all six scores; older closures' per-axis rows have the verdict in the second
  cell and are skipped. A future closure containing an unrelated numeric row starting with an
  axis name would be misread. Low risk, not triggered now.
- **F3 — LOW — `count-c1.py:163-170`: the `Score N → M` override string is recognized only
  after the second cell and only when the literal word `Score`/`score` precedes the arrow.** If a
  closure ever states the score move differently (e.g. the move floating the second cell itself),
  the override would be missed and the second cell used. Not triggered at R (no closure uses the
  override; the selftest covers the current syntax).
- **F4 — LOW — `count-c1.py:381-391` (check_locators): quote window truncates at the last `;`
  and only the last quoted string in the fragment is used.** A quoted phrase spanning an embedded
  `;` or multiple quotes before one locator would not all be checked. Not triggered at R (all 27
  locators verified, including both quote checks and the pair check).
- **F5 — LOW — `count-c1.py:545` (runner env): the child environment is the host environment
  with only `TMPDIR`/`PYTHONDONTWRITEBYTECODE` overridden.** The pinned commands therefore run
  with host PATH/env (unsandboxed) — this is a documented named limit in the contract, but the
  counter itself does not restrict e.g. `PYTHONPATH`/`HOME`. Not an error at R; recorded for
  completeness.
- **F6 — INFO — no counter defect found in `manifest_targets`, `axes_table`, `check_axes`,
  `parse_shonen`, `check_pins`, `living_pins`/`superseded`/`check_living`, `check_locators`
  (aside from F4), the selftest, or main's archive/TMPDIR/timeout handling.** The selftest
  passes 42/42; the frozen counter at R deterministically reproduces the committed data receipt
  item-for-item (only F1's concurrency sensitivity differs).

## Verification gaps
- I did not run the counter against a *mutated* data state to see each failure mode live; the
  selftest covers those synthetically, and the control receipts (do-nothing etc.) from the L1
  cover the main failure modes.
- I did not independently re-execute the tools' own selftests outside the counter's archive run;
  the counter's archive run does execute them (state=ok), which is the observation the claim
  uses.
- The five `lane_writes` files were observed during my replay; they belong to sibling seats and
  were not created by me. (No file was written by me anywhere under the lane or fleet repos.)
