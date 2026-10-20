# Mori Round 13 — Bounded Planning Data-Walk

**Role:** MoriR13.PlanningWalk (Scout)  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Milestone:** Round 13 structured scopes and verdict integrity  
**Assigned Deliverable:** `.ufo/waves/round-13/build/PlanningWalk.md`  
**Grounding Sources:** `SCORECARD.md`, `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/knowledge/audit-r11.md`, `corpus/knowledge/kill-classes-by-message-id-r12.md`, `corpus/knowledge/kernel-oom-line-attribution-r12.md`, `corpus/lessons/round-12.md`, `corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md`.

---

## 1. Mapping of Current Scorecard Planned Round 13

In `SCORECARD.md` (lines 639–650), Round 12 registered the following three planned directions for Round 13:

1. **Freshness — Re-pin after classification:**
   - *Scorecard Text:* "before `--drift baseline-r10-20261015T2231Z.json` exit 1 (classified tokens); after a new baseline file pinned with a recorded reason, old file kept, `--drift <new>` → `MORI_DRIFT: none` exit 0. Falsified by any unclassified token."
   - *Status & Assessment:* In Round 12, drift classification (`corpus/evidence/drift-r12-20261019T2204Z-classification.md`) showed the drift was due to normal host aging (new boot, souji sweep, aggregator row-B → row-C, and 14 new lane rows). Re-pinning was intentionally deferred to Round 13.
   - *Planning Recommendation:* **Do NOT execute a blanket re-pin prior to settling C1.** C1 alters the schema of `SURFACE journal` and its emitted findings. Re-pinning before C1 lands would either record obsolete journal schema or disguise semantic drift. Re-pinning must remain an explicit, recorded act (QUALITY Criterion 10, Mistake M15) with an exact mask for non-volatile fields.

2. **Operability — Close Audit F01/F02 (Milestone C2):**
   - *Scorecard Text:* "before, the long-history fixture grades `progressing-weak` despite a lane commit and the BANANA verdict wrapper scores 28/28; after, the fixture grades `progressing` and the wrapper fails while the honest oracle stays 28/28."
   - *Status & Assessment:* Directly adopted into Round 13 Milestone C2. Audit F01 (production SIGPIPE authorship loss) and F02 (oracle verdict-word/rc-consistency blind spot) are fully characterized with minimal reproducible fixtures in `corpus/knowledge/audit-r11.md` Appendices B and C. Both are mature, verified defects ready for surgical repair.

3. **Coverage (Frontier → Core) — FR1 (Milestone C1):**
   - *Scorecard Text:* "FR1: a MESSAGE-free system-journal kernel-OOM count probe with its own finding id; before 0 kernel-OOM records visible to the census, after the 5 retained records counted with `unavailable` when the system journal is unreadable."
   - *Status & Assessment:* Operationalized into Milestone C1: "replace text journal classes with MESSAGE-free structured MESSAGE_ID counts in independently labeled user and system scopes (notice units, never fleet-caused kill counts)." Grounded by Round 12 knowledge entries (`kill-classes-by-message-id-r12.md` and `kernel-oom-line-attribution-r12.md`).

---

## 2. Lowest Owned Scores & Headroom Analysis

Mori owns exactly two axes: **coverage** and **operability** (fleet-2). The six scored axes at Round 12 baseline (`SCORECARD.md:607-615` and post-review corrections `:651-656`) stand as follows:

| Axis | Ownership | Round 12 Score | Round 12 Verdict | Headroom to Saturation (8/10) | Notes |
|---|---|---|---|---|---|
| **coverage** | **Owned** | **6** | improved (5 → 6) | **+2** (Headroom available) | Increased in r12 via roster expansion (9 → 23 lanes). Current lowest owned score. |
| **operability** | **Owned** | **6** | unchanged (6 held) | **+2** (Headroom available) | Selftest 77/77 PASS, oracle 28/28 PASS, but F01/F02 open and wall time ~4.3s without budget. Current lowest owned score. |
| depth | Observed | 5 | improved (4 → 5) | N/A | S001–S034 source registry established in r12. |
| calibration | Observed | 5 | improved (score 5 held) | N/A | Post-review correction: held at 5 because non-author reviewer could not re-derive 6. |
| freshness | Observed | 5 | unchanged (5 held) | N/A | Drift pin aging classified; re-pin pending. |
| adjacency | Observed | 6 | unchanged (6 held) | N/A | Post-review correction: contract repair was unclaimed, score held. |

### Headroom & Stagnation Summary:
- **Lowest Owned Scores:** Both owned axes (`coverage` and `operability`) sit at **6**.
- **Saturation Line:** Set to **8/10** on both owned axes (`SCORECARD.md:635`). There is clear room (+2) on both axes.
- **Stagnation Window (N=3):** Round 12 added the `source registry` capability. Moving coverage and operability in Round 13 advances the lane well within the 3-round window without plateauing.
- **Axis Move Target for Round 13:**
  - Coverage: 6 → 7 (via C1: structured MESSAGE_ID scopes replacing text greps).
  - Operability: 6 → 7 (via C2: fixing F01 SIGPIPE production bug and F02 oracle verdict integrity).

---

## 3. Causal Independence Analysis: C1 (Coverage) vs C2 (Operability)

A key architectural question for planning Round 13 is whether C1 and C2 can be implemented, tested, and verified independently without cross-coupling.

### 3.1. Architectural Separation
- **C1 Scope (`tools/mori-census.sh:probe_journal()`):**
  - Replaces text greps (`grep -ciE 'Out of memory|oom-kill...'`) with structured journalctl queries using catalog `MESSAGE_ID` values (`fe6faa94e7774663a0da52717891d8ef`, `d989611b15e44c9dbf31e3c81256e4ed`, `fc2e22bc6ee647b6b90729ab34a250b1`).
  - Separates queries into independent `--user` and `--system` journal scopes.
  - Enforces `notice` units (systemd unit kill notices), never summing user and system counts, and never claiming process kill attribution.
  - Strictly restricts `--output-fields=` to non-`MESSAGE` fields (`_BOOT_ID`, `MESSAGE_ID`, `_TRANSPORT`), guaranteeing zero leak of raw `MESSAGE` payloads.
  - Emits `SURFACE journal` and journal-specific findings (`OOM_KILL_JOURNAL`, `KILL_SIGNAL_JOURNAL`, `UNIT_FAILURE_JOURNAL`, etc.).
- **C2 Scope:**
  - **F01 (`tools/mori-census.sh:grade_lane()`):** Operates exclusively within the git log authorship analysis (`inwin` processing). It evaluates committer timestamps and author identities (`%ct %an <%ae>`) within the git repository. It does not invoke `journalctl`, inspect cgroups, or read `probe_journal` findings.
  - **F02 (`tools/mori-silence-cases.sh:assert_case()`):** Operates inside the silence oracle test harness. It grades the final roll line `MORI_CENSUS: CLEAN|DRIFT` emitted on stdout by `tools/mori-census.sh`. During silence oracle case execution, `journalctl` is stubbed out (`journalctl: exit 0` or quiet JSON), producing zero journal findings.
- **Coupling Assessment:**
  - `grade_lane()` (F01) has zero dependencies on `probe_journal()` (C1).
  - `tools/mori-silence-cases.sh` (F02) stubs the journal environment; changing journal queries from text to MESSAGE_ID has zero effect on the 28 silence cases.
  - Conversely, repairing F01 (git authorship) and F02 (oracle verdict regex) does not alter the journal probe's behavior or data structures.
  - **Verdict:** C1 and C2 are **strictly causally independent**. They can be developed by parallel executor seats without semantic collision.

---

## 4. Deep Walk of Known Defects (F01, F02) and Frontier (FR1)

### 4.1. Defect F01: Production Long-History SIGPIPE Authorship Loss
- **Evidence & Location:**
  - Reported: `audit-r11.md:156` (Finding F01, Defect Category D01).
  - Reproducer: `audit-r11.md:308-375` (Appendix B).
  - Code Anchor: `tools/mori-census.sh:1494-1498` (originally `:1366-1374` at Round 11):
    ```bash
    if printf '%s\n' "$inwin" | sed -E 's/^[0-9]+ //' | grep -Fxq -- "$lane-shokunin <$lane@shokunin.local>"; then
      subj=1
    else
      sib=1
    fi
    ```
- **Root Cause & Mechanism:**
  - Script runs under `set -eo pipefail`.
  - When `inwin` contains an exact subject commit followed by thousands of sibling commits (Appendix B reproduces with 12,000 commits), `grep -Fxq` finds the exact match on the very first line and exits immediately (rc 0).
  - Exiting immediately closes `grep`'s standard input pipe.
  - Upstream `sed` and `printf` continue writing subsequent lines to the broken pipe and receive `SIGPIPE` (signal 13, exit status 128 + 13 = `141`).
  - Under `pipefail`, a non-zero exit code in the pipeline causes the entire pipeline to return `141`.
  - The `if` test evaluates to false; execution falls into `else sib=1`.
  - Result: Active lane with valid commit is wrongly graded `progressing-weak (basis=row-C)` instead of `progressing (basis=row-A)`.
- **Governing Standard:** QUALITY Criterion 7 / Lesson `2026-10-15-selftest-grep-sigpipe-race.md:202-203`: "No live producer pipe feeds a match test; capture once and assert over the captured bytes (SIGPIPE 141 ≠ 1)."
- **Resolution Approach:**
  - Do not pipe a live producer into an early-exiting `grep -q`.
  - Parse or match via `awk` directly on `$inwin` in a single pass without early exit, or read into a here-string without a pipeline.

### 4.2. Defect F02: Oracle Verdict-Word and Consistency Blind Spot
- **Evidence & Location:**
  - Reported: `audit-r11.md:157` (Finding F02, Defect Category D02).
  - Reproducer: `audit-r11.md:376-397` (Appendix C).
  - Code Anchor: `tools/mori-silence-cases.sh:569-585, 980-985`:
    ```bash
    verdict=$(printf '%s\n' "$CASE_OUT" | grep -m1 '^MORI_CENSUS:' || true)
    ```
- **Root Cause & Mechanism:**
  - The silence oracle only checked for the literal presence of prefix `^MORI_CENSUS:`.
  - It did not validate:
    1. Verdict vocabulary (`CLEAN` vs `DRIFT`).
    2. Format completeness (`(findings=N drift=M unavailable=U surfaces=S)`).
    3. Cardinality (exactly one verdict line; 0 is missing, >1 is ambiguous/duplicate).
    4. Return code agreement (`CLEAN` requires rc 0; `DRIFT` requires rc 1).
  - Appendix C demonstrated an adversarial wrapper intercepting the census output and substituting `MORI_CENSUS: BANANA` for `CLEAN`/`DRIFT`: the oracle still reported `matched=28 total=28 exit 0`.
- **Governing Standard:** QUALITY Criteria 8 & 26 (Criteria added Round 13): "A final census verdict is exactly one complete `MORI_CENSUS: CLEAN|DRIFT` record, and its roll agrees with exit 0|1 respectively; a prefix, arbitrary word, duplicate roll, or mismatched rc is rejected."
- **Resolution Approach:**
  - Introduce `verdict_grade()` validating:
    - Exactly one line matching `^MORI_CENSUS: (CLEAN|DRIFT) \(findings=[0-9]+ drift=[0-9]+ unavailable=[0-9]+ surfaces=[0-9]+\)$`.
    - `CLEAN` must have `$CASE_RC -eq 0`.
    - `DRIFT` must have `$CASE_RC -eq 1`.
  - Apply `verdict_grade()` across all cases: `assert_case`, `case_readonly_no_mutation`, and `case_shape_invariance`.

### 4.3. Frontier FR1: Structured Scopes and Notice Units
- **Evidence & Grounding:**
  - PROVINCE.md:31 (FR1 definition).
  - `corpus/knowledge/kernel-oom-line-attribution-r12.md:10-16` (S003, S004, S014, S015).
  - `corpus/knowledge/kill-classes-by-message-id-r12.md:10-16` (S013, S014, S015).
- **Core Principles & Boundaries:**
  1. **Structured MESSAGE_ID vs Text Grep:**
     - `fe6faa94e7774663a0da52717891d8ef`: systemd unit OOM kill notice ("A process of @UNIT@ unit has been killed by the OOM killer.").
     - `d989611b15e44c9dbf31e3c81256e4ed`: systemd-oomd notice ("one or more processes in unit").
     - `fc2e22bc6ee647b6b90729ab34a250b1`: systemd coredump notice (informational).
  2. **Scopes are Independent:**
     - User journal (`--user`) and system journal (`--system` / `-k`) must be reported as separate counts and separate fields.
     - Never sum user and system scopes (QUALITY Criterion 16).
  3. **Unit is Notice, Never Kill Count:**
     - A unit notice records that a systemd unit observed a kill event. One kernel OOM kill can trigger notices across multiple units/scopes.
     - A notice is NOT a 1:1 count of killed processes. Mori does NOT claim fleet-caused process kill attribution.
  4. **Strict Field Restriction (Zero MESSAGE Leakage):**
     - Queries must use `--output-fields=_BOOT_ID,MESSAGE_ID,_TRANSPORT` or non-`MESSAGE` fields.
     - Raw journal `MESSAGE` text must never be printed, emitted in findings, or grep-searched.
  5. **Degradation / Unavailability Semantics:**
     - If `--system` journal is unreadable (permissions/ENOENT), report `unavailable`, never 0 or crash exit (QUALITY Criteria 6 & 14, Mistake M14).

---

## 5. Minimum Correct Scope Recommendation (No New Claim)

To maximize correctness, maintainability, and ensure clean pass through verification by L1, Round 13 must strictly adhere to the following bounded scope:

### In Scope for Round 13:
1. **Milestone C1 (Coverage):**
   - In `tools/mori-census.sh:probe_journal()`:
     - Replace regex/text searching with structured catalog `MESSAGE_ID` queries.
     - Split journal reporting into explicit, distinct scopes: `user_notices` and `system_notices` (or explicitly labeled fields).
     - Guard system-journal readability: if `journalctl --system` returns non-zero / permission denied, emit `unavailable` for the system scope without crashing or fabricating zero.
     - Ensure zero `MESSAGE` payload is queried or output.
     - Update selftest cases to assert structured journal notice counts and unreadable fallbacks.
2. **Milestone C2 (Operability):**
   - In `tools/mori-census.sh:grade_lane()` (F01):
     - Replace `printf ... | sed ... | grep -Fxq` with a capture-safe check (e.g., awk exact string match over `$inwin` in one process without piping into an early-exit consumer).
     - Verify with a 12,000-line synthetic history fixture (faithful to Appendix B) that `progressing` is preserved.
   - In `tools/mori-silence-cases.sh` (F02):
     - Implement `verdict_grade()` asserting exact regex match, single-line cardinality, and exit-code concordance (`CLEAN:0`, `DRIFT:1`).
     - Wire `verdict_grade()` into `assert_case()`, `case_readonly_no_mutation()`, and `case_shape_invariance()`.
     - Verify rejection of BANANA wrapper, duplicate verdicts, missing verdicts, and roll/rc mismatches, while keeping honest census runs at 28/28 PASS.
3. **Knowledge & Criteria (Discipline):**
   - Update `corpus/QUALITY.md` with Criteria 26, 27, 28 (verdict integrity, long-history capture, canonical seed conformance).
   - Document the F01/F02 mechanisms and structured scope semantics in knowledge notes.

### Strictly Out of Scope (Preventing Scope Creep):
- **NO Freshness Re-pin this round:** Do not create a new `baseline-r13.json` or rewrite `baseline-r10-20261015T2231Z.json`. Any drift induced by C1's schema changes must be documented and masked; a re-pin is a dedicated, post-settlement act.
- **NO New Claims outside C1/C2:**
  - Do not claim kernel-level process victim attribution to fleet lanes.
  - Do not claim eBPF tracing (FR13 remains frontier).
  - Do not introduce instantaneous disk write-rate (FR6 remains deferred).
  - Do not alter silence grading state vocabulary (keep `silent`, `progressing`, `progressing-weak`, `young`, `not-open`, `unavailable`).
  - Do not modify the 28 registered silence case ids or expected states in `tools/mori-silence-cases.sh`.

---

## 6. Actionable Checklist for L1 Verification & Integration

When subagents conclude their assigned edits, L1 should execute the following integrated verification battery:

1. **Selftest Suite:**
   - Command: `bash tools/mori-census.sh --selftest`
   - Expected: All selftest cases pass (including new structured journal and F01 long-history cases), exit 0, stderr 0 B.
2. **Silence Oracle (Honest Run):**
   - Command: `bash tools/mori-silence-cases.sh`
   - Expected: `MORI_SILENCE_CASES: matched=28 total=28`, exit 0, stderr 0 B, `SHUFFLE_SEED` printed after case loop.
3. **F01 Regression Check (Appendix B Replay):**
   - Command: Execute isolated Python/bash fixture with 1 subject commit + 12,000 sibling commits.
   - Expected: `SURFACE lane.kagi: progressing (basis=row-A)`, exit 0 (NOT `progressing-weak basis=row-C`).
4. **F02 Adversarial Attacks (Appendix C Replay):**
   - Command: Run oracle against BANANA wrapper, missing verdict wrapper, duplicate verdict wrapper, and CLEAN-rc1 wrapper.
   - Expected: Every adversarial wrapper rejected with `FAIL <id>: MORI_CENSUS verdict ...`, oracle exits 1.
5. **Zero `MESSAGE` Leakage Scan:**
   - Command: `grep -n 'MESSAGE' tools/mori-census.sh`
   - Expected: References only in comments or as `MESSAGE_ID`, zero extraction of `MESSAGE=` payload.
6. **PROVINCE & Scope Boundaries:**
   - Expected: No writes outside lane root, no credentials, no fleet-root contamination.
