# QualityHeading review

Axes: attribution clarity; historical-text preservation; boundedness.

## Finding — low severity

`corpus/QUALITY.md:188,227-256` places Q64–68 under `## Criteria added round 19`. The appended correction at `corpus/QUALITY.md:258-261` says they were authored in round20 and that their original bytes remain, but it gives no calendar date. `corpus/lessons/round-21.md:35` likewise calls this a “dated correction” without stating a date. Concrete counterexample: a reader can identify the corrected round attribution but cannot tell from the clarification when it was recorded.

Smallest safe change: append an explicit date to the existing attribution correction (for example, `Attribution correction (2026-10-21): criteria 64–68 above were authored round20, despite their placement beneath the round19 heading; their original bytes remain.`) and leave Q64–68 verbatim where they are. If the lesson continues to call it “dated,” reference the same date there. Do not move the criteria or alter their historical wording.

## Residual risk

This clarification addresses authorship/placement only. `corpus/lessons/round-21.md:35` explicitly retains Q64/65/66/68 as routed debt; the attribution note must not imply those gates were repaired.

## Verification gaps

- No `lsp` device/server was mounted (`xd://lsp` returned “No such tool”); literal search was used only to locate the two directly relevant references, then their text was read directly.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff HEAD -- corpus/QUALITY.md` returned no output, so there was no working-tree delta for this file to review; finding is against the current text.
- No tests or implementation were run/performed, per scope.
