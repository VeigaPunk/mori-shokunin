# Mo52CritC2Prose — prose attack on the C2 entry (round 52, wave w1)

Seat: `Mo52CritC2Prose` (ucritic, prose). Lane: mori-shokunin. Fleet root:
`/home/vgpnk/Projects/shokunin`. Lane repo:
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Target at data commit
`8524904adb25e44f24d9f25aac7eae909625c18c`.

Scratch: `/fast/scratch/hyaku/mori-r52/Mo52CritC2Prose/` (created, used, removed before finish).

## Scope

Attacked prose only — the intro, `## Reading rules (mori)` and `## Boundaries` of
`corpus/knowledge/overcommit-commit-limit-r52.md` at the data commit — not the claim rows. Two
tests per sentence: (1) it says more than the five copies in
`corpus/evidence/sources-r52/` (plus the round-51 copy `corpus/evidence/sources-r51/meminfo.c.v7.2`)
support; (2) a mori operator could misread it as advice to change a sysctl.

## Evidence basis (observed)

- Entry and copies at the data commit are byte-identical to the working tree
  (verified: `git -C … show 8524904a…:corpus/knowledge/overcommit-commit-limit-r52.md | diff - <(cat …)`
  → no output, exit 0; same for the five `sources-r52/` copies via `cmp` → identical).
- Read fully: `overcommit-accounting.rst.v7.2` (85 lines), `vm.rst.v7.2` (overcommit sections),
  `util.c.v7.2` (lines 780-1003), `mmap.c.v7.2` (lines 110-240, 480-620, 1200-1245),
  `mman.h.v7.2`, `meminfo.c.v7.2` (S494).
- Key located lines:
  - `util.c.v7.2:959-1003` `__vm_enough_memory()`: charge first (`vm_acct_memory(pages)` at 964),
    ALWAYS returns 0 (969-970), GUESS refuses only when `pages > totalram_pages() + total_swap_pages`
    (972-976), otherwise mode-2: `allowed = vm_commit_limit()` minus admin reserve for non-root
    (982-983) minus `min(mm->total_vm / 32, user_reserve)` (988-992), success iff
    `percpu_counter_read_positive(&vm_committed_as) < allowed` (994).
  - `util.c.v7.2:937-940` `vm_memory_committed()` returns `percpu_counter_sum_positive(&vm_committed_as)`.
  - `util.c.v7.2:814-823` comment: deviation of `sync_overcommit_as` "could be big with loose policy";
    switching to `OVERCOMMIT_NEVER` syncs per-CPU counts. No numeric bound anywhere.
  - `mman.h.v7.2:65,78`: `vm_committed_as_batch` declared; used as batch in `percpu_counter_add_batch`.
  - `mmap.c.v7.2:550-558`: `MAP_NORESERVE` sets `VM_NORESERVE` unless mode is `OVERCOMMIT_NEVER`,
    but always for hugetlb file mappings (556-557).
  - `mmap.c.v7.2:1781`: `dup_mmap` calls `security_vm_enough_memory_mm(oldmm, len)` (fork path).
  - `mmap.c.v7.2:116-215`: `brk` syscall path — checks `check_data_rlimit` (150), `check_brk_limits`
    (181), vma gaps; no commit-limit refusal visible; `do_brk_flags` body is not in this file.
  - `vm.rst.v7.2:832-833`: "Setting one disables the other (which then appears as 0 when read)."
  - `vm.rst.v7.2:1032-1044`: `user_reserve_kbytes` — reserve `min(3% of current process size,
    user_reserve_kbytes)`; with reserve 0, "Any subsequent attempts to execute a command will result in
    'fork: Cannot allocate memory'."
  - `meminfo.c.v7.2:125-126` (S494): `CommitLimit` / `Committed_AS` printed unconditionally, any mode;
    `committed = vm_memory_committed()` (line 46).
- Checked-clean statements (no finding): mode 0 GUESS refusal exactly `pages > totalram+swap`; mode 1
  never refuses; CommitLimit printed under every mode and consulted only under mode 2; "CommitLimit … is
  enforced only under mode 2"; the `102vm_enough_memory:` kernel-line format matches
  `pr_warn_ratelimited` (998-999); rate-limited ⇒ not a count; `overcommit_ratio` reads 0 ⇒ kbytes in
  force; tsukuroi PROVINCE.md lines 8-14, 28 say "detection and report; the operator remediates" (path
  `tsukuroi-shokunin/PROVINCE.md` resolves correctly from `corpus/knowledge/`); FR8 exists and stays open
  (README.md FR8 row; audit-r11.md:205).

## Findings

### Finding 1 (MED) — unsourced numeric bound on the read-vs-sum difference

Quote (entry `## Boundaries`, lines 71-72): "`Committed_AS` is a per-CPU counter; the meminfo line is
its full sum (`util.c.v7.2:937-940`), and the mode-2 test uses a cheaper approximate read
(`util.c.v7.2:994`). The two can differ by up to the batch size per CPU."

Source line it needs: a statement of the bound. The cited lines show only *that* the two reads differ
(`percpu_counter_sum_positive` vs `percpu_counter_read_positive`); `util.c.v7.2:814-823` calls the
deviation "could be big" under loose policy and gives no number; `vm_committed_as_batch` is declared
(`mman.h.v7.2:65`) but the batch value, the number of CPUs whose slack the cheap read omits, and any
"up to batch" bound are in none of the five copies (nor in the S494 meminfo copy). The sentence asserts a
finitely bounded magnitude the copies do not contain, and as written is ambiguous about whether "batch
size per CPU" is the per-CPU slack or the total deviation (the total can be the sum over the other CPUs'
pending deltas).

```markdown
`Committed_AS` is a per-CPU counter; the meminfo line is its full sum (`util.c.v7.2:937-940`), and the
mode-2 test uses a cheaper approximate read (`util.c.v7.2:994`), so the two can differ. The magnitude is
not stated by the v7.2 sources (`util.c.v7.2:814-823` only says the deviation "could be big" under loose
policy) [INFERENCE — bounds the difference with a host-side read if one is needed].
```

### Finding 2 (MED) — untagged temporal claim "before MemAvailable is low"

Quote (entry `## Reading rules (mori)`, row 2): "| `Committed_AS` near `CommitLimit` under mode 2 |
new private writable mappings, `brk` and `fork` can fail with ENOMEM before `MemAvailable` is low | that
running processes will be killed: mode 2 refuses at request time |"

Source line it needs: any statement comparing ENOMEM timing with the `MemAvailable` level. S497's mode-2
text ("a process will not be killed while accessing pages but will receive errors on memory allocation as
appropriate") and S498's `"fork: Cannot allocate memory"` example say refusal happens at request time;
none of the copies relate that to how low `MemAvailable` is. "before `MemAvailable` is low" is an
ordering claim about host behavior that no copy supports (and it is not universally true: if the commit
limit is high relative to actual usage, the first refusals can coincide with `MemAvailable` already low).
It is also the kind of sentence an operator could read as a rule of thumb.

```markdown
| `Committed_AS` near `CommitLimit` under mode 2 | new private writable mappings, `brk` and `fork` can
fail with ENOMEM at request time; this can happen while `MemAvailable` is not low [INFERENCE] | that
running processes will be killed: mode 2 refuses at request time |
```

### Finding 3 (LOW) — `brk` listed as an ENOMEM path without a locating source

Quote (same row 2): "new private writable mappings, `brk` and `fork` can fail with ENOMEM".

Source line it needs: a committed source showing a commit-limit refusal in the `brk` path. `fork` has
S498's `"fork: Cannot allocate memory"` and S501's `dup_mmap` check (`mmap.c.v7.2:1781`); private
writable mappings have S497's mode-2 sentence plus the "PRIVATE WRITABLE - size of mapping per instance"
accounting rule. For `brk`, S497 lists only "We account brk" in the Status section (accounting, not
refusal), and the visible brk code in S501 (`mmap.c.v7.2:116-215`, `1205-1245`) checks `RLIMIT_DATA` /
`check_brk_limits` but contains no commit-limit refusal; `do_brk_flags` is not in any copy. The
brk-ENOMEM linkage says more than the five copies support.

```markdown
new private writable mappings and `fork` can fail with ENOMEM; `brk` growth is committed (S497: "We
account brk") and can likewise fail at request time [INFERENCE — the `brk` refusal path is not in the
five copies]
```

### Finding 4 (LOW) — printed CommitLimit treated as the mode-2 threshold; non-root ceiling is lower

Quote (entry `## Reading rules (mori)`, row 2): "`Committed_AS` near `CommitLimit` under mode 2 …"
and (intro, line 17) "Under mode 2 the kernel refuses a request once the committed total would reach the
limit."

Source line it needs: the reserve subtraction in the mode-2 branch. `util.c.v7.2:982-992` lowers the
effective ceiling for non-root processes by `sysctl_admin_reserve_kbytes` and by
`min(mm->total_vm / 32, sysctl_user_reserve_kbytes)`; `vm.rst.v7.2:1032-1044` documents the user
reserve. So the operative mode-2 ceiling is below the printed `CommitLimit` for non-root processes: a
refusal can occur while `Committed_AS` is still below the printed line, and "once the committed total
would reach the limit" overstates the printed line's role. An operator measuring headroom against printed
`CommitLimit` alone can overestimate the safe margin.

```markdown
| `Committed_AS` near `CommitLimit` under mode 2 (for non-root processes the effective ceiling is lower
by `admin_reserve_kbytes` plus `min(3% of process size, user_reserve_kbytes)`, `util.c.v7.2:982-992`)
| new private writable mappings, `brk` and `fork` can fail with ENOMEM … |
```

## Findings

| # | severity | file / line | finding |
|---|---|---|---|
| 1 | MED | `corpus/knowledge/overcommit-commit-limit-r52.md` `## Boundaries` (lines 71-72) | the read-vs-sum difference is bounded "up to the batch size per CPU" with no such bound in the five copies |
| 2 | MED | same file `## Reading rules (mori)` row 2 (line 59) | "before `MemAvailable` is low" is an unsourced, untagged ordering claim |
| 3 | LOW | same file `## Reading rules (mori)` row 2 (line 59) | `brk` listed as an ENOMEM path without any locating source in the five copies |
| 4 | LOW | same file `## Reading rules (mori)` row 2 (line 59) and intro (line 17) | printed `CommitLimit` treated as the mode-2 threshold; non-root effective ceiling is lower by the reserves |

No HIGH findings. No sentence is misreadable as advice to change a sysctl (the entry's
"host configuration, which the operator owns" framing is correct and matches PROVINCE.md). Data wording
corrections are for the L1, not the wave; the counter and contract are untouched.
