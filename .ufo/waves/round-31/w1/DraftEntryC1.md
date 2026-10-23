# DraftEntryC1 — C1 watchdog identity

## Behavior and findings

Prepared a draft decision table distinguishing a text or task-name match from a process identity and from liveness of a held pidfd. The draft has the required front matter, the FR5 detection-and-report-only scope paragraph, one table with the exact requested header and 13 data rows, then `## Limits` and `## Not claimed`. The pgrep and procfs readings are tied to the pinned source IDs below. The table marks combined interpretation as `[INFERENCE]`.

The census probe at `tools/mori-census.sh:703-730` runs `pgrep -af shokunin-watchdog`, filters output lines, and emits `watchdog unavailable` plus “liveness UNKNOWN, not absent” if pgrep is unavailable (`tools/mori-census.sh:710-720`). The draft does not turn a string match into a watchdog identity claim.
The subsequently read wave-1 probe report records a measured argv false positive, a `pgrep`-substring false negative, a `PR_SET_NAME` comm spoof, pid/starttime distinction, self-stage matching, and line-count inflation (`.ufo/waves/round-31/w1/LiveArgvProbe.md:28-149`). These are MoriR31.LiveArgvProbe's results, not probes run by this seat.

## Gates and limits

- Draft content addresses C1's entry shape and source citations, but C1 is **not claimed met**. No lane entry, SOURCES rows, Gate rows, evidence copies, or SKILL.md lines were written by this seat; the frozen counter was not run. Contract requirements are at `.ufo/waves/round-31/contract.md:28-54`.
- No build, test, lint, format, or product check was run. L1 owns integration and verification.
- The four initially attempted man-pages URLs without the repository's `man/` directory component returned HTTP 404 (`curl` exit 22); the corrected official tagged paths returned HTTP 200. The draft cites only the corrected downloads. Per-request UTC time was captured for the corrected batch (`2026-10-22T23:46:06Z`); it was not captured in the initial parallel batch.
- Locator discrepancy closed: MoriR31.LiveArgvProbe initially reported, “`cap "$PGREP_BIN" -af shokunin-watchdog` is :710, the `pids=$(... grep -E ... | grep -vF 'pgrep' ...)` line is :712, `pid_n=$(... grep -c .)` is :714.” The peer then withdrew those numbers and updated its report to grep-verified :711/:713/:715 (`.ufo/waves/round-31/w1/LiveArgvProbe.md:11-15`), matching my direct read of `tools/mori-census.sh:703-730`.
- No tool was installed or updated. No git or jj command was run. No process tree was started beyond bounded curl/hash commands; no unit was started, stopped, or signalled.

## Touched surfaces and artifacts

- Draft saved at `/fast/scratch/hyaku/mori-r31/DraftEntryC1/watchdog-identity-r31.md`; it was updated after the initial save to incorporate wave-1 probe observations.
- This report is the only lane file written: `.ufo/waves/round-31/w1/DraftEntryC1.md`.
- Source bytes were fetched only beneath `/fast/scratch/hyaku/mori-r31/DraftEntryC1/sources/`. S168 was fetched but is not cited in the draft. The failed initial man-pages fetches are not cited.
- No product code, source registry, lessons, upstream evidence copies, or skill files were edited.

## Source provenance and line checks

Initial batch command form (each command had the same bounded wrapper and per-source URL/output path):

```sh
timeout 45s bash -c 'ulimit -v 262144; curl -fLsS --max-time 35 --max-filesize 5000000 <URL> -o <scratch-file> && printf "<ID> curl=0 bytes=" && wc -c < <scratch-file>'
```

The command outputs were `curl=0` with these full-byte sizes; `sha256sum` was run at `2026-10-22T23:45:30Z` (the timestamp was printed by that command):

- S161 `https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/man/pgrep.1` → 9,702 bytes; SHA-256 `c2024c384dd88df2a4d5093d4726e57f38c5fee378dc7ed4c99c70c2f6341e35`. Verified `-f`/full-command-line at saved bytes `sources/S161.src:103-108`, exit meanings at `:294-311`, and 15-character process-name limit at `:313-316`.
- S162 `https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/src/pgrep.c` → 45,309 bytes; SHA-256 `af711983209fa083eef970f045104397b0d1406b9aacad2be0747e966e584e16`. Verified selection of `CMDLINE` versus `CMD` and regex matching at `sources/S162.src:908-916`, and the long-name warning at `:962-965`.
- S163 `https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/sched.h` → 73,653 bytes; SHA-256 `a31c63e692cb8ab036d01c0092fcdf4dfb75ec1f17dfda9056b12abecdb3dedf`. `TASK_COMM_LEN = 16` at `sources/S163.src:324-326`.
- S164 `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/exec.c` → 51,001 bytes; SHA-256 `44e4185bf9332d86a2fd6bbe33c22cdd0b5129521499b703058813d2106572c7`. `__set_task_comm` truncation at `sources/S164.src:1094-1101`; exec name source at `:1243-1258`.
- S165 `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/binfmt_script.c` → 4,358 bytes; SHA-256 `81b0293a89908d56575f2b00b3550f927eb80714ef540f9634272bce56f9c656`. Interpreter and script argument order at `sources/S165.src:97-106`.
- S166 `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c` → 98,196 bytes; SHA-256 `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6`. Cmdline zero-byte cases at `sources/S166.src:285-302`; setproctitle argument-area handling at `:304-334`.
- S167 `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/array.c` → 23,110 bytes; SHA-256 `a3eb1567e6125bd9c3136efacf1e6ee7526deb4212a895f3c3156d2410985828`. Start-time derivation and stat output at `sources/S167.src:584-612`.
- S027 `https://man7.org/linux/man-pages/man2/pidfd_open.2.html` → 18,141 bytes; SHA-256 `d34301a2f18869b774ad5c5dc3ef0e93988b903deb13bdc41cbbd60bce9c5bab`. Nonblocking `EAGAIN` at `sources/S027.html:92-96`; poll readability and hangup at `:171-177`.

Corrected man-pages batch command form (the command printed UTC immediately before curl):

```sh
timeout 40s bash -c 'ulimit -v 262144; printf "access="; date -u +%Y-%m-%dT%H:%M:%SZ; curl -sSL --fail -m 30 -o <scratch-file> -w "HTTP:%{http_code} SIZE:%{size_download}\\n" "<URL>"'
```

All four corrected downloads reported `access=2026-10-22T23:46:06Z`, HTTP 200:

- S169 `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_comm.5?h=man-pages-6.20` → 1,347 bytes; SHA-256 `31aee9e50c23579e7983e26edee83bee9ab7a8ba4c7be46027db2cac5ee23c08`. Per-thread names, mutation, and truncation: `sources/S169.correct.src:17-41`.
- S170 `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_cmdline.5?h=man-pages-6.20` → 1,557 bytes; SHA-256 `a9f3b83b1b0442319d0a8a5be23787c8024bc485dd54a062da9c37d57733f111`. Empty zombie cmdline and process-controlled argument strings: `sources/S170.correct.src:13-47`.
- S171 `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_stat.5?h=man-pages-6.20` → 11,350 bytes; SHA-256 `cba82e47c8c7917ec4f7c24d9c8779c53ecf478fdefe5c7835690989bb060bcd`. Field 22 and tick units: `sources/S171.correct.src:227-231`.
- S172 `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man2const/PR_SET_NAME.2const?h=man-pages-6.20` → 1,889 bytes; SHA-256 `f2ac57cc826943dcd5bc71feea9859099014bc59767b21eafad44a7325be558a`. Calling-thread name and 16-byte truncation: `sources/S172.correct.src:26-35`.

The S169-S172 fetches first attempted the context's shorter `plain/man5/...` or `plain/man2/...` paths; each returned HTTP 404. The successful URLs above include the actual repository path components `man/man5/` or `man/man2const/`. S027 and S161-S168 initial fetch results were `curl=0`; S168 (`https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst`) was 107,560 bytes with SHA-256 `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` and is unused.

## Draft pasted for L1

```markdown
source: S027, S161, S162, S163, S164, S165, S166, S167, S169, S170, S171, S172
verified-at: 2026-10-22 (round 31, procps-ng 4.0.7, Linux 7.2.11)
recheck: on procps-ng or kernel release

FR5 scope: detection and report only. `tools/mori-census.sh:703-730` runs `pgrep -af shokunin-watchdog`, filters matching output text, and emits an unavailable finding when pgrep is missing; a matching string is a candidate, not a process-identity proof.

| observation | reading | verdict | sources |
|---|---|---|---|
| `pgrep -f -a` includes an argv decoy and the census grep-stage line containing `shokunin-watchdog` | `-f` matches the full command line, so a `sleep` process whose argv merely mentions the name is a candidate. The census filters the target text, removes only lines containing `pgrep`, then counts lines (`tools/mori-census.sh:711-715`); a wave-1 run measured its own `grep -E` stage surviving alongside a decoy (`.ufo/waves/round-31/w1/LiveArgvProbe.md:28-58, 143-149`). [INFERENCE] | alive-unconfirmed | S161, S162, S170 |
| `pgrep` without `-f` searches with a pattern longer than 15 bytes and returns no match | The default process-name match is limited to 15 characters; procps warns that a longer name pattern yields zero matches. This miss is a pattern-limit result, not evidence of absence. | not-identity | S161, S162 |
| `/proc/<pid>/comm` equals the 15-byte prefix of the watchdog script basename | `comm` has a 16-byte limit including NUL and overlong values are silently truncated. Prefix equality cannot establish the full name or executable. [INFERENCE] | not-identity | S163, S164, S169 |
| A thread sets `comm` to the 15-byte truncated watchdog name via `PR_SET_NAME` | The call sets the caller's thread name from supplied bytes and truncates over 16 total; the wave-1 probe observed `pgrep -x` match a comm-forged `shokunin-watchd` process while its cmdline stayed `python3` and the census `-af` pipeline yielded none (`.ufo/waves/round-31/w1/LiveArgvProbe.md:89-119`). [INFERENCE] | not-identity | S161, S163, S169, S172 |
| `/proc/<pid>/cmdline` is empty | A zombie has an empty cmdline; the kernel also returns zero bytes when the argument range is absent or empty. No cmdline bytes means the probe cannot identify the process from that file. | unavailable | S166, S170 |
| `/proc/<pid>/cmdline` contains the watchdog script path after a shebang interpreter name | The script loader puts the interpreter in `argv[0]` and the script filename later in the argument vector. A path match therefore does not establish which script logic is active or healthy. [INFERENCE] | alive-unconfirmed | S165, S170 |
| `/proc/<pid>/stat` field 22 differs from the saved start-time token for that PID | Field 22 is process start time after boot in clock ticks; Linux emits a value derived from the task start time. In the same boot and time namespace, a mismatch means this sample does not match the saved start-time token. [INFERENCE] | not-identity | S167, S171 |
| A candidate's full command line contains both `shokunin-watchdog` and the substring `pgrep` | The census runs `grep -vF 'pgrep'` after the match, removing the candidate line (`tools/mori-census.sh:713`); a wave-1 probe measured one candidate after stage 2 and zero after stage 3 (`.ufo/waves/round-31/w1/LiveArgvProbe.md:60-87`). A missing final line is not absence under this filter. [INFERENCE] | alive-unconfirmed | S161, S162, S170 |
| `pgrep` exits 1 | procps defines this as no processes matched the criteria. Verdict is absent only for this completed query; it does not prove global watchdog absence if the query can miss a name or its command line changed. [INFERENCE] | absent | S161, S170 |
| `pgrep` exits 2 or 3 | Exit 2 is a command-line syntax error; exit 3 is a fatal error such as out of memory. Neither is a no-match result. | unavailable | S161 |
| A pid file contains a number and `/proc/<pid>/stat` can be read | `pgrep -F` reads PIDs from a file; a numeric PID and a proc record do not establish that the task is the watchdog or the same task previously recorded. [INFERENCE] | not-identity | S027, S161, S171 |
| A held, nonblocking pidfd for an independently identified watchdog task yields `EAGAIN` from `waitid` | For `PIDFD_NONBLOCK`, `EAGAIN` means the referenced task has not yet terminated. This establishes task liveness at the sample only if the handle was already bound to the watchdog. | alive | S027 |
| A held pidfd becomes poll-readable (`EPOLLIN`) | The task referred to by that pidfd has terminated and become a zombie; after reaping, polling reports hangup. This is about that task, not a later task reusing its numeric PID. | absent | S027 |

## Limits

- `pgrep -f` searches command-line text; `/proc/<pid>/cmdline` reflects argument strings the process wants observed and those strings can be changed (S161, S170).
- The census's `grep -vF 'pgrep'` stage drops otherwise matching command lines containing that substring, and its `grep -c .` counts surviving lines rather than unique processes (`tools/mori-census.sh:713-715`; measured examples at `.ufo/waves/round-31/w1/LiveArgvProbe.md:60-87, 143-149`). [INFERENCE]
- `comm` is per-thread, can be changed by a thread, and is silently truncated to 15 visible bytes (S163, S169, S172).
- Compare `stat` start-time tokens only within the same boot and time-namespace view; a matching token alone is not a durable task handle (S167, S171, S027). [INFERENCE]
- A pidfd supports stable observation only while that descriptor is held; opening one from a bare PID does not retroactively authenticate a stale pid file (S027). [INFERENCE]
- If pgrep is missing, the census code reports `watchdog unavailable` and says liveness is unknown, not absent (`tools/mori-census.sh:710-720`).

## Not claimed

- A matching `pgrep` line, `comm`, script path, or numeric PID proves the task is the fleet watchdog.
- A process-name or command-line match proves the watchdog loop is executing correctly, healthy, supervised by a particular unit, or able to complete its work.
- A pidfd reports the process's role or health; it identifies a task for liveness observation only.
- One `pgrep` query establishes fleet-wide process visibility or proves absence outside the query's searchable view. [INFERENCE]
- This entry prescribes no start, stop, restart, signal, or remediation action.
```
