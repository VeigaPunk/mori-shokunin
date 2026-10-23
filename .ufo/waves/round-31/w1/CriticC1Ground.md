# CriticC1Ground — is C1's ground new, and is it in province? (round 31, wave 1)

Seat: MoriR31.CriticC1Ground (critic, leaf). Scope: C1 of `.ufo/waves/round-31/contract.md:28-55`.
Measured 2026-10-22T23:46Z. Lane HEAD `8baccf4a`; entering tip `a12c68ae`. Since the entering tip, only
`corpus/QUALITY.md` and `corpus/knowledge/earlyoom-invocation-scope-r30.md` changed in `corpus/`, `SKILL.md` or
`PROVINCE.md` (`git diff --stat a12c68ae -- corpus SKILL.md PROVINCE.md`), and neither matches the C1 terms.
Tools installed or updated: none.

## Verdict

C1 is **in province**, and its ground is **mostly new depth**. Mori owns watchdog liveness, "pid, start time" included
(`PROVINCE.md:6-7`), and FR5 is the open frontier row on exactly this question (`PROVINCE.md:48`,
`corpus/README.md:338`). None of the 20 sibling `PROVINCE.md` files claims watchdog identity. The only sibling that
touches the question, souji, hands it back: "other uids and host-wide liveness remain mori's ground"
(`../souji-shokunin/PROVINCE.md:141-142`).

Three things already sit in the lane. Each would turn **individual rows** into quality work on held ground if a row only
restated it (§6 item 9, `../.ufo/prompts/mori-round-31.md:361-363`):

- H1: argv-substring false positives.
- H2: the 15-byte `comm` limit.
- H3: PID reuse.

None of them turns the whole claim into held ground. Two of the pre-assigned ids, S166 and S168, re-row URLs the lane
already registers. The C1 counter does not detect that, so it is a provenance risk for the L1 to handle, not a counter
miss. One false claim already held in `SKILL.md`/`PROVINCE.md` (H4) and one missing authority (the watchdog's flock lock,
X2) are the strongest counterexamples.

## Terms searched

The search covered `corpus/` (evidence excluded, then evidence checked separately), `SKILL.md` and `SOURCES.md` at
`a12c68ae`, case-insensitive. Terms: `TASK_COMM`, `PR_SET_NAME`, `pid_max`, `pid reuse`, `start_time`, `starttime`,
`pgrep`, `cmdline`, `/comm` and `comm`.

- No hits at all: `TASK_COMM`, `PR_SET_NAME`, `pid_max`, `starttime`/`start_time` (as a `/proc/<pid>/stat` field),
  zombie `cmdline`.
- `corpus/evidence/**`: the only hits are census logs that contain `pgrep -af shokunin-watchdog` (for example
  `corpus/evidence/round-2/live-before.txt`).
- `corpus/evidence/sources-r30`: no `comm` byte-limit text.

## Overlaps in the lane

| id | held text (path:line) | C1 fact it touches | effect under §6 item 9 |
|---|---|---|---|
| H1 | `corpus/knowledge/audit-r11.md:201` "D06 r2 argv-substring watchdog match \| open false-positive class; `pgrep -af` plus substring filter can count an editor/command merely mentioning the name"; `corpus/knowledge/observability-surfaces-r2.md:105-110` "Match precision is unmeasured-in-production but demonstrated under control: any argv containing the string — e.g. an editor opening `scripts/shokunin-watchdog.sh` — counts"; `:126` keeps the clause open | `pgrep -f` versus name matching | A row whose reading is only "`pgrep -f` counts argv mentions" restates D06 and is **held**. A row that sources *why* (procps `-f` matches the full command line and the default matches the process name, S161/S162) and pins *why the census cannot use name matching* (X1 below) is new. |
| H2 | `corpus/knowledge/oom-victim-selection-r27.md:30` "match the process name only** (`/proc/<pid>/comm`, at most 15 bytes)" | 15-byte name limit | The fact is **held as a statement**. It is sourced only to earlyoom `kill.c:404-427` (S118), not to the kernel, and the round-27 depth move was not counted (`SCORECARD.md:12`). A row that only says "comm ≤ 15 bytes" is quality work on held ground. If the row cites the kernel source (S163 `TASK_COMM_LEN`) and draws the watchdog consequence, it is new. It should cite `oom-victim-selection-r27.md:30` as the prior statement. |
| H3 | `corpus/SOURCES.md:33` S027 pidfd_open(2): "avoids PID reuse ambiguity … persistent handle rather than a one-shot snapshot", status `queued`, used-by `—`; Gate `corpus/lessons/round-12.md:153` | pid reuse | Held **as a queued source row only**: no entry mines it. A pid-reuse row is new depth, but it must cite or acknowledge S027 rather than present PID reuse as first found here. |
| H4 | `SKILL.md:15` (at `a12c68ae`) expected output "`liveness` rows: pid, start time, last tick, state"; `PROVINCE.md:6-7` Owns "watchdog liveness (pid, start time, …)" | start time as identity | This is **false provenance, not held ground**. `probe_watchdog` emits only a pid *count*: `tools/mori-census.sh:705-715` (`pgrep -af`, `pid_n`) and `:852` (`detail="cmd=…; pids=$pid_n; log=…; age_s=…"`), with no start-time field. A C1 `SKILL.md` line stacked next to `:15` could be read as confirming that the census already reports start time. |

## Overlaps outside the lane (read-only)

All 20 sibling `PROVINCE.md` files were searched for `watchdog`, `pgrep`, `daemon identity`, `pid reuse` and
`start.?time`. Hits: souji `:39`, `:43-46` and `:141-142`, plus one unrelated mado `:30`. None in kumitate, tsukuroi or
the others.

| sibling | text (path:line) | owns watchdog identity? |
|---|---|---|
| souji | `PROVINCE.md:43-46`: a residue process needs "fresh (pid, starttime, boot_id) verification (QUALITY Q32)" before reaping; `corpus/knowledge/process-residue-observations.md:46-48`: "Identity binder: `(pid, starttime, boot_id)`. `starttime` is proc stat field 22 (S075) … A pid alone is never identity."; `corpus/SOURCES.md:88,95` S068/S075 `proc_pid_stat(5)` at man-pages **6.19**, field 22 | **No.** This is the same fact for a different purpose (act-time reap checks on souji's own processes), and `:141-142` routes host-wide liveness to mori. C1's S171 (`proc_pid_stat(5)` at 6.20) is fleet-adjacent evidence, not held by this lane, so §6 item 9 ("a rule the lane already holds") does not apply. The entry should cite souji as adjacency, not as first finding. |
| kumitate | `corpus/knowledge/singleton-and-queue-ownership.md:23-27`: "PID existence alone can't distinguish reuse — starttime+bootId bind identity to the lock inode" | **No.** It concerns ufo-fsd-alpha watchdogs (`ufo-l0-watch`, `ufo-stale-watchdog`), under `PROVINCE.md:12` "Origin script layer `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/`". `audit-r11.md:201` routes authoritative daemon identity to "mori with kumitate". Kumitate owns the mechanism; mori owns the observation. |
| tsukuroi | `corpus/knowledge/kill-event-deep-r8.md:216,305,329` use `starttime` ticks for kill-time dating | **No.** OS diagnosis, not watchdog identity. |

## Pre-assigned ids that duplicate registered URLs

These were checked with exact-substring matches against `git show a12c68ae:corpus/SOURCES.md`.

- **S166** Linux v7.2 `fs/proc/base.c` is the same URL as S127 (`SOURCES.md:133`) and S148 (`:154`),
  `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c`. S127/S148 scope is oom_score/oom_score_adj only.
- **S168** Linux v7.2 `Documentation/filesystems/proc.rst` is the same URL as S082 (`:88`), whose scope is "textual
  mountinfo field layout only".
- **No match:** S161-S165, S167 and S169-S173 (`sched.h`, `exec.c`, `binfmt_script.c`, `array.c`, the
  `proc_pid_comm`/`proc_pid_cmdline`/`proc_pid_stat` pages, `PR_SET_NAME`/`prctl`, `admin-guide/sysctl/kernel.rst`,
  pgrep/procps).
- **The counter does not check this.** `count-c1.py:145-161` checks the URL, sha256, quotes, copy and fetch for each id,
  but not whether the URL is new. S166 and S168 can count toward "≥4 distinct new ids" while adding no new upstream file.
  Lane precedent allows a re-row with a new scope (S148 re-rows S127's URL as `supersedes`). The defect is fixable,
  not a must-reject.

## Counterexamples tested

**X1: name matching can never find this watchdog, and the 15-byte limit does not apply to it.** The fleet script starts
with `#!/usr/bin/env bash` (`../scripts/shokunin-watchdog.sh:1`). I ran an identical-shebang script named
`shokunin-watchdog.sh` in my scratch directory, then killed it (`left=0`):

```text
comm=[bash] comm_bytes_incl_nl=5
cmdline=bash <S>/shokunin-watchdog.sh
stat_field2=(bash)
pgrep_default_shokunin-watchdog=0
pgrep_f_path=1
name_len_shokunin-watchdog.sh=20
```

Under this shebang, `comm` is the interpreter's name, so name-mode `pgrep` returns 0 and only `-f` sees the script. The
D06 false-positive class is therefore forced by the shebang, not chosen by the census. A row reading "match the
truncated name `shokunin-watchd`" would be **false** on this host. [INFERENCE] The `comm` comes from the last exec, which
is `env` executing `bash`. S164/S165 must carry the exec-path quote, and this probe does not prove it.

**X2: the driver's own identity authority is missing from the C1 frame.** The watchdog enforces "one driver per fleet
root" with `exec {LOCKFD}>"$UFO/.watchdog.lock"` and `flock -n "$LOCKFD"` (`../scripts/shokunin-watchdog.sh:380-382`,
with `UFO="$SHOKUNIN_ROOT/.ufo"` at `:47`), and lanes close the descriptor (`:207-211`).

- A table limited to "what a pid probe can and cannot establish" never says that the authoritative record is the lock
  holder, not argv.
- A `flock -n` probe would contend for or take the lock. That is a mutation and belongs in a "never" row.
- At 23:46Z, `/home/vgpnk/Projects/shokunin/.ufo/.watchdog.lock` was **absent** (`lock_present=no`). [INFERENCE] Either
  the driver is not running or `SHOKUNIN_ROOT` differs. I did not check which.
- No pre-assigned id names flock(2) or `/proc/locks`. [INFERENCE] `proc.rst` (S168) may describe `/proc/locks`; I did not
  open it.

## Impacted axes

- **Depth (C1's axis):** the claim stays new ground, but rows restating H1 or H2 add nothing.
- **Calibration/honesty:** affected by H4 and by the S166/S168 duplication.
- **Province:** no conflict found. The adjacency entries for souji and kumitate should be cited.

## Smallest safe corrections (for MoriR31; text below is advisory)

1. Rows on `pgrep -f` and on `comm` must state the watchdog consequence (X1) and cite `audit-r11.md:201` and
   `oom-victim-selection-r27.md:30` as prior statements. Count no row that only restates them as new.
2. The S166 and S168 `SOURCES.md` rows name their existing twins in the source or scope cell. Suggested scope text:

```text
same bytes as S127/S148 (oom scope); new scope: proc_pid_cmdline_read / proc_pid_comm / task start time
same bytes as S082 (mountinfo scope); new scope: /proc/<pid>/stat field 22 and comm/cmdline sections
```

   Alternatively, plan the ≥4-id and ≥6-row thresholds without relying on S166 or S168.
3. One table row on the lock (observation: lock file present or absent, and who holds it; verdict: the authoritative
   singleton, not a pid probe; never `flock -n`), sourced to `scripts/shokunin-watchdog.sh:380-382`. Otherwise the entry
   must state in its scope that the lock is out of scope.
4. One entry or `SKILL.md` line records that `SKILL.md:15` and `PROVINCE.md:6-7` name "start time", but
   `tools/mori-census.sh:852` emits no start time. This must not be fixed by editing the census in C1, which C1's surface
   excludes (`contract.md:22-24`).
5. The pid-reuse row acknowledges S027 (`SOURCES.md:33`). The start-time row cites souji's
   `process-residue-observations.md:46-48` and kumitate's `singleton-and-queue-ownership.md:26-27` as adjacency.

## Files opened

- `.ufo/prompts/mori-round-31.md:330-365`
- `mori-shokunin/.ufo/waves/round-31/contract.md`
- `mori-shokunin/PROVINCE.md:1-300`
- `mori-shokunin/SKILL.md:10-30` (at `a12c68ae`)
- `mori-shokunin/corpus/SOURCES.md:5,33,88,133,154` (at `a12c68ae`)
- `mori-shokunin/corpus/knowledge/oom-victim-selection-r27.md:1-50`
- `mori-shokunin/corpus/knowledge/observability-surfaces-r2.md:84-129`
- `mori-shokunin/corpus/knowledge/audit-r11.md:195-205`
- `mori-shokunin/corpus/lessons/round-12.md:153`
- `mori-shokunin/tools/mori-census.sh` (grep lines 705-852)
- `mori-shokunin/.ufo/waves/round-31/count-c1.py` (grep lines 145-161)
- `souji-shokunin/PROVINCE.md:1-12,36-48,138-144`
- `souji-shokunin/corpus/knowledge/process-residue-observations.md:40-50,78-82`
- `souji-shokunin/corpus/SOURCES.md:88,95`
- `kumitate-shokunin/corpus/knowledge/singleton-and-queue-ownership.md:20-30`
- `kumitate-shokunin/PROVINCE.md` and `tsukuroi-shokunin/PROVINCE.md` (grep only)
- `scripts/shokunin-watchdog.sh` (grep lines 1-6, 47, 207-211, 380-382)
- `~/.agents/skills/godspeed/SKILL.md`

Scratch: `/fast/scratch/hyaku/mori-r31/CriticC1Ground/shokunin-watchdog.sh` (probe script; every process it started was
killed).
