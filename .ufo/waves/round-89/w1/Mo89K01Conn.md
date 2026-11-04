# Mo89K01Conn — Sibling Overlap and Claim Connection Scan (Connector Report)

Seat: `Mo89K01Conn` · Lane: `mori` (fleet & host observability) · Round: 89, attempt 1  
Role: UFO-FSD Connector (leaf member; no subagent dispatch; no production or corpus mutations)  
Judged on: **adjacency**, **calibration**  
Entering revision: `30a29797012281b9fd0c748b38b929ac67f8c754`  
Frozen contract revision: `d4438695998894aad7ff9b20f46d9f1852ea3c7d`  
C1 landing revision: `760428abf925d98025b34bf23f2cbf54cbeb3bca`  
Scratch: `/fast/scratch/hyaku/mori-r89/Mo89K01Conn/` (cleaned before yield)  

---

## 1. Executive Summary

This report delivers the connector analysis for mori round 89 across four required analytical surfaces:
1. **Province Authority & Adjacency:** Evaluates whether receipt script-position validation is mori's own-evidence accounting or an encroachment on kumitate's lifecycle authority.
2. **Cross-Claim Coupling:** Maps the structural and predicate coupling between C1 (operability) and C2 (calibration) centered on `.ufo/waves/round-88/count-c2.py`.
3. **Honest Claim Axis Verdict:** Recommends retaining two distinct claim axes without scope absorption while documenting the sequential substrate dependency.
4. **Considerthese Proposal 2 Forward Tracking:** Formulates a bounded three-state disposition criterion (`FIXED`, `ROUTED`, `SILENTLY DROPPED`) and evaluates the full ten-item defect matrix carried from round 88 into round 89.
5. **Connector Non-Obvious Move:** Synthesizes the calibration review findings (R02 F1/F3) and the carry-over ledger into a bounded verification move improving calibration honesty without harming operability or adjacency.

---

## 2. Province Authority & Adjacency: Receipt Script-Position Validation

### Boundary Question
*Is receipt script-position validation (`cmd-binding` in `.ufo/waves/round-87/count-c2.py`) mori's own-evidence accounting rather than kumitate lifecycle authority?*

### Evidence from Primary Province Declarations
- **`mori-shokunin/PROVINCE.md`**:
  - Lines 12–16: Mori explicitly *refuses* "dispatch and orchestration mechanism (→ kumitate)... Detection and report only — never remediation. Out of province → report, never absorb."
  - Line 46 (FR3): "Boundary: mori reports filesystem shape; kumitate owns orchestration/result semantics; `empty` alone does not prove never-written, and receipt review stays offline."
  - Line 65: Kumitate boundary: "Owns OMP task/hub orchestration and wave plan/run/record/collect semantics; mori passively grades `.ufo/waves/*` filesystem settlement state."
  - Lines 125–131 (r18): "Core, own-evidence retention: mori owns the retention gate over its *own* committed evidence (`tools/mori-retention-gate.py`...)"
  - Lines 175–181 (r21): "blocks acceptance above means **mori's own census baseline acceptance only**. An audit `disposed` row merely cites a structurally validated, hash-bound independent record; it is not mori's lifecycle settlement, result acceptance, or a reap/re-dispatch licence. Those remain kumitate-owned."
  - Lines 199–204 (r22): "The retention reconciler independently recounts the lane's committed evidence and compares a retained receipt; it does not rewrite the gate, policy, allowlist or history. Its match is accounting agreement only, not authentication, privacy clearance, exposure assessment or a kumitate lifecycle/receipt decision."
  - Lines 655–660 (r85): "Core, receipt provenance grammar (new record rule): a round's after receipts carry exactly one `# cmd:`, one `# rev:`, one `# limits:` and one or more `# counter-sha256:` ... This is a record rule over lane evidence, not a census surface."
  - Lines 678–684 (r86): "Core, receipt replay rule (rule change on an existing instrument): a receipt carrying `# replay: required` is bound to its command ... no lane replays a receipt's command; mori reports, it does not remediate."
- **`kumitate-shokunin/PROVINCE.md`**:
  - Lines 3–6, 12–16: Kumitate owns OMP task/hub orchestration, script layers (`scripts/`), runtime layers (`crates/`), and wave plan/run/record/collect semantics. It does not inspect or validate mori's internal counter receipts.
  - Lines 41–48 (r79): Kumitate acknowledges report-pointer and receipt verification as internal lane verifier disciplines, noting cross-lane report checking stays reported, never absorbed.

### Analysis & Adjacency Ruling
Receipt script-position validation is implemented in `.ufo/waves/round-87/count-c2.py` (under `binding_problems`). It verifies that the `# cmd:` line of a committed mori after-receipt executes the bound tool in script position (token index 1, or index 2 after interpreter flags like `-I`), rather than as data passed to `printf`/`echo`, in a comment following `#`, or inside an environment assignment.

1. **Scope of the Gate:** The gate inspects only mori's own historical and current after-receipts under `.ufo/waves/*/evidence/`. It does not execute or grade any artifact produced by kumitate or other sibling lanes.
2. **Authority Claimed:** Passing or failing this gate determines only whether mori's own receipt accounting meets the lane's registered gate standard (SKILL.md row 22). It asserts no authority over task dispatch, wave lifecycle settlement, seat completion status, or agent reaping.
3. **Consistency with Precedent:** Just as round-18 retention gating and round-22 retention reconciliation were ruled "accounting agreement only, not authentication... or a kumitate lifecycle/receipt decision", receipt script-position checking is strictly **mori own-evidence accounting**.

**Conclusion:** Receipt script-position validation is entirely within mori's province. It does not infringe upon or absorb kumitate's lifecycle authority.

---

## 3. Cross-Claim Coupling & Claim Axis Verdict

### Coupling Architecture
In mori round 89, two claims are declared:
- **C1 (operability):** The receipt gate `.ufo/waves/round-87/count-c2.py` binds the executed script by path identity and script position. Arm count moves 23 → 26.
- **C2 (calibration):** 12 r88 mutation survivors are killed with declared FAIL-label attribution across `.ufo/waves/round-88/count-c1.py` and `.ufo/waves/round-88/count-c2.py`. Arm counts move 25 → 28 and 17 → 26.

Despite being declared on distinct axes, C1 and C2 exhibit direct substrate and anchor coupling centered on `.ufo/waves/round-88/count-c2.py`:

```
                      +---------------------------------------+
                      |      C1 (Operability Landing)         |
                      |  .ufo/waves/round-87/count-c2.py      |
                      |      23 -> 26 selftest arms           |
                      +-------------------+-------------------+
                                          |
                        Migrates caller pin in same landing
                                          v
+---------------------------------------------------------------------------------+
|                       .ufo/waves/round-88/count-c2.py                           |
|   - Pre-C1: SUBJECT_ARMS = 23, TARGET = "... arms=23"                           |
|   - Post-C1 (760428ab): SUBJECT_ARMS = 26, TARGET = "... arms=26"              |
|   - C2 Target: Adds 9 mutation arms (17 -> 26), extracts helpers, cleans text   |
+---------------------------------------------------------------------------------+
                                          ^
                     Anchor TARGET = "... arms=26" required
                                          |
                      +-------------------+-------------------+
                      |       C2 (Calibration Counter)        |
                      |   .ufo/waves/round-89/count-c2.py     |
                      |   Mutant C2-target anchors on arms=26 |
                      +---------------------------------------+
```

### Detailed Coupling Points
1. **Caller Migration Dependency:**
   `.ufo/waves/round-88/count-c2.py` pins the arm count of `.ufo/waves/round-87/count-c2.py`. When C1 increased the gate's arms from 23 to 26, it had to update `SUBJECT_ARMS = 26` and `TARGET = "... arms=26"` in `.ufo/waves/round-88/count-c2.py` (`760428ab`).
2. **After-Specific Anchor in Frozen C2 Counter:**
   In `.ufo/waves/round-89/count-c2.py`, the frozen mutant `C2-target` uses the anchor:
   `TARGET = "real=met fx=4 clean=1 refused=2 absent=1 arms=26"`
   At the entering revision `30a297970122`, this line was `arms=23`. As recorded in `evidence/controls-r89.txt:23`, `C2-target` had 0 occurrences (`unanchored=1`). `C2-target` could **only** anchor after C1's caller migration landed!
3. **Substrate Contention:**
   `.ufo/waves/round-88/count-c2.py` is simultaneously:
   - A caller whose pin must be updated by C1.
   - A subject whose code is refactored (extracting `own_ok_of`, `met_line`, `clone_root_ok`) and expanded (17 → 26 arms) by C2.
4. **Execution Serialization:**
   Because C2's mutation anchor `C2-target` depends on the text produced by C1's caller migration, C1 had to land first (`760428ab`) before C2's candidate could be measured or integrated.

### Honest Claim Axis Verdict
- **Are the axes genuinely distinct?**
  Yes.
  - C1 measures **operability**: whether the receipt gate accepts legitimate command variants (`./tools/...`) and rejects evasions (comment-only or selfprint commands).
  - C2 measures **calibration**: whether the test suites for round-88 counters detect and attribute specific mutations (killing 12 survivors with exact `FAIL <arm>` lines).
- **Did scope absorption occur?**
  No.
  - C1 did not absorb C2's mutation arms; it migrated only the caller pin (`arms=23` → `arms=26`) as required for structural integrity.
  - C2 did not absorb C1's gate rules; it simply measures the mutant kill attribution on the migrated subject.
- **Verdict Recommendation:**
  Maintain separate, independent verdicts for C1 and C2 on the scorecard. Explicitly disclose the substrate serialization in the round iteration log: C1 establishes the operational baseline and pins `arms=26`, which C2's calibration suite subsequently tests.

---

## 4. Considerthese Proposal 2: Follow Unfixed Flags Forward

### Proposal Background
In `mori-shokunin/considerthese/2026-10-26.md`, Suggestion 2 proposed:
> *"Follow the unfixed critic flags forward. r48 left 9 flags unfixed. Each day I could check whether the next round's landing diff fixes, routes, or silently drops them, so the flagged-versus-fixed count becomes a carry-over ledger rather than a one-round snapshot."*

### Bounded Disposition Criterion
When tracking critic findings and verifier spotcheck notes across round boundaries, every identified defect from round $N-1$ must be evaluated against round $N$ contracts, candidate diffs, and evidence files according to this strict, bounded three-state criterion:

1. **`FIXED`**:
   The defect is actively remediated in code, tests, or documentation within round $N$. The fix is validated by an automated counter, selftest, or positive/negative control, with receipts committed in the round evidence.
2. **`ROUTED` (Carried Debt)**:
   The defect is not remediated in code in round $N$, but is explicitly acknowledged in `contract.md` (§Scope / out-of-scope), `PROVINCE.md` (Frontier/Carried), or `LOG.md`. The entry identifies the responsible owner, explains the rationale for deferral (e.g., preventing cross-claim coupling), and preserves the known limitation without false-green masking.
3. **`SILENTLY DROPPED` (Process Defect)**:
   The defect is neither fixed in code nor explicitly acknowledged and routed in the round contract/scorecard/log. The blind spot is omitted from verification, creating false confidence.

### Round 88 → Round 89 Carry-Over Disposition Table

| ID | Finding / Critic Flag (Round 88) | Source Citation | Round 89 State | Concrete Disposition Evidence in Round 89 |
|---|---|---|---|---|
| **F-01** | `C1-vacuity`: Checksum canary kills without arm attribution; unrelated exit code counted as kill | `Mo88C01Critic.md:23-50`; Spotcheck D3 | **FIXED** | Contract P-C2 defines `killed ⟺ (rc≠0 ∨ fail>0) ∧ FAIL <declared arm> present`. Canary retained as negative control 3 in `controls-r89.txt:67-71`. |
| **F-02** | `C2-no-harm`: Genuine `./tools/...` replay refused by raw whitespace token comparison | `Mo88C01Critic.md:97-114`; Spotcheck D2 | **FIXED** | Contract P-C1 lands `os.path.normpath` / `realpath` matching in `round-87/count-c2.py` (`760428ab`). Equiv-positive control accepted. |
| **F-03** | `C2-selfprint-own`: Self-printing command naming script as data bypasses `cmd-binding` | `Mo88C01Critic.md:115-136`; Spotcheck D2 | **FIXED** | Contract P-C1 enforces script position (token index 1 or 2 after flags) in `760428ab`. Selfprint fixture refused. |
| **F-04** | `C2-comment-bypass`: Bound path named only in comment after unquoted `#` bypasses gate | Spotcheck D2, line 109 | **FIXED** | Contract P-C1 enforces `shlex.split(..., comments=True)` in `760428ab` to drop shell comments. Comment fixture refused. |
| **F-05** | 12 mutation survivors in r88 counters (3 in c1, 9 in c2) | `Mo88M01Mut.md`; Spotcheck D4 | **FIXED (Candidate)** | E01 and E02 deliver candidates adding 12 selftest arms with exact declared `FAIL` lines; all 12 killed with attribution. |
| **F-06** | Overstated newness in `receipt-counterfeit-r88.md` and `README.md` (`absent_supersede_targets`) | Spotcheck lines 58–61, 108 | **ROUTED (Active)** | Assigned to peer `MoriR89` task ("Sweeping overstated newness mentions") for documentation correction. |
| **F-07** | Misleading `FX clean ... refused` wording on clean fixtures | Spotcheck line 111; Contract line 20 | **FIXED (Candidate)** | E02 candidate updates good clean fixture output to print `ok` instead of `refused`. |
| **F-08** | Dead `want_met` assignment in `count-c2.py` | Spotcheck line 111; Contract line 79 | **FIXED (Candidate)** | E02 candidate removes the dead assignment. |
| **F-09** | Unarmed r87 gate clauses (`c2-replay-compare-off`, `c2-supersede-*`, `c2-absent-*`) & F3 hermeticity | Spotcheck line 112; Contract lines 155–158 | **ROUTED (Carried)** | Explicitly declared out of scope in `contract.md` lines 155–158: arming them now would couple the gate's arm count to C1's pin. |
| **F-10** | Planned r89 item 3 (r86 value channel full-census snapshot) | Contract lines 151–154 | **ROUTED (Carried)** | Explicitly carried in `contract.md` lines 151–154: requires sizing a distinct population; deferred to preserve two-claim focus. |

**Disposition Summary:**
- **Fixed:** 6 / 10
- **Routed / Carried:** 4 / 10
- **Silently Dropped:** 0 / 10

No critic flags or verifier spotcheck findings from round 88 were silently dropped.

---

## 5. Non-Obvious Move: Compatible Synthesis Across Round Proposals

### Context & Evidence
Reviewer `Mo89R02C2` identified two subtle calibration risks in the frozen C2 setup:
1. **Finding F1 (Confounded Control 2b):** In `evidence/controls-r89.txt`, the skip-work control for `count-c1.py` had a pristine-red failure (`FAIL per_file_arms_frozen 24` vs `28`) because the control fixture's patch was internally inconsistent. Thus, the attribution rule was partly confounded by pristine failure rather than clean attribution.
2. **Finding F3 (Non-Specific Arm Failures):** The frozen kill rule requires `(rc!=0 or fail>0) and FAIL <declared arm>`. However, it does not assert that the declared arm is *specific* to that mutant; an arm that globally fails on any file modification could mask an unkilled mutant.
3. **Candidate Validation Evidence:** E01 (`Mo89E01ArmsC1.md`) and E02 (`Mo89E02ArmsC2.md`) proved that all 12 mutant copies fail with *exactly one* arm failing (`pass=27 fail=1` and `pass=25 fail=1`).

### Proposed Move
**Synthesize the Carry-Over Disposition Ledger with an L1 Integration Specificity Check (Single-Fault Attribution Assertion).**

During round integration, before committing the final C2 receipt, L1 (`MoriR89`) must:
1. Include the **Round 88 → Round 89 Carry-Over Disposition Table** directly in the round's permanent record (`LOG.md` / `SCORECARD.md`), demonstrating zero silently dropped flags.
2. Formally record the **Specific Attribution Tally** in the final C2 verification receipt:
   - For all 3 `count-c1.py` mutants: verify pristine passes 28/0, mutated runs exit with `fail=1`, and the failing arm matches the declared arm exactly.
   - For all 9 `count-c2.py` mutants: verify pristine passes 26/0, mutated runs exit with `fail=1`, and the failing arm matches the declared arm exactly.
   - Confirm that `count_unanchored == 0` post-C1 integration, directly corroborating that C1's `arms=26` migration anchored `C2-target`.

### Axes Affected
- **Calibration (+):** Eliminates the F3 attribution ambiguity by proving that no mutant causes multi-arm cross-fire, and provides formal carry-over accounting for critic findings.
- **Adjacency (Neutral):** Preserves strict lane boundaries; all checks remain internal evidence accounting.
- **Operability (Neutral):** Does not touch the operational gate logic landed in `760428ab`.

### Risks & Mitigations
- *Risk:* Altering the frozen predicate `P-C2` mid-flight.
- *Mitigation:* This move does NOT modify the code of `count-c2.py` or the wording of `P-C2`. It operates entirely as a verification discipline and reporting standard applied by L1 during integration.

---

## 6. Seat Clearance & Verification Checklist

- [x] Read `mori-shokunin/PROVINCE.md` and sibling `kumitate-shokunin/PROVINCE.md` and `tsukuroi-shokunin/PROVINCE.md`.
- [x] Confirmed receipt script-position validation is mori internal own-evidence accounting.
- [x] Mapped cross-claim coupling centered on `.ufo/waves/round-88/count-c2.py`.
- [x] Evaluated `considerthese/2026-10-26.md` proposal 2 and generated a bounded 10-item disposition table.
- [x] Formulated one bounded non-obvious move synthesizing calibration review and carry-over accounting.
- [x] No production, corpus, or fleet-root files modified.
- [x] Tooling compliance: No tools installed or upgraded (pacman paused host-wide; standard python3 used).
- [x] Scratch tree `/fast/scratch/hyaku/mori-r89/Mo89K01Conn/` removed before yield.

Report complete at `.ufo/waves/round-89/w1/Mo89K01Conn.md`.
