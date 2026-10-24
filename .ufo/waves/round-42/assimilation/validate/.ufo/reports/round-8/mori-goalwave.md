# mori round 8 — goal-wave delivery report

Status: **ADMITTED with correction** (round 8). Evidence commit: `9738f1a`
(records commit follows). Baseline: `ed9de46` (round-7 records). Wave: one
31-seat flash call, 31/31. Report time: 2026-10-15 ~21:10Z.

## Work performed

- Selected move: close the four `surfaces-r7.md` residuals.
- 31-seat wave disposed each with measurements, proved additive-only (no
  oracle rebase needed), and measured a harness flake.

## Landed changes (evidence commit `9738f1a`)

- `tools/mori-census.sh` → r5 `390ab9cd…`: write-rate deferral on measured
  numbers (+213 ms median, min 4.2× budget — header `:76-97`); tmux
  per-session freshness probe (bounded, `freshness/probed/idle/idle_warn_s`);
  `state_val_unread_reasons=file/symlink/dir/other` diagnosis; memory-residual
  dispositions; selftest 45 → 56.
- `corpus/knowledge/surfaces-r8.md`; `surfaces-r7.md` residual pointers;
  lesson `2026-10-15-probe-pricing-dwell-bounds-filter-drop.md`; eight receipts
  `residuals-r8-20261015T2040Z-*.log`; README/SKILL rows.

## Before → after measurements (parent acceptance, 2026-10-15T21:05Z)

| Check | Before (`c7c3569b…`) | After (`390ab9cd…`) | Exit |
|---|---|---|---|
| selftest | 45/45 | 56/56 ×2 + determinism 7/8 (flake below) | 0 |
| oracle | 28/28 (`448f7723…`) | 28/28 ×2 — NO rebase needed (additive-only field diff: 4 new names, none lost) | 0 |
| write-rate | since-boot only | since-boot + measured deferral (+213 ms median, rule-adjudicated) | — |
| tmux | relevance only | per-session freshness, no-hang canary | — |
| state files | values only | values + reason-coded unreadable diagnosis | — |
| live | `DRIFT findings=15…` | same aggregate; new fields on watchdog/cgroup/disk rows | 1 |

## Defect at admission (round 9's registered top debt)

Selftest harness flake: grep-over-pipe SIGPIPE race at
`tools/mori-census.sh:1783/:1809` — measured 1/8 (parent) and ~25% (one seat
battery); every false-FAIL a different case, green on rerun. Round 9:
root-cause and eliminate the race; ≥20-run battery at 0 flakes; selftest 56
green; oracle 28/28; zero probe-behavior change.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: detection and report only; host measurement read-only; stubs
slept only inside /tmp fixtures; no remediation; seats made no commits; fleet
root read-only for seats.
