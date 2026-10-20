# ReviewCapture — Round 16 capture refusal and owned child reap

Lane: reviewer (leaf). Read-only except this report. No execution, no builds, no tests, no commits.

## Read-time state (2026-10-20 05:48–05:49 -03:00)

- Target `tools/mori-journal-window.py`: **ABSENT**. Checked twice (glob of `tools/**`, `ls -la tools/`, and `test -e`) and a repo-wide glob for `*journal*` (only `corpus/knowledge/journal-*.md` matched). The WindowTool executor (spec `wave1-spec.json` item `WindowTool`) had not yet written the file.
- Consequence: no timeout, overflow, stderr, nonzero-rc, or child-reap code could be reviewed. **No finding below is a verdict on the production tool.** This report is a pre-review contract checklist plus one hazard found in the sibling harness pattern. L1 should re-run this review once `tools/mori-journal-window.py` exists, reading it at that time and recording the new read-time.
- `build/` contained only `swarm-registry.json` at read time.

## Contract the implementation must satisfy (from spec `WindowTool` prompt and task contract)

Source: `.ufo/waves/round-16/wave1-spec.json` items `WindowTool` (line 10) and `ReviewCapture` (line 245).

C-1. Bounded streaming collection for BOTH stdout and stderr with a wall-clock timeout AND a byte cap per stream. No unbounded `communicate()` / `read()` allocation.
C-2. On timeout: kill and reap only the owned journal child. No process-group kill that could reach the harness or unrelated processes unless the child was started with `start_new_session=True` and the kill is scoped to that session.
C-3. On byte overflow (either stream): stop reading, kill/reap owned child, return rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE` with a stable reason (overflow). No numeric positive totals.
C-4. stderr is never echoed to stdout, never written to any file, and any non-empty stderr is an unavailable refusal (rc2), not a clean window.
C-5. Nonzero journalctl returncode → rc2 unavailable. Stdout content must not be parsed in that case.
C-6. Timeout, overflow, stderr, nonzero rc, malformed/empty capture, missing/mismatched/duplicate cursor, foreign boot → all rc2 unavailable with no positive totals. Missing anchor continuity means unavailable, never clean.
C-7. Stdout of the tool must not echo raw cursor or any record; only the SHA256 of the anchor is permitted.
C-8. Reap must happen on every exit path (success, timeout, overflow, exception). A bounded post-kill wait is required; an unbounded `communicate()` after kill is a hang vector if a descendant escapes the session and holds the pipe.

## Hazard observed in sibling harness (NOT the new tool)

File: `tools/mori-round15-regressions.py`, function `execute_census`, lines ~1006–1032 (read-time, `#7D44`).

- It does use `start_new_session=True` (line 1016), so `os.killpg(os.getpgid(proc.pid), 9)` (line 1028) is scoped to the child's session. Good.
- Line 1031: after the kill, `proc.communicate()` is called with NO timeout. If any grandchild calls `setsid`/double-forks out of the group while holding the stdout/stderr pipe, this blocks indefinitely. The new tool must not copy this pattern; post-kill reap must be `wait(timeout=…)` with a bounded drain.
- Line 1023 uses `communicate(timeout=timeout)`, which buffers unbounded output into memory before the timeout is enforced. Byte caps are not enforced here. The new tool must not copy this either (C-1).

Severity: medium for the new tool if copied; informational for r15 (its own lane, not a round-16 deliverable).

## Review checklist for L1 once the file exists

1. Locate `Popen`/`subprocess.run`/`communicate` in `tools/mori-journal-window.py`. Any `communicate()` without a bounded timeout, or `read()` without a byte cap, is a C-1/C-8 defect.
2. Confirm stdout and stderr are both drained concurrently or via selectors with a byte budget each. A pipe filled on one side while the other is blocked is a deadlock vector.
3. Confirm the kill path targets only the owned child (`proc.kill()` or `os.killpg` only with `start_new_session=True`, and `getpgid` taken from the owned child). Confirm `ProcessLookupError` is handled.
4. Confirm `proc.wait()` after kill is bounded (`timeout=`), and that a failure of the bounded wait still returns rc2 without hanging.
5. Confirm every exit path (`finally` or equivalent) closes pipes and reaps the child.
6. Confirm stderr contents are never printed, returned, or written. Confirm non-empty stderr → rc2 refusal, with a stable reason string that does not include stderr text.
7. Confirm nonzero rc → rc2 without parsing stdout.
8. Confirm the overflow reason and timeout reason are distinct stable strings, and that neither leaks raw bytes.
9. Confirm the `--timeout` and `--max-bytes` defaults and bounds are validated (non-positive or absurd values → rc2 MORI_JOURNAL_WINDOW_SETUP, not a hang).
10. Confirm the selftest wrappers in the fixtures exercise: timeout (delayed child), overflow (large stdout), stderr-present with rc0, nonzero rc, and a grandchild that escapes the session if feasible. Verify the test asserts rc and finding id and does not depend on live journald.

## Findings

- None against the production tool (file absent at read time).
- Pre-review hazard recorded above (sibling harness unbounded post-kill `communicate()` and unbounded pre-timeout buffering). Not a round-16 defect in the new tool; it is a pattern the new tool must not copy.

## Residual risk and verification gaps

- Entire C-1..C-8 surface is unverified against the production code. Risk is high until the file lands and is reviewed.
- Escaped-grandchild behaviour cannot be assessed without the implementation.
- No execution was performed (per assignment). No tool installs. No pacman transactions.

## Tooling record

- No tools installed or updated by this reviewer.
