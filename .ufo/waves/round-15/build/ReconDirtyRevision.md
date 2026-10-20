# ReconDirtyRevision: Research on R13/R14 Revision Dirty Provenance and Safest Status-Only Capture

Seat: `MoriR15.ReconDirtyRevision` (scout, leaf).  
Date: 2026-10-20.  
Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.  
Judged on: **coverage** (C1: retain validated positives without fabricated totals).  
Milestone: retain validated positives without fabricated totals.  
Report target: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-15/build/ReconDirtyRevision.md`.

---

## 1. Named Axes and Problem Definition

- **Coverage (Primary Axis):** C1 preserves critical OOM (`positive_kernel_oom`, `positive_unit_oom`) and user signal alarms (`positive_unit_signal`, `positive_process_sigkill`) from individually valid current-boot structured journal records even when an adjacent malformed, non-matching, or foreign-boot record invalidates the aggregate class. Raw aggregate and split counts remain honestly `unavailable`.
- **Operability (Protected Axis):** Gate execution, status capture, and receipt generation must remain deterministic, hermetic, lock-free, and hook-free. No gate run should fail due to index lock contention, git environment leakage, or hook execution.
- **Calibration / Provenance (Milestone Standard):** A gate receipt must distinguish harmless untracked output artifacts from uncommitted mutations to tracked production code. Collapsing repository cleanliness into a bare boolean (`dirty: true`) creates provenance debt that obscures moving inputs and undermines auditability.

---

## 2. Historical Analysis: R13 vs R14 Revision and Dirty Provenance

### 2.1 Round 13 (`tools/mori-round13-regressions.py`)

- **Implementation Anchors:**
  - `tools/mori-round13-regressions.py:1046–1094` (`Harness.record_revision`):
    ```python
    revision = os.environ.get("MORI_EVIDENCE_REVISION", "").strip()
    if not revision:
        revision = (git(["rev-parse", "HEAD"]) or "").strip()
    ...
    dirty_env = os.environ.get("MORI_EVIDENCE_DIRTY", "").strip().lower()
    if dirty_env in ("true", "false"):
        dirty = dirty_env == "true"
    else:
        status = git(["status", "--porcelain"])
        dirty = None if status is None else bool(status.strip())
    return revision, dirty
    ```
  - `tools/mori-round13-regressions.py:2519–2524`: emitted `"revision": {"head": self.revision, "dirty": self.dirty, "source": ...}` in `evidence.json`.
- **Observed Receipt Evidence:**
  - In `.ufo/waves/round-14/evidence/r13-preserved/evidence.json:4–8`:
    ```json
    "revision": {
      "head": "8d22d18fb4a4124becb35123ca839c93cbae0028",
      "dirty": true,
      "source": "MORI_EVIDENCE_REVISION"
    }
    ```
- **Defects and Provenance Debt:**
  1. *Boolean Collapse:* Reducing the entire `git status --porcelain` output to `bool(status.strip())` threw away the identity of what changed. Any untracked output file (e.g. `.ufo/waves/.../evidence.json`) caused `dirty: true`, indistinguishable from uncommitted edits in production scripts (`tools/mori-census.sh`).
  2. *Auditor Finding (`corpus/lessons/round-14-verifier-spotcheck.md:83, 136`):*
     > "The r13 preserved receipt says `revision.dirty=true`. This is provenance debt, **not established input drift**: closure/reviewer matched census, oracle, SHONEN, frozen manifest and frozen scripts to the cited committed bytes; synthetic git stubs prevent live repository state from driving fixture verdicts. The registry row was already committed and unchanged. Exact contemporary porcelain was not retained; untracked output receipts are a supported explanation, not a proved complete dirty-path list."
     The verifier explicitly routed:
     > "1. mori, next round — low provenance debt: retain the dirty-path scope (or measure from an explicitly frozen clean input tree with output outside it) when a gate records `dirty=true`."
  3. *Tooling Fragility:* The git helper in R13 ran with an isolated `PATH` and `HOME`, but omitted `GIT_OPTIONAL_LOCKS=0` and `-c core.fsmonitor=false`.

### 2.2 Round 14 (`tools/mori-round14-regressions.py`)

- **Implementation Anchors:**
  - `tools/mori-round14-regressions.py:162`:
    ```python
    PINNED_BASE_COMMIT = "dbe85009253c092fe50e4e93056fceeae273ec31"
    ```
  - `tools/mori-round14-regressions.py:2239–2244`: emitted static pins only:
    ```python
    "pinned": {
        "base_commit": PINNED_BASE_COMMIT,
        "sha256": PINNED_SHA256,
        "crosschecked_manifest": str(Path(self.args.frozen_dir).resolve() / "inputs.json"),
    }
    ```
- **Observed Receipt Evidence:**
  - In `.ufo/waves/round-14/evidence/green-after-accepted/evidence.json:21–28`, only static constants were serialized.
- **Defects and Provenance Debt:**
  - R14 swung to the opposite extreme: it completely omitted dynamic `git rev-parse HEAD` and `git status` probing.
  - The harness emitted no runtime dirty status, no porcelain paths, and no execution start/end integrity verification.
  - As flagged in Round 15's `dispatch.json` / `spec.json` (task `ProvenanceCapture`):
    "Address r14 outside dirty-scope debt: revision metadata retains exact git status porcelain (untracked files included safely as paths only), not just dirty bool; capture start/end scope to detect moving input where feasible without new contract."

---

## 3. Primary Named Sources and Safest Status-Only Capture

### 3.1 Primary Named Source 1: `git-status(1)`

- **Source:** Git Documentation / Man Page `git-status(1)` (Git 2.47+).
- **URL:** `https://git-scm.com/docs/git-status`
- **Section Anchor 1:** `--porcelain[=<version>]`
  - **Quote (22 words):**
    > "Give the output in an easy-to-parse format for scripts. This is similar to the short output, but will remain stable across Git versions"
- **Section Anchor 2:** `Porcelain Format Version 1`
  - **Quote (22 words):**
    > "Version 1 porcelain format is similar to the short format, but is guaranteed not to change in a backwards-incompatible way between Git versions"
- **Section Anchor 3:** `Short Format` (untracked files)
  - **Quote (24 words):**
    > "When a path is untracked, X and Y are always the same, since they are unknown to the index. ?? is used for untracked paths."

### 3.2 Primary Named Source 2: `git(1)` Environment Variables

- **Source:** Git Documentation / Man Page `git(1)`.
- **URL:** `https://git-scm.com/docs/git`
- **Section Anchor:** `ENVIRONMENT VARIABLES > GIT_OPTIONAL_LOCKS`
  - **Quote (22 words):**
    > "If set to 0, Git will avoid taking any optional locks which do not protect against data corruption, such as the index.lock"

### 3.3 In-Tree Production Reference Anchor: `tools/mori-census.sh:1931–1934`

- `tools/mori-census.sh` already establishes the safe git invocation pattern:
  ```bash
  cap env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" \
    -c core.fsmonitor=false -c core.quotePath=false -C "$repo" ls-files -mo --exclude-standard
  ```
  This proves the host's existing design discipline:
  1. Unset `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` to avoid inherited environmental overrides.
  2. Set `GIT_OPTIONAL_LOCKS=0` to eliminate `index.lock` contention.
  3. Set `-c core.fsmonitor=false` to prevent executing external fsmonitor scripts/hooks.
  4. Set `-c core.quotePath=false` to preserve clean UTF-8 paths without octal quoting.

---

## 4. Safest Status-Only Capture Specification for R15

To fully resolve the R13/R14 provenance debt while defending against subtle moving-worktree pitfalls (collaboratively analyzed with `MoriR15.AttackProvenance`), the gate harness (`tools/mori-round14-regressions.py` / `tools/mori-round15-regressions.py`) must adopt the following pattern:

### 4.1 Invocation Protocol
```python
def git_status_porcelain(repo: Path) -> tuple[Optional[str], list[str], Optional[str]]:
    """Safe, read-only status capture without locks, hooks, or config overrides."""
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": os.environ.get("HOME", "/tmp"),
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_SYSTEM": "/dev/null",
        "GIT_OPTIONAL_LOCKS": "0",
    }
    # Clean out any inherited git pointers
    for var in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(var, None)

    cmd_rev = ["git", "-C", str(repo), "rev-parse", "HEAD"]
    cmd_status = [
        "git",
        "-c", "core.fsmonitor=false",
        "-c", "core.quotePath=false",
        "-C", str(repo),
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ]
    ...
```

### 4.2 Content Hashing vs Status Line Invariance (CE1 Defense)
**Critical Vulnerability:** When an input file is already dirty (e.g. ` M tools/mori-round14-regressions.py`), mutating its content during test execution does *not* alter its porcelain line. Therefore, `scope_start["porcelain"] == scope_end["porcelain"]` cannot prove content was unmoving!
**Required Rule:**
1. Record SHA-256 digests of all declared inputs at read/load time (`harness.sha256_loaded`, census copy, frozen census, inputs manifest, importlib modules, fixture packs).
2. Re-hash at emit time.
3. Assert `moving: false` **only if** both (a) porcelain lines match outside output, AND (b) loaded SHA-256 matches emit SHA-256 for all declared inputs. If content was not compared, emit `moving: null` with `content_compared: false`.

### 4.3 Head Observation vs Env Pin (CE2 Defense)
Always query the live, real `git rev-parse HEAD`. If `MORI_EVIDENCE_REVISION` is supplied by an orchestrator, record it as `asserted_revision` and evaluate `asserted_matches_head: bool`. Never substitute the env pin for the real HEAD check, which would make head comparison vacuous.

### 4.4 Exact Output Path Exclusion vs Broad Prefix (CE3 & CE4 Defense)
- Do not exclude by a coarse directory prefix (e.g. `--output .ufo/waves/round-15`) because doing so can swallow input fixtures (`.ufo/waves/round-15/fixtures/*.json`) or frozen directories.
- Raise `SetupError` (exit code 2) if `--output` is an ancestor of any declared input file.
- Exclude only the specific paths written by the harness (`output/targets/`, `output/evidence.json`, fixture run roots).
- Emit `dirty_outside_output: bool` in addition to raw `dirty: bool`, allowing receipts to pass clean-status gates even when generating artifacts inside the repository tree.

### 4.5 Structured Evidence Schema
```json
"revision": {
  "base_head": "5601d1201926124f7884bc694568abac2ead6d5c",
  "asserted_revision": null,
  "asserted_matches_head": true,
  "dirty": true,
  "dirty_outside_output": false,
  "tracked_dirty": false,
  "scope_start": {
    "porcelain": ["?? .ufo/waves/round-15/build/ReconDirtyRevision.md"],
    "untracked_paths": [".ufo/waves/round-15/build/ReconDirtyRevision.md"]
  },
  "scope_end": {
    "porcelain": ["?? .ufo/waves/round-15/build/ReconDirtyRevision.md", "?? .ufo/waves/round-15/evidence/..."],
    "untracked_paths": [".ufo/waves/round-15/build/ReconDirtyRevision.md", ".ufo/waves/round-15/evidence/..."]
  },
  "input_digests": {
    "harness_loaded": "c39e5a73...",
    "harness_emitted": "c39e5a73...",
    "census_target": "0e41cb83..."
  },
  "moving_input_detected": false,
  "content_compared": true
}
```

---

## 5. Scope Boundaries

1. **Inside Scope:**
   - Capturing repository commit SHA (`git rev-parse HEAD`).
   - Capturing exact porcelain v1 output strings relative to the repository root.
   - Parsing status codes to partition tracked modifications from untracked additions.
   - Restricting untracked file capture strictly to safe relative path strings (no content reads, no hashing of untracked files).
   - Comparing `scope_start` and `scope_end` porcelain and verifying input SHA-256 digests across the run.
   - Hardening git child process execution with `GIT_OPTIONAL_LOCKS=0`, `-c core.fsmonitor=false`, and `-c core.quotePath=false`.
2. **Strictly Outside Scope:**
   - No index modifications or working tree mutations (`git add`, `commit`, `stash`, `clean`, `checkout`).
   - No inspection of untracked file contents or hash calculations over untracked trees.
   - No failure/rejection of runs solely due to the presence of benign untracked reports or fixture outputs.
   - No execution of host git commands inside test fixtures (fixtures must strictly use the synthetic stub `git_stub_body()`).
   - No modification to production `tools/mori-census.sh` from this scout seat.

---

## 6. Counterexamples for C1 (Positive Alarms vs Naive Dirty Provenance)

### 6.1 Context
Under Round 15 Claim C1, a journal stream containing a valid current-boot kernel OOM record (`MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`, `_BOOT_ID=11111111111111111111111111111111`) adjacent to a malformed or non-matching record must keep the raw aggregate count unavailable (`unavailable:shape`), but must preserve `positive_kernel_oom=1` and fire the OOM alarm.

### 6.2 Counterexample 1: The "Dirty Boolean" Masking Production Regression
1. **The Injected Regression:**
   An executor attempts to implement C1 in `tools/mori-census.sh`. Due to an off-by-one or faulty fallback, when processing a mixed stream with malformed records, the census script fabricates `count=0` instead of `unavailable:shape` for the raw aggregate counter, violating C1's core invariant: *“Existing raw aggregate/split counts STAY unavailable when invalid... Positive fields unavailable on capture/parser failure; unsafe/nonmatching records excluded, never interpreted as numeric-zero total.”*
2. **Concurrent Working Tree State:**
   During a 64-seat parallel wave, sibling seats write report drafts under `.ufo/waves/round-15/build/`, creating untracked files (`?? .ufo/waves/round-15/build/HistoryDirtyHistory.md`).
3. **Failure under R13 Naive Boolean Capture:**
   The test harness runs. It queries `git status --porcelain` and checks `bool(status.strip())`. Because untracked markdown reports exist, `dirty` evaluates to `True`.
   The harness records `"dirty": true` in `evidence.json`.
   When reviewing the receipt, the verifier cannot distinguish whether `dirty: true` was caused by the benign untracked markdown file or by the fact that `tools/mori-census.sh` had uncommitted, buggy changes. If the verifier assumes `dirty: true` is just "untracked report artifacts" (as happened in R14 spot-check §83), the uncommitted fabrication of `count=0` slips through into evidence without being attributed to modified code under test!
4. **Failure under R14 Static Pins:**
   The R14 harness does not run `git status` at all. It prints `pinned: base_commit: dbe8500...`, completely masking that the running tree is dirty and that the test ran against modified, uncommitted code.
5. **Prevention under Safest Status-Only Capture:**
   The R15 status capture records:
   ```json
   "tracked_dirty": true,
   "porcelain": [
     " M tools/mori-census.sh",
     "?? .ufo/waves/round-15/build/HistoryDirtyHistory.md"
   ]
   ```
   The presence of ` M tools/mori-census.sh` immediately and unambiguously alerts L1 that tracked production code is dirty. The regression cannot hide behind untracked artifacts, preserving C1 integrity and preventing false claims of clean-commit conformance.

### 6.3 Counterexample 2: In-Flight Content Edit of Already-Dirty File (AttackProvenance CE1)
Suppose `tools/mori-census.sh` or `tools/mori-round14-regressions.py` is already dirty before the test suite starts. An editing seat modifies the script during test execution (e.g. changing positive token parsing). Because the file was already dirty, its porcelain line (` M tools/mori-census.sh`) is identical at start and end. If the harness checks only `scope_start["porcelain"] == scope_end["porcelain"]`, it reports `moving_input_detected: false`. Only dual-point content hashing (hashing loaded bytes vs emit-time bytes) catches that the code under test shifted during the run.

### 6.4 Counterexample 3: Broad Output Prefix Swallowing Input Fixtures (AttackProvenance CE3)
If a harness filters out dirty paths by checking `if path.startswith(output_dir): drop()`, and the user specifies `--output .ufo/waves/round-15`, any modifications to `.ufo/waves/round-15/fixtures/pack1.json` occurring mid-run are dropped from the status check, falsely certifying `moving_input_detected: false`.

### 6.5 Counterexample 4: Concurrency Lock Collision False Red
If status capture omits `GIT_OPTIONAL_LOCKS=0`, running the harness while another subagent or git process touches the repository causes `git status` to attempt acquiring `.git/index.lock`. The subprocess fails with exit code 128, causing the regression gate to abort with `SetupError` (exit code 2). A completely correct C1 partial-positive implementation would then be falsely reported as a gate setup failure due to tooling lock contention.

---

## 7. Remaining Unknowns and Hand-off

- **Unknowns:** None for status capture mechanics. Git's `--porcelain=v1` and `GIT_OPTIONAL_LOCKS=0` contracts are stable and verified in git documentation and local man pages.
- **Hand-off to `ProvenanceCapture` (`tools/mori-round14-regressions.py`) & `HarnessBuild` (`tools/mori-round15-regressions.py`):**
  - Implement `git_status_porcelain()` using `GIT_OPTIONAL_LOCKS=0` and `-c core.fsmonitor=false -c core.quotePath=false`.
  - Capture `scope_start` during `Harness.prepare()` and `scope_end` during `Harness.emit()`.
  - Perform loaded vs emit-time digest comparisons on all declared inputs (`sha256_loaded` vs `sha256_emitted`).
  - Emit `dirty_outside_output`, `tracked_dirty`, and clean `untracked_paths` (relative paths only).
  - Verify `--output` does not ancestor/swallow declared inputs.
  - Record live `base_head` via `rev-parse HEAD` rather than relying on environment override pins.
