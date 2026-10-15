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
| Is the shokunin fleet alive? | watchdog pid + log freshness + lane counters | restarting a daemon; killing a pid | `liveness` rows: pid, start time, last tick, state |
| Did a wave settle? | `.ufo/waves/*/swarm-registry.json` + dispatch/results pair | assuming an unsettled wave is a failed one | per-wave settled/unsettled with age |
| Did something get killed? | `journalctl --user -b` OOM/kill lines + cgroup event counters | remediating, renicing, killing | journal class counts; cgroup count with selected source path/scope and observation time, not an event timestamp |
| Is there resource runway? | `df` on the fleet + scratch roots; memory pressure counters | deleting files; resizing | runway rows with the measured value |
| Was a lane silent? | launch epoch from `.ufo/watchdog.log` + post-launch authorship (commits/files) | declaring failure from commit sparsity | silent / progressing / progressing-weak / young / not-open / unavailable |

## Error patterns

| Observation | Reading |
|---|---|
| watchdog pid gone, no `complete` line | daemon death — a fleet-liveness finding, not a lane failure |
| wave registry present, no results | wave dispatched but never settled — age it, do not call it failed |
| Positive cgroup `oom_kill` | cumulative counter for the named source; counters alone identify neither the killed PID, event time nor fleet membership |
| process alive, last tick stale | wedged, not dead — report the age |

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
exit 2 for setup/usage. Registry row lands with the gate.

## Finding → owner routing (two tiers — a deadlock was measured here)

Routing a finding to `tsukuroi` or `kama` for *remediation* deadlocks: both
provinces explicitly refuse to act (`tsukuroi/PROVINCE.md:16-17` "never restarts
services ... the operator remediates"; `kama/PROVINCE.md:22-26` "kama never writes
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
  shape-only (`refused:outside-sysfs-cgroup`).

Also excluded: `ps e` / `/proc/<pid>/environ` (`omp` carries
`HL_INITIAL_WORKSPACE_TOKEN`), `cat /proc/<pid>/fd/*` (`omp` holds 51 readable fds
onto session JSONL), and any journal output mode that keeps `MESSAGE`.

## Disk thresholds are a PROPOSAL, not a measurement

`DISK_WARN_PCT=85` / `DISK_CRIT_PCT=95` carry **no write-rate evidence** and are
labeled as such. Falsification results worth keeping:

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
