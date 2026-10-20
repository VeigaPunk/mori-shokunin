# mori-shokunin

A **shokunin lane** — an expert agent for one domain, minted and trained
under the [shokunin skill](https://github.com/VeigaPunk/shokunin).

**Domain:** "Fleet & host observability (森) — detect and report fleet liveness, wave settlement, kill/OOM events and resource runway. Triggers: 'fleet health', 'did a wave die', 'why did the daemon vanish', 'watchdog liveness', 'OOM kill'. Anti-trigger: NOT dispatch/orchestration (kumitate), NOT OS package/systemd/driver state (tsukuroi), NOT endpoint health (kama)

**Wiki:** [Devin wiki](https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/mori-shokunin?branch=master)

## What's here

- `SKILL.md` — the distilled expertise: decision tables, error patterns,
  checklists (absent on lanes still in shonen seed form — see `corpus/`)
- `PROVINCE.md` — the owned domain boundary and refusals

## Round-17 observation additions

- `python3 tools/mori-seat-terminal.py --sessions-dir DIR` observes supported
  transcript terminal-at-scan metadata; aged errors are not permanent deaths or
  incident counts. It never resumes or routes seats.
- `tools/mori-census.sh` anchors jj lane history to the helper's recorded branch
  and reports off-branch HEAD / ambient-author anomalies without repairing VCS.
- `python3 tools/mori-misroot-sweep.py --fleet-root DIR --lane mori --round N`
  finds review candidates with a no-pathspec sweep; it never moves/deletes them.

The complete CLI/verdict/selftest/write-scope registry is `SKILL.md` → **Gates**;
round evidence, corrections and limitations are in `corpus/lessons/round-17.md`.
