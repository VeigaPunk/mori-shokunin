measured 2026-10-23T05:39:45Z

# JudgeSkillCorrection — round-34 correction to SKILL.md Round33 section (rev 8d56809)

Seat: MoriR34A2.JudgeSkillCorrection (leaf; no subagents). Judge at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 (lane tip when dispatched), read from sandbox clone /fast/scratch/hyaku/mori-r34/a2-JudgeSkillCorrection/lane at that rev. No tool installed (none needed). No git/jj writes anywhere; reads only.

## Scope

The `Round34 correction to the Round33 section above` paragraph, SKILL.md:836-842 at 8d56809, against routed defects round-33-verifier-spotcheck.md §8 item 2 (lines 228-230) and item 4 (lines 233-234). Q1: is the old iostat clause (SKILL.md:820, last Round33 rule) aligned with entry row 14 without a new overclaim? Q2: do the Round33 rules citing rows 3, 6, 7, 13 (SKILL.md:816-818) hold under rows 3r/6r/7r/13r?

## Q1 — iostat clause alignment (item 4)

Old clause SKILL.md:820: "an iostat 0.0 is unavailable or unknown, never a zero write rate". Item 4 says row 14 teaches less: an idle device also shows 0.0 [INFERENCE], so align with row 14.

Correction text SKILL.md:838-842: narrows the clause to row 14 — 0.0 "does not by itself show an unchanged counter, because iostat prints 0.0 when the newer sectors-written count is below the older one; read the raw counters before reading that 0.0 as anything. An idle device also shows 0.0 [INFERENCE, closure §8 item 4], so 0.0 alone is neither a zero rate nor an unavailable one."

Check against entry row 14 (disk-write-rate-r33.md:33): observation = iostat extended stats show a zero write-sector value; reading = iostat takes ioi (current) / ioj (previous); a current sectors-written count below the previous one sets the value to 0.0; verdict = "Do not read a zero write-sector value in iostat's extended statistics as an unchanged counter without the raw counters". The correction's first sentences restate the row-14 reading and verdict. Source verified: S190.src:1516-1517 (`xios.wsectors = ioi->wr_sectors < ioj->wr_sectors ? 0.0 : S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);` inside write_ext_stat; S190 row SOURCES.md:196 locator 1444-1464,1516-1517, teaches cell matches).

Alignment: yes; the old overclaim ("never a zero write rate") is gone — the new sentence says 0.0 alone is indeterminate between a true zero (idle) and an unavailable interval (wrapped), and the idle case is disclosed with the explicit [INFERENCE, closure §8 item 4] tag (same tag the lesson itself used). No new sourced overclaim: the only non-row-14 element is the tagged inference, which is honest disclosure, not a claim.

VERDICT: supported

## Q2 — Round33 rules under rows 3r/6r/7r/13r (item 2)

Correction SKILL.md:836-838: Round33 rules citing rows 3/6/7/13 rest on 3r/6r/7r/13r, which "cite every source they need".

Entry revision section (disk-write-rate-r33.md:65-88) is append-only: `git diff ba525e1 8d56809 -- corpus/knowledge/disk-write-rate-r33.md` = 25 insertions, 0 deletions; rows 1-14 untouched (row 14 stays as round-33 judged). r-rows at lines 76-79; row-8 correction at 81-88 (item 3, out of scope).

Cited-source verification against committed copies:
- S182.src:1353 `static int diskstats_show(...)`; :1370-1372 `xa_for_each(&gp->part_tbl, idx, hd) {` + skip `!bdev_nr_sectors(hd)` + `continue;`; :1383 `seq_printf(seqf, " %pg", hd);`; :1391 `seq_put_decimal_ull(seqf, " ", stat.sectors[STAT_WRITE]);`; :1395 `seq_put_decimal_ull(seqf, " ", jiffies_to_msecs(stat.io_ticks));`; :1465 `disk->part0 = bdev_alloc(disk, 0);`; :1471-1472 `xa_init(&disk->part_tbl);` + `xa_insert(&disk->part_tbl, 0, disk->part0, ...)`.
- S183.src:58 `__this_cpu_add((part)->bd_stats->field, addnd)`; :61-64 `part_stat_add` wrapper adding to `bdev_whole(part)` when partition.
- S186.src:84-85 `bdev_whole(_bdev)` = `bd_disk->part0`.
- S184.src:1065-1068 `update_io_ticks` adds `now - stamp` to `io_ticks` when `end || bdev_count_inflight(part)`; :1100-1110 `bdev_end_io_acct` adds completed `sectors[sgrp]` via `part_stat_add`.
- S181.src:22-25 both files same 17 stats, procfs prefixed by major/minor/name; :33-37 cumulative except field 9, resets at boot/reattach/overflow, "should detect and handle resets"; :64-65 field 7 (after name) = sectors written; :67-68 field 8 = ms spent writing; :75-80 field 10 increases while field 9 nonzero, since 5.0 counts jiffies when ≥1 request, >2-jiffies caveat.
- S187.src:20 ABI field 11 = time spent writing (ms); S180.src:33-36 "write ticks … total wait time for write requests"; :75-80 multiple-wait grows >1000/s.
- 13r lane fact: tools/mori-census.sh:1869-1871 (label "AVERAGE SINCE BOOT … never as an instantaneous rate"), :1879-1894 (field 10 × 512 / `up_s`), :1907-1908 (uptime read). Confirmed.

Rule-by-rule hold:
- SKILL.md:816 (rows 2, 4, 13): "the since-boot average is never the current rate" ⊆ 13r verdict ("Call the census value a since-boot average only if none of those resets happened after boot, and never report it as the current write rate"). Holds. (Row 4 unchanged, supported.)
- SKILL.md:817 (row 3 + Host observation): "never both" ≡ 3r verdict ("never add a disk's line to the lines of its own partitions"); the dm-N clause stays grounded in the unchanged Host observation (entry :35-45, marked observed/unsourced). Holds.
- SKILL.md:818 (rows 5, 6, 7): "io_ticks delta … busy share, never as throughput" ⊆ 6r verdict (adds "approximate", forbids exact share; rule is weaker, not contradicted); "never present write ticks over elapsed time as a percentage" ≡ 7r verdict. Holds.

No residual contradiction: the rules were not rewritten (appendix-only), and every r-row's verdict supports the rule it anchors.

VERDICT: supported

## Residual risk / verification gaps

- The idle-device 0.0 leg rests on the tagged inference (per item 4), not on a source; if a future round wants it sourced, S190 or a sysstat doc would need a line. Not a defect this round.
- Row 8's 5.5+ flush boundary is explicitly not re-checked by the appended correction (entry :87); out of scope of items 2/4.
- I did not re-judge rows 1-14 as a whole (round-33 closure did); this report covers only the item 2/4 routing and the r-row citations the correction relies on.

Every citation above was read from the committed copies at 8d56809 in the sandbox clone; none was assumed.
