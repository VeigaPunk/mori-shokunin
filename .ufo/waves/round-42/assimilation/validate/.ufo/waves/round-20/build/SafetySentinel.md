# C2 security review — SafetySentinel

## Scope and evidence

Reviewed the frozen design at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/contract.md` and the oracle at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/frozen/c2-expected.json`. The contract requires non-following symlink discovery and report checks (contract lines 64–77), path validation (70–73), report-byte non-emission (77), and output fields including `lane_root`, `dispatch_path`, `members`, and missing member names (82–85). The oracle has traversal, absolute-path, symlink-report, and canary cases (oracle lines 14–19).

No implementation was available to verify: the `build/ImplSettlement*/` directory glob returned no matches; the top-level `ImplSettlement.md` and `ImplSettlementAlt.md` each contained only `STATUS: started` at line 1. The `tools/` listing had no `mori-wave-settlement.py`. Accordingly, exploit paths below are design risks, not confirmed runtime defects.

## Findings

### High if the lane can change during a scan — path checks need race-resistant no-follow access

**Exploit path [INFERENCE]:** a concurrent writer replaces a discovered dispatch file with a symlink after enumeration/type checking, or swaps a report-path component after containment validation. A check-then-open sequence can then follow a link outside the lane. The fleet-root fallback has the same exposure if it reuses ordinary path checks. An escaped dispatch can be parsed and its derived fields/hash emitted; an escaped report can at least leak existence/size and be misclassified. A symlink at `--out` (or a replaceable parent) can also redirect the promised write to a different target.

**Evidence:** the design promises symlinks are not followed (contract 64–67) and rejects absolute/`..` report paths (70–73); the oracle covers a traversal and final symlink (oracle 14–16). Neither specifies atomic access or protection against a path changing between validation and use. `--out` is an explicit write exception (contract 56), but its symlink behavior is unspecified.

**Impact:** path containment can be bypassed under concurrent mutation; outside dispatch data may influence output, and filesystem metadata or output bytes may reach an unintended target.

**Smallest remediation:** pin the lane root directory descriptor; traverse directories relative to pinned descriptors with no-follow directory opens; open dispatches and report candidates with `O_NOFOLLOW`, then use `fstat` on that same descriptor to require a regular file. Read/hash/parse dispatch bytes from the same opened file, never reopen by pathname. Apply identical containment rules to fleet-root lookup. For `--out`, reject symlinked path components or pin its parent and write via a temporary regular file plus atomic replace without following the destination symlink. Treat any symlink component in report paths as not-followed/unsafe, consistently with the frozen oracle.

### Medium — unbounded discovery, parse, and output permit resource exhaustion

**Exploit path [INFERENCE]:** a lane contains a huge `.json`, an extremely deeply nested JSON value, or very many files/tasks/long names. Hashing and `json.loads` can consume unbounded I/O, CPU, and memory; a valid file with an enormous task list can also create unbounded output. A deep value can raise `RecursionError`; no failure/limit behavior is defined.

**Evidence:** discovery covers every matching JSON under the tree (contract 64–67) and every wave/member is represented in output (82–85); no byte, depth, file-count, task-count, path/name-length, total-work, or output-size bound is stated. The oracle's malformed-JSON case (12) does not establish behavior for oversized or deeply nested input.

**Impact:** a crafted or accidental lane can stall/crash the scan or exhaust resources, preventing settlement results for other seats.

**Smallest remediation:** freeze explicit per-file and aggregate byte/file limits, parser nesting/token and task/member limits, and bounded output/string limits. Enforce byte limits while reading (not just via a prior `stat`) and handle parser/OS failures without traceback or input excerpts. Define a visible, deterministic over-limit outcome and nonzero exit before implementation; do not silently omit records while claiming complete coverage.

### Medium — output fields can disclose private paths or attacker-controlled labels

**Exploit path [INFERENCE]:** if `lane_root` is serialized as an absolute path, output exposes host/user directory names. If `dispatch_path` is not explicitly lane-relative, it could expose an absolute path. A dispatch author can put path-like or sensitive text in a member `name`; the required `missing` list then echoes that value even if report paths themselves are omitted.

**Evidence:** `lane_root`, `dispatch_path`, `members`, and `missing` are required output fields, with missing names explicitly serialized (contract 82–85). The member/output schema does not define path relativity, name character/length constraints, or whether `agent`, raw task text, or report paths are excluded.

**Impact:** scans copied to shared logs or reports can reveal local filesystem layout or untrusted task metadata. A “member name” is not safe merely because it is not the report pathname.

**Smallest remediation:** define `dispatch_path` as a normalized lane-relative path only; emit `lane_root` as a stable non-path label (or document and require an explicit redaction-safe label). Keep member output to the contract-required name/status only—never emit `agent`, task text, or expected report path. Bound and validate names as labels with no separators/control characters; use a deterministic opaque label for invalid names rather than echoing arbitrary input. JSON-escape all emitted strings.

### Report-content emission — contract safeguard present; preserve it in implementation

The contract already says report bytes are never emitted (77), and the oracle checks a report canary is absent from both stdout and `--out` (19). The status calculation only needs regular-file type and size (`present` means size > 0; contract 74), so report contents need not be opened/read. **No emission defect is confirmed because no implementation was available.**

**Smallest guard:** classify report files with descriptor metadata only (`fstat` after no-follow open); never read/hash them, include their path or contents in output, or stringify exceptions containing raw input. Keep diagnostics bounded and free of report bytes. Exercise the canary against stdout, the output file, and any error path.

## Verification

Read-only review only. No implementation, tests, builds, or selftests were run; none are claimed as passed. No tools were installed or updated.