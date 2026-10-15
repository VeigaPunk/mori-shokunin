# LOG.md entry draft — append-only (scribe seat, goal wave)

Integration target: append to `LOG.md` after the existing blocked-attempt section
(`LOG.md:100-190`). Parent owns `LOG.md`; this is the draft entry. Every figure in
it was measured by the scribe seat on 2026-10-15 between 15:27Z and 15:42Z unless a
citation names another artifact. `[PARENT]` marks the values only the integration
commit can bind.

Suggested heading: `## round 2 — silence oracle + first coverage artifacts (goal
wave)`. `[PARENT: keep or rename the heading; bind the commit hash and the
round-count statement]`

---

2026-10-15 · goal wave (13 seats, lane repo only; fleet root read-only) over lane
baseline `e30b2e3` · selected axis **coverage** — the lower owned LIVE axis. This
is the fresh round 2; the blocked interactive-cutover attempt above is preserved
append-only and is not rewritten. Verified lane rounds: `[PARENT]`.

**Motivating evidence.** The quarantined scenario driver was not a working oracle:
`bash tools/mori-silence-cases.sh` exited **1** in 0.012 s with no
`MORI_SILENCE_CASES` tally and stdout ending `nothing added to commit but untracked
files present (use "git add" to track)` (sha256
`61db3df336fcd0facfaa9de6a5f0b5753047a450bbe85f685bc2d2a051b7011f`). Mechanism,
traced on a scratch copy and independently re-confirmed: `gc()` chained
`commit --allow-empty -am || add -- rel && commit`; `A || B && C` binds as
`(A || B) && C`, and on a fresh repo the `--allow-empty` commit SUCCEEDS (empty root
commit; the file stays untracked), so the `git add` fallback is skipped and the
trailing `commit -q` dies on "nothing added to commit". The same lines carried
`-c core.autcrlf=false` (`:214`, typo) so the intended `core.autocrlf=false` pin was
silently absent. `corpus/README.md:11-12` still owed one note per surface family and
`corpus/evidence/` held no watch receipts.

**Landed.** The driver was rewritten to deterministic stage-then-commit with `die`
on setup failure (exit 2) and to the live watchdog-log grammar as its fixture
ledger (`tools/mori-silence-cases.sh` sha256
`505a7504811401b13fd96f8925605e744fbb54970c8ac65ac331b053d647e580`; typo fixed).
It now completes all 27 behavioral cases in ~1.25 s and emits
`MORI_SILENCE_CASES: matched=10 total=27` exit 1 — deterministic (two consecutive
runs byte-identical). The 17 failures are the intended honest reading against the
still-r1 census: 16 semantic/lifecycle/attribution cases the r2 contract requires
(`young`, `not-open`, `progressing-weak`, launch-aware attribution, report-window
closure) plus 1 r1 defect — `unreadable-git-unavailable`, where the census crashes
(exit 1, no `MORI_CENSUS` line) because `tools/mori-census.sh:517` assigns a
`find … | sort | tail | cut` pipeline under `set -euo pipefail` and `find`'s
permission-denied rc trips `set -e` (isolated repro rc=1). Corpus gained seven
per-surface notes in `corpus/knowledge/observability-surfaces-r2.md` (watchdog,
waves, journal, cgroup, disk, silence, tmux — Measures/Status/Gaps each, six
measured census defects), the decision table
`corpus/knowledge/silence-grading-r2.md`, the authorship proof
`corpus/knowledge/progressing-weak-r2.md`, and the first dated watch receipts —
three spaced live censuses at 15:27:46Z / 15:28:55Z / 15:30:03Z with file SHA-256s
`1ea8441f…` / `36ae6522…` / `b44f98c0…` (verified against
`corpus/evidence/README.md:36-39`), indexed by `corpus/evidence/README.md`.
`[PARENT: list any further wave artifacts landed after this draft's clock]`

**Receipts (verbatim key lines).**

- `bash tools/mori-silence-cases.sh` → `MORI_SILENCE_CASES: matched=10 total=27`,
  exit **1**; failure list begins `completed-not-open young-under-gate …` and ends
  `report-future-no-close main-repo-noise-silent`.
- Extracted authorship check (`corpus/knowledge/progressing-weak-r2.md`, extraction
  sha256 `9c91e0a011a99dfb9459f4a5cbedaecf432812a5a4237ec02e32fafd3801afd6`) →
  `MORI_AUTHORSHIP_CHECK: matched=10 total=10`, exit **0** (re-run by this seat).
- `bash tools/mori-census.sh --selftest` → `MORI_CENSUS_SELFTEST: PASS (14 cases,
  14 passed, 0 failed)`, exit **0**.
- Live census (scoped to mori) at `2026-10-15T15:29:35Z` →
  `MORI_CENSUS: DRIFT (findings=18 drift=15 unavailable=0 surfaces=7)`, exit **1**;
  three default-roster live receipts in `corpus/evidence/watch-r2-*.log`, exit
  **1** each (23/23/22 findings — the spot-3 `WATCHDOG_ABSENT` flip is recorded in
  `corpus/evidence/README.md:49-60` as a measured anomaly, not explained away).

**Verdicts.** coverage, operability, depth, freshness and calibration:
**improved**; adjacency: **unchanged**. Expansion and quality: **improved**;
discernment: **unchanged** (no outside spot-check). Evidence per axis is in
`.ufo/round-2/goal-wave/scorecard-verdict-draft.md`; no scalar score is advanced
there. `[PARENT: adopt or adjust the axis verdicts in the parent-owned scorecard]`

**Boundaries held.** Detection and report only: fixtures under `/tmp`, the lane's
own read-only tools, no remediation, no kill/pkill/killall of real processes, no
systemctl or host config edits, no lane-side commits (the parent integrates and
commits under the mori identity). Journal content stayed count-only in every
receipt. Out-of-province findings (non-fleet unit failures, the cumulative parent
OOM counter) remain reported, not absorbed (`PROVINCE.md:12-17`).

**Carried debt (named preconditions, not silent drops).** (1) The r2 census cutover
is deferred: `corpus/knowledge/silence-grading-r2.md:209-229` lists six
preconditions and `corpus/knowledge/progressing-weak-r2.md:240-264` registers the
falsifiable claim (passing tally N=M and a live `progressing-weak` grade) for the
next round. (2) D1 — the identity recipe printed in
`corpus/knowledge/lane-silence-r2.md:112` and `corpus/knowledge/silence-grading-r2.md:128`
lacks the closing `>` and matches nothing as written (verified: printed form rc=1,
corrected rc=0); the two notes still carry the defective form. (3) The census
defects measured by the surfaces note (unreachable `WATCHDOG_LOG_UNAVAILABLE`
arm `tools/mori-census.sh:198-200`; pgrep substring false positive; cgroup
local-counter invisibility `:399-404`/`:421-428`; count-only `state_rounds` `:220`;
pipefail crash `:517`) are reported, not fixed. (4) `corpus/README.md:7` and the r1
note still say "six surfaces" where the executed set is seven; the README coverage
map and `SKILL.md:111-129` cutover wording remain parent integration acts. (5) No
frozen drift pin yet.