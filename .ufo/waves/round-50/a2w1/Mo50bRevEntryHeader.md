# Mo50bRevEntryHeader — header + intro review of `corpus/knowledge/oom-memcg-stat-r50.md` at 487941b9

MACHINE_ID: 432d02b544a5459ebbff9c42ec68334d-plazir27

mori round 50 attempt 2, wave a2w1. Scope: lines 1–16 of the entry (title, the three `source:` lines vs SOURCES
rows S489–S491, `verified-at:`, the `recheck:` command and its stated expected digests, `coverage-map: FR1` vs
`corpus/README.md`) and the intro paragraph (lines 10–15), sentence by sentence, against the frozen copies
`corpus/evidence/sources-r50/memcontrol.c.v7.2` and `corpus/evidence/sources-r50/oom_kill.c.v7.2`
(`mem_cgroup_print_oom_context`, `dump_header` and their neighbors, with line numbers). The claims table and the
Reading rules / Limits / Boundaries sections are other seats' scope; I touch them only where an intro claim rests
on them.

Method (all read-only; no repo, index or jj mutation; no tool installed — none needed):

- Bytes reviewed: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 487941b9395e89678af0053cc443cdb49cdee6e3:corpus/knowledge/oom-memcg-stat-r50.md`
  (83 lines), and the same for `corpus/SOURCES.md`, `corpus/README.md` and `.ufo/waves/round-50/evidence/freeze-sha256.txt`,
  extracted into scratch. HEAD had already moved to 4548a34dc8b4072abaa4335c1f54a9efcfcc314a, so the commit blob, not the
  worktree, is the review target.
- Copy freshness: `git diff --stat 487941b9395e89678af0053cc443cdb49cdee6e3 HEAD -- corpus/` → empty, and
  `sha256sum corpus/evidence/sources-r50/*` → `2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34`
  (cgroup-v2.7.2.html), `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e` (memcontrol.c.v7.2),
  `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` (oom_kill.c.v7.2) — all three equal the
  `freeze-sha256.txt` lines. The worktree copies are byte-identical to the frozen ones, so every line number cited
  below is a frozen-copy line number.
- Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bRevEntryHeader/` with `TMPDIR` under it, removed at the end.
  `disk-guard.sh status` before starting: `/fast/scratch/hyaku` at 24% use, 613.1G free — no ENOSPC risk.

## Verdicts, lines 1–16

### Line 1 — title — LOW, replacement offered

`# A memcg OOM prints its charge three ways: usage line, stats block, victim line`

"its charge three ways" overclaims for the third item. The `Killed process` line prints the victim's own counters
(oom_kill.c.v7.2:945-950 — total-vm, anon-rss, file-rss, shmem-rss, UID, pgtables, oom_score_adj), and the entry's
own intro (lines 11-12) calls them "the victim's own counters", not the charge. The first two items do print the
cgroup's charge (usage/limit line memcontrol.c.v7.2:1805-1807; stats block 1824-1829). Suggested replacements
(either):

```
# A memcg OOM prints its charge twice and its victim once: usage line, stats block, victim line
```

```
# A memcg OOM prints three records: a usage/limit line, a stats block, and a victim line
```

### Line 3 — `source: S489` — OK

Matches SOURCES.md row S489 (line 268 of the blob): same URL `https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html`,
docs, tier A, access date 2026-10-26, used-by names `corpus/knowledge/oom-memcg-stat-r50.md`, copy sha256
`2d716cb7…` matches. The parenthetical "(memory interface files, memory.events, memory.oom.group)" is a fair
summary of the row's scope cell ("cgroup v2 memory interface at kernel 7.2: memory.current, memory.stat keys and
units, memory.events fields, memory.oom.group; not the kernel print formats (S490, S491) and not any host's values").

### Line 4 — `source: S490` — OK

Row S490 (line 269): same URL `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c`, code, tier A,
2026-10-26, used-by this entry, copy sha256 `8a28e0bc…` matches. The row's cited ranges check out against the copy:
1546-1608 is the `memory_stats[]` key table the formatter walks; 1751 `memory_stat_format`; 1770
`mem_cgroup_print_oom_context`; 1787-1830 `mem_cgroup_print_oom_meminfo`; 4905-4919 `memory_stat_show`.

### Line 5 — `source: S491` — OK

Row S491 (line 270): same URL `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c`, code, tier A,
2026-10-26, used-by this entry, copy sha256 `452f1348…` matches; "same URL as S003 and S476 with a different scope"
is the row's own wording. Cited ranges verified: 444-454 `dump_oom_victim`; 456-469(+) `dump_header`; 912-951
`__oom_kill_process` (the `Killed process` pr_err at 945); 1169-1170 the message choice; 400-410 and 424-431 are
`dump_task`'s row printer and `dump_tasks`' header — present as cited.

### Line 6 — `verified-at: 2026-10-26` — OK

Equals the three rows' access date and the recheck's "ran 2026-10-26"; today is 2026-10-26.

### Line 7 — `recheck:` — OK, VERIFIED live

Command run exactly as written (TMPDIR in scratch), 2026-10-26:

```
$ for u in https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c; do curl -fsSL "$u" | sha256sum; done
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  -
8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e  -
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  -
exit=0
```

All three digests equal the stated expected digests, in the stated order, and equal the committed copies' sha256
and the `freeze-sha256.txt` lines. The "90d" cadence matches peer entries (`census-cgroup-levels-r45.md:5`,
`conform-source-order-r42.md:6`).

### Line 8 — `coverage-map: FR1` — OK, one integration observation

`corpus/README.md:341` (blob at 487941b9) carries the FR1 row "Kernel OOM event-time attribution and fleet
correlation"; the entry documents exactly that event-time print surface, so the map fits. The bare form
`coverage-map: FR1` is precedented (`oom-evidence-loss-r38.md:13`).

Observation (LOW, L1 integration item, not an entry defect): the README blob at 487941b9 contains no round-50 note
registering this entry under FR1 (`grep -n 'oom-memcg-stat-r50|round-50|r50'` over the blob → 0 hits). Prior rounds
append a dated frontier note at closure (README.md:624+ round 43, :672+ round 48, :681+ round 49 in the same blob).
The L1 should append the round-50 FR1 note when integrating.

## Intro paragraph, sentence by sentence (lines 10–15)

### S1 — line 10 — OK; LOW optional wording

"mori attributes a kill at event time: which cgroup was over its charge, what that cgroup held, and which process
died."

Framing; each fact is carried by prints verified under S2/S3. Wording nit: "was over its charge" — the charge is
the usage itself, so being "over" it is odd; the kernel's own doc comment says "The memory cgroup that went over
limit" (memcontrol.c.v7.2:1764). Optional:

```
mori attributes a kill at event time: which cgroup went over its limit, what that cgroup held, and which process died.
```

### S2 — lines 11-12 — OK; two LOW optional sharpenings

"A memcg OOM prints all three in one burst: a usage/limit line, a `Memory cgroup stats for <path>:` block written
by the same formatter that writes memory.stat, and a per-victim `Killed process` line carrying the victim's own
counters."

Every component verified:

- usage/limit line: `pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n", …)` memcontrol.c.v7.2:1805-1807.
- `Memory cgroup stats for <path>:` header: memcontrol.c.v7.2:1824-1826 (`pr_info("Memory cgroup stats for ")` +
  `pr_cont_cgroup_path(memcg->css.cgroup)` + `pr_cont(":")`).
- same formatter as memory.stat: `memory_stat_format` called at 1828 (block) and at 4914 inside `memory_stat_show`
  (4905-4915), which is the `stat` file's seq_show (5053-5054).
- per-victim `Killed process` line with the victim's own counters: oom_kill.c.v7.2:945-950, printed by
  `__oom_kill_process`; one line per victim (chosen victim at 1042; one per group member via
  `oom_kill_memcg_member` at 1003).
- "in one burst": `dump_header` (usage line + stats block) and `dump_oom_victim` (the `oom-kill:` line) print under
  the ratelimit guard oom_kill.c.v7.2:1030-1033; the `Killed process` line prints at 1042 immediately after,
  outside the guard. All three print within one kill.

Optional sharpenings (LOW): (a) the usage line also carries failcnt (1805); "usage/limit line" is shorthand —
table row 8 states it fully; (b) "all three in one burst" is unconditional while the first two prints are
rate-limited (1030-1033) and the third is not — the Limits section carries exactly this, so the intro is
acceptable as a summary; a qualified variant:

```
A memcg OOM prints all three in one burst when the report is not rate-limited: a usage/limit/failcnt line, a
`Memory cgroup stats for <path>:` block written by the same formatter that writes memory.stat, and a per-victim
`Killed process` line carrying the victim's own counters.
```

Completeness note (no replacement needed): the burst also contains the `oom-kill:constraint=…,oom_memcg=…` context
line (oom_kill.c.v7.2:447-453), which the three-item list does not name; the table (rows 13, 14, 20) and the
Reading rules cover it.

### S3 — lines 13-14 — OK; LOW optional precision

"A global OOM prints a system-wide memory summary in place of that block and names no charged scope, so its burst
cannot place the charge in a cgroup."

Verified:

- system-wide summary: `dump_header`'s else-branch `__show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask,
  gfp_zone(oc->gfp_mask))` oom_kill.c.v7.2:467-468 (plus conditional `dump_unreclaimable_slab` 469-470).
- names no charged scope: `mem_cgroup_print_oom_context` (called at oom_kill.c.v7.2:451) prints `,oom_memcg=<path>`
  only when memcg is non-NULL, else `,global_oom` (memcontrol.c.v7.2:1774-1778); on a global OOM no charged-scope
  path appears anywhere in the burst (the Tasks state rows print no cgroup paths, oom_kill.c.v7.2:404-410).

Optional precision (LOW): "in place of that block" understates — on a global OOM the usage/limit line is absent
too (the whole `mem_cgroup_print_oom_meminfo` call is skipped, oom_kill.c.v7.2:465-468). Also note the global
burst still names the victim's own cgroup as `task_memcg=<path>` (memcontrol.c.v7.2:1779-1782) — not a charged
scope; the Reading rules bullet already distinguishes the two labels, but a detector grepping `memcg=` could
misread it. Optional replacement:

```
A global OOM prints a system-wide memory summary in place of the memcg report (usage line, swap line and stats
block) and names no charged scope — no `oom_memcg=` label; the victim's own cgroup still appears as `task_memcg=`
— so its burst cannot place the charge in a cgroup.
```

### S4 — line 15 — OK

"That difference is the detection rule this entry serves: a stats block means the kill was charged to a scope."

Verified as a one-directional rule: within the frozen copies, `Memory cgroup stats for` is printed only by
`mem_cgroup_print_oom_meminfo` (memcontrol.c.v7.2:1824), whose only call site is `dump_header`'s `is_memcg_oom`
branch (oom_kill.c.v7.2:465-466; grep over both copies finds no other caller — the other `dump_header` call sites
at 1075 and 1158 branch the same way inside the function). So observing the block entails a memcg OOM, and the
block's own header names the charged path (1824-1826). The converse (no block ⇏ global) is not claimed here and is
correctly carried by the Limits section (rate-limit); the direction stated is the direction the code supports.

Named limit: `mem_cgroup_print_oom_meminfo` is a non-static export, so this review excludes a caller outside the
two frozen copies only; the entry's Limits already scope the entry to v7.2-as-copied.

## Receipts

- Recheck run: command, output and exit 0 above, 2026-10-26.
- Copy digests: `sha256sum corpus/evidence/sources-r50/*` → `2d716cb7…`, `8a28e0bc…`, `452f1348…` =
  `freeze-sha256.txt` lines.
- Corpus unchanged 487941b9 → HEAD 4548a34d (`git diff --stat` empty), so worktree line numbers = frozen line
  numbers.
- No tool installed or upgraded. No repo, index or jj mutation. No host journal or kernel-log read. Scratch
  removed at end.
- UNVERIFIED: none within this seat's scope. Out of scope, left to the row-reopening seats: the semantic fit of
  each table row's quote to its surrounding S489 HTML text (the contract's named limit assigns that to wave-2 row
  review); the S489 copy was verified byte-identical to the live page via the recheck, not read line-by-line here.

## Findings

- LOW — `corpus/knowledge/oom-memcg-stat-r50.md:1` (title): "prints its charge three ways" — the victim line
  prints the victim's own counters (oom_kill.c.v7.2:945-950), not the cgroup's charge; the intro itself says "the
  victim's own counters" (line 12). Fenced replacements above.
- LOW — `corpus/knowledge/oom-memcg-stat-r50.md:10`: "which cgroup was over its charge" — kernel phrasing is "went
  over limit" (memcontrol.c.v7.2:1764); optional replacement above.
- LOW — `corpus/knowledge/oom-memcg-stat-r50.md:11-12`: "all three in one burst" unqualified while the usage line
  and stats block are rate-limited (oom_kill.c.v7.2:1030-1033) and the victim line is not (1042 → 945); the Limits
  section carries the exception, so this is a summary-precision nit; optional replacement above. Also "usage/limit
  line" omits the failcnt the line carries (memcontrol.c.v7.2:1805).
- LOW — `corpus/knowledge/oom-memcg-stat-r50.md:13`: "in place of that block" understates — the usage/limit line is
  absent on a global OOM too (oom_kill.c.v7.2:465-468); optional replacement above. Related misread risk: the
  global burst still prints `task_memcg=<path>` (memcontrol.c.v7.2:1779-1782); covered by the Reading rules, noted
  here for detectors.
- LOW (integration observation, not an entry defect) — `corpus/README.md` at 487941b9 has no round-50 note
  registering the entry under FR1; prior-round practice appends a dated note at closure (README.md:624+, :672+,
  :681+). L1 to append at integration.
- No HIGH, no MED. All counter-unchecked header facts (source lines vs rows, verified-at, recheck digests,
  coverage-map) verified correct; every intro claim is grounded in the frozen copies at the cited lines.
