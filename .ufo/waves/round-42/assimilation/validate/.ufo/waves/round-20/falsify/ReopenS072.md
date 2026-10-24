PARTIAL. Quote text, word limit, tier and status/used-by hold. "Teaches grounded" is BROKEN for the rejection rationale "adds nothing over S067 for the re-pin ritual"; the lead-only teaching holds.

## Field verdicts
1. Quote verbatim at the stated location (lead sentence): HOLDS
2. Quote <=25 words: HOLDS (14 words)
3. Tier honest for its scope: HOLDS (C = tertiary; no tier legend readable in the repo, see F3)
4. Teaches grounded: BROKEN for SOURCES.md:78 "adds nothing over S067 for the re-pin ritual"; HOLDS for the lead-definition scope and for the lesson's lead-only wording
5. Status / used-by consistent: HOLDS (registry rule has zero exceptions); caveat: the lesson's general used-by sentence overstates practice

## Snapshot (lane files changed during this session; refs are to these)
- corpus/SOURCES.md sha256 f2ff7d92d9b9ac3a4ee92baf96c8fbb1c1cdcfe11203f082e2ec80729d90b42f, 119 lines, 75 rows. S072 row at :78; text unchanged from my first read.
- corpus/lessons/round-20.md sha256 65c7ad2bca3eb3ab38f01d8f5128ee50964c67995503fcbd9fb8fb671c109805, 79 lines. S072 Gate row at :52 (was :47 at my first read; shifted as S073-S075 were added above), spot-check at :74. Row text unchanged.
- Wikipedia observed 2026-10-21: lastrevid 1374190248, touched 2026-09-29T19:11:09Z.

## F1 verbatim at stated location: HOLDS
- Lesson :52 quote equals Q byte-for-byte: "a means to describe (characterize) the actual behavior of an existing piece of software" (ASCII). [checks2: "HOLDS F1 Gate-row quote byte-equal to Q"]
- Rendered page: Q occurs once, in the lead sentence (whitespace normalized): "In computer programming, a characterization test (also known as Golden Master Testing [1]) is a means to describe (characterize) the actual behavior of an existing piece of software, and therefore protect existing behavior of legacy code against unintended changes via automated testing." Overview follows. [checks2: "occurs exactly once", "sits in the lead"]
- Caveat: raw HTML has `<b id="mwCw">actual</b>` and the wikitext has `'''actual'''`; raw-byte count is 0. Verbatim as rendered text only.
- Caveat: anchor "lead paragraph; fetched 2026-10-21" pins no revision id or hash.
- Observed: the reader's Markdown repeats the lead, once without the alias; rendered HTML has one occurrence.

## F2 <=25 words: HOLDS
- len(Q.split()) = 14. [checks2: "HOLDS F2 Q <= 25 words | words=14"]

## F3 tier honest for scope: HOLDS
- SOURCES.md:78 is `docs | C`, status rejected. Registry pairs (75 rows): A/mined 38, A/queued 23, A/rejected 1 (S054), B/mined 3, B/queued 2, C/rejected 8. Every C row is rejected. S067 is B (:73); tertiary S072 at C fits the row's own "tertiary summary" wording.
- Legend gap: the S074 Gate row cites "CORPUS.md tier rule" (official project docs = A). CORPUS.md is not at the lane root (directory listing) or in corpus/ (direct reads: "not found"); SKILL.md, PROVINCE.md and corpus/README.md do not mention it (grep). Fleet root not searched (bounds). Tier judged on the row's own characterization. [INFERENCE]
- Label: kind "docs" is loose for an encyclopedia article; the registry uses "community" for non-normative web prose (S021, S030, S055). Not a tier error. [INFERENCE]

## F4 teaches grounded: BROKEN (rationale); HOLDS (lead teaching)
- Lead teaching holds: the lead defines the test as describing actual behavior and protecting legacy behavior from unintended change, with the alias "Golden Master Testing" (rendered lead; wikitext lead).
- Rationale is BROKEN as written (SOURCES.md:78 teaches cell):
  a. Coverage limit. Wikipedia Overview: "Unfortunately, as with any testing, it is generally not possible to create a characterization test for every possible input and output." Counts: S067 essay "every possible input and output" 0, "coverage" 0, "branch" 0; S066 README phrase 0, and "cover" appears once, in a dependency note on covering pairs. [checks2: "body[coverage-limit] wikipedia=1 S067=0 S066=0"; "F4b FINDING ... True"]. Relevance to what a re-pinned baseline certifies (the question SOURCES.md's "Bounded search 11" names) is [INFERENCE]. Tier C is not claim-admissible in this registry, so the caveat cannot be cited from S072 [INFERENCE].
  b. Change detectors. Wikipedia: "Characterization tests are, essentially, change detectors. It is up to the person analyzing the results to determine if the detected change was expected and/or desirable..." The exact phrases are absent from S067 and S066, but S066 README:75 carries the same decision rule ("update the master because you expected the changes and they are good"). The right comparator for this point is S066.
  c. Specification fallback: S067 "it becomes its own specification"; S066 README:72-73 "If no golden master exists you can create a snapshot". Covered in spirit by both.
  d. Anchor: the row anchors only the "lead paragraph", yet the rationale judges the whole article.
- The lesson's wording (Gate row :52; spot-check :74: "lead sentence ... adds nothing over S067") is lead-scoped and holds on this evidence. The registry wording is broader.
- Out of scope: the S067 essay has 0 occurrences of "golden", so the row's "(golden-master)" (SOURCES.md:73) is a gloss. The alias the Wikipedia lead adds is not in S067, so "adds nothing over S067" is also not literally true for the alias (not re-pin relevant).

## F5 status / used-by consistent: HOLDS (caveat on the lesson sentence)
- Status rejected: SOURCES.md:78; lesson :52 "Reject C."; spot-check :74 "agree reject C".
- used-by "—" (SOURCES.md:78). No paths, so no path-existence check (vacuous).
- Convention across 75 rows: all 41 mined rows list a used-by path (8 list a lesson); all 25 queued and all 9 rejected rows carry "—". Zero exceptions.
- Reverse citations under corpus/knowledge and corpus/lessons: only lesson :52 and :74. No knowledge note cites S072 or Wikipedia.
- Caveat: the lesson paragraph after the Gate table says "CORPUS.md: lessons citing a row are listed". Practice does not follow that sentence for S069 (mined, superseded), S070 and S075 (queued), or S072 (rejected). The cited CORPUS.md is absent (see F3). This is a documentation mismatch, not an S072 cell defect.

## Repairs for L1 (not applied; lane files untouched)
1. SOURCES.md:78 teaches cell: narrow "adds nothing over S067 for the re-pin ritual" to the lead, and state that the body's coverage-limit sentence is in neither S066 nor S067 and is not admitted. Or anchor the body.
2. Anchor S072 to revid 1374190248 (or re-fetch and re-pin).
3. Lesson used-by sentence: restrict to mined rows, or locate CORPUS.md.

## Out-of-scope observations (from the first registry read; not verified further)
- S059 row (:65): the REJECTED rationale sits in the anchor cell and the teaches cell reads "rejected".
- S069 is mined, superseded by S073, and lacks round-20.md in used-by although the lesson cites it.

## Reproducibility
- Scratch: .ufo/waves/round-20/falsify/ReopenS072/ holds s072.html, s072-wikitext.json, s072-info.json (Wikipedia, fetched 2026-10-21), s067.html (Feathers essay), s066-README.md (ApprovalTests at 5d98f0c; sha256 db6b2f6a...de0b matches SOURCES.md:72), checks.py, checks2.py.
- Command: `cd .ufo/waves/round-20/falsify/ReopenS072 && python3 checks2.py; echo "exit=$?"` gives exit=1. The only failing check is the lesson-sentence rule in F5 (documentation). All F1-F4 checks HOLD and the F4b FINDING prints True.
- First run (checks.py, hard-coded lesson :47) printed three MISS lines. They were artifacts of the line shift (:47 to :51) and registry growth (72 to 74 rows), not content changes. checks2.py locates rows by content. Disclosed here, not hidden.

## Tooling and bounds
- No installs or updates. Used curl and python3, both already present.
- Read-only on lane and fleet; no edits to corpus, tools, SKILL.md or PROVINCE.md; no git/jj commands. Did not open .ufo/interactive-sessions/, .ufo/worktrees/ or .jj/. Searches limited to named files and the corpus/knowledge and corpus/lessons directories; directory listings of the lane root and corpus/ only.
- Leaf seat: no subagents dispatched.
