measured 2026-10-23T05:39:35Z
# JudgeLessonItem7 — Item 7 (receipt time labels), round-34 corrections in corpus/lessons/round-33.md at 8d56809

Scope: block `### Item 7 — receipt time labels` (round-33.md:242-251), answering routed defect §8 item 7 of
round-33-verifier-spotcheck.md (spotcheck:240-241). All reads at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3;
read-only lane git only; no tools installed (operator directive: nothing needed).

VERDICT: repaired — every factual claim checks against the committed bytes; one minor citation section-label mislabel
listed below.

## Checks (each statement vs committed bytes)

1. "§8 item 7 correctly flags two inaccurate receipt labels" — spotcheck:240-241: `c1-controls.txt:1` (02:38Z,
   actual 02:30:05Z), `parity-freeze.txt:1` (02:3xZ, actual 02:28:27Z). Matches. ✓
2. "header of evidence/c1-controls.txt:1 says the C0 dispatch was 2026-10-23T02:38Z" — file line 1 at
   8d56809: "# round-33 C1 controls (wave C0, 5 seats, dispatched 2026-10-23T02:38Z; dispatch c0-dispatch.json)". ✓
3. "closure records the actual dispatch as 2026-10-23T02:30:05.953Z (spotcheck §2, lines 50-53)" — spotcheck:52:
   "C0 was dispatched at 02:30:05.953Z." (lines 50-53 are inside §2, heading at spotcheck:48). ✓
4. "The receipt is carried by commit fdf4371f, whose committer time is 2026-10-23T02:39:02Z; that commit time is
   not the dispatch time" — `git ls-tree fdf4371f` contains .ufo/waves/round-33/evidence/c1-controls.txt (blob
   81e5e908…, byte-identical at fdf4371f and 8d56809); `git show -s --format=%cI fdf4371f` = 2026-10-22T23:39:02-
   03:00 = 2026-10-23T02:39:02Z; dispatch 02:30:05.953Z ≠ commit time. ✓
5. "header of evidence/parity-freeze.txt:1 says 2026-10-23T02:3xZ" — file line 1 at 8d56809: "parity check
   (whitespace runs collapsed) run 2026-10-23T02:3xZ by L1 MoriR33 at the freeze:". ✓
6. "closure identifies the actual run as 2026-10-23T02:28:27Z (spotcheck §1, lines 41-43)" — spotcheck:42-43:
   "the actual run was 02:28:27Z". ✓ (line 43 is the run time; lines 41-43 are inside §1.)
7. "Commit 27969134 carries the original receipt at committer time 2026-10-23T02:28:27Z, matching the closure's run
   time" — `git ls-tree 27969134` contains .ufo/waves/round-33/evidence/parity-freeze.txt; `git show -s
   --format=%cI 27969134` = 2026-10-22T23:28:27-03:00 = 2026-10-23T02:28:27Z = closure run time. ✓
8. "the closure also records that the content landed at that committer time (spotcheck §2, lines 37-39)" — the
   sentence "the content landed at committer time 23:28:27" is at spotcheck:38-39. **Minor mislabel:** lines 37-39
   are in §1 (the Timestamps bullet; §2's heading is at spotcheck:48), not §2. The quoted content, line numbers and
   substance are correct; only the section label is wrong (§1, not §2).
9. "Preserve both receipt files unchanged" — both flagged headers are intact at 8d56809; c1-controls.txt is
   byte-identical from fdf4371f to tip. Note: parity-freeze.txt is *not* byte-identical to its 27969134 version —
   at fdf4371f (A1 landing) three A1-parity lines were appended below the mislabeled header (blob 11628e0… →
   f472b44d…; `git log 27969134..8d56809 -- …/parity-freeze.txt` = fdf4371f only). This does not touch the labeled
   line and is not a correction of the label; no block claim asserts byte-identity across commits, so not a wrong
   statement.
10. "Round 34 carries the fix forward: every round-34 receipt's first line is date -u output (evidence/*.txt,
    c0/*.md, wave-A seat reports)" — at 8d56809 all five evidence/*.txt (c1-before, c1-controls, c1-posctl,
    c1-tool-provenance, census-start) open with "measured"/"written" + ISO timestamp, and all ten c0/*.md open with
    "measured 2026-10-23T…Z". Wave-A seat reports are not committed at 8d56809; the 11 seated reports in the live
    working tree (.ufo/waves/round-34/wa/*.md) all open with "measured 2026-10-23T…Z" (working-tree check, not
    committed bytes).
11. Append-only confirmation: `git diff f10a320d 8d56809 -- corpus/lessons/round-33.md` = 0 deletions, 50
    insertions (211 → 261 lines); the additions begin exactly at the "## Round-34 corrections" heading and include
    the Item 7 block; nothing above the heading changed. ✓
12. SOURCES diff 7d382043→89791013 (17+, 6-): no Item-7 statement references SOURCES; not applicable to this item.

## Findings

- **Minor (citation label):** Item 7 cites `round-33-verifier-spotcheck.md` "§2, lines 37-39" for the
  "content landed at committer time" sentence; those lines are in §1 (spotcheck:38-39), §2 starts at :48. No other
  statement is wrong.
- No wrong statements otherwise; all receipts, commit times (via %cI), spotcheck line/section anchors, and the
  append-only property verified.

## Residual risk / verification gaps

- The "actual" times (02:30:05.953Z, 02:28:27Z) are transcribed from the closure's spotcheck; I did not independently
  re-derive them from driver logs. The block faithfully matches the closure's records.
- The wave-A seat-report half of claim 10 is verified against the live working tree (untracked), not committed bytes at
  8d56809; the committed evidence/*.txt and c0/*.md halves fully verify at the revision.
