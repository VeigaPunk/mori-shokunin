source: S044/S045 — https://docs.jj-vcs.dev/latest/git-compatibility/ and /latest/cli-reference/ (colocation, metaedit --update-author); S046/S047 — https://git-scm.com/docs/git-merge-base and /docs/git-symbolic-ref; routed fleet evidence /home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md F3/F4 and JjTrialMori.md.
verified-at: 2026-10-20 — source-opening receipts .ufo/waves/round-17/build/Src{JjGitCompat,JjMetaedit,GitMergeBase,GitSymbolicRef}.md; C2 measurements and carrying revision are recorded in corpus/lessons/round-17.md.
recheck: python3 tools/mori-round17-jj-regressions.py --census tools/mori-census.sh --output .ufo/waves/round-17/evidence/recheck-jj (fresh output directory required; sandbox writes only, never mutate the lane jj repository).

# Branch-anchored census history under jj colocation — round 17

## Problem and bounded repair

A detached HEAD still names a valid commit, but that commit need not be on the lane bookmark.
`jj commit` changes the working-copy parent before a separate bookmark move; a failed guard
or a skipped bookmark move can leave HEAD ahead. The routed JjAuditMori F3 sandbox measured
this. The fleet survey `.ufo/waves/round-17/build/LiveLaneHeadVsBranch.md` found lanes at their
branch tips at its snapshot, not a live reproduction of that failure window.

The census therefore resolves a branch and reads its explicit `refs/heads/<branch>`:
attached symbolic HEAD, then `refs/remotes/origin/HEAD`, then a unique master/main local ref.
The row-6 report check resolves the **fleet root's** branch; row-9 authorship resolves the
**lane repo's** branch. Unresolved branches retain the prior HEAD behavior to preserve git
stub callers; that fallback is not a branch-identity proof.

| Observation | Finding / interpretation |
|---|---|
| `merge-base --is-ancestor HEAD branch` exits 0 | no off-branch finding (HEAD may be behind) |
| exits 1 | `HEAD_BRANCH_MISMATCH`, warn; progress still scans the branch |
| another nonzero status | probe error, not proof of divergence (S046) |
| lane committer with author outside @shokunin.local | `LANE_AUTHOR_MISMATCH`, warn |
| sibling-shokunin author integrated by lane | legitimate control, not author-mismatch alarm |

The existing row-A/C author scan stays separate from the committer diagnostic so extra
fields cannot invalidate exact-author matching. Root-lane pathspec exclusions apply to both.
`ls-files -mo` remains the existing working-tree/index-relative evidence; it is not redefined
as branch content. The change does not authenticate any Git identity.

## Helper and migration disposition

Only `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh commit` owns live lane commits.
Its `metaedit --update-author` stamps the lane author before commit; `jj commit` alone may
retain the ambient author (JjAuditMori F4). S045 documents update-author, not a universal
commit-author guarantee. Use only the helper's remotely verified `landed <hash>` in reports.
A branch-tip measurement does not prove the commit was pushed; local-vs-origin is separate.

The r13–r16 regression tools' bare-HEAD fields remain **historical commit provenance**, not
claims to pin the landed branch. Their receipts and frozen controls are preserved. They
must not be used to establish landed-branch identity under jj. This round uses a new branch-
anchored measurement and a new C2 gate rather than silently changing old instruments.
R15/r16 env hardening and .jj output-guard gaps from JjAuditMori F10/F12 remain explicit
residuals; run those historical tools only with scrubbed Git environment and an output path
outside .git/.jj. No helper fix or sibling-lane edit is included here.

## Boundary

Detection and report only. A mismatch does not authorize bookmark repair, rebase, force-push,
changing author fields, routing or replacing a worker. No full update-safety/OS diagnosis is
absorbed from tsukuroi. New C2 checks run only in real isolated git/jj sandboxes; live lane
VCS remains helper-only.

## Source and migration precision after wave-2 review

S047 supplies the resolver's premise: `git symbolic-ref -q HEAD` may return
silently nonzero for detached HEAD, so empty symbolic-ref output is not absence
of repository history and the resolver continues to origin/unique local refs.
The resolver does **not** use the numeric 1-versus-128 distinction; only the
merge-base diagnostic relies on S046's numeric error distinction.
S045 is primary for the documented metaedit flag, even though the generated
CLI page self-labels experimental; it is not a universal commit-author source.
The ambient-author behavior comes from the routed empirical JjAuditMori F4.

JjTrialMori H1 is superseded operationally by helper v2's final `landed` marker,
not its abandoned/rewritten draft hashes. H2 config-outside-repo means isolated
scratch redirects XDG_CONFIG_HOME and never copies live .jj state. H3/H5
intent-to-add/index reset means no staging-based commit flow; only the helper
tracks requested paths and no concurrent seat mutates lane VCS. H4 detached
HEAD breaks `@{u}`: measurement and census use explicit branch refs instead.
The census leaves `ls-files -mo` worktree evidence intact, not cached staging
claims. Missing origin/HEAD is covered by unique master/main fallback; other
branch names without an authoritative ref remain a disclosed fallback limit.

## A2 authoritative mirror correction

The initial init-style resolver above is insufficient for a running jj lane:
an attached side-branch HEAD can otherwise redefine the apparent lane branch.
Final C2 first reads the helper's pure-Git `lane.branch` mirror. A colocated
.jj repo without a valid mirror/ref is unavailable, not silently graded from
HEAD or an inferred master/main. Normal helper init always writes this mirror.
Non-jj Git/stub callers retain legacy fallback for compatibility with their
different evidence model; that path makes no jj branch-identity claim.
Fresh sandbox controls explicitly cover attached side branch and missing mirror.
This supersedes the earlier permissive unresolved-jj fallback, not its history.
