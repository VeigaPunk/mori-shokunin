# Mo52ExecHostCommit — read-only host check of the C2 entry's CommitLimit formula

Seat: `Mo52ExecHostCommit` (executor, leaf). Round 52, wave `w1`.
Host: linux `7.2.11-arch1-1`, x86_64, `PAGESIZE=4096` (`PAGE_SHIFT=12`).
Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ExecHostCommit/` (removed at end; `/fast/scratch/hyaku` 614.7 G free at
`scripts/hyaku/disk-guard.sh status`, 24 % used).
Scope: this is own-work evidence for the L1; it is **not** claimed by
`corpus/knowledge/overcommit-commit-limit-r52.md`, whose boundaries say the entry claims what the v7.2 bytes say and
not this host's sysctl values.

## 1. What was run

Read-only, twice, 14 s apart (two independent snapshots so a moving `Committed_AS` cannot be mistaken for a
constant):

```
date -u +%Y-%m-%dT%H:%M:%SZ
for f in overcommit_memory overcommit_ratio overcommit_kbytes user_reserve_kbytes admin_reserve_kbytes; do
  printf 'vm.%s = ' "$f"; cat /proc/sys/vm/$f; done
uname -r; getconf PAGESIZE
grep -E '^(MemTotal|SwapTotal|Hugetlb|HugePages_Total|Hugepagesize|CommitLimit|Committed_AS|MemAvailable|MemFree):' /proc/meminfo
# then: sleep 5; repeat date + the same grep + cat overcommit_memory/ratio/kbytes
```
No sysctl was written, no cgroup/swap/watermark touched, no allocation made, no kernel-log message text grepped.
Exit code 0 for both read batches. `cat /proc/swaps` was read once (§7).

## 2. Raw reads (verbatim)

Read 1, `2026-10-27T00:10:09Z`:

```
vm.overcommit_memory = 0
vm.overcommit_ratio = 50
vm.overcommit_kbytes = 0
vm.user_reserve_kbytes = 131072
vm.admin_reserve_kbytes = 8192
7.2.11-arch1-1
4096
MemTotal:       31721796 kB
MemFree:         2129964 kB
MemAvailable:   19117996 kB
SwapTotal:      31722876 kB
CommitLimit:    47583772 kB
Committed_AS:   40153484 kB
HugePages_Total:       0
Hugepagesize:       2048 kB
Hugetlb:               0 kB
```

Read 2, `2026-10-27T00:10:23Z`:

```
2026-10-27T00:10:23Z
MemTotal:       31721796 kB
MemFree:         2373952 kB
MemAvailable:   18432392 kB
SwapTotal:      31722876 kB
CommitLimit:    47583772 kB
Committed_AS:   40134276 kB
HugePages_Total:       0
Hugepagesize:       2048 kB
Hugetlb:               0 kB
---
0
50
0
```

(The last three lines are `vm.overcommit_memory`, `vm.overcommit_ratio`, `vm.overcommit_kbytes` in that order.)
`CommitLimit` is identical in both reads (47 583 772 kB); `Committed_AS` moved by 19 208 kB downward between them.

## 3. The formula, as frozen

`corpus/evidence/sources-r52/util.c.v7.2:900-916` (frozen copy; sha256 listed in
`.ufo/waves/round-52/evidence/freeze-sha256.txt`):

```
901  * Committed memory limit enforced when OVERCOMMIT_NEVER policy is used
903 unsigned long vm_commit_limit(void)
904 {
905 	unsigned long allowed;
907 	if (sysctl_overcommit_kbytes)
908 		allowed = sysctl_overcommit_kbytes >> (PAGE_SHIFT - 10);
909 	else
910 		allowed = ((totalram_pages() - hugetlb_total_pages())
911 			   * sysctl_overcommit_ratio / 100);
912 	allowed += total_swap_pages;
914 	return allowed;
915 }
```

`allowed` is in **pages**; the print side converts back, one shift the other way:
`corpus/evidence/sources-r51/meminfo.c.v7.2:28-32` (`show_val_kb`: `num << (PAGE_SHIFT - 10)`), `:125`
(`show_val_kb(m, "CommitLimit:    ", vm_commit_limit());`), `:126`
(`show_val_kb(m, "Committed_AS:   ", committed);`), `:46` (`committed = vm_memory_committed();`), and
`util.c.v7.2:937-940` (`vm_memory_committed` = `percpu_counter_sum_positive`). So the printed lines are exactly
`vm_commit_limit()` and the full per-CPU sum, under every mode — the mode-2 test itself uses the *approximate*
`percpu_counter_read_positive` at `util.c.v7.2:994`, as the entry's Boundaries section already says.

## 4. Computation from the host reads

`PAGE_SHIFT - 10 = 2`, i.e. 4 kB per page.

| quantity | read 1 | read 2 |
|---|---|---|
| branch taken | ratio (`overcommit_kbytes == 0`) | ratio |
| `totalram_pages()` (`MemTotal`) | 31 721 796 kB → **7 930 449** pages | same |
| `hugetlb_total_pages()` (`HugePages_Total` = 0, `Hugetlb` = 0 kB) | **0** pages | 0 |
| ratio term `(7930449 - 0) * 50 / 100` | **3 965 224** pages | same |
| `total_swap_pages` (`SwapTotal` 31 722 876 kB) | **7 930 719** pages | same |
| `allowed = ratio + swap` | **11 895 943** pages | same |
| computed limit in kB (`<< 2`) | **47 583 772 kB** | 47 583 772 kB |
| printed `CommitLimit` | 47 583 772 kB | 47 583 772 kB |
| **difference** | **0 kB = 0 pages** | **0 kB = 0 pages** |
| `Committed_AS` | 40 153 484 kB = 10 038 371 pages | 40 134 276 kB = 10 033 569 pages |

Driver: `python3 calc.py` in scratch (integer arithmetic only, `//`), exit 0, printed the table above.

The match is exact in both snapshots. Two discriminators make the match meaningful rather than accidental:

- **Truncation, not rounding.** `7930449 * 50 / 100 = 3 965 224.5`. Integer division gives 3 965 224 → 11 895 943
  pages → 47 583 772 kB (printed). Rounding half-up would give 3 965 225 → 11 895 944 pages → 47 583 776 kB. The
  host prints the truncated value, so the C `/ 100` really does drop the half page.
- **Swap is counted whole, not free.** `SwapTotal` (all pages) is what makes the sum match; `SwapFree`
  (`/proc/swaps` shows 5 892 192 kB used) is 23 830 684 kB and does not appear in the arithmetic. The entry's "every
  swap page then added on top" is the correct reading, and a free-swap reading would be off by ~5.9 GB.

## 5. Mode, and whether the limit is enforced here

`vm.overcommit_memory = 0` (`OVERCOMMIT_GUESS`) — the heuristic mode, which is the compiled-in default
(`util.c.v7.2:781`, `int sysctl_overcommit_memory __read_mostly = OVERCOMMIT_GUESS;`). Reading order in
`__vm_enough_memory` (`util.c.v7.2:969-978`): `OVERCOMMIT_ALWAYS` → return 0 (never refuse); `OVERCOMMIT_GUESS` →
refuse only `pages > totalram_pages() + total_swap_pages`, then return 0; only the fall-through path (mode 2)
computes `allowed = vm_commit_limit()` and compares. So on this host the printed `CommitLimit` is **computed and
published but never compared against anything** — the entry's sentence "CommitLimit is printed under every mode, but
it is enforced only under mode 2" is confirmed by both the frozen bytes and this host's mode.

Documentation agreement (frozen copies, same claim): `overcommit-accounting.rst.v7.2:33-38` — the two knobs "only
have an effect when `vm.overcommit_memory` is set to 2", and the two values are "viewable in `/proc/meminfo` as
CommitLimit and Committed_AS respectively".

## 6. Does Committed_AS exceed CommitLimit here?

**No.** 40 153 484 kB vs 47 583 772 kB (read 1) = **84.38 %** of the limit, 7 430 288 kB headroom; read 2 84.34 %,
7 449 496 kB headroom. Listed in order, the answer to the three questions asked:

- active mode: **0 (heuristic)**;
- `Committed_AS` vs `CommitLimit`: **below** the limit (≈ 84 %), so not exceeded — and under mode 0 it would not
  matter either way, because the comparison is never made;
- the printed limit is nevertheless exactly `vm_commit_limit()` (0 kB / 0 pages difference), so the formula is
  exercised and verified on this host even though it is unenforced.

Two observations that keep this from being read as a runway alarm. `MemAvailable` was 19.1 GB / 18.4 GB over the
same window while `Committed_AS` was 40.1 GB — the ledger counts address space, not residency, which is the entry's
own distinction. And `Committed_AS` fell 19 208 kB in 14 s: the per-CPU batch is visible in the line
(`vm_acct_memory` → `percpu_counter_add_batch`, `mman.h.v7.2`, `vm_committed_as_batch`), so a single read is a
snapshot, not a constant. [INFERENCE] If the operator ever selected mode 2 on this host, the ~7.4 GB of headroom is
what new private writable mappings, `brk` and `fork` would have to fit into (with the non-CAP_SYS_ADMIN admin
reserve of 8192 kB removed first, `util.c.v7.2:982-983`, and up to `min(total_vm/32, 131072 kB)` removed per mm,
`:988-991`) — that is my arithmetic on the entry's rules, not something the entry claims.

## 7. Two entry statements the host read corroborates (adjacent to the formula)

- **Reserves are at their compiled-in maxima.** `vm.user_reserve_kbytes = 131072` kB and
  `vm.admin_reserve_kbytes = 8192` kB equal `1UL << 17` kB and `1UL << 13` kB (`util.c.v7.2:784-785`). The boot
  initialisers take `min(free_kbytes / 32, SZ_128K)` (`mmap.c.v7.2:1595`) and `min(free_kbytes / 32, SZ_8K)`
  (`mmap.c.v7.2:1616`); the `SZ_*` macros are KiB-sized but the knobs are in kB, so `SZ_128K` = 131072 kB = 128 MiB
  and `SZ_8K` = 8192 kB = 8 MiB — exactly what the entry's claim text says ("128 MiB", "8 MiB"), and exactly what
  the host prints. [INFERENCE] the clamp resolved to the ceiling, i.e. `free_kbytes / 32` was at or above those
  maxima at boot; the host read alone cannot show the boot-time value of `free_kbytes`.
- **Swap in the ledger is a swap file here.** `/proc/swaps`: `/swap/swapfile file 31722876 5892192 0` — the
  `total_swap_pages` term is a 30.2 GiB file, fully counted (see §4).

## 8. Named limits of this check (mine, not the counter's)

1. The **`overcommit_kbytes` branch (`util.c.v7.2:907-908`) is unexercised**: the host reads 0, and setting it is a
   `vm.*` write, which this lane never does. The frozen hunk shows `>> (PAGE_SHIFT - 10)`; the host cannot confirm
   its arithmetic.
2. The **`hugetlb_total_pages()` subtraction is neutralised**: `HugePages_Total = 0`, `Hugetlb = 0 kB`, so the
   formula reduces to `totalram_pages() * ratio / 100`. A host with reserved huge pages is the discriminating case
   and is not available.
3. `MemTotal` → `totalram_pages()` is the identity at `meminfo.c.v7.2:60` (`show_val_kb(..., i.totalram)` fed by
   `si_meminfo`); I did not reopen `si_meminfo`'s body in this seat, so "MemTotal kB / 4 is the function's input"
   rests on that identity plus the exact 0-page match.
4. One host, one boot, one kernel build (`7.2.11-arch1-1`), two snapshots 14 s apart. Nothing here speaks for other
   kernels, other ratios, or a host under memory pressure.
5. `Committed_AS` is compared to `CommitLimit` as printed; the mode-2 kernel test uses the *approximate* per-CPU
   read, so on a mode-2 host the printed pair and the enforced decision can differ by the batch per CPU.
6. I did not and cannot test the ENOMEM path without allocating or switching mode; no allocation was made.

## Findings

- **LOW** — `corpus/knowledge/overcommit-commit-limit-r52.md`, claim row for S499 ("CommitLimit is RAM minus hugetlb
  pages, scaled by the ratio percentage, with every swap page then added on top"): the paraphrase does not say that
  the `* ratio / 100` is **integer division on pages**, which drops the half page. Host discriminator: printed
  47 583 772 kB matches truncation to 3 965 224 pages, not rounding to 3 965 225 (47 583 776 kB). The quoted code
  (`* sysctl_overcommit_ratio / 100`) is right, so this is a precision note, not an error; optional wording:
  "integer-divided by the ratio percentage, truncating any fraction of a page".
- **LOW** — `corpus/knowledge/overcommit-commit-limit-r52.md`, same row / Boundaries: the host cannot exercise the
  `overcommit_kbytes` branch (reads 0) or the `hugetlb_total_pages()` subtraction (`HugePages_Total = 0`). Both are
  named limits of *this* check; if the entry is ever re-checked on a host with reserved huge pages, that is the
  discriminating case.
- **LOW** — `corpus/knowledge/overcommit-commit-limit-r52.md`, "Reading rules" row 1: consistent with this host
  (`Committed_AS` at 84 % of `CommitLimit` under mode 0, `MemAvailable` 18–19 GB, no refusal path active), so no
  calendar risk is implied by the ratio alone; the 7.4 GB of headroom only becomes binding if mode 2 is selected.
- **LOW** — frozen-asset note, no file change requested: `util.c.v7.2:903-916` as frozen excludes the
  `__vm_enough_memory` body the same entry cites at `:969-994`; the two hunks are consistent, and the print path had
  to be read from the round-51 copy (`corpus/evidence/sources-r51/meminfo.c.v7.2:28-32,46,125-126`) because
  `corpus/evidence/sources-r52/` holds no `fs/proc/meminfo.c`.
- No HIGH or MED findings. Nothing observed contradicts the entry's formula, the entry's mode claim, or the
  round-52 target text for C2.

## Evidence retained

Every command line above was run in this seat; exit codes 0 unless stated. Scratch
`/fast/scratch/hyaku/mori-r52/Mo52ExecHostCommit/` held only `calc.py` (the arithmetic driver) and `tmp/`, and was
removed with `rm -rf` after this report was written. No file was created or modified inside
`/home/vgpnk/Projects/shokunin/mori-shokunin` or `/home/vgpnk/Projects/shokunin` by this seat, and no git or jj
mutation was issued. `/home/vgpnk/Projects/shokuknow` was not touched. No tool was installed or upgraded.
