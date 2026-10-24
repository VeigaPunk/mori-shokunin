# C2 external-corrections binding review

## Finding

**Grounded match — no bypass found in this boundary.** In a provenance-bound invocation, the checker resolves the input path, requires its resolved location beneath `--repo`, and checks the loaded bytes against the Git blob at the resolved measured revision. An external path is refused through the input-revision-mismatch path; `_check` emits the safe error result and returns exit 2. Sources: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:125-151,361-388`; `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-19/frozen/provenance-refinement.json:5-11`.

The supplementary harness does exercise that path through an actual CLI subprocess: the fixture repo is a child of the sandbox root; the harness writes a separate copy of the already-used valid corrections JSON at the sandbox root, invokes the checker in bound mode with that path, and asserts exit 2. The invocation helper launches `sys.executable` via `subprocess.run`; this supplementary result is included in the harness regression counts. Sources: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round19-regressions.py:442-445,518-527,557-577,768-780,182-200,1056-1092`.

## Residual risk and verification gaps

The external-path assertion checks exit status and the synthetic sentinel-leak flag, but does not parse the emitted error classification. Thus it establishes the expected refusal status, not the precise refusal reason. No tests or runtime checks were run. The LSP device was unavailable (`read xd://lsp` reported no such tool; only `ast_edit` and `debug` were mounted), so semantic LSP references/definition/diagnostics were not available; scoped text search was used only to locate call sites, with source behavior reviewed from file reads.