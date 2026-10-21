# F1 — `tampered_population_pin`

## Findings

None. Static trace of the integrated case matches the frozen CLI-exit expectation; no false-clean path or output leak is apparent.

## Evidence

- Frozen oracle: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-19/frozen/expected.json:13` requires exit `2`. Its `c1_required_finding` map at lines 15–20 does **not** specify a finding for this case.
- Harness input and invocation: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round19-regressions.py:366-387` constructs the synthetic population, changes the expected pin to 64 zeroes, and passes it via `--expected-sha256`. At lines 391–413, it compares the child exit to the frozen expected code, validates receipt metadata and leaks, and checks a finding only when the oracle lists one. Thus no unlisted finding requirement is being silently treated as oracle data.
- Actual CLI path: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-content-review.py:212-240` hashes the population file bytes, resolves the requested revision, compares that digest with the supplied pin, and on mismatch emits `CONTENT_REVIEW_POPULATION_PIN` before returning. The code is in `INVALID_CODES` at lines 24–34; `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-content-review.py:176-199` maps that finding to `could-not-evaluate` / exit `2`. `main` emits the result and returns the computed exit at lines 487–489.
- On this early failure path, population/review/script digests have already been recorded (`mori-content-review.py:143-163, 212-221`), and the resolved revision is recorded (`231-235`). The path adds no source path or review reason to the finding; the JSON emitter at lines 166–173, 339–340 serializes only the finding code and safe receipt fields. It returns before parsing review rows or reading population blobs.
- The tool's in-file synthetic selftest also specifies exit `2` and `CONTENT_REVIEW_POPULATION_PIN` for a pin mismatch (`mori-content-review.py:419-430, 448-455`); this is source evidence only, not an executed check.

## Residual risk

The frozen oracle does not pin the finding code for this case, so the round-19 harness will not catch a future change from `CONTENT_REVIEW_POPULATION_PIN` to another exit-2 finding, provided the other receipt checks still pass. That is not a contract mismatch for this assignment because the expected file lists no required finding for this case; no correction is required under the current oracle.

## Verification gaps

No harness, selftest, or other verification was run, as required. The `lsp` device was unavailable (`xd://lsp` returned “No such tool”); literal search was used only to locate the case, with conclusions based on direct source reads. The assigned integrated commit and the reviewed tool/oracle files had no later diff at the workspace tip.