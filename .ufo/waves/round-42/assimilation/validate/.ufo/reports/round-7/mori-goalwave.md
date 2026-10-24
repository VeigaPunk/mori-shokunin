# mori round 7 — goal-wave delivery report

Status: **ADMITTED** (round 7). Evidence commit: `d30b4e4` (records commit
follows). Baseline: `80a80f6` (round-6 records). Wave: one 31-seat flash
call, 31/31. Report time: 2026-10-15 ~20:15Z.

## Work performed

- Selected axis **coverage** — the round-2 pivot: close the four measured
  surface gaps (tmux relevance, memory pressure, disk write-rate, state_rounds
  values).
- 31-seat wave implemented all four probes (census r4), re-baselined the oracle
  additively, tested each gap live and with stubs, and named the residuals.

## Landed changes (evidence commit `d30b4e4`)

- `tools/mori-census.sh` → r4 `c7c3569b…`: tmux relevance rule
  (`rule=pane_cwd_under_fleet_root`); memory PSI (`psi_some/full_avg10`) +
  cgroup fill + host avail (thresholds labeled local); disk since-boot average
  rates per target device (`io_avg_since_boot`, honest `io_avg_unavailable`);
  state_rounds per-value read with `WATCHDOG_STATE_LAG`/`AHEAD` info findings;
  `local_oom_kill=` disclosure on the cgroup row; selftest 30 → 45.
- `tools/mori-silence-cases.sh` → `448f7723…` (additive-only re-baseline; the
  28 ids/wants and every grade semantics unchanged; verifier seats confirmed).
- `corpus/knowledge/surfaces-r7.md`; `observability-surfaces-r2.md` gap
  sections updated; lesson `2026-10-15-free-lunch-measurements-counter-baselines.md`;
  seven receipts `surfaces-r7-20261015T1948Z-*.log` (per-gap + selftest +
  oracle + live); README/SKILL rows.

## Before → after measurements (parent acceptance, 2026-10-15T20:10Z)

| Check | Before (`af2d4e79…`) | After (`c7c3569b…` / `448f7723…`) | Exit |
|---|---|---|---|
| selftest | 30/30 | 45/45 (+15, none removed) | 0 |
| oracle | 28/28 | 28/28 ×2 (additive re-baseline) | 0 |
| tmux row | `sessions=N` count only | relevance classification + unavailable handling | — |
| cgroup row | counters only | PSI + fill + host avail + local_oom disclosure | — |
| disk row | point-in-time df | since-boot avg rates + honest deferral disclosure | — |
| watchdog row | count-only state_rounds | per-value lag/ahead vs ledger (info severity) | — |
| live | `DRIFT findings=15…` | `DRIFT findings=15 drift=14 unavailable=1` (tmux unavailable, no server) | 1 |

## Honest residuals (named in `surfaces-r7.md`, round-8 registered)

1. Instantaneous write-rate: deferred with precondition (measure the
   double-sample wall-time cost; implement only if cheap).
2. tmux per-session freshness: not claimed.
3. `*.round` symlink/dir invisibility in the values probe.
4. Memory-tester's three residual items (see the seat report / note).

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: detection and report only; host measurement read-only; no
remediation/kills/config edits; fixtures under `/tmp`; seats made no commits;
fleet root read-only for seats.
