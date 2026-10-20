# ConnectSiblingOverlap — Bounded Cross-Axis Synthesis: Alarm Fallbacks, Remediation Refusal, and Fleet Membership Invariants

**Seat:** `MoriR15.ConnectSiblingOverlap`  
**Wave:** `mori-r15-positive`  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Role:** UFO-FSD connector  
**Milestone:** retain validated positives without fabricated totals  
**Judged Axis:** `coverage` (lowest owned axis 6 vs operability 7)  
**Advisory Status:** Leaf member report-only. Production files not edited; no subagents dispatched; no gates, builds, tests, or linters executed. L1 integrates and verifies.

---

## 1. Godspeed Posture & Declared Axes

1. **Name the axes:**
   - **`coverage` (primary judged axis, score 6 held):** Expand structured journal alarm coverage under claim C1 so that valid, current-boot kernel OOM notices, unit OOM results, process SIGKILL records, and unit signal failures retain their critical OOM alarm (`OOM_KILL_JOURNAL crit`) and user signal warning (`KILL_SIGNAL_JOURNAL warn`) even when adjacent malformed, non-matching, or foreign-boot records invalidate the aggregate class.
   - **`adjacency` (guarded axis, score 6 held):** Strictly preserve boundaries between Mori (fleet and host observability), Tsukuroi (OS substrate, systemd units, driver triage), and Kumitate (task/hub orchestration). Ensure alarm fallbacks never trigger or assume host remediation, never restart services, and never assert fleet membership from partial or unpartitioned streams.
   - **`calibration` (guarded axis, score 5 held):** Enforce that raw aggregate and split counts remain explicitly `unavailable:<reason>` when invalid; never synthesize positive counts into a fabricated numeric zero or total; never misrepresent individual unit notices as unique victims or fleet-caused kills.
   - **`operability` (guarded axis, score 7 held):** Process the existing captured stderr-free valid JSON stream in a single execution without adding extra `journalctl` queries or introducing new unhandled exit statuses.
   - **`freshness` & `depth` (observed axes, scores 5/5 held):** Anchor all semantics to primary source registries (S013, S014, S015, S035, S036, S037, S038) and retain explicit, documented residuals.

2. **Iterate cheap, in parallel:** Evaluated current round cache, sibling provinces, reviewer audits (`ReviewRouting`, `ReviewKernelPredicate`, `ReviewUnitPredicate`, `ReviewProcessPredicate`, `ReviewRawTotals`), and incoming fixture packs (`CrossScope.json`, `FanoutPositive.json`, `CleanControls.json`) concurrently without running heavyweight processes.
3. **Keep moves that improve any axis and harm none:** Bounded move advances `coverage` by recovering alarms from corrupted streams while holding `adjacency`, `calibration`, and `operability` uncompromised.
4. **Don't aim — let the frontier walk itself:** Surface exact mechanical constraints and cross-lane contracts so the implementation naturally satisfies both sibling boundaries and verification requirements.

---

## 2. Evidence & Sibling Province Map

All paths and citations below were read read-only from committed repository declarations and knowledge bases.

### 2.1 Mori (`mori-shokunin`) — Fleet & Host Observability (森)
- **Province & Domain:** Whether the fleet, its waves, and its host are alive and progressing (`/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md:3-5`).
- **Owns (read-only probes):** Watchdog liveness, `.ufo/waves/*` settlement state, kill/OOM catalog-ID records and signal-11 coredump records from independently labeled user/system journals, cgroup `memory.events`, resource runway (disk, PSI), lane silence grading (`PROVINCE.md:6-10`).
- **Refuses:** Dispatch and orchestration mechanism (→ Kumitate); OS package, systemd unit, driver/firmware, and boot state (→ Tsukuroi); endpoint health (→ Kama); credential material (→ Kagi) (`PROVINCE.md:12-16`).
- **Strict Invariant:** **"Detection and report only — never remediation."** (`PROVINCE.md:16`).
- **Out of province:** Report, never absorb (`PROVINCE.md:18`).
- **Adjacency & Causation Boundary:** "A host record alone does not prove a fleet-caused kill" (`PROVINCE.md:31`); "Correlation is not causation" (`PROVINCE.md:75`).

### 2.2 Tsukuroi (`tsukuroi-shokunin`) — Host Operability & System Repair (繕)
- **Province & Domain:** Host operability and system repair — OS substrate itself: package state (`pacman -Qkk`), systemd user units and timers, journal/boot triage (`journalctl -b`), driver/firmware plane (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:3-15`).
- **Refuses:** Endpoint/model serving health (→ Kama), secrets (→ Kagi), binary RE (→ Kaidoku/Revenger).
- **Strict Invariant:** "Never installs, upgrades, or removes packages; never restarts services. Detection and report; the operator remediates" (`tsukuroi-shokunin/PROVINCE.md:27-28`).
- **Adjacency Route ADJ-04:**
  - *Trigger:* Host pressure or kill signals needing fleet/wave attribution, liveness or progress correlation (`tsukuroi-shokunin/PROVINCE.md:49`).
  - *Next recipient:* `mori`.
  - *Minimum handoff evidence:* Capture time, boot/window, exact counter or PSI command/exit, observed value; distinguish presence, cumulative count, and dated event. "Request correlation, not a claim that a wave caused OOM" (`tsukuroi-shokunin/PROVINCE.md:49`).
  - *Crucial Governance Contract:* **"A recipient is an analysis/report owner, NOT permission to repair. Tsukuroi retains the OS finding. No row authorizes configuration writes, service changes... Shared evidence is not shared ownership; unresolved ownership goes to the protocol integrator"** (`tsukuroi-shokunin/PROVINCE.md:38-42`).

### 2.3 Kumitate (`kumitate-shokunin`) — Orchestration & Tooling
- **Province & Domain:** Scopes OMP task/hub, ufo-fsd scripts and runtime (`/home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md:3-6`).
- **Owns:** Origin scripts (`/home/vgpnk/Projects/ufo-fsd-alpha/scripts/`), runtime layer, Kimi Code substrate, and task orchestration.
- **Refuses:** Anything outside this domain; reports cross-domain evidence back to orchestrator. Upstream defects filed in lane reports for the operator; never patched directly (`kumitate-shokunin/PROVINCE.md:6, 28`).
- **Lifecycle Contract:** Mori passively monitors filesystem settlement (`SURFACE waves`), while Kumitate owns collection (`ufo-swarm-collect`) and member lifecycle. Mori never executes task eviction, process cancellation, or wave termination.

---

## 3. Analysis: Remediation and Fleet Membership Boundaries

The central directive of this review is to **ensure alarm fallback never assumes remediation or fleet membership**. Tracing this across runtime, contract, substrate, and verification reveals three critical traps:

### 3.1 Trap 1: The Remediation Assumption
- **Mechanism:** In system observability, alarming on critical conditions (such as kernel OOM or SIGKILL) frequently triggers automated remedial workflows in naive architectures (e.g., restarting failed systemd units, evicting running agents, killing sibling processes, or adjusting cgroup memory limits).
- **Province Mandates:**
  - Mori's charter explicitly declares: *Detection and report only — never remediation* (`PROVINCE.md:16`).
  - Tsukuroi's charter explicitly declares: *A recipient is an analysis/report owner, not permission to repair... Never restarts services* (`tsukuroi-shokunin/PROVINCE.md:27-28, 38`).
  - Kumitate's charter handles swarm tasks and hub communications, refusing un-orchestrated host-level process termination (`kumitate-shokunin/PROVINCE.md:6`).
- **Resolution:**
  - Mori’s fallback findings (`OOM_KILL_JOURNAL crit` and `KILL_SIGNAL_JOURNAL warn`) must remain pure informational evidence. They must emit structured text findings with severity and token attributes to `stdout`.
  - The finding note and attributes must NEVER include action directives (such as `action=restart`, `remediate=kill_unit`, or `target=evict`).
  - Downstream consumers (e.g., L1 aggregator or operator monitoring) must receive the finding as a diagnostic signal for operator triage, not an automated trigger for systemd restart or process eviction.

### 3.2 Trap 2: The Fleet Membership Assumption
- **Mechanism:** When a unit failure record (`MESSAGE_ID=d9b373ed...`) or kernel OOM notice (`MESSAGE_ID=fe6faa94...`) is observed, there is a risk of assuming that the affected unit is a fleet unit.
- **Source Constraints (S037, S038, S015):**
  - As established in `corpus/knowledge/journal-alarm-routing-r14.md:25-34`, `UNIT=` and `USER_UNIT=` are client-supplied subject fields passed from the manager. They are not cryptographically authenticated identifiers.
  - The trusted fields `_SYSTEMD_UNIT` and `_SYSTEMD_USER_UNIT` indicate the logging process (the manager emitter), NOT the failed subject.
  - In Round 14, fleet classification uses the token heuristic `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet` (`classification_rule=unit-name-token`). This token match is explicitly labeled as a routing rule, not proof of fleet ownership or causation (`tools/mori-census.sh:1272, 1279`).
- **The Round-15 Fallback Invariant:**
  - In Round 15 (C1), when an adjacent malformed, non-matching, or foreign-boot record exists in the stream, the aggregate class is INVALID (`record-invalid`, `multi-boot`, or `boot-mismatch`).
  - The Round 15 contract specifies: **"Existing info owner partition remains aggregate-only unavailable."**
  - **Second-Order Danger:** If Mori attempted to inspect the `USER_UNIT` or `UNIT` field of an individual positive record in a corrupted stream and emit `UNIT_FAILURE_JOURNAL` (fleet, owner=`mori`) or `UNIT_FAILURE_OUT_OF_SCOPE` (non-fleet, owner=`tsukuroi`), Mori would be fabricating a partition on an incomplete, unvalidated batch.
  - Therefore, during fallback when aggregate status is not `ok`, **all unit failure partition findings (`UNIT_FAILURE_JOURNAL`, `UNIT_FAILURE_OUT_OF_SCOPE`, `UNIT_FAILURE_UNATTRIBUTED_JOURNAL`) MUST BE COMPLETELY SUPPRESSED (unavailable)**.
  - The global alarms (`OOM_KILL_JOURNAL crit` and `KILL_SIGNAL_JOURNAL warn`) are host- and session-level alerts. They fire because a fatal condition occurred in the environment, but they must strictly maintain:
    - `attribution=none`
    - `fleet_membership=unclaimed`
    - `note=... a per-unit notice or unit result is not a unique-victim, kill-total or fleet-cause count...`
  - Neither alarm warrants or asserts fleet ownership.

### 3.3 Trap 3: Cross-Scope Signal Bleed (Desktop/OS vs. Fleet User Space)
- **Mechanism:** On a developer workstation, desktop daemons (e.g., `pipewire-pulse.service`, browser renderer sub-processes, or graphical session services) frequently experience SIGKILL or terminate with signal results during system churn. These system-level events belong to Tsukuroi's OS diagnosis domain.
- **Boundary Violation:** If system-scoped process exits (`EXIT_CODE=killed`, `EXIT_STATUS=9`) or system-scoped unit failures (`UNIT_RESULT=signal`) were allowed to trigger `KILL_SIGNAL_JOURNAL warn`, Mori would be alerting on non-fleet OS background noise, directly absorbing Tsukuroi's domain and causing false `DRIFT` on the fleet.
- **Resolution:**
  - `KILL_SIGNAL_JOURNAL warn` must gate exclusively on **USER-SCOPE** positives (`user:positive_process_sigkill > 0` or `user:positive_unit_signal > 0`).
  - System-scope signal events remain strictly informational (`KILL_SIGNAL_JOURNAL_SYSTEM info` or surface-only) and must NEVER trip the user warning alarm.
  - This is verified by fixture pack `CrossScope.json`, where `crossscope_system_unit_signal_no_user_warn` and `crossscope_system_process_sigkill_no_user_warn` declare `want_signal: false`.

---

## 4. The Non-Obvious Move: Strict Decoupling of Positive Evidence Alarms from Subject Partitioning

Synthesizing across the round's proposals (`ReviewRouting`, `ReviewKernelPredicate`, `ReviewUnitPredicate`, `ReviewProcessPredicate`, `ReviewRawTotals`):

### 4.1 The Proposal
**Decouple positive alarm triggering from the unit failure subject partition by implementing a dedicated per-record extraction pass that computes scoped positive counters (`positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`), feeds global alarms directly, and enforces complete suppression of all subject-partition findings whenever aggregate class validity fails.**

### 4.2 Architectural Mechanics

1. **Extraction on the Uncorrupted Stream Slice:**
   - In `tools/mori-census.sh::journal_query`, immediately following successful command capture (`CAP_RC=0`, `err_bytes=0`) and prior to the status evaluation branches at line 1103:
   - Execute a per-record positive filter on the exact same `$raw` payload.
   - Filter ensures robust type-guarding:
     ```jq
     [ .[] | select(type == "object")
           | select((._BOOT_ID | type) == "string" and ._BOOT_ID == $boot)
           | select((.MESSAGE_ID | type) == "string" and .MESSAGE_ID == $id)
           | <class_predicate> ] | length
     ```
   - Class predicates:
     - Kernel OOM: scalar matching `$id` (`fe6faa94...`).
     - Unit OOM: `(.UNIT_RESULT | type) == "string" and .UNIT_RESULT == "oom-kill"`.
     - Unit Signal: `(.UNIT_RESULT | type) == "string" and .UNIT_RESULT == "signal"`.
     - Process SIGKILL: `(.EXIT_CODE | type) == "string" and .EXIT_CODE == "killed"` and scalar status `((.EXIT_STATUS | type) as $t | ($t == "string" or $t == "number")) and (.EXIT_STATUS | tostring) == "9"`.
   - On capture error, timeout, non-empty stderr, or unparseable malformed JSON, all positive tokens default to `unavailable:<JQ_STATUS>`, never numeric zero.

2. **Alarm Gate Synthesis (Coverage Improvement):**
   - **`OOM_KILL_JOURNAL crit`:**
     - Triggers if: `raw_ko > 0` OR `raw_uo > 0` OR `positive_kernel_oom > 0` OR `positive_unit_oom > 0` across either `user` or `system` scope.
     - Finding line retains existing raw tokens (`user_notice=unavailable:record-invalid user_unit_oom=unavailable:record-invalid`) and appends explicit positive evidence tokens (`user_positive_kernel_oom=1 ...`).
     - Preserves `attribution=none` and explicitly states in the note that the alarm indicates environment OOM occurrence, not unique victim count or fleet causation.
   - **`KILL_SIGNAL_JOURNAL warn`:**
     - Triggers if: `raw_ps > 0` OR `raw_us > 0` OR `user_positive_process_sigkill > 0` OR `user_positive_unit_signal > 0` in **USER SCOPE ONLY**.
     - Raw counts stay `unavailable:<reason>`; positive evidence tokens are appended.

3. **Subject Partition Invariant (Adjacency & Calibration Protection):**
   - The partition loop at `tools/mori-census.sh:1264-1291` (`UNIT_FAILURE_JOURNAL`, `UNIT_FAILURE_OUT_OF_SCOPE`, `UNIT_FAILURE_UNATTRIBUTED_JOURNAL`) continues to gate strictly on `[ "${js[$key]}" = ok ]`.
   - When the aggregate stream is invalid, **zero unit failure finding lines are emitted**.
   - No attempt is made to salvage subject routing from individual records. This guarantees that Mori never asserts fleet ownership or routes non-fleet diagnostics to Tsukuroi based on an unverified, corrupted stream.

---

## 5. Trace of Second-Order Effects Across Surfaces

| Surface | Direct Effect | Second-Order Effect | Safeguard / Invariant |
|---|---|---|---|
| **Runtime (`tools/mori-census.sh`)** | Extra jq evaluation pass on captured `$raw` inside `journal_query`. | Minimal latency delta; avoids spawning a second `journalctl` process or subshell. | Executes only when `CAP_RC=0`; parser failure maps to `unavailable:malformed-json`. |
| **Contract (`spec.json`, C1 Claim)** | Valid positive records prevent silent OOM suppression under mixed streams. | Raw counters and aggregates remain honest (`unavailable:<reason>`); no fabricated totals. | Satisfies milestone: "retain validated positives without fabricated totals". |
| **Substrate (systemd / journalctl)** | Evaluates JSON objects with mixed types (arrays, nulls, wrong boot IDs). | Does not crash parser or trigger uncaught exit codes in bash. | Initial `select(type=="object")` prevents jq path indexing errors (`"str" \| .MESSAGE_ID`). |
| **Adjacency: Tsukuroi (OS Triage)** | Non-fleet unit failures from corrupted streams are not routed to Tsukuroi. | Tsukuroi's ledger is not polluted with partial, unauthenticated failure records. | ADJ-04 handoff contract preserved; recipient remains diagnostic reporter, never repair agent. |
| **Adjacency: Kumitate (Orchestration)** | Swarm tasks do not suffer false wave evictions or premature cancellations. | Kumitate's wave lifecycle proceeds without phantom failures triggered by host noise. | System signals excluded from user warn; alarms remain informational. |
| **Verification (Harness & Gates)** | Regression pin `R14_SEC_DUP_MSGID_MIXED` previously expected OOM suppression. | C1 deliberately changes this behavior: the mixed stream must now fire `OOM_KILL_JOURNAL crit`. | L1 must re-pin `R14_SEC_DUP_MSGID_MIXED` in `tools/mori-round14-regressions.py` as an intentional contract evolution. |

---

## 6. Stated Contradictions & Risks (No Scalar Smoothing)

1. **Coverage vs. Adjacency Tension:**
   - *Tension:* Maximizing alarm coverage could tempt an author to also recover unit failure partitions from partial records (e.g. alarming on `UNIT_FAILURE_JOURNAL` if a single record has `USER_UNIT=shokunin.service`).
   - *Resolution:* Contradiction explicitly resolved in favor of province purity. Aggregate partitions require whole-batch validation; unit failure routing stays aggregate-only unavailable. Alarms fire globally on the host plane, not as fleet-owned claims.

2. **Positive Zero vs. Reassurance:**
   - *Risk:* Emitting `positive_kernel_oom=0` when raw status is `unavailable:record-invalid` might be misread by an operator as proof that no OOM occurred.
   - *Resolution:* When positive extraction cannot run (e.g. capture or parse failure), positive tokens must read `unavailable:<status>`. On successful parse with zero matches, the raw token `unavailable:<status>` remains prominently displayed on the same line.

3. **Schema Drift vs. Frozen Drift Pin:**
   - *Risk:* Adding positive tokens to `DRIFT_COUNTER_KEYS` modifies the baseline volatile list, tripping the legacy round-10 drift pin (`MORI_DRIFT: volatile_fields`).
   - *Resolution:* Do not silently re-pin. The drift pin remains recorded as status-neutral conformance debt. L1 evaluates re-pinning under deliberate operator review.

---

## 7. Concrete Supported Recommendations for L1 Integrator

1. **Implementation in `tools/mori-census.sh`:**
   - In `journal_query` (around line 1099), insert the positive extraction filter prior to `case "$parsed" in record-invalid|multi-boot|boot-mismatch)`.
   - Populate `JQ_POS_KERNEL`, `JQ_POS_UNIT_OOM`, `JQ_POS_UNIT_SIG`, and `JQ_POS_SIGKILL`.
   - In `probe_journal`, update `oom_fire` (lines 1314–1321) to check both raw and positive values:
     ```bash
     [ "$ko_pos" -gt 0 ] 2>/dev/null && { oom_fire=1; oom_path_k=1; }
     [ "$uo_pos" -gt 0 ] 2>/dev/null && { oom_fire=1; oom_path_u=1; }
     ```
   - In `probe_journal`, update `kill_fire` (lines 1344–1351) to check user-scope positive values:
     ```bash
     [ "$ps_pos" -gt 0 ] 2>/dev/null && { kill_fire=1; kill_paths="${kill_paths:+$kill_paths,}process_sigkill"; }
     [ "$us_pos" -gt 0 ] 2>/dev/null && { kill_fire=1; kill_paths="${kill_paths:+$kill_paths,}unit_result_signal"; }
     ```
   - Keep lines 1264–1291 (`UNIT_FAILURE_*`) strictly gated on `[ "${js[$key]}" = ok ]`.

2. **Harness & Pin Alignment (`tools/mori-round14-regressions.py`):**
   - Re-pin `R14_SEC_DUP_MSGID_MIXED` (`:1552-1564`) to assert that `OOM_KILL_JOURNAL crit` DOES fire, while `kernel_oom_notice` remains `unavailable:record-invalid`.
   - Update the docstring at `:105-109` to record that C1 resolved the mixed-stream alarm suppression limitation.

3. **Knowledge Base Annotation (`corpus/knowledge/journal-alarm-routing-r14.md`):**
   - Update line 221 and lines 386–390 to explicitly describe the C1 positive fallback mechanism and document that subject routing remains aggregate-only unavailable.

---

## 8. Residuals & Verification Surface (For L1 Execution)

*No verification was run by this seat. The following checks are documented for L1 post-integration:*

1. **Cross-Scope Isolation Check:**
   - Execute fixture `CrossScope.json`: verify that system signal records produce NO user `KILL_SIGNAL_JOURNAL warn`.
2. **Positive Alarm Under Invalid Stream Check:**
   - Execute fixture `FanoutPositive.json` and `KernelUser.json`: verify that streams containing valid current-boot positives mixed with malformed MESSAGE_ID arrays fire `OOM_KILL_JOURNAL crit` once and keep raw fields as `unavailable:record-invalid`.
3. **Partition Suppression Check:**
   - Verify that in mixed invalid streams, NO `UNIT_FAILURE_JOURNAL`, `UNIT_FAILURE_OUT_OF_SCOPE`, or `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` finding is emitted.
4. **Remediation Absence Check:**
   - Confirm that the census output contains no action keywords (`action=`, `restart=`, `kill=`) and that host service states remain unmodified.

---

## 9. Tooling Record

In accordance with the 2026-10-19 operator tooling directive and the parent's host-safety amendment:
- **Tools installed or updated:** None.
- **Operations executed:** Read-only inspections of local files; no `pacman` commands executed.
