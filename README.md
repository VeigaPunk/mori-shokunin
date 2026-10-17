# mori-shokunin — 森

Whether the fleet, its waves, and its host are alive and progressing.

Mori censes. A silent lane, a stale watchdog log, a wave that never
settled, a cgroup that has been killing, a disk that is filling: each
becomes a finding id and a verdict line. The census does not restart a
process, delete a wave, or free memory. Remediation belongs to the
operator, and the mechanism of dispatch belongs to kumitate.

Rank: **shonen**. `SHONEN.md` is still here. The fleet `MANIFEST.json`
minted this lane on 2026-10-14 and withheld the roster row. The mint note
is explicit: detection and report only.

## Province

**Owns, as read-only probes.** Watchdog liveness (pid, start time, log
freshness, lane counters). `.ufo/waves/` settlement (registry paired with
results). Kill and OOM classes from `journalctl --user` and cgroup
`memory.events`. Resource runway on the fleet and scratch roots, and
memory pressure. Lane silence grading: silent, progressing,
progressing-weak.

**Hands off.** Dispatch and orchestration (kumitate). OS package, unit,
driver, firmware, and boot state (tsukuroi) — mori reads journal and
cgroup events as fleet evidence and reports them. Endpoint health (kama).
Credential material (kagi).

Unavailable is not unhealthy. The gate is specified to say so, and the
fixtures exist to prove a fake "healthy" cannot be earned by skipping a
surface.

## Start here

1. `PROVINCE.md` — one page, including the refusal to remediate.
2. `corpus/README.md` — coverage map and named gaps.
3. `corpus/knowledge/observability-census-r1.md` — finding-id vocabulary.
4. `tools/mori-census.sh` — the census.
5. `tools/mori-silence-cases.sh` — the silence-grading oracle.
6. `SCORECARD.md` and `LOG.md`.

## Run the census

```sh
bash tools/mori-census.sh --selftest
bash tools/mori-silence-cases.sh
bash tools/mori-census.sh
```

The census header is the contract. `MORI_CENSUS: CLEAN` exits 0.
`DRIFT` exits 1. Setup and usage exit 2. `--selftest` runs in a hermetic
temp tree. A live run reads the fleet root's `.ufo/` plus host journal,
cgroup, and disk. Exit 1 with findings is the census working. It is not
a crash of the tool.

Silence states include `silent`, `progressing`, `progressing-weak`,
`young`, `not-open`, and `unavailable`. Read
`corpus/knowledge/` for the grading contract before you treat
`progressing-weak` as a synonym for dead.

## The tree

| Path | What it is |
|---|---|
| `tools/mori-census.sh` | Six-surface census |
| `tools/mori-silence-cases.sh` | Silence-case oracle |
| `corpus/knowledge/` | Contracts and per-surface notes |
| `corpus/evidence/` | Baselines and receipts |
| `corpus/lessons/` | Per-round lessons |
| `MINT.md` | The roster scan that justified the mint |

## Fleet

Minted under [shokunin](https://github.com/VeigaPunk/shokunin).
Report the finding. Leave the repair to its owner.
