measured 2026-10-23T07:44:28Z

# ReJudgeLesson5 — wave B re-judge of `### Item 5` (non-author)

Target: `### Item 5 — §1 last column vs ## Judges` under `## Round-34 corrections` in
`corpus/lessons/round-33.md` at `8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3`, answering routed defect
`corpus/lessons/round-33-verifier-spotcheck.md` §8 item 5 (`:235-237`: move S137's `:260` pointer and the omitted
clauses S137 ×3, S149 "different contracts", S058 "ancestors first" into §1's last column with a forward pointer; fix
":209 six" = five omitted plus one misfiled).

## Independent checks against committed bytes

1. S058 corrected row: retains the two original last-column clauses (`<commit>^1 <commit>` merge form; root needs
   `--root` — both verbatim in the unchanged cell `round-33.md:58`) and adds the combined `--reverse --topo-order lists
   ancestors first` clause, flagged "two-quote inference … unsupported under R-R" matching the Judges prose at
   `round-33.md:208-209` and receipt defect (4) `.ufo/waves/round-33/judge/JudgeRepairR32.md:77`. Teaches cell verified
   `corpus/SOURCES.md:64` ("rev-list --reverse --topo-order base..tip lists ancestors first").
2. S149 corrected row: retains all eight man-page clauses plus the "supersedes S128" / "only there" / "documentation
   gap" assessments and the S127/S003-by-id parenthetical from the unchanged cell `round-33.md:61` (full line read);
   adds "the two files are different contracts (lane assessment)" — verbatim second sentence of S149's teaches cell,
   `corpus/SOURCES.md:155`; receipt `JudgeRepairR32.md` "row S149 omitted-clause" agrees it is unsupported.
3. S137 corrected row: retains the two original clauses (`round-33.md:62` last column) and adds the three omitted
   clauses — "returned on master in February 2026", "current master", "(S016 documents it…)" — all verbatim in the
   teaches cell `corpus/SOURCES.md:143`; plus the `:260`-pointer note. All five omitted clauses and the pointer move are
   present; every row ends "See “Count and pointer correction” below." (forward pointer satisfied within the append-only
   constraint — the §1 table itself cannot be edited).
4. Pointer bytes: `corpus/evidence/recheck-r33/S137-main-750a.src:260` is
   `fprintf(stderr, "Option -k is ignored since earlyoom v1.2\n");` inside a bare `case 'k'` (`:259`); the kernel-OOM
   option is the separate `LONG_OPT_USE_KERNEL_OOM` (`:201` long-opt entry, `:315-317` case, `:352` help line). Nothing
   at `:260` ties `-k` to `--kernel-oom` — the block's "misfiled … does not tie `-k` to `--kernel-oom`" and "not support
   for the kernel-OOM option identity" are accurate. Judge dissent at `JudgeRepairR32.md` "row S137 supported-pointer 1:
   disagree" matches.
5. Count: `JudgeRepairR32.md:76` — "Omitted teaches clauses: 5 (S058 1, S149 1, S137 3), plus 1 misfiled S137 clause";
   `:77` lists the four concrete defects. The block's "five omitted teaches-cell clauses (S137 ×3, S149 ×1, S058 ×1)
   plus one misfiled S137 support pointer (`…JudgeRepairR32.md:76-77`)" matches in content (receipt says "clause",
   spotcheck/item say "pointer" — same defect). `round-33.md:209-210` indeed reads "those six clauses … S137's first
   pointer moves there too" (verified by numbered `awk` on the blob).
6. Spotcheck citation `round-33-verifier-spotcheck.md:152-155`: verified — those lines are the bare `case 'k'` /
   `LONG_OPT_USE_KERNEL_OOM` bullet, verbatim as claimed.
7. Verdict span `round-33.md:56-64`: contains the table header, the five `current → not current` rows (`:58-62`) and
   two prose lines; the append changes none of them.
8. Append-only: `git diff --numstat f10a320d 8d56809af -- corpus/lessons/round-33.md` → `50  0`; single hunk
   `@@ -209,3 +209,53 @@`, zero `-` lines. Nothing above the `## Round-34 corrections` heading changed.
9. Commit-time facts (task-mandated; the times live in Item 7's block): `fdf4371f` = `2026-10-22T23:39:02-03:00` =
   02:39:02Z as Item 7 states; `27969134` = `2026-10-22T23:28:27-03:00` = 02:28:27Z as stated; receipt headers
   `c1-controls.txt:1` (02:38Z) and `parity-freeze.txt:1` (02:3xZ) confirmed. No defects found there.

VERDICT: repaired — no wrong detail found. All three corrected rows carry every original clause plus exactly the
routed additions; the count correction is accurate against the receipt tally; all cited line locators land.

## Audit of .ufo/waves/round-34/wa/JudgeLessonItem5.md

Agree/disagree per factual claim (imprecision notes do not flip agree):

- §1 route match; spotcheck range `:235-237` — agree (awk-verified bounds).
- §2 omitted clauses at `round-33.md:207-208` — agree; minor: the S058 clause continues through `:209`.
- §2 teaches strings at `SOURCES.md:143` (three S137 phrases), `:155` ("The two files are different contracts"), `:64`
  ("rev-list --reverse --topo-order … lists ancestors first") — agree, all five strings verified at the cited lines.
- §3 `round-33.md:209` "those six clauses"; `JudgeRepairR32.md:76` tally quoted verbatim; `:77` = four concrete
  defects — agree.
- §4 src `:259-261` bare `case 'k'` + fprintf at `:260`; `:192` short-opt string; `:201` LONG_OPT entry; `:315-317`
  kernel_oom case; `:352-354` help; second URL `SOURCES.md:143` — agree, all byte-checked.
- §5 spotcheck `:152-155` verbatim — agree.
- §6 hunk `@@ -209,3 +209,53 @@`, context 209-211 preserved, verdicts at `:58-62` — agree; minor: "the cited span
  `:56-64` is the table" overruns the table by two prose lines (`:63-64`).
- §7 S149 source-cell parenthetical at `SOURCES.md:155`; AttackRepairS149 F1 (`oom_kill.c:233` totalpages,
  `base.c:3352` S_IRUGO, `base.c:1131-1133` floor, sha256 `cef1a2cf…`/`452f1348…` matching the cell's recorded hashes);
  `JudgeRepairR32.md:79` "row id is not a page" — agree.
- §8 diff `50 0` numstat, pure append — agree.
- §9 commit times `7d382043`=23:21:08-03:00, `89791013`=00:16:50-03:00, `f10a320d`=00:27:16-03:00,
  `8d56809`=02:34:40-03:00 — agree, all four `%cI`-verified.
- Residual notes (forward-pointer interpretation; "(lane assessment)" label consistency) are judgments, not factual
  claims — no disagreement.

AUDIT: agree 10 / disagree 0

## Tooling

- No installs/updates; pacman untouched. Lane access read-only (`git show/diff/log`, `grep`, `awk`, `sed` reads only).
- No subagents, no background jobs. Scratch: `/tmp/s149_orig.txt` only (outside lane bounds, transient).
