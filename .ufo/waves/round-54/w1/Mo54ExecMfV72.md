# Mo54ExecMfV72 — the C2 memory-failure entry against the host's own 7.2 bytes

Seat: executor (v7.2 re-read of the six C2 copies). Lane: mori-shokunin. Round 54, wave w1.
Data commit under test: `78295c764093ff1f6cee08d7246679900bde7265`. Entry: `corpus/knowledge/memory-failure-kills-r54.md`.
Host: `uname -r` → `7.2.11-arch1-1`.

Question put to this seat: do the 21 located rows of `evidence/c2-claims.txt` also occur at v7.2, which rows are
v7.3-only, and do the entry's `## On this host` and Boundaries sentences match the v7.2 bytes?

## Method and receipts

Scratch `/fast/scratch/hyaku/mori-r54/Mo54ExecMfV72/` (`TMPDIR` set there; removed at the end).
Disk guard before the run: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit 0,
`/fast/scratch/hyaku 26% 597.8G free`.

Fetches, `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=v7.2` (all HTTP 200),
and the same six paths from the stable tree `.../git/stable/linux.git/plain/<path>?h=v7.2.11` (all HTTP 200):

| path | v7.2 bytes | sha256 (v7.2) | v7.2.11 vs v7.2 |
|---|---|---|---|
| `mm/memory-failure.c` | 80516 | `e29c93b204d35a767231884f7d89ccd17c6246e38577082ecf21c0c28a3e499e` | identical |
| `Documentation/mm/hwpoison.rst` | 6026 | `8011bb158129776bbb38ed5808959bd14d17489527ed3987dbc3d21d27e3ecb7` | identical |
| `Documentation/ABI/stable/sysfs-devices-node` | 8149 | `d852f950e42d92b862792477a892e77973ddb6a345bdb1748d2e7c5020198665` | identical |
| `include/trace/events/memory-failure.h` | 2964 | `a395e62b36ace3d1295fd3e9e469fc525f67c7787f529a380633d6b800f051ea` | identical |
| `Documentation/admin-guide/sysctl/vm.rst` | 42424 | `bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce` | identical |
| `Documentation/filesystems/proc.rst` | 107560 | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` | identical |

`include/trace/events/memory-failure.h` **exists at v7.2** (2964 bytes) and is byte-identical to the v7.3 copy; the
fallback hypothesis in the seat brief is not needed: `include/ras/ras_event.h` at v7.2 (`408ddc2ac2a5f172…`, 11341
bytes) contains zero occurrences of `memory_failure` (`grep -n memory_failure ras_event.h.v7.2` → no output, rc 1).

Diff of each v7.2 file against its v7.3 copy under `corpus/evidence/`:

| copy | result |
|---|---|
| `sources-r54/memory-failure.c.v7.3` | differs, 125 `+`/`-` lines |
| `sources-r54/hwpoison.rst.v7.3` | `cmp` identical |
| `sources-r54/sysfs-devices-node.v7.3` | `cmp` identical |
| `sources-r54/memory-failure-trace.h.v7.3` | `cmp` identical |
| `sources-r53/vm.rst.v7.3` | differs, 85 `+`/`-` lines |
| `sources-r53/proc.rst.v7.3` | differs, 5 `+`/`-` lines (one typo fix `any page page`→`any page`, one new `ur` smaps flag) |

Semantic content of the `memory-failure.c` delta (v7.2 → v7.3): new `sysctl_panic_on_unrecoverable_mf` and its
sysctl-table entry (v7.3 :78, :163-171); new predicate `panic_on_unrecoverable_mf()` (v7.3 :1268-1275) and its
`panic("Memory failure: %#lx: unrecoverable page", pfn)` call (v7.3 :1294-1295); `me_kernel()` and the
`{reserved, reserved, MF_MSG_KERNEL, me_kernel}` state-table row and the `#define reserved` removed (present at
v7.2 :1199, :1205); new `is_kernel_owned_page()` (v7.3 :1356-1381) with `PageReserved|PageSlab|PageTable|
PageLargeKmalloc`, a new `-ENOTRECOVERABLE` return, and the `switch (res) { case -ENOTRECOVERABLE: …
action_result(pfn, MF_MSG_KERNEL, MF_IGNORED) }` arm (v7.3 :2488-2490). The rest of the delta is the rmap walker
rename (`anon_vma_interval_tree_foreach` → `anon_rmap_tree_foreach`, `vma_interval_tree_foreach` →
`mapping_rmap_tree_foreach`, `vma_address` → `vma_filebacked_address`) and `#include "page_alloc.h"`.
`PageLargeKmalloc` has **0** occurrences in v7.2 `memory-failure.c`, consistent with the kernel-owned class being new.

The `vm.rst` delta is exactly the new `panic_on_unrecoverable_memory_failure` section (v7.3 :926-1004) plus its
toctree line (:67) and the removal of a stale sentence about `mm/swap.c`. The v7.2 file documents
`memory_failure_early_kill` (:497) and `memory_failure_recovery` (:525) and nothing else of this class.

## Row-by-row: does the quote occur at v7.2?

Method: `check72.py` collapses whitespace in each quote (`\|` unescaped) and in each v7.2 copy and searches;
line is the first raw line whose collapsed prefix ends at the match. Claim-cell hashes were recomputed from the
claim cells and all 21 match the listed `h` (21/21 `match=True`).

| row | h | v7.2 copy : line | v7.3 copy : line | on host's 7.2? |
|---|---|---|---|---|
| 1 | fcf9f378a818 | memory-failure.c : 37 | : 37 | yes |
| 2 | ba07ddfe1488 | memory-failure.c : 280 | : 292 | yes |
| 3 | e874fc1a128e | memory-failure.c : 283 | : 295 | yes |
| 4 | 8426794e271e | memory-failure.c : 290 | : 302 | yes |
| 5 | 4fdea8d0253f | memory-failure.c : 458 | : 470 | yes |
| 6 | 4748dc4eb41e | memory-failure.c : 471 | : 483 | yes |
| 7 | 3233412a93be | memory-failure.c : 1286 | : 1291 | yes |
| 8 | f5e240db68c0 | memory-failure.c : 862 | : 872 | yes |
| 9 | 2eb3990f7a81 | memory-failure.c : 1289 | : 1297 | yes |
| 10 | c98ac2ffa163 | memory-failure.c : 1281 | : 1286 | yes |
| 11 | 5a235a277033 | absent | : 1271 | **no — v7.3-only** |
| 12 | e3f8e075e4b2 | hwpoison.rst : 64 | : 64 | yes (file identical) |
| 13 | 63f08aa3baf0 | hwpoison.rst : 70 | : 70 | yes (file identical) |
| 14 | e3b581d09d1d | hwpoison.rst : 59 | : 59 | yes (file identical) |
| 15 | 77be7d2e2179 | vm.rst : 516 | : 514 | yes |
| 16 | 734269273c22 | absent | : 936 | **no — v7.3-only** |
| 17 | 2401e4d865f0 | sysfs-devices-node : 196 | : 196 | yes (file identical) |
| 18 | c81900e6c688 | sysfs-devices-node : 203 | : 203 | yes (file identical) |
| 19 | 4f693eb5f736 | memory-failure.h : 4 | : 4 | yes (file identical) |
| 20 | 8248e6d24be8 | memory-failure.h : 93 | : 93 | yes (file identical) |
| 21 | 257f4acfda4e | proc.rst : 1268 | : 1269 | yes |

Result: **19 of 21 quotes occur verbatim (whitespace-collapsed) at v7.2, at the lines above; 2 are v7.3-only —
row 11 (`5a235a277033`, the panic predicate) and row 16 (`734269273c22`, the panic sysctl doc).** Both v7.3-only
rows are the `panic_on_unrecoverable_memory_failure` switch. `grep -l panic_on_unrecoverable *v7.2.11` over all six
stable-tree files → no hits, rc 1: no v7.2 equivalent of either sentence exists anywhere in the C2 surface.

Consequence for the claim (observation, not a counter change): three of the six copies are byte-identical across
7.2/7.3, and 19 rows are shared bytes, so the located-quote arm of C2 gives no freshness separation on this entry;
all of the entry's new-against-7.2 content rests on rows 11 and 16.

## The entry's `## On this host` and Boundaries, clause by clause

Live reads (read-only, 2026-10-27, this host):

```
uname -r                                        -> 7.2.11-arch1-1
/proc/sys/vm/memory_failure_recovery            -> 1
/proc/sys/vm/memory_failure_early_kill          -> 0
/proc/sys/vm/enable_soft_offline                -> 1
/proc/sys/vm/panic_on_unrecoverable_memory_failure -> No such file or directory
/sys/devices/system/node/node0/memory_failure/{total,ignored,failed,delayed,recovered} -> 0 0 0 0 0
grep '^HardwareCorrupted' /proc/meminfo         -> HardwareCorrupted:     0 kB
```

| entry sentence | verdict against v7.2 bytes / live host |
|---|---|
| "the kill and recovery lines … exist on 7.2" | holds at source: `Sending SIGBUS` v7.2 :280, `forcibly killing` :458, `Cannot send advisory` :471, `recovery action for` :1286 (rows 2, 5, 6, 7). Not observed live (no event on this host). |
| "the counters … exist on 7.2" | holds: `update_per_node_mf_stats` v7.2 :1281 (row 10); ABI doc identical at v7.2 (`nodeX/memory_failure/{total,ignored,failed,delayed,recovered}`, :192-224, five counters); live node0 exposes all five and reads 0. |
| "the two older sysctls exist on 7.2" | holds: `sysctl_memory_failure_early_kill` v7.2 :71/:134, `sysctl_memory_failure_recovery` :73/:143, both documented at v7.2 vm.rst :497/:525; live reads 0 and 1. |
| "the panic switch does not [exist on 7.2]" | holds: no `panic_on_unrecoverable` symbol or doc section in any of the six v7.2/v7.2.11 files; live sysctl path absent. |
| "five per-node counters" | holds: ABI doc lists exactly total, ignored, failed, delayed, recovered. |
| "No line of this class has been observed live; every row above is read from source" | consistent with this seat: nothing in the live reads shows an event, and the trace event dir could not be listed (`ls /sys/kernel/tracing/events/ras/` → `Permission denied`, rc 2) — live tracepoint availability is UNVERIFIED from an unprivileged shell. |

## Findings

1. **MED — row 20 (`8248e6d24be8`) overstates the trace/log string match.** The claim says the traced line
   "repeats the page type and outcome strings of the logged recovery line". The trace header keeps its *own* string
   table, and one page-type string differs: `MF_MSG_ALREADY_POISONED` is `"already poisoned"` in
   `corpus/evidence/sources-r54/memory-failure-trace.h.v7.3:49` but `"already poisoned page"` in
   `corpus/evidence/sources-r54/memory-failure.c.v7.3:897` (identical mismatch at v7.2
   `include/trace/events/memory-failure.h:49` vs `mm/memory-failure.c:887`). The four outcome words match exactly
   (Ignored/Failed/Delayed/Recovered), and the tables are independent copies rather than one shared table. A traced
   line can therefore not be matched to a logged line by page-type string for that one type; only the outcome word
   and pfn agree. Affected file: `corpus/knowledge/memory-failure-kills-r54.md`, row 20.
2. **MED — row 11 (`5a235a277033`) is narrower than the v7.3 code it quotes.** The claim says the switch fires
   "when a reserved kernel page is reported with the Ignored outcome". At v7.3 `MF_MSG_KERNEL` is raised only from the
   `-ENOTRECOVERABLE` arm (`memory-failure.c.v7.3:2489-2490`), whose class is `PageReserved | PageSlab | PageTable |
   PageLargeKmalloc` (`is_kernel_owned_page()`, :1356-1381), and the v7.3 doc the entry itself cites lists exactly those
   four classes (`sources-r53/vm.rst.v7.3:936-943`). `"reserved kernel page"` is only the *log string* for
   `MF_MSG_KERNEL` (:879) and was accurate at v7.2, where the state table keyed `PG_reserved` (:1205); it is not the
   v7.3 trigger class. The necessary half of the claim (`type == MF_MSG_KERNEL && result == MF_IGNORED`, off by
   default) is exact. Affected file: `corpus/knowledge/memory-failure-kills-r54.md`, row 11; a reword such as
   "a kernel-owned page (reserved, slab, page-table or large-kmalloc) reported Ignored" would remove the gap.
3. **LOW — Boundaries sentence attributes live reading to the kill lines.** "The kill and recovery lines, the
   counters and the two older sysctls exist on 7.2 as read live above" groups the lines with the counters/sysctls;
   the lines were verified here at v7.2 source (lines 280/458/471/1286), not observed live, and the entry's own
   `## On this host` says no line of this class has been observed. Splitting the sentence ("the counters and the two
   older sysctls read live above; the lines exist in the 7.2 source") removes the ambiguity.
   File: `corpus/knowledge/memory-failure-kills-r54.md`, `## Boundaries`, last bullet.
4. **LOW — 19 of 21 rows are shared 7.2/7.3 bytes.** Only rows 11 and 16 are new at v7.3; three of the six copies
   (`hwpoison.rst`, `sysfs-devices-node`, `memory-failure.h`) are byte-identical at both tags. This is a named limit
   for the round report (the located-quote arm cannot separate this entry's bytes by freshness), not a counter change:
   the counter and predicate stay as frozen.
5. **LOW — trace-event live surface unverified.** `/sys/kernel/tracing/events/ras/` is not listable from this
   unprivileged shell (`Permission denied`, rc 2), so "the `ras:memory_failure_event` tracepoint exists on this host"
   rests on the v7.2 header bytes (identical to v7.3) and the live `/proc`/sysfs reads, not on a live listing.

No change is proposed to `count-c2.py`, its predicate, the controls or the kill rules. No lane file other than this
report was written; `corpus/`, `tools/`, `SKILL.md`, `PROVINCE.md` and the wave directory were not touched. Scratch
`/fast/scratch/hyaku/mori-r54/Mo54ExecMfV72/` was removed after the run. No tool was installed or upgraded in this
seat (curl, python3, diff, cmp, sha256sum were already present).
