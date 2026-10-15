# mori round 9 — goal-wave delivery report

Status: **ADMITTED** (round 9). Evidence commit: `cffb37e` (records commit
follows). Baseline: `c47c888` (round-8 records). Wave: one 28-seat flash
call, 28/28. Report time: 2026-10-15 ~21:55Z.

## Work performed

- Selected axis **operability** — the round-8 named debt: selftest harness
  flake (grep-over-live-pipe SIGPIPE race).
- 28-seat wave root-caused the race to rc=141 anatomy, fixed all six
  live-pipe-grep sites (capture-once-then-grep-file), and proved 0-flake
  across 70+ runs including loaded batteries; two seats independently dated
  the defect's introduction (it predates r8).

## Landed changes (evidence commit `cffb37e`)

- `tools/mori-census.sh` → `1c49238a…` (VERSION stays `census-r5`; production
  output byte-identical): `OUT_FILE` capture in `run_selftest()`; six sites
  converted; zero pipelines added; the two kept pipes are read-all,
  outside the class. Diff 21/7, all inside the selftest path.
- `corpus/knowledge/selftest-flake-r9.md` (mechanism, anatomy, pattern,
  archaeology, batteries); receipts `flake-r9-*` indexed in the evidence
  README; README/SKILL rows.

## Before → after measurements (parent acceptance, 2026-10-15T21:50Z)

| Check | Before (`390ab9cd…`) | After (`1c49238a…`) | Exit |
|---|---|---|---|
| selftest flake | 1/8–25% false-FAIL | mechanism 0/60000; batteries 20/20 + 20/20 (loaded) + parent 10/10 | 0 |
| selftest cases | 56 | 56 (names byte-identical) | 0 |
| oracle | 28/28 | 28/28 — oracle byte-FROZEN, wants unchanged | 0 |
| live | `DRIFT findings=15…` | `DRIFT findings=15 drift=14 unavailable=1` | 1 |

## Round 10 registered (the long-carried drift pin, freshness)

`--pin` writes a committed behavioral baseline (full census output with a
declared volatile-fields list: ts/age/counter fields); `--drift` diffs a fresh
run against it and reports behavioral deltas beyond the volatile list.
Selftest cases + receipts; oracle held green.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: detection and report only; load hogs killed by their seats;
fixtures `/tmp`; seats made no commits; fleet root read-only for seats.
