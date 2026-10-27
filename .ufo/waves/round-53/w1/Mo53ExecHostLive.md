# Mo53ExecHostLive — live host check of `tools/mori-commit-runway.py` at `2a4213bf`

Seat: live host check of the C2 tool (one of the wave's tool attacks, host half). Revision measured:
`2a4213bf8da72f7cd78189baa5bb9be825dca1df`, extracted with `git -C …/mori-shokunin archive … | tar -x` into
`/fast/scratch/hyaku/mori-r53/Mo53ExecHostLive` and run as `python3 -I -B tools/mori-commit-runway.py` from that
extraction (never from the lane work tree). No file under the lane, `.ufo/waves/round-53/` (except this report) or
any PATH directory was written; `git -C …/mori-shokunin status --porcelain` before and after my runs shows only the
other seats' outputs (`evidence/selftests/`, `w1.ready`, `w1.ready.partial`, `w1/`), and
`find …/mori-shokunin -newermt '-60 minutes' -type f` returned nothing.

Byte identity of what I ran (`sha256sum`, archive copy = `git show 2a4213bf:<path>` = lane work tree):

```
80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156  tools/mori-commit-runway.py
cea8045192babe3017a2682c17a1647e73c597eaf0330a27643858577cc43b63  tools/fixtures/mori-commit-runway/cases.json
```

Host: kernel `7.2.11-arch1-1`, x86_64, page size 4096 (`getconf PAGE_SIZE`), `python3 -V` = `Python 3.14.8`,
`strace` present (`/usr/bin/strace`). Instrumentation: none installed; no pacman transaction run (host-wide pause
respected). Disk guard before the run: `bash scripts/hyaku/disk-guard.sh status` rc 0, `/fast` 612.6G free,
`/tmp` 123.9G free. MACHINE_ID omitted.

## 1. Host inputs read by hand (independent of the tool)

Command: `grep -E "^(MemTotal|SwapTotal|HugePages_Total|Hugetlb|CommitLimit|Committed_AS):" /proc/meminfo` and
`for f in overcommit_memory overcommit_ratio overcommit_kbytes admin_reserve_kbytes user_reserve_kbytes; do cat
/proc/sys/vm/$f; done`, `cat /sys/devices/system/cpu/present`, `getconf PAGE_SIZE`:

```
MemTotal:       31721796 kB
SwapTotal:      31722876 kB
HugePages_Total:       0
Hugetlb:               0 kB
CommitLimit:    47583772 kB
Committed_AS:   46141848 kB        (this sample; see §5 for drift)
overcommit_memory=0
overcommit_ratio=50
overcommit_kbytes=0
admin_reserve_kbytes=8192
user_reserve_kbytes=131072
cpu present = 0-31   (32 present CPUs)
PAGE_SIZE = 4096 (page_kb = 4)
```

Mode read from `/proc/sys/vm/overcommit_memory` is **0** (`OVERCOMMIT_GUESS`) — the Arch default, and the mode the
whole live reading below is taken in.

## 2. Three live runs

Command (from the extraction, `TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecHostLive/tmp`):

`for i in 1 2 3; do python3 -I -B tools/mori-commit-runway.py; echo "exit=$?"; done`

```
run 1 exit=0 {"band_kb": null, "batch_pages": null, "commit_limit_kb": 47583772, "committed_as_kb": 46089964,
  "cpus_present": 32, "enforced": false, "findings": [], "headroom_kb": 1493808, "limit_consistent": true,
  "limit_recomputed_kb": 47583772, "mode": 0, "notes": ["mode 0 (guess): only a single request above RAM + swap is
  refused; CommitLimit is printed, not enforced"], "reserve_kb": null, "schema": "mori-commit-runway-v1",
  "single_request_cap_kb": 63444672, "usable_kb": null, "verdict": "COMMIT_HEURISTIC"}
run 2 exit=0   same fields, committed_as_kb 46145364, headroom_kb 1438408
run 3 exit=0   same fields, committed_as_kb 46112288, headroom_kb 1471484
```

Every non-`Committed_AS` field was identical across the three runs (and across the strace run in §4:
`committed_as_kb 45953988`). Only `committed_as_kb`/`headroom_kb` move.

**Mode, verdict, findings: mode 0 → `COMMIT_HEURISTIC`, exit 0, `findings: []`, `headroom_kb` positive** in all
four live invocations. No `over_limit_not_enforced`, no `inside_band`, no `limit_mismatch`.

## 3. `vm_commit_limit()` recomputed by hand

Kernel body (`corpus/evidence/sources-r53/util.c.v7.3` lines 904-916, byte-identical logic to the v7.2 copy):

```
allowed = ((totalram_pages() - hugetlb_total_pages()) * sysctl_overcommit_ratio / 100);   /* pages */
allowed += total_swap_pages;                                                              /* pages */
return allowed;
```

and `fs/proc/meminfo.c` prints it through `show_val_kb(m, "CommitLimit:    ", vm_commit_limit())`, i.e.
`pages << (PAGE_SHIFT - 10)` = pages × 4 kB. The four conversions the tool must get right:

* `MemTotal_kB = totalram_pages << 2` (same `show_val_kb`; `si_meminfo` sets `val->totalram = totalram_pages()`,
  `corpus/evidence/sources-r53/show_mem.c.v7.3:78`), so `totalram_pages = 31721796 / 4 = 7930449` exactly.
* `SwapTotal_kB = i.totalswap << 2` with `i.totalswap` from `si_swapinfo` (`meminfo.c:44-45`), i.e.
  `total_swap_pages = 31722876 / 4 = 7930719` exactly.
* `Hugetlb` line = `sum(huge_page_size(h) * nr_huge_pages) / SZ_1K` (verified from
  `mm/hugetlb.c` @ v7.2 cgit, `hugetlb_report_meminfo`, http 200, 210457 bytes), while
  `hugetlb_total_pages()` (same file, line 4586) = `sum(nr_huge_pages * pages_per_huge_page(h))` — so
  `hugetlb_total_pages = Hugetlb_kB / page_kb`. On this host `Hugetlb = 0 kB → 0`; `HugePages_Total: 0` agrees.
* ratio path only because `overcommit_kbytes = 0`; the kbytes path is `kbytes >> (PAGE_SHIFT-10)` = `kbytes //
  page_kb`, which the tool also uses.

Arithmetic on this host:

```
ram_pages   = 31721796 // 4           = 7,930,449
huge_pages  =        0 // 4           = 0
ratio term  = (7,930,449 - 0) * 50 // 100
            = 396,522,450 // 100      = 3,965,224 pages   (floor; remainder 50)
swap pages  = 31722876 // 4           = 7,930,719
allowed     = 3,965,224 + 7,930,719   = 11,895,943 pages
in kB       = 11,895,943 * 4          = 47,583,772 kB
```

Printed `CommitLimit` = **47583772 kB**; the tool's `limit_recomputed_kb` = **47583772 kB**;
`commit_limit_kb` = 47583772; `limit_consistent: true`. **Exact agreement, my hand figure between them.** No
rounding advantage is being taken: the tool's `ram_pages = MemTotal // page_kb` is the same shift as the kernel's,
not a truncating re-division.

Mode-0 cap check: kernel `if (pages > totalram_pages() + total_swap_pages) goto error;` (util.c:972-975) →
`(7,930,449 + 7,930,719) * 4 = 63,444,672 kB`, which is exactly the tool's `single_request_cap_kb`. The kernel
does **not** subtract hugetlb here, and neither does the tool.

## 4. `strace -f -e trace=openat,write,connect` (live run)

Command: `strace -f -e trace=openat,write,connect -o strace-live.txt python3 -I -B tools/mori-commit-runway.py`
→ exit 0, JSON identical to §2 apart from `committed_as_kb`. 160 `openat` in total (most are the Python 3.14
interpreter and libc/zstd/lzma/locale), **8 host files, all `O_RDONLY|O_CLOEXEC`**:

```
openat(AT_FDCWD, "/proc/self/maps", O_RDONLY|O_CLOEXEC) = 3                          (cpython itself)
openat(AT_FDCWD, "/proc/meminfo", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/proc/sys/vm/overcommit_memory", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/proc/sys/vm/overcommit_ratio", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/proc/sys/vm/overcommit_kbytes", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/proc/sys/vm/admin_reserve_kbytes", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/proc/sys/vm/user_reserve_kbytes", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/sys/devices/system/cpu/present", O_RDONLY|O_CLOEXEC) = 3
```

* `openat` with `O_WRONLY`, `O_RDWR` or `O_CREAT`: **none**.
* Writes: **one**, `write(1, "{\"band_kb\": null, ...", 504) = 504` — stdout only. No other fd written.
* `connect(`: **0**. No socket, no network.
* No `unlink`/`rename` in the live run; `/proc/meminfo` is opened once and `CommitLimit`/`Committed_AS` therefore
  come from the same snapshot (no torn read between the two lines).

Selftest under the same trace (`--selftest`, `TMPDIR` set to the seat scratch): `MATCHER: rejected 23/23 corrupted
expectations` / `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23`, exit 0. It writes only inside
`$TMPDIR/mori-commit-runway-*` (`write(3, …)` ×160) and removes that directory: `ls -la "$TMPDIR"` afterwards
shows an empty directory. No write reaches `/tmp`, the lane, or any PATH directory.

## 5. Tool ↔ REF on a frozen host snapshot (and the mode-2 arm, in scratch only)

Snapshot of the host inputs into the scratch (`cp /proc/meminfo`, the five vm files, `cpu/present`), then the tool
pointed at the snapshot with `--meminfo --vm-dir --cpu-present`, and `count-c2.py`'s `ref()` imported read-only
from the lane and evaluated on the same bytes.

```
snap  (host mode 0):  ref_exit 0  tool_verdict COMMIT_HEURISTIC  field diffs: NONE
snap2 (mode forced 2, vm/overcommit_memory=2 in the scratch copy):
                      ref_exit 0  tool_verdict COMMIT_OK          field diffs: NONE
```

Mode-2 arithmetic on this host's real numbers, by hand, for the same snapshot
(`committed_as_kb 42003360` — the host was quieter at that moment):

```
batch = max(min(7,930,449 // 32 // 256, INT_MAX), max(2*32, 32))
      = max(min(247,826 // 256 = 968, INT_MAX), 64) = 968 pages
band  = 968 * 32 * 4                = 123,904 kB
reserve = 8192 + 131072             = 139,264 kB
headroom = 47,583,772 - 42,003,360  = 5,580,412 kB
usable   = 5,580,412 - 139,264      = 5,441,148 kB   (> band → COMMIT_OK)
```

The tool printed exactly `batch_pages 968, band_kb 123904, reserve_kb 139264, headroom_kb 5580412, usable_kb
5441148, verdict COMMIT_OK, exit 0`. The kbytes path also behaved: with `overcommit_kbytes = 1048576` in a scratch
vm-dir the tool printed `limit_recomputed_kb 32771452` (= `(1048576//4 + 7930719) * 4`) and raised
`limit_mismatch` against the printed 47583772, exit 0 — the documented "inputs misread" signal, correct.

The `over_limit_not_enforced` path is reachable but not reached live: on a snapshot with `Committed_AS` rewritten
to 60169456 kB (limit + 12585684, the delta the frozen fixture `host-mode0-over-limit` carries) the tool emitted
`{"id": "over_limit_not_enforced", "headroom_kb": -12585684}`, verdict `COMMIT_HEURISTIC`, exit 0.

Refusal-vs-printed direction, checked against the sources rather than asserted: /proc/meminfo `Committed_AS` is
`vm_memory_committed()` = `percpu_counter_sum_positive(&vm_committed_as)` (util.c:947-950), i.e. the exact sum,
while the mode-2 test compares `percpu_counter_read_positive(&vm_committed_as)` (util.c:994) — the global count
only. The per-CPU deltas are bounded by one batch each (percpu_counter.c `add_batch`), and they can be negative
because `vm_unacct_memory(-pages)` charges negative amounts through the same counter, so the enforced read can sit
up to one band on either side of the printed sum — which is why "printed room remains but refusal is possible"
is the correct reading of `COMMIT_LOW`, and why the tool's `usable_kb ≤ band_kb` rule is not simply a
one-directional conservatism. [INFERENCE on the sign range; the read/sum split itself is source-verified.]

Drift of the live quantity: six `/proc/meminfo` samples one second apart gave `CommitLimit` constant 47583772 kB
and `Committed_AS` 41,638,436 / 41,109,936 / 41,049,132 / 41,062,312 / 41,807,108 / 41,526,320 kB — a ~4.5 GB
swing in six seconds, after the ~46.1 GB readings of §2. `headroom_kb` inherits that noise.

## 6. Counter cross-check at the data commit (evidence, not mine to judge)

`python3 .ufo/waves/round-53/count-c2.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df --scratch
/fast/scratch/hyaku/mori-r53/Mo53ExecHostLive/c2scratch` →

```
C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok
rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df      exit 0
```

Nothing was written into the lane by that run (`find -newermt '-60 minutes'` clean). I did not touch the counter,
predicates or controls, and propose no change to them.

## 7. Limits of this check

* The host is mode 0, so the entire live reading is one branch: `band_kb`, `batch_pages`, `reserve_kb`,
  `usable_kb` are `null` live and the mode-2 band arm never runs against real `/proc`. My mode-2 numbers come from
  a scratch copy of the same inputs with `overcommit_memory` set to 2, not from the host's policy.
* One host, one kernel line, one page size (4 kB), `Hugetlb = 0` — the hugetlb and non-4 k page conversions are
  verified against the sources, not against a live system that exercises them.
* Tool↔REF agreement is a same-author consistency check; the independent legs are the hand arithmetic in §3 and
  §5 and the source reading in §5.
* I read, I did not mutate: no sysctl, cgroup, swap or watermark was touched; no allocation was made to push the
  ledger.

## Findings

1. **MED — `corpus/knowledge/commit-runway-read-r53.md` (§Reading rules, the live-host sentence).** The entry
   states that on this host on 2026-10-26 `Committed_AS` exceeds the printed limit and the tool reports
   `COMMIT_HEURISTIC` with `over_limit_not_enforced`. At check time (three live runs, a strace run, and a frozen
   snapshot) `Committed_AS` was 45,953,988–46,145,364 kB against `CommitLimit` 47,583,772 kB: headroom positive
   (+1.44 GB…+1.63 GB), `findings: []`, no `over_limit_not_enforced`. The finding is reachable (§5, snapshot at
   60,169,456 kB), so the sentence is a stale snapshot rather than a false rule; it is not reproducible as written
   and the value it saw is not stated. Suggested correction: name the observed `Committed_AS`
   (the fixture `host-mode0-over-limit` carries 60,169,456 kB) and mark the sentence as that snapshot.
2. **MED — `count-c2.py` live arm (coverage limit, routed to round 54; counter frozen).** `live_check()` compares
   only `mode`, `commit_limit_kb`, `limit_recomputed_kb`, `cpus_present`, `limit_consistent`. On a mode-0 host the
   other eight fields are `null`, so `live=ok` exercises none of the band rule — C2's distinguishing arithmetic is
   checked by fixtures alone. A mode-2 host (or a live leg that compares the band fields against a scratch
   mode-2 vm-dir) would cover it; this is a named limit for the report, not a counter change.
3. **LOW — `tools/mori-commit-runway.py`, the `Hugetlb` input (docstring Inputs, and `evaluate()`).** The tool
   derives hugetlb pages from the `/proc/meminfo` `Hugetlb` line, but that line is emitted by
   `mm/hugetlb.c:hugetlb_report_meminfo` (`"Hugetlb:        %8lu kB"`, `total / SZ_1K`) and the subtracted
   quantity is `hugetlb_total_pages()` in the same file — neither path is among the pinned rows S502–S513, and the
   pinned `fs/proc/meminfo.c` (S504) only calls `hugetlb_report_meminfo(m)`. I fetched `mm/hugetlb.c` and
   `include/linux/hugetlb.h` at v7.2 from cgit myself (both HTTP 200) and confirmed the conversion the tool uses
   (`Hugetlb_kB / page_kb == hugetlb_total_pages()`, including the 2 MB-page case and the
   `!CONFIG_HUGETLB_PAGE` stub returning 0); so the arithmetic is right, but the lane has no committed copy for
   the emitter it depends on.
4. **LOW — single-sample reading.** `Committed_AS` moved ~4.5 GB in six one-second samples (§5) and 45.95→46.15 GB
   across three consecutive invocations; `headroom_kb` (and therefore `usable_kb` near the edge) is a point-in-time
   number with a variance far larger than the 121 MiB band on this host. A runway read taken once per round should
   not be read as a trend. Windowed/max-of-N sampling is a round-54 candidate; the tool's own contract is a single
   read.
5. **LOW — reserve subtraction is in kB, the kernel's is in pages.** `__vm_enough_memory` does
   `allowed -= sysctl_admin_reserve_kbytes >> (PAGE_SHIFT - 10)` and `-= min_t(long, mm->total_vm / 32,
   user_reserve_kbytes >> (PAGE_SHIFT - 10))`, i.e. truncation to whole pages and the admin reserve only when
   `!cap_sys_admin`; the tool subtracts the raw kB of both reserves, always. Difference ≤ 3 kB per reserve plus the
   admin-reserve gap (8192 kB) for root, and every direction makes the tool's `usable_kb` ≤ the kernel's, so it is
   conservative; the entry documents the user-reserve worst case but not the page truncation.
