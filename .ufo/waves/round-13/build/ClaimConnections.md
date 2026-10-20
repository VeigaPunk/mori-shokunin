# ClaimConnections: Synthesis of C1/C2 Across Previous Mistakes and Scope Traps

**Lane:** `mori-shokunin`  
**Milestone:** Round 13 structured scopes and verdict integrity  
**Author Seat:** `MoriR13.ClaimConnections` (connector)  
**Declared Axes:** `coverage`, `operability` (lowest owned scores: coverage=6, operability=6)  
**Date:** 2026-10-20  
**Carrying Commit Context:** Target Round 13 working tree  

---

## 1. Executive Summary & Frontier Walk

The mission for Round 13 in `mori-shokunin` centers on two core improvements:
1. **C1 (coverage):** Replacing raw message text regexes in `probe_journal` with MESSAGE-free structured `MESSAGE_ID` and field queries across independently labeled `user` and `system` scopes, recording **notice units** rather than misrepresenting them as kernel-caused victim counts or fleet-caused kills.
2. **C2 (operability):** Repairing production long-history SIGPIPE authorship loss (**F01**) and rejecting invalid verdicts (such as `BANANA`, duplicate verdicts, missing summary lines, or exit-code mismatches) in the silence oracle (**F02**).

This connector analysis synthesizes the round's proposals, traces causal connections to historical mistakes (**Q6, Q7, Q15, Q16, Q20**), unmasks hidden scope traps (especially the conflation of structured userspace notices with kernel kill records and the illusion of self-attested discernment without non-author spotchecks), and identifies **one non-obvious move** that improves `coverage` and `operability` without harming any sibling axis (`depth`, `calibration`, `freshness`, or `adjacency`).

---

## 2. Connections to Previous Mistakes & Admitted Quality Criteria

| Mistake / Criterion | Historical Origin & Context | Direct Impact on C1 / C2 | Scope Trap / Failure Mode |
|---|---|---|---|
| **Q6** (`QUALITY.md:11-12`, M2) | `2026-10-15-errexit-pipefail-silent-crash.md`<br>Unreadable input causes silent abort under `set -euo pipefail`; crash exit code `1` equals `DRIFT` exit code `1`. | **C1 & C2:** In C1, querying journalctl (user or system) or missing system journal permissions must never abort census with rc 1. In C2 (F02), oracle must distinguish setup crash (rc > 1) from real DRIFT (rc 1) and CLEAN (rc 0). | **Scope Trap:** Treating journal permission errors or unreadable input as DRIFT or silent crash rather than emitting structured `unavailable`. If journalctl exits > 1, `emit_surface journal unavailable` must preserve rc 0 for non-finding clean states. |
| **Q7** (`QUALITY.md:13-14`, M3) | `2026-10-15-selftest-grep-sigpipe-race.md`<br>Live producer pipe into early-exit consumer (`grep -q`) causes SIGPIPE (`141 ≠ 1`), inverting match condition under `pipefail`. | **C2 (F01):** Production authorship evaluation at `tools/mori-census.sh:1494` piped commit stream into `sed ... | grep -Fxq`. When history is long (>12,000 commits), early-exit grep triggers SIGPIPE in upstream writer, causing false `progressing-weak (basis=row-C)` instead of `progressing`. | **Scope Trap:** Attempting to fix F01 with another pipe (e.g. `head` or `awk | grep`). The only valid structural fix is **capture-then-match** (in-memory variable / here-string / file capture) with explicit `PIPESTATUS` or here-string feeding `grep -Fxq`. |
| **Q15** (`QUALITY.md:29-30`, M13) | `corpus/lessons/round-12.md#M13`<br>Journal class counted from arbitrary text grep instead of structured `MESSAGE_ID` or trusted metadata field. | **C1:** Current `probe_journal` greps text for `'Out of memory|oom-kill|Killed process'` and `'status=9/KILL'`. Text grep falsely matched unrelated userland noise or missed signals (e.g. 0 segfaults via text vs 656 via `COREDUMP_SIGNAL=11`). | **Scope Trap:** Grepping the `MESSAGE` field inside JSON, or trusting user-provided text. Must query trusted structured field `MESSAGE_ID` directly via `journalctl MESSAGE_ID=<id>` with `--output-fields` restricting payload, never parsing `MESSAGE`. |
| **Q16** (`QUALITY.md:31-32`, M19) | `corpus/lessons/round-12.md#M19`<br>Notice ≠ event, and independent scopes were summed. Host fact: 5 kernel kills vs 7 user + 9 system `fe6faa94…` notices in the same boot. | **C1:** Units are strictly **notices**, not killed processes. Scopes (`user` vs `system`) represent distinct collection planes and must **never be summed**. | **Scope Trap:** Combining user notices with system notices into a single aggregate count, or reporting "X processes killed" based on catalog notices. Must report separate fields: `notice_user_oom` and `notice_system_oom`. |
| **Q20** (`QUALITY.md:39-40`, M6) | `corpus/lessons/round-12.md#M6`<br>Tallies cited in reports/scorecards disagree with delivered artifacts recomputed at the carrying commit. | **C1 & C2:** Fixture counters, oracle total counts (e.g. 28 cases), and registered selftests (e.g. 77 cases) must exactly match delivered counts at the carrying commit. | **Scope Trap:** Stating expected improvements (e.g. "oracle matched 30/30" or "reconstructed 10 kills") without recomputing from frozen artifacts and verified gate output. |

---

## 3. Scope Traps & Boundary Traps Identified

### Scope Trap 1: Conflating Structured Userspace Notices with Kernel Kill Records
* **The Illusion:** Believing that counting `fe6faa94e7774663a0da52717891d8ef` (`systemd` OOM kill notice) gives an authoritative count of kernel OOM kills.
* **The Reality:** 
  - Upstream Linux kernel increments `OOM_KILL` in `mm/oom_kill.c:935-936` (S003). That is the kernel victim accounting site.
  - `systemd` catalog notice `fe6faa94...` (S013 line 604) is generated per-unit when systemd detects a unit exit or OOM event. One kernel OOM kill can fan out into multiple unit notices across system and user manager instances. Conversely, cgroup kills or userspace kills may generate notices without kernel OOM killer invocation.
  - Therefore, `fe6faa94...` notices **are notice units**, not process kill units. They must be recorded under explicit scope labels (`scope=user`, `scope=system`) and **never added together**.

### Scope Trap 2: Conflating Host/OS Health with Fleet Health
* **The Illusion:** Grepping general system logs for OOM or failure events and attributing them as fleet failures.
* **The Reality:** 
  - Unscoped system journal queries capture desktop/session background noise (e.g., desktop browser tabs, `pipewire-pulse.service`).
  - Mori's province (`PROVINCE.md`) is fleet progress and silence detection, not general OS triage (which belongs to `tsukuroi-shokunin`).
  - System-scoped notices must be clearly identified and not automatically assigned as fleet blame unless correlated with a fleet cgroup/unit.

### Scope Trap 3: Self-Attested Verification vs. Non-Author Spotcheck (M10 / Q10)
* **The Illusion:** An internal subagent (like `ClaimConnections` or a reviewer subagent in the same lane wave) declaring "Verification passed; discernment improved."
* **The Reality:** 
  - `LEARNING.md:42-43` and `round-12.md#M10` firmly establish: *A subagent dispatched by the lane is still the lane.* Self-attestation is not an external audit.
  - Verification of discernment and gate conformance strictly requires an outside non-author spotcheck (conducted post-landing by L1 or orchestrator). Leaf agents must only propose concrete verification checks, leaving execution to L1.

### Scope Trap 4: Over-Broad Deletion of Signal / Unit Failure Observability
* **The Illusion:** In the name of fixing Q15 (text grep), completely dropping `unit_failure` and `kill_signal` from the census output, breaking downstream consumers or masking real unit failures.
* **The Reality:** 
  - As flagged in peer coordination, silently dropping legacy fields breaks backwards compatibility and schema expectations.
  - Proper evolution retains structured indicators (e.g. querying structured exit statuses or isolating fleet units) while clearly delineating between fleet units and desktop/OS units.

---

## 4. The One Non-Obvious Move: Dual-Scoped Structured Notice Decoupling with Strict Oracle Grammar Assertion

### Proposed Move
Synthesize the C1 and C2 requirements into an atomic contract enhancement:
1. **In `tools/mori-census.sh` (`probe_journal` & `ps_authorship`):**
   - **For C1:** Refactor `probe_journal` to execute distinct, isolated queries:
     * User scope: `$JOURNALCTL_BIN --user -b --no-pager -o json --output-fields=_BOOT_ID,MESSAGE_ID MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`
     * System scope: `$JOURNALCTL_BIN --system -b --no-pager -o json --output-fields=_BOOT_ID,MESSAGE_ID MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` (gracefully handling permission errors as `unavailable (system_journal=eacces)` without failing rc).
     * Retain COREDUMP structured query (`COREDUMP_SIGNAL=11`).
     * Emit findings that distinguish unit notices from kills:
       `SURFACE journal: ok cmd=...; notice_user_oom=$c_user_oom notice_system_oom=$c_sys_oom segfault=$c_seg ...`
   - **For F01:** In `tools/mori-census.sh:1494`, replace:
     ```bash
     if printf '%s\n' "$inwin" | sed -E 's/^[0-9]+ //' | grep -Fxq -- "$lane-shokunin <$lane@shokunin.local>"; then
     ```
     with a safe **capture-then-match** construct (using here-string and avoiding pipeline SIGPIPE under pipefail):
     ```bash
     authors=$(printf '%s\n' "$inwin" | sed -E 's/^[0-9]+ //')
     if grep -Fxq -- "$lane-shokunin <$lane@shokunin.local>" <<< "$authors"; then
     ```
     Because `$authors` is fully captured into a shell variable before `grep` runs, `grep`'s early exit (`-q`) cannot close a live pipe to an upstream producer.

2. **In `tools/mori-silence-cases.sh` (Oracle F02):**
   - Tighten `assert_case` (and all shape/read-only cases) from loose grep `^MORI_CENSUS:` to exact grammar and cardinality:
     * Exactly **one** verdict line matching `^MORI_CENSUS: (CLEAN|DRIFT) \(findings=[0-9]+ drift=[0-9]+ unavailable=[0-9]+ surfaces=[0-9]+\)$`.
     * Strict exit-code consistency: `CLEAN` must have rc=0; `DRIFT` must have rc=1.
     * Reject `BANANA`, duplicate verdict lines, missing verdict lines, or rc/verdict mismatches.

### Why this is Non-Obvious
Most attempts treat F01 (SIGPIPE in long history) and F02 (oracle accepting BANANA) as separate bug fixes, while treating C1 as a cosmetic string swap in `probe_journal`.
In truth, they share the identical underlying failure mode: **the breakdown of pipeline contract boundaries**.
- F01 breaks because an unchecked streaming pipe in `bash` truncates producer output upon consumer early exit.
- F02 breaks because the oracle was verifying stream presence rather than strict terminal state grammar.
- C1 breaks because unstructured stream parsing (`grep` on log text) conflates disparate event types and scopes.

Unifying them under **strict bounded capture and structured contract validation** solves all three without introducing new runtime dependencies or altering fleet interfaces.

---

## 5. Affected Axes Analysis

| Axis | Status | Impact Analysis |
|---|---|---|
| **Coverage** | **Improves (6 → 7)** | C1 transitions journal inspection from unprincipled text grep to exact, verifiable structured MESSAGE_ID counts across both user and system manager planes. Avoids blind spots where signal text differs from format expectations. |
| **Operability** | **Improves (6 → 7)** | C2 fixes F01 (preventing valid progressing lanes with large commit histories from being falsely downgraded to `progressing-weak` due to SIGPIPE) and fixes F02 (hardening the oracle so it can never be fooled by synthetic or spoofed BANANA verdicts). |
| **Depth** | **Harmless (Held at 5)** | Backed by anchored primary sources S003 (`oom_kill.c`), S013 (`systemd.catalog`), S014 (`journalctl`), S015 (`journal-fields`), and S031 (`pipe(7)`). No ungrounded claims. |
| **Calibration** | **Harmless (Held at 6)** | Keeps negative controls explicit; does not claim self-attested external discernment; leaves spotcheck verification to non-author L1 evaluation. |
| **Freshness** | **Harmless (Held at 5)** | Does not tamper with the pinned `baseline-r10-20261015T2231Z.json`; all changes are schema-transparent or isolated to counter keys registered with appropriate masks. |
| **Adjacency** | **Harmless (Held at 6)** | Preserves clear boundary with `tsukuroi-shokunin` (OS vs fleet scope) and `kama-shokunin`. |

---

## 6. Risks & Second-Order Effects

1. **System Journal Permission Boundary:**
   - *Risk:* On non-root execution, `journalctl --system` may exit with rc 1 or permission denied (`EACCES`).
   - *Mitigation:* `probe_journal` must check the return code and stderr. If system journal access is denied, record `notice_system_oom=unavailable` or `0 (unreadable)`, without failing the entire census or corrupting rc.
2. **Oracle Case Rigidity:**
   - *Risk:* Hardening the oracle verdict regex might break legacy tests if any test expects a subtle variation in findings/surfaces formatting.
   - *Mitigation:* Anchor the regex strictly to the canonical grammar emitted by `tools/mori-census.sh:1785-1795` (`MORI_CENSUS: (CLEAN|DRIFT) (...)`).
3. **Subprocess Buffer Bloat:**
   - *Risk:* Capturing 12,000 commits into a shell variable in `ps_authorship` consumes memory.
   - *Mitigation:* The capture is strictly scoped to `inwin` (commits within the post-launch window `(launch, NOW]`), which is already bounded and filtered by `awk` before authorship inspection.

---

## 7. Concrete Verification Steps for L1 (Non-Author Execution)

*Per contract, this seat does not execute test runs. The following checks are designated for L1 integrated verification:*

1. **F01 Long-History Regression Test:**
   - Run the Appendix B fixture generator (`audit-r11.md:315-362`) with 12,000 sibling commits following one lane commit.
   - Verify `EXPECTED=progressing`: `SURFACE lane.kagi: progressing (basis=row-B ...)` and rc=0, with zero `progressing-weak` downgrades.
2. **F02 BANANA Rejection Test:**
   - Run the Appendix C wrapper (`audit-r11.md:382-391`) against `tools/mori-silence-cases.sh`.
   - Verify oracle reports failures on every case (`matched=0 total=28`), rejecting the `BANANA` replacement.
3. **C1 Structured Journal Scope Verification:**
   - Run `tools/mori-census.sh` with synthetic journalctl stubs providing `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` entries.
   - Confirm user and system notice counts appear in `SURFACE journal` as distinct fields without summation.
4. **Harness Conformance:**
   - Verify pristine selftest passes 77/77 (`bash tools/mori-census.sh --selftest`).
   - Verify pristine oracle passes 28/28 (`bash tools/mori-silence-cases.sh`).
