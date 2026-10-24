# AuditPathSymlink — pre-implementation review

## Findings (severity ordered)

### Medium — ancestor/root symlinks are not covered by the available fixture; evaluator not yet available to verify enforcement

The contract requires provenance `path` values to refer to committed own-lane evidence copies (`.ufo/waves/round-21/contract.md:13-16`). The relevant candidate evaluator, `tools/mori-evidence-loss.py`, was absent from both the lane `tools/` listing and the isolated `ImplLoss/tools/` listing at inspection time, so this is a pre-implementation requirement gap, not a confirmed runtime defect.

The available fixture runner checks relative-path syntax only (`.scratch/round21/FixtureLoss/fixture-loss.py:109-114`) and its symlink mutation replaces the final `row-disposition.json` leaf with a symlink (`:221-232`). It does not exercise a symlink in an ancestor directory or a symlink supplied as `--root`.

Concrete counterexamples to cover:

1. **Ancestor symlink:** let `root/evidence` be a symlink to `root/real-evidence` (or to an external directory containing a byte-identical file), with `real-evidence/row.json` a regular file. Submit provenance path `evidence/row.json`. The final component is not a symlink, and resolving the path then checking only that it remains under `root` also accepts the in-root-link variant. This violates the requested rejection of symlink path components.
2. **Root symlink:** let `root-alias` be a symlink to the intended repository root and invoke the audit with `--root root-alias`. A check that first calls `Path(root).resolve()` erases the fact that the caller supplied a symlink, so it cannot implement root-symlink rejection.

**Smallest safe change:** before resolving or reading provenance, validate the supplied root and walk each provenance path component with `lstat` (including the final component); reject any symlink, require intermediate components to be directories and the final component to be a regular file. For root rejection, inspect the supplied root before canonicalization; if the policy excludes symlinked root ancestors too, apply the same component walk from an explicit absolute anchor. Add fixture cases for an ancestor link and a symlink root while retaining the existing final-leaf case.

**Race limitation:** `lstat`-then-`read_bytes` is still TOCTOU: a concurrent local actor can replace a checked component before it is opened. If that actor is in scope, use descriptor-relative traversal (`openat`/`dir_fd`, `O_NOFOLLOW` and `O_DIRECTORY` for ancestors, then read and hash the final opened descriptor) instead of a check followed by pathname reopening. Otherwise explicitly document that the component checks assume the tree is not concurrently mutated; do not claim race-free symlink rejection.

## Residual risk

No evaluator source was available to inspect, so actual acceptance/rejection behavior, error reporting, and any existing race mitigation remain unknown. The existing fixture's final-leaf symlink case is not evidence that ancestor or root symlinks are rejected.

## Verification gaps

- `xd://lsp` is not mounted (`No such tool`), so LSP status, references, definition, and diagnostics could not be queried. Literal grep was used only to locate relevant contract/fixture text; it is not semantic proof.
- No tests, builds, or production writes were performed, as requested.
- No tools were installed or updated.
