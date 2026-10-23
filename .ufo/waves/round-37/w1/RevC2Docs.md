# w1/RevC2Docs — SOURCES rows S221–S225 vs committed copies (round 37)

Item attacked: the frontier claim "SOURCES rows S221–S225 opened this round (copies
`corpus/evidence/sources-r37/`)" — specifically the row↔committed-copy binding: is each row's
located quote contiguous in the committed `.src` copy at the stated anchor lines, is it ≤25 words,
and does the row's teaches sentence rest on it? This is the docs arm of C2's corpus binding; a
fabricated or misplaced quote would pass C2's behavioral arms while the corpus lies about its
grounds.

Scope/bounds honored: lane repo read-only (no git/jj mutation, no lane file edited); this report is
the one file written; scratch was inline (no scratch files persisted). No tools installed (none
needed), no pacman. No `lsp` device applies — all five artifacts are plain-text/HTML data files with
no code symbols; direct byte reading is the ground truth here, and the one grep fallback used
(`tools/mori-source-drift.py` excerpt convention) is recorded below.

## Method

- Quote texts: `corpus/lessons/round-37.md` `## Gate` table (the round's own located quotes).
- Row anchor cells: `corpus/SOURCES.md` rows S221–S225 (registry columns: id, source, kind, tier,
  scope, anchor, teaches, status, opened, recheck, used-by).
- Copies: working tree is clean vs HEAD `0a05f7e6` (`git status --porcelain -- corpus/evidence/sources-r37/ corpus/SOURCES.md` → empty), so verified bytes = committed blobs. Blob binding:

  ```
  git ls-tree e57c58b57c025364e79d130fbdf764d2674d83d6 -- corpus/evidence/sources-r37/
    → S221 19a88abc…  S222 2df885ea…  S223 20fbd17a…  S224 aebc30f8…   (no S225)
  git ls-tree HEAD -- corpus/evidence/sources-r37/
    → same four SHAs + S225 51b848da…
  git diff --stat e57c58b..HEAD -- corpus/evidence/sources-r37/ → only S225.src (18915 insertions)
  ```

- Contiguity check (Python, whitespace-normalized; HTML copies verified as rendered text — inline
  tags (`a`/`code`/`span`/`strong`/`var`/…) dropped with no gap, block tags as breaks, entities
  decoded; S221 is plain RFC text, whitespace collapse only). This mirrors the corpus's own
  convention — the drift probe grades `excerpt` when "the copy bytes with whitespace stripped …
  occur contiguously" (`tools/mori-source-drift.py:19-20`, applied at `:206-207`) — and matches the
  readable-text nature of the Gate quotes; raw S222–S225 bytes carry interleaved markup, so
  raw-byte matching is the wrong standard for a rendered quote.
- Word count: whitespace tokens (`len(quote.split())`, wc -w equivalent).

## Per-row verification

| row | copy (lines) | lesson quote span | contiguous at span | words | ≤25 | row anchor cell | anchor ⊇ quote |
|---|---|---|---|---|---|---|---|
| S221 | S221.src (10 785; 19a88abc) | 7230–7234 | YES (plain text) | 25 | YES | §15.4:7230-7252 | YES |
| S222 | S222.src (5 402; 2df885ea) | 5031 | YES (rendered) | 23 | YES | note:5031; allowlist:5005-5006, 5017 | YES |
| S223 | S223.src (1 964; 20fbd17a) | 1140–1142 | YES (rendered) | 23 | YES | redirect_request:1129-1147; class:555-558 | YES |
| S224 | S224.src (259; aebc30f8) | 217–221 | YES (fits 217–218) | 20 | YES | ptrace_scope:178; "1 - restricted ptrace":217-221 | YES |
| S225 | S225.src (18 915; 51b848da) | 8355 | YES (wraps to 8356) | 9 | YES | §4.5:8318-8360; "redirect count is 20":8355 | YES |

Measured details (all from the copies above):

- **S221** — line 7230 opens `15.4.  Redirection 3xx`; the quote "The 3xx (Redirection) class of
  status code indicates that further action needs to be taken by the user agent in order to fulfill
  the request." is contiguous at 7230–7234 (RFC alignment spaces; normalized match exact=true).
- **S222** — line 5031 renders `Note: Disable the support for the following of the redirection in
  your web client in order to prevent the bypass of the input validation …` (quote contiguous,
  exact=true; `redirection` is a link, invisible in rendering). Anchor companions verified in range:
  5005–5006 (`Case when allowlist approach is available/unavailable`) and 5017 (allowlist viable
  when calls are between identified trusted applications).
- **S223** — 1140–1142 renders `The default implementation of this method does not strictly follow
  RFC 2616, which says that 301 and 302 responses to POST requests must not be automatically
  redirected without confirmation …` (quote contiguous, exact=true once `RFC 2616</a>,` and
  `<span class="pre">POST</span>` markup boundaries are rendered). Class anchor 555–558:
  `class urllib.request.HTTPRedirectHandler — A class to handle redirections.`
- **S224** — 178 is the `ptrace_scope` heading; 217–218 renders `1 - restricted ptrace: a process
  must have a predefined relationship with the inferior it wants to call PTRACE_ATTACH on.` and the
  claimed span 217–221 additionally contains `By default, this relationship is that of only its
  descendants when the above classic criteria is also met. To change the relationship, an inferior
  can call prctl(PR_SET_PTRACER, debugger, …)`.
- **S225** — 8318 opens `4.5. HTTP-redirect fetch`; line 8355 renders `If request's redirect count
  is 20, then return a` and 8356 completes `network error.` — the Gate quote "redirect count is 20,
  then return a network error" is contiguous across 8355–8356 (the Gate's ":8355" names the start
  line; the row's §4.5:8318-8360 range covers both). The same range contains `Increase request's
  redirect count by 1.`

## Teaches support

All five teaches sentences are supported by their quote + anchor-range text:

- **S221** — "A 3xx answer is not the resource body: the client must take further action…" — the
  range gives the further-action requirement and names `Location`-header redirects; supported.
- **S222** — "Disabling redirect-following in the client is a named countermeasure against allowlist
  bypass…" — the quote is exactly that countermeasure, with the allowlist cases in range; the second
  clause (probe checks final destination) is the lane's own inference and is disclosed as a named
  limit ("Final destination only") in `corpus/knowledge/source-drift-hardening-r37.md`.
- **S223** — "urllib's default redirect handler is a class with its own documented deviations…" —
  class anchor 555–558 plus the RFC 2616 deviation at 1140–1142; supported. The Gate note discloses
  the mid-sentence cut (sentence continues "by the user") — verified in the copy.
- **S224** — "At ptrace_scope 1 a process may attach only to its descendants…" — supported by the
  level-1 text in range (see INFO-2 for the dropped nuance); the entry frames it as host policy.
- **S225** — "A fetch re-issues the request per hop and stops after twenty redirects…" — the
  twenty-hop stop is in range; the re-issue step exists at S225.src:8478–8483 ("running main fetch
  given fetchParams and recursive", just before §4.6) — see INFO-3.

## Findings

**LOW-1 — S225.src is absent from the scored freeze tip e57c58b.**
`git cat-file -e e57c58b…:corpus/evidence/sources-r37/S225.src` → `fatal: path … exists on disk, but
not in 'e57c58b…'`; `git ls-tree e57c58b…` lists only S221–S224. So at the commit the wave context
names as scored tip, row S225's "committed copy" binding did not hold; the row cites a copy that
commit does not carry. Repaired at `52d636d` ("round-37: S225 source copy (named explicitly; 1.9 MiB
skipped by the directory form)") and present at HEAD `0a05f7e6` (blob 51b848da). Self-documented as
lesson M5 (helper commits a named directory and skips new files over 1 MiB; mechanism captured).
S221–S224 blobs are byte-identical between e57c58b and HEAD, so those four bindings hold at the
freeze tip. No further defect beyond the one the lesson already records.

**INFO-1 — S222's quote ends mid-sentence, undisclosed in the Gate notes.** The copy continues
"…input validation **described in the section Exploitation tricks > Bypassing restrictions > Input
validation > Unsafe redirect** of this document." The Gate notes disclose mid-sentence/clause cuts
for S223 and S225 but not S222. The quote is verbatim-contiguous and the cut serves the 25-word
guard; disclosure asymmetry only, no contract breach found (registry cells carry no word-count label
to be wrong, cf. the round-30 correction).

**INFO-2 — S224 teaches drops the opt-in nuance.** Teaches: "may attach only to its descendants";
the same anchor range states "By default, this relationship is that of only its descendants when the
above classic criteria is also met" plus the `prctl(PR_SET_PTRACER, …)` escape. Substantively
supported (default behavior; the entry's limit section calls it host policy, not counter design);
precision note, no misquote.

**INFO-3 — S225's re-issue claim sits just past the anchor cut.** The row anchor stops at 8360 (the
redirect-count increment); the recursive `main fetch` re-issue is at 8478–8483. The anchor range
still covers the load-bearing twenty-hop step and the quote; note only.

## Residual risk and verification gaps

- This item re-opened rows against **committed copies**; it did not re-fetch the five URLs, so
  live-source fidelity is not re-established here (that is the drift probe's `fresh` leg, receipted
  in `.ufo/waves/round-37/evidence/drift-live-r37.txt`).
- HTML contiguity is established under rendered-text matching (markup stripped); a reader requiring
  raw-byte substring equality would fail S222–S225 by construction. The corpus's own excerpt
  convention (`tools/mori-source-drift.py:19-20`) is the standard applied.
- Word counts are whitespace-token counts of the Gate quote strings.
- No LSP server participated (data files, no code symbols); no semantic caller/definition checks were
  applicable. All claims verified by direct reads of the named files at the pinned blob SHAs.

No tool installs or upgrades were made; no pacman transactions; lane repo untouched except this
report file.

**VERDICT: PASS** — all five rows verify: quote contiguous at the anchor line range in the committed
copy, 25/23/23/20/9 words (all ≤25), teaches supported. LOW-1 is the already-recorded M5 packaging
defect (repaired at 52d636d), INFO-1..3 are disclosure/precision notes, none breaks the
rows-vs-copies contract at the scored final state.
