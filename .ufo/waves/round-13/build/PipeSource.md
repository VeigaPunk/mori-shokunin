# Scout Report: S031 pipe(7) — Precise SIGPIPE Condition vs pipefail Consequences

**Seat:** `MoriR13.PipeSource`  
**Role:** UFO-FSD scout  
**Axes:** coverage, operability  
**Date:** 2026-10-20  
**Target File:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-13/build/PipeSource.md`  

---

## 1. Tooling Directive Record

In accordance with the operator tooling directive (2026-10-19):
- **Tool installed:** `core/man-pages` (containing upstream Linux system manual pages, section 7)
- **Version:** `6.19-1`
- **Channel:** `sudo pacman -S --needed --noconfirm man-pages`
- **Reason:** Provide local authoritative upstream manual page for `pipe(7)` (`S031`) to inspect exact kernel pipe semantics, signal generation conditions, and buffer constraints without network dependence.

---

## 2. Source S031 Opening & Provenance

- **Source ID:** `S031`
- **Source Reference:** `pipe(7) — overview of pipes and FIFOs`
- **Upstream URL:** `https://man7.org/linux/man-pages/man7/pipe.7.html`
- **Local Artifact:** `man 7 pipe` via `man-pages 6.19` (`Linux man-pages 6.19`, date `2026-07-10`, access date `2026-10-20`)
- **Trio / Provenance Anchor:**
  - Section: `I/O on pipes and FIFOs`
  - Anchor paragraph: Paragraph 5 (`pipe(7):47-56`)
- **Exact Quotes:**
  > "If all file descriptors referring to the read end of a pipe have been closed, then a write(2) will cause a SIGPIPE signal to be generated for the calling process. If the calling process is ignoring this signal, then write(2) fails with the error EPIPE. An application that uses pipe(2) and fork(2) should use suitable close(2) calls to close unnecessary duplicate file descriptors; this ensures that end-of-file and SIGPIPE/EPIPE are delivered when appropriate."
- **Capacity & Buffer Anchors:**
  - Section `Pipe capacity`:
    > "Since Linux 2.6.35, the default pipe capacity is 16 pages (i.e., 65,536 bytes in a system with a page size of 4096 bytes)."
  - Section `PIPE_BUF`:
    > "POSIX.1 says that writes of less than PIPE_BUF bytes must be atomic: the output data is written to the pipe as a contiguous sequence... (On Linux, PIPE_BUF is 4096 bytes.)"
  - Byte-stream nature:
    > "The communication channel provided by a pipe is a byte stream: there is no concept of message boundaries."

---

## 3. Precise SIGPIPE Condition vs pipefail Consequences

### 3.1 Precise Kernel Condition for SIGPIPE
Under Linux and POSIX (`pipe(7)`):
1. **Trigger Condition:** A process issues a `write(2)` syscall against a file descriptor referring to the write end of a pipe (or FIFO) when **all file descriptors referring to the read end of that pipe have been closed across all processes**.
2. **Signal Generation:** The kernel immediately generates signal `SIGPIPE` (signal number 13) for the calling/writing process.
3. **Default Action:** Abnormal termination of the writing process with exit code `128 + 13 = 141`.
4. **Ignored/Handled Behavior:** If the process ignores `SIGPIPE` (`SIG_IGN`) or handles it, the `write(2)` call returns `-1` with `errno` set to `EPIPE`.
5. **Buffer Dynamics:** When a reader process exits early, any unread data remaining in the pipe buffer does not immediately cause `SIGPIPE`. The signal is generated only when an active writer attempts a subsequent `write(2)` that requires delivery across a pipe with zero remaining readers. Because producers such as `printf` or `sed` emit output line-by-line or in discrete chunks, writes issued after the consumer has terminated and closed its standard input trigger `SIGPIPE`.

### 3.2 Shell Pipeline Consequence under `pipefail`
1. **Default Pipeline Return Code (no `pipefail`):**
   In standard POSIX shell execution, the exit status of a pipeline (`cmd1 | cmd2 | cmd3`) is simply the exit status of the **last (rightmost)** command (`cmd3`). If `cmd3` exits `0`, the pipeline status is `0`, even if `cmd1` or `cmd2` was terminated by `SIGPIPE` (rc 141).
2. **`set -o pipefail` / `set -euo pipefail`:**
   Bash's `pipefail` option modifies this contract: the return status of a pipeline is the exit status of the **last (rightmost) command to exit with a non-zero status**, or `0` if all commands exit successfully.
3. **The Conflict:**
   - An early-exiting consumer (`grep -q`, `grep -Fxq`, `head -n N`, `grep -m1`) exits `0` as soon as its matching condition is satisfied.
   - Upon exiting, the consumer closes its standard input (the pipe's read end).
   - An upstream producer (`printf`, `sed`, etc.) still processing data attempts to write the next line or buffer chunk into the pipe.
   - The kernel raises `SIGPIPE`; the producer is terminated with status `141`.
   - Under `pipefail`, because `141 ≠ 0`, bash records `PIPESTATUS[producer]=141` and `PIPESTATUS[consumer]=0`. The overall pipeline return status becomes `141`.
4. **Semantic Inversion:**
   - Under `if producer | early_exit_consumer; then ...; else ...; fi`, the pipeline status `141` causes the shell to treat the test as **FALSE**.
   - Under `producer | early_exit_consumer || fallback`, the fallback executes even though the pattern matched.
   - Thus, a successful match is converted into a reported failure purely because the producer did not finish before the reader exited.

---

## 4. Operational Context in Mori: F01 vs r9 Flake

### 4.1 Production Authorship Loss Defect F01 (`tools/mori-census.sh:1494`)
- **Location:** `tools/mori-census.sh:1494` in `grade_lane()`
- **Pipeline:**
  ```bash
  if printf '%s\n' "$inwin" | sed -E 's/^[0-9]+ //' | grep -Fxq -- "$lane-shokunin <$lane@shokunin.local>"; then
    subj=1
  else
    sib=1
  fi
  ```
- **Shell Options:** `set -euo pipefail` (line 236).
- **Exact Defect Mechanism:**
  1. The variable `$inwin` contains the commit history in the launch window.
  2. If the lane author made an early commit in the window, followed by a large history of sibling commits (e.g., 12,000 sibling commits as in `corpus/knowledge/audit-r11.md:308-370` Appendix B):
  3. `grep -Fxq` finds the matching subject author line on the first line and immediately exits `0`.
  4. Exiting closes `grep`'s standard input (the pipe from `sed`).
  5. `sed` is still reading lines from `printf` and attempting to write transformed lines into the pipe.
  6. As soon as `sed` writes to the closed pipe, the kernel sends `SIGPIPE` to `sed`.
  7. `sed` exits `141`.
  8. Under `pipefail`, the pipeline status is `141` (measured: `PIPESTATUS = [141, 141, 0]`).
  9. The `if` condition evaluates to false, jumping to `else`.
  10. `subj=1` is bypassed; `sib=1` is set.
  11. The lane is wrongly graded as `progressing-weak` (sibling-only, `basis=row-C other_authored_commits=12001`) or `silence`, causing complete loss of genuine subject authorship.

### 4.2 Contrast with r9 Selftest Flake
- In round 9 (`corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md`, `corpus/knowledge/selftest-flake-r9.md`), selftest assertion sites used `printf '%s\n' "$out" | grep -qE -- "$re" || miss=...`.
- In round 9, the selftest harness was repaired by grepping a temporary capture file (`OUT_FILE`).
- However, the production silence pipeline at line 1494 (then line 1322) was explicitly left untouched due to round-9 scope constraints, carrying over as open defect F01 (item D01 in `audit-r11.md`).

---

## 5. Architectural Recommendations for CensusFix (`tools/mori-census.sh`)

In accordance with **Criterion 7 of `corpus/QUALITY.md`**:
> *"No live producer pipe feeds a match test; capture once and assert over the captured bytes (SIGPIPE 141 ≠ 1)."*

To repair F01 without introducing SIGPIPE races:
1. **Capture once / Here-string approach:**
   Extract and strip authors into a shell variable or temporary capture buffer once, then match against the captured text without a live multi-stage pipeline:
   ```bash
   authors=$(printf '%s\n' "$inwin" | sed -E 's/^[0-9]+ //')
   if grep -Fxq -- "$lane-shokunin <$lane@shokunin.local>" <<< "$authors"; then
     subj=1
   else
     sib=1
   fi
   ```
   With a here-string (`<<< "$authors"`), `grep -Fxq` reads from an already-buffered file descriptor (temporary file or memory descriptor created by the shell). When `grep` exits `0`, there is no active producer process to receive `SIGPIPE`. The exit code of `grep` is directly the exit code of the test command.
2. **Single-pass filter (no early exit):**
   Alternatively, parse `$inwin` in a single utility (e.g. `awk`) that scans the input and exits with a dedicated code without pipe chaining.

---

## 6. Sourced Findings Summary

| Dimension | Observed Fact | Source / Anchor |
|:---|:---|:---|
| **S031 Identity** | `pipe(7)` Linux man-pages 6.19 (2026-07-10) | `man 7 pipe`, S031 URL `https://man7.org/linux/man-pages/man7/pipe.7.html` |
| **SIGPIPE Condition** | `write(2)` when all read ends are closed generates `SIGPIPE` (or `EPIPE` if ignored) | `pipe(7):47-56` (Section *I/O on pipes and FIFOs*) |
| **Pipe Capacity** | 16 pages default (64 KiB), `PIPE_BUF` 4096 bytes atomic | `pipe(7)` Sections *Pipe capacity* & *PIPE_BUF* |
| **pipefail Behavior** | Pipeline exit status is rightmost non-zero status | Bash reference manual / POSIX; verified `PIPESTATUS=[141, 141, 0]` |
| **F01 Site** | `tools/mori-census.sh:1494` (`printf \| sed \| grep -Fxq` under `set -euo pipefail`) | `tools/mori-census.sh:1494`, `corpus/knowledge/audit-r11.md:156,308-370` |
| **F01 Effect** | `grep -Fxq` match causes `sed` SIGPIPE (141); `if` takes `else`, misgrading subject as weak | `corpus/knowledge/audit-r11.md:364-370` Appendix B reproduction |
| **Remediation Rule** | Quality criterion 7: capture once, match over captured bytes | `corpus/QUALITY.md:13-14`, `corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md` |

---

## 7. Status & Remaining Unknowns
- **Confidence:** High (direct upstream documentation verified on system via `man-pages 6.19`, reproducible bash execution verified, defect F01 anchored at lines 1490-1497 of `tools/mori-census.sh`).
- **Remaining Unknowns:** None for the SIGPIPE condition, `pipefail` semantics, or S031 citations.
- **Verification Note:** As a leaf scout in round 13, no test suites, builds, or lint runs were executed; findings are delivered for `CensusFix`, `HistoryKnowledge`, and `RegressionHarness`.
