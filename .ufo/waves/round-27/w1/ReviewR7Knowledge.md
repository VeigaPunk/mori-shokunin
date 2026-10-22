# ReviewR7Knowledge — routed R7 re-verification (mori round 27, wave 1)

Seat: MoriR27.ReviewR7Knowledge (reviewer, leaf; no subagents, no background jobs). Date: 2026-10-22.
Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`, tip `5fa0a00f` (R7 not yet fixed: `corpus/lessons/round-27.md`
does not exist at this tip). Scope: re-open every source behind `.ufo/waves/round-26/w1/DraftHygieneKnowledge.md`
parts (a) U1 + F10 parenthetical and (b) `system-pressure-r24.md` lines 143, 158 and the `psi.c:1538-1550` range;
return the final correction blocks that hold. This report is the only lane file written.

Method: every URL re-fetched by curl to `/fast/scratch/hyaku/mori-r27/ReviewR7Knowledge/`, pinned with `grep -n` /
`awk NR` on the sha256-verified bytes, cross-checked against the GitHub commits API (7 commits resolved). Local
lane records read with the read tool (line-accurate; URL reads were not — see §6).

## 1. Findings by severity

**H1 — the U1 draft asserts a floor that v18.12.6 does not have.** Draft §2a.1 and the U1 NEW block say "The value
100 and the floor of 1 held to v18.12.6". False: `Math.max(1, …)` disappears at `6962d5cd2ef1` (2026-09-24). At
v18.12.6 the whole clamp path carries no floor — `sdk.ts:2284` is `Math.min(100, cfgAsyncMaxJobs.get(settings))`,
the accessor `tools/settings.ts:941-946` is a plain `register({ id: "async.maxJobs", …, default: 100 })`, and
`config/registry.ts` (sha256 `757ff479…6d25`) contains no `Math.min`/`Math.max`/clamp at all. The sentence the
draft cites as evidence refutes its own claim — the same defect class R7 routes. Corrected in the block in §2.1.

**H2 — the draft's source ids S114–S117 are taken.** `corpus/SOURCES.md` holds 132 rows (S001–S132); rows
S114–S117 landed in round 26 as earlyoom rows (`SOURCES.md:120-123`: S114 README, S115 MANPAGE, S116 meminfo,
S117 release history; the round-27 contract itself names S114/S115 as earlyoom rows). The draft's proposed rows
for the four oh-my-pi commits must renumber; next free id is **S133**. §2.1 and §3 use S133–S136 as proposals;
the owner owns final numbering.

**M1 — the F10 draft's refusal enumeration reads as exhaustive and is not.** The full `grep -n -i refus` sweep
over `.ufo/waves/round-20/build/*.md` (complete output read) records single-wave refusal counts 64, 66, 68, 70,
71, 72, 78, 86, 88, 95 and the largest, 100 — the draft lists only 64/66/68/88/100. The claim "no single-wave
refusal count exceeds 100" survives (86 at `GtLaneKama.md:74-75`, 95 at `:68`, largest 100 at
`GtLaneKaidoku.md:82`), but the block in §2.2 enumerates all of them so the corpus does not overstate.

**M2 — draft §3.1's verification note mislabels the psi.c anchors.** 1540/1545/1550/1686 are the four
`psi_show(m, &psi_system, …)` **call sites**; the reader functions start at 1538/1543/1548 and (irq) 1684. The
anchor set is correct — F3 quotes the call, and range 1538-1550 holds only two full readers (io, memory) plus the
cpu signature, so the OLD range was wrong either way. Land the block unchanged; word the commit note as "call
sites". (`round-25.md:83-84` "the corrections give `1540,1545,1550` plus `1686`" is likewise call-site-true.)

## 2. Final correction blocks — (a) harness-job-capacity-r25.md

### 2.1 U1 (entry lines 266-271; replace the whole bullet)

OLD (verbatim, `:266-271`):

```
- **U1 — why the clamp is 100.** The upstream prose states the ceiling as a fact ("default and
  maximum 100", F1) but gives no reason for it. Its history is known (S104): the feature commit
  `476b858` of 2026-02-22 introduced `Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15))`
  and described the setting as "Maximum concurrent background jobs (1-100)", so the ceiling of 100 and
  the floor of 1 date from the feature's first commit and only the default moved (15 to 100). The
  rationale for the number 100 is not in the sources opened.
```

NEW (holds; ids are proposals, next free S133):

```
- **U1 — why the clamp is 100.** The upstream prose states the ceiling as a fact ("default and
  maximum 100", F1) but gives no reason for it. Its history is known (S104): the feature commit
  `476b858` of 2026-02-22 introduced `Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15))`
  and described the setting as "Maximum concurrent background jobs (1-100)", so the ceiling of 100 and
  the floor of 1 date from the feature's first commit. What moved afterwards is three things, not one:
  the default and the sdk fallback moved 15 to 100 on 2026-02-26 (S133); the "(1-100)" description was
  removed on 2026-05-03 (S134); and the clamp itself was rewritten on 2026-09-24 (S135, S136) from the
  static `Math.min(100, Math.max(1, …))` computed once at session construction to the function
  `() => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100)`, whose `?? 100` fallback was dropped the
  same day. The ceiling of 100 held to v18.12.6, where the clamp reads
  `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))` (`sdk.ts:2284`, F2); the explicit
  floor `Math.max(1, …)` did not survive that rewrite — neither the clamp expression nor the accessor
  (`tools/settings.ts:941-946`) carries a floor at v18.12.6. The rationale for the number 100 is not in
  the sources opened.
```

Required with it: the entry's `source:` front-matter line adds S133–S136 (it lists S098…S104, S112-S113 today);
the `recheck:` line's "re-open S098–S103 and S112–S113" gains S133–S136 once numbered.

### 2.2 F10 parenthetical (entry lines 164-167; replace the [INFERENCE] sentence)

OLD (verbatim, `:164-167`):

```
as proof of what filled the runway. [INFERENCE] The number of refused seats in one wave (64, 66, 68,
88 in those records) exceeds 100 in some waves because each seat is a separate registration attempt
and every attempt fails once the count has reached the cap; the cap is a session-wide count, not a
per-wave budget.
```

NEW (holds, with the enumeration completed per M1):

```
as proof of what filled the runway. [INFERENCE] Each refused seat is a separate registration attempt and every
attempt fails once the count has reached the cap, so one wave's refusals accumulate across attempts: the four
consecutive refused attempts of 64 names each (`.ufo/waves/round-20/build/GtLaneKasegi.md:48-49`) are 256 refused
registrations against a cap of 100. No single-wave refusal count in the round-20/build records exceeds 100 — the
counts recorded there are 64 (`GtLaneKasegi.md:48-49`; also `GtLaneKaidoku.md:84`, `GtLaneTsukuroi.md:72`,
`GtMoriR17W2.md:122`), 66 (`GtLaneKama.md:72`), 68 (`GtLaneChousa.md:61`; also `GtLaneKaidoku.md:86`),
70 (`GtMoriR17W1.md:109`), 71 (`GtLaneKaidoku.md:83`), 72 (`GtLaneKama.md:73`), 78 (`GtLaneKaidoku.md:80`),
86 (`GtLaneKama.md:74-75`), 88 (`GtLaneKagi.md:58`), 95 (`GtLaneKama.md:68`), and the largest, 100
(`GtLaneKaidoku.md:82`) — the cap is a session-wide count, not a per-wave budget.
```

## 3. Final correction blocks — (b) system-pressure-r24.md

### 3.1 Line 88-90, the `psi.c:1538-1550` range (holds as drafted)

OLD (lines 88-90) → NEW:

```
All four `/proc/pressure/*` readers pass the system group (`psi_show(m, &psi_system, …)`,
([psi.c:1540,1545,1550,1686](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)), so the system CPU
`full` line is always zeros at v7.2.
```

Verified: 1540/1545/1550 are the io/mem/cpu `psi_show(m, &psi_system, …)` calls (signatures 1538/1543/1548) and
1686 the irq call (signature 1684, under `CONFIG_IRQ_TIME_ACCOUNTING` at `psi.c:1683`); 1538-1550 holds two full
readers plus the cpu signature, not four readers.

### 3.2 Line 143 (holds exactly; every pin re-verified)

NEW:

```
The cgroup v2 documentation gives each controller its own pressure file in a separate section — `cgroup.pressure` at `cgroup-v2.rst:1066-1081`, `irq.pressure` at `:1083-1087`, `cpu.pressure` at `:1215-1221`, `memory.pressure` at `:1911-1915`, `io.pressure` at `:2171-2175` (S092) — and documents `cgroup.pressure` as a per-cgroup, non-hierarchical switch.
```

Verified on sha-matched bytes: headers at 1066, 1083, 1215, 1911, 2171; section ends at 1081, 1087, 1221, 1915,
2175; "This control attribute is not hierarchical" at 1073-1075; 1066-1087 holds only `cgroup.pressure` and
`irq.pressure`, so the OLD "beside" was false.

### 3.3 Line 147, second `psi.c` anchor (holds as drafted; cgroup.c anchors stay)

OLD `([psi.c:1538-1550](…)), the latter pass` → NEW with `psi.c:1540,1545,1550,1686`. The `cgroup.c:3970-4091`
anchor stays: `cgroup_io_pressure_show` 3970-3976, `cgroup_memory_pressure_show` 3977-3983,
`cgroup_cpu_pressure_show` 3984-3990, `cgroup_irq_pressure_show` 4077-4083, `cgroup_irq_pressure_write`
4085-4090, each passing `cgroup_psi(cgrp)` at 3973/3980/3987/4080; the comment "show or hide
{cpu,memory,io,irq}.pressure files" is exact at `cgroup.c:4127`.

### 3.4 Line 158 (holds as drafted; draft's verification pins verified)

NEW (first line of the F11 bullet; rest of the sentence and the `psi.rst:70-88` pointer unchanged):

```
**F11 — no upstream threshold exists.** Neither `psi.c` nor `psi.rst` — the files read here — defines a "warn at N %" rule. The only thresholds
```

Verified: psi.rst:74 "time window, e.g. 100ms of total stall time within any 500ms window to" and psi.rst:85
"For example writing "some 150000 1000000" into /proc/pressure/memory" — both quotes sit inside the unchanged
:70-88 pointer. (The draft's own note citing "psi.rst:74"/"psi.rst:85" was correct; my earlier read-tool windows
disagreed — see §6.)

## 4. Registry rows for the U1 anchors (proposals; owner owns ids; next free S133)

All four commits resolved via the GitHub commits API (author dates verified). Row sketch, same column order as
the draft used (id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by):

```
| S133 | oh-my-pi commit 944d7f8d8d44d889b77f1865f394afd1dfb48c86 — https://github.com/can1357/oh-my-pi/commit/944d7f8d8d44d889b77f1865f394afd1dfb48c86 | code | A | the async.maxJobs default and the sdk fallback moving 15 to 100 on 2026-02-26; that one commit only | settings-schema.ts "default: 15" to "default: 100"; sdk.ts "?? 15" to "?? 100" (authored 2026-02-26T11:34:29Z; touches only CHANGELOG, settings-schema.ts, sdk.ts) | The default and the fallback can move together while the clamp value stays; a feature-commit reading is not a history. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S134 | oh-my-pi commit e398f83163723b76283c2a05b08806ba37f0773f — https://github.com/can1357/oh-my-pi/commit/e398f83163723b76283c2a05b08806ba37f0773f | code | A | the removal of the "(1-100)" description on 2026-05-03; that removal only | settings-schema.ts: line `description: "Maximum concurrent background jobs (1-100)",` deleted; `default: 100` kept (authored 2026-05-03T05:09:09Z) | A setting's published range text can be deleted while the ceiling it described stays in force. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S135 | oh-my-pi commit 6962d5cd2ef157ebf9f415acd58b8744f66400d8 — https://github.com/can1357/oh-my-pi/commit/6962d5cd2ef157ebf9f415acd58b8744f66400d8 | code | A | the 2026-09-24 rewrite of the clamp from a static value to a per-check function; that rewrite only | sdk.ts:1949 `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100),`; parent d9bc4fbd still static (`:1797`, `:1811`) (authored 2026-09-24T18:04:41Z) | The clamp site is not immutable: the same ceiling can be re-expressed as a per-check function, and the explicit floor can vanish in the rewrite. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S136 | oh-my-pi commit c4a2441d8f9195de810b3492be5bf5673cecf9c9 — https://github.com/can1357/oh-my-pi/commit/c4a2441d8f9195de810b3492be5bf5673cecf9c9 | code | A | the 2026-09-24 removal of the "?? 100" fallback; that change only | sdk.ts:1964 `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),`; diff removes `?? 100` (authored 2026-09-24T23:02:43Z) | The fallback inside the clamp can disappear without the ceiling changing. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
```

## 5. What holds — verification summary

- U1 history: feature commit (patch adds `default: 15`, the description, `Math.min(100, Math.max(1, … ?? 15))`,
  static `maxRunningJobs: asyncMaxJobs`); 944d7f8d8d44 (only settings-schema.ts + sdk.ts changed;
  `default: 15`→`100`, `?? 15`→`?? 100`); e398f8316372 (description line deleted, default 100 kept);
  6962d5cd2ef1 (function with `?? 100` at `sdk.ts:1949`; parent d9bc4fbd static at `:1797/:1811`);
  c4a2441d8f91 (`?? 100` removed, `:1964`); v18.12.6 (`:2284`, sha256 `c0228add…e957` matches the entry's
  front matter). All verified. Dates in the draft are exact.
- F10: `GtLaneKasegi.md:48-49` (four refused attempts × 64 = 256), `GtLaneKama.md:72`, `GtLaneChousa.md:61`,
  `GtLaneKagi.md:58` (88 is a refusal count there — `refused: 88, started: 0`), `GtLaneKaidoku.md:82`
  (largest, 100). All verified; saturation sweep complete (M1).
- psi.c range, line 143, line 158 blocks: hold as drafted (§3.1-§3.4), on sha-matched v7.2 bytes.
- Entry-adjacent anchors re-checked and correct: `psi.rst:57-59` (CPU-full-undefined), `psi.rst:60-65` (ratios),
  `psi.c:1282-1288` (system-CPU-full skip; comment `:1282`, condition `:1283`), `psi.rst:70-88` pointer.

## 6. Tool incident (reported to `xd://report_issue`)

The read tool's URL line-range selectors on raw.githubusercontent.com text returned content at shifting offsets
this session (psi.c `:raw:1536-1554` showed `#ifdef CONFIG_PROC_FS` at window position 7; `grep -n` on the
sha256-identical download puts it at line 1537; psi.rst and cgroup-v2.rst windows drifted by +6 and −14). Local
file range reads were line-accurate in the same session. Every line pin in this report therefore comes from
`grep -n`/`awk NR` on the curl downloads, not from URL reads. Reopen-with-line-number work should do the same.

## 7. Sources opened this round (all 2026-10-22, curl, digests verified)

- https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c — sha256 `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5` (1725 lines). Quotes: `:1538` "static int psi_io_show(struct seq_file *m, void *v)"; `:1540` "return psi_show(m, &psi_system, PSI_IO);"; `:1684` "static int psi_irq_show(struct seq_file *m, void *v)"; `:1686` "return psi_show(m, &psi_system, PSI_IRQ);"; `:1282` "/* CPU FULL is undefined at the system level */".
- …/v7.2/Documentation/accounting/psi.rst — sha256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` (188). Quotes: `:57` "CPU full is undefined at the system level, but has been reported"; `:74` "time window, e.g. 100ms of total stall time within any 500ms window to"; `:85` "For example writing "some 150000 1000000" into /proc/pressure/memory".
- …/v7.2/Documentation/admin-guide/cgroup-v2.rst — sha256 `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` (3524). Quotes: `:1066` "cgroup.pressure"; `:1073` "This control attribute is not hierarchical, so disable or enable PSI"; `:1083` "irq.pressure"; `:1215` "cpu.pressure"; `:1911` "memory.pressure"; `:2171` "io.pressure".
- …/v7.2/kernel/cgroup/cgroup.c — sha256 `3d4a256adea52d7e3f3b60dbb39622c82aa30dc398c01b5a135d2ccac3379a8c` (7544). Quotes: `:3973` "struct psi_group *psi = cgroup_psi(cgrp);"; `:4127` "/* show or hide {cpu,memory,io,irq}.pressure files */".
- oh-my-pi sdk.ts at `45c35e40c46166dc726ccc52f5d27f40f2449f99` — sha256 `c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957`. Quote `:2284` "maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),". Same file at `6962d5cd2ef1` sha256 `84f3a112…e633` (`:1949` with `?? 100`), at parent `d9bc4fbd` sha256 `fde5a959…2104` (static, `:1797`), at `c4a2441d8f91` sha256 `4f489750…9186` (`:1964`).
- oh-my-pi tools/settings.ts at `45c35e40…` — sha256 `514974143d47db0c9765bc47e86dcb9a38bd6bc23113a4ffe557bff0d8e30507` (matches entry S100). Quote `:941-946` accessor with `default: 100`, no clamp. config/registry.ts at the same commit — sha256 `757ff479907c5392a18ab85a08c3a2d4f1f8a89abb0b010ba2a501e965b46d25`, no clamp expression.
- GitHub commits API (api.github.com/repos/can1357/oh-my-pi/commits/<sha>) for `476b858b3a4a…`, `944d7f8d8d44…`, `e398f8316372…`, `6962d5cd2ef1…`, `c4a2441d8f91…`, `d9bc4fbd…`, `45c35e40…`: author dates and file lists; file patches for the settings-schema.ts/sdk.ts hunks quoted in §5 (local digest of the combined patch dump `0f061b53…8366`).
- Lane records: `.ufo/waves/round-20/build/GtLane{Kasegi,Kama,Chousa,Kagi,Kaidoku,Tsukuroi,Mado}.md`, `GtMoriR17W{1,2}.md`, `GtMoriR18W2.md` (full `grep -n -i refus` sweep, all output read), plus `corpus/knowledge/harness-job-capacity-r25.md`, `corpus/knowledge/system-pressure-r24.md`, `corpus/SOURCES.md`, `corpus/lessons/round-25.md`, `corpus/lessons/round-25-verifier-spotcheck.md` at tip `5fa0a00f`.

## 8. Residual risk and verification gaps

- `register()`'s runtime `get()` was not executed (bounds: no omp run). The H1 wording is scoped to visible
  bytes (clamp expression, accessor, registry helpers) — it does not claim runtime behavior.
- sdk.ts history between the five pinned commits was not walked hunk-by-hunk beyond the API patches; the
  6962d5cd2ef1 sdk.ts API patch was truncated (large commit), so that step is evidenced by the raw files at the
  commit and its parent, both fetched and hashed.
- The F10 sweep covers the round-20/build record files (*.md). The JSON attempt files those records cite were
  not re-opened; the claim is worded about the records, as the entry already does.
- Linux files read at tag v7.2 only; single canonical source, matching the entry's version bound.

## 9. Tooling record

No installs or upgrades (directive satisfied without): curl, jq, awk, grep, sha256sum, git (read-only,
`rev-parse`/`log` in the lane). pacman untouched (transactions paused host-wide). Scratch:
`/fast/scratch/hyaku/mori-r27/ReviewR7Knowledge/`. Privacy: no OMP settings values, session ids/paths, journal
MESSAGE text, uid/pid lists, or earlyoom flag values appear above; process-class labels only where quoted from
lane records.
