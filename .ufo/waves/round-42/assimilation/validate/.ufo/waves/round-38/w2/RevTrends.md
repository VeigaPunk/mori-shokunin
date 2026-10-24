# Round 38 trend verdicts at `f725f3076972e6e70595b5ac8279be524a111ff8`

## Scope and provenance

Re-derived from a temporary shared clone checked out at the scored commit; the lane checkout was not used for execution. Expansion maps to coverage/adjacency, quality to depth/freshness/operability, and discernment to calibration (`corpus/evidence/sources-r35/S199.src:20-23`). No scalar score is assigned.

### Expansion — improved (bounded)

The entering-to-scored diff adds two new knowledge entries, the round-38 lesson, and the S226 source copy. `SOURCES.md` adds S226 and a round-38 search record, with no deletions or edits to existing registry rows (`scratch/RevTrends/expansion-diff.txt:1-7`; `scratch/RevTrends/sources-delta.txt:1-11`). S226 is explicitly admitted as mined in `corpus/lessons/round-38.md:5-19`, and its located realpath text is preserved at `corpus/evidence/sources-r38/S226.src:657-659`; the row opens `supersedes S069` (`corpus/SOURCES.md:232`).

The entries add distinct, evidenced coverage: the content-anchor entry names the round-37 token-only gap and cites S205/S221–S226 (`corpus/knowledge/source-drift-content-anchor-r38.md:3-8,12-18,20-43`); the containment entry grounds canonical-path resolution and the timed disposition of S069 (`corpus/knowledge/containment-timed-supersede-r38.md:3-8,13-29`). The new source and entries are therefore more than a row-count or index-only change.

**Counter-evidence/limit:** this is a narrow addition—one newly mined source and two entries, one extending the existing source-drift line. It does not establish broad new-domain coverage or independent validation.

**Receipts:** `scratch/RevTrends/expansion-diff.txt`; `scratch/RevTrends/sources-delta.txt`; `corpus/lessons/round-38.md:9-19`; `corpus/evidence/sources-r38/S226.src:657-659`.

### Quality — improved narrowly; not a blanket clean-recheck verdict

At the scored bytes, the C4 run exited 0: all four content checks passed, all three fabricated witnesses were rejected, and its named-row mutation was killed (`scratch/RevTrends/c4-at-f725.txt:1-12`). C5 exited 0 with all six checks passing (`scratch/RevTrends/c5-at-f725.txt:1-10`); its six-mutation selftest passed (`scratch/RevTrends/c5-selftest-with-rev.txt:1-9`). The append-only gate selftest passed 9/9 (`scratch/RevTrends/gate-selftest-at-f725.txt:1-3`). Using the actual entering tip as the round base, the timed gate exits 0, lists S069 in `superseded_as_of`, has `stale_supersede=[]`, and reports `round_changed=[]` (`scratch/RevTrends/gate-round38-base.txt:1-23`). This supports a real improvement in content binding, replayability, and timed supersede treatment. QUALITY 108–110 explicitly ground these checks in round-37 and round-38 lessons (`corpus/QUALITY.md:870-897`; `corpus/lessons/round-38.md:25-29`).

**Counter-evidence and limits:**

- The contract's `--round-base f10a320d` invocation exits 1 and reports 18 historical immutable-cell deviations plus `round_changed=[S182,S193]` (`scratch/RevTrends/gate-at-f725.txt:21-23`). That base spans earlier rounds: against the declared entering tip `e33bb561`, the round-local run has `round_changed=[]`; do not present the f10 result as a round-38 regression. The 18 historical deviations remain visible in the gate output.
- The committed `evidence/c4-after.txt` and `evidence/c5-after.txt` receipts name the earlier revision `daa1d4d2501e1671e7b7ff1fd60a069564f178b0` (`.ufo/waves/round-38/evidence/c4-after.txt:1`, `c5-after.txt:1`). That C5 receipt says `bounded_reads FAIL` and `CONFORM=unmet` (`c5-after.txt:6-9`); it is not evidence for f725. The round-38 `gate-after.txt`, `gate-selftest-after.txt`, and `c5-after-selftest.txt` are absent from f725 (`scratch/RevTrends/after-receipt-presence.txt:1-4`); the scratch receipts above are fresh reruns, not committed receipts.
- The documented `python3 .ufo/waves/round-38/conform.py --selftest` invocation failed with setup error/exit 2 (`scratch/RevTrends/c5-selftest-at-f725.txt:1-3`). Supplying the scored revision and clone paths passed all six mutations (`c5-selftest-with-rev.txt:1-9`). QUALITY 109's no-revision command form is therefore not reproducible as written (`corpus/QUALITY.md:881-888`).
- C4's `live_rows PASS` is a structural check of the inherited round-37 receipt, whose summary counts 10 drifted rows (`scratch/RevTrends/c4-at-f725.txt:7-8`); the entry itself says that this does not establish current live-body reachability (`corpus/knowledge/source-drift-content-anchor-r38.md:54-55`). No live source re-fetch was run here, so no claim is made that all external source rechecks are currently clean.

**Receipts:** `scratch/RevTrends/c4-at-f725.txt`; `scratch/RevTrends/c5-at-f725.txt`; `scratch/RevTrends/c5-selftest-with-rev.txt`; `scratch/RevTrends/gate-round38-base.txt`; `scratch/RevTrends/gate-selftest-at-f725.txt`.

### Discernment — unchanged

Round 38 admits S226 and records no new rejected candidate (`corpus/lessons/round-38.md:9-16`); the quality criteria are lesson-grounded, but those author-side gate decisions and selftests do not constitute an outside admit/reject spot-check. The scored commit has no `corpus/lessons/round-38-verifier-spotcheck.md` (`scratch/RevTrends/spotcheck-presence.txt:1-4`), and the round-38 lesson says the L1 held the planning walk and no planner role was dispatched (`corpus/lessons/round-38.md:30`). The r37 non-author closure is cited as the source of the erratum, not a round-38 review (`corpus/lessons/round-37-erratum.md:3-8`).

**Counter-evidence/limit:** prior outside feedback was incorporated into the new criteria, but no non-author round-38 verdict exists at the scored tip. Discernment must not be reported as improved on this record.

**Receipt:** `scratch/RevTrends/spotcheck-presence.txt:1-4`.

## Commands and touched surfaces

Executed against the temporary clone at f725:

- `git diff --name-status e33bb561712b32f46861362a3fa43762fa70ae4f f725f3076972e6e70595b5ac8279be524a111ff8 -- corpus/knowledge corpus/lessons/round-38.md corpus/SOURCES.md corpus/evidence/sources-r38/S226.src` — exit 0; additions listed above.
- `python3 .ufo/waves/round-38/count-c4.py f725f3076972e6e70595b5ac8279be524a111ff8` — `C4=met`, exit 0.
- `python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 --counter .ufo/waves/round-38/count-c1.py --counter .ufo/waves/round-38/count-c4.py` — `CONFORM=met`, exit 0.
- `python3 .ufo/waves/round-38/conform.py --selftest` — setup error, exit 2; rerun with the scored revision, `--repo`, `--contract`, and `--counter` — `CONFORM_SELFTEST pass=6 fail=0`, exit 0.
- `python3 tools/mori-sources-appendonly.py f725f3076972e6e70595b5ac8279be524a111ff8 --round-base e33bb561712b32f46861362a3fa43762fa70ae4f` — exit 0, `stale_supersede=[]`, `round_changed=[]`.
- `python3 tools/mori-sources-appendonly.py f725f3076972e6e70595b5ac8279be524a111ff8 --round-base f10a320d` — exit 1; inherited-base result described above.
- `python3 tools/mori-sources-appendonly.py --selftest` — `pass=9 fail=0`, exit 0.
- `git cat-file -e f725f3076972e6e70595b5ac8279be524a111ff8:corpus/lessons/round-38-verifier-spotcheck.md` — absent at the scored commit.

Only report authored: `.ufo/waves/round-38/w2/RevTrends.md`. Execution receipts were written under `.ufo/waves/round-38/scratch/RevTrends/`; no product code, judge, configuration, or committed evidence was edited. No tools were installed. No live source re-fetch, remediation, or independent review was performed.

Report: .ufo/waves/round-38/w2/RevTrends.md
