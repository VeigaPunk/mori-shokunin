# JjGate — C2 jj-colocation regression gate, falsification-driven revision

Seat: `MoriR17.JjGate-5` (executor, leaf). Date 2026-10-20.
Assigned clone recreated at base `5c1dfb8`; own only
`tools/mori-round17-jj-regressions.py` plus this report.

Deliverable (the only implementation file written this pass):

```
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/JjGate/tools/mori-round17-jj-regressions.py
sha256 da3e080aa5181e8e00872c1d5f0dd97862c495da03adce0b1aa31e27fbcb89f0
2028 lines / mode 0755
```

**No test was run this pass** (L1 executes settled commits). Every count below
is an *unexecuted prediction from the assertion construction*, not a
measurement. The only commands executed against the file were static syntax
checks (`ast.parse` and `bash -n` of the extracted fixture string, both rc0);
no census, gate run, jj or git command was executed. No tool was installed or
upgraded.

## What changed, and for which falsification

### 1. SandboxFinal F2 — output and scratch are constrained

`--output` is validated **before any mkdir/write**:

- rejected if it is a symlink (including dangling), exists as a non-directory,
  or exists as a non-empty directory (`check_output_path`, `:1186`);
- rejected if it equals or is an ancestor of any source/census repo root, or
  lies inside protected `tools/`, `corpus/`, `.git/`, `.jj/`, or `.ufo/` —
  **`.ufo/waves/` is deliberately allowed** as lane evidence;
- rejected if it overlaps the census input or the gate source.

`--scratch` is validated before any write (`check_scratch_path`, `:1202`):

- symlink / non-directory rejection, `/` rejection;
- reject `/tmp` and `/var/tmp` (and everything below them);
- reject protected/input overlaps and the output's own `cases/` or
  `run-manifest.json`;
- a child of `--output` (the default `<output>/scratch`) is accepted.

A fresh gate-owned `run-<UTCstamp>-<pid>-<n>` child is created with `os.mkdir`
(`make_run_dir`, `:1219`), never reusing an existing entry.

### 2. SandboxFinal F4 — explicit retention policy

The run sandbox is removed by default before the manifest is written (so
`retained`/`retention.cleanup` are accurate); only the fresh run child is
removed (never output, the scratch parent, or anything else). `--keep-scratch` opts into forensic retention. The manifest now records:

```
"retained": true|false,
"retention": {"policy": "cleanup"|"keep", "cleanup": "removed"|"kept"|"failed",
              "scratch_run": "<path>"},
"scratch_run": "<path>"
```

Per-case `sandbox` paths are recorded only when retention is requested
(otherwise `null`, so a cleaned run never advertises stale paths). If cleanup
fails, `retained` flips true and `cleanup_error` is recorded.

### 3. PatternConsistency C2 — exact receipt fields, not short-hash substrings

`HEAD_BRANCH_MISMATCH` is now asserted against the census's own grammar
(`mori-census.sh:2443`):

- `head=<first 12 hex of the full HEAD OID>`
- `branch_tip=<first 12 hex of the full refs/heads/<branch> OID>`
- `basis=merge-base-not-ancestor`

The expected values come from `_oid12()` (`:274`), which resolves the **full**
OID and slices 12 characters; `rev-parse --short` is no longer used as an
oracle. Tokens are compared as exact whitespace-separated tokens, not
substrings. `LANE_AUTHOR_MISMATCH` is asserted against `mori-census.sh:2446`:
`lane=<id>`, `count=1`, `basis=committer-lane-author-foreign-email`.

### 4. ReceiptC2Controls Q1 — one assertion universe on both sides

`evaluate()` (`:968`) now emits the presence, severity, token, and substring
checks for every required finding **even when the finding is absent**; a
missing finding fails every one of its checks instead of shrinking the
denominator. The before and after runs now have identical assertion counts.

### 5. CensusJj A2 — authoritative lane.branch mirror, fail-closed

The gate encodes the resolver semantics confirmed by `MoriR17.CensusJj-5`:

- a `.jj`-colocated lane requires `git config lane.branch <b>` naming an
  **existing** ref; missing/invalid/missing-ref grades `SURFACE lane.<id>:
  unavailable (... basis=row-1 reason=ref-unresolved ...)`, with **no HEAD
  fallback and no C2 finding**;
- a non-jj lane uses the mirror only when valid, else attached HEAD ->
  `refs/remotes/origin/HEAD` -> unique `master`/`main` -> the unchanged
  entering HEAD fallback;
- a jj fleet root with an unusable mirror makes row-6 closure **skip** (never
  HEAD), so an off-branch report cannot close the lane.

All normal jj controls now set the helper mirror exactly as
`scripts/hyaku/jj-lane.sh:439` does (`git config lane.branch master`,
`set_lane_branch`, `:287`).

### 6. CensusNewBranches — diagnostics survive early returns

Both C2 diagnostics are computed and emitted before the row/young/report-closed
returns. A new young-case fixture (`launch age < 7200 s`) proves
`LANE_AUTHOR_MISMATCH` is still a warn while the lane surface is `young`
(row-8). `set_launch_age` (`:298`) rewrites the ledger anchor for that case.
The adult ambient-author case and its controls are unchanged, so the young
scenario is genuinely new rather than a re-labelled control.

### 7. `--selftest` arms added (no test executed here)

`run_selftest` (`:1484`) now also contains arms that (when L1 executes the
settled commit) prove:

- output/scratch guard arms over an isolated synthetic repo (repo root,
  `tools/`, `corpus/`, `.git/`, `.jj/`, `.ufo/state`, `.ufo/waves` allowance,
  non-empty dir, symlink, ancestor, gate source, scratch under `/tmp`, scratch
  input-file/ancestor, valid scratch);
- exact-field arm: a `MODE=wrongtip` fixture emits `branch_tip=` one character
  short, and the gate must name the failed exact-token check;
- fixed-universe arm: compliant / HEAD-mutant / wrongtip manifests must have the
  same `totals.assertions`;
- retention arms: default run `retained=false` and the run tree gone; a
  `--keep-scratch` run `retained=true` and the run tree present;
- raw-argument symlink arms with an untouched empty sentinel:
  `--output <symlink>`, `--output <nested-symlink>/newout`, and
  `--scratch <symlink>` each return 2 and leave the sentinel tree unchanged;
- the existing missing-census `capability_absent` arm.

The selftest temp parent comes from `--scratch` or `TMPDIR`, and `/tmp` /
`/var/tmp` are refused. Suggested settled-commit command:
`python3 tools/mori-round17-jj-regressions.py --selftest --scratch .scratch`
from the clone (L1 executes).

### 8. Residual — raw symlink arguments

`main` previously resolved `--output`/`--scratch` before the guard, so a raw
symlink argument was followed by `resolve()` and `is_symlink()` was false on
the resolved path. Now `main` anchors a relative arg at cwd **without**
resolving, checks the raw path and every existing ancestor
(`_has_symlink_component`, `:1188`) plus a `..` refusal, and only then
canonicalises for the containment checks. The selftest subprocess arms above
are designed to prove this end-to-end (not executed here): the gate must
return 2 and the empty sentinel target must be unchanged for final-symlink,
nested-symlink and scratch-symlink args.

## Interface (unchanged shape)

```
mori-round17-jj-regressions.py --census PATH --output DIR [--scratch DIR] [--keep-scratch]
mori-round17-jj-regressions.py --selftest [--scratch DIR] [--keep-scratch]
```

A fresh, empty `--output` is required per run (F2); the standard receipt
directory must be absent or empty before the run. Exit 0 only when every
assertion holds; 1 on any failed assertion/capability gap; 2 on gate setup
error.

## Cases (17) and unexecuted expectations

`B` = predicted against the frozen entering census `f1f8d1b6…1ff7`
(no lane.branch support); `A` = predicted against the settled A2 census.
All case expectations are shared by both sides, so the assertion count per case
is identical.

| # | case | expected after (A) | B prediction |
|---|---|---|---|
| 1 | git-plain-progress | progressing row-A, CLEAN 0 | match |
| 2 | git-detached-at-tip | progressing row-A, no mismatch | match |
| 3 | git-detached-commit | silent row-D + HEAD_BRANCH_MISMATCH warn, DRIFT 1 | 10 failed |
| 4 | git-detached-behind | progressing row-A, no mismatch | 4 failed |
| 5 | git-report-on-branch | not-open row-6 | match |
| 6 | git-report-off-branch | silent row-D, not row-6 | 4 failed |
| 7 | git-foreign-author | progressing-weak row-C, no author finding | match |
| 8 | jj-helper-commit (lane.branch mirror) | progressing row-A | match |
| 9 | jj-commit-no-bookmark (mirror) | silent row-D + mismatch, DRIFT 1 | 10 failed |
| 10 | jj-ambient-author (mirror) | progressing-weak row-C + author warn, DRIFT 1 | 7 failed |
| 11 | jj-young-ambient-author (mirror, age < 7200 s) | **young row-8** + author warn, DRIFT 1 | 7 failed |
| 12 | jj-sibling-author (mirror) | progressing-weak row-C, author finding absent | match |
| 13 | jj-sidebranch-mirror (mirror=master, attached side commit) | silent row-D + mismatch warn, no side credit | 10 failed |
| 14 | jj-unresolved-mirror (`.jj`, no mirror) | unavailable row-1 `reason=ref-unresolved`, no findings, CLEAN 0 | 3 failed |
| 15 | jj-missingref-mirror (`lane.branch=master`, ref gone) | unavailable row-1 `reason=ref-unresolved`, no findings, CLEAN 0 | 3 failed |
| 16 | jj-root-unresolved-closure (jj root, no mirror; report at root HEAD) | progressing row-A (row-6 skipped, never HEAD) | 2 failed |
| 17 | git-fallback-head (non-jj, trunk, detached) | progressing row-A via unchanged HEAD fallback | match |

`jj-sidebranch-mirror` also creates `main` at the base so the entering
census's unique-`master`/`main` fallback is ambiguous and its before behavior is
deterministically the HEAD fallback; the recorded mirror is the only input the
A2 census uses.

## Predicted counts (not measured)

| side | cases | assertions | failed assertions | mismatch cases | rc |
|---|---|---|---|---|---|
| before (frozen entering census) | 17 | **204** | **60** | **10** | 1 |
| after (settled A2 census) | 17 | **204** | **0** | 0 | 0 |

Arithmetic, so the integrator can audit the prediction without a run:

- the prior gate's measured 12-case receipt was **124 / 21 → 134 / 0**;
- the fixed universe on those same 12 cases is **138 / 35** (124+10 detail
  checks that were suppressed + 4 exact-field checks; 21+10+4);
- the five new cases add 66 assertions (young 15, sidebranch 16, unresolved 12,
  missingref 12, root 11) and 25 before-failures (7+10+3+3+2) → **204 / 60**;
- after side keeps the same 204 assertions and every check passes → **204 / 0**,
  10 before-mismatch cases (3,4,6,9,10,11,13,14,15,16), 7 controls.

**This supersedes the admitted 21 → 0 receipt.** The old receipt remains valid
for the old gate bytes; it must not be paired with these new bytes. The prior
report's scratch-reference quotes (`commits=1 rule=…`, `rule=merge-base-is-…`)
were a Q2 defect: the delivered census emits `count=1 committer=… window=… 
basis=committer-lane-author-foreign-email` and
`basis=merge-base-not-ancestor`; this gate now asserts the delivered grammar.

## Evidence retained

- `tools/mori-round17-jj-regressions.py` — the deliverable, sha256
  `da3e080a…89f0`, 2028 lines, 17 cases.
- Static checks (re-runnable, no test semantics): `ast.parse` on the file and
  `bash -n` on the extracted `FIXTURE_CENSUS`, both rc0.
- No run manifest exists for this revision because no run was executed; the
  first settled-commit run will write `run-manifest.json` with `retained`,
  per-case assertions, `gate.sha256`, `census.sha256`, and `observed.refs`
  (full OIDs plus `head12`/`branch12` for provenance).

## Guard and host-access disclosure

- **This pass executed no jj or git command** and no census/gate/selftest; all
  work was file edits plus the static syntax checks. No `/tmp` or `/var/tmp`
  write occurred. No host surface (journal/systemd/tmux/cgroup) was read.
- Historical, from the prior pass on the superseded clone (same seat): jj was
  run in sandbox repos under `.scratch` without `-R`, and
  `jj git init --colocate` was run without an explicit path, before the L1
  sandbox guard arrived; the exact command list is in the prior revision of
  this report (replaced by this file). The guarded gate now uses
  `jj git init --colocate <absolute sandbox path>` and `jj -R <sandbox>` after
  asserting `<sandbox>/.jj`; every git call uses `git -C <sandbox dir>` with
  `GIT_CEILING_DIRECTORIES` and no `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE`.
- The prior pass also created and immediately removed a 237-byte
  `/tmp/does-not-exist` by a mistaken redirection; this pass wrote nothing to
  `/tmp`.
- Peer coordination: a direct `write agent://CensusJj-5` attempt failed because
  the peer was not running at that moment; `MoriR17.CensusJj-5` then sent the A2
  semantics quoted above, which this revision implements. No reply was sent
  afterward.

## Risks / limits

1. **Unmeasured counts.** 204 / 60 → 204 / 0 is an assertion-construction
   prediction. L1's settled-commit run is the measurement; the old `21 → 0`
   receipt is not comparable.
2. **A2 census not present in this clone.** The clone's `tools/mori-census.sh`
   is still the pre-A2 file. The after-side prediction assumes the exact
   semantics CensusJj-5 stated (`reason=ref-unresolved`, row-1, findings
   suppressed); if the settled census emits a different basis token or reason,
   cases 14–16 and 11 need the corresponding expectation edit.
3. **Sidebranch jj-init shape.** `jj git init --colocate` on a repo whose HEAD is
   attached to `side` is expected to import cleanly (rc0) but was not run here;
   a setup failure would surface as `setup_failed` for case 13, not as a
   false green.
4. **Young age effective value.** `set_launch_age(100)` places the anchor 100 s
   before real now; the census pins NOW at real now + 120 s, so the observed age
   is ≈220 s, still below 7200. The state remains `young`; the exact age value
   is not asserted.
5. **Output strictness (F2).** Every run needs a fresh empty `--output`; a
   second run into the same directory is rejected by design. Receipt runners
   must pick a new path per run.
6. **Selftest temp policy.** `--selftest` without `--scratch` requires `TMPDIR`
   and refuses `/tmp`/`/var/tmp`; the integrator should pass
   `--scratch <clone>/.scratch` (the wave ban).
7. **Scope of `HEAD_BRANCH_MISMATCH`.** The gate still evaluates the mismatch in
   the lane's own repo (the contract's "detail names lane"); the root-jj case
   only pins row-6 closure, not a root-level mismatch.
8. **Detail-field names beyond `lane=`** are not over-specified for the author
   finding (`count=` and `basis=` are); `committer=` is emitted by the fixture
   but not required, so a rename of that one token does not fail the gate.
