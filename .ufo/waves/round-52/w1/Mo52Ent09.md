# Mo52Ent09 — ENTAILMENT votes, C2 claim rows 15–21

Seat: Mo52Ent09 (ENTAILMENT). Entry: `corpus/knowledge/overcommit-commit-limit-r52.md` at
`8524904adb25e44f24d9f25aac7eae909625c18c`. Assigned rows: 15–21 of the `## Claims` table (all cite S499,
`mm/util.c` at v7.2; committed copy `corpus/evidence/sources-r52/util.c.v7.2`).

## Method (per row)

1. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8524904adb25e44f24d9f25aac7eae909625c18c:corpus/knowledge/overcommit-commit-limit-r52.md` (exit 0) — extracted the claims table, source rows, quotes.
2. Located each quote in the committed source copy with line numbers (grep, then `read` ranges).
3. Read ~20 lines around each quote.
4. Recomputed the claim hashes with `python3 -c 'import hashlib,re,sys;print(hashlib.sha256(re.sub(r"\s+"," ",sys.argv[1]).strip().encode()).hexdigest()[:12])' "<claim text>"`; all seven match `./ufo/waves/round-52/evidence/c2-hashes-at-data.txt` (row=15  a75ce7619818, row=16 309f4487d8b6, row=17 cddcf1bc062f, row=18 967021950067, row=19 41934e8b2887, row=20 ca2418460394, row=21 9cb0e908f997). exit 0.

Source line map (committed copy `util.c.v7.2`, sha256 e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c per the entry's recheck):
- `vm_commit_limit()` 904–916; kbytes arm 908–909; ratio arm 911–912; swap add 913.
- Knob declarations 781–786 (`sysctl_overcommit_memory … = OVERCOMMIT_GUESS;` 781; `sysctl_overcommit_ratio __read_mostly = 50;` 782; kbytes 783).
- `__vm_enough_memory()` 959–1003: charge `vm_acct_memory(pages)` 964; ALWAYS return 969–970; GUESS branch 972–976; `allowed = vm_commit_limit()` 978; admin reserve 982–983; user reserve 988–992; never-overcommit compare 994–995; error path 996–1002 (`pr_warn_ratelimited` 998–999; `vm_unacct_memory(pages)` 1000).
- `vm_committed_as` is a per-CPU counter (`struct percpu_counter` 922; comment 918–921; sync on policy switch 801–804, 814–822; full sum `vm_memory_committed()` 937–940 with cost comment 932–935).

## Verdicts

### Row 15 — hash a75ce7619818
Claim: "When the kbytes knob is nonzero it replaces the ratio term entirely, after conversion from kilobytes to pages."
Quote located: `util.c.v7.2:908-909` (`if (sysctl_overcommit_kbytes)` / `allowed = sysctl_overcommit_kbytes >> (PAGE_SHIFT - 10);`). Context read: 895–916.
The branch structure is exactly as claimed: if kbytes is nonzero the `else` ratio arm (911–912) is never reached, so the kbytes value entirely replaces the ratio term; `>> (PAGE_SHIFT - 10)` is the kilobytes-to-pages conversion (1 KB × 2^10 / 2^PAGE_SHIFT). Entailed.
Careless over-read risk: a reader could read "replaces the ratio term entirely" as keeping the hugetlb subtraction of the ratio arm (the kbytes arm does not subtract hugetlb pages), or invert the shift direction (pages-to-KB).

ENTAIL a75ce7619818 entailed

### Row 16 — hash 309f4487d8b6
Claim: "In the default heuristic mode a request fails only when its own size exceeds all RAM plus all swap together."
Quote located: `util.c.v7.2:972-976` (GUESS branch: `if (pages > totalram_pages() + total_swap_pages) goto error; return 0;`). Context read: 775–810, 959–1003.
Line 781 makes GUESS (heuristic) the compiled-in default (`__read_mostly = OVERCOMMIT_GUESS`). Within the branch, the only refusal condition is `pages > totalram_pages() + total_swap_pages`; otherwise `return 0`. So "fails only when its own size exceeds all RAM plus all swap" is exactly the code. Entailed.
Careless over-read risk: a reader could assume the failure check involves current usage or the committed counter (it compares only this single request's size against the totals), or that mode 0 is the only heuristic mode at runtime on a host (the claim is about the compiled-in default).

ENTAIL 309f4487d8b6 entailed

### Row 17 — hash cddcf1bc062f
Claim: "Every request is charged to the committed counter before the mode is examined, so the counter grows under modes 0 and 1 too."
Quote located: `util.c.v7.2:964-970` (`vm_acct_memory(pages);` then the `OVERCOMMIT_ALWAYS` check). Context read: 959–1003.
`vm_acct_memory(pages)` executes at 964, before the mode comparisons at 969 and 972, unconditionally. Per S500 (mman.h), `vm_acct_memory` is `percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch)` — it charges the committed counter. Since the charge precedes mode examination, accepted requests grow the counter under mode 0 (GUESS) and mode 1 (ALWAYS) too; refused requests in GUESS mode are subsequently uncharged (1000). Entailed.
Careless over-read risk: a reader could read "Every request is charged" as "every request permanently increases the counter" (refused requests are uncharged at 1000), or read "before the mode is examined" as the charge influencing the mode decision (it does not).

ENTAIL cddcf1bc062f entailed

### Row 18 — hash 967021950067
Claim: "The never-overcommit test compares a fast approximate read of the per-CPU committed counter with the computed limit."
Quote located: `util.c.v7.2:994` (`if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;`). Context read: 895–1003.
The test runs in the mode-2 (NEVER) path: `allowed = vm_commit_limit()` at 978 (the computed limit, after admin/user reserve reductions at 982–992), compared against `percpu_counter_read_positive(&vm_committed_as)` — a read of the per-CPU counter `vm_committed_as` (922). "Approximate": the counter can deviate from its true sum — comment 814–822 ("The deviation of sync_overcommit_as could be big … when changing policy to strict OVERCOMMIT_NEVER … sync percpu count on each CPU"), and the read is not the synced full sum used by `vm_memory_committed()` (939, whose cost is discussed at 932–935). "Fast" is inferred from the per-CPU design and read-vs-sum contrast, and from the entry's own Boundaries text ("the mode-2 test uses a cheaper approximate read (util.c.v7.2:994)"); it is not a literal word in the quote. Entailed.
Careless over-read risk: a reader could treat the read as exact (it may deviate by up to the batch per CPU — entry Boundaries), or conflate the approximate per-CPU read with the full meminfo sum `vm_memory_committed()`.

ENTAIL 967021950067 entailed

### Row 19 — hash 41934e8b2887
Claim: "Processes lacking CAP_SYS_ADMIN see the mode-2 limit lowered further by the admin reserve, converted to pages."
Quote located: `util.c.v7.2:982-983` (`if (!cap_sys_admin) allowed -= sysctl_admin_reserve_kbytes >> (PAGE_SHIFT - 10);`). Context read: 959–1003.
The ALWAYS (969–970) and GUESS (972–976) branches return before this line, so this code runs only in NEVER mode (mode 2, after `allowed = vm_commit_limit()` at 978). The comment at 954: "cap_sys_admin is 1 if the process has admin privileges, 0 otherwise." `sysctl_admin_reserve_kbytes >> (PAGE_SHIFT - 10)` is the kilobytes-to-pages conversion of the admin reserve. Entailed.
Careless over-read risk: a reader could think all processes see the reduction (holders of CAP_SYS_ADMIN skip it — `!cap_sys_admin`), or that it applies in modes 0/1 (the early returns prevent it), or confuse it with the user reserve at 988–992.

ENTAIL 41934e8b2887 entailed

### Row 20 — hash ca2418460394
Claim: "A refused request leaves a rate-limited kernel log warning that names the pid, the command and the byte count."
Quote located: `util.c.v7.2:998-999` (`pr_warn_ratelimited("%s: pid: %d, comm: %s, bytes: %lu not enough memory for the allocation\n",` / `__func__, current->pid, current->comm, bytes_failed);`). Context read: 996–1003.
Both refusal paths reach `error:` (GUESS oversize `goto error` at 974; never-overcommit fall-through at 996). The error path sets `bytes_failed = pages << PAGE_SHIFT` (byte count) and emits the rate-limited warning (`pr_warn_ratelimited`) naming `current->pid`, `current->comm`, and `bytes_failed`, then returns `-ENOMEM`. Entailed.
Careless over-read risk: a reader could treat each warning as an exact refusal count (the log is rate-limited, so refusals are not a count — the entry's reading rules say so), or read the message as an OOM-kill report (it is the ENOMEM refusal block, distinct from the OOM report), or read `comm` as the full command line (it is the short task comm).

ENTAIL ca2418460394 entailed

### Row 21 — hash 9cb0e908f997
Claim: "The compiled-in default for the ratio knob is fifty, meaning half of physical RAM under mode 2."
Quote located: `util.c.v7.2:782` (`static int sysctl_overcommit_ratio __read_mostly = 50;`). Context read: 775–810.
The quoted line is the compiled-in default (50). The "meaning" clause ("half of physical RAM under mode 2") is the documented semantics of `overcommit_ratio` in S498 (`vm.rst.v7.2:864-866`: "When overcommit_memory is set to 2, the committed address space is not permitted to exceed swap plus this percentage of physical RAM") and matches the ratio arm of `vm_commit_limit()` (911–912: `* sysctl_overcommit_ratio / 100`): 50% = half, applied in mode 2. The interpretation stays inside the committed sources; it is not a fabricated consequence. Entailed.
Careless over-read risk: a reader could read "half of physical RAM" as the whole commit limit (the ratio term is half of RAM minus hugetlb pages, with every swap page added on top — row 14's claim), or could assume 50 means 50% without the S498 percentage semantics, or think the ratio knob has an effect outside mode 2 (it is used only by the NEVER-mode limit).

ENTAIL 9cb0e908f997 entailed

## Environment notes
- Disk guard (`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`): exit 0, /fast/scratch/hyaku 24% used, 610.6G free.
- No tool installed; no lane or fleet file mutated; only read-only `git show`/grep/read on the lane, plus this report. Scratch `/fast/scratch/hyaku/mori-r52/Mo52Ent09/` created and removed on exit.
- Host reads: none beyond the allowed `/proc`/`sysctl` areas (not needed for these rows).

## Findings
- HIGH: none. All seven assigned rows (15–21) are entailed; no REPLACE lines.
- LOW (util.c.v7.2:994, row 18): the word "fast" in "a fast approximate read" is inferred from the per-CPU design and the read-vs-sum contrast (util.c:814–822, 918–921, 932–935) and the entry's own "cheaper approximate read" boundary sentence, not a literal word in the quoted line. If the L1 wants strictly literal wording, this is the only clause in these rows that is interpretive.
- LOW (util.c.v7.2:782, row 21): the clause "meaning half of physical RAM under mode 2" is grounded in S498 (`vm.rst.v7.2:864-866`) rather than the quoted S499 line; it is within the committed sources, so not an overclaim, but it is the one verdict that needed a second source row.
