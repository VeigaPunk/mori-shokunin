# Mo50ScribeRowMemcontrol — SOURCES.md row S490 (Linux mm/memcontrol.c at tag v7.2)

Seat: `Mo50ScribeRowMemcontrol` (scribe, leaf). Author date: 2026-10-26T06:05-0300.
Lane tip read: `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379` (round-50 freeze; its parent
`7197160b927f04db294c9553fb48fadcc7a3f4e3` is the entering tip named by the contract). Nothing in the
lane was edited, staged, committed, moved or re-indexed by this seat; no mutating `git` or `jj`
command ran, `pacman` was not invoked, and no subagent was spawned.

## Behavior

Deliver, inside this report only: one 11-column `corpus/SOURCES.md` registry row `S490` for
`Linux mm/memcontrol.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c`,
one `## Gate` line for it, and a grounded statement of why its scope differs from `S004`
(`corpus/SOURCES.md:10`). Drafts below; the L1 integrates.

The row's source cell carries the literal URL that the round-50 C2 counter keys on
(`.ufo/waves/round-50/count-c2.py` `COPIES`:
`https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c` →
`corpus/evidence/sources-r50/memcontrol.c.v7.2`, sha256 `8a28e0bc…4041fd5e`). `S490` is a free id at
the freeze: `git show HEAD:corpus/SOURCES.md | grep -c '^| S'` = `261` rows, maximum id `S488`, and no
row `S489`/`S490`/`S491` exists yet (those are this wave's three row seats). The v7.2 `memcontrol.c`
URL occurs 0 times in the registry at HEAD, so this row cannot produce a `W04` duplicate-URL warning.

## Draft — row S490 (one physical line; 11 columns; no `|` inside any cell)

```markdown
| S490 | Linux mm/memcontrol.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c | code | A | the memcg OOM report block only: the usage, limit and failcnt lines mem_cgroup_print_oom_meminfo prints in the kill report, the Memory cgroup stats for <path>: block it emits, and the memory_stat_format formatter that both that block and the memory.stat file handler call; not the OOM context path labels or the memory.events display (S004), not the victim fields or the global OOM __show_mem block (S491), not what any live host printed | mm/memcontrol.c:1791-1830 mem_cgroup_print_oom_meminfo, 1800-1803 failcnt source, 1805-1807 memory usage limit failcnt line, 1809-1812 swap line, 1824-1826 stats header and path, 1828 formatter call, 1829 print; 1751-1759 memory_stat_format, shared with 4905-4918 memory_stat_show (call 4914); 1546 memory_stats table, 1693 memcg_stat_format key order; caller mm/oom_kill.c:466; committed copy corpus/evidence/sources-r50/memcontrol.c.v7.2 sha256 8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e, 6068 lines; live fetch byte-identical 2026-10-26 | The OOM block reuses memory_stat_format, so every line under the stats header maps to the memory.stat key table rather than to a separate OOM schema, and usage and limit carry a kB suffix through K() while failcnt stays a bare count. | mined | 2026-10-26 | on-release | corpus/knowledge/oom-memcg-stat-r50.md |
```

Shape of that line as written: 1444 bytes, 12 `|` characters (the 11 cells' delimiters, none inside a
cell), 0 tabs, 0 backticks, one line. `count-c2.py`'s own `split_cells` returned 11 cells (see
evidence 8).

## Cell-by-cell justification

| column | value | grounding (read from the committed copy, never from a staged note) |
|---|---|---|
| id | `S490` | the id the frozen contract assigns ("New rows: … S490 (memcontrol.c at tag v7.2)"); unused at HEAD (max `S488`) |
| source | `Linux mm/memcontrol.c at tag v7.2 — <v7.2 raw URL>` | `corpus/evidence/sources-r50/memcontrol.c.v7.2` is tracked at HEAD and hashes to the C2 pin `8a28e0bc…4041fd5e` (evidence 1, 3) |
| kind | `code` | it is C source; the registry enum precedent is `S003`/`S004`/`S481` (`code`) |
| tier | `A` | primary upstream source, byte-pinned by sha256 and re-fetched against the live tag |
| scope | the memcg OOM report block and the formatter it shares | functions `mem_cgroup_print_oom_meminfo` (1791-1830) and `memory_stat_format` (1751-1759), the latter called from both 1828 and 4914 |
| anchor | function names + line numbers in the copy | every number below is an `awk`-numbered line read from the copy, listed in evidence 7 |
| teaches | one benefit: block ≡ memory.stat formatter | `memory_stat_format(memcg, &s);` at 1828 inside the OOM block and at 4914 inside `memory_stat_show` (4905-4918); the `%llukB` formats at 1805 and 1809 are fed through `K(...)` at 1806-1807/1810-1811, while `failcnt` is `%lu` |
| status | `mined` | the counter requires `mined` for a row cited by the round entry |
| opened | `2026-10-26` | the counter's `OPENED` constant; the date the copy was fetched and hashed |
| recheck | `on-release` | kptr-style cadence the lane uses for tag-pinned code rows (`S003`, `S004`) |
| used-by | `corpus/knowledge/oom-memcg-stat-r50.md` | the one entry this wave admits (contract C2 surface); the path does not exist yet — the entry is another seat's draft (finding 2) |

Anchor cell, line by line, all verified against `corpus/evidence/sources-r50/memcontrol.c.v7.2`:

- `1791-1830` `void mem_cgroup_print_oom_meminfo(struct mem_cgroup *memcg)` — the whole block.
- `1800-1803` the `failcnt` source: `cgroup_subsys_on_dfl` → `memory_events[MEMCG_MAX]`, else
  `memcg->memory.failcnt`.
- `1805-1807` `pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n", …)`.
- `1809-1812` `pr_info("swap: usage %llukB, limit %llukB, failcnt %lu\n", …)` (v2 path); v1
  alternatives `1815-1820` under `CONFIG_MEMCG_V1`.
- `1824-1826` `pr_info("Memory cgroup stats for "); pr_cont_cgroup_path(memcg->css.cgroup); pr_cont(":");`.
- `1828` / `1829` `memory_stat_format(memcg, &s);` / `seq_buf_do_printk(&s, KERN_INFO);`.
- `1751-1759` `static void memory_stat_format(...)`, dispatching `memcg_stat_format` (v2) or
  `memcg1_stat_format` (v1) and warning on buffer overflow at 1757-1758.
- `4905-4918` `int memory_stat_show(...)`, calling the same formatter at `4914`.
- `1546` the `memory_stats[]` key table; `1693` `memcg_stat_format` (v2 key order comment at 1697-1703).
- `mm/oom_kill.c:466` `mem_cgroup_print_oom_meminfo(oc->memcg);` — the caller, in the S491 copy.

## Draft — Gate-block line (house shape: `corpus/lessons/round-47.md` `## Gate`)

```markdown
| S490 | `curl -sS -m 120 -o live-memcontrol.c -w 'http=%{http_code} size=%{size_download}\n' https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c` → `http=200 size=160768`, then `sha256sum` and `cmp -s` against the frozen copy `corpus/evidence/sources-r50/memcontrol.c.v7.2` (sha256 `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e`, 6068 lines) | 2026-10-26 | "memory: usage %llukB, limit %llukB, failcnt %lu\n" — 7 words, `corpus/evidence/sources-r50/memcontrol.c.v7.2:1805` (`mem_cgroup_print_oom_meminfo` 1791-1830; the format string is line 1805, its `K(...)` arguments 1806-1807) | admit, mined |
```

The gate quote is the `pr_info` format string of the first report line, i.e. the sentence the block
adds to the kernel log before the `Memory cgroup stats for <path>:` header: located character-for-
character in the committed copy at line 1805 (evidence 8) and in the bytes served by the live URL
(same bytes, evidence 5). It introduces no host path, no MACHINE_ID and no kill record.

## Why S490 and S004 have different scopes

`S004` (`corpus/SOURCES.md:10`) is the same file at a *different document*, and it answers a different
question. Grounded line map, master `c03c1a14507dfaf8b856c2608f9ac216021fc222` (fetched 2026-10-26,
sha256 `bdb6159c…bcc41a1`, 6218 lines) versus tag `v7.2` (6068 lines):

| object | S004 anchor (master) | same object in v7.2 | drift |
|---|---|---|---|
| `pr_cont(",oom_memcg=")` | 1820 | 1775 | −45 |
| `pr_cont(",task_memcg=")` | 1825 | 1780 | −45 |
| `oom_kill` counter line (`__memory_events_show`) | 4965-4966 | 4881-4882 | −84 |
| `mem_cgroup_print_oom_meminfo` (function head) | 1836 | 1791 | −45 |
| `Memory cgroup stats for ` | 1869 | 1824 | −45 |
| `memory_stat_format` (function head) | 1796 | 1751 | −45 |
| `memory_stat_show` | 4989 | 4905 | −84 |

So the scopes differ on three counts, and none of them is a preference:

1. **Different revision.** `S004` cites an unpinned-by-tag master commit (`c03c1a14…`, dated
   2026-10-18) and its bytes change as master moves; `S489`-`S491` are tag `v7.2` documents whose bytes
   are frozen with sha256 in this lane. Anchors do not transfer between the two: the same functions sit
   45 to 84 lines apart (table above).
2. **Different objects.** `S004` covers the *path labels* `mem_cgroup_print_oom_context` appends to the
   OOM header (`,oom_memcg=` / `,task_memcg=`) and the `memory.events` display; `S490` covers the
   *numbers and the block* `mem_cgroup_print_oom_meminfo` prints after them (usage/limit/failcnt, the
   swap sibling, `Memory cgroup stats for <path>:`) and the `memory_stat_format` formatter that block
   shares with the `memory.stat` file handler. A reader quoting S004 learns which cgroup path a line
   belongs to; a reader quoting S490 learns which keys, in which order and which units, the block's
   body carries.
3. **Different learner use.** `S004`'s teaches cell is about attributing a line to a cgroup at event
   time; `S490`'s is about mapping the block's body onto the `memory.stat` key table so the body is not
   mistaken for a separate OOM-only schema. Merging them would make one row carry two flips across two
   revisions, and the C2 counter's quote cell (one source, one URL, one copy) could no longer locate a
   quote in a single frozen document.

The boundary is stated in the row's scope cell: S004 for the context path labels and the events
display, S491 for the `oom_kill.c` victim/global-`__show_mem` side, S490 for the meminfo block and the
shared formatter. Overlap is nil; adjacency is the point.

## Verified quote candidates for the S490 half of the entry (helper, not the entry)

Each span was located with the frozen counter's own `normalise_text` on the committed copy and then
pinned to a raw line; each is unique in that copy and inside the 6-25-word window
(`count-c2.py` `MIN_WORDS`/`MAX_WORDS`). Offered so the entry seat does not have to re-derive them;
the entry seat still owns the claim cells and the beyond-quote word floor.

| quote (backticked span to use in the entry) | words | line | what it supports |
|---|---|---|---|
| `"memory: usage %llukB, limit %llukB, failcnt %lu\n"` | 7 | 1805 | the `memory:` line, its three fields and its kB/`%lu` units |
| `pr_info("Memory cgroup stats for "); pr_cont_cgroup_path(memcg->css.cgroup);` | 6 | 1824-1825 | the block header names the cgroup path |
| `if (cgroup_subsys_on_dfl(memory_cgrp_subsys)) memcg_stat_format(memcg, s); else memcg1_stat_format(memcg, s);` | 12 | 1753-1756 | v2 (`memory.stat`) versus v1 formatter choice |
| `if (seq_buf_has_overflowed(s)) pr_warn("%s: Warning, stat buffer overflow, please report\n", __func__);` | 10 | 1757-1758 | the block is bounded by a fixed buffer and warns instead of truncating silently |
| `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_buf_do_printk(&s, KERN_INFO);` | 7 | 1827-1829 | the OOM block's emit path |
| `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_puts(m, buf);` | 7 | 4913-4915 | the `memory.stat` file path over the same formatter |

(The third span is 12 words because `cgroup_subsys_on_dfl` and `memcg_stat_format` are single tokens;
it stays inside the 25-word ceiling.)

## Evidence (command → output → exit code)

1. `sha256sum corpus/evidence/sources-r50/memcontrol.c.v7.2` →
   `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e` — rc 0. Equals the frozen pin in
   `evidence/freeze-sha256.txt` and the C2 `COPIES` pin.
2. `git rev-parse HEAD` → `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`; `git rev-parse HEAD^` →
   `7197160b927f04db294c9553fb48fadcc7a3f4e3`; `git log --oneline -3` → `950e99be round-50: freeze — …`,
   `7197160b hyaku run 7 interrupted: …`, `2023465f round-49 verifier spot-check …` — rc 0 each.
3. `git ls-files --error-unmatch corpus/evidence/sources-r50/memcontrol.c.v7.2` → path printed, rc 0
   (tracked); `git show HEAD:corpus/evidence/sources-r50/memcontrol.c.v7.2 | sha256sum` → the same
   digest as item 1, rc 0 (committed bytes equal working-tree bytes).
4. `wc -l corpus/evidence/sources-r50/memcontrol.c.v7.2` → `6068` — rc 0.
5. Live fetch of the row's URL (2026-10-26):
   `curl -sS -m 120 -o live-memcontrol.c -w 'http=%{http_code} size=%{size_download}\n' https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c`
   → `http=200 size=160768`, rc 0; `sha256sum live-memcontrol.c` →
   `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e`; `cmp -s live-memcontrol.c
   corpus/evidence/sources-r50/memcontrol.c.v7.2` → `BYTE_IDENTICAL` (no diff bytes).
6. `S004` comparison fetch: same `curl` shape against
   `https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/mm/memcontrol.c`
   → `http=200 size=165998`, rc 0; sha256 `bdb6159cc2378c44c356b6788f521812f15c4d4936e8b09c66ef70b56bcc41a1`;
   `wc -l` → `6218`; `awk 'NR>=1810 && NR<=1829'` shows `1820: pr_cont(",oom_memcg=")` and
   `1825: pr_cont(",task_memcg=")`; `awk 'NR>=4958 && NR<=4966'` shows `4965: seq_printf(m, "oom_kill %lu\n",`
   / `4966: atomic_long_read(&events[MEMCG_OOM_KILL]));`; `grep -n` on that file gives
   `1796:static void memory_stat_format`, `1836:void mem_cgroup_print_oom_meminfo`,
   `1869: pr_info("Memory cgroup stats for ");`, `4989:int memory_stat_show`, `4998` the formatter call.
   Written only inside the seat scratch directory.
7. Line anchors in the S490 copy: `awk 'NR>=1791 && NR<=1831'` prints the block verbatim (function head
   1791, `lockdep_assert_held(&oom_lock);` 1798, failcnt 1800-1803, memory line 1805-1807, swap
   1809-1812, v1 siblings 1815-1820, header 1824-1826, formatter 1828, print 1829, close 1830);
   `grep -n` gives `1546:static const struct memory_stat memory_stats[] = {`,
   `1693:static void memcg_stat_format`, `1751:static void memory_stat_format`, `4905:int memory_stat_show`,
   `1560: { "anon", … }`, `1561: { "file", … }`, `1562: { "kernel", … }`, `1569: { "shmem", … }`;
   in the S491 copy `grep -n 'mem_cgroup_print_oom' corpus/evidence/sources-r50/oom_kill.c.v7.2` →
   `451: mem_cgroup_print_oom_context(oc->memcg, victim);`, `466: mem_cgroup_print_oom_meminfo(oc->memcg);`.
8. Frozen-counter structural check (counter imported read-only via `importlib`; no lane bytes written —
   the row text lived in scratch):
   - `split_cells(row)` → `cells 11`.
   - `sources_row(base + "\n" + row, "S490")` → 11 cells; URL loop binds
     `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c`;
     `status/opened/usedby: mined 2026-10-26 ['corpus/knowledge/oom-memcg-stat-r50.md']`;
     `row_ok True` (the exact conjunction `count-c2.py` tests: `len(srow)==11`, url bound,
     `srow[7]=="mined"`, `srow[8]=="2026-10-26"`, entry path among the `[,;]`-split used-by tokens).
   - gate quote: `normalise_text(copy)` contains the span; raw-line hit `[1805]`; `words 7`;
     present character-for-character in the committed line (`git show HEAD:… | sed -n '1805p'` →
     `\tpr_info("memory: usage %llukB, limit %llukB, failcnt %lu\\n",`).
   - all six helper quotes: `found=True`, word counts 6-12, first-token lines as tabled above.
9. SOURCES-CONTRACT-v1 census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
   --today 2026-10-26`), run on scratch copies only:
   - Base (`SOURCES.md` bytes as at HEAD) placed in a lane-shaped scratch mirror
     (`corpus/SOURCES.md` + symlinks to the lane's `corpus/lessons`, `corpus/evidence`, and the lane's
     root files the used-by column names) → rc `0`, `E 0`, `W 21` (the same 21 `W04` lines the frozen
     `evidence/census-start.txt` records).
   - Same mirror with the S490 row inserted after `S488` → rc `1`, `E 1`, `W 21`, `W` list byte-identical
     to base, and the one E line is
     `file\tE11\tS490 missing used-by corpus/knowledge/oom-memcg-stat-r50.md`. No `E01`-`E10`, no `E12`,
     no `W01`-`W03`, and **no new `W04`** (the v7.2 `memcontrol.c` URL is unique in the registry).
   - Adding an empty stub file at the mirror's `corpus/knowledge/oom-memcg-stat-r50.md` (scratch copy
     only, never the lane) → rc `0`, `E 0`.
   - Control for the E11 artefact: the same row validated straight from a plain scratch directory (no
     sibling tree) → rc `1` with 30+ `E11` lines for *pre-existing* rows (`S001`, `S002`, `S003`,
     `S076`, `S134`, …), i.e. `--file` resolves used-by against `dirname(file)/..`
     (`scripts/sources-census.sh:501`), so only the mirror run is informative.
10. Registry state at HEAD: `git show HEAD:corpus/SOURCES.md | grep -c '^| S'` → `261`;
    `S489`/`S490`/`S491` absent; maximum id `S488`; the v7.2 `memcontrol.c` URL occurs 0 times;
    `S004` at line 10 is the master-commit URL
    `…/c03c1a14507dfaf8b856c2608f9ac216021fc222/mm/memcontrol.c`; the v7.2 `oom_kill.c` URL occurs at
    lines 9 (`S003`) and 255 (`S476`) — the contract's expected `W04` for S491, not for S490.
11. `test -e corpus/knowledge/oom-memcg-stat-r50.md` → false: the entry is not landed (finding 2).
12. Disk guard before work: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` →
    `/tmp` 3% used / 125.2G free, `/var/tmp` 37% / 576.6G free, `/fast/scratch/hyaku` 28% / 580.3G free
    — rc 0; no ENOSPC encountered.

## Gates run (and their honest reach)

- **S490 ↔ P-C2 row requirements**: every row-level condition the counter tests was exercised through
  the counter's own parser — 11 cells, URL binding to the frozen copy, `mined`, `2026-10-26`, used-by
  splitting to exactly the entry path (`row_ok True`, evidence 8). The **end-to-end** `count-c2.py R`
  run is **UNVERIFIED at this seat**: the entry is not landed, so `claims=`, `located=` and `sources=`
  would measure a synthetic fixture, not the lane. A quote is only proof of occurrence inside a copy
  under the counter's own limit; my row supplies the copy and its hash, not entailment of the entry's
  claims.
- **SOURCES-CONTRACT-v1**: `NF=13` (11 columns), no `E01`-`E10`, no `E12`, no `W01`-`W04` attributable
  to S490; the sole E line is the not-yet-landed used-by target, and it clears when the stub exists
  (evidence 9).
- **Gate line reach**: `http=200`, byte-identical to the frozen copy, so the row's URL and the copy's
  sha256 describe the same bytes on 2026-10-26. This does not establish that tag `v7.2` will never be
  re-pointed (annotated-tag re-targeting is outside what a raw fetch observes); the lane's own sha256
  pin is what protects the entry from that.
- **Rule 1 (a row is a claim)**: every value in the row is read from the committed copy, the freeze
  manifest or the live fetch of the same URL. Nothing is copied from the staged r46/r47 entries.
- **Rule 2 (append-only)**: the draft is a new row; no existing id, status, recheck or used-by is
  changed. `S004` stays exactly as it is — the comparison above is explanatory, not an edit.
- **C1**: not touched by this seat (no `SCORECARD.md`, `SHONEN.md`, selftest receipt or counter read).

## Touched surfaces

- Written: this report (`.ufo/waves/round-50/w1/Mo50ScribeRowMemcontrol.md`) and scratch only.
- Scratch: `/fast/scratch/hyaku/mori-r50/Mo50ScribeRowMemcontrol/` (`tmp/` as `TMPDIR`,
  `live-memcontrol.c`, `master-memcontrol.c`, `row-s490.txt`, `SOURCES.base.md`, `SOURCES.row.md`,
  `mirror-lane/`); removed before this report was filed. Nothing cited above depends on a scratch file:
  every quoted byte is re-derivable from the committed copy.
- Not touched: `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/evidence/`, `tools/`,
  `scripts/sources-census.sh`, `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `LOG.md`, `QUALITY.md`, the
  frozen round-50 files (`contract.md`, `count-c1.py`, `count-c2.py`, `controls/`, `evidence/`,
  `assimilation/`), any sibling lane, the fleet repo, the lane's git index and jj state,
  `/home/vgpnk/Projects/shokuknow*` (not read at all by this seat).
- Tooling: no installs or upgrades, `pacman` not run (host-wide pause respected), no subagents.
- Host reads: none. No kernel log MESSAGE text was read or grepped; no cgroup limit was read or changed;
  no journal or systemctl command ran.

## Out-of-scope / not checked

- The entry `corpus/knowledge/oom-memcg-stat-r50.md` (claim cells, quote selection, provenance header) —
  another seat; I only verified that the two S490 quotes I offer are located in the copy.
- Rows `S489` (cgroup-v2 page) and `S491` (oom_kill.c) — other seats. I fetched master `memcontrol.c`
  only to compare with `S004`; no other remote document was opened.
- The `K()` macro's arithmetic: its definition is not in the copy, so the row says the values are
  formatted through `K()` with a `kB` suffix and does not assert the shift constant. **UNVERIFIED**
  beyond `include/linux/sizes.h`-style definition not present in this file.
- Whether `corpus/knowledge/oom-memcg-stat-r50.md` will take exactly that name: if it is renamed, this
  row's used-by and the entry's `source:` line must change together.
- Wave-2 style re-open of the block's surrounding commentary (which `memory.stat` keys the OOM block
  actually prints on this kernel build, e.g. `CONFIG_ZSWAP`-gated rows at 1553-1557): out of scope for
  a row seat.

## Findings

- **MED** — `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:501` (`dir_abs=$(realpath --
  "$(dirname -- "$file_abs")/..")`, feeding the E11 test at `:566-567`): in `--file` mode the census
  resolves every used-by target against the copy's *parent directory*, so validating a copy from a
  plain scratch directory reports `E11` for dozens of pre-existing rows (`S001`, `S002`, `S003`,
  `S076`, …) and cannot distinguish "entry not landed" from "copy placed in the wrong tree". Observed:
  30+ E11 lines in a bare scratch dir versus exactly one E11 in a lane-shaped mirror (evidence 9). Any
  scribe or reviewer quoting an E11 from a scratch `--file` run over-reports; the round-49 report's
  "E11 noise from the scratch root" was the same artefact.
- **LOW** — `corpus/SOURCES.md` (pending S490 row, anchor cell): its used-by
  `corpus/knowledge/oom-memcg-stat-r50.md` does not exist at HEAD `950e99be`, so the census stays
  `rc 1` with `E11 S490 missing used-by corpus/knowledge/oom-memcg-stat-r50.md` until the entry lands
  (evidence 9, 11). Not a defect in the row; a landing-order coupling between this seat and the entry
  seat, which must also keep the filename identical on both sides.
- **LOW** — `corpus/SOURCES.md:10` (`S004`): its anchors `1820,1825,4965-4966` are master-commit
  coordinates and do not locate the v7.2 copy — the same objects sit at `1775`, `1780` and `4881-4882`
  there (drift −45, −45, −84; evidence 6, 7). An entry or review that reuses an S004 anchor while
  citing S490 would point 45-84 lines off; the two rows must be cited with their own line numbers.
- **LOW** — `corpus/SOURCES.md:9` and `:255` (`S003`, `S476`): the v7.2 `oom_kill.c` URL is already
  present twice, which is why the contract expects S491 to add a `W04` duplicate-URL warning. S490's
  URL is unique, so it adds none (the 21 `W04` lines are byte-identical with and without the row) —
  but the L1 should not read a future `W04 S491` as a regression introduced by this wave.
- **LOW** — `corpus/evidence/sources-r50/memcontrol.c.v7.2:1805-1807`: the report line's fields are
  printed through `K()` with a `%llukB` label, so a reader who compares these numbers with
  `memory.current` (bytes) or with `memory.stat`'s byte-valued keys at `1560-1600` mixes units. The row
  states the unit and the conversion call, not the arithmetic (`K()`'s definition is outside the
  copy); the entry must keep the kB-versus-bytes distinction explicit.
