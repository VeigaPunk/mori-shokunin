# Mo50ScribeEntryA — round 50, wave w1 (C2 depth: memcg OOM report block)

Seat: scribe. Lane `mori-shokunin`, repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Read at lane HEAD `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379` (round-50 freeze; entering tip
`7197160b927f04db294c9553fb48fadcc7a3f4e3`). Contract read first: `.ufo/waves/round-50/contract.md`.

Assignment: draft the C2 entry `corpus/knowledge/oom-memcg-stat-r50.md` in full from the three committed copies,
with the shape P-C2 measures; draft the S489–S491 registry rows; verify every quote with the counter's own
`normalise()`/`normalise_text()`; report only.

Nothing in the lane was edited. `corpus/`, `corpus/SOURCES.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/` and
every frozen file under `.ufo/waves/round-50/` are untouched; the drafts below are for the L1 to integrate. `git status
--porcelain` in the lane after this work shows only untracked `.ufo/waves/round-49/w1/Mo49ExecCounterTiming.md` (inherited)
and untracked `.ufo/waves/round-50/w1/` (seat reports). No host kernel log, no cgroup limit, no systemd/journald state
was read or changed.

## Behaviour (what I did)

1. Opened all three committed copies myself (bytes read, not summaries): `corpus/evidence/sources-r50/cgroup-v2.7.2.html`
   (168438 bytes), `memcontrol.c.v7.2` (160768), `oom_kill.c.v7.2` (34311). In the memcontrol copy I read
   `memory_stats[]` (:1546), `memcg_stat_format` (:1693), `memory_stat_format` (:1751),
   `mem_cgroup_print_oom_context` (:1770), `mem_cgroup_print_oom_meminfo` (:1787), the block print (:1824) and
   `memory_stat_show` (:4905). In the oom_kill copy I read `dump_task` (:400), `dump_tasks` (:424), `dump_oom_victim`
   (:444), `dump_header` (:456), `__show_mem` (:468), `__oom_kill_process`/the victim line (:912-951),
   `oom_kill_memcg_member` (:956) and the memcg/global message choice (:1169).
2. Read the two staged candidates under `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/`
   (`scope-charge-fields-r46.md`, `scope-composition-in-the-block-r47.md`) as candidates only. None of their numbers
   (266723328, 266539008, 131072, 255176, 386248, the `cap-run-*` scope path) and none of their own-work sources
   (S533/S534/S539) appear in the entry — the entry carries no host measurement at all.
3. Wrote the entry with 22 claim rows over all three sources (7 x S489, 8 x S490, 7 x S491). Every quote is an exact
   substring of the counter-normalised copy, extracted programmatically, so no hand transcription can drift.
4. Validated with the frozen counter itself: first `evaluate()` over an in-memory read, then end to end in a throwaway
   archive fixture (`git init` in scratch, `git archive HEAD` of the lane, commit under a throwaway identity,
   `--repo` the fixture). Three falsifiers were then committed against the same fixture.
5. Removed the scratch directory; every command, output and the two full drafts are reproduced here.

## Gates (commands and observed output, verbatim)

### Counter self-test (frozen tool, unchanged)

```
$ python3 .ufo/waves/round-50/count-c2.py --selftest
PASS honest_met
PASS entry_absent_unmet
PASS no_table_unmet
PASS altered_quote_unmet
PASS quote_from_wrong_copy_unmet
PASS short_quote_unmet
PASS long_quote_unmet
PASS duplicate_quote_unmet
PASS claims_floor_unmet
PASS sources_floor_unmet
PASS row_not_mined_unmet
PASS row_opened_other_day_unmet
PASS used_by_missing_unmet
PASS indented_row_ok
PASS code_indented_row_unmet
PASS pin_mismatch_unmet
PASS table_id_uncited_in_source_unmet
PASS verified_at_missing_unmet
PASS header_wrong_unmet
PASS claim_cell_short_unmet
PASS breadcrumb_identical_claims_unmet
PASS claim_echoes_quote_unmet
PASS table_inside_fence_unseen_unmet
PASS other_entry_path_unmet
PASS escaped_pipe_quote_located
PASS words_beyond_counts
PASS text_copy_keeps_angle_brackets
PASS normalise_drops_script_text
PASS normalise_drops_style_text
PASS normalise_drops_comment_text
PASS normalise_keeps_visible_text
C2_SELFTEST pass=31 fail=0
exit=0
```

### Source pins (lane worktree at the freeze)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r50
$ sha256sum cgroup-v2.7.2.html memcontrol.c.v7.2 oom_kill.c.v7.2
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  cgroup-v2.7.2.html
8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e  memcontrol.c.v7.2
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  oom_kill.c.v7.2
exit=0
```

All three equal the `COPIES` digests in `.ufo/waves/round-50/count-c2.py:31-38`.

### The entry's `recheck:` command, run today (2026-10-26)

```
$ export TMPDIR=<scratch>/tmp
$ for u in https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html \
           https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c \
           https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c; do curl -fsSL "$u" | sha256sum; done
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  -
8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e  -
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  -
exit=0
```

Live bytes still identical to the frozen copies, so the `recheck:` line states an observed result, not a planned one.

### End-to-end counter run on a throwaway archive fixture — FEASIBILITY, not the claim's landing

Fixture: `git init` in scratch, `git archive HEAD` of the lane at `950e99be` extracted into it, then the entry and the
rows installed and committed under `-c user.name=Mo50ScribeEntryA -c user.email=seat@fixture.invalid`. The counter was
run with `--repo <fixture>`, so the revs below are fixture commits, not lane revisions.

```
$ python3 .ufo/waves/round-50/count-c2.py 7189a1175bc690e31341f55d372f86551861796b --repo <fixture>
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=7189a1175bc690e31341f55d372f86551861796b
exit=0

$ python3 .ufo/waves/round-50/count-c2.py 013fa55a2d685c21ff3f3bfed9ac6988dd495919 --repo <fixture>   # restored bytes = HEAD
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=013fa55a2d685c21ff3f3bfed9ac6988dd495919
exit=0
```

An earlier 21-row draft of this entry also scored `C2=met` (fixture revs `4069616`, `3b59b19`); the entry then gained a
22nd row (the rate-limit guard, `mm/oom_kill.c:1030-1033`) and a matching Limits bullet, and every run above was redone
on the 22-row bytes. The superseded revs are named only so a reviewer can see what changed.

### Falsifiers against the same fixture (each a commit, then a counter run)

```
$ python3 .ufo/waves/round-50/count-c2.py 8915d9aa97179581f041c60a0de3627f51bde6ba --repo <fixture>
control: one quote altered ("shared memory" -> "shared storage")
C2=unmet claims=22 located=21 quote_missing=1 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=8915d9aa97179581f041c60a0de3627f51bde6ba failed=quote_missing
exit=1

$ python3 .ufo/waves/round-50/count-c2.py c8476f42cc593844376578cb59d4154e30b73fdc --repo <fixture>
control: S491 rows with opened 2026-10-25 instead of 2026-10-26
C2=unmet claims=22 located=15 quote_missing=0 bad_rows=7 sources=2 source_rows=bad pins=ok provenance=ok rev=c8476f42cc593844376578cb59d4154e30b73fdc failed=bad_rows,source_rows,sources_floor
exit=1

$ python3 .ufo/waves/round-50/count-c2.py 077bf39a4b200c13069e1b0b2b641c6ce9c86a0d --repo <fixture>
control: every S491 row removed (two sources only)
C2=unmet claims=22 located=15 quote_missing=0 bad_rows=7 sources=2 source_rows=bad pins=ok provenance=ok rev=077bf39a4b200c13069e1b0b2b641c6ce9c86a0d failed=bad_rows,source_rows,sources_floor
exit=1
```

The two row-level controls share a signature because a row whose source row is absent or mis-dated counts as bad; that is
the counter's design, and neither variant passed.

### Per-row quote verification (the counter's own normalisers)

`S489` quotes were located in `normalise(html)` of `cgroup-v2.7.2.html` (script/style/comment blocks dropped, tags
stripped, entities decoded, whitespace collapsed); `S490`/`S491` quotes in `normalise_text()` (whitespace collapsed only)
of their copies. `beyond` is `words_beyond(claim, quote)` — words of 3+ letters in the claim absent from the quote.

```
S489 html normalise()         located=True offset= 45386 qwords=17 claimwords=24 beyond=16  OK
S489 html normalise()         located=True offset= 54368 qwords=16 claimwords=21 beyond=10  OK
S489 html normalise()         located=True offset= 54636 qwords=14 claimwords=17 beyond= 7  OK
S489 html normalise()         located=True offset= 55338 qwords=17 claimwords=19 beyond= 5  OK
S489 html normalise()         located=True offset= 54724 qwords=21 claimwords=22 beyond=13  OK
S489 html normalise()         located=True offset= 54102 qwords=17 claimwords=17 beyond=14  OK
S489 html normalise()         located=True offset= 53284 qwords=15 claimwords=22 beyond=12  OK
S490 text normalise_text()    located=True offset= 45392 qwords= 7 claimwords=19 beyond= 9  OK
S490 text normalise_text()    located=True offset= 45232 qwords= 9 claimwords=21 beyond=14  OK
S490 text normalise_text()    located=True offset= 45597 qwords= 7 claimwords=19 beyond=10  OK
S490 text normalise_text()    located=True offset= 46225 qwords= 7 claimwords=22 beyond=15  OK
S490 text normalise_text()    located=True offset=125307 qwords= 7 claimwords=22 beyond=15  OK
S490 text normalise_text()    located=True offset= 44630 qwords= 8 claimwords=19 beyond=12  OK
S490 text normalise_text()    located=True offset= 44738 qwords= 7 claimwords=20 beyond=13  OK
S490 text normalise_text()    located=True offset= 50272 qwords=14 claimwords=20 beyond=12  OK
S491 text normalise_text()    located=True offset= 24631 qwords=12 claimwords=16 beyond= 5  OK
S491 text normalise_text()    located=True offset= 30850 qwords=12 claimwords=20 beyond=15  OK
S491 text normalise_text()    located=True offset= 12272 qwords= 8 claimwords=16 beyond=11  OK
S491 text normalise_text()    located=True offset= 27075 qwords= 7 claimwords=25 beyond=19  OK
S491 text normalise_text()    located=True offset= 11583 qwords=13 claimwords=18 beyond= 9  OK
S491 text normalise_text()    located=True offset= 24220 qwords=15 claimwords=21 beyond=13  OK
S491 text normalise_text()    located=True offset= 11047 qwords=20 claimwords=20 beyond=11  OK
all rows ok: True rows 22
```

## Report self-consistency (the drafts pasted here are the bytes that scored)

```
$ # re-extract both fenced drafts from this report, apply them to the lane HEAD tree in the fixture
$ git -C <fixture> status --porcelain
(no output)
$ python3 .ufo/waves/round-50/count-c2.py HEAD --repo <fixture>
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=013fa55a2d685c21ff3f3bfed9ac6988dd495919
exit=0
$ grep -c '| S489 |' <fixture>/corpus/SOURCES.md
1
```

Applying the two blocks below to `git show HEAD:corpus/SOURCES.md` (lane freeze) leaves the fixture working tree clean,
so the text in this report is byte-identical to the tree that measured `C2=met`, and no row is duplicated.

## Draft 1 — `corpus/knowledge/oom-memcg-stat-r50.md`

Bytes: 10508, sha256 `37dc8bc848f3ad6c479c44e1173d674418d8da4b7c336d3b04dbb40c292cae59`. This is the exact text that scored
`C2=met` in the fixture, pasted without edits.

```markdown
# A memcg OOM prints its charge three ways: usage line, stats block, victim line

source: S489 — https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html — docs, tier A, Control Group v2 documentation at kernel 7.2 (memory interface files, memory.events, memory.oom.group), opened 2026-10-26
source: S490 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c — code, tier A, mm/memcontrol.c at tag v7.2 (the memcg OOM report path and the memory.stat formatter), opened 2026-10-26
source: S491 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c — code, tier A, mm/oom_kill.c at tag v7.2 (the victim record and the memcg-versus-global report split), opened 2026-10-26
verified-at: 2026-10-26
recheck: 90d — `for u in https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c; do curl -fsSL "$u" | sha256sum; done` -> 2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34, 8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e, 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e in that order (ran 2026-10-26; all three matched the committed copies)
coverage-map: FR1

mori attributes a kill at event time: which cgroup was over its charge, what that cgroup held, and which process died.
A memcg OOM prints all three in one burst: a usage/limit line, a `Memory cgroup stats for <path>:` block written by the
same formatter that writes memory.stat, and a per-victim `Killed process` line carrying the victim's own counters.
A global OOM prints a system-wide memory summary in place of that block and names no charged scope, so its burst cannot
place the charge in a cgroup.
That difference is the detection rule this entry serves: a stats block means the kill was charged to a scope.
| claim | source | quote |
|---|---|---|
| Every memory amount the block prints is a byte count, and an unaligned write may be rounded up to a page when read back. | S489 | `All memory amounts are in bytes. If a value which is not aligned to PAGE_SIZE is written,` |
| The anon key counts anonymous mappings such as brk and MAP_ANONYMOUS, so it carries a process heap rather than page cache. | S489 | `anon Amount of memory used in anonymous mappings such as brk() , sbrk() , and mmap(MAP_ANONYMOUS).` |
| The file key includes tmpfs and shared memory, so a filesystem cache total also carries tmpfs pages. | S489 | `file Amount of memory used to cache filesystem data, including tmpfs and shared memory.` |
| The shmem key is the swap-backed part of that cached data, covering tmpfs, shm segments and shared anonymous mmap. | S489 | `shmem Amount of cached filesystem data that is swap-backed, such as tmpfs, shm segments, shared anonymous mmap()s` |
| The kernel key aggregates kernel_stack, pagetables, percpu, vmalloc and slab, and each of those five is also printed under its own name. | S489 | `kernel (npn) Amount of total kernel memory, including (kernel_stack, pagetables, percpu, vmalloc, slab) in addition to other kernel memory use cases.` |
| A parser must match key names, because a newer kernel can insert a counter between existing lines. | S489 | `Don’t rely on items remaining in a fixed position; use the keys to look up specific values!` |
| A rising oom_kill count does not prove a kernel memcg OOM, because the field counts kills by any kind of OOM killer. | S489 | `The number of processes belonging to this cgroup killed by any kind of OOM killer.` |
| The first usage line prints usage, limit and failcnt in that order, with usage and limit converted to kB. | S490 | `pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",` |
| On a cgroup v2 hierarchy the printed failcnt comes from the MEMCG_MAX event counter, not from a per-page charge failure count. | S490 | `if (cgroup_subsys_on_dfl(memory_cgrp_subsys)) memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]); else memory_failcnt = memcg->memory.failcnt;` |
| A second line reports swap usage, limit and failcnt on cgroup v2, so the block carries two usage lines. | S490 | `pr_info("swap: usage %llukB, limit %llukB, failcnt %lu\n",` |
| The stats block is filled by memory_stat_format and printed at KERN_INFO, so its lines reach the kernel log like any other message. | S490 | `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_buf_do_printk(&s, KERN_INFO);` |
| The memory.stat file is produced by the same memory_stat_format call, so the file and the block write their keys through one formatter. | S490 | `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_puts(m, buf);` |
| When no cgroup is named the OOM context prints global_oom instead of a cgroup path, marking a system-wide kill. | S490 | `if (memcg) { pr_cont(",oom_memcg="); pr_cont_cgroup_path(memcg->css.cgroup); } else pr_cont(",global_oom");` |
| A second label on the same line records the victim's own memory cgroup path, next to the OOM cgroup path. | S490 | `if (p) { pr_cont(",task_memcg="); pr_cont_cgroup_path(task_cgroup(p, memory_cgrp_id)); }` |
| A group kill announces itself with its own line naming every task in the cgroup as about to be killed. | S490 | `pr_info("Tasks in "); pr_cont_cgroup_path(memcg->css.cgroup); pr_cont(" are going to be killed due to memory.oom.group set\n");` |
| The Killed process line carries total-vm, anon-rss, file-rss and shmem-rss in kB, plus pgtables and oom_score_adj. | S491 | `pr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n",` |
| The victim line's message prefix says whether the kill was global or a cgroup kill, choosing between two distinct strings. | S491 | `oom_kill_process(oc, !is_memcg_oom(oc) ? "Out of memory" : "Memory cgroup out of memory");` |
| A global OOM prints the system memory summary through __show_mem instead of the memcg stats block. | S491 | `if (is_memcg_oom(oc)) mem_cgroup_print_oom_meminfo(oc->memcg); else { __show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask));` |
| The oom-kill summary and stats block are rate-limited while the victim line is not, so a burst of kills can print victims without a block. | S491 | `if (__ratelimit(&oom_rs)) { dump_header(oc); dump_oom_victim(oc, victim); }` |
| The oom-kill context line records the constraint and nodemask before the victim name, pid and uid are appended. | S491 | `/* one line summary of the oom killer context. */ pr_info("oom-kill:constraint=%s,nodemask=%*pbl", oom_constraint_text[oc->constraint], nodemask_pr_args(oc->nodemask));` |
| The vm and memcg kill counters are incremented before the signal is sent, so the count predates the victim's death record. | S491 | `/* Raise event before sending signal: task reaper must see this */ count_vm_event(OOM_KILL); memcg_memory_event_mm(mm, MEMCG_OOM_KILL);` |
| The Tasks state table prints total_vm and rss in pages, unlike the kB victim line and the byte-valued stats block. | S491 | `pr_info("Tasks state (memory values in pages):\n"); pr_info("[ pid ] uid tgid total_vm rss rss_anon rss_file rss_shmem pgtables_bytes swapents oom_score_adj name\n");` |

## Reading rules

- Units are per line. The usage and swap lines print kB (`K()` converts from pages), the `Killed process` fields print kB,
  the `Tasks state (memory values in pages)` table prints pages, and the stats block prints bytes; convert before
  comparing a number from one line with a number from another.
- Read the block by key, not by position: the entries are ordered for humans and a newer kernel can insert a counter in
  the middle. The key set is also compile-time conditional — `zswap`, `zswapped`, `swapcached`, `anon_thp`, `file_thp`,
  `shmem_thp` and `hugetlb` are printed only under their CONFIG options, so a missing key is not a zero.
- `anon` is anonymous mappings, `file` is page cache including tmpfs and shared memory, and `shmem` is the swap-backed
  subset inside `file` (tmpfs, shm segments, shared anonymous mmap). Do not add `file` and `shmem`.
- `kernel` already contains `kernel_stack`, `pagetables`, `percpu`, `vmalloc` and `slab`, which are also printed on their
  own lines; summing every key double counts kernel memory.
- The block is the cgroup's charge, not the victim's. The victim's own `anon-rss`, `file-rss` and `shmem-rss` are on the
  `Killed process` line, and the cgroup over its limit and the victim's own cgroup are two different labels on the
  `oom-kill:` line; the source's NOTE on `mem_cgroup_print_oom_context` says they can differ when hierarchy is enabled.
- A group kill announces itself with `Tasks in <path> are going to be killed due to memory.oom.group set` and then
  prints one victim line per killed mm; `oom_kill` counts processes while `oom_group_kill` counts group events.
- What the block cannot tell: which process held which byte, whether the charge was a leak or one large allocation, or
  what caused the cgroup to grow. It reports state at the kill, not history.

## Limits

- Kernel v7.2 only, read from the frozen copies whose sha256 the counter pins; later kernels add or rename keys and can
  change the report path.
- cgroup v2 only. On a v1 hierarchy the same function prints `memory+swap` and `kmem` lines and a real per-page failcnt,
  which cgroup v2 does not have; nothing here carries over to v1.
- The summary is rate-limited (`if (__ratelimit(&oom_rs)) { dump_header(oc); dump_oom_victim(oc, victim); }`), but
  the victim line is printed outside that guard; a burst of kills can leave `Killed process` lines with no block at
  all, so a missing block is not evidence that the kill was global.
- The block is formatted into a static `SEQ_BUF_SIZE` buffer under `oom_lock`, and an overflow only prints a warning, so
  a truncated block is possible at event time.
- No host block was read. The lane's rule forbids reading kernel journal MESSAGE text for kill records, so this entry
  states what the kernel prints, not what any past kill on this host printed.
- A located quote proves the quoted words occur in the committed copy, not that the claim cell follows from them.

## Boundaries

- Detection and report only. Setting `memory.max`, `memory.oom.group` or `oom_score_adj` is tsukuroi's work; this entry
  licenses no configuration change.
- No remediation, and no attribution: a memcg OOM block names the cgroup that was charged, not what made it grow.
```

## Draft 2 — `corpus/SOURCES.md` rows S489–S491

Insert immediately after the `| S488 | ...` row (line 267 at the freeze, the last row of the registry table); the
`## Leads` section and the append-only correction blocks follow it. `status=mined`, `opened=2026-10-26`, `used-by` = the
entry path, one frozen-source URL per row. S491's URL is shared with S003 and S476 by design — the contract names that a
W04 warning, not an error.

```
| S489 | Control Group v2 (v7.2) — https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html | docs | A | cgroup v2 memory interface: memory.current, memory.stat keys and units, memory.events fields, memory.oom.group | Memory Interface Files; memory.stat; memory.events; memory.oom.group | A memcg OOM block's composition is the memory.stat breakdown, whose keys are looked up by name rather than position and are conditional on kernel configuration. | mined | 2026-10-26 | on-release | corpus/knowledge/oom-memcg-stat-r50.md |
| S490 | Linux mm/memcontrol.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c | code | A | the memcg OOM report path: usage/limit/failcnt lines, the Memory cgroup stats block, and the formatter shared with memory.stat | mm/memcontrol.c:1546-1608,1693-1748,1751,1770,1787-1830,4905-4919; tag v7.2 | The OOM report and the memory.stat file share memory_stat_format, and on cgroup v2 the printed failcnt is the MEMCG_MAX event counter, not a per-page charge count. | mined | 2026-10-26 | on-release | corpus/knowledge/oom-memcg-stat-r50.md |
| S491 | Linux mm/oom_kill.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | code | A | the OOM victim record and the memcg-versus-global report split (dump_header, __show_mem, the Killed process line) | mm/oom_kill.c:400-410,424-431,444-454,456-469,912-951,1169-1170; tag v7.2 | The Killed process line carries the victim's own counters in kB, and a global OOM prints __show_mem where a memcg OOM prints the stats block. | mined | 2026-10-26 | on-release | corpus/knowledge/oom-memcg-stat-r50.md |
```

Each row is 11 cells (checked with the counter's own `split_cells`: `len == 11` for all three; `sources_row` reads
`status=mined` and the opened date for each).

## Corrections to the staged candidates (candidates only; nothing reused)

- `scope-charge-fields-r46.md`: the tmpfs hypothesis is stated as a fact about "the sandbox the fleet's runner builds",
  grounded in S534 own-work notes outside this lane; the r47 candidate refutes it for its own host block (`file 0`,
  `shmem 0`). Neither the hypothesis nor the refutation is adopted: the entry states only what the documentation and the
  code say about which bucket a tmpfs page lands in.
- `scope-charge-fields-r46.md` `recheck:` writes its fetched page to `/tmp/cg72.html`. Operator directive 2026-10-25: a
  `/tmp` path is never evidence. The entry's `recheck:` streams each URL through `sha256sum` and stores nothing.
- `scope-composition-in-the-block-r47.md` `recheck:` runs `journalctl -k ... | grep -m1 -A80 'invoked oom-killer'`, i.e.
  it reads kernel log MESSAGE text around a kill record; the lane rule (S351/QUALITY 15) forbids that class of read. Its
  numbers come from S539 notes outside the lane. Not adopted; this entry contains no host block.
- Both candidates lack a claim/source/quote table, which is why the frozen `C2=unmet` controls fail them on
  `table`/`claims_floor`/`source_rows`. This draft keeps their useful insight (the block is the composition) and adds the
  table the predicate measures.
- `scope-composition-in-the-block-r47.md` says the block "carries the scope's usage and limit (S534) and the victim's own
  fields". The usage/limit line and the victim line are separate prints and the block itself carries neither; the entry
  keeps them apart (rows 8, 16, 18).

## Out of scope / not done

- The entry was not written into `corpus/knowledge/`, and `corpus/SOURCES.md` was not edited — the L1 integrates both
  drafts (and must pick one entry draft if a sibling scribe's is also landed).
- `C2=met` was observed only on fixture revs; the claim's landing rev does not exist, so nothing here scores the claim.
- No host OOM block was read, no `journalctl`, no kernel MESSAGE grep, no cgroup limit touched, no systemd state changed.
- No tool was installed or upgraded (nothing was needed); no pacman transaction was run.
- Scratch `/fast/scratch/hyaku/mori-r50/Mo50ScribeEntryA` (one `git archive` extraction, six fixture commits) has been
  removed.

## Findings

- **LOW — `corpus/knowledge/oom-memcg-stat-r50.md` (Limits, 3rd bullet), source `mm/oom_kill.c:1030-1033`:** the summary
  and the stats block sit inside `if (__ratelimit(&oom_rs))` while `__oom_kill_process` — the `Killed process` line — is
  outside it. A burst of kills can therefore leave victim lines with no block and no `oom-kill:` line, so "no block" must
  be read as unknown, not as "global OOM". The entry states this (row 19 and the Limits bullet); any detector built on
  this entry must not invert it.
- **LOW — `corpus/knowledge/oom-memcg-stat-r50.md` (row 9), source `memcontrol.c:1801-1806`:** the printed `failcnt` on a
  cgroup v2 hierarchy is `memory_events[MEMCG_MAX]`, not a per-page charge-failure counter; a reader who takes the label
  at face value will overstate what the number counts.
- **LOW — `corpus/knowledge/oom-memcg-stat-r50.md` (Limits, 4th bullet), source `memcontrol.c:1756-1760`:** the block is
  formatted into a static `SEQ_BUF_SIZE` buffer and an overflow only warns, so a truncated block is possible at event
  time. `located=22` proves the quoted words exist in the copies, not that a given kill printed the whole key set.
- **LOW — `corpus/SOURCES.md` S491 (draft row):** same URL as S003 and S476 with a different scope. Contract calls this a
  W04 warning, not an error; the round-end census will report it again unless the scope cell is read with the row.
- **MED — `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/scope-charge-fields-r46.md`
  (`recheck:` line; "The sandbox the fleet's runner builds mounts fresh tmpfs on `/tmp` and `/run`" paragraph):** it grounds
  a fleet-runner fact in own-work notes outside the lane and writes its fixture to `/tmp`. Both are inadmissible under the
  operator's scratch directive and the lane's source rule; it must not be landed as-is.
- **MED — `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/scope-composition-in-the-block-r47.md`
  (`recheck:` line):** the command reads kernel journal MESSAGE text around `invoked oom-killer`, which the lane rule
  (S351/QUALITY 15) forbids; its composition numbers are S539 own-work from outside the lane. Landing it would put a
  forbidden read in a registry `recheck` cell.
- **LOW — both staged candidates:** no claim/source/quote table, so their `C2` failure is `table` + `claims_floor` +
  `source_rows` before any content is judged.
- **INFO — sibling drafts:** `Mo50ScribeEntryB.md` (independent entry draft) and `Mo50ScribeRowOomKill.md` (S491 row draft)
  exist in this same wave and overlap this report's drafts. No factual conflict found on the points I checked: EntryB also
  reads the v2 `failcnt` as the max event counter and also notes the rate-limit guard. The L1 must land exactly one entry
  and one row per id; the counters are byte-pinned per commit, so a doubled row would fail `sources_row`/duplicate checks.
