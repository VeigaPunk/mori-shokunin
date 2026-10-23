measured 2026-10-23T07:55:21Z

# ReJudgeSkillCorr — round-34 wave B: the SKILL.md Round33-correction paragraph at 8d56809

Object: `Round34 correction to the Round33 section above` (SKILL.md:836-842 at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3),
judged against routed defects round-33-verifier-spotcheck.md §8 item 2 (:228-230) and item 4 (:233-234). Independence:
all verdicts below were formed from the bytes at 8d56809 and the committed source copies before
`.ufo/waves/round-34/wa/JudgeSkillCorrection.md` was opened; the audit section came second.

Method: blobs read via `git show <rev>:<path>` into scratch extracts (read-only git only); every cited source line was
opened in the committed copies `corpus/evidence/sources-r33/S###.src` at 8d56809. No tools installed (none needed);
no git/jj writes anywhere.

## VERDICT 1 — iostat clause (SKILL.md:820) aligned with entry row 14 and S190, no new overclaim (§8 item 4)

VERDICT: supported

- SKILL.md:820 (identical at f10a320d and 8d56809; diff adds only) lumps "an iostat 0.0" into "unavailable or
  unknown, never a zero write rate". Row 14 (disk-write-rate-r33.md:33) says less: "Do not read a zero write-sector
  value in iostat's extended statistics as an unchanged counter without the raw counters" (S190).
- The appended paragraph (SKILL.md:836-842) narrows exactly that clause. Mechanism claim verified at
  S190.src:1516-1517: `xios.wsectors = ioi->wr_sectors < ioj->wr_sectors ? 0.0 : S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);`
  with ioi/ioj named current/previous in the write_ext_stat comment (S190.src:1452-1461), inside the row's cited
  locator 1444-1464,1516-1517 (SOURCES.md:196). So "iostat prints 0.0 when the newer sectors-written count is below
  the older one" is source-backed, and "read the raw counters before reading that 0.0 as anything" restates row 14's
  verdict.
- "An idle device also shows 0.0" is labeled `[INFERENCE, closure §8 item 4]`, mirroring the spotcheck's own
  `[INFERENCE, ConformancePromptHarm]` tag (spotcheck:233-234). The inference is sound (equal counters make the
  ternary's S_VALUE branch print 0.0) and, being labeled, is not an overclaim.
- "0.0 alone is neither a zero rate nor an unavailable one" retracts 820's unsupported "unavailable" half for the
  iostat case without asserting anything row 14 does not license. The only residual is that line 820's bytes are
  unchanged and must be read together with the appended gloss — inherent to the lane's append-only correction
  convention (same pattern as the entry's Row 8 correction at disk-write-rate-r33.md:81-88). Not a defect.

## VERDICT 2 — Round33 rules SKILL.md:816-818 hold under rows 3r, 6r, 7r, 13r (§8 item 2)

VERDICT: supported

Rule→row map: :816 cites rows 2, 4, 13 (→13r); :817 cites row 3 + Host observation (→3r); :818 cites rows 5, 6, 7
(→6r, 7r). Item 2 demands "Cite S182:1370,1472, S181:78-80, S181:22, or narrow the cells, in a new append-only
revision"; the entry's `## Round-34 revision` (disk-write-rate-r33.md:65-79) is that revision, and every citation it
makes was opened in the committed copies at 8d56809:

- 3r (:76): S182.src:1370-1372 `xa_for_each(&gp->part_tbl…)` + zero-size-partition skip; :1383 `%pg` name print;
  :1391 `stat.sectors[STAT_WRITE]` print; :1465 `disk->part0 = bdev_alloc(disk, 0)`; :1471-1472 `xa_init` +
  `xa_insert(&disk->part_tbl, 0, disk->part0, …)`; S183.src:58,61-64 `part_stat_add` mirrors to `bdev_whole(part)`;
  S186.src:84-85 `bdev_whole = bd_disk->part0`; S184.src:1100-1110 `bdev_end_io_acct` → `part_stat_add(sectors…)`.
  Demanded S182:1370 and S182:1472 are both cited. Verdict cell is materially row 3's, so SKILL.md:817 holds; the
  dm-N clause stays flagged "observed, unsourced" in the rule itself, so no overclaim.
- 6r (:77): S184.src:1065-1068 `time_after(now,stamp) && … (end || bdev_count_inflight(part))` → add `now - stamp`
  to io_ticks; S182.src:1353 (`diskstats_show` signature) and :1395 (`jiffies_to_msecs(stat.io_ticks)` print);
  S181.src:75-76 ("increases so long as field 9 is nonzero") and :78-80 (5.0 jiffies/concurrency caveat). Demanded
  S181:78-80 cited. 6r's verdict adds "approximate … never an exact share" and forbids throughput — SKILL.md:818's
  io_ticks clause ("busy share, never as throughput") is the weaker claim and holds.
- 7r (:78): S187.src:20 ("11 time spent writing (ms)"); S181.src:22-25 (same 17 statistics, procfs prefixed by
  major/minor/name); S181.src:67-68 (total ms spent by all writes); S180.src:33-36 (write ticks = total wait time
  for write requests); S180.src:75-80 (>1000/s under concurrent waits). Demanded S181:22 cited. Verdict identical to
  row 7, so SKILL.md:818's write-ticks clause holds.
- 13r (:79): S181.src:33-37 (cumulative except field 9; resets at boot, reattachment/reinitialisation, overflow;
  "detect and handle resets"), :64-65 (sectors written = total); lane fact verified in tools/mori-census.sh at
  8d56809: :1869 "AVERAGE SINCE BOOT — reported with that name and never as an instantaneous rate", :1887-1894
  (field 10 × 512 / `up_s`), :1907-1908 (uptime read). SKILL.md:816's "the since-boot average is never the current
  rate" holds; 13r keeps "never report it as the current write rate".
- "which cite every source they need": every cited range in the four r-rows carries the claimed content; none was
  missing or off-target.

## VERDICT 3 — append-only (f10a320d → 8d56809, SKILL.md)

VERDICT: supported

`git diff --numstat f10a320d 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 -- SKILL.md` → `18	0`; the only `-` line in the
patch is the `--- a/SKILL.md` header; the hunks show 3 context lines and 18 additions = exactly the Round34 section
(SKILL.md:825-834) plus the correction paragraph (SKILL.md:836-842). No deleted line.

## Audit of .ufo/waves/round-34/wa/JudgeSkillCorrection.md

Opened only after the three verdicts above were recorded in scratch. Claims the round would cite, each checked
against the bytes at 8d56809:

| # | wa claim | verdict |
|---|---|---|
| 1 | Correction paragraph is SKILL.md:836-842 at 8d56809 | agree (numbered dump) |
| 2 | §8 item 2 = spotcheck:228-230; item 4 = :233-234 | agree |
| 3 | Old clause SKILL.md:820 "unavailable or unknown, never a zero write rate" | agree |
| 4 | Row 14 at disk-write-rate-r33.md:33, verdict as quoted | agree |
| 5 | S190 mechanism: S190.src:1516-1517 `xios.wsectors` ternary; SOURCES.md:196 locator 1444-1464,1516-1517 | agree |
| 6 | Knowledge revision append-only: `git diff --numstat ba525e1 8d56809` = 25 insertions, 0 deletions | agree (reproduced: `25	0`) |
| 7 | Revision section :65-88; r-rows at :76-79; Row 8 correction at :81-88; rows 1-14 untouched | agree |
| 8 | S182.src:1353,1370-1372,1383,1391,1395,1465,1471-1472 (1471 `xa_init`, 1472 `xa_insert`) | agree |
| 9 | S183.src:58,61-64; S186.src:84-85 | agree |
| 10 | S184.src:1065-1068 (end‖inflight), :1100-1110 (bdev_end_io_acct) | agree |
| 11 | S181.src:22-25,33-37,64-65,67-68,75-76,78-80 | agree |
| 12 | S187.src:20; S180.src:33-36,75-80 | agree |
| 13 | 13r lane fact: mori-census.sh:1869-1871,1879-1894,1907-1908 | agree |
| 14 | Host observation grounded at entry :35-45, marked observed/unsourced | agree |
| 15 | Rule holds: :816 ⊆ 13r verdict | agree |
| 16 | Rule holds: :817 ≡ 3r verdict | agree |
| 17 | Rule holds: :818 io_ticks ⊆ 6r ("approximate" is stronger than the rule; not contradicted); write-ticks ≡ 7r | agree |
| 18 | "the old overclaim … is gone" | agree, with note: line 820's bytes are unchanged; the overclaim loses force through the appended narrowing (append-only convention), which the wa report itself describes correctly as "narrows the clause" |
| 19 | Row 8's 5.5+ flush boundary explicitly not re-checked (entry :87) | agree |
| 20 | Wa's residual: idle-0.0 leg rests on the tagged inference, not a source | agree |

Procedural context (seat, sandbox-clone path, "lane tip when dispatched") was not counted: not a byte-level claim
this round cites. Wa's two VERDICT lines (Q1 supported, Q2 supported) match my independent verdicts.

AUDIT: agree 20 / disagree 0

## Residual risk and verification gaps

- Alignment of SKILL.md:820 is by appended gloss; a reader of :820 alone still sees "unavailable". Inherent to
  append-only; if the lane ever rewrites, drop the "unavailable" half there.
- The idle-device 0.0 leg remains inference (labeled as such in both SKILL.md:841 and spotcheck:233-234); S190 or a
  sysstat document would have to supply a line to source it.
- I verified the r-rows' citations and the rules that rest on them; I did not re-judge the whole entry rows 1-14
  (round-33 closure's object, outside this item's scope), nor the Row 8 correction (§8 item 3, out of scope).
- fd2521351c6cef47384aef30afbe1e4db7e6912e (wave tip) was not judged here; the assignment pins 8d56809.
