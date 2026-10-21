# QualitySupersession — round21 C2 pre-implementation attack (detection/report only)

Seat: MoriR21.QualitySupersession-4. Scope: Q67 old bytes must remain; append explicit
supersedes67 with source lesson and fail-capable gate. No production writes, no tests run,
no tool installs (none needed). Entering tip e9f340c; HEAD at read time 8fed329.

## Verdict

The bounded requirement is satisfied in the landed bytes. Two state/integration findings
below; no design defect found in the supersession or the gate. No broad change recommended;
frozen files must not be touched.

## Verified requirements (evidence)

1. Q67 old bytes remain — append-only proven.
   `git diff e9f340ce986f82a60baad1b8e5ead655ab818a1c -- corpus/QUALITY.md` =
   22 insertions, 0 deletions. Criterion 67 sits at `corpus/QUALITY.md:245-250` in both
   e9f340c (`build/QualitySupersession/QUALITY-at-e9f340c.md:245-250`, extracted via
   `git show`) and HEAD `8fed329` (`grep -n '^\(67\|68\)\.'` → 245, 251). The append does
   not shift the old block.

2. Explicit supersedes67 appended and committed.
   `corpus/QUALITY.md:263` criterion 69 "**Supersedes67.**" classifies by evidence
   assurance before causal explanation; blocks baseline acceptance; blind_spot cannot
   override; r20 baseline demoted to retained historical artifact, not accepted reference;
   Q64/65/66/68 declared qualified debt, no repair asserted. Commit `a8442a0` ("round-21:
   invalidate unsafe pin and supersede QUALITY67 honestly").

3. Source lesson cites reopened S066.
   `corpus/QUALITY.md:269` anchors to `lessons/round-21.md#M1 and #M2`;
   `corpus/lessons/round-21.md:26` re-admits S066 (ApprovalTests README, commit-pinned)
   with "Not authority for mori's loss policy"; `:29` records the used-by chain. M2's fix
   column is the supersession itself — chain intact.

4. Fail-capable gate.
   `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py` (only existing copy; see F2):
   - decision reads the rule object, never phase: `:687`
     `rule["evidence_loss_blocks"] and case lost and not independent_disposition` →
     census-regression/false, else live-state/true.
   - rc contract: 0 all match / 1 mismatch (`:717`), SetupError → 2 (`:1207-1209`).
   - `_load_rule :648-651` rejects a false rule that does not cite Q67
     (`before_rule_must_cite_q67`), forcing the evaluator to read an explicit old-rule
     object; `before-rule.json` interpretation carries "QUALITY67" and honestly states the
     criterion "had no executable gate".
   - rule schema closed: `_require_keys :335-344` rejects unknown keys (rc2).
   - selftest asserts before-rule mismatches exactly loss-unknown + loss-cleanup-only
     (`mismatched == 2`, rc1, stable finding_ids `mori-evidence-loss:classify:<id>`) and
     after-rule rc0 (`:1056-1099`). I did not execute it (not authorized); this is static
     reading.

5. Independent frozen expectation table.
   `.ufo/waves/round-21/frozen/cases.json` is byte-identical to the contract's six frozen
   cases (compared field-by-field; loss-unknown and loss-cleanup-only expect
   census-regression/false). Blob unchanged across `3b792db` → HEAD → worktree
   (`git ls-tree` equal; `git status` clean). Freeze commit `3b792db` precedes the
   supersession commit: history order e9f340c → 1c00103 → **3b792db (freeze)** → b9b8b44 →
   a8442a0 → 8fed329, so the table predates implementation. MutOldPermission probe pins
   verified against actual bytes: after-rule sha256 `8bf6cd9f…` and cases `10603c9e…`
   both match; probe's own re-serialization of cases.json reproduces `10603c9e…` exactly.

6. Errata in active prose (no historical edits).
   `SCORECARD.md:1289` "QUALITY69 supersedes67; this is not a re-pin" plus C1/C2 rows
   `:1295-1296`; `PROVINCE.md` round21 correction section ("QUALITY69 supersedes67. The
   historical r20 baseline stays byte-unchanged but invalid for acceptance");
   `corpus/README.md:407` already records CloseMori20's rejection of QUALITY67's universal
   permission. Attribution correction for criteria64-68 sits beneath the r19 heading as
   appended errata, old bytes untouched.

## Counterexample (what Q67 would have permitted)

Under the old rule object (`evidence_loss_blocks:false`), frozen case `loss-unknown` —
required observation `aggregator-r10` lost, `independent_disposition:false`,
`ordinary_state_change:true` (unchanged census code + changed host/fleet state) —
classifies `live-state`, `pin_allowed:true`, against the frozen expectation
`census-regression`, `pin_allowed:false`. Operationally: a baseline is acceptable while
required evidence is gone and disposition is unknown — exactly the r20 harm CloseMori20
rejected. The static decision path (`:687` else-branch) and the selftest rows
`before_loss_unknown` / `before_loss_cleanup_only` (rc1, mismatched 2) encode this;
`MutOldPermission/probe_old_permission.py` operationalizes the mutant detection by
flipping the after-rule's token to the old value and expecting the detector signature to
change `((0,0),(1,2))` → `((1,2),(0,0))`.

## Findings by severity

- F2 [integration, medium] — `tools/mori-evidence-loss.py` is absent from HEAD and has no
  commits (`git log HEAD -- tools/mori-evidence-loss.py` empty; not in `git ls-tree HEAD
  tools/`). The fail-capable gate exists only as scratch bytes
  `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py`. Smallest safe change: ImplLoss/L1
  lands the unchanged reviewed file at the contract path `tools/mori-evidence-loss.py` and
  commits. No redesign; no edits from this seat.
- F1 [state, low] — `corpus/QUALITY.md` worktree carries one uncommitted line vs HEAD
  8fed329: the attribution correction gains "(2026-10-21)". If the round settles at HEAD,
  the dated correction is lost. Smallest safe change: L1 commits that single line during
  integration (or consciously drops it). Detection only; I made no write.
- F4 [residual, info, no action] — `frozen/after-rule.json` `source` says "round21
  supersession of QUALITY67" without pointing at `corpus/QUALITY.md:263` or
  `lessons/round-21.md#M2`. Contract requires Q67 citation only on the before-rule, so
  nonblocking; and editing the frozen file now would break the `3b792db` freeze and the
  probe pins. Recommend explicitly: do not touch.
- F3 [info] — supersession linkage in the after-rule is enforced externally by the
  MutOldPermission sha256 pins, not by `classify` itself (the tool only forces Q67 citation
  on false rules). Adequate given the pins verify today; re-verify pins if either frozen
  file is ever regenerated.

## Residual risk / verification gaps

- All gate behavior above is statically derived; no `classify` invocation or selftest run
  (not authorized for this item). MutOldPermission and KagiR25's authorized isolated runs
  are the execution witnesses.
- I did not audit `audit` subcommand internals beyond confirming the classify gate; C1
  freshness is sibling scope (HistoryRetention/AuditNoPin seats).
- LOG.md:568 references "supersession explained at corpus/evidence/README.md:349-356",
  but those lines now hold r6 receipt tables (line drift in a historical log entry).
  Historical bytes; not a round21 defect.

## Artifact

Entering-revision extract retained at
`.ufo/waves/round-21/build/QualitySupersession/QUALITY-at-e9f340c.md` (from `git show
e9f340c:corpus/QUALITY.md`) for the 245-250 line-range evidence.
