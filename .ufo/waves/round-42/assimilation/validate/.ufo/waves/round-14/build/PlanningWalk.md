# PlanningWalk — Data-Walk, Defect Counter Rubric, and UFO-FSD Connector Synthesis

- Seat: `MoriR14.PlanningWalk` (connector, leaf member, report-only).
- Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
- Assignment: Data-walk coverage/operability score active state after rejected r13; recommend C1 before→after defect counter rubric and causally bound no-harm assessment; historical score correction not score inflation; synthesize round proposals into one non-obvious move.
- Judged on: **coverage**. Milestone: **restore OOM alarm and structured fleet routing**.
- Tool installs / updates: **none**. Leaf member: no subagent dispatch, no test/build/lint runs, no git mutations, no edits outside this report.

---

## 1. Name the Axes

The six canonical axes governing `mori-shokunin`:

1. **coverage** (owned by lane, LIVE): The scope and fidelity of observed fleet-liveness and host-runway surfaces. Declared axis for round 14.
2. **operability** (owned by lane, LIVE): Reliable, deterministic execution of censuses, gates, and oracles with clean exit-code contracts, hermetic self-tests, and spoofing resistance.
3. **depth** (observed): Rigorous grounding in primary sources (Linux kernel, systemd catalog and source code, procfs/cgroup specs) rather than heuristic string grepping.
4. **freshness** (observed): Anchored temporal baselines, reproducible receipts, and drift detection over time.
5. **calibration** (observed): Truthful severity grading (avoiding alarm inflation or demotion), explicit unknown/unavailable semantics, and precise attribution of mutations.
6. **adjacency** (observed): Strict adherence to province boundaries (detection and reporting only; refusing remediation; routing OS package/unit triage to `tsukuroi` and orchestration to `kumitate`).

---

## 2. Data-Walk: Coverage and Operability Score Active State After Rejected Round 13

### 2.1 Entering Baseline vs. Claimed vs. Outside Verdict

| Axis | R12 entering baseline | R13 self-assessment | R13 outside spot-check verdict (`hyaku` closure @m_strong) | Active score entering R14 (corrected) |
|---|---|---|---|---|
| **coverage** | **6** | 6 → 7 (claimed) | **harmed** (OOM critical alert and fleet unit distinction traded away) | **6** (unadmitted point revoked; code carries defects D1–D3) |
| **operability** | **6** | 6 → 7 (claimed) | **improved** (C2 F01/F02 independently verified 2 → 0; BANANA 0/28) | **6 held (proposed conservative)** / **7 retained (L1 record)** |
| **depth** | 5 | 5 held | **unchanged** (supported C1/C2; no separate depth claim) | **5** |
| **freshness** | 5 | 5 held | **unchanged** (r10 drift baseline remains red; no re-pin) | **5** |
| **calibration** | 5 | 5 held | **unchanged** (no-harm overclaim and mutation wording require correction) | **5** |
| **adjacency** | **6** | 6 held | **harmed** (fleet/non-fleet unit distinction lost; tsukuroi routing removed) | **6** (entering baseline, but harmed in delivered r13 bytes) |

### 2.2 Historical Score Correction vs. Score Inflation

- **The Inviolable No-Harm Rule:** Under PROTOCOL §Gate and §Scoring, an improvement on one axis does not admit a harmed round (`corpus/lessons/round-13-verifier-spotcheck.md:4`). Round 13 closed with status `ok`, `admitted: false`, verdict `rejected-harmed`.
- **Coverage Correction:** The self-awarded coverage point (6 → 7) was explicitly withdrawn by L1 in `SCORECARD.md` ("The unrestricted coverage point is withdrawn: active coverage **6**, not 7"). Active coverage entering Round 14 is **6**. Pre-awarding any scalar credit for repairing a harmed round is strictly prohibited: coverage remains 6 until an admitted, harm-free round demonstrates capability expansion beyond the baseline.
- **Operability Score Status (Conservative Proposal vs. Retained Verified Score):**
  - In `SCORECARD.md` round-14 header, L1 records: `"Operability's independently verified F01/F02 improvement remains 7"`.
  - **Context & Protocol Nuance:** The score protocol does not explicitly forbid retaining an independently verified per-axis score on a rejected round (given that C2 F01/F02 improvements were independently checked and verified by hyaku closure as genuine code improvements).
  - **Proposed Conservative Choice:** While L1's draft records operability at 7, a conservative posture to avoid any perception of score inflation before Round 14 achieves an admitted, harm-free closure is to propose **holding operability at 6** (conditional upon R14 no-harm admission). This conservative choice is submitted as a recommendation for operator ruling, rather than an authoritative strict protocol decree.

---

## 3. Recommended C1 Before → After Defect Counter Rubric

### 3.1 Defect Taxonomy for C1

The outside spot-check identified three specific defects in the Round 13 delivered journal cutover (`tools/mori-census.sh:1030–1130` at `dbe8500`):

1. **Defect 1 (OOM Alarm Severity Demotion):**
   - *Entering state (`dbe8500`):* Zero occurrences of `emit_finding OOM_KILL_JOURNAL crit` in `probe_journal`. Kernel OOM notices (`fe6faa94...`) in both user and system scopes were demoted to severity `info` (`KERNEL_OOM_NOTICE_JOURNAL_USER`/`SYSTEM`), rolling `CLEAN` instead of `DRIFT`. Furthermore, `UNIT_RESULT=oom-kill` in unit failure records was completely unparsed.
   - *Repaired state (R14):* Kernel OOM notices in either user or system scope emit `OOM_KILL_JOURNAL crit` => `DRIFT`. Service units killed by OOM (`UNIT_RESULT=oom-kill` on `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c`) emit `OOM_KILL_JOURNAL crit` => `DRIFT`.
2. **Defect 2 (Fleet vs. Non-Fleet Unit Failure Routing Collapse):**
   - *Entering state (`dbe8500`):* All user unit failures emitted `UNIT_FAILURE_JOURNAL` with note `"no fleet classification"` (`:1102`). Non-fleet desktop/OS units (`pipewire-pulse.service`, etc.) were not partitioned, and zero occurrences of `emit_finding UNIT_FAILURE_OUT_OF_SCOPE` existed. Tsukuroi triage ownership was lost.
   - *Repaired state (R14):* Structured `UNIT` (system scope) or `USER_UNIT` (user scope) metadata is evaluated against the historical fleet regex (`shokunin|ufo-sighting|tmux-spawn|the-tick|fleet`). Fleet units emit `UNIT_FAILURE_JOURNAL`; non-fleet units emit `UNIT_FAILURE_OUT_OF_SCOPE info owner=tsukuroi`. Missing/malformed unit metadata emits `unknown`/`unavailable`, never falsely defaulting to non-fleet.
3. **Defect 3 (Overbroad "No-Anchored-Structured-Field" Reason):**
   - *Entering state (`dbe8500`):* Categorical emission of `JOURNAL_CLASSES_UNMEASURED info` with `reason=no-anchored-structured-field` at `:1041` and `:1127` across `oom_kill_text,other_signals,other_unit_failure_text`. Overbroad because S035/S036 demonstrate structured fields (`EXIT_CODE`, `EXIT_STATUS`, `UNIT_RESULT`) exist in systemd.
   - *Repaired state (R14):* Reason narrowed to distinguish truly unrecorded events from unimplemented structured selections and retired heuristics.

### 3.2 Before → After Defect Counter Rubric

We establish a dual rubric: static emitter count and behavioral regression test failures.

#### A. Static Defect Counter (Target: 3 → 0)

| Defect ID | Condition | Entering `dbe8500` | Repaired R14 Target | Status Delta |
|---|---|---|---|---|
| **D1: OOM Alarm** | `grep -c 'emit_finding OOM_KILL_JOURNAL crit' tools/mori-census.sh` | **0** (defect present) | **≥ 1** (defect resolved) | Defect: 1 → 0 |
| **D2: Routing** | `grep -c 'emit_finding UNIT_FAILURE_OUT_OF_SCOPE' tools/mori-census.sh` | **0** (defect present) | **≥ 1** (defect resolved) | Defect: 1 → 0 |
| **D3: Overbroad** | `grep -c 'reason=no-anchored-structured-field' tools/mori-census.sh` | **2** (defect present) | **0** (narrowed reason) | Defect: 1 → 0 |
| **Total Static Defects** | Sum of active defects | **3** | **0** | **3 → 0** |

#### B. Behavioral Defect Class Predictions via Isolated Harness (`mori-round14-regressions.py`)

*Important note on test counts:* The three entries below represent the core defect-class prediction, not an observed test execution measurement. Per `GateConformance.md` and `MutationDesign.md`, the actual delivered `mori-round14-regressions.py` test suite incorporates a larger case matrix (>3 cases, including user/system scopes independently, notice vs. result OOM triggers, fleet vs. non-fleet vs. malformed unit metadata, negative/clean controls, and mutation batteries). Any exact count of failing cases on entering `dbe8500` is a pre-run candidate prediction.

| Behavioral Defect Class | Synthetic Fixture Trigger | Expected on Repaired R14 | Predicted on Entering `dbe8500` | Status Delta (Predicted) |
|---|---|---|---|---|
| `R14_C1_OOM_NOTICE_CRIT` (user/system) | Kernel OOM notice (`fe6faa94...`) in user/system scope | `FINDING OOM_KILL_JOURNAL severity=crit` + `MORI_CENSUS: DRIFT` | Emits `info` notice finding + `MORI_CENSUS: CLEAN` | **FAIL → PASS** |
| `R14_C1_UNIT_OOM_RESULT_CRIT` (fleet/non-fleet) | Unit failure record with `UNIT_RESULT=oom-kill` on `d9b373ed...` | `FINDING OOM_KILL_JOURNAL severity=crit` + `MORI_CENSUS: DRIFT` | No OOM finding emitted; rolls `CLEAN` | **FAIL → PASS** |
| `R14_C1_NONFLEET_TSUKUROI_ROUTE` | Unit failure record with `UNIT=pipewire-pulse.service` | `FINDING UNIT_FAILURE_OUT_OF_SCOPE severity=info ... owner=tsukuroi` | Emits `UNIT_FAILURE_JOURNAL` with no fleet classification | **FAIL → PASS** |
| `R14_C1_SCOPED_COUNT_PARITY` (control) | 6 classes across 2 scopes (12 cells) | All 12 counter tokens match expected values | All 12 counter tokens match (R13 baseline) | **PASS → PASS** (Control) |
| `R14_C1_NO_MESSAGE_CANARY` (control) | Synthetic `MESSAGE` canary text | Zero canary leaks in stdout | Zero canary leaks in stdout | **PASS → PASS** (Control) |

### 3.3 Executable Verification Commands for L1

```sh
# Static emitter defect verification
python3 -c '
import subprocess, re, sys
src = subprocess.check_output(["git", "show", "HEAD:tools/mori-census.sh"], text=True)
d1 = 1 if not re.search(r"emit_finding\s+OOM_KILL_JOURNAL\s+crit", src) else 0
d2 = 1 if not re.search(r"emit_finding\s+UNIT_FAILURE_OUT_OF_SCOPE\s+info", src) else 0
d3 = 1 if "reason=no-anchored-structured-field" in src else 0
total = d1 + d2 + d3
print(f"STATIC_DEFECTS: d1_oom={d1} d2_route={d2} d3_reason={d3} total={total}")
sys.exit(total)
'

# Behavioral regression gate verification (against frozen entering dbe8500 vs. repaired target)
# Predicted on frozen entering: exit 1 (failures on un-repaired alarm/routing claims; full suite likely >3 cases)
# Predicted on repaired target: exit 0 (0 failed claims)
python3 tools/mori-round14-regressions.py --census .ufo/waves/round-14/frozen/mori-census.sh --output /tmp/r14-red

python3 tools/mori-round14-regressions.py --census tools/mori-census.sh --output /tmp/r14-green
```

---

## 4. Causally Bound No-Harm Assessment

Under PROTOCOL §Scoring, we audit the proposed C1 repair across all six axes to verify that restoring OOM alarms and fleet routing does not harm any other axis:

1. **Coverage (Declared Axis):**
   - *Gains Preserved:* Dual-scope structured journal surfaces (`journal.user` and `journal.system`), 6 boot-anchored class counters per scope (12 distinct cells), and strict MESSAGE-canary exclusion.
   - *Harm Repaired:* Restores critical OOM alarm (`OOM_KILL_JOURNAL crit => DRIFT`) for both kernel notices and unit OOM kills; restores fleet vs. non-fleet unit failure partition with explicit tsukuroi routing.
   - *No-Harm Verdict:* **IMPROVED / HARM-FREE**. No capability is traded away.
2. **Operability:**
   - *Preservation:* F01 (subject-first long-history authorship) and F02 (strict verdict roll validation) remain green and unregressed.
   - *Gate Hardening:* Both `mori-round13-regressions.py` and `mori-round14-regressions.py` registered under PROTOCOL §Gate in `SKILL.md`; self-tests execute on delivered revision bytes.
   - *No-Harm Verdict:* **UNCHANGED / IMPROVED**.
3. **Depth:**
   - Grounded directly in primary sources: S013/S035 (`systemd.catalog.in`), S036 (`unit.c`), S015/S037 (`systemd.journal-fields`). No reliance on raw string greps or heuristics.
   - *No-Harm Verdict:* **UNCHANGED (5 held)**.
4. **Freshness:**
   - Legacy r10 drift detector retained; current-commit evidence hashed and pinned in round receipts.
   - *No-Harm Verdict:* **UNCHANGED (5 held)**.
5. **Calibration:**
   - Distinguishes host pressure events from unique victims; does not inflate notice counts into victim tallies.
   - Missing unit metadata grades explicit `unknown`/`unavailable` rather than silently defaulting to non-fleet (Q30).
   - "Exact-locus" overstatement corrected to function-locus with explicit provenance (Q32).
   - *No-Harm Verdict:* **IMPROVED / UNCHANGED (5 held)**.
6. **Adjacency:**
   - Restores `UNIT_FAILURE_OUT_OF_SCOPE info owner=tsukuroi` for non-fleet units, actively upholding the refusal contract (mori reports non-fleet unit failures to tsukuroi; mori never remediates).
   - Eliminates cross-domain bleed where OS-level unit failures were labeled fleet failures.
   - *No-Harm Verdict:* **REPAIRED / UNCHANGED (6 held)**.

---

## 5. One Non-Obvious Move: Dual-Channel Structured OOM Alert Synthesis with Scope-Decoupled Fleet Triage

### 5.1 Evidence and Contradiction Observed Across Round Proposals

Reviewing the round proposals from `CensusRepair`, `JournalRegression`, `CatalogSource`, `EmitterSource`, `JournalFields`, `FleetPredicate`, `CgroupScope`, `OomAttack`, and `RoutingAttack`:

1. **Contradiction A (Notice vs. Victim Cardinality):**
   - In Round 13, the author demoted kernel OOM notices (`fe6faa94...`) to `info` because S013/catalog proves that a kernel OOM unit notice is an advisory notification, not a unique-victim counter or proof of fleet causation.
   - However, the verifier spot-check correctly noted: *"A notice need not identify a unique victim to be reported as an OOM warning."* The mint demand strictly requires `DRIFT` on OOM.
2. **Contradiction B (The Dual-Source OOM Reality):**
   - Systemd generates OOM evidence along two distinct channels:
     - **Channel 1 (Notice Channel):** `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` (catalog entry: "A process of @UNIT@ unit has been killed by the OOM killer").
     - **Channel 2 (Unit Result Channel):** `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c` (catalog entry S035: "The unit @UNIT@ has entered the 'failed' state with result '@UNIT_RESULT@'", where `UNIT_RESULT=oom-kill`).
   - If a repair only looks at Channel 1, it misses services terminated by cgroup OOM that did not emit a kernel notice in that scope.
   - If a repair looks at Channel 2 and binds it strictly to fleet routing, a non-fleet unit OOM kill (`pipewire-pulse.service`) routed to tsukuroi might suppress the host OOM alarm, violating the mint demand that *any* OOM triggers host DRIFT.
   - If both channels fire for the same kill, a naive counter would double-count the kill total.

### 5.2 The Proposed Move: Channel-Decomposed OOM Alarm with Decoupled Triage

Synthesizing these insights into one bounded, harm-free move:

1. **Unified Finding Trigger, Independent Channel Evidence:**
   - `probe_journal` emits exactly **one** `OOM_KILL_JOURNAL crit` finding per scope if `n_kernel_oom_notices > 0` OR `n_unit_oom_kills > 0`. This flips the surface to `st=drift` and rolls `MORI_CENSUS: DRIFT`, satisfying the mint demand and r12 alarm equivalence.
   - The finding payload carries explicit, unsummed channel counts:
     ```text
     FINDING OOM_KILL_JOURNAL severity=crit obs="class=oom_kill scope=user kernel_notices=N unit_oom_kills=M victim=unverified trust=client-supplied note=host memory pressure detected; not unique victim count boot=<boot_id>"
     ```
   - Kernel notice count and unit oom-kill count are **never summed into a composite total**, strictly complying with PROVINCE ("never summed kill totals; records are not unique victims").
2. **Decoupled Unit Triage Routing:**
   - Every unit failure record (`MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c`) is independently classified by reading subject `UNIT` or `USER_UNIT` metadata:
     - If matching `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet`: emit `UNIT_FAILURE_JOURNAL warn` (classifying whether `result=oom-kill` or other failed state).
     - If matching desktop/OS patterns: emit `UNIT_FAILURE_OUT_OF_SCOPE info owner=tsukuroi` with `result=<result>`.
     - If `UNIT`/`USER_UNIT` is missing, unparseable, or array-valued: emit explicit `UNIT_FAILURE_METADATA_UNAVAILABLE unavailable`, never defaulting to non-fleet.
   - **Crucial Decoupling:** Even if the failed unit is non-fleet and routed to `tsukuroi`, if its result was `oom-kill`, it STILL triggers the host `OOM_KILL_JOURNAL crit => DRIFT`. Host memory exhaustion threatens fleet execution even if the victim process belonged to the host OS.

### 5.3 Second-Order Effects Trace

- **Runtime Surface:** Zero added subprocesses or query latency. The census already queries `MESSAGE_ID=d9b373ed...` for unit failures; it simply extracts `_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT,EXIT_CODE,EXIT_STATUS` within the existing single `jq` filter.
- **Contract Surface:** Satisfies Q29 (alarm/severity preservation), Q30 (unknown for missing metadata), Q15 (no MESSAGE text), and the mint demand (`OOM_KILL_JOURNAL crit => DRIFT`).
- **Substrate Surface:** No reliance on host journal state; fully testable in hermetic synthetic fixtures.
- **Verification Surface:** Cleanly partitions test assertions in `mori-round14-regressions.py` into distinct positive fixtures:
  - Fixture A: Kernel OOM notice only (Channel 1) → verifies `OOM_KILL_JOURNAL crit`.
  - Fixture B: Unit failure with `UNIT_RESULT=oom-kill` on non-fleet unit (Channel 2) → verifies BOTH `UNIT_FAILURE_OUT_OF_SCOPE info owner=tsukuroi` AND `OOM_KILL_JOURNAL crit`.
  - Fixture C: Unit failure with `UNIT_RESULT=failed` on fleet unit → verifies `UNIT_FAILURE_JOURNAL warn` without OOM alarm.
  - Fixture D: Empty / clean journal → verifies `CLEAN` / exit 0.

### 5.4 Risks and Blockers

- **Risk 1 (Finding Identifier Churn):** Sibling tools or parsers looking for exact finding identifiers.
  - *Mitigation:* Retain the exact stable token `OOM_KILL_JOURNAL` and severity `crit`. Do not invent new compound identifiers for the primary alarm.
- **Risk 2 (Duplicate Finding Lines):** If both user and system scopes have OOM events, ensure findings carry `scope=user` and `scope=system` cleanly without duplicate un-scoped lines.
  - *Mitigation:* Follow the existing pattern `journal_finding_id "$scope" "$cls"`.
- **Blockers:** None. Pinned sources S013, S015, S035 (`d9b373ed55a64feb8242e02dbe79a49c`), S036, and S037 provide complete structural field authority.
