# Drift Scope and Persisted Baseline Analysis — Round 13

**Seat:** MoriR13.DriftScope (scout)  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Target Report:** `.ufo/waves/round-13/build/DriftScope.md`  
**Milestone:** round13 structured scopes and verdict integrity  
**Axes Judged:** coverage, operability  

---

## 1. Executive Summary & Purpose

The objective of this seat is to:
1. Examine the drift normalization mechanism in `tools/mori-census.sh` (`drift_normalize`, `DRIFT_VOLATILE_LIST`, `DRIFT_COUNTER_KEYS`).
2. Read the adopted and persisted round 10 baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` alongside round 10/12 drift analysis (`corpus/knowledge/drift-pin-r10.md`, `corpus/evidence/drift-r12-20261019T2204Z-classification.md`).
3. Map the **intentional schema and semantic drift** introduced by Claim C1 (replacing uncalibrated, MESSAGE-grepped journal classes with structured `MESSAGE_ID` catalog counts in independently labeled user and system scopes).
4. Evaluate mask dynamics and recommend explicit masks **for counters only** without widening masks over structural tokens, status words, or commands.
5. Respect the round 13 contract constraints: **no repin this round**, **no check/test executions mid-flight**.

---

## 2. Analysis of the Drift Normalization Mechanism

### 2.1 Code Anchors in `tools/mori-census.sh`
- **Volatile Contract Header & Usage:** `tools/mori-census.sh:150-188, 330-348`.
- **Counter Key List:** `tools/mori-census.sh:1763-1772`:
  ```bash
  DRIFT_COUNTER_KEYS=(
    age_unreadable aged_unsettled avail count current disp drift empty findings
    foreign freshness_unavailable has_head high host_mem_avail_pct idle idle_s
    kill_signal ledger_round local_oom_kill max mem_fill_pct mem_peak not_open
    oom oom_kill other_authored_commits pids probed progressing progressing_weak
    reg relevant round rowb_files run segfault sessions settle settled silent
    size skipped state_ahead state_cmp state_lag state_round state_rounds
    state_rounds_max state_val_unreadable surfaces total unclassified
    unit_failure unavailable unsettled used used_pct young
  )
  ```
- **Special Volatile List:** `tools/mori-census.sh:1774-1775`:
  ```bash
  DRIFT_VOLATILE_SPECIAL='ts age_s mtime_age_s *_epoch mem_peak_anchor psi_some_avg10 psi_full_avg10 io_avg_since_boot state_val_unread_reasons script_sha256 example'
  DRIFT_VOLATILE_LIST="$DRIFT_VOLATILE_SPECIAL ${DRIFT_COUNTER_KEYS[*]}"
  ```
- **Normalization Engine:** `tools/mori-census.sh:1779-1794`:
  - `drift_normalize()` runs a single `sed -E` pass fed by a here-string over the captured census output (`CENSUS_CAPTURE`).
  - Integer live counters are transformed via `\b(${cre})=[0-9]+` to `\1=<V>`, where `cre` is pipe-joined `${DRIFT_COUNTER_KEYS[*]}`.
  - Non-counter rules specifically target ISO timestamps (`ts=[^ ;)]*`), elapsed seconds (`age_s=[0-9]+`), epoch stamps (`*_epoch=[0-9]+`), PSI gauges (`psi_(some|full)_avg10=[0-9.]+`), and compound unread reasons (`state_val_unread_reasons=file:[0-9]+ ...`).
- **Drift Comparator:** `tools/mori-census.sh:1942-2020` (`run_drift`):
  - Validates baseline file existence, readability, `# --- canonical output follows ---` marker presence, and `# volatile_fields=` header match.
  - Crucial Contract Rule (`:1983`): If the baseline's recorded `# volatile_fields=` does not strictly equal current `$DRIFT_VOLATILE_LIST`, `run_drift` emits `MORI_DRIFT: volatile_fields` and flags drift (exit 1).
  - Line-level diffing (`drift_report`, `:1875-1920`): First attempts multiset line matches, then same-id pairing (`SURFACE:<name>`, `FINDING:<id>`, `VERDICT`, `HEADER`) reporting changed field keys (`-key`, `+key`, or `key`), and finally catches newly added lines (`+<id>`).

---

## 3. Persisted R10 Baseline State (`corpus/evidence/baseline-r10-20261015T2231Z.json`)

The persisted baseline reflects the settled state from round 10 (`d7710981...`):
- Pinned at `2026-10-15T22:26:29Z` with `VERSION=census-r5`.
- Header:
  ```text
  # mori-drift-baseline v1 — written by mori-census.sh --pin
  # census_sha256=d7710981aa1c7571ff9d6fd7f75822811173010e5f4e298ac3c47fab274a0b20
  # pinned_ts=2026-10-15T22:26:29Z
  # volatile_fields=ts age_s mtime_age_s *_epoch mem_peak_anchor psi_some_avg10 psi_full_avg10 io_avg_since_boot state_val_unread_reasons script_sha256 example age_unreadable aged_unsettled avail count current disp drift empty findings foreign freshness_unavailable has_head high host_mem_avail_pct idle idle_s kill_signal ledger_round local_oom_kill max mem_fill_pct mem_peak not_open oom oom_kill other_authored_commits pids probed progressing progressing_weak reg relevant round rowb_files run segfault sessions settle settled silent size skipped state_ahead state_cmp state_lag state_round state_rounds state_rounds_max state_val_unreadable surfaces total unclassified unit_failure unavailable unsettled used used_pct young
  # volatile_note=values of these fields are masked to <V>; --drift re-normalizes with the CURRENT list and reports every changed non-volatile line/field. Changing the list is itself drift; census_sha256 is informational (behavior, not revision, is compared).
  # --- canonical output follows ---
  ```
- Surface lines and findings pertinent to journal observability in the baseline:
  - Line 10:
    ```text
    SURFACE journal: drift (cmd=journalctl --user -b --no-pager; oom_kill=<V> kill_signal=<V> segfault=<V> unit_failure=<V> rc=0; ts=<V>)
    ```
  - Line 37:
    ```text
    FINDING KILL_SIGNAL_JOURNAL severity=warn obs=class=kill_signal count=<V> boot=current scope=user ts=<V> script_sha256=<V>
    ```
  - Line 38:
    ```text
    FINDING SEGFAULT_JOURNAL severity=info obs=class=segfault count=<V> boot=current scope=user ts=<V> script_sha256=<V>
    ```

---

## 4. Mapping C1 Intentional Schema and Semantic Drift

Claim C1 transitions journal inspection from unprincipled text-pattern searches over user journal messages into structured `MESSAGE_ID` catalog counts for both user and system scopes.

### 4.1 Surface Row Transformation
- **Old Entering Surface:**
  - Singleton surface: `SURFACE journal: <status> (cmd=...; oom_kill=<V> kill_signal=<V> segfault=<V> unit_failure=<V> rc=0; ts=<V>)`
- **New Structured Scopes (C1):**
  - Option A (Split surfaces):
    - `SURFACE journal.user: <status> (cmd=journalctl --user -b -o json --output-fields=_BOOT_ID,MESSAGE_ID; kernel_oom_notices=<V> oomd_notices=<V> coredump_records=<V> rc=<rc>; ts=<V>)`
    - `SURFACE journal.system: <status> (cmd=journalctl --system -b -o json --output-fields=_BOOT_ID,MESSAGE_ID; kernel_oom_notices=<V> oomd_notices=<V> coredump_records=<V> rc=<rc>; ts=<V>)`
  - Option B (Scoped fields within single surface):
    - `SURFACE journal: <status> (cmd=...; user_oom_notices=<V> user_oomd_notices=<V> user_coredumps=<V> system_oom_notices=<V> system_oomd_notices=<V> system_coredumps=<V> rc=<rc>; ts=<V>)`
  - Option C (Scoped field names on separate rows or structured surface rows):
    - If `SURFACE journal` is kept with user scope and a new `SURFACE journal_system` or similar is added, or `SURFACE journal` emits scoped key-values.

Regardless of whether surface rows are partitioned by scope (e.g. `SURFACE journal.user` / `SURFACE journal.system`) or kept under `SURFACE journal`, the key tokens inside the surface detail change:
- Removed keys: `-kill_signal`, `-segfault`, `-unit_failure`.
- Added keys: structured class counters naming catalog notice records (e.g. `kernel_oom_notices`, `oomd_notices`, `coredump_records`, or scope-prefixed forms).

### 4.2 Finding ID Transformations
- **Removed / Deprecated Findings:**
  - `KILL_SIGNAL_JOURNAL`: Previously fired on text matches like `status=9/KILL|SIGKILL`. Deprecated because text is untrusted, uncalibrated, and not attributable.
  - `UNIT_FAILURE_JOURNAL` & `UNIT_FAILURE_OUT_OF_SCOPE`: Text-based greps for `Failed with result`.
- **Preserved / Refactored User Findings:**
  - `OOM_KILL_JOURNAL`: Re-anchored to user-scope `fe6faa94e7774663a0da52717891d8ef` (`class=kernel_oom_notice`, unit=notice, NOT killed process count).
  - `SEGFAULT_JOURNAL`: Re-anchored to structured coredump catalog ID `fc2e22bc6ee647b6b90729ab34a250b1` (or retained `COREDUMP_SIGNAL=11`).
- **Added System Scope Findings:**
  - New findings scoped to system journal (e.g. `SYSTEM_OOM_NOTICE`, `SYSTEM_OOMD_NOTICE`, `SYSTEM_COREDUMP`), all designated `severity=info` (non-drifting, notice-only).

### 4.3 Semantic Drift (Crucial Knowledge & Quality Nuance)
1. **Notice Units vs. Killed Process Count:**
   - Under S013 / S015, `fe6faa94e7774663a0da52717891d8ef` logs "A process of @UNIT@ unit has been killed by the OOM killer". As documented in `corpus/knowledge/kill-classes-by-message-id-r12.md`, one kernel OOM kill can generate multiple unit notices across user and system scopes (e.g. 5 kernel kills vs. 7 user + 9 system notices).
   - Thus, C1 counts **unit notice records**, never fleet-caused kill totals.
2. **Untrusted `MESSAGE_ID` vs. Trusted Fields:**
   - As noted by safety reviews, `MESSAGE_ID` in user journal space is an unprivileged field that can theoretically be injected by userspace processes, whereas transport/boot fields (`_BOOT_ID`, `_TRANSPORT`) are kernel/systemd-trusted. The count represents catalog entries, not kernel verdicts.
3. **Producer RC Handling:**
   - Absent `journalctl` binary => `unavailable`.
   - Producer `rc > 1` (permission denied / query failure) => `unavailable` (never masked as clean or 0).
   - Valid query with empty result => `0` records.

---

## 5. Token Classification for Drift Comparator

When `--drift` is executed against `baseline-r10-20261015T2231Z.json` using the post-C1 census:
The drift engine will report differences across three categories:

| Drift Token | Category | Intentionality & Explanation |
|---|---|---|
| `-kill_signal` | Field deletion | **Intentional C1 schema drift.** Text grep for SIGKILL removed. |
| `-unit_failure` | Field deletion | **Intentional C1 schema drift.** Text grep for unit failure removed. |
| `-FINDING:KILL_SIGNAL_JOURNAL` | Finding deletion | **Intentional C1 schema drift.** Uncalibrated text warning retired. |
| `+kernel_oom_notices` (or added keys) | Field addition | **Intentional C1 schema drift.** New structured counter keys present in surface output. |
| `+FINDING:SYSTEM_OOM_NOTICE` (if any fire) | Finding addition | **Intentional C1 schema drift.** System-scoped notices added. |
| `SURFACE:journal` (or `+SURFACE:journal.system`) | Surface modification | **Intentional C1 schema drift.** Command string and field layout updated. |
| `volatile_fields` | Header mismatch | **Mandatory Drift Gate Trigger if `$DRIFT_VOLATILE_LIST` is modified.** If new counter keys are added to `DRIFT_COUNTER_KEYS`, `base_vol != DRIFT_VOLATILE_LIST` triggers `MORI_DRIFT: volatile_fields`. |

---

## 6. Recommended Mask Policy: Counters Only

The drift comparator is intentionally designed so that **behavioral and schema drift is detected, not hidden**.

### 6.1 Recommendations for `DRIFT_COUNTER_KEYS`
To ensure that newly emitted numeric counts for structured journal scopes do not cause false drift on hosts where counts churn across runs, all new counter keys **MUST be added to `DRIFT_COUNTER_KEYS`**:
- Recommended candidate keys to include in `DRIFT_COUNTER_KEYS`:
  - `kernel_oom_notices`
  - `oomd_notices`
  - `coredump_records`
  - `user_oom_notices`
  - `user_oomd_notices`
  - `user_coredumps`
  - `system_oom_notices`
  - `system_oomd_notices`
  - `system_coredumps`
  - (Any scope-specific aliases actually chosen by `CensusFix`, e.g. `notice_count`, `record_count`)

### 6.2 Strict Restrictions: What NOT to Mask
- **DO NOT mask field names / keys:** Every field name must remain unmasked. The drift engine must report `+kernel_oom_notices` or `-kill_signal` when fields are added or removed.
- **DO NOT mask surface names or finding IDs:** The appearance or disappearance of findings must be visible (`-FINDING:KILL_SIGNAL_JOURNAL`).
- **DO NOT mask commands or state tokens:** `cmd=`, `rc=`, `scope=`, `unit=`, `boot=`, `severity=`, `status` words must never be masked.
- **DO NOT mask values with broad regexes (e.g. blanking all numbers `[0-9]+`):** As demonstrated in `drift-pin-r10.md:184-189`, generic digit-blanking destroys field name contracts (e.g. `script_sha256` -> `script_sha<N>`) and masks critical threshold constants (like `warn_pct=85`).
- **Counters Only:** Only exact key-name matches of integer quantities (`\b(${cre})=[0-9]+`) may be masked to `<V>`.

---

## 7. Policy on Re-Pinning & Verification

1. **NO Re-Pinning in Round 13:**
   - Per the explicit assignment contract: **"Recommend masks for counters only; no repin this round, no checks."**
   - The persisted baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` remains intact.
   - Modifying `DRIFT_COUNTER_KEYS` in `tools/mori-census.sh` will cause `--drift corpus/evidence/baseline-r10-20261015T2231Z.json` to report `MORI_DRIFT: volatile_fields` in addition to the changed journal surface and finding tokens.
   - Per `drift-pin-r10.md §5.2` and QUALITY criterion 10, **this red drift report is the correct, honest before-state behavior**. A red drift that accurately names the schema modification and the volatile list expansion proves that the drift mechanism works. Re-pinning is only performed at admission by L1 once all changes land and the wave is integrated.
2. **NO Mid-Flight Verification Runs:**
   - In adherence to wave protocol, no builds, tests, selftests, or oracle runs were executed by this seat.
   - Verification will be conducted once by L1 after integration.

---

## 8. Summary of Proposed Verification Checks for L1

When L1 performs post-flight verification, the following checks should validate drift behavior:
1. **Volatile Contract Integrity:** Verify that `DRIFT_COUNTER_KEYS` contains all new structured counter keys and retains alphabetical/prefix sorting.
2. **Deterministic Drift Reporting:**
   ```bash
   bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json
   ```
   *Expected Outcome:* Exit code 1 with tokens naming `volatile_fields`, changed journal keys, and `-FINDING:KILL_SIGNAL_JOURNAL`. It must *not* fail with exit 2 (syntax/malformed) or exit 0 (swallowed/unreported changes).
3. **Selftest Pin/Drift Arms:**
   ```bash
   bash tools/mori-census.sh --selftest
   ```
   Ensure hermetic selftest pin/drift roundtrip cases (`tools/mori-census.sh:2930-3005`) pass cleanly under the updated counter key regex.
