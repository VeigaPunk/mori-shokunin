# CriticHarnessOverclaim — round 25 wave 2 (falsify), target `corpus/knowledge/harness-job-capacity-r25.md`

**Verdict: weakened.** The note's sourced core holds: the pinned bytes, the single clamp site, the count rule, the
three `atCapacity` hits and the host values all check out. But the Decision table and the Limits section claim more
for `RUNWAY_DEFAULT` and `RUNWAY_AS_CONFIGURED` than the tool's behaviour supports. One reproduced case is a false
number with exit 0: Bun reads `maxJobs: 50`, while the tool reports `RUNWAY_DEFAULT` and effective 100. Two
[UNKNOWN] items contradict each other and S104. One Limits sentence contradicts a Not-claimed item.

Scope: read-only on the lane. All code ran in a private clone of lane HEAD `07a31ae` at
`/fast/scratch/hyaku/mori-r25/w2-CriticHarnessOverclaim/lane`, which I removed afterwards. Upstream was a
`codeload` tarball of `45c35e40c46166dc726ccc52f5d27f40f2449f99`, and S104 was the GitHub `.patch` of `476b858`.
The installed binary was read as bytes only. omp was never run.

Tooling: nothing installed or updated. I used the pre-installed `bun` 1.4.3 at `~/.local/bin/bun` (the parser version
named in contract A2) only to call `Bun.YAML.parse` on scratch files.

## What held (checked, not assumed)

- The five upstream files I hashed match the note's sha256: job-manager.ts, sdk.ts, tools/bash.ts, tools/eval.ts and
  tools/settings.ts (`sha256sum` on the tarball). The hashes for docs/settings.md and docs/tools/eval.md were **not**
  checked.
- In non-test source, `atCapacity` has exactly 3 hits: `async/job-manager.ts:338`, `tools/bash.ts:1228` and
  `tools/eval.ts:536`. The Limits count of two consumers holds.
- There is one non-test `new AsyncJobManager`, at `sdk.ts:2283`. Every other construction is under `test/`, so U8's
  "15 unreachable" holds as labelled.
- `cfgAsyncMaxJobs` is used only at `sdk.ts:2284`, so the Not-claimed line "no effect above 100" is consistent.
- `job-manager.ts` throws only `Async job manager is disposed` (lines 361 and 459) and the limit message (line 371),
  so the Limits "upstream vocabulary" line holds for the manager.
- `protocolDefault: ["rpc"]` (`tools/settings.ts:943`; `config/registry.ts:104-108`) pins the default of 100 for RPC
  hosts unless the host configured a value itself. There is no contradiction with the effective cap of 100.
- The bash and eval auto-background branches check the cap and register synchronously, with no `await` in between
  (`tools/bash.ts:1223-1235` → `#startManagedBashJob` → `register` at line 882; `tools/eval.ts:536-563`). The
  claim "degrades and raises nothing" holds.
- The host facts match: `~/.omp/agent/config.yml:244-245` reads `async:` then `maxJobs: 200`; the state file
  `wave-cap` reads `85`; `wave1-attempts.json:10` shows `cap=85`; and there is no `~/.omp/agent/config.yaml`.
- A live read-only run printed configured `set 200`, clamp `found 100 sites 1`, default `found 100 sites 1`,
  effective 100, `RUNWAY_CLAMPED`, exit 1. The selftest printed `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`.

## Findings

### H1 (high): `RUNWAY_DEFAULT` can report a false number with exit 0; the Decision table's absent row and Limits do not say so

Target: Decision table row at line 203, and the Limits text at lines 229-231 ("Anchors, multi-line scalars and flow
mappings beyond the contracted inline-`async:` case are not modelled").

**Counterexample.** I ran each file below with
`python3 -I -B tools/mori-job-runway.py --config <file> --binary ~/.local/bin/omp`:

| File content | Tool output | `Bun.YAML.parse` (1.4.3) |
|---|---|---|
| `{async: {maxJobs: 50}}` | `configured absent`, effective 100, `RUNWAY_DEFAULT`, exit 0 | `{"async":{"maxJobs":50}}` |
| `{"async": {"maxJobs": 50}}` (JSON form) | `absent`, 100, `RUNWAY_DEFAULT`, exit 0 | `{"async":{"maxJobs":50}}` |
| `async:` then `  {maxJobs: 50}` | `absent`, 100, `RUNWAY_DEFAULT`, exit 0 | `{"async":{"maxJobs":50}}` |
| `async:` then `    x: 1` then `  maxJobs: 50` | `absent`, 100, `RUNWAY_DEFAULT`, exit 0 | `THROW SyntaxError: YAML Parse error: Unexpected token` |

omp loads settings with `YAML.parse`, and a parse failure returns `kind: "invalid"`
(`config/settings.ts:2041-2046`). So with this binary, the first three files configure 50 while the tool says 100
with exit 0. The fourth is a file omp does not load, which the tool reports as a clean default.

This contradicts the tool's own docstring (`tools/mori-job-runway.py:74-75`, "an abstention is always the safe
direction"). It also contradicts contract A2 (`contract.md:153-155`, "flow mappings that Bun reads stay abstentions:
`RUNWAY_UNKNOWN` is never a false number"). The tool abstains only on a flow value written inline on the `async:`
line (`tools/mori-job-runway.py:298-301`).

A second counterexample for the binary half: a 100-byte file that contains only the clamp text and the default text
(`decoy.bin`, not an omp build) gives clamp `found 100 sites 1`, effective 100, `RUNWAY_DEFAULT`, exit 0.

**What `RUNWAY_DEFAULT` actually proves.** In the file given, the line grammar found no direct, block-style `maxJobs`
child under a column-0 `async:`. In the binary, each byte pattern matched with one consistent number. `effective` is
the smaller of those two numbers. It does not show that the file lacks `async.maxJobs`, that omp can load the file,
or that the matched bytes are a live omp clamp.

The Limits wording also errs in the other direction. Multi-line quoted scalars, block scalars and aliases *are*
handled: the tool abstains on them. I checked `maxJobs: "5⏎  0"`, `maxJobs: |`, and `maxJobs: *x`; all three give
`malformed` and `RUNWAY_UNKNOWN`.

Impacted axes: coverage (C2 correctness) and the tool's safety claim.

**Smallest correction (note).** In row 203's "does NOT prove" cell, add: "That the file sets no `maxJobs`: a
block-style grammar does not see a top-level flow mapping, a JSON-form file or a `{maxJobs: …}` child line. These
read as `absent`, so the tool reports effective 100 while omp (Bun 1.4.3) reads the written value. That omp can load
the file: a mis-indented block also reads as `absent`."

Replace Limits lines 229-231 with: "Multi-line quoted scalars, block scalars, aliases, merge keys and complex keys make
it abstain (A2). Flow mappings are recognised only inline on the `async:` line. Elsewhere they read as `absent`, which
is a false `RUNWAY_DEFAULT`."

The tool itself still violates A2's "never a false number". That defect belongs to the tool owner and is outside this
seat.

### M1 (medium): the `RUNWAY_AS_CONFIGURED` row says "≤ 100", but 0 and negative values are `RUNWAY_CLAMPED`

Target: Decision table row at line 201, and the Clamped row at line 200 ("binary carries the clamp").

**Counterexample.** `maxJobs: 0` gives `set 0`, effective 1, `RUNWAY_CLAMPED`, exit 1. `maxJobs: -3` gives `set -3`,
effective 1, `RUNWAY_CLAMPED`, exit 1. The cause is `max(1, …)` at `tools/mori-job-runway.py:455` and the signed
`INTEGER_RE` at line 122. Bun reads 0 and -3 as given. So `RUNWAY_CLAMPED` is not only the clamp at 100; it is also
the floor at 1.

**Smallest correction.** Row 201: "set to a value from 1 to 100". Row 200's observable: "set above the clamp (e.g.
200), or below 1 (raised to the floor of 1)".

### M2 (medium): the foreground row claims the branch is entered "because the cap was reached"

Target: Decision table row at line 209.

**Counterexample.** The bash foreground fall-through runs when any one of five conditions holds (`tools/bash.ts:1223-1229`):

- bash auto-background is disabled;
- `pty` is set;
- a client terminal is available;
- there is no manager;
- `atCapacity`.

The eval fall-through has three conditions (`tools/eval.ts:536`): eval auto-background disabled, no manager, or
`atCapacity`.

Below the cap, an auto-background call with a wait threshold above 0 also runs "in the foreground". It is registered
as a job and holds a slot while the caller waits (`tools/bash.ts:1235-1243`, `foreground: !startBackgrounded`).
A foreground run therefore does not identify the cap branch, and a foreground-looking call may be counted.

**Smallest correction.** Replace "the branch is entered *because* the cap was reached" with: "the direct-foreground
branch is also entered when auto-background is off, a pty or client terminal is in use, or there is no manager
(bash.ts:1223-1229, eval.ts:536). Below the cap, a 'foreground' auto-background call is a registered job that holds a
slot."

### M3 (medium): "One seat is one task job", and "a task job is registered `queued: true`", are false as universals

Target: Limits line 232, and Decision table row at line 211. Line 232 also contradicts Not claimed line 299 ("No claim
that a seat, an agent, a task and a job are the same unit").

**Counterexample.** Only two non-test sites pass `queued: true`: `task/index.ts:1565` (the task-tool spawn) and
`task/workpool.ts:204` (the pool job). These `register("task", …)` callers pass no queued flag, so their jobs count
from registration:

- `eval/agent-bridge.ts:210` (`agent()`)
- `task/workpool.ts:363`
- `task/executor.ts:3272` (one wake job per follow-up turn of an existing subagent; `registerWakeJob`, called at
  lines 3325, 3343 and 3350)
- `task/restore.ts:85` (revived subagents)
- `vibe/runtime.ts:1370`
- `security/coordinator.ts:499`

One seat can therefore hold more than one `task` job over its life, and some `task` jobs count as soon as they are
registered.

**Smallest correction.** Line 232: "A task-tool spawn is one task job, registered queued (F5). Follow-up turns,
`agent()`, workpool batches and revived subagents register further `task` jobs that count from registration."
Row 211: "a task-*tool spawn* is registered `queued: true`…".

### M4 (medium): U1 says "only the default moved"; S104 shows more moved

Target: [UNKNOWN] U1, lines 259-262.

**Evidence (S104 `.patch`).**

- At `476b858` the cap is a static number computed once at construction: `asyncMaxJobs = Math.min(100, Math.max(1,
  settings.get("async.maxJobs") ?? 15))` passed as `maxRunningJobs: asyncMaxJobs` (patch lines 1016 and 1041), with
  `this.#maxRunningJobs = Math.max(1, Math.floor(options.maxRunningJobs ?? 15))` (line 165).
- At `45c35e40` the cap is a function that is re-read on every check (F3, F6). The floor moved into the manager's
  getter, after the `min`.
- The count changed from `this.getRunningJobs().length` (line 181), with no queued exclusion, to running-and-not-queued
  (F4).
- The job type union changed from `"bash" | "task"` (line 170) to include `eval`.
- The setting text "(1-100)" (line 470) is gone from `docs/settings.md:623`.

The claim "date from the feature's first commit" also rests on two endpoints only. Nothing between them was read, so
it is unlabelled inference.

**Smallest correction.** "At both `476b858` and `45c35e40` the ceiling is 100 and the floor is 1 ([INFERENCE]: the
commits between were not read). Since the feature commit, the default changed from 15 to 100, the cap became a
function re-read on every check, the count started excluding queued jobs, `eval` became a job type, and the settings
text lost '(1-100)'."

### M5 (medium): U6 and the last Not-claimed line contradict U1

Target: U6 at lines 275-276 ("Whether earlier … releases clamp at 100 was not checked"), and Not claimed line 303
("No claim about any omp version other than 18.12.6"). U1 states S104's code for the earlier commit `476b858`.

**Smallest correction.** U6: "Other releases were not checked, apart from the feature commit `476b858` read for U1
(S104)." Line 303: "…other than 18.12.6, apart from the S104 history in U1."

### M6 (medium): Limits treats a pattern miss as the only failure mode of the byte read

Target: Limits lines 226-228 ("a build that spells the same logic differently reads as `absent`"), and the
Decision-table rows that show `clamp {found, 100}` as the basis of `effective`.

**Counterexample.** The decoy file in H1 gives `found`, effective 100, with no omp code in it. A build that keeps the
matching text but caps elsewhere (for example a second limiter in the manager) would also read `found` with a number
that is not the live cap. Outside 18.12.6, the tool's `effective` is only the patterns' arithmetic. It never reads the
manager's getter.

**Smallest correction.** Append to the Limits bullet: "…and a `found` match is a byte pattern, not proof that the site
is live or is the only limiter. Off 18.12.6, `effective` is the patterns' arithmetic, not the manager's cap."

### L1 (low): the Decision-table header claims every "not proved" cell is forbidden by the sources

Target: lines 193-195 ("the 'not proved' column is what the sources above forbid"). Several cells rest on tool rules
or judgment, not on a source. Examples: "That 50 is a safe or tested number", "That 100 running jobs is a small
number", and H1/M1, which come from tool behaviour.

**Smallest correction.** "…is what the sources and the tool's rules do not support."

### L2 (low): Limits lists only two raisers when ten register sites do not pre-check

Target: Limits lines 241-242 ("The task spawn path and an explicit `async: true` bash call do not pre-check and do
raise it"). The source has 12 non-test `register(` sites. Only the two auto-background sites pre-check. The other ten
all reach the throw at the cap: `eval/agent-bridge.ts:210`, `eval/judgment-batch-bridge.ts:223`,
`modes/controllers/tan-command-controller.ts:144`, `security/coordinator.ts:499`, `task/executor.ts:3272`,
`task/index.ts:1407`, `task/restore.ts:85`, `task/workpool.ts:175`, `task/workpool.ts:363` and `tools/bash.ts:882`
(explicit async). F1 already quotes upstream for `agent()`.

**Smallest correction.** "Every other register caller (ten non-test sites, including `agent()`, `workpool()`, the task
spawn, subagent wake turns and explicit `async: true` bash) does not pre-check and does raise it."

### L3 (low): "not readable from outside the session" is stated as fact without a source

Target: Decision table row at line 200, Limits line 221, and U3 at lines 267-268. U3 sits under [UNKNOWN] but states a
universal fact. The only basis is the contract's scope bound (`contract.md:83-84`), which is a design decision, not a
source. I found no RPC job listing in `modes/rpc/`. But session files do record subagent turns that an outside reader
can scan: `task/restore.ts:55-78` rebuilds mid-turn subagents from them, and the fleet's `wave-live.py` estimates live
agents from the same directory (F11).

**Smallest correction.** "[INFERENCE] Not exposed by any interface in the sources opened, and this tool does not read
it. Session files allow an estimate of subagents, not the manager's running non-queued count."

### L4 (low): the Limits recheck list omits S112 and S113

Target: Limits line 219 ("re-open S098–S103"). The header's recheck line names S112–S113, which F9's bash/eval facts
depend on.

**Smallest correction.** "re-open S098–S103 and S112–S113".

### L5 (low): table enumerations are incomplete

- Row 207: "two clamp sites" should be "two or more"; the code counts every match (`tools/mori-job-runway.py:410-411`).
- Row 205's "(a different build, or a re-minified one)" omits an empty or truncated file. A zero-byte binary gives
  clamp `absent`, sha256 `e3b0c442…`, `RUNWAY_UNKNOWN`. It is not `unreadable`, and the sha256 is not null.
- The table has no row for config `unreadable`. A non-UTF-8 file (`\xff\xfe`) gives `configured unreadable`,
  `RUNWAY_UNKNOWN`, exit 2, a state the Scope paragraph names.
- Row 204 lists three `malformed` triggers. A2 adds about a dozen (tabs, document markers, merge and complex keys,
  BOM handling, block or quoted values, `#` without whitespace, multi-line quotes), as do non-integers.

**Smallest correction.** Change to "two or more"; add "or an empty file"; add one row for config `unreadable`; and in
row 204 write "…or any A2 abstention (contract `contract.md:137-155`)".

### L6 (low): Not claimed line 291 says "that session's count"

Target: line 291. Per F7, a child session borrows its root's manager, so the count is the root session tree's.

**Smallest correction.** "it means the count of running, non-queued jobs in that root session tree's manager had
reached its cap."

### Outside the four sections (reported because it is a direct contradiction): F10, line 157

F10's [INFERENCE] says the number of refused seats "(64, 66, 68, 88 in those records) exceeds 100 in some waves". None
of the four numbers exceeds 100. Also, 68 and 88 do not come from the two cited records (`GtLaneKasegi.md:48` gives 64;
`GtLaneKama.md:72` gives 66). 68 comes from `GtLaneChousa.md:61`, and 88 from the kagi lane
(`round-20/falsify/DeclaredVsDispatched.md:13`).

**Smallest correction.** "Every refused wave in these records (64, 66, 68, 88) is below 100, so each refusal shows the
count was already at the cap before the wave. Every attempt fails once the count is there."

## Checks the main agent should run

1. In a scratch directory, write a file containing `{async: {maxJobs: 50}}` and run
   `python3 -I -B tools/mori-job-runway.py --config <it> --binary ~/.local/bin/omp`. Expect `RUNWAY_DEFAULT`,
   effective 100, exit 0 (H1).
2. Run the same command with `async:` then `  maxJobs: 0`. Expect `RUNWAY_CLAMPED`, effective 1, exit 1 (M1).
3. Run `rg -n 'queued: true' packages/coding-agent/src` at `45c35e40`. Expect only `task/index.ts:1565` and
   `task/workpool.ts:204` (M3).

Not run: the hashes of docs/settings.md and docs/tools/eval.md; any omp session; the supplementary cases file.
