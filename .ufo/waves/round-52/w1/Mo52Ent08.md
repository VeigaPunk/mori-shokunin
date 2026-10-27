# Mo52Ent08 — ENTAILMENT verdicts, round 52 wave w1

Seat: `Mo52Ent08` (entailment voter). Item: claim rows 15–21 of
`corpus/knowledge/overcommit-commit-limit-r52.md` at data commit
`8524904adb25e44f24d9f25aac7eae909625c18c` (all rows cite S499 →
`corpus/evidence/sources-r52/util.c.v7.2`).

Method: quotes were located in the committed copies under
`corpus/evidence/sources-r52/` with a whitespace-flexible matcher; the ~20-line
context around each quote was read (the whole enclosing function for rows
15–20). Source bytes were verified byte-identical three ways: working tree vs
`evidence/freeze-sha256.txt` vs `git show 8524904…:<path>` (all 5 files,
sha256 match). Each claim hash was recomputed with the frozen formula
(`sha256(re.sub(r"\s+"," ",claim).strip())[:12]`) and matches the filed hash.

## Verdict lines (rows 15–21)

ENTAIL a75ce7619818 entailed
ENTAIL 309f4487d8b6 entailed
ENTAIL cddcf1bc062f entailed
ENTAIL 967021950067 entailed
ENTAIL 41934e8b2887 entailed
ENTAIL ca2418460394 entailed
ENTAIL 9cb0e908f997 entailed

## Per-row worksheet

### Row 15 — `a75ce7619818` (S499)
Claim: *When the kbytes knob is nonzero it replaces the ratio term entirely,
after conversion from kilobytes to pages.*
Quote: `if (sysctl_overcommit_kbytes) allowed = sysctl_overcommit_kbytes >> (PAGE_SHIFT - 10);`
— `util.c.v7.2:908-909`, inside `vm_commit_limit()` (901–916). Context: the
`else` branch (910–912) computes the ratio-based `allowed`; the kbytes branch
assigns `sysctl_overcommit_kbytes >> (PAGE_SHIFT - 10)` (kilobytes → pages);
`allowed += total_swap_pages;` runs after either branch (913).
Verdict: **entailed**. The if/else structure means the nonzero-kbytes branch
replaces the ratio term entirely; the shift is the kilobytes-to-pages
conversion.
Over-read risk: the kbytes branch replaces only the *ratio term*; swap is
added on top in both branches (913) — a careless reader could read the claim
as kbytes capping the whole limit including swap.

### Row 16 — `309f4487d8b6` (S499)
Claim: *In the default heuristic mode a request fails only when its own size
exceeds all RAM plus all swap together.*
Quote: `if (pages > totalram_pages() + total_swap_pages) goto error; return 0;`
— `util.c.v7.2:973-975`, inside the `OVERCOMMIT_GUESS` branch (972–976) of
`__vm_enough_memory()` (959–1003). Context: function docstring 943–958; the
default policy is `OVERCOMMIT_GUESS` (`sysctl_overcommit_memory __read_mostly =
OVERCOMMIT_GUESS;`, line 781). The branch fails (`goto error`) exactly when
`pages > totalram_pages() + total_swap_pages`, otherwise `return 0`.
Verdict: **entailed**.
Over-read risk: "fails only when its own size exceeds all RAM plus all swap"
describes the commit-refusal gate; the allocator can still fail elsewhere
(ENOMEM from address-space limits, faults), so the claim must not be read as
the only failure mode of allocations in mode 0.

### Row 17 — `cddcf1bc062f` (S499)
Claim: *Every request is charged to the committed counter before the mode is
examined, so the counter grows under modes 0 and 1 too.*
Quote: `vm_acct_memory(pages); /* * Sometimes we want to use more memory than
we have */ if (sysctl_overcommit_memory == OVERCOMMIT_ALWAYS) return 0;`
— `util.c.v7.2:964-970`. Context: `vm_acct_memory(pages)` runs first (964);
the ALWAYS check (969–970) and the GUESS check (972–976) come after; the error
path uncharges later (`vm_unacct_memory(pages)`, 1000). Under mode 1 (ALWAYS)
the function returns 0 after charging; under mode 0 (GUESS) accepted requests
keep the charge — so the counter grows under both.
Verdict: **entailed**.
Over-read risk: "every request" means every request that reaches
`__vm_enough_memory()`; requests carrying `MAP_NORESERVE` skip commit charging
under modes 0/1 (rows 25–26, S501). A careless reader applying "every"
literally to every mapping would over-read.

### Row 18 — `967021950067` (S499)
Claim: *The never-overcommit test compares a fast approximate read of the
per-CPU committed counter with the computed limit.*
Quote: `if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;`
— `util.c.v7.2:994-995`. Context: reached only after the ALWAYS/GUESS returns
(969–976), i.e. the NEVER (mode-2) path; `allowed = vm_commit_limit();` (978);
`vm_committed_as` is a `struct percpu_counter` kept in one cacheline, "updated
by several CPUs frequently" (919–922); the exact-sum accessor
`vm_memory_committed()` uses `percpu_counter_sum_positive` (937–940), while
this hot test uses the `read_positive` variant — the read-vs-sum pair in the
same region supports the "fast approximate read" characterization.
Verdict: **entailed**.
Over-read risk: "fast approximate" is inferred from the read-vs-sum function
pair (lines 939 vs 994), not stated verbatim in util.c; it should be read
qualitatively, not as a timing guarantee.

### Row 19 — `41934e8b2887` (S499)
Claim: *Processes lacking CAP_SYS_ADMIN see the mode-2 limit lowered further by
the admin reserve, converted to pages.*
Quote: `if (!cap_sys_admin) allowed -= sysctl_admin_reserve_kbytes >> (PAGE_SHIFT - 10);`
— `util.c.v7.2:982-983`. Context: this code is reached only after the ALWAYS
(969–970) and GUESS (972–976) branches return, so it is the mode-2 (NEVER)
path; `allowed` is the computed limit (978); the comment "Reserve some for
root" (979–981); the shift converts kilobytes to pages.
Verdict: **entailed**.
Over-read risk: "lowered further" refers to lowering the base computed limit by
the admin reserve; the user-reserve lowering (988–991) is a separate,
additional reduction — a careless reader could conflate the two.

### Row 20 — `ca2418460394` (S499)
Claim: *A refused request leaves a rate-limited kernel log warning that names
the pid, the command and the byte count.*
Quote: `pr_warn_ratelimited("%s: pid: %d, comm: %s, bytes: %lu not enough memory for the allocation\n",`
— `util.c.v7.2:998` (args on 999: `__func__, current->pid, current->comm,
bytes_failed`). Context: the `error:` label (996); `bytes_failed = pages <<
PAGE_SHIFT` (997); `vm_unacct_memory(pages)` (1000); `return -ENOMEM` (1002).
The warning names the pid (`current->pid`), the command (`current->comm`) and
the byte count (`bytes_failed`), and `pr_warn_ratelimited` is rate-limited.
Verdict: **entailed**.
Over-read risk: rate limiting suppresses repeated warnings, so the absence of a
log line is not evidence that no refusal happened (the entry's reading-rules
table already notes "rate-limited, so not a count").

### Row 21 — `9cb0e908f997` (S499)
Claim: *The compiled-in default for the ratio knob is fifty, meaning half of
physical RAM under mode 2.*
Quote: `static int sysctl_overcommit_ratio __read_mostly = 50;`
— `util.c.v7.2:782`. Context: the sysctl defaults block (781–786) — GUESS is
the default policy (781), kbytes defaults to 0 (783); the ratio is applied as
a percentage of RAM in `vm_commit_limit()` (`allowed = ((totalram_pages() -
hugetlb_total_pages()) * sysctl_overcommit_ratio / 100);`, 911–912), which is
the OVERCOMMIT_NEVER (mode-2) limit (901–903). With the compiled-in 50, the
RAM term is half of (RAM − hugetlb).
Verdict: **entailed**.
Over-read risk: "half of physical RAM" glosses the hugetlb subtraction; the
exact formula is `swap + (RAM − hugetlb) × ratio/100` (claimed in row 14) — a
careless reader could read "half of physical RAM" as an absolute cap including
swap.

## Evidence

- Sources byte-identity (working tree vs `evidence/freeze-sha256.txt` vs `git
  show 8524904…:<path>`, sha256, all five files): all match.
  `overcommit-accounting.rst.v7.2` 767ab88153c4494e…; `vm.rst.v7.2`
  bf8ca0265fefc019…; `util.c.v7.2` e702754c45bd7bd6…; `mman.h.v7.2`
  d7bf787c910d9a7c…; `mmap.c.v7.2` 449b858385c7ece0…
- Quote locations (all `corpus/evidence/sources-r52/util.c.v7.2`): row 15
  908–909; row 16 973–975; row 17 964–970; row 18 994–995; row 19 982–983;
  row 20 998–999; row 21 782. Locator command (my scratch):
  `python3 /fast/scratch/hyaku/mori-r52/Mo52Ent08/locate2.py` rc=0; corrected
  whitespace-flexible matching, rc=0.
- Hash recomputation for rows 15–21 with
  `python3 -c 'import hashlib,re,sys;print(hashlib.sha256(re.sub(r"\s+"," ",sys.argv[1]).strip().encode()).hexdigest()[:12])' "<claim text>"`
  — all seven match the filed hashes (a75ce7619818, 309f4487d8b6,
  cddcf1bc062f, 967021950067, 41934e8b2887, ca2418460394, 9cb0e908f997).
- `evidence/c2-at-data.txt` at 8524904: `located=28 quote_missing=0
  bad_rows=0 failed=entailment` (all 28 quotes, including the seven above,
  locate).

## Findings

- LOW — Row 17 claim wording "Every request is charged…" is accurate only for
  requests reaching `__vm_enough_memory()`; MAP_NORESERVE mappings bypass commit
  charging under modes 0/1. Covered by rows 25–26 of the same entry, so no
  correction needed. File: `corpus/knowledge/overcommit-commit-limit-r52.md`
  (claim row 17).
- LOW — Row 18's "fast approximate read" is an inference from the read-vs-sum
  function pair (`util.c.v7.2:939` vs `:994`), not a literal statement in the
  source. Keep qualitative; no correction needed. File: same entry (claim row
  18).
- LOW — Row 21's "half of physical RAM" glosses the hugetlb subtraction in
  `vm_commit_limit()` (`util.c.v7.2:911-912`); the exact formula is row 14. No
  correction needed. File: same entry (claim row 21).
- LOW — Row 20's rate-limited warning means a missing log line is not evidence
  of no refusal; the entry's reading-rules table already states this. File:
  same entry (reading rules row 3).
