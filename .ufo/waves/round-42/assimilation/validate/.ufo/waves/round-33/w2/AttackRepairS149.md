# AttackRepairS149 — falsification of the S149 repair row

Target: `corpus/lessons/round-33.md:61` (§1 row `| S149 | ...`) under R-R; compared with
`.ufo/waves/round-33/w1/RepairS149.md` and closure list `corpus/lessons/round-32-verifier-spotcheck.md:91`.
Measured revision `62db24c`; base row `git show 7d382043:corpus/SOURCES.md:155`.

## Findings by severity

### F1 — MAJOR: committed copies of two pages the row names state kernel clauses the repair row marks "unsupported on every page the row names" (round-33.md:61, column 5)

S149's source cell names the kernel pages three ways: row ids ("the v7.2 code that enforces them is
S127; the oom_badness scaling and the absent 3% root term are S003"), explicit paths+lines
("fs/proc/base.c:583-602 … mm/oom_kill.c:199-237 … kernel/fork.c:1721-1775"), and pinned sha256s
("base.c 98,196 B sha256 cef1a2cf…, fork.c 85,725 B sha256 359882ea…, oom_kill.c 34,311 B sha256
452f1348…"). The lane tree at 62db24c contains committed byte-exact copies of two of them at repo root:

- `git show 62db24c:base.c | sha256sum` → `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6`
- `git show 62db24c:oom_kill.c | sha256sum` → `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`
- both match the cell verbatim; added in `763d346` (round-28 "misroot sweep" commit; root-level
  `git ls-tree -r 62db24c` shows `base.c`, `oom_kill.c` at repo root — that is why a
  `corpus/evidence/` scan misses them). `fork.c` is NOT committed (`git ls-tree` hit count 0).

Committed-copy clauses the row calls unsupported:

- "`totalpages/1000`" scaling — `oom_kill.c:233` `adj *= totalpages / 1000;` (in `oom_badness`, `:199`).
- read-only `[0,2000]` export — `base.c:591-597` comment "scale the badness value into [0, 2000]
  range which we have been exporting" plus `base.c:3352` `ONE("oom_score", S_IRUGO, proc_oom_score)`
  (read-only mode; the neighboring entries `:3353-3354` are `S_IRUGO|S_IWUSR`).
- unprivileged-write floor — `base.c:1131-1133` `if ((short)oom_adj < task->signal->oom_score_adj_min
  && !capable(CAP_SYS_RESOURCE)) { err = -EACCES; … }` (write path gated on the floor).
- "absence of the 3% root term in v7.2" — weaker: `grep -niE "cap|root|privileg" oom_kill.c:199-237`
  → 0 hits, so the function visibly lacks the term, but no single quote *states* an absence;
  borderline under R-R's "a quote … states it".

Column 4 "supported on another page" lists only `S128-S149-oom_score.src:97-98`; it omits the
committed base.c/oom_kill.c support. Consequence limited: the verdict `current → not current` still
stands because the *population page alone* (adj manual, `recheck-r32/S149.src`) carries none of the
kernel clauses, and the fork-copy clause is unsupported on every committed named page (no `fork.c`;
`grep -i fork recheck-r32/S149.src` → 0 hits; the score page's `fork(2)` at `:86` is a scoring-factor
hyperlink, not a copy statement). But the row's support accounting is wrong and its parenthetical
rationale is false (F2). The seat report inherits the same miss: `w1/RepairS149.md:42` claims the
kernel paths "are not either named manual-page URL and cannot satisfy the population-page test" and
its unsupported-clause table never checks the root-committed kernel copies.

### F2 — MAJOR (factual): "(the kernel facts are S127/S003, not named in this cell)" is false (round-33.md:61)

"this cell" most naturally reads as the source cell the R-R test runs on; that cell names `S127` and
`S003` verbatim ("…is S127; …are S003", `SOURCES.md:155`). The accurate claim is the closure's
narrower one — *teaches* cell has "kernel file paths only, no source ids"
(`round-32-verifier-spotcheck.md:91`) — which the seat report also stated correctly (`RepairS149.md:42`).
The row compresses it into a statement that is false under the source-cell reading and hides the real
reason those clauses fail: not naming, but (for `fork.c`) no committed copy. Combined with F1, a
judge applying this row's reasoning would wrongly reject S127/S003-named kernel clauses even where
committed support exists.

### F3 — MINOR: forgotten teaches clause — "supersedes S128 — the old row said …" is unclassified

The teaches cell opens with a row-history clause ("the old row said the pages' inheritance and
privilege sentences belong to the legacy oom_adj file"). The repair row's columns never classify it:
not population-carried, not on another page, not in the unsupported list. The seat report did flag it
(`RepairS149.md:29`, "keep this as correction history, not source teaching"); the row drops that
treatment. Also unlisted: the umbrella clause "the two files are different contracts" (its atomic
parts are covered; omission defensible). No `lane rule:` declaration was added for either, unlike the
§3 treatment of six other rows' lane-inference clauses.

## Checks that passed

- (a) Pointer `S128-S149-oom_score.src:97-98`: committed at `corpus/evidence/recheck-r33/` in
  62db24c, sha256 `6169628d…` == cell's recorded score-page hash; `:97-98` states "The oom_score also
  reflects the adjustment specified by the oom_score_adj or oom_adj setting" — supports the clause,
  and the score page is named in the cell's own source text.
- (c) Column 3 matches the closure list `spotcheck.md:91` verbatim (fork copy and floor;
  unprivileged-write floor; kernel scaling; `[0,2000]` export; root allowance absent in v7.2).
- (b) On the two committed manual-page copies, the kernel/meta clauses are genuinely absent:
  `grep -in` for `fork|copies|copy_signal|unprivileged|totalpages|oom_badness|2000|read-only|S_IRUGO`
  on `recheck-r32/S149.src` → 0 hits (CAP_SYS/privileged/inherits hits at `:146-147` are the oom_adj
  file, not the oom_score_adj floor); same greps on `S128-S149-oom_score.src` → only `fork(2)` link
  `:86` and "privileged (-)" `:80`, neither stating the clauses. "only there" and "documentation gap"
  are assessments no page states — correctly in column 5.
- Population page is the sole first URL of `corpus/lessons/round-32.md:54`; score page is the second
  URL — population-alone test is the right one.

## Residual risk / verification gaps

- Whether a root-level committed file (outside `corpus/evidence/`) counts as a "committed copy"
  under the repair convention is a lane definition; if it does not, F1's classification half weakens
  but F2's "not named in this cell" remains false regardless, since the cell names the pages.
- Did not re-check the S058/S117/S128/S137 sibling rows; the same root-copy blind spot may apply to
  S128 (committed `base.c` supports its `totalpages/1000` and `[0,2000]` clauses too — worth a look).
- No tool installs; tooling rules read earlier in session (`/home/vgpnk/.omp/agent/RULES.md`).
  Lane access read-only; no git/jj writes; one backgrounded `find` timed out at 300 s (killed).
