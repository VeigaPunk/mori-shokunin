# ReviewCounterContract — count-c1.py vs its docstring and contract.md

Seat: MoriR32A2.ReviewCounterContract. Read-only review; no lane files touched except this report.
Counter: `.ufo/waves/round-32/count-c1.py` (frozen). Contract: `.ufo/waves/round-32/contract.md`.
Verification: ran the counter at the base on the lane repo and exercised its functions via `importlib` in a
Python harness (no repo writes). `pdftotext` present at /usr/bin/pdftotext. No installs needed.

## (1) P-C1 sentence: contract vs docstring

NOT byte-identical. The contract text (contract.md:32-34) and docstring text (count-c1.py:7-9) differ only in
line wrapping: identical words, identical punctuation, re-wrapped at different columns. Verified: raw `==` →
False; whitespace-normalised `==` → True (extract both with
`re.search(r'C1=met iff.*?new_ok>=1\)\.', text, re.S)`). The contract's own claim ("the same sentence", item 3
of §Routed defects, contract.md:75) holds only up to reflow. Any byte-diff audit would flag it; a word-diff does
not. Also note the contract P-C1 line carries markdown bolding around the label (`:**` …), not part of the
sentence itself.

## (2) Docstring vs code — divergences

### Code stricter or narrower than the docstring says

- D1. Header: docstring (count-c1.py:12) says "exactly `id | url | accessed | sha256 | quotes | verdict`".
  Code lowercases header cells (line 145) and strips each (line 74): `| ID | URL |…|` and
  `|id|url|accessed|sha256|quotes|verdict|` pass — confirmed empirically. Leniency, not a gap, but "exactly"
  is not enforced.
- D2. R1 "accessed is an ISO-8601 UTC time" (line 13). Code requires exactly `\d{4}-…T…Z` with seconds
  (line 235): `+00:00`, `z`, missing seconds, fractional seconds all fail. False-reject surface (§4).
- D3. R4 dispatch file: docstring says "a committed `.ufo/waves/round-32/*dispatch*.json`" (line 22). Code
  does `ls-tree -r` (line 206) so any `*.json` under the tree (including subdirectories like
  `.ufo/waves/round-32/judge/x-dispatch.json`) whose basename contains "dispatch" qualifies — wider than the
  docstring glob's implied flat directory. Basename substring vs `*dispatch*` glob is equivalent otherwise.
- D4. Docstring exit causes (line 36): "bad revision, population digest mismatch or usage". Code also exits 2
  on population *size* mismatch (line 188) — unreachable in practice since the digest check at line 184 fires
  first (digest pins the whole file). Dead-code divergence.
- D5. New-source row selection: code line 283 requires the literal `| S### |` opening (`^\| (S(\d{3})) \|`)
  and S\d{3} only — a row `|S175 |` or a future `S1000` id is silently skipped (never counted, never failed).
  Docstring (line 26) says "row s with id number >= 175 in corpus/SOURCES.md" without this format constraint.
- D6. New-source status: code requires `len(c) >= 11` AND `c[7] == 'mined'` (line 290). Column index 7 and the
  ≥11-column floor are hardcoded assumptions about the SOURCES.md column layout, unnamed by the docstring
  ("status mined"). Today's rows are 11 cells with `mined` at index 7 (verified on S015/S049).
- D7. Gate table: code hardcodes column positions g[1]=url, g[3]=sha, g[4]=quotes, g[-1]=decision and
  requires ≥6 cells (lines 295-299). Docstring names contents only; a correct gate table with columns in a
  different order, an extra leading column, or 5 cells fails `gate_rows`/`gate_url`.
- D8. Gate quotes: docstring (lines 28-29) reads "at least one double-quoted quote of 3-25 words found in the
  normalised copy". Code (line 307) requires EVERY extracted quote to be 3-25 words and in the copy: one valid
  quote plus a stray 2-word quoted fragment fails `gate_quote`.
- D9. R5: docstring (line 24) says "every corpus/knowledge/ path in p.used_by". Code line 258
  `if path.startswith('corpus/knowledge/')` silently SKIPS non-knowledge paths. S001's used_by is
  `corpus/lessons/2026-10-15-…md` only (verified in c1-population.json), so a `drifted` S001 passes R5 with
  ZERO corrections written — vacuous pass. Contract prose (contract.md:26) says "every knowledge entry in the
  row's used-by cell gets an appended Round32 correction naming the id", which matches the code, but neither
  names the S001 lessons-only hole: for S001 the "correction" lands nowhere.
- D10. Quote normalisation: `quotes_of` (line 109) applies `html.unescape` to every quote. The docstring's
  normalisation list (lines 32-34) applies entity unescape only to HTML-source text, not to quotes. For a
  plain-text or PDF copy the copy keeps literal `&amp;` while the quote is unescaped to `&` — confirmed:
  `normalise(b'fish &amp; chips plain…')` → `fish &amp; chips…` vs `quotes_of('"fish &amp; chips"')` →
  `fish & chips`, so `quote_not_in_copy`. An honest quote of a page containing a literal entity fails.
- D11. R3 "the URL fetched now (curl … up to 3 tries) yields bytes" (line 18): code `fetch()` (lines 116-120)
  yields EVERY successful try (up to 3), and `any()` (line 254) accepts if ANY one fetch's normalised text
  contains all quotes — more permissive than "the fetch" and it gives a rotating/A-B page up to 3 different
  versions a pass. Also `r.stdout` non-empty required (line 119): a `curl --fail` success with an EMPTY body
  counts as a fetch failure — an unreachable verdict can stand on a page that serves HTTP 200 with an empty
  body (and the seat's identical curl would have exited 0).
- D12. `--no-live` skips only the two `if live:` fetch blocks (lines 253, 264); the committed-transcript check
  (line 262) still runs. Docstring says "skips R3"; the transcript requirement is inside R3's sentence
  (line 19) yet survives. Consistent in effect (transcript is a file check), but the docstring is imprecise.

### Silent-drop / parsing behaviours the docstring does not name

- D13. `section()` (lines 123-133) requires the heading at column 0: `##  Recheck` (two spaces) or `##Recheck`
  yields an EMPTY section (verified) → `header_ok=False` and every id fails `shape`. `## Rechecks` correctly
  fails, `## Recheck <words>` is accepted. Any `## ` line inside a fenced code block inside the section still
  ends it (verified: section stops before the fence body).
- D14. `table()` (lines 136-150): the FIRST `|`-starting line in the section is the header. A stray `| … |`
  prose line above the real header makes the real header a body row and `header_ok=False` → all ids `shape`
  (verified). A blank line mid-table truncates the table ONLY once `body` is non-empty (lines 139-141):
  rows after the blank are silently dropped → `rows=0` (verified: row 2 of 2 dropped). Two back-to-back tables
  with NO blank line merge — the second table's header and separator become body rows (verified); a second
  table's `S00x` header-position cell can also create duplicate-id `rows=2` failures.
- D15. `quotes_of` (line 108): an odd number of `"` silently drops the trailing unclosed fragment (verified:
  `"one two three" stray "unclosed` → 1 quote). Typographic `“…”` delimiters extract ZERO quotes (verified) →
  `quote_shape`. Extra unquoted text in the quotes cell is ignored (docstring silent; seat rules do not forbid).
- D16. Non-`corpus/knowledge/` used_by entries skipped (D9); also `rid in ln` at line 259 is a SUBSTRING match:
  an added line mentioning `S0123` satisfies S012, and `Round32` need only appear on the same line, not in a
  `Round32` correction context.
- D17. `added_lines` (lines 153-158): a corrupt diff or a path absent at BASE returns `[]` (diff rc≠0) →
  `no_correction` rather than an error; fine in practice, silent.
- D18. `judged-sha256`/`judge-seat`/`judge-role` matched anywhere in the receipt (re.M on whole file,
  lines 201-203); a receipt carrying them inside a quoted block still counts. `judge-seat` `\S+` cannot contain
  a space. Malformed dispatch JSON files are `continue`d (line 211), silently.
- D19. `tokens` (line 112) `[a-z]+` drops digit-adjacent tokens (`v2.56.0`→no token, `utf8`→`utf` <4 dropped —
  verified) and non-ASCII letters; teaches/anchor/scope are NOT NFKC-folded before tokenising (line 250) while
  quotes are — asymmetric but harmless for today's population cells.
- D20. Id cell not normalized: url gets `strip('`<>')` (line 231), sha `strip('`')` (line 241), but `c[0]` is
  used raw (line 198) — a backticked id `` `S001` `` becomes a distinct key → `rows=0`. Likewise gate lookup
  `g[0]` (line 280) is raw. New-source "absent from base" test is `u in base_src` substring (line 292), so a
  URL that is a prefix-substring of a longer base URL counts as present → `url_not_new` (false reject).
- D21. `accessed`/`judge`/`agrees` regexes: `- <r>: agree` must be the whole line (line 217): `- S001: agree.`
  or `- S001: agree (with note)` fails `judge` on an honest receipt. `judge_ok` requires `jm.group(1) == sec_sha`
  with lowercase-only hex (line 201).
- D22. `verdicts` count (line 232) runs before the validity check, so `verdicts=` may report invalid verdict
  strings — cosmetic only.
- D23. R3 re-fetch uses `p['url']` (line 254), not the row's url cell — consistent since R1 pins them equal.

### Docstring checks the code does not additionally impose (counter permissive vs seat rules)

- D24. Quote substring containment is not whole-word and does not require negations/prefixes be kept: the
  seat-side guidance forbids page furniture and dropped negations (contract-context c1-controls.txt), but the
  counter's `q in ntext` is a plain substring. `"protected"` carved out of `"unprotected"` PASSES the counter;
  only the judge row-gate catches it. Frozen design; recorded as residual risk.
- D25. R2 "1-3 quotes" counts only well-formed double-quoted spans (D15); a cell with 2 closed quotes plus an
  unclosed third counts as 2 and passes `quote_shape` if both are valid.

## (3) Exit codes — all verified by running

- `count-c1.py` (no args) → usage line, exit 2. `count-c1.py deadbeef` → `unresolved C1=error exit=2`.
- `count-c1.py 641a6e86` (live): `recheck_rows=0 header_ok=False section_sha256=e3b0c44298fc1c14
  judge_ok=False judge_seat_ok=False judge_agree=0`, `rows_ok=0/34`, `new_ok=0`, `C1=unmet exit=1`.
  Exactly the contract's declared before (contract.md:47-48). 34 `rows=0` failures, all population ids.
- `count-c1.py 641a6e86 --no-live` → `C1=diagnostic exit=1`. Matches docstring line 36-37.
- Digest-mismatch and size-mismatch exits 2 at lines 184/188 (size check unreachable after digest, D4).
- `--section-sha <file>` (lines 162-165) prints sha256 of the Recheck section and exits 0 — undocumented mode;
  same `section()` function as the main path, so judge-side sha computation is consistent.

## (4) False-reject risk for an honest, correct row

High-probability traps, ordered:

1. Pipe parsing: a literal `|` inside a quote MUST be written `\|` in the cell, else `cells()` (line 74) splits
   it and the row fails `shape` (verified: `"a|b"` → 7 cells). Seat guidance already mandates `\|` — good —
   but any unescaped pipe anywhere in the row (e.g. in `url`, impossible) breaks it. `\|` inside NON-quote
   cells is never unescaped.
2. Table layout (D13/D14): blank line mid-table silently drops every later row (`rows=0`); a stray `|` line or
   prose table before the real header flips `header_ok=False` → all rows `shape`; `##  Recheck` or a second
   `## ` inside the section (incl. inside a code fence) truncates. One malformed line fails the whole claim,
   and the failure surface (`shape`, `rows=0`) is diagnosed only via `row_failures`.
3. `accessed` strictness (D2): only `YYYY-MM-DDTHH:MM:SSZ` accepted; `+00:00`, fractional seconds, or missing
   seconds fail even though ISO-8601 UTC. Conversely `2026-13-99T99:99:99Z` passes (regex + string compare) —
   invalid dates accepted. Seats writing `date -u +%FT%TZ` are safe; MIN_ACCESS `2026-10-23T01:00:00Z` is in
   the past relative to this wave (now ≈01:46Z; freeze commit 2026-10-23T01:10:09Z) so no clock trap for rows
   fetched after freeze — but any row fetched between 00:00Z-01:00Z would have failed `accessed`.
4. `&amp;` in quotes of non-HTML copies (D10): unescaped in the quote, not in the copy → `quote_not_in_copy`.
   HTML copies are fine (both sides unescape). Plain-text copies (e.g. RFC S041, raw markdown) that contain a
   literal `&amp;` sequence cannot be honestly quoted across it.
5. Typographic quote delimiters `“…”` in the cell extract zero quotes → `quote_shape` (D15).
6. Uppercase or 5-cell variant of the header? Header is case-INSENSITIVE (D1) so `ID` is fine — no risk there;
   but a separator of only 2 dashes (`|--|`) is NOT recognised as a separator and becomes a body row
   (verified) — with id cell `--` it causes no id collision but adds a phantom row.
7. Judge line shape (D21): the receipt's `- <r>: agree` must end the line; any trailing text fails `judge` for
   that id. `judge-seat` must be a single token matching a `name` in a `*dispatch*.json` task with
   `agent == 'reviewer'` (today's dispatch files use top-level `tasks[]` with `name`/`agent` — compatible).
8. Live drift between seat fetch and counter fetch → `live_quote` (inherent to the design; the `any` over 3
   successful fetches mitigates for rotating pages). Rotating content also means an honest row can pass on a
   fetch the seat never saw — mild false-ACCEPT, not reject.
9. New-source silent drops (D5/D6/D20): non-`| S### |` spacing, <11 columns, a URL that is a substring of a
   base URL, backticked gate id — each makes the row invisible or failed; `new_ok>=1` needs only one survivor.
10. S001 drifted-vacuity (D9): not a reject — the opposite: `drifted` on S001 passes R5 with no correction at
    all. If an honest seat verdicts S001 `drifted` and writes the correction into the lessons file, R5 still
    passes without checking it.

## Residual risk / verification gaps

- Whole-word/negation quote honesty is enforced only by the judge seat, not the counter (D24) — the known
  trust limit (contract.md:63-65) plus this substring leniency means the receipt is load-bearing for both R4
  and quote fidelity.
- The live R3 check was NOT exercised against the 34 real URLs here (bounded read-only review; no row data
  exists yet to form a passing row). Parser paths verified via direct function calls on synthetic inputs.
- `--no-live` still enforces transcript files (D12) — a diagnostic run reports `no_transcript` failures; that
  is the intended strict diagnostic but worth naming since the docstring says "skips R3".
- Counter was run only at base; tip behaviour is the same code path over `git show <rev>:…`.

Evidence commands: `python3 .ufo/waves/round-32/count-c1.py 641a6e86` (output §3); function probes via
`importlib.util.spec_from_file_location` on the frozen file; P-C1 extraction regex above. All runs read-only
on the lane repo (counter itself performs only `git show/diff/ls-tree/rev-parse` plus curls it never reached).
