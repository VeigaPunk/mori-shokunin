# Sibling-Overlap Scan & Boundary Review for C2 (ConnKumitate)

**Author:** MoriR20.ConnKumitate (UFO-FSD Connector, leaf seat, no subagents)  
**Target:** Sibling overlap analysis between `mori-shokunin` (C2 wave settlement) and `kumitate-shokunin` (orchestration/wave lifecycle).  
**Contract reference:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/contract.md:49-89`  
**Report path:** `.ufo/waves/round-20/build/ConnKumitate.md`  

---

## 1. Executive Summary

1. **Does the C2 tool stay on mori's side?**  
   **YES.** The proposed tool `tools/mori-wave-settlement.py` strictly adheres to filesystem-shape observation. It accepts only directory targets (`--lane-root`, optional `--fleet-root`), consumes zero execution-result records, does not read or emit report body bytes, and explicitly forbids execution-outcome semantics. The contract (`contract.md:80-81`) and oracle (`frozen/c2-expected.json:20`) ban the vocabulary `dead`, `failed`, and `killed`. It observes whether declared report files exist on disk (`present`, `empty`, `missing`, `misrooted`, `unsafe`, `unparsed`) and categorizes wave landing ratios (`settled`, `partial`, `unsettled`, `no-spawn`, `unavailable`), leaving all orchestration verdicts, execution semantics, and remediation to `kumitate` and L1/L0.

2. **Does kumitate already ship an equivalent counter?**  
   **NO.**  
   - `kumitate-shokunin/scripts/` ships 8 repository-governance scripts (`anchor-truth.mjs`, `claims-check.mjs`, `surface-probe.mjs`, `proxy-check.mjs`, `kimi-census.mjs`, `sources-check.mjs`, `cite-check.mjs`, `round-gate.mjs`), none of which inspect wave settlement or member report files.  
   - In the upstream runtime (`/home/vgpnk/Projects/ufo-fsd-alpha/scripts/`):
     - `ufo-swarm-wave.mjs` handles wave planning and dispatch (`plan`, `run`, `record`); it has no `settle` CLI verb.
     - `ufo-swarm-collect.mjs` handles outcome joining (`collect`). While it features an optional `reportSummary` block (`:719-731`), it is **not an equivalent counter**:
       1. It cannot run without orchestrator-supplied execution results: `--results <settled.json>` is mandatory (`:673`).
       2. It only looks for `<ROOT>/<reportDir>/<member.name>.md` when `reportDir` is explicitly declared in the dispatch or registry; it does not parse prompt task bodies or the fleet-wide `Report: write your scoped findings to <path>` convention.
       3. It does not distinguish empty files (size 0) from populated files (size > 0), using only `lstatSync().isFile()`.
       4. It has no fleet-root misrooting detection (files written to fleet root instead of lane root are merely reported missing).
       5. It operates on a single wave at a time, incapable of scanning lane roots or historical `.ufo/waves/` trees.

---

## 2. Boundary Citations & Province Comparison

### A. Kumitate's Province and Lifecycle Contract

- **Province domain & refusal:**  
  `kumitate-shokunin/PROVINCE.md:3-6`:  
  > `Domain: orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime`  
  > `Owns: the domain knowledge, playbooks, error patterns, and checklists above.`  
  > `Refuses: anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it.`  

- **Absence of a wave `settle` CLI verb in Kumitate:**  
  `kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:37-43`:  
  > `Round-32 re-census errata (topic prose corrected, not a member removal): the prior topic-form body claimed a wave CLI verb settle and a collector refusal code stale_dispatch_pair. Live main admits only plan / run / record (scripts/ufo-swarm-wave.mjs:1801–:1807); settlement is operator-supplied ufo-swarm-results-v1 input to collect.`

- **Collector owning surface & outcome mapping:**  
  `kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:100-104,114-120`:  
  > `scripts/ufo-swarm-collect.mjs: Owning surface. Bridge from settled wave member outcomes into the ufo-mission-result-v1 evidence envelope... Header: evidence for L1/L0 only — never a judge input and never a handoff path. Sole CLI verb is collect.`  
  > `Status → outcome map. STATUS_OUTCOME (scripts/ufo-swarm-collect.mjs:93) freezes: completed→completed, failed→failed, timeout→failed, cancelled|canceled|aborted→aborted... stopReason fallback only; never rewrite the outcome.`

- **Fail-closed join requirements:**  
  `kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:122-126`:  
  > `Join. collectEntries (scripts/ufo-swarm-collect.mjs:540) requires every dispatch member to have exactly one results row and every results row to name a dispatch member: missing → unmapped_member... extra → unexpected_member... Conflicting agentId/item evidence fails closed; a member whose outcome the inputs cannot name is never invented.`

### B. Mori's Province and Contract Boundaries

- **Mori's domain and read-only ownership:**  
  `mori-shokunin/PROVINCE.md:3-4,6-10`:  
  > `Domain: fleet & host observability (森) — whether the fleet, its waves and its host are alive and progressing.`  
  > `Owns (read-only probes): ... .ufo/waves/* settlement state (registry + results pair); ...`  

- **Refusal of orchestration and remediation:**  
  `mori-shokunin/PROVINCE.md:12-16`:  
  > `Refuses: dispatch and orchestration mechanism (→ kumitate); OS package... Detection and report only — never remediation.`

- **Wave settlement Core definition:**  
  `mori-shokunin/PROVINCE.md:23`:  
  > `Wave settlement — SURFACE waves: registry/dispatch/results presence and per-wave age; report settled, unsettled, or empty without calling an aged wave failed.`

- **FR3 frontier boundary:**  
  `mori-shokunin/PROVINCE.md:46`:  
  > `FR3 — Authoritative wave settlement and emptied-by-hygiene versus never-written (state F3). First evidence: corpus/knowledge/audit-r11.md:202; ../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:28-34,91-120. Boundary: mori reports filesystem shape; kumitate owns orchestration/result semantics; empty alone does not prove never-written, and receipt review stays offline.`

- **Adjacent routing table entry for Kumitate:**  
  `mori-shokunin/PROVINCE.md:65`:  
  > `| kumitate | Owns OMP task/hub orchestration and wave plan/run/record/collect semantics; mori passively grades .ufo/waves/* filesystem settlement state. No conflicting settlement contract was found. | ../kumitate-shokunin/PROVINCE.md:3-6; ../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:28-34,91-120; PROVINCE.md:6-10 |`

- **Authoritative verdict reservation:**  
  `mori-shokunin/PROVINCE.md:118-120`:  
  > `FR14 remainder: telemetry schema changes, concurrent snapshots, permanent termination, authoritative wave-result semantics and emission stay frontier or kumitate-owned. No scan is an orchestration verdict.`

- **Contract specification for C2 (`tools/mori-wave-settlement.py`):**  
  `mori-shokunin/.ufo/waves/round-20/contract.md:74-81`:  
  > `Member status: present (regular non-symlink file, size > 0), empty (size 0), missing, unsafe, unparsed. If missing under the lane root but the same relative path is a regular file under --fleet-root, the member is misrooted (counted as not present). Report bytes are never emitted; only status and counts.`  
  > `Wave state: settled (every member present), partial (≥1 present, ≥1 not), unsettled (0 present, ≥1 member), no-spawn, unavailable (no member had a parseable safe path). A missing report is NOT a dead seat: the output never says dead, failed or killed.`

---

## 3. Structural Comparison: Mori C2 vs Kumitate Collector

| Dimension | Mori C2 (`mori-wave-settlement.py`) | Kumitate Collector (`ufo-swarm-collect.mjs`) | Overlap / Conflict Assessment |
|---|---|---|---|
| **Role & Purpose** | Passive host/fleet observability: did declared report files land on disk? | Orchestration evidence synthesis: join member results into mission envelope. | No conflict: observation vs orchestration. |
| **Input Required** | `--lane-root DIR` (reads only `ufo-swarm-wave-dispatch-v1` files on disk). | `--wave FILE` AND `--results FILE` (`ufo-swarm-results-v1`). | Orthogonal: Mori needs zero runtime result inputs; Kumitate requires execution outcomes. |
| **Scan Scope** | Scans entire `<lane-root>/.ufo/waves/` tree across all rounds. | Single wave explicitly specified via `--wave`. | No overlap. |
| **Report Discovery** | Parses task text trailer `^Report: write your scoped findings to (\S+)$`. | Computes `join(ROOT, reportDir, member.name + ".md")` only if `reportDir` declared. | Different mechanisms: Kumitate misses prompt-trailed reports; Mori detects them. |
| **File Attributes Checked** | Regular file (`S_ISREG`), non-symlink (`os.lstat`), size > 0 vs size == 0. | Regular file (`lstatSync().isFile()`). | Mori distinguishes `empty` (size 0) from `present` (>0); Kumitate does not. |
| **Misroot Handling** | Checks `--fleet-root` for identical relative path; labels `misrooted`. | None (reported missing or dropped). | Mori provides fleet hygiene observability; Kumitate is blind to fleet root leakage. |
| **Vocabulary & Semantics** | `present`, `empty`, `missing`, `misrooted`, `unsafe`, `unparsed`; states `settled`, `partial`, `unsettled`, `no-spawn`. Banned: `dead`, `failed`, `killed`. | `completed`, `failed`, `timeout`, `aborted`, `unmapped_member`, `unexpected_member`. | Strict vocabulary firewall maintained. |
| **Output Schema** | `mori-wave-settlement-v1` | `ufo-mission-result-v1` (envelope) | Completely separated schemas. |

---

## 4. UFO-FSD Connector Synthesis: One Bounded Non-Obvious Move

### Evidence
1. **The Round-19 Mined Mistake:** Round 19 Wave 1 dispatched 64 seats and retained 16 reports; 48 missing reports went unnoticed until manual post-run recovery and closure (`contract.md:51-54`). Neither Kumitate's `ufo-swarm-collect.mjs` nor Mori's `SURFACE waves` caught this during execution because Kumitate lacked a standalone settlement observer, while Mori's existing census probe checked only `registry/dispatch/results` file existence and age without counting dispatched members (`CensusWavesSurface.md`).
2. **Schema Terminology Clash:** In `round-19`, the hand-written settlement receipt `.ufo/waves/round-19/wave1-settlement.json` used the schema identifier `mori-wave-settlement-v1` (`DraftProvince.md:25`). The C2 tool in `contract.md:82` is specified to emit `schema: mori-wave-settlement-v1`. While the tool's discovery filter (`schema == "ufo-swarm-wave-dispatch-v1"`) correctly ignores `wave1-settlement.json` as `ignored_json`, the naming collision illustrates ambient confusion between manual closure records and machine-emitted observability output.
3. **The Semantic Trap of "Settlement":** In `kumitate`, "settlement" is an *orchestration verdict* (joining execution results to dispatch). In `mori`, "settlement" has historically meant *presence of dispatch/results file pairs on disk* (`SURFACE waves`), now being refined in C2 to mean *filesystem report landing ratio*.

### Affected Axes
- **Coverage (C2):** Acquisition of the 14/14 per-seat settlement capability (`frozen/c2-expected.json`).
- **Adjacency:** Preserving the strict non-interference boundary between `mori` (observability) and `kumitate` (orchestration).
- **Operability:** Eliminating operator confusion between an in-flight filesystem landing report and an authoritative wave outcome verdict.

### Proposed Move
**Formalize the "Settlement" Boundary Split in Province Scope Notes and Tool Diagnostics: Explicitly Define Mori's C2 as "Filesystem Report Landing Verification" to Disambiguate from Kumitate's "Execution Outcome Settlement".**

Specifically, the L1 integration should synthesize the candidate text in `DraftProvince/province-r20.md` and `DraftSettlementNote` to codify three explicit architectural guarantees:
1. **Semantic Disambiguation in PROVINCE.md:**  
   In the Round-20 appended scope note (`PROVINCE.md`), state verbatim:
   > *"Mori's wave settlement probe measures physical filesystem landing only (whether declared report files exist, are non-empty, and resolve safely within lane bounds). It is decoupled from Kumitate's execution-outcome collection (`ufo-swarm-collect.mjs`), which adjudicates agent termination and process results. A wave graded `settled` by Mori means 100% of declared report files landed on disk; it does not assert that subagent tasks succeeded or passed judgment."*
2. **Diagnostic Field Preservation:**  
   Ensure the output schema `mori-wave-settlement-v1` explicitly emits `state: "settled"|"partial"|"unsettled"|"no-spawn"|"unavailable"` alongside member status counters (`present`, `empty`, `missing`, `misrooted`, `unsafe`, `unparsed`), and never adds fields resembling Kumitate's outcome envelope (`outcome`, `stopReason`, `failureClass`, `subagents`).
3. **Audit Rule for Offline Hygiene (FR3 Boundary):**  
   Record in the round lesson that a missing report observed by `mori-wave-settlement.py` cannot determine whether the report was never written or was cleaned up by `souji` hygiene (`PROVINCE.md:46`). The tool reports filesystem truth at scan time; historical causation remains offline review.

### Risks and Second-Order Effects
1. **Vocabulary Contamination Risk:** If an implementer or reviewer adds convenience aliases like `failed_count` or `dead_seats`, it would immediately violate `contract.md:80-81`, fail oracle case 14 (`c2-expected.json:20`, `no_vocab: ["dead", "failed", "killed"]`), and breach Kumitate's province boundary (`PROVINCE.md:12,118-120`).  
   *Mitigation:* Keep the strict AST/token assertion in the test harness.
2. **Path Traversal & Race Conditions:** As noted by `SafetySentinel.md:11-14`, resolving report paths across symlinks or traversing `..` components could escape the lane root or leak host directory structures.  
   *Mitigation:* Enforce `follow_symlinks=False` on `os.lstat` and perform lexical rejection of `..` before joining paths, exactly as specified in `contract.md:71-73` and grounded by `SrcPathContainment.md`.
3. **Dispatch Payload Format Drift:** If a future Kumitate release changes `taskCall.tasks` structure or alters the `Report:` trailer convention, Mori's regex `^Report: write your scoped findings to (\S+)$` would mark tasks as `unparsed`.  
   *Mitigation:* Mori's tool already explicitly defines the `unparsed` member state and `unavailable` wave state for this condition (`contract.md:74,79`), degrading gracefully to observable unparsed counts rather than crashing.

### Verification (for L1 Integration)
1. **Oracle Verification:** Confirm that `tools/mori-wave-settlement.py` passes all 14 frozen cases in `.ufo/waves/round-20/frozen/c2-expected.json`, specifically:
   - Case 5 (`misrooted`): correctly flags fleet-root reports without following symlinks.
   - Case 10 (`symlink-report`): correctly marks symlinked reports as not present (`present: 0`).
   - Case 14 (`deterministic`): verifies zero occurrences of `dead`, `failed`, or `killed` in tool output.
2. **Kumitate Non-Overlap Verification:** Confirm that no imports from `kumitate-shokunin` or `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/` are introduced into `tools/mori-wave-settlement.py`. The tool must remain stdlib Python 3 only (`contract.md:56`).
3. **Live Demonstration:** Execute `mori-wave-settlement.py scan --lane-root /home/vgpnk/Projects/shokunin/mori-shokunin --fleet-root /home/vgpnk/Projects/shokunin` and verify that Round 19 Wave 1 yields exactly `present = 16` of 64 members, matching historical closure notes (`contract.md:95-97`).

---

## 5. Tooling & Pacman Guard Disclosure

- No packages installed or updated.
- No pacman commands executed (host pacman guard respected).
- No git or jj mutating commands executed.
- Repository state untouched; all inspections read-only.
