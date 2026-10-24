VERDICT: PARTIAL
S071 quote, location, length, URL/date, anchor, scope and status HOLD. Tier, teaches and used-by completeness are BROKEN. Scope: S071 only. Nothing edited, no subagents, no tool installs.

## Re-opened source (me, 2026-10-21)
- GET https://kubernetes.io/docs/concepts/architecture/controller/ -> HTTP 200, 509019 bytes, sha256 96ad0ef9661c7a3fff3b360ce9643a6c1bc120bcec52b82385c94481194581cb, Date "Wed, 21 Oct 2026 11:02:24 GMT".
- meta article:modified_time 2024-09-01T01:54:45+03:00; footer "Last modified September 01, 2024".
- Reader text (`read`) and raw HTML agree on every point below.

## Per field
Row = corpus/SOURCES.md:77. Gate = corpus/lessons/round-20.md:46.

1. Quote verbatim at stated location: HOLDS. 75 ASCII chars, no NBSP, no double space. Exact-substring count in rendered text = 1, preceded by "The controller(s) for that resource are ". Raw HTML line-wraps between "current" and "state"; it renders as one space.
2. Quote <=25 words: HOLDS. 12 words.
3. Location "Controller pattern, third sentence": HOLDS. First paragraph under "## Controller pattern": s1 "A controller tracks at least one Kubernetes resource type." s2 "These objects have a spec field that represents the desired state." s3 = the quote.
4. Row anchor (section, sentence, revision): HOLDS. "Desired versus current state" section exists; modified 2024-09-01 matches meta and footer; opened 2026-10-21 matches fetch date and Gate access date. URL identical in row and Gate.
5. Scope "vocabulary only; acting controllers, not observe-only": HOLDS. Controllers "make or request changes where needed". The only observer sentence (under "Direct control"; "observe" occurs once): "Other control loops can observe that reported data and take their own actions."
6. Tier B: BROKEN (under-tiered; not an overclaim). CORPUS.md:93-94 puts "official docs" in A, scoped to the claim. S071 is Kubernetes project docs, authoritative for the vocabulary it is cited for. Official-docs peers are all A: S028 (Kubernetes probes docs, SOURCES.md:34), S052 (:58), S053 (:59), S068 (:74), S069 (:75). The three kind=docs B rows are S049 (OWASP cheat sheet, :55), S067 (personal essay, :73) and S071. CORPUS.md:95-96 lists B examples as expert write-up, survey, textbook.
7. Teaches ("one grounded learner benefit", CORPUS.md:101): BROKEN.
   - Clause 1, "Name the declared set (dispatch members) and the observed set (reports) separately": GROUNDED. Page defines desired state as the spec field and says controllers "report the current state back".
   - Clause 2, "mori observes the gap and never acts to close it": NOT IN S071. The page never says an observer must not act; it says observing loops "take their own actions". The rule matches the wave's read-only scope (.ufo/waves/round-20/contract.md:56 "New read-only tool"; :113-115 bounds). The row's own scope cell disclaims observe-only coverage, so S071 cannot be its source. The Gate quote grounds only clause 1.
8. Status "mined": HOLDS. CORPUS.md:103-104 defines mined as cited by >=1 used-by path; the row has one.
9. Used-by listed path exists and cites S071: HOLDS. corpus/knowledge/wave-settlement-r20.md exists; line 7 cites "S071 (desired vs current state vocabulary only — mori observes, it never reconciles)".
10. Used-by complete: BROKEN. CORPUS.md:107-108: used-by = "knowledge entries or lessons citing the row". corpus/lessons/round-20.md cites S071 at line 16 ("Sourced: S068, S069, S071.") and line 46. Not listed. S066-S069 carry the same omission.

## Evidence (commands, exit codes)
- awk over corpus/SOURCES.md, S071 row: NF=13; tier=B; status=mined; usedby=[corpus/knowledge/wave-settlement-r20.md]; rows with NF!=13 = 0.
- CORPUS.md:144-145 enum check over corpus/SOURCES.md: no output, exit 0 (S071 passes tier, status and kind enums).
- Tier x kind tally over corpus/SOURCES.md, exit 0: docs A 33, docs B 3, docs C 4; spec A 9; code A 11; tool A 4; paper A 1, C 1; book B 1, C 1; community B 1, C 2; own-work A 1.
- test -e corpus/knowledge/wave-settlement-r20.md -> exists; S071 occurrences in it = 1.
- Python fetch and exact-substring checks (eval): counts as in items 1-5.
- grep "(?i)detection|never (act|reconcile|close)|report only|reports only|observ" over .ufo/waves/round-20/contract.md: no matches. Read-only wording is at contract.md:56 and :113-115.

## Fix routing (not applied; I edited nothing)
- used-by is mutable in place, logged old->new in the round-20 lesson (CORPUS.md:116-117): add corpus/lessons/round-20.md.
- tier and teaches are not in the mutable set; a correction is a new row whose teaches opens "supersedes S071 —" (CORPUS.md:116-118). Either re-tier to A (and change the Gate "Admit B") or state the B basis under the definitions; I found none.
- teaches: keep clause 1; attribute the read-only rule to the lane contract, not S071.
- corpus/knowledge/wave-settlement-r20.md:7 carries the same clause-2 attribution in its parenthetical.

## Bounds disclosure
- Deviation: my first search (grep for S071) was rooted at the whole lane; the bounds allow named paths only. All matches were under .ufo/waves/round-20/ or corpus/; none under .ufo/interactive-sessions/, .ufo/worktrees/ or .jj/. I opened none of those and ran no further whole-lane search.
- I read /home/vgpnk/Projects/shokunin/CORPUS.md (fleet root; read-only: one grep, one range read) for tier and field definitions. It is not among the listed fleet items; flag it if that read is out of bounds.
- No scratch files written. No tool installs.
