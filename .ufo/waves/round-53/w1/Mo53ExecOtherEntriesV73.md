# Mo53ExecOtherEntriesV73 — drift probe for round 54: the round-47 and round-50 OOM entries at Linux v7.3

Seat: executor, informational drift probe. **Not a claim of round 53**: this report decides nothing about C1 or C2 and
writes no lane file. Its product is a measured held/absent reading for the two lane entries whose recheck is
release-triggered and which round 53's scope D excluded (`oom-tracepoints-r47.md`, `oom-memcg-stat-r50.md`), plus the
round-54 routing items that fall out of it.

Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecOtherEntriesV73/` (`mkdir -p`; `TMPDIR` set to its `tmp/`; `disk-guard.sh
status` read before the first fetch → `/fast/scratch/hyaku` 24 % used, 614.9 G free; removed at the end of this seat).
Tooling: none installed, none upgraded (python3, git, curl already present). No lane file, no fleet-root file and no
`~/.local/bin` entry was written; the only write is this report. All git use on the lane is read-only
(`clone --shared`, `show`, `rev-parse`); all commits in this seat were made in scratch repos with identity
`probe <probe@example.invalid>` after `git rev-parse --show-toplevel` printed the scratch dir.

## 0. What was fetched, and its provenance

`raw.githubusercontent.com` answered HTTP 429 twice while replaying the r50 recheck recipe during this seat (§5.3), and
the round-53 contract records the same on 2026-10-26, so every kernel byte below was taken from git.kernel.org cgit:

```
curl -fsSL "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=v7.3"
```

| file | v7.3 sha256 | committed v7.2 copy sha256 | relation |
|---|---|---|---|
| `include/trace/events/oom.h` | `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d` | `82f04ad4108ba949…` | **byte-identical** |
| `mm/oom_kill.c` | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | `452f1348e79c252e…` | **byte-identical** |
| `mm/page_alloc.c` | `315ef97b0ec1c6d759fe1d57c79177c2fcf00f5228bd8895ff718aa265fda33c` | `439ae8ec1e47cbf3…` | changed |
| `fs/proc/base.c` | `fb419e9a64d617039d5e90d53f0d634a0a2d4d1d9b1e99698b04e9412df38d5c` | `cef1a2cf3f34f683…` | changed |
| `mm/memcontrol.c` | `bdb6159cc2378c44c356b6788f521812f15c4d4936e8b09c66ef70b56bcc41a1` | `8a28e0bc010e0575…` | changed |
| `admin-guide/cgroup-v2.html` (docs.kernel.org/7.3) | `b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b` | `2d716cb798eacf8f…` (7.2 page) | changed (version stamp + non-memory sections) |

Tag resolution (cgit `ls-remote`, read-only):

```
237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63  refs/tags/v7.2
091b06388b117fefdcb63336ac09956a4914b961  refs/tags/v7.3
c03c1a14507dfaf8b856c2608f9ac216021fc222  refs/tags/v7.3^{}
```

`v7.3^{}` = `c03c1a14507dfaf8b856c2608f9ac216021fc222` — **the same commit** `corpus/SOURCES.md` S003/S004/S005 already
pin as "Linux master commit c03c1a14… (2026-10-18)". So the v7.3 release commit and the lane's master pin are one
commit, and the r47 entry's S005 note ("the same header at master `c03c1a14`, byte-identical") is confirmed by
`sha256(master c03c1a14 oom.h) = sha256(v7.3 oom.h) = sha256(v7.2 oom.h) = 82f04ad4…`.

Cross-channel check: all five v7.3 files fetched again from `raw.githubusercontent.com/torvalds/linux/v7.3/<path>` gave
the identical sha256 (cgit == raw.githubusercontent for every file). `https://docs.kernel.org/7.4/…` → HTTP 404, so 7.3
is the current docs version.

## 1. The round-47 entry (`oom-tracepoints-r47.md`) at v7.3

### 1.1 Can the frozen counter take the v7.3 copies? — not as a CLI, yes by its own `evaluate()`

`count-c2.py` (round 47) accepts `--repo DIR --entry PATH` and reads `git show <rev>:<path>`; it does **not** accept
copies from the filesystem. Its `PINS` are frozen v7.2 sha256 and its SOURCES-row arm hard-codes the literal `"v7.2"`
(`evaluate()`, `"v7.2" in cells[1]`). The frozen file was therefore **not edited**: it was imported read-only
(`importlib`) and its `PINS` rebound in memory to the v7.3 digests, then its own `evaluate()` run against a scratch git
repo holding the v7.3 copies at the same paths, the entry unchanged, and the lane's `SOURCES.md` unchanged.

```
$ python3 probe_r47_v73.py
== counter logic, PINS rebound to v7.3 bytes ==
C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=v73-copies
met=True

== counter logic, original frozen v7.2 PINS against v7.3 bytes (pin arm) ==
C2=unmet events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=2 source_row=ok provenance=ok rev=v73-copies-frozen-pins failed=pins
```

Baseline that the frozen counter still reads *met* on the lane's own v7.2 data (scratch `git clone --shared`, no writes):

```
$ python3 .ufo/waves/round-47/count-c2.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df --repo <scratch>/laneclone
C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df
rc=0
$ python3 .ufo/waves/round-47/count-c2.py --selftest | tail -1
C2_SELFTEST pass=13 fail=0
```

### 1.2 Held/absent — the catalogue holds at v7.3 with zero mismatch

The counter's own parse of the v7.3 header gives 8 events at the same header lines the entry cites, with the same
`TP_STRUCT__entry` field sets, and every `trace_<name>(` call site is present in its cited copy:

```
v7.3 TRACE_EVENT count: 8
v7.3 TRACE_EVENT lines: [12, 34, 76, 118, 134, 150, 166, 183]      # entry line 17 claim
  oom_score_adj_update     comm,oom_score_adj,pid
  reclaim_retry_zone       available,min_wmark,no_progress_loops,node,order,reclaimable,wmark_check,zone_idx
  mark_victim              anon_rss,comm,file_rss,oom_score_adj,pgtables,pid,shmem_rss,total_vm,uid
  wake_reaper              pid
  start_task_reaping       pid
  finish_task_reaping      pid
  skip_task_reaping        pid
  compact_retry            max_retries,order,priority,result,ret,retries
  oom_score_adj_update     -> sources-r47/fs_proc_base.c
  reclaim_retry_zone       -> sources-r47/mm_page_alloc.c
  mark_victim              -> sources-r47/mm_oom_kill.c
  wake_reaper / start / finish / skip_task_reaping -> sources-r47/mm_oom_kill.c
  compact_retry            -> sources-r47/mm_page_alloc.c
== entry table rows vs v7.3 events == rows=8
  (each of the 8 rows: fields_match=True  call_present=True)
events_not_in_entry=[]
```

The non-table prose spans also hold: `oom_kill.c` is byte-identical between v7.2 and v7.3, so
`oom_kill.c:751-775 / 656-674 / 562-599 / 567 / 578 / 582 / 595 / 673 / 774` (entry lines 25–31, 41, 44, 48) and the
`TP_printk` line 105 citation (entry line 35) are still exact at v7.3:

```
73:105 TP_printk("pid=%d comm=%s total-vm=%lukB anon-rss=%lukB file-rss:%lukB shmem-rss:%lukB uid=%u pgtables=%lukB oom_score_adj=%hd",
73:751 void mark_oom_victim(   73:774 trace_mark_victim(tsk, cred->uid.val);
73:656 void wake_oom_reaper(  73:673 trace_wake_reaper(tsk->pid);
73:562 bool oom_reap_task_mm( 73:567/578 trace_skip_task_reaping  73:582 trace_start_task_reaping  73:595 trace_finish_task_reaping
```

**Held 8/8 events, 8/8 field sets, 8/8 call sites; absent 0.** The only v7.3 mismatch is the pin arm, and it is 2, not 4:
`mm/oom_kill.c` and `include/trace/events/oom.h` are byte-identical across the two tags. The two files that changed
(`mm/page_alloc.c`, `fs/proc/base.c`) changed nowhere near the cited emit sites:

- `fs/proc/base.c`: 8 changed lines in 2 hunks, all a rename `task->fs` → `task->real_fs` in
  `get_task_root()`/`get_task_pwd()` (lines ~211–231); `trace_oom_score_adj_update(task)` is still at 1158 and
  `__set_oom_adj` still at 1106.
- `mm/page_alloc.c`: the bodies of `should_reclaim_retry()` (75 lines) and `should_compact_retry()` (66 lines) are
  **byte-identical** between v7.2 and v7.3; only their line numbers move.

### 1.3 The drift that the counter cannot see: two line citations

The entry's table cells (lines 25 and 31) name v7.2 line numbers that are now wrong:

| entry line | citation | v7.2 | v7.3 | drift |
|---|---|---|---|---|
| 25 | `reclaim_retry_zone` … `should_reclaim_retry`, `page_alloc.c:4630` | 4630 = `trace_reclaim_retry_zone(` | 4689 | +59 |
| 31 | `compact_retry` … `should_compact_retry`, `page_alloc.c:4265` | 4265 = `trace_compact_retry(` | 4311 | +46 |
| 24 | `oom_score_adj_update` … `__set_oom_adj`, `base.c:1158` | 1158 = `trace_oom_score_adj_update(task)` | 1158 | 0 |

At v7.3 line 4630 of `mm/page_alloc.c` is the comment `* Checks whether it makes sense to retry the reclaim…` and 4265 is
blank. So a v7.3 recheck of this entry keeps every structural assertion and still leaves two stale line citations, because
the counter's predicate is names/fields/call-site *presence*, not position.

## 2. The round-50 entry (`oom-memcg-stat-r50.md`) at v7.3

### 2.1 Every claim quote — 22 of 22 held, zero absent

Quote cells extracted from the entry's claims table (22 rows) and tested against the v7.3 bytes of that row's S-row
source; HTML copies are tag-stripped and entity-decoded, and both sides are whitespace-collapsed (the doc and the kernel
sources wrap the quoted spans). The same probe was also run against the committed v7.2 copies as a control, to separate
"quote wrong" from "kernel changed":

```
$ python3 probe_r50_v73.py
 0 S489 v7.2=yes v7.3=yes HELD     … (rows 1-21 identical shape)
21 S491 v7.2=yes v7.3=yes HELD
rows=22 held_v7.2=22 absent_v7.2=0 held_v7.3=22 absent_v7.3=0
```

**held=22, absent=0. There is no absent quote to list.** Because the v7.2 control is also 22/22, no quote's presence
flipped between the tags.

Superset check over every backticked span in both entries (paths, commands and placeholders excluded):

```
== r47 entry (oom-tracepoints-r47.md) : 109 backticked spans (13 path-like skipped) ==
  spans_checked=96 present_v7.2=80 absent_v7.2=16 present_v7.3=80 absent_v7.3=16
== r50 entry (oom-memcg-stat-r50.md) : 114 backticked spans (4 path-like skipped) ==
  spans_checked=110 present_v7.2=92 absent_v7.2=18 present_v7.3=92 absent_v7.3=18
```

Nothing is present in one tag and absent in the other. The 16/18 spans absent in both are non-quote text
(`merge/mori/`, `## Gate`, `sudo -n ls`, `Permission denied`, `K()`, `workingset_*`, `pgscan*`, `oom-kill.c.v7.2:954-985`,
`constraint=CONSTRAINT_MEMCG`, …), i.e. they were never meant to occur in those copies.

### 2.2 Can the frozen round-50 counter take the v7.3 copies? — yes, with `COPIES` and the SOURCES rows rebound

Same method: the frozen `count-c2.py` was imported read-only; `COPIES` was rebound in memory to the v7.3 URLs, copies and
digests; the scratch repo held the v7.3 copies and a **scratch-only** rewrite of the S489/S490/S491 `SOURCES.md` rows
(URLs → `…/7.3/…`, copy names → `*.v7.3`, sha256 → the v7.3 digests; status/date/used-by untouched). The lane's
`SOURCES.md` was not modified.

```
$ python3 probe_r50_counter_v73.py
counter logic vs v7.3 copies (COPIES rebound):
  C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=v73-copies
  met=True
counter logic vs v7.3 tree, frozen v7.2 COPIES (pin arm):
  C2=unmet claims=22 located=0 quote_missing=0 bad_rows=22 sources=0 source_rows=bad pins=bad provenance=ok rev=v73-copies-frozen-v7.2-copies failed=bad_rows,pins,source_rows,sources_floor
```

So the entry's 22 claims are re-derivable at v7.3 from v7.3 bytes with a re-pointed counter and re-pointed SOURCES rows;
with the frozen v7.2 bindings the same tree reads `pins=bad` (correct: the bytes are not the pinned bytes) and the row arm
goes `bad` (correct: the SOURCES rows still name `/v7.2/` URLs).

### 2.3 The drift in the r50 entry: memcontrol.c line citations move by +45

`mm/oom_kill.c` is byte-identical, so every S491 citation in the entry (`oom_kill.c.v7.2:239-244, 935-936, 945, 954-985,
1075, 1158`) and in SOURCES S491 (`:400-410, 424-431, 444-454, 456-469, 912-985, 1008-1054, 1146-1170`) is still exact at
v7.3. `mm/memcontrol.c` is not: the same quoted text sits 45 lines later (84 for `memory_stat_show`).

Every cited span was relocated by whole-block equality (the v7.2 lines occur verbatim, same length, at the v7.3 line):

| entry/SOURCES citation | v7.2 content | v7.3 span | drift | block identical |
|---|---|---|---|---|
| `memcontrol.c.v7.2:629` (entry line 66) | `/* Aggregated (CPU and subtree) … */` | 674 | +45 | yes |
| SOURCES S490 `:1546-1608` | `memory_stats[]` table | 1591-1653 | +45 | yes |
| `memcontrol.c.v7.2:1549` (entry line 63) | `{ "kernel", MEMCG_KMEM },` | 1594 | +45 | yes |
| `memcontrol.c.v7.2:1628-1665` (entry line 54) | `memcg_page_state_output_unit()` | 1673-1710 | +45 | yes |
| SOURCES S490 `:1693-1748` | `memcg_stat_format()` | 1738-1793 | +45 | yes |
| `memcontrol.c.v7.2:1739-1748` (entry line 54) | `memcg_vm_event_stat` loop | 1784-1793 | +45 | yes |
| SOURCES S490 `:1751` | `memory_stat_format()` | 1796 | +45 | yes |
| SOURCES S490 `:1770-1784` | `mem_cgroup_print_oom_context()` | 1815-1829 | +45 | yes |
| SOURCES S490 `:1787-1830` | `mem_cgroup_print_oom_meminfo()` | 1832-1875 | +45 | yes |
| SOURCES S490 `:1994-1999` | `mem_cgroup_print_oom_group()` | 2039-2044 | +45 | yes |
| SOURCES S490 `:4905-4919` | `memory_stat_show()` | 4989-5003 | +84 | yes |

All nine cited blocks are byte-identical between the tags; only their position moved. So the r50 entry needs a
line-number refresh, not a re-quote.

Per-quote measured drift of the eight S490 quote cells: `+45` for seven, `+84` for the `seq_puts(m, buf)` row.

### 2.4 What did *not* drift (checked because the entry claims it)

- `memory.stat` key set: 49 keyed names in `memcontrol.c` at both tags, added `[]`, removed `[]`, same order. The v7.3
  enum gains `NR_VMSCAN_WRITE`, `PGROTATE_ANON`, `PGROTATE_FILE` (lines 402, 429, 430) but none of them is in
  `memcg_vm_event_stat[]` or `memory_stats[]`, so no new `memory.stat` key appears — the entry's "conditional key set"
  reading rule is still right.
- `memory_stat_format` / `memcg_stat_format` / `mem_cgroup_print_oom_context` / `mem_cgroup_print_oom_group` all present
  with identical quoted bodies; `MEMCG_MAX` failcnt, `memory: usage`, `swap: usage`, `Memory cgroup stats for`,
  `oom.group` line and `pr_cont(",oom_memcg=")`/`(",task_memcg=")` all present once each.
- cgroup-v2 doc: after tag-strip the memory-interface block (`memory.max`…`memory.numa_stat`, 5846 chars) is
  **identical** in 7.2 and 7.3, `memory.stat` block diff = 0 lines, all ten memory.* keys appear the same number of times.
  The one memory-area change anywhere in the page is `memory.pressure A read-only nested-keyed file.` →
  `… A read-write nested-keyed file.` (§5.5).

## 3. What this means for round 54 (routing, not this claim)

Both entries' recheck triggers have fired: `oom-tracepoints-r47.md` header line 5 says `recheck: on-release`, and its
SOURCES rows S475/S476 say `on-release`; `oom-memcg-stat-r50.md` SOURCES rows S489/S490/S491 also say `on-release`
(its header line 7 says `90d` — §5.4). Neither was in C1's scope D. Measured answer to "did they drift?":

| entry | structure at v7.3 | quoted text at v7.3 | line citations at v7.3 | pins at v7.3 |
|---|---|---|---|---|
| `oom-tracepoints-r47.md` | holds (8/8 events, 8/8 field sets, 8/8 call sites) | n/a (no quote arm) | 2 stale (`page_alloc.c:4630→4689`, `:4265→4311`); `base.c:1158` and all `oom_kill.c` cites hold | 2 of 4 copies changed |
| `oom-memcg-stat-r50.md` | holds (22/22 claims re-derive) | 22/22 held, 0 absent | all 9 cited `memcontrol.c` blocks shift (+45; +84 for `memory_stat_show`), contents byte-identical; all `oom_kill.c` cites hold | 2 of 3 copies changed; doc page changed |

A round-54 recheck therefore needs no rewriting of any claim, only: new pinned copies (`*.v7.3` + the 7.3 doc page), new
SOURCES rows naming `/7.3/` URLs and the v7.3 digests, refresh of the line citations above, and re-pointed counters
(`PINS` for r47; `COPIES` **and** `OPENED` for r50 — see §5.1). Draft pin rows for that work, fenced and not applied:

```
| entry | v7.3 source row | v7.3 copy | sha256 |
|---|---|---|---|
| oom-tracepoints-r47.md | include/trace/events/oom.h @ v7.3 (tag peels to c03c1a14507dfaf8b856c2608f9ac216021fc222) | corpus/evidence/sources-r54/include_trace_events_oom.h.v7.3 | 82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d |
| oom-tracepoints-r47.md | mm/oom_kill.c @ v7.3 | …/mm_oom_kill.c.v7.3 | 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e |
| oom-tracepoints-r47.md | mm/page_alloc.c @ v7.3 | …/mm_page_alloc.c.v7.3 | 315ef97b0ec1c6d759fe1d57c79177c2fcf00f5228bd8895ff718aa265fda33c |
| oom-tracepoints-r47.md | fs/proc/base.c @ v7.3 | …/fs_proc_base.c.v7.3 | fb419e9a64d617039d5e90d53f0d634a0a2d4d1d9b1e99698b04e9412df38d5c |
| oom-memcg-stat-r50.md | https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html | …/cgroup-v2.7.3.html | b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b |
| oom-memcg-stat-r50.md | mm/memcontrol.c @ v7.3 | …/memcontrol.c.v7.3 | bdb6159cc2378c44c356b6788f521812f15c4d4936e8b09c66ef70b56bcc41a1 |
| oom-memcg-stat-r50.md | mm/oom_kill.c @ v7.3 | …/oom_kill.c.v7.3 | 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e |
# line-citation refresh (v7.3): page_alloc.c 4630->4689, 4265->4311; memcontrol.c 1549->1594,
# 1628-1665->1673-1710, 1739-1748->1784-1793, 629->674, 1751->1796, 1770-1784->1815-1829,
# 1787-1830->1832-1875, 4905-4919->4989-5003; oom_kill.c and base.c citations unchanged.
```

## 4. Reproduction (drivers; scratch is removed, code retained here)

```python
# r47: import the frozen counter read-only, rebind PINS to the v7.3 digests
spec = importlib.util.spec_from_file_location("r47c2", "<lane>/.ufo/waves/round-47/count-c2.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
pins = {p: sha256(open(v73_path(p), "rb").read()).hexdigest() for p in m.PINS}   # same four copy paths
met, line = m.evaluate(m.git_reader(REPO, "HEAD"), pins, "v73-copies")          # REPO = scratch repo with v7.3 copies

# r50: same method, rebind COPIES (url -> (path, sha256, kind)); SOURCES rows rewritten in the scratch repo only
m = importlib.util.module_from_spec(spec50); spec50.loader.exec_module(m)
met, line = m.evaluate(m.git_reader(REPO50, "HEAD"), "v73-copies", copies=COPIES73)
```

Commands: `python3 probe_r47_v73.py`, `python3 probe_r50_counter_v73.py`, `python3 probe_r50_v73.py`,
`python3 probe_spans.py` — all from `/fast/scratch/hyaku/mori-r53/Mo53ExecOtherEntriesV73` with `TMPDIR` under it.

## 5. Named limits of the frozen instruments (route to round 54; no change proposed for this round)

### 5.1 Neither counter can be pointed at a new tag without editing a frozen constant

`count-c2.py` (r47) pins v7.2 digests in `PINS` **and** asserts the literal `"v7.2"` in the SOURCES row it accepts
(`evaluate()`: `"v7.2" in cells[1]`). `count-c2.py` (r50) pins `/v7.2/` URLs → copies in `COPIES` and asserts
`srow[8] == OPENED` with `OPENED = "2026-10-26"`. Consequence measured above: on v7.3 bytes the r47 counter returns
`pin_mismatch=2` and the r50 counter returns `pins=bad … bad_rows=22` even though every claim holds. A release recheck of
these two entries therefore cannot be scored by their own counters without a new counter revision — worth deciding in
round 54 rather than improvising at recheck time.

### 5.2 A "held" reading cannot see position

Confirmed on the r47 entry (§1.3): the same eight events, field sets and call sites, and two stale `page_alloc.c` line
numbers pass the counter unchanged. The same limit in the r50 entry is +45 in `memcontrol.c` (§2.3). This is the concrete
instance of C1's named limit "held proves the words still occur somewhere in the file, not at the same place".

### 5.3 Both entries' own recheck recipes fail silently on a rate-limited fetch

- r47 (entry line 5): `curl -fsSL …/<tag>/include/trace/events/oom.h | grep -c '^TRACE_EVENT('`. On an empty body this
  prints `0` and exits 1 — a 429 would read as "the header defines zero events".
- r50 (entry line 7): `for u in …; do curl -fsSL "$u" | sha256sum; done`. The pipeline's status is `sha256sum`'s, so a
  failed fetch prints the empty-body digest and exits 0. Observed live during this seat:

```
$ for u in https://docs.kernel.org/7.2/… https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c \
           https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c; do curl -fsSL "$u" | sha256sum; done
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  -
curl: (22) The requested URL returned error: 429
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  -
curl: (22) The requested URL returned error: 429
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  -
$ ( curl -fsSL "https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/nonexistent-xyz.c" | sha256sum ); echo $?
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  -
0
```

`e3b0c442…` is the sha256 of the empty string: a rate limit is indistinguishable from byte drift by exit status, and the
two 429s above would read as "two of three pinned sources changed". (`raw.githubusercontent` answered 200 on the same
paths minutes later, so the 429 is transient — the recipe's blindness is not.)

### 5.4 The r50 entry's own trigger field disagrees with its SOURCES rows

`corpus/knowledge/oom-memcg-stat-r50.md:7` says `recheck: 90d` (with a v7.2 sha256 recipe), while `corpus/SOURCES.md`
rows S489, S490 and S491 carry `on-release` in the recheck column. Under `on-release` the trigger fired at the v7.3 tag;
under `90d` it has not. Both readings cannot govern the same entry.

### 5.5 Residual doc drift (informational; no claim covers it)

The 7.3 cgroup-v2 page changes `memory.pressure` from `read-only nested-keyed file` to `read-write nested-keyed file`,
and adds one sentence about psi ownership. Nothing in the r50 entry's 22 claims or its reading rules depends on
`memory.pressure`, so this is a change to record, not a claim drift.

## 6. Blockers / unverified

- None for the reading itself. `mm/memcontrol.c`, `mm/oom_kill.c`, `mm/page_alloc.c`, `fs/proc/base.c`,
  `include/trace/events/oom.h` and the 7.3 doc page were all fetched and hashed this seat; every count above is from
  bytes on disk in scratch at the time of the run.
- Not attempted (out of this seat's scope, and out of round 53's data scope): rewriting the two entries, the SOURCES
  rows, or either counter; any host reading; any claim judgement on C1/C2.
- No file was created inside the lane by this seat or by the instruments it ran. The two frozen counters were driven
  from scratch (r47 CLI with `--repo <scratch clone>`, both `evaluate()` calls via read-only `importlib`); neither wrote
  a `__pycache__` entry (`round-47/__pycache__/count-c2.cpython-314.pyc` still 2026-10-25 16:41,
  `round-50/__pycache__/count-c2.cpython-314.pyc` still 2026-10-26 05:50), and `find .ufo/waves -newermt '-140
  minutes'` lists nothing outside `round-53/`.
- The r47/r50 `recheck` recipes were *run*, not repaired; §5.3's 429s are the only failures observed and they were
  transient.

## Findings

- **MED** — `corpus/knowledge/oom-tracepoints-r47.md:25` and `:31`: the `mm/page_alloc.c` line citations are v7.2-only
  and are wrong at v7.3 (`should_reclaim_retry` trace call 4630→4689, +59; `should_compact_retry` trace call 4265→4311,
  +46). The entry's own counter passes at v7.3 regardless (names/fields/call sites all hold), so a release recheck will
  not surface this.
- **MED** — `corpus/knowledge/oom-memcg-stat-r50.md:54, :63, :66` and `corpus/SOURCES.md` S490: the `mm/memcontrol.c`
  line citations are v7.2-only; the same content is +45 lines later at v7.3 (1549→1594, 1628-1665→1673-1710,
  1739-1748→1784-1793, 629→674, 1751→1796, 1770-1784→1815-1829, 1787-1830→1832-1875) and +84 for 4905-4919→4989-5003.
  All 22 quotes still hold, so the r50 counter also passes without revealing it.
- **MED** — `.ufo/waves/round-47/count-c2.py` (`PINS`, and `"v7.2" in cells[1]`) and
  `.ufo/waves/round-50/count-c2.py` (`COPIES`, `OPENED`): both counters are tag-hardcoded, so a v7.3 recheck cannot be
  scored by them as they stand — measured `pin_mismatch=2` (r47) and `pins=bad … bad_rows=22` (r50) on v7.3 bytes whose
  claims all hold. Round-54 decision needed.
- **MED** — `corpus/knowledge/oom-memcg-stat-r50.md:7` and `corpus/SOURCES.md` S489/S490/S491: the entry declares
  `recheck: 90d`, its three SOURCES rows declare `on-release`; the v7.3 tag is the release those rows key on, so the entry
  has an ambiguous trigger.
- **MED** — `corpus/knowledge/oom-memcg-stat-r50.md:7` (r50 recheck recipe) and `corpus/knowledge/oom-tracepoints-r47.md:5`
  (r47 recheck recipe): neither recipe distinguishes a failed fetch from a content change. Observed HTTP 429 twice on the
  r50 recipe's `raw.githubusercontent` URLs on 2026-10-26, with the pipeline printing the empty-body sha256
  `e3b0c442…` and exiting 0; the r47 recipe prints `0` events and exits 1 on the same failure.
- **LOW** — `corpus/evidence/sources-r50/memcontrol.c.v7.2` vs v7.3: `mm/memcontrol.c` gained `NR_VMSCAN_WRITE`,
  `PGROTATE_ANON`, `PGROTATE_FILE` in its enums (v7.3 lines 402, 429, 430) but none reaches `memory.stat`; the keyed name
  set is unchanged (49 keys, same order). No claim drift — recorded so a future recheck does not read the enum churn as a
  key-set change.
- **LOW** — `corpus/SOURCES.md` S003/S004/S005 ("Linux master commit `c03c1a14…`"): that commit is exactly
  `refs/tags/v7.3^{}` (`c03c1a14507dfaf8b856c2608f9ac216021fc222`). The master pins in those rows are now
  release-identical; S005's "byte-identical" claim is confirmed for `include/trace/events/oom.h` (82f04ad4…, same at
  v7.2, v7.3 and that commit).
- **LOW** — 7.3 cgroup-v2 doc (`docs.kernel.org/7.3/admin-guide/cgroup-v2.html`, sha256 `b478c1ba…`): `memory.pressure`
  changes from read-only to read-write; the memory-interface block and the `memory.stat` description are otherwise
  identical to the 7.2 page. No r50 claim touches it.
