# Mo94S01Src — independent non-author re-open of S624 (frontier step verification)

Seat `Mo94S01Src` (scout, leaf). Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`, not edited except this file. No registry row written. No installs/updates performed.

## 1. Primary source fetch — Python `str.startswith`

```
S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r94/Mo94S01Src"; mkdir -p "$S"
curl -sSfL https://docs.python.org/3/library/stdtypes.html -o "$S/stdtypes.html" \
  -w 'HTTP=%{http_code} SIZE=%{size_download} URL=%{url_effective}\n'
wc -c < "$S/stdtypes.html"; sha256sum "$S/stdtypes.html"; date -u +%F
```

```
HTTP=200 SIZE=815447 URL=https://docs.python.org/3/builtins/stdtypes.html
815447
2397d83204d8901b852e5dcb72cb1b5cbf311e9db1f15116089b85ab21d22b68  .../stdtypes.html
2026-11-05
```

- Requested `https://docs.python.org/3/library/stdtypes.html`; access date **2026-11-05** (UTC).
- Effective URL `https://docs.python.org/3/builtins/stdtypes.html`: the `library/` path answers `HTTP/2 301`, `location: https://docs.python.org/3/builtins/stdtypes.html` (followed by `-L`).
- Bytes **815447**, sha256 **2397d83204d8901b852e5dcb72cb1b5cbf311e9db1f15116089b85ab21d22b68**.
- Re-fetch determinism: second identical `curl` → same size, same sha256, `cmp` → IDENTICAL.
- Served headers: `HTTP/2 200`, `content-length: 815447`, `last-modified: Thu, 05 Nov 2026 09:44:02 GMT`, `etag: "6aec4fe2-c7157"`, `x-cache: HIT`.

## 2. Anchor, description text, phrase counts

`id="str.startswith"` occurs **exactly 1×** in raw HTML (offset 345856), in `<dt class="sig sig-object py" id="str.startswith">`. Its description `<dd>`:

```html
<dd><p>Return <code class="docutils literal notranslate"><span class="pre">True</span></code> if string starts with the <em>prefix</em>, otherwise return <code class="docutils literal notranslate"><span class="pre">False</span></code>.
```

Counts on two tag-stripped copies (`$S/stdtypes.tagspace.txt` = tags→single space; `$S/stdtypes.txt` = tags→empty):

| convention | `Return True if string starts with the prefix` | contract quote `Return True if string starts with the prefix , otherwise return False .` |
|---|---|---|
| tags → space | **1** | **1** |
| tags → empty | **1** | 0 |

```
grep -o -F "Return True if string starts with the prefix" "$S/stdtypes.tagspace.txt" | wc -l            # 1
grep -o -F "Return True if string starts with the prefix , otherwise return False ." "$S/stdtypes.tagspace.txt" | wc -l   # 1
grep -o -F "Return True if string starts with the prefix, otherwise return False." "$S/stdtypes.tagspace.txt" | wc -l   # 0
grep -n -F "Return True if string starts with the prefix" "$S/stdtypes.tagspace.txt"                     # 3095
```

**Finding (quote form).** The page's *visible* sentence is `Return True if string starts with the prefix, otherwise return False.` (no space before the comma). The contract's recorded quote (spaces before `,` and `.`) is reproducible **only** under the tags→single-space convention, because `</em>` and `<code>` intervene between the words. The head phrase is 1× under either convention, so the locator is safe; the full quote should be the visible form or name the stripping convention. `grep -o -F "starts with the prefix"` → **3×** (the other two are `str.removeprefix` and `bytearray.removeprefix`); in raw HTML that string → 0×.

## 3. Documented Python version

Yes — but as a `<title>`/nav string, not prose ("This is the documentation for Python 3.15.2" does **not** occur on this page).

```
grep -o 'Python[^<]\{0,30\}3\.15\.2[^<]\{0,30\}' "$S/stdtypes.html" | sort | uniq -c
      2 Python 3.15.2 documentation
grep -o '<title>[^<]*</title>' "$S/stdtypes.html"
<title>Built-in Types &#8212; Python 3.15.2 documentation</title>
```

Quoted: `<title>Built-in Types — Python 3.15.2 documentation</title>`; sidebar nav `<a href="../index.html">3.15.2 documentation</a> &#187;` (`li id="cpython-language-and-version"`); `title="Search within Python 3.15.2 documentation"`. `3.15.2` occurs 4× in the raw HTML. **Adjacency:** the body also mentions `Python 3.16` once ("Deprecated since version 3.12: … raise an error in Python 3.16."), so "Python 3." alone is ambiguous; `3.15.2` is the documented version.

## 4. Comparison with the entering record

| field | entering record (contract P5, L1) | this fetch | match |
|---|---|---|---|
| sha256 | `2397d83204d8901b852e5dcb72cb1b5cbf311e9db1f15116089b85ab21d22b68` | same | **yes** |
| bytes | 815447 | 815447 | **yes** |
| access date | 2026-11-05 | 2026-11-05 | yes |
| URL recorded | `.../3/library/stdtypes.html` | 301 → `.../3/builtins/stdtypes.html` | content identical |

**Verdict: exact match on digest and byte count; no divergence found.**

**Freshness caveat (for the landing row).** The page carries `last-modified: Thu, 05 Nov 2026 09:44:02 GMT` — the docs build was regenerated ~1 h before this fetch, so the digest pins a *build*. The row should carry `last-modified` too, so a later re-open can tell "page changed" from "record wrong". Same-day refetch was byte-identical, so L1's digest and mine are the same artifact.

## 5. Second source (optional) — `git-log(1)` (fetched cleanly)

```
curl -sSfL https://git-scm.com/docs/git-log -o "$S/git-log.html" -w 'HTTP=%{http_code} SIZE=%{size_download} URL=%{url_effective}\n'
sha256sum "$S/git-log.html"; wc -c < "$S/git-log.html"
```

```
HTTP=200 SIZE=375834 URL=https://git-scm.com/docs/git-log
f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b  .../git-log.html
375834
```

- Phrase `abbreviated commit hash`: **1×** (tag-stripped line 5482). Quote: the placeholder table "Placeholders that expand to information extracted from the commit:" → `%H commit hash` / `%h abbreviated commit hash` / `%T tree hash` / `%t abbreviated tree hash` / `%P parent hashes` / `%p abbreviated parent hashes`.
- Placeholder `%h` on the page: **7×** total (1 in that table, 6 in format examples). Freshness: `last-modified: Thu, 05 Nov 2026 04:35:23 GMT`, `etag: W/"6aec078b-5bc1a"`; body line 1310 `git-log last updated in 2.56.0`.
- Matches the existing **S622** row (`corpus/SOURCES.md:403`) byte-for-byte: same URL, 375834 bytes, same sha256 `f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b`. **S622 already exists (round 93) — no row written, as instructed.**

Read-only census: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori	ok	.../corpus/SOURCES.md`, rc=0 (non-fatal W04 warnings only, incl. `S622 duplicate url git-scm.com/docs/git-log across scopes`).

## 6. Adjacency to the C1 predicate

- Frozen v1 `.ufo/waves/round-93/count-c1.py:141`: `if ac and va and ac[:7] in va:` — substring, position-agnostic.
- Frozen v2 `.ufo/waves/round-94/count-c1v2.py:103`: `return len(tok) >= 7 and ac.startswith(tok)` — prefix at position 0, whole token.
- S624 sources exactly that distinction: `startswith` = "string **starts with** the prefix" (leading position), while the same page contrasts it with containment — `str.find` note, tag-stripped line 2377: "To check if sub is a substring or not, use the `in` operator: `>>> 'Py' in 'Python'` → `True`" (bytes twin, line 4010). The page itself separates prefix-equality from substring-anywhere, which is the v1-vs-v2 semantic gap.
- Still unsourced / named limit on the v2 rule: `len(tok) >= 7` is the lane's own threshold (not from the page), and `startswith` says nothing about the admission commit having introduced the file's current content.
- Host Python 3.14.8 docstring reads "Return True if the string starts with the specified prefix, False otherwise." — **different wording from the 3.15.2 docs page**. The contract's quote is the docs-page wording, not `str.startswith.__doc__`; a row quoting "the docstring" would not match.

## Remaining unknowns / limits of this seat

- The row is not written by me (S624 is appended at landing). If it quotes the spaced form, it should name the stripping convention or use the visible form (§2).
- No copy of `stdtypes.html` is retained in the lane (`find -name '*stdtypes*'` → nothing under the lane except unrelated `evidence/recheck-r32/S068.src` pages), so the digest is verifiable only by refetch; a future docs rebuild changes it (§4 caveat).
- No LSP device was reachable here (`xd://` exposes no `lsp` mount), so the Python-symbol facts in §6 come from direct reads and grep of the frozen artifacts, not a language-server definition query.

Scratch `/fast/scratch/hyaku/mori-r94/Mo94S01Src` removed on exit (`trap 'rm -rf -- "$S"' EXIT`).
