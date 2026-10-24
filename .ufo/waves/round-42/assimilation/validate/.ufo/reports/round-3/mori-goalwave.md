# mori round 3 — goal-wave delivery report

Status: **ADMITTED** (round 3). Evidence commit: `1439c47` (records commit
follows). Lane baseline: `3da8414` (round-2 admission). Wave: one 32-seat flash
AgentSwarm call (24 completed) + an 8-seat backfill for the seats lost to a
provider content-filter false positive (8/8). Report time: 2026-10-15 ~17:30Z.

## Work performed

- Selected axis **coverage** — the registered round-2 debt: land the r2
  `probe_silence` in `tools/mori-census.sh` per
  `corpus/knowledge/silence-grading-r2.md`.
- The 32-seat wave implemented, reviewed, tested, and documented the cutover;
  the backfill completed the spec cross-checks, adversarial probes, and
  integration drafts after the cascade-shim content-filter fix (see LOG for the
  diagnosis: alibaba-token-plan `data_inspection_failed` was a terminal 400;
  both flash shims now fall through it to the next leg).
- Parent (L1) ran acceptance at integration; every figure below was re-measured,
  not quoted.

## Landed changes (evidence commit `1439c47`)

- `tools/mori-census.sh` → census r2, sha256
  `fe22a14f0bb6d90ffed14506abfcd76153ebf31cf3cb769b97e7eec61cc2f3c9`:
  launch-anchored, authorship-aware `probe_silence` (per-lane rows, six states,
  rows A–D, closure predicate, strict age gate, `LANE_SILENT` row-D only,
  `unavailable` ≠ unhealthy); `:517` pipefail construct deleted; `:283`
  rc-gated (`age_unreadable=`); selftest 14 → 25 cases.
- `corpus/knowledge/silence-cutover-r3.md` — spec-row map (all rows
  implemented/verified), divergences D-a–D-g, hardening canaries, selftest
  delta, 27-case oracle re-baseline.
- `corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md`; `SKILL.md:111-153`
  r2 contract section; `corpus/README.md` coverage + known-gaps update;
  `corpus/evidence/README.md:110-173` receipt index; five receipts
  (`cutover-r3-20261015T164140Z-before.log`,
  `cutover-r3-20261015T165712Z-{selftest,oracle,live,oracle-counterfactual}.log`).
- Integration drafts: `.ufo/round-3/goal-wave/` (superseded working record).

## Before → after measurements (parent acceptance, 2026-10-15T17:24Z)

| Command / surface | Before (r1 `e3073a2b…`) | After (r2 `fe22a14f…`) | Exit |
|---|---|---|---|
| `bash tools/mori-census.sh --selftest` | `PASS (14 cases…)` | `PASS (25 cases, 25 passed, 0 failed)` | 0 |
| `bash tools/mori-silence-cases.sh` | `matched=10 total=27` | `matched=25 total=27` (15 FAIL→PASS, 10 held; 2 residual = frozen-oracle matcher defect; counterfactual `27/27` exit 0 at `ae95b601…`) | 1 |
| live silence surface | aggregate-only, `silent=7`, 7 × `LANE_SILENT` (`head_epoch=` pair) | 9/9 per-lane rows all `progressing` (8 row-A; aggregator row-B disclosed), `silent=0`, zero `LANE_SILENT`, counters +`young=/not_open=/unavailable=` | 1 |
| `:283` unreadable waves repro | rc 1, header only, no verdict | rc-gated: full verdict + `age_unreadable=1`, no crash | 0/1 |
| live wall time (perf seat, median of 3) | ~452 ms + silence share | ~1048 ms total but ~5.7× faster net of fixtures… see perf seat: r2 parser linear, no pathological cost | 1 |

Live verdict at acceptance: `MORI_CENSUS: DRIFT (findings=15 drift=14
unavailable=1 surfaces=7)` — the 1 unavailable is tmux (no server); the +1
finding vs the 16:57Z receipt is a mutable `SEGFAULT_JOURNAL` info count
(user-journal segfaults 0→8 during the wave). Drift sources: watchdog/waves/
journal only.

## SHONEN

- [ ] SKILL.md decision tables/error patterns with cited sources — r2 contract
  section landed; verification owed.
- [ ] End-to-end domain task executed and logged — r1+r2+r3 logged; owed.
- [ ] Instructions executable by an agent without oral context — owed.
- [ ] No cross-domain bleed (PROVINCE.md still accurate) — scope-sentinel clean
  this round; owed.

All four remain unchecked: no named non-author verifier exists; the wave's
seats are the lane per protocol.

## Cross-domain evidence and named debt (round 4 registered claim)

1. **Frozen-oracle matcher fix** — one block (`case "$obs" in $want)` →
   alternation-safe match); counterfactual witness `ae95b601…` already recorded.
2. **Oracle anti-sniff hardening** — opaque per-case dirs (no case id in the
   path), stop exporting `MORI_FIXTURE`, add a shape-invariance case; a no-logic
   case-id sniffer can currently fake `27/27` (falsifier seat, m4b mutant).
3. **Census `:227` `state_n` pipefail hardening** — last bare-pipeline crash
   shape; kills the whole census incl. the silence surface (critic re-measured).
4. **Per-round close tracking** — close lines for other rounds must not close
   the anchor round (critic defect 1; not producible from the current writer,
   latent).
5. Unchanged: drift pin; row-6 presence-only residual; blocked-attempt
   receipt-binding + role-routing debts.

Boundaries held: detection and report only; no remediation/kills/config edits;
fixtures under `/tmp`; frozen oracle untouched this round; seats made no
commits; fleet root read-only for seats.
