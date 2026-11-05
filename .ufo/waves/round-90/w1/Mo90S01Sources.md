# Mo90S01Sources — round 90 source scribe report

Scope: candidate SOURCES rows and the knowledge entry for the branch-reachability rule and the call-site pin. Nothing appended to `corpus/SOURCES.md`; the L1 integrates.

## Deliverables

- `.ufo/waves/round-90/w1/Mo90S01Sources-rows.md` — five candidate rows, S612–S616, status `mined`, 11 cells each (checked: every row has 13 `|` separators, no `|` inside a cell).
- `.ufo/waves/round-90/w1/Mo90S01Sources-entry.md` — body for `corpus/knowledge/branch-reachability-r90.md`, with `## Gate` (URL, access date, located quote per row) and a `## Limits` paragraph naming the provenance class.
- Pinned copies: `.ufo/waves/round-90/w1/Mo90S01Sources/sources/` — `posix-shell-v3-chap02.html`, `python-ast-3.15.2.html`, `python-tokenize-3.15.2.html`.

## Registry check

- `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort | tail -3` → `S609`, `S610`, `S611`.
- `git show d1c8488986512a6a0475af88cc52779ce4703e00:corpus/SOURCES.md` gives the same max id, S611. Next free id: S612.

## Fetches (2026-11-05, `curl -sSL`, User-Agent set)

| URL | HTTP | redirects | bytes | sha256 (first 16) | second fetch |
|---|---|---|---|---|---|
| pubs.opengroup.org …/V3_chap02.html | 200 | 0 | 357953 | 0889867a53fe1250 | byte-identical (`cmp`) |
| docs.python.org/3/library/ast.html | 200 | 0 | 362493 | 7891c58897fe9f78 | byte-identical |
| docs.python.org/3/library/tokenize.html | 200 | 0 | 53982 | 6842ed0f53882c5a | byte-identical |
| pubs.opengroup.org …/utilities/exit.html | 200 | 0 | 6580 | 7f2e261396e8e84c | **dropped**: a script-redirect page with no specification text |

The POSIX page's hash equals S611's recorded hash, so its bytes are unchanged since round 89.

## Quote verification (`python3` over the tag-stripped text; quote count per page)

```
posix-lists-b occ=1 words=11  start_line=1385
posix-if      occ=1 words=18  start_line=1562
posix-exit    occ=1 words=14  start_line=2750
posix-errexit occ=1 words=20  start_line=3223   (not rowed; available for the set -e exemption)
py-walk       occ=1 words=18  start_line=1907
py-segment    occ=1 words=13  start_line=1881
py-tok        occ=1 words=11  start_line=38
```

Each quote is at most 25 words and occurs exactly once in its page's text.

## Findings

- The POSIX §2.9.3 sentence gives equal precedence and left associativity for the two AND-OR operators. This is the ground for rule items 1–2 (a literal `false` on the left of AND, a literal `true` on the left of OR).
- The POSIX §2.9.4.4 sentence fixes which body of an `if` runs. The `if` status is that body's status, or zero if none ran. This grounds `C02:H04-if-false`.
- The POSIX §2.15 `exit` description ends the current execution environment. In a subshell, the parent continues. This grounds `N-A08`/`H03` exit-before. `utilities/exit.html` gave no text, so the `exit` row cites the same page.
- Python `ast.walk` has no defined order, and `get_source_segment` returns `None` when location fields are missing. `tokenize` returns comments as tokens. These ground the structural pin in general terms only.
- **Not grounded:** the heredoc half of `C02:H09-heredoc-or-subshell-false`. No heredoc section was opened. The entry says so. The subshell half is covered by the `exit` sentence.

## Deviations (disclosed)

1. **Access date.** The seat brief asks for 2026-11-04. The host clock reads 2026-11-05 UTC at fetch time, and the Python tokenize page says "Last updated on Nov 05, 2026 (00:37 UTC)". I recorded 2026-11-05 rather than a date I did not observe.
2. **Python version.** The live `docs.python.org/3/` pages are 3.15.2. S607–S610 cite 3.14. The new rows name 3.15.2 and use `90d` recheck.
3. **Entering revision.** The brief names `d1c8488986512a6a0475af88cc52779ce4703e00`, which I verified with `git rev-parse`. `contract.md` names `037c02ca43a5ff36e23e449d0d6bcf50a1f2cbec`, which also exists. The working tree is dirty (untracked round-90 files). I read the registry from the working tree; its max id matches the d1c8488 blob.
4. **Path.** `CORPUS.md` is not at the lane root, so the registry contract is taken from `corpus/QUALITY.md` (row rules) and `corpus/SOURCES.md`'s own header.

## Not done / limits

- No subagent dispatch (leaf seat). No tools installed.
- Only three pages with content were opened, against the brief's 2–4 sources. Five rows come from them.
- The rule's implementation and the B4 `met_line` anchor were not checked against the counters; that mapping is marked `[INFERENCE]` in the entry.
- Scratch `/fast/scratch/hyaku/mori-r90/Mo90S01Sources` is removed before yield, after the copies were written to the wave directory.

## Handoff

For the L1: append the five rows to `corpus/SOURCES.md` after S611 (ids S612–S616 unchanged); then land the entry as `corpus/knowledge/branch-reachability-r90.md`. Check the rows against the registry's cell rules (the status, `recheck` and `used-by` cells are the only ones that may change later). Checks for the main agent to run: `grep -c '|' corpus/SOURCES.md` before and after, and `python3 -I .ufo/waves/round-90/count-c1.py d1c8488986512a6a0475af88cc52779ce4703e00` for the C1 reading (not run by this seat).
