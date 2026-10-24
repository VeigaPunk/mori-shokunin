# ReopenJjAuthor — fresh falsification of source row S045

Seat: `MoriR17.ReopenJjAuthor-4` (scout, leaf; no dispatch). Access date: **2026-10-20**
(live fetch `date: Tue, 20 Oct 2026 19:47:24 GMT`). Targets: `corpus/SOURCES.md:51` (S045),
`corpus/lessons/round-17.md:51` (Gate quote), used-by `corpus/knowledge/jj-branch-anchor-r17.md:1,37-38`,
opening receipt `.ufo/waves/round-17/build/SrcJjMetaedit.md:9-16,20-24,30-34,38-40`.
Read first: `.ufo/waves/round-17/contract.md` including Amendment A1, `PINNED_INPUTS.json`,
`corpus/lessons/round-17.md`, `wave1-context.txt`. No source-registry edit.

## Verdict

**AGREE with S045 on source, quote, tier, opened date, recheck and status/used-by; the quote is
byte-exact and 20 words.** Two non-blocking evidence-chain defects:

1. The `teaches` cell's second clause (the CLI reference does not specify universal
   `jj commit` author behavior) lies outside the declared `scope` ("metaedit author-rewrite
   flag") **and has no anchor in the row**, although the used-by knowledge note depends on that
   clause. The clause is factually true — I re-verified the absence — so this is an
   anchor/scope coverage defect, not a false claim.
2. The URL is the unpinned `/latest/` alias. It is demonstrably not the v0.45.1 artifact: the
   live page already carries a sentence absent from the tag-pinned v0.45.1 snapshot. The
   verbatim quote is stable across v0.45.1, main and the live page, so the taught fact survives;
   the line anchors 2220–2238 are tied to the live rendering and will drift on regeneration.

No falsification of the quoted fact. No reject.

## Live source evidence

- URL: `https://docs.jj-vcs.dev/latest/cli-reference/`
- Fetch (rc0): `HTTP/2 200`, `content-length: 406891`, `date: Tue, 20 Oct 2026 19:47:24 GMT`,
  `content-type: text/html; charset=UTF-8`; `<link rel="canonical">` = the same URL; generator
  `mkdocs-1.6.1, mkdocs-material-9.6.23`. The page contains **no jj version token** (regex
  `\b0\.\d{1,2}\.\d{1,2}\b` over the full HTML returned no matches).
- Legacy URL from the wave-1 request, `https://jj-vcs.github.io/jj/latest/cli-reference/`,
  returns `HTTP/2 301` with `location: http://docs.jj-vcs.dev/latest/cli-reference/` (plain
  `http` in Location). The registered row already uses the https canonical URL, so this is a
  note about the old URL, not a row defect.
- Local cross-check: `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`; `jj metaedit --help`
  (rc0) prints the identical two sentences at its `--update-author` block.
- Located quote (live page, `jj metaedit` → `--update-author`, read-render line **2226**;
  whitespace normalized, tags stripped):

  > This updates the author name and email. The author timestamp is not modified – use --update-author-timestamp to update the author timestamp.

## Anchor reproduction (same tool, fresh page)

`read` on the URL with line selectors reproduced every line number the opening receipt claims:

| Selector | Returned content | Receipt claim |
|---|---|---|
| `:2196-2196` | ``## `jj metaedit` `` heading | section 2196–2241 (`SrcJjMetaedit.md:10`) |
| `:2200-2200` | “Whenever any metadata is updated, the committer name, email, and timestamp are also updated for all rebased commits…” | committer rule line 2200 (`:10`) |
| `:2220-2220` | ``- `--update-author-timestamp` — Update the author timestamp`` | author options start 2220 (`:10`) |
| `:2226-2226` | the quote above | quote at 2226 (`:34`) |
| `:2238-2238` | ``- `--author-timestamp <AUTHOR_TIMESTAMP>` — …`` | author options end 2238 (`:10`) |
| `:708-708` | “When called without path arguments or `--interactive`, `jj commit` is equivalent to `jj describe` followed by `jj new`.” | commit line 708 (`:9`) |

So the anchor is reproducible **through the same access method** at this access date. It is not
a document-internal anchor: the raw tarball artifact numbers differ (see below).

## Immutable-field attack

| Field | Attack | Verdict |
|---|---|---|
| source | Official jj project documentation, same site and convention as S044; 200, canonical self-reference. An immutable alternative exists: `https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/cli/tests/cli-reference%40.md.snap` (200, 154561 bytes; the quote at line 2228; `main` snapshot 200, 161407 bytes, quote at 2292). | **AGREE, residual risk** (unpinned alias; see F2) |
| scope | `metaedit author-rewrite flag`. The quoted sentence and the `--author`/`--author-timestamp` neighbors are inside that scope. The `teaches` commit clause is outside it. | **DISAGREE (coverage only)**: scope ⊂ teaches; no false statement |
| anchor | `metaedit section, author options lines 2220–2238; jj 0.45.1 local help cross-check; opened 2026-10-20`. Range boundaries verified exactly (2220/2238) and the quote at 2226. No anchor for the commit-absence clause, though the opening receipt had one (`SrcJjMetaedit.md:9-11`: commit 704–717, describe section no author text). | **AGREE for metaedit; incomplete for teaches clause 2** |
| teaches | Clause 1 verified literally: option title “Update the author to the configured user”, body “This updates the author name and email”, plus the `JJ_USER`/`JJ_EMAIL` paragraph; timestamp retention is the quoted sentence, with `--update-author-timestamp` as the escape hatch. Clause 2 re-verified: bounded text over `jj commit`, `jj describe`, `jj new` sections contains **zero** `author` occurrences, and the page has **zero** `reset-author` occurrences; the only nearby “revision author” text belongs to `jj converge`, a different command. | **AGREE** (clause 2 true but under-anchored) |
| tier | A. The page is the vendor's own primary CLI documentation, consistent with S044/S046/S047. But it self-labels: “This CLI reference is experimental. It is automatically generated, but does not match the `jj help` output exactly. Run `jj help <COMMAND>` for more authoritative documentation.” | **AGREE, caveat**: A holds because the row records a local `jj metaedit --help` 0.45.1 cross-check that I independently reproduced; the page alone claims lower authority than the binary |
| opened 2026-10-20 | Matches live access. | **AGREE** |
| recheck `on-release` | A symbolic cadence accepted by `scripts/sources-census.sh:29-34` (symbolic cadences reported, never judged overdue). Appropriate for a `latest` alias. | **AGREE** |

## Quote audit (`corpus/lessons/round-17.md:51`)

- Byte comparison of the lesson's inner quoted text against the live sentence: **equal**
  (`equal: True`), U+2013 en dash in both (`0x2013`), straight ASCII hyphens elsewhere.
- Word count: 20 words if the standalone en dash is not counted; 21 whitespace tokens if it is.
  The ≤25-word Gate rule holds under either count. The row's “20 words” claim is defensible;
  state the counting rule if challenged.
- The lesson's `metaedit --update-author:` prefix is a correct locator.
- The sentence occurs once in the `--update-author` option block and is identical in the
  v0.45.1 and main snapshots, and in local `jj metaedit --help` 0.45.1. Stable wording.

## Status and used-by recheck

- `corpus/SOURCES.md:51`: 11 fields, tier `A`, status **mined**, `opened 2026-10-20`,
  `recheck on-release`, used-by `corpus/knowledge/jj-branch-anchor-r17.md`. The used-by path
  exists, so no E11 (dangling used-by) and no W03 (mined without used-by) condition.
- `corpus/knowledge/jj-branch-anchor-r17.md:1` cites “S044/S045 … /latest/cli-reference/
  (colocation, metaedit --update-author)” — correct pairing.
- `:37-38` is the only inline S045 citation: “Its `metaedit --update-author` stamps the lane
  author before commit; `jj commit` alone may retain the ambient author (JjAuditMori F4). S045
  documents update-author, not a universal commit-author guarantee.”
- `corpus/lessons/round-17.md:56` states S045 enters mined; the registry agrees. No stale
  status or used-by link found.

## Does the knowledge note depend on the cited fact?

- **Real but non-load-bearing.** The note uses S045 exactly once (`:38`) as a documentation
  boundary: the CLI reference proves `--update-author`, not how `jj commit` assigns authors.
  That is the same clause whose row anchor is missing (F1).
- No C2 predicate, gate case or census code reads S045. `LANE_AUTHOR_MISMATCH` is keyed on the
  git author/committer fields produced by the helper; its measured basis is JjAuditMori F4 and
  `scripts/hyaku/jj-lane.sh:596-605` (the helper's own comment: “`jj commit <paths>` splits @ and
  keeps @'s existing author, so a bare `--config` would only fix the committer”).
- Therefore the citation is **not decorative** — it prevents citing the CLI reference for
  commit-author semantics — but it is also not evidence for any delivered check. A reader must
  not treat S045 as support for committer stamping; the page's committer rule is at `:2200`,
  outside the row's quoted fact.
- Note on incompleteness: the page says metadata rewrite also updates committer name/email/
  timestamp for all rebased commits. The row's `teaches` omits this, which is acceptable for
  the declared scope but means S045 cannot be cited for C2's committer-keyed finding.

## Findings (for L1; no edits made)

- **F1 — anchor/scope coverage (low).** `SOURCES.md:51` teaches a `jj commit` absence claim with
  no commit-section anchor and a scope cell that excludes it, while the used-by note relies on
  that clause. Verified true by fresh bounded search. Options: add `jj commit` 704–717 plus
  “no author text in `jj describe`/`jj new`” to `anchor` and widen `scope`, or drop clause 2
  from `teaches` (F4 carries the operational claim). No factual correction needed.
- **F2 — unpinned `latest` alias (low, by convention accepted).** The live page is not the
  v0.45.1 artifact: the sentence “will then look for the first” (`jj bisect run`) is present on
  the live page and in the `main` snapshot but **absent** from the v0.45.1 tag snapshot. One
  other `main`-only line (“…workspace config directories…”) did **not** appear live, so exact
  correspondence to `main` is [UNKNOWN]; the page may be a release newer than the host's
  0.45.1. Consequence: the taught fact is stable across versions, but line anchors are
  rendering- and revision-dependent. The row's `jj 0.45.1 local help cross-check` and
  `on-release` recheck are the existing mitigations; an optional hardening is to cite the
  tag-pinned snapshot line (v0.45.1:2228) alongside the page.
- **F3 — tier evidence (info).** Tier A is defensible only with the local-help cross-check; the
  page self-labels experimental/auto-generated and directs readers to `jj help <COMMAND>` for
  authoritative text. The row records that cross-check, and I reproduced it. No change needed.
- **F4 — teaches omission (info).** The page documents that any metadata rewrite also updates
  committer fields (`:2200`). The row's quote supports author-name/email + timestamp retention
  only. This is a boundary, not an error, because the used-by note does not cite S045 for
  committer semantics.

## Residuals / unknowns

1. [UNKNOWN] Which jj revision `https://docs.jj-vcs.dev/latest/` serves today; the page exposes
   no version marker, and live content matches neither the v0.45.1 snapshot nor `main` exactly.
2. [INFERENCE] Line numbers 2220–2238/2226/708 will shift on the next docs regeneration; only
   `on-release` recheck plus the verbatim quote constrain drift. The raw v0.45.1 snapshot has the
   quote at 2228, so the row's numbers are tool-rendering-specific.
3. [UNKNOWN] Whether any archived digest of the page is retained elsewhere in the corpus; I
   found none referenced by S045.
4. [observed, procedural] One transient fetch was written to
   `.ufo/worktrees/round-17/.jjcli.html` and deleted in the next command; all later fetches were
   in memory. This was outside my assigned write path — disclosed as a violation, not defended.

## Commands run (read-only except the disclosed transient file)

| Command | rc | Output |
|---|---|---|
| `curl -sS -D /dev/stderr -o .ufo/worktrees/round-17/.jjcli.html -w … https://docs.jj-vcs.dev/latest/cli-reference/` | 0 | `200 406891`; `date: Tue, 20 Oct 2026 19:47:24 GMT` (file then deleted) |
| `curl -sSI https://jj-vcs.github.io/jj/latest/cli-reference/` | 0 | `HTTP/2 301`, `location: http://docs.jj-vcs.dev/latest/cli-reference/` |
| `jj --version` | 0 | `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` |
| `jj metaedit --help \| grep -n -A4 -B4 update-author` | 0 | identical `--update-author` sentences; `--force-rewrite` documented |
| `read <live URL>:2196-2196` … `:708-708` | ok | headings/quote/options at claimed lines |
| python3 urllib fetch + tag-strip + bounded section search | 0 | `author` hits in `jj commit`/`jj describe`/`jj new` = 0; `reset-author` = 0; quote byte-equal, 20 words / 21 tokens |
| `curl` tag snapshots v0.45.1 / main (in memory) | 0 | 154561 / 161407 bytes; quote at lines 2228 / 2292 |
| `curl` versioned docs paths `/0.45.1/`, `/0.45/`, `/en/latest/` | 0 | `404` each (no version-pinned docs URL) |

## Scope limits

Attacked only S045's source/immutability, scope, anchor, teaches, tier, quote and its
status/used-by dependency, against the live page, tag/main snapshots, and local jj 0.45.1 help.
No source-registry edit, no corpus edit, no other report touched, no VCS mutation, no package
transaction, no background job, no journal query, no credential or transcript read, no tool
installed or updated. Evidence only; L1 is the sole integrator and judge.
