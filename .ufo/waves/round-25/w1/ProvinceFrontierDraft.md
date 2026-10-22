# ProvinceFrontierDraft — PROVINCE.md and corpus/README.md drafts for claim C2

Seat: `MoriR25.ProvinceFrontierDraft` (scribe; leaf, no subagents). Date: 2026-10-22.
Claim: C2, coverage axis — harness background-job capacity runway (new PROVINCE ground).
Contract: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-25/contract.md:38-91`.

**What this seat did.** It drafted, in this report only, (a) an appended `PROVINCE.md` section and
(b) an appended `corpus/README.md` section that registers a new frontier row **FR15 — Harness
background-job capacity runway**. It edited no product file: the two drafts below are text for the
L1 to land. It checked whether any existing FR1–FR14 row already covers the ground, and answers:
**no — FR15 is distinct from FR14 and from every other row**, with the reasoning in §3.

**Lane bounds observed.** No edit to `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`,
`corpus/knowledge/*`, `tools/*` or any skill file. No `jj` command at the fleet root; no `git`
write of any kind in the lane; no `omp` execution; no settings write; no pacman/uv/cargo/npm
transaction. Tool installs and updates: **none**.

---

## 1. Behavior the drafts must describe (verified facts, with anchors)

### 1.1 The cap itself

| Fact | Anchor |
|---|---|
| The installed harness binary is `/home/vgpnk/.local/bin/omp`, 256,702,432 bytes, `omp/18.12.6` | `stat -c '%s %n' ~/.local/bin/omp` → `256702432 /home/vgpnk/.local/bin/omp`; `omp --version` → `omp/18.12.6` (version string read only) |
| Binary sha256 `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4` | tool output `binary_sha256` (below); `corpus/SOURCES.md:108` (S102) |
| The clamp is compiled at the manager's construction site: `maxRunningJobs: () => Math.min(100, XPe.get(R))` — **one** match in the whole binary | byte 164,406,766 in `~/.local/bin/omp`; upstream `packages/coding-agent/src/sdk.ts:2282-2286` at tag `v18.12.6` = commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`; `corpus/SOURCES.md:105` (S099) |
| The setting is declared with `default: 100` and no maximum in the schema: `id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100` — **one** match in the binary | byte 155,231,590; upstream `packages/coding-agent/src/tools/settings.ts:941-946`; `corpus/SOURCES.md:106` (S100) |
| Effective cap = `max(1, floor(min(100, base)))`, resolved at check time (so a live setting can resize it) | upstream `packages/coding-agent/src/async/job-manager.ts:331-335`; `corpus/knowledge/harness-job-capacity-r25.md:61` (F3) |
| The count rule: `status === "running" && !job.queued`, **no type filter** (`bash \| task \| eval` share one runway) | `job-manager.ts:337-346` and `:363-370`; `job-manager.ts:48`; `corpus/knowledge/harness-job-capacity-r25.md:77` (F4) |
| The refusal text is upstream's: `Background job limit reached (${maxRunningJobs}). Wait for running jobs to finish or cancel one.` — the interpolated number is the **effective** cap, not the configured value | `job-manager.ts:371-373`; binary byte 160,033,359; `corpus/knowledge/harness-job-capacity-r25.md:98` (F6) |
| The upstream docs page states a default and a floor but **no maximum**; the ceiling "default and maximum 100" is stated in the eval-tool prose | `docs/settings.md:623`; `docs/tools/eval.md:258`; `corpus/SOURCES.md:107` (S101), `:109` (S103) |
| Only a top-level session constructs the manager (`!options.parentTaskPrefix`); children borrow the parent's | `sdk.ts:2282`, `:2315`, `:4789-4791`; `corpus/knowledge/harness-job-capacity-r25.md:110` (F7) |

### 1.2 This host

| Fact | Anchor |
|---|---|
| `~/.omp/agent/config.yml:244-245` is a column-0 `async:` block whose direct child is `maxJobs: 200` | `grep -n "^async:\|maxJobs" ~/.omp/agent/config.yml` → `244:async:` / `245:  maxJobs: 200` |
| No project-layer `.omp/config.yml` exists for this fleet root or this lane | `ls -a /home/vgpnk/Projects/shokunin/.omp` → only `agents/`; `/home/vgpnk/Projects/shokunin/mori-shokunin/.omp` → absent |
| The other settings layers that can carry the same key are real and unread by the tool: project layer (`<cwd>/.omp/`), `--config` / `PI_CONFIG_FILES` overlays, runtime overrides, plus agent-dir/profile relocation (`OMP_PROFILE`/`PI_PROFILE` → `~/.omp/profiles/<name>/agent`, `PI_CODING_AGENT_DIR`) | `.ufo/waves/round-25/w1/ConfigOverrideSurfaces.md:14,52,87,142,173`; upstream `packages/coding-agent/src/config/registry.ts:454-455` ("environment variable, runtime override, `--config` overlay, project, global, then the default") and `packages/utils/src/dirs.ts:120-134` |
| The seat gate measures a different population under a different number (gate target 85 on this host, default 200; harness cap 100) | `.ufo/waves/round-25/w1/SeatGateRelation.md:16-18,68-72`; `corpus/knowledge/harness-job-capacity-r25.md:161` (F11) |

### 1.3 Gates observed by this seat (read-only, lane tip `7bb0fe6`)

`python3 -I -B tools/mori-job-runway.py --selftest` → `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0.

`python3 -I -B tools/mori-job-runway.py` (live host run, no arguments) → exit 1:

```json
{
  "schema": "mori-job-runway-v1",
  "config_path": "/home/vgpnk/.omp/agent/config.yml",
  "binary_path": "/home/vgpnk/.local/bin/omp",
  "binary_sha256": "85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4",
  "configured": { "state": "set", "value": 200 },
  "clamp": { "state": "found", "value": 100, "sites": 1 },
  "setting_default": { "state": "found", "value": 100, "sites": 1 },
  "effective": 100,
  "verdict": "RUNWAY_CLAMPED"
}
```

`git cat-file -e 28b79d3d:tools/mori-job-runway.py` → exit 128 (the C2 **before**-value; the tool
is absent at the round-24 tip). The tool is landed at the lane tip: commits `09f55b6` ("land
tools/mori-job-runway.py (C2) after the frozen cases"), `9a3d511` (A2 abstention), `fbecc59`
(selftest hardening). The frozen 21 cases are at `tools/fixtures/mori-job-runway/cases.json`
(J01–J21; `mori-job-runway-cases-v1`), plus the co-evolved, not-counted
`tools/fixtures/mori-job-runway/supplementary-cases.json`.

**Admission state:** the tool is landed and green, but the non-author closure has not admitted C2
yet. Every draft below therefore says **pending admission**, exactly as round 24's pressure
advance did (`PROVINCE.md:236`, `corpus/README.md:445`).

---

## 2. Why this is new PROVINCE ground, not an extension of an existing Core row

Mori's Core list (`PROVINCE.md:20-28`) names: watchdog liveness, wave settlement, kill/OOM classes,
the same-boot journal window, resource runway (`SURFACE disk` / `SURFACE cgroup` — disk, write
average, memory PSI/fill/avail, scope high-watermark), tmux relevance, lane silence.

The C2 capability is a **fourth resource class**: the harness's own concurrency ceiling, derived
from a settings file and a compiled binary, with no journal, no cgroup, no disk and no transcript
in the read. It therefore does not extend "Resource runway" (`PROVINCE.md:26`) — that row is
explicitly scoped to `SURFACE disk` and `SURFACE cgroup`. It is a separate read-only probe with a
separate schema (`mori-job-runway-v1`), and like round 24's pressure probe it is **not** a census
surface: no `SURFACE` row, no census finding id, no DRIFT verdict, no baseline re-pin.

---

## 3. Is FR15 distinct from FR14 (and from every other FR1–FR14 row)?

**Answer: yes, distinct. FR15 is a new row; FR14 is not advanced by C2.**

The FR14 row is `corpus/README.md:345` / `PROVINCE.md:57`:

> FR14 — Agent-workload telemetry … Mori is consume-only; telemetry emission belongs to the
> emitting lanes and orchestration.

Its round-17 advance (`corpus/README.md:355`, `PROVINCE.md:103-107`,
`corpus/knowledge/seat-terminal-status-r17.md`) is a **passive transcript observation**: the last
parsed `type=message` record in a byte-bounded tail, classified into `completed / aborted /
error_unsettled / dead_quota / dead_rate_limit / dead_error_other / incomplete / unavailable`.

Three independent reasons FR15 ≠ FR14:

1. **Different subject.** FR14 observes *records about agent workloads* (transcripts, telemetry
   emitted by other lanes). FR15 observes *the harness's own compiled concurrency ceiling* — a
   number derived from `~/.omp/agent/config.yml` and the bytes of `~/.local/bin/omp`. C2 reads no
   transcript, no telemetry and no lane-emitted record at all.
2. **Different ownership posture.** FR14's boundary is exactly "mori is consume-only; telemetry
   emission belongs to the emitting lanes and orchestration" — i.e. FR14 is about *receiving*
   telemetry. FR15 is about a *capacity bound of the tool mori itself runs inside*, and the
   interesting part is the **mismatch**: the operator's configured 200 is clamped to 100 by the
   binary. A consume-only telemetry row cannot carry that.
3. **Different failure mode.** FR14's failure vocabulary is `dead_*`/`unavailable` for a seat. C2's
   is `RUNWAY_AS_CONFIGURED | RUNWAY_CLAMPED | RUNWAY_DEFAULT | RUNWAY_UNKNOWN` for a cap, with
   `RUNWAY_UNKNOWN`/exit 2 meaning "this tool cannot derive a number", never "no cap".

The other thirteen rows are further away still, and the closest of them is worth naming so the
integrator can say so out loud:

| Existing row | Why it is not FR15 |
|---|---|
| FR12 (event-driven pressure / PSI), FR6 (instantaneous disk write-rate) | Host resource rates and a *resident watcher*; C2 is a one-shot byte read of a compiled constant and a settings file. Same "how much can the host take" shape, different resource and different instrument class. |
| FR9 (durable fixture evidence) | About reproducing a fixture; C2 ships a frozen 21-case fixture but the frontier row is about the fixture's durability, not about the cap. |
| FR3 / FR4 | Wave settlement and driver-state reconciliation; unrelated to harness capacity. |
| FR8 (alert-threshold calibration) | About the calibration of *mori's own* alert thresholds. C2 measures a threshold that belongs to the harness and the operator, so it is deliberately **not** a calibration claim and FR8 is untouched. |
| FR13 (eBPF tracing), FR1/FR2/FR5/FR7/FR10/FR11 | No overlap. |

**Consequence for the drafts:** FR15 is added as a **new** row; FR1–FR14 stay byte-unchanged; the
FR14 row is neither edited nor cited as advanced. Round-17's own connector reached the same
conclusion for a different new ground and the same insertion mechanic
(`.ufo/waves/round-17/build/ProvinceFrontier.md:60,66`).

**One adjacency to record (not an ownership claim):** the *mechanism* behind the clamp — what the
job manager counts, why 100, what fills a runway — is kumitate's ground
(`kumitate-shokunin/PROVINCE.md:3,19`; its OMP contract entry `…/omp-task-contract.md` has no
`async.maxJobs` row and its `:197` still says the effective live OMP setting is UNKNOWN). Mori
cites the bytes as a source and reports the read; it does not own the analysis. Writing harness
configuration is operator-owned. This is why the drafts carry an Adjacent bullet.

---

## 4. DRAFT A — appended `PROVINCE.md` section

**Placement.** Appended at the end of the file, after the round-24 section (`PROVINCE.md:234-290`).
Nothing above the append is touched: the Core bullet list (`PROVINCE.md:20-28`), the Frontier rows
(`PROVINCE.md:42-57`), the Adjacent table (`PROVINCE.md:59-90`) and the Owns header
(`PROVINCE.md:6-10`) stay byte-for-byte unchanged, so no sibling line-range pointer into
`PROVINCE.md:3-16` or `:42-57` moves — the same reason round 24 recorded an "Owns-scope extension
(append-only)" bullet (`PROVINCE.md:274-278`) instead of rewriting the header.

```markdown
## Round-25 appended scope notes (2026-10-22)

- **Core, harness background-job capacity runway read (new FR15 advance, admission pending):**
  `tools/mori-job-runway.py` (round-25 build) reads two byte sources and reports one JSON object
  (`schema: mori-job-runway-v1`): the **configured** `async.maxJobs` from one settings file
  (`--config`, default `~/.omp/agent/config.yml`), the **clamp** compiled into the installed
  harness binary (`--binary`, default the real path of `omp` on `PATH`) located by pattern over
  its bytes, and the **setting default** from the binary's own settings table. It then reports
  `effective = max(1, min(clamp, base))` — where `base` is the configured value, or the schema
  default when the file does not carry the key — with the verdicts
  `RUNWAY_AS_CONFIGURED | RUNWAY_CLAMPED | RUNWAY_DEFAULT | RUNWAY_UNKNOWN` (exit 0 / 1 / 0 / 2).
  On this host the read is configured 200, clamp 100 (one site), setting default 100 (one site),
  effective 100, verdict `RUNWAY_CLAMPED`, exit 1: the operator's configured value is **clamped
  by the binary**, not honoured. The clamp lives at the manager's construction site
  (`maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))`), so the ceiling is a
  property of the shipped harness, not of the configuration file.
  **The read is a cap, never a count.** The tool reads no job list and cannot read the number of
  running jobs from outside a session; an effective value is not evidence that any job ran, that
  the runway was free, or that a session is near its cap. `RUNWAY_UNKNOWN` (exit 2) means *this
  tool cannot derive a number from the bytes it was pointed at* — a malformed value, a missing
  clamp pattern, an unreadable binary, or two clamp sites with different numbers — and never
  means "unlimited", "zero" or "no clamp": an absent match is a failed lookup.
  Read-only: it opens one file and one binary for reading, never runs `omp`, never writes a
  settings file and never touches another configuration surface. It is **not** a census surface:
  no `SURFACE` row, no census finding id, no DRIFT verdict, no baseline re-pin.
  Knowledge: `corpus/knowledge/harness-job-capacity-r25.md` (lands with this round); the upstream
  sources opened this round are S098–S103 and S112–S113 (`corpus/SOURCES.md:104-109,118-119`),
  all at oh-my-pi tag `v18.12.6` (commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`), plus the
  installed binary as an own-work row (S102).
- **FR15 — Harness background-job capacity runway** (new row; FR1–FR14 are unchanged and FR14 is
  **not** advanced). First evidence: `corpus/knowledge/harness-job-capacity-r25.md:33-190`;
  `corpus/SOURCES.md:104-109,118-119`. Boundary: the read reports the cap the harness would
  compute from the file and the binary it is pointed at. **Still frontier:** the live count of
  running non-queued jobs in any session (not readable from outside that session); the scope in
  which a counted population lives — one manager per root session tree, children borrowing their
  parent's, so the same *number* applies to every manager while the *population* is per tree, and
  a refusal cannot be attributed to a session from outside it; and every settings layer the tool
  does not read — the project layer (`<cwd>/.omp/`), `--config` / `PI_CONFIG_FILES` overlays,
  runtime overrides, and agent-dir relocation by `OMP_PROFILE`/`PI_PROFILE` or
  `PI_CODING_AGENT_DIR`. The tool reads one file; the runtime resolves a stack, so `configured` is
  that file's value and `effective` is the cap that *would* apply if it were the effective one.
  Also frontier: why the ceiling is 100, what filled a runway when a refusal appeared, and any
  behaviour of other harness versions.
- **Adjacent (kumitate owns the harness mechanism; the operator owns the configuration):** the
  semantics behind the clamp — what the job manager counts (`running` and not `queued`, every job
  type, so a background shell job and a subagent task share one runway), the exact refusal text,
  and the fact that only a top-level session builds the manager — are kumitate's OMP task/hub
  ground (`../kumitate-shokunin/PROVINCE.md:3,19`; its OMP contract entry still has no
  `async.maxJobs` row and still records the effective live OMP setting as UNKNOWN). Mori's part
  is the bounded read and the report of it; it does not own the mechanism, proposes no change to
  `async.maxJobs` or to any settings file, and does not judge the fleet seat gate, which counts a
  different population under a different number (85 on this host, default 200; the harness cap is
  100). Changing harness configuration is operator-owned.
- **Owns-scope extension (append-only; `PROVINCE.md:6-10` is left byte-unchanged):** the Core
  bullet above extends the owned read-only probe list named at `PROVINCE.md:6-10` with a fourth
  resource class — the harness's own background-job concurrency ceiling. The header sentence
  itself is not rewritten by this round; the extension is recorded here so no sibling line-range
  pointer into `PROVINCE.md:3-16` moves.
- **Admission state (2026-10-22):** the tool and its twenty-one frozen cases are landed
  (`tools/mori-job-runway.py`, `tools/fixtures/mori-job-runway/cases.json`); the declared
  after-value command prints `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` (exit 0) and one live host
  run returned `RUNWAY_CLAMPED` with effective 100, exit 1. The Core bullet above is **pending
  admission** by the non-author closure. No frontier row is closed, no other lane's surface is
  claimed, and no remediation is added.
```

---

## 5. DRAFT B — appended `corpus/README.md` section

**Placement.** Appended at the end of the file, after the round-24 Frontier note
(`corpus/README.md:451-482`). The `## Frontier` table (`corpus/README.md:328-345`) and its FR1–FR14
rows are left byte-unchanged, and the closing policy at `corpus/README.md:349` ("Open items now
live in `## Frontier`; the historical list above is unchanged") is not edited.

```markdown
## Round-25 coverage additions — C2 harness background-job capacity runway (admission pending)

| Ground | Entry | Bounded advance |
|---|---|---|
| Harness background-job capacity runway (new FR15) | `knowledge/harness-job-capacity-r25.md` | One JSON object (`schema: mori-job-runway-v1`) naming the **configured** `async.maxJobs` read from one settings file (default `~/.omp/agent/config.yml`), the **clamp** compiled into the installed harness binary (default the real path of `omp` on `PATH`), and the **setting default** from that binary's settings table, with `effective = max(1, min(clamp, base))` and the verdicts `RUNWAY_AS_CONFIGURED` / `RUNWAY_CLAMPED` / `RUNWAY_DEFAULT` / `RUNWAY_UNKNOWN` (exit 0 / 1 / 0 / 2). On this host: configured 200, clamp 100 at one site, default 100 at one site, effective 100, `RUNWAY_CLAMPED` — the configured value is clamped by the binary, not honoured. The read is a cap, never a count: no job list is read, and the live running-job count is not readable from outside a session. `RUNWAY_UNKNOWN` means this tool cannot derive a number from the bytes it was pointed at, never "unlimited" or "no clamp". Read-only: one file and one binary, no `omp` run, no settings write, no other configuration surface. Not a census surface: no `SURFACE` row, no finding id, no DRIFT verdict, no baseline re-pin. Sources S098–S103 and S112–S113 (`SOURCES.md:104-109,118-119`), all at oh-my-pi tag `v18.12.6`. |

## Round-25 Frontier note — FR15 added, no existing row closed

The FR1–FR14 rows above (`corpus/README.md:332-345`) and their PROVINCE counterparts
(`PROVINCE.md:44-57`) are byte-unchanged by this round. This appended note registers the new
frontier row and records what it does and does not cover.

- **FR15 — Harness background-job capacity runway.** First evidence:
  `knowledge/harness-job-capacity-r25.md:33-190`; `SOURCES.md:104-109,118-119`. Boundary: the
  bounded Core advance above reads the cap the harness would compute from one settings file and
  the installed binary's bytes. **Still frontier:** the live running-job count in any session
  (not readable from outside that session); the scope of the counted population — one manager per
  root session tree, children borrowing their parent's, so the same number applies to every
  manager while the population is per tree, and a refusal cannot be attributed to a session from
  outside it; and every settings layer the tool does not read — the project layer (`<cwd>/.omp/`),
  `--config` / `PI_CONFIG_FILES` overlays, runtime overrides, and agent-dir relocation by
  `OMP_PROFILE`/`PI_PROFILE` or `PI_CODING_AGENT_DIR`. The tool reads one file while the runtime
  resolves a stack, so `configured` is that file's value and `effective` is the cap that would
  apply if it were the effective one. Also frontier: why the ceiling is 100, what filled a runway
  when a refusal appeared, and any behaviour of other harness versions.
- **FR15 is distinct from FR14.** FR14 is agent-workload telemetry: mori is consume-only and the
  emission belongs to the emitting lanes and orchestration; its round-17 advance is a passive
  transcript terminal-at-scan observation (`knowledge/seat-terminal-status-r17.md`). FR15 reads no
  transcript, no telemetry and no lane-emitted record: it reads a settings file and a compiled
  binary to state the harness's own concurrency ceiling, and its interesting content is the
  mismatch between an operator's configured value and the binary's clamp. FR14 is not advanced,
  narrowed or closed by C2, and no other FR1–FR14 row covers this ground.
- **Adjacent, not absorbed:** the mechanism behind the clamp is kumitate's OMP task/hub ground;
  writing harness configuration is operator-owned; mori reports the read and changes nothing.
  The fleet seat gate counts a different population under a different number and is not judged
  here.

No frontier row is closed by this round, and no quota, retention, wave-settlement or telemetry
ground is touched.
```

### 5.1 The same FR15 row in the `## Frontier` table's own four-column shape

For the integrator who prefers one physical table (round 17's connector took this route,
`.ufo/waves/round-17/build/ProvinceFrontier.md:66`), the row to insert **after**
`corpus/README.md:345` (FR14) is:

```markdown
| FR15 | Harness background-job capacity runway | `knowledge/harness-job-capacity-r25.md:33-190`; `SOURCES.md:104-109,118-119` | The bounded Core advance reads the cap the harness would compute from one settings file and the installed binary's bytes (configured vs clamp vs setting default, `effective = max(1, min(clamp, base))`). Still frontier: the live running-job count in any session (not readable from outside it); the scope of the counted population (one manager per root session tree, children borrowing their parent's — a refusal cannot be attributed to a session from outside it); and every settings layer the tool does not read (project layer `<cwd>/.omp/`, `--config`/`PI_CONFIG_FILES` overlays, runtime overrides, agent-dir relocation by `OMP_PROFILE`/`PI_PROFILE` or `PI_CODING_AGENT_DIR`). The tool reads one file while the runtime resolves a stack. A cap is never a count; `RUNWAY_UNKNOWN` is a failed lookup, never "unlimited" or "no clamp". Distinct from FR14 (agent-workload telemetry), which is not advanced here. |
```

**L1 decision requested (one, small):** land §5 only (append-only, zero edits to existing rows), or
land §5 **and** insert the row above into the `## Frontier` table after `corpus/README.md:345` and
the matching bullet after `PROVINCE.md:57`. Both keep FR1–FR14 byte-unchanged; only the second adds
a line to an existing table. My recommendation: land §5 and the table insert together, so the
table and the appended note do not drift, and keep the table's FR1–FR14 rows untouched.

---

## 6. Findings and risks for the L1

1. **The "200" in the config is a trap for readers.** Three different 200s exist on this host —
   `async.maxJobs: 200` (configured, clamped to 100), `task.maxConcurrency: 200` (a different
   setting, binary default 32, and **no** clamp of the `Math.min(N, X.get(Y))` shape), and the
   seat gate's default target 200 (live 85). Any note that says "the cap is 200" is wrong. The
   drafts above always pair "configured" with "effective" and never use a bare 200. This is the
   same point the sibling-overlap seat routed to kumitate
   (`.ufo/waves/round-25/w1/SiblingOverlap.md`, route R1) and that kumitate's own entry still
   records as UNKNOWN (`kumitate-shokunin/corpus/knowledge/omp-task-contract.md:197`).
2. **Do not let FR15 become a threshold-calibration claim (FR8).** The 100 is a shipped upstream
   fact, not a measured or calibrated threshold, and the drafts say so by naming the source
   rather than by asserting a policy. FR8 stays open and untouched.
3. **`RUNWAY_CLAMPED` with exit 1 is a correct measurement, not a tool failure.** The after-value
   command in the contract is the **selftest** (`PASS 21/21`, exit 0); the live host run exits 1
   by design because this host's configured value is clamped. Do not let the live exit code be
   read as a failed check.
4. **The tool's `configured` value is one file, not the effective settings value.** The drafts
   carry this as an explicit limit and keep it in FR15's boundary. If a future round reads the
   project layer or the overlays, that is a new capability, not a widening of this one.
5. **One cap, one version.** Every statement is bound to omp/oh-my-pi 18.12.6 (tag `v18.12.6`,
   commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`) and to the installed binary's sha256
   `85d9daf3…ccfa4`. A different build may clamp elsewhere; re-open S098–S103 and S112–S113 and
   re-read the binary on a release. The drafts say "lands with this round" for the knowledge entry
   rather than implying it is already admitted.
6. **Sibling overlap is settled, and it is a routing item, not a conflict.** No sibling lane
   covers the cap; every sibling hit is a refusal record quoting `Background job limit reached
   (100)`. The mechanism is kumitate's; the configuration write is the operator's; mori's read
   duplicates none of it (`.ufo/waves/round-25/w1/SiblingOverlap.md`).
7. **Naming.** "Harness background-job capacity runway" is close to the existing Core phrase
   "Resource runway" (`PROVINCE.md:26`). The drafts disambiguate in prose ("a fourth resource
   class — the harness's own concurrency ceiling") rather than by renaming an existing row.

---

## 7. Touched surfaces

| Path | Change by this seat |
|---|---|
| `.ufo/waves/round-25/w1/ProvinceFrontierDraft.md` | **created** — this report only |
| `PROVINCE.md` | none (draft text in §4 for the L1) |
| `corpus/README.md` | none (draft text in §5 for the L1) |
| `corpus/knowledge/harness-job-capacity-r25.md` | none (read) |
| `corpus/SOURCES.md` | none (read) |
| `tools/mori-job-runway.py`, `tools/fixtures/mori-job-runway/*` | none (read; ran the landed tool read-only) |
| `~/.omp/agent/config.yml`, `~/.local/bin/omp` | none (read only; no settings write, no `omp` run) |
| sibling lane repos, fleet root, `~/.omp` transcripts | none (read-only greps only) |

## 8. Out of scope for this seat

Product-code edits; the `PROVINCE.md` / `corpus/README.md` landings themselves (L1's);
`corpus/SOURCES.md` row creation (registry seat's); the `SKILL.md` error-pattern block (another
seat's); the knowledge entry's own text (already landed by the L1); any adjudication of the
harness mechanism, of the seat gate, or of the refusal records; any `omp` execution, settings
write, job start/cancel, or gate change.

## 9. Artifact paths

- This report: `.ufo/waves/round-25/w1/ProvinceFrontierDraft.md`
- Contract: `.ufo/waves/round-25/contract.md:38-91`
- Knowledge entry: `corpus/knowledge/harness-job-capacity-r25.md` (Scope `:8`, Facts `:28`,
  F1 `:33`, F2 `:53`, F3 `:61`, F4 `:77`, F6 `:98`, F7 `:110`, F11 `:161`, F12 `:176`, F13 `:182`,
  Decision table `:192`, Limits `:214`, [UNKNOWN] `:256` — U2 `:264`, U3 `:267`, U4 `:269`,
  U7 `:277`, Not claimed `:289`)
- Sources: `corpus/SOURCES.md:104-109` (S098–S103), `:118-119` (S112–S113)
- Tool and fixtures: `tools/mori-job-runway.py`,
  `tools/fixtures/mori-job-runway/cases.json`, `tools/fixtures/mori-job-runway/supplementary-cases.json`
- Sibling reports this draft relies on: `.ufo/waves/round-25/w1/SiblingOverlap.md`,
  `.ufo/waves/round-25/w1/ConfigOverrideSurfaces.md`, `.ufo/waves/round-25/w1/SeatGateRelation.md`
- Round-17 precedent for a new frontier row: `.ufo/waves/round-17/build/ProvinceFrontier.md:60,66,96-98`
- Upstream ref: `https://github.com/can1357/oh-my-pi` tag `v18.12.6`, commit
  `45c35e40c46166dc726ccc52f5d27f40f2449f99`; raw files
  `packages/coding-agent/src/async/job-manager.ts` (sha256 `0f37afaa…4e7`),
  `packages/coding-agent/src/sdk.ts` (`c0228add…957`),
  `packages/coding-agent/src/tools/settings.ts` (`51497414…507`),
  `packages/coding-agent/src/config/registry.ts` (`757ff479…25`),
  `packages/utils/src/dirs.ts` (`2d423f4f…24`)
- Tool installs and updates: **none**.
