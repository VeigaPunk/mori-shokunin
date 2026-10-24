# ConnectNoHarmAxes — Round 15 Cross-Axis No-Harm Synthesis (C1 Coverage)

**Seat:** `MoriR15.ConnectNoHarmAxes` (role: connector, leaf).  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`  
**Target File:** `.ufo/waves/round-15/build/ConnectNoHarmAxes.md`  
**Milestone:** Retain validated positives without fabricated totals.  
**Judged Axis:** Coverage (owned axis 6).  
**Constraint:** Report-only bounded cross-axis review; no builds, tests, linters, formatters, or executions. No tool installations were performed (parent host-safety notice received and observed).

---

## 1. Grounded Evidence

Evidence sourced from local repository artifacts and current round cache:

1. **Production Census (`tools/mori-census.sh` @ `0e41cb83…`):**
   - Aggregate all-or-nothing gating at lines 973–976 (`JOURNAL_JQ_TAIL`, `JOURNAL_JQ_MSGID`, `JOURNAL_JQ_SIGKILL`) and lines 1019–1037 (`JOURNAL_JQ_UNITS`): any non-matching, foreign-boot, or malformed record in a query stream forces the entire class to evaluate to `record-invalid`, `multi-boot`, or `boot-mismatch`.
   - Result suppression at lines 1303–1321 (OOM alarm) and lines 1340–1351 (user `KILL_SIGNAL_JOURNAL` warn): alarms fire strictly from positive numeric values in `ko`, `uo`, `ps`, and `us`. When `js[...] != ok`, these fall back to `unavailable:<reason>`, completely suppressing critical OOM and warning signal alarms even if a valid current-boot record is present in the stream.
   - Exact line and field constraints: line 3050 checks that `FINDING OOM_KILL_JOURNAL` does not contain `count=`; lines 3051–3053 require fields `user_notice`, `system_notice`, `user_unit_oom`, `system_unit_oom` exactly once under word boundaries (`\b$f=`); line 1331 enforces exactly one global `OOM_KILL_JOURNAL crit` line; line 1353 enforces one `KILL_SIGNAL_JOURNAL warn` line for user scope only.
   - Drift volatile contract at lines 2259–2273 (`DRIFT_COUNTER_KEYS`, `DRIFT_VOLATILE_LIST`) and lines 2481–2483: altering the declared volatile list triggers `MORI_DRIFT: volatile_fields` (exit 1).

2. **Regression Gate (`tools/mori-round14-regressions.py` @ `c39e5a73…`):**
   - Retained control `R14_SEC_DUP_MSGID_MIXED` (lines 1732–1744): tests a stream containing one valid OOM notice plus one malformed `MESSAGE_ID` array record. In Round 14, this was explicitly pinned to `forbid_ids=FORBID_OOM` and `kernel_oom_notice=unavailable:record-invalid`.
   - Explicit migration note (lines 111–121): documents that under the Round 15 partial-positive contract, `R14_SEC_DUP_MSGID_MIXED` directly conflicts with C1: it must migrate to expecting `positive_kernel_oom=1` plus an OOM crit finding, while keeping the raw aggregate count `unavailable:record-invalid`.

3. **Round 15 Dispatched Evidence & Peer Audits:**
   - `ReviewRouting.md` (F1–F7): identifies that all-or-nothing stream parsing in `journal_query` discards parsed stream context, and highlights the risk of altering `DRIFT_COUNTER_KEYS`.
   - `ReviewKernelPredicate.md` (F1–F8): demonstrates that per-record positive parsing must execute over `$raw` from the same captured output without adding extra `journalctl` invocations, and recommends keeping positives unmasked.
   - `ReviewUnitPredicate.md` (F1–F6): confirms `UNIT_RESULT="oom-kill"` and `UNIT_RESULT="signal"` must be parsed independently of `UNIT`/`USER_UNIT` subject validity.
   - `ReviewRawTotals.md` (F1–F5): identifies the contract conflict in `R14_SEC_DUP_MSGID_MIXED` and warns against emitting positive zero when the query capture fails.
   - `ReviewHarnessPacks.md` (F1–F9): notes that "malformed" records in fixture packs must remain parseable JSON objects with invalid fields (semantic invalidity), not broken non-JSON lines, because broken JSON halts the whole-stream jq parser.
   - `ScribeGateDecisions.md` (§2): establishes that all 64 dispatched seats in Round 15 are wave-internal; none constitute an outside review.
   - `ScribeNoHarmLedger.md` (§1–§3): defines the seven-gate post-integration verification order for L1.

---

## 2. Naming the Six Axes

Mori evaluates every round across six declared axes (two owned, four observed):

1. **Coverage (Owned, Score 6 held; Target of Claim C1):** Breadth of system and user failure modes observed and alarmed. C1 expands coverage by salvaging critical OOM and user signal alarms from valid current-boot records in contaminated streams without claiming arbitrary JSON repair.
2. **Operability (Owned, Score 7 held):** Reliability, fail-closed discipline, and truthfulness of the census engine. Demands zero fabricated totals, strict `unavailable:<reason>` propagation on query failure, clean hermetic execution, and regression gate consistency.
3. **Depth (Observed, Score 5 held):** Precision of domain taxonomy. Differentiates client-supplied notices vs kernel/system execution results, process exits vs unit failure states, and scoped record counts vs victim counts.
4. **Freshness (Observed, Score 5 held):** Behavioral baselines, drift detection, and volatile masking discipline. Compares current output against pinned baselines without contract mutation.
5. **Calibration (Observed, Score 5 held):** Severity accuracy (crit vs warn vs info) and honesty in self-assessment. Avoids scalar score inflation and rejects self-attestation of outside review.
6. **Adjacency (Observed, Score 6 held):** Strict boundary defense. Detection and reporting only; strictly refuses host remediation (Tsukuroi) or worktree orchestration (Kumitate). Refuses to invent fleet ownership when subject metadata is unavailable.

---

## 3. Cross-Axis Analysis & Second-Order Contradictions

Tracing second-order effects of Claim C1 across all six axes reveals four core tensions:

### A. Coverage vs. Operability (The Fabricated Zero vs. Alarmed Positive)
- *Tension:* If a stream capture fails (timeout rc 124, nonzero rc, stderr nonempty) or contains syntactically invalid JSON, reporting `positive_*=0` would falsely indicate that zero OOM/signal events occurred.
- *Second-Order Effect:* Emitting `0` on parser/capture failure constitutes a fabricated total, directly violating the milestone contract and harming Operability.
- *Resolution:* Positive tokens must be fail-closed: on capture or parser failure, they MUST evaluate to `unavailable:<JQ_STATUS>`, never numeric zero. Numeric `0` is valid ONLY when capture succeeds, JSON parses cleanly, and exactly zero matching current-boot records are found.

### B. Coverage vs. Operability (The `R14_SEC_DUP_MSGID_MIXED` Regression Break)
- *Tension:* If Census implements C1, an OOM crit will fire on a stream with mixed valid and invalid `MESSAGE_ID` records. However, `tools/mori-round14-regressions.py:1742` currently forbids OOM on this exact case (`forbid_ids=FORBID_OOM`).
- *Second-Order Effect:* Running the mandatory L1 regression gate `python3 tools/mori-round14-regressions.py` will exit 1 with a claim failure, breaking an existing verification gate and harming Operability.
- *Resolution:* The r14 harness comment (lines 111–121) explicitly registered this migration point for Round 15. L1 must update `R14_SEC_DUP_MSGID_MIXED` in `tools/mori-round14-regressions.py` atomically with the production cutover so that the regression suite passes.

### C. Coverage vs. Freshness (The Volatile List Contract Mutation)
- *Tension:* If new positive tokens (`positive_kernel_oom`, `positive_unit_oom`, etc.) are added to `DRIFT_COUNTER_KEYS` in `tools/mori-census.sh` to mask them during drift comparison, line 2273 recalculates `DRIFT_VOLATILE_LIST`.
- *Second-Order Effect:* Line 2482 detects that `base_vol != DRIFT_VOLATILE_LIST` and triggers `MORI_DRIFT: volatile_fields` (exit 1). Modifying the list mutates the volatile contract itself.
- *Resolution:* Do NOT add the positive evidence tokens to `DRIFT_COUNTER_KEYS`. The existing baseline is quiet (zero findings) and does not emit OOM finding lines. Leaving the positive counters unmasked matches the raw counts (which are also unmasked) and preserves the volatile contract.

### D. Coverage vs. Adjacency (The Attribution Leakage Risk)
- *Tension:* Valid unit OOM records (`UNIT_RESULT="oom-kill"`) may have malformed, ambiguous, or missing `UNIT`/`USER_UNIT` fields.
- *Second-Order Effect:* If Mori attempted to salvage unit failure routing (attributing to `owner=mori` or `owner=tsukuroi`) from positive evidence when subject metadata is invalid, it would guess fleet ownership without evidence, generating false remediation signals and violating Adjacency.
- *Resolution:* Positive evidence gates ONLY the single global `OOM_KILL_JOURNAL crit` alarm and user `KILL_SIGNAL_JOURNAL warn`. The unit failure owner partition (`UNIT_FAILURE_JOURNAL`, `UNIT_FAILURE_OUT_OF_SCOPE`, `UNIT_FAILURE_UNATTRIBUTED_JOURNAL`) remains aggregate-only and falls back to `unavailable` whenever the aggregate class is invalid.

### E. Calibration Discipline (No Scalar Inflation)
- Repairing the all-or-nothing omission restores coverage to its intended scope (lowest owned axis 6). In accordance with Round 14 precedents (`SCORECARD.md:753-754`), no scalar point is pre-awarded or inflated (coverage remains **6 held**).
- Internal review by dispatched seats cannot be counted as outside discernment (`ScribeGateDecisions.md:38`).

---

## 4. The Proposed Move: Orthogonal Positive Evidence Plane

To improve **Coverage** without harming **Operability**, **Depth**, **Freshness**, **Calibration**, or **Adjacency**, the round should execute one bounded, compatible synthesis: **The Orthogonal Positive Evidence Plane**.

### Specification of the Move:

1. **Single-Capture Decoupled Extraction:**
   - In `tools/mori-census.sh:journal_query()`, retain the single `CAP_OUT` capture (no added `journalctl` process).
   - After verifying `CAP_RC == 0` and `err_bytes == 0` and `jrc == 0`, execute a per-record positive extraction over `$raw` using `"$JQ_BIN"` before or alongside the aggregate check.
   - Guard every record with `type == "object"`, scalar `_BOOT_ID == $boot`, and scalar `MESSAGE_ID == $id`.
   - Positive criteria:
     - `positive_kernel_oom`: kernel MESSAGE_ID matching `fe6faa94e7774663a0da52717891d8ef`.
     - `positive_unit_oom`: unit MESSAGE_ID matching `d9b373ed55a64feb8242e02dbe79a49c` with `(.UNIT_RESULT? | type) == "string" and .UNIT_RESULT == "oom-kill"`. Subject fields are ignored.
     - `positive_unit_signal`: unit MESSAGE_ID matching `d9b373ed55a64feb8242e02dbe79a49c` with `(.UNIT_RESULT? | type) == "string" and .UNIT_RESULT == "signal"`.
     - `positive_process_sigkill`: process MESSAGE_ID matching `98e322203f7a4ed290d09fe03c09fe15` with `(.EXIT_CODE? | type) == "string" and .EXIT_CODE == "killed"` and scalar status `((.EXIT_STATUS? | type) | IN("string","number")) and ((.EXIT_STATUS | tostring) == "9")`.
   - Fail-closed status: on any capture failure (`rc != 0`, `timeout`, `stderr-nonempty`) or syntax failure (`malformed-json`), all positive variables are set to `unavailable:<JQ_STATUS>`.

2. **Preserving Aggregate Unavailable Semantics:**
   - Raw aggregate tokens (`kernel_oom_notice=`, `unit_failure_record=`, `unit_oom=`, `unit_fleet=`, etc.) remain 100% strictly `unavailable:<reason>` when any record violates the aggregate contract. No raw numeric zero is fabricated.

3. **Additive Finding and Surface Presentation:**
   - On `FINDING OOM_KILL_JOURNAL crit`:
     - Retain the exact canonical `paths=` vocabulary (`kernel_oom_notice`, `unit_result_oom_kill`). Set the path if either raw count > 0 OR positive count > 0.
     - Retain raw tokens (`user_notice=`, `system_notice=`, `user_unit_oom=`, `system_unit_oom=`) unmodified (allowing them to read `unavailable:<reason>`).
     - Append distinct positive tokens per scope: `user_positive_kernel_oom=`, `user_positive_unit_oom=`, `system_positive_kernel_oom=`, `system_positive_unit_oom=`.
     - Do not introduce `count=` on the OOM line (respecting line 3050).
   - On `FINDING KILL_SIGNAL_JOURNAL warn` (user scope only):
     - Retain canonical `paths=` (`process_sigkill`, `unit_result_signal`).
     - Retain raw `count=$ps process_sigkill=$ps user_unit_signal=$us`.
     - Append `positive_process_sigkill=` and `positive_unit_signal=`.
   - On `SURFACE journal.<scope>`:
     - Append the four literal tokens `positive_kernel_oom=`, `positive_unit_oom=`, `positive_unit_signal=`, `positive_process_sigkill=`.

4. **Atomic Gate Re-pinning (`R14_SEC_DUP_MSGID_MIXED`):**
   - L1 updates `tools/mori-round14-regressions.py:1732-1744` to remove `FORBID_OOM` and assert the positive OOM alarm on the mixed stream, fulfilling the migration notice at lines 111–121.

5. **Volatile Contract Invariance:**
   - Do NOT add positive tokens to `DRIFT_COUNTER_KEYS` or `DRIFT_VOLATILE_SPECIAL`.

---

## 5. Second-Order Risks and Residuals

1. **Non-JSON Stream Failure (Parse Boundary):**
   - If a stream contains non-JSON bytes (broken syntax), `jq -s` fails globally with `malformed-json`. Under the contract, positives are unavailable on parser failure. This is not arbitrary JSON repair; the move accepts this residual boundary honestly.
2. **Client-Supplied Trust:**
   - `MESSAGE_ID` and unit strings are client-supplied. Positive evidence reflects validated structured record presence, not kernel-authenticated process provenance or unique victim counts. Finding notes must retain `trust=client-supplied`.
3. **Word-Boundary Regex Sensitivity:**
   - New finding fields must avoid substrings that collide with existing regex tests (e.g. `user_unit_oom` check in line 3052). Using `user_positive_unit_oom` avoids colliding with `\buser_unit_oom=`.

---

## 6. Verification and Hand-off Checklist for L1 / Main Agent

This seat executed no verification commands. L1 should run the maintained gates once after integrating the production changes:

1. `bash tools/mori-census.sh --selftest`
   - Verify all existing cases pass.
   - Verify new positive-token cases pass (including mixed valid/foreign-boot and valid/malformed-field cases).
   - Verify word-boundary checks (`count=`, `\b$f=`) still succeed.
2. `python3 tools/mori-round14-regressions.py --selftest`
   - Verify harness self-consistency.
3. `python3 tools/mori-round14-regressions.py --output /tmp/mori-r14-check`
   - Verify `R14_SEC_DUP_MSGID_MIXED` reflects the migrated positive alarm expectation and that zero claims fail.
4. `python3 tools/mori-round13-regressions.py --selftest`
   - Verify r13 harness self-consistency.
5. `python3 tools/mori-round13-regressions.py --output /tmp/mori-r13-check`
   - Verify legacy r13 expectations remain green.
6. `bash tools/mori-silence-cases.sh`
   - Verify oracle silence grading does not drift (`matched == total`).
7. `bash tools/mori-census.sh` (live run)
   - Verify read-only live census executes without crash (rc 0 or 1).
8. `tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json`
   - Confirm that `volatile_fields` drift is NOT triggered (volatile list unchanged).

---

## 7. Tooling Record

- **Installed/Updated:** None.
- **Commands Run:** Greps and reads only; no pacman, uv, or binary installations performed. Parent host-safety directive was observed.
