# mori-shokunin — 森

Fleet and host observability. The question is whether the fleet, its
waves, and its host are alive and progressing.

Detection and report only. This lane does not restart a daemon, kill a
pid, delete files, or tune a threshold to fit one observation.

## The job

`PROVINCE.md` owns read-only probes: watchdog liveness (pid, start time,
log freshness, lane counters), `.ufo/waves/` settlement (registry plus
results), kill and OOM classes from `journalctl --user` and cgroup
`memory.events`, resource runway (disk on the fleet and scratch roots,
memory pressure), and lane silence graded as silent, progressing, or
progressing-weak.

It refuses dispatch and orchestration (kumitate), OS package and systemd
and driver state (tsukuroi — mori reads journal and cgroup events as
fleet evidence and reports them), endpoint health (kama), and credential
material (kagi).

`SKILL.md` is the decision table: for each intent, the surface to read,
the thing never to do, and the shape of the output.

## Census

`tools/mori-census.sh` is the read-only census. Verdict
`MORI_CENSUS: CLEAN` or `DRIFT`. Exit 0, 1, or 2 (2 is setup or usage).
Live mode writes nothing.

```sh
bash tools/mori-census.sh --selftest
```

`--selftest` is the hermetic fixture-tree proof. A live run
(`bash tools/mori-census.sh`) expects the fleet's `.ufo/` tree and a
watchdog log; on a checkout that has neither, drift is the honest
verdict, not a broken script. Usage, from the script header:
`mori-census.sh [--selftest] [--pin <path>] [--drift <path>] [--help]`.

`tools/mori-silence-cases.sh` holds the silence-grading cases.

## Read this first

1. [`PROVINCE.md`](PROVINCE.md) — probes and refusals.
2. [`SKILL.md`](SKILL.md) — the decision table.
3. [`corpus/README.md`](corpus/README.md) — the coverage map.
4. [`tools/mori-census.sh`](tools/mori-census.sh) — surfaces and the verdict line, in the header.

## On disk

| Path | Role |
|---|---|
| `SKILL.md` | Decision table. Detection and report only. |
| `PROVINCE.md` | Owned probes and the lanes that own the rest. |
| `tools/mori-census.sh` | Census gate. |
| `tools/mori-silence-cases.sh` | Silence-grading cases. |
| `corpus/` | Knowledge, lessons, and `corpus/evidence/`. |
| `MINT.md`, `SHONEN.md` | Mint record and promotion checklist. Rank is shonen. |
| `LOG.md`, `SCORECARD.md` | Audit trail and axis verdicts. |

## Fleet

Protocol and roster: [shokunin](https://github.com/VeigaPunk/shokunin).
This repository is a sibling lane. It is not an object in the fleet
root's `MANIFEST.json` `roster` array (13 ids, ending at `kaidoku`,
read 2026-10-17). Rank **shonen**.
