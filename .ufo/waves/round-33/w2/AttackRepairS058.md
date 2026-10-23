# AttackRepairS058 — round-32 repair row, S058 (rule R-R)

Target: `corpus/lessons/round-33.md:58` (§1 table row `| S058 |`), seat report
`.ufo/waves/round-33/w1/RepairS058.md`. Base row: `git show 7d382043:corpus/SOURCES.md:64`
(2 URLs: git-rev-list population, git-diff-tree second). Base teaches cell = field 8
(`Commit ordering: --topo-order … Diff-tree: -r recurses subtrees; merges need an explicit
<commit>^1 <commit> two-tree form because …; a root commit needs --root; --name-status …`).

## Verdict

The repair row survives the attack. No blocker or major defect. Two minors (nits, not errors).

## (a) "Supported on another page" pointers — all 5 verified

All five cite `corpus/evidence/recheck-r33/S058-difftree-r33.src` (sha256
`72cce597…1523`, identical to `corpus/evidence/recheck-r32/S058-difftree.src`); the page
`https://git-scm.com/docs/git-diff-tree` is named in S058's own source cell
(`SOURCES.md@7d382043:64`).

- `-r` "Recurse into sub-trees." — `S058-difftree-r33.src:4377` exact. PASS.
- two trees compared first-to-second — `:4402` "When two trees are given, it compares the
  first tree with the second." PASS.
- `--stdin` hides merge diffs by default — `:4420-4422` "By default, git diff-tree --stdin
  does not show differences for merge commits." PASS.
- `--root` creation event — `:4385-4386` "the initial commit will be shown as a big /
  creation event." PASS.
- `--name-status` — `:3663` "Show only the name(s) and status of each changed file." The
  quote lands on :3663; the cited range `:3663-3664` runs one line into the `--diff-filter`
  continuation. Harmless over-cite. **minor.**

## (b) "Unsupported" clauses — confirmed absent from every page the row names

Pages named by the source cell: rev-list (`recheck-r32/S058.src`) and diff-tree
(`recheck-r33/S058-difftree-r33.src`, byte-identical to `recheck-r32/S058-difftree.src`).

Clause 1: "a merge requires the explicit first-parent form `<commit>^1 <commit>`":
- `grep -c '\^1'` → 0 on all three copies. `grep '\^'` on diff-tree shows only the
  `--diff-filter` regex note (`:3855`) and `O(N^2)` (`:4010`); on rev-list only exclusion
  syntax `^baz`, `^<commit>` (`:3332-3363`, `:3554`, `:3740`, `:4408`, `:4416-4417`), never
  a `<commit>^1` parent selector. PASS — stated on no named page.

Clause 2: "a root commit needs `--root`":
- diff-tree `:4385` states only what `--root` does, never that it is needed. `grep -ni root`
  on `S058.src` (rev-list) shows no `--root` option at all. PASS.

## (c) "Clauses the population page does not carry" column

Row says "the whole diff-tree half". Closure list
`corpus/lessons/round-32-verifier-spotcheck.md:88`: 'the whole "Diff-tree:" half: `-r`,
`--root`, `--name-status`, first-parent two-tree merge form'. Identical scope, and matches
the teaches cell's "Diff-tree:" half verbatim. Verified the population page carries none of
it: `grep 'name-status'`, `'[Rr]ecurse into'`, `'--root'` on `recheck-r32/S058.src` → 0
hits each. PASS.

## (d) Forgotten teaches-cell clauses — none

Teaches cell splits into 8 atoms. Ordering half (4) is supported on the population page —
quotes verified at `S058.src:4464` (default reverse chronological), `:4480-4482`
(`--topo-order` no parent before children), `:4508-4510` (`--reverse`) — and correctly needs
no column entry. Diff-tree half (4 atoms): `-r`, `--root` (mechanism supported / necessity
unsupported), `--name-status`, merge two-tree (mechanism supported / necessity unsupported)
— all four mapped into the row's two evidence columns. PASS.

## Minor findings

1. `--name-status` cite `:3663-3664` includes one trailing line past the quoted sentence
   (see (a)). Cosmetic.
2. §1 prose `:52` says copies have "sha256 in its listing" — no manifest file exists under
   `corpus/evidence/recheck-r33/` (only `.src` files). The sha is recorded in the seat
   report, not a directory listing. Wording nit only; copies are committed and hashes
   verified.
3. R-R classification is right but understates: the merge-necessity clause is not merely
   unstated, it is contradicted (`:4420-4422` says `--stdin` shows merge diffs with the
   flag, i.e. `<commit>^1` is one procedure among `-m`/`-c`/`--cc`). Verdict unaffected.

## Cross-checks

- Judge basis confirmed: `JudgeRecheck.md:63` accepts the diff-tree half "through the
  companion doc … no contradiction" — exactly the R-R unsupported pattern; the repair row
  correctly relabels `current → not current (population page alone)`.
- §5 (`:110`) consistent: S058 diff-tree is the unpinned second URL, re-opened this round;
  r33 copy sha256-matches the r32 copy.
- Seat report line cites (`S058-difftree.src` r32 numbers) match the row's
  `S058-difftree-r33.src` cites because the two copies are byte-identical; both cite sets
  resolve correctly.

## Checks run (all executed, none inferred)

grep/sed/sha256sum on `recheck-r33/S058-difftree-r33.src`, `recheck-r32/S058-difftree.src`,
`recheck-r32/S058.src`; `git show 7d382043:corpus/SOURCES.md` line 64 field-split; reads of
`round-33.md:40-140`, `round-32-verifier-spotcheck.md:86-92`, `JudgeRecheck.md`,
`w1/RepairS058.md`. Tooling: none installed.
