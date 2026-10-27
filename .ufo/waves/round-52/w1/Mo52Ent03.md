# Mo52Ent03 — round 52 wave w1 — entailment report, rows 1–7

Seat: Mo52Ent03 (ENTAILMENT voter). Contract: `.ufo/waves/round-52/contract.md` (frozen, L1 MoriR52).
Judged at data commit `8524904adb25e44f24d9f25aac7eae909625c18c`; entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`.
Entry: `corpus/knowledge/overcommit-commit-limit-r52.md`. All seven rows assigned to me cite S497
(`Documentation/mm/overcommit-accounting.rst` at tag v7.2), committed copy
`corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2` (85 lines).

## Method and verification actually performed

- For each row: located the row's quote in the committed S497 copy (line numbers below), read the surrounding
  context — the file is 85 lines, so each quote's full section (well over 20 lines around) was read — and judged
  whether the claim cell follows from the quote plus that context.
- Working tree vs data commit: `git diff --stat 8524904adb…  -- corpus/evidence/sources-r52/ corpus/knowledge/overcommit-commit-limit-r52.md`
  → empty, exit 0. The bytes I judged are the committed bytes.
- Upstream byte-identity: `curl -fsSL …/v7.2/Documentation/mm/overcommit-accounting.rst | sha256sum` →
  `767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f`, identical to the committed copy and to the
  sha the entry's `recheck:` line records. The quotes are real v7.2 bytes, not doctored copies.
- Row hashes recomputed from the entry's table cells (not retyped) with the frozen formula
  (`sha256` of the claim cell, whitespace collapsed, ends stripped, first 12 hex): all seven match
  `evidence/c2-hashes-at-data.txt`.
- Vote grammar read from the frozen counter before voting:

```
ENTAIL_RE   = ^\s*ENTAIL\s+([0-9a-f]{12})\s+(entailed|overclaim)\b   (count-c2.py:124)
REPLACE_RE  = ^\s*REPLACE\s+([0-9a-f]{12})\s+::\s+(.+?)\s*$          (count-c2.py:125)
```

  My verdict lines below are unfenced and match that grammar; no verdict line appears inside a fenced block.
- LSP: no `lsp` device is mounted in this session and no language server answers for `.rst`/`.md` kernel-doc
  bytes, so all quote/definition checks are committed-text reads of `git show` output. Recorded as the fallback
  the seat rules allow; no semantic (LSP) proof is claimed anywhere below.
- Scratch: `/fast/scratch/hyaku/mori-r52/Mo52Ent03/` (created, `TMPDIR` under it, removed at end of session).
  Disk guard before starting: `/fast/scratch/hyaku` at 24 %, 614.3 G free — no ENOSPC risk. No tool installed or
  upgraded (none needed); no pacman call. No file written anywhere in the lane except this report.

## Per-row judgments

### Row 1 — `9afaa81505da` — entailed
Claim: "Mode 0 is the default and refuses only allocations that are plainly too large, so it still lets the host
overcommit."
Quote at `corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2:8-9`, inside the mode-0 block (lines 7–11):
"Heuristic overcommit handling. Obvious overcommits of address space are refused. Used for a typical system.
It ensures a seriously wild allocation fails while allowing overcommit to reduce swap usage. This is the default."
"Mode 0 is the default" ← "This is the default." (line 11). "refuses only allocations that are plainly too large"
← "Obvious overcommits … are refused" plus "a seriously wild allocation fails"; the exclusivity is the doc's own
contrast — refusals are the obvious/wild cases, everything else is "allowing overcommit" (line 10). "still lets
the host overcommit" ← "while allowing overcommit to reduce swap usage". Follows.
Careless over-read: "It ensures a seriously wild allocation fails" is a single-instance guarantee ("a"), not a
promise that every wild allocation fails; and "Used for a typical system" is a description, not a recommendation
to stay in mode 0. A reader could also take "only" as the doc's literal word — it is an inference, though the
doc's contrast supports it.

### Row 2 — `61b7677d56fe` — entailed
Claim: "Only under mode 2 is the committed total capped, at swap plus a share of RAM that defaults to one half."
Quote at lines 20–22, the body of mode 2 ("Don't overcommit."): "The total address space commit for the system is
not permitted to exceed swap + a configurable amount (default is 50%) of physical RAM." Context lines 19–35:
mode 1 is "Always overcommit" (no cap, by name and body); mode 0's rule is per-request ("Obvious overcommits …
are refused") with overcommit allowed — no total cap stated; and lines 33–35 put the cap's knobs under mode 2
only: "These only have an effect when ``vm.overcommit_memory`` is set to 2." "defaults to one half" ← "(default
is 50%)". Follows from quote + context.
Careless over-read: the cap sentence lives under mode 2's heading only; a reader skimming could apply swap+50 % to
every mode, or read "configurable amount" as necessarily a percentage (the same doc also offers
`vm.overcommit_kbytes`, line 34). The claim correctly binds both the cap and its default to mode 2.

### Row 3 — `93b4fe285dc7` — overclaim
Claim: "Under mode 2 the documented failure is an allocation error at request time rather than a kill when pages
are later touched."
Quote at lines 22–25: "in most situations this means a process will not be killed while accessing pages but will
receive errors on memory allocation as appropriate." The claim asserts the failure mode unconditionally; the
source states it only "in most situations", conditioned on "Depending on the amount you use" (lines 22–23) and
qualified by "as appropriate" (line 25). Dropping those hedges states a scope the source does not state — a kill
on later page access is not ruled out by the doc, and the doc's own Gotchas section (lines 43–46, stack growth /
mremap "if you want absolute guarantees … you MUST mmap your stack") shows a concrete case where the allocation-
time guarantee needs care. Under the frozen strictness rule this is an overclaim; the failure-mode direction
(errors at allocation, not kills at touch) is right, the universality is not.
Careless over-read: everything after "Depending on the amount you use" — the hedges are easy to drop when
summarizing; a reader of the claim alone would conclude mode 2 processes are never killed for touching pages,
which the doc explicitly does not promise.
Replacement (≥ 6 words; non-quote words of ≥ 3 letters include: documentation, says, under, mode, typically,
instead, being; hash of the replacement text is `e5f3003852f6` — informational, I cast no vote on it): the
single REPLACE line for this row sits in the Votes section below.

### Row 4 — `3b02f6680556` — entailed
Claim: "The documentation says the current limit and the committed amount are both published by the kernel for
reading, as two meminfo lines."
Quote at line 37, sentence completing on line 38: "The current overcommit limit and amount committed are viewable
in ``/proc/meminfo`` as CommitLimit and Committed_AS respectively." "the documentation says" ✓ (this is the doc's
statement); "both … for reading" ← "viewable in"; "as two meminfo lines" ← the two named `/proc/meminfo` entries;
"published by the kernel" is what "viewable in `/proc/meminfo`" means (procfs is kernel-exported), so the claim
adds no consequence the source lacks. Follows.
Careless over-read: "viewable" says nothing about the values' accuracy or update granularity — the doc claims
visibility, not exactness; and the table's quote cell stops mid-sentence at "viewable in", so a reader of only
the quoted fragment never sees the `/proc/meminfo` destination (see Findings, LOW).

### Row 5 — `921c2e511e09` — entailed
Claim: "Under mode 2 a mapping request carrying MAP_NORESERVE is still charged against the commit limit."
Quote at line 48 (Gotchas): "In mode 2 the MAP_NORESERVE flag is ignored." Context: the mode-2 rule (lines 19–25)
caps the total commit, and the accounting rules (lines 51–67) assign every map a cost. If the flag is ignored,
the request is processed as though it were absent, so the ordinary cost applies and the mode-2 cap check runs —
i.e. the mapping is charged against the commit limit. "Charged against the commit limit" is the doc's
"not permitted to exceed" plus "0 cost / size of mapping" accounting expressed in the claim's words; the
inference is direct, and the entry's own S501 rows corroborate it. Follows.
Careless over-read: "ignored" is scoped to mode 2 — the same doc's mode-0/1 behavior differs (S501 row 25
material); and "ignored" must not be read as "the mapping is free" — ignoring the flag is exactly what makes the
mapping chargeable.

### Row 6 — `e37e65e64a4c` — entailed
Claim: "Shared and read-only file mappings add nothing to the committed total, because the file itself backs
those pages."
Quote at line 57, first row of the file-backed table (lines 56–58): "SHARED or READ-only - 0 cost (the file is
the map not swap)". "add nothing to the committed total" ← "0 cost" under "How It Works … The overcommit is based
on the following rules" (lines 51–54), i.e. the overcommit accounting; "because the file itself backs those
pages" ← "(the file is the map not swap)". The claim correctly scopes to *file* mappings. Follows.
Careless over-read: the 0-cost row is file-backed only — the anonymous table (lines 60–63) charges anonymous
SHARED at "size of mapping"; a reader who generalizes "shared costs 0" to anonymous shared memory (or to shmfs,
which line 67 says is "drawn from the same pool") over-reads. "READ-only" here covers read-only file maps of
either sharing kind; PRIVATE WRITABLE file maps are charged per instance (line 58).

### Row 7 — `7b2fc298698e` — entailed
Claim: "The documentation still lists ptrace pages as unaccounted, so the committed total is not a complete
ledger of every commitment."
Quote at lines 83–85, the file's closing section: "To Do ===== * Account ptrace pages (this is hard)".
A To Do item to "account" pages states those pages are not yet accounted, so the doc still lists ptrace pages as
unaccounted at v7.2 ("still" is fair — the section survives in the tagged bytes I hashed). Given the doc's own
framing ("Overcommit Accounting", "How It Works"), an unaccounted class of pages means the committed total is not
a complete ledger of every commitment. Follows.
Careless over-read: the To Do shows a hole exists, not that ptrace is the only hole (the doc never says "only" —
the entry's Boundaries section adds the hugetlb/MAP_NORESERVE case from S501 separately, which is consistent);
and "(this is hard)" comments implementation difficulty, not doubt that the pages are commitments.

## Votes

One verdict line per assigned row (rows 1–7), unfenced, hashes verified against
`evidence/c2-hashes-at-data.txt`. No vote on any other row; no vote on my own replacement text (the counter
ignores an author's vote; two other ENTAILMENT seats must judge the replacement's new hash).

ENTAIL 9afaa81505da entailed
ENTAIL 61b7677d56fe entailed
ENTAIL 93b4fe285dc7 overclaim — the claim's unconditional "the documented failure is an allocation error at request time rather than a kill when pages are later touched" drops the source's "in most situations", "Depending on the amount you use" and "as appropriate", asserting a scope (never a kill on later touch) the doc does not state
ENTAIL 3b02f6680556 entailed
ENTAIL 921c2e511e09 entailed
ENTAIL e37e65e64a4c entailed
ENTAIL 7b2fc298698e entailed

REPLACE 93b4fe285dc7 :: The documentation says that under mode 2 a process typically receives errors on memory allocation instead of being killed while accessing pages.

## Named limits observed (for the report, no counter change proposed)

- The arm proves two ENTAILMENT seats recorded a judgment; it cannot prove the judgment right (contract's own
  named limit). My row-5 and row-6 verdicts rest on one-step inferences ("ignored" → charged; "0 cost" → not
  added to the committed total); both are direct, but a future entry could quote the accounting rules line too.
- The claim hash covers the claim cell only; the quote cell is locational. A quote cell could drift from the
  source without changing any hash — the `located`/`quote_missing` arm is what guards that, and it passed at
  data (`located=28 quote_missing=0`, `evidence/c2-at-data.txt`).
- v7.2 bytes say nothing about this host's sysctl values or other kernels (contract named limit); none of my
  verdicts relies on a host read.

## Findings

- MED — `corpus/knowledge/overcommit-commit-limit-r52.md`, `## Claims` row 3 (hash `93b4fe285dc7`): overclaim —
  the claim cell asserts the mode-2 failure mode unconditionally while S497 (`overcommit-accounting.rst.v7.2:22-25`,
  corroborated by the Gotchas stack caveat at `:43-46`) states it only "in most situations … as appropriate".
  Vote recorded above; replacement text proposed via the REPLACE line above (needs two non-author `entailed`
  votes on its new hash after the L1 lands it).
- LOW — `corpus/knowledge/overcommit-commit-limit-r52.md`, `## Claims` row 4 quote cell: the quotation is
  truncated mid-sentence ("The current overcommit limit and amount committed are viewable in"), so the cell
  alone never names `/proc/meminfo` (the completion is `overcommit-accounting.rst.v7.2:38`). The locator arm
  still matches it (`quote_missing=0` at data), so this is wording polish for the L1 — the data commit's claim
  hash would be unaffected since only the quote cell would change. No counter change proposed.
- LOW — row 1's "refuses only allocations that are plainly too large": the word "only" is an inference from the
  doc's contrast ("… while allowing overcommit …", `overcommit-accounting.rst.v7.2:8-11`), not a doc quotation.
  I judged it entailed because the contrast is the doc's own, but a stricter paraphrase quoting "a seriously wild
  allocation fails" would be unimpeachable. Data-wording observation only.
- Verification gaps: rows 8–28 were not assigned to this seat and are not judged here; upstream byte-identity
  was checked for S497 only (the sole source rows 1–7 cite); no LSP server was available for any file judged,
  so all checks are committed-text reads. Scratch removed; nothing written in the lane except this report.

## Vote on the landed row-3 replacement (3c2512af8468)

The L1 replaced row 3 with: "The documentation says that under mode 2, in most situations, a process receives
errors on memory allocation instead of being killed while touching pages." (hash recomputed: `3c2512af8468`;
text present as the row-3 claim cell in `corpus/knowledge/overcommit-commit-limit-r52.md:27`, same quote cell).
Judged against S497 (`overcommit-accounting.rst.v7.2:19-25`): "under mode 2" is the sentence's own block;
"in most situations" restores the source's load-bearing hedge verbatim; "receives errors on memory allocation"
and "instead of being killed while touching pages" paraphrase "will receive errors on memory allocation" /
"will not be killed while accessing pages" without adding scope, consequence or number. The dropped tail
qualifier "as appropriate" conditions how errors are issued, not the claim's scope; "Depending on the amount
you use" is folded into the retained "in most situations". Follows. I did not write this text (my REPLACE line
above hashes to `e5f3003852f6`, a different text), so this vote is not an author's vote. This re-judgment used
no scratch (text judgment plus one hash computation in the shell).

ENTAIL 3c2512af8468 entailed
