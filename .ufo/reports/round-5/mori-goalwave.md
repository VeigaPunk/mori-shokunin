# mori round 5 — goal-wave delivery report

Status: **ADMITTED with correction** (round 5). Evidence commit: `a420deb7`
(records commit follows). Baseline: `7a3629a` (round-4 records). Wave: one
32-seat flash call, 32/32. Report time: 2026-10-15 ~18:35Z.

## Work performed

- Selected axis **operability** — the round-4 correction's residual: run-order
  spoofing channel.
- 32-seat wave shipped seeded shuffle + run nonce, ran the four-group
  order-pair independence probes, and hunted the remaining spoof surface.

## Landed changes (evidence commit `a420deb7`)

- `tools/mori-silence-cases.sh` → `7143ccc2…`: seeded Fisher–Yates case
  execution (xorshift32; `SHUFFLE_SEED`/`CASE_ORDER` logged; seed never
  exported; `MORI_SHUFFLE_SEED` pins); per-run `RUN_NONCE` via env + fixture
  file + disk-target dir `nonce-<N>` (census echoes it in its disk row); every
  case requires the literal nonce token (stale/missing →
  `canned/replayed output?`). Registry byte-identical (28 ids/wants).
- `corpus/knowledge/verdict-machine-r5.md`; lesson
  `corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md`; six
  receipts `order-r5-20261015T180431Z-*.log` (incl. per-run seeds/orders)
  indexed in `corpus/evidence/README.md`; README/SKILL rows.

## Before → after measurements (parent acceptance, 2026-10-15T18:30Z)

| Check | Before (`be0e28b8…`) | After (`7143ccc2…`) | Exit |
|---|---|---|---|
| invocation-count canned sniffer | 28/28 faked | 0/28 | 1 |
| stale-nonce replay | n/a | 0/28 | 1 |
| adaptive positional + live-nonce echo | n/a | 8/28 | 1 |
| env-reading sniffer-v4 | n/a | 10/28 | 1 |
| honest census across shuffles | — | 28/28, different orders, grade tuples byte-identical | 0 |
| inter-case independence | n/a | 4 pair-groups, no state leakage | 0 |
| selftest / live census | — | 30/30; `DRIFT findings=15 drift=14 unavailable=1` | 0/1 |

## Corrections named (round 6 registered claim)

- **R1 stdout-backchannel:** the census reads `CASE_ORDER`/`RUN_NONCE` from the
  oracle's own stdout via `/proc/<ppid>/fd/1` (or `environ` on pinned runs) and
  replays by position — still 28/28 exit 0. Fix: print the run header AFTER the
  case loop (no living SUT invocation can read the order/nonce from the log).
- **R2 content-keyed forgery:** memorized content→state tables still pass; the
  nonce binds no fixture content. Fix: embed the nonce in fixture content
  (committed file bodies / ledger lines carry `nonce-<N>`).
Round 6: implement both, verify the R1/R2 attackers fail, keep 28/28 honest
green, zero regression.

## SHONEN

- [ ] decision tables · [ ] end-to-end task logged · [ ] executable without oral
  context · [ ] no cross-domain bleed — all remain `[ ]`: no named non-author
  verifier; wave seats are the lane per protocol.

Boundaries held: detection and report only; no remediation/kills/config edits;
fixtures under `/tmp`; seats made no commits; fleet root read-only for seats.
