# Mo53ExecBandDerivation — the C2 band rule against the kernel

Seat: Mo53ExecBandDerivation (executor, attack share). Claim under test: C2 (coverage), the mode-2 band
`band_kb = batch_pages × present CPUs × page` in `tools/mori-commit-runway.py` and the reading in
`corpus/knowledge/commit-runway-read-r53.md` (rows S511-S513). Lane: mori-shokunin. This report writes no vote
line and no counter line; it reports derivation and observed evidence only.

Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecBandDerivation/` (`TMPDIR` set there; every fixture under it;
removed at the end). No clone, no lane write, no git/jj mutation, no pacman, no tool installs (nothing was
installed or upgraded this seat). Host identity as MACHINE_ID; kernel line `7.2.11-arch1-1`; disk guard
`status` exit 0, `/fast/scratch/hyaku` 27% used.

## Answers to the three assigned questions

1. **Is `band = batch × present CPUs` a true upper bound on |global count − exact sum|?** *Yes, and it is
   conservative on the CPU-count side — but only while the tool's recomputed `batch` is ≥ the kernel's live
   `vm_committed_as_batch`.* The per-CPU pending delta is bounded by the batch itself (derivation in §2), the
   sum mask is `online ∪ dying`, and present CPUs ⊇ online. The one systematic hole is the batch value, which
   the kernel recomputes on memory hotplug and on a sysctl write but **not on CPU hotplug** (§3.3) — the tool's
   own docstring already names this; the knowledge entry's Boundaries does not (§6, finding 1).
2. **Is the batch recomputed when the mode changes at run time and when memory is hot-added?** *Both yes* —
   mode write: `mm_compute_batch(new_policy)` plus a per-CPU fold (§3.1, verified by text); memory hot-add and
   hot-remove: the memory-hotplug notifier (§3.2, verified including the `totalram` ordering).
3. **Does `mm_compute_batch` differ at v7.3?** *No* — the function text is byte-identical between the pinned
   v7.2 copy and the v7.3 file I fetched; `lib/percpu_counter.c` and `include/linux/percpu_counter.h` are
   byte-identical files between the two tags; `mm/util.c`'s four relevant functions are identical (§4).

## Method and source integrity (commands, outputs, exit codes)

Fetches into scratch, all HTTP 200 from git.kernel.org cgit (raw.githubusercontent.com not used):

```
curl -fsSL -o mm_init.c.v7.3      '.../plain/mm/mm_init.c?h=v7.3'            # HTTP 200 size=76467
curl -fsSL -o mm_init.c.v7.2      '.../plain/mm/mm_init.c?h=v7.2'            # HTTP 200
curl -fsSL -o percpu_counter.c.v7.2 / .v7.3, percpu_counter.h.v7.2 / .v7.3   # HTTP 200 (10932 / 6977 bytes each)
curl -fsSL -o util.c.v7.2 / util.c.v7.3, memory_hotplug.c.v7.2 / .v7.3      # HTTP 200
curl -fsSL -o show_mem.c.v7.3, vmstat.c.v7.3, page_alloc.c.v7.3, cpu.c.v7.3, cpuhotplug.h.v7.3,
            cpuset.h.v7.3, drivers/base/cpu.c?h=v7.2                        # HTTP 200
curl '.../plain/arch/x86/kernel/cpu.c?h=v7.2' and '?h=v7.3'                 # HTTP 404 both (see finding 5)
```

Pinned copies vs upstream, byte comparison (`diff -u`, empty output + `IDENTICAL`):

| pinned copy | vs cgit | result |
|---|---|---|
| `corpus/evidence/sources-r53/mm_init.c.v7.2` | `mm/mm_init.c?h=v7.2` | IDENTICAL |
| `corpus/evidence/sources-r53/percpu_counter.c.v7.2` | `lib/percpu_counter.c?h=v7.2` | IDENTICAL |
| `corpus/evidence/sources-r53/percpu_counter.h.v7.2` | `include/linux/percpu_counter.h?h=v7.2` | IDENTICAL |
| `corpus/evidence/sources-r52/util.c.v7.2` | `mm/util.c?h=v7.2` | IDENTICAL |
| `corpus/evidence/sources-r53/util.c.v7.3` | `mm/util.c?h=v7.3` | IDENTICAL |

So the four files S499/S511/S512/S513 rest on are the tag's bytes, and the r53 v7.3 `util.c` copy is the tag's
bytes too.

## §1 The tool's formula against `mm_compute_batch`, term by term

Kernel, `corpus/evidence/sources-r53/mm_init.c.v7.2` (identical at v7.3, lines 195-213 of the fetched file):

- `194: s32 nr = num_present_cpus();`
- `195: s32 batch = max_t(s32, nr*2, 32);`
- `196: unsigned long ram_pages = totalram_pages();`
- `204: if (overcommit_policy == OVERCOMMIT_NEVER)`
- `205: memsized_batch = min_t(u64, ram_pages/nr/256, INT_MAX);`
- `207: memsized_batch = min_t(u64, ram_pages/nr/4, INT_MAX);`   (the non-NEVER branch, 64× looser)
- `209: vm_committed_as_batch = max_t(s32, memsized_batch, batch);`

Tool, `tools/mori-commit-runway.py:182`: `batch = max(min(ram_pages // cpus // 256, INT_MAX), max(2 * cpus, 32))`,
with `ram_pages = mi["MemTotal"] // page_kb` (line 154) and `cpus` = entry count of
`/sys/devices/system/cpu/present` (lines 148, 115-125).

Term-by-term: present-CPU source ✓ (`num_present_cpus()` is `cpumask_weight(cpu_present_mask)`, and
`/sys/devices/system/cpu/present` is that same mask: `drivers/base/cpu.c?h=v7.2:231
_CPU_ATTR(present, &__cpu_present_mask)`); floor `max(2·nr, 32)` ✓; `/256` branch ✓ and it is only used in the
tool's mode-2 path (line 181 gates it), matching `OVERCOMMIT_NEVER == 2`; division order ✓ — C's
`ram_pages/nr/256` is `(ram_pages/nr)/256`, the tool's `ram_pages // cpus // 256` is the same left-to-right
floor; `INT_MAX` cap ✓ (`2**31-1`, line 66, applied to the memsized term only, exactly as the kernel's `min_t`
does); final `max` ✓.

`ram_pages` source: the kernel's `totalram_pages()`, and `/proc/meminfo` MemTotal is exactly that in kB —
`show_mem.c.v7.3:78 val->totalram = totalram_pages();` and `meminfo.c.v7.3:28-32,60` print it as
`num << (PAGE_SHIFT - 10)`. So `MemTotal // page_kb == totalram_pages` exactly (no truncation for any
`page_kb` that is a power of two dividing the shift, which the tool enforces, line 307).

The batch actually used for the counter is this one: `mman.h.v7.3:76-78
percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch);` and no other writer of
`vm_committed_as` exists in the fetched tree (`mmap.c.v7.3:1548` is the initialiser; `util.c` touches it only
through `vm_acct_memory`/`vm_unacct_memory` and `percpu_counter_sync`). In particular the tool correctly does
**not** use `percpu_counter_batch` (a different variable, `percpu_counter.c.v7.2:259-264`, sized from
`num_online_cpus()` and updated on CPU hotplug).

## §2 Derivation: why `batch × present CPUs` bounds |global − sum|

Definitions. `G = fbc->count` (the global count — what the mode-2 test reads via
`percpu_counter.h.v7.2:118-126` `s64 ret = READ_ONCE(fbc->count); if (ret >= 0) return ret; return 0;`).
`S = __percpu_counter_sum` (what /proc/meminfo prints as Committed_AS, `util.c.v7.2:937-940
return percpu_counter_sum_positive(&vm_committed_as);` reached from `meminfo.c.v7.3:46 committed =
vm_memory_committed();`). The mode-2 comparison is global-only: `util.c.v7.2:994
if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;`.

Per-CPU delta invariant. `percpu_counter_add_batch` keeps every per-CPU local strictly below one batch in
magnitude. Fast path is entered only when the *prospective* value is below the batch; the fold path resets the
local to zero:

- `percpu_counter.c.v7.2:98-112` (CMPXCHG variant): `100: if (unlikely(abs(count + amount) >= batch)) {` →
  `107: fbc->count += count + amount;` `108: __this_cpu_sub(*fbc->counters, count);` (local → 0); otherwise
  `112: } while (!this_cpu_try_cmpxchg(*fbc->counters, &count, count + amount));` with `abs(count+amount) <
  batch`, so the new local is `< batch`.
- `percpu_counter.c.v7.2:120-137` (the `#else` variant, for arches without `CONFIG_HAVE_CMPXCHG_LOCAL`): same
  shape — fold when `abs(count) >= batch` with `count = local + amount`, and the sub leaves local 0; else
  `this_cpu_add` with `abs(local+amount) < batch`.

The local is an `s32` (`percpu_counter.h.v7.2:28 s32 __percpu *counters;`), so a batch capped at INT_MAX cannot
overflow it, and the fast-path guard keeps the stored value inside `(−batch, batch)`.

The sum mask. `percpu_counter.c.v7.2:179 for_each_cpu_or(cpu, cpu_online_mask, cpu_dying_mask) {` — online plus
dying. The comment above it gives the reason (lines 161-169: dying CPUs "have been removed from the online mask,
but may not have had the hotplug dead notifier called to fold the percpu count back into the global counter
sum"), so the dying window is inside the sum.

Therefore `|S − G| = |Σ_{online∪dying} local_c| ≤ Σ |local_c| < B × |online ∪ dying|`, with `B` the live
`vm_committed_as_batch`. Substituting the tool's multiplier: `present ⊇ online`, and a dying CPU is still a
physically present CPU, so `|online ∪ dying| ≤ present` and

    |S − G| < batch × present CPUs = band_pages      (strict; the tool uses the closed bound, which is looser)

This matches the kernel's own convention for the same quantity: `percpu_counter.c.v7.2:298
if (abs(count - rhs) > (batch * num_online_cpus())) {` and `339: unknown = batch * num_online_cpus();` — the
kernel multiplies by **online**, the tool by **present**, which is the conservative superset.

CPU-set choices, explicitly:
- **online**: the only CPUs that can accumulate a delta (a CPU must run `percpu_counter_add_batch`), and the
  kernel's own bound.
- **present**: online plus offline-but-present CPUs. Used by the batch formula itself, so using it for the
  multiplier keeps the two terms consistent, and it over-covers online (safe).
- **possible**: the per-CPU storage spans possible CPUs (`percpu_counter.c.v7.2:63-70` `percpu_counter_set`
  iterates `for_each_possible_cpu`), but a CPU that never ran cannot hold a delta, so possible would inflate the
  band with nothing behind it. Not needed.
- **dying**: must be covered (the sum includes them); present covers them, subject to finding 5.
- **hotplug fold**: `percpu_counter.c.v7.2:266-285 percpu_counter_cpu_dead` does `279: fbc->count += *pcount;`
  `280: *pcount = 0;` under the counter lock, registered at `401-403 cpuhp_setup_state_nocalls(
  CPUHP_PERCPU_CNT_DEAD, ...)`. After the fold the CPU contributes 0 to the local sum and its value is inside
  `G`, so an offline CPU never widens the deviation.

**So the deviation bound itself is sound; only the batch value can break it.** The residual bound is
`B_live × present`, and the tool ships `B_tool × present` — the next section is entirely about `B_tool` vs
`B_live`.

Note the *sign*: `S − G = Σ locals` is signed (unaccounting is `vm_unacct_memory` → negative amounts), so the
enforced `G` can sit up to one band **above** the printed `S` as well as below it. The tool's docstring says
this correctly in both directions (`mori-commit-runway.py:38-45`: "net-negative deltas can refuse while they
show room, net-positive deltas can admit past them"); the knowledge entry states one direction only (finding 3).

## §3 When the kernel recomputes the batch, and when it does not

`mm_compute_batch` has exactly three call sites in the fetched tree:
`mm_init.c.v7.2:228` (init), `:218` (memory hotplug notifier), and `util.c.v7.2:831` (sysctl write). No CPU
hotplug site exists.

### §3.1 Mode change at run time — recomputed, and the pending deltas are folded first

`util.c.v7.2:806 static int overcommit_policy_handler(...)`; on write (lines 827-834):

    831:  mm_compute_batch(new_policy);
    833:  schedule_on_each_cpu(sync_overcommit_as);
    834:  sysctl_overcommit_memory = new_policy;

`mm_compute_batch` is passed the *new* policy, so switching to mode 2 selects the `/256` branch; the kernel's own
comment (lines 816-826) states the order "changing the batch / sync percpu count on each CPU / switch the
policy". `sync_overcommit_as` is `percpu_counter_sync(&vm_committed_as)` (line 803), which folds the running
CPU's local into `G`; `schedule_on_each_cpu` runs it once per CPU, so immediately after the switch
`Σ locals ≈ 0` and thereafter each local is bounded by the *new* (smaller) batch. This is the one path where the
kernel does exactly what the tool assumes, and it is the path that matters: mode 2 is reached by writing this
sysctl. The entry's claim row on this point (`Switch the sysctl to mode 2 recomputes the batch and syncs every
CPU before the new policy takes effect`) is supported by these lines.

### §3.2 Memory hot-add and hot-remove — recomputed, with `totalram` already moved

`mm_init.c.v7.2:212-224` (identical at v7.3, lines 216-222) handles both:

    216:  case MEM_ONLINE:
    217:  case MEM_OFFLINE:
    218:      mm_compute_batch(sysctl_overcommit_memory);

registered by `229: hotplug_memory_notifier(mm_compute_batch_notifier, MM_COMPUTE_BATCH_PRI);`.

Ordering versus `totalram_pages()` (this is what makes the recompute agree with today's MemTotal):

- hot-remove: `memory_hotplug.c.v7.3:2115 adjust_managed_page_count(pfn_to_page(start_pfn), -managed_pages);`
  runs **before** `2152: memory_notify(MEM_OFFLINE, &mem_arg);` — and `adjust_managed_page_count` is what feeds
  `page_alloc.c.v7.3:6426-6431 totalram_pages_add(count)`. Same order in v7.2 (2062 then 2099). So the
  recompute sees the reduced total, matching what the tool would read afterwards.
- hot-add: managed pages are incremented through `__free_pages_core(..., MEMINIT_HOTPLUG)` →
  `adjust_managed_page_count` (`page_alloc.c.v7.3:1600-1623`, `6426-6431`) when the memory is handed to the
  allocator, and `memory_notify(MEM_ONLINE, &mem_arg)` comes later at `memory_hotplug.c.v7.3:1241` — so the
  recompute sees the increased total.

One residual: on hot-remove the batch **shrinks** and no per-cell sync happens (contrast §3.1), so a delta
accumulated under the larger batch can stay above the new batch until that CPU's next add folds it. Transient
and bounded by the old batch; not named in the tool or the entry (finding 2).

### §3.3 CPU hotplug — not recomputed (the systematic hole)

`num_present_cpus()` changes with CPU hotplug (`set_cpu_present`, `cpu.c.v7.3:3163` on the bring-up side), but
nothing in the CPU-hotplug path calls `mm_compute_batch`; CPU hotplug updates only `percpu_counter_batch`
(`percpu_counter.c.v7.2:259-264 percpu_counter_batch = max(32, nr*2);`, registered at `CPUHP_AP_ONLINE_DYN`),
which is not the `vm_committed_as` batch. The tool, by contrast, re-derives the batch from **today's** MemTotal
and **today's** present count.

Direction and size. Write mode 2 at 32 present CPUs with 8 GiB RAM: live
`B_live = max(min(2097152/32/256, INT_MAX), max(64,32)) = max(256, 64) = 256` pages. Then hot-add CPUs to 64:
the tool computes `max(min(2097152/64/256), max(128,32)) = max(128,128) = 128` pages, and reports
`band = 128 × 64 = 8192` pages; the true bound with the live batch is `256 × 64 = 16384` pages. The reported
band is **half** the bound. (Hot-remove of CPUs moves the other way: the tool's memsized term grows, so it
over-states — safe.) On a host where the `/256` term dominates, the understatement factor is roughly
`nr_recompute / nr_today`.

This is the one case where `band = batch × present` is not an upper bound, and the tool's own docstring already
says so (`mori-commit-runway.py:45-47`: "The batch is recomputed on memory hotplug and on a write of the sysctl,
not on CPU hotplug: after a CPU hot-add the true bound can exceed the band."). The knowledge entry's Boundaries
does not (finding 1).

Balloon (UNVERIFIED). The entry's Boundaries says "a balloon that changes totalram without hotplug does not
[recompute the batch]". Whether `totalram_pages()` moves with ballooning is not something I confirmed: the v7.3
tree's own comment says ballooning adjusts *managed* pages (`memory_hotplug.c.v7.3:942-946`), and
`adjust_managed_page_count` is what feeds `totalram_pages_add`, but I did not fetch any balloon driver to see
whether it calls that API. If it does not, the clause describes a case that cannot arise (MemTotal, hence the
tool's `ram_pages`, would not move either, so no divergence). Marked UNVERIFIED (finding 6).

Non-SMP. `mman.h.v7.3:64-70` makes `vm_committed_as_batch` 0 and `mm_compute_batch` a no-op when `CONFIG_SMP` is
off; with batch 0 every add folds, the counter is exact, and the tool's non-zero band is a harmless
over-estimate. Not a defect, named for completeness.

## §4 v7.3 comparison (function-level, not line-level)

Extracted each function body and compared text (`python3` extraction, `IDENTICAL`/`DIFFERENT` per function):

| function | v7.2 copy | v7.3 fetched | result |
|---|---|---|---|
| `mm_compute_batch` | mm_init.c.v7.2 | mm_init.c.v7.3 | IDENTICAL (20 lines each) |
| `mm_compute_batch_notifier` | mm_init.c.v7.2 | mm_init.c.v7.3 | IDENTICAL (13 lines each; both have MEM_ONLINE and MEM_OFFLINE) |
| `overcommit_policy_handler` | util.c.v7.2 | util.c.v7.3 | IDENTICAL (35 lines each) |
| `sync_overcommit_as` | util.c.v7.2 | util.c.v7.3 | IDENTICAL (4 lines each) |
| `vm_commit_limit`, `__vm_enough_memory`, `vm_memory_committed` | util.c.v7.2 | util.c.v7.3 | IDENTICAL (13 / 45 / 4 lines) |
| whole files `lib/percpu_counter.c`, `include/linux/percpu_counter.h` | .v7.2 | .v7.3 | IDENTICAL (`diff -q`: same 10932 / 6977 bytes) |

The only difference around the function in `mm_init.c` is a new unrelated `early_param("mminit_loglevel")` block
earlier in the v7.3 file, which shifts `mm_compute_batch` from line 191 to 195. The entry's wording — "the batch
rule is unchanged at v7.3 (`mm_compute_batch` in the v7.3 copy differs only by its line number)" — is therefore
true of the function; note that no v7.3 copy of `mm_init.c`, `percpu_counter.c` or `percpu_counter.h` is pinned in
`corpus/evidence/sources-r53/` (finding 4), so the assertion rests on a fetch that was not committed.

## §5 Host arithmetic, exercised read-only (no sysctl written)

The host is mode 0, so the band is not produced live; I materialised the host's own inputs in scratch with
`overcommit_memory` changed to 2 **in the scratch copy only** and ran the tool against them:

```
cd /fast/scratch/hyaku/mori-r53/Mo53ExecBandDerivation && mkdir -p band/vm && cp /proc/meminfo band/meminfo
  && for f in overcommit_memory overcommit_ratio overcommit_kbytes admin_reserve_kbytes user_reserve_kbytes;
     do cp /proc/sys/vm/$f band/vm/$f; done && echo 2 > band/vm/overcommit_memory
  && cp /sys/devices/system/cpu/present band/present
python3 -I -B .../tools/mori-commit-runway.py --meminfo band/meminfo --vm-dir band/vm --cpu-present band/present
```

Output (exit 0):

```
{"band_kb": 123904, "batch_pages": 968, "commit_limit_kb": 47583772, "committed_as_kb": 41747916,
 "cpus_present": 32, "enforced": true, "findings": [], "headroom_kb": 5835856, "limit_consistent": true,
 "limit_recomputed_kb": 47583772, "mode": 2, "reserve_kb": 139264, "schema": "mori-commit-runway-v1",
 "single_request_cap_kb": null, "usable_kb": 5696592, "verdict": "COMMIT_OK"}
```

Hand arithmetic on the same inputs (MemTotal 31721796 kB, page 4, 32 present CPUs, `Hugetlb` 0, ratio 50,
SwapTotal 31722876 kB): `ram_pages = 7930449`; memsized term `7930449/32/256 = 968`; floor `max(64,32) = 64`;
`batch = 968`; `band = 968 × 32 × 4 = 123904` kB ≈ 121 MiB; `limit = (7930449−0)×50/100 + 7930719 = 11895943`
pages → 47583772 kB, equal to the printed CommitLimit (`limit_consistent: true`). Every field agrees with the
formula in §1 — no arithmetic defect found.

Live mode 0 (unmodified host inputs) gives `COMMIT_HEURISTIC`, `batch_pages: null`, `band_kb: null`, exit 0 —
the band is correctly absent outside mode 2.

`vm_committed_as_batch` is not exported to user space (no `/proc` or `/sys` file carries it), so the *live* kernel
value could not be read back on this host: UNVERIFIED by direct observation; §3 is derived from the source.

## §6 The entry and the fixtures

Fixture coverage of the formula's two branches (`tools/fixtures/mori-commit-runway/cases.json`, 26 static cases,
11 of them mode 2): memsized branch — `mode2-ok` (batch 256, band 32768), `mode2-negative-headroom` (968),
`mode2-sparse-cpulist` (10922), `mode2-one-cpu` (2048), `mode2-hugetlb-ratio80` (2048); floor branch —
`mode2-batch-floor-64cpu` (batch 128 = `2×64`) and `mode2-page64` (128). Both branches are exercised, so a tool
that dropped either term would fail the fixture arm. The `INT_MAX` cap is unreachable in every fixture (it needs
`ram/cpus/256 > 2**31−1`, i.e. more than ~2 TiB per CPU) — untested but harmless in that direction (the cap only
ever lowers the band).

`count-c2.py:136-138` computes the reference with the same expression
(`max(min(ram_pages // cpus // 256, INT_MAX), max(cpus * 2, 32))`) and the same `band_kb = batch * cpus * page_kb`,
so the contract's "REF and the tool share one author" limit is not merely possible: at the formula level the two
are the same six tokens. My independent check against the kernel (§1) is the only thing separating them, and it
agrees, so a shared misreading is ruled out for this formula — but a shared *omission* of the batch-staleness
(§3.3) would also be invisible to the counter, which is why that item belongs in the report as a limit rather
than as a counter defect.

Entry prose checks (claim table): the four S511/S512/S513 quotes locate in the pinned v7.2 bytes at
`mm_init.c.v7.2:194-195`, `:204-205`, `:199-201`; `percpu_counter.c.v7.2:100`; `percpu_counter.h.v7.2:121-125`;
and the two util.c quotes at `util.c.v7.2:994` and `:937-940`. The claim "the figure printed as Committed_AS is
the exact sum across CPUs" holds for the sum mask `online ∪ dying` (`percpu_counter.c.v7.2:179`), with the
caveat that a dying CPU's delta is included before it is folded — exact at the instant of the read, as the
kernel intends.

## Findings

1. **MED** — `corpus/knowledge/commit-runway-read-r53.md`, Boundaries paragraph ("the batch is a bound for
   common case, not a proof"): the entry omits the one systematic case where `band = batch × present` is *not*
   an upper bound. `mm_compute_batch` is **not** re-run on CPU hotplug (`mm/mm_init.c` v7.2:212-229 registers a
   *memory* hotplug notifier only; `lib/percpu_counter.c` v7.2:259-264 updates a different variable), while the
   tool re-derives the batch from today's present-CPU count. Worked example in §3.3: 8 GiB, mode 2 written at
   32 CPUs, then hot-add to 64 → reported band 8192 pages against a true bound of 16384 pages. The tool's own
   docstring already states this (`tools/mori-commit-runway.py:45-47`), so the entry and the tool disagree; the
   entry is data the L1 may correct. Not a counter change: `count-c2.py` compares the tool with REF, not with
   the kernel, so this is a named limit (and a routed item for round 54 would be to widen the tool's band by
   `max(batch_live_estimate, batch_today)` or to say "CPU hotplug invalidates the band").
2. **LOW** — `lib/percpu_counter.c` v7.2:98-112 vs `mm/mm_init.c` v7.2:216-218 and `mm/util.c` v7.2:831-834: on
   memory hot-remove the batch shrinks with no per-CPU sync (unlike the mode-write path, which syncs each CPU
   before switching). Pending deltas accumulated under the larger batch can exceed the new batch until each
   CPU's next add, so the band can under-state for a transient window. Named nowhere in the entry or docstring.
3. **LOW** — `corpus/knowledge/commit-runway-read-r53.md`, the paragraph ending "…although the printed numbers
   still show room": that consequence needs **net-negative** pending deltas (`vm_unacct_memory` dominating),
   because the enforced value is the global count, which normally *lags* the printed sum. The tool's docstring
   is two-sided and correct (`tools/mori-commit-runway.py:38-45`); the entry states one direction. Wording/data
   item for the L1 — the verdict rule itself (`usable_kb <= band_kb`) is conservative for both directions.
4. **LOW** — `corpus/knowledge/commit-runway-read-r53.md`, Boundaries bullet "the batch rule is unchanged at
   v7.3": true (§4: `mm_compute_batch`, its notifier, `percpu_counter.c` and `percpu_counter.h` are byte-identical
   between v7.2 and v7.3, and so are the four relevant `mm/util.c` functions), but no v7.3 copy of those three
   paths is committed under `corpus/evidence/sources-r53/` (`mm_init.c.v7.2` is there; no `.v7.3`), so the
   assertion is unpinned and the entry's own `recheck:` line defers the comparison to the next tag. My
   independent cgit fetch is the evidence here; pinning it or softening the sentence is the L1's call.
5. **LOW** — `lib/percpu_counter.c` v7.2:179, 266-285 and `kernel/cpu.c` v7.3:3163: the bound needs
   `present ⊇ online ∪ dying`. `online ⊆ present` is structural; that a *dying* CPU is still in the present mask
   when its delta is counted is UNVERIFIED — I could not locate the present-bit clear (`arch/x86/kernel/cpu.c`
   returns HTTP 404 at both tags; `kernel/cpu.c` v7.3 only sets the bit at boot). If the present bit were
   cleared before `percpu_counter_cpu_dead` folds the delta, the band would be short by at most one batch. Bounded
   and narrow, but it is the one assumption in §2 I could not close.
6. **LOW** — `corpus/knowledge/commit-runway-read-r53.md`, Boundaries: "a balloon that changes totalram without
   hotplug" — UNVERIFIED (`mm/memory_hotplug.c` v7.3:942-946 says ballooning adjusts *managed* pages and
   `adjust_managed_page_count` feeds `totalram_pages_add`, but I did not fetch a balloon driver to confirm the
   call). If the balloon does not move `totalram_pages()`, MemTotal cannot move either and the clause describes
   an impossible case; either way it does not affect the current verdicts.
7. **LOW** — `corpus/knowledge/commit-runway-read-r53.md` claim row "The mode-2 read takes only the global count
   … never summing the per-CPU deltas" quotes the CMPXCHG variant of `percpu_counter_add_batch`
   (`percpu_counter.c.v7.2:100`) for the fold rule; the `#else` variant (lines 120-137) checks `abs(count)` after
   adding and is not quoted. The claim is true of both variants, so this is a completeness note, not an error.

Verified-good (no finding, listed so the L1 can name them as checked): the batch formula against
`mm_compute_batch` on all four components including division order and the present-CPU source; MemTotal against
`totalram_pages()`; the mode-write recompute plus per-CPU fold; the MEM_ONLINE/MEM_OFFLINE recompute with the
`totalram` ordering in both directions; the per-CPU delta invariant in both `percpu_counter_add_batch` variants;
online/present/possible/dying CPU-set choices; the hotplug fold; the fixture branch coverage of the formula; the
host arithmetic in mode 2 (batch 968, band 123904 kB).

Blockers: none. Limits of this seat: no direct read of the live `vm_committed_as_batch` (not exported); the x86
CPU-removal path not fetchable (404); no balloon driver fetched; no counter, predicate or control re-run
(frozen, and not this seat's arm).
