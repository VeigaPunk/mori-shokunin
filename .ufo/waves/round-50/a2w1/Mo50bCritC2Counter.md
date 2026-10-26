# Mo50bCritC2Counter — attack on `count-c2.py` (mori round 50, attempt 2, wave a2w1)

Seat: critic. Target: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c2.py`.
Landed data under test: `487941b9395e89678af0053cc443cdb49cdee6e3` (L1 MoriR50a2). Lane repo read-only throughout
(`git show` / `git rev-parse` only; no index, worktree, jj or fleet write). No tool installed, no pacman call.

## 1. Target bytes are the frozen bytes

```
$ sha256sum /fast/scratch/hyaku/mori-r50/Mo50bCritC2Counter/count-c2.py \
            /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c2.py
533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d  .../Mo50bCritC2Counter/count-c2.py
533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d  .../round-50/count-c2.py
```
`evidence/freeze-sha256.txt:17` carries the same digest, so the file I attacked is the frozen predicate's counter.
I imported the *scratch copy* with `sys.dont_write_bytecode = True`, so nothing was written into
`.ufo/waves/round-50/` (its `__pycache__` is untouched by this seat).

## 2. Method

`evaluate(read, "R")` was called directly via `importlib`, with a dict-backed `read`:

* the three copy paths → the committed copy bytes, read from the lane working tree and decoded exactly as the
  counter's own `selftest()` does (`open(..., "rb").read().decode("utf-8", "surrogateescape")`), so `pins=ok`
  and `norm[url]` are the counter's own normalised texts;
* `corpus/knowledge/oom-memcg-stat-r50.md` → a synthetic entry;
* `corpus/SOURCES.md` → three synthetic 11-column rows (`| S489 | title — <url> | docs | A | scope | anchor |
  teaches | mined | 2026-10-26 | 180d | corpus/knowledge/oom-memcg-stat-r50.md |`), one per frozen URL.

Every junk quote below was produced **by token-slicing the counter's own `normalise`/`normalise_text` output**, so
`q in norm[url]` holds by construction and the counter's only remaining job would be to notice the quote is junk.
Harness (scratch, deleted): `attack.py`, `attack2.py`; `python3 attack2.py` → rc 0.

## 3. Classes that print `C2=met` with no depth (10 rows each; D and E in full below, F/G/N by their
class-defining rows, each entry's printed line exact)

| class | printed line | met |
|---|---|---|
| D claim = quote + 3 filler words | `C2=met claims=10 located=10 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=R` | yes |
| E claim contradicts its quote (rows 1 and 2 contradict **each other**) | same `met` line | yes |
| F quote spans two C functions | same `met` line | yes |
| G quote starts mid-word (substring, not word boundary) | same `met` line | yes |
| N claim is three nonsense words + filler | same `met` line | yes |
| H substantive claims, 100% boilerplate quotes | same `met` line | yes |

Exact bytes, class D (`beyond=3` exactly, the floor, on every row):

```
| Amount of memory used to cache filesystem data, including zqx vjy kwp | S489 | `Amount of memory used to cache filesystem data, including` |
| Amount of cached filesystem data that is swap-backed, such as zqx vjy kwp | S489 | `Amount of cached filesystem data that is swap-backed, such as` |
| Amount of memory used for storing per-cpu kernel data structures. sock zqx vjy kwp | S489 | `Amount of memory used for storing per-cpu kernel data structures. sock` |
| All memory amounts are in bytes. zqx vjy kwp | S489 | `All memory amounts are in bytes.` |
| pr_info("Memory cgroup stats for "); pr_cont_cgroup_path(memcg->css.cgroup); pr_cont(":"); seq_buf_init(&s, zqx vjy kwp | S490 | `pr_info("Memory cgroup stats for "); pr_cont_cgroup_path(memcg->css.cgroup); pr_cont(":"); seq_buf_init(&s,` |
| memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]); else memory_failcnt = memcg->memory.failcnt; zqx vjy kwp | S490 | `memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]); else memory_failcnt = memcg->memory.failcnt;` |
| memory_stat_format(struct mem_cgroup *memcg, struct seq_buf *s) { zqx vjy kwp | S490 | `memory_stat_format(struct mem_cgroup *memcg, struct seq_buf *s) {` |
| Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u zqx vjy kwp | S491 | `Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u` |
| static void dump_header(struct oom_control *oc) { pr_warn("%s invoked zqx vjy kwp | S491 | `static void dump_header(struct oom_control *oc) { pr_warn("%s invoked` |
| mem_cgroup_print_oom_meminfo(oc->memcg); else { __show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask)); if (should_dump_unreclaim_slab()) zqx vjy kwp | S491 | `mem_cgroup_print_oom_meminfo(oc->memcg); else { __show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask)); if (should_dump_unreclaim_slab())` |
```

Class E (each claim asserts the opposite of its quote; rows 1 and 2 are the same fact with opposite polarity):

```
| memory.stat amounts are printed in kilobytes and never in bytes | S489 | `All memory amounts are in bytes.` |
| memory.stat amounts are printed in bytes and never in kilobytes | S489 | `All memory amounts are in bytes. If` |
| the memcg OOM report prints no memory cgroup stats block | S490 | `pr_info("Memory cgroup stats for "); pr_cont_cgroup_path(memcg->css.cgroup); pr_cont(":"); seq_buf_init(&s,` |
| kernel memory is excluded from the per-cgroup stat breakdown | S489 | `Amount of memory used for storing per-cpu kernel data structures. sock` |
| the failcnt line counts per-page charge failures, not events | S490 | `memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]); else memory_failcnt = memcg->memory.failcnt;` |
| a global OOM prints the memcg stats block instead of show_mem | S491 | `mem_cgroup_print_oom_meminfo(oc->memcg); else { __show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask)); if (should_dump_unreclaim_slab())` |
| the victim line reports bytes and omits the process identifier | S491 | `Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u` |
| tmpfs and shared memory are never counted in the file key | S489 | `Amount of cached filesystem data that is swap-backed, such as` |
| memory.stat keys are positional and their order is stable | S489 | `A read-only flat-keyed file which exists on non-root cgroups.` |
| the report block uses a different formatter than memory.stat | S490 | `memory_stat_format(struct mem_cgroup *memcg, struct seq_buf *s) {` |
```

Class F (the quote leaves one function and enters the next signature; both locate):

```
| the boundary between two functions is described as one paragraph | S491 | `mem_cgroup_print_oom_context(oc->memcg, victim); pr_cont(",task=%s,pid=%d,uid=%d\n", victim->comm, victim->pid, from_kuid(&init_user_ns, task_uid(victim))); } static void dump_header(struct oom_control` |
| the closing braces of a helper read as part of the next signature | S490 | `seq_buf_printf(s, "%s %lu\n", vm_event_name(memcg_vm_event_stat[i]), memcg_events(memcg, memcg_vm_event_stat[i])); } } static void memory_stat_format(struct mem_cgroup` |
```

Class G (mid-word starts; `q.strip()` does not demand a word boundary):

```
| the quoted words begin inside a different word | S489 | `lat-keyed file which exists on non-root cgroups. The following entries` |
| the quoted words begin inside the unit of the mapping bucket | S489 | `unt of memory used in anonymous mappings such as brk() , sbrk()` |
| the quoted words begin inside the controller name | S490 | `emcontrol.c - Memory Controller * * Copyright IBM Corporation` |
```

Class N (the claim cell is not prose at all):

```
| qzx0 vjy0 kwp0 aa bb cc | S489 | `All memory amounts are in bytes.` |
| qzx1 vjy1 kwp1 aa bb cc | S489 | `Amount of memory used to cache filesystem data, including` |
| qzx2 vjy2 kwp2 aa bb cc | S489 | `A read-only flat-keyed file which exists on non-root cgroups.` |
... (10 rows, one per quote, same shape)
```

## 4. The headline counterexample — substantive claims carried entirely by boilerplate

1612 bytes, prints `C2=met claims=10 located=10 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok
provenance=ok rev=R`:

```
# junk

source: S489 S490 S491
verified-at: 2026-10-26
recheck: 180d — `curl -s <url> | grep -c memory.stat`

## Claims

| claim | source | quote |
|---|---|---|
| the usage, limit and failcnt line is printed before the stats block | S489 | `Control Group v2 — The Linux Kernel documentation` |
| the stats block is produced by the same formatter as the file | S489 | `The Linux Kernel 7.2.0 Quick search Contents Development` |
| the block lists anon, file, shmem and kernel with their units | S489 | `Quick search Contents Development process Submitting patches Code` |
| a global OOM prints show_mem output instead of the stats block | S489 | `Contents Development process Submitting patches Code of conduct Maintainer handbook` |
| the victim line carries kB-rounded counters and the process name | S490 | `memcontrol.c - Memory Controller * * Copyright IBM Corporation, 2007 * Author Balbir Singh` |
| memory.stat keys are looked up by name, not by column position | S490 | `Copyright IBM Corporation, 2007 * Author Balbir Singh <balbir@linux.vnet.ibm.com>` |
| the printed failcnt is the MEMCG_MAX event counter on cgroup v2 | S490 | `Copyright 2007 OpenVZ SWsoft Inc * Author: Pavel Emelianov` |
| tmpfs and shared memory are charged to the file key, not separately | S491 | `Thanks go out to Claus Fischer for some` |
| print_oom_meminfo emits one line per memory.stat key plus the header | S491 | `// SPDX-License-Identifier: GPL-2.0-only /* * linux/mm/oom_kill.c` |
| the memcg block and show_mem never appear in the same dump | S491 | `The routines in this file are used to kill a process when` |
```

Ten subject-matter claims, ten boilerplate quotes (HTML `<title>`, sidebar, global toctree, footer; C SPDX lines and
copyright blocks), and the predicate says `met`. `count-c2.py:181` (`if q in norm[url]`) is the whole test: it asks
whether the words occur *anywhere* in the copy, and page chrome occurs there.

## 5. Classes whose every row locates but which are stopped only by the copy floor

`MIN_SOURCES = 3` is met by the number of distinct **URLs** that carry at least one located quote, so a class drawn
from one or two copies fails only on `sources_floor` — the class itself is never examined:

| class | rows | printed line |
|---|---|---|
| A C comment / SPDX / copyright text | 10 (5 memcontrol.c, 5 oom_kill.c) | `C2=unmet claims=10 located=10 quote_missing=0 bad_rows=0 sources=2 source_rows=ok pins=ok provenance=ok rev=R failed=sources_floor` |
| B HTML title / sidebar / toctree / footer | 10 | `C2=unmet claims=10 located=10 quote_missing=0 bad_rows=0 sources=1 source_rows=ok pins=ok provenance=ok rev=R failed=sources_floor` |
| C 10 adjacent 6-word slices of one paragraph | 10 | `C2=unmet claims=10 located=10 quote_missing=0 bad_rows=0 sources=1 source_rows=ok pins=ok provenance=ok rev=R failed=sources_floor` |

Quotes, class A (all `located`):

```
`memcontrol.c - Memory Controller * * Copyright IBM Corporation, 2007 * Author Balbir Singh`
`Copyright IBM Corporation, 2007 * Author Balbir Singh <balbir@linux.vnet.ibm.com>`
`Copyright 2007 OpenVZ SWsoft Inc * Author: Pavel Emelianov`
`Memory thresholds * Copyright (C) 2009 Nokia Corporation * Author: Kirill`
`Kernel Memory Controller * Copyright (C) 2012 Parallels Inc. and Google`
`// SPDX-License-Identifier: GPL-2.0-or-later /* memcontrol.c -`
`// SPDX-License-Identifier: GPL-2.0-only /* * linux/mm/oom_kill.c`
`Copyright (C) 1998,2000 Rik van Riel * Thanks go out to`
`Thanks go out to Claus Fischer for some`
`The routines in this file are used to kill a process when`
```

Quotes, class B (all `located`; not one byte of these exists in the copy — see §7):

```
`Control Group v2 — The Linux Kernel documentation`
`The Linux Kernel 7.2.0 Quick search Contents`
`Quick search Contents Development process Submitting patches Code`
`Contents Development process Submitting patches Code of conduct Maintainer handbook`
`All development-process docs Core API Driver APIs Subsystems Locking`
`Subsystems Locking Licensing rules Writing documentation Development tools Testing`
`Core-kernel subsystems Control Group v2 Control Groups version 1`
`Memory Management Kernel module signing facility Namespaces Numa policy hit/miss`
`kernel development community. | Powered by Sphinx 5.3.0`
`©The kernel development community. | Powered by Sphinx 5.3.0 & Alabaster 0.7.16`
```

Quotes, class C — ten overlapping windows of **one** paragraph, each 6 words, each a distinct row:

```
`Amount of memory used to cache`
`of memory used to cache filesystem`
`memory used to cache filesystem data,`
`used to cache filesystem data, including`
`to cache filesystem data, including tmpfs`
`cache filesystem data, including tmpfs and`
`filesystem data, including tmpfs and shared`
`data, including tmpfs and shared memory.`
`including tmpfs and shared memory. kernel`
`tmpfs and shared memory. kernel (npn)`
```

One paragraph therefore yields ten "distinct" claims; adding one row from each of the other two copies lifts the
entry to `met` (measured: the earlier 13-row variant printed `C2=met claims=13 located=13 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=R`).

## 6. What the counter does catch (contrast probes, same harness)

```
altered quote (one word changed)
C2=unmet claims=10 located=9 quote_missing=1 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=R failed=quote_missing
quote from the wrong copy
C2=unmet claims=10 located=9 quote_missing=1 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=R failed=quote_missing
5-word quote
C2=unmet claims=10 located=9 quote_missing=0 bad_rows=1 sources=3 source_rows=bad pins=ok provenance=ok rev=R failed=bad_rows,source_rows
claim echoes its quote
C2=unmet claims=10 located=9 quote_missing=0 bad_rows=1 sources=3 source_rows=bad pins=ok provenance=ok rev=R failed=bad_rows,source_rows
same quote in two rows
C2=unmet claims=10 located=9 quote_missing=0 bad_rows=1 sources=3 source_rows=bad pins=ok provenance=ok rev=R failed=bad_rows,source_rows
one registry row status=queued
C2=unmet claims=10 located=6 quote_missing=0 bad_rows=4 sources=2 source_rows=bad pins=ok provenance=ok rev=R failed=bad_rows,source_rows,sources_floor
used-by cell not the entry path
C2=unmet claims=10 located=0 quote_missing=0 bad_rows=10 sources=0 source_rows=bad pins=ok provenance=ok rev=R failed=bad_rows,source_rows,sources_floor
one copy byte changed (pin)
C2=unmet claims=10 located=10 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=bad provenance=ok rev=R failed=pins
```

So the counter is sound against quote substitution, wrong-copy attribution, size/duplication/echo, registry status,
`used-by`, and the pins. It is blind to *what* the quote is (§3–§4).

## 7. Local-evidence test on the landed entry (`487941b`)

The decisive question is not whether junk *can* score `met` (it can, §4) but whether the landing *uses* it.

```
$ python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3
EXIT=0
```

Measured with the counter's own `parse_claims`, `words_beyond`, `normalise`:

* 22 rows, quote length 7–21 words (`MIN_WORDS..MAX_WORDS` = 6..25); no row at the 6-word minimum.
* `words_beyond` per row: min 5, max 19, **none at the 3 floor** → no filler-padded claim.
* No row's quote lies in the HTML nav region (first 1300 collapsed chars), the HTML footer (last 320 chars) or the
  C licence headers (first 1000 chars of each) → no row of class A or B.
* Pairwise 5-gram overlap: only two pairs touch, each by 1–2 grams, and each pair is two distinct facts, not slices:
  rows 7/9 are the `memory:` line vs the `swap:` line (`... usage %llukB, limit %llukB, failcnt ...` shared), and
  rows 10/11 are `... memory_stat_format(memcg, &s); seq_buf_do_printk(&s, KERN_INFO);` vs
  `... seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_puts(m, buf);` — the same call with
  two different sinks, which is exactly the shared-formatter claim the entry makes. Adjacent 6-word slices share a
  5-gram by construction; these pairs are 7–21-word spans around one shared call, not slices.
* No quote contains `} static` or a brace-then-identifier boundary. The code rows that quote a brace quote one
  statement: rows 12, 13 and 18 are complete `if (...) { ... }` spans, row 17 is an `if/else` that ends inside its
  `else { __show_mem(...);` branch (unclosed brace, still one function, not a two-function span).

**Result: the landing is clean of every junk class in §3–§5. These are named limits of the frozen predicate, not a
defect in C2's data.** No row needs rewriting on this ground.

## 8. Impacts

* **depth (C2)** — the predicate certifies "≥10 distinct 6–25-word spans from the three committed copies, each paired
  with a distinct ≥6-word claim adding ≥3 words"; it does not certify that the spans are about the memcg block. The
  gap is real but unexercised here.
* **calibration (C1)** — untouched (separable; this seat touched no self-assessment file).
* **adjacency, coverage, operability, freshness** — untouched.
* Receipt precision, all observed in the printed fields: `claims` is `len(rows)` before validation
  (`count-c2.py:139`), so a padded table inflates it (harmless when `met`, because then `claims == located`);
  `source_rows=ok` is `bool(ids_in_table and not bad)` (`:199`), so it reports row validity as well as registry
  soundness; `sources=N` counts URLs, and S491 shares its URL with S003/S476 (the W04 warning), so `sources=3` means
  three copies, not three documents.
* Byte-level provenance: HTML copies are tag-stripped and entity-decoded, so a located quote need not occur as bytes.
  Observed: `grep -c 'Control Group v2 — The Linux Kernel documentation' cgroup-v2.7.2.html` → `0`; the raw title is
  `<title>Control Group v2 &#8212; The Linux Kernel  documentation</title>`; `grep -c 'Quick search Contents
  Development process'` on the copy → `0`, while the same phrase is present once in the counter's `normalise` output.

## 9. Named limits to add for C2 (draft text for the L1)

```
- a located quote only proves the words occur in the copy: page chrome (title, sidebar, global toctree, footer) and
  file chrome (SPDX line, copyright block) locate as readily as subject-matter text, a quote may begin mid-word, and
  a quote may cross a function boundary; ten overlapping 6-word windows of one paragraph are ten accepted claims,
  and a claim that is its own quote plus three arbitrary words clears the beyond-word floor;
- because HTML copies are tag-stripped and entity-decoded, a located quote need not occur as bytes in the copy.
```

## 10. Smallest safe correction

1. **Data:** none. The landing at `487941b` is clean of all classes measured here; no row rewrite is justified.
2. **One clause that is not carried by its own quote (LOW, no rewrite needed):** row 7 (S490) claims "with usage and
   limit converted to kB". The quote `pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",` shows the
   `%llukB` format, and the code next to it wraps each argument in `K(...)` (`memcontrol.c:1805-1807`:
   `K((u64)page_counter_read(&memcg->memory)), K((u64)READ_ONCE(memcg->memory.max)), memory_failcnt`). The
   definition of `K` is in no committed copy (`grep -n "define K(" corpus/evidence/sources-r50/memcontrol.c.v7.2
   corpus/evidence/sources-r50/oom_kill.c.v7.2` → rc 1), so the conversion to kB is plausible from the copy, not
   provable from it. This is the contract's own named limit ("not entailment") applied once; wave-2 row reviewers
   re-open every row, and this is the one row where the context beyond the quote matters.
3. **Report:** carry the §9 limits wording so the receipt is not read as proof of subject matter. Counters and
   predicates stay frozen; excluding boilerplate would be a round-51 counter change, not a fix for this round.

## 11. Scratch and hygiene

Scratch `/fast/scratch/hyaku/mori-r50/Mo50bCritC2Counter/` (96K: the counter copy, `attack.py`, `attack2.py`, the
saved entries and a `tmp/` with `TMPDIR` exported), removed after the run:

```
$ du -sh /fast/scratch/hyaku/mori-r50/Mo50bCritC2Counter   -> 96K
$ rm -rf -- /fast/scratch/hyaku/mori-r50/Mo50bCritC2Counter -> rc 0; test ! -e -> absent
```

Everything cited above is copied into this report before that removal. No clone was made (the three copies were read
in place from the lane working tree); no fleet/lane/index/jj write; no pacman, no install. `/fast/scratch/hyaku` was
at 24% use (613.5G free) before the run, and `disk-guard.sh status` was read first.

## Findings

1. **MED** — `count-c2.py:181` (`if q in norm[url]`): boilerplate locates. A 10-row entry whose claims are all about
   the memcg block and whose quotes are all `<title>`/sidebar/toctree/footer or SPDX/copyright lines prints
   `C2=met claims=10 located=10 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=R`
   (full 1612-byte entry in §4). Not exercised by `487941b`.
2. **MED** — `count-c2.py:181`: the located test is substring, not word-boundary, so a quote may begin mid-word
   (`lat-keyed file which exists on non-root cgroups…`, `unt of memory used in anonymous mappings…`) and still print
   `met`.
3. **MED** — `count-c2.py:181`: a quote crossing a function boundary (…`); } static void dump_header(struct
   oom_control`) locates and passes `met`.
4. **MED** — `count-c2.py:65` + `:160` (`words_beyond`, `MIN_BEYOND = 3`): a claim that is its own quote plus
   `zqx vjy kwp` passes with `beyond=3` on every row, and a claim cell of `qzx0 vjy0 kwp0 aa bb cc` passes; ten such
   rows print `met` with `sources=3`.
5. **MED** — `count-c2.py:154-164` (quote/claim uniqueness): ten overlapping 6-word windows of one paragraph are ten
   distinct quotes and ten distinct claims; the entry prints `met` as soon as one row is drawn from each other copy,
   so one paragraph plus two licence lines can satisfy a "10 claims" depth floor.
6. **LOW** — `count-c2.py:70-77` (`normalise`) + `:181`: tags stripped and entities decoded, so a located quote need
   not be byte-present in the copy (`—` quote: `grep -c` → 0; nav phrase: bytes 0, rendered 1).
7. **LOW** — `count-c2.py:139`: printed `claims` is the parsed row count before validation, so it counts invalid rows;
   sound only because `met` implies `bad_rows=0`.
8. **LOW** — `count-c2.py:199`: `source_rows=ok` mixes registry soundness with row validity (a single short quote
   makes it `bad` while the registry rows are fine).
9. **LOW** — landed row 7 (`corpus/knowledge/oom-memcg-stat-r50.md`, S490): "with usage and limit converted to kB"
   is carried by `memcontrol.c:1805-1807` (`K(...)` around each argument), not by the quoted `pr_info` line, and
   `K`'s definition is in no committed copy; no rewrite required.
10. **INFO** — `487941b`: the landed entry uses none of the classes above (22 rows, quotes 7–21 words, `beyond`
    5–19 with none at the floor, no chrome/comment quote, no slice overlap); `count-c2.py` prints `met`, exit 0.
    The counterexample falsifies the predicate's reach, not this landing.
