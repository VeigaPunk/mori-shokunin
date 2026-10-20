# ConnectReceipts: Linking Dirty Scope Metadata to Committed Freeze / Current-Byte Gate Standard Without Secret Contents

**Seat**: `MoriR15.ConnectReceipts` (Role: connector, leaf member)  
**Lane Root**: `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Milestone**: Retain validated positives without fabricated totals  
**Judged On**: `coverage` (lowest owned axis 6 vs operability 7)  
**Target Report**: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-15/build/ConnectReceipts.md`  
**Safety & Protocol**: Report-only leaf member; no subagent dispatch; no production file edits; no verification or test commands run; no package installs or system updates (parent host-safety directive acknowledged).

---

## 1. Executive Summary & Named Axes (Godspeed Step 1)

In Mori Round 15, the single claim **C1** targets **coverage**:
> *Preserve critical OOM and user signal alarms from individually valid current-boot structured records even when an adjacent malformed/nonmatching/foreign-boot record invalidates the aggregate class. Existing raw aggregate/split counts stay unavailable when invalid. Do not claim completeness, authenticated IDs, unique victims, or repair arbitrary malformed JSON.*

This connector review links **dirty scope metadata** to the **committed freeze / current-byte gate standard**, synthesizing proposals across `ReconDirtyRevision`, `ProvenanceCapture`, `AttackProvenance`, and `HarnessBuild`. It provides a concrete, non-obvious architecture that guarantees cryptographic provenance and detects moving inputs while strictly preventing secret content leakage (such as raw `MESSAGE` strings, secret canaries, or host credentials).

### 1.1 The Declared Axes
1. **Coverage (Primary Judged Axis, Improves 6 → 7)**:
   - Valid current-boot structured alarms (`positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`) survive adjacent invalid, non-matching, or foreign-boot records.
   - Eliminates the silent suppression defect where an invalid record in a stream masks an individually valid critical alarm.
2. **Operability (Guard Axis, Held at 7)**:
   - Single-query stream capture without extra `journalctl` invocations.
   - Raw aggregate/split totals stay strictly `unavailable:<reason>` when invalid; no fabricated zeros or partial totals.
3. **Calibration & Provenance (Guard Axis, Held at 6)**:
   - Gate receipts must reliably tie test verdicts to the exact bytes executed and the exact repository working-tree state.
   - Eliminates the historical "boolean collapse" (`dirty: true`) without swinging to static-only opacity or false "moving: false" attestations.
4. **No-Harm & Honesty (Guard Axis, Held at 7)**:
   - All existing raw tokens, field paths, severity levels, and error reasons remain bit-for-bit identical on clean, valid streams (Invariant **I0**: `positive ≡ raw-ok`).

---

## 2. Local Repository Evidence & Cross-Round Analysis (Godspeed Step 2)

### 2.1 The Historical Dialectic: R13 vs R14 Provenance Implementations

1. **Round 13 Boolean Collapse (`tools/mori-round13-regressions.py:1088–1094, 2519–2524`)**:
   ```python
   dirty_env = os.environ.get("MORI_EVIDENCE_DIRTY", "").strip().lower()
   if dirty_env in ("true", "false"):
       dirty = dirty_env == "true"
   else:
       status = git(["status", "--porcelain"])
       dirty = None if status is None else bool(status.strip())
   return revision, dirty
   ```
   - *Receipt Impact*: In `.ufo/waves/round-14/evidence/r13-preserved/evidence.json`, the receipt serialized `"revision": {"head": "8d22d18...", "dirty": true}`.
   - *Auditor Finding*: As documented in `corpus/lessons/round-14-verifier-spotcheck.md:83, 136`:
     > "The r13 preserved receipt says `revision.dirty=true`. This is provenance debt, **not established input drift**: closure/reviewer matched census, oracle, SHONEN, frozen manifest and frozen scripts to the cited committed bytes... Untracked output receipts are a supported explanation, not a proved complete dirty-path list."
     > **Routed Defect 1**: *"retain the dirty-path scope (or measure from an explicitly frozen clean input tree with output outside it) when a gate records `dirty=true`."*
   - *Flaw*: A bare boolean collapsed benign untracked output artifacts (`?? .ufo/waves/...`) into the same state as uncommitted mutations to production code (` M tools/mori-census.sh`).

2. **Round 14 Static Pinning Over-Correction (`tools/mori-round14-regressions.py:160–166, 2239–2244`)**:
   ```python
   PINNED_BASE_COMMIT = "dbe85009253c092fe50e4e93056fceeae273ec31"
   PINNED_SHA256 = {
       "mori-census.sh": "39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985",
       "mori-silence-cases.sh": "34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa",
   }
   ```
   - *Receipt Impact*: In `.ufo/waves/round-14/evidence/green-after-accepted/evidence.json`, only static constants were recorded.
   - *Flaw*: R14 omitted runtime git inspection entirely. The receipt contained no record of repository revision at execution time, no record of whether working tree files were modified, and no defense against moving target files during the test run.

3. **Round 15 Emergent Proposals and Adversarial Criticisms**:
   - `ProvenanceCapture` (`tools/mori-round14-regressions.py:372–483`): Introduces isolated `git_capture` with `GIT_OPTIONAL_LOCKS=0`, captures `scope_start` and `scope_end` using `git status --porcelain --untracked-files=all`, and filters `--output` directory entries.
   - `ReconDirtyRevision` (`.ufo/waves/round-15/build/ReconDirtyRevision.md`): Identifies the need to partition `tracked_dirty` (modifications to tracked code) from `untracked_paths` (path strings of new files).
   - `AttackProvenance` (`.ufo/waves/round-15/build/AttackProvenance.md`): Discovers critical vulnerabilities in naive porcelain comparisons:
     - **CE1**: Porcelain status for an already-dirty file (` M tools/mori-census.sh`) does **not** change when file content changes mid-run! Start/end porcelain equality fails to detect moving inputs without content hashing at load vs emit.
     - **CE2**: Using `MORI_EVIDENCE_REVISION` pins the `head` comparison vacuously; the real `rev-parse HEAD` must always be captured.
     - **CE3**: Prefix-based output exclusion (`_output_prefix`) can swallow verdict inputs if `--output` is an ancestor of fixture or frozen directories.
     - **CE4**: `dirty` is unconditionally true when `--output` is in-repo; must emit `dirty_outside_output`.
     - **CE5**: The receipt's `head` is the pre-landing base (`0fa5e0d`), not the landing commit; must label it `base_head` and record per-input `matches_base_head`.
     - **CE6**: R15 importlib reuse of R14 modules introduces an unhashed dependency; loaded module bytes and fixture pack bytes must be hashed at load time.
   - `HarnessBuild` (`tools/mori-round15-regressions.py`): Pinned red control SHA `0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9` at commit `0fa5e0d`.

### 2.2 Security and Secret Content Invariant

1. **The Contract Rule**:
   > *"No raw MESSAGE or secret canaries... Positive fields unavailable on capture/parser failure... No fleet/sibling/MANIFEST/SHONEN/verifier/aggregator edits."*
2. **Confidentiality Surface**:
   - `git status --porcelain=v1` emits **only status codes and relative file paths** (e.g. ` M tools/mori-census.sh`, `?? .ufo/waves/round-15/build/ConnectReceipts.md`).
   - It **never reads or emits file contents**, eliminating the hazard of leaking secret canaries (`MORI_JOURNAL_CANARY`, `R14_SEC_UNIT_CANARY`), journal messages, or credential material.
   - To prevent leaking sensitive environment variables or agent data, git execution must run under an isolated environment (`PATH`, `HOME=/tmp`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_TERMINAL_PROMPT=0`).

---

## 3. The Central Contradiction: Frozen vs Current-Byte Standards

Across the round proposals, a fundamental tension exists between two verification standards:

1. **The Frozen Control Standard (Red Control)**:
   - Requires comparing against an immutable, committed snapshot pinned by in-script digest (e.g. `0e41cb83...` at `0fa5e0d`).
   - The frozen control must fail the required red cases to prove that the test suite actually exercises the target defect.
   - By definition, the frozen control has no working-tree dirty status—it is a static byte constant.
2. **The Current-Byte SUT Standard (Green Run)**:
   - Evaluates the live, working-tree development target (`tools/mori-census.sh`).
   - In active multi-agent waves, the working tree is inherently dirty: `tools/mori-census.sh` is being edited (` M tools/mori-census.sh`), and sibling seats are generating untracked markdown reports and fixture packs (`?? .ufo/waves/...`).
3. **The Contradiction / Provenance Risk**:
   - If the gate stamps `head: 0fa5e0d` without recording the dirty status of `tools/mori-census.sh`, the receipt falsely implies that commit `0fa5e0d` passed the new positive tests (when in reality commit `0fa5e0d` is the defective frozen control!).
   - If the gate rejects any run where `dirty: true`, developers and integrators cannot verify current-byte edits prior to committing.
   - If the gate records untracked report files as `dirty: true` without distinguishing them from tracked script edits, verifiers cannot determine whether the test ran against modified production logic or a clean commit with benign output files.
   - If target files are modified *during* gate execution (moving inputs in parallel waves), porcelain equality alone falsely reports `moving: false` (CE1), producing an invalid and unrepeatable receipt.

---

## 4. The Non-Obvious Move: Target-Bound Dual-Snapshot Content-Hashed Receipt Protocol (Godspeed Steps 3 & 4)

To resolve the contradiction, close the vulnerabilities exposed by `AttackProvenance`, improve calibration and coverage, and harm no existing axis, we synthesize the round's proposals into:

### **The Move**:
**Cryptographically bind the current-byte SUT execution copy SHA-256 directly to a dual-snapshot porcelain scope (start/end) AND per-input load/emit content hashes in the receipt, while partitioning porcelain into `covered_target_dirty`, `uncovered_tracked_dirty`, and `untracked_path_scope`, with a mandatory zero-byte content gate (status codes and path strings only).**

```
+---------------------------------------------------------------------------------------------------+
|                        TARGET-BOUND CONTENT-HASHED RECEIPT PROTOCOL                               |
|                                                                                                   |
|  1. Frozen Control (Red):                                                                         |
|     - Pinned In-Script SHA-256: 0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9 |
|     - Base Commit: 0fa5e0d                                                                        |
|     - Verified: In-script constant match -> Reproduced required defects                           |
|                                                                                                   |
|  2. Current-Byte SUT (Green) & Input Content Verification:                                        |
|     - SUT Executed Digest: SHA-256(tools/mori-census.sh at load time)                             |
|     - Harness Loaded Digest: SHA-256(__file__ at load time)                                       |
|     - R14 Module Loaded Digest: SHA-256(tools/mori-round14-regressions.py at load time)           |
|     - Fixture Pack Loaded Digests: SHA-256(each fixture pack as read into memory)                 |
|     - Emit-Time Re-Hash: Compare disk SHA-256 at emit against loaded SHA-256 (CE1, CE6)           |
|                                                                                                   |
|  3. Dual-Snapshot Revision Scope (Start & End):                                                   |
|     - Always run real `git rev-parse HEAD` (CE2); record env pin as asserted_revision            |
|     - Status: `git status --porcelain=v1 --untracked-files=all` (GIT_OPTIONAL_LOCKS=0)            |
|     - Output Isolation: Enforce SetupError if --output is ancestor of inputs (CE3)                |
|     - Partition:                                                                                  |
|         a. covered_targets: ["M tools/mori-census.sh"] -> Tested source mutation status           |
|         b. uncovered_tracked: ["M LOG.md", "M SCORECARD.md"] -> Repository metadata changes       |
|         c. untracked_paths: ["?? .ufo/.../ConnectReceipts.md"] -> Harmless build artifacts       |
|         d. dirty_outside_output: Computed after output prefix exclusion (CE4)                     |
|                                                                                                   |
|  4. Invariant Enforcement:                                                                        |
|     - Moving Target Invariant: Record moving: true/false/null in evidence fields.                 |
|       * In tools/mori-round14-regressions.py: Provenance is evidence-only; never change exit codes. |
|       * In tools/mori-round15-regressions.py: Evidence-only tracking, with rc2 as HarnessBuild opt |
|     - Setup Error (Exit 2): Enforce strictly on CE3 (--output overlapping inputs).                |
|     - Zero Content Gate: Path strings only; zero file contents/canaries emitted                  |
+---------------------------------------------------------------------------------------------------+
```

### 4.1 Concrete Specification for `evidence.json`

The emitted receipt `evidence.json` must record:
```json
{
  "schema": "mori-round15-evidence-v1",
  "generated_utc": "2026-10-20T...",
  "mode": "strict-with-frozen-control",
  "pinned_frozen_control": {
    "base_commit": "0fa5e0d",
    "sha256": {
      "mori-census.sh": "0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9"
    },
    "status": "pass"
  },
  "inputs": {
    "sut": {
      "path": "tools/mori-census.sh",
      "sha256_loaded": "<loaded-sha>",
      "sha256_emitted": "<emit-sha>",
      "content_unmoved": true,
      "matches_base_head": false,
      "covered_status": "M tools/mori-census.sh"
    },
    "harness": {
      "path": "tools/mori-round15-regressions.py",
      "sha256_loaded": "<harness-loaded-sha>",
      "sha256_emitted": "<harness-emit-sha>",
      "content_unmoved": true
    },
    "r14_helper_module": {
      "path": "tools/mori-round14-regressions.py",
      "sha256_loaded": "<r14-loaded-sha>",
      "sha256_emitted": "<r14-emit-sha>",
      "content_unmoved": true
    },
    "fixture_packs": {
      "KernelUser": {"path": ".ufo/waves/round-15/fixtures/KernelUser.json", "sha256": "..."},
      "UnitUser": {"path": ".ufo/waves/round-15/fixtures/UnitUser.json", "sha256": "..."}
    }
  },
  "revision_provenance": {
    "base_head": "0fa5e0d",
    "head_state": "ok",
    "asserted_revision": null,
    "asserted_matches_head": true,
    "scope_summary": {
      "is_clean": false,
      "dirty_outside_output": true,
      "covered_target_dirty": true,
      "uncovered_tracked_dirty": true,
      "untracked_count": 12,
      "moving_input_detected": false
    },
    "scope_start": {
      "covered_targets": ["M tools/mori-census.sh"],
      "uncovered_tracked": ["M LOG.md", "M SCORECARD.md", "M corpus/SOURCES.md"],
      "untracked_paths": [
        ".ufo/waves/round-15/build/ConnectReceipts.md",
        ".ufo/waves/round-15/build/ReconDirtyRevision.md"
      ]
    },
    "scope_end": {
      "covered_targets": ["M tools/mori-census.sh"],
      "uncovered_tracked": ["M LOG.md", "M SCORECARD.md", "M corpus/SOURCES.md"],
      "untracked_paths": [
        ".ufo/waves/round-15/build/ConnectReceipts.md",
        ".ufo/waves/round-15/build/ReconDirtyRevision.md",
        ".ufo/waves/round-15/evidence/..."
      ]
    }
  }
}
```

### 4.2 Why This Move Is Non-Obvious & Synergistic

1. **Closes CE1 (Content Movement Behind Unchanged Porcelain)**:
   By pairing porcelain comparison with explicit `sha256_loaded` vs `sha256_emitted` checks across all input files (SUT, harness, imported R14 helper module, fixture packs), the gate guarantees that no mid-run file mutations can produce a false `moving: false` attestation.
2. **Closes CE2 & CE5 (Head Transparency & Honest Base Labeling)**:
   By always executing real `git rev-parse HEAD`, the receipt records the actual base commit (`base_head: 0fa5e0d`), and by pairing it with `matches_base_head: false` for `tools/mori-census.sh`, it transparently demonstrates that the green run evaluated uncommitted current-byte repairs, not the defective base commit bytes.
3. **Closes CE3 & CE4 (Output Path Safety & Informative Dirty Scope)**:
   By refusing overlapping output trees (SetupError if `--output` is an ancestor of inputs) and computing `dirty_outside_output`, the receipt provides the exact path scope demanded by the R14 verifier without generating false-dirty signals from harmless test output.
4. **Guarantees Zero Secret Leakage by Design**:
   Because the capture operates solely on `git status --porcelain=v1` and file digests, it records only relative path strings, status codes, and SHA-256 hex strings. It never inspects or serializes file contents, environment strings, or journal outputs, perfectly maintaining the privacy and secret-canary invariants.
5. **Protects Concurrency with `GIT_OPTIONAL_LOCKS=0`**:
   Enforcing `GIT_OPTIONAL_LOCKS=0` prevents `git status` from taking `.git/index.lock`, ensuring that parallel subagents and concurrent processes never collide with lock contention.

---

## 5. Trace of Second-Order Effects Across Surfaces

### 5.1 Runtime Surface (`tools/mori-census.sh`)
- Zero effect on live census operation. `mori-census.sh` does not run git status during normal journal querying; its existing git inspection (`:1931–1934`) already uses `GIT_OPTIONAL_LOCKS=0` and `-c core.fsmonitor=false`.
- The production script remains completely decoupled from gate provenance mechanics.

### 5.2 Contract Surface (Claim C1 & Gate Schema)
- Preserves all raw aggregate unavailable tokens (`unavailable:record-invalid`, `unavailable:boot-mismatch`, `unavailable:multi-boot`).
- Accommodates the newly added positive evidence tokens (`positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`).
- Satisfies the R14 spot-check routed defect 1 without inventing new ad-hoc metadata schemas.

### 5.3 Substrate Surface (Git & Filesystem)
- Completely immune to index locks, fsmonitor daemons, and credential prompts via `GIT_ENV` isolation:
  ```python
  GIT_ENV = {
      "PATH": "/usr/bin:/bin",
      "HOME": os.environ.get("HOME", "/tmp"),
      "GIT_CONFIG_GLOBAL": "/dev/null",
      "GIT_CONFIG_SYSTEM": "/dev/null",
      "GIT_TERMINAL_PROMPT": "0",
      "GIT_OPTIONAL_LOCKS": "0",
  }
  ```
- Filtering `--output` paths ensures the harness never trips over its own emitted artifacts.

### 5.4 Verification Surface (L1 & Outside Spot-Check)
- Enables deterministic, automated verification:
  1. Verify frozen control: `sha256sum .ufo/waves/round-14/frozen/mori-census.sh` == pinned constant.
  2. Verify current SUT: `sha256sum tools/mori-census.sh` == receipt `sha256_loaded`.
  3. Verify revision: `git rev-parse HEAD` == receipt `base_head`.
  4. Verify cleanliness: if `covered_target_dirty` is false, the run represents clean-commit verification; if true, it represents uncommitted current-byte verification with exact byte tracking.

---

## 6. Risks and Mitigations

| Risk | Likelihood | Impact | Concrete Mitigation |
|---|---|---|---|
| **R1: Content change in already-dirty file (CE1)** | High | High | Re-hash all loaded inputs at emit time; flag `moving_input_detected: true` if loaded != emit digest. |
| **R2: Output tree swallows inputs (CE3)** | Low | High | Raise `SetupError` (exit 2) if `--output` is an ancestor of or equal to any declared input path. |
| **R3: Index lock contention in swarms** | Medium | High | `GIT_OPTIONAL_LOCKS=0` is strictly enforced on all git invocations. |
| **R4: Nonce/canary leakage in paths** | Low | High | Enforce path-only capture; reject any status line containing forbidden path fragments (e.g. `agent.db`, credentials). Untracked file contents are never read. |
| **R5: Execution outside a git repository** | Low | Medium | When `.git` is absent (e.g. exported tarball), fallback to `MORI_EVIDENCE_REVISION` environment variable; record `porcelain_state: unavailable:no-git-repo` honestly without failing. |

---

## 7. Concrete Supported Recommendations for L1 Integration

1. **Adopt Dual-Snapshot Content Hashing in Both Regression Gates**:
   Ensure `tools/mori-round14-regressions.py` (via `ProvenanceCapture`) and `tools/mori-round15-regressions.py` (via `HarnessBuild`) adopt the dual-snapshot schema partition:
   - Capture real `rev-parse HEAD` as `base_head` (CE2, CE5).
   - Track `covered_target_dirty` (`tools/mori-census.sh`) vs `uncovered_tracked_dirty` vs `untracked_paths`.
   - Calculate `dirty_outside_output` after prefix filtering (CE4).
   - Hash SUT, harness, imported R14 module, and fixture packs at load time, re-hash at emit time, and assert equality (CE1, CE6).
2. **Enforce SetupError on Output/Input Collisions (Exit 2, CE3)**:
   If `--output` is an ancestor of or equal to any declared input path, abort immediately with exit code 2 (SetupError).
3. **Evidence-Only Tracking for Moving Content (CE1, CE6)**:
   - In `tools/mori-round14-regressions.py`, keep moving-content detection strictly as evidence fields (`moving: true|false|null`); `moving: false` is emitted ONLY when both porcelain lines and load/emit content hashes match for all declared inputs, and `moving: null` if content was not compared (never emit `false` on porcelain equality alone). Do NOT alter gate exit codes (preserving ProvenanceCapture's contract of zero behavioral change).
   - In `tools/mori-round15-regressions.py`, record the same load/emit hash comparisons in evidence; whether a moving input triggers rc2 (could-not-evaluate) is an optional policy choice for `HarnessBuild`, not an R14 provenance requirement.
4. **Maintain Invariant I0 in Gate Assertions**:
   Ensure gate assertions verify that whenever a stream is clean and valid, positive tokens equal the raw/split counts bit-for-bit (`positive ≡ raw-ok`), and when invalid, positive tokens fire alerts while raw tokens remain `unavailable:<reason>`.

---

## 8. Residual Unknowns (Report-Only Honest Limits)

1. **Uncommitted Status at Final Integration**:
   At the time of this audit, `tools/mori-census.sh`, `tools/mori-round14-regressions.py`, `corpus/SOURCES.md`, `LOG.md`, and `SCORECARD.md` are uncommitted in the working tree (`git status -s`). Whether L1 creates a clean commit before or after generating the accepted round-15 receipt is an integration sequencing decision. The proposed move supports either path with complete, honest provenance.
2. **Live Execution Behavior**:
   Per leaf contract, no test commands, builds, or harnesses were executed by this seat. All findings, schema designs, and risk analyses are derived via static analysis of repository files and peer reports.
3. **Tool Installations**:
   Zero tools installed, updated, or removed. Host-safety directive observed.
