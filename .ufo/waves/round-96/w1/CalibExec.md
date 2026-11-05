# CalibExec — mori round 96, wave w1 — C1 calibration counter

Seat: CalibExec (executor). Scope: build and measure the NEW unbounded C1 counter per frozen
predicate P1; detection and report only. SCORECARD.md untouched by this seat.

## Files written (all under the lane, wave-owned paths only)

- `.ufo/waves/round-96/w1/calib/mori-scorecard-calibration.py` — the counter (stdlib only;
  CLI `<rev> [--manifest PATH] [--repo DIR] [--base REV] [--selftest]`; defaults per spec;
  exit 0 met / 1 unmet / 2 setup; honors TMPDIR, /tmp never hardcoded; the r79 counter is not
  amended). The L1 promotes it to `tools/mori-scorecard-calibration.py` after integration.
- `.ufo/waves/round-96/w1/calib/selftest.txt` — receipt (a): `CALIB_SELFTEST pass=11 fail=0`, `exit=0`.
- `.ufo/waves/round-96/w1/calib/base-run.txt` — receipt (b).
- `.ufo/waves/round-96/w1/calib/head-run.txt` — receipt (c).
- `.ufo/waves/round-96/w1/calib/derived-cells.txt` — receipt (d): expected leads for the L1.

## Counts (the three the task asks for)

1. Selftest: `CALIB_SELFTEST pass=11 fail=0`, exit 0. Eleven arms (spec minimum six):
   conformant met; stale cell (operability r78 cell vs r93 admitted expectation) unmet;
   not-admitted higher round (r100 admitted:false improved) ignored → met; verdict word
   missing before `;` unmet; duplicate axis row → state=error, unmet; Score cell changed vs
   base → columns_unchanged=no, unmet; plus Evidence-cell changed, cell-without-round,
   no-admitted-expectation (expect=none), verdict-word disagreement, and unreadable-manifest
   exit 2. Fixtures are real git repos built under TMPDIR with a toplevel assertion before any
   fixture git mutation.
2. Base run `python3 .ufo/waves/round-96/w1/calib/mori-scorecard-calibration.py
   66c5518e239eeacd6070be26d78085ef702392cb` → per-axis lines then
   `C1=unmet axes=6 mismatches=5 columns_unchanged=yes rows=6 rev=66c5518e239e`, exit=1.
   Mismatches: coverage cell r56 vs r80, operability r78 vs r93, depth r76 vs r86, freshness
   r78 vs r82, calibration r78 vs r93; adjacency ok (r19 = r19). This is exactly the
   contract's before = 5 mismatches (contract §C1 before receipts list the same five axes).
3. HEAD run `python3 .ufo/waves/round-96/w1/calib/mori-scorecard-calibration.py HEAD` →
   `C1=unmet axes=6 mismatches=5 columns_unchanged=yes rows=6 rev=b88c8ae8ff85`, exit=1.

## Note on HEAD (deviation from the task's assumption)

The task said "HEAD resolves to the same tip" as 66c5518e. Actual lane HEAD is
`b88c8ae8ff85d1cb7df81fffef2f46a0512e76b5` — the freeze commit itself ("round-96: freeze
contract, before receipts, wave-1 spec and dispatch"), one commit after the entering sha;
`66c5518e` is its ancestor. `git diff --stat 66c5518e HEAD -- SCORECARD.md` is empty, so
SCORECARD.md is byte-identical at both revisions and both runs report the same 5 mismatches
with columns_unchanged=yes. Recorded sha12: `b88c8ae8ff85`. No action needed by the L1.

## Receipt (d) — derived cells for the L1

Expected leads (all `improved`): coverage round 80, operability round 93, depth round 86,
freshness round 82, calibration round 93 — these are exactly the contract's expected landing
cells. adjacency round 19 already matches. Edit rule: replace only the text before the first
`;` of each Last change cell; never move Score or Evidence pointer cells (COLUMNS_UNCHANGED).
At a correct landing the counter prints
`C1=met axes=6 mismatches=0 columns_unchanged=yes rows=6` and exits 0.

## Implementation notes / honest history

- The counter's expectation engine was cross-checked against the fleet MANIFEST directly:
  58 admitted lane:mori integer-round rows; highest grading axes improved/harmed are
  coverage 80, operability 93, depth 86, freshness 82, calibration 93, adjacency 19.
- Only iteration during the seat was in `--selftest` fixtures: the first run crashed because
  the conformant arm writes identical SCORECARD.md bytes at base and rev, so the second
  fixture commit had nothing to stage (`nothing to commit`, rc=1, message on stdout). Fixed
  with `--allow-empty` on fixture commits (which also mirrors the real lane, where
  SCORECARD.md is identical across the freeze boundary). `measure()` was never changed after
  its first write; receipts (b)/(c) were regenerated after the fix and are from the final file.
- Selftest fixture commits run only inside scratch fixtures (toplevel asserted); no git
  mutation anywhere in the lane or fleet root. No installs (system python3 3.14.8, system git).

## Unrun checks (named, not assumed)

- No run at a landing revision with edited cells (this seat must not edit SCORECARD.md); the
  met path at tip is only proven by selftest fixtures.
- No re-verification of the frozen r79 counter (`--through 95`) — its before receipt already
  exists at `evidence/before-c1-count-c2-through95.txt` per contract.
- No freshness (C2) work — different seat.

## Risks / blockers

- None blocking. The counter pins expectations to the current fleet MANIFEST.json bytes; if a
  later admitted mori closure lands during integration (e.g. round 94+ grading these axes),
  expectations move and the L1 must re-run the counter before editing cells.
- Summary `rows=R` counts parsed axis rows (6 on any healthy scorecard); duplicate or missing
  axis rows yield state=error, C1=unmet, exit 1 — by design distinct from mismatches.
