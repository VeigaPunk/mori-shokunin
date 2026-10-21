# F1 — C1 `invalid_revision`

## Finding

- **Medium — false-clean receipt/disclosure validation bypass** — `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round19-regressions.py:402-413`.

The frozen oracle requires process exit 2 for this case (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-19/frozen/expected.json:12`). It does not list `invalid_revision` in `c1_required_finding` (`:15-20`), so the harness correctly cannot demand a frozen finding code. However, it also deliberately skips `c1_output_valid` for this case (`mori-round19-regressions.py:403-408`). It then accepts any parsed JSON object if the process returned 2 and the one hard-coded private sentinel is absent (`:391-413`; sentinel check at `:227-231`). A child returning `{}` with exit 2, or returning input reasons/content without that sentinel, therefore produces no issue and is recorded as `pass`. The case fixture uses the ordinary safe rows (`:338-367`), not the sentinel-bearing private-content row, so that leak check does not cover its input values.

The content tool's present path itself is consistent with the oracle: failed revision resolution adds `CONTENT_REVIEW_INVALID_REVISION` and returns (`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-content-review.py:223-235`); `finish` maps invalid findings to `could-not-evaluate`/2 (`:191-199`). It has already populated population/reviews digests (`:212-221`), leaves unresolved revision metadata null, and emits the result (`:339-341`, `:487-489`). Static inspection shows no reason/content echo on this path. The defect is that the harness cannot falsify missing receipt metadata or an untested value leak for this case.

**Required correction:** add an invalid-revision-specific receipt/disclosure assertion instead of skipping validation: require the allowed result shape, `could-not-evaluate` status and embedded exit code 2; check null unresolved revision plus matching population, reviews, and script digests; and reject review reasons/content in output. Do not add a required finding code unless the frozen oracle is amended to list one.

## Residual risk

A passing `invalid_revision` harness row is not evidence that the result contains the required metadata or honors the no-reasons/no-content output contract. The current content tool source appears to honor both; the harness gap allows a later regression to be reported clean.

## Verification gaps

No tests, smokes, or verification runs were executed (prohibited for this review). The `lsp` device is unavailable in this environment (`xd://lsp` reports only `ast_edit` and `debug` mounted); review used the exact source and oracle anchors, with no grep fallback. Read-only diff inspection confirmed these tool files are unchanged from integrated commit `367927c56eb1a00613e1fed65e5c47245fd570b9` to the checked-out revision.
