# Mo52Ent04 — ENTAILMENT vote, round 52 w1

Seat: Mo52Ent04. Item: ENTAILMENT. Rows judged: 8–14 of the `## Claims` table in
`corpus/knowledge/overcommit-commit-limit-r52.md` at
8524904adb25e44f24d9f25aac7eae909625c18c (read via `git -C … show 8524904…:corpus/knowledge/overcommit-commit-limit-r52.md`).

Hashes: recomputed for all seven rows as
`sha256(re.sub(r"\s+"," ",claim).strip().encode()).hexdigest()[:12]` from the git-show bytes, and every one
MATCHes `.ufo/waves/round-52/evidence/c2-hashes-at-data.txt`. No row's text was written by this seat.

## Votes

ENTAIL 43cf2a78acdd entailed
ENTAIL 35d642f1d0d9 entailed
ENTAIL fcd0e7a78872 entailed
ENTAIL 5c40f6fa5c62 entailed
ENTAIL 00e2a9db523b entailed
ENTAIL bfb15534fa5e entailed
ENTAIL 28d3042fded0 entailed
ENTAIL 3c2512af8468 entailed

No overclaim found, so no REPLACE lines. Per-row evidence, judgment and over-read notes:

## Row 8 (43cf2a78acdd) — S498

- Claim: “In mode 0 a single request is compared with all RAM plus all swap, not with what is currently free.”
- Quote located in the committed copy `corpus/evidence/sources-r52/vm.rst.v7.2` lines 841–842:
  “When this flag is 0, the kernel compares the userspace memory request size against total memory plus swap
  and rejects obvious overcommits.” Context read: lines 824–873 (overcommit_kbytes, overcommit_memory,
  overcommit_ratio sections; mode 2 at 847–848, default 0 at 855).
- Judgment: entailed. “all RAM plus all swap” = “total memory plus swap”; “a single request” = “the userspace
  memory request size”. “not with what is currently free” is entailed by the comparative being the *total*:
  comparing against total memory plus swap is not comparing against the free amount. “In mode 0” matches “When
  this flag is 0”.
- Over-read risk: a careless reader could take “rejects obvious overcommits” as a vague heuristic rather than
  the exact total-RAM+swap comparison, or could assume the request is compared with *currently free* memory. The
  claim pins the comparison basis correctly.

## Row 9 (35d642f1d0d9) — S498

- Claim: “Mode 1 never refuses an allocation on commit grounds; the kernel behaves as though memory were unlimited
  until it is exhausted.”
- Quote located at `vm.rst.v7.2` lines 844–845: “When this flag is 1, the kernel pretends there is always enough
  memory until it actually runs out.” Context read: lines 824–873.
- Judgment: entailed. “pretends there is always enough memory” is exactly refusing nothing on commit grounds (the
  commit check is skipped); “until it actually runs out” = “until it is exhausted”. The “on commit grounds” scope
  is faithful — the source describes the overcommit-side behavior only.
- Over-read risk: a careless reader could drop “on commit grounds” and conclude mode 1 refuses nothing, ever
  (other refusals — address-space limits, cgroup limits, actual allocation failure — are not covered by this
  source). The claim keeps the qualifier.

## Row 10 (fcd0e7a78872) — S498

- Claim: “The ratio setting is a percentage cap on physical RAM that applies only in mode 2, with swap added on
  top.”
- Quote located at `vm.rst.v7.2` lines 864–866: “When overcommit_memory is set to 2, the committed address space
  is not permitted to exceed swap plus this percentage of physical RAM. See above.” Context read: lines 824–873
  (overcommit_kbytes note at 831–833; mode 0/1 at 841–845; mode 2 “never overcommit” at 847–848; default 0 at
  855).
- Judgment: entailed. “percentage cap on physical RAM” = “this percentage of physical RAM”; “with swap added on
  top” = “not permitted to exceed swap plus …”; “applies only in mode 2” follows from the rule being stated only
  for “When overcommit_memory is set to 2” and from the mode-0/1 descriptions in the same section defining
  different behaviors with no ratio involvement (and, in S499, the ratio term is consumed only inside
  `vm_commit_limit()`, the mode-2 enforcement path).
- Over-read risk: a careless reader could think the ratio caps the commit limit in every mode, or that the
  percentage cap applies to swap (it caps physical RAM; swap is added on top). The claim states both bounds.

## Row 11 (5c40f6fa5c62) — S498

- Claim: “The kbytes and ratio knobs are mutually exclusive, so a ratio that reads 0 can simply mean the kbytes
  knob is in force.”
- Quote located at `vm.rst.v7.2` lines 831–833: “Note: overcommit_kbytes is the counterpart of overcommit_ratio.
  Only one of them may be specified at a time. Setting one disables the other (which then appears as 0 when
  read).” Context read: lines 824–873.
- Judgment: entailed. “mutually exclusive” = “Only one of them may be specified at a time”; “a ratio that reads 0
  can simply mean the kbytes knob is in force” = “Setting one disables the other (which then appears as 0 when
  read)”, with the claim’s “can simply mean” preserving the hedge.
- Over-read risk: a careless reader could invert the implication and decide a ratio reading 0 *always* means the
  kbytes knob is in force (the source states the mechanism but not an exhaustive cause); or could misread
  “Setting one disables the other” as a transient state rather than a persistent write effect. The claim’s “can
  simply mean” is exactly the right strength.

## Row 12 (00e2a9db523b) — S498

- Claim: “Mode 2 also holds back a user reserve sized from the requesting process and capped by the
  user_reserve_kbytes knob.”
- Quote located at `vm.rst.v7.2` lines 1032–1033: “When overcommit_memory is set to 2, "never overcommit" mode,
  reserve min(3% of current process size, user_reserve_kbytes) of free memory.” Context read: lines 1019–1053
  (intent at 1034–1035; “no effect when overcommit_memory is set to 0 or 1” at 1037; default note at 1039).
- Judgment: entailed. “holds back a user reserve” = “reserve … of free memory”; “sized from the requesting
  process” = “3% of current process size” (the process making the request); “capped by the user_reserve_kbytes
  knob” = `min(…, user_reserve_kbytes)`. “Mode 2” matches the conditional and the explicit 1037 scope line.
- Over-read risk: a careless reader could read the reserve as a percentage of *free memory* (it is `min(3% of
  current process size, user_reserve_kbytes)`), or as applying under modes 0/1 (line 1037 says it has no effect
  there). The claim states both correctly.

## Row 13 (bfb15534fa5e) — S498

- Claim: “The admin reserve exists so that root can still log in and kill a runaway process when memory runs
  short.”
- Quote located at `vm.rst.v7.2` lines 92–93: “That should provide enough for the admin to log in and kill a
  process, if necessary, under the default overcommit 'guess' mode.” Context read: lines 79–113 (reserve
  definition at 87–88; default at 90; the 'never'-mode warning at 95–97; guidance at 99–108).
- Judgment: entailed. The purpose clause “so that root can still log in and kill …” is the source’s own
  “provide enough for the admin to log in and kill a process”; “when memory runs short” tracks “if necessary”
  plus the recovery context (lines 95–97: otherwise root may not be able to log in to recover the system).
  “runaway” is a color word for the process killed in that recovery scenario (the source’s sibling user-reserve
  section calls it “a single memory hogging process … (kill the hog)”, lines 1034–1035); it adds no factual
  scope.
- Over-read risk: a careless reader could read the reserve as *guaranteeing* login/kill under every mode — the
  source warns that under 'never' overcommit the default reserve may be insufficient and should be increased
  (lines 95–97). Also, the source’s sentence is explicitly about the 'guess' mode; the claim generalizes the
  *purpose* (“when memory runs short”), which the surrounding text supports for recovery generally.

## Row 14 (28d3042fded0) — S499

- Claim: “CommitLimit is RAM minus hugetlb pages, scaled by the ratio percentage, with every swap page then added
  on top.”
- Quote located in the committed copy `corpus/evidence/sources-r52/util.c.v7.2` lines 911–913:
  `allowed = ((totalram_pages() - hugetlb_total_pages()) * sysctl_overcommit_ratio / 100);` then
  `allowed += total_swap_pages;` Context read: lines 894–933 (function comment “Committed memory limit enforced
  when OVERCOMMIT_NEVER policy is used” at 901–903; the kbytes branch at 908–909; `return allowed;` at 915).
- Judgment: entailed. Every term maps exactly: “RAM minus hugetlb pages” = `totalram_pages() - hugetlb_total_pages()`;
  “scaled by the ratio percentage” = `* sysctl_overcommit_ratio / 100`; “every swap page then added on top” =
  `allowed += total_swap_pages`. The function `vm_commit_limit()` returning `allowed` is what the meminfo
  `CommitLimit` line prints (per the entry’s own preamble), and its comment confirms it is the commit limit.
- Over-read risk: a careless reader could read this as the unconditional formula for the limit — but lines
  908–909 show that when `sysctl_overcommit_kbytes` is nonzero the ratio branch is skipped entirely, and the
  limit is enforced only under mode 2. The claim describes the ratio path itself, which is accurate.

## Method notes

- All quotes were located verbatim in the committed copies under `corpus/evidence/sources-r52/` (grep line
  numbers above) and read with ~20 lines of context (five `read` ranges: `vm.rst.v7.2:824-873`,
  `vm.rst.v7.2:1019-1053`, `vm.rst.v7.2:79-113`, `util.c.v7.2:894-933`).
- No tools were installed; no scratch files were cited (scratch used only for the hash-recompute script
  fragment, which wrote nothing to disk). Host reads only; nothing mutated.

## Findings

- LOW — rows 8–14 all entailed; seven ENTAIL lines above, each backed by a located quote + context. Concern:
  `corpus/knowledge/overcommit-commit-limit-r52.md` Claims table, rows 8–14.
- LOW — row 10 “applies only in mode 2” is entailed by the source’s conditional framing and by the mode-0/1
  descriptions in the same section, but the exclusivity word is an inference, not literal text; suitably scoped.
- LOW — row 13 “runaway” is a color word beyond the source’s “a process”; judged entailed because it adds no
  factual scope (the source’s sibling section describes the same kill-the-hog scenario). Note for the L1 only;
  no replacement proposed.
