# Round-32 live recheck of the mutable-URL source rows

What this directory holds: one fetched copy `<id>.src` for each of the 33 population rows that served bytes, and the
failed-fetch transcript `S056.fetch.txt` for the one row that did not. The population is the 34 `mined` rows of
`corpus/SOURCES.md` at `641a6e86` whose first URL is not pinned to a tag or commit
(`.ufo/waves/round-32/c1-population.json`). The verdicts and quotes are in the `## Recheck` table of
`corpus/lessons/round-32.md`. The counting command is `python3 .ufo/waves/round-32/count-c1.py <rev>`. Every copy was
fetched by a round-32 wave-1 seat between 2026-10-23T01:31:22Z and 01:31:35Z. The seat reports are under
`.ufo/waves/round-32/w1/Recheck*.md`. The bytes are unchanged; `sha256sum <id>.src` equals the row's sha256 cell.

## Method and the sources it rests on

1. **Fetch.** Each fetch is `curl -sSL --fail -m 60 <url>`, tried up to three times, the same call the counter's R3
   replays. S175, the curl(1) manual (https://curl.se/docs/manpage.html), grounds each flag. `--fail` makes curl fail
   with error code 22 and write no body when the server answers 400 or above, so an error page is never saved as
   page text. `--location` makes curl redo the request at the new place, so a redirected URL (S041 and S062 redirect
   to `rfc-editor.org/info/…`) saves the final page. `--max-time` caps each transfer, and exit code 28 is the timeout.
   A row is `unreachable` only when all three tries fail. S056 (pnas.org) answered `403` with a bot challenge on
   every try. The challenge was not passed, and the counter's own three fetches fail the same way.
2. **Normalise.** Quotes are matched against normalised text, not raw HTML. Tags and script/style blocks are
   dropped, and character references are decoded with `html.unescape`. S177, the Python `html` module docs
   (https://docs.python.org/3/library/html.html), says this converts all named and numeric character references to
   Unicode characters under the HTML5 rules. Then NFKC is applied. S176, the Python `unicodedata` docs
   (https://docs.python.org/3/library/unicodedata.html), defines NFKC as the compatibility decomposition followed by
   the canonical composition. NFKC leaves typographic quotes and dashes unchanged (wave-1 SrcUnicodedata measured
   this), so the counter folds them to ASCII in a separate step.
3. **Quote and judge.** Each row's quotes must sit inside both the committed copy and a live re-fetch. A non-author
   reviewer then checks them against the row's `teaches` cell. The receipt names the sha256 of the exact `## Recheck`
   bytes it judged.

## Limits (measured before data, wave C0, `.ufo/waves/round-32/evidence/c1-controls.txt`)

- Token overlap is not support. A real on-topic sentence can pass R1–R3 without supporting the teaches cell, and a
  quote can cut a negating prefix. Only the judge catches these.
- The population is first-URL only. A row whose teaches cell also rests on a second URL in its source cell (S058's
  `git-diff-tree` page; S117's tag-pinned code files; S128/S149's kernel sources) is rechecked only on its first URL.
- Tag URLs were excluded from the population as pinned. A force-moved tag is not measured here.
- Some pages change bytes on every fetch (S067 carries per-request tokens). For those, R3 checks that the quotes are
  still present, not that the bytes are equal.

## Sibling prior art (wave-1 ConnectorSiblings, `.ufo/waves/round-32/w1/ConnectorSiblings.md`)

Eight of the 29 URLs are also rows in seven sibling lanes. tabi round 18 already rechecked two of them (S047's and
S064's pages) with the same shape: one normaliser, one receipt per row, and `held | drift | unreachable` verdicts. Its
rule "dynamic full-page hashes are fetch identities, not semantic drift" (`tabi-shokunin/corpus/lessons/round-12.md:35`)
holds here too. Our S047 and S064 copies differ in raw bytes from tabi's 2026-10-20 bodies, only in an asset
fingerprint in the page head, and their normalised text is byte-identical. So a raw digest comparison would have
reported a false `drifted`. No sibling verdict sets a mori verdict; each row here is judged on its own copy.
