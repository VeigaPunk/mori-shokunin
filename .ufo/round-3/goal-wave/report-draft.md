# mori round 3 — goal-wave report draft (scribe seat)

Integration target: the round report (idiom of `.ufo/reports/round-2/mori-goalwave.md`).
Parent owns the final report path, the identity and the commit binding. Every figure is
bound to a landed artifact (census r2 sha `fe22a14f…`; the five
`corpus/evidence/cutover-r3-*.log` receipts; `corpus/knowledge/silence-cutover-r3.md`;
`corpus/evidence/README.md:110-173`); `[PARENT: …]` marks what only the integration commit
or the parent's acceptance re-run can bind.

- Status: `[PARENT: completion statement + verified-round-count claim 2 → 3]`
- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Lane baseline entering the wave: `3da8414` (`LANE_HEAD` unchanged through every receipt)
- Report time: `[PARENT]`
- Draft status: seed v1 by the interrupted prior dispatch (16:10Z seed; 16:43Z rewrite
  left the after-side `[AWAITING]` — it predated the impl landing at 16:55Z). Rewritten
  2026-10-15T17:22Z by the scribe backfill seat from the landed artifacts.

## Work performed

- Selected axis **coverage** — the registered round-2 debt (`SCORECARD.md:128-131`): land
  the r2 `probe_silence` in `tools/mori-census.sh` per the
  `corpus/knowledge/silence-grading-r2.md` contract, harden the `:517`/`:283` pipefail
  constructs to `unavailable` grading, add selftest cases, and re-baseline the frozen
  oracle (`tools/mori-silence-cases.sh` sha `505a7504…`) with per-case justification —
  never branching on `MORI_FIXTURE` / fixture paths.
- Wave: one 32-seat flash wave; 8 seats (including this scribe) were re-dispatched as a
  backfill wave after a provider content-filter false positive.
  `[PARENT: bind the wave record]`
- Seats named in the landed artifacts: `cutover-note-writer` (the cutover note),
  `receipts-writer` (the five receipts), `lessons-distiller` (the lesson). This scribe
  seat wrote only `.ufo/round-3/goal-wave/{scorecard-verdict-draft,log-entry-draft,report-draft}.md`.

## Landed changes

- `tools/mori-census.sh` — r2, sha256
  `fe22a14f0bb6d90ffed14506abfcd76153ebf31cf3cb769b97e7eec61cc2f3c9`
  (`VERSION=census-r2`, `:61`): the silence surface rewritten as launch-anchored,
  authorship-aware grading — per-lane rows with six states (`grade_lane` `:664-810`; row
  emission `:837`), launch/steer anchoring (`ledger_anchor` `:576-627`), closure
  (`ps_report_closed` `:648-661`), rows A–D (`:747-809`), row-D-only `LANE_SILENT`
  (`:825-828`); `MORI_TIMELINE_FILE` override (`:81`); the r1 `:517` construct deleted and
  `:283` rc-gated (`:296-302`, `age_unreadable=` `:320`); selftest grown 14 → 25 cases
  (`:1185-1311`); zero `MORI_FIXTURE` references in the silence path `:503-845`.
- `corpus/knowledge/silence-cutover-r3.md` — the cutover note: spec-row map (§1), seven
  named deltas D-a–D-g (§2), hardening + remaining `:227` (§3), selftest 14→25 (§4), the
  27-case oracle re-baseline with per-case justification (§5), live honesty check (§6),
  deferred items (§7), evidence status (§8).
- `corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md` — the crash class, canaries
  A/B/C, the rc-1/DRIFT collision, countermeasures, and the `:227` residual.
- `corpus/evidence/cutover-r3-20261015T164140Z-before.log` + four `…T165712Z-*.log`
  receipts (selftest, oracle, live, oracle-counterfactual), indexed with re-run recipes at
  `corpus/evidence/README.md:110-173`.
- `SKILL.md:111-153` — the silence section rewritten as the r2 contract with the cutover
  receipt pointer.
- `corpus/README.md` — coverage map + known gaps updated for the round-3 landing (silence
  cutover, frozen-oracle tally residual, `:227`, row-6 residual). `[PARENT: written by the
  corpus-readme-updater seat; confirm in the integration diff]`
- Scribe artifacts: `.ufo/round-3/goal-wave/{scorecard-verdict-draft,log-entry-draft,report-draft}.md`
  (no production change by this seat).

## Before → after measurements

| Command | Before (r1 `e3073a2b…`, before receipt 16:41–16:49Z) | After (r2 `fe22a14f…`, receipts 16:57–16:58Z) | Exit |
|---|---|---|---|
| `bash tools/mori-silence-cases.sh` (frozen oracle `505a7504…`) | `matched=10 total=27`; 17 FAILs (16 contract gaps + 1 crash) | `matched=25 total=27`; 15 FAIL→PASS, 10 held, 2 matcher FAILs; counterfactual `matched=27 total=27` | 1 → 1 (cf 0) |
| `bash tools/mori-census.sh --selftest` | `PASS (14 cases, 14 passed, 0 failed)` | `PASS (25 cases, 25 passed, 0 failed)` | 0 → 0 |
| live census (default env) | aggregate-only silence row; 7 × `LANE_SILENT` (`head_epoch=`/`newest_epoch=`); `DRIFT (findings=21 drift=21 unavailable=1 surfaces=7)` | 9/9 per-lane rows `progressing`; `SURFACE silence: ok (silent=0 progressing=9 …)`; 0 `LANE_SILENT`; `DRIFT (findings=14 drift=14 unavailable=1 surfaces=7)` | 1 → 1 |
| unreadable lane repo (oracle case 9) | crash: no `MORI_CENSUS` verdict, rc 1 | graded `unavailable` with verdict, rc 0 | 1 → 0 |
| `:283` waves repro | rc 1, header only, no verdict (repro vs control rc 0 CLEAN) | `cap find` + rc branch (`:296-302`); selftest case `waves: unreadable wave age -> no crash, no false finding` PASS (no §4-style re-run after the cutover in the receipts) | 1 → 0 (selftest) |
| no-fixture-branching audit | — | `grep -n MORI_FIXTURE tools/mori-census.sh` → none in the silence path `:503-845`; only non-harness branch is the r1 journal JSON arm `:358-362` | — |

## Per-case oracle re-baseline (acceptance)

Full durable per-case justification: `corpus/knowledge/silence-cutover-r3.md:152-180`
(27 rows; spec anchors + observed r1/r2 state). Aggregate:

- **15 FAIL → PASS:** completed-not-open, young-under-gate, young-age-equals-gate,
  young-future-launch, nolane-launch-not-open, unreadable-git-unavailable,
  subject-postlaunch-progressing, subject-hidden-behind-sibling-head,
  sibling-clean-checkout-weak, author-sibling-committer-subject-weak,
  author-subject-committer-sibling-progress, substring-name-mismatch-weak,
  substring-email-mismatch-weak, committed-report-closes, main-repo-noise-silent.
- **10 r1 PASSes held (no regression):** silent-open, repo-missing-unavailable,
  same-round-relaunch-silent, legacy-steer-open-silent, dirty-same-path-as-sibling-progress,
  untracked-recent-progress, old-report-before-relaunch-silent, report-eq-launch-no-close,
  untracked-report-progress, readonly-no-mutation.
- **2 remaining FAILs = frozen matcher artifact:** `ledger-missing-not-silent` (got
  `unavailable` — inside the intended `not-open|unavailable` set) and
  `report-future-no-close` (got `silent` — inside the intended `progressing-weak|silent`
  set); the matcher (`case "$obs" in $want)`, `tools/mori-silence-cases.sh:362-365`)
  treats an expansion-introduced `|` literally (bash 5.3.15 probe,
  `…-oracle-counterfactual.log:18-24`); counterfactual witness 27/27 exit 0 at identical
  census bytes. The registered literal `N = M` is unreachable at the frozen sha (max
  25/27) — the honest tally is reported and the one-block matcher fix is the named
  round-4 unblock.

`[PARENT: acceptance = selftest all-pass + oracle re-baseline with per-case justification +
honest live census — all three landed (receipts above); re-run at integration and bind]`

## Axis and learning verdicts

Five axes **improved** (coverage, operability, depth, freshness, calibration); adjacency
**unchanged**; none harmed → **ADMIT**. Learning trends: expansion **improved**, quality
**improved**, discernment **unchanged**. Per-axis before→after evidence:
`scorecard-verdict-draft.md` (this directory), to be appended to `SCORECARD.md` by the
parent. `[PARENT: bind the admission]`

## Cross-domain evidence and named debt

- **`:227` watchdog `state_n` pipefail instance — open.** Same class as the hardened
  `:517`/`:283`; measured at `fe22a14f`: unreadable `.ufo/state` → rc 1, header only,
  0 verdict lines, 0 stderr (`silence-cutover-r3.md:106-114`;
  `corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md:137-141`). Out of the
  registered scope; next-round follow-up.
- **Frozen-oracle matcher fix — open, one block.** `tools/mori-silence-cases.sh:362-365`;
  counterfactual witness recorded; oracle frozen this round.
- **Frozen-behavioral drift pin — still absent** (round-3 debt, carried;
  `silence-cutover-r3.md:253-254`).
- **Row-6 report-body conformance residual** — presence + window only; spec-declared risk
  (`silence-cutover-r3.md:250-252`).
- **Precondition 5** (admission/receipt binding into LOG/SCORECARD) — parent-owned
  (`silence-cutover-r3.md:255-257`); the receipts document the cutover side only.
- `[PARENT: status of the round-2 blocked-attempt debts (role routing, receipt binding) —
  not determinable from this wave's artifacts]`
- Out-of-province, reported not absorbed: the other census surfaces' live findings (14 in
  the 16:57Z receipt: `WATCHDOG_STALE`/`WATCHDOG_ABSENT`, 11 × `WAVE_UNSETTLED_AGE`,
  `KILL_SIGNAL_JOURNAL`) and the tmux `unavailable` (not DRIFT).

Boundaries held: detection and report only — fixtures under `/tmp`, the lane's own
read-only tools, no kill/pkill of real processes, no systemctl or host config edits, no
lane-side commits (parent integrates). The frozen oracle `tools/mori-silence-cases.sh`
was not edited (sha `505a7504…` before and after every run).
`[PARENT: confirm from the integration diff]`