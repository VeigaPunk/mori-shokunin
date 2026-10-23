# RevSupS206S207 — re-open S206 (RFC 6585) and S207 (jj git-compatibility)

Reviewer: `mori-r36-w2-RevSupS206S207-23`. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only); landed tip `bf0df77fee4b6ef54a90aea09335c7617f125151`, round base `6bd57097`.

Attack: S206/S207 SOURCES rows + their pinned copies. Verify (a) both URLs fetch and each copy sha256-equals the fetched body; (b) the S206 anchor quote (§4, 429 definition) and the S207 anchor quote (detached-HEAD feature row) are contiguous and ≤25 words in the fetched bodies; (c) the `supersedes S041/S044` form follows CORPUS rule 2 and the superseded rows are untouched. FAIL on any mismatch.

## 1. Row extraction (tip vs round base)

Command (scratch only; lane untouched):

```
$ git show bf0df77fee4b6ef54a90aea09335c7617f125151:corpus/SOURCES.md > /fast/scratch/hyaku/mori-r36/RevSupS206S207/tip-SOURCES.md
$ git show 6bd57097:corpus/SOURCES.md > /fast/scratch/hyaku/mori-r36/RevSupS206S207/base-SOURCES.md
```

Tip rows (grep on the extracted file):

```
| S206 | RFC 6585 Additional HTTP Status Codes — https://www.rfc-editor.org/rfc/rfc6585 | spec | A | HTTP 429 Too Many Requests status meaning | §4, plain-text lines 132–135; Standards Track, April 2012; opened 2026-10-23 | supersedes S041 — RFC 6585 defines 429 as too many requests in a given amount of time (rate limiting); mori lane rule: do not infer vendor business error or permanent seat death from status 429 alone. | mined | 2026-10-23 | 365d | corpus/knowledge/seat-terminal-status-r17.md |
| S207 | jj Git compatibility — https://docs.jj-vcs.dev/latest/git-compatibility/ | docs | A | colocated jj/Git HEAD state | Detached HEAD feature row and Colocated Jujutsu/Git workspaces; re-opened 2026-10-23 | supersedes S044 — jj commands will usually put the Git repo in a detached HEAD state. | mined | 2026-10-23 | on-release | corpus/knowledge/jj-branch-anchor-r17.md |
```

Base (6bd57097) has **no** S206/S207 rows; both are appended between base and tip. Python row-set diff over both files: rows present in both base and tip with changed bytes = `[]`; new rows at tip = S205–S220 (16 rows, including S206/S207). So the only delta is append-only additions; no pre-existing row changed.

## 2. Fetch + copy sha256 equality

Fetched the **exact row URLs** (not guessed variants):

```
$ curl -sS -L -o /fast/scratch/hyaku/mori-r36/RevSupS206S207/rfc6585-rowurl.html https://www.rfc-editor.org/rfc/rfc6585
$ curl -sS -L -o /fast/scratch/hyaku/mori-r36/RevSupS206S207/jj-git-compat.html https://docs.jj-vcs.dev/latest/git-compatibility/
```

| id | fetched body | bytes | sha256 (fetched) | lane copy | sha256 (copy) | equal |
|---|---|---|---|---|---|---|
| S206 | `rfc6585-rowurl.html` | 171482 | `cc0123160b49d4abce57f51a1d56c02745afc61d29dd20c0e51fc42bb5f5d968` | `corpus/evidence/sources-r36/S206.src` | `cc0123160b49d4abce57f51a1d56c02745afc61d29dd20c0e51fc42bb5f5d968` | YES |
| S207 | `jj-git-compat.html` | 61334 | `db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254` | `corpus/evidence/sources-r36/S207.src` | `db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254` | YES |

Both copies are byte-identical to the live fetched bodies. Glob over `corpus/evidence/**` finds exactly one copy per id (`sources-r36/S206.src`, `sources-r36/S207.src`) — no stale decoy copies for these ids.

## 3. Anchor quotes: contiguous and ≤25 words

### 3.1 S206 — §4 429 definition (RFC 6585 plain text)

Authoritative physical line numbers (grep -n; note: Python `splitlines()` over-counts because the RFC contains form-feed page breaks, so grep is the authority):

```
$ grep -n '429 Too Many Requests' rfc6585.txt
68:   4. 429 Too Many Requests ...........................................3
132:4.  429 Too Many Requests
$ grep -n 'The 429 status code' rfc6585.txt
134:   The 429 status code indicates that the user has sent too many
$ grep -n 'rate limiting' rfc6585.txt
135:   requests in a given amount of time ("rate limiting").
```

Anchor claim `§4, plain-text lines 132–135` is exact: heading at 132, definition sentence at 134–135.

Source sentence (normalized whitespace, fetched body): `The 429 status code indicates that the user has sent too many requests in a given amount of time ("rate limiting").` — **contiguous** in the body, **21 words ≤ 25**. PASS.

Teaches core quote: `too many requests in a given amount of time (rate limiting)` — contiguous in the body after removing the source's own ASCII double-quote characters around `rate limiting` (source spells `("rate limiting")`; teaches spells `(rate limiting)`); 11 words. The teaches preamble `RFC 6585 defines 429 as` is the row author's framing, not verbatim source — the grounded quote itself is verbatim-contiguous and within the limit. Observation, not a defect (the row's quote material maps 1:1 to §4 lines 134–135).

### 3.2 S207 — detached-HEAD feature row (jj docs)

Visible text extracted from fetched HTML (tags/scripts stripped, entities unescaped, whitespace normalized). The teaches quote `jj commands will usually put the Git repo in a detached HEAD state` appears **verbatim and contiguous** in the visible text with the source's own quote characters: `…jj commands will usually put the Git repo in a "detached HEAD" state, since in jj there is not concept of a "currently tracked branch".` — **13 words ≤ 25**. PASS.

Anchor elements both present in the same fetched body:
- Detached-HEAD feature row (comparison table): `Detached HEAD: Yes. Jujutsu supports anonymous branches, so this is a natural state.`
- Colocated workspaces heading: `Colocated Jujutsu/Git workspaces` (TOC + section).

## 4. `supersedes S041/S044` form and superseded rows

CORPUS rule 2 (fleet `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`): *"Append-only. Only `status`, `recheck` and `used-by` change in place… A correction is a new row whose `teaches` opens `supersedes S0NN —`."*

- S206 teaches cell opens `supersedes S041 —` ✓ (form `supersedes S### —`, em dash).
- S207 teaches cell opens `supersedes S044 —` ✓.

Superseded rows untouched — byte-identical between round base `6bd57097` and tip `bf0df77` (extracted rows compared):

```
S041 identical base==tip: True
S044 identical base==tip: True
```

Both rows remain present at tip (not deleted). And `tools/mori-sources-appendonly.py bf0df77… --round-base 6bd57097` reports `changed S041 superseded_by=S206`, `changed S044 superseded_by=S207` with `round_changed=[]`, exit 0 (L1/w1 receipts; reproduced in w1 reports). The S041/S044 immutable-cell debt predates the round; the supersession is recorded by the new rows, not by editing them.

## 5. Findings

No defects found. All five attacked properties hold:

1. S206 copy sha256 == fetched body of the exact row URL — PASS.
2. S207 copy sha256 == fetched body of the exact row URL — PASS.
3. S206 §4 anchor quote contiguous, 21 words ≤25; teaches core quote contiguous (quote-char normalized) — PASS.
4. S207 detached-HEAD anchor quote verbatim-contiguous, 13 words ≤25; both anchor elements (feature row, colocated heading) present — PASS.
5. `supersedes S041/S044` form matches CORPUS rule 2; S041/S044 rows untouched byte-for-byte across the round — PASS.

Observations (non-defects, recorded for completeness):
- O1: S206 teaches preamble `RFC 6585 defines 429 as` is paraphrase framing; the grounded quote itself is verbatim (see §3.1).
- O2: S207 teaches quote omits the source's double-quote characters around `detached HEAD`; the quote remains contiguous and literal modulo those punctuation characters.
- O3: the RFC plain-text body contains form-feed page breaks; line anchors in the row refer to physical lines (grep `-n`), which match.

## Verification gaps / residual risk

- Single-point fetch: both bodies fetched once each at review time; a network-level cache/ETag artifact cannot be fully excluded, but copy equality with the committed bytes plus the row-anchor line match is strong evidence.
- The jj page is a MkDocs build with a rendered fixed version; the anchor row exists in the current rendered body. No archive/version-pinned URL check was available for the past state.
- S041/S044 "untouched" verified across base→tip; their older in-round-35 history was not re-audited here (out of scope).

## VERDICT: PASS

No defect found in S206/S207 SOURCES rows, their copies, anchor quotes, supersedes form, or superseded-row state.

Commands observed (all read-only): `git show` at both revs; `curl -sS -L` fetches; `sha256sum`; `grep -n`; Python row-set diff and quote-contiguity normalization. No lane file edited; scratch only under `/fast/scratch/hyaku/mori-r36/RevSupS206S207/`.
