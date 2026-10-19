# mori-shokunin — Province

**Domain:** fleet & host observability (森) — whether the fleet, its waves and
its host are alive and progressing.

**Owns (read-only probes):** shokunin watchdog liveness (pid, start time, log
freshness, lane counters); `.ufo/waves/*` settlement state (registry + results
pair); kill/OOM event classes from `journalctl --user` and cgroup
`memory.events`; resource runway (disk on the fleet and scratch roots, memory
pressure); lane silence grading (silent / progressing / progressing-weak).

**Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package,
systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal
and cgroup events as fleet evidence and reports them, never owning OS state;
endpoint and model-serving health (→ kama); credential material (→ kagi).
**Detection and report only — never remediation.**

**Out of province → report, never absorb.**

## Core

- **Watchdog liveness** — census `SURFACE watchdog`: watchdog pid/start and log freshness, plus `.ufo/state/*.round` values against each lane's latest launch-ledger entry.
- **Wave settlement** — `SURFACE waves`: registry/dispatch/results presence and per-wave age; report settled, unsettled, or empty without calling an aged wave failed.
- **Kill/OOM classes** — `SURFACE journal` and `SURFACE cgroup`: user-journal OOM/kill/segfault/unit-failure counts plus cgroup memory-event counters; these are scoped counts, not victim, event-time, or fleet-cause attribution.
- **Resource runway** — `SURFACE disk` and `SURFACE cgroup`: default `df -P` targets `$ROOT` and `/tmp`, since-boot device-write average, memory PSI/fill/avail, and scope high-watermark.
- **tmux relevance** — `SURFACE tmux`: classify sessions by pane path; bound the freshness probe for each relevant session.
- **Lane silence** — `SURFACE lane.<id>` rows: launch-anchored authorship grading as silent, progressing, progressing-weak, young, not-open, or unavailable.

## Frontier

- **FR1 — System-journal kill/segfault scope, kernel OOM attribution, and fleet correlation** (state F1/F8 + art F2). First evidence: `corpus/knowledge/kernel-oom-line-attribution-r12.md:10-16`; `corpus/knowledge/kill-classes-by-message-id-r12.md:10-16`; `corpus/knowledge/audit-r11.md:203-204`. Boundary: system-journal coverage is not the current user-journal probe; never echo `MESSAGE`, and a host event alone does not prove a fleet-caused kill.
- **FR2 — Quota/EDQUOT observability** (state F2). First evidence: `corpus/knowledge/audit-r11.md:218-222`. Boundary: `df` capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state.
- **FR3 — Authoritative wave settlement and emptied-by-hygiene versus never-written** (state F3). First evidence: `corpus/knowledge/audit-r11.md:202`; `../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:28-34,91-120`. Boundary: mori reports filesystem shape; kumitate owns orchestration/result semantics; `empty` alone does not prove never-written, and receipt review stays offline.
- **FR4 — Driver-state versus MANIFEST versus lane-LOG round reconciliation** (state F4). First evidence: `../fleet-ledger/.ufo/waves/kaika-w1/mori-state.md:31,190`; `corpus/knowledge/observability-surfaces-r2.md:118-125`. Boundary: the census compares driver state with watchdog launch lines only; it does not establish MANIFEST admission or lane-LOG agreement.
- **FR5 — Watchdog daemon identity and degraded-pgrep visibility** (state F5). First evidence: `corpus/knowledge/audit-r11.md:200-201`. Boundary: an unavailable pid probe is not absence, and argv-substring matches do not establish daemon identity.
- **FR6 — Instantaneous disk write-rate** (state F6). First evidence: `corpus/knowledge/surfaces-r8.md:75-89`. Boundary: retain the since-boot average as a different measure; a two-sample rate stays deferred until its added latency meets the stated budget.
- **FR7 — Live tmux relevance/freshness arm** (state F7). First evidence: `corpus/knowledge/surfaces-r8.md:120-124`. Boundary: the host arm is fixture-proved only; do not create or steer sessions, and unavailable is not unhealthy.
- **FR8 — Alert-threshold calibration** (state F9). First evidence: `corpus/knowledge/audit-r11.md:205`. Boundary: thresholds remain labeled local; a quiet window is not a workload distribution or an alert-cost rule.
- **FR9 — Durable fixture evidence** (state F10). First evidence: `corpus/knowledge/audit-r11.md:41-46`. Boundary: scratch paths and unreconstructable fingerprints are not durable evidence; retain a reproducible fixture generator and digest before making replay claims.
- **FR10 — Userspace OOM killers (systemd-oomd and earlyoom)** (art F1). First evidence: `corpus/knowledge/userspace-oom-killers-r12.md:10-15`. Boundary: inactive killers are unavailable, not zero; `memory.events oom_kill` does not cover every userspace kill; never enable or tune a killer.
- **FR11 — New-since-pin journal kill counts via cursors** (art F3). First evidence: `corpus/SOURCES.md:20-21`. Boundary: cursor queries stay read-only and pin-scoped; [UNKNOWN] behavior after cursor rotation/vacuum and ordering across boots.
- **FR12 — Event-driven pressure and CPU/IRQ PSI** (art F4). First evidence: `corpus/SOURCES.md:7-8,16`; `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md:57-73`. Boundary: a PSI trigger watcher is resident, not a one-shot census probe; system CPU `full=0` is not evidence of no stall.
- **FR13 — eBPF kill/OOM tracing** (art F5). First evidence: `corpus/SOURCES.md:11-12,23-26`. Boundary: privilege and version matter; a resident tracer is outside the census, so retain this as knowledge/frontier only.
- **FR14 — Agent-workload telemetry** (art F6). First evidence: `corpus/SOURCES.md:28-32`. Boundary: mori is consume-only; telemetry emission belongs to the emitting lanes and orchestration.

## Adjacent

Report shared evidence to its owner; do not absorb another lane's domain.

| Sibling | Boundary | Evidence |
|---|---|---|
| kumitate | Owns OMP task/hub orchestration and wave plan/run/record/collect semantics; mori passively grades `.ufo/waves/*` filesystem settlement state. No conflicting settlement contract was found. | `../kumitate-shokunin/PROVINCE.md:3-6`; `../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:28-34,91-120`; `PROVINCE.md:6-10` |
| tsukuroi | Owns host OS, package, systemd-unit, driver, firmware, and boot diagnosis. It was the only sibling hit in R12Connector's corpus search for `systemd-oomd`, `earlyoom`, `memory.events`, and `MESSAGE_ID`; this is adjacent host diagnosis, not contested fleet ownership. | `../tsukuroi-shokunin/PROVINCE.md:21-24,35-44`; `../tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:231-257,279-281,301,344-367`; `../tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md:30-37,97,120-135`; `PROVINCE.md:12-16` |
| kama | Owns local model-serving and endpoint health; mori does not infer serving health from host/resource signals. | `../kama-shokunin/PROVINCE.md:3-15,40-53` |
| kagi | Owns secrets, vault operations, and credential-hygiene evidence; mori never reads or reports credential material. | `../kagi-shokunin/PROVINCE.md:3-6`; `SKILL.md:49` |
| souji | Owns artifact cleanup, not process/fleet health. Its province says “mori-shokunin observes fleet health and reports; souji acts on artifacts” (`../souji-shokunin/PROVINCE.md:40-41`). | `../souji-shokunin/PROVINCE.md:40-41`; `../souji-shokunin/census/round-3/operator-approval-list.tsv:56-73`; `../souji-shokunin/census/operator-sweep-20261018/approval-list.tsv:56-73`; `../souji-shokunin/census/operator-sweep-20261018/resume-verdicts.tsv:52-69` |

- **Received packet TSUKUROI-F1-MEM-01 (ADJ-04):** `../tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:74-112` records the 2026-10-15T04:53:46Z capture as `prepared`; boot identity/event window were not captured, and acknowledgement/acceptance/resolution are unobserved. Its request is to compare the timestamp with watchdog/wave evidence if retained, not to infer an OOM or cause.
- **What mori can place:** 04:53:46Z is 01:53:46-03:00, between watchdog ticks at 01:50:57 and 01:58:27; `mori round=2` and `tsukuroi round=1` launched at 01:50:57 (`.ufo/watchdog.log:395-402`). Fleet commits bookend that point: `git -C /home/vgpnk/Projects/shokunin show -s --format='%h %ci %s' 99efc52 f2df270` → `99efc52 2026-10-15 01:52:09 -0300`; `f2df270 2026-10-15 01:55:17 -0300`. [INFERENCE] This locates active fleet work, not a settled-wave state at the packet's exact second.
- **Count-only kill sweep for the packet second:** the packet's single PSI snapshot is not a retained pressure series; its PSI `total` fields are cumulative stall time and the fixed root `memory.events` path was absent, not zero (`../tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:94-104`). These time-bounded, MESSAGE-free queries returned 0:

  ```sh
  journalctl -k -b all -q --since='2026-10-15 04:53:46 UTC' --until='2026-10-15 04:53:47 UTC' --grep='^oom-kill:constraint=' -o json --output-fields=_BOOT_ID | wc -l
  # 0
  journalctl --system -b all -q --since='2026-10-15 04:53:46 UTC' --until='2026-10-15 04:53:47 UTC' MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=MESSAGE_ID,_BOOT_ID | wc -l
  # 0
  journalctl --system -b all -q --since='2026-10-15 04:53:46 UTC' --until='2026-10-15 04:53:47 UTC' MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID,_BOOT_ID | wc -l
  # 0
  journalctl --user -b all -q --since='2026-10-15 04:53:46 UTC' --until='2026-10-15 04:53:47 UTC' MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=MESSAGE_ID,_BOOT_ID | wc -l
  # 0
  journalctl --user -b all -q --since='2026-10-15 04:53:46 UTC' --until='2026-10-15 04:53:47 UTC' MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID,_BOOT_ID | wc -l
  # 0
  ```

  No retained kernel OOM, `fe6faa94…` unit-kill notice, or `d989611b…` oomd notice overlaps this bounded query; [UNKNOWN] no independent pressure-series comparison is available for this packet. The single snapshot cannot establish fleet cause or wave settlement. Correlation is not causation.
- **Souji's receipts distinguish only listed removals:** the approval list records hashed `aggregator-r10*` artifacts and the later sweep marks those exact paths `pushed`. For precisely those named paths, receipts support a `swept (pushed-receipt)` classification; for an empty path without a matching receipt, [UNKNOWN] history, so it is not evidence of “never written.” This is offline evidence reading, not a live census dependency.
- **Source overlap:** R12Connector compared the S001–S030 URL set in `../fleet-ledger/.ufo/waves/kaika-w1/mori-art.md:91-124` with sibling `corpus/SOURCES.md` registries; its exact-URL sweep found no shared URL, so no source rows are merged here.

## Corrections (round 12)

- The existing phrase “scratch roots” does not resolve to a measured target: `/scratch` is absent (the path inspection returned `Path '/scratch' not found`; `../fleet-ledger/.ufo/waves/kaika-w1/mori-state.md:180` records `ls /scratch` → absent). The census documents `MORI_DISK_TARGETS` as defaulting to `$ROOT /tmp` (`tools/mori-census.sh:211-212,282`); `/scratch` is not a default disk target.
