# mori round 18 (recovery attempt 2) — declared claims and interfaces

Frozen before any round-18 implementation by MoriR18Recovery (L1, sole integration
owner). Entering branch tip `d005cdde0e009dea6c0cc29b37163de536528658` (round-17
non-author spot-check). Attempt 1 (launch 2026-10-20T18:52:38-03:00, lane-dead-no-report
2026-10-21T02:47:20-03:00) left no lane files, no wave directory, no worktrees and no seats:
nothing is reused and nothing needs discarding.

## Repair first (routed by `corpus/lessons/round-17-verifier-spotcheck.md:388-417`)

1. Privacy retention (blocking): minimize the three named build reports and every repeated
   mention found by a whole-tree sweep; lesson + QUALITY criterion on minimizing committed
   handoff material. History is not rewritten; exposure assessment stays operator/kagi-owned.
2. Freeze/calibration: no round-17 item is labelled pre-build; round-18 requirement
   universes are frozen in this commit, before any implementation commit.
3. Scope enforcement: concrete pre-action VCS/scratch/field-projection bounds in every wave
   context (V1–V3, V5–V14, L1 authorization) — instruction text, not runtime prevention.
4. Evidence provenance: per-attempt payload binding of every dispatch attempt (C3).
5. Inherited gate debt: r10 red and r13–r16 qualifications stay open and named; no repin.
6. Package/boot-chain events: detection-only handoff to operator/tsukuroi.

## Claims (each causally separable; frozen inputs under `frozen/`)

**C1 — adjacency (sourced): committed private-context retention.** Gate
`tools/mori-retention-gate.py` over policy `frozen/c1-policy.json`. Count = unallowlisted
class hits in tracked blobs at the measured revision, excluding non-author files.
Before (frozen enumeration `frozen/c1-population.json` at d005cdd): 116 (routed files 40).
Target after: 0, with the three routed files at 0 hits and no allowlist entry for them.
Failure-capable: the gate must exit 1 at d005cdd and on synthetic planted fixtures.

**C2 — calibration (lowest non-retired axis, tie at 5): freeze-order discernment.** Tool
`tools/mori-freeze-order.py` over `frozen/c2-register.json`. Count = uncorrected
pre-build overclaims. Before at d005cdd: 1 (r17-C3 "precommitted", five locations);
oracle agreement with the non-author r17 rulings must be 3/3. After: 0 overclaims via an
appended correction row in `corpus/evidence/freeze-register.json`, and r18-C1..C3 verify
`pre-build` against this freeze commit. Failure-capable: a co-committed fixture must grade
`co-evolved`.

**C3 — operability: per-attempt dispatch payload binding.** Tool
`tools/mori-dispatch-ledger.py` over ledger format `frozen/c3-ledger-format.json`. Count =
unbound attempt rows. Before: round-17 wave1/wave2 attempt receipts (legacy, no payload
digest). After: round-18 `wave*-attempts.json` ledgers. Failure-capable: tampered payload,
mismatched digest, non-final or duplicate started row each verify unbound/failed.

## Executor interfaces (each executor owns exactly one tool file + its fixtures)

All three tools: Python 3 stdlib only; read-only over the lane (git `ls-tree`, `cat-file`,
`rev-list`, `diff-tree`, `show` only; `-C <repo>`); exit 0 clean, 1 findings/failed,
2 could-not-evaluate (bad input, missing rev, tampered snapshot); `--selftest` builds
isolated fixtures under `$TMPDIR` (set by the caller to the executor's own clone
`.scratch/`), asserts exit code + stable finding id per arm, prints `SELFTEST <name>
PASS n/n`; JSON output on stdout; never prints matched private text (only path, line,
class, SHA-256).

- `tools/mori-retention-gate.py scan --repo R --rev REV --policy P [--allowlist A]`:
  implements `frozen/c1-policy.json` exactly; must reproduce `frozen/c1-population.json`
  hit-for-hit at d005cdd (compare `--expect-population`). Allowlist rows: `{path, class,
  line_sha256, reason, rule:a|b|c}`; an allowlist row for a `must_redact_paths` file is
  itself a finding `allowlist_forbidden`; a stale allowlist row (no matching hit) is
  reported `allowlist_stale` (warning, not failure). `--frozen-run` checks the committed
  snapshot digests (`snapshot_tampered` => exit 2).
- `tools/mori-freeze-order.py check --repo R --register F [--corrections C] [--tip-for
  ID=REV ...]`: implements `verdict_rule` and `label_rule` of `frozen/c2-register.json`;
  prints per-claim verdict, co_committed, effective label, overclaim, oracle_disagreement
  and totals.
- `tools/mori-dispatch-ledger.py verify --repo R --rev REV --ledger PATH` and `bind`
  helper that prints the row fields for a dispatch JSON: implements
  `frozen/c3-ledger-format.json`; also accepts the round-17 legacy attempt arrays
  (counting their rows unbound).
