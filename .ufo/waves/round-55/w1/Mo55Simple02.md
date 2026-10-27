# Mo55Simple02 — YAGNI review of C2 entry and claims (redundancy without dropping coverage)

Seat: leaf, non-voting. Task: find removable weight in `corpus/knowledge/disk-runway-enospc-r55.md` and its 23 claim
rows, and say what must *not* be removed because coverage would fall. Read-only: no production edit, no git/jj
mutation, no counter or kill-rule change. Scratch `/fast/scratch/hyaku/mori-r55/Mo55Simple02` created and removed.
Line numbers and quoted cells below are the worktree file as read for this review; F0 records the one row where the
worktree differs from the measured revision.

## Axes named (god speed)

1. **Coverage floor** — 23 claim rows, 9 sources; frozen floors `MIN_CLAIMS=16`, `MIN_SOURCES=6`
   (`count-c2.py:53-54`).
2. **Semantic coverage** — six mechanism groups must each stay grounded: interface/read discipline (rows 1–8),
   XFS block+inode (9–12), btrfs zero-Avail (13–17), btrfs sysfs (18–19), tmpfs (20–23). Each of the six decision
   rows (entry:41–46) consumes at least one group.
3. **Prose reproducibility** — the host section should be one reproducible instant, not several.
4. **Vote binding** — claim hashes are `sha256(claim cell)` (`count-c2.py:137-138`), so a claim-text edit
   invalidates settled entailment votes; prose edits do not.

A move is kept only if it improves an axis and harms none. On those axes exactly two real redundancies exist, and
only one is removable this round without touching a vote.

## Command evidence

```
$ python3 .ufo/waves/round-55/count-c2.py b8b7064c2b54c8b6b22c288232a96c43fae1af47
C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=b8b7064c2b54c8b6b22c288232a96c43fae1af47 failed=entailment
exit=1
```

Matches the handed data read exactly (23/23, 0 missing, 0 bad rows, 9 sources, pins/provenance/source rows ok,
entailment arm open because no votes are settled at this instant). Disk guard before work: `/fast/scratch/hyaku`
26% use, 594.6G free — no ENOSPC, no install needed.

Measured revision and worktree diverge in one claim row (details in F0 below). The same predicate, fed the
*worktree* bytes through its own `evaluate` (reader pointing at the lane, no git write), prints:

```
C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=WORKTREE failed=entailment
```

So both text variants satisfy every mechanical arm; only the row-4 claim hash moves.

Removal simulations, run through the frozen counter's own `parse_claims` imported from the counter file (no copy of
the predicate, no git mutation):

```
as-landed:              rows=23 sources=9 hashes_unique=True
minus row 7 (line 17):  rows=22 sources=9 hashes_unique=True
minus prose (line 50):  rows=23 sources=9 hashes_unique=True
```

## Redundancy inventory

### R1 — real, one row: line 17 duplicates line 16 (severity low, blocked)

Row 6 (entry:16) states the norm: on Linux the unprivileged inode figure always equals the plain one and no
filesystem can report otherwise (`statvfs.3.man-pages-6.19:228-232`). Row 7 (entry:17) restates that as rationale —
no inode root reservation, so one reading serves every caller (`statvfs.3.man-pages-6.19:233-234`). Both rows sit in
one paragraph of one manual; row 7 adds a *reason*, not an observable. Its distinctive terms (`root reservation`,
`superuser`) appear nowhere in the decision table, the host section or the boundaries — verified by term scan over
the text after entry:35.

It is coverage-neutral to delete: S542 stays used through row 6, so the removal keeps `sources=9` (simulation above).
It is also **unpoliceable by the frozen predicate**: 22 rows still clears `MIN_CLAIMS=16`, so a deletion would print
`C2=met` while the contract's "23 claims" target is silently missed. Deletion is therefore *not* a this-round move —
the target is 23 and the seat that owns production text is the L1. If a later round consolidates, the only
coverage-preserving form is folding the rationale into row 6's claim cell, which changes that hash and forces
re-settlement of its entailment votes; that is a REPLACE-class correction, outside a non-voting leaf's scope.

### R2 — real, prose: line 50 is a superseded second copy of line 58 (severity medium)

Entry:50 (88 words) and entry:58 (154 words) publish the same measurement set, and the same set is already the
reproducible artefact `.ufo/waves/round-55/evidence/host-disk-snapshot.txt` (1861 bytes, date=2026-10-27). Checked
value by value, line 50 contributes **no unique coverage**: filesystem types, per-mount blocks/free/available/
inodes, `df -P` capacity, `df -i` inode use, `/dev/shm` size and free inodes, btrfs metadata `total_bytes`/
`bytes_used`, `global_rsv_size`, and the kernel release all appear in the captured file (including the sixth
`/run/user/1000` tmpfs line). What the two copies do *not* share is their numbers:

| datum (entry:50 vs entry:58 / evidence file) | inline | captured |
|---|---|---|
| `/fast` free/available blocks | 147,466,003 | 155,927,507 |
| `/fast` `df -P` capacity | 30% | 26% |
| `/tmp` free inodes | 67,005,211 | 67,004,121 |
| `/` bfree / bavail | 164,023,017 / 154,680,289 | 164,012,985 / 154,665,001 |
| btrfs metadata bytes_used | 41,834,954,752 | 41,824,190,464 |
| `/dev/shm` free inodes | 3,965,092 | 3,965,173 |

The `/fast` gap alone is 8,461,504 blocks = 34,658,320,384 bytes at bsize 4096 (~32.3 GiB). Neither paragraph carries
a collection time beyond the date, so a reader cannot order them, and the directions do not agree (`/fast` fuller
inline, `/tmp` inode use lower inline, btrfs metadata higher inline). Which copy is current is decidable only
against the host: the guard reading taken before this work (`/fast` 26%, 594.6G free) matches the captured file's
own `df -P` line (`623,710,028` KiB ≈ 594.8 GiB) and not the inline figures, so the inline copy is the superseded
one [INFERENCE: ordering by arithmetic, not by clock].

This is the only move that improves an axis and harms none: it is outside every table, so `parse_claims` output is
identical (23 rows, 9 sources) and no claim hash — hence no vote — moves. Recommendation to the L1: keep the
classification sentence (which path is which filesystem) and the pointer to the evidence file, drop the inline
numerals, or stamp each paragraph with its collection instant. Not applied here (production text, not my scope).

### R3 — apparent, must keep: the 14/15 clause split is forced

Rows 14 and 15 are two halves of one kernel comment (`btrfs_super.c.v7.3:1802-1808`), with quote overlap
("allocate chunks for our metadata profile"). The minimal contiguous span covering both is **34 words**, over
`MAX_WORDS=25` (`count-c2.py:57`), so a single located row cannot carry both. More important, row 15 is a precision
guard: the code's condition is three conjuncts — `space_info->full`, `total_free_meta < thresh`, and
`total_free_meta - thresh < block_rsv->size` (`btrfs_super.c.v7.3:1809-1811`). Row 14 alone would read as a
sufficient rule ("reports zero once its metadata profile can take no further chunk allocations"), which a careful
entailment voter could legitimately call an overclaim. Removing 15 would trade a row of redundancy for a depth-arm
failure — it harms an axis, so it stays.

### R4 — apparent, must keep: rows 20 and 22 are two facets of one mount option

`nr_inodes` ceiling (row 20) and `nr_inodes=0` = unlimited (row 22) come from the same option text; contiguous span
**118 words**, far over the 25-word ceiling. Row 22's load is not decorative: decision row 28 (entry:44) tells the
reader to inspect `nr_inodes=` with `findmnt`, and the value `0` is only interpretable as "no inode ceiling" from
this row. Only the "generally unwise" clause is advice rather than observation — a wording nit, not removable
weight, and rewording would change the hash.

### R5 — apparent, must keep: the decision table restates claims on purpose

Decision rows entry:41–46 re-express claims 9–17 and 20–23 in observation → interpretation → next-read form
(36–47 words per row). That is the entry's operability surface and each row consumes a distinct mechanism group;
stripping the restatements would leave a reader of the table alone without the claim basis. Do not prune this as
"duplication".

### R6 — apparent, must keep: S541 and S542 overlap but are different syscalls

`statfs(2)` publishes the unprivileged fields this host actually reads (`stat -f`, `df`), and `statvfs(3)` supplies
the `f_favail` equality of rows 6–7. Their struct listings overlap semantically (both show `f_bavail` for
unprivileged users), so on a pure source-ledger view S541 could be folded into S542 — which would drop sources to 8
and misdescribe which syscall produced the host numbers. Retain. Clarity nit: the entry never names the syscall the
host calls, so a reader can conflate the two; one clause would fix it, at the cost of a edit.

### Refuted YAGNI suspicion: no claim cell is a quote paraphrase

Because `MIN_BEYOND=3` (`count-c2.py:56`) only sets a floor, I measured the actual delta of every claim cell against
its own quote: minimum 8 words beyond (row 15), median ~18, maximum 23 (row 11). No row is a restatement of its
quote; claim cells carry real interpretation. Wording compression of the 23–30-word claims is therefore not available
weight — and any compression that changes a claim cell changes its hash and reopens its votes.

### Structural finding: the counter cannot police the target

`MIN_CLAIMS=16` / `MIN_SOURCES=6` against a contract target of 23 / 9 leaves 7 rows and 3 sources of slack
(`count-c2.py:53-54` vs `contract.md` C2 target). Rows 1 and 8 are the only single-source rows (S535, S543): deleting
either drops the entry to 8 sources, still above the floor. So every deletion candidate in this entry would pass the
frozen predicate while regressing the published target. This is a falsification gap for the depth axis, not weight to
remove, and it is why no deletion is proposed for this round beyond the vote-neutral prose line.

## Non-actions

No vote line is issued by this seat; no claim text, counter, contract, control, source copy or ledger was read-write
touched; no git/jj command was run beyond `git log`/`git show`-equivalent reads inside the counter. No installs.

## Findings

- **High — the editable worktree entry is not the measured entry, and the divergence changes one claim hash.**
  `corpus/knowledge/disk-runway-enospc-r55.md` was modified in the worktree at 2026-10-27 03:42:02, after the data
  commit `b8b7064c`. Exactly one row differs (row 4): the committed text reads “the plain free count, and a second
  count limited to what an unprivileged **process** may still use” with quote `fsblkcnt_t f_bfree; /* Free blocks in
  filesystem */ fsblkcnt_t f_bavail; /* Free blocks available to` (a two-field span cut mid-comment), while the
  worktree reads “...unprivileged **user** may still use” with quote `fsblkcnt_t f_bavail; /* Free blocks available
  to unprivileged user */`. Claim hashes: `22a23e3fb849` at the measured revision vs `45120996891a` in the worktree.
  Both variants pass every mechanical arm (pins, located 23/23, 9 sources, provenance), so this cannot be caught by
  re-running the counter at the old revision; but entailment votes are hash-bound, so any seat that reads the file
  and votes produces a row-4 line the counter rejects under `rev=b8b7064c`, and the reverse after a commit of the
  worktree text. Either revert the worktree row or commit it and re-measure, and fix which text the seats vote on.
  Evidence: `corpus/knowledge/disk-runway-enospc-r55.md:14` (worktree), `git show b8b7064c:corpus/knowledge/disk-runway-enospc-r55.md`
  (committed row 4), mtime above; `count-c2.py:137-138` (hash is the claim cell).
- **Medium — entry:50 duplicates entry:58 and is superseded, with disagreeing values.** 88-word inline snapshot has
  zero unique coverage against `.ufo/waves/round-55/evidence/host-disk-snapshot.txt`, disagrees with it on six
  figures (`/fast` free blocks 147,466,003 vs 155,927,507; 30% vs 26%; ~32.3 GiB apart), and lacks a collection
  time. Deletion is counter-neutral and vote-neutral (simulated output identical).
  Evidence: `corpus/knowledge/disk-runway-enospc-r55.md:50`, `:58`, `.ufo/waves/round-55/evidence/host-disk-snapshot.txt`.
- **Low — entry:17 (row 7) is a rationale duplicate of entry:16 (row 6).** Coverage-neutral to delete (sources stay
  9) but blocked: 22 rows still clears the counter floor, so the frozen predicate would not notice the 23-row target
  being missed. Evidence: `corpus/knowledge/disk-runway-enospc-r55.md:16-17`,
  `corpus/evidence/sources-r55/statvfs.3.man-pages-6.19:228-234`.
- **Low — the frozen counter's floors sit 7 rows / 3 sources below the contract target**, so row and source
  regressions are unpoliced. Evidence: `.ufo/waves/round-55/count-c2.py:53-54`, `.ufo/waves/round-55/contract.md` (C2).
- **Info — two apparent redundancies are load-bearing and must not be pruned:** rows 14/15 (34-word contiguous span
  > 25-word ceiling; row 15 guards row 14 against overclaim) and rows 20/22 (118-word span). Evidence:
  `corpus/evidence/sources-r55/btrfs_super.c.v7.3:1802-1811`,
  `corpus/evidence/sources-r55/tmpfs.rst.v7.3` (`nr_inodes` option text).
- **Info — claim cells are not quote paraphrase** (min 8 words beyond quote, floor 3), so wording is not available
  weight without reopening votes. Evidence: `.ufo/waves/round-55/count-c2.py:56`, measurements on entry:11-33.
