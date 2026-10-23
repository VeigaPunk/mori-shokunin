measured 2026-10-23T07:50:24Z
# ReJudgeLesson7 — re-judge of '### Item 7' under '## Round-34 corrections' in corpus/lessons/round-33.md at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3

VERDICT: not repaired — the block answers the routed defect and all receipt facts check, but it contains one wrong detail: it cites `round-33-verifier-spotcheck.md` "§2, lines 37-39" for the "content landed at committer time" sentence; those lines are in §1 (spotcheck §1 heading at line 19, §2 heading at line 48; the sentence sits at §1 lines 37-39). Wrong detail: section label §2 → should be §1.

## Checks (each factual statement vs committed bytes)

1. "§8 item 7 correctly flags two inaccurate receipt labels" — spotcheck:240-241: `c1-controls.txt:1` (02:38Z, actual 02:30:05Z) and `parity-freeze.txt:1` (02:3xZ, actual 02:28:27Z). Matches. Agree.
2. "Header of evidence/c1-controls.txt:1 says the C0 dispatch was 2026-10-23T02:38Z" — file line 1 at 8d56809: "# round-33 C1 controls (wave C0, 5 seats, dispatched 2026-10-23T02:38Z; dispatch c0-dispatch.json)". Matches.
3. "Closure records the actual dispatch as 2026-10-23T02:30:05.953Z (spotcheck §2, lines 50-53)" — spotcheck:52 "C0 was dispatched at 02:30:05.953Z."; lines 50-53 inside §2 (heading at :48). Matches.
4. "The receipt is carried by commit fdf4371f, whose committer time is 2026-10-23T02:39:02Z; that commit time is not the dispatch time" — `git show -s --format=%cI fdf4371f` = 2026-10-22T23:39:02-03:00 = 2026-10-23T02:39:02Z; fdf4371f adds .ufo/waves/round-33/evidence/c1-controls.txt (not present in parent 27969134: `git show 27969134:.ufo/waves/round-33/evidence/c1-controls.txt` → fatal path-not-in-commit); dispatch 02:30:05.953Z ≠ commit time. Matches.
5. "Header of evidence/parity-freeze.txt:1 says 2026-10-23T02:3xZ" — file line 1 at tip: "parity check (whitespace runs collapsed) run 2026-10-23T02:3xZ by L1 MoriR33 at the freeze:". Matches.
6. "Closure identifies the actual run as 2026-10-23T02:28:27Z (spotcheck §1, lines 41-43)" — spotcheck:42-43: "the actual run was 02:28:27Z"; lines 41-43 inside §1. Matches.
7. "Commit 27969134 carries the original receipt at committer time 2026-10-23T02:28:27Z, matching the closure's run time" — `git show -s --format=%cI 27969134` = 2026-10-22T23:28:27-03:00 = 2026-10-23T02:28:27Z; 27969134 contains .ufo/waves/round-33/evidence/parity-freeze.txt (4 lines, incl. header with 02:3xZ). Matches.
8. "The closure also records that the content landed at that committer time (spotcheck §2, lines 37-39)" — the sentence is at spotcheck §1 lines 37-39 (working-copy change created when 7d382043 landed at 23:21:08, content landed at committer time 23:28:27); §2 heading is at :48. WRONG section label: §2 → §1 (lines and substance correct).
9. "Preserve both receipt files unchanged" — `git log f10a320d..8d56809 -- …/evidence/c1-controls.txt …/parity-freeze.txt` = empty; c1-controls.txt byte-identical from fdf4371f (adds it) to tip; parity-freeze.txt byte-identical from fdf4371f to tip (fdf4371f appended three A1-parity lines below the mislabeled header; label line untouched; not a correction of the label). Matches.
10. "Round 34 carries the fix forward: every round-34 receipt's first line is date -u output (evidence/*.txt, c0/*.md, wave-A seat reports)" — at 8d56809 the committed tree holds five evidence/*.txt (c1-before, c1-controls, c1-posctl, c1-tool-provenance, census-start — all open "measured"/"written" + ISO UTC timestamp) and ten c0/*.md (all open "measured 2026-10-23T…Z"); wave-A reports uncommitted at 8d56809 (ls-tree wa/ = 0), checked in live working tree: all wa/*.md open "measured 2026-10-23T…Z". Notes: c1-after.txt and census-end.txt are later receipts (analysis/commit time, uncommitted at 8d56809); the phrase "date -u output" is loose (raw `date -u` prints "Thu Oct 23 07:… UTC", the ISO stamp is `date -u +%FT%TZ`), but every receipt carries a measured UTC ISO timestamp — substantively matches.
11. Append-only — `git diff f10a320d 8d56809 -- corpus/lessons/round-33.md` = 0 deletions, 50 insertions; additions begin at "## Round-34 corrections"; nothing above heading changed. Matches.

## Audit of /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/JudgeLessonItem7.md

The attempt-2 judge reached the same verdict-relevant substance; I agree with every factual claim it makes, except one anchor nit and its verdict label.

- Check 1 (spotcheck:240-241) — agree.
- Check 2 (c1-controls.txt:1) — agree.
- Check 3 (spotcheck §2:50-53, :52 dispatch 02:30:05.953Z) — agree.
- Check 4 (fdf4371f carries c1-controls.txt; %cI 02:39:02Z ≠ dispatch) — agree.
- Check 5 (parity-freeze.txt:1 02:3xZ) — agree.
- Check 6 (spotcheck §1:41-43, actual run 02:28:27Z) — agree.
- Check 7 (27969134's %cI 02:28:27Z = closure run time) — agree.
- Check 8 (mislabel: "§2, lines 37-39" should be §1) — agree with the mislabel finding; the report's own anchor "spotcheck:38-39" is one line loose (the phrase "the content landed at committer time 23:28:27" begins on line 39; lines 38-39 both carry the bullet). Substance agrees.
- Check 9 (receipts preserved; parity-freeze grew by three A1-parity lines at fdf4371f below the label) — agree.
- Check 10 (evidence/*.txt + c0/*.md committed at 8d56809; wave-A reports live-tree; five evidence files list correct for the commit) — agree.
- Check 11 (append-only: 0 deletions, 50 insertions, 211 → 261 lines) — agree.
- Check 12 (SOURCES diff 7d382043→89791013 = 17+, 6-; not applicable) — agree.
- VERDICT "repaired" — disagree. The judge itself records the §2/§1 mislabel as a wrong detail; under the rubric "not repaired (list each wrong detail)", a block containing a wrong factual detail is not repaired. The routed defect's substance is addressed and the mislabel is corrected in the attempt-2 lesson draft (corpus_lessons_round-34.md:119), so the remaining wrongness is confined to the committed Item-7 block at 8d56809.

The draft's correction at /fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:119 — "Item 7: read '(round-33-verifier-spotcheck.md §2, lines 37-39)' as '§1, lines 37-39'" — is accurate: it fixes exactly the one wrong detail found above (§1 correct for lines 37-39). The draft does not introduce new errors in this item.

## Findings

- VERDICT: not repaired. Wrong detail: §2 citation label at round-33.md:248 should be §1 (the cited lines 37-39 are in spotcheck §1; §2 starts at spotcheck:48).
- Item 7 fully answers routed §8 item 7; all receipt times, carrier commits, committer times and the append-only property verify.
- The attempt-2 draft correction (:119) is accurate and repairs the one wrong detail.

## Residual risk / verification gaps

- The "actual" times (02:30:05.953Z, 02:28:27Z) are transcribed from the closure's spotcheck; I did not re-derive them from driver logs. The block faithfully matches the closure's records.
- The wave-A seat-report half of claim 10 is verified against the live working tree (untracked), not committed bytes at 8d56809.
- No tools installed; git read-only in the lane (show, diff, log, ls-tree, rev-parse); no scratch files written.

AUDIT: agree 12 / disagree 1
