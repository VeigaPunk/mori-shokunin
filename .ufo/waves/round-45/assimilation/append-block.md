<!-- round-45 append block — drafted by ExecAssimCensus 2026-10-25, NOT appended by this seat.
     Lane: mori. Target: corpus/SOURCES.md, ## Registry table, after row S472.
     Allocation: renumber-map.tsv in this directory (lane max S472; S473 reserved to this row;
     staged S471..S606 -> S474..S609).
     Scope of this block: ONLY the rows the round-45 admitted entry cites — the kernel cgroup-v2
     rst this round opened. The staged 136-row block is the L1's to integrate, not this seat's.
     Source of the row: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/opened/cgroup-v2.rst.src
       URL    https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst
       sha256 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad  (3524 lines, fetched 2026-10-25)
     Recheck (kept OUT of the recheck cell: census E09 accepts only an ISO date / NNd / symbolic cadence):
       curl -fsSL --max-time 40 https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst | sha256sum
     Normalization applied (census schema): 11 columns; no literal or escaped pipe in any cell;
     recheck = 180d; opened = 2026-10-25; status = mined; used-by names the admitted entry only.
     Substance narrowed on purpose: the events-vs-events.local split is ALREADY held at lane S002
     (same document, docs.kernel.org HTML). This row claims only what S002 does not — that the
     aggregation scope belongs to the FILE, and that memory.peak aggregates the subtree while
     memory.events.local does not. Reported to the L1 rather than appended as a duplicate teaching.
-->
| S473 | Control Group v2 — the aggregation scope of the memory interface, kernel v7.2 (rst) — https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst | docs | A | the aggregation scope of three cgroup v2 memory files only as the v7.2 rst states it — memory.events hierarchical, memory.events.local not hierarchical, memory.peak covering the cgroup and its descendants; the events-versus-local split itself stays S002's and is not re-claimed here; not this host's readings, not cgroup v1, not systemd resource-control man pages, not the docs.kernel.org HTML rendering | cgroup-v2.rst:1468 memory.events and :1474-1477 "all fields in this file are hierarchical ... due to an event down the hierarchy"; :1517-1520 memory.events.local "local to the cgroup i.e. not hierarchical"; :1440-1444 memory.peak "the cgroup and its descendants"; tag v7.2, fetched 2026-10-25, sha256 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad | Counter scope is a property of the file, not of the reader: memory.events counts an event anywhere down the hierarchy while memory.events.local counts this cgroup only, and memory.peak is the subtree high-water mark — so a row that pairs counters from two levels is comparing different scopes unless it names the file each counter came from | mined | 2026-10-25 | 180d | corpus/knowledge/census-cgroup-levels-r45.md |
