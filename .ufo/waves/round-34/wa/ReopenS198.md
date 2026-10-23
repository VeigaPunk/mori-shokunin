measured 2026-10-23T05:38:48Z

# ReopenS198 — live re-open and clause-by-clause judgment (mori round 34 attempt 2, wave A)

Seat: MoriR34A2.ReopenS198 (leaf, no subagents). Judged row: `corpus/SOURCES.md:204` at
`8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3` (worktree copy verified byte-identical to that rev:
`git diff --quiet 8d56809 -- corpus/SOURCES.md corpus/evidence/sources-r34/S198.src` exit 0; blob
`be5bab20b2abf278fd7d7370c1a082de0928b1ed`). Note: lane HEAD is now `fd25213` (round-34 wave-A
spec/dispatch commit); it does not touch these files.

## 1. Live re-open (two fetches)

- URL: `https://raw.githubusercontent.com/torvalds/linux/v4.19/block/genhd.c`
- Fetch 1 at 2026-10-23T05:38:48Z; fetch 2 at 05:38:49Z (second pass also stamped 05:38:49Z).
- sha256 of both fetches: `4c55aeba02bfaecee8ef5a20514f834f2aa34a338f51a66a83bcc40d5a7588f1`; `cmp` identical.
- Committed copy `corpus/evidence/sources-r34/S198.src` (2024 lines, 50211 B): sha256
  `4c55aeba02bfaecee8ef5a20514f834f2aa34a338f51a66a83bcc40d5a7588f1` == fetched. The live source matches the
  committed copy byte-for-byte.

## 2. Teaches cell — clause by clause

Teaches cell (`SOURCES.md:204`): "The v4.19 diskstats_show format has 18 conversions and its argument list
ends with four STAT_DISCARD values (ios, merges, sectors, msecs). lane rule: with S197, the printer first
carries discard values at v4.19, not v4.18."

Clause 1 — "The v4.19 diskstats_show format has 18 conversions": **supported**. The `seq_printf` call at
`S198.src:1336-1358` has 18 format specifiers (lines 1336-1340: 3+4+4+3+4) and exactly 18 arguments (lines
1341-1357: major, minor, name + 15 value arguments). The argument list is quoted as five contiguous slices (all
3-25 words, no `"`, no `|`):
- `S198.src:1341-1342` (5 words): "MAJOR(part_devt(hd)), MINOR(part_devt(hd)), disk_name(gp, hd->partno, buf),"
- `S198.src:1343-1346` (9 words): "part_stat_read(hd, ios[STAT_READ]), part_stat_read(hd, merges[STAT_READ]), part_stat_read(hd, sectors[STAT_READ]), (unsigned int)part_stat_read_msecs(hd, STAT_READ),"
- `S198.src:1347-1350` (9 words): "part_stat_read(hd, ios[STAT_WRITE]), part_stat_read(hd, merges[STAT_WRITE]), part_stat_read(hd, sectors[STAT_WRITE]), (unsigned int)part_stat_read_msecs(hd, STAT_WRITE),"
- `S198.src:1351-1353` (5 words): "inflight[0], jiffies_to_msecs(part_stat_read(hd, io_ticks)), jiffies_to_msecs(part_stat_read(hd, time_in_queue)),"
- `S198.src:1354-1357` (9 words): "part_stat_read(hd, ios[STAT_DISCARD]), part_stat_read(hd, merges[STAT_DISCARD]), part_stat_read(hd, sectors[STAT_DISCARD]), (unsigned int)part_stat_read_msecs(hd, STAT_DISCARD)"
The count 18 is arithmetic over the anchored block; the format string itself is not quoted because it contains
`"` characters (excluded by the quote rule).

Clause 2 — "its argument list ends with four STAT_DISCARD values (ios, merges, sectors, msecs)": **supported**.
The final four arguments of the call are `S198.src:1354-1357` (quote above, 9 words): the in four are exactly
`ios[STAT_DISCARD]`, `merges[STAT_DISCARD]`, `sectors[STAT_DISCARD]`, and
`part_stat_read_msecs(hd, STAT_DISCARD)` (ios, merges, sectors, msecs).

Clause 3 — "lane rule: with S197, the printer first carries discard values at v4.19, not v4.18": exempt from
quotes (labelled `lane rule:`); fact-checked. Live fetch of the v4.18 URL (sha256 `96b5638180eb70886195b46722681623301c328763b47c674a6543b27c3e748b` == committed `S197.src`): the v4.18 `diskstats_show` call at `S197.src:1336-1351` has 14 conversions and its argument list ends with `inflight[0]`, `io_ticks`, `time_in_queue`, with no `STAT_DISCARD`. The v4.19 call (clauses 1-2) is the first tagged printer carrying discard values. The rule holds against S197's own committed copy.

## 3. Anchor check

Anchor cell: `block/genhd.c:1336-1358; tag v4.19`. In `S198.src` (committed copy == live fetch), lines
1336-1358 hold the `seq_printf` call: format string at 1336-1340, full 18-argument list at 1341-1357, closing
`);` at 1358. The cited line numbers hold the cited code. The URL pins tag `v4.19`; re-opened content matches.

## 4. Findings (by severity)

1. No defect found in the anchor cell (holds; 1336-1358 contain the call and complete argument list).
2. No defect found in the teaches cell: all three clauses are supported (clauses 1-2 quoted above; clause 3
   fact-checked against live v4.18 == S197.src).
3. Minor note (not a defect): "18 conversions" is an arithmetic inference over the anchored block rather than a
   literal sentence in the file; the five argument-list quotes anchor it.

## 5. Residual risk / verification gaps

- Only the pinned tag v4.19 was re-opened (what the row cites); no claim about later tags.
- The lane-rule comparison rests on S197's committed copy == live v4.18 (verified, hash above).
- Row cells outside this judgment's scope (status `mined`, recheck `on-release`, used-by) were not assessed.

## 6. Tooling record

No tool installed or updated; used existing curl, git (read-only), sed, sha256sum, wc, cmp. No pacman transaction.

## 7. Proposed Gate row

| S198 | https://raw.githubusercontent.com/torvalds/linux/v4.19/block/genhd.c | 2026-10-23T05:38:48Z | 4c55aeba02bfaecee8ef5a20514f834f2aa34a338f51a66a83bcc40d5a7588f1 | `S198.src:1341-1342` (5 words): "MAJOR(part_devt(hd)), MINOR(part_devt(hd)), disk_name(gp, hd->partno, buf),"; `S198.src:1343-1346` (9 words): "part_stat_read(hd, ios[STAT_READ]), part_stat_read(hd, merges[STAT_READ]), part_stat_read(hd, sectors[STAT_READ]), (unsigned int)part_stat_read_msecs(hd, STAT_READ),"; `S198.src:1347-1350` (9 words): "part_stat_read(hd, ios[STAT_WRITE]), part_stat_read(hd, merges[STAT_WRITE]), part_stat_read(hd, sectors[STAT_WRITE]), (unsigned int)part_stat_read_msecs(hd, STAT_WRITE),"; `S198.src:1351-1353` (5 words): "inflight[0], jiffies_to_msecs(part_stat_read(hd, io_ticks)), jiffies_to_msecs(part_stat_read(hd, time_in_queue)),"; `S198.src:1354-1357` (9 words): "part_stat_read(hd, ios[STAT_DISCARD]), part_stat_read(hd, merges[STAT_DISCARD]), part_stat_read(hd, sectors[STAT_DISCARD]), (unsigned int)part_stat_read_msecs(hd, STAT_DISCARD)" | admit, A, mined |

VERDICT: admit
