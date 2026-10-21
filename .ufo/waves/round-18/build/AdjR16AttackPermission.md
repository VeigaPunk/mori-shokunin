# C1 population adjudication — AttackPermission

## Scope and axes

Reviewed the two frozen C1 population rows for `.ufo/waves/round-16/build/AttackPermission.md` at the requested `29b0dc7` revision, then scanned the complete 68-line blob for private context outside the frozen regex classes. Axes: fidelity to the frozen adjudication rule, provenance retention, and privacy minimization.

The frozen population query returned exactly two rows for this path. Both supplied line hashes matched the corresponding lines in the requested historical blob.

## Findings — high severity

Both rows are `redact`. Neither line is an instruction/boundary/contract naming a surface without its contents (`allow-a`), a lane-code/contract/synthetic-fixture field or key (`allow-b`), or a non-author file (`allow-c`). They are narrative references to private session-derived material, not permitted allowlist cases. They are not in the policy's `must_redact_paths`, but the adjudication rule still requires redaction because no allow rule applies. Do not allowlist either row; as author-path hits, both remain in the frozen metric until removed.

- `.ufo/waves/round-16/build/AttackPermission.md:16` — class `R2`; redact. Minimal provenance-preserving replacement: `decision=redact; count=1; class=R2; line_sha256=b77377f6cdfdbd9ae8b61be183e8d71c4724dcf7dc0addb89e271d9ad371f406`. Remove the matched private session-store reference and the adjacent session-derived / temporary-artifact evidence details; do not retain them in abbreviated or ellipsized form.
- `.ufo/waves/round-16/build/AttackPermission.md:65` — class `R2`; redact. Minimal provenance-preserving replacement: `decision=redact; count=1; class=R2; line_sha256=f2c2aa7606429ffd374e5995060111b959dacbd3dbdef41aafee267d95eecf7f`. Remove the matched private session-store reference and associated session-metadata / opaque-value discussion; do not retain the underlying values or excerpt.

## Additional private context outside the frozen metric

The whole-file sweep found further private context not represented by those two C1 rows. These are reading-sweep observations, not additions to the frozen population metric:

- Other-session evidence, excerpts, and action/detail rows: `.ufo/waves/round-16/build/AttackPermission.md:14,18-28,34-35,40-48,52-55,59,65-66`. The table material includes session-derived evidence/action details; line 65 is also one of the frozen hits.
- Session metadata and opaque-value / authentication-token discussion: `.ufo/waves/round-16/build/AttackPermission.md:6,12,24-25,30,34-35,43-45,48,55,65`. These references should not be expanded with values or copied from source context; line 65 is also a frozen hit.
- Local temporary-host filesystem/artifact details and content attribution: `.ufo/waves/round-16/build/AttackPermission.md:4,10,12,16,20-28,30,45-48,53,61,63-64`. This context is outside the listed C1 regex classes and should be minimized independently of the population-row replacements.
- No private-document, operator-config, shell-history, or concrete model-routing value was observed in the complete-file pass. There is a generic model/provider reference at line 47, but no routing assignment/value was observed.

## Evidence and verification gaps

- Read-only line probes: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-16/build/AttackPermission.md | sed -n '13,19p'` — exit 0; and the same command with `sed -n '62,68p'` — exit 0. The surrounding context was used only for classification; no source excerpts are reproduced here.
- Complete historical-blob pass via read-only `git show` — exit 0; 68 lines. The two observed line SHA-256 values equal the frozen population values.
- The `lsp` device is not mounted, so no LSP status, references, definition, or diagnostics result was available. This is a Markdown privacy adjudication; no caller or runtime behavior was exercised. No tests/build were run.
- Current-branch remediation status was not evaluated; findings describe the frozen historical blob requested for this adjudication.

```json
[
  {
    "path": ".ufo/waves/round-16/build/AttackPermission.md",
    "line": 16,
    "class": "R2",
    "line_sha256": "b77377f6cdfdbd9ae8b61be183e8d71c4724dcf7dc0addb89e271d9ad371f406",
    "decision": "redact",
    "reason": "The line carries private session-derived evidence rather than an allowed instruction, lane field/key, or non-author statement."
  },
  {
    "path": ".ufo/waves/round-16/build/AttackPermission.md",
    "line": 65,
    "class": "R2",
    "line_sha256": "f2c2aa7606429ffd374e5995060111b959dacbd3dbdef41aafee267d95eecf7f",
    "decision": "redact",
    "reason": "The line carries private session-derived evidence and metadata rather than an allowed instruction, lane field/key, or non-author statement."
  }
]
```