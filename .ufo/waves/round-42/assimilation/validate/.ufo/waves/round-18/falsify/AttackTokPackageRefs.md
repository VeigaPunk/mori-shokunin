# AttackTokPackageRefs — wave-2 falsification

## Findings

### High — Pacman transaction report retains joined operator identity/path context

The `R4` personal-document-path token was removed from the changed line, but the same evidence continues across `build/PacmanTxnToday.md:119-120`: line 119 retains one account-identity value; line 120 retains two home-path values from the PWD split. These remain joined to the host-log attribution. This is out-of-metric personal-identity/private-context exposure not caught by frozen C1 classes R1–R9 (all zero on lines 117–122), not a clean redaction. Evidence-minimization rules classify personal-document paths as never-commit and prohibit adjacent private context joined to world-readable host logs (`corpus/knowledge/evidence-minimization-r18.md:30-31`); the triage also limits package-history retention to history apart from joined private context (`.ufo/waves/round-18/out-of-metric-triage.md:33`). Redact the account and both PWD path values while retaining permitted event/count facts.

Private-value citations (line SHA-256 is UTF-8 bytes excluding LF; no private text reproduced):
- `build/PacmanTxnToday.md:119` — R4 document path: 1 before → 0 at tip; residual out-of-metric account identity: 1; SHA-256 `35ec9b4c230845d56e9a62bf3201c7771bdfdc74d00e984f68c2463028067ae2`.
- `build/PacmanTxnToday.md:120` — residual out-of-metric home-path values: 2; no frozen C1 class hit; SHA-256 `4852065fdfb26d77c5045a8d27531f939e59644b703616c7ba76f1715a1cf30e`.

No session-record field values, routing values, or per-seat retry values were found in the changed line or its neighboring hunk lines. The residuals above are distinct from those categories.

### Medium — “name-only” is not a standalone allowlist rule

The L1 triage's rationale for rejecting the name-only families (`.ufo/waves/round-18/out-of-metric-triage.md:26`) is defensible only where each occurrence fits a frozen C1 adjudication case. The frozen rule is context-bound: instruction/boundary/contract surface names without contents; field/key names inside lane tool code, a contract, or a synthetic fixture; or a non-author file the lane may not edit (`.ufo/waves/round-18/frozen/c1-policy.json:27`). Merely being a field, record-type, provider/model, or error-class name is not by itself an allowlist basis for arbitrary evidence prose. The triage does not map each mentioned occurrence to one of those contexts, so its conclusion should not be applied as a blanket allowance. In the two files reviewed here, retained lane-surface references are not frozen-class hits and do not need allowlist rows.

## No finding — OverlapTsukuroi redaction and technical meaning

`build/OverlapTsukuroi.md:96` removes one R4 document-path token (1 before → 0 at tip); no R1–R9 class, account-identity, or home-path value remains on lines 95–97. The line SHA-256 at tip is `894304e9a5c05b56aee6de16525a2a48cd3489001458030c92c8bcf58f0d7ca3`. The redaction preserves the event time and package-operation meaning and leaves the sibling lane reference intact; no technical meaning or Markdown structure was broken.

## Verification and scope

- Read-only diffs, both exit 0:
  - `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-17/build/OverlapTsukuroi.md`
  - `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-17/build/PacmanTxnToday.md`
- Read-only line-hash/class scan of the tip lines and adjacent hunk lines succeeded; the two initial shell hash one-liners had quoting `SyntaxError` (exit 1), then corrected scans succeeded. No source files were changed.
- Both changed files are Markdown, not JSON; `python3 -m json.tool` was not applicable.
- LSP is unavailable in the mounted tools (`read xd://lsp` returned “No such tool”); there are no code callers/definitions to resolve, and no grep fallback was used.
- No tools were installed or updated. No URLs were accessed.
