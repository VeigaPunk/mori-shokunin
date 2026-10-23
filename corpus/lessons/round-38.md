# Round 38 — 2026-10-23 (L1 MoriR38, attempt 1)

## Gate

Candidate this round (one, opened 2026-10-23; copy under `corpus/evidence/sources-r38/`):

| candidate | decision | URL, access date, located quote (≤25 words) |
|---|---|---|
| S226 — Python `os.path.realpath` documentation | **admitted** (mined) | `https://docs.python.org/3/library/os.path.html#os.path.realpath`, opened 2026-10-23; `S226.src:657-658`: "Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system)." |

Rejected: none new. The row's `teaches` opens `supersedes S069`: S069 was edited in place at
`62db24c` (round 33) and its only superseder S073 had landed at `71abd41` (round 20), before the
edit; S226 restates the containment rule on a source opened this round and lands after `62db24c`.
Registry changes old→new: none (S226 is new; no existing row's `status`, `recheck` or `used-by`
cell was edited). Census: `sources-census.sh validate mori` exit 0 at round start and round end,
benign W04 lines only (`evidence/census-start.txt`, `census-end.txt`).

Search log: appended as "Round 38 bounded search" in `corpus/SOURCES.md` (question, where, date,
identified 1 / screened 1 / included 1 / excluded 0, stop rationale).

## Mistakes

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | tooling (a path token stripped of its leading dot) | `count-c4.py`'s first run at `e37dcc6` printed `paths=['ufo/waves/round-37/evidence/c2-after.txt', 'evidence/drift-live-r37.txt']` — `.strip(".,;)")` removed the leading `.` of `.ufo/...`, so the check reported a path missing that exists | the counter's own capability detail line; no criterion named it before | `token.strip().rstrip(".,;)")`; re-run prints `.ufo/...` and only `evidence/drift-live-r37.txt` missing (the genuine mixed-base defect). Shown able to fail: the pre-fix line is quoted above; the post-fix line is `evidence/c4-before.txt` |
| M2 | measurement (negatives judged against an already-failing baseline) | at `e37dcc6` all three fabricated witnesses print `rejected`, but the capability check already fails on the real bytes, so the before receipt does not isolate any witness | the L1's own read of the before receipt; no criterion named it | the discrimination control is a clone of the scored tip with the three witnesses committed (`fixtures/make-witness-sandbox.py`): the r37 counter prints `C2=met` there, `count-c4.py` prints `C4=unmet` (`evidence/v3-token-control.txt`, `evidence/c4-witness.txt`). Shown able to fail: a counter without the anchor check would accept the token witness, exactly as the r37 counter does |
| M3 | tooling (a landing index updated to the newest state instead of the first landing) | the first gate patch printed `stale_supersede=[]` at `e37dcc6`, i.e. S069 looked as-of although S073 landed 4,000+ path commits earlier: `if index > previous[0]` overwrote the first landing on every later state | the L1's cross-check against the known commit order (S073 `71abd41` < S069 edit `62db24c`); the selftest fixture passed because it has only two states | record the first landing per `(target, superseder)` and take the maximum across superseders. Shown able to fail: pre-fix `stale_supersede=[]` vs post-fix `stale_supersede=[S069]` at `e37dcc6` (`evidence/gate-after.txt`); the new selftest case has the superseder in the base state |
| M4 | tooling (the gate's own printed predicate read as a per-id line) | `--selftest` failed 9/9 with `per-id line malformed: "P-C6: …"` after the predicate line was added | the selftest run itself | the selftest filters the `PREDICATE` line before the per-id grammar pass; `MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=0`. Shown able to fail: the quoted 9/9 failure text |
| M5 | measurement (conformance mutations that were not load-bearing) | `CONFORM_SELFTEST pass=2 fail=4`: the predicate mutation only added whitespace (normalisation erased it), the tool-resolution mutation resolved from the checker's lane cwd, and the timeout mutation hit a `def` signature | the checker's own selftest | mutations target non-whitespace bytes, the resolver's return expression, and the bounded `run(` helper; `CONFORM_SELFTEST pass=6 fail=0`. Shown able to fail: the pre-fix selftest line is quoted above |
| M6 | wave design (a bounded planning data-walk can ride a scout/connector item) | the round prompt's planner seat is a frozen-topology role the validator rejects; the L1 holds the canonical planner seat and this round's only planning walk is the L1's own claim design | the validator's role list (round 37 M8 class) | recorded here and in the report; no planner role was dispatched |

## Round shape and debts

Round shape (orchestrator-inline contract): one validated v2 wave prepared and returned to the
orchestrator for inline dispatch; the L1 built the frozen artifacts (contract, three instruments,
fixtures), the corpus rows/entries and the receipts. See the round report for the wave accounting.

r37 routed items: (1) erratum + LOG amendment → commit `3501d4c2` + `corpus/lessons/round-37-erratum.md`;
(2) axes cells → SCORECARD correction note; (3) content half → claim C1; (4) SentTools MEDIUM/LOW →
claim C2; (5) predicate/pin → claim C2; (6) before-receipt form → C2 + `evidence/c1-before-rerun-*.txt`;
(7) capability first-working → SCORECARD 37 → 36 with the r37 narrowing; (8) debt (f) SIGTERM→grace→
SIGKILL → named, not decided: L0 question appended and the LOG amendment says OPEN/operator-owned;
(9) QUALITY 103 second clause → `dispatch-log.txt` records the index-clean check after each `landed`
line; (10) count-c2 scratch → claim C2 (`scratch` check).
ExecGateRound routed items: (a) S069 → claim C3 + S226; (b) predates-the-change gap → claim C3;
(c) `gen-w2-spec.py` recipe → the two superseded lines are rewritten and the superseded text is
named in the round report (the recipe said "18 ids QUALITY 104 names" and `grep -c 'supersedes S0'`).

Misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain` was run before the report;
see the report's Misroot line.

## Known residuals

- `count-c4.py` has no `--selftest`; its able-to-fail evidence is the witness sandbox and the
  `drift_kill` mutation arm (recorded as `count-c4.py`'s shape in QUALITY 108's Not-covered line).
- The gate's timing field is commit-order in the path's history, not global ancestry.
- Debt (f) is operator-owned; the counters still SIGTERM then SIGKILL after the 5 s grace.
