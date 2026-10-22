# SiblingOverlap — mori round 25, wave 1

Seat: MoriR25.SiblingOverlap (connector-style read-only scan; leaf, no subagents). Date 2026-10-22.
Scope: sibling lane repos `/home/vgpnk/Projects/shokunin/*-shokunin` other than mori, read-only, for
`maxJobs`, `Background job limit`, `maxRunningJobs`, `job limit` and `maxConcurrency` (case-insensitive).
I also checked the fleet seat gate and the installed binary bytes where they bear on the question.

## Verdict (short)

- **C2 does not duplicate any sibling entry.** No sibling's `corpus/knowledge`, `PROVINCE.md` or `SKILL.md` covers
  `async.maxJobs`, `maxRunningJobs` or the binary's clamp to 100. Every sibling mention is a *refusal record*: a
  lesson or LOG line quoting `Background job limit reached (100)`. None explains the cap or detects it.
- **Ownership:** writing harness configuration is **operator-owned**. No lane writes `~/.omp`. *Analysis* of OMP
  task and job semantics is **kumitate's** frontier ground. Mori's C2 (read-only detection, configured vs
  effective) fits mori's own "resource runway" core and does not take over either role.
- **C2 must route one item:** to kumitate, the gap in its OMP contract entry (no job cap, default 32 stated,
  "effective live OMP setting is UNKNOWN"). This is routed, never edited.
- **No sibling knowledge treats the job cap as 200.** The 200 figures in siblings refer to the seat gate or a
  round budget, not the omp job cap. The only "200 as capacity" text is at the fleet root, not in a sibling lane;
  it is listed below for L1 to route.
- **C1 has no sibling overlap.** No sibling references `mori-pressure`, `system-pressure-r24`, `mori-routed` or
  mori's round-24 spot-check.

## Evidence

### 1. Sibling hits on the five terms (requested surfaces)

Command: `rg -n -i --hidden -g '!**/.ufo/**' -g '!**/.git/**' -g '!**/.jj/**' -g '!**/census/**' -g '!**/sandboxes/**'
'maxJobs|Background job limit|maxRunningJobs|job limit|maxConcurrency' <each sibling>`. The run returned 32 matching
lines (`… | wc -l` → 32). The ones that bear on the omp job cap fall into these groups:

| Kind | Sibling locations | Content |
|---|---|---|
| Refusal records, 100 (lessons, LOG, considerthese) | `kagi-shokunin/corpus/lessons/round-21.md:91`; `kaidoku-shokunin/corpus/lessons/round-17.md:91`, `round-24.md:76`; `kama-shokunin/corpus/lessons/round-15-verifier-spotcheck.md:56`, `round-19-verifier-spotcheck.md:10`, `LOG.md:876`; `kumitate-shokunin/corpus/lessons/round-37-verifier-spotcheck.md:14`, `considerthese/2026-10-21.md:13`; `mado-shokunin/corpus/lessons/round-22.md:76`, `LOG.md:676,1409,1509`; `revenger-shokunin/LOG.md:795`; `souji-shokunin/corpus/lessons/round-18.md:103`, `round-20.md:102`; `tameshi-shokunin/LOG.md:565`; `tsukuroi-shokunin/corpus/lessons/round-24.md:53`, `LOG.md:1073,1077`; `kagi-shokunin/LOG.md:1024` | quote `Background job limit reached (100)` as an observed refusal; none states a mechanism or a configured value |
| Refusal record that names both limits | `kaidoku-shokunin/corpus/evidence/round-25/proposal/distiller-refusal.json:1` | "Guard granted1 with live162/pending0/cap200; **guard and process-job limits differ**" next to the error `Background job limit reached (100)`. This is correct and agrees with C2 |
| `task.maxConcurrency` knowledge (a different setting) | `kumitate-shokunin/corpus/knowledge/omp-task-contract.md:70,82,197`; `kumitate-shokunin/corpus/knowledge/kimi-modes-machinery.md:138`; `kumitate-shokunin/corpus/knowledge/native-trial-launch.md:339`; `kumitate-shokunin/SKILL.md:205`; `kumitate-shokunin/corpus/lessons/round-34.md:68`; `kasegi-shokunin/corpus/knowledge/ufo-workspaces.md:296`; `chousa-shokunin/LOG.md:262` | the session semaphore (`task.maxConcurrency`, default 32; 0 = unlimited), never `async.maxJobs` |

Broader mechanism search across the same surfaces (`job-manager`, `AsyncJobManager`, `JobManager`, `Math.min(100`,
`process job cap/limit`, `100-job`, `job cap`, `background job cap/limit`) returned only more refusal records
(for example `tsukuroi-shokunin/LOG.md:1021` "process-wide 100-job cap"; `kasegi-shokunin/considerthese/2026-10-21.md:80-82`
"64-seat waves against a 100-job cap shared across the fleet look structurally oversubscribed"). It found **0** hits for
`job-manager`, `JobManager` or `maxRunningJobs` in any sibling outside `.ufo/` (same command, output above).

The named siblings, one by one:
- **tsukuroi:** refusal records only (`corpus/lessons/round-24.md:53`: "Main lowered the seat-gate cap to 85").
  Its province is the OS substrate (`PROVINCE.md:3-4`). Its own province table hands OMP task/hub semantics to
  kumitate (`PROVINCE.md:126`: "task/hub dispatch and routing semantics are its analysis, not tsukuroi's").
- **kumitate:** the only sibling with OMP harness knowledge (`corpus/knowledge/omp-task-contract.md`), but that entry
  covers `task.maxConcurrency` and `async.enabled` only (`:70`, `:82`). Nothing on `async.maxJobs` or the job cap.
- **kama:** refusal records only. Its write boundary excludes `~/.omp` (`PROVINCE.md:45`). Its round-15 boundary advice
  already observed that kumitate's `omp-task-contract.md:70-74` "says nothing about a job limit or its scope"
  (`kama-shokunin/.ufo/waves/round-15/build/advice/SiblingBoundary.md:32`) and assigned "the scope or cause of the job
  limit" to kumitate (`:128`). That gap is still open today (search above).
- **kotodama:** one refusal record with no number (`corpus/lessons/round-50.md:83`, "refused by the job cap"). Its
  province is worldbuilding (`PROVINCE.md:3-7`), so it has no harness ground.

### 2. Who owns harness configuration

- Operator: the open L0 question marks raising the effective limit as operator-owned:
  `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:96` ("operator-owned: why the process enforces 100, and whether a
  restart or another key is needed"). The round bounds forbid editing `~/.omp/agent/config.yml` (round-25 contract
  assignment).
- kumitate: analysis of OMP task/hub semantics. `kumitate-shokunin/PROVINCE.md:3` ("scopes OMP task/hub"), `:19`
  ("OMP harness contract … first entry `corpus/knowledge/omp-task-contract.md`" on its Frontier band). Its launcher
  treats the global OMP config as "the SOLE routing authority" and only reads it (`kumitate-shokunin/SKILL.md:202-205`).
- mori: `PROVINCE.md:10` and `:26` own "resource runway" as a read-only probe; `:14` refuses "dispatch and
  orchestration mechanism (→ kumitate)"; `:17` "Detection and report only — never remediation."
- No sibling claims write ownership of `~/.omp` settings.

### 3. Does C2 overlap, and what must route

C2 (contract `.ufo/waves/round-25/contract.md:39-92`) reads one config file and the binary bytes, and reports a
verdict. It explains no job-manager semantics and changes nothing, so it sits inside mori's runway band. The
mechanism fact it depends on (clamp at 100) is kumitate's ground. Mori cites it as a source and does not own it.

Binary facts behind the routing (byte reads only, `~/.local/bin/omp`, 256,702,432 bytes per `ls -l`):
- `LC_ALL=C rg -a -n -o '.{0,200}maxRunningJobs.{0,200}'` → line 1421704 `maxRunningJobs: () => Math.min(100, XPe.get(R))`
  and line 1258472 `this.#P = e.maxRunningJobs;`.
- `rg -a -U -o 'var XPe = h\(\{[^}]{0,200}\}'` → `var XPe = h({ id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100`.
  So `XPe` is the `async.maxJobs` setting.
- The error template is ``Background job limit reached (${o}). Wait for running jobs to finish or cancel one.``.
- `rg -a -o 'Math\.min\(\s*\d+\s*,\s*[\w$]+\.get\([\w$]+\)\s*\)'` returns exactly one site (the one above). The
  `task.maxConcurrency` setting (`var oB = h({ id: "task.maxConcurrency", … default: 32`) has no clamp of that shape.
- Live config: `~/.omp/agent/config.yml:131` `maxConcurrency: 200` (under `task:` at `:130`) and `:245` `maxJobs: 200`
  (under `async:` at `:244`).

**Route R1 → kumitate** (cross-lane, report, never edit): `kumitate-shokunin/corpus/knowledge/omp-task-contract.md` has no
`async.maxJobs` entry and no job cap. Its `:197` says "the OMP session semaphore default (`task.maxConcurrency=32`) … The
effective live OMP setting is UNKNOWN." On this host the configured semaphore is 200 (`config.yml:131`), and that setting
is not clamped by the binary's only setting-clamp site. Background task spawns, however, are refused once 100 jobs run
(`Math.min(100, XPe.get(R))`, `XPe` = `async.maxJobs`). Its docs pin upstream `main` (`PROVINCE.md:19`), while mori's C2
pins the 18.12.6 tag. [INFERENCE] The binding limit for async spawns is therefore the job cap of 100, not the semaphore,
because shell jobs also count against the job cap (contract `:40-41`).

Nothing has to route to tsukuroi, kama or kotodama.

### 4. Does any sibling treat the cap as 200?

None. Command: the same scoped `rg` with `async\.`, `cap ?200`, `200[- ](concurrent|jobs?|background|seat|subagent)`,
`(job|seat)[- ]?(cap|limit|ceiling)…200` and `live\d+/pending\d+/cap`. The 200 hits are all seat-gate or budget figures:
- `kake-shokunin/corpus/lessons/round-27.md:171` and `kake-shokunin/LOG.md:1164`: "The200-seat slot was granted"
  (a seat-gate grant). The wave was 85 seats and spawned on the first attempt, consistent with a 100-job cap.
- `mado-shokunin/LOG.md:1371`: "163 of ≤200 seats spent" (a round budget, not a concurrency cap).
- `kaidoku-shokunin/corpus/evidence/round-25/proposal/distiller-refusal.json:1`: separates guard cap 200 from the process
  limit 100 explicitly (correct).

These are not sibling knowledge, but L1 may want to route them because they present 200 as capacity:
- `/home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md:54-55` lists "Capacity facts … `async.maxJobs` 200,
  `task.maxConcurrency` 200" from config. This is the configured value, not the effective one. Route to the fleet
  orchestrator or operator, not to a lane.
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/wave-slot.sh:2,5,40`: the seat gate's default target is 200; `:7` already
  notes the 100 refusal. The live state file overrides it: `~/.local/state/shokunin-hyaku/wave-cap` holds `85` (mtime
  2026-10-22 05:30). This is a fleet script that seats must not edit.
- [INFERENCE] This seat's own harness prompt says "Max 200 concurrent subagents; excess queue." The text is not in the
  binary as plain bytes (`rg -a -i -c` for `concurrent sub` and `excess queue` → 0), so its source is unconfirmed. If it
  renders `task.maxConcurrency` (200), it misleads agents: past 100 jobs, task spawns are refused, not queued (the error
  template above). Route to the operator as an observation only.

### 5. C1 sibling overlap

- `rg -l` across siblings (same exclusions) for `mori-pressure`, `system-pressure-r24`, `mori-routed` and
  `round-24-verifier-spotcheck.md:1[34]` → no files. D1–D4 are mori-internal.
- D4 convention check: `__pycache__/` is the dominant sibling ignore line (kaidoku, kama, kasegi, kengaku, kotoba,
  kotodama, lore, mado, tameshi, tsukuroi). `mori-shokunin/.gitignore:3` already holds `__pycache__/` in the working
  tree (lane HEAD `09f55b628c21` "round-25: land tools/mori-job-runway.py (C2) after the frozen cases; D4 ignore rule").
  That matches the sibling convention and is one of C1's accepted lines (contract `:23`).

## Proposed move (one, bounded)

**Axes:** coverage (C2) and adjacency (held at 6). Neither calibration nor operability is harmed.

The move is to add a short "Three ceilings" paragraph and a "Routed" line to C2's knowledge entry
`corpus/knowledge/harness-job-capacity-r25.md`, with no change to the tool or the frozen cases.

The paragraph names, with the cites above:
1. The **job cap**: configured 200, effective 100 (C2's verdict).
2. The **task semaphore** `task.maxConcurrency`: configured 200, binary default 32, and no clamp at the binary's only
   setting-clamp site.
3. The **fleet seat gate**: default 200, live 85.

It states that only the job cap refuses spawns, and that a gate target above the effective cap is what produced the
whole-wave refusals recorded in 15+ sibling lessons. The routed line sends R1 to kumitate (its entry `:197` and the
missing job cap) and the two fleet-root items to the operator.

- **Why it is non-obvious:** C2's tool reports one key. Without this paragraph, a reader of mori's entry, of kumitate's
  `:197` or of the goal file still sees "200" three times and cannot tell which one binds. The kaidoku refusal record
  already shows that seats noticed the guard/job split, but no knowledge entry records it.
- **Risks:**
  - Scope creep. Adding `task.maxConcurrency` or the seat gate to the *tool* would change the frozen 21-case contract
    (`contract.md:87-89`) and must not happen this round.
  - Mori must not explain the job-manager mechanism. That is kumitate's ground (`mori PROVINCE.md:14`), so the paragraph
    cites the bytes and routes.
  - The semaphore "no clamp" statement covers only the `Math.min(N, X.get(Y))` shape; other enforcement forms are not
    excluded ([INFERENCE]).
- **Verification for L1:**
  - `LC_ALL=C rg -a -o -c 'Math\.min\(\s*\d+\s*,\s*[\w$]+\.get\([\w$]+\)\s*\)' ~/.local/bin/omp` should return 1.
  - `rg -n '^task:|maxConcurrency|^async:|maxJobs' ~/.omp/agent/config.yml` should show `:130,:131,:244,:245`.
  - `cat ~/.local/state/shokunin-hyaku/wave-cap` should print 85.
  - Re-run the section 1 `rg` to confirm there is still no sibling `maxJobs` or job-manager knowledge.

## Process notes

- Every read was read-only. I did not run `omp`, run `jj`, or perform any git write. Only this report was written.
- A read-only `find /home/vgpnk/Projects … -path '*/.omp/config.yml'` was auto-backgrounded by the shell wrapper after
  60 s. My `pkill -f` pattern did not match it. It ran to completion (wall time 244.75 s), and `pgrep` afterwards found
  nothing running. It found three project-level configs:
  - `ufo-fsd-alpha/.omp/config.yml:3`: `maxConcurrency: 0`.
  - `gamez/dbzmon/.omp/config.yml`: no `async`, `maxJobs` or `maxConcurrency` lines.
  - `gamez/dbzmon/.tower/worktrees/dbzmon-refine2/dzr2-rigs-posa/.omp/config.yml`: no such lines either.

  Neither `shokunin/` nor `mori-shokunin/` has a `.omp/config.yml`. C2's scope bound (one global
  config file, `contract.md:83`) is therefore not contradicted for this fleet.
- Tool installs and updates: none.
