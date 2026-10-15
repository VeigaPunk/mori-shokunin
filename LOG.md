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

**Round-1 corrections (appended 2026-10-15).** A cross-domain audit falsified two
probe scopes and one settlement rule in the landed gate; all three were fixed and
the fixture suite re-verified at **14/14 PASS** (the cgroup scoping change first
broke its own fixture — the fixture had no service-scope path — which was repaired
in the same pass). Live census moved from `findings=10 drift=9` to
`findings=9 drift=7`. Carried debt: the wave-age clock is provisional
(`WaveAgeMath`), and the system-journal segfault scope is still missing.

**Round-1 correction 4 (appended 2026-10-15).** The segfault count was blind: the
journal stores signal 11 as `COREDUMP_SIGNAL`, so the text grep read 0 while the
user journal holds **656**. Fixed additively (JSON count can only raise the text
count, never replace it — a fixture stub must not be able to silence it); selftest
stays **14/14**, live now reports `SEGFAULT_JOURNAL count=656`. The compare key for
two runs is the finding-id set, not the byte stream (`current=` and the clock
fields move by construction).

**Round-1 correction 5 (appended 2026-10-15).** `FINDING` lines now stamp `ts=` and
`script_sha256=` (a finding without a clock and a code revision is not a reusable
observation); `WATCHDOG_ABSENT` no longer collapses a missing `pgrep` into a dead
daemon; the erratum's `w5`–`w11` generalization was superseded by measurement
(`w5` has no closeout file, `w6`–`w11` have `closeout.json`). Receipt clock and
script sha for this round: see the receipt block above. Carried debt: the
pgrep-unavailable arm is latent and unproven by fixture; silence has no
`unavailable` state; `/scratch/tmp` is outside the default disk targets.

**Round-1 correction 6 (appended 2026-10-15).** Disk thresholds are now explicitly
labeled `PROPOSAL, NOT MEASURED` in the gate and in `SKILL.md`, with the two traps
named (btrfs chunk percent reads 94.25% against a 10% `df` Capacity — never
threshold it; a byte floor OR'd against `df -P`'s 1024-block column false-fires on
a 10%-full filesystem). No new percent was installed.

**Lane telemetry (recorded, not a failure).** The `DiskThresholds` seat ended
without a final message (`failed` per the harness) while its **19 KB report landed
on disk** — an artifact-exists/status-failed case, not a lost lane. Its content is
used above; the process defect is recorded so the harness status is not read as a
missing deliverable.
