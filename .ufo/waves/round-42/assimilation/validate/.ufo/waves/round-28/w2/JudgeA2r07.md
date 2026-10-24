# JudgeA2r07 — A2-07 per-invocation dry-run

Verdict: **holds** — attacked rule A2-07 (`round-27/contract.md:55`: "dry-run applies per invocation (split at each version line): one dry-run invocation does not zero another invocation's real sends"). All three A2-07 cases pin only values that follow from the rule text; the freeze selftest passed 30/30 and reproduces at the attack revision; the tool was not changed after the freeze.

## Scope

- Rule text: `.ufo/waves/round-27/contract.md:55` (adopted at `.ufo/waves/round-26/contract.md:180-184`, "Wave-2 fixes ... dry-run is now applied per earlier invocation (split at each version line)").
- Companion rules exercised by the pins: scope `>=` boundary `round-26/contract.md:78-79`; version line = invocation start `:82`; send/escalation grammar `:85-86`; dry-run flag `:89`; `scope_complete` `:93`; `KILLER_ACTED` `:97-98`; `KILLERS_QUIET` `:102-104`; dry-run send accounting (A6) `:166-167`; `earlier_invocation_send_lines` `:176-178`.
- Cases: `tools/fixtures/mori-oom-killers/cases-a2.json` at `f2de0ee` (blob `7ba553d4`, same as freeze blob).

## Case a2-07-earlier-real-then-current-dryrun (blob :795-855)

Two invocations: earlier real at ts 30M, current dry-run at ts 42M = `ActiveEnterTimestampMonotonic`. Every pin follows:

- `verdict KILLERS_QUIET`, `exit 0` (:834-835): no in-scope real send (the only in-scope send is a dry-run send, "never positive evidence", `round-26/contract.md:167`); `oomd_notices` 0; earlier real sends don't change verdict for an active earlyoom (`:178`); scope complete → QUIET under `:102-104`.
- `earlyoom.dryrun: true` (:847): `dryrun mode enabled` logged in the current invocation (`:89`).
- `dryrun_send_lines: 1` (:848): exactly one `sending SIGTERM to process` line in the dry-run invocation (`:166-167`); the `dryrun, not actually sending any signal` line is not a send.
- `earlier_invocation_send_lines: 2` (:849): two real sends at ts 30M < scope start 42M; A2-07 pins that the current dry-run does not zero them. This is the discriminating pin.
- `actions.*` all 0 (:842-846), `scope_complete: true` (version line at boundary, `:78`, `:93`), `state/version/grammar/thresholds:null` (no threshold lines logged), `oomd.*` — all follow `:90-95`.

`--inputs` rerun at `f2de0ee` bytes: output matches every pin exactly; verdict `KILLERS_QUIET`, exit 0.

## Case a2-07-earlier-dryrun-then-current-real (blob :856-905)

Earlier dry-run invocation (ts 40M, no send lines), current real invocation at ts 52M = boundary. Pins:

- `verdict KILLER_ACTED`, `exit 1` (:887-888): in-scope `sending SIGTERM to process` + `escalating to SIGKILL` (`:97-98`). The earlier dry-run must not zero these — the reverse-direction pin of A2-07.
- `actions.sigterm: 1`, `sigkill: 0`, `escalations: 1`, `kill_failed: 0`, `low_memory_warnings: 0` (:895-899): grammar `:85-87`.
- `scope_complete: true` (:891 area): version line stamped exactly at `ActiveEnterTimestampMonotonic` is in scope (`:78`, inclusive).
- `state/version/grammar/thresholds:null`, `oomd.state: active`, `notices_this_boot: 0` — all follow `:90-95` and the given show texts.

`--inputs` rerun: matches all pins; verdict `KILLER_ACTED`, exit 1. `earlyoom.dryrun` is unpinned here but observed `false` — correct, since the dry-run flag belongs to the earlier invocation only.

## Case a2-07-three-invocations-dryrun-in-the-middle (blob :906-994)

Real (50M) → dry-run (55M, no sends) → current real (63M = boundary). Pins:

- `verdict KILLER_ACTED`, `exit 1` (:973-974): in-scope real SIGTERM+SIGKILL sends (`:97-98`). The middle dry-run must not zero the current real sends — the double-split pin.
- `earlier_invocation_send_lines: 2` (:989): the earliest invocation's two real sends; the middle dry-run contributes none; the `sending SIGTERM when mem avail ...` threshold lines (`:83-84`) are not send lines and are correctly excluded.
- `actions.sigterm: 1`, `sigkill: 1`, `escalations: 0` (:984-986): only current-invocation sends.
- `thresholds` 10.0/10.0/5.0/5.0: threshold lines in the current invocation parsed per `:83-84`.
- `scope_complete: true`, `state/version/grammar`, `oomd.*` — follow `:90-95`.

`--inputs` rerun: matches all pins; verdict `KILLER_ACTED`, exit 1. `earlyoom.dryrun` unpinned, observed `false` — correct.

## Failing cases / rulings

None. Freeze evidence `c2-freeze-selftest.txt:3` shows `MORI_OOM_KILLERS_SELFTEST: PASS 30/30, exit=0`. Rerun at `f2de0ee` bytes (temp extract `/fast/scratch/hyaku/mori-r28-w2/JudgeA2r07/extract/`): `PASS 30/30, exit=0`. No `tool error` / `case error` / `unclear text` ruling is owed.

## Post-freeze tool change check

- `git rev-parse d21b8bd:tools/mori-oom-killers.py` = `f2de0ee:tools/mori-oom-killers.py` = `3fb78bbc`; both case files byte-identical too (`cases-a2.json` `7ba553d4`, `cases.json` `5b4dcee7`). `git log d21b8bd..f2de0ee -- tools/mori-oom-killers.py tools/fixtures/mori-oom-killers/` is empty; `merge-base --is-ancestor` confirms `d21b8bd` is an ancestor of `f2de0ee`. The tool was NOT changed after the freeze.
- Empirically confirmed anyway: `--selftest` at the attack-rev extract → `cases-a2.json` PASS 30/30, `cases.json` PASS 32/32 (the `cases.json` pass set includes `KILLER_ACTED` cases; the tool is byte-identical, so no `KILLER_ACTED` could have been turned into anything else on either file).

## Residual risk / gaps

- `earlyoom.dryrun` is pinned only in case 1. Cases 2-3 don't pin it (observed `false`, correct); a tool bug reporting a stale global dry-run flag on the current invocation would still break the pinned action counts, so coverage is adequate.
- No A2-07 case pins where send lines of an *earlier dry-run* invocation land (both earlier dry-run invocations here logged zero send lines). `round-26/contract.md:176` counts "send and escalation lines" without a dry-run exclusion, while `:167` says dry-run sends are never positive evidence — for an inactive earlyoom that collision could matter. [INFERENCE: no case or rule text fully resolves that shape; not a defect in these cases.]
- `earlyoom.process_group_lines` unpinned in all three cases; observed 0, correct.

## Tooling

No installs or upgrades needed; used preinstalled `git`, `jq`, `python3`, `tar`. Lane untouched: all tool runs against `/fast/scratch/hyaku/mori-r28-w2/JudgeA2r07/extract/` (git archive of `f2de0ee`); no writes outside this report and that scratch dir.
