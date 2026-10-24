# Routed D3 — QUALITY draft

## Proposed QUALITY addition

```text
94. LEARNING — supersedes QUALITY criterion 93 (pre-freeze gate receipt; leave criterion 93 unchanged). A gate may support a counted condition only when a receipt committed before the freeze records the exact frozen gate blob and the round’s own writer inputs after the gate’s final edit; the receipt preserves the complete hit list, and every hit has an explicit adjudication by a non-author reviewer. A two-hit negative input must produce two separately adjudicable hits. A changed gate, omitted hit, or unadjudicated hit makes the gate ineligible for that counted condition. ← corpus/lessons/round-31.md (Routed D3; round-30 M5).

Check: At freeze F, verify the receipt is committed before F, binds the exact gate blob at F and the round’s writer inputs, and includes the complete output. Replay that blob on a two-hit negative input and require two hit records; require one explicit non-author adjudication for every recorded hit. Fail on a missing or later receipt, a blob/input mismatch, incomplete output, a missing hit or disposition, or an adjudicator who authored the gate.

Shown able to fail: the round-30 freeze db1ec469 is rejected: its A2 gate was changed after the writer-wave run and frozen without being re-run; the frozen gate printed one hit while first-forbidden-line-only reporting masked a second, and no adjudicated receipt of the freeze blob preceded the freeze (corpus/lessons/round-30.md:204-206; corpus/QUALITY.md:661-663).
```

## Proposed QUALITY 92 finding

```text
QUALITY 92 is unmet at the round-30 tip (`limit_stated=no`): no `r30-disputed-*` id is named alongside a limit in SKILL.md or `corpus/knowledge/` (corpus/lessons/round-30.md:228-229); the criterion’s committed-byte check searches for a line containing both a case id and “limit” (corpus/QUALITY.md:634-640).
```

## Findings and provenance

- Criterion 93 is the final numbered criterion in the inspected QUALITY excerpt; its wording requires adjudication, but its stated check only checks for a receipt commit that is an ancestor of the freeze and that the receipt names the frozen gate blob (corpus/QUALITY.md:656-663). The round-30 correction states the literal check passes round 29 and a sandbox with unadjudicated hits (corpus/lessons/round-30.md:215-216). Criterion 94 is therefore the next number and the draft adds observable checks for the failure modes reported in M5 (corpus/lessons/round-30.md:204-206).
- The routed spotcheck explicitly requires superseding criterion 93 rather than rewriting it, and records criterion 92 as unmet with `limit_stated=no` (corpus/lessons/round-30-verifier-spotcheck.md:182-183).
- Read-only source inspection: `corpus/QUALITY.md:599-663`, `corpus/lessons/round-30.md:204-237`, and `corpus/lessons/round-30-verifier-spotcheck.md:182-183`. No shell commands, tests, or checks were run; the proposed check is a draft, not exercised evidence.

## Scope and status

- This report is the only file written: `.ufo/waves/round-31/w1/DraftQuality93.md`.
- `corpus/QUALITY.md` and both round-30 lesson files were read only; no product or corpus files were edited.
- No tools were installed or updated. No git/jj writes or validation runs were performed.
- Out of scope: committing the proposed QUALITY row or changing the round-30 finding; the canonical round-31 lesson and QUALITY integration are not part of this scoped draft.
