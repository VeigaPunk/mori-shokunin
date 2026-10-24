VERDICT: PARTIAL. Six of seven fields HOLD. The "teaches grounded" field is BROKEN: its first clause is supported by S069, but its prescriptive remainder is not in the cited page and is presented as sourced.

Scope: S069 row (corpus/SOURCES.md:75) and its Gate row (corpus/lessons/round-20.md:44), checked against https://docs.python.org/3/library/pathlib.html, re-fetched by me 2026-10-21T11:01:23Z.

## Per-field verdicts

| Field | Verdict | Basis |
|---|---|---|
| Row identity (SOURCES.md:75, 11 columns, URL, opened 2026-10-21) | HOLDS | URL equals the Gate row URL and the effective fetch URL; opened date equals fetch date |
| Quote verbatim | HOLDS | exact match in the live page text; exactly one occurrence |
| Quote at the stated location | HOLDS (locator imprecise) | Inside PurePath.relative_to, in the Warning admonition (offset 17806) that names the walk_up option; quote at 17964. It is not inside the "When walk_up is false" paragraph (17158), so "walk_up paragraph" is a loose locator |
| <=25 words | HOLDS | 17 words |
| Tier A honest for scope | HOLDS | Official Python 3.15.0 docs are the primary source for pathlib's string-only behavior and the walk_up symlink caveat. Scope as written is documented behavior only |
| Teaches grounded | BROKEN | Clause 1 holds; clauses 2 and 3 are not in S069. See section A |
| Status / used-by consistent | HOLDS | status "mined" with a non-empty used-by; corpus/knowledge/wave-settlement-r20.md exists and cites S069 at line 6. Completeness gap in section B |
| Version label "Python 3.15.0 docs" | HOLDS | raw <title>: "pathlib — Object-oriented filesystem paths — Python 3.15.0 documentation" |

## A. "teaches grounded": BROKEN

Teaching (SOURCES.md:75): "String-only containment cannot see symlinks: reject absolute and .. lexically before any filesystem call, and test symlinks separately."

1. Clause "String-only containment cannot see symlinks": GROUNDED. Warning at offset 17806: "This function is part of PurePath and works with strings. It does not check or access the underlying file structure. This can impact the walk_up option as it assumes that no symlinks are present in the path; call resolve() first if necessary to resolve symlinks."
2. Clause "reject absolute and .. lexically before any filesystem call": NOT STATED. The page has zero hits for "reject", "before any filesystem", and "separately". What it does say: an absolute segment causes earlier segments to be ignored (offset 4700, PurePath class; this passage is not named in the row's anchor). ".." is not collapsed, because a naive collapse is wrong if foo is a symlink (offsets 5116 and 5542). These are hazards, not an instruction to reject.
3. Clause "test symlinks separately": NOT STATED as a containment remedy. The page documents Path.lstat() (offset 28056) and Path.is_symlink() (offset 29651) as ordinary methods, but its only containment-related symlink remedy is "call resolve() first if necessary to resolve symlinks" (offset 17964). The teaching omits that remedy.
4. Origin of the prescriptive clauses: the lane's C2 tool, not S069. tools/mori-wave-settlement.py:152-170 (`_safe_report_path`) rejects os.path.isabs / ntpath.isabs (:154-156) and ".." components (:158-160), then runs a lexical commonpath check (:162-167). :173-201 (`_inspect_report_path`) lstat's each component. Docstring at :153: "Validate the lexical path before performing any filesystem lookup." The tool cites no S-id and does not use pathlib (grep for S0[0-9][0-9]|pathlib|PurePath|walk_up: no matches). [INFERENCE] The teaching was written to describe this rule; no corpus record shows that derivation.

Suggested fix for L1 (not applied; read-only seat): restate the teaching to the documented facts: string-only; walk_up assumes no symlinks; resolve() first when symlinks matter; ".." is not collapsed because foo/../bar differs from bar when foo is a symlink; an absolute segment discards earlier segments. If the rejection and per-component lstat policy stays, label it as the lane's design [INFERENCE], or cite S068 for the lstat part. If the absolute-segment point stays, add its offset-4700 passage to the anchor.

## B. status / used-by

- corpus/knowledge/wave-settlement-r20.md exists (5375 bytes; sha256 8d1cb3d46fd18708...). Line 6: "Sources: S068 (...), S069 (pathlib lexical vs resolved containment), ...". It cites S069. HOLDS.
- The note's only S069 mention is that header gloss. Its containment rule at line 32 ("trailer absolute, contains `..`, or escapes the root | unsafe") matches the row's teaching. [INFERENCE] The rule relies on S069.
- Completeness (non-blocking): corpus/lessons/round-20.md cites S069 at line 16 (Claims) and line 44 (Gate) but is not in used-by. The same omission holds for S068 and S071 this round (lesson lines 16/43 and 16/46). Earlier rows do list lessons (S001, S064), so the convention is inconsistent.

## C. Other observations

- S069 has no pinned digest, unlike S066 and S070. The lesson at round-20.md:49 says all seven quotes matched byte-for-text. My check covers the live page, not the lane's opened copy. [INFERENCE] The opened copy equals the live page.
- Both anchors resolve to real text: "PurePath.relative_to, walk_up paragraph" (heading at 16544; walk_up paragraph at 17158; Warning at 17806) and "PurePath section on foo/../bar" (5116).

## Evidence

1. `curl -sSL --max-time 90 -A "Mozilla/5.0 (X11; Linux x86_64)" -o pathlib.html -w 'http=%{http_code} bytes=%{size_download} effective=%{url_effective}\n' https://docs.python.org/3/library/pathlib.html` gave `http=200 bytes=271189 effective=https://docs.python.org/3/library/pathlib.html`, exit 0. `date -u` gave 2026-10-21T11:01:23Z. `sha256sum` gave e88b811a22d4c0d6af06313ed773b6ea0afcab44ec7d2843225db4956d9a3544.
2. Python stdlib (html.parser and re) over /tmp/ReopenS069/pathlib.html: `quote exact in flattened text: True`; quote word count 17; one occurrence.
3. Offsets are in whitespace-normalized text (NBSP mapped to space): PurePath class heading 3943; absolute-segment sentence 4700; foo/../bar caveat 5116; naive-approach sentence 5542; relative_to heading 16544; walk_up paragraph 17158; Warning 17806; quote 17964; Path.lstat() 28056; Path.is_symlink() 29651.
4. Prescriptive-language probe on the page: "reject" 0 hits; "before any filesystem" 0; "separately" 0.
5. Named-file greps: corpus/knowledge/wave-settlement-r20.md `S069` gives line 6; tools/mori-wave-settlement.py `S0[0-9][0-9]|pathlib|PurePath|walk_up` gives no matches; corpus/SOURCES.md `S069` gives line 75 only; corpus/lessons/round-20.md `S069` gives lines 16 and 44.

## Tooling and scope

- No tool installs or updates. Used curl (pre-installed) and the eval kernel's Python standard library.
- Scratch only: /tmp/ReopenS069/pathlib.html and /tmp/ReopenS069/pathlib.txt. No lane production file edited. No subagents. No census run.
