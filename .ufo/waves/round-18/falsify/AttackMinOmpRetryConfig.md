# Falsification: minimized OmpRetryConfig replacement

Scope: read-only comparison of `.ufo/waves/round-17/build/OmpRetryConfig.md` at `d005cdd` and `e2bfbd6`, against the routed closure at `corpus/lessons/round-17-verifier-spotcheck.md:339-346` and the round-18 privacy decision rule. No source files or VCS state were changed.

## Findings

- **High — the replacement does not preserve the full verdict.** The original is 223 lines; the replacement is 46 lines. The replacement retains the top-level configuration/defaults conclusion and the short claim that the per-model retry budget ended while a fallback attempt applied nothing (`:11-18`). It then opens section 3 at `:43`, ends with an empty evidence lead-in at `:45`, and reaches EOF at `:46`. The engine-path analysis and the original sections 4–8 are absent. Thus the detailed conclusions are lost: 429 classification versus the usage-limit/wait branch, the distinction between failing and sibling sessions, the runtime-state explanation marked as inference with its falsifier, and the remaining unknowns. The surviving cross-reference to section 5 at `:16` is dangling. Verdict retention is partial, not complete.

- **High — operator configuration/routing information remains in semantic summaries.** At `:11`, `:13-16`, `:18`, and `:24-28`, the replacement still conveys configuration state (a toggle and omitted-key state), fallback-list shape, provider/role routing, and candidate-set properties. Exact model identifiers, route aliases, configuration paths, and line numbers from the original have been removed, but the remaining summaries still disclose configuration/routing values at a coarser level. Classify as out-of-metric semantic R7/R8-type retention; these descriptions do not assert literal C1 regex hits.

- **Medium — session-derived values and a cross-session paraphrase remain.** `:1` and `:18` retain the per-seat retry-count observation; `:16` retains one paraphrase of sibling-session behavior. No verbatim other-session tool-output excerpt or concrete session/transcript identity remains. The line-16 statement is same-round sibling-seat evidence, which the out-of-metric triage rule classifies as lane work rather than private context; it nevertheless remains a session-derived paraphrase under the question's broader inventory. These are semantic R9-type session-record-value remnants, not asserted literal C1 R9 regex hits.

- **No residual personal-document, shell-history, or privileged-configuration fact found.** No personal document/history fact, privileged-config value, session-store path, timestamped session identity, or numbered tool-output artifact was present in the replacement. `:3` retains a lane seat label, which the triage rule explicitly distinguishes from a private session identity.

## Provenance and verification

- The provenance line at replacement `:7` names the original blob `eee6fbaf3f3cb5297d2209fd0e3ce8a4eeaabe73` and SHA-256 `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7`. Verified: `git rev-parse d005cdd:.ufo/waves/round-17/build/OmpRetryConfig.md 29b0dc7:.ufo/waves/round-17/build/OmpRetryConfig.md e2bfbd6:.ufo/waves/round-17/build/OmpRetryConfig.md` returned, respectively, `eee6fbaf3f3cb5297d2209fd0e3ce8a4eeaabe73`, `eee6fbaf3f3cb5297d2209fd0e3ce8a4eeaabe73`, and `7c02c16a464cac7464405ebae54b45485e2d5b55` (exit 0). `git cat-file blob eee6fbaf3f3cb5297d2209fd0e3ce8a4eeaabe73 | sha256sum` returned the cited digest (exit 0); the provenance blob id and digest are correct.
- The audited replacement blob `7c02c16a464cac7464405ebae54b45485e2d5b55` has SHA-256 `6428d1154253d54788bb5dccaec71efb0f80c610f92c6db52e99a4a81b3cf7f4` (`git cat-file blob … | sha256sum`, exit 0).
- Read-only commands exercised: `git show d005cdd:<path>` (exit 0; 223 lines); `git show e2bfbd6:<path>` (exit 0; 46 lines); the `git rev-parse` and `git cat-file`/`sha256sum` commands above (exit 0); and a `git grep -n` line-location query against `e2bfbd6` (exit 0). The closure range and frozen C1/C2/C3 inputs were read. No installs or updates; no URLs used.

## Residual risk and verification gaps

The source blob provenance is authenticated by the requested object-id and digest checks, but that does not validate the replacement's semantic minimization. No retention-gate execution was part of this scoped read-only assignment. No LSP device was available or applicable to this Markdown-blob audit; no caller/definition/diagnostics claim is made. No other verification was run.
