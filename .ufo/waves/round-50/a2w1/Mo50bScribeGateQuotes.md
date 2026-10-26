# Mo50bScribeGateQuotes — lesson Gate lines for S489, S490, S491

Seat: `Mo50bScribeGateQuotes` (leaf, wave a2w1, mori round 50 attempt 2). Task: the `## Gate` lines for the three
new rows of the landed data commit, in the house shape of `corpus/lessons/round-49.md`.

- Lane repo read at HEAD `4548a34dc8b4072abaa4335c1f54a9efcfcc314a`; data commit
  `487941b9395e89678af0053cc443cdb49cdee6e3` (ancestor of HEAD, `merge-base --is-ancestor` exit 0).
- Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bScribeGateQuotes/` with `TMPDIR` inside it; removed at the end
  (the receipts below are pasted here first).
- Read-only throughout: no edit outside this report; no git/jj mutation; no pacman; no host change; no
  subagent. No tool install or upgrade was needed (no version to record).

## What was checked

1. The three committed copies at the landed revision and in the working tree carry the sha256 the freeze
   pins (`evidence/freeze-sha256.txt`).
2. Each of the three URLs was fetched today with `curl` into scratch; the live bytes were hashed and compared
   with the copy (`sha256sum` and `cmp -s`).
3. One verbatim span per row was tested as a substring of the committed copy after whitespace collapse
   (for S489, also under `count-c2.py`'s HTML normalisation: script/style/comment blocks dropped, tags
   stripped, entities decoded, whitespace collapsed — `count-c2.py:63-80`).

## Receipts (commands, output, exit codes)

Fetch, 2026-10-26 (host clock `2026-10-26T09:44:02-03:00`):

```
$ curl -sSL --max-time 60 -A '<UA>' -o live-cgroup-v2.html -w '%{http_code}' https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html
URL https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html -> HTTP 200 curl_rc=0 bytes=168438
$ ... https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c
URL https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c -> HTTP 200 curl_rc=0 bytes=160768
$ ... https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c
URL https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c -> HTTP 200 curl_rc=0 bytes=34311
```

Hashes and comparison (all rc 0):

```
$ sha256sum live-*
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  .../live-cgroup-v2.html
8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e  .../live-memcontrol.c
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  .../live-oom_kill.c
$ sha256sum corpus/evidence/sources-r50/*
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  .../cgroup-v2.7.2.html
8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e  .../memcontrol.c.v7.2
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  .../oom_kill.c.v7.2
$ for f in cgroup-v2.7.2.html memcontrol.c.v7.2 oom_kill.c.v7.2; do git -C <lane> show 487941b9:corpus/evidence/sources-r50/$f | sha256sum; done
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  -
8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e  -
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  -
$ cmp -s live-<file> corpus/evidence/sources-r50/<file>
cgroup-v2 cmp rc=0
memcontrol cmp rc=0
oom_kill cmp rc=0
```

The three live fetches are byte-identical to the committed copies, and the copies are identical at the
landed revision `487941b9`, at HEAD `4548a34d` and in the working tree. The copies were not re-frozen this
seat; the point of the comparison is that today's URL bytes equal the frozen bytes.

Quote test (`python3 quote-test.py` in scratch, exit 0):

```
S489 cgroup-v2.7.2.html words=17 occurrences_after_normalise=2 PASS
S490 memcontrol.c.v7.2 words=9 occurrences_after_normalise=1 PASS
S491 oom_kill.c.v7.2 words=12 occurrences_after_normalise=1 PASS
rc=0
```

The same spans were also tested against the raw bytes under plain whitespace collapse only (no tag strip):
S489 2x, S490 1x, S491 1x — i.e. each quote survives both normalisations.

## Gate lines (fenced; house shape of `corpus/lessons/round-49.md` `## Gate`)

```markdown
| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S489 | https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html — copy `cgroup-v2.7.2.html`; re-fetched 2026-10-26, live sha256 `2d716cb7…` = copy (`cmp -s` rc 0) | 2026-10-26 | "The entries are ordered to be human readable, and new entries can show up in the middle." (17 words) — §Memory Interface Files, `memory.stat` entry, copy lines 1398-1399 | admit, mined, kind docs, tier A scoped to the memory interface files (memory.current, `memory.stat` keys and units, memory.events fields, memory.oom.group), recheck on-release |
| S490 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c — copy `memcontrol.c.v7.2`; re-fetched 2026-10-26, live sha256 `8a28e0bc…` = copy (`cmp -s` rc 0) | 2026-10-26 | "if (cgroup_subsys_on_dfl(memory_cgrp_subsys)) memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]); else memory_failcnt = memcg->memory.failcnt;" (9 words) — `mem_cgroup_print_oom_meminfo()`, copy lines 1800-1803 | admit, mined, kind code, tier A for tag v7.2 only, recheck on-release |
| S491 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c — copy `oom_kill.c.v7.2`; re-fetched 2026-10-26, live sha256 `452f1348…` = copy (`cmp -s` rc 0) | 2026-10-26 | `pr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n",` (12 words) — copy line 945, arguments at lines 946-951, in `oom_kill_process()` | admit, mined, kind code, tier A for tag v7.2, recheck on-release; same URL as S003 and S476 with a different scope (census W04 warning, not E04) |
```

Full sha256, in the order of the rows: `2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34`,
`8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e`,
`452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`.

Two format notes for the integrator: (a) the decision cells above are **proposals** mirroring the committed
SOURCES row's own columns (kind `docs`/`code`, tier `A`, `mined`, opened `2026-10-26`, recheck `on-release`,
`used-by corpus/knowledge/oom-memcg-stat-r50.md`, cells `[2]`,`[3]`,`[7]`,`[8]`,`[9]`,`[10]` of lines
268-270); the verdict is the L1's. (b) The S491 span carries internal double quotes, so the cell wraps it in
backticks; if the lesson's quote column must be double-quoted for every row, use the S491 alternate below or
escape the inner quotes.

## Alternates that also locate (same test, both normalisations)

| row | span | words | location in the copy |
|---|---|---|---|
| S489 | "All memory amounts are in bytes." | 6 | line 1397, `memory.stat` entry (same sentence also at 1599 under `memory.numa_stat`) |
| S489 | "All memory amounts are in bytes. If a value which is not aligned to PAGE_SIZE is written," | 17 | line 1194, §Memory Interface Files intro (this is the span the C2 entry uses for its first row) |
| S489 | "Don’t rely on items remaining in a fixed position; use the keys to look up specific values!" | 17 | lines 1399-1400, `memory.stat` entry (also 1605-1606 under `memory.numa_stat`) |
| S490 | `/* The actual unit of the state item, not the same as the output unit */` | 16 | line 1611 |
| S490 | `pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",` | 7 | line 1805 |
| S490 | `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_puts(m, buf);` | 7 | lines 4913-4915, the `memory.stat` show path (inside the row's listed range 4905-4919) |
| S491 | `if (is_memcg_oom(oc)) mem_cgroup_print_oom_meminfo(oc->memcg); else { __show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask));` | 8 | lines 465-468, in `dump_header()` |
| S491 | `oom_kill_process(oc, !is_memcg_oom(oc) ? "Out of memory" : "Memory cgroup out of memory");` | 12 | lines 1168-1170 |
| S491 | `pr_info("Tasks state (memory values in pages):\n");` | 6 | line 424 |

Each alternate returned 1 occurrence after normalisation except the two S489 `memory.stat`/`numa_stat`
sentences, which returned 2 (one per file section). All spans were verified against the committed copy only;
the live copies are byte-identical, so they hold there too.

## Limits

- A located quote proves the words occur in the committed copy, not that the row's `teaches` follows from
  them (the same limit the contract names for C2).
- S489's primary quote states the ordering/name-lookup rule; it does not by itself show the OOM block's
  composition. The `memory.stat` key meanings sit elsewhere in the same entry (copy lines 1411 onward) and in
  the C2 entry's S489 rows.
- S490/S491 quotes are code at tag v7.2 only; they say nothing about other kernels or cgroup v1.
- The `docs.kernel.org/7.2` page was byte-stable today, but it is a rendered page: a byte change is possible
  without a content change (footer/build metadata), so the recheck is a hash comparison, not a diff review.
- No host artefact was read for any of this (lane rule: no kernel-log MESSAGE text).

## Touched surfaces

- Written: `.ufo/waves/round-50/a2w1/Mo50bScribeGateQuotes.md` (this file) only.
- Read: the three committed copies, `corpus/SOURCES.md` lines 268-270, `corpus/knowledge/oom-memcg-stat-r50.md`,
  `corpus/lessons/round-49.md`, `.ufo/waves/round-50/contract.md`, `.ufo/waves/round-50/evidence/freeze-sha256.txt`,
  `.ufo/waves/round-50/count-c2.py:40-95`.
- Scratch `/fast/scratch/hyaku/mori-r50/Mo50bScribeGateQuotes/` removed at the end; no files left in `/tmp`.

## Findings

- **LOW** — `corpus/evidence/sources-r50/cgroup-v2.7.2.html:1398-1399,1604-1605`: the S489 ordering sentence
  occurs twice in one copy (under `memory.stat` and under `memory.numa_stat`). A Gate/entry location that says
  only "§Memory" or gives no line numbers cannot say which key's rule is quoted; the line carries the entry
  name and both line ranges so the reader can tell.
- **LOW** — `corpus/evidence/sources-r50/cgroup-v2.7.2.html:1194,1397,1599`: "All memory amounts are in bytes."
  appears at 1194 (generic §Memory Interface Files intro), 1397 (`memory.stat`) and 1599 (`memory.numa_stat`).
  The C2 entry's first row locates the intro occurrence; that is a true occurrence, but a reader checking the
  `memory.stat` key units will land on line 1397/1599 instead. No claim is wrong; the location word "unit" in
  row S489's scope should be read against 1397.
- **LOW** — Gate-table format: the S491 span `pr_err("%s: Killed process …` contains internal double quotes.
  If the lesson table's quote column is uniformly double-quoted, this row needs backticks or escapes, or the
  S491 alternate at lines 465-468 (no internal quotes) swaps in cleanly.
- **LOW** — `corpus/SOURCES.md:270` (S491) and the census: the URL occurs 3x (`grep -cF` → 3, rc 0; S003,
  S476, S491). The row text already declares this, so the expected census effect is one W04 warning and no
  E04; the Gate decision cell repeats it so the round-end census line can be read without going back to the
  contract.
