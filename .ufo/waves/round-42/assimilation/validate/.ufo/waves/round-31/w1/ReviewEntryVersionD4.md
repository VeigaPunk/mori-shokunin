# D4 independent review — earlyoom version reporting

## Findings by severity

No remaining actionable D4 defect found. The landed correction in commit `1d94055` changes the entry's version claim at `corpus/knowledge/earlyoom-invocation-scope-r30.md:53-58` and adds a correction record at `:141-150`. Its S159/S120 overlap is also handled: `:23-26` distinguishes S159 as the introduction of `Restart=always` from S120 as the v1.9.0 template carrying it; `corpus/SOURCES.md:126,165` support those separate roles.

## Exact behavior and corrected sentence

`earlyoom.version` starts as `None` (`tools/mori-oom-killers.py:360`), is assigned from the capture group of each scoped message matching `RE_VERSION` (`:101`, `:389-396`), and is emitted as `earlyoom.version` (`:514-519`). Therefore the last matching message encountered in `scoped` supplies the value; no matching scoped message means `null`. For a bounded scope, only records with numeric monotonic timestamps at or after the retained stamp enter `scoped` (`:304-321`); records without numeric timestamps are excluded (`:312-319`). For an active unit with a missing or zero stamp, only placeable records are considered and the scope is trimmed to the last version line (`:281-303`). When `ActiveState` is present and the stamp is non-zero, the bounded filter applies and preserves the version for non-active states too (`:304-321`, `:442-449`); when the stamp is absent or zero on a non-active state, no scope branch supplies records. A failed journal read leaves the version null (`:450-453`). Grammar is `verified-1.9.0` only when the reported version equals `1.9.0`; otherwise it is `unverified` (`:430-431`).

Suggested precise replacement sentence for the D4 clause:

> For a non-active unit with a readable `ActiveState` and a retained non-zero `ActiveEnterTimestampMonotonic`, the reader considers only journal records with a numeric `__MONOTONIC_TIMESTAMP` greater than or equal to that stamp; `earlyoom.version` is the captured `\S+` token from the last in-scope message matching `^earlyoom\s+(\S+)` after leading whitespace is stripped, or `null` if none exists.

Evidence of a version line that is not reported: committed fixture `tools/fixtures/mori-oom-killers/cases.json:102,105` sets the active-enter stamp to `19964362` and contains `earlyoom 1.9.0` at `19964361`, one microsecond before it. I copied the committed tool to `/tmp/mori-r31-d4/mori-oom-killers.py` (SHA-256 matched the repository copy: `9c88ef272dbe3e07eb87e40f10faaedb82584df0d9f21e78e3d8764400da0fe1`) and extracted that fixture's `inputs` object. Run:

```text
timeout 30 python3 -I -B /tmp/mori-r31-d4/mori-oom-killers.py --inputs /tmp/mori-r31-d4/c04.inputs.json
```

Observed JSON fields: `earlyoom.version: null`, `earlyoom.grammar: "unverified"`, `earlyoom.scope_complete: false`, verdict `KILLER_ACTED`; exit status `1`. This follows the inclusive `stamp >= aetm` filter at `tools/mori-oom-killers.py:320`: the earlier version line is outside the scanned scope. The `c05-incomplete-scope-without-action` fixture run likewise returned `version: null` and exit `2`.

I checked all current `version` mentions in the entry. The other references are source/recheck notes, upstream startup or invocation-boundary statements, and fixture/table/limit descriptions (`:1,3,21-26,42-43,67-68,80,87,106,123`); none claims that the reader always reports a version. The reader-output claim was the corrected clause at `:53-56`, with its correction record at `:143-150`.

## Residual risk

A version line whose journal record has no numeric monotonic timestamp cannot enter a bounded scope and is not reported; the reader marks such a record unplaced (`tools/mori-oom-killers.py:312-319`). This is an explicit input limitation, not an unreported positive result. No live host or journal behavior was tested.

## Verification gaps

- LSP was unavailable: `read xd://lsp` returned “No such tool” and listed only `ast_edit` and `debug` as mounted devices. Thus no LSP status, references, definition, or diagnostics checks were possible. Text search located mentions; semantic conclusions above come from source reads and the fixture run.
- Ran the `c04` and `c05` fixture inputs (and the `a2-05-monotonic-zero-inactive-quiet` fixture input) through the `/tmp` copy. No full self-test suite or live mode was run.
- No tool was installed or updated.
