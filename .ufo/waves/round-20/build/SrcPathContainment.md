# SrcPathContainment — frontier source for C2 (report-path containment)

Seat: MoriR20.SrcPathContainment (leaf scribe, no subagents). Access date: 2026-10-21.
Tools: `read` on the two Python docs URLs (rendered 3.15.0 docs). No installs, no network tools, no lane writes beyond this report.

## Sources opened

- https://docs.python.org/3/library/pathlib.html — "pathlib — Object-oriented filesystem paths", page title "Python 3.15.0 documentation". Sections read: PurePath (pure-path semantics, `..` handling), PurePath.is_relative_to, PurePath.relative_to (`walk_up`, 3.12), Path.resolve, Path.is_symlink, pathlib-vs-os.path table.
- https://docs.python.org/3/library/os.path.html — "os.path — Common pathname manipulations", page title "Python 3.15.0 documentation". Sections read: abspath, commonpath, commonprefix (deprecated 3.15), exists, islink, realpath (including `strict` and ALL_BUT_LAST / ALLOW_MISSING).

## Located quotes (verbatim; markdown code formatting removed)

Q1 (pathlib, PurePath section, after the `foo/../bar` example), 21 words:
> a naïve approach would make PurePosixPath('foo/../bar') equivalent to PurePosixPath('bar'), which is wrong if foo is a symbolic link to another directory

Q2 (pathlib, PurePath.relative_to, `walk_up` paragraph, 3.12 note), 25 words — **selected for the row**:
> This can impact the walk_up option as it assumes that no symlinks are present in the path; call resolve() first if necessary to resolve symlinks.

Q3 (os.path, realpath), 24 words, supporting caveat on non-strict evaluation:
> By default, the path is evaluated up to the first component that does not exist, is a symlink loop, or whose evaluation raises OSError.

Q4 (pathlib, Path.is_symlink), supporting the lstat-style check for the final component:
> Return True if the path points to a symbolic link, even if that symlink is broken.

Also observed, not quoted in the row: pathlib docs say `PurePath.is_relative_to` "works with strings. It does not check or access the underlying file structure." (the sentence precedes Q2 in the relative_to section), and os.path.commonpath "Unlike commonprefix(), this returns a valid path" with `ValueError` for mixed absolute/relative or different-drive inputs.

Each quote was checked against the fetched text (the word count is counted on the quote as printed). Q2 is exactly 25 words, the limit.

## Proposed SOURCES row (not written to corpus/SOURCES.md; L1 owns the registry)

Next free id observed in the registry: S065 is the last row, so the proposed id is **S066**. (The registry header is `id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`.)

```
| S066 | Python pathlib documentation — https://docs.python.org/3/library/pathlib.html | docs | A | lexical versus resolved path containment: PurePath.relative_to walk_up symlink assumption; the `..` lexical hazard and the Path.resolve() prerequisite | PurePath.relative_to, walk_up paragraph (after the 3.12 walk_up note); Python 3.15.0 docs, page opened 2026-10-21 | A string-only containment test (is_relative_to, relative_to, `..` checks) does not see filesystem symlinks; resolve() both sides first, or reject `..` lexically and check symlinks separately. | queued | 2026-10-21 | 180d | — |
```

Quote for the row (Q2, located as above): "This can impact the walk_up option as it assumes that no symlinks are present in the path; call resolve() first if necessary to resolve symlinks."

Tier A justification: official Python documentation (the language's primary reference) for the stdlib behavior the tool would call.

Status `queued` (not yet mined by a lesson or knowledge note); used-by `—` until a consumer cites it.

## What the sources ground for C2 (scoped; detection only)

1. Lexical check: `PurePath` keeps `..` components (Q1 context), so a report path string must be rejected for `..` before any join. This matches the contract's "contain no `..` component" rule and is a lexical test on the string.
2. Resolved check: `is_relative_to`/`relative_to` compare strings and do not touch the file system (pathlib docs). Containment inside the lane root therefore needs `resolve()` on both the lane root and the candidate's existing ancestors before the comparison (Q2). Using `os.path.realpath` with the default non-strict mode returns a path even when components are missing (Q3); the containment comparison still works on the joined result, but a missing component is appended unchanged, so `missing` must be decided separately, not inferred from the resolved path.
3. Symlink caveat for the report itself: `realpath`/`resolve()` follow symlinks, including the final component. The contract requires symlinks never be followed for the member's status (`unsafe`/`present`). Q4 supports checking the final component with an lstat-style test (`Path.is_symlink()` or `os.lstat`) on the un-resolved joined path, separately from the containment comparison. [INFERENCE] that the tool's member status must use the un-resolved path for the symlink test; the docs establish the behaviors, the design choice is ours.
4. `os.path.commonpath` is an alternative to `is_relative_to`: it raises `ValueError` on mixed absolute/relative inputs or different drives, which the tool must catch or avoid if it uses commonpath. [INFERENCE] which one the tool uses is an implementation choice; both need resolved inputs to be meaningful under symlinks.

## Caveats for the registry

- The quoted sentences are from the Python 3.15.0 rendering. The `walk_up` parameter is documented as 3.12+; the oracle harness should not rely on `walk_up` if the host's Python is older. [INFERENCE] host Python version not checked in this seat.
- The row's anchor cites a section heading, not a line number: the line numbers I observed are positions in my fetch artifact and are not stable across renders.
- The grep/read artifacts were used only to locate text; no quotes were paraphrased into the row.

## Other registry notes (observed, not proposed)

- S058/S064 in the existing registry already cover git plumbing; no overlap with this row.
- The registry's `Leads (unopened)` item (GNU Bash manual) is not this seat's scope and was not touched.

## Status

Complete for the assigned scope: one frontier source opened, one row proposed with a located ≤25-word quote, symlink caveat grounded by Q3/Q4. No code candidates were produced (none asked for). No lane, census, baseline, or registry file was edited.
