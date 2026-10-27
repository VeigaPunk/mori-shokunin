# Mo52Ent06 — entailment votes, C2 claim rows 8–14

Seat: Mo52Ent06 (ENTAILMENT, C2 arm). Item: judge claim rows 8–14 of the `## Claims`
table of `corpus/knowledge/overcommit-commit-limit-r52.md` at
`8524904adb25e44f24d9f25aac7eae909625c18c`. Sources read from the committed copies under
`corpus/evidence/sources-r52/` (`git show 8524904a:corpus/evidence/sources-r52/<name>`).

All seven hashes recomputed with the round command
(`hashlib.sha256(re.sub(r"\s+"," ",s).strip().encode()).hexdigest()[:12]`) and match
`evidence/c2-hashes-at-data.txt` rows 8–14 (43cf2a78acdd, 35d642f1d0d9, fcd0e7a78872,
5c40f6fa5c62, 00e2a9db523b, bfb15534fa5e, 28d3042fded0).

ENTAIL 43cf2a78acdd entailed
ENTAIL 35d642f1d0d9 entailed
ENTAIL fcd0e7a78872 entailed
ENTAIL 5c40f6fa5c62 entailed
ENTAIL 00e2a9db523b entailed
ENTAIL bfb15534fa5e entailed
ENTAIL 28d3042fded0 entailed

## Row-by-row judgment

### Row 8 — 43cf2a78acdd
- Claim: "In mode 0 a single request is compared with all RAM plus all swap, not with what is currently free."
- Source S498 `vm.rst.v7.2:841-842` (quote): "When this flag is 0, the kernel compares the userspace memory request size against total memory plus swap and rejects obvious overcommits."
- Context (`vm.rst.v7.2:836-855`): the overcommit_memory flag section; line 855 confirms "The default value is 0" (mode 0 is the default); line 841-842 says the request size is compared against total memory plus swap.
- Judgment: entailed. "single request" = "the userspace memory request size"; "all RAM plus all swap" = "total memory plus swap"; the contrast "not with what is currently free" is an accurate reading of "against total memory plus swap" (the comparison base is the total, not the free amount). No number, consequence or scope beyond the source.
- Over-read risk: "rejects obvious overcommits" might be over-read as "rejects all overcommits"; the quote only says obvious ones are rejected. The claim itself does not make that error.

### Row 9 — 35d642f1d0d9
- Claim: "Mode 1 never refuses an allocation on commit grounds; the kernel behaves as though memory were unlimited until it is exhausted."
- Source S498 `vm.rst.v7.2:844-845` (quote): "When this flag is 1, the kernel pretends there is always enough memory until it actually runs out."
- Context (`vm.rst.v7.2:844-858`): the sentence is self-contained; lines 847-848 contrast mode 2's "never overcommit" policy, and line 857-858 points to overcommit-accounting.rst and `__vm_enough_memory()`.
- Judgment: entailed. "never refuses an allocation on commit grounds" restates "pretends there is always enough memory" (no commit check is applied); "until it is exhausted" matches "until it actually runs out". The claim's first clause is the entailment, the second is the quote.
- Over-read risk: a careless reader could take "never refuses" literally in the absolute and miss the "until it actually runs out" boundary; the claim keeps the boundary.

### Row 10 — fcd0e7a78872
- Claim: "The ratio setting is a percentage cap on physical RAM that applies only in mode 2, with swap added on top."
- Source S498 `vm.rst.v7.2:864-866` (quote): "When overcommit_memory is set to 2, the committed address space is not permitted to exceed swap plus this percentage of physical RAM."
- Context (`vm.rst.v7.2:861-867`): the overcommit_ratio section; the "See above" cross-reference to line 828-829 ("...the committed address space is not permitted to exceed swap plus this amount of physical RAM").
- Judgment: entailed. "percentage cap on physical RAM" = "this percentage of physical RAM"; "applies only in mode 2" = "When overcommit_memory is set to 2"; "swap added on top" = "not permitted to exceed swap plus ...". All three claim parts map 1:1 to the quote.
- Over-read risk: "percentage cap on physical RAM" alone could be over-read as a cap on RAM only; the cap is swap + percentage of RAM. The claim includes the swap part.

### Row 11 — 5c40f6fa5c62
- Claim: "The kbytes and ratio knobs are mutually exclusive, so a ratio that reads 0 can simply mean the kbytes knob is in force."
- Source S498 `vm.rst.v7.2:831-833` (quote): "Note: overcommit_kbytes is the counterpart of overcommit_ratio. Only one of them may be specified at a time. Setting one disables the other (which then appears as 0 when read)."
- Context (`vm.rst.v7.2:825-833`): the overcommit_kbytes section; line 828-829 states the same limit formula wording.
- Judgment: entailed. "mutually exclusive" = "Only one of them may be specified at a time"; "a ratio that reads 0 can simply mean the kbytes knob is in force" = "Setting one disables the other (which then appears as 0 when read)". The claim's "can simply mean" preserves the source's non-exclusive reading (the doc does not say 0 only ever means the other knob).
- Over-read risk: "can simply mean" is correctly hedged; a careless reader might over-read a 0 ratio as proof the kbytes knob is in force, while the doc says only that this is what happens when one disables the other.

### Row 12 — 00e2a9db523b
- Claim: "Mode 2 also holds back a user reserve sized from the requesting process and capped by the user_reserve_kbytes knob."
- Source S498 `vm.rst.v7.2:1032-1033` (quote): "When overcommit_memory is set to 2, "never overcommit" mode, reserve min(3% of current process size, user_reserve_kbytes) of free memory."
- Context (`vm.rst.v7.2:1029-1046`): the user_reserve_kbytes section; line 1034-1035 states the intent ("prevent a user from starting a single memory hogging process, such that they cannot recover (kill the hog)"); line 1037 confirms "This setting has no effect when overcommit_memory is set to 0 or 1"; line 1039 gives the default.
- Judgment: entailed. "holds back a user reserve" = "reserve ... of free memory"; "sized from the requesting process" = "min(3% of current process size, ...)"; "capped by the user_reserve_kbytes knob" = the min term "user_reserve_kbytes". All elements are in the quote; the mode-2-only condition is in both the quote and line 1037.
- Over-read risk: "sized from the requesting process" alone could over-read as proportional to process size without a cap; the min() with user_reserve_kbytes is the cap. The claim names the cap.

### Row 13 — bfb15534fa5e
- Claim: "The admin reserve exists so that root can still log in and kill a runaway process when memory runs short."
- Source S498 `vm.rst.v7.2:92-93` (quote): "That should provide enough for the admin to log in and kill a process, if necessary, under the default overcommit 'guess' mode."
- Context (`vm.rst.v7.2:84-97`): "The amount of free memory in the system that should be reserved for users with the capability cap_sys_admin."; line 90 "admin_reserve_kbytes defaults to min(3% of free pages, 8MB)"; lines 95-97 "Systems running under overcommit 'never' should increase this ... Otherwise, root may not be able to log in to recover the system."
- Judgment: entailed. "exists so that root can still log in and kill a process" = "provide enough for the admin to log in and kill a process" (admin with cap_sys_admin is the root-equivalent audience; line 96 uses "root" for the same actor). "runaway process" glosses the recovery scenario (kill to recover, cf. line 97 "recover the system"); "when memory runs short" restates "if necessary" — the reserved free memory's purpose is exactly the low-memory recovery case, and the guess mode is the policy under which memory can run short. No new number, consequence or scope; the "guess mode" condition is omitted but not contradicted (the claim does not say the reserve is absent or ineffective under mode 2, and lines 95-97 discuss the 'never' case as a separate tuning).
- Over-read risk: the quote's condition is "under the default overcommit 'guess' mode"; a careless reader could extend the claim's "when memory runs short" to mode 2, where the doc says the reserve also matters but needs a larger amount (lines 95-97). The claim itself is silent on that, so it does not overclaim.

### Row 14 — 28d3042fded0
- Claim: "CommitLimit is RAM minus hugetlb pages, scaled by the ratio percentage, with every swap page then added on top."
- Source S499 `util.c.v7.2:911-913` (quote): `allowed = ((totalram_pages() - hugetlb_total_pages()) * sysctl_overcommit_ratio / 100); allowed += total_swap_pages;`
- Context (`util.c.v7.2:901-916`): the enclosing function `vm_commit_limit()`, whose comment (lines 901-903) reads "Committed memory limit enforced when OVERCOMMIT_NEVER policy is used"; the branch structure: when `sysctl_overcommit_kbytes` is nonzero (line 908-909) the kbytes term replaces this whole formula, otherwise the quoted formula runs; the entry's own text (S494 linkage) states the meminfo line `CommitLimit` is printed from `vm_commit_limit()`.
- Judgment: entailed. "RAM minus hugetlb pages" = `totalram_pages() - hugetlb_total_pages()`; "scaled by the ratio percentage" = `* sysctl_overcommit_ratio / 100`; "every swap page then added on top" = `allowed += total_swap_pages`. The naming "CommitLimit" is supported by the function comment and the entry's meminfo linkage; the quote is the exact body of the else-branch of the limit computation.
- Over-read risk: the formula is the else-branch (run when `sysctl_overcommit_kbytes` is zero); a careless reader could over-read the claim as the unconditional definition of CommitLimit. The claim does not state "always" or "unconditionally", so it does not overreach; the kbytes replacement is a separate row (15).

## Method notes
- Quotes located with `grep -n` on the committed copies: row 8 at `vm.rst.v7.2:841`, row 9 at `:844`, row 10 at `:864`, row 11 at `:831-833`, row 12 at `:1032-1033`, row 13 at `:92-93`, row 14 at `util.c.v7.2:911-913`. Context read ~20 lines around each.
- No REPLACE lines: no row 8–14 claim was judged an overclaim, so no replacement proposal is made.
- No ENTAIL lines for rows outside 8–14.

## Findings
- MED: row 13 claim omits the quote's "under the default overcommit 'guess' mode" condition and adds "when memory runs short"; judged a faithful restatement (context lines 95-97 support the recovery scenario), but it is the closest of the seven to the overclaim line — a strict reader could insist on the guess-mode condition. Not enough to vote overclaim; routed as a watch item for round 53 if the L1 wants the mode 2 ambiguity closed.
- LOW: row 14 claim names the formula result "CommitLimit" based on the entry's meminfo linkage (S494, `fs/proc/meminfo.c:125-126`) rather than on the S499 quote itself; the quote is the function body, so the mapping is sound, but the evidence chain crosses rows.
- LOW: row 11's "can simply mean" hedge depends on the doc's wording "which then appears as 0 when read"; if a future reader takes a 0 ratio as proof of the kbytes knob, that is over-reading, not a claim defect.
