# Mo52Ent02 — ENTAILMENT report (rows 1–7, ## Claims)

Seat: Mo52Ent02 (entailment voter). Item: judge claim rows 1–7 of the `## Claims` table of
`corpus/knowledge/overcommit-commit-limit-r52.md` at `8524904adb25e44f24d9f25aac7eae909625c18c`.
All seven rows quote S497 (`corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2`); I verified
`git diff --quiet 8524904a -- corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2` → IDENTICAL
(working-tree copy equals the committed copy). Line numbers below refer to that file (the committed copy).

## Hash check

Recomputed with `python3 -c 'import hashlib,re,sys;print(hashlib.sha256(re.sub(r"\s+"," ",sys.argv[1]).strip().encode()).hexdigest()[:12])' "<claim text>"` from the claim text parsed out of the committed markdown (`git show 8524904a:corpus/knowledge/overcommit-commit-limit-r52.md`), compared against `evidence/c2-hashes-at-data.txt`:

- row 1 `9afaa81505da` MATCH
- row 2 `61b7677d56fe` MATCH
- row 3 `93b4fe285dc7` MATCH
- row 4 `3b02f6680556` MATCH
- row 5 `921c2e511e09` MATCH
- row 6 `e37e65e64a4c` MATCH
- row 7 `7b2fc298698e` MATCH

## Verdicts

ENTAIL 9afaa81505da entailed
ENTAIL 61b7677d56fe entailed
ENTAIL 93b4fe285dc7 entailed
ENTAIL 3b02f6680556 entailed
ENTAIL 921c2e511e09 entailed
ENTAIL e37e65e64a4c entailed
ENTAIL 7b2fc298698e entailed
ENTAIL 3c2512af8468 entailed

## Per-row reasoning and careless over-read warnings

### row 1 — `9afaa81505da` (Mode 0 …)
Quote at lines 8–11: "Heuristic overcommit handling. Obvious overcommits of address space are refused. Used for a typical system. It ensures a seriously wild allocation fails while allowing overcommit to reduce swap usage. This is the default."
- "Mode 0 is the default" ← "This is the default." (line 11); "refuses only allocations that are plainly too large" ← "Obvious overcommits … are refused" + "a seriously wild allocation fails" (lines 8–10); "still lets the host overcommit" ← "while allowing overcommit to reduce swap usage" (line 10).
- Verdict: entailed.
- Careless over-read: "only" is an inference from "while allowing overcommit"; a reader could over-read "plainly too large" as a precise algorithmic criterion instead of the heuristic the document describes (mode 0 is named "Heuristic").

### row 2 — `61b7677d56fe` (Only under mode 2 …)
Quote at lines 20–22: "The total address space commit for the system is not permitted to exceed swap + a configurable amount (default is 50%) of physical RAM."
- "at swap plus a share of RAM that defaults to one half" ← the quote verbatim ("swap + a configurable amount (default is 50%) of physical RAM"). "Only under mode 2" ← document structure: mode 0 (lines 7–11) and mode 1 (lines 13–17) state no cap; mode 2 (lines 19–25) is the only block with a total limit, and lines 33–35 add the ratio/kbytes knobs "only have an effect when vm.overcommit_memory is set to 2".
- Verdict: entailed.
- Careless over-read: "a share of RAM that defaults to one half" could be over-read as always 50% (it is configurable); "swap + a share" could be over-read as applying in every mode.

### row 3 — `93b4fe285dc7` (Under mode 2 the documented failure …)
Quote at lines 23–25: "in most situations this means a process will not be killed while accessing pages but will receive errors on memory allocation as appropriate."
- "an allocation error at request time rather than a kill when pages are later touched" is a faithful rendering of "will receive errors on memory allocation as appropriate" vs "will not be killed while accessing pages"; the mode-2 block (lines 22–29) frames this as the mode's failure behavior ("Useful for applications that want to guarantee their memory allocations will be available in the future without having to initialize every page").
- Verdict: entailed.
- Careless over-read: the hedge "in most situations" is dropped — a reader could read error-at-allocation as unconditional; "allocation error at request time" could be over-read as a specific errno at the mmap syscall, which the document does not state.

### row 4 — `3b02f6680556` (The documentation says …)
Quote at lines 37–38: "The current overcommit limit and amount committed are viewable in /proc/meminfo as CommitLimit and Committed_AS respectively."
- "both published by the kernel for reading, as two meminfo lines" ← "viewable in /proc/meminfo as CommitLimit and Committed_AS respectively"; the claim correctly frames this as what the documentation says.
- Verdict: entailed.
- Careless over-read: "published … for reading" could be over-read as a promise the values are always live/current (the document only says they are viewable), or as enforcement data (they are the ledger, not the enforcement).

### row 5 — `921c2e511e09` (Under mode 2 … MAP_NORESERVE …)
Quote at line 48: "In mode 2 the MAP_NORESERVE flag is ignored."
- Within the document's accounting framework — "How It Works" (lines 56–67) accounts mappings, with MAP_NORESERVE the standard no-reserve exemption — "ignored" means the exempting effect is disregarded, so the mapping is still charged against the commit limit.
- Verdict: entailed.
- Careless over-read: extending the statement to hugetlb file mappings with MAP_NORESERVE, which S501 carves out (entry Boundaries note: they stay uncharged even under mode 2) — that carve-out is outside this quote's source and does not contradict what S497 says about ordinary mappings; "ignored" could also be over-read as the flag being unparsed rather than overridden.

### row 6 — `e37e65e64a4c` (Shared and read-only file mappings …)
Quote at line 57: "SHARED or READ-only - 0 cost (the file is the map not swap)"
- "add nothing to the committed total" ← "0 cost"; "because the file itself backs those pages" ← "(the file is the map not swap)"; the row sits under "For a file backed map" (line 56).
- Verdict: entailed.
- Careless over-read: extending "0 cost" to every mapping (line 58: PRIVATE WRITABLE costs "size of mapping per instance"; anonymous PRIVATE READ-only is also 0 cost but "of little use"), or reading "0 cost" as zero memory usage rather than zero commit accounting.

### row 7 — `7b2fc298698e` (The documentation still lists ptrace pages …)
Quote at lines 83–85, To Do list: "Account ptrace pages (this is hard)"
- A To Do item is not-done work, so ptrace pages are unaccounted at v7.2; "so the committed total is not a complete ledger of every commitment" follows from that gap. "still lists" is anchored to the v7.2 bytes.
- Verdict: entailed.
- Careless over-read: reading "To Do" as a promise for a future version, or as proof ptrace pages are never charged anywhere; "not a complete ledger of every commitment" is an inference from the single listed gap.

## Verification evidence

- Source copy check: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --quiet 8524904adb25e44f24d9f25aac7eae909625c18c -- corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2` → exit 0 (IDENTICAL).
- Hash recomputation: five hashes recomputed from the committed claim text via the specified `python3 -c …` one-liner; all seven MATCH the `evidence/c2-hashes-at-data.txt` rows (script output above).
- Working-tree copy read with `cat -n` (same bytes as `git show 8524904a:…`).

## Findings

- MED — Row 1 (`9afaa81505da`): "refuses only allocations that are plainly too large" uses "only" which is inferred from "while allowing overcommit to reduce swap usage" (line 10), not stated literally; still entailed because the mode-0 block (lines 7–11) names no other refusal. File: corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2:7-11.
- MED — Row 3 (`93b4fe285dc7`): the claim drops the source hedge "in most situations" (line 23); the claim's "the documented failure is …" keeps it descriptive, so entailed, but the hedge loss is a scope-narrowing a strict reader should notice. File: corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2:22-25.
- MED — Row 5 (`921c2e511e09`): "still charged against the commit limit" is a consequence not literally printed (line 48 only says the flag "is ignored"); it follows from the document's accounting framework, but the hugetlb carve-out in S501 (entry Boundaries) means the universal phrasing does not cover hugetlb file mappings. File: corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2:48.
- LOW — Rows 2, 4, 6, 7: claims are near-verbatim restatements of the quoted lines; over-read risk is limited to generalization beyond the quoted scope (all modes, all mappings, future versions).
