# Protected Inventory & Conformance Report: Operator Lessons, Aggregator/Non-Author Artifacts, Protected Paths, and SHONEN Canonical Condition

**Seat:** `MoriR13.ProtectedInventory`  
**Role:** UFO-FSD scout  
**Axes:** coverage, operability  
**Date:** 2026-10-20  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Target File:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-13/build/ProtectedInventory.md`  

---

## 1. Executive Summary & Named Axes

- **Named axes**:
  - **Coverage (C1)**: Structured journal scope replacement for unstructured text parsing. Ensuring protected paths, canonical seeds, and historical lessons are inventoried without contamination or mutation.
  - **Operability (C2)**: Preserving exact gate integrity, append-only rules, and canonical seed formats without introducing spurious diffs, unverified promotions, or broken references.
- **Scope & Mandate**:
  - Read-only inventory of operator lessons, non-author reviews, and aggregator reports across the fleet and lane.
  - Identification of protected paths and their inherited states.
  - Verification of the `SHONEN.md` canonical condition against upstream protocol templates.
  - **No production code changes** made by this seat.

---

## 2. Inventory of Operator Lessons

Operator lessons and post-round review artifacts were identified read-only via globbing across `mori-shokunin/corpus/lessons/`, `mori-shokunin/considerthese/`, and the fleet root:

### 2.1 Lane-Level Lessons (`mori-shokunin/corpus/lessons/`)
1. `2026-10-15-free-lunch-measurements-counter-baselines.md` (origin: round 1/2) — Cumulative counters must carry baseline anchors (boot, instance creation, process start).
2. `2026-10-15-settle-evidence-references-with-artifacts.md` (origin: round 2) — Settle references against carrying commit; errata are append-only.
3. `2026-10-15-volatile-contract-behavioral-baselines.md` (origin: round 2) — Baseline declarations must include volatile mask, window, and gate SHA.
4. `2026-10-15-selftest-grep-sigpipe-race.md` (origin: round 9) — Consumer early exit (`grep -q`) triggers SIGPIPE (141) in writer under `pipefail`; capture-then-match required.
5. `2026-10-15-probe-pricing-dwell-bounds-filter-drop.md` (origin: round 7/8) — Four prices for deferred probes (found-ness, wall time, bound, filter drop).
6. `2026-10-15-run-secret-timing-and-content-freshness-limits.md` (origin: round 6) — Secrets emitted after case loop; content salting.
7. `2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` (origin: round 5) — Fisher-Yates case shuffle + triple-channel run nonce.
8. `2026-10-15-forgeable-oracle-visible-fixtures.md` (origin: round 4) — Opaque directories, elimination of fixture leaks.
9. `2026-10-15-errexit-pipefail-silent-crash.md` (origin: round 3) — rc gating on every probe; crash rc must never collide with DRIFT verdict.
10. `2026-10-15-oracle-honesty-crash-masking.md` (origin: round 3) — Pre-registered expected gradients distinguish repairs from masks.
11. `round-12.md` (origin: round 12) — Comprehensive mining of mistakes M1–M26 across rounds 1–11.
12. `round-12-verifier-spotcheck.md` (origin: round 12, non-author orchestrator) — Independent adjudication by `W3ReviewMori` under campaign binding.

### 2.2 Operator Reflections (`mori-shokunin/considerthese/`)
1. `2026-10-19.md` — Daily reflection on rounds 7–11: self-test reliability fix, drift pinning, doc drift recurrence, and saturation obligations.

---

## 3. Inventory of Non-Author and Aggregator Files

Non-author reviews and cross-lane aggregator reports represent external evaluations and must never be treated as lane-dispatchable seats:

### 3.1 External Reviews & Critic Reports (`.ufo/waves/kaika-w3/`)
- `.ufo/waves/kaika-w3/mori-review.md`: Non-author verification report by `W3ReviewMori` (fresh orchestrator task) on lane commit `1f07f1dd1`. Admitted with corrections C1–C6; held calibration at 5; verified coverage 9→23 and selftest 77/77.
- `.ufo/waves/kaika-w3/mori-critic.md`: Adversarial critique by `W3CriticMori` on S013 catalog quotes, calibration metrics, and `MORI_ROSTER_LANES` override handling.
- `.ufo/waves/kaika-w3/aggregate-review.md`: Fleet-level aggregation review across all 21 active and physical lanes.

### 3.2 Aggregator Fleet Reports (`.ufo/reports/`)
- `.ufo/reports/AGGREGATE.md` (root & round-12): Fleet-wide summaries of lane health, round counts, and promotion readiness.
- `.ufo/reports/round-12/aggregator.md`: Aggregator lane round report evaluating cross-lane corpus and boundary compliance.
- `.ufo/reports/round-12/SOURCES.md`: Fleet-wide source registry census.

---

## 4. Protected Paths & Inherited State

Under shokunin operating protocols (`PROTOCOL.md`, `CORPUS.md`, `AGENTS.md`), specific repository paths are strictly protected:

| Protected Path / Scope | Mutability Rule | Current Inherited State at Round 13 Start |
|---|---|---|
| `LOG.md` | **Append-only** | Clean. Prior round blocks (rounds 1–12) intact. Round 13 entry pending L1 integration. |
| `corpus/lessons/` | **Append-only / Frozen** | Clean. Existing lessons (12 files) frozen. No prior lines modified. |
| `corpus/QUALITY.md` | **Append-only** | Clean at HEAD (`1f07f1d`). Working tree carries uncommitted append of criteria 26–28 for round 13. |
| `PROVINCE.md` | **Strict Boundary** | Clean. Governs domain limits (read-only observability; no OS/remediation actions). |
| `SHONEN.md` | **Canonical Seed Only** | **Indentation Drift in Working Tree** (see Section 5 below). HEAD matches template. |
| `corpus/SOURCES.md` | **Contract v1 Enforced** | Clean at HEAD (`1f07f1d`). Working tree carries minor anchor adjustments. |
| `.ufo/state/` | **Driver Runtime** | Untracked / Churn. Driver-managed runtime; never committed by lane. |
| Fleet Root (`/home/vgpnk/Projects/shokunin/`) | **Read-Only to Child Lanes** | Strict read-only boundary respected. No writes outside mori lane root. |

---

## 5. SHONEN.md Canonical Condition Analysis

### 5.1 Protocol Specification & Canonical Seed Template
Per `PROTOCOL.compact.md:370-380` and `.ufo/waves/round-13/shonen-seed.txt`:
```markdown
    # <name> — Promotion checklist

    Promotion to shokunin requires all of:

    - [ ] SKILL.md contains real decision tables, error patterns, checklists, cited sources
    - [ ] At least one end-to-end domain task executed and logged in LOG.md
    - [ ] Instructions executable by an agent without oral context
    - [ ] No cross-domain bleed (PROVINCE.md still accurate)
```
- In `PROTOCOL.md:400-407`, the template is presented as a 4-space indented block under the explanation paragraph.
- The canonical file content inside a lane's repository root must be the **de-indented** 8 lines (or indented only if the canonical protocol template itself mandates 4-space markdown indentation for the raw file).

### 5.2 Observed Working Tree vs HEAD State
- **HEAD (`1f07f1d`)**:
  ```markdown
  # mori-shokunin — Promotion checklist

  Promotion to shokunin requires all of:

  - [ ] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  - [ ] At least one end-to-end domain task executed and logged in LOG.md
  - [ ] Instructions executable by an agent without oral context
  - [ ] No cross-domain bleed (PROVINCE.md still accurate)
  ```
  *Status at HEAD*: Flush to column 0. Exactly 8 lines.
- **Working Tree (`SHONEN.md`)**:
  `git diff SHONEN.md` shows:
  ```diff
  - # mori-shokunin — Promotion checklist
  +     # mori-shokunin — Promotion checklist
  - Promotion to shokunin requires all of:
  +     Promotion to shokunin requires all of:
  - - [ ] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  - - [ ] At least one end-to-end domain task executed and logged in LOG.md
  - - [ ] Instructions executable by an agent without oral context
  - - [ ] No cross-domain bleed (PROVINCE.md still accurate)
  +     - [ ] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  +     - [ ] At least one end-to-end domain task executed and logged in LOG.md
  +     - [ ] Instructions executable by an agent without oral context
  +     - [ ] No cross-domain bleed (PROVINCE.md still accurate)
  ```
  *Observed Drift*: All lines in the working copy were indented with 4 leading spaces (matching the verbatim block quote in `PROTOCOL.md` rather than the un-indented file format).

### 5.3 Promotion & Verifier Status
- Under `PROTOCOL.md:63-68` and `round-12-verifier-spotcheck.md`:
  - Promotion marks `[x]` require a **named non-author verifier**.
  - All round-13 swarm seats (`MoriR13.*`) are dispatched by the lane and remain "the lane".
  - Therefore, no round-13 seat may mark `[x]`. Any self-asserted readiness must use `[~]` with an explicit evidence pointer, or leave `[ ]`.
  - Canonical condition requires that `SHONEN.md` retains `[ ]` until an external non-author verifier is formally dispatched by the orchestrator.

---

## 6. Findings & Recommendations for L1

1. **Restore Canonical `SHONEN.md` Format**:
   - The working-tree 4-space indentation change on `SHONEN.md` renders the file as a markdown code block rather than document headers and checklists.
   - Recommended L1 action: Revert `SHONEN.md` to column-0 indentation matching HEAD (`git checkout HEAD -- SHONEN.md` or de-indent 4 spaces) before finalizing the round-13 commit.
2. **Preserve Append-Only Rules on Protected Paths**:
   - Ensure that `corpus/QUALITY.md` criteria 26–28 are appended strictly at the tail without rewriting criteria 1–25.
   - Ensure that `LOG.md` entry for round 13 is appended strictly at the tail.
3. **Report Status**:
   - No changes made to production scripts or documents by this seat.
   - All findings grounded in file paths and exact git diff records.
