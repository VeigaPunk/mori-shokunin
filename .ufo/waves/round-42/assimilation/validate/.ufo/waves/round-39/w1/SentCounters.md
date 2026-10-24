# C7 / C8 security review

**Axes:** path and symlink containment; scratch confidentiality/confinement; executed-code boundary and timeout cleanup. Reviewed the current working-tree sources; no probe or hang fixture was executed.

## HIGH — CLI-selected probe/counter is unsandboxed Python execution

**Exploit path:** A caller runs C7 with `--arms selftest --tool /attacker/probe.py`, or runs C8 with `--counter /attacker/counter.py`. The supplied file is executed by the current Python interpreter as the caller. In C8, the first counter is run for `--print-predicate`, `--pin-only`, and `--print-tool` before its source is read for static checks; static inspection is not a safety gate. Symlink and non-repository paths are not rejected for either CLI option.

**Evidence:** C7 accepts `--tool` at `count-c7.py:391`, invokes it at `:428-435`, and starts `[sys.executable, tool]` without an explicit `cwd` or `env` at `:140-146`. C8 accepts repeated `--counter` at `conform.py:522`; `evaluate` invokes the first path at `:314`, `:321`, `:331`, and `:369`, while reading source later at `:343-350`. C8's `run` inherits the environment except for four removed Git variables (`conform.py:82-90`).

**Impact:** This is arbitrary code execution with the invoking account's filesystem/network access; C7's tool additionally inherits the full environment, potentially including credentials. The list-form subprocess arguments avoid shell parsing, but do not constrain the Python program.

**Smallest remediation:** Treat these paths as trusted-code inputs and reject untrusted use, or run them in an actual low-privilege sandbox with a minimal environment, isolated working directory, and filesystem/network/resource restrictions. Canonicalizing a path alone does not make its contents safe.

## MEDIUM — Scratch path is not confined or symlink-checked

**Exploit path:** C7's `--repo` selects the Git read root, but its scratch destination stays fixed at `DEFAULT_REPO`; an invocation against another repo still creates and removes work directories in the lane. If the lane's `scratch` path is replaced with a symlink to another directory, `os.makedirs(..., exist_ok=True)` and `mkdtemp(dir=...)` follow that destination. Separately, C8's scratch check can accept a candidate whose `SCRATCH_ROOT` expression is `os.path.join("/tmp", ".ufo", "waves", "round-39", "scratch")`: it only searches the expression text for those four component strings and checks for any `mkdtemp(..., dir=...)`; it does not resolve or inspect the destination, symlink status, ownership, or permissions.

**Evidence:** C7 hardcodes `SCRATCH_ROOT` from `DEFAULT_REPO` at `count-c7.py:55-62`, converts `--repo` separately at `:389-404`, then creates the root and workdir at `:475-476`. C8's checks are lexical at `conform.py:248-264` and are reported as `scratch` at `:379-394`. The observed current scratch metadata was `drwxr-xr-x 755 vgpnk:vgpnk directory .ufo/waves/round-39/scratch`; the current root was not observed as a symlink.

**Impact:** A candidate can receive a passing `scratch` check while writing outside the intended root, and the C7 `--repo` option can cause unexpected lane-local writes during an otherwise alternate-repo run. A symlinked root redirects those temporary writes. The observed 0755 parent is not itself evidence that generated child contents are readable; the checker simply does not verify effective permissions.

**Smallest remediation:** Resolve and validate the actual scratch destination (including symlinks, ownership, and mode) before creating anything; make the `--repo`/scratch relationship explicit and reject out-of-root destinations. Have C8 evaluate the resolved path and effective directory permissions rather than source substrings.

## MEDIUM — C8 timeout does not clean up a counter's process tree

**Exploit path:** A counter started by C8 spawns a long-lived child and then hangs or exits. C8's timeout supervises the direct Python process only; the child can remain running, including after the timeout result is returned. This is a process-cleanup gap for untrusted or buggy counters, distinct from the explicit code-execution issue above.

**Evidence:** `conform.py:82-90` uses `subprocess.run(..., timeout=...)` and catches `TimeoutExpired`, with no new session or process-group cleanup. The calls at `:314`, `:321`, `:331`, and `:369` run counters under that wrapper. By contrast, C7's `run_tool` starts the tested tool in a new session and sends signals to its process group at `count-c7.py:144-169`.

**Impact:** A timed-out counter can leave workers/background processes consuming resources or continuing work under the caller's identity. C8's `run` returns a timeout result without establishing that descendants stopped.

**Smallest remediation:** Start each counter in a dedicated session and terminate/reap its process group on timeout (with a bounded grace period), or use a supervisor that provides equivalent process-tree cleanup.

## Hang fixture / path observations

The shipped hang fixture itself prints and flushes, then only calls `time.sleep(120)`; it creates no child (`fixtures/hang-after-flush.py:11-16`). C7 launches it in its own session and attempts group SIGTERM/SIGKILL on timeout (`count-c7.py:144-169`), so the fixture does not demonstrate a process-group escape. I did not run the fixture. Git and Python commands use argument lists rather than shell command strings (`count-c7.py:186-189`; `conform.py:82-88`); C8 also checks the resolved fixture path against the resolved repo root (`conform.py:331-338`). No shell-injection or current scratch-symlink finding was established from these paths.
