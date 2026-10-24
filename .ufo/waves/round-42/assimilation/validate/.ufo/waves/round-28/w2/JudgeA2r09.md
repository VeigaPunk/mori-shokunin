# JudgeA2r09 — A2-09 ruling

holds — all three A2-09 cases pin only what the rule text and frozen interface require; all pass; no post-freeze tool change exists.

## Scope attacked

Rule A2-09: "send lines of a removed (`not-found`) earlyoom unit this boot are positive evidence"
(.ufo/waves/round-27/contract.md:57, adopted at .ufo/waves/round-26/contract.md:182). Three cases in
tools/fixtures/mori-oom-killers/cases-a2.json at f2de0eedcd60d2e354da75265ea6122bc3896073:
`a2-09-removed-unit-single-sigterm-send`, `a2-09-removed-unit-two-invocations-mixed-sends`,
`a2-09-removed-unit-three-sends-oomd-active` (30 cases total, 3 rule A2-09; counted via python json).

## Pass/fail status

- Freeze evidence: `.ufo/waves/round-28/evidence/c2-freeze-selftest.txt:3` — `PASS 30/30` at
  d21b8bd38b1bf72ec903a19ed543c615564e8278.
- Re-run at attack target (temp extract `/fast/scratch/hyaku/mori-r28-w2/JudgeA2r09/extract`,
  `git archive f2de0ee… tools | tar -x`):
  `MORI_OOM_KILLERS_SELFTEST: PASS 30/30` on cases-a2.json and `PASS 32/32` on the round-26 cases.json.
- No failing A2-09 case, so no `tool error` / `case error` / `unclear text` ruling is required.

## Per-case pin check (each pinned value vs rule text)

Case 1 `a2-09-removed-unit-single-sigterm-send`:
- `earlyoom.state: absent` — show text `LoadState=not-found / ActiveState=inactive / UnitFileState= /
  ActiveEnterTimestampMonotonic=0`; `absent` is a listed state (round-26/contract.md:90) and the frozen
  case `c07-earlyoom-absent` pins this byte-identical show text to `absent`.
- `earlyoom.scope_complete: false` — journal has no `earlyoom <version>` line, and scope_complete is
  true only when the version line is inside the scope (round-26/contract.md:93); also
  ActiveEnterTimestampMonotonic=0 makes the invocation unbounded (A2-05, round-26/contract.md:173-174,
  round-27/contract.md:53).
- `verdict: KILLER_ACTED, exit: 1` — the `sending SIGTERM to process ` line is a send line of the
  removed unit this boot → positive evidence (A2-09; round-26/contract.md:97-98 says positive evidence
  stands even with incomplete scope).
- `oomd.state: inactive`, `oomd.notices_this_boot: 0` — direct echoes of the show text and
  `oomd_notices: 0` inputs (round-26/contract.md:90-95).

Case 2 `a2-09-removed-unit-two-invocations-mixed-sends`:
- Same absent/scope_complete false pins; two version lines plus one SIGTERM send, one SIGKILL send, one
  `escalating to SIGKILL after ` line — all send/escalation lines per the grammar
  (round-26/contract.md:85-86), all lines of the removed unit this boot → positive evidence →
  `KILLER_ACTED, exit 1`. `oomd.state: inactive`, `notices_this_boot: 0` as above.

Case 3 `a2-09-removed-unit-three-sends-oomd-active`:
- Same earlyoom pins; three `sending SIG… to process ` lines → `KILLER_ACTED, exit 1`.
- `oomd.state: active` — `ActiveState=active` in the show text; `notices_this_boot: 0`.

## Observed tool output at the attack target (`--inputs` on each case)

Each case produced exactly the pinned fields: `earlyoom.state: absent`, `scope_complete: false`,
`actions: null` (absent killer reports null per round-26/contract.md:102 — unpinned, consistent),
`verdict: KILLER_ACTED`, exit 1. Send lines were counted in `earlier_invocation_send_lines` (1, 3, 3),
consistent with round-26/contract.md:175-179 routing (non-zero is positive evidence for a non-active
earlyoom) and with A2-09 making removed-unit sends positive evidence. Observed, not inferred.

## Post-freeze tool change check

Vacuous: blob ids for tools/mori-oom-killers.py, cases-a2.json and cases.json are identical at
d21b8bd… and f2de0ee… (`git rev-parse`); `git merge-base --is-ancestor` confirms d21b8bd is an
ancestor of the attack target. Nothing changed, so no KILLER_ACTED could have been turned into anything
else on either case file.

## Residual risk / gaps

- Case 2's `why` text claims both invocations' sends land in `earlier_invocation_send_lines`; the
  counter is unpinned (not in `expect.fields`), so a wrong split could not fail the case — the pin only
  requires positive evidence, which any one of the three lines provides. Text-only claim, not a defect.
- I did not read the tool source; behavior was verified by running `--inputs`/`--selftest` from a
  clean archive extract of the attack target.
- No tools installed; none needed (stock python3, git, tar).
