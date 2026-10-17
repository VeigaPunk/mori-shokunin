# mori-shokunin — 森

**Fleet and host observability.** Is the fleet alive? Did a wave
settle? Did something get killed? Is there runway? Was a lane silent?

Mori detects and reports. **It never remediates.** Restarting a
daemon, deleting files, or declaring a wave "failed" because it has
not settled yet are all out of province.

This is a **shokunin lane** of the [shokunin fleet](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**.

## The craft

From [`SKILL.md`](SKILL.md):

| Intent | Correct surface | Never |
|---|---|---|
| Is the fleet alive? | watchdog pid + log freshness + `.ufo/state/*.round` | restart a daemon |
| Did a wave settle? | `.ufo/waves/*` registry / dispatch / results pair | treat unsettled as failed |
| Did something get killed? | `journalctl --user -b` + cgroup `memory.events` | remediate, renice, kill |
| Is there runway? | `df` on fleet + scratch; PSI / fill / `memory.peak` | delete or resize |
| Is a tmux session fleet work? | `tmux ls` + pane cwds under the fleet root | attach, steer, or kill |
| Was a lane silent? | launch epoch + post-launch authorship | declare failure from commit sparsity |

Silence grades: `silent` / `progressing` / `progressing-weak` /
`young` / `not-open` / `unavailable`. A watchdog pid that is gone
with no `complete` line is daemon death — a fleet-liveness finding,
not a lane failure.

The census gate (`tools/mori-census.sh`) emits `MORI_CENSUS:
CLEAN|DRIFT`, stable finding ids, and `--pin` / `--drift` against a
declared volatile contract. The silence oracle
(`tools/mori-silence-cases.sh`) is the mutation battery for that
grader.

## Province

Owns (read-only probes): watchdog liveness; wave settlement; kill/OOM
event *classes*; resource runway; lane silence grading.

**Refuses:** dispatch mechanism (→ kumitate); OS package / systemd /
driver / boot state (→ tsukuroi — mori reads journal and cgroup events
as fleet evidence and reports them, never owning OS state); endpoint
health (→ kama); credential material (→ kagi).

See [`PROVINCE.md`](PROVINCE.md).

## What's in this repository

```
mori-shokunin/
├── SKILL.md                 decision table, error patterns, silence contract
├── PROVINCE.md
├── SHONEN.md
├── LOG.md                   rounds 0–11 recorded
├── SCORECARD.md
├── MINT.md                  operator directive + unowned fleet-health demand
├── AGENTS.md
├── tools/
│   ├── mori-census.sh       live census + --pin/--drift + --selftest
│   └── mori-silence-cases.sh
└── corpus/
    ├── knowledge/           silence-grading, surface notes
    ├── lessons/
    ├── evidence/            including the r10 drift baseline
    └── fixtures/
```

## Start here

```sh
bash tools/mori-census.sh --selftest
bash tools/mori-silence-cases.sh
```

Live census against a host is `bash tools/mori-census.sh`. `DRIFT` is
a finding, not a license to fix the host. `--pin` / `--drift` are
documented in the script header and `LOG.md` round 10.

## How a round works

One axis-move. Lane identity: `mori-shokunin <mori@shokunin.local>`.

## Fleet

[VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin) ·
[kumitate-shokunin](https://github.com/VeigaPunk/kumitate-shokunin) ·
[tsukuroi-shokunin](https://github.com/VeigaPunk/tsukuroi-shokunin) ·
[kimi-shokunin](https://github.com/VeigaPunk/kimi-shokunin)
