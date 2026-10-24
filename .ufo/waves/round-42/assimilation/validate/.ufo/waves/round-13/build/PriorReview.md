# PriorReview Scout Report: Round 12 Verifier, Post-Review Fixes, Disagreements & Routed Defects

**Seat:** `MoriR13.PriorReview` (Scout)  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Milestone:** Round 13 structured scopes and verdict integrity  
**Axes Judged:** Coverage, Operability  
**Task:** Read round-12 verifier plus post-review fixes; identify every disagreement / routed defect still owed and exact criterion / fix. Do not reinterpret self-attestation as outside review. Write only assigned findings to `.ufo/waves/round-13/build/PriorReview.md`. Do not run verification.

---

## 1. Executive Summary & Verification Provenance

### 1.1 Non-Author Review vs. Self-Attestation
- **Outside Review Artifacts:**
  - `fleet-repo/.ufo/waves/kaika-w3/mori-review.md` (Integrator-dispatched verifier `W3ReviewMori` on commit `1f07f1dd1eed59f10c4859726e2f780199190b22`)
  - `fleet-repo/.ufo/waves/kaika-w3/mori-critic.md` (Integrator-dispatched critic on commit `1f07f1dd1eed59f10c4859726e2f780199190b22`)
  - `fleet-repo/.ufo/waves/kaika-aggregate/seats/audit-mori.md` (Aggregator seat `AuditMori` on commit `bf7cdc4783d0748d525fbfe3ba8fb3d285eb929a`)
  - `corpus/lessons/round-12-verifier-spotcheck.md` (Integrator/orchestrator commit `bf7cdc4`, author `protocol-shokunin`)
- **Self-Attestation Constraint:**
  - Under `QUALITY.md` criterion 10 and `LEARNING.md:42-43` (*"A subagent the lane dispatched is still the lane"*), internal reviews (by lane seats like `R12Review`, `R12Critic`, `MoriR13.Review*`) represent self-attestation.
  - The outside review verdict was **ADMIT WITH CORRECTIONS** (`W3ReviewMori`), requiring corrections C1–C6 before closure.

### 1.2 Status of Post-Review Round 12 Fixes
Lane commit `1f07f1d` was augmented by post-review fixes landing up to `a7f1ecb` / `bf7cdc4`:
- **Addressed in Round 12 Post-Review:**
  - **C1 (Dead pointer in free lunch lesson):** Corrected `:21` → `:186` in `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md` (appended erratum).
  - **C2 (`roster-truth-r12.md` source & expansion count):** Added opened own-work source `S034` in `corpus/SOURCES.md`, appended corrected `source:` to `corpus/knowledge/roster-truth-r12.md`, and corrected expansion count from 5 to 4.
  - **C3 (Calibration score):** Reconciled: verdict improved per campaign binding (26 mined mistakes, 20 lesson-cited criteria), but scalar score held at 5 because the non-author reviewer could not re-derive 6.
  - **C4 (Adjacency score):** Reconciled: verdict unchanged, score 6 held (unclaimed contract repair had no counting command or score move).
  - **C5 (`SHONEN.md` seed claim):** Acknowledged and disclosed seed indentation / formatting differences rather than claiming byte-identical output.
  - **C6 (Mutation battery on final census bytes):** Re-ran the 12 roster mutants against final census SHA-256 `3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164`: 12 killed, 0 survived, 0 inconclusive (appended to `corpus/evidence/roster-r12-20261019T220912Z-mutation.md`).

---

## 2. Identified Disagreements & Carried Defect Inventory

The non-author reviews, aggregate audit, and round 11/12 records document specific defects and disagreements that were not closed or were explicitly routed to future rounds.

### 2.1 Production Pipeline Long-History Defect: F01 / D01
- **Severity:** High / Carried Defect (Operability, Correctness)
- **Status:** **OPEN / OWED in Round 13**
- **Disagreement / Defect Description:**
  - Round 9 fixed a live-pipe `grep` race (SIGPIPE) in the *selftest harness* (`run_selftest()`), but the *production probe pipeline* for lane authorship attribution retained the identical hazard.
  - In `tools/mori-census.sh:1490-1497` (formerly lines 1366–1374 at base):
    ```bash
    inwin=$(printf '%s\n' "$CAP_OUT" | awk -v lo="$LA_EPOCH" -v hi="$NOW_EPOCH" \
      '$1 ~ /^[0-9]+$/ && $1+0 > lo+0 && $1+0 <= hi+0 { print }')
    if [ -n "$inwin" ]; then
      sibn=$(printf '%s\n' "$inwin" | awk 'END { print NR }')
      if printf '%s\n' "$inwin" | sed -E 's/^[0-9]+ //' | grep -Fxq -- "$lane-shokunin <$lane@shokunin.local>"; then
        subj=1
      else
        sib=1
      fi
    ```
  - When `inwin` has a large history (e.g. 12,000 commits), `grep -Fxq` exits 0 immediately on the first match and closes its read pipe. The upstream writer (`printf` or `sed`) receives `SIGPIPE` (141).
  - Because `tools/mori-census.sh` runs under `set -e` / `pipefail`, a 141 in the pipeline causes the entire `if` condition or command evaluation to fail (or invert under negation), causing valid lane authorship commits to be discarded or misgraded as `progressing-weak` (`basis=row-C other_authored_commits=12001`).
- **Governing Criteria:**
  - `QUALITY.md` Criterion 6: *"Every probe pipeline is rc-gated; a crash exit code never equals a verdict code..."*
  - `QUALITY.md` Criterion 7: *"No live producer pipe feeds a match test; capture once and assert over the captured bytes (SIGPIPE 141 ≠ 1)."*
  - `QUALITY.md` Criterion 25: *"A claim is admitted at the scope it was measured; narrowing is an explicit correction, not a silent edit."*
- **Exact Fix Required:**
  - Avoid streaming live pipelines into early-terminating readers (`grep -q`, `grep -m1`, `head -n1`).
  - Capture the author list once into a variable or file, or use `awk` to scan the stream to completion without early termination pipe-breaks, or match using bash pattern/here-string without a live pipe (`grep -Fxq ... <<< "$authors"`).
  - Add a dedicated regression case reproducing the synthetic 12,000-commit history (from `corpus/knowledge/audit-r11.md` Appendix B) asserting `EXPECTED=progressing`.

---

### 2.2 Oracle Final Verdict Validation Blind Spot: F02 / D02
- **Severity:** High / Carried Defect (Operability, Verdict Integrity)
- **Status:** **OPEN / OWED in Round 13**
- **Disagreement / Defect Description:**
  - `tools/mori-silence-cases.sh:570` extracts the verdict line:
    ```bash
    verdict=$(printf '%s\n' "$CASE_OUT" | grep -m1 '^MORI_CENSUS:' || true)
    ```
  - It checks only `[ -z "$verdict" ]` to catch total crashes (`tools/mori-silence-cases.sh:582-586`).
  - It does NOT validate that the verdict word matches the admitted vocabulary (`CLEAN` vs `DRIFT`) or is consistent with the return code `CASE_RC`.
  - As proven by `audit-r11.md` Appendix C, a census wrapper substituting `MORI_CENSUS: BANANA` passes all 28 oracle cases (`matched=28 total=28`, exit 0).
- **Governing Criteria:**
  - `QUALITY.md` Criterion 8: *"A 'cannot fake / cannot fail / cannot accept' claim enumerates the channels or inputs tested; untested classes are named residuals."*
  - `QUALITY.md` Criterion 21: *"Verdict cells use exactly the four admitted values... qualifications live in the evidence cell."*
- **Exact Fix Required:**
  - In `tools/mori-silence-cases.sh`: parse the token immediately following `^MORI_CENSUS:`.
  - Require the token to be strictly `CLEAN` (when `CASE_RC == 0` and findings == 0) or `DRIFT` (when `CASE_RC == 1` or findings > 0).
  - Explicitly reject invalid verdict tokens (`BANANA`, unexpected strings) and mismatched exit status (e.g. `CLEAN` with `CASE_RC != 0` or `DRIFT` with `CASE_RC == 0`), failing the case immediately.
  - Include positive and negative test cases verifying that a `BANANA` verdict is rejected.

---

### 2.3 Roster Authority vs. Config/State Union Disagreement (W3Review / W3Critic)
- **Severity:** Medium (Coverage, Adjacency)
- **Status:** Disagreement documented in R12 review/critic; partially addressed by S034 own-work scoping.
- **Disagreement / Defect Description:**
  - In Round 12, mori expanded its roster from 9 to 23 lanes by taking the union of `shokunin.conf` and `.ufo/state/*.round`.
  - `W3ReviewMori` (M1) noted that `roster-truth-r12.md` opened with an invalid path `source: FLEET/shokunin.conf...` and claimed an expansion count of 5 without an `S###` entry.
  - `W3Critic` pointed out that `PROTOCOL-APPENDIX.md:42` defines the authoritative fleet universe as `roster ∪ base LANES ∪ driver counters`. Mori's automatic parser reads only `conf + state`. A lane launched but absent from both config and state is invisible.
  - Furthermore, `tools/mori-census.sh:397-401` accepts `MORI_ROSTER_LANES` without shape validation or deduplication, potentially creating arbitrary paths via `lane_repo()`.
- **Governing Criteria:**
  - `QUALITY.md` Criterion 9: *"Every path, line or commit pointer resolves at the carrying commit..."*
  - `QUALITY.md` Criterion 25: *"A claim is admitted at the scope it was measured..."*
- **Exact Fix / Resolution:**
  - Round 12 post-review added `S034` (own-work) and narrowed the claim: mori explicitly documents that it measures the `conf + state` union, not an omniscient fleet universe.
  - In `tools/mori-census.sh`: validate `MORI_ROSTER_LANES` tokens against standard lane identifier syntax (`^[a-z0-9-]+$`) and deduplicate tokens before iteration.

---

### 2.4 Census Wall Time vs. Operability Budget Disagreement (W3Review / W3Critic)
- **Severity:** Low / Operator Adjudication Needed
- **Status:** Cost recorded; no declared budget breached.
- **Disagreement / Defect Description:**
  - Census runtime increased from ≈1.8 s (9 lanes) to ≈4.3 s (23 lanes), an increase of ≈2.3× (~0.17 s per lane).
  - `SCORECARD.md` labeled operability as "unchanged". `W3Critic` contested this label, arguing that without a pre-declared budget, one cannot claim operability is "unchanged" when wall clock time more than doubles.
  - `W3ReviewMori` noted that `AXES.md` defines no runtime budget, so this latency is an explicit trade rather than a correctness regression.
- **Governing Criteria:**
  - `QUALITY.md` Criterion 11: *"A deferred probe carries its four prices before admission: found-ness, marginal wall time, enforced bound (and code vocabulary), and the filter's drop set."*
- **Exact Fix / Resolution:**
  - Establish and document an explicit wall-time budget for census execution (e.g. `< 10.0 s` total, or `< 250 ms` per lane).
  - Explicitly record marginal wall time in census benchmarks.

---

### 2.5 Structured Journal Scopes vs. Text Regex Grepping (FR1 / C1)
- **Severity:** High / Primary Goal for Round 13 (Coverage C1)
- **Status:** **OWED in Round 13**
- **Disagreement / Defect Description:**
  - Past rounds relied on text grepping over journal streams (e.g., searching for "crashed", "segfault", "killed"), violating `QUALITY.md` criterion 15.
  - In Round 12, S013 and S014 primary sources were opened and admitted, revealing three distinct catalog IDs:
    - `fc2e22bc6ee647b6b90729ab34a250b1` — Coredump notice (systemd-coredump, line 66)
    - `fe6faa94e7774663a0da52717891d8ef` — Kernel OOM unit notice (systemd, line 604)
    - `d989611b15e44c9dbf31e3c81256e4ed` — Userspace systemd-oomd kill notice (oomd, line 884)
  - Critical distinction: `fe6faa94…` is a **unit notice**, NOT a kernel victim count. Host measurements show 5 kernel victim records vs 7 user notices vs 9 system notices on the same boot.
  - User and system journal scopes must **never be summed** (Criterion 16).
  - Journal queries must be MESSAGE-free (`--output-fields=_BOOT_ID` or `-o json --output-fields=MESSAGE_ID,_BOOT_ID`) to prevent leaking process arguments, environments, or raw messages.
  - Permission denials (`journalctl` returning `rc=1` when unprivileged) must be handled as `unavailable`, never as count `0`.
- **Governing Criteria:**
  - `QUALITY.md` Criterion 6: *"Every probe pipeline is rc-gated... unreadable-input canary per probe."*
  - `QUALITY.md` Criterion 14: *"A counter's semantics cite its increment site, not only documentation wording."*
  - `QUALITY.md` Criterion 15: *"A journal class is counted by MESSAGE_ID or another trusted structured field, never by message text."*
  - `QUALITY.md` Criterion 16: *"A kill count names its unit (kill vs notice) and its journal scope; scopes are never summed."*
  - `QUALITY.md` Criterion 17: *"A detection recipe states which delivery paths it cannot see."*
- **Exact Fix Required:**
  - Implement structured journal counting in `tools/mori-census.sh`:
    - Filter strictly by `MESSAGE_ID`.
    - Restrict output via `--output-fields=_BOOT_ID`.
    - Separate `--user` and `--system` scopes into distinct probe lines/keys.
    - Check exit code `rc=0`; map `rc=1` / permission denial to `unavailable (permissions)`.

---

### 2.6 Gate r4 / r8 / r10 Mechanical Findings in Aggregator Audit (`AuditMori`)
- **Severity:** Informational / Audit Boundary
- **Status:** Evaluated and explained in `audit-mori.md`.
- **Disagreement / Defect Description:**
  - `corpus-gate.mjs` run by `AuditMori` returned `exit 1` due to:
    - **r4 (39 findings):** Regex matching count claims lacking backticked commands. Spot-checks showed these were false positives on markdown headings (`## Known gaps — round-12 note`) and markdown table rows (`| id | URL | ... (≤25 words) |`).
    - **r8 (1 finding / 4 occurrences):** Credential regex detecting `token="nonce-${MORI_RUN_NONCE:-0}"` in logs and test notes. Classified as `could-not-evaluate` (literal shaped = 0/4, no vault secret).
    - **r10 (1 finding):** Missing `corpus/lessons/round-12-aggregator-*.md`. Mori is an investigated leaf lane, not the aggregator, and has zero aggregator files in its history.
- **Governing Criteria:**
  - `QUALITY.md` Criterion 1: *"Every claim falsifiable or marked opinion."*
  - `QUALITY.md` Criterion 19: *"A sweep's nonzero hits are inspected before the count is cited; regexes use word boundaries."*

---

## 3. Matrix of Disagreements, Criteria & Required Actions

| ID | Issue / Defect | Source / Seat | Governing Criterion | Status / Action for Round 13 |
|---|---|---|---|---|
| **F01** | Production authorship pipeline SIGPIPE 141 under pipefail | `audit-r11.md:156`, `round-12.md:25` (M2, M3) | **QUALITY 6, 7** | **CRITICAL FIX (C2)**: Remove live pipe from `inwin` pipeline in `tools/mori-census.sh:1490-1497`. Add 12k commit regression case. |
| **F02** | Oracle passes invalid verdict (`BANANA`) and ignores exit-code consistency | `audit-r11.md:157`, `round-12.md:27` (M4) | **QUALITY 8, 21** | **CRITICAL FIX (C2)**: Enforce exact verdict token grammar (`CLEAN` / `DRIFT`) and rc correlation in `tools/mori-silence-cases.sh:570-586`. Add BANANA test case. |
| **C1** | Text journal grepping instead of structured scopes | Goal C1, `round-12.md:36` (M13, M19) | **QUALITY 15, 16, 17** | **CRITICAL IMPL (C1)**: Use `MESSAGE_ID` with `--output-fields=_BOOT_ID`. Maintain independent `user` and `system` scopes (never sum). Gate on `rc=0` (map permission error to `unavailable`). |
| **Roster** | `MORI_ROSTER_LANES` unvalidated token stream | `mori-critic.md:29` | **QUALITY 9, 25** | Validate syntax (`^[a-z0-9-]+$`) and deduplicate tokens in `tools/mori-census.sh:397-401`. |
| **Budget** | Lack of declared wall-time budget for census | `mori-review.md:124`, `mori-critic.md:30` | **QUALITY 11** | Declare wall-time budget (e.g. `< 10 s`) in documentation / scorecard. |
| **S013 Quote** | S013 quote covered kernel OOM only, but `teaches` covers 3 IDs | `mori-critic.md:7-15` | **QUALITY 2, 9** | Ensure `corpus/SOURCES.md` S013 anchor/quote accurately reflects all three message catalog entries. |

---

## 4. Proposed Verification Checks for L1 Integration

The L1 integrator should verify the resolution of all carried defects using these exact checks:

```bash
# 1. F01: Verify long-history production authorship attribution does not fail with SIGPIPE
# Run Appendix B synthetic test (1 exact subject commit + 12,000 sibling commits)
python3 -c "
import tempfile, subprocess, os, pathlib
# Set up quiet fixture with 12,000 commits ...
# Verify that SURFACE lane.<lane>: progressing is produced (NOT progressing-weak)
"

# 2. F02: Verify Oracle rejects BANANA and invalid verdicts
cat << 'EOF' > /tmp/banana-wrapper.sh
#!/usr/bin/env bash
out=$(bash /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh "$@" 2>&1)
rc=$?
out=${out//MORI_CENSUS: CLEAN/MORI_CENSUS: BANANA}
out=${out//MORI_CENSUS: DRIFT/MORI_CENSUS: BANANA}
printf '%s\n' "$out"
exit "$rc"
EOF
chmod +x /tmp/banana-wrapper.sh
# Oracle MUST fail when run with BANANA wrapper
bash /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-silence-cases.sh /tmp/banana-wrapper.sh | grep -q 'FAIL'

# 3. C1: Verify MESSAGE-free structured journal extraction in census
# Verify output contains structured scope keys and NO raw MESSAGE lines
bash /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh | grep -E '^SURFACE journal\.(user|system)\.oom_notices:'

# 4. C1: Verify permission error handling
# When run under unprivileged user without journal access, must report unavailable, never 0
EOF
```

---

## 5. Tooling Record
- **Tools installed/updated:** None. Existing tools (`curl`, `git`, `python3`, `bash`, `jq`, `journalctl`) were utilized in strictly read-only inspection mode.
- **Verification Notice:** In strict accordance with the leaf scout assignment, **no integration tests, builds, lints, or smoke runs were executed**; all checks are proposed for L1 execution.
