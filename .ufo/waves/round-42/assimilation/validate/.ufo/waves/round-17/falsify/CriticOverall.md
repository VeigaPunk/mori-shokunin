# CriticOverall — whole-round falsification, mori round 17 wave 2

Seat: `MoriR17.CriticOverall-4` (leaf, report-only). Scope: attack whole-round
admission on all six axes and protocol — lowest-score duty, finite-capability vs
bug framing, old drift red, procedural disclosure, selftest independence, hidden
axis harm. Method: read-only git plumbing and jq/python reads over committed
receipts at lane tip `5c1dfb8`; measured inputs pinned at `273aa74`. No gate,
selftest, census or live probe was rerun; no VCS mutation; no /tmp write; no
install. Only this file written.

## Summary

No admission-blocking defect observed inside the attacked scope. Three residual
(non-blocking) findings at the end, the strongest a stale fixture case id whose
name asserts the pre-Amendment-A1 ordering while its pinned expectation asserts
the A1 ordering.

## Attacked scope and observed results

### 1. Lowest-score duty (calibration 5)

- `AXES.md:33` requires ≥1 claim on the lowest-scoring non-retired axis; active
  scores are depth/freshness/calibration 5, coverage 6, operability 7, adjacency
  6, none retired (`SCORECARD.md:977-984`; `build/ScorecardAxisCheck.md` §1,§4).
- C3 was added to `contract.md` before L1 measurement and is recorded as the
  corrective (`lessons/round-17.md` M5; `SCORECARD.md` r17 section lines
  added in `24526ea..273aa74` diff: "Calibration5 satisfies the lowest
  non-retired axis without a waiver"). A three-way tie is satisfied by any one
  5-axis claim. Observed: duty met, and the waiver's precondition is correctly
  not invoked (saturation 8, owned axes 6/7).
- Counterexample attempted: "C3 is retro-labeling, not a claim." The
  before→after is a genuine instrument delta (legacy pathspec emulation →
  default sweep), measured by committed receipts, not a paperwork rename. The
  residual weakness is at the *witness* level — see finding R2.

### 2. Finite capability vs bug claims

- C1 before: `seat-before/run-manifest.json` `summary.capability_absent=54`,
  tool path `.ufo/waves/round-17/frozen/absent-seat-tool.py`, `present:false`.
  The before is honest capability absence, not defect green; the lesson says so
  explicitly (`round-17.md` ¶"C1 entering capability absence is not54 old
  production defects"). After: `matched=54/54`, `mismatched=0` — verified by
  `jq '.summary'` over both committed manifests, and independently by
  `count-c1.json` (jq rc0, stdout `[54,0]`).
- C2 before: `jj-before/run-manifest.json` `totals.failed_assertions=21`
  (5 mismatch cases: git-detached-commit, git-detached-behind,
  git-report-off-branch, jj-commit-no-bookmark, jj-ambient-author — exactly the
  jj-colocation defects C2 claims); after: `failed_assertions=0`, 12/12 match.
  `count-c2.json` rc0 `[21,0]`. Frozen entering census verified byte-exact:
  `git show 24526ea:tools/mori-census.sh | sha256sum` =
  `f1f8d1b6…01ff7` == PINNED_INPUTS.
- C3: `c3-before.json` rc0 zero candidates with the exact r16 addendum pathspec
  (`--legacy-pathspec .ufo/waves .ufo/reports`, matching
  `build/MisrootR16Facts.md` §2, r16 receipt line 2 verbatim); `c3-after.json`
  rc1 exactly one candidate `MoriR16.Lesson`. `count-c3.json` rc0 `[1,0]`.
  Frozen witness sha256 `15f9f82d…510e` verified at HEAD (`git show
  HEAD:.ufo/waves/round-17/frozen/MoriR16.Lesson`) and matches the fleet
  artifact digest in `MisrootR16Facts.md` — byte-exactness confirmed.
- Counterexample attempted: "after-rc1 is a gate failure." rc1 is
  `MORI_MISROOT_CANDIDATE` = the detector's positive finding code (tool docstring,
  SKILL.md registry row); `c3-capture-recipe.json` expected `after_rc:1`.
  Consistent, not a false pass.

### 3. Old drift red unchanged

- `preservation.json`: 7 instrument/pin files sha-identical between `24526ea`
  and `273aa74`, `live_drift_rerun:false`, `baseline_repinned:false`.
- `r15-preserved.json` stdout retains `red_confirmed actual=fail` rows
  (boot-array/oom/foreignboot/fanout controls) — the old red is still red, not
  silently flipped. r13/r14 preserved gates rc0; `silence-oracle.json` rc0.
- `git diff 24526ea..273aa74 -- SCORECARD.md`: no score raised; every claim row
  says "held" (coverage6 held, operability7 held, calibration5 held). No
  premature saturation.

### 4. Procedural breaches disclosed

- Lesson records M8 (jj diff without --ignore-working-copy), M9
  (credential_pin grep exposure), M10 (overbroad selftest authorization),
  JjGate `/tmp/does-not-exist` accidental write (`build/JjGate.md:294-327`),
  wave2 preflight context-check failure
  (`evidence/context-check-wave2-original.json` rc1 → corrected rc0).
- Counterexample attempted: grep of 30+ `build/*.md` for breach vocabulary
  surfaced no undisclosed breach; `ls` of the fleet root shows no mori stray
  files (the three known root notes are absent per `MisrootR16Facts.md` §4).
- Wave-2 dispatch does not repeat M10: wave2 is report/scout/review seats plus
  four mutation seats; only `MutMisroot` carries an explicit copied-selftest
  grant (`wave2-dispatch.json`), consistent with the corrected policy
  ("selftest's existence is not permission" retained verbatim).

### 5. No claim rests on seat selftests

- All three counts are jq over gate-run `run-manifest.json` / probe stdout
  receipts committed under `evidence/`, labelled c1-before/after, c2-before/after,
  c3-before/after with recorded argv, rc, branch_ref `refs/heads/master`, and
  `measured_commit`/`branch_tip_after` = `273aa74`. Selftest receipts
  (`*-selftest.json`, `silence-oracle.json`, `*-preserved.json`) are separate
  labels and appear nowhere in `count-c{1,2,3}.json` argv. Observed: no count
  cell reads a selftest arm.
- Residual structural note: the gates themselves and `expected.json` are
  lane-authored; the counts are therefore self-instrumented (same posture as
  r13–r16). `lessons/round-17.md` correctly retains "Independent outside
  admit/reject spotcheck remains required; no SHONEN box or rank is
  self-certified" — admission cannot be self-completed. This critic confirms
  the receipts, not the admission.

### 6. No axis secretly harmed

- Depth/freshness: all preserved instruments byte-identical; r10 drift pin
  `corpus/evidence/baseline-r10-20261015T2231Z.json` unchanged; no journal
  probe was run for C2 (branch-anchored census reads local refs only).
- Coverage/operability: C1/C2 are the claims themselves; no overclaim
  (settle-window, terminal-at-scan, no-permanent-death, no-incident-count and
  no-authenticated-membership limits are in the tool `--help` text
  (`mori-seat-terminal.py:143`), the lessons, PROVINCE.md and corpus/README
  round-17 rows — consistent, no duplicate authority conflict found).
- Adjacency: `seat-live.json` reads sibling-lane transcripts but only as
  field-limited detection (keys verified: seat/key/kind/class/provider/model/
  error_status/error_code/retries/retry_exhausted/terminal_ms/reason — no
  errorMessage text, no content, no usage; `by_provider_model` verified).
  Prefix scope TabiR17/TsukuroiR17/SoujiR17-3 is disclosed in the lesson as
  observation, not lane action. Boundary statement retained in
  `lessons/round-17.md` cross-domain section.
- Calibration: A1 ordering verified in code — `(type=NNNN)` code test before
  quota tokens before 429/rate tokens (`mori-seat-terminal.py:263-273`,
  `QUOTA_CODES={1113,1308}`, `RATE_CODES={1302}`) matching `contract.md`
  Amendment A1 items 1 and 10; fixture cases `code_quota_1113_beats_429`,
  `code_quota_1308_beats_429`, `code_rate_1302_beats_quota_token`,
  `rate_limit_beats_quota_by_status_and_token` all matched 54/54.
- Diff scope: `git diff --stat 24526ea..273aa74` touches only lane files
  (tools, .ufo/waves/round-17, corpus, LOG/SCORECARD/PROVINCE/SKILL/README);
  no MANIFEST.json, .ufo/state, fleet-root or sibling-lane path. Post-measure
  commit `5c1dfb8` adds receipts only; all 9 PINNED_INPUTS digests re-verified
  at `5c1dfb8` (sha256 over `git show HEAD:<path>`) — the measured artifacts
  are unchanged at current tip.

## Residual findings (non-blocking)

- **R1 (weakest defect, cosmetic-provenance):** fixture case id
  `rate_limit_beats_quota_by_status_and_token` (`.ufo/waves/round-17/fixtures/
  seat/expected.json`) asserts `dead_quota` for both seats — i.e. the A1
  quota-beats-429 ordering — while its name still asserts the pre-A1
  rate-limit-beats-quota ordering. A closure reviewer reading ids rather than
  `want` blocks sees the case table contradict A1. Smallest correction: note
  the stale id in the lesson/closure, or rename the id and re-pin
  `expected.json` (renaming invalidates the current pin `b684c63b…`).
- **R2 (witness-scope residual):** C3's committed witness detects the artifact
  by `matched_in:["path"]` only (`c3-after.json` stdout; expected in
  `c3-capture-recipe.json` `after_matched_in:["path"]`), because the byte-exact
  retained file names neither lane nor round in content
  (`MisrootR16Facts.md:48-50`). The "or-content" branch of the detector is
  exercised only in selftest arms and the wave-2 MutMisroot probe, not in the
  admission witness. This is the honest maximum the frozen artifact allows —
  flagging so the closure does not read "filename-or-content" as witnessed
  both ways.
- **R3 (scratch-provenance residual):** C2/C3 sandboxes ran under
  `.ufo/worktrees/round-17/MainChecks/` (receipt argv), a name absent from
  wave1-assignments.json — an L1-internal scratch dir, now removed (only
  Mut* clones remain). Harmless because `.ufo/worktrees/` is gitignored
  (`.gitignore:2`) and commits show no worktree content, but the scratch path
  is not covered by the per-seat clone contract; [INFERENCE] it was L1's own
  measurement scratch.

## Hygiene

No tools installed or upgraded (none needed). No background jobs, no journalctl,
no pacman transaction, no /tmp or fleet-root writes, no VCS mutation
(`git log/show/diff/rev-parse/status/sha256sum` reads only). Untrusted transcript
content was never opened; only committed receipt JSON and tool source were read.
