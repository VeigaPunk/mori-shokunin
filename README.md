# mori-shokunin — 森

**Is the fleet alive, and is it progressing?** Detection and report
only. This lane never remediates.

This is a [shokunin](https://github.com/VeigaPunk/shokunin) lane for
fleet and host observability: watchdog liveness, wave settlement, kill /
OOM event classes, resource runway, lane silence. Rank: shonen.

Mori reads the forest. It does not restart a daemon, delete files,
renice a cgroup, or declare a silent lane failed from commit sparsity.
Dispatch mechanism is
[kumitate](https://github.com/VeigaPunk/kumitate-shokunin). OS package,
systemd, driver, and boot state are
[tsukuroi](https://github.com/VeigaPunk/tsukuroi-shokunin) — mori reads
journal and cgroup events as fleet evidence and reports them. Endpoint
health is [kama](https://github.com/VeigaPunk/kama-shokunin).

## Province

**Owns (read-only probes):** shokunin watchdog liveness (pid, start
time, log freshness, lane counters); `.ufo/waves/*` settlement
(registry + results pair); kill / OOM event classes from
`journalctl --user` and cgroup `memory.events`; resource runway (disk
on the fleet and scratch roots, memory pressure); lane silence grading
(`silent` / `progressing` / `progressing-weak` / `young` / `not-open` /
`unavailable`); tmux session relevance by pane path under the fleet
root.

**Refuses:** dispatch and orchestration (→ kumitate); OS package,
systemd unit, driver / firmware and boot state (→ tsukuroi); endpoint
and model-serving health (→ kama); credential material (→ kagi).

Full boundary: [`PROVINCE.md`](PROVINCE.md).

## Start here

1. [`SKILL.md`](SKILL.md) — decision table and silence-grading contract.
2. [`PROVINCE.md`](PROVINCE.md) — owned probes and the never-remediate rule.
3. [`tools/mori-census.sh`](tools/mori-census.sh) — the observability census.

## The census

```
bash tools/mori-census.sh              # live read-only census
bash tools/mori-census.sh --selftest   # hermetic cases
bash tools/mori-silence-cases.sh       # silence-grading fixtures
```

Verdict: `MORI_CENSUS: CLEAN|DRIFT`. Exit `0` CLEAN · `1` DRIFT · `2`
setup / usage. Surfaces: watchdog, waves, journal, cgroup, disk,
silence, optional tmux. Thresholds are labeled local. A foreign tmux
session (all panes outside the fleet root) is `TMUX_FOREIGN_SESSION`
info, not a health failure. `WATCHDOG_STATE_LAG` / `_AHEAD` are
visibility, not severity.

A CLEAN census is not a claim that a wave caused an OOM. Cumulative
cgroup counters are not dated incidents — hand those to tsukuroi with
capture time, boot window, and the exact command.

## What's in the repo

```
mori-shokunin/
├── SKILL.md          observability playbook
├── PROVINCE.md       domain boundary
├── SHONEN.md         promotion checklist
├── MINT.md           why this lane was minted
├── LOG.md            append-only audit trail
├── SCORECARD.md      axis verdicts
├── AGENTS.md         operating rules
├── tools/            mori-census.sh, mori-silence-cases.sh
└── corpus/           knowledge/, lessons/, QUALITY.md
```

Protocol: append-only corpus; every claim separates observation /
inference / unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme) for how a lane
learns.
