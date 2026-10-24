# QualityCriteriaDraft — round 17 draft criteria Q43–Q48 (draft only; QUALITY.md not edited)

Seat: MoriR17.QualityCriteriaDraft-5. Scope: draft criteria for `corpus/QUALITY.md` from six named lessons. Nothing was admitted or written to `corpus/`.

## Ground facts (observed)

- `corpus/QUALITY.md` is 110 lines. Highest criterion number is **42** (`corpus/QUALITY.md:106–110`, "42. Exact anchor start..."). Drafts start at 43.
- Existing overlapping criteria: #4 (errata append-only, `QUALITY.md:4`), #16 (kill unit and scope, `:31–33`), #34 (counted unit and validation scope, `:82`), #36 (source labelling, `:91`), #37 (dispatcher messaging restriction, `:96`), #40 (registry row swept, `:102`), #41 (drift re-pin, `:104`).
- Commands run (all read-only, exit 0 unless stated): `wc -l`, `grep -n`, `sed -n`, `cut`, `cat`, `head -c`, `sha256sum`, `stat -c`. One `mkdir -p` on the existing build directory (no-op). No VCS command, no journal query, no `/tmp` write, no installs or updates. No tool install or update was made.

## Draft criteria

### 43. A misroot sweep covers the fleet root with no pathspec

A misroot sweep of the fleet root runs `git -C <fleet> status --porcelain` with no pathspec. A sweep limited by a pathspec (for example `-- .ufo/waves .ufo/reports`) can miss a file written directly at the fleet root. Its clean result is not cited as a fleet-root misroot sweep.

- Source: `lessons/round-16-verifier-spotcheck.md:202–209`. Item 1 found a fleet-root `MoriR16.Lesson` that the pathspec sweep did not show. The lesson says "Future sweeps run `git -C <fleet> status --porcelain` with no pathspec."
- Corroboration: `lessons/round-16.md:244` (M33). Round-16 `evidence/misroot-sweep.json` records `"command": "git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/waves .ufo/reports"`, exit 0, with `?? .ufo/waves/...` lines only. Observed.
- Falsifier: a sweep receipt whose argv contains a pathspec, cited as a clean fleet-root sweep.
- Overlap: #19 (inspect nonzero sweep hits) is about hit inspection, not coverage. #43 covers coverage.

### 44. Each wave spec gets a pre-dispatch context-check receipt bound to its sha256

Before dispatch, each wave spec is run through the context checker. The receipt records the checked spec's `sha256`, the finding, and the time. Dispatch cites only a receipt whose `spec_sha256` equals the dispatched spec's bytes. A `CONTEXT_MISSING` receipt blocks dispatch until a corrected spec gets its own receipt. A green receipt is a static check, not runtime prevention (`claims_runtime_prevention: false`).

- Source: `lessons/round-16-verifier-spotcheck.md:216–219` ("Run ... on every wave spec **before** dispatch and record its receipt. A green check is still not runtime prevention."). Same L1-omission class as `lessons/round-15-verifier-spotcheck.md:260–266` (C15-1).
- Round-16 observed: `evidence/context-original.json` exit 1, `CONTEXT_MISSING ["no_live_journal_queries"]`. Corrected receipt `context-corrected.json` exit 0, `CONTEXT_OK`.
- Round-17 observed (`.ufo/waves/round-17/evidence/`):
  - `context-check-wave1-original.json`: `CONTEXT_MISSING`, `missing: ["no_tmp_probe_outputs"]`, `spec_sha256 1f58858…`, mtime 15:37:52.
  - `context-check-wave1.json`: `CONTEXT_OK`, `spec_sha256 6969eb19…`, mtime 15:38:01.
  - `sha256sum wave1-spec.json` = `6969eb19…` (equal to the green receipt). `wave1-spec.json` mtime 15:38:00.9; `wave1-dispatch.json` mtime 15:38:06.
  - Mtime order is an observation, not proof of sequence [INFERENCE].
- Not interpreted: `wave1-dispatch-attempts.json` records `refused: 70` in four attempts and `refused: 0` at 15:52:53. The field's meaning is not read here; the dispatcher is not established as the cause [INFERENCE].
- Scope note: the round-17 receipt covers wave 1 only. Per-wave coverage is the criterion's requirement, not an observation about later waves.
- Falsifier: a dispatch whose spec `sha256` has no `CONTEXT_OK` receipt, or whose receipt hash differs from the dispatched bytes.

### 45. Probe disclosures enumerate every probe and write, not a subset

A self-disclosure names every probe by command class: live host queries (including failed or rc≠0 ones), file writes, background jobs, and out-of-lane paths. A "no live query" statement is scoped to the commands the seat actually ran. A disclosure that names only part of its own probe section is a precision defect. It is corrected by an appended note, not by silent expansion. Disclosure is not prevention.

- Source: `lessons/round-16-verifier-spotcheck.md:210–215` (item 2). M7 in `lessons/round-16.md:51` cites only `BootContinuity.md:31–32` (`/tmp` writes, `bg_2667`). The seat's `## Host probe` (`BootContinuity.md:19–28`) also records live system-journal queries (`-b -n 2`, an anchor `--cursor` query, a fabricated-cursor query returning rc1, `--user -n 1`), which the verifier says are unauthorized live probes. The verifier asks for an appended precision correction.
- Corroboration: `lessons/round-15-verifier-spotcheck.md:244–245` ("Procedural-disclosure precision still requires the appended correction").
- Falsifier: a seat's probe section lists more commands than its disclosure names.
- Overlap: #24 (empty-by-removal disclosure) and #36 (source labelling) are different concerns. #45 covers the completeness of the disclosure itself.

### 46. Stale wording is superseded by appended note, and the correction sweep covers active prose

When a later artifact contradicts earlier prose (a pending lesson row, a knowledge `verified-at` line, a PROVINCE.md status, an active SKILL.md registry row), the earlier text is kept. A dated appended note names the superseding artifact by path, commit, or receipt. A correction sweep covers active registry and index prose, not only lessons. Stale active text found at read time is a finding for that read.

- Sources:
  - `lessons/round-16-verifier-spotcheck.md:220–223` (item 4): `PROVINCE.md` "verification pending" and a knowledge `verified-at` line that conflicts with the lesson's host version. "Supersede both with an appended note ... Do not rewrite history."
  - `lessons/round-15-verifier-spotcheck.md:282–289` (item 4): `SKILL.md:134` stale after the delivered change; the correction sweep missed active registry prose.
  - `lessons/round-14.md:37`: "This entry supersedes ... It does not rewrite those records."
  - `lessons/round-16.md:121` (stale knowledge line routed, not edited) and `:218` ("superseded here").
- Overlap: #4 (append-only errata) is the general rule. #40 covers registry rows when a gate changes. #46 adds the requirement that the sweep reach active prose and that supersession be a dated note. Recommendation [INFERENCE]: fold #46 into #4 as an amendment rather than a separate number, to avoid a near-duplicate.
- Falsifier: an active document still asserts a claim that a cited later artifact contradicts, with no superseding note.

### 47. VCS progress and closure reads are branch-anchored under jj, not bare HEAD

Under jj colocation, a probe that grades lane progress, report closure, or authorship reads `refs/heads/<branch>`. The branch is resolved as `scripts/hyaku/jj-lane.sh detect_branch` does (`symbolic-ref`, then `refs/remotes/origin/HEAD`, then unique `master`/`main`). A bare-`HEAD` read is allowed only as a presence or format check, and its output states the HEAD-vs-branch caveat. A gate's start/end revision pin is not asserted equal to branch tip without measurement.

- Source (not a lesson; an audit report): `.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md:62–78` (F3). After `jj commit`, HEAD is `d19d559` while `master` is `611dfb5`. Git-mode `commit` moves HEAD and the branch atomically; under jj the bookmark moves in a separate `jj bookmark set`. Observed in that sandbox only. Generality across lanes is [INFERENCE].
- Census rows affected: `JjAuditMori.md:213–230` (census rows 1, 2, 5, 6, and D-class regression pins at rows 10–18). Mitigation: `JjAuditMori.md:251–260`.
- Interface: `.ufo/waves/round-17/contract.md:80–90` (C2). Gate: `tools/mori-round17-jj-regressions.py` (not yet delivered; no result is cited here).
- No `lessons/` file yet covers this. Admission needs a round-17 lesson with a measured receipt.
- Falsifier: a census probe that grades progress or closure from `HEAD` under a jj lane without a caveat; or a gate that pins HEAD as the branch tip with no measured divergence.

### 48. A seat's terminal state is not an incident count

A seat's terminal class (`completed`, `dead_rate_limit`, `dead_quota`, `dead_error_other`, `aborted`, `incomplete`, `unavailable`) counts seats whose last observed transcript record is in that state. It is not an incident count, a failure count, a retry count, or proof that the seat will not resume. Any cited number names its unit (seat, record, or incident) and its scope (prefix, provider/model, sessions directory). Dead-state totals are not summed across scopes into an incident figure.

- Sources:
  - `.ufo/waves/round-17/contract.md:14–15` (motivation: zai `429 ... (type=1302)` deaths, "Retry budget exhausted after 10 retries"; the tool exists to detect and report, not to re-route).
  - `.ufo/waves/round-17/contract.md:65–67` (the tool's `--help` must state: the terminal error is the last observed state, not proof of no resume; "dead counts are seats, not distinct incidents"; prefixes are naming conventions, not authenticated membership).
  - Existing criteria: #16 (`corpus/QUALITY.md:31–33`, "a kill count names its unit ... scopes are never summed", source `lessons/round-12.md#M19`); #34 (`:82`, counted unit; source `lessons/round-15.md#M2`).
- No round-16 or round-17 lesson yet covers seat terminal state. Admission needs one, plus the measured C1 gate receipt. The current source is the contract and the prior unit-discipline criteria [INFERENCE].
- Falsifier: a report that equates `totals.dead_*` with incidents, or sums `by_prefix` dead counts into an incident figure.

## Admission notes

- Each draft has a falsifier and a cited source path. Per the admission bar (`QUALITY.md:3–5`), observation, inference, and unknown are kept separate in this report.
- #47 and #48 are not yet backed by a lesson; they are drafts pending round-17 receipts.
- #43–#46 are backed by lessons already in `corpus/lessons/` or the round-16/15 verifier spot-checks (`corpus/lessons/round-16-verifier-spotcheck.md`, `corpus/lessons/round-15-verifier-spotcheck.md`).
- Recommendation: admit #43, #44, #45, #46 with the fold-into-#4 note; hold #47 and #48 until their round-17 receipts exist.

## Residuals

- Not read: the body of `wave1-dispatch-attempts.json` field semantics (see #44).
- Not verified: the round-17 gate outputs (C1 and C2), which had not been delivered at the time of this read.
- Not verified: whether `tools/mori-round16-context-check.py` is currently green; only the recorded receipts were read.
