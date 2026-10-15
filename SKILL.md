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
| Did something get killed? | `journalctl --user -b` OOM/kill lines + cgroup `memory.events` | remediating, renicing, killing | classified kill events with cgroup + timestamp |
| Is there resource runway? | `df` on the fleet + scratch roots; memory pressure counters | deleting files; resizing | runway rows with the measured value |
| Was a lane silent? | lane HEAD vs last report mtime | declaring failure from commit sparsity | silent / progressing / progressing-weak |

## Error patterns

| Observation | Reading |
|---|---|
| watchdog pid gone, no `complete` line | daemon death — a fleet-liveness finding, not a lane failure |
| wave registry present, no results | wave dispatched but never settled — age it, do not call it failed |
| `oom_kill` in `memory.events` | a real kill event: record cgroup, timestamp, and the killed pid |
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
