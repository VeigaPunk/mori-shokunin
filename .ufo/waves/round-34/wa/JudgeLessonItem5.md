measured 2026-10-23T05:39:47Z

# JudgeLessonItem5 — round-34 wave A, Item 5 judge (non-author)

Target: block `### Item 5 — §1 last column vs ## Judges` under `## Round-34 corrections` in
`corpus/lessons/round-33.md` at `8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3`, answering routed defect §8 item 5 of
`corpus/lessons/round-33-verifier-spotcheck.md` ("Lesson round-33 §1 vs `## Judges`": move S137's `:260` pointer and the
omitted clauses into §1's last column with a forward pointer, and fix ":209 six" = five omitted plus one misfiled).

VERDICT: repaired. No wrong statement found in the block. Every factual claim checks against the committed bytes below.

## Checks against committed bytes

1. Route match. Spotcheck §8 item 5 (`round-33-verifier-spotcheck.md:235-237`) requires: append a correction moving S137's
   `:260` pointer and the omitted clauses (S137 ×3, S149 "different contracts", S058 "ancestors first") into §1's last
   column with a forward pointer, and fix ":209 six" (five omitted plus one misfiled). The block's table rows S058/S149/S137
   add exactly those clauses to the last-column rendering; each row ends "See “Count and pointer correction” below." (forward
   pointer); the Count subsection resolves "those six clauses" as 5+1. Moved.

2. Omitted-clause inventory. `round-33.md:207-208` (Judges prose) lists omitted clauses: S137 "returned on master in
   February 2026", "current master", "(S016 documents it…)"; S149 "the two files are different contracts"; S058 the combined
   "--reverse --topo-order lists ancestors first". The block's S137 row lists the three S137 phrases (all verbatim in S137's
   teaches cell at `corpus/SOURCES.md:143`: "returned on master in February 2026", "while current master grows a
   --kernel-oom long option", "(S016 documents it from the master README)"); the S149 row adds "the two files are different
   contracts" (verbatim second sentence of S149's teaches cell, `corpus/SOURCES.md:155`); the S058 row adds "the combined
   `--reverse --topo-order lists ancestors first` conclusion" (teaches cell at `corpus/SOURCES.md:64`: "so rev-list --reverse
   --topo-order base..tip lists ancestors first"). All five quoted strings exist in the teaches cells at the cited lines.

3. Count correction. `round-33.md:209` says "those six clauses"; `JudgeRepairR32.md:76` tally reads "Omitted teaches clauses:
   5 (S058 1, S149 1, S137 3), plus 1 misfiled S137 clause", and `:77` lists the four concrete defects. The block's
   "five omitted teaches-cell clauses (S137 ×3, S149 ×1, S058 ×1) plus one misfiled S137 support pointer
   (`.ufo/waves/round-33/judge/JudgeRepairR32.md:76-77`)" matches the receipt byte-for-byte in content. Correct.

4. S137 `:260` pointer byte check. Committed copy `corpus/evidence/recheck-r33/S137-main-750a.src` (585 lines): `:259-261`
   is the bare `case 'k'` printing "Option -k is ignored since earlyoom v1.2\n" (`:260`); `:192` is the short-option string;
   the kernel-OOM option is the separate `LONG_OPT_USE_KERNEL_OOM` at `:201` (`{ "kernel-oom", no_argument, NULL,
   LONG_OPT_USE_KERNEL_OOM }`), `:315-317` (case sets `args.kernel_oom = true`; prints "Using kernel OOM killer (requires
   Linux v5.17+)\n") and `:352-354` (help line "--kernel-oom use kernel OOM killer via /proc/sysrq-trigger"). Nothing at
   `:260` ties `-k` to the kernel-OOM option, so the block's "misfiled as support for “v1.2 removal” because it does not tie
   `-k` to `--kernel-oom`" and "not support for the kernel-OOM option identity" are accurate. The S137 page is main.c at
   commit `750a7c0d` (source cell second URL, `corpus/SOURCES.md:143`), not v1.9.0 — consistent with the row text.

5. Spotcheck citation. The block cites "the spotcheck describes the bare `case 'k'` and the separate option
   (`corpus/lessons/round-33-verifier-spotcheck.md:152-155`)". Lines 152-155 read exactly: "`S137-main-750a.src:259-261`
   is a bare `case 'k'` printing "Option -k is ignored since earlyoom v1.2". The kernel-OOM option is a separate option,
   `LONG_OPT_USE_KERNEL_OOM` (`:201`, `:315-317`, `:352-354`). Nothing on S137's named pages ties `-k` to that option."
   Citation correct.

6. Pointer/count supersede targets. `round-33.md:209-210` (unchanged by the append; the diff shows context lines 209-211
   preserved) hold "those six clauses are unsupported under R-R and belong in the last column of §1; S137's first pointer
   moves there too." The block corrects exactly this. The five not-current verdicts live in the §1 table rows at
   `round-33.md:58-62` (S058, S117, S128, S149, S137 all "current → not current"); the block changes none of them, and the
   cited span `:56-64` is the table. Correct.

7. S149 support-language check. The block's S149 row states the source cell "also refers to S127 and S003 by id" —
   `corpus/SOURCES.md:155` source cell reads "(the v7.2 code that enforces them is S127; the oom_badness scaling and the
   absent 3% root term are S003)" — and that wave-2 AttackRepairS149 found lane-root copies `base.c`/`oom_kill.c` state the
   scaling, read-only export and write floor. `AttackRepairS149.md` F1 confirms: `oom_kill.c:233` `adj *= totalpages / 1000;`,
   `base.c:3352` `ONE("oom_score", S_IRUGO, proc_oom_score)`, `base.c:1131-1133` unprivileged-write floor (sha256 `cef1a2cf…`
   / `452f1348…` match the cell's recorded hashes). "Other rows' pages" matches the repair judge's R-R application
   (`JudgeRepairR32.md:79`: the pages are named by URL only in S127/S003 source cells; a row id is not a page). Correct.

8. Append-only confirmation. `git diff f10a320d 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 -- corpus/lessons/round-33.md`
   is `@@ -209,3 +209,53 @@` with only added lines (0 deletions); the Item 5 block is part of that pure append. Nothing
   above the `## Round-34 corrections` heading changed.

9. Commit-time facts: none asserted inside Item 5 (the receipt-time claims are Item 7's scope), so no `%cI` check needed here.
   For reference, `7d382043` = 2026-10-22T23:21:08-03:00 (round-32 spotcheck), `89791013` = 2026-10-23T00:16:50-03:00
   (round-33 outcome), `f10a320d` = 2026-10-23T00:27:16-03:00 (round-33 spotcheck), `8d56809` = 2026-10-23T02:34:40-03:00.

## Residual risk / verification gaps

- The block re-presents the §1 last-column rows as "corrected" renderings; it does not insert a physical pointer inside the
  byte-unchanged §1 table itself (append-only constraint). The forward pointer exists in the correction rows
  ("See “Count and pointer correction” below."), which I accept as satisfying "with a forward pointer". This is the only
  interpretive judgment; it does not conflict with any committed byte.
- "The two files are different contracts" is labeled "(lane assessment)" in the corrected S149 row; the receipt supports its
  unsupported placement but does not itself use the words "lane assessment" for that clause. The label is consistent with how
  the same row classifies "only there"/"documentation gap"; not a factual error.

## Tooling

- No installs/updates. Read `/home/vgpnk/.omp/agent/RULES.md`. Lane access read-only (git show/ls-tree/diff only);
  scratch under `/fast/scratch/hyaku/mori-r34/a2-JudgeLessonItem5/`. No subagents, no background jobs.
