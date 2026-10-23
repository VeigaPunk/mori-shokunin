# Wave 1 — LiveCommProbe: how a `#!` script's task name is set and what pgrep sees

Seat: MoriR31.LiveCommProbe (leaf, executor). Date: 2026-10-22. Scope: measurement only on this
host, throwaway processes only; no lane files besides this report; no installs performed (none
needed — tooling directive satisfied with zero changes).

## Environment and method

Facts (all from scratch log `/fast/scratch/hyaku/mori-r31/LiveCommProbe/redacted.log`, cited as RL:n):

- kernel `7.2.11-arch1-1` (RL:2-3); interpreters that ran the probes: GNU bash `5.3.20(1)-release` (RL:4-5).
- `/usr/bin/pgrep` is `pgrep from procps-ng 4.0.7` (RL:13-14, binary RL:11-12); inside the runner
  `command -v pgrep` resolves to `/usr/bin/pgrep` (RL:15-16) — no builtin shadowing observed.
- `/bin/bash` → `/usr/bin/bash`; `/usr/bin/env` → `/usr/bin/env` (RL:17-19).

Two scripts were created in `/fast/scratch/hyaku/mori-r31/LiveCommProbe/` (assignment names one
script but requires two shebangs, so the copy needed its own name):

```sh
shokunin-watchdog-probe.sh    # 29 bytes, first line: #!/usr/bin/env bash
shokunin-watchdog-probe-b.sh  # 21 bytes, first line: #!/bin/bash
```

both body `sleep 60`, both `chmod +x` (RL:20-25). Three launches, each as its own `setsid`
process group so the whole tree could be signalled by pgid:

1. `setsid timeout 90 ./shokunin-watchdog-probe.sh &`   (env shebang) → `<wrapper-env-shebang>`
2. `setsid timeout 90 ./shokunin-watchdog-probe-b.sh &` (bin shebang) → `<wrapper-bin-shebang>`
3. `setsid timeout 90 bash ./shokunin-watchdog-probe.sh &` (interpreter-first) → `<wrapper-interpreter-first>`

Pgid-each-launch (RL:26-27). All reads taken ~2 s after launch. Every pgrep invocation used the
absolute path `/usr/bin/pgrep` and ran from a runner script whose own cmdline does not contain the
pattern, so `-f` output shows only real matches, not the measuring shell. Second run
(`redacted2.log`, cited as R2:n) isolates `-a` from `-f`.

## Observations, per command

### A. /proc reads of the three script processes (RL:28-52)

| launch | `/proc/<pid>/comm` | cmdline (`tr '\0' ' '`) | stat field 22 | `readlink exe` | source |
|---|---|---|---|---|---|
| env shebang | `bash` | `bash ./shokunin-watchdog-probe.sh` | 5720216 | `/usr/bin/bash` | RL:32-35 |
| bin shebang | `shokunin-watchd` | `/bin/bash ./shokunin-watchdog-probe-b.sh` | 5720216 | `/usr/bin/bash` | RL:40-43 |
| `bash <script>` | `bash` | `bash ./shokunin-watchdog-probe.sh` | 5720216 | `/usr/bin/bash` | RL:48-51 |

The `timeout` wrappers read as expected: comm `timeout`, cmdline `timeout 90 ./shokunin-watchdog-probe.sh` etc. (RL:30-31, 38-39, 46-47). Each script process had one child, comm `sleep`, cmdline `sleep 60` (RL:36, 44, 52).

### B. The four assigned pgrep commands (RL:53-75)

```
$ /usr/bin/pgrep shokunin-watchdog-probe; echo $?
pgrep: pattern that searches for process name longer than 15 characters will result in zero matches
Try `pgrep -f' option to match against the complete command line.
exit=1
```
(RL:54-57) — six live processes whose cmdline contains the pattern, zero matches without `-f`.

```
$ /usr/bin/pgrep -f shokunin-watchdog-probe; echo $?
<wrapper-env-shebang> <wrapper-bin-shebang> <wrapper-interpreter-first>
<script-env-shebang> <script-bin-shebang> <script-interpreter-first>
exit=0
```
(RL:58-65, all six pids) — with `-f`, both the wrappers and the script interpreters match.

```
$ /usr/bin/pgrep -x shokunin-watch; echo $?
exit=1
```
(RL:66-67) — the plausible 14-char prefix is NOT comm; no match.

```
$ /usr/bin/pgrep -af shokunin-watchdog-probe
<wrapper-env-shebang> timeout 90 ./shokunin-watchdog-probe.sh
<wrapper-bin-shebang> timeout 90 ./shokunin-watchdog-probe-b.sh
<wrapper-interpreter-first> timeout 90 bash ./shokunin-watchdog-probe.sh
<script-env-shebang> bash ./shokunin-watchdog-probe.sh
<script-bin-shebang> /bin/bash ./shokunin-watchdog-probe-b.sh
<script-interpreter-first> bash ./shokunin-watchdog-probe.sh
exit=0
```
(RL:68-75). Self-exclusion: pgrep's own process, whose cmdline contains the pattern text, is not
listed. Demonstrated directly: `/usr/bin/pgrep -af probe-run` matched the runner shell (`bash
probe-run.sh`) but not the pgrep process itself, exit=0 (RL:91-93); pgrep(1) states "The running
pgrep, pkill, or pidwait process will never report itself as a match" (`zcat
/usr/share/man/man1/pgrep.1.gz | sed -n '317,325p'`).

### C. Extra probes pinning the truncation length (RL:76-90)

- `/usr/bin/pgrep -d, shokunin-watchd` → `<script-bin-shebang>`, exit=0 (RL:77-79): comm regex of
  the 15-char truncated name matches.
- `/usr/bin/pgrep -x shokunin-watchd` → `<script-bin-shebang>`, exit=0 (RL:80-82): exact comm is
  exactly `shokunin-watchd`, 15 bytes, hard stop mid-word before the `o` of `dog`.
- `/usr/bin/pgrep -af shokunin-watch` listed all six (RL:83-90) — this is `-f` matching (`-a`
  does not change matching, see D), so it is a `-f` datum, not a comm datum.
- comm-based matching sees ONLY the bin-shebang script: neither env-shebang nor
  interpreter-first appears at RL:77-82, because their comm is `bash`.

### D. Discriminator: `-a` alone does not switch to cmdline matching (R2:5-18)

Against one live env-shebang instance (comm `bash`, R2:2-4):

```
$ /usr/bin/pgrep shokunin-watchd; echo $?    exit=1   # comm matching, no match
$ /usr/bin/pgrep -a shokunin-watchd; echo $? exit=1   # -a WITHOUT -f: still no match
$ /usr/bin/pgrep -f shokunin-watchd; echo $?
<wrapper2> <script2>
exit=0
```
(R2:6-13). And `/usr/bin/pgrep -a sleep` (no `-f`) matched sleeps by comm and merely printed their
full cmdlines, including the run's own not-yet-killed `sleep 60` (R2:14-18) — `-a` is display-only.
pgrep(1) confirms: "-a, --list-full: List the full command line as well as the process ID."
(`zcat /usr/share/man/man1/pgrep.1.gz | sed -n '71,74p'`); "-f, --full: The pattern is normally
only matched against the process name. When -f is set, the full command line is used." (`sed -n
'105,108p'` of the same).

### E. Installed man-page corroboration (procps-ng 4.0.7, the version running here)

NOTES: "The process name used for matching is limited to the 15 characters present in the output
of /proc/pid/stat. Use the -f option to match against the complete command line,
/proc/pid/cmdline." (R2:20-27, from `/usr/share/man/man1/pgrep.1.gz` lines 313-316; also
`man-extracts.txt:21-27` in the same scratch dir). EXIT STATUS: 0 "One or more processes matched
the criteria", 1 "No processes matched or none of them could be signalled" (`zcat
/usr/share/man/man1/pgrep.1.gz | sed -n '294,306p'`). These are host-installed bytes of the same
upstream file pre-assigned as S161 (procps-ng v4.0.7 man/pgrep.1); the S161 Gate row still needs
the fresh URL fetch by its owner.

## Mapping to the C1 decision-table rows

| decision-table row | verdict supported by this measurement |
|---|---|
| name truncation at 15 bytes | comm of the direct-`#!` script is `shokunin-watchd`, exactly 15 bytes, cut mid-word (RL:40); `-x shokunin-watchd` exit=0 vs `-x shokunin-watch` exit=1 (RL:66-67, 80-82); pgrep warns verbatim about >15-char name patterns (RL:55-56); pgrep(1) NOTES quote (R2:23-26). A watchdog check must target `shokunin-watchd`, not `shokunin-watchdog`. |
| interpreter vs script name | comm is the script name only when the kernel execs the script directly (bin shebang, RL:40). With `#!/usr/bin/env bash` the extra exec of bash by env overwrites comm with `bash` (RL:32); interpreter-first is `bash` too (RL:48). Same split in cmdline argv[0]: `/bin/bash` vs `bash` (RL:33, 41). An env-shebang script is invisible to comm-based pgrep: `pgrep shokunin-watchd` exit=1 while it ran (R2:6-9) though `-f` found it (R2:10-13). |
| exe path of a script | `/proc/<pid>/exe` of a script-running bash is the interpreter `/usr/bin/bash` in all three launches (RL:35, 43, 51), never the script path. exe-based liveness cannot distinguish this script from any other bash. |
| pgrep with and without -f | without `-f`: comm only, zero matches + warning for a 23-char pattern (RL:54-57). With `-f`: full cmdline, all 6 pids (RL:58-65). `-a` only changes output, not matching (R2:6-18) — so run-1 `-af` listings (RL:68-75, 83-90) are `-f` behavior. Corollary: plain `pgrep shokunin-watchdog` would also fail (17-char pattern vs 15-byte comm); only `-x shokunin-watchd`, `pgrep shokunin-watchd`, or `-f` forms can find a direct-`#!` instance. |
| exit codes | 0 iff ≥1 match, 1 iff none: observed 1 (RL:57, 67), 0 (RL:65, 75, 79, 82, 90, 93), matching pgrep(1) EXIT STATUS 0/1 text quoted above. |
| (corroboration) field 22 | stat field 22 is starttime in clock ticks: 5720216 for all three script processes (RL:34, 42, 50) — three distinct instances (different comm/cmdline) observed live in the same start tick; consistent pid→comm mapping at read time [INFERENCE: tick granularity ≈ USER_HZ=100]. |

## Cleanup evidence

Run 1: TERM sent to the three pgids (RL:94-95); then `/usr/bin/pgrep -f
shokunin-watchdog-probe` exit=1 (RL:97-98) and `/usr/bin/pgrep -x shokunin-watchd` exit=1
(RL:99-100) — no probe process remains. Run 2: group TERMed, `pgrep -f
shokunin-watchdog-probe` exit=1 (R2:28-31). The only sleeps visible afterwards belong to other
seats (cmdline `sleep 55`, and one in run 1 redacted as `<sleep-foreign-run1>`): read-looked only,
never signalled (RL:101-103, R2:32-34). My own run-2 `sleep 60` is visible pre-cleanup at R2:17
and gone after the group TERM. No process started by this probe outlived its runner; all runner
calls were wrapped in `timeout` ≤ 70 s; the long-lived probes themselves ran under `timeout 90`.

## Files

- Report (this file): `.ufo/waves/round-31/w1/LiveCommProbe.md` — only lane file written.
- Scratch (retained evidence, pids redacted at capture): `/fast/scratch/hyaku/mori-r31/LiveCommProbe/{redacted.log,redacted2.log,man-extracts.txt,probe-run.sh,probe-run2.sh,shokunin-watchdog-probe.sh,shokunin-watchdog-probe-b.sh}`. Raw unredacted intermediates were scrubbed after redaction; every pid in these files is a `<label>` placeholder (starttime tick values are clock ticks, not pids).

## Risks / limits

- Single-shot measurement per variant; conclusions are per procps-ng 4.0.7 + kernel 7.2.11 as installed here, and man-page text of the same pgrep version; kernel-side mechanism (why env rewrites comm) is for the S163-S167 source seats, not measured here.
- `<wrapper-*>`/`<script-*>`/`<sleep-*>` stand for distinct real pids; the three field-22 values being equal is expected for near-simultaneous launches [INFERENCE on tick alignment].
- S161 correspondence is to the installed binary's man page, not a fresh upstream fetch; the Gate row for S161 must come from the seat that fetches the URL bytes.
