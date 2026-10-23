# W2 seat RevQualityRows — round-38 additions to `corpus/QUALITY.md` (rows 108–110)

Verdict: **PASS** on all four acceptance axes — every new row cites the lesson that produced it,
states an observable fail state (each re-derived live this session, not read from a report), no
fabricated witness satisfies row 108, and the diff `e33bb56 → f725f307` is additions-only with
append-only numbering 108–110 after 107. Two findings below the bar: row 109's Check cell is not
runnable as printed at the scored commit (F1, reproduced; the lane has already self-flagged it in
uncommitted working-tree row 111 / lesson M10), and several `evidence/*.txt` paths the rows cite
are absent from the scored commit — present only as untracked trailing-work files (F2); every
claim they back was independently re-derived and holds.

## 1. Diff shape — additions only, append-only numbering

```
$ git diff e33bb561712b32f46861362a3fa43762fa70ae4f f725f3076972e6e70595b5ac8279be524a111ff8 -- corpus/QUALITY.md
 corpus/QUALITY.md | 29 ++++++++++++++++++++++++
 1 file changed, 29 insertions(+), 0 deletions(-)
```

Single hunk `@@ -866,3 +866,32 @@`: the new `## Criteria added round 38` header plus rows 108–110
are appended at EOF after the round-36/37 block. Zero deletions ⇒ no earlier row was touched;
rows 1–107 are byte-identical between the two revs. Numbering at the tip is strictly sequential
(`grep -nE '^[0-9]+\. '` gives 1…110 with no gap or duplicate; last committed row is 110 at
line 889). The entering tip `e33bb56` ends at row 107; the scored tip adds 108, 109, 110 in order.

Caveat on live lane state: the **working tree** now carries an uncommitted `M corpus/QUALITY.md`
appending row 111 (mtime 2026-10-23 20:05) and `M corpus/lessons/round-38.md` adding M10 — the
lane's trailing self-correction for F1 below. HEAD is still `f725f307`; the scored commit is
unaffected. All checks below run against committed tools and the scored tree.

## 2. Row 108 — corpus binding resolvability (C4 counter)

- **Citation**: `corpus/lessons/round-37.md` M9 — exists at `round-37.md:47`, and it is exactly
  the producing lesson: "a token-satisfying entry without a located quote, a capability row
  pointing nowhere and a live receipt with only the summary sentence all pass P-C2", with the
  content-anchor arm "routed to round 38" (`round-37.md:96`). `corpus/lessons/round-38.md` M1–M2 —
  exist at `round-38.md:25-26`; M2 describes this very witness-sandbox control
  (`fixtures/make-witness-sandbox.py`). PASS.
- **Observable fail state**: the row's "Shown able to fail" names the r37 counter printing
  `C2=met` on the fabricated sandbox while `count-c4.py` prints `C4=unmet`. Re-derived live:
  `python3 .ufo/waves/round-38/count-c4.py f725f3076972e6e70595b5ac8279be524a111ff8` →
  `check anchors/capability/live_rows/named_row_drift/drift_kill` all PASS, `C4=met`, exit 0
  (9.2 s); on-disk receipts `evidence/c4-witness.txt` (`C4=unmet`, exit 1 on the sandbox) and
  `evidence/v3-token-control.txt` (r37 `count-c2.py` → `C2=met`, exit 0 on the same sandbox)
  record both sides byte-consistently. PASS.
- **Fabricated witnesses do not satisfy**: the live tip run prints
  `negative witness-token-entry rejected`, `negative witness-dangling-row rejected`,
  `negative witness-summary-only-live rejected` — all three committed fixtures
  (`git ls-tree f725f307:.ufo/waves/round-38/fixtures/` lists `witness-token-entry.md`,
  `witness-dangling-row.md`, `witness-summary-only-live.txt`, `make-witness-sandbox.py`)
  are rejected while the real bytes pass, and the r37 token counter accepts the same sandbox
  (`C2=met`). The criterion is not witness-satisfiable. PASS.

## 3. Row 109 — drawn-arm replayability / conformance (C5 conform)

- **Citation**: every named lesson exists. `w1/ExecC1Seed43.md:191` — R2 (drawn-arm replay needs
  the recorded lane HEAD → the row's `head_at_measurement` clause); `w1/LabTimeoutBoundary.md`
  (timeout machinery: flush-then-hang → `tool_timeout`); SentTools MEDIUM/LOW
  (`corpus/lessons/round-37.md:100` security review: unbounded `show()`, relative `--tool`);
  `corpus/lessons/round-38.md` M5 (`:29`, the `pass=2 fail=4` → `pass=6 fail=0` mutation fix).
  **Attribution nit**: the composite "ExecC1Seed43 R4" does not exist — that report's §9 lists
  only R1–R3 (`ExecC1Seed43.md:188-195`). R4 is the round-37 verifier spotcheck's routed defect
  (`corpus/lessons/round-37-verifier-spotcheck.md:71`, "before-receipt command not re-runnable"),
  and ExecC1Seed43 §6.3 (`:158`, "`--tool` with a relative path fails") records the same defect.
  The lesson is real and cited; the seat-name + id composite is loose. Nit, not a FAIL.
- **Observable fail state**: `evidence/c5-before.txt` (committed) shows the r37 counters scoring
  all six checks FAIL → `CONFORM=unmet`; re-derived live —
  `python3 .ufo/waves/round-38/conform.py f725f307… --selftest --counter .ufo/waves/round-38/count-c1.py`
  → `CONFORM_SELFTEST pass=6 fail=0`, exit 0 (41.8 s), each mutation flipping exactly its own
  check. PASS.
- **F1 — Check cell not runnable as printed (real defect, already self-flagged)**. The row's
  Check reads `python3 .ufo/waves/round-38/conform.py --selftest` → `CONFORM_SELFTEST pass=6
  fail=0`. Run verbatim from the lane root it exits **2** with
  `conformance setup error: expected str, bytes or os.PathLike object, not NoneType`
  (`conform.py:266-270` still requires the positional `<rev>` and `--counter`; the runnable form
  is in `evidence/c5-after-selftest.txt`). I hit this independently before noticing the lane's
  fix: uncommitted working-tree row 111 + lesson M10 (`round-38.md:34` in the working tree)
  supersede 109's check cell with the runnable form. At the **scored commit** the defect stands:
  the criterion itself is sound (runnable form passes 6/0) but the printed check cell is wrong.

## 4. Row 110 — timed supersede disposition (append-only gate)

- **Citation**: `corpus/lessons/round-38.md` M3 exists (`:27` — "a landing index updated to the
  newest state instead of the first landing", pre-fix `stale_supersede=[]` vs post-fix
  `stale_supersede=[S069]` at `e37dcc6`). "ExecGateRound D3" is consistent lane bookkeeping for
  the never-returned r36 w2 seat's routed subject — the S069 supersede ruling — used identically
  in `contract.md:86` and `corpus/knowledge/containment-timed-supersede-r38.md:18`; the seat
  itself is documented at `round-37.md:85` and `round-36/w2-spec.json:23`. The `D3` token has no
  point-definition I could locate (ExecGateRound never returned a report; the spotcheck's routed
  list is numbered R1–R7), but the defect it names is real and recorded. Nit.
- **Observable fail state**: re-derived live —
  `python3 tools/mori-sources-appendonly.py f725f307… --round-base f10a320d` →
  `supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,…,S193] stale_supersede=[]`,
  and `evidence/gate-after-e37dcc6.txt` records `stale_supersede=[S069]` at `e37dcc6` — matching
  the row's "at `e37dcc6` the field lists S069 in `stale_supersede`". Selftest live:
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=0` (vs `pass=8` in committed
  `gate-selftest-before.txt` → the 9th arm is the new supersede-before-edit fixture). PASS.

## 5. F2 — cited evidence paths absent from the scored commit

`git cat-file -e f725f307:…` per cited artifact:

| cited path | at `f725f307` |
|---|---|
| `evidence/c5-before.txt`, `c4-before.txt`, `c4-after.txt`, `c5-after.txt`, `gate-before.txt`, `gate-selftest-before.txt`, `freeze-r38*.txt` | IN COMMIT |
| `evidence/v3-token-control.txt` (row 108), `evidence/c4-witness.txt` (row 108), `evidence/c5-after-selftest.txt` (row 109's runnable form), `evidence/gate-after.txt` + `gate-after-e37dcc6.txt` (row 110), `evidence/gate-selftest-after.txt` | **untracked working-tree files** (`git status --porcelain` shows `??` for all) |

So at the scored commit the rows cite evidence that does not exist in the tree they are committed
into. The claims are nonetheless true — I re-derived every one live this session — and the files
are on disk with bytes matching the live runs; they are part of the same uncommitted trailing
batch as M10/row-111 (`M dispatch-log.txt`, `M c4-after.txt`, `M c5-after.txt`). This is a
provenance gap in the commit, not a false claim; flagged for the integrator freezing the next tip.

## 6. Residual risk / verification gaps

- The `D3`/`R4` id composites are bookkeeping shorthand; a reader must chase contract + spotcheck
  to resolve them. Both resolve to real, recorded defects — no fabricated citation.
- Row 109's "Not covered" clause (pin is HEAD, not the drawn rev) was sanity-checked against the
  conform P-C5 text but I did not independently fuzz the head_pin arm beyond the selftest's own
  mutation; the mutation does flip `head_pin` alone (live run, `pin label renamed -> only
  head_pin failed`).
- I did not re-run the witness-sandbox build (`make-witness-sandbox.py` clones the tip); its two
  receipts on disk are consistent with the live counter behaviour at both ends (`C4=met` on real
  bytes; `C4=unmet`/`C2=met` on the sandbox per the recorded command lines).

Tooling: none installed or upgraded. Lane repo untouched (read-only commands only).
Report: .ufo/waves/round-38/w2/RevQualityRows.md
