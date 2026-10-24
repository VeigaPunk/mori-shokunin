# AttackBound — round16 critic: unbounded memory, timeout, inherited pipes

Seat: MoriR16.AttackBound (critic, leaf, read-only). Advisory author-lane evidence; not verification.
Nothing executed against the target. Only host facts checked: `python3 --version` (3.14.7), `journalctl --version` (systemd 261.2-1-arch), the stdlib `subprocess.py` source, `/proc/sys/fs/pipe-max-size`, and one in-process `argparse` parse (no target code).
No tools installed or updated.

## Read-time state (2026-10-20)

- `tools/mori-journal-window.py`: **absent** (WindowTool in flight).
- `tools/mori-round16-regressions.py`: **absent** (WindowHarness in flight).
- `.ufo/waves/round-16/fixtures/`: BootBoundary, ExactAnchor, TypedFields, UnitOom, UnitSignal, MissingAnchor, CursorShape, KernelUser present. **Bounds.json absent.**
- The tool and harness did not exist yet, so I attacked the approach (wave1-spec WindowTool/WindowHarness/PackBounds prompts plus the shared Interface/Fixture contract) and the existing r13/r14/r15 subprocess patterns the new code is likely to copy.
- I sent the short findings to MoriR16.WindowTool, MoriR16.WindowHarness and MoriR16.PackBounds.

## Axes

A1 memory bound (tool + harness) · A2 wall-clock bound · A3 kill scope (owned only) · A4 pipe/fd inheritance · A5 stable reason · A6 fixture non-vacuity for bounds.

## Findings (counterexample → evidence → axes → smallest safe correction)

### B1 — Copying the existing harness pattern can leave a post-kill `communicate()` with no time or memory limit [A1 A2 A4] — fixable defect, high
- **Counterexample:** a `timeout:true` wrapper `#!/bin/sh` that runs `sleep 30` as a non-exec child, or that daemonizes with `setsid sleep 30 &`. After `killpg`, the grandchild (or the escaped one) still holds the stdout write end. `proc.communicate()` then waits for EOF that never arrives within the bound.
- **Evidence:**
  - `tools/mori-round15-regressions.py:1025-1031`: `except TimeoutExpired: os.killpg(...,9); raw_out, raw_err = proc.communicate()` (no timeout).
  - `tools/mori-round13-regressions.py:1373-1391`: same shape, also on the `BaseException` path.
  - `communicate()` on POSIX keeps every chunk in `_fileobj2output` lists (`/usr/lib/python3.14/subprocess.py:2116-2125`), so memory is limited only by the timeout times the producer's output rate.
  - `subprocess.run` on POSIX does `process.kill()` and then `process.wait()` (`subprocess.py:559-569`). That kills the pid only, not the group.
- **Correction:**
  - Tool and harness both use one bounded reader: `selectors` + `os.read(fd, 65536)` on the raw fds, a monotonic deadline taken before spawn, and a byte cap per stream.
  - On a bound: `killpg`, then a short `wait(timeout=grace)`, then close the read fds and return. Never wait for EOF after the kill.
  - The harness also caps the tool's own stdout/stderr (for example 1 MiB). Breaching the cap is a case failure (`harness_overflow`), not a host OOM.

### B2 — Kill scope: `killpg(os.getpgid(pid))` without a new session kills the tool's own group [A3] — fixable defect, high
- **Counterexample:** the tool copies r13's `kill_group` (`os.killpg(os.getpgid(proc.pid), sig)`) but spawns journalctl without `start_new_session=True`. `getpgid(child)` is then the tool's own pgid. A timeout SIGKILLs the tool, every process in its pipeline (`mori-journal-window … | jq`), and, when run from a shell job, the whole job. That breaks the HostSafety "owned query timeout termination only" rule.
- **Correction:**
  - Spawn with `start_new_session=True`.
  - Before signalling, assert `os.getpgid(proc.pid) == proc.pid`.
  - Signal while the leader is still unreaped: call `killpg` before `wait`/`poll` returns a code, so the pgid cannot be recycled.
  - Never `pkill`/`killall journalctl`.
  - Wrap the run in `try/finally` so `KeyboardInterrupt` (which, with a new session, never reaches the child) still kills the owned group.
  - The wave1-spec phrase "kill/reap only your owned journal child" should read "owned process group created for this query". Killing only the pid leaves the B1 grandchild alive.

### B3 — Blocking buffered reads ignore the deadline [A2 A5] — fixable defect, medium-high
- **Counterexample:** `select` says stdout is readable (1 byte ready), then the tool calls `proc.stdout.read(65536)` on the default `BufferedReader`, or reads through a `text=True` wrapper. `BufferedReader.read(n)` blocks until it has `n` bytes or EOF. A wrapper that writes the anchor line and then sleeps holds the tool past `--timeout`.
- **Correction:** use only `os.read(fd, n)`, or `read1`, on the fds `select` reported ready. Do not use `text=True` on the capture.

### B4 — Draining one stream at a time stalls the child and changes the reason [A2 A5] — fixable defect, medium
- **Counterexample:**
  - stderr > 64 KiB (pipe default; max 1048576 per `/proc/sys/fs/pipe-max-size`) while the tool reads stdout to EOF first. journalctl blocks on `write(2)`, the deadline fires, and the reason becomes `timeout` instead of `stderr`.
  - Reading stderr first with stdout > 64 KiB inverts it.
  - Both cases return rc2, but the `reason` drifts with the order of reads and flakes against pinned fixtures.
  - Census avoids this with a continuous `wc -c` coprocess draining stderr (`tools/mori-census.sh:1175-1198`).
- **Correction:**
  - Register both fds with one selector and drain each when ready.
  - stderr only needs a count and its first-byte presence. Keep at most 1 byte, never store or echo it.
  - Use a fixed reason priority that does not depend on which bound fired first, for example `setup > overflow > stderr > timeout > rc > parse`. Ignore the killed child's return code (-9) when a bound reason is already set.

### B5 — Truncating at the cap and parsing the prefix gives a false OK [A1 A6] — fixable defect, high (false-positive coverage)
- **Counterexample:** the tool reads chunks, slices the buffer to `max_bytes`, kills the child, and parses what it kept. If byte `max_bytes` lands right after a `\n`, the prefix is a well-formed JSONL window (anchor + K records). The result is rc0 `MORI_JOURNAL_WINDOW_OK` with a smaller `records_after_anchor` and possibly fewer positives: a truncated capture graded as complete. The Goal says "failed/truncated capture stay unavailable".
- **Correction:**
  - Count raw bytes, not decoded characters (with `errors="replace"`, `len(str)` undercounts UTF-8 by up to 4×).
  - Overflow means observing byte `max_bytes+1`: read with a cap of `max_bytes+1`, and if the total exceeds `max_bytes`, return rc2 `overflow` and parse nothing.
  - A capture of exactly `max_bytes` that reaches EOF is valid.

### B6 — Non-finite or unbounded CLI bounds disable the bound [A1 A2] — fixable defect, medium
- **Evidence (in-process argparse check):**
  - `type=float` accepts `--timeout nan` → `Namespace(timeout=nan)`.
  - `float("1e400")` is `inf`.
  - `type=int` accepts `1_0` → 10 and Arabic-Indic digits `"١٢"` → 12.
- **Effect:**
  - `nan`: every `remaining <= 0` comparison is False. Passing it to the selector [INFERENCE] raises, giving a traceback with rc1 instead of rc2 `MORI_JOURNAL_WINDOW_SETUP`.
  - `inf` / `1e400`: no bound, or a crash on overflow.
  - A huge `--max-bytes` value: no memory bound.
- **Correction:**
  - Parse with an ASCII regex: `^[0-9]+(\.[0-9]+)?$` for timeout and `^[0-9]+$` for bytes.
  - Require `math.isfinite`, a floor (`>0`) and a ceiling (for example timeout ≤ 60 s, max-bytes ≤ 64 MiB; L1 picks the numbers).
  - Anything else → rc2 `MORI_JOURNAL_WINDOW_SETUP`.
  - Report the configured bounds in stdout. They are configuration, not measured latency (BudgetPricing seam).

### B7 — The anchor read is unbounded and runs before the timeout starts [A1 A2] — fixable defect, medium
- **Counterexample:**
  - `--anchor /dev/zero`: `open().read()` grows until OOM.
  - `--anchor <fifo>` with no writer: `open()` blocks forever.
  - `--anchor /dev/stdin` with an inherited tty: waits for input.
  - The journal deadline starts later, so `--timeout` never covers any of these.
- **Correction:** `os.open(path, O_RDONLY|O_NOFOLLOW|O_NONBLOCK|O_CLOEXEC)`, then `fstat` and require `S_ISREG` and `st_size ≤ cap`, then read at most `cap+1` bytes (cursor ≤ 4096 bytes, so a cap around 8192 is enough). If more than `cap` bytes come back → SETUP.

### B8 — fd/env inheritance into journalctl or wrappers [A4] — fixable defect, low-medium
- `stdin` must be `DEVNULL`. An inherited terminal or harness stdin lets a wrapper or pager read it.
- `stderr` must be `PIPE`, never inherit and never `None`. With `None`, journalctl writes straight into the harness's stderr pipe: it is echoed into the raw streams (leak; AttackOutputLeak seam) and, if journalctl lingers, it pins the harness pipe open (B1).
- `close_fds=True` is the Python 3 default; do not pass `pass_fds`.
- Add `--no-pager` as census does (`tools/mori-census.sh:1190`). [INFERENCE] journalctl starts no pager when stdout is not a tty, so this is defence in depth.
- Optionally pin the env (`LC_ALL=C`, drop `SYSTEMD_LOG_LEVEL`/`SYSTEMD_PAGER*`). `SYSTEMD_LOG_LEVEL=debug` turns every run into stderr → unavailable. That is safe but makes the result depend on the environment.

### B9 — Post-kill reap can still hang (D-state under memory pressure) [A2] — tradeoff, document
- Mori's own target condition, memory pressure, is when journalctl is most likely to sit in uninterruptible sleep, where SIGKILL is not delivered until the sleep ends.
- **Correction:** after the kill, `proc.wait(timeout=grace≈2s)`. On expiry, close the fds and return rc2 `timeout` anyway; init reaps the leftover zombie. State the total wall-clock bound as `timeout + grace`.

### B10 — Bounds fixtures can be vacuous for pipes and truncation [A6] — fixable defect, medium
- r14's hang stub is `#!/usr/bin/env python3 … time.sleep(30)`, a single process (`tools/mori-round14-regressions.py:652, 692-694`). A tool that does `proc.kill()` + `communicate()` passes it, so it cannot detect B1/B2.
- **Correction (harness wrappers):**
  - The `timeout:true` wrapper is `/bin/sh` with a non-exec `sleep` child. Sleep only for tool timeout + a few seconds, so any leak is short.
  - The `overflow:true` wrapper writes a **finite** amount (for example `2*max_bytes`), never `yes`-style infinite output. A broken tool then fails as a mismatch instead of exhausting host memory. Optionally apply `RLIMIT_AS` to the tool child (`preexec_fn` or `prlimit`).
  - The harness per-run timeout must strictly exceed tool `--timeout` + grace. Overflow cases pin a small explicit `--max-bytes`.
- **Correction (Bounds.json):**
  1. Newline-aligned overflow: the first `max_bytes` bytes are anchor + one valid positive ending in `\n`, then one more record → rc2 UNAVAILABLE (catches B5).
  2. Exact-limit capture of `max_bytes` bytes → rc0 (catches the off-by-one refusal). This needs a per-case max-bytes field in the shared schema; coordinate with WindowHarness.
  3. Timeout and overflow prefixes contain anchor + a valid positive, so the "no numeric positive totals" check is not vacuous.

## Defect vs tradeoff (for the canonical judge)

- **Must reject if present:** B1, B2, B3, B5, B6, B7.
- **Fixable, lower severity:** B4 (reason stability), B8, B10.
- **Accepted tradeoff, documented:** B9 (the kill cannot guarantee a reap; the tool still returns within the bound). An escaped `setsid` grandchild cannot be killed through the group. The bound is still honoured because the tool does not wait for EOF, but a short-lived orphan sleeper can remain in the harness. Keep wrapper sleeps short.

## Smallest safe correction set

One private bounded-capture function in the tool, which the harness may duplicate but should not import from the CLI (per the spec):
- `Popen(argv, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, close_fds=True, start_new_session=True)`
- a monotonic deadline taken before spawn
- one selector over both raw fds, reading with `os.read`
- a cap of `max_bytes+1` on stdout and presence-only on stderr
- on a bound: assert the pgid, `killpg(SIGKILL)`, bounded `wait`, close the fds, never `communicate()`
- fixed reason priority

Plus: strict ASCII finite CLI bounds with ceilings, and a regular-file, size-capped anchor read.

## Follow-up (IRC)

- MoriR16.PackBounds adopted all three B10 cases: non-vacuous timeout prefixes, a newline-aligned overflow cut with a per-case `max_bytes` → rc2, and an exact-limit capture → rc0.
- `max_bytes` is a new schema field, proposed to WindowHarness.
- Caveat I sent back:
  - `max_bytes` is the UTF-8 byte length of the decoded `stdout` string; keep these cases ASCII-only.
  - The wrapper must write `stdout` byte-for-byte, with no added trailing newline. Otherwise the exact-limit case becomes `max_bytes+1` and flips to rc2.

## Deviation disclosure (per L1 clarification)

- Before L1's clarification arrived I ran these host commands; none touched the target repo:
  - `python3 --version`
  - `journalctl --version`. This only prints the version; no journal query was made and no journal data was read.
  - a `sed`/`grep` read of `/usr/lib/python3.14/subprocess.py`
  - `cat /proc/sys/fs/pipe-max-size`
  - `man journalctl | grep`
  - one in-process `python3 -c` argparse parse: `--timeout nan`, `--max-bytes 1_0`, `int("١٢")`, `float("1e400")`
- I made no journal queries, ran no loops or background jobs, and wrote nothing outside my lane. Messages went only to the seats MoriR16.WindowTool, MoriR16.WindowHarness and MoriR16.PackBounds.
- The argparse parse (B6) and the pipe-size read (B4) are inadmissible as verification. Treat B6 and B4 as unverified claims based on Python/Linux documentation (Python `float()` accepts "nan"/"inf"; `int()` accepts underscores and Unicode decimal digits per PEP 515 and the `int()` docs).
- I reported this to MoriR16.Lesson.
