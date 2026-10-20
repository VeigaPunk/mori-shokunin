# SrcJjMetaedit — jj author handling for `jj metaedit --update-author` and `jj commit`

Seat: MoriR17.SrcJjMetaedit-5 (scout, read-only). Date: 2026-10-20. No VCS writes, no installs.

## Sources read

- Official jj CLI reference, opened 2026-10-20: `https://jj-vcs.github.io/jj/latest/cli-reference/` (requested URL). The fetch resolved to the canonical `https://docs.jj-vcs.dev/latest/cli-reference/` (page meta `canonical`). Page self-labels "This CLI reference is experimental. It is automatically generated, but does not match the `jj help` output exactly." Full extract captured as `artifact://78390` (4053 lines).
- Relevant spans of that extract:
  - `jj commit` section: lines 704-717; author-relevant sentence at line 708.
  - `jj metaedit` section: lines 2196-2241; author flags at lines 2220-2238; committer rule at line 2200.
  - `jj describe` section: no author text found (grep for `author` over the full extract returned no hits in that section).
- Local cross-check (read-only, exit 0):
  - `jj version` → `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`
  - `jj commit --help` (rc=0): no author text; states `jj commit` is "equivalent to `jj describe` followed by `jj new`" when called without paths or `--interactive`.
  - `jj metaedit --help` (rc=0): same author text as the web page, plus `--force-rewrite` (documented in the local help and at extract line 2242; the local help and page agree).
  - `jj help -k config` (rc=0): `user.name`/`user.email` config and "Author format" section (lines 832-857 of that output); no statement on how `jj commit` assigns author.

## Findings

1. `jj metaedit --update-author` sets the author name and email from the configured user (`JJ_USER`/`JJ_EMAIL` or `user.name`/`user.email`). The author timestamp is kept unless `--update-author-timestamp` is passed (extract 2224-2230; local help identical).
2. `jj metaedit --author "Name <email>"` sets name and email and retains the author timestamp for non-discardable commits (extract 2232-2236).
3. Whenever metadata is updated, the committer name, email and timestamp are also updated for all rebased commits (extract line 2200). `--force-rewrite` updates committer fields even with no other change (extract 2242-2250).
4. `jj commit` author handling: NOT DOCUMENTED. The reference only says `jj commit` (no paths, no `--interactive`) is `jj describe` followed by `jj new` (line 708), and the `jj describe` section has no author text. Whether `jj commit` sets or changes the author is therefore not stated by the CLI reference. [INFERENCE] Any author change by `jj commit` would have to come through the describe/new path; this is not observed here and was not tested (no mutating commands run).
5. Relevance to C2 `LANE_AUTHOR_MISMATCH` (contract.md lines 17-18, 88-89): the reference confirms the documented repair path for an author that differs from the configured lane identity is `jj metaedit --update-author` (or `--author`), and that this rewrite changes committer fields on the rewritten commit. [INFERENCE] This suggests the census should grade author/committer difference as a repairable drift, not a content error; this seat did not verify census behavior.

## SOURCES row draft (not written to corpus/SOURCES.md — drafting only)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S045 | jj CLI reference, `jj metaedit` and `jj commit` — https://docs.jj-vcs.dev/latest/cli-reference/ (requested as https://jj-vcs.github.io/jj/latest/cli-reference/; canonical per page meta; experimental, auto-generated; jj 0.45.1 local help cross-checked) | docs | A | jj 0.45.1 `metaedit` author/committer rewrite flags and the (undocumented) author behavior of `jj commit` | metaedit section lines 2196-2241 (author text 2220-2238, committer rule 2200); commit section lines 704-717 (line 708); describe section has no author text; local `jj metaedit --help` and `jj commit --help` rc=0 on 2026-10-20 | `jj metaedit --update-author` sets author name/email from the configured user and keeps the author timestamp unless `--update-author-timestamp`; rewritten commits get new committer fields; the reference documents no author handling for `jj commit`, which it defines as `jj describe` followed by `jj new`. | queued | 2026-10-20 | on-release | — |

Gate line: `Gate: S045 — "This updates the author name and email. The author timestamp is not modified – use --update-author-timestamp to update the author timestamp." (jj CLI reference, jj metaedit --update-author; opened 2026-10-20; https://docs.jj-vcs.dev/latest/cli-reference/)`

Quote check: 20 words; matches the live `jj metaedit --help` output (rc=0) and the web extract at line 2226.

## Limits

- The CLI reference is self-declared experimental and auto-generated; it is not authoritative (its own banner says to use `jj help <COMMAND>`). Local help agrees on every author sentence quoted here.
- No author behavior was executed: no `jj commit`, `jj metaedit` or `jj describe` run, so the `jj commit` author question remains open and marked [INFERENCE] above.
- Scope excludes git-side committer identity in colocated mode and the census code; those were not read.

## Install / update record

None. Tools used: `jj` 0.45.1 (pre-existing), `_read`, `_grep`, `_bash` (`jj commit --help`, `jj metaedit --help`, `jj version`, `jj help -k config`).

## Checks for main agent

- Decide whether S045 tier A is appropriate for an experimental auto-generated page (tier left as proposed).
- If the author behavior of `jj commit` matters for C2, run a sandboxed jj probe (in the executor's own clone only) rather than relying on this reference.
