# mori-shokunin — 森

**Fleet and host observability — is the forest alive and progressing?**

A **shokunin lane** minted and trained under the
[shokunin](https://github.com/VeigaPunk/shokunin) skill. Mori detects and
reports. **It never remediates.**

**Wiki:** [lane overview](https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/mori-shokunin?branch=master)

## Domain

Read-only probes from `PROVINCE.md` and `SKILL.md`:

| Question | Surface | Never |
|---|---|---|
| Is the fleet alive? | watchdog pid, start time, log freshness, lane counters | restart a daemon; kill a pid |
| Did a wave settle? | `.ufo/waves/*` registry + dispatch/results pair | treat unsettled as failed |
| Did something get killed? | `journalctl --user` OOM/kill lines + cgroup `memory.events` | renice, delete, remediate |
| Is there resource runway? | disk on fleet/scratch roots; PSI; `memory.peak` | resize, tune a threshold to fit one observation |
| Was a lane silent? | launch epoch + post-launch authorship | declare failure from commit sparsity |

Silence grades: `silent` / `progressing` / `progressing-weak` / `young` /
`not-open` / `unavailable`.

`WATCHDOG_STATE_LAG` / `_AHEAD` are **info** — visibility, not severity.

## What it refuses

| Out of province | Owner |
|---|---|
| dispatch and orchestration mechanism | [kumitate](https://github.com/VeigaPunk/kumitate-shokunin) |
| OS package, systemd unit, driver/firmware, boot state | [tsukuroi](https://github.com/VeigaPunk/tsukuroi-shokunin) |
| endpoint and model-serving health | [kama](https://github.com/VeigaPunk/kama-shokunin) |
| credential material | [kagi](https://github.com/VeigaPunk/kagi-shokunin) |

Mori reads journal and cgroup events as *fleet evidence* and reports
them. It does not own OS state.

## In this repository

```
PROVINCE.md     detection-only boundary
SKILL.md        liveness / settlement / silence decision table
SHONEN.md  SCORECARD.md  LOG.md  MINT.md   (minted 2026-10-14)
corpus/         knowledge/, lessons/, evidence/, QUALITY.md
tools/
  mori-census.sh
  mori-silence-cases.sh
```

## Census

```bash
bash tools/mori-census.sh
bash tools/mori-silence-cases.sh
```

These grade the fleet and host. They do not restart, kill, or delete.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
