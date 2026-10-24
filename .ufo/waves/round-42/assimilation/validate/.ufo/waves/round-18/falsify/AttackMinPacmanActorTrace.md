# AttackMinPacmanActorTrace — wave-2 falsification

## High — privacy minimization remains incomplete

Reviewed the original at `d005cdd` and the replacement at `e2bfbd6`; the working-tree file SHA-256 matches the replacement blob. The replacement still contains semantic reading-sweep findings despite removing the original explicit paths and artifact names. The frozen policy says the regex classes are a recall floor (`.ufo/waves/round-18/frozen/c1-policy.json:6-15,29`); the governing rule forbids paraphrased output and these other retained facts (`corpus/knowledge/evidence-minimization-r18.md:22-30`; `.ufo/waves/round-18/out-of-metric-triage.md:10-16`). Counts below are distinct replacement lines; classes are semantic sweep classifications, not claims that the frozen regex matched.

| Kind / class | Replacement lines (count) | Finding, without reproducing private content |
|---|---:|---|
| Other-session tool-output content/identity, R3 | `26-30, 40, 48, 78-79` (9) | Retains artifact size/time metadata, descriptions of output heads/tails and bodies, output-derived content tallies, neighboring-output summaries, and a second-store search-result summary. These exceed count/class-only support and include paraphrased output or artifact-identifying metadata. |
| Personal document, R4 | `31` (1) | Retains a paraphrase of a personal planning document's plan and its contrast with the observed action. |
| Shell history, R5 | `49, 62, 80` (3) | Retains history-derived count, search-result and flush-state facts. |
| Privileged configuration, R6 | `50, 62, 85` (3) | Retains a host privileged-configuration status fact, repeated in prose and the command-results table. |
| Session identity context, R1 semantic sweep | `36` (1) | The explicit identifier/path is gone, but the replacement still associates the relevant store with a current/boot-time context and time anchor. **[INFERENCE]** This is an identifying contextual residue rather than a literal R1 token. |
| Host login-record/session activity, out-of-metric sweep | `49, 81` (2) | Retains login-record state/timing without the account or terminal identifier. **[INFERENCE]** This is session activity data; it is not an R9 field token. |

Manual review found no literal OMP session directory/UUID, operator OMP routing assignment, or R9 session-field value in the replacement. The residuals above nevertheless answer the privacy question **yes**: other-session output/paraphrase, a personal-document fact, shell-history facts, privileged-configuration facts, and contextual session-record/activity facts remain. The lane seat name is not counted as private context under the triage rule (`out-of-metric-triage.md:14-16`).

## Verdict-level conclusions retained

The verdicts are preserved at conclusion level: replacement lines `11-12` retain the original lines `12-17`'s two actor-attribution conclusions and the unresolved human/agent identity boundary. No verdict-level conclusion was lost in the minimization.

## Provenance verified

Replacement line `5` gives the correct original blob and SHA-256. Read-only verification:

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse d005cdd:.ufo/waves/round-17/build/PacmanActorTrace.md` → `2773807b39ac60c3a4a5a5b870d9fdfbf738a5d9` (exit 0).
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file blob d005cdd:.ufo/waves/round-17/build/PacmanActorTrace.md | sha256sum` → `109e92f4d846c80d08a7ccb18c51dd42d1c0aabb9e921709515421c5f79097ef` (exit 0).
- `29b0dc7:<path>` resolves to the same blob and SHA-256 (exit 0), so the freeze-commit reference in line 5 is consistent.
- Replacement blob at `e2bfbd6` is `3458ff969fe9f300cdee46ce24b39a8610ec66a1`; SHA-256 is `b30443665d48a32bb49dfa501eef8ec594a3ab03b299bf9e84d0904b6512d1bf`. The working-tree file has that same SHA-256 (exit 0).

## Verification gaps and residual scope

This is a review of the assigned artifact only; no repo-wide minimization conclusion follows. I did not run the C1 tool or a build/test suite; this finding is from direct comparison and reading sweep, as required by the C1 known-limit. No external URLs were consulted; no tools were installed or updated.

Read-only commands run (all exit 0):

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d005cdd:.ufo/waves/round-17/build/PacmanActorTrace.md | cat -n`
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6:.ufo/waves/round-17/build/PacmanActorTrace.md | cat -n`
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse d005cdd:<path>`; `rev-parse e2bfbd6:<path>`; and `ls-tree -l` for both revisions and the target path
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file blob <revision>:<path> | sha256sum` for `d005cdd`, `e2bfbd6`, and `29b0dc7`
- `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/build/PacmanActorTrace.md`; `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse e2bfbd6`; and read-only `git log -1` for the minimization commit
