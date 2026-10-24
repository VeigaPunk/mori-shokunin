# C2 provenance critique

## Axes

Calibration (C2): measured-revision provenance and historical-versus-prospective attribution. No other axis is assessed.

## Findings

1. **Measured revision is not bound to measured inputs (fixable contract gap).** Counterexample: the checker accepts a valid `--rev` for repository `R`, while `--register` or `--corrections` names an external file or a dirty working-tree copy whose bytes differ from the corresponding blobs at that revision. The proposed receipt can still report that revision and the hashes of the bytes it actually loaded. A script hash and argv establish separate identities, but do not prove those input bytes came from the measured tree; likewise, the current loader reads the supplied paths directly, while revision checks are used for the chronology calculation. **Failure condition:** a provenance-capable clean receipt is emitted although a loaded register/corrections digest does not match its `REV:path` blob (or the path cannot be tied to that tree). **Smallest safe correction:** define the source relationship. Require repository-relative register/corrections paths and load their bytes from `REV:path` once for both hashing and parsing, or compare the once-loaded bytes to those blobs and return could-not-evaluate on mismatch. Specify `script_sha256` as the identity of the executed checker, independently of the measured tree; if the script is also claimed to belong to that tree, require the corresponding blob match too.

   Evidence: `.ufo/waves/round-19/contract.md:11` (provenance linkage gap); `tools/mori-freeze-order.py:105-125,157-160` (direct-file loading); `tools/mori-freeze-order.py:215-249` (revision use in chronology). Class: provenance/source-binding gap.

2. **Historical/prospective split is not an asserted outcome (fixable oracle gap).** R18 records that the aggregate 4-to-0 includes one historical correction and three prospective labels, not four historical defects, and explicitly routes that distinction. R19 says the frozen assertions distinguish the split, but the C2 check list asserts metadata, input consistency and unchanged verdicts only; it contains no assertion for historical-correction versus prospective-label counts/classes. A harness can therefore pass its listed checks while retaining or reporting the aggregate as four historical defects. **Smallest safe correction:** freeze structured expected outcomes for the one historical correction and three prospective labels, and check that separation; keep any aggregate 4-to-0 only as a separately identified compatibility statistic.

   Evidence: `corpus/lessons/round-18-verifier-spotcheck.md:90-94,177-179` (required split); `.ufo/waves/round-19/contract.md:7` (asserted distinction); `.ufo/waves/round-19/frozen/expected.json:22-35` (no split assertion). Class: calibration-classification/oracle gap.

## Review boundary

This is a static critique only. No code was changed and no tests, builds, or executions were run.
