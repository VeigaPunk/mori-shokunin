measured 2026-10-23T09:12:16Z

# JudgeRowsR22 — wave 2 falsify: mori round 22 register row

Scope: the single landed row keyed `rounds[427].capabilities_added[0]` in the final `## Capabilities`
section of SCORECARD.md at lane tip cedb0ec4f3a4f672804deac388b7191258f01fcd, judged under the frozen
decision rule (a) closure-faithful non-empty capability and what cells, (b) evidence cell holding only
backticked paths, against the closure record: fleet MANIFEST.json rounds[427] and
.ufo/reports/round-22/mori.md, both at fleet 37b51a24. Then, outside the rule, (c) the cited artifact
at closure commit 1bfe708a170c877db3319060d0ab38771efe03ac.

## Ground truth (commands run, read-only)

- `git show cedb0ec4…:SCORECARD.md` → scratch copy, 1978 lines; final section header at line 1941;
  file ends at 1978, so line 1941 is the last `## Capabilities` section.
- `git show 37b51a24:MANIFEST.json` → `json.load`: len(rounds)=525; rounds[427] is lane mori,
  lane_round 22, admitted true, capabilities_added length 1 (JSON path rounds[427], python extraction).
- `git show 37b51a24:.ufo/reports/round-22/mori.md` → 70 lines.
- `git show 1bfe708a…:tools/mori-retention-reconcile.py | sha256sum` →
  `0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32` (297 lines).
- `git cat-file -e 77a5bbe8…:tools/mori-retention-reconcile.py` → rc 128 (absent at the entering
  branch the record names); rc 0 at 1bfe708a.

## The landed row

SCORECARD.md@cedb0ec line 1969 (header line 1959, divider 1960). Cells as landed:

- capability: `retention receipt reconciliation`
- what: Independently recounts the measured tree of a committed retention receipt and reports identity
  agreement and policy exclusions; accounting agreement only, privacy clearance always false.
- evidence: `tools/mori-retention-reconcile.py`
- first-working round: 22

Key uniqueness: `rounds[427]` appears in SCORECARD.md only at line 1969 (register row) and line 1420
(prose verdict text in a per-round section, not a register row), so the final register holds exactly
one row for this key.

## (a) Closure faithfulness, clause by clause

Record string, fleet MANIFEST.json@37b51a24 rounds[427].capabilities_added[0], file line 12007:
Retention receipt reconciliation (tools/mori-retention-reconcile.py sha256 0795bac9…de32):
independent identity recount of a committed retention receipt's measured tree; accounting agreement
only, privacy_clearance always false

1. capability cell `retention receipt reconciliation` — the record's name, identical modulo case
   (MANIFEST.json:12007). Stated by the record.
2. `Independently recounts the measured tree of a committed retention receipt` — record clause
   `independent identity recount of a committed retention receipt's measured tree` (MANIFEST.json:12007).
   Same facts: independence, recount, committed receipt, measured tree. Stated, no widening.
3. `reports identity agreement` — record: the capability `reports exact identity agreement`
   (.ufo/reports/round-22/mori.md:7); the tool emits `receipt_match` and `RETENTION_RECONCILED`
   (tools/mori-retention-reconcile.py@1bfe708:231-232). Stated by the record.
4. `policy exclusions` — record: `policy-membership exclusions` (.ufo/reports/round-22/mori.md:7);
   measured run `policy_excluded 5 (non_author_paths_glob)` (.ufo/reports/round-22/mori.md:44);
   tool field `policy_excluded` (tool:233). Stated by the record; the cell drops the qualifier
   membership without adding anything the record lacks.
5. `accounting agreement only, privacy clearance always false` — record clause
   `accounting agreement only, privacy_clearance always false` (MANIFEST.json:12007); bound preserved
   verbatim as always false; code returns False on every path (tool:238, :273, :287, :289; docstring
   tool:2). Bounded exactly as the record bounds it.
6. first-working round 22 — rounds[427].round = 22 and .lane_round = 22 (JSON path, python
   extraction of MANIFEST@37b51a24); tool absent at entering 77a5bbe (rc 128, my check) and present at
   the closure commit, consistent with the record's own entering-branch recheck
   (MANIFEST rounds[427].verification.rechecks).

Nothing in either cell exceeds the record: no claim that retention debt was cleared (the record keeps
retention red, .ufo/reports/round-22/mori.md:44; the row is silent on the red state), and the
clearance negation is kept in the record's own always false strength. Both cells non-empty.

VERDICT: rounds[427].capabilities_added[0] supported

## (b) Evidence cell

The evidence cell is exactly one backticked path, `tools/mori-retention-reconcile.py`, with no prose
and no second token, and the path is the one the record itself names (MANIFEST.json:12007). Meets the
backticked-paths-only requirement; this cell is covered by the supported verdict above.

## (c) Pointer relevance (separate from the rule)

Opened tools/mori-retention-reconcile.py at closure commit 1bfe708a. The blob hashes to
0795bac9…de32, exactly the digest the record binds (MANIFEST.json:12007). The blob implements THIS
capability, not a sibling capability of round 22 or of another round:

- Reads the committed receipt blob from the revision tree (`committed()` via ls-tree/cat-file,
  tool:74, :91) and pins `measured_revision` (tool:170) with `merge-base --is-ancestor` (tool:175).
- `scan()` (tool:143) independently re-enumerates the measured tree (ls-tree -r, tool:74; per-blob
  cat-file, tool:149; per-line policy regex plus line sha256) and `check()` diffs every receipt
  counter — hits, allowlisted, unallowlisted, metric, routed, non_author, finding_id, exit_code —
  into `differences`, emitting MATCH/MISMATCH (tool:231-232). That is an independent identity recount,
  not a format-only validator.
- Emits the accounting fields the row names: `policy_excluded` with `exclusion_basis` (tool:233),
  `retention_state` (tool:236), and `privacy_clearance: False` on every return path
  (tool:238, :287, :289), with `receipt_authenticity: unattested` (tool:239).
- It is not the round-18 retention gate (`tools/mori-retention-gate.py`) nor the round-19
  content-review gate: different files; this blob's docstring states the reconcile-plus-never-clearance
  contract (tool:2).

VERDICT: rounds[427].capabilities_added[0] pointer-relevance holds

## Residual risk and verification gaps

- Post-closure tool drift: the blob at 913df22e29f131ef9cb5de9dcb7e3e272256c5f0 differs from the
  closure blob (`git diff --stat 1bfe708a 913df22e -- tools/mori-retention-reconcile.py`: 1 file
  changed, 2 insertions, 2 deletions). This row is judged at the closure commit per assignment;
  readers citing the evidence path at a later tip should recheck bytes. Wave-1 RowR22 observed the
  same drift; it does not affect this row's verdicts.
- Code semantics verified by reading the blob, not by executing it; the execution claims (selftest
  4/4, direct r21-receipt run rc0) belong to the record (.ufo/reports/round-22/mori.md:44) and to the
  frozen counter, not to this seat.
- MANIFEST.json line numbers are from the git-show extraction at 37b51a24; the fleet working tree may
  differ from that commit.
- Containment: no lane or fleet writes; report is the only lane write; scratch under
  /fast/scratch/hyaku/mori-r35/JudgeRowsR22/; no subagents, no background jobs; all commands
  timeout-capped; no processes left running. Tooling directive: nothing installed or updated.
