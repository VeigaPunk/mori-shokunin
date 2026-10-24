# JudgeA2r05 — Amendment-A2 judge, rule A2-05 (round-28 wave 2)

**Verdict: holds** — all three A2-05 cases in `tools/fixtures/mori-oom-killers/cases-a2.json` at `f2de0eedcd60d2e354da75265ea6122bc3896073` pin values that follow from the rule text, the tool reproduces every pinned value, and the L1 made no tool change after the freeze.

Scope: read only the rule text (round-27 contract :47-58; round-26 contract incl. :152-200), the A2-05 cases at `f2de0eed`, the freeze selftest evidence, and the tool's `--inputs` output run from a temp extract of `f2de0eed`. Nothing in the lane was edited except this Report file; no tooling was installed or updated (python3 and git preinstalled sufficed).

## Rule text (cited lines verified verbatim)

- round-26 `.ufo/waves/round-26/contract.md:173-174`: "`ActiveEnterTimestampMonotonic` missing or `0` leaves the invocation unbounded, so `scope_complete` is false (before this, a version line alone set it true)."
- round-27 `.ufo/waves/round-27/contract.md:53`: "A2-05 | `ActiveEnterTimestampMonotonic` missing or `0` leaves the invocation unbounded: `scope_complete` false" — same rule, matching id.
- Supporting text used by the cases: scope definition round-26:78-79 (lines with `__MONOTONIC_TIMESTAMP` ≥ `ActiveEnterTimestampMonotonic` of the current invocation); state vocabulary round-26:90-91 (`active`/`inactive`/`absent`/`unavailable`); `scope_complete` "true only when the version line of the current invocation is inside the scope" round-26:92-93; grammar version line `main.c:161` form round-26:82; verdict 1 round-26:97-98 (`KILLER_ACTED` exit 1 on `oomd_notices` > 0, "Positive evidence stands even when the scope is incomplete"); verdict 2 round-26:99-101 (`KILLERS_UNKNOWN` exit 2, incl. "earlyoom active but `scope_complete` false"); verdict 3 round-26:102-104 (`KILLERS_QUIET` exit 0, "An inactive or absent killer reports `actions: null`").

## Case-by-case (3 cases with `rule: A2-05`; file holds 30 cases, 3 per rule id)

### a2-05-monotonic-zero-active-quiet
- Pins: `KILLERS_UNKNOWN`, exit 2; `earlyoom.state=active`, `earlyoom.scope_complete=false`, `earlyoom.dryrun=false`, `oomd.state=inactive`, `oomd.notices_this_boot=0`.
- `ActiveEnterTimestampMonotonic=0` in the show text → unbounded → `scope_complete` false (round-26:173-174, round-27:53). `ActiveState=active` → state `active` (round-26:90-91). Journal holds only a version line (round-26:82 grammar) and threshold lines — no action lines, `oomd_notices=0` → no positive evidence, so verdict 2 applies: active but scope false → `KILLERS_UNKNOWN` exit 2 (round-26:99-101). No `dryrun mode enabled` line → `dryrun=false` (round-26:87 dry-run flag rule). Every pinned value follows.
- Deliberate non-pinning of `earlyoom.version`/`grammar`/`thresholds.*`/`actions.*` is honest: round-26:78-79 with :173-174 do not decide which lines lie in scope when the start is unknown; the case pins nothing the contract leaves open.

### a2-05-monotonic-missing-active-oomd-notices
- Pins: `KILLER_ACTED`, exit 1; `earlyoom.state=active`, `scope_complete=false`, `dryrun=false`, `oomd.state=active`, `oomd.notices_this_boot=3`.
- Show text has no `ActiveEnterTimestampMonotonic` line at all — "missing" arm of round-26:173-174 → `scope_complete` false. `ActiveState=active` on both shows → both states `active` (round-26:90-91). `oomd_notices=3 > 0` is positive evidence and "Positive evidence stands even when the scope is incomplete" (round-26:97-98) → `KILLER_ACTED` exit 1. All pinned values follow; the earlyoom escalation line's scope membership is left unpinned and the verdict correctly does not depend on it.

### a2-05-monotonic-zero-inactive-quiet
- Pins: `KILLERS_QUIET`, exit 0; `earlyoom.state=inactive`, `scope_complete=false`, `earlyoom.actions=null`, `oomd.state=inactive`, `oomd.notices_this_boot=0`.
- AETM=0 → `scope_complete` false (round-26:173-174). `ActiveState=inactive` → state `inactive` (round-26:90-91). No positive evidence anywhere (no action lines, oomd 0), and the unit is not active, so verdict 2's "active but `scope_complete` false" trigger does not fire → verdict 3 "otherwise" → `KILLERS_QUIET` exit 0, with `actions: null` for an inactive killer (round-26:102-103). All pinned values follow.

## Tool behavior at the freeze (temp extract of `f2de0eed`)

Commands run in `/fast/scratch/hyaku/mori-r28-w2/JudgeA2r05/ex` (populated by `git -C <lane> archive f2de0eedcd60d2e354da75265ea6122bc3896073 | tar -x -C …`; read-only on the lane):

- `python3 -I -B tools/mori-oom-killers.py --selftest --cases tools/fixtures/mori-oom-killers/cases-a2.json` → `MORI_OOM_KILLERS_SELFTEST: PASS 30/30`, exit 0. Matches the freeze evidence `.ufo/waves/round-28/evidence/c2-freeze-selftest.txt` (same line, `exit=0`).
- `--selftest --cases tools/fixtures/mori-oom-killers/cases.json` → `PASS 32/32`, exit 0 (round-26 frozen file still green).
- `--inputs` on each of the three A2-05 cases' inputs objects: verdict, process exit, and every pinned field matched exactly — `a2-05-monotonic-zero-active-quiet` → `KILLERS_UNKNOWN` rc 2, field mismatches none; `a2-05-monotonic-missing-active-oomd-notices` → `KILLER_ACTED` rc 1, none; `a2-05-monotonic-zero-inactive-quiet` → `KILLERS_QUIET` rc 0, none.

No failing case exists for A2-05, so no `tool error` / `case error` / `unclear text` ruling was required.

## Post-freeze change check

- Lane `HEAD` is `f2de0ee` (`git rev-parse --short HEAD` → `f2de0ee`), i.e. the attack revision is the tip: `git log f2de0ee..HEAD -- tools/mori-oom-killers.py tools/fixtures/mori-oom-killers/` is empty, and `git diff --stat HEAD` on those paths is empty. The L1 changed neither the tool nor either case file after the freeze; the conditional KILLER_ACTED-stability check is vacuously satisfied.
- Case-file immutability: blob of `cases-a2.json` at `d21b8bd38b1bf72ec903a19ed543c615564e8278` (its own freeze commit) and at `f2de0eed` are identical (`7ba553d45e3b00d507e57132cc3c28fb140f83fd`), and `git merge-base --is-ancestor d21b8bd3 f2de0eed` → ancestor ok (freeze-before-tool order holds).
- The freeze evidence's committed claim was independently reproduced, not taken on trust.

## Residual risk and verification gaps

- I did not read the tool source; per assignment the judgment is rule text vs pinned values plus observed `--selftest`/`--inputs` behavior, which is sufficient for A2-05 (no source-level claim is made).
- `--inputs` exercises the pure reader only; live-mode paths are out of scope per round-27 contract:56-57 ("The live-mode readability probe (A1c) is out of scope").
- The `why` fields cite `contract.md:78-79` for the scope lines; line 78 is the scope sentence (its continuation ends at 79) — consistent.
- [INFERENCE] none beyond the above; all verdict-relevant facts were observed by running the tool at the pinned revision.

Report ends. Seat JudgeA2r05, 2026-10-22.
