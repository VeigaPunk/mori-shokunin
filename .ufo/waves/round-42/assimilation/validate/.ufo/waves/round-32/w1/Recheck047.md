# Recheck S047 — git-symbolic-ref (C1, round 32, wave 1)

Seat: MoriR32A2.Recheck047. Lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Read-only lane use; no lane writes except this report.

## 1. Fetch record

- id: S047
- population url (also the url cell): https://git-scm.com/docs/git-symbolic-ref
- redirect: none. `curl -w` reported `HTTP=200 URL=https://git-scm.com/docs/git-symbolic-ref SIZE=28808`; url_effective equals the requested URL.
- accessed: 2026-10-23T01:31:22Z (recorded with `date -u +%FT%TZ` immediately before and after the fetch; both printed 2026-10-23T01:31:22Z)
- byte size: 28808
- sha256: 0d2ea49c643107a5fbb4c74f944114c48fe13152158b8255ceb4e71bea20791c
- scratch copy (bytes saved unchanged): /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck047/S047.src
- normalised text used for quotes: /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck047/S047.norm.txt (produced by `seat-check.py text S047.src`, 4232 bytes)
- command: `curl -sSL --fail -m 60 https://git-scm.com/docs/git-symbolic-ref -o .../S047.src` — exit 0, first try; no bot challenge encountered.

## 2. Ready-to-paste row

```markdown
| S047 | https://git-scm.com/docs/git-symbolic-ref | 2026-10-23T01:31:22Z | 0d2ea49c643107a5fbb4c74f944114c48fe13152158b8255ceb4e71bea20791c | "Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently"; "with status 1 if the requested name is not a symbolic ref, or 128 if another error occurs" | current |
```

## 3. Quote → teaches-cell mapping

Teaches cell: "Detached HEAD is a silent nonzero under -q; NOTES distinguishes status 1 from other errors such as 128."

Quote 1: "Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently"
- Bears on: the `-q` OPTIONS clause exactly — the page's `-q --quiet` entry says the command suppresses the error message for a detached HEAD and exits non-zero *silently*. Normalised text, OPTIONS section: `-q --quiet Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently.`
- Whole-word boundaries: starts "Do", ends "silently"; the sentence's negation ("Do not") and its continuation through the semicolon are kept, so no negation or prefix is dropped.

Quote 2: "with status 1 if the requested name is not a symbolic ref, or 128 if another error occurs"
- Bears on: the NOTES clause — the exit-status paragraph separates status 1 (name is not a symbolic ref, i.e. detached HEAD) from 128 (any other error). Normalised text, NOTES section: `git symbolic-ref will exit with status 0 if the contents of the symbolic ref were printed correctly, with status 1 if the requested name is not a symbolic ref, or 128 if another error occurs.`
- Whole-word boundaries: starts "with", ends "occurs"; the "not a symbolic ref" negation is inside the quote.

Why `current`: both teaches clauses are stated verbatim-in-substance on the live page, and the row's used-by premise (`corpus/knowledge/jj-branch-anchor-r17.md:59-60`: "`git symbolic-ref -q HEAD` may return silently nonzero for detached HEAD") still matches the fetched documentation. Shared content tokens with teaches+anchor+scope, per the counter: `detached, exit, head, status` (4 ≥ 2).

## 4. seat-check output

Command:
`timeout 300 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/seat-check.py row S047 S047.src '<quotes cell>'`

```
sha256=0d2ea49c643107a5fbb4c74f944114c48fe13152158b8255ceb4e71bea20791c
quotes=2 words=[24, 18] in_copy=[True, True]
shared_tokens=['detached', 'exit', 'head', 'status'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
seat_check_exit=0
```

## 5. Drift details

None. Verdict is `current`; no `Round32` correction is drafted because no teaches-cell statement changed. The page still documents `-q --quiet` as silent non-zero for detached HEAD and still documents status 1 vs 128 in NOTES. No instruction to other seats needed.

## Tooling

No installs or updates were performed; only `curl`, `python3`, `sha256sum`, `wc`, `date` already present on the host were used.

## Unknowns / limits

- The page is the site's default ("latest" docs) rendering; it carries no explicit version banner in the normalised text, so the population anchor's version-range claim (2.48.1–2.56.0) was not re-tested against a changelog — the row only asserts the two behaviour clauses, both of which the live page states. [INFERENCE] The lack of a version banner means the counter's live fetch and this copy would both track whatever the site serves next, which is what R3 measures.
- Judge checks R4/R5 are outside this seat's scope (seat-check says so explicitly).
