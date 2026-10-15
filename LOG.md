# mori-shokunin — Iteration Log

- 2026-10-14 — round 0: minted as shonen (sibling mint; rationale in MINT.md).

## round 1 — observability census + the census gate (probation round 1)

2026-10-14/15 · shonen probation round 1 · 32-lane fleet wave
(`Shokunin12hP4MoriR1`) + parent integration.

**Landed:** `tools/mori-census.sh` (read-only census over six surfaces, verdict
`MORI_CENSUS: CLEAN|DRIFT`, exit 0/1/2, `--selftest` 14 cases); the corpus receipt
`corpus/knowledge/observability-census-r1.md`; `corpus/README.md`; this scorecard.

**Verdict lines.** `bash tools/mori-census.sh --selftest` →
`MORI_CENSUS_SELFTEST: PASS (14 cases, 14 passed, 0 failed)` exit 0.
Live → `MORI_CENSUS: DRIFT (findings=10 drift=9 unavailable=0 surfaces=7)` exit 1,
with `OOM_KILL_JOURNAL count=1`, `CGROUP_OOM_KILL oom_kill=1`,
`WATCHDOG_ABSENT`, `WATCHDOG_STALE age_s=103830`, five `WAVE_UNSETTLED_AGE`.

**Three fixture defects were found and repaired while landing the design's
script** (the design shipped 3 of 14 cases red): the harness freshened the very
paths the staleness cases needed old (added an explicit opt-out and real
thresholds with backdated fixtures instead of a 0 threshold), and the silence
fixture put the lane repo where the probe does not look. All three repairs are in
the fixture harness, not the live logic.

**Carried debt:** per-surface notes still owed; `progressing-weak` authorship
proof deferred; thresholds for disk/memory are proposals with no evidence yet.
