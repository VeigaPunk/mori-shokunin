---
name: mori-shokunin
description: "Fleet & host observability (森) — detect and report fleet liveness, wave settlement, kill/OOM events and resource runway. Triggers: 'fleet health', 'did a wave die', 'why did the daemon vanish', 'watchdog liveness', 'OOM kill'. Anti-trigger: NOT dispatch/orchestration (kumitate), NOT OS package/systemd/driver state (tsukuroi), NOT endpoint health (kama). Rank: shonen."
---

# mori-shokunin — fleet & host observability (森)

Domain: observing whether the fleet and its host are ALIVE and progressing — and
reporting it. **Detection and report only. This lane never remediates.**

## Decision table

| Intent | Correct surface | Never | Expected output |
|---|---|---|---|
| Is the shokunin fleet alive? | watchdog pid + log freshness + `.ufo/state/*.round` values (count, max, per-lane value vs the ledger's last launch round) | restarting a daemon; killing a pid | `liveness` rows: pid, start time, last tick, state; `WATCHDOG_STATE_LAG`/`_AHEAD` are info — visibility, not severity |
| Did a wave settle? | `.ufo/waves/*/swarm-registry.json` + dispatch/results pair | assuming an unsettled wave is a failed one | per-wave settled/unsettled with age |
| Did something get killed? | MESSAGE-free `journalctl --user/--system -b` catalog-ID records, structured unit-process SIGKILL result records, unit-failure records and distinct numeric signal-11 records; cgroup event counters | remediating, renicing, killing; treating a client-set MESSAGE_ID as authenticated or a notice as a victim | independent `scope=user|system` record counts and current-boot anchor; arbitrary unreported signal paths remain unmeasured; cgroup count with selected source path/scope and observation time, not an event timestamp |
| Is there resource runway? | `df -P` on the fleet root and `/tmp`; since-boot write average per target device; memory pressure PSI + fill/avail against labeled-local thresholds; scope high-watermark `memory.peak` | deleting files; resizing; tuning a labeled-local threshold to fit one observation | runway rows with the measured value: `used_pct`, `io_basis=since-boot`, `psi_some_avg10`, `mem_fill_scope`, `mem_peak` + `mem_peak_anchor` |
| Is a tmux session fleet work? | `tmux ls` + `list-panes -a` pane current paths under the fleet root; per-relevant-session `display-message` activity under a per-call timeout bound | killing/attaching to/steering sessions; treating foreign, or idle past a labeled-local number, as unhealthy | `sessions=N relevant=R foreign=F unclassified=U`; relevance rows carry `freshness=ok probed=P idle=I freshness_unavailable=U`; `TMUX_FOREIGN_SESSION` info per foreign session (path-based rule); `TMUX_SESSION_IDLE` info (r8) |
| Was a lane silent? | roster = `shokunin.conf` lane ids (parsed, never sourced) ∪ `.ufo/state/*.round` names (r12; `MORI_ROSTER_LANES` overrides); launch epoch from `.ufo/watchdog.log` + post-launch authorship (commits/files) | declaring failure from commit sparsity; sourcing the conf | silent / progressing / progressing-weak / young / not-open / unavailable; `roster_source=` + `ROSTER_SET_MISMATCH` info naming conf-only / state-only ids |

## Error patterns

| Observation | Reading |
|---|---|
| watchdog pid gone, no `complete` line | daemon death — a fleet-liveness finding, not a lane failure |
| wave registry present, no results | wave dispatched but never settled — age it, do not call it failed |
| Positive cgroup `oom_kill` | cumulative counter for the named source; counters alone identify neither the killed PID, event time nor fleet membership |
| `oom_kill=0` (cgroup `memory.events` or `/proc/vmstat`) | no **kernel** OOM kills — not "no memory kills": both counters move only at the kernel victim site ([oom_kill.c:935-936 v7.2](https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c)); systemd-oomd kills via `cgroup.kill`/`kill()` and records `user.oomd_ooms`/`user.oomd_kill` xattrs instead ([oomd-util.c:269-306 v261](https://raw.githubusercontent.com/systemd/systemd/v261/src/oom/oomd-util.c)); an inactive oomd/earlyoom is `unavailable (inactive)`, never 0 — `corpus/knowledge/oom-kill-counter-kernel-only-r12.md`, `userspace-oom-killers-r12.md` |
| journal class counts | count records carrying catalog `MESSAGE_ID` (`fe6faa94…` kernel-OOM unit notice, `d989611b…` oomd notice, `fc2e22bc…` coredump — [systemd.catalog.in](https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in)) with `-o json --output-fields=`, never `MESSAGE` text; `COREDUMP_SIGNAL=11` is a separate signal-specific record class. IDs are client-set ([journal-fields](https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html)), not authenticated emitters. Scopes are never summed; nonzero query rc or malformed records is unavailable, not zero — `corpus/knowledge/structured-journal-scopes-r13.md` |
| a kill needs PID / uid / cgroup / time | the kernel `oom-kill:constraint=…,task_memcg=…,pid=…,uid=…` record in the system journal (`journalctl -k`, `__REALTIME_TIMESTAMP` always printed — [journalctl(1)](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html)) is event-time attribution; only shape-validated tokens may leave a probe; re-reading the victim's cgroup later is not attribution (`ENOENT`) — `kernel-oom-line-attribution-r12.md`; not yet a census probe (PROVINCE Frontier) |
| process alive, last tick stale | wedged, not dead — report the age |
| `state_lag=` / `state_ahead=` counters | per-lane round VALUE vs the ledger's last `launch <lane> round=N` line; both info — a state file can disagree without the fleet being unhealthy |
| `state_val_unread_reasons=file:N symlink:N dir:N other:N` | every `*.round` ENTRY is classified before any read; a symlink/directory/non-regular entry is counted with its `WATCHDOG_STATE_ENTRY_UNREADABLE` info instead of vanishing, and symlinks are never followed; `state_val_unreadable` totals them (unreadable values + non-regular entries) while `state_rounds` still counts regular files only |
| `psi_some_avg10` past `psi_warn_avg10`, or fill/avail past their floor | memory pressure graded against labeled-local thresholds (`MEM_PRESSURE_HIGH`/`MEM_FILL_HIGH`/`MEM_AVAIL_LOW` are warn — a local placeholder can flip the roll); `mem_fill_scope=` names the scope — `cgroup` with a numeric `memory.max`, else the `host-ram` fallback, `unavailable` when neither can be read |
| cgroup `mem_peak=` / `mem_peak_source=` / `mem_peak_anchor=` | the scope's kernel high-watermark, comparable only within one cgroup instance (the anchor is the scope dir's mtime); `shape-refused`/`absent`/`unreadable` when it cannot be read — never a fake zero, and it is not a threshold |
| disk row `io_avg_since_boot=` | a since-boot AVERAGE (sectors written × 512 ÷ uptime), never an instantaneous rate; `DISK_IO_UNMEASURED` info when no target device yielded one; the two-sample instantaneous rate stays deferred on measured grounds (the 0.2 s dwell costs ≈208–222 ms across three independent isolations, the extra reads alone 16 ms median); an operator-pinned writer-less FIFO for `MORI_DISKSTATS`/`MORI_UPTIME` is a named open hang, not the live default |
| tmux `foreign=` / `TMUX_FOREIGN_SESSION` | pane-cwd classification only; foreign is a relevance fact, never an unhealthy fleet; a session absent from pane data counts `unclassified`, and no pane data at all → `relevance=unavailable` — neither is foreign |
| tmux `freshness=` / `TMUX_SESSION_IDLE` | idle = now − `session_activity`, probed for fleet-relevant sessions only via one timeout-bounded client call each (default bound 2 s per call, so the freshness block's worst case scales with the relevant-session count); past `idle_warn_s` (default 3600, labeled local) it is info, never DRIFT; `freshness=unavailable` carries its reason (`rc-<N>` — `rc-124` when the bound fired, `rc-137` when the grace kill did, `unparseable` on the row / `unparseable-probe-output` on the finding, `no-timeout-bin` — the probe refuses to run unbounded, `mixed` when only some relevant sessions could be measured) and is never idleness |

## Boundaries (hard)

- **Refuses dispatch mechanism** — that is kumitate. mori observes the fleet, it
  does not start, steer, or reparent anything.
- **Refuses OS-package state** — pacman/systemd units/drivers/firmware/boot are
  tsukuroi. mori reads journal and cgroup counters as fleet-relevant events and
  reports them; it never claims OS-state ownership and never repairs.
- **Refuses endpoint/model health** — kama.
- Credentials, oauth, `server.token` and session material are SHAPE ONLY.

## Checklist (executable)

- [ ] Every observation names its command and the revision/date measured.
- [ ] A missing surface is reported as `unavailable`, never as unhealthy.
- [ ] No remediation is performed or recommended as an action this lane takes.
- [ ] Findings carry a stable id so a later run can compare.

## Gates

`tools/mori-census.sh` — read-only census over the fleet-liveness surfaces.
`verify` → `MORI_CENSUS: CLEAN|DRIFT` exit 0/1, `--selftest` over fixtures,
exit 2 for setup/usage. Registry (PROTOCOL.md §Gate standard fields):

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| census | gate | `bash tools/mori-census.sh` (`MORI_SHOKUNIN_ROOT=<fleet root>` outside the fleet tree) | 0 clean · 1 failed (DRIFT) · 2 could-not-evaluate | `--selftest` (91 cases measured at r13) | expected ids/exits in `run_selftest()` | none live; selftest temp tree | mori |
| drift pin | gate | `bash tools/mori-census.sh --drift <baseline>` | 0 clean (`none`) · 1 failed · 2 could-not-evaluate (baseline missing/unreadable/malformed) | `--selftest` pin/drift arms | `corpus/evidence/baseline-r10-20261015T2231Z.json` | none (`--pin` writes only its path) | mori |
| silence oracle | gate | `bash tools/mori-silence-cases.sh` | 0 clean (all matched) · 1 failed · 2 could-not-evaluate | itself (hermetic case table, 28 cases) | case table in-script | temp fixtures | mori |

Where mori learns — tiers, study paths, search log: `corpus/SOURCES.md`.

The journal arm needs `jq`, `timeout`, and `wc`; missing parser/timeout is
unavailable, never an unbounded or fake-zero scan. Each of twelve serial
current-boot class queries has a labeled-local 2-second bound plus one-second
kill grace (`MORI_JOURNAL_TIMEOUT_S`), not a whole-census deadline. Only known
class fields and the validated boot identifier leave the parser; stderr bytes
are counted then discarded. `oomd_activity=unmeasured` prevents interpreting
zero notice records as active/healthy oomd. Full store access, cursor dedup and
authenticated emitters are not claimed.

**Drift pin (r10).** `--pin <path>` runs the census (live, read-only) and
writes its full output normalized against a declared VOLATILE FIELD LIST —
volatile values masked to `<V>` (timestamps/ages, gauges, since-boot rates,
counters, `script_sha256`); the list is recorded verbatim in the baseline
header and defined in the script header (`tools/mori-census.sh:145-188`).
The baseline names the census bytes' sha256 and the pin clock, both
informational: behavior, not revision, is compared (two SHAs with the same
normalized output stay `none`). `--drift <path>` re-runs and diffs:
`MORI_DRIFT: none` exit 0, or the changed non-volatile fields/lines named —
`key` (changed value), `-key`/`+key` (removed/added field),
`-FINDING:<id>`/`+FINDING:<id>` (removed/added line; `output-order` for a pure
reorder) — exit 1; a missing, unreadable or
malformed baseline is exit 2, never a verdict. Pinning a DRIFT host is still
a pin (the CLEAN/DRIFT roll never decides the pin's exit code) and `--drift`
writes nothing. Selftest coverage (56 → 66 cases, r10): pin→drift clean,
volatile churn staying clean, an injected one-field regression naming its
field, a removed finding, the missing-baseline exit 2, and the two arity
cases. The lane's own live baseline is `corpus/evidence/baseline-r10-20261015T2231Z.json`
(pinned 2026-10-15T22:26:29Z at census `d7710981…`; it read `MORI_DRIFT: none` at
r10 and reads red from 2026-10-19 — tokens classified in `corpus/lessons/round-12.md`)
with its re-run recipe in the r10 evidence set.

`tools/mori-silence-cases.sh` — behavioral gate over `mori-census.sh`'s
lane-silence grading: one `PASS <id> …` / `FAIL <id>: …` line per case over
hermetic fixtures, tally `MORI_SILENCE_CASES: matched=N total=M`, exit 0 iff
all matched (1 on failures, 2 for setup/usage). **r5 run-order + r6
backchannel contract:** cases execute in a seeded-shuffled order and every
case requires the current run's nonce token `nonce-<N>` in its census output —
a stale or missing token fails the case (`run-nonce missing: the current run's
token is absent (canned/replayed output?)`; failure texts never name the
token). The run header prints `SHUFFLE_SEED=`, `RUN_NONCE=` and
`CASE_ORDER=<id> <id> …` (the order executed) only AFTER the last case — a
census running mid-loop cannot read the seed or order from the oracle's stdout
or process environment (the live nonce stays in the census's own env by
design); the graded `PASS` lines carry `nonce=1` (the two check-style
cases, `shape-invariance` and `readonly-no-mutation`, print bare `PASS <id>`).
Fixture content is per-run: the nonce token and an unprinted run salt are
woven into fixture bodies, commit messages and per-run blob files, so a
content→grade table memorized from an earlier run no longer matches. Pin
`MORI_SHUFFLE_SEED=<int>` / `MORI_RUN_NONCE=<int>` at invocation for a
byte-identical rerun (same seed → same order; both pins are dropped from the
process tree before any case runs); unset, both are random per run, and the
salt is never pinnable or printed.

**Round 13 verdict contract.** Every oracle case, including shape invariance and
read-only mutation checks, requires exactly one complete final census verdict
with the documented tally fields and `CLEAN`/exit 0 or `DRIFT`/exit 1 agreement.
`BANANA`, missing/duplicate records and opposite roll/rc combinations fail the
case. This closes audit F02's demonstrated prefix-only acceptance, not all
possible output forgery channels. Production exact-author membership consumes
captured history without an early-exiting producer pipe (audit F01); see
`corpus/knowledge/verdict-contract-r13.md` and the round-13 regression receipt.

## Finding → owner routing (two tiers — a deadlock was measured here)

Routing a finding to `tsukuroi` or `kama` for *remediation* deadlocks: both
provinces explicitly refuse to act (`tsukuroi-shokunin/PROVINCE.md:19` "never restarts
services. Detection and report; the operator remediates."; `kama-shokunin/PROVINCE.md:45-47` "kama never writes
to `~/.config`, `~/.omp`, or systemd units ... the operator repoints them"). mori
never remediates either. So a finding carries **two** owners:

| Tier | Role | Who | Acts how |
|---|---|---|---|
| 1 — triage/diagnosis | read-only domain specialist | `tsukuroi` (OS substrate, units, drivers) · `kama` (loopback model ports, baseURL drift) · `kumitate` (wave settlement, dispatcher queue, watchdog state) · `mori` (census hygiene, fixtures) | re-probes with its own tool and produces a diagnosis |
| 2 — actuation | authorized actor | `kumitate` for **automated orchestration** actions (`ufo-swarm-wave.mjs`, `fleet-dispatcher.mjs repend`, `ufo-sighting complete`) · **operator** for **host** mutations (service restarts, pacman, cgroup limits, mounts, deletions) | performs the change |

**Never collapse all findings onto `operator`** — that drowns the human in raw
kernel stacks and counter deltas with no domain triage. mori's payload must carry
enough typed context (`pid`, `comm`, `cgroup`, `mount`, `use_pct`, `wave_dir`,
`schema`, `newest_file_age_s`) that Tier 1 can diagnose without re-probing.

**Premature-settlement guard:** an `WAVE_UNSETTLED_AGE` finding must never trigger
an automated settle while lanes are still writing; require
`newest_file_age_s` past a conservative stall threshold first.

## Secret-exposure exclusions (measured by a sentinel audit)

The census is count-only over the journal and shape-only over host paths. Two forms
were ruled out and must stay out:

- **Never print journal `MESSAGE` content.** This boot's user journal carries 221
  `1password` lines and 2 `gnome-keyring-daemon` lines with opaque runs; the probe
  counts them and never echoes the text. Never run the gate under `set -x`, and
  never capture journal output into a variable that is later echoed.
- **Never read a cgroup counter outside `/sys/fs/cgroup/`.** `read_file` echoes the
  first line into the surface row, so an operator-pointed `MORI_CGROUP_CURRENT`
  would print another file's first line; the probe refuses out-of-tree paths
  shape-only (`refused:outside-sysfs-cgroup`). r7's PSI/limit readers and r8's
  `memory.peak` reader reach the same no-echo outcome by shape: only validated
  tokens (`is_decimal` avg10, `is_int` bytes, the literal `max`) can enter a row
  (`mem_peak_source=shape-refused` otherwise).

Also excluded: `ps e` / `/proc/<pid>/environ` (`omp` carries
`HL_INITIAL_WORKSPACE_TOKEN`), `cat /proc/<pid>/fd/*` (`omp` holds 51 readable fds
onto session JSONL), and any journal output mode that keeps `MESSAGE`.

## Disk thresholds are a PROPOSAL, not a measurement

`DISK_WARN_PCT=85` / `DISK_CRIT_PCT=95` carry **no write-rate evidence** and are
labeled as such. (**r7/r8 update — `census-r4` → `census-r5`:** the census
measures a write rate, but only the **average since boot** —
`io_basis=since-boot`, `io_avg_since_boot=<dev>:<Bps>/<uptime>s`, sectors
written × 512 ÷ uptime from `/proc/diskstats`, no sampling interval added to
runtime. The instantaneous two-sample rate stays a deferral, and r8 paid its
named precondition — the 0.2 s-window variant measured ≈208–222 ms across three
independent 15–30× isolations (minimum 208 ms) over the two-read floor against a
50 ms budget; the dwell is the cost, the reads alone 16 ms median — so it stays
out of census runtime on measured grounds, not an estimate. The average is not a
licence to recalibrate 85/95.) Falsification results worth keeping:

- The fleet's *actually reported* disk failures are **quota** events (`EDQUOT`,
  "disk-quota pressure") — a capacity-percent probe cannot see them, and the quota
  numbers are unreadable on this host.
- **Never threshold the btrfs chunk percent.** Data-chunk fill reads **94.25%**
  while `df -P` Capacity on the same device reads **10%**; a probe that used the
  chunk percent would fire `DISK_LOW` against every proposed default today. Keep
  the `df -P` parser.
- **Never OR a byte floor against `df -P`'s Available column** — it is in
  1024-blocks, so a bytes-denominated floor false-fires on a 10%-full filesystem.
- One pair only. A sibling note proposing 90 and another proposing 80 must not be
  described as the default beside 85/95, or a later diff cannot say which proposal
  was tested.
- The since-boot average counts **every** write to the device since boot (OS and
  desktop included) and smooths bursts; it is not attributable to the fleet and
  is not a distribution to threshold against.

## Lane-silence grading is launch-aware and authorship-aware (r2 contract)

**Revision marker r2 — round 3, 2026-10-15.** This section replaces the round-1
rolling-window description. The binding decision table (lifecycle rows, exact
identity policy, named preconditions) is `corpus/knowledge/silence-grading-r2.md`;
it implements `PROTOCOL.md:153-168`.

`probe_silence` grades each roster lane against the launch epoch of its current
round, read from `.ufo/watchdog.log` (never log mtime, never the `tick=` counter),
and emits a per-lane row `SURFACE lane.<id>: <state> (lane=<id> round=<N>
launch_epoch=<e> age_s=<s> basis=<row> …; ts=…)` with state in {`silent`,
`progressing`, `progressing-weak`, `young`, `not-open`, `unavailable`}; the
aggregate `SURFACE silence:` row keeps the per-state counters (`silent=` /
`progressing=` / `progressing_weak=` / `young=` / `not_open=` / `unavailable=` /
`skipped=`).

- **Only a still-open mission is graded — closed reads `not-open`.** A
  `complete`/`wrap` line for the same lane+round closes it, as does a committed
  report at HEAD whose newest path commit has `launch_epoch < ct ≤ now`; a later
  same-round `launch` reopens it and a state-round advance hands the grade to the
  new round. No matching launch line → `not-open`; unreadable ledger/repo/git
  input → `unavailable` — a missing surface is never unhealthy.
- **Strict age gate.** Only `now − launch_epoch > LANE_SILENCE_S` (default 7200)
  is gradeable-old; age at or below the gate, or a future launch → `young`.
- **Authorship decides open-and-old, matching both identity fields exactly** —
  `<lane>-shokunin <lane>@shokunin.local`, never substring, never `%cn`/`%ce` —
  over ALL post-launch commits: a lane-authored commit → `progressing`; no subject
  commits but unexplained untracked/dirty recent files in the lane's own scope →
  `progressing` (attribution inference disclosed); sibling-only activity with a
  clean checkout → `progressing-weak`; nothing attributed → `silent`.
- **`FINDING LANE_SILENT severity=warn` fires only for the row-D clean-old-silent
  case**, carrying lane/round/launch_epoch/age_s — replacing the r1
  `head_epoch=`/`newest_epoch=` pair. `unavailable`/`not-open`/`young` emit no
  finding and no DRIFT.

The two measured r1 divergences this contract closes: the aggregator was
over-credited `progressing` by sibling commits plus a gitignored `game-dev-3d`
`watch.log`; kasegi was graded while its round had wrapped
(`.ufo/watchdog.log:287`; `LOG.md:73-80`).

Cutover receipt: `census-r2` landed in `tools/mori-census.sh` — sha256
`fe22a14f0bb6d90ffed14506abfcd76153ebf31cf3cb769b97e7eec61cc2f3c9` — round
receipts `corpus/evidence/cutover-r3-*.log`.
