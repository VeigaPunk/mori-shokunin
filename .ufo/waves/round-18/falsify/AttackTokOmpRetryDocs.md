# AttackTokOmpRetryDocs — wave-2 falsification

## Scope and evidence

Reviewed the read-only `d005cdd` → `e2bfbd6` diff for `.ufo/waves/round-17/build/OmpRetryDocs.md`. It changes one row, at line 34. The attacked-tip file SHA-256 is `ddfdcbd224e606b39a3c4e5895eb3f3a064739615efd73d15345c00f9d206d80`.

- The changed row removes the concrete session-store path and replaces it with a withholding placeholder. Its bundled-doc locator remains; the technical statement and source attribution remain intelligible.
- No private token remains on the changed row itself. Its neighboring lines (35–42) describe record/type names and documented schema vocabulary, not observed values from an individual session. No operator-specific routing value or per-seat retry value is adjacent to this edit.
- **MEDIUM — possible residual session identity, R1 / `session_identity`:** line 240 retains one timestamped example with a truncated identifier (one candidate line). It is unchanged by the diff and is a value-shaped identity, not a name-only surface. **[INFERENCE]** It may be session-derived; the file alone does not establish provenance. The frozen R1 pattern at `frozen/c1-policy.json:7` requires a longer identifier form, so this shortened example can escape that class match. Redact it to a generic placeholder or establish that it is synthetic before treating token minimization as complete.
- The generic store-root mention at line 252 is a name-only surface, with no session-specific child path or identifier. It is not matched by frozen R2's child-path pattern (`frozen/c1-policy.json:8`). Under the adjudication rule at `frozen/c1-policy.json:27`, retaining this surface-only mention is defensible; it does not undo removal of the concrete path on line 34.
- Two R9-matching lines (`model_change` surface/record-type names) remain at lines 42 and 55. They name a documented type, not a private record value. The target file is not one of the three `must_redact_paths` listed at `frozen/c1-policy.json:17-21`, so name-only allowlisting is available under the frozen rule. This supports L1's name-only decision, provided the final allowlist has the corresponding line-hash/reason rows; this review did not inspect that allowlist. The broader draft claim is at `draft-verdicts.md:8`.

## Verification gaps

- No `.json` file changed, so `python3 -m json.tool` was not applicable.
- The `lsp` device is not mounted (`read xd://lsp` returned “No such tool”); LSP status, references, definition, and diagnostics were unavailable. Text search was used only to locate candidate lines, not as semantic proof.
- No URLs were fetched. No runtime or test command was in scope.

## Commands and results

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id -p --no-ext-diff d005cdd e2bfbd6 -- .ufo/waves/round-17/build/OmpRetryDocs.md` — rc 0; one changed row.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6:.ufo/waves/round-17/build/OmpRetryDocs.md` — rc 0; inspected for remaining candidates.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6:.ufo/waves/round-17/build/OmpRetryDocs.md | sha256sum` — rc 0; digest above.
