# CensusNewBranches — wave-2 falsification of the C2 census code paths

Seat: `MoriR17.CensusNewBranches-4` (scout, leaf, no dispatch). Date: 2026-10-20.
Base for relative paths: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

**What I attacked.** The delivered `tools/mori-census.sh`. Its sha256 is `12e8e2d9…6d85`, matching
`PINNED_INPUTS.json` (measured commit `273aa74`). The entering census is `frozen/mori-census.sh`,
sha256 `f1f8d1b6…1ff7`, and `git show 24526ea:tools/mori-census.sh` gives identical bytes. The gate
is `tools/mori-round17-jj-regressions.py`.

**Code paths covered.**
- Branch resolution: attached HEAD, then origin/HEAD, then the unique local branch.
- `merge-base` exit status 1 versus other errors.
- The separate author and committer scans.
- Root row 6 versus lane row 9.
- Every early return.
- Capture semantics (`cap`).
- The claim that SURFACE/GL_EXTRA text is unchanged.

**How I tested.** I traced the code statically and ran read-only `git` queries against existing
repos, plus one read-only parse of the ledger file.
- I did not run the census, any gate, any selftest or any live census probe.
- I made no VCS mutation, ran no jj command and wrote nothing to `/tmp`.
- No LSP device was available for this seat, so every symbol claim comes from reading the cited
  lines directly. Grep was used only to locate them.

**Verdict.** The settled count `21→0` is not overturned. Every gate case sits in the slice the
code reaches. However, the C2 claim fails outside that slice. The strongest counterexample:
`LANE_AUTHOR_MISMATCH` can never fire for most real rounds (F1).

---

## F1 — `LANE_AUTHOR_MISMATCH` cannot fire for most real rounds (medium; new evidence, and it reclassifies a sibling's "inherent limit")

**What the code does.**
- The committer/author pass runs only inside the row-9 block, at `tools/mori-census.sh:2361-2373`.
- Every earlier row returns first: row 2 at `:2242`, row 3 at `:2251`, row 4 at `:2255`, row 7 at
  `:2262`, row 8 at `:2269`, and row 6 at `:2298`.
- By contrast, `head_branch_probe` was deliberately moved ahead of those returns (`:2236-2237`).
  Its comment says this is so a drifted HEAD "is reported for every lane this census can read —
  not only for lanes that happen to grade through rows A/B/C".
- The default silence gate is `LANE_SILENCE_S=7200` (`:353`). The registry invocation
  (`SKILL.md:164`) does not override it, and no fleet script sets `MORI_LANE_SILENCE_S`.

**Why the reachable window is usually empty.** Within one launch anchor, the lane's states run in
this order:
- From launch to launch+7200: row 8 (`young`), or row 4 if the round already closed.
- After the ledger `complete`/`wrap` line: row 4, until the next launch.
- After a committed root report: row 6.

So the author pass can run only during `(launch+7200, min(close, report commit)]`. When a round
closes within 7200 s, that interval is empty. At the next launch, the `(LA_EPOCH, NOW]` window
moves past that round's commits, so they are never scanned.

**Measured from the ledger.** I parsed `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` read-only
(510 lines; 205 launch, 145 complete and 22 wrap lines). Each close was paired with the latest
earlier launch of the same lane and round.

| Set | Closed rounds | Closed within 7200 s (author pass never runs) |
|---|---|---|
| All lanes, 2026-09-28 → 2026-10-20 | 159 | **151 (95%)** |
| 8 jj-colocated lanes, whole ledger | 50 | **43 (86%)** |
| jj lanes launched since 2026-10-13 | 47 | **40 (85%)** |

- The other 7 recent jj rounds have a reachable window of at most 694 to 9771 s.
- A report committed before launch+7200 would shrink those windows further. [INFERENCE: I did not
  rerun the row-6 query.]

**Deterministic counterexample** (code trace, not executed). Take the gate's own `jj-ambient-author`
setup (`tools/mori-round17-jj-regressions.py:633-651`): ambient author, lane committer, bookmark
moved. Then change exactly one input:
- (a) put the launch at `now-7000` instead of `now-8000` (`:350`), so row 8 applies; or
- (b) append `complete alpha round=1` to the ledger, so row 4 applies; or
- (c) also commit the report on the root branch, as `git-report-on-branch` does, so row 6 applies.

In all three variants the contract predicate still holds: a post-launch commit on the branch,
committer `alpha-shokunin <alpha@shokunin.local>`, author email outside `@shokunin.local`. Yet the
code returns before line 2361, so `GL_AMN=0`, no `LANE_AUTHOR_MISMATCH` is emitted, and the verdict
is CLEAN with rc0. Applying the same change to `jj-commit-no-bookmark` still emits
`HEAD_BRANCH_MISMATCH`, because that probe runs before the early returns.

**Why the gate cannot see this.**
- The gate's launch age is 8000 s, above 7200 s.
- The selftest's C2 cases use age 2000 s with `MORI_LANE_SILENCE_S=900` (`:3946-4080`).
- So every author case sits in the only reachable slice. No case combines an author defect with
  rows 4/6/7/8.

**Undisclosed.** These sources all state the finding without the row condition:
- `build/CensusJj.md:62-68`
- `corpus/knowledge/jj-branch-anchor-r17.md:26`, which reads "lane committer with author outside
  @shokunin.local → `LANE_AUTHOR_MISMATCH`"
- the SKILL registry (`SKILL.md:164`)
- the contract predicate (`contract.md:88-90`)

**Correction to sibling `falsify/CriticC2Final.md` F6.** That report classes this as a "limit,
inherent" that "should be recorded, not fixed by expanding the window". That is inaccurate:
- The window `(LA_EPOCH, NOW]` stays defined through rows 4/6/7/8 until the next launch line.
- The blindness comes from where the pass sits in the code, not from the window semantics.
- Moving the committer pass to just after the row-3 check, mirroring `head_branch_probe`, would
  detect these commits without expanding the window.

F6 also understates the scope. It is not only that "closed lanes cannot be audited". For 85–95% of
rounds there is no census instant at all at which the finding can fire. (Whether to move the pass
is the integrator's design call; this seat does not judge admission.)

## F2 — an inherited `GIT_TRACE` disables both branch-resolver arms and the HEAD probe without any signal (low–medium; new for C2)

**The mechanism.**
- `cap` merges stderr into stdout: `CAP_OUT=$("$@" 2>&1)` at `:554-558`.
- Each new C2 parse point keeps only the first line: `b=` `:2114`, `ref=` `:2123`, `h=` `:2153`,
  `t=` `:2164`.
- The hardening removes only `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE`. A grep of the census
  for `GIT_TRACE|GIT_CONFIG_PARAMETERS|GIT_CONFIG_COUNT|unset GIT|env -i` finds only the selftest
  `env -i` at `:3175` and `:3245`, so nothing scrubs `GIT_TRACE*` in live runs.

**Reproduction.** I reproduced the census parse by hand, read-only. I did not run the census.

```
out=$(env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 GIT_TRACE=1 \
      git -C /home/vgpnk/Projects/shokunin symbolic-ref -q HEAD 2>&1)      # rc=0
first_line_stripped=[16:59:31.095193git.c:506trace:built-in:gitsymbolic-ref-qHEAD]  -> ARM1=fallthrough
same on mori-shokunin rev-parse --verify -q HEAD -> HEADPROBE=silent-return
control without GIT_TRACE: first line = refs/heads/master
```

**Consequences under inherited `GIT_TRACE=1`.**
- The attached-HEAD and origin/HEAD arms never accept a branch.
- Only the show-ref arm, which checks exit status alone, can resolve. A plain-git lane attached to
  any branch other than master/main is therefore re-anchored to the unique master/main.
- `head_branch_probe` always takes the `|| return 0` at `:2156`, so `HEAD_BRANCH_MISMATCH` can
  never fire.
- Nothing in the output reports the degradation.
- Row 6's `ct` parse at `:2192` is broken in the same way, but the entering census already had
  that problem; C2 did not cause it.

**Why the gate cannot see this.** `sanitized_env()` (`tools/mori-round17-jj-regressions.py:166-177`)
passes through only `PATH`, `LANG`, `LC_ALL`, `TZ` and `TERM`.

**Realism.** It depends on the operator environment. Agents or operators who export `GIT_TRACE` to
debug git are the realistic case. `SandboxFinal.md` F3 raised the same variable for C3's
file-write path, but not for C2's parsing.

## F3 — the resolver's branch-name rule is narrower than git's, so some attached branches are silently replaced (low)

**The rule.** `valid_branch` (`:2108`) accepts only `^[a-zA-Z0-9][a-zA-Z0-9._/-]*$`.
- Git accepts names outside that set. `git check-ref-format --branch` returned rc0 for `_wip`,
  `feat+x`, `wip@home` and `r18,fix`; the census rejects all four.
- This host has a live example: the fleet root holds `refs/heads/@foo` (rc0 under
  `check-ref-format`).

**Consequence.** A plain-git lane attached to such a branch falls through to origin/HEAD's branch
or the unique master/main.
- The lane is then graded on a branch it is not on.
- If the attached branch is not contained in that branch, `HEAD_BRANCH_MISMATCH` fires as a
  warning, which flips the verdict to DRIFT.
- The entering census graded HEAD for this lane, so this changes plain-git behavior.
- Compare `CriticC2Final` F1: an attached `wip` becomes the anchor, while an attached `wip+1` is
  replaced. Two near-identical states get opposite treatment.

**Scope.** This conforms to the contract, because it uses the same regex as
`scripts/hyaku/jj-lane.sh:85`. There is no live instance: every attached lane is on main or master,
and `@foo` is an ancestor of the root's master (`merge-base --is-ancestor` rc0).

## F4 — the scans read a moving ref, so one lane record can contradict itself (low, [INFERENCE])

**The mechanism.**
- Row 9 runs three separate git calls on the branch name, not on one resolved hash:
  `rev-parse --verify -q "$rev"` (`:2312`), the author `log` (`:2326`), and the committer `log`
  (`:2362`).
- `head_branch_probe` resolves `h` (`:2151-2153`) but then tests the literal `HEAD` (`:2158`).

**The race.** If a helper commit plus `bookmark set` lands between `:2326` and `:2362`:
- The author scan sees no commit in the window.
- The committer scan sees the ambient-authored commit.
- The lane record then says both `silent … no_other_commits=yes` and `LANE_AUTHOR_MISMATCH
  count=1`.

This needs a concurrent commit and was not observed. Fix: pass the hash already resolved at
`:2312`, and `$h` at `:2158`.

## F5 — one root-repo HEAD drift is counted twice (low)

**The mechanism.**
- `protocol` and `aggregator` both map to `$ROOT` (`:1973-1977`).
- Each runs `head_branch_probe` against the same repo, so one root divergence emits two
  `HEAD_BRANCH_MISMATCH` warnings (`:2443`) and adds 2 to `drift=`.
- `drift_line_id` keys FINDING lines on the text before ` severity=` (`:2717`). Both lines therefore
  share the identity `FINDING:HEAD_BRANCH_MISMATCH`.

The key-sharing is the same pre-existing behaviour `LANE_SILENT` already has across lanes. The double
count of one repo-level fact is specific to C2.

## Early-return inventory (code trace)

| Return | Line | Branch probe and HEAD probe run? | Committer pass runs? |
|---|---|---|---|
| row-1 ledger-unreadable | `:2209-2211` | no (the repo is readable, but the probe is skipped) | no |
| row-1 repo-absent / git-unreadable | `:2213-2222` | no (cannot read) | no |
| row-1 tree-unreadable (`ps_walk`) | `:2224-2228` | no (refs are readable, but the probe is skipped) | no |
| row-2 / row-1 unparseable launch / row-3 / row-4 / row-7 / row-8 | `:2240-2271` | yes | **no (F1)** |
| row-1 `git-ls-files-error` | `:2280-2284` | yes | no |
| row-6 report closed | `:2297-2300` | yes | **no (F1)** |
| row-1 `git-log-error` | `:2327-2331` | yes | no |
| row A / B / C / D | `:2375-2411` | yes | yes |

The comment's "every lane this census can read" overstates coverage by the two "readable but
skipped" rows. Also, no gate or selftest case puts a HEAD drift on a young or not-open lane. The
hoisted HEAD probe is correct by reading, since emission at `:2442-2444` does not depend on row
state, but it is untested.

## Attacked with no counterexample found

- **`merge-base` exit statuses.** Only rc1 sets `GL_HBM` (`:2159-2170`). A missing branch gives
  rc128, confirmed read-only: `merge-base --is-ancestor HEAD refs/heads/nonexistent-branch-xyz` in
  mori-shokunin returned 128, which emits nothing. The mapping is consistent with S046.
  - A shallow history could produce a false rc1, but
    `rev-parse --is-shallow-repository` is `false` for the 8 colocated lanes and the root.
  - The residual where a proven mismatch is withheld (rc1, then a tip query failure) was already
    raised by `CriticC2Final` F3.
- **`set -e` safety.** `lane_branch_probe` runs only in `if`/`elif` conditions (`:2236`,
  `:2294`). In `head_branch_probe`, every possible failing test is guarded by `|| return 0`. The
  `GL_AMN` awk command has a fixed program. I found no abort path.
- **Exactness of the unresolved-branch fallback.**
  - With no branch, the new code passes an explicit `HEAD`, where the entering census used
    git's implicit default revision. The results are equivalent: `log … HEAD -- path` equals
    `log … -- path`, and on an unborn HEAD both exit nonzero, so row 6 returns 1 either way.
  - The committer pass and the HEAD probe are both skipped (`:2237`, `:2361`).
  - The `grade_lane` diff between the frozen and delivered census shows only comments, the
    `root_rev`/`rev` substitution and the new probes.
- **SURFACE/GL_EXTRA text.** The diff of `grade_lane` and `probe_silence` (frozen vs delivered)
  adds no `GL_EXTRA` or `SURFACE` string. The `cmd=` text at `:2415` is byte-identical and
  therefore stale, which was already raised (CriticHarm K7) and declined under A1
  (`build/CensusJj.md:156`). The changed meaning of the `has_head` token was already raised
  (CriticC2 O4, ReceiptC2Controls Q4a).
- **Root row 6 versus lane row 9.** Child lanes resolve `$ROOT` separately (`:2293-2296`), so
  wave-1 O2 is fixed. Root lanes reuse `GL_BRANCH` because their repo is `$ROOT`.
  `CriticC2Final` F4/F5 already cover the root-drift diagnosability and pathspec residuals.

## Live read-only survey (closes ReceiptC2Controls's open question Q4a)

I ran these per repo across all 21 `*-shokunin` lanes and the fleet root: `symbolic-ref -q HEAD`,
`symbolic-ref -q refs/remotes/origin/HEAD`, `config --get lane.branch`, and
`for-each-ref refs/heads/`.

- **The 8 jj lanes** (kaidoku, kama, mado, mori, souji, tabi, tameshi, tsukuroi) are all detached.
  Each resolves through origin/HEAD to a local branch that exists and equals `lane.branch`
  (kaidoku: main; the rest: master). So there is **0 live exposure** to origin/HEAD pointing at a
  missing local branch.
- **The 13 plain-git lanes** are attached to main or master. The fleet root is attached to master.
- **Correction:** wave-1 `CriticC2.md:114-115` said kama, souji and tameshi lacked `lane.branch`.
  Today all 8 record it.
- I did not read the jj `trunk()` alias. A grep of `.jj/repo/config.toml` matched nothing; the
  config may live outside the repo. [INFERENCE] I did not run jj to check.

## Commands (all read-only; rc0 unless stated)

- `sha256sum tools/mori-census.sh frozen/mori-census.sh` gave `12e8e2d9…`/`f1f8d1b6…`.
  `git cat-file -p 24526ea:tools/mori-census.sh | sha256sum` gave `f1f8d1b6…`.
- `diff` of the `grade_lane` and `probe_silence` bodies, frozen vs delivered: rc1 (differences
  shown above).
- Lane and root survey as listed above. In the root, `merge-base --is-ancestor refs/heads/@foo
  refs/heads/master` returned rc0.
- `check-ref-format --branch` for `@foo`, `_wip`, `feat+x`, `wip@home` and `r18,fix` returned rc0
  for each.
- `merge-base --is-ancestor HEAD refs/heads/nonexistent-branch-xyz` returned rc128.
- `rev-parse --is-shallow-repository` returned `false` for the 8 jj lanes and the root.
- The `GIT_TRACE=1` parse reproduction above: output went to stderr only, nothing was written.
- A Python stdlib parse of `.ufo/watchdog.log` produced the duration table above. I opened no
  transcripts or credentials.

## Remaining unknowns

- Whether any census tick actually fell inside the reachable author-pass window of the 7 long jj
  rounds. Lane census receipts were not read.
- The report-commit times on the root master for those rounds (the row-6 probe was not rerun).
- The value of the jj `trunk()` alias per lane.

**Tooling:** nothing installed or upgraded.
