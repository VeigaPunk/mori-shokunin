# RedactOmpRetryConfig — round-18 C1 repair draft for the round-17 OmpRetryConfig report

Seat: `MoriR18Recovery.RedactOmpRetryConfig` (leaf scribe, round 18 wave 1). Read-only except this report.
Routed by: `corpus/lessons/round-17-verifier-spotcheck.md:339-346` (non-author closure) and `:390-397` (routed defect 1). Policy: `.ufo/waves/round-18/frozen/c1-policy.json` (must_redact_paths entry).
Original: `.ufo/waves/round-17/build/OmpRetryConfig.md` at 29b0dc7, blob `eee6fbaf3f3cb5297d2209fd0e3ce8a4eeaabe73`, SHA-256 `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7` (223 lines, 12726 bytes).

## Verdict

Draft complete. The replacement body below keeps the seat identity, task, verdict-level conclusions, public-source citations, non-private counts and the [INFERENCE] label with its falsifier. It carries zero hits under all nine classes R1–R9 of `frozen/c1-policy.json`. The L1 integrates: this draft is not written to the original path, and no allowlist entry is proposed for it.

## Scan results

Method: classes loaded from `frozen/c1-policy.json` with `json.load`; each class regex applied with python `re.finditer` to the draft text (121 lines, 11839 characters) and, as a counts-only control, `re.search` per line on the original blob. No text from the original is printed here.

| class | name | hits in replacement | lines with hit in original blob (counts only) |
|---|---|---|---|
| R1 | session_identity | 0 | 0 |
| R2 | session_store_path | 0 | 0 |
| R3 | tool_output_artifact | 0 | 0 |
| R4 | private_document | 0 | 0 |
| R5 | shell_history | 0 | 0 |
| R6 | privileged_config | 0 | 0 |
| R7 | operator_config_ref | 0 | 5 |
| R8 | routing_table_key | 0 | 8 |
| R9 | session_record_value | 0 | 4 |

The gate (`tools/mori-retention-gate.py`) is not run here; this is the class-regex check named in the wave brief. The original blob's non-zero counts are the before evidence for its routed status; the file has no allowlist entry and must scan to zero.

## What was removed (categories only, no values)

- Operator configuration: every line number, key-name list for routing and fallback tables, role/model identifiers and candidate-list entries replaced by a summary (values withheld).
- Transcript-derived values: per-file recovery-class and note names replaced by counts; the three named dying-class sessions and the walked-chain sessions are counted, not named; the session-store root is not named.
- Session-record field names with values: removed; only field presence and counts are kept.
- Operator model catalog: referenced as a store, not by path or table contents beyond the read-only access mode.
- Kept: the seat identity, the verdict logic, the omp public-schema defaults and byte offsets into the installed binary, the public z.ai documentation citation (docs.z.ai api-code.md:31, accessed 2026-10-20), the omp engine-path code excerpts, and the [INFERENCE] label on §6.4 with its falsifier.

## Commands and tooling

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/OmpRetryConfig.md` (read) — exit 0.
- `git -C ... rev-parse 29b0dc7:<path>` → `eee6fbaf3f3cb5297d2209fd0e3ce8a4eeaabe73`; `git -C ... show ... | sha256sum` → `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7` — exit 0.
- Read of `.ufo/waves/round-18/frozen/c1-policy.json`, `.ufo/waves/round-18/contract.md`, `corpus/lessons/round-17-verifier-spotcheck.md:322-350` and `:388-397` — exit 0.
- Python 3 stdlib scan (json, re, subprocess) as above — exit 0. No files written by the scan; no temporary files; no /tmp use.
- No installs, no upgrades, no VCS mutation, no journal query, no package-manager transaction. Tooling directive: nothing needed; none installed.

## Notes for L1

- The replacement is a full body with a provenance line: blob id and SHA-256 are the record; history is not rewritten.
- The original file must be overwritten by L1 with the body below (or the file replaced in the repair commit); the gate must then show zero hits for it with no allowlist row.
- The round-17 spot-check cites `:339-346` and `:390-397`; the frozen policy cites `:339-346` for the must-redact source. Those lesson lines are non-author; not edited here.
- The privacy exposure of already-pushed history is operator/kagi-owned and is not assessed here.

## Replacement

```markdown
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

## 5. Corpus evidence (field-limited aggregate; no content, no identities)

Transcript store: 5897 session files; 406 contain the zai provider. Only record type, custom type, message role / stop reason / error status / provider / model presence, retry-metadata keys and recovery class were inspected. Recovery classes are counted, not named.

Aggregate over the 406 zai files:

- 206 contain a fallback-switch record (182 without the exhaustion message, 24 with it).
- 183 contain only same-model retry records (124 with the exhaustion message, 59 without).
- 17 contain neither (13 without the exhaustion message, 3 with it).
- 151 files contain the budget-exhausted message in total.
- Zero files in the whole store contain a credential-rotation record; zero zai files contain a wait-class record.

Three sessions walked the cascade to the first entry of the zai flash candidate list. Three dying-class sessions carried no fallback-switch record: their model records named only the original model, and every retry-metadata entry in them was the canned plain-backoff note (counts 38, 42, 45 per file; produced by the plain-backoff branch for non-usage-limit errors).

So on the dying seats no switch was ever applied, and every retry was a plain same-model backoff counted against the default 10.

## 6. Answer: configuration vs the observed loop

1. **"10" is a default, not a setting.** `retry.maxRetries` is absent; the schema default is 10. Any change to the observed number must be an explicit configuration value.
2. **The cascade was not disabled by configuration.** The model-fallback toggle is true, `fallbackOn` is unset → "any", and the candidate list is present and resolvable. Chain key matching is role-selector based (omp 159602059); role keys resolve through the role map, and `_V`/`sD` (159597529) fills role keys that have no chain with the default chain. The zai flash role therefore uses its own entries, never the default chain.
3. **Configuration supplies only two candidates, both cross-provider.** The only same-provider sibling model is not a candidate for the zai flash role, so a zai-wide 429 cannot be absorbed by a same-provider model hop. Credential rotation is a separate path (`M`); it never fired (zero credential-rotation records in the store).
4. **The terminal message is the engine's action when the per-attempt switch applies nothing for the whole budget.** Because `fallbackOn`, the model-fallback toggle and the candidate list were all permissive, the reason no candidate applied is runtime state, not a configuration key: per-attempt filters are the thinking ceiling (`P3e`), `contextFitsModel`, selector suppression, and key availability (159674039 ff.). Both candidates pass thinking and context checks from the catalog, so the remaining suspects are registry selector suppression / cooldown (`suppressSelector` has only two call sites: `noteRetryFallbackCooldown` when a model is the failing source, 159665391) and per-session key gating. **[INFERENCE]** — not observable post hoc; retry events are not persisted in transcripts (only tool-execution and session-exit custom records).
   Falsifier: run one zai seat with debug logging, or with `retry.maxRetries` set to 1, and observe whether the fallback-applied event fires; a per-process suppression map that has already burned the first candidate would reproduce plain retries.
5. **The wait branch did not run.** zai 429s are `Transient` (§4), `ye` is false, and no zai transcript carries a wait-class record. `maxDelayMs` (5 min) therefore did not decide this case, though it would decide a quota-class death (1113/1308).

Configuration levers that would change the observed outcome: `retry.maxRetries` (surface sooner); a candidate list with a same-provider zai entry, or a selector-keyed chain for the zai flash role; `retry.fallbackOn` (already permissive); and, only for quota-class errors, `retry.maxDelayMs` / `retry.waitForUsageReset`.

## 7. Remaining unknowns

- Why the switch applied no candidate on the 124 dying zai sessions while it applied the first candidate in the 182 sibling sessions. Runtime-only state (suppression map, per-session key or pin); marked [INFERENCE] in §6.4. No configuration key explains it.
- Whether a *pinned* subagent role changes chain-key selection (pinned-role branch in the retry chain-key helper, 159665544) for these seats; the observed fallback switch to the first candidate shows the key did resolve at least once.
- Credential-pin records were not read (forbidden); their restriction effect on cross-provider key lookup is unverified.

## 8. Commands

All read-only, exit 0 unless noted: `wc -l` and `grep -n 'retry'` on the configuration file (match lines not recorded); `omp --version` → `omp/18.12.3`; repeated `grep -abo '<setting id>'` on the installed omp binary plus a Python seek/read on the same file (no copies, no temporary files); read-only SQLite via Python `mode=ro` on the operator's model catalog store (model cache table); `grep -rl` field-token counts and one Python line-scan per file under the transcript store (counts only). No installs, no upgrades, no VCS commands, no journal queries, no package-manager transactions. Writes: this file only.
```
