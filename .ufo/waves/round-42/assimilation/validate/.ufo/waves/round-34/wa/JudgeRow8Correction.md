measured 2026-10-23T05:39:44Z
# JudgeRow8Correction — Row 8 correction paragraph (disk-write-rate-r33.md @ 8d56809)

Scope: judge every factual sentence of the "Row 8 correction" paragraph (corpus/knowledge/disk-write-rate-r33.md:81-88 at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3) against the cited copies (sources-r33/S187.src:26-27; sources-r34/S197.src:1336-1351; sources-r34/S198.src:1336-1358). Counts and argument-list tails were re-derived from the committed copies (`git show 8d56809:...`), not taken from the text.

## Verification performed

- Dumped the three cited copies at 8d56809 to scratch and read the cited ranges directly.
- Re-counted format conversions by script and by hand over the fmt strings:
  - S197.src lines 1336-1337: `%4d %7d %s %lu %lu %lu %u %lu %lu %lu %u %u %u %u\n` → **14 conversions**.
  - S198.src lines 1336-1340: `%4d %7d %s %lu %lu %lu %u %lu %lu %lu %u %u %u %u %lu %lu %lu %u\n` → **18 conversions**.
- Argument lists: S197 has 14 args, last = `jiffies_to_msecs(part_stat_read(hd, time_in_queue))` (line 1350; call closes at 1351). S198 has 18 args, last four (lines 1354-1357) = `ios[STAT_DISCARD]`, `merges[STAT_DISCARD]`, `sectors[STAT_DISCARD]`, `(unsigned int)part_stat_read_msecs(hd, STAT_DISCARD)`; call closes at 1358.
- Provenance (tag-pinned) byte-exact vs live upstream fetches:
  - sha256(S197.src)=96b5638180eb70886195b46722681623301c328763b47c674a6543b27c3e748b = `https://raw.githubusercontent.com/torvalds/linux/v4.18/block/genhd.c`.
  - sha256(S198.src)=4c55aeba02bfaecee8ef5a20514f834f2aa34a338f51a66a83bcc40d5a7588f1 = `https://raw.githubusercontent.com/torvalds/linux/v4.19/block/genhd.c`.
  - sha256(S187.src)=0f2ffdc724e0a666c54aa3b1f1e94f93ce6b76745827d301dd164d789bbdd3b7 = `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/procfs-diskstats`; lines 26-27 hold the quoted sentence.

## Per-sentence verdicts

1. "Row 8 repeats the ABI file's 'Kernel 4.18+ appends four more fields for discard tracking putting the total at 18' (S187.src:26-27)" — VERDICT: supported. Entry row 8 (disk-write-rate-r33.md:27) states "kernels 4.18 and later append four discard fields for a total of 18"; S187.src:26-27 contains the exact quoted sentence.
2. "the tag-pinned printer code contradicts the 4.18 boundary" — VERDICT: supported. S197.src is byte-identical to the v4.18 tag blob and its `diskstats_show` prints no discard values (14 conversions).
3. "the v4.18 diskstats_show format has 14 conversions and its argument list ends after time_in_queue (S197.src:1336-1351)" — VERDICT: supported. Counted 14 conversions; last argument is `time_in_queue` (line 1350).
4. "while the v4.19 format has 18 conversions with four STAT_DISCARD values last (S198.src:1336-1358)" — VERDICT: supported. Counted 18 conversions; the four STAT_DISCARD args (ios, merges, sectors, msecs) are last (lines 1354-1357).
5. "Read the ABI file's '4.18+' as a documentation error: v4.18 prints 14 fields and v4.19 prints 18." — VERDICT: supported. Follows directly: one conversion per printed field — 14 in v4.18, 18 in v4.19 — so S187's "4.18+" attribution is contradicted by the pinned code.
6. "Row 8's parsing rule (accept 14, 18 or 20 fields; sectors written is field 10) and its 'not exported, never zero' verdict stand; this correction does not re-check the 5.5+ flush boundary." — VERDICT: supported. Matches the row-8 verdict cell (entry line 27: "Accept a line of 14, 18 or 20 fields and read sectors written as field 10 in each; report missing discard or flush fields as not exported by that kernel, never as zero"); the paragraph adds no flush-boundary claim.
7. "Sources S197 and S198 were opened in round 34 (Gate: corpus/lessons/round-34.md)." — VERDICT: unsupported at this revision. `corpus/lessons/round-34.md` does not exist at 8d56809 (`git ls-tree 8d56809 corpus/lessons/` lists only up to round-33) nor at HEAD fd2521351. SOURCES rows S197/S198 (SOURCES.md:203-204) do record mined / on-release entry, so "opened in round 34" has partial support, but the named Gate file dangles.

## Findings (by severity)

- No defect found in claims 1-6: the conversion counts, argument-list tails, and the 14-vs-18 conclusion all reproduce from the cited copies.
- Minor: dangling Gate pointer (claim 7) — cites a file absent from both 8d56809 and current HEAD. If intended as a forward reference to the round-closing lesson, it cannot be checked at this revision.

## Residual risk / verification gaps

- The v5.5+ flush boundary was not re-checked (explicitly declared out of scope by the paragraph itself).
- Live fetches were done at review time (2026-10-23T05:39Z); they match the committed hashes.
- No tools installed/updated; no lane writes beyond this report.
