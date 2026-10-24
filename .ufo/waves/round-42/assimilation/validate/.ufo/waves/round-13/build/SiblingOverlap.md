# Sibling Overlap & Two-Tier Handoff Synthesis: Mori, Tsukuroi, and Kumitate

**Member:** `MoriR13.SiblingOverlap`  
**Wave:** `mori-r13-build`  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Role:** UFO-FSD connector  
**Milestone:** round13 structured scopes and verdict integrity  
**Declared Axes:** `coverage` (score 6), `operability` (score 6)  
**Advisory Status:** Leaf connector proposal. Data only; never modifies contract, axes, or routes directly. Sole L1 integrates. No self-verification executed.

---

## 1. Declared Axes

1. **coverage**: Replace unstructured journal text scraping with MESSAGE-free structured `MESSAGE_ID` notice counts across independently labeled `user` and `system` scopes, establishing complete, non-overlapping boundary coverage with sibling domains.
2. **operability**: Repair long-history exact-authorship loss under SIGPIPE (`F01`) and enforce strict verdict-line validation (`F02`), providing deterministic, unforgeable handoff envelopes across sibling analysis boundaries without silent crash masking or ambiguous remediation orders.

---

## 2. Evidence & Sibling Province Map

All paths and citations below were read read-only from committed repository declarations and knowledge bases. No sibling files were mutated.

### 2.1 Tsukuroi (`tsukuroi-shokunin`) — OS Substrate, Package, Unit, and Boot Diagnosis
- **Province & Domain:** Host operability and system repair (繕). Owns read-only OS substrate probes: pacman state (`pacman -Qkk`), systemd user units & timers (`systemctl --user`), journal/boot triage (`journalctl -b`, dmesg), and driver/firmware plane.
  - *Refuses:* Endpoint/model serving health (→ `kama`), secrets (→ `kagi`), binary RE (→ `kaidoku`/`revenger`). Never installs, upgrades, or removes packages; never restarts services. Detection and report; the operator remediates.
  - *Citation:* `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:3-33`
- **OOM & Kill Knowledge:**
  - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:215-258,291-312,344-375`:
    - Distinguishes kernel OOM dumps (`journalctl -k -b -p err`) from teardown/SIGKILL waves without kernel records (`status=9/KILL`, `Failed with result 'signal'`).
    - Establishes that cgroup `memory.events oom_kill` behaves as a stored presence flag that outlives destroyed child subtrees only at ancestor slices (`user.slice`, `user-1000.slice`), not as a per-event meter.
    - Demonstrates that userspace killers (`systemd-oomd`, `earlyoom`) kill via `cgroup.kill`/`kill()` and do not increment kernel OOM counters.
  - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md:26-37,83-100,120-135`:
    - Analyzes event B (13:10:59): message #3 carrying `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` was teardown-coincident (0.45 ms after resource line), naming `user-1000.slice`, while the subject was inside the destroyed service cgroup.
    - Distinguishes subject unit (`UNIT` field set on PID 1 records) from sender unit (`_SYSTEMD_UNIT` field).
- **Adjacency Handoff Protocol & Route ADJ-04:**
  - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:35-74`:
    - Defines route `ADJ-04`: Host pressure or kill signal needing fleet/wave attribution, liveness or progress correlation → Next recipient: `mori`.
    - Minimum handoff evidence: UTC capture time, boot/time window, exact read-only counter or PSI command/exit, observed value.
    - Codifies the **5-stage closure lifecycle**: `prepared` → `reported` → `acknowledged` → `accepted` → `resolved`.
  - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:74-113`:
    - Executed observation packet `TSUKUROI-F1-MEM-01` (ADJ-04) captured at `2026-10-15T04:53:46Z`.
  - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/adjacency-recheck-2026-10-19.md:5-22,47,89-92`:
    - Notes that Mori responded in committed files (`PROVINCE.md:58-76`, `SCORECARD.md:614`, `LOG.md`), but Tsukuroi's ledger left `ADJ-04` at `prepared` because receipt sweep had no structured recipient receipt and integration was pending.

### 2.2 Kumitate (`kumitate-shokunin`) — Orchestration & Tooling
- **Province & Domain:** Orchestration and tooling. Scopes OMP task/hub, ufo-fsd scripts and runtime.
  - *Owns:* `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/` (S1–S8), `/home/vgpnk/Projects/ufo-fsd-alpha/crates/ufo-core-runtime/` and `ufo-cli/` (R1–R11), `~/.kimi-code/` (K1–K5).
  - *Refuses:* Anything outside this domain; reports cross-domain evidence back to orchestrator rather than absorbing it.
  - *Citation:* `/home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md:1-28`
- **Swarm Wave Lifecycle & Settlement:**
  - `/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:28-88,91-130`:
    - `scripts/ufo-swarm-wave.mjs` (1907 L): plan / run / record CLI. Hard ceiling 100 lanes. Roles: `scout`, `reviewer`, `critic`, `connector`, `sentinel`, `executor`, `mutation-tester`, `revenger`, `simplifier`, `scribe`.
    - **Crucial lifecycle contract:** There is **NO `settle` CLI verb** (`:28-36`). Earlier prose claiming `ufo-swarm-wave.mjs settle` was an erratum; `main` admits only `record` or `plan`/`run`.
    - `scripts/ufo-swarm-collect.mjs` (842 L): owns `collect`. Joins `ufo-swarm-results-v1`, `ufo-swarm-registry-v1`, and `ufo-swarm-wave-dispatch-v1` into `ufo-mission-result-v1`. Refusal tokens: `unmapped_member`, `unexpected_member`, `duplicate_member`.
  - `/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/failure-telemetry.md`:
    - Worker failure taxonomy: `rate_limit`, `usage_limit`, `model_unavailable`, `lane_timeout`, `process_exit`, `unavailable`, `quality_degraded`.

### 2.3 Mori (`mori-shokunin`) — Fleet & Host Observability (森)
- **Province & Core:** Fleet and host observability — whether the fleet, its waves, and its host are alive and progressing.
  - *Owns (read-only probes):* Watchdog liveness, wave settlement state (`SURFACE waves`), kill/OOM event classes (`SURFACE journal` and `SURFACE cgroup`), resource runway (`SURFACE disk`, memory PSI), lane silence grading (`SURFACE lane.<id>`).
  - *Refuses:* Dispatch and orchestration mechanism (→ `kumitate`); OS package, systemd unit, driver/firmware, and boot state (→ `tsukuroi`); endpoint and model-serving health (→ `kama`); credentials (→ `kagi`).
  - *Strict Rule:* **Detection and report only — never remediation.** (`PROVINCE.md:16`).
  - *Citation:* `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md:1-45,50-78`
- **Admission Bar & Quality Criteria:**
  - `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/QUALITY.md:27-36`:
    - Criterion 14: Counter semantics cite increment sites, not documentation wording.
    - Criterion 15: Journal class is counted by `MESSAGE_ID` or another trusted structured field, never by message text.
    - Criterion 16: Kill count names its unit (`kill` vs `notice`) and its journal scope; scopes are **never summed**.
    - Criterion 17: Detection recipe states which delivery paths it cannot see.
    - Criterion 18: Kill attribution comes from records written at event time, never from re-reading the victim's cgroup.
- **Round 13 Focus:**
  - `C1`: Replace text grep with MESSAGE-free structured `MESSAGE_ID` counts (`fe6faa94...`, `d989611b...`, `fc2e22bc...`) in independently labeled `user` and `system` scopes (`notice` units, never fleet-caused kill counts).
  - `C2`: Repair production long-history SIGPIPE authorship loss `F01` (`tools/mori-census.sh:1366-1374`) and reject invalid `BANANA`/mismatched verdicts in oracle `F02` (`tools/mori-silence-cases.sh:569-585`).

---

## 3. Contradictions & Structural Overlap

Tracing the interfaces between Mori, Tsukuroi, and Kumitate reveals three structural contradictions:

### Contradiction 1: The OOM Notice vs Kill Event Attribution Gap
- *The Gap:* Mori's census observes `fe6faa94...` notices in `journalctl --user` and `journalctl --system`. Historically, naive readers equated these notice counts with "fleet worker kills". Tsukuroi proved in `kill-event-deep-r8.md:97-100` that one kernel OOM kill produces multiple `fe6faa94...` notices across ancestor units and scopes, and teardown of a user manager also emits notices without a fresh kernel OOM.
- *The Contradiction:* If Mori increments an "OOM kill counter", it violates Quality Criteria 15 & 16 and contradicts Tsukuroi's OS diagnosis. If Mori silences the signal, fleet operators have no visibility into memory-pressure drops.
- *Resolution:* Mori must report strictly typed **`notice` units** labeled by scope (`scope=user` vs `scope=system`), cite the exact `MESSAGE_ID`, and provide them to Tsukuroi as an unmerged observation, never asserting fleet causation.

### Contradiction 2: Wave Settlement Actuation Fallacy
- *The Fallacy:* Early advisory proposals (`OwnerMap.md:29, 76-77`) suggested that when Mori flags `WAVE_UNSETTLED`, the remediation is to invoke `scripts/ufo-swarm-wave.mjs settle`.
- *The Reality:* Kumitate's canonical lifecycle contract (`swarm-wave-lifecycle.md:28-36`) proves that **no `settle` CLI verb exists**. Settlement is performed by `scripts/ufo-swarm-collect.mjs collect` joining `results.json` and `swarm-registry.json`. Invoking `settle` fails with usage error exit 64.
- *Resolution:* Mori's census must never advise running `ufo-swarm-wave.mjs settle`. It observes filesystem state only (`registry` present, `results` present/absent, age in seconds). Kumitate owns the collect join; Souji's receipts (`surfaces-r8.md:17-18; PROVINCE.md:76-77`) adjudicate whether an absent directory was `swept (pushed-receipt)` or `never-written`.

### Contradiction 3: Adjacency Handoff Lifecycle Asymmetry
- *The Asymmetry:* Tsukuroi tracks ADJ-04 handoffs via a formal 5-stage ledger (`prepared` → `reported` → `acknowledged` → `accepted` → `resolved`). Tsukuroi issued `TSUKUROI-F1-MEM-01`. Mori investigated the timestamp (`2026-10-15T04:53:46Z`), verified watchdog ticks and commits bookended it, and proved zero journal kill/notice records occurred (`PROVINCE.md:58-75`).
- *The Bottleneck:* Because Mori recorded this in narrative prose in `PROVINCE.md` rather than emitting a machine-verifiable, structured correlation receipt, Tsukuroi's recheck on 2026-10-19 found no sibling receipt matching its schema and kept ADJ-04 at `prepared`.
- *Resolution:* Mori needs a formal, typed **Adjacency Correlation Receipt** envelope that allows Tsukuroi's ledger to advance from `prepared` to `resolved` without Mori crossing into OS remediation.

---

## 4. The Proposed Move: Two-Tier Decoupled Handoff Protocol via Typed Adjacency Receipt Envelopes

We synthesize a **Two-Tier Decoupled Handoff Protocol** that preserves the non-overlapping province boundaries of Mori, Tsukuroi, and Kumitate, while eliminating handoff staleness and actuation errors.

### 4.1 Two-Tier Architecture Definition

```
  +-------------------------------------------------------------------------+
  | TIER 0: Observability & Scoped Metering (mori-shokunin)                 |
  | - Passive, read-only inspection of host surfaces & fleet filesystem.    |
  | - Emits MESSAGE-free structured MESSAGE_ID counts (notice units).       |
  | - Strictly refuses: remediation, OS state claims, dispatch actuation.   |
  +-----------------------------------+-------------------------------------+
                                      |
                     Emits Typed Observation Finding
                     & Adjacency Correlation Receipts
                                      |
                                      v
  +-------------------------------------------------------------------------+
  | TIER 1: Triage & Root-Cause Diagnosis (Domain Specialists)               |
  | - tsukuroi-shokunin: Host OS, cgroup hierarchy, systemd unit health,    |
  |                      kernel OOM vs userspace kill disambiguation.       |
  | - kumitate-shokunin: Wave dispatch state, member join reconciliation,  |
  |                      worker lifecycle, subagent timeout/retry.          |
  +-----------------------------------+-------------------------------------+
                                      |
                     Generates Structured Remediation
                     Proposal / Script Invocation
                                      |
                                      v
  +-------------------------------------------------------------------------+
  | TIER 2: Actuation Authority (Remediation Actors)                        |
  | - kumitate-shokunin: Invokes `scripts/ufo-swarm-collect.mjs collect`.   |
  | - operator: Privileged mutations (systemd restart, cgroup limits,       |
  |             pacman transactions, volume cleanup, driver reloads).       |
  +-------------------------------------------------------------------------+
```

### 4.2 Sibling Handoff Routing Matrix

| Finding / Surface | Tier 0 Mori Observation Shape | Tier 1 Triage Owner | Tier 2 Actuation Actor | Canonical Entrypoint & Remediation Rule |
|---|---|---|---|---|
| **OOM / Unit Kill Notice (`fe6faa94...`)** | `SURFACE journal: fe6faa94... scope=<user\|system> unit=<notice> boot=<BOOT_ID> count=<N>` (no MESSAGE text; scopes unmerged) | `tsukuroi` (OS/unit triage); `kumitate` if cgroup is fleet subagent | `operator` (unit config); `kumitate` (throttle concurrency) | Tsukuroi evaluates unit `MemoryMax` vs leak (`oom-event-plane.md:344-367`). Kumitate clamps `maxLanes` or agent context. Operator restarts service if degraded. |
| **Userspace OOM Notice (`d989611b...`)** | `SURFACE journal: d989611b... scope=<user\|system> unit=<notice> boot=<BOOT_ID> count=<N>` (systemd-oomd action) | `tsukuroi` | `operator` | Tsukuroi inspects `oomctl` / `user.oomd_ooms` xattrs. Inactive oomd remains `unavailable (inactive)`, never 0 (`userspace-oom-killers-r12.md:6-8`). |
| **Coredump Notice (`fc2e22bc...`)** | `SURFACE journal: fc2e22bc... scope=<user\|system> unit=<notice> boot=<BOOT_ID> count=<N>` (coredumpctl record) | `tsukuroi` | `operator` | Tsukuroi checks binary package provenance (`pacman -Qo`) and `coredumpctl info` (`oom-event-plane.md:92`). |
| **Cgroup Counter (`memory.events`)** | `SURFACE cgroup: path=<PATH> oom_kill=<N> basis=presence-flag anchor=<MTIME>` | `tsukuroi` | `operator` | Read as stored presence flag, not event count (`oom-kill-counter-kernel-only-r12.md:6-8; kill-event-deep-r8.md:120-135`). |
| **Unsettled Wave (`.ufo/waves/*`)** | `SURFACE waves: wave=<NAME> state=unsettled age_s=<N> has_registry=true has_results=false` | `kumitate` | `kumitate` | Kumitate runs `scripts/ufo-swarm-collect.mjs collect --wave <NAME> --results <RESULTS_PATH>` (`swarm-wave-lifecycle.md:91-130`). Never invoke non-existent `settle`. |
| **Empty Wave Directory** | `SURFACE waves: wave=<NAME> state=empty-by-removal receipt=<RECEIPT_HASH>` | `kumitate` / `souji` | None (closed) | Cross-checked against Souji's `pushed` receipts (`PROVINCE.md:76-77`). Distinguishes clean hygiene from `never-written`. |
| **Lane Silence (`lane.<id>`)** | `SURFACE lane.<id>: <silent\|progressing\|progressing-weak> basis=<ROW> other_commits=<N>` | `kumitate` | `operator` | Kumitate checks `ufo-sighting`. Operator prompts stuck lane. Governed by F01/F02 exact-author and verdict-line repair. |

### 4.3 Standardized Adjacency Correlation Receipt (Closing the ADJ-04 Loop)

To formally transition Tsukuroi's `TSUKUROI-F1-MEM-01` and future packets from `prepared` to `resolved`, Mori provides a machine-verifiable JSON schema for correlation responses:

```json
{
  "schema": "mori-adjacency-correlation-receipt-v1",
  "packet_id": "TSUKUROI-F1-MEM-01",
  "route": "ADJ-04",
  "capture_timestamp_utc": "2026-10-15T04:53:46Z",
  "recipient": "mori-shokunin",
  "lifecycle_state": "resolved",
  "fleet_correlation": {
    "watchdog_ticks_bookend": ["01:50:57-03:00", "01:58:27-03:00"],
    "fleet_commits_bookend": ["99efc52", "f2df270"],
    "overlapping_activity": "active-fleet-work"
  },
  "host_kill_correlation": {
    "kernel_oom_kills_in_window": 0,
    "systemd_fe6faa94_notices_in_window": 0,
    "systemd_d989611b_notices_in_window": 0,
    "cgroup_root_events": "absent"
  },
  "verdict": "correlation-only-no-kill-overlap",
  "provenance": {
    "tsukuroi_source": "tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:74-113",
    "mori_evidence": "mori-shokunin/PROVINCE.md:58-75"
  }
}
```

---

## 5. Trace Across Second-Order Surfaces

1. **Runtime Surface:**
   - Replacing text grep with structured `MESSAGE_ID` queries eliminates process piping into early-exit greps, preventing SIGPIPE 141 failures under `set -eo pipefail`.
   - Bounding queries to `--output-fields=MESSAGE_ID,_BOOT_ID` prevents large `MESSAGE` string allocations and eliminates potential regex denial-of-service or secret leakage in logs.
2. **Contract Surface:**
   - Preserves strict adherence to Quality Criteria 15 & 16: notice units, never fleet kill totals; scopes never summed.
   - Preserves Kumitate's contract: respects that `ufo-swarm-wave.mjs` has no `settle` CLI verb and directs settlement queries exclusively to `ufo-swarm-collect.mjs collect`.
3. **Substrate Surface:**
   - Respects cgroup v2 semantics: recognizes that `memory.events oom_kill` at ancestor slices is stored presence state that survives subtree destruction, avoiding false alerts on destroyed session subtrees.
   - Respects systemd catalog invariants: treats `MESSAGE_ID` as unit-level notification metadata, not per-process victim telemetry.
4. **Verification Surface:**
   - Unblocks Tsukuroi's cross-lane adjacency verification from `prepared` to `resolved`.
   - Enables isolated, deterministic testing in `tools/mori-round13-regressions.py` by checking that notice outputs carry strictly valid tokens and well-formed verdict lines consistent with rc0/1.

---

## 6. Risks & Bounded Falsifiers

1. **Spoofed or Unprivileged MESSAGE_ID Fields:**
   - *Risk:* An unprivileged process can write arbitrary `MESSAGE_ID` values to `journald` using `sd_journal_send()`.
   - *Boundary:* Kernel records (`_TRANSPORT=kernel`) and systemd user-manager records (`_TRANSPORT=journal` with `_PID=1` or `_UID=1000`) carry distinct provenance fields. Mori does not rely on `MESSAGE_ID` alone for victim attribution; event-time kernel summaries require `_TRANSPORT=kernel`.
2. **Journal Rotation and Retention Loss:**
   - *Risk:* Old notices or dumps may be vacuumed or rotated out of `/run/log/journal` or `/var/log/journal`.
   - *Boundary:* Zero notices in a historical window means zero *retained* notices, never proof that no event occurred. All negative claims must state the window and retention limit explicitly.
3. **Empty Wave Race Condition:**
   - *Risk:* A newly launched wave directory may momentarily contain only `spec.json` before `dispatch.json` and `swarm-registry.json` land.
   - *Boundary:* Mori grades wave age (`age_s`); waves younger than the launch threshold (e.g. <120s) remain in `draft` or `young` state, avoiding premature `WAVE_DISPATCH_ABSENT` alerts.

---

## 7. Verification Actions for L1

In accordance with godspeed leaf bounds, this agent performed no test execution or gate runs. The following checks are recommended for L1 integration:

1. **Adjacency Re-Read Check:**
   - Verify that all cited paths in `tsukuroi-shokunin` (`PROVINCE.md`, `oom-event-plane.md`, `kill-event-deep-r8.md`, `adjacency-handoffs-fleet-r1.md`) and `kumitate-shokunin` (`PROVINCE.md`, `swarm-wave-lifecycle.md`) resolve without ENOENT.
2. **C1 Structured Probe Check:**
   - Verify that `tools/mori-census.sh` emits structured `fe6faa94...`, `d989611b...`, and `fc2e22bc...` notice counts in independent `user` and `system` rows without raw `MESSAGE` text.
3. **F01 Pipe Safety Check:**
   - Verify that exact-author membership checks in `tools/mori-census.sh` use here-strings or variable capture instead of producer pipes into early-exit greps, preventing SIGPIPE 141 under pipefail.
4. **F02 Oracle Verdict Line Check:**
   - Verify that `tools/mori-silence-cases.sh` fails with exit 1 if a census output replaces `CLEAN`/`DRIFT` with `BANANA` or mismatched return codes.
5. **Handoff Envelope Format Check:**
   - Verify that correlation responses conforming to `mori-adjacency-correlation-receipt-v1` validate against JSON schema parsers without requiring external dependencies.
