# SiblingBoundary — Two-Tier Ownership Architecture for Out-of-Scope Unit Triage Routing

**Member:** `MoriR14.SiblingBoundary`  
**Wave:** `mori-r14-repair`  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Role:** UFO-FSD connector  
**Milestone:** Restore OOM alarm and structured fleet routing (Round 14 C1 coverage repair)  
**Judged Axis:** `coverage` (primary); directly impacted: `adjacency`, `operability`, `calibration`  
**Advisory Status:** Leaf connector proposal aligned with L1 final ruling and `.ufo/waves/round-14/scoped-counter-contract.json`. Data only; never modifies contract, axes, or routes directly. Sole L1 integrates. No self-verification executed.

---

## 1. Name the Axes

1. **coverage** (owned by lane, LIVE — primary judged axis):
   - Repair Round 13's `rejected-harmed` journal cutover by restoring structured fleet versus non-fleet failure partitioning (`UNIT_FAILURE_JOURNAL` vs `UNIT_FAILURE_OUT_OF_SCOPE`) and critical OOM alerting (`OOM_KILL_JOURNAL crit` => `DRIFT`), while retaining all six scoped counters across independent `journal.user` and `journal.system` surfaces without cross-scope summation or raw `MESSAGE` parsing.
2. **adjacency** (observed axis — directly repaired):
   - Eliminate cross-domain bleed and ambiguity. Mori performs read-only detection and reporting only—**never remediation** (`PROVINCE.md:16`). Explicitly formalize two-tier ownership for out-of-scope failed units: routing diagnostic triage to domain specialists (`tsukuroi` for OS/desktop services, `kama` for endpoint serving, `kumitate` for orchestration) while reserving actuation authority strictly to the `operator`. No extra triage runtime architecture is required.
3. **operability** (owned by lane, LIVE):
   - Ensure census execution is deterministic, fail-safe, and free of early-exit pipe crashes. Provide rigorous tri-state classification (fleet, non-fleet, unattributed) where missing, malformed, or ambiguous subject metadata emits explicit `UNIT_FAILURE_UNATTRIBUTED_JOURNAL info` with `owner=unresolved`, preventing false non-fleet routing or silent suppression.
4. **calibration** (observed axis):
   - Match finding severities strictly to operational reality and historical contracts, citing `.ufo/waves/round-14/scoped-counter-contract.json` (`l1_interface_ruling`):
     - `OOM_KILL_JOURNAL crit` => `DRIFT`: exactly one alarm per census, carrying the four separate counters `user_notice`/`system_notice`/`user_unit_oom`/`system_unit_oom` (never summed, per `l1_interface_ruling.oom`).
     - `KILL_SIGNAL_JOURNAL warn` => `DRIFT` for user-process SIGKILLs.
     - `UNIT_FAILURE_JOURNAL info`: generic fleet failure is `info`, strictly matching frozen r12 `:904–908` and `l1_interface_ruling.generic_unit_failure_severity`.
     - `UNIT_FAILURE_OUT_OF_SCOPE info`: retains `CLEAN` roll for non-fleet out-of-scope failures with `owner=tsukuroi`.
     - `UNIT_FAILURE_UNATTRIBUTED_JOURNAL info` with `owner=unresolved reason=subject-metadata-unknown` per `l1_interface_ruling.unknown_subject`.
5. **depth** & **freshness** (observed axes):
   - Ground routing semantics in upstream systemd emitter code (S036 `unit.c`), catalog definitions (S035), field specifications (S015 `systemd.journal-fields(7)`), and the authoritative contract `.ufo/waves/round-14/scoped-counter-contract.json`.

---

## 2. Ground Evidence & Sibling Province Audit

All paths and citations below were read read-only from local repository declarations and committed knowledge bases. No sibling files were mutated.

### 2.1 Tsukuroi (`tsukuroi-shokunin`) — OS Substrate, Package State, and Systemd Unit Diagnosis
- **Province Scope (`tsukuroi-shokunin/PROVINCE.md:1-33`):**
  - *Domain:* Host operability & system repair (繕, mending) — OS substrate: package state (`pacman -Qkk`), systemd user units & timers (`systemctl --user`, unit files, failed states), journal/boot triage (`journalctl -b`, dmesg error classes), driver/firmware plane.
  - *Refusals:* Endpoint/model serving health (→ `kama`), secrets (→ `kagi`), binary RE of drivers (→ `kaidoku`/`revenger`).
  - *The Remediation Prohibition (`PROVINCE.md:28`):*
    > *"Never installs, upgrades, or removes packages; never restarts services. Detection and report; the operator remediates."*
- **Adjacency & Finding-to-Owner Handoffs (`PROVINCE.md:35-70`):**
  - *The Ownership Contract (`PROVINCE.md:38-40`):*
    > *"A recipient is an analysis/report owner, **not permission to repair**. Tsukuroi retains the OS finding. No row authorizes configuration writes, service changes, credential reads, endpoint requests, or target execution."*
  - Tsukuroi defines seven shared-work classes (ADJ-01 to ADJ-07) and codifies a strict **5-stage closure lifecycle**: `prepared` → `reported` → `acknowledged` → `accepted` → `resolved`.
  - Route `ADJ-04` routes host memory/kill correlation to `mori`. Route `ADJ-01` routes wrong endpoint identity or model serving failure to `kama`.
- **Key Takeaway for Out-of-Scope Routing:**
  - Tsukuroi owns **OS-level unit failure triage** (diagnosing why a system or desktop daemon like `pipewire-pulse.service` failed: package drift, unit syntax, cgroup restriction, or missing library).
  - Tsukuroi **does not own service remediation**. Tsukuroi never restarts units. Directing an out-of-scope unit to Tsukuroi cannot be treated as delegating service restart.

### 2.2 Kumitate (`kumitate-shokunin`) — Orchestration & Tooling
- **Province Scope (`kumitate-shokunin/PROVINCE.md:1-28`):**
  - *Domain:* Orchestration & tooling — scopes OMP task/hub, `ufo-fsd` scripts (`scripts/` S1–S8) & runtime (`crates/` R1–R11), and Kimi Code substrate (`~/.kimi-code/` K1–K5).
  - *Refuses:* Anything outside this domain; reports cross-domain evidence back to orchestrator.
  - *Adjacent:* Local model serving → `kama`; MCP/OAuth security → `kagi`/`kasegi`.
- **Swarm Wave Lifecycle (`kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:28-36, 91-130`):**
  - Kumitate owns `scripts/ufo-swarm-wave.mjs` (plan/run/record) and `scripts/ufo-swarm-collect.mjs` (collect).
  - Canonical contract: There is **NO `settle` CLI verb**. Settlement is performed strictly via `ufo-swarm-collect.mjs collect`.
- **Key Takeaway for Out-of-Scope Routing:**
  - When a failed unit belongs to fleet orchestration (`shokunin`, `the-tick`, `ufo-sighting`, `tmux-spawn`), Kumitate is the Tier 1 Triage Owner for worker timeout, context limit, or dispatch failure.
  - Kumitate owns automated collect joins and worker retry logic, but host-level systemd daemon management remains with the `operator`.

### 2.3 Kama (`kama-shokunin`) — Local Model Serving & Endpoint Health
- **Province Scope (`kama-shokunin/PROVINCE.md:1-53`):**
  - *Domain:* Local model serving & endpoint health — local LLM endpoints, baseURL drift, served-model reconciliation, probe conventions (`/health`, `/props`, `/slots`).
  - *Owns:* Producer discovery & read-only service inspection of local serving ports (`tools/kama-probe.sh listeners`). E.g. historical `qwen-coder.service` on loopback `34113` or llama-server on `8080`.
  - *Refuses:* Model quality/eval (`kengaku`), credentials (`kagi`), dispatch/route mechanism (`kumitate`).
  - *Hard Write Boundary (`PROVINCE.md:46-49`):*
    > *"kama never writes to `~/.config`, `~/.omp`, or systemd units. Those are operator-owned; kama detects and reports stale pins, and the operator repoints them."*
- **Key Takeaway for Out-of-Scope Routing:**
  - If a failed unit is a local model server (e.g. `llama-server`, `qwen-coder.service`), the failure is outside Mori's fleet boundary and outside Tsukuroi's package plane. Tsukuroi routes endpoint identity to Kama via `ADJ-01`.
  - Kama diagnoses port availability, HTTP status, and model alias drift, but Kama **never restarts the service**. Remediation belongs strictly to the `operator`.

### 2.4 Mori (`mori-shokunin`) — Fleet & Host Observability (森)
- **Province Scope (`mori-shokunin/PROVINCE.md:1-45, 50-78`):**
  - *Domain:* Fleet & host observability — whether the fleet, its waves, and its host are alive and progressing.
  - *Owns:* Watchdog liveness, wave settlement state, kill/OOM catalog notices, cgroup memory events, resource runway, lane silence grading.
  - *Refuses:* Dispatch/orchestration mechanism (→ `kumitate`); OS package, systemd unit, driver/firmware and boot state (→ `tsukuroi`); endpoint/model serving health (→ `kama`); credentials (→ `kagi`).
  - *Inviolable Rule (`PROVINCE.md:16`):*
    > *"Detection and report only — never remediation."*
  - *Core Policy on Unit Failures (`PROVINCE.md:24-26`):*
    > *"Failed-unit subject metadata preserves fleet-only `UNIT_FAILURE_JOURNAL` versus non-fleet `UNIT_FAILURE_OUT_OF_SCOPE` with tsukuroi triage routing; absent or unsafe subject metadata remains unknown."*

---

## 3. Structural Contradictions & Resolution

Auditing the historical baseline, round 13's rejected cutover, and L1's final ruling in `.ufo/waves/round-14/scoped-counter-contract.json` reveals four key boundary points:

### Contradiction 1: The "Tsukuroi Owns These" Remediation Fallacy
- *The Problem:* The pre-r13 census line (`frozen/mori-census.sh:908`) emitted:  
  `emit_finding UNIT_FAILURE_OUT_OF_SCOPE info "... note=non-fleet units (desktop/OS) — tsukuroi owns these"`
- *The Fallacy:* Downstream readers or naive automation interpreted "tsukuroi owns these" as an instruction that Tsukuroi will remediate or restart the failed service. But Tsukuroi's PROVINCE.md explicitly forbids service restarts (`Never installs, upgrades, or removes packages; never restarts services... A recipient is an analysis/report owner, not permission to repair`).
- *Resolution:* Finding metadata must explicitly distinguish **Triage Owner** from **Remediation Owner**. Routing preserves `owner=tsukuroi` for triage while explicitly documenting that remediation remains with the `operator`.

### Contradiction 2: Scope Does Not Choose Subject Field; Ambiguity Handling
- *The Problem:* Early design drafts assumed `--user` exclusively uses `USER_UNIT` and `--system` exclusively uses `UNIT`.
- *The Reality & Contract Rule (`l1_interface_ruling.subject_selection`):*
  - Scope does not constrain field selection: `--system` queries can carry `USER_UNIT` for user services in system session slices, and either scope can contain valid unit metadata.
  - Per `.ufo/waves/round-14/scoped-counter-contract.json` (`l1_interface_ruling.subject_selection`):
    > *"Exactly one valid UNIT or USER_UNIT field, independent of journal scope; both present is unknown even when identical. No fallback to emitter metadata."*
  - Neither manager emitter field (`_SYSTEMD_UNIT`, `_SYSTEMD_USER_UNIT`) is ever substituted for a failed subject.

### Contradiction 3: Binary Partition vs. Unattributed Metadata (Quality Criterion 30)
- *The Problem:* If a journal record has a missing, truncated, array-valued, or unreadable subject field, a binary filter treats it as non-fleet (`is_fleet = false`), falsely dumping corrupted records onto Tsukuroi.
- *Resolution (`l1_interface_ruling.unknown_subject`):* Classification is strictly tri-state:
  1. `fleet` (subject matches historical case-insensitive token set `'shokunin|ufo-sighting|tmux-spawn|the-tick|fleet'`);
  2. `non-fleet` (subject is present, valid string, and does not match fleet tokens);
  3. `unattributed` (subject field absent, empty, non-string, malformed, or both `UNIT` and `USER_UNIT` present).
  Per `l1_interface_ruling.unknown_subject`, unattributed records emit:
  `UNIT_FAILURE_UNATTRIBUTED_JOURNAL info, scope=user|system count=N owner=unresolved reason=subject-metadata-unknown`.

### Contradiction 4: Generic Fleet Failure Severity (Prompt Typo vs. Historical Baseline)
- *The Problem:* The wave prompt suggested `UNIT_FAILURE_JOURNAL warn`.
- *The Resolution (`l1_interface_ruling.generic_unit_failure_severity`):* Generic fleet failure is `info`, strictly preserving the frozen r12 `:904–908` baseline (`emit_finding UNIT_FAILURE_JOURNAL info "class=unit_failure count=$c_unit_fleet scope=fleet-units"`). Alarm escalation is reserved for positive kernel OOM notices and `UNIT_RESULT=oom-kill` (`crit` => `DRIFT`), and user-process SIGKILL (`warn` => `DRIFT`).

---

## 4. The Proposed Move: Two-Tier Ownership Architecture for Out-of-Scope Unit Triage

We propose a decoupled **Two-Tier Ownership Architecture** for out-of-scope unit triage routing that completely reconciles Mori's census emissions with Tsukuroi's, Kumitate's, and Kama's declared provinces without requiring any extra triage runtime architecture.

### 4.1 Two-Tier Architecture Definition

```
+--------------------------------------------------------------------------------------------------+
| TIER 0: OBSERVABILITY & SCOPED DETECTION (mori-shokunin)                                          |
| - Read-only journal inspection extracting unambiguous subject metadata (USER_UNIT / UNIT).        |
| - Tri-state classification: Fleet vs. Non-Fleet vs. Unattributed.                                |
| - Inviolable boundary: Detection and report only — NEVER remediation (PROVINCE.md:16).            |
+-----------------------------------+--------------------------------------------------------------+
                                    |
               Emits Scoped Findings with Structured Owner Metadata
                                    |
                                    v
+--------------------------------------------------------------------------------------------------+
| TIER 1: TRIAGE & ROOT-CAUSE DIAGNOSIS OWNERS (Domain Specialists)                                 |
| - Non-Fleet OS/Desktop Units:  tsukuroi-shokunin (package state, unit syntax, cgroup, drivers).   |
|   -> Secondary Handoff ADJ-01: kama-shokunin if failed unit is local LLM serving producer.       |
| - Fleet Worker/Orchestration:  kumitate-shokunin (wave lifecycle, task timeout, context clamp).   |
| - Unattributed Records:        owner=unresolved (triage pending metadata recovery).              |
| - Inviolable boundary: Analysis & reporting only — NOT permission to repair (PROVINCE.md:38).    |
+-----------------------------------+--------------------------------------------------------------+
                                    |
               Produces Diagnostic Findings & Operator Action Items
                                    |
                                    v
+--------------------------------------------------------------------------------------------------+
| TIER 2: REMEDIATION & ACTUATION AUTHORITY (Remediation Actors)                                    |
| - Host / OS / Service Units:   OPERATOR EXCLUSIVELY (systemctl restart, pacman, config edit).    |
| - Swarm Wave Settlement:       kumitate-shokunin (`ufo-swarm-collect.mjs collect` join only).    |
| - Inviolable boundary: Leaf shokunin agents NEVER mutate host systemd units or restart services. |
+--------------------------------------------------------------------------------------------------+
```

### 4.2 Sibling Handoff Routing Matrix (Citing `.ufo/waves/round-14/scoped-counter-contract.json`)

| Classification Category | Observed Unit Subject (`USER_UNIT` / `UNIT`) | Finding Emitted by Mori Census | Severity & Roll Impact | Tier 1: Triage Owner (Diagnosis Only) | Tier 2: Remediation Owner (Actuation Authority) | Triage Protocol & Notes |
|---|---|---|---|---|---|---|
| **Fleet Unit Failure** | Matches regex `'shokunin\|ufo-sighting\|tmux-spawn\|the-tick\|fleet'` | `UNIT_FAILURE_JOURNAL` | `info` => `CLEAN` (per `l1_interface_ruling.generic_unit_failure_severity`) | `kumitate-shokunin` | `kumitate-shokunin` (collect/retry) & `operator` | Kumitate evaluates worker lifecycle and task logs; runs `ufo-swarm-collect.mjs collect`. Never invoke non-existent `settle`. |
| **Non-Fleet Unit Failure (OS / Desktop)** | Valid string, no fleet match (e.g. `pipewire-pulse.service`, `dunst.service`) | `UNIT_FAILURE_OUT_OF_SCOPE` | `info` => `CLEAN` (per `l1_interface_ruling.generic_unit_failure_severity`) | `tsukuroi-shokunin` (`owner=tsukuroi`) | **`operator`** (strictly forbidden to Tsukuroi) | Tsukuroi inspects unit status (`systemctl --user status`), package drift (`pacman -Qkk`), and journal errors. Reports finding to Operator. |
| **Non-Fleet Unit Failure (Model Serving)** | Valid string, matches local serving port listener (e.g. `qwen-coder.service`, `llama-server`) | `UNIT_FAILURE_OUT_OF_SCOPE` | `info` => `CLEAN` | `tsukuroi-shokunin` → handoff `ADJ-01` to `kama-shokunin` | **`operator`** (strictly forbidden to Kama) | Tsukuroi identifies service failure; Kama verifies port listener (`kama-probe.sh listeners`) and consumer pins (`registry/endpoint-consumers.tsv`). Operator restarts service. |
| **Unattributed Unit Failure** | Absent, empty, non-string, malformed, or both `UNIT` and `USER_UNIT` present | `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` | `info` => `CLEAN` (per `l1_interface_ruling.unknown_subject`) | `unresolved` (`owner=unresolved`) | **`operator`** | Logged with `owner=unresolved reason=subject-metadata-unknown`; never falsely defaulted to non-fleet. |

### 4.3 Concrete Finding Metadata Schemas (Citing `scoped-counter-contract.json`)

Per `.ufo/waves/round-14/scoped-counter-contract.json` §`l1_interface_ruling`:

1. **`UNIT_FAILURE_OUT_OF_SCOPE` Finding (Non-Fleet):**
   ```text
   FINDING UNIT_FAILURE_OUT_OF_SCOPE severity=info class=unit_failure count=1 scope=user owner=tsukuroi note=non-fleet units (desktop/OS) — tsukuroi triages; operator remediates boot=<BOOT_ID>
   ```

2. **`UNIT_FAILURE_UNATTRIBUTED_JOURNAL` Finding (Missing/Malformed/Ambiguous Metadata):**
   ```text
   FINDING UNIT_FAILURE_UNATTRIBUTED_JOURNAL severity=info class=unit_failure count=1 scope=user owner=unresolved reason=subject-metadata-unknown boot=<BOOT_ID>
   ```

3. **`OOM_KILL_JOURNAL` Finding (Global Critical Alarm, `l1_interface_ruling.oom`):**
   ```text
   FINDING OOM_KILL_JOURNAL severity=crit class=oom_kill count=N user_notice=A system_notice=B user_unit_oom=C system_unit_oom=D boot=<BOOT_ID>
   ```
   Exactly one `OOM_KILL_JOURNAL crit` alarm per census triggering `MORI_CENSUS: DRIFT` (exit 1), exposing the four separate counters (`user_notice`, `system_notice`, `user_unit_oom`, `system_unit_oom`) without cross-scope summing.

4. **No Raw Unit Payload Echoing:**
   The findings emit validated counts and structured tokens only; they **never echo raw unit strings or unvalidated user bytes**, preventing journal payload injection (Quality Criterion 15 / `JournalSentinel`).

---

## 5. Trace Across Second-Order Surfaces

1. **Runtime Surface (`tools/mori-census.sh`):**
   - Extracting structured `USER_UNIT` and `UNIT` via `jq` avoids spawning external subshell pipes into text greps, preventing SIGPIPE 141 failures under `set -eo pipefail`.
   - Implementing `l1_interface_ruling.subject_selection`: exactly one valid `UNIT` or `USER_UNIT` field independent of scope; records with both present grade as unattributed even when identical.
   - Bounding queries to `--output-fields=_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT` guarantees zero raw `MESSAGE` text allocation in memory, preventing buffer bloat and log leakage.
2. **Contract Surface (`PROVINCE.md`, `SCORECARD.md`, `QUALITY.md`, `scoped-counter-contract.json`):**
   - Fulfills the Round 14 milestone contract (`spec.json:14` and `scoped-counter-contract.json`): restores `UNIT_FAILURE_JOURNAL` as fleet-only, `UNIT_FAILURE_OUT_OF_SCOPE info owner=tsukuroi` for non-fleet units, and `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` for unknown metadata.
   - Enforces Quality Criterion 29 (no-harm behavioral equivalence after selector cutover) and Quality Criterion 30 (explicit `UNKNOWN` for missing subject attribution).
   - Preserves Tsukuroi's province guarantee: Tsukuroi is not assigned unauthorized service restart obligations.
3. **Substrate Surface (systemd journald & cgroup v2):**
   - Aligns with systemd upstream implementation (S036 `unit.c:6333-6342`): correctly consumes client-supplied `USER_UNIT`/`UNIT` attached by `log_unit_struct()`, avoiding emitter confusion with PID 1's `_SYSTEMD_UNIT`.
   - Protects cgroup boundaries: recognizes that out-of-scope unit failures do not imply fleet cgroup pressure or fleet wave abortion.
4. **Verification Surface (`tools/mori-round14-regressions.py` & `tools/mori-round13-regressions.py`):**
   - Enables clean red-before / green-after regression gates:
     - *Red-before:* Entering census `39abda0a...` at `dbe8500` emits no `UNIT_FAILURE_OUT_OF_SCOPE` and lacks `owner=tsukuroi` (fails gate with rc 1).
     - *Green-after:* Repaired census emits `UNIT_FAILURE_OUT_OF_SCOPE info owner=tsukuroi` on non-fleet fixtures, emits `UNIT_FAILURE_JOURNAL info` on fleet fixtures, and rolls `CLEAN` (exit 0) when only non-fleet failures exist.

---

## 6. Risks & Bounded Falsifiers

1. **Harness Grep Token Sensitivity:**
   - *Risk:* If a strict test harness asserts exact token patterns, changing finding names or attributes could cause failures.
   - *Boundary:* The tokens `owner=tsukuroi` on out-of-scope and `owner=unresolved reason=subject-metadata-unknown` on unattributed findings strictly match L1's contract specification.
2. **Client-Supplied Spoofing of `USER_UNIT`:**
   - *Risk:* Because `USER_UNIT` lacks a leading underscore, an unprivileged user process could send forged journal records claiming to be `the-tick.service`.
   - *Boundary:* The census explicitly grades the notice surface `trust=client-supplied`. Mori provides observability signals; trusted audit fields (`_UID`, `_PID`) remain logged for Tsukuroi's forensic analysis.
3. **Array-Valued Journal Fields:**
   - *Risk:* If a unit failure log contains multiple `USER_UNIT` entries, `jq` might emit multiple lines, corrupting line-based counters.
   - *Boundary:* The census `jq` filter must enforce type checking: `if (.USER_UNIT | type) == "string" then ... else "unknown" end`, ensuring each journal record maps to exactly one classified count.

---

## 7. Verification Actions for L1

In accordance with Godspeed leaf bounds, this agent executed no tests, builds, or gate runs. The following verification steps are recommended for L1 post-integration:

1. **Static Sibling Province Cross-Check:**
   - Verify that all cited paths in `tsukuroi-shokunin` (`PROVINCE.md:28, 38`), `kumitate-shokunin` (`PROVINCE.md:1-28`, `swarm-wave-lifecycle.md:28-36`), and `kama-shokunin` (`PROVINCE.md:46-49`) exist and match the cited line anchors.
2. **Non-Fleet Routing Finding Verification:**
   - In synthetic non-fleet fixture runs (e.g. `pipewire-pulse.service`), assert:
     ```sh
     grep -c 'FINDING UNIT_FAILURE_OUT_OF_SCOPE severity=info' <run.stdout> # == 1
     grep -c 'owner=tsukuroi' <run.stdout>                                  # >= 1
     grep -c 'FINDING UNIT_FAILURE_JOURNAL' <run.stdout>                    # == 0
     ```
3. **Fleet Failure Finding Verification:**
   - In synthetic fleet fixture runs (e.g. `the-tick.service`), assert:
     ```sh
     grep -c 'FINDING UNIT_FAILURE_JOURNAL severity=info' <run.stdout>      # == 1
     grep -c 'FINDING UNIT_FAILURE_OUT_OF_SCOPE' <run.stdout>               # == 0
     ```
4. **Unattributed Failure Finding Verification:**
   - In synthetic missing/ambiguous metadata fixture runs (including both `UNIT` and `USER_UNIT` present), assert:
     ```sh
     grep -c 'FINDING UNIT_FAILURE_UNATTRIBUTED_JOURNAL severity=info' <run.stdout> # == 1
     grep -c 'owner=unresolved' <run.stdout>                                         # >= 1
     grep -c 'reason=subject-metadata-unknown' <run.stdout>                          # >= 1
     ```
5. **Global OOM Critical Line Verification (`l1_interface_ruling.oom`):**
   - In positive OOM fixture runs, assert:
     ```sh
     grep -c 'FINDING OOM_KILL_JOURNAL severity=crit' <run.stdout>          # == 1
     grep -oE 'user_notice=[0-9]+ system_notice=[0-9]+ user_unit_oom=[0-9]+ system_unit_oom=[0-9]+' <run.stdout> # >= 1
     grep -oE '^MORI_CENSUS: DRIFT' <run.stdout>                            # == 1
     ```
6. **No-Message & No-Unit-Byte Leakage:**
   - Verify that census stdout contains zero unvalidated unit strings or `MESSAGE=` text:
     ```sh
     grep -cE 'MESSAGE=|"MESSAGE"[[:space:]]*:' <run.stdout>                # == 0
     ```
