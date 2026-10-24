# mori round 4 — goal-wave delivery report

Status: **ADMITTED with correction** (round 4). Evidence commit: `5b62c897`
(records commit follows). Baseline: `bbcc1ad` (round-3 records). Wave: one
32-seat flash AgentSwarm call, 32/32 completed. Report time: 2026-10-15
~18:00Z.

## Work performed

- Selected axis **operability** — the registered round-3 debt: trustworthy
  verdict machine end-to-end.
- The 32-seat wave implemented both fixes (two sole-writer seats), tested every
  branch (12 close sequences, state-dir variants, sniffer v1/v2/v3, shape
  invariance, six regression batteries), and documented the mechanisms.

## Landed changes (evidence commit `5b62c897`)

- `tools/mori-silence-cases.sh` → `be0e28b8…`: `want_match` exact-string
  alternation matcher (replaces the `case … in $want)` literal-`|`
  defect — the round-3 25/27 cap); opaque per-case `mktemp -d` fixture dirs (no
  case id in any census-visible path); `MORI_FIXTURE` no longer exported; new
  case 28 `shape-invariance` (same fixture under two dir names, byte-identical
  grades required). All 27 pre-registered ids/wants byte-identical (registry
  guard).
- `tools/mori-census.sh` → `af2d4e79…`: `:225-228` `state_n` bare pipeline
  rc-gated (chmod-000/missing/empty state dir → full verdict, honest surface
  state, 3 new selftest cases); close tracking per anchor round (`complete r7;
  complete r5` no longer closes the r7 anchor; 2 new selftest cases; 12
  monotone + adversarial sequences held). Selftest 25 → 30.
- `corpus/knowledge/verdict-machine-r4.md`; `corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md`;
  five receipts (`verdict-r4-20261015T173551Z-{canary227,live,oracle,selftest,sniffer-v2}.log`)
  indexed in `corpus/evidence/README.md`; `corpus/README.md` rows.

## Before → after measurements (parent acceptance, 2026-10-15T17:55Z)

| Check | Before | After | Exit |
|---|---|---|---|
| oracle vs census | `matched=25 total=27` (matcher cap) | `matched=28 total=28`, ×2 byte-identical (parent), ×3 (seat) | 0 |
| case-id sniffer census | faked `27/27` exit 0 | 1–2/28 (channel closed) | 1 |
| path-shape sniffer | n/a (pre-hardening) | 27/28 — caught by `shape-invariance` | 1 |
| `:227` chmod-000 `.ufo/state` | rc 1, header only, 0 verdicts | full verdict + honest surface state + canary receipt | 0/1 |
| `complete r7; complete r5` | closed-r7 anchor misgraded silent | per-anchor-round close: `not-open` | 0 |
| selftest | 25/25 | 30/30 | 0 |
| live census | — | `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`, 9/9 progressing, 0 `LANE_SILENT` | 1 |

## SHONEN

- [ ] decision tables (r2/r4 contract sections landed; verification owed)
- [ ] end-to-end task logged (r1–r4; owed)
- [ ] executable without oral context (owed)
- [ ] no cross-domain bleed (scope-sentinel clean all rounds; owed)

All four remain unchecked: no named non-author verifier; wave seats are the
lane per protocol.

## Correction and named debt (round 5 registered claim)

The claim's "a sniffer attempt cannot fake a pass" holds **only** for the
case-id/path channel. A run-order sniffer (critic's v3: canned grades keyed on
deterministic invocation order, zero fixture bytes) still reaches 28/28 exit 0.
Round 5 claim: close the run-order channel (per-run case-order shuffle and/or a
run nonce the census cannot predict, while keeping in-run determinism), verify
sniffer-v3-class attacks fail, and keep the full 28/28 honest tally green.
Carried unchanged: drift pin; row-6 presence-only residual; blocked-attempt
receipt-binding + role-routing debts.

Boundaries held: detection and report only; no remediation/kills/config edits;
fixtures under `/tmp`; seats made no commits; fleet root read-only for seats.
