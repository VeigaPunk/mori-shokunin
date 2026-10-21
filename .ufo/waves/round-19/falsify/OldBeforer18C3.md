# C2 before-state rederivation: r18-C3

Axes checked: row verdict, correction scope, and historical-versus-prospective attribution.

## Finding

No actionable defect on this row. Expected for `r18-C3` at the retained before state: verdict `no-implementation`, effective label `pre-build`, overclaim `true`.

## Evidence and attribution

- The retained result records that classification for `r18-C3`; its before-state total is four overclaims. (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/evidence/c2-before.json:1`)
- The frozen rule makes absence of an implementation commit yield `no-implementation`, and counts a `pre-build` label with any other verdict as an overclaim. The `r18-C3` row declares `pre-build`. (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/frozen/c2-register.json:4-14,38-41`)
- The appended correction register targets only historical `r17-C3`; it does not relabel `r18-C3`. (`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/freeze-register.json:4-12`)
- The delivered checker maps corrections by claim ID, derives `no-implementation` when no implementation commit exists, and applies the frozen overclaim predicate. (`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:203-233,249-319,322-327`)

The before artifact's four are attributable as one historical `r17-C3` row plus the three prospective `r18-C1`–`r18-C3` rows; `r18-C3` is one of the prospective three, not a fourth historical defect. The later correction affects only the historical row, preserving that distinction and leaving the three prospective labels untouched.

## Residual risk and verification gaps

Static rederivation only; no checker execution or test was run, as required. An LSP device was unavailable (`read xd://lsp` returned “No such tool”; only `ast_edit` and `debug` were mounted), so no LSP status/references/definition/diagnostics were available. No grep result is used as semantic proof.