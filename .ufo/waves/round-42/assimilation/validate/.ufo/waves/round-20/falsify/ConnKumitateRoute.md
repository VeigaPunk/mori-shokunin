VERDICT: PARTIAL

## Evidence
- `mori-shokunin/PROVINCE.md:143-158`: Round-20 scope notes append Core per-seat wave settlement capability (`tools/mori-wave-settlement.py scan`) and assign wave landing statuses (`present`/`empty`/`stub`/`missing`/`misrooted`/`unsafe`/`unparsed`; waves `settled`/`partial`/`unsettled`/`no-spawn`/`unavailable`).
- `kumitate-shokunin/PROVINCE.md:3-6,10-23`: Kumitate defines its domain as "orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime" and owns wave execution/lifecycle semantics.
- `kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:37-43,100-128`: Kumitate's lifecycle defines wave settlement as operator-supplied `ufo-swarm-results-v1` outcome joining via `ufo-swarm-collect.mjs` (mapping status to `completed`, `failed`, `timeout`, `aborted`), explicitly distinct from static file discovery.
- `mori-shokunin/PROVINCE.md:12-16,46,65`: Mori explicitly refuses dispatch and orchestration mechanism (→ kumitate), defines FR3 boundary ("mori reports filesystem shape; kumitate owns orchestration/result semantics"), and confirms "kumitate owns OMP task/hub orchestration and wave plan/run/record/collect semantics; mori passively grades `.ufo/waves/*` filesystem settlement state."
- `mori-shokunin/.ufo/waves/round-20/evidence/c2-live-fleet.json`: Fleet-wide scan across 21 lanes, finding 196 dispatch-schema files, 12,307 declared members, 10,678 present reports, 1,622 missing reports, 0 empty, 1 misrooted (in `souji-shokunin`), 0 unsafe, 0 unparsed, 45 unreadable JSON files, and 47 dispatch filename flags matching `NAME_HINT_RE`.
- `mori-shokunin/tools/mori-wave-settlement.py:33-48,221-235,360-380`: The tool grades waves into lifecycle states `settled`, `partial`, `unsettled`, `no-spawn`, `unavailable` and exits with code 1 if any wave is not `settled`/`no-spawn`.
- `mori-shokunin/corpus/knowledge/wave-settlement-r20.md:23-43,53-63`: Documents measured limits, including that "a dispatch file is not dispatch evidence" and that never-dispatched files (`revenger` `rendered-undispatched.json`, `mado` `dispatch-preview.json`, `kama` job-cap refusals) are scored `unsettled` identically to lost reports.

---

## 1. Draft Routing Note: Mori to Kumitate and Lane L1s

```markdown
# ROUTING NOTE: Fleet-Wide Filesystem Report Landing Scan (Round 20 Observability)

TO: kumitate-shokunin L1 (Orchestration & Tooling Owner), Fleet Lane L1s
FROM: mori-shokunin L1 (Fleet & Host Observability)
DATE: 2026-10-21
SOURCE EVIDENCE: .ufo/waves/round-20/evidence/c2-live-fleet.json (scan timestamp 2026-10-21T10:46:50Z)
SCHEMA: mori-r20-c2-fleet-live-v1

### Explicit Boundary Declaration
In accordance with kumitate-shokunin/PROVINCE.md:3-6 and mori-shokunin/PROVINCE.md:12,46,65:
1. Mori reports physical filesystem shape only: whether a regular file of size > 0 existed at
   a declared task's `Report:` trailer path within the lane root at the time of scan.
2. Mori DOES NOT possess, infer, or assert execution outcome semantics:
   - A report marked `missing` is NOT an assertion that a seat is dead, killed, or failed.
   - A report marked `present` is NOT an assertion of task correctness or acceptance.
   - Mori cannot determine whether a missing report was never written or removed by hygiene.
   - Mori cannot determine whether a dispatch file was ever dispatched or merely rendered.
3. Kumitate owns orchestration, dispatch verification, session accounting, and outcome join semantics
   (via scripts/ufo-swarm-collect.mjs and ufo-mission-result-v1).
4. Lane L1s own internal wave reconciliation, successor run linking, and report recovery.

---

### Fleet Summary Tally
- Total Lanes Scanned: 21
- Total Waves Discovered (`ufo-swarm-wave-dispatch-v1` schema): 196
- Total Dispatched Members Declared: 12,307
- Reports Present on Disk (>0 bytes): 10,678 (86.76%)
- Reports Missing on Disk: 1,622 (13.18%)
- Reports Empty (0 bytes): 0
- Reports Misrooted (written to fleet root instead of lane root): 1 (`souji-shokunin`)
- Reports Unsafe (lexical path traversal / escape): 0
- Tasks Unparsed (lacking valid `Report:` trailer): 0
- Unreadable JSON files under `.ufo/waves/`: 45
- Dispatch Filename Flags (`preview` / `undispatched` / `validation`): 47 files

---

### Per-Lane Missing Report Accounting

| Lane | Discovered Waves | Declared Members | Present Reports | Missing Reports | Misrooted | Unreadable JSON | Probe Exit | Critical Context / Known Disclaimers |
|---|---|---|---|---|---|---|---|---|
| audio-shokunin | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive / no dispatch files |
| chousa-shokunin | 2 | 136 | 120 | 16 | 0 | 0 | 1 | Historical wave gaps |
| game-dev-2d-shokunin | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive / no dispatch files |
| game-dev-3d-shokunin | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive / no dispatch files |
| kagi-shokunin | 7 | 479 | 437 | 42 | 0 | 0 | 1 | Live/active round during scan |
| kaidoku-shokunin | 14 | 959 | 824 | 135 | 0 | 39 | 1 | 39 truncated/non-JSON files in arc2/arc3 |
| kake-shokunin | 5 | 325 | 261 | 64 | 0 | 0 | 1 | Includes r22/w2 seats re-run as r23/w1; 1 validation file |
| kama-shokunin | 19 | 1198 | 997 | 201 | 0 | 1 | 1 | Includes r19/r21 waves refused at host job cap |
| kasegi-shokunin | 1 | 64 | 44 | 20 | 0 | 0 | 1 | Single wave partial landing |
| kengaku-shokunin | 5 | 387 | 376 | 11 | 0 | 0 | 1 | High retention (97.2%) |
| kotoba-shokunin | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive / no dispatch files |
| kotodama-shokunin | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive / no dispatch files |
| kumitate-shokunin | 6 | 512 | 468 | 44 | 0 | 0 | 1 | Round 38 build (1 miss) and falsify (43 misses) |
| lore-shokunin | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 malformed JSON fixture; no dispatch files |
| mado-shokunin | 16 | 1030 | 914 | 116 | 0 | 2 | 1 | Includes `dispatch-preview.json` (undispatched) |
| mori-shokunin | 11 | 671 | 580 | 85 | 0 | 2 | 1 | Includes r19 W1 (48 misses) and W2 (22 misses) |
| revenger-shokunin | 1 | 32 | 0 | 32 | 0 | 0 | 1 | **Undispatched payload** (`rendered-undispatched.json`) |
| souji-shokunin | 12 | 783 | 662 | 120 | 1 | 0 | 1 | **1 misrooted file** written to fleet root |
| tabi-shokunin | 67 | 3932 | 3371 | 561 | 0 | 0 | 1 | 43 validation/clone files; 63 `.txt` report variants |
| tameshi-shokunin | 16 | 965 | 857 | 108 | 0 | 0 | 1 | 1 validation file (`validation-current.json`) |
| tsukuroi-shokunin | 14 | 834 | 767 | 67 | 0 | 0 | 1 | Static historical waves |

---

### Action Items for Recipients
1. **Kumitate (Orchestration):**
   - Note the presence of 47 filename-hinted files (e.g. `rendered-undispatched.json`, `dispatch-preview.json`)
     that match dispatch schemas but may never have been dispatched through the agent hub.
   - Do not trigger re-dispatch or wave failure handling based on Mori's `missing` count alone.
2. **souji-shokunin L1:**
   - Review the 1 misrooted file recorded at the fleet root matching your lane's trailer path.
   - Mori does not move or clean this file; live round output hygiene remains L1/souji owned.
3. **revenger-shokunin & mado-shokunin L1s:**
   - Confirm whether `rendered-undispatched.json` and `dispatch-preview.json` were unexecuted design artifacts.
4. **All Lane L1s:**
   - Cross-reference Mori's physical counts against your lane's internal execution receipts (`results.json`,
     transcripts, or launch ledgers). Successor runs and format variations (e.g., `.txt` vs `.md`)
     must be resolved inside the owning lane.
```

---

## 2. Attack: Does `mori-shokunin/PROVINCE.md` Round-20 Notes Keep That Boundary?

### Attack Findings: Why the Verdict is PARTIAL

#### A. What Holds (The Defensive Boundary)
1. **Explicit Lexical & Vocabulary Firewall (`PROVINCE.md:149`, `contract.md:80-81`):**
   `PROVINCE.md:149` explicitly states: `"A missing report is not a dead seat; result acceptance and re-dispatch stay kumitate's"`.
   In `tools/mori-wave-settlement.py:33`, the tool restricts its member status vocabulary to `present`, `empty`, `stub`, `missing`, `misrooted`, `unsafe`, and `unparsed`. The oracle test 14 (`frozen/c2-expected.json`) specifically validates that the words `dead`, `failed`, and `killed` are never emitted. Mori does not claim agent death.
2. **Refusal of Remediation on Misrooted Files (`PROVINCE.md:150-151`):**
   `PROVINCE.md:150-151` specifies: `"a misrooted file is routed to its lane L1 (souji's refusal fence covers live round outputs), never moved by mori"`.
   Mori adheres to `PROVINCE.md:16` (`"Detection and report only — never remediation"`), correctly routing the 1 misrooted report detected in `souji-shokunin` without moving or editing it.
3. **Explicit Frontier Reservations (`PROVINCE.md:153-154`):**
   The notes preserve as Frontier (FR3):
   - Emptied-by-hygiene versus never-written (cannot distinguish empty files from cleaned files).
   - Whether a dispatch file was ever dispatched.
   - Successor reports for re-run seats (e.g., `kake-shokunin` r22/w2 re-run as r23/w1).

#### B. What Breaks / Strains the Boundary (The Jurisdictional Leaks)
1. **State Nomenclature Collision (`settled` / `unsettled` vs Orchestration Settlement):**
   `PROVINCE.md:145` titles the capability `"Core, per-seat wave settlement"`, and `contract.md:78` defines wave states as `settled`, `partial`, `unsettled`, `no-spawn`, and `unavailable`.
   In `kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:40-41`, "settlement" is explicitly an *orchestration verdict* produced by joining `ufo-swarm-results-v1` into `ufo-mission-result-v1`.
   When Mori classifies a wave with 100% reports present as `settled`, it assigns a lifecycle completion status to an orchestration entity based purely on filesystem presence. Conversely, a wave whose subagents all executed and completed their mission, but whose output was written as `.txt` instead of `.md` (e.g., 63 Tabi seats), is branded `unsettled` by Mori. This blurs the distinction between a physical report landing check and an authoritative wave outcome settlement.
2. **Contradiction Between Core Admission and Frontier Reservation (Undispatched Payloads):**
   `PROVINCE.md:153-154` claims that `"whether a dispatch file was ever dispatched"` is **Frontier (FR3)**.
   HOWEVER, the Core tool `tools/mori-wave-settlement.py` indiscriminately scans every `ufo-swarm-wave-dispatch-v1` file under `.ufo/waves/`. In `c2-live-fleet.json`, `revenger-shokunin` is listed with:
   `waves: 1, members: 32, present: 0, missing: 32, exit: 1`.
   As proven by `GtLaneRevenger.md:91-94`, that file was `fleet-round-1-interactive/rendered-undispatched.json`, where `dispatch_started: false` and 0 seats were dispatched.
   By reporting 32 "missing seat reports" for Revenger without segregating undispatched files from dispatched waves, Mori's Core tool directly penalizes lanes for unexecuted plans, turning a static template into an execution failure.
3. **POSIX Exit Code 1 Semantics as an Implicit Failure Gate:**
   `contract.md:87` and `mori-wave-settlement.py:375-380` force the tool to exit with code 1 if any wave is `partial` or `unsettled`.
   `knowledge/wave-settlement-r20.md:40` attempts to rationalize this by asserting `"Exit 1 is an observation, not an error"`.
   In POSIX and OMP runner environments, exit code 1 is a failure indicator. In `c2-live-fleet.json`, 15 out of 21 lanes exit 1. Because Mori assigns exit 1 based on whether all files landed on disk, any lane retaining an undispatched preview file or an experimental validation payload fails the probe with exit 1. This exceeds neutral observability and behaves as an orchestration acceptance gate.

---

## 3. UFO-FSD Connector Synthesis: One Bounded Non-Obvious Move

### Evidence
1. **Fleet Evidence:** `c2-live-fleet.json` contains 47 dispatch files flagged by `NAME_HINT_RE` (e.g. `preview`, `undispatched`, `validation`). In `revenger-shokunin`, a single undispatched file created 32 false `missing` reports and triggered `exit 1`.
2. **Refinement Evidence:** Co-evolved refinement R3 in `mori-wave-settlement.py:43` and `wave-settlement-r20.md:48` already identifies `name_hint` (e.g., `undispatched-name:preview`), proving that lexical differentiation of speculative files is feasible in stdlib Python without external dependencies.
3. **Orchestration Boundary:** `kumitate-shokunin/PROVINCE.md:3-6` owns dispatch semantics; Mori cannot inspect runtime process trees or agent hub queues.

### Affected Axes
- **Adjacency (improves):** Eliminates jurisdictional collision where Mori attributes unexecuted dispatch templates to missing execution deliverables.
- **Operability (improves):** Removes false-positive `exit 1` alarms on lanes that archive preview or validation templates under `.ufo/waves/`.
- **Coverage (improves):** Partitions fleet observability into "Dispatched Wave Landing" vs "Speculative Template Inventory" without losing visibility into either.
- **Freshness & Calibration (harms none):** Preserves all 14 frozen oracle test cases, does not mutate the census script, and requires zero subagent or network dependencies.

### Proposed Move
**Formalize a Two-Tier Filesystem Tally in `mori-wave-settlement.py` and `PROVINCE.md`: Segregate "Confirmed Dispatched Waves" from "Speculative/Validation Artifacts", Mapping Speculative Files to State `speculative` (Exempt from Exit 1).**

Specifically, the L1 integration should implement the following bounded adjustment:
1. **Refine Wave State Logic for Name-Hinted and Zero-Spawn Files:**
   When a dispatch file matches `NAME_HINT_RE` (`preview`, `undispatched`, `not-dispatched`, `validation`) or has explicit payload indicators of non-dispatch (such as `taskCall: null` or `dispatch_started: false` in companion records):
   - Categorize its wave state as `speculative` (or `validation`) rather than `unsettled`.
   - Segregate its member counts into `speculative_declared` and `speculative_missing`, keeping them separate from the primary `totals.missing` metric.
2. **Decouple Exit Code from Speculative Files:**
   Update the exit code contract so that `exit 0` is returned when all non-speculative waves are `settled` (or `no-spawn`), preventing harmless template files in lanes like `revenger` and `mado` from forcing exit 1.
3. **Codify Terminology in `PROVINCE.md`:**
   In the Round-20 notes of `PROVINCE.md`, replace ambiguous phrases like `"per-seat wave settlement"` with `"per-seat report landing verification"`, and explicitly declare:
   > *"Mori verifies physical report file existence on disk for declared dispatch payloads. It partitions active wave dispatches from speculative/validation templates. Mori asserts no judgment on task execution success, agent termination, or wave outcome acceptance, all of which remain strictly owned by Kumitate."*

### Risks and Second-Order Effects
1. **Risk of Misclassifying Dispatched Waves as Speculative:**
   - *Risk:* A lane might name a legitimate, executed wave `validation.json` (as observed in Tabi rounds 15–19, where 12 validation files were actually executed).
   - *Mitigation:* The tool should keep `name_hint` as a partition flag in output JSON, but allow `--strict-dispatch` or an explicit companion check before suppressing missing counts, ensuring no real missing reports are masked.
2. **Oracle Regression Risk:**
   - *Risk:* Altering the state or exit rules could invalidate the 14 frozen cases in `.ufo/waves/round-20/frozen/c2-expected.json`.
   - *Mitigation:* Frozen case 12 (`no-spawn`) already establishes precedence for exempting non-spawned waves from exit 1. The 14 frozen cases do not include name-hinted files; the change touches only refinement case R3 (`REFINEMENT_CASES`).

### Verification Steps (for L1 Integration)
1. **Oracle Regression Battery:** Run `python3 tools/mori-wave-settlement.py --selftest` to confirm that all 14 frozen cases and refinement cases pass.
2. **Revenger Re-evaluation:** Execute `mori-wave-settlement.py scan --lane-root /home/vgpnk/Projects/shokunin/revenger-shokunin`. Verify that `rendered-undispatched.json` is classified as `speculative`/`name-hinted`, and does not trigger `exit 1` or inflate the fleet's active missing report ledger.
3. **Fleet Scan Differential:** Re-run `scan` across all 21 lanes and verify that active missing reports reflect genuine runtime dropouts (such as Mori R19 W1's 48 missing reports) rather than static preview templates.

---

## 4. Tooling & Environment Disclosure
- No packages installed or updated.
- Host pacman guard strictly respected (zero pacman commands executed).
- All operations strictly read-only; production repository state untouched.
- Counts derived from official `/usr/bin/jq` (jq 1.8.2) and Python 3.14 stdlib.
- Scratch report written strictly at assigned path: `.ufo/waves/round-20/falsify/ConnKumitateRoute.md`.