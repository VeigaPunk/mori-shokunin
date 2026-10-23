measured 2026-10-23T07:44:04Z

# GateS192 — wave-B attack on the attempt-2 S192 Gate row and registry row (seat MoriR34A3.GateS192)

Objects: Gate row `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:17`; draft registry row
`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_SOURCES.md:198`; committed copy
`corpus/evidence/sources-r34/S192.src` at `fd2521351c6cef47384aef30afbe1e4db7e6912e` (read via `git show`, never touched).
Independence: sections 1–3 were decided from the bytes before `.ufo/waves/round-34/wa/ReopenS192.md` was opened.

## 1. Live fetch vs committed copy

`date -u` at fetch: 2026-10-23T07:40:58Z. `curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/block/holder.c`
→ sha256 `1e41cc5cde74b89d10269351383426aef2d22dd7018fbc89ad63952562153a91`, 3921 bytes, 156 lines
(scratch `/fast/scratch/hyaku/mori-r34/a3-GateS192/S192.live`). `git show fd2521351:corpus/evidence/sources-r34/S192.src
| sha256sum` → `1e41cc5c…53a91`, identical 156/3921. Live bytes equal the committed copy byte-for-byte; the Gate row's
sha256 cell is correct.

## 2. Gate-row quotes re-located in the copy (whitespace runs collapsed)

| locator | quote | contiguous? | declared words | actual tokens | `"`/`|` |
|---|---|---|---|---|---|
| `S192.src:41` | "This functions creates the following sysfs symlinks." | yes, line 41 verbatim | 7 | 7 | none |
| `S192.src:46` | "For example, if /dev/dm-0 maps to /dev/sda" | yes, contiguous prefix of line 46 | 7 | 7 | none |
| `S192.src:49-50` | "/sys/block/dm-0/slaves/sda --> /sys/block/sda" | yes, all of line 49 (after ` * ` collapse) | 3 | 3 | none |
| `S192.src:147` | "if (!WARN_ON_ONCE(holder == NULL) && !--holder->refcnt) {" | yes, line 147 verbatim | 7 | 7 | none |

All four pass 3–25 tokens, contiguous at the locator, no `"` or `|`. Note: quote 3 lives wholly on line 49; the
`:49-50` locator is one line wider than needed — a nit, not a rule break (rejects were for non-contiguity, quotes or
word count, per lesson lines 29–32). Token counting treats `-->` and `--holder->refcnt` as words, consistent with the
round-33 convention (a `disk_name(…)` symbol-heavy quote was counted likewise). URL and accessed cells match the row's
claim; decision `admit, A, mined` is consistent with the registry cells.

## 3. Draft registry row, cell by cell

Row: `| S192 | … holder.c … | code | A | the v7.2 holder/slave sysfs symlinks between a stacking disk and the device it claims | block/holder.c:34-54,128-153; tag v7.2 | bd_link_disk_holder creates sysfs symlinks; for dm-0 mapping sda, /sys/block/dm-0/slaves/sda and /sys/block/sda/holders/dm-0; bd_unlink_disk_holder deletes both when the holder count reaches zero. lane rule: a non-empty `slaves` directory marks a stacked device (tool rule R3). | mined | 2026-10-23 | on-release | tools/mori-disk-rate.py |`

- Anchor `34-54`: kernel-doc block of `bd_link_disk_holder` (S192.src:34-61). It states the symlink creation (line 41,
  directions at 43-44, example 46-50) — the cited statement holds there. The `add_symlink` calls themselves are lines
  105 and 108, outside the anchor; acceptable only because the anchor cites the documenting comment. Nit, not a defect.
- Anchor `128-153`: doc + body of `bd_unlink_disk_holder` (function spans 128-155). `del_symlink` calls at 148-149 are
  inside, guarded by `!--holder->refcnt` at 147. Holds.
- `tag v7.2`: fetch path verified (section 1).
- Teaches clause 1 (creates sysfs symlinks): supported — S192.src:41 located above; the two `add_symlink` calls at
  105/108 execute it.
- Teaches clause 2 (dm-0→sda example, both directions): supported — S192.src:46, 49, 50 located above.
- Teaches clause 3 (bd_unlink deletes both at refcnt zero): supported — S192.src:147 decrements refcnt and tests zero;
  148 `del_symlink(disk->slave_dir, …)` (the slaves link) and 149 `del_symlink(holder->holder_dir, …)` (the holders
  link) run only under it.
- `lane rule:` clause: exempt from copy-support. Consistent with the tool: `tools/mori-disk-rate.py:41-45` (R3 doc,
  "non-empty ``slaves`` directory -> ``stacked`` (S192 …)") and `:194-196` (`os.path.isdir(slaves) and
  os.listdir(slaves)` → `"stacked"`). SKILL.md:832 and :834 cite S192 the same way.
- used-by `tools/mori-disk-rate.py`: `git cat-file -e fd2521351:tools/mori-disk-rate.py` → exists. The draft row's
  only change vs tip (`attempt2-tracked.diff:124,132`) is used-by `tools/mori-disk-rate.py; SKILL.md Round34` →
  `tools/mori-disk-rate.py`, matching the lesson's census-E11/M6 single-path fix (`corpus_lessons_round-34.md:44-45`);
  SKILL.md does cite S192, so the single-path choice is a documented trade-off, not an error.
- status `mined`, tier `A`, opened `2026-10-23`, recheck `on-release`: all correct.

## 4. Audit of .ufo/waves/round-34/wa/ReopenS192.md

Claims the round would cite, each vs my evidence:
1. agree — row located at corpus/SOURCES.md:198; verified also at `8d56809:corpus/SOURCES.md:198` (same text).
2. agree — two fetches 05:38:46Z, sha `1e41cc5c…`, identical to committed copy (my 07:40:58Z fetch gives the same
   sha; the seat's scratch files are unverified but its sha claim matches observed bytes).
3. agree — copy is 3921 bytes and hash-identical at the pinned rev (`git show` output above).
4. agree — S192.src:34-54 is the `bd_link_disk_holder` kernel-doc; lines 35/41/43-44/46-50 content as described.
   (Its phrase "holds the cited code" is loose for a comment block — the `add_symlink` code is lines 105/108 — but
   every quoted element sits in the range.)
5. agree — S192.src:128-153 covers `bd_unlink_disk_holder` doc+body; `del_symlink` at 148-149 under refcnt-zero at 147.
6. agree — scope cell supported; its located quote S192.src:35 is verbatim and 10 words as labelled.
7. agree — clause 1 supported; S192.src:41 quote verbatim, 7 words as labelled.
8. disagree — clause 2 quote S192.src:46 labelled "(12 words)": actual quote "For example, if /dev/dm-0 maps to
   /dev/sda and disk" is 9 tokens; text/location correct, count wrong.
9. disagree — clause 3 quotes S192.src:49/50 each labelled "(5 tokens)": each is 3 tokens.
10. disagree — clause 4 counts wrong: ":147 (6 tokens)" is 7; ":148-149 (8 tokens)" is 4 (locator covers both
    `del_symlink` statements, which do sit at 148-149).
11. agree — `lane rule:` clause exempt; consistent with tool R3 and SKILL.md.
12. agree — no clause unsupported; no `"` or `|` in quoted passages (verified across the copy for the used quotes).
13. agree — verdict `VERDICT: admit` matches my independent verdict (admission is the orchestrator's call; this is a
    recommendation only).
14. agree — tooling record "no tool installed": no contrary evidence; I also installed nothing (RULES.md requirement
    noted; existing curl/git/python used; pacman untouched per the pause).

AUDIT: agree 11 / disagree 3

## 5. Findings and verdict

No defect in the row cells. Residual risks: (a) the `:49-50` locator on a line-49 quote; (b) the 34-54 anchor covers
the documenting comment rather than the `add_symlink` call sites at 105/108; (c) the seat report's internal word/token
labels are off on three of its quotes — cosmetic, since the landed Gate row's own counts are correct. If the L1
prefers tighter rows, optional edits: locator `S192.src:49` and anchor `block/holder.c:34-54,105-110,128-153`.
No cell needs changing for admission.

VERDICT: admit
