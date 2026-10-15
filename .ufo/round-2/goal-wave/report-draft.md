# mori round 2 — goal-wave report draft (scribe seat)

Integration target: the round report (idiom of `.ufo/reports/round-2/mori.md`; the
blocked-attempt report stays as-is — this is the fresh-round-2 delivery record).
Parent owns the final report, the identity and the commit binding. Every figure
below was measured by the scribe seat on 2026-10-15 between 15:27Z and 15:42Z
unless a citation names another artifact; `[PARENT]` marks what only the
integration commit can bind.

Status: `[PARENT: completion statement + verified-round-count claim]`
Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
Lane baseline entering the wave: `e30b2e3` · report time: `[PARENT]`

## Work performed

- Selected axis **coverage** (the lower owned LIVE axis per `SCORECARD.md:32-95`)
  and measured the falsifiable before-state of the quarantined candidate oracle:
  `bash tools/mori-silence-cases.sh` → exit **1** in 0.012 s, no
  `MORI_SILENCE_CASES` tally, stdout ending `nothing added to commit but untracked
  files present (use "git add" to track)` (sha256 `61db3df3…`).
- Traced the fixture-setup failure on a scratch copy of the candidate: `gc()`
  chained `commit --allow-empty -am || add -- rel && commit`; `A || B && C` binds
  as `(A || B) && C`, and on a fresh repo the `--allow-empty` commit succeeds
  (empty root commit; file left untracked), so the `git add` fallback is skipped
  and the trailing `commit -q` fails with nothing staged. Same lines carried the
  `-c core.autcrlf=false` typo (unknown key ignored; intended pin never applied).
- Re-measured the round-1 gate before and after: `bash tools/mori-census.sh
  --selftest` → `MORI_CENSUS_SELFTEST: PASS (14 cases, 14 passed, 0 failed)` exit 0;
  scoped live census at `2026-10-15T15:29:35Z` → `MORI_CENSUS: DRIFT (findings=18
  drift=15 unavailable=0 surfaces=7)` exit 1.
- Verified the wave's landed artifacts by re-running them, not by quoting them:
  the rewritten driver end-to-end (twice), the extracted authorship check, the
  receipt-file SHA-256s against `corpus/evidence/README.md`, and the driver's
  `unreadable-git-unavailable` census-crash mechanism (isolated pipefail repro).
- Prepared the integration drafts under `.ufo/round-2/goal-wave/`: the scorecard
  verdict section, the LOG entry, and this report.

## Landed changes

- `tools/mori-silence-cases.sh` (rewritten in-wave; sha256
  `505a7504811401b13fd96f8925605e744fbb54970c8ac65ac331b053d647e580` at the
  scribe's clock): deterministic stage-then-commit fixtures, `die` → exit 2 on
  setup failure, fixture ledger bound to the live watchdog-log grammar, report
  close path `.ufo/reports/round-<N>/<lane>.md`, three launch tails (`pid=` /
  `runId=` / `mission=`) exercised, one commit per `gc` call.
- `corpus/knowledge/observability-surfaces-r2.md` — seven per-surface notes
  (watchdog, waves, journal, cgroup, disk, silence, tmux) with Measures / Status /
  Gaps and six measured census defects; resolves the "six surfaces" framing
  (`corpus/README.md:7`) in prose.
- `corpus/knowledge/silence-grading-r2.md` — launch-aware, authorship-aware
  decision table with `proven`/`proposed` labels and a named-preconditions
  admission checklist (1-6).
- `corpus/knowledge/progressing-weak-r2.md` — the authorship discrimination proof
  (extractable check, 10 cases) + `--after` micro-semantics + D1/D2/D3 corrections
  + the falsifiable claim registered for the next round.
- `corpus/evidence/watch-r2-20261015T152746Z.log`, `…T152855Z.log`,
  `…T153003Z.log` + `corpus/evidence/README.md` — three dated live-census watch
  receipts, hash-pinned, with method, re-run recipe and compare rules.
- Scribe artifacts: `.ufo/round-2/goal-wave/{scorecard-verdict-draft,log-entry-draft,report-draft}.md`
  (these three files; no production change by this seat).

## Before → after measurements

| Command | Before (measured 15:2x–15:29Z) | After (measured 15:39–15:42Z) | Exit |
|---|---|---|---|
| `bash tools/mori-silence-cases.sh` | exit 1 in 0.012 s, fixture-setup failure before any case or tally (sha `61db3df3…`) | `MORI_SILENCE_CASES: matched=10 total=27`; deterministic (two runs byte-identical); 10 PASS / 17 FAIL | 1 |
| `bash tools/mori-census.sh --selftest` | `MORI_CENSUS_SELFTEST: PASS (14 cases, 14 passed, 0 failed)` | unchanged (census untouched) | 0 |
| `env MORI_ROSTER_LANES=mori MORI_LANE_SILENCE_S=900 bash tools/mori-census.sh` | `MORI_CENSUS: DRIFT (findings=18 drift=15 unavailable=0 surfaces=7)` at 15:29:35Z | still r1; live receipts captured by the wave (`corpus/evidence/watch-r2-*.log`, 23/23/22 findings) | 1 |
| Extracted authorship check (`sha256 9c91e0a0…`) | `progressing-weak` declared deferred; no runnable authorship proof (`corpus/README.md:13-14`) | `MORI_AUTHORSHIP_CHECK: matched=10 total=10` | 0 |

Tally semantics (driver header `tools/mori-silence-cases.sh:38-41`): against the
still-r1 census the launch/closure/attribution cases fail by design — those
failures are the measured r2 contract gap and are reported as-is. 16 of the 17 are
that gap (`young`, `not-open`, `progressing-weak`, launch-aware attribution,
report-window closure); the 17th, `unreadable-git-unavailable`, is a genuine r1
defect: the census crashes (exit 1, no `MORI_CENSUS` line) because
`tools/mori-census.sh:517` assigns a `find … | sort | tail | cut` pipeline under
`set -euo pipefail` and `find`'s permission-denied rc trips `set -e` (isolated
repro: pipeline rc=1). Verbatim failing list: `completed-not-open young-under-gate
young-age-equals-gate young-future-launch nolane-launch-not-open
ledger-missing-not-silent unreadable-git-unavailable subject-postlaunch-progressing
subject-hidden-behind-sibling-head sibling-clean-checkout-weak
author-sibling-committer-subject-weak author-subject-committer-sibling-progress
substring-name-mismatch-weak substring-email-mismatch-weak committed-report-closes
report-future-no-close main-repo-noise-silent`.

Live observations are mutable; the driver tally is the behavioral comparison this
round claims. The receipts' own scope note (`corpus/evidence/README.md:8-15`)
states the spacing (0/60/120 s) is a sampling method, not a watch mode — the census
has no watch/interval flag.

## Axis and learning verdicts

| Axis | Verdict | Evidence / limitation |
|---|---|---|
| coverage | **improved** | oracle runs end-to-end with an honest tally; seven per-surface notes; three receipts |
| operability | **improved** | driver operational/deterministic (exit 1 case failures, exit 2 setup); census green and live unchanged |
| depth | **improved** | per-surface + decision-table + authorship notes with code anchors and defects |
| freshness | **improved** | three dated hash-pinned re-runnable receipts + index; drift pin still absent |
| calibration | **improved** | authorship discrimination executed (10/10); failures counted as failures; D1 caught; admission deferred with preconditions |
| adjacency | **unchanged** | detection/report only; no remediation/kill/config edit in any artifact |

Expansion: **improved** (three new knowledge notes landed — seven-surface, decision
table, authorship proof; the precursor note from the blocked attempt remains the
derived-from record; `[PARENT: bind admission]`).
Quality: **improved** (honest failure counting; defects recorded with path:line;
receipt hashes verified). Discernment: **unchanged** (no outside spot-check).
Full before→after cells: `.ufo/round-2/goal-wave/scorecard-verdict-draft.md`.

## Cross-domain evidence and named debt

1. **r2 census cutover — deferred with named preconditions (not a silent drop).**
   `corpus/knowledge/silence-grading-r2.md:209-229` lists the six preconditions
   (r2 `probe_silence` in the census; harness reconciliation; grammar binding;
   report-path reconciliation; admission/receipt binding; the corrected identity
   recipe); `corpus/knowledge/progressing-weak-r2.md:240-264` registers the
   falsifiable claim (exit 0 with `matched=N total=M`, N=M, authorship cases among
   them; plus a live `progressing-weak` grade that is never `progressing`/`silent`).
2. **D1 — byte-defective identity recipe.** `corpus/knowledge/lane-silence-r2.md:112`
   and `corpus/knowledge/silence-grading-r2.md:128` print the `grep -Fxq` pattern
   without the closing `>`; verified printed-form rc=1 vs corrected rc=0. The
   corrected form is used by the landed check; the two notes still carry the
   defective text — parent integration should fix or annotate them.
3. **Census defects measured (report-only).** Unreachable
   `WATCHDOG_LOG_UNAVAILABLE` emission + false comment (`tools/mori-census.sh:198-200`);
   pgrep substring false positive with controlled demo (`:190-194`, receipt in
   `observability-surfaces-r2.md:114-123`); cgroup local/service counter
   invisibility when the parent file is readable (`:399-404`, `:421-428`);
   count-only `state_rounds` (`:220`); pipefail crash on unreadable `.git` (`:517`).
4. **Framing debt.** `corpus/README.md:7` and `observability-census-r1.md:10-17`
   say six surfaces; the executed set is seven
   (`tools/mori-census.sh:568-574`). The README coverage map and the
   `SKILL.md:111-129` cutover wording remain parent integration acts.
5. **Out-of-province findings stay reported, not absorbed.** Non-fleet unit
   failures are count-only (`tools/mori-census.sh:361-366`); the cumulative
   parent-slice OOM counter is info, not fleet evidence (`:424-426`). No
   remediation was performed by any seat.

Boundaries held: detection and report only — fixtures under `/tmp`, the lane's own
read-only tools, no kill/pkill/killall of real processes, no systemctl or host
config edits, no lane-side commits (parent integrates). `[PARENT: confirm from the
integration diff before publishing]`