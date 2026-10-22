# DraftHygieneKnowledge — byte-exact drafts for routed R3 and R7 (mori round 26, wave 1)

Seat: MoriR26.DraftHygieneKnowledge (scribe, leaf; no subagents, no background jobs). Date: 2026-10-22. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`, read-only; this report is the only lane file written. Scratch `/fast/scratch/hyaku/mori-r26/DraftHygieneKnowledge/`.

Scope: **old → new** drafts for the routed hygiene defects named in my item; nothing below is landed by me, every edit is a proposal for the integration owner. (a) `corpus/knowledge/harness-job-capacity-r25.md` — U1 (lines 266-271) and the F10 parenthetical (lines 164-167). (b) `corpus/knowledge/system-pressure-r24.md` — lines 89, 143, 148, 158. (c) `SKILL.md` round-25 block, rows 1-4 (lines 658-661) per R3.

**Privacy.** No OMP settings value appears in this report. The one SKILL.md clause that carries the operator's configured `async.maxJobs` value is quoted with the placeholder `«OMP-SETTINGS-VALUE»`, which stands for the bytes already in the file, unchanged. No process names, command lines, uids, `--avoid`/`--prefer` expressions or journal `MESSAGE` text are copied here.

## 1. What I opened (ordinary fetch, 2026-10-22)

- oh-my-pi raw files at commit `45c35e40c46166dc726ccc52f5d27f40f2449f99` (tag v18.12.6), all HTTP 200: `packages/coding-agent/src/sdk.ts` sha256 `c0228add…e6957` (clamp `:2284`); `src/tools/settings.ts` `51497414…30507` (`:941-946`, default 100); `src/async/job-manager.ts` `0f37afaa…544e7` (`:331-335`, `:338-346`, `:371-373`); `src/tools/bash.ts` `d985ef25…3ea2` (`:882`, `:1188-1209`, `:1220-1229`); `src/tools/eval.ts` `01e9c5c5…20e3` (`:536`, `:563`); `src/eval/agent-bridge.ts` `1c34c1ab…f3bb`, 9,893 B (`:210`, `:249-251`); `src/task/workpool.ts` `8cc4b17d…dc6`, 22,838 B (`:175`, `:363`); `src/task/index.ts` `cd1df9be…b06`, 72,824 B (`:1191-1219`, `:1221-1231`, `:1233-1236`, `:1407`, `:1490`, `:1565`); `docs/tools/eval.md` `fb2fc4a1…95c`, 28,027 B (`:258`); `docs/settings.md` `0b2e1457…883`, 148,359 B (`:623`).
- oh-my-pi tarball `codeload.github.com/can1357/oh-my-pi/tar.gz/45c35e40c46166dc726ccc52f5d27f40f2449f99`, 76,435,207 B, sha256 `645df2d527de1b0ff62514ac14250230622439d5d5e84f781ffa06d38415b8d0` (whole-source grep for `register(` / `atCapacity`); oh-my-pi commits through the GitHub API (can1357/oh-my-pi) `476b858b3a4a`, `944d7f8d8d44`, `e398f8316372`, `6962d5cd2ef1`, `c4a2441d8f91` (§2a.1). - Linux v7.2 raw files at tag `v7.2`: `kernel/sched/psi.c` sha256 `452318be…32c5`, 1,725 lines (readers at 1540/1545/1550/1686); `Documentation/accounting/psi.rst` `11c6b712…2692`, 188 lines (`:57-58`, `:60-65`, `:70-88`); `Documentation/admin-guide/cgroup-v2.rst` `a9433bb0…b7ad`, 3,524 lines (`:1066`, `:1083`, `:1215`, `:1911`, `:2171`); `kernel/cgroup/cgroup.c` `3d4a256a…9a8c` (`:3973`, `:3980`, `:3987`, `:4080`, `:4127`). - Ordinary HTTPS GETs only; no headless browser, no bot challenge.

## 2. (a) `corpus/knowledge/harness-job-capacity-r25.md`

### 2a.1 The oh-my-pi history, re-verified by ordinary fetch

- **2026-02-22T11:44:23Z `476b858b3a4a`** (feature): adds `const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15));` (sdk.ts added line 726) and the schema entry `description: "Maximum concurrent background jobs (1-100)"`, `default: 15`.
- **2026-02-26T11:34:29Z `944d7f8d8d44`**: `default: 15` → `100`; sdk `?? 15` → `?? 100`; the clamp value is unchanged. - **2026-05-03T05:09:09Z `e398f8316372`**: deletes the line `description: "Maximum concurrent background jobs (1-100)",` from `config/settings-schema.ts`; default 100 kept. - **2026-09-24 (author 18:04:41Z) `6962d5cd2ef1`**: the clamp is rewritten to a function — sdk.ts:1949 `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100),`; its parent `d9bc4fbd` still holds the static `maxRunningJobs: asyncMaxJobs`. - **2026-09-24T23:02:43Z `c4a2441d8f91`**: `… ?? 100` is dropped from that function. - **2026-10-21, tag `v18.12.6` = `45c35e40`**: `sdk.ts:2284` `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),`, unchanged since `c4a2441d`.

"Only the default moved (15 to 100)" is therefore false: the default **and** the sdk fallback moved on 2026-02-26, the "(1-100)" description was deleted on 2026-05-03, and the clamp expression was rewritten twice on 2026-09-24. The value 100 and the floor of 1 did hold from the feature commit to v18.12.6.

### 2a.2 U1 — old → new (entry lines 266-271)

OLD (verbatim):

```
- **U1 — why the clamp is 100.** The upstream prose states the ceiling as a fact ("default and
  maximum 100", F1) but gives no reason for it. Its history is known (S104): the feature commit
  `476b858` of 2026-02-22 introduced `Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15))`
  and described the setting as "Maximum concurrent background jobs (1-100)", so the ceiling of 100 and
  the floor of 1 date from the feature's first commit and only the default moved (15 to 100). The
  rationale for the number 100 is not in the sources opened.
```

NEW:

```
- **U1 — why the clamp is 100.** The upstream prose states the ceiling as a fact ("default and
  maximum 100", F1) but gives no reason for it. Its history is known (S104): the feature commit
  `476b858` of 2026-02-22 introduced `Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15))`
  and described the setting as "Maximum concurrent background jobs (1-100)", so the ceiling of 100 and
  the floor of 1 date from the feature's first commit. What moved afterwards is three things, not one:
  the default and the sdk fallback moved 15 to 100 on 2026-02-26 (S114); the "(1-100)" description was
  removed on 2026-05-03 (S115); and the clamp itself was rewritten on 2026-09-24 (S116, S117) from the
  static `Math.min(100, Math.max(1, …))` computed once at session construction to the function
  `() => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100)`, whose `?? 100` fallback was dropped the
  same day. The value 100 and the floor of 1 held to v18.12.6, where the clamp reads
  `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))` (`sdk.ts:2284`, F2). The
  rationale for the number 100 is not in the sources opened.
```

Registry rows the new anchors need (the registry holds 113 rows, S001-S113; the ids are proposals, the owner owns the final numbering). Column order: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by.

```
| S114 | oh-my-pi commit 944d7f8d8d44 — https://github.com/can1357/oh-my-pi/commit/944d7f8d8d44d889b77f1865f394afd1dfb48c86 | code | A | the async.maxJobs default and the sdk fallback moving 15 to 100 on 2026-02-26; that one commit only, not later behaviour | settings-schema.ts "async.maxJobs" default 15 to 100; sdk.ts "?? 15" to "?? 100"; commit 944d7f8d8d44 (authored 2026-02-26T11:34:29Z) | The default and the fallback can move together while the clamp value stays; a feature-commit reading is not a history. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S115 | oh-my-pi commit e398f8316372 — https://github.com/can1357/oh-my-pi/commit/e398f83163723b76283c2a05b08806ba37f0773f | code | A | the removal of the "(1-100)" UI description for async.maxJobs on 2026-05-03; that removal only | config/settings-schema.ts: the line description "Maximum concurrent background jobs (1-100)" deleted; commit e398f8316372 (authored 2026-05-03T05:09:09Z) | A setting's published range text can be deleted while the ceiling it described stays in force; the range text is not the clamp. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S116 | oh-my-pi commit 6962d5cd2ef1 — https://github.com/can1357/oh-my-pi/commit/6962d5cd2ef1 | code | A | the 2026-09-24 rewrite of the async.maxJobs clamp from a static value computed at session construction to a function re-read per check; that rewrite only | sdk.ts:1949 maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100); parent d9bc4fbd still carries the static form; commit 6962d5cd2ef1 (authored 2026-09-24T18:04:41Z) | The clamp site is not immutable: the same ceiling can be re-expressed as a per-check function. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S117 | oh-my-pi commit c4a2441d8f91 — https://github.com/can1357/oh-my-pi/commit/c4a2441d8f91 | code | A | the 2026-09-24 removal of the "?? 100" fallback from the async.maxJobs clamp function, leaving the v18.12.6 form; that change only | sdk.ts maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100) to maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)); commit c4a2441d8f91 (authored 2026-09-24T23:02:43Z) | The fallback inside the clamp can disappear without the ceiling changing; "the default moved" is not the whole history. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
```

Also required: the entry's `source:` front-matter line must name S114-S117 (it currently lists S098…S104, S112-S113).

### 2a.3 F10 — the mis-cited parenthetical

"(64, 66, 68, 88 in those records)" attributes four numbers to the two cited records. Those two hold 64 (`GtLaneKasegi.md:48`) and 66 (`GtLaneKama.md:72`); 68 and 88 live in other round-20/build records. The follow-on clause "exceeds 100 in some waves" is unsupported: no single-wave refusal count in those records exceeds 100 (the largest is 100). OLD (entry lines 164-167, verbatim):

```
as proof of what filled the runway. [INFERENCE] The number of refused seats in one wave (64, 66, 68,
88 in those records) exceeds 100 in some waves because each seat is a separate registration attempt
and every attempt fails once the count has reached the cap; the cap is a session-wide count, not a
per-wave budget.
```

NEW:

```
as proof of what filled the runway. [INFERENCE] Each refused seat is a separate registration attempt and every
attempt fails once the count has reached the cap, so one wave's refusals accumulate across attempts: the four
consecutive refused attempts of 64 names each in (`.ufo/waves/round-20/build/GtLaneKasegi.md:48-49`) are 256
refused registrations against a cap of 100. No single-wave refusal count in the round-20/build records exceeds
100: 64 (`.ufo/waves/round-20/build/GtLaneKasegi.md:48`), 66 (`.ufo/waves/round-20/build/GtLaneKama.md:72`),
68 (`.ufo/waves/round-20/build/GtLaneChousa.md:61`), 88 (`.ufo/waves/round-20/build/GtLaneKagi.md:58`), and the
largest, 100 (`.ufo/waves/round-20/build/GtLaneKaidoku.md:82`); the cap is a session-wide count, not a per-wave
budget.
```

Record lines verified: `GtLaneKasegi.md:48-49` ("All 64 names refused"; "build-refusal-2.json, build-attempt-3.json, build-attempt-4.json: same refusal, all 64 names"); `GtLaneKama.md:72` ("seats 66, refused 66, spawned 0"); `GtLaneChousa.md:61` ("refused all 68 … refused 68"); `GtLaneKagi.md:58` ("`refused: 88, started: 0`" with the limit message); `GtLaneKaidoku.md:82` ("refused 100 (result null), then refused 0"). Note for the owner: the round-25 wave-2 review called 88 a dispatch count; the bytes show 88 is a refusal count in `GtLaneKagi.md:58`, but not in the two records the entry cited. The correction keeps 88 and attributes it correctly.

## 3. (b) `corpus/knowledge/system-pressure-r24.md`

The entry already states the right wording in its own corrections bullet (`:42-44`: "F3's readers are `psi.c:1540,1545,1550` plus the irq reader at `psi.c:1686`; in F9 the cgroup files sit in separate sections of cgroup-v2.rst (1083, 1215, 1911, 2171); F11's 'no threshold rule' is scoped to `psi.c` and `psi.rst`, the files read"). The body still carries the superseded wording; the four edits below make the body match it.

**3.1 Line 89 (F3) — the `psi.c:1538-1550` range.** OLD (lines 88-90):

```
All four `/proc/pressure/*` readers pass the system group (`psi_show(m, &psi_system, …)`,
([psi.c:1538-1550](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)), so the system CPU
`full` line is always zeros at v7.2.
```

NEW:

```
All four `/proc/pressure/*` readers pass the system group (`psi_show(m, &psi_system, …)`,
([psi.c:1540,1545,1550,1686](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)), so the system CPU
`full` line is always zeros at v7.2.
```

Verified at v7.2: `psi.c:1540` (`psi_io_show`), `:1545` (`psi_memory_show`), `:1550` (`psi_cpu_show`), `:1686` (`psi_irq_show`, under `CONFIG_IRQ_TIME_ACCOUNTING`); 1538-1550 holds three of the four readers.

**3.2 Line 143 (F9) — "beside".** OLD (line 143):

```
The cgroup v2 documentation lists `irq.pressure` beside `cpu`, `io` and `memory.pressure` and documents `cgroup.pressure` as a per-cgroup, non-hierarchical switch (S092, `cgroup-v2.rst:1066-1087`).
```

NEW:

```
The cgroup v2 documentation gives each controller its own pressure file in a separate section — `cgroup.pressure` at `cgroup-v2.rst:1066-1081`, `irq.pressure` at `:1083-1087`, `cpu.pressure` at `:1215-1221`, `memory.pressure` at `:1911-1915`, `io.pressure` at `:2171-2175` (S092) — and documents `cgroup.pressure` as a per-cgroup, non-hierarchical switch.
```

Verified at v7.2: `cgroup-v2.rst:1066` `cgroup.pressure`, `:1083` `irq.pressure`, `:1215` `cpu.pressure`, `:1911` `memory.pressure`, `:2171` `io.pressure`; 1066-1087 holds only `cgroup.pressure` and `irq.pressure`, so "beside" was false and the cited range held no `cpu`, `io` or `memory` pressure file.

**3.3 Line 148 (F9) — the same range, second occurrence.** OLD (the `psi.c` anchor inside lines 146-149; the rest of the sentence is unchanged):

```
([psi.c:1538-1550](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)), the latter pass
```

NEW:

```
([psi.c:1540,1545,1550,1686](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)), the latter pass
```

The `cgroup.c:3970-4091` anchor beside it stays: that range holds the four per-controller readers (`cgroup_io_pressure_show` 3970-3976, `cgroup_memory_pressure_show` 3977-3983, `cgroup_cpu_pressure_show` 3984-3990, `cgroup_irq_pressure_show` 4077-4083, each passing `cgroup_psi(cgrp)` at 3973/3980/3987/4080), and the comment at `cgroup.c:4127` is exact.

**3.4 Line 158 (F11) — scope the negative claim.** OLD (lines 158-159; only the first line changes, the rest of the sentence and the `psi.rst:70-88` pointer are unchanged):

```
**F11 — no upstream threshold exists.** The kernel source defines no "warn at N %" rule. The only thresholds
in the documentation are the user's own trigger values, given as examples ("100ms of total stall time within
```

NEW:

```
**F11 — no upstream threshold exists.** Neither `psi.c` nor `psi.rst` — the files read here — defines a "warn at N %" rule. The only thresholds
in the documentation are the user's own trigger values, given as examples ("100ms of total stall time within
```

Verified: `psi.rst:74` "100ms of total stall time within any 500ms window"; `psi.rst:85` "some 150000 1000000".

## 4. (c) `SKILL.md` round-25 block, rows 1-4 (lines 658-661)

Upstream facts behind these drafts, re-read at tag `v18.12.6` today: `atCapacity` has exactly three hits in the shipped source — the getter `async/job-manager.ts:338`, the bash auto-background guard `tools/bash.ts:1228`, the eval auto-background guard `tools/eval.ts:536` (whole-source grep over the 76 MB tarball). Twelve `register()` call sites exist: `eval/agent-bridge.ts:210`; `eval/judgment-batch-bridge.ts:223`; `modes/controllers/tan-command-controller.ts:144`; `security/coordinator.ts:499`; `task/executor.ts:3272`; `task/index.ts:1407`; `task/restore.ts:85`; `task/workpool.ts:175` and `:363`; `vibe/runtime.ts:1370`; `tools/bash.ts:882`; `tools/eval.ts:563` — ten of them with no `atCapacity` check of their own. `docs/tools/eval.md:258`: "`agent()` fails with `Background job limit reached` once that cap is full." `tools/bash.ts:1188-1209` (explicit `async: true`) goes straight to `manager.register` (`tools/bash.ts:882`) with no pre-check; `task/index.ts:1191-1219` catches per spawn, so a batch can partially start; `:1221-1231` is the all-refused report, `:1233-1236` the partial-batch suffix.

**4.1 Row 1 (SKILL.md:658) — the garbled host sentence.** OLD clause (the only part of row 1 that R3 routes; `«OMP-SETTINGS-VALUE»` stands for the bytes already in the file):

```
that the operator configured 100 (this host's the operator's OMP settings file says «OMP-SETTINGS-VALUE» and the clamp reduces it to 100);
```

NEW, variant A — grammar only, value unchanged (minimal repair of the retention garble):

```
that the operator configured 100 (the operator's OMP settings file says «OMP-SETTINGS-VALUE» and the clamp reduces it to 100);
```

NEW, variant B — recommended: drop the host value from a durable document (the round-26 bound forbids copying OMP settings values, and the value is host-and-day specific; the entry's F12 carries the dated observation):

```
that the operator configured 100 (the operator's OMP settings file sets a value above the clamp, and the clamp reduces it to 100; that file is one host's configuration, not a fleet fact — `corpus/knowledge/harness-job-capacity-r25.md` F12);
```

The rest of row 1 (trigger, effective-cap formula, the `job-manager.ts:331-335` re-read pointer, `results: []` at `:1229`) is unchanged by this item.

**4.2 Row 2 (SKILL.md:659) — R3's core defect.** OLD (verbatim row):

```
| a bash or eval call was made while the cap was full | nothing — the auto-background branch checks `atCapacity` first and runs in the foreground instead (`tools/bash.ts:1220-1229`, `tools/eval.ts:536`) | that the cap was not reached; that the call was backgrounded |
```

NEW:

```
| an **auto-backgrounded** bash call, or the eval tool's auto-background branch, was made while the cap was full | nothing from that call — the auto-background branch checks `atCapacity` first and runs in the foreground instead (`tools/bash.ts:1220-1229`, `tools/eval.ts:536`) | that the cap was not reached; that the call was backgrounded; that every call at the cap is silent — eval `agent()`, `workpool()` and an explicit `async: true` bash reach `register()` with no `atCapacity` check and do raise the refusal (`docs/tools/eval.md:258`; `eval/agent-bridge.ts:210`; `task/workpool.ts:175,363`; `tools/bash.ts:1188-1209`) |
```

**4.3 Row 3 (SKILL.md:660) — too few refusing paths.** OLD (verbatim row):

```
| a `task` spawn or an explicit `async: true` bash was refused | one refused registration; a batch can partially start, so refusals and starts coexist in one result | that the wave is dead — a refusal creates no job; that the count was this wave's own seats: the population is every **running, non-queued** job in the session tree — bash, task and eval alike (`job-manager.ts:343,367`, `:48`; `tools/bash.ts:882`) — and a parked (queued) task job counts only after `markRunning()` (`task/index.ts:1565,1490`) |
```

NEW:

```
| a registration was refused — a `task` spawn, an eval `agent()` or `workpool()` batch, a vibe subagent, or an explicit `async: true` bash | one refused registration; a batch can partially start, so refusals and starts coexist in one result (`task/index.ts:1191-1219`, `:1233-1236`) | that the wave is dead — a refusal creates no job; that the count was this wave's own seats: the population is every **running, non-queued** job in the session tree — bash, task and eval alike (`job-manager.ts:343,367`, `:48`; `tools/bash.ts:882`) — and a parked (queued) task job counts only after `markRunning()` (`task/index.ts:1565,1490`); that the paths named here are the only ones that can refuse — of the twelve `register()` call sites in the shipped source only the bash and eval auto-background branches pre-check `atCapacity`, so ten sites refuse with no check of their own (`eval/agent-bridge.ts:210`; `eval/judgment-batch-bridge.ts:223`; `modes/controllers/tan-command-controller.ts:144`; `security/coordinator.ts:499`; `task/executor.ts:3272`; `task/index.ts:1407`; `task/restore.ts:85`; `task/workpool.ts:175,363`; `vibe/runtime.ts:1370`) |
```

**4.4 Row 4 (SKILL.md:661) — the missing false-number caveat.** OLD (the row's third cell, verbatim; the first two cells are unchanged):

```
that the session was at capacity — the tool reports the **cap**, never a running-job count, and the live count is not readable from outside the session (`contract.md:83-84`); that an absent or unreadable clamp means "no clamp" (it is `RUNWAY_UNKNOWN`); that the file's `async.maxJobs` is the value the session resolved — the runtime settings stack has project and overlay layers the tool does not read (`corpus/knowledge/harness-job-capacity-r25.md` F13)
```

NEW:

```
that the session was at capacity — the tool reports the **cap**, never a running-job count, and the live count is not readable from outside the session (`contract.md:83-84`); that an absent or unreadable clamp means "no clamp" (it is `RUNWAY_UNKNOWN`); that the file sets no `maxJobs` — `RUNWAY_DEFAULT` also reads a root flow mapping, a JSON file or a flow-mapped `maxJobs` child as absent, so the effective 100 is the schema default rather than a value read from the file (`corpus/knowledge/harness-job-capacity-r25.md` decision row `RUNWAY_DEFAULT`); that the file's `async.maxJobs` is the value the session resolved — the runtime settings stack has project and overlay layers the tool does not read (`corpus/knowledge/harness-job-capacity-r25.md` F13)
```

That caveat is the entry's own recorded tool defect (`corpus/knowledge/harness-job-capacity-r25.md:211`, round-25 correction, wave-2 `CriticHarnessOverclaim` H1); the underlying tool fix is routed elsewhere (R1).

**4.5 Registry rows the new anchors need.** Rows 2-4 cite `eval/agent-bridge.ts`, `task/workpool.ts` and `task/index.ts`, which have **no** row in `corpus/SOURCES.md` today (grep for `task/index|task/workpool| eval/agent-bridge|workpool\.ts` returns no match); the entry cites `task/index.ts` at F5, F7, F8, F10 without a row either. Proposed rows (ids to be set by the owner; same column order as §2a.2):

```
| S118 | oh-my-pi eval/agent-bridge.ts at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/eval/agent-bridge.ts | code | A | how eval agent() registers with the session's async job manager: it registers without a capacity check, so it raises the cap refusal rather than degrading; v18.12.6 only | :204-210 (manager, manager.register("task", id, …)); :249-251 (rethrow); HTTP 200, 9,893 B, sha256 1c34c1ab4b4ec6d2119025be077e678cdf7074295cd796be6cbbd1d36a10f3bb | A cell that spawns agents can still be refused at the cap even when the eval tool's own backgrounding degrades to foreground. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md, SKILL.md |
| S119 | oh-my-pi task/workpool.ts at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/task/workpool.ts | code | A | how workpool() registers its pool job and its batch with the async job manager: both register without a capacity check; v18.12.6 only | :175 (pool job registration), :363 (batch registration); HTTP 200, 22,838 B, sha256 8cc4b17def435db43d49294dbc67946585c009832d3faf0b21aebaed59be6dc6 | A pool is one registration and a batch is another; both draw on the same session-wide cap without pre-checking it. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md, SKILL.md |
| S120 | oh-my-pi task/index.ts at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/task/index.ts | code | A | how a task spawn batch registers, how a refusal inside one batch is caught per spawn, and the two report shapes; v18.12.6 only | :1191-1219 (per-spawn register and catch, discard at :1213); :1221-1231 (all-refused report, results: [] at :1229); :1233-1236 (partial-batch suffix); :1407 (register); :1490 (markRunning); :1565 (queued: true); HTTP 200, 72,824 B, sha256 cd1df9be9086ae151a8053688b99c869179413a221a9a0e519a5c8af9cc82b06 | A wave's spawns are separate registrations, so one batch can start and refuse at once; "results: []" belongs to the all-refused shape only. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md, SKILL.md |
```

The block header ("Grounded in `corpus/knowledge/harness-job-capacity-r25.md` (sources S098-S104, S112-S113)") also needs the new ids once the rows land.

## 5. Adjacent findings (not routed; for the owner, no draft)

- `corpus/knowledge/harness-job-capacity-r25.md` F9 (lines 142-156) names only the auto-background consumers and the explicit-async bash as raising paths, not eval `agent()` or `workpool()`; the entry's decision row 217 keeps the shorter list.
- `SKILL.md:654` gives only the all-refused wrapper form (`Failed to start background task job{s}: …`); the partial-batch form is `Failed to schedule N spawn(s): <agentId>: <message>.` (`task/index.ts:1233-1236`). - `corpus/knowledge/system-pressure-r24.md:198-199` ("The kernel defines no such threshold (F11)") repeats the unscoped negative that §3.4 scopes; it is a Limits bullet, not one of the routed lines. - `corpus/lessons/round-25.md:82-84` says of D2 "Not fixed: two F3 citation ranges (`psi.c:1538-1550` where the corrections give `1540,1545,1550` plus `1686`)". Once §3.1 and §3.3 land, that "Not fixed" note is stale and needs a one-line update in the same round.

## 6. Limits of this draft

Read-only everywhere: no lane file except this report, no `jj`, no git write in the lane, no upstream repository touched, no `omp` run, and the operator's settings file was not read. The oh-my-pi history rests on the GitHub commits API and on `raw.githubusercontent.com` bytes at the named commits; the sdk.ts history between `v15.1.9` and `6962d5cd` was not walked commit by commit, so "the clamp was rewritten on 2026-09-24" describes those two commits and their parent, not an exhaustive scan. The Linux files were read at tag v7.2 only. The twelve `register()` sites and the three `atCapacity` hits were counted over `packages/coding-agent/src` of the v18.12.6 tarball. I did not run the round-25 tool or the harness: every behaviour claim above is a code reading, not a runtime observation.

## 7. Tooling record and artifact paths

Nothing installed or upgraded; no pacman, uv, cargo or npm transaction (pacman transactions are paused host-wide this round). Existing tools used, all read-only: `curl` 8.x (HTTP GET of raw.githubusercontent.com, codeload, and the GitHub API via `gh` 2.102.0, authenticated), `tar`, `awk`/`grep`/`sha256sum`, `git` read-only (`log`, `show`, `diff`) in the lane. `~/.omp/agent/RULES.md` was read first; its tooling directive required no install for this task. This report: `.ufo/waves/round-26/w1/DraftHygieneKnowledge.md` (lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`). Fetched bytes and digests: `/fast/scratch/hyaku/mori-r26/DraftHygieneKnowledge/` (outside the lane; may be deleted).
