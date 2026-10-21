# OmpRetryConfig — retry settings vs a zai 429 seat that burned 10 same-model retries

Seat: `MoriR17.OmpRetryConfig-5` (leaf scout, round 17 wave 1). Read-only.
Scope: retry-related keys of an operator-owned runtime configuration file (values withheld); the embedded settings schema of the installed omp 18.12.3 binary (read-only byte inspection); the operator's model catalog store (read-only); field-limited aggregate counts over the transcript store.
Withheld: no credential, token, agent-database, oauth, credential-pin, error-message or transcript content was read. Configuration values, candidate-list entries, transcript field values and session identities are replaced by the scoped summaries below (round-18 privacy repair).
One item is not fully resolved: why the per-attempt model-switch helper returned false on the dying seats (§6.4). It is marked [INFERENCE] and given a falsifier.
Provenance: this body replaces round-17 blob `eee6fbaf3f3cb5297d2209fd0e3ce8a4eeaabe73` (SHA-256 `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7`, measured at 29b0dc7). No committed revision is rewritten; that blob remains the record.

## 0. Verdict

The configuration does **not** disable the cascade and does **not** set the retry budget. Its retry block holds only a model-fallback toggle (true, equal to its schema default) and a fallback candidate list. Everything that produced the death message comes from **schema defaults that configuration never overrides**:

- `retry.maxRetries` absent → default **10** → the literal "10 retries" in `Retry budget exhausted after 10 retries` (omp byte 159685877).
- `retry.fallbackOn` absent → default **"any"** (omp 155849564), i.e. a 429 **is** allowed to walk the fallback candidates; `T4("any", …)` returns `true` unconditionally (omp 159601238).
- `retry.maxDelayMs` absent → default **300000 ms**; `retry.waitForUsageReset` absent → default **false** (omp 155848215, 155848733).
- The fallback candidate list for the zai flash-class role exists and both entries resolve in the live model catalog, so the chain is walkable; sibling sessions do walk it to its first cross-provider entry (§5).

Therefore the observable "same model 10 times, then budget exhausted" is the engine's **per-model** budget running to its default end while the per-attempt switch applied nothing. Configuration does not set the number (10 is a default, not a setting) and does not forbid the switch; it supplies the candidate set (two cross-provider models, no same-provider replica).

## 1. Observed configuration facts (summary; values withheld)

Operator-owned configuration file, retry-related keys only:

- The retry block contains a model-fallback toggle set true (equal to its schema default) and one fallback candidate list. No other retry key is present.
- Keys verified absent (grep count 0 each; exit code 0): `fallbackOn`, `maxRetries`, `maxDelayMs`, `baseDelayMs`, `waitForUsageReset`, `fallbackRevertPolicy`, `usageAwareFallback`, `retry.enabled`.
- The zai flash-class role has its own two-entry candidate list. No general leaf-agent role is routed to a zai model; a zai 429 seat was pinned to a zai role explicitly by its dispatcher.

Consequence: general leaf-agent seats are not zai seats. A zai 429 seat belongs to a dispatcher that pinned a zai role explicitly.

## 2. Effective defaults (omp 18.12.3 embedded settings schema)

Byte offsets into the installed omp binary (grep -abo of the setting id):

- `retry.enabled` = **true** (155847620)
- `retry.maxRetries` = **10** (155847689); the omp non-compaction retry policy document agrees ("retry.maxRetries (default 10)")
- `retry.baseDelayMs` = **500** (155848143)
- `retry.maxDelayMs` = **5 * 60 * 1000** (155848215); `<= 0` disables the ceiling
- `retry.waitForUsageReset` = **false** (155848733)
- `retry.modelFallback` = **true** (155849258)
- `retry.fallbackOn` ∈ {any, usage-limit, except-usage-limit}, default **"any"** (155849564)
- `retry.fallbackRevertPolicy` default **"cooldown-expiry"** (definition at 155854122 ff.)

## 3. Engine path that emits the death message

`handleRetryableError(e,t) → #N(e,t) → #pe(e,t)` (omp 159644574, 159680293). Relevant lines:

