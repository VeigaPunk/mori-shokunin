# Round 2 verdict — integration draft (scribe seat, goal wave)

Integration target: append as a `## Round 2 verdict` section in `SCORECARD.md`
(parent-owned). Verdict vocabulary only (`improved` / `harmed` / `unchanged` /
`unprovable-but-better`); no scalar scores — the legacy scalar columns stay
untouched unless the parent binds a change. All figures below were re-measured by
this seat on 2026-10-15 between 15:39Z and 15:42Z; artifact SHA-256s are the values
at that clock (the driver was rewritten mid-wave, so earlier bytes are named as
"before"). The blocked-attempt section (`SCORECARD.md:32-95`) is preserved
append-only and not rewritten.

Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
Round-count claim: `[PARENT]` — the wave worked one coverage move; verified-round
accounting belongs to the parent.

## Round 2 verdict

Round scope: the lane-silence behavioral oracle runs end-to-end and emits its first
honest scenario tally; seven per-surface notes, three dated watch receipts and the
`progressing-weak` discrimination proof land under `corpus/`. The production census
grader remains r1 (`tools/mori-census.sh` sha256 `e3073a2b…`); the r2 cutover stays
deferred with named preconditions (`corpus/knowledge/silence-grading-r2.md:209-229`).

| Axis | Before | After | Verdict | Evidence |
|---|---|---|---|---|
| coverage | `bash tools/mori-silence-cases.sh` → exit 1 in 0.012 s, fixture-setup failure, no `MORI_SILENCE_CASES` line (sha256 `61db3df3…`, measured 15:2xZ); per-surface notes owed (`corpus/README.md:11-12`); no watch receipts | Oracle runs all 27 cases in ~1.25 s and emits `MORI_SILENCE_CASES: matched=10 total=27` exit 1 — deterministic (two consecutive runs byte-identical). Of the 17 failures, 16 are the measured r2-contract gap against the r1 grader (declared as the intended honest reading by the driver header, `tools/mori-silence-cases.sh:38-41`) and 1 is an r1 census crash (see operability/calibration); seven per-surface notes and three dated watch receipts landed | **improved** | driver sha256 `505a7504…` and its runs; `corpus/knowledge/observability-surfaces-r2.md`; `corpus/evidence/watch-r2-20261015T152746Z.log` + 2 more; `corpus/evidence/README.md:19-23` |
| operability | Census `--selftest` 14/14 exit 0 (re-measured); oracle not evaluable past fixture setup (exit 1, no case or tally) | Oracle operational and deterministic: case failures exit 1, fixture-setup failure exits 2 (`tools/mori-silence-cases.sh:7-9`, `:95`), `readonly-no-mutation` passes; census unchanged and still green (selftest 14/14 exit 0); live census still runs (exit 1 DRIFT, `script_sha256=e3073a2b…`) | **improved** | driver run outputs; `bash tools/mori-census.sh --selftest` → `PASS (14 cases, 14 passed, 0 failed)`; three live receipts `corpus/evidence/watch-r2-*.log` (all exit 1) |
| depth | Finding-id vocabulary + per-surface semantics in `corpus/knowledge/observability-census-r1.md`; two thresholds `PROPOSAL, NOT MEASURED` (`tools/mori-census.sh:88-94`) | Seven per-surface notes (Measures/Status/Gaps, code-line anchors) + launch-aware/authorship-aware decision table with `proven`/`proposed` labels and a 6-item precondition list + `--after` micro-semantics (`--after` includes ct==T; filters committer date while identity rows match author fields) + six measured census defects | **improved** | `corpus/knowledge/observability-surfaces-r2.md`; `corpus/knowledge/silence-grading-r2.md`; `corpus/knowledge/progressing-weak-r2.md:104-121` |
| freshness | One dated live receipt in the r1 note; no watch receipts; no drift pin (`SCORECARD.md:13`) | Three dated, hash-pinned, re-runnable watch receipts (spots 15:27:46Z / 15:28:55Z / 15:30:03Z) + an evidence index with the compare method (finding-id set, not byte stream) and re-run recipe; receipt file SHA-256s re-verified by this seat | **improved** | `corpus/evidence/watch-r2-*.log` (sha `1ea8441f…` / `36ae6522…` / `b44f98c0…`); `corpus/evidence/README.md:68-89`. Drift pin still absent — remains the named next step |
| calibration | `unavailable ≠ unhealthy` enforced and fixture-proved (`tools/mori-census.sh:859-864`); `progressing-weak` declared deferred rather than faked (`corpus/README.md:13-14`) | The deferred discrimination is now runnable and executed: extracted check sha `9c91e0a0…` → `MORI_AUTHORSHIP_CHECK: matched=10 total=10` exit 0 (re-run by this seat); the byte-defective identity recipe (D1) was caught and the corrected form used; the oracle counts its failures as failures (no green-washing); production admission deferred with named preconditions and a registered falsifiable claim | **improved** | `corpus/knowledge/progressing-weak-r2.md:19-37,56-71,240-264`; `corpus/knowledge/silence-grading-r2.md:209-229` |
| adjacency | Refuses dispatch (kumitate) and OS state (tsukuroi) (`PROVINCE.md:12-17`); detection/report only | Unchanged boundary: the wave landed fixtures, notes, receipts and proofs only — no remediation, no kill/pkill/killall, no systemctl or host config edit in any artifact; out-of-province findings stay reported, not absorbed | **unchanged** | `PROVINCE.md:12-17`; `corpus/knowledge/progressing-weak-r2.md:5-7`; `corpus/knowledge/observability-surfaces-r2.md:12`; driver header `:81-82`; no host mutation performed |

Learning trends (lane idiom):

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **improved** | Three new corpus notes landed under `corpus/knowledge/` (seven-surface notes, decision table, authorship proof); the precursor note from the blocked attempt remains the derived-from record `[PARENT: bind admission in the integration commit]` |
| quality | **improved** | Honest tally by construction (17 failures reported as failures); D1/D2/D3 and six census defects recorded with path:line, not hidden; receipt hashes self-verified |
| discernment | **unchanged** | No outside spot-check of an admit/reject exists in the wave's artifacts; the authorship check is the lane's own — L1 integration is not outside verification |

Baseline and after commands re-measured by this seat (before-state at 15:2x–15:29Z,
after-state at 15:39–15:42Z):

- Before: `bash tools/mori-silence-cases.sh` → exit **1**, 0.012 s, stdout ending
  `nothing added to commit but untracked files present (use "git add" to track)`;
  no tally. Mechanism traced to `tools/mori-silence-cases.sh:201-215` (`A || B && C`
  binds as `(A || B) && C`; the `--allow-empty` commit succeeds on a fresh repo and
  the `git add` fallback never runs).
- After: `bash tools/mori-silence-cases.sh` → `MORI_SILENCE_CASES: matched=10 total=27`,
  exit **1**; two consecutive runs byte-identical.
- `bash tools/mori-census.sh --selftest` → `MORI_CENSUS_SELFTEST: PASS (14 cases,
  14 passed, 0 failed)` exit **0** (before and after).
- `env MORI_ROSTER_LANES=mori MORI_LANE_SILENCE_S=900 bash tools/mori-census.sh` →
  `MORI_CENSUS: DRIFT (findings=18 drift=15 unavailable=0 surfaces=7)` exit **1** at
  `2026-10-15T15:29:35Z` (mutable live observation, not a causal comparison).

`[PARENT: hash the integration commit and replace every [PARENT] marker before
appending this section]`