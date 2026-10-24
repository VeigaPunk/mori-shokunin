# mori round 10 — goal-wave delivery report

Status: **ADMITTED** (round 10). Evidence commit: `5be8943` (records commit
follows). Baseline: `6a549b9` (round-9 records). Wave: one 29-seat flash
call, 29/29. Report time: 2026-10-15 ~22:45Z.

## Work performed

- Selected move: the drift pin (carried since round 2) — the census's own
  behavior becomes a measured surface.
- 29-seat wave implemented `--pin`/`--drift` with a declared volatile
  contract, committed the lane baseline, and attacked the mask from both
  sides (over/under-masking).

## Landed changes (evidence commit `5be8943`)

- `tools/mori-census.sh` → `d7710981…`: `--pin <path>` (normalized baseline,
  volatile list recorded in the header), `--drift <path>` (`none` exit 0 /
  named changes exit 1 / missing-malformed exit 2); selftest 56 → 66 (+10).
- `corpus/evidence/baseline-r10-20261015T2231Z.json` (THE lane baseline) +
  five receipts `pin-r10-20261015T2231Z-*.log`; `corpus/knowledge/drift-pin-r10.md`;
  lesson `2026-10-15-volatile-contract-behavioral-baselines.md`; README/SKILL rows.

## Before → after measurements (parent acceptance, 2026-10-15T22:40Z)

| Check | Before (`1c49238a…`) | After (`d7710981…`) | Exit |
|---|---|---|---|
| selftest | 56/56 | 66/66 | 0 |
| drift vs committed baseline | n/a | `MORI_DRIFT: none` | 0 |
| injected regression | n/a | names exactly the field (`warn_pct`, `-SURFACE:disk`, `VERDICT`…) | 1 |
| oracle | 28/28 | 28/28 — oracle frozen, default output byte-identical | 0 |
| live | `DRIFT findings=15…` | `DRIFT findings=15 drift=14 unavailable=1` | 1 |

## Named (not claimed away)

Unmasked state words (`rc=`, `log=`, surface states) legitimately flip with
host state — a future red drift may be baseline aging; the re-pin policy is
in `drift-pin-r10.md`. Round 11 (capstone, operator-directed): full-lane deep
audit on `openai-codex/gpt-6.1-sol` (32 seats) — evidence-chain verification,
debt adjudication, SHONEN readiness assessment, and re-execution of the four
most load-bearing historical claims.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol). The r11 audit assesses
  readiness without self-attesting.

Boundaries held: detection and report only; fixtures `/tmp`; seats made no
commits; fleet root read-only for seats.
