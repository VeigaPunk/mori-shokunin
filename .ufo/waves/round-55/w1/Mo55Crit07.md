# Mo55Crit07 — C2 claim attack A (rows 1–8)

Seat: Mo55Crit07 (critic, non-voter). Lane: mori-shokunin, round 55 wave w1.
Assignment: attack claim-table rows 1–8 of `corpus/knowledge/disk-runway-enospc-r55.md`
against their exact pinned sources, with focus on errno and statfs interpretations.
No C1/C2 vote lines are emitted by this seat (no `ENTAIL`/`RECHECK`/`REPLACE` output).
Scope: rows 1–8 only. Frozen artifacts untouched; no production edits; no git/jj mutation.

Method: all reads read-only against the lane checkout at `b8a70adf93ebd9d1e4e95bef8627a220f2fa816b`
(entry landed at data commit `b8b7064c2b54c8b6b22c288232a96c43fae1af47`). Source pins
re-verified locally before use.

## Counter state (mechanical baseline)

Command: `python3 .ufo/waves/round-55/count-c2.py b8b7064c` (run from lane root).

Output: `C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=b8b7064c2b54c8b6b22c288232a96c43fae1af47 failed=entailment` — exit 1.
Same line at `HEAD` (`b8a70adf…`) — exit 1. Matches the assignment's data read exactly.
Note: the contract's literal `count-c2.py R` form fails `C2_SETUP unresolvable revision R` (exit 2);
`R` is a placeholder — the counter resolves only real revisions. Informational; not a counter defect.

## Pin verification (rows 1–8 sources)

All five source copies match `evidence/freeze-sha256.txt` (sha256sum, local recompute):
errno-base.h.v7.3 `2c148e92…93793c`, statfs.c.v7.3 `34e684be…05398`,
statfs.2.man-pages-6.19 `3dc4ed70…b9d`, statvfs.3.man-pages-6.19 `5f65e9ce…0b58`,
coreutils.texi.v9.12 `e6521c9b…4db9`. Pins OK.

## Row-by-row attack

| row | claim hash | source | quote located | verdict |
|---|---|---|---|---|
| 1 | faeadb48a5f8 | S535 errno-base.h.v7.3:32 | yes (tab/space-normalized) | supportable |
| 2 | e581c99e0a8d | S536 statfs.c.v7.3:62-63 | yes, verbatim | OVERCLAIM (see F1) |
| 3 | a7fc4050c55d | S536 statfs.c.v7.3:67-68 | yes, verbatim | supportable |
| 4 | 22a23e3fb849 | S541 statfs.2:43-44 | yes (line-join normalized) | supportable |
| 5 | 81caa7b585a4 | S541 statfs.2:45-46 | yes, verbatim | supportable |
| 6 | 4c77d3eef474 | S542 statvfs.3:228-231 | yes (man-macro join) | supportable |
| 7 | 420d69d60ee5 | S542 statvfs.3:232-234 | yes (line join) | supportable |
| 8 | f216a7fcdad1 | S543 coreutils.texi.v9.12:11950 | yes, verbatim | supportable |

Quote word counts (6–25 required): 10, 6, 11, 15, 16, 22, 14, 8 — all in range.

### Row 1 — errno (S535)
`#define ENOSPC 28 /* No space left on device */` at errno-base.h.v7.3:32 (tabs in source,
whitespace-normalized in the ledger quote — allowed by the counter's `normalise_text`).
Host read-only cross-check: `python3 -c "import errno,os; …"` → `ENOSPC= 28`,
`strerror= No space left on device`, so the generic-header claim holds for this x86_64 host.
The claim's framing ("error name and documented message rather than diagnosing the failed
operation") matches the header's content and the entry's scope note. No overclaim.

### Row 2 — statfs zero-fill (S536) — F1
Quote is verbatim (statfs.c.v7.3:62-63) and the sequencing claim is correct:
`memset(buf, 0, sizeof(*buf))` at :62 precedes `s_op->statfs(dentry, buf)` at :65 in
`statfs_by_dentry`. But the claim's universal "any field a filesystem never sets reaches
userspace as zero" is falsified within the same pinned file: the VFS itself fills fields
after the filesystem handler — `f_frsize` is set from `f_bsize` at :67-68 when the
filesystem left it 0, and `vfs_statfs` sets `f_flags` at :86-94 (`ST_VALID | …`). A
filesystem that never sets `f_frsize` or `f_flags` still has those fields non-zero in
the userspace reply. The zero-fill guarantee covers only fields that neither the
filesystem nor the VFS later writes. The main point (buffer zeroed before the fs handler)
is correct; the quantifier overreach is the defect. See F1 in Findings.

### Row 3 — statfs fragment-size default (S536)
Quote verbatim (:67-68). The inference "block counts on such filesystems are expressed in
block-size units" is consistent with the pinned statvfs.3 struct comment `f_blocks /* Size
of fs in f_frsize units */` (statvfs.3:37): when the VFS defaults `f_frsize` to `f_bsize`,
counts are in block-size units. Interpretation sound; no overclaim.

### Rows 4–5 — statfs.2 block/inode fields (S541)
Quotes located at statfs.2:43-44 (`f_bavail /* Free blocks available to unprivileged user */`,
source line-join normalized) and :45-46 (`f_files`/`f_ffree`). Claims match the documented
field semantics. Row 5's trailing clause "that a block-only reading ignores" is a
definitional gloss (a block-only reading by construction does not read the inode pair), not
a factual overclaim.

### Rows 6–7 — statvfs favail equality (S542)
Quotes located at statvfs.3:228-231 and :232-234. statvfs.3:46-47 documents
`f_favail /* Number of free inodes for unprivileged users */`, supporting the claim's
"the statvfs field meant for ordinary users". Row 7's "no filesystem keeps inodes back for
the superuser" is a fair paraphrase of "no filesystems with an inode root reservation
exist". No overclaim.

### Row 8 — coreutils df -i (S543)
Quote located verbatim at coreutils.texi.v9.12:11950 under `@optItem{df,-i,}` /
`@optItemx{df,--inodes,}`; "List inode usage information instead of block usage" supports
"replaces the block columns rather than adding to them". "Only when asked for them" is a
fair reading of the option-gated inode listing. Note (informational): the same sentence
also appears at :12262 under `du --inodes`; the df occurrence is the located cite and the
claim is about df, so no ambiguity defect.

## Findings

- F1 — severity medium — Row 2 (hash e581c99e0a8d) universal-quantifier overclaim: "any
  field a filesystem never sets reaches userspace as zero" is falsified by VFS-filled
  fields in the same source (`f_frsize` at statfs.c.v7.3:67-68, `f_flags` at :86-94).
  Evidence: `corpus/evidence/sources-r55/statfs.c.v7.3:62-94`; row text
  `corpus/knowledge/disk-runway-enospc-r55.md` claim-table row 2. Smallest safe
  correction: scope the quantifier to fields nobody writes, e.g. "…so any field that
  neither the filesystem nor the VFS later sets remains zero in the userspace reply",
  or drop the trailing clause and keep the located zero-fill fact. This is a wording-level
  overclaim only; quote locatedness, pin, and source row are all clean, and the kill rules
  are not implicated.
- No other defects in rows 1–8. All eight quotes are located and verbatim modulo
  whitespace normalization; all pins match; errno and statfs interpretations otherwise
  check out against the pinned v7.3 / man-pages 6.19 / coreutils 9.12 bytes and the
  read-only host errno observation.
- Informational (no action): contract command form `count-c2.py R` exits 2 on the literal
  placeholder; the counter reproduces the data read with real revisions. Row 8's quote
  string occurs twice in coreutils.texi (df :11950, du :12262); the df occurrence governs.

Verification performed: pin sha256 recompute; counter runs at b8b7064c and HEAD (exit 1,
data-read line reproduced); quote substring locatedness re-check for all eight rows;
source context reads with line numbers; host read-only errno check. Unverified: none
within rows 1–8 scope; rows 9–23 are outside this seat's assignment.
