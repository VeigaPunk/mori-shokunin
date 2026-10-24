# HistoryPin — invalid r20 baseline instructions

Scope: `corpus/knowledge/drift-repin-r20.md` only. No source files were edited and no census, drift, or pin command was run.

## Observed

- The appended round-21 erratum already rejects the pin: lines 82–97 supersede the cause-only rule and acceptance readings of §§4–5, state that `baseline-r20-20261021T1051Z.json` is invalid for acceptance, and require QUALITY69 plus retained evidence-loss accounting before any future pin. It records the two aggregator observations as unresolved and blocking.
- **Remaining active operational instruction:** line 12 still says to recheck by running `--drift` against `corpus/evidence/baseline-r20-20261021T1051Z.json` and classifying against the r20 register with the round-20 checker. This conflicts with the appended ruling if read as the current acceptance/recheck recipe. It is the only forward-looking command in this note that directs use of the invalid r20 baseline.
- The stale cause-only rule and zero-regression result are at lines 26–34. Historical pin and post-pin `none` observations are at lines 54–70; the potentially over-claiming “What the new baseline certifies” text is at lines 72–78. These passages are now explicitly superseded for acceptance by lines 82–95; their observations should remain as historical record, not be erased or rewritten as if the pin did not happen.
- The title and metadata (lines 1, 5–12) still foreground a re-pin and “new baseline”; they are historical framing, but could reinforce the stale recipe unless the erratum explicitly scopes them too.

## Proposed appended erratum anchor

Append after the existing erratum at line 100, preserving all historical text. Explicitly anchor the correction to **line 12** (and, for clarity, the title/metadata at lines 1 and 5–12): label the r20 `--drift` command/register check historical-only, not an active acceptance recheck; direct readers to QUALITY69 and round-21 retained evidence-loss accounting; state that the r20 baseline cannot clear the blocker and no new pin is permitted until both old waves have independently evidenced dispositions. Preserve §§2–5 as historical observations, with their acceptance interpretation governed by the existing erratum at lines 82–97.

Suggested anchor label: `## Round21 erratum addendum — recheck recipe is historical only`.

## Evidence / confidence / gaps

Observed from the assigned note: lines 12, 26–34, 54–78, and 80–100. Confidence: high for this file. Literal search plus direct file reads were used; no LSP device was exposed in this session. This report does not audit the separate SKILL, index, scorecard, or province instruction surfaces.