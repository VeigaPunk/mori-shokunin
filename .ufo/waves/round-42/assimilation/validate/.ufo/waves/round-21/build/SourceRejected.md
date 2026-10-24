# S072 source rejection recheck

**Question:** Whether the tertiary rejection of Wikipedia's *Characterization test* remains justified for the existing re-pin claim.

## Observed

- Reopened https://en.wikipedia.org/wiki/Characterization_test (Wikipedia API fetch, 2026-10-21). Its lead contains this exact 14-word excerpt: “a means to describe (characterize) the actual behavior of an existing piece of software”.
- `corpus/SOURCES.md:78` still identifies S072 as tier C and records its scope as the lead definition for the re-pin ritual; its stated rejection reason is no added support over S067. S067 (`corpus/SOURCES.md:73`) is Michael Feathers's own essay and directly supports the actual-behavior, not desired-behavior distinction. `corpus/lessons/round-21.md:27` records the same located quote and re-rejection.
- The reopened Wikipedia lead also describes protecting legacy behavior against unintended changes through automated testing. That general context does not establish whether a re-pinned baseline is healthy or whether historical evidence is settled.

## Finding

**Yes—the tier-C rejection remains justified for S072's recorded, narrow scope.** The direct Feathers essay remains available for the relevant actual-versus-desired-behavior point, while Wikipedia's additional generic framing does not add support for the re-pin/health distinction. The row's conditional flip (a primary definition becoming unreachable) is not observed.

**Confidence:** High for the assigned re-pin question. Broader uses of Wikipedia's characterization-testing discussion were not assessed. No registry or source files were edited.