# GtLaneChousa: C2 independent fleet ground truth, chousa-shokunin (read-only)

STATUS: complete

Scope: lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, every `*.json` under `.ufo/waves` whose top-level `schema` is `ufo-swarm-wave-dispatch-v1`. Derived manually with jq and shell. Not run: `tools/mori-wave-settlement.py`, `tools/mori-census.sh`. Not opened: `frozen/c2-expected.json` (kept independent). Leaf seat, no subagents. No edits in the chousa lane; no git or jj commands.

## 1. Result

Two dispatch-schema files out of 13 JSON files under `.ufo/waves`.

| Dispatch file (lane-relative) | wave | bytes | members | trailers parsed / unparsed | lane present / empty / missing | misrooted | filename says never dispatched | wave state (contract rules) |
|---|---|---|---|---|---|---|---|---|
| `.ufo/waves/round-25/build-dispatch.json` | `chousa-r25-build` | 137320 | 68 | 68 / 0 | 68 / 0 / 0 | 0 | no | settled |
| `.ufo/waves/round-25/falsify-run.json` | `chousa-r25-falsify` | 122017 | 68 | 68 / 0 | 52 / 0 / 16 | 0 | no | partial |

sha256 (for comparison with a tool's `dispatch_sha256`):
- `build-dispatch.json` `218d4c6ad2a8e7d5a1886b509f1d835bbc94eb539becfa06980193df784c44dc`
- `falsify-run.json` `b43ec1555eb4a4c72c0dfb4d556a217dd0d1781bcf3c99371107ee56cf3677d7`

## 2. Lane totals (chousa-shokunin)

- `*.json` under `.ufo/waves`: 13. Unreadable JSON: 0. Ignored JSON: 11.
- Dispatch-v1 (counted): 2.
- Members: 136 (68 + 68).
- Report trailers: 136 parsed, 0 unparsed, 0 unsafe.
- Lane root: 120 present, 0 empty, 16 missing (all 16 in falsify).
- Misrooted: 0. All 136 relative paths are absent under `/home/vgpnk/Projects/shokunin`.
- Filename suggests never dispatched: 0 of 2.
- Wave states: settled 1, partial 1, unsettled 0, no-spawn 0, unavailable 0.

## 3. Inventory of the 13 JSON files (top-level `schema`, jq)

- Dispatch-v1 (counted): `round-25/build-dispatch.json`, `round-25/falsify-run.json`.
- Near-miss, excluded by exact match: `round-25/falsify-plan.json` has `ufo-swarm-wave-v1`.
- Ignored, `ufo-swarm-registry-v1`: `round-25/build/swarm-registry.json`, `round-25/falsify/swarm-registry.json`.
- Ignored, no top-level `schema` key: `build-assignments.json`, `build-dispatch-attempts.json`, `build-spec.json`, `falsify-assignments.json`, `falsify-checkpoint-correction.json`, `falsify-dead-seats.json`, `falsify-full-checkpoint-correction.json`, `falsify-spec.json`.

Command: `jq -r '[input_filename, (.schema // "NULL"), (has("schema")|tostring)] | @tsv' .ufo/waves/round-25/*.json .ufo/waves/round-25/*/*.json`. Run with the bash `jq` builtin (jaq 3.1.1). The same per-file check with `~/.local/bin/jq` (jq-1.8.2) in a subprocess gave identical results.

No symlinks: `find .ufo/waves -printf '%y %p'` shows only `d` and `f` entries.

## 4. Rules applied

- Members: `.taskCall.tasks[]`, 68 per file, names unique. `registry.members` keys match the task names exactly in both files (`comm -3` empty). Both registries contain 68 `kind: spawn` members.
- Report trailer: the last non-empty line of each task must match `^Report: write your scoped findings to (\S+)$`. All 136 match. Each has exactly one such line, no duplicate paths, basename equal to member name plus `.md`, a relative path with no `..`, and no symlink targets.
- Present: regular file with size > 0. Empty: size 0. Missing: absent. No whitespace-only files.
- Misrooted: missing under the lane root, but the same relative path is a regular file under `/home/vgpnk/Projects/shokunin`. Result: 0.
- Never-dispatched filename: basename contains `preview`, `undispatched`, or `validation`. None.

## 5. The 16 missing falsify reports

Sorted: FxCapR17, FxCapR18, FxCapR21, FxCapR23, FxConnectSeparability, FxFrontierR12R13, FxFrontierR14R15, FxFrontierR16R17, FxMetaDirectory, FxMetaRecheck, FxMetaRoot, FxMetaSchedule, FxRegistryAppend, FxSkillCurrent, FxSrcFAIR, FxSrcProvO.

- Observed: the same 16 names are the keys of `.failedSeats` in `.ufo/waves/round-25/falsify-dead-seats.json` (lines 3-18). `.replacements` is 0 (line 20). Providers: `openai-codex/gpt-6-luna` 15, `zai/glm-5.3-flash` 1 (FxMetaDirectory). Each reason reads "Retry budget exhausted after 5 retries" (capacity or 429).
- Observed: `falsify/swarm-registry.json` has an entry for each of the 16 with `kind: spawn` and `agentId: ChousaR25Recovery.<name>`. `resumeSends` is empty in both dispatch files.
- Observed: no file with any of the 16 names exists in the chousa lane (`find`, excluding `.git` and `.jj`). No copy exists in any `.ufo/waves` tree of the fleet root or the 17 sibling lanes (`find` returned 0 hits).
- [INFERENCE] These are dispatched seats that failed, not seats that were never dispatched. Under the contract they are `missing`, not `dead`.

## 6. Other evidence bearing on dispatch (not part of the requested fields)

- `round-25/build-dispatch-attempts.json` (no top-level schema, so excluded) lines 3-16: attempt at 03:58:24 refused all 68 ("Background job limit reached (100)"); attempt at 04:01:24 refused 68; attempt at 04:04:25 refused 0. The note says "04:04 spawned 68/68". Build registry: 68 `spawn` members, each with an `agentId`, e.g. `ChousaR25Recovery.ExecMetaMode-3`.
- Report sizes for present files. Build: min 2059 B (CapRowR18), max 13289 B (ReviewRecheckRoot). Falsify: min 2406 B (FxAllEntryIndex), max 13302 B (FxScribeEvidence). No STATUS-only stub files (`grep '^STATUS:'` in both directories: no matches).
- Files on disk not referenced by any trailer: build has `swarm-registry.json` and `unlanded-append-race.patch`; falsify has `swarm-registry.json`. These are not counted in the totals.
- Checks repeated at different times in the session gave the same counts. Dispatch files' mtimes were not compared.

## 7. Unobserved and limitations

- A fleet-wide `find` for the 16 names timed out at 270 s and was not completed. The search was narrowed to every `.ufo/waves` tree (fleet root plus 17 lane directories). Outside those trees, absence is [INFERENCE].
- "present" uses size > 0 plus non-whitespace. The contract's rule is size > 0. The two agree on this data, since the smallest present file is 2059 B.
- The failure and attempt interpretations rest on the lane's own records. No run logs, transcripts, or `~/.omp` files were opened.

## 8. Tooling and bounds

- Installs or updates: none. jq was already present. Binaries: bash `jq` builtin = jaq 3.1.1; `~/.local/bin/jq` = jq-1.8.2; `/usr/bin/jq` = jq-1.8.2. Output digests matched across the two external binaries for both dispatch files.
- This file: first written with `STATUS: started` at `.ufo/waves/round-20/build/GtLaneChousa.md`, then overwritten with this report. No other files written.
- No edits in the chousa lane. No git or jj commands. No builds, linters, or tests. No subagents.
