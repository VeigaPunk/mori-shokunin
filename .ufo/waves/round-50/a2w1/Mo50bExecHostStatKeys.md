# Mo50bExecHostStatKeys — round 50 a2w1 (host memory.stat key cross-check against v7.2 formatter)

Seat: leaf executor. No subagent and no labrat probe was needed: every step is a direct read-only command or a
local script whose full text is embedded below. Nothing was installed or upgraded; no pacman; no clone; no git
write; no host modification.

Scope of this seat (per dispatch): `uname -r`; the key names (not values) of ONE own user-session cgroup's
`memory.stat`; the key list the v7.2 formatter prints, extracted from the frozen
`corpus/evidence/sources-r50/memcontrol.c.v7.2` (`memory_stats[]` + `memcg_stat_format()` and the
`memcg_vm_event_stat[]` loop); then the four required comparisons: live-not-v7.2, v7.2-not-live, order match, and
whether the entry's CONFIG-conditional key list is consistent with what this host shows. The entry is
`corpus/knowledge/oom-memcg-stat-r50.md` at the attempt-2 landed rev `487941b9395e89678af0053cc443cdb49cdee6e3`
(working-tree bytes read; this seat did not re-hash the entry, a sibling seat owns the byte-identity check).

No kernel log was read or grepped (lane rule S351 / QUALITY 15). `cat /proc/version` is not kernel log message
text and was read only for the host build string; no kill record was touched.

Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bExecHostStatKeys/` (`TMPDIR` set there; the only files written were
`live-keys.txt`, `keysets.json`, `keysets2.json`, all containing key names only). `disk-guard.sh status` before the
run: rc=0, `/fast/scratch/hyaku` 23% used, 618.7G free. Scratch removed before yielding; every cited command and
output is copied into this report.

## 1. Host kernel and the cgroup file read

```
$ uname -r
7.2.11-arch1-1
$ echo $?          # rc=0

$ cat /proc/version
Linux version 7.2.11-arch1-1 (linux@archlinux) (gcc (GCC) 16.2.1 20260810, GNU ld (GNU Binutils) 2.47) #1 SMP PREEMPT_DYNAMIC Fri, 16 Oct 2026 00:28:58 +0000
                   # rc=0

$ id -u
1000
$ ls -l /sys/fs/cgroup/user.slice/user-1000.slice/memory.stat
-r--r--r-- 1 root root 0 Oct 26 05:50 /sys/fs/cgroup/user.slice/user-1000.slice/memory.stat
                   # rc=0
```

The host runs the **7.2 stable line** (7.2.11, Arch build), so it is inside the entry's stated "kernel v7.2 only"
window, not a later feature release.

Keys were extracted with a filter so no value ever left the kernel file into any file this seat holds:

```
$ awk '{print $1}' /sys/fs/cgroup/user.slice/user-1000.slice/memory.stat > "$S/live-keys.txt"
                   # awk rc=0, stderr empty, 72 lines
```

No value appears in this report, in the scratch files, or in the tool transcript (the only command that touched
the cgroup file emitted field 1 only).

## 2. Live key list (72 keys, in file order)

```
 1 anon                       19 file_thp                  37 pgdemote_kswapd            55 pgfault
 2 file                       20 shmem_thp                 38 pgdemote_direct            56 pgmajfault
 3 kernel                     21 inactive_anon             39 pgdemote_khugepaged        57 pgactivate
 4 kernel_stack               22 active_anon               40 pgdemote_proactive         58 pgdeactivate
 5 pagetables                 23 inactive_file             41 pgsteal_kswapd             59 pglazyfree
 6 sec_pagetables             24 active_file               42 pgsteal_direct             60 pglazyfreed
 7 percpu                     25 unevictable               43 pgsteal_khugepaged         61 swpin_zero
 8 sock                       26 slab_reclaimable          44 pgsteal_proactive          62 swpout_zero
 9 vmalloc                    27 slab_unreclaimable        45 pgscan_kswapd              63 zswpin
10 shmem                      28 slab                      46 pgscan_direct              64 zswpout
11 zswap                      29 hugetlb                   47 pgscan_khugepaged          65 zswpwb
12 zswapped                   30 workingset_refault_anon   48 pgscan_proactive           66 thp_fault_alloc
13 zswap_incomp               31 workingset_refault_file   49 pgrefill                   67 thp_collapse_alloc
14 file_mapped                32 workingset_activate_anon  50 pgpromote_success          68 thp_swpout
15 file_dirty                 33 workingset_activate_file  51 pgscan                     69 thp_swpout_fallback
16 file_writeback             34 workingset_restore_anon   52 pgsteal                    70 numa_pages_migrated
17 swapcached                 35 workingset_restore_file   53 pswpin                     71 numa_pte_updates
18 anon_thp                   36 workingset_nodereclaim    54 pswpout                    72 numa_hint_faults
```

(The list is a display reflow: read down each column in turn — 1–18, then 19–36, then 37–54, then 55–72 — which is exactly the file order.)

The entry's `kernel` aggregation claim is visible in the key set: `kernel_stack` (4), `pagetables` (5), `percpu`
(7), `vmalloc` (9) and `slab` (28) each print under their own name, next to the aggregate `kernel` (3).

## 3. v7.2 key list extracted from the frozen copy (script)

Source: `corpus/evidence/sources-r50/memcontrol.c.v7.2`, sha256
`8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e` (recomputed by this seat; equals line 2 of
`.ufo/waves/round-50/evidence/freeze-sha256.txt` and the entry's `recheck:` hash for memcontrol.c, so the parsed
bytes are the frozen ones).

Structure parsed, with anchors in that file:

- `memory_stats[]` at 1546–1609 (49 entries), gates at 1557 `CONFIG_ZSWAP`, 1565 `CONFIG_SWAP`,
  1568 `CONFIG_TRANSPARENT_HUGEPAGE`, 1580 `CONFIG_HUGETLB_PAGE`, 1606 `CONFIG_NUMA_BALANCING`.
- `memcg_stat_format()` at 1693; the loop at 1709–1725 prints the array in order, prints the aggregate `slab` line
  immediately after the `slab_unreclaimable` entry (1720–1724), and the aggregate `pgscan` (1728–1732) and
  `pgsteal` (1733–1737) lines after the array.
- `memcg_vm_event_stat[]` at 553–586 (gates at 554 `CONFIG_MEMCG_V1`, 566 `CONFIG_SWAP`, 570 `CONFIG_ZSWAP`,
  575 `CONFIG_TRANSPARENT_HUGEPAGE`, 581 `CONFIG_NUMA_BALANCING`); printed at 1739–1749 in array order.
- `memory_stat_format()` at 1751–1760 dispatches on `cgroup_subsys_on_dfl()`: v2 → `memcg_stat_format`, else
  `memcg1_stat_format` (1756); overflow warning at 1757–1759.

Script actually run (Python; parses the two arrays with `#ifdef` nesting, inserts the aggregate lines, maps enum
names, compares against the key-only extract):

```python
import os, re, subprocess
S = "/fast/scratch/hyaku/mori-r50/Mo50bExecHostStatKeys"
os.makedirs(S + "/tmp", exist_ok=True)
src = "/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r50/memcontrol.c.v7.2"
live_path = "/sys/fs/cgroup/user.slice/user-1000.slice/memory.stat"
p = subprocess.run(["awk", "{print $1}", live_path], capture_output=True, text=True)
live = p.stdout.split()
lines = open(src, encoding="utf-8", errors="replace").read().splitlines()

def parse_block(start_pat):
    i = next(k for k, l in enumerate(lines) if start_pat in l)
    gates, out = [], []
    for l in lines[i:]:
        s = l.strip()
        m = re.match(r'#ifdef\s+(CONFIG_\w+)', s)
        if m: gates.append(m.group(1)); continue
        if s.startswith('#ifndef'): gates.append('!' + s.split()[1]); continue
        if s.startswith('#endif'): gates.pop(); continue
        gm = re.search(r'\{ "([^"]+)"', s)
        if gm: out.append((gm.group(1), tuple(gates)))
        em = re.match(r'([A-Z][A-Z0-9_]+),\s*$', s)
        if em and 'memory_stat ' not in start_pat: out.append((em.group(1), tuple(gates)))
        if s == '};' and out: break
    return out

mem = parse_block('static const struct memory_stat memory_stats[] = {')       # 49
idx = [n for n, _ in mem].index('slab_unreclaimable')
expected = mem[:idx + 1] + [('slab', ())] + mem[idx + 1:]                    # aggregate slab
expected += [('pgscan', ()), ('pgsteal', ())]                                # aggregate events
ev = parse_block('static const unsigned int memcg_vm_event_stat[] = {')      # 22 with CONFIG_MEMCG_V1
name = lambda e: 'numa_pages_migrated' if e == 'NUMA_PAGE_MIGRATE' else e.lower()
expected += [(name(n), g) for n, g in ev]
# PGPGIN/PGPGOUT never reach a v2 memory.stat: array-gated by CONFIG_MEMCG_V1 (554) AND
# skipped unconditionally in the print loop under that same gate (1740-1744)
exp_v2 = [n for n, _ in expected if n not in ('pgpgin', 'pgpgout')]

import hashlib
print("live count", len(live))
print("memory_stats entries:", len(mem))
print("vm_event entries:", len(ev))
print("expected(all-gates) count", len(expected))
print("expected(v2-printable) count", len(exp_v2))
print("live-not-v72:", sorted(set(live) - set(exp_v2)))
print("v72-not-live:", sorted(set(exp_v2) - set(live)))
print("ORDER identical:", live == exp_v2)
print("sha256(memcontrol.c.v7.2):", hashlib.sha256(open(src, "rb").read()).hexdigest())
```

Observed output (two passes: the first took every `#ifdef` gate literally, the second is the v2-printable list):

```
# pass 1, all gates literal
awk rc 0 stderr ''
live count 72
memory_stats entries: 49
vm_event entries: 22
expected (all CONFIG on) count 74
SET live-not-v72: []
SET v72-not-live: ['pgpgin', 'pgpgout']
ORDER identical: False
first order divergence at 52 live= pswpin expected= pgpgin
lengths 72 74

# pass 2, v2-printable
expected(v2-printable) count 72 live count 72
live-not-v72: []
v72-not-live: []
ORDER identical: True
sha256(memcontrol.c.v7.2): 8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e
```

The 74-versus-72 gap in pass 1 is only `pgpgin`/`pgpgout`: they are in `memcg_vm_event_stat[]` under
`CONFIG_MEMCG_V1` (554–557) and the v2 print loop skips exactly those two under the same gate (1740–1744), so they
cannot appear in any cgroup-v2 `memory.stat`; pass 2 is therefore the correct expectation and it equals the live
list exactly.

So the v7.2 formatter's printable key sequence is exactly: 49 array keys (with all CONFIG gates on) + `slab` +
`pgscan` + `pgsteal` + 20 `memcg_vm_event_stat[]` names = **72 keys**, and the live `memory.stat` of
`user.slice/user-1000.slice` is those 72 keys **in the same order, with no insert, rename or extra key**.

## 4. The four required comparisons

| check | result | evidence |
|---|---|---|
| keys live but not in v7.2 | **none** (`[]`) | section 3 script output |
| keys v7.2 prints but not live | **none** (`[]`) — the only candidates were `pgpgin`/`pgpgout`, which a v2 hierarchy never prints: the array carries them only under `CONFIG_MEMCG_V1` (554) and the v2 print loop skips exactly those two under the same gate (1741–1743) | section 3 |
| order match | **exact**, all 72 positions: `live == exp_v2` is `True`; the aggregate `slab` sits at live position 28 immediately after `slab_unreclaimable` (27), matching 1721–1724, and `pgscan`/`pgsteal` sit at 51/52 right before the event counters, matching 1728–1737 | section 2/3 |
| entry's CONFIG-conditional key list vs this host | **consistent but not exhaustive** (see section 5) | sections 5–6 |

## 5. The entry's CONFIG-conditional key list against the source and the host

Entry text (`corpus/knowledge/oom-memcg-stat-r50.md:50-51`, Reading rules): "The key set is also compile-time
conditional — `zswap`, `zswapped`, `swapcached`, `anon_thp`, `file_thp`, `shmem_thp` and `hugetlb` are printed
only under their CONFIG options, so a missing key is not a zero."

Gated keys actually in v7.2, with the gate anchors and this host's observation (presence of one key proves its
gate compiled on; the script's gate table):

| gate | gated keys in v7.2 | live |
|---|---|---|
| `CONFIG_ZSWAP` (1557, 570) | `zswap`, `zswapped`, `zswap_incomp`, `zswpin`, `zswpout`, `zswpwb` | all 6 present → gate on |
| `CONFIG_SWAP` (1565, 566) | `swapcached`, `swpin_zero`, `swpout_zero` | all 3 present → gate on |
| `CONFIG_TRANSPARENT_HUGEPAGE` (1568, 575) | `anon_thp`, `file_thp`, `shmem_thp`, `thp_fault_alloc`, `thp_collapse_alloc`, `thp_swpout`, `thp_swpout_fallback` | all 7 present → gate on |
| `CONFIG_HUGETLB_PAGE` (1580) + runtime root flag (1681–1691, 1713–1716) | `hugetlb` | present → gate on **and** the hugetlb-accounting root flag is on |
| `CONFIG_NUMA_BALANCING` (1606, 581) | `pgpromote_success`, `numa_pages_migrated`, `numa_pte_updates`, `numa_hint_faults` | all 4 present → gate on |
| `CONFIG_MEMCG_V1` (554) | `pgpgin`, `pgpgout` — never print on a v2 hierarchy (1741–1743) | absent, as expected |

Every one of the seven keys the entry names is present live, so nothing in the entry's sentence is contradicted by
this host. The host also shows **all** gates compiled on, so it cannot exercise the "missing key is not a zero"
branch at all: this observation confirms the sentence's key examples and its principle, and leaves the gate-off
behavior UNVERIFIED.

Against the source the list is incomplete: 21 keys across the five compile-time gates (above), plus the
`CONFIG_MEMCG_V1` pair `pgpgin`/`pgpgout` which the array adds and the v2 print loop then skips; the entry names
7 of those 21 keys. The 14 unnamed gated keys are `zswap_incomp`, `swpin_zero`, `swpout_zero`, `zswpin`, `zswpout`,
`zswpwb`, `thp_fault_alloc`, `thp_collapse_alloc`, `thp_swpout`, `thp_swpout_fallback`, `pgpromote_success`,
`numa_pages_migrated`, `numa_pte_updates`, `numa_hint_faults`; and two gate families (`CONFIG_SWAP`,
`CONFIG_NUMA_BALANCING`) are not named at all. Nothing in the sentence is false ("printed only under their CONFIG
options" is a necessary condition, and it holds for all seven), so this is a completeness gap in the reading rule,
not a wrong claim. A reader applying the enumeration to a block from a kernel with `CONFIG_NUMA_BALANCING` or
`CONFIG_SWAP` off would not have the rule's text to explain the absent counters.

`hugetlb` has a second condition the entry does not mention: after the `CONFIG_HUGETLB_PAGE` gate (1580), the
formatter skips the key when the cgroup-v2 root's hugetlb accounting flag is off —
`if (unlikely(memory_stats[i].idx == NR_HUGETLB) && !memcg_accounts_hugetlb()) continue;` (1713–1716), where
`memcg_accounts_hugetlb()` reads `cgrp_dfl_root.flags & CGRP_ROOT_MEMORY_HUGETLB_ACCOUNTING` (1682–1690). What
sets that root flag is defined outside the three frozen copies (the string `memory_hugetlb_accounting` appears in
the copy only in a comment at 5397), so the enabling path is UNVERIFIED from these sources; the host's
`/sys/fs/cgroup` root listing shows `memory.numa_stat`, `memory.pressure`, `memory.reclaim`,
`memory.zswap.writeback` and no hugetlb knob, while `hugetlb` *is* in this cgroup's `memory.stat`, which is only
possible with the flag on. The entry's general rule ("a missing key is not a zero") still covers the case; only the
attribution to "their CONFIG options" is too narrow for this one key.

## 6. Limits section of the entry, bullet by bullet (read-only check)

| entry line | Limits bullet | check | verdict |
|---|---|---|---|
| 66–67 | "Kernel v7.2 only, read from the frozen copies whose sha256 the counter pins; later kernels add or rename keys and can change the report path." | copy sha256 recomputed = freeze ledger; host 7.2.11 inside the v7.2 line shows the same 72 keys in the same order; **no kernel later than 7.2 was observed**, so the "later kernels add or rename keys" half is UNVERIFIED here | consistent; untested beyond 7.2 |
| 68–69 | "cgroup v2 only. On a v1 hierarchy the same function prints `memory+swap` and `kmem` lines and a real per-page failcnt …" | `mem_cgroup_print_oom_meminfo()` (1791) prints, in the `CONFIG_MEMCG_V1` else-branch (1813–1821), `memory+swap: usage …` and `kmem: usage …`, with `memsw.failcnt` / `kmem.failcnt`; on v2 the failcnt comes from `memory_events[MEMCG_MAX]` (1800–1803). Host is unified v2 only, so v1 was not exercised | consistent with code; v1 path UNVERIFIED on this host |
| 70–72 | rate-limited summary vs unguarded victim line | `oom_kill.c.v7.2:1030` is the `if (__ratelimit(&oom_rs)) {` guard; this seat did not trace the victim line's position (other seats own that claim) | not re-checked here; anchor exists |
| 73–74 | "static `SEQ_BUF_SIZE` buffer under `oom_lock`, and an overflow only prints a warning" | `static char buf[SEQ_BUF_SIZE];` with comment "Use static buffer, for the caller is holding oom_lock" (1793–1794), `lockdep_assert_held(&oom_lock)` (1798), `#define SEQ_BUF_SIZE SZ_4K` (127); overflow warning at 1757–1759; the printer passes that buffer to `memory_stat_format` and `seq_buf_do_printk(&s, KERN_INFO)` (1827–1829) | consistent with code |
| 75–76 | no host block read | this seat read no kernel log; only key names were read from the live cgroup file, no values | consistent, and upheld by this seat |
| 77 | located quote ≠ entailment | meta-limit, nothing to check | n/a |

The `swap: usage …` second line on v2 (1809–1814) and the `memory: usage …` first line (1805–1808) are visible in
the same function; the entry's unit/order claims about those lines are other seats' checks, not re-run here.

## 7. What this check does not establish

- No `memory.stat` **value** was read, reported or stored, so nothing here says whether a key is nonzero, whether
  the host has a memcg OOM, or what a kill block on this host printed.
- The host has every relevant gate compiled on, so the entry's "missing key is not a zero" rule is consistent with
  the host but not exercised by it; a gate-off host was not available.
- The host is 7.2.11, a stable update of the tag the entry cites. This supports the entry's key list for the v7.2
  line; it says nothing about 7.3+ or about kernel configurations other than this one.
- Only key names and order were compared. Semantics of each key (units, overlap, which counter sums which) are the
  entry's claim rows, checked by other seats.
- No kernel-log MESSAGE text was read (lane rule); nothing here is an event-time observation of a kill.

## Findings

1. **LOW** — `corpus/knowledge/oom-memcg-stat-r50.md:50-51` (Reading rules): the CONFIG-conditional key list names
   7 of the 21 gated keys v7.2 can withhold. Unnamed: `zswap_incomp`, `swpin_zero`, `swpout_zero`, `zswpin`,
   `zswpout`, `zswpwb`, `thp_fault_alloc`, `thp_collapse_alloc`, `thp_swpout`, `thp_swpout_fallback`,
   `pgpromote_success`, `numa_pages_migrated`, `numa_pte_updates`, `numa_hint_faults`; gates `CONFIG_SWAP` and
   `CONFIG_NUMA_BALANCING` are not named. The sentence is not false and this host contradicts nothing in it (all
   seven named keys are present live); the gap is that the rule's enumeration is not the full gated set
   (anchors: `memcontrol.c.v7.2` 1557, 1565, 1568, 1580, 1606, 566, 570, 575, 581). Suggested correction for the
   L1: say the key set is compile-time conditional and name the gate families, or drop the enumeration and keep
   only "a missing key is not a zero".
2. **LOW** — `corpus/knowledge/oom-memcg-stat-r50.md:51` (Reading rules): `hugetlb` is attributed to "their CONFIG
   options" only, but v7.2 also skips it when the cgroup-v2 root's hugetlb accounting flag is off
   (`memcontrol.c.v7.2` 1713–1716 with `memcg_accounts_hugetlb()` at 1682–1690 reading
   `CGRP_ROOT_MEMORY_HUGETLB_ACCOUNTING`). The host's `hugetlb` key is present, so the flag is on here; the
   enabling path is not in the three frozen copies (only a comment at 5397), so it stays UNVERIFIED from these
   sources.
3. **No other discrepancy found.** Live key set and v7.2 printable key set are identical (72 keys) and in identical
   order; the `kernel`-aggregate keys and the aggregate `slab`, `pgscan`, `pgsteal` lines appear where the code
   places them; the entry's Limits bullets checked above (copy sha256, static buffer under `oom_lock`, overflow
   warning, v1 branch, no-host-block rule) are consistent with the frozen code and with this host.

## Evidence files (all inside this report; scratch removed)

- `uname -r` → `7.2.11-arch1-1`; `/proc/version` build string (section 1).
- 72-line key-only extract of `/sys/fs/cgroup/user.slice/user-1000.slice/memory.stat` (section 2).
- Extract script and its output (section 3); sha256 of `memcontrol.c.v7.2` =
  `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e`, equal to freeze line 2.
- `disk-guard.sh status` rc=0 (23% used, 618.7G free).
