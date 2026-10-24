measured 2026-10-23T11:52:03Z
control K9 shape harness-keyed
control_sha256 231ec3ea67bf808550cdd13a20f185c5e41a01db30edfb3bae064e416c30b1a4
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

# Scope and axes

Axes: contract fidelity, harness discrimination, exact restoration, bounded execution.
Lane-relative paths below are rooted at /home/vgpnk/Projects/shokunin/mori-shokunin.
Mutant: c0/controls/K9.py under .ufo/waves/round-36; only the classification gate differs from the isolated pristine classifier. The gate runs the contract rules for a resolved root under /fast/scratch or /tmp, or a row URL hostname of 127.0.0.1. Otherwise it emits fresh when a copy exists and no-copy otherwise, without fetching. Evidence: .ufo/waves/round-36/c0/controls/K9.py:103-113; contract rules: .ufo/waves/round-36/contract.md:33-47.
Expected detector: the frozen count-c1.py, with the deliberately defective substitute supplied through --tool. A rejecting detector would report C1=unmet; the actual output is recorded without changing the claim.

# Freeze verification

Command: timeout 20 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
Exit 0. Actual output:
```
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```
Both match .ufo/waves/round-36/evidence/freeze.txt:3-4. Both hashes were checked again before scoring and after scoring; unchanged.

# Full scored counter receipt

Started 2026-10-23T11:51:14Z. Environment: PYTHONDONTWRITEBYTECODE=1; MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK9; TMPDIR=/fast/scratch/hyaku/mori-r36/CtlK9. Working directory: /fast/scratch/hyaku/mori-r36/CtlK9. No --seed was supplied.
Command:
```
timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K9.py
```
Full stdout:
```
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=204 oracle_fetched=42 oracle_fresh=35 oracle_drifted=7 oracle_excluded=0 tool_exit=1 tool_rows=204 mismatches=0
C1=met
seed=8263611602021418904
```
Full stderr: empty (0 bytes).
Counter exit: 0.
VERDICT: K9 met exit 0

Coverage finding: the harness-keyed mutant survived. Both counter arms create their roots using scratch_dir(), including the real git-archive arm, so both run inside the accepted root prefix in this receipt. Evidence: .ufo/waves/round-36/count-c1.py:529-545,565-585; environment and output above; control gate at .ufo/waves/round-36/c0/controls/K9.py:105-113. The nontrusted-root fallback is not exercised by this receipt. The met control is reported to the integration owner under the frozen decision rule, not treated as a passing implementation or an amended claim (.ufo/waves/round-36/contract.md:85-88).

# Isolated mutation and restoration

Scratch source: /fast/scratch/hyaku/mori-r36/CtlK9/probe.py.
Single behavior-bearing mutation: line 110 changes an unconditional correct-classifier branch to the K9 hostname/root gate; it is then restored to the unconditional branch. The mutated scratch bytes have exactly the control hash above.
Detector: /fast/scratch/hyaku/mori-r36/CtlK9/detect-blind.py:8-17. It executes the unmodified frozen counter's blind_arm with random.Random(3609), unchanged for all three phases. This is a bounded blind-arm probe, not three full scored receipts; no pristine/restored real-arm result is claimed.
Detector sha256 from timeout 10 sha256sum: 24ddc5fe6fdaf0963795abf6b6e3f5014edc646fb08164eeb5fd6d307c7a6469.
Each phase used the same command and the environment recorded above:
```
timeout 120 env PYTHONDONTWRITEBYTECODE=1 MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK9 TMPDIR=/fast/scratch/hyaku/mori-r36/CtlK9 python3 /fast/scratch/hyaku/mori-r36/CtlK9/detect-blind.py /fast/scratch/hyaku/mori-r36/CtlK9/probe.py
```

Pristine sha256: d92c80a2cacd624cc3ff1488e3beb8ccae8e8eb0ed39718c52965eca91abc289.
Actual pristine output, exit 0:
```
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
bounded_blind=met
```
Mutated sha256: 231ec3ea67bf808550cdd13a20f185c5e41a01db30edfb3bae064e416c30b1a4.
Actual mutated output, exit 0:
```
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
bounded_blind=met
```
Restored sha256: d92c80a2cacd624cc3ff1488e3beb8ccae8e8eb0ed39718c52965eca91abc289.
Actual restored output, exit 0:
```
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
bounded_blind=met
```
Mutation outcome: survived the bounded blind detector; baseline and restoration both passed. Restoration evidence: timeout 10 sha256sum on the scratch source returned the pristine hash before mutation, after restoration, and after the full scored run. The assigned lane control intentionally retains K9; only the scratch probe was restored.

# Containment and teardown

Command timeout 15 df -h /fast reported 70G available before scratch writes. Command timeout 10 wc -lc on the control, restored scratch source and detector reported 4179, 4107 and 508 bytes respectively; the report was 81 lines. No tool installs or updates; no lane commits or index operations.
Process teardown observation: timeout 10 ps -eo args, captured and reduced in memory to exact probe/control script-path matches, reported owned_probe_processes=0. The scored subprocess had completed with counter_completed_exit=0 and counter_stderr_bytes=0. No process identifiers or raw process listing were written.
