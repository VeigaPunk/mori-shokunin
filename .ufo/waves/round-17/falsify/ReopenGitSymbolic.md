# ReopenGitSymbolic — fresh falsification of source row S047 and the lessons quote

Seat: `MoriR17.ReopenGitSymbolic-4` (wave 2, leaf; no subagent dispatch). Lane root:
`/home/vgpnk/Projects/shokunin/mori-shokunin`, branch `master`, measured tip
`273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` (as pinned in `PINNED_INPUTS.json`). Access date
**2026-10-20**, reopen at **19:48–19:50Z** (`date -u` = `2026-10-20T19:48:26Z`), cwd lane root.
This seat attacks evidence only; it does not judge admission, edit `corpus/SOURCES.md` or any
other file, or run a tool selftest/gate.

Installs/updates: none. Writes: this report only. VCS mutation: none (only read-only
`git show`/`cat-file`/`--version`). No `/tmp`, no background jobs, no journal query, no
transcript read.

## 1. Live reopen of the cited page

| Surface | Command | Observed |
|---|---|---|
| Canonical page | `curl -fsSI --max-time 60 https://git-scm.com/docs/git-symbolic-ref` | `HTTP/2 200`; `date: Tue, 20 Oct 2026 19:49:52 GMT`; `content-type: text/html; charset=utf-8`; `last-modified: Tue, 20 Oct 2026 04:47:21 GMT`; `etag: W/"6ad6f259-7084"`; rc0 |
| Body identity | `curl -fsSL … \| tee >(wc -c >&2) \| sha256sum` | `28804` bytes; `sha256 d706904473082a0ef07ed8eedd2c4d94be25dac852e58ff3b017048828c38872`; rc0 |
| Reader extraction | `read https://git-scm.com/docs/git-symbolic-ref` | SYNOPSIS, DESCRIPTION, OPTIONS, NOTES rendered; version list starts `2.48.1 → 2.56.0 no changes`; rc0 |
| Q1 in raw HTML | `curl -fsSL … \| tr '\n' ' ' \| grep -o 'Do not issue an error message…'` | exact bullet present (`&lt;name&gt;` entity); rc0 |
| NOTES exit status | `curl -fsSL … \| tr '\n' ' ' \| grep -o 'git symbolic-ref</em> will exit[^<]*'` | exact sentence present; rc0 |
| Numeric-code census | `curl -fsSL … \| grep -o 'status 1\|128\|detached' \| sort \| uniq -c` | `1 128`, `1 detached`, `1 status 1` — the `-q` bullet is the only `detached` mention and NOTES the only `128`/`status 1` statement |
| Host binary | `git --version` | `git version 2.56.0`, the same version as the page's top range (receipt had only inferred a match) |

Located quotes (verbatim, HTML entities decoded; both on the live 2026-10-20 page):

- OPTIONS > `-q`, `--quiet` (24 words): **“Do not issue an error message if the <name> is not a
  symbolic ref but a detached HEAD; instead exit with non-zero status silently.”**
- NOTES (fragment): **“with status 1 if the requested name is not a symbolic ref, or 128 if
  another error occurs.”** Full sentence: “*git symbolic-ref* will exit with status 0 if the
  contents of the symbolic ref were printed correctly, with status 1 if the requested name is
  not a symbolic ref, or 128 if another error occurs.”

The source seat's two-fetch method reproduces: the `-q` bullet and the NOTES sentence are both
in the delivered HTML, not only in a JS payload. The page is the manual for git 2.56.0, which
is the installed binary today.

## 2. Row fields under test (`corpus/SOURCES.md:53`)

Committed row at the measured tip, byte-identical to the working tree
(`git show 273aa74:corpus/SOURCES.md | grep '^| S047 '` vs working-tree line: `sources-row-identical`):

> `| S047 | git symbolic-ref documentation — https://git-scm.com/docs/git-symbolic-ref | docs | A | quiet detached-HEAD detection | OPTIONS -q and NOTES exit status; no changes listed 2.48.1 through 2.56.0; opened 2026-10-20 | Detached HEAD is a silent nonzero under -q; NOTES distinguishes status 1 from other errors such as 128. | mined | 2026-10-20 | on-release | corpus/knowledge/jj-branch-anchor-r17.md |`

| Field | Row text (abridged) | Observed on the live page | Verdict |
|---|---|---|---|
| source | `git symbolic-ref documentation — https://git-scm.com/docs/git-symbolic-ref` | Canonical URL 200; official Git manual page for the command | **Match.** |
| scope | `quiet detached-HEAD detection` | `-q`/`--quiet` bullet: silence on a non-symbolic-ref/detached HEAD; the exit status, not the flag, carries the condition | **Match in substance; wording overstates agency** (F2). |
| anchor | `OPTIONS -q and NOTES exit status; no changes listed 2.48.1 through 2.56.0; opened 2026-10-20` | Page anchors are `OPTIONS` (`-q`/`--quiet` sibling entries) and `NOTES`; version list entry 1 is exactly `2.48.1 → 2.56.0 no changes`; access date today | **Match exactly.** Section names are the right anchor; the extraction has no reliable line numbers, and the row does not invent any. |
| teaches | `Detached HEAD is a silent nonzero under -q; NOTES distinguishes status 1 from other errors such as 128.` | `-q` bullet says silently exit non-zero; NOTES says status 1 for “not a symbolic ref” and 128 for “another error” | **Match.** Both clauses are direct paraphrase, with the 1/128 split verbatim in NOTES. |
| tier | `A` | Upstream project documentation for the git binary the census calls | **Match.** Same `docs`/`A` class as S044/S046 (`corpus/SOURCES.md:50,52`). |
| status/opened/recheck/used-by | `mined \| 2026-10-20 \| on-release \| corpus/knowledge/jj-branch-anchor-r17.md` | Row exists; target note exists and is committed; `on-release` matches the adjacent living-doc rows | **Formally consistent; dependency overstated for the quoted fact** (§4). |

No duplicate URL: `grep -c 'git-scm.com/docs/git-symbolic-ref' corpus/SOURCES.md` = `1`.

## 3. The ≤25-word quote in `corpus/lessons/round-17.md:53`

```
| S047 | https://git-scm.com/docs/git-symbolic-ref | OPTIONS -q: “Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently.” |
```

- Located quote: the `-q`/`--quiet` OPTIONS bullet, verbatim.
- Word count: `24` (`printf '%s\n' "$q" | wc -w` → `24`; ≤25 satisfied).
- Anchor `OPTIONS -q` — correct section/sub-entry; the page has no line numbers, and the row
  claims none.
- URL, access date `2026-10-20`, and the quote's presence — verified by this reopen.
- Entity handling: the page HTML carries `&lt;name&gt;`; the receipt disclosed decoding, and the
  decoded `<name>` is the faithful text.

**Agree.** The quote is verbatim, correctly located, and under the cap. One presentational
nit: the raw `<name>` inside the Markdown cell is parsed as an HTML tag, so a rendered view can
drop the placeholder; committed bytes are correct (F4, cosmetic).

## 4. used-by / status link and the dependency test

Links checked:

- Registry row: `corpus/SOURCES.md:53`, status `mined`, used-by
  `corpus/knowledge/jj-branch-anchor-r17.md`.
- Target exists and is committed: `git cat-file -e 273aa74:corpus/knowledge/jj-branch-anchor-r17.md`
  → present; committed and working-tree sha256 both
  `e616bb28d5e0c03275642dbe89aae338babf4e0183b5dcdc49ce67bb1508641f`.
- Lessons narrative: `corpus/lessons/round-17.md:56` “S047 enter mined”, and `:60` “These are
  sourced claims, not decorative citations” — but `:59-60` names only S043 and S046 as the
  sources that “caused” fixes, so the lessons sentence itself does **not** claim S047 is
  load-bearing. The `mined` + used-by cells are the only claim of dependence.
- The source seat's own linkage already qualified it: `build/CriticFrontier.md:115-121` — “S047
  (`symbolic-ref -q`) is weaker … It means S047's detached-HEAD case exercises a fallback, not
  the authority. Cite S047 as context, not as the sourced claim.” That caveat is not carried
  into the lessons Gate section or the knowledge note's boundary.

Dependency test — delete S047 and ask what loses support:

1. `corpus/knowledge/jj-branch-anchor-r17.md` cites S047 only in the combined `source:` header
   (line 1: “S046/S047 — https://git-scm.com/docs/git-merge-base and /docs/git-symbolic-ref”).
   No body sentence names S047, and the note never mentions `-q` or symbolic-ref exit status:
   `grep -c -- '-q' corpus/knowledge/jj-branch-anchor-r17.md` → `0`.
2. The load-bearing body claims are carried elsewhere: the detached-HEAD premise by S044 and
   JjAuditMori F3, the resolver order by the contract/gate, and the only inline source marker in
   the decision table is `(S046)` at line 25 for “another nonzero status | probe error”.
3. Delivered code does not consume the quoted fact. `tools/mori-census.sh:2110-2138`
   (`lane_branch_probe`) reads only `CAP_OUT`'s first line and matches `refs/heads/*` /
   `refs/remotes/origin/*`; it never reads `CAP_RC` for either `symbolic-ref` call (rc is
   consulted only for the two `show-ref` calls at `:2131-2135`). `cap()` merges stderr
   (`:554-558`), so `-q` keeps the detached case's `CAP_OUT` empty instead of carrying a fatal
   line, but the shape checks would reject that fatal line identically — resolution outcome is
   unchanged with or without `-q`.
4. The gate's own resolver discards the status too: `tools/mori-round17-jj-regressions.py:917,919`
   (`b=$(git -C "$dir" symbolic-ref -q HEAD 2>/dev/null || true)`, same for `origin/HEAD`). The
   detached cases (`:536-544`, `:696`) assert the resulting verdict, not rc1 versus rc128.
5. Therefore neither half of the `teaches` cell — the `-q` silence or the 1-versus-128 split — is
   exercised by the knowledge note, the census, or the gate. Removing S047 from the note header
   would leave every body claim supported by S044/S046 plus measured evidence.

This is exactly CriticFrontier's earlier finding, now confirmed against the delivered code: the
page is relevant to the resolver's first step, but the **quoted sentence is context, not the
sourced claim**, and the delivered implementation does not depend on it.

## 5. Findings

- **F1 (dependency; material to registration, not to the page).** S047's quoted fact is not
  load-bearing in `corpus/knowledge/jj-branch-anchor-r17.md` or in the delivered C2 code. The
  used-by edge is a file-level bundle header, and `mined` implies a claim-level dependence that
  the quoted sentence does not have. Confidence high. If L1 wants the row to remain `mined` as a
  sourced claim, the honest strengthening is an actual consumer (for example a census/gate
  assertion that a detached `symbolic-ref -q HEAD` is rc1 and that an rc128 probe error is not
  read as detachment); otherwise the row is context and the note should say so. No registry edit
  made by this seat.
- **F2 (scope wording; low).** “quiet detached-HEAD detection” attributes detection to `-q`; the
  manual attributes the condition to the exit status and uses `-q` only to suppress the message.
  The `teaches` cell is precise, so this is a label imprecision, not a page contradiction.
- **F3 (registration/lineage; low–medium).** The critic's “cite as context” qualification
  (`build/CriticFrontier.md:115-121`) is absent from `corpus/lessons/round-17.md` and from
  `corpus/knowledge/jj-branch-anchor-r17.md`'s boundary, while the registry row carries `mined`.
  The lessons' “not decorative” sentence is explicitly scoped to S043/S046, so the gap is in the
  used-by/status linkage, not in that sentence.
- **F4 (cosmetic).** `<name>` in the `corpus/lessons/round-17.md:53` cell is raw
  HTML-significant Markdown; the committed bytes are verbatim, but a rendered view may drop the
  placeholder.

Positive checks (no defect): URL live and first-party; quote verbatim and 24 words; anchor
correct without invented line numbers; NOTES text exactly supports the 1/128 clause; version
range exact; host git 2.56.0 matches the page's top range; no duplicate URL; committed row and
note unchanged from the measured tip.

## 6. Verdict

**Agree with the source row's factual cells and the lessons quote** on source, anchor, teaches,
and tier: the page is live, the quote and NOTES sentence are verbatim, the ≤25-word cap holds
(24), and the page is the installed git 2.56.0 manual. **Disagree with the dependence implied by
`mined` + used-by for the quoted fact**: the knowledge entry and the delivered resolver never
use the `-q` silence or the status-1-versus-128 distinction; the entry would stand unchanged
without S047. Scope wording is slightly loose, not false. No falsifying defect was found in the
page, the quote, or the row's factual values; the defect is registration/lineage, and the
decision is L1's.

Exact attacked scope: the S047 row (`corpus/SOURCES.md:53`), its field values, the
`corpus/lessons/round-17.md:53` cell and the `:56/:59-60` status narrative, the
S047→`corpus/knowledge/jj-branch-anchor-r17.md` used-by edge, and the symbolic-ref consumption
in `tools/mori-census.sh:2110-2138` and `tools/mori-round17-jj-regressions.py:917,919`.
Not attacked here: other source rows, classifier/census correctness beyond the symbolic-ref
resolution path, fixture adequacy, gate outcomes, and any admission/score judgment.

## 7. Commands (read-only; no scratch writes)

| Command (cwd = lane root) | rc | Output used |
|---|---|---|
| `read https://git-scm.com/docs/git-symbolic-ref` | 0 | SYNOPSIS/OPTIONS/NOTES; version list `2.48.1 → 2.56.0 no changes` |
| `curl -fsSI --max-time 60 https://git-scm.com/docs/git-symbolic-ref` | 0 | `HTTP/2 200`, date 19:49:52 GMT, `last-modified` 04:47:21 GMT, etag `W/"6ad6f259-7084"` |
| `curl -fsSL … \| tee >(wc -c) \| sha256sum` | 0 | `28804` bytes, `d7069044…c38872` |
| `curl -fsSL … \| tr '\n' ' ' \| grep -o 'Do not issue an error message…'` | 0 | exact `-q` bullet (`&lt;name&gt;`) |
| `curl -fsSL … \| tr '\n' ' ' \| grep -o 'git symbolic-ref</em> will exit[^<]*'` | 0 | exact NOTES sentence, status 0/1/128 |
| `curl -fsSL … \| grep -o 'status 1\|128\|detached' \| sort \| uniq -c` | 0 | `1 128`, `1 detached`, `1 status 1` |
| `printf '%s\n' "$q" \| wc -w` (Q1) | 0 | `24` |
| `date -u +%Y-%m-%dT%H:%M:%SZ` | 0 | `2026-10-20T19:48:26Z` |
| `git --version` | 0 | `git version 2.56.0` |
| `git --no-optional-locks show 273aa74:corpus/SOURCES.md \| grep '^| S047 '` | 0 | row at line 53 |
| `git --no-optional-locks show 273aa74:corpus/lessons/round-17.md \| grep '^| S047 '` | 0 | cell at line 53; status narrative 56/59-60 |
| `git --no-optional-locks show 273aa74:corpus/knowledge/jj-branch-anchor-r17.md \| sha256sum` vs working tree | 0 | both `e616bb28…08641f`; `git cat-file -e` → present |
| `grep -c -- '-q' corpus/knowledge/jj-branch-anchor-r17.md` | 0 | `0` |
| `grep -n 'symbolic-ref' tools/mori-census.sh` | 0 | `:2113`, `:2122`; resolver `:2110-2138`; `cap()` `:554-558` |
| `grep -n 'symbolic-ref' tools/mori-round17-jj-regressions.py` | 0 | `:917`, `:919`, both `\|\| true`; detached cases `:536-544`, `:696` |
| `grep -n 'S047' corpus/SOURCES.md corpus/lessons/round-17.md` | 0 | `SOURCES.md:53`, `lessons:53,56` |
| `grep -c 'git-scm.com/docs/git-symbolic-ref' corpus/SOURCES.md` | 0 | `1` |

## 8. Remaining unknowns

- The source receipt recorded no page digest at its 18:54Z fetch, so a change-and-revert between
  18:54Z and 19:49Z is unobservable; the quote and NOTES sentence match at both ends, and the
  page's `last-modified` (04:47:21Z) is a build time, not a content witness. [UNKNOWN for the
  interval; observed today only]
- Whether `mined` is defined by the lane as “a knowledge note depends on it” is not stated in a
  legend I found; I treat it as the convention implied by S042/S048 (`queued`, used-by `—`).
  [INFERENCE on the status semantics]
- Whether the installed binary's actual `symbolic-ref -q` exit codes match the page is not
  probed here (no live sandbox, per the seat bounds); the manual is the only evidence, and the
  page is the 2.56.0 manual that matches `git --version`. [INFERENCE from version agreement]
- Whether L1 intends S047 as resolver context rather than a sourced claim is not recorded in the
  note; the critic's caveat is the only explicit statement, and it was not carried forward.
  [UNKNOWN as intent; observed as text]
