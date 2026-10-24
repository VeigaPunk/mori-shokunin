# RevLessonGate — round-40 lesson `## Gate` review (S229)

Axes: (1) the Gate row's claims against the committed source bytes; (2) locator
resolvability (copy path + line/section anchors); (3) lesson ↔ registry ↔
knowledge-entry consistency; (4) coverage by registered QUALITY checks.

Reviewed committed bytes at HEAD `ede486b7a09afbacfb380d5871c46a8051a6dc2e`;
the lesson row is unchanged since it landed at `8d3badd`. I edited no
production file; this report is the only write from this seat. (The lane
working tree at report time carries sibling-seat modifications to three c10
evidence files — `c10-after-conjunct.txt`, `c10-after-selftest.txt`,
`c10-red-conjunct.txt`, mtimes 03:01-03:02 — none touched or relied on by this
review; the reviewed artifacts are clean against HEAD.)

**Verdict: 3 of the 4 assigned checks pass; 2 concrete drifts found.** The
admission itself is not undermined — the quote is 17 words (≤25), verbatim,
with the copy path and access date named, and the registry teaches cell matches
the knowledge entry's claim. The drifts are (F1) a false word-count label in the
Gate row that the registered QUALITY 90 check fails on, and (F2) registry anchor
line numbers that do not resolve in the named copy.

## Assigned checks

### 1. Located quote ≤25 words — PASS (but see F1 for its label)

`corpus/lessons/round-40.md:7` carries the quote:

> When a name is used in a code block, it is resolved using the nearest enclosing scope.

- Measured: 17 words (≤25).
- Located at `corpus/evidence/sources-r40/S229.src:294-295`; one occurrence in
  the tag-stripped copy; byte-verbatim after the single line wrap (the period is
  carried; no elision/alteration).
- The row's own `(15 words)` label is false — F1.

### 2. Copy path named — PASS

`corpus/lessons/round-40.md:7` names `corpus/evidence/sources-r40/S229.src` in
the source cell and `S229.src` in the quote cell. The path exists at HEAD and
the committed blob equals the working-tree file
(`sha256 a7774d77ad6aa9da64484be0f7954b78d5daf497fc73219b1935dbb67304ca54`
on both sides); `git status --porcelain` over the three artifacts is empty.

### 3. Access date named — PASS

`opened 2026-10-24` in the Gate row, consistent with
`corpus/SOURCES.md:235` (`page fetched 2026-10-24`; opened column
`2026-10-24`), `corpus/knowledge/conform-scope-r40.md:6`
(`verified-at: 2026-10-24`), the copy footer `S229.src:858`
(“Last updated on Oct 24, 2026 (03:37 UTC)”), and commit `265a955`
(`2026-10-24T02:47:29-03:00` = 05:47 UTC). Gap: the footer is a docs build
stamp, not an access stamp; the access date is corroborated, not byte-proven.
The URL `https://docs.python.org/3/reference/executionmodel.html#naming-and-binding`
is identical in the Gate row, the registry row and the entry header, and the
fragment resolves in the copy (`id="naming-and-binding"` at `S229.src:248`).

### 4. Teaches cell matches the knowledge entry's claim — PASS

The Gate table has no teaches column (`source | decision | located quote`), so
the teaches cell under review is `corpus/SOURCES.md:235`:

> An assignment inside a function block binds the name locally for the whole
> block, so a module-map constant fold must read a function-local binding
> before any module-level map.

`corpus/knowledge/conform-scope-r40.md:16-19` claims:

> An assignment anywhere in a function block binds the name locally for the
> entire block, so a read of `TIMEOUT` inside `run()` resolves to the
> function-local binding even when a module-level `TIMEOUT = 120` exists.

Same rule (function-block assignment ⇒ local for the whole block) and same
consequence (function-local read ahead of the module map); only wording and
worked example differ. No drift.

## Findings

### F1 — MEDIUM: Gate word-count label is false (15 vs 17); QUALITY 90 fails at HEAD

- `corpus/lessons/round-40.md:7`: `…nearest enclosing scope." (15 words)`.
- The carried quote measures 17 words; the committed QUALITY 90 check over HEAD
  bytes prints
  `line=7 label=15 wc=17 quote=When a name is used in a code block, it is resolved using the nearest`
  and `word_labels=1 mismatched=1`, exit `1`.
- This is the exact defect class the round-39 erratum fixed for S227 (label 18,
  actual 17), and QUALITY 90 states “A label that differs by one is a defect,
  not rounding” (here the label is two low). It also contradicts the round's own
  M23/M24 measured-numbers discipline.
- The false count is repeated in `LOG.md:2305` (“15-word located quote”) and was
  seeded by the wave spec generator, `.ufo/waves/round-40/gen-wave-spec.py:80`
  (“(15 words, section 4.2.2)”), which the draft seat copied.
- Fix shape (not applied; reviewer seat is read-only): an append-only
  correction in the round's erratum/SCORECARD record naming the measured 17, in
  the `corpus/lessons/round-39-erratum.md` precedent; do not silently rewrite
  the committed lesson row. LOG's parallel sentence needs the same correction.

### F2 — MEDIUM: S229 registry anchor line numbers do not resolve in the named copy

`corpus/SOURCES.md:235` anchor cell:
`§4.2.2 Resolution of names:249-262; "When a name is used in a code block, it
is resolved using the nearest enclosing scope":254-256; page fetched 2026-10-24`.

In the named copy `corpus/evidence/sources-r40/S229.src` (868 newline-terminated
lines):

- §4.2.2 heading is line **288**; §4.2.3 starts at line **356** — so the
  section span is 288-355, not 249-262.
- The quoted sentence starts at line **294** and ends at line **295**; the
  anchor's `:254-256` points into §4.2.1's “constructs bind names” list
  (formal parameters/class definitions/function definitions), not the sentence.
- The copy-line convention is established: S227's `:2542-2544` and S228's
  `:657-659` land exactly on their quoted lines in their own copies. S229 is
  the outlier. The numbers match neither the committed HTML (288/294-295) nor
  upstream `Doc/reference/executionmodel.rst` (heading 100, sentence 113); they
  appear to be from a third rendering, the QUALITY 61 class (“a reader's
  transport presentation is not source bytes: never integrate line anchors”).
- No registered check catches it. `scripts/sources-census.sh`'s validate branch
  checks field count/id/kind/tier/status/opened/recheck and URL duplicate
  classes only; a re-run exits 0 with no S229 line. `tools/` has no resolver for
  SOURCES anchor line numbers. Census `ok` is therefore not evidence for the
  anchor.
- QUALITY 113 makes the registry `anchor` cell immutable: the correction must
  ride an appended erratum note or a superseding row, never an in-place anchor
  edit (an in-place edit would also appear in the round's own append-only gate).
- The lesson Gate row's locator is section-level (`§4.2.2`) and therefore
  neither repeats nor catches the bad lines. Recording `S229.src:294-295` (and
  302-307 for the corollary, see F3) in the correction would restore
  resolvability.

### F3 — LOW: the quoted sentence grounds the entry's principle, not the teaches-cell corollary by itself

The quote at 294-295 states nearest-enclosing-scope resolution. The teaches
cell and the entry claim assert the whole-block local-binding corollary, whose
supporting sentence is at 302-307 of the same §4.2.2 (“If a name binding
operation occurs anywhere within a code block, all uses of the name within the
block are treated as references to the current block … The local variables of a
code block can be determined by scanning the entire text of the block…”). The
entry itself pairs the quote with that corollary, so this is not a
teaches/entry mismatch; it is a verifiability gap — a verifier checking only
the quoted sentence cannot confirm the teaches cell. Recommend the correction
cite 302-307 alongside 294-295.

### F4 — LOW, out of S229 scope: Gate decision cell / reject declaration vs QUALITY 86

`round-40.md:7`'s decision cell is `**admitted** (mined)`; QUALITY 86's text
says each decision cell reads `admit, …` / `reject, <reason>` and a Gate with
no reject row carries `reject sample: none met`. `round-40.md:9` instead says
`Rejected: none new.`. QUALITY 86's published check at HEAD prints
`gate_reject_rows=0 none_declared=0 malformed=0`, exit 1 — but its row regex
(`^\| *S[0-9]+ *\|`) does not match the `| S229 — description | …` row shape,
so `malformed=0` is a checker blind spot and the exit 1 is the missing
reject-sample declaration. The shape predates round 40 (r37-r39 are identical),
so this is a round-template defect, not S229 content drift; route separately.

## Commands run (exact) and outputs

All from `/home/vgpnk/Projects/shokunin/mori-shokunin` unless noted. Read-only;
no pacman, no installs (none needed).

1. `printf '%s' 'When a name is used in a code block, it is resolved using the nearest enclosing scope.' | wc -w`
   → `17`
2. QUALITY 90's published check, verbatim, over `git show HEAD:` bytes with
   `lane=$PWD; rev=HEAD; round=40`:
   → `line=7 label=15 wc=17 quote=When a name is used in a code block, it is resolved using the nearest`
   → `word_labels=1 mismatched=1`, `EXIT=1`
3. `grep -n 'section-number">4\.' corpus/evidence/sources-r40/S229.src`
   → `249:…4.2. Naming and binding`; `251:…4.2.1. Binding of names`;
   `288:…4.2.2. Resolution of names`; `356:…4.2.3. Annotation scopes`;
   (also 409/453/469/488/523/525/586 for later sections)
4. `sed -n '249,262p' corpus/evidence/sources-r40/S229.src`
   → §4.2 heading + §4.2.1 heading + “The following constructs bind names:” list
5. `sed -n '294,295p' corpus/evidence/sources-r40/S229.src`
   → `<p id="index-8">When a name is used in a code block, it is resolved using the nearest enclosing` /
   `scope.  The set of all such scopes visible to a code block is called the block’s`
6. Python check over the copy + lesson:
   `lesson_quote='When a name is used in a code block, it is resolved using the nearest enclosing scope.'`
   `occurrences_in_copy 1`; `quote_is_substring True`;
   `anchor_fragment_id_present True`;
   `last_updated_markers ['Last updated on Oct 24, 2026 (03:37 UTC).…']`
7. `git cat-file -e HEAD:corpus/evidence/sources-r40/S229.src` → exit 0;
   `git show HEAD:corpus/evidence/sources-r40/S229.src | sha256sum` and
   `sha256sum corpus/evidence/sources-r40/S229.src`
   → both `a7774d77ad6aa9da64484be0f7954b78d5daf497fc73219b1935dbb67304ca54`
8. `git show HEAD:corpus/SOURCES.md | sed -n '235p'` → the full S229 row quoted above
9. `grep -n "An assignment anywhere in a function block" corpus/knowledge/conform-scope-r40.md`
   → `17:enclosing scope." An assignment anywhere in a function block binds the name`
   (`verified-at` at `:6`, `recheck: on-release` at `:7`)
10. `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
    → exit `0`; 17 lines; no `S229` line; last line
    `mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`
    (S228 W04 duplicate-URL line remains)
11. QUALITY 86's published check over HEAD → `gate_reject_rows=0 none_declared=0 malformed=0`, exit 1
12. `git log --format='%h %cI %s' -3 -- corpus/evidence/sources-r40/S229.src`
    → `265a955 2026-10-24T02:47:29-03:00 round-40: instruments — conform v3 (P-C10), gate v3 (P-C11), S229, r39 erratum`;
    `8d3badd 2026-10-24T02:56:11-03:00 …`
13. `curl -sSL https://raw.githubusercontent.com/python/cpython/3.15/Doc/reference/executionmodel.rst | grep -n "When a name is used in a code block\|Resolution of names\|Naming and binding"`
    → `39:Naming and binding`; `100:Resolution of names`; `113:When a name is used in a code block…`
    (proves the registry's 249-262/254-256 are not upstream-rst lines either)

## Residual risk / verification gaps

- The copy embeds no fetch timestamp; the access date rests on
  registry/entry/commit/footer agreement (all 2026-10-24).
- Nothing registered resolves SOURCES anchor line numbers, so F2 can recur
  silently; only an erratum/superseding row (or a new anchor checker) closes it.
- I did not run the C1/C2 counters, the conformance/gate selftests, or the
  claim receipts; those belong to other seats. My checks are documentation and
  locator checks over committed bytes only.
- F4 is a round-template defect shared with r37-r39; flagged, not owned here.
