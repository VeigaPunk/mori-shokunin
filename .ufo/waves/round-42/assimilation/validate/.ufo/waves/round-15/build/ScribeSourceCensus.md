# ScribeSourceCensus — mori-r15-positive registry census

Scope: report-only. Census of the round-15 swarm registry before any gate run. No production, registry, or fleet files were edited by this lane. No builds, tests, linters, or smoke runs were executed. No tools were installed or upgraded. No `pacman` command was run; the host safety directive (sync DB about 413 packages ahead) was received and no install was needed.

## Method

JSON inspection only, via `jq` and `python3` read-only parsing of:

- `.ufo/waves/round-15/build/swarm-registry.json`
- `.ufo/waves/round-15/spec.json`
- `.ufo/waves/round-15/dispatch.json` (`taskCall.tasks`)

`task-response.json` was located and grepped for the ScribeSourceCensus job line; its full name list was not parsed programmatically.

## Before snapshot (registry as first read)

Registry header: `schema=ufo-swarm-registry-v1`, `wave=mori-r15-positive`, `createdAt=updatedAt=2026-10-20T07:28:52.423Z`, `reportDir=.ufo/waves/round-15/build`, 64 members.

Exact histogram at that snapshot (all counts over 64 members):

| field | value | count |
|---|---|---|
| kind | spawn | 64 |
| agentId | null | 64 |
| item | null | 64 |
| axes | ["coverage"] | 64 |
| milestone | "retain validated positives without fabricated totals" | 64 |

Role histogram (same snapshot):

| role | count |
|---|---|
| executor | 24 |
| scout | 8 |
| reviewer | 8 |
| critic | 8 |
| connector | 6 |
| scribe | 6 |
| sentinel | 2 |
| revenger | 2 |

Scribe members: ScribeFixtureInventory, ScribeGateDecisions, ScribeNoHarmLedger, ScribeReportContract, ScribeRoutedDebt, ScribeSourceCensus.

ScribeSourceCensus entry at that snapshot: `{"kind":"spawn","agentId":null,"role":"scribe","item":null,"axes":["coverage"],"milestone":"retain validated positives without fabricated totals"}`.

## Name-set cross-check

- Registry members: 64 (unique).
- spec.json `items`: 64 (unique). Item keys are only `name`, `prompt`, `role`.
- dispatch.json `taskCall.tasks`: 64 (unique).
- Set differences registry vs spec and registry vs dispatch: both empty.

## Later snapshot (re-read during this run)

`updatedAt` advanced to `2026-10-20T07:29:34.596Z`. At this snapshot all 64 members have a non-null `agentId` of the form `MoriR15.<name>` (ScribeSourceCensus: `MoriR15.ScribeSourceCensus`). Other fields are unchanged in this re-read. This lane did not write that change; the writer is not identified in this lane's evidence. Both states are recorded here rather than choosing one.

## Planned delta

- This lane's delta: none. Report file only.
- Wave-level registry delta observed: `agentId` null → `MoriR15.<name>` for all 64 members. This is already present in the later snapshot. No other field changed in the re-read.
- Planned but not applied by this lane: none.

## Unresolved facts

- The writer of the agentId population is not established by this lane's evidence; it was observed only as a state change between two reads.
- The `task-response.json` spawn list was grepped, not parsed; its per-name match to the registry was not independently counted here.
- The first cross-check command was backgrounded and its output was not captured; the cross-check was re-run in the foreground and its output is the one recorded above.

## Tool install record

None. No installs, upgrades, or package-manager commands were run by this lane.
