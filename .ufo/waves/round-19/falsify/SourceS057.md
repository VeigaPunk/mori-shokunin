# S057 CrossRef quote falsification

**Verdict: AGREE** with the repaired lesson quote, its abstract-only anchor, and the rejection disposition. This is an author-side fresh falsification, not independent closure.

Re-opened `https://api.crossref.org/works/10.1177/1745691612463078`. The returned `message.abstract` contains: `Other analyses can be carried out but these should be labeled “exploratory.”` (12 words). The immediately following sentence introduces the confirmatory replication example, so the lesson's locator is accurate. The lesson normalizes the inner quotation marks from double to single and discloses that normalization. The API response is the CrossRef record/abstract, not the article body; I make no body-text claim.

- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-19.md:72` — **QUOTE/ANCHOR: AGREE.** The cited sentence is present in the named abstract field, within the 25-word limit, and is correctly located before the replication example. The stated abstract-only screening scope is accurate.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:63` — **SCOPE/DISPOSITION: AGREE; RATIONALE: CAVEAT.** The registry records CrossRef abstract-only scope, body not opened, and a C/rejected redundancy decision; these agree with the located quote and lesson. Its phrase that the stronger validity claim is “unverified” should mean that the article body's argument/support was not reviewed: the CrossRef abstract itself states that claim. This re-open verifies the abstract's wording, not the claim's validity or the body's support.

No article body was opened; no tests or verification runs were performed.