# S059 — author-side fresh falsification

## Verdict

**Partial agree.** The lesson's located quote is genuine and within the 25-word limit; retaining S059 as rejected for the C2 freeze-order claim is supported. **Disagree that the quote repair is complete across the compared artifacts:** the S059 registry row still has no located quotation or explicit unavailable/screening-only limitation.

## Evidence

- **Quote — agree:** `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-19.md:73` records a 10-word quotation and locates it at the public `git-log` **DESCRIPTION**, first explanatory paragraph. Reopened `https://git-scm.com/docs/git-log` (current page identifies version 2.56.0); that passage matches. The passage states the default order, not the explicit topology order selected by the freeze-order tool.
- **Rejection — agree, scoped to C2:** `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:94-101,104-109` uses `diff-tree` and `rev-list` with explicit first-parent/topological ordering; it does not call `git log`. The public `git-log` **DIFF FORMATTING** and **CONFIGURATION** sections document merge-diff defaults and the conditional `log.diffMerges` setting, but those porcelain defaults add no needed authority for the tool's plumbing behavior. `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:64-65` scopes S058 to the used plumbing references and S059 as an alternative; this remains a sound rejection for the stated C2 verdict.
- **Registry repair — disagree:** `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:65` contains scope/rejection text and reader-location anchors, but no verbatim quote or explicit screening-only exception. The earlier gap is explicitly recorded at `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-18-verifier-spotcheck.md:168-170`; the round-19 note at `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-19.md:77-79` confirms no S059 registry row was added or changed. Thus the Gate quote is repaired; the registry-scoped quote gap is not.

## Limits

This is an author-side source check, not independent closure. No tests or verification runs were performed.