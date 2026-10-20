# OmpRetryDocs — OMP retry, fallback, rate-limit, and transcript evidence (C1 tier-B local source)

Seat: `MoriR17.OmpRetryDocs-5` (scout, leaf member, no subagent dispatch). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`, entering tip `24526ea9617cd020fee16c28fe4d4a2789dc28cb`.
Access date: 2026-10-20. Scope: source evidence for C1 (`seat terminal status`). No edit, no
judgment of the claim, no routing. Nothing written outside this report.

Installs/updates: **none**. No pacman, uv, npx, or binary download was needed.
Methods: (a) `read` of the harness docs at `omp://…` served by the installed harness;
(b) read-only string probes over the installed `omp` binary
(`/home/vgpnk/.local/bin/omp`, sha256 `065b5079d65ff6b77d961c935ba808e8f0f569ca6a2cb7b5fb6a1e8da72d7dec`,
`omp --version` → `omp/18.12.3`, rc 0). No transcript, session file, journal, credential,
database, or VCS operation was read or run. No `/tmp` write.

LSP note: no TypeScript source tree is present for the installed harness (`omp` is a compiled
Bun ELF; `/home/vgpnk/Projects/ufo-fsd-alpha/substrates/omp` is only `bin/cli.mjs` plus a
manifest). The `lsp` device therefore had no file to answer for these symbols; the compiled
artifact's embedded source text and the bundled docs are the available evidence. That
unavailability is recorded rather than treated as absence.

## Verdict (one line)

C1's field model is real in OMP 18.12.3, with four contract-level corrections: quota deaths
collapse into HTTP 429, `after N retry` is singular for N=1, several legitimate terminal
`message.role` values have no class, and a seat id cannot be derived from a raw sessions-tree
filename.

## 1. Observed: transcript record model

All from the bundled docs (primary source for storage) unless marked binary.

| Fact | Evidence |
|---|---|
| Files are JSONL under `~/.omp/agent/sessions/<encoded-cwd>/<timestamp>_<sessionId>.jsonl` | `omp://session.md:42` |
| Current files begin with a fixed 256-byte `type:"title"` slot, then the `type:"session"` header, then entries | `omp://session.md:65-67` |
| Current session version is `3` | `omp://session.md:437` |
| `type:"message"` entries carry the `AgentMessage` directly under `message` | `omp://session.md:150-168` |
| Persisted roles are camelCase; `toolResult` is not `tool_result` | `omp://session.md:175-183` |
| A `model_usage` entry has `stopReason` and optional `errorMessage` but is a different entry type | `omp://session.md:210-214` |
| `session_exit` custom record: `{ reason, kind: normal\|signal\|fatal\|process_exit, recordedAt, pendingToolCalls? }` | `omp://session.md:327` |
| Resume appends a synthetic assistant message with `stopReason:"aborted"` after a non-terminal tail | `omp://session.md:333` |
| Retry fallback transitions can be marked by `resolvedModelIsFallback` on `model_change` | `omp://session.md:229-232` |

Quotes (each ≤25 words):

- "Current files physically begin with a fixed-width, 256-byte `type: \"title\"` slot
  (including its newline), followed by the session header" —
  `omp://session.md:65`.
- "Result of one tool call — **not** `tool_result`. Carries `toolCallId`/`toolName`." —
  `omp://session.md:180`.
- "Fields are `purpose`, optional model `role`, `api`, `provider`, `model`, `usage`,
  `stopReason`, and optional `errorMessage`." — `omp://session.md:210-212`.
- "causes `AgentSession`/SDK initialization to append a synthetic assistant message with
  `stopReason: \"aborted\"`" — `omp://session.md:333`.
- "Model fallback changes append temporary `model_change` entries" —
  `omp://non-compaction-retry-policy.md:278`.

Terminal `stopReason` vocabulary (observed, `omp://provider-streaming-internals.md:145-158`
and `omp://toolconv/anthropic.md:147`): `stop`, `toolUse`, `length`, `aborted`, `error`.
Provider finish reasons map into them (`max_tokens`/`incomplete` → `length`;
`tool_use` → `toolUse`; `refusal`/`sensitive`/`failed` → `error`).

## 2. Observed: retry policy (what produces `Retry budget exhausted`)

Quotes (≤25 words each):

- "`retry.maxRetries` (default `10`)" — `omp://non-compaction-retry-policy.md:112`
  and `omp://settings.md:576` ("Max retries per request.").
- "HTTP-like server classes: 429, 500, 502, 503, 504" —
  `omp://non-compaction-retry-policy.md:61`.
- "using the persisted `errorId`/status when present and augmenting it from provider-aware
  message classification" — `omp://non-compaction-retry-policy.md:50`.
- "auto-retry classifies assistant failures through structured `errorId` / AI error
  predicates, with message classification as a fallback" —
  `omp://provider-streaming-internals.md:226`.
- "`stopReason = \"aborted\"` for caller cancellation" — `omp://provider-streaming-internals.md:155`.
- "otherwise `stopReason = \"error\"`" — `omp://provider-streaming-internals.md:156`.
- "persistence writes finalized messages at `message_end`" —
  `omp://provider-streaming-internals.md:225`.

Defaults and mechanics (docs, lines cited): `retry.enabled` true, `maxRetries` 10,
`baseDelayMs` 500, `maxDelayMs` 300000 (`settings.md:575-577`); backoff
500/1000/2000/4000/8000 ms (`non-compaction-retry-policy.md:124-128`); a final delay past
`maxDelayMs` fails fast unless an authoritative usage reset is allowed
(`non-compaction-retry-policy.md:90`); permanent stops include `retry.enabled=false`,
non-retryable without a model switch, context overflow, budget exceeded, user cancel, and
global abort (`## Permanent stop conditions`).

Classification requires `assistant stopReason === "error"` plus retryability; context
overflow is diverted to compaction (`non-compaction-retry-policy.md:40-45`).

## 3. Observed: fallback chains

- "`retry.fallbackOn` (default `\"any\"`; `\"usage-limit\"` or `\"except-usage-limit\"`
  restrict which errors walk the chains)" — `omp://non-compaction-retry-policy.md:197`,
  also `omp://settings.md:578`.
- "A fallback model receives a fresh retry budget; credential recovery keeps the cumulative
  count." — `omp://non-compaction-retry-policy.md:89`.
- "each hop still consumes a retry attempt" — `omp://settings.md:589`.
- "When the active chat model keeps failing (429s, quota walls, provider outages) and
  `retry.modelFallback` is on" — `omp://settings.md:587`.
- Chain selection order (exact model key → `provider/*` → role chain → `default`), prefixed
  wildcards, and `[]` disabling a model-kind chain: `omp://settings.md:579,587-589`.
- Revert policy `cooldown-expiry` (default) or `never`: `omp://settings.md:580`.
- Events `retry_fallback_applied { from, to, role, reason? }` and
  `retry_fallback_succeeded { model, role }` are **session events**, not entries:
  `omp://non-compaction-retry-policy.md:228-229`.

## 4. Observed: rate-limit vs quota classification

Compiled-artifact evidence (`grep -a` over the binary; commands in §7):

`packages/ai/src/error/retryable.ts`:

```
function wm(e) {
  return e !== undefined && (e === 408 || e === 429 || e >= 500);
}
var oo = /bad record mac|stream error.*received from peer|1302/i;
function io(e) {
  return e.includes("tls: bad record mac") || e.includes("type=server_error");
}
function bE(e) {
  ...
  if (t !== undefined && t >= 400 && t < 500 && t !== 408 && t !== 429) {
    return false;
  }
  ...
}
```

`packages/ai/src/error/gateway.ts`:

```
if (/\brate[- _]?limit(?:s|ed|ing)?\b|\bquota(?:_exceeded| exceeded)?\b|\btoo[- _]many[- _]requests\b/i.test(t) || _l(t)) {
    return { status: 429, type: "rate_limit_error", message: t };
}
...
function _l(e, t) {
  return Me(Qn(e, t), N.UsageLimit);
}
```

Observed consequences:

1. `429` and `>=500` and `408` are retryable; every other `4xx` is **not** retryable and
   surfaces without retrying. `402` therefore never produces a retry-exhaustion message.
2. OMP's own gateway shaping maps text matching `rate limit`/`quota`/`too many requests`
   (and the typed `UsageLimit` flag) to **HTTP 429 `rate_limit_error`**. A quota error that
   passes through this shaper carries `errorStatus = 429`.
3. The literal `1302` is hardcoded as retryable in `retryable.ts` (independent of any vendor
   table). With zai returning HTTP 429 for 1113/1302/1308 (sibling row S043,
   `build/SrcZaiErrorCodes.md`), a zai 1302 seat is retried to the default budget of 10 and
   then stamped with the exhaustion message. This is the mechanism behind the round's
   "429 ... (type=1302)" seat deaths; the link from `(type=1302)` transcript text to this
   regex is [INFERENCE] because no transcript was read by this seat.
4. `RESOURCE_EXHAUSTED` is handled as a gRPC status string
   (`n.status.trim().toUpperCase() !== "RESOURCE_EXHAUSTED"`); lowercase
   `resource_exhausted` has **0** matching lines in the binary. Contract C1's token list
   names only the lowercase form.

## 5. Observed: the exhaustion message and `errorStatus` persistence

Compiled-artifact excerpts (source text embedded in `omp/18.12.3`):

```
    } catch (k) {
      const h = await Zs(k, { api: t.api, signal: r?.signal, rawRequestDump: m });
      f.stopReason = h.stopReason;
      f.errorStatus = h.status;
      f.errorId = h.id;
      f.errorMessage = h.message;
```

```
        const v = this.#t - 1;
        e.errorMessage = `Retry budget exhausted after ${v} ${v === 1 ? "retry" : "retries"}: ${a}`;
        await this.#u({ success: false, attempt: v, finalError: a }, { terminalTurn: e, retryErrors: { status: "superseded" } });
```

```
        const p = !t.message.errorMessage.startsWith("Retry budget exhausted") && Me(Ts(t.message), N.EmptyResponse);
```

Meaning, observed: a terminal assistant error message carries numeric `errorStatus` (the HTTP
status handed in) and `errorId` (AIError bit flags), plus `errorMessage`, and the exhaustion
text is exactly `Retry budget exhausted after N retry|retries: <final error>`. These are plain
assignments on the message object, so they serialize with `type:"message"`.

Caveat: one path defines `errorId` with `enumerable: false`
(`Object.defineProperty(e, "errorId", { value: t, enumerable: false, configurable: true })`),
so `errorId` persistence is not guaranteed. `errorStatus` and `errorMessage` are enumerable
assignments in the shown catch block. Do not design on `errorId`.

## 6. Observed: `retryRecovery` marker (persisted, rewritten in place)

Exact object built by the retry chain, then written back:

```
          kind: "auto-retry",
          status: "recovered",
          attempt: n.attempt,
          recoveredAt: new Date().toISOString(),
          recovery: n.recovery,
          note: n.note,
          supersededBy: {
            timestamp: e.supersedingMessage.timestamp,
            ...e.supersedingMessage.responseId === undefined ? {} : { responseId: e.supersedingMessage.responseId },
            provider: e.supersedingMessage.provider,
            model: e.supersedingMessage.model
          }
```

and the moot variant:

```
          status: "superseded",
          attempt: n.attempt,
          recovery: n.recovery,
          note: n.note
```

It is attached as `o.message.retryRecovery = d` and followed by
`await this.#e.sessionManager.rewriteEntries();`. Messages carrying it are excluded from a
rebuilt model context (`N.message.role === "assistant" && (N.message.retryRecovery || E0(N.message))`
→ `return;`) but remain in the transcript, and `Ex()` renders `superseded` as `{ kind: "none" }`.

Docs corroborate the shape: "`RetryErrorUpdate` (`entryId`, `persistenceKey?`, `note`,
`retryRecovery`)" (`omp://non-compaction-retry-policy.md:243`) and "each persisted error entry
from the chain is marked with a `retryRecovery` marker"
(`omp://non-compaction-retry-policy.md:276`).

Privacy note: `note` is human-readable text (for example a short recovery phrase) and
`supersededBy` names provider/model/responseId. A read-only status tool must not emit these;
`status` and `attempt` are the safe projections.

## 7. Observed: seat identity does not come from a raw session filename

- Main transcripts: `<timestamp>_<sessionId>.jsonl` (`omp://session.md:42`), e.g.
  `2026-10-20T15-54-12-123Z_019c….jsonl`. Contract C1's seat id `TameshiR17.RR7-2` is not
  that shape.
- Subagent transcripts are nested: the stats parser classifies by depth
  (`packages/stats/src/parser.ts`):
  `return s.split(p.sep).length <= 2 ? "main" : "subagent";`
- Advisor transcripts are `__advisor.jsonl` or `__advisor.<x>.jsonl`
  (`var Ae = "__advisor.jsonl";` in the same parser).
- Vibe child session files are `<id>.jsonl` with `id` matching `/^[A-Za-z0-9_-]+$/`
  (`packages/coding-agent/src/registry/persisted-agents.ts`), so a dotted seat id cannot be
  one of those either.

[INFERENCE] A directory of files literally named `<seat>.jsonl` (as in the C1 fixtures) is a
curated mirror, not a raw `~/.omp/agent/sessions` tree. On a raw tree, the `seat`/`prefix`
tallies in C1 would bucket by timestamp prefix. The seat identity that exists in the record
stream is `session_init.agent` (optional field, `omp://session.md:411-413`), which C1
currently skips because only `type=="message"` is read.

## 8. Implications for C1 (advice only; L1 decides)

1. **`errorStatus` is supported** (observed §5). Keep it as the primary signal.
2. **`retries` regex is wrong for N=1.** The template is `after N retry` when N is 1
   (observed §5). Contract text says `after N retries`. Use `after (\d+) retr(?:y|ies)`.
   With default `maxRetries: 10` the observed incidents still read `retries: 10`.
3. **`dead_quota` is mostly unreachable when a 429 is present.** OMP maps quota text to
   status 429 (§4), and zai uses 429 for 1113/1308 (S043). Because C1 tests
   `errorStatus == 429` first, such seats classify `dead_rate_limit`. `dead_quota` is then
   only for quota text with no 429/no rate-limit token (e.g. `402`, `credits`). The class
   names overstate discrimination; the knowledge note should say so rather than claim a
   quota/rate-limit split.
4. **`retry_exhausted` is a useful discriminator.** Only retryable classes (408/429/5xx and
   transport) can exhaust; 4xx (other than 408/429) surfaces immediately (§4). So
   `retry_exhausted=false` with `stopReason=error` leans hard-error/quota, not rate limit.
5. **Terminal-role gap.** The role table (`omp://session.md:175-183`) includes `developer`,
   `bashExecution`, `pythonExecution`, `fileMention`. C1 defines classes only for assistant,
   `toolResult`, and `user`. TTSR emits developer reminders as separate messages after tool
   results (`omp://ttsr-injection-lifecycle.md:283`), so a `developer`-terminal tail is
   plausible. Fold every non-assistant terminal role into `incomplete` or the classifier has
   no defined branch.
6. **Seat identity needs a decision** (§7): either document that `--sessions-dir` points at a
   renamed mirror, or read `session_init.agent`/header fields. As written, `seat`/`prefix`
   on a raw tree is a filename census, not a seat census.
7. **Incidents are not countable.** Retry lifecycle events are not persisted entries; only
   `errorMessage` and the `retryRecovery` marker survive (observed §5-§6; entry taxonomy
   `omp://session.md:114-140` has no retry entry). Contract C1's "seats, not incidents"
   limitation is exact.
8. **`aborted` can be a resume artifact.** The synthetic aborted assistant message is written
   on resume from `session_exit` (`omp://session.md:333`). An `aborted` class does not prove a
   user abort.
9. **`length` folds into `incomplete`.** Output-cap stops are `stopReason:"length"`
   (`omp://provider-streaming-internals.md:145-147`) and are not errors; the class conflates
   "still working" with "output-capped". Acceptable, but state it.
10. **Provider/model attribution is the serving model.** After a fallback hop the terminal
    message's `provider`/`model` is the fallback model (`resolvedModelIsFallback`,
    `omp://session.md:229-232`). `by_provider_model` must not be read as the seat's declared
    model role.
11. **Tail-size edge.** If the final record alone exceeds `--max-tail-bytes`, the tail contains
    only a fragment of it; dropping the partial first line leaves zero complete records and the
    seat reads `unavailable` (contract-correct). `finalizeErrorMessage` embeds captured HTTP
    request diagnostics (`omp://provider-streaming-internals.md:157`), so a large final error
    record is possible. Fixtures should pin this case; scanning such a directory needs a larger
    tail.
12. **Coverage footnote.** Archived transcripts are `.jsonl.gz` and are not matched by
    `*.jsonl`; recoverable `.jsonl.*.bak` are likewise skipped. Filesystem compression
    (`omp gc --compress`) applies only to APFS and NTFS (`omp://session.md`, storage section),
    so on this Linux host transcripts remain plain text. Cold-archived seats are simply absent
    from a scan.
13. **Token list hygiene.** `resource_exhausted` is unobserved; the observed form is
    `RESOURCE_EXHAUSTED` (gRPC status). `RATE_LIMITED` matches only HTTP/2 library constants in
    the binary. Both are harmless as extra tokens but are not evidence-backed; matching
    case-insensitively for the resource-exhausted token is closer to the artifact.

## 9. Unknowns / not observed

- No real transcript was read (that read is another seat's assignment). Whether zai seat
  records actually carry `errorStatus: 429` and the exhaustion prefix is [INFERENCE] from
  §4-§5 plus the round context.
- `errorId` persistence is unresolved (non-enumerable definition path) and should not be used.
- Subagent transcript file naming under a task spawn is not directly observed; only vibe
  (`<id>.jsonl`) and advisor (`__advisor*.jsonl`) names are.
- Whether the fleet mirror renames transcripts to seat ids is not observed in this lane.
- Docs and binary are version-pinned to `omp/18.12.3`; a later harness may change field names
  or the exhaustion template.
- `retryRecovery.status == "recovered"` on the terminal record: expected to be impossible in
  practice because the successful message is appended after the marked error, but that
  ordering is [INFERENCE] from the rewrite code, not measured.

## 10. Commands run (all read-only; exit codes)

| Command | rc | Result |
|---|---|---|
| `sha256sum /home/vgpnk/.local/bin/omp` | 0 | `065b5079d65ff6b77d961c935ba808e8f0f569ca6a2cb7b5fb6a1e8da72d7dec` |
| `omp --version` | 0 | `omp/18.12.3` |
| `grep -a -c 'Retry budget exhausted after' /home/vgpnk/.local/bin/omp` | 0 | 2 matching lines (template + `startsWith` check) |
| `grep -a -c 'errorStatus' …` | 0 | 44 matching lines |
| `grep -a -c 'retryRecovery' …` | 0 | 12 matching lines |
| `grep -a -c 'resource_exhausted' …` | 1 | 0 matching lines |
| `grep -a -c 'RESOURCE_EXHAUSTED' …` | 0 | 10 matching lines |
| `grep -a -c 'RATE_LIMITED' …` | 0 | 20 matching lines, sampled matches are HTTP/2 library constants |
| `grep -a -c '1302' …` | 0 | 9 matching lines |

`grep -c` counts matching **lines** in a binary whose lines can be very long; counts are not
occurrence counts. Context was extracted with `grep -a -o`/`-A`/`-B` and read directly.

## Verdict

C1's transcript fields are grounded: `stopReason`, `errorStatus`, `errorMessage`, and the
`retryRecovery` shape exist and persist in `omp/18.12.3`, and "Retry budget exhausted after N
retries" is the harness's own final-failure wording. The claim's weak points are semantic,
not factual: a 429-first test will absorb quota deaths that OMP itself stamps 429; the retry
count regex misses the singular; terminal non-assistant roles are unclassified; and on a raw
sessions tree the seat id is a filename timestamp, not a seat name.
