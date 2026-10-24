# AuditPathDotdot — scoped pre-implementation review

## Axes

- **Lexical validation:** reject every `..` component, including paths that normalize back inside `--root`.
- **Filesystem side effects:** reject such input before path resolution or filesystem metadata access.
- **Evidence scope:** distinguish the existing probe helper from the not-yet-present evaluator.

## High — resolve-before-check accepts lexical `..` in the existing helper pattern

Contract `.ufo/waves/round-21/contract.md:14` explicitly requires rejecting absolute/`..` paths. The directly relevant existing helper in `.ufo/waves/round-21/build/MutLostIdentity/probe-lost-identity.py:65-70` calls `resolve(strict=True)` at line 67, then checks containment and `is_file()` at line 68; it has no lexical `..` rejection.

**Concrete counterexample [INFERENCE from the cited code and existing fixture]:** with `root` set to the lane root, pass `.ufo/waves/round-21/frozen/../frozen/required.json`. The required fixture exists (`.ufo/waves/round-21/frozen/required.json`). `resolve(strict=True)` normalizes the `frozen/..` pair to that same in-root file, so the subsequent containment and regular-file checks accept it. The source helper is a probe, not the integrated evaluator; this demonstrates the exact unsafe ordering, not an observed failure of an evaluator.

The ordering also cannot guarantee **no stat escape** for an escaping `..` input: resolution happens before containment rejection, so path resolution can inspect components outside the root [INFERENCE]. No such path was executed.

**Smallest safe change for this requirement:** parse the supplied path and reject absolute paths and any `..` component before calling `resolve`, `stat`, `is_file`, or opening anything:

```python
relative = Path(value)
if relative.is_absolute() or ".." in relative.parts:
    raise ValueError("provenance path must be relative and contain no '..'")
path = (root / relative).resolve(strict=True)
```

This makes the forbidden lexical path fail without filesystem lookup. Keep the contract's symlink-component rejection explicit as well; final containment after `resolve()` alone does not establish that requirement.

## Scope and verification gaps

- The integrated target `tools/mori-evidence-loss.py` was absent: direct path discovery returned “Path not found”; the lane `tools/` listing likewise did not contain it. The corresponding path was also absent in `.scratch/round21/ImplLoss/tools/`. Therefore no evaluator defect or pass/fail result is claimed.
- No tests or commands exercising filesystem paths were run, per scope.
- LSP is unavailable in this tool session: `read xd://lsp` returned “No such tool.” Literal search was used only to locate the path helper; semantic evidence above is the direct source read at `probe-lost-identity.py:65-70`.

## Residual risk

Actual evaluator behavior remains unknown until the implementation exists. Before acceptance, verify that the integrated resolver rejects the counterexample before any filesystem metadata lookup; also verify symlink components independently as required by contract `:14`.
