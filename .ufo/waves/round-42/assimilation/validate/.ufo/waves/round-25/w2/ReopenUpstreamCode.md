# Wave 2 — ReopenUpstreamCode (S098, S099, S100, S112, S113)

author: MoriR25.ReopenUpstreamCode, 2026-10-22. Scope: re-open the five upstream source rows with curl,
record HTTP status and sha256, and check every quote and anchor in the lesson's `## Gate`
(`corpus/lessons/round-25.md`) and in each row's anchor column (`corpus/SOURCES.md:104-106,118-119`).

## Verdict

**Held.** All five rows re-open, re-download and re-verify. Every lesson `## Gate` quote is verbatim at its
cited line(s); every anchor line-range in the SOURCES rows is exact; both recorded sha256/size pairs that are
given in full match; the tag pin (v18.12.6 = `45c35e40c46166dc726ccc52f5d27f40f2449f99`) is confirmed through
the GitHub refs API. Two findings, both LOW/INFO, neither breaks a claim: a one-day date error in S099's
lineage note, and a truncated (16-hex) sha256 in S098's row.

## Re-fetch: HTTP status and sha256 (curl, 2026-10-22)

Command: `curl -sS -o <name> -w '%{http_code} %{size_download}' <url>` then `sha256sum`, run in `/tmp/reopen-r25`.

| Row | URL (ref) | HTTP | Bytes | sha256 (this fetch) | sha256 in SOURCES | Match |
|---|---|---|---|---|---|---|
| S098 | .../45c35e40.../src/async/job-manager.ts | 200 | 49,665 | `0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7` | `0f37afaaa822ef1d` (16-hex prefix only) | yes, prefix |
| S099 | .../45c35e40.../src/sdk.ts | 200 | 255,525 | `c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957` | full, identical | yes |
| S100 | .../45c35e40.../src/tools/settings.ts | 200 | 32,713 | `514974143d47db0c9765bc47e86dcb9a38bd6bc23113a4ffe557bff0d8e30507` | full, identical | yes |
| S112 | .../v18.12.6/src/tools/bash.ts | 200 | 67,415 | `d985ef25639993e05fb4de8c8b6dc75dde76422f63d1a295b95eb575e8cc3ea2` | full, identical (67,415 B) | yes |
| S113 | .../v18.12.6/src/tools/eval.ts | 200 | 41,679 | `01e9c5c56af15d3e04cdeaf99d959afa90129f8cbb015d6908e02795351920e3` | full, identical (41,679 B) | yes |

Tag pin: `GET /repos/can1357/oh-my-pi/git/ref/tags/v18.12.6` → `object.sha 45c35e40c46166dc726ccc52f5d27f40f2449f99`,
`type: commit` (a peeled lightweight tag, no tag-object indirection). So the S112/S113 tag URLs and the
S098-S100 commit URLs serve the same tree identity.

## Per-row checks (lesson Gate quote + row anchors + row prose)

### S098 — job-manager.ts — AGREE (held)

- Lesson Gate quote `:372` — line 372 is exactly
  `` `Background job limit reached (${maxRunningJobs}). Wait for running jobs to finish or cancel one.`, `` —
  verbatim, 14 words (≤25). It is the cap check's throw site, cited as "cap check and throw:369-374":
  369 `const maxRunningJobs = this.#maxRunningJobs;`, 370 `if (activeCount >= maxRunningJobs)`, 371-373 throw,
  374 close. Exact.
- `DEFAULT_MAX_RUNNING_JOBS:43` — line 43 `const DEFAULT_MAX_RUNNING_JOBS = 15;`. Exact.
- `queued-flag doc:118-123` — doc comment 118-122 ("Queued jobs do not count toward the running-job limit
  until the caller invokes `markRunning()`"), field `queued?: boolean;` at 123. Exact.
- `maxRunningJobs option:170-171` — 170 doc ("a function is re-read on every capacity check so a live setting
  resizes the cap"), 171 `maxRunningJobs?: number | (() => number);`. Exact.
- `#maxRunningJobs getter:330-335` — 331-334: `typeof option === "function" ? option() : option`, then
  `Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS))`. Confirms all three scope claims: floors at 1,
  re-reads a function option, and the 15 fallback applies only when the option is undefined (`??`), so it is
  not the effective cap. Exact.
- `atCapacity count:337-346` — 340 comment "Mirror register(): queued jobs hold no execution slot", loop
  counts `job.status === "running" && !job.queued`. Running-and-not-queued rule confirmed.
- `register count:363-368` — the same running-and-not-queued loop inside `register(` (which starts at 348),
  immediately before the 369-374 throw. Exact.
- Row decision ("registering past the cap throws a fixed Background job limit reached error") matches: the
  message text is a constant template; only the number interpolates.

### S099 — sdk.ts — AGREE (held), one LOW date finding

- Lesson Gate quote `:2284` — line 2284 is exactly
  `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),` — verbatim.
- `guard :2282` — 2282 `const asyncJobManager = !options.parentTaskPrefix` (children get `: undefined` at
  2286 and use the parent's manager; root-sessions-only guard confirmed). `clamp :2284` — as above. Range
  2282-2284 covers guard+construction+clamp. Exact.
- `import of AsyncJobManager :53` — line 53 `import { AsyncJobManager } from "./async";`. Exact.
- `cfgAsyncMaxJobs import :326` — line 326 `cfgAsyncMaxJobs,` in the `./tools/settings` import block. Exact.
- **"the single shipped construction of AsyncJobManager at v18.12.6"** — verified across the whole repo, not
  just the file: downloaded the full source tarball at `45c35e40` (codeload, HTTP 200, 76,435,207 B) and
  searched every `.ts` for `new AsyncJobManager(`. In shipped source there is exactly one hit, `src/sdk.ts:2283`.
  All other hits (40+) are under `test/` and test `fixtures/` — not shipped. Also exactly one
  `Math.min(100, cfgAsyncMaxJobs.get` in the repo. Consistent with S102's one-site binary claim.
- Clamp lineage (anchor column): all five commits fetched via the GitHub commits API.
  - `476b858b3a4a` 2026-02-22T11:44:23Z "feat(coding-agent): added async background job execution with
    configurable concurrency limits" — touches `src/async/job-manager.ts` and settings schema; the next
    commit's diff shows the `Math.min(100, ...)` clamp already in place before it, so "the clamp ships with
    the 2026-02-22 feature" holds. Also the S104 commit (message identical to S104's quote).
  - `944d7f8d8d44` 2026-02-26T11:34:29Z "increased async max jobs limit to 100 for concurrency" — sdk.ts diff:
    `Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15))` → `... ?? 100`. "Default 15 to 100"
    confirmed (it is the `??` fallback that moves).
  - `6962d5cd2ef1` 2026-09-24T18:04:41Z "implemented centralized settings registry and internal URL routing" —
    job-manager.ts diff: `maxRunningJobs?: number` → `number | (() => number)`, option stored, and a
    `get #maxRunningJobs()` introduced that re-evaluates per check. Live re-read ("live closure") confirmed at
    the job-manager level; see gap G3 for the sdk.ts side of this commit.
  - `c4a2441d8f91` — sdk.ts diff: `Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100)` →
    `Math.min(100, cfgAsyncMaxJobs.get(settings))`. "Fallback removed" confirmed. **Date finding F1 below.**
  - `9ce580c11eb3` 2026-10-10T16:16:27Z "fix(sdk): isolated async jobs for concurrent roots" — diff removes
    `!AsyncJobManager.instance()` and the singleton scoping line and lands the current
    `const asyncJobManager = !options.parentTaskPrefix ? new AsyncJobManager({...}) : undefined` form.
    "Guard simplified" confirmed; this is byte-identical in intent to today's 2282-2286.
  - Twinned SHAs `3ce6a68380f1` and `d38e1d55e1b2` resolve with the same messages and author dates as
    `476b858b` (2026-02-22) and `944d7f8d8d` (2026-02-26) respectively — consistent with "twinned upstream as".

### S100 — tools/settings.ts — AGREE (held)

- Lesson Gate quote `:941-946` — the cited block is 941 `export const cfgAsyncMaxJobs = register({`, 942
  `id: "async.maxJobs",`, 943 `protocolDefault: ["rpc"],`, 944 `type: "number",`, 945 `default: 100,`, 946
  `});`. The lesson quote is the verbatim concatenation of lines 942-945, pinned to the block — located and
  accurate; nothing in the block contradicts it.
- Anchor sub-lines (id:942, protocolDefault:943, type:944, default:945) — all exact.
- Row prose: "registers no `ui` block" — confirmed: the register call closes at 946 with no `ui` key, unlike
  every neighbouring setting in the file. "The schema states the configured value, not the effective cap" —
  consistent; nothing in the definition references a cap.

### S112 — tools/bash.ts — AGREE (held)

- Lesson Gate quote `:1221-1222` — 1221 `// At the running-job cap, fall through to direct foreground execution`
  and 1222 `// instead of failing every bash call until a slot frees up.` The lesson quote is the verbatim
  16-word prefix (≤25), eliding "until a slot frees up." (see note N1). Accurate.
- `explicit async branch 1188-1192` — 1188 `if (asyncRequested) {`, 1189-1191 manager-missing throw, 1192
  `const job = this.#startManagedBashJob({` — no capacity pre-check anywhere in the branch. `:843
  #startManagedBashJob` — exact (line 843). `:882 manager.register` — exact (line 882); the only throw on cap
  is inside `register` itself (job-manager 369-374). "Explicit `async: true` registers without a pre-check"
  confirmed.
- `auto-background guard:1220-1229` — 1220 `const autoBgManager = ...`, 1221-1222 comment, 1223-1229
  condition containing `!autoBgManager.atCapacity` at 1228. `atCapacity` occurs exactly once in the whole
  file (grep: line 1228 only), so the auto-background branch is the sole pre-check. Confirmed.

### S113 — tools/eval.ts — AGREE (held)

- Lesson Gate quote `:534-535` — 534 `// At the running-job cap, fall through to direct foreground execution`
  and 535 `// instead of failing every eval call until a slot frees up.` Verbatim 16-word prefix (note N1).
- `eval.ts:533-538` — 533 `const autoBgManager = session.asyncJobManager;`, 534-535 comment, 536
  `if (!cfgEvalAutoBackgroundEnabled.get(...) || !autoBgManager || autoBgManager.atCapacity) {`, 537
  `return await run(signal, emitToolUpdate);`, 538 `}`. Matches the anchor's `atCapacity → return await run(...)`
  exactly; `atCapacity` occurs exactly once in the file (grep: line 536). Confirmed.

## Findings

- **F1 (LOW) — S099 anchor column, wrong day on one lineage commit.** The row says "fallback removed
  2026-09-25 by c4a2441d8f"; the GitHub commits API gives author 2026-09-24T23:02:43Z and committer
  2026-09-24T23:02:53Z for `c4a2441d8f91` — both 2026-09-24 UTC. 09-25 is true only in UTC+9 or later.
  Smallest fix: in `corpus/SOURCES.md` row S099 change "2026-09-25" → "2026-09-24" (or "2026-09-24T23:02Z").
  No downstream claim depends on the day; the sha and the change itself are correct.
- **F2 (INFO) — S098 row stores a truncated sha256.** The anchor column records `0f37afaaa822ef1d`
  (16 hex) where every sibling row records the full 64-hex digest. This fetch's full value:
  `0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7`. Smallest fix: extend the stored prefix
  to the full digest so the row is byte-checkable like the others.
- **N1 (INFO, no fix needed) — S112/S113 lesson quotes are mid-sentence truncations.** Both elide
  "until a slot frees up." without an ellipsis. Within the lesson's own ≤25-word rule and not misleading —
  the elided tail weakens rather than strengthens the claim. Optional: keep as is.

## Residual risk and verification gaps

- G1: S098's committed sha evidence is only a 16-hex prefix (F2); the full-digest match is my measurement,
  so until the row is extended, the row itself proves less than my re-fetch does.
- G2: "Accessed" timestamps in the lesson/rows (e.g. S098 2026-10-22T10:10:54Z) are historical claims I
  cannot re-observe; I verified today's fetch only.
- G3: For `6962d5cd2ef1` the GitHub API returned no patch hunk for sdk.ts (large-file patch elision), so the
  sdk.ts-side introduction of the `() =>` closure at that commit is inferred from the same-day chain —
  `c4a2441d8f91` (23:02Z) is seen removing `?? 100` from an already-closure-shaped line, and the
  job-manager.ts diff of `6962d5cd2ef1` (18:04Z) introduces the function option and live getter. The chain is
  coherent but the one sdk.ts hunk was not displayed.
- G4: Twinned SHAs were verified to resolve with matching message and author date only; their trees were not
  diffed.
- G5: S102 (installed binary) is outside this assignment; the one-clamp-site claim was checked in source only.
- Housekeeping: the 225 MB tarball extract and download were removed from `/tmp/reopen-r25` after verification.
  No tools were installed or upgraded for this task (curl/python3/tar as shipped); no lane bytes other than
  this report were written.
