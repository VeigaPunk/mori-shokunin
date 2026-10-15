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

**Round-1 correction 7 (appended 2026-10-15).** Coredump taxonomy recorded: the
segfault probe filters `COREDUMP_SIGNAL=11` at the journal, which keeps it
signal-specific — `terminated abnormally` lines are signal **5** (SIGTRAP) and share
the coredump MESSAGE_ID without carrying the `dumped core` text, so neither a text
grep nor a generic coredump count may stand in for it.

**Round-1 correction 8 (appended 2026-10-15).** The lane-silence grader is recorded
as a **provisional approximation** with its rule divergence named against
`PROTOCOL.md:155-168`: it grades a rolling window instead of aging from the launch
line, so it grades wrapped missions that the protocol leaves ungraded (measured:
kasegi round 17 wrapped), and it labels any in-window file activity `progressing`
where sibling-only activity must be `progressing-weak` (measured: aggregator, whose
window evidence is a gitignored `game-dev-3d` log plus `protocol-shokunin` and
`shokunin-fleet` commits). Unblock: launch-line aging plus an author check.

**Round-1 correction 9 (appended 2026-10-15).** Two hardenings landed from the
threat model: `set +o xtrace` (the gate holds raw journal text that can carry
token-shaped lines — verified 0 leaked under `bash -x`) and a `realpath` before the
cgroup prefix check (the `/sys/fs/cgroup/../..` escape is now refused shape-only).
Selftest 14/14. Carried debt: live-mode `MORI_*_BIN` overrides and the unquoted
`MORI_DISK_TARGETS` list can automount; `/proc/<pid>/environ` is readable for 95
pids and is not contract-forbidden, so no future probe may adopt it.

**Round-1 correction 10 (appended 2026-10-15).** The selftest cleanup trap used a
`local` variable, so the EXIT trap — which fires after the function returns —
expanded to `rm -rf -- ''` and **every run leaked its temp dir** (measured: 45
leftover `/tmp/mori-census-selftest.*` dirs, and the leftover was the only
detector). The path now lives in a non-local holder; 45 leftovers were cleaned and
two consecutive runs leave **0**. Independently proved by the same seat: the gate is
idempotent on a frozen fixture (stdout diff empty, 21-file manifest unchanged,
`strace` 0 successful writes outside the fixture) and a canary write planted in a
scratch copy was killed (`forbidden 1`).

## round 2 — interactive cutover attempt (blocked; no completion credit)

2026-10-15 · Sole interactive mori L1 · baseline
`0715198ed683445768944cec2db75bce12a1d202` · selected axis **coverage**, the lower
owned LIVE axis in the actual scorecard. The read-only fleet ledger contains
one mori round-1 closure (`ok`, `7ca17b1`). Launch counter 2 is not a completed
round count. No prior entry, completed report, session, or round was reset.

**Motivation and reconciliation.** `SKILL.md:111-129` and this log's round-1
correction 8 name the launch/authorship divergence. The interrupted worker left
a silence note and scenario driver, two cgroup wording edits in `SKILL.md`, and
dispatch/baseline receipts. The production census is still the round-1 script.
The inherited nine-seat dispatch records do not satisfy this operator's
32-seat/routing contract. Originals remain unchanged and intentionally
uncommitted; exact non-session bytes are quarantined as evidence in
`.ufo/round-2/interactive-cutover/inherited-candidates.json`, with provenance
and hashes in `inherited-inventory.json`. These snapshots are not corpus
admission or a production cutover. Native session material was not read or
committed.

**Plan and dispatch evidence.** Saved WWKD before work at
`.ufo/round-2/interactive-cutover/wwkd.md`. Saved exactly 32 distinct scopes
with disjoint report ownership at `wave/spec.json`. The actual canonical
`node scripts/ufo-swarm-wave.mjs plan --spec <saved-spec> --route-families`
ran from the UFO checkout and exited 0; complete output is
`wave/plan-command.json`. No `run`, registry persistence or task batch followed.
Route preflight observes 25 planned seats on `@m_mid`, six on `@m_strong`, one
on `@m_fast`; status `unprobed`, zero pings. Global config digest:
`08788ddcbbb48180b987e6f54b517af294c85cacceb07bdd594843a53e668dcc`.
Required content `@m_composer`, audit `@m_grok`, connector `@m_antigravity`
with `@m_zfl` fallback are not bound to the used task roles. Exact actual and
required bindings are in `wave/admission.json`. No model/route/config overlay
was substituted and no host or source remediation was attempted.

**Own gate and actual CLI smoke.** Full argv, stdout/stderr, timestamps and
exit codes are in `.ufo/round-2/interactive-cutover/checks/`.
Measured production script SHA-256:
`e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2`.

- `bash tools/mori-census.sh --selftest` →
  `MORI_CENSUS_SELFTEST: PASS (14 cases, 14 passed, 0 failed)`, exit **0**.
- `env MORI_ROSTER_LANES=mori MORI_LANE_SILENCE_S=900 bash tools/mori-census.sh`
  → `MORI_CENSUS: DRIFT (findings=14 drift=11 unavailable=0 surfaces=7)`,
  exit **1**, observed at `2026-10-15T05:08:17Z`. This is an observation, not
  an instruction to remediate. Journal content remains count-only. User-slice
  cumulative OOM count is not evidence of a fleet kill.
- `bash tools/mori-silence-cases.sh` → exit **1** during fixture setup,
  stdout ends `nothing added to commit but untracked files present (use "git
  add" to track)`. No PASS/FAIL case or `MORI_SILENCE_CASES` line was emitted;
  no behavioral tally or passing cutover is claimed. The source's `gc` helper
  chains `commit --allow-empty ... || add ... && commit ...`; deterministic
  stage-then-commit setup is the concrete reconciliation target. The original
  candidate was not patched to disguise this failed admission check.

**Verdicts.** Coverage, operability, depth, freshness, calibration and adjacency:
**unchanged** for this blocked attempt. Expansion, quality and discernment:
**unchanged**. No new knowledge admitted, no improved axis claimed, no outside
spot-check, promotion, native judgment, frozen behavioral comparison or
successful round-2 receipt. Current scorecard records the evidence and debt;
historical scalar scores are not advanced.

**Receipt and continuation boundary.** `receipt-applicability.json` records
the exact running Sighting mission/run/session metadata selected read-only.
Its metadata provides no `task_` plus 24-hex queue key or authoritative expected
receipt-binding bag. The default dispatcher queue path is absent. Mechanical
shape-valid receipt generation with invented identities would not be applicable
acceptance evidence, so neither mint nor validate nor Sighting completion was
invoked. The earlier fleet-reported Phase-0 contract-sync/self-iter failures
were not rerun. Concrete unblock: operator/integrator supplies the authorized
role bindings and applicable receipt metadata; a **fresh** L1 retries actual
round 2, reconciles the quarantined candidates and issues the full validated
32-seat batch. Verified lane rounds remain **1**. This attempt is neither
saturation nor three consecutive blocked rounds.

Only this log, the appended scorecard status and explicitly named
repository-local `.ufo` artifacts are included in the cutover commits. The
report and continuation land after the evidence commit and cite its exact
hash. Shared fleet reports/ledgers, dirty originals and session storage are
outside those commits; no push is performed.

**Round-2 delivery append (same blocked attempt).** Evidence commit
`49049ab6c7c4b492457b3398ba402afbf51b3a7f` landed under the required mori
identity. After that commit, the lane wrote its repository-local report
`.ufo/reports/round-2/mori.md` and fresh-session handoffs
`.ufo/round-2/interactive-cutover/continuation.md` / `continuation.json`.
They cite that exact evidence commit, full gate verdicts/exits, unchanged
axis/trend verdicts, the missing role/receipt bindings and next actual round 2.
The report-time own-mission age was 581 s from the recorded launch, below two
450-second ticks; no stale-lane failure was inferred. This delivery commit
adds records only: no new check, candidate admission, production cutover,
receipt, native judgment, mission completion or round-count advancement.

**Round 2 — goal-wave admission (2026-10-15).** Motivating evidence: the blocked
attempt's named debt above — the quarantined oracle candidate
`tools/mori-silence-cases.sh` (sha `61db3df3…`) exited 1 in fixture setup with no
scenario tally. This round dispatched one 13-seat flash wave (single batched call;
diag/falsifier/critic/verifier seats among it). Landed: the harness reconciled to
revision `505a7504` (deterministic stage-then-commit `gc` with `die` → exit 2;
fixtures bound to the live watchdog-log grammar and the live report path
`.ufo/reports/round-<N>/<lane>.md`; root cause `(A||B)&&C` + `--allow-empty`
empty-root-commit pinned by two independent seats); seven per-surface notes
(`corpus/knowledge/observability-surfaces-r2.md`); the silence-grading decision
table (`corpus/knowledge/silence-grading-r2.md`); the progressing-weak authorship
discrimination proof with runnable 10-case check
(`corpus/knowledge/progressing-weak-r2.md`; extract sha `9c91e0a0…`,
`MORI_AUTHORSHIP_CHECK: matched=10 total=10` exit 0); three dated live-census
watch receipts (`corpus/evidence/watch-r2-20261015T15{2746,2855,3003}Z.log`,
indexed in `corpus/evidence/README.md`). Parent acceptance at integration:
`bash tools/mori-census.sh --selftest` → `MORI_CENSUS_SELFTEST: PASS (14 cases,
14 passed, 0 failed)` exit 0 (census untouched, sha `e3073a2b…`);
`bash tools/mori-silence-cases.sh` → `MORI_SILENCE_CASES: matched=10 total=27`
exit 1 — the honest gradient (16 cases = r2 contract gap vs the still-r1 census;
1 = measured r1 defect at `tools/mori-census.sh:517`, pipefail crash, minimal
repro). Parent integration fixes: byte-defective identity recipe (missing
closing `>`) in `lane-silence-r2.md`/`silence-grading-r2.md`; `mission=` tail
count 4→3 plus one untailed launch; stale pre-wave line citations annotated with
a revision-scope line per note; `corpus/README.md` six→seven surfaces + coverage
rows; lesson `corpus/lessons/2026-10-15-oracle-honesty-crash-masking.md`.
Round report: `.ufo/reports/round-2/mori-goalwave.md` (the blocked attempt's
`mori.md` remains untouched). No remediation, no kills, no host config edits; no
push (the lane repo has no remote). Verified lane rounds: 1 → 2.
