measured 2026-10-23T05:39:11Z
# JudgeRow6r — round-34 wave A, row 6r of disk-write-rate-r33.md (§Round-34 revision)

Judge rule (quoted word for word from the round-33 contract, `.ufo/waves/round-33/contract.md:47-50`):

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its
> observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row
> any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or
> through a source the row does not cite.

judged-sha256: ca489eb41140024e95641a53c7df0ae15f755a4e0a507b9f353bfec1b415f9f6
(sha256 of `git show 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3:corpus/knowledge/disk-write-rate-r33.md`; the file also matches at its own `## Round-34 revision` section, entry lines 74-79)

## Scope

Row 6r (entry line 77, `## Round-34 revision` table): observation "The `io_ticks` value printed in `/proc/diskstats`"; reading cell as judged below; verdict "Report the `io_ticks` delta over elapsed milliseconds only as an approximate busy share of the window, never as an exact share and never as throughput"; sources S184, S182, S181. This row is the append-only repair of original row 6, routed by `corpus/lessons/round-33-verifier-spotcheck.md` §3.1 (row 6 unsupported: "'approximate' needs S181:78-80, which is not cited") and §8 item 2 ("Cite … S181:78-80 … in a new append-only revision"). Committed copies read at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 via `git show` into scratch. No tool installed or updated (no installs this seat).

## Fact-by-fact located quotes (committed copies)

Observation cell — "The `io_ticks` value printed in `/proc/diskstats`":
- S182.src:1353 `static int diskstats_show(struct seq_file *seqf, void *v)`; S182.src:1395 `seq_put_decimal_ull(seqf, " ", jiffies_to_msecs(stat.io_ticks));`; S182.src:1423-1426:
  ```
  1423:static int __init proc_genhd_init(void)
  1425:	proc_create_seq("diskstats", 0, NULL, &diskstats_op);
  1426:	proc_create_seq("partitions", 0, NULL, &partitions_op);
  ```
  (`seq_operations diskstats_op` at S182.src:1416-1421 binds `.show = diskstats_show`.) States that `/proc/diskstats` is a proc file whose show function prints `io_ticks` via `jiffies_to_msecs`.

Reading cell fact 1 — "When `now` is later than `stamp` and either the I/O is ending or `bdev_count_inflight(part)` is nonzero, the kernel adds `now - stamp` to `io_ticks`" (S184.src:1065-1068, with `update_io_ticks(struct block_device *part, unsigned long now, bool end)` at S184.src:1060):
  ```
  1065:	if (unlikely(time_after(now, stamp)) &&
  1066:	    likely(try_cmpxchg(&part->bd_stamp, &stamp, now)) &&
  1067:	    (end || bdev_count_inflight(part)))
  1068:		__part_stat_add(part, io_ticks, now - stamp);
  ```

Reading cell fact 2 — "`diskstats_show` prints it through `jiffies_to_msecs`" (S182.src:1353,1395): quotes as in observation cell; `jiffies_to_msecs(stat.io_ticks)` printed to the seq file.

Reading cell fact 3 — "The field is milliseconds spent doing I/Os and grows while field 9 is nonzero" (S181.src:75-76):
  ```
  75:Field 10 -- # of milliseconds spent doing I/Os (unsigned int)
  76:    This field increases so long as field 9 is nonzero.
  ```

Reading cell fact 4 — "since 5.0 it counts jiffies when at least one request was started or completed" (S181.src:78-80):
  ```
  78:    Since 5.0 this field counts jiffies when at least one request was
  79:    started or completed. If request runs more than 2 jiffies then some
  80:    I/O time might be not accounted in case of concurrent requests.
  ```

Reading cell fact 5 — "a request running more than 2 jiffies may leave some I/O time unaccounted when requests are concurrent" (S181.src:78-80): same quote as fact 4 (lines 79-80).

No `missing` facts. All facts in the observation and reading cells are stated by contiguous quotes (>6 words where the line allows) in the committed copies of the sources the row cites (S184, S182, S181), at the locators the row gives.

Field-numbering check: S181 (iostats.rst) numbers statistics from 1 after the name (entry lines 9-11), so S181 field 10 = io_ticks and S181 field 9 = running/inflight; the reading cell uses S181 numbering consistently with the quoted lines.

## Does the verdict follow without any further fact?

The verdict: "Report the `io_ticks` delta over elapsed milliseconds only as an approximate busy share of the window, never as an exact share and never as throughput." The reading states the field is milliseconds spent doing I/Os that grows while field 9 is nonzero (a time measure → a share of an elapsed window is a busy share, and time/time is not throughput), and that since 5.0 it counts jiffies and can under-account I/O time under concurrent requests running >2 jiffies (→ approximate, therefore never exact). The verdict is arithmetic inference over those stated facts; no further fact (no new source) is required. Rows 1-14 repair precedent (spot-check §3.1) confirms the only defect in original row 6 was the uncited S181:78-80, now cited verbatim.

## Residual risk / verification gaps

- The `end` flag in `update_io_ticks` (S184.src:1060) is read as "the I/O is ending"; that mapping is from the call sites in the same file (S184), not quoted in the row — accepted because the quote itself covers the `end || bdev_count_inflight(part)` condition. [INFERENCE only for the label, not for the stated condition.]
- S181 field numbering (1 after the name) is asserted by the entry's own preamble (lines 9-11), not by a quote; read the row's cell it is used consistently. The row's facts are still each stated by its quotes.
- The row cites S184, S182, S181 only; I verified those copies at the judged revision. Gate sha256 equality of the copies is C1-predicate machinery, out of scope for this R-J seat.

VERDICT: row 6r: supported
