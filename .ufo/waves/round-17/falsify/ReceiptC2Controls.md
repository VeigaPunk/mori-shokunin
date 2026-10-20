# ReceiptC2Controls — C2 before/after assertion recount, fail-only-before cases and controls

Seat: `MoriR17.ReceiptC2Controls-4` (leaf, no dispatch). Date 2026-10-20.
Scope attacked: the settled C2 operability evidence only — the paired
`jj-before`/`jj-after` gate receipts and their exact retained census streams.
Base for all relative paths: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
No diagnosis, no re-run of the live probe, no mutation, no VCS command beyond
read-only `git show`/`cat-file`/`cmp`.

Verdict: the declared C2 count **21 → 0 failed assertions is reproduced exactly**
from the retained manifests, with 5 cases failing only before, 7 controls
passing both sides, and every retained stdout digest matching its manifest.
Four qualifications/bounds below are real but none changes the admitted numbers.

## 1. Recount (authoritative source: both `run-manifest.json`)

Receipts: `evidence/c2-before.json` (rc1), `evidence/c2-after.json` (rc0),
`evidence/count-c2.json` (rc0, stdout `[21,0]`).
Manifests: `evidence/jj-before/run-manifest.json`,
`evidence/jj-after/run-manifest.json`.

| case | before assert/failed/status | after assert/failed/status |
|---|---|---|
| git-plain-progress | 10 / 0 / match | 10 / 0 / match |
| git-detached-at-tip | 10 / 0 / match | 10 / 0 / match |
| git-detached-commit | 10 / **5** / mismatch | 14 / 0 / match |
| git-detached-behind | 10 / **4** / mismatch | 10 / 0 / match |
| git-report-on-branch | 10 / 0 / match | 10 / 0 / match |
| git-report-off-branch | 10 / **4** / mismatch | 10 / 0 / match |
| git-foreign-author | 10 / 0 / match | 10 / 0 / match |
| jj-helper-commit | 11 / 0 / match | 11 / 0 / match |
| jj-commit-no-bookmark | 11 / **5** / mismatch | 15 / 0 / match |
| jj-ambient-author | 11 / **3** / mismatch | 13 / 0 / match |
| jj-sibling-author | 11 / 0 / match | 11 / 0 / match |
| git-fallback-head | 10 / 0 / match | 10 / 0 / match |
| **totals** | **124 / 21 / 7 match 5 mismatch** | **134 / 0 / 12 match** |

Sum reconciliation: 70 (7 git cases ×10) + 44 (4 jj cases×11) + 10 = 124;
after = 124 + 4 (case 3 detail) + 4 (case 9 detail) + 2 (case 10 detail) = 134.
Declared `totals` equal these recounts on both sides (`failed=21`/`failed=0`,
`failed_cases=5`/`0`); gate exit 1→0 is consistent with
`tools/mori-round17-jj-regressions.py:1301,1315` (exit 0 iff 0 failed).
Case ids and all 12 `description` strings are byte-identical across sides
(`diff` of the two extracted lists: `IDENTICAL_DESCRIPTIONS`).
Same gate bytes on both sides: `gate.sha256=1067e4ae…0e3` in both manifests,
equal to `PINNED_INPUTS.json` and to `git show 273aa74:tools/mori-round17-jj-regressions.py`.

## 2. Cases that fail only before (exactly 5; none fails only after)

Failed-assertion ids are quoted from the manifests; the observed rows are quoted
from the retained per-case streams (`cases/<id>.out`, line anchors given).

1. `git-detached-commit` — 5: `census_exit`, `verdict_roll`, `lane_state`,
   `lane_basis`, `finding:HEAD_BRANCH_MISMATCH:present`.
   before: `cases/git-detached-commit.out:8` `SURFACE lane.alpha: progressing (… basis=row-A …)`,
   `:13` `MORI_CENSUS: CLEAN (findings=2 drift=0 …)`.
   after: `jj-after/cases/git-detached-commit.out:8` `silent (… basis=row-D …)`,
   `:13` `FINDING HEAD_BRANCH_MISMATCH severity=warn obs=lane=alpha head=53923a1e5915
   branch=master branch_tip=0cbec284382d basis=merge-base-not-ancestor`, `:15` `DRIFT (findings=4 drift=2 …)`.
2. `git-detached-behind` — 4: `census_exit`, `verdict_roll`, `lane_state`, `lane_basis`.
   before `:8` `silent (… basis=row-D …)`, `:14` `DRIFT (findings=3 drift=1 …)`.
   after `:8` `progressing (… basis=row-A …)`, `:13` `CLEAN (findings=2 drift=0 …)`.
3. `git-report-off-branch` — 4: same four ids.
   before `:8` `not-open (… basis=row-6 reason=committed-report …)`, `:13` `CLEAN`.
   after `:8` `silent (… basis=row-D …)`, `:14` `DRIFT (findings=3 drift=1 …)`
   (LANE_SILENT; row-6 closure no longer matched off-branch).
4. `jj-commit-no-bookmark` — 5: `census_exit`, `verdict_roll`, `lane_state`,
   `lane_basis`, `finding:HEAD_BRANCH_MISMATCH:present`.
   before `:8` `progressing-weak (… basis=row-C …)`, `:13` `CLEAN`.
   after `:8` `silent (… basis=row-D …)`, `:13` `HEAD_BRANCH_MISMATCH … head=6e2e721c8781
   branch=master branch_tip=0cbec284382d …`, `:15` `DRIFT (findings=4 drift=2 …)`.
5. `jj-ambient-author` — 3: `census_exit`, `verdict_roll`,
   `finding:LANE_AUTHOR_MISMATCH:present`.
   before `:8` `progressing-weak (… row-C …)`, `:13` `CLEAN`.
   after `:12` `FINDING LANE_AUTHOR_MISMATCH severity=warn obs=lane=alpha count=1
   committer=alpha-shokunin <alpha@shokunin.local> window=launch..NOW
   basis=committer-lane-author-foreign-email`, `:14` `DRIFT (findings=3 drift=1 …)`.

These are exactly the C2 changes: rows 6/9 anchored on `refs/heads/<branch>`
(`tools/mori-census.sh:2304-2312` report/author scan; `:2443`, `:2446` finding
emission-after-grading) and the two new warn findings. No other case changes side.

## 3. Controls — all pass on both sides (7/7)

Verified at both manifest and exact-stream level; every control has `failed=0`,
`rc=0`, and neither `HEAD_BRANCH_MISMATCH` nor `LANE_AUTHOR_MISMATCH` present
(`finding:*:absent` ok=true in both manifests).

| named control | id | before / after row (stream line) |
|---|---|---|
| plain git, on-branch lane commit | git-plain-progress | `progressing row-A`, `CLEAN (findings=2 drift=0)` both (`:8`, `:13`) |
| detached exactly at branch tip | git-detached-at-tip | `progressing row-A`, `CLEAN` both (`:8`, `:13`) |
| sibling-shokunin author, lane committer | jj-sibling-author | `progressing-weak row-C`, `CLEAN`, author finding absent both (`:8`, `:13`) |
| unresolved branch → entering HEAD anchor | git-fallback-head | `progressing row-A`, `CLEAN`, no C2 finding both (`:8`, `:13`) |
| report committed on root branch | git-report-on-branch | `not-open row-6`, `CLEAN` both (`:8`, `:13`) |
| ambient author **and** committer | git-foreign-author | `progressing-weak row-C`, `CLEAN`, author finding absent both (`:8`, `:13`) |
| helper shape (metaedit/commit/bookmark) | jj-helper-commit | `progressing row-A`, `CLEAN` both (`:8`, `:13`) |

This covers every control named by `build/ReviewC2Metric.md` (helper, detached-at-tip,
plain attached, on-branch closure, no-false-author) plus the A1 sibling negative
(`contract.md:122`) and the unresolved-branch fallback (`contract.md:122`).

Non-vacuity of the negative controls comes from the after side (the finding exists
there) and from the retained gate self-test
`evidence/jj-gate-selftest.json` rc0, whose stdout names
`ok_mismatch_finding,ok_mismatch_severity,ok_author_finding,ok_sibling_negative,ok_fallback_head,head_rc1,head_names_missing_mismatch,head_failed_assertions,absent_rc1,absent_capability_absent`.

## 4. Integrity checks performed (all rc0, read-only)

- Before census identity: `cmp` of
  `git show 24526ea9617cd020fee16c28fe4d4a2789dc28cb:tools/mori-census.sh`
  vs `frozen/mori-census.sh` → `IDENTICAL`; both sha256 `f1f8d1b6…1ff7`, equal to
  `PINNED_INPUTS.json`. `c2-before.json` argv passes the frozen path, not the
  `git show` path; bytes are the entering census, so the contract command is
  satisfied in substance.
- After census identity: `tools/mori-census.sh` sha256 `12e8e2d9…6d85` = `PINNED_INPUTS`
  = `git show 273aa74:tools/mori-census.sh`.
- In-stream self-proof: every one of the 24 `cases/*.out` carries
  `script_sha256=` values unique to `f1f8d1b6…` (12 before) or `12e8e2d9…`
  (12 after) — the bytes that actually executed match the pinned revisions.
- Stream integrity: all 24 `census_stdout_sha256` values equal the sha256 of the
  retained `cases/<id>.out`.
- Receipt hashes: sha256 of the exact `.stdout`/`.stderr` strings recomputed from
  JSON equals the recorded `stdout_sha256`/`stderr_sha256` for
  `c2-before`, `c2-after`, `count-c2`; `count-c2` stdout recomputed from the two
  manifests is `[21,0]` and hashes to `49fa16b5…7085`.
- Independent assertion audit over all 258 assertions (124+134): every
  `census_exit|verdict_roll|lane_state|lane_basis` `ok` equals its detail
  `X==expected`; every `:present`/`:absent` equals stdout finding membership;
  `:severity` equals the emitted severity; all 7 `:obs_contains:` needles are
  substrings of the emitted obs; `failed_assertions` equals the count of non-ok
  checks; `status=match` iff 0 failures. Result: `AUDIT OK`, 0 problems.
- Verdict cross-check: each stream has exactly one `MORI_CENSUS:` line; its
  `findings=` equals the FINDING-line count, `drift=` equals warn+crit count,
  and surface state/basis equal the manifest `observed` values.
- Read-only proof: `refs_unchanged` ok in 24/24 cases
  (`tools/mori-round17-jj-regressions.py:1243,755,774`); `jj_config_redirected`
  ok 8/8.
- No `fatal|error:|cannot|not a git repository|permission denied|command not found|syntax error`
  tokens in any retained stream.

## 5. Qualifications and defects found (none overturns 21→0)

- **Q1 denominator asymmetry (disclosed, not hidden).** The before side has 124
  assertions, the after 134, because `evaluate()` emits `:severity` and
  `:obs_contains:` checks only when the required finding is present
  (`tools/mori-round17-jj-regressions.py:778-798`, `if not present: continue`).
  The +10 are exactly 4 (case 3) + 4 (case 9) + 2 (case 10). Under a single
  assertion universe the before count would be 31 (21 observed + the 10
  suppressed detail checks, which would also fail on absence). So 21→0 is a
  conservative lower bound, not an inflated delta, and `corpus/lessons/round-17.md:126-128`
  states the reason. The 7 control cases keep identical assertion-id sets across
  sides (verified per case), so no control's checks were removed or weakened.
- **Q2 build-report quotes are from a different census than the admitted after
  run.** `build/JjGate.md:27-28` records the reference scratch census sha256
  `33e2120a…bc56c` (12/12, 134, 0), while the delivered census is `12e8e2d9…6d85`
  and the admitted receipt `evidence/c2-after.json` ran the delivered file.
  Consequently the "exact reference lines" at `build/JjGate.md:173-180` are not
  delivered output: delivered emits `count=1 committer=… window=launch..NOW
  basis=committer-lane-author-foreign-email` and `basis=merge-base-not-ancestor`,
  not the quoted `commits=1 rule=…` / `rule=merge-base-is-ancestor`.
  `build/JjGate.md:130-143` also labels cases 3/9 "DRIFT 1", while delivered
  stdout is `drift=2` (LANE_SILENT + HEAD_BRANCH_MISMATCH, both `warn`).
  The gate asserts only roll, severity and the three obs needles, all of which
  the delivered bytes satisfy (`jj-after` 134/0), so the count stands; the build
  report's prose must not be cited as the delivered stream.
- **Q3 sandbox retention.** The `MainChecks` run trees are gone
  (`ls -d .ufo/worktrees/round-17/MainChecks/jj-{before,after}/run-*` rc1), so the
  expected short head/branch needles cannot be re-derived from live sandbox refs.
  They are nevertheless cross-consistent: the manifest `observed.refs` record
  `lane.head=53923a1e…` / branch `0cbec284…` (case 3) and `6e2e721c…` / `0cbec284…`
  (case 9), matching the emitted `head=`/`branch_tip=` tokens and the gate's
  `mismatch_requirement()` read of the same sandbox
  (`tools/mori-round17-jj-regressions.py:506-515`, called before the census run).
- **Q4 coverage bounds of "12/12".** The 12 cases do not exercise:
  (a) `origin/HEAD` resolving to a branch with no local `refs/heads/<b>` —
  `lane_branch_probe()` accepts `refs/remotes/origin/*` without checking the local
  ref (`tools/mori-census.sh:2122-2129`), then `rev-parse refs/heads/<b>` fails
  (`:2308-2312`), leaving `has_head=0` and falling to row B/D `silent`
  (`:2408`) rather than `unavailable`; `build/CriticC2.md:119-123,156-158` (O4)
  asked for unavailable and the delivered file has no `branch-unresolved` /
  `branch-ref-missing` token (grep, 0 hits). `build/JjGate.md:96` states
  "no remote is configured in any sandbox; `refs/remotes/origin/HEAD` is absent",
  so this arm is structurally unreachable in the gate.
  (b) the mixed-basis case (`build/CriticC2.md:56-74`, H1: row B index under a
  branch mismatch) and (c) a lane on `main` whose root is on `master` for row 6
  (`CriticC2.md:103-107`, O2; the code does probe `$ROOT` separately at
  `mori-census.sh:2293-2296`, but no case pins it). These are untested paths, not
  refutations of the five fixed scenarios; they bound what 12/12 proves. [INFERENCE]
- **Q5 scratch placement.** Both receipts used `--scratch
  .ufo/worktrees/round-17/MainChecks/jj-*`, i.e. inside the lane checkout, while
  `contract.md:99-101` says sandboxes go in "its own temp tree (never in the lane
  or fleet)". Isolation is otherwise real: per-case `HOME`/`XDG_CONFIG_HOME`/
  `JJ_CONFIG`/`GIT_CONFIG_GLOBAL`, `GIT_CEILING_DIRECTORIES`, every non-init jj
  call with `-R` (`tools/mori-round17-jj-regressions.py:181-205,249-256`), and
  `refs_unchanged` 24/24. Observed placement; L1 decides the literal-text issue.
- **Q6 before-side control vacuity.** In the entering census neither new finding
  can exist, so `finding:*:absent` on the 7 controls is trivially true before;
  only the after side plus the retained gate self-test (Q3/non-vacuity above)
  makes those negatives meaningful. This does not weaken the control claim
  (they must pass both, and they do), it only bounds what the before pass proves.

## 6. Residual unknowns

- Whether a fresh sandbox rebuild reproduces the identical 21-failure set: not
  re-run (counting commands only over committed receipts; no live probes).
- Whether the origin/HEAD-missing-local-ref state (Q4a) has been observed live:
  not measured here. `build/CriticC2.md:104-107` says six detached colocated lanes
  resolve via `origin/HEAD`, but no live check of local-ref presence was performed
  in this seat.
- Census procedure timing/`now` drift: before `now` = 1792516897, after 1792516899
  (`launch_epoch` in the streams); both sandboxes are rebuilt per run, so the
  paired comparison is scenario-level, not byte-level sandbox identity.
- No LSP device is mounted for this seat; source claims above are direct reads of
  committed files at the cited lines, not grep-derived semantic claims. Grep was
  used only to locate candidate lines.

## 7. Commands (all read-only; rc0 unless noted)

- `jq` recounts/extractions over both `run-manifest.json` (rc0; totals above).
- `sha256sum`, `cmp`, `git show <rev>:<path>`, `git cat-file -e <rev>:<path>` (rc0).
- Python stdlib audit of all 258 assertions vs retained streams → `AUDIT OK`.
- `ls -d .ufo/worktrees/round-17/MainChecks/jj-{before,after}/run-*` → rc1 (absent).
- No gate, census, selftest, probe or live command was executed; no tool installed
  or upgraded.
- **Procedural violation (disclosed, not prevention):** one shell pipeline at
  16:47 wrote a 4,722-byte scratch file `/tmp/x` (assertion-id lists derived from
  the committed manifests; no credential or transcript content). It was my own
  file, removed at 16:54; it is not measurement evidence. This is the lane's
  forbidden `/tmp` scratch shape and is recorded here rather than excused.
