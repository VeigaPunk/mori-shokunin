# S058 repair finding — round-32 defect 1

## Contract and provenance

Applied frozen R-R from `.ufo/waves/round-33/contract.md:85-88`: “A teaches-cell clause is supported only when a quote located in the committed copy of a page that the row's own source cell names states it; a row is current under the round-32 definition only when its population page alone supports every clause of its teaches cell; a clause the judge would accept only with a caveat, through absence of contradiction, or through a page the row's source cell does not name is unsupported.”

The base row is `git show 7d382043:corpus/SOURCES.md`, line 64; its full saved snapshot is `/fast/scratch/hyaku/mori-r33/RepairS058/SOURCES-7d382043.md` (SHA-256 `5cc930974e81fce78eb6d1abca5ec5d6b3173634f3fdaf6ebd92537109b66432`). The closure records the missing population-page support for the Diff-tree half at `corpus/lessons/round-32-verifier-spotcheck.md:88`. The row's population page is its first URL, git-rev-list; its second named page is git-diff-tree.

## Clause-by-clause correction rows

`S058.src` and `S058-difftree.src` below are the committed copies at `corpus/evidence/recheck-r32/`.

| S058 | clause | page | quote | supported/unsupported |
|---|---|---|---|---|
| S058 | `--topo-order` puts no parent before its children | git-rev-list (population) | `S058.src:4480-4482` (10 words): “Show no parents before all of its children are shown” | supported |
| S058 | `--reverse` outputs the selected commits in reverse order | git-rev-list (population) | `S058.src:4508-4510` (15 words): “Output the commits chosen to be shown (see Commit Limiting section above) in reverse order.” | supported |
| S058 | Combining those options makes the `base..tip` result ancestor-first | git-rev-list (population) | `S058.src:4480-4482` (10 words): “Show no parents before all of its children are shown”; `S058.src:4508-4510` (15 words): “Output the commits chosen to be shown (see Commit Limiting section above) in reverse order.” | supported |
| S058 | The default ordering is reverse chronological | git-rev-list (population) | `S058.src:4464` (10 words): “By default, the commits are shown in reverse chronological order.” | supported |
| S058 | `-r` recurses into subtrees | git-diff-tree (second named page) | `S058-difftree.src:4377` (3 words): “Recurse into sub-trees.” | supported |
| S058 | Two supplied trees are compared in their supplied order | git-diff-tree (second named page) | `S058-difftree.src:4402` (13 words): “When two trees are given, it compares the first tree with the second.” | supported |
| S058 | `--stdin` by default does not show merge-commit differences | git-diff-tree (second named page) | `S058-difftree.src:4420-4422` (12 words): “By default, git diff-tree --stdin does not show differences for merge commits.” | supported |
| S058 | A merge requires the explicit first-parent form `<commit>^1 <commit>` | git-rev-list (population) and git-diff-tree (second named page) | `S058.src:3543-3544` (16 words): “When finding commits to include, follow only the first parent commit upon seeing a merge commit.”; `S058-difftree.src:4402` (13 words): “When two trees are given, it compares the first tree with the second.” | unsupported |
| S058 | `--root` makes the initial commit appear as a creation event | git-diff-tree (second named page) | `S058-difftree.src:4385-4386` (15 words): “When --root is specified the initial commit will be shown as a big creation event.” | supported |
| S058 | A root commit needs `--root` | git-diff-tree (second named page) | `S058-difftree.src:4385-4386` (15 words): “When --root is specified the initial commit will be shown as a big creation event.” | unsupported |
| S058 | `--name-status` shows changed-file names and statuses | git-diff-tree (second named page) | `S058-difftree.src:3663-3664` (10 words): “Show only the name(s) and status of each changed file.” | supported |

## Correction text

S058's git-rev-list page supports the ordering clauses, but it does not support the Diff-tree clauses because it is a rev-list page. The named git-diff-tree page supports `-r`, the two-tree comparison behavior, the default `--stdin` merge behavior, the stated effect of `--root`, and the `--name-status` output; it does not state that `<commit>^1 <commit>` is a required merge form or that a root commit needs `--root`. Therefore the first-parent form and root-option necessity remain unsupported under R-R, and, independently, the row is **not current on its population page alone**: that page does not support every clause in the teaches cell.

## Gates, touched surfaces, and limits

- **URL registration check:** the URL `https://git-scm.com/docs/git-diff-tree` already occurs in the S058 source cell at `corpus/SOURCES.md:64` and in rejected candidate S178 at `corpus/SOURCES.md:184`; it is not a new source. No SOURCES row or source registry entry was drafted.
- **Live source gate:** fetched the requested URL twice with `curl -sSL --fail -m 60`; both fetches returned SHA-256 `72cce59764c2ea86f06904bf1805564a3fa7047f2f424ce24620f296bc811523`, matching committed `corpus/evidence/recheck-r32/S058-difftree.src`. Both `date -u +%FT%TZ` observations were `2026-10-23T02:39:46Z`. The committed `S058.src` SHA-256 observed was `6eca09d9ef21dd4270ff2c73cac7ee26964aebc470f4dfc52705eb27749ce65f`.
- **Other evidence:** read-only `git show` retrieved the frozen row; targeted search of committed `S058-difftree.src` for `\^1|<commit>\^|first parent` returned no matches. The quoted page text in `S058-difftree.src:4402-4405` describes generic two-tree comparison and commit-versus-parents behavior, not the specific `<commit>^1` syntax or its necessity.
- **Touched lane surface:** this report only, `.ufo/waves/round-33/w1/RepairS058.md`. Scratch evidence is under `/fast/scratch/hyaku/mori-r33/RepairS058/`: `difftree-live-1.src`, `difftree-live-2.src`, and `SOURCES-7d382043.md`.
- **Out of scope / not performed:** no product or SOURCES edits, lane Git/jj writes, judge or counter execution, tests/builds, tool installation/update, or source registration. No verification beyond the source reads, targeted searches, `git show`, fetches, and hashes above is claimed.

## Exact commands and outcomes

Frozen row inspection and scratch snapshot:

```sh
timeout 30 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7d382043:corpus/SOURCES.md | timeout 10 awk 'NR==64 {print NR ":" $0}'
# Output began: 64:| S058 | git-rev-list(1) and git-diff-tree(1) — ... ; full row read from saved snapshot below.
timeout 30 sh -c 'git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7d382043:corpus/SOURCES.md > /fast/scratch/hyaku/mori-r33/RepairS058/SOURCES-7d382043.md && sha256sum /fast/scratch/hyaku/mori-r33/RepairS058/SOURCES-7d382043.md'
# 5cc930974e81fce78eb6d1abca5ec5d6b3173634f3fdaf6ebd92537109b66432  /fast/scratch/hyaku/mori-r33/RepairS058/SOURCES-7d382043.md
```

Two live fetches (each command recorded its UTC time immediately before fetching):

```sh
timeout 120 sh -c 'mkdir -p /fast/scratch/hyaku/mori-r33/RepairS058 && date -u +%FT%TZ && curl -sSL --fail -m 60 https://git-scm.com/docs/git-diff-tree -o /fast/scratch/hyaku/mori-r33/RepairS058/difftree-live-1.src && sha256sum /fast/scratch/hyaku/mori-r33/RepairS058/difftree-live-1.src'
# 2026-10-23T02:39:46Z
# 72cce59764c2ea86f06904bf1805564a3fa7047f2f424ce24620f296bc811523  /fast/scratch/hyaku/mori-r33/RepairS058/difftree-live-1.src
timeout 120 sh -c 'mkdir -p /fast/scratch/hyaku/mori-r33/RepairS058 && date -u +%FT%TZ && curl -sSL --fail -m 60 https://git-scm.com/docs/git-diff-tree -o /fast/scratch/hyaku/mori-r33/RepairS058/difftree-live-2.src && sha256sum /fast/scratch/hyaku/mori-r33/RepairS058/difftree-live-2.src'
# 2026-10-23T02:39:46Z
# 72cce59764c2ea86f06904bf1805564a3fa7047f2f424ce24620f296bc811523  /fast/scratch/hyaku/mori-r33/RepairS058/difftree-live-2.src
timeout 20 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S058-difftree.src /fast/scratch/hyaku/mori-r33/RepairS058/difftree-live-1.src /fast/scratch/hyaku/mori-r33/RepairS058/difftree-live-2.src /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S058.src
# 72cce59764c2ea86f06904bf1805564a3fa7047f2f424ce24620f296bc811523  .../corpus/evidence/recheck-r32/S058-difftree.src
# 72cce59764c2ea86f06904bf1805564a3fa7047f2f424ce24620f296bc811523  .../difftree-live-1.src
# 72cce59764c2ea86f06904bf1805564a3fa7047f2f424ce24620f296bc811523  .../difftree-live-2.src
# 6eca09d9ef21dd4270ff2c73cac7ee26964aebc470f4dfc52705eb27749ce65f  .../corpus/evidence/recheck-r32/S058.src
```
