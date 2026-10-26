# Mo51SimpEntry — redundancy pass on the MemAvailable entry prose (rows untouched)

Seat: Mo51SimpEntry (simplifier). Lane: mori-shokunin. No subagents.
Scoped entry: `corpus/knowledge/memavailable-estimate-r51.md` at `87e0c374537557754bf71dd68036ded3ddc6699c`
(freeze `4677910eae6d`, entering tip `aa3af1ec3118`).
Scope taken: the prose only — intro (`:12-16`), `## Reading rules` (`:44-55`), `## Boundaries` (`:57-65`).
The claims table, the title, the five `source:` lines, `verified-at:`, `recheck:` and `coverage-map:` are
byte-identical between the frozen entry and the draft (`claims_block_identical: True`, `table_rows_identical:
True`, `header_identical: True` in the score run below). I did not touch the entry, SKILL.md, SHONEN.md,
SOURCES.md, tools/ or any other seat's report.

Mode: detection and proposal only. The L1 integrates; the draft is fenced below and was scored in a scratch copy.

## What I ran (tools' cwd = fleet root, so I cd'd into scratch)

Scratch: `/fast/scratch/hyaku/mori-r51/Mo51SimpEntry/` with `TMPDIR=/fast/scratch/hyaku/mori-r51/Mo51SimpEntry/tmp`;
`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` exit 0, `/fast` 25% used, 604.1G free.
No installs, no pacman (paused), no clone, no fixture repo, no git mutation.

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse 87e0c374537557754bf71dd68036ded3ddc6699c^{commit}
87e0c374537557754bf71dd68036ded3ddc6699c
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain=v1 -- corpus/knowledge/memavailable-estimate-r51.md
(no output)   exit 0
$ sha256sum corpus/knowledge/memavailable-estimate-r51.md
b04f030d450b5a2f32de9efc84b9862e411a4ef56547307e2c3fec05846d4803  corpus/knowledge/memavailable-estimate-r51.md
$ git show 87e0c374537557754bf71dd68036ded3ddc6699c:corpus/knowledge/memavailable-estimate-r51.md | sha256sum
b04f030d450b5a2f32de9efc84b9862e411a4ef56547307e2c3fec05846d4803  -
```

Working tree == data commit for the entry, so the line locators below are the frozen bytes.

The scored draft is `/fast/scratch/hyaku/mori-r51/Mo51SimpEntry/draft.md`, build sha256
`3f3b8fd626d96d36ca2199c6137af68a2564abc2a5907b8fac69d25ca5ac16bb`; base copy sha256
`b04f030d450b5a2f32de9efc84b9862e411a4ef56547307e2c3fec05846d4803`.
`diff -u base.md draft.md` = 12 insertions, 17 deletions in 3 hunks (`:12-16`, `:46-55`, `:62-65`); nothing
else in the file differs.

## Redundancy inventory (frozen entry, 1-based line numbers)

| # | locator | what repeats | disposition |
|---|---|---|---|
| 1 | `:50` rule 3 | "Units are kB on every meminfo line (row 14)" restates row 14 verbatim in substance; "a ratio `MemAvailable/MemTotal` is unit-free" is arithmetic (kB/kB) — the only two things in the bullet, neither actionable | **deleted** |
| 2 | `:48` rule 2, first clause | "The figure excludes swap by construction (\"without swapping\")" restates row 1's quote; only the consequence half of the bullet is new | **compressed** to the consequence |
| 3 | `:14-16` intro | "an estimate computed by `si_mem_available()` … from free pages, the file LRU lists, reclaimable kernel memory and the zones' low watermarks, printed in kB by `meminfo.c.v7.2:62`" restates rows 2, 6, 7, 8, 10, 13 (inputs) and row 14 (kB); its "low watermarks" also duplicates rule 5 | **compressed** to the two file:line pointers |
| 4 | `:53-54` rule 5 | "a model whose holdbacks are min(half, low-watermark sum); the proc document says the model's accuracy varies by system (row 3)" restates rows 3, 8, 10, 13 before the action ("report the threshold as local") | **compressed**, action first, rows cited |
| 5 | `:12`, row 1, `:48` | swap stated three times: intro "before it swaps or kills", the row-1 quote, rule 2's "without swapping" | rule 2's copy dropped; intro keeps the lane framing |
| 6 | `:46-47` + `:64-65` | "do not rebuild it from meminfo fields" (rule 1) and "the estimate cannot be recomputed exactly from `/proc/meminfo` alone" (boundary) are the same instruction, and `:64-65` spends one bullet on two unrelated facts | **merged** into rule 1; "No host value is claimed as typical" stays its own bullet |
| 7 | `:62-63` | "v7.2 only." and "this entry claims only the v7.2 bytes" state the same scope twice inside one bullet | **compressed** to one scope sentence |
| 8 | `:46-47` | "that sum counts tmpfs and shmem pages that sit on anon LRU lists and that the estimate does not add (rows 4, 7, 17, 20)" re-derives four cited rows inside a rule whose imperative stands alone | **compressed** to the imperative + row numbers |
| 9 | `:51-52` rule 4 | "tmpfs and shared memory raise `Cached` without raising the estimate" paraphrases rows 4/5/7 — but it is the *reason* to compare `Shmem`, i.e. a derived diagnostic, not a row paraphrase | **kept** (this one earns its words) |
| 10 | `:59-61` boundary 1 | the enumerated `vm.min_free_kbytes`, `watermark_scale_factor`, swap list is longer than the reader needs, but every item is a distinct thing the entry must not touch (tsukuroi's province) | **kept verbatim** |

Prose mass (non-table, non-`source:` non-empty lines, title and meta lines included):
`base: lines=66 nonblank=57 prose_lines=29 prose_words=397 bytes=9038`
`draft: lines=61 nonblank=52 prose_lines=24 prose_words=322 bytes=8579`
→ −5 lines, −75 prose words (−18.9%), −459 bytes, with no claim row, no row number and no citation lost.

## Draft (prose sections only; splice over `:12-16`, `:44-55`, `:57-65`)

Intro — replaces `:12-16`:

```markdown
mori reports resource runway: how much memory the host can still give a new seat before it swaps or kills. The
fleet's dispatcher stops spawning seats when `MemAvailable` drops below a floor, and the lane's census and
pressure probes print `MemAvailable/MemTotal`. This entry says what that line is at kernel v7.2: the estimate
`si_mem_available()` computes (`show_mem.c.v7.2:32-72`) and `meminfo.c.v7.2:62` prints.
```

Reading rules — replaces `:44-55`:

```markdown
## Reading rules

- Read the published `MemAvailable` line; do not rebuild it as `MemFree + Cached` (rows 4, 7, 17, 20), and it
  cannot be recomputed exactly from `/proc/meminfo` alone because `totalreserve_pages` is not exported as a line.
- A reading of 0 is a clamped floor, not an exact zero; free swap keeps a host running past it (rows 1, 12).
- When `Cached` is large but `MemAvailable` is small, compare `Shmem`: tmpfs and shared memory raise `Cached`
  without raising the estimate [INFERENCE from rows 4, 5, 7, 17 — not measured on this host].
- Report a `MemAvailable` threshold as local, as the lane already does for its other thresholds (FR8): it is a
  threshold on a model whose holdbacks are min(half, low-watermark sum) and whose accuracy varies by system
  (rows 3, 8, 10, 13).
```

Boundaries — replaces `:57-65`:

```markdown
## Boundaries

- Detection and report only: this entry reads `/proc/meminfo`; it never changes `vm.min_free_kbytes`,
  `watermark_scale_factor`, swap or any limit (host configuration is tsukuroi's; the dispatcher's floor is the
  orchestrator's).
- v7.2 bytes only. The formula has held the same shape since the 2014 commit (S496); no other kernel is claimed.
- No host value is claimed as typical.
```

## Content preservation, sentence by sentence

| frozen text dropped or moved | where its content still lives |
|---|---|
| intro "from free pages, the file LRU lists, reclaimable kernel memory and the zones' low watermarks" | rows 2 (documented inputs), 6, 7, 8, 10, 13 |
| intro "printed in kB by `meminfo.c.v7.2:62`" | row 14 (kB via the `PAGE_SHIFT - 10` helper); the `meminfo.c.v7.2:62` pointer is kept in the intro |
| rule 1 "that sum counts tmpfs and shmem pages that sit on anon LRU lists and that the estimate does not add" | rows 4, 7, 17, 20, still cited on the surviving imperative |
| rule 2 "excludes swap by construction (\"without swapping\")" | row 1 (quote: "without swapping") |
| rule 3 "Units are kB on every meminfo line (row 14)" | row 14 |
| rule 3 "a ratio `MemAvailable/MemTotal` is unit-free" | arithmetic (kB/kB); no source row claims it, so nothing factual is lost — see Tradeoffs |
| rule 5 "holdbacks are min(half, low-watermark sum)" and "accuracy varies by system (row 3)" | kept in the reordered sentence, rows 3, 8, 10, 13 now all cited |
| boundary "v7.2 only. … claims only the v7.2 bytes" | one sentence, same scope, S496 kept |
| boundary "`totalreserve_pages` is not exported … cannot be recomputed exactly" | rule 1, same wording in substance |
| boundary "No host value is claimed as typical" | kept, own bullet |

No claim cell, row number, FR8 reference, S-id, `[INFERENCE]` tag or detection-only statement was removed.

## Counter score on the draft (dict-backed read, entailment arm ignored)

Method: import the frozen counter at the data revision with `importlib`, give `evaluate()` a dict-backed `read`
(`git show <rev>:<path>` for every path, the draft text substituted for the entry), and starve the entailment
arm (`ls=lambda d: []`) so the only possible failure is the arm I was told to ignore. Script (scratch, 5180
bytes, pinned to `REV` and `LANE`): builds the draft by slicing the committed entry at `## Claims` / `## Reading rules`
and substituting the three prose blocks, asserts the claims block is byte-identical, then scores base and draft.

```
$ cd /fast/scratch/hyaku/mori-r51/Mo51SimpEntry && export TMPDIR=$PWD/tmp && python3 -I -B score.py; echo exit=$?
working_tree_equals_rev: True
draft_sha256: 3f3b8fd626d96d36ca2199c6137af68a2564abc2a5907b8fac69d25ca5ac16bb
claims_block_identical: True
table_rows_identical: True
header_identical: True
base: lines=66 nonblank=57 prose_lines=29 prose_words=397 bytes=9038
draft: lines=61 nonblank=52 prose_lines=24 prose_words=322 bytes=8579
--- A base, entailment arm starved (table checks only) ---
False C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment
--- B draft, entailment arm starved (table checks only) ---
False C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment
--- C base, real w1/ vote files (informational) ---
False C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment
--- D draft, real w1/ vote files (informational) ---
False C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment
table_checks_pass_on_draft: True | base_same: entailment
exit=0
```

Reading of the score: every table/provenance/pin predicate is identical for base and draft
(`claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok`), and the only
`failed=` token on the draft is `entailment`, the arm I was told to ignore (starved, so `entailed=0` by
construction). Runs C/D add nothing because `.ufo/waves/round-51/w1/` has no reports committed at `87e0c37`
(`git ls-tree --name-only 87e0c37 .ufo/waves/round-51/w1/` prints nothing, `wc -l` = 0); the live votes live
only in the working tree, uncommitted.

Second check, run after I wrote this report: I extracted the three ```` ```markdown ```` blocks above and rebuilt
the draft from the committed entry. The rebuild is byte-identical to the scored draft
(`rebuild_sha256: 3f3b8fd626d96d36ca2199c6137af68a2564abc2a5907b8fac69d25ca5ac16bb`, `matches_scored_draft: True`,
`lines=61 prose_lines=24 prose_words=322 bytes=8579`), and scoring that rebuild gives the same line
(`C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok
entailed=0 dissent=0 … failed=entailment`). So the draft published in this report is the draft that was scored —
no transcription drift between the fenced blocks and the run.

For information only (not my judgment, counts only, no arithmetic on anyone's row): reading the working-tree
`w1/*.md` files gives 17 of 21 rows with at least one vote, 16 `entailed`-kind lines and 1 `overclaim`-kind line
at the time of my read. I did not vote, and I wrote no line beginning with that keyword.

## Tradeoffs

- **Deleting rule 3 loses "kB".** The unit fact survives in row 14's claim cell and in `S494`'s copy, but a reader
  who scans only the rules no longer sees it. If the L1 wants the reassurance, the cheapest restoration is one
  clause inside rule 1 ("values are kB, row 14") — not a separate bullet. I recommend deletion: a rule that only
  restates a row is exactly what this pass was asked to find.
- **"a ratio `MemAvailable/MemTotal` is unit-free" is real advice for the lane's probes** (they print that ratio),
  yet it is arithmetic, not a claim, and the intro already says the probes print the ratio. Deleted; restoration
  cost is one clause if the L1 disagrees.
- **Merging the non-recomputability clause into rule 1** makes rule 1 two lines long but removes a boundary bullet
  that mixed a scope statement with an arithmetic limit. If the L1 prefers Boundaries to carry all limits, leave
  `:64-65` as-is and delete the clause from rule 1 instead — the redundancy is the duplication, not either copy.
- **The intro keeps the "swaps or kills" framing** even though rows 1 and 6 are the only support; that framing is
  lane context (runway), not a claim, so I did not touch it. Prose facts are Mo51CritReadingRules' remit.
- **Named limit of the check I ran:** P-C2 never reads prose — it parses the table and the first 14 non-blank
  lines for provenance. So "table checks still pass" proves the table arm is untouched; it cannot prove the prose
  lost nothing. The preservation argument above is a per-sentence mapping, and it is the only evidence for the
  prose half. Nothing in the frozen counter would catch a prose deletion that dropped a fact.
- **Draft is a proposal, not a patch**: I did not edit the entry. Applying it as-is keeps the file at 61 lines
  and leaves `recheck:`, `verified-at:` and `coverage-map:` untouched.

## Cleanup

`rm -rf /fast/scratch/hyaku/mori-r51/Mo51SimpEntry` after copying the draft and the score output into this
report. The scratch was re-created once (mkdir + TMPDIR) for the rebuild-equivalence check above and removed
again; `[ -e …/Mo51SimpEntry ]` prints absent. No clone, no fixture repo, no PATH write, nothing left under
`/tmp` (only the 5180-byte script, `base.md` and `draft.md` lived in scratch/TMPDIR). `git status --porcelain`
over `corpus/knowledge/memavailable-estimate-r51.md corpus/SOURCES.md corpus/evidence/sources-r51/ tools/ SKILL.md
SHONEN.md` is empty — I changed no tracked file in the lane.

## Findings

- HIGH — `corpus/knowledge/memavailable-estimate-r51.md:50`: reading rule 3 exists only to restate claim row 14 and to state that a kB/kB ratio is unit-free; a reader cannot act on either half. Deletion candidate (draft deletes it).
- HIGH — `corpus/knowledge/memavailable-estimate-r51.md:48`: rule 2's first clause restates row 1's quote ("without swapping"); replace with the consequence (clamp at 0, free swap runs past it).
- MED — `corpus/knowledge/memavailable-estimate-r51.md:14-16`: the intro enumerates the estimate's inputs and its kB printing, which rows 2, 6, 7, 8, 10, 13, 14 already hold; the two file:line pointers are the only part a reader needs.
- MED — `corpus/knowledge/memavailable-estimate-r51.md:53-54`: rule 5 leads with a paraphrase of rows 3, 8, 10, 13 before reaching its action ("report the threshold as local"); put the action first.
- MED — `corpus/knowledge/memavailable-estimate-r51.md:12,46-47,64-65`: the swap idea is stated in three places and the "cannot be recomputed from meminfo" limit in two; one of each is enough.
- LOW — `corpus/knowledge/memavailable-estimate-r51.md:62-63`: the v7.2 scope is stated twice inside one boundary bullet.
- LOW — `corpus/knowledge/memavailable-estimate-r51.md:46-47`: rule 1 re-derives four cited rows' reasoning inside an imperative that stands without it.
- LOW — `.ufo/waves/round-51/count-c2.py` (predicate P-C2): no counter reads the entry's prose, so prose redundancy and prose claim loss are invisible to C1/C2; a prose regression can only be caught by a reviewer seat this round. Named limit, not a change request (predicates are frozen).
