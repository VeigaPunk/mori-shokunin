# AttackSrc188 — S188 (Linux commit b6866318, flush iostat counters)

Advisory source review, not the C1 judge receipt. Targets: `corpus/SOURCES.md:194` (S188 row),
`corpus/lessons/round-33.md:23` (S188 Gate row), and the one consumer
`corpus/knowledge/disk-write-rate-r33.md:29` (row 11). Revision `62db24c`; working tree identical for these files.
Governing text: R-J and R-R as frozen in the assignment (contract A1 not needed for a source row).

## Checks run (all with output below)

| # | check | result |
|---|---|---|
| 1 | live re-fetch `curl -sSL --fail -m 60 <url>` | HTTP 200, 8897 bytes, no 429, no retry needed |
| 2 | sha256 live vs Gate vs committed copy | all three `a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89` |
| 3 | `cmp live.src corpus/evidence/sources-r33/S188.src` | `IDENTICAL` (221 lines, 8897 bytes both) |
| 4 | each Gate quote at its `file:L-M` locator | all three exact (below) |
| 5 | each quote inside whitespace-collapsed copy | all three `CONTAINED` |
| 6 | Gate word-count labels (`wc -w` on the exact quoted strings) | 10 / 10 / 11 — matches the labels |
| 7 | anchor hunk identity | `:9,:11` in commit message (message `:6-14`, `---` at `:18`); `:72` inside `Documentation/admin-guide/iostats.rst` hunk (`diff --git` `:60`, hunk `@@ -121,6 +121,15 @@` `:67`) — accurate |
| 8 | URL pinning and duplication | commit-sha-pinned (40-hex in path); `grep -F '<sha>' SOURCES.md` → only `:194`; `grep -rn 'b6866318' corpus/*.md` → only `SOURCES.md:194` + `lessons/round-33.md:23` |
| 9 | kind / tier | `code` + `A` matches corpus convention for upstream commit `.patch` views (`SOURCES.md:165` S159 earlyoom, `:195` S189 linux) |
| 10 | undeclared consumers of S188 | `grep -rn 'S188' corpus --include=*.md --include=*.py` → only the entry row 11, its Gate row, its SOURCES row |
| 11 | provenance | row authored in the single round-33 commit `62db24c`; not a round-32 repair row |

Locator output (committed copy):
```
9:Block layer has sophisticated engine for combining several flush requests
11:Requests which trigger flushes usually are barriers - zero-size writes.
72:+    This counts flush requests executed by disk. Not tracked for partitions.
```

## Findings

### A. "after the block layer combines them" is stated only at lines the anchor and Gate omit — severity: major
Attacks `corpus/SOURCES.md:194` (scope col. 5 and teaches col. 7) and, through them,
`corpus/knowledge/disk-write-rate-r33.md:29` ("after the block layer merged flush requests").

The three located quotes state (i) a combining engine exists (`S188.src:9`) and (ii) the counter
counts flush requests executed by disk (`S188.src:72`). **No located quote states the sequencing**
that the counted flush is a *merged* one, i.e. the temporal word "after". The sequencing is stated
verbatim, twice, in the committed copy — but at lines the anchor cell does not name and the Gate row
does not quote:
```
$ grep -n 'Block layer combines flush requests\|Not tracked for partitions\|combining several flush requests' S188.src
9:Block layer has sophisticated engine for combining several flush requests
71:+    Block layer combines flush requests and executes at most one at a time.
72:+    This counts flush requests executed by disk. Not tracked for partitions.
102:+Block layer combines flush requests and executes at most one at a time.
103:+This counts flush requests executed by disk. Not tracked for partitions.
```
The anchor cell reads "patch lines 9,11 (commit message) and 72 (iostats.rst hunk)" — `:71` and
`:102` are named by neither it nor the Gate quote list. Under R-J's closing clause ("including a row
the judge would accept only with a caveat"), a judge confined to the located quotes can hold the
"after merging" clause caveat-dependent and call row 11 unsupported. This is a locator omission, not
a factual error: the copy states the fact at `:71` and again at `:102`, so the cheapest repair is to
add `:71` to the anchor cell and to the Gate quote list (no re-fetch, bytes already committed).

### B. The scope cell does not cover a fact the teaches cell asserts and the anchor cites — severity: minor
`corpus/SOURCES.md:194` scope: "what the flush counters count: disk-executed flushes after
block-layer merging, not tracked for partitions". Teaches adds a third fact, "the triggering requests
are usually zero-size writes", and the anchor names `:11` for it; row 11
(`corpus/knowledge/disk-write-rate-r33.md:29`) actually consumes that fact ("the requests that cause
flushes are mostly barriers that carry no data"). So the source is used for a fact its declared scope
does not license. Fact itself is quoted verbatim at `S188.src:11` — no overreach, but scope and
teaches should be brought into line (either name the trigger clause in scope or drop it).

### C. "flush counters" referent and noun gloss are not located — severity: minor
Teaches/scope say "flush counters count flushes ..."; the located quote `:72` says "**This** counts
flush requests executed by disk", whose referent is the field-16 heading at `S188.src:68`
("`+Field 16 -- # of flush requests completed`", with `:74` field 17). Neither `:68` nor `:74` is in
the anchor cell, so "This" has no located antecedent, and "flushes" substitutes for "flush requests".
Under a word-for-word reading this is a caveat, not a falsehood. Adding `:68` (or `:68-74`) to the
anchor removes it.

### D. Patch code prints flush fields on partition lines — severity: none (adversarial, resolved)
`block/partition-generic.c` hunk (`S188.src:185-205`) adds `part_stat_read(p, ios[STAT_FLUSH])` and
its msecs to `part_stat_show`, i.e. partition lines of the stat file do carry the two flush columns.
That looks like tension with "Not tracked for partitions" (`:72`), but the accounting path is
disk-scoped: `blk_account_io_flush` (`S188.src:139-147`) increments `rq->rq_disk->part0`, never the
request's partition, so a partition line prints a never-incremented counter. The doc claim, the
teaches clause and row 11's "partitions do not track them" stand; the code corroborates them. No repair.

### E. Row 11 wording beyond its located quotes — severity: minor
Attacks `corpus/knowledge/disk-write-rate-r33.md:29`.
- "mostly barriers that carry no data" vs quote "usually are barriers - zero-size writes"
  (`S188.src:11`): "mostly"/"usually" and "carry no data"/"zero-size" are glosses. Defensible as
  definitional, but a caveat under R-J's word-for-word reading. [INFERENCE] on the gloss reading.
- Action "never add them to sectors written" is not stated by any located quote; it follows from
  `:72` counting *requests* plus S187's field 10 being "sectors written". [INFERENCE], arithmetic
  rather than quoted. No located quote states "the flush values are not sector counts".

## Not a defect / no defect found
- Live bytes, Gate sha256 and committed copy agree exactly (check 2, 3) — the copy is honest.
- All three quotes are verbatim, at their stated locators, inside the collapsed copy (checks 4, 5);
  word-count labels 10/10/11 are correct (check 6) — the round-29 mislabel class does not recur here.
- Anchor hunk/file attributions are accurate (check 7); URL is commit-pinned and carried by no other
  SOURCES row (check 8); kind `code` / tier `A` follow the corpus convention for upstream patch views
  (check 9), though note all three located quotes come from the commit message and a Documentation
  hunk, not from any `.c` hunk — the row's evidence is documentary even though its kind is code.
- used-by cell is complete and accurate (check 10); `opened 2026-10-23` is UTC-consistent with the
  Gate `2026-10-23T02:40:15Z` (local `date` at review: `Thu 22 Oct 2026 11:58:38 PM -03` = `Fri 23 Oct 2026 02:58:38 AM UTC`) — not a future date.

## Remaining unknowns
- Whether the C1 judge reads "the quotes located in the committed copies" as the Gate-listed quotes
  (then finding A bites row 11) or as any quote in the copy (then finding A is documentation-only).
  A1 as summarised in this assignment does not settle it; finding A is the cheapest hedge either way.
- S187's contribution to row 11's partition clause is not re-attacked here (separate seat).

## Process
No edits outside this report; scratch at `/fast/scratch/hyaku/mori-r33/AttackSrc188/` (`live.src`,
`collapsed.txt`, `q9.txt`, `q11.txt`, `q72.txt`). Read-only `git log`/`git show` only; no writes, no
sandbox clone needed. No tool install or update (nothing was missing). No background job, no subagent,
no omp invocation. curl completed (exit 0); no process of mine is left running.
