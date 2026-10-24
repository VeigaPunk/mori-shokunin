# OmpRetryConfig — retry settings vs a zai 429 seat that burned 10 same-model retries

Seat: `MoriR17.OmpRetryConfig-5` (leaf scout, round 17 wave 1). Read-only.
Scope: retry-related keys of an operator-owned runtime configuration file (values withheld); the embedded settings schema of the installed omp 18.12.3 binary (read-only byte inspection); the operator's model catalog store (read-only); field-limited aggregate counts over the transcript store.
Withheld: no credential, token, agent-database, oauth, credential-pin, error-message or transcript content was read. Configuration values, candidate-list entries, transcript field values and session identities are replaced by the scoped summaries below (round-18 privacy repair).
One item is not fully resolved: why the per-attempt model-switch helper returned false on the dying seats (§6.4). It is marked [INFERENCE] and given a falsifier.
Provenance: this body replaces round-17 blob `eee6fbaf3f3cb5297d2209fd0e3ce8a4eeaabe73` (SHA-256 `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7`, measured at 29b0dc7). No committed revision is rewritten; that blob remains the record.

Round-18 second-pass minimization: the operator configuration summary (former §1) and the
transcript-store aggregate (former §5) were removed after wave-2 falsification
(`.ufo/waves/round-18/falsify/AttackMinOmpRetryConfig.md`, `ConformanceAuditR18.md`); the
first round-18 integration had also truncated §3–§8 at an inner code fence, restored here.

## 0. Verdict

The configuration does **not** disable the cascade and does **not** set the retry budget. Everything that produced the death message comes from **schema defaults that configuration never overrides**:

- `retry.maxRetries` absent → default **10** → the literal "10 retries" in `Retry budget exhausted after 10 retries` (omp byte 159685877).
- `retry.fallbackOn` absent → default **"any"** (omp 155849564), i.e. a 429 **is** allowed to walk the fallback candidates; `T4("any", …)` returns `true` unconditionally (omp 159601238).
- `retry.maxDelayMs` absent → default **300000 ms**; `retry.waitForUsageReset` absent → default **false** (omp 155848215, 155848733).

Therefore the observable "same model 10 times, then budget exhausted" is the engine's **per-model** budget running to its default end while the per-attempt switch applied nothing. Configuration does not set the number (10 is a default, not a setting) and does not forbid the switch;

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

```
const o = this.#se(e) ? Math.min(r.maxRetries, 1) : r.maxRetries;
const d = this.#t > o;                                   // budget exhausted
…
if (d) {
  if (!A && !M) {
    const v = this.#t - 1;
    e.errorMessage = `Retry budget exhausted after ${v} ${v === 1 ? "retry" : "retries"}: ${a}`;
```

`A` = model switch applied this attempt; `M` = credential switched / banked reset redeemed. So the canned message appears only when **no** switch happened on the final attempt and the per-model attempt counter exceeded `maxRetries`. With `maxRetries` = 10 the message reads exactly "after 10 retries" — i.e. 10 retries were spent, the 11th error ended the turn.

The model-switch gate (159685099–159685199):

```
if (!c && !M && I) {
  const v = this.#$(I);
  const T = s && this.#b.has(v);
  if (_ && r.modelFallback && T4(r.fallbackOn, Me(u, N.UsageLimit))
      && !ge && !me && !ye && !T && !this.#ie(e, u, d)) {
     … A = await this.#ue(I, e, { … });
```

- `_ = t?.allowModelFallback !== false` (159683792) — true on the ordinary error path; passed `false` only for reasonless aborts and Responses body-read timeouts.
- `T4` (159601238): `any → true`, `usage-limit → isUsageLimit`, `except-usage-limit → !isUsageLimit`. Unset `fallbackOn` ⇒ "any" ⇒ open.
- `ye` (1596850xx): `S !== undefined && F !== undefined && F <= r.maxDelayMs` — the "wait out a near-term usage-limit reset instead of switching" gate. `S` exists only if `recordUsageLimitOutcome` recorded a reset, which requires `Me(u, N.UsageLimit)`.
- Wait constants (147729730): `QUOTA_EXHAUSTED` 30 min, `RATE_LIMIT_EXCEEDED` 30 s, `CONCURRENT_LIMIT` 5 s, `MODEL_CAPACITY_EXHAUSTED` 45–75 s.

## 4. Is a zai rate-limit 429 a usage limit?

No. Classification path (omp 147750446 `xe`, 147733494 `P`, 147733589 `zf`):

```
if (!b && (R || MSe(d) || (u === 403 || u === undefined) && _Se(d) || f && (T || A === "QUOTA_EXHAUSTED")))
  o |= N.UsageLimit;
```

`P(e)` is true only for the quota-exhausted and insufficient-balance classes. `zf("Rate limit reached for requests")` (public source: docs.z.ai api-code.md:31, accessed 2026-10-20) hits the rate-limit substring → `RATE_LIMIT_EXCEEDED`; `f && (T || …)` is false because the message is not a bare code ⇒ **Transient only**. So `ye` is false, `recordUsageLimitOutcome` never records a reset, no wait label is produced, and the wait-gate hypothesis is **falsified** for these seats (§5: zero wait-class records in zai transcripts).

## 6. Answer: configuration vs the observed loop

1. **"10" is a default, not a setting.** `retry.maxRetries` is absent; the schema default is 10. Any change to the observed number must be an explicit configuration value.
2. **The cascade was not disabled by configuration.** The retry settings that decide fallback are permissive at their schema defaults; the operator configuration's own values are withheld (round-18 privacy repair, second pass).
4. **The terminal message is the engine's action when the per-attempt switch applies nothing for the whole budget.** Because `fallbackOn`, the model-fallback toggle and the candidate list were all permissive, the reason no candidate applied is runtime state, not a configuration key: per-attempt filters are the thinking ceiling (`P3e`), `contextFitsModel`, selector suppression, and key availability (159674039 ff.). Both candidates pass thinking and context checks from the catalog, so the remaining suspects are registry selector suppression / cooldown (`suppressSelector` has only two call sites: `noteRetryFallbackCooldown` when a model is the failing source, 159665391) and per-session key gating. **[INFERENCE]** — not observable post hoc; retry events are not persisted in transcripts (only tool-execution and session-exit custom records).
   Falsifier: run one zai seat with debug logging, or with `retry.maxRetries` set to 1, and observe whether the fallback-applied event fires; a per-process suppression map that has already burned the first candidate would reproduce plain retries.
5. **The wait branch did not run.** zai 429s are `Transient` (§4), `ye` is false, and no zai transcript carries a wait-class record. `maxDelayMs` (5 min) therefore did not decide this case, though it would decide a quota-class death (1113/1308).

Configuration levers that would change the observed outcome are the public schema keys above (`retry.maxRetries`, the fallback candidate configuration, `retry.fallbackOn`, and for quota-class errors `retry.maxDelayMs` / `retry.waitForUsageReset`).

## 7. Remaining unknowns

- Why the per-attempt switch applied no candidate on the dying zai seats while sibling seats did switch: runtime-only state (suppression map, per-session key or pin); marked [INFERENCE] in §6.4. No configuration key explains it.
- Whether a pinned subagent role changes chain-key selection for these seats (pinned-role branch in the retry chain-key helper, omp 159665544).
- Credential-pin records were not read (forbidden); their restriction effect on cross-provider key lookup is unverified.

## 8. Commands

All read-only, exit 0 unless noted: `wc -l` and `grep -n 'retry'` on the configuration file (match lines not recorded); `omp --version` → `omp/18.12.3`; repeated `grep -abo '<setting id>'` on the installed omp binary plus a Python seek/read on the same file (no copies, no temporary files); read-only SQLite via Python `mode=ro` on the operator's model catalog store (model cache table); `grep -rl` field-token counts and one Python line-scan per file under the transcript store (counts only). No installs, no upgrades, no VCS commands, no journal queries, no package-manager transactions. Writes: this file only.
