# Reading the commit ledger as runway: by mode, and under mode 2 inside the per-CPU error band

source: S499 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c — code, tier A, mm/util.c at tag v7.2 (vm_commit_limit, __vm_enough_memory, vm_memory_committed, the policy handler), opened 2026-10-26 (round 52)
source: S511 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/mm_init.c?h=v7.2 — code, tier A, mm/mm_init.c at tag v7.2 (mm_compute_batch), committed copy `corpus/evidence/sources-r53/mm_init.c.v7.2`, opened 2026-10-26
source: S512 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/lib/percpu_counter.c?h=v7.2 — code, tier A, lib/percpu_counter.c at tag v7.2 (percpu_counter_add_batch), committed copy `corpus/evidence/sources-r53/percpu_counter.c.v7.2`, opened 2026-10-26
source: S513 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/percpu_counter.h?h=v7.2 — code, tier A, include/linux/percpu_counter.h at tag v7.2 (percpu_counter_read_positive), committed copy `corpus/evidence/sources-r53/percpu_counter.h.v7.2`, opened 2026-10-26
verified-at: 2026-10-26
recheck: on-release — `python3 -I -B tools/mori-commit-runway.py --selftest` (the reading below as 23 frozen cases); at the next tag fetch the three paths with `curl -fsSL 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=<tag>'` and compare `mm_compute_batch`, `percpu_counter_add_batch` and `percpu_counter_read_positive` with the copies
coverage-map: resource runway (the commit ledger moves from knowledge, round 52, into a tool, `tools/mori-commit-runway.py`)

Round 52 said what `CommitLimit` and `Committed_AS` are and that the limit is enforced only under
`vm.overcommit_memory = 2` (`overcommit-commit-limit-r52.md`). A runway read needs one more fact: how close to the
limit the kernel's own test can be wrong. `Committed_AS` in /proc/meminfo is an exact sum over CPUs; the mode-2
test reads only the global part of a per-CPU counter, which lags the sum by less than one batch per CPU. The
batch is sized by policy: under mode 2 it is about 0.4 % of RAM per CPU, with a floor of `max(2 × CPUs, 32)`
pages. `tools/mori-commit-runway.py` reports, under mode 2, `usable_kb` (limit minus committed minus both
reserves) and `band_kb` (batch × present CPUs × page size), and says `COMMIT_LOW` when the usable room is inside
the band: there, a non-root allocation may already be refused although the printed numbers still show room.

## Claims

| claim | source | quote |
|---|---|---|
| Under mode 2 the batch of the committed-memory counter is RAM pages divided by CPUs and by 256, capped at INT_MAX. | S511 | `if (overcommit_policy == OVERCOMMIT_NEVER) memsized_batch = min_t(u64, ram_pages/nr/256, INT_MAX);` |
| The kernel comment states the mode-2 batch as 0.4 percent of memory per CPU and the looser modes' batch as 25 percent. | S511 | `For policy OVERCOMMIT_NEVER, set batch size to 0.4% of * (total memory/#cpus), and lift it to 25% for other policies` |
| The batch never falls below twice the present CPU count or 32 pages, whichever is larger. | S511 | `s32 nr = num_present_cpus(); s32 batch = max_t(s32, nr*2, 32);` |
| A CPU keeps adding into its own local delta and folds it into the global count only once the delta would reach the batch. | S512 | `if (unlikely(abs(count + amount) >= batch)) { raw_spin_lock_irqsave(&fbc->lock, flags);` |
| The mode-2 read takes only the global count and returns zero for a negative value, never summing the per-CPU deltas. | S513 | `s64 ret = READ_ONCE(fbc->count); if (ret >= 0) return ret; return 0;` |
| The mode-2 refusal compares that global-only read with the allowed figure, so the enforced value is approximate. | S499 | `if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;` |
| The figure printed as Committed_AS is the exact sum across CPUs, not the read the mode-2 test uses. | S499 | `unsigned long vm_memory_committed(void) { return percpu_counter_sum_positive(&vm_committed_as); }` |
| Switching the sysctl to mode 2 recomputes the batch and syncs every CPU before the new policy takes effect. | S499 | `1. changing the batch * 2. sync percpu count on each CPU * 3. switch the policy` |

## Reading rules (mori)

| mode | tool verdict | what the numbers mean | what they do not mean |
|---|---|---|---|
| 0 (guess, the default) | `COMMIT_HEURISTIC`, exit 0 | only one request larger than RAM + swap is refused (`single_request_cap_kb`); `CommitLimit` is printed, not enforced, and `Committed_AS` above it is normal (`over_limit_not_enforced` finding) | that the host is out of commit room |
| 1 (always) | `COMMIT_UNLIMITED`, exit 0 | the commit test always passes | anything about memory left; read `MemAvailable` (`memavailable-estimate-r51.md`) |
| 2 (never) | `COMMIT_OK` (0) or `COMMIT_LOW` (1) | `usable_kb` = CommitLimit − Committed_AS − admin_reserve_kbytes − user_reserve_kbytes; LOW when `usable_kb ≤ band_kb` | a calibrated alarm (FR8 stays open); the band is an upper bound, not a measured deviation; root keeps the admin reserve |
| any, inputs missing or malformed | `COMMIT_UNKNOWN`, exit 2 | the reason is in `notes` | a zero or a pass |

`limit_consistent` recomputes `vm_commit_limit()` from MemTotal, Hugetlb, SwapTotal and the ratio (or
`overcommit_kbytes`); a mismatch (`limit_mismatch`) means the reading of the inputs is off, not the kernel's.
On this host on 2026-10-26 (mode 0, 32 present CPUs, MemTotal 31721796 kB): the recomputed limit equals the
printed 47583772 kB and Committed_AS exceeds it — `COMMIT_HEURISTIC` with `over_limit_not_enforced`, exit 0.

## Boundaries

- v7.2 bytes, the host's kernel line (7.2.11); the batch rule is unchanged at v7.3 (`mm_compute_batch` in the
  v7.3 copy differs only by its line number).
- The band uses present CPUs and today's totalram; memory hotplug recomputes the batch, a balloon that changes
  totalram without hotplug does not, and offline CPUs' deltas are folded at hotplug — the band is a bound for the
  common case, not a proof.
- The per-process user reserve is `min(total_vm/32, user_reserve_kbytes)`; the tool subtracts the full reserve
  (worst case for a large process).
- Read-only. Choosing an overcommit mode, a ratio or a reserve is the operator's; OS-state triage is tsukuroi's.
