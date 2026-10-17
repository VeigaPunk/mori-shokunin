# mori-shokunin — 森

Fleet and host observability. Whether the fleet, its waves, and its host
are alive and progressing.

Rank: **shonen**. [`SHONEN.md`](SHONEN.md) boxes are open.

Fleet root: [shokunin](https://github.com/VeigaPunk/shokunin).

## The question

> Is the fleet alive, did the wave settle, and is there runway — and can
> that be said from a read-only probe?

Detection and report only. This lane never remediates: it does not
restart a daemon, delete files, renice a process, or attach to a tmux
session.

## Boundary

**Owns:** shokunin watchdog liveness (pid, start time, log freshness, lane
counters); `.ufo/waves/*` settlement; kill and OOM event classes from
`journalctl --user` and cgroup `memory.events`; resource runway (disk,
memory pressure); lane silence grading (`silent` / `progressing` /
`progressing-weak`, plus the younger and unreadable states the census
names).

**Hands off:** dispatch mechanism (kumitate); OS packages, systemd units,
drivers, firmware, and boot state (tsukuroi) — mori reads journal and
cgroup events as fleet evidence and reports them; endpoint health (kama);
credential material (kagi).

## Run

```sh
bash tools/mori-census.sh
```

Verdict line `MORI_CENSUS: CLEAN|DRIFT`. Exit `0` clean, `1` drift, `2`
setup or usage. Surfaces, from the script header: watchdog, waves,
journal, cgroup, disk, silence, and an optional tmux classification.
Foreign tmux sessions are a relevance fact, not an unhealthy fleet.
`tools/mori-silence-cases.sh` holds the silence-grading cases beside the
census.

Read `SKILL.md` before treating a counter as an incident. A positive
cgroup `oom_kill` is a cumulative counter for a named source. It does not
by itself name a pid, a time, or fleet membership. Disk rows are a
since-boot average, not an instantaneous rate.

## Map

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | decision table and the error-pattern readings |
| [`PROVINCE.md`](PROVINCE.md) | owned probes and refusals |
| [`corpus/knowledge/`](corpus/knowledge/) | including the silence-grading contract |
| [`corpus/evidence/`](corpus/evidence/) | captured probe output |
| [`LOG.md`](LOG.md), [`SCORECARD.md`](SCORECARD.md) | rounds and axis verdicts |

A watchdog pid that is gone, with no `complete` line, is a fleet-liveness
finding. It is not yet a verdict about any one lane.
