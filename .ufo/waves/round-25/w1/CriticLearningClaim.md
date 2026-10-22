# CriticLearningClaim — is C2 a learning claim in mori's PROVINCE core or frontier?

Seat: `MoriR25.CriticLearningClaim` (critic, leaf). Captured 2026-10-22T10:02Z.
Claim attacked: contract C2 (`.ufo/waves/round-25/contract.md:38-95`) as the round's learning claim under
the quality bar (`/home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md:145-149`).

## Verdict

**Fixable as written; not yet a strong learning claim.** C2 does add something mori does not know: no
committed mori file records the clamp mechanism. But the contract frames it as reading one constant, and
it states the after-value as a fixture self-test, so a judge can call it a regex plus `min()` that only
agrees with itself. Its real learning content is three facts the fleet is acting on wrongly or does not
record. The contract names none of them:

1. The documented setting contract leaves out the clamp. Upstream `docs/settings.md` at v18.12.6 says
   only "Running background-job cap, floored to at least 1". The fleet followed that text: the config
   sets 200, and the fleet's lane instruction names `async.maxJobs` as the limit.
2. There is one job pool per top-level session, and every descendant subagent inherits it.
3. Queued jobs do not count toward the cap.

The ownership boundary with kumitate is also unaddressed. The smallest safe corrections are listed under
"What makes C2 stronger within this round". None of them changes the frozen after-value.

## Q1 — Is a harness job cap inside mori's province?

**Partly, and only as a detection reading of a fleet capacity level. The mechanism itself belongs to kumitate.**

- **For.** Mori owns "whether the fleet, its waves and its host are alive and progressing"
  (`PROVINCE.md:3-4`). It also owns resource runway (`PROVINCE.md:10`) and wave settlement
  (`PROVINCE.md:23`). The job cap is the most frequently recorded reason fleet waves do not progress:
  - Mori's own admitted entry records waves "refused at the job cap"
    (`corpus/knowledge/wave-settlement-r20.md:64,75-76`).
  - The round-20 falsifier counted at least 13 waves that were refused and later spawned, and kama
    r19f, which was refused 66/66 and never spawned (`.ufo/waves/round-20/falsify/DeclaredVsDispatched.md:12,38`).
  - The pool is fleet-wide inside one process. The binary builds the manager only for a session with no
    `parentTaskPrefix`, and descendants take the parent's manager. Binary bytes at offset 164406734:
    `const Ui = !u.parentTaskPrefix ? new Xm({ maxRunningJobs: () => Math.min(100, XPe.get(R)) }) : undefined;`.
    At offset 164407676: `const Ao = Ui ?? u.asyncJobManager;`. The upstream source matches:
    [sdk.ts#L2282-L2284](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/sdk.ts#L2282-L2284)
    and [sdk.ts#L2315](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/sdk.ts#L2315).
    So the ceiling is shared by every lane, L1 and seat under one top-level session. That makes it a
    fleet runway quantity, not one agent's setting.
- **Against.** `PROVINCE.md:10` defines runway as "disk on the fleet root and `/tmp`, memory pressure",
  which are host resources. `PROVINCE.md:12` refuses "dispatch and orchestration mechanism (→ kumitate)".
  Kumitate's Frontier names "OMP harness contract (task batch, agent hub, agent discovery)"
  (`../kumitate-shokunin/PROVINCE.md`, Frontier band, first bullet). Its entry has a section
  "Dispatch, concurrency, and recursion" that already covers the sibling limit `task.maxConcurrency`
  (`../kumitate-shokunin/corpus/knowledge/omp-task-contract.md:68-86`). How `async.maxJobs` is computed
  and enforced is that same harness-contract ground.
- **Net.** A read-only reading of "the ceiling this host's harness enforces versus what the fleet
  believes" fits detection-and-report (`PROVINCE.md:17`). Owning the harness semantics would be a
  **duplicate authority** with kumitate. The contract says nothing about kumitate (`contract.md:38-95`
  has no adjacency line), and `PROVINCE.md` has no owned-scope extension for this. Round 24 did write
  one for pressure (`PROVINCE.md:274-278`).

## Q2 — Is it new ground or a repeat?

**It is new to mori as mechanism knowledge. It is not new to the fleet as an observation.**

- Search of `corpus/knowledge` for job, concurrency and seat-gate wording: the only job-cap mentions are
  refusal observations in `wave-settlement-r20.md:64,75-76`. The other hits are `--jobs 1` flags and
  unrelated concurrency (`audit-r11.md:120`, `structured-journal-scopes-r13.md:85`,
  `verdict-contract-r13.md:3,246`, `jj-branch-anchor-r17.md:72`). The words `maxJobs`,
  `maxRunningJobs` and "clamp" have 0 hits in any mori knowledge, PROVINCE, SKILL or SOURCES file
  outside round-25 files.
- The fleet already knows the number 100. Sibling lessons quote `Background job limit reached (100)`
  across at least 12 lanes, for example `../kama-shokunin/corpus/lessons/round-15-verifier-spotcheck.md:56`,
  `../tsukuroi-shokunin/corpus/lessons/round-24.md:53` and
  `../kumitate-shokunin/corpus/lessons/round-37-verifier-spotcheck.md:14`. The seat gate already acts on
  it: `scripts/hyaku/wave-slot.sh:6-7` quotes the refusal, and the live gate target is
  `~/.local/state/shokunin-hyaku/wave-cap` = `85`, below the effective 100.
- **The fleet holds a false belief, and nobody has recorded the mechanism.**
  `scripts/hyaku/lane-addendum.md:88-89` tells every lane that "the session's job and concurrency limits
  are `async.maxJobs` and `task.maxConcurrency` in `~/.omp/agent/config.yml`". That file sets
  `async.maxJobs: 200` (`~/.omp/agent/config.yml:244-245`), and the binary clamps the value to 100.
  `scripts/hyaku/await-capacity.sh:3` says the setting is "read once at process start". The binary
  instead re-evaluates `maxRunningJobs` on every capacity check (`get #R()` at offset 160032730), and
  upstream says settings reads are "memoized per scope"
  ([config-usage.md#L160](https://github.com/can1357/oh-my-pi/blob/v18.12.6/docs/config-usage.md#L160)).
  Whether a config edit takes effect live is therefore [INFERENCE] unsettled either way.
  The upstream docs omit the 100 ceiling
  ([docs/settings.md#L623](https://github.com/can1357/oh-my-pi/blob/v18.12.6/docs/settings.md#L623)).
  The source sets a library default of 15
  ([job-manager.ts#L43](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/async/job-manager.ts#L43))
  and a setting default of 100
  ([tools/settings.ts#L941-L946](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/tools/settings.ts#L941-L946)).
  A command search of the fleet for `Math.min(100|maxRunningJobs|maxJobs`, excluding round 25, finds
  only the two fleet-script lines above.
- **Repeat risk with the sentinel.** Round 23 C2 (quota, FR2, coverage), round 24 C2 (pressure, FR12,
  coverage) and round 25 C2 are all coverage claims under "resource runway" (`SCORECARD.md:1435,1502,1542`).
  The surfaces differ, so the "same axis+surface 3 rounds running" sentinel
  (`goal-20261022-hyaku-12h.md:173`) [INFERENCE] does not trip. Filing C2 under the FR3 or wave
  settlement hook below avoids the question altogether.

## Q3 — Would a tool that reads a constant from a binary be judged trivial?

**Yes, as framed now.**

- The declared after-value is fixture self-consistency: `PASS 21/21` over cases the author froze, with
  every expected field set by contract rules 1-5 (`contract.md:50-81,86-88`). The live host reading is
  "committed as evidence; it is not the after-value" (`contract.md:91-92`). The quality bar's capability
  route needs "a capability shown running and entered in SCORECARD's capability table"
  (`goal-20261022-hyaku-12h.md:147-148`). The contract names no capability row, and `SCORECARD.md:1542`
  declares only the self-test.
- The computation is a regex plus `max(1, min(clamp, base))`. All 21 frozen cases have a clamp of 100
  except J18, which has 300 (cases dump: `expect.clamp.value`). On this host the answer is a constant
  that the L1 had already found by hand (`contract.md:40-44`). A judge can ask what the tool knows that
  one `grep` does not.
- The regex is tied to minifier names (`XPe`, the arrow shape; `contract.md:61-62`). The next omp build
  can rename them and turn the reading `absent`, which gives `RUNWAY_UNKNOWN`. That is honest
  degradation, but it limits durability.
- **What makes it not trivial is the knowledge, not the regex.** Three binary-and-source facts change
  what the fleet should do, and none of them is in any committed fleet file:
  - The effective ceiling is 100 while the configured value is 200, and the instruction lanes follow
    names the config.
  - The pool is one per top-level session.
  - The cap counts only `status === "running" && !queued`
    ([job-manager.ts#L341-L345](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/async/job-manager.ts#L341-L345),
    [#L367-L372](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/async/job-manager.ts#L367-L372)).
    The docs line agrees: "parked/queued jobs do not consume execution slots".

## Strongest counterexamples

1. **A duplicate authority on capacity.** Three numbers coexist. The tool reports `effective` 100, the
   seat gate enforces target 85 from its state file (default 200, `wave-slot.sh:2,40`), and the lane
   addendum points at config value 200. C2 adds a fourth published ceiling and does not say which
   number an L1 should act on, or that the gate, not mori, is the dispatch authority. `PROVINCE.md:137`
   already says dispatch slot acquisition is kumitate/operator-owned.
2. **"Runway" is a level, not a ceiling.** Disk runway reports free space, not only size
   (`PROVINCE.md:26`). C2 reports only the ceiling and calls the live count unreadable "from outside
   the session" (`contract.md:84-85`). The fleet already estimates that count from outside the session:
   `scripts/hyaku/wave-live.py` (used by `wave-slot.sh:61-65`) and `await-capacity.sh:4-6`. Mori itself
   reads seat transcripts (`corpus/knowledge/seat-terminal-status-r17.md`, `PROVINCE.md:104-108`).
   "No authoritative count is readable" is defensible; "not readable" overstates it.
3. **The reading is not bound to the running process.** The tool reads the config and binary as they
   are now. A session started before an omp upgrade or a config edit enforces its own values, and reads
   are memoized (config-usage.md#L160). The contract's scope bounds name project overrides and the env
   (`contract.md:82-83`) but not process age. [INFERENCE] A mismatch would show only after a restart.

## What makes C2 stronger within this round

None of these items narrows or changes the frozen after-value. They are knowledge and evidence that
travel with C2.

1. **Make the knowledge entry the learning.** `corpus/knowledge/harness-job-capacity-r25.md`
   (`contract.md:90-92`) should state, with the tag-pinned anchors above and the binary offsets
   recorded as an own-work row:
   - the docs-versus-implementation gap: the 100 ceiling is undocumented and config 200 gives 100;
   - pool scope, one per top-level session and inherited by descendants;
   - the count rule: running and not queued, background bash jobs included;
   - the refusal text, and that a refused `register` spawns nothing (job-manager.ts#L370-L372);
   - the floor of 1 (job-manager.ts#L331-L334).
   This is "admitted knowledge on uncovered ground" in the goal's first sense, and it does not depend
   on whether the regex is judged trivial.
2. **Bind one live reading as committed evidence, not as the after-value.** Record the tool's JSON on
   this host with `binary_sha256` `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`,
   `configured` 200, `clamp` 100 over 1 site, `setting_default` 100, and `RUNWAY_CLAMPED` with exit 1.
   Add a SCORECARD capability row that points at it, which the quality bar's capability route needs.
3. **Route, don't absorb.** Add a kumitate adjacency line and an append-only owned-scope extension like
   round 24's (`PROVINCE.md:274-278`). Mori owns the read-only ceiling reading. Kumitate owns the
   harness semantics (`omp-task-contract.md:68-86`). The operator owns `lane-addendum.md:88-89`,
   `await-capacity.sh:3` and `wave-slot.sh`, and those are reported as stale beliefs, never edited.
   The SiblingOverlap and SeatGateRelation seats already in this wave (`w1/swarm-registry.json`) are
   where to carry this.
4. **Tie it to FR3 wave settlement.** In the knowledge entry, state that a member refused at this
   ceiling spawns nothing. That explains the declared-only members that
   `wave-settlement-r20.md:75-76` cannot tell apart, and it hooks C2 to an existing frontier row
   instead of a third consecutive runway coverage claim.
5. **Correct the scope sentence** at `contract.md:84-85` in the knowledge entry: no authoritative live
   count is readable; transcript estimates exist (`wave-live.py`) and stay frontier. Name process age
   and memoization as a limit.

## Impacted axes

- coverage: the claimed axis. It holds only with item 1 or 2 above.
- adjacency: at risk of a duplicate authority with kumitate and the seat gate until item 3 lands.
- depth: gains from item 1.
- calibration: the stale fleet beliefs in item 3 are reportable mismatches, not counted in C1.

## Bounds kept and tools

- Read-only throughout. The omp binary was read as bytes only, with `python3 -I -B` regex.
- Upstream was read through `gh api` at tag `v18.12.6` (`45c35e40c46166dc726ccc52f5d27f40f2449f99`).
- `~/.omp/agent/config.yml` was read only for its `async:` and `task:` lines. The seat-gate state file
  was read only.
- No omp, jj or git writes, no transcripts opened, no subagents, no background jobs.
- Tools used: gh 2.102.0, Python 3.14.8, rg 15.1.0, all pre-installed. No installs or updates.
