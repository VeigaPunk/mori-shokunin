# ConnectFrontier — Round 15 Cross-Axis Review & Frontier Connection

**Seat:** `MoriR15.ConnectFrontier`  
**Role:** UFO-FSD Connector (report-only, leaf member)  
**Judged on:** `coverage` (owned axis 6)  
**Milestone:** retain validated positives without fabricated totals  
**Lane root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  

---

## 1. Named Axes (Godspeed Step 1)

1. **coverage** (owned axis, score 6 held): primary judged axis. C1 goal: preserve critical OOM and user signal alarms from individually valid current-boot structured records even when an adjacent malformed, nonmatching, or foreign-boot record invalidates the aggregate class.
2. **operability** (owned axis, score 7 held): constraint. No new journal queries, no unbounded subprocess multiplication, no regression in existing selftest/oracle suites, and no fabricated numeric zeros.
3. **depth** (observed, score 5 held): grounded in reopened sources S014, S015, S037, S038; distinguishing unit-manager notices from kernel victims.
4. **freshness** (observed, score 5 held): re-evaluating live query behavior while preserving unmeasured status where appropriate; drift pin redness remains recognized conformance debt.
5. **calibration** (observed, score 5 held): honest unavailability semantics; avoiding overclaims of authenticated IDs or unique victims.
6. **adjacency** (observed, score 6 held): strict diagnostic/reporting boundaries; tsukuroi non-fleet routing and kumitate passive wave settlement preserved without actuation.

---

## 2. Evidence & Current State (Grounding in Local Repo & Round Cache)

### 2.1 Code Anchors in Current Production (`tools/mori-census.sh` @ `0e41cb83…`)
- **Lines 973–976 (`JOURNAL_JQ_TAIL`, `_MSGID`, `_SIGKILL`, `_SIGSEGV`) & 1019–1037 (`JOURNAL_JQ_UNITS`):**  
  Every structured journal parser starts with an all-or-nothing aggregate gate:
  ```jq
  if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and (._BOOT_ID == $boot) and (.MESSAGE_ID == $id))
  ```
  If any single record in the captured JSON array fails the predicate (e.g. foreign `_BOOT_ID`, array-typed `MESSAGE_ID`, malformed field), the filter immediately evaluates to a bare status string (`record-invalid`, `boot-mismatch`, `multi-boot`).
- **Lines 1083–1105 (`journal_query`):**  
  On receiving `record-invalid|multi-boot|boot-mismatch` at line 1104, `journal_query` returns early without populating `JQ_N` or `JQ_VEC`. The entire record stream is discarded.
- **Lines 1202–1217 (`probe_journal`):**  
  Unit-failure split counters (`ucnt[...]`) are populated **only** when `JQ_STATUS=ok`.
- **Lines 1303–1321 & 1330–1332 (OOM alarm gate):**  
  `ko` and `uo` are set to `unavailable:${js[$key]}` when status is not `ok`. Consequently, `oom_fire` is never set to 1. A valid current-boot kernel OOM notice (`fe6faa94…`) or unit failure with `UNIT_RESULT=oom-kill` (`d9b373ed…`) sitting adjacent to an invalid record is completely silenced! The census emits `MORI_CENSUS: CLEAN` despite an active OOM.
- **Lines 1340–1354 (User KILL_SIGNAL warn gate):**  
  `ps` and `us` fall back to `unavailable:*`, silently dropping the user signal warning when an adjacent record invalidates the class.

### 2.2 Sourced Knowledge Anchors
- **S014 (`journalctl(1)`):** Output options `--output-fields` restrict emitted fields, but filtering options (`MESSAGE_ID=`, `EXIT_CODE=`, `EXIT_STATUS=`) do not isolate scalar types or prevent malformed records from entering the JSON array.
- **S015 (`systemd.journal-fields(7)`):** Explicit distinction between User Journal Fields (`MESSAGE_ID`, `UNIT`, `USER_UNIT`, `EXIT_STATUS`) which are client-supplied, and Trusted Journal Fields (`_BOOT_ID`, `_SYSTEMD_UNIT`).
- **S037 (`systemd subject-unit journal metadata`):** `UNIT`/`USER_UNIT` describe the subject of the log record; trusted `_SYSTEMD_UNIT` describes the logging process.
- **S038 (`systemd service result vocabulary`):** `[SERVICE_FAILURE_OOM_KILL] = "oom-kill"` from `src/core/service.c:6598`.

### 2.3 Historical Residuals & Round Cache Evidence
- **`corpus/lessons/round-14-verifier-spotcheck.md:98, 137`:** The outside verifier noted: *"Class-wide invalidation remains a serious, disclosed inherited limitation... A valid record inside an invalidated class can be hidden."*
- **`tools/mori-round14-regressions.py:105-109, 1552-1564`:** `R14_SEC_DUP_MSGID_MIXED` historically pinned `forbid_ids=FORBID_OOM` when a duplicate malformed MESSAGE_ID was mixed with an OOM record. This was a characterization of the defect, now directly targeted for repair by C1.
- **Peer Audits (`ReviewRouting.md`, `ReviewProcessPredicate.md`, `ReviewUnitPredicate.md`, `ReviewRawTotals.md`, `ReviewKernelPredicate.md`):** Consistently confirm that `positive_*` tokens do not exist in `tools/` and that the all-or-nothing aggregate gate is the single point of alarm suppression.

---

## 3. Mapping Knowledge Expansion to the FR1 Failure-Mode Gap

### 3.1 The Evolution of FR1 Across Rounds
- **Round 12:** FR1 was defined as kernel OOM line attribution and fleet correlation. Observability relied on fragile, unanchored regexes matching `MESSAGE` text (`kernel-oom-line-attribution-r12.md`).
- **Round 13:** Dual-scope structured queries introduced catalog `MESSAGE_ID` parsing (`fe6faa94…`, `d989611b…`, `fc2e22bc…`), eliminating `MESSAGE` scraping. However, the cutover demoted OOM notices to INFO, broke the OOM critical alarm, and collapsed the fleet/non-fleet partition.
- **Round 14:** Restored the critical `OOM_KILL_JOURNAL` alarm and structured subject routing (`UNIT`/`USER_UNIT`), but retained the **whole-stream aggregate all-or-nothing gating**.
- **Round 15 Failure-Mode Gap:**  
  In real Linux environments, journal streams are inherently dirty. A previous-boot entry lingering in an unrotated log buffer, an unprivileged process logging a client record with an array `MESSAGE_ID`, or an incomplete flush can inject non-matching records into the journal buffer.  
  Under Round 14's implementation, **stream-level aggregate invalidation acts as an alarm-suppression vulnerability**: an attacker or malfunctioning application can blind mori's critical OOM and signal detection simply by spamming a malformed journal record.

### 3.2 Sourced Resolution
By reopening S014, S015, S037, and S038, Round 15 operationalizes the exact scalar type constraints and field contracts required to **decouple alarm activation from aggregate completeness**:
- An alarm requires **positive evidence of an event** ($\ge 1$ verified record).
- An aggregate total requires **complete census validity** (all records valid and counted).
These two requirements address completely different operational needs and must not share an all-or-nothing gate.

---

## 4. Distinguishing Repair from New Frontier

To maintain contract rigor and avoid overclaiming, we must strictly separate what is **bounded repair** from what **remains on the FR1 Frontier**:

```
+----------------------------------------------------------------------------------------------------+
|                                         CORE CAPABILITY                                            |
|                                                                                                    |
|  [Round 14 Core]                                                                                   |
|  - Dual-scope structured notice counting (fe6faa94, d989611b, fc2e22bc)                            |
|  - Subject-unit triage: fleet vs non-fleet (tsukuroi) vs unattributed unknown                     |
|  - Single global OOM_KILL_JOURNAL crit finding (aggregate-gated)                                  |
|                                                                                                    |
|  [Round 15 Bounded Repair (C1)] <--- THIS ROUND's CLAIM                                            |
|  - Decouple positive event alarm activation from aggregate stream invalidation                     |
|  - Retain validated positives: positive_kernel_oom, positive_unit_oom, positive_unit_signal,         |
|    positive_process_sigkill from individually valid current-boot records                           |
|  - Raw aggregate counts STAY unavailable:record-invalid (never faked as numeric 0)                 |
|  - Explicit scalar predicate validation (rejecting arrays, nulls, non-current boots)               |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  | DOES NOT CROSS
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                         FR1 FRONTIER                                               |
|                                                                                                    |
|  [Retained on FR1 Frontier - Unsettled]                                                            |
|  1. Event-time kernel OOM victim attribution: parsing task_memcg, PID, UID from mm/oom_kill.c     |
|     and memcontrol.c without MESSAGE_ID (requires kmsg/raw log token parsing without MESSAGE text) |
|  2. Fleet task causal correlation: proving whether a host kill was caused by or damaged a fleet    |
|     task (catalog notices are client-supplied notices, not proof of causation)                     |
|  3. Arbitrary malformed JSON recovery: if jq -s fails syntax parsing, stream stays malformed-json  |
|  4. Unique victim cardinality & kill totals: notices are not deduplicated victim tallies           |
+----------------------------------------------------------------------------------------------------+
```

### Key Distinctions:
1. **Bounded Repair (Admitted to Core):**
   - Preserves critical alarms (`OOM_KILL_JOURNAL crit`, `KILL_SIGNAL_JOURNAL warn`) when positive records exist.
   - Enforces honesty: invalid aggregate counts remain `unavailable:<reason>`.
   - Hardens type checks against accidental coercions (e.g. `tostring` on arrays).
2. **Retained on Frontier (FR1 Boundary):**
   - Kernel-side victim parsing without `MESSAGE_ID` remains on FR1.
   - Fleet causal correlation remains on FR1.
   - Syntactically broken JSON lines remain unparseable (`unavailable:malformed-json`); mori does not build an ad-hoc JSON repair engine.
   - Notice counts are never claimed as unique victim counts.

---

## 5. Proposed Move: Dual-Plane Query Decomposition

### 5.1 The Synthesis
Reviewers and scouts in this round have identified several potential friction points:
- *Tension 1 (ReviewRouting F5):* Adding `positive_*` tokens to `DRIFT_COUNTER_KEYS` mutates `volatile_fields`, inducing false drift against the pinned r10 baseline.
- *Tension 2 (ReviewKernelPredicate F1 vs Operability):* Running a second `jq -s` subprocess inside `journal_query` doubles subprocess execution (up to 24 `jq` invocations per census run), degrading operability.
- *Tension 3 (ReviewRawTotals F1 vs ReviewProcessPredicate 6):* `paths=` in `OOM_KILL_JOURNAL` was historically built only from raw counts; if raw is `unavailable:record-invalid`, `paths=` becomes empty unless wired to positive evidence.
- *Tension 4 (ReviewRawTotals F1):* `tools/mori-round14-regressions.py` case `R14_SEC_DUP_MSGID_MIXED` pinned the suppression of OOM on mixed streams.

### 5.2 The Non-Obvious Move
**Implement Dual-Plane Decomposition within a Single JQ Invocation while Isolating Positive Tokens from Drift Counter Keys:**

1. **Single-Pass JQ Dual-Plane Evaluation:**  
   Instead of spawning a second `jq` process over `$raw`, the jq filter evaluates both planes in a single pass:
   - **Plane A (Aggregate Partition):** Runs the existing `if all(.[]; ...)` gate. If valid, computes the full TSV vector; if invalid, sets the aggregate status (`record-invalid`, `boot-mismatch`, `multi-boot`).
   - **Plane B (Positive Witness):** Runs an independent selection:
     ```jq
     def pos_kernel: [ .[] | select(type=="object" and (._BOOT_ID?|type)=="string" and ._BOOT_ID==$boot and (.MESSAGE_ID?|type)=="string" and .MESSAGE_ID==$k_id) ] | length;
     def pos_unit_oom: [ .[] | select(type=="object" and (._BOOT_ID?|type)=="string" and ._BOOT_ID==$boot and (.MESSAGE_ID?|type)=="string" and .MESSAGE_ID==$u_id and (.UNIT_RESULT?|type)=="string" and .UNIT_RESULT=="oom-kill") ] | length;
     def pos_unit_sig: [ .[] | select(type=="object" and (._BOOT_ID?|type)=="string" and ._BOOT_ID==$boot and (.MESSAGE_ID?|type)=="string" and .MESSAGE_ID==$u_id and (.UNIT_RESULT?|type)=="string" and .UNIT_RESULT=="signal") ] | length;
     def pos_proc_sig: [ .[] | select(type=="object" and (._BOOT_ID?|type)=="string" and ._BOOT_ID==$boot and (.MESSAGE_ID?|type)=="string" and .MESSAGE_ID==$p_id and (.EXIT_CODE?|type)=="string" and .EXIT_CODE=="killed" and (((.EXIT_STATUS?|type)=="string" or (.EXIT_STATUS?|type)=="number") and (.EXIT_STATUS|tostring)=="9")) ] | length;
     ```
   - In both the valid and invalid branches, jq appends the positive counts. `journal_query` extracts `JQ_STATUS`, `JQ_N`, `JQ_VEC`, and populates `JQ_POS_K`, `JQ_POS_UO`, `JQ_POS_US`, `JQ_POS_PS`.
   - **Result:** Zero added subprocesses; operability and execution latency are preserved.

2. **Alarm Gate Synthesis (Decoupled Activation with Preserved Raw Status):**
   - `oom_fire` is set to 1 if:  
     `raw_ko > 0` OR `raw_uo > 0` OR `positive_kernel_oom > 0` OR `positive_unit_oom > 0`.
   - `oom_paths` includes `kernel_oom_notice` if `raw_ko > 0` OR `positive_kernel_oom > 0`.
   - `oom_paths` includes `unit_result_oom_kill` if `raw_uo > 0` OR `positive_unit_oom > 0`.
   - Raw fields retain their exact tokens: `user_notice=unavailable:record-invalid`, but finding fields add: `positive_kernel_oom=1 positive_unit_oom=0`.
   - `kill_fire` (user scope only) activates if:  
     `raw_ps > 0` OR `raw_us > 0` OR `positive_process_sigkill > 0` OR `positive_unit_signal > 0`.

3. **Drift Immunity (No Schema Drift):**
   - Positive evidence tokens are surfaced in finding lines and `SURFACE journal.<scope>` observation rows, but are **NOT** added to `DRIFT_COUNTER_KEYS`.
   - This ensures `tools/mori-census.sh --drift` does not suffer schema drift against the frozen r10 baseline.

---

## 6. Second-Order Effects

1. **Runtime Surface (`tools/mori-census.sh`):**
   - Capture failure handling remains absolute: if `CAP_RC != 0` or `stderr-nonempty`, positives are `unavailable:<status>`, never `0`.
   - Single OOM line guarantee (`tools/mori-census.sh:3050-3053`) is preserved: exactly one `FINDING OOM_KILL_JOURNAL crit` line emitted per census, with separate non-summed counters.
2. **Contract Surface (`PROVINCE.md`, `SKILL.md`, `corpus/README.md`):**
   - `PROVINCE.md` Core description gains structured positive alarm resilience against stream pollution.
   - FR1 Frontier text remains unchanged regarding event-time kernel attribution and fleet task causality.
   - `SKILL.md` documents the decoupled positive evidence vs unavailable aggregate interface.
3. **Substrate Surface:**
   - Evaluates systemd journal client-supplied records with strict scalar validation, defending against injection attacks (e.g. array-typed fields).
4. **Verification Surface:**
   - `tools/mori-round15-regressions.py` runs fixture packs verifying both arms: alarm fires (coverage win) AND raw aggregate stays `unavailable:record-invalid` (honesty win).
   - In `tools/mori-round14-regressions.py`, `R14_SEC_DUP_MSGID_MIXED` is explicitly re-pinned or reconciled by L1 to reflect the intentional C1 behavioral enhancement.

---

## 7. Risks and Residuals

- **Residual 1 (Syntax-Malformed JSON):** If a journal record contains unparseable raw bytes causing `jq -s` to fail syntax parsing (`jrc != 0`), `JQ_STATUS=malformed-json`. Positives become `unavailable:malformed-json`. This is compliant with the contract ("Do not repair arbitrary malformed JSON").
- **Residual 2 (Client-Supplied Authenticity):** `MESSAGE_ID`, `UNIT`, and `EXIT_STATUS` remain client-supplied fields. A positive count proves record presence, not kernel authenticity or unforgeability.
- **Residual 3 (Notice Fan-Out & Slice Attributions):** Multiple unit notices can still be emitted for a single kernel OOM event. Positives count verified records, not unique victims or total kill counts.
- **Residual 4 (Unclaimed Conformance Debt):** Pinned r10 drift baseline redness and broader oracle tally/forgery debt remain outside the round-15 claim.

---

## 8. Concrete Verification Recommendations (for L1 Post-Integration)

*Per instructions, this seat executes no tests, builds, or gates. L1 must verify the integrated tree by running:*

1. **Census Internal Selftest:**
   ```sh
   bash tools/mori-census.sh --selftest
   ```
   *Expected:* Exit 0; all existing selftest cases pass; mixed-record selftest cases verify that `OOM_KILL_JOURNAL crit` fires while raw count is `unavailable:boot-mismatch` or `unavailable:record-invalid`.
2. **Round 15 Regression Gate:**
   ```sh
   python3 tools/mori-round15-regressions.py --census tools/mori-census.sh --output .ufo/waves/round-15/evidence/r15-run
   ```
   *Expected:* Exit 0; all fixture packs in `.ufo/waves/round-15/fixtures/*.json` pass; both `want_oom=true` and raw unavailable status assertions hold.
3. **Round 14 Historical Regression Suite:**
   ```sh
   python3 tools/mori-round14-regressions.py --selftest
   python3 tools/mori-round14-regressions.py --census tools/mori-census.sh --output .ufo/waves/round-15/evidence/r14-run
   ```
   *Expected:* Clean exit, confirming no regression in historical r14 alarm/routing behavior (with `R14_SEC_DUP_MSGID_MIXED` reconciled).
4. **Silence Oracle Stability:**
   ```sh
   bash tools/mori-silence-cases.sh
   ```
   *Expected:* `MORI_SILENCE_CASES: matched=28 total=28`, exit 0.
5. **Live Census Sanity Check:**
   ```sh
   bash tools/mori-census.sh
   ```
   *Expected:* Exactly one final roll (`MORI_CENSUS: CLEAN|DRIFT`), valid exit code 0 or 1, no crash (rc 2).

---

## 9. Tooling and Host Safety Record

- **Host Safety Directive:** The parent directive concerning package management was received (`pacman -Sp` dry-run check; no `-Sy/-Syu/-U/-R`).
- **Tool Actions:** Zero tools or packages were installed, updated, or removed. No pacman commands were executed. All investigation was performed via read-only tools on local files.
