# Sibling-Overlap Scan & Boundary Review: Souji and Tsukuroi (ConnSoujiTsukuroi)

**Author:** MoriR20.ConnSoujiTsukuroi (UFO-FSD Connector, leaf seat, no subagent dispatch)  
**Round:** mori-shokunin round 20 (fleet/host observability)  
**Contract reference:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/contract.md`  
**Report path:** `.ufo/waves/round-20/build/ConnSoujiTsukuroi.md`  
**Prior status:** `STATUS: started` written as first action; this document overwrites it.

---

## 1. Executive Summary

This scan examines the sibling boundaries between `mori-shokunin` (round 20 claims C1 and C2) and two adjacent lanes:
1. **`souji-shokunin`** (domain: fleet workspace hygiene, artifact cleanup, Obsidian preservation; `souji-shokunin/PROVINCE.md:3-5`).
2. **`tsukuroi-shokunin`** (domain: host OS operability, package/systemd/kernel triage; `tsukuroi-shokunin/PROVINCE.md:3-5`).

### Key Findings
1. **C2 Wave Settlement touches Souji on two distinct surfaces:**
   - **The Fleet-Root Misrooting Surface (`misrooted`):** C2 scans for member reports at the expected lane path and, if missing, checks whether the file exists at the identical relative path under `--fleet-root` (`contract.md:75-76`). However, stray files under the fleet root repo are owned by Souji (`souji-shokunin/PROVINCE.md:8`). If Souji sweeps stray files in `$SHOKUNIN_ROOT` without recognizing misrooted reports, it would destroy the live evidence needed for lane recovery.
   - **The Empty / Missing Report Surface (FR3 "emptied-by-hygiene versus never-written"):** C2 checks filesystem shape only (`present`, `empty`, `missing`, `unsafe`, `unparsed`). C2 **cannot** determine whether an `empty` or `missing` file was emptied or removed by hygiene versus never written. Determining hygiene removal is strictly an offline check against Souji's receipt ledgers (`corpus/knowledge/obsidian-ledger.tsv`, approval lists; `mori-shokunin/PROVINCE.md:89`). During active rounds, Souji's own refusal fence forbids touching live lane work products (`souji-shokunin/PROVINCE.md:42`).
2. **C1 Drift Re-Pinning touches Tsukuroi directly in the live drift token set:**
   - Entering drift token `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` explicitly carries `owner=tsukuroi` (`tools/mori-census.sh:1493,1495`). Mori detects and reports non-fleet unit failures from the systemd journal as observability evidence and explicitly routes OS diagnosis to Tsukuroi (`mori-shokunin/PROVINCE.md:24`). In C1, this token is classified as `census-schema-change` with an evidence pointer to the round-14 unit failure routing commit.
   - Live journal notice and coredump tokens (`+FINDING:COREDUMP_NOTICE_JOURNAL_USER`, `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER`) interface with Tsukuroi's ADJ-04 / OUT-005 handoff: Tsukuroi retains OS crash and memory triage, while Mori retains fleet correlation.
3. **C2 Wave Settlement touches Tsukuroi on the process death / failure boundary:**
   - C2 strictly bans the vocabulary `dead`, `failed`, and `killed` (`contract.md:80-81`). If an unsettled wave seat crashed due to host memory exhaustion (OOM), segfault, or OS signal, C2 records only `missing` or `empty`. Triage of whether a seat died of host pressure belongs to Tsukuroi OS triage paired with Mori's Core journal window probe (`tools/mori-journal-window.py`), never to a guess made by `mori-wave-settlement.py`.

---

## 2. Evidence & Boundary Citations

### A. Souji-Shokunin Province & Boundaries
- **Domain & Core Ownership:**
  `souji-shokunin/PROVINCE.md:3-17`:
  > `Domain: fleet repository & workspace hygiene (掃除) — receipt-gated removal of stale, duplicate, and already-preserved artifacts.`  
  > `Owns:`  
  > `- The fleet root repo's hygiene surfaces: stray checkpoint/scratch files, superseded config snapshots, quarantine staging.`  
  > `- Lane-repo hygiene surfaces, per-lane and only with a receipt: .scratch/, dead worktree metadata (git worktree prune after the commits are proven pushed or empty), duplicate configs, stale generated output with no live references.`  
  > `- The Obsidian-preservation ledger: corpus/knowledge/obsidian-ledger.tsv (source path+hash, vault path+hash). Nothing qualifies as "moved to Obsidian" without a matching row.`
- **Explicit Refusals (Crucial Guards):**
  `souji-shokunin/PROVINCE.md:38-42`:
  > `Refuses:`  
  > `- Operator config (~/.config/**, driver scripts/, driver runtime .ufo/state/, .ufo/watchdog.log).`  
  > `- Any artifact whose owning lane has dirty or unpushed work touching it.`  
  > `- Live lane work products (current-round drafts, uncommitted reports).`
- **Adjacency with Mori:**
  `souji-shokunin/PROVINCE.md:50-52`:
  > `mori-shokunin observes fleet and host health (liveness, kill/OOM, runway) and reports; souji lists only its own uid's scratch residue and routes liveness or resource findings to mori. Complementary.`
- **Process Residue Boundary (F5 / Round 20):**
  `souji-shokunin/PROVINCE.md:147-158`:
  > `The F5 observation surface remains Core, list-only, on eligible readable own-uid candidates... Process listings never authorize killing, quarantine or deletion; certification OFF, K5 HELD.`

### B. Tsukuroi-Shokunin Province & Boundaries
- **Domain & Core Ownership:**
  `tsukuroi-shokunin/PROVINCE.md:3-14`:
  > `Domain: host operability & system repair (繕, mending) — the OS substrate itself: package state (pacman -Qkk verify loops, foreign/AUR census, .pkg.tar.zst receipt discipline), systemd user units & timers (systemctl --user, unit files, failed states), journal/boot triage (journalctl -b, dmesg error classes), driver/firmware plane...`
- **Refusal of Fleet Attribution & Service Remediation:**
  `tsukuroi-shokunin/PROVINCE.md:25-33`:
  > `Refuses: endpoint/model serving health (→ kama), secrets (→ kagi), binary RE of drivers (→ kaidoku/revenger — tsukuroi tracks state and health, not internals). Never installs, upgrades, or removes packages; never restarts services. Detection and report; the operator remediates.`  
  > `Host memory and kill-event measurements support OS triage; they do not establish which fleet wave caused pressure or whether an endpoint works. The existing census reports those signals; fleet correlation belongs to mori (../mori-shokunin/PROVINCE.md:6-16).`
- **Adjacency Handoff Table (ADJ-04):**
  `tsukuroi-shokunin/PROVINCE.md:49`:
  > `ADJ-04 | Host pressure or a kill signal needs fleet/wave attribution, liveness or progress correlation | OS memory, journal and boot diagnosis; cumulative counters are not dated incidents | mori | Capture time, boot/window, exact counter or PSI command/exit and observed value; distinguish presence, cumulative count and dated event. Request correlation, not a claim that a wave caused OOM`
- **Portable Ownership Anchors (OUT-001, OUT-005, OUT-007):**
  `tsukuroi-shokunin/PROVINCE.md:121,125,127`:
  > `OUT-001 | Core | mori-shokunin/PROVINCE.md @ 91940fa339e3 | # mori-shokunin — Province | independently labeled user/system journals, plus cgroup memory.events and the explicit same-boot journal window after a retained anchor; | Mori owns kill/OOM and cgroup memory evidence; fleet correlation of host pressure is mori's, not OS triage.`  
  > `OUT-005 | ADJ-04 | mori-shokunin/PROVINCE.md @ 91940fa339e3 | # mori-shokunin — Province | kill/OOM-related catalog-ID records and signal-11 coredump records | Mori owns kill/OOM catalog-ID and signal-11 coredump classification from separately labeled user/system journals; fleet attribution is its correlation, not tsukuroi's.`  
  > `OUT-007 | ADJ-05 | mori-shokunin/PROVINCE.md @ 91940fa339e3 | # mori-shokunin — Province | Refuses: dispatch and orchestration mechanism (→ kumitate); OS package, | Mori refuses dispatch and orchestration mechanism and routes it to kumitate, supporting ADJ-05's kumitate recipient.`

### C. Mori-Shokunin Province & Round 20 Contract
- **Domain & Read-Only Ownership:**
  `mori-shokunin/PROVINCE.md:3-11`:
  > `Domain: fleet & host observability (森) — whether the fleet, its waves and its host are alive and progressing.`  
  > `Owns (read-only probes): shokunin watchdog liveness... .ufo/waves/* settlement state (registry + results pair); kill/OOM-related catalog-ID records and signal-11 coredump records from independently labeled user/system journals... resource runway... lane silence grading.`
- **Explicit Refusals:**
  `mori-shokunin/PROVINCE.md:12-16`:
  > `Refuses: dispatch and orchestration mechanism (→ kumitate); OS package, systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal and cgroup events as fleet evidence and reports them, never owning OS state; endpoint and model-serving health (→ kama); credential material (→ kagi). Detection and report only — never remediation.`
- **Core Unit Failure Partitioning with Tsukuroi Routing:**
  `mori-shokunin/PROVINCE.md:24`:
  > `Failed-unit subject metadata preserves fleet-only UNIT_FAILURE_JOURNAL versus non-fleet UNIT_FAILURE_OUT_OF_SCOPE with tsukuroi triage routing; absent or unsafe subject metadata remains unknown.`
- **Coded Emission in `tools/mori-census.sh:1493,1495`:**
  > `emit_finding UNIT_FAILURE_OUT_OF_SCOPE info "class=unit_failure_record count=$nonfleetn subject=nonfleet owner=tsukuroi classification_rule=unit-name-token scope=user basis=scoped-record-count boot=${sboot[$scope]} note=non-fleet units (desktop/OS) — tsukuroi owns these; no fleet marker in the subject unit name (a routing hint, not proof of non-fleet ownership)"`
- **Frontier FR3 and Souji Offline Receipts:**
  `mori-shokunin/PROVINCE.md:46,89`:
  > `FR3 — Authoritative wave settlement and emptied-by-hygiene versus never-written (state F3)... Boundary: mori reports filesystem shape; kumitate owns orchestration/result semantics; empty alone does not prove never-written, and receipt review stays offline.`  
  > `Souji's receipts distinguish only listed removals: the approval list records hashed aggregator-r10* artifacts and the later sweep marks those exact paths pushed. For precisely those named paths, receipts support a swept (pushed-receipt) classification; for an empty path without a matching receipt, [UNKNOWN] history, so it is not evidence of “never written.” This is offline evidence reading, not a live census dependency.`
- **C2 Wave Settlement Contract Requirements:**
  `contract.md:70-81`:
  > `- Expected report path: the LAST line of a task matching ^Report: write your scoped findings to (\S+)$. The path must be relative, contain no .. component and resolve inside the lane root; otherwise the member is unsafe (never read). A task without the trailer is unparsed.`  
  > `- Member status: present (regular non-symlink file, size > 0), empty (size 0), missing, unsafe, unparsed. If missing under the lane root but the same relative path is a regular file under --fleet-root, the member is misrooted (counted as not present). Report bytes are never emitted; only status and counts.`  
  > `- Wave state: settled (every member present), partial (≥1 present, ≥1 not), unsettled (0 present, ≥1 member), no-spawn, unavailable... A missing report is NOT a dead seat: the output never says dead, failed or killed.`

---

## 3. Surface Analysis & How Mori Must Route Each Touch

### A. Surfaces Touching `souji-shokunin`

| Surface / Touch | Trigger in C1 or C2 | Sibling Ownership | How Mori Must Route It |
|---|---|---|---|
| **Fleet-Root Misrooted Reports** | C2 `mori-wave-settlement.py` observes a member report missing under `--lane-root` but present under `--fleet-root` at the identical relative path (`status=misrooted`). | `souji-shokunin` owns the fleet root repo's hygiene surfaces (`PROVINCE.md:8`), but refuses live lane work products (`:42`). | **Detection-only report.** Mori marks the member `misrooted` and counts it as not present in the lane. Mori **must not** move, copy, or delete the fleet-root file. Mori routes recovery of misrooted reports to the lane's L1 / operator. For Souji, any file under `.ufo/waves/round-*/build/*.md` is classified as a live lane work product under recovery, falling under Souji's refusal fence (`souji-shokunin/PROVINCE.md:42`) so it is never purged as an unreceipted stray file. |
| **Empty Member Reports (`size == 0`)** | C2 observes a declared report file that exists as a regular non-symlink file but has `size == 0` (`status=empty`). | Sibling question: was the file emptied by a hygiene script or truncated during artifact cleanup? | **Filesystem shape fact only.** Mori outputs `empty`. Mori **must not** infer whether the file was emptied by hygiene or written empty by an aborted agent. Resolving hygiene action is an offline inquiry against Souji's `corpus/knowledge/obsidian-ledger.tsv` or approval lists. In active rounds, Souji's refusal fence (`PROVINCE.md:40,42`) already guarantees Souji did not touch it. |
| **Missing Member Reports** | C2 observes a member whose expected report file does not exist (`status=missing`). | Sibling question: did Souji sweep or archive the report? | **Offline receipt reconciliation.** Mori reports `missing`. Differentiating "swept by hygiene" from "never written" is the FR3 frontier. If historical wave reports are missing, operator/auditor checks Souji's approval lists (`souji-shokunin/census/.../approval-list.tsv`). An absent report with no Souji receipt remains `[UNKNOWN] history`, never assumed "never written". |
| **Disappearance of Historical Wave Warnings (`-FINDING:WAVE_UNSETTLED_AGE`)** | C1 drift token `-FINDING:WAVE_UNSETTLED_AGE` appears because `aggregator-r10*` wave folders were deleted. | Souji performed receipt-gated removal of `aggregator-r10*` artifacts (`mori-shokunin/PROVINCE.md:89`). | **Drift classification evidence pointer.** In C1, Mori classifies `-FINDING:WAVE_UNSETTLED_AGE` with the explicit evidence pointer to Souji's pushed-receipt sweep (`souji-shokunin/census/operator-sweep-20261018/approval-list.tsv:56-73`). This proves the warning removal was due to receipted hygiene, not an unmeasured census regression. |
| **Roster Lane Probing (`+SURFACE:lane.souji`)** | C1 drift token `+SURFACE:lane.souji` in live drift against r10 baseline. | `souji-shokunin` is a sibling lane. Mori probes silence via git commits and launch anchors (`tools/mori-census.sh:2545`). | **Roster change classification.** Classified as `roster-change` (addition of souji to fleet roster since r10). Mori reads only public git commit metadata and launch anchors; it never inspects Souji's internal `.scratch/` or private workspaces. |

### B. Surfaces Touching `tsukuroi-shokunin`

| Surface / Touch | Trigger in C1 or C2 | Sibling Ownership | How Mori Must Route It |
|---|---|---|---|
| **Non-Fleet Unit Failures (`UNIT_FAILURE_OUT_OF_SCOPE`)** | C1 drift token `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` appears in live drift (`c1-drift-entering.json:17,68`). | `tsukuroi-shokunin` owns systemd user units, unit files, and failed states (`PROVINCE.md:8-14`). | **Explicit finding routing.** `tools/mori-census.sh:1493` already tags this finding with `owner=tsukuroi note=non-fleet units (desktop/OS) — tsukuroi owns these`. Mori classifies this token in C1 as `census-schema-change` pointing to the round-14 commit (`PROVINCE.md:24`). Mori never attempts systemctl remediation or OS triage. |
| **User Journal Coredumps & Signal-11 (`COREDUMP_NOTICE_JOURNAL_USER`, `SEGFAULT_SIGNAL11_JOURNAL_USER`)** | C1 drift tokens for structured coredump notices and signal-11 counts (`c1-drift-entering.json:13,16,66,67`). | Tsukuroi owns OS journal/boot triage (`journalctl -b`, dmesg error classes; `PROVINCE.md:11`). | **ADJ-04 / OUT-005 handoff.** Tsukuroi retains OS crash and core dump diagnosis; Mori retains fleet correlation and structured catalog-ID counting. Mori does not claim an OS segfault was caused by a specific fleet wave without correlated time-window proof. |
| **Disk Device Uptime / IO Average (`io_avg_unavailable`)** | C1 drift token `io_avg_unavailable` appears on `SURFACE disk` when diskstats or uptime cannot be read (`c1-drift-entering.json:59,72`). | Tsukuroi owns kernel/driver plane and device health (`PROVINCE.md:12-14`). | **Disclosed unmeasured data.** Mori emits `io_avg_unavailable=<dev>:<reason>`, never synthesizing a 0 B/s rate (`tools/mori-census.sh:74,1974`). If the underlying block device or `/proc/diskstats` is broken, OS repair routes to Tsukuroi / operator. |
| **Process Termination / Suspected Kill of Wave Seats** | C2 discovers an `empty` or `missing` report for a seat that may have crashed or suffered an OOM/SIGKILL. | Tsukuroi owns host memory and kill-event OS diagnosis (`PROVINCE.md:30-33`); Mori owns same-boot journal window correlation (`PROVINCE.md:25`). | **Vocabulary ban and multi-stage triage.** C2 strictly forbids `dead`, `failed`, or `killed` (`contract.md:80-81`). If an unsettled wave seat is suspected of being killed by host pressure, triage routes out-of-band: Tsukuroi checks OS unit failures and dmesg; Mori runs its read-only probe `tools/mori-journal-window.py` to check for timestamped OOM/SIGKILL catalog IDs in the same boot window. C2 itself never attempts process inspection. |
| **Roster Lane Probing (`+SURFACE:lane.tsukuroi`)** | C1 drift token `+SURFACE:lane.tsukuroi` in live drift against r10 baseline. | `tsukuroi-shokunin` is a sibling lane. Mori probes silence via git commits and launch anchors. | **Roster change classification.** Classified as `roster-change` (addition of tsukuroi to fleet roster since r10). Mori reads only public git commit metadata; it never inspects Tsukuroi's package receipts or system state. |

---

## 4. Contradictions & Second-Order Effects

### A. The Misrooted Report Contradiction (C2 vs Souji Fleet-Root Ownership)
- **The Contradiction:**
  Under `souji-shokunin/PROVINCE.md:8`, Souji owns "The fleet root repo's hygiene surfaces: stray checkpoint/scratch files, superseded config snapshots, quarantine staging."
  Under `contract.md:75-76`, C2 discovers when an agent writes its report under `--fleet-root` instead of `--lane-root` (e.g. `Projects/shokunin/.ufo/waves/round-20/build/Foo.md` instead of `Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/Foo.md`).
  A live instance occurred in this very round: `DraftProvince` mistakenly created its first draft at the fleet root before catching and moving it (`DraftProvince.md:38`).
  If Souji sweeps the fleet root for stray scratch files, it would consider an uncommitted file under `$SHOKUNIN_ROOT/.ufo/waves/` as an unreceipted stray artifact and delete or quarantine it.
  However, C2 relies on that file existing to diagnose the member as `misrooted` rather than `missing`, providing the operator and L1 the exact signal needed to recover the seat's findings!
- **Resolution:**
  Souji's `PROVINCE.md:42` already explicitly states: `Refuses: Live lane work products (current-round drafts, uncommitted reports)`.
  The routing contract must clarify that files matching `$SHOKUNIN_ROOT/.ufo/waves/round-*/build/*.md` are recognized as live work products in an unrecovered state, falling under Souji's refusal fence until the round closes and the owning lane's L1 completes recovery.

### B. The "Empty Report" Ambiguity (C2 vs Souji vs OS Kill)
- **The Ambiguity:**
  When `mori-wave-settlement.py` observes an `empty` (size 0) report file, three competing hypotheses exist:
  1. *Hygiene:* A hygiene script truncated or cleared the report.
  2. *OS / Runtime Kill:* The agent touched or opened the report file (e.g., initial `write` or shell redirect) and was immediately killed by an OOM/SIGKILL before writing bytes.
  3. *Agent Behavior:* The agent deliberately created an empty file or crashed cleanly.
- **Resolution:**
  C2 rejects all three hypotheses at runtime: it emits `status=empty` and stops.
  - Souji is ruled out for active rounds by `souji-shokunin/PROVINCE.md:40,42`. For historical rounds, hygiene requires an explicit receipt in `corpus/knowledge/obsidian-ledger.tsv`.
  - OS kills are ruled out from C2 by `contract.md:80-81` (vocabulary ban: no `dead`, `failed`, `killed`). If host pressure is suspected, triage routes to Tsukuroi (OS diagnosis) and Mori Core (`tools/mori-journal-window.py` for same-boot journal catalog IDs).
  This preserves C2 as a deterministic, purely observational filesystem scan.

### C. The `-FINDING:WAVE_UNSETTLED_AGE` Token (C1 vs Souji vs C1Critic)
- **The Issue:**
  In `c1-drift-entering.json:49`, `-FINDING:WAVE_UNSETTLED_AGE` is in drift because the warning on `aggregator-r10` and `aggregator-r10-resume` disappeared.
  `C1Critic.md:7-15` raised this as the strongest falsifier against C1, noting that if the L1 classifies this removal as benign `live-state`, it risks normalizing evidence loss without proof of settlement.
- **The Sibling Ground Truth:**
  `mori-shokunin/PROVINCE.md:89` explicitly documents why those waves disappeared: Souji performed receipt-gated removal of `aggregator-r10*` artifacts with pushed-receipt verification (`souji-shokunin/census/operator-sweep-20261018/approval-list.tsv:56-73`).
  By connecting C1's drift token classification directly to Souji's historical hygiene receipt, Mori resolves `C1Critic`'s objection: the disappearance is backed by an authoritative, immutable sibling receipt, not an unevidenced assumption.

---

## 5. The Proposed Move (UFO-FSD Synthesis)

### Proposed Move: Formalize the Tri-Lane Wave Settlement & Drift Handoff Boundary in `PROVINCE.md`

Synthesize the findings across `DraftProvince.md`, `SafetySentinel.md`, `ConnKumitate.md`, `C1Critic.md`, and this scan into a single bounded addition to `PROVINCE.md` (to be appended by L1 under the Round-20 scope notes):

```markdown
### Round-20 Tri-Lane Handoff Boundary (Souji, Tsukuroi, Mori)

1. **Wave Settlement Misrooted Reports & Fleet-Root Hygiene (Mori ↔ Souji):**
   `tools/mori-wave-settlement.py` detects member reports present under `--fleet-root` when missing from `--lane-root` and marks them `misrooted` (counted as not present in the lane). Mori performs no file manipulation, copy, or cleanup. A misrooted report file under `$SHOKUNIN_ROOT/.ufo/waves/` is a live lane work product under recovery, falling under Souji's refusal fence (`souji-shokunin/PROVINCE.md:42`) and must never be swept as an unreceipted stray file. Recovery belongs strictly to the lane L1 / operator.

2. **Empty / Missing Reports and FR3 Hygiene Triage (Mori ↔ Souji):**
   `mori-wave-settlement.py` observes filesystem shape only (`empty`, `missing`). It cannot determine whether an artifact was emptied or removed by hygiene versus never written. For active rounds, Souji's refusal fence (`souji-shokunin/PROVINCE.md:40,42`) guarantees Souji does not touch uncommitted reports. For historical waves, distinguishing hygiene removal requires offline receipt reconciliation against Souji's `corpus/knowledge/obsidian-ledger.tsv` and operator approval lists (`PROVINCE.md:89`). The live scan tool never reads Souji ledgers.

3. **Suspected Seat Kills and Non-Fleet Unit Failures (Mori ↔ Tsukuroi):**
   In C1, `FINDING UNIT_FAILURE_OUT_OF_SCOPE` carries `owner=tsukuroi`, preserving systemd non-fleet unit failure triage with Tsukuroi while Mori retains structured journal and cgroup observability. In C2, `mori-wave-settlement.py` is strictly forbidden from diagnosing process death or using the terms `dead`, `failed`, or `killed` (`contract.md:80-81`). If an unsettled wave seat is suspected of process termination from host memory pressure or a kernel signal, triage routes out-of-band: Tsukuroi investigates OS/unit health, and Mori correlates same-boot journal window catalog IDs (`tools/mori-journal-window.py`).
```

### Affected Axes
- **Adjacency (Primary Gain):** Directly resolves the boundary between C2's `misrooted` status and Souji's fleet-root hygiene; grounds FR3 offline receipt triage; establishes clear handoffs with Tsukuroi for OS unit failures and seat death triage.
- **Freshness & Calibration (Secondary Gain):** Unblocks C1 drift classification by supplying the exact sibling receipt for `-FINDING:WAVE_UNSETTLED_AGE` (Souji approval list) and the exact schema routing commit for `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` (Tsukuroi routing in round 14).
- **Coverage (No-Harm):** Preserves C2's pure filesystem-shape design without adding complex cross-lane dependencies or runtime ledger reading.
- **Operability (No-Harm):** Zero added CPU latency, zero new processes; both `tools/mori-census.sh` (SHA frozen) and `tools/mori-wave-settlement.py` remain fast, deterministic, and read-only.

---

## 6. Risks, Blocker Check, and Falsifiers

1. **Risk of Premature Fleet-Root Sweeps:** If Souji runs a sweep on `$SHOKUNIN_ROOT` while an agent has misrooted a report, Souji might delete it before the lane L1 notices C2's `misrooted` output.
   *Falsifier / Mitigation:* Souji's `PROVINCE.md:42` already refuses live work products. L1 recovery procedures must prioritize copying misrooted files into the lane root prior to round closure.
2. **Risk of Misclassifying `-FINDING:WAVE_UNSETTLED_AGE`:** If classified as `live-state` without citing Souji's receipts, `C1Critic`'s objection stands and calibration is harmed.
   *Falsifier / Mitigation:* The C1 register entry for `-FINDING:WAVE_UNSETTLED_AGE` must explicitly point to `souji-shokunin/census/operator-sweep-20261018/approval-list.tsv:56-73` and `mori-shokunin/PROVINCE.md:89`.
3. **Risk of C2 Scope Creep into OS Triage:** If future developers add process checking (`ps`, `pidfd`, `journalctl`) into `mori-wave-settlement.py`, it would violate C2's pure filesystem contract and breach Tsukuroi's domain.
   *Falsifier / Mitigation:* `c2-expected.json:20` enforces `no_vocab: ["dead", "failed", "killed"]`. The oracle harness must fail if any runtime status or execution diagnostic is introduced.

---

## 7. Verification & Audit Trail

- **Inspection Mode:** Strictly read-only file reads and greps across `souji-shokunin`, `tsukuroi-shokunin`, `mori-shokunin`, and `.ufo/waves/round-20/`.
- **Tools Executed:** None. No census runs (`--drift` / `--pin`), no selftests, no build commands, no git/jj mutating commands.
- **Tooling Directive / Installs:** Zero packages or tools installed or updated. No pacman commands executed (pacman paused per host directive).
- **Subagents:** Leaf seat; zero subagents dispatched.
- **Checks for Main Agent / L1 Integrator:**
  1. Confirm that the C1 register entry for `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` is classified as `census-schema-change` with `evidence: mori-shokunin/PROVINCE.md:24 (round-14 commit)`.
  2. Confirm that the C1 register entry for `-FINDING:WAVE_UNSETTLED_AGE` cites Souji's approval list receipt (`souji-shokunin/census/operator-sweep-20261018/approval-list.tsv:56-73`) as noted in `mori-shokunin/PROVINCE.md:89`.
  3. Include the Tri-Lane Handoff Boundary text from §5 in the round-20 `PROVINCE.md` append alongside the C2 wave settlement additions.
