# mori-shokunin — 森

The question this lane answers is whether the fleet, its waves, and its host are alive and progressing (`PROVINCE.md`).

**Rank:** `SHONEN.md` is a promotion checklist and every box is `[ ]`. `MINT.md` says the roster row is withheld until probation rounds are verified. That is not a promotion.

## Owns / refuses

Owns read-only probes: watchdog liveness (pid, start time, log freshness, lane counters), `.ufo/waves/*` settlement, kill and OOM event classes from `journalctl --user` and cgroup `memory.events`, resource runway, and lane silence grading (`PROVINCE.md`).

Refuses dispatch and orchestration (kumitate), OS package and unit and driver and boot state (tsukuroi), endpoint health (kama), and credential material (kagi). Detection and report only. Never remediation (`PROVINCE.md`).

## Start here

`tools/mori-census.sh` is read-only in live mode and may `DRIFT` off this host. The header's hermetic proof is `--selftest`, which writes only under its temp directory.

```sh
bash tools/mori-census.sh --selftest
```

Live use, when you intend a read-only census and not a mutation:

```sh
bash tools/mori-census.sh
```

Verdict `MORI_CENSUS: CLEAN` or `DRIFT`. Exit `0` CLEAN, `1` DRIFT, `2` setup or usage. `--pin` writes a baseline file you name. `--drift` compares. Neither remediates (`tools/mori-census.sh` usage text). `bash tools/mori-silence-cases.sh` is the hermetic counting driver for silence grading; it builds temp git fixtures and does not take a `--selftest` flag of its own (header).

## How to read the corpus

`corpus/README.md` is the coverage map, one row per surface family and per verdict-machine round. It is heavily line-cited (round drafts cite ranges such as `corpus/README.md:11-12` and later rows), so it was not reflowed. `corpus/knowledge/` holds the surface and silence notes. `corpus/lessons/` holds the class lessons. `corpus/evidence/` holds receipts. `corpus/QUALITY.md` is the admission bar.

## Map

| Path | What it is |
|---|---|
| `PROVINCE.md` | Observe-and-report boundary |
| `SKILL.md` | Probe checks, including watchdog, runway, and tmux |
| `SHONEN.md` | Promotion checklist, boxes unchecked |
| `MINT.md` | Mint cause; roster row withheld |
| `LOG.md` | Append-only record |
| `SCORECARD.md` | Axis verdicts |
| `AGENTS.md` | Operating rules |
| `corpus/` | Knowledge, lessons, evidence, index |
| `tools/mori-census.sh` | Census |
| `tools/mori-silence-cases.sh` | Silence-grading cases |
| `.ufo/` | Round machinery |

## Neighbors

kumitate (dispatch mechanism), tsukuroi (OS state; mori reads journal and cgroup as fleet evidence and does not own them), kama (endpoints), kagi (credentials). `MINT.md` records the roster scan that rejected those fits.

Fleet protocol: [VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin).
