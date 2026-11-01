source: S574 (learn.microsoft.com — GlobalMemoryStatusEx function, sysinfoapi;
pinned copy `corpus/evidence/sources-r64/S574.html` sha256
d52b00df51caf4037b383dfb86691a245022be22f0dedd7f0d7040ce73e8a82a) and S575
(learn.microsoft.com — GetDiskFreeSpaceExW function, fileapi; pinned copy
`corpus/evidence/sources-r64/S575.html` sha256
0d3c8d306e76ef502fa5d9a4b646d629b8354e0ddf3ae4d464b0f3622d89caf5)
verified-at: 2026-10-31 (round 64; claims below are line-located against the
pinned copies; live receipt on this host
`.ufo/waves/round-64/evidence/runway-live-win-r64.txt`)
recheck: 180d, or when a re-fetch of either page changes its sha256 against
the pinned copies

# Reading the Windows resource-runway surface (round 64)

Scope: detection and report only, counts and shapes only. This entry grounds
`tools/mori-runway-win.py` (round-64 build): a one-shot, read-only probe of
memory commitment/physical load and volume free space through the Windows API
(standard library only — `GlobalMemoryStatusEx` and `GetDiskFreeSpaceExW`).
It is the Windows-host class of the province's Core "Resource runway" row,
whose Linux instruments (`df -P` on `$ROOT` and `/tmp`, memory PSI/fill/avail
from `/proc`) are absent on this host (PROVINCE Round-62 host note). Claims
(K1–K4 ground the memory read from S574; K5–K8 ground the disk read from
S575):

- **K1** — `S574.html:829` — "Retrieves information about the system's current usage of both physical and virtual memory.": the probe's memory line is the documented function's declared purpose, not an inferred semantics.
- **K2** — `S574.html:844-845` — "You can use the GlobalMemoryStatusEx function to determine how much memory your application can allocate without severely impacting other applications.": the allocation-runway question the probe answers with `commit_avail`/`commit_avail_pct` is the function's own stated use; the probe reports the figure and never remediates.
- **K3** — `S574.html:846-847` — "The information returned by the GlobalMemoryStatusEx function is volatile. There is no guarantee that two sequential calls to this function will return the same information.": the probe is one-shot and claims no series, rate or trend; two consecutive receipts are separate counts, never a delta.
- **K4** — `S574.html:848` — "The ullAvailPhys member of the MEMORYSTATUSEX structure at lpBuffer includes memory for all NUMA nodes.": `phys_avail` is a whole-host figure; no per-NUMA attribution is claimed (none is read).
- **K5** — `S575.html:829-831` — "Retrieves information about the amount of space that is available on a disk volume, which is the total amount of space, the total amount of free space, and the total amount of free space available to the user that is associated with the calling thread.": the three figures the disk line prints (`total_bytes`, `free_bytes`, `free_to_caller`) are the documented return fields, in the doc's own order.
- **K6** — `S575.html:854` — "If per-user quotas are being used, this value may be less than the total number of free bytes on a disk.": the platform doc states the lane's FR2 boundary itself — free percentages cannot see quota exhaustion — so the probe prints both counts and computes `free_pct` from the caller figure (the conservative one); the same caveat is repeated for the total figure at `:859`.
- **K7** — `S575.html:846-847` — "This parameter does not have to specify the root directory on a disk. The function accepts any directory on a disk.": the probe queries through the lane checkout's drive root — a documented-legal directory, not a special case.
- **K8** — `S575.html:848` — "The calling application must have FILE_LIST_DIRECTORY access rights for this directory.": an access failure is a real unavailable state; the probe grades it `unavailable` (with a reason word), never zero (honest-unavailable rule, selftest arm 5).

Reading table (local, report-only; FR8 boundary — thresholds stay labeled
local, a quiet reading is not a workload distribution):

| commit_avail_pct | free_pct | reading (report phrase) |
|---|---|---|
| ≤ 10 | any | runway-thin on commit (report, never remediate) |
| > 10 | ≤ 10 | disk-thin (report, never remediate) |
| > 10 | > 10 | runway-held (a count, not a forecast) |
| any, free_to_caller < free_bytes | — | quota gap present: the gap is visible only as the two counts (K6); df-style percentages cannot see it |

Limits (declared): the probe reads two structures once and prints them — it
never infers a cause, a trend or a time-to-exhaustion; consecutive receipts
are separate volatile counts (K3). The paging-file fields are the commit
charge/limit (documented semantics of `ullTotalPageFile`/`ullAvailPageFile`
in the MEMORYSTATUSEX structure record; this entry line-locates the function
page only, so the commit naming rests on K2's allocation question, not a
structure-page anchor). Zero counts are real counts; a failed read is
`unavailable` with a reason word, never zero (selftest arm 5). No
SetSystemFileCacheSize, no pagefile configuration, no quota change, no write
of any kind is attempted — the probe is a read of two structures. The
selftest is offline (fixtures only); the live receipt is the sole live
demonstration. Coverage-map: advances the Windows-host runway arm only; the
Linux `df`/PSI instruments remain the registered gates on Linux hosts.
