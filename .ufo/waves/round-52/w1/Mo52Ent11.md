# Mo52Ent11 — entailment votes, claim rows 22–28 (round 52, wave w1)

Seat: Mo52Ent11, ENTAILMENT voter for rows 22–28 of the `## Claims` table of
`corpus/knowledge/overcommit-commit-limit-r52.md`. Data commit judged:
`8524904adb25e44f24d9f25aac7eae909625c18c` (confirmed to exist in the lane; hash recheck below). Host:
MACHINE_ID. Date: 2026-10-26. Leaf seat: no subagents used. No tools installed or upgraded (none needed).
No ENTAIL or REPLACE vote was cast for any row other than 22–28, and I authored none of the rows' text, so no
authorship conflict exists; consequently there are no replacement proposals in this report.

## Method and literal commands

All reads of lane bytes were read-only (`git show` against the data commit; no clone, no index writes, no working-tree
edits). Scratch was `/fast/scratch/hyaku/mori-r52/Mo52Ent11/` with `TMPDIR` pointed inside it; it is removed at the
end of this run (all quoted evidence is reproduced in this report first).

```
mkdir -p /fast/scratch/hyaku/mori-r52/Mo52Ent11/tmp
export TMPDIR=/fast/scratch/hyaku/mori-r52/Mo52Ent11/tmp
/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
# -> exit=0; /fast/scratch/hyaku 24% used, 612.8G free — no ENOSPC risk

git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8524904adb25e44f24d9f25aac7eae909625c18c:corpus/knowledge/overcommit-commit-limit-r52.md > entry-at-data.md   # 75 lines
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse 8524904adb25e44f24d9f25aac7eae909625c18c                                                               # -> same full hash
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree --name-only 8524904adb25e44f24d9f25aac7eae909625c18c:corpus/evidence/sources-r52/
# -> mman.h.v7.2 mmap.c.v7.2 overcommit-accounting.rst.v7.2 util.c.v7.2 vm.rst.v7.2
for f in mman.h.v7.2 mmap.c.v7.2 overcommit-accounting.rst.v7.2 util.c.v7.2 vm.rst.v7.2; do
  git -C /home/vgpnk/Projects/shokunin/mori-shokunin show "8524904adb25e44f24d9f25aac7eae909625c18c:corpus/evidence/sources-r52/$f" > "sources/$f"; done
sha256sum sources/*
# 767ab881… overcommit-accounting.rst.v7.2 / bf8ca026… vm.rst.v7.2 / e702754c… util.c.v7.2
# d7bf787c… mman.h.v7.2    / 449b8583… mmap.c.v7.2 — all five match the entry's `recheck:` line
```

Hash recheck (docstring command from the seat spec, applied to the claim cells extracted from the committed entry's
table): all seven rows MATCH the frozen hashes in
`.ufo/waves/round-52/evidence/c2-hashes-at-data.txt` — `2d64007fa0dc`, `02f5bfd6be3b`, `ff0d23e9fde8`,
`0fbd62f51ce8`, `d7a1dc88dcb3`, `10dc80bb5b2e`, `42295e410c2b`.

Quote-location recheck (whitespace-normalized substring, same normalization class as the counter): all seven quotes
FOUND in the extracted committed copies, at the line numbers cited per row below.

## Row judgments

For each row: quote location in the committed copy, the ~20 lines of context read, the verdict, and the part of the
source a careless reader might over-read. All seven verdicts are recorded in the verdict-lines section; there is
exactly one vote per row and no vote for any other row.

### Row 22 — S499 (util.c) — hash 2d64007fa0dc — vote: entailed

Claim: "Under the loose modes the per-CPU counter may drift far from its true sum, which is why switching to mode 2
syncs every CPU first."

- Quote at `util.c.v7.2:814-815` (inside the `overcommit_policy_handler` comment block, lines 813–822): "The
  deviation of sync_overcommit_as could be big with loose policy * like OVERCOMMIT_ALWAYS/OVERCOMMIT_GUESS."
- Context read: 795–845. `sync_overcommit_as` (801–804) runs `percpu_counter_sync(&vm_committed_as)`. The comment
  states the switch order: "1. changing the batch 2. sync percpu count on each CPU 3. switch the policy". The code
  (830–834) implements exactly that: `mm_compute_batch(new_policy);` then
  `if (new_policy == OVERCOMMIT_NEVER) schedule_on_each_cpu(sync_overcommit_as);` then
  `sysctl_overcommit_memory = new_policy;`.
- Judgment: every element is stated. "Loose modes" mirrors the source's "loose policy like
  OVERCOMMIT_ALWAYS/OVERCOMMIT_GUESS"; "may drift far from its true sum" mirrors "deviation … could be big";
  "syncs every CPU" mirrors `schedule_on_each_cpu` / "sync percpu count on each CPU"; "first" mirrors steps 2 before 3
  (the sync precedes the policy variable flipping), confirmed by code order.
- Careless over-read: (a) the sync is step 2 of 3 — the batch change runs first — so "first" means "before the policy
  takes effect", not "the first action"; (b) the comment concerns the per-CPU cached deviation at the switch, not the
  `Committed_AS` meminfo line being wrong under modes 0/1 — the meminfo line is the full sum (the entry's own
  Boundaries section says the mode-2 test uses the cheaper approximate read at `util.c.v7.2:994`).

### Row 23 — S500 (mman.h) — hash 02f5bfd6be3b — vote: entailed

Claim: "Charging the committed total is a batched add into a per-CPU counter, not a write to one global variable."

- Quote at `mman.h.v7.2:76-79`:
  `static inline void vm_acct_memory(long pages) { percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch); }`
- Context read: 55–95. `extern struct percpu_counter vm_committed_as;` (62); `extern s32 vm_committed_as_batch;`
  under `CONFIG_SMP` (65), `#define vm_committed_as_batch 0` (67) otherwise; `vm_unacct_memory` below (81–84).
- Judgment: the target is a percpu_counter and the charge goes through `percpu_counter_add_batch` — a batched add
  into a per-CPU counter. The contrast clause describes that mechanism and contradicts nothing shown.
- Careless over-read: "not a write to one global variable" does not mean the central count is never written —
  `percpu_counter_add_batch` spills into the central count once the accumulated delta exceeds the batch, and under
  !SMP the batch is 0. The claim's wording stays on the right side; a reader must not harden it into "never touches
  the global".

### Row 24 — S500 (mman.h) — hash ff0d23e9fde8 — vote: entailed

Claim: "Releasing a commitment uses the same batched add with the page count negated."

- Quote at `mman.h.v7.2:81-84`:
  `static inline void vm_unacct_memory(long pages) { vm_acct_memory(-pages); }`
- Context read: 55–95 (same block as row 23; `vm_unacct_memory` delegates to the row-23 function).
- Judgment: literal. Same batched add (`vm_acct_memory`), page count negated (`-pages`). Nothing added.
- Careless over-read: the source does not scope the callers (munmap, error unwind, …); the claim does not either —
  a reader should not infer a caller list from these four lines.

### Row 25 — S501 (mmap.c) — hash 0fbd62f51ce8 — vote: entailed

Claim: "For ordinary mappings MAP_NORESERVE drops commit charging only when the mode is something other than
never-overcommit."

- Quote at `mmap.c.v7.2:551-553`:
  "We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vm_flags |= VM_NORESERVE;"
- Context read: 534–570. The enclosing guard is `if (flags & MAP_NORESERVE) {` (550), under the comment
  "Set 'VM_NORESERVE' if we should not account for the memory use of this mapping." (546–548). The sibling hugetlb
  branch (555–557) is the next statement inside the same guard.
- Judgment: "drops commit charging" = setting VM_NORESERVE ("should not account"); it happens for a
  MAP_NORESERVE-carrying request only when the mode is not OVERCOMMIT_NEVER. Under OVERCOMMIT_NEVER this branch sets
  nothing, so the request stays charged — consistent with the docs' blanket rule the entry quotes elsewhere
  (`overcommit-accounting.rst.v7.2:48` "In mode 2 the MAP_NORESERVE flag is ignored."). "Ordinary mappings" correctly
  excludes the hugetlb sibling branch, which row 26 covers.
- Careless over-read: for shared/read-only file mappings the charge is 0 anyway (S497's cost table), so
  MAP_NORESERVE's effect there is vacuous — "drops charging" is about the accounting decision, not a change in the
  number actually added for such mappings.

### Row 26 — S501 (mmap.c) — hash d7a1dc88dcb3 — vote: entailed

Claim: "Hugetlb file mappings are charged strictly unless the caller passes MAP_NORESERVE, a carve-out the mode-2
rule does not mention."

- Quote at `mmap.c.v7.2:555-557`:
  "hugetlb applies strict overcommit unless MAP_NORESERVE */ if (file && is_file_hugepages(file)) vm_flags |= VM_NORESERVE;"
- Context read: 534–570. The branch sits inside `if (flags & MAP_NORESERVE)` (550): for a hugetlb file mapping the
  caller's MAP_NORESERVE always yields VM_NORESERVE, regardless of mode — i.e., honored even under mode 2. Without
  the flag this block sets nothing, so hugetlb keeps its strict treatment (the comment's own words).
- Judgment: first clause paraphrases the comment exactly ("applies strict overcommit unless MAP_NORESERVE"). Second
  clause cross-checked in the committed copies: `overcommit-accounting.rst.v7.2:48` states the mode-2 rule
  ("In mode 2 the MAP_NORESERVE flag is ignored.") and the string "hugetlb" does not occur anywhere in that
  document — the carve-out is indeed unmentioned there. Both halves hold at the strictness bar.
- Careless over-read: "charged strictly" echoes the hugetlb reservation strictness the comment names; the actual
  reservation path (`hugetlb_reserve_pages`) is not among the five sources, so the claim must not — and does not —
  state that hugetlb mappings flow through the Committed_AS charge path of `__vm_enough_memory`. Keep reading
  "charged strictly" as "subject to strict overcommit accounting", per the comment.

### Row 27 — S501 (mmap.c) — hash 10dc80bb5b2e — vote: entailed

Claim: "At boot the user reserve knob is set to the smaller of one thirty-second of free memory and 128 MiB."

- Quote at `mmap.c.v7.2:1595`: `sysctl_user_reserve_kbytes = min(free_kbytes / 32, SZ_128K);`
- Context read: 1579–1683. `init_user_reserve()` (1589) computes
  `free_kbytes = K(global_zone_page_state(NR_FREE_PAGES));` (1593) and is registered by
  `subsys_initcall(init_user_reserve);` (1598) — a boot-time initcall. The min has exactly two terms; no third
  clamp is applied in this copy. Magnitudes are grounded inside the committed copy itself: the comment
  "The default value is min(3% of free memory, 128MB)" (1584), "The default user reserve max is 128MB" (1646),
  "Default max is 128MB." (1648). The knob is kbytes-valued, so SZ_128K = 131072 KB = 128 MiB.
- Judgment: boot registration, free memory basis, 1/32, two-term min, 128 MiB cap — all stated by the quote plus
  context. No added consequence.
- Careless over-read: (a) the neighboring comment says "3%" while the code (and the claim) say 1/32 ≈ 3.1% — quote
  the code, not the comment; (b) "free memory" is `NR_FREE_PAGES` at init time, not `MemAvailable`; (c) the knob is
  re-initialised later on memory hotplug (`reserve_mem_notifier`, 1646–1654 and MEM_OFFLINE 1660–1663) — the claim
  covers the boot setting only, which is what it says.

### Row 28 — S501 (mmap.c) — hash 42295e410c2b — vote: entailed

Claim: "At boot the admin reserve knob is set to the smaller of one thirty-second of free memory and 8 MiB."

- Quote at `mmap.c.v7.2:1616`: `sysctl_admin_reserve_kbytes = min(free_kbytes / 32, SZ_8K);`
- Context read: 1579–1683. `init_admin_reserve()` (1610), same `free_kbytes` computation (1614), registered by
  `subsys_initcall(init_admin_reserve);` (1619). Magnitudes grounded in-copy: "Systems with more than 256MB will
  reserve 8MB" (1606–1607), "the default max for the admin reserve is 8MB" (1632), "Default max is 8MB." (1651).
  The knob is kbytes-valued, so SZ_8K = 8192 KB = 8 MiB.
- Judgment: boot registration, free memory basis, 1/32, two-term min, 8 MiB cap — all stated by the quote plus
  context.
- Careless over-read: the comment block describes "3% of free pages" for smaller systems (1606–1608) versus the
  code's /32 — same comment-vs-code gap as row 27; and SZ_8K must be read in the knob's kbytes unit, not bytes
  (the comments' "8MB" confirm the intended magnitude).

## Verdict lines

One vote per given row (22–28), each unfenced, in canonical row order:

ENTAIL 2d64007fa0dc entailed
ENTAIL 02f5bfd6be3b entailed
ENTAIL ff0d23e9fde8 entailed
ENTAIL 0fbd62f51ce8 entailed
ENTAIL d7a1dc88dcb3 entailed
ENTAIL 10dc80bb5b2e entailed
ENTAIL 42295e410c2b entailed

No `overclaim` verdicts were reached, so no replacement proposals accompany these votes. No vote above is for a row
outside 22–28, and none of these rows was authored by this seat.

## Replacement-row votes (L1-authored, rows 27/28)

The L1 (MoriR52) authored replacement text for rows 27 and 28 and asked this seat to judge each against
`mmap.c.v7.2:1585-1619` and `vm.rst.v7.2:1029-1046`. This seat did not write either replacement, so both votes
count (no authorship conflict). Source copies were re-extracted from the data commit for this check:

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show "8524904adb25e44f24d9f25aac7eae909625c18c:corpus/evidence/sources-r52/mmap.c.v7.2" > mmap.c.v7.2
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show "8524904adb25e44f24d9f25aac7eae909625c18c:corpus/evidence/sources-r52/vm.rst.v7.2" > vm.rst.v7.2
sha256sum mmap.c.v7.2 vm.rst.v7.2    # 449b8583… / bf8ca026… — match the entry's `recheck:` line
```

Hashes recomputed with the docstring command from the seat spec — both MATCH the L1-provided hashes:
`10ac5a250ac2` and `1cadeed9914b`.

### Row 27 replacement — hash 10ac5a250ac2 — vote: entailed

Replacement claim: "At boot the user reserve knob starts at the smaller of one thirty-second of free memory in kB
and the byte constant SZ_128K - 128 KiB, while the documented default is 128 MiB."

- `mmap.c.v7.2:1589-1598`: `init_user_reserve()` sets `sysctl_user_reserve_kbytes = min(free_kbytes / 32, SZ_128K);`
  (1595), registered by `subsys_initcall(init_user_reserve);` (1598) — boot-time; `free_kbytes` is kB
  (1593, `K(global_zone_page_state(NR_FREE_PAGES))`).
- Documented default: `mmap.c.v7.2:1586` "The default value is min(3% of free memory, 128MB)";
  `vm.rst.v7.2:1039` "user_reserve_kbytes defaults to min(3% of the current process size, 128MB)."
- The operand `SZ_128K` appears verbatim (1595); as the kernel size macro it denotes 128 KiB (131072 bytes), the
  byte-sized constant the code compares against the kbytes-scaled free-memory term.
- Verdict: every element maps to the cited lines — boot init, the two-term min with `free_kbytes / 32` (kB) and
  `SZ_128K`, and the separately-documented 128 MB (MiB) default. Nothing asserts a behavior or scope the sources
  omit; the claim keeps the byte-constant reading and the documented MiB default distinct.
- Careless over-read: taking "byte constant SZ_128K - 128 KiB" for the effective cap in the kbytes-scaled
  comparison (the documented 128 MiB default is the intended cap per the code's own comments); "at boot/starts at"
  covers only the initial initcall setting — the knob is re-initialised on hotplug (`mmap.c.v7.2:1646-1654`);
  the 3% prose vs `/32` (3.125%) gap persists — the claim follows the code.

### Row 28 replacement — hash 1cadeed9914b — vote: entailed

Replacement claim: "At boot the admin reserve knob starts at the smaller of one thirty-second of free memory in kB
and the byte constant SZ_8K - 8 KiB, while the documented default is 8 MiB."

- `mmap.c.v7.2:1610-1619`: `init_admin_reserve()` sets `sysctl_admin_reserve_kbytes = min(free_kbytes / 32, SZ_8K);`
  (1616), registered by `subsys_initcall(init_admin_reserve);` (1619) — boot-time.
- Documented default: `mmap.c.v7.2:1606-1607` "Systems with more than 256MB will reserve 8MB";
  `vm.rst.v7.2:90` "admin_reserve_kbytes defaults to min(3% of free pages, 8MB)".
- The operand `SZ_8K` appears verbatim (1616); as the kernel size macro it denotes 8 KiB (8192 bytes).
- Verdict: entailed — same structure as row 27; boot init, the two-term min, and the documented 8 MB (MiB) default
  all map to the cited lines. Nothing added.
- Careless over-read: same three cautions as row 27 (byte-constant reading vs documented 8 MiB default; boot-only
  scope; `/32` vs 3% prose).

The original rows 27/28 verdict lines remain recorded above under their old hashes (`10dc80bb5b2e`,
`42295e410c2b`); the lines below vote the L1-authored replacement texts, which this seat did not write.

Verdict lines for these L1-authored replacements (unfenced):

ENTAIL 10ac5a250ac2 entailed
ENTAIL 1cadeed9914b entailed

## Compliance notes

- Wrote only this report file inside the lane; all other work happened under `/fast/scratch/hyaku/mori-r52/Mo52Ent11/`
  (removed at end of run). No git/jj mutation anywhere; the lane was only read via `git show`/`ls-tree`/`rev-parse`.
- No sysctl, cgroup, systemctl/journalctl, kernel-log message grep, OOM or large-allocation action was performed;
  host access was limited to the disk-guard status read (exit 0).
- Scratch cleanup command (run after this report was written):
  `rm -rf /fast/scratch/hyaku/mori-r52/Mo52Ent11` — the quoted bytes above are committed lane content
  (data commit 8524904adb25e44f24d9f25aac7eae909625c18c), so removal loses no evidence.
- Named limits carried into this report per contract: a vote is a committed reviewer judgment over the five committed
  copies, not outside verification; the v7.2 bytes say nothing about other kernels or this host's sysctl values
  (entry Boundaries agree). No counter weakness was found in the entailment arm; nothing to route to round 53 from
  this seat.

Report: .ufo/waves/round-52/w1/Mo52Ent11.md

## Findings

- LOW — rows 27–28 (`corpus/knowledge/overcommit-commit-limit-r52.md` rows 27–28; `corpus/evidence/sources-r52/mmap.c.v7.2:1584,1606-1607`):
  the source's own comments say "3%" where the code and the claim cells say one thirty-second (≈3.1%). The claim
  cells follow the code correctly; risk is only that a future editor quotes the comment instead of the code. No
  change requested.
- LOW — row 23 (claim cell "…not a write to one global variable"): mechanism-descriptive contrast;
  `percpu_counter_add_batch` still spills to the central count past the batch and the !SMP batch is 0
  (`mman.h.v7.2:65-67`). Wording-risk note only; the claim as written is entailed.
- LOW — row 22 (claim cell "…syncs every CPU first"): the documented switch order has the batch change (step 1)
  before the per-CPU sync (step 2) (`util.c.v7.2:819-822,830-834`); "first" is true relative to the policy taking
  effect. Wording-risk note only.
- LOW — row 26 (claim cell "…are charged strictly"): the strictness is hugetlb reservation strictness per the code
  comment (`mmap.c.v7.2:555`); the reservation path is not among the five sources, so the claim must stay — and
  stays — inside the comment's words. Wording-risk note only.
- No HIGH or MED findings. All seven assigned rows judged `entailed`; no counter weakness, no contract deviation, and
  no host-state anomaly observed by this seat.

