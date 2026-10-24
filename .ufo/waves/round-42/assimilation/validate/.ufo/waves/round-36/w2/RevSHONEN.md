# RevSHONEN — round-36 wave-2 SHONEN checklist evidence review

Seat: `mori-r36-w2-RevSHONEN-23`. Lane repo read-only; no lane file was modified by this seat (this
report is the only file written). Scratch: none used beyond $TMPDIR-free direct runs.

**Item attacked:** `SHONEN.md` (promotion checklist, four boxes) against this round's evidence (landed
tip `bf0df77fee4b6ef54a90aea09335c7617f125151`, round base `6bd57097f7ab2b471b4593ed2019c980b1368c68`).

## Canonical mark semantics (ground truth, PROTOCOL.md:61-75)

- `SHONEN.md` itself keeps the canonical four `[ ]` boxes; the round report's `## SHONEN` heading
  carries one assessment line per box: `[x]` / `[ ]` / `[~]` + pointer.
- `[x]` may only be written by a named non-author `<id>` (fresh lane or integrator review; a subagent
  the lane dispatched is still the lane). Any `[x]` without a named non-author verifier counts as
  `[~]` for the gate.
- `[~]` = lane-asserted assessment with an evidence pointer. Minimum bar: box 1 needs ≥1 SKILL.md
  decision table + error-pattern list + checklist, each citing a resolvable source; box 2 needs an
  end-to-end task executed and logged; box 3 needs SKILL.md/corpus instructions executable without oral
  context, self-contained, with resolvable pointers; box 4 bars cross-domain bleed and keeps
  PROVINCE.md accurate.

## Measurements

- `git diff --quiet 6bd57097f7ab2b471b4593ed2019c980b1368c68 bf0df77fee4b6ef54a90aea09335c7617f125151 -- SHONEN.md` → exit 0 (**byte-identical**; matches RevNoHarm's identical check).
- `git show bf0df77:SHONEN.md | diff - SHONEN.md` → no output, exit 0 (worktree = tip for SHONEN.md).
- `read SHONEN.md` → all four boxes present, each `[ ]`.
- `git show bf0df77:LOG.md | grep -n 'Round 36'` → no match (exit 1): **no round-36 LOG entry at the
  landed tip** (LOG.md absent from the 6bd57097..bf0df77 diff; the last LOG entry is round 35).
- Round diff scope (from RevNoHarm, verified independently this seat): 118 changed paths, 0 deletions,
  no fleet-root/sibling path; `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md` byte-identical at endpoints.

## Findings by severity

### No defect — no box flipped; all `[ ]` remain

SHONEN.md is unchanged through the round and every box is still `[ ]`. No `[x]` exists anywhere; no
named non-author `<id>` verifier is present in this round (all wave-2 reviewers are lane-dispatched
seats, therefore still "the lane" per PROTOCOL.md:63-64). audit-r11.md:226-228's conclusion (no named
non-author attestation in the gate; no box checked) stands.

### Recommended marks for the round report's `## SHONEN` heading

1. **Box 1 — SKILL.md real decision tables / error patterns / checklists / cited sources: `[~]`.**
   Pointer: `SKILL.md:856-874` (three registry rows; every gate-standard field present — name, kind,
   entry, verdict map, self-test, pinned values, write scope, owner; RevSkillRows PASS, every entry
   command run at bf0df77 with mapped exit); `corpus/QUALITY.md` criteria 103-105 (error patterns with
   shown-able-to-fail evidence); `corpus/SOURCES.md` rows S205-S220 appended (16 rows, URL + pin each;
   match `git show bf0df77:corpus/SOURCES.md`). Non-author gate: not satisfied — RevSkillRows is a
   lane-dispatched seat; no `[x]`.
2. **Box 2 — at least one end-to-end domain task executed and logged in LOG.md: `[~]` (conditional).**
   The C2 capability acquisition is a full end-to-end task: tool built (tools/mori-sources-appendonly.py),
   frozen counter (count-c2.py, sha256 pinned in evidence/freeze-v2.txt), blind arm 24/24, real arm pass,
   receipts `evidence/c2-after.txt` / `evidence/c1-after.txt`. **But LOG.md has no round-36 entry at the
   landed tip** (measurement above). The mark is valid only if the round integration appends the LOG
   entry with the report (protocol ties landed changes to LOG entries); if the report lands without it,
   the box must be `[ ]` until the entry exists.
3. **Box 3 — instructions executable by an agent without oral context: `[~]`.**
   Pointer: SKILL.md registry rows are self-contained (exact entry commands, verdict maps, selftest
   commands); RevSkillRows executed all three registered commands at bf0df77 with observed mapped exits
   and selftests PASS (drift probe exit 1 `drifted=9`; append-only gate exit 0 with `--round-base`
   / 1 without; index-clean exit 0 `staged=0 intent_to_add=0`). Non-author gate: not satisfied — run is
   lane-dispatched; no `[x]`.
4. **Box 4 — no cross-domain bleed, PROVINCE.md accurate: `[~]`.**
   PROVINCE.md byte-unchanged this round; RevNoHarm's full-diff audit found 0 deletions, no fleet-root
   or sibling-lane path, no cross-domain bleed. Adjacent (carry in report findings, not a box flip):
   RevNoHarm FAIL cites internal province-scope violations — a remediation instruction in
   `corpus/knowledge/source-drift-r36.md:27-28` ("Restore `DIR/corpus/SOURCES.md`") conflicting with
   PROVINCE's "detection and report only", and SIGKILL on timeout in `.ufo/waves/round-36/count-c2.py:70-82`.
   These make the round's content deviate from the declared province; they do not falsify PROVINCE.md's
   accuracy as a statement, so box 4 keeps `[~]` but should not be promoted past it while they are open.

## Residual risk / verification gaps

- **Box 2 dependency:** the `[~]` mark for box 2 presupposes the round-36 LOG entry lands during
  integration; as of bf0df77 it does not exist. If the report is filed before the LOG entry, mark
  `[ ]`.
- **Superseded-list discrepancy (handed to RevC2Oracle; not adjudicated here):** this seat's direct
  re-runs of the registered gate at bf0df77 (commands + observed output below) print
  `superseded=[S041,..,S193]` (all 18 `ids`), while the `evidence/c2-after.txt` receipt's tool and
  oracle lines print `superseded=[S069,S182,S193]`. Same rev, same tool bytes, different superseded
  sets. This concerns C2 claim verification, not the SHONEN marks; it should be reconciled by the
  C2-oracle seat before the claim is closed.
  ```
  $ python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151
  changed S041 superseded_by=S206 ... changed S193 superseded_by=S202
  appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
  exit=1
  $ python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097
  (same `changed`/summary lines; round_changed=[]) exit=0
  ```
- **Non-author promotion review remains absent** (audit-r11.md:226-228; no change this round), so no
  box can be `[x]` and the lane stays shonen.

## VERDICT: PASS

(no defect found in the SHONEN checklist: all four boxes remain `[ ]` in SHONEN.md, no box is flipped
to `[x]` without a named non-author verifier, and the correct report marks are `[~]` for boxes 1, 3, 4
and `[~]`-conditional for box 2 per the paragraph above.)
