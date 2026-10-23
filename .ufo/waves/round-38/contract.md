# mori round 38 — frozen contract (L1 MoriR38, attempt 1)

Entering tip: `e33bb561712b32f46861362a3fa43762fa70ae4f` (round 37 admitted; closure
`corpus/lessons/round-37-verifier-spotcheck.md`).
Frozen before any data seat or data receipt: this contract, `count-c1.py` (v4), `conform.py`,
`count-c4.py`, the two conformance fixtures, and the three fabricated-witness payloads. Pins are
recorded in `evidence/freeze-r38.txt` (sha256 over the frozen paths). A change to a predicate after
this freeze is a new counter version, not an edit.

## Claims

### C1 — calibration (5, tied lowest): the content half of the drift-corpus binding (r37 M9)

Round 37's P-C2 content checks are token checks: an entry carrying `huge_cap`,
`redirect_private_refused` and `1caa242` passes, a capability row pointing at a nonexistent path
passes, and a live receipt carrying only the summary sentence passes. The critic's three fabricated
witnesses plus a real tool print `C2=met` (r37 lesson M9). This round adds the content anchors that
a token cannot satisfy.

**P-C4 (frozen, verbatim in `count-c4.py`'s PREDICATE and in the report):**

> P-C4: at revision R, the committed drift-corpus binding passes four content checks that the round-37 token checks cannot discriminate — every `anchor:` line in the round-38 knowledge entry resolves byte-exactly in tools/mori-source-drift.py at R, every path the SCORECARD capability row cites resolves at R, the live receipt names one drifted row by id per drifted row its summary counts, and the probe's selftest runs the named-row arm `row_states` whose own mutation kills it — and the same counter rejects three fabricated token-satisfying witnesses (an entry with the tokens but no resolvable anchor, a capability row citing a nonexistent path, a live receipt with only the summary sentence), while the real bytes pass.

Counter: `.ufo/waves/round-38/count-c4.py <rev>`. Exit 0 met, 1 unmet, 2 setup error.
Content checks: `anchors` (each of the entry's backticked `tools/mori-source-drift.py` anchor strings
appears verbatim in the tool bytes at R), `capability_paths` (every backticked path in the
capability row `source-drift re-fetch probe` resolves at R), `live_rows` (the live receipt carries a
`drifted <S### ...>` per-row line whose id is a registry row at R), `named_row_drift` + `drift_kill`
(the probe's selftest runs the arm and a mutated comparison fails it).
Negatives: `fixtures/witness-token-entry.md`, `fixtures/witness-dangling-row.md`,
`fixtures/witness-summary-only-live.txt` — each projected onto the real bytes and judged by the same
four checks; each must fail at least one.

**Before** (do-nothing control, measured at `e37dcc6` before this round's artifacts):
`python3 .ufo/waves/round-38/count-c4.py e37dcc6` → `C4=unmet` exit 1 with `anchors FAIL (anchors=0)`
and `capability FAIL (missing=['evidence/drift-live-r37.txt'])`; `live_rows`, `named_row_drift` and
`drift_kill` already PASS at the entering tip (the named-row arm shipped in round 37 — what round 37
lacked was a check that requires it). Receipt: `evidence/c4-before.txt`.
The discrimination control is a clone of the scored tip with the three fabricated witnesses
committed (`fixtures/make-witness-sandbox.py`): the round-37 counter prints `C2=met` exit 0 on it
(`evidence/v3-token-control.txt`) while `count-c4.py` prints `C4=unmet` exit 1
(`evidence/c4-witness.txt`). At `e37dcc6` the three negatives are also rejected, but partly by the
already-failing capability check; the witness sandbox is the control that isolates each witness.

Kill rule: a do-nothing control cannot print `C4=met`. A counter that only adds the per-row live
check (no anchor resolution, no capability-path resolution, no `named_row_drift` arm) still accepts
the token entry and the dangling row → `C4=unmet`. A docs-only control (entry rewritten, no tool
arm) fails `named_row_drift`.

### C2 — operability (7): instrument conformance and replayability (r37 R1/R2/R4 + SentTools MEDIUM/LOW + LabTimeoutBoundary)

Round 37's C1 counter prints a predicate that no longer matches the contract's P-C1 blockquote
(ExecC1Seed43 R1), does not print the lane tip its drawn arm was drawn from (R2), executes a
repo-relative `--tool` from `cwd="/"` (R4), keeps unbounded `show()` git reads (SentTools MEDIUM),
and its timeout disclosure is false: the inner GNU `timeout` fires first (exit 124), so
`tool_timeout` is unreachable inside budget+grace and `real_arm()` does not check the exit code
(LabTimeoutBoundary, measured 185.24 s). This round lands the conformance checker and the counter
version that passes it.

**P-C5 (frozen, verbatim in `conform.py`'s PREDICATE and in the report):**

> P-C5: at revision R, the round-38 C1 counter prints the contract's P-C1 bytes as its predicate, prints the lane tip it measured as `head_at_measurement=<40-hex>`, resolves a repo-relative `--tool` path against the lane, bounds every child and git read by a timeout and the committed-blob read by a byte cap, maps a tool that flushes then hangs to `tool_timeout` (never a pass and never a silent unmet), and creates every scratch directory with `tempfile.mkdtemp` under the lane's `.ufo/waves/round-38/scratch`; the conformance checker passes all six checks on those bytes and each of six mutations of them flips exactly its own check to FAIL.

Counter: `.ufo/waves/round-38/conform.py <rev> [--counter PATH] [--contract PATH]`. Checks:
`predicate` (contract P-C1 blockquote normalised == the counter's printed `PREDICATE`),
`head_pin` (`--pin-only` prints the lane tip), `tool_resolve` (`--print-tool <repo-relative path>`
prints the absolute resolved path), `bounded_reads` (every `subprocess.run`/`Popen` in the counter
carries `timeout=`; the committed-blob read carries a byte cap), `timeout_state`
(`fixtures/hang-after-flush.py` under `--tool-timeout 5` yields `C1=unmet` with a `tool_timeout`
reason, never `C1=met`, never a silent `real arm: pass`), `scratch` (every `mkdtemp` in the counter
passes `dir=` a lane scratch parent under `.ufo/waves/round-38/scratch`).
`--selftest` applies six textual mutations to copies of the counter and requires each to flip its
own check.

**Before** (do-nothing control):
`python3 .ufo/waves/round-38/conform.py e37dcc6 --counter .ufo/waves/round-37/count-c1.py --counter .ufo/waves/round-37/count-c2.py`
→ `CONFORM=unmet` exit 1, six checks FAIL (the r37 counter has no `--pin-only`/`--print-tool`/
`--tool-timeout`, its printed predicate differs from the r38 contract, `count-c2.show()` runs an
unbounded `git show`, and neither counter's scratch parent is the round-38 one). Receipt:
`evidence/c5-before.txt`.

Kill rule: a do-nothing control cannot print `CONFORM=met`; a counter with only the head pin and
the tool resolution still fails `timeout_state` (the flush-then-hang tool scores `C1=met`) and
`bounded_reads` (the unbounded `show()`), so `CONFORM=unmet`.

### C3 — depth (5, tied lowest): timed supersede semantics in the append-only gate (r37 ExecGateRound D3)

The gate's `superseded` field is presence-based: it cannot express "disposition predates the
change". S069's only superseder S073 landed at `71abd41` (2026-10-21), before S069's in-place edit
`62db24c` (2026-10-22), so the gate reports `superseded_by=S073` for a disposition that cannot
dispose the edit. This round adds the timed reading and lands S226, whose row postdates the edit.

**P-C6 (frozen, verbatim in the gate's PREDICATE and in the report):**

> P-C6: at revision R, tools/mori-sources-appendonly.py reports, after its summary line, `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; an id is superseded-as-of only when its latest superseding row's landing commit is a descendant of the id's last immutable-cell edit commit, and is listed in stale_supersede otherwise; on the lane history S069 is stale before its round-38 supersede row lands and no id is stale after, and the selftest carries a supersede-before-edit fixture that lists the id in stale_supersede.

Gate: `tracked tools/mori-sources-appendonly.py`. `--selftest` gains two cases (`supersede after
edit` → `superseded_as_of=[S001] stale_supersede=[]`; `supersede before edit` →
`stale_supersede=[S001]`), and the per-id `superseded_by=` names the latest superseder.
S069 disposition: new row `S226` (source opened this round) whose `teaches` opens `supersedes S069`,
landed after `62db24c`.

**Before** (do-nothing control): at `e37dcc6` the gate prints no `supersede_timing` line
(`grep -c 'stale_supersede=' evidence/gate-before.txt` → 0) and `--selftest` has no
supersede-before-edit case. Receipt: `evidence/gate-before.txt`,
`evidence/gate-selftest-before.txt`.

Kill rule: a do-nothing control cannot print the timing line; a gate that adds the field but derives
it from row presence (not commit order) lists S069 in `superseded_as_of` at `e37dcc6` → the frozen
reading fails its own selftest fixture.

### P-C1 of record (counter v4, printed verbatim)

> P-C1: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed, and exactly the truth's per-id `changed`/`deleted` lines, on each of 24 sandbox SOURCES.md histories drawn at run time, on the lane's own history (rev 6bd57097, round base f10a320d) where the independent oracle lists at least one id, and on one run-time-drawn challenge history presented in real-arm clothing (lane path, lane git identity, lane title); and the same counter rejects all three negative fixtures (a real-arm memoizer, a constant printer, a summary-only printer) and matches the standing truth on one run-time-drawn ancestor revision of the lane repository whose expected answer is not the published real-arm constant, and prints the lane tip it measured as head_at_measurement=<40-hex>.

Counter: `.ufo/waves/round-38/count-c1.py <rev>`. Exit 0 met, 1 unmet, 2 setup error.
`conform.py`'s `predicate` check compares this blockquote to `count-c1.py --print-predicate`
after whitespace normalisation; the r37 defect was that the contract's *first* P-C1 blockquote
matched the v1 counter while the committed counter printed the longer v2 predicate (ExecC1Seed43
§6.1). Here there is one predicate of record and one counter version.

## Debt disposition (r37 routed, r38)

| # | routed item | disposition |
|---|---|---|
| 1 | report erratum owed to r38 (8ff9bba→1caa242; live receipt 225/10; LOG append-only amendment) | first commit of the round: `corpus/lessons/round-37-erratum.md` + an appended `LOG.md` correction naming the superseded text (also F1a/F1b/F2/F4 from ExecLogAnchors, M6–M10, debt (f) reopened, capability first-working) |
| 2 | axes-cell sweep (freshness still cites r37 C2) | SCORECARD axes cells corrected in place + appended round-38 correction note; `operability` gains the round-37 pointer |
| 3 | P-C2 content-half gap (M9) | claim C1 |
| 4 | SentTools MEDIUM (unbounded `show()`) / LOW (relative `--tool`) | claim C2 |
| 5 | v3 counter freeze/predicate reconciliation (ExecC1Seed43 R1) + drawn-arm lane-tip pin (R2) | claim C2 (`predicate`, `head_pin`) |
| 6 | before-receipt command form runnable as printed (R4) | claim C2 (`tool_resolve`) + re-emitted before receipts with a `command:` line |
| 7 | source-drift capability first-working 37 vs r36 (R5) | SCORECARD capability cell corrected to 36 with the r37 narrowing; correction note |
| 8 | debt (f) SIGTERM→grace→SIGKILL operator tradeoff | named, not decided: an L0 question and a lesson row; no counter behaviour is claimed as closed |
| 9 | QUALITY 103 second clause (dispatch-log staged=/index records) | `dispatch-log.txt` records the index-clean check after each `landed` line; the criterion's check is re-read against this round's log |
| 10 | count-c2 mkdtemp scratch alignment (r36 debt g) | claim C2 (`scratch`): round-38 scratch parent under `.ufo/waves/round-38/scratch`, every arm `mkdtemp` |
| a | ExecGateRound S069 ruling | claim C3 + S226 |
| b | gate predates-the-change gap | claim C3 |
| c | gen-w2-spec recipe text (QUALITY 104 → evidence/c2-after.txt; `S[0-9]{3}` grep) | edited in the round-36 generator, with the superseded text quoted in the r38 lesson |

## Evidence paths

`evidence/census-start.txt`, `evidence/census-end.txt`, `evidence/gate-before.txt`,
`evidence/gate-selftest-before.txt`, `evidence/c4-before.txt`, `evidence/c5-before.txt`,
`evidence/c4-after.txt`, `evidence/c5-after.txt`, `evidence/gate-after.txt`,
`evidence/gate-selftest-after.txt`, `evidence/c1-before-rerun.txt`, `evidence/freeze-r38.txt`,
`evidence/v3-token-control.txt`.
