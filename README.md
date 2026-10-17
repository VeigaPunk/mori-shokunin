# mori-shokunin — 森

**Fleet and host observability.** Whether the fleet, its waves, and its
host are alive and progressing.

**Detection and report only. This lane never remediates.**

A **shokunin lane**: an expert agent for one domain, minted and trained
under the [shokunin skill](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**. Promotion is a named non-author review of
[`SHONEN.md`](SHONEN.md), never self-attestation.

This lane answers: *is the watchdog alive, did the wave settle, did
something get killed, is there runway, and was a lane silent — as
observations, not as a license to fix them?*

## Domain

From [`PROVINCE.md`](PROVINCE.md), all **read-only probes**:

| Surface | What “alive” means here |
|---|---|
| Watchdog | pid, start time, log freshness, `.ufo/state/*.round` vs ledger |
| Waves | `.ufo/waves/*` registry/dispatch × results/closeout |
| Kills | `journalctl --user` OOM/kill class counts; cgroup `memory.events` |
| Runway | disk on fleet + scratch roots; PSI / fill / `memory.peak` |
| Silence | silent / progressing / progressing-weak / young / not-open / unavailable |
| tmux | fleet-relevant vs foreign by pane cwd; freshness is info, not DRIFT |

**Refuses:** dispatch mechanism (→
[kumitate](https://github.com/VeigaPunk/kumitate-shokunin)); OS package /
systemd / driver / boot *ownership* (→
[tsukuroi](https://github.com/VeigaPunk/tsukuroi-shokunin) — mori reads
journal and cgroup events as fleet evidence and reports them); endpoint
health (→ [kama](https://github.com/VeigaPunk/kama-shokunin)); secrets
(→ [kagi](https://github.com/VeigaPunk/kagi-shokunin)).

A positive cgroup `oom_kill` is a **cumulative counter**. It does not
identify the killed PID, the event time, or fleet membership.

## What's here

| Path | Role |
|---|---|
| [`SKILL.md`](SKILL.md) | decision table, error patterns, expected output lines |
| [`PROVINCE.md`](PROVINCE.md) | owned probes and refusals |
| [`tools/mori-census.sh`](tools/mori-census.sh) | live census + hermetic selftest + pin/drift |
| [`tools/mori-silence-cases.sh`](tools/mori-silence-cases.sh) | silence-grading fixtures |
| [`corpus/`](corpus/) | knowledge, lessons, evidence |
| [`SCORECARD.md`](SCORECARD.md) · [`LOG.md`](LOG.md) · [`SHONEN.md`](SHONEN.md) | axes, trail, promotion |

## The census

```sh
bash tools/mori-census.sh --help
bash tools/mori-census.sh --selftest
bash tools/mori-census.sh                 # live, read-only
bash tools/mori-census.sh --pin   path    # write a normalized behavioral baseline
bash tools/mori-census.sh --drift path    # byte-compare against that baseline
```

Verdict: `MORI_CENSUS: CLEAN|DRIFT`. Exit `0` / `1` / `2`. Live mode
creates no files.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
