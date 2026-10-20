# HostSafety — round-16 wave1 (mori-r16-window-build)

Seat: MoriR16.HostSafety (sentinel). Advisory author-lane evidence; this is not outside verification.
Scope: host mutation, pacman, service, and kill scope in the wave spec, the production subprocess argv, and recipe/harness subprocess surfaces. I made no edits and wrote only this report.
Read time: 2026-10-20 05:47–05:58 -03 (wave dispatched at 05:47:55).

## State at read time (explicit)

- `tools/mori-journal-window.py`: **ABSENT**. I could not review the production subprocess code. Findings P1–P5 apply to the spec only. Wave2 (SecurityArgv / FalsifyBounds) must check the delivered bytes.
- `tools/mori-round16-regressions.py`: **ABSENT**.
- Present and read: `wave1-spec.json` (64 items), `wave2-spec.json` (32 items), `capture-recipe.json` (MoriR16.ReceiptCapture), `tools/mori-round16-context-check.py` (partial grep, in flight), 13 fixture packs (Bounds.json and MalformedCapture.json were not yet present).

## Axes

A1 host-mutating journal flags · A2 kill/termination scope · A3 resource bounds/orphans · A4 privilege/executable path · A5 pacman/service/sudo instructions · A6 seat-procedure disclosure.

## Findings

### S1 — Spec instructions (A5): CLEAN
- A static scan of all 64 wave1 and 32 wave2 item prompts found no instruction to run pacman, sudo, systemctl, loginctl, restart, vacuum, rotate, flush, or stress.
- `pacman` appears only in the context pause clause and in ContextGuard's static-check text.
- `kill`/`reap` appears only in WindowTool ("kill/reap only your owned journal child on bound") and in review/critic prompts.
- The L1 clarification (no live journal queries, no probe loops, no background jobs) tightens this further.

### P1 — Interface argv (A1): host-read-only as specified; two LOW gaps
The spec argv is `--cursor=<anchor> --no-tail --quiet --output=json --output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS` plus `--user`/`--system`. Every flag is read-only.

The local `journalctl --help` (systemd 261.2-1-arch) lists these mutating flags, and the spec uses none of them:
- `--vacuum-size/files/time`
- `--sync`, `--flush`, `--rotate`
- `--relinquish-var`
- `--setup-keys`, `--update-catalog`
- `--cursor-file` (man: "At the end, write the cursor of the last entry to FILE")

Gaps:
- **LOW, pager.** `--no-pager` is missing, unlike r15 census parity (`tools/mori-census.sh:1190`). The pager is not an exploit path here because stdout is a pipe, so no pager starts. Smallest fix: add `--no-pager`.
- **LOW, option injection.** The cursor must be passed as the single token `--cursor=<v>`, never with a shell. This rules out option or shell injection even if a cursor begins with `-`. Wave2 should confirm `shell=False` and the single-token form.

### P2 — Kill scope (A2): MEDIUM risk pending code
The precedent pattern, used in r13/r14/r15 harnesses, is `start_new_session=True` + `os.killpg(os.getpgid(proc.pid), 9)` (`mori-round15-regressions.py:1016,1028`).

**Exploit path.** If WindowTool copies `os.killpg(os.getpgid(proc.pid))` without `start_new_session=True`, `getpgid` returns the tool's own group. A timeout would then SIGKILL the tool's whole group. When L1 runs it from a non-interactive shell, that group includes the calling shell or recipe runner. Calling `getpgid` after the child is reaped is a PID-reuse hazard.

**Smallest remediation:**
- Use `start_new_session=True` and `os.killpg(proc.pid, SIGKILL)`.
- Only kill while `proc.returncode is None`, then `wait()`.
- Never use pid ≤ 1, `-1`, `pkill`, or `killall`.

I sent this advice to MoriR16.WindowTool at about 05:51.

### P3 — Orphans and inherited pipes (A3): MEDIUM risk pending harness
- **Timeout wrapper.** If the `timeout:true` wrapper is a shell script that runs `sleep` as a grandchild, killing only the direct child leaves the sleeper holding the stdout write end. The tool then blocks on EOF past its deadline, and an orphan stays on the host.
- **Overflow wrapper.** If `overflow:true` emits an unbounded stream (`yes`, `/dev/zero`), a reader that drains and discards turns it into CPU/IO stress.

**Smallest fix:**
- Timeout wrapper: `exec sleep N`, with N finite and slightly above `--timeout`.
- Overflow wrapper: finite output of max_bytes+1 bytes.
- Tool: group kill (P2) plus concurrent draining of both pipes.

I sent this advice to MoriR16.WindowHarness at about 05:51.

### P4 — Bound parameters (A3): LOW pending code
The spec gives no range for `--timeout` or `--max-bytes`. Accepting 0, negative, NaN, inf, or very large values lets a caller remove the bound entirely or force a huge allocation. Smallest fix: finite >0 values with upper caps, otherwise rc2 `MORI_JOURNAL_WINDOW_SETUP`. The recipe pins 10 s and 8388608 bytes as configured bounds, not measured ones.

### P5 — Executable path and privilege (A4): LOW
`--journalctl PATH` runs any executable. The host has passwordless sudo, so running the tool under sudo would execute that path as root. Under sudo, `--user` would also read root's user journal, not the operator's. The recipe passes `--journalctl /usr/bin/journalctl` explicitly and contains no sudo (`capture-recipe.json:174,204`). Smallest fix: keep recipes sudo-free; optionally refuse euid 0 or record the resolved binary's SHA-256 (recipe S00 already does this).

### P6 — `--quiet` and partial access (trust boundary, not mutation): LOW
man journalctl: `--quiet` suppresses "any warning messages regarding inaccessible system journals when run as a normal user". With partial system-journal access, the result is rc0 with empty stderr, so the stderr-nonempty refusal cannot detect it. This is consistent with the spec's no-completeness claim; the note must not imply full visibility. The recipe's `scope_access_note` already treats unreadable as unavailable only when there is an rc, stderr, or empty stdout.

### R1 — capture-recipe.json (A1/A2/A5): CLEAN at read time
- No sudo, pacman, systemctl, vacuum, rotate, flush, `--cursor-file`, or follow.
- Anchor steps use `-b -n 1 -r --no-pager --quiet -o json --output-fields=__CURSOR,_BOOT_ID`. `/proc/sys/kernel/random/boot_id` is read only.
- Every write is limited to `.ufo/waves/round-16/evidence/live-window`, with noclobber and mode 0600.
- The timeout wrapper is `timeout -k 1` on host `/usr/bin/timeout` (uutils, per the recipe).
  - Upstream uutils `src/uu/timeout/src/platform/unix.rs` runs `setpgid(0,0)` on itself before spawning, then calls `send_signal` / `send_signal_group`. The signal therefore reaches timeout's own new group, not the caller's.
  - [INFERENCE] This reading comes from upstream main, not the installed 0.8.0 bytes, and `send_signal_group` = `kill(0,…)` was not verified from primary source.

### C1 — mori-round16-context-check.py selftest (A3): LOW, in flight
`--selftest` creates `tempfile.mkdtemp(prefix="mori-r16-ctxcheck-")` (line 342). A grep found no `shutil`, `rmtree`, `finally`, or cleanup, so each L1 selftest run would leave a tree in `/tmp`. Smallest fix: `try/finally: shutil.rmtree(root)`. Its child subprocess uses `subprocess.run(..., timeout=60)`, which kills only its own child: owned scope.

### F1 — Fixture packs (13 present): CLEAN for host safety
- No shell metacharacters (`$(`, backtick, `'`, NUL) appear in `stdout`/`stderr`.
- `returncode` values are 0, 5, 124, or 137.
- No `timeout`/`overflow` keys yet, because Bounds.json was not yet present.
- If the harness wrappers are generated from these strings, they must embed them as data (for example a JSON file the wrapper reads), never as interpolated shell source.

## A6 — Procedure disclosure (also sent to MoriR16.Lesson)
Before the L1 clarification I ran:
- `journalctl --version`, `journalctl --help | grep`, `man journalctl | grep` (help text only; no `--user`/`--system` entry read)
- `id -nG`
- `ls`/`date`, and `ls` of `/usr/bin/timeout`
- two file-existence wait loops (bg_2692, bg_2828), both cancelled
- one no-op `sleep 1`
- one failed `curl` of upstream uucore source (404; no file written)

Web reads: uutils `timeout.rs` / `platform/unix.rs`. There were no /tmp writes, no tests, and no live journal query. None of these results count as verification.

Tools installed/updated: none.

## Checks for L1 / wave2
1. Delivered window tool:
   - `shell=False`, `stdin=DEVNULL`, `start_new_session=True`
   - kill limited to `os.killpg(proc.pid, …)` while not yet reaped
   - `--no-pager` present; no mutating flag (P1 list)
   - finite caps on timeout and max-bytes
   - both pipes bounded and drained concurrently
2. Delivered harness: finite timeout/overflow wrappers using `exec sleep`; fixture data never interpolated into shell; explicit `--journalctl` wrapper on every run.
3. Context-check selftest temp cleanup (C1).
