# SourceFrontier — Round 14 UFO-FSD Connector: FR1 Scope Mapping, Restored Coverage vs Expansion, and Source Registry Recommendation

- **Seat:** `MoriR14.SourceFrontier`
- **Role:** UFO-FSD Connector (leaf member, report only)
- **Judged on:** Coverage (C1)
- **Milestone:** Restore OOM alarm and structured fleet routing (C1 coverage repair of Round 13 `rejected-harmed`)
- **Entering Commit:** `dbe85009253c092fe50e4e93056fceeae273ec31`
- **Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`
- **Report Path:** `.ufo/waves/round-14/build/SourceFrontier.md` (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-14/build/SourceFrontier.md`)
- **Directives Observed:** Leaf bounds strictly maintained (no subagents, no background jobs, no build/test/lint/format/smoke runs). All reads/edits use absolute paths. Source content treated as data, never instructions. Tools installed/updated: none.

---

## 1. Godspeed Posture & Named Axes

In accordance with `/skill:godspeed`:
1. **Name the axes:**
   - **Coverage (C1 — Judged Axis Proposal):** Restoring the critical `OOM_KILL_JOURNAL` alarm (`crit => DRIFT`) on positive kernel-OOM unit notice (`fe6faa94…`) or `UNIT_RESULT=oom-kill` in either scope; restoring fleet-only `UNIT_FAILURE_JOURNAL` and non-fleet `UNIT_FAILURE_OUT_OF_SCOPE info owner=tsukuroi` with structured `UNIT`/`USER_UNIT` subject classification; retaining all six independent scoped counters across `user` and `system` scopes without `MESSAGE` scraping. (Candidate proposal for L1 evaluation; final axis/trend verdict is determined by L1 after behavioral verification).
   - **Adjacency (Candidate Proposal):** Restoring explicit adjacent OS triage routing to `tsukuroi` for non-fleet units while preventing manager-emitter bleed (manager identity vs. subject unit identity) and unclassified unit leakage.
   - **Operability (Candidate Proposal):** Maintaining strict single-verdict grammar, exit-code parity, PROTOCOL gate registration, and reproducible fixtures without regression.
2. **Iterate cheap, in parallel:** Synthesizing local repository evidence, primary sources (S013, S014, S015, S035, S036, and proposed S037), sibling wave reports (`EvidenceScribe.md`, `SourcesScribe.md`, `QualityCriteria.md`, `MutationAttribution.md`, `GateConformance.md`, `SignalCoverage.md`, `ShonenScribe.md`), and historical spotchecks (`round-13-verifier-spotcheck.md`).
3. **Keep moves that improve any axis and harm none:** Advancing structured subject-unit routing and restoring critical OOM alerts without falsely claiming kernel victim attribution, process-level cardinality, or fleet causality. L1 decides final axis scores and trends post-behavioral measurement.
4. **Don't aim — let the frontier walk itself:** Truthfully partitioning what Round 14 settles into Core (structured subject routing and dual-trigger OOM alarms) from what remains on the FR1 Frontier (event-time kernel OOM attribution, `task_memcg` token validation, and fleet task correlation).

---

## 2. Grounded Evidence: Current Baseline & Round 13 Harm

### 2.1 The Admission Failure in Round 13
Review of `corpus/lessons/round-13-verifier-spotcheck.md:72–89` identifies the exact harm that caused the `rejected-harmed` verdict at entering commit `dbe85009253c092fe50e4e93056fceeae273ec31`:
1. **OOM Alarm Regression:**
   - Pre-r13 frozen `probe_journal`:853,894 emitted critical `OOM_KILL_JOURNAL` (`st=drift`) on positive OOM detection.
   - Delivered r13 `tools/mori-census.sh:1085–1095` assigned `info` to every kernel-OOM class (`fe6faa94…`), demoting the OOM alert because a unit notice is not an authenticated unique victim.
   - Verifier finding: *"Structured selection is better than unsafe text matching, but it does not require discarding the OOM warning/DRIFT behavior; a notice need not identify a unique victim to be reported as an OOM warning."*
2. **Fleet/Non-Fleet Semantics & Adjacent Ownership Lost:**
   - Pre-r13 frozen `probe_journal`:887–908 split fleet unit failures (`UNIT_FAILURE_JOURNAL scope=fleet-units`) from desktop/OS failures (`UNIT_FAILURE_OUT_OF_SCOPE info note=non-fleet units (desktop/OS) — tsukuroi owns these`).
   - Delivered r13 `tools/mori-census.sh:1101–1102` reused `UNIT_FAILURE_JOURNAL` for all user-unit results and reported system-unit results without fleet classification or owner label.
   - Verifier finding: *"The new text honestly says 'no fleet classification', but that is a loss of the prior distinction and of named adjacent-owner context, not adjacency unchanged."*
3. **Overbroad Unknown Reason:**
   - Delivered r13 `tools/mori-census.sh:1041,1127` attributed `other_signals,other_unit_failure_text` to `no-anchored-structured-field`.
   - Verifier finding: S035 and S036 demonstrate that `UNIT_RESULT`, `EXIT_CODE`, and decimal `EXIT_STATUS` exist as anchored structured fields; describing unimplemented structured classes as categorically lacking structured fields was overbroad.

### 2.2 Quality Criteria Grounding
- **Q29 (`corpus/QUALITY.md:71`):** Requires no-harm alarm/severity+owner equivalence after selector cutover. Replaces cannot discard prior alarms or drop tsukuroi ownership routing.
- **Q30 (`corpus/QUALITY.md:72`):** Requires reading the subject's own `UNIT`/`USER_UNIT` structured metadata, never manager emitter fields (`_SYSTEMD_UNIT`/`_SYSTEMD_USER_UNIT`). Missing, malformed, or unreadable subject metadata must be explicit `UNKNOWN`/unavailable, never defaulted to non-fleet or zero.
- **Q31 (`corpus/QUALITY.md:73`):** Requires PROTOCOL §Gate standard registration and self-test verification on delivered bytes.
- **Q32 (`corpus/QUALITY.md:74`):** Requires precise qualification of mutation provenance (whole-function transplant vs. reconstructed shim).

---

## 3. Restored Coverage vs. Genuinely New Expansion (Avoiding Row-Count Learning)

A central requirement of Round 14 is to distinguish what is **restored coverage** from what is **genuinely new expansion**, while strictly avoiding "row-count learning".

### 3.1 Delineation Matrix

| Capability Dimension | Pre-R13 State (Frozen `3da5b098`) | R13 Delivered (`39abda0a`) | R14 Repaired Target | Classification |
|:---|:---|:---|:---|:---|
| **Kernel OOM Alarm** | Critical `OOM_KILL_JOURNAL` (`st=drift`) via raw `MESSAGE` regex (`c_oom`). | Demoted to `info`; no OOM finding emitted; roll stays `CLEAN`. | Critical `OOM_KILL_JOURNAL` (`st=drift`) emitted when catalog `fe6faa94…` or `UNIT_RESULT=oom-kill` > 0. | **Restored Coverage** (repairs r13 alarm harm; not new ground). |
| **Fleet Unit Failure Routing** | Regex substring match (`shokunin\|ufo-sighting\|…`) on multi-line text `MESSAGE`. | All user failures lumped into `UNIT_FAILURE_JOURNAL` ("no fleet classification"). | Structured regex matching on validated `UNIT` / `USER_UNIT` fields only. | **Restored Coverage & Precision** (restores lost partition). |
| **Non-Fleet Unit Routing** | Emits `UNIT_FAILURE_OUT_OF_SCOPE info` naming `tsukuroi` as owner. | Eliminated entirely; 0 emissions. | Emits `UNIT_FAILURE_OUT_OF_SCOPE info owner=tsukuroi` for valid non-fleet units. | **Restored Coverage** (repairs r13 adjacency harm). |
| **Structured Unit Subject Extraction** | None (unstructured regex on multi-line text output). | None (queries suppressed all subject fields, requesting only `_BOOT_ID,MESSAGE_ID`). | Queries extract `UNIT` (system) and `USER_UNIT` (user) from JSON objects without `MESSAGE`. | **Genuinely New Expansion** (structured field adoption). |
| **Subject vs. Emitter Isolation** | None (text matching could hit manager log text). | None (no subject or emitter parsed). | Explicitly consumes `UNIT`/`USER_UNIT` while rejecting manager fields `_SYSTEMD_UNIT`/`_SYSTEMD_USER_UNIT`. | **Genuinely New Expansion** (prevents manager false positives). |
| **Tri-State Classification Contract** | Two-state text partition (`fleet` vs `out-of-scope`). | Zero-state (all failures lumped). | Tri-state: `Fleet` vs `Non-Fleet (tsukuroi)` vs `UNKNOWN/unavailable` (missing/malformed). | **Genuinely New Expansion** (honest boundary per Q30). |
| **`UNIT_RESULT=oom-kill` Accounting** | Imprecise text regex (`Failed with result .signal|SIGKILL`). | Unmeasured (`classes=other_signals,other_unit_failure_text`). | Structured extraction of `UNIT_RESULT=oom-kill` from `d9b373ed…` failure records. | **Genuinely New Expansion** (structured exit-plane capture). |
| **Dual-Scope Counter Integrity** | Single user scope text scan; system scope unobserved. | 2 explicitly scoped surfaces (`journal.user`, `journal.system`), 6 counters each. | Preserved: 2 surfaces, 6 scoped counters each, strictly un-summed. | **Preserved R13 Gain** (retained without regression). |

### 3.2 The Anti-Pattern: Avoiding Row-Count Learning
- **The Pitfall:** In Round 13, the addition of S035 and S036 increased the registry row count from 34 to 36. However, as noted in `corpus/lessons/round-13-verifier-spotcheck.md:126–128`:
  *"New sourced knowledge and working separately scoped journal counters enter FR1 notice/result-plane ground; two new A rows are not themselves the evidence of learning."*
- **The Principle:** Sourced learning is measured by:
  1. Faithfully operationalizing source semantics (e.g. implementing `UNIT`/`USER_UNIT` extraction as defined in systemd documentation).
  2. Respecting negative boundaries (e.g. recognizing that S013 catalog records explicitly state memory pressure might or might not have been caused by `@UNIT@`).
  3. Enforcing trust boundaries (distinguishing client-set payload fields from trusted underscore fields).
  4. Preserving behavioral invariants across cutovers (Q29).
- Merely incrementing `SOURCES.md` row count (36 → 37) or counting source lines does not constitute evidence of learning or coverage improvement.

---

## 4. Mapping Restored Structured Unit Subject Metadata Knowledge to FR1 Scope

### 4.1 Canonical Scope of FR1
- **Current Definition (`PROVINCE.md:31`, `corpus/README.md:285`):**
  - Title: `FR1 — Kernel OOM event-time attribution and fleet correlation`
  - First evidence: `corpus/knowledge/kernel-oom-line-attribution-r12.md:10–16`; `corpus/knowledge/audit-r11.md:203–204`.
  - Boundary: System-journal structured unit notice records advanced in Round 13; kernel victim/summary token validation and fleet task correlation remain frontier.

### 4.2 What Advances into Core Ground in Round 14
Round 14 advances the following capabilities into settled **Core Ground**:
1. **Structured Unit Subject Attribution:**
   - Utilizing `UNIT` (system scope) and `USER_UNIT` (user scope) metadata emitted by `unit_log_failure()` and `unit_log_process_exit()` (S036) and documented in `systemd.journal-fields(7)` (S015/S037) to classify failed units without reading `MESSAGE`.
   - Routing unit failures deterministically between fleet health (`UNIT_FAILURE_JOURNAL`) and adjacent OS triage (`UNIT_FAILURE_OUT_OF_SCOPE owner=tsukuroi`).
   - Explicitly isolating unclassifiable, missing, or malformed unit metadata as `UNKNOWN`/`unavailable` (Q30).
2. **Dual-Trigger Structured OOM Alarm Restoration:**
   - Emitting `OOM_KILL_JOURNAL crit => DRIFT` based on positive structured kernel OOM unit notices (`fe6faa94…`) OR positive unit failure results (`UNIT_RESULT=oom-kill`).
   - Restoring the mint demand for critical OOM alerting while maintaining zero `MESSAGE` scraping.

### 4.3 What MUST Remain on the FR1 Frontier (Cannot Be Absorbed into Core)
The following boundaries define what remains unresolved on the Frontier and must **not** be claimed as settled by Round 14:
1. **Kernel OOM Victim Line Attribution:**
   - Linux kernel 7.2 source `mm/oom_kill.c:447–453` (`dump_oom_victim`) and `memcontrol.c:1820–1826` (`mem_cgroup_print_oom_context`) emit:
     `oom-kill:constraint=…,task=%s,pid=%d,uid=%d`
     `…,task_memcg=…,oom_memcg=…`
   - These are kernel log messages (`_TRANSPORT=kernel`), not systemd catalog notices.
   - Reading these fields requires token shape-validation (decimal PID/UID, sanitized cgroup path) to satisfy the "never echo raw `MESSAGE`" constraint.
   - Round 14 queries read systemd catalog IDs and unit metadata; they do not parse or validate kernel victim line tokens.
2. **Cardinality Disconnect (Notice / Unit Result $\neq$ Unique Kernel Victim):**
   - Empirical observation (`corpus/knowledge/kill-classes-by-message-id-r12.md:15–16`): In boot `7bd93aee…`, there were exactly 5 kernel `Killed process` records, yet 7 user notices and 9 system notices.
   - A unit notice indicates that systemd observed a kill affecting a unit; it is subject to multi-unit fan-out (parent slices, root scopes).
   - Furthermore, `S013` explicitly cautions: *"Note that the memory pressure might or might not have been caused by @UNIT@"*.
   - Unit-level records do not establish a 1:1 process kill count or unique victim count.
3. **Fleet Causal Attribution:**
   - A host-level unit failure or kernel OOM notice does not prove that a specific shokunin fleet agent or wave caused the OOM.
   - Correlating host events with fleet task execution requires event-time `task_memcg` / slice matching against active watchdog and wave registers.
   - Re-reading cgroups post-mortem fails (`ENOENT`, QUALITY 18).

---

## 5. Non-Obvious Move: Compatible Synthesis Across Round 14 Proposals

### 5.1 The Tensions in Round 14 Proposals
A review of the active round proposals reveals three competing tensions:
- **Tension A (Alarm vs. Count Purity):** `CensusRepair` must restore the critical OOM alarm (`OOM_KILL_JOURNAL crit => DRIFT`) without breaking the six scoped counters or conflating unit notices with unique victim counts.
- **Tension B (Unit Routing vs. Manager Emitter False Positives):** `RoutingAttack` and `JournalFields` warn that using manager emitter fields (`_SYSTEMD_UNIT`, `_SYSTEMD_USER_UNIT`) will misclassify the manager daemon (e.g. `user@1000.service`) as the failed unit. Furthermore, `QualityCriteria` (Q30) insists that missing metadata must never be defaulted to non-fleet or zero.
- **Tension C (Categorical Unknown Overreach):** `SignalCoverage` demonstrates that attributing unmeasured signals to `no-anchored-structured-field` is false, but warns against claiming arbitrary signal detection.

### 5.2 The Compatible Synthesis Proposal
The non-obvious move is **A Tri-State Subject Classification Contract with Decoupled Dual-Trigger OOM Alerting and Orthogonal Failure Ownership Routing**.

```
                           +---------------------------------------+
                           |  Raw Journal Entry (JSON Object)      |
                           +---------------------------------------+
                                              |
                     +------------------------+------------------------+
                     |                                                 |
                     v                                                 v
      [ OOM Alarm Evaluation ]                           [ Unit Subject Routing ]
  Does entry match either:                          Read UNIT or USER_UNIT independent
   a) MESSAGE_ID = fe6faa94... (kernel OOM)          of journal scope; reject manager
   b) UNIT_RESULT = oom-kill                         _SYSTEMD_UNIT / _SYSTEMD_USER_UNIT.
                     |                                                 |
                     |                              Both fields present -> UNKNOWN
                     |                              (even when identical; exactly
                     |                               one valid field accepted)
                     v                                                 v
        +------------+------------+                      [ Tri-State Validation ]
        |                         |                                    |
     YES (count > 0)             NO                     +--------------+--------------+
        |                         |                     |              |              |
        v                         v                     v              v              v
  Emit Finding:              Maintain roll        Matches Fleet   Valid Non-Fleet   Missing, Empty,
  OOM_KILL_JOURNAL           (st = CLEAN          Pattern:        Unit Name:        Array, or Both:
  severity = crit            unless other         shokunin|...    Emit Finding:     Emit Finding:
  effect = DRIFT             alarms fire)         Emit Finding:   UNIT_FAILURE_     UNIT_FAILURE_
  (scoped-counter-contract                        UNIT_FAILURE_   OUT_OF_SCOPE      UNATTRIBUTED_
   l1_interface_ruling)                           JOURNAL         severity=info     JOURNAL
                                                  severity=info   owner=tsukuroi    severity=info
                                                  scope=fleet     scope=non-fleet   owner=unresolved
```

#### Step 1: Scope-Independent Subject Classification Contract (Durable Contract Aligned)
Durable authority: `.ufo/waves/round-14/scoped-counter-contract.json` (`l1_interface_ruling`). To eliminate drift, the implementation contract is bound directly to the durable interface ruling:
1. **Query fields:** Queries request both `UNIT` and `USER_UNIT` in `--output-fields` across both `--user` and `--system` scopes.
2. **Subject selection (`l1_interface_ruling.subject_selection`):**
   - Accept exactly one valid `UNIT` or `USER_UNIT` field, independent of journal scope; do not assume journal scope determines field. (e.g. `--system` scope queries may include `USER_UNIT` manager subjects).
   - **No permissive identical exception:** If **BOTH** `UNIT` and `USER_UNIT` fields are present, the subject is classified as unknown **even when identical**. Exactly one valid subject field is accepted.
   - **No emitter fallback:** Manager emitter fields (`_SYSTEMD_UNIT`, `_SYSTEMD_USER_UNIT`) describe the logging manager daemon, not the failed subject unit, and are strictly ignored for unit failure subject attribution.
3. **Token validation:** Must be a non-empty string. If serialized as a JSON array (multi-valued journal field per S014:215), empty, or malformed, it is flagged as unparseable.
4. **Tri-State Partition:**
   - **State 1 (Fleet Unit):** Selected unit name matches historical case-insensitive token regex `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet` (`l1_interface_ruling.rule`). Emits `UNIT_FAILURE_JOURNAL` with `scope=fleet-units`, severity `info`.
   - **State 2 (Non-Fleet Unit):** Selected unit name is a valid string but does NOT match the fleet pattern (e.g. `pipewire-pulse.service`, `cups.service`). Emits `UNIT_FAILURE_OUT_OF_SCOPE` with `scope=non-fleet`, severity `info`, and explicit owner label `owner=tsukuroi`.
   - **State 3 (Unattributed / UNKNOWN — `l1_interface_ruling.unknown_subject`):** Subject field is missing, empty, an array, or both `UNIT` and `USER_UNIT` are present (even if identical). Emits `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` with severity `info`, `scope=user|system`, `count=N`, `owner=unresolved`, `reason=subject-metadata-unknown`. Never defaulted to tsukuroi (preventing false OS triage bleed) and never defaulted to fleet or zero (satisfying Q30).

#### Step 2: Decoupled Dual-Trigger OOM Alarm
1. The critical OOM alert `OOM_KILL_JOURNAL crit => DRIFT` fires if *either* of two independent structured conditions occurs in either user or system scope:
   - Condition A: Positive count of catalog `fe6faa94…` (`kernel_oom_notice > 0`).
   - Condition B: Positive count of unit termination records carrying `UNIT_RESULT=oom-kill` (`unit_failure_record > 0` with `UNIT_RESULT=oom-kill`).
2. Decoupling ensures:
   - **Zero Alarm Suppression:** If a kernel notice is lost due to log rotation or rate-limiting (`e9bf28e6…`), but a systemd service enters `failed` with `UNIT_RESULT=oom-kill`, the critical OOM alarm still fires.
   - **Counter Independence:** Scoped counters for `kernel_oom_notice` and `unit_failure_record` remain distinct, un-summed numbers.
   - **Orthogonal Ownership:** A unit failure caused by OOM still undergoes Step 1 subject routing to determine whether it is a fleet unit failure or an adjacent tsukuroi failure.

#### Step 3: Refined Categorical Unmeasured Reasons
Replace the overbroad `reason=no-anchored-structured-field` at `:1041` and `:1127` with precise, truthful classifications:
- `unimplemented_structured_signals=other_signals` (signals not having retained exit records; S035/S036 define exit records, but not all signals generate them).
- `retired_heuristics=gpf_text,unanchored_oom_text` (unstructured text regexes retired per Q15).
- `unrecorded_events=absent_records` (arbitrary processes killed outside systemd managers leave no journal record).

---

## 6. Source Registry & README Review: Immutable Scope Recommendation

### 6.1 Audit of Existing Sources Registry (`corpus/SOURCES.md`)
- Total rows: **36** (S001–S036).
- Tiers: A: 33, B: 2 (S021, S029), C: 1 (S030).
- Status: mined: 15, queued: 20, rejected: 1 (S030).
- Relevant active sources:
  - `S013`: systemd message catalog (`cf8ebfc6…`). Covers `fe6faa94…` kernel OOM notice, `d989611b…` oomd notice, `fc2e22bc…` coredump.
  - `S014`: `journalctl(1)`. Covers `--system`, `--user`, `-o json`, `--output-fields=`.
  - `S015`: `systemd.journal-fields(7)`. Immutable scope: `journal MESSAGE, MESSAGE_ID and trusted metadata fields`. Anchor: `User Journal Fields > MESSAGE=:32-39 and MESSAGE_ID=:41-44; Trusted Journal Fields > _TRANSPORT=:204`.
  - `S035`: systemd process-exit and unit-result catalog (`cf8ebfc6…`). Covers `d9b373ed…` (`UNIT_RESULT`) and `98e32220…` (`EXIT_CODE`, `EXIT_STATUS`).
  - `S036`: systemd unit termination emitter (`src/core/unit.c:6333–6392`). Covers `unit_log_failure` and `unit_log_process_exit`.

### 6.2 The Need for a New Immutable Scope: Proposed `S037`
- **The Constraint:** Under contract v1 rules, established registry cells (`id`, `source`, `kind`, `tier`, `scope`, `anchor`) are immutable. S015's existing anchor and scope cover only `MESSAGE`, `MESSAGE_ID`, and `_TRANSPORT`; they do *not* cover `UNIT=` and `USER_UNIT=`.
- **The Recommendation:** In accordance with `corpus/lessons/round-14.md:49–54`, recommend adding a new immutable row **`S037`**:

| Field | Recommended Value |
|:---|:---|
| **id** | `S037` |
| **source** | `systemd.journal-fields(7) — https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html` |
| **kind** | `docs` |
| **tier** | `A` |
| **scope** | `User Journal Fields > UNIT=, USER_UNIT= subject metadata for unit attribution` |
| **anchor** | `User Journal Fields > UNIT= and USER_UNIT=; systemd 262 man page opened 2026-10-20` |
| **teaches** | `UNIT` and `USER_UNIT` provide the specific unit subject identifier, distinct from manager emitter fields (`_SYSTEMD_UNIT`, `_SYSTEMD_USER_UNIT`). |
| **status** | `mined` |
| **opened** | `2026-10-20` |
| **recheck** | `on-release` |
| **used-by** | `corpus/knowledge/journal-alarm-routing-r14.md` |

- **Located Quote (13 words, ≤25 words):**
  *"Used by the system and user managers when logging about specific units."*
  (Location: `systemd.journal-fields(7)`, User Journal Fields → `UNIT=, USER_UNIT=`).
- **Additional Note on Gap A (`SourcesScribe.md`):** `SourcesScribe` noted that `sd-messages.h` and `process-util.c:2306–2309` (`CLD_KILLED` mapping) are cited in knowledge without an S-row. If L1 requires an explicit row for `CLD_KILLED`, it can be queued as `S038` without conflicting with `S037`.

### 6.3 Recommended Contract Updates for `PROVINCE.md` & `README.md`

#### A. Updates to `PROVINCE.md`
**Under `## Core` (line 24):**
- *Current text:*
  ```markdown
  - **Kill/OOM classes** — structured, MESSAGE-free journal records carrying catalog IDs for kernel-OOM unit notices, oomd notices, coredumps, unit-process SIGKILL results and unit failures, plus a distinct numeric signal-11 coredump count; independently labeled user/system scopes, never summed. `SURFACE cgroup` retains kernel memory-event counters. Journal IDs are client-set, not authenticated producer identity; records are not unique victims or fleet-cause attribution. Arbitrary signals without these records remain unmeasured.
  ```
- *Recommended replacement:*
  ```markdown
  - **Kill/OOM classes** — structured, MESSAGE-free journal records carrying catalog IDs for kernel-OOM unit notices (emitting critical OOM_KILL_JOURNAL => DRIFT), oomd notices, coredumps, unit-process SIGKILL results, and unit failures partitioned via structured UNIT/USER_UNIT subject metadata into fleet-units (UNIT_FAILURE_JOURNAL) and non-fleet OS triage (UNIT_FAILURE_OUT_OF_SCOPE owner=tsukuroi, with unclassifiable units explicit UNKNOWN); plus distinct numeric signal-11 coredump counts; independently labeled user/system scopes, never summed. `SURFACE cgroup` retains kernel memory-event counters. Journal IDs are client-set, not authenticated producer identity; records are not unique victims or fleet-cause attribution. Arbitrary signals without these records remain unmeasured.
  ```

**Under `## Frontier` (line 31):**
- *Current text:*
  ```markdown
  - **FR1 — Kernel OOM event-time attribution and fleet correlation** (state F1/F8 + art F2). First evidence: `corpus/knowledge/kernel-oom-line-attribution-r12.md:10-16`; `corpus/knowledge/audit-r11.md:203-204`. Round 13 advances structured system-journal notice records to Core; event-time kernel summary/victim token validation and fleet correlation remain frontier. No raw `MESSAGE` is emitted, and a host record alone does not prove a fleet-caused kill.
  ```
- *Recommended replacement:*
  ```markdown
  - **FR1 — Kernel OOM event-time attribution and fleet correlation** (state F1/F8 + art F2). First evidence: `corpus/knowledge/kernel-oom-line-attribution-r12.md:10-16`; `corpus/knowledge/audit-r11.md:203-204`. Round 13 advanced dual-scope notice counts; Round 14 advances structured UNIT/USER_UNIT subject triage routing and dual-trigger OOM alarms to Core. Boundary remaining on Frontier: parsing event-time kernel OOM summary and victim lines (task_memcg, PID, UID from mm/oom_kill.c and memcontrol.c) requires strict token-shape validation without echoing MESSAGE; catalog records do not establish unique victim counts; and post-event cgroup lookup cannot restore deleted victim paths.
  ```

#### B. Updates to `corpus/README.md`
**Under `## Frontier` Table (line 285):**
- *Current text:*
  ```markdown
  | FR1 | Kernel OOM event-time attribution and fleet correlation | `knowledge/kernel-oom-line-attribution-r12.md:10-16`; `knowledge/audit-r11.md:203-204` | Structured system-journal notice records advance round 13; kernel victim/summary token validation and fleet task correlation remain frontier. Catalog-ID records are not authenticated unique kills. |
  ```
- *Recommended replacement:*
  ```markdown
  | FR1 | Kernel OOM event-time attribution and fleet correlation | `knowledge/kernel-oom-line-attribution-r12.md:10-16`; `knowledge/audit-r11.md:203-204` | Structured unit subject routing and dual-trigger OOM alarms advance round 14; event-time kernel victim token parsing (task_memcg, PID, UID) and fleet task causal correlation remain on frontier. |
  ```

#### C. Updates to Root `README.md`
**Under `## What's here` (Domain summary):**
- Reaffirm detection-only scope: mori detects and reports fleet liveness, settlement, kill/OOM events, and resource runway; routes non-fleet unit failures to `tsukuroi` without performing OS remediation.

---

## 7. Second-Order Effects Across Surfaces

1. **Runtime Surface (`tools/mori-census.sh`):**
   - Adding `UNIT` and `USER_UNIT` to `journalctl --output-fields` increases JSON payload slightly (approx. 20–40 bytes per failure record).
   - Because queries already filter by `MESSAGE_ID` and current boot, the row count is identical; query execution time remains well within `MORI_JOURNAL_TIMEOUT_S=2`.
   - `DRIFT_COUNTER_KEYS` must retain masking for all scoped counter keys to preserve drift pin stability.
2. **Contract Surface (`PROVINCE.md`, `SKILL.md`):**
   - Preserves strict detection-only boundary. Routing non-fleet failures to `tsukuroi` informs operator/adjacent lane triage without performing OS remediation.
   - Eliminates the contradiction where mori claimed to observe fleet health while reporting `pipewire-pulse.service` core dumps as fleet failures.
3. **Substrate Surface (`journald` / systemd):**
   - Consuming `UNIT` and `USER_UNIT` relies on systemd manager convention (S036/S037). If systemd changes field names or serializes arrays, mori's tri-state validation safely degrades to `UNKNOWN` rather than crashing or misrouting.
4. **Verification Surface (`tools/mori-round14-regressions.py`):**
   - Strict-mode harness execution can assert red-before on entering commit `dbe85009` (asserting failure due to missing `OOM_KILL_JOURNAL` and missing `UNIT_FAILURE_OUT_OF_SCOPE`) and green-after on repaired commit.
   - Harness registered in `SKILL.md` satisfies PROTOCOL §Gate standard (resolving G1–G11 gaps identified by `GateConformance`).

---

## 8. Risks and Verification Checklist for L1

### 8.1 Risks & Mitigation

| Risk ID | Risk Description | Severity | Mitigation Strategy |
|:---|:---|:---|:---|
| **R1** | **Manager Emitter Confusion:** Reading `_SYSTEMD_UNIT` instead of `UNIT` causes manager services (e.g. `systemd`, `user@1000.service`) to be classified as failed units. | High | Strict field selection: examine `UNIT` / `USER_UNIT` only. Reject all underscore-prefixed emitter fields for subject classification (Q30). |
| **R2** | **Array Serialization Failure:** Systemd multi-valued fields serialize as JSON arrays, breaking string equality checks. | Medium | Tri-state validator tests `type == "string"`. Non-string or array types fall back immediately to `UNKNOWN/unavailable` without crashing. |
| **R3** | **Double-Counting OOM Alarms:** Both `fe6faa94…` notice and `UNIT_RESULT=oom-kill` record present for same kill event, leading to duplicate count expectations. | Medium | Decoupled trigger: the roll flips to `DRIFT` if `total_oom_events > 0`. Individual counter cells (`kernel_oom_notice`, `unit_failure_record`) retain distinct scoped counts and are never summed. |
| **R4** | **Silent Fallback to Non-Fleet:** Malformed fleet units being misclassified as non-fleet and routed to tsukuroi. | High | Enforce Tri-State classification: missing or malformed unit metadata routes to `UNKNOWN`, never to `tsukuroi` (Q30). |
| **R5** | **Row-Count Learning Trap:** Relying on adding S037 to claim coverage progress without demonstrating behavioral test passes. | High | L1 verification must rely strictly on red-before/green-after behavioral execution receipts, not source table row counts. |

### 8.2 Verification Checklist for L1 (Single Execution Post-Integration)
*Note: As a leaf member, this seat executes no verification runs. The commands below are provided for L1 to run once after all wave changes land.*

1. **Static Emitter & Syntax Audit:**
   ```bash
   # Confirm OOM critical alarm emission is present
   grep -n 'emit_finding OOM_KILL_JOURNAL crit' /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh
   # Confirm non-fleet tsukuroi routing emission is present
   grep -n 'emit_finding UNIT_FAILURE_OUT_OF_SCOPE info' /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh
   # Confirm fleet-only unit failure emission is present
   grep -n 'emit_finding UNIT_FAILURE_JOURNAL info' /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh
   ```
2. **Behavioral Red-Before / Green-After Regression:**
   ```bash
   # Red-before verification against frozen entering census
   python3 tools/mori-round14-regressions.py --census .ufo/waves/round-14/frozen/mori-census.sh --output .ufo/waves/round-14/evidence/regressions-before
   # Expected exit code: 1 (fails on missing OOM alarm and missing tsukuroi routing)

   # Green-after verification against repaired census
   python3 tools/mori-round14-regressions.py --census tools/mori-census.sh --output .ufo/waves/round-14/evidence/regressions-accepted
   # Expected exit code: 0 (all claims pass)
   ```
3. **Census Selftest on Delivered Bytes:**
   ```bash
   bash tools/mori-census.sh --selftest
   # Expected: PASS (asserts exact exit code and finding IDs across fixtures)
   ```
4. **SOURCES Registry Census Validation:**
   ```bash
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
   # Expected exit code: 0
   ```
5. **No `MESSAGE` Leakage Audit:**
   ```bash
   # Verify captured census output contains zero unescaped MESSAGE payload text
   grep -cE '"MESSAGE"[[:space:]]*:|(^|[^_])MESSAGE=' .ufo/waves/round-14/evidence/regressions-accepted/runs/*.stdout
   # Expected: 0
   ```

---

## 9. Conclusion & Epistemic Status of Verdicts

### 9.1 Epistemic Status (Proposals vs. Observed Code)
- **Role Boundary:** As a leaf connector seat (`SourceFrontier`), this analysis derives and presents architectural recommendations, source mappings, and candidate criteria.
- **Verdicts are Proposals:** Current verdicts, axis trend impacts, and score proposals are recommendations, not observed runtime behavior or certified passes.
- **L1 Sole Authority:** In accordance with UFO-FSD protocol, L1 alone holds post-integration verification authority and will decide final axis evaluations and trend verdicts only after all changes land and behavior is measured across the regression gate and live receipts.

### 9.2 Synthesis Summary
The synthesis outlines how to resolve the Round 13 admission harm cleanly:
- Restores critical `OOM_KILL_JOURNAL` alerting (`crit => DRIFT`) and fleet/non-fleet triage routing (`UNIT_FAILURE_JOURNAL` vs `UNIT_FAILURE_OUT_OF_SCOPE owner=tsukuroi`) as **restored coverage**.
- Implements scope-independent structured unit subject classification bound to `.ufo/waves/round-14/scoped-counter-contract.json` (`l1_interface_ruling`): exactly one valid `UNIT` or `USER_UNIT` accepted (both present is unknown even when identical; no permissive identical exception), strict emitter isolation, and explicit `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` handling for missing or multiple fields as **genuinely new expansion**.
- Re-anchors the FR1 Frontier to event-time kernel victim token parsing (`task_memcg`, PID, UID) and fleet task causal correlation, preventing overclaiming while maintaining zero `MESSAGE` scraping.
