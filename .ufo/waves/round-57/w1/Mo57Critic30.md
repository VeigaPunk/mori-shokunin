# C2 counter attack

**Counterexample.** The counter accepts exactly eight rows beginning `| K` when each has two backticks, without checking the quoted material against a source copy. It accepts S548 via marker strings alone: `S548` in the entry, `| S548 |` and `mined` in `corpus/SOURCES.md`. A fabricated S548 registry row marked mined plus eight arbitrary backtick-delimited claims and the phrase `pairing count` can therefore yield C2 met without a newly opened source or located quotes.

**Evidence.** `.ufo/waves/round-57/count-c2.py:8-16` reads only the entry and registry at the supplied revision; lines 13-15 implement the marker checks and eight-row count. The frozen predicate at `.ufo/waves/round-57/contract.md:7` additionally requires a newly opened source row and located quotes in the source copy. The current `corpus/SOURCES.md` header is line 5; search found no `| S548 |` entry. Round-56 watchdog copies are under `corpus/evidence/sources-r56/`.

**Impacted axis:** depth.

**Smallest safe correction:** Verify each claim quote against the committed source-copy bytes, and verify S548's registry metadata and copy/provenance rather than marker presence. Keep the frozen predicate unchanged.
