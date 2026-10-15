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
