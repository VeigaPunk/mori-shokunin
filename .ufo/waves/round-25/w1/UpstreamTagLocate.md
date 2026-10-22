# UpstreamTagLocate — omp 18.12.6 upstream ref and source rows

Seat `MoriR25.UpstreamTagLocate`, round 25 wave 1, 2026-10-22. Read-only. No lane commits,
no tool installs, no omp run. Scratch bytes live in `/tmp`; this file is the only lane write.

## 1. Ref resolution — tag `v18.12.6` → commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`

| Fact | Evidence |
|---|---|
| Release exists | `curl https://api.github.com/repos/can1357/oh-my-pi/releases/tags/v18.12.6` → HTTP 200, release id `420053191`, `"tag_name": "v18.12.6"`, `"target_commitish": "main"`, `"published_at": "2026-10-21T21:02:53Z"`, `"draft": false`, `"prerelease": false` |
| Tag is lightweight (points straight at a commit) | `curl .../git/ref/tags/v18.12.6` → HTTP 200, `"ref": "refs/tags/v18.12.6"`, `"object": {"sha": "45c35e40c46166dc726ccc52f5d27f40f2449f99", "type": "commit"}` |
| Tree carries the version | `packages/coding-agent/package.json:3` → `"version": "18.12.6"` (raw fetch HTTP 200, 16,030 bytes, sha256 `83c96c5097f69c0b6f13b7fb9a9b940d7f9078136154518243746765628d057b`) |
| Installed binary **is** the v18.12.6 linux-x64 asset | `~/.local/bin/omp`: size 256,702,432, sha256 `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`. Release asset `omp-linux-x64`: size 256,702,432, API `"digest": "sha256:85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4"`. Binary contains the literal `18.12.6` (9 occurrences) |

Tag-URL and commit-URL raw bytes are identical for every file below (sha256 equality, checked
for job-manager.ts, sdk.ts, tools/settings.ts and docs/settings.md), and each local copy hashes
to the git blob id recorded in the commit tree:

| Path | Tree blob id | Local `git hash-object` |
|---|---|---|
| packages/coding-agent/src/async/job-manager.ts | `1bad521c6e24151f88956830865aa59ac0feb0da` | equal |
| packages/coding-agent/src/sdk.ts | `fbf834ae39840058fd76493e6a721e191246048a` | equal |
| packages/coding-agent/src/tools/settings.ts | `344893bc9ae31d3ecc7eeeab0684bbb98606328c` | equal |
| docs/settings.md | `09e8edb169736fda0ae538ec5840988f417b3959` | equal |

## 2. Fetched files (all HTTP 200)

Base: `https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/`

| File | Bytes | sha256 |
|---|---|---|
| packages/coding-agent/src/async/job-manager.ts | 49,665 | `0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7` |
| packages/coding-agent/src/sdk.ts | 255,525 | `c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957` |
| packages/coding-agent/src/tools/settings.ts | 32,713 | `514974143d47db0c9765bc47e86dcb9a38bd6bc23113a4ffe557bff0d8e30507` |
| docs/settings.md | 148,359 | `0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883` |

## 3. Report rows

Quotes are verbatim; the multi-line schema quote folds line breaks to single spaces. All quotes
are ≤25 words. Binary offsets are byte offsets in `~/.local/bin/omp`
(sha256 `85d9daf3…ccfa4`); that binary contains the `// packages/coding-agent/src/async/job-manager.ts`
module banner at byte 160031363.

### R1 — job-manager.ts, DEFAULT max

- Raw URL: `…/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/async/job-manager.ts` → HTTP 200, 49,665 bytes, sha256 `0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7`.
- Anchor: `packages/coding-agent/src/async/job-manager.ts:43`
- Quote (4 words): `const DEFAULT_MAX_RUNNING_JOBS = 15;`
- Binary: **matches** — bundle has `var v = 15;` at byte 160031518 inside the job-manager module, consumed by the getter as `t ?? v`. Identifier minified, value identical.

### R2 — job-manager.ts, `#maxRunningJobs` getter

- Anchor: `job-manager.ts:330-335` (comment at 330, `get #maxRunningJobs(): number {` at 331)
- Quote (5 words, line 334): `return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));`
- Extra anchor: option declaration `job-manager.ts:170-171` — `/** Running-job cap; a function is re-read on every capacity check so a live setting resizes the cap. */` / `maxRunningJobs?: number | (() => number);`
- Binary: **matches** — byte 160032730: `get #R() { const e = this.#P; const t = typeof e === "function" ? e() : e; return Math.max(1, Math.floor(t ?? v)); }`. Same expression, minified names only.

### R3 — job-manager.ts, running-count rule (queued jobs do not count)

- Anchors: `job-manager.ts:337-345` (`atCapacity`) and `job-manager.ts:365-370` (`register`)
- Quote (7 words, line 343): `if (job.status === "running" && !job.queued) activeCount++;`
- Extra anchors: line 345 `return activeCount >= this.#maxRunningJobs;`; line 370 `if (activeCount >= maxRunningJobs) {`
- Binary: **matches** — `atCapacity` at byte 160032863: `if (t.status === "running" && !t.queued) e++; … return e >= this.#R;`; `register` at byte 160033342: `if (u.status === "running" && !u.queued) r++;`. Queued jobs are excluded in both.

### R4 — job-manager.ts, limit-reached throw

- Anchor: `job-manager.ts:371-373`
- Quote (14 words, line 372): `` `Background job limit reached (${maxRunningJobs}). Wait for running jobs to finish or cancel one.` ``
- Appears once in the source (`grep -c 'limit reached' job-manager.ts` → 1).
- Binary: **matches** — byte 160033342: ``throw new Error(`Background job limit reached (${o}). Wait for running jobs to finish or cancel one.`);``. Only the template variable name differs. The same message also appears split in the string table at byte 95794256 as `Background job limit reached (` + `). Wait for running jobs to finish or cancel one.`

### R5 — construction site with `Math.min(100, …)`

- Anchor: `packages/coding-agent/src/sdk.ts:2282-2286`; quote at line 2284.
- Quote (5 words): `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),`
- Context anchors: `sdk.ts:53` `import { AsyncJobManager } from "./async";`; `sdk.ts:326` `cfgAsyncMaxJobs` inside the import block that closes `} from "./tools/settings";` at `sdk.ts:339`; guard `sdk.ts:2282` `const asyncJobManager = !options.parentTaskPrefix`.
- Binary: **matches** — byte 164406753: `new Xm({ maxRunningJobs: () => Math.min(100, XPe.get(R)) })`. It is the **only** `new Xm(` in the bundle (count 1), and the contract's clamp regex matches exactly once with value 100.

### R6 — settings schema for `async.maxJobs`

- Anchor: `packages/coding-agent/src/tools/settings.ts:941-946`
- Quote (8 words, line breaks folded): `id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100,`
- Binary: **matches** — byte 155231574: `var XPe = h({ id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100 });`. The contract's setting regex (`id: "async.maxJobs" … default: (\d+)`) matches once with `100`. The second `async.maxJobs` hit (byte 96085908) is the settings-UI label table, not a second definition.

### R7 — docs page describing `async.maxJobs`

- Anchor: `docs/settings.md:623`
- Quote (15 words): ``| `async.maxJobs` | number | `100` | Running background-job cap, floored to at least 1; parked/queued jobs do not consume execution slots. |``
- Coverage: this is the only `maxJobs` mention in the fetched docs. `grep -c maxJobs` → settings.md 1; README.md, docs/cli-reference.md, docs/session.md, docs/tools/bash.md, docs/tools/task.md, docs/tools/wait.md, docs/config-usage.md, docs/stream.md all 0 (each raw fetch HTTP 200).
- Binary: **not applicable** — docs prose is not compiled into the binary (exact sentence count 0). The value the row documents (100) *is* carried, as the R6 schema default.

## 4. Discrepancy with the contract wording

The contract says "the session/sdk file that constructs the manager". At `45c35e40` there is no
`packages/coding-agent/src/session/sdk*` path (tree query returned empty). The constructor call is
in the top-level `packages/coding-agent/src/sdk.ts:2283`.

## 5. What this fixes for the C2 tool

- Observed: the shipped bundle has exactly one `AsyncJobManager` construction and it always passes
  the function form `() => Math.min(100, cfg.get(settings))` (`sdk.ts:2282-2286`, binary byte
  164406753).
- [INFERENCE] Therefore the source default `DEFAULT_MAX_RUNNING_JOBS = 15` (R1) is unreachable in
  shipped sessions: with `async.maxJobs` absent the schema default 100 flows through, and with it
  set the configured value is clamped at 100. The effective cap is always
  `max(1, floor(min(100, base)))`, which is exactly rule 4 of the C2 tool.

## 6. Proposed SOURCES.md rows (next free id: S098; current max is S097)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S098 | oh-my-pi async/job-manager.ts at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/async/job-manager.ts | code | A | the `AsyncJobManager` running-job cap: the module default 15, the `#maxRunningJobs` getter that floors at 1 and re-reads a function option, the running/non-queued count rule and the limit-reached throw; v18.12.6 only | async/job-manager.ts:43; getter:330-335; atCapacity:337-345; register count:365-370; throw:371-373; tag v18.12.6 = commit 45c35e40c46166dc726ccc52f5d27f40f2449f99; sha256 0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7 | The manager caps concurrently running jobs, not registered jobs: queued jobs hold no slot, the cap is re-read per check and floored at 1. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S099 | oh-my-pi sdk.ts at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/sdk.ts | code | A | the single shipped construction of `AsyncJobManager`: every root session passes `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))`, so the setting is clamped at 100 before the manager floors it at 1; v18.12.6 only | sdk.ts:2282-2286; import at 53; `cfgAsyncMaxJobs` import at 326 from `./tools/settings` | The 100 clamp lives at the construction site, not in the job manager, so no shipped session can run more than 100 concurrent async jobs whatever the config says. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S100 | oh-my-pi tools/settings.ts at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/tools/settings.ts | code | A | the `async.maxJobs` setting definition: a number setting with `protocolDefault: ["rpc"]` and default 100; v18.12.6 only | tools/settings.ts:941-946 (id:942, type:944, default:945) | `async.maxJobs` is a declared numeric setting whose default is 100, the value the sdk clamp also uses. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S101 | oh-my-pi docs/settings.md at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md | docs | A | the documented entry for `async.maxJobs`: type number, default 100, floored to at least 1, queued jobs excluded; v18.12.6 only | docs/settings.md:623; sha256 0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883 | The project documents `async.maxJobs` as the running background-job cap with default 100, a floor of 1 and no slot for parked/queued jobs. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S102 | Installed omp 18.12.6 binary — `~/.local/bin/omp` (own-work) | own-work | A | bytes of the installed binary that carry the job cap: byte-identical to release asset `omp-linux-x64` (sha256 `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`, 256,702,432 bytes; release API digest equal), containing the clamp, schema default 100 and source default 15 | clamp: `maxRunningJobs: () => Math.min(100, XPe.get(R))` at byte 164406766; schema `var XPe = h({ id: "async.maxJobs", … default: 100 })` at 155231574; manager default `var v = 15;` at 160031518; throw at 160033342; version string `18.12.6` | The installed binary is the v18.12.6 linux-x64 release asset and carries the same clamp (100), setting default (100), manager default (15) and throw text as the tagged source. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |

## 7. Facts, inference, gaps

Facts (all observed above): ref resolution, byte identity of raw/tag/commit/tree-blob, release-asset
digest equality with the installed binary, and every quote's presence in the binary (R1–R6) or
absence of doc prose from it (R7).

[INFERENCE] The source default 15 is dead in shipped wiring (§5); the sampled docs set is not proven
exhaustive beyond the files listed in R7.

Gaps: no upstream commit or PR rationale for the 100 clamp was traced (no commit message inspected);
the docs row does not state session-vs-global scope; GitHub's asset `digest` is an API claim,
corroborated here by size equality and the embedded version string but not by re-downloading the
256 MB asset.

## 8. Commands run / installs

`curl` to `api.github.com` (release, tag ref, tree, release assets) and `raw.githubusercontent.com`
(commit and tag URLs); `python3` for sha256, git-blob hashing and byte-offset probes; `strings`/`grep`
and Python byte searches on `~/.local/bin/omp`. No omp execution, no settings writes, no jj/git
writes. Tool installs this seat: **none**.
