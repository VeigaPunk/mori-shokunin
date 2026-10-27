# Mo52Ent07 — ENTAILMENT votes, claim rows 15–21 (block 3, all S499)

Seat: Mo52Ent07 (leaf, no subagents). Data commit: `8524904adb25e44f24d9f25aac7eae909625c18c`.
Entry: `corpus/knowledge/overcommit-commit-limit-r52.md` at that commit (read via
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8524904adb25e44f24d9f25aac7eae909625c18c:corpus/knowledge/overcommit-commit-limit-r52.md`).
Sources: committed copies extracted to scratch from the same commit
(`git show 8524904…:corpus/evidence/sources-r52/<file>`); sha256 of each copy matches the
`corpus/SOURCES.md` pins and the working tree (767ab881…, bf8ca026…, e702754c…, d7bf787c…, 449b8583…).

Method per row: locate the quote in the committed source copy (exact match, one occurrence), read the
surrounding lines in that copy, judge whether the `claim` cell follows from quote plus context.

## Votes

ENTAIL a75ce7619818 entailed
ENTAIL 309f4487d8b6 entailed
ENTAIL cddcf1bc062f entailed
ENTAIL 967021950067 entailed
ENTAIL 41934e8b2887 entailed
ENTAIL ca2418460394 entailed
ENTAIL 9cb0e908f997 entailed

## Row-by-row judgment

### Row 15 — `a75ce7619818` — entailed
Claim: "When the kbytes knob is nonzero it replaces the ratio term entirely, after conversion from kilobytes to pages."
Quote: `` if (sysctl_overcommit_kbytes) allowed = sysctl_overcommit_kbytes >> (PAGE_SHIFT - 10); `` —
`util.c.v7.2:908` (S499).
Context: `vm_commit_limit()` (`util.c.v7.2:906-917`): if `sysctl_overcommit_kbytes` is truthy the
`allowed` term is the kbytes value shifted right by `PAGE_SHIFT - 10`; otherwise the else branch computes the
ratio term; in both branches `allowed += total_swap_pages;` runs afterwards. The shift converts kilobytes to
pages (KB / (PAGE_SIZE/1024) = shift by PAGE_SHIFT−10). The claim's "replaces the ratio term entirely" matches
the if/else structure; "after conversion" matches the shift.
Over-read risk: a careless reader could over-read "replaces the ratio term" as replacing the whole limit — the
swap add still runs after both branches, and the kbytes branch is only reached when `vm_commit_limit()` is
consulted (the mode-2 path).

### Row 16 — `309f4487d8b6` — entailed
Claim: "In the default heuristic mode a request fails only when its own size exceeds all RAM plus all swap together."
Quote: `` if (pages > totalram_pages() + total_swap_pages) goto error; return 0; `` — `util.c.v7.2:973` (S499).
Context: `__vm_enough_memory()` (`util.c.v7.2:958-1001`); the default policy is
`int sysctl_overcommit_memory __read_mostly = OVERCOMMIT_GUESS;` (`util.c.v7.2:780`). In the
`OVERCOMMIT_GUESS` branch (`util.c.v7.2:972-976`) the request fails only when `pages` exceeds
`totalram_pages() + total_swap_pages`; otherwise `return 0`. The claim states exactly this branch's logic.
Over-read risk: "fails only when" is scoped to the heuristic (default) mode and a careless reader could over-read
it as a property of every mode; "all RAM plus all swap" is total capacity, not what is currently free.

### Row 17 — `cddcf1bc062f` — entailed
Claim: "Every request is charged to the committed counter before the mode is examined, so the counter grows under modes 0 and 1 too."
Quote: `` vm_acct_memory(pages); /* * Sometimes we want to use more memory than we have */ if (sysctl_overcommit_memory == OVERCOMMIT_ALWAYS) return 0; `` — `util.c.v7.2:964-966` (S499).
Context: `vm_acct_memory(pages);` is the first statement of `__vm_enough_memory()` (line 963), before either
mode test. `OVERCOMMIT_ALWAYS` (mode 1) returns success immediately after charging; `OVERCOMMIT_GUESS` (mode 0)
returns success when the request passes the size check, leaving the charge in place (failed requests are uncharged
via `vm_unacct_memory(pages)` at the `error:` label). So the committed counter grows under modes 0 and 1 for
accepted requests.
Over-read risk: "every request" means every request that reaches this gate (the LSM allocation helper), and under
mode 0 a refused request is uncharged — a careless reader could over-read it as every allocation in the kernel,
or as unconditional growth under mode 0.

### Row 18 — `967021950067` — entailed
Claim: "The never-overcommit test compares a fast approximate read of the per-CPU committed counter with the computed limit."
Quote: `` if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0; `` — `util.c.v7.2:994` (S499).
Context: this comparison sits on the `OVERCOMMIT_NEVER` path (after the ALWAYS and GUESS branches have returned,
`util.c.v7.2:967-995`); `allowed` is the computed limit from `vm_commit_limit()` minus the reserves. The counter
is declared `struct percpu_counter vm_committed_as ____cacheline_aligned_in_smp;` with the comment "It can be
updated by several CPUs frequently." (`util.c.v7.2:918-922`). The same file uses `percpu_counter_sum_positive()`
for the exact meminfo sum (`util.c.v7.2:939`), so `percpu_counter_read_positive` here is the per-CPU read
variant, cheaper than the full sum. The claim's "fast approximate" is a faithful gloss of the read-vs-sum
distinction visible within this file (lines 939 vs 994), not a verbatim word in the source.
Over-read risk: a careless reader could over-read "computed limit" as fixed for a boot (it depends on the ratio/
kbytes knob and reserves) or think the meminfo `Committed_AS` line uses the same approximate read (it uses the
full sum, line 939).

### Row 19 — `41934e8b2887` — entailed
Claim: "Processes lacking CAP_SYS_ADMIN see the mode-2 limit lowered further by the admin reserve, converted to pages."
Quote: `` if (!cap_sys_admin) allowed -= sysctl_admin_reserve_kbytes >> (PAGE_SHIFT - 10); `` — `util.c.v7.2:982` (S499).
Context: `__vm_enough_memory()` takes `cap_sys_admin` from the calling process; after `allowed = vm_commit_limit();`
(only on the never-overcommit path, `util.c.v7.2:978-981`), the check `if (!cap_sys_admin)` subtracts the admin
reserve in pages (shift by `PAGE_SHIFT - 10`). The comment "Reserve some for root" (line 980) frames it.
Over-read risk: a careless reader could over-read "mode-2 limit lowered further" as applying in every mode — this
subtraction runs only on the never-overcommit path; the "converted to pages" step is the right shift.

### Row 20 — `ca2418460394` — entailed
Claim: "A refused request leaves a rate-limited kernel log warning that names the pid, the command and the byte count."
Quote: `` pr_warn_ratelimited("%s: pid: %d, comm: %s, bytes: %lu not enough memory for the allocation\n", `` — `util.c.v7.2:998` (S499).
Context: at the `error:` label (`util.c.v7.2:996-1002`): `bytes_failed = pages << PAGE_SHIFT;` then
`pr_warn_ratelimited(... __func__, current->pid, current->comm, bytes_failed);`, then
`vm_unacct_memory(pages); return -ENOMEM;`. The error label is reached exactly from the refusal paths (GUESS
size check and the mode-2 compare). `pr_warn_ratelimited` is rate-limited; the format names pid (`current->pid`),
comm (`current->comm`) and the byte count (`bytes_failed`).
Over-read risk: a careless reader could over-read "leaves a warning" as a reliable per-refusal record — the
warning is rate-limited, so it is not a count; "the command" is `comm` (the task's command name), not the full
command line.

### Row 21 — `9cb0e908f997` — entailed
Claim: "The compiled-in default for the ratio knob is fifty, meaning half of physical RAM under mode 2."
Quote: `` static int sysctl_overcommit_ratio __read_mostly = 50; `` — `util.c.v7.2:782` (S499).
Context: the static initializer sets the ratio knob to 50 at compile time. In `vm_commit_limit()`
(`util.c.v7.2:911-914`) the ratio term is `(totalram_pages() - hugetlb_total_pages()) * sysctl_overcommit_ratio / 100`,
i.e. 50 means half of the RAM-minus-hugetlb term; `vm_commit_limit()` is used only on the mode-2 (never-overcommit) path.
Over-read risk: a careless reader could over-read "half of physical RAM" as including hugetlb pages (the formula
subtracts them) or as the whole limit (swap is added on top afterwards).

## Verification notes
- Hash recomputation: for each of the seven claim cells I extracted from the entry table at the data commit,
  `sha256(re.sub(r"\s+"," ",claim).strip()).hexdigest()[:12]` matches the frozen row hashes in
  `.ufo/waves/round-52/evidence/c2-hashes-at-data.txt` (rows 15–21: a75ce7619818, 309f4487d8b6, cddcf1bc062f,
  967021950067, 41934e8b2887, ca2418460394, 9cb0e908f997).
- Source copies: extracted via `git show 8524904…:corpus/evidence/sources-r52/<file>` into scratch; sha256 of all
  five match both the SOURCES.md pins and the lane working tree (no drift between the data commit and the disk).
- Quotes: each of the seven quote strings is an exact, single match in the committed `util.c.v7.2` copy (line
  numbers given above); no quote occurs more than once, no quote required normalisation beyond whitespace.
- No row needed a REPLACE line, so no replacement text is proposed.

## Findings
- No HIGH findings. All seven assigned rows (15–21) are entailed: quote, immediate context and the claim's
  wording agree; no consequence, number or scope beyond the source is added.
- MED: row 18's "fast approximate read" is a gloss inferred from the read-vs-sum API pair and the per-CPU
  declarations inside `util.c.v7.2` (lines 939 vs 994, 918-922), not a verbatim descriptor in the source; the
  claim is accurate, but the word "approximate" is not literally present. File: `corpus/knowledge/overcommit-commit-limit-r52.md`, claim row 18.
- LOW: row 21's "half of physical RAM" omits the hugetlb subtraction in the ratio formula (`util.c.v7.2:912`);
  the claim matches the documentation phrasing (S497) and the code's intent, but a reader could over-read it as
  literal total RAM. File: `corpus/knowledge/overcommit-commit-limit-r52.md`, claim row 21.
- LOW: row 17's "every request" and row 20's "leaves a warning" are scoped by the rate-limit and by the
  uncharge-on-failure path; a careless reader could over-read them as unconditional. File:
  `corpus/knowledge/overcommit-commit-limit-r52.md`, claim rows 17 and 20.
