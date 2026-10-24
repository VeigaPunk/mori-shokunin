# CritRecordsAppend — round-42 record append-only audit

## Verdict

PASS — zero deletions of prior bytes. The criterion as specified
(insertions only) holds across all three record files. No counterexample
found; no correction required.

## Evidence

Command:

    git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 9de7323..34b92673 -- LOG.md SCORECARD.md corpus/SOURCES.md

### Diff stat

    LOG.md            | 62 +++++++++++++++++++++++++++++++++++++++++++++++++++++++
    SCORECARD.md      | 29 ++++++++++++++++++++++++++
    corpus/SOURCES.md |  7 +++++++
     3 files changed, 98 insertions(+)

### Numstat (added / deleted / file)

    62  0  LOG.md
    29  0  SCORECARD.md
    7   0  corpus/SOURCES.md

Deletion-line scan of the full diff (`grep '^-[^-]'`): 0 matches.
Total: 98 insertions, 0 deletions, 3 files.

### Hunk placement

| file | hunk header | old file length | placement |
|---|---|---|---|
| LOG.md | `@@ -2379,3 +2379,65 @@` | 2381 | tail append (round-42 entry + inherited-tree addendum §5) |
| SCORECARD.md | `@@ -2315,3 +2315,32 @@` | 2317 | tail append (round-42 section + errata: 4-scribes → 1-scout-5-scribes supersession) |
| corpus/SOURCES.md | `@@ -235,6 +235,13 @@` | 296 | mid-file insert into the sorted registry table: S232, S233, S234, S235, S241, S262, S347 |

Commits in range: `249c7e73` (freeze), `316f3dcf` (assimilation scratch),
`34b92673` (data).

## Notes / attack surface probed

- **Mid-file insertion is not a deletion.** corpus/SOURCES.md places the
  seven new rows inside the existing sorted table (before old line 236),
  not at end-of-file. Probed for hidden rewrite: all 6 context lines in
  the hunk are unchanged prior rows; the insert is a pure splice. The
  stated contract is "zero deletions of prior bytes (insertions only)" —
  this satisfies it literally. If the intent were strictly "tail-append
  only," SOURCES.md's sorted-table convention would make a tail append
  the violation instead; the current form is the correct discipline for
  this file.
- **Errata handled append-only.** The SCORECARD block corrects a prior
  superseded value ("4 scribes" → "1 scout, 5 scribes") by *adding* an
  errata section that records the supersession, not by editing the old
  line — consistent with append-only record discipline; the superseded
  bytes remain in place.
- No `-` lines, no rename/copy headers, no mode changes in the diff.

## Tooling

No installs or updates performed; `git` (already present) sufficed.

Report: .ufo/waves/round-42/w1/CritRecordsAppend.md
