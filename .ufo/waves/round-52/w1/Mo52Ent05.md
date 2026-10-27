# Mo52Ent05 — ENTAILMENT votes, rows 8–14 (C2 entry `overcommit-commit-limit-r52.md`)

Seat Mo52Ent05, leaf (no subagents). Item: judge claim rows 8–14 of the `## Claims`
table of `corpus/knowledge/overcommit-commit-limit-r52.md` at data commit
`8524904adb25e44f24d9f25aac7eae909625c18c`.

Method: the entry was read with `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show
8524904adb25e44f24d9f25aac7eae909625c18c:corpus/knowledge/overcommit-commit-limit-r52.md`.
The frozen evidence copies were extracted read-only into seat scratch
(`/fast/scratch/hyaku/mori-r52/Mo52Ent05/`) with `git show`; no mutation of the lane, its
jj state, git index, or any repo file was performed. Each quote cell was located verbatim
in the frozen copy (whitespace-tolerant regex over raw bytes; line ranges below are the
first–last line of the match). ~20 lines around each quote were read before judging. Row
hashes were taken from `.ufo/waves/round-52/evidence/c2-hashes-at-data.txt`; all seven
were re-computed with the prescribed one-liner (`sha256` of the whitespace-normalised,
stripped claim text, first 12 hex) and all match.

Data examined:

- S498 `corpus/evidence/sources-r52/vm.rst.v7.2` (rows 8–13)
- S499 `corpus/evidence/sources-r52/util.c.v7.2` (row 14)

## Row-by-row judgment

### Row 8 — `43cf2a78acdd` — ENTAILED
Quote: `vm.rst.v7.2:841-842` — "When this flag is 0, the kernel compares the userspace
memory request size against total memory plus swap and rejects obvious overcommits."
Claim: "In mode 0 a single request is compared with all RAM plus all swap, not with what
is currently free." Every element maps: flag=0 (overcommit_memory, default 0 at line 848)
→ mode 0; "userspace memory request size" → a single request; "total memory plus swap" →
all RAM plus all swap; the comparison target being total memory+swap entails it is not
current free memory. Entailed.
Over-read risk: "total memory" could be misread as free/MemAvailable; it means full
physical RAM + swap. Also, "rejects obvious overcommits" applies to a single request's
size, not to the aggregate committed total (mode 0 refuses nothing on aggregate-commit
grounds).

### Row 9 — `35d642f1d0d9` — ENTAILED
Quote: `vm.rst.v7.2:844-845` — "When this flag is 1, the kernel pretends there is always
enough memory until it actually runs out."
Claim: "Mode 1 never refuses an allocation on commit grounds; the kernel behaves as though
memory were unlimited until it is exhausted." "Pretends there is always enough memory"
entails no commit-based refusal; "until it actually runs out" matches "until it is
exhausted". Entailed.
Over-read risk: "pretends there is always enough memory" could be over-read as
allocations never fail at all; the source's "until it actually runs out" is the bound the
claim preserves.

### Row 10 — `fcd0e7a78872` — ENTAILED
Quote: `vm.rst.v7.2:864-866` — "When overcommit_memory is set to 2, the committed address
space is not permitted to exceed swap plus this percentage of physical RAM."
Claim: "The ratio setting is a percentage cap on physical RAM that applies only in mode 2,
with swap added on top." "Percentage cap on physical RAM" = "this percentage of physical
RAM"; "swap added on top" = "swap plus ..."; the sentence is conditional on mode 2 and the
mode 0/1 descriptions (lines 841–845) never involve the ratio, so "only in mode 2" is an
entailment, not an added scope. Entailed.
Over-read risk: assuming the ratio participates in modes 0/1 (the mode 0/1 paragraphs are
the only behaviour descriptions for those modes and are ratio-free); or reading the cap as
applying to RAM+swap jointly rather than swap added on top.

### Row 11 — `5c40f6fa5c62` — ENTAILED
Quote: `vm.rst.v7.2:831-833` — "Only one of them may be specified at a time. Setting one
disables the other (which then appears as 0 when read)."
Claim: "The kbytes and ratio knobs are mutually exclusive, so a ratio that reads 0 can
simply mean the kbytes knob is in force." "Mutually exclusive" = "Only one of them may be
specified at a time"; the 0-reading consequence is verbatim, and the claim's "can simply
mean" hedge exactly matches the source's conditional phrasing. Entailed.
Over-read risk: reading "appears as 0 when read" as "ratio=0 always means kbytes is in
force" (the source only says setting one disables the other; 0 is one possible meaning).
The claim is correctly hedged.

### Row 12 — `00e2a9db523b` — ENTAILED
Quote: `vm.rst.v7.2:1032-1033` — "When overcommit_memory is set to 2, "never overcommit"
mode, reserve min(3% of current process size, user_reserve_kbytes) of free memory."
Claim: "Mode 2 also holds back a user reserve sized from the requesting process and capped
by the user_reserve_kbytes knob." "Holds back a user reserve" = "reserve ... of free
memory" in the user_reserve_kbytes section; "sized from the requesting process" = "3% of
current process size" (the process being evaluated; context lines 1034–1036: "prevent a
user from starting a single memory hogging process"); "capped by the user_reserve_kbytes
knob" = the min(..., user_reserve_kbytes). Entailed.
Over-read risk: treating the reserve as a fixed 3% of total free memory rather than 3% of
the current process size (the min with `user_reserve_kbytes` caps it); or reading it as
active under modes 0/1 (context line 1037: "has no effect when overcommit_memory is set to
0 or 1").

### Row 13 — `bfb15534fa5e` — ENTAILED
Quote: `vm.rst.v7.2:92-93` — "That should provide enough for the admin to log in and kill
a process, if necessary, under the default overcommit 'guess' mode."
Claim: "The admin reserve exists so that root can still log in and kill a runaway process
when memory runs short." Purpose clause matches verbatim ("log in and kill a process");
"root" is the admin (section context lines 86–88: reserved for users with `cap_sys_admin`;
line 95: "root may not be able to log in"); "when memory runs short" restates the section's
premise (reserving free memory under the default guess mode). The adjective "runaway" is a
gloss not in the source — it adds no consequence, number, or scope, and the claim's
functional content (existence, purpose, conditions) is fully supported. Entailed.
Over-read risk: importing properties of the killed process from "runaway" (e.g. the
process being unkillable or out of control) that the source never attributes; the source
only says "kill a process, if necessary".

### Row 14 — `28d3042fded0` — ENTAILED
Quote: `util.c.v7.2:911-913` — "allowed = ((totalram_pages() - hugetlb_total_pages()) *
sysctl_overcommit_ratio / 100); allowed += total_swap_pages;"
Claim: "CommitLimit is RAM minus hugetlb pages, scaled by the ratio percentage, with every
swap page then added on top." Exact term-by-term mapping: RAM=totalram_pages(); minus
hugetlb pages; scaled by ratio percentage (* sysctl_overcommit_ratio / 100); every swap
page added on top (allowed += total_swap_pages). The function is `vm_commit_limit()` with
comment "Committed memory limit enforced when OVERCOMMIT_NEVER policy is used" (lines
903–905), the value printed as `CommitLimit` in `/proc/meminfo` per the entry's framing.
Entailed.
Over-read risk: reading the formula as unconditional. The expression is the `else` branch
of the `if (sysctl_overcommit_kbytes)` at lines 909–910; when kbytes is nonzero the limit
is instead `sysctl_overcommit_kbytes >> (PAGE_SHIFT - 10)` + swap (row 15 covers that
branch). The claim restates exactly the quoted code and does not deny the kbytes branch,
so I do not treat the omission as an overclaim, but the branch conditionality is the
sharpest over-read point in this row.

## Verdict lines

ENTAIL 43cf2a78acdd entailed
ENTAIL 35d642f1d0d9 entailed
ENTAIL fcd0e7a78872 entailed
ENTAIL 5c40f6fa5c62 entailed
ENTAIL 00e2a9db523b entailed
ENTAIL bfb15534fa5e entailed
ENTAIL 28d3042fded0 entailed

## Findings

- LOW — row 14 (`corpus/knowledge/overcommit-commit-limit-r52.md`, claim cell S499):
  the ratio formula is stated without restating its `sysctl_overcommit_kbytes == 0`
  branch condition (`util.c.v7.2:909-910`). The claim follows from the quote and is
  covered jointly with row 15, but an unconditional reader would over-read it.
- LOW — row 13 (same entry, claim cell S498): "runaway process" is a gloss beyond the
  verbatim source ("kill a process, if necessary", `vm.rst.v7.2:92-93`); no new
  consequence/number/scope is added, so the verdict stands entailed.
- INFO — over-read cautions per row are recorded above; no HIGH/MED findings. No data or
  wording errors found in rows 8–14; no REPLACE lines proposed.

Scratch (`/fast/scratch/hyaku/mori-r52/Mo52Ent05/`) removed on completion; no files were
created anywhere outside the seat scratch and this report file.
