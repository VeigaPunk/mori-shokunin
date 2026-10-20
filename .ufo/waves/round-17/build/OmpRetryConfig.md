# OmpRetryConfig — retry.* config vs a zai 429 seat that burned 10 same-model retries

Seat: `MoriR17.OmpRetryConfig-5` (leaf scout, round 17 wave 1). Read-only.
Scope: `~/.omp/agent/config.yml` retry keys + `fallbackChains` for `m_zfl` / `m_flash`;
omp 18.12.3 embedded source (read-only byte inspection of `/home/vgpnk/.local/bin/omp`);
model catalog `~/.omp/agent/models.db`; field-limited transcript counts.
No credential, token, `agent.db`, `oauth`, `credential_pin` content or `errorMessage` text was read.
One item is not fully resolved: why the per-attempt model-switch helper returned false on the
dying seats (§6.4). It is marked [INFERENCE] and given a falsifier.

## 0. Verdict

The config does **not** disable the cascade and does **not** set the retry budget.
`retry:` contains exactly two keys: `modelFallback: true` (config.yml:141) and
`fallbackChains` (142–208). Everything that produced the death message comes from
**schema defaults that config never overrides**:

- `retry.maxRetries` absent → default **10** → the literal "10 retries" in
  `Retry budget exhausted after 10 retries` (omp byte 159685877).
- `retry.fallbackOn` absent → default **"any"** (omp 155849564), i.e. a 429 **is** allowed
  to walk `fallbackChains`; `T4("any", …)` returns `true` unconditionally (omp 159601238).
- `retry.maxDelayMs` absent → default **300000 ms**; `retry.waitForUsageReset` absent →
  default **false** (omp 155848215, 155848733).
- `fallbackChains.m_zfl` (189–191) exists, both entries are in `enabledModels`
  (74, 35) and resolvable in the live registry (models.db: 1,000,000 / 1,048,576 context,
  efforts `low/high/max`), so the chain is walkable — and sibling sessions do walk it
  to exactly `devin/glm-5-3-flash-1m` (§5).

Therefore the observable "same model 10 times, then budget exhausted" is the engine's
**per-model** budget running to its default end while the per-attempt switch applied
nothing. Config fixes the *number* (10) and the *candidate set* (two cross-provider models,
no zai replica); it does not forbid the switch itself.

## 1. Observed config facts (absolute paths, line numbers)

`/home/vgpnk/.omp/agent/config.yml`

| line | value | note |
|---|---|---|
| 94–95 | `zai/glm-5.3`, `zai/glm-5.3-flash` | only zai entries in `enabledModels` |
| 110 | `m_glm53: zai/glm-5.3:max` | zai role |
| 112 | `m_zfl: zai/glm-5.3-flash:max` | the zai role a zai seat runs as |
| 113 | `m_flash: commandcode/deepseek/deepseek-v4.1-flash:max` | role every leaf agent gets (see 121–138) |
| 121–138 | `agentModelOverrides`: all roles → `@m_flash` / `@m_strong` | **no** role maps to `@m_zfl`; zai seats are pinned explicitly by their dispatcher |
| 140 | `retry:` | block starts |
| 141 | `modelFallback: true` | redundant with default `true` (omp 155849258) |
| 142 | `fallbackChains:` | the only effective retry setting |
| 143–147 | `default:` devin/cursor/google-antigravity/openai-codex opus | |
| 182–184 | `m_glm53:` `devin/glm-5-3-1m`, `charm-hyper/glm-5.3` | |
| 189–191 | `m_zfl:` `devin/glm-5-3-flash-1m`, `charm-hyper/glm-5.3-flash` | **the zai chain** |
| 192–195 | `m_flash:` `charm-hyper/deepseek-v4.1-flash`, `opencode-go/deepseek-v4.1-flash`, `devin/deepseek-v4-1-flash` | |
| 209 | `dev:` | retry block ends at 208 |

Verified absent (grep count 0 each): `fallbackOn`, `maxRetries`, `maxDelayMs`,
`baseDelayMs`, `waitForUsageReset`, `fallbackRevertPolicy`, `usageAwareFallback`,
`retry.enabled`. Exit code 0 for
`for k in …; do grep -c "$k" config.yml; done`.

Consequence: `m_flash` seats (all mori wave-1 leaf agents) are **not** zai; a zai 429 seat
belongs to a dispatcher that pinned `@m_zfl` or `zai/glm-5.3-flash` explicitly.

## 2. Effective defaults (omp 18.12.3 embedded settings schema)

Byte offsets are into `/home/vgpnk/.local/bin/omp` (grep -abo `id: "retry.…"`):

- `retry.enabled` = **true** (155847620)
- `retry.maxRetries` = **10** (155847689); doc `omp://non-compaction-retry-policy.md`
  agrees ("retry.maxRetries (default 10)")
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

`A` = model switch applied this attempt; `M` = credential switched / banked reset redeemed.
So the canned message appears only when **no** switch happened on the final attempt and the
per-model attempt counter exceeded `maxRetries`. With `maxRetries` = 10 the message reads
exactly "after 10 retries" — i.e. 10 retries were spent, the 11th error ended the turn.

The model-switch gate (159685099–159685199):

```
if (!c && !M && I) {
  const v = this.#$(I);
  const T = s && this.#b.has(v);
  if (_ && r.modelFallback && T4(r.fallbackOn, Me(u, N.UsageLimit))
      && !ge && !me && !ye && !T && !this.#ie(e, u, d)) {
     … A = await this.#ue(I, e, { … });
```

- `_ = t?.allowModelFallback !== false` (159683792) — true on the ordinary error path;
  passed `false` only for reasonless aborts and Responses body-read timeouts.
- `T4` (159601238): `any → true`, `usage-limit → isUsageLimit`,
  `except-usage-limit → !isUsageLimit`. Config's unset `fallbackOn` ⇒ "any" ⇒ open.
- `ye` (1596850xx): `S !== undefined && F !== undefined && F <= r.maxDelayMs` — the
  "wait out a near-term usage-limit reset instead of switching" gate. `S` exists only if
  `recordUsageLimitOutcome` recorded a reset, which requires `Me(u, N.UsageLimit)`.
- Wait constants (147729730): `QUOTA_EXHAUSTED` 30 min, `RATE_LIMIT_EXCEEDED` 30 s,
  `CONCURRENT_LIMIT` 5 s, `MODEL_CAPACITY_EXHAUSTED` 45–75 s.

## 4. Is a zai 1302 429 a usage limit?

No. Classification path (omp 147750446 `xe`, 147733494 `P`, 147733589 `zf`):

```
if (!b && (R || MSe(d) || (u === 403 || u === undefined) && _Se(d) || f && (T || A === "QUOTA_EXHAUSTED")))
  o |= N.UsageLimit;
```

`P(e)` is true only for `QUOTA_EXHAUSTED` / `INSUFFICIENT_G1_CREDITS_BALANCE`.
`zf("Rate limit reached for requests")` (S043, docs.z.ai api-code.md:31, accessed
2026-10-20) hits `r.includes("rate limit")` → `RATE_LIMIT_EXCEEDED`; `f && (T || …)` is
false because `T = LE(d)` is false for a message with words ⇒ **N.Transient only**.
So `ye` is false, `recordUsageLimitOutcome` never records a reset, no "wait" label is
produced, and the wait-gate hypothesis is **falsified** for these seats (confirmed in §5:
zero `recovery:"wait"` records among zai transcripts).

## 5. Corpus evidence (field-limited; no content read)

Root `/home/vgpnk/.omp/agent/sessions` (5897 `*.jsonl`; 406 contain `"provider":"zai"`).
Only `type`, `customType`, `message.role/stopReason/errorStatus/provider/model`, and
`retryRecovery` keys / canned `note` / `recovery` values were inspected.

Cross-tab of zai files (fields: `recovery` class, `Retry budget exhausted`, model):

| recovery | exhausted | model | files |
|---|---|---|---|
| model | – | glm-5.3-flash | 182 |
| plain | yes | glm-5.3-flash | 124 |
| plain | – | glm-5.3-flash | 59 |
| model | yes | glm-5.3-flash | 24 |
| – | – | glm-5.3-flash | 13 |
| – | yes | glm-5.3-flash | 3 |
| – | – | glm-5.3 | 1 |

`model_change` records (session metadata, not content):

- `W1StateKotodama.jsonl`, `W1StateKumitate.jsonl`, `W1StateSouji.jsonl`:
  `zai/glm-5.3-flash → zai/glm-5.3-flash → devin/glm-5-3-flash-1m` — the cascade walked
  to **the first `m_zfl` chain entry (config.yml:190)**.
- `TameshiR17.RR8-2.jsonl`, `TameshiR17.RR4-2.jsonl`, `TameshiR17.RR3-2.jsonl`
  (the dying class): only `zai/glm-5.3-flash` twice, **no fallback model_change**.
- All `retryRecovery.note` values in those three files: 38/42/45 × `error; retried`
  (canned; produced by `#j(a,d)` for `recovery=="plain"` and non-usage-limit).
  `recovery:"credential"` appears in **0** files anywhere; `recovery:"wait"` in 0 zai files.

So: the chain is functional and OMP does walk it on zai seats; on the dying seats no
switch was ever applied, and every retry was a plain same-model backoff that counted
against the default 10.

## 6. Answer: config vs the observed loop

1. **"10" is a default, not a setting.** `retry.maxRetries` is absent; the schema default
   is 10. Any change to the observed number must be an explicit config value.
2. **The cascade was not disabled by config.** `modelFallback: true` (141), `fallbackOn`
   unset → "any", chain present and resolvable. The chain key matching is role-selector
   based (`cA`, 159602059; role keys resolve through `modelRoles`), and `m_zfl` resolves
   exactly to the running `zai/glm-5.3-flash` (at worst an "effort"/"base" match, still
   returned). `_V`/`sD` (159597529) fills role keys that have no chain with `default`, so
   `m_zfl` uses its own two entries, never the opus default chain.
3. **Config supplies only two candidates, both cross-provider** (`devin/…`, `charm-hyper/…`).
   The only same-provider sibling is `zai/glm-5.3` (config.yml:94, role `m_glm53`:110), and
   it is not a `m_zfl` chain candidate (189–191), so a zai-wide 429 cannot be absorbed by a
   same-provider model hop; credential rotation is a separate path (`M`) and it never fired
   (zero `recovery:"credential"` in all sessions).
4. **The terminal message is the engine's action when the per-attempt switch applies
   nothing for the whole budget.** Because `fallbackOn`/`modelFallback`/chain were all
   permissive, the reason no candidate applied is runtime state, not a config key:
   per-attempt filters are thinking ceiling (`P3e`), `contextFitsModel`, selector
   suppression, and key availability (159674039 ff.). Both candidates pass thinking/context
   from the catalog (1M context, `max` effort), so the remaining suspects are
   registry selector suppression/cooldown (`suppressSelector` has only two call sites:
   `noteRetryFallbackCooldown` when a model is the *failing source*, 159665391) and
   per-session key gating. **[INFERENCE]** — not observable post hoc; retry events are not
   persisted in transcripts (only `tool_execution_start`/`session_exit` custom types).
   Falsifier: run one zai seat with debug logging or with `retry.maxRetries: 1` and observe
   whether `retry_fallback_applied` fires; a per-process suppression map that has already
   burned `devin/glm-5-3-flash-1m` would reproduce "plain" retries.
5. **The wait branch did not run**: zai 429s are `Transient` (§4), `ye` false, and no zai
   transcript carries `recovery:"wait"`. `maxDelayMs` = 5 min therefore did not decide
   this case, though it would decide a quota-class (1113/1308) death.

Config levers that would change the observed outcome:
`retry.maxRetries` (surface sooner), a `m_zfl` chain with a same-provider zai entry or a
selector-keyed chain (`"zai/glm-5.3-flash": [...]`), `retry.fallbackOn`
(already permissive), and — only for quota-class errors — `retry.maxDelayMs` /
`retry.waitForUsageReset`.

## 7. Remaining unknowns

- Why `#ue` applied no candidate on the 124 dying zai sessions while it applied
  `devin/glm-5-3-flash-1m` in 182 sibling sessions. Runtime-only state (suppression map,
  per-session key/pin); marked [INFERENCE] in §6.4. No config key explains it.
- Whether a *pinned* subagent role changes chain-key selection (`pinnedRole` branch in
  `retryFallbackChainKeys`, 159665544) for these seats; the observed `model_change` to the
  `m_zfl` entry shows the key did resolve at least once.
- `credential_pin` content was not read (forbidden); its restriction effect on cross-provider
  `getApiKey` is unverified.

## 8. Commands

All read-only, exit 0 unless noted:
`wc -l`, `grep -n 'retry' config.yml`; `omp --version` → `omp/18.12.3`;
repeated `grep -abo '<symbol>' /home/vgpnk/.local/bin/omp` + Python `open().seek()/read()`
on the same file (no copies, no /tmp); `sqlite3` via Python `file:…?mode=ro` on
`~/.omp/agent/models.db` (`model_cache`); `grep -rl/‑l` field-token counts and one Python
line-scan per file under `~/.omp/agent/sessions`. No installs, no upgrades, no VCS commands,
no journalctl, no pacman. Writes: this file only.
