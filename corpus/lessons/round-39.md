# Round 39 — 2026-10-24 (L1 mori-r39, attempt 1)

## Gate

| source | decision | located quote |
|---|---|---|
| S227 — gitrevisions(7) `https://git-scm.com/docs/gitrevisions`, opened 2026-10-24 (copy `corpus/evidence/sources-r39/S227.src`) | **admitted** (mined) | `S227.src:2542-2544`: "you can ask for commits that are reachable from r2 excluding those that are reachable from r1" (18 words) |
| S228 — Python `os.path.realpath` docs re-open `https://docs.python.org/3/library/os.path.html#os.path.realpath`, opened 2026-10-24 (copy `corpus/evidence/sources-r39/S228.src`, differs from `S226.src` only in the docs build footer) | **admitted** (mined; supersedes S226) | `S228.src:657-659`: "Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system)." (24 words) |

Rejected: none new. Search log: `corpus/SOURCES.md` Round 39 bounded search (identified 2, opened 2, excluded 0).
Registry rows before → after: 226 → 228 (+S227, +S228); no existing row's `status`/`recheck`/`used-by` changed
(S226's cells are immutable; its `:657-658` suffix is corrected by S228's superseding row, QUALITY 113).
Census: start exit 0 (`evidence/census-start.txt`), end exit 0 (`evidence/census-end.txt`).

## Mistakes

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M20 | routed-defect latency (a located-quote defect disclosed in-round was routed outward instead of fixed in-round) | the S226 anchor suffix `:657-658` was found one line short by w2/RevS226Row in round 38 (mined there as M16's evidence) and routed by the r38 closure instead of corrected; the same closure routed it again to round 39 | none — no criterion then required fixing a located-quote defect before round end; QUALITY 113 now exists | S228 (`supersedes S226`) lands the corrected `:657-659` suffix this round without an in-place immutable-cell edit; the r38 fleet report's `:2` cite is fleet history outside lane write scope, recorded in the round-39 report. Shown able to fail: an in-place anchor edit would list the row in the gate's `ids=[...]`; the entering-tip row still prints `:657-658` (`git show 13f3db7e:corpus/SOURCES.md`) |
| M21 | fixture-not-discriminating (the intended F1 fixture did not separate v1 from v2) | the first dag-a construction made the side branch carry the pre-edit value; the r38 gate printed `stale=[S001]` on it — the right verdict reached through fabricated intermediate edits (F2), so the fixture showed no F1 divergence; the divergence appeared only after brute-forcing 16 DAG constructions × 2 date orders | none — "the receipt must show the old instrument wrong" was assumed, not checked; the round-39 selftest now carries fixture D ("landing is the last edit commit") whose receipt separates the instruments | fixture D: both branches make the same edit and the supersede row rides the side branch; the predicate's plain words read as-of and the r38 bytes print stale (`evidence/c9-red-a.txt` third block). Shown able to fail: the pre-fix fixture's red receipt shows no v1/v2 timing divergence; fixture D's does |
| M22 | measurement-shape drift (the honest arm's output shape was assumed, not read) | count-c7's first draft parsed the honest `row_states` table, but the probe prints the got/want tables only on FAIL; the smoke run at the entering tip printed `drift_kill_v2 FAIL (mutation anchor or table unparsable)` | none — the counter's own smoke run against the real tool caught it before any data seat ran | the check parses the mutant run's got and want tables structurally (a symmetric-substring cheat dies on the parse, and the expected post-state stays run-time-drawn). Shown able to fail: the smoke-run output above; the fixed counter prints `drift_kill_v2 PASS (drawn=fresh … want_drifted=['S103'] flips_ok=True)` (`evidence/c7-after.txt`) |

## Round shape and debts

r38 routed items: M18 residuals → claim C1 (+ lesson M20–M22); M19 residuals → claim C2; F1/F2 → claim C3;
S226 quote suffix → S228 (QUALITY 113); r38 report `:2` cite → recorded, fleet history (round-39 report). Debt (f)
stays OPEN/operator-owned (L0 question from round 37; the round-39 counters freeze the same disclosed
SIGTERM → grace → SIGKILL trade).

## Wave-1 findings for integration (attempt 2 / closure)

1. (w1/ScoutC7Bounds, FAIL) P-C7's words "a structural per-row state difference between the honest and
   mutated runs" exceed the code: drift_kill_v2 compares the mutant run's got table against its want table
   (the fixture expectation, equal to the honest table only because named_row_drift gates the honest PASS).
   Semantically equivalent on a passing honest run; the prose should say "against the arm's expected
   table" or the code should parse both runs. Routed with the frozen-pins note (a wording fix needs no
   re-freeze of the predicate; a code fix is a new counter version).
2. (w1/RevCensus, MEDIUM) The gate's `superseded` eligible set is edit-bounded (`superseded = cid for cid
   in ids if cid in sup_map`, ids = changed rows), so a never-edited superseded row (S226) never reaches
   `supersede_timing` even though P-C9's plain words cover it (last edit = its landing commit; the
   superseder descends from it). The receipt (18 ids) is honest; the contract/SCORECARD prose "18 ids +
   S226 once S228 lands" overclaims — the same words-vs-code class C3 closed for F1/F2, re-entering via
   the eligible-set definition. Routed: either narrow the prose or extend the eligible set (new gate
   version + pin change), next attempt.
3. (w1/MutC8NoneVal, note) timeout_value's violation message says "non-numeric constant" where the value
   is a name resolving to None; naming the symbol would aid audits. Cosmetic; routed forward.
4. (w1/RevC8Value, HIGH) timeout_value survives two r38-M19-class bypasses: a function-local shadow
   (`TIMEOUT = 120` module-level, then `TIMEOUT = None` inside `run()` before a
   `communicate(timeout=TIMEOUT)`) and a module-level conditional rebind (`if cond: NAME = None` after
   `NAME = 120` — the fold only walks `tree.body`). Both print CONFORM=met with a runtime-None drain.
   The frozen C2 claim (routed fixtures + conjunct) stands measured; these survivors are next-round claim
   material. Also: `1e400` (inf) passes (OverflowError at runtime); fold crashes (`1/0`, `A = A`) exit 2
   rather than FAIL. Routed to round 40 with the seat's PoCs under `w1/RevC8Value.md`.
5. (w1/CritC9Semantics, FAIL) Two reproduced gate-v2 defects: (a) a linear delete-then-re-add history
   changes v2's timing/exit versus v1, so "on linear histories v1 and v2 agree byte-for-byte" holds only
   for rows without a re-add (the lane has none — lane parity stands); (b) when the first parent lacks the
   path, the ref falls through to the second parent's state, which contradicts P-C9's "first parent's
   state" for merges. Routed: eligible-set/refinement semantics as a new gate version or narrowed prose,
   next attempt.
6. (w1/RevC9Walk, MEDIUM) `evidence/c9-after-lane.txt` walk counts (53/52) name no rev; at the landed tip
   the counts are 54/53 (the +1 is this round's own data commit). The 6531ac60 simplification finding
   stands. Amended receipt names the measured rev (committed alongside).
7. (w1/RevC9Live + RevCensus, notes) contract prose `pass=11` is stale (selftest prints 12); the
   "18 ids + S226" prose overclaims (eligible set is edit-bounded — see finding 2 above). Receipts
   themselves are honest.
8. (w1/RevC8Drain, HIGH) drain_shape never binds a communicate to a Popen: any used communicate in a
   function drains every Popen in it, so the r38 M19-B shape (wait+read on the tool child) passes with a
   decoy `out, err = dummy.communicate(timeout=…)` in the same function; `_ = proc.communicate(...)` and
   tuple-wrapped results also pass as "used"; the rule is per-function, not per-Popen. C2's frozen claim is
   untouched (the routed fixture has no decoy); the drain_shape clause is not what P-C8's words claim.
   Routed to round 40 with the seat's variants under `w1/RevC8Drain.md`.
