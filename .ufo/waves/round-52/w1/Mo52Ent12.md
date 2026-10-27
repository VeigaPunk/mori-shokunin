# Mo52Ent12 — ENTAILMENT vote, rows 22–28

Seat: Mo52Ent12 (ENTAILMENT voter, twelve-voter list Mo52Ent01–Mo52Ent12).
Item: C2 entailment — judge claim rows 22–28 of the `## Claims` table in
`corpus/knowledge/overcommit-commit-limit-r52.md` at the data commit
`8524904adb25e44f24d9f25aac7eae909625c18c`.
Method per row: the quote was located in the committed copy under
`corpus/evidence/sources-r52/` (line numbers below); ~20 lines around each quote were
read; verdict: does the CLAIM cell follow from the quote plus that context?
Hashes below were recomputed with
`python3 -c 'import hashlib,re,sys;print(hashlib.sha256(re.sub(r"\s+"," ",sys.argv[1]).strip().encode()).hexdigest()[:12])' "<claim text>"`
and all seven match `evidence/c2-hashes-at-data.txt`.

## Row 22 — hash 2d64007fa0dc — entailed

- Claim: "Under the loose modes the per-CPU counter may drift far from its true sum, which is why switching to mode 2 syncs every CPU first."
- Quote: `The deviation of sync_overcommit_as could be big with loose policy * like OVERCOMMIT_ALWAYS/OVERCOMMIT_GUESS.` — `sources-r52/util.c.v7.2:814-815`.
- Context (util.c.v7.2:804-843): the full `overcommit_policy_handler` comment says the deviation can be big under OVERCOMMIT_ALWAYS/GUESS; when changing policy to strict OVERCOMMIT_NEVER the switch is done in order: (1) change the batch, (2) sync the percpu count on each CPU, (3) switch the policy (`util.c.v7.2:813-823`). `sync_overcommit_as` is scheduled on every CPU before `sysctl_overcommit_memory` is changed (lines 831-834). Mode 2 = OVERCOMMIT_NEVER (per S498 row 12 context, vm.rst "never overcommit").
- Verdict: entailed. "Drift far from its true sum" = "deviation could be big"; "syncs every CPU first" = step 2 of the switch, which precedes the policy change.
- Careless-reader over-read: "first" could be read as the very first step of the switch — the batch change (step 1) actually happens first; the sync precedes the policy flip, not every other action. Also "may drift" is a paraphrase of "could be big", not a measured bound.

## Row 23 — hash 02f5bfd6be3b — entailed

- Claim: "Charging the committed total is a batched add into a per-CPU counter, not a write to one global variable."
- Quote: `static inline void vm_acct_memory(long pages) { percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch); }` — `sources-r52/mman.h.v7.2:76-79`.
- Context (mman.h.v7.2:69-93): `vm_acct_memory` is the only charge path shown; it adds `pages` to `vm_committed_as` via `percpu_counter_add_batch` with `vm_committed_as_batch`. `vm_committed_as` is the committed total (util.c prints it as `vm_memory_committed()`; row 18 context uses `percpu_counter_read_positive(&vm_committed_as)`). `percpu_counter_add_batch` is a batched add into a per-CPU counter — not a single-global-variable write.
- Verdict: entailed.
- Careless-reader over-read: "per-CPU counter" is implied by the percpu_counter API, not spelled out in the quoted line; and "not a write to one global variable" is an inference from the API's nature — the source does not contrast it with a global-variable design.

## Row 24 — hash ff0d23e9fde8 — entailed

- Claim: "Releasing a commitment uses the same batched add with the page count negated."
- Quote: `static inline void vm_unacct_memory(long pages) { vm_acct_memory(-pages); }` — `sources-r52/mman.h.v7.2:81-84`.
- Context (mman.h.v7.2:69-93): `vm_unacct_memory` forwards to `vm_acct_memory(-pages)`, i.e. the same batched add from row 23 with the page count negated. In util.c, `vm_unacct_memory(pages)` is called when a request is refused, undoing the earlier charge (`util.c.v7.2:1000`), and by `__mm_drop_locks`/do_munmap paths (`mmap.c.v7.2:1326,1893,1919`).
- Verdict: entailed.
- Careless-reader over-read: "releasing a commitment" is the well's semantic for unaccounting; the literal code only negates the page count — it does not itself say the counter is a commitment ledger.

## Row 25 — hash 0fbd62f51ce8 — entailed

- Claim: "For ordinary mappings MAP_NORESERVE drops commit charging only when the mode is something other than never-overcommit."
- Quote: `We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vm_flags \|= VM_NORESERVE;` — `sources-r52/mmap.c.v7.2:551-553`.
- Context (mmap.c.v7.2:539-573): inside `if (flags & MAP_NORESERVE)`, `VM_NORESERVE` (the flag that means "we should not account for the memory use of this mapping", comment at lines 546-549) is set only when `sysctl_overcommit_memory != OVERCOMMIT_NEVER`. So the commit charge is dropped for an ordinary mapping only when the mode is not never-overcommit; under mode 2 the flag is ignored for these mappings (and S497 row 5's "In mode 2 the MAP_NORESERVE flag is ignored" corroborates).
- Verdict: entailed.
- Careless-reader over-read: "ordinary mappings" — the claim is scoped to non-hugetlb mappings; the adjacent hugetlb branch (row 26) is an exception, and a careless reader could apply this row to hugetlb too. Also "drops commit charging" maps to `VM_NORESERVE` being set, which the quoted line does not spell out.

## Row 26 — hash d7a1dc88dcb3 — entailed

- Claim: "Hugetlb file mappings are charged strictly unless the caller passes MAP_NORESERVE, a carve-out the mode-2 rule does not mention."
- Quote: `hugetlb applies strict overcommit unless MAP_NORESERVE */ if (file && is_file_hugepages(file)) vm_flags \|= VM_NORESERVE;` — `sources-r52/mmap.c.v7.2:555-557`.
- Context (mmap.c.v7.2:539-573): the hugetlb branch is inside `if (flags & MAP_NORESERVE)` and sets `VM_NORESERVE` unconditionally (for a hugepage file), i.e. even when the outer mode-2 guard at line 552 would not set it. A hugepage file mapping without `MAP_NORESERVE` never enters the block, so it is charged strictly; with the flag, it is exempted regardless of mode. The mode-2 rule (S497 row 5: "In mode 2 the MAP_NORESERVE flag is ignored") does not mention this hugetlb exception — hence "carve-out the mode-2 rule does not mention".
- Verdict: entailed.
- Careless-reader over-read: the strict-charge clause is only about the absence of `MAP_NORESERVE`; and "carve-out … does not mention" depends on the S497 mode-2 sentence (another row's quote) — within this file's context alone the mode-2 rule is not visible.

## Row 27 — hash 10dc80bb5b2e — entailed

- Claim: "At boot the user reserve knob is set to the smaller of one thirty-second of free memory and 128 MiB."
- Quote: `sysctl_user_reserve_kbytes = min(free_kbytes / 32, SZ_128K);` — `sources-r52/mmap.c.v7.2:1595`.
- Context (mmap.c.v7.2:1579-1623): `init_user_reserve()` runs as `subsys_initcall` (line 1598), i.e. at boot; `free_kbytes = K(global_zone_page_state(NR_FREE_PAGES))` (line 1593) is current free memory in kB; the assignment caps at `min(free_kbytes / 32, SZ_128K)`. `SZ_128K` = 0x00020000 = 131072; since `free_kbytes` is in kB, the cap numeric 131072 kB = 128 MiB, matching the function comment "The default value is min(3% of free memory, 128MB)" (line 1586) — note 1/32 = 3.125%, the comment's "3%" is the same expression rounded.
- Verdict: entailed.
- Careless-reader over-read: `SZ_128K` reads as "128 KiB", not 128 MiB; the units of the comparison (free_kbytes in kB) are what make the cap 128 MiB. "At boot" comes from the `subsys_initcall` registration, not from the quoted line itself.

## Row 28 — hash 42295e410c2b — entailed

- Claim: "At boot the admin reserve knob is set to the smaller of one thirty-second of free memory and 8 MiB."
- Quote: `sysctl_admin_reserve_kbytes = min(free_kbytes / 32, SZ_8K);` — `sources-r52/mmap.c.v7.2:1616`.
- Context (mmap.c.v7.2:1600-1623): `init_admin_reserve()` runs as `subsys_initcall` (line 1619); `free_kbytes` same as row 27; `SZ_8K` = 0x2000 = 8192, and as a kB cap 8192 kB = 8 MiB, matching the comment "Systems with more than 256MB will reserve 8MB" (lines 1606-1607).
- Verdict: entailed.
- Careless-reader over-read: same unit trap as row 27 — `SZ_8K` is 8192, applied to a kB value it is 8 MiB; "at boot" again comes from the `subsys_initcall` registration.

## Verdict lines (rows 22–28; one per row; unfenced)

ENTAIL 2d64007fa0dc entailed
ENTAIL 02f5bfd6be3b entailed
ENTAIL ff0d23e9fde8 entailed
ENTAIL 0fbd62f51ce8 entailed
ENTAIL d7a1dc88dcb3 entailed
ENTAIL 10dc80bb5b2e entailed
ENTAIL 42295e410c2b entailed

## Supplemental replacement votes from L1

The L1 supplied replacement cells for rows 27 and 28. I checked each against
`mmap.c.v7.2:1585-1619` and `vm.rst.v7.2:1029-1046`. In the source, `free_kbytes`
is divided by 32 and compared with `SZ_128K` / `SZ_8K`; these `SZ_*` values are
byte constants (128 KiB / 8 KiB), while the `*_reserve_kbytes` variables and
`free_kbytes` are in kB. Separately, the code comments state the documented
defaults as 128 MB and 8 MB; vm.rst states the documented user default as 128MB.
The replacement wording distinguishes the initial byte-constant cap from the
documented default and correctly preserves the units.

ENTAIL 10ac5a250ac2 entailed
ENTAIL 1cadeed9914b entailed

No REPLACE lines: no overclaim found. The seven hashes above are the table's row hashes at the data commit, verified by recomputation.

## Findings

- MED — Row 27/28 unit reading: the cap constants `SZ_128K`/`SZ_8K` are byte quantities; because `free_kbytes` is in kB, the effective cap is 128 MiB / 8 MiB, not 128 KiB / 8 KiB. The claims are correct, but a careless reader will misread the quote's units (`mmap.c.v7.2:1595,1616`).
- LOW — Row 22 "first": the sync of every CPU precedes the policy switch but follows the batch change; "first" is an ordering claim about the switch, not about the whole handler (`util.c.v7.2:819-822`).
- LOW — Row 26: the mode-2 "ignored" rule lives in S497 (row 5's quote); the hugetlb carve-out is only visible by reading both sources together (`mmap.c.v7.2:555-557` + `overcommit-accounting.rst.v7.2:48`).
