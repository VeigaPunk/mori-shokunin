# Mo52ExecBatchDeviation — how large is the mode-2 commit test's approximation error?

Seat: executor, attack/measure on C2's Boundaries sentence (round 52, wave w1). Lane `mori-shokunin`, data revision
`8524904adb25e44f24d9f25aac7eae909625c18c`. Read-only on the host and on the lane; nothing written outside this
report and `/fast/scratch/hyaku/mori-r52/Mo52ExecBatchDeviation/` (removed at the end).

Verdict in one line: the error is bounded by `batch × nr_cpus` pages, and the batch is policy-derived — **968 pages
(3.78 MiB/CPU, a 121.0 MiB band) under mode 2** versus **61956 pages (242.02 MiB/CPU, a 7.56 GiB band) under modes
0/1** on this host. So yes, the number belongs in Boundaries: without it the sentence "can differ by up to the batch
size per CPU" is true but uncomputable, and the wrong batch (the mode-0/1 one) is 64× larger than the right one.

## Commands and receipts

All commands below ran with cwd `/fast/scratch/hyaku/mori-r52/Mo52ExecBatchDeviation/` and
`TMPDIR=/fast/scratch/hyaku/mori-r52/Mo52ExecBatchDeviation/tmp`. Fetches are the only writes; no host state was
touched (`/proc` reads only), no `pacman`, no installs.

```
$ nproc ; cat /proc/sys/vm/overcommit_memory /proc/sys/vm/overcommit_ratio /proc/sys/vm/overcommit_kbytes ; cat /sys/devices/system/cpu/present
32
0
50
0
0-31
exit=0

$ grep -E '^(MemTotal|SwapTotal|CommitLimit|Committed_AS|HugePages_Total)' /proc/meminfo      # read 1
MemTotal:       31721796 kB
SwapTotal:      31722876 kB
CommitLimit:    47583772 kB
Committed_AS:   40122148 kB
HugePages_Total:       0
exit=0
   # read 2, eight minutes later (host is live; Committed_AS moved, nothing else did)
Committed_AS:   40154220 kB
```

Fetch + digest (raw.githubusercontent and git.kernel.org both, to rule out a mirror surprise):

```
$ curl -fsSL -o mm_init.c https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/mm_init.c ; sha256sum mm_init.c
ed691b24afbc0dc45090e149d115d707af0c5f7369a10b7722d491075f26a754  mm_init.c
$ curl -fsSL -o korg-mm_init.c 'https://git.kernel.org/.../plain/mm/mm_init.c?h=v7.2' ; sha256sum korg-mm_init.c
ed691b24afbc0dc45090e149d115d707af0c5f7369a10b7722d491075f26a754  korg-mm_init.c
exit=0

util.c                         e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c   (raw + korg identical)
lib/percpu_counter.c           2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d   (raw + korg identical)
include/linux/percpu_counter.h 4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896   (raw + korg identical)
fs/proc/meminfo.c              d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda
mm/show_mem.c                  dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5
```

Corroboration that these are the v7.2 bytes the entry already froze: `util.c`'s digest equals the entry's S499
recheck digest and the committed copy's digest —

```
$ sha256sum corpus/evidence/sources-r52/util.c.v7.2 corpus/evidence/sources-r52/mman.h.v7.2
e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c  corpus/evidence/sources-r52/util.c.v7.2
d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058  corpus/evidence/sources-r52/mman.h.v7.2
$ sed -n '831p;939p;994p' corpus/evidence/sources-r52/util.c.v7.2
		mm_compute_batch(new_policy);
	return percpu_counter_sum_positive(&vm_committed_as);
	if (percpu_counter_read_positive(&vm_committed_as) < allowed)
exit=0
```

So every `util.c.v7.2:NNN` locator in this report (and in the entry) indexes the same bytes the entry committed.

## The rule at v7.2 (quotes ≤ 25 words, line numbers from the fetched files)

The batch (`mm/mm_init.c`, CONFIG_SMP):

| line | quote |
|---|---|
| 189 | `s32 vm_committed_as_batch = 32;` |
| 194 | `s32 nr = num_present_cpus();` |
| 195 | `s32 batch = max_t(s32, nr*2, 32);` |
| 196 | `unsigned long ram_pages = totalram_pages();` |
| 199–200 | `For policy OVERCOMMIT_NEVER, set batch size to 0.4% of (total memory/#cpus), and lift it to 25% for other policies` |
| 204–207 | `if (overcommit_policy == OVERCOMMIT_NEVER)` / `memsized_batch = min_t(u64, ram_pages/nr/256, INT_MAX);` / `else` / `memsized_batch = min_t(u64, ram_pages/nr/4, INT_MAX);` |
| 209 | `vm_committed_as_batch = max_t(s32, memsized_batch, batch);` |
| 228 | `mm_compute_batch(sysctl_overcommit_memory);` (initcall) |
| 218 | `mm_compute_batch(sysctl_overcommit_memory);` (memory-hotplug notifier) |

The batch is recomputed on a policy write, and mode 2 also syncs every CPU (`mm/util.c`):

| line | quote |
|---|---|
| 831 | `mm_compute_batch(new_policy);` |
| 832–833 | `if (new_policy == OVERCOMMIT_NEVER)` / `schedule_on_each_cpu(sync_overcommit_as);` |

The approximate read, and the exact one behind the meminfo line:

| file:line | quote |
|---|---|
| util.c:994 | `if (percpu_counter_read_positive(&vm_committed_as) < allowed)` |
| util.c:939 | `return percpu_counter_sum_positive(&vm_committed_as);` |
| percpu_counter.h:108–111 | `static inline s64 percpu_counter_read(struct percpu_counter *fbc)` / `return fbc->count;` |
| percpu_counter.c:100 | `if (unlikely(abs(count + amount) >= batch)) {` |
| percpu_counter.c:298 | `if (abs(count - rhs) > (batch * num_online_cpus())) {` |
| meminfo.c:46 | `committed = vm_memory_committed();` |

Two facts follow, and they are the substance of the error:

1. `percpu_counter_read()` returns **only `fbc->count`**, the global field. The per-CPU residues are not read at all,
   so the deviation is the sum of the residues, each `< batch` (the fold happens at `abs(count + amount) >= batch`,
   percpu_counter.c:100). Bound: `nr_cpus × (batch - 1)` pages; the kernel's own rough-count bound in
   percpu_counter.c:298 is `batch * num_online_cpus()`. Sign: allocation-heavy load leaves positive residues, so the
   read **understates** and the test is lenient; `vm_unacct_memory` can leave negative residues, so it can also
   refuse early. Both directions are inside the same bound.
2. The batch is **policy-derived**, not a constant: `ram_pages/nr/256` under NEVER, `ram_pages/nr/4` otherwise, with a
   `max(nr*2, 32)` floor. On a host that boots mode 0 and is switched to mode 2 by the sysctl, util.c:831 recomputes
   it *before* the sync, so mode 2 does get the small batch. (Had that line been absent, a switched host would keep a
   7.56 GiB band — the counterfactual is why the ordering comment at util.c:814–823 exists.)

### `ram_pages` from `MemTotal` (so the numbers are reproducible from `/proc/meminfo` alone)

`si_meminfo()` sets `val->totalram = totalram_pages();` (show_mem.c:77); `show_val_kb()` prints `num << (PAGE_SHIFT -
10)` (meminfo.c:30) and MemTotal is `show_val_kb(m, "MemTotal:       ", i.totalram);` (meminfo.c:60). With 4 KiB pages,
`ram_pages = MemTotal_kB / 4` **exactly** = 31721796/4 = 7 930 449 pages. `HugePages_Total: 0` on this host, so the
hugetlb term that `vm_commit_limit()` subtracts (and `mm_compute_batch()` does not) is zero here — see finding 4.

## This host's numbers

`nr = num_present_cpus() = 32` (present `0-31`, online `0-31`, `nproc` 32); `ram_pages = 7930449`;
floor `max(nr*2, 32) = 64`.

| policy | `memsized_batch` (mm_init.c:204–207) | batch (line 209) | per CPU | worst-case band `batch × 32` | share of RAM |
|---|---|---|---|---|---|
| 2 (NEVER) | 7930449/32/256 = **968** | 968 pages | 3.78 MiB | 30976 pages = **121.0 MiB** (tight, batch−1: 120.88 MiB) | **0.3906 %** |
| 0 / 1 (GUESS / ALWAYS) | 7930449/32/4 = **61956** | 61956 pages | 242.02 MiB | 1982592 pages = **7744.5 MiB = 7.56 GiB** | 24.9997 % |

The host runs mode 0 today (`/proc/sys/vm/overcommit_memory` = 0), so its *current* batch is the 61956-page one and the
current band is 7.56 GiB — but the limit is not enforced in mode 0 at all, so that band is invisible. Under mode 2 the
band is 121.0 MiB, i.e. 0.39 % of RAM by construction.

Context for a reading rule (live numbers, mode 0, limit unenforced): `CommitLimit` 47583772 kB = 45.38 GiB,
`Committed_AS` 40122148 → 40154220 kB = 38.26 → 38.30 GiB, headroom 7286.7 → 7255.4 MiB. The mode-2 band would be
1.66–1.67 % of that headroom: a `Committed_AS` within ~121 MiB of the enforcement threshold is inside the counter's
error band, not at a sharp edge. (`allowed` is not `CommitLimit`: `__vm_enough_memory` also subtracts
`sysctl_admin_reserve_kbytes` for non-`CAP_SYS_ADMIN` and `min(mm->total_vm/32, user_reserve)` — util.c:982–993 — so
the refusal threshold sits below `CommitLimit`, and the band is the slack in *that* comparison.)

Arithmetic reproduced verbatim (python3, integer division as the C does):

```
ram_pages=7930449 nr_present_cpus=32 floor_batch=64
mode2:   memsized=968   batch=968   pages  per_cpu=3.78 MiB  band=121.00 MiB (30976 pages)   tight=120.88 MiB
mode0/1: memsized=61956 batch=61956 pages  per_cpu=242.02 MiB band=7744.50 MiB (1982592 pages) tight=7744.38 MiB
mode2 band as pct of RAM = 0.3906%   mode0/1 band as pct of RAM = 24.9997%
ratio check: CommitLimit kB vs MemTotal*50/100+SwapTotal = 47583774 kB   (printed 47583772; page-granular rounding)
```

The ratio check confirms the host really is at `overcommit_ratio` 50 with swap added and no hugetlb subtraction
(47 583 772 vs 47 583 774 kB, 2 kB = rounding of `ram_pages*ratio/100`), which independently corroborates S499's
`allowed` formula against this host's two meminfo lines.

## Does this belong in the entry's Boundaries?

**Yes — as a replacement for the second sentence of the existing bullet, not a new bullet.** Today's text
(`corpus/knowledge/overcommit-commit-limit-r52.md:71-72`) reads: the meminfo line is the full sum, the mode-2 test uses
a cheaper approximate read, "The two can differ by up to the batch size per CPU." Every clause is right; what is
missing is the magnitude and the policy dependence, and those are exactly the two things a reader cannot recover
without opening mm_init.c. The bound `batch × nr_cpus` is also the kernel's own (percpu_counter.c:298), so citing it
is not a mori invention.

Draft, one sentence, for the L1 to place after the existing first sentence of that bullet (locators in the entry's own
`file.v7.2:NNN` style):

```text
The mode-2 test compares a lagged read with the limit (`util.c.v7.2:994`; `percpu_counter_read()` returns only the
global field, `percpu_counter.c.v7.2:108-111`), so what it sees trails the true sum by at most `batch × nr_cpus` pages
— the bound `percpu_counter.c.v7.2:298` itself uses — and `mm_compute_batch()` derives that batch from the policy
(`mm_init.c.v7.2:191-209`), re-run by the policy write (`util.c.v7.2:831`): at 32 CPUs and 7,930,449 RAM pages the
mode-2 batch is 968 pages, a 121.0 MiB band (0.39% of RAM), whereas the mode-0/1 batch is 61956 pages, 7.56 GiB (25%
of RAM), which is why switching to mode 2 recomputes the batch and syncs every CPU first (`util.c.v7.2:832-833`).
```

It is one sentence; if the L1 prefers two, split at the `:` after `util.c.v7.2:831` — no content changes. It replaces
the clause "The two can differ by up to the batch size per CPU." (which it strictly contains), so the bullet keeps its
two-sentence shape if the first sentence is left as is.

## Integration constraints the L1 must know

1. **Prose only — no new S-row.** `mm_init.c`, `percpu_counter.c` and `percpu_counter.h` are not among the five frozen
   copies. `count-c2.py` maps exactly five URLs (`count-c2.py:55-65`), and a SOURCES row naming any other URL gets
   `url = None` → `row_ok` false → `bad_rows` → `C2=unmet` (`count-c2.py:220-240`). A sixth source is therefore not
   integrable this round; the sentence must sit in Boundaries prose, which the counter never scans (it reads the 14
   non-blank head lines, the claims table and the votes only). This is the same class of limit as the entry's existing
   `util.c.v7.2:937-940` prose locators — but note the difference: `util.c` *is* a committed copy, `mm_init.c` is not.
2. **`mman.h` cannot carry the rule.** The committed copy declares the symbol —
   `extern s32 vm_committed_as_batch;` (`mman.h.v7.2:65`) and uses it at `mman.h.v7.2:78` — but the *sizing formula*
   exists only in mm_init.c. Citing mman.h:65 alone would name the batch without a value.
3. **Numbers are host-specific.** "32 CPUs / 7,930,449 pages" is this host. If the L1 prefers a host-neutral sentence,
   the same content is: "the band is `ram_pages/256` under mode 2 and `ram_pages/4` under modes 0/1" — i.e. 0.39 % vs
   25 % of RAM, independent of CPU count, which is the cleanest form for a knowledge entry. My draft keeps the
   concrete host numbers because the entry's own Boundaries cites this host's readings elsewhere; either is faithful.
4. **No counter or predicate change is requested.** Nothing here proposes a change to P-C2, `count-c2.py` or the
   controls.

## Named limits of this measurement

- `batch × nr_cpus` is a **worst-case bound**, reachable only if every CPU holds a near-`batch` residue at the same
  instant (32 threads each accruing ~967 single-page charges on distinct CPUs without folding). Typical lag is far
  smaller; the entry must not imply a routine 121 MiB error.
- `nr` is `num_present_cpus()` (mm_init.c:194), not `num_online_cpus()`; on this host they agree (32/32), on a host with
  offline CPUs the recomputation from `nproc` would be low. The kernel's compare bound uses `num_online_cpus()`
  (percpu_counter.c:298), so bound and batch use different CPU counts — harmless, but worth not conflating.
- `mm_compute_batch()` uses `totalram_pages()` **without** the hugetlb subtraction `vm_commit_limit()` applies, so on a
  host with reserved hugepages the batch is slightly larger than `(MemTotal − hugetlb)/nr/256`. Here `HugePages_Total`
  is 0, so the numbers above need no correction.
- I did not read `/proc/zoneinfo`, `/proc/vmstat` or any per-CPU counter: the residues are not observable from
  userspace in aggregate, so the band is computed from the source, not measured.
- `Committed_AS` moved between two reads 8 minutes apart (40122148 → 40154220 kB); every headroom figure above is
  labelled with its read.
- I did not run `count-c1.py` or `count-c2.py`; scoring is the L1's seat. The `entailed=0` state I saw in
  `evidence/c2-at-data.txt` is unchanged by this report (no ENTAIL lines from this seat).

## Findings

1. **MED — the Boundaries sentence is true but uncomputable, and the wrong batch is 64× the right one.**
   `corpus/knowledge/overcommit-commit-limit-r52.md:72` ("can differ by up to the batch size per CPU") gives no
   magnitude and no policy dependence. A reader who assumes the batch is a fixed 32 pages, or who carries the
   mode-0/1 batch (242 MiB/CPU) into a mode-2 reading, is off by 3.78 MiB vs 121.0 MiB vs 7.56 GiB. Fix is the fenced
   sentence above; no predicate or counter change.
2. **MED — the mode-2 reading rule has no error-band row.** The Reading-rules table
   (`overcommit-commit-limit-r52.md:56-61`) warns that `Committed_AS > CommitLimit` is normal under modes 0/1, but says
   nothing about mode 2, where the printed line (exact, util.c:939) can sit up to ~121 MiB on this host from the
   threshold the kernel actually compares (lagged, util.c:994). A host read within that band is not evidence of a
   broken ledger, and a refusal slightly *before* `CommitLimit` is not evidence of a leak (reserves at util.c:982–993
   also lower `allowed`). Suggested as a routed item for round 53 or an L1 data correction — I did not draft the row
   because my seat asked for the Boundaries sentence only.
3. **MED — the sizing locators cannot be made checkable this round.** The batch rule lives in `mm/mm_init.c`'s
   `mm_compute_batch()` and `lib/percpu_counter.c`, neither of which has a committed copy under
   `corpus/evidence/sources-r52/`; the frozen counter's five-URL `COPIES` map (`count-c2.py:55-65`) makes a sixth
   source row score `bad_rows`. Consequence: the new numbers rest on bytes a reader must re-fetch, and the entry's
   `recheck:` command does not include them. If the L1 wants them checkable, that is a round-53 freeze item (extend
   `COPIES` + a `recheck:` URL list), not a change to be smuggled in now. Concerns `count-c2.py:55-65,220-240` and
   `overcommit-commit-limit-r52.md:9` (the `recheck:` line).
4. **LOW — batch and limit use different RAM bases and different CPU counts.** `mm_compute_batch()` divides
   `totalram_pages()` with no hugetlb subtraction and by `num_present_cpus()` (`mm_init.c:194-196`), while
   `vm_commit_limit()` subtracts `hugetlb_total_pages()` (`util.c` S499 quote) and percpu_counter.c:298 bounds by
   `num_online_cpus()`. Immaterial here (`HugePages_Total: 0`, present = online = 32) but it is why a host-neutral
   restatement should say "0.39 % / 25 % of RAM" rather than quote a page count.
5. **LOW — the bound is two-sided and the draft says "trails".** Negative residues from `vm_unacct_memory` can make the
   read *overstate*, so mode 2 can also refuse slightly early. My sentence's "trails … by at most" describes the
   allocation path (the common case); if the L1 wants strict symmetry, "differs from … by at most" is the safe wording.
   Concerns the fenced draft only.

## Cleanup, tooling, host state

- Scratch `/fast/scratch/hyaku/mori-r52/Mo52ExecBatchDeviation/` (fetched sources, `compute.txt`, `evidence-raw.txt`,
  `tmp/`) removed after this report was written; nothing cited lives only there — every quote and number above is in
  the report.
- No tools installed or upgraded (no `uv`, `npx`, `pacman`; pacman is paused host-wide anyway). No git/jj mutation in
  the lane or the fleet root; the only lane reads were `git`-free file reads and one `sed -n` over a committed copy.
- Host reads were `/proc/meminfo`, `/proc/sys/vm/overcommit_{memory,ratio,kbytes}`, `/sys/devices/system/cpu/{present,online}`
  and `nproc` — detection only, no write, no allocation, no cgroup/swap/watermark touch, no kernel-log read.
- Files written: this report only. Files the frozen instruments created inside the lane: none.
