agree — all five behavior-bearing fix hunks are pinned by frozen cases; no mutant survived.

## Scope and detector

Tested the `ad0f04745ced2194e58c22a0d6b38131bee3e230` measured-tip tool in the required scratch clone; its tool blob is `1a70bddc66e4510038a6e5e887e7fc872a235ed6` (lane `tools/mori-oom-killers.py`, fix hunks at `.ufo/waves/round-30/evidence/fix-tool.diff:3-83`). Detector for every run: `python3 -I -B tools/mori-oom-killers.py --selftest --cases tools/fixtures/mori-oom-killers/<case-file>`; ran separately against all five named case files, pristine, each single-hunk mutant, and after each restoration.

Pristine output: `cases.json PASS 32/32`, `cases-supplementary.json PASS 32/32`, `cases-a2.json PASS 30/30`, `cases-a2-r29.json PASS 24/24`, `cases-a2-r30.json PASS 8/8`; all exit 0 (`/fast/scratch/hyaku/mori-r30-w2/MutToolFix/baseline.txt:2-20`). Thus mutant failures below are killed mutants, not baseline failures.

## One-hunk-at-a-time results

All mutant SHA256 values below were captured with `sha256sum` (`/fast/scratch/hyaku/mori-r30-w2/MutToolFix/hashes.txt:1-12`). Every mutant retained the three older-suite passes (`32/32`, `32/32`, `30/30`) and `cases-a2-r30.json PASS 8/8`; failures were exclusively in `cases-a2-r29.json`.

| Diff hunk | Single behavior mutation | Mutant SHA256 | Actual failing output | Verdict |
|---|---|---|---|---|
| `fix-tool.diff:3-24` | Restored the active-only outer journal gate (`if earlyoom_state == "active" and journal is not None`). | `2a8beb99eef1c760f0582b9b5a476686405eb1e040f17dcacf02513c4b5b115a` | `FAIL 21/24`; three inactive cases fail: `r29-a2-10-inactive-lone-missing-stamp`, `r29-a2-10-failed-stamped-positive`, `r29-a2-10-not-found-earlier-stamped-positive` (`hunk-1-mutant.txt:14-29`). | Killed / pinned |
| `fix-tool.diff:25-40` | Reverted the nonzero-boundary `elif` branch to `else: scope_known = True`, without setting `scope_bounded`. | `fd8c889dfd341fe04337b65fec96da8fca9eccab8bfe50b4d5f1f3d8f5fca8a1` | `FAIL 21/24`; the same three inactive cases expect non-null `dryrun_send_lines` and `process_group_lines` (`hunk-2-mutant.txt:14-22`). | Killed / pinned |
| `fix-tool.diff:41-55` | Restored `version = None` and `grammar = GRAMMAR_UNVERIFIED` for non-active units. | `24cda8a06337ac3156b42579d41bb83c9d32a457021b953336e179756813e168` | `FAIL 21/24`; the same three inactive cases expect version `1.9.0` and grammar `verified-1.9.0` (`hunk-3-mutant.txt:14-22`). | Killed / pinned |
| `fix-tool.diff:56-66` | Reverted the diagnostic-field guard to `if actions is None:`. | `20c5b14dd09476983f4d5bc76acedae70c04ba60f2bf6bd27e0e6e3e2ead156a` | `FAIL 21/24`; the same three inactive cases expect non-null `dryrun_send_lines` and `process_group_lines` (`hunk-4-mutant.txt:14-22`). | Killed / pinned |
| `fix-tool.diff:67-83` | Reverted the `acted` condition to count only `earlier_send_lines`, omitting scoped SIGTERM/SIGKILL/escalations. | `d30155b4048582233dcf909d501a32e077c76d03edaedb550fad2f8702ea9af0` | `FAIL 23/24`; `r29-a2-10-failed-stamped-positive` becomes `KILLERS_UNKNOWN` (exit 2), expected `KILLER_ACTED` (exit 1) (`hunk-5-mutant.txt:14-18`). | Killed / pinned |

No unpinned hunk. The new round-30 file remained `PASS 8/8` under every mutant; it did not kill these probes. The frozen round-29 suite supplies the pins above.

## Restoration

Pristine tool SHA256 before mutation: `9c88ef272dbe3e07eb87e40f10faaedb82584df0d9f21e78e3d8764400da0fe1`. After restoring each hunk, SHA256 returned to that exact value (`hashes.txt:2-12`) and the same five-case detector returned `PASS 32/32`, `PASS 32/32`, `PASS 30/30`, `PASS 24/24`, `PASS 8/8`, all exit 0; final restored run is recorded at `/fast/scratch/hyaku/mori-r30-w2/MutToolFix/hunk-5-restored.txt:2-20`. This matches the pristine hash, confirming exact-byte restoration.

Tool installs/updates: none.