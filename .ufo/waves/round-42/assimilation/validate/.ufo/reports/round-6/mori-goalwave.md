# mori round 6 — goal-wave delivery report

Status: **ADMITTED with correction** (round 6). Evidence commit: `92b2e42`
(records commit follows). Baseline: `848b3a6` (round-5 records). Wave: one
32-seat flash call, 33/33 reports. Report time: 2026-10-15 ~19:25Z.

## Work performed

- Selected axis **operability** — the round-5 residuals: R1 stdout backchannel,
  R2 content-keyed forgery.
- 32-seat wave shipped the closures, attacked them from five directions, and
  pinned the honest boundaries.

## Landed changes (evidence commit `92b2e42`)

- `tools/mori-silence-cases.sh` → `3307761a…`: run header after the case loop;
  `redact()` strips the nonce token from echoed fragments; pinned-seed re-exec
  (env pins passed via pipe fd, dropped before any census exists); per-run
  `RUN_SALT_HEX` in every committed body; random `blob-*` payloads outside
  graded trees. Registry byte-identical (28 ids/wants); exit contract 0/1/2;
  shape-invariance retained.
- `corpus/knowledge/verdict-machine-r6.md`; lesson
  `corpus/lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md`;
  seven receipts `backchannel-r6-20261015T191216Z-*.log` incl. the two attack
  receipts; README/SKILL rows.

## Before → after measurements (parent acceptance, 2026-10-15T19:20Z)

| Check | Before (`7143ccc2…`) | After (`3307761a…`) | Exit |
|---|---|---|---|
| R1 fd/environ backchannel | 28/28 faked | attacker 0–1/28 (probe 29/29 zero hits); header at line 29/32 | 1 |
| R2 content memorizer | 28/28 faked | fails at salt-discriminating cases | 1 |
| honest census | 28/28 | 28/28 ×2 byte-identical (parent), distinct orders | 0 |
| selftest / live census | — | 30/30; `DRIFT findings=15 drift=14 unavailable=1` | 0/1 |

## Corrections and honest boundaries

1. Mid-wave the claim did NOT hold (first revision `9ce164ec` still leaked via
   environ); the re-exec revision closed it. Acceptance pins final bytes only.
2. **Full-grammar normalizer** residual: strips nonce/salt shapes AND excludes
   `salt-*`/`blob-*` keys → still 28/28. Finite fixtures + deterministic
   grades are memorizable in principle; anti-forgery here is depth, not
   impossibility (`verdict-machine-r6.md`).
3. Ancestor-environ pin hygiene (`MORI_SHUFFLE_SEED` visible via a surviving
   parent) is operator-side, named.
Round 7 (registered): coverage — the round-2 surface gaps (tmux session
relevance, memory-pressure threshold, disk write-rate, `state_rounds`
count-only). The verdict-machine arc r3–r6 is complete.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]`: no named non-author
  verifier; wave seats are the lane per protocol.

Boundaries held: detection and report only; no remediation/kills/config edits;
fixtures under `/tmp`; seats made no commits; fleet root read-only for seats.
