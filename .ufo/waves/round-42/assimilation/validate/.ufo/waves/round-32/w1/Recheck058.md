# Recheck S058 — git-rev-list (C1, wave 1)

Seat: MoriR32A2.Recheck058. Leaf; no subagents, no background jobs, no tool installs, no git/jj writes.
Fetched by plain `curl` from the public URL only; no bot challenge encountered.

## 1. Fetch record

| id | url | accessed (UTC) | bytes | sha256 | scratch copy |
|---|---|---|---|---|---|
| S058 | https://git-scm.com/docs/git-rev-list | 2026-10-23T01:31:23Z | 254770 | 6eca09d9ef21dd4270ff2c73cac7ee26964aebc470f4dfc52705eb27749ce65f | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck058/S058.src |

- One fetch, first try: `HTTP=200 URL=https://git-scm.com/docs/git-rev-list SIZE=254770`, exit 0. No redirect — `%{url_effective}` equals the population url.
- Bytes saved unchanged (curl wrote the response body directly into `S058.src`); normalised text at `S058.text` via `seat-check.py text`.
- Live page still carries its version stamp "last updated in 2.56.0" and "2.56.0 2026-09-28" (normalised text offsets ~1606 and ~1655), i.e. the same revision the row records ("git 2.56.0 docs dated 2026-09-28").

## 2. Ready-to-paste row (verdict: `current`)

```
| S058 | https://git-scm.com/docs/git-rev-list | 2026-10-23T01:31:23Z | 6eca09d9ef21dd4270ff2c73cac7ee26964aebc470f4dfc52705eb27749ce65f | "By default, the commits are shown in reverse chronological order."; "--topo-order Show no parents before all of its children are shown, and avoid showing commits on multiple lines of history intermixed."; "--reverse Output the commits chosen to be shown (see Commit Limiting section above) in reverse order." | current |
```

Byte-exact copy for committing at `corpus/evidence/recheck-r32/S058.src`: `S058.src` in the scratch dir above (sha256 6eca09d9…ce65f).

## 3. Quote → teaches-cell fact → why `current`

1. **"By default, the commits are shown in reverse chronological order."** (10 words; normalised-text `Commit Ordering` lead-in.)
   Bears on the teaches clause "the default is only reverse chronological". Live text states it verbatim, and DESCRIPTION repeats "The output is given in reverse chronological order by default." Nothing qualifies the claim, so the default-ordering half of the teaches cell is unchanged.

2. **"--topo-order Show no parents before all of its children are shown, and avoid showing commits on multiple lines of history intermixed."** (21 words; `Commit Ordering`.)
   Bears on "`--topo-order` shows no parent before its children". The live definition is word-for-word the same rule the teaches cell paraphrases; the following illustrated example (8 6 5 3 7 4 2 1) is consistent with it. No drift.

3. **"--reverse Output the commits chosen to be shown (see Commit Limiting section above) in reverse order."** (16 words; `Commit Ordering`.)
   Bears on "`--reverse` flips the output" and hence on "`rev-list --reverse --topo-order base..tip` lists ancestors first". The live `--reverse` definition still inverts the chosen order; its only restriction stated there is "Cannot be combined with `--walk-reflogs`", so the `--topo-order` combination asserted by the row is not excluded. Composing quote 2 with quote 3 to conclude ancestors come first is [INFERENCE] from two verbatim sentences, not a third sentence in the doc.

`--first-parent` (anchor) is also still present and unchanged: "When finding commits to include, follow only the first parent commit upon seeing a merge commit." (normalised text ~offset 9065).

## 4. seat-check output (`row S058 S058.src '<quotes cell>'`)

```
sha256=6eca09d9ef21dd4270ff2c73cac7ee26964aebc470f4dfc52705eb27749ce65f
quotes=3 words=[10, 21, 16] in_copy=[True, True, True]
shared_tokens=['children', 'chronological', 'commit', 'default', 'limiting', 'lines', 'order', 'output', 'reverse', 'shown', 'topo']
topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
EXIT=0
```

## 5. Drift details and corrections

None. Verdict `current`; no `Round32` correction is drafted for `corpus/knowledge/freeze-order-r18.md` (the row's sole used-by entry), because nothing in the row's teaches cell changed.

## 6. Observation (not drift): the diff-tree half of the teaches cell is not served by the population URL

`SOURCES.md:64` names **two** URLs for S058 — `https://git-scm.com/docs/git-rev-list` **and** `https://git-scm.com/docs/git-diff-tree` — while the population row's url is only the first. The teaches cell's second half (`-r` recursion, two-tree `<commit>^1 <commit>` form, merge diffs suppressed by default under `--stdin`, `--root`, `--name-status`) is absent from the rev-list page (normalised copy contains 0 occurrences of `--root`, `--name-status`, `--name-only`, `--no-commit-id`; its only `diff-tree` occurrence is the EXAMPLES pipeline `git rev-list HEAD | git diff-tree --stdin --format=medium -p`). This is a pre-existing scope boundary of the row, visible in the row's own anchor text, not a live change.

To still test the second half this round I opened the companion URL by ordinary means (no challenge):
`curl` 2026-10-23T01:31:59Z → `HTTP=200 SIZE=256942`, sha256 `72cce59764c2ea86f06904bf1805564a3fa7047f2f424ce24620f296bc811523`, saved at `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck058/S058-difftree.src`, normalised at `S058-difftree.text`. It still states, verbatim:

- "-r Recurse into sub-trees."
- "--root When --root is specified the initial commit will be shown as a big creation event. This is equivalent to a diff against the NULL tree."
- "-m By default, git diff-tree --stdin does not show differences for merge commits. With this flag, it shows differences to that commit from all of its parents."
- "--name-status Show only the name(s) and status of each changed file."
- SYNOPSIS still permits two tree-ish operands: `git diff-tree [...] <tree-ish> [ <tree-ish> ] [<path>...]`, which is the two-tree form the row asks for.

So both halves of the teaches cell remain supported; the row's sha/quote cells can only draw from the rev-list copy per the frozen rules, which is what the row above does. If L1 wants the diff-tree half itself receipted in the `## Recheck` table, it needs a population row for the second URL — not something this seat can add, since the population is frozen.
