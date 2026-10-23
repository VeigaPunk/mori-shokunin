measured 2026-10-23T05:39:05Z

# JudgeRow7r — row 7r of disk-write-rate-r33.md (§Round-34 revision) at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3

## Rule (quoted word for word from the round-33 contract)

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or through a source the row does not cite.

## Judgment object

- `judged-sha256:` = ca489eb41140024e95641a53c7df0ae15f755a4e0a507b9f353bfec1b415f9f6 — sha256 of `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3:corpus/knowledge/disk-write-rate-r33.md` (run 2026-10-23).
- Row 7r (committed file line 78):

> | 7r | Field 11 of a `/proc/diskstats` line, time spent writing in milliseconds (S187.src:20) | `/proc/diskstats` and the sysfs stat file carry the same 17 statistics, the procfs line prefixed by major, minor and name (S181.src:22-25); the matching statistic is the total wait time for write requests (S181.src:67-68; S180.src:33-36), and when several requests wait at once these values grow faster than 1000 per second (S180.src:75-80) | Never present the delta of time spent writing divided by elapsed time as a percentage of time | S187, S181, S180 |

Cited committed copies: `corpus/evidence/sources-r33/S187.src`, `S181.src`, `S180.src` at 8d56809 (blobs 6a719cf2075cd60578a75b81382f366b62557330, 9453196ade51b8065563d8e76989f274098f0fe8, a1cd9db2058f94a4918112842a2441df9f3cb2fb). SOURCES.md at the same rev maps S180→Documentation/block/stat.rst v7.2, S181→Documentation/admin-guide/iostats.rst v7.2, S187→Documentation/ABI/testing/procfs-diskstats v7.2 (SOURCES.md lines 186,187,193).

## Fact-by-fact quotes (committed copies)

Observation cell:
1. "Field 11 of a `/proc/diskstats` line, time spent writing in milliseconds" — S187.src:20: `11  time spent writing (ms)` (inside the `/proc/diskstats` field table; header line 1 `What: /proc/diskstats`). STATED.
   Supporting context S187.src:19: `10  sectors written`.

Reading cell:
2. "`/proc/diskstats` and the sysfs stat file carry the same 17 statistics, the procfs line prefixed by major, minor and name" — S181.src:22-25: `Both files contain the same 17 statistics. ``/sys/block/<device>/stat`` / contains the fields for ``<device>``. In ``/proc/diskstats`` the fields / are prefixed with the major and minor device numbers and the device / name.` STATED.
3. "the matching statistic is the total wait time for write requests" — S181.src:67-68: `Field  8 -- # of milliseconds spent writing (unsigned int) / This is the total number of milliseconds spent by all writes (as / measured from blk_mq_alloc_request() to __blk_mq_end_request()).`; S180.src:36: `write ticks     milliseconds  total wait time for write requests`. STATED (S181 names field 8/ms spent writing; S180 names the same stat-file position write ticks = total wait time for write requests; S187:20 links ABI field 11 to the same statistic; S181:22 states the two files carry the same 17 statistics).
4. "when several requests wait at once these values grow faster than 1000 per second" — S180.src:78-80: `These values count the number of milliseconds that I/O requests have / waited on this block device.  If there are multiple I/O requests waiting, / these values will increase at a rate greater than 1000/second; for`. STATED.

Every fact in the observation and reading cells has a contiguous located quote in the committed copies the row cites; none is missing.

## Verdict cell

"Never present the delta of time spent writing divided by elapsed time as a percentage of time" — follows from the reading without any further fact: field 11 is a cumulative millisecond wait-time counter (S187:20; S180:36) that grows by >1000 ms per elapsed second when several requests wait concurrently (S180:79-80); its delta over elapsed time is therefore not bounded by 1 and is not a share of wall-clock time, so presenting it as a percentage of time is invalid. No extra source or fact is needed.

## Findings

- No defect found in row 7r; every read fact is quoted in the committed copies; the verdict follows from the reading.

## Residual risk / verification gaps

- Working-tree copies `corpus/evidence/sources-r33/S18{0,1,7}.src` currently have sha256 4c35b795…, 166bdc8f…, 0f2ffdc7…, which differ from the committed blobs at 8d56809 (a1cd9db…, 9453196a…, 6a719cf2…). The verdict is based on the committed copies as the rule requires; the local checkout's divergence is a repo-state observation, not a row defect. [INFERENCE] none beyond this.

VERDICT: row 7r: supported
