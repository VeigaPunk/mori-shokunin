# ConnectMoriScope — sibling boundary vs C1/C2

Axes: C1 operability, C2 depth, C3 calibration. Freshness is tied-lowest in the contract and is not a worked claim. Sibling repos were not opened. No tool was installed.

## Evidence

Adjacent table (`PROVINCE.md:63-69`): kumitate owns wave plan/run/record/collect; mori only grades `.ufo/waves/*` filesystem settlement. Round-20 scope (`PROVINCE.md:145-154`) says that grade is report-file shape, not lifecycle settlement, and a never-spawned dispatch still reads `unsettled`.

`evidence/wave-run.json` is schema `ufo-swarm-wave-dispatch-v1` with `counts.spawn=64`, a non-null `taskCall.tasks` of 64 members, and registry `kind: spawn` with `agentId: null` on every member (header `:1-20`, ConnectMoriScope `:404-408`). Its own context says the wave is prepared and not dispatched (`:421`). Contract `:43` says the same.

`tools/mori-wave-settlement.py` walks every regular `*.json` under `.ufo/waves/` (`:100-126`) and keeps schema `ufo-swarm-wave-dispatch-v1` (`:346-349`). `no-spawn` is only `taskCall is None` (`:262-264`). `name_hint` matches the filename against `preview|undispatched|not-dispatched|validation` (`:38`, `:301-310`). `wave-run.json` matches none of those. The scanner never reads `agentId` or `counts.spawn`. Each task's last `Report:` line is a safe lane path under `.ufo/waves/round-41/w1/<Name>.md` (RevC1Walrus `:426`, ConnectMoriScope `:741`). Missing reports therefore classify as `unsettled` (exit 1); any present report flips the same file to `partial`; all 64 present flips it to `settled`. Round-20 knowledge (`corpus/knowledge/wave-settlement-r20.md:62-66`) already says that `unsettled` shape is the same for a never-spawned file and a dispatched wave whose reports were lost.

`evidence/wave-plan.json` is schema `ufo-swarm-wave-v1` and `w1/swarm-registry.json` is `ufo-swarm-registry-v1`, so both are ignored. Only `wave-run.json` is settlement-visible.

C1/C2 targets are the control receipt, not this file. `evidence/control-after.txt` records the honest counter `CONFORM=met`, three survivors `CONFORM=unmet` on `timeout_scope` only, `CONFORM_SELFTEST pass=14 fail=0`, and `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`. Contract `:37` already keeps C3 off P-C12.

## Contradiction (not a score)

The contract and the file's context say undispatched. The schema, `counts.spawn`, and `kind: spawn` say spawned. Every `agentId` is null. Settlement will report filesystem shape and will not say which of those is true.

## Proposed move

Grade C1 and C2 only from `run-r41-controls.py` receipts (`control-before.txt` / `control-after.txt`). Do not read `mori-wave-settlement.py` on `evidence/wave-run.json` as an operability or depth result: `unsettled`/`partial` is not a failed attack, and a later `settled` is not C1 met or C2 met. Leave the file bytes alone — nulling `taskCall` would be the only scanner-local `no-spawn`, and it would delete the prepared task list; renaming the file to contain `undispatched` sets `name_hint` but does not change state. Report the shape to kumitate as shared settlement evidence. Do not absorb lifecycle, result acceptance, or re-dispatch.

This improves calibration: settlement exit 1 is not a seventh mismatch beside C3's frozen six, and C3 stays on `tools/mori-round41-calibration.py`. It does not change P-C10, P-C12, or the control counters.

## Scanned, not the move

- Souji (`PROVINCE.md:69`): C1 scratch tokens are `"round-39"` (`conform.py:571-572`) while the docstring says `.ufo/waves/round-40/scratch` (`:42-44`). The honest counter and `control-after.txt` pass on the round-39 tokens. The control clone is `/tmp/mori-r41-sandbox-*` (`control-after.txt:4`). Retargeting the check to round-40 or to `/tmp` would fail the honest counter. Mori still does not reclaim; do not treat harness `TemporaryDirectory` cleanup as souji disposition.
- Kagi (`PROVINCE.md:68`): gate `_clean_env` (`mori-sources-appendonly.py:108-110`) omits `GIT_CONFIG_GLOBAL`, which `run-r41-controls.py:28` strips. The frozen counter is the control runner, so the measured C2 path does not inherit that variable. Do not open the config file.
- Source-overlap note (`PROVINCE.md:90`) covers S001–S030 only. S230/S231 were not compared to sibling registries. [UNKNOWN] whether those URLs are shared. Do not merge rows.
- Tsukuroi and kama: no C1/C2 claim in the lane artifacts above diagnoses host OS or serving health.

## Risks

A real later dispatch that reuses these bytes would be marked `duplicate_of` the prepared file and still would not be a C1/C2 receipt. Writers who treat `settled` as claim admission would undo the move. The incomparable-edit residual in P-C12 is unchanged.

## Verification

Read-only: `python3 tools/mori-wave-settlement.py scan` on the lane root must show `.ufo/waves/round-41/evidence/wave-run.json` with `name_hint` null and state outside `{settled, no-spawn}` until every trailer report exists; even then, compare that state to `evidence/control-after.txt` rather than replacing it. Do not rerun the C1/C2 counters for this finding.
