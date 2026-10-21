PARTIAL — round-20 trend verdicts are not yet in SCORECARD; the evidence supports one clear expansion advance, not a quality improvement, and the required lesson-recorded outside spot-check is absent.

## Proposed verdicts and attacks

### Expansion — proposed `improved`

There is **1 unambiguous qualifying new entry**: `knowledge/wave-settlement-r20.md` adds per-seat report settlement, a previously named FR3 frontier, and cites three mined rows (S068, S069, S071). The coverage map records this as a bounded FR3 advance. `knowledge/drift-repin-r20.md` cites two more mined rows (S066, S067) and adds a closed-class, evidence-per-token disposition of the live drift. The two new entries therefore cite **5 unique mined rows** in total. In the current S066–S072 gate/registry slice, the actual status histogram is **5 mined, 1 queued, 1 rejected**; S070 remains queued and is not cited by either new entry. Evidence: `corpus/README.md:397-402`; `corpus/knowledge/wave-settlement-r20.md:1-8`; `corpus/knowledge/drift-repin-r20.md:1-10,22-48`; `corpus/SOURCES.md:72-78`; `corpus/lessons/round-20.md:41-47`.

**Strongest counterargument:** do not automatically count the drift note as a second new-ground entry. The coverage map already held `knowledge/drift-pin-r10.md` as the census behavioral-baseline/re-pin note (`corpus/README.md:18`); that note already states a re-pin ritual (`drift-pin-r10.md:235-265`), and its round-12 erratum points to an earlier token-by-token drift classification (`drift-pin-r10.md:290-301`; `corpus/evidence/drift-r12-20261019T2204Z-classification.md:27-41`). The r20 closed-class/evidence-pointer discipline is a meaningful refinement, but the coverage map should identify that *specific* new sub-ground rather than relabeling the already-held general drift-pin ground. Thus the strict defensible count is 1; count 2 only if L1 makes the new classification sub-ground explicit. The one clear entry still supports `improved`.

### Quality — proposed `unchanged`

The lesson says the L1 reopened seven source URLs and quote-matched them, but reports no status/recheck/used-by changes to existing rows (`corpus/lessons/round-20.md:49-51`). That verifies the round's selected source quotations; it does not establish that an existing knowledge entry was reverified, deepened, or superseded without a failed re-check. QUALITY criterion 59 expressly rejects source-row volume or repairs alone as quality-trend evidence (`corpus/QUALITY.md:202-206`). Further, neither new knowledge entry has the `verified-at:` and `recheck:` fields specified by LEARNING (`knowledge/drift-repin-r20.md:1-10`; `knowledge/wave-settlement-r20.md:1-8`; `LEARNING.md:67-71`). This prevents a stronger freshness claim; it is not evidence that either entry is false or stale.

**Strongest counterargument:** the drift note materially deepens the older drift-pin note with per-token classes, a current baseline, and explicit comparator blind spots; the wave note combines independent-oracle results with historical live-ground-truth comparison and carefully states limits (`wave-settlement-r20.md:52-78`). That could support `improved` if L1 explicitly treats it as deepening/re-verification of the existing note and supplies the missing verification metadata. On the present record, the improvement is not demonstrated under the trend observable, so `unchanged` is safer than either `improved` or `harmed`.

### Discernment — proposed `unchanged` as filed

The round-20 `## Gate` records L1 decisions for admits S066–S071 and reject S072, but no outside `agree`/`disagree` result (`corpus/lessons/round-20.md:37-51`). LEARNING requires a non-author to check at least one admit and one reject and record reasons in the round's lesson (`LEARNING.md:40-48`). The Scorecard still ends at round 19 (`SCORECARD.md:1211-1231`), so there is no later round-20 trend entry to credit.

**Outside spot-check supplied by this critic (not yet recorded in the lesson):** agree with admitting S068: the Python 3.15 `os.stat` entry says it normally follows symlinks, while `os.lstat` does not (`https://docs.python.org/3/library/os.html#os.stat`, `#os.lstat`; local source row `corpus/SOURCES.md:74`). This is directly relevant to report-path safety. Agree with rejecting S072: the opened Wikipedia lead repeats the actual-behavior definition already supported by Feathers' coiner essay; the specific r20 claim gains no distinct support (`https://en.wikipedia.org/wiki/Characterization_test`; `corpus/SOURCES.md:73,78`; lesson Gate `:42,47`). This favorable counterargument to `unchanged` is recorded here, but does not satisfy the exact round record requirement while it remains outside the lesson.

## Smallest safe correction

1. Expansion: keep the strict count at one unless the coverage-map row names the precise newly held drift-classification ground distinct from the old re-pin coverage.
2. Quality: add `verified-at:` and a reproducible `recheck:` to both new entries; claim `improved` only if the cited older entry is explicitly deepened/rechecked and no check fails.
3. Discernment: append a named non-author's admit-and-reject spot-check, reasons, and `agree`/`disagree` outcomes to `corpus/lessons/round-20.md` under `## Gate`; then reassess the trend.

Evidence scope: read-only artifact/source review; no census, build, or test was run; no tools were installed.