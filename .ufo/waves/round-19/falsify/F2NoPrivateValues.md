# F2NoPrivateValues — C2 static falsification

Scope: integrated commit `367927c56eb1a00613e1fed65e5c47245fd570b9`; C2 only. Static review; no tests, smokes, or other verification runs.

## Findings

### P2 — Legacy unbound metadata can be absent or wrong without failing C2

In the integrated harness, `same_verdicts_as_base` compares claim verdict maps, and `no_private_values` scans captured bytes for the one canary. Neither inspects the legacy result's `provenance` object. The frozen expected list names these checks but has no separate legacy-status assertion. A counterexample tool can return the expected legacy verdicts while omitting `provenance` or falsely labeling that legacy invocation as bound; the bound invocation and its metadata can remain correct, and these C2 checks still pass. The CLI contract requires a legacy invocation to be explicitly unbound; the current tool emits that field, but the integrated harness does not protect it.

Evidence (path:line/class):
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round19-regressions.py:703-714/legacy-provenance-not-asserted`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-19/frozen/expected.json:22-34/no-legacy-status-assertion`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-19/contract.md:11/legacy-must-be-unbound`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:397-405/actual-status-field`

### P2 — The privacy canary does not cover values in emitted label fields

The assertion checks only whether the exact canary bytes occur in stdout or stderr. Its fixture places that canary in an extra claim field, while the freeze tool accepts any string for `declared` or a correction label and copies the effective label into each result row. Consequently, private text in an emitted label field (including a different value from the canary) is echoed by the CLI and does not make `no_private_values` fail. This is a concrete false acceptance for the assertion's broad name; it also reaches early result paths because `effective_label` is populated before revision-resolution returns.

Evidence (path:line/class):
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round19-regressions.py:227-231/exact-canary-only`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round19-regressions.py:487-491/canary-only-in-extra-field`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:185-194/unrestricted-declared-string`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:223-232/unrestricted-correction-label`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:252-260/effective-label-in-result`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:345-347/json-output`

## Residual risk and verification gaps

- `expected.json` pins the presence and order of C2 check names; the harness implements the `no_private_values` semantics itself rather than checking an expected value for that assertion. Bound-receipt fields are independently checked; missing bound metadata is classified absent and causes the after-mode summary to fail. The gaps above are specifically legacy provenance and input-derived emitted labels.
- LSP was unavailable: `read xd://lsp` returned no such tool; only `ast_edit` and `debug` devices were mounted. Source inspection used line reads and the read-only diff; no semantic LSP result is claimed.
- No tests, smokes, linters, or runtime checks were run, per assignment restrictions.
