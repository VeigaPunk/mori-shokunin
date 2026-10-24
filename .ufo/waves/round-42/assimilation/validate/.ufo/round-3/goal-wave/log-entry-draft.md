# LOG.md entry draft — append-only (scribe seat, goal wave)

Integration target: append to `LOG.md` at EOF, after the round-2 goal-wave admission entry
(last section at this draft's clock, `LOG.md:192-220`) — parent-owned, append-only.
Suggested heading: `## round 3 — silence grading cutover (goal wave)`
`[PARENT: keep or rename the heading; bind the commit hash(es), the acceptance re-run
outputs and the round-count line]`.

Draft status: seed v1 by the interrupted prior dispatch (16:10Z); rewritten 2026-10-15T17:22Z
by the scribe backfill seat from the landed artifacts (census r2 sha `fe22a14f…`; receipts
`corpus/evidence/cutover-r3-*.log`; `corpus/knowledge/silence-cutover-r3.md`). Supersedes
the 16:43Z `[AWAITING]` seed, which predated the impl landing.

---

## round 3 — silence grading cutover (goal wave)   `[PARENT: heading]`

**Round 3 — goal-wave admission (2026-10-15).** Motivating evidence: the round-2 verdict's
named debt (`SCORECARD.md:128-131`, admission commit `3da8414`) — the r2 `probe_silence`
census cutover (preconditions `corpus/knowledge/silence-grading-r2.md:216-236`; the passing
tally `matched=N total=M`, `N=M` registered as the claim), the census `:517` (and `:283`)
pipefail crash → `unavailable` semantics, and the frozen-behavioral drift pin. Measured
before-state at the r1 census sha `e3073a2b…` (before-leg receipt, 16:41:40–16:49:31Z):
oracle `matched=10 total=27` exit 1 — 16 r2-contract gaps + 1 crash
(`unreadable-git-unavailable: census emitted no MORI_CENSUS verdict (rc=1) — crashed
mid-run`); selftest 14/14 exit 0; live aggregate-only silence row + 7 × `LANE_SILENT` with
`head_epoch=`/`newest_epoch=`; `:283` repro rc 1 header-only vs control rc 0 CLEAN.

**Landed.** Census r2 (`VERSION=census-r2`, sha256
`fe22a14f0bb6d90ffed14506abfcd76153ebf31cf3cb769b97e7eec61cc2f3c9`): launch-anchored,
authorship-aware `probe_silence` — per-lane rows with six states, closure predicate
(ledger close + committed-report window), rows A–D with the exact identity pair, strict age
gate, `LANE_SILENT` only for row D, `unavailable` ≠ unhealthy
(`corpus/knowledge/silence-cutover-r3.md` §1 spec-row map); the r1 `:517` construct is
deleted and `:283` rc-gated with `age_unreadable=` disclosure (§3); selftest 14 → 25
(11 new + 1 reworked, §4). Supporting artifacts: the cutover note
`corpus/knowledge/silence-cutover-r3.md`; the lesson
`corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md` (crash class, canaries A/B/C,
rc 1 collides with DRIFT); `SKILL.md:111-153` r2 contract section with the cutover pointer;
five receipts under `corpus/evidence/` indexed at `corpus/evidence/README.md:110-173`;
`corpus/README.md` coverage map + known gaps updated. Frozen oracle
`tools/mori-silence-cases.sh` unmodified (sha `505a7504…` verified before/after every run).
`[PARENT: bind the wave record — 32-seat flash wave; 8 seats re-dispatched as a backfill
wave after a provider content-filter false positive]`

**Parent acceptance at integration.** `bash tools/mori-census.sh --selftest` →
`MORI_CENSUS_SELFTEST: PASS (25 cases, 25 passed, 0 failed)` exit 0 (receipt 16:57:12Z);
`bash tools/mori-silence-cases.sh` → `MORI_SILENCE_CASES: matched=25 total=27` exit 1 —
15 FAIL→PASS, the 10 r1 PASSes held; the 2 remaining FAILs are the frozen-oracle matcher
defect (`case "$obs" in $want)` never matches an expansion-introduced `|`,
`tools/mori-silence-cases.sh:362-365`; calls `:455`, `:613`) — counterfactual witness at
identical census bytes `matched=27 total=27` exit 0; live `census-r2` census: 9/9 roster
lanes `progressing` (aggregator row-B with `attribution=inference` disclosed),
`SURFACE silence: ok (silent=0 progressing=9 …)`, zero `LANE_SILENT`,
`DRIFT (findings=14 drift=14 unavailable=1 surfaces=7)` (the 1 unavailable is tmux),
reverify spot identical. `[PARENT: re-run and bind these outputs at admission]`

**Verdicts.** Five axes **improved** (coverage, operability, depth, freshness,
calibration); adjacency **unchanged**; none harmed → **ADMIT**; learning trends:
expansion/quality **improved**, discernment **unchanged**. Full per-axis before→after in
the `SCORECARD.md` Round 3 section. `[PARENT: bind]`

**Carried debt (named, not silently dropped).** `:227` watchdog `state_n` pipefail
instance — measured open at `fe22a14f`, out of the registered `:517`/`:283` scope
(`silence-cutover-r3.md` §3; lesson). The frozen-oracle matcher fix — one block; witness
already recorded; oracle frozen this round, fix belongs to round 4. The frozen-behavioral
drift pin — still absent (`silence-cutover-r3.md` §7). Row-6 report-body conformance
residual (presence + window only; spec-declared risk). `[PARENT: carry the round-2
blocked-attempt debts (role routing, receipt binding) only if still open — not
determinable from this wave's artifacts]`

**Boundaries held.** Detection and report only: fixtures under `/tmp`, the lane's own
read-only tools; no remediation, no kill/pkill of real processes, no systemctl or host
config edits; no lane-side commits (the parent integrates under the mori identity); the
frozen oracle `tools/mori-silence-cases.sh` was not edited (sha `505a7504…`).
`[PARENT: confirm from the integration diff]`

Round report: `[PARENT: .ufo/reports/round-3/<report>.md or equivalent]` · Verified lane
rounds: `[PARENT: 2 → 3 on admission]`