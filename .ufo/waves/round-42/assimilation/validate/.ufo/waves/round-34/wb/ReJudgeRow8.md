measured 2026-10-23T07:47:59Z
# ReJudgeRow8 — independent re-judgment of the "Row 8 correction" paragraph

Object: `corpus/knowledge/disk-write-rate-r33.md:81-88` at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3
(routed defect: `corpus/lessons/round-33-verifier-spotcheck.md` §8 item 3 — "Row 8 still teaches the ABI
file's '4.18+' discard boundary, which v4.18 code contradicts (w2 AttackRow08). Mark it in the entry.")

## Independent verification (before reading the attempt-2 report)

- S187.src (committed at 8d56809, sha256 0f2ffdc7…dd3b7): lines 26-27 hold exactly the quoted sentence
  "Kernel 4.18+ appends four more fields for discard / tracking putting the total at 18" (grep -n 'Kernel').
- S197.src = block/genhd.c tag v4.18 (sha256 96b56381…748b, verified byte-equal to live upstream fetch,
  same hash). `diskstats_show` at :1313; its seq_printf at :1336-1351. My script counted the format
  conversions at :1336-1337: `%4d %7d %s %lu %lu %lu %u %lu %lu %lu %u %u %u %u\n` = **14 conversions**,
  and 14 arguments (:1338-1350), last `jiffies_to_msecs(part_stat_read(hd, time_in_queue))` at :1350; no
  STAT_DISCARD argument anywhere in the call.
- S198.src = block/genhd.c tag v4.19 (sha256 4c55aeba…588f1, byte-equal to live upstream, same hash).
  Same function, seq_printf at :1336-1358: format at :1336-1340 =
  `%4d %7d %s %lu %lu %lu %u %lu %lu %lu %u %u %u %u %lu %lu %lu %u\n` = **18 conversions**, 18 arguments
  (:1341-1357); last four (:1354-1357) are `ios[STAT_DISCARD]`, `merges[STAT_DISCARD]`,
  `sectors[STAT_DISCARD]`, `(unsigned int)part_stat_read_msecs(hd, STAT_DISCARD)`.
- So the paragraph's field counts (14 at v4.18, 18 at v4.19) and its v4.19 boundary **follow directly**
  from the cited copies: one conversion per printed field; discard values first appear in the v4.19
  printer, not v4.18's.
- On the "lane rule" question: the correction paragraph itself never uses the words "lane rule". The
  label appears in `corpus/SOURCES.md:204` (S198 teaches-cell: "lane rule: with S197, the printer first
  carries discard values at v4.19, not v4.18"). No source states the boundary verbatim — S198's bytes
  show only the v4.19 format — so the SOURCES cell correctly flags it as a lane rule derived from two
  sources. The derivation is sound (v4.18 lacks the fields; v4.19 has them; v4.19 is the immediate
  release after v4.18; both copies are tag-pinned and byte-exact). No defect in the labelling.
- Caveat (locator, not fact): the paragraph's Gate pointer `corpus/lessons/round-34.md` resolves in the
  live working tree but the file is absent from the judged tree 8d56809 and from lane tip fd2521351
  (`git ls-tree` empty both; `git status` shows `??`). Untracked attempt-2 draft.

## Per-sentence verdicts (paragraph sentences in order)

1. Header: "Row 8 correction — discard release boundary (append-only; spot-check §8 item 3)." —
   VERDICT: supported. Spot-check §8 item 3 routes exactly this defect; the revision block is appended,
   rows above untouched (file :77-88).
2. "Row 8 repeats the ABI file's 'Kernel 4.18+ appends four more fields for discard tracking putting the
   total at 18' (S187.src:26-27)" — VERDICT: supported. Row 8 (entry :27) restates it; quote is verbatim
   at S187.src:26-27.
3. "but the tag-pinned printer code contradicts the 4.18 boundary" — VERDICT: supported. S197.src is the
   byte-exact v4.18 tag blob and prints no discard values.
4. "the v4.18 diskstats_show format has 14 conversions and its argument list ends after time_in_queue
   (S197.src:1336-1351)" — VERDICT: supported. Counted 14 conversions, 14 args, last arg `time_in_queue`
   at :1350; range covers the whole call.
5. "while the v4.19 format has 18 conversions with four STAT_DISCARD values last (S198.src:1336-1358)" —
   VERDICT: supported. Counted 18 conversions; the four STAT_DISCARD args are the last four (:1354-1357);
   range covers the call.
6. "Read the ABI file's '4.18+' as a documentation error: v4.18 prints 14 fields and v4.19 prints 18." —
   VERDICT: supported. Follows from 4+5; "documentation error" is a flagged interpretation consistent
   with the contradiction and marked as guidance ("Read … as"), not as a sourced quote.
7. "Row 8's parsing rule (accept 14, 18 or 20 fields; sectors written is field 10) and its 'not
   exported, never zero' verdict stand; this correction does not re-check the 5.5+ flush boundary." —
   VERDICT: supported. Matches row 8's verdict cell verbatim (entry :27); paragraph makes no flush claim.
8. "Sources S197 and S198 were opened in round 34 (Gate: corpus/lessons/round-34.md)." —
   VERDICT: supported, with a dangling-locator defect. The factual claim holds: SOURCES.md:203-204 record
   both as `mined`/`on-release`, opened 2026-10-23 (round 34), and committed at 8d56809. The cited Gate
   file does not exist at 8d56809 or fd2521351 (untracked draft only) — the pointer, not the fact, fails.

Overall paragraph verdict: VERDICT: supported — every factual sentence reproduces from the cited bytes;
one locator defect (Gate file uncommitted at the judged revision) and the "lane rule" label in
SOURCES.md:204 is correctly applied to a two-source derivation, not asserted as sourced text.

## Audit of .ufo/waves/round-34/wa/JudgeRow8Correction.md

Claims checked against my own byte-level verification:
1. Paragraph at :81-88; cited ranges S187:26-27, S197:1336-1351, S198:1336-1358 — agree (my line checks
   match exactly).
2. S197 fmt :1336-1337 = "%4d %7d %s %lu %lu %lu %u %lu %lu %lu %u %u %u %u\n", 14 conversions —
   agree (my script counted the identical string, 14).
3. S198 fmt :1336-1340 = 18 conversions — agree.
4. S197 last arg `time_in_queue` at :1350, closes :1351; S198 last four :1354-1357 = ios/merges/
   sectors/msecs STAT_DISCARD, closes :1358 — agree.
5. sha256 values for S197/S198/S187 — agree (recomputed: 96b56381…, 4c55aeba…, 0f2ffdc7…); S197/S198
   byte-equality to upstream v4.18/v4.19 confirmed by my own live fetch returning identical hashes.
   (v7.2 procfs-diskstats fetch returned empty/404, so the S187 upstream-equality claim is
   uncontradicted but unverified by me [INFERENCE]; the quote was verified in the committed copy.)
6. Verdicts 1-6 each "supported" — agree, matching my verdicts 1-7 above.
7. Claim: `corpus/lessons/round-34.md` absent at 8d56809 and at fd2521351 — agree (ls-tree empty both;
   untracked in working tree).
8. Verdict 7 "unsupported at this revision" — agree as a verdict on the Gate pointer; I split it:
   the "opened in round 34" fact itself is supported by SOURCES.md:203-204.
9. Finding "no defect in claims 1-6"; dangling Gate pointer is minor — agree (I rate it the same: the
   sole defect, and locator-level).
10. Residuals: 5.5+ boundary out of scope; live fetches match committed hashes — agree (I reproduced
    both fetch hashes).
AUDIT: agree 10 / disagree 0

Tooling: none installed or updated (all checks used git/python3/curl already present). No lane writes
beyond this report; scratch only /tmp copies of the two .src files (outside the lane repo).
