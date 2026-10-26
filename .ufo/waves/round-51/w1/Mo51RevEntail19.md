# Mo51RevEntail19 — entailment votes, claim rows 19–21 (mori round 51, wave w1)

Seat: Mo51RevEntail19 (reviewer, ENTAILMENT item, leaf — no subagents).
Data commit: `87e0c374537557754bf71dd68036ded3ddc6699c`. Frozen contract: `.ufo/waves/round-51/contract.md` (read first).
Assigned rows: 19–21 of the `## Claims` table of `corpus/knowledge/memavailable-estimate-r51.md` at the data commit.
All three rows draw on source S496, the committed copy `corpus/evidence/sources-r51/34e431b0.patch` (the 2014
commit `34e431b0ae39` "/proc/meminfo: provide estimated available memory").

## Method and provenance

- Committed bytes, not worktree guesses: every file was read via `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 87e0c374537557754bf71dd68036ded3ddc6699c:<path>` into my scratch. A read-only `git diff --stat 87e0c374 -- corpus/knowledge/memavailable-estimate-r51.md corpus/evidence/sources-r51/ corpus/SOURCES.md` returned empty, so the worktree matches the data commit for every path I judged.
- Copy integrity: `sha256sum` of the extracted patch copy = `9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0`, equal to the sha256 named in the S496 row of `corpus/SOURCES.md` (line 275 at the data commit) and to the last hash in the entry's `recheck:` line (verified present in the committed entry, grep count 1).
- Hash verification: each claim cell was re-hashed with the prescribed one-liner `python3 -c 'import hashlib,re,sys;print(hashlib.sha256(re.sub(r"\s+"," ",sys.argv[1]).strip().encode()).hexdigest()[:12])' "<claim text>"` and all three outputs equal the frozen values in `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt` (row 19 `a07e4bd7a5ec`, row 20 `4d162ecf1409`, row 21 `50f54829ae20`). The claim cells were extracted programmatically from the committed entry's table (21 rows found), so no transcription is trusted.
- Quote location: each quote, whitespace-collapsed, occurs exactly once in the committed patch copy (programmatic count = 1 for each).
- Context: I read the whole commit message (patch lines 1–27, which is ±20 lines around all three quotes) and the diff body (patch lines 28–133) of the committed copy.

## Row judgments

### Row 19 — hash `a07e4bd7a5ec`

Claim cell: "The 2014 commit says workload placers estimated free memory by summing free and cached, which it calls outdated."

Quote: `` `They generally do this by adding up "free" and "cached", which was fine ten years ago,` `` — located at `corpus/evidence/sources-r51/34e431b0.patch` lines 7–8 (tail of line 7, head of line 8; whitespace collapsed), unique.

Context read (patch lines 6–9): "Many load balancing and workload placing programs check /proc/meminfo to estimate how much free memory is available.  They generally do this by adding up "free" and "cached", which was fine ten years ago, but is pretty much guaranteed to be wrong today."

Decomposition: "workload placers" = "workload placing programs" (the "load balancing" half is dropped — compression, not addition); "estimated free memory" = "estimate how much free memory is available" (backshifted tense of indirect speech after "The 2014 commit says"); "by summing free and cached" = "by adding up 'free' and 'cached'"; "which it calls outdated" = "was fine ten years ago, but is pretty much guaranteed to be wrong today" — a one-word gloss of exactly that judgment (fine then, wrong now). The unquantified plural "workload placers" stays generic; the source's own quantifier ("Many … programs", "generally") is not contradicted and no universal is asserted. No consequence, number, or scope is added beyond the source.

Verdict: entailed.

### Row 20 — hash `4d162ecf1409`

Claim cell: "That commit's reason the sum misleads is that Cached includes shared memory, tmpfs and ramfs pages that cannot be dropped like cache."

Quote: `` `It is wrong because Cached includes memory that is not freeable as page cache, for example shared memory segments, tmpfs, and ramfs,` `` — located at `corpus/evidence/sources-r51/34e431b0.patch` lines 11–12, unique.

Context read (patch lines 11–14): the sentence continues "and it does not include reclaimable slab memory, which can take up a large fraction of system memory on mostly idle systems with lots of files." So the commit's stated reason has two conjuncts; the claim reports the first.

Decomposition: "the sum misleads" glosses "It is wrong", where "It" is the free+cached summing that the programs of lines 6–8 rely on for their estimates — a wrong estimate for its stated use misleads; "Cached includes shared memory, tmpfs and ramfs" = "for example shared memory segments, tmpfs, and ramfs" ("segments" dropped — compression); "cannot be dropped like cache" = "not freeable as page cache". The commit's own wording is "It is wrong because Cached includes …", so the claim's reason attribution is literal. The second conjunct (reclaimable slab absent from Cached) is omitted by the claim — an omission, not an addition; nothing in the claim goes beyond the source.

Verdict: entailed.

### Row 21 — hash `50f54829ae20`

Claim cell: "The commit put the estimate into meminfo so that monitoring programs need not model reclaim internals themselves."

Quote: `` `user space really should not be expected to know kernel internals to come up with an estimate for the amount of free memory.` `` — located at `corpus/evidence/sources-r51/34e431b0.patch` lines 21–23 (tail of line 21, line 22, head of line 23), unique.

Context read (patch lines 16–26): "Currently, the amount of memory that is available for a new workload, without pushing the system into swap, can be estimated from MemFree, Active(file), Inactive(file), and SReclaimable, as well as the "low" watermarks from /proc/zoneinfo. / However, this may change in the future, and user space really should not be expected to know kernel internals … / It is more convenient to provide such an estimate in /proc/meminfo.  If things change in the future, we only have to change it in one place." Plus subject line 4 ("/proc/meminfo: provide estimated available memory") and the diff body, which adds `long available;` and the `MemAvailable:` line to `fs/proc/meminfo.c` (patch lines ~60–100).

Decomposition: "put the estimate into meminfo" is grounded by the subject line, by "provide such an estimate in /proc/meminfo", and by the diff actually adding it to `fs/proc/meminfo.c` in this committed copy; "so that … need not model … themselves" matches the source's modality ("really should not be expected to know … to come up with an estimate"); "monitoring programs" names the subset of user space the commit opens with (programs checking meminfo to estimate free memory) — within, not beyond, the source's "user space"; "reclaim internals" concretizes "kernel internals" via the immediately preceding paragraph, whose inputs (MemFree, Active(file), Inactive(file), SReclaimable, low watermarks) are exactly the reclaim estimate. No consequence, number, or scope is added beyond the source.

Verdict: entailed.

## Verdict lines (one per assigned row; no overclaim, so no replacement lines)

ENTAIL a07e4bd7a5ec entailed
ENTAIL 4d162ecf1409 entailed
ENTAIL 50f54829ae20 entailed

## Evidence log (command → output → exit)

1. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree --name-only 87e0c374537557754bf71dd68036ded3ddc6699c corpus/evidence/sources-r51/` → the five frozen copies (`34e431b0.patch`, `meminfo.c.v7.2`, `mm_inline.h.v7.2`, `proc.rst.v7.2`, `show_mem.c.v7.2`) → exit 0.
2. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat 87e0c374537557754bf71dd68036ded3ddc6699c -- corpus/knowledge/memavailable-estimate-r51.md corpus/evidence/sources-r51/ corpus/SOURCES.md` → empty output (worktree matches the data commit for these paths) → exit 0.
3. `git show 87e0c374…:corpus/evidence/sources-r51/34e431b0.patch` then `sha256sum` → `9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0` → matches SOURCES.md:275 (S496) and the entry `recheck:` line (grep count 1) → exit 0.
4. Hash one-liner on the three claim cells extracted from the committed table → `a07e4bd7a5ec`, `4d162ecf1409`, `50f54829ae20` → all equal `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt` rows 19–21.
5. Whitespace-collapsed occurrence count of each quote in the committed patch copy → 1, 1, 1 (unique each).
6. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 87e0c374…:corpus/SOURCES.md | grep -n 'S496'` → one row at line 275: names the commit URL, the copy path, the same sha256, `mined`, opened `2026-10-26`, used-by lists `corpus/knowledge/memavailable-estimate-r51.md` → exit 0.
7. `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku 25% 602.3G free`, no ENOSPC.

## Limits and UNVERIFIED

- I judged the claim cells against the committed copy only. I did not re-fetch the five source URLs; that the URL still returns these bytes today is UNVERIFIED by me (the counter's pin arm and the recheck line cover it; the copy's sha256 matches both the S496 row and the entry's recheck line, which is the internal consistency check available locally).
- All three of my rows draw on the single source S496; I wrote no verdict for rows 1–18 and no vote on any text other than the three assigned claim cells.
- No overclaim was found, so no replacement claim cell was proposed and no second hash was computed.

## Tooling

No tool was installed or upgraded (nothing needed: `git show`, `sha256sum`, `grep`, `python3` hashlib only). No pacman transaction was run (host-wide pause respected). No writes outside my report file and my scratch.

## Scratch

Scratch root `/fast/scratch/hyaku/mori-r51/Mo51RevEntail19/` (with `tmp/` as TMPDIR) held only `entry-at-data.md` and `34e431b0.patch`; every cited line is quoted inside this report, and the directory is removed after this report is written. No clone was made (read-only `git show` from the lane only); the lane repo, its jj state and its git index were not mutated.

## Findings

- LOW — `corpus/knowledge/memavailable-estimate-r51.md` row 20 (claim cell; source `corpus/evidence/sources-r51/34e431b0.patch:11-14`): the claim states only the first conjunct of the commit's two-part reason — the commit also cites that Cached "does not include reclaimable slab memory". Judged entailed (omission is not an added consequence, number, or scope), but as a statement of "the commit's reason" it is incomplete; if the L1 ever rewords the cell, adding the slab conjunct would make it complete.
- LOW — `corpus/knowledge/memavailable-estimate-r51.md` row 21 (claim cell; source `34e431b0.patch:16-26`): the largest paraphrase distance of the three ("monitoring programs" for "load balancing and workload placing programs"/"user space"; "reclaim internals" for "kernel internals"; "model" for "know … to come up with an estimate"). Judged entailed — each gloss stays inside the source's stated scope and the diff body grounds the meminfo part — noted for calibration.
- LOW — `corpus/knowledge/memavailable-estimate-r51.md` row 19 (claim cell; source `34e431b0.patch:6-9`): "which it calls outdated" compresses "was fine ten years ago, but is pretty much guaranteed to be wrong today", and the hedges "Many"/"generally" are dropped in the generic plural. Judged entailed; noted.

No HIGH or MED finding: all three assigned claim cells follow from their quotes plus the surrounding committed context, and all three hashes match the frozen values.
