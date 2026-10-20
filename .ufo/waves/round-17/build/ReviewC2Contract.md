# Review: round 17 C2 census contract

## Axes reviewed
C2 correctness across Git/jj-colocated layouts; existing verdict compatibility; branch-resolution and report diagnostics.

## Findings (severity order)

### High — row 6 and row 9 do not share one repository branch

C2 says to resolve “the lane branch” and use `refs/heads/<branch>` for both row 6 and row 9 (`.ufo/waves/round-17/contract.md:82-85`), but the existing probes operate on different repositories. `ps_report_closed` reads the report from `-C "$ROOT"` (`tools/mori-census.sh:2097-2103`), whereas row 9 reads `-C "$repo"` (`tools/mori-census.sh:2113-2116,2194-2207`). `lane_repo` maps `protocol`/`aggregator` to `$ROOT` but maps every child lane to `$ROOT/<lane>-shokunin` (`tools/mori-census.sh:1967-1974`). Therefore row 6 needs the branch ref resolved in the fleet-root repo and row 9 the branch ref resolved in the lane repo; they coincide only for the two root lanes. Reusing a child lane’s branch name/ref for row 6 can make a report appear absent or fail its closure test and alter the lane grade. Clarify separate `root_branch_ref` and `lane_branch_ref` (or explicitly require resolution against each probe’s `-C` repository).

### Medium — branch fallback and failure semantics need to be explicit

The referenced helper does not implement the full fallback ladder inside `detect_branch`: it accepts an attached `HEAD` only when its target is `refs/heads/*`, then accepts `refs/remotes/origin/HEAD` only when it targets `refs/remotes/origin/*`; it ignores other symbolic targets such as `refs/jj/*` and otherwise returns failure (`scripts/hyaku/jj-lane.sh:113-125`). The unique-local-`master`/`main` fallback is in the `cmd_state` caller (`scripts/hyaku/jj-lane.sh:155-168`). Thus, with no `origin/HEAD`, an attached local branch still resolves; a detached repo resolves only if exactly one of local `refs/heads/master` or `refs/heads/main` exists; with neither or both, the current helper path has no branch result. C2 should state that an unresolved/invalid ref produces an explicit unavailable outcome rather than silently falling back to `HEAD` or grading as clean.

For the `repo .` case, the helper’s calls use `git -C "$dir"`; `.` means the process’s current working directory, not the helper’s/script’s directory. The helper invokes it literally for its root-repo use (`scripts/hyaku/jj-lane.sh:387-396`). Census root lanes currently use `$ROOT` as their repo (`tools/mori-census.sh:1967-1974`), so the resolver must receive the same `$ROOT`/`$repo` path as the corresponding probe. This matters if `MORI_SHOKUNIN_ROOT=.` or if a resolver accidentally uses literal `.` while grading a child lane.

### Medium — the new author finding can change a plain-Git lane verdict

Yes. Replacing existing `HEAD` inputs with the current attached branch ref should preserve row 6/9 behavior on an ordinary attached Git branch where `HEAD` equals that branch tip. But `LANE_AUTHOR_MISMATCH` is an additive drift finding with no jj-colocation condition in C2 (`.ufo/waves/round-17/contract.md:88-90`): a post-launch commit on any plain Git lane with the specified lane committer and a different author qualifies. Drift-level findings flip the existing roll when emitted with severity `warn` or `crit` (`tools/mori-census.sh:405-417`). So a previously CLEAN plain-Git lane can become DRIFT. If C2 is intended to affect only jj-colocated lanes, the contract needs an explicit eligibility guard; otherwise this is an intentional compatibility change that should be recorded as such.

### Low — “severity drift” must map to the census severity vocabulary

The C2 wording calls the new findings “severity drift” (`.ufo/waves/round-17/contract.md:86-90`), but the existing `emit_finding` roll logic recognizes only `warn|crit` as drift-producing; an `info` or literal `drift` severity leaves `ROLL` unchanged (`tools/mori-census.sh:405-417`). Specify the actual emitted severity (`warn` or `crit`) for both findings, or define a corresponding roll mapping. Otherwise the findings may be printed without changing CLEAN to DRIFT.

### Low — the surfaced command diagnostic will become stale unless updated

`probe_silence` publishes a literal `cmd=` diagnostic containing `git log` without a branch ref and `cat-file -e HEAD:<report>` (`tools/mori-census.sh:2275-2277`); it is emitted on the silence surface (`tools/mori-census.sh:2304-2308`). After branch-anchoring the probes, update this diagnostic to show the correct root- and lane-repo refs. Otherwise the reported probe command contradicts the behavior.

## Direct answers

- In the current pre-change census, row 6 and row 9 are the only HEAD-dependent grading areas: row 6 uses `HEAD:<path>` plus a `git log` with implicit default `HEAD` (`tools/mori-census.sh:2097-2103`); row 9 verifies `HEAD` and scans `git log` with implicit default `HEAD` (`tools/mori-census.sh:2194-2207`). The `cmd=` string at line 2276 is diagnostic, not a grading input. Under C2, `HEAD_BRANCH_MISMATCH` is an additional, deliberate HEAD-dependent finding, so row 6/9 would no longer be the only HEAD-related grading input.
- Root lanes share `$ROOT`; with `$ROOT=.` this is relative to the caller’s working directory. A child lane has a separate repo, so row 6 and row 9 must resolve branch refs independently as above.
- Without `origin/HEAD`, the helper first succeeds from attached `refs/heads/<branch>`; for detached HEAD it falls back to the unique local `master` or `main`. If neither or both exist, it cannot resolve a branch.
- Yes, C2’s new author-mismatch finding can change a plain-Git verdict. The ref substitution alone normally does not for an attached branch at its own tip.

## Evidence and verification gaps

- LSP was unavailable: `read xd://lsp` returned “No such tool”; therefore no LSP status/references/definition/diagnostics requests could be made. Literal grep was used only to locate candidate lines; conclusions above are grounded in the cited source reads, not grep as semantic proof.
- Read-only comparison: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --no-ext-diff --unified=5 24526ea -- tools/mori-census.sh` produced no hunk (`diff_exit=0`); `git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --short -- tools/mori-census.sh` was empty (`status_exit=0`). Thus there was no delivered census-file diff against the entering tip to review; this report attacks the C2 contract against the entering implementation.
- No census selftest or C2 regression gate was run; no tools were installed or updated.
