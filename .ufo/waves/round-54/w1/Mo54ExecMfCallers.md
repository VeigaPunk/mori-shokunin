# Mo54ExecMfCallers — `mm/memory-failure.c` v7.3: rows 1–11 and the kill-caller graph

Report: `.ufo/waves/round-54/w1/Mo54ExecMfCallers.md` (this file). Lane: mori-shokunin, round 54, wave w1.
Seat kind: non-voting executor. Nothing below is a vote and this file must never be read as one: the C1 counter
reads start-of-line `RECHECK`/`QUOTE` lines only in `Mo54Rc01.md`…`Mo54Rc12.md`, the C2 counter reads
`ENTAIL`/`REPLACE` lines only in `Mo54En01.md`…`Mo54En12.md`, and no line of this file begins with any of those
four tokens. Findings are facts for the voters and for the L1's data-correction decision.

Scope: the C2 rows whose source is S521, i.e. rows 1–11 of `.ufo/waves/round-54/evidence/c2-claims.txt`, read
against `corpus/evidence/sources-r54/memory-failure.c.v7.3` (3029 lines, sha256
`94d24a605b61f94ad1d10ab3db26aed12cb6113af15431ff873da5b98ca48003` — matches the short hash the entry cites),
plus the five questions in the seat dispatch: callers of `kill_proc`/`kill_procs` and their forcekill
conditions, the `tk->addr == -EFAULT` condition, where `MF_ACTION_REQUIRED` is set, which paths reach
`action_result` with `MF_MSG_KERNEL`/`MF_IGNORED`, whether `update_per_node_mf_stats` has another caller, and
whether every `pr_*` in the file goes through `pr_fmt` or something bypasses it.

## Method and receipts

All reads are absolute paths into the lane's committed copies; all writes are the scratch dir and this file.

| step | command (abridged) | result |
|---|---|---|
| copy identity | `sha256sum corpus/evidence/sources-r54/memory-failure.c.v7.3` | `94d24a605b61…a48003`, exit 0; `wc -l` → 3029 |
| row → line map | `grep -n` for each row's quoted text | rows 1–11 at lines 37, 292, 295, 302, 470, 483, 1291, 872, 1297, 1286, 1271 (exit 0) |
| log calls | `grep -o "pr_[a-z_]*(" \| sort \| uniq -c` | `12 pr_err(`, `26 pr_info(`, `1 pr_info_once(`, `3 pr_fmt(` (definition + two rebinds), exit 0 |
| non-pr logging | `grep -n "printk(\|dev_err(\|dev_warn(\|dev_info(\|dev_dbg(\|dev_crit(\|dev_notice("` | no match, exit 1 |
| KSM collector | cgit `plain/mm/ksm.c?h=v7.3` → scratch | 4060 lines; `collect_procs_ksm` at 3268–3300, `add_to_kill_ksm` call 3296, `addr = rmap_item->address & PAGE_MASK` 3286 |
| MCE caller | cgit `plain/arch/x86/kernel/cpu/mce/core.c?h=v7.3` → scratch | 2937 lines; `kill_me_maybe` 1416–1449, `memory_failure` calls 623, 1430, 1459 |
| v7.2 cross-check | cgit `plain/mm/memory-failure.c?h=v7.2` → scratch | 2960 lines; same filter at 417, same `forcekill` at 1622, same SIGKILL branch at 457–462 |
| helpers header | cgit `plain/include/linux/memory-failure.h?h=v7.3` → scratch | 28 lines, only `pfn_address_space` + registration prototypes (no flags, no `mf_result`) |

Scratch `/fast/scratch/hyaku/mori-r54/Mo54ExecMfCallers/` (with `tmp/`), removed at the end of this seat; the
fetched files lived there only and are not cited as evidence — every citation below is either the lane's own
copy or a line number in a fetch that the report quotes in place. No tool was installed or upgraded (nothing was
needed; pacman untouched). No host write, no sysctl read or write, no kernel line counted by message text. Fetch
channel: `git.kernel.org` cgit `plain` at a tag; four files, ~250 KB total, one per question.

## 1. Caller graph: `kill_proc` (286) and `kill_procs` (462)

`kill_proc` sends the SIGBUS (`force_sig_mceerr(BUS_MCEERR_AR, …)` at 296–297, or `send_sig_mceerr(BUS_MCEERR_AO, …)`
at 305–306) and `kill_procs` is the loop plus the SIGKILL branch.

| callee | call site | arguments / gating |
|---|---|---|
| `kill_proc` | 482, inside `kill_procs` | `else if (kill_proc(tk, pfn, flags) < 0)` — reached only when `forcekill` is true **and** `tk->addr != -EFAULT` |
| `kill_proc` | 843, inside `kill_accessing_process` | `if (ret == 1 && priv.tk.addr)` after `walk_page_range` over `p->mm` for the poisoned pfn; `p` is always `current` (callers 2104, 2442) |
| `kill_procs` | 1680, inside `hwpoison_user_mappings` | `forcekill` computed at 1678–1679: `folio_test_dirty(folio) || (flags & MF_MUST_KILL) || !unmap_success` |
| `kill_procs` | 1750, inside `unmap_and_kill` | `forcekill = !!(flags & MF_MUST_KILL)`; `unmap_and_kill` is called from `mf_generic_kill_procs` 1817 and `mf_dax_kill_procs` 1857, both of which set `flags |= MF_ACTION_REQUIRED \| MF_MUST_KILL` (1811, 1837) → **always** forcekill there |
| `kill_procs` | 2222, inside `kill_procs_now` | literal `true`; `kill_procs_now` has exactly one caller, 2540 (large folio whose split failed or left `new_order != 0`) |
| `kill_procs` | 2356, inside `memory_failure_pfn` | literal `true`, after `flags \|= MF_ACTION_REQUIRED \| MF_MUST_KILL` (2354) |

`kill_procs_now` callers: only 2540 (`grep -n "kill_procs_now"` → 2213 definition, 2540 call, exit 0).
`kill_accessing_process` callers: only 2104 (`try_memory_failure_hugetlb`, folio/page already poisoned, guarded
by `flags & MF_ACTION_REQUIRED`) and 2442 (`memory_failure`, `TestSetPageHWPoison` true, same guard).

Consequence of 466–468: with `forcekill == false` the collected list is freed with **no signal at all** — the
comment at 466–467 states it ("Only do anything when FORCEKILL is set, otherwise just free the list (this is used
for clean pages which do not need killing)"). `forcekill == false` is reachable only through
`hwpoison_user_mappings` (clean folio, no `MF_MUST_KILL`, unmap succeeded).

Also structurally relevant: `forcekill` does not change *which* signal `kill_proc` sends. `kill_proc` picks
`BUS_MCEERR_AR` solely from `(flags & MF_ACTION_REQUIRED) && (t == current)` (295); every other entry, forcekill
or not, takes `send_sig_mceerr(BUS_MCEERR_AO, …)` (305–306).

## 2. When is `tk->addr == -EFAULT`

The value is produced by the collect functions and consumed only in `__add_to_kill`'s diagnostic branch
(412–415) and in `kill_procs`' SIGKILL branch (469–473). The file's own comment at 403–408 states the intent
("Send SIGKILL if `tk->addr == -EFAULT`") inside a block about ZONE_DEVICE mappings.

| producer | line | can it hand `-EFAULT` to `__add_to_kill`? |
|---|---|---|
| `add_to_kill_anon_file` (anon pages, `page_mapped_in_vma`, 572) | 425–431 | **no** — `if (addr == -EFAULT) return;` at 429 |
| `add_to_kill_anon_file` (file pages, `page_address_in_vma`, 611) | 425–431 | **no** — same filter at 429 |
| `add_to_kill_ksm` (KSM pages) | 448–453 | **no** — its only producer is `mm/ksm.c:3296` with `addr = rmap_item->address & PAGE_MASK` (ksm.c:3286), never `-EFAULT` |
| `add_to_kill_fsdax` (fsdax pages) | 618–625 | **yes** — `vma_filebacked_address(vma, pgoff, 1)` result is passed unfiltered |
| `add_to_kill_pgoff` (pfn-space pages) | 2254–2277 | **yes** — `tk->addr = vma_filebacked_address(vma, pgoff, 1)` (2270), logs `Unable to find address %lx in %s` (2271–2273), and still appends the entry (2276) |
| `hwpoison_pte_range` → `set_to_kill` (kill_accessing_process path) | 684–687, 740–780 | **no** — addresses come from walked PTEs, and 842 additionally requires `priv.tk.addr` non-zero |

The other `-EFAULT` in the file is a *return* value, not a `tk->addr`: `kill_accessing_process` returns
`-EFAULT` when `p->mm` is NULL (830–831), and 2079 documents it.

Therefore the SIGKILL branch (469–473) is reachable only from the device paths — `mf_generic_kill_procs`/
`mf_dax_kill_procs` (fsdax entries, 1817/1857 → 1750) and `memory_failure_pfn` (PFN entries, 2356) — not from a
System-RAM anon/file page whose unmap failed. `unmap_poisoned_folio` failing does not rewrite any `tk->addr`; the
collection happened before the unmap call (1654 before 1656), and its entries were already filtered of `-EFAULT`.
The v7.2 copy has the identical structure (filter 417, `forcekill` 1622, SIGKILL branch 457–462), so this is not a
v7.3 change.

## 3. Where `MF_ACTION_REQUIRED` is set

In-file (all three set it for device memory, never for System RAM):

- 1811 `mf_generic_kill_procs` — ZONE_DEVICE/`dev_pagemap` fallback (`flags |= MF_ACTION_REQUIRED | MF_MUST_KILL`);
- 1837 `mf_dax_kill_procs` — fsdax range (`mf_flags |= …`), exported;
- 2354 `memory_failure_pfn` — pages not backed by `struct page`.

Consumed at 295 (`kill_proc` AR branch), 1654 and 2219 (`collect_procs(…, flags & MF_ACTION_REQUIRED)` → the
`force_early` argument), 2103 and 2441 (`kill_accessing_process`).

From callers (outside the copy; x86 MCE path fetched): `kill_me_maybe` (mce-core.c:1416) sets
`int flags = MF_ACTION_REQUIRED;` (1419), adds `MF_MUST_KILL` when `!p->mce_ripv` (1426–1427), and calls
`memory_failure(pfn, flags)` (1430) from the task_work of an uncorrected error hit during user access. Paths that
pass `0` therefore produce action-optional handling only: `uc_decode_notifier` (mce-core.c:623, AO/deferred
severity) and `kill_me_never` (1459, "kernel accessed poison in user space").

The in-file comment at 278–282 defines the pair: “action optional” if the processes are not immediately affected,
“action required” if the error happened in current execution context. `kill_proc`'s AR branch additionally
requires `t == current`, and `t` is what `task_early_kill(tsk, force_early)` returned (528–539): with
`force_early` set, that is `current` for `current->mm`, otherwise only a thread with `PF_MCE_EARLY` (or any thread
when `sysctl_memory_failure_early_kill` is 1, 509).

## 4. Paths that reach `action_result` with `MF_MSG_KERNEL` + `MF_IGNORED`

`MF_MSG_KERNEL` occurs exactly three times in the copy: 879 (its display string `"reserved kernel page"`), 1274
(the panic predicate) and **2490 — the only `action_result` call site with that type**.

2490 is reached only from `memory_failure()`: `get_hwpoison_page(p, flags)` (2460) returns `-ENOTRECOVERABLE`,
which `get_any_page` produces only at 1434–1439 when `is_kernel_owned_page(p)` is true. `is_kernel_owned_page`
(1355–1377) returns true for `PageReserved` (1361) **and** for `PageSlab(head) || PageTable(head) ||
PageLargeKmalloc(head)` (1375–1376) — i.e. the class is broader than the display string "reserved kernel page".
`MF_MSG_KERNEL_HIGH_ORDER` + `MF_IGNORED` (2478) is a different row and does not panic.

The other `MF_IGNORED` sites are 2099 (`MF_MSG_GET_HWPOISON`, hugetlb retry exhausted), 2345 (`MF_MSG_PFN_MAP`,
no address space), 2494 (`MF_MSG_GET_HWPOISON`, transient lifecycle race) and 2605 (`MF_MSG_TRUNCATED_LRU`);
none of them can fire the panic switch, because the predicate (1268–1275) tests the type.

The switch itself: `sysctl_panic_on_unrecoverable_mf` declared at 78 with no initializer (default 0), exposed as
`panic_on_unrecoverable_memory_failure` in the `vm` table (162–169, mode 0644, `proc_dointvec_minmax` clamped to
0..1). The panic argument is `"Memory failure: %#lx: unrecoverable page"` (1295), and `panic()` output appears on
the console behind `Kernel panic - not syncing: `, not as a line that *starts* with `Memory failure:`.

Soft offline and unpoison never call `action_result` (no call site after 2605; the two later sections start at
2716 and 2841).

## 5. Does `update_per_node_mf_stats` have another caller?

No. `grep -n "update_per_node_mf_stats"` → 1235 (definition) and 1288 (inside `action_result`), exit 0.
Reachability follows `action_result`: every call except the two excluded page types (1286). The counter is bumped
*before* the `pr_err` at 1291, so on a live host the sysfs counter is at least as large as the number of matching
recovery lines. `->total` is incremented unconditionally at 1265, including for `MF_IGNORED` (so a panic-inducing
ignore is counted first).

## 6. `pr_fmt` coverage and what bypasses it

- 37 defines `#define pr_fmt(fmt) "Memory failure: " fmt`, before every include and every `pr_*` — all 39 `pr_*`
  uses expand it. There is **no** `printk(` and **no** `dev_err(`/`dev_warn(`/`dev_info(`/`dev_dbg(`/`dev_crit(`/
  `dev_notice(` anywhere in the copy (grep exit 1). The only `dev_`-prefixed identifiers are functions:
  `dev_pagemap_mapping_shift` (337, 398), `put_dev_pagemap` (2200), `get_dev_pagemap` (2418).
- `pr_fmt` is *rebound twice* in the same file: `#undef pr_fmt` at 2716 then `"Unpoison: "` at 2717, and again at
  2841–2842 for `"Soft offline: "`. Counted by position: 23 `pr_*` uses before 2716 (all `Memory failure: `), 19
  after (two other prefixes; the `unpoison_pr_info` macro at 2717–2722 wraps `pr_info` and rate-limits it, and
  2986 is a `pr_info_once` under the soft-offline prefix).
- Not routed through `pr_fmt`, though the text carries the prefix by hand: `WARN_ONCE(1, "Memory failure: …")` at
  1243 and 1262, and the panic string at 1295. `panic("Memory failure on page %lx", pfn)` at 2396 has **no colon**
  and prints as `Kernel panic - not syncing: Memory failure on page 0x…`; `WARN_ON` at 2111, 2566, 2974 carry no
  message text.

## 7. Row-by-row facts for rows 1–11

Line numbers are the line on which the row's quoted text begins in the v7.3 copy. "Entailment note" is what the
code adds or withholds; it is a fact for the voters, not a vote.

| row | h | line | code facts | entailment note |
|---|---|---|---|---|
| 1 | fcf9f378a818 | 37 | `pr_fmt` covers every `pr_*` in the memory-failure section (23 uses before 2716); no `printk`, no `dev_*` print macro | "Every message the memory-failure handler prints" is true only for the `pr_*` lines of the section that ends at 2716. The same file prints 19 further `pr_*` lines under `Unpoison: ` (2717) and `Soft offline: ` (2842), and two `panic()` strings (1295, 2396) are emitted behind `Kernel panic - not syncing: `, one of them without the colon. The clause "which names the kernel component that wrote the line" is interpretation, not text |
| 2 | ba07ddfe1488 | 292 | `pr_err` executes at the top of `kill_proc`, before the `force_sig_mceerr`/`send_sig_mceerr` call (295–306); fields are `pfn`, `t->comm`, `task_pid_nr(t)` | the line is emitted per collected task, i.e. once per signal *attempt*, and it precedes delivery. `t` is the thread `task_early_kill` returned (528–539) and `task_pid_nr(t)` is that thread's pid, not `tgid` — a parser that joins this to a process by pid must not assume a thread-group leader |
| 3 | e874fc1a128e | 295 | `if ((flags & MF_ACTION_REQUIRED) && (t == current)) ret = force_sig_mceerr(BUS_MCEERR_AR, …)`; `force_sig_mceerr` has this single call site | the condition is a conjunction: AR flag **and** the collected task is `current`. In-file, AR is set only on the three device paths (1811, 1837, 2354); for System RAM it arrives from the caller (x86 `kill_me_maybe`, mce-core.c:1419/1430). Without the flag the same task takes the AO branch |
| 4 | 8426794e271e | 302 | else-branch 298–306 with the comment 299–304; `send_sig_mceerr(BUS_MCEERR_AO, …)` | true of the *signal form*, but not of "other processes sharing the page": `collect_procs` (664–676) collects only `current` (when AR/`force_early`) and threads with `PF_MCE_EARLY`, or every thread when `sysctl_memory_failure_early_kill == 1` (509, 528–539). A process that maps the page without early kill is not signalled at this point; it dies later on fault (late kill). Also, `forcekill` never upgrades AO to AR (295, 305) |
| 5 | 4fdea8d0253f | 470 | SIGKILL branch 469–473 `if (tk->addr == -EFAULT)`; `unmap_success` only feeds `forcekill` at 1678–1679; separate `pr_err("%#lx: failed to unmap page (folio mapcount=%d)")` at 1658–1659; anon/file collectors drop `-EFAULT` at 429 | the trigger is an unresolvable user address in a *device* collect path (fsdax 624, pfn 2270), not "unmapping failed". A System-RAM page whose unmap failed sets `forcekill` and then still goes through `kill_proc`: forced `BUS_MCEERR_AR` if it is `current` with the AR flag, `BUS_MCEERR_AO` otherwise. The message text says "because of failure to unmap corrupted page", which is what the row paraphrases — the code does not implement that causality (see Findings, HIGH) |
| 6 | 4748dc4eb41e | 483 | the `pr_err` is inside the forcekill branch at 482–484; independently, `kill_proc` logs `pr_info("Error sending signal to %s:%d: %d")` on any negative return (307–309); the SIGKILL send at 472–473 ignores `do_send_sig_info`'s return | a failed SIGBUS delivery always gets the `pr_info` line; the quoted `pr_err` is emitted only when the failure happens in the forcekill branch (and then both appear). A failed SIGKILL delivery gets no line at all, so "a sending line alone does not prove delivery" holds, but the converse "a failure line exists" does not hold for SIGKILL |
| 7 | 3233412a93be | 1291 | `action_result` is the only producer of the recovery line, `pr_err` at 1291–1292; 17 call sites, 16 direct plus one from `page_action` (1313) | not every handled page produces one: `hwpoison_filter`'ed pages return `-EOPNOTSUPP` with no `action_result` (2502–2508, and the hugetlb twin 2118–2126), and `arch_memory_failure` handled pages return early with none (2405–2407). For a dax range, one `MF_MSG_DAX` line covers the whole range (2202 after `mf_dax_kill_procs`, 1857), not one per page |
| 8 | f5e240db68c0 | 872 | `action_name[]` at 871–874 with exactly four designated initializers; `action_result` indexes it at 1292 without a bounds check | the four display words are exactly those; "%s" of a value outside 0..3 would index past the array (no guard), and `update_per_node_mf_stats` has its own `WARN_ONCE` default (1261–1263). `enum mf_result` itself is declared outside this copy — its member count is UNVERIFIED here, the four entries are |
| 9 | 2eb3990f7a81 | 1297 | `return (result == MF_RECOVERED \|\| result == MF_DELAYED) ? 0 : -EBUSY;` | "error" is specifically `-EBUSY` for both `Ignored` and `Failed`; callers see that value (e.g. `memory_failure` returns it, and x86 `kill_me_maybe` treats anything but 0/`-EHWPOISON`/`-EOPNOTSUPP` as "Memory error not recovered", mce-core.c:1444–1448) |
| 10 | c98ac2ffa163 | 1286 | guard 1286–1289 wraps both `num_poisoned_pages_inc` (1287) and `update_per_node_mf_stats` (1288) | true, and stronger than the row says: the same guard also skips the global `num_poisoned_pages` increment and `mf_stats->total`; and a *successful* pfn-space kill (`MF_MSG_PFN_MAP`, `MF_RECOVERED` at 2358) is therefore counted in no per-node counter at all |
| 11 | 5a235a277033 | 1271 | predicate 1268–1275; single `MF_MSG_KERNEL` call site 2490; default 0 at 78; table 162–169 | true as text. Two qualifications: the class behind the label "reserved kernel page" is `PG_reserved` **plus** slab, page-table and large-kmalloc pages (1375–1376), and the emission is a `panic()` whose console line starts with `Kernel panic - not syncing: ` (1295) |

## Findings

- **HIGH** — row 5 (`4fdea8d0253f`, line 470) and the entry's causal sentence at
  `corpus/knowledge/memory-failure-kills-r54.md:15` ("**SIGKILL** when the unmap failed") state a causality the
  code does not implement. SIGKILL is sent only for entries whose `tk->addr == -EFAULT` (469–473), and the anon and
  file collectors discard `-EFAULT` before the entry is built (429); `-EFAULT` can only reach an entry through
  `add_to_kill_fsdax` (624) or `add_to_kill_pgoff` (2270) — device memory, not a System-RAM unmap failure.
  A failed unmap sets `forcekill` (1678–1679) but the entries keep resolved addresses, take `kill_proc` (482) and
  receive a *forced* `BUS_MCEERR_AR` when they are `current` with the AR flag, or `BUS_MCEERR_AO` otherwise
  (295–306); the failed unmap has its own line, `failed to unmap page (folio mapcount=%d)` (1658). The v7.2 copy is
  structurally identical (417, 457–462, 1622), so this is a long-standing misreading, not a v7.3 change. Effect on
  the entry: the decision-table mapping "forcibly killing → SIGKILL" is right, the trigger sentence, the prose and
  the row's "instead of SIGBUS" clause are wrong for system RAM.
- **MED** — row 4 (`8426794e271e`, line 302): "Other processes sharing the page are signalled through the ordinary
  path" overstates collection. Only early-kill threads (`PF_MCE_EARLY`, or every thread when
  `sysctl_memory_failure_early_kill == 1`) and, under AR, `current` are collected (528–539, 562, 595, 648, 664–676);
  all other sharers are not signalled at this moment and die on their next fault. The "not forced / can be blocked"
  half of the row is accurate (299–306).
- **MED** — row 7 (`3233412a93be`, line 1291) and the entry's decision-table row for the recovery line
  ("one handled page and its outcome", entry line 57): filtered pages (2502–2508, 2118–2126) and arch-handled pages
  (2405–2407) end with no `recovery action` line, and a dax range produces a single `MF_MSG_DAX` line for many
  pages (1857 → 2202). "Each handled page" is false in both directions.
- **MED** — the entry's kill-class table (`memory-failure-kills-r54.md:55–56`) has no row for the arch-side kill:
  x86 MCE `kill_me_maybe` sends its own `force_sig(SIGBUS)` (mce-core.c:1408–1414, 1447–1448) when
  `memory_failure()` returns anything other than 0, `-EHWPOISON` or `-EOPNOTSUPP`, and logs
  `Memory error not recovered` under no `Memory failure:` prefix. On the `MF_MSG_KERNEL`/`MF_IGNORED` path
  `action_result` returns `-EBUSY` (1297), so with the new sysctl at 0 the user task still gets a bare SIGBUS from
  arch code — a death with a line, but not one of the two kill lines the table maps.
- **LOW** — row 1 (`fcf9f378a818`, line 37): the claim is scoped correctly only if "the memory-failure handler"
  excludes this file's other two sections. An operator grepping the console sees three prefixes from this one file
  (`Memory failure: ` 23 uses, `Unpoison: `, `Soft offline: `) plus `Kernel panic - not syncing:` wrappers, and one
  panic string without the colon (2396).
- **LOW** — row 2 (`ba07ddfe1488`, line 292): the logged `%d` is `task_pid_nr(t)` of the collected thread, not the
  thread-group id; the line is printed before delivery, so it is an attempt marker, not a delivery record (see row 6).
- **LOW** — row 6 (`4748dc4eb41e`, line 483): the quoted `pr_err` exists only in the forcekill branch (482–484);
  the universal delivery-failure line is the `pr_info` at 307–309, and the SIGKILL send at 472–473 has no failure
  check at all.
- **LOW** — row 10 (`c98ac2ffa163`, line 1286): the guard also drops `num_poisoned_pages_inc` and `mf_stats->total`,
  and the successful `MF_MSG_PFN_MAP`/`Recovered` outcome (2358) is invisible in the per-node counters — a
  detection gap for device-memory kills, not a defect in the row.
- **LOW** — row 11 (`5a235a277033`, line 1271): "reserved kernel page" is the display string only; the gating class
  is `is_kernel_owned_page` (PG_reserved, slab, page table, large kmalloc; 1361, 1375–1376), and the emitted line
  is a `panic()` (1295) whose console line does not begin with `Memory failure:`.

## Limits of this seat

- No live event exists on this host for this class (the sibling host-read seat covers the read-only surfaces); every
  statement above is read from source. Nothing here was observed firing.
- `enum mf_result` and the `MF_*` flag values are declared outside the fetched bytes; the four `action_name`
  entries and the in-file comment at 278–282 are the basis for the flag and outcome statements, everything else is
  marked UNVERIFIED where it matters (row 8).
- Whether `vma_filebacked_address` returns `-EFAULT` for an unbacked pgoff is not in the copy (it is a helper
  declared elsewhere); what is verified is that the fsdax and pfn collectors pass its result unfiltered while the
  anon/file collector filters `-EFAULT` (429). That asymmetry is what the HIGH finding rests on, and it holds
  identically at v7.2 (417).
- External `memory_failure()` callers were enumerated only for the x86 MCE path (`arch/x86/kernel/cpu/mce/core.c`
  v7.3: 623, 1430, 1459). GHES/APEI, `memory_failure_queue` producers and the EDAC notifiers were not fetched, so
  the claim "MF_ACTION_REQUIRED arrives from the caller" is verified for x86 MCE only.
- The v7.2 check is a structural spot-check of the three constructs this seat depends on (filter, `forcekill`,
  SIGKILL branch), not the byte-level comparison the `Mo54ExecMfV72` seat owns.
