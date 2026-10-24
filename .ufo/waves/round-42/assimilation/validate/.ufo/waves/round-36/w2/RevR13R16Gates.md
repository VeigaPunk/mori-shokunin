# RevR13R16Gates — lane regression-gate battery (no-harm to operability)

Seat: RevR13R16Gates (mori round 36, wave 2, attempt 2)
Attacks: C2 (measured, operability) / C1 (exploratory) no-harm — pre-existing round-13..17,
retention, freeze-order, dispatch-ledger, content-review gates after round-36 changes.
Lane tip: bf0df77fee4b6ef54a90aea09335c7617f125151 (pushed). Round base: 6bd57097.
Run date: 2026-10-23. Python: 3.14.8.

## Battery results (all commands run in /home/vgpnk/Projects/shokunin/mori-shokunin)

### 1. round-13 (python3 tools/mori-round13-regressions.py --selftest)
```
SELFTEST: case isolated-stub-target-red ok ok
SELFTEST: case isolated-frozen-manifest-tamper ok ok
SELFTEST: pass checks=33 cases=2
EXIT=0
```
Exit code: 0 — PASS.

### 2. round-14 (python3 tools/mori-round14-regressions.py --selftest)
```
SELFTEST: pass checks=20 (parsers + real-gate red rc1/tamper rc2)
EXIT=0
```
Exit code: 0 — PASS.

### 3. round-15 (python3 tools/mori-round15-regressions.py --selftest)
```
SELFTEST control classifier checks: PASS
SELFTEST PASS selftest_root=/tmp/mori-r15-selftest-jvp0w4gq
EXIT=0
```
Exit code: 0 — PASS (sandbox root under /tmp, not the lane).

### 4. round-16 (python3 tools/mori-round16-regressions.py --selftest)
```
SELFTEST ok: pin_rc0,green_rc0_verdict_ok,absent_rc1_capability_absent,tool_drift_rc2,bad_want_rc1_mismatch,pack_drift_rc2
EXIT=0
```
Exit code: 0 — PASS.

### 5. round-17 (TMPDIR=.../.scratch python3 tools/mori-round17-seat-regressions.py --selftest)
```
SELFTEST ok: green_rc0_and_manifest,capability_absent_rc1,mismatch_rc1,forbidden_key_rc1,seats_map_projection_rc0,a1_main_sessions_rc0,generated_fifo_rc0,symlink_ancestor_fifo_trap_rc2,unreadable_dirs_sandbox_rc0,root_symlink_rebase_rc0,key_metadata_required_rc1,wrong_type_metadata_rc1,pinned_snapshot_tamper_rc2,prefix_filter_rc0,files_scanned_falsifier_rc1,unreadable_fixture_rc0,fixture_drift_rc2,output_guard_rc2,nonempty_output_rc2
EXIT=0
```
Exit code: 0 — PASS.

### 6. retention gate (TMPDIR=.../.scratch python3 tools/mori-retention-gate.py --selftest)
```
SELFTEST retention-gate PASS 21/21
EXIT=0
```
Exit code: 0 — PASS.

### 7. freeze-order (TMPDIR=.../.scratch python3 tools/mori-freeze-order.py --selftest)
```
SELFTEST freeze-order PASS 12/12
EXIT=0
```
Exit code: 0 — PASS.

### 8. dispatch-ledger (TMPDIR=.../.scratch python3 tools/mori-dispatch-ledger.py --selftest)
```
SELFTEST mori-dispatch-ledger PASS 14/14
EXIT=0
```
Exit code: 0 — PASS.

### 9. content-review (TMPDIR=.../.scratch python3 tools/mori-content-review.py --selftest)
```
{"exit_code":0,"findings":[{"code":"CONTENT_REVIEW_SELFTEST_CLEAN"}],"schema":"mori-content-review-result-v1","status":"clean"}
EXIT=0
```
Exit code: 0 — PASS.

## No-harm verification

- Round changes (git diff --stat 6bd57097 bf0df77 -- tools/) touched exactly three NEW tools:
  tools/mori-index-clean.sh (+242), tools/mori-source-drift.py (+379), tools/mori-sources-appendonly.py (+499).
  None of the nine battery scripts (round13/14/15/16/17, retention, freeze-order, dispatch-ledger,
  content-review) were modified by the round. They are pre-existing and run from tip bf0df77.
- Lane state: `git status --short` immediately before the battery and after all nine runs is
  byte-identical — only pre-existing working-tree modifications (contract.md, dispatch-log.txt,
  corpus/README.md, source-drift-r36.md) and pre-existing untracked items (.scratch/,
  __pycache__/, evidence/*, wave-2 spec files, w2/). No new files, no deletions, no stage changes.
  Selftests created throwaway sandboxes under /tmp (seen in round-15 output) and TMPDIR-scoped
  .scratch; nothing landed in the lane.
- No tools installed/upgraded (nothing was needed; no pacman or other channel used).

## VERDICT

PASS — no defect found. All nine pre-existing gate selftests pass with exit 0 at
bf0df77fee4b6ef54a90aea09335c7617f125151; round-36 changes are additive-only in tools/ and the
battery leaves the lane untouched. No harm to operability (C2) or to the exploratory C1
technique (which itself admits no freshness verdict; no gate here infers one).
