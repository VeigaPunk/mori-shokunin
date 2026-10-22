holds — A2-03 (`killing whole process group ` → `earlyoom.process_group_lines`): all 3 cases pin values that follow
from the rule text, all passed at the freeze (PASS 30/30), and the tool is unchanged since the freeze, so no ruling
and no post-freeze audit is owed.

Seat: MoriR28.JudgeA2r03 (amendment-A2 judge, rule A2-03 only). Attack revision:
f2de0eedcd60d2e354da75265ea6122bc3896073. Read-only; no lane writes except this report; scratch at
/fast/scratch/hyaku/mori-r28-w2/JudgeA2r03/ (git archive extract, not a clone — tool run only).

## Rule text

- `.ufo/waves/round-27/contract.md:51` — A2-03: "`killing whole process group ` lines are counted in
  `earlyoom.process_group_lines`".
- `.ufo/waves/round-26/contract.md:164-165` (amendment A2, item A5/X2) — same rule, plus "every count is a count of
  earlyoom log lines, not of processes signalled or killed".
- Supporting pins come from the base contract the amendment text builds on: scope = journal lines with
  `__MONOTONIC_TIMESTAMP` ≥ `ActiveEnterTimestampMonotonic` of the current invocation, current boot
  (round-26 contract.md:78); message grammar incl. send lines as the only action lines (:80-89, esp. :85);
  `scope_complete` true only when the current invocation's version line is in scope (:93); verdicts (:96-106).

## What I verified

1. Freeze evidence `.ufo/waves/round-28/evidence/c2-freeze-selftest.txt:1-4`: at the freeze commit
   d21b8bd38b1bf72ec903a19ed543c615564e8278 the tool printed `MORI_OOM_KILLERS_SELFTEST: PASS 30/30`, exit 0.
   No A2-03 case failed, so no `tool error` / `case error` / `unclear text` ruling is owed.
2. Tool blob identical at freeze and attack rev: `git rev-parse d21b8bd:tools/mori-oom-killers.py` =
   `git rev-parse f2de0eed:tools/mori-oom-killers.py` = 3fb78bbc2612c38e463e04083bdb213954647568; the log of
   d21b8bd..f2de0eed on `tools/mori-oom-killers.py` and `tools/fixtures/mori-oom-killers/` is empty. The
   "L1 changed the tool after the freeze" clause is vacuous; no KILLER_ACTED flip check needed (the tool never
   moved). Case-file blob also identical (7ba553d45e3b00d507e57132cc3c28fb140f83fd both revs).
3. Independent re-run at the attack revision (temp archive extract of f2de0eed, `python3 -I -B
   tools/mori-oom-killers.py --inputs /dev/stdin` per case, compared every pin): all 3 cases return the pinned
   verdict, exit and every `expect.fields` value — output `ALL-PINS-MATCH` x3.

## Per-case pinned values vs rule text

`a2-03-group-kill-one-with-sigterm-action`: one `killing whole process group 5507 (-g flag is active)` at
ts 20510001, in scope (ActiveEnterTimestampMonotonic 20500000) → `process_group_lines: 1` per A2-03; one
`sending SIGTERM to process ` line → `actions.sigterm: 1` (contract:85) → `KILLER_ACTED`, exit 1 (contract:97-98).
Threshold pins follow the grammar lines :83-84; `scope_complete: true` per :78+:93; `dryrun: false`; oomd pins
match `oomd_show`/notices 0. Every pin follows.

`a2-03-group-kill-two-no-action-oomd-notices`: two group lines in scope → `process_group_lines: 2` per A2-03;
no send lines → all action counts 0 (contract:85 names only send prefixes; group lines go to
`process_group_lines`, not actions — the "count of log lines" clause of round-26:165); `thresholds: null` (no
threshold lines logged, schema :91-95); `scope_complete: true` (version line at ts == 41000000 boundary, :78);
`KILLER_ACTED` forced by `oomd_notices: 4` (contract:97). Every pin follows.

`a2-03-group-kill-three-after-earlier-invocation`: three group lines after the current-invocation version line at
ts 62000000 → `process_group_lines: 3`; the earlier invocation (version line at 19960000, before
ActiveEnterTimestampMonotonic) contributes no in-scope group line, matching A2-03 + scope :78; `actions.sigkill: 1`
from the `sending SIGKILL to process ` line (:85) → `KILLER_ACTED`; `scope_complete: true`. Every pin follows.

## Rulings

None owed — no A2-03 case fails at the freeze or at the attack revision. For the record, had one failed:
`tool error` would be decided by round-27 contract.md:51 / round-26 contract.md:164-165; a mismatch on a
verdict pin only, with `process_group_lines` correct, would be decided by the verdict rules at round-26
contract.md:96-106.

## Residual risk / gaps

- Rule text is silent on whether group lines alone are positive evidence; no case isolates that shape (case 2's
  verdict is forced by oomd notices). Within my assigned scope (do the pinned values follow?) this is not a defect:
  nothing pinned contradicts the text. [INFERENCE] — flagged only as untested surface, not a finding.
- I verified pins at f2de0eed myself; the 30/30 at the freeze is taken from the committed evidence file plus the
  identical tool blob (equivalent bytes, not a re-run of the freeze rev).
- Tooling: no installs; system git 2.x and python3 used, channel n/a (pacman paused host-wide per RULES.md).
