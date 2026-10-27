# Mo57Reviewer06 — C2 counter attack

## Findings

**High — C2 can report eight located claims when the entry has no claim rows or located quotes.** In `.ufo/waves/round-57/count-c2.py`, line 11 counts every line beginning `| K`; line 13 treats the presence of any backtick as `quotes=ok` (the same test is duplicated, not a paired-delimiter or source-copy check); line 14 accepts the count and the mere substring `pairing count`. The counter does not enforce the contract's `source:`, `verified-at:`, and `recheck:` opening fields or establish that a quote occurs in a source copy. The contract requires all of those (`.ufo/waves/round-57/contract.md`, C2 predicate).

Reproducer: scratch fixture commit `d30fc7623fa635fb3ebc5be24378d78f4055989c`. Its entry omits all required opening fields, contains the contrary statement “`unclosed` is NOT a pairing count; it is a present-running count,” and has eight filler lines beginning `| K`, each with only one backtick; it has no quotes or source copy. Running the unmodified entry-tip counter against that fixture (using `GIT_DIR` to redirect its `git show`, without modifying the script or lane repo) produced:

`C2=met claims=8 source=ok quotes=ok rev=d30fc7623fa635fb3ebc5be24378d78f4055989c` (exit 0).

**High — `source=ok` does not establish a mined S548 source.** Counter line 12 checks only for `S548` anywhere in the entry, the literal `| S548 |` anywhere in the registry, and `mined` anywhere in that registry. It does not bind the mined status to S548 or verify that the row is a newly opened, relevant source. The same fixture registry marks S548 `queued`; its only `mined` substring is in `determined`. Nevertheless the counter reported `source=ok`. At the frozen entering revision, the real registry already has 271 occurrences of `mined` and no S548 row, so the global substring condition is especially non-discriminating (read-only check against `corpus/SOURCES.md` at `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`).

## Verification / verdict

The counter script on disk is byte-identical to the frozen `618562c72a03dc4d17386b715357f863fd327274` version. Running it against that real revision returned `C2=unmet claims=0 source=bad` (exit 1), consistent with the controls' entering-tip baseline. Fixture only was created and committed under `/fast/scratch/hyaku/mori-r57/Mo57Reviewer06/fixture`; no production changes or commits were made. The scratch fixture was removed before yielding.

**Verdict:** C2 counter has reproducible false positives for both located-claim completeness and a mined S548 source; counter output is not evidence that the frozen C2 predicate was met.
