# SrcCharacterization — frontier source for C1 (characterization / golden-master tests)

Seat: MoriR20.SrcCharacterization (scribe, leaf). Access date: 2026-10-21. No subagents. No lane, registry, census, baseline or git/jj state was edited. Read-only fetches only.

## Proposed SOURCES row (for L1 admission; not written to corpus/SOURCES.md)

Shape follows `corpus/SOURCES.md` header: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S066 | Michael Feathers, "Characterization Testing" (blog post, dated August 08, 2016) — https://michaelfeathers.silvrback.com/characterization-testing | docs | B | origin-author essay defining a characterization test as documenting actual behavior, not desired behavior; informal essay, not a normative specification; the term's coiner | Post section "Characterization Testing", paragraph beginning "It’s a trick question.", final sentence; access 2026-10-21 | A characterization test records what the system actually does so that behavior changes are detected; it is not evidence that the behavior is correct. | queued | 2026-10-21 | 365d | — |

Located quote (verified byte-exact against the page fetched 2026-10-21; 22 words; the source uses a curly apostrophe in "system’s"):

> "The purpose of characterization testing is to document your system’s actual behavior, not check for the behavior you wish your system had."

Supporting located sentence in the same post (also verified): "We can run our tests and find out immediately whether we’ve changed behavior." Not needed for the row.

Method used in the post (for the C1 register/lesson, not a quote): write a test named `x` with a dummy expectation, run it, read the actual value from the failure, then paste it as the expectation.

## Tier and scope, stated honestly

- Tier B, not A. The page is the coiner's own blog post (primary about his usage) but it is an informal essay, not a normative spec or standard. Tier B is the same tier the registry gives the Google SRE book (S029) for an expert, non-normative source.
- The canonical definition is the book *Working Effectively with Legacy Code* (Feathers, 2004; ISBN 0-13-117705-2 as cited by Wikipedia). I did NOT open the book, so no quote from it is proposed. Secondary sites that paraphrase the book's definition were seen in search snippets only and are not admissible.
- Wikipedia "Characterization test" is tier C (encyclopedic secondary; no `primary` status). Verified located text (rendered page, fetched 2026-10-21): "a characterization test is a means to describe (characterize) the actual behavior of an existing piece of software" (18 words). The wikitext contains the same words wrapped in markup (`'''actual'''`, `[[legacy code]]`), so the rendered page is the quoted form. Not proposed as a row; available as a tier-C orientation cross-check only if the L1 wants one.

## Verification performed

- Fetched https://michaelfeathers.silvrback.com/characterization-testing (HTML, 36,970 bytes) and grepped the exact quote: 1 match. Word count of the quote: 22 (`wc -w` on the exact string).
- Fetched Wikipedia via the MediaWiki/markdown reader (rendered) and the raw wikitext; the 18-word phrase is present in rendered text; the wikitext check matched after markup, not byte-exactly (expected: markup in source).
- Quote word counts: Feathers 22 (≤25 ✓); Wikipedia 18 (≤25 ✓).

## Tools installed or updated

None. Used `curl` (system binary, already present) to fetch two pages into /tmp for grep verification; nothing installed.

## Rejected or unfit candidates

- Book *Working Effectively with Legacy Code* (2004): not opened; no quote claimed.
- Secondary blogs and aggregators (DaedTech, understandlegacycode.com, lassala.net, dev.to, helpmetest.com and similar): paraphrases of the book; tier C or lower; not proposed.
- Feathers' 2016 post supports the definition and the "document actual behavior" framing; it does not state a scope limit on characterization tests for C1 freshness claims. Any C1 claim beyond "characterization = actual current behaviour pinned for change detection" needs its own source.

## Findings for C1 (no edits made)

- The located quote grounds the central C1 premise: a drift/baseline register pins observed behavior and a diff is a change signal, not a correctness verdict. This supports classifying a drift token as "census-schema-change | roster-change | live-state | census-regression" without implying any of them is a defect by default.
- Limit the lesson: a passing characterization/baseline proves only that behavior did not change since the pin. It does not prove the pinned behavior is right, which matches the contract's "a re-pin is not a correctness claim" stance.

## Paths

- This report: mori-shokunin/.ufo/waves/round-20/build/SrcCharacterization.md
- No candidate code or drafts written.
