# r17-C3 after-state review

Axes: row result; correction application; historical/prospective attribution.

## Finding

### Medium — The row's exact oracle agreement drops the ruling's qualification

For this row, the expected after-state is `verdict=co-evolved`, `effective_label=co-evolved`, `overclaim=false`; the retained after record also marks no oracle disagreement (`.ufo/waves/round-18/evidence/c2-after.json:1`). This follows the frozen declared label and its single correction (`.ufo/waves/round-18/frozen/c2-register.json:24-29`; `corpus/evidence/freeze-register.json:5-11`): the checker applies the correction label over the declared label and tests overclaim against the effective label and verdict (`tools/mori-freeze-order.py:203-233,310-327`).

But the correction rationale characterizes the cited non-author ruling as partial, while the frozen outside-ruling field remains a single category. The checker compares only the computed verdict with that field (`tools/mori-freeze-order.py:310-318`), so the after row's no-disagreement result establishes agreement only with the encoded category; it does not preserve the partial qualification. Do not present this row as exact-category oracle agreement without representing that qualification.

## Attribution

Yes, the historical-versus-prospective separation is preserved in the retained after rows: the one r17-C3 correction changes that historical row's effective label, while r18-C1 through r18-C3 retain their prospective pre-build labels and pre-build verdicts (`.ufo/waves/round-18/evidence/c2-after.json:1`; `.ufo/waves/round-18/frozen/c2-register.json:24-41`). This is the one historical correction plus three prospective labels described by the round-19 contract, not four historical defects (`.ufo/waves/round-19/contract.md:7`).

## Residual risk and verification gaps

This review covers r17-C3 only. No checker execution or other verification was run, as required. The `lsp` device is unavailable (`read xd://lsp` returned “No such tool”), so no LSP status, references, definitions, or diagnostics were obtained. No grep result is used as semantic proof.