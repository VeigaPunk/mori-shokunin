# SrcGitMergeBase — S046 draft (round 17, wave 1)

Scope: open the git-merge-base documentation and draft SOURCES row S046 plus a Gate line for the `--is-ancestor` exit-status contract. Draft only; `corpus/SOURCES.md` is not edited.

## Observed source

- URL: https://git-scm.com/docs/git-merge-base (accessed 2026-10-20, native reader, HTML body).
- Page header: "git-merge-base last updated in 2.43.0"; version table lists "2.43.1 → 2.56.0 no changes".
- SYNOPSIS: `git merge-base --is-ancestor <commit> <commit>`.
- OPERATION MODES, `--is-ancestor` (verbatim):
  > Check if the first <commit> is an ancestor of the second <commit>, and exit with status 0 if true, or with status 1 if not. Errors are signaled by a non-zero status that is not 1.

## Gate quote (verbatim, 25 words)

"Check if the first <commit> is an ancestor of the second <commit>, and exit with status 0 if true, or with status 1 if not."

Word count: 25 (`<commit>` tokens counted as words).

## S046 draft row

| S046 | git merge-base documentation — https://git-scm.com/docs/git-merge-base | docs | A | `git merge-base --is-ancestor` exit-status contract for ancestry checks | OPERATION MODES, `--is-ancestor`; git-merge-base page, "last updated in 2.43.0", 2.43.1 → 2.56.0 listed no changes; accessed 2026-10-20 | Exit status 0 means the first commit is an ancestor of the second, status 1 means it is not, and any other non-zero status is an error, so status 1 and error must be distinguished. | queued | 2026-10-20 | on-release | — |

## Gate line (draft)

Gate: S046 `git-merge-base --is-ancestor` — "Check if the first <commit> is an ancestor of the second <commit>, and exit with status 0 if true, or with status 1 if not." (https://git-scm.com/docs/git-merge-base, accessed 2026-10-20)

## Scoped observations

- The doc gives exit status 0 (ancestor), 1 (not ancestor), and "non-zero status that is not 1" (error). A check that collapses all non-zero statuses into "not ancestor" misreads errors. [INFERENCE] This bears on contract C2 (`HEAD_BRANCH_MISMATCH`: "`merge-base --is-ancestor HEAD refs/heads/<branch>` fails"): the census should treat only status 1 as the mismatch finding and route other non-zero statuses to an error path. Contract text at `.ufo/waves/round-17/contract.md:86-88` does not state this distinction.
- Row S046 is a docs-tier source for the exit-status contract only. It does not establish behavior under jj-colocated repos; no local command was run to verify exit codes (out of the named read-only scope).
- S-number check: `corpus/SOURCES.md` shows rows through S040 in the file; S041–S045 appear only in the wave spec, so S046 is the number requested by the spec and was not taken in the file as read.

## Tools and installs

None. Only the docs reader was used. No pacman, uv, or npm activity.

## Mutations

None. Report file is the only write.
