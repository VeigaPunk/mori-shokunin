# Mo61ScribePsi1 — C2 ledger rows for the `psi.rst` / `psi.c` pointers (round 61)

Seat: `Mo61ScribePsi1` · lane `mori-shokunin` · read-only scribe · no VCS mutation, no production file touched.

## Result

1. **41 of the 47 enumerated pointers are mine** (`psi.rst` 9, `psi.c` 32). The 6 remaining (`psi_types.h:41-49`,
   `cgroup-v2.rst:1066-1081`, `cgroup-v2.rst:1066-1087`, `Kconfig:730-731`, `Kconfig:743-760`,
   `kernel-parameters.txt:5505-5507`) belong to the sibling scribe seat.
2. **Every one of my 41 rows is `same`.** Proof, not reading: the lane already holds the v7.2 baselines as
   committed bytes, and the diff between the v7.2 baseline and the pinned v7.3 copy is **one line for `psi.c`
   and zero lines for `psi.rst`**. No pointer's words moved; no pointer's words changed. Each quote below was
   additionally re-checked to be present at the *same line range* in the v7.2 baseline and in the v7.3 copy.
3. **One real upstream drift exists and it is invisible to the ledger**: `psi.c:1026` changed
   `if (delta < 0)` → `if (delta <= 0)` between v7.2 and v7.3. No enumerated pointer covers line 1026, so no
   ledger row can carry it (finding F1).
4. **13 of my 41 rows cannot satisfy the frozen counter's ≥5-word quote floor**, and a 14th (`psi_types.h:41-49`,
   sibling slice) cannot either: 14 of 47 enumerated pointers are *structurally* blocked, because the range the
   pointer enumerates contains no line with five whitespace-separated tokens, and a ledger row is one physical
   line, so a quote cannot span the newline (finding F2, empirical receipt in F5).
   **The floor is the counter's own, not the contract's**: `contract.md:67` states the quote rule as
   "≤25 words, ≥8 distinct bytes, pairwise distinct" — no five-word floor. **All 41 of my rows satisfy the
   frozen contract's own quote rule in full**; the rule that rejects them exists only in `count-c2.py:151`.
   Amendments are barred and I may not propose a counter change, so this is filed as a report-only finding.
5. **Every other rule of the frozen counter passes on my rows.** With only the word floor relaxed in a
   scratch copy, the same 47 rows read `C2=met pointers=47 rows=47 same=47 moved=0 changed=0 quotes_ok=47
   spans_ok=47 sources=6 failed=none` (receipt F5).
6. **Six new `SOURCES.md` rows are mandatory** before C2 can read met: the `rows_src` check needs one line per
   cited copy carrying `corpus/evidence/sources-r61/<file>` + `| mined |` + the ledger entry name, and the
   existing v7.3 rows S529–S533 carry the r55 paths and the r55 ledger instead (finding F4). Two of the six
   are my slice's copies (`psi.rst`, `psi.c`).

## Method and exact evidence

Frozen contract: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/contract.md` (read first).
Frozen counter: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c2.py`
(sha256 `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8`, unchanged before and after my run).

```sh
# disk guard before heavy work
/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
#   /tmp 24% 97.5G free | /var/tmp 41% 533.9G free | /fast/scratch/hyaku 47% 433.0G free  -> green, no ENOSPC

# pointer enumeration (the counter's own function, imported from the frozen bytes)
python3 -c "import importlib.util;s=importlib.util.spec_from_file_location('c2','.ufo/waves/round-61/count-c2.py');\
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);\
p=m.enumerate_pointers(open('corpus/knowledge/system-pressure-r24.md',encoding='utf-8').read());\
print(len(p));print([x for x in p if x.startswith('psi.rst:') or x.startswith('psi.c:')])"
#   47
#   ['psi.rst:60-65', 'psi.c:342-360', 'psi.c:1268-1270', 'psi.c:1372-1373', 'psi.c:1379-1380', 'psi.c:1712',
#    'psi.c:1017', 'psi.c:1540', 'psi.c:1686', 'psi.rst:36-38', 'psi.c:1710-1721', 'psi.rst:40-43',
#    'psi.c:1290-1296', 'psi.rst:45-56', 'psi.rst:57-59', 'psi.c:1282-1288', 'psi.c:1284-1288',
#    'psi.c:160-164', 'psi.c:1268', 'psi.c:1269-1270', 'psi.c:600-602', 'psi.c:1273-1296',
#    'psi.c:1032-1042', 'psi.c:1364-1367', 'psi.c:1717-1719', 'psi.c:1260-1263', 'psi.c:1257-1258',
#    'psi.c:228-240', 'psi.c:149-158', 'psi.c:1553-1566', 'psi.c:1711-1719', 'psi.rst:67-88',
#    'psi.rst:102-104', 'psi.c:167', 'psi.c:1596-1598', 'psi.rst:178-187', 'psi.c:408-410',
#    'psi.rst:70-88', 'psi.c:845-857', 'psi.c:551', 'psi.c:1538-1550']
# my anchor set == my drafted anchor set (set equality asserted in the validator, exit 0)

# v7.2 baselines are committed bytes at the freeze revision 7370a731abcafc4c803111de7c22cd6264d63be1
git show 7370a731:corpus/evidence/sources-r55/kernel_sched_psi.c.v7.2        | sha256sum  # 452318beaca3e6d1  48859 bytes
git show 7370a731:corpus/evidence/sources-r55/kernel_sched_psi.c.v7.3        | sha256sum  # c4edc1e7c18ca76e  48860 bytes
git show 7370a731:corpus/evidence/sources-r55/Documentation_accounting_psi.rst.v7.2 | sha256sum # 11c6b7129103b454 6792
git show 7370a731:corpus/evidence/sources-r55/Documentation_accounting_psi.rst.v7.3 | sha256sum # 11c6b7129103b454 6792
git show 7370a731:corpus/evidence/sources-r61/psi.c                          | sha256sum  # c4edc1e7c18ca76e  48860
git show 7370a731:corpus/evidence/sources-r61/psi.rst                        | sha256sum  # 11c6b7129103b454  6792

# the whole v7.2 -> v7.3 delta of psi.c, and nothing else
diff -u corpus/evidence/sources-r55/kernel_sched_psi.c.v7.2 corpus/evidence/sources-r61/psi.c
#   @@ -1023,7 +1023,7 @@
#   	irq = irq_time_read(cpu);
#   	delta = (s64)(irq - rq->psi_irq_time);
#   -	if (delta < 0)
#   +	if (delta <= 0)
#   		return;
#   	rq->psi_irq_time = irq;
diff corpus/evidence/sources-r55/kernel_sched_psi.c.v7.2 corpus/evidence/sources-r61/psi.c | grep -c '^[<>]'
#   2        (one changed line; line numbers 1026/1026, both files 1725 lines)
diff corpus/evidence/sources-r55/Documentation_accounting_psi.rst.v7.2 corpus/evidence/sources-r61/psi.rst | grep -c '^[<>]'
#   0        (psi.rst is byte-identical v7.2 -> v7.3)
```

The v7.2 baseline digest `452318beaca3e6d1…` is the same digest the round-24 lesson records for S091
(`corpus/lessons/round-24.md:26`) and the sibling lane records for S116
(`tsukuroi-shokunin/corpus/SOURCES.md:122`), so the baseline is the same bytes the r24 entry was mined from.
The upstream URL the entry names still resolves and returns exactly those bytes
(`curl https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c` → HTTP 200, 48859 bytes,
sha256 `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5`); the fetched file was kept in
scratch, not in `/tmp`, and the citable copy of the baseline is the committed r55 file above.

## Draft ledger rows (41, in the counter's enumeration order)

Format: `| <file>:<start>[-<end>] | same|moved|changed | <loc or -> | \`<quote>\` |`
All rows are `same`; no row in this slice is `moved` or `changed`.

```
| psi.rst:60-65 | same | - | `The ratios (in %) are tracked as recent trends over ten, sixty, and` |
| psi.c:342-360 | same | - | `avg[0] = calc_load_n(avg[0], EXP_10s, 0, missed_periods);` |
| psi.c:1268-1270 | same | - | `if (now >= group->avg_next_update)` |
| psi.c:1372-1373 | same | - | `if (window_us == 0 || window_us > WINDOW_MAX_US)` |
| psi.c:1379-1380 | same | - | `if (!privileged && window_us % 2000000)` |
| psi.c:1712 | same | - | `if (psi_enable) {` |
| psi.c:1017 | same | - | `if (!curr->pid)` |
| psi.c:1540 | same | - | `return psi_show(m, &psi_system, PSI_IO);` |
| psi.c:1686 | same | - | `return psi_show(m, &psi_system, PSI_IRQ);` |
| psi.rst:36-38 | same | - | `respective file in /proc/pressure/ -- cpu, memory, and io.` |
| psi.c:1710-1721 | same | - | `proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops);` |
| psi.rst:40-43 | same | - | `some avg10=0.00 avg60=0.00 avg300=0.00 total=0` |
| psi.c:1290-1296 | same | - | `seq_printf(m, "%s avg10=%lu.%02lu avg60=%lu.%02lu avg300=%lu.%02lu total=%llu\n",` |
| psi.rst:45-56 | same | - | `The "some" line indicates the share of time in which at least some` |
| psi.rst:57-59 | same | - | `CPU full is undefined at the system level, but has been reported` |
| psi.c:1282-1288 | same | - | `if (!(group == &psi_system && res == PSI_CPU && full)) {` |
| psi.c:1284-1288 | same | - | `total = div_u64(group->total[PSI_AVGS][res * 2 + full],` |
| psi.c:160-164 | same | - | `#define PSI_FREQ	(2*HZ+1)	/* 2 sec intervals */` |
| psi.c:1268 | same | - | `collect_percpu_times(group, PSI_AVGS, NULL);` |
| psi.c:1269-1270 | same | - | `group->avg_next_update = update_averages(group, now);` |
| psi.c:600-602 | same | - | `if (now >= group->avg_next_update) {` |
| psi.c:1273-1296 | same | - | `for (full = 0; full < 2 - only_full; full++) {` |
| psi.c:1032-1042 | same | - | `if (group->rtpoll_states & (1 << PSI_IRQ_FULL))` |
| psi.c:1364-1367 | same | - | `if (res == PSI_IRQ && --state != PSI_IRQ_FULL)` |
| psi.c:1717-1719 | same | - | `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` |
| psi.c:1260-1263 | same | - | `if (!irqtime_enabled() && res == PSI_IRQ)` |
| psi.c:1257-1258 | same | - | `if (static_branch_likely(&psi_disabled))` |
| psi.c:228-240 | same | - | `if (!psi_enable) {` |
| psi.c:149-158 | same | - | `static bool psi_enable = true;` |
| psi.c:1553-1566 | same | - | `static int psi_io_open(struct inode *inode, struct file *file)` |
| psi.c:1711-1719 | same | - | `proc_create("pressure/io", 0666, NULL, &psi_io_proc_ops);` |
| psi.rst:67-88 | same | - | `Users can register triggers and use poll() to be woken up when resource` |
| psi.rst:102-104 | same | - | `The kernel accepts window sizes ranging from 500ms to 10s, therefore min` |
| psi.c:167 | same | - | `#define WINDOW_MAX_US 10000000	/* Max window size is 10s */` |
| psi.c:1596-1598 | same | - | `if (seq->private) {` |
| psi.rst:178-187 | same | - | `into cgroups. Each subdirectory in the cgroupfs mountpoint contains` |
| psi.c:408-410 | same | - | `for (s = 0; s < NR_PSI_STATES - 1; s++)` |
| psi.rst:70-88 | same | - | `time window, e.g. 100ms of total stall time within any 500ms window to` |
| psi.c:845-857 | same | - | `if (unlikely(groupc->state_mask & (1 << PSI_NONIDLE)))` |
| psi.c:551 | same | - | `sample = group->total[PSI_AVGS][s] - group->avg_total[s];` |
| psi.c:1538-1550 | same | - | `static int psi_io_show(struct seq_file *m, void *v)` |
```

### Per-row claim map (what each quote carries, and the r24 line that cites the pointer)

`r24:<n>` is the line of `corpus/knowledge/system-pressure-r24.md` where the pointer first appears.

| row | r24 line | claim the pointer supports | quote line in the pinned copy |
|---|---|---|---|
| psi.rst:60-65 | 19 | F4 / K4: averages are trends over 10/60/300 s windows | psi.rst:60 |
| psi.c:342-360 | 19 | F4: the averages are exponentially decayed | psi.c:349 (`calc_load_n` with `EXP_10s`; the same decay is spelled at 347, `/* Fill in zeroes for periods of no activity */`) |
| psi.c:1268-1270 | 21 | K5: the averages are recomputed on a read only when the next 2 s update is due | psi.c:1269 |
| psi.c:1372-1373 | 23 | K6: the code enforces 0 < window ≤ 10 s | psi.c:1372 |
| psi.c:1379-1380 | 23 | K6: unprivileged writers need a multiple of 2 s | psi.c:1379 |
| psi.c:1712 | 26 | P2: `psi_proc_init` tests `psi_enable` directly | psi.c:1712 |
| psi.c:1017 | 32 | P3: IRQ time is charged only to a non-idle current task (the idle task has pid 0) | psi.c:1017 |
| psi.c:1540 | 42 | F3: the readers pass `&psi_system` (io reader) | psi.c:1540 |
| psi.c:1686 | 42 | F3: the readers pass `&psi_system` (irq reader) | psi.c:1686 |
| psi.rst:36-38 | 66 | F1: the documented file set is cpu, memory, io | psi.rst:38 |
| psi.c:1710-1721 | 68 | F1: the kernel creates a fourth file, `pressure/irq` | psi.c:1718 |
| psi.rst:40-43 | 75 | F2: the emitted line shape | psi.rst:42 |
| psi.c:1290-1296 | 78 | F2: the emitter format string | psi.c:1290 |
| psi.rst:45-56 | 81 | F2: the `some` line semantics | psi.rst:45 |
| psi.rst:57-59 | 85 | F3: system CPU `full` is undefined | psi.rst:57 |
| psi.c:1282-1288 | 87 | F3: the kernel skips the system CPU `full` read | psi.c:1283 |
| psi.c:1284-1288 | 96 | F3/F4: the total is converted to microseconds (`NSEC_PER_USEC`) | psi.c:1286 |
| psi.c:160-164 | 98 | F4: `PSI_FREQ = (2*HZ+1)` = 2 s intervals | psi.c:161 |
| psi.c:1268 | 99 | F4: every read collects the per-CPU times | psi.c:1268 |
| psi.c:1269-1270 | 100 | F4/K5: the averages work item runs on the read path | psi.c:1270 |
| psi.c:600-602 | 101 | F4: the same update gate on the averages work item | psi.c:600 |
| psi.c:1273-1296 | 106 | F5: the print loop runs once for irq (`only_full`) | psi.c:1277 |
| psi.c:1032-1042 | 107 | F5: the IRQ path names `PSI_IRQ_FULL` only (the `+= delta` statement is line 1040) | psi.c:1042 |
| psi.c:1364-1367 | 109 | F5: a trigger naming `some` for irq is refused | psi.c:1365 |
| psi.c:1717-1719 | 113 | F6: `pressure/irq` exists only under `CONFIG_IRQ_TIME_ACCOUNTING` | psi.c:1717 |
| psi.c:1260-1263 | 116 | F6: the irq read fails `EOPNOTSUPP` without IRQ time accounting | psi.c:1261 |
| psi.c:1257-1258 | 120 | F7: the `psi_disabled` key makes every read fail | psi.c:1257 |
| psi.c:228-240 | 121 | F7: the key is enabled at init when `psi_enable` is false | psi.c:230 |
| psi.c:149-158 | 123 | F7: `psi_enable` default; the `CONFIG_PSI_DEFAULT_DISABLED` branch is line 149, the `psi=` parser lines 154–158 | psi.c:152 |
| psi.c:1553-1566 | 124 | F7: the open handlers are plain `single_open` (the `single_open` call is line 1555, 4 tokens) | psi.c:1553 |
| psi.c:1711-1719 | 126 | F7: the proc files are created only inside the `psi_enable` branch (line 1712) | psi.c:1714 |
| psi.rst:67-88 | 132 | F8: the event-driven trigger interface | psi.rst:70 |
| psi.rst:102-104 | 133 | K6/F8: the documented window range 500 ms – 10 s | psi.rst:102 |
| psi.c:167 | 134 | F8: `WINDOW_MAX_US 10000000` | psi.c:167 |
| psi.c:1596-1598 | 136 | F8: a second trigger on the same descriptor is `EBUSY` | psi.c:1596 |
| psi.rst:178-187 | 142 | F9: the cgroup scope | psi.rst:183 |
| psi.c:408-410 | 154 | F10: the monotonic accumulation loop (the `+= div_u64(...)` statement is line 410) | psi.c:409 |
| psi.rst:70-88 | 160 | F11: the only thresholds are the user's own example values | psi.rst:74 |
| psi.c:845-857 | 225 | U7: `psi_group_change` concludes and flushes the state when the group is disabled | psi.c:853 |
| psi.c:551 | 225 | U7/K4: the averages decay toward zero once the total freezes | psi.c:551 |
| psi.c:1538-1550 | 241 | round-27 correction: the range holds two full readers and a signature, not four readers | psi.c:1538 |

## Findings

### F1 — the one real v7.2→v7.3 change in `psi.c` is at line 1026 and no enumerated pointer covers it

`corpus/evidence/sources-r61/psi.c:1026` reads `if (delta <= 0)`; the v7.2 baseline
`corpus/evidence/sources-r55/kernel_sched_psi.c.v7.2:1026` reads `if (delta < 0)`. It is the only differing
line in the file (2 diff lines; both files 1725 lines; digests 452318be… → c4edc1e7…).

Effect on the r24 entry: **none of the r24 claims is falsified.** In v7.2 a zero delta fell through to
`rq->psi_irq_time = irq;` and added 0 to `PSI_IRQ_FULL`; in v7.3 the zero delta returns early. The numeric
accounting is identical (adding 0), the skipped assignment is a no-op (`irq == rq->psi_irq_time`), so F5
("the IRQ accounting path adds only to `PSI_IRQ_FULL`", `psi.c:1032-1042`), P3 (`psi.c:1017`) and U7
(`psi.c:845-857`) all still hold at v7.3. The nearest enumerated pointers are `psi.c:1017` and
`psi.c:1032-1042`; line 1026 is inside neither, and no pointer in the whole 47-pointer set names it.

Consequence for the ledger: **the C2 ledger will read "every row `same`" for `psi.c` while the file did
change.** The ledger's anchor set is derived from the r24 entry's pointer list, so a real upstream change
outside that list has no row to land in. If the round wants the recheck to be able to see upstream drift at
all, the anchor set needs a source that is not the r24 pointer list — that is an L1/L0 design point, not
something a row can express, and I did not touch the counter.

### F2 — 14 of the 47 enumerated pointers cannot carry a `same` row that passes the frozen counter

**The counter is stricter than the frozen contract it implements.** `contract.md:67` states the C2 quote rule
as: "with every quote ≤25 words, ≥8 distinct bytes, pairwise distinct". There is **no five-word floor in the
contract**. The floor exists only in the counter: `count-c2.py:151` — `if not (5 <= wordcount(q) <= 25):
res["failed"].append(f"quote_words:{anchor}")`. So under the contract as written, every quote I draft below
is conformant (all ≤13 words, all ≥8 distinct bytes, all pairwise distinct), and the only thing that rejects
14 of the 47 rows is a rule the contract never states. Amendments are barred and I may not propose a counter
change, so this is filed as a report-only finding for the L1/L0.

Mechanism: the counter locates the quote in the range's joined lines (`count-c2.py:157-166`), while a ledger
row is one physical line (`measure()` iterates `led_text.splitlines()`, `count-c2.py:141`), so a quote cannot
span the newline that joins two lines of the copy. A `same` row therefore has to take its quote from a
**single line** of the enumerated range, and 14 of the 47 enumerated ranges contain no line with five
whitespace-separated tokens:

| pointer | max tokens in range | longest line in range |
|---|---|---|
| psi.c:1710-1721 | 4 | `static int __init psi_proc_init(void)` |
| psi.c:1711-1719 | 4 | `proc_create("pressure/io", 0666, NULL, &psi_io_proc_ops);` |
| psi.c:1717-1719 | 4 | `proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops);` |
| psi.c:1268-1270 | 4 | `if (now >= group->avg_next_update)` |
| psi.c:1269-1270 | 4 | `if (now >= group->avg_next_update)` |
| psi.c:1540 | 4 | `return psi_show(m, &psi_system, PSI_IO);` |
| psi.c:1686 | 4 | `return psi_show(m, &psi_system, PSI_IRQ);` |
| psi.c:1712 | 3 | `if (psi_enable) {` |
| psi.c:1268 | 3 | `collect_percpu_times(group, PSI_AVGS, NULL);` |
| psi.c:1017 | 2 | `if (!curr->pid)` |
| psi.c:228-240 | 3 | `void __init psi_init(void)` |
| psi.c:1257-1258 | 2 | `if (static_branch_likely(&psi_disabled))` |
| psi.c:1596-1598 | 3 | `if (seq->private) {` |
| psi_types.h:41-49 *(sibling slice)* | 3 | `enum psi_res {` |

For those 14 the only counter-conformant options are (a) a `moved`/`changed` row whose `loc` is a **wider
range** with a longer line, or (b) a counter-side word-floor change — and the counter is frozen (contract:
amendments barred once a seat has scored), and I am barred from proposing a counter change, so I report the
defect instead of proposing a fix. Note the truthfulness cost of (a): for all 14 pointers the words did **not**
move and did **not** change (proved by the v7.2/v7.3 diff above), so a `moved`/`changed` status would record
a falsehood to satisfy a counter that was not written for this shape of source. The 13 rows in my slice are
drafted as `same` with the claim-carrying verbatim quote, which is what they are; they are the 13
`quote_words:*` failures in the F5 receipt. I did not fabricate a `moved`/`changed` status for them.

Restated for the L1: **the 41 rows in this report satisfy the frozen contract's own quote rule
(contract.md:67) in full.** Their only defect is measured against a floor the contract does not contain, and
that floor cannot be satisfied for those 14 rows by any honest quote of the source they point at.

### F3 — the `psi.c:1372-1373` quote contains `||` (markdown cell hazard, no floor-conformant alternative)

`if (window_us == 0 || window_us > WINDOW_MAX_US)` is verbatim and it is the only line of that range with ≥5
tokens (line 1373 is `return ERR_PTR(-EINVAL);`, 3 tokens). The counter's row regex (`count-c2.py:44-47`)
accepts it — the frozen counter validated this row (`quotes_ok` counted it) — but a `|` inside a markdown
table cell splits the cell in most renderers. The L1 may leave it (the gate is the counter, not the
renderer) or pick a different line and accept the `quote_words` failure; there is no third option that both
passes the floor and avoids the pipe.

### F4 — copy-citation dependency across seats, and six new SOURCES rows are mandatory

My 41 rows cite **2** of the 6 pinned copies (`psi.rst`, `psi.c`). The counter's floor is `>= 4` distinct
cited copies (`count-c2.py:169-171`). The sibling slice's 6 rows are the only source of the other four
(`psi_types.h`, `cgroup-v2.rst`, `Kconfig`, `kernel-parameters.txt`), so the floor is met only if that seat
lands rows citing all four. Note the coupling with F2: a failed row never reaches `cited.add(fname)`
(`count-c2.py:159-161`), so `psi_types.h:41-49` failing drops the counted copies from 6 to 5 — still ≥ 4, so
the floor survives even in the failure case.

Second half of the same finding, measured against the registry (`corpus/SOURCES.md:309-313`): the `rows_src`
check (`count-c2.py:180-182`) requires **one single SOURCES.md line** to carry
`corpus/evidence/sources-r61/<file>`, `| mined |` **and** `psi-v73-recheck-r61.md`. The five existing v7.3
rows S529–S533 cannot satisfy it: their copy paths are the **r55** ones
(`corpus/evidence/sources-r55/Documentation_accounting_psi.rst.v7.3`,
`…/kernel_sched_psi.c.v7.3`, `…/include_linux_psi_types.h.v7.3`,
`…/Documentation_admin-guide_kernel-parameters.txt.v7.3`,
`…/Documentation_admin-guide_cgroup-v2.rst.v7.3`) and their used-by is
`corpus/knowledge/kernel-v7.3-recheck-r55.md` — zero of the five lines mentions `sources-r61` or the r61
ledger (grep count 0). **Six new rows naming the r61 copy paths are therefore mandatory**, one per pinned
copy, each naming the ledger entry in used-by. This is the r55 rows' gap as well as the r61 rows' duty, and
it lands squarely on my slice: the `psi.rst` and `psi.c` rows are two of the six. (Independently raised by
`Mo61ScoutS090`, whose §2 F-2 makes the same point; I did not edit the registry.)

### F5 — empirical receipts from the frozen counter (scratch fixture, no repo change)

Fixture: a throwaway git repo at `/fast/scratch/hyaku/mori-r61/Mo61ScribePsi1/fixture` (created with
`git -C "$D" init -q`, `git -C "$D" rev-parse --show-toplevel` asserted to equal the fixture dir before any
write), holding the real r24 entry, the six pinned copies (sha256-equal to `count-c2.py` `PINS`), a
`corpus/SOURCES.md` with six `mined` / `used-by: …psi-v73-recheck-r61.md` rows, and a ledger with my 41 rows
plus 6 probe-filler rows for the sibling pointers (fillers are probe scaffolding only, not draft rows).

Frozen counter, unmodified:

```text
$ python3 .ufo/waves/round-61/count-c2.py 468f1f26… --repo <fixture> --scratch <scratch>
C2=unmet pointers=47 rows=47 same=33 moved=0 changed=0 quotes_ok=33 spans_ok=33 sources=5 failed=quote_words:psi.c:1268-1270;quote_words:psi.c:1712;quote_words:psi.c:1017;quote_words:psi.c:1540;quote_words:psi.c:1686;quote_words:psi.c:1710-1721;quote_words:psi.c:1268;quote_words:psi.c:1269-1270;quote_words:psi.c:1717-1719;quote_words:psi.c:1257-1258;quote_words:psi.c:228-240;quote_words:psi.c:1711-1719;quote_words:psi.c:1596-1598;quote_words:psi_types.h:41-49 rev=468f1f26…
rc=1
```

Counterfactual (scratch **copy** of the counter with the word floor 5 → 1; the frozen file's sha256 was
`82d0fee6…` before and after the run, so it was not modified):

```text
$ python3 <scratch>/count-c2-wordfloor-probe.py 468f1f26… --repo <fixture> --scratch <scratch>
C2=met pointers=47 rows=47 same=47 moved=0 changed=0 quotes_ok=47 spans_ok=47 sources=6 failed=none rev=468f1f26…
rc=0
```

Reading of the two receipts together: **the only thing standing between these rows and `C2=met` is the
5-word floor**, and the 14 failures it produces are exactly the 14 pointers listed in F2 — 13 of them mine,
1 (`psi_types.h:41-49`) in the sibling slice. No `quote_missing`, no `quote_dup`, no `span_small`, no
`rows_missing`/`rows_orphan`, no `rows_src`, no `provenance` failure: my 41 anchors are exactly the counter's
enumeration, my quotes are byte-located where the rows state, they are pairwise distinct, and they are ≥8
distinct bytes each.

## Boundaries observed

- Read-only on the lane: no production file (`SKILL.md`, `corpus/`, `SCORECARD.md`, `LOG.md`, `tools/`), no
  registry, no VCS state was touched. The only file written is this report, at the path the seat spec names.
- No `task` dispatch, no `agent://all` message.
- No mutating git/jj command in the lane or the fleet. The only git writes were `init`/`add`/`commit` inside
  the scratch fixture, all with `git -C "$D"`, after asserting the fixture top-level.
- No service, config or provider change; detection and report only.
- Tools installed: **none**. Tooling used, all pre-existing: `python3` 3.14.8, `git` 2.56.0,
  `curl` 8.23.0, `diff`, `sha256sum`. The operator's tooling authorization (read
  `/home/vgpnk/.omp/agent/RULES.md`) was not needed: no install or upgrade was required for this item.
- Scratch: `/fast/scratch/hyaku/mori-r61/Mo61ScribePsi1/` (fixture, receipts, row table) — removed before
  yielding; every receipt needed for this report is quoted above.
