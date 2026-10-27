# Mo52Ent01 — round-52 w1 — ENTAILMENT votes, claim rows 1–7 (S497, overcommit-accounting.rst at v7.2)

Seat Mo52Ent01, one of the twelve ENTAILMENT voters. Scope: claim rows 1–7 of the `## Claims` table of
`corpus/knowledge/overcommit-commit-limit-r52.md` at the data commit `8524904adb25e44f24d9f25aac7eae909625c18c`
(entry lines 25–31 at that commit), all seven rows sourced S497 = `Documentation/mm/overcommit-accounting.rst`
at tag v7.2, committed copy `corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2`.

## Method and provenance (commands, output, exit codes)

Run from my scratch (`/fast/scratch/hyaku/mori-r52/Mo52Ent01`, `TMPDIR=…/tmp`); all reads absolute:

1. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8524904adb25e44f24d9f25aac7eae909625c18c:corpus/knowledge/overcommit-commit-limit-r52.md > entry-at-data.md` — rc 0 (75 lines). Judged the data-commit bytes.
2. `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2` — rc 0: `767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f`, equal to the first recheck hash recorded in the entry at R. The copy I judged is the bytes the entry pins.
3. Row-hash recompute with the seat-spec one-liner (`hashlib.sha256(re.sub(r"\s+"," ",claim).strip().encode()).hexdigest()[:12]`) over each of the seven claim cells extracted from the data-commit entry — rc 0: 7/7 match `.ufo/waves/round-52/evidence/c2-hashes-at-data.txt` (`9afaa81505da`, `61b7677d56fe`, `93b4fe285dc7`, `3b02f6680556`, `921c2e511e09`, `e37e65e64a4c`, `7b2fc298698e`).
4. Drift check `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat 8524904adb25e44f24d9f25aac7eae909625c18c -- corpus/knowledge/overcommit-commit-limit-r52.md corpus/evidence/sources-r52/` — rc 0, empty diff: the working-tree entry and S497 copy equal the data-commit bytes I judged.

I read the S497 copy in full (85 lines), so every row was judged with well over 20 lines of surrounding context. Quote line numbers below are lines of `corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2`; the quotes match verbatim once the document's line wraps are joined.

## Per-row judgment

### Row 1 — `9afaa81505da` — quote at S497 copy lines 8–11

```
0
	Heuristic overcommit handling. Obvious overcommits of address
	space are refused. Used for a typical system. It ensures a
	seriously wild allocation fails while allowing overcommit to
	reduce swap usage. This is the default.
```

Verdict: entailed. "This is the default" (line 11) grounds "Mode 0 is the default". "Obvious overcommits of address space are refused" plus "allowing overcommit to reduce swap usage" (lines 8–10) ground both "refuses only allocations that are plainly too large" (refusal is tied to obvious/wild overcommits) and "so it still lets the host overcommit". Nothing in the mode-0 passage or the rest of the file names any other mode-0 refusal condition, and lines 29–32 confirm the commit-limit knobs have no effect outside mode 2.

What a careless reader might over-read: "Used for a typical system" is a use note, not a recommendation or a guarantee; and "It ensures a seriously wild allocation fails" covers a single wild request failing — it does not promise the host never OOM-kills under mode 0. The claim's "plainly too large" is a fair gloss of "obvious overcommits"/"seriously wild", not a size threshold.

### Row 2 — `61b7677d56fe` — quote at S497 copy lines 20–22

```
2
	Don't overcommit. The total address space commit for the
	system is not permitted to exceed swap + a configurable amount
	(default is 50%) of physical RAM.  Depending on the amount you
	use, in most situations this means a process will not be
	killed while accessing pages but will receive errors on memory
	allocation as appropriate.
```

Verdict: entailed. The cap sentence sits under the mode-2 heading (line 19). "Only under mode 2" is supported by context: mode 1 is "Always overcommit" (lines 13–17), mode 0 is heuristic (lines 7–11), and lines 29–32 say the amount knobs "only have an effect when `vm.overcommit_memory` is set to 2". "At swap plus a share of RAM that defaults to one half" is "swap + a configurable amount (default is 50%) of physical RAM" nearly verbatim.

What a careless reader might over-read: the 50% is a default, not a constant — the share is configurable via `vm.overcommit_ratio` or `vm.overcommit_kbytes` (lines 29–31); and the cap is swap plus the amount, not the amount alone. The claim cell already says "defaults to", so no text change is needed.

### Row 3 — `93b4fe285dc7` — quote at S497 copy lines 22–25 — OVERCLAIM

```
	(default is 50%) of physical RAM.  Depending on the amount you
	use, in most situations this means a process will not be
	killed while accessing pages but will receive errors on memory
	allocation as appropriate.
```

Verdict: overclaim. The exact words beyond the source: the claim asserts, for mode 2 as such, "the documented failure is an allocation error at request time rather than a kill when pages are later touched", while the source scopes the error-not-kill outcome twice — "Depending on the amount you use" and "in most situations" (lines 22–23). Dropping both hedges converts the documented typical outcome into an unconditional contract, a scope the source does not state. The document's own context denies the absolute reading: the Gotchas section says absolute guarantees require mapping the stack up front ("you MUST mmap your stack for the largest size you think you will need", lines 41–44), and the To Do list leaves commitment holes (line 85). A careless reader takes "in most situations" as "always" and reads "will receive errors on memory allocation as appropriate" as a synchronous per-request ENOMEM on every allocation path.

Replacement proposed (24 words; 3+-letter words absent from the quote include "documentation", "says", "under", "instead", "being", "touching"; preserves the source's hedge):

REPLACE 93b4fe285dc7 :: The documentation says that under mode 2, in most situations, a process receives errors on memory allocation instead of being killed while touching pages.

Per the seat rules I do not vote on my own replacement; two voters who did not write it must judge it.

### Row 4 — `3b02f6680556` — quote at S497 copy lines 37–38

```
The current overcommit limit and amount committed are viewable in
``/proc/meminfo`` as CommitLimit and Committed_AS respectively.
```

Verdict: entailed. "Viewable in /proc/meminfo as CommitLimit and Committed_AS respectively" grounds "published by the kernel for reading"; the two named fields are the two `/proc/meminfo` lines the entry is about, so "as two meminfo lines" restates the source without adding a consequence.

What a careless reader might over-read: "viewable" is not "enforced" — the doc's Status list still carries "Implement actual limit enforcement" (line 81), which is stale relative to the code (S499 shows the mode-2 check in `__vm_enough_memory`) but must not be read as "no enforcement exists"; and the mapping is respectively: limit → `CommitLimit`, committed → `Committed_AS`.

### Row 5 — `921c2e511e09` — quote at S497 copy line 48

```
In mode 2 the MAP_NORESERVE flag is ignored.
```

Verdict: entailed. "Ignored" means the flag has no effect under mode 2, so a mapping request carrying it is charged as if it lacked it. The charging rules in the same document (How It Works, lines 56–63: file-backed private writable and anonymous mappings cost "size of mapping per instance") plus the mode-2 cap (lines 20–22) make that charge count against the limit — hence "still charged against the commit limit".

What a careless reader might over-read: the sentence is mode-2-scoped — in modes 0/1 the flag is honored (S501, entry row 25) — and "ignored" does not mean the mapping is free; it is charged per the cost table. It also does not mean the request is refused outright; refusal follows only if the charge would breach the limit.

### Row 6 — `e37e65e64a4c` — quote at S497 copy line 57

```
The overcommit is based on the following rules

For a file backed map
	| SHARED or READ-only	-	0 cost (the file is the map not swap)
	| PRIVATE WRITABLE	-	size of mapping per instance

For an anonymous or ``/dev/zero`` map
	| SHARED			-	size of mapping
	| PRIVATE READ-only	-	0 cost (but of little use)
	| PRIVATE WRITABLE	-	size of mapping per instance

Additional accounting
	| Pages made writable copies by mmap
	| shmfs memory drawn from the same pool
```

Verdict: entailed. The cost table's file-backed row (line 57) says SHARED or READ-only costs 0, with the reason "(the file is the map not swap)" — exactly the claim's "add nothing to the committed total" and "because the file itself backs those pages". The claim's scope "file mappings" is load-bearing and matches the source: anonymous SHARED costs the mapping size (line 61), so the claim does not over-generalize.

What a careless reader might over-read: the 0-cost row is for file-backed maps only — extending it to anonymous shared memory (SysV shm, shmfs) is wrong per line 61 and lines 65–67 ("shmfs memory drawn from the same pool"). The claim keeps the file scope.

### Row 7 — `7b2fc298698e` — quote at S497 copy lines 83–85

```
To Do
=====
*	Account ptrace pages (this is hard)
```

Verdict: entailed. The To Do list still carries "Account ptrace pages (this is hard)" at v7.2, so ptrace pages are not accounted today — "the documentation still lists ptrace pages as unaccounted" — and a ledger that misses them "is not a complete ledger of every commitment". Both halves follow directly.

What a careless reader might over-read: "(this is hard)" is the kernel authors' note on implementation difficulty, not a measure of the hole's size; the source nowhere quantifies how much committed memory ptrace represents. The To Do item proves the doc lists the gap, nothing more.

## Verdict lines

ENTAIL 9afaa81505da entailed
ENTAIL 61b7677d56fe entailed
ENTAIL 93b4fe285dc7 overclaim — the claim states for mode 2 as such that "the documented failure is an allocation error at request time rather than a kill when pages are later touched", while the source scopes that outcome with "Depending on the amount you use, in most situations" (S497 copy lines 22–23); the unhedged sentence is a scope the source does not state.
ENTAIL 3b02f6680556 entailed
ENTAIL 921c2e511e09 entailed
ENTAIL e37e65e64a4c entailed
ENTAIL 7b2fc298698e entailed
REPLACE 93b4fe285dc7 :: The documentation says that under mode 2, in most situations, a process receives errors on memory allocation instead of being killed while touching pages.

(No votes on rows 8–28 — out of my assigned block.)

## Bounds

- Leaf seat: no subagents dispatched. No tools installed or upgraded (no pacman, no uv, no binaries) — nothing to record under the tooling authorization.
- Lane writes: this report file only. All git calls in the lane were read-only (`show`, `diff --stat`, `rev-parse`); no index, worktree or jj mutation anywhere; no fixture repos needed.
- Host reads: none beyond the lane; no sysctls read or written; no kernel-log message greps.
- Scratch `/fast/scratch/hyaku/mori-r52/Mo52Ent01/` (held only derived copies of lane-public bytes: the data-commit entry text and the hash-check script) is removed at the end of this session; the excerpts and hashes cited above are copied into this report.

## Verification of my own vote lines (post-write)

1. Frozen-counter run at R (read-only; `TMPDIR` in scratch, cwd scratch, absolute script path): `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c2.py 8524904adb25e44f24d9f25aac7eae909625c18c` → `C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment`, rc 1. Identical in shape to the pre-wave receipt (`evidence/c2-at-data.txt`), as expected before integration: the arm reads voter reports from revision R's tree (`git show <rev>:<path>`, count-c2.py lines 273–276; report list from `ls(ENTAIL_DIR)` at R, lines 128–135), so working-tree votes register when the L1 integrates the wave reports into a commit, not before. This is an observed instrument behavior, recorded as a limit — no change proposed to the frozen counter.
2. Parse check of my exact committed-to-be report bytes with the counter's own regexes (`ENTAIL_RE`, `REPLACE_RE` from count-c2.py lines 124–125, with its fence toggling) — rc 0: hashes present exactly `3b02f6680556 entailed`, `61b7677d56fe entailed`, `7b2fc298698e entailed`, `921c2e511e09 entailed`, `93b4fe285dc7 overclaim`, `9afaa81505da entailed`, `e37e65e64a4c entailed`; one `REPLACE` line parsed; its replacement text hashes (counter's `claim_hash`) to `3c2512af8468` — the hash two non-author voters will be asked to judge after the L1 applies the replacement.
3. Authorship side effect confirmed harmless: my authored set is `{3c2512af8468}` (count-c2.py line 148 hashes the replacement text), so my `entailed` votes on rows 1, 2, 4, 5, 6, 7 count normally; only the new row-3 text would ignore a vote from me, and I cast none on it.

## Findings

- MED — `corpus/knowledge/overcommit-commit-limit-r52.md:27` (Claims row 3, hash `93b4fe285dc7`): the claim cell drops the source's two hedges ("Depending on the amount you use", "in most situations" — S497 copy lines 22–23) and asserts an unconditional mode-2 failure mode; overclaim vote cast and replacement proposed (`REPLACE 93b4fe285dc7 :: …`). Under the frozen kill rule the L1 resolves this by replacing the claim text and collecting two `entailed` votes from voters who did not write the new text.
- LOW — `corpus/knowledge/overcommit-commit-limit-r52.md:26` (Claims row 2): correct as written, but "a share of RAM that defaults to one half" is easy to over-read as a constant; the share is configurable via `vm.overcommit_ratio`/`vm.overcommit_kbytes` and the knobs act only in mode 2 (S497 copy lines 29–32). No text change needed; the cell already says "defaults to".
- LOW — `.ufo/waves/round-52/count-c2.py:273-276` (observed behavior, frozen instrument — named limit, not a change request): the entailment arm reads voter reports only from revision R's tree, so a seat cannot see its own votes in the counter's output until the L1 commits the wave reports; mid-wave seat-level self-verification is limited to regex-level parse checks (done, section above). Receipts produced before integration will read `entailed=0 dissent=0` by construction.
- LOW — `corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2:81`: the upstream Status list still says "Implement actual limit enforcement" at v7.2, stale relative to the code (S499 shows the mode-2 check executing in `__vm_enough_memory`). The entry does not misstate this, but a reader of the doc alone could conclude mode 2 enforces nothing; candidate note for a round-53 route, not a round-52 claim defect.
