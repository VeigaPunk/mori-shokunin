measured 2026-10-23T09:10:43Z

# ScoutAppendDebt — classify the 15 in-place SOURCES edits the append-only check still flags

Attacks wave-1 `MineAppendOnly.md:166-182`, which marks all 15 ids `defect` without a per-id class or a lesson old-to-new check, and round-35 M2 (`corpus/lessons/round-35.md:65`), which routes the same 15 without saying which are claim rewrites.

Axes: (1) every flagged id classified, not a sample of 5; (2) old and new taken from `git log -p` on `corpus/SOURCES.md`, not from the checker alone; (3) class is one of real-content / formatting-only / rules-allow; (4) lesson old-to-new is yes only when the lesson text states both sides.

## Rule and run

CORPUS §SOURCES.md rule 2 (`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`): only status, recheck and used-by change in place, and that change is logged old-to-new; any other correction is a new row whose teaches opens `supersedes S0NN`. QUALITY 81 (`corpus/QUALITY.md:373-376`) says the same after the row's first published cells, and round-27 M2 (`corpus/lessons/round-27.md:32-39`) is the precedent: a logged same-round teaches edit (S124) was still a defect. Round-34's closure called S193's same-round anchor/teaches rewrite a form defect (`corpus/lessons/round-34-verifier-spotcheck.md:118`). Same-round is not an exception.

Check (scratch copy, not imported from the lane): `timeout 120 python3 /fast/scratch/hyaku/mori-r35/ScoutAppendDebt/check-sources-appendonly.py cedb0ec4f3a4f672804deac388b7191258f01fcd --repo /home/vgpnk/Projects/shokunin/mori-shokunin --show-cells` → exit 1, `appendonly_violations=15 ids=[S041,S044,S051,S062,S064,S179,S180,S181,S183,S184,S185,S186,S188,S189,S190]`. None of the 15 has a teaches row opening `supersedes` that id (S069 does, via S073, and is discharged). Diffs below are from `git log -p -G` of those ids (`/fast/scratch/hyaku/mori-r35/ScoutAppendDebt/logp-early.txt`, `logp-late.txt`) plus a cell-level opcode on the parent and the commit (`deltas.txt` in the same scratch dir).

No install. No formatting-only hit and no rules-allowed hit among the 15. S064's round-22 commits `8cb4afbf` and `da40bb20` change only used-by (allowed); the checker correctly omits them; `corpus/lessons/round-22.md:29,73` logs those used-by transitions.

## Per id

Columns are the 11-cell names. Logged means the lesson states the old cell text and the new cell text.

**S041** — commit `62db24c0` (2026-10-22 23:55 -0300, round-33: C1 FR6 entry…). First published `273aa74a` (round 17). Column: teaches. Delta: insert the two words lane rule before it does not identify. No other cell. Class: real content. The sentence is otherwise the same, but the label moves the clause from an implied source reading to lane doctrine, which is what round-32 §8 item 3 asked (`corpus/lessons/round-32-verifier-spotcheck.md:190-191`). The model it cites (S073, S074, S076) is a new supersede row, not an in-place edit. Logged: yes, `corpus/lessons/round-33.md:82`.

**S044** — same commit `62db24c0`. First published `273aa74a`. Column: teaches. Delta: insert lane rule before a commit-id read is not. Class: real content, same attribution move. Logged: yes, `round-33.md:83`.

**S051** — same commit `62db24c0`. First published `daceeec8` (round 18). Column: teaches. Delta: insert lane rule before A class-hit gate. Class: real content, same attribution move. Logged: yes, `round-33.md:84`.

**S062** — two commits. `62db24c0`: teaches gains lane rule before each of the -0 clause and the json.dumps clause. `ab8f4cfe` (2026-10-23 00:08 -0300, round-33 wave-2): teaches gains between JSON tokens after no whitespace. First published `daceeec8`. Class: real content. The second commit narrows a source claim (whitespace between tokens, not inside strings), which is not a label. Logged: yes as one net old-to-new, `round-33.md:85-88`, including the wave-2 addition. The lesson's summary sentence at `:79` (no other word changed) is false; the spot-check already says so (`round-33-verifier-spotcheck.md:43-44,238`). The bullets themselves are the log.

**S064** — `62db24c0`: scope gains lane rule before not remote publication; teaches replaces the comma after object id with semicolon plus lane rule, so then separately bind moves under the label. `ab8f4cfe`: teaches moves once and retain the full object id inside that lane-rule clause (page-stated flags stay outside). First published `367927c5` (round 19). Columns: scope, teaches. Class: real content (re-attributes procedure, and the second commit moves words). Logged: yes, `round-33.md:89-93`. The `:79` summary is the same false sentence as S062.

**S179** — commit `5126891` (2026-10-22 23:05 -0300), 44 seconds after first publish `55c3ed5`. Columns: scope, teaches. Scope: same work as S056 → the full-text mirror S056's source cell already names. Teaches: same article as S056 → duplicate URL already carried in S056's source cell. Class: real content (the rejection ground changes from same article to duplicate URL). Logged: no. The same commit rewrites the Gate decision cell of `corpus/lessons/round-32.md` (`git log -p -G S179 -- corpus/lessons/round-32.md`: minus same work as S056, plus duplicate URL) so the landed lesson states only the new side. There is no old-to-new pair in the lesson text. `round-32.md:69` is the new decision only.

**S180** — `ab8f4cfe`, first published `62db24c0` (same round, 13 minutes earlier). Columns: anchor, teaches. Anchor `stat.rst:21-22,71-73,79-80` → `:2-5,21-22,71-73,75-80`. Teaches: tick values → the millisecond wait values. Class: real content (drops the word tick and widens the lines). Logged: no cell old-to-new. `round-33.md:174` names AttackSrc180 for the entry row; `:180` does not list S180 among the tightened source cells.

**S181** — `ab8f4cfe`. Columns: source, scope, anchor. Teaches unchanged. Source gloss: tag-pinned source of the docs.kernel.org page → tag-pinned counterpart of that page (URL unchanged). Scope: field 10 (io_ticks) → how field 10 grows. Anchor `:22,33-36,76` → `:22,33-36,75-76`. Class: real content (what the row claims to cover, and its relation to S033). Logged: no. `round-33.md:180` says S181 cells and anchors were tightened, without the old or the new text.

**S183** — `ab8f4cfe`. Columns: anchor, teaches. Anchor `part_stat.h:10,61-63` → `:10,60-63`. Teaches: the whole disk (bdev_whole) → bdev_whole(part). Class: real content (the call and its argument replace a gloss). Logged: no. AttackSrc183 is named for the entry (`round-33.md:171`), not as a cell old-to-new.

**S184** — `ab8f4cfe`. Column: anchor only. `blk-core.c:1067-1068,1100,1110` → `:1067-1068,1100,1108-1110`. Teaches byte-identical. Class: real content of the locator (the cited span grows to include the part_stat_inc / part_stat_add lines). Not formatting: no whitespace or punctuation-only delta. Not an allowed column. Logged: no. `round-33.md:180` says S184 quotes widened, without the old span.

**S185** — `ab8f4cfe`. Columns: anchor, teaches. Anchor `blk-mq.c:856,862` → `:856,858,862` (adds the flag test). Teaches gains For a request flagged RQF_IO_STAT before blk_account_io_completion. Class: real content (a precondition the first published cell did not state). Logged: no. `round-33.md:170` records the entry-row guard, not the SOURCES old-to-new.

**S186** — `ab8f4cfe`. Columns: scope, anchor, teaches. Scope gains and the bdev_whole macro. Anchor `blk_types.h:25-26,31` → `:25-28,31,84-85`. Teaches gains bdev_whole(bdev) is bd_disk->part0. Class: real content (a second fact). Logged: no. Named only as tightened at `round-33.md:180`.

**S188** — `ab8f4cfe`. Columns: scope, anchor, teaches. Scope now says flush requests executed by the disk, which the block layer combines, and adds triggered by requests that are usually zero-size writes. Anchor patch lines 9,11 and 72 → 9,11 and 71-72. Teaches now names fields 16-17, at most one flush at a time, and barriers. Class: real content. Logged: no. AttackSrc188 is an entry note (`round-33.md:177`); `:180` says the cells were tightened, without old or new text.

**S189** — `ab8f4cfe`. Column: anchor only. Patch lines 9-10,14 → 7-17. Teaches byte-identical. Class: real locator change (a wider commit-message span), not formatting, not an allowed column. Logged: no. `round-33.md:180` says S189 quotes widened, without the old span.

**S190** — `ab8f4cfe`. Columns: scope, anchor, teaches. Scope narrows to the extended-statistics display (write_ext_stat) and excludes the default report. Anchor `iostat.c:1151-1152,1516-1517` → `:1444-1464,1516-1517 (write_ext_stat)`. Teaches: prints a write-sector rate of 0.0 → sets the write-sector value to 0.0, and adds that the default report computes its rate elsewhere. Class: real content (the row stops covering the default report). Logged: no. `round-33.md:178-180` records the entry narrowing and that cells were tightened, without the cell text.

## What does not fall out

The three lane-rule-only edits (S041, S044, S051) are the closest to formatting. They are not. Inserting lane rule changes who the following clause is attributed to, and the spot-check's own examples did that on a new supersede row. Logging the old-to-new (`round-33.md:82-84`) satisfies the log half of rule 2 and not the supersede half. QUALITY 81 requires both.

S184 and S189 change no teaches word. They still change the anchor, which rule 2 does not allow in place. A wider line span is a different citation, not a reflow.

No id in the 15 is a status, recheck or used-by edit. The only rules-allowed edits found while tracing them are S064's two used-by appends, which the check does not flag.

VERDICT: S041 defect
VERDICT: S044 defect
VERDICT: S051 defect
VERDICT: S062 defect
VERDICT: S064 defect
VERDICT: S179 defect
VERDICT: S180 defect
VERDICT: S181 defect
VERDICT: S183 defect
VERDICT: S184 defect
VERDICT: S185 defect
VERDICT: S186 defect
VERDICT: S188 defect
VERDICT: S189 defect
VERDICT: S190 defect
VERDICT: holds — all 15 are real content or locator changes of immutable cells, none formatting-only, none a column rule 2 allows; five are logged old-to-new in round-33 (S041, S044, S051, S062, S064) and ten are not

## Limits

Net cells are origin versus tip. S062 and S064 each have an intermediate cell at `62db24c0` that the round-33 bullets collapse into one old-to-new; both halves are in the log -p. Discharge is per id: a later edit of an already superseded row would not show, and none of these 15 is superseded at `cedb0ec4`. Unresolved: whether a future round will supersede the 15 or only the ten that lack a log. This seat did not edit SOURCES.md.
