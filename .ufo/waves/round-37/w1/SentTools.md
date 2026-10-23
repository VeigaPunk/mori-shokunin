# Round 37 security review — counters and fixtures

Scope: `count-c1.py`, `count-c2.py`, and all three `fixtures/*.py`; static review only. No counter, fixture, target tool, or network operation was run. No tools were installed.

## Findings

### HIGH — Candidate code executes with the counter user's full privileges

- **Exploit path:** A caller points C1 `--tool` at an untrusted Python file, or selects an untrusted repository/revision with `--repo` and `<rev>`. C1 runs the supplied or extracted tool under `sys.executable`; C2 extracts the committed drift tool and runs it with `--selftest`. The fixtures also delegate to the hard-coded lane tool. A malicious target can read inherited credentials, access and modify files available to the caller (including the checkout), and use the network. The selected `clean_env()` functions only remove some Git variables; they preserve the rest of `os.environ` and do not restrict filesystem or network access.
- **Evidence:** `count-c1.py:80-85,532-535,874-888`; `count-c2.py:95-99,151-160`; `fixtures/memo-n1.py:29-33`; `fixtures/summary-only.py:16-20`. The subprocess arguments are lists (no shell interpolation), but the Python target is still intentionally executed directly.
- **Impact:** Testing untrusted input is arbitrary code execution as the invoking user, outside the claimed scratch boundary; timeout handling is not a security sandbox.
- **Smallest remediation:** Treat repository revisions and `--tool` inputs as trusted-only and enforce that boundary, or run targets in an OS sandbox with restricted filesystem, isolated environment/secrets, and network denied.

### MEDIUM — C2 committed-file reads have no timeout or output bound

- **Exploit path:** Run C2 against an untrusted or pathological `--repo`/revision whose Git operation stalls (for example, an unavailable mounted repository) or whose committed source/receipt objects are very large. `show()` blocks in `subprocess.run()` without a timeout and buffers complete output with `capture_output=True`.
- **Evidence:** `count-c2.py:102-112`; `main()` calls `show()` on the selected revision at `151,187,195,202,208`.
- **Impact:** A run can hang indefinitely or consume excessive memory before the bounded self-test runner is reached. C2's documented probe timeout does not cover these reads.
- **Smallest remediation:** Apply a bounded timeout and size-limited reads to the Git subprocesses, and fail closed when the limits are exceeded.

### LOW — Relative `--tool` paths are checked and executed from different directories

- **Exploit path:** From a checkout, pass a relative `--tool` path that exists there. `os.path.isfile()` validates it relative to the counter's current directory, but `run_tool()` sets the subprocess cwd to `/`, so Python resolves the same relative spelling under `/` instead. A different file can be selected if that root-relative path exists; otherwise execution fails.
- **Evidence:** `count-c1.py:532-535,874-878`.
- **Impact:** Target selection is ambiguous for relative paths and can execute an unintended root-relative file.
- **Smallest remediation:** Convert the requested path to an absolute path once, before validating and invoking it.

## Scoped checks

- No direct shell API or `shell=` use was found in the scoped files; subprocess commands are constructed as argument lists. Static search for `shell\s*=`, `os.system`, `os.popen`, and common socket/HTTP client APIs returned **“No matches found”**. Thus there is no direct shell injection or counter/fixture HTTP client in this scope; the executed candidate code is not network-restricted.
- C1's sandbox histories and C2's extracted/mutant files are created under temporary directories and removed in `finally` blocks (`count-c1.py:929-947`; `count-c2.py:153-185`). C1 also creates its challenge history under the fixed lane `.ufo/waves/round-37/scratch` parent (`count-c1.py:56,762-763`) and removes the per-run root in `finally` (`791`). Temp-file cleanup is best-effort (`ignore_errors=True`) and cannot clean after abrupt termination.
- C1's `--repo` and `--tool` values are passed as arguments, not interpolated into a shell command. The trust-boundary finding above is code execution by design, not shell metacharacter injection.

VERDICT: FAIL
