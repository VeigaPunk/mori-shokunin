# GtLaneRevenger: C2 independent ground truth, lane `revenger-shokunin`

STATUS: complete. Manual jq and shell checks. Read-only on the lane and the fleet root. No tool under test was run, no lane file was edited, nothing was installed or updated.

## Rules applied (frozen contract, C2 section, verbatim)
- Discovery: regular `*.json` under `<lane>/.ufo/waves/`, symlinks not followed. Dispatch file = top-level `schema == "ufo-swarm-wave-dispatch-v1"`.
- Members: `taskCall.tasks[*]`.
- Report path: last line of `task` matching `^Report: write your scoped findings to (\S+)$`. Unparsed if no match. Unsafe if absolute or containing `..`.
- Member status under lane root: `present` (regular, non-symlink, size > 0), `empty` (size 0), `missing`. `misrooted` = missing under the lane root but the same relative path is a regular file under `/home/vgpnk/Projects/shokunin`.
- Wave state: `unsettled` = 0 present with at least 1 member.
- The frozen oracle `frozen/c2-expected.json` was not read, to keep this check independent.

## 1. Discovery under `revenger-shokunin/.ufo/waves/`
- `find -printf` gives 27 entries: 3 directories (`.`, `fleet-round-1-interactive/`, `kaika-r1/`), 9 `*.json` (all regular files, 0 symlinks), and 15 `*.md` (all in `kaika-r1/`, which has 0 JSON).
- `/usr/bin/jq -e .` parses all 9 (rc 0 each), so `unreadable_json = 0`.

| file (relative to `.ufo/waves/`) | bytes | top-level `.schema` | class |
|---|---|---|---|
| `fleet-round-1-interactive/rendered-undispatched.json` | 35955 | `ufo-swarm-wave-dispatch-v1` (line 2) | **dispatch** |
| `fleet-round-1-interactive/audit-spec.json` | 12826 | none | ignored |
| `fleet-round-1-interactive/coverage-remeasurement.json` | 3259 | none (keys are two 40-hex SHAs) | ignored |
| `fleet-round-1-interactive/inherited-input-shapes.json` | 2981 | none | ignored |
| `fleet-round-1-interactive/inherited-preservation.json` | 1022 | none | ignored |
| `fleet-round-1-interactive/local-acceptance.json` | 13941 | none | ignored |
| `fleet-round-1-interactive/routing-assessment-run.json` | 1681 | none | ignored |
| `fleet-round-1-interactive/routing-contract.json` | 1670 | none | ignored |
| `fleet-round-1-interactive/wave-plan-run.json` | 38123 | none | ignored |

## 2. Per-file totals: `fleet-round-1-interactive/rendered-undispatched.json`

| measure | value |
|---|---|
| wave | `revenger-r1-interactive-audit` |
| `.counts` spawn / resume / total | 32 / 0 / 32 |
| members (`.taskCall.tasks[*]`) | 32 (`.taskCall` non-null, so not `no-spawn`) |
| distinct member names | 32; equal to the key set of `.registry.members` (32) |
| agents | reviewer 17, critic 12, connector 1, scribe 1, sentinel 1 |
| trailer parsed / unparsed | 32 / 0 |
| unsafe | 0 |
| present / empty / missing (lane root) | 0 / 0 / 32 |
| misrooted (fleet root) | 0 |
| wave state (contract rule) | `unsettled` |
| `.resumeSends` | `[]` (line 611) |
| filename suggests never dispatched | **yes**: token `undispatched` |

All 32 trailers equal `.ufo/waves/fleet-round-1-interactive/reviews/<member>.md`. Checked with `jq`: 32/32 match this template, 32 distinct, exactly one `Report:` line per task, no `..`.

## 3. Lane totals (`revenger-shokunin`)

| measure | value |
|---|---|
| JSON files under `.ufo/waves` | 9 |
| dispatch-schema files | 1 |
| `ignored_json` (no dispatch schema) | 8 |
| `unreadable_json` / symlinks skipped | 0 / 0 |
| waves | 1 |
| wave states | `unsettled` 1; `settled` 0; `partial` 0; `no-spawn` 0; `unavailable` 0 |
| members | 32 |
| trailers parsed / unparsed | 32 / 0 |
| unsafe | 0 |
| present / empty / missing | 0 / 0 / 32 |
| misrooted | 0 |
| filename-flagged never-dispatched | 1 (`rendered-undispatched.json`); `preview` 0; `validation` 0 |

Per the contract's exit rule, a scan of this lane would exit 1 (`unsettled`). [INFERENCE: applied by hand, no tool run.]

## 4. Member table (dispatch order; all rows identical in status)

Status for every row: `missing` under lane root; `misrooted` = no; report path is the template in section 2.

| # | member | agent | # | member | agent |
|---|---|---|---|---|---|
| 1 | PeHeader55 | reviewer | 17 | ScenarioLaneRoot | reviewer |
| 2 | PeDirectories55 | reviewer | 18 | ScenarioForeignCwd | reviewer |
| 3 | PeUnicode55 | reviewer | 19 | ScenarioUnicodeCopy | reviewer |
| 4 | PePayloads55 | reviewer | 20 | ScenarioArtifactForgery | critic |
| 5 | PeGroup55 | reviewer | 21 | ScenarioCommandForgery | critic |
| 6 | PeMissing56 | reviewer | 22 | ScenarioCandidateForgery | critic |
| 7 | PeSize57 | reviewer | 23 | ScenarioSizeForgery | critic |
| 8 | ReplayLocalReads | reviewer | 24 | ScenarioNameLocationForgery | critic |
| 9 | ReplayArtifactPin | critic | 25 | ScenarioEntryLocationForgery | critic |
| 10 | ReplayCommandPin | critic | 26 | ScenarioIsolationSafety | sentinel |
| 11 | ReplayReceipt55 | reviewer | 27 | InputPreservationLedger | scribe |
| 12 | ReplayReceipt56 | reviewer | 28 | ReplayScoreCalibration | critic |
| 13 | ReplayReceipt57 | reviewer | 29 | ReplayCoverageTaxonomy | reviewer |
| 14 | ReplayEnvelopeLimits | critic | 30 | ReplayHistoryErrata | critic |
| 15 | ReplayWholeNormalized | reviewer | 31 | ReplayContinuationContract | reviewer |
| 16 | ReplayBuiltinMutants | critic | 32 | ReplayCrossAxisConnector | connector |

## 5. Corroboration (observed, read-only)
- `fleet-round-1-interactive/wave-plan-run.json:6` → `"dispatch_started": false`. Its `.command` is `ufo-swarm-wave.mjs plan --spec …audit-spec.json --route-families`, exit 0.
- `fleet-round-1-interactive/routing-contract.json:2` → `"verdict": "could-not-evaluate"`. Line 3 `finding_id: required_role_alias_binding_missing`, line 4 `exit_code: 2`. Line 7 `"planned_lanes": 32`, line 8 `"dispatched_lanes": 0`, line 9 `"registry_persisted": false`.
- `rendered-undispatched.json:611` → `"resumeSends": []`.
- `.ufo/waves/fleet-round-1-interactive/reviews/` does not exist under the lane root (`test -d` → no). The same relative path does not exist under the fleet root either (`ls` → no such file).

## 6. Bounded search for copies elsewhere (informational; not part of the misrooted rule)
- `find /home/vgpnk/Projects/shokunin -maxdepth 6`, pruning `node_modules`, `.git`, `.jj`, looking for the 32 member basenames (`Pe*` 7 explicit, `Replay*.md`, `Scenario*.md`, `InputPreservationLedger.md`).
- Hits: 6 unrelated files (`kaidoku-shokunin/.ufo/waves/round-20/w2/Replay{WasmCompare,WasmInspect,Rizin,ObjdumpArch,Harmony}.md` and `kama-shokunin/.ufo/waves/round-14/advice/ReplayKnowledge.md`). None is one of the 32 member report names.
- An unbounded search timed out at 180 s, so copies deeper than depth 6 are unobserved. [INFERENCE: none exist.]

## 7. Observations for the integration owner (not acted on)
1. A rendered, never-dispatched dispatch file (`taskCall` non-null, `dispatch_started: false`) gets `unsettled` under the contract's state rules. That is the same state as a dispatched wave whose reports were lost. The contract's state set has no never-dispatched state, so the tool cannot tell these apart. Flagging for a decision, not fixing.
2. `kaika-r1/` holds 15 `.md` files and no dispatch JSON. It contributes 0 members to C2 totals.

## 8. Environment and tooling
- Installs or updates performed: none.
- The persistent shell's `jq` is a shell builtin that reports `jaq 3.1.1`. All counts above were recomputed with `/usr/bin/jq` (jq-1.8.2, system package). The first pass with the builtin gave the same schema detection and the same 32 tasks.
- Not run: `tools/mori-census.sh`, `tools/mori-wave-settlement.py`, lane selftests, builds or linters.
- Not opened: no retained transcripts, no `~/.omp` session logs.
