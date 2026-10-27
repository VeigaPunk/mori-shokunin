# Mo54ScribeReadme — corpus/README.md round-54 additions (draft)

Lane: mori-shokunin. Seat: scribe (leaf). Contract: `.ufo/waves/round-54/contract.md` (frozen at `6830f3af`); C1 data
at `78295c76` (`1116c092` data commit, `78295c76` correction commit). Task: draft, fenced, a
`## Round-54 coverage additions` block in the house shape of the round-53 block, plus a dated frontier note.

Status: draft complete, verified against the data commit's artifacts and the live host reads below. Nothing in the
lane was written except this report.

## What I read (command → outcome → rc)

| command (cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`) | outcome | rc |
|---|---|---|
| `read corpus/README.md` (785 lines) | round-53 block at `:750-769`; `## Frontier` table at `:337-355`; an uncommitted round-54 block at `:771-785` | 0 |
| `git log --oneline -6` | tip `2d0347a3` (wave spec), data at `78295c76`, `1116c092`, freeze `6830f3af`, entering `39dcf4d7` | 0 |
| `git diff --stat 78295c76` | `corpus/README.md` **+16**, `SKILL.md` +38, `PROVINCE.md` +20, `SCORECARD.md` +15, `corpus/QUALITY.md` +41, plus the wave spec/dispatch/receipt files — all uncommitted relative to the data commit | 0 |
| `stat -c '%y %n' corpus/README.md` | `2026-10-27 01:42:11.723946492 -0300` | 0 |
| `read .ufo/waves/round-54/evidence/c1-at-data.txt` | `C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 rev=78295c764093ff1f6cee08d7246679900bde7265 failed=votes` | `exit=1` |
| `read .ufo/waves/round-54/evidence/c2-at-data.txt` | `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=78295c764093ff1f6cee08d7246679900bde7265 failed=entailment` | `exit=1` |
| `grep` count of 12-hex ledger rows in `corpus/knowledge/kernel-v7.3-recheck-r54.md` | 62 = 31 ledger rows (`:23-53`) + 31 moved rows (`:69-99`) | 0 |
| `wc -l .ufo/waves/round-54/evidence/c1-scope.txt`; entry split | 33 lines; `commit-runway-read-r53.md` 8, `oom-memcg-stat-r50.md` 22, `quota-observability-r48.md` 1 | 0 |
| `grep` count of claim rows (S5xx source column) in `corpus/knowledge/memory-failure-kills-r54.md` | 21 claim rows (`:24-44`) | 0 |
| `grep -rln 'memory_failure\|hwpoison\|HardwareCorrupted' tools/` | no file (no tool reads these surfaces) | 1 |
| host reads (see "Host surfaces" below) | counters 0, `HardwareCorrupted: 0 kB`, recovery 1, early-kill 0, panic sysctl absent | 0 |
| `grep -n` on `corpus/evidence/sources-r54/cgroup-v2.7.3.html` | `memory.pressure` read-write `:1719`, `io.pressure` read-write `:2012`, `delay_nsec` nanoseconds `:2117-2118`, `cpu.stat` non-hierarchical `:1103` | 0 |

## State of the target file (read this before applying the draft)

`corpus/README.md` at the data commit `78295c76` has **no** round-54 block. The working tree at read time already
carries one (`:771-785`, +16 lines vs the data commit, mtime `2026-10-27 01:42:11 -0300`), together with uncommitted
edits to `SKILL.md`, `PROVINCE.md`, `SCORECARD.md` and `corpus/QUALITY.md`. I did not write any of those and cannot
attribute them from git (uncommitted; no author on a working-tree change).

Consequence for integration: the block below is a **replacement** for `corpus/README.md:771-785`, not an append.
Appending it verbatim would leave two `## Round-54 coverage additions` headings. Relocating/removing the existing
block is the L1's call; I only read it.

## Draft (fenced)

```markdown
## Round-54 coverage additions

| Ground | Entry | Bounded advance |
|---|---|---|
| Kill and OOM events — hardware memory-failure kills, a kill class outside the OOM path (new ground, knowledge only) | `knowledge/memory-failure-kills-r54.md` (S521–S524; S502, S507 reused) | 21 claim rows over six v7.3 copies: the `Memory failure:` prefix every handler line carries; the send lines — SIGBUS with `BUS_MCEERR_AR` forced for the task that touched the page, the ordinary catchable path for other mappers, SIGKILL when the unmap failed, and a separate line when the signal could not be delivered; the one-line recovery action with its four outcomes; the per-node `memory_failure/{total,ignored,failed,delayed,recovered}` counters; `HardwareCorrupted`; `memory_failure_recovery` and `memory_failure_early_kill` plus v7.3's `panic_on_unrecoverable_memory_failure`; and `ras:memory_failure_event` under `ras`, not `oom`. The decision table separates a handler kill from an OOM kill (no `memory.events oom_kill` movement, no `oom-kill:` line) and counts by the structured surfaces, using the kernel lines for attribution only. `python3 .ufo/waves/round-54/count-c2.py 78295c76…` → `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 … failed=entailment`, exit 1 (`.ufo/waves/round-54/evidence/c2-at-data.txt`); the vote arm is the twelve ENTAILMENT voters', and the landed reading is the round-54 report's. Bounded: a located quote proves the words exist in the copy, not that the row means what they say — the votes carry that; nothing was observed firing (this host's node counters and `HardwareCorrupted` read 0 on 7.2.11, and the v7.3 panic sysctl is absent there), so every kill line and counter is read from source; no tool reads these surfaces yet; and the entry is detection knowledge only — mori never injects poison and never writes a memory-failure sysctl. |
| Freshness — the remaining v7.2-pinned claim rows rechecked at tag v7.3 | `knowledge/kernel-v7.3-recheck-r54.md` (S515–S520; S508, S514 reused) | The counter's `--scope` at the entering tip `39dcf4d7` listed every remaining claim row that pins Linux tag v7.2 — 31 rows across `oom-memcg-stat-r50.md` (22), `commit-runway-read-r53.md` (8) and `quota-observability-r48.md` (1) — and the ledger carries all 31, one row per claim hash with the counter's derived status, a v7.3 source row, the v7.3 line on which the quote begins, and a disposition (`holds`, pending the votes). All 31 quotes occur in the v7.3 copies: four of the eight files are byte-unchanged, `mm/util.c` changed outside the quoted lines, and the moved lines sit at +4 (`mm_init.c`), +31 (rendered cgroup-v2 7.3.0), +45 and +84 (`memcontrol.c`). `python3 .ufo/waves/round-54/count-c1.py 78295c76…` → `C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 … failed=votes`, exit 1 (`.ufo/waves/round-54/evidence/c1-at-data.txt`); the vote arm is the twelve RECHECK voters', and the landed reading is the round-54 report's. Bounded: `held` proves the words still occur somewhere in the copy and `line` where they begin, not that the code around them means the same — the disposition and its two votes carry that; the `file:line` anchors the two older entries give in prose are v7.2 positions and are not rewritten (`memcontrol.c:1774-1830`, …); `oom-tracepoints-r47.md` (its pin is `on-release`, and the v7.3 tag fires it) and `system-pressure-r24.md`'s anchors are not claim tables and stay outside the scope; the pins prove the bytes are what the L1 fetched from cgit, not that cgit served the tag. |

Dated note (append-only, 2026-10-27): the round-53 note's lead "`panic_on_unrecoverable_memory_failure` … `mm/memory-failure.c`
at v7.3 was not opened" is answered by `knowledge/memory-failure-kills-r54.md`; its "unrechecked at v7.3" list loses
`oom-memcg-stat-r50.md` (the ledger reads its claim table) and keeps `oom-tracepoints-r47.md` (a catalogue, not a
claim table) together with the prose outside the three tables and the `file:line` anchors those entries give, which are
v7.2 positions and are not rewritten. No frontier row is rewritten: the class lands as knowledge only — no census arm,
no tool, no live event — so a memory-failure death stays unobservable to the census (FR1's attribution question and
FR13's eBPF boundary are untouched), and the three entries keep their own `source:` pins and `recheck:` clocks
(`oom-memcg-stat-r50.md` 90d, `quota-observability-r48.md` 180d), which the ledger is not a re-pin of. New leads, not
held: the rendered cgroup-v2 7.3.0 page renames the `io.stat` throttle field `delay` → `delay_nsec` (microseconds →
nanoseconds; committed copy lines 2117-2118), so an io observer keyed on the old name or unit reads wrong, and
documents `memory.pressure`/`io.pressure` as read-write where 7.2 said read-only (copy lines 1719, 2012 — the files
always accepted PSI trigger writes, round-24 F8), with the `cpu.stat` CFS bandwidth stats now documented
non-hierarchical (copy line 1103); `block/blk-iolatency.c` and `kernel/sched/` at v7.3 are not opened
(`corpus/SOURCES.md` `## Leads (unopened)`, round-54 bullet); and the surfaces before `memory_failure()` runs — MCE
decoding, EDAC, `rasdaemon` — are hardware-health ground the lane does not hold, so a corrected-error reading is not a
kill.
```

## What the draft changes against the block already in the working tree

The uncommitted block at `corpus/README.md:771-785` is factually consistent with the artifacts on the points it
states; the draft differs in five ways, each tied to a source:

1. Adds the two counter readings at the data commit, with receipt paths and revision — the round-53 house shape
   carries the measurement, and without it the map row is a claim about a ledger rather than a measured scope
   (`c1-at-data.txt`, `c2-at-data.txt`; contract "Target after").
2. States the C1 `--scope` and its split (31 = 22 + 8 + 1) instead of the lane-wide negative "no claim-table row of
   the lane pins v7.2 unrechecked", which the counter does not establish beyond the three entries' tables
   (`evidence/c1-scope.txt`).
3. Names the entry `source:`/`recheck:` headers as unchanged, so the table row is not read as a re-pin of the three
   entries (`oom-memcg-stat-r50.md:1-7` `recheck: 90d`; `quota-observability-r48.md:7-8` `recheck: 180d`).
4. Gives the release-drift leads their copy lines, so each is checkable in the committed page rather than by trust
   (`cgroup-v2.7.3.html:1103,1719,2012,2117-2118`).
5. Adds the bounded lists (what `held`/`line` do not prove; which entries' anchors stay v7.2; which sources are out of
   scope) and keeps the `HardwareCorrupted`/counter host reading in the row rather than only in the entry
   (`memory-failure-kills-r54.md:69-73`).

It also drops the round-53 note's `## Release drift` citation to `kernel-v7.3-recheck-r54.md` only where the SOURCES
lead already names the same three items (`corpus/SOURCES.md:365`), so the note and the lead cannot drift apart.

## Verification of the draft's factual claims

- Ledger row count: 31 (`grep` count above; `:23-53`), matching `scope=31`, `rows=31`.
- Entry row count: 21 (`:24-44`), matching `claims=21`, `located=21`; sources 6 = S521–S524 + S502 + S507.
- SOURCES rows S515–S520 at `corpus/SOURCES.md:294-299`, S521–S524 at `:300-303`; S508 `:287`, S514 `:293`;
  used-by cells of S502 `:281` and S507 `:286` name `memory-failure-kills-r54.md`; S508/S514 name
  `kernel-v7.3-recheck-r54.md`; leads at `:363-365`.
- Host surfaces (read-only, `uname -r` = `7.2.11-arch1-1`):
  `/proc/meminfo:40 HardwareCorrupted: 0 kB`; `/sys/devices/system/node/node0/memory_failure/{delayed,failed,ignored,recovered,total}=0`;
  `/proc/sys/vm/memory_failure_recovery=1`, `memory_failure_early_kill=0`, `enable_soft_offline=1`,
  `panic_on_unrecoverable_memory_failure` ABSENT. This is the only node on this host; no second node directory exists.
- Release drift: all three leads located verbatim in the committed v7.3 page copy (lines above).
- No tool names the class: `grep -rln` over `tools/` returned no file (rc 1). `SKILL.md:1217-1239` and
  `PROVINCE.md:463-469` do name it, but only as uncommitted working-tree edits (+38, +20 vs `78295c76`), so the
  draft's "no tool reads these surfaces yet" is the claim that survives.

## Not verified / out of scope for this seat

- I did not re-fetch the v7.3 bytes; the pins arm is the counter's, and wave seats re-fetch independently (contract
  "Named limits").
- I did not read the twelve RECHECK or twelve ENTAILMENT voter files: no votes were cast at read time
  (`voted=0`, `entailed=0`), and the landed reading belongs to the round-54 report. The draft's `holds` and the
  vote-arm attribution are therefore stated as pending.
- I could not attribute the uncommitted working-tree block (`corpus/README.md:771-785`) or the uncommitted
  `SKILL.md`/`PROVINCE.md`/`SCORECARD.md`/`corpus/QUALITY.md` edits to a seat; they are uncommitted and git records
  no author for them.
- Lane-wide "no other entry's table pins v7.2" (contract C1 surface sentence) was checked only through the counter's
  scope listing, not by an independent sweep of every claim table.

## Scratch, tooling, network

- No clone, work tree, fixture or temp file was created; no scratch directory was needed and none was left behind.
  No write outside this report.
- No tool installed or upgraded; no `pacman` transaction attempted; disk-guard not needed (read-only work).
- No network fetch; the release-drift checks read the committed copy. No host mutation: no sysctl write, no poison
  injection, no cgroup or systemctl action.

## Findings

1. **LOW — `corpus/README.md:771-785`**: a `## Round-54 coverage additions` block already exists as an uncommitted
   working-tree change (+16 lines vs data commit `78295c76`, mtime 2026-10-27 01:42:11 -0300). Applying this draft
   by append would duplicate the heading; integration must replace those lines or drop one of the two blocks.
2. **LOW — `corpus/README.md:776`** (existing block, row 2): "no claim-table row of the lane pins v7.2 unrechecked"
   is a lane-wide negative; the counter's scope evidence is 31 rows of three named entries
   (`.ufo/waves/round-54/evidence/c1-scope.txt`). The draft attributes the scope to the counter instead.
3. **LOW — `corpus/README.md:775-776`** (existing block): neither row carries the data-commit counter reading
   (`c1-at-data.txt`, `c2-at-data.txt`), unlike the round-53 rows at `:754-755`; as written the block asserts
   coverage without a measurement line.
4. **LOW — `corpus/README.md:773-785`** (existing block): the release-drift leads name `delay_nsec` and the
   read-write pressure files without the page copy lines, and the block does not say the three entries' own
   `source:`/`recheck:` headers are unchanged; both are checkable facts (`cgroup-v2.7.3.html:1719,2012,2117-2118`;
   `oom-memcg-stat-r50.md:1-7`; `quota-observability-r48.md:7-8`) and the draft states them.
5. **LOW — `SKILL.md:1217-1239`, `PROVINCE.md:463-469`, `SCORECARD.md`, `corpus/QUALITY.md`**: uncommitted
   working-tree edits (+38/+20/+15/+41 vs `78295c76`) exist outside this seat's write scope and outside the data
   commit. Not read as evidence by this report; the L1 should confirm they are the intended drafts and commit or
   discard them deliberately.
