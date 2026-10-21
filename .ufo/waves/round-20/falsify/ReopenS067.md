VERDICT: PARTIAL

The Gate quote holds byte-for-byte at its stated location, is 22 words, and is tier-B honest. The S067 row holds on tier, scope, anchor, status and opened. `teaches` is BROKEN: its census clause is lane application with no "not taught here" marker. Used-by holds on the defined check, but SKILL.md:498 cites S067 for the same over-reached clause and is not listed.

## Scope and state

- Row: `corpus/SOURCES.md:73`. Gate row: `corpus/lessons/round-20.md:44`. Source: https://michaelfeathers.silvrback.com/characterization-testing, re-opened today (reader text and raw HTML).
- The lane changed while I reviewed. At my first read, S067 used-by listed only `corpus/knowledge/drift-repin-r20.md`, and the knowledge note cited S067 at line 68. Now used-by also lists `corpus/lessons/round-20.md` (lesson line 55 records this as an in-place change), and the knowledge note cites S067 at line 70. Verdicts below are against these checksums (sha256, 16-hex prefix, final check): SOURCES.md `869e926dc9bb5a9c`; lessons/round-20.md `0e8afa6e22808c41`; knowledge/drift-repin-r20.md `125ed4aaeed5c605`; SKILL.md `dbf51a7fc4e7aa6a`; .ufo/waves/round-20/contract.md `2bbe9d56acddca6d`.

## Per-field verdicts

1. **Source re-open — HOLDS.** `curl -sSL -A … -o /tmp/ReopenS067/S067-raw.html -w "http_code=%{http_code} bytes=%{size_download}"` → `http_code=200 bytes=36970`, exit 0. `sha256sum` → `3d83cf24a8d4d7550ad321871543a654a0c821530cad4c6073eff97aec0d5408`, `wc -l` → 731, exit 0. This hash changes per fetch because of CSRF tokens, so it is not a stable identifier. Author meta "Michael Feathers"; "August 08, 2016" present in the raw HTML.
2. **Gate quote verbatim — HOLDS.** The 138-character string "The purpose of characterization testing is to document your system’s actual behavior, not check for the behavior you wish your system had." matches the raw article text exactly once, with U+2019 in "system’s". The ASCII-apostrophe variant matches 0 times. Lesson line 44 contains the same curly string once.
3. **Stated location — HOLDS.** The paragraph beginning "It’s a trick question." ends with this sentence; the next paragraph begins "Once, when I first started programming". Cosmetic only: the locator labels at lesson:44 and SOURCES:73 write "It's" with an ASCII apostrophe, while the source uses U+2019. The quote itself is unaffected.
4. **≤25 words — HOLDS.** Quoted span: 22 words (`str.split`). The whole Decision cell is 33 tokens including "Admit B." and the locator. I read the limit as applying to the quote.
5. **Tier B — HOLDS.** An informal essay by the term's author, explicitly non-normative: B fits. Not A: lesson:48 states the lane rule "official project docs are tier A (CORPUS.md tier rule)", and a personal blog is not official project docs. Not C: no rejection reason is recorded. [INFERENCE: the CORPUS.md rule text itself was not located; see G1.]
6. **Scope — HOLDS, with external attribution.** The essay supports the quoted purpose. "coiner's" and "(golden-master)" are not in the essay (0 hits each for coin, golden, master). Wikipedia "Characterization test" (fetched via read) supports both: "This term was coined by Michael Feathers." and "also known as Golden Master Testing". A web search returned the same attribution.
7. **Anchor — HOLDS.** Section "Characterization Testing" exists; the paragraph and its final sentence were verified (item 3).
8. **Teaches — BROKEN.**
   - Clause 1 holds: "A behavioral baseline documents actual behavior, not desired behavior" restates the essay's purpose sentence.
   - Clause 2 is lane application, not taught by S067: "a re-pinned census baseline certifies sameness since the pin, never health". The essay has 0 hits for pin, re-pin, census, baseline, sameness and health.
   - The nearest essay text supports only a principle: "descriptions of what we have rather than statements of correctness" and "it becomes its own specification … regardless of whether we think it’s right or not".
   - The lane's own standard requires such clauses to be marked. Wave-2 corrections did this: S073 says "Rejecting .. and absolute trailer paths … is mori's own tool rule, not taught by this page"; S074 says "mori's observe-only stance is the lane's own boundary, not taught here". S066 marks its census application as "grounds … for the census drift baseline". S067 has no marker.
   - The over-reach repeats at `SKILL.md:498` ("A re-pinned baseline certifies sameness since the pin, never health (S067)") and at `corpus/knowledge/drift-repin-r20.md:70` ("Sameness of census behavior … (S067)").
9. **Status — HOLDS.** `mined`, with two used-by paths; consistent with the two consuming artifacts.
10. **Opened / recheck — HOLDS.** The opened field and the Gate Access column agree with today's re-open. Recheck 365d; no conflicting evidence.
11. **Used-by, as defined (paths exist and cite S067) — HOLDS.** `corpus/knowledge/drift-repin-r20.md` exists and cites S067 at lines 7–8 and 70. `corpus/lessons/round-20.md` exists and cites S067 at lines 14, 44, 51, 55 and 73.
12. **Used-by completeness — GAP (observation, outside the brief's defined test).** `SKILL.md:498` cites S067 for the over-reached clause and is not listed. Lesson:55's convention ("lessons citing a row are listed") does not reach SKILL.md. This is a gap only if used-by is meant as an exhaustive consumer list. Flip: if that reading is adopted, list SKILL.md or remove the citation together with the teaches fix.

## Other observations (non-blocking)

- Kind: the row says `docs` for a personal blog. The registry's blog precedent is `community` (S030, S055). Nit.
- Reproducibility: no hash or archived copy of S067 is recorded, while S066 and S070 have one. A whole-page hash is unstable, so record a sha256 of the normalized article paragraph.
- Cross-row, not reviewed: S068 `teaches` ("A report-presence check must lstat the final component") has the same shape, a lane application under a source title with no marker. Its own falsifier should apply the same standard.

## Recommended fix (for L1; I changed nothing)

- Follow the append-only pattern of S069→S073 and S071→S074. Add a superseding S067 row whose `teaches` is narrowed to "A characterization baseline documents actual behavior, not desired behavior; a system in production becomes its own specification, so a change must be detected whether or not it is right", and add: "The census re-pin rule (sameness since the pin, never health) is mori's own application, not taught by this essay."
- Narrow the S067 attribution at `SKILL.md:498` and `drift-repin-r20.md:70` to the principle.
- Scope the Gate admission as S071 does ("Admit B, vocabulary only"). The current "Admit B." carries no qualifier.
- Flip: if the row marks clause 2 as application using the S066 "grounds … for" pattern, `teaches` becomes HOLDS.

## Gaps (not verified)

- G1: `CORPUS.md` is cited as the tier rule (lesson:48) and as the used-by convention (lesson:55). It is not at `corpus/CORPUS.md` or the lane root, and a listing of `corpus/` shows no such file. `corpus/README.md` has no tier legend. The tier verdict therefore rests on registry precedent [INFERENCE].
- G2: The reverse-citation check covered named files only: SKILL.md, PROVINCE.md, contract.md, the round-20 lesson, the knowledge note, wave-settlement-r20.md, drift-classification-r20.json, the baseline-r20 JSON, and tools/mori-wave-settlement.py. Other corpus citers were not searched, per bounds.
- G3: The wave-2 scribe notes (`build/Src*.md`) were not read; they are not named for S067.

## Evidence summary (exact commands, exit codes)

- `curl … -w "http_code=%{http_code} bytes=%{size_download}"` → `http_code=200 bytes=36970`, exit 0.
- Python exact-match on the raw HTML: curly apostrophe count 1, ASCII count 0; trick paragraph ends with the purpose sentence: true; quote words 22; essay term counts 0 for pin, census, baseline, health, sameness, golden, master, coin.
- Lesson line 44 exact-quote check: 1 match.
- SOURCES raw line 73, used-by cell: `corpus/knowledge/drift-repin-r20.md, corpus/lessons/round-20.md`.
- Installs or updates: none. Tools used: curl 8.23.0 (already present), the Python eval kernel, and the read and grep tools.
- Bounds: read-only on lane files; scratch only under /tmp/ReopenS067/ and this report; no reads of `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/` or ~/.omp; no whole-lane grep; no subagents; no peer messages.
