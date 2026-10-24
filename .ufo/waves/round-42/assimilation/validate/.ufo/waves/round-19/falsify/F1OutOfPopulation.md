# F1 — `out_of_population`

Axes: runtime rejection, regression-oracle strength, output privacy.

## Finding — Low: the regression harness can accept a contradictory clean receipt

`tools/mori-round19-regressions.py:392-413` compares the child process return code with the frozen expected code, then calls `c1_output_valid`; this case has no required finding in the frozen oracle (`.ufo/waves/round-19/frozen/expected.json:15-20`), so it performs no finding assertion. The validator at `tools/mori-round19-regressions.py:244-274` permits a missing status and never checks the result's `exit_code` or consistency between status, JSON exit code, and process return code. Thus a process returning the expected non-clean code with a well-shaped receipt claiming `clean`/zero can be marked passing. The fixture at `tools/mori-round19-regressions.py:356-363` also gives the extra row a benign reason, so the output-marker check at `:398` does not exercise a leak of that row's value.

**Required correction:** validate the JSON exit code against the child return code and reject a clean status for this failed case. Put a private sentinel in the out-of-population row's reason and retain the stdout/stderr leak assertion. Do not require a case-specific finding code unless the frozen oracle is updated to list one.

## Trace and residual risk

The frozen oracle pins exit 2 for this case (`.ufo/waves/round-19/frozen/expected.json:3-13`) and does not pin a finding code. The harness adds one otherwise well-formed extra review row (`tools/mori-round19-regressions.py:356-363`), using the same complete in-population reviews. The checker detects the unknown path, records `CONTENT_REVIEW_OUT_OF_POPULATION` without attaching the row path, and skips the row (`tools/mori-content-review.py:296-300`). That code belongs to the invalid set (`:24-34`), which `finish` maps to `could-not-evaluate`/2 (`:191-199`). The serialized result is JSON (`:339-341`); this branch does not serialize the extra row or its reason. Static tracing therefore found no current runtime false-clean or value leak for this input; the finding is limited to the harness's ability to catch a future contradictory receipt or path-specific value leak.

## Verification gaps

No runtime, test, or smoke was run, per assignment. The `xd://lsp` device is unavailable in this environment (the device lookup returned only `ast_edit` and `debug`); no LSP references/definition/diagnostics were available. Source review was static.