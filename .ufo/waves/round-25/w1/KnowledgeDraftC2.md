# KnowledgeDraftC2 — round 25, claim C2 knowledge draft (harness background-job runway)

Seat: `MoriR25.KnowledgeDraftC2` (scribe, leaf). Claim: **C2 — harness background-job runway
capability** (contract `.ufo/waves/round-25/contract.md`, C2).

Scope of this seat: **draft the knowledge entry and hand it to the L1 in this report.** The entry
itself is **not** written into the lane: `corpus/knowledge/harness-job-capacity-r25.md` does not
exist and was not created. No `SOURCES.md` row was added (the registry is the L1's to admit; this
draft cites the rows proposed by wave-1 seat `MoriR25.UpstreamTagLocate` as `S###` placeholders).
No tool was written, no tool was run against the harness, no omp invocation, no settings edit, no
lane commit, no jj command at the fleet root.

---

## 1. Behavior the draft establishes

The draft is the knowledge note for the C2 surface: the **effective background-job cap of the
omp harness**, the rule that counts against it, the exact refusal text, and what the cap does and
does not mean for the hyaku seat gate and for a lane observer. It is shaped on
`corpus/knowledge/system-pressure-r24.md` (frontmatter/source line, `## Scope`, `## Facts F#`,
`## Decision table`, `## Limits`, `## [UNKNOWN]`, `## Not claimed`).

Facts the draft asserts, each from bytes this seat opened:

| # | Fact | Primary source opened |
|---|---|---|
| F1 | `async.maxJobs` is a registered number setting with `default: 100`; upstream docs call it the "Running background-job cap, floored to at least 1; parked/queued jobs do not consume execution slots" | S100 (`tools/settings.ts:941-946`), S101 (`docs/settings.md:623`), S102 (binary bytes) |
| F1b | Upstream prose names the ceiling: the session-wide cap is "default and maximum 100", shared with every background job in the session; the settings page itself states **no maximum** | S103 (`docs/tools/eval.md:258`, verified HTTP 200, sha256 `fb2fc4a1…495c`) |
| F2 | The clamp is **at the construction site**, not in the manager: `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))` | S099 (`sdk.ts:2282-2286`), S102 (binary byte 164406766) |
| F3 | Effective cap = `max(1, floor(min(100, base)))`, `base` = configured value or the schema default 100; the manager's own default 15 is unreachable in shipped wiring **[INFERENCE]** | S098 (`job-manager.ts:43,330-335`), S099, S102 |
| F4 | Count rule: jobs with `status === "running" && !job.queued`; **no type filter** — every type (`bash`, `task`, `eval`) draws on the same runway | S098 (`job-manager.ts:48,337-345,363-370`) |
| F5 | A task job is registered `queued: true` and only counts after `markRunning()`; a bash job counts from registration | `task/index.ts:1565,1490`; `tools/bash.ts:882` |
| F6 | Exact error text: ``Background job limit reached (${maxRunningJobs}). Wait for running jobs to finish or cancel one.``; the number is the effective cap, re-read at every check | S098 (`job-manager.ts:170-171,371-373`), S102 |
| F7 | **Only a top-level session** (`!options.parentTaskPrefix`) constructs the manager; children borrow the parent's manager, so the cap is one number per root session tree | S099 (`sdk.ts:2282,2315,4789-4791`) |
| F8 | A refusal creates nothing: `register()` throws before the job record, the `AbortController` and the run; the task tool discards that spawn's run and returns `Failed to start background task job(s): …` with `results: []` | S098 (`job-manager.ts:365-374` vs `:378-396`); `task/index.ts:1213,1220-1230` |
| F9 | Reaching the cap is **not** always an error: the bash and eval auto-background branches pre-check `atCapacity` and fall back to direct foreground execution; only registration paths (explicit `async: true` bash, task spawns) throw | S118 (`tools/bash.ts:1224-1229`), S119 (`tools/eval.ts:535-538`), S098 (`job-manager.ts:337-346`); `grep -rn atCapacity` over the tag's `src` returns exactly three hits |
| F10 | The fleet's own ground-truth notes carry this refusal text with the number 100 | `.ufo/waves/round-20/build/GtLaneKasegi.md:48`, `.ufo/waves/round-20/build/GtLaneKama.md:72` (lane records, not registry rows) |
| F11 | The hyaku seat gate measures a **different population** under a **different number**: `wave-slot.sh` defaults `CAP=200` over a live-agent estimate, the harness cap is 100 over running non-queued jobs | `scripts/hyaku/wave-slot.sh:28-49,62-96` (read-only) |
| F12 | This host: config 200, clamp 100 → effective 100, `RUNWAY_CLAMPED`, exit 1 | the operator's OMP settings file; `.ufo/waves/round-25/w1/BuildJobRunwayTool.md` §2 |
| F13 | The tool reads one global config file; the runtime settings stack also has a project layer, `--config` overlays and runtime overrides that the tool cannot see | `config/settings.ts:587-595,1561-1620` |

## 2. Gates — commands run and their outputs

Read-only. Nothing wrote outside this report file.

```
$ ls -l ~/.local/bin/omp; file ~/.local/bin/omp; sha256sum ~/.local/bin/omp; ~/.local/bin/omp --version
-rwxr-xr-x 1 vgpnk vgpnk 256702432 Oct 21 20:37 /home/vgpnk/.local/bin/omp
ELF 64-bit LSB executable, x86-64 … not stripped
85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4  /home/vgpnk/.local/bin/omp
omp/18.12.6
```
(`omp --version` is a version query, not a harness run: it prints the version and exits. No
session, no job manager, no settings write. Everything else below reads bytes only.)

**Clamp site (installed binary, byte search):**

```
$ python3 - <<'PY'   # regex from contract C2 rule 2 over the raw bytes
clamp matches: 1
164406766 maxRunningJobs: () => Math.min(100, XPe.get(R))
  context: …
  const Ui = !u.parentTaskPrefix ? new Xm({
    maxRunningJobs: () => Math.min(100, XPe.get(R))
  }) : undefined;
```

**Setting default (installed binary):**

```
setting_default matches: 1
155231590 id: "async.maxJobs",
  protocolDefault: ["rpc"],
  type: "number",
  default: 100
```

**Error text (installed binary, two occurrences):**

```
95794256   Background job limit reached (
160033359  Background job limit reached (${o}). Wait for running jobs to finish or cancel one.`);
```

**Manager body (installed binary, byte 160031363 onward, minified):**

```
// packages/coding-agent/src/async/job-manager.ts
var g = 500; var p = 30000; var y = 200; var f = 5*60*1000; var A = 30000; var w = 60000; var J = f; var v = 15;
…
get #R() { const e = this.#P; const t = typeof e === "function" ? e() : e; return Math.max(1, Math.floor(t ?? v)); }
get atCapacity() { … if (t.status === "running" && !t.queued) e++; … return e >= this.#R; }
register(e, t, s, n) { … for (const u of this.#e.values()) { if (u.status === "running" && !u.queued) r++; }
  const o = this.#R; if (r >= o) { throw new Error(`Background job limit reached (${o}). Wait for running jobs to finish or cancel one.`); }
```

**Upstream at tag `v18.12.6` = commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`**

```
$ git ls-remote --tags https://github.com/can1357/oh-my-pi | grep 18\.12
45c35e40c46166dc726ccc52f5d27f40f2449f99	refs/tags/v18.12.6

$ curl -sSL https://codeload.github.com/can1357/oh-my-pi/tar.gz/refs/tags/v18.12.6  → 225M extracted
$ sha256sum packages/coding-agent/src/{async/job-manager.ts,sdk.ts,tools/settings.ts,task/index.ts,tools/bash.ts}
0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7  …/async/job-manager.ts
c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957  …/sdk.ts
514974143d47db0c9765bc47e86dcb9a38bd6bc23113a4ffe557bff0d8e30507  …/tools/settings.ts
cd1df9be9086ae151a8053688b99c869179413a221a9a0e519a5c8af9cc82b06  …/task/index.ts
d985ef25639993e05fb4de8c8b6dc75dde76422f63d1a295b95eb575e8cc3ea2  …/tools/bash.ts
```

Upstream anchors opened (line numbers are of the files above at that commit):

* `packages/coding-agent/src/async/job-manager.ts:43` — `const DEFAULT_MAX_RUNNING_JOBS = 15;`
* `…/job-manager.ts:48` — `export type AsyncJobType = "bash" | "task" | "eval";`
* `…/job-manager.ts:170-171` — option type + the comment "a function is re-read on every capacity check so a live setting resizes the cap"
* `…/job-manager.ts:330-335` — `get #maxRunningJobs()` → `Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS))`
* `…/job-manager.ts:337-345` — `atCapacity` → `if (job.status === "running" && !job.queued) activeCount++;`
* `…/job-manager.ts:363-373` — `register()` count loop + the throw with the exact text
* `…/sdk.ts:2282-2286` — `const asyncJobManager = !options.parentTaskPrefix ? new AsyncJobManager({ maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)) }) : undefined;`
* `…/sdk.ts:2315` — `const scopedAsyncJobManager = asyncJobManager ?? options.asyncJobManager;`
* `…/sdk.ts:4789-4791` — "Children borrow their parent's manager but never dispose it."
* `…/tools/settings.ts:941-946` — `export const cfgAsyncMaxJobs = register({ id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100 });`
* `…/tools/settings.ts` line 1046 of `task/index.ts` — `logger.warn("task: no AsyncJobManager registered; falling back to sync execution")`
* `…/task/index.ts:1490` (`markRunning()`), `:1565` (`queued: true`), `:1213` (`spawn.run?.discard(...)`), `:1220-1230` (`Failed to start background task job…`, `results: []`)
* `…/tools/bash.ts:882` — `manager.register("bash", …)`
* `docs/settings.md:623` — `| \`async.maxJobs\` | number | \`100\` | Running background-job cap, floored to at least 1; parked/queued jobs do not consume execution slots. |`
* `docs/tools/eval.md:258` — "every handle is a running background job counted against the session-wide
  `async.maxJobs` cap (default and maximum 100) … which it shares with every other background job in
  the session, including async `bash`, async `task` spawns, `workpool()` pools and nested subagents'
  jobs. `agent()` fails with `Background job limit reached` once that cap is full."

**Upstream docs fetched independently (not taken on report):**

```
$ curl -sS -o /tmp/eval.md -w "%{http_code}\n" \
    "https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/tools/eval.md"
200
$ sha256sum /tmp/eval.md docs/tools/eval.md
fb2fc4a139ba187f1cc062fab53bd72a48dd13b1f81f0c3318ec7a79d41e495c  /tmp/eval.md
fb2fc4a139ba187f1cc062fab53bd72a48dd13b1f81f0c3318ec7a79d41e495c  docs/tools/eval.md
$ grep -rn "async.maxJobs" docs/ | head
docs/settings.md:623:| `async.maxJobs` | number | `100` | Running background-job cap, floored to at least 1; parked/queued jobs do not consume execution slots. |
docs/tools/eval.md:258:… session-wide `async.maxJobs` cap (default and maximum 100) …
```
(only two files in `docs/` mention `async.maxJobs`; the anchor was named to wave-1 seat
`MoriR25.SrcRejections` over IRC and was re-opened byte-for-byte here before use.)

**Capacity pre-checks (independent re-verification of the same caveat):**

```
$ grep -rn "atCapacity" --include=*.ts packages/coding-agent/src
./async/job-manager.ts:338:	get atCapacity(): boolean {
./tools/bash.ts:1228:			!autoBgManager.atCapacity
./tools/eval.ts:536:		if (!cfgEvalAutoBackgroundEnabled.get(session.settings) || !autoBgManager || autoBgManager.atCapacity) {
$ sha256sum packages/coding-agent/src/tools/bash.ts packages/coding-agent/src/tools/eval.ts
d985ef25639993e05fb4de8c8b6dc75dde76422f63d1a295b95eb575e8cc3ea2  …/src/tools/bash.ts   (67,415 B)
01e9c5c56af15d3e04cdeaf99d959afa90129f8cbb015d6908e02795351920e3  …/src/tools/eval.ts   (41,679 B)
```
`tools/bash.ts:1224-1229` — "At the running-job cap, fall through to direct foreground execution
instead of failing every bash call until a slot frees up", guard `!autoBgManager.atCapacity`.
`tools/eval.ts:535-538` — the same sentence for eval, guard `autoBgManager.atCapacity` →
`return await run(...)` (foreground).
`tools/bash.ts:1187-1208` — the explicit `asyncRequested` branch calls `#startManagedBashJob`
without any `atCapacity` pre-check, so it reaches `manager.register` (`tools/bash.ts:882`) and
throws. Exactly three hits for `atCapacity` exist in the shipped `src`: the getter plus those two
consumers. (Anchor named to wave-1 seat `MoriR25.SrcRejections`; re-opened here before use.)

**Host config (read-only):**

```
$ grep -n 'async:' -A1 the operator's OMP settings file
async:
  maxJobs: 200
```

**Hyaku seat gate (read-only, `scripts/hyaku/wave-slot.sh`):**

* `configured_cap()` (lines 28-49): `HYAKU_WAVE_CAP` (environment) → `$STATE/wave-cap` (state) → else `value=200; source=default`.
* `fits_cap()` (50-58): grants only while `used < cap`.
* `acquire` (68-96): `used = live + pending + seats`, `live` from `scripts/hyaku/wave-live.py`, `pending` from the ledger's last 120 s; also requires `MemAvailable ≥ 6144 MB`.
* Script header (own note, not a spec): "Observed 2026-10-21: L1 sessions kept dispatching full waves (~160 jobs at once overall) while Main's own spawns were refused with 'Background job limit reached (100)'."
* sha256 `41b487ef51012c099ab704e8c226f3bb701e11c120f7c6973ab73cb1f3737a81` (gate), `ee02129280d001c25fed528da5d1fc49ad7884c4205242f08ea15e5f10c73126` (`wave-live.py`).

**Host settings layers (read-only):** `/home/vgpnk/Projects/shokunin/.omp` holds only `agents/` (no
`config.yml`); `mori-shokunin/.omp` does not exist; the global file is the operator's OMP settings file
(`config/settings.ts:674-675`, `MAIN_CONFIG_FILENAMES`).

## 3. Touched surfaces

| Path | Change |
|---|---|
| `.ufo/waves/round-25/w1/KnowledgeDraftC2.md` | **this report — the only lane write** |

Not written: `corpus/knowledge/harness-job-capacity-r25.md`, `corpus/SOURCES.md`, `tools/**`,
`corpus/lessons/**`, `.ufo/waves/round-25/evidence/**`, `LOG.md`, `PROVINCE.md`, `SCORECARD.md`.

## 4. Out of scope (deliberately not done)

* The knowledge entry itself — the L1 lands it (this report carries the full draft, §7).
* `corpus/SOURCES.md` rows: S098–S102 proposed by `MoriR25.UpstreamTagLocate`; S103 (upstream prose
  row `docs/tools/eval.md:258`) and S118/S119 (the two `atCapacity` consumer rows,
  `tools/bash.ts` and `tools/eval.ts`) proposed by `MoriR25.SrcRejections`. All three of the latter
  were re-opened byte-for-byte here before being cited (HTTP 200; sha256
  `fb2fc4a139ba187f1cc062fab53bd72a48dd13b1f81f0c3318ec7a79d41e495c`,
  `d985ef25639993e05fb4de8c8b6dc75dde76422f63d1a295b95eb575e8cc3ea2`,
  `01e9c5c56af15d3e04cdeaf99d959afa90129f8cbb015d6908e02795351920e3`). The L1 admits them. This
  draft cites them as placeholders and does not create them.
* The C2 tool `tools/mori-job-runway.py`: built by `MoriR25.BuildJobRunwayTool` in a sandbox clone
  (`9cb0dc3c4f04e9e35ccfb00912fcd70f0fd806fa`); this seat did not write, run or review it and
  makes no claim about its code. The draft quotes only the contract's own vocabulary.
* The live evidence file for the tool's live run (another seat's).
* Any change to `scripts/hyaku/wave-slot.sh` (fleet root, read-only here) — the draft *describes*
  the gate's numbers, it does not propose changing them.
* the operator's OMP settings file, `~/.omp/agent/mcp.json`, OMP settings — read only, never edited.
* Running `omp` as a harness (no session was started; only `omp --version` was asked for the
  version string).

## 5. Findings for the canonical judge

1. **The contract's "exact error text" is a template, and the number in it is the effective cap,
   not the configured value.** On this host the config says 200 and every refusal says 100. A
   lane that reads "Background job limit reached (100)" as "the cap is 100 because someone set it
   to 100" is wrong: 100 is the clamp (F2), and 200 is unreachable (F3).
2. **The count rule excludes queued jobs, and the task path queues by default.** A task job is
   registered with `queued: true` and only becomes countable when `markRunning()` fires after it
   acquires its permit. So "100 jobs registered" ≠ "100 jobs running", and a parked batch does not
   by itself consume the runway — the upstream comment says exactly that ("Queued jobs hold no
   execution slot yet — only count jobs that are actually running so a large parked batch cannot
   starve registration", `job-manager.ts:363-364`).
3. **The cap is per root session tree, not per seat.** Children borrow the parent's manager
   (`sdk.ts:2315,4789-4791`); only a session with no `parentTaskPrefix` builds one. A lane observer
   must therefore not attribute "100 running jobs" to one wave: the count is session-global.
4. **A refusal spawns nothing.** `register()` throws before the job object exists
   (`job-manager.ts:365-374` precede `:378-396`); the tool then discards that spawn's run
   (`task/index.ts:1213`) and reports `results: []`. A refused seat produced no work and no
   runway consumption. **[INFERENCE]** the pre-registered speculative launch (`task/speculative-launch.ts`)
   may already have been started when the refusal happens; the same catch path aborts it, so
   "spawns nothing" is a statement about the registration refusal, not a proof that no process was
   ever pre-started.
5. **The hyaku gate and the harness measure different things under different numbers.** The gate
   defaults to a target of 200 *agents* (live estimate + 120 s of reservations + the request);
   the harness caps at 100 *running, non-queued jobs*. A gate grant is not a harness reservation,
   and the gate cannot see the harness's count. The gate's own header records the resulting
   failure mode ("~160 jobs at once overall" while "Main's own spawns were refused").
6. **Unavailable is not zero.** The contract's states distinguish `absent` (no `async:` block /
   no `maxJobs` child / no file) from `unreadable` (path exists, cannot be read) and `malformed`;
   when the clamp cannot be derived, `effective` is null and the verdict is `RUNWAY_UNKNOWN`
   (exit 2). An absent clamp is never "no clamp" and never "unlimited". The draft's decision table
   makes that an explicit "does NOT prove" column, in the model entry's own style.
7. **`absent` conflates three cases** (no file / no `async:` block / no `maxJobs` child) and all
   three fall back to the schema default 100. A lane observer therefore cannot distinguish "the
   operator never configured a cap" from "the operator configured it in a file the tool was not
   pointed at".
8. **The upstream default 15 is dead in shipped wiring. [INFERENCE]** The construction site always
   passes the function form, so `value` is never `undefined` in a shipped session and the manager's
   `DEFAULT_MAX_RUNNING_JOBS = 15` never applies. The installed binary agrees (the constant is
   minified to `var v = 15;`, and the getter consumes it only through `t ?? v`).
9. **Version-bound.** Everything above is omp/oh-my-pi **18.12.6** (tag `v18.12.6`, commit
   `45c35e40c46166dc726ccc52f5d27f40f2449f99`). No upstream commit or PR rationale for the 100
   clamp was traced, so "why 100" is [UNKNOWN], not "the vendor chose 100".
10. **Discrepancy carried forward from `UpstreamTagLocate`:** the contract says "the session/sdk
    file that constructs the manager"; at `45c35e40` there is no `packages/coding-agent/src/session/sdk*`
    path — the constructor call is in the top-level `packages/coding-agent/src/sdk.ts:2282-2286`.
    The draft cites the real path.
11. **The upstream settings page states no maximum; the upstream prose states it as 100.**
    `docs/settings.md:623` gives type, default 100 and the floor of 1 — and nothing about a
    ceiling. `docs/tools/eval.md:258` says the cap is "default and maximum 100". A reader of the
    settings page alone would predict that a configured 200 runs 200 jobs; at this tag it runs 100
    (F2, F3). The draft states the ceiling from the prose and from the code, and carries the
    contrast as an explicit "does NOT prove" row rather than leaving a reader to infer it.
12. **Reading guard: 15 is not the shipped cap.** `DEFAULT_MAX_RUNNING_JOBS = 15`
    (`job-manager.ts:43`) is the fallback for a caller that passes no `maxRunningJobs` option; the
    shipped construction always passes the function form, so the fallback is unreachable in a
    shipped session [INFERENCE] (F3). A cap of "15 or 100" quoted from upstream discussion is
    therefore a category error. This seat did not open any upstream issue or pull request, so no
    rationale is claimed here; the ceiling is a shipped fact, its history is not.
13. **The tool's live run exits 1 by design** (`RUNWAY_CLAMPED`). A gate that reads a non-zero exit
    as "the tool failed" will misgrade a correct measurement.
14. **Reaching the cap is not always an error — scope every "the harness refuses at the cap"
    statement to the registration paths.** `AsyncJobManager` publishes `atCapacity`, and exactly two
    production consumers consult it: the bash auto-background branch (`tools/bash.ts:1228`) and the
    eval auto-background branch (`tools/eval.ts:536`). Both fall through to direct foreground
    execution at the cap ("At the running-job cap, fall through to direct foreground execution
    instead of failing every bash/eval call until a slot frees up"), so those calls run and raise
    nothing. The explicit `async: true` bash branch (`tools/bash.ts:1187-1208`) and the task spawn
    path do not pre-check, so they throw the refusal text. Consequence for a lane observer: the
    absence of a refusal is **not** evidence that the runway was free, and the fleet's visible
    refusals are a lower bound on the cap's pressure, not a measure of it. The draft states this as
    F9, a decision-table row, a Limits bullet and U9, and cites S118/S119 as placeholders (rows
    proposed by `MoriR25.SrcRejections`; re-opened byte-for-byte here before use).

## 6. Artifact paths

| Artifact | Path | Note |
|---|---|---|
| This report | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-25/w1/KnowledgeDraftC2.md` | the only lane write |
| Draft target (NOT written) | `corpus/knowledge/harness-job-capacity-r25.md` | L1 lands it from §7 |
| Upstream snapshot (scratch, outside the lane) | `/tmp/ohmp/oh-my-pi-18.12.6/` | tarball of tag `v18.12.6`; upstream fetch, no lane bytes |
| Upstream job-manager raw | `/tmp/jm.ts` | same bytes as the tarball copy |
| Tool (other seat, sandbox) | `/fast/scratch/hyaku/mori-r25/wt-runway/tools/mori-job-runway.py` | commit `9cb0dc3c…`; not this seat's work |

## 7. The full draft — `corpus/knowledge/harness-job-capacity-r25.md`

Paste-ready. `S###` ids are placeholders for the rows proposed by `MoriR25.UpstreamTagLocate`
(S098–S102) and by `MoriR25.SrcRejections` (S103, S118, S119 — all re-opened here); the L1 admits
them or renumbers, and the `source:` line is edited to match.

```markdown
source: S098 (oh-my-pi packages/coding-agent/src/async/job-manager.ts at tag v18.12.6 = commit 45c35e40c46166dc726ccc52f5d27f40f2449f99), S099 (oh-my-pi packages/coding-agent/src/sdk.ts at the same commit), S100 (oh-my-pi packages/coding-agent/src/tools/settings.ts at the same commit), S101 (oh-my-pi docs/settings.md at the same commit), S102 (installed binary ~/.local/bin/omp, own-work: 256,702,432 bytes, sha256 85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4, byte-identical to release asset omp-linux-x64 of tag v18.12.6), S103 (oh-my-pi docs/tools/eval.md at the same commit: the session-wide cap documented as "default and maximum 100", shared with every background job in the session), S118 (oh-my-pi packages/coding-agent/src/tools/bash.ts at the same commit: the bash auto-background branch's `atCapacity` pre-check and its fall-through to direct foreground execution), S119 (oh-my-pi packages/coding-agent/src/tools/eval.ts at the same commit: the eval auto-background branch's `atCapacity` pre-check and its fall-through to direct foreground execution). S-ids S098–S103 and S118–S119 are cited as placeholders pending the L1's admission. Supporting reads without registry rows, opened by wave-1 seat KnowledgeDraftC2 (round 25) at the same commit: packages/coding-agent/src/task/index.ts, packages/coding-agent/src/task/speculative-launch.ts, packages/coding-agent/src/task/spawn-run.ts, packages/coding-agent/src/config/settings.ts; and the fleet script scripts/hyaku/wave-slot.sh (read-only, sha256 41b487ef51012c099ab704e8c226f3bb701e11c120f7c6973ab73cb1f3737a81).
verified-at: 2026-10-22 — upstream sources opened as raw bytes at tag v18.12.6 (sha256 job-manager.ts 0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7, sdk.ts c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957, tools/settings.ts 514974143d47db0c9765bc47e86dcb9a38bd6bc23113a4ffe557bff0d8e30507, docs/settings.md 0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883, docs/tools/eval.md fb2fc4a139ba187f1cc062fab53bd72a48dd13b1f81f0c3318ec7a79d41e495c, tools/bash.ts d985ef25639993e05fb4de8c8b6dc75dde76422f63d1a295b95eb575e8cc3ea2, tools/eval.ts 01e9c5c56af15d3e04cdeaf99d959afa90129f8cbb015d6908e02795351920e3); the installed binary read as bytes only (never executed as a harness). Host observation, read-only: the operator's OMP settings file carries `async:` then `maxJobs: 200`; the live read-only run of the round-25 tool reports configured 200, clamp 100, effective 100, verdict RUNWAY_CLAMPED (exit 1) — `.ufo/waves/round-25/w1/BuildJobRunwayTool.md` §2.
recheck: `python3 -I -B tools/mori-job-runway.py --selftest` (frozen cases) and one live run of `python3 -I -B tools/mori-job-runway.py`; on an omp release, re-open S098–S103 and S118–S119 and re-read the installed binary's clamp site and setting default.
author: MoriR25 (L1) from the wave-1 scribe draft `.ufo/waves/round-25/w1/KnowledgeDraftC2.md`.

# Harness background-job runway — the effective cap, the count that reaches it, and what a refusal proves

## Scope

This note records what the omp harness's background-job runway is: the cap a session enforces,
the rule that counts against it, the exact text a refusal carries, and what that cap does and
does not decide for the hyaku seat gate and for a lane observer. It covers the
`AsyncJobManager` of oh-my-pi 18.12.6 as shipped in the installed binary `~/.local/bin/omp`, and
the `async.maxJobs` setting it is derived from.

It is a **reading** note. It describes one cap, computed from bytes on disk. It does not run a
harness session, does not start, list, count or cancel a job, does not edit the operator's OMP settings file
or any other settings file, does not change the hyaku gate, and does not measure how many jobs
are running now. The tool's vocabulary (`configured`, `clamp`, `setting_default`, `effective`;
`set`, `absent`, `malformed`, `unreadable`, `found`, `ambiguous`), its verdicts
(`RUNWAY_AS_CONFIGURED | RUNWAY_CLAMPED | RUNWAY_DEFAULT | RUNWAY_UNKNOWN`) and its exit codes are
the tool's own contract (contract `.ufo/waves/round-25/contract.md` C2), not upstream vocabulary.

Everything here is bound to one version, omp/oh-my-pi **18.12.6** (tag `v18.12.6`, commit
`45c35e40c46166dc726ccc52f5d27f40f2449f99`). A different build may clamp elsewhere, and this note
does not carry over.

## Facts

Every fact below carries its pointer. Upstream URLs are at commit
`45c35e40c46166dc726ccc52f5d27f40f2449f99` of `https://github.com/can1357/oh-my-pi`.

**F1 — the setting, its default, and the documented ceiling.** `async.maxJobs` is a declared number
setting with `default: 100`:
`export const cfgAsyncMaxJobs = register({ id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100 });`
([tools/settings.ts:941-946](https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/tools/settings.ts)).
The upstream settings page documents the same entry as
"Running background-job cap, floored to at least 1; parked/queued jobs do not consume execution slots"
with type `number` and default `100` (S101, [docs/settings.md:623](https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md)).
The installed binary carries the same definition in its settings table (S102): `id: "async.maxJobs",
protocolDefault: ["rpc"], type: "number", default: 100` at byte 155231590.

The settings page states a default and a floor but **no maximum**. The ceiling is stated elsewhere in
the upstream prose: "every handle is a running background job counted against the session-wide
`async.maxJobs` cap (default and maximum 100)" and "`agent()` fails with `Background job limit
reached` once that cap is full" (S103, [docs/tools/eval.md:258](https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/tools/eval.md),
sha256 `fb2fc4a139ba187f1cc062fab53bd72a48dd13b1f81f0c3318ec7a79d41e495c`, 28,027 bytes). The same
line names the shared population: the cap is shared "with every other background job in the session,
including async `bash`, async `task` spawns, `workpool()` pools and nested subagents' jobs". So a
reader of the settings page alone would predict that a configured 200 runs 200 jobs; at this tag that
is false (F2, F3), and the prose is the form that states the ceiling.

**F2 — the clamp lives at the construction site, not in the manager.** The one shipped construction of
the job manager is:
`const asyncJobManager = !options.parentTaskPrefix ? new AsyncJobManager({ maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)) }) : undefined;`
(S099, [sdk.ts:2282-2286](https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/sdk.ts)).
The installed binary carries it once, at byte 164406766: `maxRunningJobs: () => Math.min(100, XPe.get(R))`
(S102). So the value the operator configures is clamped at 100 **before** the manager sees it, and no
shipped session can run more than 100 concurrent background jobs whatever the configuration says.

**F3 — the effective cap.** The manager resolves its cap at check time:
`get #maxRunningJobs(): number { const option = this.#maxRunningJobsOption; const value = typeof option === "function" ? option() : option; return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS)); }`
(S098, [job-manager.ts:330-335](https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/async/job-manager.ts)),
with `const DEFAULT_MAX_RUNNING_JOBS = 15;` at `job-manager.ts:43`. Composed with F2, the effective
cap of a shipped session is

    effective = max(1, floor(min(100, base)))

where `base` is the configured `async.maxJobs` value, or the schema default 100 when the setting is
not configured. The manager's own 15 is a fallback for a caller that passes no option at all; the
shipped construction always passes the function form, so `value` is never undefined there.
[INFERENCE] The 15 is therefore unreachable in a shipped 18.12.6 session: with the setting absent
the schema default 100 flows through, and with it set the value is clamped at 100. The installed
binary agrees — the constant is minified to `var v = 15;` and is consumed only through `t ?? v`
(S102).

**F4 — the count rule: running and not queued, every type.** Both the capacity probe and the
registration check count the same population:
`for (const job of this.#jobs.values()) { if (job.status === "running" && !job.queued) activeCount++; }`
(S098, [job-manager.ts:337-345](https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/async/job-manager.ts)
and `job-manager.ts:363-370`). A job counts when its status is `running` **and** its `queued` flag is
clear. The loop iterates over every job the manager holds and applies **no type filter**: the type
union is `export type AsyncJobType = "bash" | "task" | "eval";` (`job-manager.ts:48`). A background
shell job and a subagent task draw on the same runway, and the upstream comment states the intent:
"Queued jobs hold no execution slot yet — only count jobs that are actually running so a large
parked batch cannot starve registration" (`job-manager.ts:363-364`). The upstream prose says the same
rule in words: every background job in the session shares one cap, "including async `bash`, async
`task` spawns, `workpool()` pools and nested subagents' jobs" (S103, `docs/tools/eval.md:258`).

**F5 — queued is the normal state of a task job at registration.** The task tool registers each
spawn with `queued: true` (`task/index.ts:1565`) and calls `markRunning()` only after the spawn
acquires its permit and actually begins executing (`task/index.ts:1490`); `markRunning` clears the
flag (`job-manager.ts:355-357` upstream, "Clear the queued flag once the job actually starts
executing"). A bash job registers without the flag (`tools/bash.ts:882`) and therefore counts from
registration. So a batch of task jobs that is admitted but not yet running does not consume the
runway, and "registered" is not "running".

**F6 — the exact refusal text, and what the number in it is.** When the count has reached the cap and
a caller goes through the registration path, `register()` throws:
`Background job limit reached (${maxRunningJobs}). Wait for running jobs to finish or cancel one.`
(S098, [job-manager.ts:371-373](https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/async/job-manager.ts));
the string occurs once in the source and the installed binary carries the same template (S102,
byte 160033359). The interpolated number is the **effective** cap at that instant (F3), never the
configured value. The cap is re-read on every check — the option may be a function and "a function
is re-read on every capacity check so a live setting resizes the cap" (`job-manager.ts:170-171`) —
so the number in a refusal is a snapshot, and the same session may refuse with a different number
later. The throw is reached only where a caller registers without pre-checking the cap; two
production paths pre-check it and degrade instead of throwing (F9).

**F7 — only a top-level session constructs the manager.** The guard is `!options.parentTaskPrefix`
(`sdk.ts:2282`, F2). A child session does not build its own; it uses the manager handed to it:
`const scopedAsyncJobManager = asyncJobManager ?? options.asyncJobManager;` (`sdk.ts:2315`), and the
session options carry the comment "Children borrow their parent's manager but never dispose it."
(`sdk.ts:4789-4791`). The upstream comment at the construction site adds that "Every root owns its
jobs and delivery sinks, even when another root is live" (`sdk.ts:2279-2281`). The cap is therefore
**one number per root session tree**, shared by every subagent under that root, and it is not
re-derived per seat. A session that has no manager at all falls back to synchronous execution with
the warning "task: no AsyncJobManager registered; falling back to sync execution"
(`task/index.ts:1046`).

**F8 — a refusal creates nothing.** The throw in `register()` happens before the job record, before
the `AbortController` and before the run callback is ever invoked (`job-manager.ts:365-374` precede
the job object at `job-manager.ts:378-396`). The task tool catches it per spawn, discards that
spawn's run — `spawn.run?.discard(\`background job registration failed: ${message}\`)`
(`task/index.ts:1213`), and `discard` "Abort[s] an unadopted run and drop[s] anything it retained;
nothing ever consumes its result" (`task/spawn-run.ts:126-134`) — then reports
`Failed to start background task job{s}: <agentId>: <message>` with `details.results: []`
(`task/index.ts:1220-1230`). A refused seat therefore adds nothing to the runway, produces no
output, and is a scheduling failure, not a result. [INFERENCE] The task path can pre-start a
speculative launch before the job is registered (`task/speculative-launch.ts:200-260`); the same
catch path discards it, so "spawns nothing" is a statement about the refusal itself, not a proof
that no process was ever pre-started.

**F9 — reaching the cap is not always an error: two production paths pre-check it and degrade to
foreground.** The manager publishes `get atCapacity(): boolean` (S098, `job-manager.ts:337-346`), and
exactly three places in the shipped source consult it: the getter itself and two consumers. The bash
tool's auto-background branch tests `!autoBgManager.atCapacity` and, at the cap, falls through to
direct foreground execution — "At the running-job cap, fall through to direct foreground execution
instead of failing every bash call until a slot frees up" (S118, `tools/bash.ts:1224-1229`, sha256
`d985ef25639993e05fb4de8c8b6dc75dde76422f63d1a295b95eb575e8cc3ea2`). The eval tool does the same —
"At the running-job cap, fall through to direct foreground execution instead of failing every eval
call until a slot frees up" (S119, `tools/eval.ts:535-538`, sha256
`01e9c5c56af15d3e04cdeaf99d959afa90129f8cbb015d6908e02795351920e3`). An **explicit** `async: true`
bash call does not pre-check: it goes straight to `#startManagedBashJob` (`tools/bash.ts:1187-1208`)
and therefore to `manager.register` (`tools/bash.ts:882`), where it throws (F6). The task tool's
spawn path does not pre-check either, so a wave of task spawns at the cap is refused with the error
(F6, F10). The refusal text is therefore the signature of the **registration** paths only: at the
cap, an auto-backgrounded bash or eval call degrades to a foreground run and raises nothing.

**F10 — the refusal as the fleet records it.** The lane's own round-20 ground-truth notes carry this
exact text, and their numbers are the effective cap: "Failed to start background task jobs:
KasegiR23.FixMirror: Background job limit reached (100)" with all 64 names refused
(`.ufo/waves/round-20/build/GtLaneKasegi.md:48`), and "seats 66, refused 66, spawned 0,
'Background job limit reached (100)'" (`.ufo/waves/round-20/build/GtLaneKama.md:72`). These are
lane-written records, not upstream sources, and they are cited as observations of the message, not
as proof of what filled the runway. [INFERENCE] The number of refused seats in one wave (64, 66, 68,
88 in those records) exceeds 100 in some waves because each seat is a separate registration attempt
and every attempt fails once the count has reached the cap; the cap is a session-wide count, not a
per-wave budget.

**F11 — the hyaku seat gate measures a different population under a different number.**
`scripts/hyaku/wave-slot.sh` (read-only) resolves a target `CAP` from `HYAKU_WAVE_CAP` (environment),
else from `$STATE/wave-cap` (state), else the default `200` (`configured_cap()`, lines 28-49), and
grants a wave only while `live + pending + seats` fits under it (`fits_cap()`, lines 50-58;
`acquire`, lines 68-96), also requiring `MemAvailable ≥ 6144 MB`. `live` is an estimate of live
agents computed by `scripts/hyaku/wave-live.py` from the live session directory's tail metadata;
`pending` sums ledger rows from the last 120 s. The gate's unit is **agents**, its number is
**200** by default, and its input is an agent estimate. The harness's unit is **running non-queued
jobs**, its number is **100** by clamp (F2, F3), and its input is the manager's own job map (F4).
The script's own header records the resulting mismatch: "Observed 2026-10-21: L1 sessions kept
dispatching full waves (~160 jobs at once overall) while Main's own spawns were refused with
'Background job limit reached (100)'". [INFERENCE] A wave the gate grants is not a reservation in
the harness: the gate cannot see the harness's count, the harness cannot see the gate's, and
neither number is derived from the other. A grant therefore does not imply that the wave can spawn.

**F12 — this host.** the operator's OMP settings file carries a column-0 `async:` block whose direct child
is `maxJobs: 200` (read 2026-10-22). The installed binary's clamp is 100 (F2) and its setting
default is 100 (F1), so the effective cap on this host is 100, and the round-25 tool's live run
reports configured 200, clamp 100, effective 100, verdict `RUNWAY_CLAMPED`, exit 1
(`.ufo/waves/round-25/w1/BuildJobRunwayTool.md` §2). This is one host on one day, not a fleet fact.

**F13 — the tool reads one file, the runtime reads a stack.** The settings layer keeps a global
layer (`config.yml`/`config.yaml` under the agent directory, here `~/.omp/agent/`), a project layer
(`.claude/settings.yml`, `.omp/config.yml`, …) and further overlays and runtime overrides
(`config/settings.ts:587-595,1561-1620`). The C2 tool reads exactly one file — the global one —
and therefore reports that file's `async.maxJobs` value, not necessarily the value a session
resolved. On this host no project-layer `config.yml` exists (the fleet root's `.omp/` holds only
`agents/`; the lane repo has no `.omp/`), but an overlay or a runtime override remains possible
and unread by the tool. [INFERENCE] `configured` is the file's value; `effective` is the cap that
*would* apply if that file's value were the effective one.

## Decision table

Observable → what the C2 tool reports → what that state does **not** prove. The states, verdicts
and exit codes are the contract's vocabulary (contract C2); the "not proved" column is what the
sources above forbid.

| Observable | Tool state (C2) | Verdict / exit | What it does NOT prove |
|---|---|---|---|
| `async.maxJobs` present and set, e.g. 200 on this host (F12); binary carries the clamp (F2) | `configured {set, 200}`, `clamp {found, 100, sites 1}`, `effective 100` | `RUNWAY_CLAMPED`, exit 1 | That the session was at capacity: the tool reads no job count, and the live count is not readable from outside the session. That the configuration is wrong or ignored — 200 is read, then clamped. That the configured number is the number a refusal would show (F6). That a different layer did not override the file (F13). |
| `async.maxJobs` set to a value ≤ 100 (e.g. 50) | `configured {set, 50}`, `effective 50` | `RUNWAY_AS_CONFIGURED`, exit 0 | That any job ran, that the runway was free, or that 50 is a safe or tested number. That the value survives the settings stack (F13). |
| The settings page alone (`docs/settings.md:623`: type number, default 100, floored to at least 1, no maximum stated — F1) | (not a tool state — a documentation reading) | — | That a configured value above 100 takes effect: the page states no ceiling, the code clamps at 100 (F2, F3), and the upstream prose names the ceiling "default and maximum 100" (F1). That the manager's `DEFAULT_MAX_RUNNING_JOBS = 15` is the shipped cap: 15 is the fallback for a caller that passes no option (F3). |
| No `async:` block, no `maxJobs` child, or no config file at all (F1, F3) | `configured {absent, null}`, `setting_default {found, 100}`, `effective 100` | `RUNWAY_DEFAULT`, exit 0 | That the operator never configured a cap — `absent` also covers "the file the tool was pointed at is not the file the session reads" (F13). That a clamp is absent: the clamp is in the binary's bytes, not in the config (F2). That 100 running jobs is a small number. |
| `maxJobs` quoted, duplicated as a direct child, or `async:` carrying an inline value | `configured {malformed, null}` | effective null → `RUNWAY_UNKNOWN`, exit 2 | That the cap is zero, unlimited or absent. That the harness is unclamped. That the refusal text in a transcript can be re-derived; the tool knows only that it cannot derive the number. |
| The binary's bytes carry no clamp match (a different build, or a re-minified one) | `clamp {absent, null}` | effective null → `RUNWAY_UNKNOWN`, exit 2 | That there is no clamp. An absent match is a failed lookup, never "unlimited" and never "zero". |
| The binary cannot be read (missing path, a directory, unreadable file) | `clamp {unreadable, null}`, `setting_default {unreadable, null}`, `binary_sha256 null` | effective null → `RUNWAY_UNKNOWN`, exit 2 | That the cap is unknown-in-general; it is unknown-to-this-tool. Unavailable is not zero: no state here means "zero capacity" or "no limit". |
| The binary carries two clamp sites with different numbers | `clamp {ambiguous, null, sites 2}` | effective null → `RUNWAY_UNKNOWN`, exit 2 | Which site is live. That the smaller number is the effective one. |
| A refusal observed in a transcript: `Background job limit reached (100). Wait for running jobs to finish or cancel one.` (F6) | (not a tool state — an observation) | — | That the configured value was 100: the number is the effective cap (F3, F12). That the runway was full of *this* wave's work: the count is session-wide and shared by the whole root tree (F7). That the refused seats did anything: a refusal creates nothing (F8). That the cap is still 100 now: it is re-read at every check (F6). That every call at the cap would have errored: the auto-background paths degrade to foreground instead (F9). |
| An auto-backgrounded bash or eval call at the cap: it runs in the foreground, with no error (F9) | (not a tool state — an observation) | — | That the cap was not reached: the branch is entered *because* the cap was reached. That the call was backgrounded: it was deliberately not. That the fleet's silence at the cap means the runway was free — a foreground run and a refusal are different observations of the same cap. |
| A seat that was refused | (not a tool state) | — | That the seat ran, finished, or produced output: `register()` throws before the job exists and the tool returns `results: []` (F8). That the refusal consumed runway: it did not. |
| A spawn record reporting many started agents | (not a tool state) | — | That those agents were running: a task job is registered `queued: true` and counts only after `markRunning()` (F5). That they held slots at any particular moment. |
| The hyaku gate prints `granted lane=… seats=… cap=200` (F11) | (not a tool state) | — | That the wave can spawn: the gate counts agents against 200 and cannot see the harness's running-job count against 100 (F11). That the gate's live estimate is the harness's job count — they are different populations computed from different sources. That a refusal after a grant is a gate bug. |

## Limits

- **One cap, one version.** Every statement is bound to omp/oh-my-pi 18.12.6 (tag `v18.12.6`,
  commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`) and to the installed binary
  `~/.local/bin/omp` (sha256 `85d9daf3…ccfa4`). A different version or a rebuilt binary may clamp
  elsewhere; re-open S098–S103 and re-read the binary's bytes on a release.
- **A cap, not a count.** The tool reports the cap the binary would compute from the files it is
  pointed at. It does not read, and cannot read from outside the session, how many jobs are running
  now (contract C2 scope bound).
- **One config file.** The tool reads one file. The runtime settings stack also has a project
  layer, `--config` overlays and runtime overrides (F13), so `configured` is that file's value and
  `effective` is the cap that would apply if it were the effective one.
- **The binary read is a byte read.** The clamp and the setting default are located by pattern over
  the file's bytes. The pattern is the contract's; it is not a parse of the bundle, so a build that
  spells the same logic differently reads as `absent` — a failed lookup, not an absent clamp.
- **The config reader is a line grammar, not YAML.** It finds a column-0 `async:` and its direct
  children (contract C2 rule 1). Anchors, multi-line scalars and flow mappings beyond the
  contracted inline-`async:` case are not modelled.
- **The cap counts jobs, not seats, not agents, not waves.** One seat is one task job; a bash job
  counts the same; a queued task job does not (F4, F5). `wave-slot.sh`'s seats are agents it
  estimates, which is a different unit again (F11).
- **The refusal text is upstream's, but the sentence a lane reads is composed by the task tool**
  (`Failed to start background task job{s}: <agentId>: <message>`, `task/index.ts:1220-1230`). The
  fixed inner sentence is the upstream string; the wrapper is the tool's.
- **The cap is a registration limit, not a global refusal switch.** Only callers that register
  without pre-checking it raise the error (F9). The bash and eval auto-background branches check
  `atCapacity` and fall back to direct foreground execution, so at the cap those calls still run —
  silently, in the foreground. The task spawn path and an explicit `async: true` bash call do not
  pre-check and do raise it. The number of `atCapacity` consumers in the shipped source is two
  (`tools/bash.ts:1228`, `tools/eval.ts:536`); the getter is the third hit and is not a consumer.
- **Transcripts are private.** Session transcripts under `~/.omp` may hold private text. Only
  counts, timestamps and the fixed error text may be reported from them; no message content.
- **Detection and report only.** No omp run, no settings write, no gate change, no job started,
  listed or cancelled (round-25 bounds).
- **The verdict vocabulary and exit codes are the tool's own** (contract C2). The upstream vocabulary
  is `Background job limit reached (N).` and `Async job manager is disposed`; upstream never emits
  `RUNWAY_CLAMPED`. A live run that exits 1 on this host is a correct measurement, not a tool
  failure.
- **The gate is described, not judged.** This note states what `wave-slot.sh` computes and that the
  two numbers differ. It proposes no change to the gate, no change to `async.maxJobs`, and no
  reconciliation of the two populations.

## [UNKNOWN]

- **U1 — why the clamp is 100.** The upstream prose states the ceiling as a fact ("default and
  maximum 100", F1) but gives no reason for it, and no upstream commit, PR or issue explaining the
  `Math.min(100, …)` at the construction site was traced by this seat. The number is a shipped fact
  (F2); its rationale is not in the sources opened.
- **U2 — what filled the runway.** The count that reached the cap is session-global (F7) and is not
  recorded in a refusal. A refusal therefore cannot attribute the capacity to the wave that hit
  it, to an earlier wave, or to background shell jobs.
- **U3 — the live count.** The number of running, non-queued jobs in any session is not readable
  from outside that session. The tool reports a cap, never a load.
- **U4 — the effective settings value.** Whether a project layer, a `--config` overlay or a runtime
  override sets `async.maxJobs` in a given session was not established; only the global file was
  read (F13). The tool cannot answer it either.
- **U5 — the queueing behaviour under load.** A task job registers queued and counts only once it
  starts (F5). How many registrations of a large wave succeed before the count reaches the cap was
  not measured; the upstream comment only states the intent (F4).
- **U6 — other versions.** The clamp, the default and the count rule were read at 18.12.6 only.
  Whether earlier or later releases clamp at 100 was not checked.
- **U7 — the gate's relation to the harness.** No upstream or fleet document ties
  `wave-slot.sh`'s target to `async.maxJobs`. The script's header comment is an operator's
  observation, not a specification. Whether the two numbers are meant to agree is not established.
- **U8 — the manager's fallback of 15.** [INFERENCE] The `DEFAULT_MAX_RUNNING_JOBS = 15` path is
  unreachable in a shipped 18.12.6 session (F3). It was not exercised on this host, and no
  upstream statement says it is intended to be dead.
- **U9 — how much work degraded instead of erroring.** At the cap, auto-backgrounded bash and eval
  calls run in the foreground with no error (F9), while task spawns are refused. How many calls in a
  given session took the degraded path, and how long they blocked the caller, was not measured;
  the tool reads no job count at all (U3). A fleet's observable refusals are therefore a lower
  bound on the cap's pressure, not a measure of it.

## Not claimed

- No claim that a refusal means the fleet overloaded the harness; it means that session's count of
  running, non-queued jobs had reached its cap.
- No claim that `async.maxJobs` above 100 has any effect (F2, F3).
- No claim that the configured value on this host, 200, is an error, or that any settings file
  should be changed.
- No claim about how many jobs are running on this host or on any host.
- No claim that changing the hyaku gate's target would prevent refusals, or that the gate is
  defective; only that the two numbers and the two populations differ (F11).
- No claim that a seat, an agent, a task and a job are the same unit.
- No claim that a call which ran in the foreground proves the cap was not reached (F9).
- No claim that every refused or degraded call in a session is visible in any one record.
- No claim that a refused seat's work was completed, lost or harm-free; it was not run (F8).
- No claim about any omp version other than 18.12.6.
```

## 8. Tooling

**No tool was installed, upgraded or removed by this seat.** No `pacman`, `uv tool`, `cargo` or
`npm` transaction was run (host-wide pacman transactions are paused for this round, and none was
needed). Commands used, all pre-existing: `python3` (standard library only; byte searches and
regex over the binary), `curl` (upstream raw bytes and the release tarball), `git ls-remote`
(read-only, no clone of the lane), `grep`/`sed`/`sha256sum`/`ls`/`file` (coreutils) for the
read-only host checks. `omp --version` was asked for the version string; no harness session was
started.
