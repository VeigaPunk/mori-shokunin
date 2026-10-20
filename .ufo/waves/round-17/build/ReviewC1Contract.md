# C1 contract review: real terminal shapes

## Finding

### Medium — `provider`/`model` attribution is undefined for real `toolResult` terminals

C1 selects the last `message` as terminal (contract.md:35–39), defines a terminal `toolResult` as `incomplete` (48–50), then requires per-seat `provider` and `model` and `by_provider_model` tallies (52, 57–59). It does not say whether those values come only from the terminal message, are inherited from an earlier message, or how absent values are represented and tallied.

Concrete observed shape: in the supplied session directory, 52 terminal messages had `role=toolResult`, no `stopReason`, and neither `provider` nor `model` present. Each of these files had an earlier message carrying a provider/model pair. Thus both terminal-only attribution (missing/null group) and prior-message attribution are possible, and the contract does not select between them. Observed earlier pairs: `anthropic/claude-opus-5-5` (12), `openai-codex/gpt-6-luna` (11), `openai-codex/gpt-6.1-sol` (1), `opencode-go/deepseek-v4.1-flash` (23), `zai/glm-5.3-flash` (5). Specify the source/fallback and missing-value grouping before treating the required provider/model census as reproducible.

## Classifier observations

A bounded, key-limited pass over `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07` followed C1's 262144-byte tail and partial-first-line rule. It examined only top-level `type`, `message.role`, `message.stopReason`, `message.errorStatus`, `message.provider`, `message.model`, and the contract-named error-message tokens/patterns; it did not emit message text or inspect other record fields. Snapshot counts: 2509 regular non-symlink `*.jsonl` files; 0 unparseable lines; 2202 `completed`, 80 `aborted`, 166 `dead_rate_limit`, 2 `dead_quota`, 59 `incomplete` (52 `toolResult` and 7 assistant `toolUse`); 0 `dead_error_other`, 0 `unavailable`, and 0 unclassified terminal-role/stop-reason shapes. Therefore no class-level misclassification was observed among these terminal shapes; this is a scan of real inputs against the contract rules, not a run of the delivered tool. The directory is live; counts describe only this observation time, not a stable population.

One observed `assistant/error` shape had `errorStatus=429` and both `RATE_LIMITED` and `usage limit` tokens. C1 line 51 explicitly resolves that overlap to `dead_rate_limit`; the rule is deterministic. [INFERENCE] If this particular message's usage-limit signal meant quota rather than request rate, that precedence would hide the quota signal. The permitted field-only observation cannot settle that semantic interpretation, so this is residual risk, not a confirmed class defect.

## Verification gaps / residual risk

- `tools/mori-seat-terminal.py` is absent from the repository's `tools/` listing, so no implementation behavior or C1 test was exercised. The scoped diff was empty: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --no-ext-diff --unified=3 -- .ufo/waves/round-17/contract.md tools/mori-seat-terminal.py` — exit 0; `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff HEAD --no-ext-diff --unified=3 -- .ufo/waves/round-17/contract.md tools/mori-seat-terminal.py` — exit 0.
- No LSP device/server was available: `read xd://lsp` returned “No such tool.” Literal grep was used only to locate C1 references, not as semantic proof. No build, test, lint, or selftest was run.
- The real snapshot had no `dead_error_other` or `unavailable` examples, so those class paths were not exercised by this corpus scan.
- No tools were installed or updated.
