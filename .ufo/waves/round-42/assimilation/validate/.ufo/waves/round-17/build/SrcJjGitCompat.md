# SrcJjGitCompat — jj Git-compatibility source (S044) draft

Seat: `MoriR17.SrcJjGitCompat-5`. Scope: draft one SOURCES row (S044) and one Gate line for the jj
colocated HEAD semantics. Registry writes are L1's; this seat wrote only this report. No VCS
mutation, no builds/tests, no census or gate runs.

## Source opened

- URL: https://jj-vcs.github.io/jj/latest/git-compatibility/ (redirects to canonical
  `https://docs.jj-vcs.dev/latest/git-compatibility/`), accessed 2026-10-20 via `read` (reader text).
- Page title: "Git compatibility - Jujutsu docs". The page is the `latest` alias, so the text may
  drift; the access date pins it.

## Verbatim quote (25 words, backticks removed for the table)

> jj commands will usually put the Git repo in a "detached HEAD" state, since in jj there is not concept of a "currently tracked branch".

Word count: 25 (verified by hand). Source text is `` `jj` commands will usually put the Git repo in
a "detached HEAD" state, since in `jj` there is not concept of a "currently tracked branch". `` —
the "not concept" wording is the upstream text, kept verbatim.

Supporting statements on the same page (not quoted in the row):

- Colocation default: "This is the default for Git-backed workspace created with `jj git init` or
  `jj git clone`. The Git repo and the Jujutsu workspace then share the same working copy."
- Import/export: "Jujutsu will import and export from and to the Git repo on every `jj` command
  automatically."
- Branch-mapping gap: "## Branches ... TODO: Describe how branches are mapped" (the page's Branches
  section is a TODO).
- Conflicted branch: "When a `jj` branch is conflicted, the position of the branch in the Git repo
  will disagree with one or more of the conflicted positions."
- Detached HEAD row in the feature table: "**Detached HEAD: Yes.** Jujutsu supports anonymous
  branches, so this is a natural state."

## Draft SOURCES row S044 (for L1 to register; not written to `corpus/SOURCES.md`)

Registry check: `corpus/SOURCES.md` (grep `^| S0(38|39|4x)`) has S037–S040 and no S041–S043; S044 is the
next unused id, but S041–S043 are absent, so the id sequence has a gap. L1 must decide whether the
gap is held by a sibling draft before inserting. [INFERENCE: the gap is unassigned; no sibling row observed.]

```
| S044 | jj Git compatibility — https://docs.jj-vcs.dev/latest/git-compatibility/ | docs | A | colocated jj/git workspace HEAD state and branch mapping | Detached HEAD feature row; Colocated Jujutsu/Git workspaces; Branches (TODO); page accessed 2026-10-20 | jj commands will usually put the Git repo in a "detached HEAD" state, since in jj there is not concept of a "currently tracked branch". | mined | 2026-10-20 | on-release | — |
```

Columns follow the registry header (`id | source | kind | tier | scope | anchor | teaches | status |
opened | recheck | used-by`). `used-by` is `—` because no note cites S044 yet. Status `mined` is proposed
only; L1 may keep `queued` until a consuming note exists. Source URL is the canonical host the page
redirected to; the lane may prefer the `jj-vcs.github.io` string used in the task — both resolve to the same page.

## Gate line (draft)

Gate: S044 quote is 25 words, verbatim from `docs.jj-vcs.dev/latest/git-compatibility/` (accessed
2026-10-20); the page states jj commands "will usually" detach Git HEAD in a colocated workspace.

## Lane observation (read-only, 2026-10-20)

Commands run from `/home/vgpnk/Projects/shokunin/mori-shokunin` (all read-only):

| Command | rc | Output |
|---|---|---|
| `git symbolic-ref -q HEAD` | 0 | `refs/heads/master` |
| `git rev-parse --short HEAD` | 0 | `24526ea` |
| `git branch --show-current` | 0 | `master` |
| `git rev-parse --short refs/heads/master` | 0 | `24526ea` |
| `ls -d .git .jj` | 0 | both present (colocated layout) |
| `git config --get core.bare` | 0 | `false` |
| `git log -1 --format='%H %D'` | 0 | `24526ea…` `HEAD -> master, origin/master, origin/HEAD` |
| `jj --version` | 0 | `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` |
| `git --version` | 0 | `git version 2.56.0` |

Observed: the lane's Git HEAD is **attached** to `refs/heads/master` at `24526ea`, not detached.
The docs say jj "will usually" detach HEAD, so an attached HEAD is consistent with the docs' "usually"
and is not a contradiction. [INFERENCE: the attachment comes from an earlier git-side checkout or
jj's branch export; no jj mutating command was run to confirm which.]

## Relevance to C2 (census operability, `tools/mori-census.sh`)

- The census resolves the lane branch from `symbolic-ref -q HEAD` first. In this lane that returns
  `refs/heads/master`, so the first branch-resolution step succeeds without falling back. In a
  detached state (the docs' "usually" case) the same step fails and falls through to
  `refs/remotes/origin/HEAD` → `refs/heads/master|main`, which is why the contract anchors probes on
  `refs/heads/<branch>` rather than bare `HEAD`.
- `HEAD_BRANCH_MISMATCH` (contract C2) would fire when HEAD resolves but is not an ancestor of
  `refs/heads/<branch>`. With HEAD == `refs/heads/master` at `24526ea` it does not fire on the
  current lane state [observed].
- The docs' conflicted-branch caveat (`branch@git` disagreement) is a census edge case: a conflicted
  bookmark leaves `refs/heads/<branch>` at a position that disagrees with one of its conflicted
  positions. The census should not treat that disagreement as lane drift without checking jj
  state. [INFERENCE: no conflicted bookmark observed in this lane.]
- The Branches section is a TODO upstream. The branch-to-bookmark mapping the census assumes
  (`refs/heads/<branch>` equals the jj bookmark) is therefore not documented by this page;
  it rests on the colocated import/export statement above. [INFERENCE]

## Findings

1. Source opened and quote drafted; S044 is the next unused id, with a S041–S043 gap for L1 to resolve.
2. The docs' detached-HEAD statement is hedged ("will usually"); the lane is attached now. Census
   must not assume either state.
3. Branch mapping is undocumented upstream (TODO); C2's `refs/heads/<branch>` anchor relies on
   colocated import/export, not on a documented contract.

## Tools installed or updated

None. Versions recorded above were read, not installed.

## Out of scope

No SOURCES.md, Gate, or census edit (L1 integration). No jj mutating command run. No pacman
transaction. No journal query.
