measured 2026-10-23T07:52:39Z

# ReJudgeRow7r — row 7r of corpus/knowledge/disk-write-rate-r33.md (§Round-34 revision) at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3

Rule (quoted word for word from the round-33 contract):

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or through a source the row does not cite.

judged-sha256: ca489eb41140024e95641a53c7df0ae15f755a4e0a507b9f353bfec1b415f9f6
(command: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3:corpus/knowledge/disk-write-rate-r33.md | sha256sum`, run 2026-10-23; identical hash measured twice.)

Judged row (committed file line 78):

| 7r | Field 11 of a `/proc/diskstats` line, time spent writing in milliseconds (S187.src:20) | `/proc/diskstats` and the sysfs stat file carry the same 17 statistics, the procfs line prefixed by major, minor and name (S181.src:22-25); the matching statistic is the total wait time for write requests (S181.src:67-68; S180.src:33-36), and when several requests wait at once these values grow faster than 1000 per second (S180.src:75-80) | Never present the delta of time spent writing divided by elapsed time as a percentage of time | S187, S181, S180 |

Committed copies opened at 8d56809: `corpus/evidence/sources-r33/S187.src` (43 lines), `S181.src` (187 lines), `S180.src` (103 lines). Blob ids at the rev (git rev-parse REV:path): S187 6a719cf2…, S181 9453196a…, S180 a1cd9db2….

## Fact-by-fact check (contiguous located quotes)

Observation cell — "Field 11 of a `/proc/diskstats` line, time spent writing in milliseconds":
- S187.src:20: ` 11  time spent writing (ms)` — inside the field table headed by :1 `What: /proc/diskstats` and :5-7 "The /proc/diskstats file displays the I/O statistics of block devices. Each line contains the following 14 fields". STATED. The single-line locator carries the number/name pair; the file identity is the document's own header. This matches the locator depth the round-33 re-judge already accepted for supported rows 1 and 5 (S187 single-line field locators), so no caveat.

Reading cell fact 1 — "`/proc/diskstats` and the sysfs stat file carry the same 17 statistics, the procfs line prefixed by major, minor and name" (S181.src:22-25):
- S181.src:22-25: `Both files contain the same 17 statistics. ``/sys/block/<device>/stat`` / contains the fields for ``<device>``. In ``/proc/diskstats`` the fields / are prefixed with the major and minor device numbers and the device / name.` — contiguous, verbatim, covers both halves of the claim. STATED. (This is exactly the identity line spotcheck §3.1 said row 7 lacked: "needs S181:22 or S182:1392".)

Reading cell fact 2 — "the matching statistic is the total wait time for write requests" (S181.src:67-68; S180.src:33-36):
- S181.src:67-68: `Field  8 -- # of milliseconds spent writing (unsigned int)` / `This is the total number of milliseconds spent by all writes (as` — the iostats numbering for the same statistic (11 − 3 prefix fields = 8). STATED.
- S180.src:33-36 contiguous: `write I/Os      requests      number of write I/Os processed` … `write ticks     milliseconds  total wait time for write requests` (:36 carries the phrase verbatim). STATED.
- The "matching" identification — ABI field 11 = iostats field 8 = stat.rst "write ticks" — is stated by the union of the three cited quotes plus the S181:22-25 equivalence; the entry header documents the two numbering conventions. No uncited line needed.

Reading cell fact 3 — "when several requests wait at once these values grow faster than 1000 per second" (S180.src:75-80):
- S180.src:75-80 contiguous: `read ticks, write ticks, discard ticks, flush ticks` (:75 heading) `These values count the number of milliseconds that I/O requests have / waited on this block device.  If there are multiple I/O requests waiting, / these values will increase at a rate greater than 1000/second;` (:78-80). "These values" includes write ticks per the :75 heading. STATED.

No fact in either cell is `missing`.

## Verdict cell

"Never present the delta of time spent writing divided by elapsed time as a percentage of time" — follows from the reading with no further fact: the field is the total wait time for write requests (a sum over requests, not a share of elapsed time), and when several requests wait at once it grows faster than 1000 ms per elapsed second, so its delta can exceed elapsed time and the quotient is not a fraction of time. This is the same reasoning the round-33 judge accepted; the only defect it found in row 7 was the uncited identity line, which 7r now cites. FOLLOWS.

## SKILL.md:816-818 check (at 8d56809)

- :816 (rows 2,4,13): no clause rests on row 7. Holds, unchanged by 7r.
- :817 (row 3 + Host observation): "total a host's writes over whole-disk lines or over partition lines but never both" — row 7r does not touch this; row 3r (its own judgment object) carries it. Holds.
- :818 (rows 5,6,7): the row-7 clause "never present write ticks over elapsed time as a percentage" is row 7r's verdict verbatim ("write ticks" is S180's name for the same statistic). 7r supplies the full citation chain (S187 field 11 ↔ iostats field 8 ↔ stat.rst write ticks) the rule previously rested on the unsupported row 7. Holds, now fully sourced.

## Audit of /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/JudgeRow7r.md

Independence: my verdict above was reached from the committed bytes before this report was opened.

1. `judged-sha256:` ca489eb4…f9f6 — agree; identical to my measurement.
2. Row 7r is committed file line 78 — agree (my extraction, line 78).
3. Blob ids S187=6a719cf2075cd60578a75b81382f366b62557330, S181=9453196ade51b8065563d8e76989f274098f0fe8, S180=a1cd9db2058f94a4918112842a2441df9f3cb2fb — agree; `git rev-parse 8d56809:corpus/evidence/sources-r33/S###.src` returns all three exactly.
4. SOURCES.md at the rev maps S180→Documentation/block/stat.rst, S181→admin-guide/iostats.rst, S187→ABI/testing/procfs-diskstats at lines 186/187/193 — agree; lines 186/187/193 verbatim, all v7.2 tag-pinned.
5. S187.src:20 quote `11  time spent writing (ms)` and header line 1 `What: /proc/diskstats` — agree; verbatim at those lines.
6. S181.src:22-25 quote — agree; verbatim and contiguous.
7. S181.src:67-68 quote — agree in substance (the cited fact, "total number of milliseconds spent by all writes", is fully on :68); minor slip: the quote they print extends onto :69 ("measured from blk_mq_alloc_request()…"), one line past the labeled range. Content verbatim.
8. S180.src:36 `write ticks … total wait time for write requests` (inside their labeled 33-36 span) — agree; verbatim.
9. S180.src:78-80 quote ending mid-sentence at `for` — agree; verbatim (the sentence continues :80-82, which does not change the stated fact).
10. "Every fact … has a contiguous located quote … none is missing" — agree; matches my fact table.
11. Verdict reasoning ("delta over elapsed time … not bounded by 1 … not a share of wall-clock time … No extra source or fact is needed") — agree; equivalent to my derivation. Their label "cumulative" for field 11 is loose wording (S181:33's cumulative-monotonic statement covers the statistic) but is not load-bearing.
12. VERDICT: row 7r: supported — agree.
13. Residual-risk claim (:41): "Working-tree copies … have sha256 4c35b795…, 166bdc8f…, 0f2ffdc7…, which differ from the committed blobs at 8d56809 (a1cd9db…, 9453196a…, 6a719cf2…)" — disagree. Measured: sha256 of the worktree file equals sha256 of the committed content for all three files (S180=4c35b795a518…, S181=166bdc8fd4ee…, S187=0f2ffdc724e0… — the same values they list). The values differ from the blob ids only because git blob ids are SHA-1s and their sha256s are content SHA-256s — different hash functions, not divergent content. The worktree copies are identical to the committed copies at this rev; the claimed divergence does not exist.

AUDIT: agree 12 / disagree 1

VERDICT: row 7r: supported
