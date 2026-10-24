# SrcGitRevList — C2 freeze-order source (round 18, wave 1)

Seat: MoriR18Recovery.SrcGitRevList (leaf scribe). Scope: ordering semantics and per-commit changed-path listing for the r18-C2 freeze-order verdict. Read-only; no downloads, no files written outside this report, no VCS mutation, no installs.

## 1. Sources opened

| # | URL | Access date | Document version | Result |
|---|---|---|---|---|
| 1 | https://git-scm.com/docs/git-rev-list | 2026-10-21 | page "git-rev-list last updated in 2.56.0"; 2.56.0 entry dated 2026-09-28 | opened (reader text) |
| 2 | https://git-scm.com/docs/git-diff-tree | 2026-10-21 | page "git-diff-tree last updated in 2.56.0"; 2.56.0 entry dated 2026-09-28 | opened (reader text) |
| 3 | https://git-scm.com/docs/git-log (screened alternative, see section 5) | 2026-10-21 | page "git-log last updated in 2.56.0"; 2.56.0 entry dated 2026-09-28 | opened (reader text) |

Local cross-check (read-only): `git --version` printed `git version 2.56.0` (exit 0). Local manual `man -P cat git-rev-list` and `man -P cat git-diff-tree` (exit 0) contain the same sentences quoted below for the lines checked. The local man wraps lines differently; the rendered page is the cited source.

Anchors below are line numbers of the reader's rendering of each page (not upstream source line numbers) plus the section heading. Headings are the more durable anchor.

## 2. Located quotes (each at most 25 words)

Q1 — git-rev-list, "Commit Ordering" heading, `--topo-order` (reader lines 1191-1194):
> "Show no parents before all of its children are shown, and avoid showing commits on multiple lines of history intermixed."

Q2 — git-rev-list, "Commit Ordering" heading, `--reverse` (reader lines 1213-1215):
> "Output the commits chosen to be shown (see *Commit Limiting* section above) in reverse order."

Q3 — git-rev-list, "Commit Ordering" heading, default order (reader line 1179):
> "By default, the commits are shown in reverse chronological order."

Q4 — git-rev-list, DESCRIPTION, range short-hand (reader lines 286-287; angle brackets elided here):
> "A special notation "commit1..commit2" can be used as a short-hand for "^commit1 commit2"."

Q5 — git-rev-list, Commit Limiting, `--first-parent` (reader lines 464-467):
> "When finding commits to include, follow only the first parent commit upon seeing a merge commit."

Q6 — git-diff-tree, OPTIONS, `-r` (reader lines 1114-1116):
> "Recurse into sub-trees."

Q7 — git-diff-tree, OPTIONS, `--root` (reader lines 1122-1125):
> "When --root is specified the initial commit will be shown as a big creation event."

Q8 — git-diff-tree, DESCRIPTION (reader lines 272-273):
> "If there is only one <tree-ish> given, the commit is compared with its parents"

Q9 — git-diff-tree, OPTIONS, `--stdin` merge default (reader lines 1155-1156):
> "By default, git diff-tree --stdin does not show differences for merge commits."

Q10 — git-diff-tree, OPTIONS, `--name-only` (reader lines 502-503):
> "Show only the name of each changed file in the post-image tree."

Q11 — git-diff-tree, OPTIONS, `--name-status` (reader lines 506-509):
> "Show only the name(s) and status of each changed file."

Q12 — git-diff-tree, `--no-commit-id` (reader lines 1276-1279):
> "git diff-tree outputs a line with the commit ID when applicable. This flag suppresses the commit ID output."

Q13 — git-rev-list, Commit Ordering example (reader lines 1205-1211; not a `--reverse` precedence statement): the doc's example gives "8 7 6 5 4 3 2 1" for `--date-order` and "8 6 5 3 7 4 2 1 (or 8 7 4 2 6 5 3 1)" for `--topo-order`. The example shows commits listed with children before parents in the default output; the doc does not state a `--reverse` precedence rule.

## 3. What it teaches mori (C2 freeze-order verdict)

The register's `verdict_rule.R` is `git rev-list --reverse --topo-order <base>..<tip>`. The sources support these statements:

1. **Ordering guarantee comes from `--topo-order`, not from the default.** Q1 says no parent is shown before all of its children. Q3 says the default is only reverse chronological, with no parent-before-child statement. Reading the default as a freeze order would depend on commit timestamps, which the doc does not promise to be parent-consistent. [INFERENCE from Q1 + Q3]
2. **`--reverse` runs after ordering.** Q2 says it reverses the chosen output. Combined with Q1, `--reverse --topo-order` lists every ancestor before its descendants, so "first" in R means earliest ancestor-first. The doc does not state this combined guarantee in one sentence. [INFERENCE from Q1 + Q2]
3. **`base..tip` is set subtraction, and R includes merged side branches.** Q4 defines it as `^base tip`. The register does not pass `--first-parent` to R, and the verdict does not pass it either. So a side-branch commit merged from a topic branch can be I or L. Q5 shows `--first-parent` would drop those; the register does not use it, which is correct for "first commit touching impl" but must be stated. [INFERENCE: consequence for the register]
4. **Per-commit changed paths must be computed against the first parent explicitly.** The register says "diff vs its first parent". Q8 says a single tree-ish compares a commit with its parents. Q9 says that under `--stdin` merge commits show no diff by default. The doc does not state the same default for a single command-line merge commit. Therefore the tool should not rely on the single-commit form for merges; it should pass the two-tree form `<commit>^1 <commit>` explicitly. [INFERENCE: single-commit merge default is not stated for the command line]
5. **Root commits need `--root`.** Q7 says `--root` shows the initial commit as a creation event, equivalent to a diff against the NULL tree. A root commit reachable from tip and not from base cannot be diffed against `^1`; the tool must either pass `--root` for the root form or treat it as all-added.
6. **Subtree recursion needs `-r`.** Q6 says `-r` recurses into sub-trees. Without it, a frozen path such as `tools/x.py` inside `tools/` may not appear as a file-level change. [INFERENCE: non-recursive output shows subtree-level entries; this is implied by Q6, not quoted]
7. **Deletions: prefer `--name-status`.** Q10 says `--name-only` lists the name "in the post-image tree", so a deleted path may not be listed by name. Q11 says `--name-status` gives the status letter per file. The register's `absent` verdict is already defined by checking frozen paths at tip, so this is a secondary concern. Recommend `--name-status` for the impl/frozen change list. [INFERENCE: actual deleted-file output not observed in this read-only pass]
8. **`--no-commit-id`.** Q12 says the commit-ID line appears "when applicable" and can be suppressed. Parsers should pass `--no-commit-id` or use the two-tree form, or they will see a header line. Not a verdict risk; a parser hygiene note.

Scope boundary: these sources describe Git's command semantics. They do not show that any particular repository's history is parent-consistent, that timestamps are monotone, or that the lane's commits follow any merge policy. Those remain facts to be measured by the tool at the measured revision.

## 4. Tier proposal

- **S0xx (git-rev-list + git-diff-tree): tier A, primary/normative.** Scope: Git 2.56.0 command semantics for `rev-list` ordering/limiting and `diff-tree` changed-path listing, for the C2 freeze-order verdict only. It is the official reference for the commands the contract names, pinned to the same version as the local `git 2.56.0`. It does not establish repository history properties.

## 5. Alternative source screened — git-log(1)

Candidate: https://git-scm.com/docs/git-log (opened 2026-10-21, version 2.56.0).

Evidence:
- `--reverse`, `--topo-order`, `--first-parent` share the rev-list wording (reader lines 1252-1276 in the rendered page).
- The log page adds that with `--first-parent` the default merge diff format becomes `first-parent`: "The exception is when `--first-parent` is in use, in which case `first-parent` is the default format for merge commits." (reader lines 2186-2190). The page also says the default diff-merges format is `off` unless `--first-parent` is in use (reader lines 2241-2243).
- Porcelain output is also configuration-dependent (`log.*`, `diff.merges` style settings), which the contract's plumbing-only rule (rev-list, diff-tree, ls-tree, cat-file, show) excludes.

Decision: **REJECT for C2 authority.** Reason: it is porcelain, not one of the plumbing commands the contract names; its merge-diff defaults depend on `--first-parent` and configuration, which is exactly the merge ambiguity the verdict must avoid; and it would add a second ordering source without adding a fact the two named pages do not already state. Flip condition: if the tool needs rendered merge-diff output, log's `--diff-merges` text would be admitted as a cross-check, not as the verdict's authority.

## 6. Registry rows (draft; L1 integrates; SOURCES.md not edited)

Column shape: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`

Row 1 (admitted, single row covering both named pages, following the S039 precedent of one row per exact function set):

| S0xx | git-rev-list(1) and git-diff-tree(1) — https://git-scm.com/docs/git-rev-list ; https://git-scm.com/docs/git-diff-tree | docs | A | C2 freeze-order verdict: rev-list ordering of base..tip (--reverse, --topo-order, --first-parent) and per-commit diff-tree changed-path listing against the first parent, with -r, --root and --name-status | git-rev-list: DESCRIPTION short-hand; Commit Limiting --first-parent; Commit Ordering --topo-order and --reverse (reader lines 286-287, 464-467, 1179, 1191-1215); git-diff-tree: DESCRIPTION, OPTIONS -r, --root, --stdin, --name-only, --name-status, --no-commit-id (reader lines 272-273, 502-509, 1114-1125, 1155-1156, 1276-1279); git 2.56.0 docs dated 2026-09-28; opened 2026-10-21 | Commit ordering: --topo-order shows no parent before its children and --reverse flips the output, so rev-list --reverse --topo-order base..tip lists ancestors first; the default is only reverse chronological. Diff-tree: -r recurses subtrees; merges need an explicit <commit>^1 <commit> two-tree form because the doc states merge diffs are not shown by default under --stdin; a root commit needs --root; --name-status is the status-bearing listing. | queued | 2026-10-21 | on-release | — |

Row 2 (rejected alternative, same shape, tier C as the S030 precedent):

| S0xx | git-log(1) — https://git-scm.com/docs/git-log | docs | C | Alternative screened for the C2 freeze-order verdict: porcelain log ordering and merge-diff defaults | REJECTED: porcelain command outside the contract's plumbing set; shares --reverse/--topo-order/--first-parent wording but makes merge-diff format depend on --first-parent and configuration (reader lines 2186-2190, 2241-2243); adds no fact beyond the admitted pages. Flip: a rendered merge-diff need admits its --diff-merges text as a cross-check only. | rejected | 2026-10-21 | on-release | — |

## 7. Recheck command

Local, read-only, matched to the pinned version:
`git --version && man -P cat git-rev-list | grep -n -e 'Show no parents before all' -e 'Output the commits chosen' && man -P cat git-diff-tree | grep -n -e 'Recurse into sub-trees' -e 'compared with its parents'`
Expected at git 2.56.0: git version line printed; the matching sentences present (grep exit 0). Observed this pass: `git --version` = 2.56.0, exit 0; the four sentences matched in the local man pages (exit 0).

Web recheck when git releases change: `read https://git-scm.com/docs/git-rev-list` and `read https://git-scm.com/docs/git-diff-tree`, then compare the "last updated in" version line and quotes Q1, Q2, Q6, Q9.

## 8. Tooling

No installs or updates performed. Local tools used: `git --version`, `man`, `grep` (read-only). Nothing was downloaded to disk; web reads used the read tool only.

## 9. Privacy and scope notes

- No session, transcript, tool-log, configuration or credential content is copied into this report.
- No lane file was written or read beyond the committed `corpus/SOURCES.md` table shape, `.ufo/waves/round-18/contract.md`, and `.ufo/waves/round-18/frozen/c2-register.json` (read to confirm the verdict rule under test).
- The C2 verdict itself was not computed; this report supplies source semantics only.

## 10. Notes for the main agent (advice; L1 decides)

- The register's `verdict_rule.R` (`--reverse --topo-order base..tip`) matches the docs' ordering semantics. It does not state a merge policy; the tool should state explicitly that R includes merged side-branch commits (no `--first-parent`).
- The per-commit diff should be specified as an explicit `<commit>^1 <commit>` two-tree diff-tree (with `-r`, `--name-status`), with `--root` for a root commit, not the single-commit form, because the single-commit merge default is not stated for the command line.
- No other source is needed for C2 ordering; the two admitted pages cover the question.
