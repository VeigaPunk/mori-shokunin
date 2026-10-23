measured 2026-10-23T07:43:36Z
# ReJudgeRow6r — round-34 wave B, row 6r of corpus/knowledge/disk-write-rate-r33.md (§Round-34 revision)

Judge rule (quoted word for word from the round-33 contract, `.ufo/waves/round-33/contract.md:47-50`):

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its
> observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row
> any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or
> through a source the row does not cite.

judged-sha256: ca489eb41140024e95641a53c7df0ae15f755a4e0a507b9f353bfec1b415f9f6
(sha256 of `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3:corpus/knowledge/disk-write-rate-r33.md`)

## Scope

Row 6r (entry line 77 of the committed file): observation "The `io_ticks` value printed in `/proc/diskstats`"; sources
cell `S184, S182, S181`. All source bytes read at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 via `git show` (committed
copies `corpus/evidence/sources-r33/S181.src`, `S182.src`, `S184.src`; each `git cat-file -e` exists at the revision).

## Fact-by-fact located quotes

Observation — "The `io_ticks` value printed in `/proc/diskstats`":
- S182.src:1353 `static int diskstats_show(struct seq_file *seqf, void *v)`; S182.src:1395
  `seq_put_decimal_ull(seqf, " ", jiffies_to_msecs(stat.io_ticks));`; S182.src:1416-1425 binds `.show = diskstats_show`
  (`diskstats_op`, :1420) and `proc_create_seq("diskstats", 0, NULL, &diskstats_op)` (:1425). Stated.

Reading fact 1 — "When `now` is later than `stamp` and either the I/O is ending or `bdev_count_inflight(part)` is
nonzero, the kernel adds `now - stamp` to `io_ticks`" — S184.src:1065-1068 (signature `update_io_ticks(struct
block_device *part, unsigned long now, bool end)` at :1060):
```
1065:	if (unlikely(time_after(now, stamp)) &&
1066:	    likely(try_cmpxchg(&part->bd_stamp, &stamp, now)) &&
1067:	    (end || bdev_count_inflight(part)))
1068:		__part_stat_add(part, io_ticks, now - stamp);
```
Stated; the quote carries one further conjunct (`try_cmpxchg` success) that the cell omits — an elided implementation
condition, not an unstated contrary fact. The `end`→"the I/O is ending" label is read from the same file's call sites
(S184.src:1080,1108 call with `false`/`true`); [INFERENCE] for the English label only, the quoted condition stands.

Reading fact 2 — "`diskstats_show` prints it through `jiffies_to_msecs`" — S182.src:1353,1395 (quotes above). Stated.

Reading fact 3 — "The field is milliseconds spent doing I/Os and grows while field 9 is nonzero" — S181.src:75-76:
```
75:Field 10 -- # of milliseconds spent doing I/Os (unsigned int)
76:    This field increases so long as field 9 is nonzero.
```
Stated. The bridge (printed `io_ticks` = S181 field 10) is itself supported inside cited copies: S182.src:1384-1395
prints nine statistics before `io_ticks` (ios/merges/sectors/nsecs→ms for read, same for write, then `inflight`), and
S181.src:22-25 says `/proc/diskstats` carries the same 17 statistics prefixed by major, minor and name — so the tenth
statistic is field 10, "milliseconds spent doing I/Os". No uncited source needed.

Reading fact 4 — "since 5.0 it counts jiffies when at least one request was started or completed" — S181.src:78-79:
```
78:    Since 5.0 this field counts jiffies when at least one request was
79:    started or completed. If request runs more than 2 jiffies then some
```
Stated.

Reading fact 5 — "a request running more than 2 jiffies may leave some I/O time unaccounted when requests are
concurrent" — S181.src:79-80:
```
79:    started or completed. If request runs more than 2 jiffies then some
80:    I/O time might be not accounted in case of concurrent requests.
```
Stated.

No `missing` facts.

## Verdict cell — does it follow with no further fact?

Verdict: "Report the `io_ticks` delta over elapsed milliseconds only as an approximate busy share of the window, never
as an exact share and never as throughput." From the reading alone: the field is a time measure that grows while I/Os
are in progress → its delta over elapsed ms is a busy-share-of-window quantity and is not throughput (it carries no
byte/sector dimension); it is accumulated in whole jiffies and can under-account concurrent requests running >2
jiffies → "approximate", hence never "exact". Both qualifications are arithmetic consequences of stated facts; no
further fact or source required. Follows.

## SKILL.md:816-818 under 6r

- :816 (rows 2, 4, 13 → 13r): unaffected by 6r; 13r still supplies the since-boot-average clause. Holds.
- :817 (row 3 → 3r): unaffected by 6r. Holds.
- :818 (rows 5, 6, 7 → 6r for the io_ticks clause): "report the io_ticks delta over elapsed time as busy share, never
  as throughput" — 6r supports this and tightens it to "approximate busy share … never as an exact share". Not a
  contradiction; the rule holds and the row permits a stricter reading.

## Audit of /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/JudgeRow6r.md

Factual claims the round would cite (marked agree/disagree against the committed bytes):

1. Rule quote attributed to `.ufo/waves/round-33/contract.md:47-50` — agree; the quoted text matches verbatim (the
   quote itself sits at :46-49 of the committed contract; the :47-50 range still covers it).
2. `judged-sha256: ca489eb4…f9f6` — agree; my own `git show … | sha256sum` gives the identical value.
3. Row 6r is at entry line 77 with the observation/verdict/sources it restates — agree (file line 77, verified).
4. Row 6r is the append-only repair of row 6 routed by spot-check §3.1 and §8 item 2 — agree;
   `corpus/lessons/round-33-verifier-spotcheck.md:93-95` lists rows 3,6,7,13 unsupported with row 6 = "'approximate'
   needs S181:78-80, which is not cited", and :229-230 (§8 item 2) orders citing S181:78-80 in an append-only revision.
5. Observation support via S182.src:1353,1395 plus proc registration at S182.src:1416-1426 with `.show =
   diskstats_show` — agree; quoted lines verified (diskstats_op at :1416-1421, proc_create_seq at :1425).
6. Reading fact 1 quote S184.src:1065-1068 with signature at :1060 — agree, byte-for-byte.
7. Reading fact 3 quote S181.src:75-76 — agree, byte-for-byte.
8. Reading facts 4-5 quote S181.src:78-80 — agree, byte-for-byte.
9. "No missing facts; all facts stated at the locators the row gives" — agree, with the nuance that the printed
   io_ticks = field-10 bridge also rests on S182.src:1384-1394 ordering (same cited source); the report's field-
   numbering note reaches the same conclusion via the entry preamble.
10. Verdict follows without further fact — agree, same reasoning as my §Verdict cell above.
11. Residual-risk item 1 (the `end`-flag English label is same-file inference, not quoted) — agree.
12. Residual-risk item 2 (S181 numbering from preamble lines 9-14 rather than a quote) — agree as far as it goes; the
    committed copies also contain the stronger 17-statistics statement at S181.src:22-25, so the inference is
    conservative, not wrong.
13. "Committed copies read at 8d56809…" — unverifiable process claim, but consistent with the bytes being the
    committed copies; treated as [INFERENCE], no disagreement.
14. No tool installed or updated this seat — consistent with its report; I likewise installed nothing (all reads via
    git/awk/grep; pacman untouched per pause).

AUDIT: agree 12 / disagree 0 (two claims noted as unverifiable-or-conservative rather than disagreed)

VERDICT: row 6r: supported
