source: S098 (oh-my-pi packages/coding-agent/src/async/job-manager.ts at tag v18.12.6 = commit 45c35e40c46166dc726ccc52f5d27f40f2449f99), S099 (oh-my-pi packages/coding-agent/src/sdk.ts at the same commit), S100 (oh-my-pi packages/coding-agent/src/tools/settings.ts at the same commit), S147 (oh-my-pi docs/settings.md at the same commit; supersedes the round-25 row, round 28), S102 (installed binary ~/.local/bin/omp, own-work: 256,702,432 bytes, sha256 85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4, byte-identical to release asset omp-linux-x64 of tag v18.12.6), S103 (oh-my-pi docs/tools/eval.md at the same commit: the session-wide cap documented as "default and maximum 100", shared with every background job in the session), S112 (oh-my-pi packages/coding-agent/src/tools/bash.ts at the same commit: the bash auto-background branch's `atCapacity` pre-check and its fall-through to direct foreground execution), S113 (oh-my-pi packages/coding-agent/src/tools/eval.ts at the same commit: the eval auto-background branch's `atCapacity` pre-check and its fall-through to direct foreground execution). S104 (oh-my-pi commit 476b858b3a4abe6f6c8a06c252c23961be41e912, 2026-02-22, "added async background job execution with configurable concurrency limits": the 100 ceiling shipped with the feature). Rows S098–S100, S102–S104 and S112–S113 were opened and admitted in round 25 (the round-25 settings.md row is superseded by S147); S105–S111 are this round's rejected candidates. Supporting reads without registry rows, opened by wave-1 seat KnowledgeDraftC2 (round 25) at the same commit: packages/coding-agent/src/task/index.ts, packages/coding-agent/src/task/speculative-launch.ts, packages/coding-agent/src/task/spawn-run.ts, packages/coding-agent/src/config/settings.ts; and the fleet script scripts/hyaku/wave-slot.sh (read-only, sha256 41b487ef51012c099ab704e8c226f3bb701e11c120f7c6973ab73cb1f3737a81).; S138, S139, S152, S141 (oh-my-pi commits 944d7f8d, e398f831, 6962d5cd, c4a2441d — the clamp history after the feature commit; added round 27, routed R7; S152 supersedes the round-27 row for 6962d5cd, round 28)
verified-at: 2026-10-22 — upstream sources opened as raw bytes at tag v18.12.6 (sha256 job-manager.ts 0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7, sdk.ts c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957, tools/settings.ts 514974143d47db0c9765bc47e86dcb9a38bd6bc23113a4ffe557bff0d8e30507, docs/settings.md 0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883, docs/tools/eval.md fb2fc4a139ba187f1cc062fab53bd72a48dd13b1f81f0c3318ec7a79d41e495c, tools/bash.ts d985ef25639993e05fb4de8c8b6dc75dde76422f63d1a295b95eb575e8cc3ea2, tools/eval.ts 01e9c5c56af15d3e04cdeaf99d959afa90129f8cbb015d6908e02795351920e3); the installed binary read as bytes only (never executed as a harness). Host observation, read-only: the operator's OMP settings file carries `async:` then `maxJobs:` with a value above the clamp (value withheld, round 27); the live read-only run of the round-25 tool reports a configured value above the clamp, clamp 100, effective 100, verdict RUNWAY_CLAMPED (exit 1) — `.ufo/waves/round-25/w1/BuildJobRunwayTool.md` §2.
recheck: `python3 -I -B tools/mori-job-runway.py --selftest` (frozen cases) and one live run of `python3 -I -B tools/mori-job-runway.py`; on an omp release, re-open S098–S103, S112–S113 and S138–S141 and re-read the installed binary's clamp site and setting default.
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

**Whose ground (wave-2 CriticC2Admission).** Mori's own ground here is the reading: what the settings
file says, what the installed binary clamps it to, what the documentation does and does not state, and
what the fleet's own records show (F1–F3, F10, F12–F13). The facts about how the job manager counts,
refuses and is shared (F4–F9) are the OMP harness contract, which `PROVINCE.md` Adjacent assigns to
kumitate, and F11 describes the fleet's seat gate, which is orchestration; this note cites them only to
explain what a refusal means for an observer, and the round-25 report routes them to kumitate. Changing
the cap is the operator's.

## Facts

Every fact below carries its pointer. Upstream URLs are at commit
`45c35e40c46166dc726ccc52f5d27f40f2449f99` of `https://github.com/can1357/oh-my-pi`.

**F1 — the setting, its default, and the documented ceiling.** `async.maxJobs` is a declared number
setting with `default: 100`:
`export const cfgAsyncMaxJobs = register({ id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100 });`
([tools/settings.ts:941-946](https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/tools/settings.ts)).
The upstream settings page documents the same entry as
"Running background-job cap, floored to at least 1; parked/queued jobs do not consume execution slots"
with type `number` and default `100` (S147, [docs/settings.md:623](https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md)).
The installed binary carries the same definition in its settings table (S102): `id: "async.maxJobs",
protocolDefault: ["rpc"], type: "number", default: 100` at byte 155231590.

The settings page states a default and a floor but **no maximum**. The ceiling is stated elsewhere in
the upstream prose: "every handle is a running background job counted against the session-wide
`async.maxJobs` cap (default and maximum 100)" and "`agent()` fails with `Background job limit
reached` once that cap is full" (S103, [docs/tools/eval.md:258](https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/tools/eval.md),
sha256 `fb2fc4a139ba187f1cc062fab53bd72a48dd13b1f81f0c3318ec7a79d41e495c`, 28,027 bytes). The same
line names the shared population: the cap is shared "with every other background job in the session,
including async `bash`, async `task` spawns, `workpool()` pools and nested subagents' jobs". So a
reader of the settings page alone would predict that a configured value above 100 runs that many jobs; at this tag that
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
instead of failing every bash call until a slot frees up" (S112, `tools/bash.ts:1224-1229`, sha256
`d985ef25639993e05fb4de8c8b6dc75dde76422f63d1a295b95eb575e8cc3ea2`). The eval tool does the same —
"At the running-job cap, fall through to direct foreground execution instead of failing every eval
call until a slot frees up" (S113, `tools/eval.ts:535-538`, sha256
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
as proof of what filled the runway. [INFERENCE] Each refused seat is a separate registration attempt and every
attempt fails once the count has reached the cap, so one wave's refusals accumulate across attempts: the four
consecutive refused attempts of 64 names each (`.ufo/waves/round-20/build/GtLaneKasegi.md:48-49`) are 256 refused
registrations against a cap of 100. No single-wave refusal count in the round-20/build records exceeds 100 — the
counts recorded there are 64 (`GtLaneKasegi.md:48-49`; also `GtLaneKaidoku.md:84`, `GtLaneTsukuroi.md:72`,
`GtMoriR17W2.md:122`), 66 (`GtLaneKama.md:72`), 68 (`GtLaneChousa.md:61`; also `GtLaneKaidoku.md:86`),
70 (`GtMoriR17W1.md:109`), 71 (`GtLaneKaidoku.md:83`), 72 (`GtLaneKama.md:73`), 78 (`GtLaneKaidoku.md:80`),
86 (`GtLaneKama.md:74-75`), 88 (`GtLaneKagi.md:58`), 95 (`GtLaneKama.md:68`), and the largest, 100
(`GtLaneKaidoku.md:82`) — the cap is a session-wide count, not a per-wave budget.

**F11 — the hyaku seat gate measures a different population under a different number.**
`scripts/hyaku/wave-slot.sh` (read-only) resolves a target `CAP` from `HYAKU_WAVE_CAP` (environment),
else from `$STATE/wave-cap` (state), else the default `200` (`configured_cap()`, lines 28-49), and
grants a wave only while `live + pending + seats` fits under it (`fits_cap()`, lines 50-58;
`acquire`, lines 68-96), also requiring `MemAvailable ≥ 6144 MB`. `live` is an estimate of live
agents computed by `scripts/hyaku/wave-live.py` from the live session directory's tail metadata;
`pending` sums ledger rows from the last 120 s. The gate's unit is **agents**, its number is
**200** by default, and its input is an agent estimate. On this host the target is not the default: `~/.local/state/shokunin-hyaku/wave-cap` holds `85` (set 2026-10-22T08:30:46Z, `PHASE3.md:182`), and round 25's own grant printed `granted lane=mori wave=r25-w1 seats=34 live=50 pending=0 cap=85` (`.ufo/waves/round-25/wave1-attempts.json`). Removing that state file restores 200, twice the harness ceiling. The harness's unit is **running non-queued
jobs**, its number is **100** by clamp (F2, F3), and its input is the manager's own job map (F4).
The script's own header records the resulting mismatch: "Observed 2026-10-21: L1 sessions kept
dispatching full waves (~160 jobs at once overall) while Main's own spawns were refused with
'Background job limit reached (100)'". [INFERENCE] A wave the gate grants is not a reservation in
the harness: the gate cannot see the harness's count, the harness cannot see the gate's, and
neither number is derived from the other. A grant therefore does not imply that the wave can spawn.

**F12 — this host.** the operator's OMP settings file carries a column-0 `async:` block whose direct child
is a `maxJobs:` value above the clamp (value withheld in round 27; read 2026-10-22). The installed binary's clamp is 100 (F2) and its setting
default is 100 (F1), so the effective cap on this host is 100, and the round-25 tool's live run
reports a configured value above the clamp, clamp 100, effective 100, verdict `RUNWAY_CLAMPED`, exit 1
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
| `async.maxJobs` set to a value from 1 to 100 (e.g. 50) | `configured {set, 50}`, `effective 50` | `RUNWAY_AS_CONFIGURED`, exit 0 | That any job ran, that the runway was free, or that 50 is a safe or tested number. That the value survives the settings stack (F13). A value of 0 or below is floored to 1 and reads `RUNWAY_CLAMPED`, exit 1 (round-25 correction, wave-2 CriticHarnessOverclaim M1). |
| The settings page alone (`docs/settings.md:623`: type number, default 100, floored to at least 1, no maximum stated — F1) | (not a tool state — a documentation reading) | — | That a configured value above 100 takes effect: the page states no ceiling, the code clamps at 100 (F2, F3), and the upstream prose names the ceiling "default and maximum 100" (F1). That the manager's `DEFAULT_MAX_RUNNING_JOBS = 15` is the shipped cap: 15 is the fallback for a caller that passes no option (F3). |
| No `async:` block, no block-style `maxJobs` child, or no config file at all (F1, F3) | `configured {absent, null}`, `setting_default {found, 100}`, `effective 100` | `RUNWAY_DEFAULT`, exit 0 | That the file sets no `maxJobs`: the tool's line grammar does not read flow mappings or JSON-form files, so a file omp reads as `async.maxJobs: 50` written as `{async: {maxJobs: 50}}`, as JSON, or as `maxJobs` inside a flow mapping under `async:` still reads `RUNWAY_DEFAULT`, effective 100 (a false number; round-25 correction, wave-2 CriticHarnessOverclaim H1, a known tool defect for round 26). That omp can load the file. That the operator never configured a cap — `absent` also covers "the file the tool was pointed at is not the file the session reads" (F13). That a clamp is absent: the clamp is in the binary's bytes, not in the config (F2). That a pattern match is the live clamp of an 18.12.6 build: a file that merely contains the two byte patterns also matches. |
| `maxJobs` quoted, duplicated as a direct child, or `async:` carrying an inline value | `configured {malformed, null}` | effective null → `RUNWAY_UNKNOWN`, exit 2 | That the cap is zero, unlimited or absent. That the harness is unclamped. That the refusal text in a transcript can be re-derived; the tool knows only that it cannot derive the number. |
| The binary's bytes carry no clamp match (a different build, or a re-minified one) | `clamp {absent, null}` | effective null → `RUNWAY_UNKNOWN`, exit 2 | That there is no clamp. An absent match is a failed lookup, never "unlimited" and never "zero". |
| The binary cannot be read (missing path, a directory, unreadable file) | `clamp {unreadable, null}`, `setting_default {unreadable, null}`, `binary_sha256 null` | effective null → `RUNWAY_UNKNOWN`, exit 2 | That the cap is unknown-in-general; it is unknown-to-this-tool. Unavailable is not zero: no state here means "zero capacity" or "no limit". |
| The binary carries two clamp sites with different numbers | `clamp {ambiguous, null, sites 2}` | effective null → `RUNWAY_UNKNOWN`, exit 2 | Which site is live. That the smaller number is the effective one. |
| A refusal observed in a transcript: `Background job limit reached (100). Wait for running jobs to finish or cancel one.` (F6) | (not a tool state — an observation) | — | That the configured value was 100: the number is the effective cap (F3, F12). That the runway was full of *this* wave's work: the count is session-wide and shared by the whole root tree (F7). That the refused seats did anything: a refusal creates nothing (F8). That the cap is still 100 now: it is re-read at every check (F6). That every call at the cap would have errored: the auto-background paths degrade to foreground instead (F9). |
| An auto-backgrounded bash or eval call at the cap: it runs in the foreground, with no error (F9) | (not a tool state — an observation) | — | That the cap was not reached: the branch is entered *because* the cap was reached. That the call was backgrounded: it was deliberately not. That the fleet's silence at the cap means the runway was free — a foreground run and a refusal are different observations of the same cap. |
| A seat that was refused | (not a tool state) | — | That the seat ran, finished, or produced output: `register()` throws before the job exists and the tool returns `results: []` (F8). That the refusal consumed runway: it did not. |
| A spawn record reporting many started agents | (not a tool state) | — | That those agents were running: a task job is registered `queued: true` and counts only after `markRunning()` (F5). That they held slots at any particular moment. |
| The hyaku gate prints `granted lane=… seats=… cap=<target>` (85 on this host today, default 200; F11) | (not a tool state) | — | That the wave can spawn: the gate counts agents against its target and cannot see the harness's running-job count against 100 (F11). That the gate's live estimate is the harness's job count — they are different populations computed from different sources. That a refusal after a grant is a gate bug. |

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
  maximum 100", F1) but gives no reason for it. Its history is known (S104): the feature commit
  `476b858` of 2026-02-22 introduced `Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15))`
  and described the setting as "Maximum concurrent background jobs (1-100)", so the ceiling of 100 and
  the floor of 1 date from the feature's first commit. What moved afterwards is three things, not one:
  the default and the sdk fallback moved 15 to 100 on 2026-02-26 (S138); the "(1-100)" description was
  removed on 2026-05-03 (S139); and the clamp itself was rewritten on 2026-09-24 (S152, S141) from the
  static `Math.min(100, Math.max(1, …))` computed once at session construction to the function
  `() => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100)`, whose `?? 100` fallback was dropped the
  same day. The ceiling of 100 held to v18.12.6, where the clamp reads
  `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))` (`sdk.ts:2284`, F2); the explicit
  floor `Math.max(1, …)` did not survive that rewrite — neither the clamp expression nor the accessor
  (`tools/settings.ts:941-946`) carries a floor at v18.12.6. The rationale for the number 100 is not in
  the sources opened.
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

## Round-27 corrections (routed R7; wave-1 seat ReviewR7Knowledge)

Applied in place on 2026-10-22 by MoriR27 (QUALITY 77); old → new:

- U1: old "so the ceiling of 100 and the floor of 1 date from the feature's first commit and only the default moved (15 to 100)" → new: three later moves (default and fallback 15 → 100 on 2026-02-26, S138; the "(1-100)" description removed on 2026-05-03, S139; the clamp rewritten on 2026-09-24, S152, S141), the ceiling of 100 held to v18.12.6, and the explicit floor of 1 did not survive the rewrite. The round-26 draft's "floor of 1 held" was false (ReviewR7Knowledge H1) and was not carried.
- F10: old refusal list "(64, 66, 68, 88 in those records) exceeds 100 in some waves" → new: the full recorded set 64, 66, 68, 70, 71, 72, 78, 86, 88, 95, 100 with cites; no single-wave count exceeds 100; refusals accumulate across attempts (four attempts of 64 = 256 refused registrations).
