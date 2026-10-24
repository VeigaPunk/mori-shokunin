verdict: holds — A2-10 (malformed `__MONOTONIC_TIMESTAMP` → uncounted + incomplete scope, positive evidence stands): all pins in the 3 cases follow from the rule text; no failing case to rule on; no post-freeze tool change.

Seat: MoriR28.JudgeA2r10 (Amendment-A2 judge, rule A2-10). Attack rev: f2de0eedcd60d2e354da75265ea6122bc3896073. Lane: /home/vgpnk/Projects/shokunin/mori-shokunin (read-only; all runs from /fast/scratch/hyaku/mori-r28-w2/JudgeA2r10/).

## Rule text (what the pins must follow from)

- round-27/contract.md:58 (A2-10 row): "a journal record without a numeric `__MONOTONIC_TIMESTAMP` is left uncounted and makes the scope incomplete; positive evidence elsewhere still stands".
- Adopted as round-26/contract.md:186-188 (D1 wave-2 fix), superseding the setup-error rule at round-26/contract.md:168-169 (`KILLERS_UNKNOWN`, exit 2 with `error` field).
- Verdict rules round-26/contract.md:96-106: r1 `KILLER_ACTED` exit 1 — any in-scope send/escalation line or `oomd_notices` > 0, "Positive evidence stands even when the scope is incomplete" (:97-98); r2 `KILLERS_UNKNOWN` exit 2 — no positive evidence and earlyoom active but `scope_complete` false (:99-100); r4 setup error exit 2 carries an `error` field (:105).
- Scope round-26/contract.md:78 — in scope iff `__MONOTONIC_TIMESTAMP` >= `ActiveEnterTimestampMonotonic`; grammar :85-86 — `sending SIGTERM to process ` (kill.c:627) and `escalating to SIGKILL after ` (kill.c:318) are action/escalation lines.

## The three A2-10 cases (cases-a2.json @ f2de0eed, blob 7ba553d4)

1. `a2-10-malformed-action-line-uncounted` (:1164-1200): version line at 20441000 in scope (:78); one record with `__MONOTONIC_TIMESTAMP="not-a-number"` carrying a kill.c:627 send line. Pins: `KILLERS_UNKNOWN`, exit 2, `scope_complete=false`, all action counts 0. Derivation: A2-10 uncounted → sigterm 0 despite matching grammar; A2-10 → scope incomplete; verdict r2 :99-100 → UNKNOWN/2. Follows. (Same verdict/exit as the superseded setup-error rule, but the pin's `scope_complete=false`+uncounted fields and absent `error` pin distinguish it — see tool check below.)
2. `a2-10-positive-evidence-elsewhere-stands` (:1202-1242): version at 31007000 in scope; malformed-timestamp escalation record + well-formed escalation at 31007500 >= 31007000 (:78). Pins: `KILLER_ACTED`, exit 1, `scope_complete=false`, `escalations=1`. Derivation: malformed record uncounted → 1 not 2; in-scope escalation → r1 :97-98 ACTED/1 despite incomplete scope; "positive evidence elsewhere still stands" (:58). Follows.
3. `a2-10-oomd-notices-positive-malformed-records` (:1244-1284): version at 41852500 >= 41852000 in scope; two escalation-shaped records with non-numeric timestamps; `oomd_notices=2`. Pins: `KILLER_ACTED`, exit 1, `scope_complete=false`, `escalations=0`, `oomd.notices_this_boot=2`. Derivation: both records uncounted → 0; `oomd_notices` > 0 → r1 :97-98 ACTED/1. Follows.

## Evidence (all run, nothing assumed)

- Freeze selftest `.ufo/waves/round-28/evidence/c2-freeze-selftest.txt`: `PASS 30/30`, exit 0 at freeze d21b8bd (first tool run, 2026-10-22T18:51:02Z).
- `bash .ufo/waves/round-28/count-c2.sh f2de0eed`: `tool_blob=3fb78bbc`, `tool_blob_at_freeze=3fb78bbc` (identical), `frozen_blob=match`, `cases_changed_since_freeze=0`, `a2_A2-10=cases=3 distinct=3 field=3`, `a2_selftest=PASS 30/30`, `frozen32_selftest=PASS 32/32`, `C2=met`, exit 0.
- `git rev-parse d21b8bd:tools/mori-oom-killers.py` == `f2de0eed:tools/mori-oom-killers.py` = 3fb78bbc; `git diff`/`git log d21b8bd..f2de0eed` on the tool path: empty. `git merge-base --is-ancestor`: freeze is ancestor of target.
- `--inputs` runs on a temp extract of f2de0eed's tool (never the lane): for each of the 3 cases I fed the case's `inputs` object; observed verdict, exit, and all 12 pinned fields each match with zero mismatches; `scope_complete=False` in all three; no `error` field in output — the tool is on the D1 uncounted/incomplete-scope path, not residual setup-error behavior from 278f02e4.

## Rulings for failing cases

None — all three A2-10 cases pass at the attack rev and every pin derives from the rule text. No `tool error` / `case error` / `unclear text` ruling is owed.

## Post-freeze tool change check

Vacuous: tool blob identical freeze→target, so there is no change to check against the rule text. No KILLER_ACTED pin (or any pin) flipped on either case file: `PASS 30/30` on cases-a2.json and `PASS 32/32` on the frozen round-26 cases at f2de0eed (counter output above), confirmed by direct `--inputs` runs.

## Residual risk / gaps

- A2-10's "makes the scope incomplete" is unconditional in the rule text; the cases pin `scope_complete=false` with the version line in scope, consistent with that reading and with r26 :93-94 (version-in-scope is only a necessary condition for true). No tension found; an alternative reading (malformed record merely uncounted, scope decided by version line alone) would make case 1's pin wrong, but that reading contradicts the explicit clause.
- `grammar` field (`verified-1.9.0`/`unverified`) is not pinned by any A2-10 case; not checked beyond verdict consistency.
- I judged only A2-10 rows; other rule ids are other seats' scope.

Tooling: none installed (git, python3 already present; pacman transactions paused host-wide).
